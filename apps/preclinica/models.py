from django.db import models

from apps.citas.models import Cita
from apps.core.models import Institucion


class Preclinica(models.Model):
    TRIAJE_CHOICES = [("baja", "Baja"), ("media", "Media"), ("alta", "Alta")]

    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE)
    presion_arterial_sis = models.IntegerField(null=True, blank=True)
    presion_arterial_dia = models.IntegerField(null=True, blank=True)
    frecuencia_cardiaca = models.IntegerField(null=True, blank=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    saturacion_o2 = models.IntegerField(null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    talla = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    imc = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    motivo_consulta = models.TextField(blank=True)
    triaje = models.CharField(max_length=20, choices=TRIAJE_CHOICES, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def alertas(self):
        alertas = []
        if self.presion_arterial_sis and self.presion_arterial_sis >= 140:
            alertas.append("Presion sistolica elevada")
        if self.presion_arterial_dia and self.presion_arterial_dia >= 90:
            alertas.append("Presion diastolica elevada")
        if self.temperatura and self.temperatura >= 38:
            alertas.append("Fiebre")
        if self.saturacion_o2 and self.saturacion_o2 < 92:
            alertas.append("Saturacion de oxigeno baja")
        return alertas

    def __str__(self):
        return f"Preclinica {self.cita}"
