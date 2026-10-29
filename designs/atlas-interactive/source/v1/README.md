# XMedical Visual Assets 1.0

Paquete de recursos individuales para la interfaz isométrica 2.5D de XMedical.

## Directorios
- `modulos/`: recepción, archivador de pacientes cerrado/abierto, agenda cerrada/abierta, consultorio, historia, medicamentos, laboratorio, administración y sala de espera.
- `avatares/`: **paquete v2** — 10 retratos genéricos, uno por grupo de edad y sexo (`ninos_masculino.webp`, `adultos_femenino.webp`, …). Sustituyen a las 18 variantes numeradas del v1; ver `avatares/README.md`.
- `documentos/`: carpetas, receta, resultados, documento y estudios.
- `estados/`: iconos de citas.
- `profesionales/`: médico, enfermera, recepcionista, administrativo.
- `manifest.json`: identificadores, rutas y dimensiones (incluye los avatares v2 con `transparencia: false`).

## Uso
Los WebP de `modulos/`, `documentos/`, `estados/` y `profesionales/` tienen canal alfa y pueden mostrarse con `<img>` o como sprites. Las variantes abierto/cerrado se pueden intercambiar con CSS/JS; no son modelos 3D.

> **Excepción:** los avatares del paquete v2 **no tienen canal alfa** (conservan el fondo de la lámina) y son de 240×330 px. Están pensados para fichas pequeñas; no ampliar. Para uso a mayor tamaño hay que regenerarlos con transparencia.

**Nota de diseño:** recursos recortados y separados de una lámina generativa maestra. Revisar bordes y consistencia antes de uso en producción, especialmente para animaciones de continuidad exacta; se recomienda conservar un rótulo de texto y no usar imágenes como único elemento de navegación. Ningún avatar corresponde a pacientes reales.
