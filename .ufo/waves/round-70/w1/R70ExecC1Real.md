# R70ExecC1Real — claim C1 counting command, driven end to end (round 70)

seat: `R70ExecC1Real` (leaf; no subagents)
lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`
scratch: `/fast/scratch/hyaku/mado-r70/R70ExecC1Real` (removed on exit)
frozen inputs: `.ufo/waves/round-70/claims-declaration-r70.md`; base `b37a5aec4ea03f2223d8e09dd5d386d055c24179`; dispatch rev `5144a6b5f43225d8021a469f4d24c19558026b9e`.

Installed/updated nothing this seat; pacman untouched.

## 0. Instrument identity actually measured

| path | sha256 at 5144 | sha256 at 71caa8b7 (HEAD during measurement) | same |
|---|---|---|---|
| `quality/counters/c1-r70-real-children.py` | `b1785f388724c8f0a21dda016da2e212105354221767eaa128fa73c3ddaaebb4` | `b3a6f131abf371ecf64273b65a143478c4b23eaa7acf974ec80e5efebf6e6a7b` | **NO** (1 line) |
| `quality/counters/c1-r70-landing-controls.py` | `71a7b6c45b904a734f194be9a8de6cc2eeb5f5ea1922760f908f5637f1d4db58` | same | yes |
| `quality/counters/c1-r69-landing-controls.py` | `9461a059466e723ba0ae88c86dea2fc97eb5f4fdfb15ef6c6646acce69649a73` | same | yes |
| `quality/landing-counters.sh` | `4378fd8c278126111ad6d970ac20215c170238ffe1a796c5c7d03c9e5b3b93a9` | same | yes |
| `tools/mado-receipt-citecheck.py` | `3b61fa42b77e9c8065ab05668247c330b537910b06f7209caba7afbd0b102ad0` | same | yes |

The lane HEAD moved **while this seat ran** (not by this seat; no mutating git command was issued):

```
5144a6b5 2026-11-03 23:29:46 -0300  the two scored instruments and the repaired harness
9508e878 2026-11-03 23:32:33 -0300  create the per-scenario scratch dir in the C1 counter (pre-data setup repair; predicate unchanged)
5adba5a9 2026-11-03 23:33:01 -0300  label the candidate and base control-leg lines (observability only)
71caa8b7 2026-11-03 23:34:48 -0300  ledger rows + wave spec/dispatch/ready + measurement receipt
```

`git diff 5144 71caa8b7 -- quality/counters/c1-r70-real-children.py` is exactly one added line:

```
+    os.makedirs(scratch, exist_ok=True)
```
inside `run_harness()`, immediately before `subprocess.run(..., cwd=scratch, ...)`.

HEAD advanced again after the measurement (`3aea1e10`, `f754347a`: harm-watch battery and ledger/index/scorecard rows). `git diff 71caa8b7 f754347a -- <the five files tabulated above>` is empty; `c1-r70-real-children.py` is still `b3a6f131…` and `c1-r70-landing-controls.py` still `71a7b6c4…` at `f754347a`.

## 1. Selftest

```
$ python3 -I quality/counters/c1-r70-real-children.py --selftest --scratch-root <scratch>/st
MADO_R70_REAL_CHILDREN_SELFTEST: 26/26 assertions passed
rc=0
```
Same command and same `26/26`, `rc=0` for the exact 5144 blob (`counter-5144.py`, sha256 `b1785f38…`). Selftest is hermetic and does not exercise `run_harness`, so it cannot see the defect below.

## 2. The frozen counting command

### 2a. At REV = 5144, with the lane's current counter (`b3a6f131…`, also HEAD `71caa8b7`)

```
$ python3 -I quality/counters/c1-r70-real-children.py --repo . \
    --rev 5144a6b5f43225d8021a469f4d24c19558026b9e \
    --base-rev b37a5aec4ea03f2223d8e09dd5d386d055c24179 --scratch-root <scratch>/m
MADO_R70_REVS rev=5144a6b5f43225d8021a469f4d24c19558026b9e base=b37a5aec4ea03f2223d8e09dd5d386d055c24179
MADO_R70_HARNESS role=candidate path=quality/counters/c1-r70-landing-controls.py present=yes sha256=71a7b6c45b904a734f194be9a8de6cc2eeb5f5ea1922760f908f5637f1d4db58
MADO_R70_HARNESS role=base path=quality/counters/c1-r69-landing-controls.py sha256=9461a059466e723ba0ae88c86dea2fc97eb5f4fdfb15ef6c6646acce69649a73
MADO_R70_FIXTURE mode=genuine rev=19cd39f09db2237e12d6ee66fc2126e590113e6b lane_sha256=96cf148ea48964331fb4ca19557e322a348127687b1b3a6492d1b3a3b7a9a2cc
MADO_R70_FIXTURE mode=crash rev=cd120576ac2eefaa96d5db61382539b5a924aabb lane_sha256=e8562c3fa3e4e3c0747f8354192bb76f9ea5a7cea4a39bbd625f7912ecc3c33c
MADO_R70_FIXTURE mode=garbage rev=fad99cf7f8b47b9433c7fdaf93f8d1f2091e4af7 lane_sha256=85dcd09cd619562c4a4f60b212395ccab1581fd8b5a4fb90f14bb94ba4216ff2
MADO_R70_SCENARIO mode=genuine expect_mz=pass candidate_mz=pass base_mz=pass correct=yes base_correct=yes rev=19cd39f09db2237e12d6ee66fc2126e590113e6b
MADO_R70_SCENARIO mode=crash expect_mz=fail candidate_mz=fail base_mz=pass correct=yes base_correct=no rev=cd120576ac2eefaa96d5db61382539b5a924aabb
MADO_R70_SCENARIO mode=garbage expect_mz=fail candidate_mz=fail base_mz=pass correct=yes base_correct=no rev=fad99cf7f8b47b9433c7fdaf93f8d1f2091e4af7
MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=1 verdict=TARGET_MET rev=5144a6b5f43225d8021a469f4d24c19558026b9e
rc=0
```

Last line is **byte-identical to the declaration's C1 frozen sentence** (`rev=<sha>` = 5144). Exit 0. No divergence for the instrument present at the lane's HEAD.

### 2b. At base (do-nothing leg)

```
$ python3 -I quality/counters/c1-r70-real-children.py --repo . \
    --rev b37a5aec4ea03f2223d8e09dd5d386d055c24179 \
    --base-rev b37a5aec4ea03f2223d8e09dd5d386d055c24179 --scratch-root <scratch>/mb
MADO_R70_REVS rev=b37a5aec4ea03f2223d8e09dd5d386d055c24179 base=b37a5aec4ea03f2223d8e09dd5d386d055c24179
MADO_R70_HARNESS role=candidate path=quality/counters/c1-r70-landing-controls.py present=no
MADO_R70_REAL_CHILDREN: cases=3 correct=absent base_correct=0 verdict=TARGET_MISSED rev=b37a5aec4ea03f2223d8e09dd5d386d055c24179
rc=1
```

`correct=absent` matches the declaration's stated "before"; `base_correct=0` is a short-circuit — the counter returns before measuring the base harness, so the receipt's `1/3` is not re-derived by this invocation (see F3).

### 2c. At REV = 5144 with the counter bytes actually committed at 5144 (`b1785f38…`)

```
$ python3 -I <scratch>/counter-5144.py --repo . \
    --rev 5144a6b5f43225d8021a469f4d24c19558026b9e \
    --base-rev b37a5aec4ea03f2223d8e09dd5d386d055c24179 --scratch-root <scratch>/m5144
MADO_R70_REVS rev=5144a6b5f43225d8021a469f4d24c19558026b9e base=b37a5aec4ea03f2223d8e09dd5d386d055c24179
MADO_R70_HARNESS role=candidate path=quality/counters/c1-r70-landing-controls.py present=yes sha256=71a7b6c45b904a734f194be9a8de6cc2eeb5f5ea1922760f908f5637f1d4db58
MADO_R70_HARNESS role=base path=quality/counters/c1-r69-landing-controls.py sha256=9461a059466e723ba0ae88c86dea2fc97eb5f4fdfb15ef6c6646acce69649a73
MADO_R70_FIXTURE mode=genuine rev=0b22f3e66b01f0d74ea27637706aee840cb6629f lane_sha256=96cf148e…
MADO_R70_FIXTURE mode=crash rev=53d05cbdac9cbe47de2515919f2333f795cfa3fe lane_sha256=e8562c3f…
MADO_R70_FIXTURE mode=garbage rev=8ab7270145e4532dd87cb25d7b25695cf3029033 lane_sha256=85dcd09c…
rc=1
```

No contract line. stderr:

```
Traceback (most recent call last):
  File "<scratch>/counter-5144.py", line 430, in <module>
    sys.exit(main(sys.argv[1:]))
  File "<scratch>/counter-5144.py", line 420, in main
    return measure(args)
  File "<scratch>/counter-5144.py", line 303, in measure
    _, got, _ = run_harness(cand_path, CAND_PREFIX, fx, revs[mode],
  File "<scratch>/counter-5144.py", line 254, in run_harness
    r = subprocess.run(argv, cwd=scratch, ...)
FileNotFoundError: [Errno 2] No such file or directory: '<scratch>/m5144/r70-c1/cand-genuine'
```

Pre-creating `<scratch>/r70-c1/{cand,base}-{genuine,crash,garbage}` does **not** help: `measure()` itself does `shutil.rmtree(work); os.makedirs(work)` first, deleting them. The 5144 bytes therefore cannot produce the frozen line at all.

## 3. Fixture re-derived independently

`LANE_TEMPLATE` extracted with `python3 -c 'import runpy; print(runpy.run_path("quality/counters/c1-r70-real-children.py")["LANE_TEMPLATE"])'`:

- sha256 `9055bfa091eaba8063458eecc3b2d8247f90224f9537c8baa106a3c5aa86c945`, 1021 bytes, clause count 1, `@MODE@` slots 2.
- vs frozen `.ufo/waves/round-70/proto/fixture-lane.tmpl` (sha256 `9e31681dd95976af4b107566b1710a50d962b9af36d3e5db6b73078393c91b6f`): identical except the placeholder token (`__MODE__` → `@MODE@`, 2 occurrences). No behavioral diff.

Own scratch git repo (children extracted from 5144, one commit per mode, explicit identity, `-C` on every git call, toplevel asserted):

| mode | rev | lane sha256 |
|---|---|---|
| genuine | `aad5ea451d82d3b255ba92feaad5a1d114e9d6ac` | `96cf148ea48964331fb4ca19557e322a348127687b1b3a6492d1b3a3b7a9a2cc` |
| crash | `bc14c138c23e9fa13b1b21bb5c0d40a8c8d8c7c6` | `e8562c3fa3e4e3c0747f8354192bb76f9ea5a7cea4a39bbd625f7912ecc3c33c` |
| garbage | `e80dd754c7de6d38271ba3521a00aee44179d76b` | `85dcd09cd619562c4a4f60b212395ccab1581fd8b5a4fb90f14bb94ba4216ff2` |

All three lane hashes equal the baseline receipt's `from_sha256`, i.e. the emitted fixture bytes are the frozen ones.

`python3 -I quality/counters/c1-r70-landing-controls.py --repo <fixture> --rev <mode-rev> --scratch-root <dir>`:

```
genuine  rc=0  MADO_R70_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MET rev=aad5ea45…
crash    rc=1  MADO_R70_LANDING_CONTROLS: selftest=0 mz=fail mr=pass killed=1/2 baseline=0/2 verdict=TARGET_MISSED rev=bc14c138…
garbage  rc=1  MADO_R70_LANDING_CONTROLS: selftest=0 mz=fail mr=pass killed=1/2 baseline=0/2 verdict=TARGET_MISSED rev=e80dd754…
```

M-Z lines behind them: genuine `clause_count=1 recipe=clause-delete rc=1 failed_assertions=1 assertions=1/2 killed=yes`; crash `rc=2 failed_assertions=0 assertions=none killed=no`; garbage `rc=1 failed_assertions=0 assertions=none killed=no`.

Same fixture, frozen round-69 harness:

```
genuine  rc=0  MADO_R69_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MET rev=aad5ea45…
crash    rc=0  MADO_R69_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MET rev=bc14c138…
garbage  rc=0  MADO_R69_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MET rev=e80dd754…
```

So `correct=3` / `base_correct=1` is reproducible from the template alone; the base harness indeed credits crash and garbage (`mz=pass`) and the candidate does not.

## 4. Adversarial checks

Clone of the lane at 5144 (`git clone --no-hardlinks`, then `git checkout 5144…`; toplevel asserted), one commit per state.

**(a) Candidate harness deleted** — rev `e961d3ab64c6c5d38d1c063fffcf3c6db67152ba`:

```
MADO_R70_HARNESS role=candidate path=quality/counters/c1-r70-landing-controls.py present=no
MADO_R70_REAL_CHILDREN: cases=3 correct=absent base_correct=0 verdict=TARGET_MISSED rev=e961d3ab64c6c5d38d1c063fffcf3c6db67152ba
rc=1
```
No scenario lines, no credit.

**(b) Candidate replaced by a stub printing `mz=fail` every run** — rev `529d7c16bc10f53a55c84ac51376a919b0e59164`, candidate sha256 `c04d6145…`:

```
MADO_R70_SCENARIO mode=genuine expect_mz=pass candidate_mz=fail base_mz=pass correct=no base_correct=yes rev=…
MADO_R70_SCENARIO mode=crash   expect_mz=fail candidate_mz=fail base_mz=pass correct=yes base_correct=no rev=…
MADO_R70_SCENARIO mode=garbage expect_mz=fail candidate_mz=fail base_mz=pass correct=yes base_correct=no rev=…
MADO_R70_REAL_CHILDREN: cases=3 correct=2 base_correct=1 verdict=TARGET_MISSED rev=529d7c16…
rc=1
```
Refused: `genuine` cannot be satisfied by an always-fail harness.

**(c) Candidate replaced by a stub printing `mz=pass` every run** — rev `68b33d116992efc455f44066cd4099b95696d196`, candidate sha256 `2c0ac7d7…`:

```
MADO_R70_SCENARIO mode=genuine expect_mz=pass candidate_mz=pass base_mz=pass correct=yes base_correct=yes rev=…
MADO_R70_SCENARIO mode=crash   expect_mz=fail candidate_mz=pass base_mz=pass correct=no base_correct=no rev=…
MADO_R70_SCENARIO mode=garbage expect_mz=fail candidate_mz=pass base_mz=pass correct=no base_correct=no rev=…
MADO_R70_REAL_CHILDREN: cases=3 correct=1 base_correct=1 verdict=TARGET_MISSED rev=68b33d11…
rc=1
```
`crash` and `garbage` fail it; refused.

**(d) Fixture lane with no `[ "$citations" -gt 0 ] && ` at all** (template with that token stripped, `clause_count=0`) — genuine rev `23813785de6a1b5be08b33b022ca15fc57f01318`, crash `cda2423b…`, garbage `d7fbdc4d…`. Harness result per mode:

```
MADO_R70_SELFTEST instrument=quality/landing-counters.sh rc=1 assertions=1/2        (genuine; crash rc=2 assertions=none; garbage rc=1 assertions=none)
MADO_R70_MUTANT M-Z ... clause_count=0 recipe=none removed=none rc=- failed_assertions=- assertions=none killed=no sha256=absent note=zero-citation clause occurs 0 times, expected exactly 1
MADO_R70_LANDING_CONTROLS: selftest=1 mz=fail mr=pass killed=1/2 baseline=0/2 verdict=TARGET_MISSED rev=23813785…
rc=1
```
No credit for an inapplicable recipe (`mz=fail`, `killed=no`), and M-R still runs and passes.

**But** the counting command, pointed at a repo whose own `quality/landing-counters.sh` has `clause_count=0` (children + r69 harness + r70 harness committed; rev `eec53483…`, base `1f6c146d…`), still prints:

```
MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=1 verdict=TARGET_MET rev=eec53483794e793bf5954dadf48291d8c493ec43
rc=0
```

Mechanism confirmed in source: `measure()` extracts only `CHILDREN` from the repo and writes the fixture lane from the embedded `LANE_TEMPLATE`; it never reads `quality/landing-counters.sh` at `--rev`. The score is a property of the embedded fixture, not of the repo's lane (see F4).

## 5. Write containment

Traced the full frozen run (`python3 -I … --rev 5144…`) under `strace -f -e trace=%file,chmod,fchmodat,truncate,ftruncate` with a fresh scratch root `<scratch>/nowrite`; 1624 write-side syscalls total, resolved per-PID with `chdir` tracking:

- 1610 targets inside the scratch root (fixture repos, extract trees, mutant trees, child HOME/TMPDIR under `<scratch>/nowrite/r70-c1/…`); 341 regular files there after the run;
- 174 `openat("/dev/null", O_RDWR)` (device, `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM`);
- **0 successful writes outside the scratch root**;
- 18 `openat("/dev/tty", O_RDWR|O_NONBLOCK)` attempts, all `ENXIO` (no device) — no write.

Lane listing before/after (paths+sizes+mtimes, `.git` included):
- `.ufo/waves/round-70/w1/R70ExecCadence.md` added, `…/R70ExecHarness.md` modified, `…/R70ScribeEntryC2/draft/corpus/knowledge/guard-carrier-shapes-r70.md` modified, `corpus/knowledge/guard-carrier-shapes-r70.md` added, `quality/__pycache__/check-anchor-cover.cpython-314.pyc` added, one `.git` directory mtime.
- All of these are concurrent sibling integration (timestamps inside the same minute, and the trace shows the counter's own tree performing zero writes outside scratch). Nothing was written by this seat into the lane except this report file.

## 6. Findings / divergences

- **F1 — the frozen sentence is not produced by the counter bytes committed at 5144.** At 5144 the file (`b1785f38…`) crashes with `FileNotFoundError` on `<scratch>/r70-c1/cand-genuine` before the first scenario, rc 1, **no contract line**. The frozen sentence is produced only after `9508e878` adds `os.makedirs(scratch, exist_ok=True)` in `run_harness()` (`b3a6f131…`). Selftest is blind to this (26/26 at both revisions).
- **F2 — dispatch text ("scored instruments are committed at 5144") is stale for this one file.** HEAD moved to `9508e878` → `5adba5a9` → `71caa8b7` at 23:32–23:34, and the L1's own `measurement-r70.txt` records the run at `5adba5a9`, not 5144. Predicate unchanged (one `os.makedirs`), but the instrument that produced the receipt is not the 5144 blob.
- **F3 — base-rev invocation prints `base_correct=0`.** The counter short-circuits on candidate-absent before running the base harness, so the `1/3` "before" figure is not re-derived by that invocation; it comes from the receipt / held harness. Matches the declaration's "before `correct=absent`" wording, but `base_correct=0` there must not be read as a contradiction of `1/3`.
- **F4 — the counting command never validates the repo's own lane.** It scores `3/3` on a repo whose `quality/landing-counters.sh` has no zero-citation clause, because the fixture lane comes from the embedded `LANE_TEMPLATE`. Within the declaration ("the fixture is the counter's own instrument") this is allowed; as a sanity check on the repo it is blind.
- **F5 — template placeholder differs from the frozen proto** only as `__MODE__` → `@MODE@`; emitted per-mode bytes match the receipt's `from_sha256` exactly.
- **No divergence from the C1 frozen sentence for the instrument at the lane's HEAD**: at REV 5144 it prints the sentence verbatim and exits 0; `correct=3 base_correct=1` is reproducible from the extracted template on an independently built fixture.

## 7. Reproduction

All commands above were run from `/home/vgpnk/Projects/shokunin/mado-shokunin` with `-I`; fixture repos under `/fast/scratch/hyaku/mado-r70/R70ExecC1Real`, each `git init`-ed after `git rev-parse --show-toplevel` was asserted equal to its directory, with `-c user.name=… -c user.email=…` identity. Scratch was removed on exit; no lane file was modified except this report.
