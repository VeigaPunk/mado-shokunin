#!/usr/bin/env python3
"""Probe client_fsmode's return values in the reference and in the boundary mutants.

Shows which values the counter's selftest case `fsmode-values` pins and which it does not.
Read-only: imports each body from the seat dir and calls one pure function.
Usage: python3 probe_fsmode.py > receipts/fsmode-probe.txt
"""
import os
import types

SEAT = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(SEAT, "..", "..", "c1", "ctl-ref-tool.py.txt")
BODIES = ["M01-fsmode-extra-3", "M04-fsmode-admit-0", "M05-fsmode-admit-neg",
          "M06-fsmode-range-chain", "M22-fallback-none", "M51-return-any-int"]
VALUES = [("1", 1), ("2", 2), ("0", 0), ("3", 3), ("-1", -1), ("-7", -7), ("True", True),
          ("False", False), ("2.0", 2.0), ("'2'", "2"), ("None", None), ("[2]", [2]),
          ('{"internal":2}', {"internal": 2})]


def load(path, tag):
    """Load a tool body (any suffix, incl. the reference .txt) into a fresh module."""
    mod = types.ModuleType(tag)
    mod.__file__ = path
    with open(path, "rb") as fh:
        code = compile(fh.read(), path, "exec")
    exec(code, mod.__dict__)
    return mod


def main():
    print("fsmode probe: client_fsmode({'fullscreen': v}) per body (contract: 0 for everything but 1 and 2)")
    print("value\tREF\t" + "\t".join(BODIES))
    ref = load(REF, "ref_tool")
    mods = [(n, load(os.path.join(SEAT, "mutants", n + ".py"), "m_" + n.replace("-", "_")))
            for n in BODIES]
    for label, v in VALUES:
        row = ["%r" % (ref.client_fsmode({"fullscreen": v}),)]
        for _n, m in mods:
            row.append("%r" % (m.client_fsmode({"fullscreen": v}),))
        print("%s\t%s" % (label, "\t".join(row)))
    print("")
    print("counter selftest case that pins these values (c1-r44 fixture text, from the reference):")
    print("  chk(\"fsmode-values\", [client_fsmode({\"fullscreen\": v}) for v in "
          "(1, 2, 0, 3, True, 2.0, \"1\", None)], [1, 2, 0, 0, 0, 0, 0, 0])")
    print("  -> covers 1, 2, 0, 3, True, 2.0, '2', None; does NOT cover any negative integer.")
    for n, m in mods:
        neg = m.client_fsmode({"fullscreen": -1})
        print("  %s: client_fsmode(fullscreen=-1) = %r (reference %r), eight-case selftest tuple unchanged"
              % (n, neg, ref.client_fsmode({"fullscreen": -1})))


if __name__ == "__main__":
    main()
