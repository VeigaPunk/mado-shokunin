# R53One2 — adversarial review (critic)

Axes: **operability** (C1) and **coverage** (C2). Scope: falsify frozen predicates and their controls; r52 defects are evidence, not assumptions. No source URLs newly opened; all evidence below is lane-local, already available bytes.

## C1 — instrument-ledger accountability

**Attacked predicate:** frozen claims `claims-frozen.md:7`: scratch-aware counter distinguishes production ledger from no-work and each frozen forgery, with exact population coverage and non-self pointers; structural accountability only.

**Counterexample / risk:** Passing a no-work control and named, frozen forgeries is not equivalent to proving that *every possible* self-pointer laundering form is rejected. The r52 mutation evidence supplies a concrete counterexample family: `.ufo/waves/round-52/w2/Attack02.md` reports nine self-pointer spellings reaching `TARGET_MET`, including symlink-mode alias P09; `.ufo/waves/round-52/w2/Attack19/mut-selfptr-dot.md:12-15` defines the relevant check as stripping `:<line>`, requiring pointer path existence and basename occurrence in bytes. That predicate admits a path that names itself under a different spelling/alias if resolution/identity is not canonicalized. The frozen C1 wording says “non-self pointers” but does not operationally define identity (literal path, normalized path, inode, or revision path), nor demand an exhaustive adversarial alias control set. Thus a green finite control suite could demonstrate only the listed spellings, not the claimed general non-self property.

**Smallest safe correction:** Freeze the exact identity rule (repository-relative canonical path at pinned revision; reject any pointer resolving to the ledger itself, including symlink aliases) and make symlink/dot/`./`/`..`/absolute-path and alternate line-suffix cases explicit reject controls. Keep claim bounded to the tested finite shapes if exhaustive canonicalization is not implemented. Require reported population denominator to be independently derived at pinned revision, not supplied by ledger/counter output.

**Evidence/commands:** Read-only source inspection: `read` of `claims-frozen.md` lines 5–13; `read` of `Attack02`/`Attack19` receipts. Exact recorded output in r52 `Attack19/mut-selfptr-dot.md`: “landed counter … `TARGET_MET`” for its named mutant (the file itself documents the case); no new executable counter or source process was run in this critic seat.

## C2 — proposition-bound synthetic-dispatch entry

**Attacked predicate:** frozen claims `claims-frozen.md:11`: append-only repair of P16–P18 against opened pinned bytes, and frozen counter rejects old bytes / accepts corrected entry with quote-pin-proposition bindings; independent reviewer checks source truth.

**Counterexample:** Even a counter that binds each proposition identifier to a pin and a quote can accept a fabricated quote if it checks only that the quote text occurs somewhere in the pinned file, rather than in the cited proposition's relevant source span or as a complete statement. The r52 evidence is direct: `.ufo/waves/round-52/w2/Attack32/ev-integrated-mutants.txt` records integrated mutant B, fabricated quote, still `props=18 rows=4 indexed=1 failures=0 verdict=TARGET_MET`, exit 0. Mutant A also passes after shape correction, so fixing the table parser alone does not repair quote truth. This is a concrete counterexample to the proposition-bound admission mechanism, not a claim that the r53 candidate repeats the defect.

**Additional source-truth boundary:** r52 verifier spot-check `corpus/lessons/round-52-verifier-spotcheck.md:38-40` independently states P16 quote splicing, P17 attribution to sendshortcut although pin lies in sendkeystate, and P18 “inside the scan” although loop closed earlier. These are three distinct proposition/source bindings; exact quote presence alone cannot establish subject, control-flow scope, or non-spliced continuity.

**Smallest safe correction:** For each proposition, bind a locator interval in the pinned source and verify quote bytes as a contiguous excerpt within that interval; treat multi-clause propositions as separately cited clauses or explicitly mark the omitted gap. Counter acceptance remains structural and must be paired with the frozen independent source-truth review; do not relabel counter pass as entailment proof. Preserve old entry rejection and corrected entry acceptance as separate controls.

**Evidence/commands:** Read-only inspection of frozen claims, r52 spot-check lines 38–40, and Attack32 integrated-mutant receipt lines 6–9. Exact receipt: `C2_R52: props=18 rows=4 indexed=1 failures=0 verdict=TARGET_MET rev=364cdd343b7c73811dfb2125f327b1e1d753bd6c`; `exit=0`. No r53 counter execution was performed.

## R52 routed defects and judgment

The spot-check also routes missing per-row Gate records for S370–S373 and stale Changes prose (`corpus/lessons/round-52-verifier-spotcheck.md:69-74`); these are provenance/closure defects, not proof that r53's frozen C1/C2 controls fail. The C2 source-truth defects P16–P18 are directly relevant evidence. No admission or axis score is assigned here.

## Report trailer

Attacked predicates: C1 `claims-frozen.md:7`; C2 `claims-frozen.md:11`. Evidence paths are relative to `/home/vgpnk/Projects/shokunin/mado-shokunin` as cited above. Report path: `.ufo/waves/round-53/w1/R53One2.md`.
