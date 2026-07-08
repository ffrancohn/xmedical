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
    "reentrenar-modelos-predictivos": {
        "task": "apps.ia_predictiva.tasks.reentrenar_modelos_predictivos",
        "schedule": 604800.0,
    },
    "backup-diario": {
        "task": "apps.core.tasks.backup_database",
        "schedule": 86400.0,
        "kwargs": {"include_tenants": True},
    },
    "rotar-backups": {
        "task": "apps.core.tasks.limpiar_logs",
        "schedule": 86400.0,
        "kwargs": {"retention_days": 30},
    },
}
