from django.contrib import admin

from .models import Cita


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "hora", "paciente", "profesional", "estado", "institucion")
    list_filter = ("institucion", "estado", "fecha")
    search_fields = ("paciente__documento", "paciente__nombre", "paciente__apellido")
