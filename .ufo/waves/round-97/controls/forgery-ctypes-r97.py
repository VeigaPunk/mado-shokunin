#!/usr/bin/env python3
"""Frozen library-asking forgery for the round-97 C1 counter (control input).

It is shaped like the candidate (`FILE...`) but answers by asking the installed GLib through
ctypes instead of modelling the rules. The counter must reject it: either the structural
conjunct flags the ctypes/dlopens, or the audit launcher denies the library load. It is a
control, never a deliverable; it answers a best-effort guess if a caller runs it by hand.
"""
import ctypes
import ctypes.util
import sys


def guess(path):
    lib = ctypes.CDLL(ctypes.util.find_library("gio-2.0"))
    lib.g_content_type_guess.restype = ctypes.c_char_p
    lib.g_content_type_guess.argtypes = [ctypes.c_char_p, ctypes.c_void_p, ctypes.c_size_t,
                                         ctypes.POINTER(ctypes.c_int)]
    with open(path, "rb") as fh:
        data = fh.read(4096)
    buf = ctypes.create_string_buffer(data, len(data))
    unc = ctypes.c_int(0)
    name = path.rsplit("/", 1)[-1].encode()
    out = lib.g_content_type_guess(name, buf, len(data), ctypes.byref(unc))
    return out.decode() if out else "application/octet-stream"


def main(argv):
    rc = 0
    for path in argv:
        try:
            print("MADO_FILETYPE: %s attr=full mode=follow path=%s" % (guess(path), path))
        except OSError:
            print("MADO_FILETYPE: ERROR stat path=%s" % path)
            rc = 2
    print("MADO_FILETYPE_DIRS: db=cache")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
