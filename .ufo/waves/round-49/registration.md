# mado round 49 — registration (frozen before any data commit; attempt 1, budget-shortened)

Base `03e4ae76aff7a4be59cb69970dd553baa319695a`. Claims `claims.md` (commit `5f37c1b8`). Wave `w1` (45 build seats) ran; at freeze
38 of 45 seat reports had landed (missing: ExecControlsC1 scoring, ExecSessionTriage, ScoutHyprBinds, CritPremiseC1, CritPremiseC2,
CritRoutedItems, SentPrivacy) and WAVE-DONE had not arrived. The L1's request budget ran out before wave `w2` could be dispatched,
so this freeze is not attacked by a falsify wave (declared; `w2-items.json` holds the 38 drafted attack items, never dispatched).

## C1 — operability (capability acquisition): `tools/mado-keysym.py`, `PRED-C1-r49`

- Counter `quality/counters/c1-r49-keysym.py` (w1/ExecCounterC1 draft `1a7fcc21…` plus L1 freeze edits: compile with
  `--include=/usr/share/xkeyboard-config-2` and a byte-equal default-path reference compile in a pristine HOME (w1/SentHost H2/H3),
  judge stdin `/dev/null` and no Compose section (H1), GEN 60 → 150 drawing ARG from every header name and `U` names and 1-3
  layout pairs per keymap (w1/CritClaimSizing), TMPDIR refused under `/tmp`, `/var/tmp`, `/dev/shm`). Fixtures
  `quality/counters/c1-r49-fixtures.json` (633 cases, 17 classes, sha256 `81836bfb…`, w1/ExecFixtures).
- Command: `cd /home/vgpnk/Projects/shokunin/mado-shokunin && TMPDIR=<scratch> python3 -I quality/counters/c1-r49-keysym.py --repo . --rev <rev> --work <scratch outside the lane> --nonce <n>`.
- TARGET_MET iff `fixtures=633/633 generated=150/150 selftest=ok readonly=ok tool=present`; the predicate sentence is the counter
  docstring, clauses t/s/f/g/r/i.
- Before (base, tool absent): `fixtures=0/633 generated=0/150 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED`
  (L1 run on a scratch clone, `receipts/c1-base.txt`). Do-nothing control: w1/ExecCounterC1 `receipts-stub-always2.txt`
  (exit-2 stub with an honest selftest line: `fixtures=52/633 … TARGET_MISSED`); tripwire controls write/exec/socket all MISSED.
- Candidate: w1/ExecRefKeysymA `mado-keysym.py` (sha256 `dcc13cce…`, selftest 38/38). Independent reference B
  (w1/ExecRefKeysymB) agrees with the judge on 57,865 random (keymap, keysym) pairs over 400 random RMLVO keymaps (L1 run).

## C2 — coverage (sourced): `corpus/knowledge/hyprland-bind-key-match-r49.md`, `PRED-C2-r49`

- Counter `quality/counters/c2-r49-bind-entry.py` (w1/ExecCounterC2 draft plus L1 freeze edits: new clause j — seven
  source-derived topics each answered by a numbered step quoting the implementing line; clause f reads counts from prose with
  backticked code spans blanked).
- Command: `cd /home/vgpnk/Projects/shokunin/mado-shokunin && TMPDIR=<scratch> python3 -I quality/counters/c2-r49-bind-entry.py --repo . --rev <rev>`.
- State at freeze: the integrated candidate (`candidate/hyprland-bind-key-match-r49.md`, `candidate/rows.md`) does NOT meet the
  counter on a scratch tree (clauses b/c/d/e/j fail on row-pin binding and quote attachment); no C2 data commit follows this round.

## Residuals (declared)

C1 f/g are a finite sample of an unbounded contract; C2 checks quote presence and topic location, not sentence truth; no w2.
