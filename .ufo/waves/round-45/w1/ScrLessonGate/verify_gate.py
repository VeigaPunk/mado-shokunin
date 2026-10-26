#!/usr/bin/env python3
"""ScrLessonGate: verify the nine Gate quotes against the frozen pins, using the
FROZEN counter's own helpers (quality/counters/c2-r45-monitor-entry.py) so the
evidence is the predicate's semantics, not a paraphrase. Read-only: reads the
lanes's fetch/ and build-pos.py; writes only stdout."""
import ast
import hashlib
import importlib.util
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FETCH = os.path.join(LANE, ".ufo/waves/round-45/fetch")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ctr = load(os.path.join(LANE, "quality/counters/c2-r45-monitor-entry.py"), "c2r45")
bp = open(os.path.join(LANE, ".ufo/waves/round-45/l1-draft/build-pos.py")).read()
QUOTES = ast.literal_eval(re.search(r"QUOTES = (\{.*?\n\})", bp, re.S).group(1))
C = re.search(r'^C = "([0-9a-f]{40})"', bp, re.M).group(1)
HY = "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/src/" % C
FETCH_REL = ".ufo/waves/round-45/fetch/"


def anchor(rname, ranges, rev):
    blob = open(os.path.join(LANE, FETCH_REL + rname), "rb").read()
    return "%s (receipt %s) @ %s, %d B sha256:%s; receipt %s%s" % (
        ranges, rname, rev, len(blob), hashlib.sha256(blob).hexdigest(),
        FETCH_REL, rname)


ROWS_SRC = re.search(r"ROWS = (\[.*?\n\])", bp, re.S).group(1)
ROWS = eval(ROWS_SRC, {"__builtins__": {"len": len, "open": open},
                       "HY": HY, "C": C, "anchor": anchor, "os": os, "hashlib": hashlib})

print("PINS table vs fetch/ bytes and sizes")
ok = True
blobs = {}
for rname, digest in sorted(ctr.PINS.items()):
    blob = open(os.path.join(FETCH, rname), "rb").read()
    blobs[rname] = blob
    got = hashlib.sha256(blob).hexdigest()
    good = got == digest and len(blob) >= ctr.MIN_RECEIPT
    ok &= good
    print("  %-42s %6d B sha256=%s pin_match=%d" % (rname, len(blob), got, good))

print("\nGate quotes (counter semantics: collapsed whitespace, word-bounded,")
print("comments stripped for the code check; distinct path/sha/quote)")
seen_q = set()
for rid, (rname, quote) in QUOTES.items():
    blob = blobs[rname]
    nq = re.sub(r"\s+", " ", quote)
    nwords = len(quote.split())
    at = ctr.quote_at(blob, nq)
    occ = ctr.occurrences(blob, nq)
    inc = ctr.quote_in_code(blob, nq, rname)
    uniq = nq not in seen_q
    seen_q.add(nq)
    good = (3 <= nwords <= 25 and at is not None and len(occ) == 1 and inc and uniq)
    ok &= good
    print("  %s %-42s words=%2d occurrences=%d line=%s code=%d distinct=%d %s"
          % (rid, rname, nwords, len(occ), at, inc, uniq, "OK" if good else "FAIL"))
    print("      quote=%r" % nq)

# cross-receipt: no quote occurs in another cited receipt
print("\ncross-receipt containment (must be 0)")
for rid, (rname, quote) in QUOTES.items():
    nq = re.sub(r"\s+", " ", quote)
    others = [n for n in blobs if n != rname
              and ctr.quote_at(blobs[n], nq) is not None]
    ok &= not others
    print("  %s foreign=%d %s" % (rid, len(others), others))

# held rows cannot carry the monitor scope: their frozen anchor cells do not
# cover the lines the entry cites
print("\nheld-row reuse check (S158/S162 anchor cells, frozen at base)")
rows = {}
for line in ctr.section(open(os.path.join(LANE, "corpus/SOURCES.md")).read(), "## Registry"):
    m = ctr.ROW_RE.match(line)
    if m:
        rows[m.group(1)] = [c.strip() for c in line.strip().split("|")[1:-1]]


def ranges(cell):
    return [(int(a), int(b or a)) for a, b in
            re.findall(r":(\d+)(?:-(\d+))?", cell)]


def covered(cell, lo, hi):
    return any(a <= lo and hi <= b for a, b in ranges(cell))


# S158 -> HyprCtl.cpp (monitors JSON at 242, request at 313-321)
c158 = rows["S158"]
# S162 -> legacy ConfigManager.cpp (handleMonitor 1293-1387)
c162 = rows["S162"]
checks = [
    ("S158", "scope", c158[4]),
    ("S158", "anchor", c158[5]),
    ("S162", "scope", c162[4]),
    ("S162", "anchor", c162[5]),
]
for rid, what, cell in checks:
    print("  %s %s: %s" % (rid, what, cell))
print("  S158 anchor covers HyprCtl.cpp:242 -> %d" % covered(c158[5], 242, 242))
print("  S158 anchor covers HyprCtl.cpp:313-321 -> %d" % covered(c158[5], 313, 321))
print("  S162 anchor covers ConfigManager.cpp:1293-1387 -> %d"
      % covered(c162[5], 1293, 1387))

print("\nnew row scopes (cells 5) and held scopes must differ for clause e")
for rid, _, _, _, scope, anchor_cell, _k in ROWS:
    print("  %s scope=%s" % (rid, scope))
    print("      anchor=%s" % anchor_cell)
print("\nS307 scope equals S158 scope -> %d" % (ROWS[5][4] == c158[4]))
print("S303 scope equals S162 scope -> %d" % (ROWS[1][4] == c162[4]))
print("\nALL_QUOTES_OK=%d" % int(ok))
sys.exit(0 if ok else 1)
