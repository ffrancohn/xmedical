# Doc 24 — Cómo pedir (y verificar) una interfaz isométrica de verdad

Este documento existe por una razón concreta: lo que hoy hay en el hub del médico **no es una
interfaz isométrica**, es una rejilla de tarjetas con ilustraciones isométricas dentro. Sirve para
explicar la diferencia, dar el vocabulario para pedirla y fijar criterios que se puedan verificar.

## 1. La prueba que separa una cosa de la otra

> **Si quitas las imágenes, ¿la interfaz sigue funcionando igual?**
> Si la respuesta es sí, la isometría es decoración.

En el hub actual: tres `<button>` en un `grid auto-fit`, cada uno con un WebP y un panel HTML
debajo. Sin los WebP queda exactamente la misma navegación. Eso es **ilustración isométrica**, no
**interfaz isométrica**.

Una interfaz isométrica cumple lo contrario: el espacio *es* la navegación. No hay "tarjetas"; hay
un lugar, con cosas en su sitio, y el usuario actúa sobre ese lugar.

## 2. Las siete propiedades que hay que exigir

| # | Propiedad | Qué significa en la práctica | Cómo detectar que falta |
|---|---|---|---|
| 1 | **Escena única y continua** | Un solo lienzo axonométrico; todo lo que el médico necesita está en el mismo espacio | Hay secciones apiladas, cada módulo en su tarjeta |
| 2 | **Cámara fija axonométrica** | Proyección isométrica constante (30°), sin perspectiva, con un único origen de luz | Cada ilustración tiene su propio ángulo/perspectiva |
| 3 | **El espacio significa algo** | Cada zona del plano = un área de trabajo (escritorio, sala de espera, archivo, laboratorio) | Los objetos flotan o están alineados en rejilla |
| 4 | **Objetos = affordances con estado** | Cada objeto muestra su estado real (pacientes en espera, citas pendientes) y cambia al interactuar | Los objetos son imágenes estáticas sin datos |
| 5 | **Selección en la escena + panel contextual** | Se elige sobre el objeto; el detalle aparece al lado, sin salir de la escena | El clic navega a otra página |
| 6 | **Continuidad espacial** | Al entrar a una zona la cámara se acerca; al salir vuelve. Nunca hay salto de página para "entrar" | Se abre un modal o se recarga la vista |
| 7 | **Fallback explícito** | Existe una vista de tabla/lista equivalente, accesible con un enlace (`?classic=1`) | No hay forma de hacer la tarea si la escena falla |

## 3. La escena del médico (qué debe ver al entrar)

Plano cenital isométrico de **su consultorio**, con el resto de la clínica al fondo:

```
              [ laboratorio ]      [ farmacia ]
                    \                 /
   [ archivo ]   [  SALA DE ESPERA  ]   [ recepción ]
        \              |                  /
         \       [ CONSULTORIO ]  ← el médico está aquí
                 escritorio con agenda, silla, historia
```

- **Escritorio** (primer plano, centro): agenda del día. El número de citas pendientes se ve en el
  propio escritorio (p. ej., tres hojas = tres pendientes).
- **Silla vacía** frente al escritorio: el siguiente paciente. Si hay alguien en espera, la silla
  está ocupada; si no, vacía.
- **Sala de espera** (fondo): siluetas genéricas con el conteo; el que más espera se distingue.
- **Archivo** (izquierda): historias clínicas; abre el explorador de pacientes.
- **Laboratorio / farmacia** (fondo): resultados pendientes y medicamentos.
- **Puerta / pasillo**: navegación al resto de la clínica.

El médico **no navega a un módulo**: mira su consultorio y actúa donde corresponde.

## 4. Interacción mínima (v1)

| Acción | Resultado |
|---|---|
| Hover / foco sobre un objeto | Se ilumina el contorno y aparece su etiqueta; el objeto "se abre" (variante `open`) |
| Clic / `Enter` | La cámara hace *punch-in* a esa zona y se abre el panel contextual al lado (no modal) |
| `Escape` | Vuelve la cámara a la vista general y devuelve el foco al objeto |
| Tab / flechas | Recorre los objetos en orden espacial (izq→der, fondo→frente) |
| Enlace «ver como tabla» | Vista clásica equivalente con la misma tarea |

El panel contextual puede seguir siendo HTML: no es una contradicción. La regla es que **la escena
manda** y el panel es su consecuencia, no al revés.

## 5. Criterios de aceptación verificables

Se pueden comprobar con el navegador y con tests, sin discutir gustos:

1. Existe **un** `<svg>` de escena (o un canvas) que contiene todos los objetos interactivos.
2. Quitar los `<img>` decorativos **no** deja la misma navegación: los objetos son parte de la escena.
3. Cada objeto expone `data-station`, `role="button"`, `tabindex="0"` y `aria-label` con su dato
   (p. ej. «Sala de espera: 3 pacientes, el primero hace 20 min»).
4. La selección no cambia de URL: el panel se abre en la misma página y la cámara se mueve.
5. `Escape` restaura la vista y el foco; `Tab` recorre los objetos en orden espacial.
6. Los estados de los objetos reflejan datos reales del backend (conteos, no texto fijo).
7. La escena no tiene scroll horizontal en 390 px; en móvil se recorta o se reencuadra, no se aplasta.
8. `prefers-reduced-motion` desactiva el *punch-in* y los fundidos.
9. Existe `?classic=1` con la misma tarea resuelta en tabla/formulario.
10. Un test verifica la correspondencia objeto → panel (ningún objeto abre un panel vacío).

## 6. Errores que hay que evitar (y que explican el resultado actual)

- **Rejilla con imágenes**: parece ordenado, pero es una galería. Es lo que hay hoy.
- **CSS 3D con `rotateX/rotateZ`**: no es isometría real; rompe la luz y las proporciones.
- **Todo clicable**: si cada píxel hace algo, nada se entiende.
- **Texto dentro del SVG**: no se selecciona, no se traduce, no escala. Etiquetas en HTML superpuesto.
- **Una escena distinta por módulo**: se pierde la continuidad que justifica la isometría.
- **Sustituir la tabla**: la escena no reemplaza la vista densa; la complementa.
- **Perspectiva "artística"**: si cada objeto tiene su punto de fuga, no es un espacio, es un collage.

## 7. Cómo implementarlo sin reescribir todo

El motor `static/js/iso.js` ya proyecta cajas isométricas (`P(x, y, z)`, `Scene.poly/line/text`) y hay
una escena `medico`. Lo que falta es dejar de usarlo como banner y usarlo como superficie:

| Fase | Entregable | Esfuerzo |
|---|---|---|
| **v1** | Una escena de consultorio con 3–4 estaciones, objetos con estado, foco y panel lateral; datos reales de `atlas_explore` | 3–4 días |
| **v2** | *Punch-in* por zona (la cámara se acerca y la zona se vuelve el contexto), transición de vuelta | 2–3 días |
| **v3** | Acciones dentro de la escena (marcar llegada, abrir historia) sin salir a otra página | 3–4 días |

Decisión técnica recomendada: **SVG generado por el DSL existente** (no sprites ni canvas en v1)
porque permite hit areas reales, foco de teclado y estilos por token; los WebP actuales quedan como
texturas opcionales, no como estructura.

## 8. Prototipo aprobable

[`deck/atlas-interactive/consultorio.html`](../deck/atlas-interactive/consultorio.html) — HTML
autocontenido, sin backend ni dependencias. Abre el archivo en el navegador:

- 7 estaciones: agenda, paciente en la silla, sala de espera, archivo, farmacia, laboratorio, pasillo.
- Cámara con *punch-in* al seleccionar; `Escape` vuelve y devuelve el foco; `Tab` recorre.
- Panel lateral con KPIs y barras; en móvil pasa a hoja inferior.
- Enlace «Ver como tabla» con el fallback equivalente.
- Datos ficticios en un objeto `DATA` al inicio del `<script>` (fácil de sustituir por `atlas_explore`).

Lo que **no** demuestra: arte final (los muebles son geometría generada), datos reales, permisos por rol
ni persistencia. Sirve para aprobar la metáfora, la composición y el modelo de interacción.

## 9. El párrafo que puedes pegar en cualquier brief

> Quiero una interfaz isométrica, no una galería de ilustraciones isométricas. Al entrar, el médico
> debe ver **una sola escena axonométrica de su consultorio**, con la sala de espera, el archivo y el
> laboratorio en su sitio, como un lugar real. Cada objeto de esa escena representa una tarea de su
> día y muestra su estado real (cuántos esperan, qué falta). Al seleccionar un objeto la cámara se
> acerca a esa zona y el detalle aparece al lado, sin cambiar de página; `Escape` vuelve. Todo debe
> poder hacerse con teclado, y debe existir una vista de tabla equivalente. Si al quitar las imágenes
> la interfaz sigue siendo la misma, no es lo que pido.

## 10. Cómo encaja con lo que ya existe

- Modo `classic` intacto; todo esto vive en `interface_mode = atlas`.
- `atlas_catalog.py` pasa a declarar **estaciones** (id, posición en el plano, etiqueta, panel, permisos)
  en vez de tarjetas.
- `atlas_explore.py` sigue aportando los agregados; sólo cambia cómo se presentan.
- `atlas-interactive.js` cambia de "mostrar panel bajo la tarjeta" a "seleccionar estación, mover cámara,
  abrir panel contextual".
- Los WebP v2 (240×330) sirven como detalle dentro de la escena, no como botones.
