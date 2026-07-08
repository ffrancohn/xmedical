from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from apps.core.models import Profesional

from apps.portal_paciente.models import PerfilPaciente

from .forms import ProfesionalRegistroForm, UserPreferenceForm, XMedicalAuthenticationForm
from .models import UserPreference


class XMedicalLoginView(LoginView):
    template_name = "auth_app/login.html"
    form_class = XMedicalAuthenticationForm
    redirect_authenticated_user = True

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["show_institucion"] = not getattr(self.request, "institucion", None)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_institucion"] = not getattr(self.request, "institucion", None)
        return context

    def form_valid(self, form):
        user = form.get_user()
        institucion = getattr(self.request, "institucion", None)
        if not institucion:
            institucion = form.cleaned_data.get("institucion")
        if not institucion and not user.is_superuser:
            messages.error(self.request, "Debes seleccionar la institucion a la que perteneces.")
            return self.form_invalid(form)
        if not user.is_superuser:
            profesional = Profesional.objects.filter(
                usuario=user, institucion=institucion, activo=True
            ).first()
            perfil_paciente = PerfilPaciente.objects.filter(
                usuario=user, institucion=institucion, activo=True
            ).first()
            if not profesional and not perfil_paciente:
                messages.error(
                    self.request,
                    "Tu usuario no tiene acceso a la institucion seleccionada.",
                )
                return self.form_invalid(form)
        if institucion:
            self.request.session["institucion_id"] = institucion.id
        return super().form_valid(form)


class XMedicalLogoutView(LogoutView):
    next_page = "login"


class RegistroProfesionalView(LoginRequiredMixin, View):
    template_name = "auth_app/registro.html"

    def get(self, request):
        return render(request, self.template_name, {"form": ProfesionalRegistroForm()})

    def post(self, request):
        form = ProfesionalRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect("dashboard")
        return render(request, self.template_name, {"form": form})


class PreferenciasVisualesView(LoginRequiredMixin, View):
    template_name = "auth_app/preferencias.html"

    def get(self, request):
        preference, _ = UserPreference.objects.get_or_create(user=request.user)
        return render(request, self.template_name, {"form": UserPreferenceForm(instance=preference)})

    def post(self, request):
        preference, _ = UserPreference.objects.get_or_create(user=request.user)
        form = UserPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            messages.success(request, "Preferencias visuales actualizadas.")
            return redirect("preferencias_visuales")
        return render(request, self.template_name, {"form": form})
