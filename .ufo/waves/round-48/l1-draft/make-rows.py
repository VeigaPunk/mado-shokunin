#!/usr/bin/env python3
"""L1: build the S340-S350 registry rows for the C2 entry from the committed fetch pins (digests computed, never typed)
and the locators the entry cites for each pin. Prints the 11 rows; no cell carries a '|'."""
import hashlib
import os
import re
import sys

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(W, "fetch")
ENTRY = os.path.join(W, "l1-draft", "xkb-keymap-compile-r48.md")
USED = "corpus/knowledge/xkb-keymap-compile-r48.md"
XC = "https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/"
XKC = "https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config/-/raw/xkeyboard-config-2.48/"
XCOMMIT = "d1442aaa6b635551182e83c3b55037f4c118c962"
KCOMMIT = "cf8d1151bb4c9ef5b895828d0e6dd7860c0833e0"
ROWS = [
    ("S340", "libxkbcommon 1.13.2 RMLVO rules matcher", XC + "src/xkbcomp/rules.c", "code", ["xkbcommon-rules.c"],
     "how the rules file is found and read, how comma lists of layouts and variants pair, how %l and %v expand, and which unmatched names are reported as ignored",
     "an unknown layout or variant is consumed by the wildcard expansion and only fails later as a missing symbols file or map, while an unknown option is dropped with XKB-595 and the compile succeeds", XCOMMIT),
    ("S341", "libxkbcommon 1.13.2 keymap compiler entry", XC + "src/xkbcomp/xkbcomp.c", "code", ["xkbcommon-xkbcomp.c"],
     "the RMLVO to KcCGST to parse pipeline and the points where it returns no keymap",
     "a failed rules resolve or a failed parse makes the names call return NULL, which is all a compositor sees", XCOMMIT),
    ("S342", "libxkbcommon 1.13.2 include search", XC + "src/xkbcomp/include.c", "code", ["xkbcommon-include.c"],
     "how an include such as symbols/br(nodeadkeys) is looked up over the include paths and what a miss reports",
     "the first include path holding the file wins; a missing file logs XKB-338 with the paths searched, a missing map logs XKB-661", XCOMMIT),
    ("S343", "libxkbcommon 1.13.2 context and default include paths", XC + "src/context.c", "code", ["xkbcommon-context.c"],
     "the order of the default include paths, the legacy-root fallback and the default log level",
     "user paths ($XDG_CONFIG_HOME/xkb, $HOME/.xkb) come before /etc/xkb and the xkeyboard-config root, and WARNING lines are hidden at the default ERROR level", XCOMMIT),
    ("S344", "libxkbcommon 1.13.2 rule-name defaults", XC + "src/context-priv.c", "code", ["xkbcommon-context-priv.c"],
     "which empty names are replaced, from the environment or the build defaults, and the layout-variant tie",
     "empty rules, model and layout are replaced (environment first when the context reads it); options are replaced only when NULL, so an empty options string stays empty", XCOMMIT),
    ("S345", "libxkbcommon 1.13.2 build options", XC + "meson_options.txt", "code", ["xkbcommon-meson_options.txt"],
     "the compiled-in default rules, model, layout, variant and options",
     "the build defaults are rules evdev, model pc105, layout us, no variant and no options", XCOMMIT),
    ("S346", "xkeyboard-config 2.48 evdev ruleset - package file /usr/share/xkeyboard-config-2/rules/evdev of xkeyboard-config 2.48-1, generated from the tag's rules/rules.in by rules/meson.build",
     XKC + "rules/rules.in", "code", ["xkeyboard-config-rules-evdev", "xkeyboard-config-rules-rules.in", "xkeyboard-config-rules-meson.build"],
     "how model, layout, variant and option names become keycodes, types, compat, symbols and geometry components on this host",
     "any model maps to keycodes evdev, any layout and variant to symbols pc+%l%(v), and each option name to its own include such as compose:caps to +compose(caps)", KCOMMIT),
    ("S347", "xkeyboard-config 2.48 symbols file for Brazil", XKC + "symbols/br", "code", ["xkeyboard-config-symbols-br"],
     "which variant names the br layout defines as maps",
     "a variant compiles only when the layout file has an xkb_symbols map of that name; br has eleven", KCOMMIT),
    ("S348", "libxkbcommon 1.13.2 xkbcli compile-keymap tool", XC + "tools/compile-keymap.c", "code", ["xkbcommon-tools-compile-keymap.c"],
     "what the read-only compile verb passes to the library, its environment flag and its exit status",
     "xkbcli ignores XKB_DEFAULT_* unless --enable-environment-names is given and prints its own error line after the library's", XCOMMIT),
    ("S349", "libxkbcommon 1.13.2 message-code registry", XC + "src/messages-codes.h", "code", ["xkbcommon-messages-codes.h"],
     "the numeric ids behind the XKB-NNN prefixes in compiler output",
     "XKB-338, XKB-595 and XKB-661 are registered message ids, not severities", XCOMMIT),
]


def sha(name):
    return hashlib.sha256(open(os.path.join(F, name), "rb").read()).hexdigest()


def nlines(name):
    return open(os.path.join(F, name), "rb").read().count(b"\n")


def locs(entry, name):
    out = []
    for m in re.finditer(re.escape(name) + r":(\d+(?:-\d+)?)", entry):
        if m.group(1) not in out:
            out.append(m.group(1))
    return out


def main():
    entry = open(ENTRY).read()
    rows = []
    for rid, label, url, kind, pins, scope, teaches, commit in ROWS:
        anch = []
        for p in pins:
            ls = locs(entry, p)
            anch.append(", ".join("%s:%s" % (p, l) for l in ls) if ls else "%s whole file" % p)
        digests = "; ".join("%s %d B %d lines sha256:%s receipt .ufo/waves/round-48/fetch/%s" % (
            p, os.path.getsize(os.path.join(F, p)), nlines(p), sha(p), p) for p in pins)
        anchor = "%s @ commit %s; %s" % ("; ".join(anch), commit, digests)
        src = "%s - %s" % (label, url)
        row = [rid, src, kind, "A", scope, anchor, teaches, "mined", "2026-10-26", "on-release", USED]
        assert not any("|" in c for c in row), rid
        rows.append("| " + " | ".join(row) + " |")
    rec = os.path.join(W, "receipts", "xkbcli-compile-keymap-r48.txt")
    rsha = hashlib.sha256(open(rec, "rb").read()).hexdigest()
    rows.append("| " + " | ".join([
        "S350", "mado host - read-only xkbcli compile-keymap receipt, this host's names and the five unknown-name classes (measured 2026-10-26) - .ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt",
        "own-work", "A", "what libxkbcommon 1.13.2-1 with xkeyboard-config 2.48-1 does on this host with the configured names and with each class of wrong name",
        "xkbcli-compile-keymap-r48.txt whole file, %d B sha256:%s; receipt .ufo/waves/round-48/fetch/xkbcli-compile-keymap-r48.txt (byte copy of .ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt), generator .ufo/waves/round-48/receipts/make-xkb-receipt.sh" % (os.path.getsize(rec), rsha),
        "br plus compose:caps compiles (rc 0); unknown layout, variant and rules fail (rc 1); unknown option and model compile (rc 0), the option with XKB-595",
        "mined", "2026-10-26", "on-release", USED]) + " |")
    print("\n".join(rows))


if __name__ == "__main__":
    sys.exit(main())
