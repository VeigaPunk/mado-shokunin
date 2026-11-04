#!/usr/bin/env python3
"""mado — bar footprint join: declared waybar config -> live layer box -> reserved band.

Reads three caller-supplied artifacts and writes nothing:

  --config    the waybar configuration (JSONC; object form, as waybar 0.15.0 reads it)
  --layers    a captured `hyprctl layers -j` reply (file or `-` for stdin)
  --monitors  a captured `hyprctl monitors -j` reply (file or `-` for stdin)
  --monitor   the monitor name to join (optional when exactly one monitor answers)
  --rules     optional: the Hyprland config file carrying the joined monitor's `monitor =`
              rules, from which the static reserved area (`addreserved`) is read

It derives the bar's declared layer-surface footprint from the configuration at the
resolution Hyprland 0.56.2 gives it, finds the live layer entry with the same namespace
at the declared level, and compares the footprint with the live box and with the
monitor's `reserved` band. Nothing is connected, started or written.

Contract (v1, round 77):
  * position top/bottom/left/right; layer background/bottom/top/overlay; height/width;
    margin-<side> and CSS-form margin strings (std::stoi prefix parse); exclusive; name;
    output (waybar 0.15.0's two branches: an array's `!name`/`name`/`*` walk falling through
    to false, a string's empty/`!name`/`name`; monitor names only).
  * Hyprland's arrange rule (src/render/Renderer.cpp arrangeLayerArray/@ efb5099):
    a zero desired width extends across the usable box minus horizontal margins;
    waybar clears both horizontal anchors when the bar declares a width > 1
    (src/bar.cpp:422-424), and the both-anchors branch then centres the box; the same
    holds transposed for vertical bars.
  * The reserved expectation is formed for any non-negative margin. It composes two
    measured contributors (round 78): gtk-layer-shell's auto zone for a horizontal bar is
    the allocation (bar height) plus the margin of the *unanchored* edge of that axis
    (src/layer-surface.c layer_surface_update_auto_exclusive_zone), and Hyprland's
    applyExclusive adds the anchored edge's margin (src/render/Renderer.cpp:2575-2583).
    For a top bar both add up to `height + margin.top + margin.bottom`; the transposed
    rule gives `width + margin.left + margin.right` for a vertical bar, so the expected
    band is the anchored-edge extent plus the opposite edge's margin. Horizontal margins of
    a horizontal bar never enter the band (they only move/resize a zero-width box).
    A negative margin is refused (the band can be voided or extend past the box).
  * A static reserved area declared by a `monitor = NAME, addreserved, TOP, BOTTOM, LEFT,
    RIGHT` rule is composed once, underneath the bar's own contribution (round 79):
    the monitor's usable box starts after it (`CReservedArea::apply`), the layer box is
    placed inside that usable box, and the printed `reserved` sums the static and the
    dynamic bands (`CReservedArea::calculate`). So `expected = static_band + extent +
    opposite margin`, the box is translated by the static origin, and an uncontained box
    contributes nothing (the dynamic-area constructor refuses it; Hyprland's own
    `m_reservedArea` then keeps the static band). The rule walk follows
    `handleMonitor`: a positional rule or `disable` replaces the selector's rule (reserved
    zero), `addreserved` sets it in line order TOP, BOTTOM, LEFT, RIGHT, `transform`
    copies the rule and keeps its reserved area, and the newest rule for the selector is
    the static reserve the monitor applies (`Monitor.cpp:654 setStatic`). An `addreserved`
    line with no same-selector rule ahead of it adds a default rule that never received the
    area, so its reserve is zero and the written area is dropped.
  * `reserved` band order is [left, top, right, bottom] (HyprCtl.cpp monitors reply).
  * Refused, never guessed: a monitor whose scale is not 1 or whose transform is not 0 (the
    monitors reply carries pixel size, the layer box is logical); a dynamic band (a
    horizontal surface with height 0, or a vertical one with width 0) unless `--allocation`
    declares the client's own band for that namespace, in which case the allocation is the
    band (both the arranged box and gtk-layer-shell's auto zone, layer-surface.c:276/282)
    and a zero or absent allocation is refused, never guessed (round 83: an entry in the map
    resolves the band of *any* declared surface, not only the bar's; a dynamic band with an
    explicit zone and no entry keeps the compositor's assign branch, the box spanning the
    usable axis, and the auto-zone arm that needs the band stays a refusal); a list-valued config
    (multiple bars); a
    space-bearing or string-`*` output pattern; a negative margin; a `mode` key (presets
    rewrite layer and exclusive zone at runtime); and a `--rules` file carrying a `source =`
    line or a selector outside the literal subset (a sourced file is not followed).
  * Modelled with the sources: the usable box starts at the monitor's layout origin
    (`logicalBox()` is `{position, size}`, Monitor.cpp:1768-1770; the monitors reply prints
    `x`/`y`); an `addreserved` field is clamped at 0 (`CReservedArea(top, right, bottom, left)`
    takes `std::max(x, 0.0)`, ReservedArea.cpp:14-15); the centred box rounds once (Hyprland
    computes the centre in doubles and calls `box.round()`, Renderer.cpp:2660); a static
    reserved area that leaves no usable box is refused; and a bar whose box is not contained
    in the usable box — or whose band (extent plus opposite margin) does not fit the usable
    axis — reserves nothing (CReservedArea's parent/child short-circuit, ReservedArea.cpp:19-30)
    so the expected band is then the static band alone.
  * Not modelled and named as a limit: a second *layer-surface* consumer whose band is not
    declared statically (the reported band then exceeds `expected` and is reported `GT`,
    never attributed); an output entry naming the xdg-output identifier waybar derives from
    the monitor description (only the monitor name is matched); and any runtime change after
    the capture.

Exit map: 0 CLEAN · 1 DIFFER · 2 SETUP/ERROR · 3 NOT_FORMED (NO_LAYER/UNMODELLED/NO_BAR).
"""

import argparse
import json
import math
import os
import re
import stat
import sys

VERSION = "r83-v1"

MAX_BYTES = 1048576

# zwlr_layer_surface_v1 anchor bits: top 1, bottom 2, left 4, right 8.
ANCHOR = {"top": 1, "bottom": 2, "left": 4, "right": 8}

# IHyprRenderer::applyExclusive walks these four rules in this order and stops at the
# first match; the match is (exclusiveEdge == singular) or (anchor == singular) or
# (anchor == triplet) and zone + margin(edge) > 0 (Renderer.cpp:2541-2586).
EDGE_RULES = (
    ("top", ANCHOR["top"], ANCHOR["left"] | ANCHOR["right"] | ANCHOR["top"]),
    ("bottom", ANCHOR["bottom"], ANCHOR["left"] | ANCHOR["right"] | ANCHOR["bottom"]),
    ("left", ANCHOR["left"], ANCHOR["left"] | ANCHOR["top"] | ANCHOR["bottom"]),
    ("right", ANCHOR["right"], ANCHOR["right"] | ANCHOR["top"] | ANCHOR["bottom"]),
)

# The triplet each position anchors by default (gtk-layer-shell's set_anchor set).
POSITION_ANCHORS = {
    "top": ("top", "left", "right"),
    "bottom": ("bottom", "left", "right"),
    "left": ("left", "top", "bottom"),
    "right": ("right", "top", "bottom"),
}

LEVEL = {"background": 0, "bottom": 1, "top": 2, "overlay": 3}
POSITIONS = ("top", "bottom", "left", "right")
MARGIN_SIDES = ("top", "right", "bottom", "left")

# HyprCtl.cpp: monitors reply prints m_reservedArea in left, top, right, bottom order.
RESERVED_INDEX = {"left": 0, "top": 1, "right": 2, "bottom": 3}

# The edge opposite the anchored one on the band axis: gtk-layer-shell's auto zone adds
# the unanchored edge's margin; Hyprland adds the anchored edge's margin (r78 model).
OPPOSITE_EDGE = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}

# `monitor = NAME, addreserved, TOP, BOTTOM, LEFT, RIGHT` line order: the handler reads
# ARGS[2] as top, ARGS[3] as bottom, ARGS[4] as left, ARGS[5] as right and hands them to
# CReservedArea(top, right, bottom, left) (Hyprland-legacy-ConfigManager.cpp:1323-1326).
STATIC_SIDES = ("top", "bottom", "left", "right")

ZERO_STATIC = {"top": 0, "right": 0, "bottom": 0, "left": 0}

# The KEY forms a positional `monitor =` line accepts; any other key drops the whole line
# before the rule is added (Hyprland-legacy-ConfigManager.cpp:1351-1379), so the rule the
# selector already had survives and its reserved area is kept.
MONITOR_RULE_KEYS = {"mirror", "bitdepth", "cm", "sdrsaturation", "sdrbrightness",
                     "transform", "vrr", "icc"}

INT_FIELD_RE = re.compile(r"-?[0-9]{1,6}")


class Setup(Exception):
    """Caller-side setup error (unreadable input, bad JSON, refused path)."""


class Unmodelled(Exception):
    """A declaration this tool's model does not cover; never guessed."""


def read_bytes(path, stdin_ok=False):
    if path == "-":
        if not stdin_ok:
            raise Setup("stdin is not accepted for this argument")
        data = sys.stdin.buffer.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise Setup("stdin exceeds %d bytes" % MAX_BYTES)
        return data
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise Setup("unreadable path %s: %s" % (path, exc))
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            raise Setup("refused non-regular path: %s" % path)
        if st.st_size > MAX_BYTES:
            raise Setup("file exceeds %d bytes: %s" % (MAX_BYTES, path))
        with os.fdopen(fd, "rb") as fh:
            fd = None
            return fh.read()
    finally:
        if fd is not None:
            os.close(fd)


def strip_jsonc(text):
    """Remove // and /* */ comments and trailing commas outside strings."""
    out = []
    i = 0
    n = len(text)
    in_str = False
    esc = False
    while i < n:
        ch = text[i]
        if in_str:
            out.append(ch)
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            i += 1
            continue
        if ch == '"':
            in_str = True
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
            continue
        out.append(ch)
        i += 1
    cleaned = "".join(out)
    return re.sub(r",(\s*[}\]])", r"\1", cleaned)


def load_json(raw, label):
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise Setup("%s is not UTF-8" % label)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise Setup("%s is not valid JSON: %s" % (label, exc))


def load_jsonc(raw, label):
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise Setup("%s is not UTF-8" % label)
    try:
        return json.loads(strip_jsonc(text))
    except json.JSONDecodeError as exc:
        raise Setup("%s is not valid JSONC: %s" % (label, exc))


def as_uint(value):
    """waybar: isUInt() ? asUInt() : 0 — bool is not accepted here."""
    if isinstance(value, bool):
        return 0
    if isinstance(value, int) and value >= 0:
        return value
    return 0


def parse_margins(config):
    """Reproduce Waybar 0.15.0 bar.cpp's margin precedence exactly.

    1. any integer margin-<side> present -> each side is its own integer or 0
    2. else a string margin in CSS order (1, 2, 3 or 4 integers)
    3. else an integer margin -> all sides
    A parse failure leaves the initial zeros.
    """
    sides = {s: 0 for s in MARGIN_SIDES}
    per_side = ["margin-" + s for s in MARGIN_SIDES]
    if any(isinstance(config.get(k), int) and not isinstance(config.get(k), bool) for k in per_side):
        for side in MARGIN_SIDES:
            value = config.get("margin-" + side)
            sides[side] = value if isinstance(value, int) and not isinstance(value, bool) else 0
        return sides
    margin = config.get("margin")
    if isinstance(margin, str):
        tokens = margin.split()
        values = []
        for token in tokens:
            # std::stoi is a prefix parse (4px -> 4); a token without an integer prefix
            # throws and the catch leaves every side at its default
            match = re.match(r"[+-]?[0-9]+", token)
            if match is None:
                return sides
            values.append(int(match.group(0), 10))
        if len(values) > 4:
            return sides
        if len(values) == 1:
            sides = {s: values[0] for s in MARGIN_SIDES}
        elif len(values) == 2:
            sides = {"top": values[0], "right": values[1], "bottom": values[0], "left": values[1]}
        elif len(values) == 3:
            sides = {"top": values[0], "right": values[1], "bottom": values[2], "left": values[1]}
        elif len(values) == 4:
            sides = {"top": values[0], "right": values[1], "bottom": values[2], "left": values[3]}
        return sides
    if isinstance(margin, int) and not isinstance(margin, bool):
        return {s: margin for s in MARGIN_SIDES}
    return sides


def output_matches(config, monitor):
    """Waybar 0.15.0 `isValidOutput`: the array and the string branch differ.

    Array: `!name` excludes and continues, `name` includes, an entry starting with `*`
    includes, and the loop falls through to false when no entry matched. String: an empty
    value means every output, `!name` excludes, `name` includes, anything else does not
    match. Monitor *names* only: an entry naming the xdg-output identifier (which waybar
    derives from the output description) is not modelled and is reported as a limit.
    """
    spec = config.get("output")
    if spec is None:
        return True
    if isinstance(spec, list):
        for entry in spec:
            if not isinstance(entry, str):
                raise Unmodelled("output entries must be strings")
            if " " in entry:
                raise Unmodelled("output pattern %r is outside the modelled subset" % entry)
            if entry.startswith("!"):
                if entry[1:] == monitor:
                    return False
                continue
            if entry == monitor or entry.startswith("*"):
                return True
        return False
    if isinstance(spec, str):
        if " " in spec:
            raise Unmodelled("output pattern %r is outside the modelled subset" % spec)
        if spec == "":
            return True
        if spec.startswith("!"):
            return spec[1:] != monitor
        if spec.startswith("*"):
            raise Unmodelled("output pattern %r is outside the modelled subset" % spec)
        return spec == monitor
    raise Unmodelled("output must be a string or an array")


def declared_bar(config):
    position = config.get("position", "top")
    if position not in POSITIONS:
        raise Unmodelled("position %r is outside top/bottom/left/right" % (position,))
    layer = config.get("layer", "bottom")
    if layer not in LEVEL:
        raise Unmodelled("layer %r is outside background/bottom/top/overlay" % (layer,))
    if layer == "background":
        raise Unmodelled("waybar's presets never select the background layer")
    namespace = config.get("name") if isinstance(config.get("name"), str) else "waybar"
    if isinstance(config.get("mode"), str):
        raise Unmodelled("a mode preset rewrites layer and exclusive zone at runtime")
    exclusive = config.get("exclusive")
    exclusive = exclusive if isinstance(exclusive, bool) else True
    margins = parse_margins(config)
    if any(value < 0 for value in margins.values()):
        raise Unmodelled("a negative margin can void or invert the exclusive band; not modelled")
    return {
        "position": position,
        "layer": layer,
        "level": LEVEL[layer],
        "namespace": namespace,
        "exclusive": exclusive,
        "height": as_uint(config.get("height")),
        "width": as_uint(config.get("width")),
        "margins": parse_margins(config),
    }


def strip_rule_comment(line):
    """Hyprland config comments run from `#` to the end of the line."""
    return line.split("#", 1)[0].strip()


def read_text(path):
    data = read_bytes(path)
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Setup("rules file is not UTF-8: %s" % exc)


def parse_static_reserve(text, monitor):
    """The static reserved area the joined monitor's `monitor =` rules leave active.

    Walks the file in order and keeps one rule slot for the exact selector, following the
    handler's own effects: a positional rule (or `disable`) replaces the selector's rule
    with a zero reserved area, `addreserved` sets the slot's area (creating a default rule
    when none exists), and `transform` copies the slot and keeps its area. The newest rule
    for the selector is the one the monitor applies, so the final slot is the static
    reserve. Rules for other selectors never touch this slot. Fail-closed: a `source =`
    line (a sourced file is not followed), a rule line outside the literal subset, or an
    `addreserved` field that is not a plain integer refuses the whole join.
    """
    slot = None
    for number, raw in enumerate(text.splitlines(), 1):
        line = strip_rule_comment(raw)
        if not line:
            continue
        key, sep, value = line.partition("=")
        if not sep:
            continue
        key = key.strip()
        if key == "source":
            raise Unmodelled("the rules file carries a `source =` line (line %d); a sourced "
                             "file is not followed, so the static reserve is unknown" % number)
        if key != "monitor":
            continue
        if "$" in value or "\\" in value or "##" in value:
            raise Unmodelled("a monitor rule outside the literal subset (line %d)" % number)
        fields = [field.strip() for field in value.split(",")]
        selector = fields[0]
        if selector == "" or selector.startswith("desc:"):
            raise Unmodelled("a monitor rule selector %r is outside the literal subset "
                             "(line %d); it is not matched by name" % (selector, number))
        kind = fields[1] if len(fields) > 1 else ""
        if selector != monitor:
            continue
        if kind in ("disable", "disabled"):
            slot = dict(ZERO_STATIC)
        elif kind == "addreserved":
            values = fields[2:6]
            if len(values) != 4 or not all(INT_FIELD_RE.fullmatch(v) for v in values):
                raise Unmodelled("addreserved needs four plain integers, TOP BOTTOM LEFT "
                                 "RIGHT (line %d)" % number)
            # the four-argument constructor clamps each field at 0 (ReservedArea.cpp:14-15)
            area = dict(zip(STATIC_SIDES, (max(0, int(v)) for v in values)))
            # the handler writes the area into the selector's *existing* rule and returns; with
            # no such rule it falls through to `add(parser.rule())`, and the parser never
            # received the area, so the added rule's reserve is zero (the area is dropped)
            slot = area if slot is not None else dict(ZERO_STATIC)
        elif kind == "transform":
            # the handler copies the first same-selector rule; with none it adds nothing
            slot = dict(slot) if slot is not None else None
        else:
            # a positional rule replaces the selector's rule only when the line parses:
            # an unknown key drops the whole line before the add (ConfigManager:1351-1379)
            index = 4
            kept = True
            while index < len(fields) and fields[index] != "":
                if fields[index] not in MONITOR_RULE_KEYS:
                    kept = False
                    break
                index += 2
            if kept:
                slot = dict(ZERO_STATIC)
    return dict(slot) if slot is not None else dict(ZERO_STATIC)


def parse_allocation(raw):
    """The `--allocation` declaration: {namespace: band} — the band size the client's own
    surface was allocated on its band axis. It is the only input that can turn a declared
    dynamic band (`height = 0` on a horizontal surface, `width = 0` on a vertical one) into
    a modelled value; nothing is inferred when it is absent."""
    data = load_json(raw, "allocation")
    if not isinstance(data, dict):
        raise Setup("the allocation declaration is not an object of namespace -> band")
    out = {}
    for name, value in data.items():
        if not isinstance(name, str) or not name:
            raise Setup("the allocation declaration carries an empty namespace")
        if not isinstance(value, int) or isinstance(value, bool):
            raise Setup("the allocation for %r is not an integer" % name)
        if value < 0:
            raise Setup("the allocation for %r is negative" % name)
        out[name] = value
    return out


def band_of(spec, allocation):
    """The band size on the surface's band axis: the declared value when it is positive,
    else the client's allocation for that namespace. A zero or absent allocation is a
    refusal, never a guessed band."""
    axis = "height" if spec["position"] in ("top", "bottom") else "width"
    if spec[axis] > 0:
        return spec[axis]
    band = allocation.get(spec["namespace"])
    if band is None:
        raise Unmodelled("%s %r has a dynamic %s (0) and no --allocation entry: the band "
                         "is the client's allocation, not a declared value"
                         % (spec["namespace"], spec["position"], axis))
    if band <= 0:
        raise Unmodelled("%s %r was allocated a %d %s band; a zero band reserves nothing"
                         % (spec["namespace"], spec["position"], band, axis))
    return band


def declared_box(bar, mon_w, mon_h, allocation=None):
    """Hyprland 0.56.2 arrangeLayerArray: desired size, anchors, margins."""
    m = bar["margins"]
    pos = bar["position"]
    allocation = allocation or {}
    # the band axis always resolves through band_of: the declaration wins when it is
    # positive, the client's allocation fills the dynamic case, and neither is guessed
    height = band_of(bar, allocation) if pos in ("top", "bottom") else bar["height"]
    width = band_of(bar, allocation) if pos in ("left", "right") else bar["width"]
    if pos in ("top", "bottom"):
        if width > 1:
            w = width
            x = (mon_w - w + 1) // 2  # Hyprland centres in doubles and rounds once (:2660)
        else:
            w = mon_w - m["left"] - m["right"]
            x = m["left"]
        if height > 0:
            h = height
            y = m["top"] if pos == "top" else mon_h - h - m["bottom"]
        else:
            # zero desired height: the auto-height branch spans the usable box
            h = mon_h - m["top"] - m["bottom"]
            y = m["top"]
    else:
        if height > 1:
            h = height
            y = (mon_h - h + 1) // 2  # Hyprland centres in doubles and rounds once (:2660)
        else:
            h = mon_h - m["top"] - m["bottom"]
            y = m["top"]
        if width > 0:
            w = width
            x = m["left"] if pos == "left" else mon_w - w - m["right"]
        else:
            w = mon_w - m["left"] - m["right"]
            x = m["left"]
    if w <= 0 or h <= 0:
        raise Unmodelled("declared box is empty (%dx%d)" % (w, h))
    return {"x": x, "y": y, "w": w, "h": h}


def edge_extent(bar, box, usable):
    """The anchored-edge extent of the realised box, measured inside the usable box."""
    pos = bar["position"]
    if pos == "top":
        return (box["y"] - usable["y"]) + box["h"]
    if pos == "bottom":
        return (usable["y"] + usable["h"]) - box["y"]
    if pos == "left":
        return (box["x"] - usable["x"]) + box["w"]
    return (usable["x"] + usable["w"]) - box["x"]


def anchor_mask(names):
    """The zwlr anchor mask for a list of edge names."""
    mask = 0
    for name in names:
        mask |= ANCHOR[name]
    return mask


def std_round(value):
    """std::round: half away from zero (C++11 26.8/9), not Python's banker's rounding."""
    return math.floor(value + 0.5) if value >= 0 else math.ceil(value - 0.5)


def cbox_round(box):
    """hyprutils CBox::round (src/math/Box.cpp:51-63, v0.14.0): round the origin first,
    then round the far edge's distance from it, so an odd overflow past a negative tie
    keeps the compositor's width."""
    rx = std_round(box["x"])
    ry = std_round(box["y"])
    nw = box["x"] + box["w"] - rx
    nh = box["y"] + box["h"] - ry
    return {"x": int(rx), "y": int(ry), "w": int(std_round(nw)), "h": int(std_round(nh))}


def arranged_box(spec, bounds):
    """IHyprRenderer::arrangeLayerArray's box arithmetic against a bounds box
    (Renderer.cpp:2606-2660): desired size, anchors, then margins, in doubles.
    The result is unrounded; the caller applies cbox_round like :2660."""
    m = spec["margins"]
    anchor = spec["anchor"]
    both_h = bool(anchor & ANCHOR["left"]) and bool(anchor & ANCHOR["right"])
    both_v = bool(anchor & ANCHOR["top"]) and bool(anchor & ANCHOR["bottom"])
    w, h = spec["width"], spec["height"]
    if w == 0:
        x = bounds["x"]
    elif both_h:
        x = bounds["x"] + (bounds["w"] / 2.0 - w / 2.0)
    elif anchor & ANCHOR["left"]:
        x = bounds["x"]
    elif anchor & ANCHOR["right"]:
        x = bounds["x"] + bounds["w"] - w
    else:
        x = bounds["x"] + (bounds["w"] / 2.0 - w / 2.0)
    if h == 0:
        y = bounds["y"]
    elif both_v:
        y = bounds["y"] + (bounds["h"] / 2.0 - h / 2.0)
    elif anchor & ANCHOR["top"]:
        y = bounds["y"]
    elif anchor & ANCHOR["bottom"]:
        y = bounds["y"] + bounds["h"] - h
    else:
        y = bounds["y"] + (bounds["h"] / 2.0 - h / 2.0)
    if w == 0:
        x += m["left"]
        w = bounds["w"] - m["left"] - m["right"]
    elif both_h:
        pass  # both horizontal anchors: margins are not applied
    elif anchor & ANCHOR["left"]:
        x += m["left"]
    elif anchor & ANCHOR["right"]:
        x -= m["right"]
    if h == 0:
        y += m["top"]
        h = bounds["h"] - m["top"] - m["bottom"]
    elif both_v:
        pass
    elif anchor & ANCHOR["top"]:
        y += m["top"]
    elif anchor & ANCHOR["bottom"]:
        y -= m["bottom"]
    return {"x": x, "y": y, "w": w, "h": h}


def surface_zone(spec):
    """The zone the surface requests from the compositor. An explicit integer is stored
    verbatim (LayerShell.cpp:100-102). `auto` is gtk-layer-shell's client-side value
    (layer-surface.c:264-292, v0.10.1): gated on the anchor set being horizontal or
    vertical but not both, and taken from the allocation's band size plus the unanchored
    margins of that axis."""
    declared = spec["exclusive"]
    if declared != "auto":
        return declared
    anchor = spec["anchor"]
    horiz = bool(anchor & ANCHOR["left"]) == bool(anchor & ANCHOR["right"])
    vert = bool(anchor & ANCHOR["top"]) == bool(anchor & ANCHOR["bottom"])
    if horiz and not vert:
        if spec["height"] == 0:
            raise Unmodelled("auto zone on a dynamic height (0) is the client's allocation, "
                             "not a declared value")
        zone = spec["height"]
        if not anchor & ANCHOR["top"]:
            zone += spec["margins"]["top"]
        if not anchor & ANCHOR["bottom"]:
            zone += spec["margins"]["bottom"]
        return zone
    if vert and not horiz:
        if spec["width"] == 0:
            raise Unmodelled("auto zone on a dynamic width (0) is the client's allocation, "
                             "not a declared value")
        zone = spec["width"]
        if not anchor & ANCHOR["left"]:
            zone += spec["margins"]["left"]
        if not anchor & ANCHOR["right"]:
            zone += spec["margins"]["right"]
        return zone
    # gtk-layer-shell sends no zone for a corner, a parallel pair or all four anchors
    return 0


def zone_for_pass(spec):
    """The zone used to split the two arrange passes; a class the model refuses still
    has to be ordered, and it is refused at its turn (after the empty-box skip)."""
    try:
        return surface_zone(spec)
    except Unmodelled:
        return 0


def parse_surfaces(raw):
    """The `--surfaces` declaration: a list (or {"surfaces": [...]}) of layer surfaces."""
    data = load_json(raw, "surfaces")
    if isinstance(data, dict):
        data = data.get("surfaces")
    if not isinstance(data, list):
        raise Setup("surfaces declaration is not a list")
    specs = []
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise Setup("surface %d is not an object" % index)
        namespace = item.get("namespace")
        if not isinstance(namespace, str) or not namespace:
            raise Setup("surface %d has no namespace" % index)
        level = item.get("level")
        if not isinstance(level, int) or isinstance(level, bool) or not 0 <= level <= 3:
            raise Setup("surface %r level is outside 0-3" % namespace)
        position = item.get("position", "top")
        if position not in POSITIONS:
            raise Setup("surface %r position %r is outside top/bottom/left/right"
                        % (namespace, position))
        names = item.get("anchor")
        if names is None:
            names = list(POSITION_ANCHORS[position])
        if not isinstance(names, list) or not names or any(n not in ANCHOR for n in names):
            raise Setup("surface %r anchor is not a non-empty list of top/bottom/left/right"
                        % namespace)
        if len(set(names)) != len(names):
            raise Setup("surface %r repeats an anchor" % namespace)
        exclusive = item.get("exclusive", "auto")
        if exclusive != "auto" and (not isinstance(exclusive, int)
                                    or isinstance(exclusive, bool)):
            raise Setup("surface %r exclusive is neither an integer nor \"auto\"" % namespace)
        edge = item.get("exclusiveEdge")
        if edge is not None and edge not in ANCHOR:
            raise Setup("surface %r exclusiveEdge is not an edge name" % namespace)
        if edge is not None and edge not in names:
            # the protocol errors when the exclusive edge does not align with the anchor
            raise Unmodelled("surface %r declares exclusiveEdge %r outside its anchor set"
                             % (namespace, edge))
        margins = {}
        declared = item.get("margins", {})
        if not isinstance(declared, dict):
            raise Setup("surface %r margins is not an object" % namespace)
        for side in MARGIN_SIDES:
            value = declared.get(side, 0)
            if not isinstance(value, int) or isinstance(value, bool):
                raise Setup("surface %r margin %r is not an integer" % (namespace, side))
            margins[side] = value
        order = item.get("order", 0)
        if not isinstance(order, int) or isinstance(order, bool):
            raise Setup("surface %r order is not an integer" % namespace)
        for key, kind in (("height", "height"), ("width", "width")):
            value = item.get(key, 0)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise Setup("surface %r %s is not a non-negative integer" % (namespace, kind))
        specs.append({
            "namespace": namespace,
            "level": level,
            "position": position,
            "anchor": anchor_mask(names),
            "anchor_names": list(names),
            "height": item.get("height", 0),
            "width": item.get("width", 0),
            "margins": margins,
            "exclusive": exclusive,
            "exclusiveEdge": ANCHOR[edge] if edge else 0,
            "order": order,
        })
    return specs


def apply_exclusive(usable, spec, zone):
    """IHyprRenderer::applyExclusive (Renderer.cpp:2529-2586): shrink the running usable
    box on the first matching edge; returns the edge it hit, or None."""
    if zone <= 0:
        return None
    for edge, singular, triplet in EDGE_RULES:
        if ((spec["exclusiveEdge"] == singular or spec["anchor"] == singular
             or spec["anchor"] == triplet) and zone + spec["margins"][edge] > 0):
            amount = zone + spec["margins"][edge]
            if edge == "top":
                usable["y"] += amount
                usable["h"] -= amount
            elif edge == "bottom":
                usable["h"] -= amount
            elif edge == "left":
                usable["x"] += amount
                usable["w"] -= amount
            else:
                usable["w"] -= amount
            return edge
    return None


def contains_box(parent, child):
    """CBox::containsPoint at both child corners (ReservedArea.cpp:23-25)."""
    return (child["x"] >= parent["x"] and child["y"] >= parent["y"]
            and child["x"] + child["w"] <= parent["x"] + parent["w"]
            and child["y"] + child["h"] <= parent["y"] + parent["h"])


def evaluate_composition(config, layers, monitors, monitor, static, static_source, extras,
                         allocation=None):
    """The composition model: every declared layer surface is arranged in level order
    against the *running* usable box; each exclusive surface's shrink is attributed."""
    if monitor is None:
        if len(monitors) != 1:
            raise Setup("--monitor is required when the monitors reply carries %d entries"
                        % len(monitors))
        monitor = next(iter(monitors))
    if monitor not in monitors:
        raise Setup("monitor %r is not in the monitors reply" % monitor)
    if monitor not in layers:
        raise Setup("monitor %r is not in the layers reply" % monitor)
    mon = monitors[monitor]
    scale, transform = mon.get("scale"), mon.get("transform")
    if scale not in (1, 1.0) or transform not in (0, 0.0):
        raise Unmodelled("monitor %s has scale/transform %r/%r; the reply carries pixel size "
                         "and the layer box is logical, so this join is not modelled"
                         % (monitor, scale, transform))
    bar = declared_bar(config)
    allocation = dict(allocation or {})
    # every declared surface's band is resolved from this map (round 83): an entry naming a
    # namespace no declared surface carries is refused here, never silently unused
    resolved = {bar["namespace"]} | {s["namespace"] for s in extras}
    unknown = sorted(set(allocation) - resolved)
    if unknown:
        raise Setup("the allocation declaration names %s, which no declared surface carries"
                    % ", ".join(repr(name) for name in unknown))
    static = dict(static or ZERO_STATIC)
    if not output_matches(config, monitor):
        rows = [("RESULT", "monitor=%s box=NOT_ON_MONITOR reserved=NOT_APPLIED verdict=NO_BAR"
                 % monitor)]
        return "NO_BAR", 3, rows
    mon_w, mon_h = mon["width"], mon["height"]
    original = {"x": mon.get("x", 0) + static["left"], "y": mon.get("y", 0) + static["top"],
                "w": mon_w - static["left"] - static["right"],
                "h": mon_h - static["top"] - static["bottom"]}
    if original["w"] <= 0 or original["h"] <= 0:
        raise Unmodelled("the static reserved area leaves no usable box (%dx%d)"
                         % (original["w"], original["h"]))
    full = {"x": mon.get("x", 0), "y": mon.get("y", 0), "w": mon_w, "h": mon_h}
    usable = dict(original)

    bar_spec = {
        "namespace": bar["namespace"],
        "level": bar["level"],
        "position": bar["position"],
        "anchor": anchor_mask(POSITION_ANCHORS[bar["position"]]),
        "anchor_names": list(POSITION_ANCHORS[bar["position"]]),
        "height": bar["height"],
        "width": bar["width"],
        "margins": bar["margins"],
        "exclusive": "auto" if bar["exclusive"] else 0,
        "exclusiveEdge": 0,
        "order": 0,
    }
    band_axis = "height" if bar["position"] in ("top", "bottom") else "width"
    bar_spec[band_axis] = band_of(bar_spec, allocation)
    surfaces = [bar_spec] + [dict(s) for s in extras]
    # every declared surface's own band (round 83): an allocation entry for a dynamic band is
    # the client's declared allocation, resolved before the arrange order is derived from zones
    for spec in surfaces:
        axis = "height" if spec["position"] in ("top", "bottom") else "width"
        if spec[axis] == 0 and spec["namespace"] in allocation:
            spec[axis] = band_of(spec, allocation)
    order = sorted(range(len(surfaces)),
                   key=lambda i: (surfaces[i]["level"], -surfaces[i]["order"], i))
    rows = [("CONFIG", "pos=%s layer=%s level=%d ns=%s height=%d width=%d margins=%d,%d,%d,%d "
             "exclusive=%s surfaces=%d"
             % (bar["position"], bar["layer"], bar["level"], bar["namespace"], bar["height"],
                bar["width"], bar["margins"]["top"], bar["margins"]["right"],
                bar["margins"]["bottom"], bar["margins"]["left"],
                "true" if bar["exclusive"] else "false", len(surfaces))),
            ("STATIC", "monitor=%s top=%d right=%d bottom=%d left=%d source=%s"
             % (monitor, static["top"], static["right"], static["bottom"], static["left"],
                static_source))]

    boxes = []
    attribution = {}   # (namespace, edge) -> amount
    invalid_empty = []
    sequence = [i for want in (True, False) for i in order
                if (zone_for_pass(surfaces[i]) > 0) == want]
    for index in sequence:
        spec = surfaces[index]
        if spec["exclusive"] == -1:
            bounds = dict(full)
        else:
            bounds = dict(usable)
        box = cbox_round(arranged_box(spec, bounds))
        if box["w"] <= 0 or box["h"] <= 0:
            # the compositor logs and skips the surface: no box, no zone applied
            rows.append(("SKIP", "monitor=%s level=%d ns=%s box=%d,%d,%d,%d reason=empty"
                         % (monitor, spec["level"], spec["namespace"], box["x"], box["y"],
                            box["w"], box["h"])))
            boxes.append("SKIP")
            invalid_empty.append(spec["namespace"])
            continue
        zone = surface_zone(spec)
        rows.append(("DECL", "monitor=%s level=%d ns=%s box=%d,%d,%d,%d anchor=%s zone=%d"
                     % (monitor, spec["level"], spec["namespace"], box["x"], box["y"],
                        box["w"], box["h"], "+".join(spec["anchor_names"]), zone)))
        live = find_layer(layers, monitor, spec["level"], spec["namespace"])
        if live is None:
            rows.append(("LIVE", "monitor=%s level=%d ns=%s entries=0"
                         % (monitor, spec["level"], spec["namespace"])))
            boxes.append("NO_LAYER")
        else:
            try:
                live_box = {k: int(live[k]) for k in ("x", "y", "w", "h")}
            except (KeyError, TypeError, ValueError):
                raise Setup("a layers entry lacks integer x/y/w/h")
            rows.append(("LIVE", "monitor=%s level=%d ns=%s box=%d,%d,%d,%d entries=1"
                         % (monitor, spec["level"], spec["namespace"], live_box["x"],
                            live_box["y"], live_box["w"], live_box["h"])))
            boxes.append("MATCH" if live_box == box else "DIFFER")
        if zone > 0:
            edge = apply_exclusive(usable, spec, zone)
            if edge is None:
                rows.append(("ATTR", "monitor=%s level=%d ns=%s edge=none contribution=0"
                             % (monitor, spec["level"], spec["namespace"])))
            else:
                amount = zone + spec["margins"][edge]
                attribution[(spec["namespace"], edge)] = \
                    attribution.get((spec["namespace"], edge), 0) + amount
                rows.append(("ATTR", "monitor=%s level=%d ns=%s edge=%s contribution=%d box=%d,%d,%d,%d"
                             % (monitor, spec["level"], spec["namespace"], edge, amount,
                                box["x"], box["y"], box["w"], box["h"])))

    ls_valid = (usable["w"] > 0 and usable["h"] > 0 and contains_box(original, usable))
    if ls_valid:
        ls = {"left": usable["x"] - original["x"], "top": usable["y"] - original["y"],
              "right": (original["x"] + original["w"]) - (usable["x"] + usable["w"]),
              "bottom": (original["y"] + original["h"]) - (usable["y"] + usable["h"])}
    else:
        ls = dict(ZERO_STATIC)
    expected = {edge: static[edge] + ls[edge] for edge in POSITIONS}
    attributed = {edge: static[edge] + sum(
        amount for (namespace, hit), amount in attribution.items() if hit == edge)
        for edge in POSITIONS}

    edge = bar["position"]
    band = mon["reserved"][RESERVED_INDEX[edge]]
    if not bar["exclusive"] and not attribution:
        reserved_verdict = "NOT_APPLIED"
    elif band == expected[edge]:
        reserved_verdict = "EQ"
    elif band > expected[edge]:
        reserved_verdict = "GT"
    else:
        reserved_verdict = "DIFFER"
    bar_box = boxes[sequence.index(0)] if 0 in sequence else "NO_LAYER"
    if bar_box == "DIFFER" or reserved_verdict == "DIFFER":
        verdict, rc = "DIFFER", 1
    elif any(state in ("DIFFER", "NO_LAYER") for state in boxes):
        verdict, rc = "DIFFER", 1
    else:
        verdict, rc = "CLEAN", 0
    vector = lambda area: "%d,%d,%d,%d" % (area["left"], area["top"], area["right"],
                                           area["bottom"])
    rows.append(("RESULT", "monitor=%s box=%s boxes=%s reserved=%s band=%d expected=%d "
                 "attributed=%d gt=%s attr=%s ls=%s verdict=%s"
                 % (monitor, bar_box, ",".join(boxes), reserved_verdict, band,
                    expected[edge], attributed[edge],
                    "%d,%d,%d,%d" % (mon["reserved"][0], mon["reserved"][1],
                                     mon["reserved"][2], mon["reserved"][3]),
                    vector(attributed), "VALID" if ls_valid else "INVALID", verdict)))
    return verdict, rc, rows


def parse_layers(raw):
    data = load_json(raw, "layers")
    if not isinstance(data, dict):
        raise Setup("layers reply is not an object keyed by monitor")
    return data


def parse_monitors(raw):
    data = load_json(raw, "monitors")
    if not isinstance(data, list):
        raise Setup("monitors reply is not a list")
    monitors = {}
    for item in data:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            raise Setup("monitors reply carries a non-object or nameless entry")
        reserved = item.get("reserved")
        if not isinstance(reserved, list) or len(reserved) != 4 or not all(
            isinstance(v, int) and not isinstance(v, bool) for v in reserved
        ):
            raise Setup("monitors reply carries a malformed reserved array")
        if not isinstance(item.get("width"), int) or not isinstance(item.get("height"), int):
            raise Setup("monitors reply carries a non-integer size")
        for axis in ("x", "y"):
            if axis in item and (not isinstance(item[axis], int)
                                 or isinstance(item[axis], bool)):
                raise Setup("monitors reply carries a non-integer %s" % axis)
        item.setdefault("x", 0)
        item.setdefault("y", 0)
        monitors[item["name"]] = item
    return monitors


def find_layer(layers, monitor, level, namespace):
    levels = layers.get(monitor, {}).get("levels")
    if not isinstance(levels, dict):
        return None
    entries = levels.get(str(level))
    if not isinstance(entries, list):
        return None
    hits = [e for e in entries if isinstance(e, dict) and e.get("namespace") == namespace]
    if len(hits) > 1:
        raise Unmodelled("more than one %r layer on monitor %s level %d"
                         % (namespace, monitor, level))
    return hits[0] if hits else None


def evaluate(config, layers, monitors, monitor=None, static=None, static_source="none",
             surfaces=None, allocation=None):
    allocation = dict(allocation or {})
    if surfaces:
        return evaluate_composition(config, layers, monitors, monitor, static, static_source,
                                    surfaces, allocation)
    bar = declared_bar(config)
    unknown = sorted(set(allocation) - {bar["namespace"]})
    if unknown:
        raise Setup("the allocation declaration names %s, which the join does not resolve "
                    "(only the bar's band is resolved)" % ", ".join(repr(name) for name in unknown))
    static = dict(static or ZERO_STATIC)
    if monitor is None:
        if len(monitors) != 1:
            raise Setup("--monitor is required when the monitors reply carries %d entries"
                        % len(monitors))
        monitor = next(iter(monitors))
    if monitor not in monitors:
        raise Setup("monitor %r is not in the monitors reply" % monitor)
    if monitor not in layers:
        raise Setup("monitor %r is not in the layers reply" % monitor)
    mon = monitors[monitor]
    scale, transform = mon.get("scale"), mon.get("transform")
    if scale not in (1, 1.0) or transform not in (0, 0.0):
        raise Unmodelled("monitor %s has scale/transform %r/%r; the reply carries pixel size "
                         "and the layer box is logical, so this join is not modelled"
                         % (monitor, scale, transform))
    mon_w, mon_h = mon["width"], mon["height"]
    # logicalBox() = {position, size}; the usable box starts at the monitor's layout origin
    usable = {"x": mon.get("x", 0) + static["left"], "y": mon.get("y", 0) + static["top"],
              "w": mon_w - static["left"] - static["right"],
              "h": mon_h - static["top"] - static["bottom"]}
    if usable["w"] <= 0 or usable["h"] <= 0:
        raise Unmodelled("the static reserved area leaves no usable box (%dx%d)"
                         % (usable["w"], usable["h"]))

    rows = [("CONFIG", "pos=%s layer=%s level=%d ns=%s height=%d width=%d margins=%d,%d,%d,%d exclusive=%s"
             % (bar["position"], bar["layer"], bar["level"], bar["namespace"], bar["height"],
                bar["width"], bar["margins"]["top"], bar["margins"]["right"],
                bar["margins"]["bottom"], bar["margins"]["left"],
                "true" if bar["exclusive"] else "false")),
            ("STATIC", "monitor=%s top=%d right=%d bottom=%d left=%d source=%s"
             % (monitor, static["top"], static["right"], static["bottom"], static["left"],
                static_source))]

    if not output_matches(config, monitor):
        rows.append(("RESULT", "monitor=%s box=NOT_ON_MONITOR reserved=NOT_APPLIED verdict=NO_BAR" % monitor))
        return "NO_BAR", 3, rows

    local = declared_box(bar, usable["w"], usable["h"], allocation)
    box = {"x": local["x"] + usable["x"], "y": local["y"] + usable["y"],
           "w": local["w"], "h": local["h"]}
    rows.append(("DECL", "monitor=%s box=%d,%d,%d,%d edge=%s"
                 % (monitor, box["x"], box["y"], box["w"], box["h"], bar["position"])))

    live = find_layer(layers, monitor, bar["level"], bar["namespace"])
    if live is None:
        rows.append(("LIVE", "monitor=%s level=%d ns=%s entries=0"
                     % (monitor, bar["level"], bar["namespace"])))
        rows.append(("RESULT", "monitor=%s box=NO_LAYER reserved=NOT_CHECKED verdict=NO_LAYER" % monitor))
        return "NO_LAYER", 3, rows

    try:
        live_box = {k: int(live[k]) for k in ("x", "y", "w", "h")}
    except (KeyError, TypeError, ValueError):
        raise Setup("a layers entry lacks integer x/y/w/h")
    rows.append(("LIVE", "monitor=%s level=%d ns=%s box=%d,%d,%d,%d entries=1"
                 % (monitor, bar["level"], bar["namespace"], live_box["x"], live_box["y"],
                    live_box["w"], live_box["h"])))

    box_verdict = "MATCH" if live_box == box else "DIFFER"

    extent = edge_extent(bar, box, usable)
    edge = bar["position"]
    band = mon["reserved"][RESERVED_INDEX[edge]]
    contained = (box["x"] >= usable["x"] and box["y"] >= usable["y"]
                 and box["x"] + box["w"] <= usable["x"] + usable["w"]
                 and box["y"] + box["h"] <= usable["y"] + usable["h"])
    # the layer region starts at the usable origin and extends by the band; when that region
    # leaves the usable box the parent/child constructor returns zeros (ReservedArea.cpp:19-30)
    # and the monitor reserves nothing for this surface
    axis_size = usable["h"] if edge in ("top", "bottom") else usable["w"]
    if extent + bar["margins"][OPPOSITE_EDGE[edge]] > axis_size:
        contained = False
    # CReservedArea(parent, child) is empty when the child is not contained (S459:19-31);
    # the static band survives either way (CReservedArea::calculate sums static + dynamic)
    contribution = (extent + bar["margins"][OPPOSITE_EDGE[edge]]) if contained else 0
    expected = static[edge] + contribution
    if not bar["exclusive"]:
        reserved_verdict = "NOT_APPLIED"
    elif band == expected:
        reserved_verdict = "EQ"
    elif band > expected:
        reserved_verdict = "GT"
    else:
        reserved_verdict = "DIFFER"

    if box_verdict == "DIFFER" or reserved_verdict == "DIFFER":
        verdict, rc = "DIFFER", 1
    else:
        verdict, rc = "CLEAN", 0
    rows.append(("RESULT", "monitor=%s box=%s reserved=%s band=%d expected=%d verdict=%s"
                 % (monitor, box_verdict, reserved_verdict, band, expected, verdict)))
    return verdict, rc, rows


def emit(rows, verdict):
    for kind, text in rows:
        print("MADO_BARFOOT_%s: %s" % (kind, text))
    print("MADO_BARFOOT: verdict=%s" % verdict)


def selftest():
    import tempfile
    checks = 0
    total = 0

    def ok(cond, label):
        nonlocal checks, total
        total += 1
        if cond:
            checks += 1
        else:
            print("MADO_BARFOOT_SELFTEST_FAIL: %s" % label)

    def case(config, layers, monitors, monitor=None, static=None, source="none"):
        return evaluate(config, layers, monitors, monitor, static, source)

    mon = {"name": "M1", "width": 3440, "height": 1440, "reserved": [0, 26, 0, 0], "scale": 1.0, "transform": 0}
    monitors = {"M1": mon}
    layers_top = {"M1": {"levels": {"0": [], "1": [], "2": [
        {"namespace": "waybar", "x": 0, "y": 0, "w": 3440, "h": 26, "alpha": 1, "pid": 1}], "3": []}}}
    base = {"position": "top", "layer": "top", "height": 26}
    v, rc, _ = case(base, layers_top, monitors)
    ok((v, rc) == ("CLEAN", 0), "host-top clean")

    # margin integer
    ok(parse_margins({"margin": 4}) == {"top": 4, "right": 4, "bottom": 4, "left": 4}, "margin int")
    # CSS two-value string
    ok(parse_margins({"margin": "4 8"}) == {"top": 4, "right": 8, "bottom": 4, "left": 8}, "margin 2")
    # CSS three-value string
    ok(parse_margins({"margin": "1 2 3"}) == {"top": 1, "right": 2, "bottom": 3, "left": 2}, "margin 3")
    # per-side wins over margin
    ok(parse_margins({"margin": 9, "margin-top": 2}) == {"top": 2, "right": 0, "bottom": 0, "left": 0},
       "margin-* precedence")
    # comments and trailing commas
    ok(load_jsonc(b'{ // x\n "a": 1, /* y */ }', "t") == {"a": 1}, "jsonc strip")

    # bottom bar box
    mon_b = {"name": "M1", "width": 1920, "height": 1080, "reserved": [0, 0, 0, 30], "scale": 1.0, "transform": 0}
    layers_b = {"M1": {"levels": {"0": [], "1": [], "2": [
        {"namespace": "waybar", "x": 0, "y": 1050, "w": 1920, "h": 30, "alpha": 1, "pid": 1}], "3": []}}}
    v, rc, _ = case({"position": "bottom", "layer": "top", "height": 30}, layers_b, {"M1": mon_b})
    ok((v, rc) == ("CLEAN", 0), "bottom clean")

    # exclusive false -> NOT_APPLIED
    v, rc, rows = case({"position": "top", "layer": "top", "height": 26, "exclusive": False},
                       layers_top, {"M1": {"name": "M1", "width": 3440, "height": 1440,
                                           "reserved": [0, 0, 0, 0], "scale": 1.0, "transform": 0}})
    ok(v == "CLEAN" and any("reserved=NOT_APPLIED" in t for _, t in rows), "exclusive false")

    # drift in the live box
    layers_drift = {"M1": {"levels": {"0": [], "1": [], "2": [
        {"namespace": "waybar", "x": 0, "y": 0, "w": 3440, "h": 28, "alpha": 1, "pid": 1}], "3": []}}}
    v, rc, _ = case(base, layers_drift, {"M1": {"name": "M1", "width": 3440, "height": 1440,
                                                "reserved": [0, 28, 0, 0], "scale": 1.0, "transform": 0}})
    ok((v, rc) == ("DIFFER", 1), "box drift differ")

    # reserved smaller than the footprint
    v, rc, _ = case(base, layers_top, {"M1": {"name": "M1", "width": 3440, "height": 1440,
                                              "reserved": [0, 0, 0, 0], "scale": 1.0, "transform": 0}})
    ok((v, rc) == ("DIFFER", 1), "reserved differ")

    # reserved greater than the footprint is admissible
    v, rc, rows = case(base, layers_top, {"M1": {"name": "M1", "width": 3440, "height": 1440,
                                                 "reserved": [0, 40, 0, 0], "scale": 1.0, "transform": 0}})
    ok(v == "CLEAN" and any("reserved=GT" in t for _, t in rows), "reserved gt")

    # declared level has no entry
    v, rc, _ = case({"position": "top", "layer": "bottom", "height": 26}, layers_top, monitors)
    ok((v, rc) == ("NO_LAYER", 3), "level miss")

    # the margined band composes the anchored-edge extent plus the opposite margin
    v, rc, rows = case({"position": "top", "layer": "top", "height": 26, "margin": "4 0"},
                       {"M1": {"levels": {"0": [], "1": [], "2": [
                           {"namespace": "waybar", "x": 0, "y": 4, "w": 3440, "h": 26,
                            "alpha": 1, "pid": 1}], "3": []}}},
                       {"M1": {"name": "M1", "width": 3440, "height": 1440, "reserved": [0, 34, 0, 0], "scale": 1.0, "transform": 0}})
    ok(v == "CLEAN" and any("reserved=EQ band=34 expected=34" in t for _, t in rows), "top margin band eq")
    v, rc, rows = case({"position": "top", "layer": "top", "height": 26, "margin": "4 0"},
                       {"M1": {"levels": {"0": [], "1": [], "2": [
                           {"namespace": "waybar", "x": 0, "y": 4, "w": 3440, "h": 26,
                            "alpha": 1, "pid": 1}], "3": []}}},
                       {"M1": {"name": "M1", "width": 3440, "height": 1440, "reserved": [0, 26, 0, 0], "scale": 1.0, "transform": 0}})
    ok(v == "DIFFER" and rc == 1, "top margin band differ")
    # a horizontal margin never enters a horizontal bar's vertical band; it only moves the box
    v, rc, rows = case({"position": "top", "layer": "top", "height": 30, "margin": "4 8"},
                       {"M1": {"levels": {"0": [], "1": [], "2": [
                           {"namespace": "waybar", "x": 8, "y": 4, "w": 1904, "h": 30,
                            "alpha": 1, "pid": 1}], "3": []}}},
                       {"M1": {"name": "M1", "width": 1920, "height": 1080, "reserved": [0, 38, 0, 0], "scale": 1.0, "transform": 0}})
    ok(v == "CLEAN" and any("box=MATCH reserved=EQ band=38 expected=38" in t for _, t in rows),
       "cross-axis margin stays out of the band")
    # transposed rule: a left bar's band is width + left + right margins
    v, rc, rows = case({"position": "left", "layer": "top", "width": 40, "margin": 6},
                       {"M1": {"levels": {"0": [], "1": [], "2": [
                           {"namespace": "waybar", "x": 6, "y": 6, "w": 40, "h": 1428,
                            "alpha": 1, "pid": 1}], "3": []}}},
                       {"M1": {"name": "M1", "width": 3440, "height": 1440, "reserved": [52, 0, 0, 0], "scale": 1.0, "transform": 0}})
    ok(v == "CLEAN" and any("reserved=EQ band=52 expected=52" in t for _, t in rows), "left margin band eq")
    # a negative margin is refused, never composed
    try:
        declared_bar({"position": "top", "height": 26, "margin": "-2 0"})
        ok(False, "negative margin refused")
    except Unmodelled:
        ok(True, "negative margin refused")

    # centred explicit width
    v, rc, rows = case({"position": "top", "layer": "top", "height": 26, "width": 800},
                       {"M1": {"levels": {"0": [], "1": [], "2": [
                           {"namespace": "waybar", "x": 1320, "y": 0, "w": 800, "h": 26,
                            "alpha": 1, "pid": 1}], "3": []}}}, monitors)
    ok(v == "CLEAN", "centred width")

    # output exclusion
    v, rc, _ = case({"position": "top", "layer": "top", "height": 26, "output": "!M1"}, layers_top, monitors)
    ok((v, rc) == ("NO_BAR", 3), "output exclusion")

    # namespace from name
    layers_named = {"M1": {"levels": {"0": [], "1": [], "2": [
        {"namespace": "bar2", "x": 0, "y": 0, "w": 3440, "h": 26, "alpha": 1, "pid": 1}], "3": []}}}
    v, rc, _ = case({"position": "top", "layer": "top", "height": 26, "name": "bar2"},
                    layers_named, monitors)
    ok((v, rc) == ("CLEAN", 0), "namespace name")

    # round 78 repairs: waybar's output branches, std::stoi margins, rounding, overflow
    v, rc, _ = case({"position": "top", "layer": "top", "height": 26, "output": ["!M2"]},
                    layers_top, monitors)
    ok((v, rc) == ("NO_BAR", 3), "output array without a positive entry")
    v, rc, _ = case({"position": "top", "layer": "top", "height": 26, "output": ["M1", "!M1"]},
                    layers_top, monitors)
    ok((v, rc) == ("CLEAN", 0), "output array first positive wins")
    v, rc, _ = case({"position": "top", "layer": "top", "height": 26, "output": ""},
                    layers_top, monitors)
    ok((v, rc) == ("CLEAN", 0), "empty output string means every output")
    ok(parse_margins({"margin": "4px 0"}) == {"top": 4, "right": 0, "bottom": 4, "left": 0},
       "margin stoi prefix parse")
    layers_odd = {"M1": {"levels": {"0": [], "1": [], "2": [
        {"namespace": "waybar", "x": 1320, "y": 0, "w": 801, "h": 26, "alpha": 1, "pid": 1}],
        "3": []}}}
    v, rc, rows = case({"position": "top", "layer": "top", "height": 26, "width": 801},
                       layers_odd, monitors)
    ok(v == "CLEAN" and any("box=MATCH" in t for _, t in rows), "odd centring rounds like std::round")
    layers_over = {"M1": {"levels": {"0": [], "1": [], "2": [
        {"namespace": "waybar", "x": 0, "y": 0, "w": 1920, "h": 120, "alpha": 1, "pid": 1}],
        "3": []}}}
    v, rc, rows = case({"position": "top", "layer": "top", "height": 120},
                       layers_over,
                       {"M1": {"name": "M1", "width": 1920, "height": 100,
                               "reserved": [0, 0, 0, 0], "scale": 1.0, "transform": 0}})
    ok(v == "CLEAN" and any("expected=0" in t for _, t in rows), "an overflowing bar reserves nothing")

    # round 79: the static `addreserved` band composes under the bar's own contribution
    ok(parse_static_reserve("monitor = M1, 3440x1440@100, 0x0, 1\n"
                            "monitor = M1, addreserved, 26, 0, 0, 0\n", "M1")
       == {"top": 26, "right": 0, "bottom": 0, "left": 0},
       "static addreserved parses top bottom left right")
    ok(parse_static_reserve("monitor = M1, addreserved, 26, 0, 0, 0\n", "M1") == ZERO_STATIC,
       "an addreserved with no prior selector rule drops its area")
    ok(parse_static_reserve("monitor = M2, addreserved, 5, 0, 0, 0\n", "M1") == ZERO_STATIC,
       "another selector does not reserve")
    ok(parse_static_reserve("monitor = M1, 3440x1440@100, 0x0, 1\n"
                            "monitor = M1, addreserved, 10, 0, 0, 0\n"
                            "monitor = M1, addreserved, 26, 0, 0, 0\n", "M1")["top"] == 26,
       "the later addreserved wins")
    ok(parse_static_reserve("monitor = M1, addreserved, 26, 0, 0, 0\n"
                            "monitor = M1, 3440x1440@100, 0x0, 1\n", "M1") == ZERO_STATIC,
       "a later positional rule replaces the reserved rule")
    ok(parse_static_reserve("monitor = M1, 3440x1440@100, 0x0, 1\n"
                            "monitor = M1, addreserved, 26, 0, 0, 0\n"
                            "monitor = M1, 3440x1440, 0x0, 1, sdr_eotf, 1\n", "M1")["top"] == 26,
       "a dropped positional rule keeps the reserved area")
    ok(parse_static_reserve("# monitor = M1, addreserved, 99, 0, 0, 0\n", "M1") == ZERO_STATIC,
       "a commented rule is not a rule")
    ok(parse_static_reserve("monitor = M1, 3440x1440@100, 0x0, 1 # prior\n"
                            "monitor = M1, addreserved, 26, 0, 0, 0 # a comment\n", "M1")["top"]
       == 26, "a trailing comment is not part of the rule")
    for label, bad in (
        ("bad addreserved field", "monitor = M1, addreserved, x, 0, 0, 0\n"),
        ("short addreserved", "monitor = M1, addreserved, 1, 2, 3\n"),
        ("a source line", "source = ~/.config/hypr/other.conf\n"),
        ("a variable rule", "monitor = $MON, 3440x1440, 0x0, 1\n"),
    ):
        try:
            parse_static_reserve(bad, "M1")
            ok(False, "refused %s" % label)
        except Unmodelled:
            ok(True, "refused %s" % label)

    static26 = {"top": 26, "right": 0, "bottom": 0, "left": 0}
    layers_static = {"M1": {"levels": {"0": [], "1": [], "2": [
        {"namespace": "waybar", "x": 4, "y": 30, "w": 3432, "h": 26, "alpha": 1, "pid": 1}],
        "3": []}}}
    v, rc, rows = case({"position": "top", "layer": "top", "height": 26, "margin": 4},
                       layers_static,
                       {"M1": {"name": "M1", "width": 3440, "height": 1440,
                               "reserved": [0, 60, 0, 0], "scale": 1.0, "transform": 0}},
                       None, static26, "rules")
    ok(v == "CLEAN" and any("box=MATCH reserved=EQ band=60 expected=60" in t for _, t in rows),
       "static reserve composes with the bar band")
    v, rc, rows = case({"position": "top", "layer": "top", "height": 26, "exclusive": False},
                       {"M1": {"levels": {"0": [], "1": [], "2": [
                           {"namespace": "waybar", "x": 0, "y": 26, "w": 3440, "h": 26,
                            "alpha": 1, "pid": 1}], "3": []}}},
                       {"M1": {"name": "M1", "width": 3440, "height": 1440,
                               "reserved": [0, 26, 0, 0], "scale": 1.0, "transform": 0}},
                       None, static26, "rules")
    ok(v == "CLEAN" and any("reserved=NOT_APPLIED band=26 expected=52" in t for _, t in rows),
       "static reserve enters the printed expectation when not applied")
    static_left = {"top": 0, "right": 0, "bottom": 0, "left": 40}
    v, rc, rows = case({"position": "top", "layer": "top", "height": 26},
                       {"M1": {"levels": {"0": [], "1": [], "2": [
                           {"namespace": "waybar", "x": 40, "y": 0, "w": 3400, "h": 26,
                            "alpha": 1, "pid": 1}], "3": []}}},
                       {"M1": {"name": "M1", "width": 3440, "height": 1440,
                               "reserved": [40, 26, 0, 0], "scale": 1.0, "transform": 0}},
                       None, static_left, "rules")
    ok(v == "CLEAN" and any("box=MATCH reserved=EQ band=26 expected=26" in t for _, t in rows),
       "a static left reserve moves the box only")
    try:
        case({"position": "top", "height": 26}, layers_top, monitors, None,
             {"top": 1440, "right": 0, "bottom": 0, "left": 0}, "rules")
        ok(False, "empty usable box refused")
    except Unmodelled:
        ok(True, "empty usable box refused")

    # round 79 repair R2 (wave R79ScoutModel A/B/C/D/E): origin, clamp, selectors, band overflow,
    # transform with no rule
    origin_mon = {"name": "M2", "width": 1920, "height": 1080, "reserved": [0, 26, 0, 0],
                  "scale": 1.0, "transform": 0, "x": 1920, "y": 0}
    v, rc, rows = case({"position": "top", "layer": "top", "height": 26},
                       {"M2": {"levels": {"0": [], "1": [], "2": [
                           {"namespace": "waybar", "x": 1920, "y": 0, "w": 1920, "h": 26,
                            "alpha": 1, "pid": 1}], "3": []}}},
                       {"M2": origin_mon})
    ok(v == "CLEAN" and any("box=1920,0,1920,26" in t for _, t in rows),
       "the monitor's layout origin moves the box")
    ok(parse_static_reserve("monitor = M1, 1920x1080@100, 0x0, 1\n"
                            "monitor = M1, addreserved, 0, -30, 0, 0\n", "M1") == ZERO_STATIC,
       "a negative addreserved field clamps at zero")
    for label, bad in (
        ("a desc selector", "monitor = desc:Dell U2720Q, addreserved, 26, 0, 0, 0\n"),
        ("an empty selector", "monitor = , preferred, auto, auto\n"),
    ):
        try:
            parse_static_reserve(bad, "M1")
            ok(False, "refused %s" % label)
        except Unmodelled:
            ok(True, "refused %s" % label)
    v, rc, rows = case({"position": "top", "layer": "top", "height": 26,
                        "margin-top": 4, "margin-bottom": 80},
                       {"M1": {"levels": {"0": [], "1": [], "2": [
                           {"namespace": "waybar", "x": 0, "y": 4, "w": 1920, "h": 26,
                            "alpha": 1, "pid": 1}], "3": []}}},
                       {"M1": {"name": "M1", "width": 1920, "height": 100,
                               "reserved": [0, 0, 0, 0], "scale": 1.0, "transform": 0}})
    ok(v == "CLEAN" and any("reserved=EQ band=0 expected=0" in t for _, t in rows),
       "a band that overflows the usable box reserves nothing")
    ok(parse_static_reserve("monitor = M1, transform, 1\n"
                            "monitor = M1, addreserved, 26, 0, 0, 0\n", "M1") == ZERO_STATIC,
       "a transform with no rule adds nothing, so the later addreserved drops")

    # malformed inputs are setup errors, never verdicts
    with tempfile.TemporaryDirectory() as td:
        bad = os.path.join(td, "bad.json")
        with open(bad, "w") as fh:
            fh.write("{not json")
        try:
            load_json(read_bytes(bad), "layers")
            ok(False, "malformed json refused")
        except Setup:
            ok(True, "malformed json refused")
        try:
            read_bytes(td)
            ok(False, "directory refused")
        except Setup:
            ok(True, "directory refused")

    # --- r80: arranged_box reproduces declared_box on the bar's own specification grid ---
    for pos in POSITIONS:
        for width in (0, 120, 1200):
            for height in (0, 26, 300):
                for margin in (0, 4):
                    if (pos in ("top", "bottom") and height == 0) or \
                            (pos in ("left", "right") and width == 0):
                        continue  # declared_box refuses the bar's dynamic band-axis size
                    sides = dict((side, margin) for side in MARGIN_SIDES)
                    bar = {"position": pos, "height": height, "width": width,
                           "margins": sides}
                    spec = {"position": pos, "anchor": anchor_mask(POSITION_ANCHORS[pos]),
                            "height": height, "width": width, "margins": sides}
                    ok(arranged_box(spec, {"x": 0, "y": 0, "w": 1920, "h": 1080})
                       == declared_box(bar, 1920, 1080),
                       "arranged_box = declared_box %s %dx%d m%d" % (pos, width, height,
                                                                     margin))

    def comp(config, level_entries, reserved, extras, static=None, allocation=None):
        layers = {"M1": {"levels": dict((str(i), []) for i in range(4))}}
        for level, entries in level_entries.items():
            layers["M1"]["levels"][str(level)] = entries
        mon = {"name": "M1", "width": 1000, "height": 800, "reserved": reserved,
               "scale": 1, "transform": 0}
        return evaluate(config, layers, {"M1": mon}, "M1", static, "rules",
                        parse_surfaces(json.dumps(list(extras)).encode()), allocation)

    def line(verdict_rows, prefix):
        return [text for kind, text in verdict_rows if kind == prefix]

    top = {"position": "top", "layer": "top", "height": 26}
    waybar = {"namespace": "waybar", "x": 0, "y": 0, "w": 1000, "h": 26}
    panel2 = {"namespace": "panel", "x": 0, "y": 26, "w": 1000, "h": 40}

    # a later level is arranged against the box the earlier level already shrank
    v, rc, rows = comp(top, {2: [waybar], 3: [panel2]}, [0, 66, 0, 0],
                       [{"namespace": "panel", "level": 3, "height": 40}])
    ok((v, rc) == ("CLEAN", 0) and any("attributed=66" in text and "boxes=MATCH,MATCH" in text
                                       and "band=66 expected=66" in text
                                       for text in line(rows, "RESULT")),
       "overlay composes on top of the bar")
    # ... and an earlier level moves the bar's own box
    v, rc, rows = comp(top, {1: [{"namespace": "panel", "x": 0, "y": 0, "w": 1000, "h": 40}],
                             2: [{"namespace": "waybar", "x": 0, "y": 40, "w": 1000, "h": 26}]},
                       [0, 66, 0, 0],
                       [{"namespace": "panel", "level": 1, "height": 40}])
    ok((v, rc) == ("CLEAN", 0)
       and any("ns=waybar box=0,40,1000,26" in text for text in line(rows, "DECL")),
       "a lower level shifts the bar's box")
    # a negative margin can cancel the zone: exclusive + margin must stay > 0
    v, rc, rows = comp(top, {2: [waybar], 3: [{"namespace": "panel", "x": 0, "y": 14,
                                               "w": 1000, "h": 100}]}, [0, 26, 0, 0],
                       [{"namespace": "panel", "level": 3, "height": 100, "exclusive": 12,
                         "margins": {"top": -12}}])
    ok((v, rc) == ("CLEAN", 0)
       and any("ns=panel edge=none contribution=0" in text for text in line(rows, "ATTR")),
       "zone plus margin at zero reserves nothing")
    # an exclusive zone on an anchor mask no rule matches reserves nothing
    v, rc, rows = comp(top, {2: [waybar], 3: [{"namespace": "panel", "x": 800, "y": 26,
                                               "w": 200, "h": 100}]}, [0, 26, 0, 0],
                       [{"namespace": "panel", "level": 3, "height": 100, "width": 200,
                         "anchor": ["top", "right"], "exclusive": 30}])
    ok((v, rc) == ("CLEAN", 0)
       and any("edge=none contribution=0" in text for text in line(rows, "ATTR")),
       "an unmatched anchor mask reserves nothing")
    # ... while the same declaration with a matching exclusive edge does reserve
    v, rc, rows = comp(top, {2: [waybar], 3: [{"namespace": "panel", "x": 800, "y": 26,
                                               "w": 200, "h": 100}]}, [0, 56, 0, 0],
                       [{"namespace": "panel", "level": 3, "height": 100, "width": 200,
                         "anchor": ["top", "right"], "exclusive": 30,
                         "exclusiveEdge": "top"}])
    ok((v, rc) == ("CLEAN", 0)
       and any("ns=panel edge=top contribution=30" in text for text in line(rows, "ATTR")),
       "an exclusive edge matching the anchor reserves")
    # exclusive -1 arranges against the full monitor box, not the usable one
    v, rc, rows = comp(top, {2: [waybar], 3: [{"namespace": "panel", "x": 800, "y": 700,
                                               "w": 200, "h": 100}]}, [0, 26, 0, 0],
                       [{"namespace": "panel", "level": 3, "height": 100, "width": 200,
                         "anchor": ["bottom", "right"], "exclusive": -1}])
    ok((v, rc) == ("CLEAN", 0)
       and any("ns=panel box=800,700,200,100" in text for text in line(rows, "DECL")),
       "exclusive -1 uses the full monitor box")
    # an empty arranged box is skipped: no zone, no attribution
    v, rc, rows = comp(top, {2: [waybar], 3: []}, [0, 26, 0, 0],
                       [{"namespace": "panel", "level": 3, "height": 0,
                         "margins": {"top": 1000}}])
    ok((v, rc) == ("CLEAN", 0) and line(rows, "SKIP")
       and any("attributed=26" in text for text in line(rows, "RESULT")),
       "an empty box is skipped")
    # a zone larger than the axis voids the whole layer reserve (the area guard)
    v, rc, rows = comp(top, {2: [waybar], 3: [{"namespace": "panel", "x": 0, "y": 26,
                                               "w": 1000, "h": 100}]}, [0, 0, 0, 0],
                       [{"namespace": "panel", "level": 3, "height": 100,
                         "exclusive": 2000}])
    ok((v, rc) == ("CLEAN", 0)
       and any("band=0 expected=0 attributed=2026" in text and "ls=INVALID" in text
               for text in line(rows, "RESULT")),
       "an invalid layer area zeroes the whole layer reserve")

    # the surfaces declaration refuses what the protocol refuses
    for label, item in (
            ("level", {"namespace": "p", "level": 4}),
            ("anchor", {"namespace": "p", "level": 3, "anchor": ["middle"]}),
            ("edge-outside-anchor", {"namespace": "p", "level": 3, "anchor": ["top"],
                                     "exclusiveEdge": "bottom"}),
            ("margin", {"namespace": "p", "level": 3, "margins": {"top": "4"}}),
            ("exclusive", {"namespace": "p", "level": 3, "exclusive": "max"})):
        try:
            parse_surfaces(json.dumps([item]).encode())
            ok(False, "surfaces refuse %s" % label)
        except (Setup, Unmodelled):
            ok(True, "surfaces refuse %s" % label)

    # r81: CBox::round (hyprutils src/math/Box.cpp:51-63, v0.14.0)
    ok(cbox_round({"x": -0.5, "y": 363.0, "w": 1001.0, "h": 100.0})
       == {"x": -1, "y": 363, "w": 1002, "h": 100}, "cbox round negative tie")
    ok(cbox_round({"x": 399.5, "y": 0.0, "w": 201.0, "h": 26.0})
       == {"x": 400, "y": 0, "w": 201, "h": 26}, "cbox round positive half")
    ok(std_round(-0.5) == -1 and std_round(0.5) == 1 and std_round(398.5) == 399,
       "std round half away from zero")

    # r81: the auto gate (gtk-layer-shell src/layer-surface.c:264-292, v0.10.1)
    def zone(names, height=100, width=200, margins=None):
        return surface_zone({
            "anchor": anchor_mask(names), "height": height, "width": width,
            "exclusive": "auto",
            "margins": margins or {s: 0 for s in MARGIN_SIDES}})

    ok(zone(["top", "left", "right"]) == 100, "auto zone on a horizontal band")
    ok(zone(["left"], width=40, height=0) == 40, "auto zone on a vertical band")
    ok(zone(["top", "left"]) == 0, "auto zone refused on a corner")
    ok(zone(["top", "bottom", "left", "right"]) == 0, "auto zone refused on all four anchors")
    ok(zone(["top", "bottom"]) == 0, "auto zone refused on a parallel pair")
    ok(zone(["top", "left", "right"],
            margins={"top": 1, "right": 2, "bottom": 3, "left": 4}) == 103,
       "auto zone adds the unanchored margins")
    try:
        zone(["top", "left", "right"], height=0)
        ok(False, "a dynamic auto band is refused")
    except Unmodelled:
        ok(True, "a dynamic auto band is refused")

    # r82: the client allocation is a declared input (S481: a zero width/height is the
    # client's own size), so a dynamic band becomes a modelled box and a zero or absent
    # allocation stays a refusal
    for pos, band, want in (("top", 34, {"x": 0, "y": 0, "w": 3440, "h": 34}),
                            ("bottom", 30, {"x": 0, "y": 1410, "w": 3440, "h": 30}),
                            ("left", 60, {"x": 0, "y": 0, "w": 60, "h": 1440}),
                            ("right", 50, {"x": 3390, "y": 0, "w": 50, "h": 1440})):
        spec = {"namespace": "waybar", "position": pos, "height": 0, "width": 0,
                "margins": {s: 0 for s in MARGIN_SIDES}}
        ok(declared_box(spec, 3440, 1440, {"waybar": band}) == want,
           "declared box from the allocation on a %s surface" % pos)
    ok(declared_box({"namespace": "waybar", "position": "top", "height": 26, "width": 0,
                     "margins": {s: 0 for s in MARGIN_SIDES}}, 3440, 1440,
                    {"waybar": 34})["h"] == 26,
       "a declared band is not overridden by the allocation")
    try:
        band_of({"namespace": "w", "position": "top", "height": 0, "width": 0}, {})
        ok(False, "a dynamic band with no allocation is refused")
    except Unmodelled:
        ok(True, "a dynamic band with no allocation is refused")
    try:
        band_of({"namespace": "w", "position": "top", "height": 0, "width": 0}, {"w": 0})
        ok(False, "a zero allocation is refused")
    except Unmodelled:
        ok(True, "a zero allocation is refused")
    ok(band_of({"namespace": "w", "position": "left", "height": 0, "width": 70},
               {"w": 9}) == 70, "the vertical band axis is the width")
    ok(parse_allocation(b'{"waybar": 34}') == {"waybar": 34}, "allocation parses")

    # r83: every declared surface's band axis resolves from the same map, at its own turn
    v, rc, rows = comp({"position": "top", "layer": "top", "height": 26},
                       {2: [waybar], 3: [{"namespace": "panel", "x": 0, "y": 26,
                                          "w": 1000, "h": 40}]},
                       [0, 66, 0, 0],
                       [{"namespace": "panel", "level": 3, "height": 0, "exclusive": "auto"}],
                       allocation={"panel": 40})
    ok((v, rc) == ("CLEAN", 0)
       and any("ns=panel box=0,26,1000,40 anchor=top+left+right zone=40" in text
               for text in line(rows, "DECL")),
       "a declared surface's dynamic band resolves from the allocation")
    v, rc, rows = comp({"position": "top", "layer": "top", "height": 26},
                       {2: [waybar], 3: [{"namespace": "panel", "x": 0, "y": 26,
                                          "w": 1000, "h": 774}]},
                       [0, 66, 0, 0],
                       [{"namespace": "panel", "level": 3, "height": 0, "exclusive": 40}])
    ok((v, rc) == ("CLEAN", 0)
       and any("ns=panel box=0,26,1000,774" in text and "zone=40" in text
               for text in line(rows, "DECL")),
       "an unallocated dynamic band with an explicit zone keeps the assign branch")
    try:
        comp(top, {2: [waybar], 3: []}, [0, 26, 0, 0], [], allocation={"nope": 3})
        ok(False, "an allocation naming no declared surface is refused")
    except Setup:
        ok(True, "an allocation naming no declared surface is refused")
    for label, raw in (("a negative band", b'{"w": -1}'),
                       ("a non-integer band", b'{"w": "x"}'),
                       ("a non-object", b'[34]')):
        try:
            parse_allocation(raw)
            ok(False, "allocation refuses %s" % label)
        except Setup:
            ok(True, "allocation refuses %s" % label)

    print("MADO_BARFOOT_SELFTEST: %d/%d" % (checks, total))
    return 0 if checks == total else 1


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--config")
    ap.add_argument("--layers")
    ap.add_argument("--monitors")
    ap.add_argument("--monitor")
    ap.add_argument("--rules")
    ap.add_argument("--surfaces")
    ap.add_argument("--allocation")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not (args.config and args.layers and args.monitors):
        print("MADO_BARFOOT: ERROR (usage: --config PATH --layers PATH|- --monitors PATH|- [--rules PATH] [--surfaces PATH] [--allocation PATH|-])")
        return 2
    try:
        config = load_jsonc(read_bytes(args.config), "config")
        if not isinstance(config, dict):
            raise Setup("waybar config is not a JSON object (list-valued configs are unmodelled)")
        layers = parse_layers(read_bytes(args.layers, stdin_ok=True))
        monitors = parse_monitors(read_bytes(args.monitors, stdin_ok=True))
        monitor = args.monitor
        if monitor is None:
            if len(monitors) != 1:
                raise Setup("--monitor is required when the monitors reply carries %d entries"
                            % len(monitors))
            monitor = next(iter(monitors))
        static = dict(ZERO_STATIC)
        static_source = "none"
        if args.rules:
            static = parse_static_reserve(read_text(args.rules), monitor)
            static_source = "rules"
        surfaces = None
        if args.surfaces:
            surfaces = parse_surfaces(read_bytes(args.surfaces, stdin_ok=True))
            if not surfaces:
                raise Setup("the surfaces declaration is empty")
        allocation = None
        if args.allocation:
            allocation = parse_allocation(read_bytes(args.allocation, stdin_ok=True))
        verdict, rc, rows = evaluate(config, layers, monitors, monitor, static, static_source,
                                     surfaces, allocation)
        emit(rows, verdict)
        return rc
    except Unmodelled as exc:
        print("MADO_BARFOOT: ERROR (stage=model %s)" % exc)
        return 3
    except Setup as exc:
        print("MADO_BARFOOT: ERROR (stage=setup %s)" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
