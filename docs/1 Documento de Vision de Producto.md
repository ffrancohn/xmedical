# DOCUMENTO 1: VISIÓN DEL PRODUCTO (ACTUALIZADO)
## XMedical - Sistema de Gestión Clínica Multi-tenant para Primer y Segundo Nivel de Atención

| Versión | Fecha | Autor | Estado |
|---------|-------|-------|--------|
| 2.3 | 2026 | Agente de Documentación Técnica | **Aprobado** |

---

## 1. PROPÓSITO DEL SISTEMA

**XMedical** es un sistema integral de gestión clínica **multi-tenant** (soporta múltiples instituciones/clientes en una sola instalación) diseñado para instituciones de salud de **primer nivel** (atención primaria, medicina general, consulta externa básica) y **segundo nivel** (especialidades, subespecialidades, atención ambulatoria avanzada), tanto para **clínicas privadas** como **instituciones públicas**, con **visión de expansión a tercer nivel** (hospitalización, cirugía, cuidados intensivos) en fases posteriores.

El sistema opera como **SaaS (Software as a Service)** o **on-premise**, permitiendo que cada institución tenga su propio entorno aislado con su configuración, pacientes, médicos y datos clínicos.

**Valor fundamental:** Unificar, estandarizar y optimizar los flujos de atención sanitaria mediante una **interfaz guiada paso a paso**, **parámetros configurables por institución**, **aislamiento multi-tenant** y **tecnologías de IA** (visión artificial, modelos predictivos, sugerencia diagnóstica), manteniendo la flexibilidad para adaptarse a clínicas públicas o privadas, con **capacidad de crecimiento hacia entornos hospitalarios**.

---

## 2. PROBLEMA A RESOLVER

| # | Problema | Impacto | Enfoque XMedical |
|---|----------|---------|------------------|
| 1 | **Falta de parametrización** - Cada clínica tiene flujos, horarios, especialidades y roles distintos | Implementaciones rígidas, costosas de adaptar | ✅ **Configuración 100% parametrizable** (horarios, especialidades, perfiles, flujos) |
| 2 | **Brecha entre niveles** - Primer nivel (medicina general) y segundo nivel (especialistas) trabajan aislados | Pérdida de continuidad, referencias manuales | ✅ **Flujo integrado**: Referencia → Especialista → Retorno → Seguimiento |
| 3 | **Agendamiento rígido** - Solo fechas fijas, no se adapta a disponibilidad del paciente | Alto ausentismo (20-35%) | ✅ **Dual**: Específico + Flexible (rango con asignación automática) |
| 4 | **Validación manual de documentos** | Errores, suplantación, lentitud | ✅ **Visión artificial** para cédulas/pasaportes |
| 5 | **Flujos clínicos descoordinados** - Cita → Preclínica → Consulta → Referencia no están conectados | Reprocesos, pérdida de tiempo | ✅ **Flujo guiado paso a paso** (wizard clínico) |
| 6 | **Sobrecarga cognitiva del médico** - Sin apoyo de IA | Diagnósticos tardíos, omisiones | ✅ **Sugerencia diagnóstica por IA + modelos predictivos** |
| 7 | **Baja adherencia a tratamientos** - Sin recordatorios proactivos | Fallo terapéutico | ✅ **Recordatorios** de citas y medicamentos (correo inicial) |
| 8 | **Múltiples clínicas en una misma instalación** - Cada clínica requiere su propia instalación o mezcla datos | Costos elevados, riesgos de seguridad | ✅ **Arquitectura multi-tenant** (aislamiento completo) |
| 9 | **Falta de integración hospitalaria** (futuro) | Hospitalizaciones aisladas de la historia ambulatoria | 🔮 **Visión a futuro**: Integración con camas, cirugías, UCI |

---

## 3. PROPUESTA DE VALOR POR SEGMENTO

| Segmento | Propuesta de valor (actual) | Visión a futuro |
|----------|----------------------------|-----------------|
| **Clínicas privadas** | Parametrización rápida, imagen profesional, facturación integrable, portal del paciente, **multi-tenant** | + Gestión de hospitalización y cirugías |
| **Instituciones públicas** | Escalabilidad, reportes epidemiológicos, auditoría completa, bajo costo de implementación | + Gestión de camas, lista de espera quirúrgica |
| **Grupos de salud / Franquicias** | **Múltiples sedes en una misma instalación**, datos aislados por sede, reportes consolidados | + Visión de red completa |
| **Médicos generales (1er nivel)** | Flujo guiado, acceso a referencias a especialistas, sugerencias diagnósticas IA | + Visión de evolución hospitalaria de sus pacientes |
| **Especialistas (2do nivel)** | Visión de referencias recibidas, historia clínica por episodio, dashboard por especialidad | + Interconsultas hospitalarias, seguimiento post-alta |
| **Hospitales (3er nivel - futuro)** | - | Gestión de camas, block quirúrgico, UCI, evolución diaria |
| **Enfermeras** | Registro rápido de preclínica, alertas de riesgo, triaje integrado | + Registro de signos vitales periódicos en hospitalización |
| **Pacientes** | Agendamiento flexible, QR check-in, recordatorios, portal de resultados | + Visión de hospitalizaciones, evolución durante internación |
| **Administración de institución** | Parametrización sin programación, dashboards por rol, KPIs de eficiencia | + Ocupación hospitalaria, tiempos de espera quirúrgica |
| **Superadministrador (Global)** | Gestionar múltiples instituciones, monitoreo global, facturación SaaS | + Métricas de uso por tenant |
| **TI / Soporte** | Código abierto, despliegue flexible (on-premise/nube), backups automáticos | + Integración con sistemas de laboratorio e imágenes |

---

## 4. REGISTRO Y SELECCIÓN DE ESPECIALIDAD PARA MÉDICOS

### 4.1 Flujo de registro de médico (Administrador de institución)

```
ADMINISTRADOR DE LA INSTITUCIÓN crea usuario médico
       ↓
┌──────────────────────────────────────────────────────────────────┐
│ REGISTRO DE MÉDICO - SELECCIÓN DE ESPECIALIDAD                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Institución: Clínica Los Andes (automático por contexto)        │
│                                                                  │
│  Datos personales:                                               │
│  • Nombre: [Dr. Carlos Pérez]                                   │
│  • Correo: [carlos.perez@clinica.com]                           │
│  • Teléfono: [123456789]                                        │
│                                                                  │
│  🏥 ESPECIALIDAD (obligatorio):                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ○ Medicina General (Primer nivel)                          ││
│  │ ○ Cardiología (Segundo nivel)                              ││
│  │ ○ Endocrinología (Segundo nivel)                           ││
│  │ ○ Neurología (Segundo nivel)                               ││
│  │ ○ Pediatría (Primer nivel)                                 ││
│  │ ○ Cirugía General (Segundo nivel)                          ││
│  │ ○ Oncología (Segundo nivel)                                ││
│  │ ○ Medicina Física y Rehabilitación (Segundo nivel)         ││
│  │ ○ ...                                                       ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  • Subespecialidad (opcional): [_______________]                 │
│                                                                  │
│  • Nivel de atención: ● Primer nivel  ○ Segundo nivel            │
│    (se determina automáticamente según especialidad)             │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 Flujo de auto-registro (si se permite, requiere validación)

```
MÉDICO se registra en el sistema
       ↓
┌──────────────────────────────────────────────────────────────────┐
│ AUTO-REGISTRO DE MÉDICO                                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Seleccione su institución:                                      │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ [Clínica Los Andes                     ▼]                   ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Datos personales:                                               │
│  • Nombre: [_______________]                                     │
│  • Correo: [_______________]                                     │
│  • Contraseña: [_______________]                                 │
│                                                                  │
│  🏥 Seleccione su especialidad:                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ [Medicina General                    ▼]                     ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  • Número de registro médico (opcional): [_______________]       │
│                                                                  │
│  ⚠️ El registro será validado por un administrador de la institución │
│                                                                  │
│  [Registrarse]                                                   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 4.3 Impacto en el sistema

| Aspecto | Impacto |
|---------|---------|
| **Multi-tenant** | Médico pertenece a UNA institución; no puede ver datos de otras |
| **Agendamiento** | Al agendar una cita, se muestra especialidad, luego médicos de esa especialidad de la misma institución |
| **Referencias** | Médico general solo puede referir a especialidades de segundo nivel de su misma institución |
| **Dashboard** | Cada médico ve su agenda filtrada por su especialidad Y por su institución |
| **Flujo de consulta** | Los campos de examen físico se parametrizan por especialidad e institución |
| **Clasificaciones clínicas** | Oncólogo ve opciones CIE-O; Rehabilitador ve opciones CIF (configurable por institución) |

---

## 5. NIVELES DE ATENCIÓN SOPORTADOS

| Nivel | Descripción | Módulos específicos | Flujo típico | Estado |
|-------|-------------|---------------------|--------------|--------|
| **Primer nivel** | Medicina general, atención primaria, consulta externa básica | Citas, preclínica, consulta general, farmacia básica, referencia a especialista | Paciente → Cita → Médico general → (Alta o Referencia a 2do nivel) | ✅ **Disponible** |
| **Segundo nivel** | Especialidades (cardiología, endocrinología, etc.) y subespecialidades | Recepción de referencias, consulta especializada, órdenes de exámenes avanzados, contrarreferencia | Referencia desde 1er nivel → Especialista → (Alta o Retorno a 1er nivel) | ✅ **Disponible** |
| **Tercer nivel** (Futuro) | Hospitalización, cirugía, cuidados intensivos, procedimientos complejos | Gestión de camas, block quirúrgico, UCI, evolución diaria, interconsultas hospitalarias | Hospitalización → Evolución → Cirugía (si aplica) → Alta hospitalaria → Control ambulatorio | 🔮 **Visión a futuro** |

### Flujo entre niveles (actual + visión futura)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         XMEDICAL - FLUJO INTEGRADO (ACTUAL + FUTURO)                  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌─────────────┐│
│   │   1ER NIVEL   │ ──► │    REFERENCIA  │ ──► │   2DO NIVEL   │ ──► │ 3ER NIVEL   ││
│   │ Medicina Gral │      │   (automática) │      │  Especialista │      │ (Futuro)    ││
│   └──────────────┘      └──────────────┘      └──────────────┘      └─────────────┘│
│          │                      │                    │                      │       │
│          │                      │                    │                      │       │
│          ▼                      ▼                    ▼                      ▼       │
│   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌─────────────┐│
│   │    ALTA       │ ◄─── │ CONTRARREFERENCIA │ ◄─── │    ALTA       │ ◄─── │    ALTA     ││
│   │ (seguimiento) │      │ (al 1er nivel)    │      │ (seguimiento) │      │ Hospitalaria││
│   └──────────────┘      └────────────────┘      └──────────────┘      └─────────────┘│
│                                                                                      │
│   🔮 Visión a futuro: Integración con hospitalización, camas, cirugías, UCI          │
│   🏢 Multi-tenant: Todo el flujo está aislado por institución                         │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. PARAMETRIZACIÓN (CLAVE PARA PÚBLICO Y PRIVADO)

XMedical permite configurar **sin programación** los siguientes aspectos, **de forma independiente por cada institución (tenant)**:

| Parámetro | Qué se puede configurar | Ejemplo | Estado |
|-----------|------------------------|---------|--------|
| **Institución (Tenant)** | Nombre, logo, subdominio, tipo (pública/privada), configuración global | "Clínica Los Andes S.A." (subdominio: clinicaandes) | ✅ |
| **Especialidades** | Nombre, código, color, duración de consulta, nivel (1er/2do), subespecialidades | Cardiología (30 min, 2do nivel) | ✅ |
| **Profesionales** | Médicos, enfermeras, recepcionistas: especialidad asignada, horarios, días | Dr. Pérez: Cardiología, Lunes 9-13h | ✅ |
| **Perfiles y permisos** | Roles personalizables con permisos granulares | Crear rol "Farmacéutico jefe" con permisos especiales | ✅ |
| **Horarios** | Días laborales, festivos, horas inhábiles, bloques | Lunes a Viernes 8-18h, sábados 9-13h | ✅ |
| **Flujos clínicos** | Pasos obligatorios/opcionales, orden de pasos | Forzar preclínica antes de consulta (sí/no) | ✅ |
| **Variables clínicas** | Campos personalizables por especialidad | Cardiología: "Fracción eyección", "ECG" | ✅ |
| **CIE-10** | Diagnósticos activos, agrupaciones por especialidad | Activar solo códigos de cardiología para ese servicio | ✅ |
| **Clasificaciones OMS** | Activar CIE-O (oncología), CIF (rehabilitación), ICHI (cirugía) por especialidad | Oncólogo: activar CIE-O | 🔮 Futuro |
| **Servicios auxiliares** | Exámenes, procedimientos, precios (si aplica), tiempos | Hemograma ($5.000), TAC ($150.000) | ✅ |
| **Farmacia** | Medicamentos, equivalentes, alertas de interacciones | Paracetamol 500mg, Ibuprofeno 400mg | ✅ |
| **IA** | Activar/desactivar módulos, umbrales de riesgo, prompts configurables | Prompt personalizado por institución | ✅ |
| **Notificaciones** | Canales (correo/WhatsApp/SMS), plantillas, horarios | Recordatorio 24h antes, plantilla personalizada | ✅ |
| **Camas** (Futuro) | Servicios, tipos de cama (UCI, intermedio, básico), costos por día | UCI (8 camas), Medicina (20 camas) | 🔮 |
| **Block quirúrgico** (Futuro) | Pabellones, equipos, tiempos de cirugía por especialidad | Pabellón 1: Cirugía general (2h) | 🔮 |

---

## 7. ARQUITECTURA MULTI-TENANT (DETALLADA)

XMedical soporta **múltiples instituciones (clientes)** en una sola instalación, permitiendo:

| Escenario | Soporte |
|-----------|---------|
| Una clínica privada | ✅ Sí |
| Múltiples sedes de la misma red | ✅ Sí (mismo tenant o tenants separados) |
| SaaS ofreciendo servicio a muchas clínicas | ✅ Sí |
| Data center regional con múltiples hospitales | ✅ Sí |
| Franquicias médicas | ✅ Sí |

### 7.1 ¿Qué comparten todas las instituciones?

| Recurso | Compartido | Explicación |
|---------|------------|-------------|
| Código fuente | ✅ Sí | Todos usan la misma versión del software |
| Infraestructura (servidores, BD) | ✅ Sí | Misma instalación física |
| Catálogos base | ✅ Sí | CIE-10, especialidades base, países, etc. |
| Módulos de IA | ✅ Sí | Modelos y APIs compartidas |

### 7.2 ¿Qué es independiente por institución (tenant)?

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

### 7.3 Modelo técnico

**Modelo seleccionado:** Tabla única con `institucion_id` + **Row Level Security (RLS)** en PostgreSQL

```sql
-- Estructura base
CREATE TABLE institucion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    subdominio VARCHAR(100) UNIQUE,  -- ej: 'clinicaandes'
    tipo VARCHAR(50),  -- 'privada', 'publica'
    configuracion JSONB,
    activo BOOLEAN DEFAULT true,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Todas las tablas de negocio incluyen institucion_id
CREATE TABLE profesional (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id),
    -- ... resto de campos
);

-- Política RLS (PostgreSQL)
ALTER TABLE profesional ENABLE ROW LEVEL SECURITY;
CREATE POLICY profesional_tenant_isolation ON profesional
    USING (institucion_id = current_setting('app.current_institucion_id')::INTEGER);
```

### 7.4 Identificación de la institución

| Método | Ejemplo | Uso |
|--------|---------|-----|
| **Subdominio** | `clinicaandes.xmedical.com` | Método principal (SaaS) |
| **Dominio personalizado** | `clinicaandes.com` apunta a XMedical | Clínicas grandes |
| **Campo en login** | Usuario selecciona "Clínica Los Andes" | Respaldo / intranet |
| **Header en API** | `X-Institution-ID: 1` | Integraciones |

### 7.5 Roles multi-tenant

| Rol | Alcance | Permisos |
|-----|---------|----------|
| **Superadministrador** | Global | Crear/editar instituciones, monitoreo global, soporte técnico |
| **Administrador de institución** | Su institución | Configurar su clínica, usuarios, horarios, especialidades |
| **Médico, Enfermera, Recepcionista** | Su institución | Operaciones diarias de su clínica |

### 7.6 Ejemplo de flujo multi-tenant

```
Usuario de "Clínica Los Andes" ingresa a clinicaandes.xmedical.com
       ↓
Sistema identifica institución por subdominio → institucion_id = 1
       ↓
Middleware Django inyecta current_institucion_id = 1 en la consulta
       ↓
Todas las consultas SQL tienen filtro WHERE institucion_id = 1
       ↓
Usuario ve SOLO datos de Clínica Los Andes
       ↓
Si intenta acceder a /api/pacientes/ sin filtro, RLS lo bloquea
```

---

## 8. FLUJO GUIADO COMPLETO (MÉDICO)

El sistema guía al médico **paso a paso** desde que ingresa hasta que finaliza la consulta, adaptando los pasos según su **especialidad** y su **institución**:

| # | Paso | Acción | Sistema hace |
|---|------|--------|--------------|
| 0 | Login | Ingresa credenciales (vía subdominio o selección) | Identifica institución, valida, identifica especialidad, redirige a dashboard personalizado |
| 1 | Dashboard | Ve agenda del día (filtrada por su especialidad E institución) | Muestra citas pendientes, en preclínica, atendidas |
| 2 | Selección | Elige paciente o "Comenzar próximo" | Carga datos de preclínica (si existe) |
| 3 | Preclínica | Revisa signos vitales registrados | Muestra datos de enfermería + alertas de riesgo |
| 4 | Motivo | Registra motivo de consulta | Guarda automáticamente |
| 5 | Anamnesis | Marca antecedentes | Sugiere preguntas según especialidad |
| 6 | Examen físico | Registra hallazgos | **Campos específicos por especialidad** (parametrizados por institución) |
| 7 | Diagnóstico | Selecciona CIE-10 | **IA sugiere según especialidad** + activa clasificaciones adicionales (CIE-O si oncólogo, CIF si rehabilitador) |
| 8 | Plan | Define conducta (alta/cita/referencia/exámenes/medicamentos) | Genera QR, recetas electrónicas |
| 9 | Resumen | Confirma todo | Guarda, notifica, muestra siguiente paciente |

---

## 9. OBJETIVOS POR PLAZO

### Corto plazo (MVP - 4 semanas) - 1er Nivel + Multi-tenant básico

| # | Objetivo | Métrica de éxito |
|---|----------|------------------|
| 1 | Registro de pacientes (presencial + en línea básico) | 95% registros < 2 min |
| 2 | Agendamiento específico (fecha/hora fija) | 100% sin conflictos |
| 3 | Flujo completo 1er nivel: Cita → Preclínica → Consulta | Tiempo < 45 min |
| 4 | Registro de diagnósticos CIE-10 | 100% consultas con código |
| 5 | Perfiles básicos (admin, recepción, médico general, enfermera) | Acceso controlado |
| 6 | **Registro de médicos con selección de especialidad** | 100% médicos tienen especialidad asignada |
| 7 | Dashboard médico filtrado por especialidad | Ver solo pacientes de su especialidad |
| 8 | Parametrización básica (especialidades, profesionales, horarios) | Configurable desde admin |
| 9 | **Soporte multi-tenant básico** | Al menos 2 instituciones en paralelo sin mezclar datos |

### Mediano plazo (Fase 2 - 4 semanas) - 1er + 2do Nivel

| # | Objetivo | Métrica de éxito |
|---|----------|------------------|
| 1 | Agendamiento flexible (rango + asignación automática) | 30% citas vía flexible |
| 2 | Validación IA de documentos | Precisión > 95% |
| 3 | Referencia 1er nivel → 2do nivel | Trazabilidad 100% |
| 4 | Contrarreferencia (especialista → médico general) | Plan de retorno documentado |
| 5 | QR en órdenes y recetas | 0 papel |
| 6 | Dashboards por perfil (enfermera, admin, especialista) | Satisfacción > 4/5 |
| 7 | Parametrización avanzada (flujos, variables clínicas) | Sin necesidad de programación |
| 8 | **Variables clínicas por especialidad** (campos específicos) | Configurable por especialidad |
| 9 | **Portal multi-tenant** (administradores por institución) | Cada institución gestiona su propio personal |

### Largo plazo (Fase 3 - 6 semanas) - IA y Diferenciadores

| # | Objetivo | Métrica de éxito |
|---|----------|------------------|
| 1 | Modelos predictivos (ausentismo, demanda) | Precisión > 80% |
| 2 | Detección de riesgos (enfermedades crónicas) | Sensibilidad > 85% |
| 3 | API de IA para sugerencia diagnóstica (prompt configurable) | Uso > 50% consultas |
| 4 | FastAPI separado para microservicio IA | Latencia < 500ms |
| 5 | Portal del paciente | 40% pacientes activos |
| 6 | Dashboard epidemiológico (alertas de brotes) | Alertas < 1 hora |
| 7 | Parametrización total (todas las tablas vía UI) | Configuración 100% sin código |
| 8 | **Clasificaciones especializadas** (CIE-O para oncología, CIF para rehabilitación) | Activación por especialidad |
| 9 | **Superadministrador global** | Gestión de múltiples tenants desde un panel |

### 🔮 Visión a futuro (Fase 4+ - Tercer Nivel)

| # | Objetivo (Futuro) | Estimación |
|---|-------------------|-------------|
| 1 | Gestión de hospitalización (ingreso, egreso, camas) | 6-8 semanas |
| 2 | Block quirúrgico (programación de cirugías, equipos) | 8-10 semanas |
| 3 | Evoluciones diarias en hospitalización | 4 semanas |
| 4 | Integración con laboratorio clínico e imágenes | 8-10 semanas |
| 5 | Gestión de UCI con monitoreo de signos vitales | 6-8 semanas |
| 6 | Facturación por día cama y procedimientos (privado) | 6 semanas |

---

## 10. CAPACIDADES CLAVE DEL SISTEMA

| Capacidad | Descripción | Nivel | Prioridad | Estado |
|-----------|-------------|-------|-----------|--------|
| **Multi-tenant** | Múltiples instituciones en una sola instalación, datos aislados | Infraestructura | P0 | ✅ |
| **Parametrización completa** | Configurar institución, especialidades, perfiles, horarios, flujos, variables clínicas sin programar | Todos | P0 | ✅ |
| **Selección de especialidad al registrar médico** | Al crear un médico, se asigna especialidad que determina su nivel, agenda y flujo | Administración | P0 | ✅ |
| **Flujo guiado (wizard)** | Médico sigue pasos secuenciales, sistema avanza automáticamente | Todos | P0 | ✅ |
| **Variables clínicas por especialidad** | Campos específicos según especialidad (ej: fracción eyección para cardiología) | 2do nivel | P0 | ✅ |
| **Agendamiento dual** | Específico (fijo) + Flexible (rango con asignación automática) | Todos | P0 | ✅ |
| **Referencia/Contrarreferencia** | 1er nivel → 2do nivel → retorno con plan | Integración | P1 | ✅ |
| **IA - Visión artificial** | Validación de documentos de identidad | Admisión | P1 | ✅ |
| **IA - Sugerencia diagnóstica** | API configurable con prompt anonimizado | Consulta | P2 | ✅ |
| **IA - Modelos predictivos** | Ausentismo, demanda, riesgo de enfermedades crónicas | Analítica | P2 | ✅ |
| **Dashboards por perfil** | Médico, enfermera, recepción, admin, especialista, superadmin | Todos | P1 | ✅ |
| **QR en órdenes/recetas** | Check-in, exámenes, farmacia sin papel | Servicios | P1 | ✅ |
| **Recordatorios** | Citas y medicamentos por correo (inicial) | Notificaciones | P1 | ✅ |
| **Auditoría completa** | Registro de todos los cambios en datos clínicos | Seguridad | P0 | ✅ |
| **Historia por episodio** | Trazabilidad de cada problema de salud | HCE | P0 | ✅ |
| **Clasificaciones OMS múltiples** | CIE-10 (todas), CIE-O (oncología), CIF (rehabilitación), ICHI (cirugía) | Especialidades | P2 | 🔮 Futuro |

---

## 11. MÉTRICAS DE ÉXITO

### Métricas clínicas

| Métrica | Objetivo | Frecuencia |
|---------|----------|------------|
| Tiempo cita → consulta (1er nivel) | < 30 minutos | Diaria |
| Tiempo referencia → especialista (2do nivel) | < 7 días | Semanal |
| Ausentismo a citas | Reducir del 25% al 10% | Semanal |
| Adherencia a medicamentos (recordatorios) | Aumentar del 50% al 75% | Mensual |
| Satisfacción médico (1-5) | > 4.2 | Trimestral |

### Métricas de sistema

| Métrica | Objetivo | Frecuencia |
|---------|----------|------------|
| Tiempo de registro paciente | < 2 minutos | Diaria |
| Precisión validación IA | > 95% | Semanal |
| Precisión modelos predictivos | > 80% | Mensual |
| Disponibilidad | 99.5% | Mensual |
| Tiempo de respuesta API | < 500ms | Diaria |
| **Aislamiento multi-tenant** | 0 fugas de datos entre instituciones | Continua |

### Métricas de parametrización

| Métrica | Objetivo |
|---------|----------|
| Tiempo de configuración nueva clínica (tenant) | < 2 días |
| Porcentaje de parámetros configurables vía UI | 100% (Fase 3) |
| Cambios sin reinicio del sistema | 100% |
| **Tiempo de asignación de especialidad a médico** | < 1 minuto |
| **Tiempo de aprovisionamiento de nuevo tenant** | < 5 minutos |

---

## 12. POSICIONAMIENTO ESTRATÉGICO

| Atributo | XMedical | Sistemas tradicionales |
|----------|----------|------------------------|
| **Multi-tenant** | ✅ Soporte nativo, datos aislados por institución | ❌ Una instalación por cliente |
| **Especialidades médicas** | Parametrizables, con asignación al registrar médico | Fijas, requieren código |
| **Variables clínicas** | Por especialidad, configurables vía UI | Genéricas o fijas |
| **Niveles de atención** | 1er y 2do nivel integrados (3er nivel futuro) | Solo uno u otro |
| **Flujo de atención** | Guiado paso a paso (wizard) | Formularios sueltos |
| **Agendamiento** | Específico + Flexible | Solo específico |
| **IA** | Visión + Predictiva + Generativa | Ninguna o básica |
| **Referencia/contrarreferencia** | Automática, trazable | Manual, sin integración |
| **Curva de aprendizaje** | 1-2 días (interfaz guiada) | 1-2 semanas |
| **Tecnología** | Open source (Django, DaisyUI) | Propietario, costoso |
| **Despliegue** | On-premise o nube | Generalmente on-premise |
| **Costo** | Bajo/mediano | Alto |
| **Público/Privado** | Ambos, con parámetros | Uno u otro |
| **Modelo de negocio** | SaaS o licencia perpetua | Generalmente licencia perpetua |

**Declaración de posicionamiento:**

> *"XMedical es el sistema de gestión clínica multi-tenant que combina una interfaz guiada paso a paso con parametrización completa para adaptarse a clínicas públicas o privadas, integrando primer y segundo nivel de atención con IA práctica y agendamiento flexible, permitiendo **asignar especialidades a cada médico** para personalizar su experiencia, y soportando **múltiples instituciones en una sola instalación** con completo aislamiento de datos, con visión de expansión a entornos hospitalarios (tercer nivel) en fases posteriores."*

---

## 13. CONCEPTOS CLAVE DEL DOMINIO (38 términos)

| # | Término | Definición | Nivel |
|---|---------|-------------|-------|
| 1 | **Primer nivel** | Atención primaria, medicina general, primer contacto del paciente | 1er |
| 2 | **Segundo nivel** | Atención especializada (cardiología, endocrinología, etc.) | 2do |
| 3 | 🔮 **Tercer nivel** | Atención hospitalaria, internación, cirugía, UCI (futuro) | 3er |
| 4 | **Especialidad médica** | Rama de la medicina que se enfoca en un área específica | Todos |
| 5 | **Subespecialidad** | Área más específica dentro de una especialidad | 2do |
| 6 | **Referencia** | Derivación desde 1er nivel a 2do nivel | 1er→2do |
| 7 | **Contrarreferencia** | Retorno desde 2do nivel a 1er nivel con plan de seguimiento | 2do→1er |
| 8 | **Episodio** | Periodo continuo de atención para un problema de salud específico | Todos |
| 9 | **Encuentro** | Cada interacción paciente-sistema (cita, preclínica, consulta) | Todos |
| 10 | **Parametrización** | Capacidad de configurar el sistema sin programación | Todos |
| 11 | **Flujo guiado (Wizard)** | Interfaz que guía al usuario paso a paso en un proceso | Todos |
| 12 | **Agendamiento específico** | Cita con fecha y hora exacta | 1er/2do |
| 13 | **Agendamiento flexible** | Rango de fechas con asignación automática | 1er/2do |
| 14 | **Preclínica** | Registro de signos vitales por enfermería | 1er/2do |
| 15 | **Consulta médica** | Atención por médico (general o especialista) | 1er/2do |
| 16 | **CIE-10/CIE-11** | Clasificación internacional de enfermedades | Todos |
| 17 | **Variable clínica** | Campo configurable por especialidad | Todos |
| 18 | **Plan terapéutico** | Indicaciones, medicamentos, exámenes, conducta | Todos |
| 19 | **Cita subsiguiente** | Nueva cita generada al finalizar una consulta | 1er/2do |
| 20 | **Servicio auxiliar** | Exámenes, farmacia, procedimientos | Todos |
| 21 | **Historia Clínica (HCE)** | Registro longitudinal de episodios y encuentros | Todos |
| 22 | **Prompt IA** | Texto configurable enviado a API para sugerencias | Todos |
| 23 | **Validación documental** | Verificación de identidad con visión artificial | Admisión |
| 24 | **Perfil (rol)** | Conjunto de permisos (médico, especialista, enfermera, etc.) | Todos |
| 25 | **Dashboard** | Pantalla de indicadores por tipo de usuario | Todos |
| 26 | **Triaje** | Clasificación inicial de prioridad | 1er/2do |
| 27 | **Interconsulta** | Solicitud de opinión entre especialistas | 2do/3er |
| 28 | **Teleconsulta** | Atención remota (futuro) | Todos |
| 29 | **SNOMED CT** | Terminología clínica estandarizada (opcional) | Todos |
| 30 | **HL7/FHIR** | Estándar de interoperabilidad (futuro) | Todos |
| 31 | **Auditoría** | Registro de todos los cambios en datos sensibles | Todos |
| 32 | **Código QR** | Identificador para check-in, órdenes, recetas | Todos |
| 33 | **Modelo predictivo** | Algoritmo IA que predice ausentismo, demanda o riesgo | Todos |
| 34 | 🔮 **CIE-O** | Clasificación para tumores (oncología) - futuro | 2do/3er |
| 35 | 🔮 **CIF** | Clasificación de funcionalidad (rehabilitación) - futuro | 2do/3er |
| 36 | **Multi-tenant** | Arquitectura donde múltiples clientes comparten la misma instalación | Infraestructura |
| 37 | **Tenant** | Cada institución/cliente dentro del sistema multi-tenant | Infraestructura |
| 38 | **Superadministrador** | Usuario con capacidad de gestionar múltiples tenants | Global |

---

## 14. TECNOLOGÍAS CONFIRMADAS

| Capa | Tecnología | Justificación |
|------|------------|----------------|
| **Frontend** | Django templates + DaisyUI + Tailwind | Interfaz guiada, componentes accesibles, temas configurables |
| **Backend** | Django (unificado inicialmente) | ORM potente, admin, auth, seguridad probada |
| **Base de Datos** | PostgreSQL con **RLS (Row Level Security)** | Aislamiento multi-tenant nativo, robustez, índices |
| **IA - Visión** | API externa (Google/AWS/Tesseract) | Validación de documentos |
| **IA - Sugerencia** | API configurable (OpenAI/Local LLM) | Prompt anonimizado |
| **IA - Modelos** | scikit-learn, XGBoost | Predictivos, detección riesgos |
| **Tareas programadas** | Celery + Redis (por tenant) | Recordatorios, backups |
| **Dashboard** | Django + Chart.js / Plotly | Gráficos integrados |
| **QR** | Python segno | Generación nativa |
| **Correos** | SMTP / SendGrid | Recordatorios |
| **FastAPI** | Post-MVP (separado) | Microservicio para IA pesada |

---

## 15. TIPOS DE INSTITUCIÓN SOPORTADOS

| Característica | Clínica Privada | Institución Pública | Hospital (Futuro) |
|----------------|-----------------|---------------------|-------------------|
| Facturación | Integrable (opcional) | No aplica | Por día cama + procedimientos |
| Reportes | Financieros + clínicos | Epidemiológicos + gestión | Ocupación + quirófanos |
| Portal paciente | Con acceso a resultados | Básico (citas) | + Visión de hospitalización |
| Precios en servicios | Configurables | No aplica | Configurables por cama |
| Integración fiscal | SII, facturación electrónica | No aplica | SII, facturación |
| Múltiples sedes | Sí (como tenants separados) | Sí | Sí |
| Tiempo de espera público | No aplica | KPIs de gestión | Lista de espera quirúrgica |
| Auditoría | Estándar | Reforzada | Estándar + UCI |

---

## 16. HOJA DE RUTA DE EVOLUCIÓN

| Fase | Duración | Entregable principal | Parametrización alcanzada | Niveles |
|------|----------|----------------------|---------------------------|---------|
| **Fase 1 (MVP)** | 4 semanas | Citas específicas + flujo guiado + **especialidades médicas** + **multi-tenant básico** + parametrización básica | Especialidades, profesionales, horarios, asignación de especialidad | 1er nivel |
| **Fase 2** | 4 semanas | Agendamiento flexible + IA visión + QR + referencias + **variables clínicas por especialidad** | Flujos, variables clínicas por especialidad | 1er + 2do nivel |
| **Fase 3** | 6 semanas | Modelos predictivos + detección riesgos + portal paciente + **superadministrador global** | IA (umbrales, prompts) | 1er + 2do nivel |
| **Fase 4** | 4 semanas | FastAPI separado + dashboard epidemiológico | 100% de parámetros vía UI | 1er + 2do nivel |
| 🔮 **Fase 5** | 8-10 semanas | **Tercer nivel básico**: Camas, ingreso/egreso hospitalario | Camas, servicios hospitalarios | +3er nivel (básico) |
| 🔮 **Fase 6** | 10-12 semanas | **Tercer nivel avanzado**: Block quirúrgico, UCI, evolución | Quirófanos, pabellones | +3er nivel (completo) |
| 🔮 **Fase 7+** | Continuo | Teleconsulta, app móvil, HL7/FHIR, **clasificaciones OMS especializadas** | Interoperabilidad, CIE-O, CIF | Todos |

---

## 17. RIESGOS Y MITIGACIONES

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|-------------|
| Adopción baja por médicos | Media | Alto | UI guiada, capacitación corta, gamificación |
| Parametrización insuficiente | Baja | Alto | Diseño modular desde MVP |
| Diferencia público/privado no cubierta | Media | Medio | Parámetros específicos por tipo |
| Precisión IA insuficiente | Media | Alto | Feedback humano para reentrenamiento |
| **Fuga de datos entre tenants** | Baja | **Crítico** | RLS en PostgreSQL + pruebas de aislamiento + auditoría continua |
| Performance con 1000 pacientes/día por tenant | Baja | Medio | Índices DB, caching, escalado horizontal |
| **Médicos sin especialidad asignada** | Baja | Medio | Validación al crear usuario (campo obligatorio) |
| **Complejidad de gestión multi-tenant** | Media | Medio | Panel de superadministrador, documentación |
| **Onboarding de nuevos tenants** | Media | Bajo | Proceso automatizado con script de creación |

---

## 18. APROBACIÓN

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Product Owner | [Usuario] | ✅ Aprobado | 2026 |
| Agente Documentación | DeepSeek | Generado | 2026 |

---

**Fin del Documento 1: Visión del Producto (Actualizado con Multi-tenant)**

---

## RESUMEN DE CAMBIOS REALIZADOS

| # | Cambio | Ubicación |
|---|--------|-----------|
| 1 | **Título actualizado**: incluye "Multi-tenant" | Encabezado |
| 2 | **Propósito**: añade multi-tenant y SaaS | Sección 1 |
| 3 | **Problemas**: nuevo problema #8 (múltiples clínicas) | Sección 2 |
| 4 | **Propuesta de valor**: nuevo segmento "Grupos de salud" y "Superadministrador" | Sección 3 |
| 5 | **Registro médico**: añade selección de institución | Sección 4 |
| 6 | **Flujo entre niveles**: añade nota de multi-tenant | Sección 5 |
| 7 | **Parametrización**: aclara "por institución" | Sección 6 |
| 8 | **Nueva Sección 7**: Arquitectura Multi-tenant (completa, 6 subsecciones) | Sección 7 |
| 9 | **Flujo médico**: añade identificación de institución | Sección 8 |
| 10 | **Objetivos**: nuevos objetivos multi-tenant | Sección 9 |
| 11 | **Capacidades clave**: nueva fila "Multi-tenant" | Sección 10 |
| 12 | **Métricas**: nueva métrica "Aislamiento multi-tenant" | Sección 11 |
| 13 | **Posicionamiento**: nuevo atributo "Multi-tenant" | Sección 12 |
| 14 | **Conceptos clave**: +3 términos (multi-tenant, tenant, superadministrador) | Sección 13 |
| 15 | **Tecnologías**: añade PostgreSQL RLS | Sección 14 |
| 16 | **Hoja de ruta**: actualizada con hitos multi-tenant | Sección 16 |
| 17 | **Riesgos**: nuevo riesgo "Fuga de datos entre tenants" | Sección 17 |

---