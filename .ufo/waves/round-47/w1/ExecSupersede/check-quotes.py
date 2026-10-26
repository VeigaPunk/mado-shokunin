#!/usr/bin/env python3
"""Re-verify every locator and quote the round-47 supersession rows (S346-S353) cite.

Run from anywhere:  python3 -I check-quotes.py [--fetch DIR] [--lane DIR]
Writes locators.txt / shape-check.txt next to this script (or --out DIR).
Exit 0 only when every check passes; last line is QUOTE_AND_RANGE_CHECK: ok.
No third-party imports, no network, no writes outside --out.
"""
import argparse
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# (row, fetch basename, line, quote)  -- quote must appear exactly once, on `line`
QUOTES = [
    ("S346", "RegexMatchEngine.cpp", 16,
     "return re2::RE2::FullMatch(other, *m_regex) != m_negative;"),
    ("S347", "DefaultFloatingAlgorithm.cpp", 56,
     "const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);"),
    ("S348", "Target.cpp", 68,
     "void ITarget::rememberFloatingSize(const Vector2D& size) {"),
    ("S349", "WindowTarget.cpp", 339,
     "if (DESIRED_GEOM.width <= 2 || DESIRED_GEOM.height <= 2) {"),
    ("S350", "GeometricMovableAnimated.cpp", 19,
     "case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();"),
    ("S351", "host-clients-r43.json", 5, '"class": "Alacritty",'),
    ("S352", "gkeep-ui-excerpt.py", 33, "window.set_default_size(420, 500)"),
    ("S353", "Rule.cpp", 52, "{RULE_PROP_CLASS, RULE_MATCH_ENGINE_REGEX},"),
]

# anchor ranges to print (row, basename, first, last)
RANGES = [
    ("S346", "RegexMatchEngine.cpp", 6, 13), ("S346", "RegexMatchEngine.cpp", 15, 17),
    ("S346", "Rule.cpp", 52, 52), ("S346", "Rule.cpp", 98, 98),
    ("S346", "WindowRule.cpp", 395, 396),
    ("S347", "DefaultFloatingAlgorithm.cpp", 16, 16),
    ("S347", "DefaultFloatingAlgorithm.cpp", 19, 45),
    ("S347", "DefaultFloatingAlgorithm.cpp", 49, 66),
    ("S347", "DefaultFloatingAlgorithm.cpp", 56, 58),
    ("S347", "DefaultFloatingAlgorithm.cpp", 60, 61),
    ("S347", "DefaultFloatingAlgorithm.cpp", 68, 77),
    ("S347", "DefaultFloatingAlgorithm.cpp", 79, 84),
    ("S347", "DefaultFloatingAlgorithm.cpp", 85, 88),
    ("S347", "DefaultFloatingAlgorithm.cpp", 90, 91),
    ("S347", "DefaultFloatingAlgorithm.cpp", 93, 102),
    ("S347", "DefaultFloatingAlgorithm.cpp", 193, 196),
    ("S347", "Window.cpp", 2402, 2409), ("S347", "Window.cpp", 2413, 2414),
    ("S348", "Target.cpp", 10, 14), ("S348", "Target.cpp", 64, 66),
    ("S348", "Target.cpp", 68, 70), ("S348", "Target.cpp", 72, 74),
    ("S349", "WindowTarget.cpp", 297, 304), ("S349", "WindowTarget.cpp", 313, 313),
    ("S349", "WindowTarget.cpp", 323, 326), ("S349", "WindowTarget.cpp", 339, 339),
    ("S349", "WindowTarget.cpp", 342, 347), ("S349", "WindowTarget.cpp", 350, 362),
    ("S349", "WindowTarget.cpp", 364, 364),
    ("S350", "GeometricMovableAnimated.cpp", 10, 11),
    ("S350", "GeometricMovableAnimated.cpp", 19, 20),
    ("S350", "GeometricMovableAnimated.cpp", 26, 29),
    ("S353", "Rule.cpp", 52, 52), ("S353", "Rule.cpp", 98, 98),
]

# (row, basename, pattern, expected count) -- the negative sweeps
SWEEPS = [
    ("S351", "host-clients-r43.json", "fullscreen", 0),
    ("S351", "host-clients-r43.json", "title", 0),
    ("S351", "host-clients-r43.json", "org.omarchy.gkeep", 0),
    ("S352", "gkeep-ui-excerpt.py", "set_size_request", 0),
]

# row -> primary fetch basename, for the anchor-locator bounds check
PRIMARY = {
    "S346": "RegexMatchEngine.cpp", "S347": "DefaultFloatingAlgorithm.cpp",
    "S348": "Target.cpp", "S349": "WindowTarget.cpp",
    "S350": "GeometricMovableAnimated.cpp",
    "S353": "Rule.cpp",
}

ENUM_KIND = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book", "community", "own-work"}
ENUM_TIER = {"A", "B", "C"}
ENUM_STATUS = {"queued", "mined", "rejected"}

fails = []


def fail(msg):
    fails.append(msg)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_lines(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read().split("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", default=os.path.join(HERE, "fetch"))
    ap.add_argument("--lane", default="/home/vgpnk/Projects/shokunin/mado-shokunin")
    ap.add_argument("--rows", default=os.path.join(HERE, "rows-block.txt"))
    ap.add_argument("--out", default=HERE)
    args = ap.parse_args()

    def locate(name):
        """fetch copy first, then the lane's round-43 own-work copy."""
        cand = [os.path.join(args.fetch, name),
                os.path.join(args.fetch, "Hyprland-" + name),
                os.path.join(args.lane, ".ufo/waves/round-43/fetch", name)]
        for c in cand:
            if os.path.isfile(c):
                return c
        fail("missing source for %s (looked in %s)" % (name, args.fetch))
        return None

    lines_out = ["# locators.txt -- computed by check-quotes.py (no values typed by hand)", ""]

    # ---- quotes
    lines_out.append("## 1. Gate quotes (row, line, hits, words, sha256)")
    for row, name, want_line, quote in QUOTES:
        path = locate(name)
        if not path:
            continue
        text = read_lines(path)
        if want_line > len(text):
            fail("%s: locator :%d beyond %d lines of %s" % (row, want_line, len(text), name))
            continue
        hits = [i + 1 for i, ln in enumerate(text) if quote in ln]
        words = len(quote.split())
        digest = sha256(path)
        on_line = quote in text[want_line - 1]
        if hits != [want_line]:
            fail("%s: quote hits %r, expected [%d] in %s" % (row, hits, want_line, name))
        if not on_line:
            fail("%s: quote not on :%d of %s" % (row, want_line, name))
        if words > 25:
            fail("%s: quote is %d words (>25)" % (row, words))
        lines_out.append("%-4s :%-4d hits=%d words=%2d sha256=%s..  %s"
                         % (row, want_line, len(hits), words, digest[:16], name))
        lines_out.append("      %s" % text[want_line - 1].strip())

    # ---- anchor ranges, with the first and last source line printed
    lines_out.append("")
    lines_out.append("## 2. Anchor ranges (first and last line of each, from the re-fetched bytes)")
    for row, name, a, b in RANGES:
        path = locate(name)
        if not path:
            continue
        text = read_lines(path)
        if not (1 <= a <= b <= len(text)):
            fail("%s: range %s:%d-%d outside 1..%d" % (row, name, a, b, len(text)))
            continue
        lines_out.append("%-4s %s:%d-%d" % (row, name, a, b))
        lines_out.append("      first %4d | %s" % (a, text[a - 1].strip()))
        if b != a:
            lines_out.append("      last  %4d | %s" % (b, text[b - 1].strip()))

    # ---- every locator token inside each primary anchor cell must be in bounds
    lines_out.append("")
    lines_out.append("## 3. Anchor-cell locator bounds (every :N / :N-M token, primary source file)")
    rows = [l for l in read_lines(args.rows) if l.strip()]
    if len(rows) != 8:
        fail("rows-block.txt holds %d rows, expected 8" % len(rows))
    for raw in rows:
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if len(cells) != 11:
            fail("%s: %d cells (expected 11)" % (cells[0] if cells else "?", len(cells)))
            continue
        rid, anchor = cells[0], cells[5]
        name = PRIMARY.get(rid)
        if not name:
            lines_out.append("%-4s (own-work anchor, checked in section 4)" % rid)
            continue
        path = locate(name)
        if not path:
            continue
        n = len(read_lines(path))
        toks = re.findall(r":(\d+)(?:-(\d+))?", anchor.split("@ tag")[0])
        bad = []
        for a, b in toks:
            lo, hi = int(a), int(b or a)
            if not (1 <= lo <= hi <= n):
                bad.append("%d-%d" % (lo, hi))
        lines_out.append("%-4s %s tokens=%d range=1..%d out-of-bounds=%s"
                         % (rid, name, len(toks), n, bad or "none"))
        if bad:
            fail("%s: anchor locators out of bounds in %s: %s" % (rid, name, bad))

    # ---- own-work anchors: the cited lines must carry what the cell says
    lines_out.append("")
    lines_out.append("## 4. Own-work anchors (line content at the cited numbers)")
    ln = read_lines(os.path.join(args.lane, ".ufo/waves/round-43/fetch/host-clients-r43.json"))
    for want in (2, 17, 32, 47):
        if ln[want - 1].strip() != "{":
            fail("S351: line %d of the dump is not an object opener" % want)
        lines_out.append("S351 dump :%-3d | %s" % (want, ln[want - 1].strip()))
    for want in (5, 20, 35, 50):
        if not ln[want - 1].strip().startswith('"class"'):
            fail("S351: line %d of the dump is not a class line" % want)
        lines_out.append("S351 dump :%-3d | %s" % (want, ln[want - 1].strip()))
    ex = read_lines(os.path.join(args.lane, ".ufo/waves/round-43/fetch/gkeep-ui-excerpt.py"))
    if "application_id" not in ex[6 - 1]:
        fail("S352: excerpt :6 is not the application_id line")
    if "set_default_size" not in ex[33 - 1]:
        fail("S352: excerpt :33 is not the default-size line")
    lines_out.append("S352 excerpt :6  | %s" % ex[6 - 1].strip())
    lines_out.append("S352 excerpt :33 | %s" % ex[33 - 1].strip())

    # ---- negative sweeps
    lines_out.append("")
    lines_out.append("## 5. Negative sweeps (a count of 0 is the evidence)")
    for row, name, pat, want in SWEEPS:
        path = locate(name)
        if not path:
            continue
        got = sum(1 for ln_ in read_lines(path) if pat in ln_)
        lines_out.append("%s %s: grep -c %s -> %d (want %d)" % (row, name, pat, got, want))
        if got != want:
            fail("%s: sweep %s in %s -> %d, wanted %d" % (row, pat, name, got, want))

    # ---- registry shape of the block itself
    lines_out.append("")
    lines_out.append("## 6. Row shape")
    shape = []
    ids = []
    usedby = set()
    for raw in rows:
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if len(cells) != 11:
            continue
        rid = cells[0]
        ids.append(rid)
        usedby.add(cells[10])
        problems = []
        if not re.fullmatch(r"S[0-9]{3,}", rid):
            problems.append("id")
        if cells[2] not in ENUM_KIND:
            problems.append("kind=%s" % cells[2])
        if cells[3] not in ENUM_TIER:
            problems.append("tier=%s" % cells[3])
        if cells[7] not in ENUM_STATUS:
            problems.append("status=%s" % cells[7])
        if cells[8] != "2026-10-26":
            problems.append("opened=%s" % cells[8])
        if not re.fullmatch(r"(\d{4}-\d{2}-\d{2}|\d+d|on-release|on-[a-z]+)", cells[9]):
            problems.append("recheck=%s" % cells[9])
        if "supersedes S" not in cells[6] and rid != "S353":
            problems.append("no supersedes opener")
        if raw.strip().count("|") != 12:
            problems.append("pipes=%d" % raw.strip().count("|"))
        shape.append((rid, "OK" if not problems else "DEFECT " + ",".join(problems)))
        if problems:
            fail("%s: %s" % (rid, ",".join(problems)))
    if ids != sorted(ids) or len(set(ids)) != len(ids):
        fail("ids not ascending and unique: %s" % ids)
    if len(usedby) != 1:
        fail("used-by differs across rows: %s" % sorted(usedby))
    hit = sorted(os.listdir(os.path.dirname(args.rows)))
    for rid, verdict in shape:
        lines_out.append("%s %s" % (rid, verdict))
    lines_out.append("ids=%s contiguous=%s used-by=%s"
                     % (",".join(ids), ids == ["S%d" % i for i in range(int(ids[0][1:]), int(ids[0][1:]) + 8)],
                        ",".join(sorted(usedby))))
    lines_out.append("defects=%d" % sum(1 for _, v in shape if v != "OK"))

    with open(os.path.join(args.out, "locators.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines_out) + "\n")
    with open(os.path.join(args.out, "shape-check.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join("%s %s" % (r, v) for r, v in shape) +
                 "\ndefects=%d\n" % sum(1 for _, v in shape if v != "OK"))

    if fails:
        for f in fails:
            print("FAIL " + f)
        print("QUOTE_AND_RANGE_CHECK: %d failure(s)" % len(fails))
        return 1
    print("QUOTE_AND_RANGE_CHECK: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
