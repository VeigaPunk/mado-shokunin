#!/bin/bash
# Single-defect mutants of the positive control for checks.py 86-89 (seat ScrMistakes).
# Every mutant must print FAIL; the pristine control prints CLEAN (receipts/green-control.txt).
set -o pipefail
S=$(mktemp -d -p /fast/scratch/hyaku/mado-r45/ScrMistakes) || exit 2
trap 'rm -rf -- "$S"' EXIT
L="$(cd "$(dirname "$0")" && pwd)/checks.py"
mk() {
  local X="$S/$1"
  git init -q "$X" || return 1
  [ "$(git -C "$X" rev-parse --show-toplevel)" = "$X" ] || return 1
  mkdir -p "$X/.ufo/waves/round-45/receipts" "$X/.ufo/waves/round-45/w1/fixtures" "$X/quality/counters"
  printf 'base\n' > "$X/base.txt"
  printf '%s' '[{"address":"0x1","at":[0,0],"class":"app","floating":false,"mapped":true,"monitor":0,"size":[800,600]}]' > "$X/.ufo/waves/round-45/w1/fixtures/projected.json"
  printf '## Round 45 - control\n\n| Claim / axis | Before -> after | Counting command | Self-verdict |\n|---|---|---|---|\n| C1 test claim | `fixtures=0/49` exit 1 at base -> `fixtures=49/49 TARGET_MET` exit 0 | `cmd` | TARGET_MET |\n' > "$X/SCORECARD.md"
  printf 'import argparse\nap = argparse.ArgumentParser()\nap.add_argument("--seed", type=int, default=45)\n' > "$X/quality/counters/c1-seeded.py"
  printf 'quality/counters/c1-seeded.py\n' > "$X/.ufo/waves/round-45/registration.md"
  git -C "$X" add -A
  git -C "$X" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m base || return 1
}
commit_tip() { git -C "$1" add -A; git -C "$1" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m tip; }

echo "# POSITIVE control first (must print CLEAN), then one single-defect mutant per check (must print FAIL)"
mk ctrl; X="$S/ctrl"; BC=$(git -C "$X" rev-parse HEAD)
printf 'MADO_AXIS: checked=3 mismatched=0 rev=%s (equivalent: the closing tip changes nothing outside .ufo/waves/round-45/)\nexit=0\n' "$BC" > "$X/.ufo/waves/round-45/receipts/axis-tip.txt"
printf 'PRED-C1: fixtures=49/49 verdict=TARGET_MET rev=%s (equivalent: the closing tip changes nothing outside .ufo/waves/round-45/)\nexit=0\n' "$BC" > "$X/.ufo/waves/round-45/receipts/c1-after-tip.txt"
commit_tip "$X"
echo; echo "control base=$BC tip=$(git -C "$X" rev-parse HEAD) outside-round diff files=$(git -C "$X" diff --name-only "$BC" HEAD | grep -cv '^.ufo/waves/round-45/')"
for c in 86 87 88 89; do
  echo; echo "\$ checks.py $c --repo <control> --rev HEAD"
  python3 -I "$L" "$c" --repo "$X" --rev HEAD --round .ufo/waves/round-45 --registration .ufo/waves/round-45/registration.md
  echo "exit=$?"
done

mk m86; X="$S/m86"; B6=$(git -C "$X" rev-parse HEAD)
printf 'MADO_AXIS: checked=3 mismatched=0 rev=%s\nexit=0\n' "$B6" > "$X/.ufo/waves/round-45/receipts/axis-tip.txt"
commit_tip "$X"
echo; echo "\$ checks.py 86 (tip receipt names the predecessor, no equivalence statement)"
python3 -I "$L" 86 --repo "$X" --rev HEAD --round .ufo/waves/round-45; echo "exit=$?"

mk m87; X="$S/m87"
printf '%s' '[{"address":"0x1","at":[0,0],"class":"app","floating":false,"mapped":true,"monitor":0,"size":[800,600],"title":"REDACTED"}]' > "$X/.ufo/waves/round-45/w1/fixtures/projected.json"
commit_tip "$X"
echo; echo "\$ checks.py 87 (one title key in the projected dump)"
python3 -I "$L" 87 --repo "$X" --rev HEAD; echo "exit=$?"

mk m88; X="$S/m88"
python3 - "$X" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]) / 'SCORECARD.md'
p.write_text(p.read_text().replace('`fixtures=49/49 TARGET_MET` exit 0', 'see `receipts/c1-after-data.txt`'))
PY
commit_tip "$X"
echo; echo "\$ checks.py 88 (after side is a pointer)"
python3 -I "$L" 88 --repo "$X" --rev HEAD; echo "exit=$?"

mk m89; X="$S/m89"
printf 'import argparse\nap = argparse.ArgumentParser()\nap.add_argument("--nonce", default=None)\n' > "$X/quality/counters/c1-seeded.py"
commit_tip "$X"
echo; echo "\$ checks.py 89 (--nonce default=None)"
python3 -I "$L" 89 --repo "$X" --rev HEAD --registration .ufo/waves/round-45/registration.md; echo "exit=$?"
