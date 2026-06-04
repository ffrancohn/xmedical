# DOCUMENTO 10: PLAN DE PRUEBAS
## XMedical - Sistema de Gestión Clínica Multi-tenant para Primer y Segundo Nivel

| Versión | Fecha | Autor | Estado |
|---------|-------|-------|--------|
| 1.0 | 2026 | Agente de Documentación Técnica | **Aprobado** |

---

## 1. VISIÓN GENERAL

Este documento define la **estrategia de calidad y pruebas** para XMedical, incluyendo:

- **Tipos de pruebas** (unitaria, integración, API, UI, rendimiento, seguridad, aceptación)
- **Herramientas** utilizadas
- **Casos de prueba** por módulo
- **Cobertura requerida**
- **Criterios de éxito**
- **Ambiente de pruebas**

---

## 2. ESTRATEGIA DE PRUEBAS

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              PIRÁMIDE DE PRUEBAS - XMEDICAL                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│                              ┌─────────────────┐                                     │
│                              │   E2E / UI      │  ← 10%                              │
│                              │   (Selenium)     │                                     │
│                          ┌───┴─────────────────┴───┐                                 │
│                          │    Integración / API    │  ← 20%                          │
│                          │     (pytest + DRF)      │                                 │
│                      ┌───┴─────────────────────────┴───┐                            │
│                      │          Unitarias              │  ← 70%                      │
│                      │          (pytest)               │                            │
│                      └─────────────────────────────────┘                            │
│                                                                                      │
│  Adicionales:                                                                        │
│  • Pruebas de seguridad (OWASP ZAP)                                                  │
│  • Pruebas de rendimiento (Locust)                                                   │
│  • Pruebas de aceptación (UAT)                                                       │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. TIPOS DE PRUEBAS

### 3.1 Pruebas Unitarias

| Propiedad | Valor |
|-----------|-------|
| **Objetivo** | Validar funciones y métodos individuales |
| **Herramienta** | pytest, pytest-django |
| **Cobertura objetivo** | > 80% |
| **Ejecución** | En cada commit (CI/CD) |
| **Duración** | < 2 minutos |

**Ejemplo:**

```python
# tests/test_models.py
import pytest
from django.test import TestCase
from apps.core.models import Paciente, Institucion

class PacienteModelTest(TestCase):
    def setUp(self):
        self.institucion = Institucion.objects.create(
            nombre="Clínica Test",
            subdominio="test"
        )
    
    def test_crear_paciente(self):
        paciente = Paciente.objects.create(
            institucion=self.institucion,
            documento="12345678-9",
            nombre="Juan",
            apellido="Pérez",
            email="juan@test.com"
        )
        self.assertEqual(paciente.nombre, "Juan")
        self.assertEqual(paciente.email, "juan@test.com")
    
    def test_paciente_str(self):
        paciente = Paciente(
            institucion=self.institucion,
            nombre="Juan",
            apellido="Pérez"
        )
        self.assertEqual(str(paciente), "Juan Pérez")
    
    def test_documento_unico_por_tenant(self):
        Paciente.objects.create(
            institucion=self.institucion,
            documento="12345678-9",
            nombre="Juan",
            apellido="Pérez"
        )
        with pytest.raises(Exception):
            Paciente.objects.create(
                institucion=self.institucion,
                documento="12345678-9",
                nombre="Pedro",
                apellido="González"
            )
```

---

### 3.2 Pruebas de Integración

| Propiedad | Valor |
|-----------|-------|
| **Objetivo** | Validar interacción entre componentes |
| **Herramienta** | pytest, pytest-django, factory_boy |
| **Cobertura objetivo** | Flujos críticos 100% |
| **Ejecución** | En cada commit (CI/CD) |
| **Duración** | < 5 minutos |

**Ejemplo:**

```python
# tests/test_integration.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from apps.core.models import Institucion, Profesional, Paciente

class CitaIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.institucion = Institucion.objects.create(
            nombre="Clínica Test",
            subdominio="test"
        )
        self.profesional = Profesional.objects.create(
            institucion=self.institucion,
            nombre="Dr. Test",
            tipo="medico"
        )
        self.paciente = Paciente.objects.create(
            institucion=self.institucion,
            documento="12345678-9",
            nombre="Juan",
            apellido="Pérez"
        )
    
    def test_agendar_cita_flujo_completo(self):
        # 1. Crear cita
        response = self.client.post('/api/citas/', {
            'paciente_id': self.paciente.id,
            'profesional_id': self.profesional.id,
            'fecha': '2026-06-15',
            'hora': '10:00'
        })
        self.assertEqual(response.status_code, 201)
        cita_id = response.data['id']
        
        # 2. Crear preclínica
        response = self.client.post('/api/preclinica/', {
            'cita_id': cita_id,
            'presion_arterial_sis': 120,
            'presion_arterial_dia': 80,
            'frecuencia_cardiaca': 75,
            'temperatura': 36.5
        })
        self.assertEqual(response.status_code, 201)
        
        # 3. Crear consulta
        response = self.client.post('/api/consultas/', {
            'cita_id': cita_id,
            'motivo_consulta': "Dolor de cabeza",
            'diagnostico': "R51"
        })
        self.assertEqual(response.status_code, 201)
```

---

### 3.3 Pruebas de API

| Propiedad | Valor |
|-----------|-------|
| **Objetivo** | Validar endpoints REST |
| **Herramienta** | pytest, DRF APIClient, drf-yasg (schema validation) |
| **Cobertura objetivo** | 100% de endpoints |
| **Ejecución** | En cada PR (CI/CD) |

**Ejemplo:**

```python
# tests/test_api.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class PacienteAPITest(APITestCase):
    def setUp(self):
        self.institucion = Institucion.objects.create(
            nombre="Clínica Test",
            subdominio="test"
        )
        self.client.credentials(HTTP_X_INSTITUTION_ID=self.institucion.id)
    
    def test_listar_pacientes(self):
        url = reverse('paciente-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_crear_paciente(self):
        url = reverse('paciente-list')
        data = {
            'documento': '12345678-9',
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'email': 'juan@test.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre'], 'Juan')
    
    def test_crear_paciente_sin_documento(self):
        url = reverse('paciente-list')
        data = {
            'nombre': 'Juan',
            'apellido': 'Pérez'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
```

---

### 3.4 Pruebas de UI (End-to-End)

| Propiedad | Valor |
|-----------|-------|
| **Objetivo** | Validar flujos completos de usuario |
| **Herramienta** | Selenium / Playwright |
| **Cobertura objetivo** | Flujos críticos (login, consulta, agendamiento) |
| **Ejecución** | Diaria / En releases |
| **Duración** | < 20 minutos |

**Ejemplo (Playwright):**

```python
# tests/e2e/test_consulta_flow.py
from playwright.sync_api import sync_playwright

def test_consulta_completa():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # 1. Login médico
        page.goto("https://test.xmedical.com")
        page.fill("#username", "doctor@test.com")
        page.fill("#password", "password123")
        page.click("#login-btn")
        
        # 2. Ver dashboard
        assert page.is_visible("text=Pacientes en espera")
        
        # 3. Iniciar consulta
        page.click("button:has-text('Comenzar próximo paciente')")
        
        # 4. Flujo de 7 pasos
        assert page.is_visible("text=Paso 1 de 7: Revisar preclínica")
        page.click("button:has-text('Iniciar consulta médica')")
        
        # 5. Motivo
        page.fill("#motivo", "Dolor de cabeza")
        page.click("button:has-text('Siguiente')")
        
        # 6. Diagnóstico
        page.fill("#diagnostico", "cefalea")
        page.click("text=R51 - Cefalea")
        page.click("button:has-text('Siguiente')")
        
        # 7. Plan
        page.click("text=Alta médica")
        page.click("button:has-text('Finalizar')")
        
        # 8. Confirmación
        assert page.is_visible("text=Consulta finalizada")
        
        browser.close()
```

---

### 3.5 Pruebas de Rendimiento / Carga

| Propiedad | Valor |
|-----------|-------|
| **Objetivo** | Validar comportamiento bajo carga |
| **Herramienta** | Locust / k6 / JMeter |
| **Escenarios** | 100, 500, 1000 usuarios concurrentes |
| **Ejecución** | Pre-release / Mensual |
| **Métricas objetivo** | Tiempo respuesta < 500ms, error rate < 1% |

**Ejemplo (Locust):**

```python
# tests/performance/locustfile.py
from locust import HttpUser, task, between

class XMedicalUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def listar_pacientes(self):
        self.client.get("/api/pacientes/")
    
    @task(2)
    def listar_citas_hoy(self):
        self.client.get("/api/citas/hoy/")
    
    @task(1)
    def crear_cita(self):
        self.client.post("/api/citas/", json={
            "paciente_id": 1,
            "profesional_id": 1,
            "fecha": "2026-06-15",
            "hora": "10:00"
        })
    
    @task(1)
    def login(self):
        self.client.post("/api/auth/login/", json={
            "username": "test@test.com",
            "password": "test123"
        })

# Ejecutar: locust -f locustfile.py --host=https://test.xmedical.com
```

---

### 3.6 Pruebas de Seguridad

| Propiedad | Valor |
|-----------|-------|
| **Objetivo** | Identificar vulnerabilidades |
| **Herramienta** | OWASP ZAP, Bandit (Python), npm audit |
| **Escaneo** | Estático (CI) + Dinámico (mensual) |
| **Cobertura** | OWASP Top 10 |

**Comandos:**

```bash
# Análisis estático Python
bandit -r apps/ -f json -o bandit_report.json

# Escaneo de dependencias
pip-audit --requirement requirements.txt
npm audit

# Escaneo dinámico con OWASP ZAP
zap-api-scan.py -t https://test.xmedical.com/api/v1/ \
    -f openapi -f openapi.yaml \
    -r zap_report.html
```

**Casos de prueba de seguridad:**

| ID | Prueba | Método | Criterio |
|----|--------|--------|----------|
| SEC-01 | SQL Injection | Enviar `' OR '1'='1` en campos | Debe ser sanitizado |
| SEC-02 | XSS | Enviar `<script>alert(1)</script>` | Debe ser escapado |
| SEC-03 | CSRF | POST sin token CSRF | Debe ser rechazado |
| SEC-04 | Auth Bypass | Intentar acceder sin token | 401 Unauthorized |
| SEC-05 | Tenant Isolation | Intentar ver datos de otro tenant | 403 Forbidden |
| SEC-06 | Rate Limiting | 200 requests en 1 minuto | Bloqueo temporal |

---

### 3.7 Pruebas de Aceptación (UAT)

| Propiedad | Valor |
|-----------|-------|
| **Objetivo** | Validar que el sistema cumple requisitos de negocio |
| **Participantes** | Médicos, enfermeras, recepcionistas (piloto) |
| **Duración** | 2 semanas |
| **Criterio de éxito** | > 90% de casos de uso aprobados |

**Casos de prueba UAT:**

| ID | Caso de uso | Actor | Criterio |
|----|-------------|-------|----------|
| UAT-01 | Registrar paciente nuevo | Recepcionista | < 2 minutos |
| UAT-02 | Agendar cita específica | Recepcionista | Horario correcto |
| UAT-03 | Realizar preclínica | Enfermera | Todos los campos registrados |
| UAT-04 | Realizar consulta completa (7 pasos) | Médico | Flujo completado |
| UAT-05 | Registrar diagnóstico CIE-10 | Médico | Búsqueda funciona |
| UAT-06 | Generar referencia a especialista | Médico | Referencia creada |
| UAT-07 | Ver historia clínica | Médico | Datos correctos |
| UAT-08 | Cancelar cita | Recepcionista | Cupo liberado |
| UAT-09 | Dashboard médico | Médico | Muestra agenda correcta |
| UAT-10 | Aislamiento multi-tenant | Admin | Datos no se mezclan |

---

### 3.8 Pruebas de Recuperación (Disaster Recovery)

| Propiedad | Valor |
|-----------|-------|
| **Objetivo** | Validar recuperación ante fallos |
| **Frecuencia** | Trimestral |
| **Escenarios** | Falla BD, corrupción datos, caída servidor |

**Escenarios de prueba:**

| ID | Escenario | Procedimiento | Tiempo objetivo |
|----|-----------|---------------|-----------------|
| DR-01 | Falla de base de datos | Restaurar desde backup | < 4 horas |
| DR-02 | Corrupción de datos | Restaurar tabla específica | < 1 hora |
| DR-03 | Caída de servidor | Levantar réplica | < 30 minutos |
| DR-04 | Pérdida de archivos (QR, logos) | Restaurar desde S3 | < 15 minutos |

---

## 4. HERRAMIENTAS DE PRUEBAS

| Categoría | Herramienta | Propósito |
|-----------|-------------|-----------|
| **Unitarias** | pytest, pytest-django | Tests de Python |
| **Cobertura** | pytest-cov | Medición de cobertura |
| **Integración** | factory_boy | Creación de datos de prueba |
| **API** | DRF APIClient, drf-yasg | Tests de endpoints |
| **UI** | Playwright / Selenium | Tests end-to-end |
| **Rendimiento** | Locust | Pruebas de carga |
| **Seguridad** | OWASP ZAP, Bandit | Escaneo de vulnerabilidades |
| **Mocking** | unittest.mock | Simular APIs externas |
| **BD** | pytest-django, SQLite (test) | Base de datos de prueba |

---

## 5. AMBIENTES DE PRUEBAS

| Ambiente | URL | Propósito | Datos |
|----------|-----|-----------|-------|
| **Desarrollo** | dev.xmedical.com | Pruebas de desarrollador | Datos sintéticos |
| **Integración** | ci.xmedical.com | CI/CD automatizado | Datos sintéticos |
| **Staging** | staging.xmedical.com | Pruebas pre-release | Copia anonimizada |
| **UAT** | uat.xmedical.com | Pruebas de aceptación | Datos pilotos reales |
| **Producción** | *.xmedical.com | Sistema real | Datos reales |

---

## 6. CRITERIOS DE ÉXITO

### 6.1 Por tipo de prueba

| Tipo | Cobertura | Tasa éxito | Tiempo máximo |
|------|-----------|------------|---------------|
| Unitarias | > 80% líneas | 100% | < 2 min |
| Integración | Flujos críticos | 100% | < 5 min |
| API | 100% endpoints | 100% | < 3 min |
| UI (E2E) | Flujos críticos | > 95% | < 20 min |
| Rendimiento | 100 usuarios | < 500ms | < 30 min |
| Seguridad | 0 críticas | 0 vulnerabilidades altas | < 60 min |

### 6.2 Por severidad de bugs

| Severidad | Definición | Acción |
|-----------|------------|--------|
| **Crítica** | Sistema no funciona, pérdida de datos | Bloquea release |
| **Alta** | Funcionalidad principal afectada | Bloquea release |
| **Media** | Funcionalidad secundaria afectada | Parche post-release |
| **Baja** | UI, texto, cosméticos | Próximo release |

---

## 7. PLAN DE PRUEBAS POR FASE

### Fase 1 (MVP) - 4 semanas

| Semana | Actividad | Entregable |
|--------|-----------|------------|
| Semana 1 | Setup de herramientas | Configuración CI/CD |
| Semana 2 | Pruebas unitarias + integración | Cobertura > 70% |
| Semana 3 | Pruebas API + UI básicas | Suite de tests |
| Semana 4 | UAT con piloto | Reporte de aceptación |

### Fase 2 - 4 semanas

| Semana | Actividad | Entregable |
|--------|-----------|------------|
| Semana 1 | Pruebas de referencias | Tests 2do nivel |
| Semana 2 | Pruebas de QR | Validación escaneo |
| Semana 3 | Pruebas de rendimiento | Reporte Locust |
| Semana 4 | Pruebas de seguridad (ZAP) | Reporte vulnerabilidades |

### Fase 3 - 6 semanas

| Semana | Actividad | Entregable |
|--------|-----------|------------|
| Semana 1-2 | Pruebas de modelos IA | Validación precisión |
| Semana 3 | Pruebas de integración APIs IA | Mocks + reales |
| Semana 4 | Pruebas portal paciente | UAT pacientes |
| Semana 5 | Pruebas de recuperación (DR) | Reporte DR |
| Semana 6 | Regresión completa | Release readiness |

---

## 8. REPORTES Y MÉTRICAS

### 8.1 Reporte diario (CI/CD)

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
      
      - name: Run unit tests
        run: pytest tests/unit --cov=apps --cov-report=xml
      
      - name: Run integration tests
        run: pytest tests/integration
      
      - name: Run API tests
        run: pytest tests/api
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### 8.2 Dashboard de calidad

| Métrica | Objetivo | Actual |
|---------|----------|--------|
| Cobertura de código | > 80% | 82% |
| Tests pasando | 100% | 98% |
| Bugs abiertos | < 10 | 5 |
| Bugs críticos | 0 | 0 |
| Tiempo de ejecución | < 10 min | 8 min |

---

## 9. CRONOGRAMA DE PRUEBAS (RESUMEN)

```
Semanas 1-4 (MVP)     ████████░░░░░░░░░░░░  (pruebas básicas)
Semanas 5-8 (Fase 2)  ░░░░░░░░████████░░░░  (pruebas avanzadas)
Semanas 9-14 (Fase 3) ░░░░░░░░░░░░░░██████  (IA + regresión)
```

---

## 10. APROBACIÓN

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Product Owner | [Usuario] | ✅ Aprobado | 2026 |
| QA Lead | [Usuario] | ✅ Aprobado | 2026 |
| Agente Documentación | DeepSeek | Generado | 2026 |

---

**Fin del Documento 10: Plan de Pruebas**

---

## RESUMEN DEL DOCUMENTO

| Aspecto | Valor |
|---------|-------|
| **Tipos de pruebas** | 8 (unitarias, integración, API, UI, rendimiento, seguridad, UAT, DR) |
| **Cobertura objetivo** | > 80% |
| **Herramientas** | 12 |
| **Ambientes** | 5 |
| **Criterios de éxito** | Por tipo y severidad |
| **Casos de prueba** | 10 UAT, 6 seguridad, 4 DR |
| **Cronograma** | 14 semanas (3 fases) |

---
