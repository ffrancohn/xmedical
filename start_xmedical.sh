#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "=== XMedical - Django (Linux) ==="

if ! command -v uv >/dev/null 2>&1; then
  echo "Error: uv no esta instalado. Ver https://docs.astral.sh/uv/"
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Error: Docker no esta instalado."
  exit 1
fi

echo "[1/4] Levantando PostgreSQL y Redis..."
docker compose up -d db redis

echo "[2/4] Sincronizando entorno con uv..."
uv sync

echo "[3/4] Migraciones y datos de prueba..."
uv run python manage.py migrate
uv run python manage.py loaddata fixtures/initial_data.json

echo "[4/4] Iniciando Django en http://localhost:8000"
echo "Login: http://localhost:8000/auth/login/"
echo "Usuarios: ver USUARIOS_PRUEBA.md"
uv run python manage.py runserver 0.0.0.0:8000
