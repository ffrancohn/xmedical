from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from apps.citas.models import Cita
from apps.citas.services import FlexibleAgendamientoService, SinTurnosDisponiblesError
from apps.core.views import current_institucion

from .decorators import PacienteRequiredMixin, get_perfil_paciente, paciente_required
from .forms import PortalCitaFlexibleForm, PortalRegistroForm
from .services import consultas_para_paciente, exportar_hce_json, exportar_hce_pdf


class PortalRegistroView(View):
    template_name = "portal_paciente/registro.html"

    def get(self, request):
        institucion = current_institucion(request)
        if not institucion:
            messages.error(request, "Selecciona una institucion valida para registrarte.")
            return redirect("home")
        if request.user.is_authenticated and get_perfil_paciente(request.user, institucion):
            return redirect("portal_dashboard")
        return render(
            request,
            self.template_name,
            {"form": PortalRegistroForm(institucion=institucion), "institucion": institucion},
        )

    def post(self, request):
        institucion = current_institucion(request)
        if not institucion:
            messages.error(request, "No se pudo identificar la institucion.")
            return redirect("home")
        form = PortalRegistroForm(request.POST, institucion=institucion)
        if form.is_valid():
            perfil = form.save()
            request.session["institucion_id"] = institucion.id
            messages.success(request, "Cuenta creada. Ya puedes iniciar sesion en el portal.")
            return redirect("login")
        return render(request, self.template_name, {"form": form, "institucion": institucion})


class PortalDashboardView(LoginRequiredMixin, PacienteRequiredMixin, View):
    template_name = "portal_paciente/dashboard.html"

    def get(self, request):
        perfil = request.perfil_paciente
        hoy = timezone.localdate()
        proximas = (
            Cita.objects.select_related("profesional", "profesional__especialidad")
            .filter(
                paciente=perfil.paciente,
                institucion=perfil.institucion,
                fecha__gte=hoy,
            )
            .exclude(estado__in=["cancelada", "atendida"])
            .order_by("fecha", "hora")[:5]
        )
        return render(
            request,
            self.template_name,
            {"perfil": perfil, "proximas": proximas},
        )


class PortalCitasView(LoginRequiredMixin, PacienteRequiredMixin, View):
    template_name = "portal_paciente/citas.html"

    def get(self, request):
        perfil = request.perfil_paciente
        hoy = timezone.localdate()
        citas = (
            Cita.objects.select_related("profesional", "profesional__especialidad")
            .filter(paciente=perfil.paciente, institucion=perfil.institucion)
            .order_by("-fecha", "-hora")
        )
        proximas = citas.filter(fecha__gte=hoy).exclude(estado__in=["cancelada", "atendida"])
        historial = citas.filter(fecha__lt=hoy) | citas.filter(
            estado__in=["cancelada", "atendida"]
        )
        historial = historial.distinct().order_by("-fecha", "-hora")
        return render(
            request,
            self.template_name,
            {
                "perfil": perfil,
                "proximas": proximas,
                "historial": historial,
                "hoy": hoy,
            },
        )


@login_required
@paciente_required
def portal_cancelar_cita(request, pk):
    perfil = request.perfil_paciente
    cita = get_object_or_404(
        Cita,
        pk=pk,
        paciente=perfil.paciente,
        institucion=perfil.institucion,
    )
    if cita.estado in ("cancelada", "atendida"):
        messages.error(request, "Esta cita no puede cancelarse.")
        return redirect("portal_citas")
    cita_datetime = timezone.make_aware(datetime.combine(cita.fecha, cita.hora))
    if cita_datetime - timezone.now() < timedelta(hours=2):
        messages.error(request, "Las citas solo pueden cancelarse con al menos 2 horas de anticipacion.")
        return redirect("portal_citas")
    cita.estado = "cancelada"
    cita.save(update_fields=["estado"])
    messages.info(request, "Cita cancelada correctamente.")
    return redirect("portal_citas")


@login_required
@paciente_required
def portal_llegada_cita(request, pk):
    perfil = request.perfil_paciente
    cita = get_object_or_404(
        Cita,
        pk=pk,
        paciente=perfil.paciente,
        institucion=perfil.institucion,
    )
    hoy = timezone.localdate()
    if cita.fecha != hoy:
        messages.error(request, "Solo puedes registrar llegada para citas de hoy.")
        return redirect("portal_citas")
    if cita.estado in ("cancelada", "atendida"):
        messages.error(request, "Esta cita no admite registro de llegada.")
        return redirect("portal_citas")
    cita.estado = "en_espera"
    cita.save(update_fields=["estado"])
    messages.success(request, "Llegada registrada. El personal de la clinica fue notificado.")
    return redirect("portal_citas")


class PortalHistoriaView(LoginRequiredMixin, PacienteRequiredMixin, View):
    template_name = "portal_paciente/historia.html"

    def get(self, request):
        perfil = request.perfil_paciente
        consultas = consultas_para_paciente(perfil.paciente, perfil.institucion)
        return render(
            request,
            self.template_name,
            {"perfil": perfil, "consultas": consultas},
        )


@login_required
@paciente_required
def portal_exportar_hce(request, formato):
    perfil = request.perfil_paciente
    if formato == "json":
        contenido = exportar_hce_json(perfil.paciente, perfil.institucion)
        response = HttpResponse(contenido, content_type="application/json; charset=utf-8")
        response["Content-Disposition"] = (
            f'attachment; filename="hce_{perfil.paciente.documento}.json"'
        )
        return response
    if formato == "pdf":
        contenido = exportar_hce_pdf(perfil.paciente, perfil.institucion)
        response = HttpResponse(contenido, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="hce_{perfil.paciente.documento}.pdf"'
        )
        return response
    return JsonResponse({"error": "Formato no soportado"}, status=400)


class PortalSolicitarCitaView(LoginRequiredMixin, PacienteRequiredMixin, View):
    template_name = "portal_paciente/solicitar_cita.html"
    resultado_template = "portal_paciente/cita_confirmada.html"

    def get(self, request):
        perfil = request.perfil_paciente
        form = PortalCitaFlexibleForm(institucion=perfil.institucion)
        return render(request, self.template_name, {"form": form, "perfil": perfil})

    def post(self, request):
        perfil = request.perfil_paciente
        form = PortalCitaFlexibleForm(request.POST, institucion=perfil.institucion)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form, "perfil": perfil})

        servicio = FlexibleAgendamientoService(perfil.institucion)
        try:
            cita = servicio.asignar_primer_turno(
                paciente=perfil.paciente,
                especialidad=form.cleaned_data["especialidad"],
                fecha_inicio=form.cleaned_data["fecha_inicio"],
                fecha_fin=form.cleaned_data["fecha_fin"],
                jornada=form.cleaned_data["jornada"],
                profesional=form.cleaned_data.get("profesional"),
            )
        except SinTurnosDisponiblesError as exc:
            messages.error(request, str(exc))
            return render(request, self.template_name, {"form": form, "perfil": perfil, "sin_turnos": True})

        messages.success(request, "Cita solicitada y confirmada automaticamente.")
        return render(
            request,
            self.resultado_template,
            {"cita": cita, "perfil": perfil},
        )
