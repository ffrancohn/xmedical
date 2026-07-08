from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from apps.citas.models import Cita
from apps.core.views import current_institucion, institution_filter_context, selected_instituciones
from .forms import PreclinicaForm
from .models import Preclinica


class PreclinicaListView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = "preclinica/lista.html"
    context_object_name = "citas"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        from apps.core.decorators import get_profesional

        profesional = get_profesional(request.user)
        if profesional and profesional.tipo in ("enfermera", "admin"):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, "No tienes permiso para acceder a preclinica.")
        return redirect("dashboard")

    def get_queryset(self):
        qs = Cita.objects.select_related("paciente", "profesional").filter(
            fecha=timezone.localdate(), estado__in=["pendiente", "confirmada"]
        )
        instituciones, _ = selected_instituciones(self.request)
        qs = qs.filter(institucion__in=instituciones)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(institution_filter_context(self.request))
        return context


class PreclinicaRegistroView(LoginRequiredMixin, View):
    template_name = "preclinica/form.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        from apps.core.decorators import get_profesional

        profesional = get_profesional(request.user)
        if profesional and profesional.tipo in ("enfermera", "admin"):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, "No tienes permiso para registrar preclinica.")
        return redirect("dashboard")

    def get_object(self, cita):
        return Preclinica.objects.filter(cita=cita).first()

    def get(self, request, cita_id):
        cita = get_scoped_cita(request, cita_id)
        preclinica = self.get_object(cita)
        from apps.ia_predictiva.services import alertas_activas_paciente

        return render(
            request,
            self.template_name,
            {
                "cita": cita,
                "form": PreclinicaForm(instance=preclinica),
                "alertas_riesgo": alertas_activas_paciente(cita.paciente, cita.institucion),
            },
        )

    def post(self, request, cita_id):
        cita = get_scoped_cita(request, cita_id)
        institucion = cita.institucion
        preclinica = self.get_object(cita)
        form = PreclinicaForm(request.POST, instance=preclinica)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.institucion = institucion
            obj.cita = cita
            obj.save()
            cita.estado = "en_espera"
            cita.save(update_fields=["estado"])
            messages.success(request, "Preclinica registrada.")
            return redirect("preclinica_lista")
        return render(request, self.template_name, {"cita": cita, "form": form})


def get_scoped_cita(request, cita_id):
    qs = Cita.objects.all()
    institucion = current_institucion(request)
    if institucion:
        qs = qs.filter(institucion=institucion)
    return get_object_or_404(qs, pk=cita_id)
