from django.db import models

from apps.citas.models import Cita
from apps.consulta.models import Consulta
from apps.core.models import Especialidad, Institucion
from apps.pacientes.models import Paciente
from apps.preclinica.models import Preclinica


class PrediccionAusentismo(models.Model):
    NIVEL_CHOICES = [
        ("bajo", "Bajo"),
        ("medio", "Medio"),
        ("alto", "Alto"),
    ]

    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE, related_name="prediccion_ausentismo")
    probabilidad = models.DecimalField(max_digits=5, decimal_places=2)
    nivel = models.CharField(max_length=10, choices=NIVEL_CHOICES)
    factores = models.JSONField(default=dict, blank=True)
    calculado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-calculado_en"]
        indexes = [
            models.Index(fields=["institucion", "nivel"]),
        ]

    def __str__(self):
        return f"Ausentismo {self.cita_id}: {self.probabilidad}%"


class DemandaCita(models.Model):
    DIAS = [
        (0, "Lunes"),
        (1, "Martes"),
        (2, "Miercoles"),
        (3, "Jueves"),
        (4, "Viernes"),
        (5, "Sabado"),
        (6, "Domingo"),
    ]

    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    dia_semana = models.IntegerField()
    franja_horaria = models.CharField(max_length=20)
    demanda_esperada = models.DecimalField(max_digits=6, decimal_places=2)
    muestras = models.PositiveIntegerField(default=0)
    calculado_en = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["institucion", "especialidad", "dia_semana", "franja_horaria"]
        ordering = ["-demanda_esperada"]

    def __str__(self):
        return f"Demanda {self.especialidad} d{self.dia_semana} {self.franja_horaria}"

    def get_dia_semana_display(self):
        return dict(self.DIAS).get(self.dia_semana, str(self.dia_semana))


class AlertaRiesgoCronico(models.Model):
    TIPO_CHOICES = [
        ("diabetes", "Diabetes"),
        ("hta", "Hipertension"),
        ("otro", "Otro"),
    ]
    NIVEL_CHOICES = [
        ("bajo", "Bajo"),
        ("medio", "Medio"),
        ("alto", "Alto"),
    ]

    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="alertas_riesgo")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    nivel = models.CharField(max_length=10, choices=NIVEL_CHOICES)
    mensaje = models.TextField()
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, null=True, blank=True)
    preclinica = models.ForeignKey(Preclinica, on_delete=models.CASCADE, null=True, blank=True)
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, null=True, blank=True)
    activa = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]
        indexes = [
            models.Index(fields=["institucion", "paciente", "activa"]),
            models.Index(fields=["tipo", "nivel"]),
        ]

    def __str__(self):
        return f"{self.get_tipo_display()} ({self.nivel}) - {self.paciente}"
