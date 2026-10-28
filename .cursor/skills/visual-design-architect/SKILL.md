---
name: visual-design-architect
description: Selecciona y diseña la representación visual óptima para datos, procesos, productos, lecciones o aplicaciones. Úsala cuando se requiera decidir entre isometría, diagramas, mapas, grafos, dashboards, timelines, storytelling o gráficos interactivos, antes de programar la visualización.
---
# Visual Design Architect

## Propósito
Transformar objetivos informativos o de interacción en una arquitectura visual clara, accesible y realizable. No asumir que la isometría o el 3D son la solución por defecto.

## Proceso obligatorio
1. Inspecciona el proyecto, stack, componentes existentes, restricciones y necesidades reales. No reemplaces arquitectura existente sin justificación.
2. Define usuario, tarea, unidad de información, relaciones entre entidades, interacción esperada, estado y escala de datos. Diferencia *vista principal*, *detalle* y *acciones*.
3. Clasifica la información: espacial/física, relacional, secuencial, temporal, cuantitativa, jerárquica, narrativa o mixta.
4. Revisa `references/decision-matrix.md` y compara al menos tres representaciones candidatas por claridad, utilidad, esfuerzo, accesibilidad, mantenimiento y rendimiento (escala 1–5; justificar cada puntuación). La claridad y pertinencia cuentan más que el atractivo visual.
5. Define representación primaria y vistas complementarias; enumera qué elementos **no** deben ser isométricos. Evita mezclar técnicas innecesariamente.
6. Entrega un contrato de visualización siguiendo `assets/visual-brief.template.md`: entidades, datos, interacciones, navegación, fallbacks, responsive, criterios de aceptación.
7. Antes de construir, verifica que cada gráfico o escena permita completar una tarea concreta. Si la solicitud pide implementación, comienza a implementarla tras formular el contrato, sin esperar autorización adicional salvo restricciones que impidan avanzar.

## Principios
- Espacialidad real -> plano, mapa, isometría; relaciones abstractas -> grafo; flujo -> diagrama; magnitudes -> gráfico; tiempo -> timeline.
- Nunca usar color como único canal de significado; proporcionar etiquetas, alternativas textuales y manejo de teclado.
- SVG/HTML/CSS primero; canvas si existen numerosos elementos; WebGL/3D solo ante necesidad genuina.
- Diseñar estados vacío, carga, error, selección, zoom y detalle; no depender de hover en móvil.
- Separar modelo de dominio, vista, componentes visuales y estado de interacción. Usar ECS solo si la complejidad y cantidad de entidades lo justifican.

## Salida
Tabla de decisión, propuesta seleccionada, arquitectura de vistas, contrato de datos/eventos, riesgos, plan de implementación y criterios verificables. Para tareas de código, entregar además implementación funcional.
