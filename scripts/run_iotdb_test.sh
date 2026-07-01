#!/usr/bin/env bash




set -euo pipefail

if [[ $
  echo "Usage: $0 <Test>" >&2
  echo "  Example: $0 \"BPTest
  exit 1
fi

TEST=$1
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IOTDB_DIR="$ROOT/iotdb"

if [[ ! -d "$IOTDB_DIR" ]]; then
  echo "Missing iotdb checkout at $IOTDB_DIR (run ./scripts/bootstrap_env.sh first)." >&2
  exit 1
fi

cd "$IOTDB_DIR"
mvn test -pl iotdb-core/tsfile \
  "-Dtest=$TEST" \
  "-Dcheckstyle.skip=true" \
  "-Dmaven.checkstyle.skip=true" \
  "-Dspotless.check.skip=true"
