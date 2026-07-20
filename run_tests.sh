#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

if [[ ! -d .venv ]]; then
  uv sync --group dev
fi

APPS="apps.core apps.auth_app apps.pacientes apps.citas apps.preclinica apps.consulta apps.api.tests"

echo "=== Django system check ==="
uv run python manage.py check

echo ""
echo "=== Django deploy check ==="
uv run python manage.py check --deploy || true

echo ""
echo "=== Test suite ==="
uv run python manage.py test $APPS --verbosity=2

echo ""
echo "=== Coverage (umbral 60%) ==="
if uv run python -c "import coverage" 2>/dev/null; then
  uv run coverage erase
  uv run coverage run --source=apps manage.py test $APPS --verbosity=0
  uv run coverage report --fail-under=60
else
  echo "coverage no instalado; ejecutar: uv sync --group dev"
fi

echo ""
echo "=== OK ==="
