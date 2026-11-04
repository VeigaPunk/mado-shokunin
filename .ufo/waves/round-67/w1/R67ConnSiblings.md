# R67ConnSiblings — sibling-overlap and adoption scan (read-only)

Seat: connector, round mado-67 w1. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base (pre-r67 tip) `0b28ffb4baac9586566d246c3f0986b2bb650a33`; freeze `061dc329b598b2723a224b6c7b305b436946ec91`.
Read-only: no sibling instrument or campaign tool executed, no host probe, no compositor/
service/socket access, no git/jj mutation, no write outside this seat file and its scratch
(`/fast/scratch/hyaku/mado-r67/R67ConnSiblings`, removed before yield). All greps are static reads.

## 0. Axes named

- **C1 — calibration**: `quality/counters/c1-r67-register.py` must accept the committed
  returned-host register **and** score 6/6 on the frozen six controls, where the block must cite
  the live receipt path in a *table row's receipt cell*; the superseded r66 counter scores 4/6.
- **C2 — operability**: `quality/landing-counters.sh` selftest green **and** its new control set
  kills M-Z (zero-citation guard clause deleted) and M-R (`GIT_NO_REPLACE_OBJECTS` deleted from a
  child's env constructor); base leaves both untested (`zero_citation_case=0`, `replace_ref_case=0`).

## 1. Prior art on the three named patterns

### (a) `refs/replace` / `GIT_NO_REPLACE_OBJECTS`

| item | source file:line | fit | what mado does |
|---|---|---|---|
| Env object carrying `GIT_NO_REPLACE_OBJECTS` + `GIT_GRAFT_FILE` per git child | `tabi-shokunin/scripts/check-measurement-binding.mjs:186-196` (same shape `check-round-contract.mjs:72`, `check-user-round-contract.mjs:132`) | fits (env-constructor shape) | cites as the per-child env precedent; does not adopt tabi's gate or manifest schema |
| Repo carrying any `refs/replace/` refused outright, plus env pin, plus fixture that plants a replace ref | `kotodama-shokunin/tools/ledger-token-guard.py:50-52,167-168,286-287,393-407,488-492` | **does not fit** (~refusal≠verdict-preservation) | must **not** adopt: C2's R fixture plants a replace ref *inside* the measured fixture and requires the verdict unchanged; refusal would make the control unmeasurable and change the frozen predicate |
| Identical mutation (`GIT_NO_REPLACE_OBJECTS="1"` deleted from the git env) **survives** the default selftest; killed only by a supplemental replace-ref control | `kotodama-shokunin/tools/check-readme-revisions.py:242`; `kotodama-shokunin/.ufo/waves/round-50/falsify/MutateReadmeRev.md:81,242-243,274` | fits | cites as the precedent that C2-R is a **coverage repair**, not a contract change ("smallest repair" is literally mado's R control) |
| Replace refs change committed bytes; fix = env pin + enumerate/refuse | `kotodama-shokunin/.ufo/waves/round-79/w1/MutPath.md:48-49` (F6); adopted in fleet `.ufo/reports/round-80/kotodama.md:12-16` | fits as evidence | C2's knowledge entry may cite kotodama's finding; mado does not claim the mechanism as new |
| Planted `git replace HEAD <fake>` fixture whose selftest case expects exit 0, no findings | `tameshi-shokunin/tools/evidence-disposition.py:387-391`, `:2309-2317`, `:2928-2935` (`v2-historical-replace-ref`) | **fits exactly** | strongest sibling analogue of C2-R: cite; do not adopt tameshi's tool |
| Complete redirect-env set including `GIT_REPLACE_REF_BASE` | `tsukuroi-shokunin/tools/check-adjacency-table-r51.py:188-193` | fits (checklist) | cite for env-set completeness; no adoption |
| Same mutation already measured **in this lane**: `c1-m5-drop-replace-isolation` and `c2-m10-drop-replace-isolation` survive the published denominators (15/15, 58/58) and are killed only by aux replace-ref probes | mado `.ufo/waves/round-66/w1/R66MutHardening.md:85,106,125`; receipt `.ufo/waves/round-66/w1/R66MutHardening/evidence/c1-matrix-c1-m5-drop-replace-isolation.json` (`aux.replace-ref.correct=false`) | fits (internal) | see §5 E1 — C1's frozen 6-case set contains no replace-ref case |

### (b) zero-citation / vacuous-evidence positivity

| item | source file:line | fit | what mado does |
|---|---|---|---|
| Citation checker whose PASS requires `resolved > 0`; `resolved === 0` is a named fail-closed environment condition, with a selftest case | `kumitate-shokunin/scripts/cite-check.mjs:1590`, `:1626-1629`, `:2438-2441` | **fits exactly** | mado's Z control is the same rule one lane over (label ERROR/2 vs DRIFT). Cite; C2 must not claim the rule as new |
| Vacuous pass refused: `named=0 findings=0` on a defective range is not a pass | `tameshi-shokunin/tools/receipt-commit-bind.py:30-31,81` | fits (same class) | cites |
| A manifest with zero rows fails closed (`an empty manifest proves nothing`, exit 2) | `tameshi-shokunin/tools/arm-liveness.py:41` | fits | cites |
| Evaluation failure never recorded as a measured disagreement (exit 2 propagated) | `kumitate-shokunin/scripts/counter-rerun.mjs:50-52` | fits | cites |
| Valid **zero-citation corpus query** expectations: exit 0, `findings: []` | `kake-shokunin/scripts/fixtures/citing-set/21-no-citations-empty-citing-set/expected.json:1-4` | **does not fit** | must **not** absorb: mado's rule is scoped to evidence markers; generalising it to corpus scans would flip kake's legitimate clean result red |

### (c) citation-to-live-object binding

| item | source file:line | fit | what mado does |
|---|---|---|---|
| Receipt must carry `rev=`, a required regex line, ancestry and digest | `tameshi-shokunin/tools/receipt-revision-gate.py:26-29,46-49,108,123` | fits (stronger) | C1's row-local live citation is a narrow instance; cite, no adoption |
| Worktree-only receipt is false on committed bytes | `tsukuroi-shokunin/tools/check-cited-receipts-r62.py:5` | fits | cites |
| ORPHAN = cited but not committed | `kotodama-shokunin/tools/check-orphan-evidence.py:1-12` | **inverse direction — does not fit** | must not be claimed as coverage for C1's *unreferenced* live object (committed but uncited); name the gap |
| Tree-level live check with no row binding (the r67 defect) | mado `quality/counters/c1-r66-register.py:105-116`; frozen register `PROVINCE.md:259-274` | fits (baseline) | r67 counter adds receipt-cell binding only; no new predicate |

## 2. `shokuknow/merge/mado` package

- **Theme: no fit.** 147 rows, 65 knowledge files, 4 amendments; theme is Hyprland/Waybar/IPC/
  gkeep/two-literature. Grep for `git replace|refs/replace|replacement object|no-replace` returns
  nothing. Grep for `instrument|exit status|citation` returns exactly one row, `S333`
  (`SOURCES.append.md:137`) — a Japanese post naming the *input-observation* tools wev and evtest,
  not a lane instrument, receipt or citation contract. **Nothing in the package is evidence for C1
  or C2**, and nothing may become a third claim.
- **Registry collision: real and worse than the package states.** `MERGE-REPORT.md:9` was built when
  the lane held 192 rows and first staged id was S203. Now: lane `corpus/SOURCES.md` holds **372
  rows through S435** (64 holes below max). Staged ids are contiguous **S203–S349 (147)**:
  **94 collide**, **53 free but interleaved** (S222–S231, …). Adoption would need scratch
  renumbering plus per-entry re-grounding (`CORPUS` rules 1/2/4) and would still be off-axis.
- **Adoption: none.**

## 3. `considerthese/2026-10-28.md`

Six proposals (missing-day placeholder; privacy recheck; lane-state streak; live-tool table;
relayed-vs-re-measured; adoption flagging). **None is claim-shaped for C1/C2.** Proposal 2 is
**already executed this round** by L1: `.ufo/waves/round-67/considerthese-privacy-r67.txt`
(`exit=1`, `files=33466 findings=280`, `waived findings=49 files=47`, flagged
`round-37/receipts/eventq-live-ss.txt`, `round-38/receipts/eventq-live-ss.txt`, plus four
self-matches inside `quality/`). Its residual is a bookkeeping statement, not an instrument.
Proposal 4 (live-tool table) is not claim-shaped. Proposal 5 (relayed vs re-measured) is the only
thematic neighbour of C1's live-cited distinction and remains a writing convention — adopting it
would impose a rule outside both frozen predicates. **Answer: none.**

## 4. Adjacent-domain evidence mado must NOT absorb (owner named)

| evidence | owning lane | why not absorbed |
|---|---|---|
| `zero-resolutions` → `DRIFT (environment: …)` taxonomy, exit-2 fail-closed | kumitate (`scripts/cite-check.mjs:1626-1629`) | adopting the label/taxonomy would rewrite C2's frozen marker contract (`citations=0` ⇒ ERROR/2 inside `marker_valid`) |
| "refuse a repo carrying any `refs/replace/`" policy | kotodama (`tools/ledger-token-guard.py:50-52,286-287`) | would make C2's own R fixture (which plants a replace ref) unmeasurable |
| valid zero-citation corpus query is clean | kake (`scripts/fixtures/citing-set/21-no-citations-empty-citing-set/expected.json`) | contradicts mado's Z only if generalised beyond evidence markers |
| measurement-binding manifest/reproduce schema | tabi (`scripts/check-measurement-binding.mjs`) | different instrument family; would widen C2 |
| evidence-disposition lifecycle gate | tameshi (`tools/evidence-disposition.py`) | same class, different object; cite only |
| privacy-gate findings at tip (280/49 waived) | operator-owned (proposal 2) | C2's GREEN/rc0 is a landing-instrument verdict; do not read it as privacy-clean |

## 5. Second-order effects on the planned moves (no claim change)

- **E1 — C1's 6/6 is blind to a dropped replace-ref pin.** The frozen six C1 controls contain no
  replace-ref case, and the in-lane measurement already showed `c1-m5` surviving 15/15 while reading
  replacement bytes (`R66MutHardening.md:85`). A freshly written `c1-r67-register.py` that omits
  `GIT_NO_REPLACE_OBJECTS` in its `git()` env still prints 6/6. Carry the pin verbatim
  (`c1-r66-register.py:43-45`); state m5 as still outside the denominator.
- **E2 — ledger-population coupling.** Population = `tools/**` + `quality/*.py` + `quality/counters/*.py`
  (`quality/check-tool-ledger.py:10-16,82`). Both r67 counters land there, so **each claim's landing
  adds an uncovered path** until `quality/tool-ledger.md` gets its row; C2's ledger leg then reads
  `TARGET_MISSED` for reasons outside C2. Add both rows in the same landing.
- **E3 — C2's Z kill has two detectors.** Draft `w1/R67ExecLanding/draft/quality/landing-counters.sh`
  adds a behavioural case (`:153-159`, zero marker ⇒ rc 2) and a textual needle
  (`:160-172`, clause present exactly once inside `marker_valid`). The needle is self-referential;
  report the behavioural case as the detector and the needle as a tripwire, or a critic will call the
  kill thesis-guarding.
- **E4 — the child stays permissive.** `tools/mado-receipt-citecheck.py:130` still yields
  `TARGET_MET` at `citations=0` when invoked directly. The claim installs the guard in the *marker
  contract* only; say so, and do not let "zero-citation closed" float free of that scope.
- **E5 — register refinement must not be a heading.** A second `### Surface state register (2026-11-03`
  breaks C1's uniqueness test and flips `genuine` to reject; r65/r66 refinements are bold paragraphs
  (`PROVINCE.md:259,274`). Keep the r67 refinement bold and after `<!-- r65 register end -->`.
- **E6 — live-cited must read the 4th cell only.** r66 collects receipts from anywhere in the block
  (`c1-r66-register.py:106`), which is why `live-in-state-cell-only` passes. A whole-row scan in the
  r67 counter reproduces that failure.
- **E7 — fresh private scratch.** Both r67 counters extract fixtures; predictable scratch paths are
  the planted-symlink class already closed at `corpus/lessons/round-66.md:130-131`.

## 6. One bounded proposal (cheap, non-widening)

Re-run the **retained** r66 m5 recipe against the r67 counter as a **declared auxiliary probe**:
plant `refs/replace` in a fixture, run `quality/counters/c1-r67-register.py`, require the same
verdict as on the un-planted fixture, and record the result **beside** the 6/6 with the sentence
"m5 remains outside the frozen denominator". Recipe source:
`.ufo/waves/round-66/w1/R66MutHardening/evidence/c1-matrix-c1-m5-drop-replace-isolation.json`
(`aux.replace-ref`, `want=accept`, `want_rc=0`). Cost: one fixture run. It improves calibration
(the counter is shown to read real objects) and harms no axis: no predicate, control, expectation,
denominator or axis changes; if it fails it is a caught regression before land.

## 7. Verification the main agent should run (not run here)

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
grep -c '^| S[0-9]' corpus/SOURCES.md                  # 372
grep -oE '^\| S[0-9]+' corpus/SOURCES.md | grep -oE '[0-9]+' | sort -n | tail -1   # 435
grep -n 'GIT_NO_REPLACE_OBJECTS' quality/counters/c1-r67-register.py              # must hit
grep -n 'citations" -gt 0' quality/landing-counters.sh                            # exactly one, in marker_valid
grep -n 'GIT_NO_REPLACE_OBJECTS' quality/counters/c3-r56-used-by.py quality/check-tool-ledger.py
```

## 8. Scratch

`/fast/scratch/hyaku/mado-r67/R67ConnSiblings` created and removed; nothing retained.
