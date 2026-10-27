#!/usr/bin/env python3
"""ExecHomeUnset r48 driver: run the pinned xdg-terminal-exec and tools/mado-terminal.py side by side.

The sandbox is the round-47 C1 counter's own `Box` (imported read-only from the lane), so the pin sees exactly the
instrument's allowlist (7 externals, no /etc, no /home, no /usr/share of the host, XDG_CACHE_HOME under the case
root's writable .rw). Each fixture materializes one tree; the pin and the tool each get their own copy.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality/counters/c1-r47-terminal.py")
TOOL = os.path.join(LANE, "tools/mado-terminal.py")
SEAT = os.path.join(LANE, ".ufo/waves/round-48/w1/ExecHomeUnset")
SCRATCH = "/fast/scratch/hyaku/mado-r48/ExecHomeUnset"
TIMEOUT = 10


def load_counter():
    spec = importlib.util.spec_from_file_location("c1r47", COUNTER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ENTRY = "[Desktop Entry]\nType=Application\nName=Term\nCategories=TerminalEmulator;\nExec=$ROOT/bin/term\n"


def base_files(term_in="home/.local/share/applications"):
    return {
        "home/.config/xdg-terminals.list": "term.desktop\n",
        term_in + "/term.desktop": ENTRY,
    }


CASES = [
    dict(id="C0-baseline", files=base_files(), execs=["bin/term"], env={}, args=["--print-id"]),
    dict(id="C1-home-unset-no-xdg", files=base_files(), execs=["bin/term"],
         env={"HOME": None, "XDG_CONFIG_HOME": None, "XDG_CONFIG_DIRS": None, "XDG_DATA_HOME": None,
              "XDG_DATA_DIRS": None, "XDG_CACHE_HOME": None}, args=["--print-id"]),
    dict(id="C2-home-unset-all-xdg", files=base_files(), execs=["bin/term"], env={"HOME": None},
         args=["--print-id"]),
    dict(id="C2b-home-unset-all-xdg-print-cmd", files=base_files(), execs=["bin/term"], env={"HOME": None},
         args=["--print-cmd"]),
    dict(id="C3-home-unset-no-cache-home", files=base_files(), execs=["bin/term"],
         env={"HOME": None, "XDG_CACHE_HOME": None}, args=["--print-id"]),
    dict(id="C3b-home-unset-no-data-home", files=base_files(), execs=["bin/term"],
         env={"HOME": None, "XDG_DATA_HOME": None}, args=["--print-id"]),
    dict(id="C3c-home-unset-no-config-home", files=base_files(), execs=["bin/term"],
         env={"HOME": None, "XDG_CONFIG_HOME": None}, args=["--print-id"]),
    dict(id="C4b-home-empty-no-xdg", files=base_files(), execs=["bin/term"],
         env={"HOME": "", "XDG_CONFIG_HOME": None, "XDG_CONFIG_DIRS": None, "XDG_DATA_HOME": None,
              "XDG_DATA_DIRS": None, "XDG_CACHE_HOME": None}, args=["--print-id"]),
    dict(id="C12-loop-desktop-symlink", files={"home/.config/xdg-terminals.list": "loop.desktop\n"},
         env={}, links={"home/.local/share/applications/loop.desktop": "$ROOT/home/.local/share/applications"},
         args=["--print-id"]),
    dict(id="C13-subdir-cycle", files={"home/.config/xdg-terminals.list": "sub-term.desktop\n",
                                       "home/.local/share/applications/sub/term.desktop": ENTRY},
         execs=["bin/term"],
         links={"home/.local/share/applications/sub/loop": "$ROOT/home/.local/share/applications"},
         args=["--print-id"]),
    dict(id="C4-home-empty", files=base_files(), execs=["bin/term"], env={"HOME": ""},
         args=["--print-id"]),
    dict(id="C5-fifo-later-dir-unused", files=base_files("usr/share/applications"), execs=["bin/term"],
         env={"XDG_DATA_DIRS": "$ROOT/usr/share"},
         fifos=["home/.local/share/applications/foot.desktop"], args=["--print-id"]),
    dict(id="C6-fifo-later-dir-listed", files={"home/.config/xdg-terminals.list": "foot.desktop\n"},
         env={}, fifos=["home/.local/share/applications/foot.desktop"], args=["--print-id"]),
    dict(id="C7-fifo-first-dir", files=base_files("usr/share/applications"), execs=["bin/term"],
         env={"XDG_DATA_DIRS": "$ROOT/usr/share"},
         fifos=["usr/share/applications/foot.desktop"], args=["--print-id"]),
    dict(id="C8-symlink-loop", files=base_files("usr/share/applications"), execs=["bin/term"],
         env={"XDG_DATA_DIRS": "$ROOT/usr/share"},
         links={"home/.local/share/applications/loop": "$ROOT/home/.local/share/applications"},
         args=["--print-id"]),
    dict(id="C9-unreadable-entry-not-candidate", files=base_files("usr/share/applications"), execs=["bin/term"],
         env={"XDG_DATA_DIRS": "$ROOT/usr/share"},
         files_extra={"home/.local/share/applications/aaa.desktop": ENTRY},
         chmod0=["home/.local/share/applications/aaa.desktop"], args=["--print-id"]),
    dict(id="C10-unreadable-entry-only", files={"home/.config/xdg-terminals.list": "aaa.desktop\n"},
         env={}, files_extra={"home/.local/share/applications/aaa.desktop": ENTRY},
         chmod0=["home/.local/share/applications/aaa.desktop"], args=["--print-id"]),
    dict(id="C14-dir-shadows-file-later-dir", files={"home/.config/xdg-terminals.list": "x.desktop\n",
                                                    "usr/share/applications/x.desktop": ENTRY},
         execs=["bin/term"], env={"XDG_DATA_DIRS": "$ROOT/usr/share"},
         dirs_extra=["home/.local/share/applications/x.desktop"], args=["--print-id"]),
    dict(id="C11-unreadable-list", files=base_files(), execs=["bin/term"], env={},
         chmod0=["home/.config/xdg-terminals.list"], args=["--print-id"]),
]


def materialize(root, case):
    os.makedirs(os.path.join(root, "home"), exist_ok=True)
    os.makedirs(os.path.join(root, ".rw", "cache"), exist_ok=True)
    files = dict(case.get("files") or {})
    files.update(case.get("files_extra") or {})
    for rel, text in files.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(text.replace("$ROOT", root).encode())
    for rel in case.get("execs") or []:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)
    for rel in case.get("fifos") or []:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        os.mkfifo(p)
    for rel, target in (case.get("links") or {}).items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if os.path.lexists(p):
            os.unlink(p)
        os.symlink(target.replace("$ROOT", root), p)
    for rel in case.get("dirs_extra") or []:
        os.makedirs(os.path.join(root, rel), exist_ok=True)
    for rel in case.get("chmod0") or []:
        os.chmod(os.path.join(root, rel), 0o000)


def case_env(case, root):
    env = {"HOME": root + "/home", "PATH": root + "/bin:/oracle/bin",
           "XDG_CONFIG_HOME": root + "/home/.config", "XDG_CONFIG_DIRS": root + "/etc/xdg",
           "XDG_DATA_HOME": root + "/home/.local/share", "XDG_DATA_DIRS": root + "/usr/share",
           "XDG_CACHE_HOME": root + "/.rw/cache", "LANG": "C.UTF-8"}
    for k, v in (case.get("env") or {}).items():
        if v is None:
            env.pop(k, None)
        else:
            env[k] = v.replace("$ROOT", root)
    return env


def run_one(box, root, env, is_tool, args, trace, trace_set):
    argv = box.argv(root, env, is_tool, args)
    if is_tool:
        argv = [box.strace, "-f", "-qq", "-e", trace_set, "-e", "signal=none", "-o", trace] + argv
    try:
        p = subprocess.run(argv, capture_output=True, timeout=TIMEOUT, env={"PATH": "/usr/bin"})
        res = (p.returncode, p.stdout.decode("utf-8", "surrogateescape"),
               p.stderr.decode("utf-8", "surrogateescape"))
    except subprocess.TimeoutExpired:
        res = (124, "", "")
    return res


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    mod = load_counter()
    work = tempfile.mkdtemp(dir=SCRATCH, prefix="work-")
    box = mod.Box(work, tool_path=TOOL)
    print("pin  sha256", __import__("hashlib").sha256(open(box.pin, "rb").read()).hexdigest())
    print("tool sha256", __import__("hashlib").sha256(open(TOOL, "rb").read()).hexdigest())
    results = []
    for case in CASES:
        row = {"id": case["id"], "args": case["args"]}
        for who in ("pin", "tool"):
            root = os.path.join(work, "r-%s-%s" % (case["id"], who))
            os.makedirs(root)
            materialize(root, case)
            env = case_env(case, root)
            row["env"] = {k: ("<unset>" if k not in env else env[k].replace(root, "$ROOT"))
                          for k in ("HOME", "XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME")}
            args = case["args"] if who == "pin" else ["print"] + case["args"]
            trace = os.path.join(work, "tr-%s-%s" % (case["id"], who))
            open(trace, "w").close()
            rc, out, err = run_one(box, root, env, who == "tool", args, trace, mod.TRACE_SET)
            tripped = []
            if who == "tool":
                box.check_trace(trace)
                tripped = box.trips
                box.trips = []
            e = err.strip().splitlines()
            row[who] = {"rc": rc, "stdout": out.replace(root, "$ROOT"), "stderr1": e[0].replace(root, "$ROOT")[:220] if e else "",
                        "stderr_n": len(e), "stderr": [x.replace(root, "$ROOT")[:200] for x in e[:4]], "trips": tripped}
        row["agree"] = (row["pin"]["rc"] == row["tool"]["rc"]
                        and row["pin"]["stdout"] == row["tool"]["stdout"])
        results.append(row)
        print(json.dumps(row))
    with open(os.path.join(SEAT, "pin-vs-tool.json"), "w") as fh:
        json.dump(results, fh, indent=1)
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
