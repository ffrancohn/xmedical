"""Pruebas de export/import de tenant (Fase 3)."""
import json
from datetime import time

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from apps.citas.models import Cita
from apps.consulta.models import Consulta, Diagnostico
from apps.core.models import Especialidad, Institucion, Profesional
from apps.core.tenant_transfer import (
    TenantTransferError,
    export_tenant_package,
    import_tenant_package,
    tenant_stats,
)
from apps.core.test_utils import HOST, auth_client
from apps.pacientes.models import Paciente


class TenantTransferTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.institucion = Institucion.objects.get(pk=1)
        self.paciente = Paciente.objects.get(pk=1)
        self.medico = Profesional.objects.get(pk=2)
        self.especialidad = Especialidad.objects.get(pk=1)

    def _crear_datos_clinicos(self):
        cita = Cita.objects.create(
            institucion=self.institucion,
            paciente=self.paciente,
            profesional=self.medico,
            fecha=timezone.localdate(),
            hora=time(10, 0),
            estado="atendida",
        )
        consulta = Consulta.objects.create(institucion=self.institucion, cita=cita)
        Diagnostico.objects.create(
            institucion=self.institucion,
            consulta=consulta,
            codigo_cie10="J06.9",
            nombre="Infeccion respiratoria",
            es_principal=True,
        )

    def test_export_incluye_metadata_y_registros(self):
        self._crear_datos_clinicos()
        package = export_tenant_package(self.institucion)
        self.assertEqual(package["format_version"], 1)
        self.assertEqual(package["source_institucion"]["subdominio"], "demo")
        self.assertGreater(len(package["records"]), 0)
        self.assertGreater(package["stats"]["consultas"], 0)

    def test_import_nuevo_tenant_con_remap(self):
        self._crear_datos_clinicos()
        package = export_tenant_package(self.institucion)
        before = Institucion.objects.count()
        institucion, id_maps = import_tenant_package(
            package,
            mode="new",
            nombre="Clinica Importada Test",
            subdominio="demo-import-test",
        )
        self.assertEqual(Institucion.objects.count(), before + 1)
        self.assertEqual(institucion.nombre, "Clinica Importada Test")
        self.assertEqual(institucion.subdominio, "demo-import-test")
        stats = tenant_stats(institucion)
        self.assertGreater(stats["pacientes"], 0)
        self.assertGreater(stats["consultas"], 0)
        self.assertIn("core.institucion", id_maps)

    def test_import_rechaza_paquete_invalido(self):
        with self.assertRaises(TenantTransferError):
            import_tenant_package({"format_version": 99, "records": []})

    def test_subdominio_duplicado_genera_sufijo(self):
        package = export_tenant_package(self.institucion)
        inst1, _ = import_tenant_package(package, mode="new", subdominio="demo")
        inst2, _ = import_tenant_package(package, mode="new", subdominio="demo")
        self.assertNotEqual(inst1.subdominio, inst2.subdominio)


class TenantTransferViewsTests(TestCase):
    fixtures = ["initial_data.json"]

    def test_superadmin_exporta_tenant(self):
        client = auth_client("superadmin.demo")
        response = client.get("/superadmin/tenant/1/exportar/", **HOST)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        data = json.loads(response.content.decode())
        self.assertEqual(data["source_institucion"]["id"], 1)

    def test_superadmin_importa_tenant(self):
        client = auth_client("superadmin.demo")
        package = export_tenant_package(Institucion.objects.get(pk=1))
        archivo = SimpleUploadedFile(
            "tenant.json",
            json.dumps(package).encode("utf-8"),
            content_type="application/json",
        )
        before = Institucion.objects.count()
        response = client.post(
            "/superadmin/tenant/importar/",
            {
                "modo": "new",
                "nombre": "Clinica desde vista",
                "subdominio": "vista-import",
                "archivo": archivo,
            },
            **HOST,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Institucion.objects.count(), before + 1)
        self.assertTrue(Institucion.objects.filter(subdominio="vista-import").exists())
