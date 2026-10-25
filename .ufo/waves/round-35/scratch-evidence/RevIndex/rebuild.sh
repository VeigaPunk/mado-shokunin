#!/bin/bash
# Rebuild of RevIndex evidence after the external sweep of .ufo/waves/round-35/scratch/ (~03:45).
# Everything below is regenerated from this seat's transcript commands; outputs are fresh runs.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
S=$LANE/.ufo/waves/round-35/scratch/RevIndex
Q=$LANE/quality/check-index.py
QR=$LANE/quality/check-index-rows.py
mkdir -p "$S"

echo "# RevIndex evidence log (REBUILT after external scratch sweep)"
echo "utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "sweep=the whole .ufo/waves/round-35/scratch/ tree was removed by an external sweep ~03:45; w2/reports/ intact"
echo "lane=$LANE"
echo "master=$(git -C "$LANE" rev-parse master)"
echo "readme_sha256=$(sha256sum "$LANE/corpus/README.md" | cut -d' ' -f1)"
echo "readme_lines=$(wc -l < "$LANE/corpus/README.md")"
echo

echo "## 1. ASSIGNED COMMAND (rev=master)"
echo '$ python3 -I quality/check-index.py --repo . --rev $(git rev-parse master)'
python3 -I "$Q" --repo "$LANE" --rev "$(git -C "$LANE" rev-parse master)"; echo "rc=$?"
echo
echo "## 2. master universe"
echo -n "master knowledge blobs: "; git -C "$LANE" ls-tree --format='%(path)' master:corpus/knowledge | wc -l
echo -n "master README index rows: "; git -C "$LANE" show master:corpus/README.md | grep -cE '^\| `knowledge/[^`]+\.md`'
echo -n "master knowledge names containing idle-lock: "; git -C "$LANE" ls-tree --format='%(path)' master:corpus/knowledge | grep -c idle-lock
echo -n "new notes tracked at HEAD: "; git -C "$LANE" ls-files corpus/knowledge/idle-lock-never-asked-r12.md corpus/knowledge/idle-lock-chain-armed-r14.md corpus/knowledge/idle-lock-offered-in-the-bar-r15.md | wc -l
echo
echo "## 3. LANE WORKING TREE (root mode)"
echo '$ python3 -I quality/check-index.py --root .'
python3 -I "$Q" --root "$LANE"; echo "rc=$?"
python3 -I "$QR" --root "$LANE"; echo "rc=$?"
echo
echo "## 4. SCRATCH COPY OF WORKING TREE (root + rev mode)"
rm -rf "$S/repo"; mkdir -p "$S/repo"
rsync -a --exclude .git --exclude .jj --exclude .ufo "$LANE/corpus" "$LANE/quality" "$S/repo/"
echo -n "copied README sha256: "; sha256sum "$S/repo/corpus/README.md" | cut -d' ' -f1
python3 -I "$Q" --root "$S/repo"; echo "rc=$?"
( cd "$S/repo" && git init -q . && git add -A && \
  git -c user.email=revindex@scratch.invalid -c user.name=RevIndex commit -qm "w2 RevIndex rebuild" && \
  git rev-parse HEAD > "$S/scratch-sha.txt" )
SHA=$(cat "$S/scratch-sha.txt"); echo "scratch_commit=$SHA"
python3 -I "$Q" --repo "$S/repo" --rev "$SHA"; echo "rc=$?"
echo
echo "## 5. per-note row census (lane working tree)"
python3 -I - <<'PY'
import re, collections, pathlib
base = pathlib.Path('/home/vgpnk/Projects/shokunin/mado-shokunin')
row = re.compile(r"^\| `knowledge/([^`]+\.md)`", re.M)
c = collections.Counter(row.findall((base/'corpus/README.md').read_text()))
notes = sorted(p.name for p in (base/'corpus/knowledge').glob('*.md'))
print("notes_total", len(notes), "row_occurrences", sum(c.values()), "distinct_row_names", len(c))
for n in ['idle-lock-never-asked-r12.md', 'idle-lock-chain-armed-r14.md', 'idle-lock-offered-in-the-bar-r15.md']:
    print(f"new_row {n}: count={c.get(n,0)} note_present={(base/'corpus/knowledge'/n).is_file()}")
print("notes_with_count_ne_1", [n for n in notes if c.get(n,0) != 1])
print("rows_with_unknown_note", [k for k in c if k not in set(notes)])
PY
echo "rc=$?"
echo
echo "## 6. determinism (two root-mode runs, lane)"
python3 -I "$Q" --root "$LANE" > "$S/run1.txt"; r1=$?
python3 -I "$Q" --root "$LANE" > "$S/run2.txt"; r2=$?
echo "rc1=$r1 rc2=$r2"
cmp -s "$S/run1.txt" "$S/run2.txt" && echo "byte-identical" || echo "DIFFER"
echo
echo "## 7. gate selftest"
python3 -I "$Q" --selftest; echo "rc=$?"
echo
echo "## 8. negative controls rebuilt on top of the copy"
for v in neg-missing neg-dup neg-dangling neg-spacerow neg-fence neg-secondtable neg-prose; do
    rm -rf "$S/$v"; cp -a "$S/repo" "$S/$v"; rm -rf "$S/$v/.git"
done
python3 - "$S" <<'PY'
import sys, pathlib
S = pathlib.Path(sys.argv[1]); src = (S/'repo/corpus/README.md').read_text()
names = {'r12': 'idle-lock-never-asked-r12.md',
         'r14': 'idle-lock-chain-armed-r14.md',
         'r15': 'idle-lock-offered-in-the-bar-r15.md'}
def row(n): return [l for l in src.splitlines() if l.startswith(f'| `knowledge/{n}`')][0]
(S/'neg-missing/corpus/README.md').write_text(src.replace(row(names['r12'])+'\n', '', 1))
(S/'neg-dup/corpus/README.md').write_text(src + '\n' + row(names['r12']) + '\n')
(S/'neg-dangling/corpus/README.md').write_text(
    src.replace(row(names['r14']), row(names['r14']).replace(names['r14'], 'idle-lock-chain-armed-r99.md'), 1))
(S/'neg-spacerow/corpus/README.md').write_text(
    src.replace(row(names['r15']), row(names['r15']).replace('| `', '|  `', 1), 1))
body = src.replace(row(names['r15'])+'\n', '', 1)
(S/'neg-fence/corpus/README.md').write_text(body + '\n```\n' + row(names['r15']) + '\n```\n')
(S/'neg-secondtable/corpus/README.md').write_text(
    body + '\n## Unrelated table\n\n| Note | X |\n|---|---|\n' + row(names['r15']) + '\n')
(S/'neg-prose/corpus/README.md').write_text(
    body + '\n- The index entry for `knowledge/' + names['r15'] + '` lives here.\n')
PY
for v in neg-missing neg-dup neg-dangling neg-spacerow neg-fence neg-secondtable neg-prose; do
    out=$(python3 -I "$Q" --root "$S/$v" 2>&1); rc=$?
    echo "--- $v rc=$rc"; echo "$out"
done
echo
echo "## 9. historical (pre-sweep) values, from the seat transcript — NOT re-runnable, the trees were swept"
echo "readme_sha256_at_audit=a3769befe3558c54c79c015910ba514a7009aa6a825e15f2bafdfd896fc5e83a (246 L)"
echo "scratch_commit_pre_sweep=285314d3fe9f58dfda5eb7adb4b693f82daa1e08 -> indexed=50/50, rc=0"
echo "negatives pre-sweep: missing=1 rc=1 | duplicates=1 rc=1 | missing=1+dangling=1 rc=1 | missing=1 rc=1 | fence 50/50 rc=0 | secondtable 50/50 rc=0 | prose missing=1 rc=1"
echo "determinism pre-sweep: rc1=0 rc2=0, byte-identical"
