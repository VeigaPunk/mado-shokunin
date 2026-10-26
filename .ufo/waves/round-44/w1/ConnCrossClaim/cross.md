# Cross-claim matrix: C1 (operability) × C2 (coverage) — round 44 w1

Seat `ConnCrossClaim`, 2026-10-26. Lane `mado-shokunin`, freeze commit
`e2289516a9a857f55cda7be635933e89b931c3da`, base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`.
All pin line numbers computed with `grep -n`/`sed` against the frozen bytes
(sha256 in `.ufo/waves/round-44/receipts/fetch-sha256.txt`); both counters run
once each (receipts `cross-c1-ref-run.txt`, `cross-c2-base-run.txt`,
`cross-separability-grep.txt` in this dir).

Sources: C1 pins `.ufo/waves/round-44/fetch-c1/` (FullscreenController.hpp,
FullscreenHandler.cpp, HyprCtl.cpp — Hyprland @ efb50993780079460b0cbed1363e2166a2de1d9f);
C2 pins `.ufo/waves/round-44/fetch/` (Hyprland-Window.cpp, Hyprland-XDGShell.cpp @
efb5099, xdg-shell.xml 1.49, gdktoplevel-wayland.c 4.24.1, gkeep-ui.py @ 133b867).

## 1. Claims-vs-sources matrix

### 1a. C1 contract sentences (reference `c1/ctl-ref-tool.py.txt` docstring + `PRED-C1-r44` docstring) × fetch-c1 pins

| # | C1 sentence | fetch-c1 evidence | status |
|---|-------------|-------------------|--------|
| C1-s1 | fsmode = the `fullscreen` value when a JSON integer 1 or 2 (not bool, not float), else 0 | `Hyprland-FullscreenController.hpp:12-15` `enum eFullscreenMode : int8_t { FSMODE_NONE = 0, FSMODE_MAXIMIZED, FSMODE_FULLSCREEN }`; `Hyprland-HyprCtl.cpp:431` prints `sc<uint8_t>(...getFullscreenModes(w).internal)` into the `"fullscreen"` slot of the clients JSON (`:410`) | supported |
| C1-s2 | verdict order BADSIZE \| FULLSCREEN(2) \| MAXIMIZED(1) \| TILED \| AGREE \| DIFFER | enum order at `FullscreenController.hpp:13-15` (1 = maximized, 2 = fullscreen); `:34-35` shows `internal`/`client` are distinct slots, matching the fixture `fsclient0` guard (tool must read `fullscreen`, not `fullscreenClient`; ref tool `client_fsmode` at `ctl-ref-tool.py.txt:195-199`) | supported |
| C1-s3 | summary carries ` maximized=<n> fullscreen=<n>` before ` verdict=` iff maximized+fullscreen > 0, else round-43 line byte-identical | output contract; no pin needed | format clause |
| C1-s4 | TILED narrowed: pseudo-tiled clients take their size from stored pseudo size; dump carries no pseudo field | closure defect D3 (round-43 lesson), not a pin fact | supported by closure text |
| C1-s5 | "Hyprland 0.56.2 sets a maximized window's box to the workspace work area and a fullscreen window's box to the monitor box … and remembers the floating size for later" | `Hyprland-FullscreenHandler.cpp:192-198` — `FSMODE_FULLSCREEN` → `MONBOX = MONITOR->logicalBox()`, `setPositionGlobal(MONBOX)`; `FSMODE_MAXIMIZED` → `WORKAREA = WORKSPACE->m_space->workArea(...)`, `setPositionGlobal(WORKAREA)`; `:131` `target->rememberFloatingSize(target->position().size())` | supported |
| C1-s6 | "`hyprctl clients -j` prints the internal mode as the integer `fullscreen`" | `Hyprland-HyprCtl.cpp:431` `.internal` (vs `:432` `.client`) | supported |

### 1b. C2 planned claims (registration + `PRED-C2-r44` docstring) × fetch pins

| # | C2 claim | fetch evidence | status |
|---|----------|----------------|--------|
| C2-s1 | after the box is set: `CWindow::sendWindowSize` → `realToReportSize` → xdg `setSize` → `scheduleConfigure` | `Hyprland-Window.cpp:1732-1754` (sendWindowSize body), `:1741` `REPORTSIZE = realToReportSize()`, `:1753` `m_pendingSizeAcks.emplace_back(m_xdgSurface->m_toplevel->setSize(REPORTSIZE), ...)`, `:1685-1687` `realToReportSize` xdg branch returns `m_realSize->goal().clamp(...)`; `Hyprland-XDGShell.cpp:354-358` `CXDGToplevelResource::setSize` sets `m_pendingApply.size`, calls `m_owner->scheduleConfigure()` returning the serial; `:629` `CXDGSurfaceResource::scheduleConfigure` | supported |
| C2-s2 | the pending-size-ack list and `onAck` | `Hyprland-Window.cpp:184` ack listener → `onAck(d)`; `:1514-1521` `onAck(uint32_t serial)` searches `m_pendingSizeAcks` reversed, sets `m_pendingSizeAck`, `std::erase_if(...)`; `:1523-1524` X11 early-return | supported |
| C2-s3 | the X11 `configure` branch | `Hyprland-Window.cpp:1751` `m_xwaylandSurface->configure({REPORTPOS, REPORTSIZE})` (one `->configure(` inside sendWindowSize); `realToReportSize` X11 branch `:1688-1697` (clamp `{1,1}`, `xwayland:force_zero_scaling` scale-and-round) | supported |
| C2-s4 | what xdg-shell 1.49 lets a client do with a configure size | `xdg-shell.xml:1150` "The width and height arguments specify a hint to the window" (21 words); `:1154-1156` zero w/h ⇒ client decides its own dimension; `:1166` "Clients must send an ack_configure in response to this event" | supported |
| C2-s5 | what GTK 4.24.1's Wayland toplevel does with it | `gdktoplevel-wayland.c:606-706` `gdk_wayland_toplevel_handle_configure`: fixed_size = MAXIMIZED/FULLSCREEN/TILED or resizing (`:634-637`); w,h>0 → `should_constrain = TRUE`, `size_is_fixed = fixed_size` (`:666-680`); 0x0 after fixed → restore `saved_width/saved_height` (`:648-657` comment + `:658-662`); client ack at `:706` `xdg_surface, ack_configure, ...` | supported |
| C2-s6 | what gkeep 133b867 declares | `gkeep-ui.py:476` `window.set_default_size(420, 500)` (exactly one); `:449` `application_id="org.omarchy.gkeep"`; zero `set_size_request(` occurrences in the 14639-byte pin | supported |

## 2. Q1 — one fact both claims rest on: consistent?

**The shared fact is the compositor's goal box for the gkeep window.** It is the
operand of both claims, from opposite ends:

- C1's tool joins the rule `size 420 500` against the `size` field of
  `hyprctl clients -j`, and that field is the goal box:
  `Hyprland-HyprCtl.cpp:427-428` prints
  `sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x/.y)`.
- C2's chain is what the compositor does with the same box after setting it:
  `sendWindowSize` reports `REPORTSIZE = realToReportSize()`
  (`Hyprland-Window.cpp:1741`), and for an xdg toplevel `realToReportSize`
  returns `m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX)`
  (`Hyprland-Window.cpp:1685-1687`) — i.e. the goal size, clamped only at zero.

Consistency, both ways:

- Same quantity, same direction: the number the dump shows is the number the
  compositor hands the client via `setSize` (xdg) or `configure` (X11). When
  the internal mode is fullscreen/maximized, `setTargetSizeAndPosition`
  (`FullscreenHandler.cpp:192-198`) rewrites the goal to the monitor box / work
  area, so *both* the `clients -j` size C1 reads and the size C2's chain
  transmits are the monitor/work-area box. The two claims cannot disagree about
  the value without one of the pinned files being wrong at the same commit.
- Cross-source numeric echo: the C1 fixtures embed
  `windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$`
  (`quality/counters/c1-r44-geometry-states.py:179`) — the same 420×500 gkeep
  itself declares at `gkeep-ui.py:476`. Consistent; the rule size and the
  client default coincide by construction, which is what makes the round-43
  happy-path `AGREE` meaningful.

Boundaries of the shared fact (where "same value" stops):

- xdg vs X11 reporting: `realToReportSize` clamps X11 at `{1,1}` and applies
  the `xwayland:force_zero_scaling` scale-and-round (`Window.cpp:1688-1697`),
  while `clients -j` prints the raw goal cast via `sc<int>` with no clamp and
  no scale conversion. Divergence is reachable only for X11 clients and only at
  fractional/scale boundaries; gkeep is an xdg toplevel, so for the gkeep
  theme the two reads coincide.
- The identity `size(GEOMETRIC_GOAL) == m_realSize->goal()` is not itself in
  the pinned bytes: the `CWindow::size(...)` accessor lives in a header that is
  not among the round-44 pins (grep for `GEOMETRIC_GOAL` in the pinned
  `Hyprland-Window.cpp` returns nothing). Marked [INFERENCE] from the goal
  naming; neither counter checks it, and no claim sentence needs it beyond the
  informal "same box" framing.

## 3. Q2 — contradiction search

No hard contradiction found between the two claims, nor between either claim
and the other claim's pins. All six Hyprland pins (fetch-c1's three + fetch's
two Hyprland files) sit at commit efb50993780079460b0cbed1363e2166a2de1d9f per
`receipts/fetch-sha256.txt`, so there is no version skew to contradict through.
Three near-misses, stated rather than smoothed:

1. **Synthetic fixture vs live behavior (C1 internal).** Fixture `fsagree0`
   (`c1-r44-geometry-states.py`) posits a dump with `fullscreen: 2` and
   `size: [420,500]` and the C1 model resolves it to FULLSCREEN ("the reported
   size says nothing about the rule"), while the pinned
   `FullscreenHandler.cpp:192-198` says a live fullscreen window's goal is the
   monitor box. Not a contradiction: fixtures are synthetic dumps, the pins
   describe live compositor behavior, and the registration's residual note says
   exactly that the live-box fact is "the pinned source's fact, not scored".
   The scopes are disjoint by design.
2. **Spec permission vs compositor behavior (cross C2↔C1's why).** xdg-shell
   1.49 (`xdg-shell.xml:1150-1156`) makes the configure size a *hint* and
   reserves 0×0 for "the client should decide its own window dimension";
   Hyprland's `sendWindowSize` never emits a 0×0 configure for a mapped window
   (the goal is clamped at ≥0 for xdg, ≥1 for X11 — `Window.cpp:1685-1697`) and
   GTK fixes its surface to any non-zero configured size (`gdktoplevel-wayland.c:666-680`).
   Spec-permit vs compositor-do is not a contradiction (the spec permits, it
   does not require 0×0), but it is the riskiest sentence in the planned C2
   entry: wording that upgrades the hint to a client obligation ("the client
   must draw at the configured size") would overstate `xdg-shell.xml:1150` and
   be falsifiable from the same pin.
3. **X11 clamp divergence** (item in §2): `clients -j` and `sendWindowSize`
   can print different values for an X11 client under
   `xwayland:force_zero_scaling`. Unreachable for gkeep (xdg); flagged so the
   C2 entry does not generalize "sendWindowSize reports the goal size" to X11
   without the clamp caveat (`Window.cpp:1688-1697`).

## 4. Q3 — does C1's FULLSCREEN verdict need a C2 fact, or vice versa?

Neither direction.

- **C1 needs no C2 fact.** The FULLSCREEN/MAXIMIZED verdicts rest only on
  fetch-c1: the enum (`FullscreenController.hpp:12-15`), the
  `.internal`-as-`fullscreen` print (`HyprCtl.cpp:431`), and — for the
  docstring's why — `setTargetSizeAndPosition` (`FullscreenHandler.cpp:192-198`)
  plus `rememberFloatingSize` (`:131`). Nothing in C1's contract or counter
  reads `sendWindowSize`, `m_pendingSizeAcks`, `xdg-shell.xml`, the GTK pin, or
  `gkeep-ui.py`. The C2 chain (what the compositor tells the client after
  setting the box) is downstream of everything C1 scores.
- **C2 needs no C1 fact that is gate-checked.** C2's scored sentences bind only
  to the five fetch/ pins (its `PINS` dict, `c2-r44-gkeep-size-request.py:167-173`;
  `host_census` recomputes its two census lines from `gkeep-ui.py` and
  `Hyprland-Window.cpp` alone, `:382-407`). The narrative antecedent "after
  Hyprland sets the gkeep window's box" is framing, not a gate. And the
  separation is enforced, not merely observed: a C2 `GATE` line citing a
  fetch-c1 file fails `pin_ok`, because the counter requires
  `path == ".ufo/waves/round-44/fetch/" + basename` and the basename to be in
  `PINS` (`c2-r44-gkeep-size-request.py:495-499`), which excludes all of
  fetch-c1. So a C2 sentence needing a fetch-c1 quote would be unscorable by
  construction.
- **Cross-claim numeric coupling is load-bearing but not scored:** the C1
  fixture rule 420×500 (`c1-r44-geometry-states.py:179`) and gkeep's
  `set_default_size(420, 500)` (`gkeep-ui.py:476`) are the same numbers from
  independent sources; if gkeep's default ever changed, C1 fixtures would keep
  passing (their `want` is synthetic) while C2's clause-h census line is
  recomputed from the pinned bytes, so the two cannot silently drift apart.

## 5. Q4 — separability, shown with greps and one run each

Grep evidence (full transcript `cross-separability-grep.txt`):

- **C1's counter reads no knowledge file.** The only `corpus|knowledge|
  SOURCES|README|LESSON|fetch` hit in `c1-r44-geometry-states.py` is the
  docstring prose at line 14; at runtime the only bytes it opens are the tool
  under test (`:336` `open(args.tool, "rb")` or `git show rev:tools/mado-geometry.py`)
  and the scratch copies it writes (`:351`). The imported round-42 counter
  (`c1-r42-geometry.py`) likewise reads only the tool (`:963/:965`); it has no
  knowledge/corpus references at all. Its fixtures build rules text in-memory
  (`GKCONF` at `:179`); it never opens `fetch-c1/` — the pins are cited by
  docstring only.
- **C2's counter runs no tool.** `grep -nE 'mado-geometry|tools/|c1-r4'
  quality/counters/c2-r44-gkeep-size-request.py` exits 1 (no match); the only
  `subprocess` use is `git -C repo ...` (`:194`), with no `importlib`/`exec`.
  It scores an entry, the registry, the lesson gate and the README index — no
  executable under test exists in its world.

One run each:

- C1 with the reference tool:
  `python3 -I quality/counters/c1-r44-geometry-states.py --repo . --rev e2289516… --tool .ufo/waves/round-44/c1/ctl-ref-tool.py.txt --work /fast/scratch/hyaku/mado-r44/ConnCrossClaim`
  → `fixtures=26/26 … verdict=TARGET_MET`, clauses `a:1 b:1 b4:1 g:1 r:1`,
  exit 0; clause r shows the round-43 counter still `PRED-C1-r42: fixtures=37/37 … TARGET_MET`
  on the same bytes (receipt `cross-c1-ref-run.txt`).
- C2 on the base:
  `python3 -I quality/counters/c2-r44-gkeep-size-request.py --repo . --rev 6a1a905… --base 6a1a905…`
  → `admitted=0/1 verdict=TARGET_MISSED`, all clauses 0, exit 1
  (receipt `cross-c2-base-run.txt`).

Both ran without the other claim's artifact existing: the C1 run needed only
the tool bytes and the r42 counter; the C2 run needed only git objects at base.
**Either lands without the other** — matching the registration's §Separability
sentence, now with mechanical evidence.

## 6. One bounded cross-claim move (connector output)

Axis touched: C2 coverage only; C1 operability untouched; no instrument edited.

The C2 entry's highest-risk sentence is the spec-generalization of the shared
fact: §3 item 2 shows the pinned xdg-shell text licenses only a *hint*, while
the pinned GTK text shows obedience. **Proposed move:** in
`corpus/knowledge/hyprland-gkeep-size-request-r44.md`, bind every
"client-surface-size" sentence to the GTK pin (`gdktoplevel-wayland.c:606-706`,
behavioral fact) and keep the xdg-shell pin (`xdg-shell.xml:1150-1166`) for the
permission/obligation sentence only (must `ack_configure`; size is a hint;
0×0 ⇒ client decides) — never the reverse. Risk if unheeded: a w2 falsifier
quotes `xdg-shell.xml:1150` ("specify a hint") against any "must draw at the
configured size" wording and the admission dies on its own pins; the fix costs
one sentence and no counter change. Verification: entry draft, then
`python3 -I quality/counters/c2-r44-gkeep-size-request.py --repo . --rev <data-commit>`
(the counter already enforces quote-to-pin binding for exactly this).
