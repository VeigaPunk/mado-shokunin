# R72ExecBattery — harm-watch battery (round mado 72, wave 1)

Seat: harm-watch battery at the instrument commit. Axes under round 72: **C1 calibration**
(landing kill credit requires the run's own failure detail) and **C2 operability** (the harness
outcome reads the gate's own summary, not its exit status). This seat is read-only: it proves the
round harmed no measured surface. Repo: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Refs verified read-only: base `976684a27e99c2508037a60eec415f550f53d70e` exists; `master` =
`fd9ea03b554d6925594957c381f09e29a2ac159e` (the tree advanced past base mid-wave; check-ledger
and check-axis stamped that rev). No tools installed (none needed); no tooling-authorization
event to record. Scratch `/fast/scratch/hyaku/mado-r72/R72ExecBattery/` created and deleted; no
receipt needed copying (all evidence is inline below). No file written anywhere except this
report.

## Battery results

| command | rc | last line | verdict |
|---|---|---|---|
| `bash tools/mado-verify.sh --selftest` | 0 | `MADO_SELFTEST: 460/460 assertions passed` | **PASS** — gate held at 460/460 (no-harm obligation met) |
| `python3 -I quality/check-index.py --repo . --rev master` | 0 | `MADO_INDEX: rev=master indexed=85/85 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | **PASS** — index held at measured maximum 85/85, coverage 10.0000 |
| `python3 -I quality/check-tool-ledger.py --repo . --rev master` | 1 | `LEDGER: population=125 ledger_rows=122 uncovered=3 dangling=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED rev=fd9ea03b554d6925594957c381f09e29a2ac159e` | **EXPECTED (pre-registration)** — uncovered set is exactly the three new r72 instruments (listed below); held population is the pre-round 122 rows over 125 tracked tools; `uncovered=0` is the declared same-round end-state, not yet due mid-wave |
| `python3 quality/check-axis-scores.py` | 0 | `MADO_AXIS: checked=3 mismatched=0 rev=fd9ea03b554d6925594957c381f09e29a2ac159e` (rows: navigation 85/85 MATCH, calibration 86/86 MATCH, operability 12/12 MATCH) | **PASS** — bare run is complete; no flags needed; all published sub-axes at measured values |
| `git diff --stat 976684a27e99c2508037a60eec415f550f53d70e master -- tools/mado-verify.sh quality/landing-counters.sh` | 0 | *(no output — empty diff)* | **PASS** — zero drift base→master in both production instruments |
| `git rev-parse 976684a2:quality/counters/c1-r71-landing-controls.py master:quality/counters/c1-r71-landing-controls.py` | 0 | `1b1e293c3e80863061911f039e19b91f9537cb5b` = `1b1e293c3e80863061911f039e19b91f9537cb5b` | **PASS** — same blob |
| `git rev-parse 976684a2:quality/counters/c1-r71-real-children.py master:quality/counters/c1-r71-real-children.py` | 0 | `857a2ab2348e7fbdcf3db95ba030805bd35b1ed8` = `857a2ab2348e7fbdcf3db95ba030805bd35b1ed8` | **PASS** — same blob |
| `git rev-parse 976684a2:quality/counters/c2-r71-shapes.py master:quality/counters/c2-r71-shapes.py` | 0 | `6b9c301976be74edbbbacf12dc5ba8efbfc42fe8` = `6b9c301976be74edbbbacf12dc5ba8efbfc42fe8` | **PASS** — same blob |
| `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` (run 1) | 1 | `mado   E11   S445 missing used-by corpus/knowledge/outcome-verdict-gate-summary-r72.md` | **MID-FLIGHT DRIFT, not round harm** — 2× E11 (`S444`, `S445` both `missing used-by corpus/knowledge/outcome-verdict-gate-summary-r72.md`): the round's two new source rows were already appended but the r72 C2 knowledge entry had not landed at that moment; all other output is the pre-existing W04/W01 baseline warning set (38 W04 duplicate-url + 1 W01 tierC note, unchanged from prior rounds) |
| same census command (run 2, re-run minutes later at the converged tree) | 0 | `ok   /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` | **PASS** — exit 0 once `corpus/knowledge/outcome-verdict-gate-summary-r72.md` existed (confirmed on disk); both E11s gone; W04/W01 baseline unchanged |
| registry row count (my measurement: `grep -c '^\| S[0-9][0-9][0-9] \|'` on `corpus/SOURCES.md`) | 0 | `383` | **CONSISTENT** — the seat's "380 rows" expectation refers to the pre-append state; the round's 3 appends (S444, S445 included + S446 curated rejection, per the SOURCES.md round-72 sweep note) had already landed at measurement time: 380 + 3 = 383 |

## Exact uncovered ledger set (check-tool-ledger, `--rev master`)

```
LEDGER-ROW reason=uncovered path=quality/counters/c1-r72-landing-controls.py detail=no-row
LEDGER-ROW reason=uncovered path=quality/counters/c1-r72-summary-credit.py detail=no-row
LEDGER-ROW reason=uncovered path=quality/counters/c2-r72-outcome.py detail=no-row
```

`population=125 ledger_rows=122 uncovered=3` — the held pre-round population (122/122 at base)
with exactly the round's three new instruments unregistered, matching the declaration's
mid-round expectation. End-of-round obligation remains `uncovered=0` (L1's registration step,
not this seat's).

## Verdict

**No measured surface regressed.** Gate selftest 460/460, index 85/85 @ 10.0000, all three
published axis rows MATCH, production instruments (`tools/mado-verify.sh`,
`quality/landing-counters.sh`) byte-identical base→master, and all three frozen round-71
counters byte-identical (same blob hashes both revs). The two non-green readings are both
explained mid-round states, not harm: the ledger's 3 uncovered rows are the round's own new
instruments awaiting their declared same-round registration, and the census's transient E11s
self-resolved when the r72 C2 knowledge entry landed between run 1 and run 2 (run 2 exits 0).
Census row arithmetic reconciles exactly with the declaration's sources plan (380 + 3 = 383).

## Limits

- `master` advanced during the battery (base → `fd9ea03b…`); census run 1 and run 2 sampled
  different tree states — both are recorded rather than averaged.
- The W04 duplicate-url and W01 tierC census warnings are baseline noise carried from earlier
  rounds; I did not diff them against an older census receipt beyond observing the set is
  identical across my own two runs.
- The row count is my own `grep -c` over the registry table, not a census-script output; the
  script prints only per-row warnings plus a final `ok` line on success.
