import unicodedata

from django.db import models

from apps.citas.models import Cita
from apps.core.models import Institucion


def normalizar_texto(valor: str) -> str:
    """Minúsculas, sin tildes y con espacios colapsados (para búsqueda)."""
    valor = unicodedata.normalize("NFKD", valor or "")
    valor = "".join(c for c in valor if not unicodedata.combining(c))
    return " ".join(valor.lower().split())



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


class CodigoCie10(models.Model):
    """Catálogo CIE-10: capítulos, bloques y códigos facturables.

    `nivel` replica la jerarquía del archivo de origen:
    0 capítulo, 1 bloque, 2 categoría, 3-5 subcategorías.
    Sólo los niveles >= 2 se ofrecen en el buscador (`es_hoja`).
    """

    codigo = models.CharField(max_length=12, unique=True)
    descripcion = models.CharField(max_length=255)
    nivel = models.PositiveSmallIntegerField(default=2)
    capitulo = models.CharField(max_length=12, blank=True)
    bloque = models.CharField(max_length=12, blank=True)
    es_hoja = models.BooleanField(default=True)
    busqueda = models.CharField(max_length=300, blank=True, db_index=True)

    class Meta:
        verbose_name = "Código CIE-10"
        verbose_name_plural = "Códigos CIE-10"
        ordering = ["codigo"]
        indexes = [
            models.Index(fields=["capitulo"], name="cie10_capitulo_idx"),
            models.Index(fields=["es_hoja"], name="cie10_hoja_idx"),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    def save(self, *args, **kwargs):
        self.busqueda = normalizar_texto(f"{self.codigo} {self.descripcion}")
        super().save(*args, **kwargs)
