#!/usr/bin/env python3
"""Probe: can a bwrap run capture the resolver's background cache save deterministically?"""
import importlib.util
import os
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
spec = importlib.util.spec_from_file_location("c47", os.path.join(LANE, "quality", "counters", "c1-r47-terminal.py"))
c47 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c47)

WORK = "/fast/scratch/hyaku/mado-r48/ExecCounterC1/probe"
os.makedirs(WORK, exist_ok=True)
box = c47.Box(WORK)

CASE = {
    "id": "p1",
    "env": {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
            "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share",
            "XDG_CURRENT_DESKTOP": "Hyprland"},
    "files": {
        "usr/share/applications/foot.desktop":
            "[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=foot\n",
        "home/.config/hyprland-xdg-terminals.list": "foot.desktop\n",
        "home/.config/xdg-terminals.list": "foot.desktop\n",
        "etc/xdg/xdg-terminals.list": "foot.desktop\n",
    },
    "exec": ["bin/foot"],
    "args": ["--print-cmd"],
}

WRAP = r'''set +e
xte__cache=$1; shift
"$@"
xte__rc=$?
xte__n=0
while [ "$xte__n" -lt 1200 ]; do
  xte__ok=
  if [ -f "$xte__cache" ]; then
    while IFS= read -r xte__l || [ -n "$xte__l" ]; do
      case "$xte__l" in *$'\036'END_OF_EXEC_USEP) xte__ok=1 ;; esac
    done < "$xte__cache" 2>/dev/null
  fi
  if [ -n "$xte__ok" ]; then break; fi
  xte__n=$((xte__n+1)); xte__z=0
  while [ "$xte__z" -lt 400 ]; do xte__z=$((xte__z+1)); done
done
exit "$xte__rc"
'''


def prime(root, wrapped):
    env = c47.case_env(CASE, root, "C.UTF-8")
    a = box.argv(root, env, False, ["--print-cmd"])
    if wrapped:
        cache = os.path.join(root, ".rw", "cache", "xdg-terminal-exec")
        # last len(args)+1 items are [pin] + args
        i = len(a) - 2
        assert a[i] == "/oracle/xdg-terminal-exec", a[i]
        a[i:i + 1] = ["/bin/bash", "-c", WRAP, "w", cache, "/oracle/xdg-terminal-exec"]
    p = subprocess.run(a, capture_output=True, timeout=60, env={"PATH": "/usr/bin"})
    return p.returncode, p.stdout.decode(), p.stderr.decode()


base = tempfile.mkdtemp(dir=WORK, prefix="pr-")
for mode in ("wrapped",):
    seen = []
    for k in range(8):
        root = os.path.join(base, mode, "r%d" % k)
        c47.materialize(root, CASE)
        rc, out, err = prime(root, mode == "wrapped")
        cf = os.path.join(root, ".rw", "cache", "xdg-terminal-exec")
        try:
            blob = open(cf, "rb").read()
            seen.append((len(blob), blob.count(b"\x1eEND_OF_EXEC_USEP"), blob.split(b"\n", 1)[0][:8]))
        except OSError as e:
            seen.append(("MISSING", str(e)[:40]))
        if k == 0:
            print(mode, "rc=%d out=%r err=%r" % (rc, out[:80], err[:200]))
    print(mode, "runs=%r" % (seen,))
