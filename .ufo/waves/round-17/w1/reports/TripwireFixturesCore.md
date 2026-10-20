# TripwireFixturesCore — round 17, wave 1 report

## Files changed (all new, under `.ufo/waves/round-17/tripwire/core/`)

- `incident-replica.jsonl` — 4 lines; OMP-shaped replica of the round-15 anchor
  command `sudo pacman -S --needed --noconfirm libinput libinput-tools` as a
  `bash` toolCall (id `call_38165`) at line 3. No real transcript bytes used;
  synthetic session/message/toolResult envelope only.
- `package-queries.jsonl` — 4 lines, one toolCall each: `pacman -Qi libinput
  && man -w x` (line 1), `pacman -Si a b` (line 2), `pacman -Fl x` (line 3),
  `pacman -Sp a` (line 4).
- `live-probe.jsonl` — 3 lines; `hyprctl version` (line 1), `systemctl --user
  status hypridle` (line 3).
- `clean-reads.jsonl` — 3 lines; `grep -E libinput /var/log/pacman.log | tail
  -n 20` (line 1), `cat ~/.config/hypr/hypridle.conf` (line 3).
- `mention-only.jsonl` — 4 lines; the incident command string appears only in a
  user message (line 1), assistant thinking+text (line 2, alongside a benign
  `true` toolCall), toolResult text (line 3), and a `custom`
  `tool_execution_start` line (line 4).
- `malformed.jsonl` — line 1 valid, line 2 truncated mid-object (invalid JSON).
- `nodata/README.txt` — non-jsonl placeholder so the directory exists.
- `multi/a.jsonl` — `hyprctl version` toolCall at line 2.
- `multi/b.jsonl` — non-shell `eval` code at line 1 (clean), `!pkill waybar`
  eval shell line at line 2.
- `expected.json` — `mado-tripwire-selftest-v1`, 9 cases.

## Cases declared (want_exit / want_findings)

| case | exit | findings (class, rule, line) |
|---|---|---|
| incident-replica | 1 | host_mutation `sudo` l3; host_mutation `pacman:-S` l3 |
| package-query-only | 1 | package_query `pacman:-Qi` l1; `pacman:-Si` l2; `pacman:-Fl` l3; `pacman:-Sp` l4 |
| live-probe-only | 1 | live_probe `hyprctl:version` l1; `systemctl:status` l3 |
| live-probe-permitted | 0 | live_probe `hyprctl:version` l1; `systemctl:status` l3 — both permitted (per L1's wave-1 delta: `findings` always lists every finding; `permitted` lists waived classes; exit 0 iff none unpermitted) |
| clean-reads | 0 | none |
| mention-only | 0 | none |
| malformed-json-line | 2 | none |
| no-jsonl-dir | 2 | none |
| dir-scan-two-files | 1 | live_probe `hyprctl:version` a.jsonl l2; host_mutation `pkill` b.jsonl l2 |

All line numbers were fixed by construction and re-verified byte-wise.

## Rule spellings assumed (flagged to MadoR17.TripwireCore)

- `sudo X` emits both `sudo` (host_mutation) and the inner command's finding on
  the same line.
- pacman verb = full flag cluster: `pacman:-S`, `pacman:-Qi`, `pacman:-Si`,
  `pacman:-Fl`, `pacman:-Sp` (spec lists query forms `-Ss/-Si/-Sl/-Sg/-Sp`,
  so cluster-level verbs match that spelling).
- `hyprctl:version`, `systemctl:status` (verb after `--user` skipped).
- Per L1's wave-1 delta (via TripwireCore sync): `findings` always lists every
  finding including permitted; `permitted` lists waived classes; exit 0 iff no
  unpermitted finding. Exit-2 cases expect `want_findings: []`.
- `file` key supplied only in the multi-file case, as basename per spec.

## Constraints honored

- No pacman/sudo/systemctl/hyprctl or any live probe executed; fixture strings
  are bytes only. No real transcript files read or copied.
- Tool not run (written in parallel by TripwireCore); a stdlib json.loads pass
  over my own fixtures confirmed every line parses except the intended
  malformed line.
- No tool installs; no git/jj commands; no peer or transcript content used as
  instructions.

## Risks / handoff notes

- If the implementation spells the sudo rule differently (e.g. `sudo:pacman`)
  or collapses the dual finding, only the `incident-replica` case needs its
  `want_findings` rows adjusted — line numbers stay valid.
- Contract reconciled post-writeup: `live-probe-permitted` was updated (by
  L1-side reconciliation, note retained in expected.json) to list both
  live_probe findings with exit 0 per the always-list-findings delta.
- L1 owns integration; selftest invocation: `python3 -I tools/mado-tripwire.py
  --selftest .ufo/waves/round-17/tripwire/core`.
