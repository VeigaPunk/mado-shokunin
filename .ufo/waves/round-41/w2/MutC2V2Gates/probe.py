#!/usr/bin/env python3
"""Clause-level probes: for survived mutants with a predicted kill, score the
predicted target fixture under the MUTANT counter and print the counter's own
clause line, to name the gate that actually fires (redundancy evidence)."""
import contextlib
import importlib.util
import io
import shutil
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = LANE + "/.ufo/waves/round-41/w2/MutC2V2Gates"
RUNNER = LANE + "/.ufo/waves/round-41/ctl/run-c2-v2-controls.py"
SCRATCH = "/tmp/mutc2v2gates-tmp"


def load_mod(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


tempfile.tempdir = SCRATCH
import os
os.makedirs(SCRATCH, exist_ok=True)
ctl = load_mod(RUNNER, "ctl_probe")
base = ctl.base_files()
G = ctl.admitted()
M = ctl.mutants(base, G)

PROBES = [
    ("M14-quote-binding-drop", "N04-quote-absent"),
    ("M16-quote-word-window", "N05-quote-26-words"),
    ("M17-sessions-floor-1", "J02-single-session"),
    ("M20-ascending-drop", "J17-sessions-replayed"),
    ("M21-loglevel-loosen", "J11-other-level-adverts"),
    ("M23-cited-case-drop", "W02-lowercase-id"),
    ("M22-census-anchor-drop", "X03-journal-line-in-prose"),
    ("M07-pin-path-drop", "F5-receipt-renamed"),
    ("M10-new-ids-3-to-1", "N07-two-new-ids-left"),
    ("M27-badloc-drop", "A05-localized-channel-source"),
    ("M27-badloc-drop", "F4-localized-redirect"),
]

# J02 tail anatomy: does the single-session tail keep a boot line?
jt = ctl.JBYTES.decode()
tail = "\n".join(jt.split("\n")[116:]) + "\n"
boots = sum(1 for l in tail.splitlines()
            if __import__("re").fullmatch(r"-- Boot [0-9a-f]{32} --", l))
print("J02-TAIL boot-lines=%d lines=%d" % (boots, len(tail.splitlines())))

# M22 vacuity: Pattern.match anchors at pos 0 with or without '^'
m22 = load_mod(SEAT + "/mutants/M22-census-anchor-drop.py", "m22")
x03line = "The census said " + ctl.JLINE + "."
print("M22-JOURNAL_RE match(prose)=%r match(bare)=%r"
      % (m22.JOURNAL_RE.match(x03line), m22.JOURNAL_RE.match(ctl.JLINE)))

for mut_name, ctl_name in PROBES:
    counter = SEAT + "/mutants/" + mut_name + ".py"
    kind, g = M[ctl_name]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ctl.COUNTER = counter
        rc, observed, clauses = ctl.score(base, g, kind)
    print("PROBE %-26s x %-30s kind=%-7s rc=%d admitted-in=%s"
          % (mut_name, ctl_name, kind, rc, observed.split(" verdict")[0]))
    print("   %s" % clauses)

shutil.rmtree(SCRATCH, ignore_errors=True)
