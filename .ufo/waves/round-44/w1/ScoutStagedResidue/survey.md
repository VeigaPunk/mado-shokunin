# ScoutStagedResidue — gkeep residue vs. the five pins (round 44, w1, C2 planning data-walk)

Read-only walk. Inputs: the 7 named staged entries, `merge/mado/MERGE-REPORT.md`, the staged `SOURCES.append.md` rows they cite,
`corpus/lessons/round-43.md` (assimilation ledger, lines 70-84, 214-226), `PROVINCE.md`, the five pins in
`.ufo/waves/round-44/fetch/` (sha256 match `receipts/fetch-sha256.txt`: Window d735d454…, XDGShell d90b534c…, gdktoplevel 0ee38458…, gkeep-ui 07a3c4a5…,
xdg-shell.xml 7ba7f9c8…), the frozen counter `quality/counters/c2-r44-gkeep-size-request.py`, `assimilation/*`.
Locators below are computed (`grep -n` / a normalizing script over the pins), not typed. "OBS" = read in a file this session; "INF" = my inference.
No tool beyond read-only shell/python was run; no host or compositor access.

## 0. Headline

- **Admit `gkeep-client-size-request-r12.md` as the predecessor — but only its two re-groundable observations, rewritten.** Its two staged sources are both
  re-groundable from pins (S311 → pin `Hyprland-Window.cpp` = held S164, sha d735d454 equals S164's recorded sha; S312 → pin `gkeep-ui.py`). Its
  *inferences* are not clean: three are refuted or unsupported by the pins (§2). The entry must be a rewrite carrying the corrected chain, not a copy.
- **Refuse** (recommended, with flips): r9 (partly), r13, r14, r15, r31. **Defer/withhold** r30 (flip already fired but off C2's theme and no lane row for the
  fired source). r8, r10, obs-r11 were refused in round 43 and need no new line; r11-size is admitted (r43) and may not be touched.
- The pins re-ground MORE than r12 needs: `commitWindow` clamps a floating xdg window to the client's `set_min_size`/`set_max_size` (Window.cpp:2742-2746),
  which is the real path by which "a client minimum larger than the request" would change the box — the one question r12 said it had "excluded by the
  client's own source". It is only *open* (UNK), not excluded, because the window's own minimum comes from GTK's widget layer (gtkwindow.c, not pinned).

## 1. Per-file table

| file (staged) | claims | re-groundable from the 5 pins | rests on private `lanes/mado/roundN` receipt / unpinned source | PROVINCE | overlap with `hyprland-gkeep-geometry-r43.md` |
|---|---|---|---|---|---|
| **r12** `gkeep-client-size-request-r12.md` | C-a: `sendWindowSize` asks the client for the size via an xdg-shell call and files it in `m_pendingSizeAcks`. C-b: gkeep declares `set_default_size(420, 500)`, no `set_size_request`; `min-*` only under `button.ink`. C-c: so nothing client-side can refuse; "a GTK4 window with no minimum-size request will adopt the size the compositor configures". C-d: rendered geometry is 420×500 "with no competing claim". | **C-a yes** (Window.cpp:1732-1754, quotes at 1741, 1753 verified; S311 tag URL ≡ pin: same sha as held S164). **C-b yes** (gkeep-ui.py:449,474-476; `set_size_request` 0 hits; `min-height/min-width` only at 87-88 under `button.ink`). **C-c/C-d: not supported / partly refuted** — see §2. | none private; S311 is cited at the *tag* URL, the pin is the *commit* URL (same bytes: sha d735d454 = S164 row). Header cites `gkeep-size-to-real-size-r11.md` by a path the lane does not have (r11 is `hyprland-gkeep-geometry-r43.md`). | in (the host's gkeep window sizing; r43 already admits that chain) | **none**: r43 stops at `m_realSize`/GOAL and the JSON; `git grep -E 'sendWindowSize\|pendingSizeAcks\|xdg_toplevel.configure\|set_size_request'` at base = 0 hits. r12 is strictly downstream of r43 §2-§3. |
| **r9** `gkeep-rendered-geometry-chain-r9.md` | class = Wayland app_id (`fetchClass`); gkeep declares app_id; host rule matches it; 420×500 agrees twice ("not coincidence"); wiki never mentions `app_id` (0 occurrences); `min-height:30px/min-width:72px` "far below target"; observation still missing (S292: `gkeep clients: 0`, S293 hyprland.log). | `fetchClass` yes (Window.cpp:1502-1512; `return m_xdgSurface->m_toplevel->m_state.appid;` at 1505, appid stored at XDGShell.cpp:189); app_id decl yes (gkeep-ui.py:449); css numbers yes (87-88). | **S286** docs.gtk.org set_default_size ("if no other constraints apply" etc.) — not pinned (gdktoplevel is the GDK layer, default-size semantics live in gtk). **S287** wiki size effect + "0 occurrences of app_id" — not pinned. **S292, S293** = `lanes/mado/round9/fetch/*` private host receipts. | in | r43 already holds the match + rule path (S290, S155, S295, S297). Unique to r9: only the `fetchClass`→app_id link. §3's "agree by design" is the "two agreeing numbers" point r43 §4 already makes (as INF: "cannot say which of the two set it"). |
| **r13** `…-record-r13.md` | `onAck` reconciles pending list by serial (S318); map-time size log line at DEBUG (S319); host journal has 0 map lines, INFO control 2, DEBUG control 0 (S320); "the size that becomes the window's is the compositor's own… the client can acknowledge or refuse; it cannot substitute"; two gates stop the observation. | `onAck` yes (Window.cpp:1514-1528); the DEBUG line yes (2515, `Log::DEBUG`). §1's "cannot substitute / refuse" **not supported** (§2). | **S320** = `lanes/mado/round13/fetch/host-journal-map-log-sweep.txt` (private; no copy in lane). Its journal counts are a 2026-10-24 host measurement. | §1-§2 in; §3 (journal sweep) borders tsukuroi's journal/unit ground (round-43 CritAssimilation F6 already says so of r14) | onAck absent from r43. DEBUG-line locator absent from r43 (entry "makes no log claim"). |
| **r14** `…-record-r14.md` | whole-journal sweep: 140496 lines, 0 map lines, 2 boots, INFO control 2 / DEBUG control 0; gkeep store keys `body/created/id` (no geometry). | nothing. | S326 private receipt; the store-key census (3 keys) has **no row at all** (only prose). | journal = tsukuroi-adjacent; `journalctl` is not in this round's allowed host reads | none |
| **r15** `gkeep-geometry-never-recorded-r15.md` | lane's round-24 `.bin` artifacts: 16, 0 name gkeep. | nothing. | S339 = `lanes/mado/round15/fetch/…` private. (The artifact dir does exist in this lane: `.ufo/waves/round-24/fetch/S153.bin…`, so the count is re-measurable by `grep -l gkeep …/*.bin \| wc -l`; the claim is negative-existential about the lane's own history.) | in, but a negative census of the lane's own paperwork, not a desktop fact | stale: r43 §4 now holds an *isolated-oracle* observation of 420×500; r15's "the corpus has never held an observation" is true only for host sessions. |
| **r30** `gkeep-element-rules-r30.md` | three rule lines + the file comment "Omarchy sizes that tag at 875×600" → the 420×500 is a work-around for a tag rule. | rule lines: none of the five pins (they are S295, held). | S251 = host file (own-work). The 875×600 side is host `~/.local/share/omarchy/default/hypr/apps/system.conf:4` (r43 lesson 220-221 / `w1/ExecLiveHost/live-census.txt:232`) — **no lane row for it** (`grep apps/system.conf corpus/SOURCES.md` → 0). | in | rule lines duplicate r43 §1 (S295). New content = the 875×600 tag collision only. |
| **r31** `glyph-and-geometry-r31.md` | §1 weather glyph = Nerd Fonts `weather-cloud` e33d (S256); §2 gkeep size "agreed twice", rule "makes the geometry deterministic across sessions and window managers". | §2 half only: gkeep-ui.py:476. | S256 nerd-fonts glyphnames (unpinned); S219 (staged id collides with lane S219) | §1 off-theme (bar/glyph); §2 in | §2 = r43 §4 INF. "deterministic across … window managers" is an unsupported overclaim (a Hyprland rule binds no other WM). |

## 2. r12 claims the pins refute or do not support

Each row: r12 text → what the pins say. Locators computed.

1. **"with `xdg_toplevel.set_size`" (§1 INF) — refuted as protocol wording.** In xdg-shell 1.49 the only `set_size` request is on `xdg_positioner`
   (xdg-shell.xml:157; interfaces at :32, :124, :409, :622, :1247). `xdg_toplevel` has no `set_size`; it receives an `xdg_toplevel.configure` *event*
   (xdg-shell.xml:1144-1171) whose width/height are "a hint to the window about how its surface should be resized" (:1150-1152).
   `setSize` is Hyprland's C++ method `CXDGToplevelResource::setSize` (XDGShell.cpp:354-357: stores `m_pendingApply.size`, calls
   `scheduleStateApplication()`, returns `m_owner->scheduleConfigure()`), which later emits `m_resource->sendConfigure(m_pendingApply.size.x,
   m_pendingApply.size.y, &arr)` (XDGShell.cpp:455) and then `CXDGSurfaceResource::configure` → `sendConfigure(m_scheduledSerial)` (XDGShell.cpp:640-642;
   serial allocated in `scheduleConfigure`, :629-638). The counter's own line `hyprland sendWindowSize xdg_setSize=1 x11_configure=1` counts the C++ call
   `->setSize(` (Window.cpp:1753) and `->configure(` (:1751); the entry must not describe the C++ name as a protocol request.
2. **"the acknowledgement is tracked — which is precisely the mechanism by which a client could report a different size" (§1 INF) — refuted.**
   `xdg_surface.ack_configure` carries only a serial (xdg-shell.xml:575-593; `Doing so will raise an invalid_serial error` at :593).
   Hyprland's `onAck(serial)` (Window.cpp:1514-1528) looks up the newest pending entry with `e.first <= serial`, erases entries up to it, and writes the
   *compositor's stored size* into `m_pending.ackedSize` (:1526; the trailing `// apply pending size. We pinged, the window ponged.` is a comment — the counter's
   comment-stripping means that sentence cannot be the Gate quote, use the code on the left of it). No client-supplied size passes through the ack. This also
   contradicts r13's §1 framing ("the client can acknowledge or refuse"): xdg-shell says `Clients must send an ack_configure in response` (xdg-shell.xml:1166); there is no refusal.
   What the ack feeds: `getReportedSize()` returns `m_current.ackedSize` (Window.cpp:1861-1866).
3. **"a GTK4 window with no minimum-size request will adopt the size the compositor configures" (§2 INF) — only conditionally supported.**
   GDK-layer pin (gdktoplevel-wayland.c): a configure with width>0 and height>0 sets `next_layout.configured_width/height` (:681-682); `compute_size` then runs
   `gdk_surface_constrain_size(&geometry_hints, …)` when `should_constrain` (:525-529) and calls `gdk_wayland_toplevel_update_size` (:530, :548). So the GDK
   layer adopts the configured size, **clamped by geometry hints** (min size from `gdk_toplevel_notify_compute_size`, :485, :498-500). A 0×0 configure means
   "client decides" (:647-653; xdg-shell.xml:1154-1155). Where the state is maximized/fullscreen/tiled `size_is_fixed` is set (gdktoplevel-wayland.c:633-637 `fixed_size`, :680).
   What is **not** in any pin: GTK's widget-layer window minimum (gtkwindow.c measure), which is what fills `size.min_width/min_height` — and `set_size_request` is
   only one input to a widget's minimum. "No `set_size_request` in ui.py" (true: gkeep-ui.py has 0 hits) does not imply "no minimum": child
   `button.ink` `min-height:30px; min-width:72px` (gkeep-ui.py:87-88) and ScrolledWindow/label children still feed the window's measured minimum. r9's "far below
   the target" compares two numbers, not the window's measured minimum. → UNK, not excluded.
4. **"The one way the rendered geometry could differ from 420×500 — a client minimum larger than the request — is excluded by the client's own source" (§2) —
   not supported by the pins; and the compositor-side path is now visible.** GTK sends `xdg_toplevel.set_min_size/set_max_size` from its hints
   (gdktoplevel-wayland.c:1333-1334); Hyprland stores them (XDGShell.cpp:244-246, `layoutMinSize` :467-473), and **on every commit** a floating, non-fullscreen
   xdg window is clamped to them: `clampWindowSize(MINSIZE, MAXSIZE…)` in `CWindow::commitWindow` (Window.cpp:2742-2746; `clampWindowSize` :1277-1288 rewrites
   the target box via `setPositionGlobal`). So the compositor's box *can* be changed by the client's declared minimum — contra r13's "the value is the
   compositor's throughout" and r12's "the compositor's action and with no competing claim from the app". Also `CWindow::minSize()` (:2885-2900) lets a
   rule override. Whether gkeep's min exceeds 420×500 is not decidable from the pins → UNK that the entry should state as such.
5. **"a GTK4 default size is … " paraphrase (r9 §3, S286) — not re-groundable.** The five pins contain no `set_default_size` documentation; the entry may only say
   what gkeep *declares* (gkeep-ui.py:476, `window.set_default_size(420, 500)`) and what GDK does with a configure, not what GTK's default-size means.
6. **"The rendered geometry of a gkeep window is 420×500 on this host's build" (§3 INF) — over-reaches** r43's own scope: r43 says the GOAL is the box, and
   nothing in the pins shows a window drawn at that size; the pins add that fullscreen/maximized states change the box (C1) and that min/max hints can clamp it (item 4).
7. **Package-local paperwork the entry must not copy:** `coverage-map: R-4`, `ground: P6`, `recheck: 30d — … (ran 2026-10-24, no window open)`, `AMENDS corpus/knowledge/
   gkeep-size-to-real-size-r11.md` (path absent in lane; the lane's successor is `hyprland-gkeep-geometry-r43.md`), and the self-referential
   "`gkeep-client-size-request-r12.md`'s predecessor" sentence. A `recheck` must be a counter-valid cell (ISO date, `NNd` or `on-*`).

## 3. What the pins re-ground that r12 did not use (so the entry can say more than the staged file)

All locators computed; quote candidates were each tested for: exactly one occurrence in the pin (whitespace-normalized), absence from the other four pins,
and a whitespace-word count. The counter (docstring d+) additionally strips `//`,`/* */` (C/C++) and `#` (py) comments before searching, and requires 3-25 words — several
short code lines below are 2 whitespace-words; extend them with the adjacent token until ≥3 (verify with the counter's own splitter before the Gate line).

| topic | pin | locator | candidate Gate quote (unique across the 5 pins: verified) |
|---|---|---|---|
| reported size = GOAL clamped at ≥0 | Window.cpp | 1685-1688 | `return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);` (:1687, 4 words) |
| the call | Window.cpp | 1753 | `m_pendingSizeAcks.emplace_back(m_xdgSurface->m_toplevel->setSize(REPORTSIZE), REPORTSIZE.floor());` — 2 whitespace-words, extend |
| X11 branch | Window.cpp | 1750-1751; `onX11ConfigureRequest` 1536-1574 | `m_xwaylandSurface->configure({REPORTPOS, REPORTSIZE});` (:1751) |
| ack consumption | Window.cpp | 1514-1528 | `m_wlSurface->resource()->m_pending.ackedSize = m_pendingSizeAck->second;` (:1526; 3 words) |
| where the ack is read | Window.cpp | 1861-1866 | `return m_wlSurface->resource()->m_current.ackedSize;` (:1865) |
| client min/max clamps the box | Window.cpp | 2742-2746 | `if (clampWindowSize(MINSIZE, MAXSIZE > Vector2D{1, 1} ? std::optional<Vector2D>{MAXSIZE} : std::nullopt))` (10 words) |
| class = app_id (only if the entry keeps the r9 link) | Window.cpp | 1502-1512 | `return m_xdgSurface->m_toplevel->m_state.appid;` (:1505) |
| map-time DEBUG line (only if the journal route is kept) | Window.cpp | 2515 | `Log::logger->log(Log::DEBUG, "Map request dispatched, monitor {}, window pos: {:5j}, window size: {:5j}"` |
| setSize → configure event | XDGShell.cpp | 354-357, 444-455, 629-642 | `m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);` (:455); `m_stateUpdate = g_pEventLoopManager->doLaterLock([this] { configure(); });` (:633) |
| min size stored | XDGShell.cpp | 244-246, 467-473 | `m_pending.minSize = {x, y};` (:245) |
| configure is a hint | xdg-shell.xml | 1150-1152 | "The width and height arguments specify a hint to the window about how its surface should be resized in window geometry coordinates." (22 words) |
| 0×0 = client decides | xdg-shell.xml | 1154-1156 | "If the width or height arguments are zero, it means the client should decide its own window dimension." (18) |
| fullscreen = a maximum | xdg-shell.xml | 850-852 | "The surface is fullscreen. The window geometry specified in the configure event is a maximum; the client cannot resize beyond it." (21) — links C1 |
| maximized must be obeyed | xdg-shell.xml | 841-842 | "The window geometry specified in the configure event must be obeyed by the client" (locator by grep; uniqueness re-checked below) |
| ack must be sent | xdg-shell.xml | 1166 | "Clients must send an ack_configure in response to this event." (10) |
| multiple configures | xdg-shell.xml | 614-616 | "If the client receives multiple configure events before it can respond to one, it is free to discard all but the last event it received." (25 — at the limit) |
| min size is not obeyed | xdg-shell.xml | 1009-1011 | "The client should not rely on the compositor to obey the minimum size." (13) |
| GTK adopts configured size | gdktoplevel-wayland.c | 681-682, 513-531 | `wayland_surface->next_layout.configured_width = width;` (:681) |
| GTK 0×0 = own size / restore | gdktoplevel-wayland.c | 647-653 | `saved_size = (width == 0 && height == 0);` (:647) |
| GTK acks the serial | gdktoplevel-wayland.c | 706 | `XDG_SHELL_CALL (xdg_surface, ack_configure, wayland_surface, wayland_surface->pending.serial);` |
| GTK sends min size | gdktoplevel-wayland.c | 1333-1334 | `XDG_SHELL_CALL (xdg_toplevel, set_min_size, toplevel, min_width, min_height);` |
| constraint applied | gdktoplevel-wayland.c | 525-529 | `gdk_surface_constrain_size (&wayland_toplevel->geometry_hints,` (2 words) |
| gkeep declares | gkeep-ui.py | 449, 474-476 | `window.set_default_size(420, 500)` (:476; 2 words); `application_id="org.omarchy.gkeep",` (:449) |
| gkeep undecorated | gkeep-ui.py | 475 | `window.set_decorated(False)` — no CSD shadows; relevant to GTK's `shadow_*` offsets (gdktoplevel-wayland.c:518-521) |
| gkeep never asks for max/fullscreen | gkeep-ui.py | grep `maximize\|fullscreen\|set_resizable` → 0 hits | negative; locator by grep, not a line |

Counter facts the plan must respect (read from `c2-r44-gkeep-size-request.py` docstring):
- clause i+: the Gate receipts of the cited ids must cover **all five** pin names → the entry cites S164 (Window.cpp, held) + 4 new rows (S298 XDGShell, S299 xdg-shell.xml,
  S300 gdktoplevel, S301 gkeep-ui); clause c needs ≥3 new ids with opened 2026-10-26 — satisfied by the 4.
- clause h census: `gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep` and `hyprland sendWindowSize xdg_setSize=1 x11_configure=1`;
  both verbatim, own line, outside fences, once, and not claim lines (g). My own read agrees: `->setSize(` ×1 (:1753), `->configure(` ×1 (:1751) inside `sendWindowSize` (:1732-1754);
  `set_size_request(` ×0, `set_default_size(420, 500)` ×1, `application_id="org.omarchy.gkeep"` ×1.
- clause g: **every** unfenced entry line naming a cited id must carry that id's Gate quote and `<receipt>:<N>`; so each "§" claim line cites exactly one id.
- held S164: cells 1-9 byte-equal; only used-by may gain the entry path. **Caveat:** S164's locator cell (cell 6) lists `Window.cpp:103-108,141-146,1484-1486,1791-1795,2143-2281,2497`
  — none of the lines the entry would quote (1514-1528, 1685-1754, 2742-2746). The row's cells cannot be edited (clause c), so the entry's own computed locators are
  the evidence and the lesson should say the row's locator cell is incomplete for this use (same pattern as r43's S155/S158 "held rows cited").
- ids: no staged id is carried (id-guard: 42 collisions S203..S297; `collisions` file contains S216, S219, S284-S287, S292, S293; **not** S251, S255, S256, S311, S312, S318-S320, S326, S339).
  The entry must never write `S311/S312/S318…` (clause b: no non-cited S-token). The renumber map already fixes S311→S164, S312→S301 (provisional).
- Gate lines go in the lesson named by the frozen docstring (`corpus/lessons/round-44.md`, `## Gate`), not in `round-43.md` (the inherited v2 text names round-43; the round-44 preamble says to read the round-44 values).

## 4. PROVINCE fit

- PROVINCE.md (lines 3-15): the lane owns Hyprland/waybar/walker configuration plane and display behavior; probes, measures, recommends; "every claim is file-byte- or
  screenshot-verified". Compositor sizing of a client window from a host rule is in (r43 already admitted that). The configure path (Hyprland → xdg-shell → GTK) is
  upstream-source knowledge about how a host rule becomes a client size; in.
- GTK internals (gdktoplevel) are a client-toolkit surface, not an owned config plane: keep the claim narrow — "what GDK's Wayland toplevel does with a configure" as upstream
  source, not "what gkeep renders". The pins forbid more (gtkwindow.c unpinned).
- r13-r15 (journal/DEBUG sweeps): the journal and its unit state are tsukuroi-adjacent (round-43 CritAssimilation F6 says the same for r14), and `journalctl` is not among this
  round's allowed host reads. A sweep re-measurement is therefore out of reach this round; the staged numbers are un-reproducible private receipts → refuse (not "out of province").
- r31 §1 (glyph) belongs to the bar theme (r43 ledger already says so); §2 is covered.
- r9's Chinese-wiki-free; no BAD_LOC marker in r9/r12/r13 text I read, but their cited rows' cells are not mine to audit — clause i's BAD_LOC check is on the cited *rows*; the entry cites none of the localized rows.
  (I did not run the counter's BAD_LOC marker list against any row.)

## 5. Recommended decisions (lesson `## Gate` lines)

`i+` needs ≥1 ADMIT and ≥1 REFUSE with the exact path form `merge/mado/knowledge/corpus/knowledge/<file>`, a REFUSE reason ≥4 distinct words holding a flip word
(superseded|until|unless|once|when|if|after), and a REFUSE target different from the ADMIT target.

**ADMIT** `merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md` as `corpus/knowledge/hyprland-gkeep-size-request-r44.md`
— as the r44 successor of the r12 file: keep §1 (the send path) and §2 (gkeep's declarations), drop its C-c/C-d inferences (§2 above), add the pin-grounded links it lacked
(XDGShell configure emission; onAck; commitWindow's min/max clamp; xdg-shell "hint"/fullscreen-maximum; GDK adopt-and-constrain), state the open UNK (GTK widget-layer
minimum; no window observed), and keep the two census lines. Overlap with r43: none (r43 ends at the box/GOAL).

**REFUSE** (each with a flip that can fire):
1. `…/gkeep-rendered-geometry-record-r13.md` — reason: its §1 onAck is re-grounded inside the admitted entry from the pins, its map-log locator is not a claim of this
   entry, its journal measurement S320 rests on a private `lanes/mado/round13` receipt absent from this lane, and its "client cannot substitute a different number" is not supported
   (the commit-time clamp to client min/max, Window.cpp:2742-2746). Flip: if a lane row holds an in-lane journal-sweep receipt with its INFO and DEBUG controls.
2. `…/gkeep-rendered-geometry-record-r14.md` — reason: a whole-journal count (S326, private receipt) plus a store-key census no row holds; the journal is tsukuroi-adjacent ground
   and `journalctl` is outside this round's allowed reads. Flip: if a committed in-lane receipt re-measures the sweep with both controls.
3. `…/gkeep-geometry-never-recorded-r15.md` — reason: a negative census of the lane's own round-24 artifacts (S339, private receipt), and its premise "the corpus has never held an
   observation" is superseded by r43's isolated-oracle observation. Flip: if the count is re-run in the lane against a named artifact set and committed.
4. `…/gkeep-rendered-geometry-chain-r9.md` — reason: its unique link (`fetchClass`→app_id) is in the pin but outside C2's configure-path theme, its default-size semantics (S286) and
   wiki-silence claim (S287) are unpinned, and S292/S293 are private; its agreement-of-numbers point is already r43 §4. Flip: if a round pins `Window.cpp` `fetchClass` plus the
   window-rules page and writes the class-is-app_id entry (the pin Window.cpp:1502-1512 already holds the first half).
5. `…/glyph-and-geometry-r31.md` — reason: two themes; the glyph half belongs to the bar theme, the gkeep half is r43 §4, and "deterministic across window managers" has no source.
   Flip: if the weather-glyph theme is taken up with its own pinned glyph map.

**Withhold (no REFUSE line unless the L1 wants the extra decision):** `…/gkeep-element-rules-r30.md` — r43's "first candidate for the next [round]". Its flip fired
(`apps/system.conf:4`), but it is not on C2's theme, its 875×600 side has no lane row, and the rule-line half duplicates r43 §1. A REFUSE line for it would contradict the r43
ledger; if refused, say "unless a lane row registers the omarchy default `apps/system.conf`" and note the old "first candidate" is restated.

**Not to be re-decided:** `gkeep-size-to-real-size-r11.md` (admitted in r43; counter and registration forbid a second decision); `gkeep-size-rule-application-r10.md`,
`gkeep-geometry-unobservable-r8.md`, `gkeep-observation-route-r11.md` (refused r43 with flips; their flips have not fired). One nuance for the L1: the r10 refusal's
flip, "if a pinned source shows the reported size coming from the client's acknowledgement", is *worth re-reading against the new pins* — `getReportedSize()` reads
`ackedSize` (Window.cpp:1861-1866) but the ack stores the compositor's own pending size (:1526), not a client-chosen one, so the flip has **not** fired (INF). This is also D1's
open point in the routed defects (the `size` field in `clients -j` is GOAL, S158; `getReportedSize` is a different function).

## 6. Risks for the entry author / the L1

1. **S311 vs S164:** the staged S311 text cites the *tag* URL. The lane maps by document to held S164 (commit URL; sha identical), so the entry must cite `S164`, never `S311`.
2. **Counter comment-stripping:** `// apply pending size. We pinged, the window ponged.` and every `Log::` string in a `//` comment vanish before the Gate-quote search.
   Use code text (candidates above).
3. **"The compositor's own value" / "client cannot substitute"** appear in r13 and r12 — do not carry. The pins show a client-driven min/max clamp (Window.cpp:2742-2746)
   and the xdg-shell "hint" wording (xdg-shell.xml:1150-1152).
4. **GTK default-size semantics are unpinned.** Phrase "gkeep declares", never "GTK treats … as".
5. **The word "refuse" in the xdg protocol:** there is none; the only protocol "no" is a client ignoring a hint (xdg-shell.xml:1150-1152 plus maximize/fullscreen carve-outs at :841-852).
6. The r12 quote of `window = Gtk.ApplicationWindow(application=self, title="gkeep")` is real (gkeep-ui.py:474) — if re-used, escape-free quoting in the Gate line (`quote="…"`) needs care for the inner `"` characters;
   prefer `window.set_default_size(420, 500)` (:476).
7. **Not run:** the counter itself, any fixture entry, any live host read. Quote candidates were checked by a normalizing script against the pins only (not the counter's word-boundary/comment-strip
   implementation, which I did not execute); the `maximized must be obeyed` quote locator is unverified.

## 7. Tools and receipts

Only read-only coreutils/grep/python3 stdlib in the seat shell; no installs; no scratch left (no `/fast/scratch` dir was created); no git mutation (one read-only `git grep` at base:
`git grep -nE 'fetchClass|Map request dispatched|m_state\.appid|onAck|set_min_size|layoutMinSize|clampWindowSize' 6a1a905… -- corpus PROVINCE.md SKILL.md tools` → only the round-43 lesson/spotcheck
ledger lines; `git grep -ciE 'sendWindowSize|pendingSizeAcks|xdg_toplevel.configure|set_size_request'` → 0).
