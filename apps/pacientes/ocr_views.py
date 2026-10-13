from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.core.audit import log_ia_usage
from apps.core.views import current_institucion

from .forms import DocumentoIdentidadForm, PacienteOCRReviewForm
from .models import DocumentoOCRLog
from .services.vision_service import VisionService, VisionServiceError
from .views import can_manage_pacientes


class PacienteOCRUploadView(LoginRequiredMixin, View):
    template_name = "pacientes/ocr_subir.html"

    def dispatch(self, request, *args, **kwargs):
        if can_manage_pacientes(request.user):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, "No tienes permiso para registrar pacientes.")
        return redirect("dashboard")

    def get(self, request):
        institucion = current_institucion(request)
        servicio = VisionService(institucion)
        return render(
            request,
            self.template_name,
            {
                "form": DocumentoIdentidadForm(),
                "proveedores": servicio.provider_labels(),
                "ocr_habilitado": bool(servicio.available_providers()),
            },
        )

    def post(self, request):
        institucion = current_institucion(request)
        servicio = VisionService(institucion)
        form = DocumentoIdentidadForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "proveedores": servicio.provider_labels(),
                    "ocr_habilitado": bool(servicio.available_providers()),
                },
            )

        archivo = form.cleaned_data["documento_imagen"]
        try:
            VisionService.validar_imagen(archivo)
            contenido = archivo.read()
            resultado = servicio.extract_from_image(contenido, archivo.content_type or "image/jpeg")
        except VisionServiceError as exc:
            messages.error(request, str(exc))
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "proveedores": servicio.provider_labels(),
                    "ocr_habilitado": bool(servicio.available_providers()),
                },
            )

        if institucion and not resultado.manual_fallback:
            DocumentoOCRLog.objects.create(
                institucion=institucion,
                usuario=request.user,
                proveedor=resultado.proveedor,
                confianza=resultado.confianza,
                resultado={
                    "nombre": resultado.nombre,
                    "apellido": resultado.apellido,
                    "documento": resultado.documento,
                    "fecha_nacimiento": resultado.fecha_nacimiento,
                },
                texto_raw=resultado.texto_raw[:5000],
            )
            cfg = servicio._settings
            log_ia_usage(
                institucion,
                feature="ocr_asistido",
                provider=resultado.proveedor,
                model=cfg.get("vision_model") or cfg.get("model") or "",
                usuario=request.user,
                request=request,
            )

        request.session["ocr_paciente_data"] = {
            "documento": resultado.documento,
            "nombre": resultado.nombre,
            "apellido": resultado.apellido,
            "fecha_nacimiento": resultado.fecha_nacimiento,
            "proveedor": resultado.proveedor,
            "confianza": resultado.confianza,
            "manual_fallback": resultado.manual_fallback,
        }
        if resultado.manual_fallback:
            messages.warning(request, "OCR no disponible. Complete los datos manualmente.")
        else:
            messages.info(request, "Revise y confirme los datos extraidos antes de guardar.")
        return redirect("pacientes_ocr_revisar")


class PacienteOCRReviewView(LoginRequiredMixin, View):
    template_name = "pacientes/ocr_revisar.html"

    def dispatch(self, request, *args, **kwargs):
        if can_manage_pacientes(request.user):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, "No tienes permiso para registrar pacientes.")
        return redirect("dashboard")

    def _session_data(self, request):
        return request.session.get("ocr_paciente_data", {})

    def get(self, request):
        data = self._session_data(request)
        if not data:
            messages.error(request, "No hay datos OCR para revisar.")
            return redirect("pacientes_ocr_subir")
        form = PacienteOCRReviewForm(initial=data)
        return render(request, self.template_name, {"form": form, "ocr_meta": data})

    def post(self, request):
        data = self._session_data(request)
        form = PacienteOCRReviewForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form, "ocr_meta": data})

        request.session["ocr_paciente_data"] = {
            **form.cleaned_data,
            "fecha_nacimiento": form.cleaned_data["fecha_nacimiento"].isoformat()
            if form.cleaned_data.get("fecha_nacimiento")
            else None,
            "proveedor": data.get("proveedor", "manual"),
            "confianza": data.get("confianza", 0),
            "manual_fallback": data.get("manual_fallback", True),
            "confirmado": True,
        }
        messages.success(request, "Datos confirmados. Complete el registro del paciente.")
        return redirect("pacientes_nuevo")
