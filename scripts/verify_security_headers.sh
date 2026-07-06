#!/usr/bin/env bash
set -euo pipefail

BASE="${XMEDICAL_BASE_URL:-https://xmedical.cloud}"
DOMAIN="${XMEDICAL_DOMAIN:-xmedical.cloud}"

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

headers() {
  curl -skI "$1" 2>/dev/null
}

echo "=== SEC-08: Headers de seguridad ==="

HSTS=$(headers "$BASE/" | grep -i "^strict-transport-security:" || true)
if echo "$HSTS" | grep -qi "max-age=31536000\|max-age=31536000"; then
  record "SEC-08a" "HSTS max-age" "PASS"
elif echo "$HSTS" | grep -qi "max-age="; then
  record "SEC-08a" "HSTS max-age" "WARN"
else
  record "SEC-08a" "HSTS max-age" "FAIL"
fi

if headers "$BASE/" | grep -qi "x-content-type-options:.*nosniff"; then
  record "SEC-08b" "X-Content-Type-Options" "PASS"
else
  record "SEC-08b" "X-Content-Type-Options" "FAIL"
fi

if headers "$BASE/" | grep -qi "referrer-policy:.*same-origin"; then
  record "SEC-08c" "Referrer-Policy" "PASS"
else
  record "SEC-08c" "Referrer-Policy" "FAIL"
fi

XFO=$(headers "$BASE/auth/login/" | grep -i "^x-frame-options:" || true)
if echo "$XFO" | grep -Eqi "DENY|SAMEORIGIN"; then
  record "SEC-08d" "X-Frame-Options" "PASS"
else
  record "SEC-08d" "X-Frame-Options" "FAIL"
fi

COOKIE_HDR=$(curl -skI -X POST "$BASE/auth/login/" \
  -d "username=medico.demo&password=wrong" 2>/dev/null | grep -i "^set-cookie:" || true)
if echo "$COOKIE_HDR" | grep -qi "secure" && echo "$COOKIE_HDR" | grep -qi "httponly"; then
  record "SEC-08e" "Cookie Secure+HttpOnly" "PASS"
elif [[ -z "$COOKIE_HDR" ]]; then
  record "SEC-08e" "Cookie Secure+HttpOnly" "WARN"
else
  record "SEC-08e" "Cookie Secure+HttpOnly" "FAIL"
fi

if echo | openssl s_client -connect "${DOMAIN}:443" -tls1_2 2>/dev/null | grep -q "BEGIN CERTIFICATE"; then
  record "SEC-08f" "TLS 1.2+" "PASS"
else
  record "SEC-08f" "TLS 1.2+" "FAIL"
fi

SERVER_HDR=$(headers "$BASE/" | grep -i "^server:" || true)
if [[ -z "$SERVER_HDR" ]]; then
  record "SEC-08g" "Server header oculto" "PASS"
else
  record "SEC-08g" "Server header oculto" "WARN"
fi

printf '%s\n' "${RESULTS[@]}"
echo "--- SEC-08: $PASS PASS, $FAIL FAIL, $WARN WARN ---"
exit $([[ "$FAIL" -eq 0 ]] && echo 0 || echo 1)
