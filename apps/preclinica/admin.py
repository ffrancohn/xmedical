from django.contrib import admin

from .models import Preclinica


@admin.register(Preclinica)
class PreclinicaAdmin(admin.ModelAdmin):
    list_display = ("cita", "institucion", "triaje", "presion_arterial_sis", "presion_arterial_dia", "imc")
    list_filter = ("institucion", "triaje")
