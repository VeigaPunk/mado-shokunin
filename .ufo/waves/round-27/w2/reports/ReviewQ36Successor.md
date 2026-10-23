# ReviewQ36Successor — quality/check-control-receipts.py vs round-26 spot-check §7 defects 2 and 5

Reviewer: MadoR27.ReviewQ36Successor (leaf, no spawns, read-only lane except this report). No tools installed.
No compositor, Hyprland, tinywl or bwrap process started; no coredump delta to report. No LSP device exists in this
seat's tool inventory, so caller/definition checks were done by direct file read + execution, not by a language
server; recorded here per reviewer contract.

## Verdicts (short)

- **Does it do what it says: YES.** Every docstring rule sentence is implemented as written and fixture-backed; the
  two routed defects are genuinely repaired. Worktree bytes = tip bytes = the receipt's pinned sha.
- **Is the substring shape rule a defect: YES — MEDIUM.** `EmptyTable ⊂ EmptyTableZeroNodes` credits one control's
  receipt to another shape's seed count, masking exactly the M26-9 shortfall repair 2 exists to catch. Disclosed in
  the receipt text, and not verdict-flipping in any recorded run (including mine below), but it is a false-pass
  channel in the seed clause, demonstrated live in this round as `DoNothing:4`.
- **Round-27 run (assigned command): verdict=FAIL, exit 1 — `seeds_short=FlatScan(1<2)`.** Chronology holds
  (oldest qualifying receipt 10:38:49Z < w2 registry createdAt 10:52:15.411Z). This is an accurate diagnosis, not a
  checker malfunction: under `v2/*.txt`, FlatScan's only receipt is `v2/K1FlatScan-L1pilot.txt`; its two seeds are
  v1-counter receipts at the controls root (`K1FlatScan-v1-seed{1,2}.txt`), correctly excluded by the glob.

## 1. Defect-map check (spot-check §7, routed defects 2 and 5)

- **Defect 2 / M26-9** ("teach the Q36 successor to count seeds per control shape") → repaired: `--seeds N`
  (default 1, positive-int validated, quality/check-control-receipts.py:71-79, :88-93) and per-shape counting at
  :186-194; `seeds_short=` reports each `shape(count<required)`. Receipt fixtures `red-seeds-short`,
  `red-seeds-partial` and mutants M1/M2 kill both neglect directions (seed rule dropped; count collapsed to 1).
- **Defect 5** ("Q36 successor exits 1 on round 26 (.txt receipts): add a receipt-path option") → repaired:
  `--receipt-glob` (repeatable, default `*.md,*.txt`), matched against the controls-relative path OR basename
  (:95-99), `*` crossing `/` (fnmatch), case-insensitive. Receipt shows the old checker failing the round-26 tree
  (`r26-checker-on-txt`, receipts=0) and the successor passing the same bytes with defaults (`r26-v2-seeds1`,
  GREEN). Depth behavior is mutant-killed both ways (M3 glob-ignored, M4 basename-only) and scoped both ways
  (`red-glob-late` fails when the glob selects only late receipts; `green-glob-subdir` passes when it selects only
  early ones).
- Marker rule (CONTROL marker demanded of `.md` only, `--any-md` kept), `--counter-sha` full-64 first-line match,
  strict `<` chronology, oldest-receipt-commit-wins, updatedAt ignored, exit codes 0/1/2: all as documented, each
  fixture-backed in the receipt (`equal-time`+M8, `later-receipt`+M7, `updated-at`, `sha-prefix`+M9, `bad-tip`,
  `missing-registry`, `unreadable-createdAt`, `no-adding-commit`). 24/24 fixtures expected==actual, 9/9 mutants
  killed (`QS36SEEDS lane_runs=5 fixtures=24 mutants_killed=9/9; Q36SUCCESSOR verdict=PASS`).
- Print-order parity claim verified: round-26 checker's header line
  (`.ufo/waves/round-26/quality/check-control-receipts.py:106`) is `tip= round= receipts= counter_sha=
  excluded_by_counter_sha=`, and the successor appends `receipt_glob= excluded_by_glob= seeds=`
  (:149-151) — the stored round-26 line remains a substring.
- Read-only claim verified: only `rev-parse/ls-tree/show/log` via subprocess with `GIT_OPTIONAL_LOCKS=0` and
  `GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE` unset (:60-65); nothing writes.

## 2. Receipt integrity

`successor=…/quality/check-control-receipts.py sha256=2233db1d489fa325c3b4bd9b5b1dccc68eb9311864a0d975303907463fa65af2`
— recomputed over the worktree file: identical; `git diff --stat 2fdca5ca -- <file>` empty, so tip bytes match too.
Receipt's lane runs are history-only (round-26 at 5ddc5885; round-24/25 parity at stored tips) and its synthetic
repos live under /fast/scratch/hyaku/mado-r27/q36 — consistent with the seat contract; no subject sha/AST pin, no
W-blocklist, no path/environment/process sniffing (it is a git-history checker and its fixtures declare their commits).

## 3. Findings by severity

**MEDIUM — substring shape attribution false-passes the seed clause** (`counts[shape] = n` at :190-192, where
`n = sum(1 for name in names if any(o in name for o in opts))`, names lowercased basenames).
- Round-26 evidence, from the receipt's own `r26-v2-seeds2` run: `shape_counts=…,EmptyTable:2,EmptyTableZeroNodes:1`
  while `controls/v2/` contains exactly one true EmptyTable receipt (`K1EmptyTable.txt`); the second credit is
  `K1EmptyTableZeroNodes.txt` — a different control. M26-9's defect (one seed where two are registered) is therefore
  reported as satisfied for EmptyTable. That run still exits 1 (nine other shapes are short), so no recorded verdict
  flipped — but a round whose only shortfall were EmptyTable would false-pass.
- Round-27 live evidence (my run): `DoNothing:4` = `K1DoNothing-seed{1,2}.txt` (C1) + `K2DoNothing-seed{1,2}.txt`
  (C2) under one glob — cross-claim crediting that inflates the C1 seed count from 2 to 4. The `|` alternative
  syntax already exists for genuine aliases; substring is not needed for that.
- Mitigations present: disclosed in the receipt ("EmptyTable is the lone shape at 2 because 'K1EmptyTableZeroNodes'
  contains it"); in the assigned invocation the verdict is invariant to the defect — exact-token matching would give
  DoNothing:2 (still ≥2) and FlatScan:1 (still short). Recommended fix: match the alternative as a dash/underscore-
  delimited component of the basename (e.g. `(^|[-_.])NAME([-_.]|[0-9]|$)`) instead of `in`.

**LOW — chronology anchor may be a non-seed control log.** "Qualifying receipt" is any glob-selected file, so the
printed `receipt_commit` can come from a pilot or summary file: my run's `receipt_commit=a4dc0da` is
`v2/K1FlatScan-L1pilot.txt` (10:38:49Z), not a seed receipt. The guarantee still holds — the earliest true v2 seed
commit (e8eae62, 10:52:01Z) also precedes createdAt 10:52:15.411Z — but a reader quoting `receipt_commit=` should
know it is oldest-qualifying, not oldest-seed. Documented behavior, caller-scoped by the glob.

**LOW — unreadable blobs silently dropped** (:142-144 `git show` failure → `continue`, uncounted). Fails safe
(shrunken set → more likely FAIL, and receipts=0 → FAIL), but a transient git error would present as
seeds_short rather than UNEVALUABLE.

**COSMETIC —** empty `--shapes` segments (trailing comma) become always-missing shapes rather than an argument
error; a timezone-naive registry `createdAt` would be read in local time (`fromisoformat` without tz). Both lane
registries use `Z`; neither can bite here.

## 4. Round-27 run (assigned command, executed verbatim)

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/check-control-receipts.py --round 27 \
  --data-registry .ufo/waves/round-27/w2/reports/swarm-registry.json --tip 2fdca5ca \
  --receipt-glob 'v2/*.txt' --seeds 2 \
  --shapes DoNothing,Junk,Echo,LabelKeyed,StaticBase,NaiveGrep,RootOnly,NoMerge,NoVariables,FlatScan
tip=2fdca5caaab6859386effbb8fa6acc5250c90633 round=27 receipts=39 counter_sha=- excluded_by_counter_sha=0 receipt_glob=v2/*.txt excluded_by_glob=100 seeds=2
receipt_commit=a4dc0da0394a committed=2026-10-23T10:38:49+00:00 data_registry=.ufo/waves/round-27/w2/reports/swarm-registry.json createdAt=2026-10-23T10:52:15.411Z
order=ok gap_s=806 shapes_missing=- seeds_short=FlatScan(1<2)
shape_counts=DoNothing:4,Junk:2,Echo:2,LabelKeyed:2,StaticBase:2,NaiveGrep:2,RootOnly:2,NoMerge:2,NoVariables:2,FlatScan:1
CONTROL_RECEIPTS verdict=FAIL
EXIT=1
```

Independently re-derived from `git ls-tree -r 2fdca5ca -- .ufo/waves/round-27/controls/`: v2/ holds exactly 39
`*.txt` files (21 K1 + 17 K2 + `L1-sealed-rescore-summary.txt`), matching `receipts=39`; per-shape recount matches
every printed count; FlatScan's only v2 receipt is the L1 pilot. The FAIL is therefore a true statement about the
tree at 2fdca5ca: FlatScan has no two v2-era seed receipts at that tip (v4/ carries only the three L1 pilots there;
the v4 two-seed re-scores required by PRED-C1-r27-v4 are not yet committed at this revision).

**Verdict line:** `RUN round-27 tip=2fdca5ca glob=v2/*.txt seeds=2 verdict=FAIL exit=1 seeds_short=FlatScan(1<2) order=ok — checker behaves as documented; diagnosis accurate`

## 5. Residual risk and verification gaps

- Did not re-execute the 24 fixtures or 9 mutants myself; the receipt is the evidence and I verified its pinned sha
  matches tip bytes plus re-derived the live selection/counts by hand. A skeptical L1 can rerun `run_fixtures.py`
  (path in the receipt) for a fresh-seed confirmation.
- The substring defect's false-pass is latent: it flips no recorded verdict today, but any future round whose shape
  list contains a name that is a substring of another control's slug inherits it silently.
- Chronology uses committer time (`%ct`), so a history rewrite could shift it; appropriate for this lane, noted for
  the record.
- Defect 5's second half (landing MutSelftest/MutQ37 survivor witnesses as committed fixtures) is a different item's
  scope; not judged here.
