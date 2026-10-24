# CritCausal — r30 w1 — falsify causal separability (report only)

Assignment: attack the registration's frozen line "**Claims (3; distinct axes;
causally separable)**" (registration.md:36). For each counter, score it at
base `8f51071b` and at a hypothetical commit carrying only its own delta;
report any cross-dependency. Lane repo bytes and lane git state untouched —
all hypotheticals run in a scratch clone `/tmp/mado-causal` (read-only on the
lane), synthetic trees under `/tmp/c1tree` for the `--root` mode. Nothing
written outside this report.

## 0. Method — where the deltas live

| Commit | Role | Files |
|---|---|---|
| `8f51071b` | base | — |
| `451e8b3` | freeze | `c2/count.py`, `quality/check-index.py`, controls, registration |
| `446dc39` | data (ONE commit) | `corpus/README.md` (+2 rows, C1) · `corpus/QUALITY.md` (rows 41–52, C2) · `corpus/SOURCES.md` (+S185, C3 provenance) · `corpus/lessons/round-30.md` (shared: M30-1/C2, M30-2/C1, Gate/C3) |

Counter input surfaces (read from `git show REV:path` only):
- C1 fence (SCORECARD.md:69–87): `ls-tree REV:corpus/knowledge` names +
  `REV:corpus/README.md` rows. Inputs: {knowledge dir, README}.
- C2 counter `count.py`: `REV:corpus/QUALITY.md` + `REV:corpus/lessons/*`.
  Inputs: {QUALITY, lessons/}.
- C3 gate `check-index.py --rev`: same two inputs as the fence; `--root`
  reads a plain tree; `--selftest` reads nothing in-repo.

The three input surfaces are disjoint **except** `lessons/round-30.md` —
the only newly-cited file (all 30 other `lessons/` files QUALITY cites exist
at base; verified `git cat-file -e 8f51071b:corpus/lessons/*`).

## 1. Baseline re-derivation at `8f51071b` (lane, read-only — all match receipts)

| Counter | Result | Receipt |
|---|---|---|
| C1 fence (verbatim SCORECARD block) | `indexed=41/43 missing=2 dangling=0 duplicates=0` exit 1, both routed notes named | `evidence/c1-before-8f51071b.txt` ✓ |
| C3 gate `--rev 8f51071b` | `indexed=41/43` exit 1 | `controls/C3K1-base-red.txt` ✓ |
| C2 `count.py 8f51071b` | literal 28/40 (0.7000), active 39, resolved 31/39 (0.7949), UNRESOLVED {1-5,38,39,40}, TARGET_MISSED exit 1 | `evidence/c2-before-8f51071b.txt` ✓ |

Also at base: `lessons/round-30.md` ABSENT, `quality/check-index.py` ABSENT,
both routed notes PRESENT in `corpus/knowledge/` (the C1 gap is rows-only).

## 2. Hypothetical single-delta commits (scratch clone `/tmp/mado-causal`)

| Hypothetical commit | Content | Counter scored | Result |
|---|---|---|---|
| `e0c0c95` | base + `corpus/QUALITY.md`@446dc39 only | `count.py HEAD` | **TARGET_MISSED** — `resolved_active=34/40`; `UNRESOLVED criterion {41,42,43,44,45,52}: missing corpus/lessons/round-30.md` |
| `e0c0c95`+lesson | + `corpus/lessons/round-30.md`@446dc39 | `count.py HEAD` | **TARGET_MET** — 40/40, literal 40/52=0.7692 |
| above +README+SOURCES | + `corpus/README.md`, `corpus/SOURCES.md`@446dc39 (gate file absent from tree) | `count.py HEAD` | **TARGET_MET** — identical output |
| `ec40702` (GateOnly D1) | base + `quality/check-index.py`@451e8b3 only | `check-index.py --rev HEAD` | **`indexed=41/43` exit 1 — C3 tip leg FAILS**; `--selftest` 6/6 exit 0 |
| `e017580` (D2) | D1 + `corpus/README.md`@446dc39 | `check-index.py --rev HEAD` | `indexed=43/43` exit 0 |
| synthetic tree (`--root`) | 43 base knowledge files + data README only (no QUALITY/SOURCES/lesson/gate in tree — 44 files total) | `check-index.py --root` | `indexed=43/43` exit 0 |
| synthetic tree | same, base README | `check-index.py --root` | `indexed=41/43` exit 1 |

## 3. Answers to the three falsification questions

**(a) Does PRED-C2-r30 depend on C1's README rows or C3's tool?**
*Neither — but it does depend on the shared lesson file.* README/SOURCES
added on top of QUALITY+lesson leave the counter's output byte-identical
(TARGET_MET 40/40), and MET obtains at a commit where
`quality/check-index.py` does not exist. However, QUALITY alone →
**TARGET_MISSED**: six new active criteria (41–45, 52) cite
`lessons/round-30.md`, which is not in C2's QUALITY file. If
`lessons/round-30.md` counts as C2's own delta (it holds M30-1, C2's audit
finding), C2 verifies independently; the file also carries M30-2 (the C1 gap
record) and the §Gate S185 row (C3's provenance), so under any strict
"own delta only" reading C2 is not self-contained either.

**(b) Does C1's 43/43 depend on the QUALITY/SOURCES edits?**
*No — C1 is cleanly separable.* A 44-file tree containing nothing but the
base knowledge corpus and the data README prints `indexed=43/43` exit 0.
The fence's input surface never touches QUALITY, SOURCES, or lessons/.
QUALITY-only edits cannot move the fence either direction (files disjoint).

**(c) Does C3's gate verdict depend on either?**
*Yes — the tip leg is C1's output re-printed.* Gate-only commit `ec40702`:
the tool exists, `--selftest` passes 6/6, but `--rev HEAD` prints
`indexed=41/43` exit 1 — the predicate's green leg fails outright. Adding
C1's README delta flips the same command to `43/43` exit 0. PRED-C3-r30 as
registered is therefore **not verifiable by its own delta**: two of its
three legs are self-sufficient (base-red needs only the tool at freeze
`451e8b3`; selftest is hermetic), but the green-at-tip leg measures the
state of `corpus/README.md`, i.e. C1's deliverable.

## 4. Verdict on the frozen line

"3 claims; distinct axes" — holds (input surfaces are disjoint modulo the
lesson file; each counter's numerator is genuinely different work).
"causally separable" — **falsified**: C3 → C1 is a hard dependency
(empirical: `ec40702`), and C2 → `lessons/round-30.md` is a dependency on a
shared artifact the registration assigns to no claim explicitly (empirical:
`e0c0c95`). The bundled single data commit `446dc39` made this invisible:
at the shipped tip every leg is simultaneously satisfied, so receipts cannot
distinguish "independent" from "co-landed".

Impacted axes: operability (C3's green leg inherits coverage's measurement —
the "capability" is real but its headline number is borrowed); coverage
(itself unaffected — C1 is the only claim that stands alone); calibration
(C2's MET is conditional on delta-assignment of the lesson file).

## 5. Collateral findings (report-grade)

1. **Gate ≠ fence on four measured classes** (corroborates
   CritSourcedClaim §3.2; RevC1Fence reported first — three classes
   reproduced by me on synthetic trees/commits):
   a) *Row-regex superset* — gate `ROW_RE = "^\|\s*`knowledge/…"` vs
   fence `"^\| `knowledge/…"`. Reproduced: tree with row
   `|`knowledge/x.md`` (zero space) → gate `--root` prints `indexed=1/1`
   exit 0 while the fence's regex finds zero rows (would print
   `missing=1` exit 1). The gate can print green where the fence prints
   red — the one case C3's green diverges from C1's verdict.
   b) *`--rev` name-splitting* — gate `load_rev` uses `names.split()` vs
   the fence's `splitlines()`. Reproduced (clone branch `SpaceNote`,
   note `sp ace.md` + canonical row): gate `--rev` prints
   `indexed=41/44 missing=3` (phantom `ace.md`) + `dangling: sp ace.md`;
   gate `--root` (`os.listdir`) prints `42/44 missing=2`; the fence
   prints `42/44 missing=2`. `--rev` diverges from BOTH `--root` and the
   fence — the gate's git mode is the least faithful of the three.
   c) *Vacuous green on absent corpus* — gate `--root` on a tree with no
   `corpus/knowledge` prints `indexed=0/0` exit 0; `--rev` exits 2
   (SETUP_ERROR); the fence cannot express a green there (no notes to
   list from a missing tree-path is a crash in its `git` call). Reproduced.
   d) *Default-REV asymmetry* — fence pins `bb08dd57` (fleet-1 baseline;
   an unflagged default run today prints 8/22 exit 1) vs gate default
   `master` (43/43 exit 0). Only bites if an unflagged run is cited.
   On committed bytes all classes are latent (43 canonical rows, 43
   regular ASCII names, contiguous table) — but they sharpen §4: the
   gate is a superset *approximation* of the fence whose tip leg is
   literally C1's measurement re-printed, so any divergence silently
   converts C3's green into a false positive against the fence's own
   semantics. "Implements the frozen fence's row-set semantics"
   (registration.md:69) overstates; "approximates, agreeing on all
   committed revisions to date" is the honest claim.
2. **Counterpart kill-rule risk, dormant**: C1 is fenced by harm-watch —
   had C1's rows landed in the freeze commit (before K3's base-red
   measurement), C3's control would have been *unmeasurable*, not failed.
   Ordering saved it; nothing in the registration enforces that order
   beyond convention.
3. **C1 recheck pointer in a new row** cites
   `.ufo/waves/round-27/c1/count-v4.py` — exists at `446dc39` (spot-checked
   `git cat-file -e`). No dangling pointer.
4. **Out-of-scope worktree write (verified, relayed to Main)**:
   `quality/q36-successor-receipts.txt` carries worktree modifications
   (mtime 2026-10-24 04:06:46, after records commit `92d3c86`): 4 lines of
   rotated ephemeral `/tmp/mado-r28-q36-*` and `run.*` paths; every
   rc/expected/verdict/checker-output line byte-identical — no verdict
   moved, committed bytes safe, but a committed evidence file was
   rewritten outside the registered write scope (likely an Exec* re-run).
   Not restored — worktree repair is outside this item's write scope.

## 6. Smallest safe corrections (for the judge to weigh, not defects to ship)

- Restate PRED-C3's tip leg as an *agreement* leg — "the gate reproduces the
  fence's verdict at base and at tip" — rather than an independent target.
  This is what was actually demonstrated and is arguably the stronger claim
  (equivalence with the frozen fence at two revisions), while making the
  C1 dependency explicit instead of hidden.
- Alternatively split: `PRED-C3a` = capability (exists, selftest 6/6,
  red-at-base on real bytes, green on a synthetic complete tree — all
  self-contained) and `PRED-C3b` = agreement. Each then verifies on its own
  delta.
- For C2: name `corpus/lessons/round-30.md` inside the C2 claim text (it is
  C2's own M30-1 record), or split the lesson file's M-rows per claim.
- Note for future rounds: claim deltas landed in ONE data commit; the
  separability audit requires per-file delta attribution, which the data
  rule could make explicit (file → claim mapping at registration).

## Evidence index

Lane (read-only): `evidence/c1-before-8f51071b.txt`,
`c1-after-446dc396.txt`, `c2-before-8f51071b.txt`, `c2-after-446dc396.txt`,
`c3-after-446dc396.txt`, `controls/C3K1-base-red.txt`,
`controls/C3K2-selftest.txt` — all byte-reproduced this session.
Scratch (reproducible): `/tmp/mado-causal` commits `e0c0c95`, its children
(+lesson, +README+SOURCES), branch `GateOnly` (`ec40702`, `e017580`), and
branch `SpaceNote` (space-named note divergence); synthetic trees
`/tmp/nc` (zero-space row), `/tmp/sp` (space note), `/tmp/empty` (no
knowledge dir) retained; `/tmp/c1tree` deleted after scoring (rebuild:
extract `8f51071b:corpus/knowledge` + `446dc39:corpus/README.md`).

Tooling: none installed; no pacman/uv/npm transactions. Lane git read-only
(`log`, `show`, `cat-file -e`, `ls-tree`); all writes confined to
`/tmp/mado-causal` clone, `/tmp/c1tree`, `/tmp/{nc,sp,empty}`, and this report.
