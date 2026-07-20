#!/usr/bin/env bash
# Utilidades uv para sincronizar entornos virtuales del proyecto.
set -euo pipefail

UV_BIN="${UV_BIN:-uv}"

uv_ensure() {
  if command -v "$UV_BIN" >/dev/null 2>&1; then
    return 0
  fi
  echo "[uv] Instalando uv en /usr/local/bin ..."
  curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin UV_NO_MODIFY_PATH=1 sh
  command -v "$UV_BIN" >/dev/null 2>&1
}

# uv_sync_venv <directorio_proyecto> <ruta_venv_relativa> <requirements.txt> [más reqs...]
uv_sync_venv() {
  local project_dir="$1"
  local venv_rel="$2"
  shift 2
  local py="${PYTHON_BIN:-python3.12}"
  if ! command -v "$py" >/dev/null 2>&1; then
    py=python3
  fi
  local venv_path="${project_dir%/}/${venv_rel}"
  uv_ensure
  "$UV_BIN" venv "$venv_path" --python "$py" --allow-existing
  local req
  for req in "$@"; do
    local req_path="${project_dir%/}/${req}"
    if [[ ! -f "$req_path" ]]; then
      echo "No existe: $req_path" >&2
      return 1
    fi
    echo "[uv] $req"
    "$UV_BIN" pip install -r "$req_path" --python "${venv_path}/bin/python"
  done
}
