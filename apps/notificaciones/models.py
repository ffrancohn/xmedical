from django.db import models

from apps.citas.models import Cita
from apps.consulta.models import Consulta
from apps.core.models import Institucion
from apps.pacientes.models import Paciente


class RecordatorioMedicamento(models.Model):
    FRECUENCIA_CHOICES = [
        ("diario", "Diario"),
        ("12h", "Cada 12 horas"),
        ("8h", "Cada 8 horas"),
    ]

    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="recordatorios_medicamentos")
    consulta = models.ForeignKey(Consulta, on_delete=models.SET_NULL, null=True, blank=True)
    medicamento = models.CharField(max_length=200)
    dosis = models.CharField(max_length=100, blank=True)
    frecuencia = models.CharField(max_length=20, choices=FRECUENCIA_CHOICES, default="diario")
    hora_recordatorio = models.TimeField()
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.medicamento} -> {self.paciente}"


class LogNotificacion(models.Model):
    TIPO_CHOICES = [
        ("cita_24h", "Recordatorio cita 24h"),
        ("cita_1h", "Recordatorio cita 1h"),
        ("medicamento", "Recordatorio medicamento"),
    ]
    ESTADO_CHOICES = [
        ("enviado", "Enviado"),
        ("fallido", "Fallido"),
        ("omitido", "Omitido"),
    ]

    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, null=True, blank=True, related_name="logs_notificacion")
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True, blank=True)
    recordatorio_medicamento = models.ForeignKey(
        RecordatorioMedicamento,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="logs",
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    destinatario = models.EmailField(blank=True)
    asunto = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    detalle = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]
        constraints = [
            models.UniqueConstraint(
                fields=["cita", "tipo"],
                condition=models.Q(cita__isnull=False, estado="enviado"),
                name="uniq_log_cita_tipo_enviado",
            ),
        ]
        indexes = [
            models.Index(fields=["institucion", "tipo", "creado_en"]),
            models.Index(fields=["recordatorio_medicamento", "creado_en"]),
        ]

    def __str__(self):
        return f"{self.tipo} {self.estado} {self.destinatario}"
