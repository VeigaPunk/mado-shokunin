#!/usr/bin/env python3
"""Source-truth audit of the fixture propositions: what the located span actually says.

Mechanical part only: locate the quote, print the full located span and the operator tokens
that fall *outside* the quoted span but inside the same statement. The truth verdicts in the
report are read off these printed bytes; nothing here claims automated entailment.
"""
import importlib.util
import os
import re

SCR = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("c2fix", os.path.join(SCR, "c2_fixture_check.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

ENTRY = os.path.join(SCR, "fixture/entry/hyprland-dispatcher-argument-split-r52-fixture.md")
PINS = os.path.join(SCR, "fixture/pins")
OPS = re.compile(r"\b(not|never|only|unless|no|without)\b|n't|(?<![=!<>])!(?!=)")


def span(pin, first, last):
    lines = open(os.path.join(PINS, pin), encoding="utf-8", errors="replace").read().splitlines()
    return lines[first - 1:min(last, len(lines))]


def main():
    props, _ = m.prop_rows(open(ENTRY, encoding="utf-8").read())
    for i, p in enumerate(props, 1):
        loc = p["pin"].strip("`* ")
        mm = m.LOC_RE.match(loc)
        pin, first = mm.group("pin"), int(mm.group("first"))
        last = int(mm.group("last") or first)
        q = m.QUOTE_RE.findall(p["quote"])[0]
        lines = span(pin, first, last)
        text = "\n".join(lines)
        idx = text.find(q)
        before = text[:idx]
        print("=" * 78)
        print("P%d  %s" % (i, p["proposition"]))
        print("locator   : %s" % loc)
        print("quote     : %r  (%d words)" % (q, len(m.words(q))))
        print("verbatim  : %s" % ("yes" if m.collapse(q) in m.collapse(text) else "NO"))
        print("span bytes:")
        for i, ln in enumerate(lines, start=first):
            mark = "<-- quote line" if q in ln else ""
            print("  %d: %s %s" % (i, ln, mark))
        print("left of quote inside the same located text: %r" % before[-80:])
        ops = sorted(set(x.group(0) for x in OPS.finditer(before)))
        print("operator tokens before the quote (outside it): %s" % (ops or "none"))
        print()
    print("=" * 78)
    print("truthful variant (same shape, propositions the source states):")
    inc = os.path.join(SCR, "fixture/entry/hyprland-dispatcher-argument-split-r52-truthful.md")
    props, _ = m.prop_rows(open(inc, encoding="utf-8").read())
    for i, p in enumerate(props, 1):
        q = m.QUOTE_RE.findall(p["quote"])[0]
        print("  P%d %r words=%d" % (i, q, len(m.words(q))))


if __name__ == "__main__":
    main()
