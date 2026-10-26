#!/usr/bin/env python3
"""Verify every locator and every quote the seat report cites.

Quotes are checked against the *cited revision's blob* (never the worktree) and
against the frozen predicate files in the lane; every verdict line the report
cites is grepped out of this seat's own receipts. Any failure exits 1.
"""
import hashlib
import os
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-44/w2/ExecDoNothingV2")
DATA = "e46789213830597348fe96a351ae004d10587385"
BASE = "6a1a90528fe533cadee506a9fa3e9d13d15cc41f"
fails = []


def line_of(rev, path, n):
    out = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
                         capture_output=True).stdout.decode("utf-8", "replace")
    lines = out.split("\n")
    if n > len(lines):
        return None, len(lines)
    return lines[n - 1], len(lines)


QUOTES = [
    (DATA, "quality/counters/c2-r44-gkeep-size-request-v2.py", 398,
     "if int(a) <= L <= int(b or a):"),
    (DATA, "quality/counters/c2-r44-gkeep-size-request-v2.py", 56,
     "surface coverage: for each of the twelve SURFACES (pinned receipt, anchor text"),
    (DATA, "quality/counters/c2-r44-gkeep-size-request-v2.py", 58,
     "with a <= L <= b (b = a when absent) and matches the keyword"),
    (DATA, "quality/counters/c1-r44-geometry-states-v2.py", 319,
     "need = math.ceil(KILL_FRACTION * len(sites))"),
    (DATA, "quality/counters/c1-r44-geometry-states-v2.py", 78,
     "KILL_FRACTION = 0.75"),
    (DATA, "quality/counters/c1-r44-geometry-states-v2.py", 31,
     "the comparison sites of every function (selftest, main, usage and functions nested in selftest excluded)"),
    (DATA, "quality/counters/c1-r42-geometry.py", 931,
     "return killed >= KILL_NEED and forced_dead"),
    (DATA, ".ufo/waves/round-44/registration-v2.md", 38,
     "b4 is a naming heuristic (b5 carries the teeth)"),
    (DATA, ".ufo/waves/round-44/registration-v2.md", 64,
     "claim-to-quote binding (CritC2Cheat F1, F6) and registry prose cells (F8) are the non-author reading"),
    (DATA, ".ufo/waves/round-44/registration-v2.md", 65,
     "binds a locator and a keyword per surface, not the truth of the sentence"),
    (DATA, "corpus/lessons/round-44.md", 133,
     "the tool docstring narrows TILED to"),
    (DATA, "tools/mado-geometry.py", 59,
     "BADSIZE (size none) |"),
    (DATA, "tools/mado-geometry.py", 76,
     "every matched client was TILED or BADSIZE"),
    (DATA, "corpus/knowledge/hyprland-gkeep-size-request-r44.md", 72,
     "onAck writes the compositor's own stored size for that serial"),
    (DATA, "tools/mado-geometry.py", 73,
     "NOT_COMPARED (exit 5, agree=0 and maximized + fullscreen > 0) | OK (exit 0),"),
]

print("== quotes (cited revision blob, cited line)")
for rev, path, n, q in QUOTES:
    got, total = line_of(rev, path, n)
    ok = got is not None and q in got
    words = len(q.split())
    ok = ok and words <= 25
    print("%s %s:%d words=%d %r" % ("PASS" if ok else "FAIL", path, n, words, q))
    if not ok:
        fails.append("%s:%d %r" % (path, n, q))
        print("     line read: %r (file has %d lines)" % (got, total))

print("\n== the round-43 tool's docstring carries no round-44 vocabulary")
for rev, path, token in ((BASE, "tools/mado-geometry.py", "NOT_COMPARED"),
                         (BASE, "tools/mado-geometry.py", "FULLSCREEN"),
                         (DATA, "tools/mado-geometry.py", "NOT_COMPARED")):
    blob = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
                          capture_output=True).stdout.decode("utf-8")
    n = blob.count(token)
    ok = (n == 0) if rev == BASE else (n >= 1)
    print("%s %s %s at %s count=%d (want %s)" % (
        "PASS" if ok else "FAIL", token, path, rev[:8], n,
        "0" if rev == BASE else ">=1"))
    if not ok:
        fails.append("%s count at %s" % (token, rev[:8]))

print("\n== entry sizes (raw / non-blank lines)")
cases = [(DATA, "corpus/knowledge/hyprland-gkeep-size-request-r44.md", "landed"),
         (None, os.path.join(SEAT, "variants/min.md"), "MIN"),
         (None, os.path.join(SEAT, "variants/minfalse.md"), "MINFALSE"),
         (None, os.path.join(SEAT, "variants/wide.md"), "WIDE"),
         (None, os.path.join(SEAT, "variants/wide2.md"), "WIDE2")]
for rev, path, name in cases:
    if rev:
        text = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
                              capture_output=True).stdout.decode("utf-8")
    else:
        text = open(path).read()
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    nb = sum(1 for l in lines if l.strip())
    print("%s %s raw=%d non_blank=%d" % ("INFO", name, len(lines), nb))

print("\n== seat variant anchors (this seat's own files, cited line)")
SEAT_ANCHORS = [
    ("variants/wide2.md", 21, "(Hyprland-Window.cpp:1-3000)"),
    ("variants/wide2.md", 22, "(Hyprland-XDGShell.cpp:1-2000)"),
    ("variants/wide2.md", 24, "(gdktoplevel-wayland.c:1-2000)"),
    ("variants/min.md", 21, "report size (Hyprland-Window.cpp:1685-1699)"),
    ("variants/minfalse.md", 21, "stores the size the client chose"),
    ("variants/wide.md", 21, "Locators (whole files)"),
    ("variants/c1-b4pad5.py", 283,
     "_shape = (1 == 2, 3 != 3, 4 < 3, 5 > 6, 1 <= 0)"),
    ("variants/c1-b4pad6.py", 283,
     "_shape = (1 == 2, 3 != 3, 4 < 3, 5 > 6, 1 <= 0, 2 >= 3)"),
]
for rel, n, needle in SEAT_ANCHORS:
    lines = open(os.path.join(SEAT, rel)).read().split("\n")
    got = lines[n - 1] if n <= len(lines) else ""
    ok = needle in got
    print("%s %s:%d %r" % ("PASS" if ok else "FAIL", rel, n, needle[:50]))
    if not ok:
        fails.append("%s:%d %r" % (rel, n, needle))

print("\n== receipt verdict lines the report cites")
CITES = [
    ("receipts/c1-landed-tool.txt",
     "verdict=TARGET_MET rev=e46789213830597348fe96a351ae004d10587385 nonce=doNothingA"),
    ("receipts/c1-b4pad5.txt", "clause=b4 sites=21 killed=16 need=16"),
    ("receipts/c1-b4pad5.txt", "clauses=a:1 b:1 b4:1 b5:1 e:1 g:1 r:0"),
    ("receipts/c1-b4pad5-nA.txt",
     "clauses=a:1 b:1 b4:1 b5:1 e:1 g:1 r:1"),
    ("receipts/c1-b4pad5-nA.txt",
     "verdict=TARGET_MET rev=e46789213830597348fe96a351ae004d10587385 nonce=dn2-pad5-nA"),
    ("receipts/c1-b4pad5-nB.txt", "clauses=a:1 b:1 b4:1 b5:1 e:1 g:1 r:0"),
    ("receipts/c1-b4pad6.txt", "clause=b4 sites=22 killed=16 need=17"),
    ("receipts/c1-b4pad6.txt", "clauses=a:1 b:1 b4:0 b5:1 e:1 g:1 r:1"),
    ("receipts/c1-olddoc.txt",
     "verdict=TARGET_MET rev=e46789213830597348fe96a351ae004d10587385 nonce=dn2-c1-olddoc"),
    ("receipts/c1-docs.txt",
     "verdict=TARGET_MET rev=0f1dc4bdb79a1be915bf9c523f8c987376cf48ed nonce=dn-docs"),
    ("receipts/c2-docs.txt",
     "admitted=1/1 verdict=TARGET_MET rev=0f1dc4bdb79a1be915bf9c523f8c987376cf48ed"),
    ("receipts/c1-toolonly.txt",
     "verdict=TARGET_MET rev=ce5da7d073ee3bf9b423d15e50b15568f26777dd nonce=dn-toolonly"),
    ("receipts/c2-toolonly.txt",
     "admitted=0/1 verdict=TARGET_MISSED rev=ce5da7d073ee3bf9b423d15e50b15568f26777dd"),
    ("receipts/c2-data-baseline.txt",
     "admitted=1/1 verdict=TARGET_MET rev=e46789213830597348fe96a351ae004d10587385"),
    ("receipts/c2-min.txt",
     "admitted=1/1 verdict=TARGET_MET rev=cd9cb46f848396c667ba1579af846570ee3e81ff"),
    ("receipts/c2-minfalse.txt",
     "admitted=1/1 verdict=TARGET_MET rev=399797f40fed750396d2bac8b8f97221d597bbf7"),
    ("receipts/c2-wide.txt",
     "admitted=1/1 verdict=TARGET_MET rev=0f81ce0350f2ab7b167fd0de90d8e93abe2ec4b2"),
    ("receipts/c2-lesson.txt",
     "admitted=1/1 verdict=TARGET_MET rev=44d1f3d3f1af51e24be2f592b11e95a547d2f008"),
    ("receipts/c2-wide2.txt",
     "admitted=1/1 verdict=TARGET_MET rev=27bd17ff84e27a2efb86e1f8f05e572270b8e416"),
]
for rel, needle in CITES:
    text = open(os.path.join(SEAT, rel)).read()
    ok = needle in text
    print("%s %s :: %r" % ("PASS" if ok else "FAIL", rel, needle[:60]))
    if not ok:
        fails.append("%s missing %r" % (rel, needle))

print("\n== lesson-gate-only variant size (landed lesson is 266 lines at DATA)")
gate = open(os.path.join(SEAT, "variants/lesson-gate-only.md")).read().split("\n")
nb = sum(1 for l in gate if l.strip())
print("INFO variants/lesson-gate-only.md raw=%d non_blank=%d sections=%s" % (
    len(gate) - 1, nb, [l for l in gate if l.startswith("## ")]))
if len(gate) - 1 != 29 or nb != 24:
    fails.append("lesson-gate-only size %d/%d" % (len(gate) - 1, nb))

print("\n== predicate sha256 (frozen files this seat read)")
for p in ("quality/counters/c1-r44-geometry-states-v2.py",
          "quality/counters/c2-r44-gkeep-size-request-v2.py"):
    h = hashlib.sha256(open(os.path.join(LANE, p), "rb").read()).hexdigest()
    print("INFO %s %s" % (h, p))

print("\nVERIFY: %s (%d failures)" % ("PASS" if not fails else "FAIL", len(fails)))
raise SystemExit(0 if not fails else 1)
