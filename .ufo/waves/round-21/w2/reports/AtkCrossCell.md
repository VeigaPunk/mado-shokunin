# CrossCell — scoped C1 review

## Verdict and axes

**Advisory: no actionable defect found in the assigned CrossCell shape.** The frozen expected row is semantically warranted. The inspected repair follows the reached helper and literal values by binding shape, not by matching this fixture's identifiers or package text. One nearby bounded variant emitted the expected observed query; that is evidence for this shape, not a global no-counterexample claim.

Axes assessed:

1. **Frozen semantic warrant:** class, command and evidence for CrossCell.
2. **Repair generality:** cross-cell state, helper invocation and argument-to-argv flow.
3. **Nearby falsification:** a changed helper/parameter with a cross-cell literal passed by keyword.

## Frozen expected row

`oracle/expected.json` entry `CrossCell` (fixture SHA-256 `051791ab1325e7298416604684437da984ca907600eb85788f1193416d6f83a6`; proposal SHA-256 `021d82e54aa04d4a8671956e95944d5206aaa7bcce151a8706b4c110d9b74da5`) expects exactly:

```json
{"class":"package_query","command":"pacman -Q r21","evidence":"observed"}
```

The transcript has two Python eval cells, each `reset:false`: the first imports `subprocess` and defines `query_package(name)` whose body calls `subprocess.run(["pacman", "-Q", name])`; the second directly calls `query_package("r21")`. The helper body is reached, and its only command argument is completely determined as `pacman -Q r21`. CPython 3.14.8's execution-model source states that formal parameters, function definitions and imports bind names, with module-level names global and resolved in the enclosing environment (`w1/sources/SourceNamespace/cpython-v3.14.8-executionmodel.rst:55-96`). Python 3.14's `subprocess.run` documentation says it runs the command described by `args`; its command argument accepts a sequence (`https://docs.python.org/3.14/library/subprocess.html#subprocess.run`). The installed `pacman(8)` manual, OPERATIONS `-Q, --query`, says it queries the package database; querying an absent package would not change the command's class. Thus `package_query` is warranted, and `observed` (not merely a lead) is warranted by the direct call with bound arguments. This describes a recorded command path, not a claim about whether `r21` is installed or what output it returned. No transcript code or pacman command was executed.

## Repair generality

The current candidate is commit `f499a8d` (full revision reported by L1: `f499a8db7171b7476fe9f204ab9edbac5a956fa9`). `tools/mado-tripwire.py` had SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d` before and after the bounded probe.

The relevant implementation is shape-based:

- `scan_file` retains Python literal and callable-binding environments across eval records in a file, and resets those environments only for `reset:true` (`tools/mado-tripwire.py:2502-2562`). `update_bindings` records imports and visible function definitions (`:1717-1735`).
- `bind_literal` binds positional, keyword and default arguments; `literal_value` resolves names and literal containers (`:1322-1378`, `:1896-1964`). `follow_helper` scans the invoked helper with those bound values (`:2155-2200`).
- `spawn_scan` folds the reached `subprocess.run` argv and sends the resulting command to the ordinary shell/classifier path (`:2201-2450`); `classify_pacman` maps query operation `-Q` to `package_query` (`:737-784`).

This is an ordinary cross-cell helper → bound parameter → literal argv path. Nothing in those mechanisms depends on `CrossCell`, `query_package`, `name`, or `r21`; the package/query classification is the general pacman option rule. The frozen rationale's `observed` classification agrees with the followed direct-call path.

## Nearby bounded variant

Retained inert input: `.ufo/waves/round-21/w2/fixtures/AtkCrossCell-2/keyword-through-cell.jsonl` (SHA-256 `3a7b81dc0b46b75a2be2bd293c7127d1386472d3d15df0bbca81c8a5c185a7f4`). It changes the helper to `check_pkg(pkg_name)`, assigns `target = "kern"` in a separate middle cell, then calls `check_pkg(pkg_name=target)` in a third cell; every cell has `reset:false`. This tests persistent helper and literal bindings with keyword argument binding while changing the fixture identifiers and value.

I invoked the existing `oracle/measure.py` `scan(tool, fixture)` API once for this inert JSONL only. It uses a single scanner child with `RLIMIT_AS=402653184` and a 15-second timeout; the Python/shell text in the fixture was data and was not executed. Observed scanner result:

```text
scanner exit: 1 (one detected finding is unpermitted with the default empty permit set)
counts: package_query=1; host_mutation=0; live_probe=0; tool_install=0; vcs_write=0
observed_findings=1; lead_findings=0; unparsed_spawns=0; eval_unparsed=0; stderr=""
finding: class=package_query, command="pacman -Q kern", evidence=observed, rule=pacman:-Q, line=3
```

The exit 1 is the expected default `--scan` verdict for an unpermitted detected query, not a timeout, parse failure or missing finding. This variant did not falsify the rule.

## Residual risk and verification gaps

- This was one nearby variant only; no whole-corpus or full-suite run was performed. The original CrossCell case was not separately rescanned against the current candidate. The available `oracle-candidate.json` receipt measures commit `843d301` with a different tool SHA (`56ff93751ac09a75065534b5a8d7af5f94986369cee6963b49d27912fce73e11`), so I did not treat that receipt as current-candidate evidence.
- No LSP device/server was exposed in this seat's tool inventory, so LSP status, references, definition and diagnostics were unavailable. Source conclusions above come from direct implementation tracing; textual search, where used, was only a literal check and is not semantic proof.
- No tools were installed or updated.
