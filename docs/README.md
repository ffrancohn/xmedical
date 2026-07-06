# Documentación XMedical

Índice de documentación del proyecto.

## Estado de implementación (2026-07)

| Área | Estado | Notas |
|------|--------|-------|
| Backend Django 4.2 | ✅ Producción | Gunicorn + systemd |
| Frontend web (plantillas) | ✅ Producción | https://xmedical.cloud |
| PostgreSQL + Redis | ✅ Docker | Puertos 5432 / 6379 |
| HTTPS | ✅ Let's Encrypt | Certificado auto-renovable |
| Multi-tenant (subdominio) | ✅ Implementado | `TenantMiddleware` |
| API REST / JWT | 🔮 Planificado | Ver [doc 13](13%20App%20movil%20y%20API%20REST.md) |
| App móvil | 🔮 Planificado | Repo separado, consume API |
| Celery workers | ⚠️ Configurado | Docker compose, no en systemd prod. |
| Microservicio IA (FastAPI) | 🔮 Fase 4 | Visión producto, no el prototipo eliminado |

**Producción actual:** `https://xmedical.cloud` — Apache → Gunicorn → Django.

---

## Documentos de producto

| # | Documento | Descripción |
|---|---|---|
| 0 | [Descripción General](0%20Documento%20de%20Descripcion%20General.md) | Visión, usuarios y alcance |
| 1 | [Visión de Producto](1%20Documento%20de%20Vision%20de%20Producto.md) | Objetivos estratégicos |
| 2 | [MVP](2%20Documento%20de%20MVP.md) | Alcance mínimo viable |
| 3 | [Historias de Usuario](3%20Documento%20de%20Historias%20de%20Usuario.md) | Requisitos funcionales |
| 4 | [Arquitectura de alto nivel](4%20Documento%20Arquitectura%20de%20alto%20nivel.md) | Arquitectura Django |
| 5 | [Diagramas de Flujo](5%20Documento%20Diagramas%20de%20Flujo.md) | Flujos clínicos |
| 6 | [Modelo de datos](6%20Documento%20Modelo%20de%20datos.md) | Entidades y relaciones |
| 7 | [Seguridad](7%20Documento%20de%20Seguridad.md) | Políticas de seguridad |
| 8 | [Modelo de negocio](8%20Documento%20de%20modelo%20de%20negocio.md) | Modelo comercial |
| 9 | [Integraciones](9%20Documento%20de%20integraciones.md) | APIs e integraciones externas |
| 10 | [Plan de Pruebas](10%20Plan%20de%20Pruebas.md) | Estrategia de testing |
| 11 | [Plan de Despliegue](11%20Plan%20de%20Deespliegue.md) | Despliegue en producción |
| 12 | [Sprint backlog](12%20Sprint%20backlog.md) | Backlog de desarrollo |
| 13 | [App móvil y API REST](13%20App%20movil%20y%20API%20REST.md) | **Hoja de ruta móvil** |

## Guías operativas

| Documento | Descripción |
|---|---|
| [`../README.md`](../README.md) | Instalación y uso |
| [`../GUIA_CONFIGURACION.md`](../GUIA_CONFIGURACION.md) | Configuración local y producción |
| [`../USUARIOS_PRUEBA.md`](../USUARIOS_PRUEBA.md) | Credenciales demo |
| [`run_tests.sh`](../run_tests.sh) | Suite Django + cobertura |
| [`scripts/run_all_verifications.sh`](../scripts/run_all_verifications.sh) | Verificación completa + informe |
| [Checklist UAT](CHECKLIST-UAT.md) | Aceptación manual por rol |
| [Informes de verificación](informes/) | Informes automáticos semanales |
| [Evidencia de pruebas](informes/evidencia/) | **Logs y resultados completos por ejecución** |
| [Informe verificación 2026-07-06](INFORME-VERIFICACION-2026-07-06.md) | Revisión operativa inicial |
