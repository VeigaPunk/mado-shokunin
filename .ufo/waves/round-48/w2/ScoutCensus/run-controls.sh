#!/usr/bin/env bash
# ScoutCensus r48/w2: negative controls for the census reading of the candidate rows.
# (a) rows without the entry file  -> E11 per new row (used-by binding is real)
# (b) duplicate S340 id            -> E03 (the "no E03" observation is not vacuous)
set -eu
ulimit -f 2048
L=/home/vgpnk/Projects/shokunin/mado-shokunin
W=$L/.ufo/waves/round-48
SEAT=$W/w2/ScoutCensus
S=/fast/scratch/hyaku/mado-r48/ScoutCensus-ctl
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
python3 - "$D" "$W/l1-draft/rows-c2.md" <<'EOF'
import sys
d, rows = sys.argv[1], sys.argv[2]
p = d + "/corpus/SOURCES.md"
s = open(p).read().split("\n")
i = max(k for k, l in enumerate(s) if l.startswith("| S339 |"))
s[i + 1:i + 1] = open(rows).read().rstrip("\n").split("\n")
open(p, "w").write("\n".join(s))
EOF

# (a) no entry file: used-by target absent
rc=0; bash "$C" validate --file "$D/corpus/SOURCES.md" > "$SEAT/ctl-a-no-entry.txt" 2>&1 || rc=$?
printf 'ctl_a_exit=%s\n' "$rc" >> "$SEAT/ctl-exits.txt"
grep -E 'E11\tS3(4[0-9]|50)' "$SEAT/ctl-a-no-entry.txt" | wc -l > "$SEAT/ctl-a-e11-count.txt" || true

# (b) duplicate id: copy the S340 line verbatim (same id, same URL) -> E03
python3 - "$D" <<'EOF'
import sys
p = sys.argv[1] + "/corpus/SOURCES.md"
s = open(p).read().split("\n")
i = max(k for k, l in enumerate(s) if l.startswith("| S340 |"))
s.insert(i + 1, s[i])
open(p, "w").write("\n".join(s))
EOF
rc=0; bash "$C" validate --file "$D/corpus/SOURCES.md" > "$SEAT/ctl-b-dup-id.txt" 2>&1 || rc=$?
printf 'ctl_b_exit=%s\n' "$rc" >> "$SEAT/ctl-exits.txt"
echo DONE
