import base64
from datetime import timedelta
from io import BytesIO

from django.conf import settings
from django.utils import timezone

from .models import DocumentoQR


class QRServiceError(Exception):
    """Error base del servicio QR."""


class QRNoEncontradoError(QRServiceError):
    pass


class QRYaUsadoError(QRServiceError):
    pass


class QRExpiradoError(QRServiceError):
    pass


class QRService:
    def __init__(self, institucion=None):
        self.institucion = institucion

    def build_validation_url(self, token: str) -> str:
        base = getattr(settings, "QR_BASE_URL", "http://localhost:8000/qr/").rstrip("/")
        return f"{base}/validar/{token}/"

    def expiration_datetime(self):
        days = int(getattr(settings, "QR_EXPIRATION_DAYS", 30))
        return timezone.now() + timedelta(days=days)

    def generar_receta(self, consulta, usuario=None, notas: str = "") -> DocumentoQR:
        return self._crear_documento(
            tipo="receta",
            institucion=consulta.institucion,
            paciente=consulta.cita.paciente,
            consulta=consulta,
            cita=consulta.cita,
            metadata={"plan": consulta.plan_terapeutico, "notas": notas},
            usuario=usuario,
        )

    def generar_examen(self, consulta, usuario=None, orden: str = "") -> DocumentoQR:
        return self._crear_documento(
            tipo="examen",
            institucion=consulta.institucion,
            paciente=consulta.cita.paciente,
            consulta=consulta,
            cita=consulta.cita,
            metadata={"orden": orden or consulta.plan_terapeutico},
            usuario=usuario,
        )

    def generar_checkin(self, cita, usuario=None) -> DocumentoQR:
        return self._crear_documento(
            tipo="checkin",
            institucion=cita.institucion,
            paciente=cita.paciente,
            consulta=None,
            cita=cita,
            metadata={"fecha": str(cita.fecha), "hora": str(cita.hora)},
            usuario=usuario,
        )

    def validar(self, token: str) -> dict:
        try:
            documento = DocumentoQR.objects.select_related(
                "institucion", "paciente", "consulta", "cita"
            ).get(token=token)
        except DocumentoQR.DoesNotExist as exc:
            raise QRNoEncontradoError("Codigo QR no encontrado.") from exc

        if documento.usado:
            return {"estado": "usado", "documento": documento}
        if documento.expira_en < timezone.now():
            return {"estado": "vencido", "documento": documento}
        return {"estado": "valido", "documento": documento}

    def marcar_usado(self, documento: DocumentoQR) -> DocumentoQR:
        if documento.usado:
            raise QRYaUsadoError("Este codigo QR ya fue utilizado.")
        if documento.expira_en < timezone.now():
            raise QRExpiradoError("Este codigo QR esta vencido.")

        documento.usado = True
        documento.usado_en = timezone.now()
        documento.save(update_fields=["usado", "usado_en"])

        if documento.tipo == "checkin" and documento.cita_id:
            cita = documento.cita
            if cita.estado in ("pendiente", "confirmada"):
                cita.estado = "en_espera"
                cita.save(update_fields=["estado"])

        return documento

    def generar_imagen_base64(self, token: str) -> str:
        url = self.build_validation_url(token)
        try:
            import segno

            buffer = BytesIO()
            segno.make(url).save(buffer, kind="png", scale=6)
            return base64.b64encode(buffer.getvalue()).decode("ascii")
        except Exception:
            import qrcode

            qr = qrcode.QRCode(version=1, box_size=8, border=4)
            qr.add_data(url)
            qr.make(fit=True)
            image = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            return base64.b64encode(buffer.getvalue()).decode("ascii")

    def _crear_documento(
        self,
        tipo,
        institucion,
        paciente,
        consulta,
        cita,
        metadata,
        usuario,
    ) -> DocumentoQR:
        if self.institucion and institucion.id != self.institucion.id:
            raise QRServiceError("El documento no pertenece a la institucion activa.")
        return DocumentoQR.objects.create(
            institucion=institucion,
            tipo=tipo,
            paciente=paciente,
            consulta=consulta,
            cita=cita,
            metadata=metadata,
            expira_en=self.expiration_datetime(),
            creado_por=usuario,
        )
