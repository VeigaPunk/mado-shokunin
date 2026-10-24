# mado round 30 — registration (frozen before data commit)

Steered round 30, attempt 1. Base `8f51071b5bc44c815eeb5da76bb7f1947994ffb8`
(round-29 closure: ADMITTED; C1/C2 TARGET_MET; the inherited 41/43 navigation
gap routed here). Written and frozen before the data commit; the lane's own
worktree already carries the claimed edits at write time — all measurements
read committed bytes at named revisions (`git show REV:path`), never the
worktree.

## Routed queue (from `corpus/lessons/round-29-verifier-spotcheck.md`)

1. Close the inherited coverage-index gap: index rows for
   `mutation-testing-r28.md` and `workspace-rules-r27.md`. → **C1** below.
2. Wave dispatch surface: the r29 33-seat wave was prepared but not
   dispatched — an L1 seat has no swarm-dispatch tool (expected host surface;
   the orchestrator dispatches prepared waves between rounds). → This round
   prepares its wave under `.ufo/waves/round-30/` and itemizes it in the
   report; no dispatch claim.

## Axis selection (criterion 22: re-derive every active axis first)

Bounded sub-axes, measured at base `8f51071b` on 2026-10-24:

| Sub-axis | Rule | Base value |
|---|---|---|
| coverage / admitted-note reachability | frozen literal fence (S185): `indexed/notes` over `corpus/knowledge/*.md` vs `corpus/README.md` rows | 41/43 = 9.5349/10, exit 1 (evidence `c1-before-8f51071b.txt`) |
| coverage / sourced current-art ground | `covers: U1..U7` entries whose `source:` cites a `mined` row | 7/7 = 10.0000 |
| calibration / literal lesson-citation | `grep -cE '^[0-9]+\. .*lessons/'` over `^[0-9]+\. '` QUALITY.md | 28/40 = 0.7000 |
| calibration / resolved-active grounding | `.ufo/waves/round-30/c2/count.py` active-resolved rubric (below) | 31/39 = 0.7949, TARGET_MISSED |
| operability / hermetic suite | `bash tools/mado-verify.sh --selftest` | 460/460 = 10.0000 (harm watch) |

Lowest-scoring non-retired axis: **calibration** (literal 0.7000,
resolved-active 0.7949 — both below coverage 0.9535 and operability 1.0).
depth and adjacency carry no bounded rubric (unscored, declared, not invented).

## Claims (3; distinct axes; causally separable)

**C1 — coverage / admitted-note reachability (routed defect; sourced: S185).**
Land the two missing coverage-map index rows in `corpus/README.md` for
`knowledge/workspace-rules-r27.md` and `knowledge/mutation-testing-r28.md`,
each row quoting the note's own header/scope (no new domain claim admitted).
Predicate `PRED-C1-r30`: the frozen fence prints `indexed=43/43
missing=0 dangling=0 duplicates=0` exit 0 at the data commit.
Before: `indexed=41/43`, exit 1 at `8f51071b`. Target: 43/43, exit 0.
Kill rule: any of missing/dangling/duplicates nonzero at data commit.
Control K1: the same fence at base `8f51071b` — prints `missing=2`, exit 1
(do-nothing cannot reach 43/43).

**C2 — calibration / lesson-grounded admission criteria (lowest axis).**
Every *active* criterion line in `corpus/QUALITY.md` resolves a `lessons/`
citation at the data commit. Counter `.ufo/waves/round-30/c2/count.py` (its
docstring freezes the rubric): criterion lines = `^[0-9]+\. `; a line is
superseded when a later line says `Supersedes criterion N` (20 is already
superseded by 21 — counted out of both fractions); *resolved* = every
`lessons/<file>`, `lessons/<file>#<anchor> M<ids>` and `lesson round<NN>
M<ids>` citation in the criterion's text resolves (file exists at REV, anchor
word present, every M-id present; compound ids `M<round>-<n>` match
literally). Predicate `PRED-C2-r30`: `unresolved_active = 0` AND literal
fraction ≥ 0.70 at the data commit. Before at `8f51071b`: literal 28/40,
resolved-active 31/39, UNRESOLVED {1..5, 38..40}, TARGET_MISSED. Target:
resolved-active 40/40 (12 lines superseded by rows 41–51, +1 new criterion
52; literal 40/52 = 0.7692). Kill rule: any UNRESOLVED active criterion, or
literal < 0.70. Control K2: the same counter at base — TARGET_MISSED with 8
named unresolved criteria (do-nothing stays red).

**C3 — operability, capability acquisition: index-completeness gate
(sourced: S185).** `quality/check-index.py` implements the frozen fence's
row-set semantics as a re-runnable lane gate: `corpus/knowledge/*.md` vs
`corpus/README.md` index rows, at a git revision (`--rev`) or a plain tree
(`--root`; regular files only, symlinks refused), plus `--selftest`.
Predicate `PRED-C3-r30`: at base `8f51071b` the gate prints
`MADO_INDEX: ... indexed=41/43` exit 1; at the data commit it prints
`indexed=43/43` exit 0; `--selftest` prints `MADO_INDEX_SELFTEST: 6/6
assertions passed` exit 0 (missing/dangling/duplicate rows, symlink refusal,
empty tree). Kill rule: gate reports indexed≠notes at either revision, or
selftest < 6/6, or gate misses the base gap (a green-at-base gate is vacuous).
Control K3: gate at base must be RED — committed before data; a gate that
prints green at base cannot measure C1.

## Data rule

One data commit carries `corpus/README.md` (2 rows), `corpus/QUALITY.md`
(rows 41–52), `corpus/SOURCES.md` (+S185), `corpus/lessons/round-30.md`, and
the control receipts if space allows; the after-measurements run against
that commit's hash. Receipts land in `.ufo/waves/round-30/evidence/`.
Counters and the gate are frozen in the pre-data commit; the composite
smoke rule (criterion 49) is satisfied by running all three at their freeze
commit before the data commit lands.

## Harm watch (registered)

`bash tools/mado-verify.sh --selftest` stays N/N; census
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
mado` exit 0 at start and end; no `tools/` byte changes beyond the new
`quality/check-index.py`; `SKILL.md`, `PROVINCE.md`, `corpus/knowledge/`
byte-untouched; no compositor/config mutation; misroot sweep at fleet root
before the report.

## Sourced claim

C3's gate implements S185 (own-work, opened 2026-10-24 — the frozen
navigation fence text in `SCORECARD.md`); C1 is the repair S185's fence
measured. The lesson `## Gate` records the URL-equivalent (repo path + block
sha), access date, and a verbatim ≤25-word quote.

## Planner-seat mapping (orchestrator ruling 2026-10-19)

The §3 planner seat is held by the L1 (validator rejects `planner`); the
bounded planning data-walk (axis re-derivation table above) rides the
`ScoutAxisScores` wave item.
