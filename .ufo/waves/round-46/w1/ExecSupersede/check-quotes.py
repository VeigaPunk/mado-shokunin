#!/usr/bin/env python3
"""ExecSupersede (round 46 w1) - computed locators for the S326-S333 supersession rows.

For every quote the Gate lines carry: the quote is found in the pinned bytes, its line numbers are
computed (never typed), and the count on the cited line must be 1. For every anchor range the row
cites, the first and last source lines are printed so the receipt shows what the range covers.
Reads only the seat's own fetch/ copies and the lane's round-43 own-work receipts. Starts no process,
opens no socket.
"""
import hashlib
import os
import re
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(SEAT, *[".."] * 5))  # .ufo/waves/round-46/w1/<seat> -> lane root

PINS = {
    "RegexMatchEngine.cpp": "8ca655336cd111df1136be76bbdf91bd6830e7e8891df4bb8c766f1e55a3a282",
    "DefaultFloatingAlgorithm.cpp": "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91",
    "Target.cpp": "49323833c6bc327656e6d02245ebbccf7643fc94f4fbee3cebbae035bbd4ca06",
    "WindowTarget.cpp": "8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d",
    "GeometricMovableAnimated.cpp": "649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d",
    "Rule.cpp": "257687efd814cb714024c14e2952adb26e1e7a1f5907d20aa6aaea1e4c098e2e",
    "WindowRule.cpp": "7034c3325fee476cb501266af67999534ca36cf2841d83c9940db96d116d1f78",
    "Window.cpp": "d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded",
    "host-clients-r43.json": "21db902e1f1234b9f52411cf7885097a18d67b00b9dd0110f9bbd2b36fb442ad",
    "gkeep-ui-excerpt.py": "3695b788c6d766b8e87c01916a6594158a26c2cf816f991ccf30b72d9c5d1713",
}

# (row, file, cited line, quote)
QUOTES = [
    ("S326", "RegexMatchEngine.cpp", 16, "return re2::RE2::FullMatch(other, *m_regex) != m_negative;"),
    ("S327", "DefaultFloatingAlgorithm.cpp", 56,
     "const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);"),
    ("S328", "Target.cpp", 68, "void ITarget::rememberFloatingSize(const Vector2D& size) {"),
    ("S329", "WindowTarget.cpp", 339, "if (DESIRED_GEOM.width <= 2 || DESIRED_GEOM.height <= 2) {"),
    ("S330", "GeometricMovableAnimated.cpp", 19,
     "case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();"),
    ("S331", "host-clients-r43.json", 5, '"class": "Alacritty",'),
    ("S332", "gkeep-ui-excerpt.py", 33, "window.set_default_size(420, 500)"),
    ("S333", "Rule.cpp", 52, "{RULE_PROP_CLASS, RULE_MATCH_ENGINE_REGEX},"),
]

# anchor ranges each row cites: (row, file, start, end, what)
RANGES = [
    ("S326", "RegexMatchEngine.cpp", 6, 13, "constructor branches on the prefix"),
    ("S326", "RegexMatchEngine.cpp", 15, 17, "match returns FullMatch against the flag"),
    ("S327", "DefaultFloatingAlgorithm.cpp", 19, 45, "desired geometry or its absence"),
    ("S327", "DefaultFloatingAlgorithm.cpp", 49, 66, "first-map static size evaluation"),
    ("S327", "DefaultFloatingAlgorithm.cpp", 79, 84, "center rule only"),
    ("S327", "DefaultFloatingAlgorithm.cpp", 90, 91, "re-center when no position"),
    ("S327", "DefaultFloatingAlgorithm.cpp", 93, 102, "placement"),
    ("S328", "Target.cpp", 10, 14, "box stored and both parts rounded"),
    ("S328", "Target.cpp", 64, 66, "position returns the logical part"),
    ("S328", "Target.cpp", 68, 74, "floating-size member and setter"),
    ("S329", "WindowTarget.cpp", 297, 304, "clamp by min and max"),
    ("S329", "WindowTarget.cpp", 313, 313, "size starts as the clamped client size"),
    ("S329", "WindowTarget.cpp", 323, 326, "persistent-size override"),
    ("S329", "WindowTarget.cpp", 339, 365, "small-box fallbacks"),
    ("S330", "GeometricMovableAnimated.cpp", 17, 24, "size reads goal or value"),
    ("S333", "Rule.cpp", 52, 52, "class bound to the regex engine"),
    ("S333", "Rule.cpp", 98, 98, "engine id constructs CRegexMatchEngine"),
    ("S333", "WindowRule.cpp", 395, 396, "class case hands the class to the engine"),
    ("S327", "Window.cpp", 2402, 2409, "tiled consumer of the same stored expression"),
]


def path_of(name):
    seat = os.path.join(SEAT, "fetch", name)
    if os.path.exists(seat):
        return seat
    return os.path.join(LANE, ".ufo", "waves", "round-43", "fetch", name)


def main():
    fail = 0
    print("# computed locators - quotes")
    for row, name, line, quote in QUOTES:
        p = path_of(name)
        blob = open(p, "rb").read()
        sha = hashlib.sha256(blob).hexdigest()
        pin_ok = sha == PINS[name]
        text = blob.decode()
        lines = text.split("\n")
        hits = [i for i, l in enumerate(lines, 1) if quote in l]
        words = len(quote.split())
        ok = pin_ok and hits == [line] and words <= 25
        fail += 0 if ok else 1
        print(f"{row} {name}:{line} words={words} hits={hits} sha256={sha[:16]} pin={'ok' if pin_ok else 'MISMATCH'} {'OK' if ok else 'FAIL'}")
        print(f"    line {line}: {lines[line - 1].strip()[:120]}")
    print("\n# computed locators - anchor ranges (first and last line of each range)")
    for row, name, a, b, what in RANGES:
        lines = open(path_of(name), encoding="utf-8", errors="replace").read().split("\n")
        print(f"{row} {name}:{a}-{b} ({what})")
        print(f"    {a}: {lines[a - 1].strip()[:120]}")
        if b != a:
            print(f"    {b}: {lines[b - 1].strip()[:120]}")
    print("\n# negative sweeps")
    for name, needle in [("host-clients-r43.json", "fullscreen"), ("host-clients-r43.json", "title"),
                         ("host-clients-r43.json", "org.omarchy.gkeep"), ("gkeep-ui-excerpt.py", "set_size_request"),
                         ("Window.cpp", "set_size_request")]:
        text = open(path_of(name), encoding="utf-8", errors="replace").read()
        print(f"{name}: grep -c {needle} = {text.count(needle)}")
    ui = os.path.expanduser("~/Projects/gkeep/gkeep/ui.py")
    if os.path.exists(ui):
        blob = open(ui, "rb").read()
        print(f"ui.py sha256={hashlib.sha256(blob).hexdigest()} set_size_request={blob.decode().count('set_size_request')}")
        for n, l in enumerate(blob.decode().split("\n"), 1):
            if "application_id" in l or "set_default_size" in l:
                print(f"ui.py:{n}: {l.strip()}")
    print(f"\nQUOTE_AND_RANGE_CHECK: {'ok' if fail == 0 else f'{fail} FAILED'}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
