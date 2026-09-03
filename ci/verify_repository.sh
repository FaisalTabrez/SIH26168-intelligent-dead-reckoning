#!/usr/bin/env sh
set -eu
python3 "$(dirname "$0")/verify_repository.py" "${1:-all}"
