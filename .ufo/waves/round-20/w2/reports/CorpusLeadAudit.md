# CorpusLeadAudit — partly falsified: 22 of 25 leads are mis-marked visible helpers

## Findings

### Medium — 22 `lead` tags hide visible helper bodies

I cloned the lane to `/tmp/mado-r20w2-CorpusLeadAudit` (HEAD `a4046a8216080d4004de3f268c62cf142095ac07`) and ran the cloned tripwire over the session root:

```text
python3 -I /tmp/mado-r20w2-CorpusLeadAudit/tools/mado-tripwire.py --scan /home/vgpnk/.omp/agent/sessions/-Projects-shokunin
MADO_TRIPWIRE: findings
scan_exit=1; files=6078; findings=8363; observed_findings=8338; lead_findings=25
```

Exit 1 is the findings verdict, not `could_not_evaluate`. The scanned tool SHA-256 is `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`; the full scan output (`/tmp/mado-r20w2-CorpusLeadAudit/session-scan-final.txt`, 5,813,892 bytes) SHA-256 is `b9d55c7126d83b0e2fda2dd905be6edee241573cda60a94a274ed71343397d27`.

I inspected all 25 lead rows and matched each to its exact tool-call ID in the same transcript. Twenty-two are mis-marked: one cross-cell `run_record` in MadoR13 and 21 same-cell `run` calls in the Tameshi transcript. In both cases the visible helper body calls `subprocess.run(argv, ...)`, so these are observed spawn paths, not opaque callees or data-only leads. The implementation advertises visible-helper recursion at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1810-1847`; unresolved/deleted names instead enter `helper_argv_leads` at `:1872-1878`. The visible cases below nevertheless receive `evidence: lead`.

| # | Transcript path:line | Lead command | Verdict |
|---:|---|---|---|
| 1 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR13.jsonl:470` | `pacman -Q wayland-utils wayland wayland-protocols hyprland` | **MIS-MARKED** — `run_record` is defined in the earlier eval cell at `:437`; its body calls `subprocess.run(args, ...)`. The caller is at `:470`; recorded result at `:472` says `packages exit 0 expected 0`. |
| 2 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:60` | `git add -A` | **MIS-MARKED** — same-cell `run(argv, ...)` body calls `subprocess.run(argv, ...)`; tool result at `:62` records this command with exit 0. |
| 3 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:60` | `git commit -qm initial pin` | **MIS-MARKED** — same visible wrapper; tool result at `:62` records the command with exit 0. |
| 4 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:60` | `jj log --no-graph -r all() -T commit_id.short() ++ " " ++ bookmarks ++ "\\n"` | **MIS-MARKED** — same visible wrapper; the recorded result at `:62` includes the `jj log` invocation and output. |
| 5 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:81` | `git add -A` | **MIS-MARKED** — same-cell `run(argv, ...)` delegates to `subprocess.run(argv, ...)`; tool result at `:83` records this command with exit 0. |
| 6 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:81` | `git commit -qm initial pin` | **MIS-MARKED** — same visible wrapper; tool result at `:83` records the command with exit 0. |
| 7 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:81` | `jj log --no-graph -r all() -T commit_id.short() ++ " " ++ bookmarks ++ "\\n"` | **MIS-MARKED** — same visible wrapper; the recorded result at `:83` includes the `jj log` invocation and output. |
| 8 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:87` | `git add -A` | **MIS-MARKED** — same-cell `run(argv, ...)` delegates to `subprocess.run(argv, ...)`; tool result at `:89` records this command with exit 0. |
| 9 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:87` | `git commit -qm pin` | **MIS-MARKED** — same visible wrapper; tool result at `:89` records the command with exit 0. |
| 10 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:87` | `jj log --no-graph -r all() -T commit_id.short() ++ " " ++ bookmarks ++ "\\n"` | **MIS-MARKED** — same visible wrapper; the recorded result at `:89` includes the `jj log` invocation and output. |
| 11 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:93` | `git add -A` | **MIS-MARKED** — same-cell `run(argv, ...)` delegates to `subprocess.run(argv, ...)`; tool result at `:95` records this command with exit 0. |
| 12 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:93` | `git commit -qm pin` | **MIS-MARKED** — same visible wrapper; tool result at `:95` records the command with exit 0. |
| 13 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:93` | `jj file track -- tools/pinned-tool.py` | **MIS-MARKED** — same visible wrapper; tool result at `:95` records the `jj` invocation. |
| 14 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:93` | `jj diff --summary` | **MIS-MARKED** — same visible wrapper; tool result at `:95` records the `jj` invocation. |
| 15 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:93` | `jj metaedit --update-author` | **MIS-MARKED** — same visible wrapper; tool result at `:95` records the `jj` invocation. |
| 16 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:93` | `jj commit -m waived move` | **MIS-MARKED** — same visible wrapper; tool result at `:95` records the `jj` invocation. |
| 17 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:93` | `jj log --no-graph -r @- -T commit_id` | **MIS-MARKED** — same visible wrapper; tool result at `:95` records the `jj log` invocation. |
| 18 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:96` | `git add -A` | **MIS-MARKED** — same-cell `run(argv, ...)` delegates to `subprocess.run(argv, ...)`; tool result at `:98` records this command with exit 0. |
| 19 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:96` | `git commit -qm pin` | **MIS-MARKED** — same visible wrapper; tool result at `:98` records the command with exit 0. |
| 20 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:96` | `jj log --no-graph -r all() -T commit_id.short() ++ " " ++ bookmarks ++ "\\n"` | **MIS-MARKED** — same visible wrapper; tool result at `:98` records the `jj log` invocation. |
| 21 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:96` | `jj file track -- tools/pinned-tool.py` | **MIS-MARKED** — same visible wrapper; tool result at `:98` records the `jj` invocation. |
| 22 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:96` | `jj commit -m waived tool change` | **MIS-MARKED** — same visible wrapper; tool result at `:98` records the `jj` invocation. |
| 23 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.AtkCasesS.jsonl:129` | `pacman -Q hyprland` | **VALID LEAD** — the embedded test defines `run(argv)` then deletes it before calling `run(...)`; there is no callable binding at the call site. Tool result at `:132` says `NameError: name 'run' is not defined`. |
| 24 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ReopenExecModel.jsonl:63` | `pacman -Q hyprland` | **VALID LEAD** — `run(...)` precedes the later `def run(a): pass`; no earlier binding/import exists in this transcript. The tool result at `:69` fails earlier with `UnboundLocalError`, so the test never reaches this call. |
| 25 | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ReopenExecModel.jsonl:70` | `pacman -Q hyprland` | **VALID LEAD** — `run(...)` precedes the later `def run(a): pass`; no earlier binding/import exists. Tool result at `:73` explicitly says `call_before_def: NameError name 'run' is not defined`. |

There are no pure-data-only leads in this set: every row is attached to a call expression with a literal argv. The three valid rows are unresolved/deleted-name probes, not bare command data; none is reported as an observed spawn. The 22 mislabeled rows are genuine visible spawn paths, with recorded successful invocations.

Input SHA-256s recorded by the final full scan: `MadoR13.jsonl` `21126251c6154d5c97194a7a155abf2be33ae958506ba3f0383b92a1b6c59615`; `MadoR20.AtkCasesS.jsonl` `0807767a25609efc2b3619690b9a6fc2999893f785cb80707c3d01a629dc5b00`; `MadoR20.ReopenExecModel.jsonl` `2a72493d33e90600e9c4ebb8f27ce659dce12e3f8f004dd64d99e69e2945fe3f`; `TameshiR18.X06DispositionGuards.jsonl` `e22cbf2ca421db8e524cd42802782d2d3e7c6d77b4134192097c83af86d7baf0`.

## Limits

- Session files were parsed as data only; no transcript code was executed or followed. The full root is live, not an atomic snapshot: the census grew from 5,978 files/24 leads to 6,078 files/25 leads. `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.AtkCasesS.jsonl` grew after the final full scan; a subsequent targeted scan of that file (218 lines, SHA-256 `417bfeee2e2f4dde3d7a59f896c701a260584a98d32907e3d9fa4e2d36676ce8`) still returned only the same lead at `:129`. I did not run another full-root scan after that append, so later changes elsewhere remain [UNK].
- LSP is unavailable: attempting `read xd://lsp` returned “No such tool” and listed no LSP route. No LSP references/definitions/diagnostics were available; text search was not used as semantic proof.
- The tripwire output exit code 1 is its `findings` verdict. I did not run unrelated suites, build, or lint checks.

## Installs

none
