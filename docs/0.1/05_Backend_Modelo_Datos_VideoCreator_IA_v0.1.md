# Diseño del Backend y Modelo de Datos

**Proyecto:** VideoCreator IA  
**Versión:** 0.1  
**Estado:** Borrador inicial  

---

## 1. Objetivo

Definir la organización interna del sistema, sus servicios, entidades, almacenamiento y relaciones de datos.

---

## 2. Entidades principales

- Proyecto.
- Escena.
- Audio.
- Video.
- Imagen (asset de medios: escena, miniatura o biblioteca).
- Configuración de proveedor.
- Exportación.

---

## 3. Modelo de datos

### 3.1 Tabla `PROJECT`

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER | Identificador |
| name | TEXT | Nombre |
| description | TEXT | Descripción |
| folder_path | TEXT | Carpeta |
| status | TEXT | Estado |
| thumbnail_path | TEXT | Ruta opcional a miniatura del proyecto |
| created_at | DATETIME | Creación |
| updated_at | DATETIME | Modificación |

### 3.2 Tabla `SCENE`

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER | Identificador |
| project_id | INTEGER | Proyecto |
| scene_number | INTEGER | Orden |
| title | TEXT | Título |
| text | TEXT | Guion |
| status | TEXT | Estado |
| estimated_duration | REAL | Duración estimada |
| words_count | INTEGER | Cantidad de palabras |
| chars_count | INTEGER | Cantidad de caracteres |
| active_audio_id | INTEGER | Audio activo |

### 3.3 Tabla `AUDIO_ASSET`

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER | Identificador |
| project_id | INTEGER | Proyecto |
| scene_id | INTEGER | Escena |
| audio_type | TEXT | IA o grabación |
| provider | TEXT | Proveedor |
| model_id | TEXT | Modelo |
| voice_id | TEXT | Voz |
| file_path | TEXT | Ruta |
| duration | REAL | Duración |
| status | TEXT | Estado |
| version_number | INTEGER | Número de versión (1, 2, ...) |
| previous_version_id | INTEGER | Referencia al audio previo (NULL si es la primera versión) |
| take_number | INTEGER | Número de toma (solo grabaciones; NULL en IA) |
| created_at | DATETIME | Fecha |

### 3.4 Tabla `VIDEO_ASSET`

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER | Identificador |
| project_id | INTEGER | Proyecto |
| file_path | TEXT | Ruta |
| duration | REAL | Duración |
| width | INTEGER | Ancho |
| height | INTEGER | Alto |
| fps | REAL | Fotogramas |
| has_audio | BOOLEAN | Tiene audio |

### 3.5 Tabla `PROVIDER_CONFIG`

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER | Identificador |
| provider_name | TEXT | Proveedor |
| credential_reference | TEXT | Referencia segura |
| default_model | TEXT | Modelo |
| default_voice | TEXT | Voz |
| enabled | BOOLEAN | Estado |

### 3.6 Tabla `EXPORT`

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER | Identificador |
| project_id | INTEGER | Proyecto |
| file_path | TEXT | Archivo |
| resolution | TEXT | Resolución |
| aspect_ratio | TEXT | Relación / orientación |
| quality | TEXT | Calidad (p. ej. alta, media, baja) |
| status | TEXT | Estado |
| created_at | DATETIME | Fecha |

### 3.7 Tabla `IMAGE_ASSET` (v0.2 medios)

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER | Identificador |
| project_id | INTEGER | Proyecto |
| file_path | TEXT | Ruta del archivo |
| prompt | TEXT | Prompt usado en la generación |
| provider | TEXT | Proveedor (p. ej. fal) |
| kind | TEXT | `scene` \| `thumbnail` \| `library` |
| scene_id | INTEGER | Escena asociada (NULL si no aplica) |
| width | INTEGER | Ancho |
| height | INTEGER | Alto |
| created_at | DATETIME | Fecha |

---

## 4. Relaciones

```text
PROJECT
├── SCENE
│   ├── AUDIO_ASSET
│   └── IMAGE_ASSET (opcional, kind=scene)
├── VIDEO_ASSET
├── IMAGE_ASSET
└── EXPORT
```

Reglas:

- Un proyecto tiene muchas escenas.
- Una escena puede tener varias versiones de audio.
- Solo una versión de audio será activa.
- Cada versión de audio enlaza con su versión anterior (`previous_version_id`).
- Un proyecto puede contener varios videos.
- Un proyecto puede tener múltiples imágenes (`IMAGE_ASSET`) y un `thumbnail_path` opcional.
- Un proyecto puede tener múltiples exportaciones.

---

## 5. Estructura de carpetas del proyecto

```text
projects/
└── nombre_proyecto/
    ├── project.json
    ├── script/
    │   └── guion.txt
    ├── audio/
    │   ├── generated/
    │   ├── recordings/
    │   ├── edited/
    │   └── final/
    ├── video/
    │   ├── imported/
    │   ├── captured/
    │   └── edited/
    ├── images/
    │   ├── generated/
    │   ├── library/
    │   └── thumbnails/
    ├── temp/
    ├── exports/
    └── logs/
```

---

## 6. Convención de nombres

```text
scene_001_openai_voice_01.mp3
scene_002_elevenlabs_voice_03.mp3
scene_003_recording_take_01.wav
narration_final.wav
video_preview.mp4
video_final_1080p.mp4
```

---

## 7. Servicios internos

### ProjectService

- Crear proyecto.
- Abrir proyecto.
- Guardar.
- Duplicar.
- Eliminar.
- Recuperar.

### SceneService

- Crear escena.
- Editar.
- Eliminar.
- Reordenar.
- Calcular duración.
- Aprobar escena.

### ProviderService

- Validar credenciales.
- Consultar modelos.
- Consultar voces.
- Generar audio.

### AudioService

- Grabar.
- Recortar.
- Dividir.
- Unir.
- Normalizar.

### VideoService

- Analizar archivo.
- Importar.
- Recortar.
- Silenciar.
- Convertir.

### CompositionService

- Combinar medios.
- Ajustar duraciones.
- Validar sincronización audio/video.
- Crear vista previa.

### ImageService (v0.2 medios)

- Generar imagen (fal.ai).
- Asistir prompt (OpenRouter).
- Asociar imagen a escena.
- Gestionar biblioteca y miniaturas.
- Persistir `IMAGE_ASSET` y `PROJECT.thumbnail_path`.

### ExportService

- Validar configuración.
- Ejecutar FFmpeg.
- Informar progreso.
- Cancelar.
- Validar salida.

---

## 8. Estados sugeridos

> **Convención de estados:** Los identificadores de dominio se almacenan en inglés. La interfaz los presenta traducidos al idioma del usuario; el mapeo se documenta en el doc 03 §5.

### Proyecto

### Escena

- Empty.
- Ready.
- Generating.
- Generated.
- Recorded.
- ReviewRequired.
- Approved.
- Error.

### Exportación

- Pending.
- Processing.
- Completed.
- Cancelled.
- Failed.
