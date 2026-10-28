# 20 · Archivo: idea original «Agente Médico»

Documento de archivo. Conserva el único contenido del repositorio `agentemedico` antes de su eliminación (local y en GitHub). No es documentación funcional vigente: es un registro histórico de la idea de producto de la que nació XMedical.

## Procedencia

| Dato | Valor |
|---|---|
| Repositorio | `ffrancohn/agentemedico` (https://github.com/ffrancohn/agentemedico) |
| Archivo | `README.md` (360 bytes) |
| Commit | `dc3f064` — «Initial commit», 2025-06-12 08:42 (-0600), Francisco Alejandro Franco |
| Contenido del repo | Solo ese README: sin código, sin pruebas, sin ramas adicionales |
| Archivado | 2026-10-28, antes de eliminar el repositorio |

## Texto original (íntegro)

> # agentemedico
> Plataforma de gestión médica con IA integrada que automatiza tareas clínicas y administrativas, ofreciendo diagnósticos sugeridos y flujos personalizados según el rol del usuario. Diferenciador: Enfoque realista en problemas médicos diarios, uso centrado en el rol, y capacidades clínicas de IA no presentes en softwares tradicionales.

## Correspondencia con XMedical

Ninguna idea de este README queda sin cubrir en el proyecto actual; la única que no está cerrada es la sugerencia diagnóstica asistida por IA.

| Idea del README | Estado en XMedical | Dónde |
|---|---|---|
| Plataforma de gestión médica | ✅ En producción | [README](../README.md) |
| Automatización de tareas clínicas y administrativas | ✅ Implementado | `apps/citas`, `apps/preclinica`, `apps/consulta`, `apps/notificaciones` |
| Flujos personalizados según rol | ✅ Implementado | Roles superadmin, admin, médico, enfermera, recepcionista |
| Diagnósticos sugeridos con IA | ⚠️ Parcial / en curso | `apps/core/ai_services.py`, `apps/core/views_ai.py`, [doc 16](16%20Modelo%20Local%20IA%20(Ollama).md), [doc 17](17%20Caracteristicas%20Pantallas%20y%20Flujo%206%20Diagnostico.md) |
| «Enfoque realista en problemas médicos diarios» | ✅ Principio de diseño | [doc 1](1%20Documento%20de%20Vision%20de%20Producto.md), [doc 0](0%20Documento%20de%20Descripcion%20General.md) |
| IA clínica ausente en software tradicional | 🔮 Diferenciador vigente | `apps/ia_predictiva` (ausentismo, demanda, riesgo crónico) |
