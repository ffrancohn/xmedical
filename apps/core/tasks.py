from celery import shared_task

from .backup_utils import rotate_old_backups, run_scheduled_backups


@shared_task(name="apps.core.tasks.backup_database")
def backup_database(include_tenants=True):
    return run_scheduled_backups(include_tenants=include_tenants)


@shared_task(name="apps.core.tasks.limpiar_logs")
def limpiar_logs(retention_days=30):
    return {"removed_backups": rotate_old_backups(retention_days=retention_days)}
