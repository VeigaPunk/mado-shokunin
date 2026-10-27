# OverlapScan — round 52

## Deliverables

- `.ufo/waves/round-52/w1/OverlapScan.md`

## Scope and axes

Axes: coverage and operability. This is a source-only cross-axis/overlap review of the frozen claims; no claims or predicates are changed. Round 52 targets C1 (bounded accountability checks in tool ledger) and C2 (proposition-bound dispatcher source entry).

## Findings

- C1 and C2 have distinct artifacts and acceptance predicates: C1 checks uniqueness, resolvable non-self evidence pointers, and instrument-context descriptions in an existing ledger; C2 requires a new indexed knowledge entry with proposition-to-source row/pin/quote/support mappings. Neither is a duplicate of the other.
- Round 51 exposed the direct C1 failure mode round 52 is intended to address: its literal basename-in-file pointer and non-empty description predicate passed generic descriptions and ledger-wide self-pointer patterns. Round-51 registration records the residual as bounded evidence, not proof of meaningful accountability. Thus C1 is a substantive repair, not duplicate scope.
- Round 51 C2 required source rows/quotes, indexing and lexical novelty, but its registration records source-truth overclaims found by independent review and append-only errata. Round 52's proposition-to-pin/quote/support mapping plus outside source-truth sampling is directionally complementary: mechanical binding is improved without pretending the counter proves entailment. This overlaps the sourced-dispatcher theme but strengthens a different assurance layer; do not describe it as semantic proof.
- Round 50 C1 was sourced coverage for bind-key matching, and its declared post-freeze residual includes recycled candidate novelty and omitted held mechanism facts. Round 50 C2 was session-material gate operability and disclosed counter/gate forgery residuals. These are different targets from round-52 C1 ledger accountability and round-52 C2 dispatcher propositions; no direct duplicate scope is evident. Round 50's gate was allowed live compositor receipt replay, whereas round 52 is explicitly source-only: do not import that runtime verification pattern.
- Potential *counter-contamination* boundary: C1 must demonstrate production ledger pass and specified generic-self-pointer control fail; C2 must use a separate target slug and prove the new entry absent at pinned base. A broad scan or shared success condition could accidentally let one artifact satisfy both. Keep counters and receipts scoped to claim, target artifact/control and revision.
- C1's explicit limit (“bounded accountability checks, not prose entailment”) is compatible with C2's external source-truth review. Do not treat C1's context-string check as proof of factual support, or C2's mechanical bindings as semantic entailment. Collapsing these would falsely inflate both axes.

## Affected axes and proposed bounded move

- **Operability:** isolate C1 counter targeting and control diagnosis so its production pass cannot be supplied by C2's new knowledge entry.
- **Coverage:** preserve C2 proposition mapping and independent truth review as distinct from C1's lexical context predicate.
- **Move:** Label every check/receipt by claim, target slug/path, pinned revision, and control; require C1's production pass + its specific control fail and C2's base absence + its own entry checks as separate evidence. This is a bounded verification/reporting separation and does not alter either frozen predicate.

## Risks and verification

Risk: over-separation can miss legitimate reuse of a source across artifacts; permit reuse only where each claim independently meets its frozen predicate. Risk: lexical context/mapping checks may appear stronger than they are; retain explicit semantic-proof limitation. No cross-axis harm is identified in the bounded separation move.

Verification remains in owning lanes: run C1's committed counter at the requested base revision against production and the specified control, with explicit red/green receipts; run C2's new counter against its distinct target slug and prove base absence, then obtain independent source-truth review. This seat did not run counters or truth checks.

## Evidence and limitations

- `.ufo/waves/round-52/claims-frozen.md` lines 5–13 and `registration.md` lines 7–15: frozen round-52 predicates, controls and source-only boundary (local repository evidence).
- `.ufo/waves/round-51/registration.md` lines 7–19, 27–31: C1 generic-description/self-pointer residuals; C2 source-truth correction; limits (local repository evidence).
- `.ufo/waves/round-51/w2/CritC1GenericDesc/generic-descriptions.md` lines 1–6: receipt reporting C1_R51 TARGET_MET with selftest and generic-description attack context (local repository evidence).
- `.ufo/waves/round-50/registration.md` lines 9–23, 32–49, 79–94: round-50 sourced bind-key coverage, session-material operability, and declared post-freeze residuals (local repository evidence).

No external source candidates or URLs were used. No package queries, live reads, probes, producer execution, or source checkout writes performed. No installs.

## Report

- `.ufo/waves/round-52/w1/OverlapScan.md`
