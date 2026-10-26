#!/usr/bin/env python3
"""Generate demo fixtures for the round-47 oracle harness.

`expect` is produced ONLY by running the pinned script on the materialized case
(never typed by hand): the real /usr/bin/xdg-terminal-exec (sha256 pinned) is
run directly, print modes only, with XDG_CACHE_HOME redirected into the
generator scratch and PATH set to the case bin plus a directory holding only
the externals the resolver needs (tr find awk ls md5sum mkdir rm), so the host
run sees exactly what the sandbox run sees.

  gen-demo-fixtures.py --scratch DIR --out F.json [--receipts DIR]

Writes F.json (frozen schema) and, with --receipts, a host-reference receipt.
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

PIN = "/usr/bin/xdg-terminal-exec"
PIN_SHA = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"
EXTERNALS = ("tr", "find", "awk", "ls", "md5sum", "mkdir", "rm")

ENTRY = """[Desktop Entry]
Type=Application
Name={name}
Exec={exec}
Categories=System;TerminalEmulator;
"""


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def cases():
    """Return (id, class, env, files, exec, args) tuples."""
    out = []

    def add(cid, cls, env, files, execs, args):
        out.append((cid, cls, env, files, execs, args))

    hypr = {"XDG_CURRENT_DESKTOP": "Hyprland"}
    std = dict(
        XDG_CONFIG_HOME="$ROOT/home/.config",
        XDG_CONFIG_DIRS="$ROOT/etc/xdg",
        XDG_DATA_HOME="$ROOT/home/.local/share",
        XDG_DATA_DIRS="$ROOT/usr/share",
    )

    add(
        "c01-config-select",
        "config-list-wins",
        dict(hypr, **std),
        {
            "home/.config/xdg-terminals.list": "Alacritty.desktop\n",
            "home/.local/share/applications/Alacritty.desktop":
                ENTRY.format(name="Alacritty", exec="alacritty"),
        },
        ["bin/alacritty"],
        ["--print-id", "--print-path", "--print-cmd"],
    )
    add(
        "c02-fallback-scan",
        "no-config-fallback",
        dict(hypr, **std),
        {
            "usr/share/applications/Alacritty.desktop":
                ENTRY.format(name="Alacritty", exec="alacritty"),
            "usr/share/applications/Foot.desktop":
                ENTRY.format(name="Foot", exec="foot --server"),
        },
        ["bin/alacritty", "bin/foot"],
        ["--print-id", "--print-path", "--print-cmd"],
    )
    add(
        "c03-hidden-skipped",
        "hidden",
        dict(hypr, **std),
        {
            "home/.config/xdg-terminals.list": "Alacritty.desktop\nFoot.desktop\n",
            "home/.local/share/applications/Alacritty.desktop":
                ENTRY.format(name="Alacritty", exec="alacritty")
                + "Hidden=true\n",
            "home/.local/share/applications/Foot.desktop":
                ENTRY.format(name="Foot", exec="foot"),
        },
        ["bin/alacritty", "bin/foot"],
        ["--print-id", "--print-path"],
    )
    add(
        "c04-not-terminal-emulator",
        "wrong-category",
        dict(hypr, **std),
        {
            "home/.config/xdg-terminals.list": "Editor.desktop\nFoot.desktop\n",
            "home/.local/share/applications/Editor.desktop":
                "[Desktop Entry]\nType=Application\nName=Editor\n"
                "Exec=alacritty\nCategories=Utility;TextEditor;\n",
            "home/.local/share/applications/Foot.desktop":
                ENTRY.format(name="Foot", exec="foot"),
        },
        ["bin/alacritty", "bin/foot"],
        ["--print-id", "--print-path"],
    )
    add(
        "c05-tryexec-missing",
        "tryexec-not-on-path",
        dict(hypr, **std),
        {
            "home/.config/xdg-terminals.list": "Alacritty.desktop\nFoot.desktop\n",
            "home/.local/share/applications/Alacritty.desktop":
                ENTRY.format(name="Alacritty", exec="alacritty")
                .replace("Exec=alacritty", "TryExec=ghostterm\nExec=alacritty"),
            "home/.local/share/applications/Foot.desktop":
                ENTRY.format(name="Foot", exec="foot"),
        },
        ["bin/alacritty", "bin/foot"],
        ["--print-id", "--print-path"],
    )
    add(
        "c06-entry-missing",
        "listed-id-absent",
        dict(hypr, **std),
        {
            "home/.config/xdg-terminals.list": "Ghost.desktop\nFoot.desktop\n",
            "home/.local/share/applications/Foot.desktop":
                ENTRY.format(name="Foot", exec="foot"),
        },
        ["bin/foot"],
        ["--print-id", "--print-path"],
    )
    add(
        "c07-desktop-action",
        "action-id",
        dict(hypr, **std),
        {
            "home/.config/xdg-terminals.list": "Alacritty.desktop:New\n",
            "home/.local/share/applications/Alacritty.desktop":
                ENTRY.format(name="Alacritty", exec="alacritty")
                + "Actions=New;NewTab;\n\n[Desktop Action New]\nName=New\n"
                "Exec=alacritty --new-window\n\n[Desktop Action NewTab]\n"
                "Name=New tab\nExec=alacritty --new-tab\n",
        },
        ["bin/alacritty"],
        ["--print-id", "--print-path", "--print-cmd"],
    )
    add(
        "c08-onlyshowin",
        "show-in-rules",
        dict(hypr, **std),
        {
            "home/.config/xdg-terminals.list": "Alacritty.desktop\nFoot.desktop\n",
            "home/.local/share/applications/Alacritty.desktop":
                ENTRY.format(name="Alacritty", exec="alacritty")
                + "OnlyShowIn=GNOME;\n",
            "home/.local/share/applications/Foot.desktop":
                ENTRY.format(name="Foot", exec="foot"),
        },
        ["bin/alacritty", "bin/foot"],
        ["--print-id", "--print-path"],
    )
    add(
        "c09-desktop-list-order",
        "multi-current-desktop",
        {
            "XDG_CURRENT_DESKTOP": "GNOME:Hyprland",
            "XDG_CONFIG_HOME": "$ROOT/home/.config",
            "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
            "XDG_DATA_HOME": "$ROOT/home/.local/share",
            "XDG_DATA_DIRS": "$ROOT/usr/share",
        },
        {
            "home/.config/gnome-xdg-terminals.list": "Foot.desktop\n",
            "home/.config/hyprland-xdg-terminals.list": "Alacritty.desktop\n",
            "home/.local/share/applications/Alacritty.desktop":
                ENTRY.format(name="Alacritty", exec="alacritty"),
            "home/.local/share/applications/Foot.desktop":
                ENTRY.format(name="Foot", exec="foot"),
        },
        ["bin/alacritty", "bin/foot"],
        ["--print-id", "--print-path"],
    )
    add(
        "c10-print-delimiters",
        "print-delimiters",
        dict(hypr, **std),
        {
            "home/.config/xdg-terminals.list": "Alacritty.desktop\n",
            "home/.local/share/applications/Alacritty.desktop":
                ENTRY.format(name="Alacritty", exec="alacritty"),
        },
        ["bin/alacritty"],
        [
            "--print-id",
            "--print-path",
            "--print-cmd",
            "--print-delimiter=,",
            "--print-cmd=|",
        ],
    )
    add(
        "c11-no-terminal",
        "no-terminal",
        dict(hypr, **std),
        {"usr/share/README": "no applications here\n"},
        [],
        ["--print-id", "--print-path", "--print-cmd"],
    )
    add(
        "c12-duplicate-id-precedence",
        "data-dir-precedence",
        dict(hypr, **std),
        {
            "home/.local/share/applications/Alacritty.desktop":
                ENTRY.format(name="Alacritty user", exec="alacritty-user"),
            "usr/share/applications/Alacritty.desktop":
                ENTRY.format(name="Alacritty system", exec="alacritty-system"),
        },
        ["bin/alacritty-user", "bin/alacritty-system"],
        ["--print-id", "--print-path", "--print-cmd"],
    )
    add(
        "c13-arg-composition",
        "title-dir-appid-hold",
        dict(hypr, **std),
        {
            "home/.config/xdg-terminals.list": "Alacritty.desktop\n",
            "home/.local/share/applications/Alacritty.desktop":
                ENTRY.format(name="Alacritty", exec="alacritty")
                + "TerminalArgAppId=--class=\nTerminalArgTitle=--title=\n"
                "TerminalArgDir=--working-directory\nTerminalArgHold=--hold\n",
        },
        ["bin/alacritty"],
        [
            "--print-cmd",
            "--app-id=app.x",
            "--title=hello world",
            "--dir=$ROOT/work",
            "--hold",
            "--",
            "sh",
            "-c",
            "echo hi",
        ],
    )
    add(
        "c14-cache-disabled",
        "disable-cache-directive",
        dict(hypr, **std),
        {
            "home/.config/xdg-terminals.list": "/disable_cache\nAlacritty.desktop\n",
            "home/.local/share/applications/Alacritty.desktop":
                ENTRY.format(name="Alacritty", exec="alacritty"),
        },
        ["bin/alacritty"],
        ["--print-id", "--print-path", "--print-cmd"],
    )
    add(
        "c15-exec-quoting",
        "exec-quoting-and-field-code",
        dict(hypr, **std),
        {
            "home/.config/xdg-terminals.list": "Alacritty.desktop\n",
            "home/.local/share/applications/Alacritty.desktop":
                ENTRY.format(
                    name="Alacritty",
                    exec='alacritty -e "hello world" %f --flag=\\\\s',
                ),
        },
        ["bin/alacritty"],
        ["--print-cmd"],
    )
    big = ENTRY.format(name="Alacritty", exec="alacritty") + "".join(
        "# pad line %04d\n" % i for i in range(2000)
    )
    add(
        "c16-print-content-large",
        "print-content",
        dict(hypr, **std),
        {
            "home/.config/xdg-terminals.list": "Alacritty.desktop\n",
            "home/.local/share/applications/Alacritty.desktop": big,
        },
        ["bin/alacritty"],
        ["--print-content"],
    )
    return out


def materialize(cid, files, execs, root):
    if os.path.isdir(root):
        shutil.rmtree(root)
    os.makedirs(os.path.join(root, "home"))
    os.makedirs(os.path.join(root, "bin"))
    for rel, text in files.items():
        dest = os.path.join(root, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8", newline="") as fh:
            fh.write(text.replace("$ROOT", root))
    for rel in execs:
        dest = os.path.join(root, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if not os.path.exists(dest):
            with open(dest, "w", encoding="utf-8", newline="") as fh:
                fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(dest, 0o755)


def build_toolbin(scratch):
    toolbin = os.path.join(scratch, "toolbin")
    if os.path.isdir(toolbin):
        shutil.rmtree(toolbin)
    os.makedirs(toolbin)
    for name in EXTERNALS:
        src = shutil.which(name)
        if not src:
            sys.exit("missing host command: %s" % name)
        os.symlink(os.path.realpath(src), os.path.join(toolbin, name))
    return toolbin


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--receipts", default=None)
    args = ap.parse_args(argv)
    scratch = os.path.abspath(args.scratch)
    os.makedirs(scratch, exist_ok=True)
    if sha256(PIN) != PIN_SHA:
        sys.exit("pinned script sha256 mismatch")
    toolbin = build_toolbin(scratch)
    fixtures = []
    hostref = []
    for cid, cls, env, files, execs, cargs in cases():
        if not any(a.startswith("--print-") for a in cargs):
            sys.exit("generator only allows print modes: %s" % cid)
        root = os.path.join(scratch, cid)
        materialize(cid, files, execs, root)
        resolved = {k: v.replace("$ROOT", root) for k, v in env.items()}
        cache = os.path.join(scratch, "cache", cid)
        if os.path.isdir(cache):
            shutil.rmtree(cache)
        os.makedirs(cache)
        real_args = [a.replace("$ROOT", root) for a in cargs]
        run_env = dict(resolved)
        run_env["HOME"] = os.path.join(root, "home")
        run_env["PATH"] = os.path.join(root, "bin") + ":" + toolbin
        run_env["XDG_CACHE_HOME"] = cache
        proc = subprocess.run(
            [PIN] + real_args,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            env=run_env,
        )
        stdout = proc.stdout.decode("utf-8", "surrogateescape").replace(root, "$ROOT")
        hostref.append(
            {
                "id": cid,
                "rc": proc.returncode,
                "stdout": stdout,
                "stderr_digest": hashlib.sha256(proc.stderr).hexdigest()[:32],
                "path_shape": "$ROOT/bin:<TOOLBIN>",
            }
        )
        fixtures.append(
            {
                "id": cid,
                "class": cls,
                "env": env,
                "files": files,
                "exec": execs,
                "args": cargs,
                "expect": {"rc": proc.returncode, "stdout": stdout},
            }
        )
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(fixtures, fh, indent=1, sort_keys=True)
        fh.write("\n")
    if args.receipts:
        os.makedirs(args.receipts, exist_ok=True)
        with open(os.path.join(args.receipts, "host-reference.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(
                {"pin": PIN, "pin_sha256": PIN_SHA, "cases": hostref},
                fh,
                indent=1,
                sort_keys=True,
            )
            fh.write("\n")
    print("generated %d fixtures -> %s" % (len(fixtures), args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
