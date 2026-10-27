#!/usr/bin/env python3
"""Round-49 C1 fixture builder (ExecFixtures seat).

Compiles each fixture keymap with the PINNED xkbcli-compile-keymap in a clean
environment, runs the PINNED xkbcli-how-to-type three times per (keymap, arg)
case, requires the three runs to be identical, and emits fixtures.json.

Never writes outside its work dir (--work); refuses a /tmp work dir.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

COMPILE = "/usr/lib/xkbcommon/xkbcli-compile-keymap"
JUDGE = "/usr/lib/xkbcommon/xkbcli-how-to-type"
PIN_COMPILE = "43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250"
PIN_JUDGE = "f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54"

DEFAULT_RMLVO = {"rules": "evdev", "model": "pc105", "layout": "us",
                 "variant": "", "options": ""}

# Classes whose args must all resolve to a keysym (rc 0 with the fixed header).
RESOLVABLE = frozenset({"HOST", "MULTI", "VARIANT", "OPTIONS", "LETTERS",
                        "DIGITS", "PUNCT", "DEAD", "KEYPAD", "FUNCTION",
                        "XF86", "MODIFIER", "ABSENT", "NUMERIC"})

KEYMAPS = [
    ("host",              {"layout": "br", "options": "compose:caps"}),
    ("multi-br-us",       {"layout": "br,us"}),
    ("multi-us-ru-de",    {"layout": "us,ru,de"}),
    ("multi-us-ru-grp",   {"layout": "us,ru", "options": "grp:alt_shift_toggle"}),
    ("multi-3var",        {"layout": "us,ru,de", "variant": ",,nodeadkeys"}),
    ("var-br-nodeadkeys", {"layout": "br", "variant": "nodeadkeys"}),
    ("var-br-abnt2",      {"layout": "br", "variant": "abnt2"}),
    ("var-br-thinkpad",   {"layout": "br", "variant": "thinkpad"}),
    ("var-br-dvorak",     {"layout": "br", "variant": "dvorak"}),
    ("var-us-intl",       {"layout": "us", "variant": "intl"}),
    ("var-us-dvorak",     {"layout": "us", "variant": "dvorak"}),
    ("var-us-colemak",    {"layout": "us", "variant": "colemak"}),
    ("var-us-altgr-intl", {"layout": "us", "variant": "altgr-intl"}),
    ("var-de-nodeadkeys", {"layout": "de", "variant": "nodeadkeys"}),
    ("opt-lv3-ralt",      {"layout": "us", "options": "lv3:ralt_switch"}),
    ("opt-caps-escape",   {"layout": "us", "options": "caps:escape"}),
    ("opt-ctrl-nocaps",   {"layout": "us", "options": "ctrl:nocaps"}),
    ("opt-altwin",        {"layout": "us", "options": "altwin:swap_lalt_lwin"}),
    ("opt-compose-ralt",  {"layout": "us", "options": "compose:ralt"}),
    ("opt-keypad-pointer", {"layout": "de", "options": "keypad:pointerkeys"}),
    ("opt-lv3-compose",   {"layout": "br", "options": "lv3:ralt_switch,compose:ralt"}),
    ("opt-swapcaps",      {"layout": "us", "options": "ctrl:swapcaps"}),
    ("multi-4lay",        {"layout": "us,ru,de,fr"}),
    ("opt-lv5-caps",      {"layout": "us", "options": "lv5:caps_switch"}),
    ("opt-grp-shifts",    {"layout": "us,ru", "options": "grp:shifts_toggle"}),
    ("opt-breaks-caps",   {"layout": "us", "options": "shift:breaks_caps"}),
    ("opt-nbsp-l3",       {"layout": "us", "options": "nbsp:level3"}),
    # Same RMLVO as `host`: the CASE class needs its own pair space so the
    # case-sensitivity contrasts cannot be eaten by BIND/HOST dedupe.
    ("case-host",         {"layout": "br", "options": "compose:caps"}),
]

LETTERS = list("abcdefghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
DIGITS = list("0123456789")
PUNCT = ["slash", "question", "backslash", "bar", "at", "numbersign", "dollar",
         "percent", "asciicircum", "ampersand", "asterisk", "parenleft",
         "parenright", "minus", "underscore", "equal", "plus", "bracketleft",
         "bracketright", "braceleft", "braceright", "semicolon", "colon",
         "apostrophe", "quotedbl", "grave", "asciitilde", "comma", "less",
         "period", "greater", "exclam", "guillemotleft", "masculine"]
DEAD = ["dead_grave", "dead_acute", "dead_circumflex", "dead_tilde",
        "dead_diaeresis", "dead_cedilla", "dead_abovering", "dead_macron",
        "dead_breve", "dead_abovedot", "dead_caron", "dead_ogonek",
        "dead_doubleacute", "dead_stroke", "dead_belowdot", "dead_hook",
        "dead_horn", "dead_currency", "dead_greek", "dead_abovedot"]
KEYPAD = ["KP_0", "KP_1", "KP_2", "KP_3", "KP_4", "KP_5", "KP_6", "KP_7",
          "KP_8", "KP_9", "KP_Add", "KP_Subtract", "KP_Multiply", "KP_Divide",
          "KP_Decimal", "KP_Enter", "KP_Separator", "KP_Equal", "KP_Space",
          "KP_Tab", "KP_Begin", "KP_Home", "KP_End", "KP_Insert"]
FUNCTION = (["F%d" % i for i in range(1, 36)] +
            ["Return", "Tab", "BackSpace", "Escape", "Delete", "Insert",
             "Home", "End", "Page_Up", "Page_Down", "Up", "Down", "Left",
             "Right", "space", "Menu", "Print", "Pause", "Scroll_Lock",
             "Num_Lock", "Begin", "Clear", "Linefeed"])
XF86 = ["XF86AudioMute", "XF86AudioRaiseVolume", "XF86AudioLowerVolume",
        "XF86AudioMicMute", "XF86AudioPlay", "XF86AudioPause", "XF86AudioNext",
        "XF86AudioPrev", "XF86AudioStop", "XF86AudioRecord",
        "XF86MonBrightnessUp", "XF86MonBrightnessDown",
        "XF86KbdBrightnessUp", "XF86KbdBrightnessDown", "XF86KbdLightOnOff",
        "XF86TouchpadToggle", "XF86TouchpadOn", "XF86TouchpadOff",
        "XF86PowerOff", "XF86Calculator", "XF86WakeUp", "XF86Sleep",
        "XF86WWW", "XF86Search", "XF86HomePage", "XF86Mail", "XF86Battery",
        "XF86Display", "XF86Favorites", "XF86Shop"]
MODIFIER = ["Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R",
            "Super_L", "Super_R", "Caps_Lock", "ISO_Level3_Shift", "ISO_Level5_Shift",
            "ISO_Next_Group", "ISO_Prev_Group", "Mode_switch", "Meta_L", "Meta_R",
            "Hyper_L", "Shift_Lock"]
ABSENT = ["Greek_alpha", "Greek_omega", "Armenian_ayb", "Armenian_ben",
          "Thai_kokai", "Thai_khokhai", "Georgian_an", "Greek_beta", "Amacron",
          "Emacron", "Imacron", "Omacron", "Umacron", "adiaeresis", "eacute",
          "ccedilla", "ntilde", "udiaeresis", "oe", "ssharp", "Cyrillic_a",
          "Cyrillic_ya", "Serbian_dje", "Arabic_alef"]
NUMERIC = ["0x2f", "47", "0x1000e9", "0xff0d", "0x20",
           "0xfe51", "0xffb7", "0x61", "97", "0x1008ff12", "0x1008ff13",
           "0x7e1", "10", "0x3"]
CASE = ["return", "Return", "RETURN", "SLASH", "Slash", "slash", "A", "a",
        "XF86AudioMute", "xf86audiomute", "XF86audiomute", "DEAD_ACUTE",
        "kp_7", "KP_7", "Space", "SPACE", "backspace", "BackSpace",
        "Escape", "escape", "ESCAPE", "Num_lock", "NUM_LOCK"]
INVALID = ["nosuchsym", "", "U+0041", "0x", "0xzz", "-1", "0xfffffffff",
           "slash ", " slash", "SLASH!", "dead_", "XKB_KEY_slash",
           "0x0", "999999999", "zero", "one", "five", "nine"]

# (class, keymap_id, arg) -- order matters: first class to claim a pair wins.
def cases():
    out = []
    # HOST: the host's own keymap (br + compose:caps), broad arg kinds.
    host_args = (["a", "s", "d", "q", "w", "e", "z", "x", "c"] + DIGITS[:6] +
                 ["slash", "question", "backslash", "bar", "at", "numbersign",
                  "semicolon", "colon", "apostrophe", "quotedbl", "minus",
                  "equal", "comma", "period", "exclam", "parenleft"] +
                 ["dead_acute", "dead_grave", "dead_tilde", "dead_circumflex",
                  "dead_diaeresis", "dead_cedilla"] +
                 ["Return", "Tab", "BackSpace", "Escape", "F1", "F9", "F35",
                  "space", "Up", "Left"] +
                 ["XF86AudioMute", "XF86AudioRaiseVolume", "XF86MonBrightnessUp",
                  "XF86KbdBrightnessDown", "XF86PowerOff"] +
                 ["KP_7", "KP_Enter", "KP_Add"] +
                 ["Shift_L", "ISO_Level3_Shift", "Caps_Lock", "Super_L"] +
                 ["cedilla", "ccedilla", "at", "Escape"])
    for a in host_args:
        out.append(("HOST", "host", a))
    # MULTI: 2-4 layouts.
    for km, args in [
        ("multi-br-us", ["slash", "question", "a", "z", "dead_acute", "Return",
                         "Cyrillic_ya", "adiaeresis", "semicolon", "period"]),
        ("multi-us-ru-de", ["a", "Cyrillic_a", "Cyrillic_ya", "Cyrillic_shorti", "ssharp",
                            "adiaeresis", "dollar", "at", "slash", "question",
                            "dead_acute", "dead_circumflex", "F1", "KP_7",
                            "Return", "space", "Shift_L", "backslash"]),
        ("multi-us-ru-grp", ["Cyrillic_a", "Cyrillic_ya", "a", "slash",
                             "ISO_Next_Group", "Mode_switch", "question",
                             "dead_grave", "y", "z"]),
        ("multi-3var", ["a", "Cyrillic_a", "adiaeresis", "dead_acute", "ssharp",
                        "dead_grave", "slash", "question", "F2", "KP_8",
                        "Return", "space"]),
        ("multi-4lay", ["a", "Cyrillic_a", "adiaeresis", "eacute", "1",
                        "slash", "question", "ssharp"]),
    ]:
        for a in args:
            out.append(("MULTI", km, a))
    # VARIANT
    for km, args in [
        ("var-br-nodeadkeys", ["dead_acute", "dead_grave", "dead_tilde", "acute",
                               "grave", "slash", "question", "a", "e"]),
        ("var-br-abnt2", ["slash", "question", "backslash", "KP_Decimal",
                          "KP_Separator", "a", "dead_acute", "Escape",
                          "cedilla", "dead_cedilla"]),
        ("var-br-thinkpad", ["slash", "question", "dead_grave", "a", "e",
                             "XF86AudioMute", "Return"]),
        ("var-br-dvorak", ["a", "x", "slash", "question", "dead_acute", "e",
                           "comma", "period"]),
        ("var-us-intl", ["dead_acute", "dead_grave", "dead_circumflex",
                         "dead_tilde", "dead_diaeresis", "apostrophe",
                         "quotedbl", "a", "e", "space"]),
        ("var-us-dvorak", ["a", "e", "period", "comma", "slash", "minus",
                           "semicolon", "x", "y", "apostrophe"]),
        ("var-us-colemak", ["a", "e", "semicolon", "slash", "period", "f",
                            "j", "y"]),
        ("var-us-altgr-intl", ["dead_acute", "dead_grave", "dead_tilde",
                               "eacute", "adiaeresis", "ssharp", "at",
                               "braceleft", "e", "a"]),
        ("var-de-nodeadkeys", ["adiaeresis", "ssharp", "dead_acute", "dead_grave",
                               "dead_circumflex", "z", "y", "minus", "plus"]),
    ]:
        for a in args:
            out.append(("VARIANT", km, a))
    # OPTIONS
    for km, args in [
        ("opt-lv3-ralt", ["ISO_Level3_Shift", "eacute", "at", "braceleft",
                          "EuroSign", "bar", "a", "slash"]),
        ("opt-caps-escape", ["Escape", "Caps_Lock", "a", "slash", "dead_grave"]),
        ("opt-ctrl-nocaps", ["Caps_Lock", "Control_L", "a", "slash"]),
        ("opt-altwin", ["Alt_L", "Super_L", "a", "Return"]),
        ("opt-compose-ralt", ["Multi_key", "Alt_R", "a", "at"]),
        ("opt-keypad-pointer", ["KP_7", "KP_Home", "KP_Add", "KP_Decimal"]),
        ("opt-lv3-compose", ["ISO_Level3_Shift", "slash", "question", "at",
                             "Multi_key"]),
        ("opt-swapcaps", ["Caps_Lock", "Control_L", "a", "slash"]),
        ("opt-lv5-caps", ["ISO_Level5_Shift", "a", "at", "braceleft"]),
        ("opt-grp-shifts", ["ISO_Next_Group", "Cyrillic_a", "a"]),
        ("opt-breaks-caps", ["A", "a", "slash"]),
        ("opt-nbsp-l3", ["nobreakspace", "space", "a"]),
    ]:
        for a in args:
            out.append(("OPTIONS", km, a))
    # LETTERS: letter keysyms across layouts.
    for km, args in [
        ("var-us-dvorak", LETTERS[:14]),
        ("multi-us-ru-de", ["q", "w", "e", "r", "t", "y", "u", "i",
                            "o", "p", "A", "Q", "Z", "W"]),
        ("var-us-colemak", ["a", "b", "c", "d", "e", "n", "o", "u", "A", "B"]),
        ("var-br-dvorak", ["a", "b", "c", "d", "e", "f", "g", "h"]),
    ]:
        for a in args:
            out.append(("LETTERS", km, a))
    # DIGITS
    for km, args in [
        ("multi-us-ru-de", DIGITS),
        ("var-us-intl", ["0", "1", "5", "9"]),
        ("var-br-abnt2", ["0", "1", "2", "3"]),
    ]:
        for a in args:
            out.append(("DIGITS", km, a))
    # PUNCT
    for km, args in [
        ("multi-br-us", PUNCT[:16]),
        ("var-us-intl", PUNCT[16:]),
        ("multi-us-ru-de", ["slash", "question", "backslash", "bar", "at",
                            "numbersign", "semicolon"]),
        ("var-us-altgr-intl", ["at", "numbersign", "braceleft", "braceright",
                               "bracketleft", "bar", "slash"]),
    ]:
        for a in args:
            out.append(("PUNCT", km, a))
    # DEAD
    for km, args in [
        ("multi-br-us", DEAD[:10]),
        ("var-us-intl", DEAD[10:]),
        ("var-de-nodeadkeys", DEAD[:6]),
        ("var-br-nodeadkeys", DEAD[2:8]),
    ]:
        for a in args:
            out.append(("DEAD", km, a))
    # KEYPAD
    for km, args in [
        ("multi-us-ru-de", KEYPAD[:12]),
        ("opt-keypad-pointer", KEYPAD[12:]),
        ("host", ["KP_7", "KP_8", "KP_Add"]),
        ("var-de-nodeadkeys", ["KP_Decimal", "KP_Separator", "KP_Enter"]),
    ]:
        for a in args:
            out.append(("KEYPAD", km, a))
    # FUNCTION
    for km, args in [
        ("multi-us-ru-de", FUNCTION[:18]),
        ("host", FUNCTION[18:28]),
        ("var-us-dvorak", FUNCTION[28:]),
        ("opt-caps-escape", ["Escape", "F11", "F12"]),
    ]:
        for a in args:
            out.append(("FUNCTION", km, a))
    # XF86
    for km, args in [
        ("host", XF86[:10]),
        ("multi-us-ru-de", XF86[10:20]),
        ("var-br-thinkpad", XF86[20:]),
        ("opt-lv3-ralt", ["XF86AudioMute", "XF86MonBrightnessDown"]),
    ]:
        for a in args:
            out.append(("XF86", km, a))
    # MODIFIER
    for km, args in [
        ("opt-lv3-ralt", MODIFIER[:8]),
        ("multi-us-ru-grp", MODIFIER[8:14]),
        ("opt-altwin", MODIFIER[14:]),
        ("host", ["Shift_L", "ISO_Level3_Shift", "Caps_Lock"]),
    ]:
        for a in args:
            out.append(("MODIFIER", km, a))
    # ABSENT
    for km, args in [
        ("multi-us-ru-de", ["Greek_alpha", "Thai_kokai", "Armenian_ayb",
                            "Greek_beta", "Amacron", "Emacron"]),
        ("host", ["Greek_alpha", "Thai_kokai", "Armenian_ayb", "Amacron"]),
        ("var-us-intl", ["Greek_omega", "Thai_khokhai", "Georgian_an"]),
        ("var-de-nodeadkeys", ["Greek_alpha", "Arabic_alef"]),
    ]:
        for a in args:
            out.append(("ABSENT", km, a))
    # NUMERIC
    for km, args in [
        ("host", NUMERIC),
        ("multi-us-ru-de", ["0x2f", "47", "0x7e1", "0x1008ff12"]),
        ("var-us-dvorak", ["0x2f", "0x3f", "0x20"]),
    ]:
        for a in args:
            out.append(("NUMERIC", km, a))
    # CASE
    for km, args in [
        ("case-host", CASE),
        ("var-us-dvorak", ["A", "a", "Return", "return"]),
        ("multi-us-ru-de", ["SLASH", "slash", "KP_7", "kp_7"]),
    ]:
        for a in args:
            out.append(("CASE", km, a))
    # INVALID
    for km, args in [
        ("host", INVALID),
        ("var-us-dvorak", ["nosuchsym", "U+0041"]),
    ]:
        for a in args:
            out.append(("INVALID", km, a))
    return out


def bind_args(path):
    """Distinct keysym-ish key strings from a `hyprctl binds -j` capture."""
    keys = []
    seen = set()
    with open(path, encoding="utf-8") as fh:
        for row in json.load(fh):
            k = row.get("key")
            if not isinstance(k, str) or not k:
                continue
            if k.startswith(("mouse:", "mouse_", "switch:")):
                continue
            if k not in seen:
                seen.add(k)
                keys.append(k)
    return keys


def clean_env(work):
    return {"PATH": "/usr/bin", "HOME": os.path.join(work, "w"),
            "XDG_CONFIG_HOME": os.path.join(work, "w", "cfg")}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--binds", required=True, help="hyprctl binds -j capture")
    ap.add_argument("--log", required=True)
    args = ap.parse_args()
    work = os.path.abspath(args.work)
    if work == "/tmp" or work.startswith("/tmp/"):
        sys.exit("refusing a work dir under /tmp")

    if sha256(COMPILE) != PIN_COMPILE or sha256(JUDGE) != PIN_JUDGE:
        sys.exit("pinned binaries do not match")
    for d in ("km", "w/cfg"):
        os.makedirs(os.path.join(work, d), exist_ok=True)
    env = clean_env(work)
    log = open(args.log, "w", encoding="utf-8")

    def note(msg):
        log.write(msg + "\n")
        log.flush()

    note("judge_sha256=%s" % sha256(JUDGE))
    note("compile_sha256=%s" % sha256(COMPILE))

    rmlvo = {}
    kmfile = {}
    for kid, over in KEYMAPS:
        envd = dict(DEFAULT_RMLVO)
        envd.update(over)
        rmlvo[kid] = envd
        path = os.path.join(work, "km", kid + ".xkb")
        cmd = [COMPILE]
        for opt in ("rules", "model", "layout", "variant", "options"):
            if envd[opt]:
                cmd += ["--" + opt, envd[opt]]
        with open(path, "wb") as out:
            proc = subprocess.run(cmd, stdout=out, stderr=subprocess.PIPE, env=env)
        err = proc.stderr.decode("utf-8", "replace")
        if proc.returncode != 0:
            note("COMPILE_FAIL %s rc=%d %s" % (kid, proc.returncode,
                                               err.replace("\n", " | ")))
            sys.exit("compile failed for %s" % kid)
        if "XKB-595" in err or "Unrecognized" in err:
            note("COMPILE_WARN %s %s" % (kid, err.replace("\n", " | ")))
            sys.exit("rmlvo option not recognized for %s" % kid)
        kmfile[kid] = path
        note("keymap %s sha256=%s bytes=%d rmlvo=%s"
             % (kid, sha256(path), os.path.getsize(path), json.dumps(envd, sort_keys=True)))

    # BIND cases first: every keysym-ish key the host's `hyprctl binds -j`
    # names, upper-case as Hyprland writes them, on the host keymap. Claiming
    # them first keeps the class complete instead of losing pairs to HOST.
    requested = [("BIND", "host", a) for a in bind_args(args.binds)]
    requested += cases()

    seen = set()
    fixtures = []
    run_count = 0
    for cls, kid, arg in requested:
        if (kid, arg) in seen:
            continue
        seen.add((kid, arg))
        results = []
        for _ in range(3):
            proc = subprocess.run(
                [JUDGE, "--keymap=" + kmfile[kid], "--disable-compose",
                 "--keysym", arg],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env)
            run_count += 1
            results.append((proc.returncode, proc.stdout))
        if len({r for r in results}) != 1:
            note("UNSTABLE %s %s %r" % (cls, kid, arg))
            sys.exit("judge output not reproducible for %r" % arg)
        rc, stdout = results[0]
        fixtures.append({
            "id": "r49-c1-%04d" % (len(fixtures) + 1),
            "class": cls,
            "rmlvo": rmlvo[kid],
            "arg": arg,
            "expect": {"stdout": stdout.decode("utf-8"), "rc": rc},
        })
        if rc == 2 and stdout:
            note("INVALID_WITH_STDOUT arg=%r bytes=%d" % (arg, len(stdout)))

    # Class invariants: a mis-classed arg (a name that does not resolve, an
    # absent keysym filed under a resolvable class) fails the build.
    header = "=== Direct access ==="
    for f in fixtures:
        cls, exp = f["class"], f["expect"]
        rows = 0
        if exp["rc"] == 0:
            lines = exp["stdout"].splitlines()
            if header not in lines:
                sys.exit("%s: rc 0 without header (%r)" % (f["id"], f["arg"]))
            idx = lines.index("KEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS")
            rows = len([l for l in lines[idx + 1:] if l.strip()])
        if cls in RESOLVABLE and exp["rc"] != 0:
            sys.exit("%s: %s arg %r does not resolve (rc %d)"
                     % (f["id"], cls, f["arg"], exp["rc"]))
        if cls == "ABSENT" and rows != 0:
            sys.exit("%s: ABSENT arg %r printed %d rows" % (f["id"], f["arg"], rows))
        if cls == "INVALID" and (exp["rc"] != 2 or exp["stdout"]):
            sys.exit("%s: INVALID arg %r rc=%d stdout=%r"
                     % (f["id"], f["arg"], exp["rc"], exp["stdout"][:40]))
        if cls == "BIND" and exp["rc"] == 2 and exp["stdout"]:
            sys.exit("%s: BIND arg %r rc 2 with stdout" % (f["id"], f["arg"]))

    with open(args.out, "w", encoding="utf-8") as out:
        json.dump(fixtures, out, ensure_ascii=False, indent=1)
        out.write("\n")

    note("fixtures=%d judge_runs=%d triples_stable=%d" % (len(fixtures), run_count,
                                                          len(fixtures)))
    log.close()


if __name__ == "__main__":
    main()
