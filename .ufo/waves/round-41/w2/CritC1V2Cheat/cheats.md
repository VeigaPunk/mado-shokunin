# CritC1V2Cheat — can PRED-C1-r41-v2 reach TARGET_MET without evidenced work?

Round 41, wave w2, seat `CritC1V2Cheat`. Lane `mado-shokunin`. Attacked: the
frozen predicate `PRED-C1-r41-v2` (`quality/counters/c1-r41-globals-v2.py`) at
rev `07f2641696b5ac73de1404ea737a9f27e9819aa1` (base `ab2bfaab…`). Nothing
outside `.ufo/waves/round-41/w2/CritC1V2Cheat/` was written; the counter,
controls, registration, reference and fetch receipts were read only. No git/jj
mutation, no pacman, no compositor or Wayland contact, no journal verb.

## Answer first

**Eleven new cheats; five reach TARGET_MET at two nonces.** All five keep a
correct model — the fixture lattice is still information-tight, and no cheat
answers a fixture without parsing its journal. What they break is the *evidence
layer*, which is the layer the C1 claim rests on:

| # | cheat | fixtures | clauses | verdict |
|---|---|---|---|---|
| C13 | `c13-ast-fingerprint.py` | **39/39** | a1 b1 **b2 6/6** **b3 2/2** g1 | **TARGET_MET** |
| C14 | `c14-exec-model.py` | **39/39** | a1 b1 **b2 6/6** b3 2/2 **g1** | **TARGET_MET** |
| C15 | `c15-home-backdoor.py` | **39/39** | a1 b1 b2 6/6 b3 2/2 g1 | **TARGET_MET** |
| C16 | `c16-nproc-detect.py` | **39/39** | a1 b1 b2 6/6 b3 2/2 g1 | **TARGET_MET** |
| C17 | `c17-fork-selftest.py` | **39/39** | a1 b1 b2 6/6 b3 2/2 g1 | **TARGET_MET** |
| C20 | `c20-mark-forge.py` | 35/39 | a1 b1 b2 6/6 b3 2/2 g1 | MISSED |
| C22 | `c22-stub-read.py` | 33/39 | a1 b1 b2 6/6 b3 2/2 g1 | MISSED |
| C18 | `c18-filemode-spawn.py` | 13/39 | a1 b1 b2 6/6 b3 2/2 g1 | MISSED |
| C21 | `c21-threads.py` | 13/39 | a1 b1 b2 6/6 b3 2/2 g1 | MISSED |
| C23 | `c23-selftest-echo.py` | 39/39 | a1 b1 **b2 0/6** b3 2/2 g1 | MISSED |
| C19 | `c19-sandbox-scan.py` | 0/39 | a1 **b2 no summ site** | MISSED |

**No finding on the DATA.** The delivered tool is byte-identical to the v2
reference (`sha256 286c051f…f55e`, both from `git show 07f2641:tools/mado-globals.py`
and `c1/ctl-ref-tool-v2.py.txt`), and that binary carries no judge-detection path:
the only `HOME` in it is a canary assertion inside its own selftest
(`tools/mado-globals.py:395`), and it names no `/proc`, `__builtins__`, fork or
thread. So the five survivors are **open defects on the predicate** (no third
registration), not on the delivered artifact.

Three of them (C13, C14, C17) are MET with **no test of the shipped code at
all**; two (C15, C16) are MET while the code path that would run on the host
produces a *different, unfounded* report. Concretely, `clauses=a:1 b:1 b2:1 b3:1
g:1` is satisfiable by a tool whose `--selftest` is a hash of its own syntax
tree, whose model is a string, and whose `--live` on the host is a canned line.

## Method

Each cheat is the frozen reference with one localized patch, so every score
isolates one hole. `make_cheats.py` asserts the reference sha256 before patching
and asserts each anchor matched exactly once; `ast.parse` validates every
generated tool. Scored with one fixed nonce so all eleven see the same 39
fixtures and the same b2 sample:

```
python3 -I quality/counters/c1-r41-globals-v2.py \
  --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
  --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1 \
  --nonce c0ffee00deadbeef \
  --tool .ufo/waves/round-41/w2/CritC1V2Cheat/<cheat>.py
```

Controls: the frozen reference scores `fixtures=39/39 … verdict=TARGET_MET` at
this nonce (`score-ref.txt`, exit 0) and at `0123456789abcdef`
(`score2-ref.txt`), so the lattice and the b2 sample are intact. Every MET cheat
was re-scored at the second nonce (`score2-c1*.txt`): identical verdicts and
identical fixture counts. Full outputs: `score-*.txt`.

Two probes give the *inside* of the judge's own sandbox, using the counter's
`sandbox_cmd`/`prepare` (so mount set, cwd, env and RLIMIT are exactly the
judge's): `probe-sandbox.py` → `probe-sandbox.txt`; and `remedy-tests.py` →
`remedy-tests.txt` tests each proposed remedy against the cheats **and** against
the reference.

## Survivors

### C13 — b3 is blind to a structural fingerprint (MET, 39/39)

Attacks `neutrality()` (`c1-r41-globals-v2.py:1119-1133`), the v2 clause that
was added to kill w1's CH9 self-fingerprint, and the b2 kill criterion
(`teeth()`, `:1087-1116`).

The selftest reads its own file and hashes the sorted `ast.dump()` of every
`Compare` node. Both b3 transforms are **AST-inert for comparisons**: appending
`# b3-neutral …` changes nothing, and `ast.unparse(ast.parse(src))` plus a
top-level `B3_NEUTRAL_x = 1` preserves every `Compare` dump. A b2 mutant flips
one operator, so exactly one dump changes. Result: `clause=b2 sites=18 killed=6/6
forced_dead=1`, `clause=b3 variant=comment ok=1`, `variant=unparse ok=1` — and
nothing is tested (`selftest=60/60` is a constant print either way). All 18
sites die, not just the sampled six (`local-checks.txt`).

`ast` is not in `STDLIB_ALLOW` (`:186-189`), so the cheat reaches it through
`__builtins__["__im" + "port__"]("ast")` — clause g does not look at a
`Subscript` on `__builtins__` (`imports_ok`, `:974-1017`).

Reproduce: `python3 -I quality/counters/c1-r41-globals-v2.py --repo . --rev
07f2641… --nonce c0ffee00deadbeef --tool .ufo/waves/round-41/w2/CritC1V2Cheat/c13-ast-fingerprint.py`
→ `score-c13.txt`, exit 0.

Cheapest remedy (**tested, R1**): add a third b3 variant that is
semantics-preserving *and* AST-visible — rewrite every comparison with a dunder
(`a == b` → `a.__eq__(b)`, `a in b` → `b.__contains__(a)`, `not in` wrapped in
`not`) and require the selftest to still pass. Measured: the reference still
passes (`63/63`), C13 fails (`rc=1 0/60`) → `remedy-tests.txt` R1. Cost: one
more selftest run, ~8 lines reusing the existing walker. A cheaper *partial* net
(w1's CH9 remedy, still unimplemented) is to reject `open()` whose argument
subtree mentions `sys.argv`/`__file__`; it is evadable through a dynamic import
of `linecache`, so it is a first net only. The sound version is the b2 change in
C14's remedy (site must be on the shipped path).

### C14 — b2's site inventory is text, not code; g cannot see `exec` (MET, 39/39)

Attacks `function_sites()`/`teeth()` (`:1035-1116`) and `imports_ok`
(`CALL_DENY`, `:190`).

`report()` — the only function whose body holds `MADO_GLOBALS: sessions=` — is
removed from the source and executed from a string constant:
`_NS = {"classify": classify}; __builtins__["ex" + "ec"](_REPORT_SRC, _NS)`.
The counter's inventory therefore sees **no site at all** in the real summary
function; a decoy `invariants()` carrying the summary text and 12 comparisons
becomes the only forced-site candidate (`clause=b2 sites=26 killed=6/6
forced_dead=1`, `local-checks.txt`: all 26 die, `summ_sites=12`, all in the
decoy). Clause g passes (`g=1`) because `CALL_DENY` only matches the literal
`Name`/`Attribute` forms, and `__builtins__` is not in `NAME_DENY` (`:194-195`).

Reproduce: `--tool …/c14-exec-model.py` → `score-c14.txt`, exit 0.

Cheapest remedy (**tested, R2**): in `imports_ok`, reject any `Subscript` or
`Attribute` whose value is the name `__builtins__` or `builtins` — three lines,
no honest census tool needs it. Measured: the reference stays `g=1`; C13, C14
and C21 drop to `g=0`; the other eight cheats are untouched (`remedy-tests.txt`
R2). Second net for the decoy (not just this cheat): make b2's kill
*behavioural on the shipped path* — run each mutant on one cheap fixture (e.g.
`diff1`) and require its stdout to change, so a site in dead code or in an
exec'd string can never be "killed".

### C15 — a HOME backdoor makes the host receipt unbacked (MET, 39/39)

Attacks the declared residual (`:153-157`, "the sandbox is detectable
(HOME=/nonexistent)") at the level of the *claim*: C1 is operability, and the
only host evidence is `--live` on the running desktop, which is produced by the
same binary that can branch on `HOME`.

`run()` returns a canned `… classes=focus-grab:1 … verdict=OK` line whenever
`HOME != "/nonexistent"`; under the judge the model runs, so all 39 fixtures
pass. The tell is real: `probe-sandbox.txt` shows `home_ls=ERRNO2` and
`environ=['HOME', 'LC_CTYPE', 'PATH', 'PWD', 'XDG_RUNTIME_DIR']`.

Reproduce: `--tool …/c15-home-backdoor.py` → `score-c15.txt`, exit 0; and R3 in
`remedy-tests.txt`: same tool, same journal, judge diet vs normal diet →
`identical=0`, the host line reports `interfaces=1` where the journal has 2.

Cheapest remedy (**tested, R3**): one extra control per run — re-run a single
file fixture with `HOME` set to a normal value and no `RLIMIT_NPROC`, and
require byte-identical stdout. Measured: reference `identical=1`; C15 `identical=0`.
Cost: two sandbox runs, no new fixture. (Claim-level: the C1 host receipt should
be taken under the same sandbox with a normal `HOME`, so the scored path and the
receipt path are the same path — an L1 decision, not a counter edit.)

### C16 — v2 added a new tell: `RLIMIT_NPROC = 1` (MET, 39/39)

Attacks `run_sandboxed()`'s new `prlimit --nproc=1:1` lead (`:299-303`).

`_judge_shaped()` reads `/proc/self/limits` (string built as `"/pro" + "c/self/limits"`
to dodge `STR_DENY`, `:193`) and branches: with a limit and `HOME` normal it
returns the canned line, otherwise the model. `probe-sandbox.txt`:
`nproc_limit=['Max','processes','1','1','processes']` in file mode versus
`122865` in live/selftest mode — so the file-mode boundary introduced by the v2
CH4 fix is itself a fingerprint of the judge.

Reproduce: `--tool …/c16-nproc-detect.py` → `score-c16.txt`, exit 0; R3 →
`identical=0`.

Cheapest remedy: the same R3 control (it catches both C15 and C16 with one
extra run). A static net is not available here: reading `/proc` is not
forbidden by clause g beyond the literal string, and building the path is one
`+`.

### C17 — the selftest path has no RLIMIT_NPROC at all (MET, 39/39; host hazard)

Attacks `selftest_result()` (`:1020-1026`) and `run_selftest_copy()` (`:1075-1084`):
both call `run_sandboxed(..., nproc=False)` by default (`:300`), so clauses b,
b2 and b3 execute with **no process limit**, while file-mode fixtures run under
`1`. `os.fork` is also absent from `OS_DENY` (`:191-192`), so clause g permits
it by name.

The cheat's selftest forks 8 children and asserts `kids == 8`; the counter
reports `clause=b rc=0 selftest=64/64`, i.e. all eight forks succeeded inside the
judge's sandbox. bwrap's `--unshare-all` gives a private PID namespace but no
pids cgroup, so a *fork bomb* there is bounded only by the host task table and by
the counter's 300 s timeout — a hostile tool can degrade the machine the round
runs on. The boundary is real for fixtures only: `prlimit --nproc=1:1 python3 -c
'os.fork()'` → `fork_errno 11` (EAGAIN), and with no limit → `fork_ok True`.

Reproduce: `--tool …/c17-fork-selftest.py` → `score-c17.txt`, exit 0.

Cheapest remedy: pass a **bounded** limit to the three selftest paths —
`prlimit --nproc=64:64` (the honest reference spawns at most a handful of
`/bin/sh` stubs; 64 is ample) — one argument each for `selftest_result` and
`run_selftest_copy`. This *bounds* the hazard rather than detecting it; a
detector is not available because the honest selftest legitimately spawns.

## Killed cheats — what the predicate got right

- **C18, child interpreter in file mode (13/39).** w1's CH4 trick, replayed
  against v2: `read_file` delegates to `/usr/bin/python3 -I -c …`. Every gen/diff
  fixture returns `rc=2` (the spawn fails, `Setup unreadable`); the 13 that pass
  are the SETUP-only fixtures. `RLIMIT_NPROC=1` closes the v1 hole.
- **C21, threads (13/39).** `_thread.start_new_thread` raises `RuntimeError`
  under the limit, so every file fixture returns `rc=2`. Threads are counted
  against `RLIMIT_NPROC`, so the same limit closes them. It also shows the
  dynamic-import hole in g (`_thread` is not in `STDLIB_ALLOW`) — see C14's R2.
- **C22, stub bytes (33/39).** The compiled stub is execute-only and unreadable
  by the tool: `probe-sandbox.txt` `stub_read=ERRNO13` (EACCES), `stub_mode=0o100111`.
  w1's CH1 payload-oracle family stays closed. The judge's `program_ran`
  assertion then caught the cheat on four live fixtures (`program_ran=False
  want=True`) — that assertion is load-bearing.
- **C23, constant `--selftest` (39/39 fixtures, b2 0/6).** `print("… 60/60
  passed"); return 0` satisfies clause b outright and dies on b2 (`killed=0/6
  forced_dead=0`). Clause b alone is worth nothing; b2 is what makes it mean
  something.
- **C19, sandbox scan (0/39).** No answer is reachable: `/tmp` is a fresh tmpfs
  holding only the two mountpoints this run created (`tmp_ls=['probe-gen0-…']`,
  `grandparent_ls=[<tool-parent>, <fixture>]`), `/home` and the lane are absent
  from the root listing (`root_ls=['bin','dev','lib','lib64','proc','tmp','usr']`),
  `HOME` is ENOENT, and the fixture's `fx` holds only the input. Sibling
  fixtures are not mounted, so the v1 sibling-leak stays closed. The tool does
  see the *names* of this run's two mountpoints under the tmp root
  (`<opaque("real")>` and `<opaque(fixture)>`), but each is
  `sha256(NONCE:name)[:12]` (`opaque()`, `:565-567`) with a 64-bit nonce the tool
  never sees, so the name identifies nothing it does not already hold (the
  fixture's own journal).

## Two further observations

1. **`ran` is forgeable (C20, 35/39).** The mark directory is bound rw into the
   tool's view (`probe-sandbox.txt` `mark_write=wrote`) and `judge()` checks only
   `os.path.exists` (`:601-603`), so a tool can write `../mk/ran` itself. C20
   never executes the program and still passes `livefail0`, `livehang0`,
   `livewritable0` and `livenopath0`. Severity is low today — the three fixtures
   that need the payload still need the payload — but the record is not evidence.
   Cheapest remedy: have the C stub write a digest of its payload (compiled in,
   unreadable: EACCES) into `ran`, and compare that in `judge()`; forging then
   requires knowing the payload, i.e. running the program.
2. **A hostile tool can burn ~78 min of round time.** My first C19 version
   blocked on `open("/proc/self/fd/0")` (the counter's stdin is an open pipe,
   `run_piped`, `:287-295`) and each fixture waited out the 120 s timeout; 39
   fixtures make that 78 minutes before the counter reports `TARGET_MISSED`.
   Cheapest remedy: a 20 s timeout for the file-mode fixtures (the contract
   already promises 20 s for the FIFO case) and keep 100 s only for `livehang0`.

## Scope and limits

- I did not run `--live` against the compositor, by rule; every host-side claim
  here is made inside the judge's own sandbox with the judge's own fixtures, or
  with a journal file.
- The five survivors need the model; none of them answers a fixture without
  parsing its journal. The nonce lattice, the opaque fixture names, the 0111
  stub and the empty `/tmp` all held.
- `remedy-tests.py` R1/R2/R3 are measured; the `ran`-digest and timeout remedies
  are reasoned from the measured EACCES and the measured hang, and are labelled
  as such.
- No tools were installed for this seat (no pacman, no `uv`, no binaries).
