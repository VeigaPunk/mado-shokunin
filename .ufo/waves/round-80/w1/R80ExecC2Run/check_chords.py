#!/usr/bin/env python3
"""R80ExecC2Run independent checker for the round-80 chord-grammar row.

Parses chords.txt (real reply of `omarchy menu keybindings --print | cut -c1-35`)
against the declaration grammar (claims-declaration-r80.md, C2):

    chord := MOD ( " + " MOD ){0,3} " + " key   (MOD in SUPER/SHIFT/CTRL/ALT, distinct)
    bare  := key

Strict reading: `key` is one whitespace-free token. Lines that parse as a chord or
bare key but carry a multi-word key are classified "soft" (the frozen counter's
chord_shape matcher accepts them: rpartition at the last " + ", tail needs no '+'
and no leading/trailing space); lines that violate the grammar outright are "hard".
"""
import json
from collections import Counter
from pathlib import Path

SEAT = Path(__file__).resolve().parent
MODS = {"SUPER", "SHIFT", "CTRL", "ALT"}

lines = (SEAT / "chords.txt").read_text(encoding="utf-8").splitlines()

chords = []   # (n, mods tuple, key) grammar-valid chords (incl. soft multi-word keys)
bare = []     # (n, key) bare-key lines (incl. soft multi-word keys)
soft = []     # (n, text, reason) parses, but key is not one whitespace-free token
hard = []     # (n, text, reason) grammar violation
mod_tuples = Counter()
bare_forms = Counter()
max_len = 0
arrows = []

for n, raw in enumerate(lines, 1):
    max_len = max(max_len, len(raw))
    if "→" in raw:
        arrows.append((n, raw))
    line = raw.rstrip()
    if not line.strip():
        hard.append((n, raw, "empty/blank line"))
        continue
    if " + " in line:
        head, _, tail = line.rpartition(" + ")
        mods = head.split(" ")
        bad = [w for w in mods if w not in MODS]
        if not 1 <= len(mods) <= 4:
            hard.append((n, raw, "%d modifier words (grammar allows 1-4)" % len(mods)))
        elif bad:
            hard.append((n, raw, "word(s) outside SUPER/SHIFT/CTRL/ALT: " + " ".join(bad)))
        elif len(set(mods)) != len(mods):
            hard.append((n, raw, "repeated modifier word"))
        elif not tail or "+" in tail or tail != tail.strip():
            hard.append((n, raw, "bad key tail (empty, contains '+', or padded)"))
        else:
            chords.append((n, tuple(mods), tail))
            mod_tuples[tuple(mods)] += 1
            if " " in tail:
                soft.append((n, raw, "chord key is %d tokens: %r" % (len(tail.split()), tail)))
        continue
    if "+" in line:
        hard.append((n, raw, "stray '+' outside a ' + ' separator"))
        continue
    key = line.strip()
    bare.append((n, key))
    bare_forms[key] += 1
    if " " in key:
        soft.append((n, raw, "bare key is %d tokens: %r" % (len(key.split()), key)))

report = {
    "total_lines": len(lines),
    "chord_lines": len(chords),
    "bare_lines": len(bare),
    "modifier_tuples": {" + ".join(k) + " + <key>": v for k, v in sorted(mod_tuples.items())},
    "hard_failures": [{"line": n, "text": t.rstrip(), "reason": r} for n, t, r in hard],
    "soft_multiword_key_lines": [{"line": n, "text": t.rstrip(), "reason": r} for n, t, r in soft],
    "arrow_lines": [{"line": n, "text": t.rstrip()} for n, t in arrows],
    "distinct_bare_key_forms": dict(sorted(bare_forms.items())),
    "longest_line_chars": max_len,
    "min_chords_assumption": {"min_chords": 100, "observed_chord_lines": len(chords),
                              "holds": len(chords) >= 100},
    "min_lines_assumption": {"min_lines": 100, "observed_lines": len(lines),
                             "holds": len(lines) >= 100},
}
print(json.dumps(report, indent=2, ensure_ascii=False))
