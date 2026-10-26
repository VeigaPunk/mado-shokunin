#!/usr/bin/env python3
"""Verify the deletion quotes this seat reports, against the lane's git objects only.

Read-only: `git show` on the lane at the data commit `e4678921` and on the deletion fixture. No write to the lane.
Each check states the locator it computed (grep -n equivalent) and asserts:
  (1) the quoted text sits on that line of that file at e4678921;
  (2) the text appears in a removed ('-') line of deletions.diff;
  (3) the surviving counterpart (the place the same fact stays) is present at e4678921.
"""
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
DATA = "e46789213830597348fe96a351ae004d10587385"
SEAT = LANE + "/.ufo/waves/round-44/w2/SimpLanded"

DELETIONS = [
    # (label, path, line, quote)
    ("D1 entry", "corpus/knowledge/hyprland-gkeep-size-request-r44.md", 40,
     "What Hyprland does with a buffer of another size after the ack is outside this entry's pins (UNK)."),
    ("D2 entry", "corpus/knowledge/hyprland-gkeep-size-request-r44.md", 9,
     "(Hyprland efb5099, wayland-protocols 1.49, GTK 4.24.1, gkeep 133b867)"),
    ("D3 README", "corpus/README.md", 318,
     'to "not floating" (a pseudo-tiled client takes its box from the stored pseudo size, which `clients -j` does not'),
    ("D4 SKILL", "SKILL.md", 289,
     'Licenses cell overstates \u2014 "the tiler, not the floating rule path, set its box" is false for a pseudo-tiled client,'),
    ("D4 SKILL", "SKILL.md", 290,
     "whose box comes from the rule's size stored as its pseudo size (`Hyprland-Window.cpp:2402-2408`, round-44 pin"),
    ("D5 lesson", "corpus/lessons/round-44.md", 52,
     "Rejected staged material, with reasons and flips, is in the REFUSE lines above and the ledger below;"),
    ("D6 docstring", "tools/mado-geometry.py", 16,
     "state (FULLSCREEN, MAXIMIZED) instead of comparing; the round-43 tool printed"),
    ("D6 docstring", "tools/mado-geometry.py", 17,
     "DIFFER there, true about the box and silent about the cause."),
]

SURVIVORS = [
    # (what stays, path, line, quote that must still be there)
    ("D1: the same boundary, in the entry's own not-established list",
     "corpus/knowledge/hyprland-gkeep-size-request-r44.md", 79,
     "What Hyprland does when a client commits a buffer whose size differs from the acked one (not among the pins)."),
    ("D2: the four documents and versions, in the entry's source: lines",
     "corpus/knowledge/hyprland-gkeep-size-request-r44.md", 3, "@ efb5099"),
    ("D2: wayland-protocols version", "corpus/knowledge/hyprland-gkeep-size-request-r44.md", 5, "wayland-protocols 1.49"),
    ("D2: gtk version", "corpus/knowledge/hyprland-gkeep-size-request-r44.md", 6, "@ 4.24.1"),
    ("D2: gkeep commit", "corpus/knowledge/hyprland-gkeep-size-request-r44.md", 7, "@ 133b867"),
    ("D3/D4: the tool's own TILED licence", "tools/mado-geometry.py", 61,
     "TILED claims only that the client is not floating: a"),
    ("D3/D4: the tool's pseudo-size clause", "tools/mado-geometry.py", 62,
     "pseudo-tiled client takes its size from its stored pseudo size, and the dump"),
    ("D4: the SKILL TILED row's caveat cell", "SKILL.md", 276,
     "stores the rule's size as its pseudo size (`Window.cpp:2402-2408`, round-43 pin)"),
    ("D4: the lesson's M44-3 evidence, with the round-44 pin", "corpus/lessons/round-44.md", 130,
     "while for a pseudo-tiled client the size arrives from the stored rule pseudo-size"),
    ("D6: the calibration record, in the frozen v2 registration", ".ufo/waves/round-44/registration-v2.md", 13,
     "silent about the cause"),
    ("D6: the calibration record, in the round's own mistake row", "corpus/lessons/round-44.md", 190,
     "The box really differs; the tool could not say why."),
]

FAILS = []


def show(rev, path):
    p = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
                       capture_output=True)
    if p.returncode != 0:
        FAILS.append("missing at %s: %s" % (rev[:8], path))
        return []
    return p.stdout.decode("utf-8", "replace").split("\n")


def check(label, path, line, quote, want=True, rev=DATA, unique=True):
    lines = show(rev, path)
    got = lines[line - 1] if 0 < line <= len(lines) else "<no such line>"
    hits = [n for n, l in enumerate(lines, 1) if quote in l]
    if unique:
        # locator is computed, not typed: the line number must be the only line holding the quote
        ok = bool(hits) and all(h == line for h in hits)
    else:
        ok = line in hits
    ok = ok if want else not hits
    where = "%s:%d" % (path, line)
    if ok:
        print("PASS %-8s %-46s computed_line=%d" % (label, where, hits[0]))
    else:
        print("FAIL %-8s %-46s hits=%s" % (label, where, hits))
        FAILS.append(label)
        if got.strip():
            print("     line reads: %s" % got[:150])


def main():
    diff = open(SEAT + "/deletions.diff", encoding="utf-8").read()
    removed = "\n".join(l[1:] for l in diff.splitlines() if l.startswith("-") and not l.startswith("---"))
    for label, path, line, quote in DELETIONS:
        check(label, path, line, quote)
        if quote not in removed:
            print("FAIL diff    %s: quote absent from a removed line of deletions.diff" % label)
            FAILS.append(label + "-diff")
        else:
            print("PASS diff    %-46s removed-line carries the quote" % ("%s:%d" % (path, line)))
    for label, path, line, quote in SURVIVORS:
        check(label, path, line, quote, unique=False)
    # the tool and the frozen C1 reference were byte-equal at the data commit (the tradeoff D6 pays)
    tool = subprocess.run(["git", "-C", LANE, "show", DATA + ":tools/mado-geometry.py"],
                          capture_output=True).stdout
    ref = subprocess.run(["git", "-C", LANE, "show", DATA + ":.ufo/waves/round-44/c1/ctl-ref-tool-v2.py.txt"],
                         capture_output=True).stdout
    print("INFO tool==reference at %s: %s" % (DATA[:8], "yes" if tool == ref else "no"))
    print("\nQUOTE-VERIFY %s (%d checks, %d failures)" %
          ("PASS" if not FAILS else "FAIL", len(DELETIONS) + len(SURVIVORS), len(FAILS)))
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
