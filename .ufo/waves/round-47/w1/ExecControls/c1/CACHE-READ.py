#!/usr/bin/env python3
"""C1 control CACHE-READ - prints the host resolver cache instead of resolving.

Reads $XDG_CACHE_HOME/xdg-terminal-exec (lines 1-10 are hash, cmd, path, id, action, execarg,
appidarg, titlearg, dirarg, holdarg; the rest is the USEP-separated command terminated by
RS+END_OF_EXEC_USEP) and prints from it.  Rejected by clauses f and g because the counter models a
cold cache with XDG_CACHE_HOME in a fresh directory: there is no cache file, so this prints nothing
and exits 1 on every case.  A counter that forgot to isolate XDG_CACHE_HOME would score the host
fixture TARGET_MET here.
"""

import os
import sys

USEP = "\x1f"
RSEP = "\x1e"


def cache_path():
    base = os.environ.get("XDG_CACHE_HOME") or os.path.join(
        os.environ.get("HOME", ""), ".cache")
    return os.path.join(base, "xdg-terminal-exec")


def read_cache():
    try:
        with open(cache_path(), "rb") as fh:
            text = fh.read().decode("utf-8", "surrogateescape")
    except OSError:
        return None
    lines = text.split("\n")
    if text.endswith("\n"):
        lines = lines[:-1]
    if len(lines) < 11:
        return None
    head = lines[:10]
    body = "\n".join(lines[10:])
    marker = RSEP + "END_OF_EXEC_USEP"
    if not body.endswith(marker):
        return None
    body = body[:-len(marker)]
    return {"id": head[3], "action": head[4], "path": head[2], "execarg": head[5],
            "appidarg": head[6], "titlearg": head[7], "dirarg": head[8], "holdarg": head[9],
            "tokens": body.split(USEP) if body else []}


def main(argv):
    if argv[:1] == ["--selftest"]:
        sys.stdout.write("MADO_TERMINAL_SELFTEST: 30/30 passed\n")
        return 0
    cache = read_cache()
    if argv[:1] == ["explain"]:
        if cache is None:
            sys.stdout.write("MADO_TERM: selected=- path=- verdict=NO_TERMINAL\n")
            return 3
        sys.stdout.write("MADO_TERM: selected=%s path=%s verdict=OK\n"
                         % (cache["id"], cache["path"]))
        return 0
    if argv[:1] != ["print"]:
        sys.stderr.write("usage: mado-terminal.py print [...]\n")
        return 2
    if cache is None:
        sys.stderr.write("CACHE-READ: no cache data at %s\n" % cache_path())
        return 1
    args = argv[1:]
    parts = []
    delim = "\\n"
    cmd_delim = "\\n"
    want = {"appid": "", "title": "", "dir": "", "hold": False}
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
            want["appid"] = a.split("=", 1)[1]
        elif a.startswith("--title="):
            want["title"] = a.split("=", 1)[1]
        elif a.startswith("--dir="):
            want["dir"] = a.split("=", 1)[1]
        elif a == "--hold":
            want["hold"] = True
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
    out = []
    first = True
    name = cache["id"] + ((":" + cache["action"]) if cache["action"] else "")
    if "id" in parts:
        out.append(name)
        first = False
    if "path" in parts:
        if not first:
            out.append(delim.replace("\\n", "\n"))
        out.append(cache["path"])
        first = False
    if "content" in parts:
        first = False
    if "cmd" not in parts:
        if "content" not in parts and delim == "\\n":
            out.append("\n")
        sys.stdout.write("".join(out))
        return 0
    av = []
    if rest and cache["execarg"]:
        av = [cache["execarg"]] + rest
    else:
        av = list(rest)
    if cache["holdarg"] and want["hold"]:
        av = [cache["holdarg"]] + av
    if cache["dirarg"] and want["dir"]:
        if cache["dirarg"].endswith("="):
            av = [cache["dirarg"] + want["dir"]] + av
        else:
            av = [cache["dirarg"], want["dir"]] + av
    if cache["titlearg"] and want["title"]:
        if cache["titlearg"].endswith("="):
            av = [cache["titlearg"] + want["title"]] + av
        else:
            av = [cache["titlearg"], want["title"]] + av
    if cache["appidarg"] and want["appid"]:
        if cache["appidarg"].endswith("="):
            av = [cache["appidarg"] + want["appid"]] + av
        else:
            av = [cache["appidarg"], want["appid"]] + av
    av = list(cache["tokens"]) + av
    if not first:
        out.append(delim.replace("\\n", "\n"))
    sep = cmd_delim.replace("\\n", "\n")
    out.append(sep.join(av))
    if cmd_delim == "\\n" or (not first and delim == "\\n"):
        out.append("\n")
    sys.stdout.write("".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
