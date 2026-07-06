# Guía de Configuración - XMedical

Guía paso a paso para configurar y ejecutar XMedical con Django.

## Checklist de preparación

- [ ] **Python 3.11+** instalado
- [ ] **Docker y Docker Compose** instalados (recomendado)
- [ ] Git instalado

Verificación rápida:

```bash
python --version    # o python3 --version en Linux
docker --version
docker compose version
```

## Paso 1: Clonar y configurar entorno

```bash
git clone <repository-url>
cd xmedical
cp .env.example .env
```

Editar `.env` si necesitas cambiar credenciales de base de datos o `SECRET_KEY`.

## Paso 2: Levantar PostgreSQL y Redis

### Con Docker (recomendado)

**Linux / macOS:**

```bash
./levantar_xmedical.sh
```

**Windows:**

```bash
levantar_xmedical.bat
```

Servicios:

- PostgreSQL: `localhost:5432` (base `xmedical`, usuario `xmedical_user`)
- Redis: `localhost:6379`

### Sin Docker

Instalar PostgreSQL 14+ y Redis 7 manualmente, crear la base de datos:

```sql
CREATE DATABASE xmedical;
CREATE USER xmedical_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE xmedical TO xmedical_user;
```

## Paso 3: Configurar entorno Python

**Linux / macOS:**

```bash
./setup_venv.sh
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Paso 4: Inicializar base de datos

```bash
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
```

Opcional — crear superusuario adicional:

```bash
python manage.py createsuperuser
```

## Paso 5: Iniciar Django

```bash
python manage.py runserver
```

**Sistema listo en:** http://localhost:8000

## Paso 6: Verificar acceso

| Recurso | URL (local) | URL (producción) |
|---|---|---|
| Login | http://localhost:8000/auth/login/ | https://xmedical.cloud/auth/login/ |
| Dashboard médico | http://localhost:8000/dashboard/ | https://xmedical.cloud/dashboard/ |
| Admin Django | http://localhost:8000/admin/ | https://xmedical.cloud/admin/ |
| Superadmin | http://localhost:8000/superadmin/ | https://xmedical.cloud/superadmin/ |

Credenciales de prueba: ver [`USUARIOS_PRUEBA.md`](USUARIOS_PRUEBA.md).

Contraseña común de todos los usuarios demo: `Xmedical123!`

## Inicio con Docker completo

Para levantar Django y Celery dentro de contenedores:

```bash
docker compose up -d
```

Esto inicia: `db`, `redis`, `web` (Django) y `celery`.

## Scripts de inicio rápido (Windows)

| Script | Descripción |
|---|---|
| `start_xmedical.bat` | Levanta Docker + Django en desarrollo |
| `levantar_xmedical.bat` | Solo PostgreSQL y Redis |
| `bajar_xmedical.bat` | Detiene servicios Docker |
| `reiniciar_xmedical.bat` | Reinicia PostgreSQL y Redis |

## Solución de problemas

### Error: "No module named django"

Activar el entorno virtual e instalar dependencias:

```bash
pip install -r requirements.txt
```

### Error de conexión a PostgreSQL

1. Verificar que Docker esté corriendo: `docker compose ps`
2. Verificar credenciales en `.env`
3. Probar conexión:

```bash
docker compose exec db psql -U xmedical_user -d xmedical
```

### Recargar datos de prueba

```bash
python manage.py loaddata fixtures/initial_data.json
```

### Puerto 8000 ocupado

Usar otro puerto:

```bash
python manage.py runserver 8001
```

## Checklist final

- [ ] PostgreSQL y Redis en ejecución
- [ ] Migraciones aplicadas (`migrate`)
- [ ] Datos de prueba cargados (`loaddata`)
- [ ] Django responde en http://localhost:8000
- [ ] Login exitoso con usuario demo

## Próximos pasos

1. Revisar [`docs/`](docs/) para arquitectura y plan de despliegue
2. Cambiar contraseñas de usuarios demo en entornos reales
3. Configurar `DEBUG=False` y `SECRET_KEY` seguro para producción

---

## Producción (xmedical.cloud)

Despliegue actual en servidor Linux:

| Componente | Ubicación / comando |
|---|---|
| Código | `/var/www/xmedical` |
| Servicio Gunicorn | `systemctl status xmedical` |
| Apache vhost | `/etc/apache2/sites-available/xmedical-le-ssl.conf` |
| SSL | Certbot / Let's Encrypt |
| Variables | `/var/www/xmedical/.env` (no en Git) |

Comandos útiles:

```bash
sudo systemctl restart xmedical    # reiniciar Django
sudo systemctl reload apache2      # recargar Apache
./bajar_xmedical.sh                # detener Docker (BD)
./levantar_xmedical.sh             # levantar PostgreSQL + Redis
python manage.py collectstatic --noinput
```

URL producción: https://xmedical.cloud/auth/login/

**Apache SSL** (`/etc/apache2/sites-available/xmedical-le-ssl.conf`): el vhost HTTPS debe enviar `X-Forwarded-Proto "https"` a Gunicorn (no `"http"`).

**Pruebas automatizadas:**

```bash
./run_tests.sh
```
