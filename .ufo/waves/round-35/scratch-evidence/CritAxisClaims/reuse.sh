#!/usr/bin/env bash
# Probe: does C2 accept one shared control receipt covering every live clause?
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
S=$LANE/.ufo/waves/round-35/scratch/CritAxisClaims
rm -rf "$S/t7"; git clone --shared --quiet "$LANE" "$S/t7"
python3 - "$S/t7/.ufo/waves/round-35/c1/clauses.json" <<'PY'
import json, sys
p = sys.argv[1]
d = json.load(open(p))
# point every live clause at the single receipt that already says TARGET_MISSED
r = d["live"][0]["control"]["receipt"]
for c in d["live"]:
    if "control" in c:
        c["control"] = {"tree": "controls/c1-entry-symlink", "receipt": r}
json.dump(d, open(p, "w"), indent=1)
PY
python3 -I "$S/t7/.ufo/waves/round-35/c2/count.py" --repo "$S/t7" --frozen "$S/t7/.ufo/waves/round-35/c2/frozen.json"
echo "  exit=$?"
