#!/usr/bin/env bash
# Comprueba que xmedical quede operativo tras reinicio (ejecutar como root).
set -euo pipefail

fail=0
ok() { echo "OK  $*"; }
err() { echo "FAIL $*"; fail=1; }

systemctl is-enabled docker >/dev/null 2>&1 && ok "docker enabled" || err "docker no enabled"
systemctl is-enabled apache2 >/dev/null 2>&1 && ok "apache2 enabled" || err "apache2 no enabled"
systemctl is-enabled xmedical >/dev/null 2>&1 && ok "xmedical enabled" || err "xmedical no enabled"

for c in xmedical-db-1 xmedical-redis-1; do
  if docker inspect "$c" --format '{{.State.Running}} {{.HostConfig.RestartPolicy.Name}}' 2>/dev/null | grep -q '^true unless-stopped$'; then
    ok "contenedor $c (running, unless-stopped)"
  else
    err "contenedor $c (revisar estado o restart policy)"
  fi
done

/var/www/xmedical/venv/bin/python /var/www/xmedical/scripts/wait_for_tcp.py 127.0.0.1 5432 5 || err "PostgreSQL 5432"
/var/www/xmedical/venv/bin/python /var/www/xmedical/scripts/wait_for_tcp.py 127.0.0.1 6379 5 || err "Redis 6379"

if systemctl is-active --quiet xmedical; then
  ok "gunicorn xmedical active"
else
  err "gunicorn xmedical inactive"
fi

code=$(curl -s -o /dev/null -w '%{http_code}' -H 'Host: xmedical.cloud' http://127.0.0.1:8000/auth/login/ || true)
[[ "$code" == "200" ]] && ok "HTTP login $code" || err "HTTP login $code"

exit "$fail"
