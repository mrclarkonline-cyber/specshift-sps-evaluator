#!/usr/bin/env bash
set -euo pipefail

echo "======================================================================="
echo "Orchestra / Fetch_ET Status"
echo "======================================================================="
echo

if [ -x tools/orchestra/orchestra_audit.py ]; then
  python3 tools/orchestra/orchestra_audit.py
else
  echo "MISSING tools/orchestra/orchestra_audit.py"
fi

echo
echo "======================================================================="
echo "Orchestra status complete."
echo "======================================================================="
