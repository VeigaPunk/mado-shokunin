#!/usr/bin/env python3
"""Probe the committed C2 acceptance function with a negator-elided verbatim span.

No fixture logic of our own: imports `bind_row` / `quote_candidates` / `words`
straight out of quality/counters/c2-r51-dispatch-entry.py at base 85d57a8
(read-only) and calls them on real pin bytes copied from .ufo/waves/round-51/fetch/.
"""
import importlib.util
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality/counters/c2-r51-dispatch-entry.py")
SCR = os.path.dirname(os.path.abspath(__file__))

spec = importlib.util.spec_from_file_location("c2_r51", COUNTER)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

PINS = {
    "wiki-Dispatchers.md": os.path.join(SCR, "fixture/pins/wiki-Dispatchers.md"),
    "Hyprland-KeybindManager.cpp": os.path.join(SCR, "fixture/pins/Hyprland-KeybindManager.cpp"),
}


def loader(name):
    with open(PINS[name], "rb") as fh:
        return fh.read()


CASES = [
    # (rowid, source line as it would be written in an entry, claim the quote is offered for)
    (
        "S380",
        "source: S380 - dispatcher table page - `invoke any action immediately`(wiki-Dispatchers.md:15)",
        "Q1: a dispatcher invokes its action immediately when it is called",
    ),
    (
        "S381",
        "source: S381 - submap reset gate - `k->submap.reset.empty()`(Hyprland-KeybindManager.cpp:820)",
        "Q2: a bind's reset submap is applied when the reset field is empty",
    ),
]
MAN = {
    "wiki-Dispatchers.md": {"row": "S380", "file": "content/Configuring/Dispatchers.md"},
    "Hyprland-KeybindManager.cpp": {"row": "S381", "file": "src/managers/KeybindManager.cpp"},
}
AT_REV = set(MAN)

for rowid, line, claim in CASES:
    bound, why = mod.bind_row(rowid, [line], MAN, AT_REV, loader)
    print("ROW  %s" % rowid)
    print("CLAIM %s" % claim)
    print("LINE  %s" % line)
    if bound is None:
        print("BIND  REJECT reason=%s" % why)
    else:
        pin, first, last, quote, _ = bound
        print("BIND  ACCEPT pin=%s:%d-%d quote=%r quote_words=%d"
              % (pin, first, last, quote, len(mod.words(quote))))
    print()

# Left context the predicate never looks at: what precedes the accepted span.
def left_context(path, lineno, quote, width=46):
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read().splitlines()[lineno - 1]
    idx = text.find(quote)
    return text[max(0, idx - width):idx]


print("LEFT-CONTEXT OF EACH ACCEPTED SPAN (source bytes, not scored by bind_row):")
for path, lineno, quote in (
    (PINS["wiki-Dispatchers.md"], 15, "invoke any action immediately"),
    (PINS["Hyprland-KeybindManager.cpp"], 820, "k->submap.reset.empty()"),
):
    with open(path, encoding="utf-8", errors="replace") as fh:
        full = fh.read().splitlines()[lineno - 1]
    print("  %s:%d" % (os.path.basename(path), lineno))
    print("    full : %s" % full.strip())
    print("    before span: %r" % left_context(path, lineno, quote))
