#!/usr/bin/env python3
"""Verify every locator/quote pair claimed in dead-weight.md against the frozen files."""
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
TOOL = LANE + "/.ufo/waves/round-45/l1-draft/mado-monitors.py"
CTR = LANE + "/quality/counters/c2-r45-monitor-entry.py"
DOC = LANE + "/.ufo/waves/round-45/w1/SimpContract/dead-weight.md"
doc = open(DOC, encoding="utf-8").read()
DOC_FLAT = re.sub(r"\s+", " ", doc)

PAIRS = [
    (TOOL, 324, "math.isfinite(x) and"),
    (TOOL, 332, "z > 0 and whole(w / z)"),
    (TOOL, 336, "cand != 0 and"),
    (TOOL, 393, "isinstance(mo, str) and len(ids) >= 1"),
    (TOOL, 392, 'str_or_empty(m.get("name")) == rule["mirror"]'),
    (TOOL, 346, 'name, desc = str_or_empty(mon.get("name"))'),
    (TOOL, 296, 'counts["v2"] += 1'),
    (TOOL, 297, "continue"),
    (TOOL, 100, "monitorv2(?:[ \\t={]|$)"),
    (TOOL, 194, 'toks[0] == "modeline"'),
    (TOOL, 384, "w > 0 and h > 0"),
    (TOOL, 220, 'rule["scale"] = 1.0 if s < 0.25 else s'),
    (TOOL, 381, "is_int(w) and is_int(h)"),
    (CTR, 318, "def host_census(new_ids, reg_rev, gates, receipts_raw, lines):"),
    (CTR, 579, "h_ok, census_lines = host_census(new_ids, reg_rev, gates, receipts_raw, lines)"),
    (CTR, 398, r'(?<![\w.-])%s:(\d+)(?:-(\d+))?(?!\d)'),
    (CTR, 322, "gl and gl[0] is not None and len(gl) == 1:"),
    (CTR, 328, r"([0-9]+(?:\.[0-9]+)?);"),
    (CTR, 335, 'after = mon[mon.index("std::round(m_scale * %s.0)" % k[0]):]'),
    (CTR, 333, "if len(r) != 1 or len(t) != 1"),
    (CTR, 620, "if rows and len(rows[0]) == 11:"),
    (CTR, 627, 'cl["j"] = int(raw is not None and surfaces_ok'),
    (CTR, 326, "if not all(n in byname for n in need):"),
]
fails = 0
for path, n, frag in PAIRS:
    line = open(path, encoding="utf-8").read().split("\n")[n - 1]
    ok_file = frag in line
    ok_doc = frag in doc
    words = len(frag.split())
    print("%-3s %-42s :%-4d words=%2d in_file=%s in_doc=%s"
          % ("OK" if ok_file and ok_doc and words <= 25 else "FAIL",
             path.rsplit("/", 1)[-1], n, words, ok_file, ok_doc))
    fails += 0 if (ok_file and ok_doc and words <= 25) else 1

# the docstring sentences quoted in the report
for frag in ["stderr empty on exit 0/1/3/4/5",
             "A live value that is missing or of the wrong JSON type",
             "none found means the scale is not compared",
             "a first token `modeline` (any case) is modeline",
             "52", ]:
    pass
ds_lines = open(TOOL, encoding="utf-8").read().split("\n")
for frag in ["stderr empty on exit 0/1/3/4/5", "A live value that is missing or of the wrong JSON type",
             "none found means the scale is not compared", "first rule with an empty selector"]:
    hits = [i + 1 for i, l in enumerate(ds_lines[:95]) if frag in l]
    ok = bool(hits) and frag in DOC_FLAT and len(frag.split()) <= 25
    print("%-3s docstring %-50r lines=%s" % ("OK" if ok else "FAIL", frag, hits))
    fails += 0 if ok else 1
print("FAILURES=%d" % fails)
sys.exit(1 if fails else 0)
