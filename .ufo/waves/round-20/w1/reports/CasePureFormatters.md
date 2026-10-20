# CasePureFormatters — 13 P formatter cases: 11 red at 1f7f995, all 13 pass at 9c54c56, 2 controls; the real counter gives P 2/13 at 1f7f995 and 13/13 at 9c54c56

Seat: MadoR20.CasePureFormatters-3 (leaf; no labrat spawned). Family P, formatters. Every case states a host argv — `['sudo','pacman','-S','hyprland']`, `['sudo','systemctl','restart','iwd']` or `['pacman','-Q','hyprland']` — and only formats it. Want for every case: `want_exit 0`, `want_findings []`.

## Deliverable

Directory `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureFormatters/` (untracked; L1 integrates):

| sha256 | file |
|---|---|
| `30dd67e2c9bdfed34864caf9c16134835d7deea5d2a1517556f4b6b8065e4a65` | cases.json (schema `mado-tw-precision-cases-v1`, seat `CasePureFormatters`, 13 cases; keys exactly name/family/file/want_exit/want_findings/why/before) |
| `b8f5f013b77a073ed48127b4222decb074c98943b523aeb1257f1b7368a73de9` | shlex-join.jsonl |
| `af6042a32a6c2f7a815594da72e5db2d10ac46b1be804be02efb1f69cc512b4d` | json-dumps.jsonl |
| `6f9693b048fabf31ad20d8b0db00518148d4e11eeccf9043e18238a71ebcd7de` | pprint-pformat.jsonl |
| `cbed66b3dd35e77e159ba1f08cc5fbfa7b4372df7fcb6f93df46f2e9b78aa2c1` | textwrap-indent-chain.jsonl |
| `6f144da02834799a7c1a2a0bb5a8e64fd34e9a5e3906ebb65aed5aead1524b00` | lambda-join.jsonl |
| `3d4a00f9b28de0fff71585ebe27dd287b2bdf0619a87d5e8fbad4c27dab17bbf` | fstring-def.jsonl |
| `5595f2832f4bb1bb18221209e2bd2df9d6cd9f8787d9bb8535bb01a78b1a5a56` | str-format-bound.jsonl |
| `7dee943f6bd660e4c1bf8f74b64f8e470bdb8f5f560b024631e9855137e75d46` | quote-cross-cell.jsonl |
| `a4e6d30c255b6cce572f5a4ac7bde117ba6cacd64d479b104a1a9fc5b2086def` | dumps-alias.jsonl |
| `5d3b5c0065e03fcf18cc106b4d75f345cdc88fb634cd4e1bcc1877a7a1a41ae6` | join-cross-cell-import.jsonl |
| `fa4a517ff90d56bd7ac3c7d1ca74ac4b19ad73d31634007c8f96918b1e383b96` | partial-dumps.jsonl |
| `0751ef58d3126a47304539c273079f0b835f35d8d371a90b0cd56e4cc6fe3ff8` | fstring-def-control.jsonl |
| `9a7a1dca6964357178dc4e6f123dea5d12c54a4b5d1d5e0167eea63c614b6930` | dotted-control.jsonl |

Each .jsonl uses the envelope of `.ufo/waves/round-19/tripwire/r19-helperfn/py-lead-cross-cell-literal.jsonl` (type message, role assistant, one `toolCall` named `eval` with `{language:"py", code}`), one line per cell, newline-terminated. Every cell parses (`ast.parse` only). Both baseline tools report `eval_unparsed=0 unparsed_spawns=0` for every file, so no case is clean because a parse failed.

## Cases and `before`, using the counter rule

Counter rule: a case passes when the exit code matches and the multiset of (class, rule, line, evidence) matches; a row with no `evidence` key counts as `observed`. I computed it twice for each case and revision: (a) by hand, `cd /tmp/CasePureFormatters/scan-REV && python3 -I /tmp/CasePureFormatters/tool-REV.py --scan FILE`, where scan-REV is a copy of the case dir; (b) by calling `scan_case()` from `.ufo/waves/round-20/tw-precision.py`. Both readings agree on all 26 case×revision results (the runner asserts this).

| # | name | fixture code (cells separated by ‖) | 1f7f995 | 9c54c56 |
|---|---|---|---|---|
| 1 | P-CasePureFormatters-shlex-join | `from shlex import join` / `print(join(['sudo', 'pacman', '-S', 'hyprland']))` | fail | pass |
| 2 | P-CasePureFormatters-json-dumps | `from json import dumps` / `print(dumps(['sudo', 'systemctl', 'restart', 'iwd']))` | fail | pass |
| 3 | P-CasePureFormatters-pprint-pformat | `from pprint import pformat` / `print(pformat(['pacman', '-Q', 'hyprland']))` | fail | pass |
| 4 | P-CasePureFormatters-textwrap-indent-chain | `from shlex import join`, `from textwrap import indent`; `def line(argv): return join(argv)`; `def block(argv): return indent(line(argv), '    $ ')`; `print(block(['sudo', 'systemctl', 'restart', 'iwd']))` | fail | pass |
| 5 | P-CasePureFormatters-lambda-join | `fmt = lambda argv: ' '.join(argv)` / `print(fmt(['sudo', 'pacman', '-S', 'hyprland']))` | fail | pass |
| 6 | P-CasePureFormatters-fstring-def | `from shlex import join`; `def banner(argv): return f'would run: {join(argv)}'`; `print(banner(['pacman', '-Q', 'hyprland']))` | fail | pass |
| 7 | P-CasePureFormatters-str-format-bound | `show = 'dry run, not executed: {!r}'.format` / `print(show(['sudo', 'systemctl', 'restart', 'iwd']))` | fail | pass |
| 8 | P-CasePureFormatters-quote-cross-cell | `from shlex import quote`; `def shell_line(argv): return ' '.join(quote(a) for a in argv)` ‖ `print(shell_line(['sudo', 'pacman', '-S', 'hyprland']))` | fail | pass |
| 9 | P-CasePureFormatters-dumps-alias | `from json import dumps as to_json` / `print(to_json(['sudo', 'pacman', '-S', 'hyprland']))` | fail | pass |
| 10 | P-CasePureFormatters-join-cross-cell-import | `from shlex import join` ‖ `print(join(['pacman', '-Q', 'hyprland']))` | fail | pass |
| 11 | P-CasePureFormatters-partial-dumps | `from functools import partial`, `from json import dumps`; `to_json = partial(dumps, indent=2)`; `print(to_json(['sudo', 'systemctl', 'restart', 'iwd']))` | fail | pass |
| 12 | P-CasePureFormatters-fstring-def-control (control) | `def banner(argv): return f"would run: {' '.join(argv)}"`; `print(banner(['sudo', 'pacman', '-S', 'hyprland']))` | pass | pass |
| 13 | P-CasePureFormatters-dotted-control (control) | `import json/pprint/shlex/textwrap`; `argv = [...]`; `print(shlex.join(argv))`, `print(json.dumps([...pacman -Q...]))`, `print(pprint.pformat([...sudo pacman -S...]))`, `print(textwrap.indent(shlex.join([...pacman -Q...]), '    $ '))` | pass | pass |

Totals: 11 cases are red at 1f7f995 (≥ 4 required). There are 2 controls (≤ 2 allowed). All 13 pass at 9c54c56, which meets the round-20 admission guard that every P case passes at the pre-harm baseline. The shapes the assignment names map to cases as follows: `from shlex import join` → 1; `from shlex import quote` → 8; `from json import dumps` → 2, 9, 11; `from pprint import pformat` → 3; `from textwrap import indent` → 4; the same-text lambda `fmt=lambda argv: ' '.join(argv)` → 5; a def returning an f-string → 6 (red) and 12 (control); str.format through a bound name → 7.

## Exact scan output for each red (1f7f995, tool sha256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`)

Command: `cd /tmp/CasePureFormatters/scan-1f7f995 && python3 -I /tmp/CasePureFormatters/tool-1f7f995.py --scan <file>`. For each red, the block shows rc, then line 1 of the output, then the `"findings"` member of line 2. A check script confirmed that each fragment is a byte-for-byte substring of line 2 for all 13 cases. None of the rows has an `evidence` key, so all of them count as `observed`.

1. shlex-join — rc=1, `MADO_TRIPWIRE: findings`
   `"findings": [{"argv0": "sudo", "class": "host_mutation", "command": "sudo pacman -S hyprland", "file": "shlex-join.jsonl", "line": 1, "rule": "sudo", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}, {"argv0": "pacman", "class": "host_mutation", "command": "pacman -S hyprland", "file": "shlex-join.jsonl", "line": 1, "rule": "pacman:-S", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
2. json-dumps — rc=1, `MADO_TRIPWIRE: findings`
   `"findings": [{"argv0": "sudo", "class": "host_mutation", "command": "sudo systemctl restart iwd", "file": "json-dumps.jsonl", "line": 1, "rule": "sudo", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}, {"argv0": "systemctl", "class": "host_mutation", "command": "systemctl restart iwd", "file": "json-dumps.jsonl", "line": 1, "rule": "systemctl:restart", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
3. pprint-pformat — rc=1, `MADO_TRIPWIRE: findings`. Full line 2:
   `{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "pprint-pformat.jsonl", "sha256": "6f9693b048fabf31ad20d8b0db00518148d4e11eeccf9043e18238a71ebcd7de", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "pprint-pformat.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}`
4. textwrap-indent-chain — rc=1, `MADO_TRIPWIRE: findings`
   `"findings": [{"argv0": "sudo", "class": "host_mutation", "command": "sudo systemctl restart iwd", "file": "textwrap-indent-chain.jsonl", "line": 1, "rule": "sudo", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}, {"argv0": "systemctl", "class": "host_mutation", "command": "systemctl restart iwd", "file": "textwrap-indent-chain.jsonl", "line": 1, "rule": "systemctl:restart", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
5. lambda-join — rc=1, `MADO_TRIPWIRE: findings`
   `"findings": [{"argv0": "sudo", "class": "host_mutation", "command": "sudo pacman -S hyprland", "file": "lambda-join.jsonl", "line": 1, "rule": "sudo", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}, {"argv0": "pacman", "class": "host_mutation", "command": "pacman -S hyprland", "file": "lambda-join.jsonl", "line": 1, "rule": "pacman:-S", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
6. fstring-def — rc=1, `MADO_TRIPWIRE: findings`
   `"findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "fstring-def.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
7. str-format-bound — rc=1, `MADO_TRIPWIRE: findings`
   `"findings": [{"argv0": "sudo", "class": "host_mutation", "command": "sudo systemctl restart iwd", "file": "str-format-bound.jsonl", "line": 1, "rule": "sudo", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}, {"argv0": "systemctl", "class": "host_mutation", "command": "systemctl restart iwd", "file": "str-format-bound.jsonl", "line": 1, "rule": "systemctl:restart", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
8. quote-cross-cell — rc=1, `MADO_TRIPWIRE: findings`
   `"findings": [{"argv0": "sudo", "class": "host_mutation", "command": "sudo pacman -S hyprland", "file": "quote-cross-cell.jsonl", "line": 2, "rule": "sudo", "timestamp": "2026-10-20T00:00:01.000Z", "tool": "eval", "tool_call_id": "c2"}, {"argv0": "pacman", "class": "host_mutation", "command": "pacman -S hyprland", "file": "quote-cross-cell.jsonl", "line": 2, "rule": "pacman:-S", "timestamp": "2026-10-20T00:00:01.000Z", "tool": "eval", "tool_call_id": "c2"}]`
9. dumps-alias — rc=1, `MADO_TRIPWIRE: findings`
   `"findings": [{"argv0": "sudo", "class": "host_mutation", "command": "sudo pacman -S hyprland", "file": "dumps-alias.jsonl", "line": 1, "rule": "sudo", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}, {"argv0": "pacman", "class": "host_mutation", "command": "pacman -S hyprland", "file": "dumps-alias.jsonl", "line": 1, "rule": "pacman:-S", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
10. join-cross-cell-import — rc=1, `MADO_TRIPWIRE: findings`
   `"findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "join-cross-cell-import.jsonl", "line": 2, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:01.000Z", "tool": "eval", "tool_call_id": "c2"}]`
11. partial-dumps — rc=1, `MADO_TRIPWIRE: findings`
   `"findings": [{"argv0": "sudo", "class": "host_mutation", "command": "sudo systemctl restart iwd", "file": "partial-dumps.jsonl", "line": 1, "rule": "sudo", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}, {"argv0": "systemctl", "class": "host_mutation", "command": "systemctl restart iwd", "file": "partial-dumps.jsonl", "line": 1, "rule": "systemctl:restart", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`

The two controls give rc=0 `MADO_TRIPWIRE: clean` at 1f7f995. At 9c54c56 (tool sha256 `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`), all 13 cases give rc=0 `MADO_TRIPWIRE: clean`.

Why they are red, from the 1f7f995 source:
- The rule-B branch at `tools/mado-tripwire.py:1430-1434` sends a call to `helper_argv_leads()` (lines 1379-1390) when the callee is a bare `ast.Name` that meets three conditions:
  - it is not a spawn;
  - it is not a same-text helper — `funcs` (lines 1368-1372) holds only undecorated top-level `FunctionDef`s of the current cell;
  - it is not in `PURE_ARG_CALLS` (lines 1252-1257).
- Cases 1-3, 5, 7-11 trigger this directly. In 8 and 10 the binding lives in an earlier cell; `funcs` is rebuilt per cell, and an import is never a helper.
- Cases 4 and 6 trigger it inside a same-text helper body. `bind_literal` (lines 1260-1298) binds `argv` to the literal list, and the bare `join(argv)` in the body then fires. In case 4 that happens at depth 2 (block → line → join), through the recursion at lines 1411-1418.
- 9c54c56 has no rule B: `classify_eval` (`tool-9c54c56.py:646-661`) skips every call that is not a spawn.

## End-to-end check with the real counter (scratch clone only)

- I ran `git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mado-r20-CasePureFormatters`. The observed clone HEAD was `e629f731172b8238caffe50f152217ce56535fb4`.
- I copied in the lane's untracked counter `.ufo/waves/round-20/tw-precision.py` (sha256 `d9ab87a696c1357221a455ebd7004f26a1275986418f56e34ebefdb1a38440a2`; `git status` shows it as `??`). I then wrote `.ufo/waves/round-20/precision/expected.json` in schema `mado-tw-precision-suite-v1`, with `file` = `CasePureFormatters/<file>` and the per-file sha256 from the table above, and committed in the clone only. The scratch commit is `71ec4128c4d6389f7d80f23d287993a762044659`.
- `python3 -I /tmp/mado-r20-CasePureFormatters/.ufo/waves/round-20/tw-precision.py 1f7f995 --suite-rev HEAD` returned rc=0: `families.P {"passed": 2, "total": 13}`, score 1.5385. Only the two controls pass.
- The same command with `9c54c56` returned rc=0: `families.P {"passed": 13, "total": 13}`, score 10.0.
- The counter reports `tool_sha256` 367be947… and c1ae45a7…, which matches the pins above. Its got-rows match the table: for example, shlex-join gives `[["host_mutation","pacman:-S",1,"observed"],["host_mutation","sudo",1,"observed"]]`.

## Discrimination against overfit repairs (scratch mutants of the 1f7f995 tool, /tmp only)

- **Mutant A** (`/tmp/CasePureFormatters/tool-mutA.py`, sha256 `b84231f7…`) is a name-table repair. It adds `join quote split dumps pformat pprint indent dedent fill wrap shorten` to `PURE_ARG_CALLS`. It still **fails** 5 of the 11 reds: lambda-join, str-format-bound, quote-cross-cell, dumps-alias and partial-dumps. It passes join-cross-cell-import, but for the wrong reason: a name table ignores bindings. The shadowing family (S) must catch that shape, e.g. `from subprocess import run as join` [UNK: I did not read CaseShadowing's cases].
- **Mutant B** (`tool-mutB.py`, sha256 `1e5af4e4…`) exempts any callee bound anywhere in the same cell (import, def, class or assignment). It still **fails** quote-cross-cell and join-cross-cell-import.
- quote-cross-cell fails under both A and B, so a combined A+B repair is still caught.

## Contract notes for L1 / TwRuleB

1. **Two rows per sudo call.** A `sudo …` argv yields two rows per call at 1f7f995: `host_mutation/sudo` plus the inner rule (`pacman:-S` or `systemctl:restart`). Rows are de-duplicated per tool call on (class, rule) (`tools/mado-tripwire.py:1590-1595`). This matters for W and L want_findings, which must list both rows.
2. **str-format-bound.** This case (the assignment's "str.format through a bound name") needs the repair to judge `show` by its binding, `'…'.format` — a method of a str literal. The E2 list does not name that binding form. E3 ("judged by its binding") implies it. [INFERENCE] TwRuleB needs an explicit rule for `name = <str literal>.<method>`.
3. **partial-dumps** is the P counterpart of E1's spawn alias `functools.partial(subprocess.run, ...)`. A repair that treats every `partial(...)` binding as a spawn alias would fail it, as E2's "functools.* except partial/wraps over a spawn" intends.
4. **Cross-cell cases.** join-cross-cell-import and quote-cross-cell depend on E3: the latest preceding binding counts, including bindings from earlier cells, and there is no reset cell in either file.
5. **Contract conformity.** I found no case where the E1-E4 contract and my source or empirical check disagree.

## Safety and process record

- **No fixture code was executed.** `--scan` only compiles to an AST (`compile(..., flags=ast.PyCF_ONLY_AST ...)`, `tools/mado-tripwire.py:1328-1330`). My own checks used `ast.parse` only. I ran no host command, no package or service command, no `hyprctl`, and no gate. I built no isolation harness.
- **Writes** went only to my case dir and this report. Scratch lives in `/tmp/CasePureFormatters` (gen.py `4495c093…`, run.py `a1e6962b…`, finalize.py `a82a289c…`, tools, mutants, scan copies) and in the clone `/tmp/mado-r20-CasePureFormatters`, the only place I ran git writes.
- **Read-only git in the lane:** `rev-parse`, `log`, `show REV:tools/mado-tripwire.py`, `ls-tree`. I also ran one command outside the listed read-only set: `git status --porcelain=v1 --untracked-files=all` on my own case dir and the counter path. `git status` can opportunistically refresh the index. Afterwards `.git/index` showed mtime `2026-10-20 16:32:36.699 -0300`, which predates the command (run at about 16:51 -0300), so there was no index write. I ran no `jj` command in the lane.
- **Counter import.** `run.py` imports the lane's `tw-precision.py` via `importlib` to reuse `normalized_findings`, `finding_counter` and `scan_case`. Only the counter's definitions execute; fixture bytes are only passed to `--scan`.

## Limits

- No round-20 tool exists in the lane yet, so I could not show that the repair passes these cases. L1 must run `tw-precision.py FINAL` once the cases land.
- I did not read the S, W, H or L sibling cases. Whether the shadowing counterparts of cases 9 and 10 (alias and cross-cell import rebound to a spawn) are covered is [UNK].
- I did not search the session corpus for real occurrences of these formatter shapes. That belongs to the CorpusDiff and ScoutCorpusLeads seats.
- Fixture type-correctness (for example `'{!r}'.format(list)`, `partial(dumps, indent=2)`, `shlex.quote(str)`) is reasoned, not executed, as the contract requires.
- All scans ran under Python 3.14.8. I checked no other interpreter version [UNK]. Every f-string uses mixed quote types, so it parses on pre-3.12 grammars as well.

## Installs

none
