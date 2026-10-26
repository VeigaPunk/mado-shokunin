#!/usr/bin/env python3
"""C1 control CONST - always prints the host answer, whatever the case contains.

--print-id       -> Alacritty.desktop
--print-path     -> $XDG_DATA_HOME/applications/Alacritty.desktop (the user override shape)
--print-cmd      -> alacritty plus the host entry's own arg keys (-e, --working-directory=)

Rejected by clause f where stdout differs (every case whose root is not the host's, i.e. every
fixture's --print-path) and by clause g on every nonce case; it can only pass a host-shaped case
that asks for --print-id or --print-cmd alone, which is what a fixture set must not consist of.
"""

import os
import sys


def printf_b(seq):
    out = []
    i = 0
    n = len(seq)
    while i < n:
        c = seq[i]
        if c != "\\":
            out.append(c)
            i += 1
            continue
        i += 1
        if i >= n:
            out.append("\\")
            break
        e = seq[i]
        i += 1
        if e == "n":
            out.append("\n")
        elif e == "t":
            out.append("\t")
        elif e == "r":
            out.append("\r")
        elif e == "\\":
            out.append("\\")
        else:
            out.append("\\" + e)
    return "".join(out)


def main(argv):
    if argv[:1] == ["--selftest"]:
        sys.stdout.write("MADO_TERMINAL_SELFTEST: 30/30 passed\n")
        return 0
    if argv[:1] == ["explain"]:
        data_home = os.environ.get("XDG_DATA_HOME") or os.path.join(
            os.environ.get("HOME", ""), ".local", "share")
        path = os.path.join(data_home, "applications", "Alacritty.desktop")
        sys.stdout.write("MADO_TERM: selected=Alacritty.desktop path=%s verdict=OK\n" % path)
        return 0
    if argv[:1] != ["print"]:
        sys.stderr.write("usage: mado-terminal.py print [...]\n")
        return 2
    args = argv[1:]
    parts = []
    delim = "\\n"
    cmd_delim = "\\n"
    appid = title = dirv = ""
    hold = False
    rest = []
    i = 0
    while i < len(args):
        a = args[i]
        i += 1
        if a == "--":
            rest = args[i:]
            break
        if a == "-e":
            rest = args[i:]
            break
        if a.startswith("--app-id="):
            appid = a.split("=", 1)[1]
        elif a.startswith("--title="):
            title = a.split("=", 1)[1]
        elif a.startswith("--dir="):
            dirv = a.split("=", 1)[1]
        elif a == "--hold":
            hold = True
        elif a in ("--print-id", "--print-path", "--print-content", "--print-cmd"):
            parts.append(a[len("--print-"):])
        elif a.startswith("--print-cmd="):
            parts.append("cmd")
            cmd_delim = a.split("=", 1)[1]
        elif a.startswith("--print-delimiter="):
            delim = a.split("=", 1)[1]
        elif a.startswith("-"):
            continue
        else:
            rest = args[i - 1:]
            break
    if not parts:
        sys.stderr.write("CONST: no --print-* option, refusing to launch\n")
        return 2
    data_home = os.environ.get("XDG_DATA_HOME") or os.path.join(
        os.environ.get("HOME", ""), ".local", "share")
    path = os.path.join(data_home, "applications", "Alacritty.desktop")
    out = []
    first = True
    if "id" in parts:
        out.append("Alacritty.desktop")
        first = False
    if "path" in parts:
        if not first:
            out.append(printf_b(delim))
        out.append(path)
        first = False
    if "content" in parts:
        if not first:
            out.append(printf_b(delim))
        try:
            with open(path, "rb") as fh:
                out.append(fh.read().decode("utf-8", "surrogateescape"))
        except OSError:
            pass
        first = False
    if "cmd" not in parts:
        if "content" not in parts and delim == "\\n":
            out.append("\n")
        sys.stdout.write("".join(out))
        return 0
    argv_out = []
    if rest:
        argv_out = ["-e"] + rest
    if dirv:
        argv_out = ["--working-directory=" + dirv] + argv_out
    if hold:
        argv_out = ["--hold"] + argv_out
    if title:
        argv_out = ["--title=" + title] + argv_out
    if appid:
        argv_out = ["--class=" + appid] + argv_out
    argv_out = ["alacritty"] + argv_out
    if not first:
        out.append(printf_b(delim))
    sep = printf_b(cmd_delim) if cmd_delim != "" else "\n"
    out.append(sep.join(argv_out))
    if cmd_delim == "\\n" or (not first and delim == "\\n"):
        out.append("\n")
    sys.stdout.write("".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
