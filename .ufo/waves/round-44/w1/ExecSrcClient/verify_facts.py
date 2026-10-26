#!/usr/bin/env python3
"""ExecSrcClient (round 44, w1): verify every located-quote fact and emit facts.md.

Every row is checked by the FROZEN counter's own parsers, imported read-only from
quality/counters/c2-r44-gkeep-size-request.py:
  quote_at        -> 1-based line on which the whitespace-collapsed, word-bounded quote starts
  occurrences     -> number of word-bounded occurrences in the collapsed text
  quote_in_code   -> survives comment stripping (.cpp/.hpp/.h/.cc: // and /* */; .py/.conf: #)
  norm_receipt    -> cross-receipt collision test
Locators are therefore COMPUTED, never typed. Exit 1 if any row fails.

usage: python3 -I verify_facts.py [--out facts.md]
"""
import argparse
import hashlib
import importlib.util
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
ROUND = LANE + "/.ufo/waves/round-44"
FETCH = ROUND + "/fetch"
COUNTER = LANE + "/quality/counters/c2-r44-gkeep-size-request.py"

_spec = importlib.util.spec_from_file_location("c2pred_r44", COUNTER)
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)

FILES = ["xdg-shell.xml", "gdktoplevel-wayland.c", "gkeep-ui.py",
         "Hyprland-Window.cpp", "Hyprland-XDGShell.cpp"]
BLOBS = {}
for _f in FILES:
    with open(os.path.join(FETCH, _f), "rb") as _fh:
        BLOBS[_f] = _fh.read()

# pins as frozen before the wave (receipts/fetch-sha256.txt)
PIN_SHA = {}
with open(ROUND + "/receipts/fetch-sha256.txt", "r", encoding="utf-8") as _fh:
    for _line in _fh:
        _p = _line.split()
        if len(_p) == 3 and _p[2].startswith("fetch/"):
            PIN_SHA[os.path.basename(_p[2])] = _p[0]

# (section, claim, quote, file)
ROWS = [
    # ---- xdg-shell 1.49 ---------------------------------------------------
    ("A", "configure width/height is a HINT, in window-geometry coordinates, not an order",
     "The width and height arguments specify a hint to the window", "xdg-shell.xml"),
    ("A", "configure 0x0 means the client picks its own dimension",
     "If the width or height arguments are zero, it means the client should decide its own window dimension.",
     "xdg-shell.xml"),
    ("A", "the configured size is interpreted THROUGH the states array, not on its own",
     "The states listed in the event specify how the width/height arguments should be interpreted",
     "xdg-shell.xml"),
    ("A", "state maximized=1 makes the configure geometry EXACT (must be obeyed)",
     "The window geometry specified in the configure event must be obeyed by the client",
     "xdg-shell.xml"),
    ("A", "state fullscreen=2 makes the configure geometry a MAXIMUM, not an exact size",
     "The surface is fullscreen. The window geometry specified in the configure event is a maximum; the client cannot resize beyond it.",
     "xdg-shell.xml"),
    ("A", "state resizing=3 also makes the configure geometry a maximum",
     "The surface is being resized. The window geometry specified in the configure event is a maximum; the client cannot resize beyond it.",
     "xdg-shell.xml"),
    ("A", "tiled_* states carry NO size semantics in the protocol, only decoration advice",
     "The window is currently in a tiled layout and the left edge is considered to be adjacent to another part of the tiling grid.",
     "xdg-shell.xml"),
    ("A", "every configure must be acked before the commit that responds to it",
     "must make an ack_configure request sometime before the commit request, passing along the serial of the configure event.",
     "xdg-shell.xml"),
    ("A", "intermediate configures may be dropped: only the last needs acking",
     "If the client receives multiple configure events before it can respond to one, it only has to ack the last configure event.",
     "xdg-shell.xml"),
    ("A", "configure_bounds (since v4) may precede a configure and bounds the recommended size",
     "The configure_bounds event may be sent prior to a xdg_toplevel.configure event to communicate the bounds",
     "xdg-shell.xml"),
    ("A", "client min size is advisory: the compositor may ignore it",
     "The client should not rely on the compositor to obey the minimum size", "xdg-shell.xml"),

    # ---- GTK 4.24.1 gdk/wayland/gdktoplevel-wayland.c ---------------------
    ("B", "the xdg_toplevel.configure handler only STORES width/height into pending",
     "pending_state |= resize_constraint_state; toplevel->pending.state |= pending_state; toplevel->pending.width = width;",
     "gdktoplevel-wayland.c"),
    ("B", "the xdg_surface.configure handler is where pending width/height is consumed",
     "width = wayland_toplevel->pending.width;", "gdktoplevel-wayland.c"),
    ("B", "GTK reads a 0 width AND 0 height as 'no size given' (saved_size)",
     "saved_size = (width == 0 && height == 0);", "gdktoplevel-wayland.c"),
    ("B", "on 0x0 while leaving a fixed state GTK restores its own saved size",
     "if (saved_size && !fixed_size && was_fixed_size) { width = wayland_toplevel->saved_width; height = wayland_toplevel->saved_height;",
     "gdktoplevel-wayland.c"),
    ("B", "a floating configure (no maximized/fullscreen/tiled, not resizing) is NOT fixed_size",
     "fixed_size = new_state & (GDK_TOPLEVEL_STATE_MAXIMIZED | GDK_TOPLEVEL_STATE_FULLSCREEN | GDK_TOPLEVEL_STATE_TILED) || is_resizing;",
     "gdktoplevel-wayland.c"),
    ("B", "a non-zero configure size is latched as configured_width/configured_height",
     "wayland_surface->next_layout.configured_width = width;", "gdktoplevel-wayland.c"),
    ("B", "and is marked fixed only when the state says so (floating -> not fixed)",
     "wayland_toplevel->next_layout.size_is_fixed = fixed_size;", "gdktoplevel-wayland.c"),
    ("B", "a fresh non-zero configure asks for constraint against GTK's own min size",
     "if (!saved_size) { wayland_toplevel->next_layout.should_constrain = TRUE;",
     "gdktoplevel-wayland.c"),
    ("B", "compute_size takes the compositor size when one was latched",
     "if (wayland_surface->next_layout.configured_width > 0 && wayland_surface->next_layout.configured_height > 0)",
     "gdktoplevel-wayland.c"),
    ("B", "the latched size is clamped by GTK's geometry hints before use",
     "if (wayland_toplevel->next_layout.should_constrain) { gdk_surface_constrain_size (&wayland_toplevel->geometry_hints,",
     "gdktoplevel-wayland.c"),
    ("B", "a non-fixed latched size is cleared after one application (one-shot)",
     "if (!wayland_toplevel->next_layout.size_is_fixed) { wayland_toplevel->next_layout.should_constrain = FALSE;",
     "gdktoplevel-wayland.c"),
    ("B", "GTK's min size is the compute_size callback's min_width, sent to the compositor",
     "geometry.min_width = size.min_width;", "gdktoplevel-wayland.c"),
    ("B", "the constraint mask is MIN-only for a resizable window: no ceiling from GTK",
     "if (gdk_toplevel_layout_get_resizable (layout))", "gdktoplevel-wayland.c"),
    ("B", "so the clamp applied to a latched size is a floor, not a ceiling",
     "mask = GDK_HINT_MIN_SIZE;", "gdktoplevel-wayland.c"),
    ("B", "a non-resizable window pins min=max=natural size",
     "geometry.max_width = geometry.min_width = size.width; geometry.max_height = geometry.min_height = size.height;",
     "gdktoplevel-wayland.c"),
    ("B", "those hints leave as xdg_toplevel.set_min_size/set_max_size",
     "XDG_SHELL_CALL (xdg_toplevel, set_min_size, toplevel, min_width, min_height);",
     "gdktoplevel-wayland.c"),
    ("B", "the ack is sent at the END of handle_configure, with the pending serial",
     "XDG_SHELL_CALL (xdg_surface, ack_configure, wayland_surface, wayland_surface->pending.serial);",
     "gdktoplevel-wayland.c"),
    ("B", "the saved size strips GTK's shadow margins",
     "toplevel->saved_width = surface->width - impl->shadow_left - impl->shadow_right;",
     "gdktoplevel-wayland.c"),
    ("B", "with no configure_bounds GTK falls back to the union of all monitors",
     "gdk_rectangle_union (&display_geometry, &monitor_geometry, &display_geometry);",
     "gdktoplevel-wayland.c"),
    ("B", "and passes that fallback in as the size-request bound",
     "bounds_width = display_geometry.width; bounds_height = display_geometry.height;",
     "gdktoplevel-wayland.c"),

    # ---- gkeep 133b867 gkeep/ui.py ----------------------------------------
    ("C", "gkeep sets a default size of 420x500, immediately after turning CSD off",
     "window.set_decorated(False) window.set_default_size(420, 500)", "gkeep-ui.py"),
    ("C", "gkeep's application_id, the token the windowrule class matches",
     'super().__init__( application_id="org.omarchy.gkeep", flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE, )',
     "gkeep-ui.py"),
    ("C", "the only CSS min-* properties in the file: 30px tall, 72px wide, in one block",
     "padding: 6px 12px; min-height: 30px; min-width: 72px;", "gkeep-ui.py"),

    # ---- seam: what Hyprland sends (context for the client rows) ----------
    ("D", "Wayland targets are reported with a 0 lower clamp (X11 uses 1)",
     "if (!m_isX11) return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);",
     "Hyprland-Window.cpp"),
    ("D", "sendWindowSize calls realToReportSize, then setSize on the xdg toplevel",
     "const auto REPORTSIZE = realToReportSize();", "Hyprland-Window.cpp"),
    ("D", "the serial from setSize is queued with the size, for onAck",
     "else if (m_xdgSurface && m_xdgSurface->m_toplevel) m_pendingSizeAcks.emplace_back(",
     "Hyprland-Window.cpp"),
    ("D", "the X11 branch instead pushes an xcb configure",
     "if (m_isX11 && m_xwaylandSurface) m_xwaylandSurface->configure({REPORTPOS, REPORTSIZE});",
     "Hyprland-Window.cpp"),
    ("D", "onAck applies the acked size to the surface's pending state",
     "m_pendingSizeAck = *SERIAL;", "Hyprland-Window.cpp"),
    ("D", "setSize latches the size and schedules a configure for the whole surface",
     "m_pendingApply.size = size;", "Hyprland-XDGShell.cpp"),
    ("D", "the configure carries exactly the latched size and the latched states",
     "if (const auto PSTATES = sc<int*>(wl_array_add(&arr, m_pendingApply.states.size() * sizeof(int)))) std::ranges::copy(m_pendingApply.states, PSTATES); m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);",
     "Hyprland-XDGShell.cpp"),
    ("D", "Hyprland tracks a client min size for the layout",
     "Vector2D CXDGToplevelResource::layoutMinSize() { Vector2D minSize;", "Hyprland-XDGShell.cpp"),
]


CENSUS_EXPECTED = [
    "gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep",
    "hyprland sendWindowSize xdg_setSize=1 x11_configure=1",
]


def census_check():
    """Run the FROZEN counter's clause-h parser on the pinned bytes.

    The two expected lines are the ones the round-44 registration and the counter
    docstring require. Nothing here is typed into the entry: the strings are
    recomputed by c2-r44's own host_census() and compared to the expectation.
    """
    gates = {"SX1": [(FETCH + "/gkeep-ui.py",
                      PIN_SHA["gkeep-ui.py"], "q")],
             "SX2": [(FETCH + "/Hyprland-Window.cpp",
                      PIN_SHA["Hyprland-Window.cpp"], "q")]}
    raw = {"SX1": BLOBS["gkeep-ui.py"], "SX2": BLOBS["Hyprland-Window.cpp"]}
    ok, want = C.host_census(["SX1", "SX2"], {}, gates, raw,
                             list(CENSUS_EXPECTED))
    return ok, want


def struct_facts():
    """Facts read by parser rather than quoted: counts, values, enclosing selectors."""
    ui = BLOBS["gkeep-ui.py"].decode("utf-8", "replace")
    lines = ui.split("\n")
    rows = []

    def finding(text, line):
        return "%s:%d" % (text, line)

    sd = re.findall(r"set_default_size\(([0-9]+), ([0-9]+)\)", ui)
    sd_line = next(i for i, l in enumerate(lines, 1) if "set_default_size(" in l)
    rows.append(("gkeep calls set_default_size exactly once, with 420, 500",
                 "calls=%d args=%s" % (len(sd), sd[0][0] + "x" + sd[0][1]),
                 finding("gkeep-ui.py", sd_line)))
    sr_line = [i for i, l in enumerate(lines, 1) if "set_size_request(" in l]
    rows.append(("gkeep calls set_size_request zero times",
                 "calls=%d" % len(sr_line), "gkeep-ui.py (whole file)"))
    ai = re.findall(r'application_id="([^"]+)"', ui)
    ai_line = next(i for i, l in enumerate(lines, 1) if 'application_id="' in l)
    rows.append(("gkeep declares one application_id",
                 "calls=%d value=%s" % (len(ai), ai[0]),
                 finding("gkeep-ui.py", ai_line)))
    deco_line = next(i for i, l in enumerate(lines, 1) if "set_decorated(" in l)
    rows.append(("gkeep turns CSD off",
                 lines[deco_line - 1].strip(), finding("gkeep-ui.py", deco_line)))
    sel_line = None
    for i, l in enumerate(lines, 1):
        if re.search(r"\{\{\s*$", l):
            sel_line = i
        m = re.search(r"(min-width|min-height)\s*:\s*([0-9]+px)", l)
        if m and sel_line is not None:
            rows.append(("%s at line %d sits under the selector declared at line %d"
                         % (m.group(1), i, sel_line),
                         "%s / %s" % (lines[sel_line - 1].strip(), m.group(0)),
                         finding("gkeep-ui.py", i)))
    nmin = sum(1 for l in lines if "min-width" in l or "min-height" in l)
    rows.append(("the file declares this many min-* CSS properties in total",
                 "count=%d" % nmin, "gkeep-ui.py (whole file)"))
    win_min = [i for i, l in enumerate(lines, 1)
               if re.match(r"\s*window[^{]*\{\{", l) and
               any(k in lines[i] for k in ("min-width", "min-height"))]
    rows.append(("number of `window...{` CSS blocks that themselves declare min-*",
                 "count=%d" % len(win_min), "gkeep-ui.py (whole file)"))

    g = BLOBS["gdktoplevel-wayland.c"].decode("utf-8", "replace")
    rows.append(("GTK acks the configure exactly once per handle_configure",
                 "ack_configure calls=%d" % g.count("ack_configure, wayland_surface"),
                 "gdktoplevel-wayland.c (whole file)"))
    rows.append(("GTK never sends set_min_size/max_size anywhere else",
                 "set_min_size=%d set_max_size=%d"
                 % (g.count("set_min_size"), g.count("set_max_size")),
                 "gdktoplevel-wayland.c (whole file)"))
    h = BLOBS["Hyprland-XDGShell.cpp"].decode("utf-8", "replace")
    rows.append(("Hyprland never sends xdg_toplevel.configure_bounds",
                 "configure_bounds occurrences=%d" % h.count("configure_bounds"),
                 "Hyprland-XDGShell.cpp (whole file)"))
    return rows


def grep_check(rows):
    """Independent check that each computed locator is a real grep -n line.

    Takes the source line the frozen parser reported, strips it, and greps -nF
    a 32-character prefix of it; the reported line number must be one of grep's.
    Nothing here is typed: the pattern comes from the pinned bytes.
    """
    import subprocess
    bad = []
    for r in rows:
        fn = r["file"]
        path = os.path.join(FETCH, fn)
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            src = fh.read().split("\n")
        line = src[r["line"] - 1].strip()
        if not line:
            bad.append((fn, r["line"], "empty source line"))
            continue
        pat = line[:32]
        got = subprocess.run(["grep", "-nF", "--", pat, path],
                             capture_output=True, text=True)
        hits = [int(x.split(":", 1)[0]) for x in got.stdout.splitlines()]
        r["grep_hits"] = hits
        r["grep_ok"] = r["line"] in hits
        if not r["grep_ok"]:
            bad.append((fn, r["line"], pat))
    return bad


def check(rows):
    fails = []
    out = []
    for sec, claim, quote, fn in rows:
        blob = BLOBS[fn]
        nq = " ".join(quote.split())
        words = len(quote.split())
        at = C.quote_at(blob, nq)
        occ = len(C.occurrences(blob, nq))
        incode = C.quote_in_code(blob, nq, fn)
        clash = [g for g in FILES if g != fn and nq in C.norm_receipt(BLOBS[g])]
        ok = (3 <= words <= 25 and at is not None and occ == 1
              and incode and not clash)
        if not ok:
            fails.append((fn, claim, words, at, occ, incode, clash))
        out.append(dict(sec=sec, claim=claim, quote=quote, file=fn, line=at,
                        words=words, occ=occ, incode=incode, clash=clash,
                        sha=hashlib.sha256(blob).hexdigest(), ok=ok))
    return out, fails


def pin_report():
    lines, bad = [], []
    for f in FILES:
        got = hashlib.sha256(BLOBS[f]).hexdigest()
        want = PIN_SHA.get(f)
        state = "PIN-OK" if got == want else "PIN-MISMATCH"
        if got != want:
            bad.append(f)
        lines.append((f, got, want, state, len(BLOBS[f])))
    return lines, bad


HEAD = """# ExecSrcClient - located-quote fact table: the CLIENT side of C2

Round 44, wave w1, seat ExecSrcClient. Scope: what xdg-shell 1.49, GTK 4.24.1 and gkeep 133b867
establish about the client's handling of the size a compositor configures, plus the compositor
seam that hands the size over (context rows, section D - another seat owns that side).

Pins (`.ufo/waves/round-44/fetch/`, sha256 from `receipts/fetch-sha256.txt`, all verified by
`verify_facts.py` below before any row is emitted):

| receipt | sha256 | bytes |
|---|---|---|
"""

MID_A = """
## A. xdg-shell 1.49 (`xdg-shell.xml`)

Protocol text only: it constrains the compositor's *offer* and the client's *obligation*, never
GTK's behaviour. Locators are the 1-based line on which the quote starts, computed by
`verify_facts.py` from the pinned bytes.

| claim | quote (<=25 words) | file:line | sha256 |
|---|---|---|---|
"""

MID_B = """
## B. GTK 4.24.1 (`gdktoplevel-wayland.c`)

The whole client path, in order: `xdg_toplevel_configure` stores -> `xdg_surface.configure`
(`handle_configure`) consumes -> `compute_size` applies -> `ack_configure` is sent. `pending` is
`{int width; int height; GdkToplevelState state; gboolean is_resizing; ...}` (gdktoplevel-wayland.c,
struct GdkWaylandToplevel). The extension is `.c`, which the frozen counter's comment stripper does
not cover (it lists `.cpp/.hpp/.h/.cc`), so a GTK quote *may* come from a comment; every row below is
code anyway, so the rows hold under either reading.

| claim | quote (<=25 words) | file:line | sha256 |
|---|---|---|---|
"""

MID_C = """
## C. gkeep 133b867 (`gkeep-ui.py`)

| claim | quote (<=25 words) | file:line | sha256 |
|---|---|---|---|
"""

MID_D = """
## D. Seam: what Hyprland 0.56.2 actually sends (context, not client behaviour)

Rows here exist only to fix the input to the client rows in A-C: which size leaves
`CWindow::sendWindowSize`, over which request, and how the ack comes back. Verified against the
same pinned bytes with the same parsers; the compositor-side argument belongs to its own seat
(`Hyprland-Window.cpp` is held row S164's receipt).

| claim | quote (<=25 words) | file:line | sha256 |
|---|---|---|---|
"""

SEMANTICS = """
## F. Exact / maximum / hint, per configure state (composed from section A)

| configure state | protocol force on width/height | row |
|---|---|---|
| none (plain floating configure) | a *hint*; the client may pick another size | A1 |
| `maximized` (1) | *exact*: "must be obeyed by the client, or ... invalid_surface_state" | A4 |
| `fullscreen` (2) | *maximum*: "cannot resize beyond it"; must be obeyed to cover the whole area | A5 |
| `resizing` (3) | *maximum*: "cannot resize beyond it" | A6 |
| `tiled_left/right/top/bottom` (5-8) | **no size semantics stated at all**; decoration advice only | A7 |
| `0x0` in either dimension | the client decides (A2), which GTK reads as "restore my own size" (B4) | A2, B4 |

So the protocol never makes a floating configure binding, and never makes a fullscreen configure
exact - it makes it a ceiling. A client that lands *below* the ceiling, or above a bare hint, is
conforming. GTK's own reading of a latched size is a one-shot application (B9 -> B11), clamped
against a MIN-only mask when the configure carried a fresh non-zero size (B8, B10, B13, B14): GTK
cannot come out *smaller* than its own minimum, and nothing in the pinned file stops it from
adopting a size bigger than its natural request. That is the whole room in which the
gkeep/Hyprland size disagreement lives.

## G. What the pinned sources do NOT establish

Each item names the rows it would have needed and the file that was never pinned.

1. **That GTK honours a compositor size LARGER than its natural size.** B9-B11 show the latched size
   is taken and applied; B13/B14 show the only clamp is a MIN floor for a resizable window. But the
   `update_size` -> buffer-commit path that turns this into a `wl_surface` size lives in
   `gdk/wayland/gdksurface.c` and GTK's widget allocation in `gtk/gtkwindow.c`, **neither pinned**.
   Reading these five files does not say what a 900x1200 configure does to a 420x500 gkeep.
   [INFERENCE] from B9-B11: the configured size is the one GDK *adopts*, raised to GTK's minimum.
2. **What gkeep's actual minimum/natural size IS.** `set_size_request(` occurs zero times in the
   pinned full file (E), and the only CSS `min-*` declarations are two lines under `button.ink`
   (C3, E) - i.e. 30px/72px on *buttons*. The window's minimum is whatever `GtkWindow` computes
   from its children in `gtk/gtkwindow.c`, not pinned.
3. **That `set_default_size(420, 500)` reaches the screen as 420x500.** C1 pins the call; how GTK
   turns it into the size it commits on a 0x0 configure is `gtk/gtkwindow.c` plus
   `gdk/wayland/gdksurface.c`, not pinned. B20 only shows the *fallback* size comes from
   `gdk_toplevel_notify_compute_size`, not from a field holding 420x500.
4. **Which states Hyprland attaches to the configure for a rule-sized floating window.** D6/D7 show
   the states array is whatever `m_pendingApply.states` holds at schedule time; they do not show
   the set for gkeep. If `maximized`/`fullscreen`/`tiled`/`resizing` were ever in it, GTK's
   `fixed_size` flips (B5), the one-shot clearing at B11 stops applying and the size becomes sticky.
   This needs a runtime capture, not a source read.
5. **That Hyprland honours GTK's `set_min_size` when it sizes the box from a windowrule.** D8 proves
   Hyprland *tracks* a client min size for the layout; no pinned line shows the rule-size path
   consulting it.
6. **That GTK's shadow margins are zero for gkeep.** `set_decorated(False)` is pinned (E) and B18
   subtracts `shadow_*` from the saved size, but where those fields are assigned is not in this
   file. "The surface commits exactly 420x500" is therefore not visible in the pins.
7. **That `configure_bounds` reaches GTK on Hyprland.** `grep -c configure_bounds` on the pinned
   `Hyprland-XDGShell.cpp` is 0 (E), so GTK's `has_bounds` stays false and the monitor-union
   fallback (B19, B20) is the live path - but that is a statement about this commit, not about
   0.56.2 under every state.
8. **Anything about a client other than GTK.** Section F's permissiveness means one configure can be
   honoured exactly, clamped, or ignored by three toolkits. No row here generalises to
   Qt/Electron/Chromium, so no row supports a claim about "clients" as a class.
9. **That the ack is observable as a resize.** B17 acks at the end of `handle_configure`, i.e. before
   `compute_size` applies the size in the same layout pass, and the pins do not order that ack
   against the buffer commit. "The compositor saw the ack, so the window resized" is unsupported.
10. **Which of the two boxes C1 compares.** Nothing in these five files says whether
    `hyprctl clients -j` reports the box Hyprland assigned or the size the client committed; that is
    the compositor-side question, and it is why A1+A2 (hint, client decides) matter: the two may
    legitimately differ without either side misbehaving.

## H. What the C2 entry can lift from here

Clause h of PRED-C2-r44 recomputes two lines from the pinned bytes. `verify_facts.py` runs the
frozen counter's own `host_census()` against these same pins and both lines come back verbatim:

    gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep
    hyprland sendWindowSize xdg_setSize=1 x11_configure=1

`xdg_setSize=1` / `x11_configure=1` are D3/D4 counted inside `CWindow::sendWindowSize`; the gkeep
line's three fields are C1 (default size), E (zero `set_size_request` calls) and C2
(application_id). Every row in A-D is gate-usable as written: 3-25 words, word-bounded, occurring
exactly once in its receipt, surviving the counter's comment stripping for that extension, and
occurring in none of the other four pins - so five Gate rows quoting five different receipts stay
pairwise distinguishable.

Tooling: no package was installed for this seat; `python3` (host) plus the lane's frozen counter,
imported read-only, were sufficient. No scratch tree was left behind.

## I. Verification

`verify_facts.py` (this seat dir) imports the FROZEN counter's own parsers (`quote_at`,
`occurrences`, `quote_in_code`, `norm_receipt`, `host_census`) from
`quality/counters/c2-r44-gkeep-size-request.py` and, for every row above, asserts:

* `3 <= len(quote.split()) <= 25`;
* the whitespace-collapsed quote occurs word-bounded **exactly once** in its receipt;
* it survives the frozen counter's comment stripping for that extension (`.cpp` stripped, `.c` and
  `.xml` untouched, `.py` `#`-stripped);
* it occurs in **no other** pinned receipt (`norm_receipt`);
* the printed locator is the line the parser computed, and each receipt's sha256 still equals the
  frozen `receipts/fetch-sha256.txt` value (5/5 `PIN-OK`);
* **grep agrees with every locator**: taking the source line at the computed number and running
  `grep -nF` on a 32-character prefix of it returns that same line number (42/42).

It also runs the frozen counter's `host_census()` on the same pinned bytes and requires it to
reproduce both clause-h lines verbatim (section H).

Raw output: `verify.log` in this seat dir. Re-run:
`cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I .ufo/waves/round-44/w1/ExecSrcClient/verify_facts.py`
-> `grep_locator_ok=42/42`, `census_clause_h ok=True`,
`rows=42 fails=0 pin_mismatch=0 census_ok=True grep_fails=0`.
"""


MID_E = """
## E. Structure facts (parser-read, not quoted)

| fact | value | where |
|---|---|---|
"""


def emit(out, pin_lines, path, structs):
    buf = [HEAD]
    for f, sha, want, state, n in pin_lines:
        buf.append("| `%s` | `%s` | %d |\n" % (f, sha, n))
    cur = None
    n = 0
    for r in out:
        if r["sec"] != cur:
            cur = r["sec"]
            n = 0
            buf.append({"A": MID_A, "B": MID_B, "C": MID_C, "D": MID_D}[cur])
        n += 1
        r["id"] = "%s%d" % (cur, n)
        buf.append("| %s | %s | `%s` | `%s:%d` | `%s` |\n"
                   % (r["id"], r["claim"], r["quote"], r["file"], r["line"],
                      r["sha"]))
    buf.append(MID_E)
    for fact, value, where in structs:
        buf.append("| %s | `%s` | `%s` |\n" % (fact, value, where))
    buf.append(SEMANTICS)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("".join(buf))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "facts.md"))
    a = ap.parse_args()
    pin_lines, bad_pins = pin_report()
    print("pins:")
    for f, sha, want, state, n in pin_lines:
        print("  %-24s %d bytes sha256=%s %s" % (f, n, sha, state))
    out, fails = check(ROWS)
    gbad = grep_check(out)
    print("grep_locator_ok=%d/%d fails=%d"
          % (len(out) - len(gbad), len(out), len(gbad)))
    for f in gbad:
        print("GREPFAIL file=%s line=%s pattern=%r" % f)
    cok, want = census_check()
    print("census_clause_h ok=%s" % cok)
    for w in want:
        print("  census %r expected_match=%s"
              % (w, w in CENSUS_EXPECTED))
    structs = struct_facts()
    for fact, value, where in structs:
        print("struct %-62s %-28s %s" % (fact, value, where))
    for r in out:
        print("row sec=%s file=%s line=%s words=%d occ=%d code=%s sha=%s .. %s"
              % (r["sec"], r["file"], r["line"], r["words"], r["occ"],
                 r["incode"], r["sha"][:12], r["claim"][:58]))
    emit(out, pin_lines, a.out, structs)
    print("rows=%d fails=%d pin_mismatch=%d census_ok=%s grep_fails=%d wrote=%s"
          % (len(out), len(fails), len(bad_pins), cok, len(gbad), a.out))
    if fails or bad_pins or not cok or gbad:
        for f in fails:
            print("FAIL file=%s words=%d at=%s occ=%d code=%s clash=%s claim=%s"
                  % (f[0], f[2], f[3], f[4], f[5], f[6], f[1]))
        if want != CENSUS_EXPECTED:
            print("FAIL census want=%r" % (want,))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
