#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
PAPER="$REPO_ROOT/paper/stephenson-et-al-2026-autocatalytic-governance.md"
OUTPUT="$REPO_ROOT/paper/stephenson-et-al-2026-autocatalytic-governance.pdf"

pandoc "$PAPER" \
  -o "$OUTPUT" \
  --pdf-engine=lualatex \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V documentclass=article \
  -V colorlinks=true \
  -V linkcolor=blue \
  -V urlcolor=blue \
  --number-sections \
  --standalone \
  -V mainfont="DejaVu Serif" \
  -V sansfont="DejaVu Sans" \
  -V monofont="DejaVu Sans Mono" \
  -V header-includes='\usepackage{booktabs}\usepackage{longtable}'

echo "Built: $OUTPUT"
