#!/usr/bin/env python3
"""Verify every located quote used in this seat's mistakes.md.

Each row is (file, line-or-range, fragment, max_words). The file is opened relative to --root; the cited lines are
whitespace-collapsed and the fragment must appear in them. A locator that exists but does not carry its fragment is a
violation (criterion 77's rule). --shift N moves every locator by N lines to show the check can fail.
"""
import argparse
import re
import sys

ROWS = [
    ("mado-shokunin/corpus/knowledge/hyprland-input-devices-r46.md", "57", "live-devices-host-l1.txt"),
    ("mado-shokunin/.ufo/waves/round-46/receipts/live-devices-host-l1.txt", "1", "l1-draft/mado-devices.py"),
    ("mado-shokunin/.ufo/waves/round-46/receipts/live-devices-host-r46.txt", "1", "tools/mado-devices.py"),
    (".ufo/reports/round-46/mado.md", "55", "The helper skips new files over 1 MiB inside a named directory."),
    (".ufo/reports/round-46/mado.md", "90", "quality: improved."),
    ("mado-shokunin/SKILL.md", "770", "no synthetic marker yet, so a red exit is expected until it lands"),
    ("mado-shokunin/corpus/lessons/round-46.md", "307-308", "slips a third time"),
    ("mado-shokunin/corpus/lessons/round-46.md", "311", "age now 4 rounds"),
    ("mado-shokunin/corpus/lessons/round-46.md", "360", "S290-S297 supersession not landed"),
    ("mado-shokunin/corpus/lessons/round-46-verifier-spotcheck.md", "52", "defect R1"),
    ("mado-shokunin/corpus/lessons/round-46-verifier-spotcheck.md", "95", "unprovable-but-better"),
    ("mado-shokunin/corpus/lessons/round-46-verifier-spotcheck.md", "116", "third deferral"),
    ("mado-shokunin/.ufo/waves/round-46/w1/ScrRoutedAges/ages.md", "14-15", "first_routed_round"),
    ("mado-shokunin/.ufo/waves/round-46/w1/ScrRoutedAges/ages.md", "55", "S43:100"),
    ("mado-shokunin/.ufo/waves/round-46/w1/ScrRoutedAges/ages.md", "88", "R43-D2"),
    ("scripts/hyaku/lane-addendum.md", "274-275", "are skipped with a warning"),
    ("scripts/hyaku/jj-lane.sh", "638", "10485760"),
    ("mado-shokunin/.gitignore", "3", "__pycache__/"),
    ("mado-shokunin/quality/counters/c1-r46-devices-v3.py", "76", "sys.dont_write_bytecode = True"),
    ("mado-shokunin/quality/counters/c1-r46-devices-v2.py", "69", "sys.dont_write_bytecode = True"),
    ("mado-shokunin/quality/counters/c1-r46-devices.py", "67-68", "MODEL_SHA256"),
    ("mado-shokunin/quality/counters/c1-r46-devices.py", "98", "pinned(MODEL_PATH, MODEL_SHA256)"),
    ("mado-shokunin/quality/counters/c1-r46-devices-v3.py", "121", "pinned(MODEL_PATH, MODEL_SHA256)"),
    ("mado-shokunin/.ufo/waves/round-46/receipts/session-material-data.txt", "117", "SESSION_MATERIAL:"),
    ("mado-shokunin/.ufo/waves/round-47/w1/ScrMistakes/receipts/session-material-head.txt", "4", "SESSION_MATERIAL:"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--shift", type=int, default=0)
    a = ap.parse_args()
    bad = 0
    for path, rng, frag in ROWS:
        lo, _, hi = rng.partition("-")
        lo = int(lo) + a.shift
        hi = int(hi) + a.shift if hi else lo
        p = "%s/%s" % (a.root, path)
        try:
            lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
        except OSError as e:
            print("LOC %s:%s verdict=NOFILE %s" % (path, rng, e))
            bad += 1
            continue
        seg = " ".join(lines[lo - 1:hi])
        seg = re.sub(r"\s+", " ", seg)
        words = len(frag.split())
        ok = re.sub(r"\s+", " ", frag) in seg and words <= 25
        print("LOC %s:%s words=%d found=%d verdict=%s" % (path, rng, words, int(ok), "OK" if ok else "MISS"))
        if not ok:
            bad += 1
    print("QUOTE_CHECK: checked=%d failed=%d shift=%d" % (len(ROWS), bad, a.shift))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
