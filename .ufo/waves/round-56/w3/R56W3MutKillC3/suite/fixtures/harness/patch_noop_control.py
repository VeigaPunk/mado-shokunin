#!/usr/bin/env python3
"""patch_noop_control.py -- the M36/M37/M38 kill fixture.

It adds a tenth control, "noop-control", to a copy of quality/r56_ctl_c3.py.  The control's mutation is
deliberately ineffective:

  mode "empty" -- the tree is not changed at all (an empty registry/entry mutation);
  mode "entry" -- one entry is touched (its last line gets a suffix), so no leg can rise either.

A harness that checks the effectiveness of its controls must refuse this control with a setup error
(exit 2, "control noop-control is ineffective").  A harness whose effectiveness check is missing or weakened
credits the control instead, and the control then fails at run time -- that is the observable difference this
fixture kills on.

The patched harness is a COPY; the lane's file is never touched.
"""

NOOP_FN = '''

def mut_noop(src, entries, base_src):
    """a deliberately ineffective control (the frozen tree is not changed): the harness must reject it."""
    return src, {}, "no-op mutation", "%s"
'''

NOOP_ENTRY_FN = '''

def mut_noop(src, entries, base_src):
    """a deliberately ineffective control: one entry is touched, but no leg can rise."""
    path = sorted(entries)[0]
    lines = entries[path].split("\\n")
    lines[-1] = lines[-1] + " x"
    return src, {path: "\\n".join(lines)}, "no-op mutation of one entry", "%s"
'''


def patch_noop(src, leg, mode="empty"):
    """-> bytes: the harness source with control 10 "noop-control" (leg, mode) appended."""
    if isinstance(src, bytes):
        src = src.decode("utf-8")
    fn = (NOOP_ENTRY_FN if mode == "entry" else NOOP_FN) % leg
    src = src.replace("\nCONTROLS = [", fn + "\nCONTROLS = [", 1)
    src = src.replace('    ("stale-allow", mut_stale_allow),\n]',
                      '    ("stale-allow", mut_stale_allow),\n    ("noop-control", mut_noop),\n]', 1)
    return src
