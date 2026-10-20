# OracleR13R14 — independent oracle over rounds 13 and 14

Seat: MadoR17.OracleR13R14 (executor, leaf). Date 2026-10-20.
Deliverable written: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/evidence/oracle-r13-r14.json` (only assigned file).
Method used a throwaway scanner at `/tmp/oracle-r13-r14.py` (not part of the deliverable; the tripwire tool was never read or waited on).

## Scope and method

- Inputs, read-only: `.../MadoR13.jsonl`, all 32 `.../MadoR13/*.jsonl`, `.../MadoR14.jsonl`, all 32 `.../MadoR14/*.jsonl` — **66 files, 0 unreadable, 0 invalid JSON lines containing toolCalls**.
- Same token list as the round-15 oracle: `sudo doas pkexec pacman yay paru systemctl hyprctl pkill killall libinput evtest wayland-info journalctl loginctl expac checkupdates grim omarchy-` (word-boundary).
- Only assistant `message.content` items of `type:"toolCall"` scanned: `bash` → `arguments.command`; `eval` → `arguments.code` lines starting with `!`. **1,073 bash calls; 0 eval `!`-lines** across both rounds.
- Per hit: file basename, 1-based line, toolCall id, timestamp, tool, command (truncated 240 chars, `[A-Za-z0-9_-]{32,}` runs redacted), manual class + reason.
- Manual classes per the round-15 rubric: `host_mutation` / `package_query` / `live_probe` / `clean-data-mention`. Parsing split on `; && || | &`, stripped wrappers and assignments, recursed into `$(...)`/backticks/`sh -c`/`eval`, stripped heredoc bodies, and additionally flagged probe tools spawned via `subprocess`/`os.system` inside inline python.

## Totals

| class | hits |
|---|---|
| host_mutation | 3 |
| package_query | 55 |
| live_probe | 10 |
| clean-data-mention | 38 |
| **total hits** | **108** |

## host_mutation (3)

1. `MadoR13/MadoR13.GlobalCapture.jsonl:19`, bash, `2026-10-20T04:06:49Z`, `call_2a68aff4b6984128b91f75d2` — `sudo pacman -S --needed --noconfirm wayland-utils` (install) plus `wayland-info --version` and `pacman -Q` in the same call.
2. `MadoR14/MadoR14.OutputSpec.jsonl:65`, bash, `2026-10-20T05:45:52Z` — `sudo pacman -S --needed --noconfirm wlr-protocols` (install) among sibling `pacman -Q/-Ss/-Ql/-Qi` query calls.
3. `MadoR14/MadoR14.ReviewSourceBar.jsonl:41`, bash, `2026-10-20T05:41:25Z` — `sudo pacman -Sw --noconfirm wlr-protocols` (download-only into `/var/cache/pacman/pkg`, then `bsdtar -xOf` inspection).

## package_query (55)

All `pacman -Q/-Qi/-Ql/-Qo/-Qs/-Ss/-Si` queries across 20 files (e.g. `MadoR14.EvidenceChain.jsonl:61` ×6, `MadoR14.OutputSpec.jsonl:65` ×5, `MadoR13.AttackCoverage.jsonl`, `MadoR13.GlobalCapture.jsonl`, `MadoR14.SourceInventory/Safety`, `MadoR14.jsonl:134`). No `-S`/`-Sy`/`-U`/`-R`/`-D` transaction verbs among them; none is a mutation.

## live_probe (10)

Round-13 only: real `wayland-info` executions (capture to `/tmp` scratch), `hyprctl version`/`-j version` queries, and inline-python `subprocess.run(['hyprctl',...])` calls in `MadoR13.GlobalCapture`/`EvidenceChain`. No round-14 probe execution; `command -v`/`man`/grep-pattern mentions were classed clean-data.

## Disclosure check (the assigned extra)

- **Disclosed:** both round-14 mutations — `round-14.md` lines 111–115 name the `wlr-protocols` install and the `-Sw` download explicitly.
- **Undisclosed in the lesson:** `MadoR13.GlobalCapture.jsonl:19` `sudo pacman -S wayland-utils` is **not** in `corpus/lessons/round-13.md` (no tooling section; grep finds no `pacman -S`/`sudo`/`install` disclosure). It **is** disclosed in `corpus/lessons/round-13-verifier-spotcheck.md` line 211. Flagged as the one lesson-level gap.
- **Not individually disclosed:** the 55 package_query hits — `round-14.md:116` claims "no installs/updates" for other seats but never enumerates queries; none implies a transaction.
- Out-of-token observation: `MadoR14.Safety.jsonl:62` ran `jj --ignore-working-copy op log` in-lane (flag present — safe); the disclosed R14 low-severity incident was AttackCoverage's `jj log` *without* the flag (round-14.md:126–130).

## Residual limits

Token list is fixed; a shell command touching host state without a listed token (e.g. bare `kill`, `rm`, `tee` into system paths, `jj`/`git` mutations) is out of scope by design — noted, not classified. Heredoc/quoting handled but exotic quoting could still evade; eval `!`-lines were absent, so eval coverage is unexercised. `pacman -Sw` is classified host_mutation per the shared rule table (it writes the package cache), though the lesson treats it as download-only.

No tools installed or updated this wave. No pacman/sudo/probe commands were run by this seat; transcripts were read as file bytes only.
