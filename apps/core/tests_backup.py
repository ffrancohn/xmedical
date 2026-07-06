"""Pruebas de backup y restore (BAK-*)."""
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.core.backup_utils import create_global_backup, create_institution_backup, restore_fixture
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
            models = {item["model"] for item in data}
            self.assertIn("pacientes.paciente", models)
            pacientes = [item for item in data if item["model"] == "pacientes.paciente"]
            for item in pacientes:
                self.assertEqual(item["fields"]["institucion"], self.institucion.pk)

    def test_bak03_restore_fixture(self):
        with patch("apps.core.backup_utils.BACKUP_DIR", self.tmp):
            backup_path = create_institution_backup(self.institucion, self.user)
            uploaded = SimpleUploadedFile(
                "restore.json",
                backup_path.read_bytes(),
                content_type="application/json",
            )
            restore_fixture(uploaded, "institucion", self.user, self.institucion)
            self.assertTrue(BackupLog.objects.filter(tipo="restore").exists())


class BackupViewTests(TestCase):
    fixtures = ["initial_data.json"]

    def test_bak04_vista_post_superadmin(self):
        client = auth_client("superadmin.demo")
        with patch("apps.core.views.create_global_backup") as mock_backup:
            mock_backup.return_value = Path("/tmp/test_backup.json")
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
