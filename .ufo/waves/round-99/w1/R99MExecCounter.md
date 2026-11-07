# R99MExecCounter -- w1 report: the C1 launch-environment counter (round 99)

Seat `R99MExecCounter`, lane `/home/vgpnk/Projects/shokunin/mado-shokunin`,
predicate **PRED-C1-r99-v1**. Instrument spawns (counter = instrument, not a
candidate): read-only `git` (rev-parse / `git show`), the measured candidate
`python3 -I`, the held round-98 tool `python3 -I`, the embedded naive control
`python3 -I`, and the frozen fresh generator `python3 -I` (the generator itself
runs `/usr/bin/gio` to measure its labels -- it is the oracle's instrument). The
counter never launches a host application, never writes the lane, never runs a
mutating git command.

## Files written (owned paths only)

- `.ufo/waves/round-99/build/c1-r99-launchenv.py` -- the C1 counter draft.
  sha256 `52abbbaa78e358ef646f3e7e92c1bd36516196540d4bb0221f38edd368801ecd`,
  1589 lines, ASCII-clean, stdlib only. Never writes the lane.
- `.ufo/waves/round-99/w1/R99MExecCounter.md` -- this report.

## Counter design (what the instrument does)

- CLI exactly as dispatched: `--repo --rev --base-rev --cases
  --expect-cases-sha256 --mutants --expect-mutants-sha256 --genseed
  --expect-genseed-sha256 --expect-tool-sha256 --expect-execargv-sha256
  --expect-gio-sha256 --scratch-root`, plus `--selftest` and a hidden
  `--mini-scale` (selftest fixture scale only). rc 0 TARGET_MET / 1
  TARGET_MISSED / 2 SETUP_ERROR.
- All six pins fail closed (64-hex format check, then byte comparison;
  `tool_pin=ok`, `execargv_pin=ok`, `gio_pin=ok` printed). The envelope's
  `gio_sha256` is cross-checked against `--expect-gio-sha256` AND `/usr/bin/gio`
  is re-hashed; `renderer_sha256 == oracle_sha256` is required (one file is the
  one renderer, M98-8).
- **Materialisation is the oracle's, never re-implemented**: the counter
  importlib-loads `.ufo/waves/round-99/controls/launchenv-probe-r99.py` from
  beside the `--cases` file after verifying its sha256 against BOTH envelope
  pins (`renderer_pin=ok`; absence or mismatch is SETUP because without the
  oracle builder there is nothing to score against), then drives
  `build_root(case, parent)` / `path_string(case, root)` /
  `sub_placeholders` from the loaded module. The `--selftest` mini universe
  swaps in an equivalent embedded module (`MINI_ORACLE_SRC`) so the selftest
  exercises the same production load-and-verify path.
- Case leg (byte-pinned with R99MMutC1): `python3 -I <tool> <desktop-arg>
  <args...> [--path <PATHSTR>] --json`, cwd = the case root (the oracle probe's
  measurement cwd), env exactly `{PATH: "", LC_ALL: "C", HOME: <root>/h}`.
  `<desktop-arg>` is the bare `case.desktop` for a `rel_desktop` case else
  `<root>/case.desktop`; args are root-joined unless `args_rel`; PATHSTR comes
  from the oracle's `path_string` (entries `{root}`/`{probe}`-substituted
  verbatim, `:`-joined, `""`/`.` entries preserved); `path: null` omits
  `--path`. The forced-empty process PATH makes a candidate that sneaks a
  `getenv("PATH")` lookup fail the frozen expects (the load-gate-path mutant
  class is observable).
- Comparison: strict and normalisation-free. Success = launches equal, argv as
  a sorted MULTISET of vectors (r98 M98-10; frozen expects are pre-sorted by
  the producer; `<x>/./p` != `<x>/p` != `<x>/bin//p`), cwd exact, env
  `GIO_LAUNCHED_DESKTOP_FILE` exact. Refusal = rc 2 + the exact cause string;
  `detail` ignored; causes pass through opaquely (all seven tokens:
  `load`, `no-terminal`, `program-not-found`, `cwd-failed`, `no-exec`,
  `desktop-file`, `exec-parse`) -- the counter never remaps, so any taxonomy
  drift surfaces as a scored mismatch, not as a silent pass. Expect tokens
  reversed `{root}`-first then `{probe}` (the exact inverse of the oracle's
  `canon()`), so `<x>/./p` forms and the `rel_desktop` literal survive.
- Mutant leg: each counted mutant's `find` must occur exactly once in the
  candidate's non-selftest prefix (cut at the first `def selftest(`, QUALITY
  167); finds unique across mutants/not_observable/equivalents;
  `candidate_sha256` cross-checked against the materialised tool bytes. A kill
  needs a NEW wrong answer vs the candidate's own baseline (r70 rule); a new
  crash is `crashed_not_killed`, never a kill. The mutated copy runs with the
  sibling module beside it (the candidate loads its committed sibling by path).
- Fresh leg: seed drawn at measurement (`os.urandom(8).hex()`,
  `MADO_R99_FRESH_SEED` override), generator run as
  `python3 -I <genseed> --seed HEX --dir D --out F --count 60` with PATH
  starting `/usr/bin` so its gio is the pinned binary; requires rc 0, a
  `FRESH_GEN:` summary matching the JSONL count, and a `FRESH_GEN_PIN` line
  carrying BOTH the pinned gio sha256 and the pinned oracle sha256. Every
  fresh root is rebuilt by the counter (the generator's roots are transient)
  and scored through the identical leg.
- Controls (predicate conjuncts 5 and 6): `control_naive` is the embedded
  <=20-line `Exec.split()` + no-environment model (one launch, field codes
  literal, args ignored, `no-exec` on a missing Exec) run through the same leg
  and parser; `control_held_r98` is the materialised round-98
  `tools/mado-execargv.py` at the measured revision over the same cases with
  the same strict comparator (its cwd/env answers are absent on its side and
  mismatch a real expect).
- Separability: `tools/mado-launchenv.py` must be ABSENT at `--base-rev`
  (SETUP `setup-base-has-tool` otherwise). Run with `--rev <base-rev>` the
  counter prints `SETUP_ERROR ... tools/mado-launchenv.py absent at <base-rev>`
  and exits 2 (the declared demonstration).
- Census atoms (informational, NOT predicate conjuncts): cases >= 60,
  classes >= 16, counted mutants >= 60, the fresh count, and a static scan of
  the candidate bytes (informational only -- the r99 predicate carries no
  structural clause; the scan flags process/socket/network top-level imports
  and the `os.system/popen/exec*/spawn*/fork*` family while explicitly
  allowing `importlib`, which contract 1 requires for the sibling load).
- `--selftest`: 18 stable checks (`MADO_COUNTER_SELFTEST: checks=18 failed=0`,
  exit 0) over a mini universe built at selftest time under the scratch root:
  fixture git repos (base without / base with the tool), mini candidate +
  sibling, mini cases (including `rel_desktop` and `args_rel` shapes), mini
  mutants (kill / survive / crash), mini generator, mini oracle builder; green
  run TARGET_MET, both pins, both separability runs (`setup-base-has-tool`,
  `tools/mado-launchenv.py absent at <base>` at `--rev <base>`), renderer
  missing, corrupted label (correct=3, TARGET_MISSED), surviving and crashing
  mutants, fresh seed override + randomness, controls behind, scratch clean.

## Validation measured this session (all in scratch; the lane was never written)

1. `--selftest`: `MADO_COUNTER_SELFTEST: checks=18 failed=0`, exit 0.
2. Case-leg semantics validated against the real `/usr/bin/gio` on a fixture
   root (my own probe, `env -i`, PATH only the case's bins): Terminal=true with
   a planted `kgx` prepends `kgx -e` and the R3 rewrite keeps the absolute
   argv[0]; the bare-name load-gate find + R3 rewrite answered `<root>/bin/probe`
   with `$0`; `Path=` set the child cwd; `GIO_LAUNCHED_DESKTOP_FILE` equalled
   the desktop argument; a program named differently from the Exec bare name
   refused at load exactly as gutils.c's walk predicts (my first fixture named
   the file `probe.sh` while Exec said `probe` -- the trace showed access() on
   `<Path>/probe`, `<entry1>/probe`, `<entry2>/probe`, i.e. the modelled walk;
   naming the file `probe` flipped it to a launch).
3. Dress rehearsal A (synthetic 17-case universe measured by the real oracle
   module, two agreeing runs each, candidate draft `a63c20c8`, real lane
   execargv `49f7fecd`, real renderer `cbfff7a4`, real fresh generator
   `50126423`): frozen 16/17 (the one miss is finding 2 below -- an
   out-of-freeze boundary case I planted deliberately), fresh 60/60, mutants
   3/4 killed + 1 survived (the unset-default string mutant, unobservable
   through the leg, exactly as R99MMutC1 classified it), control_naive 0/17,
   control_held_r98 1/17, static none, exit 1 TARGET_MISSED (correctly red
   because of my own boundary case + the surviving mutant).
4. Dress rehearsal B (the REAL frozen file `14b4cc57`, 31 classes, 67 cases,
   four real-class mutants anchored on the draft): see Final state.

## Findings for the L1 (frozen-plane relevant)

1. **Case-id prefix rule dropped.** My first draft enforced the r98
   `<class>-` id prefix; the real freeze names ids freely (`xte-plain` in
   class `term-xte`). Contract 2 never demanded a prefix, so the counter now
   checks only the safe charset (`^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$`) +
   envelope-level uniqueness. No frozen case is affected.
2. **path:null boundary (documented limit, no frozen case affected).** The
   shared leg runs the candidate with `PATH=""` (set-empty) while the oracle's
   probe ran path:null cases with NO PATH variable. A case whose answer uses
   the unset-default (`Exec="sh {probe}"`, path null -- the load gate must
   find `sh` on `/bin:/usr/bin:.`) is therefore not scoreable under today's
   leg: the candidate correctly models set-empty as one empty entry and
   refuses where gio launched. Both frozen `pu-*` cases carry an absolute
   Exec (PATH-independent) and score identically either way. If a later round
   wants the default branch observable, the leg for path:null cases should
   omit the PATH variable entirely (3-line change in `run_tool`'s caller).
   Sent to R99MExecOracle for the freeze ledger.
3. **`rel_desktop` measures tokenised, not literal.** The measured
   `GIO_LAUNCHED_DESKTOP_FILE` for the rel-desktop rehearsal case canon'd to
   `{root}/case.desktop` (gio canonicalises the bare argument against its cwd
   before storing info->filename). The counter supports both forms (the
   reversal leaves the literal `case.desktop` untouched); the frozen
   `env-gdf` class measured tokenised. No action.
4. **Multi-spawn cwd/gdf:** the oracle enforces one cwd and one gdf across
   spawns; the counter's per-vector multiset compare plus the single
   cwd/env_gdf comparison reproduces that plane exactly (rehearsal
   multispawn case: 3 launches, exact).

## Named limits of the counter

- Spawn order of multi-spawn launches is not compared (multiset, M98-10).
- `--rev worktree` reads the lane working tree for an uncommitted candidate;
  anything else must be a commit.
- The candidate's `--selftest` is not a counter leg (PRED-C1-r99-v1 has no
  selftest conjunct; the reviewer runs it directly).
- The census minimums are printed, not judged: the predicate is exactly the
  six declared conjuncts.

## Final state

- Counter: `.ufo/waves/round-99/build/c1-r99-launchenv.py`, sha256
  `52abbbaa78e358ef646f3e7e92c1bd36516196540d4bb0221f38edd368801ecd`.
- `--selftest`: `MADO_COUNTER_SELFTEST: checks=18 failed=0` (exit 0).
- **Real-freeze end-to-end, measured this session** (fixture repo in scratch
  carrying the candidate draft bytes `a63c20c8` at `tools/mado-launchenv.py`
  and the lane execargv `49f7fecd`; real frozen cases `14b4cc57`; a 4-mutant
  scratch set `649ab775` anchored on real classes; the real generator
  `50126423`):

  ```
  MADO_LAUNCHENV_COUNT: TARGET_MET pred=PRED-C1-r99-v1
    rev=1945a771... (fixture head) base_rev=70c3703e...
    tool_sha256=a63c20c8... tool_pin=ok execargv_sha256=49f7fecd... execargv_pin=ok
    gio_sha256=d2164260... renderer_pin=ok renderer_sha256=cbfff7a4...
    cases=67 correct=67 classes=31/31
    mutants=4 killed=4/4 crashed_not_killed=0 survived=0 class_kills=23/31
    fresh=60/60 fresh_seed=245f9fa206a2c0a4
    census cases=ok classes=ok mutants=FAIL(static 4-set < 60; the official
      population is R99MMutC1's >=60 file, not yet landed when I ran)
    static_findings=none
    control_naive=1/67 control_held_r98=4/67
  ```
  rc 0, exit 0. Every PRED-C1-r99-v1 conjunct green on the real freeze with
  the real candidate draft: frozen 67/67, classes 31/31, my four real-class
  mutants all killed, fresh 60/60, both controls behind. The official scoring
  run is the L1's, at the landed rev with MutC1's frozen population; my run
  validates the instrument end-to-end on the real bytes.
- The rehearsal-B transcript block above is the retained evidence; the run
  itself lived entirely under
  `/fast/scratch/hyaku/mado-r99/R99MExecCounter` (deleted before yield).
- Lane `__pycache__` side-effects of my importlib debug runs removed; no tool
  installs or upgrades were needed (stdlib only).
