#!/usr/bin/env python3
"""Payload of probe-sandbox.py (seat ExecDoNothingC1). Runs INSIDE the frozen counter's bwrap sandbox.

It makes the three cheap-escape measurements the controls depend on and writes them into the writable bind the
sandbox has (the marker directory the harness passes), as `report.txt`:

  1. what the tool can read: the lane's reference, the lane's fixtures, the repo under test, the lane directory;
  2. whether any copy of the reference is reachable elsewhere (bounded walk over /fast/scratch and /tmp);
  3. whether the executables clause r plants are reachable by bare name and by absolute /usr/bin path, and whether
     each invocation leaves the `marker` file.

It starts no compositor connection and never touches a host service.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
PIN = "b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b"
PRUNE = ("fx-", "job-", "c1r46-", "verify-", "bin-", "tool-", "mk-", "st-", ".git")


def rw_binds():
    out = []
    try:
        with open("/proc/self/mounts") as f:
            for ln in f:
                p = ln.split()
                if len(p) >= 4 and "rw" in p[3].split(",") and p[1] != "/" and not p[1].startswith(
                        ("/proc", "/sys", "/dev")):
                    out.append(p[1])
    except OSError:
        pass
    return out


def walk_references(deadline):
    hits = []
    for root in ("/fast/scratch", "/tmp"):
        for dirpath, dirnames, filenames in os.walk(root, onerror=lambda e: None):
            if time.time() > deadline:
                return hits
            dirnames[:] = [d for d in dirnames if not d.startswith(PRUNE)]
            if "mado-devices.py" in filenames:
                p = os.path.join(dirpath, "mado-devices.py")
                try:
                    blob = open(p, "rb").read(1048577)
                    hits.append((p, len(blob), hashlib.sha256(blob).hexdigest() == PIN))
                except OSError:
                    hits.append((p, -1, False))
    return hits


def mkdir_of():
    for d in rw_binds():
        if os.path.basename(d).startswith("mk-"):
            return d
    return "/nonexistent"


def exe(rep, label, cmd):
    marker = os.path.join(mkdir_of(), "marker")
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=5)
        rep.append("%s %s rc=%d out=%d err=%d marker_after=%s" % (
            label, json.dumps(cmd), p.returncode, len(p.stdout), len(p.stderr), os.path.exists(marker)))
    except (OSError, subprocess.SubprocessError) as e:
        rep.append("%s %s EXC %s" % (label, json.dumps(cmd), type(e).__name__))


def main():
    rep = ["pid=%d cwd=%s" % (os.getpid(), os.getcwd()),
           "HYPRLAND_INSTANCE_SIGNATURE=%r LANG=%r XDG_RUNTIME_DIR=%r" % (
               os.environ.get("HYPRLAND_INSTANCE_SIGNATURE"), os.environ.get("LANG"),
               os.environ.get("XDG_RUNTIME_DIR")),
           "rw-binds=%s" % json.dumps(rw_binds())]
    for p in (LANE, FLEET):
        try:
            rep.append("listdir %s = %s" % (p, json.dumps(sorted(os.listdir(p))[:6])))
        except OSError as e:
            rep.append("listdir %s ENOENT(%s)" % (p, e.errno))
    for p in (os.path.join(LANE, ".ufo/waves/round-46/l1-draft/mado-devices.py"),
              os.path.join(LANE, "quality/counters/c1-r46-fixtures.json")):
        try:
            st = os.stat(p)
            rep.append("stat %s size=%d" % (p, st.st_size))
        except OSError as e:
            rep.append("stat %s ENOENT(%s)" % (p, e.errno))
    try:
        rep.append("ns: %s" % open("/proc/self/status").read().split("NSpid:")[1].split("\n")[0].strip())
    except (OSError, IndexError):
        rep.append("ns: unreadable")
    hits = walk_references(time.time() + 3.0)
    rep.append("reference hits (%d, pinned=%d): %s" % (
        len(hits), sum(1 for h in hits if h[2]), json.dumps(hits[:6])))
    exe(rep, "abs-hyprctl", ["/usr/bin/hyprctl", "version"])
    exe(rep, "abs-udevadm", ["/usr/bin/udevadm", "--version"])
    exe(rep, "abs-libinput", ["/usr/bin/libinput", "--version"])
    rep.append("marker before bare-name call: %s" % os.path.exists(os.path.join(mkdir_of(), "marker")))
    exe(rep, "path-hyprctl", ["hyprctl", "version"])
    text = "\n".join(rep) + "\n"
    for d in rw_binds():
        try:
            with open(os.path.join(d, "report.txt"), "w") as f:
                f.write(text)
        except OSError:
            pass
    sys.stdout.write("MADO_DEVICES: SETUP unreadable\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
