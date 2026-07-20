#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
echo "Iniciando PostgreSQL y Redis..."
docker compose up -d db redis
echo "Listo. PostgreSQL: localhost:5432 | Redis: localhost:6379"
echo "Sincroniza deps: uv sync"
echo "Inicia Django: uv run python manage.py runserver"
