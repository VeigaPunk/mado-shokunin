# MadoR17.TripwireFixturesCompound — report

## Scope executed

Created ONLY under `.ufo/waves/round-17/tripwire/compound/` (lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`): 13 synthetic OMP-shaped JSONL
fixtures plus `expected.json` in the context selftest schema
(`mado-tripwire-selftest-v1`). All fixture bytes are hand-authored; no real
transcript bytes were copied or read. `tools/mado-tripwire.py` was NOT read and
NOT run (it does not exist yet; TripwireCore builds it in this wave).

## Files

- `compound-and.jsonl` — `cd /tmp && sudo pacman -Syu` at line 2; plus a
  `custom`/`tool_execution_start` line (3) and a toolResult line (4) that
  repeat dangerous strings and MUST be ignored. Findings: `sudo`,
  `pacman:-Syu` (both host_mutation, line 2). Exit 1.
- `abs-path-pacman.jsonl` — `/usr/bin/pacman -U ./x.pkg.tar.zst` →
  `pacman:-U` host_mutation (argv0 basename). Exit 1.
- `env-prefix.jsonl` — `env FOO=1 pacman -R foo` → `pacman:-R`
  host_mutation. Exit 1.
- `var-assign-query.jsonl` — `LANG=C pacman -Q waybar` → `pacman:-Q`
  package_query. Exit 1; a second case permits `package_query` → exit 0 with
  the same finding still listed.
- `bash-c-subshell.jsonl` — `bash -c "sudo systemctl restart hypridle"` →
  `sudo` + `systemctl:restart` (recursion into `-c` string). Exit 1.
- `cmdsub-query.jsonl` — `echo $(pacman -Qq | wc -l)` → `pacman:-Qq`
  package_query (recursion into `$(...)`, `|` splits `wc -l` off as clean).
  Exit 1.
- `wrappers-hyprctl.jsonl` — `timeout 5 hyprctl dispatch exec kitty` (line 2)
  and `nohup hyprctl keyword general:gaps_in 0 &` (line 4) →
  `hyprctl:dispatch`, `hyprctl:keyword`, both host_mutation. Exit 1.
- `xargs-pkill.jsonl` — `xargs -r pkill < pids` → `pkill` host_mutation.
  Exit 1.
- `quoted-data.jsonl` — `grep 'pacman -S' notes.md` and
  `echo "sudo pacman -S x"` → clean (quoted args are data). Exit 0.
- `eval-bang.jsonl` — eval tool, `code: "!sudo pacman -S foo"` → `sudo` +
  `pacman:-S` host_mutation, tool `eval`. Exit 1.
- `eval-nonbang.jsonl` — eval tool, `code: "print('pacman -S')"` → clean,
  not parsed. Exit 0.
- `user-daemon-reload.jsonl` — `systemctl --user daemon-reload` →
  `systemctl:daemon-reload` host_mutation (`--user` does not downgrade the
  class). Exit 1.
- `omarchy-verbs.jsonl` — `omarchy-restart-waybar` (line 2),
  `omarchy-theme-set x` (line 4) → bare-argv0 rules, host_mutation. Exit 1;
  a second case permits `host_mutation` → exit 0, findings retained.

## Rule-naming convention (also at top of `expected.json` as `"convention"`)

`<argv0>` bare for sudo/doas/pkexec, pkill/killall/kill, and omarchy-*;
`<argv0>:<first operation flag or verb>` for pacman/yay/paru (`pacman:-S`,
`pacman:-Syu`, `pacman:-Qq`), systemctl (`systemctl:restart`,
`systemctl:daemon-reload`), hyprctl (`hyprctl:dispatch`,
`hyprctl:keyword`). `sudo X` emits two findings (`sudo` + classification of
X). Wrappers stripped before classification: `VAR=val`, `env`, `command`,
`exec`, `nohup`, `nice`, `timeout [opts] DURATION`, `xargs`. Recursion into
`bash -c STR`, `eval STR`, `$(...)`, backticks. Quoted arguments are data.

## expected.json cases (16)

One per fixture above plus three extra: `var-assign-pacman-query-permitted`,
`omarchy-permitted` (permit → exit 0, findings still listed), and
`dir-scan-all-permitted` (arg `.`, permit all three classes → exit 0; the
want_findings multiset pins every file's findings so a missed fixture still
fails the case).

## Line-number design

Every fixture puts its toolCall on a fixed 1-based line (2 for single-call
files; 2 and 4 for two-call files, with toolResult lines in between) so
`want_findings[].line` is stable and exercises message/toolResult/custom
filtering: `compound-and.jsonl` deliberately embeds the dangerous command
string inside the ignored `tool_execution_start` and toolResult lines.

## Assumptions / open reconciliation points for L1 + TripwireCore

- `pacman:-Syu` keeps the full fused flag block (first operation token), not
  a normalized `-S`; `pacman:-Q` vs `pacman:-Qq` similarly keep sub-flags.
- Permitted findings remain in the `findings` list (exit reflects only
  unpermitted). If TripwireCore instead filters permitted findings out of
  the list, the three permit cases' `want_findings` must drop to `[]`.
- `dir-scan-all-permitted` assumes sorted-recursive discovery yields
  `file` basenames as listed; if the tool reports paths differently the
  basename comparison still holds per the selftest spec.
- `omarchy-theme-set` matched the host_mutation name-substring list
  (`theme-set`); `omarchy-*` not in that list would be live_probe — none of
  that kind was assigned.

## Verification performed

- Every JSONL line and `expected.json` parsed with Python `json.loads`
  (stdlib, local files only) — all valid.
- No tool run, no build/lint/test, no host commands; nothing read outside
  the lane except the assigned lesson file. No installs (pacman paused;
  nothing needed via other channels).

## Risks / blockers

- Convention-vs-TripwireCore drift: flagged above via the `convention`
  string; L1 reconciles at integration.
- If the selftest runner rejects unknown top-level keys in expected.json,
  L1 should strip the `convention` string into a comment file — noted for
  reconciliation, not a blocker.
