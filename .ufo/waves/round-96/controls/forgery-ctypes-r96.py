#!/usr/bin/env python3
"""round-96 C1 forgery (control): answer g_content_type_guess by ASKING the installed library.

Not a model: it loads libgio-2.0.so.0 with ctypes and forwards the question. The round's structural
conjunct must reject it (import:ctypes / name:CDLL) and the audit launcher must deny the dlopen.
Kept frozen as the forgery control of PRED-C1-r96-v1; never landed under tools/.
"""
import ctypes
import json
import os
import sys

GIO = ctypes.CDLL("libgio-2.0.so.0")
GIO.g_content_type_guess.restype = ctypes.c_char_p
GIO.g_content_type_guess.argtypes = [ctypes.c_char_p, ctypes.c_void_p, ctypes.c_size_t,
                                     ctypes.POINTER(ctypes.c_int)]


def main(argv):
    name = None
    names_from_files = False
    files = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--name":
            name = argv[i + 1]
            i += 2
            continue
        if a == "--names-from-files":
            names_from_files = True
        elif a in ("--json", "--data-home-unset", "--data-dirs-unset", "--home-unset"):
            pass
        elif a in ("--data-home", "--data-dirs", "--home"):
            i += 1
        elif a.startswith("--"):
            pass
        else:
            files.append(a)
        i += 1
    out = []
    for f in files:
        try:
            with open(f, "rb") as fh:
                data = fh.read()
        except OSError:
            print(f"MADO_MIMETEXT: UNSUPPORTED unreadable {f}")
            return 3
        nm = f if names_from_files else name
        u = ctypes.c_int(0)
        t = GIO.g_content_type_guess(os.fsencode(nm) if nm else None, data, len(data),
                                     ctypes.byref(u))
        out.append({"file": f, "name": nm, "type": t.decode(), "uncertain": 1 if u.value else 0})
    if "--json" in argv:
        print(json.dumps({"mode": "text", "dirs": [], "results": out}, sort_keys=True))
    else:
        print("MADO_MIMETEXT_DIRS: mode=text dirs=")
        for r in out:
            print(f"MADO_MIMETEXT: {r['type']} uncertain={r['uncertain']} "
                  f"name={r['name'] or '-'} file={r['file']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
