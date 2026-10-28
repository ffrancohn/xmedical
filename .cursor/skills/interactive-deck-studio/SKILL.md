---
name: interactive-deck-studio
description: Diseña, implementa o mejora presentaciones HTML navegables, decks educativos, historias multimedia, scrollytelling y storytelling con HTML, CSS, JavaScript, SVG, imágenes, animaciones y diagramas. Úsala para decks narrativos, lecciones interactivas y visualizaciones web embebibles.
---
# Interactive Deck Studio

## Procedimiento
1. Inspecciona el repositorio y stack: no instales frameworks si no son necesarios.
2. Reúne contenido y determina audiencia, objetivo pedagógico, recorrido narrativo, ritmo y estructura de escenas. No inventes citas ni datos históricos.
3. Selecciona modalidad: paginada (slides), desplazamiento narrativo (scroll), recorrido guiado o híbrida. Consulta `references/narrative-patterns.md`.
4. Si debe seleccionarse tipo de visualización, utiliza la lógica de `visual-design-architect` si está disponible y lee su matriz; de lo contrario usa tipos de representación apropiados a los datos.
5. Produce mapa de escenas: propósito, información, visual, interacción, transición y fallback. Prioriza contenido comprensible sin animación.
6. Construye HTML semántico, CSS modular, JS modular y SVG accesible. Distingue contenido de presentación mediante JSON/objetos o componentes reutilizables.
7. Navegación: indicadores visibles siguiente/anterior o desplazamiento, progreso, teclado y gestos táctiles no conflictivos. La navegación debe seguir siendo evidente sin instrucciones externas.
8. Animaciones deben guiar atención, no distraer. Soportar prefers-reduced-motion y pausar multimedia fuera de escena.
9. Optimiza imágenes (tamaños, formatos, lazy loading), SVG (viewBox), fuentes y eventos de scroll con IntersectionObserver y/o animación optimizada.
10. Verifica en móvil y escritorio, lectura por teclado, links, navegación, carga, errores y presentación embebida en LMS.

## Bibliotecas opcionales, no obligatorias
- CSS scroll-snap e IntersectionObserver para decks ligeros.
- GSAP/ScrollTrigger para secuencias complejas vinculadas al scroll.
- Reveal.js para paradigma de diapositivas.
- Mermaid, D3 o SVG manual para diagramas/visualizaciones.
- Three.js solo si 3D aporta una necesidad específica.
- Se debe explicar y justificar cada dependencia agregada.

## Entrega
- Proyecto ejecutable con README y comando de arranque.
- Archivos editables, sin depender de imágenes aplanadas para contenido que debe interactuar.
- Mapa de escenas y guía para reemplazar imágenes y textos.
- Comportamiento seguro al incrustar en LMS: rutas relativas, responsive, sin secretos en frontend, contenido estático apto para CDN cuando corresponda.
- Priorizar salida completa funcional, no solo mockup.

## Plantilla
Usa `assets/minimal-deck/` como referencia de un deck sin dependencias; personalízala según proyecto. Consulta `references/narrative-patterns.md`.
