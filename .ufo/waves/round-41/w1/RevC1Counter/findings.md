# RevC1Counter — findings on `quality/counters/c1-r41-globals.py` (frozen)

Counter read end-to-end (855 lines). Cheats built in this seat dir. Repros use
the counter's own module functions (`importlib` import of the frozen file,
read-only) or plain `bwrap` probes; nothing in the lane was written.

---

## 1. Clause b2 is vacuous — a selftest can kill every mutant without testing

- **Severity:** HIGH (predicate clause b2 does not constrain the tool).
- **Line:** `teeth()` at 754-779; `function_sites()` 727-737; `NOT_SITES` 721;
  `selftest_result()` 712-718.
- **Why:** mutants are written by the judge to `<tmp>/mut<i>/mado-globals.py`
  (754-760) and run from there; the tool's `--selftest` can read
  `basename(dirname(abspath(__file__)))` and exit 1 if it contains "mut". The
  required >=12 comparison sites (MIN_SITES=12, line 128) can be placed in a
  function the selftest never calls.
- **Reproduction:** `cheat_selfcopy.py` (13 sites in uncalled `dummy()`; 30/30
  selftest in normal dir; `["mut" in here] -> return 1`):
  - `len(function_sites(src)) == 13`
  - counter's own `teeth(src, tmp, nonce)` prints `killed=6/6` and returns
    `True`.
  - In its normal tool-dir run the same source's selftest passes (k==n=30),
    so clause b also holds.
- **Impact:** a tool can pass b2 with zero real test teeth; the clause's
  "comparison flips must break the selftest" premise is unenforceable against a
  self-aware tool. (The M39 control only covers an echo selftest, not this.)

## 2. Clause g is bypassable at AST level (getattr / kwargs / subscript)

- **Severity:** HIGH (g is the only static gate against arbitrary execution).
- **Lines:** `imports_ok()` 679-709; denylists 135-140.
- **Why:** the AST checks only match `Call(Name=os, attr in OS_DENY/exec*)`,
  `Call(Name in CALL_DENY)` (incl. on `builtins`), and keyword args with
  `kw.arg == "shell"` (700-705). They miss:
  - `getattr(os, "sys" + "tem")("hostname")` — Call func is `Name=getattr`.
  - `subprocess.run("x", **{"shell": True})` — `kw.arg is None`.
  - `globals()["eval"]("...")` — Subscript, not Name/Attribute.
- **Reproduction:** `imports_ok(open("clause_g_bypass.py").read()) == True`
  and `imports_ok('import subprocess\nsubprocess.run("x", **{"shell": True})\n')
  == True` (printed by the counter's own function).

## 3. Declared residual is real: live fixtures pass without running journalctl

- **Severity:** HIGH (filed as residual in registration; concretely buildable).
- **Lines:** `prepare()` 459-478 writes `fx/journal.txt` (plaintext) alongside
  the stub; `live_stub` 444-457 embeds the journal as base64; `score_live*`
  652-676.
- **Reproduction:** `cheat_decoder.py` reads `dirname(dirname(argv[--journalctl]))/journal.txt`
  (never spawns a process). Counter's own `execute`+`judge` on a generated
  `live0` fixture: `rc=0 ok=1 why='ok'` — byte-exact match, zero spawned
  processes. (Also passes live1 by locating the stub via PATH.)
- **Note:** this is exactly the declared residual ("a tool that decodes it
  without running it passes"); confirming it is cheap and total for live0/live1.

## 4. Fixture identity is learnable (name oracle) — fixed fixtures collapse

- **Severity:** MEDIUM-HIGH (defeats the "fixed fixture" discrimination).
- **Lines:** `run_sandboxed` 235-244 mounts scratch ro; `prepare()` names dirs
  `gen0..gen7`, `diff0`, `usage0`, `badexpect0`, `live0`… at 459-478.
- **Why:** the fixture dir is a real directory (not hidden); the tool's own
  path is `<scratch>/tool/mado-globals.py`, and the scratch root lists every
  fixture directory as a sibling.
- **Reproduction (bwrap, exact judge layout):** with the tool at
  `/tmp/mado-c1r41-XXXXXX/tool/mado-globals.py` and fixtures `gen0`,`live0`
  as sibling dirs of the scratch root:
  - `os.path.abspath("tool/mado-globals.py")` → the path above,
  - `os.path.basename(os.path.dirname(me))` → `tool`,
  - `os.listdir(os.path.dirname(os.path.dirname(me)))` →
    `['gen0', 'live0', 'tool']` — every fixture name is visible.
- **Impact:** a tool can contain a switch: usage0/badexpect0/unreadable0/
  toolarge0/live* emit the expected `SETUP`/verdict lines by fixture name; only
  gen0-7 require real parsing. The 16 "fixed" fixtures become lookup tables, so
  they no longer discriminate implementations. (Not covered by any control:
  all 43 mutants are single-edit defects of the reference, not oracle tools.)

## 5. Sandbox is detectable → judge-vs-host behavior split

- **Severity:** MEDIUM (undermines the "sandbox is the boundary" premise).
- **Lines:** `sandbox_cmd` 195-210 (`--clearenv --setenv HOME /nonexistent`,
  fresh /proc /dev, tmpfs /tmp); `execute` 481-487 (env with XDG_RUNTIME_DIR).
- **Reproduction (bwrap):** inside the judge's exact sandbox shape:
  - `HOME=/nonexistent`, `/home` does not exist,
  - `os.listdir("/dev") == ['core','fd','full','null','ptmx','pts',…]`
    (minimal),
  - `/usr` is not writable; `/proc/mounts` shows the bwrap layout.
  Any of these is enough to branch: behave as a real tool on a host, cheat under
  the judge. The counter cannot detect this because the tool never runs outside
  the sandbox.
- **Impact:** a hostile tool passes the predicate while being non-functional on
  a real desktop; the counter scores only sandboxed behavior.

## 6. Docstring sentences with NO fixture exercising them

- **Severity:** LOW-MEDIUM (coverage gaps; each is a docstring sentence).
- 1. "A non-zero exit, **a spawn failure or a timeout** is SETUP
     journalctl_failed (exit 5)" — livefail0 exercises only non-zero exit; no
     fixture makes `subprocess.run` raise or time out. (Lines 652-676, 174-189
     of reference.)
- 2. "…resolved to an absolute regular executable file that is not group- or
     other-writable, **otherwise journalctl_unusable**" — the "not found in
     PATH" branch is never exercised (live1 always finds `fx/bin/journalctl`;
     livewritable0 only exercises the writable branch).
- 3. "**the program is not run**" (on unusable program) — judge only checks the
     stdout/rc; a tool that runs a writable stub and prints a synthetic
-     `journalctl_unusable` line passes livewritable0.
- 4. "`ver_changed=<name:old>new csv|->`" — a NON-empty ver_changed is never
     deterministically produced: gen fixtures sample versions with
     `rng.randrange`; overlap with differing max versions is probabilistic, not
     guaranteed (gen_fixture 359-429; model_diff 286-298). A tool that always
     prints `ver_changed=-` will pass most runs by luck.
- 5. "The tree the tool reads is mounted read-only" — environmental, never
     asserted by any fixture (a tool could write into `fx/` and still pass
     everything).
- 6. "coverage comes from a deterministic lattice on the fixture index" — meta
     statement, not fixture-testable (harmless).

## 7. Vacuous / near-vacuous fixtures

- **Severity:** LOW.
- A tool that reads only the **first line** of the journal passes:
  - `nosess0` (line 578-583): first line is noise -> NO_SESSIONS wins over
    MISSING_EXPECTED (the actual assertion).
  - `nosess1` (586-588): empty file -> NO_SESSIONS.
  - `toolarge0` accept phase (622-632): `x`-filled 8 MiB file -> NO_SESSIONS
    (the size-boundary is asserted by phase 1, not parsing).
- `unreadable0`/`usage0`/`badexpect0` never parse a journal at all (they assert
  CLI/IO behavior).
- These fixtures remain meaningful (each pins a distinct contract), but none
  exercises multi-line parsing; a degenerate parser passes them.

## 8. Robustness defects (docstring-vs-code fidelity)

- **Severity:** LOW-MEDIUM.
- `check_sandbox()` (213-220): if `bwrap` is missing, `subprocess.run` raises
  `FileNotFoundError` — not caught, so the counter crashes with traceback and
  exit 1 instead of the documented `SETUP … / exit 2`.
- `resolve()` (187-191): raises `Setup("unresolved revision …")` already for
  an unresolvable `--rev` (correct), but `git()` (181-184) returns None on any
  git failure; callers outside `resolve` (e.g. `git show` at 820-823) pass None
  to `open(...)` -> AttributeError traceback, not SETUP.
- `teeth()` kill test (774): a mutant is considered dead iff `rc != 0 or not
  has or k < n_`; a mutant printing **more** than its total (`k > n_`) is NOT
  dead — the "k < n" docstring wording is implemented as `k < n_` only, so an
  over-claiming selftest survives.

## 9. Minor / observations

- `live_stub` env guard tolerates `PWD`, `SHLVL`, `_`, `OLDPWD` beyond the
  docstring's four variables (444-457); necessary for `/bin/sh`, so the
  docstring's "environment limited to …" is approximate.
- The "no shell" claim is not enforced: `subprocess.run(["sh","-c", …])` and
  `bash -c` produce a `sh`-parented stub that passes the `$*` check; clause g
  only bans `shell=True` (AST), not `sh -c`.
- In file mode the prohibition is only enforced for `journalctl` via PATH
  (decoy `fx/bin/journalctl`, `STUB_FILE` 441, `judge` 491-494); a tool may
  spawn any other process (e.g. `cat`, `ls`) undetected — the docstring says
  "must not start any process".
- `--tool PATH` controls bind the controls directory read-only into the sandbox
  (`execute` ro=`dirname(tool)`, 481-487); a control tool can read sibling
  files in `c1/` (benign for controls, but a deviation from "sees neither the
  lane, nor this counter").
- `imports_ok` scans **all** imports (not just top-level) and fails a tool with
  zero imports (`bool(mods) and …`, 709) — stricter than the docstring in both
  directions.
- `score_badexpect0` (611-619) tests 5 cases while the docstring lists 3
  (`--expect=a b`, `--expect=`, 129-char); the extra `--expect=a;b`,
  `--expect=a/b` are harmless but undocumented.
- Nonce: not discoverable by the tool (it is printed only on the judge's final
  line, outside the sandbox; journal content is what matters, not the nonce).
- Model-vs-docstring check: session splitting, per-name max-ver/count, diff
  fields, classes, verdict precedence (NO_SESSIONS > MISSING_EXPECTED), and
  byte-exact stderr-empty-on-0/1/3 all match the docstring exactly for the
  sentences that have fixture coverage.

## Verification status

- `bwrap 0.13.1`, `git`, `python3` present; no installs performed (no package
  transactions).
- Repros run: sandbox fingerprint (bwrap), fixture-name visibility (bwrap,
  judge layout), `imports_ok` bypasses, live0 decode-cheat, `teeth()` b2
  cheat. All read-only w.r.t. the lane; no lane/fleet/repo mutation.
