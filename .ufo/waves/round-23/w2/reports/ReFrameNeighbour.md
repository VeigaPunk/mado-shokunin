# ReFrameNeighbour — wave-2 falsify re-run of the CritFrameNeighbour C1 neighbour set

Verdict: **no regression. Tip strictly better than base on 3/3 neighbour cases.** Every case that
was base-false-observed at the base classifier (`cd9da20c…`) reports the executed global
`pacman -Q …` at the `observed` tier on the tip classifier (`41489991…` at
`2f1134f38930fc8b067d2d7f5bba126338faabdd`), with zero foreign `pacman -S …` rows at any tier and
zero unparsed counts. Under the closure rule ("any forbidden -S command at any tier on the tip is
a regression") the tip is clean: it emits no `-S` row at all on this set.

## What I did

1. Read `registration.md`, `w1/reports/CritFrameNeighbour.md`, and the critic's runner
   `w1/out/CritFrameNeighbour/measure.py` (sha256 `5dd070a24c1d9ae5ac90c4bb5be53a46c71302f6475be7a015170f00065d9637`).
2. Built a fresh scratch tree. The runner is unmodified, but it resolves its helper as
   `LANE = ROOT.parents[5]`, so I mirrored the `.ufo/waves/…` depth inside my scratch dir instead
   of a flat copy (a flat copy would resolve the helper to `/.ufo/…`, which does not exist):

        S=/fast/scratch/hyaku/mado-r23/w2/ReFrameNeighbour
        rm -rf "$S"
        mkdir -p "$S/.ufo/waves/round-23/w1/out/CritFrameNeighbour" "$S/.ufo/waves/round-21/oracle"
        cp -a /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/out/CritFrameNeighbour/. \
              "$S/.ufo/waves/round-23/w1/out/CritFrameNeighbour/"
        cp /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/measure.py \
           "$S/.ufo/waves/round-21/oracle/measure.py"
        git -C /home/vgpnk/Projects/shokunin/mado-shokunin show \
          2f1134f38930fc8b067d2d7f5bba126338faabdd:tools/mado-tripwire.py > "$S/tool.py"
        cp /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/evidence/tool-base-cd9da20c.py \
           "$S/base-tool.py"

   sha256 verified: tip `tool.py` = `41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009`;
   base `base-tool.py` = `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`;
   helper = `4eb893d2337a4aa758d14c064a855032737c6e2b2b1239d7ca3502042c6c82da` (byte-exact copy of the
   lane's round-21 oracle helper); runner = `5dd070a2…9637` (unmodified); all three fixture sha256s
   match the wave-1 receipt byte-for-byte. No `__pycache__` in the tree.

3. Safety verification before running: the runner's `CHILD` fake-subprocess string is byte-identical
   to `round-23/repair/truth.py`'s (`CHILD identical: True`, sha256 of the CHILD text
   `c7d6aa4c8d8885012ed1ee1c8d1b77b56c38b27277f8f63dfaca9b8706538b19`). All fixture-code execution
   went through that recording fake `subprocess` under `python3 -I -S`; the classifier itself is
   only ever a static parser over the fixture files and ran as one `python3 -I` child per fixture
   with `RLIMIT_AS` 384 MiB and a 15 s timeout (`round-21/oracle/measure.py` lines 24–31), one
   child at a time. Note: the w1 `out/CritFrameNeighbour/` dir is untracked working-copy data
   (`git ls-files` is empty there); I measured the exact bytes named in the w1 receipt, verified by
   hash. No installs or updates were performed.

4. Ran the runner twice, sequentially, once per classifier:

        cd $S/.ufo/waves/round-23/w1/out/CritFrameNeighbour
        python3 -I measure.py --tool $S/base-tool.py   # exit 0, stderr empty
        python3 -I measure.py --tool $S/tool.py        # exit 0, stderr empty

## Results

Receipts (all under `/fast/scratch/hyaku/mado-r23/w2/ReFrameNeighbour/`):
`cases-base.json` (tool `cd9da20c…`), `cases-tip.json` (tool `41489991…`), plus raw stdout
`run-base.stdout.json` / `run-tip.stdout.json`. Both receipts: helper `4eb893d2…`, runner
`5dd070a2…`, Python 3.14.8. The w1 base receipt (`cases-w1-base.json`, saved before the runs)
matches my base run case-for-case, so the set did not drift between waves.

| Case | Truth executed | Truth forbid | Base rows (cd9da20c) | Tip rows (41489991) | Tip vs base |
|---|---|---|---|---|---|
| DecoratorWrapperCallsWrapped | `pacman -Q r23cf-deco-global` | `pacman -S r23cf-deco-foreign` | `host_mutation / pacman -S r23cf-deco-foreign / observed` | `package_query / pacman -Q r23cf-deco-global / observed` | **better** |
| HelperCalledFromLambda | `pacman -Q r23cf-lambda-global` | `pacman -S r23cf-lambda-foreign` | `host_mutation / pacman -S r23cf-lambda-foreign / observed` | `package_query / pacman -Q r23cf-lambda-global / observed` | **better** |
| HelperCalledFromMethod | `pacman -Q r23cf-method-global` | `pacman -S r23cf-method-foreign` | `host_mutation / pacman -S r23cf-method-foreign / observed` | `package_query / pacman -Q r23cf-method-global / observed` | **better** |

All rows carry evidence `observed`; scanner exit 1 with `error: null` and empty stderr on every
case (exit 1 = findings present, same as base). Unparsed: 0 everywhere, both tools.

Per-case reading:

- **Better (3/3, no ties).** On every case the base showed two defects: the foreign `pacman -S …`
  argv as a false `observed` `host_mutation`, and a silent miss of the true `pacman -Q …`. The tip
  fixes both at once: the foreign row is gone at every tier (no `-S` string appears in any tip row,
  which also satisfies the closure rule for these cases), and the executed command is reported at
  the `observed` tier.
- **Worse (0/3).** Base passed none of these cases, so there was no base-passing case the tip could
  have broken; nothing regressed.
- **Runner verdicts:** base run `base-false-observed` ×3 (matching wave 1); tip run
  `base-correct` ×3 (the runner keeps the `base-` prefix on candidates; it means candidate-correct:
  no foreign row, no unparsed, every executed command seen at `observed`).

## Honest-saturation and residual risk

- What is proven: the three neighbour shapes the wave-1 critic authored (helper invoked from a
  method parameter frame, from a lambda parameter frame, and through a decorator wrapper rebound to
  its `inner`) are false-observed at base and clean at the tip, on the same fixture bytes, through
  the same unmodified runner and helper.
- What is not proven here: the tip could reach this result by a shape-narrow rule that still leaks
  on a neighbour shape the critic did not author (e.g. a helper free name bound only in a
  comprehension or `except as` frame). That hunt was outside my assignment; the 12-case repair set
  (including `ForwarderPassesCallerArgument`, the overcorrection trap the critic flagged) and the
  no-harm guards are the L1's counters for it, and I did not re-measure them.
- Scope note: I did not run any other counter (repair measure, precision, corpus comparator); this
  report covers only the neighbour re-run assigned to wave 2.

Report: .ufo/waves/round-23/w2/reports/ReFrameNeighbour.md
