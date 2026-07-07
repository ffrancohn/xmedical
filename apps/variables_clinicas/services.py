from apps.citas.models import Cita

from .models import VariableClinica


def especialidad_para_cita(cita: Cita):
    if cita.profesional_id and cita.profesional.especialidad_id:
        return cita.profesional.especialidad
    return None


def variables_para_cita(cita: Cita):
    especialidad = especialidad_para_cita(cita)
    if not especialidad:
        return VariableClinica.objects.none()
    return VariableClinica.objects.filter(
        institucion=cita.institucion,
        especialidad=especialidad,
        activo=True,
    )


def cita_tiene_variables(cita: Cita) -> bool:
    return variables_para_cita(cita).exists()
