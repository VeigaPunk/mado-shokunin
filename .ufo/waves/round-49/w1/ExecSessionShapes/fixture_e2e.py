#!/usr/bin/env python3
"""End-to-end: v2 is blind to the round-48 receipt shapes, v3 is not.

Usage: fixture_e2e.py SCRATCH V2_GATE V3_GATE

Builds one throwaway git repository under *SCRATCH* holding (a) the four
receipt shapes round-48 committed, with a synthetic home user and account, and
(b) the masked + prose forms the lane's probe scripts already write. Then runs
both gates over it and prints the per-rule tally. The fixture repository is
asserted to be its own toplevel before the first commit.
"""
import os
import subprocess
import sys

SCRATCH = os.path.abspath(sys.argv[1])
V2 = os.path.abspath(sys.argv[2])
V3 = os.path.abspath(sys.argv[3])
ACCOUNT = "someone"

LEAK_GREP = "\n".join([
    "/home/someone/.config/hypr/input.conf:5:  # kb_layout = us,dk,eu",
    "/home/someone/.config/hypr/input.conf:10:  kb_layout = br",
]) + "\n"

LEAK_DIAG = (
    'xkbcommon: INFO: Include path failed: "/home/someone/.xkb" '
    '(No such file or directory)\n')

LEAK_LS = "\n".join([
    "-rw-r--r-- 1 someone someone 12 Oct 26 19:50 xdg-terminals.list",
    "/home/someone/.local/share/applications:",
    "total 8",
    "-rw-r--r-- 1 1000 1000 87 Oct 26 19:50 synthetic-term.desktop",
]) + "\n"

LEAK_CACHE = "\n".join([
    "0" * 32,
    "/usr/bin/synthetic-term",
    "--working-directory=/home/someone",
    "--title=synthetic window title",
]) + "\n"

CLEAN = "\n".join([
    "~/.config/hypr/input.conf:5:  # kb_layout = us,dk,eu",
    "$HOME/.cache/xdg-terminal-exec/log.txt:3: wrote 1 entry",
    "The entry lives at `/home/someone/.config/hypr/input.conf` in prose.",
    'the tool said "/home/someone/.xkb" was missing and moved on.',
    "-rw-r--r-- 1 1000 1000 12 Oct 26 19:50 xdg-terminals.list",
    "Pass `--title=` to leave the title alone.",
]) + "\n"

FILES = {
    "receipts/leak-grep.txt": LEAK_GREP,
    "receipts/leak-diag.txt": LEAK_DIAG,
    "receipts/leak-ls.txt": LEAK_LS,
    "receipts/leak-cache.txt": LEAK_CACHE,
    "receipts/clean-masked.txt": CLEAN,
}


def main():
    root = os.path.join(SCRATCH, "fixture")
    os.makedirs(root, exist_ok=True)
    for relpath, text in FILES.items():
        target = os.path.join(root, relpath)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(text)
    subprocess.run(["git", "-C", root, "init", "-q"], check=True)
    subprocess.run(["git", "-C", root, "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", root, "-c", "user.name=fixture",
         "-c", "user.email=fixture@scratch.invalid", "commit", "-q", "-m", "fixture"],
        check=True,
    )
    top = subprocess.run(["git", "-C", root, "rev-parse", "--show-toplevel"],
                         check=True, capture_output=True, text=True).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(root):
        raise SystemExit("toplevel %r != %r" % (top, root))
    print("fixture=%s files=%d" % (os.path.basename(root), len(FILES)))

    for label, gate, extra in (
        ("v2 default scope", V2, ()),
        ("v2 --scope all", V2, ("--scope", "all")),
        ("v3 --account", V3, ("--account", ACCOUNT)),
    ):
        proc = subprocess.run(
            [sys.executable, "-I", gate, "--repo", root, "--rev", "HEAD",
             "--no-waivers", *extra],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300,
        )
        print("== %s rc=%d" % (label, proc.returncode))
        for line in proc.stdout.decode("utf-8", "replace").splitlines():
            if line.startswith(("FINDING", "SESSION_MATERIAL")):
                print("   " + line)


main()
