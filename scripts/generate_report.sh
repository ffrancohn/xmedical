#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATE="${1:-$(date +%Y-%m-%d)}"
EVIDENCE_DIR="${2:-${XMEDICAL_EVIDENCE_DIR:-}}"

if [[ -z "$EVIDENCE_DIR" || ! -d "$EVIDENCE_DIR" ]]; then
  echo "Uso: generate_report.sh FECHA CARPETA_EVIDENCIA" >&2
  exit 1
fi

REPORT_DIR="$ROOT/docs/informes"
SUMMARY="$REPORT_DIR/INFORME-VERIFICACION-${DATE}.md"
INFORME="$EVIDENCE_DIR/INFORME.md"

INF_OUT="$EVIDENCE_DIR/01-infraestructura.txt"
SSL_OUT="$EVIDENCE_DIR/02-ssl.txt"
SMK_OUT="$EVIDENCE_DIR/03-humo-http.txt"
CHECK_OUT="$EVIDENCE_DIR/04-django-check.txt"
DEPLOY_OUT="$EVIDENCE_DIR/05-django-deploy-check.txt"
DJANGO_OUT="$EVIDENCE_DIR/06-django-tests.txt"
COVERAGE_OUT="$EVIDENCE_DIR/07-cobertura-report.txt"
SEC_STATIC_OUT="$EVIDENCE_DIR/08-seguridad-estatica.txt"
SEC_HEADERS_OUT="$EVIDENCE_DIR/09-seguridad-headers.txt"
SEC_TESTS_OUT="$EVIDENCE_DIR/11-django-security-tests.txt"

count_pass() {
  local n=0
  n=$(grep -c "| PASS |" "$1" 2>/dev/null) || n=0
  echo "$n"
}
count_fail() {
  local n=0
  n=$(grep -c "| FAIL |" "$1" 2>/dev/null) || n=0
  echo "$n"
}
count_warn() {
  local n=0
  n=$(grep -c "| WARN |" "$1" 2>/dev/null) || n=0
  echo "$n"
}

INF_PASS=$(count_pass "$INF_OUT")
INF_FAIL=$(count_fail "$INF_OUT")
SSL_PASS=$(count_pass "$SSL_OUT")
SSL_FAIL=$(count_fail "$SSL_OUT")
SMK_PASS=$(count_pass "$SMK_OUT")
SMK_FAIL=$(count_fail "$SMK_OUT")
SEC_S_PASS=$(count_pass "$SEC_STATIC_OUT")
SEC_S_FAIL=$(count_fail "$SEC_STATIC_OUT")
SEC_S_WARN=$(count_warn "$SEC_STATIC_OUT")
SEC_H_PASS=$(count_pass "$SEC_HEADERS_OUT")
SEC_H_FAIL=$(count_fail "$SEC_HEADERS_OUT")
SEC_H_WARN=$(count_warn "$SEC_HEADERS_OUT")

DJANGO_STATUS="PASS"
grep -qiE "FAILED|ERROR \(" "$DJANGO_OUT" 2>/dev/null && DJANGO_STATUS="FAIL"

SEC_DJANGO_STATUS="PASS"
grep -qiE "FAILED|ERROR \(" "$SEC_TESTS_OUT" 2>/dev/null && SEC_DJANGO_STATUS="FAIL"

CHECK_STATUS="PASS"
grep -qi "error" "$CHECK_OUT" 2>/dev/null && CHECK_STATUS="FAIL"

TOTAL_PASS=$((INF_PASS + SSL_PASS + SMK_PASS + SEC_S_PASS + SEC_H_PASS))
TOTAL_FAIL=$((INF_FAIL + SSL_FAIL + SMK_FAIL + SEC_S_FAIL + SEC_H_FAIL))
TOTAL_WARN=$((SEC_S_WARN + SEC_H_WARN))
[[ "$DJANGO_STATUS" == "FAIL" ]] && TOTAL_FAIL=$((TOTAL_FAIL + 1)) || TOTAL_PASS=$((TOTAL_PASS + 1))
[[ "$SEC_DJANGO_STATUS" == "FAIL" ]] && TOTAL_FAIL=$((TOTAL_FAIL + 1)) || TOTAL_PASS=$((TOTAL_PASS + 1))
[[ "$CHECK_STATUS" == "FAIL" ]] && TOTAL_FAIL=$((TOTAL_FAIL + 1)) || TOTAL_PASS=$((TOTAL_PASS + 1))

REL_EVIDENCE="${EVIDENCE_DIR#$ROOT/docs/informes/}"
REL_FROM_INFORMES="${REL_EVIDENCE}"

write_report() {
  local dest="$1"
  local link_prefix="$2"
  cat > "$dest" <<EOF
# Informe de verificación — XMedical

**Fecha:** ${DATE}  
**Carpeta de evidencia:** \`${REL_EVIDENCE}\`  
**Generado por:** \`scripts/run_all_verifications.sh\`

## 1. Resumen ejecutivo

| Métrica | Valor |
|---------|-------|
| PASS | ${TOTAL_PASS} |
| FAIL | ${TOTAL_FAIL} |
| WARN | ${TOTAL_WARN} |
| Tests Django | ${DJANGO_STATUS} |
| Tests seguridad Django | ${SEC_DJANGO_STATUS} |
| Django check | ${CHECK_STATUS} |

## 2. Archivos de evidencia

| Archivo | Contenido |
|---------|-----------|
| [01-infraestructura.txt](${link_prefix}01-infraestructura.txt) | INF-01..08 |
| [02-ssl.txt](${link_prefix}02-ssl.txt) | SSL-01..08 |
| [03-humo-http.txt](${link_prefix}03-humo-http.txt) | SMK-01..06 |
| [08-seguridad-estatica.txt](${link_prefix}08-seguridad-estatica.txt) | SEC-S01..03 |
| [09-seguridad-headers.txt](${link_prefix}09-seguridad-headers.txt) | SEC-08a..g |
| [11-django-security-tests.txt](${link_prefix}11-django-security-tests.txt) | SEC-01..12 |
| [04-django-check.txt](${link_prefix}04-django-check.txt) | \`manage.py check\` |
| [05-django-deploy-check.txt](${link_prefix}05-django-deploy-check.txt) | \`check --deploy\` |
| [06-django-tests.txt](${link_prefix}06-django-tests.txt) | Suite Django completa |
| [07-cobertura-report.txt](${link_prefix}07-cobertura-report.txt) | Cobertura |
| [07-cobertura-html/index.html](${link_prefix}07-cobertura-html/index.html) | Cobertura visual |

## 3. Infraestructura (INF-*)

| ID | Prueba | Resultado |
|----|--------|-----------|
$(grep "| INF-" "$INF_OUT" 2>/dev/null || echo "| — | Sin datos | — |")

## 4. SSL (SSL-*)

| ID | Prueba | Resultado |
|----|--------|-----------|
$(grep "| SSL-" "$SSL_OUT" 2>/dev/null || echo "| — | Sin datos | — |")

## 5. Humo HTTP (SMK-*)

| ID | Prueba | Resultado |
|----|--------|-----------|
$(grep "| SMK-" "$SMK_OUT" 2>/dev/null || echo "| — | Sin datos | — |")

## 6. Seguridad estática (SEC-S*)

| ID | Prueba | Resultado |
|----|--------|-----------|
$(grep "| SEC-S" "$SEC_STATIC_OUT" 2>/dev/null || echo "| — | Sin datos | — |")

## 7. Headers seguridad (SEC-08*)

| ID | Prueba | Resultado |
|----|--------|-----------|
$(grep "| SEC-08" "$SEC_HEADERS_OUT" 2>/dev/null || echo "| — | Sin datos | — |")

## 8. Tests Django (extracto)

\`\`\`
$(tail -40 "$DJANGO_OUT" 2>/dev/null || echo "Sin salida")
\`\`\`

## 9. Tests seguridad Django (SEC-*)

\`\`\`
$(tail -30 "$SEC_TESTS_OUT" 2>/dev/null || echo "Sin salida")
\`\`\`

## 10. Deploy check

\`\`\`
$(cat "$DEPLOY_OUT" 2>/dev/null || echo "Sin salida")
\`\`\`

Warnings aceptados: W008 (Apache redirige HTTPS), W021 (HSTS preload opcional), SEC-06 (rate limit pendiente).

## 11. Cobertura

\`\`\`
$(cat "$COVERAGE_OUT" 2>/dev/null || echo "Sin salida")
\`\`\`

## 12. Comandos para reproducir

\`\`\`bash
cd /var/www/xmedical
./scripts/run_all_verifications.sh
./scripts/verify_security_zap.sh   # mensual
\`\`\`

## 13. Incidencias abiertas

- Revisar filas FAIL en tablas anteriores.
- ZAP mensual: \`scripts/verify_security_zap.sh\` → ver \`10-seguridad-zap.html\`.
EOF
}

write_report "$INFORME" ""
write_report "$SUMMARY" "${REL_FROM_INFORMES}/"

echo "Informe en evidencia: $INFORME"
echo "Resumen del día:       $SUMMARY"
