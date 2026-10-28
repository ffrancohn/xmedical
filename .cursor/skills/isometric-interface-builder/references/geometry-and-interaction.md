# Geometría e interacción isométrica

## Proyección 2:1 típica
Para coordenadas de una cuadrícula `(x,y,z)`: `screenX = originX + (x - y) * tileW / 2`; `screenY = originY + (x + y) * tileH / 2 - z * heightScale`. Usar `tileW=2*tileH` como punto de partida, no como ley universal.

## Capas
Suelo -> paredes/estructura -> elementos -> hit targets -> etiquetas/indicadores. Ordenar según profundidad `(x+y+z)` cuando exista oclusión; evitar esconder áreas clicables.

## Accesibilidad
Mantener lista HTML paralela de entidades y botones asociados a un panel. `aria-pressed`/`aria-selected` acorde al patrón de interacción real. Anunciar selección en región viva; teclado funcional; no depender de color o movimiento.

## Selección de arquitectura
- SVG para decenas o centenas de piezas sencillas.
- Canvas para miles de objetos con renderizado frecuente, acompañado de estructura accesible alternativa.
- WebGL/Three.js para perspectiva/cámara 3D real y geometría compleja, siempre ponderando costo y contexto.
- ECS solo si hay sistemas independientes que actualizan gran cantidad de entidades; usar componentes convencionales en CRUD espacial básico.

## Principio visual
Vista isométrica para descubrir *dónde*, panel HTML para entender *qué* y decidir *qué hacer*.
