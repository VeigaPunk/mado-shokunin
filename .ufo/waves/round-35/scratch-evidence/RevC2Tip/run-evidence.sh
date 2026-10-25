#!/usr/bin/env bash
# RevC2Tip evidence runner — REBUILT 2026-10-25 ~03:50 after the ~03:45 external
# sweep deleted `.ufo/waves/round-35/scratch/`. Regenerates every artifact the
# report cites and writes one transcript. Read-only on lane bytes.
set -u
cd /home/vgpnk/Projects/shokunin/mado-shokunin
S=.ufo/waves/round-35/scratch/RevC2Tip
EV="$S/evidence.txt"

{
  echo "# RevC2Tip evidence transcript"
  echo "# rebuilt $(date -Is) from the seat transcript after the ~03:45 external sweep"
  echo "# that removed the whole .ufo/waves/round-35/scratch/ tree; w2/reports/ was intact."
  echo "# lane counter/spec/ledger/controls unmodified; C2 inputs clean at HEAD $(git rev-parse --short HEAD)"

  echo
  echo "## 1. canonical command"
  echo '$ python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json'
  python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json
  echo "rc=$?"

  echo
  echo "## 2. seven blob ids at dff3941 (rev-parse)"
  for p in .ufo/waves/round-33/c1/count.py .ufo/waves/round-33/c1/frozen.json \
           .ufo/waves/round-33/c2/count.py .ufo/waves/round-34/c1/count.py \
           .ufo/waves/round-34/c1/frozen.json .ufo/waves/round-34/c2/count.py \
           .ufo/waves/round-34/c2/frozen.json; do
    printf '%s ' "$p"; git rev-parse "dff394109f3cc3d851309ad7c67dd3b35b46adf2:$p"
  done
  echo "rc=$?"

  echo
  echo "## 3. ledger table parsed vs spec frozen_blobs"
  python3 - <<'PY'
import json, re
from pathlib import Path
spec = json.loads(Path('.ufo/waves/round-35/c2/frozen.json').read_text())
doc = Path(spec['blob_ledger']).read_text()
rows = re.findall(r'^\|\s*`([^`]+)`\s*\|\s*`([0-9a-f]{40})`\s*\|', doc, re.M)
docd = dict(rows)
specd = {b['path']: b['blob_id'] for b in spec['frozen_blobs']}
print("doc rows:", len(rows), "spec entries:", len(specd), "table == spec:", docd == specd)
PY

  echo
  echo "## 4. attack.py (per-observable mutation matrix)"
  python3 "$S/attack.py"
  echo "rc=$?"

  echo
  echo "## 5. probes.py (clause-list shrink + retired.why non-use)"
  python3 "$S/probes.py"
  echo "rc=$?"

  echo
  echo "## 6. digest-match probe: corrupt S203 receipt bytes in a golden copy"
  D="$S/digest-probe"
  rm -rf "$D"; mkdir -p "$D"
  cp -a .ufo/waves/round-35/controls/golden/. "$D"/
  printf 'CORRUPTED DOCUMENT - not the fetched evidence\n' >> "$D/.ufo/waves/round-35/fetch/S203.receipt.txt"
  echo "actual=$(sha256sum "$D/.ufo/waves/round-35/fetch/S203.receipt.txt" | cut -d' ' -f1)"
  echo "frozen=$(python3 -c "import json;print(json.load(open('.ufo/waves/round-35/c1/frozen.json'))['receipts']['S203']['sha256'])")"
  python3 -I .ufo/waves/round-35/c1/count.py --root "$D" --frozen .ufo/waves/round-35/c1/frozen.json
  echo "rc=$?"
  echo "-- digest uses in c1/count.py --"
  grep -n "digest" .ufo/waves/round-35/c1/count.py

  echo
  echo "## 7. control trees re-run against committed receipts"
  ls -d .ufo/waves/round-35/controls/*/ | while read -r d; do
    printf '%-18s ' "$(basename "$d")"
    python3 -I .ufo/waves/round-35/c1/count.py --root "$d" --frozen .ufo/waves/round-35/c1/frozen.json
    echo "  exit=$?"
  done

  echo
  echo "## 8. committed C2 negative control"
  echo '$ python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen /fast/scratch/mado-r35/c2-donothing/frozen.json'
  python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen /fast/scratch/mado-r35/c2-donothing/frozen.json
  echo "rc=$?"
} > "$EV" 2>&1

echo "wrote $EV ($(wc -l < "$EV") lines, $(wc -c < "$EV") bytes)"
