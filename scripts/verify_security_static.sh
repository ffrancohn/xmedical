#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0
WARN=0
RESULTS=()

record() {
  local id="$1" name="$2" status="$3"
  case "$status" in
    PASS) PASS=$((PASS + 1)) ;;
    FAIL) FAIL=$((FAIL + 1)) ;;
    WARN) WARN=$((WARN + 1)) ;;
  esac
  RESULTS+=("| $id | $name | $status |")
}

echo "=== SEC-S: Analisis estatico ==="

if command -v bandit >/dev/null 2>&1; then
  if bandit -r apps/ -ll -q 2>/dev/null; then
    record "SEC-S01" "Bandit apps/" "PASS"
  else
    record "SEC-S01" "Bandit apps/" "FAIL"
  fi
else
  record "SEC-S01" "Bandit apps/" "WARN"
  echo "bandit no instalado; pip install -r requirements/dev.txt"
fi

if command -v pip-audit >/dev/null 2>&1; then
  if pip-audit -r requirements.txt -q 2>/dev/null; then
    record "SEC-S02" "pip-audit requirements.txt" "PASS"
  else
    record "SEC-S02" "pip-audit requirements.txt" "FAIL"
  fi
else
  record "SEC-S02" "pip-audit requirements.txt" "WARN"
  echo "pip-audit no instalado; pip install -r requirements/dev.txt"
fi

if git ls-files --error-unmatch .env >/dev/null 2>&1; then
  record "SEC-S03" ".env fuera de git" "FAIL"
else
  record "SEC-S03" ".env fuera de git" "PASS"
fi

printf '%s\n' "${RESULTS[@]}"
echo "--- SEC-S: $PASS PASS, $FAIL FAIL, $WARN WARN ---"
exit $([[ "$FAIL" -eq 0 ]] && echo 0 || echo 1)
