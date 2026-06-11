from django.contrib import admin

from .models import DocumentoQR


@admin.register(DocumentoQR)
class DocumentoQRAdmin(admin.ModelAdmin):
    list_display = ("token", "tipo", "institucion", "paciente", "usado", "expira_en", "creado_en")
    list_filter = ("tipo", "usado", "institucion")
    search_fields = ("token", "paciente__nombre", "paciente__apellido", "paciente__documento")
    readonly_fields = ("token", "creado_en", "usado_en")
