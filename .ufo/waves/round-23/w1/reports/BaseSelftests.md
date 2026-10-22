# BaseSelftests — C1 no-harm baseline: eleven legacy selftest suites re-measured at base

Seat: `MadoR23.BaseSelftests` · Date: 2026-10-22 · Judged on: operability

## Verdict

**PASS — 247/247 reproduced at the base classifier** (exit 0 on all eleven suites; every
run's `SELFTEST_SCRIPT_SHA256` equals `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`;
no harness defect observed; outputs byte-identical across reruns). The round-22 claim
"eleven selftest suites 247/247" is independently confirmed at commit
`a28e4815aabfa85f55274884000fb2608355f8cf`.

## What was measured

Tool: extracted from the pinned base commit, not the working copy:

```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show a28e4815aabfa85f55274884000fb2608355f8cf:tools/mado-tripwire.py \
  > /fast/scratch/hyaku/mado-r23/BaseSelftests/base-tool.py
sha256sum /fast/scratch/hyaku/mado-r23/BaseSelftests/base-tool.py \
          /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py
```

Both sha256 `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84` — the
scratch copy and the lane working-copy tool are byte-identical at base, so either path
would measure the same classifier; the scratch copy was used for every run (no
lane-relative path needed).

Fixture provenance: all eleven suite dirs live under lane `.ufo/waves/round-{17,18,19}/tripwire/…`
(committed; enumerated via `git ls-tree -r --name-only a28e4815…`). The lane working copy
was checked clean for those trees before running:

```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain -- \
  .ufo/waves/round-17 .ufo/waves/round-18 .ufo/waves/round-19
# empty output → fixtures match the index (base content)
```

Harness flags checked first (`--help`, exit 2 usage banner): single harness
`mado-tripwire.py --selftest DIR`, each suite = one directory with `expected.json`
(schema `mado-tripwire-selftest-v1`). Each case spawns a sequential child
`python3 -I <script> --scan|--frozen …` over the committed fixture data; no concurrent
processes at any point.

## Per-suite runs (exact command form, one process at a time)

```
prlimit --as=402653184 --cpu=15 python3 -I /fast/scratch/hyaku/mado-r23/BaseSelftests/base-tool.py \
  --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/<suite-path>
```

| suite | exit | count | sha pin | wall |
|---|---|---|---|---|
| round-17/tripwire/core | 0 | 9/9 | ok | 0.41s |
| round-17/tripwire/compound | 0 | 16/16 | ok | 0.69s |
| round-17/tripwire/hardening | 0 | 33/33 | ok | 1.37s |
| round-17/tripwire/w2-regressions | 0 | 30/30 | ok | 1.24s |
| round-18/tripwire/r18-failsafe | 0 | 1/1 | ok | 0.08s |
| round-18/tripwire/frozen | 0 | 31/31 | ok | 1.24s |
| round-19/tripwire/r19-bashcvar | 0 | 45/45 | ok | 1.82s |
| round-19/tripwire/r19-helperfn | 0 | 34/34 | ok | 1.41s |
| round-19/tripwire/r19-vcs | 0 | 17/17 | ok | 0.74s |
| round-19/tripwire/r19-frozen-f1f2 | 0 | 13/13 | ok | 0.56s |
| round-19/tripwire/r19-installers | 0 | 18/18 | ok | 0.82s |
| **total** | | **247/247** | | |

Every per-suite count equals the round-22 legacy summary
(`.ufo/waves/round-22/evidence/resume/legacy-selftests-summary.json`) exactly, case names
included. All stderr files are empty (0 bytes). Caps were never approached: worst wall
time 1.82 s against the 15 s CPU cap; no allocation-related failure under the 384 MiB
`--as` cap.

## Determinism and tamper checks

- Rerun of the two most complex suites (`r19-bashcvar`, `frozen`) under identical caps:
  exit 0, stdout **byte-identical** to the first run (saved as `*.rerun.stdout`), stderr
  empty. No nondeterminism observed.
- Every run's `SELFTEST_SCRIPT_SHA256` line compared externally to
  `cd9da20c…ea84` — matched 13/13 runs (11 primary + 2 reruns). The scratch copy was
  never modified between runs.
- The frozen suite's own tamper cases (`tampered-input-byte`, `missing-input`,
  `symlink-input`, `path-traversal`, …) all pass, i.e. the classifier's digest-pinned
  frozen replay rejects tampered inputs as expected.

## Harness observations (no defect blocking the claim)

1. `SELFTEST_SCRIPT_SHA256` is **informational**: `run_selftest` prints the sha of the
   running script but does not itself assert it; tamper detection inside the suite comes
   from frozen-mode digest pinning. External comparison (as done here and by the legacy
   runner) is what turns the line into a tamper guard. Worth knowing for anyone wiring
   new suites.
2. Per-case children get `subprocess.run(..., timeout=120)` from the harness while the
   outer cap is `--cpu=15`; the 120 s wall timeout is unreachable in practice because the
   CPU cap fires first for runaway children. No conflict observed, noted for completeness.
3. `--help` is not a real flag: it falls into the usage branch and emits a
   `could_not_evaluate` verdict with exit 2. Flag discovery only; harmless.

## Raw evidence

All under `.ufo/waves/round-23/w1/out/BaseSelftests/`:
`round-17_tripwire_core.stdout/.stderr`, … (11 suites × stdout+stderr),
`round-19_tripwire_r19-bashcvar.rerun.stdout`, `round-18_tripwire_frozen.rerun.stdout`,
and `rerun-manifest.json` (per-suite command, exit, counts, sha-ok flag, wall time).

## Scope notes

- No host changes; no tool installs or upgrades performed (nothing needed).
- Lane untouched except this report and the `out/BaseSelftests/` artifacts; no jj/git
  state mutations (only read-only `git show`/`ls-tree`/`status`/`sha256sum`).
- Leaf seat: no subagents spawned; suites run strictly one process at a time.
