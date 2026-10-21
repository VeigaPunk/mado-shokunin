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
