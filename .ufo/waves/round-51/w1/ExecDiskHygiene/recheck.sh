#!/bin/sh
# recheck.sh — re-run the seat ExecDiskHygiene scratch-rule-4 matrix on the CURRENT bytes of the
# round-51 w1 drafts. Read-only with respect to the lane; writes only under the scratch dir.
#
#   sh recheck.sh <scratch-dir> [lane-repo]
#
# The scratch dir must be on a scratch filesystem (/tmp, /var/tmp and /dev/shm are refused by the
# probe itself). Nothing is left behind except the probe JSON receipts inside <scratch-dir>.
set -eu

SCRATCH=${1:?usage: recheck.sh <scratch-dir> [lane-repo]}
LANE=${2:-/home/vgpnk/Projects/shokunin/mado-shokunin}
SEAT=$(cd "$(dirname "$0")" && pwd)
WAVE="$LANE/.ufo/waves/round-51/w1"
BASE=6ca8c559a4a3d6d361101592116eea2bc7452437

mkdir -p "$SCRATCH/tmp" "$SCRATCH/w-c1" "$SCRATCH/w-c2" "$SCRATCH/home"
echo "== static scan: $WAVE"
python3 -I "$SEAT/hygiene-scan.py" --root "$WAVE" --json "$SCRATCH/static-scan.json" || true
echo
for spec in c1-r51 c2 checker2; do
    echo "== spec $spec"
    python3 -I "$SEAT/selftest-probe.py" \
        --spec "$SEAT/specs/$spec.json" \
        --scratch "$SCRATCH" \
        --out "$SCRATCH/$spec-probe.json" || true
    echo
done
echo "receipts: $SCRATCH/{static-scan,c1-r51-probe,c2-probe,checker2-probe}.json"
echo "base rev: $BASE (specs already carry it)"
