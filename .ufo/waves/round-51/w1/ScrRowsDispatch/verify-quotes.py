#!/usr/bin/env python3
"""S364-S369 quote verifier (round-51 w1, seat ScrRowsDispatch).

Read-only: for every drafted row, open the pin, read the cited line, assert the
quote appears verbatim on that line, and count words (whitespace tokens, <=25).

Usage: python3 verify-quotes.py <pin-dir> [<pin-dir-2> ...]
The first directory that holds a pin supplies its bytes; later ones must be
byte-equal where the file repeats (reported as cmp lines).
No writes, no network, no /tmp.
"""
import hashlib
import sys
from pathlib import Path

# id, pin basename, cited line, quote, expected bytes, expected sha256
ROWS = [
    ("S364", "Hyprland-KeybindManager.cpp", 785,
     'const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);',
     39334, "8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40"),
    ("S364", "Hyprland-KeybindManager.hpp", 137,
     "std::unordered_map<std::string, std::function<SDispatchResult(std::string)>> m_dispatchers;",
     7936, "cee22c13d413ab389803e0eb87a6fcefadedea885cee4457b56ae351228dd1e0"),
    ("S365", "Hyprland-legacy-DispatcherTranslator.cpp", 32,
     'return {.success = false, .error = "Bad dispatcher"};',
     35997, "7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771"),
    ("S365", "Hyprland-legacy-DispatcherTranslator.hpp", 19,
     "std::unordered_map<std::string, std::function<SDispatchResult(const std::string&)>> m_dispMap;",
     567, "438c1e662f5c9fa4d5821fbab251113c66562dd452d1844f965c294bb3444e87"),
    ("S366", "Hyprland-HyprCtl.cpp", 1149,
     "const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(DISPATCHSTR);",
     97582, "798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa"),
    ("S367", "Hyprland-ConfigActions.cpp", 1681,
     'return std::unexpected(std::format("Cannot set submap {}, submap doesn\'t exist (wasn\'t registered!)", submap));',
     71407, "a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637"),
    ("S368", "Hyprland-legacy-ConfigManager.cpp", 1594,
     "const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(HANDLER);",
     90963, "9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b"),
    ("S369", "Hyprland-SharedDefs.hpp", 53,
     "bool        passEvent = false;",
     1915, "0b40cc83f827587f3a94260ca89d4464150dc2b45de2b9331e3d1876cafe0087"),
]


def main(argv):
    if len(argv) < 2:
        print("usage: verify-quotes.py <pin-dir> [<pin-dir> ...]", file=sys.stderr)
        return 2
    dirs = [Path(a) for a in argv[1:]]
    bad = 0
    seen = {}
    for rid, pin, line_no, quote, exp_bytes, exp_sha in ROWS:
        path = next((d / pin for d in dirs if (d / pin).is_file()), None)
        if path is None:
            print(f"{rid} {pin}:{line_no} ABSENT-PIN searched={[str(d) for d in dirs]}")
            bad += 1
            continue
        data = path.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        nbytes = len(data)
        lines = data.decode("utf-8").split("\n")
        text = lines[line_no - 1] if line_no <= len(lines) else ""
        words = len(quote.split())
        verbatim = quote in text
        meta_ok = (nbytes == exp_bytes and sha == exp_sha)
        seen.setdefault(pin, []).append((path, sha))
        print(f"{rid} {pin}:{line_no} bytes={nbytes} sha256={sha[:16]} meta={'ok' if meta_ok else 'MISMATCH'}")
        print(f"  line: {text.strip()}")
        print(f"  quote({words}w): {quote}")
        print(f"  verbatim={'YES' if verbatim else 'NO'} words_ok={'YES' if words <= 25 else 'NO'} pipe_free={'YES' if '|' not in quote else 'NO'}")
        if not (verbatim and words <= 25 and meta_ok and "|" not in quote):
            bad += 1
    for pin in sorted({r[1] for r in ROWS}):
        copies = [d / pin for d in dirs if (d / pin).is_file()]
        for a, b in zip(copies, copies[1:]):
            same = a.read_bytes() == b.read_bytes()
            print(f"cmp {pin}: {a} vs {b} byte_equal={same}")
            if not same:
                bad += 1
    print(f"ROWS={len({r[0] for r in ROWS})} CHECKS={len(ROWS)} BAD={bad} verdict={'OK' if bad == 0 else 'FAIL'}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
