from django.contrib import admin

from .models import Contrarreferencia, Referencia


@admin.register(Referencia)
class ReferenciaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "institucion",
        "paciente",
        "especialidad_destino",
        "estado",
        "prioridad",
        "medico_referente",
        "especialista",
        "creado_en",
    )
    list_filter = ("estado", "prioridad", "institucion", "especialidad_destino")
    search_fields = ("motivo", "consulta_origen__cita__paciente__nombre")

    @admin.display(description="Paciente")
    def paciente(self, obj):
        return obj.paciente


@admin.register(Contrarreferencia)
class ContrarreferenciaAdmin(admin.ModelAdmin):
    list_display = ("id", "institucion", "referencia", "creado_por", "creado_en")
    list_filter = ("institucion",)
