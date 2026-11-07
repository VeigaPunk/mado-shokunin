#!/usr/bin/env bash
# round-95 L1: C1 pre-freeze controls (DRAFT runs of the frozen counter on the frozen inputs).
# usage (lane root): bash .ufo/waves/round-95/controls/c1-prefreeze-r95.sh SCRATCH OUT [candidate...]
set -u
S=$1; OUT=$2; shift 2
R=.ufo/waves/round-95
sha() { sha256sum "$1" | cut -c1-64; }
mkdir -p "$S"
: > "$OUT"
for cand in "$@"; do
  echo "## DRAFT candidate $cand sha256=$(sha "$cand")" >> "$OUT"
  python3 -I quality/counters/c1-r95-mimesniff.py --repo . --rev master \
    --base-rev 4a2af6817024f6ed47084a5217c1825ae247f4fe \
    --cases $R/controls/mimesniff-cases-r95-frozen.json --expect-cases-sha256 "$(sha $R/controls/mimesniff-cases-r95-frozen.json)" \
    --mutants $R/controls/mimesniff-mutants-r95-frozen.json --expect-mutants-sha256 "$(sha $R/controls/mimesniff-mutants-r95-frozen.json)" \
    --oracle-src $R/controls/mimesniff-oracle-r95.c --expect-oracle-sha256 "$(sha $R/controls/mimesniff-oracle-r95.c)" \
    --fresh-gen $R/controls/mimesniff-fresh-r95.py --expect-fresh-gen-sha256 "$(sha $R/controls/mimesniff-fresh-r95.py)" \
    --host-files $R/controls/mimesniff-host-files-r95.txt --expect-host-files-sha256 "$(sha $R/controls/mimesniff-host-files-r95.txt)" \
    --expect-tool-sha256 "$(sha $R/build/mado-mimesniff.c1c.py)" \
    --expect-mimeglob-sha256 65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453 \
    --forgery $R/controls/forgery-sibling-ctypes-r95.py --expect-forgery-sha256 "$(sha $R/controls/forgery-sibling-ctypes-r95.py)" \
    --fresh 120 --workers 28 --scratch-root "$S" --draft-tool "$cand" > "$S/run.log" 2>&1
  rc=$?
  grep -vE '^mutant .* killed by' "$S/run.log" >> "$OUT"
  echo "rc=$rc" >> "$OUT"
done
