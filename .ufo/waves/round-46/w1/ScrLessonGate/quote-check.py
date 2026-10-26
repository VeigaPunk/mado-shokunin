#!/usr/bin/env python3
"""Re-check every GATE quote of corpus/lessons/round-46.md against the round-46 pins.

Read-only: reads .ufo/waves/round-46/fetch/ (the frozen pins) and the Gate lines given below (the exact lines the
lesson draft carries). Reproduces PRED-C2-r46 clause d's quote test: whitespace-collapsed, word-bounded, exactly one
occurrence, also inside the comment-stripped text; prints the computed locator (start line of the quote in the
collapsed receipt, the same rule as the counter's quote_at).
"""
import hashlib
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FETCH = os.path.join(LANE, ".ufo/waves/round-46/fetch")
QUOTES = [
    ("S316", "Hyprland-InputManager.cpp", 'const auto LAYOUT = Config::mgr()->getDeviceString(devname, "kb_layout", "input:kb_layout");'),
    ("S317", "Hyprland-ConfigManager.cpp", "if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())"),
    ("S318", "Hyprland-ConfigValues.cpp", 'MS<String>("input:kb_layout", "Appropriate XKB keymap parameter", "us",'),
    ("S319", "Hyprland-IKeyboard.cpp", 'm_currentRules.layout = "us";'),
    ("S320", "Hyprland-HyprCtl.cpp", '"defaultSpeed": {:.5f}, "scrollFactor": {:.2f}'),
    ("S321", "Hyprland-MiscFunctions.cpp", "case ',': return '-';"),
    ("S322", "Hyprland-VirtualKeyboard.cpp", "m_keymapOverridden = true;"),
    ("S323", "Hyprland-protocols-VirtualKeyboard.cpp", 'std::string name = "hl-virtual-keyboard";'),
    ("S324", "hyprlang-config.cpp", "special category's first value must be the key."),
    ("S325", "wiki-Keywords.md", "It's worth noting that ONLY values explicitly changed will be overwritten."),
]


def collapse(text):
    out, lines, prev = [], [], True
    for ln, line in enumerate(text.split("\n"), 1):
        for ch in line + "\n":
            if ch.isspace():
                if not prev:
                    out.append(" ")
                    lines.append(ln)
                    prev = True
            else:
                out.append(ch)
                lines.append(ln)
                prev = False
    return "".join(out), lines


def strip_comments(text, name):
    if name.endswith((".cpp", ".hpp", ".h", ".cc")):
        text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
        return re.sub(r"//[^\n]*", " ", text)
    if name.endswith((".py", ".conf")):
        return re.sub(r"#[^\n]*", " ", text)
    return text


def occurrences(text, nq):
    isw = lambda c: c.isalnum() or c == "_"
    out, start = [], 0
    while True:
        k = text.find(nq, start)
        if k < 0:
            return out
        before = text[k - 1] if k > 0 else " "
        after = text[k + len(nq)] if k + len(nq) < len(text) else " "
        if not (isw(nq[0]) and isw(before)) and not (isw(nq[-1]) and isw(after)):
            out.append(k)
        start = k + 1


bad = 0
seen_q = {}
for sid, name, quote in QUOTES:
    path = os.path.join(FETCH, name)
    blob = open(path, "rb").read()
    text = blob.decode("utf-8", "replace")
    nq = re.sub(r"\s+", " ", quote)
    coll, lines = collapse(text)
    occ = occurrences(coll, nq)
    code = re.sub(r"\s+", " ", strip_comments(text, name))
    words = len(quote.split())
    at = lines[occ[0]] if occ else None
    ok = (len(occ) == 1 and nq in code and 3 <= words <= 25 and nq not in seen_q)
    seen_q[nq] = sid
    bad += 0 if ok else 1
    print("%s %-36s sha256=%s bytes=%6d loc=%s:%s words=%2d occ=%d code=%d uniq=%d %s"
          % (sid, name, hashlib.sha256(blob).hexdigest(), len(blob), name, at, words,
             len(occ), int(nq in code), int(ok), "OK" if ok else "FAIL"))
print("QUOTE_CHECK: checked=%d failed=%d" % (len(QUOTES), bad))
sys.exit(0 if bad == 0 else 1)
