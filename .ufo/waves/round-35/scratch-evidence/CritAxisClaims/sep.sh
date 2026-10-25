#!/usr/bin/env bash
# Read-only-vs-lane separability probes. Writes only under this scratch dir.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
S=$LANE/.ufo/waves/round-35/scratch/CritAxisClaims
NOTES="idle-lock-never-asked-r12.md idle-lock-chain-armed-r14.md idle-lock-offered-in-the-bar-r15.md"

mk() {  # $1 = dir name
  rm -rf "$S/$1"
  git clone --shared --quiet "$LANE" "$S/$1"
}

copy_data() {  # full r35 working-tree data
  local d=$S/$1
  cp "$LANE/LOG.md" "$d/LOG.md"
  cp "$LANE/corpus/QUALITY.md" "$d/corpus/QUALITY.md"
  cp "$LANE/corpus/README.md" "$d/corpus/README.md"
  cp "$LANE/corpus/SOURCES.md" "$d/corpus/SOURCES.md"
  for n in $NOTES; do cp "$LANE/corpus/knowledge/$n" "$d/corpus/knowledge/$n"; done
}

run_c1() { python3 -I "$S/$1/.ufo/waves/round-35/c1/count.py" --root "$S/$1" --frozen "$S/$1/.ufo/waves/round-35/c1/frozen.json"; echo "  exit=$?"; }
run_c2() { python3 -I "$S/$1/.ufo/waves/round-35/c2/count.py" --repo "$S/$1" --frozen "$S/$1/.ufo/waves/round-35/c2/frozen.json"; echo "  exit=$?"; }

echo "== T0 base: all data present =="
mk t0; copy_data t0
run_c1 t0; run_c2 t0

echo "== T1 C2 with C1 claim data absent (no 3 entries, no S203-S210, no index rows) =="
mk t1; copy_data t1
git -C "$S/t1" show HEAD:corpus/SOURCES.md > "$S/t1/corpus/SOURCES.md"
git -C "$S/t1" show HEAD:corpus/README.md > "$S/t1/corpus/README.md"
for n in $NOTES; do rm -f "$S/t1/corpus/knowledge/$n"; done
run_c2 t1
echo "  (C1 must now fail, proving the data really is absent)"
run_c1 t1

echo "== T2 C1 with C2 artifacts absent (no round-35 c2 dir, no ledger dir) =="
mk t2; copy_data t2
rm -rf "$S/t2/.ufo/waves/round-35/c2" "$S/t2/.ufo/waves/round-35/ledger"
run_c1 t2

echo "== T3 C2 with the C1 clause ledger absent =="
mk t3; copy_data t3
rm -f "$S/t3/.ufo/waves/round-35/c1/clauses.json"
run_c2 t3

echo "== T4 C2 with C1 control receipts absent =="
mk t4; copy_data t4
rm -rf "$S/t4/.ufo/waves/round-35/controls"
run_c2 t4

echo "== T5 C2 with a phantom retired id (never existed in r34) =="
mk t5; copy_data t5
python3 - "$S/t5/.ufo/waves/round-35/c1/clauses.json" <<'PY'
import json, sys
p = sys.argv[1]
d = json.load(open(p))
d["retired"] = [{"id": "phantom-clause-never-in-r34", "why": "fabricated for the separability probe"}]
json.dump(d, open(p, "w"), indent=1)
PY
run_c2 t5

echo "== T6 C1 with the clause ledger and controls absent (C1 reads neither) =="
mk t6; copy_data t6
rm -rf "$S/t6/.ufo/waves/round-35/controls"; rm -f "$S/t6/.ufo/waves/round-35/c1/clauses.json"
run_c1 t6
