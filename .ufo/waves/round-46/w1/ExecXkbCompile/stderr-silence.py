#!/usr/bin/env python3
"""Can a --xkb mode keep stderr silent (mado-devices' contract: stderr empty on exit 0/1/3/4/5)?
xkb_context_set_log_level(ctx, XKB_LOG_LEVEL_CRITICAL=10) before compiling the failing name."""
import ctypes, sys
sys.path.insert(0, ".")
from importlib import import_module
p = import_module("xkb-probe")
L = p.LIB
L.xkb_context_set_log_level.restype = None
L.xkb_context_set_log_level.argtypes = [ctypes.c_void_p, ctypes.c_int]
L.xkb_context_set_log_fn.restype = None
L.xkb_context_set_log_fn.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]

def compile_quiet(layout):
    ctx = L.xkb_context_new(0)
    try:
        L.xkb_context_set_log_level(ctx, 10)          # XKB_LOG_LEVEL_CRITICAL
        L.xkb_context_set_log_fn(ctx, None, None)      # no callback
        names = p.XkbRuleNames(None, None, layout.encode(), None, None)
        km = L.xkb_keymap_new_from_names2(ctx, ctypes.byref(names), p.XKB_KEYMAP_FORMAT_TEXT_V2, 0)
        if not km:
            return None
        try:
            n = L.xkb_keymap_num_layouts(km)
            return [ (L.xkb_keymap_layout_get_name(km, i) or b"").decode() or None for i in range(n) ]
        finally:
            L.xkb_keymap_unref(km)
    finally:
        L.xkb_context_unref(ctx)

print("SILENCE: zz(loud path) would print xkbcommon errors above; quiet path follows")
print("SILENCE: quiet zz ->", compile_quiet("zz"))
print("SILENCE: quiet br ->", compile_quiet("br"))
print("SILENCE: quiet us ->", compile_quiet("us"))
