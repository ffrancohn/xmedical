# DOCUMENTO 9: INTEGRACIONES
## XMedical - Sistema de Gestión Clínica Multi-tenant para Primer y Segundo Nivel

| Versión | Fecha | Autor | Estado |
|---------|-------|-------|--------|
| 1.0 | 2026 | Agente de Documentación Técnica | **Aprobado** |

---

## 1. VISIÓN GENERAL

Este documento define las **integraciones** de XMedical con sistemas externos, organizadas en:

- **Integraciones actuales** (MVP y Fase 2)
- **Integraciones futuras** (Fase 3 y posteriores)
- **APIs expuestas** (para que otros sistemas se integren)
- **Formatos de datos**
- **Seguridad en integraciones**

---

## 2. MAPA DE INTEGRACIONES

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              INTEGRACIONES XMEDICAL                                  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                           SISTEMAS EXTERNOS                                   │   │
│  │                                                                              │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │   │
│  │  │   Email      │  │  IA - Visión │  │   IA - LLM   │  │   Storage    │    │   │
│  │  │  (SMTP/      │  │  (Google/    │  │  (OpenAI/    │  │   (S3/NFS)   │    │   │
│  │  │  SendGrid)   │  │   AWS/Tes.)  │  │  Local LLM)  │  │              │    │   │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │   │
│  │         │                 │                 │                 │            │   │
│  └─────────┼─────────────────┼─────────────────┼─────────────────┼────────────┘   │
│            │                 │                 │                 │                │
│            ▼                 ▼                 ▼                 ▼                │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                           XMEDICAL CORE                                     │   │
│  │                                                                              │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │   │
│  │  │   Django     │  │   Celery     │  │   API REST   │  │   Webhooks   │    │   │
│  │  │  Application │  │   Workers    │  │  (Django RF) │  │   (salida)   │    │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │   │
│  │                                                                              │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│            │                 │                 │                 │                │
│            ▼                 ▼                 ▼                 ▼                │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                         SISTEMAS EXTERNOS (FUTURO)                           │   │
│  │                                                                              │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │   │
│  │  │  Laboratorio │  │  Imágenes    │  │  Facturación │  │   HL7/FHIR   │    │   │
│  │  │   Clínico    │  │  (PACS)      │  │   (SII)      │  │  (Interop.)  │    │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │   │
│  │                                                                              │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. INTEGRACIONES ACTUALES (MVP - Fase 2)

### 3.1 Email (Recordatorios y notificaciones)

| Propiedad | Valor |
|-----------|-------|
| **Proveedor** | SMTP / SendGrid / AWS SES |
| **Propósito** | Recordatorios de citas, medicamentos, confirmaciones |
| **Protocolo** | SMTP (587), API REST |
| **Autenticación** | API Key / Usuario+contraseña |
| **Volumen estimado** | 500-5,000 emails/día |

**Configuración:**

```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.getenv('SENDGRID_API_KEY')
DEFAULT_FROM_EMAIL = 'noreply@xmedical.com'
```

**Plantillas de email:**

```html
<!-- templates/email/recordatorio_cita.html -->
<!DOCTYPE html>
<html>
<body>
    <h2>Recordatorio de cita médica</h2>
    <p>Estimado/a {{ paciente.nombre }},</p>
    <p>Le recordamos que tiene una cita programada:</p>
    <ul>
        <li><strong>Fecha:</strong> {{ cita.fecha|date:"d/m/Y" }}</li>
        <li><strong>Hora:</strong> {{ cita.hora }}</li>
        <li><strong>Médico:</strong> {{ medico.nombre }}</li>
        <li><strong>Especialidad:</strong> {{ especialidad.nombre }}</li>
    </ul>
    <p>Por favor, llegue con 15 minutos de anticipación.</p>
    <p>Para cancelar, haga clic <a href="{{ cancelar_url }}">aquí</a>.</p>
</body>
</html>
```

---

### 3.2 IA - Visión Artificial (Validación de Documentos)

| Propiedad | Valor |
|-----------|-------|
| **Proveedores soportados** | Google Cloud Vision, AWS Rekognition, Tesseract (local) |
| **Propósito** | Extraer datos de cédulas/pasaportes |
| **Protocolo** | API REST |
| **Autenticación** | API Key / IAM Role |
| **Volumen estimado** | 50-500 documentos/día |

**Implementación:**

```python
# services/vision_service.py
import boto3
from google.cloud import vision

class VisionService:
    def __init__(self, provider='google'):
        self.provider = provider
        
    def extract_document(self, image_bytes):
        if self.provider == 'google':
            client = vision.ImageAnnotatorClient()
            image = vision.Image(content=image_bytes)
            response = client.document_text_detection(image=image)
            return self._parse_google_response(response)
        
        elif self.provider == 'aws':
            client = boto3.client('rekognition')
            response = client.detect_text(Image={'Bytes': image_bytes})
            return self._parse_aws_response(response)
        
        else:  # tesseract local
            import pytesseract
            from PIL import Image
            text = pytesseract.image_to_string(Image.open(image_bytes))
            return self._parse_text(text)
```

**Formato de respuesta estandarizado:**

```json
{
    "documento": "12345678-9",
    "nombre": "JUAN",
    "apellido": "PEREZ GONZALEZ",
    "fecha_nacimiento": "1980-05-15",
    "nacionalidad": "CHILENA",
    "confianza": 0.95
}
```

---

### 3.3 IA - LLM (Sugerencia Diagnóstica)

| Propiedad | Valor |
|-----------|-------|
| **Proveedores soportados** | OpenAI, Anthropic, Local LLM (Ollama) |
| **Propósito** | Sugerir diagnósticos basados en síntomas |
| **Protocolo** | API REST (RESTful o streaming) |
| **Autenticación** | API Key |
| **Prompt configurable** | Por institución (tenant) |
| **Volumen estimado** | 100-1,000 consultas/día |

**Configuración por tenant:**

```python
# models.py - Configuración IA por institución
class Institucion(models.Model):
    # ...
    configuracion_ia = models.JSONField(default=dict)
    # Ejemplo:
    # {
    #     "llm_provider": "openai",
    #     "llm_model": "gpt-4",
    #     "prompt_template": "Eres un médico asistente...",
    #     "temperatura": 0.7,
    #     "max_tokens": 500
    # }
```

**Ejemplo de llamada a API:**

```python
# services/llm_service.py
import openai

def sugerir_diagnostico(motivo, sintomas, edad, sexo, prompt_template):
    prompt = prompt_template.format(
        motivo=motivo,
        sintomas=sintomas,
        edad=edad,
        sexo=sexo
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un asistente médico."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content
```

---

### 3.4 Almacenamiento (Archivos)

| Propiedad | Valor |
|-----------|-------|
| **Proveedores soportados** | S3 (AWS), NFS local, MinIO (self-hosted) |
| **Propósito** | Logos, documentos escaneados, QR codes, attachments |
| **Protocolo** | S3-compatible API |
| **Autenticación** | Access Key + Secret Key |

**Configuración:**

```python
# settings.py
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'xmedical-storage'
AWS_S3_REGION_NAME = 'us-east-1'
```

---

## 4. INTEGRACIONES FUTURAS (Fase 3+)

### 4.1 Logging y Monitoreo

| Propiedad | Valor |
|-----------|-------|
| **Herramientas** | Loki + Prometheus + Grafana |
| **Propósito** | Agregación de logs por tenant, métricas, alertas |
| **Protocolo** | HTTP API (Prometheus), syslog (Loki) |

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'xmedical'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

---

### 4.2 Sistema de Laboratorio Clínico (Futuro)

| Propiedad | Valor |
|-----------|-------|
| **Estándar** | HL7 v2.x / FHIR |
| **Propósito** | Recibir resultados de exámenes automáticamente |
| **Protocolo** | MLLP (HL7), REST (FHIR) |

**Ejemplo mensaje HL7:**

```
MSH|^~\&|LAB|Hospital|XMedical|Clinic|202606041030||ORU^R01|12345|P|2.5|
PID|1||12345678||PEREZ^JUAN||19800515|M|
OBR|1|LAB123|ORD456|CBC^Hemograma||202606041000|
OBX|1|NM|GLUC^Glucosa||95|mg/dL|70-99|N|||F|
```

---

### 4.3 Sistema de Imágenes (PACS) - Futuro

| Propiedad | Valor |
|-----------|-------|
| **Estándar** | DICOM |
| **Propósito** | Visualizar imágenes médicas (Rayos X, TAC, RM) |
| **Protocolo** | DICOMweb (REST), C-STORE SCP |

---

### 4.4 Facturación Electrónica (SII - Chile)

| Propiedad | Valor |
|-----------|-------|
| **Estándar** | SII DTE (XML firmado) |
| **Propósito** | Emitir boletas y facturas electrónicas |
| **Protocolo** | HTTPS + XML |

---

### 4.5 Whatsapp / SMS (Notificaciones)

| Propiedad | Valor |
|-----------|-------|
| **Proveedores** | Twilio, Meta Cloud API, AWS SNS |
| **Propósito** | Recordatorios vía WhatsApp/SMS |
| **Protocolo** | API REST |

---

## 5. APIS EXPUESTAS POR XMEDICAL

### 5.1 API REST (para integraciones externas y app móvil)

> **Estado:** 🔮 Planificada — no implementada en código. Especificación objetivo. Ver [Documento 13](13%20App%20movil%20y%20API%20REST.md).

La API se implementará con **Django REST Framework + JWT** dentro del monolito Django (no un backend separado).

| Endpoint | Método | Descripción | Autenticación |
|----------|--------|-------------|---------------|
| `/api/v1/pacientes` | GET | Listar pacientes | Bearer token |
| `/api/v1/pacientes` | POST | Crear paciente | Bearer token |
| `/api/v1/citas` | GET | Listar citas | Bearer token |
| `/api/v1/citas` | POST | Crear cita | Bearer token |
| `/api/v1/consultas` | GET | Listar consultas | Bearer token |
| `/api/v1/consultas/{id}` | GET | Detalle consulta | Bearer token |
| `/api/v1/referencias` | GET | Listar referencias | Bearer token |
| `/api/v1/referencias` | POST | Crear referencia | Bearer token |
| `/api/v1/webhooks` | POST | Configurar webhook | Bearer token |

### 5.2 Webhooks (eventos salientes)

XMedical puede **notificar a sistemas externos** cuando ocurren eventos:

| Evento | Payload | Destino |
|--------|---------|---------|
| `cita.creada` | Datos de la cita | URL configurada |
| `cita.cancelada` | Datos de la cita | URL configurada |
| `consulta.guardada` | Resumen de consulta | URL configurada |
| `referencia.creada` | Datos de referencia | URL configurada |
| `examen.resultado` | Resultado de laboratorio | URL configurada |

**Ejemplo webhook:**

```json
POST /webhook/xmedical HTTP/1.1
Content-Type: application/json
X-Webhook-Signature: sha256=abc123...

{
    "evento": "cita.creada",
    "tenant_id": 1,
    "timestamp": "2026-06-04T10:30:00Z",
    "data": {
        "cita_id": 123,
        "paciente": {
            "id": 456,
            "nombre": "Juan Pérez",
            "documento": "12345678-9"
        },
        "fecha": "2026-06-15",
        "hora": "10:00",
        "medico": "Dr. Carlos Pérez"
    }
}
```

---

## 6. FORMATOS DE DATOS

### 6.1 JSON (estándar)

```json
{
    "version": "1.0",
    "tenant_id": 1,
    "data": {
        "paciente": {
            "id": 123,
            "nombre": "Juan Pérez",
            "documento": "12345678-9"
        }
    }
}
```

### 6.2 CSV (exportaciones)

```csv
id,nombre,apellido,documento,fecha_nacimiento,sexo,telefono,email
1,Juan,Pérez,12345678-9,1980-05-15,M,912345678,juan@email.com
```

### 6.3 HL7/FHIR (interoperabilidad futura)

```json
{
    "resourceType": "Patient",
    "id": "123",
    "identifier": [{
        "system": "https://xmedical.com/id/documento",
        "value": "12345678-9"
    }],
    "name": [{
        "family": "Pérez",
        "given": ["Juan"]
    }],
    "birthDate": "1980-05-15",
    "gender": "male"
}
```

---

## 7. SEGURIDAD EN INTEGRACIONES

| Medida | Implementación | Descripción |
|--------|----------------|-------------|
| **Autenticación API** | JWT (Bearer token) | Token con expiración (1 hora) |
| **API Keys** | Header `X-API-Key` | Para integraciones servidor-servidor |
| **Rate limiting** | 100 req/min | Por API key o IP |
| **Cifrado** | TLS 1.3 | Todo el tráfico cifrado |
| **Webhook signature** | HMAC-SHA256 | Verificar origen de webhooks |
| **IP Whitelist** | Configurable | Limitar origen de peticiones |
| **Auditoría** | Logs | Registrar todas las integraciones |

### Ejemplo verificación webhook:

```python
import hmac
import hashlib

def verify_webhook_signature(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)
```

---

## 8. CONFIGURACIÓN POR TENANT

Cada institución puede configurar sus propias integraciones:

```json
{
    "tenant_id": 1,
    "integraciones": {
        "email": {
            "provider": "sendgrid",
            "api_key": "***",
            "from_email": "noreply@clinicaandes.cl"
        },
        "vision": {
            "provider": "google",
            "api_key": "***"
        },
        "llm": {
            "provider": "openai",
            "api_key": "***",
            "model": "gpt-4",
            "prompt_template": "..."
        },
        "webhooks": {
            "cita_creada": "https://sistema-externo.com/webhook",
            "consulta_guardada": "https://sistema-externo.com/consulta"
        }
    }
}
```

---

## 9. PLAN DE INTEGRACIONES POR FASE

| Fase | Integración | Estado |
|------|-------------|--------|
| **Fase 1 (MVP)** | Email (SMTP) | 🔮 Planificado |
| **Fase 2** | IA - Visión (Google/AWS) | 🔮 Planificado |
| **Fase 2** | Almacenamiento S3/NFS | 🔮 Planificado |
| **Fase 2** | API REST (salida) + app móvil | 🔮 Planificado — [Doc 13](13%20App%20movil%20y%20API%20REST.md) |
| **Fase 3** | IA - LLM (OpenAI/Local) | 🔮 Planificado |
| **Fase 3** | Webhooks | 🔮 Planificado |
| **Fase 3** | Monitoreo (Prometheus) | 🔮 Planificado |
| **Futuro** | Laboratorio clínico (HL7) | 🔮 Planificado |
| **Futuro** | Imágenes (DICOM) | 🔮 Planificado |
| **Futuro** | Facturación (SII) | 🔮 Planificado |
| **Futuro** | WhatsApp/SMS | 🔮 Planificado |

---

## 10. APROBACIÓN

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Product Owner | [Usuario] | ✅ Aprobado | 2026 |
| Tech Lead | [Usuario] | ✅ Aprobado | 2026 |
| Agente Documentación | DeepSeek | Generado | 2026 |

---

**Fin del Documento 9: Integraciones**

---

## RESUMEN DEL DOCUMENTO

| Aspecto | Valor |
|---------|-------|
| **Integraciones actuales** | 0 en producción (web Django operativa) |
| **Integraciones planificadas** | Email, IA, Storage, API REST, app móvil |
| **APIs expuestas** | 8 endpoints |
| **Webhooks** | 5 eventos |
| **Formatos soportados** | JSON, CSV, HL7/FHIR (futuro) |
| **Medidas de seguridad** | 7 |
| **Configuración por tenant** | ✅ Sí |
