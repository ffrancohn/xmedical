from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.decorators import get_profesional
from apps.core.permissions import (
    CAN_DASHBOARD_ADMIN,
    CAN_DASHBOARD_ENFERMERIA,
    CAN_DASHBOARD_EPIDEMIOLOGIA,
    CAN_DASHBOARD_RECEPCION,
    RoleRequiredMixin,
)
from apps.core.views import institution_filter_context, selected_instituciones

from .epidemiologia import epidemiologia_dashboard_data
from .hilo import hilo_del_dia
from .services import administracion_dashboard_data, enfermeria_dashboard_data, especialista_dashboard_data


class InstitutionFilterMixin:
    def get_instituciones(self):
        instituciones, _ = selected_instituciones(self.request)
        return instituciones

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(institution_filter_context(self.request))
        return context


class EnfermeriaDashboardView(LoginRequiredMixin, RoleRequiredMixin, InstitutionFilterMixin, TemplateView):
    allowed_roles = CAN_DASHBOARD_ENFERMERIA
    template_name = "dashboards/enfermeria.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(enfermeria_dashboard_data(self.get_instituciones()))
        profesional = get_profesional(self.request.user)
        if profesional and profesional.tipo == "enfermera":
            context["hilo"] = hilo_del_dia(self.get_instituciones(), "enfermeria")
        return context


class RecepcionDashboardView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    allowed_roles = CAN_DASHBOARD_RECEPCION
    template_name = "dashboards/recepcion.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect("superadmin_dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instituciones, _ = selected_instituciones(self.request)
        context["hilo"] = hilo_del_dia(instituciones, "recepcion")
        pref = getattr(self.request.user, "preference", None)
        if pref and pref.interface_mode == "atlas":
            from apps.core.atlas_catalog import modules_for_hub
            from apps.core.atlas_explore import citas_exploracion, pacientes_exploracion

            inst = instituciones[0] if len(instituciones) == 1 else None
            context["atlas_modules"] = modules_for_hub(self.request.user)
            context["pacientes_explore"] = pacientes_exploracion(instituciones, inst)
            context["citas_explore"] = citas_exploracion(instituciones)
            context["atlas_hub"] = True
        return context


class AdministracionDashboardView(LoginRequiredMixin, RoleRequiredMixin, InstitutionFilterMixin, TemplateView):
    allowed_roles = CAN_DASHBOARD_ADMIN
    template_name = "dashboards/administracion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(administracion_dashboard_data(self.get_instituciones()))
        return context


class EspecialistaDashboardView(LoginRequiredMixin, InstitutionFilterMixin, TemplateView):
    template_name = "dashboards/especialista.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        profesional = get_profesional(request.user)
        if profesional and profesional.tipo == "medico" and profesional.especialidad and profesional.especialidad.nivel == "segundo":
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, "No tienes permiso para ver este dashboard.")
        return redirect("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profesional = get_profesional(self.request.user)
        context["profesional"] = profesional
        context.update(especialista_dashboard_data(self.get_instituciones(), profesional=profesional))
        if profesional and profesional.tipo == "medico":
            context["hilo"] = hilo_del_dia(self.get_instituciones(), "especialista")

        preference = getattr(self.request.user, "preference", None)
        use_atlas = bool(preference and preference.interface_mode == "atlas") and not self.request.GET.get(
            "classic"
        )
        if use_atlas:
            from django.urls import reverse

            from apps.core.atlas_explore import (
                agenda_exploracion,
                espera_exploracion,
                referencias_exploracion,
            )
            from apps.core.atlas_scene import construir_escena_especialista

            instituciones = self.get_instituciones()
            agenda = agenda_exploracion(instituciones, profesional)
            espera = espera_exploracion(instituciones, profesional)
            referencias = referencias_exploracion(instituciones, profesional)
            context["atlas_scene"] = construir_escena_especialista(
                agenda,
                espera,
                referencias,
                urls={
                    "citas": reverse("citas_lista"),
                    "preclinica": reverse("preclinica_lista"),
                    "pacientes": reverse("pacientes_lista"),
                    "referencias": reverse("referencias_lista"),
                },
                perfil=profesional.nombre if profesional else "Vista global",
                especialidad=(
                    profesional.especialidad.nombre
                    if profesional and profesional.especialidad
                    else ""
                ),
            )
        return context


class EpidemiologiaDashboardView(LoginRequiredMixin, RoleRequiredMixin, InstitutionFilterMixin, TemplateView):
    allowed_roles = CAN_DASHBOARD_EPIDEMIOLOGIA
    template_name = "dashboards/epidemiologia.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(epidemiologia_dashboard_data(self.get_instituciones()))
        return context
