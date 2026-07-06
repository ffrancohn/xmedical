#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "=== XMedical - Django (Linux) ==="

if ! command -v docker >/dev/null 2>&1; then
  echo "Error: Docker no esta instalado."
  exit 1
fi

echo "[1/4] Levantando PostgreSQL y Redis..."
docker compose up -d db redis

if [[ ! -d venv/bin ]]; then
  echo "[2/4] Creando entorno virtual..."
  python3 -m venv venv
  source venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
else
  echo "[2/4] Activando entorno virtual..."
  source venv/bin/activate
fi

echo "[3/4] Migraciones y datos de prueba..."
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json

echo "[4/4] Iniciando Django en http://localhost:8000"
echo "Login: http://localhost:8000/auth/login/"
echo "Usuarios: ver USUARIOS_PRUEBA.md"
python manage.py runserver 0.0.0.0:8000
