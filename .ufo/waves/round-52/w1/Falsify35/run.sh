#!/usr/bin/env bash
# Falsify35 reproducible driver -- round-52 C1 no-work control validity.
# Source-only: reads base-revision bytes via `git archive`; no host/live probes.
# Writes only under $F35_SCRATCH (default /fast/scratch/hyaku/mado-r52/Falsify35).
set +e

LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
BASE=85d57a818c3707397e21c840b6498b105ba798aa
W=${F35_SCRATCH:-/fast/scratch/hyaku/mado-r52/Falsify35}
CTL="$LANE/.ufo/waves/round-52/controls/c1-do-nothing.md"
HERE=$(cd "$(dirname "$0")" && pwd)
HOLLOW="$HERE/f35-hollow.py"

export TMPDIR="$W/work"
mkdir -p "$W/work"

run() { out=$(python3 "$@" 2>&1); rc=$?; printf '%s\nrc=%s\n' "$out" "$rc"; }

echo "### 0. pinned inputs"
sha256sum "$CTL"
git -C "$LANE" rev-parse "$BASE"
git -C "$LANE" cat-file -e "$BASE:.ufo/waves/round-52/controls/c1-do-nothing.md" 2>&1 | head -2
git -C "$LANE" cat-file -e "HEAD:.ufo/waves/round-52/controls/c1-do-nothing.md" 2>&1 | head -2
git -C "$LANE" ls-tree -r --name-only "$BASE" -- quality/counters | grep -c 'r52'

echo
echo "### 1. base-revision snapshot (read-only source bytes)"
rm -rf "$W/repo-prod" "$W/repo-ctl-tracked" "$W/repo-ctl-path" "$W/repo-fix-c" "$W/repo-fix-d" "$W/fixture-git"
mkdir -p "$W/repo-prod"
git -C "$LANE" archive "$BASE" | tar -x -C "$W/repo-prod"
sha256sum "$W/repo-prod/quality/tool-ledger.md" "$W/repo-prod/quality/check-tool-ledger.py" \
          "$W/repo-prod/quality/counters/c1-r51-ledger.py"

echo
echo "### 2. table shape: production ledger vs frozen control (column counts)"
echo -n "production data-row cells: "; awk -F'|' '/^\| *`/{print NF-2}' "$W/repo-prod/quality/tool-ledger.md" | sort | uniq -c | tr '\n' ' '; echo
echo -n "control rows: ";     awk -F'|' '/^\|/{print NF-2}' "$CTL" | sort | uniq -c | tr '\n' ' '; echo
echo "production header:"; grep -n '^| instrument' "$W/repo-prod/quality/tool-ledger.md"
echo "control header:";    head -1 "$CTL"

echo
echo "### 3. control materialised at the tracked ledger path (no-work ledger semantics)"
cp -a "$W/repo-prod/." "$W/repo-ctl-tracked/"
cp "$CTL" "$W/repo-ctl-tracked/quality/tool-ledger.md"
cat -A "$W/repo-ctl-tracked/quality/tool-ledger.md"

echo
echo "### 4. control left at its delivered path (path-parameterised self check)"
cp -a "$W/repo-prod/." "$W/repo-ctl-path/"
mkdir -p "$W/repo-ctl-path/.ufo/waves/round-52/controls"
cp "$CTL" "$W/repo-ctl-path/.ufo/waves/round-52/controls/c1-do-nothing.md"

echo
echo "### 5. fixture C: 2 committed-grammar rows, self-pointers, generic description"
cp -a "$W/repo-prod" "$W/repo-fix-c"
cat > "$W/repo-fix-c/quality/tool-ledger.md" <<'EOF'
# fixture C: 2-row generic self-pointer ledger (committed grammar)
| instrument | description | accountability pointer |
|---|---|---|
| `tools/mado-verify.sh` | generic accountability pointer to this ledger itself. | `quality/tool-ledger.md` |
| `tools/mado-binds.py` | generic accountability pointer to this ledger itself. | `quality/tool-ledger.md` |
EOF
cat "$W/repo-fix-c/quality/tool-ledger.md"

echo
echo "### 6. fixture D: population-shaped (82 rows) generic self-pointer ledger"
cp -a "$W/repo-prod" "$W/repo-fix-d"
python3 - "$W" <<'PY'
import os, sys
W = sys.argv[1]
root = os.path.join(W, "repo-prod"); pop = []
for dp, dn, fn in os.walk(root):
    rel = os.path.relpath(dp, root); rel = "" if rel == "." else rel
    for n in fn:
        p = n if not rel else rel + "/" + n
        if p.startswith("tools/") or (p.startswith("quality/") and p.count("/") == 1 and p.endswith(".py")) \
           or (p.startswith("quality/counters/") and p.endswith(".py")):
            pop.append(p)
pop = sorted(set(pop))
out = ["# fixture D: population-shaped generic self-pointer ledger (committed grammar)\n",
       "| instrument | description | accountability pointer |\n|---|---|---|\n"]
for p in pop:
    out.append("| `%s` | generic accountability pointer to this ledger itself. | `quality/tool-ledger.md` |\n" % p)
open(os.path.join(W, "repo-fix-d/quality/tool-ledger.md"), "w").write("".join(out))
print("fixture_d_rows=%d population=%d" % (len(pop), len(pop)))
PY

echo
echo "### 7. seat-local instrument matrix (count implements none of the three clauses;"
echo "###    unique implements only uniqueness; semantic implements uniqueness+resolution+"
echo "###    non-self with the instrument-specific context check STUBBED to True)"
for mode in count unique semantic; do
  echo "--- prod/$mode";        run "$HOLLOW" --root "$W/repo-prod"        --ledger quality/tool-ledger.md --mode $mode
done
for mode in count unique semantic; do
  echo "--- ctl-tracked/$mode"; run "$HOLLOW" --root "$W/repo-ctl-tracked" --ledger quality/tool-ledger.md --mode $mode
done
echo "--- ctl-path/semantic (self = ledger argument)"
run "$HOLLOW" --root "$W/repo-ctl-path" --ledger .ufo/waves/round-52/controls/c1-do-nothing.md --mode semantic
echo "--- ctl-path/semantic (self = tracked ledger path)"
run "$HOLLOW" --root "$W/repo-ctl-path" --ledger .ufo/waves/round-52/controls/c1-do-nothing.md --self quality/tool-ledger.md --mode semantic
for mode in count unique semantic; do
  echo "--- fix-c/$mode"; run "$HOLLOW" --root "$W/repo-fix-c" --ledger quality/tool-ledger.md --mode $mode
done
for mode in count unique semantic; do
  echo "--- fix-d/$mode"; run "$HOLLOW" --root "$W/repo-fix-d" --ledger quality/tool-ledger.md --mode $mode
done

echo
echo "### 8. committed base checker on production and on the frozen control at the tracked path"
F="$W/fixture-git"
cp -a "$W/repo-ctl-tracked" "$F"
cd "$F" || exit 1
git init -q -b main . && git config user.name f35 && git config user.email f35@local \
  && git config commit.gpgsign false
cp "$W/repo-prod/quality/tool-ledger.md" "$F/quality/tool-ledger.md"
git add -A >/dev/null 2>&1; git commit -q -m base --no-verify
REV_BASE=$(git rev-parse HEAD)
cp "$W/repo-ctl-tracked/quality/tool-ledger.md" "$F/quality/tool-ledger.md"
git add -A >/dev/null 2>&1; git commit -q -m control --no-verify
REV_CTL=$(git rev-parse HEAD)
echo "fixture toplevel: $(git rev-parse --show-toplevel)"
echo "REV_BASE=$REV_BASE REV_CTL=$REV_CTL"
echo '--- base checker on production'
run "$W/repo-prod/quality/check-tool-ledger.py" --repo "$F" --rev "$REV_BASE"
echo '--- base checker on frozen control bytes'
run "$W/repo-prod/quality/check-tool-ledger.py" --repo "$F" --rev "$REV_CTL" | tail -3
cd "$W/repo-fix-d" || exit 1
git init -q -b main . && git config user.name f35 && git config user.email f35@local \
  && git config commit.gpgsign false && git add -A >/dev/null 2>&1 \
  && git commit -q -m fixture-d --no-verify
REV_FIXD=$(git rev-parse HEAD)
cd "$F" || exit 1
echo '--- base checker on fixture D (population-shaped no-work ledger)'
run "$W/repo-prod/quality/check-tool-ledger.py" --repo "$W/repo-fix-d" --rev "$REV_FIXD"

echo
echo "### 9. round-51 counter (declared by C1 as NOT measuring context) on both"
echo '--- r51 counter on production'
run "$W/repo-prod/quality/counters/c1-r51-ledger.py" --repo "$F" --rev "$REV_BASE" --work "$W/work/r51-base" | tail -3
echo '--- r51 counter on frozen control at tracked path'
run "$W/repo-prod/quality/counters/c1-r51-ledger.py" --repo "$F" --rev "$REV_CTL" --work "$W/work/r51-ctl" | tail -3

cd "$HERE" || exit 1
echo
echo "### done"
