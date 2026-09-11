#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
[ -f .env ] || cp .env.example .env
set -a; . ./.env; set +a

docker compose up -d db
until docker compose exec -T db pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" >/dev/null 2>&1; do sleep 1; done

docker compose run --rm odoo \
  --database "$ODOO_DB" \
  --init acme_ems_demo \
  --without-demo=all \
  --stop-after-init

docker compose up -d odoo
echo "ACME EMS Odoo is available at http://localhost:${ODOO_PORT:-8069}"
