from django.contrib import admin

from .models import PerfilPaciente


@admin.register(PerfilPaciente)
class PerfilPacienteAdmin(admin.ModelAdmin):
    list_display = ("paciente", "institucion", "usuario", "activo", "creado_en")
    list_filter = ("activo", "institucion")
    search_fields = ("paciente__documento", "paciente__nombre", "usuario__email")
