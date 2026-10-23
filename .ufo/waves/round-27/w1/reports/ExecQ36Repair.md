# ExecQ36Repair — routed defects 2 and 5 (round-26 spot-check §7: M26-9 seeds, `.txt` receipts)

Seat: `MadoR27.ExecQ36Repair` (leaf). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, branch master,
lane HEAD `a4dc0da` when the receipt was generated (it advanced from `7c25697` during the seat: the L1's
round-27 C1 counter v2 commit — not this seat's write); every lane-history run is pinned to the declared
round tip `5ddc5885`. No git/jj write command was run in this lane or in the fleet repo; the only lane
paths written are the two deliverables below plus this report.

## Deliverables

| path | sha256 | bytes | lines |
|---|---|---|---|
| `quality/check-control-receipts.py` | `2233db1d489fa325c3b4bd9b5b1dccc68eb9311864a0d975303907463fa65af2` | 9860 | 207 |
| `.ufo/waves/round-27/quality/q36-successor-receipts.txt` | `5c162fe5e31e85e4d15fcbf0dbd3f0937ef75e9371fb20ca1652becb13bd6e7b` | 59229 | 627 |

Scratch runner (not a lane file; the assignment named only the two outputs): 
`/fast/scratch/hyaku/mado-r27/q36/run_fixtures.py`, sha256 `f32ea076e9764e49f1e67ae32c138dbb8d95476955298a3f358cf4683e42fe26`.
All synthetic git repositories and mutated checker copies it builds live under
`/fast/scratch/hyaku/mado-r27/q36/{repos,checkers}`; nothing else under `/fast` is touched.

The round-26 checker was **not** edited: its current sha256 is
`351127bd0d735665f899129fa3ad408b8d23c85d9f71969b44e3b63d86b6d3b4`, byte-identical to the value its own
`q36-mutants.txt:4` recorded (the receipt records this comparison).

## Behaviour (what the successor is)

Base: `.ufo/waves/round-26/quality/check-control-receipts.py`, read in full. Unchanged rule: exit 0 only
if, at TIP, the **oldest** commit that *adds* a qualifying receipt under
`.ufo/waves/round-N/controls/` (`git log --reverse --diff-filter=A`, committer `%ct`) is **strictly
before** the data registry's `createdAt` (never `updatedAt`), and every named shape is covered; exit 1
otherwise; exit 2 when history cannot be evaluated (bad tip, `ls-tree` failure, no adding commit,
registry absent, `createdAt` unreadable). `--any-md` and `--counter-sha` (first line only, full 64 hex)
are kept.

Two additions (the routed defects):

1. **Repair 5 — receipt selection by path, not format.** `--receipt-glob PATTERN` (repeatable) replaces
   the hard-coded `.md` filter. Defaults are `*.md` and `*.txt`; a pattern matches a path under
   `controls/` when it matches the controls-relative path **or** that path's basename (case-insensitive,
   `*` crosses `/`), so the defaults reach any depth, including `.ufo/waves/round-26/controls/v2/*.txt`.
   The `CONTROL ` / `# Control` marker line is required **only of markdown receipts**; a verbatim counter
   log carries `exit=` and no markdown marker, so demanding one would keep defect 5 red. `--any-md`
   keeps its meaning. `excluded_by_glob=N` is printed.
2. **Repair 2 — seed accounting (M26-9).** `--seeds N` (default 1, positive integer) fails (exit 1)
   unless **every named shape** has at least N distinct qualifying receipts. A receipt counts toward a
   shape when its **file name** contains one of that shape's `|` alternatives (case-insensitive). The
   verdict line gains `seeds_short=<shape>(count<N),...` and a `shape_counts=` line; `shapes_missing=`
   keeps its round-26 meaning (zero receipts for that shape). New fields are appended to existing lines,
   so every stored round-26 receipt line stays a substring of the current line (legacy parity below is
   the test of that).

Usage:

```
python3 -I quality/check-control-receipts.py --round N --data-registry PATH [--repo PATH] [--tip REV]
        [--shapes S1,S2,...] [--seeds N] [--receipt-glob PATTERN ...] [--any-md] [--counter-sha SHA]
```

The round-27 pre-data invocation this enables (stated in the receipt, **not** scored there because the
wave-1 receipts are still untracked at the tip):

```
python3 -I quality/check-control-receipts.py --round 27 --seeds 2 \
  --data-registry .ufo/waves/round-27/<data-wave>/reports/swarm-registry.json \
  --shapes <registered shapes> --tip <landing rev>
```

CLI guards exercised: `--seeds 0` and `--seeds abc` are rejected by argparse with exit 2.

## Exact commands and retained evidence

Receipt generation (single command, 7.7 s wall, exit 0):

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && \
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 --as=4000000000 -- \
  python3 -I -B /fast/scratch/hyaku/mado-r27/q36/run_fixtures.py \
  --out .ufo/waves/round-27/quality/q36-successor-receipts.txt
```

The runner builds 24 synthetic repositories, runs the pristine successor plus 9 single-locus mutants on
each (240 runs), then runs the successor and the read-only round-26 checker on the real lane. Final
lines of the receipt:

```
QS36SEEDS lane_runs=5 fixtures=24 mutants_killed=9/9
Q36SUCCESSOR verdict=PASS
```

### The two mandated round-26 cases (read-only git at `5ddc5885`)

* `--round 26 --data-registry .ufo/waves/round-26/w2/reports/swarm-registry.json --shapes
  DoNothing,EmptyTable,EmptyTableZeroNodes,Junk,LabelKeyed,NaiveGrep,NoValidation,RootOnly,SnapshotCache,StaticDefault
  --receipt-glob 'v2/*.txt' --seeds 2` → **exit 1**, `receipts=10`, `order=ok gap_s=17`,
  `seeds_short=DoNothing(1<2),EmptyTableZeroNodes(1<2),Junk(1<2),LabelKeyed(1<2),NaiveGrep(1<2),
  NoValidation(1<2),RootOnly(1<2),SnapshotCache(1<2),StaticDefault(1<2)` — one seed per v2 control.
  `EmptyTable` is not short at `2` because `K1EmptyTableZeroNodes.txt` contains that shape's name; that
  is the mandated file-name rule, not a hole.
* Same args with `--seeds 1` → **exit 0**, `order=ok gap_s=17 shapes_missing=- seeds_short=-`,
  `CONTROL_RECEIPTS verdict=PASS` (receipts committed `2026-10-23T09:16:22Z`, w2 `createdAt`
  `2026-10-23T09:16:39.175Z`).
* Same receipts against the **w1** registry → exit 1 `order=LATE gap_s=-1985` (chronology control: the
  pass above is the declaration plus the commit order, not a missing rule).
* Whole round-26 `controls/` tree, `--seeds 2` → exit 1 with only `EmptyTableZeroNodes(1<2)` short
  (`K2` logs share slugs such as `DoNothing`); `--seeds 1` → exit 0 PASS.

### Before (the routed defects, reproduced on lane bytes)

* round-26 checker on round 26, default flags: exit 1, `receipts=0`,
  `reason=no-receipt-under-.ufo/waves/round-26/controls/` — defect 5.
* round-26 checker plus `--seeds 2`: exit 2,
  `error: unrecognized arguments: --seeds 2` — defect 2.

### Legacy parity (stored receipts, unchanged behaviour)

* `--round 24 --data-registry .ufo/waves/round-24/w1/reports/swarm-registry.json --tip 41cc04c8
  --any-md` → exit 1, `order=LATE gap_s=-1083`, `shapes_missing=EmptyArray|AllFalse,Echo,LabelKeyed`;
  `parity_with_q36-red-round24.txt=ok`.
* `--round 25 --data-registry .ufo/waves/round-25/a3w2/reports/swarm-registry.json --tip ef94763c`
  → exit 0, `order=ok gap_s=7695 shapes_missing=-`; `parity_with_q36-green-round25.txt=ok`.

### Synthetic fixtures — one per failure branch (24 total; 9 green, 11 red, 4 unevaluable)

Green (exit 0): `green-one-seed`, `green-two-seeds` (two seeds/shape at `--seeds 2`),
`green-txt-glob` (bare `.txt` logs, no marker, default globs), `green-txt-v2-seeds2` (two `.txt` seeds
per shape under `controls/v2/`), `green-any-md`, `green-glob-subdir` (glob scopes to `v2/*.txt`, later
`.md` decoy ignored), `later-receipt` (newest adding commit must not supply the time),
`updated-at` (`updatedAt` before the receipt, `createdAt` after — only `createdAt` decides),
`sha-green`.

Red (exit 1): `red-seeds-short` (the `green-one-seed` set at `--seeds 2`), `red-seeds-partial` (only the
short shapes reported), `red-md-marker` (markdown without a marker), `red-glob-md-only`
(`--receipt-glob '*.md'` rejects the `.txt` set), `red-glob-late` (glob scopes to a late `v2/*.txt`
commit; an ignored glob would pick an early `.md` and pass), `equal-time` (`<=` would pass),
`missing-shape`, `sha-not-first-line`, `sha-prefix`, `sha-late`, `red-no-receipts-py` (control `.py`
sources are not receipts).

Unevaluable (exit 2): `bad-tip`, `missing-registry`, `unreadable-createdAt`, `no-adding-commit`
(receipts reach the tip only through a `--no-ff` merge commit, so the default log pass reports no adding
commit).

### Mutant kill table (each mutant applied alone to a scratch copy; green baseline must not move)

| mutant | locus | killer fixture | pristine → mutant |
|---|---|---|---|
| M1-seeds-ignored | L195 seed rule dropped | red-seeds-short | 1 → 0 |
| M2-seeds-collapsed | L192 seed count collapsed to one | green-two-seeds | 0 → 1 |
| M3-glob-ignored | L136 glob never applied | red-glob-late | 1 → 0 |
| M4-basename-only | L99 patterns matched by basename only | green-glob-subdir | 0 → 1 |
| M5-marker-all-formats | L143 marker demanded of `.txt` (restores defect 5) | green-txt-glob | 0 → 1 |
| M6-marker-ignored | L143 marker predicate dropped | red-md-marker | 1 → 0 |
| M7-newest-receipt | L156 `--reverse` removed | later-receipt | 0 → 1 |
| M8-nonstrict | L185 `<` becomes `<=` | equal-time | 1 → 0 |
| M9-sha-prefix | L92 12-hex prefix match | sha-prefix | 1 → 0 |

9/9 killed; every mutant leaves `green-one-seed` at exit 0, so no kill is collateral.

## Host safety

No Hyprland, tinywl, bwrap or oracle invocation appears in any transcript; this seat never started a
compositor, never set `WAYLAND_DISPLAY`/`HYPRLAND_INSTANCE_SIGNATURE`, never touched `/dev/dri`, and ran
no `hyprctl`. Only `git`, `python3`, `df` and `sha256sum` were executed, each under `timeout` and (for
the runner) `prlimit --core=0 --as=4000000000`. Current host Hyprland coredump count:
`coredumpctl list … | grep -c /usr/bin/Hyprland` = 1338; delta from this seat = 0 by construction (no
compositor process was ever spawned). No background job or service survives this seat; the one
backgrounded grep inherited from an earlier shell was read-only.

No tool install or upgrade was needed or made (python 3.14.8, git 2.56.0, all preinstalled). No pacman
transaction was attempted.

## Risks and limits

1. **File-name substring counting is inclusive by construction.** `EmptyTable` also counts
   `K1EmptyTableZeroNodes.txt`, so at `--seeds 2` over round-26's v2 set nine of ten shapes are short,
   not ten. This is the rule the assignment states; a token-exact variant would be a different rule and
   was not smuggled in.
2. **Default globs widen the legacy runs to `.txt`.** Round-24/25 were re-run and their stored lines
   still match (`parity=ok`, exit 1/0); round-24 has no `.txt` receipts, and the widened filter only adds
   files, so no stored verdict moved. A future `.txt` receipt older than a round's `.md` receipts would
   now set the oldest receipt commit — that is intended for future rounds, and the round-24/25 receipts
   are byte-for-byte parity-checked here as the guard.
3. **Markdown receipts still need a marker.** A future wave that keeps control logs in `.md` without a
   `CONTROL ` / `# Control` line must pass `--any-md`, exactly as in round 26.
4. **Fixture runner is scratch-side.** The assignment named only the checker, the receipt and the
   report as lane outputs, so the fixtures/runner stay at
   `/fast/scratch/hyaku/mado-r27/q36/run_fixtures.py` (sha256 pinned in the receipt, and every fixture's
   commits, dates, file names, args and expectations are printed inside the receipt so it reads
   standalone). Promoting the runner to `quality/q36-fixtures/` would be a data-wave decision; not done
   here to stay inside the assigned paths.
5. **Round-27 is not scored here.** At lane HEAD `a4dc0da` only one round-27 shape (`K1FlatScan`) has
   committed `-seed1`/`-seed2` receipts; the other wave-1 receipts are still untracked, and no round-27
   data registry exists yet, so the gate is not scoreable and no verdict is claimed; the receipt states
   the invocation only.
6. **Data-registry choice is a declaration.** Round-26's v2 controls landed 17 s before the w2
   registry's `createdAt` and ~33 min after w1's; the receipt runs both, so the pass and the
   `gap_s=-1985` LATE control are both visible.

No blockers. The gate this seat was asked to build is red on the two routed defects at their base
behaviours, green on the repaired surface, and 9/9 on its own mutants.

VERDICT: repairs 2 and 5 landed in `quality/check-control-receipts.py`; round 26 `--seeds 2` over the v2
controls exits 1 (one seed per control), round 26 `--seeds 1` exits 0 with `order=ok gap_s=17`; 24
fixtures, 9/9 mutants, legacy parity ok — evidence in
`.ufo/waves/round-27/quality/q36-successor-receipts.txt` (`Q36SUCCESSOR verdict=PASS`).
