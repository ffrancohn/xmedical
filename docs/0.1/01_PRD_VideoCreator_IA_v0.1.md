# Documento de Requerimientos del Producto (PRD)

**Proyecto:** VideoCreator IA  
**Versión:** 0.1b (producto redefinido)  
**Estado:** Planificación aprobada  
**Plataforma inicial:** Windows  
**Tipo de solución:** Aplicación de escritorio  
**Visión:** ver `08_Vision_Producto_Redefinida.md`

---

## 1. Introducción

VideoCreator IA será una aplicación de escritorio sencilla para **crear videos narrados de punta a punta**: escribir o pegar un guion, generar o grabar la narración, **obtener el video importándolo o capturándolo** (pantalla, cámara, región o ventana), montar hasta **tres pistas de audio** (original del video, narración y música instrumental) y exportar un MP4.

La aplicación permitirá escribir o pegar un guion, seleccionar un proveedor de generación de voz, elegir una voz, generar archivos de audio, grabar la voz del usuario, realizar correcciones básicas de audio, **importar o capturar video**, componer audio y video, y exportar.

El sistema no pretende convertirse en un editor profesional comparable con CapCut, Adobe Premiere o DaVinci Resolve. Su finalidad será facilitar la **producción básica** del video narrado (incluido capturar el material visual) y generar una primera versión exportable.

---

## 2. Objetivo general

Desarrollar una aplicación de escritorio que facilite la creación de videos narrados a partir de texto, audio generado mediante inteligencia artificial, grabaciones de voz, **video importado o capturado**, y una mezcla simple de hasta tres pistas de audio.

---

## 3. Objetivos específicos

La aplicación deberá permitir:

- Crear y administrar proyectos de video.
- Escribir o pegar un guion.
- Dividir el guion en párrafos o escenas.
- Configurar proveedores de generación de voz.
- Guardar de forma segura las API keys.
- Consultar las voces disponibles.
- Generar audio a partir del texto.
- Escuchar y revisar los audios generados.
- Regenerar fragmentos individuales.
- Grabar la voz del usuario.
- Realizar edición básica de audio.
- **Importar archivos de video.**
- **Capturar video** (pantalla completa, cámara, región rectangular, ventana).
- **Identificar pantallas de forma legible** (resolución, principal, posición).
- **Montar hasta 3 pistas de audio** (original, narración, música instrumental).
- Unir / componer audio y video con vista previa.
- Exportar el resultado en formato MP4.

---

## 4. Problema que se desea resolver

La creación de videos narrados normalmente requiere utilizar varias herramientas distintas:

- Un editor de texto para preparar el guion.
- Una plataforma de inteligencia artificial para generar la voz.
- Un programa para grabar audio.
- Un editor para limpiar o recortar el audio.
- Una herramienta para grabar pantalla o cámara.
- Una aplicación para unir el audio y el video.
- Otra herramienta para generar subtítulos.

La aplicación propuesta concentrará estas tareas básicas en una única herramienta, **incluyendo la captura del video** cuando el usuario no tenga ya un archivo.

---

## 5. Usuarios objetivo

- Creadores de contenido.
- Docentes.
- Pastores y líderes religiosos.
- Capacitadores.
- Estudiantes.
- Personas que producen videos educativos.
- Usuarios sin experiencia avanzada en edición audiovisual.

---

## 6. Alcance inicial (MVP redefinido 0.1b)

La versión objetivo permitirá:

- Crear proyectos.
- Escribir y guardar guiones.
- Dividir el guion por escenas.
- Configurar OpenAI y ElevenLabs.
- Seleccionar proveedor, modelo y voz.
- Generar audio por escenas.
- Reproducir los audios.
- Regenerar escenas individuales.
- Grabar audio desde un micrófono.
- Recortar el inicio y final de un audio.
- Unir varios fragmentos de narración.
- **Importar un video.**
- **Capturar pantalla completa, cámara, región o ventana**, con vista previa en vivo.
- **Etiquetar monitores de forma comprensible.**
- **Montar hasta 3 pistas de audio:** original del video, narración, música instrumental.
- Ajustar volúmenes por pista.
- Previsualizar la composición.
- Exportar el video en MP4.

---

## 7. Fuera del alcance inicial

La primera versión no incluirá:

- Edición profesional multipista / timeline ilimitado (máximo 3 pistas de audio).
- Corrección avanzada de color.
- Efectos visuales complejos.
- Animaciones avanzadas.
- Seguimiento de objetos.
- Edición multicámara.
- Eliminación profesional de ruido.
- Clonación de voz.
- Publicación automática en redes sociales.
- Edición colaborativa en línea.
- Armar presentaciones desde imágenes (diferido; fuera de la fase medios v0.2).
- Generación e inserción de subtítulos (diferido a v0.2 posterior; RF-054..056).
- Teleprompter y plantillas intro/outro/logo (prioridad cursos → v0.2 posterior; RF-074/075).
- Generación de video completo mediante IA (reservado fase 2; RF-078).
- Audio del sistema en captura (v0.3 si no se anticipa).

**Entra en v0.2 medios (activo):** imagen por escena (fal.ai), asistente de prompt (OpenRouter), biblioteca `images/`, miniatura generada (RF-076), audio sencillo TTS rápido (RF-077).

---

## 8. Flujo general de uso

1. El usuario crea un proyecto.
2. Escribe o pega un guion.
3. Divide el contenido en escenas o párrafos.
4. Selecciona el proveedor de voz.
5. Selecciona el modelo y la voz.
6. Genera el audio (o graba con micrófono).
7. Revisa cada fragmento.
8. Corrige o regenera los fragmentos necesarios.
9. **Importa o captura** el video (pantalla / cámara / región / ventana).
10. Configura hasta 3 pistas de audio (original, narración, música).
11. Une / compone y revisa la vista previa.
12. Exporta el archivo MP4.
13. Opcionalmente continúa la edición en CapCut u otra herramienta.

---

## 9. Requerimientos funcionales

### 9.1 Gestión de proyectos

- **RF-001:** Crear proyecto.
- **RF-002:** Abrir proyecto.
- **RF-003:** Guardar proyecto.
- **RF-004:** Duplicar proyecto.
- **RF-005:** Eliminar proyecto.

### 9.2 Gestión del guion

- **RF-006:** Escribir o pegar texto.
- **RF-007:** Guardar el guion.
- **RF-008:** Dividir el texto en escenas.
- **RF-009:** Editar escenas.
- **RF-010:** Reordenar escenas.
- **RF-011:** Contar palabras y caracteres.

### 9.3 Configuración de proveedores

- **RF-012:** Registrar proveedor.
- **RF-013:** Registrar API key.
- **RF-014:** Validar API key.
- **RF-015:** Almacenar credenciales de forma segura.
- **RF-016:** Consultar modelos.
- **RF-017:** Consultar voces.
- **RF-018:** Escuchar muestra.
- **RF-019:** Guardar configuración predeterminada.

### 9.4 Generación de voz

- **RF-020:** Generar audio de una escena.
- **RF-021:** Generar todo el guion.
- **RF-022:** Regenerar una escena.
- **RF-023:** Cambiar de voz.
- **RF-024:** Reproducir audio.
- **RF-025:** Detener generación.
- **RF-026:** Mostrar progreso.
- **RF-027:** Manejar límites de texto.

### 9.5 Grabación de voz

- **RF-028:** Seleccionar micrófono.
- **RF-029:** Grabar audio.
- **RF-030:** Pausar grabación.
- **RF-031:** Detener grabación.
- **RF-032:** Reproducir grabación.
- **RF-033:** Repetir grabación.
- **RF-034:** Mostrar guion durante la grabación.

### 9.6 Edición básica de audio

- **RF-035:** Recortar inicio y final.
- **RF-036:** Dividir audio.
- **RF-037:** Eliminar fragmento.
- **RF-038:** Unir audios.
- **RF-039:** Normalizar volumen.
- **RF-040:** Insertar pausas.
- **RF-041:** Aplicar entrada y salida gradual.

### 9.7 Gestión de video

- **RF-042:** Importar video.
- **RF-043:** Reproducir video.
- **RF-044:** Silenciar audio original.
- **RF-045:** Mantener audio original.
- **RF-046:** Ajustar volumen del audio original.
- **RF-047:** Asociar audio al video.
- **RF-048:** Recortar video.
- **RF-049:** Ajustar duración.
- **RF-049a:** Validar la sincronización entre la duración de la narración y la del video antes de exportar.

> **Reservados (no implementados en la fase medios v0.2):** RF-054..056 (subtítulos), RF-074/075 (teleprompter, plantilla de marca). RF-078 (video IA) queda reservado para una fase 2 posterior.

### 9.7b Captura de video (MVP redefinido)

- **RF-063:** Capturar pantalla completa.
- **RF-064:** Capturar cámara.
- **RF-065:** Vista previa en vivo durante la captura.
- **RF-066:** Reproducir video del proyecto tras captura o importación.
- **RF-067:** Etiquetar pantallas de forma legible (resolución, monitor principal, posición relativa).
- **RF-068:** Capturar región rectangular de una pantalla.
- **RF-069:** Capturar una ventana de aplicación concreta.

### 9.7c Mezcla de audio sobre video (máx. 3 pistas)

- **RF-070:** Añadir pista de narración al video (IA o micrófono).
- **RF-071:** Mezclar audio original del video con narración (volúmenes independientes).
- **RF-072:** Añadir pista de música instrumental (archivo) con control de volumen.
- **RF-073:** Limitar la composición a un máximo de 3 pistas de audio simultáneas (original, narración, música).

### 9.8 Exportación

- **RF-057:** Exportar a MP4.
- **RF-058:** Seleccionar resolución.
- **RF-059:** Seleccionar orientación.
- **RF-060:** Mostrar progreso de exportación.
- **RF-061:** Cancelar exportación.
- **RF-062:** Abrir archivo generado.

### 9.9 Reservados v0.2 — prioridad cursos (posteriores a medios)

- **RF-074:** Teleprompter (mostrar guion/escena con desplazamiento al grabar).
- **RF-075:** Plantilla de marca (intro, outro y logo reutilizables).
- **RF-054:** Generar subtítulos (reservado).
- **RF-055:** Editar / sincronizar subtítulos (reservado).
- **RF-056:** Exportar / incrustar subtítulos (reservado).

### 9.10 Generación de medios (v0.2)

Proveedores: **OpenRouter** (asistente de prompt) y **fal.ai** (imágenes). Audio rápido reutiliza OpenAI / ElevenLabs existentes.

- **RF-050:** Generar imagen con fal.ai a partir de un prompt.
- **RF-051:** Asistente de prompt con OpenRouter (refinar o sugerir prompts desde el guion/escena).
- **RF-052:** Asociar una imagen generada a una escena.
- **RF-053:** Biblioteca de imágenes del proyecto (`images/`: generated, library, thumbnails).
- **RF-076:** Miniatura generada del proyecto (portada para LMS / catálogo; `kind=thumbnail`).
- **RF-077:** Audio sencillo / rápido TTS (generación puntual reutilizando proveedores OpenAI o ElevenLabs).
- **RF-078:** Generación de video con IA — **reservado fase 2** (no implementar en v0.2 medios).

---

## 10. Requerimientos no funcionales

- **RNF-001:** Facilidad de uso.
- **RNF-002:** Procesamiento en segundo plano.
- **RNF-003:** Seguridad de credenciales.
- **RNF-004:** Disponibilidad local.
- **RNF-005:** Recuperación y guardado automático.
- **RNF-006:** Compatibilidad con Windows 10 y 11.
- **RNF-007:** Extensibilidad para nuevos proveedores.
- **RNF-008:** Mantenibilidad.
- **RNF-009:** Registro de errores.
- **RNF-010:** Privacidad de archivos y guiones.
- **RNF-011:** Validación y sanitización de entradas (texto del guion y rutas de archivos importados) para prevenir path traversal y entradas inválidas.

---

## 11. Reglas de negocio

- **RN-001:** Un proyecto deberá tener un nombre.
- **RN-002:** Cada escena tendrá un número de orden único.
- **RN-003:** Una escena podrá tener varios audios, pero solo uno activo.
- **RN-004:** No se enviará texto sin una API key válida.
- **RN-005:** El usuario será responsable de costos y condiciones del proveedor.
- **RN-006:** Los audios anteriores se conservarán al regenerar.
- **RN-007:** Los temporales podrán eliminarse después de exportar.
- **RN-008:** El sistema advertirá sobre espacio insuficiente.
- **RN-009:** No se exportará un proyecto sin audio ni video.
- **RN-010:** No se permitirá clonar voces de terceros sin autorización.
- **RN-011:** Las versiones previas de un audio se conservarán al regenerar, manteniendo un identificador de versión y de versión anterior.
- **RN-012:** Un proyecto podrá obtener su video por importación o por captura; ambos orígenes son válidos para exportación.
- **RN-013:** La composición de audio admitirá como máximo tres pistas: original del video, narración y música instrumental.
- **RN-014:** La pista de música estará pensada para audio instrumental (archivo); no se ofrece un editor musical avanzado.

---

## 12. Criterios de aceptación del MVP (redefinido 0.1b)

El MVP se considerará funcional cuando permita:

1. Crear y abrir proyectos (misma carpeta base al crear y al abrir).
2. Pegar un guion.
3. Dividirlo en escenas.
4. Configurar OpenAI.
5. Configurar ElevenLabs.
6. Consultar voces.
7. Generar audio por escena.
8. Reproducir audio.
9. Regenerar una escena.
10. Grabar desde micrófono.
11. Recortar audio.
12. Unir fragmentos de narración.
13. Importar un video.
14. Capturar pantalla o cámara con vista previa en vivo.
15. Capturar una región o una ventana.
16. Identificar monitores con etiquetas legibles.
17. Montar hasta 3 pistas (original + narración + música) con volúmenes.
18. Previsualizar la composición.
19. Exportar un MP4 reproducible.
