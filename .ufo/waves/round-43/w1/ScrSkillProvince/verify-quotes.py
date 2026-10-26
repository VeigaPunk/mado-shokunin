#!/usr/bin/env python3
"""ScrSkillProvince quote verifier (round 43, w1).

Every quote a draft lifts from a source must be (a) <= 25 words, (b) present in the
receipt the draft cites, at the locator the draft names, and (c) actually used by the
draft.  Reads only files under this seat directory; writes nothing.

    python3 -I .ufo/waves/round-43/w1/ScrSkillProvince/verify-quotes.py
"""
import os
import re
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
SRC_RECEIPT = os.path.join(SEAT, "receipts", "source-quotes.txt")
RUN_RECEIPT = os.path.join(SEAT, "receipts", "geometry-host-run.txt")
DRAFTS = [os.path.join(SEAT, n) for n in
          ("skill-rows.md", "province-row.md", "readme-row.md")]

# (quote, receipt-file, receipt-line); every entry must exist at its locator,
# and every entry in USED must also appear in a draft.
SOURCE_QUOTES = [
    ('"size": [{}, {}]', "Hyprland-HyprCtl.cpp", 395),
    ("w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL)", "Hyprland-HyprCtl.cpp", 427),
    ("m_realSize->goal()", "Hyprland-GeometricMovableAnimated.cpp", 19),
    ("m_realSize->value()", "Hyprland-GeometricMovableAnimated.cpp", 20),
    ("m_ruleApplicator->static_.size", "Hyprland-DefaultFloatingAlgorithm.cpp", 55),
    ("calculateExpression", "Hyprland-DefaultFloatingAlgorithm.cpp", 56),
    ("static_.size = expr", "Hyprland-WindowRuleApplicator.cpp", 426),
    ("negative:", "Hyprland-RegexMatchEngine.cpp", 7),
    ("re2::RE2::FullMatch", "Hyprland-RegexMatchEngine.cpp", 16),
]

# locators the drafts cite but whose exact bytes they do not quote
LOCATOR_ONLY = [
    ("m_firstMap", "Hyprland-DefaultFloatingAlgorithm.cpp", 49),
    ('registerCommand(SHyprCtlCommand{"clients", true, clientsRequest});',
     "Hyprland-HyprCtl.cpp", 2007),
]

RUN_QUOTES = [
    "MADO_GEOMETRY: rules=1 float_rules=1 other=1 unsupported=0 clients=4 "
    "matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_MATCHING_CLIENT",
    "MADO_GEOM_RULE: n=1 file=1 effect=float arg=on class=^(org.omarchy.gkeep)$",
    "MADO_GEOM_RULE: n=2 file=1 effect=size arg=420x500 class=^(org.omarchy.gkeep)$",
]

LINE_RE = re.compile(r"^([\w.-]+\.cpp):(\d+):(.*)$")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def main():
    checks, failed = [], []

    def check(name, ok):
        checks.append(name)
        if not ok:
            failed.append(name)

    src = {}
    for line in read(SRC_RECEIPT).splitlines():
        m = LINE_RE.match(line)
        if m:
            src[(m.group(1), int(m.group(2)))] = m.group(3)

    drafts = {p: read(p) for p in DRAFTS}
    joined = "\n".join(drafts.values())

    for quote, fname, lineno in SOURCE_QUOTES:
        tag = f"{fname}:{lineno} {quote[:40]!r}"
        check(f"locator-present {tag}", (fname, lineno) in src)
        check(f"quote-at-locator {tag}",
              (fname, lineno) in src and quote in src[(fname, lineno)])
        check(f"quote-used-by-draft {tag}", quote in joined)
        check(f"quote-<=25-words {tag}", len(quote.split()) <= 25)

    for quote, fname, lineno in LOCATOR_ONLY:
        tag = f"locator-only {fname}:{lineno} {quote[:36]!r}"
        check(f"locator-present {tag}", (fname, lineno) in src)
        check(f"quote-at-locator {tag}",
              (fname, lineno) in src and quote in src[(fname, lineno)])

    run = read(RUN_RECEIPT)
    for quote in RUN_QUOTES:
        tag = f"run {quote[:48]!r}"
        check(f"quote-in-run-receipt {tag}", quote in run)
        check(f"quote-used-by-draft {tag}", quote in joined)
        check(f"quote-<=25-words {tag}", len(quote.split()) <= 25)

    # the host-run receipt must carry its own exit code and the tool identity
    check("run-receipt has exit=3", "exit=3" in run)
    check("run-receipt pins the reference sha256",
          "e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99" in run)

    print(f"QUOTES: {len(checks) - len(failed)}/{len(checks)} checks passed")
    for name in failed:
        print(f"FAILED: {name}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
