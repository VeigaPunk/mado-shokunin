#!/usr/bin/env python3
"""Does the frozen counter's no-write guard exist, and does it catch the writes-cache control?

Builds two identical trees and runs the frozen control tool `writes-cache.py` on each through the frozen
counter's own sandbox:
  A. the counter's own Box (tool tree's .rw READ-ONLY, clause i as frozen)
  B. a Box whose prefix() binds the tool tree's .rw writable (the `i-no-write-tripwire` mutant's shape)
and reports, per run: exit status, stdout equality with the control's expected output, whether the cache file
appeared, and the counter's own trip list.  Also runs the data candidate on both for the baseline row.
Nothing in the lane is written; scratch is under the seat root.
"""
import importlib.util
import os
import shutil
import sys
import tempfile

S = "/fast/scratch/hyaku/mado-r48/MutC1Counter"
L = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(L, "quality/counters/c1-r48-terminal-cache.py")
CAND = os.path.join(L, ".ufo/waves/round-48/l1-draft/mado-terminal.py")
WRITES = os.path.join(L, ".ufo/waves/round-48/w1/ExecControlsC1/controls/writes-cache.py")
TOOLS = {"candidate": CAND, "writes-cache": WRITES}


def load():
    spec = importlib.util.spec_from_file_location("c1r48", COUNTER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CASE = {
    "id": "probe-write", "class": "WARM-ABSENT", "expect": {"rc": 0, "stdout": ""},
    "env": {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
            "XDG_DATA_HOME": "$ROOT/home/.local/share",
            "XDG_DATA_DIRS": "$ROOT/opt/share:$ROOT/usr/share", "XDG_CURRENT_DESKTOP": "Hyprland"},
    "files": {"usr/share/applications/foot.desktop":
              "[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=foot\nName=foot\n",
              "home/.config/xdg-terminals.list": "foot.desktop\n"},
    "exec": ["bin/foot"], "mtime": 1600000000, "args": ["--print-cmd"],
}


class RWBox(object):
    """A Box subclass whose tool tree .rw is writable (the no-write tripwire removed)."""


def run(mod, tool, writable, work, tag):
    toolpath = os.path.join(work, "tool-" + tag + ".py")
    shutil.copy(TOOLS[tool], toolpath)
    box = mod.Box(work, toolpath)
    if writable:
        orig = box.prefix

        def prefix(root, otool, default_cache, _orig=orig):
            a = _orig(root, otool, default_cache)
            out = []
            i = 0
            while i < len(a):
                if a[i] in ("--ro-bind", "--bind") and i + 2 < len(a) and a[i + 2].endswith("/.rw") \
                        and a[i + 1].endswith("/.rw"):
                    out += ["--bind", a[i + 1], a[i + 2]]
                    i += 3
                    continue
                out.append(a[i])
                i += 1
            return out

        box.prefix = prefix
    root = os.path.join(work, "t-" + tag)
    mod.prepare(box, root, CASE, "C.UTF-8")
    env = mod.case_env(CASE, root, "C.UTF-8", "scored")
    rc, out, err = box.run(root, env, True, ["print"] + CASE["args"])
    cache = os.path.join(root, ".rw", "cache", "xdg-terminal-exec")
    return {"tool": tool, "rw": "rw" if writable else "ro", "rc": rc, "stdout": out,
            "cache_exists": os.path.exists(cache), "cache_bytes": os.path.getsize(cache) if os.path.exists(cache) else 0,
            "trips": list(box.trips)}


def main():
    mod = load()
    work = tempfile.mkdtemp(dir=S, prefix="work/probe-write-")
    rows = []
    try:
        for tool in ("candidate", "writes-cache"):
            for writable in (False, True):
                rows.append(run(mod, tool, writable, work, "%s-%s" % (tool, "rw" if writable else "ro")))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    for r in rows:
        print("tool=%-12s rw=%-2s rc=%d stdout=%r cache_exists=%s cache_bytes=%d trips=%r" % (
            r["tool"], r["rw"], r["rc"], r["stdout"], r["cache_exists"], r["cache_bytes"], r["trips"]))


if __name__ == "__main__":
    sys.exit(main())
