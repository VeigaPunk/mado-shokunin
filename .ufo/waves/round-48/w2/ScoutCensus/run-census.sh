#!/usr/bin/env bash
# ScoutCensus r48/w2: frozen sources-census on BASE and on a scratch mirror carrying the
# proposed C2 rows (S340-S350) + entry + README row. No lane writes, no git mutation anywhere:
# the corpus tree is extracted read-only from the base revision with `git archive`.
set -eu
ulimit -f 2048
L=/home/vgpnk/Projects/shokunin/mado-shokunin
W=$L/.ufo/waves/round-48
SEAT=$W/w2/ScoutCensus
S=/fast/scratch/hyaku/mado-r48/ScoutCensus
C=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
BASE=579f694b45c797a9c39761fdb4f9e0a1b71b3585
mkdir -p "$SEAT" "$S"
trap 'rm -rf -- "$S"' EXIT

D=$S/m
mkdir -p "$D"
git -C "$L" archive "$BASE" corpus | tar -x -C "$D"
for p in quality/check-index.py SKILL.md tools/mado-binds.py tools/mado-verify.sh \
         tools/mado-wsrules.py .ufo/waves/round-29/registration.md \
         .ufo/waves/round-30/registration.md .ufo/waves/round-47/w1/ExecSupersede/rows.md; do
  git -C "$L" archive "$BASE" -- "$p" | tar -x -C "$D"
done
printf 'base_rev=%s\n' "$BASE" > "$SEAT/revs.txt"
( cd "$D" && sha256sum corpus/SOURCES.md ) > "$SEAT/base-sources.sha256"
( cd "$D" && git -C "$L" show "$BASE:corpus/SOURCES.md" | sha256sum ) > "$SEAT/base-sources-gitshow.sha256"

# ---------- BASE ----------
rc=0; bash "$C" validate --file "$D/corpus/SOURCES.md" > "$SEAT/base-census-validate.txt" 2>&1 || rc=$?
printf 'base_validate_exit=%s\n' "$rc" >> "$SEAT/revs.txt"
rc2=0; bash "$C" census --file "$D/corpus/SOURCES.md" > "$SEAT/base-census.txt" 2>&1 || rc2=$?
printf 'base_census_exit=%s\n' "$rc2" >> "$SEAT/revs.txt"
grep -c '^| S' "$D/corpus/SOURCES.md" > "$SEAT/base-rowcount-all.txt" || true
awk -F'|' '$2 ~ /^ S3[0-9][0-9] $/ {print $2}' "$D/corpus/SOURCES.md" | wc -l > "$SEAT/base-rowcount-S3xx.txt"

# ---------- MIRROR: overlay proposed C2 data ----------
mkdir -p "$D/.ufo/waves/round-48/fetch" "$D/.ufo/waves/round-48/receipts" "$D/.ufo/waves/round-48/tools"
cp "$W"/fetch/* "$D/.ufo/waves/round-48/fetch/"
cp "$W/receipts/xkbcli-compile-keymap-r48.txt" "$D/.ufo/waves/round-48/receipts/"
cp "$W/tools/make-xkb-receipt.sh" "$D/.ufo/waves/round-48/tools/"
cp "$W/l1-draft/xkb-keymap-compile-r48.md" "$D/corpus/knowledge/"
python3 - "$D" "$W/l1-draft/rows-c2.md" "$W/l1-draft/readme-row.md" <<'EOF'
import sys
d, rows, rr = sys.argv[1:]
p = d + "/corpus/SOURCES.md"
s = open(p).read().split("\n")
i = max(k for k, l in enumerate(s) if l.startswith("| S339 |"))
s[i + 1:i + 1] = open(rows).read().rstrip("\n").split("\n")
open(p, "w").write("\n".join(s))
p = d + "/corpus/README.md"
s = open(p).read().split("\n")
i = max(k for k, l in enumerate(s) if l.startswith("| `knowledge/xdg-terminal-selection-r47.md`"))
s[i + 1:i + 1] = [open(rr).read().rstrip("\n")]
open(p, "w").write("\n".join(s))
EOF
( cd "$D" && sha256sum corpus/SOURCES.md ) > "$SEAT/mirror-sources.sha256"

# ---------- MIRROR ----------
rc=0; bash "$C" validate --file "$D/corpus/SOURCES.md" > "$SEAT/mirror-census-validate.txt" 2>&1 || rc=$?
printf 'mirror_validate_exit=%s\n' "$rc" >> "$SEAT/revs.txt"
rc2=0; bash "$C" census --file "$D/corpus/SOURCES.md" > "$SEAT/mirror-census.txt" 2>&1 || rc2=$?
printf 'mirror_census_exit=%s\n' "$rc2" >> "$SEAT/revs.txt"
grep -c '^| S' "$D/corpus/SOURCES.md" > "$SEAT/mirror-rowcount-all.txt" || true
awk -F'|' '$2 ~ /^ S3[0-9][0-9] $/ {print $2}' "$D/corpus/SOURCES.md" | wc -l > "$SEAT/mirror-rowcount-S3xx.txt"
grep -c '^| S' "$L/corpus/SOURCES.md" > "$SEAT/lane-worktree-rowcount-all.txt" || true

# ---------- structural checks on the mirror registry ----------
python3 - "$D/corpus/SOURCES.md" > "$SEAT/rows-structure.txt" <<'EOF'
import sys
lines = open(sys.argv[1]).read().split("\n")
rows = [l for l in lines if l.startswith("| S") and l.split("|")[1].strip().startswith("S34") or l.startswith("| S350")]
rows = [l for l in lines if l.startswith("| S") and l.split("|")[1].strip() in
        {"S%d" % n for n in range(340, 351)}]
print("new_row_lines=%d" % len(rows))
for l in rows:
    cells = l.split("|")
    print("%s fields_total=%d columns=%d tier=%s status=%s opened=%s recheck=%s usedby=%s"
          % (cells[1].strip(), len(cells), len(cells) - 2, cells[4].strip(), cells[8].strip(),
             cells[9].strip(), cells[10].strip(), cells[11].strip()))
EOF
# duplicate-id and duplicate-url scan restricted to the new ids
python3 - "$D/corpus/SOURCES.md" > "$SEAT/new-id-scan.txt" <<'EOF'
import sys, re
lines = open(sys.argv[1]).read().split("\n")
rows = []
for l in lines:
    if not l.startswith("| S"):
        continue
    c = [x.strip() for x in l.split("|")]
    if len(c) < 13:
        continue
    rows.append(c)
ids = [c[1] for c in rows]
new = [c for c in rows if c[1] in {"S%d" % n for n in range(340, 351)}]
print("registry_rows=%d distinct_ids=%d" % (len(ids), len(set(ids))))
print("new_ids=%s" % ",".join(c[1] for c in new))
print("new_id_dupes=%d" % (len(new) - len({c[1] for c in new})))
urls = {}
for c in new:
    m = re.search(r'(https?://[^\s|]+)', c[2])
    if m:
        urls.setdefault(m.group(1).rstrip('/'), []).append(c[1])
print("new_url_groups_repeated=%s" % {k: v for k, v in urls.items() if len(v) > 1})
EOF

# largest output file in this run
find "$SEAT" -type f -printf '%s %p\n' | sort -n | tail -1 > "$SEAT/largest-output.txt"
echo DONE
