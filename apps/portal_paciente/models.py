from django.conf import settings
from django.db import models

from apps.core.models import Institucion
from apps.pacientes.models import Paciente


class PerfilPaciente(models.Model):
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil_paciente",
    )
    paciente = models.OneToOneField(
        Paciente,
        on_delete=models.CASCADE,
        related_name="perfil_portal",
    )
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "perfil de paciente"
        verbose_name_plural = "perfiles de paciente"

    def __str__(self):
        return f"Portal {self.paciente}"
