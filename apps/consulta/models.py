from django.db import models

from apps.citas.models import Cita
from apps.core.models import Institucion


class Consulta(models.Model):
    CONDUCTA_CHOICES = [
        ("alta", "Alta medica"),
        ("cita_subsiguiente", "Cita subsiguiente"),
        ("referencia", "Referencia"),
    ]

    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE)
    motivo_consulta = models.TextField(blank=True)
    anamnesis = models.TextField(blank=True)
    examen_fisico = models.TextField(blank=True)
    plan_terapeutico = models.TextField(blank=True)
    conducta = models.CharField(max_length=50, choices=CONDUCTA_CHOICES, default="alta")
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consulta {self.cita}"


class Diagnostico(models.Model):
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name="diagnosticos")
    codigo_cie10 = models.CharField(max_length=10)
    nombre = models.CharField(max_length=200)
    es_principal = models.BooleanField(default=False)
    orden = models.IntegerField(default=1)

    class Meta:
        ordering = ["orden", "id"]

    def __str__(self):
        return f"{self.codigo_cie10} - {self.nombre}"
