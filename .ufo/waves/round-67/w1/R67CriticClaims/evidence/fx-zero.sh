#!/usr/bin/env bash
# Falsification fixture: does the BASE (0b28ffb4) landing instrument refuse a
# zero-citation citecheck marker at rc 0?  All writes under $S only.
set -u
S=/fast/scratch/hyaku/mado-r67/R67CriticClaims
D=$S/fx-zero
rm -rf -- "$D" "$S/instr" "$S/shim" "$S/run"
mkdir -p "$D/corpus/knowledge" "$D/.ufo/waves/round-66/receipts" \
         "$S/instr/quality/counters" "$S/instr/tools" "$S/shim"
printf '| `knowledge/n.md` |\n' >"$D/corpus/README.md"
printf '# note\n' >"$D/corpus/knowledge/n.md"
printf 'cite corpus/README.md\n' >"$D/.ufo/waves/round-66/receipts/a.txt"
git -C "$D" init -q || exit 2
top=$(git -C "$D" rev-parse --show-toplevel) || exit 2
[ "$top" = "$D" ] || { echo "FIXTURE_TOP_MISMATCH $top" >&2; exit 2; }
git -C "$D" add -A || exit 2
git -C "$D" -c user.name=p -c user.email=p@example.invalid -c commit.gpgsign=false commit -qm fixture || exit 2
REV=$(git -C "$D" rev-parse HEAD) || exit 2
INSTR=${INSTR:-}
if [ -z "$INSTR" ]; then
  git -C "/home/vgpnk/Projects/shokunin/mado-shokunin" show \
    0b28ffb4baac9586566d246c3f0986b2bb650a33:quality/landing-counters.sh >"$S/base-landing.sh" || exit 2
  INSTR=$S/base-landing.sh
fi
cp -- "$INSTR" "$S/instr/quality/landing-counters.sh"
for f in "$S/instr/quality/counters/c3-r56-used-by.py" "$S/instr/quality/check-tool-ledger.py" "$S/instr/tools/mado-receipt-citecheck.py"; do
  printf '# stub child\n' >"$f"
done
REAL=$(command -v python3)
cat >"$S/shim/python3" <<SHIM
#!/usr/bin/env bash
case "\$1" in
  -) exec "$REAL" "\$@" ;;
  */c3-r56-used-by.py) printf 'MADO_USED_BY: rev=%s entries=1 rows=1 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=0 verdict=TARGET_MET missed=none\n' "$REV"; exit 0 ;;
  */check-tool-ledger.py) printf 'LEDGER: population=1 ledger_rows=1 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET rev=%s\n' "$REV"; exit 0 ;;
  */mado-receipt-citecheck.py) printf 'MADO_CITECHECK: rev=%s files=1 citations=0 resolved=0 missing=0 skipped_large=0 verdict=TARGET_MET\n' "$REV"; exit 0 ;;
  *) exit 2 ;;
esac
SHIM
chmod +x "$S/shim/python3"
PATH="$S/shim:$PATH" bash "$S/instr/quality/landing-counters.sh" \
  --repo "$D" --rev "$REV" --round 66 --scratch-root "$S/run"
echo "INSTRUMENT_RC=$?"
