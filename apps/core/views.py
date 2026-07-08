import json

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import ListView, TemplateView

from apps.citas.models import Cita
from apps.consulta.models import Consulta
from apps.core.backup_utils import create_global_backup, create_institution_backup, restore_fixture
from apps.core.decorators import get_profesional
from apps.core.models import BackupLog, Institucion, LogAuditoria, Profesional
from apps.core.tenant_transfer import (
    TenantTransferError,
    export_tenant_json,
    import_tenant_package,
    log_tenant_operation,
    tenant_stats,
)
from apps.pacientes.models import Paciente
from apps.portal_paciente.decorators import get_perfil_paciente


def current_institucion(request):
    if getattr(request, "institucion", None):
        return request.institucion
    if request.user.is_authenticated and request.user.is_superuser:
        return None
    institucion_id = request.session.get("institucion_id")
    if institucion_id:
        return Institucion.objects.filter(id=institucion_id, activo=True).first()
    institucion = Institucion.objects.filter(activo=True).first()
    if institucion:
        request.session["institucion_id"] = institucion.id
    return institucion


def selected_instituciones(request):
    """Return institutions visible for list screens, with multi-select for superadmins."""
    if request.user.is_authenticated and request.user.is_superuser:
        ids = [value for value in request.GET.getlist("instituciones") if value]
        qs = Institucion.objects.filter(activo=True).order_by("nombre")
        if ids:
            qs = qs.filter(id__in=ids)
        return qs, ids
    institucion = current_institucion(request)
    if institucion:
        return Institucion.objects.filter(id=institucion.id), [str(institucion.id)]
    return Institucion.objects.none(), []


def institution_filter_context(request):
    all_instituciones = Institucion.objects.filter(activo=True).order_by("nombre")
    _, selected_ids = selected_instituciones(request)
    return {
        "is_superadmin_view": request.user.is_authenticated and request.user.is_superuser,
        "all_instituciones": all_instituciones,
        "selected_instituciones": selected_ids,
    }


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard_medico.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect("superadmin_dashboard")
        perfil = get_perfil_paciente(request.user, current_institucion(request))
        if perfil:
            return redirect("portal_dashboard")
        profesional = Profesional.objects.filter(usuario=request.user, activo=True).first()
        if profesional and profesional.tipo == "recepcionista":
            return redirect("citas_agendar")
        if profesional and profesional.tipo == "enfermera":
            return redirect("dashboards_enfermeria")
        if profesional and profesional.tipo == "admin":
            return redirect("dashboards_administracion")
        if (
            profesional
            and profesional.tipo == "medico"
            and profesional.especialidad
            and profesional.especialidad.nivel == "segundo"
        ):
            return redirect("dashboards_especialista")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        institucion = current_institucion(request)
        profesional = Profesional.objects.filter(usuario=request.user, activo=True).first()
        citas = Cita.objects.select_related("paciente", "profesional").filter(fecha=timezone.localdate())
        if institucion:
            citas = citas.filter(institucion=institucion)
        if profesional and profesional.tipo == "medico":
            citas = citas.filter(profesional=profesional)
        context["profesional"] = profesional
        context["citas_hoy"] = citas.order_by("hora")
        context["pacientes_espera"] = citas.filter(estado__in=["pendiente", "confirmada", "en_espera"])
        context["atendidos"] = citas.filter(estado="atendida").count()
        return context


def home(request):
    if request.user.is_authenticated:
        if get_perfil_paciente(request.user, current_institucion(request)):
            return redirect("portal_dashboard")
        return redirect("dashboard")
    return render(request, "home.html")


def is_superadmin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_superadmin)
def superadmin_dashboard(request):
    instituciones = Institucion.objects.all().order_by("nombre")
    rows = []
    for institucion in instituciones:
        rows.append(
            {
                "institucion": institucion,
                "profesionales": Profesional.objects.filter(institucion=institucion, activo=True).count(),
                "pacientes": Paciente.objects.filter(institucion=institucion, activo=True).count(),
                "citas": Cita.objects.filter(institucion=institucion).count(),
                "consultas": Consulta.objects.filter(institucion=institucion).count(),
            }
        )
    context = {
        "instituciones": instituciones,
        "rows": rows,
        "total_instituciones": instituciones.count(),
        "total_pacientes": Paciente.objects.count(),
        "total_citas": Cita.objects.count(),
        "total_consultas": Consulta.objects.count(),
        "backup_logs": BackupLog.objects.select_related("institucion", "usuario")[:10],
    }
    return render(request, "core/superadmin_dashboard.html", context)


class AuditoriaListView(LoginRequiredMixin, ListView):
    model = LogAuditoria
    template_name = "core/auditoria_lista.html"
    context_object_name = "registros"
    paginate_by = 50

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        profesional = get_profesional(request.user)
        if profesional and profesional.tipo == "admin":
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, "No tienes permiso para ver la auditoria.")
        return redirect("dashboard")

    def get_queryset(self):
        qs = LogAuditoria.objects.select_related("institucion", "usuario")
        if self.request.user.is_superuser:
            institucion_id = self.request.GET.get("institucion")
            if institucion_id:
                qs = qs.filter(institucion_id=institucion_id)
            return qs
        institucion = current_institucion(self.request)
        if institucion:
            qs = qs.filter(institucion=institucion)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_instituciones"] = Institucion.objects.filter(activo=True).order_by("nombre")
        context["is_superadmin_view"] = self.request.user.is_superuser
        return context


@user_passes_test(is_superadmin)
def superadmin_backup(request):
    if request.method != "POST":
        return redirect("superadmin_dashboard")
    alcance = request.POST.get("alcance")
    institucion = None
    if alcance == "institucion":
        institucion = get_object_or_404(Institucion, pk=request.POST.get("institucion_id"))
        path = create_institution_backup(institucion, request.user)
    else:
        path = create_global_backup(request.user)
    messages.success(request, f"Respaldo creado: {path}")
    return redirect("superadmin_dashboard")


@user_passes_test(is_superadmin)
def superadmin_restore(request):
    if request.method != "POST":
        return redirect("superadmin_dashboard")
    alcance = request.POST.get("alcance", "global")
    institucion = None
    if alcance == "institucion" and request.POST.get("institucion_id"):
        institucion = get_object_or_404(Institucion, pk=request.POST.get("institucion_id"))
    uploaded_file = request.FILES.get("archivo")
    if not uploaded_file:
        messages.error(request, "Selecciona un archivo JSON para restaurar.")
        return redirect("superadmin_dashboard")
    path = restore_fixture(uploaded_file, alcance, request.user, institucion)
    messages.success(request, f"Restauracion aplicada desde: {path}")
    return redirect("superadmin_dashboard")


@user_passes_test(is_superadmin)
def superadmin_export_tenant(request, institucion_id):
    institucion = get_object_or_404(Institucion, pk=institucion_id)
    contenido = export_tenant_json(institucion)
    log_tenant_operation(
        "backup",
        institucion,
        request.user,
        detalle="Descarga directa de paquete tenant.",
    )
    response = HttpResponse(contenido, content_type="application/json; charset=utf-8")
    response["Content-Disposition"] = (
        f'attachment; filename="xmedical_tenant_{institucion.subdominio}_{timezone.localtime():%Y%m%d}.json"'
    )
    return response


@user_passes_test(is_superadmin)
def superadmin_import_tenant(request):
    if request.method != "POST":
        return redirect("superadmin_dashboard")
    uploaded_file = request.FILES.get("archivo")
    if not uploaded_file:
        messages.error(request, "Selecciona un archivo JSON de tenant.")
        return redirect("superadmin_dashboard")

    try:
        package = json.loads(uploaded_file.read().decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        messages.error(request, "El archivo no es un JSON valido.")
        return redirect("superadmin_dashboard")

    mode = request.POST.get("modo", "new")
    nombre = request.POST.get("nombre", "").strip() or None
    subdominio = request.POST.get("subdominio", "").strip() or None
    target_institucion = None
    if mode == "replace":
        target_institucion = get_object_or_404(Institucion, pk=request.POST.get("institucion_id"))

    try:
        institucion, _ = import_tenant_package(
            package,
            mode=mode,
            nombre=nombre,
            subdominio=subdominio,
            target_institucion=target_institucion,
        )
    except TenantTransferError as exc:
        messages.error(request, str(exc))
        return redirect("superadmin_dashboard")

    log_tenant_operation(
        "restore",
        institucion,
        request.user,
        detalle=f"Importacion tenant modo={mode}.",
    )
    stats = tenant_stats(institucion)
    messages.success(
        request,
        f"Tenant importado: {institucion.nombre} ({institucion.subdominio}). "
        f"Pacientes: {stats['pacientes']}, citas: {stats['citas']}, consultas: {stats['consultas']}.",
    )
    return redirect("superadmin_dashboard")
