# Round 21 W2 — C1/C2 causal separation and corpus scope

## Axes and verdict

- **C1 — operability:** tripwire residual detection, retained-memory behavior, and whole-frozen-corpus no-loss. Its population is 52 accepted oracle cases, partitioned into 35 primary and 17 supplemental cases; these partitions do not have equal authorship independence.
- **C2 — calibration:** acquire one artifact-only assessment-integrity capability. It is not a historical lesson/criterion-count gain, not a C1 behavior result, and not outside-lane promotion authority.

**Verdict:** C2 is executable independently of the C1 tripwire *provided its own gate and fixture bundle are retained*. The current `--check` path has no C1 code/result dependency, and committed W2 probes of the exact current C2 source exercised that path without opening or running C1. No probe here actually reverted C1 or ran the current 20-case C2 selftest, so runtime invariance under an actual rollback is not claimed. A whole-tree reset to before C2 was introduced would of course remove the gate itself.

The scorecard should keep C1's 35/35 primary evidence distinct from the 17 supplemental guards, and keep C2 as one capability result. Do not turn 52 rows into 52 independent authors, 20 C2 cases into 20 criteria, or C2 artifact assertions into chronology/authorship proof.

## Exact code and frozen-input identity

Read-only inspection found repository `HEAD` `a8da015624c92f4cb4a7de92adbf6643a3f8b38a`; the production candidate is `f499a8db7171b7476fe9f204ab9edbac5a956fa9`. The tip adds records/documentation only relative to that candidate for the two tools examined here (`git diff --quiet f499a8d HEAD -- tools/mado-tripwire.py tools/mado-assessment.py` returned 0).

- Current `tools/mado-tripwire.py` SHA-256: `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`. The 2ac0f9b version was `7f41b0e8a7f194fddaece22ae9957bdedd15bf4b7de9a97cfcbdcf87683866ea`; f499a8d and current tip have the same new bytes.
- Current `tools/mado-assessment.py` SHA-256: `5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7`. This is also its hash at 2ac0f9b and f499a8d. The C2 code changed after 843d301 only in the selftest's expected-finding-ID checks; the current `--check` implementation was not changed by the later C1 tripwire commits.
- Frozen C1 `oracle/expected.json` SHA-256 is `fd2bfbc86897e1ee7a79302f6ccf6c3403709b132180864a0674f8212925576f`, matching `expected.sha256`. A read-only revision diff from the frozen `b96d1b8` seal through current HEAD showed no changes to the C1 expectations or C2 `seal.json` / `expected.json`.

The current f499a8d scanner bytes were inspected but not run by this seat. The current-candidate whole-corpus result is therefore not inferred from the older 2ac0f9b run.

## Registration, scorecard, and QUALITY scope

`registration.md` declares C1 as operability repair using the same independent truth cases, resource recipes, and frozen whole-corpus population before/after; the historical 175-case result remains unchanged. It declares C2 as a separate artifact-only assessment gate that reads no tripwire output and invokes no classifier, with a stated goal of remaining verifiable if C1 is reverted. The appended clarification makes C2 a capability acquisition (before capability absent), not an invented permissive historical baseline. It also says timestamps are artifact assertions, not independently authenticated chronology.

`SCORECARD.md` describes C1's score as `10 * matching new oracle cases / frozen new oracle cases`, and C2 as a separate calibration capability. The 52-case C1 denominator must be reported with its two provenance strata; otherwise the aggregate hides the fact that only 35 are primary independent proposals. `corpus/QUALITY.md` applies criteria 7/9/13/24 to bind frozen inputs and measured revisions, requires removal-side adjudication under criterion 30, and explicitly keeps the round-20 criterion-30-prime count coupled to C1. It cautions that C2 cannot prove no unrecorded earlier measurement occurred and that a 20-case selftest is not twenty criteria.

## Primary 35, supplemental 17, and rejected JjReadIwc

`oracle/assemble.py` assigns `primary` only when a proposal has both a surviving delivered `Oracle*.md` report and a proposal file; recovered/L1/late-source extras are `supplemental`. The sealed `expected.json` confirms 35 primary + 17 supplemental = 52 executable fixture rows. It separately retains one rejected proposal, `w1/oracles/JjReadIwc.json`, and does not put it into either denominator. The `primary_rule` also excludes dead seats. A cross-count of report/proposal membership agrees with the 35/17 split.

Observed committed C1 receipts are historical, not a final f499 result:

- At `b96d1b888a111971b430dc653f5826dc041b26bd`, `evidence/oracle-before.json` records primary 8/35 and supplemental 5/17.
- At `843d301d1b17af78427918f7845af336b2218de0`, `evidence/oracle-candidate.json` records primary 35/35 and supplemental 15/17; its two misses are `ClassTargetDormant` and `MethodcallerInvoke`. Later commits address those cases, but no current full C1 oracle/corpus run was performed here.
- LOG records the first whole-corpus replay at 2ac0f9b as 33 removed/relabelled groups, 77 added/relabelled groups, and 108 explicit error pairs; those findings motivated f499a8d. Per the parent handoff, the new candidate preserves reached protocol/callable forms. This does not establish the current whole-corpus verdict.

The rejected JjReadIwc proposal is retained with digest `407891e9842b08818b2f604f4429603a89c2e8ee57df1df3528f8f96d0e635a9`. Its proposed universal `vcs_write`/`observed` expectation for `jj --ignore-working-copy log` was rejected because index rebuild/repair is conditional, not an unconditional observed write. The rejection preserves the narrow no-working-copy-snapshot boundary; it does **not** generalize that to “no possible cache/index side effect.” Thus JjReadIwc is neither a clean case nor a supplemental scored case, and its proposal has not been silently rewritten to match a tool result.

## C2 independence and limits

Static source review of current `mado-assessment.py` (`5101c317…`) shows `--check` follows `main → evaluate → check` and reads the supplied assessment, declared population bytes, and C2 `expected.json`; it imports only the standard library and does not import or call `mado-tripwire.py`, consume a C1 counter/result, or execute transcript content. Its only `subprocess.run` is in the separate selftest branch, which invokes this same assessment gate on C2 fixtures. The sealed C2 bundle says its synthetic fixtures do not depend on current C1 classifier/counters/results. Current W2 `GateBaselineValid.md` reports the exact current C2 hash and an audit of `--check` opening only C2 source/assessment/snapshot/expectations, with no C1 execution. This supports source- and observed-path independence if only C1 is rolled back.

The committed `assessment-candidate.json` records 20/20 at `843d301`, exit 0, but embeds the earlier C2 tool hash `9d976face474379119da630f2963f6da1a482073327e6f3d4876fa8114937a98`; current code adds finding-ID assertions, so that receipt is not a current-hash full-selftest result. Current-hash W2 single-case probes exist. They do not replace the current full-selftest that L1 owns.

A concrete current-C2 limitation must remain explicit: `w2/reports/GateShonenXWithoutNonauthor.md` tested the current hash and found that an author-only `[x]` row ending in `non-author verifier: N/A` is accepted as `assessment_clean`; pristine and restored forms fail as expected. The lexical regex accepts the `N` prefix and does not validate an actual verifier or negate the preceding text. This is a surviving false negative in the neighboring artifact, not evidence of genuine independent assessment. It does not re-couple C2 to C1, but it limits any claim that C2 proves substantive or authentic SHONEN review. The gate itself disclaims authenticated chronology, authorship, semantic proof, and promotion authority.

## One bounded move

For L1's final round record, keep one **causal-partition receipt**: report C1 primary and supplemental outcomes separately (then the aggregate only as a convenience), report C2 as a single capability with its own current-hash cases, and preserve the `N/A` C2 false negative as unresolved rather than altering frozen expectations. This improves C2 calibration and keeps the C1 independence denominator honest without changing C1 code, fixtures, or the frozen target. It must not be represented as proof of real-world chronology or independent authorship.

**Verification/limits:** This seat performed read-only repository inspection, byte hashing, and comparisons; it ran no scanner, C2 tool, full suite, full corpus, or C1-revert simulation, installed no tools, and edited no production/frozen files. The current-candidate C1 whole-corpus verdict and current-hash 20-case C2 selftest remain for L1's final verification. Evidence paths above retain historical code hashes and outputs where applicable.

Report: .ufo/waves/round-21/w2/reports/CorpusIndependence.md
