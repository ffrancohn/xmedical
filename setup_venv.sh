#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "=== Configurando entorno con uv ==="

if ! command -v uv >/dev/null 2>&1; then
  echo "Error: uv no esta instalado. Ver https://docs.astral.sh/uv/"
  exit 1
fi

if [[ -d venv ]]; then
  echo "Eliminando venv legado (pip)..."
  rm -rf venv
fi

uv sync --group dev

echo ""
echo "Entorno listo (.venv). Comandos utiles:"
echo "  uv run python manage.py runserver"
echo "  source .venv/bin/activate"
echo ""
uv run python --version
uv pip list | head -5
