# Doc 18 — Interfaz Atlas (isométrica): despliegue y recuperación en producción

**Versión:** 1.0 · **2026-10-27**  
**Código:** rama `cursor/interfaz-atlas-8777` · GitHub PR **#22**  
**Producción:** `https://xmedical.cloud`

Este documento permite **desplegar**, **verificar** y **revertir** el modo de interfaz **Atlas** (escenas SVG del prototipo `deck/prototipo`) en el entorno productivo.

---

## 1. Qué incluye el cambio

| Componente | Ubicación |
|------------|-----------|
| Preferencia por usuario | `UserPreference.interface_mode` (`classic` \| `atlas`) |
| Migración Django | `apps/auth_app/migrations/0004_userpreference_interface_mode.py` |
| Motor isométrico | `static/js/iso.js` (origen: `deck/assets/js/iso.js`) |
| Estilos Atlas | `static/css/atlas.css` |
| Resolución de escena | `apps/core/atlas_ui.py` |
| UI | `/auth/preferencias/` → modo **Atlas**; dashboards clínicos (piloto) |

**Fix relacionado (misma rama):** cookies de sesión en HTTP local cuando `DEBUG=False` y `SECURE_SSL_REDIRECT=False` (`xmedical/settings.py`).

---

## 2. Desplegar en producción (VPS Hostinger u otro)

### 2.1 Prerrequisitos

- Acceso SSH al servidor donde corre Gunicorn/Apache.
- Backup reciente de PostgreSQL (recomendado antes de migraciones).
- Ventana de mantenimiento corta (solo migrate + restart + collectstatic).

### 2.2 Obtener el código

**Opción A — Tras merge del PR #22 en `master` (recomendado):**

```bash
cd /ruta/al/xmedical
git fetch origin
git checkout master
git pull origin master
```

**Opción B — Desplegar la rama del PR sin merge:**

```bash
cd /ruta/al/xmedical
git fetch origin
git checkout cursor/interfaz-atlas-8777
git pull origin cursor/interfaz-atlas-8777
```

Anota el commit desplegado para rollback:

```bash
git rev-parse HEAD
```

### 2.3 Entorno virtual y dependencias

```bash
source venv/bin/activate   # ajusta ruta si aplica
pip install -r requirements/prod.txt   # o requirements.txt del proyecto
```

No hay paquetes Python nuevos solo por Atlas; solo assets estáticos y migración.

### 2.4 Migración de base de datos (obligatoria)

```bash
python manage.py migrate auth_app
# o migración completa:
python manage.py migrate
```

Verifica que exista la columna:

```bash
python manage.py showmigrations auth_app | tail -3
# debe listar [X] 0004_userpreference_interface_mode
```

### 2.5 Archivos estáticos

```bash
python manage.py collectstatic --noinput
```

Comprueba que existan en el directorio servido por Apache/Nginx:

- `static/js/iso.js`
- `static/css/atlas.css`

### 2.6 Reiniciar aplicación

Según tu instalación (ejemplo systemd):

```bash
sudo systemctl restart xmedical
# o gunicorn + nombre del servicio que uses
sudo systemctl status xmedical
```

Si usas Apache como proxy, normalmente no hace falta reiniciar Apache tras solo estáticos; **sí** reiniciar Gunicorn tras cambio de código Python.

### 2.7 Variables `.env` en producción (HTTPS)

Para `https://xmedical.cloud`:

```env
DEBUG=False
SECURE_SSL_REDIRECT=True
SECURE_COOKIES=True
ALLOWED_HOSTS=xmedical.cloud,www.xmedical.cloud,.xmedical.cloud
CSRF_TRUSTED_ORIGINS=https://xmedical.cloud,https://www.xmedical.cloud,https://*.xmedical.cloud
```

Con HTTPS y `SECURE_SSL_REDIRECT=True`, las cookies Secure son correctas. No uses la configuración de cookies Secure en HTTP plano.

---

## 3. Verificación post-despliegue

1. **Login** staff: `https://xmedical.cloud/auth/login/` (o subdominio tenant, p. ej. `https://demo.xmedical.cloud/...`).
2. **Preferencias:** `https://xmedical.cloud/auth/preferencias/`  
   - Debe aparecer **Modo de interfaz** con **Clásica** y **Atlas**.
3. Elegir **Atlas** → **Guardar**.
4. **Recepción:** `https://xmedical.cloud/dashboards/recepcion/`  
   - Escena isométrica + hilo del día (en pantalla ancha).
5. **Estáticos:** en DevTools → Network, confirmar `200` en `/static/js/iso.js` y `/static/css/atlas.css`.

Usuario de prueba: ver [`USUARIOS_PRUEBA.md`](../USUARIOS_PRUEBA.md) (`recepcion.demo` / `Xmedical123!`).

---

## 4. Activación para usuarios finales

Atlas **no** se activa solo. Cada usuario:

1. Menú lateral → **Preferencias** (o clic en el nombre en la parte inferior del sidebar).
2. Modo **Atlas** → Guardar.
3. Ir al **inicio** de su rol (recepción: `/dashboards/recepcion/`).

El modo **Clásica** sigue siendo el valor por defecto en base de datos (`interface_mode=classic`).

---

## 5. Rollback / recuperación ante fallo

### 5.1 Rollback de código (rápido)

```bash
cd /ruta/al/xmedical
git fetch origin
git checkout master
git reset --hard <COMMIT_ANTERIOR_AL_DESPLIEGUE>
python manage.py collectstatic --noinput
sudo systemctl restart xmedical
```

La columna `interface_mode` puede quedar en la BD; Django antiguo la ignorará si el modelo no la define (no suele romper). Para código pre-#22 no hace falta revertir migración.

### 5.2 Revertir migración (solo si necesitas quitar la columna)

```bash
python manage.py migrate auth_app 0003_remove_tema_vital
```

**Precaución:** pierdes valores guardados de `interface_mode`. Haz backup antes.

### 5.3 Desactivar Atlas sin rollback de código

Los usuarios pueden volver a **Preferencias** → **Clásica**.  
O en SQL (emergencia):

```sql
UPDATE auth_app_userpreference SET interface_mode = 'classic' WHERE interface_mode = 'atlas';
```

---

## 6. Sincronizar `iso.js` con el deck

El prototipo sigue en `deck/assets/js/iso.js`. Tras editar escenas allí:

```bash
cp deck/assets/js/iso.js static/js/iso.js
python manage.py collectstatic --noinput
# commit + despliegue
```

---

## 7. Referencias

| Recurso | Enlace |
|---------|--------|
| Prototipo navegable | `deck/prototipo/` — `python -m http.server 8080 --directory deck` |
| PR GitHub | [#22](https://github.com/ffrancohn/xmedical/pull/22) |
| Catálogo de pantallas | [Doc 17](17%20Caracteristicas%20Pantallas%20y%20Flujo%206%20Diagnostico.md) |
| Credenciales demo | [`USUARIOS_PRUEBA.md`](../USUARIOS_PRUEBA.md) |

---

## 8. Checklist resumido (copiar en ticket de despliegue)

- [ ] Backup BD
- [ ] `git pull` (master con #22 o rama `cursor/interfaz-atlas-8777`)
- [ ] `python manage.py migrate`
- [ ] `python manage.py collectstatic --noinput`
- [ ] Reiniciar Gunicorn/systemd
- [ ] Probar `/auth/preferencias/` (opción Atlas visible)
- [ ] Probar `/dashboards/recepcion/` con usuario Atlas
- [ ] Anotar `git rev-parse HEAD` en registro de cambios
