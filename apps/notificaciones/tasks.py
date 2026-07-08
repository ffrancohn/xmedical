from celery import shared_task

from .services import procesar_recordatorios_citas, procesar_recordatorios_medicamentos


@shared_task(name="apps.notificaciones.tasks.enviar_recordatorios_citas")
def enviar_recordatorios_citas():
    return procesar_recordatorios_citas()


@shared_task(name="apps.notificaciones.tasks.enviar_recordatorios_medicamentos")
def enviar_recordatorios_medicamentos():
    return procesar_recordatorios_medicamentos()
