#!/usr/bin/env python3
"""strict_probe.py - seat-local receipt: what a case needs before a prime can write a cache at all.

A list file holding `/execarg_strict` (xdg-terminal-exec :394) makes the resolver skip every desktop entry that has
no TerminalArgExec (x:1091 -> get_default_execarg x:1113, whose `-e` default applies in compat mode only). An injected
entry without that key therefore selects nothing, the resolver exits 1 before the save point (x:1457), and the prime
writes no cache: the case cannot be a warm case at all.

Builds two otherwise identical trees, primes both through the wrapper (/oracle/prime.sh, see warm_judge.py), 3 runs
each, and writes receipts/prime-strict-mode.txt.
"""
import os
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_warm  # noqa: E402
import warm_judge as W  # noqa: E402

C1 = gen_warm.R47
WORK = sys.argv[1] if len(sys.argv) > 1 else "/fast/scratch/hyaku/mado-r48/ExecGenWarm/strict"
RECEIPTS = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "receipts")

WITHOUT = ("[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=foot\n")
WITH = WITHOUT.replace("Exec=foot\n", "TerminalArgExec=-e\nExec=foot\n")


def case(entry_text, list_text="/execarg_strict\nfoot.desktop\n"):
    return {"id": "strict", "class": "probe",
            "env": {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
                    "XDG_DATA_HOME": "$ROOT/home/.local/share",
                    "XDG_DATA_DIRS": "$ROOT/opt/share:$ROOT/usr/share",
                    "XDG_CURRENT_DESKTOP": "Hyprland"},
            "files": {"home/.config/xdg-terminals.list": list_text,
                      "usr/share/applications/foot.desktop": entry_text},
            "exec": ["bin/foot"], "args": ["--print-cmd"], "mtime": gen_warm.MT_ANCHOR,
            "prime": {"args": ["--print-cmd"]}}


def main():
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(RECEIPTS, exist_ok=True)
    box = W.Box(WORK)
    out = []
    variants = (("strict list, entry WITHOUT TerminalArgExec", WITHOUT, "/execarg_strict\nfoot.desktop\n"),
                ("strict list, entry WITH TerminalArgExec=-e", WITH, "/execarg_strict\nfoot.desktop\n"),
                ("compat list WITH /disable_cache, entry WITH TerminalArgExec=-e", WITH,
                 "/disable_cache\nfoot.desktop\n"))
    for label, text, list_text in variants:
        seen = []
        for _ in range(3):
            root, d, pout, _c = W.build(box, case(text, list_text), True)
            try:
                data = W.cache_bytes(root)
                state = ("absent" if not data else
                         "complete" if data.endswith(W.SENTINEL.encode()) else "partial")
                seen.append("stdout=%r/rc=%d/cache=%s" % ((pout[1][:20] if pout else ""), (pout[0] if pout else -1),
                                                          state))
            finally:
                shutil.rmtree(d, ignore_errors=True)
        out.append("%s: %s" % (label, "; ".join(seen)))
    with open(os.path.join(RECEIPTS, "prime-requirements.txt"), "w") as fh:
        fh.write("list file: home/.config/xdg-terminals.list = '/execarg_strict\\nfoot.desktop\\n'\n"
                 "pin: %s sha256=%s\n"
                 "3 prime runs per variant, wrapper prime, round-47 sandbox argv.\n\n" % (
                     os.path.realpath(C1.PIN_PATH),
                     __import__("hashlib").sha256(open(C1.PIN_PATH, "rb").read()).hexdigest()))
        fh.write("\n".join(out) + "\n")
        fh.write("\nmechanism 1: /execarg_strict x:394 -> strict mode; an entry without TerminalArgExec is skipped\n"
                 "x:1091 (get_default_execarg x:1113 supplies '-e' only in compat mode), so nothing is selected and\n"
                 "the resolver exits 1 before save_cache x:1457. gen_warm.ENTRY therefore carries "
                 "TerminalArgExec=-e.\n"
                 "mechanism 2: /disable_cache x:380 sets XTE__CACHE_ENABLED=false, so save_cache x:300 takes its\n"
                 "disable branch and removes the cache file: a tree carrying that line cannot be primed.\n"
                 "gen_warm strips both cache directives from the base list files (the directive families are\n"
                 "generated explicitly: a same-size content swap while the cache is valid, and XTE_CACHE_ENABLED\n"
                 "in the environment).\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
