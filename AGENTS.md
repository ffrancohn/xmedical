# AGENTS.md

## Cursor Cloud specific instructions

XMedical es un monolito Django 4.2 (multi-tenant por subdominio) con PostgreSQL, Redis y Celery. Comandos estándar de desarrollo/pruebas ya están documentados en `README.md`, `USUARIOS_PRUEBA.md` y `run_tests.sh`; abajo solo van los detalles no obvios del entorno cloud.

### Servicios y cómo levantarlos

- **Docker no está disponible** en este entorno. En lugar de `docker compose`, PostgreSQL y Redis se instalan de forma nativa (vía apt) y se inician manualmente:
  - PostgreSQL: `sudo pg_ctlcluster 16 main start`
  - Redis: `sudo redis-server /etc/redis/redis.conf --daemonize yes` (verificar con `redis-cli ping`)
  - No hay systemd activo, por eso se inician a mano en cada sesión (no autoarrancan).
- Base de datos ya creada: rol `xmedical_user` (contraseña `password`) y base `xmedical`. El rol tiene **CREATEDB**, necesario para que Django cree la base de test (`test_xmedical`).

### Configuración obligatoria (`.env`)

- Copiar `.env.example` a `.env` (está en `.gitignore`, así que recréalo si falta) y usar `DEBUG=True` para desarrollo.
- **Gotcha de puerto:** `xmedical/settings.py` usa por defecto `DB_PORT=5433`, pero PostgreSQL y todo lo demás usan `5432`. El `.env` (con `DB_PORT=5432`) corrige esto; sin `.env` la app falla al conectar.

### Servidor de desarrollo

- Sincronizar deps e iniciar: `uv sync && uv run python manage.py runserver 0.0.0.0:8000` (o `source .venv/bin/activate` y luego `python manage.py runserver`).
- Primer arranque en base limpia: `uv run python manage.py migrate` y `uv run python manage.py loaddata fixtures/initial_data.json`.
- Login en `http://localhost:8000/auth/login/`. Usuarios en `USUARIOS_PRUEBA.md` (contraseña `Xmedical123!`).
- El tenant se resuelve por subdominio. En `localhost` no hay subdominio, por lo que el formulario de login **muestra un selector de clínica**; los usuarios no-superadmin (p. ej. `recepcion.demo`) deben elegir "Clinica Demo". `superadmin.demo` es superusuario y no requiere institución.

### Pruebas

- Suite: `uv run python manage.py test apps.core apps.auth_app apps.pacientes apps.citas apps.preclinica apps.consulta` (o `./run_tests.sh` para checks + cobertura; requiere `uv sync --group dev`).
- **4 fallos preexistentes** (no relacionados con el entorno): varios tests hacen peticiones con `HTTP_HOST=xmedical.cloud` (subdominio `xmedical`), pero `fixtures/initial_data.json` define la institución con `subdominio="demo"`. Por eso el login vía POST en esos tests devuelve 200 en vez de 302 y arrastra fallos en `test_fun_a01_login_valido`, `test_sec_04`, `test_sec_11` y `test_fun_pr02_registrar_signos`. Es una inconsistencia test/fixture del repo, no del setup.
- **Interfaz Atlas (isométrica):** modo usuario en `/auth/preferencias/` (`interface_mode=atlas`); motor `static/js/iso.js`, estilos `static/css/atlas.css`, prototipo `deck/prototipo/`. Despliegue: `docs/18 Interfaz Atlas Despliegue Produccion.md` (`migrate`, `collectstatic`, reiniciar Gunicorn).

### Skills Cursor (`.cursor/skills/`)

Leer el `SKILL.md` correspondiente **antes** de diseñar o refactorizar UI visual:

| Skill | Uso en XMedical |
|-------|-----------------|
| `visual-design-architect` | Decidir si Atlas/isometría vs tablas/grafos en una pantalla nueva. |
| `isometric-interface-builder` | Extender mapas SVG, estaciones clínicas, panel lateral (complementa `iso.js` / Atlas). |
| `interactive-deck-studio` | Mejorar o crear decks en `deck/` (Atlas del sistema, prototipo). |
| `visual-quality-auditor` | Revisar accesibilidad y UX tras cambios en Atlas, pacientes/citas o decks. |

Índice y ejemplos de prompts: `.cursor/README.md`. Validación: `python3 .cursor/scripts/validate_package.py`.

**Pantalla nueva o rediseño UI:** (1) Consultar la matriz en `docs/21 Arquitectura Visual Pantallas.md` (añadir fila si falta). (2) Invocar **`visual-design-architect`** para comparar representaciones y, si aplica, rellenar un brief en `docs/visual-briefs/` a partir de `.cursor/skills/visual-design-architect/assets/visual-brief.template.md`. (3) Implementar la **primaria** (tabla, formulario, wizard, hilo) en templates Django; usar **`isometric-interface-builder`** solo si el brief aprueba complemento Atlas (`atlas_scene_banner` / `atlas_hero`) y actualizar `apps/core/atlas_ui.py`. (4) Cerrar con **`visual-quality-auditor`** si se modificó Atlas o CSS global.

### Graphify (opcional)

Regla `.cursor/rules/graphify.mdc`: explorar dependencias con `graphify query` **si la CLI está instalada** en el entorno. Artefactos locales en `graphify-out/` (caché ignorada en git); regenerar con `graphify update .` tras cambios amplios.
