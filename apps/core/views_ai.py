import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.core.ai_institution_config import (
    default_ai_settings,
    get_institution_ai_settings,
    save_institution_ai_settings,
)
from apps.core.ai_services import OllamaProvider
from apps.core.forms import ConfiguracionIAForm
from apps.core.models import Institucion
from apps.core.permissions import AdminRequiredMixin
from apps.core.views import current_institucion


def _resolve_institucion(request):
    if request.user.is_superuser:
        institucion_id = request.GET.get("institucion") or request.POST.get("institucion")
        if institucion_id:
            return get_object_or_404(Institucion, pk=institucion_id, activo=True)
    return current_institucion(request)


def _ollama_from_request_data(data):
    base_url = (data.get("ollama_base_url") or "").strip()
    model = (data.get("model") or "").strip()
    return OllamaProvider(default_model=model, base_url=base_url or None)


class ConfiguracionIAView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = "core/configuracion_ia.html"

    def _context(self, request, form, institucion):
        return {
            "form": form,
            "institucion": institucion,
            "is_superadmin_view": request.user.is_superuser,
            "all_instituciones": Institucion.objects.filter(activo=True).order_by("nombre"),
            "selected_institucion_id": str(institucion.id) if institucion else "",
        }

    def get(self, request):
        institucion = _resolve_institucion(request)
        if not institucion:
            messages.error(request, "No hay institución seleccionada para configurar IA.")
            return redirect("dashboard")

        settings_data = get_institution_ai_settings(institucion)
        form = ConfiguracionIAForm.from_institution_settings(settings_data)
        return render(request, self.template_name, self._context(request, form, institucion))

    def post(self, request):
        institucion = _resolve_institucion(request)
        if not institucion:
            messages.error(request, "No hay institución seleccionada para configurar IA.")
            return redirect("dashboard")

        if request.POST.get("action") == "restore_defaults":
            save_institution_ai_settings(institucion, default_ai_settings())
            messages.success(request, "Configuración IA restaurada a los valores por defecto.")
            if request.user.is_superuser:
                return redirect(f"/configuracion-ia/?institucion={institucion.id}")
            return redirect("configuracion_ia")

        form = ConfiguracionIAForm(request.POST)
        if form.is_valid():
            save_institution_ai_settings(institucion, form.cleaned_data)
            messages.success(request, "Configuración de IA guardada correctamente.")
            if request.user.is_superuser:
                return redirect(f"/configuracion-ia/?institucion={institucion.id}")
            return redirect("configuracion_ia")

        return render(request, self.template_name, self._context(request, form, institucion))


class ConfiguracionIAProbarView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request):
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            payload = request.POST

        provider = payload.get("provider", "ollama")
        if provider != "ollama":
            return JsonResponse(
                {
                    "ok": False,
                    "error": "La prueba de conexión solo está disponible para Ollama local.",
                },
                status=400,
            )

        provider_client = _ollama_from_request_data(payload)
        result = provider_client.health_check(probe_chat=True)
        status = 200 if result.get("ok") else 502
        return JsonResponse(result, status=status)


class ConfiguracionIAModelosView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request):
        base_url = request.GET.get("base_url", "").strip()
        model = request.GET.get("model", "").strip()
        provider_client = OllamaProvider(default_model=model, base_url=base_url or None)
        try:
            models = provider_client.list_models()
        except Exception as exc:  # noqa: BLE001 — respuesta JSON al cliente
            return JsonResponse({"ok": False, "error": str(exc), "models": []}, status=502)
        return JsonResponse({"ok": True, "models": models})
