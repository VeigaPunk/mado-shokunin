# R69ExecRecipeCounter — C1 counting command draft

seat: R69ExecRecipeCounter (leaf executor, wave w1 round 69)
draft: `.ufo/waves/round-69/w1/R69ExecRecipeCounter/draft/quality/counters/c1-r69-paired-recipes.py`
draft sha256: `f7cd7bb2e53864118b5527e93c6e789cc10d94c3c304cafce71f669acc87112d`
size: 32553 bytes, 733 lines, `python3 -m py_compile` ok (Python 3.14.8)
integration target: `quality/counters/c1-r69-paired-recipes.py` (L1 copies; this seat wrote no
production path)

## What the draft is

The frozen C1 counting command. One measurement:

1. `git rev-parse --verify <rev>^{commit}` and `<base-rev>^{commit}`, then extracts
   `quality/counters/c1-r69-landing-controls.py` at `--rev` with `git_env` — `GIT_OPTIONAL_LOCKS=0`,
   `GIT_NO_REPLACE_OBJECTS=1`, every inherited `GIT_*` dropped (`GIT_CONFIG_GLOBAL/SYSTEM=/dev/null`,
   `HOME/TMPDIR` pinned into the scratch tree).
2. Runs the extracted harness `--selftest --scratch-root <scratch>/r69-c1/candidate/st`;
   `selftest=<rc>`, or `selftest=absent` when the path does not exist at `--rev` (probed with
   `cat-file -e`, a read failure is a setup error, not `absent`).
3. Applies each frozen recipe R1/R2/R3 exactly once to a fresh scratch copy (the old text must
   occur exactly once before mutating, `applicable=no` otherwise and the recipe is never counted
   killed), then runs the mutant's own `--selftest`; a mutant is killed iff that exits nonzero.
   Mutants are compile-checked before the run so a syntax break cannot be credited as a kill.
4. Extracts `quality/counters/c1-r68-landing-controls.py` at `--base-rev`, applies the same three
   recipes, counts kills there (`base=<m>/3`). Per the declaration's "both counts are asserted
   before scoring", a base recipe that does not occur exactly once is a setup error (rc 2), never
   a silent `base=0/3`.
5. Prints the frozen contract line last and exits 0/1/2.

Contract line (byte-exact, `CONTRACT_RE.fullmatch`-asserted in the hermetic selftest):

```
MADO_R69_PAIRED_RECIPES: selftest=<rc|absent> killed=<n>/3 applied=<k>/3 base=<m>/3 verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>
```

Embedded recipe bytes (verified `occurrences=1` in both the r69 proto harness and the r68 harness
at base; both counts asserted at run time, not just at authoring):

- R1 old = two lines, 12 + 29 spaces: `            mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker)\n                             and forged_credit(mr_rc, mr_marker))`
  → new = `            mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker))`
- R2 old = `        mz_killed = mz_rc != 0`
  → new = `        mz_killed = mz_rc != 0 or mz_summary == "none"`
- R3 old = `    subprocess.run = _no_spawn`
  → new = `    pass  # spawn guard removed by recipe`

Hermetic `--selftest` (61 assertions): installs `subprocess.run = _no_spawn` for the whole body,
asserts the guard is installed and that an attempted spawn raises, patches the module-level `run`
with scripted children, and drives the real `measure()` body six times: met, killed<3, applied<3,
base>0, selftest!=0, candidate absent, plus a base-inapplicable setup-error case. It asserts each
printed line byte-exactly and via `fullmatch`, that the scripted met case issued 7 harness calls
(1 candidate + 3 mutants + 3 base mutants) with the spawn guard still installed afterwards, that
`/tmp`-family and symlinked scratch roots are refused, that inherited hostile `GIT_*` are scrubbed
from both env constructors, and that the frozen env key set is exact.

## Evidence (all commands run from scratch `/fast/scratch/hyaku/mado-r69/R69ExecRecipeCounter`, since removed)

`D` = the draft path above; `L` = `/home/vgpnk/Projects/shokunin/mado-shokunin`;
`B` = `04093b83f73a841117d3b31dbb2a6063f4f2a454`.

### (a) hermetic selftest — rc 0

```
python3 "$D" --selftest --scratch-root /fast/scratch/hyaku/mado-r69/R69ExecRecipeCounter/st2
MADO_R69_PAIRED_RECIPES_SELFTEST: 61/61 assertions passed
rc=0
```

First run (before the base-inapplicable hardening) was `60/60`; the hardening added one check.

### (b) frozen command at the lane base rev — rc 1, exact line

```
python3 "$D" --repo "$L" --rev "$B" --base-rev "$B" --scratch-root .../base-run
MADO_R69_EXTRACT path=quality/counters/c1-r69-landing-controls.py rev=04093b83f73a841117d3b31dbb2a6063f4f2a454 present=no
MADO_R69_EXTRACT path=quality/counters/c1-r68-landing-controls.py rev=04093b83f73a841117d3b31dbb2a6063f4f2a454 present=yes bytes=36005 sha256=25470bc432ad3b612f08869052915f331d9a930149b3af6a9bf0e3eb87cf5527
MADO_R69_BASE_MUTANT name=R1 path=quality/counters/c1-r68-landing-controls.py recipe=R1 from_sha256=25470bc4… rc=0 assertions=52/52 killed=no sha256=bc2d71bc2e350fed83a7db4beaf339f04e8857e19a6a2926471057b3970915d3
MADO_R69_BASE_MUTANT name=R2 … rc=0 assertions=52/52 killed=no sha256=d85500d40302d9d1dfbacfb909640a06c8625b1857cfb02964822b192b05c25b
MADO_R69_BASE_MUTANT name=R3 … rc=0 assertions=52/52 killed=no sha256=1764a0082d3bd379183877f704dbaa34f22dc5622af1740dc7e55011a37902ba
MADO_R69_PAIRED_RECIPES: selftest=absent killed=0/3 applied=0/3 base=0/3 verdict=TARGET_MISSED rev=04093b83f73a841117d3b31dbb2a6063f4f2a454
rc=1
```

The three base mutants are byte-identical to the frozen control-baseline receipt's independent
`RECIPE/MUTANT` probes (52/52, rc 0, killed=no), i.e. the r68 harness survives all three.

### (c) scratch fixture repo (not the lane) — rc 0, TARGET_MET

Fixture: `mktemp -d "$S/fixture.XXXX"` → `git init -q`; `rev-parse --show-toplevel` asserted equal
to the fixture dir before the first commit; `git -C "$D" fetch "$L" "$B"`; `git -C "$D" checkout -q
"$B"`; copied `.ufo/waves/round-69/proto/c1-r69-landing-controls.proto.py` to
`quality/counters/c1-r69-landing-controls.py`; `git -C "$D" -c user.name=r69-c1 -c
user.email=r69-c1@example.invalid -c commit.gpgsign=false commit`. Fixture HEAD
`e33aeac480b0139c0c761a0fdc121240844c317f`; fixture worktree = lane base tree + draft harness; the
lane itself was only read (`fetch`/`cat-file`/`rev-parse`).

```
python3 "$D" --repo /fast/scratch/.../fixture.nI2K --rev HEAD --base-rev "$B" --scratch-root .../fixture-run
MADO_R69_EXTRACT path=quality/counters/c1-r69-landing-controls.py rev=e33aeac4… bytes=37646 sha256=f4d138bfe806f787a98d5ca4d48ebf44896a4276cb0964df5d99e16f6b25390f
MADO_R69_SELFTEST harness=quality/counters/c1-r69-landing-controls.py rc=0 assertions=59/59
MADO_R69_MUTANT name=R1 … rc=1 assertions=57/59 killed=yes sha256=19d8de98b5e3e3980a7ee66fbe68cab32b8fc61972d3226de3c96e8f3d1a6481
MADO_R69_MUTANT name=R2 … rc=1 assertions=58/59 killed=yes sha256=0298800931525c113c4b3ead0b9d2317ad3cc625750dece36d60f72ccd02625e
MADO_R69_MUTANT name=R3 … rc=1 assertions=57/59 killed=yes sha256=e5e538dd4f8612c85d1a2ece46a4ed344b7a89e60bbff6faa8122f03041341c7
MADO_R69_BASE_MUTANT name=R1/R2/R3 … rc=0 assertions=52/52 killed=no
MADO_R69_PAIRED_RECIPES: selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET rev=e33aeac480b0139c0c761a0fdc121240844c317f
rc=0
```

The three mutant assertion fractions equal the frozen feasibility receipt (`MADO_R69_C1_PROTO`).

### (d) anti-gaming — rc 1, TARGET_MISSED

Two scratch fixtures, each built like (c) and then committing an edited copy of the harness:

1. **Recipe text deleted** (R1's two frozen lines replaced by the semantically identical one-liner
   `            mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker) and forged_credit(mr_rc, mr_marker))`):
   fixture HEAD `397dffaeecdcfe8f832cfa493d3c088802deb4f3`, harness selftest still green `59/59`.
   `MADO_R69_RECIPE name=R1 occurrences=0 applicable=no note=R1 text occurs 0 times, expected exactly 1`
   `MADO_R69_PAIRED_RECIPES: selftest=0 killed=2/3 applied=2/3 base=0/3 verdict=TARGET_MISSED rev=397dffae…` rc=1
   → the counter refuses to credit a recipe it could not apply; `killed` never exceeds `applied`.
2. **Forgery undetected by a weakened oracle** (the harness's `mz-unparseable` scripted case
   removed; all three recipe texts intact): fixture HEAD
   `9e02e7c14d380216ddc5cd157947539ae610e92f`, harness selftest green `56/56`.
   All three `applicable=yes`, `applied=3/3`, but the R2 mutant's own `--selftest` exits 0 →
   `MADO_R69_PAIRED_RECIPES: selftest=0 killed=2/3 applied=3/3 base=0/3 verdict=TARGET_MISSED rev=9e02e7c1…` rc=1.
   → kill credit is decided by the mutant's own exit code, never by recipe presence.

Both edited-harness fixture trees were scratch commits; the lane was never touched.

### (e) extraction guard against a planted replacement ref — rc 0, TARGET_MET

Scratch fixture (same construction; HEAD `1316a6ec23bb0999ff29732b535803caf1190cd5`), then
`hash-object -w` a forged blob (`print("forged harness")`) and `git replace <real blob>
<forged blob>`:

- plain read: `git -C "$D" cat-file blob 72a23d14…` → `print("forged harness")`
- guarded read (`GIT_NO_REPLACE_OBJECTS=1`): real harness bytes
- counter: extracts `sha256=f4d138bf…` (the real proto bytes, not the forged blob) and prints
  `MADO_R69_PAIRED_RECIPES: selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET rev=1316a6ec…` rc=0

So a `refs/replace` plant in `--repo` cannot forge the bytes the recipes and selftest score.

### (f) lane HEAD at run time (informational, read-only) — rc 0, TARGET_MET

`--rev HEAD` against the lane resolved to `6a5cefd252c41c7ff71217da65126fc831f8bc34`: candidate
harness present (bytes=37647, sha256 `b374cfb8e024971e69a19d44af21efe5ed1b46c03a3b57387f7dd7fd4eed69aa`),
selftest `59/59`, mutants `57/59`, `58/59`, `57/59` rc=1, base `0/3`:

```
MADO_R69_PAIRED_RECIPES: selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET rev=6a5cefd252c41c7ff71217da65126fc831f8bc34
rc=0
```

HEAD moved during the wave (`98bff016` → `6a5cefd2`) because sibling seats were integrating; the
L1 must re-run the frozen command at the final measured content.

### (g) exit-code contract probes — all rc 2

| invocation | rc | stderr first line |
|---|---|---|
| `--selftest` (no scratch) | 2 | `c1-r69-paired-recipes.py: --scratch-root is required` |
| `--selftest --scratch-root /tmp/x` | 2 | `… unsafe scratch root (tmp-family): /tmp/x` |
| frozen args `--scratch-root /tmp/y` | 2 | `… usage error: unsafe scratch root (tmp-family): /tmp/y` |
| `--rev B --scratch-root …` (no `--base-rev`) | 2 | `… usage error: --repo, --rev and --base-rev are required` |
| `--rev deadbeef` | 2 | `… setup error: rev does not resolve to a commit at --repo` |
| `--selftest` through a symlinked scratch component | 2 | `… scratch root contains a symlink component: …/linkroot` |

## Findings

- The draft satisfies the frozen C1 counting command: (b) is the before-state exact line
  `selftest=absent killed=0/3 applied=0/3 base=0/3 verdict=TARGET_MISSED` rc 1; (c) is the
  target `selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET` rc 0. Both use the real
  harness bytes, the real mutants and the real r68 base, with the declared scrubbed env.
- The counter is not satisfiable by weakening the harness silently: removing a recipe text yields
  `applicable=no` (never killed), and a green mutant never counts as a kill even when all three
  recipes apply.
- Extraction is replacement-ref-proof (e), and the printed rev is the resolved commit sha.
- Base-leg recipes are asserted exactly once; an inapplicable base recipe is rc 2 (setup), so a
  wrong `--base-rev` can never produce a credited `base=0/3`.

## Risks / notes for the L1

- The counter embeds the three recipe texts literally; any legitimate reformat of the r69 harness
  that changes those bytes flips `applicable=no` and the target to MISSED. That is the frozen
  contract, not a defect, but the harness seat must not reflow those three anchors.
- `selftest=<rc>` prints the harness's exit code verbatim; only `0` is green. A harness rc 2 is a
  red selftest (MISSED), not a counter setup error.
- Kill = mutant `--selftest` nonzero, exactly as declared; the compile gate only prevents a
  syntax-broken mutant from being credited.
- The base leg runs after the candidate leg; a base-harness problem therefore surfaces as rc 2
  after the candidate evidence lines (no contract line). Nothing is credited in that case.
- Lane HEAD was moving during this seat (`98bff016` at start, `6a5cefd2` when (f) ran, sibling
  edits to `corpus/SOURCES.md` and new round-69 knowledge/lesson files are visible in
  `git status`). This seat wrote no lane path except this report and its seat directory.
- Integration: copy the draft to `quality/counters/c1-r69-paired-recipes.py`; the frozen command
  needs only `python3` and `git` (host: Python 3.14.8, git 2.56.0).

## Lane / hygiene

- Wrote only `.ufo/waves/round-69/w1/R69ExecRecipeCounter/` (draft) and this report.
- No git/jj mutation in the lane, the fleet repo or any sibling lane; fixture git calls used
  `-C "$D"` with an asserted fixture toplevel and explicit `-c user.name/user.email`.
- No pacman transaction (PACMAN paused host-wide); no tool installs or upgrades were needed —
  system `python3 3.14.8` and `git 2.56.0` only.
- No compositor/socket/service/package-manager probe; no screenshots; no credentials.
- Scratch `/fast/scratch/hyaku/mado-r69/R69ExecRecipeCounter/` removed after capturing the
  evidence above (fixtures, selftest dirs, run dirs all deleted).
