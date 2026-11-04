#!/usr/bin/env bash
# C2 counter at base and at a scratch candidate (drafts copied, no lane writes).
set -u
S=/fast/scratch/hyaku/mado-r67/R67CriticClaims
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
H=$LANE/.ufo/waves/round-67/w1/R67ExecHarness/draft/quality/counters/c2-r67-landing-controls.py
C=$S/cand
rm -rf -- "$C" "$S/c2-base" "$S/c2-cand"
mkdir -p "$C/quality/counters" "$C/tools"
cp -- "$LANE/.ufo/waves/round-67/w1/R67ExecLanding/draft/quality/landing-counters.sh" "$C/quality/landing-counters.sh"
cp -- "$LANE/.ufo/waves/round-67/w1/R67ExecChildren/draft/quality/counters/c3-r56-used-by.py" "$C/quality/counters/c3-r56-used-by.py"
cp -- "$LANE/.ufo/waves/round-67/w1/R67ExecChildren/draft/quality/check-tool-ledger.py" "$C/quality/check-tool-ledger.py"
cp -- "$LANE/.ufo/waves/round-67/w1/R67ExecChildren/draft/tools/mado-receipt-citecheck.py" "$C/tools/mado-receipt-citecheck.py"
git -C "$C" init -q || exit 2
top=$(git -C "$C" rev-parse --show-toplevel) || exit 2
[ "$top" = "$C" ] || { echo "CAND_TOP_MISMATCH $top" >&2; exit 2; }
git -C "$C" add -A || exit 2
git -C "$C" -c user.name=p -c user.email=p@example.invalid -c commit.gpgsign=false commit -qm candidate || exit 2
echo "=== BASE rev 0b28ffb4 (do-nothing instrument) ==="
python3 -I "$H" --repo "$LANE" --rev 0b28ffb4baac9586566d246c3f0986b2bb650a33 --scratch-root "$S/c2-base" | grep -E 'MADO_R67_(SELFTEST|MUTANT|R_CHILD|LANDING_CONTROLS)'
echo "BASE_RC=${PIPESTATUS[0]}"
echo "=== CANDIDATE rev (drafts copied into scratch) ==="
python3 -I "$H" --repo "$C" --rev HEAD --scratch-root "$S/c2-cand" | grep -E 'MADO_R67_(SELFTEST|MUTANT|R_CHILD|LANDING_CONTROLS)'
echo "CAND_RC=${PIPESTATUS[0]}"
