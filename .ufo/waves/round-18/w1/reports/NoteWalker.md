# NoteWalker — round 18 P3 documentary route (report)

Seat: MadoR18.NoteWalker (leaf, no delegation). Surface P3 (walker, elephant). Documentary route only; no walker or elephant process was run, no socket connected, no launcher opened.

## Behavior

Drafted the P3 route note with the four required sections and head lines 1-4. Every upstream claim is a tag-pinned raw body with a fetch receipt; every host claim is file bytes (sha256, stat, grep, one python byte read of `/usr/bin/walker`). No host state was changed.

Key findings:

- Host walker and elephant were upgraded by pacman on 2026-10-20: `walker 2.17.0-1 -> 2.17.2-1` (`/var/log/pacman.log:2929`) and `elephant 2.21.0-1 -> 2.22.1-1` (`:3095`). Walker-restart hooks ran at `:3062` and `:3123`. Tags v2.17.2 and v2.22.1 match.
- The round-7/9 pins (walker 2.17.0 binary, packaged config) are superseded by file bytes now on disk: `/usr/bin/walker` 7,039,912 B sha `25240650…`; `/etc/xdg/walker/config.toml` 13,743 B sha `3c5c6867…`, byte-equal to upstream `resources/config.toml` at v2.17.2. Reported as MOVED pins in the note; older notes not edited (S015 protocol).
- Source-side (tag v2.17.2): walker loads config once (`src/config.rs:7-8, 586-594`; `src/main.rs:108`); no config reload or file-watch call anywhere in `src/` (whole-tree textual search of the tag tarball). `notify = "8.2.0"` is declared in `Cargo.toml:21` but unused in `src/`.
- Source-side: a `WALKER_` environment overlay is declared (`src/config.rs:234-239`). Which names it honours is unexercised.
- Source-side: elephant socket is `$XDG_RUNTIME_DIR/elephant/elephant.sock` (`internal/comm/comm.go:38-44`; walker `src/data.rs:156-161`). The elephant README's `/tmp/elephant.sock` (`README.md:211`) is stale for v2.22.1.
- Source-side: config discovery uses `xdg::BaseDirectories::find_config_file`, which searches `XDG_CONFIG_HOME` then `XDG_CONFIG_DIRS` (crate docs, saved HTML lines 356-358).
- Omarchy v3.8.4 tag bytes equal the host copies for `config/walker/config.toml`, `bin/omarchy-launch-walker`, `bin/omarchy-restart-walker`, `bin/omarchy-refresh-walker`, `default/walker/walker.desktop` and `restart.conf`. The omarchy checkout is at `8fcc9d60…` (= tag `v3.8.4`), read from `.git/packed-refs` as bytes.

## Gates

No lane gate was run (documentary seat; contract forbids gates here). No verification run beyond the hashing and grep checks listed in the note's § Safe observation.

## Touched surfaces

Files written (only these, plus the fetch artifacts below):

- `corpus/knowledge/walker-route-r18.md` (new; head lines 1-4 as specified; sections `## Upstream contract`, `## Host declaration`, `## Safe observation`, `## Unexercised behavior`; `[UNK]` inside the last).
- `.ufo/waves/round-18/drafts/NoteWalker-rows.md` (proposed SOURCES rows in the 11-column shape, 20 rows, all `S0xx-pending`, `used-by` names the note).
- `.ufo/waves/round-18/fetch/NoteWalker/` — 27 raw bodies plus `receipts.jsonl` (27 JSON lines, schema `mado-fetch-receipt-v1`). Largest body: walker tag tarball 165,438 B (below the 1 MiB limit; nothing skipped).
- `.ufo/waves/round-18/w1/reports/NoteWalker.md` (this report).

Scratch outside the lane: `/tmp/nw-r18/` (tag tarball extracted for the textual search; `git ls-remote` tag lines recorded in the note head). No git write of any kind; no git command in the lane or in the omarchy checkout.

Host reads only: `/usr/bin/walker` (python byte read, never executed), `/etc/xdg/walker/`, `~/.config/walker/`, `~/.config/elephant/` (listing and sizes), `~/.config/autostart/walker.desktop`, `~/.config/systemd/user/app-walker@autostart.service.d/restart.conf`, `~/.local/share/omarchy/` (bin, config, default, `.git` files as bytes), `~/.config/hypr` and `~/.local/share/omarchy/default/hypr` (grep for walker bindings), `/var/log/pacman.log` (grep and read). Not run: walker, elephant, any omarchy-* command, systemctl, journalctl, pacman in any form, pidof/pgrep, hyprctl, busctl, sockets.

## Out-of-scope items

- P5 theme rendering: `theme/mod.rs` is cited only for the `additional_theme_location` path and tilde replace.
- `omarchy-refresh-config` (the helper called by `omarchy-refresh-walker`) was not fetched.
- `src/providers/emergency.rs`, provider implementations, and the walker-to-elephant message handlers were not read.
- `/etc/xdg` and `/usr/bin/walker` identity against a rebuild of the v2.17.2 tag was not attempted.
- Errata to `walker-deep-r9.md` and `walker-live-surface.md` (moved pins): reported, not edited.

## Findings for the integrator

1. L1 assigns S-ids to the 20 rows in `drafts/NoteWalker-rows.md`; the note head uses `S0xx-pending` in order. The rows are proposed `mined` with `opened 2026-10-20`.
2. Tag resolutions in the head are `git ls-remote` output, not receipts (walker v2.17.2 = `a515085f…`, elephant v2.22.1 = `8f1e21d6…`, omarchy v3.8.4 = `8fcc9d60…`, all lightweight).
3. Two drifts for the lane owner: the elephant README socket path (`/tmp/elephant.sock`) vs source; and the unused `notify` crate in walker's manifest.
4. The `[UNK]` list in § Unexercised behavior is the open list for P3. It covers running-process identity, binary-to-tag identity, the `WALKER_*` overlay names, array merge semantics, emergency provider, elephant provider loading and protocol, the refresh helper, and hypr include edges.

## Tool installs

None. Tools used were already present: `curl 8.23.0`, `git` (read-only `ls-remote`), `python3`, `tar`, `sha256sum`, `stat`, `wc`, grep tool.
