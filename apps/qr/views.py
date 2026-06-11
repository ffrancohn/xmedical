from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.consulta.models import Consulta
from apps.core.decorators import get_profesional, role_required
from apps.core.views import current_institucion

from .models import DocumentoQR
from .services import QRExpiradoError, QRNoEncontradoError, QRService, QRYaUsadoError


def scoped_consulta(request, consulta_id):
    qs = Consulta.objects.select_related("cita__paciente", "institucion")
    institucion = current_institucion(request)
    if institucion:
        qs = qs.filter(institucion=institucion)
    return get_object_or_404(qs, pk=consulta_id)


class QRGenerarView(LoginRequiredMixin, View):
    def post(self, request, consulta_id, tipo):
        consulta = scoped_consulta(request, consulta_id)
        profesional = get_profesional(request.user)
        if not request.user.is_superuser and (not profesional or profesional.tipo not in ("medico", "admin")):
            messages.error(request, "No tienes permiso para generar codigos QR.")
            return redirect("consulta_wizard", cita_id=consulta.cita_id, step=7)

        service = QRService(institucion=consulta.institucion)
        if tipo == "receta":
            documento = service.generar_receta(consulta, usuario=request.user)
        elif tipo == "examen":
            orden = request.POST.get("orden", "")
            documento = service.generar_examen(consulta, usuario=request.user, orden=orden)
        elif tipo == "checkin":
            documento = service.generar_checkin(consulta.cita, usuario=request.user)
        else:
            messages.error(request, "Tipo de QR no valido.")
            return redirect("consulta_wizard", cita_id=consulta.cita_id, step=7)

        return redirect("qr_mostrar", token=documento.token)


def qr_mostrar(request, token):
    documento = get_object_or_404(
        DocumentoQR.objects.select_related("institucion", "paciente", "consulta", "cita"),
        token=token,
    )
    institucion = current_institucion(request)
    if institucion and documento.institucion_id != institucion.id and not request.user.is_superuser:
        messages.error(request, "No tienes acceso a este codigo QR.")
        return redirect("home")

    service = QRService(institucion=documento.institucion)
    imagen = service.generar_imagen_base64(documento.token)
    return render(
        request,
        "qr/mostrar.html",
        {
            "documento": documento,
            "imagen_base64": imagen,
            "validation_url": service.build_validation_url(documento.token),
        },
    )


def qr_validar(request, token):
    service = QRService()
    try:
        resultado = service.validar(token)
    except QRNoEncontradoError:
        return render(request, "qr/validar.html", {"estado": "no_encontrado", "token": token})

    documento = resultado["documento"]
    puede_marcar = False
    if request.user.is_authenticated:
        profesional = get_profesional(request.user)
        puede_marcar = request.user.is_superuser or (
            profesional and profesional.tipo in ("recepcionista", "admin")
        )

    if request.method == "POST" and puede_marcar and resultado["estado"] == "valido":
        try:
            service.marcar_usado(documento)
            messages.success(request, "Codigo QR marcado como utilizado.")
            return redirect("qr_validar", token=token)
        except (QRYaUsadoError, QRExpiradoError) as exc:
            messages.error(request, str(exc))

    return render(
        request,
        "qr/validar.html",
        {
            "estado": resultado["estado"],
            "documento": documento,
            "token": token,
            "puede_marcar": puede_marcar and resultado["estado"] == "valido",
        },
    )


@login_required
@role_required("recepcionista", "admin")
def qr_lista_consulta(request, consulta_id):
    consulta = scoped_consulta(request, consulta_id)
    documentos = DocumentoQR.objects.filter(consulta=consulta).order_by("-creado_en")
    return render(
        request,
        "qr/lista_consulta.html",
        {"consulta": consulta, "documentos": documentos},
    )
