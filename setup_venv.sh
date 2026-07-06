#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "=== Configurando entorno virtual Linux ==="

if [[ -d venv/Scripts ]]; then
  echo "Eliminando venv de Windows..."
  rm -rf venv
fi

if [[ ! -d venv ]]; then
  python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Entorno listo. Para activarlo:"
echo "  source venv/bin/activate"
echo ""
python --version
pip list | head -5
