# Informe de verificación operativa — XMedical

| Campo | Valor |
|-------|-------|
| **Fecha** | 2026-07-06 |
| **Entorno** | Producción — https://xmedical.cloud |
| **Servidor** | srv1746626.hstgr.cloud (2.25.194.6) |
| **Ejecutado por** | Agente / revisión automatizada |
| **Commit Git** | `cea964f6` (rama `master`) |

---

## 1. Resumen ejecutivo

| Resultado | Detalle |
|-----------|---------|
| **Estado general** | ✅ **Operativo** |
| **Servicios críticos** | 4/4 activos |
| **HTTPS** | ✅ Válido hasta 2026-10-03 |
| **Autenticación** | ✅ 4/4 usuarios demo |
| **Rutas clínicas** | ✅ Accesibles por rol |
| **Base de datos** | ✅ Datos demo cargados |
| **Advertencias** | 5 avisos Django `--deploy` (endurecimiento SSL pendiente) |

---

## 2. Infraestructura

| Componente | Prueba | Resultado | Evidencia |
|------------|--------|-----------|-----------|
| Gunicorn (`xmedical.service`) | `systemctl is-active xmedical` | ✅ active | systemd |
| Apache | `systemctl is-active apache2` | ✅ active | systemd |
| PostgreSQL 15 | `docker compose ps db` | ✅ Up 2h+ | contenedor `xmedical-db-1` |
| Redis 7 | `docker compose ps redis` | ✅ Up 2h+ | contenedor `xmedical-redis-1` |

---

## 3. Red y SSL

| Prueba | Comando / método | Resultado |
|--------|------------------|-----------|
| DNS | `dig xmedical.cloud A` | ✅ → `2.25.194.6` |
| HTTPS login | `curl -I https://xmedical.cloud/auth/login/` | ✅ HTTP 200 |
| Redirect HTTP→HTTPS | `curl -I http://xmedical.cloud/` | ✅ HTTP 301 → HTTPS |
| Certificado Let's Encrypt | `certbot certificates` | ✅ Válido 89 días |
| Dominios en cert | — | `xmedical.cloud`, `www.xmedical.cloud` |

---

## 4. Rutas públicas (sin autenticación)

| URL | HTTP esperado | Resultado |
|-----|---------------|-----------|
| `https://xmedical.cloud/` | 200 | ✅ |
| `https://xmedical.cloud/auth/login/` | 200 | ✅ |
| `https://xmedical.cloud/admin/` | 200 (form login) | ✅ |
| `https://xmedical.cloud/dashboard/` | 302 → login | ✅ |
| `https://xmedical.cloud/pacientes/` | 302 → login | ✅ |
| `https://xmedical.cloud/static/admin/css/base.css` | 200 | ✅ |

---

## 5. Autenticación y roles

Contraseña usada en pruebas: `Xmedical123!` (ver `USUARIOS_PRUEBA.md`).

| Usuario | Login | Ruta probada | Resultado esperado | Resultado |
|---------|-------|--------------|-------------------|-----------|
| `superadmin.demo` | ✅ | `/dashboard/` | Redirect → `/superadmin/` | ✅ |
| `superadmin.demo` | ✅ | `/superadmin/` | 200 | ✅ |
| `medico.demo` | ✅ | `/dashboard/` | 200 (agenda médico) | ✅ |
| `recepcion.demo` | ✅ | `/dashboard/` | Redirect → `/citas/agendar/` | ✅ |
| `recepcion.demo` | ✅ | `/pacientes/`, `/citas/` | 200 | ✅ |
| `enfermera.demo` | ✅ | `/dashboard/` | Redirect → `/preclinica/` | ✅ |
| `enfermera.demo` | ✅ | `/preclinica/` | 200 | ✅ |

> Los redirects por rol en `/dashboard/` son **comportamiento correcto**, no errores.

---

## 6. Base de datos

| Entidad | Registros | Esperado (fixture) | Resultado |
|---------|-----------|-------------------|-----------|
| Usuarios | 5 | 5 | ✅ |
| Instituciones | 1 | 1 | ✅ |
| Profesionales | 4 | 4 | ✅ |
| Pacientes | 10 | 10 | ✅ |
| Citas | 3 | 3 | ✅ |

---

## 7. Django — comprobaciones

| Comando | Resultado |
|---------|-----------|
| `python manage.py check` | ✅ 0 errores |
| `python manage.py check --deploy` | ⚠️ 5 advertencias (ver sección 8) |

---

## 8. Advertencias pendientes (no bloquean operación)

Detectadas con `manage.py check --deploy`:

| Código | Ajuste recomendado |
|--------|-------------------|
| W004 | Configurar `SECURE_HSTS_SECONDS` |
| W008 | `SECURE_SSL_REDIRECT=True` (Apache ya redirige) |
| W009 | Revisar longitud/complejidad de `SECRET_KEY` |
| W012 | `SESSION_COOKIE_SECURE=True` |
| W016 | `CSRF_COOKIE_SECURE=True` |

Estas mejoras se pueden aplicar en `.env` / `settings.py` para endurecer cookies y HSTS.

---

## 9. Lo que NO se probó en esta revisión

| Tipo | Descripción | Cómo ejecutarlo |
|------|-------------|-----------------|
| **Pruebas unitarias** | Lógica aislada de modelos/forms | `python manage.py test` (suite por crear) |
| **Pruebas E2E navegador** | Flujo completo wizard consulta | Playwright / Selenium manual |
| **Carga / estrés** | Concurrencia, tiempos bajo carga | `locust` o `ab -n 1000` |
| **Regresión visual** | UI plantillas HTML | Revisión manual en navegador |
| **Backup/restore** | Superadmin JSON backup | Login superadmin → `/superadmin/` |
| **Celery workers** | Tareas asíncronas | `docker compose up celery` + tarea test |
| **Subdominios tenant** | `*.xmedical.cloud` | Requiere DNS wildcard + cert |
| **API REST** | Endpoints móvil | No implementada aún |

---

## 10. Cómo reproducir estas pruebas

### Infraestructura rápida

```bash
systemctl is-active xmedical apache2
docker compose -f /var/www/xmedical/docker-compose.yml ps
curl -I https://xmedical.cloud/auth/login/
```

### Django check

```bash
cd /var/www/xmedical
source venv/bin/activate
python manage.py check
python manage.py check --deploy
```

### Prueba funcional login (shell Django)

```bash
python manage.py shell
```

```python
from django.test import Client
H = {"HTTP_HOST": "xmedical.cloud"}
c = Client(**H)
assert c.login(username="medico.demo", password="Xmedical123!")
assert c.get("/dashboard/", **H).status_code == 200
print("OK")
```

### Verificación manual recomendada para ti

1. Abrir https://xmedical.cloud/auth/login/
2. Entrar como `medico.demo` / `Xmedical123!`
3. Verificar agenda en dashboard
4. Entrar como `recepcion.demo` → pacientes y citas
5. Entrar como `enfermera.demo` → preclínica
6. Entrar como `superadmin.demo` → panel superadmin

---

## 11. Plantilla para futuras revisiones

Copiar este archivo con fecha nueva y completar:

```markdown
# Informe de verificación — YYYY-MM-DD
- [ ] Servicios activos
- [ ] HTTPS válido
- [ ] Login por rol
- [ ] Rutas clínicas
- [ ] Datos BD
- [ ] manage.py check
- [ ] Revisión manual navegador
- [ ] Notas / incidencias
```

---

**Conclusión:** El sistema web XMedical en producción está **funcional** para uso demo y operación básica. Las advertencias de seguridad Django son mejoras recomendadas, no fallos de servicio.
