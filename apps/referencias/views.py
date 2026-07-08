from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView

from apps.consulta.models import Consulta
from apps.core.decorators import get_profesional
from apps.core.permissions import CAN_REFERENCIAS, RoleRequiredMixin
from apps.core.views import current_institucion, institution_filter_context, selected_instituciones

from .forms import ContrarreferenciaForm, ReferenciaAgendarForm, ReferenciaForm, ReferenciaRespuestaForm
from .models import Contrarreferencia, Referencia


def scoped_referencias(request):
    qs = Referencia.objects.select_related(
        "institucion",
        "consulta_origen__cita__paciente",
        "especialidad_destino",
        "medico_referente",
        "especialista",
        "cita_derivada",
    )
    instituciones, _ = selected_instituciones(request)
    qs = qs.filter(institucion__in=instituciones)
    profesional = get_profesional(request.user)
    if request.user.is_superuser:
        return qs
    if profesional and profesional.tipo == "admin":
        return qs
    if profesional and profesional.especialidad and profesional.especialidad.nivel == "segundo":
        return qs.filter(
            Q(estado="pendiente", especialidad_destino=profesional.especialidad)
            | Q(especialista=profesional)
            | Q(medico_referente=profesional)
        )
    if profesional:
        return qs.filter(medico_referente=profesional)
    return qs.none()


class ReferenciaListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    allowed_roles = CAN_REFERENCIAS
    model = Referencia
    template_name = "referencias/lista.html"
    context_object_name = "referencias"

    def get_queryset(self):
        qs = scoped_referencias(self.request)
        estado = self.request.GET.get("estado")
        if estado:
            qs = qs.filter(estado=estado)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(institution_filter_context(self.request))
        context["estado_filtro"] = self.request.GET.get("estado", "")
        context["pendientes"] = scoped_referencias(self.request).filter(estado="pendiente").count()
        return context


class ReferenciaCreateView(LoginRequiredMixin, View):
    template_name = "referencias/form.html"

    def dispatch(self, request, *args, **kwargs):
        profesional = get_profesional(request.user)
        if request.user.is_superuser or (profesional and profesional.tipo == "medico"):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, "Solo los medicos pueden crear referencias.")
        return redirect("dashboard")

    def get_consulta(self, request, consulta_id):
        institucion = current_institucion(request)
        qs = Consulta.objects.select_related("cita__paciente", "cita__profesional")
        if institucion:
            qs = qs.filter(institucion=institucion)
        return get_object_or_404(qs, pk=consulta_id)

    def get(self, request, consulta_id):
        consulta = self.get_consulta(request, consulta_id)
        institucion = consulta.institucion
        return render(
            request,
            self.template_name,
            {
                "form": ReferenciaForm(institucion=institucion),
                "consulta": consulta,
                "paciente": consulta.cita.paciente,
            },
        )

    def post(self, request, consulta_id):
        consulta = self.get_consulta(request, consulta_id)
        institucion = consulta.institucion
        profesional = get_profesional(request.user)
        if not profesional and not request.user.is_superuser:
            messages.error(request, "No se pudo identificar al medico referente.")
            return redirect("dashboard")
        form = ReferenciaForm(request.POST, institucion=institucion)
        if form.is_valid():
            referencia = form.save(commit=False)
            referencia.institucion = institucion
            referencia.consulta_origen = consulta
            referencia.medico_referente = profesional or consulta.cita.profesional
            referencia.save()
            consulta.conducta = "referencia"
            consulta.save(update_fields=["conducta"])
            messages.success(request, "Referencia creada correctamente.")
            return redirect("referencias_detalle", pk=referencia.pk)
        return render(
            request,
            self.template_name,
            {"form": form, "consulta": consulta, "paciente": consulta.cita.paciente},
        )


class ReferenciaDetailView(LoginRequiredMixin, View):
    template_name = "referencias/detalle.html"

    def get(self, request, pk):
        referencia = get_object_or_404(scoped_referencias(request), pk=pk)
        return render(
            request,
            self.template_name,
            {
                "referencia": referencia,
                "contrarreferencia": getattr(referencia, "contrarreferencia", None),
                "respuesta_form": ReferenciaRespuestaForm(),
            },
        )


class ReferenciaAceptarView(LoginRequiredMixin, View):
    def post(self, request, pk):
        referencia = get_object_or_404(scoped_referencias(request), pk=pk, estado="pendiente")
        profesional = get_profesional(request.user)
        if not request.user.is_superuser:
            if not profesional or profesional.especialidad_id != referencia.especialidad_destino_id:
                messages.error(request, "Solo el especialista de destino puede aceptar esta referencia.")
                return redirect("referencias_detalle", pk=pk)
        form = ReferenciaRespuestaForm(request.POST)
        if form.is_valid():
            referencia.estado = "aceptada"
            referencia.especialista = profesional
            referencia.comentarios_especialista = form.cleaned_data.get("comentarios_especialista", "")
            referencia.save()
            messages.success(request, "Referencia aceptada. Puedes agendar la cita.")
            return redirect("referencias_agendar", pk=pk)
        messages.error(request, "No se pudo aceptar la referencia.")
        return redirect("referencias_detalle", pk=pk)


class ReferenciaRechazarView(LoginRequiredMixin, View):
    def post(self, request, pk):
        referencia = get_object_or_404(scoped_referencias(request), pk=pk, estado="pendiente")
        profesional = get_profesional(request.user)
        if not request.user.is_superuser:
            if not profesional or profesional.especialidad_id != referencia.especialidad_destino_id:
                messages.error(request, "Solo el especialista de destino puede rechazar esta referencia.")
                return redirect("referencias_detalle", pk=pk)
        form = ReferenciaRespuestaForm(request.POST)
        if form.is_valid():
            referencia.estado = "rechazada"
            referencia.especialista = profesional
            referencia.comentarios_especialista = form.cleaned_data.get("comentarios_especialista", "")
            referencia.save()
            messages.info(request, "Referencia rechazada.")
            return redirect("referencias_lista")
        messages.error(request, "No se pudo rechazar la referencia.")
        return redirect("referencias_detalle", pk=pk)


class ReferenciaAgendarView(LoginRequiredMixin, View):
    template_name = "referencias/agendar.html"

    def get(self, request, pk):
        referencia = get_object_or_404(scoped_referencias(request), pk=pk, estado="aceptada")
        if referencia.cita_derivada_id:
            messages.info(request, "Esta referencia ya tiene una cita asignada.")
            return redirect("referencias_detalle", pk=pk)
        form = ReferenciaAgendarForm(institucion=referencia.institucion, referencia=referencia)
        return render(request, self.template_name, {"form": form, "referencia": referencia})

    def post(self, request, pk):
        referencia = get_object_or_404(scoped_referencias(request), pk=pk, estado="aceptada")
        form = ReferenciaAgendarForm(request.POST, institucion=referencia.institucion, referencia=referencia)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.institucion = referencia.institucion
            cita.paciente = referencia.paciente
            cita.profesional = referencia.especialista or form.cleaned_data["profesional"]
            cita.tipo_agendamiento = "especifico"
            cita.estado = "confirmada"
            cita.save()
            referencia.cita_derivada = cita
            referencia.save(update_fields=["cita_derivada"])
            messages.success(request, "Cita agendada desde la referencia.")
            return redirect("referencias_detalle", pk=pk)
        return render(request, self.template_name, {"form": form, "referencia": referencia})


class ContrarreferenciaCreateView(LoginRequiredMixin, View):
    template_name = "referencias/contrarreferencia_form.html"

    def get(self, request, pk):
        referencia = get_object_or_404(scoped_referencias(request), pk=pk, estado="aceptada")
        if hasattr(referencia, "contrarreferencia"):
            messages.info(request, "Ya existe una contrarreferencia para esta referencia.")
            return redirect("referencias_detalle", pk=pk)
        return render(
            request,
            self.template_name,
            {"form": ContrarreferenciaForm(), "referencia": referencia},
        )

    def post(self, request, pk):
        referencia = get_object_or_404(scoped_referencias(request), pk=pk, estado="aceptada")
        profesional = get_profesional(request.user)
        if not request.user.is_superuser and (not profesional or referencia.especialista_id != profesional.id):
            messages.error(request, "Solo el especialista asignado puede crear la contrarreferencia.")
            return redirect("referencias_detalle", pk=pk)
        form = ContrarreferenciaForm(request.POST)
        if form.is_valid():
            contrarreferencia = form.save(commit=False)
            contrarreferencia.institucion = referencia.institucion
            contrarreferencia.referencia = referencia
            contrarreferencia.creado_por = profesional or referencia.especialista
            contrarreferencia.save()
            referencia.estado = "completada"
            referencia.save(update_fields=["estado"])
            messages.success(request, "Contrarreferencia enviada al primer nivel.")
            return redirect("referencias_detalle", pk=pk)
        return render(request, self.template_name, {"form": form, "referencia": referencia})
