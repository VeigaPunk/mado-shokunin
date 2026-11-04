#!/usr/bin/env bash
# Falsification fixture: does adding quality/counters/c1-r67-register.py (a C1
# deliverable) without a tool-ledger row turn the standing instrument's ledger
# leg red at the candidate revision?  All writes under $S only.
set -u
S=/fast/scratch/hyaku/mado-r67/R67CriticClaims
L=$S/ledger-fx
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
rm -rf -- "$L"
mkdir -p "$L"
git -C "$LANE" archive 0b28ffb4baac9586566d246c3f0986b2bb650a33 tools quality | tar -x -C "$L" || exit 2
cp -- "$LANE/.ufo/waves/round-67/w1/R67ExecRegister/draft/quality/counters/c1-r67-register.py" \
      "$L/quality/counters/c1-r67-register.py" || exit 2
git -C "$L" init -q || exit 2
top=$(git -C "$L" rev-parse --show-toplevel) || exit 2
[ "$top" = "$L" ] || { echo "FIXTURE_TOP_MISMATCH $top" >&2; exit 2; }
git -C "$L" add -A || exit 2
git -C "$L" -c user.name=p -c user.email=p@example.invalid -c commit.gpgsign=false commit -qm fx || exit 2
REV=$(git -C "$L" rev-parse HEAD) || exit 2
echo "--- base ledger at fixture (control, same tree minus the new counter) ---"
python3 "$LANE/quality/check-tool-ledger.py" --repo "$LANE" --rev 0b28ffb4baac9586566d246c3f0986b2bb650a33 | tail -1
echo "--- candidate tree with c1-r67-register.py, no ledger row ---"
python3 "$LANE/quality/check-tool-ledger.py" --repo "$L" --rev "$REV" | tail -3
echo "LEDGER_FX_RC=${PIPESTATUS[0]}"
