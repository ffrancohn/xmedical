#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=scripts/uv_lib.sh
source "$ROOT/scripts/uv_lib.sh"
uv_sync_venv "$ROOT" "venv" requirements.txt
