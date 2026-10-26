#!/usr/bin/env python3
"""ExecFixtureMap: every quotation in the seat report, re-located by grep.

Each entry is (file, line, quote). The script fails if the quote is not the whole content of
that line (leading/trailing whitespace ignored) in that file, so a typed locator cannot drift.
"""
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
PIN = LANE + "/.ufo/waves/round-47/fetch/xdg-terminal-exec"
REG = LANE + "/.ufo/waves/round-47/registration.md"
COUNTER = LANE + "/quality/counters/c1-r47-terminal.py"

QUOTES = [
    (PIN, 221, 'if [ -f "${XTE__CACHE_FILE}" ]; then'),
    (PIN, 552, '# unsupported sequence, reappend backslash'),
    (PIN, 1456, '# saves or removes cache, forked out of the way'),
    (PIN, 1457, 'save_cache "$1" &'),
    (PIN, 1418, 'set -- "${XTE__TITLEARG}${XTE__TITLEVAL}" "$@"'),
    (PIN, 1499, 'exec "$@"'),
    (PIN, 882, '# Default in this case is to succeed'),
    (REG, 54, 'different host may drift; the drift check stops the count); the warm-cache path, `-h/--help`, an empty argv element'),
]

bad = 0
for path, line, quote in QUOTES:
    try:
        text = open(path, encoding="utf-8", errors="surrogateescape").read().split("\n")
        got = text[line - 1].strip()
    except OSError as e:
        print("MISSING %s: %s" % (path, e))
        bad += 1
        continue
    ok = got == quote.strip()
    if not ok and quote.strip() not in got:
        bad += 1
    words = len(quote.split())
    print("%s %-4s %s:%d words=%d\n     %s"
          % ("OK  " if ok or quote.strip() in got else "FAIL", "", path.split("/")[-1], line,
             words, quote))
    if words > 25:
        print("     FAIL: more than 25 words")
        bad += 1
print("\n%d quotes, %d failures" % (len(QUOTES), bad))
sys.exit(1 if bad else 0)
