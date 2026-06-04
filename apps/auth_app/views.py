from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from .forms import ProfesionalRegistroForm, UserPreferenceForm
from .models import UserPreference


class XMedicalLoginView(LoginView):
    template_name = "auth_app/login.html"


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

    def get_preference(self, request):
        preference, _ = UserPreference.objects.get_or_create(user=request.user)
        return preference

    def get(self, request):
        form = UserPreferenceForm(instance=self.get_preference(request))
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        preference = self.get_preference(request)
        form = UserPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            messages.success(request, "Preferencias visuales actualizadas.")
            return redirect("preferencias_visuales")
        return render(request, self.template_name, {"form": form})
