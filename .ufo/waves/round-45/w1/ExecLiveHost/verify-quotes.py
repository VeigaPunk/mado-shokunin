#!/usr/bin/env python3
"""Check every quoted line in .ufo/waves/round-45/w1/ExecLiveHost.md against runs.txt.

Prints `OK <md-line-quote> <- runs.txt:<n>` or `FAIL ...` and exits non-zero on any failure.
Also checks that R1's stdout block reproduces the L1 host receipt's stdout lines verbatim.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
RUNS = os.path.join(HERE, "runs.txt")
MD = os.path.join(HERE, "..", "ExecLiveHost.md")
L1 = os.path.join(LANE, ".ufo/waves/round-45/receipts/live-monitors-host-l1.txt")

quotes = [
    'MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
    'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
    'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK',
    'MADO_MON_RULE: n=1 sel="" mode=preferred pos=auto scale=auto transform=0 mirror=- disabled=false',
    'MADO_MONITORS: lines=0 rules=0 v2=0 unsupported=0 badrules=0 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NO_RULES',
    'MADO_MONITORS: lines=0 rules=0 v2=1 unsupported=0 badrules=0 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NOT_COMPARED',
    'MADO_MON_RULE: n=2 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
    'MADO_MON_OUTPUT: name="DP-1" rule=2 differ=- verdict=AGREE',
    'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
    'MADO_MONITORS: lines=2 rules=2 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK',
    '/home/vgpnk/.config/hypr/monitors.conf:10:monitor = DP-1, 3440x1440@100, 0x0, 1',
    'R2 stdout == R1 stdout: True',
    'R5 stdout == R4 stdout: True ; R11 stdout == R4 stdout: True',
    '# Byte-identical: 1339 bytes each, `cmp` exit 0; no key is present in only one form; the projected fields are equal.',
    'MADO_MONITORS_SELFTEST: 33/33 passed',
    'commented-monitor-lines ~/.config/hypr/monitors.conf=7',
    'commented-monitor-lines ~/.local/share/omarchy/config/hypr/monitors.conf=6',
]

receipt = open(RUNS, encoding="utf-8").read().split("\n")
fails = 0
for q in quotes:
    hits = [i + 1 for i, line in enumerate(receipt) if q in line]
    if hits:
        print("OK   runs.txt:%d  %s" % (hits[0], q[:90]))
    else:
        print("FAIL %s" % q[:120])
        fails += 1

# the report must not carry raw session material (L1 integration: the host serial literal that stood here was
# itself session material and is redacted; the make/model strings remain as they name a public product line)
for bad in ("LG Electronics", "LG ULTRAWIDE"):
    body = open(MD, encoding="utf-8").read()
    if bad in body or bad in "\n".join(receipt):
        print("FAIL session material present: %s" % bad)
        fails += 1

# R1 reproduces the L1 host receipt stdout
l1 = [l for l in open(L1, encoding="utf-8").read().split("\n") if l.startswith("MADO_")]
r1_start = receipt.index("### R1 user monitors.conf, all list form")
r1_end = receipt.index("### R2 user monitors.conf, plain list form")
r1 = [l for l in receipt[r1_start:r1_end] if l.startswith("MADO_")]
if l1 == r1:
    print("OK   R1 stdout == receipts/live-monitors-host-l1.txt stdout (%d lines)" % len(r1))
else:
    print("FAIL R1 stdout differs from the L1 host receipt:\n  L1=%r\n  R1=%r" % (l1, r1))
    fails += 1

print("VERIFY: %s" % ("all checks passed" if fails == 0 else "%d failure(s)" % fails))
sys.exit(0 if fails == 0 else 1)
