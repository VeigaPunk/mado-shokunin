# Attack20 — C1 red control defect-isolation

Seat `Attack20` (leaf, reviewer/attacker). Wave w2, round 52, lane `mado-shokunin`.
Every number below was produced by re-execution in this seat's own scratch fixtures;
no W1 receipt was trusted without an independent run. Source-only fences held: no
package query, no live read, no probe/screenshot, no producer execution, no tracked edit,
no git/jj mutation in the lane (fixtures are throwaway clones under scratch, each git
mutation preceded by a `git rev-parse --show-toplevel` assertion). No tools installed.

## Attacked clauses

- `claims-frozen.md` C1 — "Demonstrate production pass and control fail at the frozen
  revision"; the control is "a no-work control of repeated generic self-pointers".
- `registration.md` C1 — "It must pass on the existing production ledger at the base
  revision and fail on `controls/c1-do-nothing.md` **specifically for self-pointer/context
  defects**." (`registration.md:7`, emphasis added.)
- `registration.md:15` — "C1 do-nothing control `controls/c1-do-nothing.md` is the
  committed ledger shape with only repeated generic self-pointers. … Controls cannot be
  changed after workers score them."

Base for all runs: `85d57a818c3707397e21c840b6498b105ba798aa`. Subject counters: the
incumbent committed gate `quality/check-tool-ledger.py`, the incumbent
`quality/counters/c1-r51-ledger.py`, and the W1 draft
`.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py` (sha256
`0fe862f116a789e8f6bebf38dea74b1f5ee20b3c810190ecf295621a3c34dc31`, verified before use).
Fixture revisions are recorded per item; full stdout in `Attack20/receipts/`.

## Verdict up front

The W1 finding is **confirmed and sharpened**: `controls/c1-do-nothing.md` does not
isolate the two required defect classes. Under both incumbent gates its failure is a
pure function of its 4-cell schema, its duplicate row, and its 2-row coverage (A1–A3),
and the incumbent gates pass the very same defect semantics at full population (A4).
The W1 draft counter does name both defects on the control and its signals are causal
(A5, A6) — but the red arm's attribution is **gate-design-dependent**, demonstrated by
two patched compliant gates: one fails the control naming *neither* required defect (A7),
the other fails it naming *only one* (A8). A true isolating red exists; it is a different
fixture (A9). The context half of the control's defect is the weakest instance of its
class: the final draft bytes still accept a zero-content counterfeit (A10).

---

## A1 — Incumbent committed checker on the frozen control: shape + coverage, nothing else

*Attacked:* registration C1 red-arm attribution, under the lane's own enforcement gate.

*Reproduction:* fixture `fix-ctl` (control bytes verbatim at `quality/tool-ledger.md`,
clone commit `5099ef42a2afb4d830def6349a675c978a15cdbd`):
`python3 -I quality/check-tool-ledger.py --repo <fix> --rev HEAD`

*Observed:* exit 1; `LEDGER: population=82 ledger_rows=0 uncovered=82 dangling=2
bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED` (`receipts/fix-ctl.chk.out`). Both
4-cell rows are malformed (`dangling`); there are no self-pointer or context fields in
this gate at all.

*Verdict:* reproduced. The committed gate fails the control for row shape and coverage;
it cannot attribute anything to the required defects because it has no such checks.

## A2 — Incumbent r51 counter on the frozen control: fails without any new-check logic

*Attacked:* "control fail" as evidence that a counter implements the new predicate.

*Reproduction:* same fixture:
`python3 -I quality/counters/c1-r51-ledger.py --repo <fix> --rev HEAD --work <scratch>`

*Observed:* exit 1; `C1_R51: … ledger_rows=2 uncovered=81 … bad_pointer=1 … dup=1 …
verdict=TARGET_MISSED` (`receipts/fix-ctl.out` under the r51 section). The r51 counter —
the instrument the frozen claim explicitly deems insufficient — fails the control via
pointer-shape and duplication, with no self-pointer/context measurement.

*Verdict:* reproduced, and this is the decisive non-isolation fact: **the literal red arm
("fail on controls/c1-do-nothing.md") is already satisfied by a counter that implements
none of the required checks.** Discrimination between old and new counters cannot come
from the control's exit status; it can only come from per-field attribution.

## A3 — Schema-normalized, deduplicated control under incumbent gates: coverage only

*Attacked:* the claim that the control's failure tracks the required defects rather
than its schema.

*Reproduction:* `fix-ctl-3cell-1row` (control semantics normalized to the ledger's own
3-cell row grammar, single unique row, pointer `quality/tool-ledger.md`; commit
`32a569a1dd350d0efccb25088dbea0d839758d94`), same two commands as A1/A2.

*Observed:* committed checker — exit 1, `LEDGER: population=82 ledger_rows=1
uncovered=81 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED`
(`receipts/fix-ctl-3cell-1row.chk.out`). r51 counter — exit 1, `C1_R51: … uncovered=81
… bad_pointer=0 … verdict=TARGET_MISSED` (`receipts/fix-ctl-3cell-1row.out`).

*Verdict:* falsifier confirmed. With schema and duplication removed, the *only* remaining
failure cause is coverage (`uncovered=81`); the generic self-pointer itself scores
`bad_pointer=0` under r51 resolution semantics (the pointed-to ledger bytes contain the
row basename). The incumbent red is a pure function of confounds the frozen predicate
does not name.

## A4 — Round-51 gap at full population: incumbent gates pass an all-self-pointer ledger

*Attacked:* the premise that the control is needed at all to exhibit the gap; also the
"committed ledger shape" wording in `registration.md:15`.

*Reproduction:* `fix-allself` (all 82 population rows retained, unique paths, every
description "Generic accountability pointer to this ledger itself.", every pointer
`quality/tool-ledger.md`; commit `1a558277ff2a4451c039a829900cc714243da29f`), both gates.

*Observed:* committed checker — exit 0, `… ledger_rows=82 uncovered=0 dangling=0
bad_pointer=0 empty_desc=0 verdict=TARGET_MET` (`receipts/fix-allself.chk.out`). r51
counter — exit 0, `C1_R51: … verdict=TARGET_MET` (`receipts/fix-allself.out`).

*Verdict:* reproduced at scale. A no-work ledger carrying exactly the target defect set
— generic descriptions plus ledger-wide self-pointers — passes both incumbent gates
once coverage is satisfied. The natural red arm is a full-population grammar-valid
no-work ledger, not the 2-row frozen control, which trips shape/coverage before any
semantic clause is reached.

## A5 — W1 draft counter on the frozen control: both defect classes named (independent re-run)

*Attacked:* W1 red receipt for the draft counter (`C1CounterDesign.md`,
`C1Fixture.md`) — verified, not trusted.

*Reproduction:* `python3 -I .ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py
--repo <lane> --rev 85d57a8… --work <scratch> --ledger .ufo/waves/round-52/controls/c1-do-nothing.md`

*Observed:* exit 1; detail lines `self_pointer path=tools/mado-verify.sh
target=quality/tool-ledger.md`, `generic_desc path=tools/mado-verify.sh
reason=no-instrument-specific-phrase`, `dup`, `uncovered=81`; summary
`self_pointer=1 generic_desc=1 … verdict=TARGET_MISSED`
(`receipts/c52ctl.out`). Byte-identical field values on the committed-fixture twin
`fix-ctl` (`receipts/c52-fix-ctl.out`).

*Verdict:* reproduced on final bytes. For this specific counter, the control's red
receipt names both required defect classes.

## A6 — Deconfounded variants under the draft counter: signals are causal

*Attacked:* whether the draft's `self_pointer=1/generic_desc=1` on the control depends
on the confounds (dup, 4-cell shape).

*Reproduction and observed* (`receipts/c52-fix-*.out`):

| fixture | commit | dup | self_pointer | generic_desc | other |
|---|---|---|---|---|---|
| `fix-ctl-3cell` (normalized, 2 identical rows) | `fc7e22a051a0042e32e89d921ac5ec8f7772abfd` | 1 | 1 | 1 | — |
| `fix-ctl-3cell-1row` (normalized, deduplicated) | `32a569a1dd350d0efccb25088dbea0d839758d94` | 0 | 1 | 1 | — |
| `fix-ctl-dedup-4cell` (unique 2nd tool, shape kept) | `00fe46d3899d5ff2252dec3481d0b0518750f11e` | 0 | 2 | 2 | — |
| `fix-ctl-legit-ptr` (PROVINCE.md pointers, generic desc kept) | `936666bc4cc84e275b4ada45982768a0a72b2366` | 0 | **0** | 2 | bad_pointer=0 |

*Verdict:* for the draft, neither duplication nor 4-cell shape is load-bearing, and the
self-pointer charge is causal: giving the rows a legitimate accountable document
(`PROVINCE.md:18/:30`, which resolve with `bad_pointer=0`) removes `self_pointer`
entirely while `generic_desc` still fires. **But** A7/A8 show this behaviour is the
counter author's design choice, not something the frozen control enforces.

## A7 — Falsifier: a schema-strict gate fails the control naming *neither* required defect

*Attacked:* the frozen predicate's silence on wide-row handling.

*Reproduction:* scratch-patched copy of the draft (`c52-patchA.py`): rows whose cell
count differs from the ledger's own 3-cell grammar are scored as `dangling`, mirroring
the committed checker's rule and the ledger's stated row contract. Run on the frozen
control via `--ledger`.

*Observed:* exit 1; `dangling=2 uncovered=82 **self_pointer=0 generic_desc=0**
verdict=TARGET_MISSED` (`receipts/pA-ctl.out`).

*Verdict:* falsifier. A gate that enforces the ledger's published 3-cell row grammar
and implements uniqueness/resolvable/non-self/context checks for well-formed rows
still fails the frozen control — attributing the failure to nothing the registration
names. Two gates can therefore both be plausibly compliant with the frozen text yet
disagree on whether the control demonstrates the required defects. The control isolates
nothing unless wide-row scoring is pinned by the predicate.

## A8 — Falsifier: a pointer-region-only self scan silences the self-pointer defect

*Attacked:* the control's content as a "repeated generic self-pointer" (claims C1,
registration:15).

*Reproduction:* scratch-patched copy (`c52-patchB.py`): the `self_pointer` charge fires
only when the ledger (or the row's own path) is named in the pointer region — the
natural reading of "non-self **evidence targets**", since the row grammar defines cell 3
as the accountability pointer. Run on the frozen control via `--ledger`.

*Observed:* exit 1; `self_pointer=0 generic_desc=1 bad_pointer=1 (reason=
no-target-names-the-instrument) … verdict=TARGET_MISSED` (`receipts/pB-ctl.out`).

*Verdict:* falsifier, confirming `C1Simplify.md` §1 by execution: the control's rows
hold `nothing` in the Writes cell; the ledger path appears in the Reads cell (cell 2)
and the words "this ledger" appear in prose. There is **no self-pointer in the pointer
cell at all**. Under a compliant pointer-region reading the control fails only the
context half of the required defect set; the self-pointer half is invisible. (The draft
counter sees it only via its wider all-cell fallback — its design decision #2.)

## A9 — The true isolating red exists, and it is not the frozen control

*Attacked:* what defect isolation requires; whether any fixture fails *only* for the
two required reasons.

*Reproduction:* `fix-isored` (all 82 population rows, unique paths, unique generic
descriptions "Generic accountability note N pointing back at the ledger.", every
pointer `quality/tool-ledger.md`; commit `9a6cefa4f6fef39d3cffa068137ab952bb276192`),
all three gates.

*Observed:* committed checker — exit 0, `TARGET_MET` (`receipts/isored-chk.out`).
r51 counter — exit 0, `C1_R51: … verdict=TARGET_MET` (`receipts/isored-r51.out`).
Draft counter — exit 1, `population=82 ledger_rows=82 uncovered=0 dup=0 dangling=0
bad_pointer=0 **self_pointer=82 generic_desc=79** verdict=TARGET_MISSED`
(`receipts/isored-r52.out`).

*Verdict:* verified. Isolation requires a full-population, grammar-valid, duplicate-free,
resolvable ledger carrying only the intended defects; then both incumbent gates pass it
and the draft fails it on exactly the required fields (three rows escape `generic_desc`
because their instrument bytes happen to bind a qualifying phrase — observed, not
load-bearing, since `self_pointer=82` alone forces the miss). The frozen control
satisfies none of the isolation preconditions.

## A10 — Context-signal ceiling: zero-content counterfeit still lands green

*Attacked:* the strength of the "context defect" the control demonstrates, bounding the
context half of the red arm.

*Reproduction:* draft counter with `--ledger` over `C1Simplify`'s read-only controls
(final bytes `0fe862f1…`).

*Observed:* `control-H-minimal-forgery.md` (one row's description = prediction id +
filler) — exit 0, `generic_desc=0 verdict=TARGET_MET` (`receipts/f3-control-H-minimal-forgery.md.out`).
`control-F3-forged.md` (82 distinct forgeries each quoting a word pair from its
instrument) — exit 1 but only `generic_desc=10` of 82 (`receipts/f3-control-F3-forged.md.out`).
`control-G-legit-ledger-reader.md` — exit 0 `TARGET_MET` (no false positive on an honest
ledger-mentioning description).

*Verdict:* reproduced against final bytes. The frozen control's generic text is rejected
only because it binds no instrument phrase whatsoever; any counterfeit that quotes the
instrument's own id bytes passes. This is inside the claim's "bounded accountability
checks, not prose entailment" wording, so it is a disclosed ceiling, not a predicate
violation — but it bounds what the control's context arm proves.

---

## Smallest safe correction

1. Keep the frozen control (controls cannot change post-scoring, `registration.md:15`),
  but demote it to a *presence* red only; require the red receipt to quote
  `self_pointer` and `generic_desc` fields and require both non-zero — the
  `C1Fixture` harness already encodes exactly this and should remain the arbiter.
  Raw exit status must never be accepted as the red arm (A2).
2. Add a pinned supplementary fixture of the `fix-isored` shape (full population,
  grammar-valid, unique, resolvable, only the two intended defects; sha256-recorded)
  as the attribution-bearing red (A9); this is the same correction `C1ControlAttack`
  recommended — independently reached here by execution.
3. Pin two readings into the predicate so A7/A8 cannot recur by design choice:
  wide rows are **scored, not discarded**, and the self-pointer scan covers the row's
  whole accountability claim (pointer region plus rows that designate no accountable
  target while naming the ledger). Both are one-line contract sentences; without them
  "fail specifically for self-pointer/context defects" is not decidable from the
  control.
4. Report A10 as a bounded ceiling in the integration claim; do not widen the predicate
  toward prose entailment.

## Limitations

- A7/A8 use patched scratch copies of the W1 draft as existence proofs of predicate
  under-specification; they are not claims about the draft's quality, and they were
  never written to any tracked path.
- The draft counter's bytes are the W1 seat artifact; integration into
  `quality/counters/c1-r52-ledger.py` is the L1's call. At report time the lane worktree
  shows integration activity (untracked `quality/counters/c1-r52-ledger.py`, a new
  knowledge entry, and tracked modifications) from other seats; this seat read only
  committed bytes at the base revision plus the W1 seat files, and made no lane writes.
- In the first incumbent-gate batch the driver reported the exit code of `tail`, not of
  python; all quoted verdict lines are unaffected, and every item where the exit code
  matters (A5–A10) was re-run with the corrected driver (`exit=` lines above).
- The committed checker rejects `--work` outside `--selftest` (exit 2); its runs used
  environment redirection only, which is sufficient (it writes nothing).
- A9's `generic_desc=79/82`: three descriptions accidentally bound a qualifying phrase
  from their instrument's bytes; reported as observed fixture wording, not counter
  behaviour.
- Scratch `/fast/scratch/hyaku/mado-r52/Attack20/` was removed after receipts were
  copied into this seat directory; no packages installed; lane `git diff`/`git status`
  show no changes attributable to this seat.

## Receipts

- `Attack20/receipts/` — verbatim stdout of every run cited above, one file per item.
- Fixture definitions are reproducible from the `## Reproduction` lines (each fixture is
  a `--shared --no-checkout` clone of the lane at the base revision with
  `quality/tool-ledger.md` replaced as described and committed under a scratch
  identity; fixture commit shas are quoted per item).

Report: `.ufo/waves/round-52/w2/Attack20.md`
