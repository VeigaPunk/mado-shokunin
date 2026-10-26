#!/usr/bin/env python3
"""Read-only probe: compile declared XKB rule names with the host libxkbcommon, exactly as
Hyprland 0.56.2 src/devices/IKeyboard.cpp setKeymap does, and print what the compositor would
then report as hyprctl devices -j `layout` / `active_keymap`.

Loads libxkbcommon with ctypes; starts no process, opens no socket, writes nothing.

  python3 -I xkb-probe.py            # probe table
  python3 -I xkb-probe.py --json     # same, one JSON object
"""
import ctypes
import ctypes.util
import json
import os
import sys

TYPE_LAYOUT_INDEX = ctypes.c_uint32


class XkbRuleNames(ctypes.Structure):
    _fields_ = [
        ("rules", ctypes.c_char_p),
        ("model", ctypes.c_char_p),
        ("layout", ctypes.c_char_p),
        ("variant", ctypes.c_char_p),
        ("options", ctypes.c_char_p),
    ]


def load():
    cand = []
    lib = ctypes.util.find_library("xkbcommon")
    if lib:
        cand.append(lib)
    cand += ["libxkbcommon.so.0", "libxkbcommon.so"]
    last = None
    for name in cand:
        try:
            return ctypes.CDLL(name), name
        except OSError as e:  # pragma: no cover
            last = e
    raise SystemExit(f"XKB_PROBE: SETUP cannot load libxkbcommon: {last}")


LIB, LIBNAME = load()
LIB.xkb_context_new.restype = ctypes.c_void_p
LIB.xkb_context_new.argtypes = [ctypes.c_int]
LIB.xkb_context_unref.restype = None
LIB.xkb_context_unref.argtypes = [ctypes.c_void_p]
LIB.xkb_keymap_new_from_names2.restype = ctypes.c_void_p
LIB.xkb_keymap_new_from_names2.argtypes = [
    ctypes.c_void_p,
    ctypes.POINTER(XkbRuleNames),
    ctypes.c_int,
    ctypes.c_int,
]
LIB.xkb_keymap_unref.restype = None
LIB.xkb_keymap_unref.argtypes = [ctypes.c_void_p]
LIB.xkb_keymap_num_layouts.restype = ctypes.c_uint32
LIB.xkb_keymap_num_layouts.argtypes = [ctypes.c_void_p]
LIB.xkb_keymap_layout_get_name.restype = ctypes.c_char_p
LIB.xkb_keymap_layout_get_name.argtypes = [ctypes.c_void_p, TYPE_LAYOUT_INDEX]

XKB_CONTEXT_NO_FLAGS = 0
XKB_KEYMAP_FORMAT_TEXT_V2 = 1
XKB_KEYMAP_COMPILE_NO_FLAGS = 0


def compile_names(rules, model, layout, variant, options):
    """Hyprland setKeymap's compile: fresh context, TEXT_V2, no flags. None args stay NULL."""
    ctx = LIB.xkb_context_new(XKB_CONTEXT_NO_FLAGS)
    if not ctx:
        raise SystemExit("XKB_PROBE: SETUP xkb_context_new returned NULL")
    try:
        names = XkbRuleNames(
            None if rules is None else rules.encode(),
            None if model is None else model.encode(),
            None if layout is None else layout.encode(),
            None if variant is None else variant.encode(),
            None if options is None else options.encode(),
        )
        km = LIB.xkb_keymap_new_from_names2(
            ctx, ctypes.byref(names), XKB_KEYMAP_FORMAT_TEXT_V2, XKB_KEYMAP_COMPILE_NO_FLAGS
        )
        if not km:
            return None
        try:
            n = LIB.xkb_keymap_num_layouts(km)
            layouts = []
            for i in range(n):
                nm = LIB.xkb_keymap_layout_get_name(km, i)
                layouts.append(nm.decode() if nm else None)
            return layouts
        finally:
            LIB.xkb_keymap_unref(km)
    finally:
        LIB.xkb_context_unref(ctx)


def hyprland_fallback(layout="us"):
    """IKeyboard.cpp:107-115: memset the rule names, then layout = "us" only."""
    return compile_names(None, None, layout, None, None)


CASES = [
    # id, rules, model, layout, variant, options
    ("host-br-compose-caps", "", "", "br", "", "compose:caps"),
    ("us-defaults", "", "", "us", "", ""),
    ("empty-defaults", "", "", "", "", ""),
    ("br-us-compose-caps", "", "", "br,us", "", "compose:caps"),
    ("typo-layout-zz", "", "", "zz", "", ""),
    ("typo-layout-brq", "", "", "brq", "", ""),
    ("br-nodeadkeys-variant", "", "", "br", "nodeadkeys", ""),
    ("br-variant-zzz", "", "", "br", "zzz", ""),
    ("us-nodeadkeys-variant", "", "", "us", "nodeadkeys", ""),
    ("br-option-notanoption", "", "", "br", "", "notanoption:x"),
    ("br-option-compose-mixed", "", "", "br", "", "compose:caps,notanoption:x"),
    ("br-option-grp-alts", "", "", "br", "", "compose:caps,grp:alts_toggle"),
    ("br-rules-zzz", "zzz", "", "br", "", ""),
    ("br-model-zzz", "", "zzz", "br", "", ""),
    ("br-uppercase-BR", "", "", "BR", "", ""),
    ("br-us-variant-nodeadkeys", "", "", "br,us", "nodeadkeys", ""),
]


def main():
    out = {
        "lib": LIBNAME,
        "xkb_config_root_env": os.environ.get("XKB_CONFIG_ROOT"),
        "xkb_config_extra_path_env": os.environ.get("XKB_CONFIG_EXTRA_PATH"),
        "cases": [],
        "hyprland_fallback": None,
    }
    out["hyprland_fallback"] = hyprland_fallback()
    for cid, r, m, l, v, o in CASES:
        layouts = compile_names(r, m, l, v, o)
        out["cases"].append(
            {
                "id": cid,
                "names": {"rules": r, "model": m, "layout": l, "variant": v, "options": o},
                "compiled": layouts is not None,
                "layout_names": layouts,
            }
        )

    if "--json" in sys.argv[1:]:
        print(json.dumps(out, indent=1))
        return 0

    print(f"XKB_PROBE: lib={out['lib']} XKB_CONFIG_ROOT={out['xkb_config_root_env']!r}")
    print(f"XKB_PROBE: hyprland-fallback(all NULL, layout=us) -> {out['hyprland_fallback']}")
    for c in out["cases"]:
        n = c["names"]
        tag = "COMPILES" if c["compiled"] else "NULL(compile failed)"
        print(
            f"XKB_PROBE: {c['id']:28s} layout={n['layout']!r} variant={n['variant']!r} "
            f"options={n['options']!r} rules={n['rules']!r} model={n['model']!r} -> {tag} "
            f"layouts={c['layout_names']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
