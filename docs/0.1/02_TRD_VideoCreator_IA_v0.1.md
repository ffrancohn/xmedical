# Documento de Requerimientos Técnicos (TRD)

**Proyecto:** VideoCreator IA  
**Versión:** 0.1b  
**Estado:** Planificación actualizada (visión redefinida)

---

## 1. Objetivo técnico

Definir la arquitectura, tecnologías, componentes, integraciones y restricciones técnicas necesarias para implementar VideoCreator IA como una aplicación de escritorio modular y extensible.

---

## 2. Arquitectura propuesta

La aplicación utilizará una arquitectura modular en capas:

```text
Interfaz de usuario
        │
        ▼
Servicios de aplicación
        │
        ├── Gestión de proyectos
        ├── Gestión de guiones
        ├── Generación de voz
        ├── Grabación de voz
        ├── Edición de audio
        ├── Procesamiento de video
        ├── Captura de video (pantalla / cámara / región / ventana)
        ├── Composición (hasta 3 pistas de audio)
        └── Exportación
        │
        ▼
Infraestructura
        ├── SQLite
        ├── Sistema de archivos
        ├── Keyring
        ├── FFmpeg / FFprobe
        ├── Qt Multimedia (captura, preview, reproducción)
        ├── OpenAI
        └── ElevenLabs
```

---

## 3. Tecnologías propuestas

| Área | Tecnología |
|---|---|
| Lenguaje | Python 3.12 o versión estable compatible |
| Interfaz gráfica | PySide6 |
| Base de datos | SQLite |
| Audio y video | FFmpeg y FFprobe (análisis, mux, export, recorte) |
| Captura / preview | Qt Multimedia (`QScreenCapture`, `QCamera`, `QMediaPlayer`, `QVideoWidget`) |
| Operaciones simples de audio | Pydub |
| Grabación de voz | sounddevice y soundfile |
| Reproducción | Qt Multimedia |
| Región / ventana (Windows) | Qt + APIs nativas / enumeración de ventanas según diseño de `CaptureService` |
| Credenciales | Python keyring / Windows Credential Manager |
| Medios IA (v0.2) | OpenRouter (asistente de prompt), fal.ai (imágenes) |
| Pruebas | Pytest |
| Empaquetado | PyInstaller |
| Alternativa de empaquetado | Nuitka |

---

## 4. Componentes principales

### 4.1 ProjectManager

Responsable de:

- Crear proyectos.
- Abrir proyectos.
- Guardar cambios.
- Administrar carpetas.
- Duplicar proyectos.
- Recuperar proyectos interrumpidos.

### 4.2 ScriptManager

Responsable de:

- Guardar el guion.
- Dividir escenas.
- Reordenar escenas.
- Calcular duración estimada.
- Detectar cambios pendientes.

### 4.3 VoiceProviderManager

Responsable de:

- Registrar proveedores.
- Validar credenciales.
- Consultar modelos.
- Consultar voces.
- Solicitar generación de audio.
- Normalizar respuestas de distintos proveedores.

### 4.4 AudioRecorder

Responsable de:

- Detectar micrófonos.
- Iniciar grabación.
- Pausar.
- Continuar.
- Detener.
- Guardar archivos WAV.

### 4.5 AudioEditor

Responsable de:

- Recortar.
- Dividir.
- Unir.
- Normalizar volumen.
- Insertar pausas.
- Aplicar fundidos básicos.

### 4.6 VideoManager

Responsable de:

- Importar videos.
- Consultar duración.
- Obtener resolución.
- Obtener FPS.
- Recortar.
- Silenciar audio.
- Validar formatos.
- Registrar videos capturados en el proyecto.
- Exponer reproducción y metadatos a la UI.

### 4.6b CaptureService (nuevo — RF-063..069)

Responsable de:

- Enumerar pantallas con etiquetas legibles (RF-067).
- Enumerar cámaras.
- Capturar pantalla completa (RF-063).
- Capturar cámara (RF-064).
- Capturar región rectangular (RF-068).
- Capturar ventana de aplicación (RF-069).
- Vista previa en vivo (RF-065).
- Guardar el resultado en `video/captured/`.

Implementación de referencia: `infrastructure/capture` (Qt Multimedia); región/ventana pueden apoyarse en APIs de Windows cuando Qt no baste.

### 4.7 MediaComposer

Responsable de:

- Combinar video con hasta **3 pistas de audio** (RF-070..073):
  - Pista A: audio original del video (on/off + volumen).
  - Pista B: narración.
  - Pista C: música instrumental.
- Ajustar duraciones.
- Validar sincronización audio/video.
- Crear vistas previas.

### 4.8 ExportManager

Responsable de:

- Construir comandos FFmpeg.
- Ejecutar exportaciones.
- Mostrar progreso.
- Cancelar procesos.
- Registrar errores.
- Validar el archivo final.

### 4.9 SettingsManager

Responsable de:

- Leer y escribir preferencias globales.
- Administrar carpeta de proyectos y carpeta temporal.
- Idioma de la interfaz.
- Configuración de guardado automático.
- Ruta de FFmpeg y limpieza de temporales.
- Exponer la configuración al resto de servicios.

### 4.10 ImageManager / ImageService (v0.2 medios)

Responsable de:

- Generar imágenes vía `FalImageProvider` (fal.ai).
- Asistir y refinar prompts vía `PromptAssistant` (OpenRouter).
- Asociar imágenes a escenas y gestionar biblioteca / miniaturas.
- Persistir `IMAGE_ASSET` y actualizar `PROJECT.thumbnail_path`.
- Exponer TTS rápido (RF-077) reutilizando `VoiceProvider` (OpenAI / ElevenLabs).

> **Nota de nomenclatura:** Los componentes en §4 (`*Manager`) representan la capa de **aplicación/servicios** y se corresponden con los `*Service` descritos en el documento 05 (Backend). Un `Manager` corresponde a un `Service` de la capa de dominio. Esta diferencia de suffijo es intencional y refleja la separación de capas, no duplicación de responsabilidades.

---

## 5. Interfaz común para proveedores

```python
from abc import ABC, abstractmethod
from pathlib import Path


class VoiceProvider(ABC):

    @abstractmethod
    def validate_credentials(self) -> bool:
        """Valida las credenciales configuradas."""

    @abstractmethod
    def list_models(self) -> list[dict]:
        """Obtiene los modelos disponibles."""

    @abstractmethod
    def list_voices(self) -> list[dict]:
        """Obtiene las voces disponibles."""

    @abstractmethod
    def generate_speech(
        self,
        text: str,
        voice_id: str,
        model_id: str,
        output_path: Path,
        **options
    ) -> Path:
        """Genera un archivo de audio."""
```

Implementaciones iniciales (v0.1):

```text
VoiceProvider
├── OpenAIVoiceProvider
└── ElevenLabsVoiceProvider
```

> `LocalVoiceProvider` se prevé para la versión 0.4 (Piper / Coqui TTS) y no formará parte del MVP.

### 5.1 Proveedores de medios (v0.2)

```text
ImageProvider
└── FalImageProvider

PromptAssistant
└── OpenRouterPromptAssistant
```

- `ImageProvider`: contrato para generar imágenes (prompt → archivo + metadatos).
- `FalImageProvider`: implementación contra fal.ai.
- `PromptAssistant`: refina o sugiere prompts a partir del guion/escena vía OpenRouter.
- Claves en keyring: `openrouter` y `fal` (además de las de voz existentes).

---

## 6. Estructura sugerida del código

```text
videocreator_ia/
├── app.py
├── config/
├── domain/
│   ├── models/
│   └── services/
├── application/
│   ├── projects/
│   ├── scripts/
│   ├── audio/
│   ├── video/
│   ├── media/          # ImageManager (v0.2)
│   └── export/
├── infrastructure/
│   ├── database/
│   ├── providers/      # VoiceProvider + FalImageProvider + OpenRouter
│   ├── ffmpeg/
│   ├── storage/
│   └── security/       # keyring: openai, elevenlabs, openrouter, fal
├── ui/
│   ├── windows/
│   ├── dialogs/
│   ├── widgets/
│   └── resources/
├── tests/
└── requirements.txt
```

---

## 7. Requisitos de seguridad

- No almacenar API keys en texto plano.
- No incluir credenciales en archivos JSON.
- No escribir claves completas en logs.
- Mostrar las claves parcialmente ocultas.
- Utilizar el almacén seguro del sistema operativo.
- Permitir eliminar credenciales.
- Informar qué contenido se envía a servicios externos.
- Claves de medios (v0.2): OpenRouter y fal.ai en keyring, nunca en JSON ni logs completos.

---

## 8. Procesamiento en segundo plano

Las siguientes operaciones deberán ejecutarse sin bloquear la interfaz:

- Generación de audio.
- Generación de imágenes y asistencia de prompt (v0.2).
- Descarga de resultados.
- Análisis con FFprobe.
- Conversión de archivos.
- Generación de vistas previas.
- Exportación final.

Se recomienda utilizar `QThread`, `QThreadPool` o procesos separados según la carga.

---

## 9. Requisitos de compatibilidad

### Sistema operativo inicial

- Windows 10.
- Windows 11.

> **Nota de multiplataforma:** La pila tecnológica (Python, PySide6, FFmpeg, keyring) es compatible con Linux y macOS, pero la v0.1 **no se probará, empacará ni soportará oficialmente** en esos sistemas. No se bloqueará su ejecución, pero no se garantiza comportamiento correcto.

### Formatos de entrada

- Audio: WAV, MP3, M4A.
- Video: MP4, MOV, MKV.
- Texto: TXT y contenido pegado.

> Imágenes (PNG, JPG) se incorporarán en v0.2.

### Formatos de salida

- Audio: WAV y MP3.
- Video: MP4 con H.264 y AAC.

> Subtítulos SRT se incorporarán en v0.2.

---

## 10. Manejo de errores

El sistema deberá contemplar:

- API key inválida.
- Falta de conexión.
- Tiempo de espera agotado.
- Límite de uso alcanzado.
- Texto vacío o demasiado largo.
- Micrófono no disponible.
- Archivo multimedia corrupto.
- FFmpeg no disponible.
- Falta de espacio.
- Falta de permisos.
- Fallo durante la exportación.

Cada error deberá incluir:

- Descripción entendible.
- Posible causa.
- Acción recomendada.
- Detalle técnico opcional.

---

## 11. Registro de actividad

Los logs deberán registrar:

- Inicio y cierre de la aplicación.
- Apertura y guardado de proyectos.
- Proveedor utilizado.
- Inicio y fin de procesos.
- Errores técnicos.
- Comandos FFmpeg sin credenciales.
- Tiempo de ejecución.

No deberán incluir:

- API keys.
- Guiones completos, salvo que el usuario active depuración.
- Datos personales innecesarios.

---

## 12. Empaquetado y distribución

La primera versión podrá distribuirse como:

- Ejecutable para Windows.
- Carpeta portable.
- Instalador opcional.

El instalador deberá comprobar:

- Compatibilidad del sistema.
- Disponibilidad de FFmpeg.
- Permisos de escritura.
- Dependencias requeridas.

### 12.1 Estrategia para FFmpeg

FFmpeg no se exigirá como dependencia externa del usuario. En v0.1 se aplicará la siguiente estrategia:

1. **FFmpeg embebido:** se empaquetará un binario de FFmpeg dentro del instalador y de la carpeta portable.
2. **Verificación en arranque:** la aplicación comprobará la integridad y disponibilidad del binario embebido al iniciar.
3. **Anulación manual:** el usuario podrá indicar una ruta propia de FFmpeg en Configuración general, lo que sustituirá al embebido.
4. **Descarga en primer arranque (opcional):** si se omite el binario embebido por tamaño, se ofrecerá descarga automática desde un mirror oficial verificado.
