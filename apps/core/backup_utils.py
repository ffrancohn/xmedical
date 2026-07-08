from pathlib import Path
import shutil

from django.conf import settings
from django.core.management import call_command
from django.utils import timezone

from .models import BackupLog, Institucion
from .tenant_transfer import export_tenant_json, log_tenant_operation

BACKUP_DIR = Path(settings.BASE_DIR) / "backups"
BACKUP_RETENTION_DAYS = getattr(settings, "BACKUP_RETENTION_DAYS", 30)
BACKUP_REMOTE_DIR = getattr(settings, "BACKUP_REMOTE_DIR", "")


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


def _mirror_to_remote(path: Path):
    if not BACKUP_REMOTE_DIR:
        return
    remote_root = Path(BACKUP_REMOTE_DIR)
    remote_root.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, remote_root / path.name)


def rotate_old_backups(retention_days=None):
    retention_days = retention_days or BACKUP_RETENTION_DAYS
    if not BACKUP_DIR.exists():
        return 0
    cutoff_ts = (timezone.now() - timezone.timedelta(days=retention_days)).timestamp()
    removed = 0
    for path in BACKUP_DIR.glob("xmedical_*.json"):
        if path.stat().st_mtime < cutoff_ts:
            path.unlink(missing_ok=True)
            removed += 1
    if BACKUP_REMOTE_DIR:
        remote_root = Path(BACKUP_REMOTE_DIR)
        if remote_root.exists():
            for path in remote_root.glob("xmedical_*.json"):
                if path.stat().st_mtime < cutoff_ts:
                    path.unlink(missing_ok=True)
    return removed


def run_scheduled_backups(include_tenants=True):
    BACKUP_DIR.mkdir(exist_ok=True)
    paths = []
    global_path = create_global_backup(user=None)
    _mirror_to_remote(global_path)
    paths.append(str(global_path))
    if include_tenants:
        for institucion in Institucion.objects.filter(activo=True).order_by("id"):
            tenant_path = create_institution_backup(institucion, user=None)
            _mirror_to_remote(tenant_path)
            paths.append(str(tenant_path))
    removed = rotate_old_backups()
    return {"created": paths, "removed": removed}


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
