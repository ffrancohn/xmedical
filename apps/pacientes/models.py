from django.contrib.auth.models import User
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


class DocumentoOCRLog(models.Model):
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    proveedor = models.CharField(max_length=50)
    confianza = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    resultado = models.JSONField(default=dict, blank=True)
    texto_raw = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]

    def __str__(self):
        return f"OCR {self.proveedor} {self.creado_en:%Y-%m-%d %H:%M}"
