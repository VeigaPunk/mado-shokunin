#!/usr/bin/env python3
"""ScrLessonGate: run PRED-C2-r45 clause d over the draft lesson, with the frozen
counter's own helpers and PINS table. Reads the draft + lane fetch/; read-only."""
import hashlib
import importlib.util
import os
import re

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FETCH = ".ufo/waves/round-45/fetch/"
DRAFT = os.path.join(LANE, ".ufo/waves/round-45/w1/ScrLessonGate/round-45.md")
spec = importlib.util.spec_from_file_location(
    "c2r45", os.path.join(LANE, "quality/counters/c2-r45-monitor-entry.py"))
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)

text = open(DRAFT).read()
glines = ctr.unfenced("\n".join(ctr.section(text, "## Gate")))
gates = {}
for line in glines:
    m = ctr.GATE_RE.match(line.rstrip("\n"))
    if m:
        gates.setdefault(m.group(1), []).append(m.groups()[1:])
    elif re.match(r"^\s+GATE S\d", line):
        print("INDENTED GATE LINE:", line)
in_gate = set(glines)
outside = [l for l in ctr.unfenced(text)
           if re.match(r"^GATE S\d", l) and l not in in_gate]
print("gate lines: ids=%d outside=%d" % (len(gates), len(outside)))
ok = not outside
seen_paths, seen_sha, seen_quote = set(), set(), set()
for i in sorted(gates):
    gl = gates[i]
    good = False
    if len(gl) == 1:
        path, digest, quote = gl[0]
        blob = (open(os.path.join(LANE, path), "rb").read()
                if path.startswith(FETCH) else None)
        pin_ok = (ctr.PINS.get(os.path.basename(path)) in (None, digest)
                  and (os.path.basename(path) not in ctr.PINS
                       or path == FETCH + os.path.basename(path)))
        nq = re.sub(r"\s+", " ", quote)
        good = bool(blob is not None and len(blob) >= ctr.MIN_RECEIPT and pin_ok
                    and hashlib.sha256(blob).hexdigest() == digest
                    and 3 <= len(quote.split()) <= 25
                    and path not in seen_paths and digest not in seen_sha
                    and nq not in seen_quote
                    and ctr.quote_at(blob, nq) is not None
                    and len(ctr.occurrences(blob, nq)) == 1
                    and ctr.quote_in_code(blob, nq, path))
        if good:
            seen_paths.add(path)
            seen_sha.add(digest)
            seen_quote.add(nq)
            print("  %s OK line=%d path=%s" % (i, ctr.quote_at(blob, nq),
                                               os.path.basename(path)))
    ok &= good
    if not good:
        print("  %s FAIL gates=%d %r" % (i, len(gl), gl[:1]))
missing = [i for i in ("S%03d" % (302 + k) for k in range(9)) if i not in gates]
print("missing ids:", missing)
print("CLAUSE_D_OK=%d" % int(ok and not missing))

# the draft's headings, so the L1 can splice it unchanged
print("headings:", [l for l in text.splitlines() if l.startswith("## ")])
