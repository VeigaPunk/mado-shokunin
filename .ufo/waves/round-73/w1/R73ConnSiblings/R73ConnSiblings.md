# R73ConnSiblings — one bounded connector proposal

## Axes and evidence

Declared axes: **calibration (C1)** and **operability (C2)**. Preserve the declaration's navigation, ledger, axis-table and 460/460 verifier obligations; no new score is claimed here.

Read first: `.ufo/waves/round-73/claims-declaration-r73.md`, especially lines 27–61, 63–91 and 93–99. Re-read the committed receipts without rewriting or rerunning them:

- `measurement-c1-r73.txt:5–11`: pristine 10/10; four named mutations killed; held controls kill two. N1 is separated by `zero-denominator`; N2 by `valid-then-garbled`.
- `measurement-c2-r73.txt:46–50,75–81`: candidate gets the three new positive carrier cases and two negative cases right; held classifier misses exactly the three positives; terminal census is population=20, readers=13, guarded=13, unguarded=0, controls=28/28, base_controls=25/28.
- `control-baseline-r73.txt:1–8` records the same pre-freeze contrast. These are existing receipts, not executions by this seat.

## Fleet overlap: method shared, target not duplicated

The requested grep of `*-shokunin/quality/counters/*.py` for `mutant|killed|base_killed` returned only mado files (21 matching files, both pages inspected). That path convention is not fleet-wide: stopping there would falsely suggest methodological novelty. A wider sibling Python search, excluding mado and `.git`, `.jj`, `.ufo`, finds substantive precedents:

- **souji**, `census/round-40/c3-counter.py:1–34,185–206`: four named mutations M15–M18 of `tools/souji-worktree-drift.py`, pristine fixture first, candidate versus held fixture, exactly-once anchor checking, named kill evidence and `base_killed=0`. This is directly analogous *control-suite discrimination*, not the same instrument or predicate.
- **kaidoku**, `tools/round-34/replay-gate.py:255–280` and `c2-shortcut-gate-counter.py:28,102–118`: three mutations of its replay gate exercised by red/vacuous cases; the outer counter requires `mutants_killed=3`. Again, shared method, different target.

The wider `GIT_NO_REPLACE_OBJECTS` search finds many sibling **uses**, not evidence that mado invented the guard: e.g. kaidoku `tools/round-25/ruler.py:25–30`, kagi `corpus/revision-audit.py:44–47`, kotodama `reports/round-14/run-validation.py:160–163`. Kaidoku `tools/round-29/freeze-gate.py:195–199` even mutates `os.environ`, showing a related idiom exists elsewhere. That alone neither certifies its launch flow nor makes it a census.

A separate sibling Python search for `guard.census|carrier.census|guarded=|base_controls` found unrelated audio AST guard counting and unrelated fixture arguments, not a replacement-object environment-carrier census. **Bounded conclusion:** no duplicate sibling instrument was found; the mutation-certification method overlaps souji/kaidoku, while this round's landing-outcome rule and mado `quality/check-*.py` carrier population remain mado-specific. This is a current local-source scan, not proof that no historical or differently named sibling implementation ever existed.

## Shared pattern and an explicit contradiction

The useful synthesis is an instrument/control/defect triangle: a suite passing its intended instrument does not show that it detects a specified broken instrument. Require pristine agreement **and** a named mutation's disagreement, with the held leg visible.

C1 measures this directly. C2 measures a related but not identical contrast: its held round-71 classifier is a real predecessor, **not** a literal mutation of the successor. Do not relabel `25/28` as a mutation-kill score or merge the claims into one denominator.

The assignment's requested assertion that `tools/mado-verify.sh` has **never** been scored this way is contradicted by local evidence:

- `tools/mado-verify.sh:1886–1904` documents a pinned ten-defect sweep, pristine GREEN, ten KILLED results and restoration requirements.
- `:2070–2084` includes verdict-token, UNKNOWN-guard deletion and exit-map mutations.
- `SCORECARD.md:21` and `LOG.md:297` record the historical 10/10 sweep and regression replay.

Therefore it cannot honestly be named an unscored instrument. Current-revision certification breadth is a different question, not investigated or asserted here.

Two grounded **not-found-as-mutation-scored** candidates instead are:

1. `quality/counters/c1-r67-register.py`: its contract (`:33–53`) scores six input controls and extra selftest shapes; the counter source and inspected counter registry/history contain no named mutation-separation measurement of this counter. This is a bounded negative finding, not an absolute historical “never.”
2. `quality/counters/c2-r73-shapes.py`: the frozen declaration and receipt score 28 labeled inputs against candidate and predecessor, not successor mutations. Its round-73 evidence does not establish a mutation-separation certificate.

## Proposed move — register-control mutation certificate only

For a future frozen claim, score the **existing six-case r67 register controls** against a small, predeclared set of single-defect mutations of the committed `c1-r67-register.py` assessor: relax fourth-cell live citation, allow a dangling pointer beside a valid pointer, and relax exact live-line membership. Relevant source: `:168–185`; controls and production both call `assess` (`:271–274,319–328`). Freeze exact recipes and denominators before measurement. First measure rather than assume any survivor. Only if a frozen target requires it, add independent controls that separate measured survivors while preserving the held six byte-identically.

This reuses souji's paired pristine/held/candidate evidence structure without importing its code or target semantics. It transfers C1's suite-certification idea to an existing calibration boundary instead of extending carrier grammar indefinitely.

### Second-order effects and risks

- **Runtime:** assessor-only mutation scoring can be hermetic with the controls' embedded object maps; it does not refresh a live host observation.
- **Contract:** distinguish input correctness, mutation applicability, pristine pass and semantic kill. A missing anchor or syntax error is not a kill. Do not alter r73's frozen targets, receipts or four-mutation denominator.
- **Substrate/ownership:** all proposed work is mado-local scratch or future mado artifacts. No sibling file is touched by either r73 claim: C1 reads a mado harness/control set; C2 enumerates mado `quality/check-*.py`. Looking at sibling source here creates no integration dependency.
- **Verification:** report each recipe, digest, separating case and held score independently. Correlated labels and limited mutation families remain limits; no general fault-coverage claim. No axis improvement is asserted until a new frozen measurement earns it. Keeping production bytes unchanged during certification avoids a runtime tradeoff.

### Verification for the responsible future executor (not run here)

Freeze source/control digests and exactly-once, syntax-valid recipes; require pristine six-case agreement; run all named mutations against held and any proposed extended suite under an explicit permitted scratch root; require a named wrong answer, not a crash, for each credited kill. Recheck the then-current no-harm obligations separately. This seat ran no counters, tests, verifier, host probes or alternate runtime, and installed no tools.

## Boundaries and delivery

Only this seat directory was written. The explicit scratch directory was created and removed empty; no scratch receipts were generated. The flat report path requested in the seat footer conflicts with the hard only-write-directory rule, so the actual report is the nested authorized path below; no flat alias was written.

Self-evaluation: accuracy 4/5 (negative overlap findings bounded to searched local source); completeness 4/5 (the demanded verifier “never” claim is disproved, not fabricated); clarity 4/5 (method versus target overlap separated); actionability 4/5 (recipes still require a future freeze and measurement); conciseness 4/5 (extra evidence retained to expose both contradictions). Overall 4.0/5. Main improvement: future evidence can replace bounded negative findings with revision-pinned mutation receipts.

Report: .ufo/waves/round-73/w1/R73ConnSiblings/R73ConnSiblings.md
Sibling mutation methods overlap; no duplicate target instrument found.
Verifier already has mutation scoring; its requested “never” premise is false.
One proposal: certify the register counter's controls against named assessor mutations.

L1 clarification received: the verifier premise is an assignment correction, **not a finding against the lane**. L1 also confirmed the seat-directory write bound controls the report location.
