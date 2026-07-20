# Diseño UI/UX

**Proyecto:** VideoCreator IA  
**Versión:** 0.1b  
**Estado:** Planificación actualizada (visión redefinida)

---

## 1. Objetivo

Definir una interfaz sencilla para usuarios sin experiencia avanzada en edición audiovisual.

El sistema deberá priorizar:

- Claridad.
- Pocos pasos.
- Controles visibles.
- Retroalimentación inmediata.
- Prevención de errores.
- Separación entre funciones básicas y avanzadas.

---

## 2. Estructura general

La ventana principal se dividirá en cuatro áreas:

```text
┌──────────────────────────────────────────────────────────────┐
│ Menú principal y acciones del proyecto                      │
├───────────────┬────────────────────────┬─────────────────────┤
│ Proyecto      │ Guion                  │ Configuración voz   │
│ y escenas     │ y contenido            │ y generación        │
├───────────────┴────────────────────────┴─────────────────────┤
│ Audio, video, reproducción y exportación                    │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. Pantallas propuestas

### UI-001. Pantalla de inicio

Elementos:

- Nuevo proyecto.
- Abrir proyecto.
- Proyectos recientes.
- Configuración.
- Ayuda.

### UI-002. Nuevo proyecto

Campos:

- Nombre.
- Descripción.
- Carpeta de almacenamiento.
- Formato preferido.
- Botón Crear.
- Botón Cancelar.

### UI-003. Editor de guion

Funciones:

- Escribir o pegar texto.
- Guardar.
- Dividir por párrafos.
- Crear escenas.
- Reordenar escenas.
- Contar palabras.
- Estimar duración.
- Marcar escenas pendientes o completadas.

### UI-004. Configuración de proveedores

Elementos:

- Lista de proveedores.
- Campo API key.
- Botón Validar.
- Estado de conexión.
- Modelo predeterminado.
- Voz predeterminada.
- Botón Eliminar credencial.

### UI-005. Selección de voces

Elementos:

- Proveedor.
- Modelo.
- Idioma.
- Voz.
- Muestra.
- Velocidad.
- Formato.
- Favoritos.

### UI-006. Generador de audio

Elementos:

- Lista de escenas.
- Estado de cada escena.
- Botón Generar selección.
- Botón Generar todo.
- Botón Cancelar.
- Barra de progreso.
- Reproductor.

### UI-007. Grabador de voz

Elementos:

- Micrófono.
- Nivel de entrada.
- Texto de la escena.
- Grabar.
- Pausar.
- Continuar.
- Detener.
- Repetir.
- Guardar toma.

### UI-008. Editor básico de audio

Elementos:

- Forma de onda.
- Selección de intervalo.
- Recortar.
- Dividir.
- Eliminar.
- Normalizar.
- Insertar pausa.
- Deshacer.

### UI-009. Gestor de video

Elementos:

- Origen del video: **Importar** | **Capturar**.
- Lista seleccionable de videos del proyecto.
- Captura:
  - Fuente: pantallas (etiqueta legible), cámaras, región, ventana.
  - Iniciar / Detener.
  - Temporizador.
  - Vista previa en vivo.
- Reproducción del video seleccionado (play / pausa / seek).
- Metadatos: duración, resolución, FPS, audio.
- Acciones RF-044..048.
- Abrir carpeta del archivo.

Archivos:

- `video/imported/` — importados.
- `video/captured/` — pantalla / cámara / región / ventana.

### UI-010. Composición

Elementos:

- Video principal.
- **Hasta 3 pistas de audio:**
  - Original del video (activar + volumen).
  - Narración (activar + volumen).
  - Música instrumental (añadir archivo + volumen).
- Advertencia si se intenta superar 3 pistas (RN-013).
- Vista previa de la mezcla.
- Sincronización / alternativas de duración.
- Pasar a exportación.

### UI-011. Exportación

Elementos:

- Nombre del archivo.
- Carpeta destino.
- Resolución.
- Orientación.
- Calidad.
- Botón Exportar.
- Progreso.
- Cancelar.

### UI-012. Configuración general

Opciones:

- Carpeta de proyectos.
- Carpeta temporal.
- Ruta de FFmpeg.
- Idioma.
- Guardado automático.
- Limpieza de temporales.
- Preferencias de audio.

### UI-013. Estudio de medios (v0.2)

Pantalla unificada para generación de medios del proyecto. Pestañas:

- **Imagen:** prompt (manual o asistido por OpenRouter) → generar con fal.ai → galería; asociar a escena o guardar en biblioteca.
- **Audio rápido:** TTS sencillo (OpenAI / ElevenLabs) sin pasar por el flujo completo de escenas (RF-077).
- **Credenciales medios:** API keys de OpenRouter y fal.ai (keyring; ocultas parcialmente).

Flujo principal: escribir o asistir prompt → generar → revisar en galería → asignar (escena / miniatura / biblioteca).

---

## 4. Navegación

Flujo principal:

```text
Inicio
  ↓
Proyecto
  ↓
Guion
  ↓
Audio generado o grabado
  ↓
Video
  ↓
Medios (UI-013, opcional v0.2)
  ↓
Composición
  ↓
Exportación
```

---

## 5. Estados visuales

Cada escena podrá mostrar uno de los siguientes estados en la interfaz (se muestra entre paréntesis el identificador de dominio equivalente usado por el backend, ver doc 05 §8):

- Sin texto (`Empty`).
- Lista para generar (`Ready`).
- Generando (`Generating`).
- Audio generado (`Generated`).
- Grabación disponible (`Recorded`).
- Requiere revisión (`ReviewRequired`).
- Aprobada (`Approved`).
- Error (`Error`).

---

## 6. Mensajes de interfaz

Los mensajes deberán ser claros y orientados a la acción.

Ejemplo correcto:

> No fue posible generar el audio porque la API key no es válida. Revise la credencial en Configuración.

Ejemplo incorrecto:

> Error 401.

---

## 7. Principios de usabilidad

- No mostrar opciones avanzadas por defecto.
- Mantener las acciones principales siempre visibles.
- Confirmar eliminaciones.
- Guardar automáticamente.
- Permitir deshacer cuando sea posible.
- Mostrar progreso en tareas largas.
- No bloquear toda la aplicación durante una exportación.
- Conservar versiones anteriores de audios regenerados.

---

## 8. Accesibilidad básica

- Tamaños de fuente legibles.
- Buen contraste.
- Navegación por teclado.
- Etiquetas claras.
- Estados que no dependan únicamente del color.
- Tooltips en funciones técnicas.
