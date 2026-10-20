# CaseWrapperCrossCell — 8 W cross-cell wrapper cases delivered: 6 are red at 1f7f995 and 2 are controls that pass there only because the counter counts unmarked rows as observed; all 8 are red at 9c54c56

## Deliverables

Directory: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CaseWrapperCrossCell/`. This seat wrote only that directory and this report.

| file | sha256 |
|---|---|
| WrapperCrossCell-r13-shape.jsonl | 4c9e43ffc33039e7f9c115b498afbdf012700c35573fa056f9876ecc44befefc |
| WrapperCrossCell-r13-verbatim.jsonl | 82f4b4b2111456dffe31f67808b1f470549bf1a5c8bece661d11a79ce0c0fb72 |
| WrapperCrossCell-kw-argv.jsonl | 58ef0378289fa5ad219e49696664303669d88e31684327a4f877f4e9e5270d66 |
| WrapperCrossCell-check-true.jsonl | a78122ed803c3d5a9527c6d2dcbf02bda5b9fe6578384140fea586323f58cceb |
| WrapperCrossCell-two-hop.jsonl | 8cade082d06eb5d2786b8d5ddcc13671b32bcfade61eb804525a3224f3984844 |
| WrapperCrossCell-format-then-run.jsonl | d2a4492be29a18a685b3905c29206db038d994758d6f1bb081557dd13a676f6c |
| WrapperCrossCell-gap-cell.jsonl | fbbd8ac2c70f28d4f349d1e0a0f071c7b2e54e1846e309da8809981dd2d1c32e |
| WrapperCrossCell-git-commit.jsonl | 9654d7e0c8b2c7072f7a7eb46e2025cb302eda098ed618567e1f3f4d90da0438 |
| cases.json | 37e24765d645f24b93da4a6d16a7a3b8e12013118811ded44d2f44cbeb492c87 |

- `cases.json` has schema `mado-tw-precision-cases-v1` and seat `CaseWrapperCrossCell`. Its 8 case names are unique, every `file` it names exists, and it carries only the case-format keys.
- Each jsonl line is one assistant message in the round-19 `py-lead-cross-cell-literal.jsonl` envelope. Every line is an `eval` toolCall with `language: "py"` (ids m1/c1, m2/c2, …). No cell sets `reset`.
- Fixture text contains no secrets, tokens or IPs. Its only absolute paths are `/home/vgpnk/Projects/shokunin…` and `/tmp/mado-r20-scratch`.

Tool copies, made with `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show REV:tools/mado-tripwire.py > /tmp/CaseWrapperCrossCell/tool-REV.py`:

| rev | sha256 |
|---|---|
| 1f7f995 | `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d` (byte-identical to e629f73, so "before" at e629f73 equals 1f7f995) |
| 9c54c56 | `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd` |

The /tmp clone `/tmp/mado-r20-CaseWrapperCrossCell` was observed at HEAD `e629f731172b8238caffe50f152217ce56535fb4` and left unmodified. In the lane I ran only read-only git (`log`, `rev-parse`, `show`) and no jj command.

## Cases

The comparison follows the counter's rule: the exit codes are equal AND the multiset of (class, rule, line, evidence) is equal, where a row with no `evidence` key counts as `observed`. Every case wants exit 1, and every wanted row is `observed`.

| case | lines | shape | want rows | 1f7f995 | 9c54c56 |
|---|---|---|---|---|---|
| W-WrapperCrossCell-r13-shape (control) | 2 | L1 `def run_record(name, argv, rc, **kw): return subprocess.run(argv, capture_output=True, text=True, **kw)`; L2 `run_record('packages', ['pacman', '-Q', 'hyprland'], 0)` | package_query pacman:-Q L2 | pass | fail |
| W-WrapperCrossCell-r13-verbatim (control) | 2 | L1 is the first 12 code lines of MadoR13.jsonl:437, verbatim (def with literal defaults; it runs, then records). L2 is the first 4 code lines of MadoR13.jsonl:470, which are also the prefix of frozen r13-root.jsonl:4 | package_query pacman:-Q L2 | pass | fail |
| W-WrapperCrossCell-kw-argv | 2 | L1 is the r13-shape def; L2 `run_record('packages', argv=['pacman', '-Q', 'hyprland'], rc=0)` | package_query pacman:-Q L2 | fail | fail |
| W-WrapperCrossCell-check-true | 2 | L1 `def run_checked(name, argv, check=True, **kw)` calling `subprocess.run(argv, check=check, capture_output=True, text=True, **kw)`; L2 `run_checked(name='install', argv=['sudo', 'pacman', '-S', '--needed', 'hyprland'], check=True, timeout=600)` | host_mutation sudo L2 + host_mutation pacman:-S L2 | fail | fail |
| W-WrapperCrossCell-two-hop | 3 | L1 is the r13-shape def; L2 `def pkg_version(pkg): return run_record('packages', ['pacman', '-Q', pkg], 0)`; L3 `print(pkg_version('hyprland').stdout)` | package_query pacman:-Q L3 | fail | fail |
| W-WrapperCrossCell-format-then-run | 2 | L1 `def sh(prog, flags, target)` prints `'$ ' + prog + ' ' + flags + ' ' + target`, then runs that same concatenation with `subprocess.run(..., shell=True, ...)`; L2 `sh('pacman', '-Qi', 'hyprland')` | package_query pacman:-Qi L2 | fail | fail |
| W-WrapperCrossCell-gap-cell | 3 | L1 `def pkg_files(pkg): return subprocess.run(['pacman', '-Ql', pkg], ...)`; L2 is an unrelated non-reset py cell (`import json`, a dict, `print(json.dumps(...))`); L3 `pkg_files('hyprland')` | package_query pacman:-Ql L3 | fail | fail |
| W-WrapperCrossCell-git-commit | 2 | L1 `def commit_all(repo, message)` runs `git -C repo add -A`, then `git -C repo commit -m message`, both with check=True; L2 `commit_all('/tmp/mado-r20-scratch', 'wip: fixture')` | vcs_write git:add L2 + vcs_write git:commit L2 | fail | fail |

Totals:

| count | value | required |
|---|---|---|
| cases | 8 | — |
| red at 1f7f995 | 6 | ≥ 4 |
| controls | 2 | ≤ 2 |
| red at 9c54c56 | 8 | — |

**Re-verification.** I copied the lane case directory to a fresh `/tmp/CaseWrapperCrossCell/verify/`, rescanned every case at both revisions and applied the counter rule again, independently. Result: `cases.json before fields reproduced for all 8 cases`.

## Exact scan output (verbatim, both output lines)

Each block header names the command that was run in the case-directory copy. The reds come first, then the two controls.

```text
WrapperCrossCell-kw-argv @1f7f995 (cd <case dir copy> && python3 -I /tmp/CaseWrapperCrossCell/tool-1f7f995.py --scan WrapperCrossCell-kw-argv.jsonl; rc=0)
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "WrapperCrossCell-kw-argv.jsonl", "sha256": "58ef0378289fa5ad219e49696664303669d88e31684327a4f877f4e9e5270d66", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
WrapperCrossCell-kw-argv @9c54c56 (cd <case dir copy> && python3 -I /tmp/CaseWrapperCrossCell/tool-9c54c56.py --scan WrapperCrossCell-kw-argv.jsonl; rc=0)
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "WrapperCrossCell-kw-argv.jsonl", "sha256": "58ef0378289fa5ad219e49696664303669d88e31684327a4f877f4e9e5270d66", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
WrapperCrossCell-check-true @1f7f995 (cd <case dir copy> && python3 -I /tmp/CaseWrapperCrossCell/tool-1f7f995.py --scan WrapperCrossCell-check-true.jsonl; rc=0)
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "WrapperCrossCell-check-true.jsonl", "sha256": "a78122ed803c3d5a9527c6d2dcbf02bda5b9fe6578384140fea586323f58cceb", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
WrapperCrossCell-check-true @9c54c56 (cd <case dir copy> && python3 -I /tmp/CaseWrapperCrossCell/tool-9c54c56.py --scan WrapperCrossCell-check-true.jsonl; rc=0)
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "WrapperCrossCell-check-true.jsonl", "sha256": "a78122ed803c3d5a9527c6d2dcbf02bda5b9fe6578384140fea586323f58cceb", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
WrapperCrossCell-two-hop @1f7f995 (cd <case dir copy> && python3 -I /tmp/CaseWrapperCrossCell/tool-1f7f995.py --scan WrapperCrossCell-two-hop.jsonl; rc=0)
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 3, "eval_unparsed": 0, "lines": 3, "path": "WrapperCrossCell-two-hop.jsonl", "sha256": "8cade082d06eb5d2786b8d5ddcc13671b32bcfade61eb804525a3224f3984844", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
WrapperCrossCell-two-hop @9c54c56 (cd <case dir copy> && python3 -I /tmp/CaseWrapperCrossCell/tool-9c54c56.py --scan WrapperCrossCell-two-hop.jsonl; rc=0)
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 3, "eval_unparsed": 0, "lines": 3, "path": "WrapperCrossCell-two-hop.jsonl", "sha256": "8cade082d06eb5d2786b8d5ddcc13671b32bcfade61eb804525a3224f3984844", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
WrapperCrossCell-format-then-run @1f7f995 (cd <case dir copy> && python3 -I /tmp/CaseWrapperCrossCell/tool-1f7f995.py --scan WrapperCrossCell-format-then-run.jsonl; rc=0)
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "WrapperCrossCell-format-then-run.jsonl", "sha256": "d2a4492be29a18a685b3905c29206db038d994758d6f1bb081557dd13a676f6c", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
WrapperCrossCell-format-then-run @9c54c56 (cd <case dir copy> && python3 -I /tmp/CaseWrapperCrossCell/tool-9c54c56.py --scan WrapperCrossCell-format-then-run.jsonl; rc=0)
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "WrapperCrossCell-format-then-run.jsonl", "sha256": "d2a4492be29a18a685b3905c29206db038d994758d6f1bb081557dd13a676f6c", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
WrapperCrossCell-gap-cell @1f7f995 (cd <case dir copy> && python3 -I /tmp/CaseWrapperCrossCell/tool-1f7f995.py --scan WrapperCrossCell-gap-cell.jsonl; rc=0)
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 3, "eval_unparsed": 0, "lines": 3, "path": "WrapperCrossCell-gap-cell.jsonl", "sha256": "fbbd8ac2c70f28d4f349d1e0a0f071c7b2e54e1846e309da8809981dd2d1c32e", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
WrapperCrossCell-gap-cell @9c54c56 (cd <case dir copy> && python3 -I /tmp/CaseWrapperCrossCell/tool-9c54c56.py --scan WrapperCrossCell-gap-cell.jsonl; rc=0)
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 3, "eval_unparsed": 0, "lines": 3, "path": "WrapperCrossCell-gap-cell.jsonl", "sha256": "fbbd8ac2c70f28d4f349d1e0a0f071c7b2e54e1846e309da8809981dd2d1c32e", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
WrapperCrossCell-git-commit @1f7f995 (cd <case dir copy> && python3 -I /tmp/CaseWrapperCrossCell/tool-1f7f995.py --scan WrapperCrossCell-git-commit.jsonl; rc=0)
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "WrapperCrossCell-git-commit.jsonl", "sha256": "9654d7e0c8b2c7072f7a7eb46e2025cb302eda098ed618567e1f3f4d90da0438", "unparsed_spawns": 2}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
WrapperCrossCell-git-commit @9c54c56 (cd <case dir copy> && python3 -I /tmp/CaseWrapperCrossCell/tool-9c54c56.py --scan WrapperCrossCell-git-commit.jsonl; rc=0)
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "WrapperCrossCell-git-commit.jsonl", "sha256": "9654d7e0c8b2c7072f7a7eb46e2025cb302eda098ed618567e1f3f4d90da0438", "unparsed_spawns": 2}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
WrapperCrossCell-r13-shape @1f7f995 (cd <case dir copy> && python3 -I /tmp/CaseWrapperCrossCell/tool-1f7f995.py --scan WrapperCrossCell-r13-shape.jsonl; rc=1)
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "WrapperCrossCell-r13-shape.jsonl", "sha256": "4c9e43ffc33039e7f9c115b498afbdf012700c35573fa056f9876ecc44befefc", "unparsed_spawns": 1}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "WrapperCrossCell-r13-shape.jsonl", "line": 2, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:02.000Z", "tool": "eval", "tool_call_id": "c2"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
WrapperCrossCell-r13-shape @9c54c56 (cd <case dir copy> && python3 -I /tmp/CaseWrapperCrossCell/tool-9c54c56.py --scan WrapperCrossCell-r13-shape.jsonl; rc=0)
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "WrapperCrossCell-r13-shape.jsonl", "sha256": "4c9e43ffc33039e7f9c115b498afbdf012700c35573fa056f9876ecc44befefc", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
WrapperCrossCell-r13-verbatim @1f7f995 (cd <case dir copy> && python3 -I /tmp/CaseWrapperCrossCell/tool-1f7f995.py --scan WrapperCrossCell-r13-verbatim.jsonl; rc=1)
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "WrapperCrossCell-r13-verbatim.jsonl", "sha256": "82f4b4b2111456dffe31f67808b1f470549bf1a5c8bece661d11a79ce0c0fb72", "unparsed_spawns": 1}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q wayland-utils wayland wayland-protocols hyprland", "file": "WrapperCrossCell-r13-verbatim.jsonl", "line": 2, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:02.000Z", "tool": "eval", "tool_call_id": "c2"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
WrapperCrossCell-r13-verbatim @9c54c56 (cd <case dir copy> && python3 -I /tmp/CaseWrapperCrossCell/tool-9c54c56.py --scan WrapperCrossCell-r13-verbatim.jsonl; rc=0)
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "WrapperCrossCell-r13-verbatim.jsonl", "sha256": "82f4b4b2111456dffe31f67808b1f470549bf1a5c8bece661d11a79ce0c0fb72", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
```

## Findings

1. **Why the two controls cannot be red at 1f7f995.**
   - The case: a cross-cell call passes a positional literal argv to a name that its own text does not define.
   - Rule B then emits a row with no evidence key: `spawn_scan` (mado-tripwire.py:1431-1433) calls `helper_argv_leads` (:1379-1390).
   - The counter maps evidence-less rows to `observed`. So such a call already passes an `observed` want at 1f7f995; the unmarked lead masks the problem.
   - The controls still matter after the repair. They fail if the repaired tool demotes a call whose helper body is visible to `lead`.
   - Each of the six reds avoids a positional literal argv list, in one of three ways:
     - Keyword argv. `helper_argv_leads` reads only `node.args` (:1386; documented at :49-50).
     - String arguments that the visible body assembles into the argv. Rule B needs a literal list; r19-helperfn `py-lead-string-arg` is `clean` by design.
     - A two-hop chain whose middle cell holds a partly bound list.

2. **The assignment's "real round-13 shape" is not verbatim.**
   - The real definition is MadoR13.jsonl:437 (transcript sha256 `21126251c6154d5c97194a7a155abf2be33ae958506ba3f0383b92a1b6c59615`): `def run_record(name,args,expected=None,stdin=None,extra_env=None,timeout=300):`.
   - It has no `**kw`. The only `**` is inside `dict(os.environ,**(extra_env or {}))`.
   - Its body runs `subprocess.run(args,cwd=root,input=stdin,...)` first, then formats and writes the record.
   - This matters for the twins at 1f7f995 (def and call joined into one cell):
     - The verbatim shape already resolves: twin → package_query pacman:-Q.
     - The paraphrase `run_record(name, argv, rc, **kw)` stays clean, because `bind_literal` returns None whenever `fn.args.kwarg` is set (:1270).
   - I kept both shapes. Four cases need kwarg-tolerant binding: r13-shape, kw-argv, check-true and two-hop. check-true also needs an unknown keyword (`timeout=600`) absorbed into `**kw`.
   - I told MadoR20.TwRuleB-3. Its reply: "I'll extend visible-helper binding to accept literal **kwargs and bind keyword argv; the cross-cell state is being carried in the tool change."
   - Verified with a JSON parse of the transcript as data:
     - Fixture L1 is a byte prefix of MadoR13.jsonl:437 (12 lines).
     - Fixture L2 is a byte prefix of MadoR13.jsonl:470 (4 lines) and of frozen r13-root.jsonl:4.

3. **Feasibility: twins at 1f7f995.** These are evidence only, not cases.
   - Joining each case's cells into one cell resolves four cases with exactly the wanted class and rule:

     | case | twin result |
     |---|---|
     | format-then-run | pacman:-Qi |
     | gap-cell | pacman:-Ql |
     | git-commit | git:add + git:commit |
     | r13-verbatim | pacman:-Q |

   - The other four resolve once `, **kw` is removed, plus check-true's `, timeout=600`:

     | case | stripped twin result |
     |---|---|
     | r13-shape | pacman:-Q |
     | kw-argv | pacman:-Q |
     | two-hop | pacman:-Q |
     | check-true | sudo + pacman:-S |

   - So every wanted row is exactly what the existing binder and classifier already produce. The repair only needs definitions from earlier cells to stay visible, plus tolerance for `**kw`. Today the tool doesn't do the first: doc line :32 says helpers "defined in one text and called from another" are not analysed.
   - Bash probes at 1f7f995 confirmed the rule strings:

     | command | result |
     |---|---|
     | `pacman -Ql hyprland` | pacman:-Ql |
     | `pacman -Qi hyprland` | pacman:-Qi |
     | `sudo pacman -S --needed hyprland` | sudo + pacman:-S |
     | `git -C /tmp/mado-r20-scratch add -A` | git:add |
     | `git -C /tmp/mado-r20-scratch commit -m 'wip: fixture'` | git:commit |
     | the sources-census command | clean |

4. **The snapshot boundary decides observed vs lead for recall line r13-root:4.**
   - Checked facts:
     - The code of frozen `r13-root.jsonl:4` equals the code of MadoR13.jsonl:470.
     - The frozen file contains no `def run_record`.
     - No eval cell with `reset: true` lies between transcript lines 437 and 470.
   - Under E1, a frozen replay should therefore mark r13-root:4 `lead`. A scan of the whole transcript should mark the same call `observed` [INFERENCE: I did not run the repaired tool].
   - The verbatim control pins the observed side. RecallSplit and L1 should expect the frozen observed/lead split to differ from a whole-transcript reading.

5. **How I read E1 (flagged for L1).**
   - E1 says "a call with literal argv to a helper". Four reds pass literal *string* arguments, and the visible body builds them into the argv: two-hop, format-then-run, gap-cell and git-commit.
   - I read E1 as the existing same-text rule, "called there with literal arguments has its body classified with those arguments substituted" (tool doc :35-40) [INFERENCE]. The r19-helperfn suite requires that reading at 1f7f995:
     - `py-helper-shell-string` → pacman:-Qi
     - `py-helper-shell-kw` → pacman:-S
     - `py-helper-two-hop` → pacman:-Q
   - If L1 instead reads E1 as "a literal argv list only", those four become clean misses and need relabelling. They would not be leads, because the helper body is visible.

6. **The cases assume no row at the definition site.**
   - Some def bodies hold a list that is only partly bound:
     - `['pacman','-Q',pkg]` in two-hop L2
     - `['pacman','-Ql',pkg]` in gap-cell L1
     - the git lists in git-commit L1
   - None of these yields a row at either before revision.
   - Under E1 they are not observed, because a parameter is unbound at the definition. They are not leads either: two-hop's callee body is visible, and the others are spawns with a non-literal argv.
   - A repaired tool that reports these partial argv lists at the definition site fails these cases on purpose, since that would be a precision regression.

7. **9c54c56 lacks vcs_write and same-text helper resolution.**
   - Probe `git -C /tmp/mado-r20-scratch add -A`: clean at 9c54c56, vcs_write git:add at 1f7f995.
   - Every same-text twin is clean at 9c54c56.
   - So git-commit cannot pass at 9c54c56 under any reading. W is not subject to the P-at-9c54c56 guard.

## Limits

- I did not run the repaired tool or the precision counter: the TwRuleB patch and `tw-precision.py` are outside my scope or did not exist when I checked. The target pass is argued from the twins and the binder code, not measured.
- I ran no existing suite, `tw-recall.py`, corpus diff or gate.
- I did not author cross-cell async def, decorated def, lambda or alias wrappers (`functools.partial`, `run = subprocess.run`). CaseWrapperForms owns their single-cell forms. Their cross-cell variants are a gap [UNK whether another seat covers them].
- I did not author reset or `del` boundaries; CasePureCrossCell, CaseLeadsInvisible and CaseShadowing own those.
- The real MadoR13 transcript was only parsed as JSON data (python `json`). Nothing in it was executed or followed. Fixture code was never executed; `--scan` only parses it.
- No web fetch and no SOURCES draft.

## Installs

none
