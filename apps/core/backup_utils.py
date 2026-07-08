from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.utils import timezone

from .models import BackupLog, Institucion
from .tenant_transfer import export_tenant_json, log_tenant_operation

BACKUP_DIR = Path(settings.BASE_DIR) / "backups"


def timestamp():
    return timezone.localtime().strftime("%Y%m%d_%H%M%S")


def create_global_backup(user):
    BACKUP_DIR.mkdir(exist_ok=True)
    filename = f"xmedical_global_{timestamp()}.json"
    path = BACKUP_DIR / filename
    with path.open("w", encoding="utf-8") as handle:
        call_command(
            "dumpdata",
            "--natural-foreign",
            "--natural-primary",
            "--indent",
            "2",
            exclude=["contenttypes", "auth.Permission", "sessions"],
            stdout=handle,
        )
    BackupLog.objects.create(tipo="backup", alcance="global", archivo=str(path), usuario=user)
    return path


def create_institution_backup(institucion, user):
    BACKUP_DIR.mkdir(exist_ok=True)
    filename = f"xmedical_tenant_{institucion.subdominio}_{timestamp()}.json"
    path = BACKUP_DIR / filename
    path.write_text(export_tenant_json(institucion), encoding="utf-8")
    log_tenant_operation(
        "backup",
        institucion,
        user,
        archivo=str(path),
        detalle="Exportacion completa de tenant (Fase 3).",
    )
    return path


def restore_fixture(uploaded_file, alcance, user, institucion=None):
    BACKUP_DIR.mkdir(exist_ok=True)
    filename = f"restore_{alcance}_{timestamp()}_{uploaded_file.name}"
    path = BACKUP_DIR / filename
    with path.open("wb") as handle:
        for chunk in uploaded_file.chunks():
            handle.write(chunk)
    call_command("loaddata", str(path))
    BackupLog.objects.create(
        tipo="restore",
        alcance=alcance,
        institucion=institucion,
        archivo=str(path),
        usuario=user,
        detalle="Restauracion logica mediante loaddata. Actualiza o inserta registros por PK.",
    )
    return path
