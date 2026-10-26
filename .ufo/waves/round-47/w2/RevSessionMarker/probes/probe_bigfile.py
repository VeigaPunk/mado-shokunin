#!/usr/bin/env python3
"""probe_bigfile.py — does content beyond the 16 MiB decode cap stay invisible?"""
import os
import subprocess
import sys

GATE = ("/home/vgpnk/Projects/shokunin/mado-shokunin/"
        ".ufo/waves/round-47/w1/ExecSessionMarker/check-session-material.py")
SCRATCH = "/fast/scratch/hyaku/mado-r47/RevSessionMarker/probes"

DUMP = ('[{"address": "0x1", "mapped": true, "class": "Alacritty",'
        ' "title": "a live window title", "pid": 2562}]\n')
PROC = 'u_str ESTAB 0 0 * 3001 * 2001 users:(("gnome-keyring-d",pid=999,fd=9))\n'


def build(name, files):
    root = os.path.join(SCRATCH, name)
    os.makedirs(root, exist_ok=True)
    for rel, data in files.items():
        target = os.path.join(root, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        mode = "wb" if isinstance(data, bytes) else "w"
        with open(target, mode) as h:
            h.write(data)
    subprocess.run(["git", "-C", root, "init", "-q"], check=True)
    subprocess.run(["git", "-C", root, "add", "-A"], check=True)
    subprocess.run(["git", "-C", root, "-c", "user.name=probe", "-c",
                    "user.email=probe@scratch.invalid", "commit", "-q", "-m", "f"],
                   check=True)
    return root


def run(root):
    r = subprocess.run([sys.executable, "-I", GATE, "--repo", root, "--rev", "HEAD"],
                       capture_output=True, text=True,
                       env={**os.environ, "TMPDIR": SCRATCH + "/tmp"})
    lines = [l for l in r.stdout.splitlines()
             if l.startswith(("FINDING", "SESSION_MATERIAL:"))]
    return r.returncode, lines


def main():
    os.makedirs(SCRATCH + "/tmp", exist_ok=True)
    filler = b"x" * (16 << 20)  # exactly 16 MiB of filler

    # t1: dump + proc row beyond the 16 MiB cap.
    tail = filler + DUMP.encode() + PROC.encode()
    root = build("big-tail", {".ufo/waves/round-47/w1/ProbeSeat/big.txt": tail})
    rc, lines = run(root)
    print("== t1 material beyond 16 MiB cap rc=%d" % rc)
    for l in lines:
        print("   " + l)

    # t2 control: same material inside the cap.
    head = DUMP.encode() + PROC.encode() + filler
    root = build("big-head", {".ufo/waves/round-47/w1/ProbeSeat/big.txt": head})
    rc, lines = run(root)
    print("== t2 control material inside cap rc=%d" % rc)
    for l in lines:
        print("   " + l)


if __name__ == "__main__":
    main()
