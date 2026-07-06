# DOCUMENTO 12: SPRINT BACKLOG
## XMedical - Sistema de Gestión Clínica Multi-tenant para Primer y Segundo Nivel

| Versión | Fecha | Autor | Estado |
|---------|-------|-------|--------|
| 1.0 | 2026 | Agente de Documentación Técnica | **Aprobado** |

---

## 1. VISIÓN GENERAL

Este documento define el **Sprint Backlog** para la **Fase 1 (MVP - 4 semanas)** de XMedical, incluyendo:

- **Historias de usuario priorizadas** (P0)
- **Estimación con Story Points** (escala Fibonacci modificada: 1, 2, 3, 5, 8, 13)
- **Planificación por día/semana**
- **Capacidad del equipo**
- **Definición de "Hecho" (Definition of Done)**
- **Burndown chart esperado**

---

## 2. CAPACIDAD DEL EQUIPO

### 2.1 Equipo de desarrollo (recomendado para MVP)

| Rol | Cantidad | Dedicación | Horas/semana | Total horas/sprint |
|-----|----------|------------|--------------|-------------------|
| **Tech Lead / FullStack** | 1 | 100% | 40 | 40 |
| **Backend Developer** | 1 | 100% | 40 | 40 |
| **Frontend Developer** | 1 | 100% | 40 | 40 |
| **QA Engineer** | 1 | 50% | 20 | 20 |
| **DevOps** | 1 | 25% | 10 | 10 |
| **Product Owner** | 1 | 25% | 10 | 10 |
| **Total** | **6** | - | **160** | **160** |

### 2.2 Capacidad ajustada por sprint (4 semanas = 160 horas)

| Concepto | Horas | Porcentaje |
|----------|-------|------------|
| Capacidad bruta | 160 | 100% |
| Reuniones (daily, planning, review) | -16 | -10% |
| Documentación | -16 | -10% |
| Bugs imprevistos | -16 | -10% |
| **Capacidad neta para desarrollo** | **112** | **70%** |

### 2.3 Story Points por hora

| Estimación | Story Points | Horas equivalentes |
|------------|--------------|---------------------|
| 1 SP | 1-2 horas | Tarea muy pequeña |
| 2 SP | 3-4 horas | Tarea pequeña |
| 3 SP | 5-6 horas | Tarea mediana |
| 5 SP | 7-10 horas | Tarea grande |
| 8 SP | 11-16 horas | Tarea muy grande |
| 13 SP | 17-24 horas | Épica pequeña |

**Capacidad en SP:** 112 horas / 5 horas por SP ≈ **22-25 SP por sprint**

---

## 3. HISTORIAS DE USUARIO PRIORIZADAS (P0 - MVP)

### 3.1 Épica: Administración Multi-tenant (ADM)

| ID | Historia | SP | Dependencias |
|----|----------|-----|--------------|
| HU-ADM-001 | Crear nueva institución (tenant) | 3 | Ninguna |
| HU-ADM-002 | Listar y gestionar instituciones | 2 | HU-ADM-001 |
| HU-SEG-001 | Autenticación de usuarios | 2 | HU-ADM-001 |
| HU-SEG-002 | Control de acceso por roles | 3 | HU-SEG-001 |

### 3.2 Épica: Gestión de Tenant (TEN)

| ID | Historia | SP | Dependencias |
|----|----------|-----|--------------|
| HU-TEN-001 | Configurar institución (perfil) | 2 | HU-ADM-001 |
| HU-TEN-002 | Gestionar especialidades | 3 | HU-ADM-001 |
| HU-TEN-003 | Registrar médico con especialidad | 3 | HU-TEN-002 |
| HU-TEN-004 | Configurar horarios por médico | 3 | HU-TEN-003 |

### 3.3 Épica: Gestión de Pacientes (PAC)

| ID | Historia | SP | Dependencias |
|----|----------|-----|--------------|
| HU-PAC-001 | Registrar paciente presencial | 2 | HU-ADM-001 |
| HU-PAC-002 | Buscar paciente | 2 | HU-PAC-001 |

### 3.4 Épica: Agendamiento de Citas (CIT)

| ID | Historia | SP | Dependencias |
|----|----------|-----|--------------|
| HU-CIT-001 | Agendar cita específica | 3 | HU-TEN-003, HU-PAC-001 |
| HU-CIT-002 | Cancelar cita | 2 | HU-CIT-001 |

### 3.5 Épica: Preclínica (PRE)

| ID | Historia | SP | Dependencias |
|----|----------|-----|--------------|
| HU-PRE-001 | Registrar signos vitales | 3 | HU-CIT-001 |
| HU-PRE-002 | Registrar motivo de consulta | 2 | HU-PRE-001 |

### 3.6 Épica: Consulta Médica (CON)

| ID | Historia | SP | Dependencias |
|----|----------|-----|--------------|
| HU-CON-001 | Flujo guiado de consulta (7 pasos) | 5 | HU-PRE-001 |
| HU-CON-002 | Registrar diagnóstico CIE-10 | 3 | HU-CON-001 |
| HU-CON-003 | Registrar plan terapéutico | 3 | HU-CON-001 |
| HU-CON-004 | Ver historia clínica | 2 | HU-CON-001 |

### 3.7 Épica: Seguridad (SEG)

| ID | Historia | SP | Dependencias |
|----|----------|-----|--------------|
| HU-SEG-003 | Auditoría de cambios | 3 | HU-CON-001 |

---

## 4. RESUMEN DE SP POR ÉPICA (MVP - P0)

| Épica | SP total | % del sprint |
|-------|----------|--------------|
| ADM - Administración Multi-tenant | 10 | 20% |
| TEN - Gestión de Tenant | 11 | 22% |
| PAC - Gestión de Pacientes | 4 | 8% |
| CIT - Agendamiento de Citas | 5 | 10% |
| PRE - Preclínica | 5 | 10% |
| CON - Consulta Médica | 13 | 26% |
| SEG - Seguridad | 3 | 6% |
| **TOTAL P0** | **51** | **102%** |

**Nota:** El total de 51 SP excede la capacidad de 22-25 SP por sprint. Por lo tanto, se priorizan las historias más críticas para el MVP.

---

## 5. SPRINT BACKLOG PRIORIZADO (TOP 25 SP)

| Prioridad | ID | Historia | SP | Épica | Día estimado |
|-----------|-----|----------|-----|-------|--------------|
| 1 | HU-ADM-001 | Crear nueva institución | 3 | ADM | Día 1-2 |
| 2 | HU-ADM-002 | Listar y gestionar instituciones | 2 | ADM | Día 2-3 |
| 3 | HU-SEG-001 | Autenticación de usuarios | 2 | SEG | Día 3-4 |
| 4 | HU-SEG-002 | Control de acceso por roles | 3 | SEG | Día 4-5 |
| 5 | HU-TEN-001 | Configurar institución | 2 | TEN | Día 5-6 |
| 6 | HU-TEN-002 | Gestionar especialidades | 3 | TEN | Día 6-8 |
| 7 | HU-TEN-003 | Registrar médico con especialidad | 3 | TEN | Día 8-10 |
| 8 | HU-PAC-001 | Registrar paciente | 2 | PAC | Día 10-11 |
| 9 | HU-CIT-001 | Agendar cita específica | 3 | CIT | Día 11-13 |
| 10 | HU-PRE-001 | Registrar signos vitales | 3 | PRE | Día 13-15 |
| 11 | HU-CON-001 | Flujo guiado consulta (7 pasos) | 5 | CON | Día 15-18 |
| 12 | HU-CON-002 | Registrar diagnóstico CIE-10 | 3 | CON | Día 18-20 |
| 13 | HU-CON-003 | Registrar plan terapéutico | 3 | CON | Día 20-22 |
| **TOTAL** | | | **37 SP** | | **22 días** |

**Nota:** 37 SP para 22 días hábiles = 1.68 SP/día (considerando capacidad neta)

---

## 6. PLANIFICACIÓN DETALLADA POR DÍA

### Semana 1 (Días 1-5) - Configuración base

| Día | Tareas | SP | Entregable |
|-----|--------|-----|------------|
| **Día 1** | HU-ADM-001 (Setup proyecto, modelo Institución) | 1.5 | Estructura Django lista |
| **Día 2** | HU-ADM-001 (CRUD instituciones) + HU-ADM-002 | 1.5 | CRUD instituciones funcionando |
| **Día 3** | HU-SEG-001 (Login, logout, sesiones) | 2 | Autenticación funcionando |
| **Día 4** | HU-SEG-002 (Modelos de roles, permisos básicos) | 1.5 | RBAC básico |
| **Día 5** | HU-SEG-002 (Middleware de autorización) + HU-TEN-001 | 1.5 | Control de acceso por rol |

### Semana 2 (Días 6-10) - Configuración y pacientes

| Día | Tareas | SP | Entregable |
|-----|--------|-----|------------|
| **Día 6** | HU-TEN-002 (Modelo Especialidad, CRUD) | 1.5 | Especialidades configurables |
| **Día 7** | HU-TEN-002 (Vistas admin especialidades) | 1.5 | UI especialidades |
| **Día 8** | HU-TEN-003 (Modelo Profesional, FK a Especialidad) | 1.5 | Médicos con especialidad |
| **Día 9** | HU-TEN-003 (Vistas admin profesionales) + HU-TEN-004 | 1.5 | Horarios configurables |
| **Día 10** | HU-PAC-001 (Modelo Paciente + CRUD básico) | 2 | Registro pacientes |

### Semana 3 (Días 11-15) - Agendamiento y preclínica

| Día | Tareas | SP | Entregable |
|-----|--------|-----|------------|
| **Día 11** | HU-CIT-001 (Modelo Cita, lógica disponibilidad) | 1.5 | Estructura citas |
| **Día 12** | HU-CIT-001 (Vista agendamiento, bloqueo de turnos) | 1.5 | Agendamiento funcionando |
| **Día 13** | HU-CIT-002 (Cancelación de citas) + HU-PRE-001 | 1.5 | Cancelación + estructura preclínica |
| **Día 14** | HU-PRE-001 (Formulario signos vitales) | 1.5 | UI preclínica |
| **Día 15** | HU-PRE-002 (Motivo consulta, triaje) + HU-CON-001 inicio | 1.5 | Preclínica completa |

### Semana 4 (Días 16-20) - Consulta médica

| Día | Tareas | SP | Entregable |
|-----|--------|-----|------------|
| **Día 16** | HU-CON-001 (Flujo 7 pasos - estructura wizard) | 1.5 | Wizard base |
| **Día 17** | HU-CON-001 (Pasos 1-3: preclínica, motivo, anamnesis) | 1.5 | Pasos implementados |
| **Día 18** | HU-CON-001 (Pasos 4-6: examen físico, diagnóstico, plan) | 1.5 | Pasos implementados |
| **Día 19** | HU-CON-002 (Buscador CIE-10) + HU-CON-003 (Plan) | 1.5 | Diagnóstico y plan |
| **Día 20** | HU-CON-004 (Historia clínica) + HU-SEG-003 (Auditoría) | 1.5 | HCE y auditoría |

### Semana 5 (Días 21-22) - Pruebas y ajustes

| Día | Tareas | SP | Entregable |
|-----|--------|-----|------------|
| **Día 21** | Pruebas de integración, corrección de bugs | 1.5 | Tests pasando |
| **Día 22** | Deploy a staging, smoke tests, documentación | 1.5 | MVP listo |

---

## 7. DEFINICIÓN DE "HECHO" (DEFINITION OF DONE)

| Criterio | Descripción | Responsable |
|----------|-------------|-------------|
| **Código** | Código escrito, revisado y mergeado a develop | Desarrollador |
| **Pruebas unitarias** | Tests escritos y pasando (cobertura > 80% en nueva funcionalidad) | Desarrollador |
| **Pruebas de integración** | Tests de integración pasando | Desarrollador |
| **Code review** | Aprobado por al menos otro desarrollador | Tech Lead |
| **Documentación** | Docstrings, README actualizado, comentarios en código complejo | Desarrollador |
| **UI/UX** | Interfaz funcional y responsive | Frontend |
| **QA** | Validado por QA (pruebas manuales) | QA Engineer |
| **Product Owner** | Aprobado por PO | Product Owner |
| **Sin bugs críticos** | No hay bugs que bloqueen la funcionalidad | QA |
| **Desplegable** | Código puede ser desplegado a staging | DevOps |

---

## 8. BURNDOWN CHART ESPERADO

```
SP
40│
   │
35│  ● (Día 0: 37 SP)
   │  ●
30│     ●
   │        ●
25│           ●
   │              ●
20│                 ●
   │                    ●
15│                       ●
   │                          ●
10│                             ●
   │                                ●
 5│                                   ● (Día 22: 0 SP)
   │
 0└──────────────────────────────────────────► Días
   0  2  4  6  8 10 12 14 16 18 20 22 24
   
   ● = Progreso ideal
   ○ = Progreso real esperado (con desviaciones)
```

### Datos del burndown

| Día | SP restantes (ideal) | SP restantes (real esperado) | Nota |
|-----|---------------------|------------------------------|------|
| 0 | 37 | 37 | Inicio del sprint |
| 2 | 34 | 35 | Ajuste inicial |
| 4 | 31 | 32 | |
| 6 | 28 | 29 | |
| 8 | 25 | 26 | |
| 10 | 22 | 23 | |
| 12 | 19 | 20 | |
| 14 | 16 | 17 | |
| 16 | 13 | 14 | |
| 18 | 10 | 11 | |
| 20 | 7 | 8 | |
| 22 | 4 | 5 | |
| 22 (fin) | 0 | 0 | Sprint completado |

---

## 9. RIESGOS Y MITIGACIONES DEL SPRINT

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|-------------|
| Médicos rechazan flujo guiado | Media | Alto | UI simple, botones grandes, pruebas tempranas |
| Tiempos de carga con datos reales | Baja | Medio | Índices DB, caching desde inicio |
| Doble reserva de citas | Baja | Crítico | `select_for_update()` en transacción |
| Pérdida de datos clínicos | Baja | Crítico | Backups diarios manuales |
| Parametrización insuficiente | Media | Medio | Reunión previa para mapear requerimientos |
| **Médicos sin especialidad asignada** | Baja | Medio | Validación al crear usuario (campo obligatorio) |

---

## 10. HITOS DEL SPRINT

| Hito | Día | Criterio |
|------|-----|----------|
| **Setup completado** | Día 2 | Proyecto corriendo, BD configurada |
| **Autenticación funcionando** | Día 5 | Login/logout con roles |
| **Configuración base lista** | Día 10 | Especialidades, médicos, horarios |
| **Agendamiento funcionando** | Día 12 | Citas se pueden agendar |
| **Preclínica funcionando** | Día 15 | Signos vitales registrados |
| **Consulta médica funcionando** | Día 19 | Flujo de 7 pasos completo |
| **MVP completado** | Día 22 | Todas las historias P0 entregadas |

---

## 11. ENTREGABLES DEL SPRINT

### 11.1 Entregables técnicos

| # | Entregable | Formato |
|---|------------|---------|
| 1 | Código fuente Django completo | Repositorio Git |
| 2 | Scripts de base de datos (DDL + datos iniciales) | SQL |
| 3 | Manual de usuario (4 perfiles + flujo guiado) | PDF/Markdown |
| 4 | Manual de instalación y configuración | PDF/Markdown |
| 5 | Suite de pruebas unitarias (pytest, cobertura > 70%) | Código Python |
| 6 | Documentación de API básica | Swagger/OpenAPI |
| 7 | Scripts de backup/restore manual | Bash |
| 8 | Prototipo interactivo del flujo guiado | HTML/JS |

### 11.2 Entregables funcionales

| # | Funcionalidad | Estado |
|---|---------------|--------|
| 1 | Registro de pacientes | ✅ |
| 2 | Agendamiento específico | ✅ |
| 3 | Preclínica (signos vitales, motivo, triaje) | ✅ |
| 4 | Consulta médica (flujo 7 pasos) | ✅ |
| 5 | Diagnóstico CIE-10 | ✅ |
| 6 | Plan terapéutico | ✅ |
| 7 | Historia clínica | ✅ |
| 8 | Autenticación y roles | ✅ |
| 9 | Multi-tenant básico | ✅ |

---

## 12. APROBACIÓN

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Product Owner | [Usuario] | ✅ Aprobado | 2026 |
| Scrum Master | [Usuario] | ✅ Aprobado | 2026 |
| Tech Lead | [Usuario] | ✅ Aprobado | 2026 |
| Agente Documentación | DeepSeek | Generado | 2026 |

---

**Fin del Documento 12: Sprint Backlog**

---

## RESUMEN DEL DOCUMENTO

| Aspecto | Valor |
|---------|-------|
| **Duración del sprint** | 4 semanas (22 días hábiles) |
| **Capacidad del equipo** | 160 horas brutas, 112 horas netas |
| **Total SP planificados** | 37 SP |
| **SP por día** | ~1.7 SP |
| **Historias P0 incluidas** | 13 |
| **Riesgos identificados** | 6 |
| **Hitos del sprint** | 7 |
| **Entregables** | 8 técnicos + 9 funcionales |

---

## DOCUMENTOS COMPLETADOS (1-12)

| # | Documento | Estado |
|---|-----------|--------|
| 0 | Descripción General | ✅ |
| 1 | Visión del Producto | ✅ |
| 2 | Alcance del MVP | ✅ |
| 3 | Historias de Usuario | ✅ |
| 4 | Arquitectura de Alto Nivel | ✅ |
| 5 | Diagramas de Flujo | ✅ |
| 6 | Modelo de Datos | ✅ |
| 7 | Seguridad | ✅ |
| 8 | Modelo de Negocio | ✅ |
| 9 | Integraciones | ✅ |
| 10 | Plan de Pruebas | ✅ |
| 11 | Plan de Despliegue | ✅ |
| 12 | Sprint Backlog | ✅ |
| 14 | Roadmap Seguridad | ✅ |

---

## 8. BACKLOG POST-MVP — SEGURIDAD

Items planificados tras el MVP. Detalle en [`14 Roadmap Seguridad.md`](14%20Roadmap%20Seguridad.md).

| ID | Historia / tarea | SP est. | Fase | Dependencias |
|----|------------------|---------|------|--------------|
| SEC-P01 | RBAC estricto por rol (mixins + tests SEC-13) | 5 | Fase 1 | HU-SEG-002 |
| SEC-P02 | Remediar CVE pip-audit | 2 | Fase 1 | — |
| SEC-P03 | Remediar bandit High | 2 | Fase 1 | — |
| SEC-P04 | Apache ServerTokens Prod | 1 | Fase 1 | — |
| SEC-P10 | Rate limiting API (SEC-06) | 3 | Fase 2 | API REST doc 13 |
| SEC-P11 | JWT + tests API-01..06 | 8 | Fase 2 | doc 13 |
| SEC-P20 | HSTS preload | 1 | Fase 3 | SEC-P04 |
| SEC-P21 | 2FA administradores | 5 | Fase 3 | django-otp |

**Completado 2026-07:** tests SEC-01..12, scripts verify_security_*, login_required en rutas expuestas.

---

**¡Documentación completa de XMedical generada exitosamente!**
