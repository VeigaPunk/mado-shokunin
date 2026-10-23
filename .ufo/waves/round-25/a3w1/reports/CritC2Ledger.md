# CritC2Ledger — pre-data attack on the proposed current-state ledger

CRITIC C2: population 27; risks: omitted lowercase status rows, transcription without fresh execution, historical-revision substitution, partial-demonstration overclaim, stale or competing authorities.

The population is **27 substantive capability-table row occurrences representing 15 distinct capability names**. There is also one placeholder. Thus 15 is the full distinct-name population, but **not** the full literal row population in registration.md:68–70. The smallest correction is to keep 15 primary entries while explicitly reconciling all 12 repeated round-24 status rows; duplicate demonstrations need not be executed twice solely because their names recur.

This is an advisory review of the proposal, not a judgment or admission of C2. No proposed ledger or capability implementation was edited, and no capability demonstration, counter, compositor command, or other model runtime was invoked. Findings about earlier demonstration outcomes below are readings of committed evidence descriptions, not new execution receipts.

Axes at risk: **calibration** first (claims versus observed state), **freshness** (dated evidence and supersession), and **operability** (whether the claimed command and scope were actually exercised). A bookkeeping improvement must not become a claim of repaired behavior, an admitted capability, a score increase, or saturation.

## Evidence and exact commands

Read registration.md first, including C2 at lines 59–72 and the current Attempt 3 section. Read the round-24 non-author closure, especially §2.2 and §7.6. Independently opened the frozen scorecard with:

```text
timeout 30 git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 41cc04c8:SCORECARD.md
```

Repeated the read through a memory-capped subprocess for an in-memory Markdown-table census:

```text
timeout 30 prlimit --as=4000000000 git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 41cc04c8:SCORECARD.md
```

Observed census input and output:

```text
exit=0 bytes=146640 lines=1618 sha256=6b6995ff6998a405c2d4472463204b16e644829ad821a368922a65a60853ca08
markdown_tables=30
capability_tables=11 table_data_rows=28 placeholder_rows=1 substantive_row_occurrences=27 distinct_names=15
```

The Python Eval census excluded fenced code, recognized pipe-table headers by their following separator line, enumerated **all 30 headers**, and selected first cells equal to `capability` after whitespace trimming and case folding. It did not select sections by a `Capabilities` heading or import the previous counter's manifest. Raw output from the first command is available in this session as artifact://6286; durable evidence here is the frozen blob identity and located census below.

All scorecard line references in this report mean **41cc04c8d593837a0d5078bffaacdaa163d12897:SCORECARD.md**, not mutable working-tree line numbers.

## Independent population enumeration

| Header line | Heading | Data rows | Treatment |
|---|---|---|---|
| 202 | Capabilities | 204 | `— none yet —`: placeholder, not a capability |
| 306 | Capabilities (round 12) | 308–311 | Four repertoire rows |
| 435 | Sources and demonstrated repertoire | 437–438 | Two repertoire rows; third header cell is `Demonstrated evidence`, not `Evidence pointer` |
| 780 | Demonstrated capability | 782 | One repertoire row |
| 917 | Capabilities (round 17) | 919 | One repertoire row |
| 1018 | Capabilities (round 18) | 1020 | One repertoire row |
| 1156 | Capabilities (round 19) | 1158 | One repertoire row |
| 1340 | Capabilities (round 20) | 1342–1343 | Two repertoire rows |
| 1407 | Capabilities (round 20, attempt 2; append-only) | 1409–1410 | Two repertoire rows |
| 1462 | Capabilities demonstrated this round | 1464 | One repertoire row |
| **1573** | **Capability status (round 24 re-demonstration)** | **1575–1586** | **Twelve repeated capability rows; lowercase header `\| capability \| status \| observed evidence \|`** |

The last table is the strongest population counterexample. A case-sensitive search for `| Capability |` finds the 15 original substantive rows but misses twelve later present-tense statements. A heading-only search also misses the three already known repertoire rows at 437, 438, and 782.

Here are all 15 identities, with every repeated status occurrence mapped rather than silently discarded:

| Original row | Capability | Stated capability, abbreviated | Round-24 status row |
|---|---|---|---|
| 308 | sources registry | Curate opened, scoped sources; run census and join mined rows to citing entries | 1575 |
| 309 | verdict gate (live + file plane) | Read-only verdict across declared config and live hyprctl surfaces; exit 0/1/2 and boundary check | 1576 |
| 310 | hermetic self-test | 269 assertions over isolated fixtures | 1577 |
| 311 | mutation regression with re-cut | Replay ten-defect kill table; report moved-target setup and support re-cut | 1578 |
| 437 | source-fragment collision screen | Detect repeated active canonical URLs while preserving rejected history and valid supersedes links | — |
| 438 | digest-pinned frozen regression | Verify gate/harness digests before regression, refusing tampering | — |
| 782 | finite declared-action classifier | Refuse specified declared kinds/names and malformed inputs; compare pinned plan replay | — |
| 919 | post-hoc transcript tripwire | Classify supported OMP command surfaces into named classes, with exit 0/1/2 | 1579 |
| 1020 | tripwire frozen replay (gate entry) | Verify incident-line digests and report match/mismatch/setup-or-tamper outcomes | 1580 |
| 1158 | landedness check | Classify cited hashes against the live remote tip without fetching or writing | 1581 |
| 1342 | tripwire evidence marker | Distinguish observed commands from leads and drop provably pure data | 1582 |
| 1343 | harness fail-closed check | Check payload reachability after six forced setup failures | 1583 |
| 1409 | tripwire reached-body sweep | Report every visible reached but unfollowed body as a lead instead of dropping it | 1584 |
| 1410 | detector removal-side guard | Count older findings lost, crash flips, and pure-data rows over frozen adversarial inputs | 1585 |
| 1464 | artifact-only assessment integrity | Check declared chronology, hashes, rejection disclosure, and four SHONEN subjects without C1 dependency | 1586 |

The other 19 tables are move, axis, or claim/result tables, not additional repertoire/status tables. Their prose still matters to supersession. For example, the round-22 evidence-audit claim at 1493 is under `| Claim / axis |`; 1503 explicitly distinguishes demonstrated availability from admitted repertoire credit, and 1509 says no admitted capability row is added. It is not a sixteenth repertoire identity under this assignment. Similarly, claim-result restatements are not new capability identities. The correction should resolve repeated statements, not broaden the assignment to every capability-like sentence.

## Counterexamples, impacted axes, and smallest safe corrections

### 1. A complete-looking 15-row ledger can omit existing authorities

**Counterexample:** append the 15 requested names, each with a new status, but leave 1575–1586 out of the coverage/supersession mapping. The artifact can call itself complete while twelve earlier status statements remain unexplained. At 1568–1570, the old table explicitly says it supersedes the implied `works` of every earlier row. Adding another unqualified authority repeats the problem rather than resolving it.

**Evidence:** census above; 1573–1586; registration.md:68–70. The round-24 closure §2.2 already explains why section-title filtering was insufficient.

**Axes:** calibration, freshness.

**Smallest safe correction:** label the 15 entries as distinct identities, attach all 27 substantive base-row locations to them, and explicitly supersede/reconcile the 12 old status entries. Retain the placeholder as an explained exclusion. No extra twelve executions are necessary merely to cover duplicate names.

### 2. Copying fifteen plausible outputs is still transcription

**Counterexample:** copy the twelve round-24 status cells plus the three outcomes in its scope correction at 1588–1596; relabel the resulting table `Current state (round 25)`. That supplies all fifteen names and plausible results with **zero** new demonstration runs. Even an accurate copy would not establish the registered fresh base re-run or fresh provenance.

**Evidence:** the old table and correction already supply these outcomes. The round-24 closure §2.2:98–115 records that agreement with the old counter's observed column was guaranteed by construction.

**Axes:** calibration, freshness.

**Smallest safe correction:** retain a fresh, revision-bound execution receipt for each demonstration, including exact invocation, working directory, actual target/input revision, stdout/stderr, exit code, and limitations. The ledger must derive its observations from those executions, not from an expected-output column or a successful old receipt. Matching an old result is allowed; pretending that copying it is a re-run is not.

### 3. Running from a base clone does not prove that base code ran

**Counterexample:** execute the literal evidence commands at 1342 and 1409 from a clone checked out at 41cc04c8. They explicitly name **28c6837** and **a8960de**, respectively. A successful run can therefore demonstrate historical tool bytes rather than the claimed current base state.

**Evidence:** row 1342 names `tw-precision.py 28c6837` and `tw-recall-split.py 28c6837`; row 1409 names `a2-guards.py a8960de --fixtures-rev 6a7d9ca`. The later status at 1582 distinguishes the old L 17/18 from the then-current L 15/18.

**Axes:** calibration, operability, freshness.

**Smallest safe correction:** preserve the literal historical command as historical, separately record the documented base-targeted form, and bind actual loaded tool bytes to 41cc04c8. Keep intentionally frozen fixture revisions frozen; do not substitute all revision arguments indiscriminately. A base working directory is not sufficient provenance.

### 4. A partial demonstration cannot inherit the whole row's scope

**Counterexample:** rerun `--no-live`, obtain a verdict, and label row 309's **live + file plane** capability fully re-demonstrated. The old status row already makes exactly the important limitation visible: 1576 says the live layer was not exercised. Likewise, one green fixture suite cannot establish row 1409's universal “every visible body” wording.

**Evidence:** 309 versus 1576; 1409 versus the retained residual failures at 1412–1424. Row 311 also includes re-cut behavior, not merely a frozen replay. Row 1464 expressly excludes identity authentication and evidence sufficiency.

**Axes:** calibration, operability.

**Smallest safe correction:** keep the original stated claim intact and state the exact demonstrated subset and unexercised remainder in the observation cell. Record every relevant component command, or mark the missing component not demonstrated/not runnable. Do not widen the work to repair capabilities just to obtain `works`.

### 5. Exit status and capability status are not interchangeable

**Counterexample A:** row 437's selftest passes, so label its “current exits 0” assertion current. But 1592–1595 records a registry collision result, exit 1, while the selftest still passes 25/25. The stale clean-registry assertion and the collision detector's ability to report a collision are different propositions.

**Counterexample B:** mark row 1020's replay broken solely because it exits 1. Its contract explicitly assigns 1 to mismatch; 1580 says the replay runs and reports `frozen_verdict_mismatch` rather than failing to execute.

**Evidence:** 437, 1020, 1580, 1592–1595. These are prior recorded observations, not independently rerun here.

**Axes:** calibration, operability.

**Smallest safe correction:** report the raw outcome and distinguish (a) command executed correctly, (b) asserted condition holds/fails, and (c) setup/could-not-evaluate. A single `works/fails` token may remain if its object is unambiguous in the same cell; do not equate exit 0 with truth or exit 1 with a broken diagnostic. Changed historical assertion totals likewise require explanation, not automatic failure or success of the entire original claim.

### 6. A green sample cannot erase a rejection or restore an authority

**Counterexample:** a fresh guard run returns zero lost findings, and the ledger presents row 1409 as a generally restored, admitted capability. Yet 1412–1433 retains the round-20 harmed disposition despite passing fixed-population checks. Similarly, 1472 explicitly says the working round-21 assessment demonstration is **not an admitted capability or rank from a rejected round**.

**Evidence:** 1409–1433 and 1464–1474; the round-22 withdrawal at 1501 and the round-23 withdrawal at 1548–1557 are additional reasons not to infer production identity from an intermediate candidate's result.

**Axes:** calibration; freshness and operability if capability scope is misrepresented.

**Smallest safe correction:** keep operational observation, finite demonstration scope, residual defects, and historical admission disposition separate. Point to the governing withdrawal/rejection even when the present command succeeds. C2 cannot grant a new rank, erase H2, or adjudicate the strict-boundary tradeoff by changing a label.

### 7. Bare line numbers and relative receipt paths can silently change referents

**Counterexample:** write `SCORECARD.md:1342` as though it were a current-tree pointer after in-section stale-row pointers have been inserted. Or copy `evidence/...` from an old section into the new ledger without its round-qualified base directory. A syntactically present pointer is not necessarily the intended evidence.

**Evidence:** the registration plans section-local stale-row pointers (R6); the scorecard explicitly defines the round-13 short paths under `.ufo/waves/round-13/` at 440–442. The round-24 closure §2.2:111 identifies the missing at-row pointer as a distinct defect.

**Axes:** freshness, calibration, operability of the review instructions.

**Smallest safe correction:** qualify original locations by the full frozen base revision and capability name; use fully resolved repository-relative receipt paths with their containing revision. Provide navigation from stale sections to the new ledger and from the ledger to original statements and superseding dispositions. Reconcile the round-24 table too, rather than leaving it an independent current authority.

## Non-author acceptance test

This is a human evidence review, **not a replacement counter or a new numeric target**. A reviewer who did not author the artifact should apply the following test to the delivered revision:

1. **Independently recover the population.** Open the frozen base blob, inspect every table header without a case-sensitive `Capability` or heading-name restriction, and reproduce the 15 identities / 27 substantive occurrences / one excluded placeholder distinction. Verify that all 27 occurrences are accounted for, either as primary entries or explicit superseded aliases. Do not accept the author's list or an old manifest as the authority for completeness.
2. **Reconstruct and reproduce each demonstration.** In a detached 41cc04c8 sandbox, with Git directory/worktree/index overrides unset, independently reproduce the documented base-targeted demonstrations under the assignment's timeout, memory, read-only-host, and cleanup bounds. Resolve placeholders and nearest documented forms explicitly. Check actual tool/fixture bytes and external dependencies rather than trusting the checkout label. A single fresh guard receipt may serve 1409 and 1410 only if it actually demonstrates both stated observations. Preserve setup failures and unavailable dependencies; do not replace them with old green receipts.
3. **Audit receipt provenance and scope.** Every primary entry must resolve to a fresh execution receipt at the claimed base, exact command and inputs, raw output, and exit code. Distinguish executed-but-negative from could-not-evaluate. Check every component of compound evidence or state exactly which part was not exercised. Record time and observed remote tip for live-remote-dependent landedness; do not imply those external observations are permanently pinned by the local base commit.
4. **Apply the strongest local falsifiers.** Try to justify 437 using only its selftest, 309 using only `--no-live`, 1342 using the historical 28c6837 argument, 1020 using only a nonzero-exit rule, and 1409 using only a zero guard count. The ledger must make each mistaken inference visibly invalid, while preserving what the actual run did demonstrate. Also check that replacing a fresh receipt with an old one would be detectable from the recorded provenance.
5. **Resolve authority and navigation.** Follow every original-to-current and current-to-evidence/superseding pointer. Explicitly reconcile 1575–1586 and the old table's supersession sentence. Preserve rejected rounds, withdrawn candidate identities, known residuals, and available-but-not-admitted distinctions. No score, capability acquisition, saturation, promotion, or repaired-behavior credit may be inferred from this bookkeeping artifact.
6. **Make the qualitative comparison.** Using the prior state and delivered artifact, answer the same questions: what was claimed, what bytes and inputs were actually run at base, what happened, what remains unknown, and which statement now governs? Name a concrete improvement in answering those questions, beyond having copied the old status table or changing its denominator. A named non-author's reasoned `unprovable-but-better` finding is required by the registration; without that finding, C2 remains `unprovable`. This pre-data critique supplies no such final finding.

The population ambiguity, missing fresh receipts, and broken pointers are fixable defects. A ledger that instead obtains a nicer status by dropping red cases, collapsing setup failure into success, discarding rejection authority, or promoting a finite demonstration to a universal capability makes a substantive epistemic tradeoff. A later canonical judge should not accept that tradeoff as the claimed improvement merely because all 15 names appear.

## Scope and tool record

Only this report was written. No lane Git/JJ writes, sandbox clones, package installs/updates, persistent processes, host configuration changes, or capability tests were performed. Static census/read commands completed; unrun demonstrations have not passed. No tool installation record is needed because none occurred.
