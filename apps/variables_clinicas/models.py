from django.db import models

from apps.consulta.models import Consulta
from apps.core.models import Especialidad, Institucion


class VariableClinica(models.Model):
    TIPO_CHOICES = [
        ("texto", "Texto"),
        ("numero", "Numero"),
        ("booleano", "Booleano"),
        ("fecha", "Fecha"),
        ("select", "Seleccion"),
    ]

    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name="variables_clinicas")
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    opciones = models.JSONField(default=list, blank=True)
    obligatorio = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "nombre"]
        unique_together = ["institucion", "especialidad", "codigo"]
        indexes = [
            models.Index(fields=["institucion", "especialidad", "activo"]),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.especialidad.nombre})"


class ValorVariableClinica(models.Model):
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name="valores_variables")
    variable = models.ForeignKey(VariableClinica, on_delete=models.PROTECT, related_name="valores")
    valor = models.TextField(blank=True)

    class Meta:
        unique_together = ["consulta", "variable"]
        indexes = [
            models.Index(fields=["institucion", "consulta"]),
        ]

    def __str__(self):
        return f"{self.variable.codigo}={self.valor}"

    @property
    def valor_mostrar(self):
        if self.variable.tipo == "booleano":
            return "Si" if self.valor in ("1", "true", "True", "on") else "No"
        return self.valor
