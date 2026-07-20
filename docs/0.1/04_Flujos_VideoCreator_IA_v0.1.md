# Flujos Funcionales y Casos de Uso

**Proyecto:** VideoCreator IA  
**Versión:** 0.1b  
**Estado:** Planificación actualizada (visión redefinida)

---

## FL-001. Crear proyecto

### Actor

Usuario.

### Precondición

La aplicación está abierta.

### Flujo principal

1. El usuario selecciona **Nuevo proyecto**.
2. El sistema muestra el formulario.
3. El usuario ingresa el nombre.
4. Selecciona la carpeta.
5. El sistema valida que el nombre y la carpeta sean válidos.
6. Crea la estructura del proyecto.
7. Registra el proyecto.
8. Abre la ventana principal.

### Flujos alternativos

- La carpeta no tiene permisos.
- El proyecto ya existe.
- No hay espacio suficiente.

### Resultado

Proyecto creado y disponible para edición.

---

## FL-002. Dividir guion

1. El usuario pega o escribe el texto.
2. Selecciona **Dividir**.
3. El sistema identifica párrafos.
4. Crea escenas.
5. Asigna numeración.
6. Calcula duración estimada.
7. Presenta la lista de escenas.

### Alternativas

- El texto está vacío.
- El usuario selecciona división manual.
- El texto contiene escenas ya marcadas.

---

## FL-003. Configurar proveedor

1. El usuario abre Configuración.
2. Selecciona OpenAI o ElevenLabs.
3. Ingresa la API key.
4. Presiona **Validar**.
5. El sistema consulta al proveedor.
6. Si la clave es válida, guarda una referencia segura.
7. Consulta modelos y voces.
8. Muestra el estado **Conectado**.

### Errores

- Clave inválida.
- Sin conexión.
- Proveedor no disponible.
- Cuenta sin acceso al servicio.

---

## FL-004. Generar audio

1. El usuario selecciona una o varias escenas.
2. Selecciona proveedor.
3. Selecciona modelo y voz.
4. Presiona **Generar**.
5. El sistema valida la credencial.
6. Verifica el texto.
7. Divide el texto cuando excede el límite.
8. Envía la solicitud.
9. Descarga el audio.
10. Guarda el archivo.
11. Registra el resultado.
12. Actualiza la interfaz.
13. Permite reproducirlo.

### Errores

- Texto vacío.
- Límite alcanzado.
- Error de red.
- Respuesta inválida.
- Error de escritura.

---

## FL-005. Regenerar audio

1. El usuario selecciona una escena.
2. Modifica el texto, modelo o voz.
3. Presiona **Regenerar**.
4. El sistema crea una nueva versión.
5. Conserva la anterior.
6. Marca la nueva como activa.
7. Permite comparar ambas versiones.

---

## FL-006. Grabar voz

1. El usuario selecciona el micrófono.
2. Selecciona una escena.
3. Presiona **Grabar**.
4. El sistema muestra el nivel de entrada.
5. El usuario narra.
6. Puede pausar y continuar.
7. Presiona **Detener**.
8. El sistema guarda el archivo WAV.
9. Permite escuchar.
10. El usuario acepta o repite.

### Errores

- Micrófono no disponible.
- Permiso denegado.
- Entrada silenciosa.
- Falta de espacio.

---

## FL-007. Editar audio

1. El usuario selecciona un archivo.
2. El sistema muestra la forma de onda.
3. El usuario marca un intervalo.
4. Elige recortar, dividir o eliminar.
5. El sistema crea una nueva versión.
6. Permite escuchar el resultado.
7. El usuario confirma.

---

## FL-008. Obtener video (importar o capturar)

### Alternativa A — Importar

1. El usuario selecciona **Importar video**.
2. Elige un archivo.
3. El sistema valida el formato.
4. Ejecuta FFprobe.
5. Obtiene duración, resolución y FPS.
6. Copia el archivo a `video/imported/`.
7. Muestra la vista previa / reproducción.

### Alternativa B — Capturar

1. El usuario selecciona **Capturar**.
2. Elige modo: pantalla | cámara | región | ventana.
3. Si es pantalla, ve etiquetas legibles (Monitor N · resolución · Principal).
4. Si es región, dibuja el rectángulo.
5. Si es ventana, elige de la lista de ventanas abiertas.
6. Inicia captura con vista previa en vivo.
7. Detiene y el sistema guarda en `video/captured/`.
8. Reproduce el resultado.

### Errores

- Formato no compatible (import).
- Archivo corrupto.
- Codec no disponible.
- Sin permiso de captura de pantalla (Windows).
- Cámara en uso.
- Ventana cerrada durante la captura.

---

## FL-009. Combinar audio y video (hasta 3 pistas)

1. El usuario selecciona el video.
2. Configura pista A: audio original (on/off + volumen).
3. Selecciona pista B: narración (IA o mic).
4. Opcionalmente añade pista C: música instrumental (archivo + volumen).
5. El sistema rechaza una cuarta pista (RN-013 / RF-073).
6. Compara duraciones y valida sincronización (RF-049a).
7. Muestra alternativas de duración.
8. Genera vista previa de la mezcla.
9. El usuario acepta.

### Alternativas de duración

- Recortar video.
- Recortar audio.
- Agregar silencio.
- Mantener el último fotograma del video.
- Repetir video.

---

## FL-010. Exportar

1. El usuario abre Exportación.
2. Selecciona resolución.
3. Selecciona orientación.
4. Elige carpeta.
5. El sistema verifica FFmpeg.
6. Comprueba espacio.
7. Inicia exportación.
8. Lee el progreso.
9. Finaliza.
10. Valida el archivo.
11. Muestra el resultado.

### Errores

- FFmpeg no disponible.
- Espacio insuficiente.
- Carpeta sin permisos.
- Codec no disponible.
- Proceso cancelado.
- Archivo final inválido.

---

## FL-011. Capturar región o ventana

1. El usuario elige **Región** o **Ventana**.
2. Región: selecciona pantalla y dibuja el área.
3. Ventana: elige título de ventana de la lista.
4. Confirma e inicia captura con preview.
5. Detiene y registra el asset.

---

## FL-012. Añadir música instrumental

1. En composición, el usuario pulsa **Añadir música**.
2. Selecciona un archivo de audio.
3. Ajusta volumen de la pista C.
4. Escucha la mezcla con narración y/o original.
5. Confirma.

---

## FL-013. Abrir proyecto desde carpeta de guardado

1. El usuario pulsa **Abrir proyecto**.
2. El diálogo parte de la carpeta base de proyectos (la misma que al crear).
3. Selecciona un proyecto (`project.json`) o la carpeta base.
4. El sistema registra en BD si faltaba y lo selecciona.

---

# Casos de uso

## CU-001. Crear proyecto

**Actor:** Usuario.  
**Resultado esperado:** Proyecto creado con su estructura de carpetas.

## CU-002. Configurar proveedor

**Actor:** Usuario.  
**Resultado esperado:** API key validada y voces disponibles.

## CU-003. Generar narración

**Actor:** Usuario.  
**Resultado esperado:** Audio creado y asociado a una escena.

## CU-004. Grabar voz

**Actor:** Usuario.  
**Resultado esperado:** Grabación guardada y reproducible.

## CU-005. Unir audio y video

**Actor:** Usuario.  
**Resultado esperado:** Vista previa sincronizada con hasta 3 pistas.

## CU-006. Exportar video

**Actor:** Usuario.  
**Resultado esperado:** Archivo MP4 reproducible.

## CU-007. Capturar video

**Actor:** Usuario.  
**Resultado esperado:** Video capturado (pantalla/cámara/región/ventana) registrado y reproducible.

## CU-008. Añadir música

**Actor:** Usuario.  
**Resultado esperado:** Pista instrumental mezclada sin superar 3 pistas.
