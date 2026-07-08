import secrets

from django.contrib.auth.models import User
from django.db import models

from apps.citas.models import Cita
from apps.consulta.models import Consulta
from apps.core.models import Institucion
from apps.pacientes.models import Paciente


def generar_token_qr():
    return secrets.token_urlsafe(32)


class DocumentoQR(models.Model):
    TIPO_CHOICES = [
        ("receta", "Receta"),
        ("examen", "Orden de examen"),
        ("checkin", "Check-in de cita"),
    ]

    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True, default=generar_token_qr)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, null=True, blank=True)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    usado = models.BooleanField(default=False)
    usado_en = models.DateTimeField(null=True, blank=True)
    expira_en = models.DateTimeField()
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]
        indexes = [
            models.Index(fields=["institucion", "tipo"]),
            models.Index(fields=["token"]),
        ]

    def __str__(self):
        return f"QR {self.get_tipo_display()} - {self.paciente}"
