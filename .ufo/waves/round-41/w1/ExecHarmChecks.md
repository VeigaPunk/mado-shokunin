# ExecHarmChecks — round 41 w1 harm baselines (seat report)

Findings: `.ufo/waves/round-41/w1/ExecHarmChecks/baseline.md` (full verbatim captures) and
`.ufo/waves/round-41/w1/ExecHarmChecks/out-*.txt` (8 raw stdout+stderr files).

## Method

Throwaway clone at `/tmp/tmp.Npi7p9BBiM/lane` (`git clone -q` of the lane, toplevel verified equal
to the clone root, `git checkout -q 60c3914154333180450d5da27ba222d5763cc56a` detached, `rev-parse
HEAD` = that sha). Never the lane, never the fleet. Python 3.14.8 (`-I`), bash 5.3.20. Clone removed
after the captures; `git status --porcelain` was empty after all runs.

## Results (run, not inferred)

| # | command (cwd = clone root) | exit | counted line |
|---|---|---|---|
| 1 | `bash tools/mado-verify.sh --selftest` | 0 | `MADO_SELFTEST: 460/460 assertions passed` |
| 2 | `python3 -I tools/mado-options.py --selftest` | 0 | `MADO_OPTIONS_SELFTEST: 211/211 passed` |
| 3 | `python3 -I quality/check-index.py --rev 60c3914… --repo .` | 0 | `MADO_INDEX: … indexed=58/58 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` |
| 4 | `python3 -I quality/check-index-rows.py` (bare) | **2** | `SETUP_ERROR: --rev or --root is required` |
| 4b | `… --rev 60c3914… --repo .` (supplementary) | 0 | `MADO_INDEX_ROWS: … rows=58 errors=0 warns=3` (+3 `WARN cited-glob-nomatch`) |
| 5 | `python3 -I quality/check-axis-scores.py --repo . --rev 60c3914…` | 0 | `MADO_AXIS: checked=3 mismatched=0 rev=60c3914…` (navigation 58/58, calibration 55/55, operability 12/12, all MATCH) |
| 6 | `python3 -I tools/mado-eventq.py --selftest` | **2** | `mado-eventq.py: error: unrecognized arguments: --selftest` |
| 7 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | 0 | `mado<TAB>ok<TAB>…/mado-shokunin/corpus/SOURCES.md`; 7×`W04` + 1×`W01` (S277) |

## Findings the round needs

1. **Two assigned commands are usage errors, not passes.** (a) `quality/check-index-rows.py` requires
   `--rev`/`--root` (`quality/check-index-rows.py:462-471`; exit map "2 setup error"), so the bare
   form carries no fidelity signal — I captured it verbatim **and** added 4b at the freeze rev
   (`rows=58 errors=0 warns=3`, exit 0) so the round has a comparable baseline. (b) `tools/mado-eventq.py`
   exists but defines no `--selftest` flag (`tools/mado-eventq.py:208-218`; `grep -n selftest` empty),
   so **there is no eventq selftest baseline**; its self-check is a live read (`ss`, socket2,
   `hyprctl getoption`) that host safety forbids this seat. Recorded as a gap, not a pass.
2. **All four green baselines reproduce the frozen receipts.** `receipts/selftest-base.txt`
   (`MADO_SELFTEST: 460/460`) is line-identical to run 1; `receipts/axis-base.txt` matches run 5 on
   all three fractions and `checked=3 mismatched=0`, differing only in `rev=` (base vs freeze);
   `receipts/census-before.txt` matches run 7 on all 9 TSV lines (the frozen file adds a trailing
   `exit=0`). The freeze commit changed none of the seven instruments and no corpus file
   (`git diff --name-only ab2bfaa..60c3914`: round-40 marker, `.ufo/waves/round-41/**`,
   `quality/counters/{c1-r41-globals,c2-r41-focus-entry}.py`), so the freeze numbers are the base
   numbers re-measured.
3. **The 3 `cited-glob-nomatch` WARNs are pre-existing, not round-41 damage** (rows
   `window-rule-effects-getprop`, `config-drift-r12`, `rule-attribution-r24`); WARNs never move that
   exit code.
4. **Regression trip-wires for the data commit** (baseline.md §"What these baselines constrain"):
   `460/460`, `211/211`, `missing=0 dangling=0 duplicates=0`, `indexed` denominator rising only by
   the number of new notes ([INFERENCE] C2's one note → `59/59`), `MADO_INDEX_ROWS errors=0`,
   `MADO_AXIS mismatched=0`, census `mado ok` with no new E-code.

## Evidence

`out-*.txt` sha256 (from the seat dir): verify `58e720dd…`, options `647b6712…`, check-index
`81cc75ae…`, rows-bare `3d2d8ba2…`, rows-rev `eeece2b7…`, axis `87957cb6…`, eventq `a282a04a…`,
census `858315d2…` (full digests and line counts in baseline.md's manifest).

Residue: clone tree clean; no `/tmp/w5-mado-m52-selftest.*` dir in my run's window (20:00:35–20:00:51
— the 105 dirs spanning 17:59–20:04 belong to concurrent sibling seats); `ls -d
/tmp/mado-options-st-*` → 0; clone dir removed.

## Risks / blockers

- No blocker. The only gap is the missing eventq selftest flag (above) — the L1 may decide whether a
  harm baseline for eventq needs a live run by an authorized seat.
- Read-only verbs used: `git clone/checkout/rev-parse/status/show/diff/log/ls-tree`; no journal verb,
  no compositor/portal access, no package transaction, no installs (nothing needed installing).
