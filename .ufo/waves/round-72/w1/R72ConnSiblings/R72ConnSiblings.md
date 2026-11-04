# R72ConnSiblings — cross-lane contract boundary

## Axes and evidence posture

- **C1 calibration:** kill credit requires the last failing summary plus exactly `n-p` captured `SELFTEST FAIL` lines.
- **C2 operability:** outcome requires kills `2/2` and the last positive-denominator all-green gate summary; the child exit is evidence, not a gate.

Authority: `.ufo/waves/round-72/claims-declaration-r72.md:39-102`, read first. Base `976684a27e99c2508037a60eec415f550f53d70e`; scored instruments `9bcb4fd5b598844f168230dc05e441721d95b272`.

**Relayed, not re-measured:** frozen `measurement-c1-r72.txt:20-21` records `cases=8 correct=8 base_correct=6 verdict=TARGET_MET`, `C1_RC=0`; `measurement-c2-r72.txt:13-14` records `cases=8 correct=8 base_correct=4 verdict=TARGET_MET`, `C2_RC=0`. Both baseline receipts were re-read: C1 has exactly two `correct_for_held=NO` rows; C2 has four `held_correct=NO` rows. These are observations of existing receipts, not a new execution or admission.

## Sibling doctrines: report, do not absorb

Paths in this section are relative to the fleet root, not the mado lane. Source inspected read-only; no sibling runtime invoked.

### Summary over process status exists: kengaku

`kengaku-shokunin/SKILL.md:604`, the `git-webserver-probe` registry row, says:

> **mismatches are on the summary line, never in the exit code** (`mismatches=1` still exits 0, measured)

The row distinguishes successful measurement completion from prediction agreement. This is an adjacent instance of C2's essential distinction: process completion does not carry the measured assertion result. It is not mado's exact grammar or outcome function. **Reuse the distinction in explanation; defer implementation and ownership to kengaku.** No shared parser, imported instrument, or stronger blanket rule follows.

### Detail/summary arithmetic exists: kasegi

`kasegi-shokunin/corpus/instruments/kill-rule-check.py:17-20` says:

> one `selftest cases=N failures=0` summary whose N equals the number of case

and:

> stdout carries only the summary is rejected as `summary-only`; a forged

The executable predicate `accept_selftest`, lines 444-455, rejects missing case detail and disagreement between summary count and case-line count. Lines 459-464 additionally compare pristine case names and reject duplicate cases. This corroborates C1's report-consistency idea, **not authentication of execution**. Its protocol is stronger/different in specific ways: exactly one summary, named case population, pristine floor, and an exit-zero requirement at lines 437-438. **Do not copy it into the frozen mado predicate**: importing its exit gate or single-summary rule would contradict this round's C2 or last-summary contract. Kasegi retains ownership of that fuller protocol.

### Arithmetic plus attribution exists: tameshi; exit doctrine explicitly differs

`tameshi-shokunin/tools/bash-witness-study.py:495-496` says:

> reasons.append(f"failure-count={runinfo['failures']}"
>                f"!=bad-case-count={len(runinfo['bad'])}")

`run_problems` checks case population, numbering, labels, skips and failure arithmetic (lines 464-500). `classify` lines 521-524 requires a declared failing witness for `killed-on-witness`, otherwise `accidental`.

**Contradiction, not a scalar ranking:** lines 497-500 reject summary/exit disagreement; the selftest at line 1525 explicitly names:

> check("KILLED with exit 0 is inconclusive",

Mado intentionally credits a detail-backed failing summary even with exit zero, and intentionally permits a green outcome with child exit two. Tameshi's witness protocol intentionally refuses disagreement. They answer different contracts; there is no globally interchangeable “kill” parser. **Defer witness attribution to tameshi; do not absorb its exit policy.** Mado's count agreement is not equivalent to tameshi's named-case attribution, nor does either quoted arithmetic establish cryptographic authenticity.

## Operator input: no qualifying unimplemented proposal established

Read `considerthese/2026-10-28.md:50-57` in full. No still-unimplemented proposal can be established from the inspected local evidence that also fits this round's landing-instrument scope.

The tempting exact wording is proposal 5:

> **Separate "relayed" from "re-measured" in every number.** The closures re-ran some tools on the host and only evidence-verified others. I should mark each number I quote with which of the two it is, as the spot-checks do.

It fits evidence reporting, but the input itself says spot-checks already do this; `corpus/lessons/round-13-verifier-spotcheck.md:41-43` and `round-14-verifier-spotcheck.md:43-45` already distinguish fresh measurement from evidence verification. I cannot truthfully label it still-unimplemented universally from those facts. Proposal 4 is explicitly still unadopted in `corpus/lessons/round-71.md:147-149`, but it governs live tools, not this host-free landing-instrument round. Thus **no adoption candidate claimed**; the quoted proposal is context, not a second proposed move.

## Round-71 contention and remaining limit

`.ufo/waves/round-71/w1/R71RevC1.md:66-68`:

> the inconsistency is that the same doctrine is not applied to the
> unmutated selftest leg.

This is the specific predecessor objection C2 addresses, not a reason to reintroduce an exit gate.

The same seat's lines 72-74:

> Summary-only credit severs the evidentiary link between the mutation and the failing summary:
> a lane whose output does not depend on the deleted clause at all (canned/stale/echoed failing
> summary) earns the kill.

C1 closes bare-summary and mismatched-detail examples, not complete transcript replay. Frozen claims lines 70-73 expressly preserve that limit. The prior review also states at lines 83-85 that “last” is stdout-then-stderr concatenation position, not execution chronology. Merely reading both streams does not authenticate their order or source. Neither concern is erased by the relayed finite target results.

## One bounded proposed move

**Add a contract-boundary evidence note to this round's closure, rather than introducing a cross-lane parser or generalized “authentic kill” label.** Use one compact comparison: mado = summary/detail count agreement, exit recorded; kengaku = summary carries measurement; kasegi/tameshi = own named-case and exit-consistency protocols. Explicitly label frozen counts as relayed unless actually re-executed, and retain the replay/stream-order limits.

This is a reporting proposal only, supplied here for the L1; no production draft, integration, or judgment is made.

- **Affected axes:** [INFERENCE] improves C1 calibration by preventing count consistency from being advertised as execution authentication, and C2 operability by preventing adjacent exit gates from being imported into the wrong protocol. No new scored gain asserted.
- **Runtime:** no child invocation, changed decision, new dependency, or shared parser.
- **Contract:** frozen denominators, last-summary selection and exit-independent outcome remain unchanged. Cross-lane disagreement stays explicit.
- **Substrate:** read-only sibling files; no host/config/service access and no sibling writes. No tool installed or updated.
- **Risk:** readers could interpret the note as a new admission condition or as rejection of tameshi's protocol. State that each protocol retains its owner and that the note changes neither frozen claim.
- **Verification for L1:** review the note against the cited predicate lines; confirm that `green-summary-exit2` remains green, `liar-success` remains credited when detail agrees, and bare/mismatched detail remains uncredited using the already-frozen receipts or the declared counters with explicit scratch roots. Do not substitute a kasegi/tameshi exit check. No new counter run was performed by this seat.

## Scope and path resolution

Only this report was written. Own scratch was created explicitly and removed empty before completion. No VCS mutations, fixtures, production edits or runtime launches occurred. The assignment's flat `.ufo/waves/round-72/w1/R72ConnSiblings.md` trailer conflicts with its stricter directory-only write bound; the deliverable is nested under the authorized own directory instead.

Report: .ufo/waves/round-72/w1/R72ConnSiblings/R72ConnSiblings.md
Summary/exit separation exists in kengaku; detail arithmetic exists in kasegi and tameshi.
Sibling exit-consistency rules contradict mado's frozen contract and must not be absorbed.
One closure-note proposal preserves limits and provenance; no execution or admission claimed.
