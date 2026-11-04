# R74ExecHarm — harm watch

Axes: gate stability, navigation integrity, registration coverage, axis-table consistency, source validity, frozen-instrument identity.

Exact commands, stdout/stderr and exit codes: [harm-watch-r74.txt](harm-watch-r74.txt). Repository revision for pinned checks: `b73db773aaf67c9b26c8cf1a4cd567dec3af11f4`; base: `bd5a971532f37df85a78f6f566dd1e649b79de11`.

| Check | Observed result | Exit |
|---|---|---|
| Selftest | NOT RUN: explicit no-`/tmp` bound conflicts with hardcoded scratch | not executed |
| Index | indexed=89/89 missing=0 dangling=0 duplicates=0 | 0 |
| Tool ledger | population=130 ledger_rows=127 uncovered=3 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED | 1 |
| Axis table | navigation 89/89; calibration 86/86; operability 12/12; all MATCH; checked=3 mismatched=0 | 0 |
| Sources census | final line: `mado\tok\t/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` (tabs rendered as escapes here; exact bytes in receipt) | 0 |
| Frozen instruments | all five base/freeze blob pairs identical | 0 each |

## Deviations and blocker

- Ledger expectation was inaccurate at the frozen pre-registration revision: three uncovered files, not two: `quality/counters/c1-r74-replay-witness.py`, `quality/counters/c1-r74-witness-rule.py`, and `quality/counters/c2-r74-shapes.py`. L1 confirmed this is the expected pre-registration state. No ledger repair attempted; later registration cannot change this pinned-revision result.
- `tools/mado-verify.sh:418` reads exactly: `T=$(mktemp -d /tmp/w5-mado-m52-selftest.XXXXXX) || { echo "cannot mktemp" >&2; exit 2; }`. An explicit template is not redirected by TMPDIR. The supplied user assignment prohibits `/tmp`; therefore no selftest was run and no 460/460 claim is made. L1 accepted this seat's stricter bound and will own the selftest separately under its own authorization. L1-designated receipt: `.ufo/waves/round-74/receipts/gate-selftest-r74.txt` (not observed by this seat; not this seat's run). Routed defect: hardcoded scratch location; gate unchanged.

## Scope and evidence

Re-read the frozen claims and all three committed measurement/baseline receipts; no rewriting or rerunning their scored counters. Evidence of those receipts remains in their committed paths. No production files changed, no git mutations, no installs, no host/session/network probing. Only this report and the exact receipt were written. Scratch was empty after the read-only checks and removed before handoff. LSP symbol work was not applicable: no implementation/refactor performed.

Self-assessment: accuracy 4/5 (selftest result deliberately unavailable); completeness 3/5 (one mandatory command blocked); clarity 4/5 (full raw output separated into receipt); actionability 4/5 (exact blocking line and needed authorization recorded); conciseness 4/5 (necessary discrepancy detail retained). Overall 3.8/5. Improvement: exercise the unmodified gate only once a compliant scratch route or authoritative exception exists. The user should agree that reporting unavailable evidence is preferable to inventing a pass.
