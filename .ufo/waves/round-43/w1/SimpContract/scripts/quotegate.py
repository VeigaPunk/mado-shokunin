"""Quote gate: every quoted fragment in dead-weight.md is grepped from the frozen sources,
normalised for line wrapping, and its word count is checked (<= 25)."""
import re, sys
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SRC = {
    "counter": LANE + "/quality/counters/c1-r42-geometry.py",
    "ref": LANE + "/.ufo/waves/round-42/c1/ctl-ref-tool.py.txt",
    "controls": LANE + "/.ufo/waves/round-42/ctl/run-c1-controls.py",
    "receipt-c1": LANE + "/.ufo/waves/round-43/receipts/ctl-c1.txt",
}
TEXT = {}
for k, p in SRC.items():
    raw = open(p, encoding="utf-8").read()
    TEXT[k] = raw

def norm(s):
    return re.sub(r"\s+", " ", s)

CLAIMS = [
    ("counter", "REGEX fully matches 1-200 characters of", 34),
    ("counter", "`--clients -` reads standard input, at most 1048577 bytes;", 20),
    ("counter", "DIFFER (differ>0; exit 1) | NO_MATCHING_CLIENT (matched=0; exit 3) | OK (exit 0), tested in that order.", 55),
    ("counter", "(not booleans, not floats)", 44),
    ("counter", "The effect is the first", 29),
    ("counter", "first token of field 0", 30),
    ("counter", "(two-token form only, any order)", 17),
    ("ref", "in any order", 17),
    ("counter", "decoded as UTF-8 with errors replaced", 26),
    ("counter", "the capture being REGEX", 34),
    ("counter", "then the rules files in argument order", 22),
    ("counter", 'The body is split on ","', 29),
    ("counter", "A duplicate JSON key keeps its last value.", 48),
    ("counter", "A PATH that is missing, unreadable", 19),
    ("counter", "field 0 has exactly two argument tokens", 31),
    ("counter", "No bwrap -> SETUP, exit 2.", None),
    ("counter", "Cost bound", None),
    ("counter", "restated here, the code below being the same sentence", 9),
    ("counter", "A client with at least one matching size rule", 46),
    ("counter", "a list of exactly two JSON integers", 43),
    ("counter", "A RULE LINE fully matches", 27),
    ("ref", "It reads files and standard input only; it starts no process and opens no socket.", 14),
    ("ref", "DIFFER is a report, not a fault: a user may have resized the window", 57),
    ("ref", "REGEX is 1-200 characters of", 34),
    ("ref", "(not booleans, not floats)", 45),
    ("ref", "tested in that order.", 57),
    ("ref", "is read at most 1048577 bytes)", 22),
    ("controls", "M38 `{1,200}` -> `{0,200}`: MATCH_FIELD's `(.+)` already requires a non-empty regex.", 72),
    ("controls", "the test was dead; the contract sentence and the code were deleted instead.", 71),
    ("controls", "M05-stdin-short", None),
    ("receipt-c1", "equivalent_mutants_excluded=M03-read-short,M20-hash-allowed,M38-regex-empty", 1),
]

bad = 0
for key, quote, line in CLAIMS:
    nq = norm(quote)
    ok = nq in norm(TEXT[key])
    words = len(quote.split())
    wok = words <= 25
    if not ok or not wok:
        bad += 1
    print("%-9s line=%-4s words=%-2d present=%d len_ok=%d  %s" % (
        key, line if line else "-", words, ok, wok, quote[:80]))
print("QUOTE_GATE claims=%d failed=%d" % (len(CLAIMS), bad))
sys.exit(1 if bad else 0)
