#!/usr/bin/env python3
"""L1: measure extra warm fixtures from the pinned resolver (3 identical runs, the counter's own prepare/oracle_side)
and append them to c1-r48-fixtures.json. Usage: add-fixtures.py WORK"""
import importlib.util
import json
import os
import random
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("c48", os.path.join(HERE, "c1-r48-terminal-cache.py"))
c48 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c48)

MT = c48.PINNED_MTIME
APP = "home/.local/share/applications/"
LIST = "home/.config/hyprland-xdg-terminals.list"


def env(desk="Hyprland"):
    return {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
            "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share", "XDG_CURRENT_DESKTOP": desk}


def entry(cmd, extra=""):
    return "[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=%s\n%s" % (cmd, extra)


FILES = {LIST: "foot.desktop\n", APP + "foot.desktop": entry("foot --a", "Actions=srv;\n[Desktop Action srv]\nExec=footclient\n")}
CASES = [
    ("L1-01-gone-path-content", "MALFORMED", ["--print-content"], {"cache_lines": {"3": "$ROOT/nope.desktop"}}, env()),
    ("L1-02-gone-path-id-content", "MALFORMED", ["--print-id", "--print-content"], {"cache_lines": {"3": "$ROOT/nope.desktop"}}, env()),
    ("L1-03-gone-path-content-cmd", "MALFORMED", ["--print-content", "--print-cmd"], {"cache_lines": {"3": "$ROOT/nope.desktop"}}, env()),
    ("L1-04-cached-test-mode", "WARM-DIFFERS", ["--test", "--", "top"], {"cache_sub": [["foot\x1f--a", "foot\x1f--b"]]}, env()),
    ("L1-05-cached-action-path", "WARM-DIFFERS", ["--print-id", "--print-path"], {"cache_lines": {"5": "srv"}}, env()),
    ("L1-06-desk-echo-n", "WARM-SAME", ["--print-cmd"], {}, env("-n")),
    ("L1-07-desk-echo-e", "WARM-SAME", ["--print-cmd"], {}, env("-eE")),
    ("L1-08-desk-backslash", "WARM-SAME", ["--print-cmd"], {}, env("a\\tb:Hyprland")),
    ("L1-09-desk-dash-only", "WARM-SAME", ["--print-cmd"], {}, env("-")),
    ("L1-10-desk-echo-n-edit", "WARM-DIFFERS", ["--print-cmd"], {"cache_sub": [["foot\x1f--a", "foot\x1f--b"]]}, env("-n")),
]


def build(cid, cls, args, after, e):
    c = {"id": cid, "class": cls, "env": e, "files": dict(FILES), "exec": ["bin/foot", "bin/footclient"],
         "args": args, "mtime": MT, "prime": {"args": ["--print-cmd"]}, "expect": {"rc": -1, "stdout": ""}}
    if after:
        c["after"] = dict(after)
    return c


def measure(box, case, seed):
    rng = random.Random(seed)
    base, lang = c48.variant_roots(box, "A", rng)
    ro, rc_ = os.path.join(base, "o", "r"), os.path.join(base, "c", "r")
    c48.prepare(box, ro, case, lang)
    warm, state = c48.oracle_side(box, case, ro, lang)
    c48.prepare(box, rc_, case, lang, cold=True)
    cold, _s = c48.oracle_side(box, case, rc_, lang)
    shutil.rmtree(base, ignore_errors=True)
    return warm, state, cold


def main():
    work = tempfile.mkdtemp(dir=sys.argv[1], prefix="addfx-")
    box = c48.Box(work)
    path = os.path.join(HERE, "c1-r48-fixtures.json")
    fx = [c for c in json.load(open(path)) if not c["id"].startswith("L1-")]
    for cid, cls, args, after, e in CASES:
        case = build(cid, cls, args, after, e)
        runs = [measure(box, case, k) for k in range(3)]
        if len({json.dumps(r) for r in runs}) != 1:
            print("UNSTABLE %s %r" % (cid, runs))
            continue
        (rc, out), state, (crc, cout) = runs[0]
        case["expect"] = {"rc": rc, "stdout": out}
        case["state"] = state
        case["cold"] = {"rc": crc, "stdout": cout}
        if cls == "WARM-DIFFERS" and [rc, out] == [crc, cout]:
            print("NOT-DIFFERING %s %r" % (cid, runs[0]))
            continue
        if cls == "WARM-SAME" and [rc, out] != [crc, cout]:
            case["class"] = "WARM-DIFFERS"
        print("ADD %s class=%s state=%s rc=%d out=%r cold=%r" % (cid, case["class"], state, rc, out[:80], cout[:60]))
        fx.append(case)
    with open(path, "w") as fh:
        json.dump(fx, fh, indent=1, ensure_ascii=False, sort_keys=True)
        fh.write("\n")
    shutil.rmtree(work, ignore_errors=True)
    print("fixtures=%d" % len(fx))


main()
