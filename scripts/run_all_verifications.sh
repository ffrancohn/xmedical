#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
DATE="$(date +%Y-%m-%d)"
TMP="${TMPDIR:-/tmp}/xmedical-verify-$$"
mkdir -p "$TMP" docs/informes

echo "=== XMedical: verificación completa ($DATE) ==="

bash scripts/verify_infra.sh | tee "$TMP/infra.out" || true
bash scripts/verify_ssl.sh | tee "$TMP/ssl.out" || true
bash scripts/verify_smoke.sh | tee "$TMP/smoke.out" || true

source venv/bin/activate
python manage.py check 2>&1 | tee "$TMP/check.out"
python manage.py check --deploy 2>&1 | tee "$TMP/deploy.out" || true
python manage.py test apps.core apps.auth_app apps.pacientes apps.citas apps.preclinica apps.consulta apps.api.tests --verbosity=1 2>&1 | tee "$TMP/django.out"

export TMP
bash scripts/generate_report.sh "$DATE"

rm -rf "$TMP"
echo "=== Verificación completada ==="
