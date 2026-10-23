# CritRegistration — round 27 w1

Read-only review of registration, both frozen counter sources, existing receipts, and the canonical claim-sizing rule. Only this report was written. No counter, control, suite, subject, harness, registration, or sealed held-out file was changed. No sealed held-out file was opened. This is criticism, not a judgment or an admission decision.

## Direct answers

| Question | Finding and evidence |
|---|---|
| Same C1 predicate sentence? | Yes between `registration.md:19-25` and `c1/count.py:5-11`, ignoring Markdown labeling and line wrapping. The receipt contains the same **identifier**, not the sentence: `evidence/c1-before-543f0445.txt:49` says `PRED-C1-r27 cases_pass=0/41 verdict=TARGET_MISSED`. The emitter is `c1/count.py:317-319`. |
| Same C2 predicate sentence? | Yes between `registration.md:36-43` and `c2/count.py:5-12`, on the same normalization. The receipt again contains the identifier and measurements, not the sentence: `evidence/c2-before-543f0445.txt:31`. The emitter and target condition are `c2/count.py:201-208`. |
| Does this satisfy canonical §9's identity rule? | The sentence/condition/label division is the division actually required by `../.ufo/prompts/mado-round-27.md:357-360`. Thus absent full prose in receipts is not itself a §9 violation. Both counter docstrings' parenthetical “same sentence ... receipt label” is literally too strong. There is, however, a C1 condition-versus-JSON-equality caveat below. |
| Is C1 named by its surface? | Yes: the new operation is deriving the ordered workspace-rule table from configuration, not merely obtaining 41 points. `registration.md:10-17` names the operation, output, version and unmoved command. Available prior notes mention the read verb, not an offline derivation (`corpus/knowledge/rule-attribution-r24.md:18-25,58`; `window-rule-effects-getprop.md:24-31`). The historical baseline receipt proves the proposed tool path is missing at the declared base (`evidence/c1-before-543f0445.txt:1-2`); it does not independently prove absence of every conceivable alternative at that revision. |
| Is C2 named by its surface? | Yes: operability of two lane gates over existing counters/checker, explicitly named at `registration.md:30-34`. It is not new Hyprland coverage. Whether its measurements establish behavioral gate effectiveness, rather than source-identity classification, is a separate construct risk below. |
| Causally separable? | Yes at the registered surface/dependency level. C1 extracts only the new tool and configuration into its tool sandbox (`c1/count.py:244-267,290-295`; `harness/oracle.py:231-239`). C2 targets three round-26 subjects and two quality suites (`c2/count.py:36-40,70-89`), not the workspace tool. Its old counters target `tools/mado-anims.py` and `tools/mado-binds.py` (`round-26/c1/count-v2.py:48`; `round-26/c2/count.py:31`). Either operation can therefore remain missing while the other is implemented. This is a dependency finding, not an executed causal ablation; actual suites can introduce additional dependencies and have not been reviewed here. |

Coverage is the appropriate name for C1's intended new operation, with an accuracy counter as its instrument, rather than re-scoring an operation already held. However, the observed source-blind bypass below shows that attaining 41/41 does not establish faithful source-graph handling. C2 is operability by changed surface, with a separate identity-classification risk. Neither label cures the instrument limitations. C1's “sourced” qualifier is also not verified by its counter: passing output comparisons cannot establish upstream-source provenance.

## Quantifier audit

- **C1's finite universal is enumerated.** `c1/count.py:262-267` constructs BASE + 25 APPEND + 15 SYNTH, `:290-314` scores every constructed case, and `:317` requires all 41. There is no stated universal over every legal Hyprland configuration or every seed. Reading 41/41 as such a universal would exceed the frozen predicate. The baseline receipt enumerates all 41 at `evidence/c1-before-543f0445.txt:7-47`.
- **C2's finite universals are enumerated.** `c2/count.py:177-182` creates two pristine runs and six one-subject benign-edit runs, then a run for every loaded W/H record. W's size and applicability are guarded at `:162-164`. `:201-207` requires 8/8 greens, 15/15 W kills, at least six valid H records, and `ceil(0.75 * h_valid)` H kills. No substitution of floor for ceiling was found.
- **The H denominator is applicable records, not distinct demonstrated bugs.** Validation checks subject/strings/different replacement/exactly-one old occurrence (`c2/count.py:97-115`). It does not establish uniqueness, behavioral harm, syntactic validity, or non-equivalence. Duplicate records can count separately; invalid records are reported and omitted (`:165-173,202-207`). This matches a narrow replacement-applicability definition of “valid,” but does not license “six independent bugs” or “all broken subjects.” No actual H contents were inspected.
- **“Sealed” is procedural provenance, not an enumerated counter check.** The counter reads every current `*.json` in the supplied directory and prints its current hash (`c2/count.py:166-171`). It does not compare those hashes against a committed pre-repair manifest. The registration supplies that external obligation at `:48-50`; a score alone cannot prove it occurred.
- **Do not confuse W-only control receipts with completion of the kill test.** With no H, `h_valid=0` necessarily misses the full C2 target even for an otherwise successful control. The registration correctly requires a post-seal H re-score (`:65-66`). The existing pilots' H=0 lines are not full C2 measurements.

Thus no unbounded “all configurations/all faults/all equivalent edits” clause is present in the formal PRED sentences. The broader heading “fail when their subject is broken” must remain bounded by the actual finite predicate, and sealing needs separate evidence.

## Counterexamples, impacted axes, smallest safe corrections

### 1. C1 reaches saturation without following configuration sources

**Counterexample:** the C1 critic's flat scanner walks every file in the four roots, ignores `source` directives, orders files using existing/root/six-letter-filename buckets, and resolves only the generator's `$ws...` variables in a global prepass. It therefore skips source-graph reachability, source order, and execution-time variable scope.

**Observed evidence:** `/fast/scratch/hyaku/mado-r27/crit/CritC1Counter-flat.py:14-31,35-43` shows that mechanism. Both existing receipts, `CritC1Counter-flat-seed1.txt:1-4,49-50` and `CritC1Counter-flat-seed2.txt:1-4,49-50` in the same directory, report the frozen counter hash `3d7d301fb9315f9a6cea2427db7c39e556482b30d3f4283373579ae665afd136`, override SHA `68339595f2a1ae6c0d41276c78852f81af7fb5ebc7b423f320a4d0f0c7abf1ea`, and `PRED-C1-r27 cases_pass=41/41 verdict=TARGET_MET`, `exit=0`. Seeds are `441b4edd8b45b26d` and `37705180291e18c5`. This seat read the artifacts; it did not run them. The generator's layout and variable conventions are visible at `c1/count.py:139-145,193-208`.

**Impacted axes:** coverage construct validity and the quality instrument's premature saturation. The intended surface is new, but this passing result does not demonstrate that the implementation follows the actual configuration tree. It is an override-control result, not evidence that the committed lane tool exists or passes.

**Smallest safe correction:** one unsourced file containing a workspace rule inside a scanned root would distinguish this scanner from Hyprland without a dangerous input. A future authorized counter could include that decoy instead of letting “all files” substitute for the source graph. The current rule is already frozen and scored: applicability of the declared control kill rule, redesign, or exploratory status belongs to the canonical judge. Do not silently patch the counter or advertise general source semantics from these 41 cases.

### 2. C2 can mistake source-identity discrimination for behavioral gate operability

**Counterexample:** normalize the counter's recognizable benign comment/assignment edits, then compare source hashes with pristine pins. Alternatively, ignore comments via AST parsing and remove only the recognizable inserted assignment before comparing ASTs. Neither needs to execute either counter or the population checker.

**Evidence:** `c2/count.py:118-124` generates only appended comments and an inserted `_benign_<8 hex digits> = <integer>` assignment. The actual unnormalized AST control passes the two pristine and three comment greens, kills all W, and fails only the three assignment greens: `controls/K2ASTPin-seed1.txt:8-31` records `green=5/8 w_killed=15/15 h_valid=0`. The SHA control independently records `green=2/8 w_killed=15/15` (`controls/K2ShaPin-seed1.txt:8-31`).

The C2 critic's pure-data diagnostic is stronger: `/fast/scratch/hyaku/mado-r27/crit/CritC2Counter-probe.txt:14,23` records `classifier=normalized-sha green_accepted=8/8 W_rejected=15/15 subjects_executed=0` on seeds `ea2ee13a11112617` and `7d9753ff553277c8`. Its `:24-28` separately demonstrates the loader accepting six comment-only equivalents, six syntax-broken rows, and eight copies of one effect; six synthetic code-change records are all rejected by the classifier. Crucially, `:30` states `NOT_A_CANONICAL_SCORE`: sealed H was unread, suites and counter main were not invoked. These diagnostics were read, not rerun by this seat.

**[INFERENCE]:** normalized pinning would also reject sealed H changes that remain different after normalization, but the actual H threshold and full TARGET_MET are unestablished. No full normalized-pin C2 score is present in the reviewed evidence. This is not an observed full-target kill-rule trigger.

**Impacted axes:** operability evidence and robustness of its quality instrument; not coverage or C1 independence. A bounded gate classifier can satisfy the literal measurement without establishing that its tests exercise subject behavior.

**Smallest safe correction:** keep reporting the exact finite gate-discrimination claim; do not promote it to general semantic gate effectiveness. If the canonical judge requires the latter, the benign-normalized pin is a concrete challenge for a properly authorized pre-data redesign/control, not permission for this critic to expand a control shape or change frozen criteria. The judge must distinguish that construct tradeoff from a demonstrated target-met receipt.

### 3. C1's executable equality is weaker than JSON value identity

**Counterexample:** replace a JSON boolean in an otherwise correct table with the corresponding number, or a numeric zero/one with a boolean.

**Evidence:** `harness/oracle.py:243-244` decodes tool output with `json.loads`; `c1/count.py:299-302` checks only the outer list type and then native Python `got == exp`. **[INFERENCE]:** nested `true` and `1`, or `false` and `0`, compare equal under those semantics despite being different JSON value kinds. The prose promises the same array values entry-by-entry (`registration.md:22-25`; `c1/count.py:13-14`). This is static language-semantics analysis, not an observed malformed-tool receipt; the dedicated C1 counter critic owns the runtime demonstration.

**Impacted axes:** quality of the C1 instrument and exact predicate/condition alignment. This does not turn the proposed new operation into a pre-existing one.

**Smallest safe correction:** a recursive JSON-kind-aware comparator that separates booleans from numbers. Since seats have already scored the frozen counter, such a change cannot silently retain the same r27 rule; canonical disposition is required. This report changes nothing.

### 4. Committed-input reconstruction and sealing are not established by a receipt label

**Counterexample:** keep REV and seed unchanged but change the configuration under the invoking HOME. `c1/count.py:259-267` rebuilds BASE and APPEND from that live HOME, not from REV. **[INFERENCE]:** the evaluated inputs can change while committed tool bytes remain identical. The counter later deletes its temporary tree (`:320-321`). A printed digest identifies an input but cannot recover its bytes.

**Evidence:** `harness/oracle.py:34-35,65-90` defines the four-root, size-filtered snapshot. Both existing baseline receipts happen to show the same 79-file digest (`evidence/c1-before-543f0445.txt:3-4`; `evidence/c1-before-543f0445-run2.txt:3-4`), which is evidence of those runs' input identity, not a recoverable committed snapshot. C2 similarly needs the external H seal procedure described above. This matters to canonical §9's “one command over committed bytes” requirement (`../.ufo/prompts/mado-round-27.md:343-345`).

**Impacted axes:** evidence provenance and reproducibility of the coverage/operability measurements, not causal overlap between the changed surfaces.

**Smallest safe correction:** retain the exact bounded snapshot input bytes/content-addressed artifact and recorded seed for replay; closure should identify that input rather than imply REV alone determines it. For H, retain the committed pre-repair hash manifest and compare it to every receipt's `HELDOUT_FILE` hash and eventual committed bytes. These are evidence obligations, not a license to retarget an already-frozen claim or to claim that a seal was violated. No actual seal violation was demonstrated here.

## Review record and safety

Static `read`, `grep`, and `glob` inspection only, plus two read-only coredump-count commands. Existing receipts and peer diagnostics above were read, not rerun. No build, test, counter, control, compositor, judgment runtime, or alternate implementation was invoked by this seat. No tool was installed or updated. No process tree remains from this seat.

Exact shell command, run for two safety observations during this review:

```sh
env -i PATH=/usr/bin timeout 30 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend /usr/bin/Hyprland | env -i PATH=/usr/bin timeout 30 prlimit --as=4000000000 --core=0 -- wc -l
```

Outputs: before `1338`; after `1338`; measured host Hyprland coredump delta between observations `0`. No Hyprland instance was started by this seat.
