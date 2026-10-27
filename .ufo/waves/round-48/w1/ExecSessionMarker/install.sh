#!/bin/sh
# install.sh — apply the round-48 synthetic-material marker set to a lane checkout.
#
# Usage: install.sh /path/to/lane-checkout
#
# Writes (never commits, never runs git):
#   quality/check-session-material.py            (gate v2 bytes)
#   quality/session-material-waivers.txt         (the registry, 47 rows)
#   .ufo/waves/.../<path>.synthetic              (47 sidecars, lane-relative)
#
# Run it from the integrator, then commit the result as the round's data commit.
set -eu
SEAT=$(cd "$(dirname "$0")" && pwd)
LANE=${1:?usage: install.sh <lane-checkout>}
[ -d "$LANE/quality" ] || { echo "not a lane checkout: $LANE" >&2; exit 2; }

cp "$SEAT/check-session-material.py" "$LANE/quality/check-session-material.py"
cp "$SEAT/session-material-waivers.txt" "$LANE/quality/session-material-waivers.txt"

cd "$SEAT/sidecars"
find . -type f -name '*.synthetic' | LC_ALL=C sort | while IFS= read -r rel; do
    rel=${rel#./}
    mkdir -p "$LANE/$(dirname "$rel")"
    cp "$SEAT/sidecars/$rel" "$LANE/$rel"
done

echo "installed gate sha256=$(sha256sum "$LANE/quality/check-session-material.py" | cut -d' ' -f1)"
echo "installed registry rows=$(grep -vc '^#' "$LANE/quality/session-material-waivers.txt")"
echo "installed sidecars=$(find "$SEAT/sidecars" -type f -name '*.synthetic' | wc -l)"
