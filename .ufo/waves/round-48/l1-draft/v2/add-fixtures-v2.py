#!/usr/bin/env python3
"""L1 (attempt 3), registration v2: measure the B2 warm fixtures (w2/RevC1Counter: --print-content on a hit whose
cached entry path is LIVE and differs from the cold selection) from the pinned resolver - three identical runs through
the v2 counter's own prepare/oracle_side - and write c1-r48-fixtures-v2.json = the 204 v1 fixtures unchanged + these.
Usage: add-fixtures-v2.py WORK"""
import importlib.util
import json
import os
import random
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("c48v2", os.path.join(HERE, "c1-r48-terminal-cache-v2.py"))
c48 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c48)

MT = c48.PINNED_MTIME
UAPP = "home/.local/share/applications/"
VAPP = "usr/share/applications/"
LIST = "home/.config/hyprland-xdg-terminals.list"


def env(desk="Hyprland"):
    return {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
            "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share", "XDG_CURRENT_DESKTOP": desk}


def entry(cmd):
    return "[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=%s\n" % cmd


def files(app):
    return {LIST: "alpha.desktop\n", app + "alpha.desktop": entry("alpha --a"), app + "bravo.desktop": entry("bravo --b")}


# Same-length list edit alpha -> bravo under the re-pinned mtime: gen_hash is unchanged, so the warm run trusts the
# cached (live) alpha entry while a cold run selects bravo.
EDIT = {"files": {LIST: "bravo.desktop\n"}}


def base(cid, cls, args, files_, execs, after=None, links=None, prime=True, why=""):
    c = {"id": cid, "class": cls, "env": env(), "files": files_, "exec": execs, "args": args, "mtime": MT,
         "expect": {"rc": -1, "stdout": ""}, "meta": {"note": "registration v2: " + why}}
    if prime:
        c["prime"] = {"args": ["--print-cmd"]}
    if after:
        c["after"] = after
    if links:
        c["links"] = links
    return c


B2 = "w2/RevC1Counter B2 - live cached path, content differs from cold"
AB = ["bin/alpha", "bin/bravo"]
CASES = [
    base("L1-11-live-path-content", "WARM-DIFFERS", ["--print-content"], files(UAPP), AB, EDIT, why=B2),
    base("L1-12-live-path-id-content", "WARM-DIFFERS", ["--print-id", "--print-content"], files(UAPP), AB, EDIT, why=B2),
    base("L1-13-live-path-content-cmd", "WARM-DIFFERS", ["--print-content", "--print-cmd"], files(UAPP), AB, EDIT, why=B2),
    base("L1-14-live-path-path-content", "WARM-DIFFERS", ["--print-path", "--print-content"], files(UAPP), AB, EDIT, why=B2),
    base("L1-15-live-path-content-vendor", "WARM-DIFFERS", ["--print-content"], files(VAPP), AB, EDIT, why=B2),
    # The cache's path line re-pointed at another LIVE entry: content follows the cached path, the cold run does not.
    base("L1-16-cached-other-live-path-content", "WARM-DIFFERS", ["--print-content"], files(UAPP), AB,
         {"cache_lines": {"3": "$ROOT/" + UAPP + "bravo.desktop"}}, why=B2),
]

# w2/MutC1Tool G1: `command -v` is an executability test - a command that exists without +x is not a command.
_g1 = json.load(open(os.path.join(HERE, "..", "..", "w2", "MutC1Tool", "probe", "proposed-fixture-W-GAP-CMDV-NONEXEC.json")))
_g1 = {k: v for k, v in _g1.items() if k in ("after", "args", "class", "env", "exec", "files", "mtime", "prime")}
_g1.update({"id": "L1-17-cached-cmd-not-executable", "expect": {"rc": -1, "stdout": ""},
            "meta": {"note": "registration v2: w2/MutC1Tool G1 (proposed-fixture-W-GAP-CMDV-NONEXEC.json, re-measured)"}})
G1 = "w2/MutC1Tool G1 - Exec[0] exists without the executable bit"
FK = {LIST: "foot.desktop\nkitty.desktop\n", VAPP + "foot.desktop": entry("foot"), VAPP + "kitty.desktop": entry("kitty")}
CASES += [
    _g1,
    base("L1-18-cold-exec0-not-executable", "EXEC-MODE", ["--print-cmd"], dict(FK), ["bin/foot", "bin/kitty"],
         {"modes": {"bin/foot": 420}}, prime=False, why=G1),
]

# w2/RevC1Cache F1 (multi-line cached command, LF reconstruction) and F2 (unreadable cache -> invalid, not absent).
F1 = "w2/RevC1Cache F1 - hash-valid cache whose command spans two lines"
ML = {LIST: "foot.desktop\n", VAPP + "foot.desktop": entry('foot "a\\nb"')}
CASES += [
    base("L1-19-multiline-cmd-print", "WARM-SAME", ["--print-cmd"], dict(ML), ["bin/foot"], why=F1),
    base("L1-20-multiline-cmd-test", "WARM-SAME", ["--test"], dict(ML), ["bin/foot"], why=F1),
    base("L1-21-unreadable-cache", "MALFORMED", ["--print-cmd"], {LIST: "foot.desktop\n", UAPP + "foot.desktop": entry("foot")},
         ["bin/foot"], {"modes": {".rw/cache/xdg-terminal-exec": 0}},
         why="w2/RevC1Cache F2 - mode-000 cache: -f true, read fails, invalid cache data"),
]

# w2/RevC1Ls: `ls -LRl` dereferences symlinks; schema v2 `links` makes trees a no-dereference tool hashes wrongly.
LS = "w2/RevC1Ls - symlinks under a hashed operand (ls -L)"
ST = "store/"
CASES += [
    base("L1-22-link-operand-dir", "WARM-SAME", ["--print-cmd"],
         {LIST: "foot.desktop\n", ST + "apps/foot.desktop": entry("foot --a")}, ["bin/foot"],
         {"files": {ST + "apps/foot.desktop": entry("foot --bb")}}, links={UAPP: "$ROOT/" + ST + "apps"}, why=LS),
    base("L1-23-link-entry-file", "WARM-SAME", ["--print-cmd"],
         {LIST: "foot.desktop\n", ST + "foot.desktop": entry("foot --a")}, ["bin/foot"],
         {"files": {ST + "foot.desktop": entry("foot --bb")}}, links={UAPP + "foot.desktop": "$ROOT/" + ST + "foot.desktop"},
         why=LS),
    base("L1-24-link-dangling-entry", "WARM-SAME", ["--print-cmd"],
         {LIST: "foot.desktop\n", UAPP + "foot.desktop": entry("foot")}, ["bin/foot"],
         links={UAPP + "ghost.desktop": "$ROOT/nowhere.desktop"}, why=LS),
    base("L1-25-link-dangling-revived", "WARM-SAME", ["--print-cmd"],
         {LIST: "ghost.desktop\nfoot.desktop\n", UAPP + "foot.desktop": entry("foot")}, ["bin/foot", "bin/ghost"],
         {"files": {ST + "ghost.desktop": entry("ghost")}}, links={UAPP + "ghost.desktop": "$ROOT/" + ST + "ghost.desktop"},
         why=LS),
    base("L1-26-link-chain", "WARM-SAME", ["--print-cmd"],
         {LIST: "foot.desktop\n", ST + "real.desktop": entry("foot --a")}, ["bin/foot"],
         {"files": {ST + "real.desktop": entry("foot --bb")}},
         links={UAPP + "foot.desktop": "$ROOT/" + ST + "l1", ST + "l1": "$ROOT/" + ST + "real.desktop"}, why=LS),
    base("L1-27-link-sibling-twins", "WARM-SAME", ["--print-id", "--print-cmd"],
         {LIST: "b.desktop\n", ST + "t.desktop": entry("foot --a")}, ["bin/foot"],
         {"files": {ST + "t.desktop": entry("foot --bb")}},
         links={UAPP + "a.desktop": "$ROOT/" + ST + "t.desktop", UAPP + "b.desktop": "$ROOT/" + ST + "t.desktop"}, why=LS),
    base("L1-28-link-data-home", "WARM-SAME", ["--print-cmd"],
         {LIST: "foot.desktop\n", "sharestore/applications/foot.desktop": entry("foot --a")}, ["bin/foot"],
         {"files": {"sharestore/applications/foot.desktop": entry("foot --bb")}},
         links={"home/.local/share": "$ROOT/sharestore"}, why=LS),
]


# w2/CritDataCompleteness C1-A/B/C and w2/RevC1Explain F2.
FOOT = {LIST: "foot.desktop\n", UAPP + "foot.desktop": entry("foot --a")}
CD = "w2/CritDataCompleteness"
CASES += [
    dict(base("L1-29-default-cache-hit", "WARM-SAME", ["--print-cmd"], dict(FOOT), ["bin/foot"],
              why=CD + " C1-A - a primed cache at the default $HOME/.cache location"), default_cache=True),
    dict(base("L1-30-default-cache-differs", "WARM-DIFFERS", ["--print-cmd"], dict(FOOT), ["bin/foot", "bin/feot"],
              {"files": {UAPP + "foot.desktop": entry("feot --a")}},
              why=CD + " C1-A - same-size edit under a default-location cache"), default_cache=True),
    base("L1-31-cache-enabled-empty", "MALFORMED", ["--print-cmd"], dict(FOOT), ["bin/foot"],
         {"env": {"XTE_CACHE_ENABLED": ""}}, why=CD + " C1-B - XTE_CACHE_ENABLED='' disables the cache"),
    base("L1-32-cache-path-is-dir", "MALFORMED", ["--print-cmd"], dict(FOOT), ["bin/foot"],
         {"files": {".rw/cache/xdg-terminal-exec/": ""}}, prime=False,
         why=CD + " C1-C - a directory at the cache path fails -f: absent"),
    base("L1-33-empty-cmd-word", "WARM-DIFFERS", ["--print-cmd"], dict(FOOT), ["bin/foot"],
         {"cache_lines": {"11": "foot\x1f\x1f--a\x1eEND_OF_EXEC_USEP"}},
         why="w2/RevC1Explain F2 - an empty word in the cached command is printed"),
    base("L1-34-newline-first-cmd-word", "WARM-DIFFERS", ["--print-cmd"], dict(FOOT), ["bin/foot"],
         {"cache_lines": {"11": "fo\not\x1f--a\x1eEND_OF_EXEC_USEP"}},
         why="w2/RevC1Explain F3 - a newline inside the FIRST cached command word (explain writes it as \\n)"),
]


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
    work = tempfile.mkdtemp(dir=sys.argv[1], prefix="addfx2-")
    box = c48.Box(work)
    fx = json.load(open(os.path.join(HERE, "..", "c1-r48-fixtures.json")))
    assert len(fx) == 204, len(fx)
    for case in CASES:
        cid, cls = case["id"], case["class"]
        runs = [measure(box, case, k) for k in range(3)]
        if len({json.dumps(r) for r in runs}) != 1:
            print("UNSTABLE %s %r" % (cid, runs))
            continue
        (rc, out), state, (crc, cout) = runs[0]
        case["expect"] = {"rc": rc, "stdout": out}
        case["state"] = state
        if "prime" in case or "cache" in case:
            case["cold"] = {"rc": crc, "stdout": cout}
        same = [rc, out] == [crc, cout]
        if (cls == "WARM-DIFFERS" and same) or (cls == "WARM-SAME" and not same):
            print("REFUSED %s class=%s state=%s %r" % (cid, cls, state, runs[0]))
            continue
        print("ADD %s class=%s state=%s rc=%d out=%r cold=%r" % (cid, cls, state, rc, out[:60], cout[:60]))
        fx.append(case)
    with open(os.path.join(HERE, "c1-r48-fixtures-v2.json"), "w") as fh:
        json.dump(fx, fh, indent=1, ensure_ascii=False, sort_keys=True)
        fh.write("\n")
    shutil.rmtree(work, ignore_errors=True)
    print("fixtures=%d" % len(fx))


main()
