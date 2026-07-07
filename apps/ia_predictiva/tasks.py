from celery import shared_task

from apps.core.models import Institucion

from .services.ausentismo import reentrenar_ausentismo_institucion
from .services.demanda import calcular_demanda_institucion


@shared_task(name="apps.ia_predictiva.tasks.reentrenar_modelos_predictivos")
def reentrenar_modelos_predictivos():
    resultados = {"instituciones": 0, "ausentismo": 0, "demanda": 0}
    for institucion in Institucion.objects.filter(activo=True):
        resultados["instituciones"] += 1
        resultados["ausentismo"] += reentrenar_ausentismo_institucion(institucion)
        resultados["demanda"] += calcular_demanda_institucion(institucion)
    return resultados
