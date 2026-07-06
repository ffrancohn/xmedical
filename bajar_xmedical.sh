#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
echo "Deteniendo servicios Docker..."
docker compose down
echo "Servicios detenidos. Los datos de PostgreSQL se conservan en el volumen postgres_data."
