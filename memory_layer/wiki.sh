#!/usr/bin/env bash
set -euo pipefail

case "${1:-help}" in
  lint)
    python3 memory_layer/tools/memory_lint.py
    ;;

  status)
    echo "SpecShift Wiki Status"
    echo
    python3 memory_layer/tools/memory_lint.py
    echo
    git status --short
    ;;

  log)
    tail -n 80 memory_layer/logs/activity_log.md
    ;;

  index)
    sed -n '1,220p' memory_layer/wiki/index.md
    ;;

  help|*)
    cat <<'HELP'
SpecShift Wiki Commands

./memory_layer/wiki.sh lint     Run wiki lint checks
./memory_layer/wiki.sh status   Run lint and git status
./memory_layer/wiki.sh log      Show recent wiki activity log
./memory_layer/wiki.sh index    Show wiki index
HELP
    ;;
esac
