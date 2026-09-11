#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
docker compose down -v --remove-orphans
exec "$ROOT/scripts/init-demo.sh"
