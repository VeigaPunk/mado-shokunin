# RevTruthF: C1 truth attack on CallbackStoredInDict and CallbackStoredOnAttribute

Seat: `MadoR23.RevTruthF` (reviewer, leaf, no dispatch). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`, HEAD `a28e4815aabfa85f55274884000fb2608355f8cf`. `git diff --stat e33ea304 a28e4815 -- tools/` is empty, so the committed classifier equals the base `e33ea304` (sha256 `cd9da20c…`). Lane writes: this report only. No installs, no pacman, no sudo, no subagents, no candidate patch.

## Verdicts

| Case | kind | argv Python executes (one call each) | Truth | Pass rule |
|---|---|---|---|---|
| CallbackStoredInDict | present | `pacman -S r23-hook-dict` | truth-correct | rule-too-loose (class, extra rows, declared unparsed); not too strict |
| CallbackStoredOnAttribute | present | `pacman -S r23-hook-attr` | truth-correct | rule-too-loose (same three axes); not too strict |

No truth-wrong finding in scope. Both cases already pass at base (the 6/12 includes them), so they guard only against a dropped row. They cannot reward or penalise a change between `lead` and `observed`, or a class change.

## Commands and outputs

Every command ran from `/tmp` or read-only. Nothing was written except this file, plus one bytecode cache that my probe import created in the lane and that I removed again (F6).

1. `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/repair/truth.py` (ran once). Exit 0. `{"passed": 12, "total": 12, "python": "3.14.8", "expected_sha256": "53e34d2691f1a456ce6a4387795c84e5a55d3449b94245d68de516023187c6b9"}`. Executed sets: InDict `["pacman -S r23-hook-dict"]`, OnAttribute `["pacman -S r23-hook-attr"]`; all 12 cases executed exactly one argv. The committed receipt `evidence/repair-truth.json` matches this run row for row.
2. `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/repair/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` (ran once). Exit 1, `passed: 6, total: 12`, `tool_sha256 cd9da20c…`, `helper_sha256 4eb893d2…`. Both target cases: `passed: true, unparsed: 0, exit: 1, error: null, rows: [[host_mutation, <command>, lead]]`. I compared this against `evidence/repair-before-e33ea304.json` field by field for both cases; they are identical. The other ten rows and the 6/12 pass set also reproduce.
3. Hashes: `CallbackStoredInDict.jsonl` `6602eedf…`, `CallbackStoredOnAttribute.jsonl` `c403bb3c…`, `expected.json` `53e34d26…`, all equal to the pins. `wc -l fixtures/*.jsonl`: each of the 12 fixtures is exactly one line, so `code_of()` reads the whole record.
4. Base identity: `sha256sum tools/mado-tripwire.py` gives `cd9da20c…`. `git -C <lane> show a28e4815:tools/mado-tripwire.py | sha256sum` gives `cd9da20c…`.
5. Pass-rule probe (eval kernel, Python): I loaded `repair/measure.py` with importlib (only its top-level definitions run; `main()` does not) and called `measure.judge(case, got)` on synthetic `got` dicts. No fixture code and no classifier process ran. The importlib load wrote `repair/__pycache__/measure.cpython-314.pyc`; I deleted that file and its directory, and `ls -la` confirms the `repair/` directory holds only the frozen files. Results in the table below.
6. Reads: expected.json (raw), truth.py, measure.py, the round-21 scan helper, all 12 fixture code bodies, the base evidence, the committed truth receipt, and the registration. Regex searches: `S121` and callback or hook identifiers across round-21/round-22 expected files and `tools/`.

## Pass-rule probe (synthetic classifier output through `measure.judge`)

| Synthetic output for the case | InDict | OnAttr | Reading |
|---|---|---|---|
| A. `host_mutation` + `lead` (base shape) | pass | pass | correct |
| B. `host_mutation` + `observed` | pass | pass | correct |
| C. `package_query` + `lead` (class flipped) | pass | pass | **too loose** |
| D. `vcs_write` + `observed` (class flipped) | pass | pass | **too loose** |
| E. base row + phantom `host_mutation` `observed` row | pass | pass | **too loose** (`forbid_any` is `[]`) |
| F. only a typo'd command | fail | fail | correct |
| G. no rows | fail | fail | correct |
| H. base row + `eval_unparsed: 1` | pass | pass | **too loose** (present branch ignores unparsed) |
| I. evidence `dead` | fail | fail | correct |
| J. exit 2 with the row | fail | fail | correct |

No correct output is rejected by the present rule. Only absent rows, evidence outside observed or lead, exit codes other than 0 or 1, and errors fail. So the rule is not too strict.

Reproduce one row (set `sys.dont_write_bytecode` first, so that the load leaves no cache in the lane):

```python
import sys, importlib.util, json
from pathlib import Path
sys.dont_write_bytecode = True
R = Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/repair")
spec = importlib.util.spec_from_file_location("probe", R / "measure.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)  # top-level definitions only; main() is not run
cases = {c["id"]: c for c in json.loads((R / "expected.json").read_bytes())["cases"]}
got = {"exit": 1, "error": None, "payload": {"findings": [{"class": "package_query", "command": "pacman -S r23-hook-dict", "evidence": "lead"}], "files": []}}
print(m.judge(cases["CallbackStoredInDict"], got)[0])  # True: a class flip passes the present rule
```

## Per-case analysis

### CallbackStoredInDict (kind `present`; `want_present` `pacman -S r23-hook-dict`; `forbid_any` `[]`)

Fixture code:

```python
import subprocess
hooks = {}
def run():
    subprocess.run(["pacman", "-S", "r23-hook-dict"])
def register(callback):
    hooks["k"] = callback
register(run)
hooks["k"]()
```

Python semantics. `run` is a module-level def. Its free name `subprocess` is not bound in any enclosing function scope, so it is a global, looked up when `run` is called (the late-global rule that S121 and the LateGlobalRebinding case cite). That lookup reaches the module binding made by `import subprocess`, which is the fake inside truth.py's child. `register` only performs a subscript store, so `hooks` is a global too. `register(run)` stores the function object `run` in the dict, and the module-level `hooks["k"]()` calls it exactly once. Executed argv: `["pacman","-S","r23-hook-dict"]`. Lexical and late resolution agree here, because there is no rebinding and no closure cell.

Check: `want_present` is a subset of the executed set, and the executed set has no other command. truth.py and the receipt agree. The truth is tight: executed set equals the wanted set.

Base: the scanner emits `host_mutation`, `pacman -S r23-hook-dict`, `lead`, exit 1. The exit 1 means the gate fires, because `verdict_of` counts leads as unpermitted. The `lead` label is the documented behaviour for a def handed on as a value, such as a callback (`tools/mado-tripwire.py` module docstring, lines 48-49). It also follows round-21 policy: "Mere stored targets without start remain distinct conservative leads" (`.ufo/waves/round-21/oracle/expected.json:49`).

Verdict: **truth-correct**. Pass rule: **too loose**.
- Class is not checked. The present branch (`measure.py:47-48`) tests only command and evidence in {observed, lead}. Probes C and D pass.
- `forbid_any` is empty, so phantom rows pass (probe E).
- The present branch ignores `unparsed` (`measure.py:48`, while `:38` computes it). Probe H passes.

### CallbackStoredOnAttribute (kind `present`; `want_present` `pacman -S r23-hook-attr`; `forbid_any` `[]`)

Fixture code:

```python
import subprocess
class Box:
    pass
box = Box()
def run():
    subprocess.run(["pacman", "-S", "r23-hook-attr"])
def register(callback):
    box.cb = callback
register(run)
box.cb()
```

Python semantics. `register` performs an attribute store on `box`, not a name bind, so `box` is a global read and there is no UnboundLocalError. The instance attribute `cb` holds the plain function `run`. `box.cb()` is an instance-attribute call, so no `self` is bound and `run()` takes no arguments. It calls the fake exactly once with `["pacman","-S","r23-hook-attr"]`. The S121 reasoning is the same as above.

Check and base: truth-correct, with the same tightness. Base emits `host_mutation`, `pacman -S r23-hook-attr`, `lead`, exit 1, for the same documented reason.

Verdict: **truth-correct**. Pass rule: **too loose** on the same three axes (probes C, D, E and H).

## Findings (by severity)

**F1 (medium, rule; operability of the guard).** The present kind is recall-only. It accepts a wrong class. A `pacman -S` row labelled `package_query` passes, and `verdict_of` would then permit it under `--permit package_query`, giving exit 0 and label `permitted_only`. It also accepts phantom extra rows and declared unparsed evals. The frozen rule cannot change in this round (the expected file is sha-pinned, and the set was "authored before any patch"). Suggested follow-up, as an append-only case or a new suite: a kind that requires class `host_mutation`, the command, and evidence in {observed, lead}, plus an exact extra-row check and `unparsed == 0`.

**F2 (medium, contract).** `truth.py:68-69` runs each fixture child with `timeout=15` but sets no `RLIMIT_AS`. The contract names 384 MiB and 15 s for fixture runs. The round-21 helper applies the memory cap (`round-21/oracle/measure.py:31`, `preexec_fn=cap`), but truth.py does not. So my truth.py run was not under the memory cap. The 12 frozen fixtures are benign, so there is no current effect. A memory-heavy fixture would be unbounded, because the AST gate does not reject operators such as string multiplication. [INFERENCE from the code; not executed.]

**F3 (low to medium, latent safety).** `truth.py:45 safe()` is a denylist of names and of attributes on `subprocess`. It rejects imports other than `subprocess` and names such as `eval`, `exec`, `open`, `__import__`, `compile`, `getattr`, `globals` and `os`. It does not reject dunder-attribute chains such as `().__class__.__base__.__subclasses__()`. [INFERENCE from CPython introspection; not executed.] Such a chain could reach host-level calls that the fake does not record, so truth.py is not a sandbox, and its docstring ("calls anything outside the allowed shape") overstates what the gate checks. I read all 12 code bodies: none uses `__`, imports anything besides `subprocess`, or uses a gated name. So the 12/12 run recorded every call that happened.

**F4 (info, coverage).** Both cases pass at base. They guard only row deletion. In the round-21 and round-22 expected files and in `tools/` (regex hits reviewed), the pinned callback cases are Thread-start callbacks (observed) and closures. I found no pinned expectation for a callback stored and then invoked directly, so a class regression on that form is caught by no frozen case. I did not enumerate every selftest suite.

**F5 (info, provenance).** `fixtures/ReturnedGlobalHelper.jsonl` is a byte-exact round-22 copy. Its internal record id is `NHBFactoryReturnsGlobalHelperParamShadow-0`, which differs from the case id. truth.py reads only the code, so there is no effect.

**F6 (low, hygiene).** The round-21 helper's child (`round-21/oracle/measure.py:31`, `python3 -I -c WRAPPER`) loads each tool through a spec loader, so a stale `tools/__pycache__` entry is rewritten inside the lane on a counter run. `-I` does not suppress bytecode writes; `-B` does. `tools/__pycache__/mado-tripwire.cpython-314.pyc` is 18 h old and my run did not rewrite it, so the counter did not write into the lane. The one write was my probe import, now removed. Suggest `-B` in the helper's child argv. Not changed here, because the helper is a sealed round-21 file.

**Related note, outside my two cases.** Three base exact failures have the correct row but `unparsed=1`: ForwardExistingClosureWithoutFrameContamination, ForwarderPassesCallerArgument and ForwarderInvokesFactoryClosure. Python executes exactly the wanted argv for each. So the exact rule demands only scanner self-accounting here (`unparsed == 0`), not any Python behaviour the fake does not show. That is a legitimate repair target for the scanner.

## Residual risk and verification gaps

- Each harness ran once, as instructed. Base results come from a single `measure.py` run.
- The Python semantics for the two cases come from reading the code. The only execution of fixture code was truth.py's recording run.
- I assumed single-namespace cell execution, as truth.py and the classifier's binding model do. I did not verify the production eval kernel's namespace model. If cells ran with split locals, `run` would raise NameError, no argv would execute, and the present expectation would not hold. [INFERENCE]
- F1 and F3 do not block the 12/12 claim. They limit what 12/12 proves.
- No candidate patch was in my scope, so I did not audit one.

## Installs and updates

None. I read `~/.omp/agent/RULES.md`. I installed or updated nothing, and ran no pacman, sudo, or host change.

## Verdict

- CallbackStoredInDict: **truth-correct**; pass rule **too loose** (class, extra rows, declared unparsed); not too strict.
- CallbackStoredOnAttribute: **truth-correct**; pass rule **too loose** (same); not too strict.
- Base C1 result reproduced exactly: 6/12, with both target cases passing via `lead`. No truth-wrong finding.
