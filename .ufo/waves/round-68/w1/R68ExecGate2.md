# R68ExecGate2 — C2: replacement-ref guard for four standing readers

Axis posture: C1 untouched (no harness/recipe work in this seat). C2 operability moved only by
guarding the four assigned readers. Per-file census effect: `guarded` 1 -> 5 on the fixture set,
`population=20 readers=13` unchanged, `controls=11/11`.

Frozen inputs: declaration `claims-declaration-r68.md` (freeze `e0727cda15621766c35dcf8b70c211b6531aab45`),
controls `.ufo/waves/round-68/controls/c2-controls.json`. Base blob ids extracted from the lane
(HEAD `40d2bef89...` and freeze `e0727cda...` carry identical blobs, checked by `git rev-parse`):

| lane file | blob | draft sha256 | diff |
|---|---|---|---|
| quality/check-evidence-pointers.py | c2dcdc9e571fc5c3bdee2f4d094fac5974a6fac4 | dc4cda1b99eb134bb928af350a458df829ee2e43804654a79f5ffde269839efd | +1 / -0 |
| quality/check-freeze-order.py | ada2cf72fd73a2f2d65885a45b406a0f5b032ed0 | cb3493ec84ff908f95b18163865afc3e63d68a68ad9369b2100ae7a7b0c528c0 | +1 / -0 |
| quality/check-index-rows.py | 05c7255d4960e3b5a742871afa1b2faa98ca6ba9 | 9c0915f96fadf660ff3db33092d093dd9ea417e109b737c4d4b180eda309a36c | +4 / -1 |
| quality/check-index.py | d90767623a626be2fec81f5597469ab4bf63830d | b348d92707b04d5b8203003515ceecaca6fabe4ad7aa5094ff83d279bf233e22 | +4 / -1 |

Drafts live at `.ufo/waves/round-68/w1/R68ExecGate2/draft/quality/<same path>`; lane production
files were not written. The `-1` in each index gate is the inline comprehension becoming an
`env` local (`env={...}` -> `env=env`), required to attach the guard; no other byte changed.

## Guard sites and calls guarded

1. `check-evidence-pointers.py` L71-72: module constant
   `GIT_ENV = {...}` then `GIT_ENV["GIT_NO_REPLACE_OBJECTS"] = "1"` (subscript store, env-named target).
   Guarded calls: all `git()` reads (`ls-tree` listing, `show` of LOG/SCORECARD/lesson/axis receipts)
   and the direct `git status --porcelain` using `GIT_ENV`.
2. `check-freeze-order.py` L45-47: `env["GIT_NO_REPLACE_OBJECTS"] = "1"` in `git_env()`.
   Guarded calls: every `git()`/`subprocess.run` path built from `git_env(work)` (init in selftest,
   rev-parse, show, log/merge-base). `extra_env` merge untouched; runtime probe below shows the
   guard survives and `extra_env` override still wins.
3. `check-index-rows.py`: `_git()` L55-61 builds `env`, sets the guard, passes `env=env`; the
   selftest fixture env L404-409 adds `GIT_NO_REPLACE_OBJECTS="1"`. Object reads guarded:
   `rev-parse`, `show` (README, SOURCES, note text), `ls-tree` (knowledge listing). The fixture dict
   only feeds the selftest's `git init/add/commit` (writes), never an object read.
4. `check-index.py`: same two shapes at L48-54 and L281-286. Object reads guarded: `rev-parse`,
   `ls-tree`, `show` (README). Fixture dict only feeds selftest case 9 `init/add/commit`.

## a) Census on scratch (20 lane files + four drafts)

Fixture: `git init` in `/fast/scratch/hyaku/mado-r68/R68ExecGate2/fixture.stb4`,
`rev-parse --show-toplevel` asserted equal, 20 files copied from `HEAD:quality/check-*.py`,
four drafts overwritten, `git add -A`, commit with `-c user.name=r68 -c user.email=r68@example.invalid`
(fixture commit `dc824b4153f192b99073e86cb1e3cb03b7977932`). Command:

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r68-reader-guard.py \
  --repo "$D" --rev HEAD --controls /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-68/controls/c2-controls.json
```

My four lines:

```
MADO_R68_READER file=quality/check-evidence-pointers.py reader=yes guard=yes
MADO_R68_READER file=quality/check-freeze-order.py reader=yes guard=yes
MADO_R68_READER file=quality/check-index-rows.py reader=yes guard=yes
MADO_R68_READER file=quality/check-index.py reader=yes guard=yes
```

Final contract line (rc 1; TARGET_MISSED is expected at seat scope — the other 8 unguarded
readers belong to sibling seats):

```
MADO_R68_READER_GUARD: population=20 readers=13 guarded=5 unguarded=8 controls=11/11 verdict=TARGET_MISSED rev=dc824b4153f192b99073e86cb1e3cb03b7977932
```

All 11 frozen control cases still score `correct=yes`.

## b) Selftest / compile / live read-only invocations (base vs draft)

`python3 -I -c 'py_compile.compile(..., cfile=<scratch>)'`: rc 0 for all four drafts (no
`__pycache__` written next to drafts; the probe cache was removed).

| gate | base rc | draft rc | stdout/stderr diff |
|---|---|---|---|
| check-index-rows.py --selftest | 0 | 0 | empty (rc 0) — `MADO_INDEX_ROWS_SELFTEST: 10/10 assertions passed` |
| check-index.py --selftest | 0 | 0 | empty (rc 0) — `MADO_INDEX_SELFTEST: 12/12 assertions passed` |
| check-freeze-order.py --selftest --work <sep dirs> | 0 | 0 | empty (rc 0) — `MADO_FREEZE_ORDER_SELFTEST: OK` |

Live invocations on the lane, committed file vs draft, `TMPDIR` pointed at scratch:

| command | base/draft rc | output |
|---|---|---|
| `check-evidence-pointers.py --repo <lane> --rev HEAD --branch master` | 0 / 0 | identical, diff rc 0: `PRED-PTR-r36-v1 rev=HEAD pointers_r35=8 dangling_r35=2 dangling_r35_closed=1 pointers_r36=35 dangling_r36=0 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok verdict=TARGET_MET` |
| `check-freeze-order.py --repo <lane> --rev HEAD --round 68 --wave w1` | 1 / 1 | identical, diff rc 0: `MADO_FREEZE_ORDER: round=68 wave=w1 freeze=none freeze_time=none launch=none verdict=FAIL reason=no_freeze` (wave files not committed) |
| `check-index-rows.py --repo <lane> --rev HEAD` | 0 / 0 | identical, diff rc 0: `MADO_INDEX_ROWS: rev=HEAD rows=79 errors=0 warns=3` |
| `check-index.py --repo <lane> --rev HEAD` | 0 / 0 | identical, diff rc 0: `MADO_INDEX: rev=HEAD indexed=79/79 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` |

`sha256 .git/index` before/after the live runs: `e2eee0353d56d66feff99d6224ca24dbf9eae17ea65dee00f775512f1ab59cbc`
both sides (unchanged). An earlier exploratory `git status --porcelain -- quality` refreshed the
index metadata (5981cc13... -> e2eee0...); no tracked file bytes changed. This seat ran no
mutating git command in the lane.

Runtime env probe (imported drafts, fixture repo named via `-C`): `GIT_ENV["GIT_NO_REPLACE_OBJECTS"]=='1'`;
`git_env(None)` key `'1'`; merged `git(..., extra_env={"GIT_DIR": "/x"})` keeps key `'1'` and
`GIT_DIR=='/x'`; both `_git()` paths capture `env['GIT_NO_REPLACE_OBJECTS']=='1'` with argv
unchanged `['git','-C','R','show','HEAD:a']`.

## c) Diffs

`diff -u <lane file> <draft>` per file, hunks only at the guard sites:

- evidence: `@@ -69,6 +69,7 @@` `+GIT_ENV["GIT_NO_REPLACE_OBJECTS"] = "1"` (+1/-0)
- freeze: `@@ -43,6 +43,7 @@` `+    env["GIT_NO_REPLACE_OBJECTS"] = "1"` (+1/-0)
- index-rows: `@@ -53,9 +53,11 @@` env binding + guard (+2), `env=env` (1 replaced), fixture `@@ -401,6 +403,7 @@` (+1) => +4/-1
- index: `@@ -46,9 +46,11 @@` env binding + guard (+2), `env=env` (1 replaced), fixture `@@ -278,6 +280,7 @@` (+1) => +4/-1

Draft sha256 values are in the table above.

## Supplementary hazard probe (planted refs/replace, scratch fixture)

Raw discriminator: with `refs/replace/<README-blob>` planted, inherited-env
`git show <rev>:corpus/README.md` prints `knowledge/ghost.md` (forged); with
`GIT_NO_REPLACE_OBJECTS=1` it prints `knowledge/a.md` (real).

Repaired-byte behaviour (fixture commit `34693a9b3e656c75058690a00a84fdc2dcd1bd1d`, forged row
`ghost.md` + undefined `S999`):

```
check-index.py       base rc 1  MADO_INDEX: ... indexed=0/1 missing=1 dangling=1 coverage=0.0000/10
                     draft rc 0 MADO_INDEX: ... indexed=1/1 missing=0 dangling=0 coverage=10.0000/10
check-index-rows.py  base rc 1  MADO_INDEX_ROWS: ... rows=1 errors=1 warns=0
                     draft rc 0 MADO_INDEX_ROWS: ... rows=1 errors=0 warns=0
```

Evidence/freeze guards are proven by construction (census) plus byte-identical live outputs; the
declaration's auxiliary hazard-probe seat samples one repaired gate separately.

## Risks / notes

- Census classifies committed source construction, not runtime dataflow; the runtime env probe
  above and the hazard probe are the behavioural corroboration for this seat.
- The lane worktree currently also carries sibling edits in 8 other `quality/check-*.py` files
  (`check-anchor-cover`, `check-axis-scores`, `check-control-receipts`, `check-deliverables`,
  `check-landed-contract`, `check-round-outcome-first`, `check-session-material`, `check-wave-done`).
  This seat did not touch them. My four lane files still hash to their HEAD blobs, and the drafts
  derive from the HEAD/freeze blobs, so integration must apply drafts to frozen bytes, not to a
  sibling-mutated worktree.
- No packages installed (pacman paused); no commits, staging or lane git mutation by this seat.
- Scratch `/fast/scratch/hyaku/mado-r68/R68ExecGate2` removed (`rm -rf` rc 0, verified absent)
  before this report was written; fixture repos were removed by per-script `trap`.
