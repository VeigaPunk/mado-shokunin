# RerunMutantsOut — partial

The `--out` change itself holds under every assigned probe (bare writes nothing; `--out` inside
the read worktree is refused in 10 spellings; `--force-lane-receipt` writes; `.summary` reproduces
exactly). Two claims made *around* the change are overstated: the w1 diff-size sentence (both
instances), and the shipped docstring's unqualified "cannot silently overwrite the lane receipt".
An unguarded inherited `--workdir` channel also remains.

Tip under attack: `01b80946d92b26370d3012a7da655d00dd135154` (HEAD; worktree clean at clone time).
Script bytes at tip: `595a6a9be8b8e6bc7b43043f293f7ac3afc1672cf2d756a0830e4e6af3766687`.
Committed lane receipt: `58929eeaf9e822042a43e45f2363885ce1b4094a3fa5e3531ca3e2845bb133e5`.

## Setup (no lane write; read-only git)

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/r19mm   # HEAD 01b80946, status clean
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/r19mm2
python3 -VV   # Python 3.14.8 (same as committed receipt environment)
git --version # 2.56.0 (same)
```

## Probe 1 — bare run writes nothing: HOLDS

```
cd /tmp/r19mm2 && touch /tmp/r19mm-out/marker2 && sleep 1
python3 -I .ufo/waves/round-18/measure-mutants.py --lane /tmp/r19mm2 \
  > /tmp/r19mm-out/bare2.json 2> /tmp/r19mm-out/bare2.err          # RC=0
find /tmp/r19mm2 -newer /tmp/r19mm-out/marker2 -printf '%y %p\n'   # (no output)
find /tmp/r19mm2 -name __pycache__ -o -name '*.pyc'                # (no output)
ls -d /tmp/mado-r18-mutants-* | wc -l                               # 2 before, 2 after (temp dir removed)
```

Mtime-level proof: nothing in the clone (worktree *or* `.git`) is newer than the marker; the clone
receipt is unchanged (`58929eea…`) and no `.tmp`/`__pycache__` appears. In `/tmp/r19mm` an earlier
`find -newer` did show `.git/index`, but that file was touched by my own intervening `git status`,
not by the script — the `r19mm2` probe has no git command between marker and `find`. stdout is one
parseable JSON document (`/tmp/r19mm-out/bare2.json`, 56,4xx B); stderr carries only the six
`M<n> BITES:` blocks. Wall time 2.3–3.3 s per full run, all runs rc 0.

## Probe 2 — `--out` inside the read worktree is refused: HOLDS (10 shapes)

All from `/tmp/r19mm`, all `rc=1`, `stdout_bytes=0`, refusal on stderr, elapsed **0.041 s**
(before archive/instruments — the check precedes `root = …` at `measure-mutants.py:537`):

| shape | result |
|---|---|
| absolute evidence path | `refusing --out /tmp/r19mm/.ufo/waves/round-18/evidence/refused-abs.json: inside the git worktree being read (/tmp/r19mm); pass --force-lane-receipt …` |
| relative `.ufo/…` (cwd = clone) | refused |
| `--out <clone>` (worktree itself) | refused |
| `<clone>/../<clone>/…` | normalised, refused |
| symlinked parent (`/tmp/r19mm-out/into-clone -> /tmp/r19mm/.ufo`) | refused |
| `/proc/self/cwd/…` | refused |
| the receipt itself | refused |
| symlink leaf (dangling, target inside) | `… /tmp/r19mm/.ufo/leaf-target.json …` refused |
| `<clone>/.git/…` | refused |
| `--lane` via symlink (`/tmp/r19mm-link`) or trailing `/.` | refused |

False positives: none observed. `--out /tmp/r19mm-out/outside.json` (sibling name sharing the
string prefix `r19mm`, not a path child) was written, rc 0 — the test is `worktree in out.parents`
on resolved paths (`:521-522`), not a string prefix. No refused file was created; the receipt
stayed `58929eea…`.

## Probe 3 — `--force-lane-receipt` writes: HOLDS

```
cd /tmp/r19mm
python3 -I .ufo/waves/round-18/measure-mutants.py --lane /tmp/r19mm \
  --out .ufo/waves/round-18/evidence/measure-mutants.json --force-lane-receipt   # RC=0
# pre 58929eea… → post 82282a7d58009f7d18ace0c570cddce8a765b12d65097ef25ebfdd016f3c1b62
```
No `.tmp` sibling left; stderr ends `wrote /tmp/r19mm/.ufo/waves/round-18/evidence/measure-mutants.json`;
stdout summary equals the file's `.summary`; the file's `harness.sha256` is `595a6a9b…` (the new
bytes). Clone restored with `git checkout --` → back to `58929eea…`.

## Probe 4 — `.summary` equals the committed receipt: HOLDS

Bare stdout `.summary` vs `git show 01b80946:…/evidence/measure-mutants.json` `.summary`:
`True`, both
`{"baselines_agree": true, "bites": 6, "expectations_met": 6, "expected_but_unmet": [], "mutants": 6, "no_bite": [], "unexpected_tight_only": []}`.
Every `baseline`/`mutant` `c2` block is equal for all six mutants; M6 tight still refuses
(`exit 2`, `duplicate SOURCES id S016`) and its `stdout_sha256` is `e3b0c442…` in both. The six
stderr lines match the committed counts (M1 4/3, M2 4/4, M3/M4/M5 5/4, M6 5/None).

## Findings that keep this from "holds"

**F1 (claim false as written).** `.ufo/waves/round-19/w1/reports/MeasureMutantsOut.md:39` says
"Non-normalized new-vs-committed diff (deep JSON walk) has 11 leaves, all
`mutants[*].mutant.{loose,tight}.stdout_sha256`" and "Two back-to-back new-script runs differ in
exactly those 11 leaves". Measured at tip:

- new vs committed, true deep walk: **63** differing leaves — `stdout_sha256` 11, `commit sha` 24,
  workdir path 18, `harness.*` 5, identity/time/env 5 (incl. `harness.sha256` `075815bd…` vs
  `595a6a9b…`, `lane`, `generated_at`, `started_at`).
- two back-to-back identical invocations (`bare2.json` vs `bare3.json`): **50** differing leaves —
  `stdout_sha256` 11, commit shas 24, `cmd[0]` workdir paths 12, plus `generated_at`, `started_at`,
  `environment.workdir` (random `mkdtemp`).

The `11` is exactly the `stdout_sha256` subset (12 minus M6-tight, whose refused empty stdout is
`e3b0c442…` in both runs). So the sentence describes a *normalised* comparison while calling it
"non-normalized". The conclusion it supports is true and I confirmed it independently
(`summary_equal: True`, `c2_all_equal: True`); only the counts/label are wrong.

**F2 (docstring overclaim; class disclosed in w1:63).** `measure-mutants.py:22-24` states a file
inside the read worktree is refused, "so a lab rerun cannot silently overwrite the lane receipt".
The guard is local to the worktree *path* named by `--lane` (`:494-499`, `:521-522`). Demonstrated
without touching the lane, using a linked worktree of the same repository:

```
git -C /tmp/r19mm2 worktree add -q --detach /tmp/r19mm-B HEAD      # .git is a file, worktree /tmp/r19mm-B
python3 -I /tmp/r19mm-B/.ufo/waves/round-18/measure-mutants.py \
  --lane /tmp/r19mm-B --out /tmp/r19mm2/.ufo/waves/round-18/evidence/measure-mutants.json  # RC=0, no refusal
# /tmp/r19mm2 receipt 58929eea… → 64b29ea57f570cd31d535c918970a949ff7fa329a9109ff6ca96264d68b8451b
# /tmp/r19mm-B receipt untouched 58929eea…; stderr: wrote /tmp/r19mm2/…
```
The inside-out direction is refused (`--lane /tmp/r19mm-B --out /tmp/r19mm-B/.ufo/x.json` →
refused), so the guard is symmetric — but a lane operated from a linked worktree (a normal layout
in this project's own tooling) can still silently rewrite the primary checkout's receipt. The w1
report's Risks block (`:63`) discloses the `--lane <clone> --out <real lane>` class; the shipped
docstring does not carry that qualifier. No in-lane claim (QUALITY `:202-204`) asserts the stronger
invariant; QUALITY's two statements (bare prints/writes nothing; explicit receipt needs
`--force-lane-receipt`) are true.

**F3 (unguarded write channel, inherited flag).** `--workdir` (`:513`, `:537`, cleanup `:681-682`)
is neither containment-checked nor tied to `--force-lane-receipt`: it extracts into the given path
and `shutil.rmtree`s it at exit (after per-mutant `rmtree` of `M1..M6`). With `--out` outside:

```
mkdir -p /tmp/r19mm2/sacrificial/M1; echo keep > …/M1/keepme; echo sib > …/sibling.txt
python3 -I …/measure-mutants.py --lane /tmp/r19mm2 --out /tmp/r19mm-out/outside.json \
  --workdir /tmp/r19mm2/sacrificial          # RC=0
# before: sacrificial/M1/keepme sacrificial/sibling.txt
# after:  (none) — `sacrificial` itself is gone
```
Payload records `environment.workdir=/tmp/r19mm2/sacrificial`, `kept=false`. This deletes, not
overwrites the receipt, and the flag predates the change (old version `17661e0:…:498`), so it is a
residual hazard, not a regression — but it falsifies any reading of "no file/dir is created"
beyond the bare invocation, and a mistyped `--workdir <lane>/corpus` would be destructive.

## Agreements checked, not merely assumed

- Old→new default removal: old `out = args.out or (lane / OUT_DEFAULT)` (`17661e0:…:502`,
  `OUT_DEFAULT` `:43`) vs new `out = args.out.resolve() if args.out else None` — the incident shape
  (bare run rewrites whatever lane `--lane` names) is gone.
- Edit size/identity: `git diff --stat 17661e0 01b80946` → `1 file changed, 41 insertions(+), 16 deletions(-)`;
  sha `075815bd…` → `595a6a9b…`.
- Instrument pins still enforced (`fetch_instrument`) — every run's `baseline_assert` passed at 4
  provinces P1/P2/P4/P6, so the pinned loose/tight bytes were verified in-run.
- stdout/stderr split: with `--out`, stdout is the summary JSON only; progress/wrote lines are on
  stderr (`:589-592`, `:678`), as the report states.

## Limits

- Never invoked the script against `/home/vgpnk/Projects/shokunin/mado-shokunin` as `--lane` and
  never ran it with the default `--lane`; the real lane receipt remains `58929eea…`
  (mtime `2026-10-20 13:30:28 -0300`) and `git status -- <round-18 paths>` is clean for it.
- Did not run the gate, round-18/19 suites, linters or formatters (wave rule).
- Did not test `GIT_DIR`/`GIT_WORK_TREE` env redirection of `rev-parse --show-toplevel`
  [INFERENCE: it would also redirect `git -C <tmp-repo>` and break the run before any write].
- Did not kill a run between `.tmp` write and `os.replace`; "atomic" here is verified only as
  "no `.tmp` left after success, summary visible in one `os.replace`".
- Did not test a mid-run symlink swap (TOCTOU) between the check and the write; a lab rerun does
  not perform one.
- Linked-worktree experiment used two /tmp checkouts; commit hashes/temp paths in my JSONs are
  run-specific and not comparable to the committed receipt's.
- All 24 instrument runs (2 clones × runs) were in /tmp; no file under the lane was created,
  modified or deleted by this seat except this report.

## Installs

none.
