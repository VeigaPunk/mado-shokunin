#!/usr/bin/env python3
"""Differential harness: real /usr/bin/xdg-terminal-exec vs mado-terminal.py.

Usage: cmp.py [--cases designed|nonce|wild|all] [--seed N] [--count N]
              [--receipt FILE] [--write-expect FILE] [--show-stderr]

Materialises each case under $CMP_BASE/<id> (default: a scratch dir) and
compares stdout bytes + exit status byte for byte.  Every path below is
overridable from the environment, so the harness can be re-run elsewhere:

  CMP_REAL     the pinned reference script   (default /usr/bin/xdg-terminal-exec)
  CMP_TOOL     the tool under test           (default: the draft next to this file)
  CMP_BASE     scratch root for case trees   (default $TMPDIR/cmp-cases)
  CMP_TOOLBIN  dir holding tr/find/awk/...   (default $CMP_BASE/../toolbin)

Note: a fixture repository is never needed; cases are plain directories.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
REAL = os.environ.get("CMP_REAL", "/usr/bin/xdg-terminal-exec")
TOOL = os.environ.get("CMP_TOOL", os.path.join(_HERE, "..", "mado-terminal.py"))
BASE = os.environ.get("CMP_BASE",
                      os.path.join(os.environ.get("TMPDIR", "/tmp"), "cmp-cases"))
TOOLBIN = os.environ.get("CMP_TOOLBIN",
                         os.path.join(os.path.dirname(BASE), "toolbin"))

TE = """[Desktop Entry]
Type=Application
Name={name}
Exec={exe}
Categories=System;TerminalEmulator;
X-TerminalArgExec=-e
"""


def env(**kw):
    e = {
        "XDG_CURRENT_DESKTOP": "Hyprland",
        "XDG_CONFIG_HOME": "$ROOT/home/.config",
        "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
        "XDG_DATA_HOME": "$ROOT/home/.local/share",
        "XDG_DATA_DIRS": "$ROOT/usr/share",
    }
    e.update(kw)
    return {k: v for k, v in e.items() if v is not None}


def materialise(case, root):
    os.makedirs(os.path.join(root, "bin"), exist_ok=True)
    os.makedirs(os.path.join(root, "home"), exist_ok=True)
    os.makedirs(os.path.join(root, "cache"), exist_ok=True)
    os.makedirs(os.path.join(root, "toolbin"), exist_ok=True)
    for rel, text in case["files"].items():
        p = os.path.join(root, rel)
        d = os.path.dirname(p)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    for rel in case["exec"]:
        p = os.path.join(root, rel)
        d = os.path.dirname(p)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write("#!/bin/sh\nexit 0\n")
        os.chmod(p, 0o755)


def case_env(case, root):
    e = {"HOME": root + "/home", "PATH": root + "/bin:" + TOOLBIN,
         "XDG_CACHE_HOME": root + "/cache"}
    for k, v in case["env"].items():
        e[k] = v.replace("$ROOT", root)
    return e


def run_real(case, root):
    try:
        p = subprocess.run([REAL] + case["args"], env=case_env(case, root),
                           capture_output=True, timeout=6)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", b"", b"harness: real timed out"
    return p.returncode, p.stdout, p.stderr


def run_tool(case, root):
    try:
        p = subprocess.run([sys.executable, TOOL, "print"] + case["args"],
                           env=case_env(case, root), capture_output=True, timeout=6)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", b"", b"harness: tool timed out"
    return p.returncode, p.stdout, p.stderr


# --------------------------------------------------------------------------
def designed():
    C = []

    def add(cid, files, execs, args, e=None):
        C.append({"id": cid, "env": env(**(e or {})), "files": files,
                  "exec": execs, "args": args})

    P = ["--print-id", "--print-path", "--print-cmd"]
    A = "home/.local/share/applications/"
    S = "usr/share/applications/"
    CFG = "home/.config/"

    # 1 host-shaped: user list names Alacritty.desktop, host-like entry
    add("01-host-shaped",
        {CFG + "xdg-terminals.list": "Alacritty.desktop\n",
         A + "Alacritty.desktop": (
             "[Desktop Entry]\nType=Application\nTryExec=alacritty\nExec=alacritty\n"
             "Icon=Alacritty\nTerminal=false\nCategories=System;TerminalEmulator;\n"
             "Name=Alacritty\nActions=New;\nX-TerminalArgExec=-e\n"
             "X-TerminalArgAppId=--class=\nX-TerminalArgTitle=--title=\n"
             "X-TerminalArgDir=--working-directory=\n\n"
             "[Desktop Action New]\nName=New Terminal\nExec=alacritty\n")},
        ["bin/alacritty"], P)
    # 2 no list at all -> fallback
    add("02-fallback", {A + "zzz.desktop": TE.format(name="Z", exe="sh")},
        ["bin/sh"], P)
    # 3 prefixed list beats plain list in same dir
    add("03-prefixed-beats-plain",
        {CFG + "hyprland-xdg-terminals.list": "bbb.desktop\n",
         CFG + "xdg-terminals.list": "aaa.desktop\n",
         A + "aaa.desktop": TE.format(name="A", exe="sh"),
         A + "bbb.desktop": TE.format(name="B", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    # 4 config home beats config dirs
    add("04-confighome-beats-dirs",
        {CFG + "xdg-terminals.list": "aaa.desktop\n",
         "etc/xdg/xdg-terminals.list": "bbb.desktop\n",
         A + "aaa.desktop": TE.format(name="A", exe="sh"),
         A + "bbb.desktop": TE.format(name="B", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    # 5 data-dir level list
    add("05-datadir-list",
        {"usr/share/xdg-terminal-exec/xdg-terminals.list": "bbb.desktop\n",
         A + "aaa.desktop": TE.format(name="A", exe="sh"),
         A + "bbb.desktop": TE.format(name="B", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    # 6 duplicate ID: user dir wins over system dir
    add("06-duplicate-user-wins",
        {A + "dup.desktop": TE.format(name="U", exe="alacritty"),
         S + "dup.desktop": TE.format(name="S", exe="sh")},
        ["bin/sh", "bin/alacritty"], P)
    # 7 Hidden=true
    add("07-hidden-true",
        {A + "hid.desktop": TE.format(name="H", exe="sh").replace(
            "Categories=", "Hidden=true\nCategories="),
         A + "ok.desktop": TE.format(name="O", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    # 8 Hidden=True is not "true"
    add("08-hidden-capital",
        {A + "hid.desktop": TE.format(name="H", exe="sh").replace(
            "Categories=", "Hidden=True\nCategories=")},
        ["bin/sh"], P)
    # 9 no Categories
    add("09-no-categories",
        {A + "nocat.desktop": "[Desktop Entry]\nType=Application\nExec=sh\n",
         A + "ok.desktop": TE.format(name="O", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    # 10 Categories without TerminalEmulator
    add("10-wrong-category",
        {A + "nocat.desktop": TE.format(name="N", exe="sh").replace(
            "Categories=System;TerminalEmulator;", "Categories=System;Utility;"),
         A + "ok.desktop": TE.format(name="O", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    # 11 TryExec missing
    add("11-tryexec-missing",
        {A + "te.desktop": TE.format(name="T", exe="alacritty").replace(
            "Categories=", "TryExec=nothere\nCategories=")},
        ["bin/alacritty"], P)
    # 12 Exec[0] not on PATH
    add("12-exec-not-on-path",
        {A + "x.desktop": TE.format(name="X", exe="ghost")},
        ["bin/alacritty"], P)
    # 13 Exec quoting and field codes
    add("13-exec-fields",
        {A + "f.desktop": (
            "[Desktop Entry]\nType=Application\n"
            "Exec=\"sh\" -c \"echo hi\" %i %c %%f\n"
            "Categories=TerminalEmulator;\n")},
        ["bin/sh"], P)
    # 14 two %f fields -> discard, next candidate
    add("14-two-file-fields",
        {A + "a.desktop": "[Desktop Entry]\nExec=sh %f %u\nCategories=TerminalEmulator;\n",
         A + "b.desktop": TE.format(name="B", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    # 15 unknown % field
    add("15-unknown-field",
        {A + "a.desktop": "[Desktop Entry]\nExec=sh %z\nCategories=TerminalEmulator;\n"},
        ["bin/sh"], P)
    # 16 action selection
    add("16-action",
        {CFG + "xdg-terminals.list": "aaa.desktop:New\n",
         A + "aaa.desktop": (
             "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\nActions=New;\n\n"
             "[Desktop Action New]\nExec=sh\n-c\necho hi\n")},
        ["bin/sh"], P)
    # 17 action not listed in Actions
    add("17-action-unlisted",
        {CFG + "xdg-terminals.list": "aaa.desktop:Ghost\n",
         A + "aaa.desktop": (
             "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\nActions=New;\n\n"
             "[Desktop Action Ghost]\nExec=sh\n"),
         A + "zzz.desktop": TE.format(name="Z", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    # 18 exclusion markers: system entry excluded, user listed
    add("18-exclusion",
        {CFG + "xdg-terminals.list": "-excluded.desktop\nAlacritty.desktop\n",
         A + "Alacritty.desktop": TE.format(name="A", exe="sh"),
         S + "excluded.desktop": TE.format(name="E", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    # 19 exclusion only -> fallback skips it
    add("19-exclusion-only",
        {CFG + "xdg-terminals.list": "-aaa.desktop\n",
         A + "aaa.desktop": TE.format(name="A", exe="sh"),
         A + "bbb.desktop": TE.format(name="B", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    # 20 NoDisplay and Type=Link are not consulted
    add("20-nodisplay-type",
        {A + "a.desktop": TE.format(name="A", exe="sh").replace(
            "Type=Application", "Type=Link\nNoDisplay=true")},
        ["bin/sh"], P)
    # 21 OnlyShowIn skipped for explicit list, enforced for fallback
    add("21-onlyshowin",
        {CFG + "xdg-terminals.list": "listed.desktop\n",
         A + "listed.desktop": TE.format(name="L", exe="sh").replace(
             "Categories=", "OnlyShowIn=GNOME;\nCategories="),
         S + "gnome.desktop": TE.format(name="G", exe="alacritty").replace(
             "Categories=", "OnlyShowIn=GNOME;\nCategories=")},
        ["bin/sh", "bin/alacritty"], P)
    # 22 NotShowIn excludes on fallback only
    add("22-notshowin",
        {A + "a.desktop": TE.format(name="A", exe="sh").replace(
            "Categories=", "NotShowIn=Hyprland;\nCategories="),
         A + "b.desktop": TE.format(name="B", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    # 23 XDG_CURRENT_DESKTOP empty
    add("23-no-desktop",
        {CFG + "hyprland-xdg-terminals.list": "aaa.desktop\n",
         A + "aaa.desktop": TE.format(name="A", exe="sh"),
         A + "bbb.desktop": TE.format(name="B", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P, {"XDG_CURRENT_DESKTOP": ""})
    # 24 multi desktop
    add("24-multi-desktop",
        {CFG + "gnome-xdg-terminals.list": "bbb.desktop\n",
         CFG + "hyprland-xdg-terminals.list": "aaa.desktop\n",
         A + "aaa.desktop": TE.format(name="A", exe="sh"),
         A + "bbb.desktop": TE.format(name="B", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P,
        {"XDG_CURRENT_DESKTOP": "Hyprland:GNOME"})
    # 25 XDG_CONFIG_HOME unset
    add("25-no-confighome",
        {"home/.config/xdg-terminals.list": "aaa.desktop\n",
         A + "aaa.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], P, {"XDG_CONFIG_HOME": None})
    # 26 trailing slash in XDG_DATA_DIRS
    add("26-trailing-slash",
        {S + "aaa.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], P, {"XDG_DATA_DIRS": "$ROOT/usr/share/"})
    # 27 empty list file
    add("27-empty-list", {CFG + "xdg-terminals.list": ""},
        [], P)
    # 28 comments, blanks, garbage in list
    add("28-list-noise",
        {CFG + "xdg-terminals.list": (
            "# comment\n\n   \nnot an id.x\nfoo\n/unknown/directive\n"
            "aaa.desktop\n:bad\n"),
         A + "aaa.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], P)
    # 29 misspelled list line
    add("29-misspelled",
        {CFG + "xdg-terminals.list": "bad name.desktop\n",
         A + "aaa.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], P)
    # 30 subdirectory -> dash-joined ID
    add("30-subdir-id",
        {CFG + "xdg-terminals.list": "sub-aaa.desktop\n",
         A + "sub/aaa.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], P)
    # 31 invalid chars in a filename are not registered
    add("31-invalid-chars",
        {A + "bad name.desktop": TE.format(name="B", exe="sh"),
         A + "good.desktop": TE.format(name="G", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    # 32 print modes
    add("32-print-id-only", {A + "a.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], ["--print-id"])
    add("33-print-path-only", {A + "a.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], ["--print-path"])
    add("34-print-both", {A + "a.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], ["--print-path", "--print-id"])
    add("35-print-delim", {A + "a.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], ["--print-id", "--print-path", "--print-delimiter=|"])
    add("36-print-cmd-empty-delim",
        {A + "a.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], ["--print-cmd=", "--print-delimiter=|", "--print-id"])
    add("37-print-cmd-seq",
        {A + "a.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], ["--print-cmd=\\t", "--print-id"])
    # 38 option prepends
    add("38-prepend-all",
        {A + "a.desktop": (
            "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n"
            "X-TerminalArgExec=-e\nX-TerminalArgAppId=--class=\n"
            "X-TerminalArgTitle=--title=\nX-TerminalArgDir=--cd=\n"
            "X-TerminalArgHold=--hold\n")},
        ["bin/sh"], ["--print-cmd", "--app-id=com.x", "--title=T y",
                     "--dir=/tmp", "--hold"])
    # 39 prepend with separate-arg args
    add("39-prepend-space",
        {A + "a.desktop": (
            "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n"
            "X-TerminalArgAppId=--class\nX-TerminalArgTitle=--title\n"
            "X-TerminalArgDir=--cd\nX-TerminalArgHold=--hold\n")},
        ["bin/sh"], ["--print-cmd", "--app-id=x", "--title=t", "--dir=/d", "--hold"])
    # 40 TerminalArgExec escapes
    add("40-execarg-escape",
        {A + "a.desktop": (
            "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n"
            "X-TerminalArgExec=--opt=\\s\\t\n")},
        ["bin/sh"], ["--print-cmd", "echo", "hi"])
    # 41 --print-content
    add("41-print-content",
        {A + "a.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], ["--print-id", "--print-content"])
    # 42 --test
    add("42-test-mode", {A + "a.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], ["--test"])
    # 43 --help
    add("43-help", {}, [], ["--help"])
    # 44 no valid entry
    add("44-none", {A + "a.desktop": "[Desktop Entry]\nExec=sh\n"}, ["bin/sh"], P)
    # 45 strict mode: no TerminalArgExec and XTE_EXECARG_COMPAT=false
    add("45-strict",
        {A + "a.desktop": "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n"},
        ["bin/sh"], P, {})
    # 46 execarg_default directive
    add("46-execarg-default",
        {CFG + "xdg-terminals.list": (
            "/execarg_default:aaa.desktop:--\naaa.desktop\n"),
         A + "aaa.desktop": "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n"},
        ["bin/sh"], ["--print-cmd", "echo", "hi"])
    # 47 directives: strict + disable_cache
    add("47-directives",
        {CFG + "xdg-terminals.list": "/execarg_strict\n/disable_cache\n/execarg_compat\naaa.desktop\n",
         A + "aaa.desktop": "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n"},
        ["bin/sh"], ["--print-cmd", "echo"])
    # 48 residue: A has category but no Exec, B has Exec but no category
    add("48-residue",
        {A + "aaa.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\n",
         A + "bbb.desktop": "[Desktop Entry]\nExec=alacritty\n"},
        ["bin/alacritty"], P)
    # 49 a directory named *.desktop in the second applications dir
    add("49-dir-entry",
        {S + "dir.desktop/keep": "", A + "ok.desktop": TE.format(name="O", exe="sh")},
        ["bin/sh"], P)
    # 50 empty Exec
    add("50-empty-exec", {A + "a.desktop": "[Desktop Entry]\nExec=\nCategories=TerminalEmulator;\n"},
        ["bin/sh"], P)
    # 51 CRLF categories
    add("51-crlf",
        {A + "a.desktop": "[Desktop Entry]\r\nExec=sh\r\nCategories=TerminalEmulator;\r\n"},
        ["bin/sh"], P)
    # 52 unquoted special char in Exec
    add("52-exec-bad-quote",
        {A + "a.desktop": "[Desktop Entry]\nExec=sh | cat\nCategories=TerminalEmulator;\n"},
        ["bin/sh"], P)
    # 53 escaped space in Exec
    add("53-exec-escaped-space",
        {A + "a.desktop": "[Desktop Entry]\nExec=sh\\ -c \"echo a b\"\nCategories=TerminalEmulator;\n"},
        ["bin/sh"], P)
    # 54 list line with action and trailing colon
    add("54-action-trailing-colon",
        {CFG + "xdg-terminals.list": "aaa.desktop:New:\n",
         A + "aaa.desktop": ("[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n"
                             "Actions=New;\n\n[Desktop Action New]\nExec=sh\n")},
        ["bin/sh"], P)
    # 55 '+' marker
    add("55-plus-marker",
        {CFG + "xdg-terminals.list": "-zzz.desktop\n+zzz.desktop\nzzz.desktop\n",
         A + "zzz.desktop": TE.format(name="Z", exe="sh")},
        ["bin/sh"], P)
    # 56 XDG_DATA_HOME unset
    add("56-no-datahome",
        {S + "aaa.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], P, {"XDG_DATA_HOME": None})
    # 57 dir= only, no TerminalArgDir
    add("57-dir-no-arg", {A + "a.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], ["--print-cmd", "--dir=/x", "echo"])
    # 58 hold without TerminalArgHold
    add("58-hold-no-arg", {A + "a.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], ["--print-cmd", "--hold", "echo"])
    # 59 unknown options ignored
    add("59-unknown-opt", {A + "a.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], ["--nonsense", "--print-id", "--print-cmd", "echo"])
    # 60 explicit end of options
    add("60-dashdash", {A + "a.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], ["--print-cmd", "--", "--print-id"])
    return C


def designed2():
    """Second designed batch: hierarchy, ID collisions, delimiters, quirks."""
    C = []

    def add(cid, files, execs, args, e=None):
        C.append({"id": cid, "env": env(**(e or {})), "files": files,
                  "exec": execs, "args": args})

    P = ["--print-id", "--print-path", "--print-cmd"]
    A = "home/.local/share/applications/"
    S = "usr/share/applications/"
    L = "usr/local/share/applications/"
    CFG = "home/.config/"

    add("d01-three-datadirs",
        {CFG + "xdg-terminals.list": "ss.desktop\n",
         A + "hh.desktop": TE.format(name="H", exe="sh"),
         S + "ss.desktop": TE.format(name="S", exe="alacritty"),
         L + "ll.desktop": TE.format(name="L", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P,
        {"XDG_DATA_DIRS": "$ROOT/usr/share:$ROOT/usr/local/share"})
    add("d02-nested-collision",
        {A + "sub-x.desktop": TE.format(name="Flat", exe="sh"),
         A + "sub/x.desktop": TE.format(name="Nested", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    add("d03-prefix-shadow",
        {CFG + "xdg-terminals.list": "a.desktop\n",
         A + "a.desktop": TE.format(name="A", exe="sh"),
         A + "aa.desktop": TE.format(name="AA", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    add("d04-uppercase-listfile",
        {CFG + "Hyprland-xdg-terminals.list": "aaa.desktop\n",
         A + "aaa.desktop": TE.format(name="A", exe="sh"),
         A + "bbb.desktop": TE.format(name="B", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    add("d05-desktop-trailing-colon",
        {CFG + "hyprland-xdg-terminals.list": "bbb.desktop\n",
         A + "aaa.desktop": TE.format(name="A", exe="sh"),
         A + "bbb.desktop": TE.format(name="B", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P,
        {"XDG_CURRENT_DESKTOP": "Hyprland:"})
    add("d06-delims",
        {A + "a.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], ["--print-id", "--print-path", "--print-cmd=\\t",
                     "--print-delimiter=\\\\"])
    add("d07-two-exec-lines",
        {A + "a.desktop": "[Desktop Entry]\nExec=ghost\nCategories=TerminalEmulator;\n"
                          "Exec=sh\n"},
        ["bin/sh"], P)
    add("d08-exec-later-group",
        {A + "a.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\n\n"
                          "[Other]\nExec=sh\n"},
        ["bin/sh"], P)
    add("d09-two-main-groups",
        {A + "a.desktop": "[Desktop Entry]\nExec=ghost\nCategories=TerminalEmulator;\n\n"
                          "[Desktop Entry]\nExec=sh\n"},
        ["bin/sh"], P)
    add("d10-digit-key",
        {A + "a.desktop": "[Desktop Entry]\nExec=sh\n1Key=value\n"
                          "Categories=TerminalEmulator;\n"},
        ["bin/sh"], P)
    add("d11-no-trailing-newline",
        {A + "a.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=sh"},
        ["bin/sh"], P)
    add("d12-list-no-newline", {CFG + "xdg-terminals.list": "aaa.desktop",
                                A + "aaa.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], P)
    add("d13-dot-desktop-name",
        {A + ".desktop": TE.format(name="D", exe="sh"),
         A + "ok.desktop": TE.format(name="O", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    add("d14-double-desktop", {A + "a.desktop.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], P)
    add("d15-tryexec-escaped",
        {A + "a.desktop": TE.format(name="A", exe="sh").replace(
            "Categories=", "TryExec=not\\shere\nCategories=")},
        ["bin/sh"], P)
    add("d16-literal-percent-file",
        {A + "a.desktop": "[Desktop Entry]\nExec=sh %%f\nCategories=TerminalEmulator;\n"},
        ["bin/sh"], P)
    add("d17-cmd-delim-cut",
        {A + "a.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], ["--print-cmd=x\\cy", "--print-id"])
    add("d18-content-and-id",
        {A + "a.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], ["--print-id", "--print-content"])
    add("d19-content-dir",
        {S + "dir.desktop/keep": "", A + "ok.desktop": TE.format(name="O", exe="sh")},
        ["bin/sh"], ["--print-content"])
    add("d20-plus-only",
        {CFG + "xdg-terminals.list": "+\n",
         A + "ok.desktop": TE.format(name="O", exe="sh")},
        ["bin/sh"], P)
    add("d21-system-exclusion-host-shape",
        {"usr/share/xdg-terminal-exec/xdg-terminals.list":
            "-foot.desktop\n-footclient.desktop\n/execarg_default:aaa.desktop:--\n",
         CFG + "xdg-terminals.list": "aaa.desktop\n",
         A + "aaa.desktop": "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n",
         S + "foot.desktop": TE.format(name="F", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], ["--print-id", "--print-cmd", "echo", "x"])
    add("d22-action-missing-group",
        {CFG + "xdg-terminals.list": "aaa.desktop:New\n",
         A + "aaa.desktop": "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n"
                           "Actions=New;\n",
         A + "zzz.desktop": TE.format(name="Z", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    add("d23-onlyshowin-multi",
        {A + "a.desktop": TE.format(name="A", exe="sh").replace(
            "Categories=", "OnlyShowIn=KDE;GNOME;\nCategories=")},
        ["bin/sh"], P, {"XDG_CURRENT_DESKTOP": "GNOME:Hyprland"})
    add("d24-notshowin-empty",
        {A + "a.desktop": TE.format(name="A", exe="sh").replace(
            "Categories=", "NotShowIn=\nCategories=")},
        ["bin/sh"], P)
    add("d25-onlyshowin-empty",
        {A + "a.desktop": TE.format(name="A", exe="sh").replace(
            "Categories=", "OnlyShowIn=\nCategories=")},
        ["bin/sh"], P)
    add("d26-hidden-false",
        {A + "a.desktop": TE.format(name="A", exe="sh").replace(
            "Categories=", "Hidden=false\nCategories=")},
        ["bin/sh"], P)
    add("d27-dir-spaces",
        {A + "a.desktop": TE.format(name="A", exe="sh").replace(
            "Categories=", "X-TerminalArgDir=--cd=\nCategories=")},
        ["bin/sh"], ["--print-cmd", "--dir=/a b", "echo"])
    add("d28-dirarg-split",
        {A + "a.desktop": TE.format(name="A", exe="sh").replace(
            "Categories=", "X-TerminalArgDir=--cd\nCategories=")},
        ["bin/sh"], ["--print-cmd", "--dir=/x", "echo"])
    add("d29-empty-execarg",
        {A + "a.desktop": "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n"
                          "X-TerminalArgExec=\n"},
        ["bin/sh"], ["--print-cmd", "echo", "hi"])
    add("d30-dashdash-args",
        {A + "a.desktop": TE.format(name="A", exe="sh")},
        ["bin/sh"], ["--print-cmd", "--", "-x", "--print-id"])
    add("d31-exec-tab",
        {A + "a.desktop": "[Desktop Entry]\nExec=sh\t-c\t\"echo\thi\"\n"
                          "Categories=TerminalEmulator;\n"},
        ["bin/sh"], P)
    add("d32-crlf-trailing-space",
        {A + "a.desktop": "[Desktop Entry]  \r\nExec=sh   \r\n"
                          "Categories=TerminalEmulator;\r\n"},
        ["bin/sh"], P)
    add("d33-datadir-prefixed-list",
        {"usr/local/share/xdg-terminal-exec/hyprland-xdg-terminals.list":
            "bbb.desktop\n",
         A + "aaa.desktop": TE.format(name="A", exe="sh"),
         A + "bbb.desktop": TE.format(name="B", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P,
        {"XDG_DATA_DIRS": "$ROOT/usr/share:$ROOT/usr/local/share"})
    add("d34-two-config-dirs",
        {CFG + "xdg-terminals.list": "aaa.desktop\n",
         "etc/xdg/xdg-terminals.list": "aaa.desktop\nbbb.desktop\n",
         A + "aaa.desktop": TE.format(name="A", exe="sh"),
         A + "bbb.desktop": TE.format(name="B", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    add("d35-no-dot-name",
        {A + "termdesktop": TE.format(name="T", exe="sh"),
         A + "ok.desktop": TE.format(name="O", exe="alacritty")},
        ["bin/sh", "bin/alacritty"], P)
    return C


def wild(n=200, seed=4711):
    """Wide generator: exotic names, keys, quoting and delimiters."""
    import random
    rnd = random.Random(seed)
    C = []
    desktops = ["Hyprland", "gnome", "", "Hyprland:GNOME:KDE", "Weird DE",
                "hyprland", "Hyprland:", ":Hyprland"]
    ids = ["aaa.desktop", "BBB.desktop", "a_b.desktop", "a-b.desktop",
           "sub/nested.desktop", "sub/deep/x.desktop", "9lives.desktop",
           "_under.desktop", "A.b.c.desktop"]
    badnames = ["bad name.desktop", "x%.desktop", "x+y.desktop", "x@y.desktop",
                ".desktop", "nope", "dir.desktop"]
    dirs = ["home/.local/share/applications/", "usr/share/applications/",
            "usr/local/share/applications/"]
    for i in range(n):
        files = {}
        execs = ["bin/sh"]
        # applications entries
        for eid in rnd.sample(ids, k=rnd.randint(1, 3)):
            lines = []
            if rnd.random() < 0.85:
                lines.append("[Desktop Entry]")
            keys = []
            if rnd.random() < 0.85:
                keys.append("Exec=" + rnd.choice(
                    ["sh", "sh -c \"echo a b\"", "sh\\ -c", "ghost", "\"sh\"",
                     "sh %f", "sh %f %u", "sh %i %c", "sh %%", "sh %%f", "sh %z",
                     "sh | cat", "sh 'x'", "sh \"unterminated", "", "sh \"a\\\"b\"",
                     "sh %d %n", "sh %m"]))
            if rnd.random() < 0.85:
                keys.append("Categories=" + rnd.choice(
                    ["TerminalEmulator;", "System;TerminalEmulator;", "System;",
                     "", "TerminalEmulator", "System;TerminalEmulator", "Other;TE;"]))
            if rnd.random() < 0.3:
                keys.append("Actions=" + rnd.choice(["New;", "", "New;Other;"]))
            if rnd.random() < 0.25:
                keys.append("Hidden=" + rnd.choice(["true", "True", "false", "1"]))
            if rnd.random() < 0.25:
                keys.append("TryExec=" + rnd.choice(["sh", "ghost", "", "sh\\s"]))
            if rnd.random() < 0.3:
                keys.append("TerminalArgExec=" + rnd.choice(
                    ["-e", "--", "", "-e\\s-f", "exec"]))
            if rnd.random() < 0.2:
                keys.append("ExecArg=-x")
            if rnd.random() < 0.3:
                keys.append("X-TerminalArgTitle=" + rnd.choice(
                    ["--title=", "--title", "", "--t\\t"]))
            if rnd.random() < 0.3:
                keys.append("X-TerminalArgDir=" + rnd.choice(
                    ["--cd=", "--cd", ""]))
            if rnd.random() < 0.25:
                keys.append("X-TerminalArgAppId=" + rnd.choice(
                    ["--class=", "--class", ""]))
            if rnd.random() < 0.25:
                keys.append("X-TerminalArgHold=" + rnd.choice(["--hold", ""]))
            if rnd.random() < 0.2:
                keys.append("OnlyShowIn=" + rnd.choice(
                    ["GNOME;", "Hyprland;", "", "KDE;GNOME;", "Weird DE;"]))
            if rnd.random() < 0.2:
                keys.append("NotShowIn=" + rnd.choice(
                    ["GNOME;", "Hyprland;", "", "KDE;"]))
            if rnd.random() < 0.15:
                keys.append("Type=" + rnd.choice(["Application", "Link"]))
            if rnd.random() < 0.15:
                keys.append("NoDisplay=true")
            if rnd.random() < 0.1:
                keys.append("X-Foo=bar")
            if rnd.random() < 0.1:
                keys.append("1Numeric=value")
            rnd.shuffle(keys)
            lines.extend(keys)
            if rnd.random() < 0.5:
                lines.append("")
                lines.append("[Desktop Action " + rnd.choice(["New", "Other"]) + "]")
                lines.append("Exec=" + rnd.choice(["sh", "ghost", "sh %f"]))
            body = "\n".join(lines)
            body += "\n" if rnd.random() < 0.9 else ""
            files[rnd.choice(dirs) + eid] = body
        # junk entries
        if rnd.random() < 0.3:
            files[rnd.choice(dirs) + rnd.choice(badnames)] = TE.format(
                name="J", exe="sh")
        # list files
        cfgdirs = ["home/.config/", "etc/xdg/", "usr/share/xdg-terminal-exec/",
                   "home/.config/subconf/"]
        names = ["xdg-terminals.list", "hyprland-xdg-terminals.list",
                 "gnome-xdg-terminals.list", "Hyprland-xdg-terminals.list",
                 "xdg-terminals", "other.list"]
        pool = (ids + badnames[:3] +
                ["aaa.desktop:New", "aaa.desktop:Other", "aaa.desktop:",
                 "BBB.desktop:New", "+aaa.desktop", "-aaa.desktop",
                 "+a_b.desktop", "-a-b.desktop", "ghost.desktop"])
        for _ in range(rnd.randint(0, 3)):
            p = rnd.choice(cfgdirs) + rnd.choice(names)
            lines = []
            for _ in range(rnd.randint(0, 5)):
                r = rnd.random()
                if r < 0.65:
                    lines.append(rnd.choice(pool))
                elif r < 0.75:
                    lines.append(rnd.choice(["/execarg_compat", "/execarg_strict",
                                             "/enable_cache", "/disable_cache"]))
                elif r < 0.85:
                    lines.append(rnd.choice([
                        "/execarg_default:aaa.desktop:--",
                        "/execarg_default:BBB.desktop:-x",
                        "/execarg_default:.desktop:q",
                        "/execarg_default:aaa.desktop:"]))
                else:
                    lines.append(rnd.choice(["", "  ", "# comment", "  aaa.desktop  ",
                                             "aaa.desktop ", "\taaa.desktop"]))
            files[p] = "\n".join(lines) + ("\n" if rnd.random() < 0.85 else "")
        # args
        args = []
        for _ in range(rnd.randint(1, 2)):
            args.append(rnd.choice([
                "--print-id", "--print-path", "--print-cmd",
                "--print-cmd=" + rnd.choice(["|", "\\t", "\\\\", "\\0", "x",
                                             "", "\\c", "%s", "a b"]),
                "--print-delimiter=" + rnd.choice(["|", "\\t", "\\\\", "\\0",
                                                   "", "\\c", "<>"]),
                "--print-content"]))
        if "--print-content" in args and any(a.startswith("--print-cmd") for a in args):
            args.remove("--print-content")
        if not any(a in ("--print-id", "--print-path") or a.startswith("--print-cmd")
                   for a in args):
            args.append("--print-id")
        if rnd.random() < 0.3:
            args += ["--dir=" + rnd.choice(["/w", "/a b", "-x", ""])]
        if rnd.random() < 0.25:
            args += ["--title=" + rnd.choice(["t", "a b", ""])]
        if rnd.random() < 0.25:
            args += ["--app-id=" + rnd.choice(["x", "", "a=b"])]
        if rnd.random() < 0.25:
            args += ["--hold"]
        if rnd.random() < 0.15:
            args += ["-e"]
        if rnd.random() < 0.35:
            args += rnd.choice([["echo", "hi"], ["--", "-x"], ["a b", "c"],
                                ["-notanopt"], [""]])
        e = env(XDG_CURRENT_DESKTOP=rnd.choice(desktops))
        if rnd.random() < 0.1:
            e.pop("XDG_CURRENT_DESKTOP", None)
        if rnd.random() < 0.15:
            e["XTE_EXECARG_COMPAT"] = rnd.choice(["false", "true", "no", "1"])
        if rnd.random() < 0.1:
            e["XDG_CONFIG_DIRS"] = "$ROOT/etc/xdg:$ROOT/etc/xdg2"
        C.append({"id": "w%03d" % i, "env": e, "files": files, "exec": execs,
                  "args": args})
    return C


def nonce(n=150, seed=47):
    import random
    rnd = random.Random(seed)
    C = []
    desktops = ["Hyprland", "GNOME", "", "Hyprland:GNOME", "gnome", None]
    exes = ["sh", "alacritty", "ghost", "sh -c", "/bin/true"]
    for i in range(n):
        files = {}
        execs = []
        # random entries
        n_entries = rnd.randint(1, 4)
        dirs = ["home/.local/share/applications/", "usr/share/applications/"]
        ids = ["aaa.desktop", "bbb.desktop", "Alacritty.desktop", "sub/ccc.desktop",
               "zzz.desktop"]
        chosen = rnd.sample(ids, k=min(n_entries, len(ids)))
        for j, eid in enumerate(chosen):
            d = rnd.choice(dirs)
            exe = rnd.choice(exes)
            body = "[Desktop Entry]\n"
            if rnd.random() < 0.9:
                body += "Type=Application\n"
            if rnd.random() < 0.5:
                body += "Categories=%s\n" % rnd.choice(
                    ["TerminalEmulator;", "System;TerminalEmulator;",
                     "System;Utility;", "TerminalEmulator", ""])
            else:
                body += "Categories=System;TerminalEmulator;\n"
            if rnd.random() < 0.2:
                body += "Hidden=%s\n" % rnd.choice(["true", "True", "false", "1"])
            if rnd.random() < 0.2:
                body += "TryExec=%s\n" % rnd.choice(["sh", "ghost", ""])
            if rnd.random() < 0.2:
                body += "NoDisplay=true\n"
            if rnd.random() < 0.4:
                body += "TerminalArgExec=%s\n" % rnd.choice(["-e", "--", "", "-x\\t"])
            if rnd.random() < 0.25:
                body += "X-TerminalArgTitle=--title=\n"
            if rnd.random() < 0.2:
                body += "X-TerminalArgDir=--working-directory=\n"
            if rnd.random() < 0.15:
                body += "OnlyShowIn=%s\n" % rnd.choice(["GNOME;", "Hyprland;", "KDE;"])
            if rnd.random() < 0.15:
                body += "NotShowIn=%s\n" % rnd.choice(["GNOME;", "Hyprland;"])
            if rnd.random() < 0.25:
                body += "Actions=New;\n"
            body += "Exec=%s\n" % exe.replace("%", "%%") if False else "Exec=%s\n" % exe
            if rnd.random() < 0.2:
                body += "\n[Desktop Action New]\nExec=sh\n"
            files[d + eid] = body
            for token in exe.split():
                if token in ("sh", "alacritty"):
                    execs.append("bin/" + token)
        execs = sorted(set(execs))
        # random list files
        cfgdirs = ["home/.config/", "etc/xdg/", "usr/share/xdg-terminal-exec/"]
        names = ["xdg-terminals.list", "hyprland-xdg-terminals.list",
                 "gnome-xdg-terminals.list"]
        for _ in range(rnd.randint(0, 2)):
            p = rnd.choice(cfgdirs) + rnd.choice(names)
            lines = []
            for _ in range(rnd.randint(0, 4)):
                kind = rnd.random()
                if kind < 0.6:
                    lines.append(rnd.choice(ids + ["aaa.desktop:New", "ghost.desktop",
                                                   "bad name.desktop", "# c", "",
                                                   "+aaa.desktop", "-bbb.desktop",
                                                   "/execarg_default:aaa.desktop:--",
                                                   "/execarg_compat", "/execarg_strict"]))
                else:
                    lines.append(rnd.choice(["/execarg_compat", "/execarg_strict",
                                             "/enable_cache", "/disable_cache"]))
            files[p] = "\n".join(lines) + ("\n" if lines else "")
        # random args
        modes = rnd.sample(["--print-id", "--print-path", "--print-cmd",
                            "--print-content", "--print-cmd=\\t",
                            "--print-delimiter=|", "--test"],
                           k=rnd.randint(1, 3))
        if "--print-content" in modes and "--print-cmd" in modes:
            modes.remove("--print-content")
        # Never emit a case that reaches `exec "$@"`: that is outside the
        # byte-identical contract (the tool refuses with rc=2) and it would
        # start a process.
        if not any(m in ("--print-id", "--print-path", "--print-cmd",
                         "--print-cmd=\\t", "--test") for m in modes):
            modes.append("--print-id")
        args = list(modes)
        if rnd.random() < 0.3:
            args += ["--dir=/w"]
        if rnd.random() < 0.2:
            args += ["--title=t"]
        if rnd.random() < 0.2:
            args += ["--hold"]
        if rnd.random() < 0.3:
            args += ["echo", "hi"]
        desk = rnd.choice(desktops)
        e = env(**({"XDG_CURRENT_DESKTOP": desk} if desk is not None else
                   {"XDG_CURRENT_DESKTOP": None}))
        if rnd.random() < 0.15:
            e["XTE_EXECARG_COMPAT"] = "false"
        C.append({"id": "n%03d" % i, "env": e, "files": files, "exec": execs,
                  "args": args})
    return C


def main(argv):
    which = "all"
    write_expect = None
    seed = 47
    count = 150
    show_stderr = False
    receipt = None
    i = 0
    while i < len(argv):
        if argv[i] == "--cases":
            which = argv[i + 1]
            i += 2
        elif argv[i] == "--write-expect":
            write_expect = argv[i + 1]
            i += 2
        elif argv[i] == "--receipt":
            receipt = argv[i + 1]
            i += 2
        elif argv[i] == "--seed":
            seed = int(argv[i + 1])
            i += 2
        elif argv[i] == "--count":
            count = int(argv[i + 1])
            i += 2
        elif argv[i] == "--show-stderr":
            show_stderr = True
            i += 1
        else:
            i += 1
    cases = []
    if which in ("designed", "all"):
        cases += designed() + designed2()
    if which in ("nonce", "all"):
        cases += nonce(count, seed)
    if which == "wild":
        cases += wild(count, seed)
    os.makedirs(BASE, exist_ok=True)
    ok = 0
    bad = []
    stderr_diff = 0
    hangs = 0
    expect = []
    receipts = []
    for case in cases:
        root = os.path.join(BASE, case["id"])
        shutil.rmtree(root, ignore_errors=True)
        materialise(case, root)
        rrc, rout, rerr = run_real(case, root)
        # a second, untouched root for the tool (the real run may have written
        # the cache; the contract models a cold cache for each invocation)
        shutil.rmtree(root, ignore_errors=True)
        materialise(case, root)
        trc, tout, terr = run_tool(case, root)
        if (rrc, rout) == (trc, tout):
            ok += 1
        elif rrc == "TIMEOUT" and trc == 4 and tout == b"":
            # the real script spins forever on an empty argument; the tool
            # reports HANG_RC instead.  Documented divergence.
            ok += 1
            hangs += 1
        else:
            bad.append((case, rrc, trc, rout, tout, rerr, terr))
        if rerr != terr:
            stderr_diff += 1
            if show_stderr and stderr_diff <= 12:
                print("STDERR-DIFF %s\n  real: %r\n  tool: %r"
                      % (case["id"], rerr[:300], terr[:300]))
        expect.append({"id": case["id"], "env": case["env"], "files": case["files"],
                       "exec": case["exec"], "args": case["args"],
                       "rc": rrc, "stdout": rout.decode("utf-8", "surrogateescape")
                       .replace(root, "$ROOT")})
        if receipt:
            verdict = ("MATCH" if (rrc, rout) == (trc, tout) else
                       "MATCH-hang-modelled" if (rrc == "TIMEOUT" and trc == 4)
                       else "DIFF")
            receipts.append(
                "%-28s args=%-58r rc theirs=%-4r ours=%-4r sha256=%s %s\n"
                "    theirs=%r\n    ours  =%r"
                % (case["id"], case["args"], rrc, trc,
                   hashlib.sha256(rout).hexdigest()[:16], verdict,
                   rout[:300].replace(root.encode(), b"$ROOT"),
                   tout[:300].replace(root.encode(), b"$ROOT")))
    print("agree %d/%d  (stderr differs in %d, modelled hangs %d)"
          % (ok, len(cases), stderr_diff, hangs))
    for case, rrc, trc, rout, tout, rerr, terr in bad:
        cid = case["id"]
        print("=" * 70)
        print("DISAGREE %s: real rc=%r tool rc=%r" % (cid, rrc, trc))
        print("  args: %r" % (case["args"],))
        print("  env: %r" % (case["env"],))
        print("  files: %r" % (sorted(case["files"]),))
        print("  real stdout: %r" % rout)
        print("  tool stdout: %r" % tout)
        print("  real stderr: %r" % rerr[:400])
        print("  tool stderr: %r" % terr[:400])
    if receipt:
        with open(receipt, "w") as f:
            f.write("\n".join(receipts) + "\n")
            f.write("# summary: agree %d/%d, stderr differs %d, modelled hangs %d\n"
                    % (ok, len(cases), stderr_diff, hangs))
        print("wrote %s" % receipt)
    if write_expect:
        with open(write_expect, "w") as f:
            json.dump(expect, f, indent=0)
        print("wrote %s" % write_expect)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
