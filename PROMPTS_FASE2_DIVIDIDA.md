# Prompts divididos para XMedical Fase 2

Este documento divide la Fase 2 en prompts ejecutables por partes. La idea es evitar que Codex/Cursor intente modificar demasiadas areas al mismo tiempo.

## Politica de APIs y modelos

No pegar claves reales en el prompt, codigo o repositorio. Usar variables de entorno.

| Proveedor | Uso | Modelc:\py\ruta-interna.rar c:\py\voices.rar c:\py\xmedical.rar c:\py\Dashboard Estadistico IHSS.raro | Variable de API Key | Base URL | Notas |
|---|---|---|---|---|---|
| OpenAI | Diagnostico sugerido, resumen clinico, ayuda de redaccion | PENDIENTE_DEFINIR | `OPENAI_API_KEY` | `https://api.openai.com/v1` | Usar solo con datos minimos necesarios y consentimiento/configuracion institucional. |
| OpenRouter | Diagnostico sugerido, OCR asistido, clasificacion de texto | PENDIENTE_DEFINIR | `OPENROUTER_API_KEY` | `https://openrouter.ai/api/v1` | El modelo se selecciona por institucion o por configuracion global. |
| Google Cloud Vision | OCR/vision de documentos | `google-cloud-vision` | `GOOGLE_APPLICATION_CREDENTIALS` | N/A | Opcional; fallback manual obligatorio. |
| AWS Rekognition/Textract | OCR/vision de documentos | `boto3` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | Region por `AWS_REGION` | Opcional; fallback manual obligatorio. |
| Email/SendGrid | Recordatorios | N/A | `SENDGRID_API_KEY` | N/A | Alternativamente SMTP Django. |

Variables sugeridas para `.env`:

```bash
OPENAI_API_KEY=
OPENAI_MODEL=
OPENROUTER_API_KEY=
OPENROUTER_MODEL=
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
AI_PROVIDER=openai

GOOGLE_APPLICATION_CREDENTIALS=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1

QR_BASE_URL=http://localhost:8000/qr/
QR_EXPIRATION_DAYS=30

SENDGRID_API_KEY=
EMAIL_FROM=noreply@xmedical.local
```

Cuando me des el listado de modelos, reemplazar esta tabla:

| Prioridad | Proveedor | Modelo | Uso recomendado | Costo/latencia | Variable |
|---|---|---|---|---|---|
| 1 | OpenAI | PENDIENTE | Produccion clinica controlada | PENDIENTE | `OPENAI_MODEL` |
| 2 | OpenRouter | PENDIENTE | Alternativa economica o especializada | PENDIENTE | `OPENROUTER_MODEL` |
| 3 | OpenRouter | PENDIENTE | Tareas ligeras: resumen, clasificacion | PENDIENTE | `OPENROUTER_MODEL_FAST` |

---

## Prompt 1 - Infraestructura IA y configuracion por institucion

```markdown
Analiza el proyecto XMedical actual y agrega una capa de configuracion para proveedores IA sin ejecutar integraciones externas reales todavia.

Objetivo:
- Permitir usar OpenAI o OpenRouter mediante variables de entorno.
- Permitir seleccionar proveedor/modelo por configuracion global o por institucion.
- No guardar API keys reales en base de datos.
- Crear servicios reutilizables para llamadas IA con una interfaz comun.

Cambios esperados:
- Agregar variables a `.env.example`.
- Agregar settings para:
  - `OPENAI_API_KEY`
  - `OPENAI_MODEL`
  - `OPENROUTER_API_KEY`
  - `OPENROUTER_MODEL`
  - `OPENROUTER_BASE_URL`
  - `AI_PROVIDER`
- Crear `apps/core/ai_services.py` con:
  - `AIClient`
  - `OpenAIProvider`
  - `OpenRouterProvider`
  - metodo `complete(system_prompt, user_prompt, model=None, temperature=0.2)`
- Agregar validaciones para no fallar si no hay claves configuradas.
- Agregar tests unitarios usando mocks, sin llamadas reales a internet.

Restricciones:
- No ejecutar llamadas reales a OpenAI/OpenRouter.
- No modificar el flujo clinico todavia.
- Mantener compatibilidad con Django 4.2.
```

---

## Prompt 2 - Referencias y contrarreferencias

```markdown
Implementa referencias y contrarreferencias para XMedical Fase 2.

Objetivo:
- Medico general puede referir paciente a una especialidad de segundo nivel.
- Especialista puede aceptar/rechazar la referencia.
- Al aceptar, puede agendar una cita.
- Al finalizar, puede crear contrarreferencia al primer nivel.

Crear app:
- `apps/referencias`

Modelos:
- `Referencia`
- `Contrarreferencia`

Vistas:
- Bandeja de referencias pendientes.
- Crear referencia desde consulta.
- Aceptar/rechazar referencia.
- Crear contrarreferencia.

Templates DaisyUI:
- Lista/bandeja de referencias.
- Formulario de referencia.
- Detalle de referencia.
- Formulario de contrarreferencia.

Reglas:
- Todo debe filtrarse por institucion salvo superadmin.
- Superadmin puede filtrar por una o varias instituciones.
- No borrar ni modificar datos de Fase 1.
- Incluir migraciones.
- Incluir pruebas basicas.
```

---

## Prompt 3 - Agendamiento flexible

```markdown
Agrega agendamiento flexible al modulo de citas de XMedical.

Objetivo:
- Mantener agendamiento especifico actual.
- Agregar opcion flexible por rango:
  - rango de fechas
  - preferencia de jornada: manana, tarde, cualquiera
  - especialidad
  - medico opcional
- El sistema asigna automaticamente el primer turno disponible.

Crear:
- `apps/citas/services.py`
- `FlexibleAgendamientoService`

Metodos:
- `buscar_disponibilidad(profesional, fecha_inicio, fecha_fin, jornada)`
- `asignar_primer_turno(paciente, especialidad, fecha_inicio, fecha_fin, jornada, profesional=None)`

UI:
- Formulario de cita flexible.
- Mostrar resultado asignado.
- Mostrar error si no hay turnos.

Reglas:
- Respetar horarios del profesional.
- Evitar choques con citas existentes.
- Filtrar por institucion.
- Agregar pruebas unitarias del algoritmo.
```

---

## Prompt 4 - QR para recetas, examenes y check-in

```markdown
Implementa codigos QR para XMedical Fase 2.

Crear app:
- `apps/qr`

Modelo:
- `DocumentoQR`

Servicio:
- `QRService`

Funciones:
- Generar QR de orden de examen.
- Generar QR de receta.
- Generar QR de check-in de cita.
- Validar QR por token.
- Marcar QR como usado.
- Rechazar QR vencido o ya usado.

Dependencias:
- `segno`
- `qrcode`

UI:
- Boton para generar QR en consulta.
- Vista publica/segura para validar QR.
- Pantalla de resultado de validacion.

Reglas:
- Token aleatorio seguro.
- Caducidad configurable por `.env`.
- Filtrar por institucion.
- Incluir migraciones y tests.
```

---

## Prompt 5 - Variables clinicas por especialidad

```markdown
Agrega variables clinicas configurables por especialidad.

Crear app:
- `apps/variables_clinicas`

Modelos:
- `VariableClinica`
- `ValorVariableClinica`

Objetivo:
- Admin de clinica configura campos por especialidad.
- En consulta, el wizard muestra campos dinamicos segun especialidad del profesional/cita.
- Guardar valores por consulta.

Tipos:
- texto
- numero
- booleano
- fecha
- select

UI:
- Admin Django para configurar variables.
- Seccion nueva en wizard de consulta.

Reglas:
- Variables filtradas por institucion y especialidad.
- Validar campos obligatorios.
- Incluir migraciones y tests.
```

---

## Prompt 6 - Vision IA para documentos

```markdown
Agrega validacion IA/OCR de documentos de paciente.

Objetivo:
- Subir imagen de cedula/pasaporte.
- Extraer nombre, documento y fecha de nacimiento.
- Permitir confirmar o corregir manualmente antes de guardar.

Crear:
- `apps/pacientes/services/vision_service.py`
- `VisionService`

Proveedores:
- Google Cloud Vision
- AWS Textract/Rekognition
- OpenAI/OpenRouter vision-capable model cuando este configurado

Reglas:
- Si no hay API keys, mostrar fallback manual.
- No enviar imagenes a proveedores sin configuracion explicita.
- Guardar resultado OCR y confianza solo si se agrega modelo para auditoria.
- No guardar claves reales.

UI:
- Subida de documento en formulario de paciente.
- Pantalla de revision de datos extraidos.

Tests:
- Mock de respuestas OCR.
- Prueba de fallback manual.
```

---

## Prompt 7 - Notificaciones y recordatorios

```markdown
Implementa recordatorios con Celery y Redis.

Objetivo:
- Recordatorio de cita 24h antes.
- Recordatorio de cita 1h antes.
- Recordatorio de medicamentos configurable.

Crear app:
- `apps/notificaciones`

Archivos:
- `tasks.py`
- `services.py`
- `models.py` si se requiere bitacora de envio.

Actualizar:
- `xmedical/celery.py`
- `docker-compose.yml` con `celery` y `celery-beat`
- `.env.example` con email settings.

Reglas:
- No enviar email real en tests.
- Usar backend de email configurable.
- Registrar bitacora de envios.
- Evitar duplicados.
```

---

## Prompt 8 - Dashboards de enfermeria, administracion y especialista

```markdown
Agrega dashboards avanzados para Fase 2.

Crear app:
- `apps/dashboards`

Dashboards:
- Enfermeria:
  - pacientes pendientes de preclinica
  - pacientes ya evaluados
  - alertas vitales
- Administracion de clinica:
  - ocupacion de agenda
  - ausentismo
  - citas canceladas
  - consultas atendidas
- Especialista:
  - referencias pendientes
  - referencias aceptadas
  - agenda propia

Reglas:
- Admin de clinica ve solo su institucion.
- Superadmin puede filtrar una o varias instituciones.
- Usar DaisyUI.
- Mantener dashboard medico actual.
```

---

## Prompt 9 - Mejoras al wizard de consulta con IA

```markdown
Mejora el wizard de consulta.

Objetivo:
- Autosave cada 30 segundos.
- Atajo Ctrl+Enter para avanzar.
- Sugerencia basica de diagnostico usando OpenAI/OpenRouter si esta configurado.

Crear:
- `static/js/wizard.js`
- endpoint autosave seguro
- endpoint sugerir diagnostico

Reglas IA:
- No enviar datos identificables del paciente por defecto.
- Enviar solo motivo, anamnesis y examen fisico.
- Si no hay API key, ocultar o desactivar sugerencias IA.
- Mostrar sugerencias como apoyo, nunca como diagnostico definitivo.

UI:
- Indicador de autosave.
- Boton "Sugerir diagnosticos".
- Confirmacion manual antes de agregar diagnostico.
```

---

## Orden recomendado de ejecucion

1. Prompt 1 - Infraestructura IA.
2. Prompt 2 - Referencias y contrarreferencias.
3. Prompt 3 - Agendamiento flexible.
4. Prompt 5 - Variables clinicas por especialidad.
5. Prompt 8 - Dashboards.
6. Prompt 4 - QR.
7. Prompt 7 - Notificaciones.
8. Prompt 6 - Vision IA.
9. Prompt 9 - Wizard con autosave e IA.

Este orden reduce riesgos porque primero crea bases internas y deja para despues integraciones externas.
