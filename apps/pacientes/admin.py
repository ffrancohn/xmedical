from django.contrib import admin

from .models import DocumentoOCRLog, Paciente


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("documento", "nombre", "apellido", "institucion", "telefono", "activo")
    list_filter = ("institucion", "sexo", "activo")
    search_fields = ("documento", "nombre", "apellido")


@admin.register(DocumentoOCRLog)
class DocumentoOCRLogAdmin(admin.ModelAdmin):
    list_display = ("proveedor", "confianza", "institucion", "usuario", "creado_en")
    list_filter = ("proveedor", "institucion")
    readonly_fields = ("creado_en",)
