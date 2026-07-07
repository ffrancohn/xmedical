# 1. PRD — DOCUMENTO DE REQUERIMIENTOS DEL PRODUCTO
## Módulo: Recepción Virtual Omnicanal (XMedical)

| Versión | Fecha | Autor | Estado |
|---------|-------|-------|--------|
| 0.1 | 2026-07 | Equipo XMedical | **Borrador — Descubrimiento** |

> Documento de negocio y usuario. Responde a **¿qué producto vamos a crear y para quién?**. No entra todavía en código, base de datos ni tecnologías (eso va en el TRD y en Backend/Esquema). Complementa el resumen de diseño de [Documento 15](../15%20Recepcion%20Virtual%20Omnicanal.md).

---

## 1. Nombre provisional

**Recepción Virtual** (asistente omnicanal de XMedical). Se evita el término "recepcionista" para no confundir con el **rol humano** `recepcionista` ya existente en el sistema.

---

## 2. Problema que resuelve

Las clínicas pierden tiempo y citas por tareas repetitivas de comunicación:

- El personal de recepción se satura llamando/escribiendo para **recordar y confirmar** citas.
- Los pacientes **no tienen atención fuera del horario** de la clínica.
- Las solicitudes llegan por **canales dispersos** (llamada, WhatsApp, correo) sin registro unificado.
- El **ausentismo** (pacientes que no llegan) reduce la ocupación de la agenda.

---

## 3. Objetivo principal

Ofrecer un asistente que **reciba y envíe comunicaciones con los pacientes por correo, WhatsApp y voz**, entienda su intención y ejecute acciones administrativas sobre XMedical (agendar, reprogramar, cancelar, confirmar, responder preguntas frecuentes), **descargando al personal humano** y atendiendo 24/7, siempre dentro del tenant correcto y con opción de escalar a una persona.

---

## 4. Usuarios objetivo

| Tipo de usuario | Descripción | Interacción con Recepción Virtual |
|-----------------|-------------|-----------------------------------|
| **Paciente** | Persona que busca o tiene una cita | Escribe/llama por WhatsApp, correo o voz |
| **Recepcionista** (humano) | Personal administrativo de la clínica | Recibe conversaciones escaladas; supervisa desde un panel web |
| **Administrador de institución** | Configura la clínica | Activa canales, plantillas, horarios de atención del bot |
| **Superadmin proveedor** | Operador de la plataforma | Habilita el módulo y proveedores por institución |

---

## 5. Propuesta de valor

- **Para el paciente:** atención inmediata 24/7 en su canal preferido, sin esperas ni llamadas repetidas.
- **Para la clínica:** menos carga operativa, menos ausentismo (recordatorios/confirmaciones automáticas) y mejor ocupación de agenda.
- **Para el proveedor (XMedical):** función diferenciadora omnicanal integrada al sistema clínico existente y multi-tenant.

---

## 6. Alcance inicial (MVP)

El MVP se concentra en el canal de **menor costo y riesgo** y en los casos de mayor impacto:

**Incluido en el MVP:**

- Canal **Email** (recibir y enviar).
- Intenciones: **recordatorio**, **confirmación** y **cancelación** de citas; **pregunta frecuente** simple.
- Identificación del paciente y del tenant a partir del mensaje entrante.
- **Escalado a un humano** (recepcionista) cuando la confianza es baja o el paciente lo pide.
- Registro/auditoría de todas las conversaciones.
- Configuración básica por institución (activar canal, plantillas).

**Fuera del MVP (fases posteriores):**

- Canal **WhatsApp** (Fase 2).
- Canal **Voz** / llamadas (Fase 3).
- Agendamiento conversacional completo con selección de médico/horario (Fase 2).
- Campañas/marketing masivo.
- Pagos o cobros.
- Consejo o diagnóstico clínico (queda **explícitamente excluido**, ver reglas de negocio).

---

## 7. Funcionalidades principales

1. Recibir mensajes entrantes por canal (email en MVP; WhatsApp/voz después).
2. Identificar tenant y paciente.
3. Clasificar la intención del mensaje (NLU/IA).
4. Ejecutar acciones sobre citas: confirmar, cancelar, (agendar/reprogramar en fases siguientes).
5. Responder preguntas frecuentes (horarios, ubicación, requisitos).
6. Enviar mensajes proactivos: recordatorios y confirmaciones de cita.
7. Escalar a un recepcionista humano (handoff) con contexto.
8. Panel web para que la recepción vea, retome y cierre conversaciones.
9. Registrar todo para auditoría y métricas.

---

## 8. Funcionalidades fuera de esta primera versión

- WhatsApp y voz (planificadas, pero **proveedor a definir** — ver [Documento 15](../15%20Recepcion%20Virtual%20Omnicanal.md) §7 y §8).
- Recomendaciones clínicas con IA.
- Integración con pagos.
- Multilenguaje (arranca en **español LatAm**).

---

## 9. Casos de uso principales

- **CU-01 Recordatorio y confirmación:** el sistema envía un recordatorio 24 h antes; el paciente responde "confirmo" o "cancelo" y la cita se actualiza.
- **CU-02 Cancelación por iniciativa del paciente:** el paciente escribe para cancelar; el sistema identifica su cita y la cancela, liberando el horario.
- **CU-03 Pregunta frecuente:** el paciente pregunta por horarios/ubicación; el sistema responde con información de la institución.
- **CU-04 Escalado a humano:** el paciente pide "hablar con una persona" o el sistema no entiende; la conversación pasa a un recepcionista con el historial.
- **CU-05 (Fase 2) Agendamiento:** el paciente solicita una cita; el sistema ofrece disponibilidad, la agenda y confirma.

---

## 10. Reglas de negocio importantes

- **RN-01:** el asistente **nunca** brinda diagnóstico ni consejo médico; solo tareas administrativas y deriva a un profesional.
- **RN-02:** toda acción se limita al **tenant** (institución) del canal; jamás se cruzan datos entre clínicas.
- **RN-03:** se requiere **consentimiento (opt-in)** del paciente para contactarlo por cada canal; en voz, aviso de grabación.
- **RN-04:** por canales externos se envía **el mínimo dato necesario** (no volcar historia clínica por WhatsApp/correo).
- **RN-05:** ante baja confianza o acción sensible, **escalar a humano** en vez de adivinar.
- **RN-06:** una cita solo puede confirmarse/cancelarse por su paciente titular (verificación de identidad).
- **RN-07:** el bot respeta el **horario de atención** configurado por institución para mensajes proactivos.

---

## 11. Criterios de éxito (indicadores)

| Indicador | Meta inicial |
|-----------|--------------|
| Tasa de confirmación de citas vía asistente | ≥ 40 % de las citas recordadas |
| Reducción de ausentismo (no-shows) | −20 % respecto a la línea base |
| Conversaciones resueltas sin humano | ≥ 60 % en MVP (email) |
| Tiempo medio de primera respuesta (canales asíncronos) | < 1 min |
| Errores de identificación de tenant/paciente | < 1 % |
| Satisfacción del paciente (encuesta post-conversación) | ≥ 4/5 |

---

## 12. Prioridades

| Prioridad | Función |
|-----------|---------|
| Alta | Recepción/envío por **Email** (MVP) |
| Alta | Identificación tenant + paciente |
| Alta | Recordatorio y confirmación de citas |
| Alta | Escalado a humano + panel de conversaciones |
| Media | Cancelación/reprogramación conversacional |
| Media | Canal **WhatsApp** (Fase 2) |
| Baja | Canal **Voz** (Fase 3) |
| Baja | Preguntas frecuentes avanzadas / base de conocimiento |

---

## 13. Referencias

- [Documento 15: Recepción Virtual Omnicanal (resumen de diseño)](../15%20Recepcion%20Virtual%20Omnicanal.md)
- [Documento 1: Visión de Producto](../1%20Documento%20de%20Vision%20de%20Producto.md)
- [Documento 2: MVP](../2%20Documento%20de%20MVP.md)

---

**Fin del PRD — Recepción Virtual**
