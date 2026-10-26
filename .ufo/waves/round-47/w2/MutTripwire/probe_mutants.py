#!/usr/bin/env python3
"""MutTripwire probe harness.

For every mutant, run the exact input that reaches its trigger under host
strace with the FULL syscall set (execve, execveat, clone, clone3, fork,
vfork, socket, socketpair, connect) and record:
  - which forbidden events actually fired (with sample trace lines),
  - what the counter's clause-r subset (execve,execveat,socket,socketpair,
    connect) would have recorded,
  - whether the mutant's stdout still equals the reference's on that input.
Everything is written to receipts/probes.json; probe trees live in scratch.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = LANE + "/.ufo/waves/round-47/w2/MutTripwire"
MUTDIR = SEAT + "/mutants"
RCPT = SEAT + "/receipts"
SCRATCH = "/fast/scratch/hyaku/mado-r47/MutTripwire"
REF = LANE + "/.ufo/waves/round-47/l1-draft/mado-terminal.py"
PY = "/usr/bin/python3"

TRACE_SET = "execve,execveat,clone,clone3,fork,vfork,socket,socketpair,connect"
COUNTER_SET = {"execve", "execveat", "socket", "socketpair", "connect"}

FOOT = ("[Desktop Entry]\nType=Application\nName=foot\nExec=foot\n"
        "Categories=System;TerminalEmulator;\n")
FOOT_ACTION = FOOT + "Actions=srv;\n[Desktop Action srv]\nExec=footclient\n"
STUB = "#!/bin/sh\nexit 0\n"


def build_tree(root, action):
    os.makedirs(root + "/usr/share/applications")
    os.makedirs(root + "/bin")
    os.makedirs(root + "/home/.config")
    os.makedirs(root + "/cache")
    with open(root + "/usr/share/applications/foot.desktop", "w") as fh:
        fh.write(FOOT_ACTION if action else FOOT)
    for n in ("foot", "footclient"):
        p = root + "/bin/" + n
        with open(p, "w") as fh:
            fh.write(STUB)
        os.chmod(p, 0o755)
    if action:
        with open(root + "/home/.config/xdg-terminals.list", "w") as fh:
            fh.write("foot.desktop:srv\n")


def tree_env(root):
    return {
        "HOME": root + "/home", "PATH": root + "/bin:/usr/bin",
        "XDG_CONFIG_HOME": root + "/home/.config", "XDG_CONFIG_DIRS": root + "/etc/xdg",
        "XDG_DATA_HOME": root + "/home/.local/share", "XDG_DATA_DIRS": root + "/usr/share",
        "XDG_CACHE_HOME": root + "/cache", "LANG": "C.UTF-8",
    }


EVENT_RES = {
    "execve_bin_sh": r'execve\("/bin/sh"',
    "execveat": r"execveat\(",
    "clone": r"\bclone3?\(",
    "fork": r"\bfork\(",
    "vfork": r"\bvfork\(",
    "socket": r"\bsocket\(",
    "socketpair": r"\bsocketpair\(",
    "connect": r"\bconnect\(",
}


def run_probe(tool, argv, env, trace_path):
    cmd = ["strace", "-f", "-qq", "-e", "trace=" + TRACE_SET, "-o", trace_path, PY, "-I", tool] + argv
    p = subprocess.run(cmd, capture_output=True, timeout=120, env=env, cwd=SCRATCH)
    events = {}
    try:
        lines = open(trace_path, encoding="latin-1").read().splitlines()
    except OSError:
        lines = []
    for name, pat in EVENT_RES.items():
        hits = [l for l in lines if re.search(pat, l)]
        if hits:
            events[name] = {"count": len(hits), "sample": hits[0].strip()[:160]}
    return p.returncode, p.stdout, events


def main():
    shutil.rmtree(SCRATCH + "/probe", ignore_errors=True)
    capfile = SCRATCH + "/probe/capture.txt"
    os.makedirs(SCRATCH + "/probe", exist_ok=True)
    with open(capfile, "w") as fh:
        fh.write("id=foot.desktop\npath=x\n")
    results = []
    ref_cache = {}
    for mid, beh, trig in [
        ("M01", "os.system", "selftest-start"), ("M02", "os.system", "explain-plain"),
        ("M03", "subprocess", "print-cmd"), ("M04", "subprocess.Popen", "explain-observed"),
        ("M05", "socket", "print-cmd"), ("M06", "socket", "action-accepted"),
        ("M07", "fork-exec", "selftest-start"), ("M08", "fork-exec", "explain-plain"),
        ("M09", "fork-only", "selftest-start"), ("M10", "fork-only", "print-cmd"),
        ("M11", "multiprocessing", "explain-plain"), ("M12", "multiprocessing", "selftest-100th"),
    ]:
        kind = trig.replace("selftest-100th", "selftest-start")
        action = trig == "action-accepted"
        root = "%s/probe/%s" % (SCRATCH, mid)
        build_tree(root, action)
        env = tree_env(root)
        if kind == "selftest-start":
            argv = ["--selftest"]
        elif kind == "print-cmd":
            argv = ["print", "--print-cmd"]
        elif kind == "explain-plain":
            argv = ["explain"]
        elif kind == "explain-observed":
            argv = ["explain", "--observed", capfile]
        else:
            argv = ["print", "--print-id"]
        mut = "%s/%s-%s-%s.py" % (MUTDIR, mid, beh.replace(".", "-"), trig)
        mrc, mout, events = run_probe(mut, argv, env, "%s/probe/%s.trace" % (SCRATCH, mid))
        rrc, rout, _ = run_probe(REF, argv, env, "%s/probe/ref-%s.trace" % (SCRATCH, mid))
        rootb = root.encode()
        stdout_equal = mout.replace(rootb, b"$ROOT") == rout.replace(rootb, b"$ROOT")
        counter_visible = sorted({("execve" if k == "execve_bin_sh" else k)
                                  for k in events} & COUNTER_SET)
        results.append({
            "id": mid, "behaviour": beh, "trigger": trig, "argv": argv,
            "mut_rc": mrc, "ref_rc": rrc,
            "stdout_equal_to_reference": stdout_equal,
            "mut_stdout_sha256": hashlib.sha256(mout).hexdigest()[:16],
            "ref_stdout_sha256": hashlib.sha256(rout).hexdigest()[:16],
            "events": events,
            "counter_visible_events": counter_visible,
            "fired": any(k in events for k in (
                "execve_bin_sh", "clone", "fork", "vfork", "socket", "socketpair", "connect")),
            "counter_would_see": bool(counter_visible),
        })
        r = results[-1]
        print("%s fired=%s counter_would_see=%s stdout_equal=%s events=%s" % (
            mid, r["fired"], r["counter_would_see"], r["stdout_equal_to_reference"],
            ",".join(sorted(events)) or "-"))
    with open(RCPT + "/probes.json", "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1)
    print("probes.json written")


if __name__ == "__main__":
    main()
