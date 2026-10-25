#!/usr/bin/env python3
"""Run a controls.py copy with its C1/C2 counter paths redirected to scratch copies.

usage: run_controls.py <controls.py> <c1.py> <c2.py> <out>
The controls file itself is loaded unmodified; only its module globals are rebound.
"""
import importlib.util
import sys

ctl, c1, c2, out = sys.argv[1:5]
spec = importlib.util.spec_from_file_location("ctl", ctl)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
_sh = m.sh


def logged_sh(*cmd, **kw):
    p = _sh(*cmd, **kw)
    if p.returncode != 0:
        print(f"SH_FAIL rc={p.returncode} cmd={' '.join(cmd[:4])} err={p.stderr.strip()[-300:]!r}",
              file=sys.stderr)
    return p


m.sh = logged_sh
swap = {m.C1: c1, m.C2: c2}
m.CONTROLS = [(n, swap[c], b, w) for n, c, b, w in m.CONTROLS]
m.C1, m.C2 = c1, c2
sys.argv = ["controls.py", "--out", out]
sys.exit(m.main())
