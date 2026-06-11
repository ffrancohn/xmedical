from django.contrib import admin

from .models import BackupLog, Especialidad, Horario, Institucion, LogAuditoria, Profesional


@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "subdominio", "tipo", "activo", "creado_en")
    search_fields = ("nombre", "subdominio")


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "institucion", "nivel", "duracion_consulta_minutos", "activo")
    list_filter = ("institucion", "nivel", "activo")


@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ("nombre", "usuario", "institucion", "tipo", "especialidad", "activo")
    list_filter = ("institucion", "tipo", "activo")


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ("profesional", "dia_semana", "hora_inicio", "hora_fin", "activo")
    list_filter = ("institucion", "dia_semana", "activo")


@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ("creado_en", "institucion", "usuario", "accion", "tabla_afectada", "registro_id")
    list_filter = ("accion", "tabla_afectada", "institucion")
    search_fields = ("tabla_afectada", "usuario__username")
    readonly_fields = (
        "institucion",
        "usuario",
        "accion",
        "tabla_afectada",
        "registro_id",
        "valor_anterior",
        "valor_nuevo",
        "ip_address",
        "creado_en",
    )


@admin.register(BackupLog)
class BackupLogAdmin(admin.ModelAdmin):
    list_display = ("tipo", "alcance", "institucion", "archivo", "usuario", "creado_en")
    list_filter = ("tipo", "alcance", "institucion")
    search_fields = ("archivo", "detalle", "usuario__username")
