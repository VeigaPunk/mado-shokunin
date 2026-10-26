#!/usr/bin/env python3
"""Every quoted source line in dead-weight.md: exists at the stated line of the frozen reference and
appears verbatim in the receipt. Exit 0 iff all quotes verify."""
import sys

REF = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/l1-draft/mado-devices.py"
DOC = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/w1/SimpContract/dead-weight.md"
QUOTES = [
    (100, 'WS = " \\t\\r\\n\\v\\f"'),
    (121, "return math.inf if x > 0 else -math.inf"),
    (216, 'if math.isinf(v) or (v != 0.0 and abs(float(m.group(0))) < FLT_MIN):'),
    (245, 'text.split("\\n")'),
    (270, "if lb != -1 and rb != -1 and lb < rb:"),
    (286, "set_device_key(st.device(bracket), field, rhs, st)"),
    (290, "else:"),
    (291, "st.device(bracket)"),
    (301, "cur is False"),
    (328, "if not isinstance(lst, list):"),
    (371, "rep = tuple(kb.get(n) if isinstance(kb.get(n), str) else None for n in NAMES)"),
]
ref = open(REF, encoding="utf-8").read().split("\n")
doc = open(DOC, encoding="utf-8").read()
bad = 0
for line, quote in QUOTES:
    at_line = ref[line - 1]
    ok_line = quote in at_line
    ok_doc = quote in doc
    words = len(quote.split())
    if not ok_line or not ok_doc or words > 25:
        bad += 1
        print("FAIL line=%d words=%d in_ref=%s in_doc=%s quote=%r" % (line, words, ok_line, ok_doc, quote))
    else:
        print("OK   line=%-4d words=%-2d %r" % (line, words, quote))
print("quotes=%d failures=%d" % (len(QUOTES), bad))
sys.exit(1 if bad else 0)
