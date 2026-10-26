#!/usr/bin/env python3
"""Read-only scan of the frozen 90 fixtures (quality/counters/c1-r46-fixtures.json) for the two mechanisms this
seat found, so the report's statement about fixture coverage is computed rather than asserted.

B1 precondition: a value line inside a `device`-rooted category whose LHS is not one of the 47 registered device
values and is not `name` (such a line can re-target the selection).
B2 precondition: a `scroll_factor` literal that is non-zero as a decimal but rounds to float32 zero.
"""
import decimal
import json
import os
import re
import struct
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FIXTURES = os.path.join(LANE, "quality/counters/c1-r46-fixtures.json")
REF = os.path.join(LANE, ".ufo/waves/round-46/l1-draft/mado-devices.py")

REGISTERED = {"name", "sensitivity", "accel_profile", "rotation", "kb_file", "kb_layout", "kb_variant", "kb_options",
              "kb_rules", "kb_model", "repeat_rate", "repeat_delay", "natural_scroll", "tap_button_map",
              "numlock_by_default", "resolve_binds_by_sym", "disable_while_typing", "clickfinger_behavior",
              "middle_button_emulation", "tap-to-click", "tap-and-drag", "drag_lock", "left_handed", "scroll_method",
              "scroll_button", "scroll_button_lock", "scroll_points", "scroll_factor", "transform", "output",
              "enabled", "region_position", "absolute_region_position", "region_size", "relative_input",
              "active_area_position", "active_area_size", "flip_x", "flip_y", "drag_3fg", "keybinds", "share_states",
              "release_pressed_on_close", "tags", "eraser_button_mode", "eraser_button_override",
              "pressure_range_min", "pressure_range_max"}


def load_ref():
    import importlib.util
    spec = importlib.util.spec_from_file_location("refscan", REF)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def scan(text, ref):
    stack, b1, b2 = [], [], []
    for raw in text.split("\n"):
        line = raw.strip(" \t\r")
        if line.startswith("#"):
            continue
        line = line.split("#")[0].strip(" \t\r\n\v\f")
        if not line:
            continue
        if "=" not in line:
            if line == "}":
                if stack:
                    stack.pop()
            elif line.endswith("{"):
                stack.append(line[:-1].strip())
            continue
        lhs, rhs = line.split("=", 1)
        lhs, rhs = lhs.strip(), rhs.strip()
        key = ":".join(stack + [lhs])
        if not key.startswith("device"):
            continue
        field = key.split(":")[-1]
        if field == "name":
            continue
        if field not in REGISTERED:
            b1.append("%s = %s (key `%s` not registered by Hyprland)" % (lhs, rhs, field))
        if field == "scroll_factor":
            m = ref.FLOAT_RE.match(rhs)
            if m:
                try:
                    lit = decimal.Decimal(m.group(0))
                except decimal.InvalidOperation:
                    lit = None
                if lit is not None and lit != 0:
                    try:
                        f = struct.unpack("<f", struct.pack("<f", float(m.group(0))))[0]
                    except OverflowError:
                        f = None
                    if f == 0.0:
                        b2.append("%s (decimal %s, float32 0.0)" % (rhs, lit))
    return b1, b2


def main():
    ref = load_ref()
    fixtures = json.load(open(FIXTURES, encoding="utf-8"))
    n_b1 = n_b2 = 0
    for f in fixtures:
        cfgs = f.get("configs") or []
        text = "\n".join(c for c in cfgs if isinstance(c, str))
        b1, b2 = scan(text, ref)
        if b1 or b2:
            n_b1 += bool(b1)
            n_b2 += bool(b2)
            print("%-32s B1=%s B2=%s" % (f["label"], b1 or "-", b2 or "-"))
    decl = []
    for f in fixtures:
        st = ref.State()
        for c in (f.get("configs") or []):
            if isinstance(c, str):
                ref.parse_config(c, st)
        if st.unsupported:
            decl.append((f["label"], st.unsupported))
    print("fixtures whose config the reference marks unsupported: %d of %d %s" % (len(decl), len(fixtures), decl))
    print("FIXTURES: total=%d with-B1-precondition=%d with-B2-precondition=%d" % (len(fixtures), n_b1, n_b2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
