#!/usr/bin/env python3
"""Warm-cache differential: pin (cold prime, mutate, warm run) vs the draft tool, twin trees.

Case fields: id, cls, files, execs, modes, env, args, prime (default --print-cmd), after{files,exec_add,
exec_remove,env,mtime}, cache (literal text, $ROOT substituted; no priming), nohome (drop HOME).
"""
import json
import os
import shutil
import sys

import harness

BASE = 1600000000
TERM = harness.TERM
USEP = harness.USEP
A_ = "usr/share/applications/"
H_ = "home/.local/share/applications/"
L_ = "home/.config/xdg-terminals.list"


def term(name, extra=""):
    return ("[Desktop Entry]\nType=Application\nName=%s\nExec=%s\n"
            "Categories=System;TerminalEmulator;\n%s" % (name, name, extra))


def cache_text(h, cmd="", path="", eid="", action="", execarg="-e", appid="", title="", dirarg="", hold="",
               exec_words=(), fillers=0, final_newline=True, body_at=None):
    """A cache file: 10 header lines, optional filler lines, then the Exec line and its terminator."""
    head = [h, cmd, path, eid, action, execarg, appid, title, dirarg, hold]
    body = USEP.join(exec_words) + TERM
    lines = head + ["pad%02d" % i for i in range(fillers)]
    if body_at is not None:
        lines = lines[:body_at] + [body] + lines[body_at:]
    else:
        lines = lines + [body]
    return "\n".join(lines) + ("\n" if final_newline else "")


def case(id_, cls, files, execs, args, after=None, env=None, cache=None, modes=(), nohome=False,
         primed=True, before=None, mtime=BASE, prime_env=None):
    return {"id": id_, "cls": cls, "files": files, "execs": execs, "args": args, "after": after or {},
            "env": env or {}, "cache": cache, "modes": modes, "nohome": nohome, "primed": primed,
            "before": before or {}, "mtime": mtime, "prime_env": prime_env or {}}


ARGS_ID = ["--print-id"]
ARGS_ALL = ["--print-id", "--print-path", "--print-cmd"]
ARGS_CMD = ["--print-cmd"]
ARGS_TEST = ["--test"]
ARGS_CONTENT = ["--print-content"]

# every id is 12 characters, so a list swap can keep both the list's size and its mtime minute
BASE_TREE_FILES = {A_ + "foot.desktop": term("foot"), A_ + "kity.desktop": term("kity"),
                   A_ + "alac.desktop": term("alac"), L_: "foot.desktop\n"}
BASE_EXECS = ["bin/foot", "bin/kity", "bin/alac"]


def cases():
    C = []
    # ---- hits: the warm answer differs from the cold one --------------------------------
    C.append(case("W-01-hit-basic", "hit", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL))
    C.append(case("W-02-hit-list-swapped-same-size", "hit-differs", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  after={"files": {L_: "kity.desktop\n"}, "mtime": BASE}))
    C.append(case("W-03-hit-list-swapped-same-size-id", "hit-differs", BASE_TREE_FILES, BASE_EXECS, ARGS_ID,
                  after={"files": {L_: "kity.desktop\n"}, "mtime": BASE}))
    C.append(case("W-04-hit-list-swapped-alac", "hit-differs", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  after={"files": {L_: "alac.desktop\n"}, "mtime": BASE}))
    C.append(case("W-05-hit-two-lines-swapped", "hit-differs",
                  dict(BASE_TREE_FILES, **{L_: "foot.desktop\nkity.desktop\n"}), BASE_EXECS, ARGS_ALL,
                  after={"files": {L_: "kity.desktop\nfoot.desktop\n"}, "mtime": BASE}))
    C.append(case("W-06-hit-list-emptied-same-size", "hit-differs",
                  dict(BASE_TREE_FILES, **{L_: "kity.desktop\n"}), BASE_EXECS, ARGS_ALL,
                  after={"files": {L_: "foot.desktop\n"}, "mtime": BASE}))
    C.append(case("W-07-hit-tryexec-stub-removed", "hit-differs",
                  {A_ + "foot.desktop": term("foot", "TryExec=footstub\n"), A_ + "kitty.desktop": term("kitty"),
                   L_: "foot.desktop\n"}, BASE_EXECS + ["bin/footstub"], ARGS_ALL,
                  after={"exec_remove": ["bin/footstub"], "mtime": BASE}))
    C.append(case("W-08-hit-tryexec-stub-kept", "hit", {A_ + "foot.desktop": term("foot", "TryExec=footstub\n"),
                                                        A_ + "kitty.desktop": term("kitty"), L_: "foot.desktop\n"},
                  BASE_EXECS + ["bin/footstub"], ARGS_ALL))
    C.append(case("W-09-hit-directive-added-after-prime", "hit",
                  dict(BASE_TREE_FILES, **{L_: "foot.desktop\n"}), BASE_EXECS, ARGS_ALL,
                  after={"files": {L_: "foot.desktop\n"}, "env": {}, "mtime": BASE}))
    C.append(case("W-10-hit-exec-changed-same-size", "hit-differs",
                  {A_ + "foot.desktop": term("foot"), A_ + "kity.desktop": term("kity"), L_: "foot.desktop\n"},
                  BASE_EXECS + ["bin/fooo"], ARGS_CMD,
                  after={"files": {A_ + "foot.desktop": term("fooo").replace("Name=fooo", "Name=foot")},
                         "mtime": BASE}))
    C.append(case("W-11-hit-execarg-name-changed", "hit-differs",
                  {A_ + "foot.desktop": term("foot", "TerminalArgTitle=--title\n"), L_: "foot.desktop\n"},
                  BASE_EXECS, ["--print-cmd", "--title=x"],
                  after={"files": {A_ + "foot.desktop": term("foot", "TerminalArgTitle=--titel\n")},
                         "mtime": BASE}))
    C.append(case("W-12-hit-dir-arg-changed-same-size", "hit-differs",
                  {A_ + "foot.desktop": term("foot", "X-TerminalArgDir=--working-directory=\n"),
                   L_: "foot.desktop\n"}, BASE_EXECS, ["--print-cmd", "--dir=/srv"],
                  after={"files": {A_ + "foot.desktop": term("foot", "X-TerminalArgDir=--working-directorx=\n")},
                         "mtime": BASE}))
    C.append(case("W-13-hit-multiline-exec", "hit", {A_ + "foot.desktop": term("foot").replace(
        "Exec=foot", 'Exec=foot "--a\\nb"'), L_: "foot.desktop\n"}, BASE_EXECS, ARGS_TEST))
    C.append(case("W-14-hit-multiline-exec-cmd", "hit", {A_ + "foot.desktop": term("foot").replace(
        "Exec=foot", 'Exec=foot "--a\\nb"'), L_: "foot.desktop\n"}, BASE_EXECS, ARGS_CMD))
    C.append(case("W-15-hit-action", "hit", {A_ + "foot.desktop": term("foot", "Actions=srv;\n"
                  "[Desktop Action srv]\nExec=footclient\n"), L_: "foot.desktop:srv\n"},
                  BASE_EXECS + ["bin/footclient"], ARGS_ALL))
    C.append(case("W-16-hit-action-swapped", "hit-differs",
                  {A_ + "foot.desktop": term("foot", "Actions=srv;\n[Desktop Action srv]\nExec=footclient\n"),
                   A_ + "kity.desktop": term("kity"), L_: "foot.desktop:srv\n"},
                  BASE_EXECS + ["bin/footclient"], ARGS_ALL,
                  after={"files": {L_: "kity.desktop:srv\n"}, "mtime": BASE}))
    C.append(case("W-17-hit-hold-and-appid", "hit",
                  {A_ + "foot.desktop": term("foot", "TerminalArgHold=--hold\nTerminalArgAppId=--app-id=\n"),
                   L_: "foot.desktop\n"}, BASE_EXECS, ["--print-cmd", "--hold", "--app-id=org.x"],
                  after={"mtime": BASE}))
    C.append(case("W-18-hit-command-after-cached-execarg", "hit",
                  {A_ + "foot.desktop": term("foot", "TerminalArgExec=--exec\n"), L_: "foot.desktop\n"},
                  BASE_EXECS, ["--print-cmd", "--", "htop", "-d", "5"], after={"mtime": BASE}))
    C.append(case("W-19-hit-cache-default-enable-directive", "hit",
                  {A_ + "foot.desktop": term("foot"), A_ + "kitty.desktop": term("kitty"),
                   L_: "/disable_cache\nfoot.desktop\n"}, BASE_EXECS, ARGS_ALL,
                  env={"XTE_CACHE_ENABLED": "true"}))
    C.append(case("W-20-hit-xdg-cache-home-unset", "hit", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  env={"XDG_CACHE_HOME": None}))
    C.append(case("W-21-hit-print-delimiter", "hit", BASE_TREE_FILES, BASE_EXECS,
                  ["--print-id", "--print-path", "--print-delimiter=\\t"], after={"mtime": BASE}))
    C.append(case("W-22-hit-print-cmd-delimiter", "hit", BASE_TREE_FILES, BASE_EXECS, ["--print-cmd=\\s", "--", "a"],
                  after={"mtime": BASE}))
    C.append(case("W-23-hit-subdir-id", "hit", {A_ + "vendor/foot.desktop": term("foot"), L_: "vendor-foot.desktop\n"},
                  BASE_EXECS, ARGS_ALL, after={"mtime": BASE}))
    C.append(case("W-24-hit-mtime-same-day", "hit", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  after={"mtime": BASE + 3600}))
    C.append(case("W-25-hit-dangling-link-in-apps", "hit",
                  {A_ + "foot.desktop": term("foot"), A_ + "gap.desktop": "/nope\n", L_: "foot.desktop\n"},
                  BASE_EXECS, ARGS_ALL, after={"mtime": BASE}))
    C.append(case("W-26-absent-cold", "absent", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL, primed=False))
    C.append(case("W-27-hit-desktop-two-app-dirs", "hit",
                  {A_ + "foot.desktop": term("foot"), H_ + "kitty.desktop": term("kitty"), L_: "foot.desktop\n"},
                  BASE_EXECS, ARGS_ALL, after={"mtime": BASE}))

    # ---- stale: the cache is invalidated, the cold answer stands ------------------------
    C.append(case("W-31-stale-list-size", "stale", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  after={"files": {L_: "foot.desktop\nkitty.desktop\n"}, "mtime": BASE}))
    C.append(case("W-32-stale-list-mtime-day", "stale", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  after={"mtime": BASE + 2 * 86400}))
    C.append(case("W-33-stale-desktop-added", "stale", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  after={"files": {A_ + "extra.desktop": term("extra")}, "exec_add": ["bin/extra"],
                         "mtime": BASE}))
    C.append(case("W-34-stale-desktop-removed", "stale", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  after={"files": {A_ + "kity.desktop": None}, "mtime": BASE}))
    C.append(case("W-35-stale-desktop-size", "stale", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  after={"files": {A_ + "foot.desktop": term("foot", "X-Note=1\n")}, "mtime": BASE}))
    C.append(case("W-36-stale-desktop-mtime-day", "stale", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  after={"files": {}, "mtime": BASE + 3 * 86400}))
    C.append(case("W-37-stale-current-desktop", "stale", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  env={"XDG_CURRENT_DESKTOP": "GNOME"},
                  prime_env={"XDG_CURRENT_DESKTOP": "Hyprland"}))
    C.append(case("W-38-stale-current-desktop-unset", "stale", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  env={"XDG_CURRENT_DESKTOP": None},
                  prime_env={"XDG_CURRENT_DESKTOP": "Hyprland"}))
    C.append(case("W-39-stale-current-desktop-empty", "stale", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  env={"XDG_CURRENT_DESKTOP": ""},
                  prime_env={"XDG_CURRENT_DESKTOP": "Hyprland"}))
    C[-1]["cls"] = "stale"
    C.append(case("W-40-stale-exec-gone", "stale", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  after={"exec_remove": ["bin/foot"], "mtime": BASE}))
    C.append(case("W-41-stale-exec-not-executable", "stale", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  after={"modes": [("bin/foot", 0o644)], "mtime": BASE}))
    C.append(case("W-42-stale-list-removed", "stale", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  after={"files": {L_: None}, "mtime": BASE}))
    C.append(case("W-43-stale-desktop-colon-suffix", "stale",
                  {A_ + "foot.desktop": term("foot"), L_: "foot.desktop\n"}, BASE_EXECS, ARGS_ALL,
                  env={"XDG_CURRENT_DESKTOP": "Hyprland:GNOME"},
                  prime_env={"XDG_CURRENT_DESKTOP": "Hyprland"}))
    C.append(case("W-44-stale-subdir-file", "stale", {A_ + "vendor/foot.desktop": term("foot"),
                                                      L_: "vendor-foot.desktop\n"}, BASE_EXECS, ARGS_ALL,
                  after={"files": {A_ + "vendor/more.desktop": term("more")}, "exec_add": ["bin/more"],
                         "mtime": BASE}))
    C.append(case("W-45-stale-config-dir-list-added", "stale",
                  dict(BASE_TREE_FILES, **{"etc/xdg/xdg-terminals.list": ""}), BASE_EXECS, ARGS_ALL,
                  after={"files": {"etc/xdg/xdg-terminals.list": "kitty.desktop\n"}, "mtime": BASE}))
    C.append(case("W-46-stale-hash-wrong", "stale", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  cache=cache_text("0" * 32, "foot", "$ROOT/" + A_ + "foot.desktop", "foot.desktop", "", "-e",
                                   exec_words=["foot"]), primed=False))
    C.append(case("W-47-stale-hash-uppercase", "stale", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  cache=cache_text("AB" * 16, "foot", "$ROOT/" + A_ + "foot.desktop", "foot.desktop", "", "-e",
                                   exec_words=["foot"]), primed=False))
    C.append(case("W-48-stale-cmd-empty", "stale", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  cache=None, primed=True, before={"cache_patch": {"cmd": ""}}))

    # ---- invalid: the cache cannot be parsed -------------------------------------------
    HEAD = "0123456789abcdef0123456789abcdef\nfoot\n"
    C.append(case("W-51-invalid-empty", "invalid", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL, cache="", primed=False))
    C.append(case("W-52-invalid-no-terminator", "invalid", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  cache=cache_text("0123456789abcdef0123456789abcdef", "foot", "$ROOT/" + A_ + "foot.desktop",
                                   "foot.desktop", "", "-e", exec_words=["foot"], final_newline=False)[:-len(TERM)]
                        .replace(TERM, "") + "foot\n", primed=False))
    C.append(case("W-53-invalid-terminator-line-5", "invalid", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  cache=cache_text("0" * 32, "foot", "p", "f.desktop", "", "-e", exec_words=["foot"],
                                   body_at=4), primed=False))
    C.append(case("W-54-invalid-terminator-line-50", "invalid", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  cache=cache_text("0" * 32, "foot", "p", "f.desktop", "", "-e", exec_words=["foot"], fillers=39),
                  primed=False))
    C.append(case("W-55-valid-terminator-line-49", "stale", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  cache=cache_text("0" * 32, "foot", "$ROOT/" + A_ + "foot.desktop", "foot.desktop", "", "-e",
                                   exec_words=["foot"], fillers=38), primed=False))
    C.append(case("W-56-invalid-ten-lines", "invalid", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  cache="\n".join(["0" * 32, "foot", "p", "f.desktop", "", "-e", "", "", "", ""]) + "\n",
                  primed=False))
    C.append(case("W-57-invalid-unterminated-last-line", "invalid", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  cache=cache_text("0" * 32, "foot", "p", "f.desktop", "", "-e", exec_words=["foot"],
                                   final_newline=False), primed=False))
    C.append(case("W-58-invalid-cache-is-dir", "absent", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  cache="DIR", primed=False))

    # ---- disabled: the gate is off ----------------------------------------------------
    C.append(case("W-61-disabled-env-false", "disabled", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  env={"XTE_CACHE_ENABLED": "false"}, prime_env={"XTE_CACHE_ENABLED": "true"}))
    C.append(case("W-62-disabled-env-zero", "disabled", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  env={"XTE_CACHE_ENABLED": "0"}, prime_env={"XTE_CACHE_ENABLED": "true"}))
    C.append(case("W-63-disabled-env-garbage", "disabled", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  env={"XTE_CACHE_ENABLED": "maybe"}, prime_env={"XTE_CACHE_ENABLED": "true"}))
    C.append(case("W-64-disabled-env-empty-string", "disabled", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  env={"XTE_CACHE_ENABLED": ""}, prime_env={"XTE_CACHE_ENABLED": "true"}))
    C.append(case("W-65-disabled-directive-prime", "hit", {A_ + "foot.desktop": term("foot"),
                                                            L_: "/disable_cache\nfoot.desktop\n"},
                  BASE_EXECS, ARGS_ALL, prime_env={"XTE_CACHE_ENABLED": "true"}))

    # ---- HOME unset -------------------------------------------------------------------
    C.append(case("W-71-nohome-print", "nohome", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL, nohome=True, primed=False))
    C.append(case("W-72-nohome-print-id", "nohome", BASE_TREE_FILES, BASE_EXECS, ARGS_ID, nohome=True,
                  primed=False))
    C.append(case("W-73-nohome-cache-default", "nohome", BASE_TREE_FILES, BASE_EXECS, ARGS_ID, nohome=True,
                  primed=False,
                  env={"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
                       "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share",
                       "XDG_CACHE_HOME": None}))
    C.append(case("W-74-nohome-cache-home-set", "nohome", BASE_TREE_FILES, BASE_EXECS, ARGS_ID, nohome=True,
                  env={"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_DATA_HOME": "$ROOT/home/.local/share",
                       "XDG_CACHE_HOME": "$ROOT/.rw/cache"}))

    # ---- crafted-but-valid caches (the cache drives the answer) ------------------------
    C.append(case("W-81-valid-cache-other-entry", "hit-differs", BASE_TREE_FILES, BASE_EXECS, ["--print-id"],
                  cache=None, primed=True,
                  before={"cache_patch": {"eid": "kitty.desktop",
                                          "path": "$ROOT/usr/share/applications/kitty.desktop",
                                          "exec_words": ["kitty"]}}))
    C.append(case("W-82-valid-cache-empty-execarg", "hit-differs", BASE_TREE_FILES, BASE_EXECS,
                  ["--print-cmd", "--", "top"], cache=None, primed=True,
                  before={"cache_patch": {"execarg": ""}}))
    C.append(case("W-83-valid-cache-args", "hit-differs", BASE_TREE_FILES, BASE_EXECS,
                  ["--print-cmd", "--app-id=a", "--title=t", "--dir=/x", "--hold"], cache=None, primed=True,
                  before={"cache_patch": {"appidarg": "--app-id=", "titlearg": "--title", "dirarg": "--chdir=",
                                          "holdarg": "--hold"}}))
    C.append(case("W-84-valid-cache-action", "hit-differs", BASE_TREE_FILES, BASE_EXECS,
                  ["--print-id", "--print-path"], cache=None, primed=True,
                  before={"cache_patch": {"action": "srv"}}))
    C.append(case("W-85-valid-cache-multiline-exec", "hit-differs", BASE_TREE_FILES, BASE_EXECS, ["--test"],
                  cache=None, primed=True,
                  before={"cache_patch": {"exec_words": ["foot", "--a\nb", "c\nd"]}}))
    C.append(case("W-86-valid-cache-cmd-builtin", "hit", BASE_TREE_FILES, BASE_EXECS, ARGS_ALL,
                  cache=None, primed=True, before={"cache_patch": {"cmd": "printf"}}))
    C.append(case("W-87-valid-cache-path-gone-content", "hit-differs",
                  dict(BASE_TREE_FILES, **{"elsewhere/foot.desktop": term("foot")}), BASE_EXECS, ARGS_CONTENT,
                  cache=None, primed=True,
                  before={"cache_patch": {"path": "$ROOT/elsewhere/foot.desktop", "eid": "foot.desktop"}},
                  after={"files": {"elsewhere/foot.desktop": None}, "mtime": BASE}))
    C.append(case("W-88-valid-cache-path-dot-fold", "hit", BASE_TREE_FILES, BASE_EXECS, ["--print-path"],
                  cache=None, primed=True,
                  before={"cache_patch": {"path": "$ROOT/usr/share/./applications/foot.desktop",
                                          "eid": "foot.desktop"}}))
    C.append(case("W-89-valid-cache-id-only-path-empty", "hit-differs", BASE_TREE_FILES, BASE_EXECS,
                  ["--print-id", "--print-path"], cache=None, primed=True,
                  before={"cache_patch": {"path": ""}}))
    C.append(case("W-90-valid-cache-holdarg", "hit-differs", BASE_TREE_FILES, BASE_EXECS,
                  ["--print-cmd", "--hold", "--", "x"], cache=None, primed=True,
                  before={"cache_patch": {"holdarg": "--hold"}}))
    return C


def build(box, root, c, mtime):
    os.makedirs(root + "/.rw/cache", exist_ok=True)
    os.makedirs(root + "/home", exist_ok=True)
    os.makedirs(root + "/home/.cache", exist_ok=True)
    files = dict(c["files"])
    if c.get("env", {}).get("XDG_CACHE_HOME", "x") is None:
        shutil.rmtree(root + "/home/.cache", ignore_errors=True)
        os.symlink("../.rw/cache", root + "/home/.cache")
    harness.materialize(root, files, c["execs"], c["modes"], mtime)


def apply(box, root, c, mutate=True):
    if not mutate:
        return
    a = c["after"]
    for rel, text in (a.get("files") or {}).items():
        p = os.path.join(root, rel)
        if text is None:
            if os.path.isdir(p):
                shutil.rmtree(p)
            elif os.path.lexists(p):
                os.unlink(p)
            continue
        if rel.endswith("/"):
            os.makedirs(p, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(text.replace("$ROOT", root).encode("latin-1"))
    for rel in a.get("exec_add") or []:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)
    for rel in a.get("exec_remove") or []:
        p = os.path.join(root, rel)
        if os.path.lexists(p):
            os.unlink(p)
    for rel, mode in a.get("modes") or []:
        os.chmod(os.path.join(root, rel), mode)
    if a.get("mtime") is not None:
        harness.pin_mtime(root, a["mtime"])


WARM_ENV = {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
           "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share",
           "XDG_CURRENT_DESKTOP": "Hyprland"}


def env_of(c, root):
    extra = dict(WARM_ENV)
    extra.update(c["env"])
    e = harness.case_env({}, root, extra)
    if c.get("nohome"):
        e.pop("HOME", None)
    for k, v in list(e.items()):
        if v is None:
            e.pop(k)
    return e


def write_cache(box, root, c):
    path = os.path.join(root, ".rw/cache/xdg-terminal-exec")
    if c["cache"] == "DIR":
        os.makedirs(path, exist_ok=True)
        return
    if c["cache"] is not None:
        with open(path, "wb") as fh:
            fh.write(c["cache"].replace("$ROOT", root).encode("latin-1"))
        return
    if not c["primed"]:
        return                      # no cache file at all (absent)
    penv = env_of(c, root)
    penv.update(c["prime_env"])
    primed = harness.prime(box, root, penv)
    text = primed
    before = c.get("before") or {}
    if "cache_patch" in before:
        lines = text.split("\n")
        patch = before["cache_patch"]
        idx = {"hash": 0, "cmd": 1, "path": 2, "eid": 3, "action": 4, "execarg": 5, "appidarg": 6,
               "titlearg": 7, "dirarg": 8, "holdarg": 9}
        body = lines[10]
        for k, v in patch.items():
            if k in idx:
                lines[idx[k]] = v
        if "exec_words" in patch:
            body = USEP.join(patch["exec_words"]) + TERM
        lines[10] = body
        text = "\n".join(lines)
        with open(path, "wb") as fh:
            fh.write(text.encode("latin-1"))
    return primed


STATE_OF_CLASS = {"hit": "hit", "hit-differs": "hit", "stale": "stale", "invalid": "invalid",
                  "absent": "absent", "disabled": "disabled", "nohome": None}


def explain_state(box, root, env):
    rc, out, err = box.run(root, env, "tool", ["explain"])
    state = verdict = None
    for line in out.splitlines():
        if line.startswith("MADO_TERM: "):
            m = __import__("re").search(r" cache=(\S+) verdict=(\S+)$", line)
            if m:
                state, verdict = m.group(1), m.group(2)
    return state, verdict, rc


def cold_answer(box, root, env, args):
    path = os.path.join(root, ".rw/cache/xdg-terminal-exec")
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.lexists(path):
        os.unlink(path)
    return box.run(root, env, "warm", args)


def run_case(box, c):
    base = os.path.join(box.work, "w-" + c["id"])
    shutil.rmtree(base, ignore_errors=True)
    ro, rt = os.path.join(base, "o/r"), os.path.join(base, "t/r")
    for r in (ro, rt):
        build(box, r, c, c["mtime"])
    po = pt = None
    if c["cache"] is None:
        po = write_cache(box, ro, c)
        pt = write_cache(box, rt, c)
    else:
        for r in (ro, rt):
            write_cache(box, r, c)
    for r in (ro, rt):
        apply(box, r, c)
    env_o, env_t = env_of(c, ro), env_of(c, rt)
    rc_o, out_o, err_o = box.run(ro, env_o, "warm", c["args"])
    rc_t, out_t, err_t = box.run(rt, env_t, "tool", ["print"] + c["args"])
    state, verdict, _xrc = explain_state(box, rt, env_t)
    rc_c, out_c, _err_c = cold_answer(box, ro, env_o, c["args"])
    norm = lambda s, r: s.replace(r, "$ROOT")
    ok = (rc_o, norm(out_o, ro)) == (rc_t, norm(out_t, rt))
    stale_check = None
    if po is not None and pt is not None:
        stale_check = norm(po, ro) == norm(pt, rt)
    want_state = STATE_OF_CLASS[c["cls"]]
    state_ok = want_state is None or state == want_state
    differs = (rc_c, norm(out_c, ro)) != (rc_o, norm(out_o, ro))
    shutil.rmtree(base, ignore_errors=True)
    return ok and state_ok, (rc_o, norm(out_o, ro)), (rc_t, norm(out_t, rt)), err_t, {
        "twin_cache_same": stale_check, "state": state, "want_state": want_state,
        "verdict": verdict, "differs_from_cold": differs,
        "cold": (rc_c, norm(out_c, ro))}


def main(only=None):
    box = harness.Box(harness.S)
    cs = cases()
    if only:
        cs = [c for c in cs if only in c["id"]]
    bad = 0
    lines = []
    for c in cs:
        try:
            ok, o, t, err, same = run_case(box, c)
        except SystemExit as ex:
            print("SETUP FAIL %s: %s" % (c["id"], ex))
            bad += 1
            continue
        lines.append("%s class=%s args=%r" % (c["id"], c["cls"], c["args"]))
        lines.append("  oracle rc=%d out=%r" % o)
        lines.append("  tool   rc=%d out=%r" % t)
        lines.append("  cold   rc=%d out=%r" % same["cold"])
        lines.append("  state=%s want=%s verdict=%s differs_from_cold=%s twin_cache_same=%r"
                     % (same["state"], same["want_state"], same["verdict"], same["differs_from_cold"],
                        same["twin_cache_same"]))
        if not ok:
            lines.append("  VERDICT DIFF tool_stderr=%r" % err[:300])
            bad += 1
        else:
            lines.append("  VERDICT agree")
        print("\n".join(lines[-4:]))
    print("WARM: %d/%d agree" % (len(cs) - bad, len(cs)))
    with open(os.path.join(harness.S, "warm-results.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else None) else 0)
