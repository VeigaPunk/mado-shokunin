# MutMergedTripwire — partial

## Attack and result

Attacked the merged `mado-tripwire.py` at commit `01b80946d92b26370d3012a7da655d00dd135154` with **20 independent single-point mutants**. Every mutant ran all **11 assigned suites / 247 cases** on its own pristine, mutated, and exactly restored copy. **15 killed, 5 survived, 0 inconclusive** against the assigned suites (75% of these selected mutants killed). The five survivors are non-equivalent: five additional, synthetic regression proposals each pass on pristine/restored bytes and fail against their respective mutant. No lane implementation or existing test was changed.

This is a coverage finding, not a change to the contract and not a ship/judge decision. In particular, it does not refute the separately claimed six-incident 6/6 recall fraction; it shows why passing the enumerated suites does not protect every new supported behavior.

**Axes:** (1) command-class recall and false-positive control; (2) explicit-permit and frozen fail-closed semantics; (3) sensitivity to plausible one-point regressions; (4) exact-byte restoration and host-safe evidence. Work was bounded to four concurrent selftest subprocesses, with no dispatch or alternate agent runtime.

## Pinned material and detector

- Committed source: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`, read with the command below; 90,536 bytes.
- Scratch: `/tmp/mado-r19-MutMergedTripwire.uMlaZe`.
- Pristine/restored SHA-256 for **every** active mutant copy: `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`.
- The worktree source matched those committed bytes before the attack and has the same SHA-256 afterward.
- All 11 suite `expected.json` files matched the assigned commit. A manifest of 294 fixture files/symlink targets was unchanged before/after the run.
- Interpreter: `/usr/bin/python`, Python 3.14.8. Detector: the tripwire's own `--selftest` interface. The selftest launches only this Python classifier; recorded host/tool commands remain transcript data and were never executed.

Actual source-extraction command:

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 01b80946d92b26370d3012a7da655d00dd135154:tools/mado-tripwire.py
```

Actual phase commands (each harness invocation expands into every mutant × every suite; exact child argv and stdout/stderr paths are retained in the phase results):

```sh
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/run_phase.py baseline
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/run_phase.py mutated
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/run_phase.py restored
```

The phase harness asserts the expected source digest before each suite and that it has not changed afterward. Each suite has a 300-second bound; internal selftest child calls retain their 120-second bound. No timeout or suite error occurred.

### Every assigned suite

Each row ran once per mutant in **each of the three phases** (20 × 3 = 60 runs per row). The table paths are the actual `--selftest` arguments.

| Suite absolute path | Cases |
| --- | ---: |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core` | 9 |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound` | 16 |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening` | 33 |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/w2-regressions` | 30 |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen` | 31 |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/r18-failsafe` | 1 |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-bashcvar` | 45 |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-helperfn` | 34 |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-installers` | 18 |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-vcs` | 17 |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-frozen-f1f2` | 13 |

### Actual aggregate outputs

```text
{"case_failures": 0, "case_passes": 4940, "phase": "baseline", "results": "/tmp/mado-r19-MutMergedTripwire.uMlaZe/baseline/results.json", "suite_errors": 0, "suite_failures": 0, "suite_passes": 220, "suite_runs": 220}
{"case_failures": 39, "case_passes": 4901, "phase": "mutated", "results": "/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/results.json", "suite_errors": 0, "suite_failures": 15, "suite_passes": 205, "suite_runs": 220}
{"case_failures": 0, "case_passes": 4940, "phase": "restored", "results": "/tmp/mado-r19-MutMergedTripwire.uMlaZe/restored/results.json", "suite_errors": 0, "suite_failures": 0, "suite_passes": 220, "suite_runs": 220}
```

**660 suite invocations; 14,820 case executions.** Baseline: 4,940/4,940 passed. Mutated: 4,901/4,940 passed (39 failing cases across 15 suites). Restored: 4,940/4,940 passed. All 20 pristine and restored copies individually passed 247/247 cases.

## Mutant ledger

Each change is isolated to one behavior-bearing source line in one `/tmp` copy. All source locations below refer to the assigned committed implementation. `Cases` is the actual total across the 11 suites on mutated bytes; other suites passed. A survivor still has verdict **survived** against the original detector even though its proposed additional detector kills it.

| ID | Source evidence | Single-point defect | Mutated cases | Original detector verdict |
| --- | --- | --- | ---: | --- |
| M01 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1112` | `literal-concat-drops-right` | 246/247 | **killed** |
| M02 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1119` | `literal-replace-is-identity` | 246/247 | **killed** |
| M03 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1121` | `tuple-literal-not-folded` | 246/247 | **killed** |
| M04 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1358` | `opaque-statement-keeps-env` | 243/247 | **killed** |
| M05 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:727` | `shell-positional-always-first` | 247/247 | **survived** |
| M06 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1287` | `python-keyword-bind-lost` | 247/247 | **survived** |
| M07 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1294` | `python-default-index-always-zero` | 247/247 | **survived** |
| M08 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1386` | `helper-lead-only-first-arg` | 245/247 | **killed** |
| M09 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1253` | `print-no-longer-pure` | 245/247 | **killed** |
| M10 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:803` | `uv-tool-upgrade-omitted` | 243/247 | **killed** |
| M11 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:829` | `npm-add-alias-omitted` | 247/247 | **survived** |
| M12 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:842` | `cargo-list-becomes-install` | 242/247 | **killed** |
| M13 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:809` | `uvx-without-operand-classifies` | 242/247 | **killed** |
| M14 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1619` | `tool-install-implicitly-permitted` | 239/247 | **killed** |
| M15 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:527` | `git-stash-show-writes` | 246/247 | **killed** |
| M16 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:129` | `jj-absorb-write-omitted` | 247/247 | **survived** |
| M17 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:499` | `jj-ignore-after-dashdash-counts` | 246/247 | **killed** |
| M18 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1883` | `f1-whitespace-is-nonblank` | 245/247 | **killed** |
| M19 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1906` | `f2-normalizes-prefix-first` | 246/247 | **killed** |
| M20 | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1910` | `f2-forbids-ancestor-symlinks` | 246/247 | **killed** |

### Exact mutations, expected detectors, and observed suite output

**M01 — literal-concat-drops-right**

- Expected detector: round-19/r19-bashcvar: concat/name recipes must preserve both literal operands.
- Exact old/new text:

```python
            return left + right
# becomes
            return left
```

- Actual failing detector: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-bashcvar`, exit 1.

```text
SELFTEST_SUMMARY: 44/45 passed failed=['plus-concat']
CASE plus-concat FAIL want=(1, [('package_query', 'pacman:-Q', 1, 'plus-concat.jsonl')]) got=(0, [])
```

- Full stdout: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M01/round-19__r19-bashcvar.stdout`.

**M02 — literal-replace-is-identity**

- Expected detector: round-19/r19-bashcvar: literal replace recipes must resolve the replacement.
- Exact old/new text:

```python
            return base.replace(old, new)
# becomes
            return base
```

- Actual failing detector: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-bashcvar`, exit 1.

```text
SELFTEST_SUMMARY: 44/45 passed failed=['replace-removes-command-clean']
CASE replace-removes-command-clean FAIL want=(0, []) got=(1, [('package_query', 'pacman:-Q', 1, '')])
```

- Full stdout: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M02/round-19__r19-bashcvar.stdout`.

**M03 — tuple-literal-not-folded**

- Expected detector: round-19/r19-bashcvar: tuple argv variables must classify.
- Exact old/new text:

```python
    if isinstance(node, (ast.List, ast.Tuple)):
# becomes
    if isinstance(node, ast.List):
```

- Actual failing detector: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-bashcvar`, exit 1.

```text
SELFTEST_SUMMARY: 44/45 passed failed=['r19-tuple-var']
CASE r19-tuple-var FAIL want=(1, [('package_query', 'pacman:-Q', 1, 'tuple-var.jsonl')]) got=(0, [])
```

- Full stdout: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M03/round-19__r19-bashcvar.stdout`.

**M04 — opaque-statement-keeps-env**

- Expected detector: round-19/r19-bashcvar: exec/globals/import-star invalidates carried recipes.
- Exact old/new text:

```python
        if opaque_statement(stmt):
# becomes
        if False and opaque_statement(stmt):
```

- Actual failing detector: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-bashcvar`, exit 1.

```text
SELFTEST_SUMMARY: 41/45 passed failed=['exec-clears-carry-clean', 'r19-import-star-clears-clean', 'r19-import-star-same-cell-clears-clean', 'r19-exec-same-cell-clears-clean']
CASE exec-clears-carry-clean FAIL want=(0, []) got=(1, [('package_query', 'pacman:-Q', 3, '')])
```

- Full stdout: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M04/round-19__r19-bashcvar.stdout`.

**M05 — shell-positional-always-first**

- Expected detector: round-19/r19-helperfn: $2 and later positions must use the supplied argument.
- Exact old/new text:

```python
                    val = args[int(key) - 1]
# becomes
                    val = args[0]
```

- Actual output: every suite exited 0, 247/247 cases passed; all eleven `SELFTEST_SUMMARY` records and per-case lines are retained under `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M05`. The additional distinguishing case is below.

**M06 — python-keyword-bind-lost**

- Expected detector: round-19/r19-helperfn: literal keyword argument substitution must resolve.
- Exact old/new text:

```python
        bound[k.arg] = value
# becomes
        bound[k.arg] = LITERAL_MISS
```

- Actual output: every suite exited 0, 247/247 cases passed; all eleven `SELFTEST_SUMMARY` records and per-case lines are retained under `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M06`. The additional distinguishing case is below.

**M07 — python-default-index-always-zero**

- Expected detector: helper rule A: multiple literal defaults must retain their corresponding values.
- Exact old/new text:

```python
        value = literal_value(fn.args.defaults[idx - first_default], {})
# becomes
        value = literal_value(fn.args.defaults[0], {})
```

- Actual output: every suite exited 0, 247/247 cases passed; all eleven `SELFTEST_SUMMARY` records and per-case lines are retained under `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M07`. The additional distinguishing case is below.

**M08 — helper-lead-only-first-arg**

- Expected detector: helper rule B: a host argv list in any positional argument contributes a lead.
- Exact old/new text:

```python
    for a in node.args:
        vals = argv_strings(literal_value(a, env))
# becomes
    for a in node.args[:1]:
        vals = argv_strings(literal_value(a, env))
```

- Actual failing detector: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-helperfn`, exit 1.

```text
SELFTEST_SUMMARY: 32/34 passed failed=['py-lead-cross-cell-literal', 'py-lead-two-calls']
CASE py-lead-cross-cell-literal FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(0, [])
```

- Full stdout: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M08/round-19__r19-helperfn.stdout`.

**M09 — print-no-longer-pure**

- Expected detector: round-19/r19-helperfn: pure print calls must not become argv leads.
- Exact old/new text:

```python
    "print", "list", "tuple", "set", "dict", "sorted", "reversed", "repr", "str",
# becomes
    "list", "tuple", "set", "dict", "sorted", "reversed", "repr", "str",
```

- Actual failing detector: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-helperfn`, exit 1.

```text
SELFTEST_SUMMARY: 32/34 passed failed=['py-helper-nonspawn-body', 'py-lead-pure-print']
CASE py-helper-nonspawn-body FAIL want=(0, []) got=(1, [('package_query', 'pacman:-Q', 1, '')])
```

- Full stdout: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M09/round-19__r19-helperfn.stdout`.

**M10 — uv-tool-upgrade-omitted**

- Expected detector: round-19/r19-installers: uv tool upgrade must be tool_install.
- Exact old/new text:

```python
                "install", "upgrade", "uninstall", "run"):
# becomes
                "install", "uninstall", "run"):
```

- Actual failing detector: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-installers`, exit 1.

```text
SELFTEST_SUMMARY: 14/18 passed failed=['uv-tool-install-upgrade-uninstall', 'uv-tool-install-permitted', 'installers-only-permit', 'whole-directory-permitted']
CASE uv-tool-install-upgrade-uninstall FAIL want=(1, [('tool_install', 'uv:tool-install', 2, 'uv-tool.jsonl'), ('tool_install', 'uv:tool-uninstall', 4, 'uv-tool.jsonl'), ('tool_install', 'uv:tool-upgrade', 3, 'uv-tool.jsonl')]) got=(1, [('tool_install', 'uv:tool-install', 2, 'uv-tool.jsonl'), ('tool_install', 'uv:tool-uninstall', 4, 'uv-tool.jsonl')])
```

- Full stdout: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M10/round-19__r19-installers.stdout`.

**M11 — npm-add-alias-omitted**

- Expected detector: tool_install: npm add -g is an explicitly supported global install alias.
- Exact old/new text:

```python
        if verb in ("install", "i", "add"):
# becomes
        if verb in ("install", "i"):
```

- Actual output: every suite exited 0, 247/247 cases passed; all eleven `SELFTEST_SUMMARY` records and per-case lines are retained under `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M11`. The additional distinguishing case is below.

**M12 — cargo-list-becomes-install**

- Expected detector: round-19/r19-installers: cargo install --list is a query, not an install.
- Exact old/new text:

```python
        if verb == "install" and "--list" not in rest:
# becomes
        if verb == "install":
```

- Actual failing detector: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-installers`, exit 1.

```text
SELFTEST_SUMMARY: 13/18 passed failed=['cargo-install-uninstall', 'negative-controls-stay-clean', 'negative-controls-clean-under-permit', 'installers-only-permit', 'whole-directory-permitted']
CASE cargo-install-uninstall FAIL want=(1, [('tool_install', 'cargo:install', 2, 'cargo-channel.jsonl'), ('tool_install', 'cargo:install', 3, 'cargo-channel.jsonl'), ('tool_install', 'cargo:install', 7, 'cargo-channel.jsonl'), ('tool_install', 'cargo:install', 8, 'cargo-channel.jsonl'), ('tool_install', 'cargo:uninstall', 5, 'cargo-channel.jsonl')]) got=(1, [('tool_install', 'cargo:install', 2, 'cargo-channel.jsonl'), ('tool_install', 'cargo:install', 3, 'cargo-channel.jsonl'), ('tool_install', 'cargo:install', 4, 'cargo-channel.jsonl'), ('tool_install', 'cargo:install', 7, 'cargo-channel.jsonl'), ('tool_install', 'cargo:install', 8, 'cargo-channel.jsonl'), ('tool_install', 'cargo:uninstall', 5, 'cargo-channel.jsonl')])
```

- Full stdout: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M12/round-19__r19-installers.stdout`.

**M13 — uvx-without-operand-classifies**

- Expected detector: round-19/r19-installers: uvx help/version without a package remains clean.
- Exact old/new text:

```python
        return ("tool_install", "uvx") if has_operand(args, NPX_ARG_OPTS) else None
# becomes
        return ("tool_install", "uvx")
```

- Actual failing detector: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-installers`, exit 1.

```text
SELFTEST_SUMMARY: 13/18 passed failed=['uv-pip-uvx-and-tool-run', 'negative-controls-stay-clean', 'negative-controls-clean-under-permit', 'installers-only-permit', 'whole-directory-permitted']
CASE uv-pip-uvx-and-tool-run FAIL want=(1, [('tool_install', 'uv:pip-install', 2, 'uv-pip-and-uvx.jsonl'), ('tool_install', 'uv:tool-run', 7, 'uv-pip-and-uvx.jsonl'), ('tool_install', 'uvx', 3, 'uv-pip-and-uvx.jsonl')]) got=(1, [('tool_install', 'uv:pip-install', 2, 'uv-pip-and-uvx.jsonl'), ('tool_install', 'uv:tool-run', 7, 'uv-pip-and-uvx.jsonl'), ('tool_install', 'uvx', 3, 'uv-pip-and-uvx.jsonl'), ('tool_install', 'uvx', 4, 'uv-pip-and-uvx.jsonl')])
```

- Full stdout: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M13/round-19__r19-installers.stdout`.

**M14 — tool-install-implicitly-permitted**

- Expected detector: round-19/r19-installers: tool_install requires an explicit permit.
- Exact old/new text:

```python
    unpermitted = sum(1 for f in findings if f["class"] not in permit)
# becomes
    unpermitted = sum(1 for f in findings if f["class"] not in permit and f["class"] != "tool_install")
```

- Actual failing detector: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-installers`, exit 1.

```text
SELFTEST_SUMMARY: 10/18 passed failed=['uv-tool-install-upgrade-uninstall', 'uv-pip-uvx-and-tool-run', 'pip-pipx-python-m', 'npm-global-and-exec', 'cargo-install-uninstall', 'channel-forms-detected', 'host-mutation-permit-leaves-install-unpermitted', 'compound-wrappers-shell-c']
CASE uv-tool-install-upgrade-uninstall FAIL want=(1, [('tool_install', 'uv:tool-install', 2, 'uv-tool.jsonl'), ('tool_install', 'uv:tool-uninstall', 4, 'uv-tool.jsonl'), ('tool_install', 'uv:tool-upgrade', 3, 'uv-tool.jsonl')]) got=(0, [('tool_install', 'uv:tool-install', 2, 'uv-tool.jsonl'), ('tool_install', 'uv:tool-uninstall', 4, 'uv-tool.jsonl'), ('tool_install', 'uv:tool-upgrade', 3, 'uv-tool.jsonl')])
```

- Full stdout: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M14/round-19__r19-installers.stdout`.

**M15 — git-stash-show-writes**

- Expected detector: round-19/r19-vcs: git stash show is read-only.
- Exact old/new text:

```python
    if verb == "stash" and sub_verb(args, verb) in ("list", "show"):
# becomes
    if verb == "stash" and sub_verb(args, verb) == "list":
```

- Actual failing detector: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-vcs`, exit 1.

```text
SELFTEST_SUMMARY: 16/17 passed failed=['git-reads-clean']
CASE git-reads-clean FAIL want=(0, []) got=(1, [('vcs_write', 'git:stash', 13, '')])
```

- Full stdout: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M15/round-19__r19-vcs.stdout`.

**M16 — jj-absorb-write-omitted**

- Expected detector: vcs_write: jj absorb remains a write even with --ignore-working-copy.
- Exact old/new text:

```python
            "edit", "restore", "split", "duplicate", "absorb"}
# becomes
            "edit", "restore", "split", "duplicate"}
```

- Actual output: every suite exited 0, 247/247 cases passed; all eleven `SELFTEST_SUMMARY` records and per-case lines are retained under `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M16`. The additional distinguishing case is below.

**M17 — jj-ignore-after-dashdash-counts**

- Expected detector: round-19/r19-vcs: a path after -- cannot disable working-copy snapshot classification.
- Exact old/new text:

```python
    head = args[:args.index("--")] if "--" in args else args
# becomes
    head = args
```

- Actual failing detector: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-vcs`, exit 1.

```text
SELFTEST_SUMMARY: 16/17 passed failed=['jj-dashdash-paths']
CASE jj-dashdash-paths FAIL want=(1, [('vcs_write', 'jj:diff', 2, '')]) got=(0, [])
```

- Full stdout: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M17/round-19__r19-vcs.stdout`.

**M18 — f1-whitespace-is-nonblank**

- Expected detector: round-19/r19-frozen-f1f2: whitespace-only pinned lines are unreachable/frozen_error.
- Exact old/new text:

```python
            stats[os.path.normpath(e["path"])] = [bool(r.strip()) for r in raw]
# becomes
            stats[os.path.normpath(e["path"])] = [bool(r) for r in raw]
```

- Actual failing detector: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-frozen-f1f2`, exit 1.

```text
SELFTEST_SUMMARY: 11/13 passed failed=['f1-whitespace-expected', 'f1-blank-after-valid']
CASE f1-whitespace-expected FAIL want=(2, 'MADO_TRIPWIRE_FROZEN: frozen_error', 0, 0) got=(1, 'MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch', ('frozen_verdict_mismatch', 1, 1, 0))
```

- Full stdout: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M18/round-19__r19-frozen-f1f2.stdout`.

**M19 — f2-normalizes-prefix-first**

- Expected detector: round-19/r19-frozen-f1f2: link/../evil must be resolved by kernel prefix semantics.
- Exact old/new text:

```python
    for part in path.split(os.sep):
# becomes
    for part in os.path.normpath(path).split(os.sep):
```

- Actual failing detector: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-frozen-f1f2`, exit 1.

```text
SELFTEST_SUMMARY: 12/13 passed failed=['f2-symlink-dotdot-launder']
CASE f2-symlink-dotdot-launder FAIL want=(2, 'MADO_TRIPWIRE_FROZEN: snapshot_tampered', 0, 0) got=(0, 'MADO_TRIPWIRE_FROZEN: frozen_match', ('frozen_match', 0, 0, 0))
```

- Full stdout: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M19/round-19__r19-frozen-f1f2.stdout`.

**M20 — f2-forbids-ancestor-symlinks**

- Expected detector: round-19/r19-frozen-f1f2: an unrelated ancestor symlink is allowed.
- Exact old/new text:

```python
        if os.path.islink(prefix) and os.path.realpath(prefix) == real_dir:
# becomes
        if os.path.islink(prefix):
```

- Actual failing detector: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-frozen-f1f2`, exit 1.

```text
SELFTEST_SUMMARY: 12/13 passed failed=['f2-ancestor-symlink-match']
CASE f2-ancestor-symlink-match FAIL want=(0, 'MADO_TRIPWIRE_FROZEN: frozen_match', 0, 0) got=(2, 'MADO_TRIPWIRE_FROZEN: snapshot_tampered', ('snapshot_tampered', 2, 0, 0))
```

- Full stdout: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/M20/round-19__r19-frozen-f1f2.stdout`.

## Five survivor regression-case proposals

These are **proposals only**, not integrated tests. Each lives under the absolute directory stated below and consists of one synthetic OMP-shaped JSONL record plus a `mado-tripwire-selftest-v1` `expected.json`. Every expected finding is at JSONL line 1, with `want_exit: 1` and `want_label: findings`. The fixture snippets below are tool argument values, **not commands executed on the host**.

The bounded additional detector was run unchanged on pristine, mutated and restored bytes. For all five, selftest exits were **0 → 1 → 0**. The direct `--scan` command was also captured in every phase.

### M05 — shell-second-third-positional

The named existing positional fixture uses only `$1`: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-helperfn/sh-fn-positional-n.jsonl:1`. Replacing every positional lookup with the first argument therefore survived. Exercise `$2`/`$3` as well. The proposal distinguishes the exact class/rule even though both baseline and mutant exit 1.

- Proposal directory: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M05`.
- Expected finding: `package_query / pacman:-Q / line 1`.
- Tool argument (`bash`):

```text
query() { "$1" "$2" "$3"; }
query pacman -Q wayland
```

Actual additional selftest commands:

```sh
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/pristine.py --selftest /tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M05
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/M05/mado-tripwire.py --selftest /tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M05
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/M05/mado-tripwire.py --selftest /tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M05
```

Actual detector outputs:

```text
baseline: selftest_exit=0; scan_exit=1; MADO_TRIPWIRE: findings; findings=[('package_query', 'pacman:-Q', 1)]
CASE shell-second-third-positional ok
SELFTEST_SUMMARY: 1/1 passed failed=[]
mutated: selftest_exit=1; scan_exit=1; MADO_TRIPWIRE: findings; findings=[('host_mutation', 'pacman', 1)]
CASE shell-second-third-positional FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(1, [('host_mutation', 'pacman', 1, '')])
SELFTEST_SUMMARY: 0/1 passed failed=['shell-second-third-positional']
restored: selftest_exit=0; scan_exit=1; MADO_TRIPWIRE: findings; findings=[('package_query', 'pacman:-Q', 1)]
CASE shell-second-third-positional ok
SELFTEST_SUMMARY: 1/1 passed failed=[]
```

Raw complete scan JSON, stderr, selftest output and exact argv: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/proposal-results.json`.

### M06 — python-command-keyword

The existing keyword fixture passes the command argv positionally and only `timeout=5` by keyword: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-helperfn/py-helper-keyword.jsonl:1`. Losing a literal keyword binding does not change its command finding. Pass the command itself by keyword.

- Proposal directory: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M06`.
- Expected finding: `package_query / pacman:-Q / line 1`.
- Tool argument (`eval`):

```python
import subprocess
def run(cmd):
    return subprocess.run(cmd)
run(cmd=['pacman', '-Q', 'wayland'])

```

Actual additional selftest commands:

```sh
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/pristine.py --selftest /tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M06
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/M06/mado-tripwire.py --selftest /tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M06
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/M06/mado-tripwire.py --selftest /tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M06
```

Actual detector outputs:

```text
baseline: selftest_exit=0; scan_exit=1; MADO_TRIPWIRE: findings; findings=[('package_query', 'pacman:-Q', 1)]
CASE python-command-keyword ok
SELFTEST_SUMMARY: 1/1 passed failed=[]
mutated: selftest_exit=1; scan_exit=0; MADO_TRIPWIRE: clean; findings=[]
CASE python-command-keyword FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(0, [])
SELFTEST_SUMMARY: 0/1 passed failed=['python-command-keyword']
restored: selftest_exit=0; scan_exit=1; MADO_TRIPWIRE: findings; findings=[('package_query', 'pacman:-Q', 1)]
CASE python-command-keyword ok
SELFTEST_SUMMARY: 1/1 passed failed=[]
```

Raw complete scan JSON, stderr, selftest output and exact argv: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/proposal-results.json`.

### M07 — python-multiple-literal-defaults

Literal defaults are explicitly folded in `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1266` and indexed at line 1294. The named default fixture exercises only a nonliteral default: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-helperfn/py-helper-default-nonliteral.jsonl:1`. Add two distinct literal defaults to protect correspondence. This is implemented default-binding behavior, not a claim of arbitrary Python execution.

- Proposal directory: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M07`.
- Expected finding: `package_query / pacman:-Q / line 1`.
- Tool argument (`eval`):

```python
import subprocess
def run(prog='pacman', op='-Q'):
    return subprocess.run([prog, op])
run()

```

Actual additional selftest commands:

```sh
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/pristine.py --selftest /tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M07
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/M07/mado-tripwire.py --selftest /tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M07
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/M07/mado-tripwire.py --selftest /tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M07
```

Actual detector outputs:

```text
baseline: selftest_exit=0; scan_exit=1; MADO_TRIPWIRE: findings; findings=[('package_query', 'pacman:-Q', 1)]
CASE python-multiple-literal-defaults ok
SELFTEST_SUMMARY: 1/1 passed failed=[]
mutated: selftest_exit=1; scan_exit=1; MADO_TRIPWIRE: findings; findings=[('host_mutation', 'pacman', 1)]
CASE python-multiple-literal-defaults FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(1, [('host_mutation', 'pacman', 1, '')])
SELFTEST_SUMMARY: 0/1 passed failed=['python-multiple-literal-defaults']
restored: selftest_exit=0; scan_exit=1; MADO_TRIPWIRE: findings; findings=[('package_query', 'pacman:-Q', 1)]
CASE python-multiple-literal-defaults ok
SELFTEST_SUMMARY: 1/1 passed failed=[]
```

Raw complete scan JSON, stderr, selftest output and exact argv: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/proposal-results.json`.

### M11 — npm-add-global-alias

The implementation explicitly supports `add` at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:829`. Existing npm-family positive cases include `install`/`i` but not `add`: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-installers/npm-family.jsonl:2-14`. Add a global `add` alias case.

- Proposal directory: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M11`.
- Expected finding: `tool_install / npm:install-global / line 1`.
- Tool argument (`bash`):

```text
npm add -g typescript
```

Actual additional selftest commands:

```sh
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/pristine.py --selftest /tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M11
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/M11/mado-tripwire.py --selftest /tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M11
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/M11/mado-tripwire.py --selftest /tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M11
```

Actual detector outputs:

```text
baseline: selftest_exit=0; scan_exit=1; MADO_TRIPWIRE: findings; findings=[('tool_install', 'npm:install-global', 1)]
CASE npm-add-global-alias ok
SELFTEST_SUMMARY: 1/1 passed failed=[]
mutated: selftest_exit=1; scan_exit=0; MADO_TRIPWIRE: clean; findings=[]
CASE npm-add-global-alias FAIL want=(1, [('tool_install', 'npm:install-global', 1, '')]) got=(0, [])
SELFTEST_SUMMARY: 0/1 passed failed=['npm-add-global-alias']
restored: selftest_exit=0; scan_exit=1; MADO_TRIPWIRE: findings; findings=[('tool_install', 'npm:install-global', 1)]
CASE npm-add-global-alias ok
SELFTEST_SUMMARY: 1/1 passed failed=[]
```

Raw complete scan JSON, stderr, selftest output and exact argv: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/proposal-results.json`.

### M16 — jj-absorb-with-ignore-working-copy

The existing absorb case has no ignore flag: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-vcs/jj-write-subcommands.jsonl:13`. Removing absorb from `JJ_WRITE` still yields `jj:absorb` via the generic snapshot fallback at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:521`. Existing explicit-write-with-ignore cases cover commit/bookmark/op/git, not absorb: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-vcs/jj-mutation-with-ignore.jsonl:2-5`. Add the interaction of absorb and the ignore flag; the declared VCS contract names absorb as mutating.

- Proposal directory: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M16`.
- Expected finding: `vcs_write / jj:absorb / line 1`.
- Tool argument (`bash`):

```text
jj --ignore-working-copy absorb
```

Actual additional selftest commands:

```sh
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/pristine.py --selftest /tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M16
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/M16/mado-tripwire.py --selftest /tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M16
/usr/bin/python -I /tmp/mado-r19-MutMergedTripwire.uMlaZe/M16/mado-tripwire.py --selftest /tmp/mado-r19-MutMergedTripwire.uMlaZe/proposals/M16
```

Actual detector outputs:

```text
baseline: selftest_exit=0; scan_exit=1; MADO_TRIPWIRE: findings; findings=[('vcs_write', 'jj:absorb', 1)]
CASE jj-absorb-with-ignore-working-copy ok
SELFTEST_SUMMARY: 1/1 passed failed=[]
mutated: selftest_exit=1; scan_exit=0; MADO_TRIPWIRE: clean; findings=[]
CASE jj-absorb-with-ignore-working-copy FAIL want=(1, [('vcs_write', 'jj:absorb', 1, '')]) got=(0, [])
SELFTEST_SUMMARY: 0/1 passed failed=['jj-absorb-with-ignore-working-copy']
restored: selftest_exit=0; scan_exit=1; MADO_TRIPWIRE: findings; findings=[('vcs_write', 'jj:absorb', 1)]
CASE jj-absorb-with-ignore-working-copy ok
SELFTEST_SUMMARY: 1/1 passed failed=[]
```

Raw complete scan JSON, stderr, selftest output and exact argv: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/proposal-results.json`.

## Hashes and restoration evidence

Common original/restored SHA-256: `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d` (90,536 bytes). The following mutant digest was observed during the replay and immediately before restoration; each active path was then overwritten with the original committed bytes in a `finally` block and byte-compared equal. All 20 subsequently re-passed the full detector. No active mutated source remains.

| ID | Mutated SHA-256 | Restored exact bytes |
| --- | --- | --- |
| M01 | `a4ec65ea6365ae8293e390612ba498ac765da4f448120c8f1828c4fce810089f` | true |
| M02 | `78430fd8b67c792e95b1a626fdef9f8bb9f1db9d55a7d7806dd2a15a04f90e74` | true |
| M03 | `fd04a37940fea9023991d0fa505b4c2275b5c716e360c0f22f8d012d8e877f21` | true |
| M04 | `ccba6ba46f97ae413f2701a22352739b349ea39114f6a8dcc3bdfbadc78e1e77` | true |
| M05 | `4b3780a55711685a99c1f7597e2b9b4a1b1a4cccafd697ad07abf2569a27ba98` | true |
| M06 | `87e703acb9895e870d87baac75762847b6e37527630ba6e3044e1fcb46f3bcbe` | true |
| M07 | `b875994e88cfb73f996ae6b6e9eaa2a78f0bbd628e3a850d085d1af715f02913` | true |
| M08 | `76040723d6b785ff6433608473d1d1d7a5c2e5c7684de386b95a94e219eba8be` | true |
| M09 | `c4ef62aad5034a1a9d93f59a4adb610a25bd4868ddee74cb80386fe90d9a84fd` | true |
| M10 | `99b943d706cfa84d0c9420db6326bb31272fcd0c245d4db84314b34b8d3b8522` | true |
| M11 | `551c8d958388faa0dd5e3111314c9ce1d97d80bb9a3735a823de7459d35eff20` | true |
| M12 | `e14a31dcc3664a8028793f15fb1c6be9298586c6100cf9f5caba31bcd9e5261b` | true |
| M13 | `9d368e1efacf539bc29a43fea79c5975ebab82e48fa5968327970a6e1aab1e1b` | true |
| M14 | `6899b3f1f7a474d0eecb392ef2f770f45a27f6feb8f025f2d655ecf207e19b27` | true |
| M15 | `7825d1aa25516fac2315c7ce979eeb5b4216272eca34be8a4bfb5b65ded0ef2b` | true |
| M16 | `4a312a0b12ecf5e0589577a16b5dd7ed5b6bfd50b1125cd56251f7aa1e9be04e` | true |
| M17 | `16166b7b6114e70c90a19982c8549bd41ec3d933b4133420d12362c87c749977` | true |
| M18 | `698c996c7137cd22785b90137526d3ffa07e805d5eee04192f086bc163243db0` | true |
| M19 | `286324024fbe7543ecaaccf12eae2cb7a7203bac904111afd6f586bb908cf747` | true |
| M20 | `f845605b6c5a5aa7dc53c977acfcc513e78644361dbcc9bbd80500a27b5fb4a1` | true |

Machine-readable evidence:

- Mutation source locations, exact old/new text and all expected hashes: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/manifest.json`.
- Per-copy before/mutated/restored hashes and byte-equality results: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/restoration.json`.
- Baseline full child argv/results/stdout locations: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/baseline/results.json`.
- Mutated full child argv/results/stdout locations: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/mutated/results.json`.
- Restored full child argv/results/stdout locations: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/restored/results.json`.
- Fixture digest/symlink manifests: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/fixtures-before.json` and `/tmp/mado-r19-MutMergedTripwire.uMlaZe/fixtures-after.json`.
- Final interpreter, unchanged-fixture and source-digest evidence: `/tmp/mado-r19-MutMergedTripwire.uMlaZe/final-evidence.json`.

## Limits

- These are 20 deliberately selected plausible defects, not a statistical sample or a proof of complete coverage. The 75% score applies only to this set.
- Original-detector survivors remain reported as survivors. Proposal kills establish non-equivalence and a concrete missing regression assertion; they do not retroactively improve the existing suite score.
- The F1 whitespace mutation and both selected F2 prefix-walk mutations were killed. This holds only for the tested defects, not every possible filesystem race or symlink topology.
- No host mutation/probe, package-manager transaction, gate execution, real jj command, credential/database access, fetch, or alternate agent runtime was used. Shell payloads and recorded host-tool strings were data only.
- The first attempt to start the baseline through the asynchronous Bash transport was refused with `Background job limit reached (100)`. No detector ran in that attempt; the same bounded Python harness was then executed synchronously through Eval. This is not a baseline test failure.
- The separate incident recall, freshness, calibration and gate commands were outside this assigned mutation probe and were not rerun here. No claims about their independent result are made.
- `[UNK]` Behavior outside the exercised parser/suite forms is not established. `[INFERENCE]` The retained distinguishing proposals should close these specific five detector gaps if incorporated with their asserted findings; integration is not part of this attack.
- Evidence was completed at 2026-10-20T18:09:21Z. Scratch evidence is ephemeral `/tmp` material; the full findings, mutations, distinguishing payloads and digest ledger are preserved in this report.

## Installs

None. Existing Python 3.14.8 and read-only Git source extraction were sufficient.
