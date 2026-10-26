#!/usr/bin/env python3
"""Supplementary probe: does clause d's documented rule "a new id's receipt must be
one of PINS" bind per id? Build a fixture commit in a scratch clone that adds a SIXTH
cited id gated on an unpinned, fixture-invented receipt under fetch/, leaving the five
real pins cited by the five real ids. If the frozen counter admits it, the documented
per-id rule is not enforced.

Writes only inside the clone directory (passed as argv[1]); the lane is read-only.
"""
import hashlib
import os
import re
import subprocess
import sys

D = sys.argv[1]
REV = "e46789213830597348fe96a351ae004d10587385"
ENTRY = "corpus/knowledge/hyprland-gkeep-size-request-r44.md"


def sh(*a, **kw):
    p = subprocess.run(a, cwd=kw.get("cwd", D), capture_output=True)
    if p.returncode != 0 and not kw.get("ok"):
        raise SystemExit("FAILED %s\n%s" % (a, p.stderr.decode()))
    return p


def read(p):
    with open(os.path.join(D, p), "rb") as f:
        return f.read().decode("utf-8")


def write(p, s):
    full = os.path.join(D, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(s)


assert sh("git", "rev-parse", "--show-toplevel").stdout.decode().strip() == D, "toplevel mismatch"
sh("git", "checkout", "-q", "--detach", REV)

RECEIPT = ".ufo/waves/round-44/fetch/unpinned-receipt.txt"
body = (
    "synthetic round-44 fixture receipt (invented for a predicate probe)\n"
    "a configure width of 0 leaves the choice to the client\n"
    "the ack serial orders the configure it answers\n"
    "no upstream project publishes this file\n"
    "this text exists to clear the counter's minimum receipt size of 256 bytes\n"
    "and to say nothing about any compositor, toolkit or client under study\n"
    "the fixture is deleted with the scratch directory that holds it\n"
)
assert len(body.encode()) >= 256
write(RECEIPT, body)
sha = hashlib.sha256(body.encode()).hexdigest()
quote = "a configure width of 0 leaves the choice to the client"
assert len(quote.split()) == 11 and body.count(quote) == 1

# lesson: one GATE line for the sixth id
lesson = read("corpus/lessons/round-44.md")
gate_line = 'GATE S302 receipt=%s sha256=%s quote="%s"\n' % (RECEIPT, sha, quote)
assert "GATE S302" not in lesson
lines = lesson.split("\n")
i = next(n for n, l in enumerate(lines) if l.startswith("GATE S301 "))
lines.insert(i + 1, gate_line.rstrip("\n"))
write("corpus/lessons/round-44.md", "\n".join(lines))

# registry: one 11-cell row for S302, location = a URL with a / and a .
src = read("corpus/SOURCES.md")
row = ("| S302 | synthetic unpinned receipt - the zero-width rule - "
       "https://example.com/spec/unpinned-receipt.txt | spec | A | "
       "A file that exists only in this fixture | "
       "unpinned-receipt.txt:1-2 (receipt .ufo/waves/round-44/fetch/unpinned-receipt.txt) | "
       "a zero configure width leaves the choice to the client | mined | 2026-10-26 | "
       "on-release | %s |" % ENTRY)
assert "| S302 |" not in src
sl = src.split("\n")
j = next(n for n, l in enumerate(sl) if l.startswith("| S301 |"))
sl.insert(j + 1, row)
write("corpus/SOURCES.md", "\n".join(sl))

# entry: one source: line inside the first 20 raw lines, one OBS line with quote+locator
entry = read(ENTRY)
el = entry.split("\n")
k = next(n for n, l in enumerate(el) if l.startswith("source: S301 "))
el.insert(k + 1, "source: S302 - fixture-only synthetic receipt - the zero-width sentence")
k2 = next(n for n, l in enumerate(el) if l.startswith("recheck:"))
el.insert(k2, "**OBS** S302 - synthetic half: `%s` (unpinned-receipt.txt:2)." % quote)
write(ENTRY, "\n".join(el))

sh("git", "add", "-A")
sh("git", "-c", "user.name=RerunC2Data", "-c", "user.email=rerunc2data@fixture.invalid",
   "commit", "-q", "-m", "fixture: sixth cited id on an unpinned receipt")
new = sh("git", "rev-parse", "HEAD").stdout.decode().strip()
print("fixture_rev=%s receipt_sha256=%s" % (new, sha))
