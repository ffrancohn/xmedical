from django.contrib import admin

from .models import ValorVariableClinica, VariableClinica


@admin.register(VariableClinica)
class VariableClinicaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo", "especialidad", "institucion", "tipo", "obligatorio", "orden", "activo")
    list_filter = ("institucion", "especialidad", "tipo", "activo", "obligatorio")
    search_fields = ("nombre", "codigo")
    ordering = ("institucion", "especialidad", "orden", "nombre")


@admin.register(ValorVariableClinica)
class ValorVariableClinicaAdmin(admin.ModelAdmin):
    list_display = ("consulta", "variable", "valor", "institucion")
    list_filter = ("institucion", "variable__tipo")
    search_fields = ("variable__nombre", "valor")
