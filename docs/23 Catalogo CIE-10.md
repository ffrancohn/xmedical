# Doc 22 — Catálogo CIE-10 y búsqueda de diagnósticos

Estado: **implementado** (2026-10-29). Reemplaza la lista embebida de 10 códigos que usaba el wizard.

## Problema que resuelve

Hasta ahora el autocompletado de diagnósticos leía `CIE10_MVP`, una lista de **10 códigos**
escrita a mano en `apps/consulta/wizard.py` (0,07 % de la CIE-10), sin tildes, sin sinónimos y
sin ranking. El diagnóstico se guardaba como texto libre (`codigo_cie10` + `nombre`), así que
«Hipertensión arterial» y «Hipertension esencial primaria» contaban como enfermedades distintas
en epidemiología.

## Solución

| Pieza | Dónde |
|---|---|
| Modelo `CodigoCie10` (`codigo`, `descripcion`, `nivel`, `capitulo`, `bloque`, `es_hoja`, `busqueda`) | `apps/consulta/models.py` |
| Normalizador (`normalizar_texto`: minúsculas, sin tildes, espacios colapsados) | `apps/consulta/models.py` |
| Importador idempotente | `apps/consulta/management/commands/import_cie10.py` |
| Sinónimos y abreviaturas (HTA, DM2, IAM, EPOC, ITU, ICC, EVC…) | `apps/consulta/sinonimos.py` |
| Endpoint con ranking y fallback | `apps/consulta/views.py::cie10_search` |
| Pruebas | `apps/consulta/tests_cie10.py` (11 tests) |

## Carga del catálogo

Ver [`data/cie10/README.md`](../data/cie10/README.md). Resumen:

```powershell
Invoke-WebRequest https://raw.githubusercontent.com/verasativa/CIE-10/master/cie-10.csv -OutFile data/cie10/cie-10.csv
python manage.py import_cie10
```

Resultado en la instalación de demo: **14.498 entradas**, de las cuales **14.268 consultables**
(nivel ≥ 2).

## Búsqueda

`GET /consulta/cie10/?q=...` → `{"results": [{"codigo", "nombre"}], "total": n, "catalogo": true}`

1. Normaliza la consulta (tildes fuera) y la expande con sinónimos.
2. Filtra `es_hoja=True` por `busqueda` (contiene) o prefijo de código.
3. Ordena: código exacto → prefijo de código → mismo capítulo → resto; desempata por longitud.
4. Devuelve 10 resultados e informa el total.
5. Si la tabla está vacía, cae a `CIE10_MVP` (`catalogo: false`) para no romper el wizard.

Medido en la demo (14.268 códigos): **5–40 ms** por consulta, sin índice trigram. Si el catálogo
crece o se quiere tolerancia a erratas, el siguiente paso es `pg_trgm` (extensión ya disponible
en Postgres pero no instalada) con `GIN (busqueda gin_trgm_ops)`.

## Pendiente (siguiente incremento)

1. `Diagnostico` con FK opcional a `CodigoCie10` y snapshot del texto (para no alterar historias).
2. Validar en el formulario que el código exista (hoy `CharField(max_length=10)` acepta cualquier texto).
3. Agrupar epidemiología y el panel «Historia clínica» del hub por `codigo`/capítulo, no por `nombre`.
4. Mapear los diagnósticos históricos sin código (`codigo_cie10 = ''`).
