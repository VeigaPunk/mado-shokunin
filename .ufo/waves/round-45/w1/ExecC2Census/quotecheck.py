#!/usr/bin/env python3
"""ExecC2Census independent check (NOT the counter): extract QUOTES from build-pos.py,
count normalized occurrences in each pin (raw and comments-stripped), compute the
start line, then compare with the locators the L1 entry uses for each id."""
import ast
import os
import re
import sys

L1 = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/l1-draft"
F = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/fetch/"
ENTRY = os.path.join(L1, "entry.md")

src = open(os.path.join(L1, "build-pos.py")).read()
i = src.index("QUOTES = {")
j = src.index("\n}", i)
QUOTES = ast.literal_eval(src[i + len("QUOTES = "):j + 2])
ANCHORS = [(m.group(1), m.group(2), m.group(3) or m.group(2)) for m in re.finditer(
    r"([A-Za-z0-9-]+\.(?:cpp|hpp|h|md)):(\d+)(?:-(\d+))?", src)]


def collapse(text):
    out, lines, prev = [], [], True
    for ln, line in enumerate(text.split("\n"), 1):
        for ch in line + "\n":
            if ch.isspace():
                if not prev:
                    out.append(" ")
                    lines.append(ln)
                    prev = True
            else:
                out.append(ch)
                lines.append(ln)
                prev = False
    return "".join(out), lines


def word_hits(text, q):
    isw = lambda c: c.isalnum() or c == "_"
    hits, start = [], 0
    while True:
        k = text.find(q, start)
        if k < 0:
            return hits
        before = text[k - 1] if k > 0 else " "
        after = text[k + len(q)] if k + len(q) < len(text) else " "
        if not (isw(q[0]) and isw(before)) and not (isw(q[-1]) and isw(after)):
            hits.append(k)
        start = k + 1


def strip_comments(text, path):
    if path.endswith((".cpp", ".hpp", ".h", ".cc")):
        text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
        return re.sub(r"//[^\n]*", " ", text)
    if path.endswith((".py", ".conf")):
        return re.sub(r"#[^\n]*", " ", text)
    return text


def main():
    entry = open(ENTRY).read().splitlines()
    bad = 0
    print("id   receipt                                raw# strip# start  entry-locator  verdict")
    for sid in sorted(QUOTES):
        rname, quote = QUOTES[sid]
        raw = open(F + rname, "rb").read().decode("utf-8", "replace")
        nq = re.sub(r"\s+", " ", quote).strip()
        flat, lmap = collapse(raw)
        hits = word_hits(flat, nq)
        nstrip = len(word_hits(re.sub(r"\s+", " ", strip_comments(raw, rname)).strip(), nq))
        start = lmap[hits[0]] if hits else None
        loc = None
        for l in entry:
            if re.search(r"\b%s\b" % sid, l) and re.search(re.escape(rname) + r":\d+", l):
                m = re.search(re.escape(rname) + r":(\d+)(?:-(\d+))?", l)
                loc = "%s-%s" % (m.group(1), m.group(2)) if m.group(2) else m.group(1)
                break
        a = int(loc.split("-")[0]) if loc else None
        ok = len(hits) == 1 and nstrip == 1 and loc and a <= start and int(loc.split("-")[-1]) >= start
        bad += 0 if ok else 1
        print("%-4s %-40s %-5d %-6d %-6s %-14s %s" % (
            sid, rname, len(hits), nstrip, start, loc or "NONE", "OK" if ok else "MISMATCH"))
    print("mismatches=%d" % bad)

    print("\nROW anchor cell ranges (b <= receipt line count):")
    for name, a, b in ANCHORS:
        n = len(open(F + name, encoding="utf-8", errors="replace").read().split("\n"))
        print("%-42s %s-%s receipt_lines=%d %s" % (name, a, b, n,
                                                   "OK" if int(b) <= n else "OUT_OF_RANGE"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
