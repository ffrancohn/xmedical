#!/usr/bin/env bash
set -euo pipefail

DOMAIN="${XMEDICAL_DOMAIN:-xmedical.cloud}"
EXPECTED_IP="${XMEDICAL_EXPECTED_IP:-2.25.194.6}"

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

echo "=== SSL: Conectividad y certificado ==="

DNS_IP=$(dig +short "$DOMAIN" A 2>/dev/null | head -1 || true)
if [[ "$DNS_IP" == "$EXPECTED_IP" ]]; then record "SSL-01" "DNS A" "PASS"; else record "SSL-01" "DNS A ($DNS_IP)" "FAIL"; fi

if curl -sfI "https://${DOMAIN}/" >/dev/null 2>&1; then record "SSL-02" "HTTPS responde" "PASS"; else record "SSL-02" "HTTPS responde" "FAIL"; fi

REDIRECT=$(curl -sI "http://${DOMAIN}/" 2>/dev/null | grep -i "^location:" | grep -ci "https" || true)
if [[ "$REDIRECT" -ge 1 ]]; then record "SSL-03" "HTTP a HTTPS" "PASS"; else record "SSL-03" "HTTP a HTTPS" "FAIL"; fi

if echo | openssl s_client -connect "${DOMAIN}:443" -servername "$DOMAIN" 2>/dev/null | openssl x509 -noout -checkend 86400 >/dev/null 2>&1; then
  record "SSL-04" "Certificado valido" "PASS"
else
  record "SSL-04" "Certificado valido" "FAIL"
fi

if certbot certificates 2>/dev/null | grep -q "$DOMAIN"; then record "SSL-05" "Certbot dominio" "PASS"; else record "SSL-05" "Certbot dominio" "FAIL"; fi

if certbot renew --dry-run >/dev/null 2>&1; then record "SSL-06" "Renovacion dry-run" "PASS"; else record "SSL-06" "Renovacion dry-run" "FAIL"; fi

if curl -sI "https://${DOMAIN}/" 2>/dev/null | grep -qi "strict-transport-security"; then
  record "SSL-07" "Header HSTS" "PASS"
else
  record "SSL-07" "Header HSTS" "FAIL"
fi

if curl -sfI "https://www.${DOMAIN}/auth/login/" >/dev/null 2>&1; then record "SSL-08" "www alias" "PASS"; else record "SSL-08" "www alias" "FAIL"; fi

printf '%s\n' "${RESULTS[@]}"
echo "--- SSL: $PASS PASS, $FAIL FAIL ---"
exit $([[ "$FAIL" -eq 0 ]] && echo 0 || echo 1)
