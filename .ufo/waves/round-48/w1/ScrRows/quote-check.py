#!/usr/bin/env python3
"""Quote check for the S340-S347 Gate lines (round 48 w1, seat ScrRows).

For every (receipt, quote) pair: collapse runs of whitespace to one space per line
(the round-46 locator rule), require exactly one word-bounded occurrence, and report
the start line of the first occurrence. Locators are computed here, never typed.
Writes quote-check.txt next to this script; exit 1 if any check fails.
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
QUOTES = [
    ("S340", "fetch/host-rules-evdev", "* * = pc+%l%(v)"),
    ("S341", "fetch/xkbc-symbols-br", 'xkb_symbols "nativo" {'),
    ("S342", "fetch/libxkbcommon-context.c", "XDG_CONFIG_HOME fallback is $HOME/.config/"),
    ("S343", "fetch/libxkbcommon-rules.c", 'Unrecognized RMLVO option'),
    ("S344", "fetch/libxkbcommon-include.c", "Couldn't process include statement for '%s(%s)'"),
    ("S345", "fetch/libxkbcommon-messages-codes.h", "XKB_ERROR_CANNOT_RESOLVE_RMLVO = 595,"),
    ("S346", "fetch/host-xkbcli-compile-keymap.1",
     "If an include path is given, the default include path list is not used."),
    ("S347", "fetch/host-xkbcommon.h", "A comma separated list of variants, one per layout"),
]

lines_out = []
checked = failed = 0
for row, rel, quote in QUOTES:
    checked += 1
    path = HERE / rel
    text = path.read_text(encoding="utf-8", errors="replace")
    hits = []
    for idx, line in enumerate(text.splitlines(), 1):
        flat = " ".join(line.split())
        if quote in flat:
            # word-bounded: the character before/after the match is not a name char
            for m in re.finditer(re.escape(quote), flat):
                before = flat[m.start() - 1] if m.start() else " "
                after = flat[m.end()] if m.end() < len(flat) else " "
                if not (before.isalnum() or before == "_") and not (after.isalnum() or after == "_"):
                    hits.append(idx)
    words = len(quote.split())
    ok = len(hits) == 1 and words <= 25
    if not ok:
        failed += 1
    lines_out.append(
        f"{row} {'PASS' if ok else 'FAIL'} receipt={rel} words={words} "
        f"hits={len(hits)} locator={rel}:{hits[0] if hits else 'none'}"
    )

lines_out.append(f"QUOTE_CHECK: checked={checked} failed={failed}")
report = "\n".join(lines_out) + "\n"
(HERE / "quote-check.txt").write_text(report, encoding="utf-8")
sys.stdout.write(report)
sys.exit(1 if failed else 0)
