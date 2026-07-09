from django.contrib import admin

from .models import AlertaRiesgoCronico, DemandaCita, PrediccionAusentismo


@admin.register(PrediccionAusentismo)
class PrediccionAusentismoAdmin(admin.ModelAdmin):
    list_display = ("cita", "probabilidad", "nivel", "institucion", "calculado_en")
    list_filter = ("nivel", "institucion")


@admin.register(DemandaCita)
class DemandaCitaAdmin(admin.ModelAdmin):
    list_display = ("especialidad", "dia_semana", "franja_horaria", "demanda_esperada", "institucion")
    list_filter = ("institucion", "franja_horaria")


@admin.register(AlertaRiesgoCronico)
class AlertaRiesgoCronicoAdmin(admin.ModelAdmin):
    list_display = ("paciente", "tipo", "nivel", "activa", "institucion", "creado_en")
    list_filter = ("tipo", "nivel", "activa", "institucion")
