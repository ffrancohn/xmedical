# DOCUMENTO 3: HISTORIAS DE USUARIO
## XMedical - Sistema de Gestión Clínica Multi-tenant para Primer y Segundo Nivel

| Versión | Fecha | Autor | Estado |
|---------|-------|-------|--------|
| 1.0 | 2026 | Agente de Documentación Técnica | **Aprobado** |

---

## 1. INTRODUCCIÓN

Este documento contiene las **historias de usuario** para XMedical, organizadas por **épicas** (módulos funcionales). Cada historia incluye:

- **ID**: Identificador único (ej: HU-ADM-001)
- **Épica**: Módulo al que pertenece
- **Título**: Descripción corta
- **Descripción**: Formato "Como [rol], quiero [acción], para [beneficio]"
- **Criterios de aceptación**: Formato Given/When/Then
- **Prioridad**: P0 (MVP), P1 (Fase 2), P2 (Fase 3), 🔮 (Futuro)
- **Story Points**: Escala Fibonacci (1, 2, 3, 5, 8, 13)

---

## 2. ÉPICAS DEL PROYECTO

| Código | Épica | Descripción | Prioridad |
|--------|-------|-------------|-----------|
| **ADM** | Administración Multi-tenant | Gestión de instituciones, superadministrador, parametrización global | P0 |
| **TEN** | Gestión de Tenant (Institución) | Configuración de cada clínica: especialidades, profesionales, horarios | P0 |
| **PAC** | Gestión de Pacientes | Registro, búsqueda, validación de documentos | P0 |
| **CIT** | Agendamiento de Citas | Agendamiento específico, flexible, cancelaciones, QR | P0 |
| **PRE** | Preclínica y Enfermería | Signos vitales, triaje, flujo guiado | P0 |
| **CON** | Consulta Médica | Flujo guiado de 7 pasos, diagnóstico, plan terapéutico | P0 |
| **REF** | Referencia y Contrarreferencia | Derivación 1er nivel ↔ 2do nivel | P1 |
| **SER** | Servicios Auxiliares | Exámenes, farmacia, QR, recetas | P1 |
| **DASH** | Dashboards | Por perfil: médico, enfermera, admin, especialista, superadmin | P1 |
| **NOT** | Notificaciones | Recordatorios por correo (citas, medicamentos) | P1 |
| **IA** | Inteligencia Artificial | Visión, predictiva, generativa | P2 |
| **POR** | Portal del Paciente | Autogestión de citas, resultados, HCE portátil | P2 |
| **SEG** | Seguridad y Auditoría | Autenticación, roles, RLS, logs | P0 |
| 🔮 **HOS** | Hospitalización (Futuro) | Camas, ingreso/egreso, cirugías | 🔮 |
| 🔮 **OMS** | Clasificaciones OMS (Futuro) | CIE-O, CIF, ICHI | 🔮 |

---

## 3. HISTORIAS DE USUARIO POR ÉPICA

---

### ÉPICA ADM - ADMINISTRACIÓN MULTI-TENANT (P0)

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-ADM-001 | Crear nueva institución (tenant) | P0 | 3 |

**Descripción:** Como **superadministrador**, quiero **crear una nueva institución (tenant)** en el sistema, para **que una nueva clínica pueda comenzar a usar XMedical de forma aislada**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Soy superadministrador autenticado | Accedo al panel de creación de instituciones | Veo un formulario con: nombre, subdominio, tipo (pública/privada), contacto |
| 2 | Completo todos los campos obligatorios | Hago clic en "Crear institución" | El sistema crea la institución con un ID único y genera las tablas base (especialidades, roles) |
| 3 | Ingreso un subdominio ya existente | Intento crear la institución | El sistema rechaza la operación con mensaje "Subdominio ya registrado" |
| 4 | La institución es creada | Reviso la lista de instituciones | La nueva institución aparece en el listado con estado "Activa" |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-ADM-002 | Listar y gestionar instituciones | P0 | 2 |

**Descripción:** Como **superadministrador**, quiero **ver un listado de todas las instituciones registradas**, para **monitorear y gestionar los tenants del sistema**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Soy superadministrador autenticado | Accedo al panel de instituciones | Veo una tabla con: nombre, subdominio, tipo, fecha creación, estado |
| 2 | Hay más de 10 instituciones | La lista carga | Veo paginación para navegar |
| 3 | Selecciono una institución | Hago clic en "Editar" | Puedo modificar nombre, tipo, contacto, estado |
| 4 | Selecciono una institución | Hago clic en "Desactivar" | La institución queda como "Inactiva" y sus usuarios no pueden acceder |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-ADM-003 | Dashboard de superadministrador | P1 | 3 |

**Descripción:** Como **superadministrador**, quiero **ver un dashboard con métricas globales**, para **monitorear el uso del sistema por cada institución**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Soy superadministrador autenticado | Accedo al dashboard global | Veo tarjetas con: total de instituciones, total de pacientes, total de citas hoy |
| 2 | Quiero ver detalles por institución | Selecciono una institución del listado | Veo métricas específicas de ese tenant (pacientes, médicos, citas) |
| 3 | Quiero monitorear actividad reciente | Veo la sección "Actividad reciente" | Veo logs de acceso y operaciones importantes |

---

### ÉPICA TEN - GESTIÓN DE TENANT (INSTITUCIÓN) (P0)

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-TEN-001 | Configurar institución (perfil) | P0 | 2 |

**Descripción:** Como **administrador de la institución**, quiero **configurar los datos de mi clínica**, para **personalizar la apariencia y datos fiscales del sistema**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Soy administrador autenticado en mi institución | Accedo a "Configuración → Institución" | Veo un formulario con: nombre, logo, dirección, teléfono, email |
| 2 | Subo un logo (imagen) | Hago clic en "Guardar" | El logo se muestra en el header del sistema |
| 3 | Cambio el tipo de institución (pública/privada) | Guardo los cambios | Los reportes y opciones de facturación se ajustan según el tipo |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-TEN-002 | Gestionar especialidades de la institución | P0 | 3 |

**Descripción:** Como **administrador de la institución**, quiero **crear, editar y desactivar especialidades médicas**, para **que los médicos puedan ser asignados a ellas**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Soy administrador autenticado | Accedo a "Configuración → Especialidades" | Veo un listado de especialidades con: nombre, nivel (1er/2do), duración, estado |
| 2 | Hago clic en "Nueva especialidad" | Completo nombre, nivel, duración | La especialidad se guarda y está disponible para asignar a médicos |
| 3 | Intento eliminar una especialidad con médicos asignados | Hago clic en "Eliminar" | El sistema muestra advertencia y propone desactivar en lugar de eliminar |
| 4 | Desactivo una especialidad | Confirmo la acción | La especialidad ya no aparece en listados de agendamiento |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-TEN-003 | Registrar médico con especialidad obligatoria | P0 | 3 |

**Descripción:** Como **administrador de la institución**, quiero **registrar un médico y asignarle una especialidad obligatoria**, para **que el sistema pueda filtrar su agenda y consultas**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Soy administrador autenticado | Accedo a "Usuarios → Médicos → Nuevo médico" | Veo un formulario con campos: nombre, email, teléfono, especialidad (desplegable), registro médico |
| 2 | No selecciono ninguna especialidad | Intento guardar | El sistema muestra error "La especialidad es obligatoria" |
| 3 | Selecciono una especialidad de 1er nivel | Guardo el médico | El médico tiene nivel "Primer nivel" asignado automáticamente |
| 4 | Selecciono una especialidad de 2do nivel | Guardo el médico | El médico tiene nivel "Segundo nivel" y podrá recibir referencias |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-TEN-004 | Configurar horarios por médico | P0 | 3 |

**Descripción:** Como **administrador de la institución**, quiero **configurar los horarios de atención de cada médico**, para **que los pacientes puedan agendar citas solo en horarios disponibles**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Soy administrador autenticado | Accedo a "Horarios → Seleccionar médico" | Veo una vista semanal con bloques de tiempo |
| 2 | Arrastro para seleccionar un bloque horario | Configuro días y horas de atención | El horario se guarda y está disponible para agendamiento |
| 3 | Configuro un horario que se solapa con otro existente | Intento guardar | El sistema muestra advertencia de conflicto |
| 4 | Configuro un horario especial (ej: feriado) | Marco "No laborable" | El médico no aparece disponible ese día |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-TEN-005 | Gestionar perfiles y permisos | P1 | 3 |

**Descripción:** Como **administrador de la institución**, quiero **crear perfiles personalizados con permisos específicos**, para **controlar el acceso de diferentes tipos de usuarios**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Soy administrador autenticado | Accedo a "Configuración → Perfiles" | Veo una lista de perfiles (por defecto: Admin, Médico, Enfermera, Recepción) |
| 2 | Hago clic en "Nuevo perfil" | Asigno nombre y selecciono permisos (checkboxes) | El nuevo perfil se guarda |
| 3 | Asigno un perfil personalizado a un usuario | Selecciono el perfil en edición de usuario | El usuario tiene solo los permisos asignados |

---

### ÉPICA PAC - GESTIÓN DE PACIENTES (P0)

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-PAC-001 | Registrar paciente presencial | P0 | 2 |

**Descripción:** Como **recepcionista**, quiero **registrar un paciente en el sistema**, para **que pueda ser agendado y atendido**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Soy recepcionista autenticado | Accedo a "Registrar paciente" | Veo un formulario con: documento, nombres, apellidos, fecha nacimiento, sexo, teléfono, email |
| 2 | Completo todos los campos obligatorios | Hago clic en "Guardar" | El paciente queda registrado y recibe un ID único |
| 3 | Ingreso un documento ya existente | Intento guardar | El sistema muestra "Paciente ya registrado" y ofrece buscarlo |
| 4 | Registro el paciente | La operación se completa | El tiempo total de registro es < 2 minutos |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-PAC-002 | Buscar paciente | P0 | 2 |

**Descripción:** Como **recepcionista o médico**, quiero **buscar un paciente por documento o nombre**, para **acceder rápidamente a su historia clínica o agendar una cita**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Estoy en el módulo de agendamiento | Escribo parte del nombre del paciente | El sistema muestra resultados coincidentes en tiempo real |
| 2 | Escribo un número de documento completo | Presiono Enter | El sistema lleva directamente al perfil del paciente |
| 3 | El paciente pertenece a otra institución | Busco por documento | El sistema no lo encuentra (aislamiento por tenant) |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-PAC-003 | Registrar paciente en línea (auto-registro) | P0 | 2 |

**Descripción:** Como **paciente**, quiero **registrarme en el portal web**, para **poder agendar citas en línea sin necesidad de ir a la clínica**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Accedo al portal web de la clínica (subdominio específico) | Hago clic en "Registrarse" | Veo un formulario con campos básicos |
| 2 | Completo mis datos (incluyendo email válido) | Envío el formulario | Recibo un correo de confirmación con enlace para activar mi cuenta |
| 3 | Activo mi cuenta | Hago clic en el enlace del correo | Mi cuenta queda activa y puedo iniciar sesión |
| 4 | Intento registrarme con documento ya existente | Envío el formulario | El sistema detecta duplicado y me pide recuperar mi cuenta |

---

### ÉPICA CIT - AGENDAMIENTO DE CITAS (P0/P1)

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-CIT-001 | Agendar cita específica (fecha/hora fija) | P0 | 3 |

**Descripción:** Como **recepcionista o paciente en línea**, quiero **agendar una cita en una fecha y hora específica**, para **asegurar la atención con un médico determinado**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Estoy en el módulo de agendamiento | Selecciono especialidad → médico → fecha → hora | El sistema me muestra solo horarios disponibles |
| 2 | Selecciono un horario disponible | Confirmo la cita | El sistema bloquea el turno y no permite doble reserva |
| 3 | Intento agendar en un horario ya ocupado | Selecciono la hora | El sistema muestra "Horario no disponible" |
| 4 | La cita es agendada | Confirmo | El sistema guarda la cita con estado "Pendiente" |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-CIT-002 | Cancelar cita | P0 | 2 |

**Descripción:** Como **recepcionista o paciente**, quiero **cancelar una cita agendada**, para **liberar el cupo para otro paciente**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Tengo una cita agendada para dentro de 3 días | Accedo a "Mis citas" y selecciono "Cancelar" | El sistema libera el cupo y cambia estado a "Cancelada por paciente" |
| 2 | Intento cancelar una cita con menos de 2 horas de anticipación | Selecciono "Cancelar" | El sistema muestra advertencia y no libera el cupo |
| 3 | La cita es cancelada | Completo el proceso | El paciente recibe notificación por correo (si aplica) |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-CIT-003 | Agendar cita flexible (por rango) | P1 | 3 |

**Descripción:** Como **paciente**, quiero **solicitar una cita en un rango de fechas (ej: "próxima semana")**, para **que el sistema asigne automáticamente el primer turno disponible**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Estoy agendando una cita en línea | Selecciono especialidad y "Agendamiento flexible" | Veo opciones: "Mañana", "Esta semana", "Próxima semana" |
| 2 | Selecciono "Próxima semana" | Confirmo la solicitud | El sistema asigna el primer turno disponible en ese rango |
| 3 | No hay turnos disponibles en el rango solicitado | Confirmo la solicitud | El sistema muestra "No hay disponibilidad, seleccione otro rango" |

---

### ÉPICA PRE - PRECLÍNICA Y ENFERMERÍA (P0)

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-PRE-001 | Registrar signos vitales (flujo guiado) | P0 | 3 |

**Descripción:** Como **enfermera**, quiero **seguir un flujo guiado para registrar signos vitales del paciente**, para **asegurar que no se omitan datos importantes**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Soy enfermera autenticada | Selecciono un paciente en espera y "Comenzar preclínica" | El sistema muestra el primer paso del flujo (signos vitales) |
| 2 | Completo TA, FC, Temp, SatO2, peso, talla | Hago clic en "Siguiente" | El sistema calcula IMC automáticamente y muestra alertas si hay valores anormales |
| 3 | Registro TA = 150/95 | El sistema detecta hipertensión | Muestra alerta "Presión alta - informar al médico" |
| 4 | Completo todos los pasos obligatorios | Hago clic en "Enviar a consulta médica" | El paciente pasa a estado "En espera consulta" |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-PRE-002 | Registrar motivo de consulta inicial | P0 | 2 |

**Descripción:** Como **enfermera**, quiero **registrar el motivo de consulta del paciente**, para **que el médico tenga contexto antes de iniciar la consulta**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Estoy en el flujo de preclínica | Llego al paso "Motivo de consulta" | Veo un campo de texto para describir el motivo |
| 2 | Escribo el motivo | Hago clic en "Siguiente" | El motivo se guarda y estará visible para el médico |
| 3 | El paciente no puede comunicarse (ej: niño) | Escribo "Madre refiere..." | El campo acepta texto libre sin restricciones |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-PRE-003 | Realizar triaje (prioridad) | P0 | 2 |

**Descripción:** Como **enfermera**, quiero **clasificar al paciente por prioridad de atención**, para **que los casos más urgentes sean atendidos primero**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Estoy en el flujo de preclínica | Llego al paso "Triaje" | Veo opciones: Baja, Media, Alta |
| 2 | Selecciono "Alta" | Hago clic en "Siguiente" | El paciente aparece destacado en la lista del médico |
| 3 | Un paciente con triaje "Alta" está en espera | Otros pacientes tienen prioridad "Media" | El paciente con "Alta" aparece primero en la cola |

---

### ÉPICA CON - CONSULTA MÉDICA (P0)

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-CON-001 | Flujo guiado de consulta (7 pasos) | P0 | 5 |

**Descripción:** Como **médico**, quiero **seguir un flujo guiado de 7 pasos durante la consulta**, para **asegurar que registro todos los datos necesarios de forma ordenada**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Soy médico autenticado | Selecciono un paciente para atender | El sistema inicia el flujo en el Paso 1 (Revisar preclínica) |
| 2 | Veo el indicador de pasos | Avanzo al Paso 2 (Motivo) | El indicador muestra mi progreso (ej: "Paso 2 de 7") |
| 3 | Intento saltar un paso obligatorio | Hago clic en "Siguiente" sin completar | El sistema muestra error y me impide avanzar |
| 4 | Completo los 7 pasos | Llego al resumen final | Veo todos los datos ingresados antes de guardar |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-CON-002 | Registrar diagnóstico CIE-10 | P0 | 3 |

**Descripción:** Como **médico**, quiero **buscar y seleccionar un diagnóstico CIE-10**, para **estandarizar el registro de enfermedades**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Estoy en el paso 5 (Diagnóstico) | Escribo parte del diagnóstico en el buscador | El sistema muestra resultados coincidentes (código + nombre) |
| 2 | Selecciono un diagnóstico principal | Hago clic en el diagnóstico | El diagnóstico queda seleccionado como "Principal" |
| 3 | Necesito agregar diagnósticos secundarios | Hago clic en "+ Agregar" | Puedo seleccionar múltiples diagnósticos adicionales |
| 4 | No encuentro el diagnóstico en la búsqueda | Escribo el nombre completo | El sistema permite usar texto libre con advertencia "No estándar" |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-CON-003 | Registrar plan terapéutico | P0 | 3 |

**Descripción:** Como **médico**, quiero **registrar el plan terapéutico del paciente**, para **indicar la conducta a seguir (alta, cita subsiguiente o referencia)**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Estoy en el paso 6 (Plan) | Veo las opciones de conducta: Alta, Cita subsiguiente, Referencia | Selecciono una opción |
| 2 | Selecciono "Cita subsiguiente" | Ingreso el número de días | El sistema agenda automáticamente la cita al finalizar |
| 3 | Selecciono "Referencia a especialista" | Elijo la especialidad destino | El sistema crea una referencia pendiente |
| 4 | Agrego medicamentos o exámenes al plan | Hago clic en "+ Agregar" | Los items se añaden a la lista del plan |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-CON-004 | Ver historia clínica del paciente | P0 | 2 |

**Descripción:** Como **médico**, quiero **ver la historia clínica previa del paciente**, para **conocer sus antecedentes y consultas anteriores**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Estoy en la consulta de un paciente | Veo un botón "Historia Clínica" | Al hacer clic, veo todos los encuentros previos ordenados por fecha descendente |
| 2 | Selecciono una consulta anterior | Hago clic en "Ver detalles" | Veo diagnóstico, plan, medicamentos de esa consulta |
| 3 | El paciente tiene múltiples episodios | Navego por la historia | Veo separación por episodios (ej: "Diabetes - Episodio 1") |

---

### ÉPICA REF - REFERENCIA Y CONTRARREFERENCIA (P1)

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-REF-001 | Generar referencia a especialista | P1 | 3 |

**Descripción:** Como **médico de 1er nivel**, quiero **generar una referencia a un especialista**, para **derivar al paciente a atención de segundo nivel**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Estoy en el paso 6 (Plan) | Selecciono "Referencia a especialista" | Veo un desplegable con especialidades de 2do nivel disponibles en mi institución |
| 2 | Selecciono una especialidad | Agrego un comentario con el motivo de referencia | La referencia queda pendiente en la bandeja del especialista |
| 3 | El especialista acepta la referencia | El sistema notifica al paciente | Se agenda automáticamente una cita con el especialista |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-REF-002 | Ver bandeja de referencias entrantes | P1 | 2 |

**Descripción:** Como **médico especialista (2do nivel)**, quiero **ver las referencias entrantes de médicos generales**, para **priorizar y aceptar nuevos pacientes**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Soy especialista autenticado | Accedo a mi dashboard | Veo un contador "Referencias pendientes: X" |
| 2 | Hago clic en "Ver referencias" | Veo una lista con: paciente, médico que refiere, motivo, prioridad, fecha | Puedo ordenar por prioridad o fecha |
| 3 | Selecciono una referencia | Hago clic en "Aceptar" | La referencia pasa a "Aceptada" y puedo agendar cita |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-REF-003 | Realizar contrarreferencia | P1 | 2 |

**Descripción:** Como **médico especialista**, quiero **realizar una contrarreferencia al médico general**, para **informar el resultado de la atención y plan de seguimiento**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | He completado la consulta con el paciente | Al finalizar, veo la opción "Devolver a médico general" | Hago clic y veo un formulario para resumen |
| 2 | Completo el resumen de atención y plan de seguimiento | Envío la contrarreferencia | El médico general recibe notificación |
| 3 | El médico general recibe la contrarreferencia | Abre su bandeja | Ve el resumen y puede dar seguimiento |

---

### ÉPICA SER - SERVICIOS AUXILIARES (P1)

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-SER-001 | Generar orden de exámenes con QR | P1 | 3 |

**Descripción:** Como **médico**, quiero **generar órdenes de exámenes con código QR**, para **que el paciente pueda realizarlos sin papel**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Estoy en el paso 6 (Plan) | Hago clic en "+ Agregar examen" | Veo un buscador de exámenes disponibles |
| 2 | Selecciono "Hemograma" | Confirmo la orden | El sistema genera un QR único para este examen |
| 3 | El paciente llega al laboratorio | Muestra el QR | El técnico escanea y ve la orden completa |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-SER-002 | Generar receta electrónica con QR | P1 | 3 |

**Descripción:** Como **médico**, quiero **generar recetas electrónicas con código QR**, para **que el paciente pueda retirar medicamentos sin papel**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Estoy en el paso 6 (Plan) | Hago clic en "+ Agregar medicamento" | Veo un formulario con: medicamento, dosis, frecuencia, duración |
| 2 | Completo la prescripción | Confirmo | El sistema genera un QR único con los datos de la receta |
| 3 | La receta tiene fecha de caducidad | La receta no se usa después de X días | El sistema invalida el QR automáticamente |

---

### ÉPICA DASH - DASHBOARDS (P1)

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-DASH-001 | Dashboard del médico | P0 | 3 |

**Descripción:** Como **médico**, quiero **ver un dashboard con mi agenda del día y pacientes en espera**, para **organizar mi jornada de atención**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Soy médico autenticado | Accedo al sistema | Veo mi agenda del día con horarios y pacientes asignados |
| 2 | Hay pacientes en preclínica | Veo una sección "Pacientes en espera" | Los pacientes aparecen con orden de prioridad (triaje) |
| 3 | Hago clic en "Comenzar próximo paciente" | El sistema carga el flujo de consulta | El primer paciente en cola es asignado automáticamente |
| 4 | Termino una consulta | Vuelvo al dashboard | El paciente atendido ya no aparece en espera |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-DASH-002 | Dashboard del administrador de institución | P1 | 3 |

**Descripción:** Como **administrador de la institución**, quiero **ver un dashboard con métricas de mi clínica**, para **monitorear el rendimiento y la ocupación**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Soy administrador autenticado | Accedo al sistema | Veo tarjetas con: pacientes hoy, citas hoy, médicos activos, ausentismo |
| 2 | Quiero ver tendencias | Selecciono un período (semana, mes) | Veo gráficos de evolución de citas y ausentismo |
| 3 | Quiero exportar datos | Hago clic en "Exportar" | El sistema descarga un archivo CSV con las métricas |

---

### ÉPICA NOT - NOTIFICACIONES (P1)

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-NOT-001 | Enviar recordatorio de cita por correo | P1 | 3 |

**Descripción:** Como **paciente**, quiero **recibir un recordatorio de mi cita por correo**, para **no olvidar mi hora médica**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Tengo una cita agendada para mañana a las 10:00 | El sistema ejecuta la tarea programada a las 8:00 | Recibo un correo con los detalles de la cita |
| 2 | La cita está en 2 horas | Recibo un segundo recordatorio | El correo dice "Su cita es en 2 horas" |
| 3 | No tengo email registrado | El sistema intenta enviar | No se envía correo, se registra en log |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-NOT-002 | Enviar recordatorio de medicamentos por correo | P1 | 3 |

**Descripción:** Como **paciente**, quiero **configurar recordatorios de medicamentos**, para **tomar mis medicamentos a tiempo**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | El médico me prescribe un medicamento | Recibo un email "Recordatorio configurado" | El recordatorio se activa según la frecuencia prescrita |
| 2 | Es hora de tomar el medicamento | El sistema envía un correo | El correo dice "Hora de tomar [medicamento] [dosis]" |
| 3 | Puedo desactivar el recordatorio | Accedo a mis preferencias | Apago los recordatorios del medicamento |

---

### ÉPICA IA - INTELIGENCIA ARTIFICIAL (P2)

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-IA-001 | Sugerencia de diagnóstico por IA | P2 | 5 |

**Descripción:** Como **médico**, quiero **recibir sugerencias de diagnóstico basadas en los síntomas del paciente**, para **apoyar mi decisión clínica**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Estoy en el paso 5 (Diagnóstico) | Hago clic en "Sugerir diagnóstico IA" | El sistema envía datos anonimizados (edad, sexo, síntomas, motivo) a la API |
| 2 | La API responde con 3 diagnósticos probables | Veo los diagnósticos con porcentaje de probabilidad | Puedo seleccionar uno para precargar el campo diagnóstico |
| 3 | La API no responde (timeout) | El sistema muestra "Servicio no disponible" | Puedo continuar con el ingreso manual |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-IA-002 | Detección de riesgo de enfermedades crónicas | P2 | 5 |

**Descripción:** Como **médico**, quiero **recibir alertas de riesgo para enfermedades crónicas (diabetes, HTA)**, para **intervenir tempranamente**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | El paciente tiene IMC > 30 y antecedentes familiares de diabetes | El sistema analiza los datos | Muestra alerta "Riesgo alto de diabetes - considerar screening" |
| 2 | El paciente tiene TA > 140/90 en tres mediciones | El sistema detecta el patrón | Muestra alerta "Posible hipertensión - confirmar diagnóstico" |
| 3 | El médico ve la alerta | Puede actuar en consecuencia | La alerta se registra en la historia clínica |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-IA-003 | Predicción de ausentismo a citas | P2 | 3 |

**Descripción:** Como **administrador**, quiero **recibir predicciones de ausentismo para optimizar la agenda**, para **reducir pérdida de cupos**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | El sistema tiene historial de citas | Ejecuta el modelo predictivo | Asigna una probabilidad de ausentismo a cada cita nueva |
| 2 | Una cita tiene probabilidad > 70% | El sistema muestra alerta | Se sugiere overbooking o recordatorio adicional |
| 3 | La cita se cancela o confirma | El modelo se reentrena semanalmente | La precisión mejora con el tiempo (> 80%) |

---

### ÉPICA POR - PORTAL DEL PACIENTE (P2)

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-POR-001 | Ver próximas citas | P2 | 2 |

**Descripción:** Como **paciente autenticado**, quiero **ver mis próximas citas agendadas**, para **no perder la fecha de atención**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Inicio sesión en el portal | Accedo a "Mis citas" | Veo una lista de citas futuras con fecha, hora, médico y especialidad |
| 2 | Tengo una cita para hoy | Veo un botón "Llegué a la clínica" | Al hacer clic, el sistema registra mi llegada |
| 3 | Tengo una cita cancelada | Aparece en el historial | El estado es "Cancelada" y no está activa |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-POR-002 | Exportar historia clínica (HCE portátil) | P2 | 3 |

**Descripción:** Como **paciente**, quiero **exportar mi historia clínica completa en PDF o JSON**, para **tener un respaldo o compartirlo con otro médico**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Inicio sesión en el portal | Accedo a "Mi historia clínica" | Veo un botón "Exportar HCE" |
| 2 | Selecciono formato PDF | Hago clic en "Exportar" | El sistema genera un PDF con todas mis consultas, diagnósticos y tratamientos |
| 3 | Selecciono formato JSON (interoperabilidad) | Hago clic en "Exportar" | El sistema descarga un archivo JSON estructurado |

---

### ÉPICA SEG - SEGURIDAD Y AUDITORÍA (P0)

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-SEG-001 | Autenticación de usuarios | P0 | 2 |

**Descripción:** Como **usuario del sistema**, quiero **iniciar sesión con mi correo y contraseña**, para **acceder a las funciones según mi rol**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Accedo al sistema (subdominio específico) | Ingreso mi correo y contraseña | Si son correctos, accedo al dashboard de mi rol |
| 2 | Ingreso credenciales incorrectas | Hago clic en "Ingresar" | El sistema muestra "Credenciales inválidas" |
| 3 | Mi cuenta está inactiva | Intento iniciar sesión | El sistema muestra "Cuenta desactivada, contacte al administrador" |
| 4 | Soy usuario de otra institución | Intento acceder desde subdominio equivocado | El sistema no me permite acceder (aislamiento por tenant) |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-SEG-002 | Control de acceso por roles (RBAC) | P0 | 3 |

**Descripción:** Como **administrador**, quiero **que los usuarios tengan acceso solo a las funciones de su rol**, para **proteger la información sensible**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Un médico intenta acceder a la configuración de usuarios | Hace clic en "Administración" | El sistema muestra "Acceso denegado" |
| 2 | Un recepcionista intenta ver la historia clínica | Hace clic en el paciente | Puede ver solo datos básicos, no información clínica |
| 3 | Un administrador intenta ver reportes financieros | Accede al módulo de reportes | Tiene acceso completo |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-SEG-003 | Auditoría de cambios en datos clínicos | P0 | 3 |

**Descripción:** Como **administrador**, quiero **que todos los cambios en datos clínicos queden registrados**, para **tener trazabilidad y cumplir normativas**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Un médico modifica un diagnóstico | El sistema guarda la consulta | Se registra en tabla `log_auditoria`: usuario, acción (UPDATE), tabla, ID, fecha, valor anterior, valor nuevo |
| 2 | Un recepcionista elimina un paciente | Confirma la eliminación | Se registra la acción y quién la realizó |
| 3 | Reviso los logs de auditoría | Accedo al panel de auditoría | Veo una lista filtrable por usuario, fecha, tabla afectada |

---

### 🔮 ÉPICA HOS - HOSPITALIZACIÓN (Futuro)

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-HOS-001 | Registrar ingreso hospitalario | 🔮 | 5 |

**Descripción:** Como **médico**, quiero **registrar el ingreso de un paciente a hospitalización**, para **gestionar su internación y asignarle una cama**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | El paciente requiere hospitalización | En el plan de consulta, selecciono "Hospitalizar" | El sistema muestra el módulo de ingreso hospitalario |
| 2 | Selecciono servicio y tipo de cama | El sistema me muestra camas disponibles | Asigno una cama al paciente |
| 3 | El paciente ingresa | Confirmo el ingreso | El paciente pasa a estado "Hospitalizado" y su cama queda ocupada |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-HOS-002 | Gestionar mapa de camas | 🔮 | 5 |

**Descripción:** Como **enfermera o administrador**, quiero **ver un mapa de camas con disponibilidad por servicio**, para **asignar y liberar camas eficientemente**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Accedo al módulo de camas | Veo un mapa visual por servicio (ej: Medicina, Cirugía, UCI) | Cada cama muestra estado: Disponible, Ocupada, En limpieza |
| 2 | Hago clic en una cama ocupada | Veo detalles del paciente internado | Puedo gestionar el alta o traslado |
| 3 | Un paciente es dado de alta | Libero la cama | La cama cambia a "Disponible" |

---

### 🔮 ÉPICA OMS - CLASIFICACIONES OMS ESPECIALIZADAS (Futuro)

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-OMS-001 | Registrar diagnóstico oncológico con CIE-O | 🔮 | 5 |

**Descripción:** Como **oncólogo**, quiero **registrar el diagnóstico de un tumor usando códigos CIE-O**, para **documentar topografía, morfología y comportamiento del tumor**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Soy oncólogo autenticado | En el paso de diagnóstico, veo la opción "Registro oncológico (CIE-O)" | Puedo buscar por topografía (ej: C50 - Mama) |
| 2 | Selecciono topografía | Luego selecciono morfología (ej: M-8500 - Adenocarcinoma ductal) | El sistema completa el código CIE-O completo |
| 3 | Selecciono comportamiento (/3 - Maligno primario) | Guardo el diagnóstico | El diagnóstico queda registrado con el formato CIE-O |

---

| ID | Título | Prioridad | SP |
|----|--------|-----------|-----|
| HU-OMS-002 | Registrar evaluación funcional con CIF | 🔮 | 5 |

**Descripción:** Como **médico rehabilitador**, quiero **registrar una evaluación de funcionalidad usando CIF**, para **documentar el nivel de discapacidad del paciente**.

**Criterios de aceptación:**
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Soy médico rehabilitador autenticado | En la consulta, veo la opción "Evaluación funcional (CIF)" | Puedo buscar códigos CIF por componente (b, s, d, e) |
| 2 | Selecciono "d4 - Movilidad" | Elijo "Caminar" y asigno calificador (0-4) | El sistema registra la evaluación |
| 3 | Completo la evaluación CIF | Guardo los datos | El perfil de funcionalidad queda asociado a la consulta |

---

## 4. RESUMEN DE HISTORIAS POR ÉPICA

| Épica | Nombre | Total HU | P0 | P1 | P2 | 🔮 | SP Total |
|-------|--------|----------|----|----|----|----|----------|
| ADM | Administración Multi-tenant | 3 | 2 | 1 | 0 | 0 | 8 |
| TEN | Gestión de Tenant | 5 | 4 | 1 | 0 | 0 | 13 |
| PAC | Gestión de Pacientes | 3 | 3 | 0 | 0 | 0 | 6 |
| CIT | Agendamiento de Citas | 3 | 2 | 1 | 0 | 0 | 8 |
| PRE | Preclínica | 3 | 3 | 0 | 0 | 0 | 7 |
| CON | Consulta Médica | 4 | 4 | 0 | 0 | 0 | 13 |
| REF | Referencias | 3 | 0 | 3 | 0 | 0 | 7 |
| SER | Servicios Auxiliares | 2 | 0 | 2 | 0 | 0 | 6 |
| DASH | Dashboards | 2 | 1 | 1 | 0 | 0 | 6 |
| NOT | Notificaciones | 2 | 0 | 2 | 0 | 0 | 6 |
| IA | Inteligencia Artificial | 3 | 0 | 0 | 3 | 0 | 13 |
| POR | Portal Paciente | 2 | 0 | 0 | 2 | 0 | 5 |
| SEG | Seguridad | 3 | 3 | 0 | 0 | 0 | 8 |
| 🔮 HOS | Hospitalización (Futuro) | 2 | 0 | 0 | 0 | 2 | 10 |
| 🔮 OMS | Clasificaciones OMS (Futuro) | 2 | 0 | 0 | 0 | 2 | 10 |
| **TOTAL** | | **42** | **22** | **11** | **5** | **4** | **126** |

---

## 5. DESGLOSE POR PRIORIDAD Y SPRINT

| Prioridad | HU total | SP total |
|-----------|----------|----------|
| **P0 (MVP - Fase 1)** | 22 | 66 |
| **P1 (Fase 2)** | 11 | 38 |
| **P2 (Fase 3)** | 5 | 22 |
| **🔮 (Futuro)** | 4 | 20 |
| **TOTAL** | **42** | **146** |

---

## 6. APROBACIÓN

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Product Owner | [Usuario] | ✅ Aprobado | 2026 |
| Agente Documentación | DeepSeek | Generado | 2026 |

---

**Fin del Documento 3: Historias de Usuario**

---

## RESUMEN DEL DOCUMENTO

| Aspecto | Valor |
|---------|-------|
| **Total de historias de usuario** | 42 |
| **Épicas cubiertas** | 15 |
| **P0 (MVP - Fase 1)** | 22 historias (66 SP) |
| **P1 (Fase 2)** | 11 historias (38 SP) |
| **P2 (Fase 3)** | 5 historias (22 SP) |
| **🔮 (Futuro)** | 4 historias (20 SP) |
| **Multi-tenant incluido** | ✅ Sí (épicas ADM, TEN, SEG) |
| **Flujos guiados** | ✅ Sí (PRE, CON) |
| **Especialidades médicas** | ✅ Sí (TEN, REF) |

---
