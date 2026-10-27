#!/usr/bin/env python3
"""Receipts for the seat: the five MADO_TERM cache states from real primed trees, and an isolation trace."""
import os
import re
import shutil
import subprocess
import sys

import harness

A_ = "usr/share/applications/"
L_ = "home/.config/xdg-terminals.list"


def term(name):
    return ("[Desktop Entry]\nType=Application\nName=%s\nExec=%s\n"
            "Categories=System;TerminalEmulator;\n" % (name, name))


def tree(box, root, mtime=1600000000):
    os.makedirs(root + "/home", exist_ok=True)
    os.makedirs(root + "/.rw/cache", exist_ok=True)
    harness.materialize(root, {A_ + "foot.desktop": term("foot"), L_: "foot.desktop\n"}, ["bin/foot"], (), mtime)


def env_of(root, extra=None):
    e = harness.case_env({}, root, {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
                                    "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share",
                                    "XDG_CURRENT_DESKTOP": "Hyprland"})
    e.update({k: v.replace("$ROOT", root) for k, v in (extra or {}).items()})
    return e


def mado_line(tool_out):
    for line in tool_out.splitlines():
        if line.startswith("MADO_TERM: "):
            return line
    return "(no MADO_TERM line)"


def states(box, out_path):
    lines = []
    for state in ("hit", "stale", "invalid", "absent", "disabled"):
        root = os.path.join(box.work, "demo-" + state + "/r")
        shutil.rmtree(os.path.dirname(root), ignore_errors=True)
        tree(box, root)
        env = env_of(root)
        cache = os.path.join(root, ".rw/cache/xdg-terminal-exec")
        if state in ("hit", "stale", "disabled"):
            harness.prime(box, root, env)
        if state == "stale":
            with open(os.path.join(root, L_), "wb") as fh:
                fh.write(b"kity.desktop\nfoot.desktop\n")   # size changes -> hash changes
            harness.pin_mtime(root, 1600000000)
        if state == "invalid":
            with open(cache, "wb") as fh:
                fh.write(b"0" * 32 + b"\nfoot\n\n\n\n\n\n\n\n\n\nfoot\n")
        if state == "disabled":
            env["XTE_CACHE_ENABLED"] = "false"
        rc_t, out_t, _e = box.run(root, env, "tool", ["explain"])
        rc_p, out_p, _e2 = box.run(root, env, "warm", ["--print-id", "--print-path", "--print-cmd"])
        lines.append("%-8s pin rc=%d stdout=%r" % (state, rc_p, out_p.replace(root, "$ROOT")))
        lines.append("%-8s tool explain rc=%d %s" % (state, rc_t, mado_line(out_t).replace(root, "$ROOT")))
        lines.append("")
        shutil.rmtree(os.path.dirname(root), ignore_errors=True)
    text = "\n".join(lines)
    with open(out_path, "w") as fh:
        fh.write(text + "\n")
    return text


def isolation(box, out_path):
    root = os.path.join(box.work, "iso/r")
    shutil.rmtree(os.path.dirname(root), ignore_errors=True)
    tree(box, root)
    env = env_of(root)
    harness.prime(box, root, env)
    strace = shutil.which("strace")
    reports = []
    for args in (["print", "--print-id", "--print-path", "--print-cmd"], ["explain"]):
        trace = os.path.join(box.work, "iso/trace-%s" % args[0])
        argv = box.argv(root, env, "tool", args)
        full = [strace, "-f", "-qq", "-e", "trace=execve,execveat,socket,socketpair,connect", "-e", "signal=none",
                "-o", trace] + argv
        p = subprocess.run(full, capture_output=True, env={"PATH": "/usr/bin"})
        seen = trips = 0
        events = []
        for ln in open(trace, encoding="latin-1"):
            rest = ln.split(" ", 1)[1].strip() if " " in ln else ln.strip()
            if not seen:
                if 'execve("/usr/bin/python3"' in rest and rest.endswith("= 0"):
                    seen += 1
                continue
            trips += 1
            events.append(rest[:80])
        reports.append("%s rc=%d python_execve_seen=%d traced_events_after=%d%s"
                       % (args[0], p.returncode, seen, trips, (": " + "; ".join(events[:5])) if events else ""))
    text = "tool = " + harness.TOOL + "\n" + "\n".join(reports)
    with open(out_path, "w") as fh:
        fh.write(text + "\n")
    shutil.rmtree(os.path.dirname(root), ignore_errors=True)
    return text


def main(outdir):
    box = harness.Box(harness.S)
    print(states(box, os.path.join(outdir, "explain-states.txt")))
    print(isolation(box, os.path.join(outdir, "isolation.txt")))


if __name__ == "__main__":
    main(sys.argv[1])
