# Connector sibling-overlap — Hyprland IPC / dispatcher (round 32 w1)

Read-only. No sibling repo was written. Nothing absorbed.

Probe (re-run this session, each sibling `corpus/knowledge/`):

```
grep -rilE 'socket2|\.socket\.sock|hyprctl dispatch' <lane>/corpus/knowledge/
```

20 sibling lanes (mado excluded). Every `corpus/knowledge/` exists. Exact-probe file count is **0** on every lane. No note to inspect as a hit. **No SAME-SURFACE. No ADJACENT overlap with the IPC request/event socket contract or with dispatcher semantics.**

| Lane | Exact-probe notes | What they claim | Verdict |
|---|---|---|---|
| audio | none | — | NONE |
| chousa | none | — | NONE |
| game-dev-2d | none | — | NONE |
| game-dev-3d | none | — | NONE |
| kagi | none | — | NONE |
| kaidoku | none | — | NONE |
| kake | none | — | NONE |
| kama | none | — | NONE |
| kasegi | none | — | NONE |
| kengaku | none | — | NONE |
| kotoba | none | — | NONE |
| kotodama | none | — | NONE |
| kumitate | none | — | NONE |
| lore | none | — | NONE |
| mori | none | — | NONE |
| revenger | none | — | NONE |
| souji | none | — | NONE |
| tabi | none | — | NONE |
| tameshi | none | — | NONE |
| tsukuroi | none | — | NONE |

## Incidental Hyprland text (not the probe; not the contract)

A second pass (`hyprland|hyprctl|socket2|HYPRLAND_INSTANCE|.socket.sock`, case-insensitive) found mentions. None state a socket path, an event-socket grammar, a request-socket grammar, or `hyprctl dispatch` semantics. Left NONE so they are not silent and not absorbed.

- **kake** `ops-automation.md`: `grokbot start` spawns a GUI on Hyprland workspace 3. Window target, not IPC.
- **kotoba** `checklist-execution-round15.md`: a Hyprland config block is an example of a shell-block vs config-block cut. Parsing pedagogy, not IPC.
- **kotoba** `sibling-overlap-census-round49.md`: quotes mado `SKILL.md` as the Hyprland/waybar/walker/terminal **config plane**. Assigns that plane to mado; says nothing about sockets or dispatch.
- **kumitate** `counter-amendment-discipline.md` and `mount-order-and-bind-scope.md`: disambiguate bwrap bind mounts from mado keybinds / `mado-binds.py`. Explicitly not the compositor IPC surface.
- **mori** `observability-census-r1.md`: cgroup name `app-Hyprland-xdg-terminal-exec-….scope` in an OOM census. Process death, not the socket contract.
- **tabi** `hygiene-sweep-r4.md`, `webbridge-daemon-disposition.md`, `webbridge-revival-assessment.md`: Hyprland appears as a process ancestor (`--watchdog-fd 4`) and as the session that restarted in an OOM teardown. Lifecycle, not IPC.
- **tameshi** `mutation-case-mado-verify.md`: mutation case of `mado-verify.sh`. `hyprland.conf` is a sha pin; scenario C starves `PATH` so the `hyprctl` binary is absent and no compositor is touched. Test hermeticity of mado's verifier, not request/event socket grammar and not dispatcher semantics.
- **tsukuroi** `aur-risk-plane.md`, `aur-risk-plane-ver-s6.md`, `update-safety-note.md`: package names (`hyprland`, `hyprland-guiutils`, `hyprland-preview-share-picker`) and sync sizes. Package plane.
- **tsukuroi** `boot-plane.md`, `oom-event-plane.md`, `degraded-triage-r4.md`, `kill-event-deep-r8.md`, `systemd-user-plane.md`, `driver-firmware-plane.md`: journal/cgroup/segfault/session-restart evidence (including `xdg-desktop-portal-hyprland` as a journal writer and `uwsm_hyprland.desktop` scheduling warning). Host lifecycle, not the IPC contract.
- **tsukuroi** `adjacency-anchors-r19.md` / `.json`: records mado's province as the config plane ("Mado owns the Hyprland, waybar, walker and terminal configuration plane"). Does not grant mado, or claim for tsukuroi, the IPC socket or dispatcher surface.

## "dispatcher" false friends (rejected)

The word `dispatcher` occurs outside the probe pattern. Inspected; none are Hyprland:

- **kagi** `janitor-command-surface.md`, `claim-ledger.md`: shell `case` verb dispatcher.
- **kaidoku** EVM notes (`2026-10-13-r3-evm-interface.md`, `2026-10-19-arc3-r*`): Solidity/Vyper bytecode selector dispatch.
- **kasegi** `mission-control.md` and related: bounty `fleet-dispatch.mjs` mission loop.
- **kengaku** `ledger-route-telemetry.md`: counts of kasegi's `dispatcher_tick`; states mission-state/dispatcher semantics belong to kasegi.

## mado `PROVINCE.md` — does not claim the IPC/dispatcher surface

`grep` of `PROVINCE.md` for `socket2`, `.socket.sock`, `hyprctl dispatch`, `IPC`, and `dispatcher` returned no matches.

The owns line stops at config files and idle behavior (lines 6–9):

> **Owns (surfaces):** `~/.config/hypr/` (hyprland.conf, keybinds, rules, animations), `~/.config/waybar/`, `~/.config/walker/`, terminal emulator configs (`~/.config/alacritty|foot|kitty|ghostty/`), themes/wallpapers as declared files, screen/idle behavior (hypridle/hyprlock where present).

Line 15 refuses mutation of a running compositor; it does not claim the socket. The tool table is the closest text and still is not the contract: line 28 allows `hyprctl` **read verbs only** (`version`, `instances`, `configerrors`, `getoption`, `binds`, `monitors`, `layers`) — `dispatch` is not in that list. Lines 29 and 30 say `mado-binds.py` and `mado-anims.py` open **no compositor, socket, network**.

Integrator: the IPC request/event socket contract and dispatcher semantics are unoccupied by sibling knowledge. Do not treat the incidental notes above as a contest.
