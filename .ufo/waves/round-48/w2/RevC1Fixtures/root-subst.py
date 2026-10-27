#!/usr/bin/env python3
"""RevC1Fixtures (round 48 w2): the `$ROOT` substitution premise of schema v2 and the counter's norm().

Static: every occurrence of `$ROOT` in the frozen fixture file, by context (path prefix vs mid-token), and every
absolute path that would betray a baked scratch root. Dynamic: cases whose `$ROOT` sits in a colon list twice, in a
non-path position, as a whole value, and in a lying cached path - each measured against the pin and normalized with
the counter's own rule, in both variants (different root depth + lang).
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
    spec = importlib.util.spec_from_file_location("c48r", COUNTER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def leaves(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, path + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, path + "/%d" % i)
    else:
        yield path, o


def scan(fx):
    tot = ctx = 0
    mid = []
    baked = []
    for f in fx:
        for fld, v in f.items():
            for path, leaf in leaves(v, fld):
                if not isinstance(leaf, str):
                    continue
                if "/fast/" in leaf or LANE in leaf:
                    baked.append((f["id"], path, leaf[:80]))
                n = leaf.count("$ROOT")
                tot += n
                i = 0
                for _ in range(n):
                    i = leaf.index("$ROOT", i)
                    nxt = leaf[i + 5:i + 6]
                    if path.endswith("expect/stdout") or path.endswith("cold/stdout"):
                        if path.split("/")[0] == "expect" and nxt != "/":
                            mid.append((f["id"], path, leaf[max(0, i - 20):i + 20]))
                    elif nxt != "/":
                        mid.append((f["id"], path, leaf[max(0, i - 20):i + 20]))
                    if nxt == "/":
                        ctx += 1
                    i += 5
    return tot, ctx, mid, baked


def case(args, files, env, prime=True, cache=None):
    c = {"id": "ROOTSUB", "class": "WARM-SAME", "env": env, "files": files, "exec": ["bin/foot"],
         "args": args, "expect": {"rc": 0, "stdout": ""}, "mtime": 1600000000}
    if cache is not None:
        c["cache"] = cache
    elif prime:
        c["prime"] = {"args": ["--print-cmd"]}
    return c


def measure(c48, box, c, variant, rng):
    base, lang = c48.variant_roots(box, variant, rng)
    try:
        ro = os.path.join(base, "o", "r")
        c48.prepare(box, ro, c, lang)
        warm, state = c48.oracle_side(box, c, ro, lang)
    finally:
        shutil.rmtree(base.split("/deep/")[0] if "/deep/" in base else base, ignore_errors=True)
    return warm, state, lang


def main():
    work, out = sys.argv[1], sys.argv[2]
    c48 = load()
    fx = json.load(open(WARM))
    tot, ctx, mid, baked = scan(fx)
    esc = [(f["id"], p, l[:60]) for f in fx for p2, l in leaves(f) if isinstance(l, str)
           for p in [p2] if "$$ROOT" in l]
    res = {"static": {"escaped_double_root": esc, "$ROOT_occurrences": tot, "path_prefix": ctx,
                      "non_path": mid, "baked_absolute": baked,
                      "fixtures_with_root": sum(1 for f in fx if any("$ROOT" in l for _p, l in leaves(f)
                                                                      if isinstance(l, str)))},
           "dynamic": []}
    print("static: occurrences=%d path_prefix=%d non_path=%d fixtures=%d baked=%d" % (
        tot, ctx, len(mid), res["static"]["fixtures_with_root"], len(baked)))
    for m in mid:
        print("  NON-PATH", m)
    for b in baked:
        print("  BAKED", b)

    os.makedirs(work, exist_ok=True)
    wd = os.path.join(work, "rootsub-%d" % os.getpid())
    os.makedirs(wd)
    box = c48.Box(wd)
    rng = random.Random(4849)
    E = {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
         "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share",
         "XDG_CURRENT_DESKTOP": "Hyprland"}
    cases = {
        "colon-list-two-roots": case(["--print-path"], {APP + "foot.desktop": ENTRY, LIST: "foot.desktop\n"},
                                     dict(E, XDG_DATA_DIRS="$ROOT/usr/share:$ROOT/usr/local/share")),
        "two-roots-same-dir": case(["--print-path", "--print-id"],
                                   {"home/.config/hyprland-xdg-terminals.list": "$ROOT/foot.desktop\n",
                                    "home/.config/foot.desktop": ENTRY}, E),
        "exec-word-with-root": case(["--print-cmd"],
                                    {APP + "foot.desktop": ENTRY.replace("foot --a", "foot --$ROOT/x"),
                                     LIST: "foot.desktop\n"}, E),
        "root-as-whole-cache-line": case(["--print-path"], {APP + "foot.desktop": ENTRY},
                                         E, prime=False,
                                         cache="00000000000000000000000000000000\nfoot\n$ROOT\nfoot.desktop\n\n"
                                               "-e\n\n\n\n\nfoot\x1f--a\x1eEND_OF_EXEC_USEP\n"),
        "double-root-token": case(["--print-cmd"], {APP + "foot.desktop": ENTRY, LIST: "foot.desktop\n"},
                                  dict(E, XDG_DATA_DIRS="$ROOT$ROOT/usr/share")),
        "escaped-double-root": case(["--print-cmd"],
                                    {APP + "foot.desktop": ENTRY.replace("foot --a", "foot --$$ROOT/x"),
                                     LIST: "foot.desktop\n"}, E),
    }
    try:
        for name, c in cases.items():
            for variant in ("A", "B"):
                warm, state, lang = measure(c48, box, c, variant, rng)
                nroot = warm[1].count("$ROOT")
                raw_abs = "/fx-" in warm[1] or "/job-" in warm[1]
                free = c48.norm(warm[0], warm[1], os.path.join(wd, "ZZ"))
                row = {"case": name, "variant": variant, "rc": warm[0], "state": state, "lang": lang,
                       "stdout": warm[1][:160], "root_tokens": nroot, "unnormalized_abs": raw_abs,
                       "norm_unchanged": free == warm}
                res["dynamic"].append(row)
                print("%-24s %s rc=%d state=%-8s roots=%d abs=%s %r" % (
                    name, variant, warm[0], state, nroot, raw_abs, warm[1][:100]))
    finally:
        shutil.rmtree(wd, ignore_errors=True)
    # the masking property, stated exactly: a literal `$ROOT` in stdout is indistinguishable from the case root
    root = "/fast/scratch/x/r"
    res["masking"] = {
        "tool_prints_root": c48.norm(0, root + "/foot.desktop\n", root)[1],
        "oracle_prints_literal": c48.norm(0, "$ROOT/foot.desktop\n", root)[1],
        "identical": c48.norm(0, root + "/foot.desktop\n", root) == c48.norm(0, "$ROOT/foot.desktop\n", root),
    }
    print("masking: %s" % json.dumps(res["masking"], sort_keys=True))
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
