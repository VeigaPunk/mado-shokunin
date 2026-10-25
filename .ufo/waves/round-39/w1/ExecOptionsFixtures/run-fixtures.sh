#!/usr/bin/env bash
# ExecOptionsFixtures — fixture evidence runner for tools/mado-options.py (C2).
#
# Runs the tool over the synthetic trees and compares its output to expected.json.
# Prints `fixtures=N/N` (N = passing fixtures, total = all fixtures) and exits 0
# iff every fixture expectation matches.
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LANE="$(cd "$HERE/../../../../.." && pwd)"
TOOL="$LANE/tools/mado-options.py"
MAIN="$HERE/trees/main-home"
FIFO_HOME="$HERE/trees/fifo-home"
DANG_HOME="$HERE/trees/dangling-home"

mkdir -p "$HERE/observed"

pass=0
total=0

# cmp_rows EXPECTED ACTUAL MODE HOME — strict row comparison, order-insensitive by key.
cmp_rows() {
  python3 -I - "$1" "$2" "$3" "$4" <<'PY'
import json, sys, os
exp_path, act_path, mode, home = sys.argv[1], sys.argv[2], sys.argv[3], os.path.abspath(sys.argv[4])

def norm(rows):
    out = []
    for r in rows:
        rr = dict(r)
        o = rr.get("owner")
        if isinstance(o, str):
            if o.startswith(home):
                o = o[len(home):].lstrip("/")
            o = o.replace("\\", "/").lstrip("./")
            rr["owner"] = o
        # a JSON null field is the same as an absent field
        rr = {k: v for k, v in rr.items() if v is not None}
        out.append(rr)
    return out

exp = {r["key"]: r for r in norm(json.load(open(exp_path))[mode])}
act = {r["key"]: r for r in norm(json.load(open(act_path)))}
bad = 0
for k in sorted(set(exp) ^ set(act)):
    where = "expected-only" if k in exp else "actual-only"
    print("KEYSET %s %s" % (k, where))
    bad += 1
for k in sorted(exp):
    if k in act and act[k] != exp[k]:
        bad += 1
        for f in sorted(set(exp[k]) | set(act[k])):
            if exp[k].get(f) != act[k].get(f):
                print("DIFF %s %s expected=%r actual=%r" % (k, f, exp[k].get(f), act[k].get(f)))
sys.exit(1 if bad else 0)
PY
}

# --- fixture 1: static option table over the main chain tree ---
total=$((total + 1))
if [ ! -f "$TOOL" ]; then
  echo "FAIL fixture1 tool-missing: $TOOL"
else
  timeout 30 python3 -I "$TOOL" --home "$MAIN" \
    >"$HERE/observed/treeA-static.json" 2>"$HERE/observed/treeA-static.err"
  rc=$?
  if [ "$rc" -ne 0 ]; then
    echo "FAIL fixture1 run rc=$rc"
    cat "$HERE/observed/treeA-static.err"
  elif cmp_rows "$HERE/expected.json" "$HERE/observed/treeA-static.json" static "$MAIN"; then
    pass=$((pass + 1))
  else
    echo "FAIL fixture1 expectation mismatch"
  fi
fi

# --- fixture 2: --getoption live merge over the same tree ---
total=$((total + 1))
timeout 30 python3 -I "$TOOL" --home "$MAIN" --getoption "$MAIN/.config/hypr/live.json" \
  >"$HERE/observed/treeA-getoption.json" 2>"$HERE/observed/treeA-getoption.err"
rc=$?
if [ "$rc" -ne 0 ]; then
  echo "FAIL fixture2 run rc=$rc"
  cat "$HERE/observed/treeA-getoption.err"
elif cmp_rows "$HERE/expected.json" "$HERE/observed/treeA-getoption.json" getoption "$MAIN"; then
  pass=$((pass + 1))
else
  echo "FAIL fixture2 expectation mismatch"
fi

# --- fixture 3: strict-file refusal — source targets a FIFO ---
total=$((total + 1))
rm -f "$FIFO_HOME/.config/hypr/pipe.conf"
mkfifo "$FIFO_HOME/.config/hypr/pipe.conf"
timeout 15 python3 -I "$TOOL" --home "$FIFO_HOME" \
  >"$HERE/observed/fifo.out" 2>"$HERE/observed/fifo.err"
rc=$?
if [ "$rc" -eq 0 ]; then
  echo "FAIL fixture3 fifo accepted (rc=0, must refuse)"
elif grep -q "pipe.conf" "$HERE/observed/fifo.out" "$HERE/observed/fifo.err"; then
  pass=$((pass + 1))
else
  echo "FAIL fixture3 fifo refusal unnamed (rc=$rc)"
  cat "$HERE/observed/fifo.out" "$HERE/observed/fifo.err"
fi

# --- fixture 4: strict-file refusal — source is a dangling symlink ---
total=$((total + 1))
rm -f "$DANG_HOME/.config/hypr/gone.conf"
ln -s /nonexistent-target "$DANG_HOME/.config/hypr/gone.conf"
timeout 15 python3 -I "$TOOL" --home "$DANG_HOME" \
  >"$HERE/observed/dangling.out" 2>"$HERE/observed/dangling.err"
rc=$?
if [ "$rc" -eq 0 ]; then
  echo "FAIL fixture4 dangling accepted (rc=0, must refuse)"
elif grep -q "gone.conf" "$HERE/observed/dangling.out" "$HERE/observed/dangling.err"; then
  pass=$((pass + 1))
else
  echo "FAIL fixture4 dangling refusal unnamed (rc=$rc)"
  cat "$HERE/observed/dangling.out" "$HERE/observed/dangling.err"
fi

echo "fixtures=${pass}/${total}"
[ "$pass" -eq "$total" ] && [ "$total" -gt 0 ]
