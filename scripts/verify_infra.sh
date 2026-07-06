#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0
RESULTS=()

record() {
  local id="$1" name="$2" status="$3"
  if [[ "$status" == "PASS" ]]; then
    PASS=$((PASS + 1))
    RESULTS+=("| $id | $name | PASS |")
  else
    FAIL=$((FAIL + 1))
    RESULTS+=("| $id | $name | FAIL |")
  fi
}

check_active() {
  systemctl is-active --quiet "$1"
}

echo "=== INF: Infraestructura ==="

if check_active xmedical; then record "INF-01" "Gunicorn activo" "PASS"; else record "INF-01" "Gunicorn activo" "FAIL"; fi
if check_active apache2; then record "INF-02" "Apache activo" "PASS"; else record "INF-02" "Apache activo" "FAIL"; fi

if docker compose ps db 2>/dev/null | grep -q "Up"; then record "INF-03" "PostgreSQL Docker" "PASS"; else record "INF-03" "PostgreSQL Docker" "FAIL"; fi
if docker compose ps redis 2>/dev/null | grep -q "Up"; then record "INF-04" "Redis Docker" "PASS"; else record "INF-04" "Redis Docker" "FAIL"; fi

if ss -tlnp 2>/dev/null | grep -q ":8000"; then record "INF-05" "Gunicorn puerto 8000" "PASS"; else record "INF-05" "Gunicorn puerto 8000" "FAIL"; fi
if ss -tlnp 2>/dev/null | grep -q ":443"; then record "INF-06" "Apache puerto 443" "PASS"; else record "INF-06" "Apache puerto 443" "FAIL"; fi

if journalctl -u xmedical -n 20 --no-pager 2>/dev/null | grep -qi traceback; then
  record "INF-07" "Logs sin traceback" "FAIL"
else
  record "INF-07" "Logs sin traceback" "PASS"
fi

if touch backups/.write_test 2>/dev/null && rm -f backups/.write_test; then
  record "INF-08" "Backups escribible" "PASS"
else
  record "INF-08" "Backups escribible" "FAIL"
fi

printf '%s\n' "${RESULTS[@]}"
echo "--- INF: $PASS PASS, $FAIL FAIL ---"
exit $([[ "$FAIL" -eq 0 ]] && echo 0 || echo 1)
