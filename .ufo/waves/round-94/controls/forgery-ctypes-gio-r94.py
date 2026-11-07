#!/usr/bin/env python3
"""Round-94 C1 pre-freeze forgery control: answers every name by calling the installed libgio's
g_content_type_guess through ctypes (no model of its own).  PRED-C1-r94-v1 (vi) must reject it."""
import argparse
import ctypes
import json
import os
import sys

ap = argparse.ArgumentParser()
ap.add_argument("names", nargs="*")
ap.add_argument("--json", action="store_true")
for f in ("--data-home", "--data-dirs", "--home"):
    ap.add_argument(f)
    ap.add_argument(f + "-unset", action="store_true")
a = ap.parse_args()
for k, f in (("XDG_DATA_HOME", "data_home"), ("XDG_DATA_DIRS", "data_dirs"), ("HOME", "home")):
    v = getattr(a, f)
    if getattr(a, f + "_unset"):
        os.environ.pop(k, None)
    elif v is not None:
        os.environ[k] = v
gio = ctypes.CDLL("libgio-2.0.so.0")
gio.g_content_type_guess.restype = ctypes.c_char_p
gio.g_content_type_guess.argtypes = [ctypes.c_char_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_int)]
res = []
for n in a.names:
    u = ctypes.c_int(0)
    t = gio.g_content_type_guess(os.fsencode(n), None, 0, ctypes.byref(u))
    res.append({"name": n, "type": t.decode(), "uncertain": 1 if u.value else 0, "types": []})
print(json.dumps({"mode": "gio", "dirs": [], "results": res}))
sys.exit(0)
