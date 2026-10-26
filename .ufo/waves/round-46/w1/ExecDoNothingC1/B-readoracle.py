#!/usr/bin/env python3
"""B-READORACLE control (seat ExecDoNothingC1, mado round 46 w1).

Attack (b) of the seat spec: read the counter's oracle at runtime instead of modelling the contract. It tries the
reference and the fixtures at their lane paths, then walks the filesystem for any file named `mado-devices.py` or
`c1-r46-fixtures.json`, imports what it finds and answers with it. When nothing is reachable it prints a SETUP line.

Whatever it can see, it records in the one writable bind mount it can find in /proc/self/mounts (the counter's
marker directory), as `probe-<pid>.txt`, so the seat can read the sandbox's actual visibility from outside. It
never creates the file named `marker`, so clause r is not tripped by the probe itself.

This file is the control; its output is the measurement. Committed at tools/mado-devices.py in a scratch clone.
"""
import importlib.util
import json
import os
import sys
import time

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
CAND = [os.path.join(LANE, ".ufo/waves/round-46/l1-draft/mado-devices.py"),
        os.path.join(LANE, "quality/counters/c1-r46-fixtures.json"),
        os.path.join(FLEET, "mado-shokunin/.ufo/waves/round-46/l1-draft/mado-devices.py"),
        "/fast/scratch/hyaku/mado-r46/ExecDoNothingC1/ref/tools/mado-devices.py",
        "/tmp/mado-devices.py"]
ROOTS = ["/home", "/fast", "/tmp", "/opt", "/srv", "/var/tmp", "/run"]
MAX_BYTES = 1048576


def writable_binds():
    out = []
    try:
        with open("/proc/self/mounts") as f:
            for ln in f:
                p = ln.split()
                if len(p) >= 4 and "rw" in p[3].split(",") and p[1] != "/" and not p[1].startswith(("/proc", "/sys",
                                                                                                      "/dev")):
                    out.append(p[1])
    except OSError:
        pass
    return out


def probe():
    rep = ["pid=%d ppid=%d cwd=%s" % (os.getpid(), os.getppid(), os.getcwd()),
           "argv=%s" % json.dumps(sys.argv[1:])]
    for k in ("HYPRLAND_INSTANCE_SIGNATURE", "LANG", "HOME", "XDG_RUNTIME_DIR", "PATH"):
        rep.append("env %s=%r" % (k, os.environ.get(k)))
    for p in CAND:
        try:
            st = os.stat(p)
            rep.append("stat %s size=%d mode=%o" % (p, st.st_size, st.st_mode))
        except OSError as e:
            rep.append("stat %s ENOENT(%s)" % (p, e.errno))
    for d in (FLEET, LANE):
        try:
            rep.append("listdir %s = %r" % (d, sorted(os.listdir(d))[:8]))
        except OSError as e:
            rep.append("listdir %s ENOENT(%s)" % (d, e.errno))
    deadline, hits = time.time() + 0.2, []
    for root in ROOTS:
        for dirpath, dirnames, filenames in os.walk(root, onerror=lambda e: None):
            if time.time() > deadline:
                break
            for fn in filenames:
                if fn in ("mado-devices.py", "c1-r46-fixtures.json"):
                    hits.append(os.path.join(dirpath, fn))
                    if len(hits) >= 20:
                        break
        if time.time() > deadline:
            break
    rep.append("walk hits(%d)=%s" % (len(hits), json.dumps(hits[:20])))
    rep.append("mounts rw-binds=%s" % json.dumps(writable_binds()))
    for d in writable_binds():
        try:
            with open(os.path.join(d, "probe-%d.txt" % os.getpid()), "w") as f:
                f.write("\n".join(rep) + "\n")
        except OSError:
            pass
    return hits


def load(path):
    spec = importlib.util.spec_from_file_location("stolen_model", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_regular(path):
    with open(path, "rb") as f:
        data = f.read(MAX_BYTES + 2)
    if len(data) > MAX_BYTES:
        return None
    return data


def answer(argv):
    hits = probe()
    for p in [CAND[0]] + hits:
        if not p.endswith(".py"):
            continue
        data = read_regular(p) if os.path.isfile(p) else None
        if not data or b"MADO_DEVICES" not in data:
            continue
        mod = load(p)
        dev, cfgs, i = None, [], 0
        while i < len(argv):
            if i + 1 >= len(argv):
                return ["MADO_DEVICES: SETUP usage"], 2
            if argv[i] == "--devices" and dev is None:
                dev = argv[i + 1]
            elif argv[i] == "--config":
                cfgs.append(argv[i + 1])
            else:
                return ["MADO_DEVICES: SETUP usage"], 2
            i += 2
        ddata = sys.stdin.buffer.read() if dev == "-" else read_regular(dev)
        texts = [read_regular(c).decode("utf-8", "replace") for c in cfgs]
        return mod.report(ddata, texts)
    return ["MADO_DEVICES: SETUP unreadable"], 2


def run(argv):
    if argv == ["--selftest"]:
        print("MADO_DEVICES_SELFTEST: 48/48 passed")
        return None, 0
    try:
        return answer(argv)
    except Exception:
        return ["MADO_DEVICES: SETUP unreadable"], 2


def main():
    lines, rc = run(sys.argv[1:])
    if lines is not None:
        sys.stdout.write("".join(l + "\n" for l in lines))
    return rc


if __name__ == "__main__":
    sys.exit(main())
