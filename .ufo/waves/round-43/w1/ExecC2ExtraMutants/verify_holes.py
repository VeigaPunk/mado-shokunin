#!/usr/bin/env python3
"""Independent mechanism check for the three non-declared survivors.

Regenerates the three fixtures with the control runner's own helpers and shows the
*branch* that lets each through, without relying on the counter's verdict line.
"""
import importlib.util
import os
import re
import sys

os.environ["TMPDIR"] = "/fast/scratch/hyaku/mado-r43/ExecC2ExtraMutants"
os.makedirs(os.environ["TMPDIR"], exist_ok=True)
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
CTL = os.path.join(LANE, ".ufo/waves/round-43/ctl/run-c2-controls.py")
spec = importlib.util.spec_from_file_location("ctl43", CTL)
ctl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctl)
ctr_spec = importlib.util.spec_from_file_location(
    "ctr43", os.path.join(LANE, "quality/counters/c2-r43-gkeep-entry.py"))
ctr = importlib.util.module_from_spec(ctr_spec)
ctr_spec.loader.exec_module(ctr)

G = ctl.admitted()
LES, SRC = ctl.LES, ctl.SRC
gate = lambda i: [l for l in G[LES].splitlines() if l.startswith("GATE %s " % i)][0]

# 1. clause d outside-section scan: identical vs differing duplicate
same = dict(G)
same[LES] = same[LES] + "\n## Notes\n\n" + gate("S293") + "\n"
differ = dict(G)
differ[LES] = differ[LES] + "\n## Notes\n\n" + ctl.gate_line(
    "S293", ".ufo/waves/round-42/fetch/Hyprland-Target.cpp", b"x" * 300, "stale line")
for tag, g in (("identical", same), ("differing", differ)):
    lesson = g[LES]
    glines = ctr.unfenced("\n".join(ctr.section(lesson, "## Gate")))
    in_gate = set(glines)
    total = [l for l in ctr.unfenced(lesson) if re.match(r"^GATE S\d", l)]
    outside = [l for l in total if l not in in_gate]
    outside_notes = [l for l in lesson.split("## Notes", 1)[-1].splitlines()
                     if l.startswith("GATE ")]
    print("d-outside %-9s gate_lines=%d in_gate_set=%d notes_gate_lines=%d "
          "counted_outside=%d" % (tag, len(total), len(in_gate), len(outside_notes),
                                  len(outside)))

# 2. clause i staged_ok is basename-only
STAGED = ctr.STAGED
for p in ("merge/mado/knowledge/corpus/knowledge/gkeep-size-to-real-size-r11.md",
          "/tmp/gkeep-size-to-real-size-r11.md",
          "/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/"
          "gkeep-size-to-real-size-r11.md"):
    print("i-staged_ok %-92s basename_in_STAGED=%s" % (p, os.path.basename(p) in STAGED))
admit = [m for m in map(ctr.ADMIT_RE.match,
                        [l for l in ctr.unfenced("\n".join(
                            ctr.section(G[LES], "## Gate")))]) if m]
print("i-admit_regex groups on the genuine line:", admit[0].groups())

# 3. two-digit id: every id reader requires 3+ digits
entry = G[ctl.ENTRY].replace("recheck: 90d", "source: S99 - two-digit id\nrecheck: 90d")
entry = entry.replace("host rules", "**OBS** S99 an unregistered citation.\nhost rules")
print("b-src_re on 'source: S99':", bool(ctr.SRC_RE.match("source: S99 - two-digit id")))
print("b-src_re on 'source: S94' (2 digits):", bool(ctr.SRC_RE.match("source: S94 - x")))
print("b-src_re on 'source: S290' (3 digits):", bool(ctr.SRC_RE.match("source: S290 - x")))
print("b-ghost_scan finds:", re.findall(r"\b[Ss]\d{3,}\b",
                                        "source: S99 - two-digit id\n**OBS** S99 x"))
print("b-row_re on '| S99 | ... |':", bool(ctr.ROW_RE.match("| S99 | t | code | A | s | a | t | mined | 2026-10-26 | 90d | x |")))
print("b-gate_re on a S99 gate:", bool(ctr.GATE_RE.match(
    'GATE S99 receipt=.ufo/waves/round-43/fetch/S99.txt sha256=%s quote="a b c"' % ("0" * 64))))

# 4. declared residual, for contrast: claim-to-quote binding is not tested at all
print("g-claim-binding: clause g tests quote+locator presence in a line, not the claim;"
      " no token of the prose sentence is examined")
print("d-held-receipt pin: PINS lookup is guarded by `if i in new_ids:` ->",
      [l.strip() for l in open(os.path.join(
          LANE, "quality/counters/c2-r43-gkeep-entry.py")).read().splitlines()
       if "if i in new_ids:" in l])
sys.exit(0)
