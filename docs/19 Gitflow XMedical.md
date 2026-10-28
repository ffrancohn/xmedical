# Gitflow en XMedical (guía breve)

**Rama troncal de producción:** `master` (GitHub usa `origin/master`).

A partir de ahora el flujo recomendado es **Gitflow simplificado**: código estable en `master`, integración continua en `develop`, trabajo aislado en ramas `feature/*`, `release/*` y `hotfix/*`.

---

## Ramas y propósito

| Rama | Propósito | ¿Desplegar a producción? |
|------|-----------|---------------------------|
| **`master`** | Lo que está (o estará) en https://xmedical.cloud | **Sí** — solo tras merge/review |
| **`develop`** | Integración del siguiente release; pruebas en staging | No (entorno de integración) |
| **`feature/…`** | Una mejora o ticket (Atlas, citas, IA, etc.) | No |
| **`release/…`** | Congelar versión, solo fixes y docs de release | Staging → luego merge a `master` |
| **`hotfix/…`** | Corrección urgente en producción | Sí, directo a `master` (+ back-merge a `develop`) |

Convención de nombres: minúsculas, guiones — p. ej. `feature/interfaz-atlas`, `hotfix/login-cookies`, `release/1.4.0`.

---

## Diagrama del flujo

```mermaid
gitGraph
   commit id: "prod"
   branch develop
   checkout develop
   commit id: "integración"
   branch feature/nueva-funcion
   checkout feature/nueva-funcion
   commit id: "trabajo"
   commit id: "tests"
   checkout develop
   merge feature/nueva-funcion
   commit id: "QA"
   branch release/1.4.0
   checkout release/1.4.0
   commit id: "ajustes release"
   checkout master
   merge release/1.4.0 tag: "v1.4.0"
   checkout develop
   merge release/1.4.0
   checkout master
   branch hotfix/urgente
   checkout hotfix/urgente
   commit id: "fix prod"
   checkout master
   merge hotfix/urgente tag: "v1.4.1"
   checkout develop
   merge hotfix/urgente
```

**Lectura rápida:** las *features* entran a `develop`; un *release* pasa a `master` (tag de versión); un *hotfix* nace de `master` y vuelve a `master` y `develop`.

---

## Comandos habituales

Actualizar referencias remotas (hacerlo al inicio del día):

```bash
git fetch origin
```

### Cambiar de rama (local)

```bash
git switch master          # producción
git switch develop         # integración
git switch feature/mi-tarea
```

Equivalente clásico: `git checkout <rama>`.

Crear rama y cambiarte en un paso:

```bash
git switch -c feature/mi-tarea origin/develop
```

### Empezar una feature

```bash
git fetch origin
git switch develop
git pull origin develop
git switch -c feature/descripcion-corta
# … commits …
git push -u origin feature/descripcion-corta
```

Abrir **Pull Request** en GitHub: **`feature/…` → `develop`**.

### Cerrar release (staging → producción)

```bash
git switch develop
git pull origin develop
git switch -c release/1.4.0
# solo fixes de release, changelog, versión
git push -u origin release/1.4.0
```

PR **`release/1.4.0` → `master`** (deploy) y otro merge **`release/1.4.0` → `develop`** (o merge back manual).

Tag en `master`:

```bash
git switch master && git pull origin master
git tag -a v1.4.0 -m "Release 1.4.0"
git push origin v1.4.0
```

### Hotfix en producción

```bash
git fetch origin
git switch master
git pull origin master
git switch -c hotfix/descripcion
# … fix …
git push -u origin hotfix/descripcion
```

PR **`hotfix/…` → `master`**, desplegar, luego merge del hotfix en **`develop`**.

---

## Producción (VPS)

Solo actualizar desde **`master`**:

```bash
git pull origin master
python manage.py migrate
python manage.py collectstatic --noinput
# reiniciar Gunicorn / systemd
```

Ver también [Doc 18 — Interfaz Atlas](18%20Interfaz%20Atlas%20Despliegue%20Produccion.md) y [Doc 11 — Plan de despliegue](11%20Plan%20de%20Deespliegue.md).

---

## Puesta en marcha (una vez en el repo)

Si aún no existe `develop`:

```bash
git fetch origin
git switch master
git pull origin master
git switch -c develop
git push -u origin develop
```

En GitHub: **Settings → Branches** → proteger `master` (PR obligatorio, sin push directo) y opcionalmente `develop`.

---

## Ramas históricas `cursor/*`

Son ramas de agentes/PRs anteriores. **No forman parte del Gitflow nuevo.** Las nuevas tareas usan `feature/*` desde `develop`. Se pueden archivar o borrar en remoto cuando ya estén mergeadas.

---

## Resumen en una línea

**Feature → `develop` → `release` → `master` (prod); hotfix desde `master` → `master` + `develop`.**
