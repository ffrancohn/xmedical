from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from apps.core.permissions import CAN_VIEW_HISTORIA, CAN_VIEW_PACIENTES, CAN_EDIT_PACIENTES, role_required, user_has_role
from apps.core.views import current_institucion, institution_filter_context, selected_instituciones
from .forms import PacienteForm, PacientePublicForm
from .models import Paciente


def can_view_pacientes(user):
    return user_has_role(user, *CAN_VIEW_PACIENTES)


def can_manage_pacientes(user):
    return user_has_role(user, *CAN_EDIT_PACIENTES)


class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = "pacientes/lista.html"
    context_object_name = "pacientes"

    def dispatch(self, request, *args, **kwargs):
        if can_view_pacientes(request.user):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, "No tienes permiso para acceder a pacientes.")
        return redirect("dashboard")

    def get_queryset(self):
        qs = Paciente.objects.filter(activo=True)
        instituciones, _ = selected_instituciones(self.request)
        qs = qs.filter(institucion__in=instituciones)
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(documento__icontains=q)
                | Q(nombre__icontains=q)
                | Q(apellido__icontains=q)
                | Q(telefono__icontains=q)
                | Q(telefono_fijo__icontains=q)
            )
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

    def dispatch(self, request, *args, **kwargs):
        if can_manage_pacientes(request.user):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, "No tienes permiso para registrar pacientes.")
        return redirect("dashboard")

    def get_initial(self):
        initial = super().get_initial()
        data = self.request.session.pop("ocr_paciente_data", None)
        if data and data.get("confirmado"):
            initial.update(
                {
                    "documento": data.get("documento", ""),
                    "nombre": data.get("nombre", ""),
                    "apellido": data.get("apellido", ""),
                    "fecha_nacimiento": data.get("fecha_nacimiento") or None,
                    "sexo": data.get("sexo", ""),
                }
            )
        return initial

    def form_valid(self, form):
        form.instance.institucion = current_institucion(self.request)
        return super().form_valid(form)


class PacienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "pacientes/form.html"
    success_url = "/pacientes/"

    def dispatch(self, request, *args, **kwargs):
        if can_manage_pacientes(request.user):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, "No tienes permiso para editar pacientes.")
        return redirect("dashboard")

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

    def dispatch(self, request, *args, **kwargs):
        if can_view_pacientes(request.user):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, "No tienes permiso para ver pacientes.")
        return redirect("dashboard")

    def get_queryset(self):
        qs = super().get_queryset()
        institucion = current_institucion(self.request)
        if institucion:
            qs = qs.filter(institucion=institucion)
        return qs


class PacientePublicRegistroView(View):
    template_name = "pacientes/registro_publico.html"

    def get(self, request):
        institucion = current_institucion(request)
        if not institucion:
            messages.error(request, "Selecciona una institucion valida para registrarte.")
            return redirect("home")
        return render(request, self.template_name, {"form": PacientePublicForm(), "institucion": institucion})

    def post(self, request):
        institucion = current_institucion(request)
        if not institucion:
            messages.error(request, "No se pudo identificar la institucion.")
            return redirect("home")
        form = PacientePublicForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.institucion = institucion
            paciente.activo = True
            paciente.save()
            messages.success(
                request,
                "Registro completado. Acude a recepcion con tu documento para confirmar tu cita.",
            )
            return redirect("home")
        return render(request, self.template_name, {"form": form, "institucion": institucion})


@login_required
@role_required(*CAN_VIEW_HISTORIA)
def paciente_historia_redirect(request, pk):
    qs = Paciente.objects.all()
    institucion = current_institucion(request)
    if institucion:
        qs = qs.filter(institucion=institucion)
    paciente = get_object_or_404(qs, pk=pk)
    return redirect("historia_clinica", paciente_id=paciente.id)
