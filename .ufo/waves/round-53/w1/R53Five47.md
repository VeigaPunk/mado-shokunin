# R53Five47 — adversarial review of frozen C1/C2

**Axes:** operability (C1), coverage (C2). Independent critic; no candidate implementation was executed and no source-code pin was newly opened. Historical routed failures below are controls/evidence, not assumed r53 outcomes.

## C1 — counterexamples to a green structural result

**Attacked predicate:** `.ufo/waves/round-53/claims-frozen.md:5-7` requires a newly committed scratch-aware counter, explicit selftest, production-ledger `TARGET_MET`, no-work and every frozen-forgery `TARGET_MISSED`, exact population coverage and non-self pointers. Scope expressly excludes semantic proof.

Strong counterexample: equal cardinality can conceal substitution. An attacker can remove one canonical instrument from the enumerated population and add a duplicate/alias row; `population == ledger_rows`, `uncovered == 0` and a nominally successful selftest may still be reported unless the population is independently derived and compared as identities (not only counts). Separately, basename containment can be satisfied by a pointer to an unrelated existing file, and symlink/dot-segment spellings can make a self-pointer appear non-self absent canonical resolution. These defeat accountability without claiming semantic proof is required.

Evidence is historical, not a new execution: `corpus/lessons/round-52-verifier-spotcheck.md:29-32,57` records an r51 `population=82 ledger_rows=82 ... selftest=ok TARGET_MET` on generic descriptions, plus nine self-pointer laundering forms (including symlink alias) passing. That report explicitly says these were reproduced predecessor attacks. No round-53 counter or fixture receipt was found by this seat, so current C1 is unproven rather than falsified.

**Smallest safe correction:** require identity-level set equality against an independently enumerated pinned-revision population, plus per-row pointer resolution and explicit canonical self-target rejection; make the selftest invoke every frozen control and assert both verdict and exit status. Keep the claim structural; do not infer description semantics from these checks.

## C2 — counterexamples to proposition binding

**Attacked predicate:** `.ufo/waves/round-53/claims-frozen.md:9-11` requires append-only repair of P16–P18 against opened pinned bytes, rejection of old and acceptance of corrected entry by a frozen counter with quote/pin/proposition bindings, independent source-truth review, and no expansion credit without an opened-this-round source row and uncovered ground.

A counter that validates only pin existence and quote presence can accept a fabricated quote attached to a real pin; one that checks quote text but not proposition identity can accept a subject swap; one that checks row existence but not full coverage can leave an unmapped proposition unnoticed. These produce a superficial green counter with false grounding or incomplete mapping. The routed r52 cases are concrete controls: P16's joined quote is not contiguous, P17's `sendshortcut` attribution points into `sendkeystate`, and P18's return is placed after the scan loop closes. The round-52 spot-check also records a counter grammar mismatch (`props=0 TARGET_MISSED`) and fabricated text at valid pins passing `TARGET_MET` (`corpus/lessons/round-52-verifier-spotcheck.md:38-40`).

These are local historical records; this critic did not reopen source pins or inspect/execute a round-53 correction. Therefore they do not prove a current repair is wrong or absent. They do show why binding must include proposition ID, source-row identity, immutable revision/file/line, and exact contiguous quote, with independent entailment review. Repair alone is not coverage expansion: require separate evidence of newly opened source row and uncovered proposition ground.

**Smallest safe correction:** freeze old bytes and isolated quote-splice, subject-swap, localization-shift and fabricated-quote negatives, alongside a corrected positive; require all controls plus independent source-truth review. Keep novelty/expansion adjudication separate from counter success.

## Evidence and limits

No source URL newly opened; no live reads, package queries, source fetch, producer execution, or candidate counter run. No install. No scratch directory/artifact was created. No claim pass/fail or axis movement is asserted.

### Report trailer
- Attacked predicate: C1 exact population/non-self-pointer accountability and executable selftest; C2 old/repaired proposition-grounded entry discrimination, independent truth review, and provenance-qualified coverage.
- Exact command/output: no target predicate command was run. Specialized local reads: `claims-frozen.md:5-11` (frozen contract) and `corpus/lessons/round-52-verifier-spotcheck.md:29-40,57,69-75` (historical counterexamples and routed defects). Disk guard: `df -P /fast/scratch/hyaku/mado-r53 /tmp` → `/fast` available 621749608 1K blocks (27% used); `/tmp` available 130075564 1K blocks (4% used).
- Source URL/date/located quote for newly opened source: none; no external or pinned source opened.
- Report: `.ufo/waves/round-53/w1/R53Five47.md
