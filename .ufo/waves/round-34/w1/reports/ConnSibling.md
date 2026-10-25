# ConnSibling — sibling-overlap scan, Waybar⇄Hyprland event-socket theme

Seat: connector, mado round-34 w1. Read-only scan, executed 2026-10-24.
Scope: every `*-shokunin` directory under `/home/vgpnk/Projects/shokunin/`;
surfaces grepped: `corpus/SOURCES.md` and `corpus/knowledge/` (recursively).
Terms: `waybar`, `hyprland`, `socket2` (case-insensitive).

Command shape actually run (one grep over a semicolon path list, then `skip=20`
to drain the result set):

```sh
grep -inE 'waybar|hyprland|socket2' \
  <lane>/corpus/SOURCES.md <lane>/corpus/knowledge/**   # per lane, all 21 lanes
```

Lanes rostered on disk: 21 (`*-shokunin` glob). `tameshi-shokukin/` (misspelled)
does not match the pattern and holds only a nested `tameshi-shokunin/` dir; not
scanned as a lane. mado's own corpus was grepped separately for the delta and is
excluded from the hit tables below.

## Hits per sibling (repo → file → line)

### kaidoku-shokunin — waybar as a coredump/RE artifact only

- `corpus/knowledge/2026-10-13-crash-evidence.md:16` — `getfacl` on
  `core.waybar.1000.…1728….zst`; ACL readability of the waybar core.
- `corpus/knowledge/2026-10-13-crash-evidence.md:22-23` — waybar SIGABRT
  (PID 1728) counted among 3 organic crashes.
- `corpus/knowledge/2026-10-13-crash-evidence.md:50,54` — `coredumpctl debug
  1728` RE loop against the waybar core.
- `corpus/knowledge/2026-10-13-crash-evidence.md:57` — summary naming the waybar
  core among retained crash surface.
- `corpus/knowledge/2026-10-13-r2-crash-inspect-probe.md:22` — waybar core
  decompresses to 434,184,192 B > REA's 32 MiB cap.
- `corpus/knowledge/2026-10-13-r2-crash-inspect-probe.md:29-30` — feeding
  `/usr/bin/waybar` (ET_EXEC) refused `unsupported_target` (not ET_CORE).
- `corpus/knowledge/2026-10-13-r2-crash-inspect-probe.md:50,56,60,66` — run-log
  entries: waybar core selection, `out_of_range` boundary, ET_EXEC negative
  probe, frontier note (organic waybar core uninspectable by REA).

### kake-shokunin — incidental ops row

- `corpus/knowledge/ops-automation.md:83` — `grokbot start` spawns a Grok Bot
  app "on Hyprland ws 3". Workspace number, not compositor mechanics.

### kotoba-shokunin — a lint caveat and a census quote of mado's SKILL

- `corpus/knowledge/checklist-execution-round15.md:146` — the lane's extractor
  "cannot distinguish a Hyprland config block from a shell block".
- `corpus/knowledge/sibling-overlap-census-round49.md:82` — census table row
  quoting mado SKILL.md:8: "the Hyprland/waybar/walker/terminal config plane"
  (attributes ownership to mado).

### kumitate-shokunin — name disambiguation only

- `corpus/knowledge/counter-amendment-discipline.md:82-83` — "a lane file named
  `mado-binds.py` is Hyprland keybind config"; avoids the bind/mount collision.
- `corpus/knowledge/mount-order-and-bind-scope.md:15` — "not mado's Hyprland
  keybinding table or `mado-binds.py`".

### mori-shokunin — host-incident journal rows

- `corpus/knowledge/observability-census-r1.md:94,143` — the
  `app-Hyprland-xdg-terminal-exec-dd9e67bd.scope` oom-kill record and its
  non-attribution to the webbridge daemon.

### tabi-shokunin — session-restart forensics

- `corpus/knowledge/hygiene-sweep-r4.md:114,117,127,229` — Hyprland 1203316 in
  the process ancestry; `coredumpctl` Hyprland SIGSEGV at 13:11:07; trigger
  listed as unresolved.
- `corpus/knowledge/webbridge-daemon-disposition.md:271` — OOM teardown;
  "session/Hyprland restarted".
- `corpus/knowledge/webbridge-revival-assessment.md:66` — cross-ref to the same
  restart.

### tameshi-shokunin — mutation study OF mado's gate (nearest sibling contact)

- `corpus/knowledge/mutation-case-mado-verify.md:41,87` — names mado's
  `hyprland.conf` sha pin (`:574`) and include-graph census while mutating
  `tools/mado-verify.sh`.
- `corpus/knowledge/mutation-case-mado-verify.md:114` — live-mutation fixture
  writes to `$C/waybar/style.css` mid-run.
- `corpus/knowledge/mutation-case-mado-verify.md:154` — asserts
  `waybar.config.reload_style` PASS / `waybar.config.parse` FAIL row vocabulary
  of mado's verifier. Content is about the gate, not about Waybar itself.

### tsukuroi-shokunin — host triage, package metadata, and one province quote

- `corpus/knowledge/adjacency-anchors-r19.md:84` and
  `adjacency-anchors-r19.json:56,58` — quotes mado PROVINCE.md:3-16 verbatim:
  "Mado owns the Hyprland, waybar, walker and terminal configuration plane"
  (marks the surface OUT for tsukuroi).
- `corpus/knowledge/aur-risk-plane-ver-s6.md:70`,
  `aur-risk-plane.md:199` — `hyprland-preview-share-picker` and
  `hyprland-guiutils` as package-name tokens in AUR risk rows.
- `corpus/knowledge/boot-plane.md:101,132` — `app-Hyprland-…scope` oom-kill rows.
- `corpus/knowledge/calibration-synthesis.md:274` — same scope row re-cited.
- `corpus/knowledge/degraded-triage-r4.md:214,253,478-481,500,534` — greeter
  Hyprland SIGSEGV (`Hyprland --watchdog-fd 4 --config
  /usr/share/sddm/hyprland.conf`), waybar among session-4 restarts, OOM cgroup
  ancestry.
- `corpus/knowledge/driver-firmware-plane.md:97` — Hyprland listed as a GPU
  client process.
- `corpus/knowledge/kill-event-deep-r8.md:47,62-66,72,78,94,109,141,219` —
  `xdg-desktop-portal-hyprland`'s last journal record, greeter-Hyprland
  libaquamarine segfault, `waybar` inside the killed cgroup's scope members,
  `uwsm start … hyprland.desktop` session-command chain.
- `corpus/knowledge/oom-event-plane.md:35,65,71,125,151,181,304,332` — same OOM
  family: Hyprland scope names, session leader `uwsm … Hyprland`, Hyprland in
  `ps` consumer list, session cgroup members incl. Hyprland processes.
- `corpus/knowledge/systemd-user-plane.md:19` — `uwsm_hyprland.desktop` journal
  warning line.
- `corpus/knowledge/update-safety-note.md:166,172,197` — `hyprland` package
  download/installed sizes and a pacman `-Qu` class-filter regex.

## Zero-hit siblings on the scoped surfaces

`corpus/SOURCES.md` + `corpus/knowledge/` clean in: audio, chousa,
game-dev-2d, game-dev-3d, kagi, kama, kasegi, kengaku, kotodama, lore,
revenger, souji (12 lanes). No sibling `SOURCES.md` matched at all — every hit
above is inside `knowledge/`.

Out-of-scope sighting (reported for completeness, not counted): audio's
`corpus/live/` receipts contain many `waybar`/`xdg-desktop-portal-hyprland`
tokens as PipeWire client names in `pw-dump`/`pactl` captures; the task scope
was `SOURCES.md` + `knowledge/` only.

`socket2`: zero hits in every sibling on the scoped surfaces.

## What the round-34 entry adds that no sibling holds

Committed at `fa7ba11` (verified via `git show --stat`): new
`corpus/knowledge/waybar-module-text-route-r25.md` plus SOURCES rows S201/S202.
Content observed directly: tagged Waybar 0.15.0 upstream files
`src/modules/hyprland/backend.cpp` and `src/modules/hyprland/window.cpp` —
Waybar's own code deriving the Hyprland socket folder
(`$XDG_RUNTIME_DIR/hypr`, `/tmp/hypr` fallback) and registering
`m_ipc.registerForIPC("activewindow", this)`.

This is the **client side** of the event-socket contract (mado's r32 entries
covered the compositor's two-socket server side). No sibling corpus carries any
of it: their every mention is process-level (coredumps, cgroup scopes, journal
lines), package-level (pacman names), or meta-level (province/SKILL quotes that
assign this surface to mado, a mutation study of mado's verifier, a config-block
lint caveat). Zero sibling rows bind Waybar to IPC mechanics, and `socket2`
appears nowhere. The two siblings that even *point at* this territory —
kotoba's census and tsukuroi's adjacency anchors — both record it as mado's
province, i.e. they explicitly route the theme here rather than holding it.

## No-edit confirmation

Every operation this seat ran against sibling paths was `read`, `grep`, or `ls`
— no `write`/`edit`/redirect touched any sibling file. The only file created is
this report, inside mado's own `.ufo/waves/round-34/w1/reports/` tree.
