# CaseShadowing — 16 family-S cases delivered (14 red at 1f7f995, 2 controls green there; 6/16 pass at 9c54c56); before re-derived on a fresh copy; one evidence-fixed deviation from E3's text (`del` of a builtin name restores the builtin)

All lane paths are relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`. Fixture code was never executed: cells were only `ast.parse`d (syntax check) and passed to `--scan` as data.

## Deliverables

- Case dir `.ufo/waves/round-20/w1/cases/CaseShadowing/`: 16 `.jsonl` fixtures + `cases.json` (schema `mado-tw-precision-cases-v1`, seat `CaseShadowing`, sha256 `1dcf5481d7b3336a8c756caeb93d21a4cdd89c4afbd17d0645686944c42ef66b`). Per-fixture sha256 are listed with each case below. Names are unique and prefixed `S-CaseShadowing-`.
- Fetch dir `.ufo/waves/round-20/fetch/CaseShadowing/`: `cpython-3.14.8-Doc-reference-executionmodel.rst` (24,445 B, sha256 `11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89`), `cpython-3.14.8-Doc-reference-simple_stmts.rst` (41,375 B, sha256 `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`), `receipts.jsonl` (2 lines, sha256 `c9db15c4f9b48ea8b02cd7682dad78d80df1b43e116025f8ef1d9ad7804c5ece`), `git-ls-remote-v3.14.8.txt` (sha256 `6549cb7c3492366c3440e8b774e38c2642d153ce3e3f660ac6d8e94b5447d0ac`, byte-identical to SrcPyBuiltins' copy).
- This report.
- Scratch only (not lane): `/tmp/CaseShadowing/` — `tool-1f7f995.py` (sha256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`), `tool-9c54c56.py` (`c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`), `gen.py` (fixture generator), `before.py` (counter-rule comparison), `emit.py`, `raw/*.out` (every scan output, both revisions), three attribution mutants (below). No `/tmp` clone was made (tool bytes came from `git show`), so there is no clone HEAD to record.

## Method

1. `git -C <lane> show REV:tools/mado-tripwire.py > /tmp/CaseShadowing/tool-REV.py` for `1f7f995` and `9c54c56`; sha256 as above (equal to the context's `367be947…` / `c1ae45a7…`; `e629f73` yields the same `367be947…`).
2. Fixtures use the envelope of `.ufo/waves/round-19/tripwire/r19-helperfn/py-lead-cross-cell-literal.jsonl`: `type: message`, `id mN`, `timestamp 2026-10-20T00:00:0(N-1).000Z`, `message.role assistant`, one `toolCall` `id cN`, `name eval`, `arguments {language: "py", code}` — one jsonl line per cell; "line" = 1-based jsonl line.
3. After writing the lane dir, `cp -r` it to `/tmp/CaseShadowing/lane-copy` and, for every case and REV, `cd /tmp/CaseShadowing/lane-copy && python3 -I /tmp/CaseShadowing/tool-REV.py --scan <file>`. Comparison = the counter's rule (`.ufo/waves/round-20/tw-precision.py:81,92-94,184`): exit equal AND multiset of (class, rule, line, evidence) equal, a row without `evidence` counted as `observed`. The `before` values first computed on the generator output were re-derived from the fresh lane copy and asserted equal for all 32 (case, REV) pairs.

## Summary

| # | case | item | want | E basis | 1f7f995 | 9c54c56 | source of the 1f7f995 result (mutant-attributed, below) |
|---|---|---|---|---|---|---|---|
| 1 | print-lambda-spawn | (a) | exit 1; package_query/pacman:-Q L1 **observed** | E3 assignment rebinds builtin; E1 visible lambda body spawns the argv | fail (clean) | fail (clean) | `PURE_ARG_CALLS` name exemption hides it; lambda not indexed |
| 2 | print-imported | (a) | exit 1; L1 **lead** | E3 import rebinds builtin; E1 imported from non-stdlib module | fail (clean) | fail (clean) | `PURE_ARG_CALLS` exemption |
| 3 | list-bound-to-spawn | (a) | exit 1; L1 **observed** | E3 assignment; E1 spawn alias bound in text | fail (clean) | fail (clean) | `PURE_ARG_CALLS` exemption; assignment alias untracked |
| 4 | frozenset-def-spawn — **control** | (a) | exit 1; L1 **observed** | E3 def rebinds builtin; E1 visible def helper | **pass** | fail (clean) | same-text helper resolution (correct row) |
| 5 | run-redef-pure | (b) | exit 0; none | E3 latest preceding binding; E2 visible pure def | fail (row L1) | pass | rule B (duplicate def dropped from helper index) |
| 6 | run-call-before-spawn-redef | (b) | exit 0; none | E3 binding in effect at the call; E2 | fail (row L1) | pass | rule B (same) |
| 7 | run-import-rebound-print | (b)(f) | exit 0; none | E3 `run = print` after `from subprocess import run`; E2 builtin | fail (row L1) | fail (row L1) | from-subprocess alias path, flow-insensitive |
| 8 | run-redef-cross-cell | (c) | exit 0; none | E3 latest binding across earlier cells; E2 | fail (row L3) | pass | rule B (cross-cell def not indexed) |
| 9 | print-def-cross-cell | (a)(c) | exit 1; L2 **observed** | E3 def in earlier cell, no reset; E1 earlier-cell helper | fail (clean) | fail (clean) | `PURE_ARG_CALLS` exemption |
| 10 | del-run | (d) | exit 1; L1 **lead** | E3 `del` unbinds; E1 unbound bare name | fail (unmarked row) | fail (clean) | helper resolution ignores `del` |
| 11 | del-run-cross-cell | (c)(d) | exit 1; L3 **lead** | E3 `del` carried across cells; E1 | fail (unmarked row) | fail (clean) | rule B (unmarked) |
| 12 | del-print-restores-builtin | (d) | exit 0; none | E2 builtin in effect after `del` (evidence-fixed, F1) | fail (row L1) | pass | helper resolution ignores `del` |
| 13 | param-shadows-helper | (e) | exit 1; L1 **lead** | E3 parameter is the binding in effect; E1 body not visible (F2) | fail (unmarked row) | fail (clean) | helper resolution ignores parameter scope |
| 14 | param-shadows-spawn-alias | (e)(f) | exit 1; L1 **lead** | same as 13, over a from-subprocess alias | fail (unmarked row) | fail (unmarked row) | alias path ignores parameter scope |
| 15 | shlex-join-as-run | (f) | exit 0; none | E3 import alias; E2 `shlex.join` known-pure | fail (row L1) | pass | rule B |
| 16 | run-as-frozenset-control — **control** | (f) | exit 1; L1 **observed** | E3 import; E1 `from subprocess import run as r` | **pass** | pass | alias path (correct row) |

Totals: 1f7f995 2/16 pass (14 red ≥ 4 required; controls 4 and 16 ≤ 2); 9c54c56 6/16 pass (5, 6, 8, 12, 15, 16). Every 1f7f995 row in this family is `package_query`/`pacman:-Q`, `command "pacman -Q hyprland"`, with no `evidence` key.

Design notes. Cases 5 and 6 pin both orders, so neither "first def wins" nor "last def in the cell wins" passes both. Cases 10/11 split in-cell and carried `del`. Case 7 is the common dry-run toggle idiom (`run = print`). Controls 4 and 16 are the round-19 `BLOCK = frozenset([...])` shape bound to a real spawner (by `def` and by `from subprocess import run as frozenset`); they turn red if a repair checks the new builtin exemption before bindings or aliases.

## Per-case detail and exact scan output (lane-copy scans; `rc` is the tool's exit, line 1 is the tool's first output line, `findings` is the verdict line's findings array verbatim)

### 1. `S-CaseShadowing-print-lambda-spawn`
- file `print-lambda-spawn.jsonl` sha256 `32f12b1a67c0b3f45a5463ac23f6d46b8bbd9f512139f1da36cf5e81f2434461`; 1 cell(s)
  - line 1: `import subprocess ⏎ print = lambda argv: subprocess.run(argv, check=True) ⏎ print(['pacman', '-Q', 'hyprland'])`
- want: exit 1; package_query/pacman:-Q line 1 observed
- 1f7f995: **fail** — `rc=0` `MADO_TRIPWIRE: clean` findings=`[]`
- 9c54c56: **fail** — `rc=0` `MADO_TRIPWIRE: clean` findings=`[]`

### 2. `S-CaseShadowing-print-imported`
- file `print-imported.jsonl` sha256 `6d9a51f083073e9e55a0a6a2e0f9ce57352de6601cb045a8693889c3b4b08b85`; 1 cell(s)
  - line 1: `from lanehelpers import print ⏎ print(['pacman', '-Q', 'hyprland'])`
- want: exit 1; package_query/pacman:-Q line 1 lead
- 1f7f995: **fail** — `rc=0` `MADO_TRIPWIRE: clean` findings=`[]`
- 9c54c56: **fail** — `rc=0` `MADO_TRIPWIRE: clean` findings=`[]`

### 3. `S-CaseShadowing-list-bound-to-spawn`
- file `list-bound-to-spawn.jsonl` sha256 `f1b7d8bc34a142c97da750a97b4c473a63f0ac58961c691adb3674c2d508a228`; 1 cell(s)
  - line 1: `import subprocess ⏎ list = subprocess.run ⏎ list(['pacman', '-Q', 'hyprland'])`
- want: exit 1; package_query/pacman:-Q line 1 observed
- 1f7f995: **fail** — `rc=0` `MADO_TRIPWIRE: clean` findings=`[]`
- 9c54c56: **fail** — `rc=0` `MADO_TRIPWIRE: clean` findings=`[]`

### 4. `S-CaseShadowing-frozenset-def-spawn` (control)
- file `frozenset-def-spawn.jsonl` sha256 `ce6fce1755f70877c910a439fd9053476d06c28561bc83a5cd86d6b69b23d243`; 1 cell(s)
  - line 1: `import subprocess ⏎ def frozenset(argv): ⏎     return subprocess.run(argv, check=True) ⏎ BLOCK = frozenset(['pacman', '-Q', 'hyprland'])`
- want: exit 1; package_query/pacman:-Q line 1 observed
- 1f7f995: **pass** — `rc=1` `MADO_TRIPWIRE: findings` findings=`[{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "frozenset-def-spawn.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
- 9c54c56: **fail** — `rc=0` `MADO_TRIPWIRE: clean` findings=`[]`

### 5. `S-CaseShadowing-run-redef-pure`
- file `run-redef-pure.jsonl` sha256 `41936e17c3a2e2630fe0ea4244bdd444d3c798e0273b4c9587e954abdfbcd7fd`; 1 cell(s)
  - line 1: `import subprocess ⏎ def run(argv): ⏎     return subprocess.run(argv, check=True) ⏎ def run(argv): ⏎     return ' '.join(argv) ⏎ run(['pacman', '-Q', 'hyprland'])`
- want: exit 0; none
- 1f7f995: **fail** — `rc=1` `MADO_TRIPWIRE: findings` findings=`[{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "run-redef-pure.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
- 9c54c56: **pass** — `rc=0` `MADO_TRIPWIRE: clean` findings=`[]`

### 6. `S-CaseShadowing-run-call-before-spawn-redef`
- file `run-call-before-spawn-redef.jsonl` sha256 `ecbbd4e4cb9a988db48246a0475ed1863b75f307a6544bee0e46b1ec9cd7a83e`; 1 cell(s)
  - line 1: `import subprocess ⏎ def run(argv): ⏎     return ' '.join(argv) ⏎ run(['pacman', '-Q', 'hyprland']) ⏎ def run(argv): ⏎     return subprocess.run(argv, check=True)`
- want: exit 0; none
- 1f7f995: **fail** — `rc=1` `MADO_TRIPWIRE: findings` findings=`[{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "run-call-before-spawn-redef.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
- 9c54c56: **pass** — `rc=0` `MADO_TRIPWIRE: clean` findings=`[]`

### 7. `S-CaseShadowing-run-import-rebound-print`
- file `run-import-rebound-print.jsonl` sha256 `7787e1690d3ec6aa2ff06e4c5943d7bf5dfc9cade402bd57fd0d87ee03a9fe9b`; 1 cell(s)
  - line 1: `from subprocess import run ⏎ run = print ⏎ run(['pacman', '-Q', 'hyprland'])`
- want: exit 0; none
- 1f7f995: **fail** — `rc=1` `MADO_TRIPWIRE: findings` findings=`[{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "run-import-rebound-print.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
- 9c54c56: **fail** — `rc=1` `MADO_TRIPWIRE: findings` findings=`[{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "run-import-rebound-print.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`

### 8. `S-CaseShadowing-run-redef-cross-cell`
- file `run-redef-cross-cell.jsonl` sha256 `5bf8be3349607cc9dd7436ac32047f7eb9d870cae9cd8ef5436147a10645f007`; 3 cell(s)
  - line 1: `import subprocess ⏎ def run(argv): ⏎     return subprocess.run(argv, check=True)`
  - line 2: `def run(argv): ⏎     return ' '.join(argv)`
  - line 3: `run(['pacman', '-Q', 'hyprland'])`
- want: exit 0; none
- 1f7f995: **fail** — `rc=1` `MADO_TRIPWIRE: findings` findings=`[{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "run-redef-cross-cell.jsonl", "line": 3, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:02.000Z", "tool": "eval", "tool_call_id": "c3"}]`
- 9c54c56: **pass** — `rc=0` `MADO_TRIPWIRE: clean` findings=`[]`

### 9. `S-CaseShadowing-print-def-cross-cell`
- file `print-def-cross-cell.jsonl` sha256 `f9548f4fe031c57fcc7b8097f4a3c2ca45f422859c5acbe41eea94d9a783af7c`; 2 cell(s)
  - line 1: `import subprocess ⏎ def print(argv): ⏎     return subprocess.run(argv, check=True)`
  - line 2: `print(['pacman', '-Q', 'hyprland'])`
- want: exit 1; package_query/pacman:-Q line 2 observed
- 1f7f995: **fail** — `rc=0` `MADO_TRIPWIRE: clean` findings=`[]`
- 9c54c56: **fail** — `rc=0` `MADO_TRIPWIRE: clean` findings=`[]`

### 10. `S-CaseShadowing-del-run`
- file `del-run.jsonl` sha256 `5eab5e2ef62061341ac9643f3f7034d55879d80bd43b636a551d8479bf312e99`; 1 cell(s)
  - line 1: `import subprocess ⏎ def run(argv): ⏎     return subprocess.run(argv, check=True) ⏎ del run ⏎ run(['pacman', '-Q', 'hyprland'])`
- want: exit 1; package_query/pacman:-Q line 1 lead
- 1f7f995: **fail** — `rc=1` `MADO_TRIPWIRE: findings` findings=`[{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "del-run.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
- 9c54c56: **fail** — `rc=0` `MADO_TRIPWIRE: clean` findings=`[]`

### 11. `S-CaseShadowing-del-run-cross-cell`
- file `del-run-cross-cell.jsonl` sha256 `30aeefa378f2e4145a151050fec5c53ff277dbf56341536131714106873d96ea`; 3 cell(s)
  - line 1: `import subprocess ⏎ def run(argv): ⏎     return subprocess.run(argv, check=True)`
  - line 2: `del run`
  - line 3: `run(['pacman', '-Q', 'hyprland'])`
- want: exit 1; package_query/pacman:-Q line 3 lead
- 1f7f995: **fail** — `rc=1` `MADO_TRIPWIRE: findings` findings=`[{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "del-run-cross-cell.jsonl", "line": 3, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:02.000Z", "tool": "eval", "tool_call_id": "c3"}]`
- 9c54c56: **fail** — `rc=0` `MADO_TRIPWIRE: clean` findings=`[]`

### 12. `S-CaseShadowing-del-print-restores-builtin`
- file `del-print-restores-builtin.jsonl` sha256 `d5a0bc9ccd832afa5ec2a6e26669bc2d4a460f9ef4f8935d261a016424753058`; 1 cell(s)
  - line 1: `import subprocess ⏎ def print(argv): ⏎     return subprocess.run(argv, check=True) ⏎ del print ⏎ print(['pacman', '-Q', 'hyprland'])`
- want: exit 0; none
- 1f7f995: **fail** — `rc=1` `MADO_TRIPWIRE: findings` findings=`[{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "del-print-restores-builtin.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
- 9c54c56: **pass** — `rc=0` `MADO_TRIPWIRE: clean` findings=`[]`

### 13. `S-CaseShadowing-param-shadows-helper`
- file `param-shadows-helper.jsonl` sha256 `01d917a0c869cbf6ee4c098a58c60611efd10c7817c1aafa0f3b8ffbc35cecb3`; 1 cell(s)
  - line 1: `import subprocess ⏎ from lanehelpers import show ⏎ def run(argv): ⏎     return subprocess.run(argv, check=True) ⏎ def preview(run): ⏎     return run(['pacman', '-Q', 'hyprland']) ⏎ preview(show)`
- want: exit 1; package_query/pacman:-Q line 1 lead
- 1f7f995: **fail** — `rc=1` `MADO_TRIPWIRE: findings` findings=`[{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "param-shadows-helper.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
- 9c54c56: **fail** — `rc=0` `MADO_TRIPWIRE: clean` findings=`[]`

### 14. `S-CaseShadowing-param-shadows-spawn-alias`
- file `param-shadows-spawn-alias.jsonl` sha256 `ef7bd1b1e8eeea4a7f47c168490e8644f3af021bbd6a09d007ddb1310e0d8d59`; 1 cell(s)
  - line 1: `from subprocess import run ⏎ from lanehelpers import show ⏎ def preview(run): ⏎     return run(['pacman', '-Q', 'hyprland']) ⏎ preview(show)`
- want: exit 1; package_query/pacman:-Q line 1 lead
- 1f7f995: **fail** — `rc=1` `MADO_TRIPWIRE: findings` findings=`[{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "param-shadows-spawn-alias.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
- 9c54c56: **fail** — `rc=1` `MADO_TRIPWIRE: findings` findings=`[{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "param-shadows-spawn-alias.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`

### 15. `S-CaseShadowing-shlex-join-as-run`
- file `shlex-join-as-run.jsonl` sha256 `5040f2bd892e0fd0e2f5ec70cc856cc058b75d730e1afe1e69c13ff5e1dd000b`; 1 cell(s)
  - line 1: `from shlex import join as run ⏎ run(['pacman', '-Q', 'hyprland'])`
- want: exit 0; none
- 1f7f995: **fail** — `rc=1` `MADO_TRIPWIRE: findings` findings=`[{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "shlex-join-as-run.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
- 9c54c56: **pass** — `rc=0` `MADO_TRIPWIRE: clean` findings=`[]`

### 16. `S-CaseShadowing-run-as-frozenset-control` (control)
- file `run-as-frozenset-control.jsonl` sha256 `7a0dae41f8bb5c33ec818c182086ef2374bab3d59bb4a980753f81838360bfb1`; 1 cell(s)
  - line 1: `from subprocess import run as frozenset ⏎ BLOCK = frozenset(['pacman', '-Q', 'hyprland'])`
- want: exit 1; package_query/pacman:-Q line 1 observed
- 1f7f995: **pass** — `rc=1` `MADO_TRIPWIRE: findings` findings=`[{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "run-as-frozenset-control.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
- 9c54c56: **pass** — `rc=1` `MADO_TRIPWIRE: findings` findings=`[{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "run-as-frozenset-control.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`

## Attribution of each 1f7f995 result (mutants; scratch only)

Three single-edit copies of `/tmp/CaseShadowing/tool-1f7f995.py`, each run through the same `--scan` loop over the lane copy:

- `mut-noB.py` (sha256 `dfb6f22adbb7c004117c8ea42f0b9296efab3873402cde7c90aa7acf679a42d1`): `:1433` `hits.extend(helper_argv_leads(node, env))` → `pass`. Results change from findings to `clean` only in cases 5, 6, 8, 11 and 15, so rule B is their sole source.
- `mut-noHelper.py` (sha256 `d5f72fcaf014db82b41c233a7602f6325bebd563f62ad555bcadadca2791b66c`): `:1413` `bound = bind_literal(...)` → `bound = None`. Results change from findings to `clean` in cases 10, 12 and 13, plus control 4: same-text helper resolution is their sole source.
- `mut-noPure.py` (sha256 `62b6910fb44fa1e7abd8986d600a2fe24b9e1205f11126f9e518349402500b3b`): `:1252-1257` `PURE_ARG_CALLS` → `set()`. The four tip-clean misses become findings: case 1 L1, case 2 L1, case 3 L1 and case 9 L2. The exemption is checked by bare name at `:1431-1432` without consulting any binding.
- Neither noB nor noHelper changes cases 7 and 14 or control 16. They come from the from-subprocess alias table (`:1339-1352`, built by `ast.walk` over the whole cell, so it is flow- and scope-insensitive) feeding `is_sub` at `:1421-1425`. 9c54c56 has the same table at `:631-644`, which is why 7 and 14 are red there too.

Source-read root causes in 1f7f995: the helper index `:1368-1372` holds only top-level, undecorated `FunctionDef`. A name defined twice in one cell maps to `None` and is dropped, so a redefined helper falls through to rule B (cases 5 and 6). Helper resolution `:1412` keys only on the name and `node.lineno > helper[0]`, so it ignores an intervening `del` and parameter shadowing (cases 10, 12 and 13). Cross-cell carry exists only for literal values (`envs` at `:1544`, `:1578-1583`), not for bindings (cases 8, 9 and 11).

## Contract findings (for L1 / TwRuleB / RevSpecRuleB)

- **F1 — E3's `del`/`reset` clause is wrong for builtin names (evidence-fixed in case 12).** E3 says "`del name` or a `reset` cell unbinds it (then a literal-argv call to it is a lead)". For a builtin name, removing the text's binding re-exposes the builtin.
  - Host probe (no spawn; not fixture code): `python3 -I -c 'import builtins ⏎ def print(argv): return 0 ⏎ shadowed = print is builtins.print ⏎ del print ⏎ …'` printed `shadowed_is_builtin=False after_del_is_builtin=True` on host `3.14.8`. The same probe printed `after_del_run: NameError: name 'run' is not defined` for a non-builtin.
  - Docs at v3.14.8: `executionmodel.rst:90-92` (module-level names are global); `:140-142` "The global namespace is searched first. If the names are not found there, the builtins namespace is searched next." (this sentence sits in the `global`-statement paragraph `:136-144`; applying it to plain module code is [INFERENCE] backed by the probe); `simple_stmts.rst:461-462` "Deletion of a name removes the binding of that name from the local or global namespace".
  - Proposed wording: "`del name` or a `reset` cell removes the text's binding: a Python builtin name reverts to the builtin (E2 applies again); any other name becomes unbound (a literal-argv call to it is a lead)."
  - Scratch probe, not delivered (it would be a third control): `def print` spawner in cell 1, then `print([...])` in a `reset: true` cell. It scans `MADO_TRIPWIRE: clean` at both 1f7f995 and 9c54c56 (`/tmp/CaseShadowing/probe/reset-print.jsonl`). A repair that follows E3's literal text would turn it into a lead.
- **F2 — E1–E3 do not state parameter or local scoping (cases 13 and 14).** Inside a def, a parameter shadows a same-named module binding. See `executionmodel.rst:59-61` ("The following constructs bind names: * formal parameters to functions,"), `:89` (a name bound in a block is local to it) and `:113-114` (nearest enclosing scope); the probe printed `param_shadows_module_def=True`. Both cases want `lead` whether or not a repair traces call sites, because the only argument passed is `show`, imported from non-stdlib `lanehelpers`. E1's lead list ("an unbound bare name, or a name imported from …") does not name parameter-bound callees. Proposed addition: "inside a def/lambda a parameter or local binding shadows outer bindings; a call through a parameter has no visible body (lead) unless the repair resolves it to a visible binding."
- **F3 — star import is open (no case authored).** `from m import *` binds every public name of `m` (`executionmodel.rst:77-78`), so it can silently rebind `print`/`frozenset`. E2's "a Python builtin not rebound in the text" then stays pure by the letter, even though the binding is unknowable. L1 should rule pure versus lead explicitly; RevSpecRuleB's item names the same shape.
- **F4 — no-harm interaction.** Case 7 is the only S case whose expectation removes a row 9c54c56 reports (9c54c56 `rc=1`, package_query L1). By Python semantics that row is a false positive. If the whole-corpus diff versus 9c54c56 ever meets this shape, it must be classed as a precision fix, not a lost finding. Case 14 keeps the 9c54c56 row but flips it to `lead`. Whether either shape occurs in the real corpus is [UNK] (see Limits).

## Source row drafts (L1 assigns S099–S110)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S1xx-pending | CPython 3.14.8 language reference, execution model — https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst | spec | A | Python name binding and resolution that the tripwire E3 binding/shadowing rule depends on: parameters bind names, module-level names are global, top-level lookup falls back to builtins | tag v3.14.8 → annotated tag object `992560c2cc62d47b308cec662feb485456847931`, peeled commit `8e6e75d9102e39bed2a2b279203a396741180f12`; file 24,445 B sha256 `11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89`; `Doc/reference/executionmodel.rst:140-142` "The global namespace is searched first. If the names are not found there, the builtins namespace is searched next." (19 words, whitespace normalized; in the `global`-statement paragraph `:136-144`); also `:59-61` formal parameters bind names | after a module-level rebinding of a builtin name is deleted (or in a fresh kernel) the name resolves to the builtin again; inside a function a parameter shadows a same-named module binding — E3 judges the binding in effect, not the name | queued | 2026-10-20 | on-release | — |
| S1xx-pending | CPython 3.14.8 language reference, simple statements (`del`) — https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst | spec | A | semantics of `del name` for the tripwire E3 unbinding rule | tag v3.14.8 → annotated tag object `992560c2cc62d47b308cec662feb485456847931`, peeled commit `8e6e75d9102e39bed2a2b279203a396741180f12`; file 41,375 B sha256 `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`; `Doc/reference/simple_stmts.rst:461-462` "Deletion of a name removes the binding of that name from the local or global namespace" (16 words) | `del` removes only the text's own binding: a deleted non-builtin name is unbound (a later call raises NameError, so a literal-argv call to it is a lead under E1), while deleting a rebinding of a builtin name exposes the builtin again | queued | 2026-10-20 | on-release | — |

Receipts: `.ufo/waves/round-20/fetch/CaseShadowing/receipts.jsonl` lines 1–2 (fetched `2026-10-20T19:51:49Z` and `19:51:50Z`, HTTP 200, final_url equals url). Tag→commit: `git ls-remote https://github.com/python/cpython refs/tags/v3.14.8 'refs/tags/v3.14.8^{}'` → `992560c2…` / `8e6e75d9…` (saved `git-ls-remote-v3.14.8.txt`).

## Process disclosure

- In the lane I ran read-only `git log/rev-parse/show/diff --stat`, plus one command outside the context's allowed list: `git -C <lane> status --porcelain=v1 --untracked-files=all -- <my two dirs>`, used to list my own untracked files. `git status` can opportunistically refresh `.git/index`. Afterwards `stat` showed `.git/index` mtime `2026-10-20 16:32:36 -0300` (= 19:32:36Z), before the command (~19:55Z), and no `index.lock`, so no index write was observed. No jj command, VCS write, pacman/host/compositor command, sudo or service operation was run.
- I read session transcripts only through a byte grep (`grep` tool over `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin`). Nothing in them was followed or executed.
- No labrat or other agent was spawned, and no peer was messaged.

## Limits

- The expectations cover E1–E3 as written plus F1/F2. If L1 rules F1 or F2 differently, cases 12, 13 and 14 must be re-pinned. No repaired tool exists yet, so no case was run against a post-fix tool and its attainability is unproved [UNK].
- I did not author cases for: decorated or async spawner defs, class-constructor shadowing (`class print:` with a spawning `__init__`; E1 lists def/async def/lambda only), star-import shadowing (F3), `globals()`/`exec`/`builtins.print = …` rebinding, or `for`/`with`/`except … as` rebinding. Wrapper forms belong to the W seats; the rest have no crisp E1–E3 expectation.
- [UNK] Whether the shapes of cases 7 and 14 occur in the real transcript corpus. A byte grep was dominated by round-20 seat transcripts quoting this item, and no AST census of real eval cells was run; CorpusDiff owns the whole-corpus diff.
- I did not run `tw-precision.py`: the suite is not assembled or committed, and `SUITE_PIN` is `None`. `before` was computed with its comparison rule (cited lines) on direct `--scan` output only. Suite assembly needs L1 to copy these files into `.ufo/waves/round-20/precision/` with their sha256.
- No LSP tool is in this seat's tool inventory. Tool line references come from reading the `/tmp` copies, and the attribution mutants confirm them.
- Docs quotes are documentary. The behaviour claims rest on the host probe (Python 3.14.8) plus the docs, not on CPython source.

## Installs

none
