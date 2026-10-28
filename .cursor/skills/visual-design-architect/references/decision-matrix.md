# Guía de selección de representaciones

| Forma | Adecuado para | Evitar cuando | Implementación inicial |
|---|---|---|---|
| Isometría 2.5D | Infraestructura y áreas físicas, navegación espacial | Riesgos intangibles, tablas densas | SVG grupos transformados + HTML paneles |
| Plano / mapa | Ubicación precisa, recorridos físicos | Conceptos abstractos sin geografía | SVG / mapas específicos |
| Grafo / red | Dependencias, contagio de riesgo, rutas lógicas | Comparación exacta de montos | SVG con d3-force o layout estable |
| Diagrama de flujo | Procedimientos, decisiones, estados | Gran cantidad de nodos sin agregación | Mermaid / SVG / React Flow |
| Heatmap / matriz | Probabilidad-impacto, concentración | Identificación de recorridos | CSS grid / SVG |
| Barras / líneas | Valores, tendencias, comparaciones | Situaciones donde importa la ubicación | SVG / librería existente |
| Timeline | Secuencia temporal, evolución de incidentes | Redes de relaciones complejas | HTML/CSS / SVG |
| Vista explotada / capas | Arquitectura de equipos y componentes | Datos no espaciales | SVG en capas |
| Storytelling / scrollytelling | Aprendizaje progresivo, casos y narrativas | Operación transaccional cotidiana | HTML/CSS/GSAP opcional |
| Tabla + filtros | Gestión, auditoría, detalle preciso y exportable | Exploración espacial como tarea primaria | HTML semántico |

## Método
1. Determina tarea primaria y representación mental del usuario.
2. Puntúa de 1 a 5: pertinencia (peso 30%), legibilidad (25%), interacción (15%), accesibilidad (15%), rendimiento (10%), facilidad de mantenimiento (5%). Mayor puntuación es mejor.
3. Registra supuestos, ventajas, riesgos y fallback.
4. Si las puntuaciones son similares, prefiere la solución más simple y familiar.
5. En riesgos, conservar trazabilidad proceso/activo -> amenaza -> vulnerabilidad -> evento -> consecuencia -> control -> responsable -> tratamiento, con vista textual disponible.
