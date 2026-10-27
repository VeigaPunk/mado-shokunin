#!/bin/sh
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
S=/fast/scratch/hyaku/mado-r50/L1Freeze
DATA=906178b607f2071af7c2efec5aad976a8bfa5757
BASE=8ae47b957034ae21012bbf09173cca2c48be345e
export TMPDIR=$S
rm -rf "$S/fx2" && git clone -q --shared "$LANE" "$S/fx2"
[ "$(git -C "$S/fx2" rev-parse --show-toplevel)" = "$S/fx2" ] || { echo TOPLEVEL-MISMATCH; exit 2; }
git -C "$S/fx2" checkout -q --detach "$DATA"

run() { # name rev nonce
  echo "== $1 ($2) nonce=$3"
  python3 -I "$LANE/quality/counters/c2-r50-session-gate.py" --repo "$S/fx2" --rev "$2" --work "$S/work-$3" --nonce "$3"; echo "exit=$?"
}

# control: v2 gate at base (rules blind to new shapes)
run c2-c00-v2-at-base "$BASE" 602211
git -C "$S/fx2" checkout -q --detach "$DATA"

# control: stub gate (flags every line; over-flagging green shapes)
python3 - "$S/fx2" <<'PY'
import sys, re
p = sys.argv[1] + "/quality/check-session-material.py"
src = open(p).read()
i = src.find("def scan_blob(")
j = src.find("def serials_from_json(")
assert 0 < i < j
stub_body = '''def scan_blob(data, home_limit, serials=(), account="", cache_fields=DEFAULT_CACHE_FIELDS):
    """CONTROL c2-stub: flag every non-empty line with R7 (over-flagging gate)."""
    text = decode(data)
    if text is None:
        return []
    n = sum(1 for line in text.splitlines() if line.strip())
    if not n:
        return []
    return [(R7, n, "forms=prefix:%d,header:0,diag:0,row:0 paths=0" % n)]

'''
open(p, "w").write(src[:i] + stub_body + src[j:])
PY
git -C "$S/fx2" add quality/check-session-material.py && git -C "$S/fx2" -c user.name=fixture -c user.email=fx@fixture commit -q -m "control c2-stub"
RSTUB=$(git -C "$S/fx2" rev-parse HEAD)
run c2-c12-stub "$RSTUB" 602211
git -C "$S/fx2" checkout -q --detach "$DATA"

# control: v3 rules with ufo default scope (blind outside .ufo)
python3 - "$S/fx2" <<'PY'
import sys
p = sys.argv[1] + "/quality/check-session-material.py"
src = open(p).read()
old = 'DEFAULT_SCOPE = "all"'
if old not in src:
    old = "DEFAULT_SCOPE = 'all'"
assert old in src, "DEFAULT_SCOPE literal not found"
open(p, "w").write(src.replace(old, old.replace("all", "ufo"), 1))
PY
git -C "$S/fx2" add quality/check-session-material.py && git -C "$S/fx2" -c user.name=fixture -c user.email=fx@fixture commit -q -m "control c2-v3-ufo-default"
RUFO=$(git -C "$S/fx2" rev-parse HEAD)
run c2-c14-v3-ufo-default "$RUFO" 602211
