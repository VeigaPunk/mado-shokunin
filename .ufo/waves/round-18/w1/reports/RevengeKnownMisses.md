# RevengeKnownMisses — three real tripwire misses, reconstructed

Scope: `MadoR14.SourceSafety.jsonl:152,155` and `MadoR13.jsonl:470` — what was
issued, what ran, why the baseline tripwire cannot see it, and the minimal rule
per miss. Read-only: no lane file was edited; no `pacman`, probe or service
command was run. Fixtures and a throwaway prototype live under `/tmp/rkm/`.

## 0. Anchors

**Tool.** All line numbers and the sha below are for the immutable baseline blob
`git show d9a5a18:tools/mado-tripwire.py` → sha256
`962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072`, 935 lines.
The working tree has since diverged (`tools/mado-tripwire.py` is now 1160 lines,
sha `593b3aaf…`, `--frozen` landing concurrently), so line citations here are
baseline-only: re-anchor by symbol name, not by number.

**Transcripts** (both sha256 match `.ufo/waves/round-17/evidence/session-index.json`):

| file | sha256 | lines |
|---|---|---|
| `MadoR14/MadoR14.SourceSafety.jsonl` | `ee7331bf5d42…` | 193 |
| `MadoR13.jsonl` | `21126251c615…` | 541 |

Each cited line is a `type:"message"`, `role:"assistant"` record whose
`content[]` carries a `type:"toolCall"`, `name:"eval"`, `arguments.language:"py"`
(the 470 record also holds three empty thinking blocks). The adjacent
`tool_execution_start` event for these eval cells carries intent text but no
code; `scan_file` reading only message records (773–778) loses nothing.

**Baseline verdicts** (blob, not working tree):

| file | label | findings | unparsed_spawns |
|---|---|---|---|
| SourceSafety | `findings` | 5 × `package_query`, lines 38, 45, 45, 107, 107 | 2 |
| MadoR13 | `clean` | 0 | 5 |

The five caught SourceSafety findings are literal `pacman -Q…` bash cells at
lines 38/45/107. The same transcript's `pacman -Q` inside the two eval cells is
not among them: the classifier knows `pacman -Q`; the payload never reaches it.

Round-17 receipts re-verified byte-for-byte: `tripwire-r13/14/15/16.txt` replay to
33/50/209/2 findings, and none carries `tool_sha256` or `measured_commit`
(grep count 0) — consistent with R17-V1/V2.

## 1. Miss A — `SourceSafety.jsonl:152` (`bash -c "$recipe"`, argv by name)

Shape (long tokens shortened; full bytes at the line):

```python
recipe = r'''
set -euo pipefail
HYPR=<hex40>   # v0.56.2 (S041 pin)
...
fetch(){ curl -fsSL --max-time 30 "$1" -o "$T/$2"; }
fetch …                                  # 8 raw.githubusercontent / gitlab raws
( cd "$T" && sha256sum om.cpp pm.cpp comp.cpp mrm.cpp ctm.cpp om-vendored.xml om-upstream.xml cm.xml )
b(){ if "$@" >/dev/null 2>&1; then echo true; else echo false; fi; }
echo "…"  # 12 echo probes + 1 in the /usr/share/wlr-protocols loop (13 values, 12 boolean)
pacman -Q hyprland wayland-protocols wayland-utils 2>&1 || true
'''
import subprocess
p = subprocess.run(["bash","-c",recipe],capture_output=True,text=True)
```

**Executed.** `bash -c recipe`, rc `0` (first byte of the result at line 154).
The result's tail is decisive: `hyprland 0.56.2-2`, `wayland-protocols 1.49-1`,
`wayland-utils 1.3.0-1` — a live package query whose output was captured. The
`|| true` suppresses only the exit status, not the read. (The eight `curl`
fetches and the `/usr/share` `cmp` also ran; neither is a paused host action.)

**Why the baseline misses it — code path.** `scan_file` (773–778) passes
`arguments.code` to `classify_eval` (586). The spawn is
`subprocess.run(<List>)`; `str_list` (579–583) requires *every* element to be
`ast.Constant`, and element 3 is `ast.Name('recipe')`, so it returns `None`.
The `List` is not `ast.Constant`, so control falls to `unparsed += 1` (672).
No shell text is ever synthesized, so `classify_segment`/`classify_pacman`
(509–513) never see `pacman`. This is the tool's declared limit, docstring line
16 ("non-literal spawn arguments (counted as unparsed_spawns)") — and the label
computation (828) never consults the counter, so `clean` can coexist with it.

**Minimal rule A — argv resolves through literal name bindings.**
For a recognised spawn, resolve each argv element that is a bare `Name` (also
`JoinedStr`/`BinOp(Add)` of literals) through the most recent literal assignment
to that name in the same transcript file; anything unresolved stays unparsed.
Pure AST; nothing is read or executed. Patch points: `str_list` (579) resolves;
`classify_eval` (586) takes a bindings map; `scan_file` (778) keeps one map per
file (one eval kernel per file).

**Check A.** Fixture `f1` = the shape above with the fetch/probe body elided but
the `pacman -Q … 2>&1 || true` line and the `subprocess.run(["bash","-c",recipe])`
call intact. Baseline: `clean`, `unparsed_spawns 1`. With rule A: `findings`,
`(1, package_query, pacman:-Q)`, unparsed 0. Control `f1-literal`
(`subprocess.run(["bash","-c","pacman -Q hyprland"])`, payload literal) is
already `findings` at baseline — proving only reachability changes, not
classification.

## 2. Miss B — `SourceSafety.jsonl:155` (`bash -c recipe2`, computed string)

Shape:

```python
recipe2 = recipe.replace("pacman -Q hyprland", """grep -n -e 'setDisableHead' … "$T/om.cpp"
grep -n -e 'isGlobalPrivileged' … "$T/pm.cpp"
… five more grep -n …
pacman -Q hyprland""")
assert recipe2 != recipe
p = subprocess.run(["bash","-c",recipe2],capture_output=True,text=True)
```

**Executed.** A second `bash -c`, rc `0` (line 157 begins `0`). The result
repeats the whole recipe — the same sha256 block, the same 13 probes — now with
six `grep -n` anchor lines prepended, and again ends with the three package
lines. So a *second* live `pacman -Q hyprland wayland-protocols wayland-utils`,
plus six `grep -n` invocations. `assert recipe2 != recipe` passing proves the
replacement applied.

**Why the baseline misses it — code path.** `recipe2` is
`ast.Call(Attribute(Name('recipe'),'replace'), …)`: not a `List`, not a
`Constant`. `str_list` (579) yields `None`; the fallthrough at 672 counts one
unparsed spawn. Two independent obstacles stack: (i) nothing folds `.replace` on
a string, and (ii) `recipe` is not assigned in this cell at all — it is kernel
state from the earlier cells, and `scan_file` computes each `toolCall`
independently with no carried bindings (773–778). A same-cell-only resolver
therefore still misses this line.

**Minimal rule B — fold literal `str.replace`; bindings persist per file.**
Resolve `x.replace(a,b)` when `x,a,b` resolve to literals, and keep the binding
map across cells of one file (last assignment wins; an unresolvable value drops
the name). Models the kernel, invents no dataflow.

**Check B.** Fixture `f2` = recipe + `recipe.replace(...)` + the second
`subprocess.run(["bash","-c",recipe2])`. Baseline: `clean`, unparsed 1. With
rules A+B: `findings`, `(1, package_query, pacman:-Q)`, unparsed 0. Ablation:
disabling `.replace` folding *or* cross-cell persistence each loses 155 while
152 and 470 stay found — both ingredients are individually necessary.

## 3. Miss C — `MadoR13.jsonl:470` (helper `run_record`, argv by position)

Shape (`run_record` is defined in the same transcript, cell at line 437):

```python
def run_record(name,args,expected=None,stdin=None,…):
    cp = subprocess.run(args, cwd=root, input=stdin, text=True, capture_output=True, …)
    ...
packages = run_record('packages',['pacman','-Q','wayland-utils','wayland',
                                  'wayland-protocols','hyprland'],0)
gl       = run_record('globals-recheck',['bash','-s'],0,stdin=recipe)
```

`recipe` is the first ```bash fence of
`corpus/knowledge/wayland-protocol-boundaries-r13.md`, itself a python heredoc
doing `subprocess.run(["wayland-info"], …)`.

**Executed** (result at line 472). `packages exit 0 expected 0` then
`wayland-utils 1.3.0-1`, `wayland 1.26.0-1`, `wayland-protocols 1.49-1`,
`hyprland 0.56.2-2` — a live `pacman -Q` again. `globals-recheck exit 1
expected 0` with `advertisement UNKNOWN: exit=255 stderr_bytes=52` — the
`bash -s` script also ran and invoked `wayland-info`, failing on missing session
prerequisites. Two invisible spawns on one line; the named miss is the package
query.

**Why the baseline misses it — code path.** `run_record` is not in `SPAWN_FUNCS`
(87), not in `SHELL_STRING_FUNCS` (89), not an alias, not `tool.bash`. The guard
at 640 (`if not (is_sub or is_shell_fn or is_exec or is_tool)`) skips the call
**before any counter**: line 470 contributes 0 to `unparsed_spawns` (the file's 5
come from other cells). The helper's own `subprocess.run(args, …)` has a
non-constant `args`, so that cell is counted once (651–660) — but a count says
nothing about which argv a call site supplied. Adding `run_record` to a helper
table would be name-specific and die on the next helper. The `bash -s` half is
structurally unseeable: the script body is a file outside the transcript, and the
tool's doctrine refuses to follow file reads.

**Minimal rule C — argv position, not callee.** For any call, if an argument is
a literal command vector (after rule A resolution), classify
`shlex.join(vector)`: the vector's first element is the command, whatever the
callee is named. No helper table, no interprocedural analysis; lists that do not
look like a classified command produce nothing.

**Check C.** Fixture `f3b` (`run_record('packages',['pacman','-Q',…],0)`,
helper undefined in the cell, as in the real transcript). Baseline: `clean`,
**unparsed 0** — total silence. With rule C: `findings`,
`(1, package_query, pacman:-Q)`. Ablation `noargv` loses 470 and keeps 152/155.

## 4. Measured effect of the three rules (throwaway prototype)

Prototype `/tmp/rkm/proto.py`, sha256 `5b5320c7…`, is the baseline blob plus 7
hunks (helpers, signature, bindings application, argv rule, resolved argv,
`scan_file` threading, ablation switch). Replayed read-only over the four
round-17 receipt file sets:

* 228 transcript files, 2 880 bash calls, 217 eval cells, baseline 294 findings.
* Prototype: 297 findings — exactly `+152`, `+155` (SourceSafety) and `+470`
  (MadoR13); **0 lost, 0 other additions** anywhere in the corpus.
* `unparsed_spawns` for SourceSafety 2 → 0; MadoR13 unchanged at 5.
* Baseline suites still pass: core 9/9, compound 16/16, hardening 33/33,
  w2-regressions 30/30 (run against the prototype, not the lane tool).
* Ablation matrix: `nocross` → 155 lost, `norep` → 155 lost, `noargv` → 470
  lost; no ablation loses 152.

Reproduce:

```bash
cd /home/vgpnk/Projects/shokunin/mado-shokunin
git show d9a5a18:tools/mado-tripwire.py > /tmp/base.py
sha256sum /tmp/base.py        # 962919ce…
python3 -I /tmp/base.py --scan <the two transcripts>   # 5 findings / clean
python3 -I /tmp/rkm/proto.py --scan <same>             # +152,+155 / +470
```

Fixture builder (inert JSONL; nothing is executed by the tool):

```python
import json
def cell(code):
    return json.dumps({"type":"message","id":"x","timestamp":"2026-10-20T00:00:00.000Z",
        "message":{"role":"assistant","content":[{"type":"toolCall","id":"fx-1",
        "name":"eval","arguments":{"language":"py","code":code}}]}})+"\n"
```

## 5. Residual limits no rule of this shape closes

1. **Script on stdin.** `run_record('x',['bash','-s'],0,stdin=recipe)` stays
   invisible even with rule C (`f3c`: `clean`, unparsed 0); the body lives in a
   file. Honest disposition is a counter, not a finding: a shell argv with
   `-s`/`-` and a non-constant `stdin=` is a spawn we could not see into.
2. **Dynamic string building.** `"".join`, `%`, `.format`, slicing and
   f-strings with non-constant parts stay unresolved → unparsed. Rule B folds
   only literal `.replace`.
3. **Binding approximation.** The map takes module-level assignments in source
   order; a conditional rebind inside a branch is not modelled (last top-level
   value wins). No false positive observed on the 228-file corpus, but the
   approximation should be stated wherever the rule is documented.
4. Intent is not reconstructed — only the issued command, its effect, and the
   classifier path. Whether the seats believed the counters covered them is
   `[INFERENCE]` and not needed for the fix.

## 6. Handoff / sequencing (L1 decides)

* If rules A–C land, the frozen snapshot must be re-cut: TwFrozenSnapshot is
  building `.ufo/waves/round-18/frozen-tripwire/` with 152/155/470 as
  `known_misses` (asserting **no** finding). After the rules those three become
  `expected_findings` `{class:"package_query", rule:"pacman:-Q"}`, and the
  receipt must pin `tool_sha256` + `measured_commit` (R17-V1/V2). Until re-cut,
  `--frozen` will return `frozen_verdict_mismatch` — which is the contract
  working as designed ("a finding there forces a re-pin").
* If they do not land this round, the `known_misses` are correct for the pinned
  tool, and the three lines remain the demonstrated ceiling of the current
  classifier; the receipt should say that explicitly rather than imply coverage.
* For QUALITY criteria 24–26 (one per miss), the check text is the fixture plus
  the expected finding `(line, package_query, pacman:-Q)`; each check fails on
  the baseline tool and passes with its rule, and each has a negative control
  (`f1-literal` is already caught; `f3c` stays clean by design). Lessons/QUALITY
  wording stays with L1.
* Prototype is `/tmp` only; no lane file was modified by this seat. No tool
  installs.

## 7. Confidence

* **High** — command shapes, executions (tool-result bytes quoted above), code
  paths (baseline blob, sha-pinned), baseline verdicts (blob scan reproduces the
  round-17 receipt counts 33/50/209/2).
* **High** — rule sufficiency and individual necessity (prototype replay over
  228 files plus the ablation matrix; suites unchanged).
* **Medium** — whether the rules should land this round: that is sequencing
  policy, not evidence. The technical tradeoff is in §6.
