# AttackNoExec — supplied argv never reaches a subprocess; selftest child is the fixed script only

Seat `MadoR16.AttackNoExec` (UFO-FSD critic, leaf). Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
Source reading only. I did not run the gate, `--selftest`, `--frozen`, a fixture, measure.py, a probe,
or any interpreter check. I installed nothing and ran no package or service operations. I edited no
file except this report. I read `corpus/lessons/round-15-verifier-spotcheck.md` before starting.

## Snapshot under review (the file was being edited while I read it)

`tools/mado-action-plan.py` is untracked and was edited three times while I reviewed it:

| Observation | sha256 | Lines | mtime (-0300) |
|---|---|---|---|
| first full read | (not hashed) | 752 | 05:46 |
| second | `4ce2a2335d62ecde816794814add97667a37c82de85f9174cd0348a873414559` | 760 | 05:52:57 |
| **final, anchors below** | `eee51dda87bd19ffb86b826d984ad99faf2dd2061d753e80235c1131f39257aa` | 779 | 05:53:23 |

The edits between snapshots:
- `O_NOFOLLOW` added to `_read_regular`.
- `_evaluate_raw` split out of `_evaluate`.
- `--frozen` changed to read each file once, then hash and classify the same bytes.

None of these edits added an execution sink. L1 should re-check the anchors against the bytes it
commits.

## Verdict on the assigned property

**The property holds on the final snapshot. No supplied argv reaches a subprocess.** There is one
subprocess sink and one way to reach it. The selftest child, though, is identified by a path that is
re-read from disk. It is not bound to the bytes being tested (F1), so the claim "fixed script only"
is weaker than stated.

### Sink inventory (final bytes)

- `import subprocess` at :75. The only call is `subprocess.run` in `_self_invoke` (:490–497):
  - argv: `[sys.executable, "-I", script, *args]`, `shell=False`
  - `stdin=DEVNULL`, `timeout=60`, `cwd=tmp`, `env={"PATH": …}`
- `_self_invoke` is called only from `run_selftest`, at :660 and :734.
- `run_selftest` takes no parameters. `main` (:755) routes `--selftest` to it with no arguments.
- I grepped for `os.system`, `os.exec*`, `spawn`, `Popen`/`popen`, `eval(`, `exec(`, `__import__`,
  `importlib`, `pickle` and `shutil`. There are no hits other than the call above.

### Data-flow trace: plan argv (the declared actions)

1. JSON bytes go through `_read_regular`, `_parse_json_bytes`, `_validate_plan` and `_classify` (:327).
2. In `_classify`, `argv[0]` only passes through `_basename` (:319) and a frozenset membership test:
   `strip`, `rstrip("/")`, `rsplit("/", 1)`.
3. The kind or executable can appear in the output only in limited forms:
   - `finding` strings render a kind from `PINNED_KINDS` or an executable from the pinned deny set.
   - An unknown kind appears only as `repr()` in `detail`.
   - `detail` reaches stdout only through `json.dumps`.
   - The `MADO_PLAN:` line prints `finding` only. Hostile kind or argv strings therefore cannot inject
     lines or verdicts into stdout.

### Data-flow trace: CLI argv (`--plan`, `--policy`, `--frozen`)

- Paths go only to `os.open`/`os.fstat`/`os.read` (:150–) and `os.path.join`/`abspath` in `run_frozen`
  (:402).
- `run_frozen` classifies in-process through `_evaluate_raw`. It does not re-invoke itself.
- argparse has no `fromfile_prefix_chars`, so `@file` expansion does not apply.
- The selftest receives none of the CLI values.

### Selftest child arguments

The child gets only:
- the fixed flags `--plan`/`--policy`/`--frozen`;
- paths built as `os.path.join(tmp, f"{name}.plan.json")` from literal case names;
- `tmp` itself, for the `__DIR__` case.

`tmp` comes from `tempfile.TemporaryDirectory`. `tempfile` makes `TMPDIR` absolute, so every child
operand starts with `/` and cannot be parsed as an option. The fixture actions (`sudo pacman …`,
`systemctl`, `evtest`, `curl`) are written only as JSON data into temp files. The child classifies
them in-process, and nothing executes them.

### Child isolation

From `/usr/share/man/man1/python3.14.1.gz`: `-I` implies `-E`, `-P` and `-s`. So the child's
`sys.path` has neither the script directory nor user site-packages, and all `PYTHON*` variables are
ignored. A shadow module such as `tools/json.py` cannot hijack the child.

## Counterexamples

### F1 — Medium: the selftest child's script identity is not bound to the bytes under test

Anchor: `script = os.path.realpath(__file__)` (:502), then a fresh exec of `script` for each of the
~40 cases (:660, :734).

**(a) Concurrent edits.** Each child re-reads the gate from disk. The parent never hashes it, and
nothing compares it before and after the run.
- If the file changes during a selftest, different cases test different bytes.
- The SKILL registry row (`SKILL.md:530`) says the receipt "separately binds executable … digests to
  measured commit". That digest is taken at a different time from the child runs.
- This is not hypothetical in this round: I saw three different contents within about 2 minutes
  (table above). A selftest run during that window is false provenance. Its summary line names no
  digest.

**(b) No script file.** If the gate runs without a real script file, `__file__` does not name the gate.
- Piped run: `python3 -I - --selftest < tools/mado-action-plan.py` sets `__file__` to `"<stdin>"`.
  `realpath` then turns it into `$PWD/<stdin>`. [INFERENCE: CPython's `_PyRun_SimpleFileObject` sets
  `__file__` to the filename `<stdin>`; not executed here.]
  - If no file with that name exists, every child fails and the selftest fails closed.
  - If a file named `<stdin>` exists in the working directory, that arbitrary script runs as the
    "self" child. It can print the pinned verdict lines and turn the selftest green without the gate
    being tested.
- `python3 -c "$(cat …)" --selftest`: `NameError` traceback, which fails closed.

Neither case lets supplied plan or CLI argv reach the subprocess. Both break "child = fixed script
only" and the selftest-as-evidence claim.

**Smallest correction** (in `run_selftest`, about 8 lines):
1. Read `os.path.realpath(__file__)` once through `_read_regular`. If it fails, print a
   `SELFTEST_ERROR` line and return 1.
2. Compute `sha256` of those bytes.
3. Write the bytes to `tmp/gate-under-test.py` and pass that path to every `_self_invoke`.
4. Print `SELFTEST_SCRIPT_SHA256: <hex>` before `SELFTEST_SUMMARY`.

The children then run exactly the hashed bytes, and later edits on disk cannot mix into the run. The
receipt can compare the printed digest with `git show REV:tools/mado-action-plan.py | sha256sum`. An
alternative is to hash before and after and fail if they differ, but that still leaves a mid-run
window.

### F2 — Low: non-regular inputs are opened before the type check

Anchor: `flags = O_RDONLY | O_NONBLOCK | O_NOFOLLOW` (:155), `os.open(path, flags)` (:157), then
`fstat` and `S_ISREG`.

- `--plan /dev/input/eventN` opens the evdev node. The user is in the `input` group (`id -nG` shows
  `vgpnk docker input wheel`), so the open succeeds. The gate rejects the file only after the open.
- Opening a tty with no `O_NOCTTY` can make it the controlling terminal of a session leader. On some
  serial devices, open itself has side effects (DTR).
- No events are read, so this is not input capture. It is still a driver open on a path supplied in
  argv. That conflicts with the docstring's "NEVER inspects host state" and the round's no-input-device
  stance. It is not an execution path.

**Smallest correction:**
1. `os.lstat(path)` and require `S_ISREG` before `os.open`.
2. Add `os.O_NOCTTY` to `flags`.
3. Keep the post-open `fstat` and compare `(st_dev, st_ino)` with the `lstat` result, so a swap
   between the two calls is rejected.

No new fixture is needed for F2: the existing `plan-is-directory` case already covers the reject path.

### F3 — Low / honesty: wording and failure-mode gaps around `_self_invoke`

- The docstring says the env is "only what the interpreter needs" (:491–493). The child needs no
  `PATH`: `sys.executable` is absolute. This is harmless. The wording could be "PATH only", or the
  key could be dropped.
- **Empty `sys.executable`.** If it is `""` or `None` (embedded interpreters),
  `subprocess.run([None, …])` raises an uncaught traceback.
- **Timeout.** `TimeoutExpired` at `timeout=60` is also uncaught: traceback, exit 1.
- Both outcomes fail closed, matching the registry's selftest "1 failed". However, the docstring's
  "no traceback" promise covers only `--plan`/`--frozen`. State that, or catch both exceptions in
  `run_selftest` and count them as FAIL.

### F4 — Low: the parent's isolation depends on how it is invoked, and the documented commands disagree

- The SKILL rows (:529–530) use `python3 -I tools/mado-action-plan.py …`.
- `SCORECARD.md:706–707` and `safety-cases.json:6` (`subject`) give the command without `-I`.
- Without `-I`, the parent puts `tools/` first on `sys.path` and honors `PYTHONPATH` and user
  site-packages. A planted `tools/json.py`, `tools/hashlib.py` or `tools/subprocess.py` would then run
  in the parent before any classification.
- This is repository or host state, not supplied argv. It is still a gap in the "never executes"
  narrative.

**Smallest correction:** use `python3 -I` in the SCORECARD command and the cases `subject`.
(SCORECARD and SKILL are owned by L1; `safety-cases.json` by its author.)

Side observation: an untracked `tools/__pycache__/mado-action-plan.cpython-314.pyc` (05:46) exists.
Running a file as `__main__` does not write bytecode, so some seat imported or compiled the module.
The `.pyc` is not ignored (`git status`: `?? tools/__pycache__/`). L1 should not commit it. It has no
bearing on execution.

## Not demanded

- These are not demands for shell parsing, an argv allowlist, operand path analysis or interception.
- The classifier limits stated at `SKILL.md:533–` are declared policy, not defects.
- `--frozen` single-read and hash-the-same-bytes now holds on the final snapshot (:436–451). I note
  it only to show the earlier TOCTOU concern is closed in these bytes.

## Impacted axes

- **operability (C2):** F1 weakens selftest-as-evidence and its provenance binding. F2 is a minor host
  touch.
- **calibration:** F3 and F4 are wording/command mismatches between the docstring, SKILL, SCORECARD and
  cases.
- **coverage (C1):** none.

None of these is a tradeoff the judge must reject. All four are fixable in place. F1 should be fixed
before any selftest receipt is cited as binding the committed gate bytes.

## Tooling

Nothing installed or updated. `pacman` was not touched.
