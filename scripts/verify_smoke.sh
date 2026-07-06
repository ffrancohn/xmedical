#!/usr/bin/env bash
set -euo pipefail

BASE="${XMEDICAL_BASE_URL:-https://xmedical.cloud}"

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

check_code() {
  local url="$1"
  local expected_regex="$2"
  local code
  code=$(curl -sk -o /dev/null -w "%{http_code}" "$url")
  [[ "$code" =~ $expected_regex ]]
}

check_redirect_login() {
  local url="$1"
  local code location
  code=$(curl -sk -o /dev/null -w "%{http_code}" "$url")
  location=$(curl -sk -I "$url" | grep -i "^location:" | tr -d '\r' || true)
  [[ "$code" == "302" && "$location" == *"/auth/login/"* ]]
}

echo "=== SMK: Humo HTTP ==="

check_code "${BASE}/" "^(200|302)$" && record "SMK-01" "Home" "PASS" || record "SMK-01" "Home" "FAIL"
check_code "${BASE}/auth/login/" "^200$" && record "SMK-02" "Login" "PASS" || record "SMK-02" "Login" "FAIL"
check_code "${BASE}/admin/" "^(200|302)$" && record "SMK-03" "Admin" "PASS" || record "SMK-03" "Admin" "FAIL"
check_redirect_login "${BASE}/dashboard/" && record "SMK-04" "Dashboard protegido" "PASS" || record "SMK-04" "Dashboard protegido" "FAIL"
check_redirect_login "${BASE}/pacientes/" && record "SMK-05" "Pacientes protegido" "PASS" || record "SMK-05" "Pacientes protegido" "FAIL"
check_code "${BASE}/static/admin/css/base.css" "^200$" && record "SMK-06" "Static admin CSS" "PASS" || record "SMK-06" "Static admin CSS" "FAIL"

printf '%s\n' "${RESULTS[@]}"
echo "--- SMK: $PASS PASS, $FAIL FAIL ---"
echo "Nota: SMK-07..11 requieren sesion; ver apps.core.tests SmokeHttpTests"
exit $([[ "$FAIL" -eq 0 ]] && echo 0 || echo 1)
