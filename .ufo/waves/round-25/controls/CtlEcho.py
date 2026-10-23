#!/usr/bin/env python3
"""SERVER ECHO control stub for mado round 25 C1 (shape: ask the compositor).

Does no config parsing at all. Tries, in order:
  1. `hyprctl binds -j` (read verb) and echoes its stdout;
  2. an AF_UNIX connect to the first Hyprland command socket found by globbing
     $XDG_RUNTIME_DIR/hypr/*/.socket.sock and /run/user/*/hypr/*/.socket.sock,
     sending `j/binds` and echoing the reply;
  3. otherwise prints `[]` so the caller still sees a JSON array.

Accepts (and ignores) `--home DIR`, which the counter always passes.
"""
import argparse
import glob
import json
import os
import socket
import subprocess
import sys


def from_hyprctl():
    p = subprocess.run(["hyprctl", "binds", "-j"], capture_output=True, timeout=30)
    if p.returncode != 0:
        return None
    return p.stdout


def sockets():
    pats = []
    xdg = os.environ.get("XDG_RUNTIME_DIR")
    if xdg:
        pats.append(os.path.join(xdg, "hypr", "*", ".socket.sock"))
    pats.append("/run/user/*/hypr/*/.socket.sock")
    found = []
    for pat in pats:
        found.extend(sorted(glob.glob(pat)))
    return found


def from_socket():
    for path in sockets():
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(10)
        try:
            s.connect(path)
            s.sendall(b"j/binds")
            chunks = []
            while True:
                b = s.recv(65536)
                if not b:
                    break
                chunks.append(b)
            return b"".join(chunks)
        except OSError:
            continue
        finally:
            s.close()
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--home")
    ap.parse_args()
    for fn in (from_hyprctl, from_socket):
        raw = fn()
        if raw is None:
            continue
        try:
            data = json.loads(raw)
        except Exception:  # noqa: BLE001
            continue
        if isinstance(data, list):
            print(json.dumps(data))
            return 0
    print("[]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
