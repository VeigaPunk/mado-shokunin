# Seat ExecLedgerPopulation — round 51 w1: C1 population and tool-ledger draft

Lane: mado-shokunin. Round base (lane tip at round start): `6ca8c559a4a3d6d361101592116eea2bc7452437`.
Scope: derive the C1 population exactly as the frozen predicate `PRED-C1-r51` defines it, and draft the
ledger at `quality/tool-ledger.md` into this seat. Nothing tracked was edited; no gate, build, lint or
formatter was run (parent owns those). Status: complete.

## Population — derivation and result

Command (read-only git, at the round base):

```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-tree -r 6ca8c559a4a3d6d361101592116eea2bc7452437 \
    --name-only -- tools quality
```

The listing returns 91 paths. Applying the frozen rule — every file under `tools/` (any extension),
every `quality/*.py` (direct children only), every `quality/counters/*.py` (direct children only);
`__pycache__`/`.pyc` do not exist at this rev, `.txt` and `.json` excluded, `.sh` counted only under
`tools/` — leaves **79** files:

| group | count | note |
|---|---|---|
| `tools/` | 17 | 16 `.py` plus `tools/mado-verify.sh` (the only `.sh` the rule admits) |
| `quality/*.py` | 18 | `check-*.py` (15), `counter-selftest.py`, `population-suite.py`, `ratio-domain-meta.py` |
| `quality/counters/*.py` | 44 | 20 `c1-*`, 22 `c2-*` (including `c2-ledger.py` and `c2-r50-session-gate.py`), `c3-r39-options.py`, `c4-r39-options-entry.py` |

The 12 paths under `tools/`+`quality/` that the rule excludes, with the reason:

- `.json` (6): `quality/counters/c1-r46-fixtures.json`, `c1-r46-fixtures-v2.json`, `c1-r47-fixtures.json`,
  `c1-r48-fixtures.json`, `c1-r48-fixtures-v2.json`, `c1-r49-fixtures.json` — fixture data, not instruments.
- `.txt` (5): `quality/q36-successor-receipts.txt`, `quality/session-material-waivers.txt`,
  `quality/receipts/axis-2a65350a4df2a31985ed37e90df90325348a8820.txt`,
  `quality/receipts/axis-520c631d2925807aadadb041eeda13f8b829b0c5.txt`,
  `quality/receipts/red-axis-publication-stale-at-data-commit.txt` — receipts.
- `.sh` outside `tools/` (1): `quality/q36-successor-run.sh` — the rule admits `.sh` only under `tools/`.

Both counts are re-derivable with no worktree read; `population.json` carries the per-file line count and
blob sha256 at the base, so drift is measurable without re-listing.

## Deliverables

- `.ufo/waves/round-51/w1/ExecLedgerPopulation/tool-ledger.md`
- `.ufo/waves/round-51/w1/ExecLedgerPopulation/population.json`
- `.ufo/waves/round-51/w1/ExecLedgerPopulation.md`

`tool-ledger.md` is the draft of the tracked `quality/tool-ledger.md` (same basename, seat copy);
`population.json` is the population manifest.

## Ledger draft — shape and verification

115 lines, one header, one separator, **79 rows**, three cells per row, the row grammar stated inside a
fenced block so no row parser can read it as data:

```
| `<repo-relative path>` | <one-line description> | `<pointer path>` or `<pointer path>:<line>` |
```

- cell 1 — the instrument's exact repository path, backticked, each population file exactly once.
- cell 2 — what the instrument does, read from its own module docstring (every description is a restatement
  of the file's own header: resolver contract, clauses, exit codes). No description was inferred from a
  file name, and none contains a `|`.
- cell 3 — an accountability pointer to a tracked file that names the instrument, with the line where the
  name occurs at the base (`path:line`; the suffix is an annotation, containment is the checked property).

Measured on the draft (structural re-parse, fenced blocks skipped, header and separator skipped):

| check | result |
|---|---|
| rows | 79 |
| distinct cell-1 paths | 79 (no duplicate) |
| population files named | 79/79 → `uncovered=0` |
| rows naming a non-population file | 0 → `dangling=0` |
| rows with a placeholder/empty description | 0 → `empty_desc=0` |
| rows whose pointer file is absent at base | 0 |
| rows whose pointer file bytes lack the basename | 0 → `bad_pointer=0` |
| rows whose stated `:<line>` does not carry the basename | 0 (all 79 re-read at the base blob) |

Pointer classes actually used (79 total): `SCORECARD.md` 42, `PROVINCE.md` 20,
`corpus/lessons/round-48.md` 4, `corpus/QUALITY.md` 3, `corpus/lessons/round-44.md` 2,
`.ufo/waves/round-45/registration.md` 2, `.ufo/waves/round-40/registration.md` 2, and one each from
`corpus/lessons/round-25-verifier-spotcheck.md`, `corpus/lessons/round-41.md`,
`corpus/lessons/round-43.md`, `.ufo/waves/round-44/registration.md`.

Selection rule (so a reviewer can re-derive any row): preference order `PROVINCE.md`, `SCORECARD.md`,
`corpus/lessons/*`, `corpus/knowledge/*`, `corpus/README.md`, `SKILL.md`, `LOG.md`, other `corpus/*`,
`plans/`+`reports/`, then `.ufo/waves/**/registration*.md`; inside a file, the first line carrying the
row's full repo-relative path, else the first line carrying the basename.

**Gap status: no row needed the report fallback.** Every one of the 79 files is named by at least one
tracked document at the base. The five superseded v1 counters (`quality/counters/c1-r40-live.py`,
`c1-r44-geometry-states.py`, `c1-r45-monitors.py`, `c2-r40-forms-entry.py`, `c2-r45-monitor-entry.py`) are
named by no lane-level document at all — PROVINCE.md, SCORECARD.md, SKILL.md, LOG.md and every `corpus/`
file were searched — so their row points at the round registration that froze the predicate
(`.ufo/waves/round-40/registration.md`, `round-44`, `round-45`). That is the honest record of where they
are answerable, and it is a real gap in the lane's accountability surface, not only in this ledger: a
superseded counter has no lane-level entry naming it once the round closes.

## Data-revision delta — two rows owed at integration

At the data revision the population is **81**: `quality/check-tool-ledger.py` and
`quality/counters/c1-r51-ledger.py` enter it. The draft deliberately omits both (listing a file that does
not exist at the checked rev is `dangling`), so the integration must add exactly two rows or the counter
reads `uncovered=2`. The two rows below are the bytes `ExecLedgerGate` measured to score clean at 81 (shape
B in `.ufo/waves/round-51/w1/ExecLedgerGate/crosscheck.txt`; description wording is each instrument's own
scope, restated):

```
| `quality/check-tool-ledger.py` | PRED-C1-r51 gate: derives the population (tools/, quality/*.py, quality/counters/*.py) at a rev, parses the lane ledger, fails uncovered/dangling/bad_pointer/empty_desc; hermetic --selftest. | `.ufo/waves/round-51/claims.md` |
| `quality/counters/c1-r51-ledger.py` | PRED-C1-r51 counter: runs the ledger gate and an independent population sweep at --rev, emits the frozen `C1_R51:` line. | `.ufo/waves/round-51/claims.md` |
```

The pointer `.ufo/waves/round-51/claims.md` is the right one: it is committed at the claims commit
`d2740281` (before any data rev), and lines 20–21 carry both basenames verbatim, so containment holds
without a line suffix and without depending on any seat report.

**Rehearsed on both instruments, not assumed:**

- `ExecLedgerGate` (owner of the checker) ran my 79-row draft against a full `git archive 6ca8c559` tree
  with the ledger at `quality/tool-ledger.md`: `population=79 ledger_rows=79 uncovered=0 dangling=0
  bad_pointer=0 empty_desc=0 verdict=TARGET_MET` exit 0 (`.ufo/waves/round-51/w1/ExecLedgerGate/crosscheck.txt`
  §M0), and the same fixture's four one-defect controls plus the absent-ledger case all MISS as specified.
  With the checker and counter landed and the ledger still at 79 rows it reads `population=81 ledger_rows=79
  uncovered=2` exit 1 (shape A); with the two rows above it reads `population=81 ledger_rows=81 uncovered=0
  dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET` exit 0 (shape B).
- `ExecLedgerCounter` independently committed my ledger plus the gate and its counter at their tracked paths
  in a scratch clone at `d2740281` and measured twice: `uncovered=2` for exactly these two files and
  `bad_pointer=0` at 81, then 81/81 clean once the two rows are added
  (`.ufo/waves/round-51/w1/ExecLedgerCounter/receipts/rehearsal.txt`).

The durability property both runs establish: all 79 existing pointers resolve from **committed record files
with no round-51 seat report present** — only the two owed rows need a pointer of their own, and
`claims.md` supplies it at the claims commit. `quality/tool-ledger.md` itself is not in the population (not
a `.py`), so it needs no row.

Pointer-target choice, settled by measurement rather than preference: both peers first rehearsed the owed
rows with seat-report pointers (`.ufo/waves/round-51/w1/ExecLedgerGate.md`, `…/ExecLedgerCounter.md`), which
is legal only if both reports are committed at the same tip. `claims.md` removes that dependency — it is
already committed at `d2740281` and names both basenames. Two independent runs confirm it: the gate's
shape-B fixture (checker + counter landed, `claims.md` present) scores 81/81 clean, and the counter's
stage-c rehearsal at `24a9ea7d` re-points the two rows at `claims.md:20` / `claims.md:21` **with the seat
reports removed** and still reads `population=81 ledger_rows=81 uncovered=0 dangling=0 bad_pointer=0
empty_desc=0 verdict=TARGET_MET` exit 0 from both instruments
(`.ufo/waves/round-51/w1/ExecLedgerCounter/receipts/rehearsal.txt`, stage-c). Use `claims.md`; the seat
reports are the fallback, not the default.

The predicate's base clause is receipted independently by the counter seat: at
`6ca8c559a4a3d6d361101592116eea2bc7452437` the frozen command prints
`C1_R51: verdict=TARGET_MISSED ledger=absent population=79 rev=6ca8c559…` and exits 1
(`.ufo/waves/round-51/w1/ExecLedgerCounter/receipts/base-and-setup.txt`; the same at the claims tip
`d2740281`), with three setup-error cases exiting 2.

## Notes for the freeze and risks

1. **Population rule spelling.** "Under `tools/`" is recursive; `quality/*.py` and `quality/counters/*.py`
   are direct children. A checker that globs `quality/**/*.py`, `quality/**/*.sh` or `tools/**` with no
   extension filter changes `P`. The three group counts (17/18/44) are the cheap cross-check.
2. **Pointer line suffix must not be validated.** The `:<line>` is measured at base; a later edit to
   `SCORECARD.md` can move a name while containment still holds. Verifying the line number would make the
   predicate fail on an unrelated prose edit.
3. **Containment is substring-level.** `quality/check-population.py` resolves through a round-26 wave copy
   (SCORECARD.md:1735) because that line contains the tracked path as a substring; if the freeze wants
   pointers restricted to a class list, §Pointer classes above is the exact set to rule on.
4. **Five registration pointers** (superseded counters) are tracked and immutable, but they are
   `.ufo/waves/` evidence rather than a lane-level doc; flag them for the freeze rather than re-pointing —
   no lane-level alternative exists at base.
5. **Do-nothing controls stay cheap.** `uncovered` bites by deleting one row, `dangling` by adding
   `` `tools/mado-verify.py` `` (a non-existent sibling of `mado-verify.sh`, which is in the population),
   `bad_pointer` by pointing a row at `README.md` (tracked, does not name any instrument), and `empty_desc`
   by replacing a description with `N/A`. Each is a one-cell edit of the draft.
6. **Descriptions are pipe-free by construction.** A literal `|` in a description splits the row into four
   cells and the gate reads it as `dangling`; every one of the 79 descriptions was checked for `|` and none
   contains one. Keep that property when the two data-rev rows are added.
7. **Containment is name-bounded in the gate as landed.** `ExecLedgerGate` changed pointer matching so that a
   pointer file mentioning only `not-alpha-tool.py` does not cover `alpha-tool.py`, and duplicate rows count
   as `dangling` (`row-duplicate-line-N`) with whitespace-only descriptions as `empty_desc`. The 79-row draft
   passes unchanged under that stricter matcher (re-run by the gate after the change), and every row also
   passes name bounding under three plausible boundary classes — `[A-Za-z0-9_]`, `[A-Za-z0-9_.]` and
   `[A-Za-z0-9_.-]` on both sides of the basename — with 0 failures, because no basename here is a proper
   prefix of another at a name boundary (v1/v2/v3 siblings differ before the extension, so `c1-r46-devices.py`
   never occurs inside `c1-r46-devices-v2.py`).
8. Peer alignment: `ExecLedgerGate` (owner of `quality/check-tool-ledger.py`) published the 3-cell row
   contract and the same 79-file base population; the draft was built to that contract and both facts were
   confirmed to that seat, including a correction of two pointer-distribution figures I first reported.
   Both peers then measured the draft independently (§Data-revision delta): the gate on a `git archive` tree
   with its controls, the counter in a scratch clone at the claims rev.

## Retained evidence and host discipline

- Read-only git at the base for every measurement (`ls-tree`, `show`); no worktree mutation, no checkout.
- No tool installed, no package manager invoked, no service touched, no compositor socket opened.
- Scratch `/fast/scratch/hyaku/mado-r51/ExecLedgerPopulation/` held the derivation intermediates
  (`pop.txt`, `headers.txt`, `pointers*.json`, `gen_ledger.py`) and was deleted after the artifacts landed;
  nothing in it is cited as evidence that is not restated above.
- Artifact digests at hand-off: `tool-ledger.md` sha256
  `c0a89805f4e5b7362d74763c3ef2aad0def8adb9664dc3c7845b6c381f382e25` (115 lines);
  `population.json` sha256 `bd110aa67a87425a2e3933611c259e378f87de8a4aaed8ca39ea8b6ae83af8ca` (425 lines).

Report: .ufo/waves/round-51/w1/ExecLedgerPopulation.md
