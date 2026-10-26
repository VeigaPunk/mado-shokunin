# ScoutCoverage - coverage-map ground for C1 and C2 (round 44, w1)

Base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f` (commit object confirmed: `git cat-file -t` -> `commit`). All greps are read-only
`git grep` at that revision. Scope: `corpus/knowledge` (60 entries), `PROVINCE.md`, `SKILL.md`, `tools`, plus `corpus/README.md` (which the
registration's path set omits). Tool: git grep only; no LSP question (prose and markdown, not code symbols). Lane HEAD during the read was
`ae996fcf5e50`, a descendant of base; every fact below is cited at base, not HEAD.

## 1. Did the lane hold the C2 chain at base? NO - zero hits on every compositor-side and client-side token

| command (at base, `-- corpus/knowledge PROVINCE.md SKILL.md tools`) | files with a hit |
|---|---|
| `git grep -ciE 'sendWindowSize\|realToReportSize\|scheduleConfigure\|pending.?size.?ack\|onAck' ...` | none |
| `git grep -ciE 'x11_configure\|xdg_setSize\|setSize' ...` | none |
| `git grep -ciE 'xdg-shell\|xdg_toplevel' ...` | none |
| `git grep -ciE 'set_default_size\|default.size\|size_request\|set_size_request' ...` | `hyprland-gkeep-geometry-r43.md` x4 only (all are the default-size census, see below) |
| `git grep -ciE 'application_id\|org.omarchy.gkeep' ...` | SKILL.md x3, `hyprland-gkeep-geometry-r43.md` x8, `tools/mado-geometry.py` x3 |
| the registration's own command `git grep -ciE 'sendWindowSize\|pendingSizeAcks\|xdg_toplevel.configure\|set_size_request' ...` | empty, exit 1 (`receipts/c2-ground-base.txt` agrees) |
| same tokens over the whole tree minus `.ufo` and `corpus/lessons` | only `SCORECARD.md:1` (the planned-item line naming the gap), nothing in a corpus entry |
| same tokens with `.ufo` included | only raw pins (`.ufo/waves/round-24/fetch/S164.bin`, round-43 pins of `Window.cpp`, `WindowTarget.cpp`) and the ScoutStagedGkeep/ScoutMergeRest survey notes: bytes held as evidence, never cited by an entry |

False positives I checked and rejected (so a later reader does not count them as holdings):
- `configure` hits in 11 files (waybar, portals, input debugging, ...) are the English verb or config-plane wording, none is xdg `configure`.
- `wayland-protocol-boundaries-r13.md:33` "acknowledgment requirements" is protocol *governance* (S040), not `ack_configure`; line 54 holds
  `xdg_wm_base | 7 | Registry header only; no test window.` - the interface exists in the host registry and nothing else about it is held.
- `\back\b|acknowledg|ack_configure` over the corpus returns only that governance line and `wayland-protocol-boundaries-r13.md:113`.
- GTK: the only GTK hits are `org.gtk.Actions` D-Bus probes (walker/waybar entries), `GDK_SCALE=1` env rows (`hyprland-config-plane.md`,
  `hyprctl-verification-layer.md:154`), `walker-route-r18.md:50` ("built with GTK4 and Rust") and the r43 entry's `Gtk.ApplicationWindow`.
  Nothing on how a GTK 4 Wayland toplevel handles a configure size. `input-debugging-boundaries-r15.md` explicitly leaves "toolkit/IME behavior" `[UNK]`.

What the r43 entry already holds on the client side (so C2 deepens this, not replaces it): `hyprland-gkeep-geometry-r43.md` §4 (lines 60-66):
S297 `window.set_default_size(420, 500)` on a `Gtk.ApplicationWindow`, application id `org.omarchy.gkeep`; an isolated-oracle observation of 420x500 floating;
census line `gkeep request default_size=420x500 application_id=org.omarchy.gkeep`. It carries no `size_request_call` count: `git grep -ciE size_request` over corpus/knowledge,
tools, SKILL.md, PROVINCE.md, README.md at base has no hit; the only related words are "default size" and, at line 66, the oracle stand-in's "no size request". Its S297 is an excerpt `gkeep/ui.py:446-488`, not the file.
Its own "does not establish" section and the round-43 README route (README.md:294-301) name the open items C2 targets: "the client's acknowledgement path".

## 2. Did the lane hold the C1 ground (fullscreen/maximized box) at base? NO

| command | result |
|---|---|
| `git grep -ciE 'maximi[sz]\|work.?area'` (corpus/knowledge, PROVINCE.md, SKILL.md, tools) | `work.?area`: none; `maximize` variants appear only as keybind vocabulary (see next row) |
| `git grep -ciE 'setTargetSizeAndPosition\|eFullscreenMode\|FullscreenHandler'` | none (also none for `FullscreenController` content) |
| `git grep -niE fullscreen` over the same paths | `keybind-rule-semantics.md:156,158` (`fullscreen`/`fullscreenstate` dispatcher flags: mode 0 = whole screen, 1 = maximize, documented from the wiki), `:189,220,224` (rule matchers); `config-health-report-r3.md:528,747,811,973` (`misc:on_focus_under_fullscreen`, dispatcher counts); `window-rule-effects-getprop.md:14,27,50,74` (`opacity_fullscreen`); `hyprland-gkeep-geometry-r43.md:46` (one quoted `isFullscreen` guard); `tools/mado-binds.py`, `tools/mado-options.py` (binds/options) |
| `git grep -nE 'fullscreen' -- tools/mado-geometry.py` | no hit: the shipped tool never reads the `fullscreen` field |

So: the dispatcher and rule-matcher vocabulary for fullscreen/maximize is held (keybind, getprop opacity, option rows); what a fullscreen or maximized window's
*box* is, and that `hyprctl clients -j` prints `fullscreen` = the internal mode (0/1/2), was held nowhere. The r43 entry's only touch is the quoted WindowTarget
guard (`Fullscreen::controller()->isFullscreen`, S293), which says the floating `setBox` is skipped for a fullscreen window and not what box such a window gets;
C1's own docstring finding (registration "Why these claims") is that the shipped tool therefore reports a fullscreen window DIFFER. Grounding pins are
`.ufo/waves/round-44/fetch-c1/` (FullscreenHandler.cpp, FullscreenController.hpp, HyprCtl.cpp), which C1 consumes in the tool docstring, not in a corpus entry:
C1 has no corpus-entry deliverable (counter reads only the tool and the r42 counter).

## 3. Coverage-map rows and Frontier bullets each claim moves

Layout of `corpus/README.md` at base (header lines): `## Coverage map` L3 (table rows L5-71, last row = the r43 geometry entry at **L71**), `## Quality bar` L73,
`## Province routes` L78 (table, surface "Hyprland config, binds, rules and display"), `## Frontier` L104 (bullets L106-~190), then dated `###` sub-routes; the
newest is `### Round-43 rule-size versus reported-size route` **L294-301**. There is no round-41/42 bullet in the top Frontier list (L106 is round 40); rounds 35-43 are
sub-route headings.

### C2 (hyprland-gkeep-size-request-r44.md) - a new coverage-map row plus a new sub-route
- **New row appended after README.md:71** in the Coverage map: `knowledge/hyprland-gkeep-size-request-r44.md` (MADO-R44-1, round 44; assimilation of the gkeep residue, successor to
  the staged `gkeep-client-size-request-r12`), Sources S164 (held; scope below), S298, S299, S300, S301.
- **Frontier sub-route to add** (pattern: the dated `###` routes): `### Round-44 compositor-to-client size route`. It is the continuation of the
  **Round-43 route, README.md:294-301**, whose own "Still open" list names three things: a live gkeep window, "the drawn size during and after the open animation",
  and "the client's acknowledgement path, and rule attribution". C2 moves *only* "the client's acknowledgement path" (documentary, from pins), and must keep the rest open:
  no live window, no drawn-size observation, no rule attribution (`rule-attribution-r24.md` holds that, README Round-24 route L226). The route's wording at L298-301
  must be read as superseded for that one clause only; any edit to L294-301 is an edit to a held sentence and must be an append-only correction, not a rewrite.
- **Province routes table (L78+)**: surface "Hyprland config, binds, rules and display" should gain a link to the r44 entry next to r43 (the r43 entry is not in that table either; no
  `hyprland-gkeep-geometry-r43` text there - the route is reached via the coverage-map row and the sub-route only).
- **Frontier top list (L106+)**: no bullet there is about client size. The nearest open bullets are "Rendered UI, Waybar module text, Walker socket protocol, dispatcher behavior and
  per-window rule effects" (L108-110, arc gap ledger §6) and "Round 15 ... toolkit/IME behavior ... stay open" (README.md:139-143). C2 does **not** close "per-window rule effects" nor
  "toolkit behavior" in general: the GTK claim is bounded to GTK 4.24.1's toplevel configure handling in one file. State that limit.
- **SKILL.md**: only the question row L158 ("rendered size, the client's own request and rule attribution stay `[UNK]`") and the Rule-size section (L246-290) mention the client's request.
  C2 may add one question row; it must not flip L158's `[UNK]` for rendered size.
- **PROVINCE.md**: no row needed for C2 (no tool, no new read surface). The assimilation is documentary; Hyprland/xdg-shell/GTK sources are upstream, gkeep is `~/Projects/gkeep`, already outside the lane's
  owned config planes (PROVINCE "Owns"): note that the entry's gkeep claims are about a client the lane does not own and read only through a pinned file.

### C1 (tools/mado-geometry.py states) - no new coverage row, but five existing sentences go stale and must be moved with the tool
Instrument/operability, not a new entry. The sentences that name the four-verdict set or the tool's blind spot, at base:
| file:line | text that becomes wrong or incomplete |
|---|---|
| `corpus/README.md:71` (tail) | "Tool `tools/mado-geometry.py`; ... " row of the r43 entry - add nothing to it; S-id list unchanged |
| `corpus/README.md:298` | "(AGREE / DIFFER / TILED / BADSIZE)" - now six verdicts (BADSIZE/FULLSCREEN/MAXIMIZED/TILED/AGREE/DIFFER) |
| `SKILL.md:225` | "per matched client AGREE / DIFFER / TILED / BADSIZE" row of the tool table |
| `SKILL.md:158` | question row's licence: add the state verdicts without widening `[OBS]` beyond the two printed sides plus the printed `fullscreen` integer |
| `SKILL.md:246-290` | § "Rule size versus reported size": verdict table L274-277 (add FULLSCREEN, MAXIMIZED rows; narrow the TILED "licenses" cell for closure D3, pseudo-tiled clients, already routed in registration L26), summary line grammar (L290 example is the zero-sum byte-identical case), exit map |
| `PROVINCE.md:32` | the `tools/mado-geometry.py` row: reads/writes unchanged (same two inputs); its owner clause still says "an AGREE verdict says nothing about the rendered size" - extend to the state verdicts |
These are record edits for the L1 (SKILL/PROVINCE/README rows); a C1 seat edits only the tool.

## 4. Honest expansion-credit sentence

**C2 is new ground at the compositor-to-client boundary and a deepening of the client declaration.** Candidate sentence for the lesson `## Gate` / README row (state both halves):

> "Round 44 adds the path *after* the box is set - `CWindow::sendWindowSize`, `realToReportSize`, the xdg toplevel `setSize`/`scheduleConfigure`, the pending-ack list and `onAck`, the X11 configure branch, what xdg-shell 1.49 lets a client do with a configure size and what GTK 4.24.1's Wayland toplevel does with one - none of which any entry held at base (zero hits for those tokens in corpus/knowledge, PROVINCE.md, SKILL.md and tools at 6a1a905); it deepens, and does not replace, `hyprland-gkeep-geometry-r43.md` §4, which held only the client's `set_default_size(420, 500)` and application id, here extended from a 43-line excerpt (S297) to the full `gkeep/ui.py` at 133b867 and to the absence of any `set_size_request`; it does not move 'rendered size', 'toolkit behavior' in general or rule attribution."

What it must NOT claim as new ground: (a) `gkeep default_size=420x500` and `application_id` (r43 §4, S297 already carry it); (b) the animation GOAL vs CURRENT split and the `clients -j` reading (S294/S158, r43 §3); (c) `Window.cpp` as a source in itself: S164 is held, but its recorded locators (`103-108,141-146,1484-1486,1791-1795,2143-2281,2497`) do **not** cover `onAck` (L1514), `realToReportSize` (L1685) or `sendWindowSize` (L1732-1760) in the pinned bytes (`grep -n` of `fetch/Hyprland-Window.cpp`: onAck 1514, realToReportSize 1685, sendWindowSize 1732, `setSize(` 1753): this is held-row *scope extension*, not a new row - the entry must cite S164 with its own computed locators, and the registry row's `Gives` text for S164 ("static-rule application, property-change hooks") does not describe it; flag for the L1 (append-only registry: a held row cannot be edited, so the extension lives in the entry/gate lines). XDGShell.cpp (S298), xdg-shell.xml (S299), gdktoplevel-wayland.c (S300) are new ground: the lane holds `xdg_wm_base | 7` as a registry header only (`wayland-protocol-boundaries-r13.md:54`), no xdg-shell semantics.

**C1 earns no coverage credit.** It is operability on an existing instrument (round-43 tool): fullscreen/maximized *geometry* is new knowledge only to the extent the tool docstring pins it; no corpus entry, README row or Frontier bullet is moved, and the lane held no fullscreen-box claim (§2) to deepen. Honest wording: "C1 fixes a false DIFFER the round-43 tool gave for fullscreen windows; its grounding (FullscreenHandler.cpp, FullscreenController.hpp, HyprCtl.cpp `.internal`) is cited in the tool docstring and the fetch-c1 pins, not added to the corpus."

## 5. Adjacency with siblings' provinces (flags, not edits)

- **Keybind/dispatcher province** (`keybind-rule-semantics.md:156,158`, `fullscreen`/`fullscreenstate` dispatchers, documented 0=fullscreen 1=maximize): C1's `fullscreen` = `.internal` mode 0/1/2 uses the *internal* enum, the same word as the dispatcher's `fullscreenstate` internal. Any C1 SKILL text must say `clients -j` prints `.internal` (HyprCtl pin) and must not reuse the dispatcher table's "client" half; cross-link to keybind-rule-semantics rather than restate.
- **Rule attribution / window rule effects** (`rule-attribution-r24.md`, `window-rule-effects-getprop.md`): the S164 row's own "Gives" says the source does not identify an originating rule; C2 must not cite `Window.cpp` as saying which rule wrote a box.
- **Wayland protocol boundaries** (`wayland-protocol-boundaries-r13.md`, README Round-13 bullet "Feature behavior ... remain unclaimed"): C2's xdg-shell 1.49 text is the first *behavioral* xdg-shell claim; the r13 entry holds only the `xdg_wm_base` v7 registry header and the stable/staging policy. Adjacent, not overlapping; link it, do not rewrite its "advertisement is not feature behavior" boundary.
- **Input debugging** (`input-debugging-boundaries-r15.md`: "toolkit/IME behavior ... stay [UNK]"): C2's GTK claim is toolkit behavior for one file and one release; cite as bounded, do not close that open bullet.
- **Event/IPC province** (`ipc-contract-r25.md`, `event-delivery-limits-r26.md`, `request-socket-live-bound-r8.md`): they share `HyprCtl.cpp` (S158); C1's `fullscreen` field sits in the `clients` builder (`fetch-c1/Hyprland-HyprCtl.cpp:410-412`, `.internal` per the registration), inside S158's recorded range `346-484`, so no scope extension of S158 is needed for the line numbers (check the fetch-c1 pin is the same commit before citing).
- **Idle/lock, waybar, walker, theme**: no adjacency (zero token overlap in §1 and §2 greps).
- **Quarantine/staging siblings** (ScoutStagedResidue, ScoutQuarantine, ConnSiblingOverlap and the id-guard slice under `.ufo/waves/round-44/assimilation/`): the staged predecessor `gkeep-client-size-request-r12.md` is the only staged file this theme may admit; `gkeep-size-to-real-size-r11.md` is r43-admitted and may not be re-admitted (counter STAGED set excludes it).

## 6. Unknowns left
- Whether the new rows S298-S301 are the final ids (provisional; the id guard and the registry tip S297 decide).
- Whether README L294-301 should be amended in place or by a new sub-route (append-only vs held sentence: the lane's pattern at L192, L202 is a dated `###` correction route; I recommend the same).
- I did not read the pins' content (other seats do); every claim above about their lines is from `grep -n` of the pinned bytes or the cited docs.
