# RevPtrBefore — C2 before measurement re-run and pointer-extractor audit

Seat: reviewer (mado round 36, wave 1). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` (LANE).

All paths below are LANE-relative unless absolute. Quotes are verbatim from the runs I executed.

## 0. Running state observed during the audit

- The repo is jj-colocated (reflog: `HEAD@{0}: export from jj`), and a new commit
  `a3094c9` ("round-36: the repaired counters, the r36 ledgers, the discrimination receipts,
  the lesson, four criteria and one source row") was exported at 04:37 while I worked.
  The main-agent rebuild is running beside me; my seat is read-only and I touched nothing.
- `LOG.md` and `SCORECARD.md` are byte-identical between `4243d03` (freeze base) and
  `a3094c9` (`git diff 4243d03 a3094c9 --stat -- LOG.md SCORECARD.md corpus/lessons/`:
  only `corpus/lessons/round-36.md` added, 255 lines). The round-35 record audit below is
  therefore stable across both revisions.

## 1. Assigned command: re-run the C2 before measurement

Command (exact, from the prompt):

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/check-evidence-pointers.py --rev master
```

Quoted output (the exact lines my run printed, followed by `echo "EXIT=$?"`):

```
PRED-PTR-r36-v1 rev=master pointers_r35=8 dangling_r35=2 dangling_r35_closed=0 pointers_r36=0 dangling_r36=0 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=0 tip_axis_transcript=0 setup=missing-r36-sections verdict=TARGET_MISSED
dangling_r35: .ufo/waves/round-35/scratch/SimplifyCounter/
dangling_r35: .ufo/waves/round-35/scratch/MutC1Drop/mutants/
tip_axis: none
EXIT=1
```

Notes:

- `--rev master` is a moving name: at my 04:40 run, `master` = `dbf8b57` (the freeze commit);
  by now `master` = `a3094c9`. The four revision-derived observables are identical at both
  (`LOG.md`/`SCORECARD.md` unchanged; the round-36 lesson adds only `dangling_r36` inputs,
  and there are no round-36 sections yet).
- At the freeze, `master` was `4243d03` (the spot-check commit, per registration.md line 4).
  Vertbatim check of the frozen receipt (`receipts/before-pointers.txt` at the freeze):
  `pointers_r35=8 dangling_r35=2 dangling_r35_closed=0 pointers_r36=0 dangling_r36=0
  inherited_dirty=10 scratch_tracked=124 scratch_disposition_ok=0 tip_axis_transcript=0
  setup=missing-r36-sections verdict=TARGET_MISSED` — with the ten dirty paths listed below it.

## 2. The four before-defects named in the registration — findings

The registration names five before observables. Findings per observable:

| Observable | Frozen receipt (4243d03) | My re-run | Verdict |
|---|---|---|---|
| `dangling_r35` | 2 | **2** (exact same two paths) | **PASS — confirmed** |
| `dangling_r35_closed` | 0 | 0 | PASS — confirmed |
| `inherited_dirty` | 10 | **0** | **FAIL — NOT reproducible** (see below) |
| `scratch_disposition_ok` | 0 | 0 | PASS — confirmed |
| `tip_axis_transcript` | 0 | 0 | PASS — confirmed |
| `setup` | missing-r36-sections | missing-r36-sections | PASS — confirmed |

### 2.1 `dangling_r35=2` — confirmed exactly

My run printed exactly:

```
dangling_r35: .ufo/waves/round-35/scratch/SimplifyCounter/
dangling_r35: .ufo/waves/round-35/scratch/MutC1Drop/mutants/
```

Both are in the round-35 LOG.md sections (lines 2003 and 2020) and both fail
`git ls-tree -r --name-only 4243d03` (`git cat-file -e` fails for both paths). No other
extracted pointer is dangling at 4243d03 (see §3). `dangling_r35_closed=0` because no
correction pair exists in a round-36 LOG section (none exists).

### 2.2 `inherited_dirty=10` — confirmed as recorded, but NOT reproducible

The `inherited_dirty` observable counts `git status --porcelain` lines for the ten
`INHERITED_PATHS` (~ the live work tree, not the `--rev` tree. The frozen receipt recorded
10 at the freeze; my re-run of the same command prints `inherited_dirty=0`, because the ten
paths are now clean (eight modified files reverted to committed bytes, two untracked scratch
dirs removed — the dirs are gone from disk: `ls -d .ufo/waves/round-35/scratch/RevQuoteS203/`
→ "No such file or directory").

Evidence the ten were dirty at the freeze: the frozen `before-pointers.txt` lists them verbatim
(8 × ` M ` + 2 × `?? `). Evidence they are clean now:
`git status --porcelain -- <the ten paths>` prints nothing (empty output), and the live file
bytes equal the committed bytes (`md5sum` of `RevC1Tip.md` at dbHEAD == at `4243d03`).
The freeze commit `dbf8b57` did not commit them (`git show --stat dbf8b57 -- .ufo/waves/round-35/`
is empty); the paths were resolved by a later `jj export` (the work-tree rewrite at 04:31,
mtime 04:31:47 on the eight files), which also delivered `a3094c9`.

Consequence: the before reading `inherited_dirty=10` is a work-tree artifact, not a committed
measure. The same command at the same commit on a clean clone prints `inherited_dirty=0` —
so the gate's `inherited_dirty` observable is trivially satisfiable by a clean checkout and
cannot distinguish a real repair from a pristine tree. This is a do-nothing hazard on the
C2 claim's path (the gate itself penalizes nothing for it: `met` only requires
`inherited_dirty == 0` at run time).

The live receipt has already been amended by the main agent to record this exactly
(uncommitted diff in `receipts/before-pointers.txt`: the 10-line dirty listing replaced by a
comment noting the live-tree reading and a re-run at `rev=4243d03` with
`inherited_dirty=0`). I did not see the original 10-line freeze listing disappear from any
committed byte; the committed freeze version at `dbf8b57` still carries it.

### 2.3 `scratch_disposition_ok=0`, `tip_axis_transcript=0`, `setup=missing-r36-sections` — confirmed

- `scratch_disposition_ok=0`: no round-36 lesson exists (`corpus/lessons/round-36.md` absent
  at the freeze; `git show 4243d03:corpus/lessons/round-36.md` fails). No disposition line.
- `tip_axis_transcript=0`: no `quality/receipts/axis-<40hex>.txt` at the freeze/dbf8b57
  (`git ls-tree -r --name-only <rev> -- quality/receipts/` has no `axis-*.txt`); the run
  prints `tip_axis: none`.
- `setup=missing-r36-sections`: there are no `## Round 36` sections in `LOG.md`/`SCORECARD.md`
  and no lesson at the freeze revision. The run prints exactly that token and `TARGET_MISSED`,
  exit 1, per the PRED-PTR-r36-v1 spec.

## 3. Pointer-extractor audit (hand check)

I extracted every backticked token from the round-35 sections of `LOG.md` (three `## Round 35`
sections, lines 1999–2110) and `SCORECARD.md` (one `## Round 35` section, lines 2161–2235) at
`4243d03`, replicating the gate's `sections()`/`pointers()`/`pointerish()` logic, and compared
with the gate's `pointers_r35=8`.

### 3.1 Extracted set (8 unique, matches `pointers_r35=8`)

| # | Pointer | Source | Resolves at 4243d03? |
|---|---|---|---|
| 1 | `.ufo/waves/round-35/c1/count.py` | LOG:2001,2019 | yes |
| 2 | `.ufo/waves/round-35/scratch/SimplifyCounter/` | LOG:2003 | **no** (dangling) |
| 3 | `.ufo/waves/round-35/w1/reports/SimplifyCounter.md` | LOG:2014 | yes |
| 4 | `.ufo/waves/round-35/scratch/MutC1Drop/mutants/` | LOG:2020 | **no** (dangling) |
| 5 | `.ufo/waves/round-35/w1/reports/MutC1Drop.md` | LOG:2033 | yes |
| 6 | `corpus/lessons/round-34-verifier-spotcheck.md` | LOG:2037 | yes |
| 7 | `corpus/knowledge/idle-lock-never-asked-r12.md` | LOG:2053 | yes |
| 8 | `.ufo/waves/round-35/registration.md` | SC:2163 | yes |

Exactly 2 of 8 are dangling; both are the two paths ** registration and the R35 spot-check
(D5). No over-counts: every extracted token is a backticked lane path, and no token appears
twice in the set.

### 3.2 Misses — lane-relative evidence pointers the extractor skips

The gate's `pointerish()` requires the token to start with
`(?:\.ufo|corpus|quality|tools|scripts|considerthese)/`. The following backticked tokens in
the round-35 record are lane-relative evidence pointers that the extractor does **not**
extract:

1. LOG:2011 `c1/clauses.json` — the committed clause ledger path (resolves as
   `.ufo/waves/round-35/c1/clauses.json`; exists). Skipped: no leading prefix.
2. LOG:2051 `ledger/RevFrozenBlobs-r35.md` — the round-35 C2 ledger receipt path (resolves as
   `.ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md`; exists). Skipped: no leading prefix.
   This is precisely the record the C2 claim's ledger rule hinges on.
3. LOG:2053 `idle-lock-chain-armed-r14.md` — one of the three adopted knowledge entries
   (resolves as `corpus/knowledge/idle-lock-chain-armed-r14.md`; exists). Skipped: no
   `corpus/` prefix in the token.
4. LOG:2054 `idle-lock-offered-in-the-bar-r15.md` — same (resolves as
   `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md`; exists). Skipped.
5. SC:2176 `controls-content/` — the crib directory pointer (the round-35 counter cribs live
   at `.ufo/waves/round-35/controls-content/`; resolves as a directory). Skipped: prefix
   `controls-content/` is not in the allowlist, and the C1 counter-crib citation uses the
   relative form.
6. SC:2176 `python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json`
   — a counting-command line, not a pointer, but its embedded backticked content would not be
   extracted anyway (contains spaces); harmless.

None of these misses changes the verdict (all exist, so they are not dangling), but the
extractor's coverage claim ("every lane-relative evidence pointer cited by the round-35 LOG.md
entry and SCORECARD.md sections") is narrower than its enumerations: the two cited dangling
paths are found, while 4–5 non-dangling lane pointers are silently uncounted. The extractor
also does not count `LOG.md`/`SCORECARD.md` themselves (root files are lane-relative but no
prefix), nor `corpus/lessons/round-35.md` (not cited in the round-35 sections).

### 3.3 The two "over-count" candidates are correct

Line 2055 `shokuknow/merge/mado/` and SC:2176 `merge/mado/` are campaign-package paths, not
lane paths — correctly excluded. Line 2040 `RevFrozenBlobs.md` is a seat-report filename, not
a lane path — correctly excluded (it is the *name* of the file whose lane path is
`.ufo/waves/round-35/w2/reports/RevFrozenBlobs.md`, which the round-35 record never cites).

## 4. Verdicts

| Item | Verdict |
|---|---|
| Re-run command executed exactly | PASS |
| `dangling_r35=2` with the exact two paths (SimplifyCounter/, MutC1Drop/mutants/) | **PASS** |
| `inherited_dirty=10` with the ten paths | **CONFIRMED AS RECORDED, NOT REPRODUCIBLE** (live work-tree measure; re-run prints 0; receipt amended honestly) |
| `scratch_disposition_ok=0` | PASS |
| `tip_axis_transcript=0` | PASS |
| `setup=missing-r36-sections` | PASS |
| Pointer extractor count `pointers_r35=8` | PASS — no over-counts, sets match |
| Pointer extractor completeness | **MISS** — 4 lane evidence pointers not extracted (clauses.json, ledger/RevFrozenBlobs-r35.md, two knowledge entries) |
| Gate do-nothing hazard | **FINDING** — `inherited_dirty` is work-tree-dependent; a clean checkout trivially passes it (also: an `?` path at the freeze was resolved by reversion/deletion, not by a committed repair at the freeze) |

Residual risk: the main-agent rebuild (running concurrently, in the same work tree, my
read-only seat) is itself the source of the amended receipt and of the clean work tree; I
recorded what I observed without proposing or performing any edit.

Verification gaps: I could not produce a byte-identical reproduction of the original
`inherited_dirty=10` listing (the work tree is clean), which is exactly the point of §2.2;
the freeze's committed receipt is the only committed record of that measurement.
