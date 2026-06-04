from django.contrib import admin

from .models import Consulta, Diagnostico


class DiagnosticoInline(admin.TabularInline):
    model = Diagnostico
    extra = 0


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ("cita", "institucion", "conducta", "creado_en")
    list_filter = ("institucion", "conducta")
    inlines = [DiagnosticoInline]


@admin.register(Diagnostico)
class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ("codigo_cie10", "nombre", "consulta", "es_principal", "orden")
    search_fields = ("codigo_cie10", "nombre")
