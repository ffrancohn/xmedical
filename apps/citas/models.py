from django.db import models

from apps.core.models import Institucion, Profesional
from apps.pacientes.models import Paciente


class Cita(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("confirmada", "Confirmada"),
        ("cancelada", "Cancelada"),
        ("atendida", "Atendida"),
    ]
    TIPO_AGENDAMIENTO_CHOICES = [("especifico", "Especifico"), ("flexible", "Flexible")]

    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="pendiente")
    tipo_agendamiento = models.CharField(max_length=20, choices=TIPO_AGENDAMIENTO_CHOICES, default="especifico")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["profesional", "fecha", "hora"]
        ordering = ["fecha", "hora"]

    def __str__(self):
        return f"{self.fecha} {self.hora} - {self.paciente}"
