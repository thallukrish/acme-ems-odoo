#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 tests/validate_source.py
grep -q 'image: odoo:19.0' docker-compose.yml
grep -q 'image: postgres:16' docker-compose.yml
echo 'smoke validation passed'
