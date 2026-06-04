from django.db import models

from apps.core.models import Institucion


class Paciente(models.Model):
    SEXO_CHOICES = [("M", "Masculino"), ("F", "Femenino"), ("OTRO", "Otro")]

    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    documento = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, blank=True)
    telefono = models.CharField("telefono movil", max_length=20, blank=True)
    telefono_fijo = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    departamento = models.CharField(max_length=100, blank=True)
    contacto_emergencia_nombre = models.CharField(max_length=150, blank=True)
    contacto_emergencia_telefono = models.CharField(max_length=20, blank=True)
    observaciones = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ["institucion", "documento"]
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
