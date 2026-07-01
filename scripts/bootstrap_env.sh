#!/usr/bin/env bash


set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing command: $1" >&2
    exit 1
  fi
}

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "Missing command: python3 (or python)" >&2
  exit 1
fi

need_cmd git

PY_VERSION="$("$PYTHON" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
PY_MAJOR="${PY_VERSION%%.*}"
PY_MINOR="${PY_VERSION#*.}"
if (( PY_MAJOR < 3 || (PY_MAJOR == 3 && PY_MINOR < 11) )); then
  echo "Need Python 3.11 or newer (found: $PY_VERSION)" >&2
  exit 1
fi

if [[ ! -d .venv ]]; then
  "$PYTHON" -m venv .venv
fi


source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt

clone_if_missing() {
  local dir=$1 url=$2 branch=${3:-}
  local path="$ROOT/$dir"
  if [[ -d "$path" ]]; then
    echo "Directory ${dir}/ already exists; skip clone."
    return
  fi
  if [[ -n "$branch" ]]; then
    git clone -b "$branch" --single-branch "$url" "$path"
  else
    git clone "$url" "$path"
  fi
}

clone_if_missing iotdb "https://anonymous.4open.science/r/iotdb-research-encoding-subcolumns"
clone_if_missing tsfile "https://anonymous.4open.science/r/tsfile-research-encoding-subcolumns"
clone_if_missing elf "https://github.com/Spatio-Temporal-Lab/elf.git" dev

echo ""
echo "Python venv ready:  source .venv/bin/activate"
echo "Repo root:          $ROOT"
echo ""
echo "Install JDK 17+ and Maven 3.6+ for Java benchmarks (README section 3.2)."
if command -v java >/dev/null 2>&1; then
  java -version 2>&1 | head -n 1
else
  echo "  java: not found"
fi
if command -v mvn >/dev/null 2>&1; then
  mvn -version | head -n 1
else
  echo "  mvn:  not found"
fi
