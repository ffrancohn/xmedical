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

    def _resolve_login_institucion(self, user, form_institucion, request_institucion):
        if request_institucion:
            return request_institucion
        if form_institucion:
            return form_institucion
        if user.is_superuser:
            return None

        perfiles = list(
            PerfilPaciente.objects.filter(usuario=user, activo=True).select_related("institucion")
        )
        profesionales = list(
            Profesional.objects.filter(usuario=user, activo=True).select_related("institucion")
        )
        if len(perfiles) == 1 and not profesionales:
            return perfiles[0].institucion
        if len(profesionales) == 1 and not perfiles:
            return profesionales[0].institucion
        if (
            len(perfiles) == 1
            and len(profesionales) == 1
            and perfiles[0].institucion_id == profesionales[0].institucion_id
        ):
            return perfiles[0].institucion
        return None

    def form_valid(self, form):
        from apps.core.db import set_institucion_rls

        set_institucion_rls(None)
        user = form.get_user()
        institucion = self._resolve_login_institucion(
            user,
            form.cleaned_data.get("institucion"),
            getattr(self.request, "institucion", None),
        )
        if not institucion and not user.is_superuser:
            messages.error(
                self.request,
                "Debes seleccionar la institución a la que perteneces.",
            )
            return self.form_invalid(form)

        from apps.core.db import set_institucion_rls

        if institucion:
            set_institucion_rls(institucion.id)

        if not user.is_superuser:
            profesional = Profesional.objects.filter(
                usuario=user, institucion=institucion, activo=True
            ).first()
            perfil_paciente = PerfilPaciente.objects.filter(
                usuario=user, institucion=institucion, activo=True
            ).first()
            if not perfil_paciente and not profesional:
                perfil_paciente = PerfilPaciente.objects.filter(
                    usuario=user, activo=True
                ).first()
                if perfil_paciente:
                    institucion = perfil_paciente.institucion
                    set_institucion_rls(institucion.id)
            if not profesional and not perfil_paciente:
                messages.error(
                    self.request,
                    "Tu usuario no tiene acceso a la institución seleccionada.",
                )
                return self.form_invalid(form)

        if institucion:
            self.request.session["institucion_id"] = institucion.id
        return super().form_valid(form)

    def get_success_url(self):
        redirect_to = self.get_redirect_url()
        user = self.request.user
        if user.is_superuser:
            return redirect_to or str(reverse_lazy("superadmin_dashboard"))
        from apps.core.views import current_institucion
        from apps.portal_paciente.decorators import get_perfil_paciente

        institucion = current_institucion(self.request)
        perfil = get_perfil_paciente(user, institucion)
        if not perfil:
            perfil = get_perfil_paciente(user, None)
        if perfil and not Profesional.objects.filter(usuario=user, activo=True).exists():
            return redirect_to or str(reverse_lazy("portal_dashboard"))
        return redirect_to or super().get_success_url()


class PortalLoginView(XMedicalLoginView):
    template_name = "portal_paciente/login.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["patient_mode"] = True
        return kwargs


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
    staff_template = "auth_app/preferencias.html"
    portal_template = "auth_app/preferencias_portal.html"

    def _template_name(self, request):
        from apps.core.views import current_institucion
        from apps.portal_paciente.decorators import get_perfil_paciente

        perfil = get_perfil_paciente(request.user, current_institucion(request))
        if perfil and not request.user.is_superuser:
            from apps.core.models import Profesional

            if not Profesional.objects.filter(
                usuario=request.user, activo=True
            ).exists():
                return self.portal_template
        return self.staff_template

    def get(self, request):
        preference, _ = UserPreference.objects.get_or_create(user=request.user)
        return render(
            request,
            self._template_name(request),
            {"form": UserPreferenceForm(instance=preference)},
        )

    def post(self, request):
        preference, _ = UserPreference.objects.get_or_create(user=request.user)
        form = UserPreferenceForm(request.POST, instance=preference)
        template_name = self._template_name(request)
        if form.is_valid():
            form.save()
            messages.success(request, "Preferencias visuales actualizadas.")
            return redirect("preferencias_visuales")
        return render(request, template_name, {"form": form})
