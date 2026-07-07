"""Pruebas de OCR/vision para documentos de paciente (Fase 2)."""
import base64
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from apps.core.models import Institucion
from apps.core.test_utils import auth_client
from apps.pacientes.models import DocumentoOCRLog
from apps.pacientes.services.vision_service import OCRResult, VisionService, VisionServiceError, parse_document_text


PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)


class VisionServiceParserTests(TestCase):
    def test_parse_document_text(self):
        texto = "JUAN PEREZ LOPEZ\nIdentidad 0801-1990-12345\nNac: 15/03/1990"
        resultado = parse_document_text(texto)
        self.assertEqual(resultado.nombre, "JUAN")
        self.assertEqual(resultado.apellido, "PEREZ LOPEZ")
        self.assertIn("0801199012345", resultado.documento)
        self.assertEqual(resultado.fecha_nacimiento, "1990-03-15")

    @override_settings(OPENAI_API_KEY="", OPENROUTER_API_KEY="")
    def test_fallback_manual_sin_proveedores(self):
        servicio = VisionService()
        resultado = servicio.extract_from_image(PNG_1X1, "image/png")
        self.assertTrue(resultado.manual_fallback)
        self.assertEqual(resultado.proveedor, "manual")

    @override_settings(OPENAI_API_KEY="test-key", OPENAI_MODEL="gpt-4o")
    def test_extract_with_ai_vision_mock(self):
        payload = {
            "choices": [
                {
                    "message": {
                        "content": (
                            '{"nombre":"Maria","apellido":"Lopez","documento":"123456",'
                            '"fecha_nacimiento":"1991-04-02","confianza":0.9}'
                        )
                    }
                }
            ]
        }
        servicio = VisionService()
        with patch("apps.pacientes.services.vision_service._post_chat_completion", return_value=payload):
            resultado = servicio.extract_from_image(PNG_1X1, "image/png")
        self.assertEqual(resultado.nombre, "Maria")
        self.assertEqual(resultado.apellido, "Lopez")
        self.assertEqual(resultado.documento, "123456")
        self.assertFalse(resultado.manual_fallback)


class PacienteOCRViewTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.client = auth_client("recepcion.demo")
        self.institucion = Institucion.objects.get(pk=1)
        self.imagen = SimpleUploadedFile("cedula.png", PNG_1X1, content_type="image/png")

    @override_settings(OPENAI_API_KEY="", OPENROUTER_API_KEY="")
    def test_subida_ocr_fallback_manual(self):
        response = self.client.post(
            "/pacientes/ocr/",
            {"documento_imagen": self.imagen},
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/pacientes/ocr/revisar/", response.url)
        session = self.client.session
        self.assertIn("ocr_paciente_data", session)
        self.assertTrue(session["ocr_paciente_data"]["manual_fallback"])

    @override_settings(OPENAI_API_KEY="test-key", OPENAI_MODEL="gpt-4o")
    def test_flujo_ocr_confirmar_y_precargar_formulario(self):
        payload = {
            "choices": [
                {
                    "message": {
                        "content": (
                            '{"nombre":"Pedro","apellido":"Ramirez","documento":"OCR-001",'
                            '"fecha_nacimiento":"1988-01-10","confianza":0.88}'
                        )
                    }
                }
            ]
        }
        with patch("apps.pacientes.services.vision_service._post_chat_completion", return_value=payload):
            self.client.post(
                "/pacientes/ocr/",
                {"documento_imagen": SimpleUploadedFile("cedula.png", PNG_1X1, content_type="image/png")},
                **{"HTTP_HOST": "xmedical.cloud"},
            )
        self.assertEqual(DocumentoOCRLog.objects.count(), 1)
        response = self.client.post(
            "/pacientes/ocr/revisar/",
            {
                "documento": "OCR-001",
                "nombre": "Pedro",
                "apellido": "Ramirez",
                "fecha_nacimiento": "1988-01-10",
                "sexo": "M",
            },
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get("/pacientes/nuevo/", **{"HTTP_HOST": "xmedical.cloud"})
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertEqual(form.initial.get("documento"), "OCR-001")
        self.assertEqual(form.initial.get("nombre"), "Pedro")

    def test_validar_imagen_rechaza_no_imagen(self):
        archivo = SimpleUploadedFile("doc.txt", b"hola", content_type="text/plain")
        with self.assertRaises(VisionServiceError):
            VisionService.validar_imagen(archivo)
