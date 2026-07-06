#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

source venv/bin/activate

APPS="apps.core apps.auth_app apps.pacientes apps.citas apps.preclinica apps.consulta apps.api.tests"

echo "=== Django system check ==="
python manage.py check

echo ""
echo "=== Django deploy check ==="
python manage.py check --deploy || true

echo ""
echo "=== Test suite ==="
python manage.py test $APPS --verbosity=2

echo ""
echo "=== Coverage (umbral 60%) ==="
if python -c "import coverage" 2>/dev/null; then
  coverage erase
  coverage run --source=apps manage.py test $APPS --verbosity=0
  coverage report --fail-under=60
else
  echo "coverage no instalado; ejecutar: pip install -r requirements/dev.txt"
fi

echo ""
echo "=== OK ==="
