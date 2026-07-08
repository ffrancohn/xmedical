from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.decorators import get_profesional
from apps.core.views import institution_filter_context, selected_instituciones

from .services import administracion_dashboard_data, enfermeria_dashboard_data, especialista_dashboard_data


class InstitutionFilterMixin:
    def get_instituciones(self):
        instituciones, _ = selected_instituciones(self.request)
        return instituciones

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(institution_filter_context(self.request))
        return context


class EnfermeriaDashboardView(LoginRequiredMixin, InstitutionFilterMixin, TemplateView):
    template_name = "dashboards/enfermeria.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        profesional = get_profesional(request.user)
        if profesional and profesional.tipo in ("enfermera", "admin"):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, "No tienes permiso para ver este dashboard.")
        return redirect("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(enfermeria_dashboard_data(self.get_instituciones()))
        return context


class AdministracionDashboardView(LoginRequiredMixin, InstitutionFilterMixin, TemplateView):
    template_name = "dashboards/administracion.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        profesional = get_profesional(request.user)
        if profesional and profesional.tipo == "admin":
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, "No tienes permiso para ver este dashboard.")
        return redirect("dashboard")

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
        return context
