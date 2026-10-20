# R14History — accepted R14-V1 correction limits; why no replay and no preimage recovery

Seat `MadoR16.R14History` (scout), 2026-10-20. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, baseline
`32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.

Read-only. No gate, harness, selftest, measure, mutant, frozen replay, live,
package or service operation was run. Evidence is committed text plus static
git-object reads and `sha256sum` over bytes read in memory or in scratch;
scratch was removed. No tool installed or updated.

## Axes

This seat moves no scored axis. It preserves **calibration/quality** provenance
precision under QUALITY 7/9/13 and leaves coverage, operability, freshness,
depth and adjacency unchanged. The round-15 closure already recorded
operability as harmed by the unrelated host partial upgrade (M2); the R14-V1
correction neither repairs nor offsets that. Claiming coverage or operability
gain from this correction would be a category error: it is coverage-neutral and
adds no runtime proof.

## One-line answer

No replay is needed because R14-V1 is a **static identity/label correction**
whose acceptance predicates are checked entirely against committed bytes; a
replay would create a new, differently bound observation, not recover the old
one. No preimage is recoverable because the two provisional whole-gate digests
were taken over **uncommitted worktree bytes that were never objectified**, the
`/tmp` target was a lossy excision and is gone, and no blob in the object store
matches either digest.

## 1. What was routed, authored and accepted

| Step | Artifact | Anchor |
|---|---|---|
| Defect routed | provisional `input_binding`, old whole-gate hashes, no `measured_commit`; asks for appended mapping only | `corpus/lessons/round-14-verifier-spotcheck.md:169` |
| Lesson row | M1, class "standalone ancillary receipt precision / R14-V1" | `corpus/lessons/round-15.md:14` |
| Correction artifact | per-receipt mapping, cautions, forward-binding recommendation | `.ufo/waves/round-15/receipt-correction.json` |
| Standing-use erratum | append-only, historical bytes preserved | `corpus/knowledge/gate-standing-use.md` § "Erratum — round 15, R14-V1 ancillary mutation receipts" |
| Static red/green audit | exit 1 `receipt_mapping_missing` at baseline; exit 0 `receipt_mapping_verified`, mapped 3, problems `[]` at content | `.ufo/waves/round-15/evidence/receipt-correction-red.txt`, `receipt-correction-green.txt` |
| Quality application | existing criteria 7, 9, 13; no new criterion or wrapper | `corpus/QUALITY.md:62-70` |
| Scorecard/log record | static audit red/green; "No gate/mutant replay is claimed" | `SCORECARD.md:656-660`, `LOG.md:1146-1150` |
| Closure acceptance | correction accepted as landed; preimages unrecoverable; full-gate authority permanently withheld | `corpus/lessons/round-15-verifier-spotcheck.md:150-155, 277-281` |

The accepted acceptance test is narrow: "Append an explanatory correction
mapping each provisional header to its committed derived target; keep
historical bytes" (`:169`). It does not ask for a re-measurement.

## 2. Accepted correction limits

1. **Mapping only, no rewrite.** The three receipts and three TSVs keep their
   bytes. Committed digests: `d5462634…`, `267de2b5…`, `57c462c2…` (receipts);
   the three result TSVs are unchanged too. `git diff 32118fc…HEAD` for those
   six paths is empty.
2. **Two provisional whole-gate identities, not one.**
   `ef50e262…` (`regression-recut.txt:4`, 05:58:44Z) and `d6d5eb27…`
   (`regular-target-mutants.txt:4`, 06:00:23Z; `retained-census-mutants.txt:4`,
   06:01:00Z). Both are uncommitted worktree digests; neither maps to a commit,
   to `fba82a66…`, or to "the committed gate".
3. **Derived target is the only recovered identity.**
   `cd1d73d7…`, 117602 bytes, 2403 lines, equals each receipt's
   `MUTATE_TARGET`, `CONTROL` pristine digest and `MUTATE_RESTORE`
   before/after. It also equals `PIN_MADO` at `tools/mado-verify.sh:1639`.
4. **Derived-target equality authenticates retained bytes only.** The
   correction records that `PIN_MADO`, `SPEC_SHA`, `TABLE_MADO` and
   `HARNESS_SHA_RECORDED` "live inside the excised R7 regression span", so the
   117602-byte identity does not authenticate those constants.
5. **Not standalone final-full-gate receipts.** Standalone full-gate authority
   is permanently withheld (`round-15-verifier-spotcheck.md:279-281`).
6. **Counts are not interchangeable.** `267/267` is the derived target's
   control; `372/372` is the committed full gate's selftest
   (`gate-selftest.txt`). Neither substitutes for the other.
7. **Outcomes remain recorded, not re-executed.** 10/10, 4/4 and 8/8 KILLED
   are historical observations. Only the inputs were statically reproduced: the
   derived target, defect semantics and all 22 mutant byte digests
   (`receipt-correction.json.mutant_recomputation`).
8. **RT/P spec run-time bytes are not attested.** The receipts print path and
   defect count, not a spec sha; only defect semantics and mutant bytes bind.
   `regression-recut`'s spec body is recoverable from the committed heredoc and
   its sha equals the recorded `SPEC_SHA` (`c7ee75b9…`).
9. **Harness identity is split.** `75ed934d…` is the mutable sibling tool the
   receipts actually invoked; `b56c6e57…` is the gate's printed provenance
   constant, explicitly not the harness digest.
10. **Forward binding.** Future standalone mutation receipts bind
    `measured_commit`, derived-target sha, spec sha, harness sha and actual
    command/time/exit. "Never stamp a later full-gate measured commit onto a
    pre-commit mutation run" (`corpus/QUALITY.md:62-70`).

## 3. Why no replay is needed

The correction's truth conditions are static relations among committed bytes
and recorded strings:

- (a) receipt bytes preserved and equal to their recorded digests;
- (b) derived target = excision of the committed measured-commit gate;
- (c) each receipt's `MUTATE_TARGET`/control/restore equals that target;
- (d) each provisional header is truthfully labeled uncommitted and
  unrecoverable, with no `measured_commit` line and no full-gate relabel.

The red/green audit tests exactly (a)–(d) and reports
`"runtime_verdicts_reexecuted": false` (`receipt-correction-green.txt:41`).
None of (a)–(d) acquires information from executing the gate again.

A replay cannot perform the required act. It would produce a run bound to the
then-current executable, revision, spec, harness and time. Presented as the
05:58–06:01Z runs, that would be the prohibited relabel; presented honestly, it
is a **new** claim with a **new** receipt, still leaving the provisional
preimages absent and full-gate authority withheld. A replay against the derived
target would re-measure the 267-assertion control and recorded kills but would
not authenticate the whole gate or the excised constants.

The only commit-bound outcome observation is the round-14 frozen replay at
`2026-10-20T06:04:11Z`: gate `fba82a66…`, harness `75ed934d…`, target
`cd1d73d7…`, `10/10`, `MADO_REGRESSION: PASS`, `frozen_match`
(`.ufo/waves/round-14/evidence/frozen-regression.txt`). It is historical
evidence for unchanged bytes, not a fresh verdict for round 16; RT/P have no
commit-bound replay and none is claimed. Finally, the round-16 contract bars
seat check execution and reserves verification to L1.

**Replay would be needed only for a different claim:** "these KILLED outcomes
are true now at revision R with executable E." Nobody makes that claim, and
the accepted correction expressly excludes it.

## 4. Why the provisional preimages are unrecoverable

Define the missing object precisely: the whole-gate byte strings whose SHA-256
is `ef50e262…` and `d6d5eb27…`. This is not the derived target, the specs or
the mutants, several of which *are* recoverable.

1. **Never objectified.** The digests were computed over uncommitted worktree
   bytes. Receipts line 3 says `input_binding: provisional worktree snapshot`;
   no `measured_commit` appears. Runs at 05:58:44Z, 06:00:23Z and 06:01:00Z
   precede commit `32118fc…` at 06:03:28Z. Two different digests across the
   three runs show at least two transient gate states.
2. **Absent from the object store.** Neither digest is the sha256 of any blob.
   This seat scanned all **530** blobs currently reachable with
   `git cat-file --batch-all-objects`; earlier seats scanned 484 and 433 with
   the same negative result. None of the nine committed `tools/mado-verify.sh`
   revisions matches. Denominator drift is object-store growth; the absence
   result is constant.
3. **Absent from the execution path.** `/tmp/mado-r14-recut-0blumi29` does not
   exist now; the correction records `target.retained: false`. Even when it
   existed, that path held the **derived target**, not the whole gate.
4. **Excision is lossy and non-invertible.** The derived target is the committed
   gate minus four spans: R7 SELFTEST lines 440–619, R8 lines 1368–1531,
   R7 REGRESSION lines 1543–1983, R8 lines 1984–2506 — 1308 lines and 60247
   bytes removed (177849 → 117602). Many whole-gate variants whose removed
   spans differ but whose retained bytes agree excise to the same target. The
   removed spans contain the very constants that would distinguish variants,
   so target equality constrains only the retained 117602 bytes.
5. **Cryptographic irreversibility.** SHA-256 preimage resistance makes
   inversion from the digest infeasible, and the intermediate edit history is
   unrecorded, so there is no constrained candidate set to search.
6. **No independent hash chain.** The receipts record a digest and time, not
   the bytes. Even a later byte string that hashes to `ef50e262…` would be a
   candidate, not proof of the 05:58:44Z run-time object.

**What is recoverable:** the derived target (reproduced here as 117602 bytes,
2403 lines, `cd1d73d7…`); the `regression-recut` spec body from the committed
heredoc (`c7ee75b9…` = `SPEC_SHA`); the committed `regular-target.spec`
(`45f1fcd3…`) and round-13 `covering.spec` (`d7cc64ca…`); all 22 mutant byte
digests (reproduced by round-15 seats, not re-derived here); and the receipt
bytes themselves.

## 5. Static observations made by this seat

| Check | Result |
|---|---|
| `git show 32118fc…:tools/mado-verify.sh \| sha256sum` | `fba82a66…`, 177849 B, 3711 lines; worktree file identical |
| Exact `mado_r7_target_build` sed over that committed gate | `cd1d73d7…`, 117602 B, 2403 lines |
| Marker spans in committed gate | 440–619, 1368–1531, 1543–1983, 1984–2506 |
| All current blobs vs both provisional digests | 530 blobs, zero matches |
| Three receipt sha256 vs correction mapping | exact matches (`d5462634…`, `267de2b5…`, `57c462c2…`) |
| `git diff 32118fc…HEAD` on six historical files | empty |
| `/tmp/mado-r14-recut-0blumi29` | absent |
| Committed gate revisions | 9, latest `32118fc…` (content unchanged through baseline) |

I did **not** rerun the red/green audit, re-derive the 22 mutant digests,
execute any gate/harness/mutant, or probe live state. Those remain recorded
observations.

## 6. Confidence and remaining unknowns

- **High:** accepted limits and their anchors; receipt headers/times; committed
  gate digest/size; derived-target digest/size/line count; four excision spans;
  absence of either provisional digest from all current blobs; `/tmp` absence;
  historical receipt-byte identity since `32118fc…`.
- **Medium:** absolute non-existence of the provisional bytes anywhere outside
  this repository and its object store. The defensible claim, matching the
  correction, is "not retained or recoverable here"; a disk backup or an
  unrecorded copy is neither proven nor disproven.
- **[INFERENCE]:** that the `/tmp` target was produced by the gate's own
  `mado_r7_target_build` from the run-time worktree gate, and therefore that
  any difference between `ef50e262…`, `d6d5eb27…` and `fba82a66…` lies inside
  the excised spans. The receipts record the target digest, not the build
  command; the correction itself names the algorithm and the consequence, not
  a recorded invocation.
- **Unknown and retained:** the exact run-time whole-gate bytes and edit
  history; RT/P run-time spec comment bytes; `d6d5eb27…` line count (no record
  outside the two receipts); whether any non-repository copy exists.
- **Not claimed:** fresh verification of any KILLED outcome, standalone
  full-gate authority, coverage or operability movement, promotion, or host
  remediation.
