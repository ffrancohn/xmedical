from django.contrib import admin

from .models import Paciente


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("documento", "nombre", "apellido", "institucion", "telefono", "activo")
    list_filter = ("institucion", "sexo", "activo")
    search_fields = ("documento", "nombre", "apellido")
