from django.contrib import admin

from .models import BackupLog, Especialidad, Horario, Institucion, Profesional


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


@admin.register(BackupLog)
class BackupLogAdmin(admin.ModelAdmin):
    list_display = ("tipo", "alcance", "institucion", "archivo", "usuario", "creado_en")
    list_filter = ("tipo", "alcance", "institucion")
    search_fields = ("archivo", "detalle", "usuario__username")
