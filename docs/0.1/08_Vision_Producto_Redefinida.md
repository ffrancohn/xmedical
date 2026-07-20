# Visión de producto redefinida

**Proyecto:** VideoCreator IA  
**Versión documento:** 0.1b  
**Fecha:** 2026-07-17  
**Estado:** Aprobado para planificación  

---

## 1. Decisión

VideoCreator IA se redefine como aplicación de escritorio para **apoyar la creación de cursos en video** (clases, cápsulas, lecciones narradas) de punta a punta:

1. Preparar guion y voz (IA o micrófono).  
2. Obtener el video (**importar** o **capturar**).  
3. Montar hasta **3 pistas de audio**.  
4. Componer, previsualizar y exportar MP4.

No es un editor profesional multipista (CapCut/Premiere). Sí es un **creador/capturador sencillo** orientado a producir material de curso, no solo un ensamblador de archivos ajenos.

---

## 2. Decisiones de alcance (acordadas)

| Tema | Decisión |
|---|---|
| Importar video | Sí (si el usuario ya tiene el archivo) |
| Capturar video | Sí: pantalla completa, cámara, **región** y **ventana** |
| Etiquetas de pantallas | Legibles (resolución, principal, posición) |
| Pistas de audio | Máximo **3**: (1) original del video opcional, (2) narración, (3) música instrumental |
| Música | Solo instrumental / archivo de audio; sin editor DAW |
| Timeline profesional | Fuera de alcance |
| **Medios IA (imágenes + miniatura + audio rápido)** | **v0.2 activo** (RF-050..053, RF-076, RF-077; OpenRouter + fal.ai) |
| Subtítulos | v0.2 posterior (RF-054..056) |
| **Teleprompter** | **Prioridad cursos → v0.2 posterior** (RF-074) |
| **Plantilla intro/outro + logo** | **Prioridad cursos → v0.2 posterior** (RF-075) |
| Video IA | Reservado fase 2 (RF-078) |

---

## 3. Modelo mental del usuario

```text
Proyecto
 ├── Guion / escenas
 ├── Video  ← Importar  |  Capturar (pantalla | cámara | región | ventana)
 ├── Audio (hasta 3 pistas)
 │    ├── Pista A: audio original del video (on/off + volumen)
 │    ├── Pista B: narración (IA o mic)
 │    └── Pista C: música instrumental (archivo + volumen)
 └── Medios (v0.2)  ← Imágenes fal.ai | Miniatura | Audio rápido TTS
           ↓
      Composición + vista previa
           ↓
      Exportar MP4
```

---

## 4. Matriz de orígenes

| Origen video | Descripción | Prioridad ciclo |
|---|---|---|
| Importar | MP4/MOV/MKV/AVI existente | MVP redefinido |
| Pantalla completa | Monitor seleccionado (etiqueta clara) | MVP redefinido |
| Cámara | Webcam / USB | MVP redefinido |
| Región | Rectángulo dentro de una pantalla | MVP redefinido (0.1b) |
| Ventana | Ventana de aplicación (HWND) | MVP redefinido (0.1b) |

| Origen audio | Pista | Prioridad |
|---|---|---|
| Del video | A (original) | Ya en RF-044..046 |
| IA / micrófono | B (narración) | Ya en RF-020..034 |
| Archivo música | C (instrumental) | Nuevo RF-072 |

---

## 5. Fuera de alcance (cerrar scope)

- Multipista ilimitada / timeline tipo NLE.  
- Efectos visuales, color grading, transiciones complejas (salvo las de 0.2).  
- Multicámara sincronizada.  
- Publicación en redes.  
- Generación automática del video completo por IA.  
- Más de 3 pistas de audio.

---

## 6. Trazabilidad

Detalle normativo en:

- PRD §1–§12 actualizado (RF-063..072, RN nuevas, MVP).  
- TRD: `CaptureService` + composición a 3 pistas.  
- UI-009 / UI-010.  
- FL-008 ampliado, FL-011, FL-012, FL-013.  
- Plan: Fase 8 / ciclo **0.1b** = cierre del MVP redefinido.

---

## 7. Criterio de éxito del MVP redefinido

El usuario puede, en una sola app:

1. Crear proyecto y guion.  
2. Generar o grabar narración.  
3. **Importar o capturar** el video (incl. región/ventana).  
4. Activar hasta 3 pistas (original + narración + música).  
5. Previsualizar y exportar un MP4 usable.

---

## 8. Prioridades post-MVP (v0.2)

Orden sugerido de desarrollo tras cerrar 0.1b:

1. **Medios IA (activo):** imágenes fal.ai (RF-050..053), asistente OpenRouter (RF-051), miniatura (RF-076), audio rápido TTS (RF-077); UI-013.
2. **Teleprompter (RF-074)** — mostrar el guion/escena con desplazamiento al grabar cámara o narración.
3. **Plantilla de marca (RF-075)** — intro, outro y logo reutilizables por curso/proyecto.
4. Subtítulos (RF-054..056).
5. **Video IA (RF-078)** — reservado fase 2 (posterior a medios).
