"""Pruebas de backup y restore (BAK-*)."""
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from apps.core.backup_utils import (
    create_global_backup,
    create_institution_backup,
    restore_fixture,
    rotate_old_backups,
    run_scheduled_backups,
)
from apps.core.models import BackupLog, Institucion
from apps.core.test_utils import HOST, auth_client


class BackupUtilsTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.user = User.objects.get(username="superadmin.demo")
        self.institucion = Institucion.objects.get(pk=1)
        self.tmp = Path(tempfile.mkdtemp())

    def test_bak01_backup_global(self):
        with patch("apps.core.backup_utils.BACKUP_DIR", self.tmp):
            path = create_global_backup(self.user)
            self.assertTrue(path.exists())
            self.assertTrue(BackupLog.objects.filter(tipo="backup", alcance="global").exists())

    def test_bak02_backup_institucion(self):
        with patch("apps.core.backup_utils.BACKUP_DIR", self.tmp):
            path = create_institution_backup(self.institucion, self.user)
            self.assertTrue(path.exists())
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["format_version"], 1)
            models = {item["model"] for item in data["records"]}
            self.assertIn("pacientes.paciente", models)
            pacientes = [item for item in data["records"] if item["model"] == "pacientes.paciente"]
            for item in pacientes:
                self.assertEqual(item["fields"]["institucion"], self.institucion.pk)

    def test_bak03_restore_fixture(self):
        with patch("apps.core.backup_utils.BACKUP_DIR", self.tmp):
            backup_path = create_global_backup(self.user)
            uploaded = SimpleUploadedFile(
                "restore.json",
                backup_path.read_bytes(),
                content_type="application/json",
            )
            restore_fixture(uploaded, "global", self.user)
            self.assertTrue(BackupLog.objects.filter(tipo="restore").exists())


class BackupViewTests(TestCase):
    fixtures = ["initial_data.json"]

    def test_bak04_vista_post_superadmin(self):
        client = auth_client("superadmin.demo")
        with patch("apps.core.views.create_global_backup") as mock_backup:
            mock_backup.return_value = Path(tempfile.mkdtemp()) / "test_backup.json"
            response = client.post(
                "/superadmin/backup/",
                {"alcance": "global"},
                **HOST,
            )
            self.assertEqual(response.status_code, 302)
            mock_backup.assert_called_once()

    def test_bak05_permiso_denegado_medico(self):
        client = auth_client("medico.demo")
        response = client.post(
            "/superadmin/backup/",
            {"alcance": "global"},
            **HOST,
        )
        self.assertIn(response.status_code, [302, 403])


class ScheduledBackupTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_backup_diario_crea_global_y_tenants(self):
        with patch("apps.core.backup_utils.BACKUP_DIR", self.tmp):
            result = run_scheduled_backups(include_tenants=True)
            self.assertGreaterEqual(len(result["created"]), 2)
            self.assertTrue(BackupLog.objects.filter(tipo="backup", alcance="global").exists())
            self.assertTrue(BackupLog.objects.filter(tipo="backup", alcance="institucion").exists())

    def test_rotacion_elimina_backups_antiguos(self):
        with patch("apps.core.backup_utils.BACKUP_DIR", self.tmp):
            old_file = self.tmp / "xmedical_global_old.json"
            old_file.write_text("{}", encoding="utf-8")
            old_ts = (timezone.now() - timezone.timedelta(days=40)).timestamp()
            import os

            os.utime(old_file, (old_ts, old_ts))
            removed = rotate_old_backups(retention_days=30)
            self.assertEqual(removed, 1)
            self.assertFalse(old_file.exists())
