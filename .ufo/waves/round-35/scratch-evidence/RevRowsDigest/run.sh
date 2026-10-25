#!/bin/sh
# RevRowsDigest — round-35 w2 reproduction driver. Read-only on the lane:
# every mutation happens under this scratch dir; the lane tree is only read.
# Usage: sh .ufo/waves/round-35/scratch/RevRowsDigest/run.sh
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
S=$LANE/.ufo/waves/round-35/scratch/RevRowsDigest
FZ=$LANE/.ufo/waves/round-35/c1/frozen.json
CNT=$LANE/.ufo/waves/round-35/c1/count.py
PY="python3 -I"
cd "$LANE" || exit 2

echo "=== 0. baseline (live lane) ==="
$PY "$CNT" --root . --frozen "$FZ"; echo "exit=$?"

echo
echo "=== 1. per-receipt: working tree vs frozen vs HEAD blob ==="
for s in S203 S204 S205 S206 S207 S208 S209 S210; do
  wt=$(sha256sum ".ufo/waves/round-35/fetch/$s.receipt.txt" | cut -d' ' -f1)
  hd=$(git cat-file -p "HEAD:.ufo/waves/round-35/fetch/$s.receipt.txt" | sha256sum | cut -d' ' -f1)
  fz=$(python3 -I -c "import json;print(json.load(open('$FZ'))['receipts']['$s']['sha256'])")
  anc=$(grep -E "^\| $s \|" corpus/SOURCES.md | awk -F'|' '{print $7}' | grep -o 'receipt .*sha256 [0-9a-f]\{64\}' | grep -o '[0-9a-f]\{64\}$')
  v1=$([ "$wt" = "$fz" ] && echo OK || echo MISMATCH)
  v2=$([ "$hd" = "$fz" ] && echo OK || echo MISMATCH)
  v3=$([ "$anc" = "$fz" ] && echo OK || echo MISMATCH)
  echo "$s wt=$v1 head=$v2 anchor=$v3 wt=$wt"
done

echo
echo "=== 2. anchor rows at the freeze commit ==="
echo -n "rows S203-S210 in HEAD:corpus/SOURCES.md: "
git show HEAD:corpus/SOURCES.md | grep -cE '^\| S2(0[3-9]|10) '
echo -n "rows in worktree: "
grep -cE '^\| S2(0[3-9]|10) ' corpus/SOURCES.md
echo "worktree diff vs HEAD (numstat):"
git diff HEAD --numstat -- corpus/SOURCES.md
echo "receipts diff vs HEAD (numstat, empty = identical):"
git diff HEAD --numstat -- .ufo/waves/round-35/fetch/

echo
echo "=== 3. falsifiers: mutations the C1 counter does not see ==="
rm -rf "$S/m1" "$S/m2" "$S/m3" "$S/m4" "$S/m5"
for m in m1 m2 m3 m4 m5; do cp -r "$S/tree" "$S/$m"; done
cp "$FZ" "$S/m5/frozen.json"
python3 -I - <<PY
import pathlib, hashlib, json
S = pathlib.Path("$S")
FROZEN = json.loads(pathlib.Path("$FZ").read_text())

# m1: receipt bytes change after freeze; anchor and frozen untouched.
p = S/"m1/.ufo/waves/round-35/fetch/S210.receipt.txt"
p.write_bytes(p.read_bytes() + b"\nMUTATED-AFTER-FREEZE\n")
print("m1 S210 actual sha", hashlib.sha256(p.read_bytes()).hexdigest(), "frozen", FROZEN["receipts"]["S210"]["sha256"])

# m2: anchor names a different receipt file, keeps its own frozen digest.
q = S/"m2/corpus/SOURCES.md"; t = q.read_text()
old = "receipt .ufo/waves/round-35/fetch/S207.receipt.txt sha256 81c33e7926f0bad071d31e9fc67e1d06967e3142da40ea3c93b16510b0adec59"
new = "receipt .ufo/waves/round-35/fetch/S208.receipt.txt sha256 81c33e7926f0bad071d31e9fc67e1d06967e3142da40ea3c93b16510b0adec59"
assert t.count(old) == 1; q.write_text(t.replace(old, new))

# m3: anchor names no file at all, keeps the digest.
r = S/"m3/corpus/SOURCES.md"; t = r.read_text()
old = "section per-copy handler count in .ufo/waves/round-35/fetch/S209.receipt.txt; receipt sha256"
new = "section per-copy handler count; anonymous sha256"
assert t.count(old) == 1; r.write_text(t.replace(old, new))

# m4: host-file digest in the anchor replaced with another file's digest.
u = S/"m4/corpus/SOURCES.md"; t = u.read_text()
old = "6354 B, file sha256 a408a33df48a39dc16214124dd0b86d6ab03e13802bac173146ae8a858aae829"
new = "6354 B, file sha256 6d8d2c11d3c3b15fa0aa31a830410c98d9e630a7683a9cedffb888d10f0f1750"
assert t.count(old) == 1; u.write_text(t.replace(old, new))

# m5: receipt mutated, anchor and frozen both re-pointed at the new bytes (laundering).
v = S/"m5/.ufo/waves/round-35/fetch/S208.receipt.txt"
v.write_bytes(v.read_bytes() + b"\nLAUNDERED\n")
h = hashlib.sha256(v.read_bytes()).hexdigest()
w = S/"m5/corpus/SOURCES.md"; x = w.read_text()
w.write_text(x.replace("6e72f0db3d7bbfecf4096b0aa22f716f417c00caa50b6d3319106387d6ce4654", h))
f = S/"m5/frozen.json"; d = json.loads(f.read_text())
d["receipts"]["S208"]["sha256"] = h; f.write_text(json.dumps(d, indent=1))
print("m5 S208 new sha", h, "anchor+frozen re-pointed")
PY
for m in m1 m2 m3 m4; do
  echo "-- $m (lane frozen.json) --"
  $PY "$CNT" --root "$S/$m" --frozen "$FZ"; echo "exit=$?"
done
echo "-- m5 (doubly re-pointed frozen.json) --"
$PY "$CNT" --root "$S/m5" --frozen "$S/m5/frozen.json"; echo "exit=$?"

echo
echo "=== 4. clause the digest test actually implements ==="
grep -n "receipt\[.sha256.\] in cs\[5\]\|digest = hashlib" "$CNT"
echo "-- is 'digest' ever read again? (grep count) --"
grep -cw digest "$CNT"
