#!/usr/bin/env python3
"""Verify the ScrEntryB draft against PRED-C2-r44 clauses b, g, h (read-only)."""
import importlib.util, os, re, sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
C = os.path.join(LANE, "quality/counters/c2-r44-gkeep-size-request.py")
spec = importlib.util.spec_from_file_location("c2", C)
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)

ENTRY = os.path.join(LANE, ".ufo/waves/round-44/w1/ScrEntryB/hyprland-gkeep-size-request-r44.md")
TSV = os.path.join(os.path.dirname(ENTRY), "quotes.tsv")
F = os.path.join(LANE, ".ufo/waves/round-44/fetch/")
text = open(ENTRY, encoding="utf-8").read()
lines = c2.unfenced(text)
fail = []

# header window
head, fenced, window = [], False, 0
for k, l in enumerate(text.splitlines()):
    if re.match(r"^\s{0,3}(```|~~~)", l):
        fenced = not fenced
        continue
    if not fenced:
        if k < 20:
            head.append(l)
        elif re.match(r"^(source|verified-at|recheck):", l):
            window += 1
ids = []
for l in head:
    m = c2.SRC_RE.match(l)
    if m and m.group(1) not in ids:
        ids.append(m.group(1))
cited = set(re.findall(r"\b[Ss]\d{3,}\b", "\n".join(lines)))
ghosts = cited - set(ids)
va = [l for l in head if l.startswith("verified-at:")]
rc = [l for l in head if l.startswith("recheck:")]
print("ids=%s ghosts=%s window=%d va=%d rc=%d lines=%d" %
      (ids, ghosts, window, len(va), len(rc), len(text.splitlines())))
if len(ids) != 5 or ghosts or window or len(va) != 1 or len(rc) != 1:
    fail.append("header")
if va and va[0] != "verified-at: 2026-10-26":
    fail.append("verified-at value")
if rc and not c2.recheck_ok(rc[0][len("recheck:"):].strip()):
    fail.append("recheck value")

# gates, read from the tsv (id, receipt basename, quote)
gates = {}
for row in open(TSV, encoding="utf-8").read().splitlines()[1:]:
    if not row.strip():
        continue
    i, base, sha, ln, words, q = row.split("\t")
    gates[i] = (base, q)
raw = {i: open(F + b, "rb").read() for i, (b, q) in gates.items()}

ok_all = True
for i, (base, q) in gates.items():
    qn = re.sub(r"\s+", " ", q)
    at = c2.quote_at(raw[i], qn)
    occ = len(c2.occurrences(raw[i], qn))
    code = c2.quote_in_code(raw[i], qn, base)
    words = len(qn.split())
    others = [j for j in raw if j != i and qn in c2.norm_receipt(raw[j])]
    # claim lines: non-source entry lines naming i
    namers = [l for l in lines if re.search(r"\b%s\b" % i, l)
              and not l.startswith("source:")]
    good = (at is not None and occ == 1 and code and 3 <= words <= 25
            and not others and len(namers) == 1
            and qn in re.sub(r"\s+", " ", namers[0])
            and ("%s:%d" % (base, at)) in namers[0]
            and len(set(re.findall(r"\bS\d{3,}\b", namers[0]))) == 1)
    ok_all &= good
    print("%s locator=%s:%s occ=%d code=%d words=%d namers=%d ok=%d"
          % (i, base, at, occ, code, words, len(namers), good))
    if not good:
        fail.append("claim " + i)

# census
ok_h, want = c2.host_census(set(raw), {}, gates if False else
                            {i: [(F + b, "x", "x")] for i, (b, q) in gates.items()},
                            raw, lines)
for w in want:
    n = sum(1 for l in lines if l == w)
    print("census n=%d %s" % (n, w))
    if n != 1:
        fail.append("census")
if not ok_h:
    fail.append("host_census recompute")

# BAD_LOC
for l in lines:
    for b in c2.BAD_LOC:
        if b in l.lower():
            fail.append("BAD_LOC %s in %r" % (b, l[:60]))

# every locator in the entry, recomputed
for l in lines:
    for m in re.finditer(r"([A-Za-z0-9._-]+\.(?:cpp|xml|c|py)):(\d+)", l):
        base, n = m.group(1), int(m.group(2))
        path = F + base
        if not os.path.exists(path):
            fail.append("locator file " + base)
            continue
        body = open(path, encoding="utf-8", errors="replace").read().split("\n")
        if n < 1 or n > len(body):
            fail.append("locator range %s:%d" % (base, n))
        else:
            print("loc %s:%d -> %s" % (base, n, body[n - 1].strip()[:70]))
print("FAILS: %s" % fail)
sys.exit(1 if fail else 0)
