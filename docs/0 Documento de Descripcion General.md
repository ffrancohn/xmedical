# DOCUMENTO 0: DESCRIPCIÓN GENERAL DEL PROYECTO
## XMedical - Sistema de Gestión Clínica Multi-tenant para Primer y Segundo Nivel

| Versión | Fecha | Autor | Estado |
|---------|-------|-------|--------|
| 1.1 | 2026 | Agente de Documentación Técnica | **Aprobado** |

---

## 1. ¿QUÉ ES XMEDICAL?

**XMedical** es un sistema de gestión clínica **multi-tenant** (soporta múltiples instituciones/clientes en una sola instalación) diseñado para instituciones de salud de **primer nivel** (medicina general, atención primaria) y **segundo nivel** (especialidades, subespecialidades), tanto para **clínicas privadas** como **instituciones públicas**.

El sistema opera como **SaaS (Software as a Service)** o **on-premise**, permitiendo que cada institución tenga su propio entorno aislado con su configuración, pacientes, médicos y datos clínicos.

---

## 2. ¿QUÉ PROBLEMA RESUELVE?

| Problema | Solución XMedical |
|----------|-------------------|
| Agendamiento rígido (solo fechas fijas) | Agendamiento específico + flexible (por rango) |
| Validación manual de documentos | Visión artificial para cédulas/pasaportes |
| Flujos clínicos descoordinados | Flujo guiado paso a paso (wizard) |
| Médicos generales y especialistas aislados | Referencia/contrarreferencia integrada |
| Sin apoyo de IA | Sugerencia diagnóstica + modelos predictivos |
| Baja adherencia a tratamientos | Recordatorios por correo (citas y medicamentos) |
| Falta de parametrización | Configuración 100% vía UI sin programación |
| **Múltiples clínicas en una misma instalación** | **Arquitectura multi-tenant (aislamiento completo)** |

---

## 3. ¿QUIÉNES SON LOS USUARIOS?

| Usuario | Funcionalidades principales |
|---------|----------------------------|
| **Médico general (1er nivel)** | Consulta guiada, referencias a especialistas, HCE |
| **Médico especialista (2do nivel)** | Bandeja de referencias, consulta especializada, contrarreferencia |
| **Enfermera** | Preclínica, signos vitales, triaje |
| **Recepcionista** | Registro de pacientes, agendamiento de citas |
| **Administrador de institución** | Parametrización, usuarios, horarios, especialidades de SU institución |
| **Superadministrador (Global)** | Gestionar múltiples instituciones, monitoreo global |
| **Paciente** | Autoagendamiento web, portal de resultados |
| **TI / Soporte** | Despliegue, backups, monitoreo multi-tenant |

---

## 4. ¿CUÁLES SON LOS NIVELES DE ATENCIÓN?

| Nivel | Descripción | Estado |
|-------|-------------|--------|
| **Primer nivel** | Medicina general, atención primaria | ✅ Disponible (Fase 1) |
| **Segundo nivel** | Especialidades (cardiología, endocrinología, etc.) | ✅ Disponible (Fase 2) |
| **Tercer nivel** | Hospitalización, cirugía, UCI | 🔮 Visión a futuro |

---

## 5. ¿QUÉ TECNOLOGÍAS USA?

| Capa | Tecnología |
|------|------------|
| **Frontend** | Django templates + DaisyUI + Tailwind |
| **Backend** | Django (FastAPI para IA post-MVP) |
| **Base de Datos** | PostgreSQL (con RLS para multi-tenant) |
| **IA** | Visión artificial, modelos predictivos, LLM para sugerencias |
| **Tareas programadas** | Celery + Redis (por tenant o compartidas) |
| **QR** | Python segno |

---

## 6. ¿CUÁLES SON LAS CLASIFICACIONES CLÍNICAS SOPORTADAS?

| Clasificación | Propósito | Especialidades | Estado |
|---------------|-----------|----------------|--------|
| **CIE-10/CIE-11** | Diagnóstico de enfermedades | Todas | ✅ MVP |
| **CIF** | Funcionamiento y discapacidad | Rehabilitación, kinesiología | 🔮 Futuro |
| **CIE-O** | Tumores (oncología) | Oncología, Anatomía Patológica | 🔮 Futuro |
| **ICHI** | Intervenciones sanitarias | Cirugía, procedimientos | 🔮 Futuro |

---

## 7. ¿CUÁL ES EL ALCANCE POR FASES?

| Fase | Duración | Entregable principal |
|------|----------|----------------------|
| **Fase 1 (MVP)** | 4 semanas | 1er nivel: Citas + flujo guiado + parametrización básica + **multi-tenant básico** |
| **Fase 2** | 4 semanas | 2do nivel: Referencias + especialidades + QR + recordatorios |
| **Fase 3** | 6 semanas | IA predictiva + detección riesgos + portal paciente |
| **Fase 4+** | Futuro | Tercer nivel (hospitalización, cirugías) |

---

## 8. ¿CUÁLES SON LOS DIFERENCIADORES CLAVE?

| # | Diferenciador |
|---|---------------|
| 1 | Flujo guiado paso a paso para cada usuario |
| 2 | Parametrización 100% vía UI (sin programación) |
| 3 | Agendamiento dual (específico + flexible) |
| 4 | Referencia/contrarreferencia integrada 1er ↔ 2do nivel |
| 5 | IA en tres vertientes: visión, predictiva, generativa |
| 6 | Códigos QR para órdenes, recetas y check-in |
| 7 | Recordatorios automáticos por correo |
| 8 | Historia clínica por episodios y encuentros |
| 9 | Auditoría completa de cambios |
| 10 | Tecnología open source (bajo costo) |
| 11 | **Arquitectura multi-tenant (múltiples clínicas en una instalación)** |

---

## 9. ARQUITECTURA MULTI-TENANT (DETALLADA)

### 9.1 ¿Qué significa multi-tenant?

XMedical permite que **múltiples instituciones (clientes)** compartan la misma instalación del software, pero con **datos completamente aislados**. Cada institución ve y opera solo sus propios datos.

### 9.2 Escenarios soportados

| Escenario | Ejemplo | Soporte |
|-----------|---------|---------|
| Una clínica privada | "Clínica Los Andes" | ✅ Sí |
| Múltiples sedes de la misma red | "Clínica Los Andes - Sede Norte" y "Sede Sur" | ✅ Sí (como mismo tenant o separados) |
| SaaS ofreciendo servicio a muchas clínicas | XMedical como servicio a 50+ clínicas | ✅ Sí |
| Data center regional con múltiples hospitales | "Hospital Regional Norte" y "Hospital Regional Sur" | ✅ Sí |
| Franquicias médicas | "Medicenter" con 20 sucursales | ✅ Sí |

### 9.3 ¿Qué comparten todas las instituciones?

| Recurso | Compartido | Explicación |
|---------|------------|-------------|
| Código fuente | ✅ Sí | Todos usan la misma versión del software |
| Infraestructura (servidores, BD) | ✅ Sí | Misma instalación física |
| Catálogos base | ✅ Sí | CIE-10, especialidades base, países, etc. |
| Módulos de IA | ✅ Sí | Modelos y APIs compartidas |

### 9.4 ¿Qué es independiente por institución?

| Entidad | Independencia | Explicación |
|---------|---------------|-------------|
| **Pacientes** | ✅ Completamente aislados | Paciente de Clínica A NO es visible en Clínica B |
| **Médicos** | ✅ Pertenecen a una institución | Un médico puede trabajar en múltiples clínicas (con usuarios separados) |
| **Citas** | ✅ Por institución | Cada clínica tiene su propia agenda |
| **Consultas/HCE** | ✅ Visibles solo dentro de la institución | Datos clínicos no se comparten entre clínicas |
| **Configuración** | ✅ Cada institución tiene sus parámetros | Horarios, especialidades activas, flujos |
| **Usuarios (admin, recepción)** | ✅ Por institución | Cada clínica gestiona su propio personal |
| **Reportes** | ✅ Solo datos de su institución | KPIs, epidemiológicos, financieros |
| **Facturación** | ✅ Independiente | Cada clínica tiene su propia lógica de facturación |
| **Portal del paciente** | ✅ Por institución | Portal aislado por cada clínica |

### 9.5 Modelo técnico

**Modelo seleccionado:** Tabla única con `institucion_id` + **Row Level Security (RLS)** en PostgreSQL

```sql
-- Estructura base
CREATE TABLE institucion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    subdominio VARCHAR(100) UNIQUE,  -- ej: 'clinicaandes'
    tipo VARCHAR(50),  -- 'privada', 'publica'
    configuracion JSONB,
    activo BOOLEAN DEFAULT true
);

-- Todas las tablas de negocio incluyen institucion_id
CREATE TABLE paciente (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id),
    nombre VARCHAR(100),
    documento VARCHAR(20),
    -- ... otros campos
);

-- Política RLS (PostgreSQL)
ALTER TABLE paciente ENABLE ROW LEVEL SECURITY;
CREATE POLICY paciente_tenant_isolation ON paciente
    USING (institucion_id = current_setting('app.current_institucion_id')::INTEGER);
```

### 9.6 Identificación de la institución

| Método | Ejemplo | Uso |
|--------|---------|-----|
| **Subdominio** | `clinicaandes.xmedical.com` | Método principal (SaaS) |
| **Dominio personalizado** | `clinicaandes.com` apunta a XMedical | Clínicas grandes |
| **Campo en login** | Usuario selecciona "Clínica Los Andes" | Respaldo / intranet |
| **Header en API** | `X-Institution-ID: 1` | Integraciones |

### 9.7 Roles multi-tenant

| Rol | Alcance | Permisos |
|-----|---------|----------|
| **Superadministrador** | Global | Crear/editar instituciones, monitoreo global, soporte técnico |
| **Administrador de institución** | Su institución | Configurar su clínica, usuarios, horarios, especialidades |
| **Médico, Enfermera, Recepcionista** | Su institución | Operaciones diarias de su clínica |

### 9.8 Aislamiento de datos (seguridad)

| Mecanismo | Propósito |
|-----------|-----------|
| **RLS (Row Level Security)** | Base de datos filtra automáticamente por `institucion_id` |
| **Middleware Django** | Inyecta `current_institucion_id` en cada request |
| **Vistas por tenant** | Las consultas nunca cruzan instituciones |
| **Auditoría con tenant** | Logs incluyen `institucion_id` para trazabilidad |

### 9.9 Backups y restauración

| Nivel | Estrategia |
|-------|-------------|
| **Global** | Backup completo de toda la BD periódico |
| **Por institución** | Posibilidad de exportar/importar datos de una sola clínica |

---

## 10. GLOSARIO DE TÉRMINOS CLAVE (NUEVOS)

| Término | Definición |
|---------|-------------|
| **Multi-tenant** | Arquitectura donde múltiples clientes comparten la misma instalación de software con datos aislados |
| **Tenant** | Cada institución/cliente dentro del sistema multi-tenant |
| **Institución** | Clínica, hospital u organización de salud que usa XMedical |
| **Aislamiento de datos** | Garantía de que los datos de un tenant no son visibles por otros |
| **Superadministrador** | Usuario con capacidad de gestionar múltiples tenants |

---

**Fin del Documento 0: Descripción General del Proyecto**

---

## RESUMEN DE CAMBIOS REALIZADOS

| # | Cambio | Justificación |
|---|--------|---------------|
| 1 | Título actualizado: incluye "Multi-tenant" | Refleja la capacidad clave |
| 2 | Sección 1: se añade "multi-tenant" y "SaaS" | Explicitar el modelo de negocio |
| 3 | Sección 2: nuevo problema "Múltiples clínicas" | Justificar multi-tenant |
| 4 | Sección 3: nuevo rol "Superadministrador (Global)" | Necesario para gestionar tenants |
| 5 | Sección 5: BD con RLS | Aclarar tecnología específica |
| 6 | Sección 7: Fase 1 incluye "multi-tenant básico" | Prioridad desde MVP |
| 7 | Sección 8: nuevo diferenciador #11 | Multi-tenant como ventaja competitiva |
| 8 | **Sección 9 completamente reescrita y ampliada** | Desde 1 línea a 9 subsecciones detalladas |
| 9 | Nueva Sección 10: Glosario | Términos específicos de multi-tenant |

---
