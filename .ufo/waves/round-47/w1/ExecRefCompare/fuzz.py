#!/usr/bin/env python3
"""Grammar fuzzer for the selection chain of xdg-terminal-exec 0.14.3.

Pinned target: /usr/bin/xdg-terminal-exec
  sha256 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac

The fuzzer only ever invokes the target with a --print-* option (never bare: a
bare invocation launches a terminal). Every run gets a fresh, empty
XDG_CACHE_HOME inside the work directory (cold cache) and a restricted PATH of
$ROOT/bin (executable stubs) + a tool bin of symlinks to the host's
tr/find/awk/ls/md5sum/mkdir/rm.

Case schema = the frozen round-47 fixture schema
    {"id","class","env","files","exec","args","expect":{"rc","stdout"}}
plus one fuzzer-only key, "setup", used to express things a text map cannot:
    {"setup":{"symlinks":{rel:target},"modes":{rel:int}}}
It is stripped from nothing: a judge that ignores "setup" simply sees a case
without the symlink/mode. expect is always produced by running the real script
on the materialized case, never typed by hand.

Usage:
  fuzz.py run  [--work DIR] [--out DIR] [--seed S] [--random N]
  fuzz.py case FILE [--work DIR]      # replay one case: rc + stdout + stderr
"""
import argparse
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile

SCRIPT = "/usr/bin/xdg-terminal-exec"
PIN = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"
TOOLS = ("tr", "find", "awk", "md5sum", "ls", "mkdir", "rm")
SELECT = ["--print-id", "--print-path", "--print-cmd"]

WORK = None      # scratch work dir (TMPDIR / --work)
TOOLBIN = None   # dir with symlinks to host tools
ROOTS = []       # case roots, deleted at the end (background save_cache races)


# --------------------------------------------------------------------------- #
# sandbox
# --------------------------------------------------------------------------- #
def make_toolbin(work):
    tb = os.path.join(work, "toolbin")
    os.makedirs(tb, exist_ok=True)
    for t in TOOLS:
        src = shutil.which(t)
        if not src:
            raise SystemExit("required tool not on host PATH: %s" % t)
        dst = os.path.join(tb, t)
        if not os.path.lexists(dst):
            os.symlink(os.path.realpath(src), dst)
    return tb


def _write(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def materialize(case, root):
    os.makedirs(os.path.join(root, "home"), exist_ok=True)
    os.makedirs(os.path.join(root, "bin"), exist_ok=True)
    os.makedirs(os.path.join(root, "cache"), exist_ok=True)  # cold, empty
    for rel, text in (case.get("files") or {}).items():
        _write(os.path.join(root, rel), text)
    setup = case.get("setup") or {}
    for rel, target in (setup.get("symlinks") or {}).items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
        if os.path.lexists(p):
            os.unlink(p)
        os.symlink(target, p)
    for rel in case.get("exec") or []:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
        if os.path.lexists(p):
            os.unlink(p)
        _write(p, "#!/bin/sh\nexit 0\n")
        os.chmod(p, 0o755)
    for rel, mode in (setup.get("modes") or {}).items():
        os.chmod(os.path.join(root, rel), mode)


def run_case(case):
    root = tempfile.mkdtemp(prefix="c-", dir=WORK)
    ROOTS.append(root)
    materialize(case, root)
    env = {
        "HOME": root + "/home",
        "PATH": root + "/bin:" + TOOLBIN,
        "XDG_CACHE_HOME": root + "/cache",
    }
    for k, v in (case.get("env") or {}).items():
        env[k] = v.replace("$ROOT", root)
    args = [a.replace("$ROOT", root) for a in case.get("args") or SELECT]
    try:
        p = subprocess.run(
            [SCRIPT] + args,
            env=env,
            cwd=root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
        )
        out = p.stdout.decode("utf-8", "backslashreplace")
        err = p.stderr.decode("utf-8", "backslashreplace")
        rc = p.returncode
    except subprocess.TimeoutExpired:
        out, err, rc = "", "<TIMEOUT>", -9
    norm = out.replace(root, "$ROOT")
    return {
        "rc": rc,
        "stdout": norm,
        "stderr": err.replace(root, "$ROOT"),
        "root": root,
    }


def finish_case(case):
    r = run_case(case)
    case = dict(case)
    case["expect"] = {"rc": r["rc"], "stdout": r["stdout"]}
    return case, r


# --------------------------------------------------------------------------- #
# case constructors
# --------------------------------------------------------------------------- #
def base(cid, cls, env=None, files=None, execs=None, args=None, setup=None):
    e = {
        "XDG_CURRENT_DESKTOP": "Hyprland",
        "XDG_CONFIG_HOME": "$ROOT/home/.config",
        "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
        "XDG_DATA_HOME": "$ROOT/home/.local/share",
        "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share",
    }
    if env:
        for k, v in env.items():
            if v is None:
                e.pop(k, None)
            else:
                e[k] = v
    c = {
        "id": cid,
        "class": cls,
        "env": e,
        "files": dict(files or {}),
        "exec": list(execs or ["bin/alacritty"]),
        "args": list(args or SELECT),
    }
    if setup:
        c["setup"] = setup
    return c


def entry(*lines, header="[Desktop Entry]"):
    body = [header] + list(lines) if header is not None else list(lines)
    return "\n".join(body) + "\n"


E = "home/.local/share/applications/Alacritty.desktop"
L = "home/.config/xdg-terminals.list"


def simple_case(cid, cls, entrytext=None, listtext=None, env=None, execs=None,
                args=None, extra_files=None, setup=None, listdir="home/.config"):
    files = {
        "home/.local/share/applications/Alacritty.desktop":
            entrytext if entrytext is not None else entry(
                "Name=Alacritty", "Type=Application",
                "Categories=TerminalEmulator;", "Exec=alacritty",
                "TerminalArgExec=-e"),
    }
    if listtext is not None:
        files[listdir + "/xdg-terminals.list"] = listtext
    if extra_files:
        files.update(extra_files)
    return base(cid, cls, env=env, files=files, execs=execs, args=args,
                setup=setup)


# --------------------------------------------------------------------------- #
# families: base + one-token deltas (flip detection)
# --------------------------------------------------------------------------- #
def families():
    fam = []
    A = "home/.local/share/applications/Alacritty.desktop"
    B = "usr/share/applications/Foot.desktop"
    both_exec = ["bin/alacritty", "bin/foot"]

    def add(fid, cls, mk, variants):
        fam.append((fid, cls, mk, variants))

    # F01 list-line whitespace / trimming
    add("F01", "list/whitespace",
        lambda: simple_case("F01-", "list/whitespace", listtext="foot.desktop\n",
                            extra_files={B: entry("Categories=TerminalEmulator;",
                                                  "Exec=foot")},
                            execs=both_exec),
        [("plain", lambda c: c),
         ("lead-space", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                       " foot.desktop\n")),
         ("trail-space", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                        "foot.desktop   \n")),
         ("tab", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                "\tfoot.desktop\t\n")),
         ("inline-comment", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                           "foot.desktop # preferred\n")),
         ("crlf", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                 "foot.desktop\r\n"))])

    # F02 Categories trailing semicolon
    add("F02", "entry/categories-semicolon",
        lambda: simple_case("F02-", "entry/categories-semicolon"),
        [("trailing-semi", lambda c: c),
         ("no-trailing-semi", lambda c: _sub(c, A, "Categories=TerminalEmulator;",
                                             "Categories=TerminalEmulator")),
         ("double-semi", lambda c: _sub(c, A, "Categories=TerminalEmulator;",
                                        "Categories=TerminalEmulator;;")),
         ("with-peers", lambda c: _sub(c, A, "Categories=TerminalEmulator;",
                                       "Categories=System;TerminalEmulator;")),
         ("semi-space", lambda c: _sub(c, A, "Categories=TerminalEmulator;",
                                       "Categories=TerminalEmulator; "))])

    # F03 key/value whitespace
    add("F03", "entry/key-whitespace",
        lambda: simple_case("F03-", "entry/key-whitespace"),
        [("clean", lambda c: c),
         ("value-trail-space", lambda c: _sub(c, A, "Categories=TerminalEmulator;",
                                              "Categories=TerminalEmulator;   ")),
         ("space-before-eq", lambda c: _sub(c, A, "Exec=alacritty",
                                            "Exec = alacritty")),
         ("tab-before-key", lambda c: _sub(c, A, "Exec=alacritty",
                                           "\tExec=alacritty")),
         ("indented-value", lambda c: _sub(c, A, "Exec=alacritty",
                                           "Exec=    alacritty"))])

    # F04 duplicate keys
    add("F04", "entry/duplicate-key",
        lambda: simple_case("F04-", "entry/duplicate-key"),
        [("single-cat", lambda c: c),
         ("cat-second-bad", lambda c: _sub(c, A, "Categories=TerminalEmulator;",
                                           "Categories=TerminalEmulator;\nCategories=Xterm;")),
         ("cat-second-good", lambda c: _sub(c, A, "Categories=TerminalEmulator;",
                                            "Categories=Xterm;\nCategories=TerminalEmulator;")),
         ("exec-second-missing", lambda c: _sub(c, A, "Exec=alacritty",
                                                "Exec=alacritty\nExec=nothere")),
         ("exec-second-ok", lambda c: _sub(c, A, "Exec=alacritty",
                                           "Exec=nothere\nExec=alacritty")),
         ("hidden-second", lambda c: _sub(c, A, "Exec=alacritty",
                                          "Exec=alacritty\nHidden=true"))])

    # F05 group headers
    add("F05", "entry/group-header",
        lambda: simple_case("F05-", "entry/group-header"),
        [("exact", lambda c: c),
         ("suffix-text", lambda c: _sub(c, A, "[Desktop Entry]",
                                        "[Desktop Entry] comment")),
         ("unclosed", lambda c: _sub(c, A, "[Desktop Entry]", "[Desktop Entry")),
         ("wrong-group-first", lambda c: _sub(c, A, "[Desktop Entry]",
                                              "[Desktop EntryX]\n[Desktop Entry]")),
         ("kde-group", lambda c: _sub(c, A, "[Desktop Entry]", "[KDE Entry]"))])

    # F06 Hidden casing
    add("F06", "entry/hidden-case",
        lambda: simple_case("F06-", "entry/hidden-case"),
        [("absent", lambda c: c),
         ("true", lambda c: _sub(c, A, "Exec=alacritty", "Exec=alacritty\nHidden=true")),
         ("True", lambda c: _sub(c, A, "Exec=alacritty", "Exec=alacritty\nHidden=True")),
         ("TRUE", lambda c: _sub(c, A, "Exec=alacritty", "Exec=alacritty\nHidden=TRUE")),
         ("one", lambda c: _sub(c, A, "Exec=alacritty", "Exec=alacritty\nHidden=1")),
         ("spaced", lambda c: _sub(c, A, "Exec=alacritty", "Exec=alacritty\nHidden= true"))])

    # F07 symlinked entry
    add("F07", "entry/symlink",
        lambda: base("F07-", "entry/symlink",
                     files={"usr/share/applications/real/Real.desktop":
                            entry("Categories=TerminalEmulator;", "Exec=alacritty"),
                            "home/.config/xdg-terminals.list": "Linked.desktop\n"},
                     setup={"symlinks": {"home/.local/share/applications/Linked.desktop":
                                         "../../../../usr/share/applications/real/Real.desktop"}}),
        [("linked", lambda c: c),
         ("dangling", lambda c: base("F07-dangling", "entry/symlink",
                                     files={"home/.config/xdg-terminals.list":
                                            "Linked.desktop\n"},
                                     setup={"symlinks": {"home/.local/share/applications/Linked.desktop":
                                                         "../../nowhere/Real.desktop"}}))])

    # F08 unreadable entry
    add("F08", "entry/unreadable",
        lambda: simple_case("F08-", "entry/unreadable"),
        [("readable", lambda c: c),
         ("mode000", lambda c: _with(c, "setup", {"modes": {A: 0o000}})),
         ("mode000-second", lambda c: simple_case(
             "F08-mode000-second", "entry/unreadable",
             extra_files={"home/.local/share/applications/Zed.desktop":
                          entry("Categories=TerminalEmulator;", "Exec=alacritty")},
             setup={"modes": {"home/.local/share/applications/Zed.desktop": 0o000}}))])

    # F09 dash = subdirectory in ID
    add("F09", "entry/id-dash-subdir",
        lambda: base("F09-", "entry/id-dash-subdir",
                     files={"home/.local/share/applications/sub/Foo.desktop":
                            entry("Categories=TerminalEmulator;", "Exec=alacritty"),
                            "home/.config/xdg-terminals.list": "sub-Foo.desktop\n"}),
        [("dash-id", lambda c: c),
         ("slash-id", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                     "sub/Foo.desktop\n")),
         ("dot-id", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                   ".Foo.desktop\n")),
         ("trailing-dot", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                         "sub-Foo.desktop.\n"))])

    # F10 XDG_DATA_DIRS shape
    add("F10", "env/data-dirs-shape",
        lambda: base("F10-", "env/data-dirs-shape",
                     files={"usr/share/applications/Foot.desktop":
                            entry("Categories=TerminalEmulator;", "Exec=foot"),
                            "usr/local/share/applications/Alacritty.desktop":
                            entry("Categories=TerminalEmulator;", "Exec=alacritty")},
                     execs=both_exec),
        [("two-dirs", lambda c: c),
         ("leading-colon", lambda c: _env(c, "XDG_DATA_DIRS",
                                          ":$ROOT/usr/share")),
         ("trailing-colon", lambda c: _env(c, "XDG_DATA_DIRS",
                                           "$ROOT/usr/share:")),
         ("double-colon", lambda c: _env(c, "XDG_DATA_DIRS",
                                         "$ROOT/usr/share::$ROOT/usr/local/share")),
         ("trailing-slash", lambda c: _env(c, "XDG_DATA_DIRS",
                                           "$ROOT/usr/share/")),
         ("dot-segment", lambda c: _env(c, "XDG_DATA_DIRS",
                                        "$ROOT/usr/./share"))])

    # F11 XDG_CURRENT_DESKTOP shape
    add("F11", "env/current-desktop",
        lambda: base("F11-", "env/current-desktop",
                     files={"home/.local/share/applications/Alacritty.desktop":
                            entry("Categories=TerminalEmulator;", "Exec=alacritty"),
                            "home/.config/hyprland-xdg-terminals.list":
                            "Alacritty.desktop\n",
                            "home/.config/gnome-xdg-terminals.list":
                            "-Alacritty.desktop\n"}),
        [("Hyprland", lambda c: c),
         ("hyprland", lambda c: _env(c, "XDG_CURRENT_DESKTOP", "hyprland")),
         ("HYPRLAND", lambda c: _env(c, "XDG_CURRENT_DESKTOP", "HYPRLAND")),
         ("colon-list", lambda c: _env(c, "XDG_CURRENT_DESKTOP", "Hyprland:GNOME")),
         ("unset", lambda c: _env(c, "XDG_CURRENT_DESKTOP", None)),
         ("semi", lambda c: _env(c, "XDG_CURRENT_DESKTOP", "Hyprland;GNOME"))])

    # F12 duplicate ID in two data dirs
    add("F12", "entry/duplicate-across-dirs",
        lambda: base("F12-", "entry/duplicate-across-dirs",
                     files={"usr/share/applications/Same.desktop":
                            entry("Categories=TerminalEmulator;", "Exec=foot"),
                            "home/.local/share/applications/Same.desktop":
                            entry("Categories=TerminalEmulator;", "Exec=alacritty")},
                     execs=both_exec),
        [("both", lambda c: c),
         ("list-one", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                     "Same.desktop\n")),
         ("system-only", lambda c: base(
             "F12-system-only", "entry/duplicate-across-dirs",
             files={"usr/share/applications/Same.desktop":
                    entry("Categories=TerminalEmulator;", "Exec=foot")},
             execs=both_exec))])

    # F13 actions
    add("F13", "entry/action",
        lambda: simple_case("F13-", "entry/action", args=["--print-id", "--print-path"])
        ,
        [("no-action", lambda c: c),
         ("listed-action", lambda c: simple_case(
             "F13-listed", "entry/action", listtext="Alacritty.desktop:New\n",
             entrytext=entry("Categories=TerminalEmulator;", "Exec=alacritty",
                             "Actions=New;", "[Desktop Action New]",
                             "Exec=alacritty --new"),
             args=["--print-id", "--print-path", "--print-cmd"])),
         ("unlisted-action", lambda c: simple_case(
             "F13-unlisted", "entry/action", listtext="Alacritty.desktop:New\n",
             entrytext=entry("Categories=TerminalEmulator;", "Exec=alacritty"),
             args=["--print-id"])),
         ("action-group-before-actions", lambda c: simple_case(
             "F13-order", "entry/action", listtext="Alacritty.desktop:New\n",
             entrytext=entry("Categories=TerminalEmulator;", "Exec=alacritty",
                             "[Desktop Action New]", "Exec=alacritty --new",
                             "Actions=New;"),
             args=["--print-id"])),
         ("action-header-suffix", lambda c: simple_case(
             "F13-suffix", "entry/action", listtext="Alacritty.desktop:New\n",
             entrytext=entry("Categories=TerminalEmulator;", "Exec=alacritty",
                             "Actions=New;", "[Desktop Action New] extra",
                             "Exec=alacritty --new"),
             args=["--print-cmd"]))])

    # F14 Exec tokenizing and % fields
    add("F14", "entry/exec-grammar",
        lambda: simple_case("F14-", "entry/exec-grammar"),
        [("plain", lambda c: c),
         ("unclosed-quote", lambda c: _sub(c, A, "Exec=alacritty",
                                           'Exec=alacritty "unclosed')),
         ("unquoted-semicolon", lambda c: _sub(c, A, "Exec=alacritty",
                                               "Exec=alacritty;x")),
         ("field-f", lambda c: _sub(c, A, "Exec=alacritty",
                                    "Exec=alacritty %F")),
         ("field-bad", lambda c: _sub(c, A, "Exec=alacritty",
                                      "Exec=alacritty %b --keep")),
         ("field-double-fu", lambda c: _sub(c, A, "Exec=alacritty",
                                            "Exec=alacritty %f %u")),
         ("field-escaped", lambda c: _sub(c, A, "Exec=alacritty",
                                          "Exec=alacritty 100%%")),
         ("trailing-backslash", lambda c: _sub(c, A, "Exec=alacritty",
                                               "Exec=alacritty \\")),
         ("empty-exec", lambda c: _sub(c, A, "Exec=alacritty", "Exec="))])

    # F15 list fallback control and nonexistent ids
    add("F15", "list/fallback-control",
        lambda: base("F15-", "list/fallback-control",
                     files={"home/.local/share/applications/Alacritty.desktop":
                            entry("Categories=TerminalEmulator;", "Exec=alacritty"),
                            "usr/share/applications/Foot.desktop":
                            entry("Categories=TerminalEmulator;", "Exec=foot"),
                            "home/.config/xdg-terminals.list": "Ghost.desktop\n"},
                     execs=both_exec),
        [("ghost-then-fallback", lambda c: c),
         ("exclude-foot", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                         "-Foot.desktop\n")),
         ("include-foot-excluded", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                                  "-Foot.desktop\n+Foot.desktop\n")),
         ("exclude-then-list", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                              "-Foot.desktop\nFoot.desktop\n"))])

    # F16 show-in rules on explicit vs fallback
    add("F16", "entry/showin",
        lambda: base("F16-", "entry/showin",
                     files={"usr/share/applications/Foot.desktop":
                            entry("Categories=TerminalEmulator;", "Exec=foot",
                                  "NotShowIn=Hyprland;")},
                     execs=both_exec),
        [("fallback", lambda c: c),
         ("explicit", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                     "Foot.desktop\n")),
         ("onlyshowin-miss", lambda c: base(
             "F16-onlyshowin", "entry/showin",
             files={"usr/share/applications/Foot.desktop":
                    entry("Categories=TerminalEmulator;", "Exec=foot",
                          "OnlyShowIn=GNOME;")}, execs=both_exec))])

    # F17 fallback ordering: two entries, reverse discovery by list
    add("F17", "order/fallback-selection",
        lambda: base("F17-", "order/fallback-selection",
                     files={"usr/share/applications/AAA.desktop":
                            entry("Categories=TerminalEmulator;", "Exec=foot"),
                            "usr/share/applications/ZZZ.desktop":
                            entry("Categories=TerminalEmulator;", "Exec=alacritty")},
                     execs=both_exec),
        [("natural", lambda c: c),
         ("list-zzz-first", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                           "ZZZ.desktop\nAAA.desktop\n")),
         ("list-reversed", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                          "AAA.desktop\nZZZ.desktop\n"))])

    # F18 print-mode combinations and delimiters
    add("F18", "print/delimiters",
        lambda: simple_case("F18-", "print/delimiters"),
        [("all-default", lambda c: c),
         ("cmd-only", lambda c: base("F18-cmd-only", "print/delimiters",
                                     files=dict(simple_case("x", "y")["files"]),
                                     args=["--print-cmd"])),
         ("delim-pipe", lambda c: base("F18-delim-pipe", "print/delimiters",
                                       files=dict(simple_case("x", "y")["files"]),
                                       args=["--print-id", "--print-path",
                                             "--print-delimiter=|"])),
         ("cmd-delim-comma", lambda c: base("F18-cmd-comma", "print/delimiters",
                                            files=dict(simple_case("x", "y")["files"]),
                                            args=["--print-cmd=,"])),
         ("id-only", lambda c: base("F18-id-only", "print/delimiters",
                                    files=dict(simple_case("x", "y")["files"]),
                                    args=["--print-id"])),
         ("content", lambda c: base("F18-content", "print/delimiters",
                                    files=dict(simple_case("x", "y")["files"]),
                                    args=["--print-content"]))])

    # F19 compat / strict directives
    add("F19", "list/directive-execarg",
        lambda: simple_case("F19-", "list/directive-execarg",
                            entrytext=entry("Categories=TerminalEmulator;",
                                            "Exec=alacritty"),
                            listtext="Alacritty.desktop\n"),
        [("compat-default", lambda c: c),
         ("strict", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                   "/execarg_strict\nAlacritty.desktop\n")),
         ("compat-then-strict", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                               "/execarg_compat\n/execarg_strict\nAlacritty.desktop\n")),
         ("default-execarg", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                            "/execarg_default:Alacritty.desktop:--x\nAlacritty.desktop\n"))])

    # F20 TryExec / PATH
    add("F20", "entry/tryexec",
        lambda: simple_case("F20-", "entry/tryexec"),
        [("no-tryexec", lambda c: c),
         ("tryexec-ok", lambda c: _sub(c, A, "Exec=alacritty",
                                       "TryExec=alacritty\nExec=alacritty")),
         ("tryexec-missing", lambda c: _sub(c, A, "Exec=alacritty",
                                            "TryExec=ghost\nExec=alacritty")),
         ("exec-not-path", lambda c: _sub(c, A, "Exec=alacritty",
                                          "Exec=ghost")),
         ("exec-absolute", lambda c: _sub(c, A, "Exec=alacritty",
                                          "Exec=$ROOT/bin/alacritty"))])

    # F21 file naming / find filter
    add("F21", "entry/find-filter",
        lambda: base("F21-", "entry/find-filter",
                     files={"home/.local/share/applications/Ok.desktop":
                            entry("Categories=TerminalEmulator;", "Exec=alacritty")}),
        [("ok", lambda c: c),
         ("uppercase-ext", lambda c: base(
             "F21-upper", "entry/find-filter",
             files={"home/.local/share/applications/Ok.Desktop":
                    entry("Categories=TerminalEmulator;", "Exec=alacritty")})),
         ("space-in-name", lambda c: base(
             "F21-space", "entry/find-filter",
             files={"home/.local/share/applications/Ok Two.desktop":
                    entry("Categories=TerminalEmulator;", "Exec=alacritty")})),
         ("leading-dot", lambda c: base(
             "F21-dot", "entry/find-filter",
             files={"home/.local/share/applications/.Hidden.desktop":
                    entry("Categories=TerminalEmulator;", "Exec=alacritty")})),
         ("no-ext", lambda c: base(
             "F21-noext", "entry/find-filter",
             files={"home/.local/share/applications/Ok":
                    entry("Categories=TerminalEmulator;", "Exec=alacritty")}))])

    # F22 desktop-specific list files for a colon-joined desktop
    add("F22", "list/desktop-specific",
        lambda: base("F22-", "list/desktop-specific",
                     files={"home/.local/share/applications/Alacritty.desktop":
                            entry("Categories=TerminalEmulator;", "Exec=alacritty"),
                            "usr/share/applications/Foot.desktop":
                            entry("Categories=TerminalEmulator;", "Exec=foot"),
                            "home/.config/hyprland-xdg-terminals.list":
                            "Foot.desktop\n",
                            "home/.config/gnome-xdg-terminals.list":
                            "Alacritty.desktop\n"},
                     execs=both_exec),
        [("single-desktop", lambda c: c),
         ("joined-desktop", lambda c: _env(c, "XDG_CURRENT_DESKTOP",
                                           "Hyprland:GNOME")),
         ("joined-reversed", lambda c: _env(c, "XDG_CURRENT_DESKTOP",
                                            "GNOME:Hyprland"))])

    # F23 list file in a data dir (xdg-terminal-exec/) vs config dir
    add("F23", "list/data-dir-list",
        lambda: base("F23-", "list/data-dir-list",
                     files={"home/.local/share/applications/Alacritty.desktop":
                            entry("Categories=TerminalEmulator;", "Exec=alacritty"),
                            "usr/share/applications/Foot.desktop":
                            entry("Categories=TerminalEmulator;", "Exec=foot"),
                            "usr/share/xdg-terminal-exec/xdg-terminals.list":
                            "Foot.desktop\n"},
                     execs=both_exec),
        [("data-list", lambda c: c),
         ("both-lists", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                       "Alacritty.desktop\n")),
         ("config-overrides", lambda c: _set(c, "home/.config/xdg-terminals.list",
                                             "Foot.desktop\n"))])
    return fam


def _set(case, path, text):
    case = json.loads(json.dumps(case))
    case["files"][path] = text
    return case


def _sub(case, path, old, new):
    case = json.loads(json.dumps(case))
    case["files"][path] = case["files"][path].replace(old, new)
    return case


def _env(case, key, val):
    case = json.loads(json.dumps(case))
    if val is None:
        case["env"].pop(key, None)
    else:
        case["env"][key] = val
    return case


def _with(case, key, val):
    case = json.loads(json.dumps(case))
    case[key] = val
    return case


# --------------------------------------------------------------------------- #
# random grammar
# --------------------------------------------------------------------------- #
ENTRY_LINES = [
    "Name=Fuzz", "Type=Application", "Type=Link", "Terminal=false",
    "Categories=TerminalEmulator;", "Categories=TerminalEmulator",
    "Categories=;TerminalEmulator;", "Categories=TerminalEmulator;;",
    "Categories=System;TerminalEmulator", "Categories=terminalemulator;",
    "Categories=TerminalEmulatorX;", "Categories=",
    "Exec=alacritty", "Exec=foot", "Exec=ghost",
    'Exec=alacritty --title="a b"', "Exec=alacritty %F", "Exec=alacritty %b",
    "Exec=alacritty 100%%", 'Exec=alacritty "x', "Exec=alacritty;y",
    "Exec =alacritty", "Exec=  alacritty", "Exec=",
    "TryExec=alacritty", "TryExec=ghost", "TryExec=",
    "Hidden=true", "Hidden=True", "Hidden=false", "Hidden=1",
    "OnlyShowIn=Hyprland;", "OnlyShowIn=GNOME;",
    "NotShowIn=Hyprland;", "NotShowIn=GNOME;",
    "Actions=New;", "Actions=New", "Actions=Other;",
    "TerminalArgExec=-e", "X-TerminalArgExec=--", "TerminalArgExec=",
    "X-TerminalArgDir=--working-directory=", "X-TerminalArgTitle=-T",
    "X-TerminalArgAppId=--class=", "X-TerminalArgHold=--hold",
    "ExecArg=-x", "X-ExecArg=-y", "StartupNotify=true",
    "Name", "=value", "-Weird=1",
    "[Desktop Action New]", "[Desktop Action Other]", "[Desktop Entry]",
    " extra=1", "\tIndented=1", "Name = spaced",
]
EXEC_STUBS = ["bin/alacritty", "bin/foot"]


def rand_entry(rng):
    lines = ["[Desktop Entry]"]
    for _ in range(rng.randint(1, 7)):
        lines.append(rng.choice(ENTRY_LINES))
    if rng.random() < 0.5:
        lines.insert(rng.randint(1, len(lines)),
                     rng.choice(["", "# comment", "[Desktop Entry]"]))
    return "\n".join(lines) + "\n"


def rand_ids(rng, names):
    out = []
    for _ in range(rng.randint(0, 3)):
        r = rng.random()
        if r < 0.45 and names:
            out.append(rng.choice(names))
        elif r < 0.55:
            out.append("Ghost%d.desktop" % rng.randint(0, 3))
        elif r < 0.65:
            out.append(rng.choice(["/enable_cache", "/disable_cache",
                                   "/execarg_compat", "/execarg_strict"]))
        elif r < 0.75:
            out.append("/execarg_default:%s:%s" % (
                rng.choice(names) if names else "X.desktop",
                rng.choice(["-e", "--x", ""])))
        elif r < 0.85 and names:
            out.append(rng.choice(["+", "-"]) + rng.choice(names))
        elif r < 0.92 and names:
            out.append(rng.choice(names) + ":" + rng.choice(["New", "Other", "a b"]))
        else:
            out.append(rng.choice(["   ", "  #c", ".dot.desktop", "id/path.desktop"]))
    return "\n".join(out) + ("\n" if out else "")


def rand_case(rng, idx):
    files = {}
    execs = []
    names = []
    ndirs = rng.choice([1, 1, 2, 3])
    prefixes = ["usr/share", "usr/local/share", "opt/apps", "srv/data"]
    rng.shuffle(prefixes)
    dirs = prefixes[:ndirs]
    data_home = rng.random() < 0.75
    for i in range(rng.randint(0, 3)):
        nm = rng.choice(["Alacritty.desktop", "Foot.desktop", "Kitty.desktop",
                         "Sub-Term.desktop", "Zed.desktop", "Ghost.desktop"])
        sub = "sub/" if rng.random() < 0.15 else ""
        base_p = ("home/.local/share" if (data_home and rng.random() < 0.5)
                  else rng.choice(dirs))
        rel = "%s/applications/%s%s" % (base_p, sub, nm)
        if rng.random() < 0.12:
            continue
        files[rel] = rand_entry(rng)
        names.append((sub.replace("/", "-") if sub else "") + nm)
    if not execs and rng.random() < 0.9:
        execs = list(EXEC_STUBS)
    # config tree
    cfg_home = "home/.config"
    cfg_dirs = []
    for d in dirs:
        if rng.random() < 0.5:
            cfg_dirs.append("etc/" + d.replace("/", "-"))
    nlists = rng.randint(0, 2)
    for _ in range(nlists):
        which = rng.random()
        if which < 0.6:
            rel = "%s/xdg-terminals.list" % cfg_home
        elif which < 0.8 and cfg_dirs:
            rel = "%s/xdg-terminals.list" % rng.choice(cfg_dirs)
        else:
            rel = "%s/xdg-terminal-exec/xdg-terminals.list" % rng.choice(dirs)
        if rng.random() < 0.3:
            dname = rng.choice(["hyprland", "gnome", "kde", "sway"])
            rel = rel.replace("xdg-terminals.list", "%s-xdg-terminals.list" % dname)
        files[rel] = rand_ids(rng, names)
    env = {}
    if rng.random() < 0.9:
        env["XDG_CONFIG_HOME"] = "$ROOT/" + cfg_home
        env["XDG_CONFIG_DIRS"] = ":".join("$ROOT/" + d for d in cfg_dirs) or "$ROOT/etc/xdg"
        env["XDG_DATA_HOME"] = "$ROOT/home/.local/share"
        env["XDG_DATA_DIRS"] = ":".join("$ROOT/" + d for d in dirs)
    env["XDG_CURRENT_DESKTOP"] = rng.choice(
        ["Hyprland", "hyprland", "HYPRLAND", "Hyprland:GNOME", "GNOME", ""])
    r = rng.random()
    if r < 0.7:
        args = list(SELECT)
    elif r < 0.82:
        args = ["--print-id"]
    elif r < 0.9:
        args = ["--print-path"]
    elif r < 0.95:
        args = ["--print-content"]
    else:
        args = rng.choice([["--print-cmd"], ["--print-id", "--print-cmd"],
                           ["--print-cmd=,"], ["--print-id", "--print-path",
                                               "--print-delimiter=|"]])
    cid = "R%03d" % idx
    c = base(cid, "random/%s" % rng.choice(
        ["tree", "list", "entry", "env", "mixed"]), env=env, files=files,
        execs=sorted(set(execs)) if execs else [], args=args)
    # occasional symlink / mode setup
    s = rng.random()
    if s < 0.06 and files:
        target = rng.choice(list(files))
        c.setdefault("setup", {})["symlinks"] = {
            "home/.local/share/applications/Link.desktop":
                os.path.relpath(target, "home/.local/share/applications")}
    elif s < 0.1 and files:
        c.setdefault("setup", {})["modes"] = {rng.choice(list(files)): 0o000}
    return c


# --------------------------------------------------------------------------- #
# analysis
# --------------------------------------------------------------------------- #
def selection(stdout, rc):
    if rc != 0:
        return ("<rc%d>" % rc,)
    return tuple(stdout.split("\n"))


def run(work, out, seed, nrandom):
    global WORK, TOOLBIN
    WORK = work
    os.makedirs(work, exist_ok=True)
    os.makedirs(out, exist_ok=True)
    TOOLBIN = make_toolbin(work)
    rng = random.Random(seed)

    cases = []
    runs = []
    # families
    flips = []
    fam_report = []
    for fid, cls, mk, variants in families():
        base_case = mk()
        base_case["id"] = fid + "-base"
        bcase, br = finish_case(base_case)
        cases.append(bcase)
        runs.append((bcase["id"], bcase["class"], br))
        bsel = selection(br["stdout"], br["rc"])
        for label, fn in variants:
            v = fn(mk())
            v["id"] = "%s-%s" % (fid, label)
            v["class"] = cls
            vcase, vr = finish_case(v)
            cases.append(vcase)
            runs.append((vcase["id"], vcase["class"], vr))
            vsel = selection(vr["stdout"], vr["rc"])
            fam_report.append((fid, label, bsel, vsel))
            if vsel != bsel:
                flips.append({
                    "family": fid, "delta": label, "class": cls,
                    "base": {"id": bcase["id"], "rc": br["rc"],
                             "sel": list(bsel)},
                    "variant": {"id": vcase["id"], "rc": vr["rc"],
                                "sel": list(vsel)},
                })
    # random
    for i in range(nrandom):
        c = rand_case(rng, i + 1)
        ccase, cr = finish_case(c)
        cases.append(ccase)
        runs.append((ccase["id"], ccase["class"], cr))

    # clustering
    clusters = {}
    for cid, cls, r in runs:
        key = (r["rc"], selection(r["stdout"], r["rc"]))
        clusters.setdefault(key, []).append((cid, cls))
    cluster_rows = sorted(clusters.items(), key=lambda kv: -len(kv[1]))

    with open(os.path.join(out, "cases.jsonl"), "w", encoding="utf-8") as f:
        for c in cases:
            f.write(json.dumps(c, sort_keys=True) + "\n")

    with open(os.path.join(out, "runs.tsv"), "w", encoding="utf-8") as f:
        f.write("id\tclass\trc\tstdout\tstderr\n")
        for cid, cls, r in runs:
            f.write("%s\t%s\t%d\t%s\t%s\n" % (
                cid, cls, r["rc"],
                json.dumps(r["stdout"]), json.dumps(r["stderr"])))

    with open(os.path.join(out, "clusters.tsv"), "w", encoding="utf-8") as f:
        f.write("count\trc\tselection\texamples\n")
        for (rc, sel), ids in cluster_rows:
            f.write("%d\t%d\t%s\t%s\n" % (
                len(ids), rc, json.dumps(list(sel)),
                ",".join(i for i, _ in ids[:6])))

    with open(os.path.join(out, "flips.tsv"), "w", encoding="utf-8") as f:
        f.write("family\tdelta\tclass\tbase_rc\tbase_sel\tvariant_rc\tvariant_sel\n")
        for fl in flips:
            f.write("%s\t%s\t%s\t%d\t%s\t%d\t%s\n" % (
                fl["family"], fl["delta"], fl["class"], fl["base"]["rc"],
                json.dumps(fl["base"]["sel"]), fl["variant"]["rc"],
                json.dumps(fl["variant"]["sel"])))

    with open(os.path.join(out, "families.tsv"), "w", encoding="utf-8") as f:
        f.write("family\tvariant\tbase\tvariant_sel\tsame\n")
        for fid, label, bsel, vsel in fam_report:
            f.write("%s\t%s\t%s\t%s\t%s\n" % (
                fid, label, json.dumps(list(bsel)), json.dumps(list(vsel)),
                "same" if bsel == vsel else "DIFF"))

    stderr_kinds = {}
    for cid, cls, r in runs:
        if r["stderr"]:
            stderr_kinds.setdefault(r["stderr"].strip()[:120], []).append(cid)

    summary = {
        "runs": len(runs),
        "families": len(families()),
        "family_variants": len(fam_report),
        "random": nrandom,
        "distinct_outcomes": len(clusters),
        "flips_in_families": len(flips),
        "rc_counts": {},
        "stderr_kinds": {k: len(v) for k, v in stderr_kinds.items()},
        "seed": seed,
    }
    for _, _, r in runs:
        summary["rc_counts"][str(r["rc"])] = summary["rc_counts"].get(str(r["rc"]), 0) + 1

    with open(os.path.join(out, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("\nflips: %d" % len(flips))
    for fl in flips:
        print("  %-4s %-28s %-40s -> %s" % (
            fl["family"], fl["delta"], json.dumps(fl["base"]["sel"]),
            json.dumps(fl["variant"]["sel"])))
    print("\ntop clusters:")
    for (rc, sel), ids in cluster_rows[:25]:
        print("  n=%-3d rc=%d %s   [%s]" % (len(ids), rc, json.dumps(list(sel)),
                                            ids[0][0]))
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--work", default=None)
    r.add_argument("--out", default=None)
    r.add_argument("--seed", type=int, default=20261026)
    r.add_argument("--random", type=int, default=420)
    c = sub.add_parser("case")
    c.add_argument("file")
    c.add_argument("--work", default=None)
    a = ap.parse_args(argv)

    work = a.work or os.environ.get("TMPDIR") or tempfile.gettempdir()
    if a.cmd == "case":
        global WORK, TOOLBIN
        WORK = tempfile.mkdtemp(prefix="replay-", dir=work)
        TOOLBIN = make_toolbin(WORK)
        with open(a.file, encoding="utf-8") as f:
            case = json.load(f)
        res = run_case(case)
        print("rc=%d" % res["rc"])
        print("stdout=%s" % json.dumps(res["stdout"]))
        print("stderr=%s" % json.dumps(res["stderr"]))
        return 0

    out = a.out or os.path.join(work, "out")
    try:
        return run(tempfile.mkdtemp(prefix="w-", dir=work), out, a.seed,
                   a.random)
    finally:
        for rt in ROOTS:
            shutil.rmtree(rt, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
