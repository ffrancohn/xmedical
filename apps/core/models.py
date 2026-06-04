from django.contrib.auth.models import User
from django.db import models


class Institucion(models.Model):
    TIPO_CHOICES = [("privada", "Privada"), ("publica", "Publica")]

    nombre = models.CharField(max_length=200)
    subdominio = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    configuracion = models.JSONField(default=dict, blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "instituciones"

    def __str__(self):
        return self.nombre


class Especialidad(models.Model):
    NIVEL_CHOICES = [("primero", "Primer Nivel"), ("segundo", "Segundo Nivel")]

    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, blank=True)
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    duracion_consulta_minutos = models.IntegerField(default=20)
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ["institucion", "nombre"]

    def __str__(self):
        return self.nombre


class Profesional(models.Model):
    TIPO_CHOICES = [
        ("admin", "Admin"),
        ("medico", "Medico"),
        ("enfermera", "Enfermera"),
        ("recepcionista", "Recepcionista"),
    ]

    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    registro_medico = models.CharField(max_length=50, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class Horario(models.Model):
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
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    dia_semana = models.IntegerField(choices=DIAS)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ["profesional", "dia_semana", "hora_inicio", "hora_fin"]

    def __str__(self):
        return f"{self.profesional} {self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fin}"


class BackupLog(models.Model):
    ALCANCE_CHOICES = [("global", "Toda la base de datos"), ("institucion", "Por institucion")]
    TIPO_CHOICES = [("backup", "Respaldo"), ("restore", "Restauracion")]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    alcance = models.CharField(max_length=20, choices=ALCANCE_CHOICES)
    institucion = models.ForeignKey(Institucion, on_delete=models.SET_NULL, null=True, blank=True)
    archivo = models.CharField(max_length=255, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    detalle = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.get_tipo_display()} {self.get_alcance_display()} {self.creado_en:%Y-%m-%d %H:%M}"
