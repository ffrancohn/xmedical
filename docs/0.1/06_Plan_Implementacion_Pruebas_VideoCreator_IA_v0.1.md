# Plan de Implementación y Pruebas

**Proyecto:** VideoCreator IA  
**Versión:** 0.1b  
**Estado:** Planificación actualizada (visión redefinida + Fase 7b + v0.2 medios)

---

## 1. Estrategia de implementación

El proyecto se desarrollará por fases incrementales. Cada fase deberá producir una versión utilizable y verificable.

---

## 2. Fases

### Fase 1. Base del sistema

Entregables:

- Estructura de código.
- Ventana principal.
- Base de datos.
- Gestión de proyectos.
- Sistema de configuración.
- Sistema de logs.

Criterio de salida:

- Se pueden crear, guardar y abrir proyectos.

### Fase 2. Guion

Entregables:

- Editor.
- División de escenas.
- Reordenamiento.
- Guardado automático.
- Cálculo de duración.

Criterio de salida:

- El usuario puede convertir un texto en escenas administrables.

### Fase 3. Proveedores de voz

Entregables:

- Interfaz común.
- OpenAI.
- ElevenLabs.
- Validación de credenciales.
- Consulta de voces.
- Generación de audio.

Criterio de salida:

- Se puede generar y reproducir audio desde ambos proveedores.

### Fase 4. Grabación

Entregables:

- Selección de micrófono.
- Grabación.
- Pausa.
- Reproducción.
- Guardado.

Criterio de salida:

- Se puede grabar y asociar una toma a una escena.

### Fase 5. Edición de audio

Entregables:

- Forma de onda básica.
- Recorte.
- División.
- Unión.
- Normalización.

Criterio de salida:

- Se puede preparar una narración final básica.

### Fase 6. Video (importación)

Entregables:

- Importación.
- Vista previa / reproducción.
- FFprobe.
- Recorte.
- Manejo de audio original.

Criterio de salida:

- Se puede importar y preparar un video.

### Fase 7. Composición y exportación (base)

Entregables:

- Unión de audio y video.
- Validación de sincronización audio/video (RF-049a).
- Resoluciones.
- Orientaciones.
- Progreso.
- Exportación MP4.

Criterio de salida:

- Se genera un archivo MP4 reproducible.

### Fase 7b. MVP redefinido — captura y 3 pistas (ciclo 0.1b)

Entregables (planificación → desarrollo):

- Navegación unificada desde pantalla de inicio.
- Etiquetas legibles de monitores (RF-067).
- Captura pantalla y cámara con preview (RF-063..066) — parcialmente adelantado.
- Captura de **región** y **ventana** (RF-068, RF-069).
- Composición con máximo **3 pistas**: original, narración, música (RF-070..073).
- FL-011, FL-012, FL-013.
- Actualización de pruebas CP-011..CP-015.

Criterio de salida:

- Cumplir criterios de aceptación del MVP redefinido (PRD §12).

### Fase 8. Pruebas y distribución

Entregables:

- Casos de prueba completos.
- Instalador para Windows con FFmpeg embebido (ver TRD §12.1).
- Manual de usuario.
- Manual técnico.
- Corrección de errores.

Criterio de salida:

- El sistema puede instalarse y utilizarse en otra computadora.

### Fase 9 / v0.2. Medios IA (imágenes + audio rápido)

Entregables:

- `ImageProvider` / `FalImageProvider` (fal.ai) y `PromptAssistant` (OpenRouter).
- `ImageService` / `ImageManager`, tabla `IMAGE_ASSET`, carpeta `images/{generated,library,thumbnails}/`.
- UI-013 Estudio de medios (Imagen / Audio rápido / Credenciales).
- RF-050..053 (imagen, prompt, asociación, biblioteca), RF-076 (miniatura), RF-077 (TTS rápido).
- RF-078 (video IA) **no** incluido — reservado fase 2 posterior.

Criterio de salida:

- Generar imagen por escena, miniatura y biblioteca; audio rápido TTS operativo; claves openrouter/fal en keyring.

---

## 3. Pruebas iniciales

### CP-001. Crear proyecto válido

**Resultado esperado:** Se crea la estructura de carpetas.

### CP-002. Crear proyecto duplicado

**Resultado esperado:** El sistema solicita otro nombre.

### CP-003. API key inválida

**Resultado esperado:** No se almacena y se muestra un error.

### CP-004. Generar audio

**Resultado esperado:** Se crea un archivo reproducible.

### CP-005. Texto vacío

**Resultado esperado:** No se realiza la solicitud.

### CP-006. Micrófono no disponible

**Resultado esperado:** Se informa al usuario.

### CP-007. Importar MP4 válido

**Resultado esperado:** Se muestra duración y resolución.

### CP-008. Archivo de video corrupto

**Resultado esperado:** Se rechaza el archivo.

### CP-009. Exportación normal

**Resultado esperado:** Se genera un MP4 válido.

### CP-010. Falta de espacio

**Resultado esperado:** La exportación no inicia.

### CP-011. Capturar pantalla o cámara

**Resultado esperado:** Archivo en `video/captured/` reproducible con preview previo.

### CP-012. Capturar región

**Resultado esperado:** Solo se graba el rectángulo seleccionado.

### CP-013. Capturar ventana

**Resultado esperado:** Solo se graba la ventana elegida.

### CP-014. Tres pistas de audio

**Resultado esperado:** Original + narración + música se mezclan; una 4.ª pista se rechaza.

### CP-015. Abrir desde carpeta de proyectos

**Resultado esperado:** El diálogo parte de la misma carpeta base que al crear.

---

## 4. Matriz de trazabilidad inicial

| Requisito | Pantalla | Flujo | Componente | Prueba |
|---|---|---|---|---|
| RF-001 | UI-002 | FL-001 | ProjectManager | CP-001 |
| RF-008 | UI-003 | FL-002 | ScriptManager | CP-002 |
| RF-011 | UI-003 | FL-002 | ScriptManager | — |
| RF-014 | UI-004 | FL-003 | VoiceProviderManager | CP-003 |
| RF-020 | UI-006 | FL-004 | VoiceProvider | CP-004 |
| RF-022 | UI-006 | FL-005 | VoiceProvider | CP-004 |
| RF-028/029/033 | UI-007 | FL-006 | AudioRecorder | CP-006 |
| RF-035/036/038 | UI-008 | FL-007 | AudioEditor | — |
| RF-042 | UI-009 | FL-008 | VideoManager | CP-007/CP-008 |
| RF-047 | UI-010 | FL-009 | MediaComposer | CP-009 |
| RF-049a | UI-010 | FL-009 | MediaComposer | — |
| RF-057 | UI-011 | FL-010 | ExportManager | CP-009/CP-010 |
| RF-063/064/065 | UI-009 | FL-008/011 | CaptureService | CP-011 |
| RF-067 | UI-009 | FL-008 | CaptureService | — |
| RF-068/069 | UI-009 | FL-011 | CaptureService | CP-012/CP-013 |
| RF-070..073 | UI-010 | FL-009/012 | MediaComposer | CP-014 |
| RF-002 / FL-013 | UI-001 | FL-013 | ProjectManager | CP-015 |

---

## 5. Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Cambios en las API | Alto | Crear capa de abstracción |
| Costos de proveedores | Medio | Mostrar estimación y límites |
| Complejidad de FFmpeg | Medio | Centralizar comandos |
| Archivos grandes | Alto | Procesamiento por partes |
| Interfaz congelada | Alto | Procesos en segundo plano |
| Pérdida de proyectos | Alto | Guardado automático |
| Audio desincronizado | Alto | Comparar duración |
| Diferencias entre codecs | Medio | Convertir a formatos estándar |
| Claves expuestas | Alto | Usar keyring |
| Alcance excesivo | Alto | Mantener el MVP limitado; ver visión 08 y RN-013 |

---

## 6. Versiones posteriores

### Ciclo 0.1b (en curso — MVP redefinido)

Ver `08_Vision_Producto_Redefinida.md` y Fase 7b. Incluye captura (pantalla/cámara/región/ventana), etiquetas de monitores y 3 pistas de audio.

### Versión 0.2 — Medios IA + cursos

**Primero — Medios IA (Fase 9 / activa):**

1. **Imágenes (RF-050..053)** — fal.ai + biblioteca `images/` + asociar a escena.
2. **Asistente de prompt (RF-051)** — OpenRouter.
3. **Miniatura generada (RF-076)** — portada del proyecto.
4. **Audio sencillo TTS (RF-077)** — OpenAI / ElevenLabs en UI-013.

**Después — Prioridad cursos y subtítulos:**

5. **Teleprompter (RF-074)** — guion visible al grabar cámara/voz.
6. **Plantilla de marca (RF-075)** — intro, outro y logo del curso.
7. Subtítulos (RF-054/055/056).
8. Transiciones básicas / ampliación de plantillas.

**Reservado fase 2 (no en 0.2 medios):** video IA (RF-078).

> La música instrumental de fondo pasa al MVP 0.1b (RF-072); 0.2 puede ampliar biblioteca musical.

### Versión 0.3

- Audio del sistema en captura (si no se cubrió en 0.1b).
- Mejoras de usabilidad en región/ventana.
- Exportar por escena/lección (útil para LMS).

### Versión 0.4

- Proveedores locales.
- Piper.
- Coqui TTS.
- Whisper para transcripción.

### Versión 0.5

- Video IA (RF-078) si no anticipado.
- Creación automática de escenas.
- Sugerencias visuales avanzadas basadas en el guion.
- Publicación asistida.
