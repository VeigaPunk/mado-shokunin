#!/usr/bin/env python3
"""RevC1Fixtures (round 48 w2): the resolver's cache line-limit boundary, 49 vs 50, on a real primed cache.

The pin (`read_cache`, :217-298) increments `xte__line_num` and returns 1 with `reached cache line limit (50)` when
the counter reaches 50 before the terminator case; line 49 is still parsed. This measures, with the frozen counter's
own sandbox, whether a cache whose terminator sits on line 49 is accepted (hash compared -> hit when the hash is the
primed one) and whether the same cache one line longer is rejected. It then shifts the two frozen boundary fixtures
(M-16 LINE49, M-17 LINE50) by one line each way to show they sit exactly on the boundary.
"""
import importlib.util
import json
import os
import random
import shutil
import sys

sys.dont_write_bytecode = True
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r48-terminal-cache.py")
WARM = os.path.join(LANE, "quality", "counters", "c1-r48-fixtures.json")
APP = "home/.local/share/applications/"
LIST = "home/.config/hyprland-xdg-terminals.list"
ENTRY = "[Desktop Entry]\nType=Application\nName=Terminal\nCategories=System;TerminalEmulator;\nTerminalArgExec=-e\nExec=foot --a\n"


def load():
    spec = importlib.util.spec_from_file_location("c48b", COUNTER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def base_case(c48):
    return {"id": "BOUND", "class": "WARM-SAME",
            "env": {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
                    "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share",
                    "XDG_CURRENT_DESKTOP": "Hyprland"},
            "files": {LIST: "foot.desktop\n", APP + "foot.desktop": ENTRY},
            "exec": ["bin/foot"], "args": ["--print-cmd"], "expect": {"rc": 0, "stdout": ""},
            "mtime": c48.PINNED_MTIME, "prime": {"args": ["--print-cmd"]}}


def oracle(box, c48, root, case, lang):
    env = c48.case_env(case, root, lang, "scored")
    env["XTE_DEBUG"] = "1"
    rc, out, err = box.run(root, env, False, [a.replace("$ROOT", root) for a in case["args"]],
                           default_cache=case.get("default_cache", False))
    marks = [l.split("D: ")[-1] for l in err.split("\n")
             if any(s in l for s in ("cache is actual", "cache is out-of-date", "invalid cache data",
                                     "reached cache line limit", "no cache data", "failed to get fresh hash",
                                     "got cache:"))]
    return rc, out.replace(root, "$ROOT"), c48.cache_state(err), marks


def write_cache(path, lines):
    with open(path, "wb") as fh:
        fh.write(("\n".join(lines) + "\n").encode())


def main():
    work = sys.argv[1]
    out = sys.argv[2]
    c48 = load()
    os.makedirs(work, exist_ok=True)
    wd = os.path.join(work, "bound-%d" % os.getpid())
    os.makedirs(wd)
    box = c48.Box(wd)
    rows = []
    try:
        # ---- part 1: a real primed cache, terminator moved along the 48/49/50 boundary
        case = base_case(c48)
        rng = random.Random(49)
        root = os.path.join(wd, "prime", "r")
        c48.prepare(box, root, case, "C.UTF-8")
        cp = c48.cache_host(root)
        primed = open(cp, "rb").read().decode("utf-8", "surrogateescape").rstrip("\n").split("\n")
        assert len(primed) == 11 and "END_OF_EXEC_USEP" in primed[-1], primed
        hdr, cmd = primed[:10], primed[10]
        cmd_noterm = cmd.replace(c48.CACHE_TERMINATOR, "")
        rc0, out0, st0, mk0 = oracle(box, c48, root, case, "C.UTF-8")
        rows.append({"variant": "primed-cache (terminator line 11)", "rc": rc0, "state": st0,
                     "stdout_head": out0.split("\n")[0][:40], "debug": mk0[-2:]})
        variants = []
        for pad, term in ((36, True), (37, True), (38, True), (39, True), (38, False), (39, False), (40, False)):
            body = hdr + ["j"] * pad + [cmd if term else cmd_noterm]
            variants.append(("term_line_%d%s" % (len(body), "" if term else "_no_terminator"), body))
        for name, body in variants:
            write_cache(cp, body)
            rc, tout, st, mk = oracle(box, c48, root, case, "C.UTF-8")
            rows.append({"variant": name, "lines": len(body), "rc": rc, "state": st,
                         "stdout_lines": len(tout.split("\n")), "debug": mk[-2:]})
            print("%-26s lines=%2d rc=%d state=%-8s debug=%r" % (name, len(body), rc, st, mk[-2:]))

        # ---- part 2: shift the two frozen boundary fixtures by one line each way
        byid = {f["id"]: f for f in json.load(open(WARM))}
        rng = random.Random(50)
        for fid in ("M-16", "M-17"):
            fx = byid[fid]
            lines = fx["cache"].rstrip("\n").split("\n")
            t = [i for i, l in enumerate(lines) if "END_OF_EXEC_USEP" in l]
            assert len(t) == 1
            idx = t[0]
            for delta in (-2, -1, 0, 1, 2):
                c2 = dict(fx)
                body = list(lines)
                if delta < 0:
                    del body[idx + delta:idx]          # remove padding lines before the terminator
                elif delta > 0:
                    body[idx:idx] = ["j"] * delta       # insert padding lines before the terminator
                c2["cache"] = "\n".join(body) + "\n"
                t2 = [i for i, l in enumerate(body) if "END_OF_EXEC_USEP" in l][0]
                r = os.path.join(wd, "%s-%+d" % (fid, delta), "r")
                c48.prepare(box, r, c2, "C.UTF-8")
                rc, tout, st, mk = oracle(box, c48, r, c2, "C.UTF-8")
                rows.append({"fixture": fid, "delta": delta, "term_line": t2 + 1, "rc": rc, "state": st,
                             "recorded_state": fx.get("state"), "debug": mk[-1:]})
                print("%-6s delta=%+d term_line=%2d rc=%d state=%-8s recorded=%s debug=%r" % (
                    fid, delta, t2 + 1, rc, st, fx.get("state"), mk[-1:]))
    finally:
        shutil.rmtree(wd, ignore_errors=True)
    with open(out, "w") as fh:
        json.dump(rows, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
