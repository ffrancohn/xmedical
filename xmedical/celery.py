import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xmedical.settings")

app = Celery("xmedical")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "recordatorios-citas": {
        "task": "apps.notificaciones.tasks.enviar_recordatorios_citas",
        "schedule": 3600.0,
    },
    "recordatorios-medicamentos": {
        "task": "apps.notificaciones.tasks.enviar_recordatorios_medicamentos",
        "schedule": 3600.0,
    },
}
