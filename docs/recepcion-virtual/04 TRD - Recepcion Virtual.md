# 4. TRD — DOCUMENTO DE REQUERIMIENTOS TÉCNICOS
## Módulo: Recepción Virtual Omnicanal (XMedical)

| Versión | Fecha | Autor | Estado |
|---------|-------|-------|--------|
| 0.1 | 2026-07 | Equipo XMedical | **Borrador** |

> Responde a **¿cómo debe funcionar técnicamente?**. Traduce el [PRD](01%20PRD%20-%20Recepcion%20Virtual.md) a requisitos de arquitectura, seguridad, rendimiento e integraciones. El detalle de datos/API está en [Backend y Esquema](05%20Backend%20y%20Esquema%20de%20Datos%20-%20Recepcion%20Virtual.md).

---

## 1. Tipo de aplicación

Módulo **backend dentro del monolito Django** de XMedical (no un servicio separado), más una **UI web** (plantillas server-side) para el panel de recepción. Los pacientes interactúan por **canales externos** (email/WhatsApp/voz), no por una app propia.

---

## 2. Tecnologías propuestas

| Capa | Tecnología | Justificación |
|------|------------|---------------|
| Backend | Django 4.2 (app `apps/recepcion_virtual/`) | Reutiliza el stack actual |
| Tareas asíncronas | Celery + Redis | Ya presentes; ideal para webhooks/no bloquear |
| Base de datos | PostgreSQL 15 | Motor único del sistema |
| IA / NLU | `apps.core.ai_services` (OpenAI/OpenRouter) | Ya integrado y configurable por entorno |
| Email | Django email backend + inbound (SES/SendGrid/Postmark) | Ver [Doc 15](../15%20Recepcion%20Virtual%20Omnicanal.md) §6 |
| WhatsApp | **Proveedor a definir** (Meta Cloud API / Twilio / 360dialog) | Ver [Doc 15](../15%20Recepcion%20Virtual%20Omnicanal.md) §7 |
| Voz | **Proveedor a definir** (telefonía + STT + TTS) | Ver [Doc 15](../15%20Recepcion%20Virtual%20Omnicanal.md) §8 |
| Panel web | Plantillas Django + WhiteNoise | Consistencia con el resto |

---

## 3. Compatibilidad (panel web)

- **Navegadores:** últimas 2 versiones de Chrome, Edge, Firefox y Safari.
- **Dispositivos:** escritorio y móvil (diseño responsivo).
- **Sistemas:** independiente del SO (web).

---

## 4. Autenticación

| Actor | Mecanismo |
|-------|-----------|
| Recepcionista/Admin (panel web) | Sesión Django existente (login actual) |
| Pacientes (canales) | Sin sesión; identidad por remitente + verificación (documento) |
| Webhooks entrantes (proveedores) | Verificación de **firma/HMAC** y token de verificación por canal |
| Acciones a la API interna (si se usa Doc 13) | JWT / servicio interno |

---

## 5. Roles y permisos

Se reutilizan los roles existentes de XMedical:

| Rol | Permisos en Recepción Virtual |
|-----|-------------------------------|
| Superadmin proveedor | Habilitar módulo y proveedores por institución |
| Admin institución | Configurar canales, plantillas, horario del bot |
| Recepcionista | Ver/atender/cerrar conversaciones, ejecutar acciones de cita |
| Médico / Enfermera | Sin acceso al panel (salvo lectura opcional) |
| Paciente | Interacción por canal, solo sobre sus propios datos |

---

## 6. Integraciones externas

| Integración | Dirección | Protocolo | Notas |
|-------------|-----------|-----------|-------|
| Email | Entrante + saliente | SMTP / API REST + webhook inbound o IMAP | Proveedor configurable |
| WhatsApp | Entrante + saliente | API REST + webhook | **Proveedor a definir**; plantillas HSM, ventana 24 h |
| Voz | Entrante + saliente | Telefonía/SIP + webhooks + STT/TTS | **Proveedor a definir**; streaming para baja latencia |
| LLM/NLU | Saliente | API REST | Vía `apps.core.ai_services` |

---

## 7. Requisitos de seguridad

- Verificación de **firma HMAC/token** en todos los webhooks entrantes.
- **Aislamiento estricto por tenant** (`institucion_id`) en cada conversación y acción.
- **Minimización de datos** en canales externos (RN-04 del PRD).
- **Consentimiento (opt-in)** por canal y aviso de grabación en voz (RN-03).
- **Secretos de proveedor fuera de la BD** (variables de entorno / gestor de secretos); en BD solo referencias.
- **TLS** en todo el tráfico.
- Alinear con [Documento 7: Seguridad](../7%20Documento%20de%20Seguridad.md) y [Documento 14: Roadmap Seguridad](../14%20Roadmap%20Seguridad.md).

---

## 8. Rendimiento esperado

| Métrica | Objetivo |
|---------|----------|
| Respuesta del webhook (ACK al proveedor) | < 500 ms (procesamiento real en Celery) |
| Primera respuesta en canales asíncronos (email/WhatsApp) | < 1 min |
| Latencia conversacional en voz (STT→LLM→TTS) | < 1.5 s por turno |
| Panel web (carga de bandeja) | < 3 s con cientos de conversaciones |
| Concurrencia | Escalar workers Celery según volumen por tenant |

---

## 9. Disponibilidad y respaldo

- Conversaciones y mensajes persistidos en PostgreSQL → cubiertos por los **respaldos diarios** existentes.
- Reintentos con backoff en Celery ante caídas de proveedor.
- **Degradación elegante**: si un canal cae, avisar a recepción o cambiar de canal.
- Idempotencia por `externo_id` para no duplicar procesamiento de webhooks reintentados.

---

## 10. Registro de auditoría

- Registrar cada **mensaje** (entrante/saliente), **intención** detectada y **acción** ejecutada.
- Integrar con la auditoría de `apps.core` (quién/qué/cuándo/detalle).
- Registrar escalados, cierres y cambios de estado de cita originados por el bot.

---

## 11. Escalabilidad

- Procesamiento asíncrono desacoplado (Celery) permite escalar horizontalmente los workers.
- Adaptadores por canal → agregar/cambiar proveedores sin tocar el orquestador.
- Configuración por tenant → cada institución con su propio número/credenciales/volumen.

---

## 12. Restricciones técnicas

- No introducir un backend separado: todo dentro del monolito Django.
- WhatsApp requiere **API oficial** (no conexiones no autorizadas).
- El asistente **no** ejecuta lógica clínica (solo administrativa).
- Español LatAm como idioma inicial.

---

## 13. Requisitos no funcionales (resumen)

| Área | Requerimiento |
|------|---------------|
| Acceso (panel) | Login Django con correo/usuario y contraseña, control por roles |
| Seguridad | Webhooks firmados, aislamiento por tenant, secretos fuera de BD, TLS |
| Datos | PostgreSQL; retención/borrado de audios y transcripciones |
| Backend | Django + Celery; adaptadores por canal |
| Integración | Email (MVP), WhatsApp (Fase 2), Voz (Fase 3) — proveedores configurables |
| Auditoría | Registrar mensajes, intenciones y acciones |
| Respaldo | Copias diarias de la BD (existente) |
| Rendimiento | ACK webhook < 500 ms; voz < 1.5 s/turno |

---

## 14. Referencias

- [PRD — Recepción Virtual](01%20PRD%20-%20Recepcion%20Virtual.md)
- [Documento 15: Recepción Virtual Omnicanal](../15%20Recepcion%20Virtual%20Omnicanal.md)
- [Documento 4: Arquitectura de alto nivel](../4%20Documento%20Arquitectura%20de%20alto%20nivel.md)
- [Documento 7: Seguridad](../7%20Documento%20de%20Seguridad.md)
- [Documento 9: Integraciones](../9%20Documento%20de%20integraciones.md)

---

**Fin del TRD — Recepción Virtual**
