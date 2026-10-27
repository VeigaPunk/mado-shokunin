#!/usr/bin/env python3
"""ScoutCensus r48/w2: per-row Gate quote check for gate-rows.md.

For every admitted row S340-S350 in the Gate draft: extract the backticked quote and its
parenthesised locator, resolve the locator against the committed pin/receipt bytes, require the
quote to be a verbatim substring of that exact line, and count words (round-47 rule: <= 25).
Reports rows with no Gate line. Read-only; writes one report to stdout.
"""
import re, sys, pathlib

W = pathlib.Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48")
GATE = W / "l1-draft/gate-rows.md"
RECEIPT = W / "receipts/xkbcli-compile-keymap-r48.txt"
ADMITTED = ["S%d" % n for n in range(340, 351)]

lines = GATE.read_text().split("\n")
pat = re.compile(r"\*\*(S\d+) admit\*\*.*?quote `([^`]+)` \(`([^`:]+):(\d+)`")
found = {}
for ln in lines:
    m = pat.search(ln)
    if m:
        found[m.group(1)] = (m.group(2), "%s:%s" % (m.group(3), m.group(4)))

ok = fail = 0
out = []
for rid in ADMITTED:
    if rid not in found:
        out.append("%s MISSING gate line (no quote, no locator)" % rid)
        fail += 1
        continue
    quote, loc = found[rid]
    if loc.startswith("receipt:"):
        path_s, lineno = str(RECEIPT), int(loc.split(":", 1)[1])
    else:
        p, n = loc.rsplit(":", 1)
        path_s, lineno = str(W / p), int(n)
    target = pathlib.Path(path_s)
    if not target.is_file():
        out.append("%s FAIL pin missing %s" % (rid, path_s))
        fail += 1
        continue
    body = target.read_text(errors="replace").split("\n")
    if lineno < 1 or lineno > len(body):
        out.append("%s FAIL locator out of range %s" % (rid, loc))
        fail += 1
        continue
    inline = body[lineno - 1]
    words = len(quote.split())
    hits = sum(1 for b in body if quote in b)
    verdict = "PASS" if quote in inline and words <= 25 else "FAIL"
    if verdict == "PASS":
        ok += 1
    else:
        fail += 1
    out.append("%s %s locator=%s line_has_quote=%s quote_occurrences=%d words=%d quote=%r"
               % (rid, verdict, loc, quote in inline, hits, words, quote))
out.append("GATE_QUOTES: checked=%d passed=%d failed=%d missing=%d"
           % (len(ADMITTED), ok, fail, sum(1 for r in ADMITTED if r not in found)))
sys.stdout.write("\n".join(out) + "\n")
sys.exit(0 if fail == 0 else 1)
