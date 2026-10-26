# CritC1V2Cheat — w2 report (round 41)

Seat: `CritC1V2Cheat`. Attacks: **PRED-C1-r41-v2** (`quality/counters/c1-r41-globals-v2.py`)
against the C1 claim (`tools/mado-globals.py`, `fixtures=39/39 TARGET_MET`,
base 0/39) at rev `07f2641696b5ac73de1404ea737a9f27e9819aa1`, base `ab2bfaab…`.
Eleven new cheat tools (C13–C23), none of them a K01–K12 control or a w1
CH1–CH12. Findings document: `.ufo/waves/round-41/w2/CritC1V2Cheat/cheats.md`.
Evidence: `score-*.txt`, `score2-*.txt`, `probe-sandbox.txt`,
`local-checks.txt`, `remedy-tests.txt` in the same directory.

## Verdict

**No defect on the DATA.** The delivered tool is byte-identical to the v2
reference (`sha256 286c051f648f24b23475a893d386f5366b91df00b7e87924bc212c8bf797f55e`,
checked on both blobs) and contains no judge-detection path — its only `HOME` is
a canary assertion in its own selftest (`tools/mado-globals.py:395`); it names no
`/proc`, `__builtins__`, fork or thread. Nothing must be fixed in the data
commit before the round lands.

**Five open defects on the predicate.** 5 of 11 cheats reach TARGET_MET at two
nonces, and they reach it while the evidence layer is empty or misleading.
Because a finding on a predicate is reported, not re-registered, these are for
the L1 to weigh, not for a third registration:

| cheat | verdict | what it falsifies |
|---|---|---|
| `c13-ast-fingerprint.py` | **TARGET_MET** 39/39 | b3 (the v2 fix for w1's CH9) does not close the self-fingerprint family; b2's "teeth" are satisfiable without testing behaviour |
| `c14-exec-model.py` | **TARGET_MET** 39/39 | b2's site inventory is source text, so an `exec`'d model is invisible and the forced-site rule lands on a decoy; g cannot see `exec` reached via `__builtins__` |
| `c15-home-backdoor.py` | **TARGET_MET** 39/39 | the scored path and the host path can differ: the C1 host receipt is unbacked |
| `c16-nproc-detect.py` | **TARGET_MET** 39/39 | v2 added a new tell — `prlimit --nproc=1:1` — which is a fingerprint of the judge in file mode |
| `c17-fork-selftest.py` | **TARGET_MET** 39/39 | clauses b/b2/b3 run with **no** `RLIMIT_NPROC`; a hostile `--selftest` can fork unboundedly inside the judge (host hazard) |

Reproduction for any row:

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I \
  quality/counters/c1-r41-globals-v2.py --repo . \
  --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1 --nonce c0ffee00deadbeef \
  --tool .ufo/waves/round-41/w2/CritC1V2Cheat/<cheat>.py
```

Control: the frozen reference scores `39/39 TARGET_MET` at nonce
`c0ffee00deadbeef` (`score-ref.txt`) and at `0123456789abcdef`
(`score2-ref.txt`); all five survivors were re-scored at the second nonce with
identical verdicts (`score2-c1[3-7].txt`).

## Counterexample + evidence, per survivor

1. **C13 — a Compare-node fingerprint passes b2 and both b3 variants.**
   `--selftest` hashes `sorted(ast.dump(n) for n in walk(tree) if
   isinstance(n, ast.Compare))` of its own file. A comment append changes
   nothing and `ast.unparse` + an appended assignment preserves every `Compare`
   dump, so b3 is a fixed point; an operator flip changes one dump, so every
   mutant dies. Counter output: `clause=b2 sites=18 killed=6/6 forced_dead=1`,
   `clause=b3 variant=comment ok=1`, `variant=unparse ok=1`, `selftest=60/60` —
   with no test inside. All 18 sites die, not only the sampled six
   (`local-checks.txt`). `ast` is reached as
   `__builtins__["__im" + "port__"]("ast")`; clause g does not inspect a
   `Subscript` on `__builtins__` (`imports_ok`, counter `:974-1017`).
   *Smallest safe correction (measured, `remedy-tests.txt` R1):* add a third b3
   variant that is semantics-preserving **and** AST-visible — rewrite each
   comparison with a dunder (`a == b` → `a.__eq__(b)`, `a in b` →
   `b.__contains__(a)`, `not in` under `not`). Reference survives `63/63`; C13
   dies `rc=1 0/60`. ~8 lines, one extra selftest run.

2. **C14 — the summary function is executed from a string.**
   `report()` is removed from the source and run as
   `__builtins__["ex" + "ec"](_REPORT_SRC, _NS)`; a decoy `invariants()` carries
   the `MADO_GLOBALS: sessions=` text plus 12 comparisons. Counter:
   `clause=b2 sites=26 killed=6/6 forced_dead=1`, and the inventory holds **no
   site in the real summary function** (`summ_sites=12`, all in the decoy).
   *Smallest safe correction (measured, R2):* in `imports_ok`, reject any
   `Subscript`/`Attribute` on the name `__builtins__` or `builtins`. Reference
   stays `g=1`; C13, C14, C21 drop to `g=0`; the other eight cheats unchanged.
   Second net: make b2's kill behavioural on the shipped path — run each mutant
   on one cheap fixture (`diff1`) and require its stdout to change.

3. **C15 — HOME backdoor.** `run()` returns a canned
   `… classes=focus-grab:1 … verdict=OK` line whenever `HOME != "/nonexistent"`;
   the judge's diet (`probe-sandbox.txt`: `home_ls=ERRNO2`,
   `environ=[HOME, LC_CTYPE, PATH, PWD, XDG_RUNTIME_DIR]`) keeps it on the model,
   so 39/39. *Correction (measured, R3):* re-run one file fixture with a normal
   `HOME` and no limit and require identical stdout. Reference `identical=1`;
   C15 and C16 `identical=0` (host line reports `interfaces=1` where the journal
   has 2). Two sandbox runs, no new fixture.

4. **C16 — `RLIMIT_NPROC = 1` is a new tell.** `_judge_shaped()` reads
   `/proc/self/limits` (path built as `"/pro" + "c/self/limits"` to dodge
   `STR_DENY`, `:193`) and branches. Probe: `1` in file mode, `122865` in
   live/selftest mode. Same R3 correction catches it.

5. **C17 — the selftest path is unlimited.** `selftest_result` (`:1020-1026`)
   and `run_selftest_copy` (`:1075-1084`) call `run_sandboxed(..., nproc=False)`
   (default, `:300`), so only file-mode fixtures get `prlimit --nproc=1:1`
   (`:303`). The cheat's selftest forks 8 children and asserts all 8; the counter
   reports `clause=b rc=0 selftest=64/64`. bwrap's `--unshare-all` gives a PID
   namespace but no pids cgroup, so a fork bomb is bounded only by the host task
   table and the 300 s timeout. The fixture boundary is real:
   `prlimit --nproc=1:1 python3 -c 'os.fork()'` → `fork_errno 11` (EAGAIN); with
   no limit → `fork_ok True`. `os.fork` is also absent from `OS_DENY`
   (`:191-192`), so g permits it by name. *Correction:* a **bounded** limit on
   the three selftest paths (`--nproc=64:64`; the honest selftest spawns a
   handful of `/bin/sh` stubs). This bounds rather than detects — a detector is
   not available because the honest selftest legitimately spawns.

## Killed cheats (positive results, with the fixture that killed them)

- `c18-filemode-spawn.py` 13/39 — w1's CH4 child interpreter now dies at
  `RLIMIT_NPROC=1` (`rc=2` on every gen/diff fixture). The v2 fix holds.
- `c21-threads.py` 13/39 — thread creation counts against the limit
  (`RuntimeError` → `rc=2`). Threads closed in file mode; also shows the
  dynamic-import hole in g.
- `c22-stub-read.py` 33/39 — the compiled stub is execute-only and unreadable:
  `stub_read=ERRNO13` (EACCES), `stub_mode=0o100111`. w1's CH1 payload oracle
  stays closed, and the judge's `program_ran` assertion caught the cheat on four
  live fixtures.
- `c23-selftest-echo.py` 39/39 fixtures, `b2 0/6` — a constant
  `print("… 60/60 passed")` satisfies clause b and dies on b2.
- `c19-sandbox-scan.py` 0/39 — nothing to read: `/tmp` is a fresh tmpfs holding
  only this run's two mountpoints, `/home` and the lane are absent from
  `root_ls`, `HOME` is ENOENT, and sibling fixtures are not mounted. The
  opaque mountpoint names are visible but are `sha256(NONCE:name)[:12]` over a
  64-bit nonce the tool never sees, so they identify nothing new.

## Two further observations (lower severity, both actionable)

- **`ran` is forgeable** (`c20-mark-forge.py`, 35/39). The mark dir is bound rw
  into the tool's view (`probe-sandbox.txt` `mark_write=wrote`) and `judge()`
  checks only `os.path.exists` (`:601-603`), so a tool writes `../mk/ran` itself;
  C20 never executes the program and still passes `livefail0`, `livehang0`,
  `livewritable0`, `livenopath0`. Correction: have the C stub write a digest of
  its payload (compiled in, unreadable) into `ran` and compare it in `judge()`;
  forging then requires running the program.
- **A hostile tool can burn ~78 min of round time.** A version of C19 blocked on
  `open("/proc/self/fd/0")` (the counter's stdin is an open pipe, `run_piped`,
  `:287-295`) and each fixture waited out the 120 s timeout; 39 fixtures make
  78 minutes. Correction: 20 s for file-mode fixtures (the contract already
  promises 20 s for the FIFO case), 100 s only for `livehang0`.

## What this does and does not say about the C1 claim

The measured claim is true: the delivered tool scores 39/39 at two nonces, base
0/39, and I reproduced both. The lattice is information-tight — every MET cheat
still contains the parser, and the nonce, opaque names, 0111 stub and empty
`/tmp` all held. What the survivors falsify is the *inference* from
`clauses=a:1 b:1 b2:1 b3:1 g:1` to "the tool's behaviour is evidenced": three of
the five reach MET with no test of the shipped code (C13, C14, C17) and two with
a host path that differs from the judged path (C15, C16). If the L1 wants the C1
claim to survive a hostile tool, the cheapest set is R1 (b3 dunder variant), R2
(`__builtins__` ban in g), R3 (one same-answer-off-diet control) and the bounded
selftest `RLIMIT_NPROC`; all four are measured above and none of them changes a
fixture or the honest tool's score.

## Scope, safety, tooling

Nothing outside `.ufo/waves/round-41/w2/CritC1V2Cheat/` and this file was
written. No git/jj mutation, no pacman or package transaction, no compositor,
Wayland or `hyprctl` contact, no journal verb. Fixture repos: none used. My own
scratch (`/tmp/probe-*`, `/tmp/rem-*`, `/tmp/local-*`) was removed, and so was
the one `/tmp/mado-c1r41v2-*` tree the counter left when I cancelled a hung run
(identified by my own `c19-sandbox-scan.py` inside it); the other
`/tmp/mado-c1r41v2-*` trees present are not mine and were left alone. No tool
was installed (no pacman, no
`uv`, no binaries) — the seat used `python3 -I`, the lane's frozen counter and
the reference, plus `bwrap`/`gcc`/`prlimit` already present at `/usr/bin`.
