# ExecClausePins — executor report, mado round 36 wave 1

Seat: `L1Mado36.ExecClausePins` — lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` (read-only).
Write scope: this report + `/tmp/exec-clause-pins/`. No production file touched. No tool installed
(channel directive: nothing was needed; Python stdlib only).

## Assignment

Build clause-set fixtures in `/tmp` from `LANE/.ufo/waves/round-36/c2/clauses.json`:
(a) one live clause deleted; (b) a live clause marked `not-load-bearing` with a reason
(second declaration); (c) the toctou clause's declaration removed; (d) the retired id re-added
to `live`; (e) the live list duplicated. Write a `/tmp` implementation of the round-36 C2 rule
(from `frozen.json`'s predicate text) and report `uncovered`/`retired`/`tip_ok` per fixture.
This is the pin's failing case.

## What I built

- `/tmp/exec-clause-pins/build-fixtures.py` — builds 8 fixture dirs (5 assigned + `base` +
  2 adjacent probes). Each fixture is a mini repo root with the mutated `clauses.json` at
  `.ufo/waves/round-36/c2/clauses.json`, committed copies of the blob ledger
  (`.ufo/waves/round-36/ledger/RevFrozenBlobs-r36.md`) and every receipt in
  `controls/receipts/`, and `.git` symlinked to the lane's `.git` so `git log`/
  `git rev-parse` resolve lane history (read-only).
- `/tmp/exec-clause-pins/c2-clause-pins.py` — fresh implementation of `PRED-C2-r36-v1`
  derived from the frozen predicate text in `frozen.json` (line 3), emitted same CLI as the
  lane counter (`--repo`, `--frozen`) and the same output line contract:
  `PRED-C2-r36-v1 uncovered=N retired=N tip_ok=N verdict=...`.

Frozen spec used: `.ufo/waves/round-36/c2/frozen.json` (predicate `PRED-C2-r36-v1`,
expected live ids ×11, expected retired `r34-word-bound-1-25`, toctou `o-nofollow-open`,
tip rule round 34 / `round-34` / 3 tip lines, receipts dir `controls/receipts`).

## Semantics implemented (from the frozen predicate text)

1. Live id **set** must equal `expected_live_clause_ids` exactly → deleted clause uncovered
   and never silently skipped; unexpected extra live id also uncovered.
2. Each live clause carrying a `not-load-bearing` declaration with a reason is exempt from the
   control bind, counts as a declaration, and is uncovered unless it is the frozen toctou
   clause; **exactly one** declaration total.
3. Every other live clause must name `control.control_id` + `control.receipt`; the receipt must
   record `observed=TARGET_MISSED` and name both the clause id and the control id (a one-line
   token file or an unbound receipt does not cover).
4. `retired` = live-absent count of retired ids; a retired id outside
   `expected_retired_clause_ids` zeroes it.
5. `tip_ok`: newest commit whose subject names `round-34` computed via git log; blob ledger
   names the superseded round-35 ledger; every 40-hex token on tip-naming lines (lines
   containing `supersedes` exempt) equals it, ≥3 such lines; every table row names a frozen
   path whose blob re-derives at the tip; row path set = frozen path set.

## Commands and quoted output

Fixture build:

```
$ python3 /tmp/exec-clause-pins/build-fixtures.py
fixture=a-deleted dir=/tmp/exec-clause-pins/a-deleted
fixture=b-second-declared dir=/tmp/exec-clause-pins/b-second-declared
fixture=c-decl-removed dir=/tmp/exec-clause-pins/c-decl-removed
fixture=d-retired-live dir=/tmp/exec-clause-pins/d-retired-live
fixture=d2-retired-live-plain dir=/tmp/exec-clause-pins/d2-retired-live-plain
fixture=e-live-duplicated dir=/tmp/exec-clause-pins/e-live-duplicated
fixture=f-dup-controlled-only dir=/tmp/exec-clause-pins/f-dup-controlled-only
fixture=base dir=/tmp/exec-clause-pins/base
```

Run (my implementation; `--frozen` = lane's `c2/frozen.json`):

```
$ python3 -I /tmp/exec-clause-pins/c2-clause-pins.py --repo /tmp/exec-clause-pins/<FIXTURE> --frozen LANE/.ufo/waves/round-36/c2/frozen.json
```

Results (one line per fixture, exact stdout):

| fixture | mutation | uncovered | retired | tip_ok | verdict |
|---|---|:--:|:--:|:--:|---|
| base | none (committed ledger) | 0 | 1 | 1 | **TARGET_MET** |
| a-deleted | (a) live clause deleted (gate-quote-word-bound) | 1 | 1 | 1 | TARGET_MISSED |
| b-second-declared | (b) second not-load-bearing declaration (entry-regular) | 2 | 1 | 1 | TARGET_MISSED |
| c-decl-removed | (c) toctou declaration removed | 2 | 1 | 1 | TARGET_MISSED |
| d-retired-live | (d) retired id re-added to live (declared) | 3 | 0 | 1 | TARGET_MISSED |
| d2-retired-live-plain | (d) adjacent read: retired object verbatim | 2 | 0 | 1 | TARGET_MISSED |
| e-live-duplicated | (e) live list duplicated | 1 | 1 | 1 | TARGET_MISSED |
| f-dup-controlled-only | probe: one controlled clause duplicated | 0 | 1 | 1 | **TARGET_MET** |

Detail lines (exact, representative):

```
# a-deleted
  clause-set: missing ['gate-quote-word-bound'] extra []
  tip: computed 6d754bd599caa7ab21c4c20b548c0fa83914ffce, 7 rows re-derived
# b-second-declared
  declared: entry-regular is not the frozen toctou clause
  declared: 2 not-load-bearing clauses, expected exactly one
# c-decl-removed
  uncontrolled: o-nofollow-open names no control id and receipt
  declared: 0 not-load-bearing clauses, expected exactly one
# d-retired-live
  clause-set: missing [] extra ['r34-word-bound-1-25']
  declared: r34-word-bound-1-25 is not the frozen toctou clause
# d2-retired-live-plain
  clause-set: missing [] extra ['r34-word-bound-1-25']
  uncontrolled: r34-word-bound-1-25 names no control id and receipt
# e-live-duplicated
  clause-set: missing [] extra []
  declared: 2 not-load-bearing clauses, expected exactly one
```

Cross-validation — the lane's committed counter (`quality/counters/c2-ledger.py`) run over the
same 8 fixtures produced **byte-identical** output lines and exit codes on every fixture
(base 0, a 1, b 1, c 1, d 1, d2 1, e 1, f 0). My implementation and the lane's agree
exactly; the outputs above are therefore the lane counter's own behaviour on these inputs.
Baseline sanity: `base` → `uncovered=0 retired=1 tip_ok=1 verdict=TARGET_MET`
(exit 0), and the lane's `c2-live` committed receipt shows `observed=TARGET_MET` with the
same tip `6d754bd599caa7ab21c4c20b548c0fa83914ffce`.

Extra validation against the lane's own generated mutants (leftover `/tmp/mado-r36-mutants-r36/`
dirs, no git history): my implementation reproduced the committed receipts' `uncovered`/
`retired` counts exactly — `c2-clause-deleted` 1/1, `c2-retired-also-live` 3/0,
`c2-receipt-token` 1/1, `c2-receipt-unbound` 1/1. `tip_ok=0` there only because those dirs
have no `.git` (no commit reachable), an environment property, not a predicate difference.

## Verdicts per item

- **(a)** one live clause deleted → `uncovered=1 retired=1 tip_ok=1` → MISSED. PASS (pin holds).
- **(b)** second not-load-bearing declaration → `uncovered=2 retired=1 tip_ok=1` → MISSED.
  PASS (pin holds). Note: taking the declaration (entry-regular; can't be the toctou clause)
  and double-declaration are counted separately → 2.
- **(c)** toctou declaration removed → `uncovered=2 retired=1 tip_ok=1` → MISSED. PASS (pin
  holds): the clause loses its declared status and names no control (uncontrolled) and the
  declaration count drops to 0.
- **(d)** retired id re-added to `live` → canonical read (per `gen-mutants.py`'s
  `retired-also-live` profile: re-enters declared) `uncovered=3 retired=0 tip_ok=1` → MISSED;
  literal read (retired object verbatim) `uncovered=2 retired=0 tip_ok=1` → MISSED. PASS
  (pin holds both ways).
- **(e)** live list duplicated → `uncovered=1 retired=1 tip_ok=1` → MISSED. PASS with a
  caveat: the set-equality pin alone sees `missing [] extra []`; the attack is actually caught
  by the "exactly one not-load-bearing declaration" guard because the duplicated list carries
  `o-nofollow-open` twice.

## Findings — the pin's coverage and its residual hole

1. The `expected_live_clause_ids` pin is the load-bearing check for deletions: without it
   (cf. `MutC2NoClausePin` seat), a deleted clause keeps `uncovered=0` and is skipped — the
   fail-open the pin exists to close. Assigned cases (a)–(e) all stay closed.
2. **Residual fail-open (probe f):** `f-dup-controlled-only` — the live list duplicated by
   appending one *controlled* clause (`row-unique`) while leaving the single toctou
   declaration intact — scores `uncovered=0 retired=1 tip_ok=1` → **TARGET_MET**. The pin
   compares id *sets*, so it cannot see multiplicity; the "exactly one declaration" guard only
   fires when the duplicated clause is itself declared. A ledger that lists a controlled clause
   twice passes as clean. (The 12-entries-11-expected ledger is still structurally plausible.)
   Fix direction: compare sorted id *lists* (multiset) to `expected_live_clause_ids`, or add
   an explicit live-length check; `gen-mutants.py` has no mutant for this kind, so it is
   currently uncontested.
3. Receipt binding works as frozen: unbound/token receipts (`entry-regular`'s, in the lane's
   own mutants) don't cover; clause deletion and retired re-entry are both visible in
   `uncovered`/`retired` exactly as the predicate describes.

## Files changed

- `.ufo/waves/round-36/w1/reports/ExecClausePins.md` (this report) — the only lane write.
- `/tmp/exec-clause-pins/build-fixtures.py`, `/tmp/exec-clause-pins/c2-clause-pins.py`,
  `/tmp/exec-clause-pins/base-clauses.json`, and the 8 fixture dirs under
  `/tmp/exec-clause-pins/` — all scratch.

## Blockers

None. Git operations on the lane repo were read-only (`git log`, `git rev-parse`) and all
lane writes were confined to the report path above.
