---
name: isometric-interface-builder
description: Diseña e implementa interfaces isométricas 2.5D interactivas con SVG, CSS y JavaScript para instalaciones, clínicas, mapas de activos, infraestructura y recorridos. Úsala cuando la relación espacial física sea relevante y se requieran áreas seleccionables, detalles y estados.
---
# Isometric Interface Builder

## Antes de dibujar
Verifica que el usuario necesite orientación, ubicación, proximidad, recorrido o contexto físico. Si las entidades son abstractas (procesos o riesgos financieros), recomienda grafo, proceso o tabla; considera consultar `visual-design-architect`.

## Arquitectura
1. Modelo de dominio: entidades con `id`, `name`, `type`, `position`, `status`, `metrics`, `actions` y relaciones. Datos fuera del SVG cuando sea posible.
2. Vista isométrica SVG: geometría estable, capas suelo/paredes/objetos/indicadores; `viewBox`, grupos con transform y orden de profundidad coherente.
3. Interacción: superposición de controles accesibles o elementos SVG con semántica/teclado contrastada; zona táctil adecuada; selección y foco perceptibles.
4. Panel de detalle HTML debajo o al lado: acciones, datos, filtros, información de la entidad seleccionada. La escena es un navegador espacial, no reemplaza formularios o tablas.
5. Estados: hover, focus, selected, disabled, warning, loading; usar color más texto/icono y descripción accesible.
6. Rendimiento: cache de formas, pocos nodos, no actualizar toda la escena con cada movimiento; preferir SVG a WebGL para escenas pequeñas/medianas. Implementar LOD o canvas cuando crezca significativamente.
7. Responsive: zoom y pan solo si aportan valor, controles grandes en móvil, lista alternativa de lugares y navegación de teclado.

## Coordenadas
Consulta `references/geometry-and-interaction.md` para proyección y capas. Emplea componentes parametrizados, no números mágicos dispersos. En casos sencillos, SVG con polígonos es suficiente; no agregar Three.js sin justificación.

## Entregables
Modelo de entidades, descripción de escenas/capas, componente reutilizable, fallback textual, panel de detalle, pruebas de navegación por teclado/tacto, documentación de importación en app existente.

## Ejemplo
`assets/isometric-demo/` contiene un ejemplo independiente y funcional con selección accesible de áreas, sin dependencias externas.
