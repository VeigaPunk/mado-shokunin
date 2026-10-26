# ScoutSiblings - sibling-lane overlap on the monitor/output plane (round 45, C1 `tools/mado-monitors.py`, C2 `hyprland-monitor-rule-r45.md`)

Method: read-only `grep -n -i -E` over `PROVINCE.md`, `SKILL.md`, `corpus/knowledge/*`, `corpus/*.md` of the 20 sibling lanes (`/home/vgpnk/Projects/shokunin/*-shokunin`, mado excluded), pass 1 terms
`hyprctl monitors|monitor =|monitorv2|EDID|wl_output|xdg_output|wlr-randr|wayland-info|kanshi|DP-N|HDMI-A|DRM connector|modetest|refresh rate|Hyprland|fractional scale|scale factor|monitor rule|multi-monitor|DPI|display server`
(67 hits), pass 2 terms `nvidia-drm|modeset|/sys/class/drm|connector|aquamarine|framebuffer|HiDPI|content_scale|VRR|HDR|resolution|...` on tsukuroi, game-dev-2d/3d, tabi, souji, mori. Tooling: grep only (no LSP; text-search is literal evidence of presence/absence, not semantic proof).
Host/compositor: not touched. No sibling lane was edited.

## Result in one line

**No sibling lane owns, overlaps or even mentions the `monitor =` rule -> `hyprctl monitors all -j` join.** Zero hits for `hyprctl monitors`, `monitor =`, `monitorv2`, `EDID`, `wlr-randr`, `wayland-info`, `wl_output`, `xdg_output`, `kanshi`, `DP-1` in any sibling PROVINCE.md / SKILL.md / corpus file. Every hit is one of: an explicit deferral TO mado, an adjacent kernel/driver-health layer below the compositor, a Hyprland-the-process incident record, or a homonym. Verdict: C1/C2 absorb **no** sibling ground.

## Hit table (lane - file:line - relation)

Relation key: OWNS = lane holds the ground; OVERLAPS = lane holds part of the same surface; ADJACENT = neighbouring surface, different object; DEFERS-TO-MADO = lane states the ground is mado's; HOMONYM = same word, other thing.

| lane | file:line | what it says (<=25 words) | relation |
|---|---|---|---|
| game-dev-3d | PROVINCE.md:75 | "Desktop/compositor display behavior belongs to `mado-shokunin`" (cites `../mado-shokunin/PROVINCE.md:3-12`) | DEFERS-TO-MADO |
| game-dev-3d | PROVINCE.md:62 | Godot visual capture needs a real render path; `--headless` has no rasterizer/framebuffer | ADJACENT (engine render path, not outputs) |
| tsukuroi | PROVINCE.md:124 (OUT-004, ADJ-03) | quotes mado's Owns line: Hyprland/waybar/walker config plane, screen/idle behaviour | DEFERS-TO-MADO |
| tsukuroi | PROVINCE.md:48 (ADJ-03) | "Desktop rendering, bindings, menu or idle behavior needs configuration-level diagnosis" -> mado; tsukuroi supplies unit/package/driver health only | DEFERS-TO-MADO |
| tsukuroi | corpus/knowledge/adjacency-anchors-r19.md:84, .json:56-58 | anchor of the same OUT-004 quote | DEFERS-TO-MADO (derivative) |
| tsukuroi | corpus/knowledge/driver-firmware-plane.md:23-25, 97-100 | `nvidia_modeset`, `nvidia_drm` loaded; `[drm] Initialized nvidia-drm 0.0.0 ... on minor 1`; Hyprland/Xwayland named as GPU clients | ADJACENT (kernel DRM module state below the compositor; no connector, mode, EDID or output data) |
| tsukuroi | SKILL.md:49 (driver & firmware plane row) | `nvidia-smi`, `lsmod`, `dkms`, `modinfo` | ADJACENT (driver health) |
| tsukuroi | corpus/knowledge/oom-event-plane.md:35,65-71,151; kill-event-deep-r8.md:62-66; boot-plane.md:101; degraded-triage-r4.md:214,478-479; hygiene-sweep-r4 (tabi) :114-127 | `app-Hyprland-*.scope` oom-kill, greeter-Hyprland SIGSEGV in `libaquamarine` (the greeter compositor, uid 964) | ADJACENT (process/OOM/crash records naming Hyprland; no config or output state) |
| tsukuroi | corpus/knowledge/update-safety-note.md:166-172,197 | `hyprland` package sizes and a pacman class filter | ADJACENT (package update trigger; relevant to C2's recheck line "a Hyprland or hyprutils package update ... is the earlier trigger") |
| mori | corpus/knowledge/observability-census-r1.md:94,143 | `app-Hyprland-xdg-terminal-exec-*.scope` oom-kill | ADJACENT (journal/OOM) |
| tabi | corpus/knowledge/hygiene-sweep-r4.md:114-127,229; webbridge-disposition:271; webbridge-revival-assessment.md:66 | Hyprland SIGSEGV 13:11:07 / session cycle | ADJACENT (same incident as tsukuroi's) |
| tabi | corpus/knowledge/cdp-evidence-patterns.md:32,68; PROVINCE.md:9 | chromium run with `--ozone-platform=wayland`; CDP screenshot PNG IHDR W x H | ADJACENT (browser viewport pixels, not output geometry; `captureScreenshot` dims are page not monitor) |
| kake | corpus/knowledge/ops-automation.md:83 | `grokbot start` spawns app "on Hyprland ws 3" | ADJACENT (workspace, not monitor rule) |
| kotoba | PROVINCE.md:69; corpus/knowledge/sibling-overlap-census-round74.md:66,97 (also round49:82) | census row: mado owns Hyprland/waybar/walker/terminal config plane and display behaviour read-only; "states no split with kotoba" | DEFERS-TO-MADO |
| kotoba | corpus/knowledge/checklist-execution-round15.md:146 | a Hyprland config block vs a shell block in a docstring | ADJACENT (docs hygiene) |
| kumitate | SKILL.md:622; corpus/knowledge/counter-amendment-discipline.md:82; mount-order-and-bind-scope.md:15 | "bind" = bwrap mount, not mado's keybind file `mado-binds.py` | HOMONYM (keybind, not monitor) |
| tameshi | corpus/knowledge/mutation-case-mado-verify.md:41,87 | mutation case on mado-verify's `hyprland.conf` sha-pin (`mado-verify.sh:574`) | ADJACENT (mutation target is the verifier, not the monitor check at `:3518-3530`) |
| audio, chousa, kagi, kasegi, kotodama, kengaku | various | "output name", "display resolution", "Hyprland ws" strings in unrelated contexts | HOMONYM |
| game-dev-2d | PROVINCE.md:23-24 | "Rendered output/performance" | HOMONYM (game render output) |
| souji, kaidoku, kama, revenger, kake | - | no monitor/output/Hyprland hit beyond homonyms ("output", "DRM circumvention" revenger PROVINCE:20, game-dev-3d PROVINCE:41 = copy protection) | HOMONYM |

Owns-the-ground count: **0 sibling lanes**. Overlaps: **0**. Adjacent: tsukuroi (driver/DRM-module health; Hyprland process crash/OOM records), mori/tabi (same incident records), tabi (browser screenshot dims), tameshi (verifier mutation), kake (workspace launch). Defers to mado: game-dev-3d, tsukuroi, kotoba (3 lanes, 5 locators).

## Intra-lane prior ground (mado's own, disclosed for the adjacency axis; not sibling)

- `tools/mado-verify.sh:3518-3530` - checks one hardcoded output (DP-1, 3440x1440, abs(refresh-100)<0.5) from `hyprctl monitors`; reads no rule. Already declared in registration.md as base prior art.
- `corpus/knowledge/output-colour-boundaries-r14.md:1-32` - U5 wlr-output-management/colour protocol boundary; its `UNK` "runtime state agreement" is exactly what C1/C2 measure (entry.md `ground:` line cites it). No monitor-rule parsing.
- `tools/mado-wsrules.py:233,261,277-293` - workspace-rule `monitor:` key (a different keyword than `monitor =`); C1 does not compute workspace-to-monitor binding. Disjoint surface, same selector vocabulary (`desc:`) - kept cross-referenced, not absorbed.
- `tools/mado-geometry.py` - exists at base; K01 control copies it and is rejected by the counter (registration.md, ctl-c1). Not monitor-rule ground.

## Ruling: do C1/C2 absorb sibling ground? (adjacency axis)

**No.** Rationale (each against a located source):
1. No sibling owns the `monitor =` rule plane or `hyprctl monitors` data (0 literal hits across 20 lanes, both greps).
2. The only lanes touching the same *physical* stack are tsukuroi (DRM kernel modules `driver-firmware-plane.md:23-25,97-100`; Hyprland crash/OOM records) - one layer below. C1 reads files + one JSON dump; per its docstring it starts no process and opens no socket, and the counter clause `r` forbids `hyprctl/journalctl/wlr-randr/wayland-info` on PATH, so C1 cannot drift into tsukuroi's journalctl/dmesg/DRM probes or kaidoku/REA artifact territory. C2's entry states `ground: U5 output management` (mado's own), cites only hyprwm sources (S302-S310), and states no EDID/DRM/driver fact.
3. EDID: sibling lanes hold no EDID text (0 hits). The draft entry mentions EDID only inside the disclosed round-3 neighbour note (registration.md:41); `desc:` selectors read the description string only. EDID/connector fields/serials remain unmodelled -> mado-shaped shape-only rule (no monitor serials/descriptions committed) stays enforced by `ExecPrivacyGate`.
4. Three lanes already route display behaviour to mado by name (game-dev-3d PROVINCE:75, tsukuroi PROVINCE:48/124, kotoba PROVINCE:69), so landing C1/C2 is consistent with every sibling's own boundary statement; no lane needs a pointer change.

## Handoffs / watch items (reported, not absorbed; none require action in w1)

- tsukuroi ADJ-03 (`PROVINCE.md:48`) could cite `tools/mado-monitors.py` as the mado read route once admitted - **tsukuroi's L1's call, no edit made**.
- Entry recheck line "Hyprland or hyprutils package update is the earlier trigger" lines up with tsukuroi update-safety (`update-safety-note.md:166-197`); the entry should keep it as a *trigger reference only* and not restate package state (tsukuroi's plane).
- The tsukuroi greeter-Hyprland `libaquamarine` segfault records (greeter compositor, uid 964, `/usr/share/sddm/hyprland.conf`) are a *different Hyprland instance*; C1 must not be read as covering it (it joins `~/.config/hypr` rules to the session's dump). One disclosure sentence in the entry would pre-empt the confusion; no sibling ground is moved.
- kotoba sibling-overlap census (`...round74.md:66,97`) is the lane that would re-classify mado after landing; no pre-emptive edit.

## Unresolved / unobserved

- Sibling `corpus/lessons`, `reports`, `.ufo` and tracked `tools` trees were not grepped (scope was PROVINCE.md + corpus/knowledge + SKILL.md + corpus/*.md); absence there is [INFERENCE]. A second grep for `hyprctl monitors` over tsukuroi/tools returned no hits (tsukuroi tools listing checked).
- No semantic (LSP) pass: grep is the literal fallback; this is a presence/absence sweep, not a semantic proof.
