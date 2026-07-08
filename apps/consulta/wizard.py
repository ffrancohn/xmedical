from apps.citas.models import Cita
from apps.variables_clinicas.services import cita_tiene_variables

CIE10_MVP = [
    {"codigo": "I10", "nombre": "Hipertension esencial primaria"},
    {"codigo": "E11", "nombre": "Diabetes mellitus tipo 2"},
    {"codigo": "J00", "nombre": "Rinofaringitis aguda"},
    {"codigo": "J06.9", "nombre": "Infeccion aguda de vias respiratorias superiores"},
    {"codigo": "N39.0", "nombre": "Infeccion de vias urinarias"},
    {"codigo": "K29.7", "nombre": "Gastritis no especificada"},
    {"codigo": "M54.5", "nombre": "Lumbalgia"},
    {"codigo": "R51", "nombre": "Cefalea"},
    {"codigo": "A09", "nombre": "Diarrea y gastroenteritis de presunto origen infeccioso"},
    {"codigo": "B34.9", "nombre": "Infeccion viral no especificada"},
]

STEPS = {
    1: "Revisar preclinica",
    2: "Motivo de consulta",
    3: "Anamnesis",
    4: "Examen fisico",
    5: "Variables clinicas",
    6: "Diagnostico",
    7: "Plan terapeutico",
    8: "Resumen",
}

MAX_STEP = max(STEPS)
VARIABLES_STEP = 5
FINAL_STEP = MAX_STEP


def siguiente_paso(step: int, cita: Cita) -> int:
    step = int(step)
    if step < VARIABLES_STEP:
        siguiente = step + 1
        if siguiente == VARIABLES_STEP and not cita_tiene_variables(cita):
            return VARIABLES_STEP + 1
        return siguiente
    if step == VARIABLES_STEP:
        return VARIABLES_STEP + 1
    return min(step + 1, MAX_STEP)


def paso_anterior(step: int, cita: Cita) -> int:
    step = int(step)
    if step <= 1:
        return 1
    anterior = step - 1
    if anterior == VARIABLES_STEP and not cita_tiene_variables(cita):
        return VARIABLES_STEP - 1
    return anterior
