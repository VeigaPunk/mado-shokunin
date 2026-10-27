#!/usr/bin/env python3
"""Build a scratch git fixture of SYNTHETIC receipt shapes and score the gate.

Every value is a placeholder ("syntheticuser", "example-host", ...). Nothing is
copied from the host. Prints one line per shape: the rules the gate reported.
"""
import base64
import json
import os
import subprocess
import sys

ROOT = sys.argv[1]
GATE = sys.argv[2]

CLIENT_DUMP = '[{"class": "SyntheticTerm", "title": "synthetic window title"}]\n'
HOME_LINES = "\n".join("/home/syntheticuser/dir%02d/file.txt" % i for i in range(12)) + "\n"


def ls_lRl(root, names, mode="-rw-r--r--  1 1000 1000  12 Oct 26 10:00"):
    out = []
    out.append("%s:" % root)
    out.append("total %d" % (len(names) * 4))
    for name in names:
        out.append("%s %s" % (mode, name))
    out.append("")
    return "\n".join(out) + "\n"


CACHE = "\n".join([
    "0" * 32,
    "/usr/bin/synthetic-term",
    "/home/syntheticuser/.local/share/applications/synthetic-term.desktop",
    "synthetic-term.desktop",
    "open",
    "--working-directory=/home/syntheticuser",
    "--app-id=synthetic-term",
    "--title=synthetic window title",
    "--dir=/home/syntheticuser/projects",
    "",
    "/usr/bin/synthetic-term",
    "--title=synthetic window title",
    "/home/syntheticuser/projects",
    "\x1eEND_OF_EXEC_USEP",
]) + "\n"

FILES = {
    # 1 device names / addresses, projected out of hyprctl devices -j
    ".ufo/s/devices.json": json.dumps(
        {"keyboards": [{"name": "synthetic-keyboard", "address": "synthetic-addr",
                        "layout": "ab", "active_keymap": "Synthetic (Layout)"}],
         "mice": [{"name": "synthetic-mouse", "scrollFactor": 0.4}]}, indent=1) + "\n",
    # 2 instance signature + runtime socket path
    ".ufo/s/instances.json": json.dumps(
        [{"instance": "example-host_4242_9001", "pid": 4242,
          "wl_socket": "/run/user/1000/hypr/example-host_4242_9001/.socket.sock"}], indent=1) + "\n",
    # 3 small ls -LRl of a home tree (3 headers, under the R4 limit)
    ".ufo/s/ls-lRl-small.txt": ls_lRl("/home/syntheticuser/.config/xdg", ["a.desktop", "b.desktop"]),
    # 4 same dump rooted outside /home (the C1 sandbox shape)
    ".ufo/s/ls-lRl-scratch.txt": ls_lRl("/fast/scratch/run/xdg", ["a.desktop", "b.desktop"]),
    # 5 literal warm cache (entry path, dir arg, title arg)
    ".ufo/s/cache-warm.txt": CACHE,
    # 6 home listing, base64 encoded
    ".ufo/s/b64.txt": base64.b64encode(HOME_LINES.encode()).decode() + "\n",
    # 7 home listing inside a JSON array
    ".ufo/s/home-json.txt": json.dumps(HOME_LINES.split()) + "\n",
    # 8 home listing rendered as markdown rows
    ".ufo/s/home-table.md": "| path |\n| --- |\n" + "".join(
        "| %s |\n" % line for line in HOME_LINES.split()) ,
    # 9 secret-shaped values
    ".ufo/s/secret-env.txt": "SYNTH_TOKEN=ghp_" + "a" * 36 + "\nAWS_SECRET_ACCESS_KEY=syntheticsecret\n",
    # 10 xkb verbose include paths in prose
    ".ufo/s/xkb-verbose.txt": (
        "loaded include file: /home/syntheticuser/.xkb/symbols/synthetic-layout\n"
        "loaded include file: /home/syntheticuser/.xkb/rules/evdev\n"),
    # 11 relative listing (ls -1): names only
    ".ufo/s/relative-names.txt": "synthetic-bank.desktop\nsynthetic-therapy.desktop\nsynthetic-jobsearch.desktop\n",
    # 11b home listing under $HOME spelling and with duplicate paths
    ".ufo/s/home-dollar.txt": "\n".join("$HOME/dir%02d/f.txt" % i for i in range(12)) + "\n",
    ".ufo/s/home-dupes.txt": "\n".join("/home/syntheticuser/dir00/f%02d.txt" % (i % 2) for i in range(12)) + "\n",
    # 11c a large dir tree: ls -LRl headers only (12 absolute dir lines)
    ".ufo/s/ls-lRl-tree.txt": "".join("%s:\n\ntotal 0\n\n" % d for d in
        ["/home/syntheticuser/.config/xdg/d%02d" % i for i in range(12)]),
    # 11d listing with a space in one path
    ".ufo/s/home-space.txt": "\n".join("/home/syntheticuser/My Documents/f%02d.txt" % i for i in range(12)) + "\n",
    # 12 control: plain home listing (expected R4)
    ".ufo/s/home-listing.txt": HOME_LINES,
    # 13 control: client dump (expected R1)
    ".ufo/s/clients.json": CLIENT_DUMP,
    # 14 same dump outside .ufo/ (C2 knowledge + C1 counter fixture locations)
    "corpus/knowledge/synthetic-note.md": CLIENT_DUMP,
    "quality/counters/synthetic-fixtures.json": json.dumps({"cache": CACHE}) + "\n",
}


def main():
    os.makedirs(ROOT, exist_ok=True)
    for rel, text in FILES.items():
        path = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)

    # 15 a >16 MiB receipt whose client dump sits past the text cap
    big = os.path.join(ROOT, ".ufo/s/big.txt")
    with open(big, "w", encoding="utf-8") as handle:
        handle.write("filler line\n" * ((17 << 20) // 12))
        handle.write(CLIENT_DUMP)
    # 16 UTF-16 encoded client dump (NUL bytes inside the first 8 KiB)
    with open(os.path.join(ROOT, ".ufo/s/utf16.md"), "wb") as handle:
        handle.write(CLIENT_DUMP.encode("utf-16"))

    subprocess.run(["git", "-C", ROOT, "init", "-q"], check=True)
    top = subprocess.run(["git", "-C", ROOT, "rev-parse", "--show-toplevel"],
                         check=True, capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(ROOT), (top, ROOT)
    subprocess.run(["git", "-C", ROOT, "add", "-A"], check=True)
    subprocess.run(["git", "-C", ROOT, "-c", "user.name=fixture",
                    "-c", "user.email=fixture@scratch.invalid", "commit", "-q", "-m", "shapes"],
                   check=True)

    proc = subprocess.run([sys.executable, "-I", GATE, "--repo", ROOT, "--rev", "HEAD"],
                          capture_output=True, text=True)
    print("rc=%d" % proc.returncode)
    print(proc.stdout, end="")
    if proc.stderr:
        print("stderr: " + proc.stderr.strip())


main()
