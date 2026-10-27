#!/usr/bin/env bash
# Build a minimal scratch fixture repo whose population contains a ledger reader.
set -euo pipefail
S=/fast/scratch/hyaku/mado-r52/Attack06
L=/home/vgpnk/Projects/shokunin/mado-shokunin
F=$S/fixtures/repo
rm -rf "$F"; mkdir -p "$F"/{quality/counters,tools,.ufo/waves/round-52}
cp "$L/quality/check-tool-ledger.py" "$F/quality/check-tool-ledger.py"
cp "$L/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py" "$F/quality/counters/c1-r52-ledger.py"
cp "$L/.ufo/waves/round-52/registration.md" "$F/.ufo/waves/round-52/registration.md"
printf '%s\n' '#!/usr/bin/env bash' '# alpha checker -- prints widget verdicts.' 'echo verdict' > "$F/tools/alpha.sh"
cat > "$F/PROVINCE.md" <<'EOF'
# province

Line 5 names `quality/check-tool-ledger.py` as the ledger gate.
Line 6 names `quality/counters/c1-r52-ledger.py` as the round-52 C1 counter.
Line 7 names `tools/alpha.sh` as the example instrument.
EOF
cat > "$F/SCORECARD.md" <<'EOF'
# scorecard

- `quality/check-tool-ledger.py` gate row.
- `quality/counters/c1-r52-ledger.py` counter row.
- `tools/alpha.sh` instrument row.
EOF
cd "$F"
git init -q .
git config user.name fixture
git config user.email fixture@example.invalid
git add -A
git commit -q -m fixture
git rev-parse --show-toplevel
