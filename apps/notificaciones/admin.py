from django.contrib import admin

from .models import LogNotificacion, RecordatorioMedicamento


@admin.register(RecordatorioMedicamento)
class RecordatorioMedicamentoAdmin(admin.ModelAdmin):
    list_display = ("medicamento", "paciente", "institucion", "frecuencia", "hora_recordatorio", "activo")
    list_filter = ("institucion", "frecuencia", "activo")
    search_fields = ("medicamento", "paciente__nombre", "paciente__apellido", "paciente__documento")


@admin.register(LogNotificacion)
class LogNotificacionAdmin(admin.ModelAdmin):
    list_display = ("tipo", "estado", "destinatario", "institucion", "cita", "creado_en")
    list_filter = ("tipo", "estado", "institucion")
    search_fields = ("destinatario", "asunto", "detalle")
    readonly_fields = ("creado_en",)
