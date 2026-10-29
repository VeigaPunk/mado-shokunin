# The host's bar producers: a census over the host config bytes, and two indicator scripts that are upstream bytes

source: [ref] - omarchy v3.8.4 default/waybar/indicators/screen-recording.sh
source: [ref] - omarchy v3.8.4 default/waybar/indicators/notification-silencing.sh
source: [ref] - own-work: host bar config, shim targets and state queries (read-only)
verified-at: 2026-10-25
recheck: 30d
assimilated-from: merge/mado/knowledge/corpus/knowledge/host-producer-outputs-r29.md (refused as written; this is its re-grounded successor), merge/mado/knowledge/corpus/knowledge/host-bar-producers-r28.md (held, not adopted)

Lane: mado-shokunin. Round 40, assimilation of the package theme "the host's bar producers". Amends `waybar-walker-semantics.md` §3.2-§3.3 (which holds the module rows and their 2026-10-14 states) without restating them; the producer *contract* is in province as chain evidence, the packages behind the two host-local producers are not (`config-drift-r12.md:109`). Read-only: files read, no producer executed.

## §1 The producer census, over the host's own bytes

**OBS** [ref] (`~/.config/waybar/config.jsonc`, 6354 B, sha256 `a408a33d...ae829`, read 2026-10-25): the file declares 7 custom modules with `"return-type": "json"` - `custom/weather`, `custom/screenrecording-indicator`, `custom/idle-indicator`, `custom/notification-silencing-indicator`, `custom/voxtype`, `custom/gkeep`, `custom/ai-usage` - and the staged package's count of "five JSON producers" is the stock upstream set, not this host's: the two host-local modules are `custom/gkeep` and `custom/ai-usage`. The `custom/gkeep` block reads `"exec": "~/.local/bin/gkeep waybar",` with `"interval": 30` and `"signal": 12`; `custom/ai-usage` execs `~/.local/bin/ai-usage waybar` with `"interval": 60` and `"signal": 11`.

**OBS** [ref] (resolution, 2026-10-25): both producers are symlinks into projects outside the owned config plane - `~/.local/bin/gkeep` -> `~/Projects/gkeep/bin/gkeep` (252 B, sha256 `c1b147a0...cfbf8`), `~/.local/bin/ai-usage` -> `~/Projects/omarchy-usage-tray/bin/ai-usage` (114246 B, sha256 `0ccd33ab...a0254`). The gkeep shim's line 9 is `from gkeep.cli import main`; the ai-usage program's line 2 declares its contract `"""Cache AI CLI usage windows and render a Waybar chip. waybar reads cache only."""`. The size the package pinned for ai-usage (134 777 B) is not today's; sizes of a moving program are anchors, not facts.

**UNK** The text `custom/weather`, `custom/update` and `custom/voxtype` render now was not determined: weather and update need the network, and no producer was executed this round.

## §2 Two indicator scripts are upstream bytes

**OBS** [ref] (omarchy `v3.8.4`, `default/waybar/indicators/screen-recording.sh`, 169 B, sha256 `28491cd3...c63c`): the whole probe is one process test, `if pgrep -f "^gpu-screen-recorder" >/dev/null; then`, a start-anchored match on the full command line; its negative branch prints `{"text": ""}`.

**OBS** [ref] (same tag, `notification-silencing.sh`, 174 B, sha256 `312900d1...de69`): the whole probe is one read, `if makoctl mode | grep -q 'do-not-disturb'; then`, a substring test on the mode name, not an equality test.

**OBS** [ref] (measured 2026-10-25): the host's copies of both scripts (`~/.local/share/omarchy/default/waybar/indicators/`, mode 755) are byte-identical to the upstream bytes (`cmp` rc 0 in both directions) and to upstream `v3.8.3`; the host checkout is at tag `v3.8.4` while its `version` file still reads `3.8.3`. The 6354 B host config is *not* upstream (the stock file is 5114 B, held in `config-health-report-r3.md`): the host edits the config, not these scripts.

## §3 State, with the dates it was read

**OBS** [ref] (2026-10-25, read-only queries): `pgrep -a -x hypridle` printed a running daemon, no `gpu-screen-recorder` process matched, and `makoctl mode` printed `default`; the cache of the ai-usage chip was younger than 24 hours (its raw timestamp is deliberately not quoted: it rotates every few minutes).

**INF** With `hypridle` running, `idle.sh`'s `then` branch fires, so the idle chip renders **empty text** - the opposite of the held 2026-10-14 reading ("glyph shown = lock disabled"), which was true when `hypridle` was absent. The round-35 registry row for the idle chain already records the daemon running; the held module row stays correct as a statement of the script's rule, and is stale as a statement of the host's state. Three of the seven JSON producers (recorder, do-not-disturb, idle) render empty today; `voxtype` is absent from `PATH` on this host.

## §4 What this does not license

- Nothing about the weather or update producers' text, or any live usage figure from the ai-usage cache.
- Nothing about the gkeep or ai-usage packages' behaviour, install state or window rules: they are chain evidence (shim bytes and declared contract), not owned.
- State lines (§3) are dated reads of a moving host; re-read, never reuse.
