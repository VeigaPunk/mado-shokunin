# SchemaVariants — OMP transcript schema census for tripwire coverage

Seat: `MadoR17.SchemaVariants` (executor, leaf). Read-only survey of
`/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR1[3-6]/*.jsonl`.
Full counts and redacted examples: `.ufo/waves/round-17/evidence/schema-variants.json`
(`mado-r17-schema-variants-v1`). No installs; python3 stdlib only; no
pacman/sudo/probes run (host pause respected — every count below is from
file-byte parsing).

## Corpus

| Dir | files | Total lines | invalid JSON |
|---|---|---|---|
| MadoR13 | 32 | | |
| MadoR14 | 32 | | |
| MadoR15 | 64 | | |
| MadoR16 | 96 | | |
| **all** | **224** | **26975** | **0** |

## Line-type census

`type` field: message 15188, custom 9972, model_change 485, session_init 264,
title 224, session 224, thinking_level_change 224, credential_pin 213,
custom_message 181. No other types, no blanks, no invalid JSON.

- `custom` → `tool_execution_start` 9507, `system-prompt-digest` 238,
  `session_exit` 227.
- `custom_message` → `irc:incoming` 148, `async-result` 30,
  `eval-state-context` 1, `gemini-tool-call-reminder` 1,
  `thinking-loop-redirect` 1.

## Message roles and content items

Roles: toolResult 9431, assistant 5485, user 272. Content items:
toolResult/text 9434 (3 multi-text results), assistant/thinking 4484,
assistant/toolCall 9431, assistant/text 727, user/text-items 225,
**user bare-string content 47** (see V4). `toolCall` appears only in
assistant messages; never in user or toolResult lines.

## toolCall name inventory (complete)

| name | count |
|---|---|
| read | 3582 |
| bash | 2841 |
| grep | 1266 |
| edit | 632 |
| glob | 535 |
| write | 394 |
| eval | 148 |
| web_search | 30 |
| wait | 3 |

**No other shell-executing tool exists in this corpus**: no `task`, `spawn`,
`ssh`, `browser`, or service-start tool calls. `write`/`edit` paths are
filesystem paths or `agent://<seat>` peer messages (≥4 agent:// writes,
messaging not execution); **no `xd://` writes observed**. `arguments` is
always a dict (0 string-encoded, 0 missing key).

## Variants that could hide or fake issued commands

- **V1 eval→subprocess→`bash -c <recipe>`: 2 calls.** Both in
  `MadoR14/MadoR14.SourceSafety.jsonl` (lines 152 `toolu_01DtvHZ7…`,
  155 `toolu_01GGG3mR…`). recipe2 contains a literal `pacman -Q hyprland`.
  A toolCall parser keyed on `name==bash` or `eval` code starting with `!`
  misses both. This is the only real hidden-shell channel found.
- **V2 eval→subprocess→direct argv: 29 calls** across 14 files; argv0s seen:
  git 19, sed 3, sha256sum 1, bash 2, `-c` 1. **None are
  sudo/pacman/yay/systemctl/hyprctl argv0s** — but the pattern means eval
  `code` must be scanned for `subprocess.*([...])` argv lists, not only `!`.
- **V3 command text in non-executing fields: 623 arg blobs** matched the
  suspicious-token regex — grep patterns (`"pattern": "…hyprctl reload|…"`),
  write/edit content, web_search queries. These are data; a raw-line regex
  would false-positive on them. Field-scoped parsing is required.
- **V4 user `content` as bare string: 47 messages** (`[Wait interrupted by
  message] <irc …>` interrupts). Iterating `content` as a list over a str
  yields 22901 phantom char-items; must type-check first.
- **V5 `tool_execution_start` duplicate channel: 9507 rows, 1:1 with
  toolCall ids.** Every bash (2841) and eval (148) call has a twin —
  including the red anchor `call_38165` (`MadoR15.LibinputEvents.jsonl`
  line 54 toolCall ↔ line 55 te_start, both carry
  `sudo pacman -S --needed --noconfirm libinput libinput-tools`). Scanning
  both channels double-counts; scanning te_start alone loses args on 338
  rows (all 148 eval te_starts carry no `data.args`).
- **V6 te_start name relabeling: 77 id-matched rows** where
  `tool_execution_start.data.toolName` ≠ `toolCall.name` (76 edit→write,
  1 edit→read). Name on the custom line is unreliable; join by id only.
- **V7 toolCall id formats: 6 shapes** — `toolu_*` 4167, `call_N` 4076,
  `N_tool_<hex>` 1039 (parallel-indexed), `<name>:<n>#<hex>` 132 (e.g.
  `bash:0#219afd2`), `chatcmpl-tool-*` 17, `0_tool_*` 826. Finding records
  must treat id as opaque.
- **bash arg keysets**: all 2841 have `command`; extras are `i`/`cwd`/
  `timeout`/`async`/`name`/`pty`/`ready` — 6 calls use async+pty+ready
  (service launches, e.g. `git rev-parse` checks). `command` is always
  present and non-empty (0 missing).
- **eval**: 148 calls, all `language:"py"`, **zero `!` shell-magic**, zero
  `os.system`/`os.popen`; 23 do `urllib.request.urlopen` network fetches
  (documentary, not shell).

## Absent variants (checked, zero)

`eval` `!`-lines, `eval language:"js"`, `os.system`/`commands.getoutput`,
string-encoded `arguments`, `toolCall` outside assistant role, `toolCall`
missing `arguments`, te_start without matching toolCall (0), toolCall
without te_start (0), unknown toolCall names, invalid JSON lines.

## Implication for `tools/mado-tripwire.py`

The planned input shape
(`message/assistant/toolCall` + `name=="bash"`/`arguments.command`, plus
`eval` `code` `!`-prefix) covers the red anchor and every `bash` call in
this corpus. The one gap is **V1/V2: eval `code` spawning
`subprocess.run(["bash","-c",…])` or argv lists** — real in R14–R16 data
(2 bash-c shells, 29 subprocess users). A second-order doc-scan rule
(flag `eval` code containing `subprocess` + `bash|sh|-c|sudo|pacman`
literals) would catch it post-hoc; it is safe to add as a finding class
rather than extending the shlex segmenter into Python. V3 (arg-text),
V4 (bare-str user), V5/V6 (custom-line duplicate, name relabel) all argue
for strict field scoping and id-only joins — already aligned with the
shared interface, which ignores `custom`/`toolResult` lines.

## Host-pause and tool records

No tool installs this task; python3 (stdlib json/re/glob) only. All reads
were file bytes of the session transcripts; no pacman/sudo/systemctl/
hyprctl or live probes issued. Host versions remain [UNK].

## SHONEN

- `[~]` surveyed all 224 `MadoR1[3-6]` JSONL files (26975 lines, 0 invalid)
  — evidence: `schema-variants.json` totals.
- `[~]` toolCall names are exactly the 9 listed; bash/eval are the only
  exec channels — evidence: `toolCall_names`, `other_shell_executing_tools`.
- `[~]` two eval→`subprocess bash -c` hidden-shell calls exist
  (MadoR14.SourceSafety L152/L155) — evidence: V1 examples.
- `[~]` red anchor `call_38165` is reachable by a plain toolCall-only
  parser — evidence: `red_anchor_check`.
