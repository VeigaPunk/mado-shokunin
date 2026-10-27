#!/usr/bin/env python3
"""ScrEntry (round 48, C2) - verify every quote in the entry draft.

For each (file, line, needle):
  1. the file's sha256 equals the digest pinned when the file was fetched,
  2. the needle occurs on the cited line,
  3. the computed locators (every line that carries the needle) are printed,
  4. the needle's words number <= 25,
  5. the needle also occurs in the entry draft (so the entry quotes the bytes it cites).

Exit 0 only when every check passes.
"""
import hashlib
import pathlib
import re
import sys

SEAT = pathlib.Path(__file__).resolve().parent
ENTRY = SEAT / "xkb-keymap-compile-r48.md"
RULES_EVDEV = pathlib.Path("/usr/share/xkeyboard-config-2/rules/evdev")

PINS = {
    "fetch/xkbcommon-rules.c":
        "04dfd93468369de226b47c94475c1df93a41ce85bdd698c761312a38204e42a8",
    "fetch/xkbcommon-xkbcomp.c":
        "ae6823a876691c340362fb43a784ad4f45a3a96869474503965bfef4481dd74c",
    "fetch/xkbcommon-include.c":
        "95b5d8b53be3d53e30d07824cae6952f2f148c63c29e552592cf1dd6da68eaef",
    "fetch/xkbcommon-context.c":
        "e6547abb657d27cdb42907d254d9bdd047435db8b5f59bb88fe69a315b84b8b7",
    "fetch/xkbcommon-context-priv.c":
        "c2ffff03f40181e4110d5549d4cab3be002cfc4258125a15d6f4876f31724c10",
    "fetch/xkbcommon-tools-compile-keymap.c":
        "099664cea533c2ea4c85b2bd45b8f3dc0f9ed4e2b39f904b2cf5c165f10e533d",
    "fetch/xkbcommon-messages-codes.h":
        "4e721d31ebd9b8979efb46905644f8f19dcdb450f6a00e57be48cf2cf013631d",
    "fetch/xkbcommon-meson_options.txt":
        "496455ea3c5b368b382e3b155e66eb43226f66b0a0d1eeabbca450976175c32d",
    "fetch/xkeyboard-config-symbols-br":
        "8cf65550e08b598407d5f7317f297e186561a94c866ab95d0c9a8737ef3bf35e",
    "fetch/xkeyboard-config-rules-evdev":
        "0cc48ee1279d91045fe2cf092ee5a0744cbee1c02bd164f02871d13140d12132",
}

# (file, line, needle) - needles are exact byte substrings of the pinned file.
QUOTES = [
    ("fetch/xkbcommon-rules.c", 1259,
     r"No index provided: match only if single layout"),
    ("fetch/xkbcommon-rules.c", 1297,
     r"expanded_value->matched = true;"),
    ("fetch/xkbcommon-rules.c", 2063,
     r'Unrecognized RMLVO option \"%.*s\" was ignored'),
    ("fetch/xkbcommon-rules.c", 530,
     r'Less layouts than variants: \"%s\" vs. \"%s\".'),
    ("fetch/xkbcommon-xkbcomp.c", 157,
     r"ok = xkb_components_from_rules_names(keymap->ctx, rmlvo, &kccgst,"),
    ("fetch/xkbcommon-xkbcomp.c", 161,
     r"Couldn't look up rules '%s', model '%s', layout '%s', "),
    ("fetch/xkbcommon-include.c", 355,
     "Couldn't find file \\\"%s/%.*s\\\" in include paths"),
    ("fetch/xkbcommon-include.c", 501,
     r"Couldn't process include statement for '%s(%s)'"),
    ("fetch/xkbcommon-context.c", 317,
     r"const char * const root = xkb_context_include_path_get_system_path(ctx);"),
    ("fetch/xkbcommon-context.c", 336,
     r"ret |= context_include_path_append(ctx, DFLT_XKB_LEGACY_ROOT);"),
    ("fetch/xkbcommon-context.c", 503,
     r"ctx->log_level = XKB_LOG_LEVEL_ERROR;"),
    ("fetch/xkbcommon-context-priv.c", 208,
     r'Layout not provided, but variant set to \"%s\": '),
    ("fetch/xkbcommon-meson_options.txt", 46,
     r"value: 'us',"),
    ("fetch/xkeyboard-config-rules-evdev", 175,
     r"pc+%l%(v)"),
    ("fetch/xkeyboard-config-rules-evdev", 570,
     r"compose:caps"),
    ("fetch/xkeyboard-config-symbols-br", 47,
     r'xkb_symbols "nodeadkeys" {'),
    ("fetch/xkbcommon-tools-compile-keymap.c", 587,
     r"ctx_flags |= XKB_CONTEXT_NO_ENVIRONMENT_NAMES;"),
    ("fetch/xkbcommon-tools-compile-keymap.c", 521,
     'fprintf(stderr, "ERROR: Couldn\'t create xkb keymap\\n");'),
    ("fetch/xkbcommon-messages-codes.h", 116,
     r"XKB_ERROR_INCLUDED_FILE_NOT_FOUND = 338,"),
    ("fetch/xkbcommon-messages-codes.h", 150,
     r"XKB_ERROR_CANNOT_RESOLVE_RMLVO = 595,"),
]


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    entry = ENTRY.read_text(encoding="utf-8")
    failures = []
    print(f"entry: {ENTRY.name} ({len(entry)} bytes)")
    pin_ok = {}
    for rel, want in PINS.items():
        path = pathlib.Path(rel) if rel.startswith("/") else SEAT / rel
        got = sha256(path) if path.exists() else "MISSING"
        ok = got == want
        pin_ok[rel] = ok
        print(f"pin {'PASS' if ok else 'FAIL'} {rel} {got[:16]}")
        if not ok:
            failures.append(f"pin {rel}: {got}")

    for i, (rel, line, needle) in enumerate(QUOTES, 1):
        path = pathlib.Path(rel) if rel.startswith("/") else SEAT / rel
        lines = path.read_text(encoding="utf-8", errors="surrogateescape").splitlines()
        cited = lines[line - 1] if 0 < line <= len(lines) else ""
        on_line = needle in cited
        computed = [n for n, text in enumerate(lines, 1) if needle in text]
        words = len(needle.split())
        in_entry = needle in entry
        ok = pin_ok.get(rel, False) and on_line and in_entry and words <= 25
        status = "PASS" if ok else "FAIL"
        print(f"q{i:02d} {status} {rel}:{line} words={words} "
              f"locators={computed} on_cited_line={on_line} in_entry={in_entry}")
        print(f"     needle={needle!r}")
        if not ok:
            failures.append(f"quote {i} {rel}:{line}: {needle!r} "
                            f"(pin={pin_ok.get(rel)} on_line={on_line} "
                            f"in_entry={in_entry} words={words})")

    print()
    if failures:
        print(f"FAIL {len(failures)} of {len(PINS) + len(QUOTES)} checks")
        for f in failures:
            print("  - " + f)
        return 1
    print(f"PASS all {len(PINS)} pins and {len(QUOTES)} quotes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
