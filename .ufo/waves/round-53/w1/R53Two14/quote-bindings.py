#!/usr/bin/env python3
"""quote-bindings.py — seat R53Two14 mechanical quote/pin census (read-only).

Reads the committed round-52 entry and the committed round-52 fetch bytes, both
under the lane root given as argv[1] (default: the lane). For every proposition
row `| P## | proposition | S### | file:anchor | `quote` | ... |` it reports the
whitespace-collapsed minimal line span of the pin file that contains the quote
and whether that span lies inside the stated anchor. It makes no semantic
entailment claim: subject, localization and support clauses are reviewer work.
"""
import os
import re
import sys

LANE = sys.argv[1] if len(sys.argv) > 1 else "/home/vgpnk/Projects/shokunin/mado-shokunin"
FETCH = os.path.join(LANE, ".ufo/waves/round-52/fetch")
ENTRY = os.path.join(LANE, "corpus/knowledge/hyprland-synthetic-dispatch-r52.md")


def collapse(text):
    return re.sub(r"\s+", " ", text).strip()


def main():
    files = {
        name: open(os.path.join(FETCH, name), encoding="utf-8", errors="replace").read()
        for name in sorted(os.listdir(FETCH))
        if name.endswith((".cpp", ".hpp"))
    }
    rows = []
    for line in open(ENTRY, encoding="utf-8"):
        if re.match(r"^\|\s*P\d\d\s*\|", line):
            rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    print("# entry: %s" % ENTRY)
    print("# fetch: %s (%d files)" % (FETCH, len(files)))
    print("props=%d" % len(rows))
    spliced, outside = [], []
    for cells in rows:
        pid, pin, quote = cells[0], cells[3], cells[4].strip("`")
        fname, _, anchor = pin.partition(":")
        text = files.get(fname, "")
        if not text:
            print("%s MISSING_PIN_FILE pin=%s" % (pid, pin))
            continue
        lines = text.splitlines()
        q = collapse(quote)
        best = None
        for i in range(len(lines)):
            for j in range(i, min(i + 8, len(lines))):
                if q in collapse("\n".join(lines[i : j + 1])):
                    if best is None or (j - i) < (best[1] - best[0]):
                        best = (i, j)
                    break
        words = len(re.findall(r"\S+", q))
        span = "%d-%d" % (best[0] + 1, best[1] + 1) if best else "NONE"
        nums = [int(n) for n in re.findall(r"\d+", anchor)]
        inside = bool(best) and nums[0] <= best[0] + 1 and best[1] + 1 <= nums[-1]
        occ = collapse(text).count(q)
        if best is None:
            spliced.append(pid)
        elif not inside:
            outside.append(pid)
        print(
            "%s file=%s anchor=%s words=%d span=%s inside_anchor=%s occurrences=%d"
            % (pid, fname, anchor, words, span, inside, occ)
        )
    print("spliced_or_absent=%s outside_anchor=%s" % (spliced or "-", outside or "-"))
    return 0 if not spliced else 1


if __name__ == "__main__":
    sys.exit(main())
