# Guía rápida de uso (visión 0.1b)

**Proyecto:** VideoCreator IA  
**Versión:** 0.1b  
**Detalle de visión:** `08_Vision_Producto_Redefinida.md`

---

## Idea del producto

Crear un video narrado en una sola app:

**Guion → Voz → Video (importar o capturar) → Hasta 3 audios → Exportar MP4**

---

## Cómo crear un proyecto

1. Pulsa **Nuevo proyecto**.
2. Completa **Nombre**, **Carpeta** (por defecto la carpeta de proyectos) y descripción opcional.
3. Pulsa **Crear**.

---

## Cómo abrir un proyecto

1. Pulsa **Abrir proyecto**.
2. El diálogo parte de la **misma carpeta** donde se guardan los proyectos.
3. Elige la carpeta del proyecto (`project.json`) o la carpeta base para cargar varios.

---

## Cómo obtener el video

### Importar

1. Proyecto seleccionado → **Gestor de video** → **Importar video**.
2. Elige un MP4/MOV/MKV/AVI.
3. Queda en `video/imported/` y se puede reproducir.

### Capturar

1. En **Gestor de video**, elige fuente:
   - Pantalla (etiquetas tipo *Monitor 1 · 1920×1080 · Principal*).
   - Cámara.
   - Región (dibujar área) — ciclo 0.1b.
   - Ventana (elegir app) — ciclo 0.1b.
2. **Iniciar captura** → verás preview en vivo.
3. **Detener** → archivo en `video/captured/` listo para reproducir.

---

## Cómo montar el audio (máx. 3 pistas)

En **Composición**:

| Pista | Contenido |
|---|---|
| A | Audio original del video (on/off + volumen) |
| B | Narración (IA o micrófono) |
| C | Música instrumental (archivo + volumen) |

No se permite una cuarta pista.

---

## Exportar

Composición aceptada → **Exportar** → MP4.

---

## Dónde quedan los archivos

```text
projects/<nombre>/
├── project.json
├── script/guion.txt
├── audio/...
├── video/
│   ├── imported/
│   └── captured/
└── exports/
```

---

## Problemas frecuentes

| Síntoma | Qué revisar |
|---|---|
| Captura en negro / archivo vacío | Permiso de grabación de pantalla en Windows |
| Cámara no lista | Otra app la está usando |
| No se oye música | Volumen de pista C y que el archivo sea audio válido |
| FFmpeg / import metadatos | Ruta de FFmpeg en configuración (export y análisis) |
