#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

source venv/bin/activate

echo "=== Django system check ==="
python manage.py check

echo ""
echo "=== Django deploy check ==="
python manage.py check --deploy || true

echo ""
echo "=== Test suite ==="
python manage.py test apps.core --verbosity=2

echo ""
echo "=== OK ==="
