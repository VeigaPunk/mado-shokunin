#!/usr/bin/env python3
"""mado-monitors (CONTROL B2, r45 - loads the reference out of the lane's working tree).

The scored blob is a loader: it executes .ufo/waves/round-45/l1-draft/mado-monitors.py (the reference, not a
commit object of the scored revision) and passes argv/stdin through. A control against PRED-C1-r45: at the
scored revision the repository holds no implementation.
"""
import sys

REF = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/l1-draft/mado-monitors.py"
NAMESPACE = {"__name__": "mado_monitors_reference", "__file__": REF}
exec(compile(open(REF, "rb").read(), REF, "exec"), NAMESPACE)
sys.exit(NAMESPACE["main"]())
