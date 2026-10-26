#!/usr/bin/env python3
"""Metamorphic environment check: the same input must produce the same bytes in a real-looking environment."""
import json
import os
import subprocess
import sys
import tempfile

S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
from probe import M  # noqa: E402

TOOLS = ["ref.py", "cheat-env-gate.py", "cheat-table45.py", "cheat-scorer-oracle.py"]
CFG = ["monitor = DP-5, 3440x1440@100, 0x0, 1\n"]
DUMP = [M("DP-5")]


def run(tool, envname):
    d = tempfile.mkdtemp(dir=S, prefix="env-")
    if envname == "fixture":
        cwd = os.path.join(d, "fx-abc")
        home = os.path.join(cwd, "home")
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": home,
               "HYPRLAND_INSTANCE_SIGNATURE": "mado-r45-fixture"}
    else:
        cwd = os.path.join(d, "config", "hypr")
        home = os.path.join(d, "home")
        env = {"PATH": "/usr/bin:/bin:/usr/local/bin", "LANG": "C.UTF-8", "HOME": home,
               "HYPRLAND_INSTANCE_SIGNATURE": "a1b2c3d4e5f6_1729944000_987654321"}
    os.makedirs(cwd)
    os.makedirs(home)
    raw = json.dumps(DUMP, indent=2).encode()
    dp = os.path.join(d, "monitors.json")
    with open(dp, "wb") as f:
        f.write(raw)
    args = ["--monitors", dp]
    for k, t in enumerate(CFG):
        cp = os.path.join(d, "c%d.conf" % k)
        with open(cp, "w") as f:
            f.write(t)
        args += ["--config", cp]
    p = subprocess.run([sys.executable, "-I", os.path.join(S, tool)] + args, capture_output=True,
                       cwd=cwd, env=env, timeout=30)
    return p.returncode, p.stdout.decode("utf-8", "replace").replace(d, "<D>").replace(cwd, "<CWD>")


def main():
    print("# same input, two environments: fixture env (cwd fx-*, HOME <fx>/home, signature mado-r45-fixture)")
    print("# vs real-looking env (cwd <d>/config/hypr, HOME <d>/home, PATH+/usr/local/bin, random signature)")
    for t in TOOLS:
        a = run(t, "fixture")
        b = run(t, "real")
        print("%-24s fixture rc=%d real rc=%d identical=%s" % (t, a[0], b[0], a == b))
        if a != b:
            print("%-24s real stdout: %r" % ("", b[1].strip()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
