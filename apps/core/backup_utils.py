from pathlib import Path

from django.conf import settings
from django.core import serializers
from django.core.management import call_command
from django.utils import timezone

from apps.citas.models import Cita
from apps.consulta.models import Consulta, Diagnostico
from apps.pacientes.models import Paciente
from apps.preclinica.models import Preclinica
from .models import BackupLog, Especialidad, Horario, Institucion, Profesional


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
    filename = f"xmedical_{institucion.subdominio}_{timestamp()}.json"
    path = BACKUP_DIR / filename
    objects = []
    objects.extend(Institucion.objects.filter(pk=institucion.pk))
    objects.extend(Especialidad.objects.filter(institucion=institucion))
    objects.extend(Profesional.objects.filter(institucion=institucion))
    objects.extend(Horario.objects.filter(institucion=institucion))
    objects.extend(Paciente.objects.filter(institucion=institucion))
    objects.extend(Cita.objects.filter(institucion=institucion))
    objects.extend(Preclinica.objects.filter(institucion=institucion))
    objects.extend(Consulta.objects.filter(institucion=institucion))
    objects.extend(Diagnostico.objects.filter(institucion=institucion))
    data = serializers.serialize("json", objects, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    path.write_text(data, encoding="utf-8")
    BackupLog.objects.create(tipo="backup", alcance="institucion", institucion=institucion, archivo=str(path), usuario=user)
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
