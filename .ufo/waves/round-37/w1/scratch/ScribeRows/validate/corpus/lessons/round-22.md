author: mado

# Round 22 attempt 1 — authorized recovery, not restored admission

Base master741122d177ae8ff68a73768777f20484d5bdcbe4; registration a963ce67e303db94201507a93018416e4e44fd23. Full claim contract `.ufo/waves/round-22/registration.md`; motivating LOG entry `2026-10-21 — round22: explicitly authorized recovery registration`. Operator authorization permits this round only; all r19/r20/r21 rejection receipts and the old streak remain until non-author admitted closure. Never start r23.

## Mistakes

| id | class | evidence pointer | captured-by | fix / demonstrated boundary |
|---|---|---|---|---|
| M1 | survivor | `.ufo/waves/round-21/residual/FinalBindingReview.md` F1/F2: factory arguments rebound at invocation; unknown captures borrow module globals | QUALITY32, added after r21 falsification and not retrospectively satisfied | Freeze stored/cross-cell/unknown captures independently before implementation; creation-time lexical capture must coexist with late-bound globals. Actual red/green receipts, not this plan, determine repair. Original reds retained, not rerun merely to confirm user-reported failures. |
| M2 | reference-drift | same review F3: returned function selected from def rather than post-prefix binding | QUALITY32 callable identity | Independent returned aliases/rebinding variants and exact rows; no expectation rewrite after seeing output. |
| M3 | survivor | same review F4/F5: direct Thread.run/Timer.run silent; legal source identifier collides with synthetic state | QUALITY32 scope/identity; supported-form evidence requirement | Independent inline/stored/aliased/direct-run and legal-name collision variants; synthetic metadata must not enter source binding namespace. |
| M4 | scope | `round-19-verifier-spotcheck.md:63-81`: six incident detections do not prove precision; markerless RuleB turns pure frozenset data into ordinary finding | QUALITY30; existing no-trade rule | Preserve actual precision counterexample and label distinction. Separate artifact audit can check count/evidence assertions, not establish semantic precision, authenticate markers or retrospectively admit r19. A5-observed/1-lead translation is explicitly a later interpretation, not unchanged markerless r19 output. |
| M5 | landing | `.ufo/waves/round-22/w1-record.json`: validator refused absolute --registry with invalid_registry_path | swarm registry relative-path contract | Corrected same identity assignment with lane-relative registry, `w1-record-success.json`; no spawn repeated. |

## Gate

Declared C1 bounded static source-shape repair and C2 independent evidence-tier/count audit. No exploratory or criterion-count claim. The lowest measured non-retired axis is calibration; C2 is a capability, with genuine absent before-state `evidence/audit-before-absence.json` rather than a fabricated permissive implementation.

Initial census command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` exited0. Exact start output and branch pin are in `.ufo/waves/round-22/evidence/sources-start.txt`; warnings S030/S042/S045/S097/S119/S120 duplicate URLs are retained. Source rows are not written before opening. Existing immutable source fields and prior corpus lessons remain unchanged.

Reject: “a finite green suite or operator dispatch permission restores admission.” Flip: all declared measured targets and no-harm evidence, followed by genuinely independent non-author falsification, including at least one admit and one reject. Author-lane advisers cannot grant this. Current outside-lane spot-check is pending and not pre-claimed.

Wave1 consists of64 independently specified work items, not64 claim admissions. L1 holds planner seat. Sources, proposals and harnesses are authored without production edits, detector measurements or fixture execution; failed deliveries remain uncredited, never replaced.

### Opened source decisions (2026-10-21)

- GATE S121 — https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst ; accessed2026-10-21; located quote `Doc/reference/executionmodel.rst:322`: “Name resolution of free variables occurs at runtime, not at compile time.” (12 whitespace words). Tag peel8e6e75d9 and raw SHA11f99f83…eb89 are retained in `w1/sources/SourceClosure/`; enclosing-scope rule is at113–114. Admit the finite lexical/global distinction, not complete Python semantics. S121 enters A/mined, used-by this lesson, on-release recheck; no pre-existing immutable row changed.
- GATE S122 — https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/threading.py ; accessed2026-10-21; located quote `Lib/threading.py:1023-1024`: “if self._target is not None: self._target(*self._args, **self._kwargs)” (6 whitespace words). At1383–1385: “self.finished.wait(self.interval) if not self.finished.is_set(): self.function(*self.args, **self.kwargs)” (7 whitespace words). Raw SHA53239096…b7e3 and receipts retained in `w1/sources/SourceThread/`. Admit direct standard Thread target invocation and conditional Timer behavior only; subclass override, cancellation, repeated run and shared mutable argument changes remain separate boundaries. S122 enters A/mined, used-by this lesson, on-release recheck.

Independent schema/source review caught a representation gap before implementation: r19's actual raw scan has11 markerless finding rows across6 incident lines. The six-line5/1 reading is a later source-derived interpretation, not the unchanged r19 row population. The old raw artifact must remain could-not-evaluate under an explicit-marker audit; any6-line projection is explicitly derived. Main agreed in-session that could-not-evaluate stays labeled, projections never retrospectively admit r19, and non-author closure grades what is actually demonstrated. This does not silently replace the literal registered unchanged-row target with a fabricated green.

Pre-implementation audit clarifications, including count grain, validation order, missing markers and raw-byte fixture coverage, are retained in `audit-clarifications.md`. All original independent proposals and normalization reasons remain visible; no verdict was selected from candidate output.

Quote-count correction (append-only): the S122 Thread quote above has7 whitespace words and Timer quote has6, not6/7. The exact quoted bytes and locations are unchanged; both remain≤25. Counting receipt `evidence/source-quote-counts.json` uses `len(quote.split())`.

Pre-seal scope work is retained in `supported-forms.md` and `guard-clarifications.md`: exact finite forms, true unknown versus definite invalid-call outcomes, every-tier borrowed-command exclusions, no source-identifier sentinel, no-worse historical166/175 guard, added-row and per-file unparsed review, actual delivered-r21 baseline for1356-fixture replay and new finite closure-heavy resource guard. The original C3 raw-row target remains explicitly limited, not relabelled green. Additional truth cases precede implementation; author typos or omitted assigned alias/global contrasts receive retained originals and new corrected proposals before sealing, never a result-driven denominator swap.

### Authorship and provider corrections

| id | class | evidence pointer | captured-by | fix / demonstrated boundary |
|---|---|---|---|---|
| M6 | scope | `w1-spec.json` assigned three executor-owned new harness paths in the shared checkout; `evidence/{audit,oracle}-assemble-shared-draft.py` retain unfinished drafts | campaign hard rule requiring actual separate worktrees for concurrent code writers | Stop overlapping harness drafting; resume the SAME living identities in distinct sparse Git clones/unique branches with observed bases (`implementation-trees.json`, `oracle-isolation.json`). Main alone integrates. No retroactive isolation or collision-absence claim; this is conformance debt, not silently repaired history. |
| M7 | attribution | pre-seal `CaptureNestedFactory.json` wanted r22-inner while its literal source passed r22-nest-inner; two assigned alias/global contrast seats initially supplied a different valid form | independent source-to-expectation inspection, before any detector result | Keep original typo as rejected; corrected same-source proposal selected before seal. Keep the two valid initial variants and additional actual-alias/late-global cases. All decisions and raw source digests are sealed, not selected after measurement. |
| M8 | provider | `implementation-native-result.json` identities RepairBindings and ImplementEvidenceAudit; both failed with Codex capacity turn_rate_limit_exceeded before delivery | no-dead-seat-replacement campaign rule | No replacement. Main acknowledged coordinator-direct reachable implementation; retain exact deaths and count both seats. Original living harness authors continue only their own isolated artifact work. |

Raw independent truth and input digests landed `9185f1f9806b823a23ef9f5077a893e40e46e1b9` before production implementation:106 input rows,52 C1 raw proposal files and35 independent C2 proposal files, plus originals/contracts/resource recipes (`truth-seal.json`; counts are lengths of its file list and the named directory subsets). Normalized expected.json/JSONL materialization happens later from that raw seal; its later hash is NOT falsely described as already committed. The C1 author typo/addendum decisions and inclusive2MiB audit limit are frozen in this pre-implementation seal.

S121/S122 used-by old→new: `corpus/lessons/round-22.md` → `corpus/lessons/round-22.md, corpus/knowledge/tripwire-lifetime-recovery-r22.md`; status mined→mined and recheck on-release→on-release are unchanged. The new sourced note holds documentary distinctions, not a pre-claimed detector pass or a new desktop frontier admission.

Unless a full repo-relative prefix is given, the abbreviated `w1/`, `evidence/`, specification and seal pointers in this lesson resolve under `.ufo/waves/round-22/`. Both original provider-dead production tasks returned the exact text: `[openai-codex/gpt-6-luna] Retry budget exhausted after 5 retries: Codex error event: Codex is at capacity, please try again later (code=turn_rate_limit_exceeded)`. No dead identity was resumed or replaced.

### Fresh falsification is stronger than a green finite denominator

| id | class | evidence pointer | captured-by | fix / demonstrated boundary |
|---|---|---|---|---|
| M9 | scope | `w2/reports/NoHarmBoundary.md`, exact independently authored truth and raw scan in `w2/receipts/NoHarmBoundary/`: module helper returned from a factory acquires an unrelated factory parameter as observed argv | QUALITY32 lexical scope/identity, not the thin57-case denominator | Candidate71228fd remains falsified. Preserve its actual wrong observed row and true module-global want; freeze the discovered case and static neighbouring call-argument/callable/forwarded-frame guards in `residual-truth/expected.json` before any patch. A repair must distinguish callable lexical ownership and evaluate invocation arguments in the caller before installing a callee frame. No claimed green until actual later evidence. |
| M10 | attribution | W2 FalsifyC233–236: inherited six-row rationale on three D1 row-level cases, and four duplicate historical case pairs | criteria10/24 provenance/count grain | Append `audit/rationale-and-duplicates-correction.json`; do not alter frozen bytes/wants/seals. Report46 named cases beside42 distinct pinned case trees, not46 independent semantic classes. Original wrong prose remains named and corrected. |
| M11 | scope | W2 FalsifyC228 reports an additional absolute/relative same-case audit replay; FalsifyC227 reports a timeout-wrapper sleep control; FalsifyC144 reports an initial failed time wrapper before Python | one-assigned-measurement seat boundary | Retain actual receipts, do not claim every seat made exactly one process invocation. These are disclosed read-only scope deviations, not host mutation or semantic coverage gains; no seat or observation is replaced. |

The initial57/57 does not grant C1 admission: the fresh module-helper counterexample is inside the declared forms. No production patch is applied while other W2 readers hold the71228fd identity. The original primary50/supplemental7 denominators and all old red receipts stay unchanged; additional discovery guards are supplemental, not a result-driven target rewrite.

### Replacement coordinator final disposition

No operator wrap-up is in force; withdrawal is correctness-driven, not forced by a deadline. The eight-line v3 consumer suppression was removed, restoring exact v2 classifier bytescd9da20c. Primary57/57 and old35/35+17/17 hold, but supplemental2/4 remains red and `residual/ResidualForward.md` retains source-supported caller-local leakage and escaping callback-store risk. Strict C1 and the unchanged-row historical C2 target are unprovable/not admitted; an internally consistent46-case audit does not rewrite either target.

| id | class | evidence pointer | captured-by | fix / demonstrated boundary |
|---|---|---|---|---|
| M12 | scope | `residual/ResidualForward.md:17-24`, v3 commit4d308e5 | criteria30/32; callback reference escaping via container/attribute stores is not a consumed safe value | Withdraw only the unsafe v3 suppression; preserve v2's concrete returned-callable ownership and caller-argument fixes, every failed supplemental/v3 receipt and the unresolved caller-frame defect. Withdrawal is not a general repair. |
| M13 | attribution | `evidence/resume/corpus.json`, `corpus-delivered-r21.json`, `corpus-adjudication.json` | frozen actual-delivered-r21 baseline and one-child-per-seat contract | First replay used the older pre-r21 scanner and overlapped the correct comparator/primary oracle; retain it as excluded, disclose overlap. Actual no-harm uses baseline46c82902. All later resource/mutation/supplemental probes are sequential. No timing claim uses the overlapping runs. |
| M14 | landing | `evidence/resume/inherited-worktrees-inventory.json` | round-end clean-lane and no-discarded-evidence requirements | Byte-verify archive of all22 sparse-clone source files, record each branch/base/status, remove obsolete clones. Exclude only their Git administration and generated bytecode; no round evidence silently omitted. |

C2's actual snapshot-digest comparison is independently disabled in a retained mutant file. The unchanged self-invocation rejects that code fault (44/46, exit1; AuditRawDigestTamper and AuditRawTamperMalformed), while production remains46/46 (`evidence/resume/audit-digest-mutant{.py,.json}`, `audit-final.json`). This demonstrates a criterion able to fail without changing any expected verdict.

Inherited spending170 seats, five dead/unreported: RepairBindings, ImplementEvidenceAudit (capacity error already quoted above); ResidualOwner, ResidualCaller, ResidualCallable (zero-byte reports, terminal `Request was aborted`). Partial artifacts remain evidence, not completed advice. ResidualForward completed; its session output is retained beside its lane report. Four fresh3-seat advisory requests hit `Background job limit reached (100)`, zero spawned and no dead seat replacement. No additional repair or admission proposal follows.

End census command unchanged, exit0, exact output `evidence/resume/sources-end.json`:120→122 rows, tierA113→115/B1/C6; mined103→105/queued8/rejected9. Only S121/S122 were added; their used-by changes are recorded above, no province frontier moved into core. Current outside-lane admit/reject spot-check remains the fresh closure's responsibility. Author advice cannot satisfy it.

### Frozen staging is itself a gate

| id | class | evidence pointer | captured-by | fix / demonstrated boundary |
|---|---|---|---|---|
| M15 | landing | `evidence/resume/audit-active-path-intervention{,-retry,-final}.json` | committed input boundary, safe extraction and exact fixture inventory | Whole-tree safe extraction refused an unrelated absolute symlink; narrowed extraction then exposed Git's absent empty directories. Keep both code2 receipts. Stage only the tracked auditor/active-classifier/C2 inputs; recreate only manifest-pinned missing directories after symlink-ancestor rejection. The same intervention then passes235 command-state runs and sensitive FIFO/marker controls, with no expected byte or verdict changed. |

Intervention runtime equality is finite active-path evidence, not universal filesystem noninterference or semantic precision. The first two attempts ran zero C2 commands; only the final235-run receipt is a pass. Standalone fresh-clone C2 use first runs the explicit three-directory setup in SKILL.md / `empty-directory-materialization.json`; its immutable fixture inventory otherwise remains unchanged.

Final historical precision is166/175, with zero previously passing-case losses on the identical175 names (`precision-comparison.json`), not175/175. Final author trends: expansion unchanged, quality unchanged with unresolved defects visibly marked, discernment improved through grounded corrections to previous outside rejection and preserved counterexamples. Current outside-lane spot-check and admission remain unclaimed.
