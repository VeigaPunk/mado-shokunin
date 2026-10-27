#!/usr/bin/env python3
"""ExecDoNothing / round 50 - normalise the receipts and build the combined control summary.

Two declared edits, applied to files under ../receipts/ only:

  1. the absolute home prefix -> `~` (the seat rule: no absolute home paths in receipts; the only
     affected counter output is its own `lane=` field, and each receipt says so in its header);
  2. the scratch root is kept as an absolute path (not home state).

Then `receipts/controls-all.txt` is rebuilt from the per-control receipts, so the summary can never
say something a receipt does not.
"""
import os
import re

SEAT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(SEAT, "receipts")
# the lane is derived from this seat's own path (no absolute home path in committed code):
# SEAT is .../w1/ExecDoNothing (this file lives in its controls/), five levels below it
LANE = os.path.realpath(os.path.join(SEAT, "..", "..", "..", "..", ".."))
if not os.path.isfile(os.path.join(LANE, "SKILL.md")):
    raise SystemExit("lane derivation failed: %r has no SKILL.md" % LANE)
NOTE = ("# paths normalised: the absolute home prefix -> ~ (declared edit; no other byte of the "
        "counter output changed)\n")
NOTE_RE = re.compile(r"^# paths normalised:.*\n", re.M)
HOME_RE = re.compile(r"/home/[A-Za-z0-9._-]+")


def normalise(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    text = NOTE_RE.sub("", text)
    if NOTE in text:
        return text
    text = HOME_RE.sub("~", text)
    if text.startswith("# "):
        first, sep, rest = text.partition("\n\n")
        text = first + "\n" + NOTE.rstrip("\n") + sep + rest
    else:
        text = NOTE + text
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return text


def main():
    names = sorted(f for f in os.listdir(OUT) if re.fullmatch(r"c[12]-.*\.txt", f)
                   and f not in ("c1-controls.txt", "c2-controls.txt", "controls-all.txt"))
    lines = ["# ExecDoNothing round 50 - section-9 controls on the FROZEN round-49 counters",
             "# counters: quality/counters/c1-r49-keysym.py sha256 "
             "2597c204abf1e9e7c625d98cf83f0b340a0d82897da4986c550e35c5dff5db62; "
             "quality/counters/c2-r49-bind-entry.py sha256 "
             "bc171714c5349dbe980b84f5c434126965cc8a6e8226704c28604d10cff28c69 (both at "
             "13631f24050f22db92bf5bd33e0f4d014192992e)",
             "# base for both: 03e4ae76aff7a4be59cb69970dd553baa319695a  "
             "(the C2 tree's parent commit is 13631f24)",
             ""]
    for name in names:
        text = normalise(os.path.join(OUT, name))
        body = text.splitlines()
        exit_line = next((l for l in body if l.startswith("# exit: ")), "")
        final = [l for l in body if re.match(r"^PRED-C[12]-r49: ", l)]
        fails = [l for l in body if re.search(r" clause=[a-z] ", l)
                 and re.search(r"(FAIL|ok=0|<6|unanswered|missing|disagrees|no_receipt|mismatch"
                               r"|unparseable|not_ok|=0 |:0)", l)]
        lines.append("==")
        lines.append("%s  %s" % (name, exit_line))
        lines.extend("  " + l for l in final)
        lines.extend("  stop: " + l for l in fails[:14])
        lines.append("")
    with open(os.path.join(OUT, "controls-all.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
