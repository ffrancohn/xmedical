#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

TIMESTAMP="$(date +%Y-%m-%d_%H%M%S)"
DATE="${TIMESTAMP%%_*}"
EVIDENCE_DIR="${XMEDICAL_EVIDENCE_DIR:-$ROOT/docs/informes/evidencia/$TIMESTAMP}"

mkdir -p "$EVIDENCE_DIR"
echo "$EVIDENCE_DIR" > "$ROOT/docs/informes/evidencia/ULTIMA.txt"

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$EVIDENCE_DIR/00-ejecucion.log"; }

log "=== XMedical: verificación completa ==="
log "Carpeta de evidencia: $EVIDENCE_DIR"

run_step() {
  local id="$1"
  local name="$2"
  local outfile="$EVIDENCE_DIR/${id}-${name}.txt"
  shift 2
  log "--- $id: $name ---"
  set +e
  "$@" > >(tee "$outfile") 2>&1
  local code=$?
  set -e
  echo "$code" > "$EVIDENCE_DIR/${id}-exit-code.txt"
  return 0
}

run_step "01" "infraestructura" bash scripts/verify_infra.sh
run_step "02" "ssl" bash scripts/verify_ssl.sh
run_step "03" "humo-http" bash scripts/verify_smoke.sh
run_step "08" "seguridad-estatica" bash scripts/verify_security_static.sh
run_step "09" "seguridad-headers" bash scripts/verify_security_headers.sh

source venv/bin/activate

run_step "04" "django-check" python manage.py check
run_step "05" "django-deploy-check" bash -c "python manage.py check --deploy || true"

APPS="apps.core apps.auth_app apps.pacientes apps.citas apps.preclinica apps.consulta apps.api.tests"
run_step "06" "django-tests" python manage.py test $APPS --verbosity=2
run_step "11" "django-security-tests" python manage.py test apps.core.tests_security --verbosity=2

if python -c "import coverage" 2>/dev/null; then
  log "--- 07: cobertura ---"
  coverage erase
  set +e
  coverage run --source=apps manage.py test $APPS --verbosity=0 \
    > "$EVIDENCE_DIR/07-cobertura-tests.txt" 2>&1
  coverage report --fail-under=60 > "$EVIDENCE_DIR/07-cobertura-report.txt" 2>&1
  coverage html -d "$EVIDENCE_DIR/07-cobertura-html" \
    >> "$EVIDENCE_DIR/07-cobertura-report.txt" 2>&1
  set -e
  log "Cobertura HTML: $EVIDENCE_DIR/07-cobertura-html/index.html"
else
  echo "coverage no instalado" > "$EVIDENCE_DIR/07-cobertura-report.txt"
fi

export XMEDICAL_EVIDENCE_DIR="$EVIDENCE_DIR"
bash scripts/generate_report.sh "$DATE" "$EVIDENCE_DIR"

cat > "$EVIDENCE_DIR/LEEME.txt" <<EOF
Evidencia de verificación XMedical
==================================
Fecha/hora: $TIMESTAMP
Generado por: scripts/run_all_verifications.sh

Archivos:
  00-ejecucion.log          Log de la ejecución
  01-infraestructura.txt    Pruebas INF-*
  02-ssl.txt                Pruebas SSL-*
  03-humo-http.txt          Pruebas SMK-*
  04-django-check.txt       manage.py check
  05-django-deploy-check.txt manage.py check --deploy
  06-django-tests.txt       Suite completa Django
  07-cobertura-report.txt   Resumen de cobertura
  07-cobertura-html/        Reporte HTML de cobertura
  08-seguridad-estatica.txt   Bandit + pip-audit (SEC-S*)
  09-seguridad-headers.txt    Headers HTTP prod (SEC-08*)
  11-django-security-tests.txt Pruebas SEC-* Django
  INFORME.md                Resumen consolidado (empezar aquí)

Última ejecución registrada en: docs/informes/evidencia/ULTIMA.txt
EOF

log "=== Verificación completada ==="
log "Revisar evidencia en: $EVIDENCE_DIR"
log "Informe resumen: $EVIDENCE_DIR/INFORME.md"
echo "$EVIDENCE_DIR"
