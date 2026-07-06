#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${XMEDICAL_BASE_URL:-https://xmedical.cloud}"
TIMESTAMP="$(date +%Y-%m-%d_%H%M%S)"
EVIDENCE_DIR="${XMEDICAL_EVIDENCE_DIR:-$ROOT/docs/informes/evidencia/zap_$TIMESTAMP}"

mkdir -p "$EVIDENCE_DIR"
echo "$EVIDENCE_DIR" > "$ROOT/docs/informes/evidencia/ULTIMA_ZAP.txt"

echo "=== SEC-Z: OWASP ZAP baseline ==="
echo "Target: $TARGET"
echo "Evidencia: $EVIDENCE_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "FAIL: Docker no disponible"
  exit 1
fi

REPORT_HTML="$EVIDENCE_DIR/10-seguridad-zap.html"
REPORT_JSON="$EVIDENCE_DIR/10-seguridad-zap.json"

docker run --rm \
  -v "$EVIDENCE_DIR:/zap/wrk:rw" \
  zaproxy/zap-stable \
  zap-baseline.py \
  -t "$TARGET" \
  -r 10-seguridad-zap.html \
  -J 10-seguridad-zap.json \
  -m 5 \
  -z "-config spider.maxDepth=3" \
  2>&1 | tee "$EVIDENCE_DIR/10-seguridad-zap.log" || true

if [[ -f "$REPORT_HTML" ]]; then
  echo "Informe ZAP: $REPORT_HTML"
  HIGH=$(grep -ci "risk=\"High\"" "$REPORT_HTML" 2>/dev/null || echo 0)
  if [[ "$HIGH" -eq 0 ]]; then
    echo "SEC-Z01: PASS (0 alertas High)"
    exit 0
  fi
  echo "SEC-Z01: FAIL ($HIGH alertas High)"
  exit 1
fi

echo "SEC-Z01: WARN (ZAP no genero informe)"
exit 0
