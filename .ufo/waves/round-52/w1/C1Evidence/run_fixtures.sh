#!/bin/bash
set -u
ROOT=/fast/scratch/hyaku/mado-r52/C1Evidence
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
BASE=85d57a818c3707397e21c840b6498b105ba798aa
CTRL=$LANE/.ufo/waves/round-52/controls/c1-do-nothing.md
export TMPDIR=$ROOT/tmp
mkdir -p "$TMPDIR"

mkfix () { # $1=dir
  rm -rf "$1"; mkdir -p "$1" "$1/tools" "$1/quality"
  git -C "$1" init -q
  git -C "$1" config user.email fixture@local
  git -C "$1" config user.name fixture
}

topof () { git -C "$1" rev-parse --show-toplevel; }
assert_top () { # $1=dir
  t=$(topof "$1") || { echo "ASSERT-FAIL: no toplevel for $1"; exit 9; }
  [ "$t" = "$1" ] || { echo "ASSERT-FAIL: toplevel=$t want=$1"; exit 9; }
}

echo "== fixture A: committed control bytes at the production ledger path, vs committed checker"
A=$ROOT/fix-a
mkfix "$A"
printf '#!/bin/sh\ntrue\n' > "$A/tools/mado-verify.sh"; chmod +x "$A/tools/mado-verify.sh"
cp "$CTRL" "$A/quality/tool-ledger.md"
git -C "$A" add -A; git -C "$A" commit -q -m fixture-a
assert_top "$A"
echo "\$ git -C $A rev-parse --show-toplevel"; topof "$A"
echo "\$ python3 -I $LANE/quality/check-tool-ledger.py --repo $A --rev HEAD"
python3 -I "$LANE/quality/check-tool-ledger.py" --repo "$A" --rev HEAD; echo "exit=$?"

echo
echo "== fixture B: committed control bytes vs round-51 counter (unchanged)"
echo "\$ python3 -I $LANE/quality/counters/c1-r51-ledger.py --repo $A --rev HEAD --work $ROOT/work-b"
python3 -I "$LANE/quality/counters/c1-r51-ledger.py" --repo "$A" --rev HEAD --work "$ROOT/work-b"; echo "exit=$?"

echo
echo "== fixture C: grammar-compatible no-work ledger (3 cells, self-pointer, generic description)"
C=$ROOT/fix-c
mkfix "$C"
printf '#!/bin/sh\ntrue\n' > "$C/tools/mado-verify.sh"; chmod +x "$C/tools/mado-verify.sh"
git -C "$LANE" show $BASE:quality/check-tool-ledger.py > "$C/quality/check-tool-ledger.py"
cat > "$C/quality/tool-ledger.md" <<'MD'
| instrument | description | accountability pointer |
|---|---|---|
| `tools/mado-verify.sh` | Generic accountability pointer to this ledger itself. | `quality/tool-ledger.md` |
| `quality/check-tool-ledger.py` | Generic accountability pointer to this ledger itself. | `quality/tool-ledger.md` |
MD
git -C "$C" add -A; git -C "$C" commit -q -m fixture-c
assert_top "$C"
echo "\$ git -C $C rev-parse --show-toplevel"; topof "$C"
echo "\$ python3 -I $LANE/quality/check-tool-ledger.py --repo $C --rev HEAD"
python3 -I "$LANE/quality/check-tool-ledger.py" --repo "$C" --rev HEAD; echo "exit=$?"
echo "\$ python3 -I $LANE/quality/counters/c1-r51-ledger.py --repo $C --rev HEAD --work $ROOT/work-c"
python3 -I "$LANE/quality/counters/c1-r51-ledger.py" --repo "$C" --rev HEAD --work "$ROOT/work-c"; echo "exit=$?"
echo
echo "== fixture C content (verifiable bytes)"
echo "\$ cat $C/quality/tool-ledger.md"
cat "$C/quality/tool-ledger.md"
echo "\$ sha256sum $C/quality/tool-ledger.md"; sha256sum "$C/quality/tool-ledger.md"
