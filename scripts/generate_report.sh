#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATE="${1:-$(date +%Y-%m-%d)}"
REPORT_DIR="$ROOT/docs/informes"
REPORT="$REPORT_DIR/INFORME-VERIFICACION-${DATE}.md"
TMP="${TMPDIR:-/tmp}/xmedical-verify-$$"

mkdir -p "$REPORT_DIR" "$TMP"

INF_OUT="$TMP/infra.out"
SSL_OUT="$TMP/ssl.out"
SMK_OUT="$TMP/smoke.out"
DJANGO_OUT="$TMP/django.out"
DEPLOY_OUT="$TMP/deploy.out"

count_pass() { grep -c "| PASS |" "$1" 2>/dev/null || echo 0; }
count_fail() { grep -c "| FAIL |" "$1" 2>/dev/null || echo 0; }

INF_PASS=$(count_pass "$INF_OUT")
INF_FAIL=$(count_fail "$INF_OUT")
SSL_PASS=$(count_pass "$SSL_OUT")
SSL_FAIL=$(count_fail "$SSL_OUT")
SMK_PASS=$(count_pass "$SMK_OUT")
SMK_FAIL=$(count_fail "$SMK_OUT")

DJANGO_STATUS="PASS"
grep -qi "FAILED\|ERROR" "$DJANGO_OUT" 2>/dev/null && DJANGO_STATUS="FAIL"

TOTAL_PASS=$((INF_PASS + SSL_PASS + SMK_PASS))
TOTAL_FAIL=$((INF_FAIL + SSL_FAIL + SMK_FAIL))
[[ "$DJANGO_STATUS" == "FAIL" ]] && TOTAL_FAIL=$((TOTAL_FAIL + 1)) || TOTAL_PASS=$((TOTAL_PASS + 1))

cat > "$REPORT" <<EOF
# Informe de verificación — XMedical

**Fecha:** ${DATE}  
**Generado por:** \`scripts/run_all_verifications.sh\`

## 1. Resumen ejecutivo

| Métrica | Valor |
|---------|-------|
| PASS | ${TOTAL_PASS} |
| FAIL | ${TOTAL_FAIL} |
| Tests Django | ${DJANGO_STATUS} |

## 2. Infraestructura (INF-*)

| ID | Prueba | Resultado |
|----|--------|-----------|
$(grep "| INF-" "$INF_OUT" 2>/dev/null || echo "| — | Sin datos | — |")

## 3. SSL (SSL-*)

| ID | Prueba | Resultado |
|----|--------|-----------|
$(grep "| SSL-" "$SSL_OUT" 2>/dev/null || echo "| — | Sin datos | — |")

## 4. Humo HTTP (SMK-*)

| ID | Prueba | Resultado |
|----|--------|-----------|
$(grep "| SMK-" "$SMK_OUT" 2>/dev/null || echo "| — | Sin datos | — |")

## 5. Tests Django

\`\`\`
$(tail -30 "$DJANGO_OUT" 2>/dev/null || echo "Sin salida")
\`\`\`

## 6. Deploy check

\`\`\`
$(cat "$DEPLOY_OUT" 2>/dev/null || echo "Sin salida")
\`\`\`

## 7. Comandos para reproducir

\`\`\`bash
cd /var/www/xmedical
./scripts/run_all_verifications.sh
./run_tests.sh
\`\`\`

## 8. Incidencias abiertas

- Revisar filas FAIL en tablas anteriores.
EOF

echo "Informe generado: $REPORT"
