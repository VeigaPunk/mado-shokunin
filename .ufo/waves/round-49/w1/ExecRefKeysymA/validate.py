#!/usr/bin/env python3
"""Differential check: ours (mado-keysym.py) against the pinned judge, on compiled keymaps.

Every judge run gets a clean environment (env -i PATH=/usr/bin, HOME and XDG_* under the scratch
dir) so no user xkb include path exists. Keymaps are compiled with the pinned
xkbcli-compile-keymap; the judge is /usr/lib/xkbcommon/xkbcli-how-to-type.

Usage: validate.py <workdir> <receipt-dir>
"""
import json
import os
import subprocess
import sys

COMPILE = "/usr/lib/xkbcommon/xkbcli-compile-keymap"
JUDGE = "/usr/lib/xkbcommon/xkbcli-how-to-type"
TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mado-keysym.py")

# (layout, variant, options, model)
MATRIX = [
    ("us", None, None, None),
    ("us", "intl", None, None),
    ("us", "dvorak", None, None),
    ("us", "colemak", None, None),
    ("us", "altgr-intl", None, None),
    ("br", None, None, None),
    ("br", "nodeadkeys", None, None),
    ("br", "nativo", None, None),
    ("de", None, None, None),
    ("de", "neo", None, None),
    ("de", "nodeadkeys", None, None),
    ("de", "T3", None, None),
    ("fr", None, None, None),
    ("fr", "oss", None, None),
    ("fr", "bepo", None, None),
    ("fr", "latin9", None, None),
    ("gb", None, None, None),
    ("gb", "intl", None, None),
    ("es", None, None, None),
    ("es", "nodeadkeys", None, None),
    ("es", "winkeys", None, None),
    ("it", None, None, None),
    ("pt", None, None, None),
    ("pt", "nodeadkeys", None, None),
    ("ru", None, None, None),
    ("ru", "phonetic", None, None),
    ("ru", "typewriter", None, None),
    ("ua", None, None, None),
    ("gr", None, None, None),
    ("gr", "polytonic", None, None),
    ("pl", None, None, None),
    ("cz", "qwerty", None, None),
    ("tr", None, None, None),
    ("jp", None, None, None),
    ("kr", None, None, None),
    ("in", None, None, None),
    ("ir", None, None, None),
    ("ca", "multix", None, None),
    ("ch", "fr", None, None),
    ("ch", "de", None, None),
    ("no", None, None, None),
    ("se", None, None, None),
    ("fi", None, None, None),
    ("nl", None, None, None),
    ("dk", None, None, None),
    ("hu", None, None, None),
    ("us,br", None, "grp:alt_shift_toggle", None),
    ("us,ru", None, "grp:ctrl_shift_toggle", None),
    ("de,fr", None, "grp:alt_shift_toggle", None),
    ("us,ru,de", None, "grp:alt_shift_toggle", None),
    ("br", None, "compose:caps", None),
    ("br", None, "compose:caps,lv3:ralt_switch", None),
    ("us", None, "lv3:ralt_switch_multikey", None),
    ("de", None, "lv5:caps_switch_lock", None),
    ("us", None, "caps:escape", None),
    ("us", None, "ctrl:swapcaps", None),
    ("us", None, "keypad:pointerkeys", None),
    ("us", None, "compose:menu", None),
    ("us", None, "altwin:swap_alt_win", None),
    ("us", "intl", "lv3:lalt_switch", None),
    ("fr", None, "lv5:lsgt_switch_lock", None),
    ("us", None, None, "pc105"),
    ("us", None, None, "pc104"),
    ("us", None, None, "evdev"),
    ("ru", None, "grp:win_space_toggle", None),
    ("gr", None, "lv3:switch", None),
    ("jp", None, "kana:ligature", None),
    ("us", None, "euv:EuroSign", None),
    ("gb", None, "numpad:mac", None),
]

KEYSYMS = """Escape Return Tab BackSpace space slash question q Q a A z Z e E 1 2 exclam at
numbersign dollar percent dead_diaeresis dead_acute dead_grave dead_circumflex eacute Eacute
adiaeresis Cyrillic_a Cyrillic_A Cyrillic_ya U00E9 U0104 Aogonek 0x2f 0x26 47 0xff0d NoSymbol
nosuchsym XF86AudioMute XF86_MonBrightnessUp XF86_Switch_VT_1 Menu Multi_key ISO_Level3_Shift
ISO_Level5_Shift ISO_Next_Group ISO_First_Group KP_1 KP_7 KP_Enter KP_Home KP_Begin KP_End Left
Right Up Down Home End Prior Next Insert Delete Pause Scroll_Lock Num_Lock Caps_Lock Hyper_L Super_L
Super_R Meta_L Alt_L Alt_R Control_L Control_R Shift_L Shift_R Mode_switch ISO_Group_Shift EuroSign
sterling yen tslash Tslash oslash Oslash thorn THORN section plusminus multiplication division
masculine degree mu Greek_alpha Greek_ALPHA Ukrainian_i U0051 0x1008FF13 65 0x41 U+0041 XF86AudioPlay
dead_stroke ae AE ssharp U1E9E 0x01000100""".split()


def clean_env(home, cache):
    return {
        "PATH": "/usr/bin",
        "HOME": home,
        "XDG_CONFIG_HOME": os.path.join(home, ".config"),
        "XDG_CACHE_HOME": cache,
        "XDG_DATA_HOME": os.path.join(home, ".local", "share"),
        "LC_ALL": "C",
    }


def main():
    work = sys.argv[1]
    receipts = sys.argv[2]
    home = os.path.join(work, "home")
    cache = os.path.join(work, "cache")
    os.makedirs(home, exist_ok=True)
    os.makedirs(cache, exist_ok=True)
    os.makedirs(os.path.join(work, "k"), exist_ok=True)
    env = clean_env(home, cache)
    tool_env = {
        "PATH": "/usr/bin",
        "HOME": home,
        "XDG_CONFIG_HOME": env["XDG_CONFIG_HOME"],
        "XDG_CACHE_HOME": cache,
        "TMPDIR": os.path.join(work, "tmp"),
    }
    os.makedirs(tool_env["TMPDIR"], exist_ok=True)

    lines = []
    agreed = 0
    compared = 0
    compile_failures = []
    disagreements = []
    checked_keymaps = 0

    for number, (layout, variant, options, model) in enumerate(MATRIX):
        path = os.path.join(work, "k", "%03d.kmap" % number)
        command = [COMPILE, "--layout", layout]
        if variant:
            command += ["--variant", variant]
        if options:
            command += ["--options", options]
        if model:
            command += ["--model", model]
        with open(path, "wb") as handle:
            result = subprocess.run(command, stdout=handle, stderr=subprocess.PIPE, env=env)
        rmlvo = "%s/%s/%s/%s" % (layout, variant or "-", options or "-", model or "-")
        if result.returncode != 0:
            compile_failures.append("%s rc=%d %s" % (
                rmlvo, result.returncode,
                result.stderr.decode("utf-8", "replace").splitlines()[:1]))
            continue
        checked_keymaps += 1

        for keysym in KEYSYMS:
            judge = subprocess.run(
                [JUDGE, "--keymap=" + path, "--disable-compose", "--keysym", keysym],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            ours = subprocess.run(
                [sys.executable, "-I", TOOL, "how-to-type", "--keymap", path,
                 "--disable-compose", "--keysym", keysym],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=tool_env)
            compared += 1
            same = (judge.stdout == ours.stdout and judge.returncode == ours.returncode)
            if same:
                agreed += 1
            else:
                disagreements.append((rmlvo, keysym, judge.returncode, ours.returncode,
                                      judge.stdout, ours.stdout, ours.stderr))
            lines.append("%-40s %-20s judge_rc=%d ours_rc=%d %s" % (
                rmlvo, keysym, judge.returncode, ours.returncode,
                "ok" if same else "DIFF"))

    import hashlib
    tool_sha = hashlib.sha256(open(TOOL, "rb").read()).hexdigest()
    with open(os.path.join(receipts, "agree.txt"), "w", encoding="utf-8") as handle:
        handle.write("# ours == the pinned judge, per (compiled keymap, keysym)\n")
        handle.write("# tool mado-keysym.py sha256 %s bytes %d\n"
                     % (tool_sha, os.path.getsize(TOOL)))
        handle.write("# python %s\n" % sys.version.split()[0])
        handle.write("# compile: env -i PATH=/usr/bin HOME=<scratch> XDG_CONFIG_HOME=<scratch>\n")
        handle.write("#          %s --layout L [--variant V] [--options O] [--model M]\n" % COMPILE)
        handle.write("# judge:   %s --keymap=FILE --disable-compose --keysym ARG\n" % JUDGE)
        handle.write("# ours:    python3 -I mado-keysym.py how-to-type --keymap FILE "
                     "--disable-compose --keysym ARG\n")
        handle.write("# keymaps=%d pairs=%d agree=%d\n" % (checked_keymaps, compared, agreed))
        for line in lines:
            handle.write(line + "\n")

    print(json.dumps({
        "keymaps": checked_keymaps,
        "pairs": compared,
        "agree": agreed,
        "compile_failures": compile_failures,
        "disagreement_count": len(disagreements),
    }, indent=2))

    for rmlvo, keysym, judge_rc, ours_rc, judge_out, ours_out, ours_err in disagreements[:25]:
        print("DIFF", rmlvo, keysym, "judge_rc", judge_rc, "ours_rc", ours_rc)
        print("  judge:", judge_out.decode("utf-8", "replace").splitlines()[:8])
        print("  ours :", ours_out.decode("utf-8", "replace").splitlines()[:8])
        if ours_err:
            print("  stderr:", ours_err.decode("utf-8", "replace").strip().splitlines()[:3])
    return 0 if not disagreements else 1


if __name__ == "__main__":
    sys.exit(main())
