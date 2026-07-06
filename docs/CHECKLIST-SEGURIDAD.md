# Checklist de seguridad — XMedical

Revisión manual pre-release. Marcar **PASS** / **FAIL** / **N/A**.

Referencia: [`docs/7 Documento de Seguridad.md`](7%20Documento%20de%20Seguridad.md)

---

## Configuración y secretos

| Caso | PASS | FAIL | Notas |
|------|:----:|:----:|-------|
| `.env` no está en Git | | | |
| `SECRET_KEY` rotada y ≥ 50 caracteres | | | |
| `DEBUG=False` en producción | | | |
| Credenciales demo no usadas en prod real | | | |

## Transporte y headers

| Caso | PASS | FAIL | Notas |
|------|:----:|:----:|-------|
| HTTP redirige a HTTPS (Apache) | | | |
| Certificado válido > 30 días | | | |
| HSTS activo | | | |
| Cookies `Secure` + `HttpOnly` | | | |
| W008/W021 documentados como aceptados | | | |

## Acceso y roles

| Caso | PASS | FAIL | Notas |
|------|:----:|:----:|-------|
| Rutas clínicas requieren login | | | |
| Superadmin solo para `is_superuser` | | | |
| Aislamiento tenant (subdominio/sesión) | | | |
| RBAC por rol documentado (gaps conocidos) | | | |

## Datos e infraestructura

| Caso | PASS | FAIL | Notas |
|------|:----:|:----:|-------|
| PostgreSQL no expuesto a Internet | | | |
| Redis no expuesto a Internet | | | |
| `backups/` permisos restringidos | | | |
| Logs sin contraseñas en texto claro | | | |

## Escaneos automatizados

| Caso | PASS | FAIL | Notas |
|------|:----:|:----:|-------|
| `verify_security_static.sh` (bandit, pip-audit) | | | |
| `apps.core.tests_security` (SEC-*) | | | |
| `verify_security_headers.sh` | | | |
| OWASP ZAP baseline mensual | | | |

---

**Ejecutor:** _______________  
**Fecha:** _______________  
**Evidencia:** `docs/informes/evidencia/<timestamp>/`
