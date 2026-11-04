#!/usr/bin/env python3
"""mado — bar footprint join: declared waybar config -> live layer box -> reserved band.

Reads three caller-supplied artifacts and writes nothing:

  --config    the waybar configuration (JSONC; object form, as waybar 0.15.0 reads it)
  --layers    a captured `hyprctl layers -j` reply (file or `-` for stdin)
  --monitors  a captured `hyprctl monitors -j` reply (file or `-` for stdin)
  --monitor   the monitor name to join (optional when exactly one monitor answers)

It derives the bar's declared layer-surface footprint from the configuration at the
resolution Hyprland 0.56.2 gives it, finds the live layer entry with the same namespace
at the declared level, and compares the footprint with the live box and with the
monitor's `reserved` band. Nothing is connected, started or written.

Contract (v1, round 77):
  * position top/bottom/left/right; layer background/bottom/top/overlay; height/width;
    margin-<side> and CSS-form margin strings; exclusive; name; output (exact names and
    `!name` exclusions only).
  * Hyprland's arrange rule (src/render/Renderer.cpp arrangeLayerArray/@ efb5099):
    a zero desired width extends across the usable box minus horizontal margins;
    waybar clears both horizontal anchors when the bar declares a width > 1
    (src/bar.cpp:422-424), and the both-anchors branch then centres the box; the same
    holds transposed for vertical bars.
  * The reserved expectation is formed only when exclusive is true and the bar's edge
    margin is zero: gtk-layer-shell's auto exclusive zone composes margins in a way this
    tool does not model (named limit), so a margined exclusive bar reports NOT_MODELLED.
  * `reserved` band order is [left, top, right, bottom] (HyprCtl.cpp monitors reply).
  * Refused, never guessed: a monitor whose scale is not 1 or whose transform is not 0 (the
    monitors reply carries pixel size, the layer box is logical); a dynamic cross size (a
    horizontal bar with height 0, or a vertical bar with width 0 — the realised size is the
    module allocation, not the declaration); a list-valued config (multiple bars); `*` or
    space-bearing output patterns; and a `mode` key (presets rewrite layer and exclusive
    zone at runtime).
  * Not modelled and named as a limit: a static `monitor … addreserved` band (the reported
    band mixes the static reserve with the layer contribution), and any runtime change
    after the capture.

Exit map: 0 CLEAN · 1 DIFFER · 2 SETUP/ERROR · 3 NOT_FORMED (NO_LAYER/UNMODELLED/NO_BAR).
"""

import argparse
import json
import os
import re
import stat
import sys

VERSION = "r77-v1"

MAX_BYTES = 1048576

LEVEL = {"background": 0, "bottom": 1, "top": 2, "overlay": 3}
POSITIONS = ("top", "bottom", "left", "right")
MARGIN_SIDES = ("top", "right", "bottom", "left")

# HyprCtl.cpp: monitors reply prints m_reservedArea in left, top, right, bottom order.
RESERVED_INDEX = {"left": 0, "top": 1, "right": 2, "bottom": 3}


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
    try:
        st = os.lstat(path)
    except OSError as exc:
        raise Setup("unreadable path %s: %s" % (path, exc))
    if not stat.S_ISREG(st.st_mode):
        raise Setup("refused non-regular path: %s" % path)
    if st.st_size > MAX_BYTES:
        raise Setup("file exceeds %d bytes: %s" % (MAX_BYTES, path))
    try:
        with open(path, "rb") as fh:
            return fh.read()
    except OSError as exc:
        raise Setup("unreadable path %s: %s" % (path, exc))


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
        try:
            values = [int(t, 10) for t in tokens]
        except ValueError:
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
    """Exact monitor names and `!name` exclusions only; anything smarter is unmodelled."""
    spec = config.get("output")
    if spec is None:
        return True
    if isinstance(spec, str):
        names = [spec]
    elif isinstance(spec, list):
        names = spec
    else:
        raise Unmodelled("output must be a string or an array")
    include, exclude = [], []
    for name in names:
        if not isinstance(name, str):
            raise Unmodelled("output entries must be strings")
        if "*" in name or " " in name:
            raise Unmodelled("output pattern %r is outside the modelled subset" % name)
        if name.startswith("!"):
            exclude.append(name[1:])
        else:
            include.append(name)
    if monitor in exclude:
        return False
    if not include:
        return True
    return monitor in include


def declared_bar(config):
    position = config.get("position", "top")
    if position not in POSITIONS:
        raise Unmodelled("position %r is outside top/bottom/left/right" % (position,))
    layer = config.get("layer", "bottom")
    if layer not in LEVEL:
        raise Unmodelled("layer %r is outside background/bottom/top/overlay" % (layer,))
    namespace = config.get("name") if isinstance(config.get("name"), str) else "waybar"
    if isinstance(config.get("mode"), str):
        raise Unmodelled("a mode preset rewrites layer and exclusive zone at runtime")
    exclusive = config.get("exclusive")
    exclusive = exclusive if isinstance(exclusive, bool) else True
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


def declared_box(bar, mon_w, mon_h):
    """Hyprland 0.56.2 arrangeLayerArray: desired size, anchors, margins."""
    m = bar["margins"]
    pos = bar["position"]
    if pos in ("top", "bottom") and bar["height"] == 0:
        raise Unmodelled("dynamic height on a horizontal bar is the module allocation, not a declared value")
    if pos in ("left", "right") and bar["width"] == 0:
        raise Unmodelled("dynamic width on a vertical bar is the module allocation, not a declared value")
    if pos in ("top", "bottom"):
        if bar["width"] > 1:
            w = bar["width"]
            x = (mon_w - w) // 2  # both horizontal anchors cleared -> centred, no margins
        else:
            w = mon_w - m["left"] - m["right"]
            x = m["left"]
        if bar["height"] > 0:
            h = bar["height"]
            y = m["top"] if pos == "top" else mon_h - h - m["bottom"]
        else:
            # zero desired height: the auto-height branch spans the usable box
            h = mon_h - m["top"] - m["bottom"]
            y = m["top"]
    else:
        if bar["height"] > 1:
            h = bar["height"]
            y = (mon_h - h) // 2  # both vertical anchors cleared -> centred, no margins
        else:
            h = mon_h - m["top"] - m["bottom"]
            y = m["top"]
        if bar["width"] > 0:
            w = bar["width"]
            x = m["left"] if pos == "left" else mon_w - w - m["right"]
        else:
            w = mon_w - m["left"] - m["right"]
            x = m["left"]
    if w <= 0 or h <= 0:
        raise Unmodelled("declared box is empty (%dx%d)" % (w, h))
    return {"x": x, "y": y, "w": w, "h": h}


def edge_extent(bar, box, mon_w, mon_h):
    pos = bar["position"]
    if pos == "top":
        return box["y"] + box["h"]
    if pos == "bottom":
        return mon_h - box["y"]
    if pos == "left":
        return box["x"] + box["w"]
    return mon_w - box["x"]


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


def evaluate(config, layers, monitors, monitor=None):
    bar = declared_bar(config)
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

    rows = [("CONFIG", "pos=%s layer=%s level=%d ns=%s height=%d width=%d margins=%d,%d,%d,%d exclusive=%s"
             % (bar["position"], bar["layer"], bar["level"], bar["namespace"], bar["height"],
                bar["width"], bar["margins"]["top"], bar["margins"]["right"],
                bar["margins"]["bottom"], bar["margins"]["left"],
                "true" if bar["exclusive"] else "false"))]

    if not output_matches(config, monitor):
        rows.append(("RESULT", "monitor=%s box=NOT_ON_MONITOR reserved=NOT_APPLIED verdict=NO_BAR" % monitor))
        return "NO_BAR", 3, rows

    box = declared_box(bar, mon_w, mon_h)
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

    extent = edge_extent(bar, box, mon_w, mon_h)
    edge = bar["position"]
    band = mon["reserved"][RESERVED_INDEX[edge]]
    if not bar["exclusive"]:
        reserved_verdict = "NOT_APPLIED"
    elif any(bar["margins"][s] != 0 for s in MARGIN_SIDES):
        reserved_verdict = "NOT_MODELLED"
    elif band == extent:
        reserved_verdict = "EQ"
    elif band > extent:
        reserved_verdict = "GT"
    else:
        reserved_verdict = "DIFFER"

    if box_verdict == "DIFFER" or reserved_verdict == "DIFFER":
        verdict, rc = "DIFFER", 1
    elif reserved_verdict == "NOT_MODELLED":
        verdict, rc = "UNMODELLED", 3
    else:
        verdict, rc = "CLEAN", 0
    rows.append(("RESULT", "monitor=%s box=%s reserved=%s band=%d expected=%d verdict=%s"
                 % (monitor, box_verdict, reserved_verdict, band, extent, verdict)))
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

    def case(config, layers, monitors, monitor=None):
        return evaluate(config, layers, monitors, monitor)

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

    # margins are not modelled for the reserved band
    v, rc, rows = case({"position": "top", "layer": "top", "height": 26, "margin": "4 0"},
                       {"M1": {"levels": {"0": [], "1": [], "2": [
                           {"namespace": "waybar", "x": 0, "y": 4, "w": 3440, "h": 26,
                            "alpha": 1, "pid": 1}], "3": []}}},
                       {"M1": {"name": "M1", "width": 3440, "height": 1440, "reserved": [0, 26, 0, 0], "scale": 1.0, "transform": 0}})
    ok(v == "UNMODELLED" and any("reserved=NOT_MODELLED" in t for _, t in rows), "margin unmodelled")

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

    print("MADO_BARFOOT_SELFTEST: %d/%d" % (checks, total))
    return 0 if checks == total else 1


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--config")
    ap.add_argument("--layers")
    ap.add_argument("--monitors")
    ap.add_argument("--monitor")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not (args.config and args.layers and args.monitors):
        print("MADO_BARFOOT: ERROR (usage: --config PATH --layers PATH|- --monitors PATH|-)")
        return 2
    try:
        config = load_jsonc(read_bytes(args.config), "config")
        if not isinstance(config, dict):
            raise Setup("waybar config is not a JSON object (list-valued configs are unmodelled)")
        layers = parse_layers(read_bytes(args.layers, stdin_ok=True))
        monitors = parse_monitors(read_bytes(args.monitors, stdin_ok=True))
        verdict, rc, rows = evaluate(config, layers, monitors, args.monitor)
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
