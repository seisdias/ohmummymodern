#!/usr/bin/env bash
set -e

MIN_COVERAGE=80

echo "==> Ejecutando tests con cobertura (mínimo ${MIN_COVERAGE}%)"

python -m pytest \
  -v \
  --tb=short \
  --cov=src/world \
  --cov-report=term-missing \
  --cov-fail-under=${MIN_COVERAGE}

echo "✅ Tests OK y cobertura >= ${MIN_COVERAGE}%"
