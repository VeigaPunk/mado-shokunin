# ConnSiblingOverlap — sibling-overlap scan for round-44 C1/C2

Seat: `ConnSiblingOverlap` (w1). Date: 2026-10-26. Lane: mado-shokunin.
Scope: read-only scan of the other lanes under `/home/vgpnk/Projects/shokunin/*-shokunin/` for
holdings overlapping **C1** (`tools/mado-geometry.py` state verdicts: fsmode from the client's
`fullscreen` value, verdict order BADSIZE | FULLSCREEN | MAXIMIZED | TILED | AGREE | DIFFER,
`maximized=<n> fullscreen=<n>` summary fields) or **C2**
(`corpus/knowledge/hyprland-gkeep-size-request-r44.md`: the post-box configure/ack path —
`sendWindowSize` → `realToReportSize` → xdg `setSize` → `scheduleConfigure` → pending-ack list /
`onAck`, the X11 configure branch, xdg-shell 1.49 client freedoms, GTK 4.24.1 Wayland toplevel
sizing, gkeep 133b867 `set_default_size(420, 500)` / `size_request_calls=0`).

Method (read-only; every locator below was computed with `grep -n`, none typed):

1. Case-insensitive content sweep across all 20 sibling lanes for
   `fullscreen|maximiz|xdg_toplevel|configure|set_default_size|gtk4|gkeep` over
   `{PROVINCE.md, corpus/README.md, corpus/knowledge, tools, SKILL.md}`, then a second sweep for
   `gkeep|hyprland|hyprctl|wayland|gtk4|xdg.?shell|xdg_toplevel|compositor` with `.ufo` and
   `node_modules` excluded.
2. Exact-word checks: `gkeep`, `hyprctl|hyprland`, `xdg_toplevel|xdg-shell|xdg_shell`,
   `set_default_size|gtk4|wayland` — sibling lanes only, `.ufo`/`node_modules` excluded.
3. Read all 20 sibling `PROVINCE.md` files (domain/owns/refuses lines) to confirm no lane claims
   the compositor/desktop domain.
4. Verified the two surviving sibling `gkeep` byte-hits are non-substantive (kumitate archived
   session blob; souji tmp-snapshot census paths) and re-verified game-dev-2d's `hyprctl clients
   -j` consumer.
5. Cross-checked mado's own holdings (PROVINCE.md, corpus/README.md coverage map, round-43
   admitted entry) and kotoba's fleet sibling-overlap census rows for mado.

## 1. Overlaps: none

No sibling lane holds a fact that C1's state-verdict tool or C2's configure-path entry would
duplicate or re-derive:

- **C1 terms** (`fullscreen`, `maximized`, compositor geometry verdicts): zero substantive hits
  in any sibling lane. The only `fullscreen`/`maximize` string hits outside mado are unrelated
  domains — audio's mpv strace logs (`audio-shokunin/corpus/live/r73-reviewer/strace-mpv-*.log`,
  mpv CLI flags), game-dev-3d's unreal-mcp upstream docs, kake's web-publish entries.
- **C2 terms** (`xdg_toplevel`, `xdg-shell`, `set_default_size`, `gtk4`, configure/ack):
  zero substantive hits. `xdg_toplevel` appears only inside game-dev-2d Godot **export binary
  fixtures** (`corpus/live/r25-export-scout/pair1-absolute/project/out/fixture.x86_64` and
  siblings — binary strings, not knowledge); `wayland` appears only as mpv display-connection
  strings in audio strace logs.
- **`gkeep`**: zero substantive sibling hits. The word occurs twice, both non-knowledge:
  - `kumitate-shokunin/corpus/knowledge/kimi-session-state.md:166` — the substring inside an
    archived agent-session JSON blob (`"thinkingKeep":"all"`); no knowledge claim.
  - `souji-shokunin/census/operator-sweep-20261019/fresh-120min.txt:686,989,1289,1589,1889,2189,
    2489,2790,3090` — souji's hygiene sweep listing **stale /tmp xsnapshot artifacts** whose paths
    end `applied/hypr/gkeep.conf`; path mentions only, no content, no behavior claim. (This file
    is not cited in the round-43 scan; it is either newer or was below that scan's noise floor.
    Either way it is a hygiene census, not a holding.)
- No sibling `PROVINCE.md` claims the desktop/compositor domain. mado's
  `PROVINCE.md:3` — "desktop & compositor craft — the Hyprland/waybar/walker configuration plane"
  — is the only compositor province in the fleet; every other lane's province (audio, chousa,
  game-dev-2d/3d, kagi, kaidoku, kake, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore,
  mori, revenger, souji, tabi, tameshi, tsukuroi) is disjoint by its own "Owns/Refuses" text.

## 2. Adjacent sibling holdings (shared surface, no content overlap)

| # | Lane | Holding (path:line) | What it touches | Relation to C1/C2 |
|---|---|---|---|---|
| A | game-dev-2d | `corpus/live/r79-boundary-exec/run_love_probe.py:40-47` | runs `hyprctl clients -j`, reads `class`/`initialClass`/`title` to detect a love window | Same **read verb** as C1, disjoint fields (presence, not size/state); no rules, no geometry join |
| B | souji | `census/operator-sweep-20261019/fresh-120min.txt:686` et al. | hygiene sweep of stale /tmp xsnapshot dirs listing `applied/hypr/gkeep.conf` paths | **Hygiene census only**; names a gkeep.conf path, holds no content or behavior claim; any question about the config's bytes routes to mado |
| C | kumitate | `corpus/knowledge/kimi-session-state.md:166` | archived session JSON blob | Substring false positive; not a holding |
| D | tsukuroi | `PROVINCE.md` (adjacency anchors), `corpus/knowledge/adjacency-anchors-r19.md` | host-surface adjacency registry assigning the Hyprland config plane to mado | **Boundary arbiter**, not a content holder |
| E | kotoba | `corpus/knowledge/sibling-overlap-census-round49.md`, `…round74.md:66,97` | fleet sibling-overlap census; mado row = `none`, quote `SKILL.md:8` | **Registrar/arbiter** for overlap claims |
| F | tameshi | `corpus/knowledge/mutation-case-mado-verify.md` | mutation-testing service over mado tools | Relationship lane for tool quality; no fact overlap |
| G | mori | `corpus/knowledge/observability-census-r1.md` | host process/cgroup liveness | Would arbitrate live-process claims; C1/C2 make none |

## 3. Contradictions

None. No sibling holding states or implies anything about (a) Hyprland fullscreen/maximized
client geometry or the `fullscreen` IPC field, or (b) the xdg configure/ack path, GTK Wayland
toplevel sizing, or gkeep's declared size — so nothing contradicts the round-44 claims. The
round-43 scan's verdict (no overlap) still holds; the round-44 deltas (fsmode state verdicts for
C1; the post-box configure/ack chain for C2) introduce holdings in territory no sibling has
entered.

## 4. Who arbitrates (adjacency axis)

- **kotoba** — standing registrar of fleet sibling-overlap (`check_sibling_census.py`, census
  rounds 49/74). Its round-74 row pins mado at adjacency `none`; it is the neutral arbiter if a
  future sibling moves into the Hyprland geometry plane.
- **tsukuroi** — host-operability lane; its adjacency registry already assigns the Hyprland
  config plane to mado. Host-surface boundary questions route through it.
- **game-dev-2d** — the only other consumer of the `hyprctl clients -j` read verb; would
  arbitrate any claim about reading `clients -j` fields (currently disjoint: presence vs
  size/state).
- **tameshi** — owns the mutation-testing method over mado tools; arbitrates tool-quality
  claims, not facts.
- **mori** — host liveness/process observation; would arbitrate any live gkeep/hyprland process
  claim (none is made).
- **souji** — if its sweep ever escalates the stale `gkeep.conf` snapshot paths into a content
  claim, mado arbitrates the content (souji's own province is receipt-gated removal, not domain
  knowledge).

## 5. Duplication verdict

- **C1 tool extension** duplicates no sibling-held fact. The `fullscreen` IPC field, the
  eFullscreenMode 0/1/2 semantics, and the maximized/fullscreen box replacement are un-held
  outside mado; the nearest sibling usage of the same dump (game-dev-2d row A) reads disjoint
  fields.
- **C2 entry** duplicates no sibling-held fact. Its chain maps to the round-44 pins
  (`Hyprland-Window.cpp` S164-held, `Hyprland-XDGShell.cpp` S298, `xdg-shell.xml` S299,
  `gdktoplevel-wayland.c` S300, `gkeep-ui.py` S297-held/S301) plus the shokuknow residue
  predecessor `gkeep-client-size-request-r12.md`; no sibling lane holds any link of it. The
  round-43 entry `hyprland-gkeep-geometry-r43.md` (admitted from `gkeep-size-to-real-size-r11.md`,
  which may not be re-admitted) is in-lane history, not sibling overlap.

## 6. gkeep: what mado may claim (operator's project)

No sibling contests mado's gkeep coverage; the binding constraints are in-lane and
operator-ownership:

1. `~/Projects/gkeep` is the operator's project — read-only to this lane (never written, never
   executed). Round-44 C2 claims only what the pinned bytes license: `set_default_size(420, 500)`,
   `size_request_calls=0`, `application_id=org.omarchy.gkeep` — a source census, not a runtime
   behavior claim.
2. `corpus/knowledge/config-drift-r12.md` — the lane measures and reports; the gkeep project owns
   its installer; the installer "was read, not executed".
3. `corpus/knowledge/host-bar-producer-census-r40.md:37` — gkeep's behavior/install state is
   "chain evidence … not owned".
4. mado may claim the compositor side (what Hyprland does with the window: box set, then
   `sendWindowSize` → configure → ack bookkeeping) as sourced knowledge, and may claim the join to
   gkeep's declared size only via the pinned `gkeep-ui.py` bytes — never a claim that the operator
   observed gkeep at some size on the host session (round-43 census: no gkeep window mapped).
5. SKILL.md's geometry row stays honest under C1: a fullscreen gkeep window is now reported
   FULLSCREEN (not DIFFER); `NO_MATCHING_CLIENT` still means only "no mapped window carried the
   class".
