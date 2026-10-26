#!/bin/bash
# MutC2Counter driver: one repo per mutant, one 15-control suite per mutant.
set -u
S=/fast/scratch/hyaku/mado-r46/MutC2Counter
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
FREEZE=8c5434c60e03f147ee1f75ab195e8bc3f0db4dec
BASE=b22ea56bff2faec39ce9ff75d2107eaf4612ecbe
for m in M1-census-regex-uniq M1b-census-devicekeys M2-surface-width M3-quote-uniq M4-T1-census-prose M5-T2-supersede M6-T3-fences M7-T4-verdict-tokens M8-T4-anchor-range M9-T5-readme-ids; do
  D="$S/repos/$m"
  rm -rf "$D"
  git clone -q --shared --no-checkout "$LANE" "$D" || { echo "$m CLONE-FAIL"; exit 1; }
  git -C "$D" checkout -q --detach "$FREEZE" || { echo "$m CHECKOUT-FAIL"; exit 1; }
  T="$(git -C "$D" rev-parse --show-toplevel)"
  test "$T" = "$(realpath "$D")" || { echo "$m TOPLEVEL-MISMATCH"; exit 1; }
  cp "$S/mutants/$m.py" "$D/quality/counters/c2-r46-input-device-entry.py" || { echo "$m CP-FAIL"; exit 1; }
  git -C "$D" add -A
  git -C "$D" -c user.name=seat-mutc2 -c user.email=mutc2@scratch.invalid commit -q -m "mutant $m" || { echo "$m COMMIT-FAIL"; exit 1; }
  python3 -I "$S/wave/ctl/run-c2-controls.py" --repo "$D" --freeze "$FREEZE" --base "$BASE" --work "$S/work-$m" > "$S/out/$m.txt" 2>&1
  echo "$m rc=$?"
  rm -rf "$S/work-$m"
done
echo DRIVER-DONE
