#!/usr/bin/env python3
"""CritC1Narrow prober: run the reference and one variant on hand-written real-config cases and print divergences."""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REF = os.path.join(LANE, ".ufo/waves/round-46/l1-draft/mado-devices.py")
SCR = "/fast/scratch/hyaku/mado-r46/CritC1Narrow"
sys.path.insert(0, SCR)
from triage import VARIANTS  # noqa: E402


def kb(name, layout="us", variant="", options="", model="", rules=""):
    return {"address": "0x1", "name": name, "rules": rules, "model": model, "layout": layout, "variant": variant,
            "options": options, "active_layout_index": 0, "active_keymap": "x", "capsLock": False, "numLock": False,
            "main": False}


def mouse(name, sf=-1.0):
    return {"address": "0x2", "name": name, "defaultSpeed": 0.0, "scrollFactor": sf}


def dump(kbs, mice=(), **extra):
    d = {"mice": list(mice), "keyboards": list(kbs), "tablets": [], "touch": [], "switches": []}
    d.update(extra)
    return d


CASES = [
    ("three-line-continuation",
     ["input {\n  kb_options = grp:alts_toggle,\\\n    compose:caps,\\\n    ctrl:nocaps\n}\n"],
     dump([kb("kbd-1", options="grp:alts_toggle,compose:caps,ctrl:nocaps")])),
    ("source-line",
     ["source = ~/.config/hypr/input.conf\ninput:kb_layout = br\n"],
     dump([kb("kbd-1", "br")])),
    ("indented-directive",
     ["input {\n  # hyprlang noerror true\n  kb_layout = br\n}\n"],
     dump([kb("kbd-1", "br")])),
    ("comma-spaces",
     ["input:kb_options = grp:alts_toggle, compose:caps\n"],
     dump([kb("kbd-1", options="grp:alts_toggle, compose:caps")])),
    ("input-bracket",
     ["input[usb]:kb_layout = de\n"],
     dump([kb("kbd-1", "de")])),
    ("kb-file-empty-marker",
     ["input:kb_file = [[EMPTY]]\n"],
     dump([kb("kbd-1")])),
    ("int-scroll-factor",
     ["device[mouse-1]:scroll_factor = 2\n"],
     dump([kb("kbd-1")], [mouse("mouse-1", 2)])),
    ("equal-no-spaces",
     ["input:kb_layout=br\n"],
     dump([kb("kbd-1", "br")])),
    ("block-open-no-space",
     ["input{\n  kb_layout = br\n}\n"],
     dump([kb("kbd-1", "br")])),
    ("underflow-factor",
     ["device[mouse-1]:scroll_factor = 1e-40\n"],
     dump([kb("kbd-1")], [mouse("mouse-1")])),
    ("uppercase-NaN",
     ["device[mouse-1]:scroll_factor = NaN\n"],
     dump([kb("kbd-1")], [mouse("mouse-1")])),
    ("virtual-contained",
     ["input:kb_layout = br\n"],
     dump([kb("usb-hl-virtual-keyboard-uinput")])),
    ("exact-1MiB-config",
     ["# " + "x" * 1048573 + "\n"],
     dump([kb("kbd-1")])),
    ("crlf-comment",
     ["input:kb_options = a##b\r\n"],
     dump([kb("kbd-1", options="a#b")])),
]


def mod(source_path, name):
    spec = importlib.util.spec_from_file_location(name, source_path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def out_of(m, texts, dump_bytes):
    try:
        lines, rc = m.report(dump_bytes, texts)
    except m.Setup as e:
        return ["MADO_DEVICES: SETUP %s" % e], 2
    return lines, rc


def main():
    name = sys.argv[1]
    edits, _ = VARIANTS[name]
    src = open(REF).read()
    for old, new in edits:
        assert src.count(old) == 1, old
        src = src.replace(old, new)
    p = os.path.join(SCR, "work-%s" % name, "mado-devices.py")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(src)
    ref, var = mod(REF, "refmod"), mod(p, "varmod")
    for label, texts, d in CASES:
        db = json.dumps(d).encode()
        a, ra = out_of(ref, texts, db)
        b, rb = out_of(var, texts, db)
        if (a, ra) != (b, rb):
            print("DIFF %s\n  ref  rc=%d %r\n  var  rc=%d %r" % (label, ra, a[-2:], rb, b[-2:]))


if __name__ == "__main__":
    main()
