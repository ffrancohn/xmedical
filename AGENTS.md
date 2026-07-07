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

- Activar venv y correr: `source venv/bin/activate && python manage.py runserver 0.0.0.0:8000`.
- Primer arranque en base limpia: `python manage.py migrate` y `python manage.py loaddata fixtures/initial_data.json`.
- Login en `http://localhost:8000/auth/login/`. Usuarios en `USUARIOS_PRUEBA.md` (contraseña `Xmedical123!`).
- El tenant se resuelve por subdominio. En `localhost` no hay subdominio, por lo que el formulario de login **muestra un selector de clínica**; los usuarios no-superadmin (p. ej. `recepcion.demo`) deben elegir "Clinica Demo". `superadmin.demo` es superusuario y no requiere institución.

### Pruebas

- Suite: `python manage.py test apps.core apps.auth_app apps.pacientes apps.citas apps.preclinica apps.consulta` (o `./run_tests.sh` para checks + cobertura; requiere `requirements/dev.txt`).
- **4 fallos preexistentes** (no relacionados con el entorno): varios tests hacen peticiones con `HTTP_HOST=xmedical.cloud` (subdominio `xmedical`), pero `fixtures/initial_data.json` define la institución con `subdominio="demo"`. Por eso el login vía POST en esos tests devuelve 200 en vez de 302 y arrastra fallos en `test_fun_a01_login_valido`, `test_sec_04`, `test_sec_11` y `test_fun_pr02_registrar_signos`. Es una inconsistencia test/fixture del repo, no del setup.
