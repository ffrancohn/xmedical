from django.db import models

from apps.citas.models import Cita
from apps.consulta.models import Consulta
from apps.core.models import Especialidad, Institucion, Profesional


class Referencia(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("aceptada", "Aceptada"),
        ("rechazada", "Rechazada"),
        ("completada", "Completada"),
    ]
    PRIORIDAD_CHOICES = [("baja", "Baja"), ("media", "Media"), ("alta", "Alta")]

    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    consulta_origen = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name="referencias")
    especialidad_destino = models.ForeignKey(
        Especialidad, on_delete=models.PROTECT, related_name="referencias_recibidas"
    )
    medico_referente = models.ForeignKey(
        Profesional, on_delete=models.PROTECT, related_name="referencias_emitidas"
    )
    especialista = models.ForeignKey(
        Profesional,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referencias_asignadas",
    )
    cita_derivada = models.ForeignKey(
        Cita,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referencias",
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="pendiente")
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default="media")
    motivo = models.TextField()
    comentarios_especialista = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]
        indexes = [
            models.Index(fields=["institucion", "estado"]),
            models.Index(fields=["consulta_origen"]),
        ]

    def __str__(self):
        paciente = self.consulta_origen.cita.paciente
        return f"Referencia {paciente} -> {self.especialidad_destino.nombre}"

    @property
    def paciente(self):
        return self.consulta_origen.cita.paciente


class Contrarreferencia(models.Model):
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    referencia = models.OneToOneField(Referencia, on_delete=models.CASCADE, related_name="contrarreferencia")
    resumen_atencion = models.TextField()
    plan_seguimiento = models.TextField()
    creado_por = models.ForeignKey(Profesional, on_delete=models.PROTECT)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]

    def __str__(self):
        return f"Contrarreferencia #{self.referencia_id}"
