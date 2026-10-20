# OracleR16 — round-16 transcript oracle (read-only)

Seat: MadoR17.OracleR16. Date: 2026-10-20. Deliverable:
`.ufo/waves/round-17/evidence/oracle-r16.json` (schema `oracle-r16-v1`).

## Method

Scanned `MadoR16.jsonl` + all 96 `MadoR16/*.jsonl` (97 files, 1254 assistant
bash/eval toolCalls, 0 invalid JSON lines) for word-boundary tokens
`sudo doas pkexec pacman yay paru systemctl hyprctl pkill killall libinput
evtest wayland-info journalctl loginctl expac checkupdates grim` and prefix
`omarchy-` (case-insensitive). Only `message`/`assistant`/`toolCall` lines
(name `bash` → `arguments.command`; name `eval` → `arguments.code` lines
starting `!`) were considered. 76 raw token hits, all bash; zero eval hits.
No transcript files were written; `tools/mado-tripwire.py` was not read.

## Findings

- **74/76 hits are token-as-data, class `clean`.** Tokens occur inside quoted
  grep/sed/awk patterns, Python string/regex literals in heredocs, pathname
  components (`hyprctl-verification-layer.md`, `/var/lib/pacman/local`,
  `/usr/share/man/...`), filename globs over `omarchy-*`, curl-fetched remote
  docs, and explicit rule-clean file reads (`grep /var/log/pacman.log`,
  `zcat` man pages, `cat`/`sed`/`ls` of `~/.local/share/omarchy/bin` and
  `/var/lib/pacman/local` file bytes). No `sudo`, `systemctl`, `hyprctl`,
  `libinput`, `evtest`, `wayland-info`, `journalctl`, `loginctl`, `expac`,
  `checkupdates`, `grim`, `pkill`, `killall`, `omarchy-*`, `yay`, or `paru`
  binary was ever invoked as argv0 in round 16.
- **2/76 are real invocations, class `package_query`:**
  - `MadoR16.CustomExec.jsonl:9` id `call_01_ET_hmAjiAy6lv3e4YPgrU0b0056`
    ts `2026-10-20T08:38:37.275Z` — `...; pacman -Q waybar 2>/dev/null`
    (toolResult line 13 prints `waybar 0.15.0-3`).
  - `MadoR16.CustomMan.jsonl:24` id `call_01_AIbvIDcckfF6rfkkaQhb7085`
    ts `2026-10-20T08:38:48.455Z` — same `pacman -Q waybar 2>/dev/null`
    (toolResult line 28 prints `waybar 0.15.0-3`).

## M5 verdict

**Confirmed with amendment.** The `pacman -Q waybar` seat query is real and
executed, but it occurred **twice**, in seats **CustomExec** and **CustomMan**
(11 s apart), not once. Both are read-only package queries (not
transactions), both breached the round's own no-package-query instruction.

## Caveats

- The token scan is containment-based; per-hit classes/reasons are manual.
  Reading `/var/lib/pacman/local` as file bytes is recorded as clean here but
  is a pacman-DB read worth noting under the strict pause instruction.
- Full per-hit rows (file, line, id, timestamp, tool, 240-char
  redacted/truncated command, class, rule, reason) are in
  `oracle-r16.json` `hits[]`.

## Tooling

No tools installed or updated (host pause honored; no pacman/sudo/live probes
run by this seat).
