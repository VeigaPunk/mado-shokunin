#!/usr/bin/env python3
"""Seat ScrFormsEntryA own re-derivation of the round-40 native census.

Read-only: parses the host config tree with the lane's delivered static
resolver (imported, not edited), then labels each row against the committed
native capture .ufo/waves/round-40/c1/native-capture.jsonl using the
conversion documented in the entry (hyprlang configStringToInt; Hyprland
gradient/gap/font-weight handlers). Writes nothing; prints counts.
"""
import collections
import importlib.util
import json
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
TOOL = os.path.join(LANE, "tools/mado-options.py")
CAPTURE = os.path.join(LANE, ".ufo/waves/round-40/c1/native-capture.jsonl")

WEIGHTS = {"thin": 100, "ultralight": 200, "light": 300, "semilight": 350,
           "book": 380, "normal": 400, "medium": 500, "semibold": 600,
           "bold": 700, "ultrabold": 800, "heavy": 900, "ultraheavy": 1000}


def hl_int(v):
    """hyprlang configStringToInt: 0x hex, rgba()/rgb(), bool words, number."""
    if v.startswith("0x"):
        try:
            return int(v, 16)
        except ValueError:
            return None
    if v.startswith("rgba(") and v.endswith(")"):
        inner = v[5:-1].strip()
        if inner.count(",") == 3:
            parts = [x.strip() for x in inner.split(",")]
            r, g, b = (hl_int(x) for x in parts[:3])
            try:
                a = int(round(float(parts[3]) * 255.0)) & 0xFF
            except ValueError:
                return None
            if None in (r, g, b):
                return None
            return a * 0x1000000 + r * 0x10000 + g * 0x100 + b
        if len(inner) == 8:
            try:
                x = int(inner, 16)
            except ValueError:
                return None
            return (x >> 8) + 0x1000000 * (x & 0xFF)
        return None
    if v.startswith("rgb(") and v.endswith(")"):
        inner = v[4:-1].strip()
        if inner.count(",") == 2:
            r, g, b = (hl_int(x.strip()) for x in inner.split(","))
            if None in (r, g, b):
                return None
            return 0xFF000000 + r * 0x10000 + g * 0x100 + b
        if len(inner) == 6:
            try:
                return int(inner, 16) + 0xFF000000
            except ValueError:
                return None
        return None
    if v.startswith(("true", "on", "yes")):
        return 1
    if v.startswith(("false", "off", "no")):
        return 0
    if v.lstrip("-").isdigit():
        return int(v)
    return None


def native_equal(form, declared, live, angle):
    d = declared.strip()
    try:
        if form == "int":
            return hl_int(d) == live
        if form == "float":
            return abs(float(d) - float(live)) < 1e-6
        if form == "str":
            return d == str(live).strip()
        toks = str(live).split()
        if toks and toks[-1].endswith("deg"):
            cols, ang = [], angle
            for tok in d.split():
                if "deg" in tok:
                    ang = int(tok[:tok.index("deg")])
                    break
                c = hl_int(tok)
                if c is None:
                    return False
                cols.append(c)
            return bool(cols) and " ".join("%x" % c for c in cols) + \
                " %ddeg" % ang == str(live)
        if len(toks) == 4 and all(t.lstrip("-").isdigit() for t in toks):
            n = [int(x) for x in d.split()]
            if len(n) == 1:
                n = n * 4
            elif len(n) == 2:
                n = [n[0], n[1], n[0], n[1]]
            elif len(n) == 3:
                n = [n[0], n[1], n[2], n[1]]
            return " ".join(str(x) for x in n[:4]) == str(live)
        return str(WEIGHTS.get(d.lower(), -1)) == str(live)
    except (ValueError, IndexError):
        return False


def load_tool():
    spec = importlib.util.spec_from_file_location("mado_options", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    home = os.path.expanduser("~")
    mod = load_tool()
    angles = {}
    orig = mod.State.declare

    def declare(self, key, value, path, lineno):
        orig(self, key, value, path, lineno)
        for tok in value.split():
            if "deg" in tok:
                try:
                    angles[key] = int(tok[:tok.index("deg")])
                except ValueError:
                    pass
                break

    mod.State.declare = declare
    st = mod.State(home)
    mod.parse_file(os.path.join(home, ".config/hypr/hyprland.conf"), st)
    rows = {k: dict(v) for k, v in st.options.items()}
    cap = {}
    forms = collections.Counter()
    for line in open(CAPTURE):
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        fs = [f for f in ("int", "float", "str", "custom") if f in rec]
        assert len(fs) == 1 and "set" in rec, rec
        forms[fs[0]] += 1
        cap[rec["option"]] = (fs[0], rec[fs[0]], bool(rec["set"]))
    labels = collections.Counter()
    shadowed = []
    for key in sorted(rows):
        row = rows[key]
        if key not in cap:
            labels["config-only"] += 1
            continue
        form, value, isset = cap[key]
        if not isset or not native_equal(form, row["value"], value,
                                         angles.get(key, 0)):
            labels["mismatch"] += 1
            print("MISMATCH", key, form, repr(row["value"]), repr(value))
        elif row["_decls"] > 1:
            labels["agreement*"] += 1
            shadowed.append(key)
        else:
            labels["agreement"] += 1
    for key in cap:
        if key not in rows:
            labels["live-default"] += 1
    order = ("agreement", "agreement*", "mismatch", "config-only",
             "live-default")
    print("forms int=%d float=%d str=%d custom=%d" % (
        forms["int"], forms["float"], forms["str"], forms["custom"]))
    print("labels " + " ".join("%s=%d" % (k, labels[k]) for k in order))
    print("rows=%d capture=%d sum_forms=%d sum_labels=%d" % (
        len(rows), len(cap), sum(forms.values()), sum(labels.values())))
    print("shadowed=%s" % " ".join(shadowed))
    print("active_border live=%r angle=%d decls=%d" % (
        cap.get("general:col.active_border"),
        angles.get("general:col.active_border", -1),
        rows["general:col.active_border"]["_decls"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
