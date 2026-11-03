# mado round 66 — lesson

author: mado L1 lane (integrated from wave w1 seat reports; the non-author closure verifies this round)
date: 2026-11-03
frozen contract: `.ufo/waves/round-66/claims-declaration-r66.md` (commit `ed980316e330703030d0c17b2a7098e058295b99`)
base: `eafd500fa7be76dca59e729435e231a5032cc037`

## Context

Round 66 is a calibration/operability round on the counter-design ground opened in round 65: the
register counter's discrimination and the landing instrument's ability to tell a genuine red child
from a crash, a skipped child, a drifted default tree, or a missing sibling. It is not desktop
mastery and not a new surface. Two claims only (C1, C2); no C3 and no knowledge expansion is claimed.
The r65 counters stay frozen; the round's successors are new files.

Process limits disclosed by the L1, kept truthful here and not repaired:

- Freeze order was not met (M66-4): the freeze commit landed after the wave registry and the ready
  marker, so criterion 106's strict order is not satisfied and no chronological pass is claimed.
- The do-nothing baseline was specified before dispatch, but its fresh executable control run was
  delegated to wave seats after the freeze; the prompt-literal instruction to score the cheapest
  control before freezing is therefore not satisfied. Baseline receipts are retained, and a target
  miss stays a miss.
- The frozen declaration named a ledger marker the child does not emit (M66-5). The implementation
  anchors the actual `LEDGER:` line; the four C2 expected outcomes are unchanged, and the literal
  mismatch is left for closure to grade as a conformance defect.
- The round's source row supports C2 exit-status vocabulary only. It proves neither C1 register
  truth nor that any child actually ran or emitted a marker.
- The frozen control harness's C2 count was found by the critic to run cases a-d only: it never runs
  the candidate selftest or a real four-leg landing, so its `correct=4/4 TARGET_MET` is a diagnostic,
  not the full frozen target (`.ufo/waves/round-66/w1/R66CriticLanding.md` F1).

## Mistakes

**M66-1 — the r65 re-open edited the `opened` cell in place, which contract v1 does not allow.**
Class: record lifecycle (column contract).
Evidence: `git diff 524fa1f90b1f2de44b3019bacf833d54e0af13a0 23fbc174d02fa44662e9aee735bbf6de5cad3f1d -- corpus/SOURCES.md`
changes exactly two data rows, each only in the `opened` column: S028 `2026-10-19` → `2026-11-03`
and S097 `2026-10-20` → `2026-11-03`. Every other cell of those rows is byte-identical (`status`
`mined`, `recheck` `on-release`, `used-by` unchanged). `corpus/SOURCES.md:6-7` says only `status`,
`recheck` and `used-by` change in place. The r65 lesson logged old→new, but the date landed in
`opened`, not in `recheck`. First locator: `corpus/lessons/round-65-verifier-spotcheck.md:126`
(routed item 1).
Captured-by: none — the source census checks row shape, tier and URL collisions, not the column
whitelist, and no instrument compares an existing row's `opened` cell across revisions.
Fix: the r66 source seat appends one new row (S435) and edits no existing row
(`.ufo/waves/round-66/w1/R66ScribeSources.md` § Limits 7). A re-open date belongs in the Gate access
date, and a row-level date in `recheck` or a correction row; a contract-v1 amendment that would
legalise a dated re-open column is proposed only, not applied.
Fix counts only observed red: the r65 diff is observed; no r66 instrument is shown to reject a
future in-place `opened` edit — **UNOBSERVED**.

**M66-2 — a shape-valid register accepts forged state cells; r66 narrows the accepted shapes but
does not bind truth.**
Class: counter design (shape+receipt gate, no truth binding).
Evidence: `.ufo/waves/round-65/w1/R65RevRegister/a3-forge-r65.txt` — eight false state cells with
one real receipt → `MADO_R65_REGISTER: rows=8 groups=8/8 receipts=1 resolved=1 gate=ok
verdict=TARGET_MET` rc=0. The receipt's own header records the counter it ran as `sha256` prefix
`6d28e6ca7c2e7a69`; the committed r65 counter at HEAD reads `2ccedc68…`, so no committed receipt
binds that forge to the committed bytes (evidence-byte caveat below). First locator:
`corpus/lessons/round-65-verifier-spotcheck.md:131`; original M65-2 in `corpus/lessons/round-65.md`
§ Mistakes.
Captured-by: none — git objects at `--rev` cannot prove a row's truth, and the r65 `gate` clause
accepts any resolved receipt containing any `MADO_VERIFY: CLEAN` line, including the file-plane-only
line at `.ufo/waves/round-65/receipts/gate-fileplane-r65.txt:46`.
Fix (r66, structural): `quality/counters/c1-r66-register.py` (draft sha256
`4e1b94ff94309e3bd728b50bb83991c5ca71f5a46602eb96afb06313c5bbf829`) requires exactly one
returned-host heading, exactly eight group rows once each, a resolving receipt in every row's
receipt cell, and the exact live CLEAN line copied from
`.ufo/waves/round-65/receipts/gate-live-r65.txt:65` — `MADO_VERIFY: CLEAN (52 pass, 8 notes; file +
live planes verified read-only)` — rejecting the file-plane-only line. State-cell truth remains NOT
measured: invented state prose with valid per-row pointers is a deliberate selftest pass case
(`R66ExecRegister/selftest.txt`, case `state-truth-not-measured`).
Fix counts only observed red: the r65 acceptance is observed, and the candidate's rejection of the
three controls is observed twice at diagnostic level — the implementer's comparison (baseline 1/4,
candidate 4/4, `R66ExecRegister/controls.json`; selftest 15/15; genuine base
`MADO_R66_REGISTER: headings=1 rows=8 groups=8/8 receipts=4 resolved=4 gate=ok verdict=TARGET_MET
rev=eafd500f…` rc=0) and the frozen harness in `--candidate-draft` mode (C1 baseline
`correct=1/4 TARGET_MISSED`, candidate `correct=4/4 TARGET_MET`; summary at
`.ufo/waves/round-66/w1/R66ExecHarness/evidence/final-c1-cand/r66harness/c1/summary.txt`). Neither
is the post-integration `--rev` score, and truth binding remains unobserved/unmeasured.
Evidence-byte caveat: the 6d28e6ca forge ran before the counter's last pre-landing edit; the
reviewer's own report says "counter bytes may move before landing" and calls the A3 verdict
structural, holding for any variant that honours the frozen predicate
(`.ufo/waves/round-65/w1/R65RevRegister.md:83`). That is plausible but is not a byte-bound
reproduction on the committed counter. This is a criterion-24-class provenance gap in the r65
evidence; it is recorded here and not repaired.

**M66-3 — the landing instrument could not separate red, crash, a skipped child, a drifted default
tree, or a missing sibling.**
Class: instrument hermeticity and vacuous/indistinct verdicts.
Evidence: `.ufo/waves/round-65/w1/R65CriticInstrument/report.md` §S5 — three legs rc=2 produced
`MADO_LANDING_COUNTERS: RED …` exit 1, identical to a genuine red, and selftest a9 passed on
crashes. `.ufo/waves/round-65/w1/R65MutCounters.md` and `evidence/instr-mutants.json` — I1
(citecheck skipped, rc forced 0) and I7 (default citecheck tree redirected to round 64) SURVIVED
with `19/19` selftest; I9 (used-by sibling absent) SURVIVED, and
`evidence/probe-location-blind.log` reads `19/19` with all three siblings absent. Probe bytes: I1
prints `LANDING_LEG citecheck rc=0` then `GREEN` at a rev whose pristine run is RED; I7 prints
`MADO_CITECHECK: … files=21 citations=18 … verdict=TARGET_MET`; I9 prints `LANDING_LEG usedby rc=2`
inside `RED`. First locator: `corpus/lessons/round-65-verifier-spotcheck.md:135`.
Captured-by: none — the selftest asserted that a `LANDING_LEG <leg> rc=<digits>` line was printed,
not that the child ran; nothing pinned the default receipts tree; the aggregate reduced every
non-zero rc to RED/1.
Fix (r66): hardened `quality/landing-counters.sh` (draft sha256
`1671cebc65c13582413d91ee61204d258a8f0d79db015785b8193fc5e0216cae` at the final read; the wave moved
it `f72e579d…`/46 -> `f0c8d74f…`/56 -> `1671cebc…`/58, and no final count is pinned) requires
`--round N`, derives
`.ufo/waves/round-N/receipts`, applies the dirty guard to explicit citecheck paths too, and validates
each child's actual marker against its rc: navigation `revision=… indexed=A/B …`, used-by
`MADO_USED_BY: … verdict=…`, ledger `LEDGER: … verdict=…`, citecheck `MADO_CITECHECK: …
citations=… verdict=…`. A genuine red child (rc=1 with its red marker) yields RED/1; rc≥2, rc=0 with
an absent/inconsistent marker, or a missing used-by sibling yields ERROR/2; ERROR dominates RED;
GREEN requires four green markers and rc=0. The hermetic selftest covers green/red/crash/skipped per
leg, missing sibling, a dirty decoy round and a dirty selected round, explicit dirty paths,
inherited Git steering, required `--round`/`--rev`, tmp-family and symlink scratch refusal.
Fix counts only observed red: the r65 defect is observed (S5/I1/I7/I9). The candidate selftest was
observed at 56/56 on the `f0c8d74f` bytes; the critic then found an empty-note corpus read GREEN/0
where the r65 bytes crashed red (`R66CriticLanding` F2). At the final read the draft was
`1671cebc…` with 58/58 assertions, the added case reading `empty population summary RED`; L1
instructs that no final count be pinned, so these are read-time values, not the integration pin. The
frozen harness's four cases are observed in
`--candidate-draft` mode — C2 baseline `correct=1/4`, candidate `correct=4/4 TARGET_MET mode=candidate`
(`.ufo/waves/round-66/w1/R66ExecHarness/evidence/final-c2-cand/r66harness/c2/summary.txt`) — but
critic F1 shows that count never runs the candidate selftest or a real four-leg landing, so its 4/4
alone does not meet the frozen target. A committed `--round 66` four-leg GREEN and the parent-owned
driver run remain **UNOBSERVED**. The r65 counters and instrument stay frozen.

**M66-4 — the freeze commit landed after the wave registry and the ready marker.**
Class: freeze chronology.
Evidence: `.ufo/waves/round-66/process-defects.txt`; `git show -s --format=%cI ed980316` →
`2026-11-03T20:03:29-03:00`; `.ufo/waves/round-66/w1/swarm-registry.json` `createdAt`
`2026-11-03T23:03:10.291Z` (mtime `20:03:10.290 -03:00`); `.ufo/waves/round-66/w1.ready` mtime
`20:03:21.9 -03:00`. The freeze commit is 19 s after the registry plan time and 8 s after the ready
file, so criterion 106's strict order (freeze committer time strictly earlier than `createdAt`) is
not met.
Captured-by: criterion 106 (`quality/check-freeze-order.py`); this draft does not re-run it.
Fix: chronology cannot be repaired; the round claims no chronological pass and keeps the disclosure.
A later wave freezes before writing the registry and the ready file.
Fix counts only observed red: the ordering fact is observed; no fix is claimed.

**M66-5 — the frozen declaration named a marker the child does not emit.**
Class: spec premise (remembered literal vs actual child output).
Evidence: `.ufo/waves/round-66/marker-premise-erratum.md`; `quality/check-tool-ledger.py:368-371`
prints `LEDGER: population=… ledger_rows=… uncovered=… dangling=… bad_pointer=… empty_desc=…
verdict=TARGET_MET|TARGET_MISSED rev=…`, as observed in
`.ufo/waves/round-65/w1/R65MutCounters/evidence/probe-I1.log`; the frozen C2 text says "ledger
MADO_TOOL_LEDGER".
Captured-by: R66ExecLanding's pre-implementation inspection of the actual child (the erratum names
it).
Fix: the implementation anchors the actual `LEDGER:` line and never renames or fabricates child
output; the four C2 outcomes, target 4/4, default-round scope and scratch predicates are unchanged;
closure may grade the literal mismatch as a conformance defect.
Fix counts only observed red: the child's actual line is observed in committed r65 receipts; the
candidate's marker binding is observed in the seat selftest and the harness shim, while the
committed four-leg run remains **UNOBSERVED**.

## Observed / unobserved at draft time

| item | state | pointer |
|---|---|---|
| r65 in-place `opened` edit (S028, S097) | observed | `git diff 524fa1f9 23fbc174 -- corpus/SOURCES.md` |
| r65 forged-cell acceptance | observed | `w1/R65RevRegister/a3-forge-r65.txt` |
| r65 landing mutants I1/I7/I9 survive | observed | `w1/R65MutCounters/evidence/{instr-mutants.json,probe-I1.log,probe-I7.log,probe-I9.log}` |
| r65 red/crash indistinguishability | observed | `w1/R65CriticInstrument/report.md` §S5 |
| freeze-order miss | observed | `process-defects.txt`; timestamps above |
| C1 candidate selftest 15/15, controls 1/4 → 4/4, genuine base TARGET_MET | observed at seat level | `w1/R66ExecRegister/{selftest.txt,controls.json,genuine-base.txt}` |
| r65 forge bound to a superseded counter revision | observed | a3 header `6d28e6ca` vs committed `2ccedc68` |
| C1 harness diagnostic (`--candidate-draft`): baseline 1/4, candidate 4/4 | observed diagnostic | `w1/R66ExecHarness/evidence/final-c1-cand/r66harness/c1/summary.txt` |
| C2 harness diagnostic: baseline 1/4, candidate 4/4 | observed diagnostic | `w1/R66ExecHarness/evidence/final-c2-cand/r66harness/c2/summary.txt` |
| harness c2 count omits candidate selftest + real four-leg landing | observed defect (critic F1) | `w1/R66CriticLanding.md:35,43` |
| C2 candidate selftest 58/58 at final read (not final) | observed at seat level | `w1/R66ExecLanding/selftest.txt` (sha `1671cebc…`) |
| v2 empty-note corpus reads GREEN/0 where r65 was red | observed defect (critic F2); later draft adds case 58 `empty population summary RED` | `w1/R66CriticLanding.md:58`; `w1/R66ExecLanding/selftest.txt` |
| C2 driver baseline TARGET_MISSED (`--round` unsupported) | observed | `w1/R66ExecDriver/report.md` |
| mutation hardening of final candidates | observed at seat level (C1 4/4 killed incl. selftest; C2 7/7 killed) | `w1/R66MutHardening.md` §§4-5 |
| post-integration `--rev` re-score of C1/C2 | unobserved | requires committed candidates |
| committed integrated four-leg landing GREEN (`--round 66`) | unobserved | requires L1 integration + committed r66 receipts |
| C2 candidate selftest final count after the empty-corpus fix | unobserved | fix in flight; no final count pinned |
| parent-owned C2 driver run on the integrated rev | unobserved | `w1/R66ExecDriver/report.md` § Limitations |
| r66 census end, S435 admission | unobserved | L1/closure; no row is admitted in this draft |

## Gate

No row is admitted or rejected in this draft. The source seat's single draft row is quoted below for
L1 integration; admission of S435 is the closure's decision, not this seat's, and the row cannot
prove C1 register truth or that any C2 child ran.

### Draft source row S435 (as drafted by R66ScribeSources; not admitted here)

- Source: GNU Bash Reference Manual §3.7.5 Exit Status —
  https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html
- Access date: 2026-11-03 (opened this round).
- Located quote (15 words, ≤25): "So while an exit status of zero indicates success, a non-zero
  exit status indicates failure." — `Exit-Status.html:68-69`. Supporting quote (18 words): "If a
  command is not found, the child process created to execute it returns a status of 127." —
  `Exit-Status.html:77-78`.
- Version/section: §3.7.5 of Bash Reference Manual 5.3 (18 May 2025); host `bash --version` →
  `5.3.20(1)-release`. Digests: node 5,187 B
  `b5489d3d21e32da01de356e7a63093ec276a60a020d616a05fffcc9b7b19d983`; single page 1,040,954 B
  `78d0eefbe60cfe7345ffdafede7294f055b04e53bd520360ff699b24f81e2b4b`; identical after a second
  fetch.
- used-by: `corpus/lessons/round-66.md` (this file; a census E11 fires if the row lands before this
  path exists).
- Declared limits (source seat): cannot prove any register row's truth or that a child ran, returned
  a given rc, or emitted a marker; the manual is series-level 5.3, not 5.3.20; the page is live HTML
  with no tag, so the digest is the only drift check (`recheck: on-release`); the lane's rc=2 crash
  class is a convention, not this source's claim.

## Frontier

- Census start: `.ufo/waves/round-66/census-start-r66.txt`, exit 0, 37 pre-existing W01/W04 lines
  (seat-measured by R66ScribeSources; this seat did not re-run the census).
- No new knowledge entry, no new surface group, no C3 claim, assimilation none.
- S435 supports C2 child exit-status vocabulary only; it is not evidence for C1 truth or for any
  child having executed.

## Routed defects (carried; identity and age)

| id | item | first locator | age (rounds) | r66 status |
|---|---|---|---|---|
| R65-1 | SOURCES rule-2 `opened` cell edited in place | `corpus/lessons/round-65-verifier-spotcheck.md:126` | 1 | process control only (M66-1); no instrument — open |
| R65-2 | C1 accepts forged state cells | `corpus/lessons/round-65-verifier-spotcheck.md:131` | 1 | three structural controls drafted (M66-2); truth gap explicitly open |
| R65-3 | landing instrument red/crash/skip/tree-pin/sibling residue | `corpus/lessons/round-65-verifier-spotcheck.md:135` | 1 | hardened instrument drafted (M66-3); committed demonstration open |
| R65-4 | wave role split: no planner seat; L1 planned | `corpus/lessons/round-65-verifier-spotcheck.md:138` | 1 | process note, operator-owned, not a claim defect — unchanged |

Age derivation: `printf '%s\n' $((66-65))` → `1`. Ages are round deltas from the first routing round
(`65`) to this round (`66`); they are restated here, not emitted by a ledger.

## Notes for round 67

1. R65-1 has no capturing instrument. A column-whitelist diff (existing row's `opened` cell
   unchanged between revisions) is a candidate, not registered here.
2. R65-2's truth gap stays open: the r66 counter adds heading uniqueness, per-row receipts and the
   exact live line, and deliberately leaves state-cell truth unmeasured. Do not read its green as
   truth binding.
3. R65-3 needs the committed integrated four-leg GREEN and the mutant re-run before any closure; the
   seat selftest's shimmed children are not that evidence. The count harness must also run the
   candidate selftest and the real four-leg landing — its a-d 4/4 alone over-credits (critic F1) —
   and the empty-note-corpus false-green (critic F2) needs its own regression case before the
   selftest count is final.
4. If S435 is admitted, it must land with this lesson path present, or the census E11 fires on the
   unresolvable `used-by` cell.
5. The r65 counters (`quality/counters/c1-r65-register.py`, `quality/counters/c2-r65-landing-
   instrument.py`) and the r65 instrument bytes stay frozen; r66 adds successors, never an edit.

## Landing addendum

No landing measurement is claimed in this draft. C1/C2 admission, the committed landing run, the
census end and the promotion decision are L1/closure/operator-owned.
