# R56ExecWatchplanHarness — C2 control harness (w1)

Deliverable: `.ufo/waves/round-56/w1/R56ExecWatchplanHarness/r56_ctl_c2.py` (exposes `run(argv)->int`; also `python3 -I r56_ctl_c2.py --repo R --rev REV --work DIR [--holdout DIR]`). Not run against `tools/mado-watchplan.py` of a real tool: at `3423ae28` the tool does not exist (see A).

## What it does
- Reads git objects at `--rev` only. `frozen-tables.json` must be a regular blob (100644/100755) with sha256 `d50d2b7b…f9af` (embedded) else setup error (rc 2, stderr, nothing on stdout). Also rc 2: bad/duplicate/missing options, unresolvable rev, `fixtures/c2` absent, `--holdout` not a directory.
- Exports with `git archive --format=tar <rev> -- <paths> | tar -x --no-same-owner` (paths: tools/mado-watchplan.py if a regular blob, fixtures/c2, ctl, frozen-tables.json; `fixtures/c2-holdout` only when `--holdout` is absent and the tree exists at rev). `--holdout DIR` is copied with `tar -c | tar -x` into `<export>/.ufo/waves/round-56/fixtures/c2-holdout` (symlinks kept). Export lives in `mkdtemp(dir=--work)` and is removed in `finally`.
- Per fixture: `{FX}` -> absolute fixture dir inside the export in every `args.json` string; `python3 -I <program> <args>`, cwd = export root, env = `PATH, HOME=work, TMPDIR=work, LC_ALL/LANG=C.UTF-8` only, stdin /dev/null, stderr discarded, 30 s timeout; pass = stdout bytes AND rc equal `expected.out`/`expected.rc`. Missing tool => every fixture fails (fixtures=0/18 "by absence").
- Commitments recomputed per registration (sorted UTF-8 bytes of relpath; `<rel>\0<f|l>\0<sha256 of bytes or link text>\n`; symlinks never followed). Compared with `c2.fixture_commit_sha256` / `c2.holdout_commit_sha256` from the exported tables blob. `holdout_commit=absent|ok|bad`.
- Controls run in place of the tool on the same fixtures from the exported `ctl/`: const-host passes iff (committed+holdout passes) <= 1; empty iff 0; lookup-committed iff 18/18 committed and 0 hold-out. Missing stub => that control fails.
- `TARGET_MET` needs fixtures=18, holdout=8, holdout_commit=ok, fixture commitment ok, controls=3. One extra diagnostic line (fixture commitment + control scores) goes to **stderr**; stdout is exactly the one `MADO_R56_C2:` line. Exit 0/1/2.

## Evidence (scratch repos built from `git archive 3423ae28 -- frozen-tables.json fixtures ctl`; scratch removed)
A. Real lane rev (no tool at rev):
```
r56_ctl_c2: fixture_commit=ok control_scores={'const-host': (1, 0), 'empty': (0, 0), 'lookup-committed': (18, 0)}
MADO_R56_C2: rev=3423ae28… fixtures=0/18 holdout=0/8 holdout_commit=absent controls=3/3 verdict=TARGET_MISSED   rc=1
```
**Control scoring on the committed fixtures: const-host 1/18 (passes F02 only), empty 0/18, lookup-committed 18/18; hold-out 0 for all three (hold-out absent). Fixture commitment recomputed = frozen `fixture_commit_sha256` (`ok`), which also proves symlinks (F05 linked.conf, F06 hyprland.conf, F10 mix/b.conf) survive export.**

B. Throwaway tool printing `MADO_WATCH: garbage`, exit 7 (fails every fixture): `fixtures=0/18 … controls=3/3 verdict=TARGET_MISSED` rc=1. A first throwaway printing `MADO_WATCH: SETUP usage`/exit 2 scored `fixtures=1/18`: one committed fixture legitimately expects that exact setup output (not a harness defect; choose a garbage tool, not a SETUP printer, for a 0/18 control).

C. Plumbing of the 18/18 path: lookup-style tool that replays `expected.out/rc` from any `F##`/`H##` ancestor dir of its args: `fixtures=18/18`. With a synthetic hold-out (F01..F08 copied as H01..H08, via `--holdout` and also via a committed `c2-holdout` tree at rev): `fixtures=18/18 holdout=8/8 holdout_commit=bad controls=2/3 verdict=TARGET_MISSED` (bad: not the sealed set; controls 2/3 because const-host prints F02, which equals synthetic H02, giving 1+1 passes — consistent with the "at most 1 of 26" rule, an artifact of my synthetic copy). Export of the hold-out dir preserved symlinks (commitment of export == commitment of source, H05 `linked.conf` still a link). Argument errors / bad rev: rc 2, stderr reason, empty stdout. `--work` left empty after every run.

## Ambiguities / decisions (registration is silent)
1. `frozen-tables.json` sha mismatch at rev: I treat as setup error rc 2 (counters have a `tables_sha` leg; the harness line has no place for it).
2. Fixture-dir absent at rev: setup error; absent tool: `fixtures=0/18` per claims "by absence"; absent `ctl/` or a stub: that control fails (controls<3).
3. Registration says pass counts are over "26 fixtures": when hold-out is absent the const-host/lookup checks use only the committed 18 (holdout counted 0).
4. The `--rev` string is printed as given (not resolved to a full sha).
5. Env scrub choice (`LC_ALL=C.UTF-8`, PATH `/usr/local/bin:/usr/bin:/bin`) is mine; the spec says only "scrubbed".
6. Task says compare against the lane `frozen-tables.json`; I read the blob at `--rev` (verified against the embedded sha), which is the same file at 3423ae28.
7. The ctl stubs find fixtures via `__file__/../fixtures/c2`, so the harness keeps the full in-repo layout in the export (`<export>/.ufo/waves/round-56/{ctl,fixtures}`) and tool at `<export>/tools/`.

## Not verified
Never run against a real `tools/mado-watchplan.py` (none exists yet); the real sealed hold-out was not seen or used; no tool installs; no host reads beyond lane files. Not a non-author review.
