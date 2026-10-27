#!/bin/sh
# verify-install.sh — prove the delivered set installs from base bytes and lands
# the measured state, in a throwaway clone. Read-only on the lane.
#
# Usage: verify-install.sh <lane-repo> <scratch-dir>
set -eu
SEAT=$(cd "$(dirname "$0")" && pwd)
LANE=${1:?usage: verify-install.sh <lane-repo> <scratch-dir>}
S=${2:?usage: verify-install.sh <lane-repo> <scratch-dir>}
BASE=579f694b45c797a9c39761fdb4f9e0a1b71b3585
mkdir -p "$S"

rm -rf "$S/vclone"
git clone -q --shared "$LANE" "$S/vclone"
cd "$S/vclone"
[ "$(git rev-parse --show-toplevel)" = "$S/vclone" ] || { echo "toplevel guard failed" >&2; exit 2; }
git checkout -q --detach "$BASE"

sh "$SEAT/install.sh" "$S/vclone"

git add -A
git -c user.name=verify -c user.email=verify@scratch.invalid commit -qm "verify: install round-48 marker set"
REV=$(git rev-parse HEAD)
echo "verify rev=$REV base=$BASE"
rc=0
python3 -I quality/check-session-material.py --repo . --rev "$REV" || rc=$?
echo "verify rc=$rc"
