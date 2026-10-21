# CriticRecovery — round 22 W1 critic review

Seat: `MadoR22.CriticRecovery`. This is author-lane advice only: no judgment, admission, closure or streak disposition. Structured note: `.ufo/waves/round-22/w1/notes/CriticRecovery.json`.

## Bottom line

The registration correctly precedes implementation. There are no `tools/` changes since base `741122d`, and the tripwire is still `46c82902…`, the same bytes as r21 final. Four admission conditions are nonetheless weak enough that a passing r22 could hide harm or overstate history:

1. **The three-rejection streak is not enforced.** The fleet driver does not block mado now, and would not block it after a fourth rejection.
2. **C2's "actual r19" target cannot be met honestly as written.** Faithful r19 bytes yield could-not-evaluate (code 2). The 5 observed + 1 lead split is counted in incident lines, not finding rows, and its labels come from a round-20 detector.
3. **The no-harm corpus guard cannot see added rows or unparsed-counter changes.** F2 failures, and r19's original false positive, show up as exactly those.
4. **Non-author closure is not defined operationally.** The same party may end up authorizing the recovery, closing it and disposing of its streak.

## Counterexamples

### CR1 (high): the streak is not enforced, and the authorization has no source

- **Driver behavior.** `scripts/hyaku/inline.sh:164` counts a round toward the streak only when its outcome file is exactly `rejected`.
- **Mado state.** The outcome files under `~/.local/state/shokunin-hyaku/outcome/` read `mado-r19=rejected`, `mado-r20=rejected` and `mado-r21=rejected-harmed`.
- **Writer of the r21 token.** `rejected-harmed` was written at 07:24:49. The driver's `closure_count` (`inline.sh:64-71`) emits only `admitted`, `rejected` or `none`, so this token came from somewhere else.
- **Effect.** The streak at r21 counts 2. No `blocked/mado` file exists; `blocked/` holds only `kumitate`. Mado r22 launched at 11:14:32 (`watchdog.log:602`).
- **Contradiction.** MANIFEST `rounds[400].notes` says "lane blocked".
- **Fourth rejection.** If r22 is rejected, the r22/r21/r20 window again counts 2, so the lane still does not block.
- **Authorization.** `registration.md:3` says "Operator permission" but gives no pointer:
  - The r21 L0 question (`l0-questions.md:78`) has no recorded answer.
  - The dispatch prompt (`mado-round-22.md`, fleet `0820349`) contains no unblock or authorization sentence.
- [INFERENCE] The launch is mechanically explained by the outcome-token mismatch.
- **Fix, outside this lane.** Main or the operator normalizes the r21 outcome token, or makes the streak test match the `rejected*` prefix, and records the disposition.
- **Fix, in this lane.** An append-only registration clarification citing the authorization artifact, or stating that none is committed. The lane must not edit driver state.

### CR2 (high): C2's actual-r19 gap is mis-stated

1. **Faithful r19 bytes yield code 2, not red.** Neither r19 artifact carries an evidence marker:
   - `tw-recall-after.txt` (`8ff13d23…`) rows hold only `{file,line,detected}`.
   - `tripwire-frozen-scan-classes.txt` (`64648cca…`) has 11 rows with class and command but no `evidence` key.
   - The contract treats a missing marker as uncertainty, and the frozen W1 proposal `AuditMissingEvidence` expects code 2. So an unchanged r19 snapshot is could-not-evaluate.
   - A red result needs labels added, which changes rows.
2. **Unit mismatch.** The contract counts finding rows. r19 has 11 rows over 6 incident lines.
   - "5 observed + 1 lead" is the incident-line split. The row split is 10 observed + 1 lead.
   - A row-level claim of 6/5/1 against the real snapshot is red, so the registered green is unreachable without collapsing rows.
3. **Label provenance.** The split exists only in round-20 `recall-split-final.txt` (`5165b728…`), produced by r20 tool `9613f510…` at `28c6837`, inside the rejected-harmed round 20.
   - My read-only join of the two committed receipts matches 11 = 11 rows by `(file,line,class,rule)`. The single lead is `r13-root.jsonl:4`.
   - Only that lead has independent authority: `round-19-verifier-spotcheck.md:65`.
4. **The "observed 6/6 assertion" is r22-authored.** r19 asserted detected=6 with no evidence tier and self-disclosed "5/6 without the HelperFn rule-B lead".
   - Presenting a constructed observed=6 claim as "the actual r19 receipt red" repeats the manufactured-baseline pattern that r21's registration clarification refused.

**Fix:** before seal, add an append-only clarification that replaces the single target with three provenanced fixtures.

| Fixture | Snapshot | Claim | Expected |
|---|---|---|---|
| (a) | Raw r19 scan, bytes unchanged | n/a | code 2, `evidence_audit_input_invalid` |
| (b) | Translated: r19 scan rows plus an evidence key joined 1:1 from r20 split | total 11, observed 11, lead 0, errors 0, clean false | code 1, `observed_count_mismatch` + `lead_count_mismatch` |
| (c) | Same as (b) | total 11, observed 10, lead 1, errors 0, clean false | code 0 |

Fixture (b) must name both receipt digests, the r20 tool digest and verifier `:65` as its translation provenance. Use row-level wording, and never call (b)'s claim an r19 assertion.

### CR3 (medium): the contract cannot represent an unknown error count

- The registration demands "explicit unknown/error totals", but the contract requires exact integer file counters.
- Zero-filling a missing counter would fake a clean population.
- The W1 proposals also mix `expected.code` types: integer `2` in `AuditNoFiles`, strings elsewhere.
- **Fix:** missing counters are input-invalid and never zero-filled. Normalize the code type in `assemble.py` and record the normalization as a reason, not a silent cast.

### CR4 (high): the no-harm corpus guard has blind spots

The comparator is `.ufo/waves/round-21/corpus/compare.py`.

- **Additions are unguarded.** The registered guard compares removals and errors only, yet F2 and r19's frozenset failure are added false rows. r21's 104 added groups were never individually adjudicated (`dispositions.json` `addition_side`).
- **Unparsed counters are ignored.** Lines 104-108 diff findings only, never the `eval_unparsed`/`unparsed_spawns` stats.
- **Error pairs are skipped.** Lines 101-103 skip any file where either side errors, which covers the 108 inherited pairs. The exit is always 1, so it cannot signal no-harm.
- **The baseline is undeclared.** The registration names neither the a6cef89 tool nor the r21 `tool-before.py`.
- **Fix:** declare both baselines and the comparator digest. Require a non-author semantic disposition for every added observed group. Report per-file unparsed deltas. List both-error pairs verbatim.

### CR5 (medium): the resource guard misses the F1 remedy

- F1's remedy snapshots factory-time bindings, which is the retained-memory mechanism behind r20's harm.
- The frozen recipes are shallow assignment-only cells with no factories or closures.
- **Fix:** add a separately labelled recipe of N factory calls followed by N closure invocations at 1000/2000/4000, under the same caps. This is an addition, not a replacement.

### CR6 (medium): the denominator can be controlled after the fact

- **Undefined terms.** Neither "eligible" nor "declared supported forms" is enumerated, so a falsifier can be excluded post hoc.
- **F2 truth admits two outputs.** It allows "unparsed or lead", so either result could pass unless one is frozen.
- **oracle35+17 cannot detect F1–F3** (`FinalBindingReview.md:150`), so its green is a no-harm guard only.
- **Fix:** seal an eligibility rule, a supported-form list and an exact allowed-output set per fixture before implementation.

### CR7 (high): non-author closure is undefined

- W2 seats are author-lane advisers.
- "Main owns closure" collides with Main's r21 parent ruling and with its role as the claimed channel of the r22 authorization.
- The r21 precedent used CloseMado21, an orchestrator-dispatched non-author seat that re-ran fixtures in a scratch clone.
- **Fix:** an append-only clarification:
  - The closure seat has no r22 wave membership and is separate from whoever recorded the authorization.
  - Its minimum re-run set: the original six fixtures plus sealed variants, both comparator baselines with added-group dispositions, the resource addition, the C2 fixture triple, and the intervention and mutant receipts.
  - "Falsifying rejects" means re-examining every exclusion and every retained red output.

### CR8 (low): wording drift

- MANIFEST records r19 and r20 as `rejected-harmed`, not plain `rejected`.
- "Lowest axis" cites no current score or measured commit.

## What held up

- The registration commit `a963ce6` precedes any implementation.
- r21 C1=harmed and the 166/175 and 172/175 history are preserved.
- No criterion-count credit is claimed, and r19's precision failure is not retroactively admitted.
- C2's independence method mirrors the demonstrated r21 method.

## Tradeoff for the canonical judge

Even after the CR2 correction, the C2 green certifies that a translated snapshot's labels and counts are consistent. It does not certify r19 truth. It should be weighed as a capability, not a historical repair.

## Unknowns

- Whether an out-of-band operator authorization exists.
- Who wrote `rejected-harmed` into the r21 outcome file.
- The registration and contract digests were copied from `audit-authority.json`, not recomputed by this seat.

## Verification and tools

Only read-only reads and JSON parsing of committed receipts were done. No detector, comparator, harness or payload was run. No builds, tests or Git/jj mutations. Tools installed: none. The main agent should run, after seal: the CR2 fixture triple through the audit harness, both comparator baselines with stats deltas, and the CR5 resource addition.
