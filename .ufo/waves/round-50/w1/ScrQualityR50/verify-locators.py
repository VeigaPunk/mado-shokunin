#!/usr/bin/env python3
"""verify-locators.py — every locator this seat's criteria.md cites, proved by its own bytes.

Each row is (path relative to the lane, line, expected substring). The script opens the line and
greps it; a locator that does not hold prints LOCATOR_FAIL and the script exits 1. It also prints
the derived facts the criteria rest on: QUALITY.md's highest criterion number, and whether round
50's lesson file exists.
"""
import os
import subprocess
import sys

LANE = os.environ.get("LANE", ".")
FLEET = os.path.dirname(os.path.abspath(LANE))

ROWS = [
    ("corpus/lessons/round-49.md", 31, "M49-1"),
    ("corpus/lessons/round-49.md", 41, "M49-3"),
    ("corpus/lessons/round-49-verifier-spotcheck.md", 126, "D2"),
    ("corpus/lessons/round-49-verifier-spotcheck.md", 136, "D6"),
    ("corpus/QUALITY.md", 507, "96. **A landed contract"),
    ("corpus/QUALITY.md", 521, "97. **A corpus-to-corpus locator"),
    ("corpus/QUALITY.md", 533, "98. **A wave's scratch bound"),
    ("corpus/QUALITY.md", 543, "99. A round's closure section"),
    (".ufo/waves/round-50/claims.md", 39, "D6 (QUALITY criteria for M49-1 and M49-3)"),
    (".ufo/waves/round-49/w1/ScrSkill/pins/KeybindManager.cpp", 369, "xkb_state_key_get_one_sym"),
    (".ufo/waves/round-49/w1/ScrSkill/pins/KeybindManager.cpp", 332, "xkb_state_new(PKEYMAP)"),
    (".ufo/waves/round-49/w1/ScrSkill/pins/IKeyboard.cpp", 379, "xkb_state_update_mask(m_xkbState"),
    (".ufo/waves/round-49/w1/ScrSkill/pins/IKeyboard.cpp", 382, "xkb_state_update_mask(m_xkbSymState"),
    (".ufo/waves/round-50/w1/ScrQualityR50/round-50.md", 11, "M50-1"),
]

ok = bad = 0
for rel, line, want in ROWS:
    path = os.path.join(LANE, rel)
    try:
        with open(path, "r", errors="replace") as fh:
            text = fh.read().splitlines()[line - 1]
    except (OSError, IndexError):
        print(f"LOCATOR_FAIL {rel}:{line} unreadable")
        bad += 1
        continue
    if want in text:
        print(f"LOCATOR_OK {rel}:{line} has={want!r}")
        ok += 1
    else:
        print(f"LOCATOR_FAIL {rel}:{line} want={want!r} got={text[:90]!r}")
        bad += 1

# derived facts
qf = os.path.join(LANE, "corpus/QUALITY.md")
nums = [int(l.split(".", 1)[0]) for l in open(qf, errors="replace")
        if l[:1].isdigit() and ". " in l[:6]]
print(f"QUALITY_MAX={max(nums)}")
lesson = os.path.join(LANE, "corpus/lessons/round-50.md")
print(f"ROUND50_LESSON={'present' if os.path.isfile(lesson) else 'absent'}")
r49 = os.path.join(FLEET, ".ufo/reports/round-49/mado.md")
print(f"FLEET_R49_REPORT={'present' if os.path.isfile(r49) else 'absent'}")
rc = subprocess.run(("git", "-C", LANE, "cat-file", "-e",
                     "8a370cd4:.ufo/waves/round-49/w1-results.json"), capture_output=True)
print(f"R49_RESULTS_AT_CLOSURE={'present' if rc.returncode == 0 else 'absent'}")
print(f"LOCATORS: ok={ok} fail={bad}")
sys.exit(0 if bad == 0 else 1)
