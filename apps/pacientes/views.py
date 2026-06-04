from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from apps.core.views import current_institucion, institution_filter_context, selected_instituciones
from .forms import PacienteForm
from .models import Paciente


class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = "pacientes/lista.html"
    context_object_name = "pacientes"

    def get_queryset(self):
        qs = Paciente.objects.filter(activo=True)
        instituciones, _ = selected_instituciones(self.request)
        qs = qs.filter(institucion__in=instituciones)
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(documento__icontains=q) | Q(nombre__icontains=q) | Q(apellido__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(institution_filter_context(self.request))
        return context


class PacienteCreateView(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "pacientes/form.html"
    success_url = "/pacientes/"

    def form_valid(self, form):
        form.instance.institucion = current_institucion(self.request)
        return super().form_valid(form)


class PacienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "pacientes/form.html"
    success_url = "/pacientes/"

    def get_queryset(self):
        qs = super().get_queryset()
        institucion = current_institucion(self.request)
        if institucion:
            qs = qs.filter(institucion=institucion)
        return qs


class PacienteDetailView(LoginRequiredMixin, DetailView):
    model = Paciente
    template_name = "pacientes/detalle.html"
    context_object_name = "paciente"

    def get_queryset(self):
        qs = super().get_queryset()
        institucion = current_institucion(self.request)
        if institucion:
            qs = qs.filter(institucion=institucion)
        return qs


def paciente_historia_redirect(request, pk):
    qs = Paciente.objects.all()
    institucion = current_institucion(request)
    if institucion:
        qs = qs.filter(institucion=institucion)
    paciente = get_object_or_404(qs, pk=pk)
    return redirect("historia_clinica", paciente_id=paciente.id)
