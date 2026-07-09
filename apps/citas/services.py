from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Optional

from apps.core.models import Especialidad, Horario, Profesional

from .models import Cita


class SinTurnosDisponiblesError(Exception):
    """No hay turnos libres en el rango solicitado."""


@dataclass
class TurnoDisponible:
    profesional: Profesional
    fecha: date
    hora: time


class FlexibleAgendamientoService:
    MANANA_LIMITE = time(12, 0)

    def __init__(self, institucion):
        self.institucion = institucion

    def buscar_disponibilidad(
        self,
        profesional: Profesional,
        fecha_inicio: date,
        fecha_fin: date,
        jornada: str,
        especialidad: Optional[Especialidad] = None,
    ) -> list[TurnoDisponible]:
        if fecha_fin < fecha_inicio:
            return []

        duracion = 20
        if especialidad:
            duracion = especialidad.duracion_consulta_minutos
        elif profesional.especialidad_id:
            duracion = profesional.especialidad.duracion_consulta_minutos

        turnos: list[TurnoDisponible] = []
        dia = fecha_inicio
        while dia <= fecha_fin:
            horarios = Horario.objects.filter(
                institucion=self.institucion,
                profesional=profesional,
                dia_semana=dia.weekday(),
                activo=True,
            )
            ocupados = set(
                Cita.objects.filter(
                    institucion=self.institucion,
                    profesional=profesional,
                    fecha=dia,
                )
                .exclude(estado="cancelada")
                .values_list("hora", flat=True)
            )
            for horario in horarios:
                for slot in self._iter_slots(horario.hora_inicio, horario.hora_fin, duracion):
                    if slot in ocupados:
                        continue
                    if self._matches_jornada(slot, jornada):
                        turnos.append(TurnoDisponible(profesional=profesional, fecha=dia, hora=slot))
            dia += timedelta(days=1)

        turnos.sort(key=lambda item: (item.fecha, item.hora))
        return turnos

    def asignar_primer_turno(
        self,
        paciente,
        especialidad: Especialidad,
        fecha_inicio: date,
        fecha_fin: date,
        jornada: str,
        profesional: Optional[Profesional] = None,
    ) -> Cita:
        candidatos: list[TurnoDisponible] = []
        if profesional:
            candidatos = self.buscar_disponibilidad(
                profesional, fecha_inicio, fecha_fin, jornada, especialidad
            )
        else:
            profesionales = Profesional.objects.filter(
                institucion=self.institucion,
                tipo="medico",
                activo=True,
                especialidad=especialidad,
            )
            for medico in profesionales:
                candidatos.extend(
                    self.buscar_disponibilidad(medico, fecha_inicio, fecha_fin, jornada, especialidad)
                )
            candidatos.sort(key=lambda item: (item.fecha, item.hora))

        if not candidatos:
            raise SinTurnosDisponiblesError(
                "No hay turnos disponibles en el rango y jornada seleccionados."
            )

        turno = candidatos[0]
        return Cita.objects.create(
            institucion=self.institucion,
            paciente=paciente,
            profesional=turno.profesional,
            fecha=turno.fecha,
            hora=turno.hora,
            estado="confirmada",
            tipo_agendamiento="flexible",
        )

    def _iter_slots(self, hora_inicio: time, hora_fin: time, duracion_minutos: int):
        actual = datetime.combine(date.today(), hora_inicio)
        fin = datetime.combine(date.today(), hora_fin)
        paso = timedelta(minutes=duracion_minutos)
        while actual + paso <= fin:
            yield actual.time()
            actual += paso

    def _matches_jornada(self, hora: time, jornada: str) -> bool:
        if jornada == "cualquiera":
            return True
        if jornada == "manana":
            return hora < self.MANANA_LIMITE
        if jornada == "tarde":
            return hora >= self.MANANA_LIMITE
        return True
