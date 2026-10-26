# CritEntryClient — round 44 w2: the entry's protocol / GTK / gkeep sentences (sections 3-5, predecessor corrections)

Seat: leaf critic (no dispatch). Lane repo: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Target: `corpus/knowledge/hyprland-gkeep-size-request-r44.md` (landed at `e46789213830597348fe96a351ae004d10587385`,
base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`), sections 3-5 and "What the staged predecessor said".
Status: DONE. Every verdict below is against the pinned bytes, not against the entry's own wording.

**Method.** `check.py` (this seat) recomputes every locator from the bytes and re-verifies every quote used here;
`trace.py` transcribes the two pinned GTK functions into a branch-for-branch state machine and drives the states the
entry's universal sentences claim over; `c2-admit-at-data.log` is the frozen C2 counter re-run read-only at the data
revision. Five pins re-hashed against `receipts/fetch-sha256.txt`: **PIN-OK 5/5**. Last lines:

```
RESULT pins_bad=0 line_fails=0 quote_fails=0 count_fails=0      (verify.log, 80 line assertions + 14 quotes + 8 counts)
RESULT cases=7 fails=0                                          (trace.log)
PRED-C2-r44-v2: admitted=1/1 verdict=TARGET_MET rev=e4678921…    (c2-admit-at-data.log)
```

Four GTK 4.24.1 files were fetched into this seat dir to answer "is gkeep's window resizable" and to read the clamp;
they are **not** round-44 pins and are **not** proposed as cites inside the entry (see F2):

| file | sha256 | url |
|---|---|---|
| gtkwindow.c | `f99f6a7ef1efdd000d3268629015f1c136ef6ae4ed31abca5066d026d7896ff6` | gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/gtk/gtkwindow.c |
| gdksurface.c | `9101ce7f660a03df40d77f1412f98d49226d4b74fd75e340069f8ab53e7a62d4` | gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/gdk/gdksurface.c |
| gdktoplevelsize.c | `58708338993e392a1044cf4026a00493650fd22614e7ea5c8f8dc421955dc237` | gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/gdk/gdktoplevelsize.c |
| gtkapplicationwindow.c | `94be79f4d28f72b4bfbb9df93fc2de4f8341f6da532fab144fe64903a2ad26ff` | gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/gtk/gtkapplicationwindow.c |

## The three questions asked

1. **Is "adopts a non-zero configured size unless below its minimum" what 513-545 and 606-700 say?**
   For a **resizable** window, yes: min-only mask (490-494), constrain gate (523-528),
   `width = CLAMP (width, min_width, max_width)` (gdksurface.c:1610). For a **non-resizable** window, no:
   min and max are both set to the computed size (496-501), so the configured size is replaced even when it is far above
   the minimum → **F2**. Two deviations inside those lines: the 0x0 sentence omits the saved-size restore (656-660) →
   **F3**, and it omits that the else branch clamps too (539-547) → **F3**.
2. **Is gkeep's window really resizable, so the min-size branch applies?** **Yes** — and the entry never says it.
   `gkeep-ui.py` calls no `set_resizable` (count 0 in verify.log); GtkWindow's instance default is
   `priv->resizable = TRUE;` (gtkwindow.c:1837, documented `Windows are user resizable by default`, gtkwindow.c:5864),
   it reaches the layout at gtkwindow.c:4056, which GDK copies at gdktoplevel-wayland.c:1857 and reads at :489-490, and
   GtkApplicationWindow does not touch it (0 occurrences of `resizable` in gtkapplicationwindow.c). So for gkeep the mask
   is `GDK_HINT_MIN_SIZE` only (494) and the clamp can only raise. This premise is load-bearing and unpinned → F2.
3. **Is "the ack carries a serial only" exact?** **Yes, exact.** `xdg_surface.ack_configure` has exactly one argument,
   `serial` (xdg-shell.xml:595), inside the request opened at :560. Locator refinement only: the argument is at :595, so
   cite `560-596` (or `:595`). The substance of the predecessor correction is right: `onAck` writes the compositor's
   stored size for that serial (Hyprland-Window.cpp:1515-1521,1526), not a size the client chose.

## Sentence ledger (verdict + computed locator)

| entry line | sentence (short) | verdict | computed locator |
|---|---|---|---|
| :44 | "the configure size binds nobody" | **FALSE** → F1 | xdg-shell.xml:841-842, 852, 861 |
| :44 | hint quote `... should be resized` | TRUE but truncated mid-sentence → F5 | 1150-1152 (entry cites 1150) |
| :44 | "zero width or height leaves the dimension to the client" | TRUE | 1154-1155 (entry: 1154-1157) |
| :44 | "the states sent with it say how to interpret the size" | TRUE but understates → F1 | 1159-1161; semantics at 839-865 |
| :44 | "answers with ack_configure before it commits" | TRUE | 560-596, 562-565, 1166 |
| :44 | "that ack is what Hyprland's onAck receives" | TRUE | Hyprland-Window.cpp:184, 1514, 1515-1521 |
| :48 | "kept for the next layout" | TRUE | gdktoplevel-wayland.c:681-682, 680, 513-514 |
| :48 | "marked fixed only when maximized/fullscreen/tiled or resizing" | TRUE, but with Hyprland it is always fixed → F4 | 633-637, 680; mapping 743-744, 746-760 |
| :50 | "configured size plus shadows becomes the surface size" | TRUE | 505-511, 518-521, 530 |
| :50 | "constrained ... when the configure was not a 0x0 one" | TRUE | 664-668, 523-528 |
| :50 | "hints carry the widget tree's minimum size for a resizable window" | TRUE | 490-494; gtkwindow.c:4456-4461, 4463 |
| :50 | "0x0 ... keeps the size GTK computes itself (539-544)" | **PARTLY FALSE** → F3 | 647, 656-660, 677, 681-682; clamp at 539-547 |
| :52 | "adopts a non-zero configured size unless below its minimum" | **FALSE as universal** → F2 | 490-494 vs 496-501; gdksurface.c:1596-1611 |
| :52 | "whether Hyprland sends a tiled state ... is not read here (UNK)" | **DECIDABLE: yes** → F4 | Hyprland-XDGShell.cpp:150, 176-181, 452-455 |
| :52 | "it would only mark the size fixed, not change it" | **PARTLY FALSE** → F4 | gdktoplevel-wayland.c:532-537, 1861-1865 |
| :56 | "one undecorated application window ... default size only" | TRUE | gkeep-ui.py:474, 475, 476 |
| :56 | quote located at `:475` | TRUE bytes, wrong span → F6 | gkeep-ui.py:475-476 |
| :56 | "no set_size_request call" | TRUE | count 0 (verify.log) |
| :56 | "only min-width/min-height (87-88) in button.ink" | TRUE | gkeep-ui.py:80, 87, 88 |
| :56 | application id at `:449` | TRUE | gkeep-ui.py:449 |
| :56 | INF "default equals 420x500; minimum from the widget tree; configure and default do not compete" | TRUE as far as stated, **missing the resizable premise** → F2 | gkeep-ui.py:476; 490-494 |
| :69 | "no such toplevel request" | TRUE, keep the word "toplevel" → F8 | xdg-shell.xml:157 (positioner), 950, 990 |
| :71 | "ack_configure carries a serial only (560)" | TRUE exact; locator → F7 | 595 in request 560-596 |
| :73-75 | "GTK adopts after constraining; gkeep's minimum not measured (UNK)" | same non-resizable gap → F2 | 523-528, 496-501 |

## Findings

### F1 [MEDIUM] §3 (`:44`): "the configure size binds nobody" — three of the protocol's own states bind it
**Attacks** the entry's statement of what S299 says (`hyprland-gkeep-size-request-r44.md:44`) and the licences row at
`:21` ("the size is a hint; zero means the client decides"). This is the C2 claim's protocol element.

**Evidence.** `xdg-shell.xml:841-842`: `The window geometry specified in the configure event must be obeyed by the client`
— and :842-843 adds "or the xdg_wm_base.invalid_surface_state error is raised". Fullscreen (:851-855) and resizing
(:860-863) say `the client cannot resize beyond it` (computed occurrences :852 and :861): a maximum, not a hint. The hint
text the entry quotes (:1150) is the plain-configure rule; the state enum (:839-865) is where the size stops being
optional. The entry never says so, and its §4 UNK inherits the omission.

**Why it matters.** The entry is the round's sourced answer to "what does the protocol let the client do with the size".
As written it licenses "gkeep can ignore any configured size"; the spec says that only while no binding state is set.
It does not move the round's gkeep conclusion (Hyprland's floating configure carries no maximized/fullscreen/resizing
state — see F4 for the tiled states it does carry), but the spec sentence itself is wrong.

**Reproduction.** `python3 check.py` → rows `xdg-shell.xml:841`, `:852,861`, `:1150-1152` in `verify.log`.

**Smallest safe correction** — replace the clause, keep the rest of `:44`:
> **OBS** S299 - for a plain configure the size is a hint: `The width and height arguments specify a hint to the window
> about how its surface should be resized in window geometry coordinates` (xdg-shell.xml:1150-1152); a zero width or
> height leaves the dimension to the client (xdg-shell.xml:1154-1155), and the states sent with it say how to read the
> size (xdg-shell.xml:1159-1161) - under `maximized` the window geometry `must be obeyed by the client`
> (xdg-shell.xml:841-842), and under `fullscreen` or `resizing` the client `cannot resize beyond it`
> (xdg-shell.xml:852,861). The client answers a configure with the xdg_surface ack_configure request
> (xdg-shell.xml:560) before it commits the matching state; that ack is what Hyprland's onAck receives.

and the licences row `:21`:
> | Must the client use the configured size? | the protocol text: a plain configure's size is a hint and a zero dimension leaves it to the client; `maximized` makes it mandatory and `fullscreen`/`resizing` make it a maximum (xdg-shell.xml:839-865) | OBS (spec) |

Gate-safe: the line keeps S299's Gate quote and its computed start line 1150 (`clause=g id=S299 … locator_line=1150`
in `c2-admit-at-data.log`), and the added quotes are not id-bearing.

### F2 [MEDIUM] §4 INF (`:52`): the universal over GTK windows is false for a non-resizable one
**Attacks** `:52` sentence 1 (and, by dependence, the licences row `:22` and the predecessor bullet at `:73-75`).

**Counterexample (reachable, inside the pinned file).** For a non-resizable window, `gdktoplevel-wayland.c:496-501` sets
`geometry.max_width = geometry.min_width = size.width;` (and the same for height) with mask
`GDK_HINT_MIN_SIZE | GDK_HINT_MAX_SIZE`, so `gdk_surface_constrain_size` (`width = CLAMP (width, min_width, max_width)`,
gdksurface.c:1610) replaces **any** configured size with the computed one — above the minimum as well as below it.
`trace.py` case C: non-resizable window, min 200x150, natural 420x500, configure 600x700 → surface (420, 500); the entry's
sentence predicts 600x700. `verify.log` asserts 496-501, 500, gdksurface.c:1596-1611, 1602-1606.

**Why it matters.** The sentence is the entry's GTK conclusion; it holds only on the resizable branch, and the entry
never states that gkeep is on that branch (it is — see question 2 — but the evidence is gtkwindow.c, not a pin).

**Smallest safe correction (pin-only, no new source):**
> **INF** So a GTK 4.24.1 window adopts a non-zero configured size unless that size is below its minimum, in which case
> it is raised to the minimum - **only when the window is resizable** (gdktoplevel-wayland.c:490-494); a non-resizable
> window has its minimum and maximum both set to the computed size (gdktoplevel-wayland.c:496-501) and drops the
> configured size. gkeep calls no `set_resizable` (gkeep-ui.py:474-476), but the layout's resizable flag comes from
> GtkWindow, which is not pinned (UNK).

*(L1 decision: the premise can be established with one more receipt — `priv->resizable = TRUE;` gtkwindow.c:1837, the
documented default at :5864, `gdk_toplevel_layout_set_resizable (layout, priv->resizable)` at :4056, sha256 `f99f6a7e…`
above. Adding a sixth pinned file after the data commit is a predicate/pin change, so this seat does not propose it as
landed text; the pin-only form above needs no re-registration.)*

### F3 [LOW] §4 OBS (`:50`): the 0x0 sentence drops the saved-size restore and the else-branch clamp
**Attacks** `:50` last sentence ("A 0x0 configure is recognised as one (647) and instead keeps the size GTK computes
itself (539-544)").

**Two counterexamples in the pinned GTK code** (neither reachable on Hyprland 0.56.2 — see F4 — so this does not move
the round's window; it makes a general GTK claim incomplete):
1. A 0x0 configure arriving after maximized/fullscreen/tiled is not kept as "computed": with `saved_size && !fixed_size
   && was_fixed_size` GTK substitutes the size saved before that state — `width = wayland_toplevel->saved_width`
   (gdktoplevel-wayland.c:658); being non-zero, that size is then latched as the configured size (:681-682) with no
   constraint asked for (:677). `trace.py` case D (500x400, then 900x700 maximized, then 0x0) → surface (500, 400), not
   the computed (420, 500) the entry predicts; case E (fresh 0x0) → (420, 500), the only path the sentence describes.
   The saved size is the live surface with shadows stripped (:210-211), refused while the surface is fixed (:202-205).
2. "keeps the size GTK computes itself" is not unclamped: the else branch re-applies the same hints
   (`gdk_surface_constrain_size (&geometry, mask, …)` :545-547); the difference from the 523-528 branch is which hints
   copy is used, not whether a clamp runs.

**Reproduction.** `python3 trace.py` cases D/E; `verify.log` assertions 647, 656-660, 677, 681-682, 539-547, 197-212,
202-205, 210-211, 648-655 (GTK's own comment states the intent the entry omits).

**Smallest safe correction** — replace the last sentence of `:50`:
> A 0x0 configure is recognised as one (gdktoplevel-wayland.c:647) and keeps the size GTK computes itself, constrained
> by the same hints (gdktoplevel-wayland.c:539-547) - except when it arrives after a maximized, fullscreen or tiled
> state, where GTK restores the size it saved before that state (`width = wayland_toplevel->saved_width`,
> gdktoplevel-wayland.c:656-660), latches it as the configured size because it is non-zero
> (gdktoplevel-wayland.c:681-682) and asks for no constraint (gdktoplevel-wayland.c:677).

### F4 [MEDIUM] §4 INF (`:52`): the tiled-state UNK is decided by the entry's own pins — and fixed is sticky
**Attacks** the parenthetical "Whether Hyprland 0.56.2 sends a tiled state with a floating window's configure is not read
here (UNK; it would only mark the size fixed, not change it)."

**The pins decide it: Hyprland sends all four per-edge tiled states with every xdg_toplevel.configure.**
`CXDGToplevelResource::CXDGToplevelResource` appends `XDG_TOPLEVEL_STATE_TILED_LEFT/RIGHT/TOP/BOTTOM` for every client
binding xdg_toplevel version >= 2 (Hyprland-XDGShell.cpp:150, 176-181); the deferred application copies the whole state
list into the configure it sends (Hyprland-XDGShell.cpp:443, 452-455, `sendConfigure(m_pendingApply.size.x, …)`), and in
the pinned file nothing removes a tiled state and the list is never cleared (4 occurrences of
`XDG_TOPLEVEL_STATE_TILED`, all pushes; 5 `std::erase(m_pendingApply.states, …)` calls, none for a tiled state; no
`states.clear`, no whole-struct reset — verify.log counts). GTK maps them to `GDK_TOPLEVEL_STATE_TILED`
(gdktoplevel-wayland.c:746-760), which is one of the states that sets `fixed_size` (:633-637).

**Consequences the entry should state.** For gkeep on this compositor `size_is_fixed` is therefore true on every
configure (:680): the latched configured size is never cleared (:532-537), so a later layout that no configure caused
(`gdk_wayland_toplevel_present` sets `surface_geometry_dirty = TRUE`, :1861-1865) re-applies the last compositor size
instead of GTK's newly computed one — `trace.py` F (tiled configure, then a present with natural 600x700) → (500, 400);
G, the same without the state, → (600, 700). It also means the saved-size branch of F3 never runs for gkeep
(`!fixed_size` is never true, and `gdk_wayland_toplevel_save_size` refuses while the surface is tiled, :202-205).
"Not change it" is thus true only for the pass that consumed the configure.

**Reproduction.** `python3 check.py` rows `Hyprland-XDGShell.cpp:177,178,179,180`, `:455`, and the counts
(`XDG_TOPLEVEL_STATE_TILED` 4, `std::erase(m_pendingApply.states` 5, `states.clear` 0); `python3 trace.py` F/G.

**Smallest safe correction** — replace the parenthetical:
> **OBS** Hyprland 0.56.2 puts the four per-edge tiled states on every xdg_toplevel.configure: the toplevel constructor
> appends them for every client at version 2 or above (Hyprland-XDGShell.cpp:176-181) and the deferred application copies
> the whole list into the configure (Hyprland-XDGShell.cpp:452-455), with nothing in the file removing them. GTK 4.24.1
> therefore marks every configure from this compositor fixed (gdktoplevel-wayland.c:633-637, 746-760) and keeps the
> latched size for later layouts (gdktoplevel-wayland.c:532-537), so a tiled state does change a later pass even though
> it does not change the size of the pass that consumed the configure.

### F5 [LOW] §3 quote (`:44`) ends mid-sentence and drops the coordinate space
The entry quotes up to "resized" (computed 1150-1151) and closes the quote, while the sentence continues
`in window geometry coordinates. See set_window_geometry.` (computed 1150-1152). The dropped qualifier is load-bearing
inside the same entry: GTK adds the shadow margins to the configured size (:518-521) precisely because the configure is
in window geometry coordinates. **Correction:** quote `... how its surface should be resized in window geometry
coordinates` (xdg-shell.xml:1150-1152, 22 words) — folded into F1's replacement. Gate-safe: the 18-word S299 Gate quote
(`corpus/lessons/round-44.md:33`) stays a prefix of the 22-word quote with the same computed start line, so clause g
still holds, and 22 words is inside clause d's 3-25 range if the lesson quote is extended too.

### F6 [LOW] §5 quote/locator (`:56`): two statements quoted as one, located at `:475`
`window.set_decorated(False) window.set_default_size(420, 500)` is lines **475 and 476** (computed span 475-476); the
entry cites `:475`. The bytes are right under the house whitespace normalization (the C2 counter's `quote_at` returns
475), but the round-43 precedent cites the span for a two-line concatenation
(`corpus/knowledge/hyprland-gkeep-geometry-r43.md:62`, `(gkeep-ui-excerpt.py:33-34)`). **Correction:** cite
`(gkeep-ui.py:475-476)`. Gate-safe: clause g's locator check is `re.search(r"(?<![\w.-])NAME:AT(?!\d)", …)`
(counter:617,621), so `gkeep-ui.py:475-476` still matches the computed start line 475 — observed as
`clause=g id=S301 … locator_line=475` in `c2-admit-at-data.log`.

### F7 [PASS] "the ack carries a serial only" — exact; locator refinement
`<request name="ack_configure">` at :560 holds one `<arg name="serial" type="uint" …>` at :595 and no other argument;
"must make an ack_configure request sometime before the commit request" (:562-565), "must send an ack_configure"
(:1166). Hyprland's side is as the entry says: listener at Hyprland-Window.cpp:184, `onAck` takes the newest pending pair
whose serial is not after the ack (:1515), erases it and every older pair (:1521) and writes the stored size (:1526).
Only refinement: cite `xdg-shell.xml:560-596` (or `:595`) rather than `:560`, which alone is the request declaration.

### F8 [PASS, keep the wording] predecessor bullet 1
`set_size` exists in the file only for `xdg_positioner` (xdg-shell.xml:157); `xdg_toplevel` offers `set_max_size`
(:950) and `set_min_size` (:990). The bullet's phrase "no such **toplevel** request" is therefore precise, and a later
editor must keep the word "toplevel": dropping it turns a true sentence into a false one against :157.

## Passes worth recording (no change)

- `:48` first OBS: kept for the next layout (:681-682), the flag assigned at :680 from `fixed_size` (:633-637), whose
  `tiled`/`resizing` inputs are real mappings (:746-760, :743-744) — with F4, the fixed path is the one gkeep is on.
- `:50` shadow sentence: capture at :505-511, addition at :518-521, applied at :530; hints are exported shadow-subtracted
  (:1301-1306, :1333-1334) and `GdkToplevelSize`'s minimum is a toplevel minimum (gdktoplevelsize.c:114), so clamping a
  shadow-inclusive size by it is coherent, not a double count. For gkeep, `set_decorated(False)` zeroes GTK's shadow
  (gtkwindow.c:4182-4183, :4206), so the addition is a no-op — a strengthening the entry cannot cite without a sixth pin.
- `:56`: one `Gtk.ApplicationWindow` construction (:474), `set_decorated(False)` (:475), `set_default_size(420, 500)`
  (:476), `set_size_request(` count 0, `application_id="org.omarchy.gkeep"` (:449), and the only `min-*` CSS inside
  `button.ink` (:80, :87-88). "one undecorated application window" and "declares a default size only" hold.
- Counter/predicate: no new predicate hole. The frozen counter admits the entry at the data revision
  (`c2-admit-at-data.log`: `admitted=1/1 verdict=TARGET_MET`), so F1/F3 pass the gate exactly as its declared residual
  says ("clause j binds a locator and a keyword per surface, not the truth of the sentence around them",
  `quality/counters/c2-r44-gkeep-size-request-v2.py:65-68`). These are entry-text fixes for the L1, not an OPEN
  predicate defect, and nothing here needs a re-registration.

## What this review does not establish

- That nothing outside the pinned `Hyprland-XDGShell.cpp` clears the state list: within the pinned file it is never
  cleared and no code removes a tiled state, but the class header is not a round-44 pin.
- Whether gkeep's widget-tree minimum is below 420x500 — unchanged UNK; no live window, and a GTK client on the host
  session is forbidden by the seat rules.
- The rendered geometry — unchanged UNK; no gkeep window was opened.
- Any GTK other than 4.24.1, any Hyprland other than 0.56.2 at `efb5099`, any gkeep other than `133b867`.

## Safety / tool state

- Wrote only inside `.ufo/waves/round-44/w2/CritEntryClient/` and the report file; no tracked file, counter, control,
  registration, pin, README, corpus file or index was edited. No git/jj mutation (read-only `git`/counter reads only);
  no pacman; no compositor command; no host service; no Wayland client.
- No tool installed (python3 stdlib, plus `curl` for four GTK 4.24.1 raw files with the hashes above).
- Scratch `/fast/scratch/hyaku/mado-r44/CritEntryClient/` was created empty and removed before yield; every citable
  artefact is in this seat dir.

Artefacts: `check.py`, `verify.log`, `trace.py`, `trace.log`, `c2-admit-at-data.log`, `gtkwindow.c`, `gdksurface.c`,
`gdktoplevelsize.c`, `gtkapplicationwindow.c`.
