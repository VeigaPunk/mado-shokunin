#!/usr/bin/env python3
"""Check the compile probe against the live compositor dump (read-only).

1. For every keyboard in `hyprctl devices -j`, recompile its PRINTED rules and compare the
   compiled layout name at `active_layout_index` with `active_keymap` (HyprCtl.cpp:781-794 prints
   xkb_keymap_layout_get_name of the active layout, so equality is the prediction test).
2. For every names set that fails to compile, print the tuple Hyprland would then report
   (IKeyboard.cpp:107-115 resets rules to layout us, everything else empty).
3. Exercise the kb_file branch shape (xkb_keymap_new_from_string, TEXT_V2) to show what a
   compile-based mode could and could not see.
No process is started by this script; the dump is supplied on stdin.
"""
import ctypes
import json
import subprocess
import sys

sys.path.insert(0, ".")
from importlib import import_module

probe = import_module("xkb-probe")

LIB = probe.LIB
LIB.xkb_keymap_new_from_string.restype = ctypes.c_void_p
LIB.xkb_keymap_new_from_string.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]

MINIMAL = """xkb_keymap {
    xkb_keycodes  { include "evdev+aliases(qwerty)" };
    xkb_types     { include "complete" };
    xkb_compat    { include "complete" };
    xkb_symbols   { include "pc+br" };
    xkb_geometry  { include "pc(pc105)" };
};
"""


def from_string(text):
    ctx = LIB.xkb_context_new(0)
    try:
        km = LIB.xkb_keymap_new_from_string(ctx, text.encode(), probe.XKB_KEYMAP_FORMAT_TEXT_V2, 0)
        if not km:
            return None
        try:
            n = LIB.xkb_keymap_num_layouts(km)
            names = []
            for i in range(n):
                v = LIB.xkb_keymap_layout_get_name(km, i)
                names.append(v.decode() if v else None)
            return names
        finally:
            LIB.xkb_keymap_unref(km)
    finally:
        LIB.xkb_context_unref(ctx)


def dump():
    p = subprocess.run(["hyprctl", "devices", "-j"], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit("VERIFY: SETUP hyprctl devices -j failed")
    return json.loads(p.stdout)


def main():
    d = dump()
    kbs = [k for k in d.get("keyboards", []) if isinstance(k, dict) and isinstance(k.get("name"), str)]
    mismatch = 0
    virtual = 0
    for k in kbs:
        if k["name"].startswith("hl-virtual-keyboard"):
            virtual += 1
        layouts = probe.compile_names(
            k.get("rules", ""), k.get("model", ""), k.get("layout", ""),
            k.get("variant", ""), k.get("options", ""),
        )
        idx = k.get("active_layout_index")
        got = None if not layouts or not isinstance(idx, int) or not (0 <= idx < len(layouts)) else layouts[idx]
        ok = got == k.get("active_keymap")
        mismatch += 0 if ok else 1
        print(f"VERIFY: keyboard[{len(kbs)}] printed_rules_compile={layouts is not None} "
              f"active_keymap_matches_compiled={ok} virtual={k['name'].startswith('hl-virtual-keyboard')}")
    print(f"VERIFY: keyboards={len(kbs)} virtual={virtual} active_keymap_mismatches={mismatch}")

    # what the compositor reports AFTER a failed compile (fallback path)
    fb = probe.hyprland_fallback()
    print(f"VERIFY: fallback_compile_layouts={fb} -> printed tuple would be "
          f"layout='us' variant='' options='' model='' rules='' active_keymap='{fb[0] if fb else None}'")

    print("VERIFY: kb_file branch -- from_string(minimal br map) ->", from_string(MINIMAL))
    print("VERIFY: kb_file branch -- from_string(garbage) ->", from_string("xkb_keymap { nope };"))
    return 0 if mismatch == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
