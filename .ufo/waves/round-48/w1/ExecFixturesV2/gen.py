#!/usr/bin/env python3
"""gen.py - C1 fixture set v2 (round 48 w1, seat ExecFixturesV2).

Builds fixtures-v2.json: >= 120 NEW cases for the warm-cache path of xdg-terminal-exec v0.14.3, every `expect`
produced by THREE runs of the pinned resolver (sha256 89f2be...27ac) in the C1 bwrap allowlist, plus the COLD answer
(same tree, no cache) for every warm case.

Fixture schema v2 = the round-47 schema
    id, class, env ($ROOT), files, exec, args, expect {rc, stdout}
plus (all optional):
    "mtime": <epoch seconds>          pin st_mtime of every materialized file and dir (deterministic `ls -l` dates;
                                      the resolver's gen_hash is an md5 over `LANG=C ls -LRl` of the list/app paths)
    "prime": {"args": [...]}          one cold run before the scored run; its background `save_cache "$1" &` is waited
                                      for (see prime-wrap.sh - the resolver runs as PID 1 of the sandbox otherwise, so
                                      the background save dies with the PID namespace; the wrapper runs the resolver
                                      under a bash parent that outlives the save and polls for the cache file)
    "after": {"files": {path: text|null}, "exec_add": [...], "exec_remove": [...], "env": {...}, "mtime": <epoch>,
              "cache_lines": {"<line no>": "<replacement>"}, "cache_sub": [[find, replace], ...],
              "cache_append": ["<line>", ...]}
                                      mutations applied AFTER priming and BEFORE the scored run; "files" text/null
                                      (null deletes), mtime re-pins every file and dir (same value as "mtime" keeps
                                      the hash valid); cache_lines/sub/append edit the primed cache file itself
    "cache": "<literal cache text, $ROOT substituted>"   pre-seeded cache, no priming
    "unset": ["HOME", ...]            env names removed AFTER the harness sets HOME/PATH/XDG_CACHE_HOME/LANG
    "cold": {"rc": n, "stdout": "..."}                    recorded cold answer (same tree/env, XDG_CACHE_HOME empty)
    "meta": {probe, cache_state, warm_differs_from_cold, readdir_order, fs, note}
`expect` is always the scored run's (rc, stdout) with the case root replaced by $ROOT.

Resolution harness: bwrap argv copied from quality/counters/c1-r47-terminal.py Box.argv (same 7 externals at
/oracle/bin, /usr/lib ro, host bash at /bin/sh,/bin/bash, /dev,/proc,tmpfs /tmp, case root ro + root/.rw rw, no /etc so
`ls -l` prints numeric ids, PATH=<root>/bin:/oracle/bin, HOME=<root>/home, XDG_CACHE_HOME=<root>/.rw/cache).
Scored runs are the pin as PID 1, like the counter. Runs are `--print-*` only (never a launch).

Usage: python3 gen.py --work /fast/scratch/hyaku/mado-r48/ExecFixturesV2/work --out fixtures-v2.json \
                      --receipt fixtures-v2.receipt.json [--only CLASS]
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
PIN = os.path.join(LANE, ".ufo/waves/round-47/fetch/xdg-terminal-exec")
PIN_SHA256 = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"
EXTERNALS = ("tr", "find", "awk", "ls", "md5sum", "mkdir", "rm")
MT = 1577836800  # 2020-01-01T00:00:00Z: `ls -l` prints the old ("Mon dd  YYYY") date form, stable forever

WRAP = r'''
/oracle/xdg-terminal-exec "$@"
rc=$?
c=${XDG_CACHE_HOME:-${HOME}/.cache}/xdg-terminal-exec
e=$'\036END_OF_EXEC_USEP'
t0=${EPOCHREALTIME/./}
while :; do
    v=
    [ -f "$c" ] && v=$(< "$c")
    case "$v" in *"$e") break ;; esac
    case "${XTE_CACHE_ENABLED-}" in 0|false|False|FALSE|no|No|NO|banana) break ;; esac
    t=${EPOCHREALTIME/./}
    [ $((t - t0)) -gt 5000000 ] && break
done
exit $rc
'''

LIST = "home/.config/hyprland-xdg-terminals.list"
APP = "home/.local/share/applications"
GLOBAL_LIST = "home/.config/xdg-terminals.list"
USR_APP = "usr/share/applications"

ENV_BASE = {
    "XDG_CONFIG_DIRS": "$ROOT/cd",
    "XDG_CONFIG_HOME": "$ROOT/home/.config",
    "XDG_CURRENT_DESKTOP": "Hyprland",
    "XDG_DATA_DIRS": "$ROOT/usr/share",
    "XDG_DATA_HOME": "$ROOT/home/.local/share",
}


class Bad(Exception):
    pass


# ------------------------------------------------------------------------------------------------ sandbox
class Box:
    def __init__(self, work):
        self.work = work
        self.bwrap = shutil.which("bwrap")
        if not self.bwrap:
            raise Bad("bwrap missing")
        self.bin = tempfile_dir(work, "bin-")
        for n in EXTERNALS:
            src = shutil.which(n, path="/usr/bin")
            if not src:
                raise Bad("external %s missing" % n)
            shutil.copy(os.path.realpath(src), os.path.join(self.bin, n))
        self.pin = os.path.join(tempfile_dir(work, "pin-"), "xdg-terminal-exec")
        blob = open(PIN, "rb").read()
        if hashlib.sha256(blob).hexdigest() != PIN_SHA256:
            raise Bad("pin sha256 mismatch")
        open(self.pin, "wb").write(blob)
        os.chmod(self.pin, 0o755)
        self.bash = os.path.realpath("/usr/bin/bash")

    def argv(self, root, env, args, wrap):
        a = [self.bwrap, "--unshare-all", "--die-with-parent", "--new-session", "--clearenv",
             "--ro-bind", "/usr/lib", "/usr/lib", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
             "--ro-bind", self.bash, "/bin/sh", "--ro-bind", self.bash, "/bin/bash",
             "--ro-bind", self.bin, "/oracle/bin", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
             "--ro-bind", root, root, "--bind", os.path.join(root, ".rw"), os.path.join(root, ".rw"),
             "--ro-bind", self.pin, "/oracle/xdg-terminal-exec", "--chdir", root]
        for k in sorted(env):
            a += ["--setenv", k, env[k]]
        if wrap:
            a += ["/bin/bash", "-c", WRAP, "xte"] + list(args)
        else:
            a += ["/oracle/xdg-terminal-exec"] + list(args)
        return a

    def run(self, root, env, args, wrap=False, timeout=30):
        p = subprocess.run(self.argv(root, env, args, wrap), capture_output=True, timeout=timeout,
                           env={"PATH": "/usr/bin"})
        return (p.returncode,
                p.stdout.decode("utf-8", "surrogateescape"),
                p.stderr.decode("utf-8", "surrogateescape"))


def tempfile_dir(parent, prefix):
    return __import__("tempfile").mkdtemp(dir=parent, prefix=prefix)


# ------------------------------------------------------------------------------------------------ materialize
def cache_path(root, case):
    """$XDG_CACHE_HOME/xdg-terminal-exec, or $HOME/.cache/xdg-terminal-exec when the case unsets XDG_CACHE_HOME."""
    if (case.get("meta") or {}).get("cache_dir") == "home":
        return os.path.join(root, "home", ".cache", "xdg-terminal-exec")
    return os.path.join(root, ".rw", "cache", "xdg-terminal-exec")


def materialize(root, case, with_cache):
    os.makedirs(os.path.join(root, "home"))
    os.makedirs(os.path.join(root, ".rw", "cache"))
    order = case.get("meta", {}).get("files_order") or list(case["files"].keys())
    seen = set()
    for rel in list(order) + [r for r in case["files"] if r not in order]:
        if rel in seen:
            continue
        seen.add(rel)
        if ".." in rel.split("/") or rel.startswith("/"):
            raise Bad("unsafe path %r in %s" % (rel, case["id"]))
        text = case["files"][rel]
        p = os.path.join(root, rel)
        if rel.endswith("/") or text is None:
            os.makedirs(p, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(text.replace("$ROOT", root).encode("utf-8", "surrogateescape"))
    for rel in case["exec"]:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if not os.path.exists(p):
            with open(p, "w") as fh:
                fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)
    if with_cache and case.get("cache") is not None:
        p = cache_path(root, case)
        if os.path.isdir(p):
            raise Bad("cache path is a directory in %s" % case["id"])
        with open(p, "wb") as fh:
            fh.write(case["cache"].replace("$ROOT", root).encode("utf-8", "surrogateescape"))
    if case.get("mtime") is not None:
        pin_mtime(root, case["mtime"])


def pin_mtime(root, t):
    for dp, dns, fns in os.walk(root, topdown=False):
        if os.path.basename(dp) in (".rw",) and dp == os.path.join(root, ".rw"):
            pass
        for n in fns:
            os.utime(os.path.join(dp, n), (t, t))
        for n in dns:
            os.utime(os.path.join(dp, n), (t, t))


def build_env(case, root, after_env=None, extra=None):
    env = {k: v.replace("$ROOT", root) for k, v in case["env"].items()}
    env["HOME"] = os.path.join(root, "home")
    env["PATH"] = os.path.join(root, "bin") + ":/oracle/bin"
    env["XDG_CACHE_HOME"] = os.path.join(root, ".rw", "cache")
    env["LANG"] = "C.UTF-8"
    for src in (after_env or {}, extra or {}):
        for k, v in src.items():
            if v is None:
                env.pop(k, None)
            else:
                env[k] = v.replace("$ROOT", root)
    for k in case.get("unset", []):
        env.pop(k, None)
    return env


def apply_after(root, case, with_cache=True):
    after = case.get("after") or {}
    for rel, text in (after.get("files") or {}).items():
        p = os.path.join(root, rel)
        if text is None:
            if os.path.isdir(p):
                shutil.rmtree(p)
            elif os.path.exists(p):
                os.unlink(p)
            continue
        if rel.endswith("/"):
            os.makedirs(p, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(text.replace("$ROOT", root).encode("utf-8", "surrogateescape"))
    for rel in after.get("exec_add") or []:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)
    for rel in after.get("exec_remove") or []:
        p = os.path.join(root, rel)
        if os.path.exists(p):
            os.unlink(p)
    for rel, mode in (after.get("modes") or {}).items():
        os.chmod(os.path.join(root, rel), int(mode))
    cpath = cache_path(root, case)
    if with_cache and (after.get("cache_lines") or after.get("cache_sub")
                       or after.get("cache_append") is not None):
        text = open(cpath, encoding="utf-8", errors="surrogateescape").read()
        if after.get("cache_lines"):
            lines = text.split("\n")
            for ln, val in after["cache_lines"].items():
                i = int(ln) - 1
                if i >= len(lines):
                    raise Bad("cache_lines %s beyond %d lines in %s" % (ln, len(lines), case["id"]))
                lines[i] = val
            text = "\n".join(lines)
        for pair in after.get("cache_sub") or []:
            old, new = pair
            if old not in text:
                raise Bad("cache_sub find %r absent in %s" % (old, case["id"]))
            text = text.replace(old, new)
        for ln in after.get("cache_append") or []:
            text = text + ln + "\n"
        with open(cpath, "wb") as fh:
            fh.write(text.encode("utf-8", "surrogateescape"))
    if after.get("mtime") is not None:
        pin_mtime(root, after["mtime"])


CACHE_STATES = ("cache is actual", "cache is out-of-date", "invalid cache data", "no cache data",
                "cache is disabled, removing", "reached cache line limit")


def cache_state_from(stderr):
    hits = [s for s in CACHE_STATES if s in stderr]
    if "cache is actual" in hits:
        return "hit"
    if "cache is out-of-date" in hits:
        return "stale"
    if "invalid cache data" in hits or "reached cache line limit" in hits:
        return "invalid"
    if "cache is disabled, removing" in hits:
        return "disabled"
    if "no cache data" in hits:
        return "absent"
    if "unbound variable" in stderr:
        return "error"
    return "unknown"


def readdir(root, case):
    out = {}
    for rel in case["files"]:
        if rel.endswith("/"):
            p = os.path.join(root, rel)
            try:
                out[rel] = [e.name for e in os.scandir(p)]
            except OSError:
                pass
    for rel in ("home/.local/share/applications", "usr/share/applications", "usr/local/share/applications",
                "home/.config"):
        p = os.path.join(root, rel)
        if os.path.isdir(p):
            out[rel] = [e.name for e in os.scandir(p)]
    return out


def run_trial(box, case, root, cached):
    materialize(root, case, with_cache=cached)
    env = build_env(case, root)
    if case.get("prime"):
        cpath = cache_path(root, case)
        rc, out, err = box.run(root, env, case["prime"]["args"], wrap=True)
        if not os.path.exists(cpath):
            raise Bad("prime produced no cache (rc=%d) in %s: %r" % (rc, case["id"], err[-300:]))
        blob = open(cpath, "rb").read()
        if b"\x1eEND_OF_EXEC_USEP" not in blob:
            raise Bad("prime left an incomplete cache (%d bytes) in %s" % (len(blob), case["id"]))
    if case.get("after"):
        apply_after(root, case)
    env2 = build_env(case, root, (case.get("after") or {}).get("env"))
    dbg = dict(env2)
    dbg["XTE_DEBUG"] = "1"
    rc, out, err = box.run(root, dbg, case["args"])
    return rc, out.replace(root, "$ROOT"), err, readdir(root, case)


def run_cold(box, case, root):
    materialize(root, case, with_cache=False)
    if case.get("after"):
        apply_after(root, case, with_cache=False)
    env = build_env(case, root, (case.get("after") or {}).get("env"))
    env["XDG_CACHE_HOME"] = os.path.join(root, ".rw", "nocache")
    os.makedirs(env["XDG_CACHE_HOME"], exist_ok=True)
    rc, out, err = box.run(root, env, case["args"])
    return rc, out.replace(root, "$ROOT"), err


# ------------------------------------------------------------------------------------------------ fixtures
def sub(text, old, new):
    if old not in text:
        raise Bad("edit target absent: %r" % old)
    if len(old.encode()) != len(new.encode()):
        raise Bad("edit changes byte length: %r -> %r" % (old, new))
    return text.replace(old, new)


def subn(text, old, new):
    if old not in text:
        raise Bad("edit target absent: %r" % old)
    return text.replace(old, new)


def entry(exec_="foot --a", cats="System;TerminalEmulator;", arg_exec="TerminalArgExec=-e\n",
          extra="", name="Terminal"):
    return ("[Desktop Entry]\nType=Application\nName=%s\nCategories=%s\n%s%sExec=%s\n"
            % (name, cats, arg_exec, extra, exec_))


def case(cid, cls, files, execs, args, *, prime=None, after=None, mtime=None, cache=None, unset=None,
         env_extra=None, note="", files_order=None, cache_home=None):
    env = dict(ENV_BASE)
    for k, v in (env_extra or {}).items():
        if v is None:
            env.pop(k, None)
            unset = list(unset or []) + [k]
        else:
            env[k] = v
    c = {"id": cid, "class": cls, "env": env, "files": files, "exec": execs,
         "args": list(args), "expect": None}
    if prime is not None:
        c["prime"] = {"args": list(prime)}
    if after is not None:
        c["after"] = after
    if mtime is not None:
        c["mtime"] = mtime
    if cache is not None:
        c["cache"] = cache
    if unset:
        c["unset"] = list(unset)
    c["meta"] = {"probe": "prime" if prime else ("cache" if cache is not None else "cold"),
                 "note": note}
    if cache_home:
        c["meta"]["cache_dir"] = cache_home
        c["unset"] = list(c.get("unset") or []) + ["XDG_CACHE_HOME"]
    if files_order:
        c["meta"]["files_order"] = files_order
    return c


def warm(cid, cls, files, execs, args, *, prime, after=None, note="", env_extra=None, exec_add=None,
         cache_home=None):
    """A primed case: mtime pinned, after.mtime pinned back to the same value."""
    after = dict(after or {})
    after.setdefault("mtime", MT)
    if exec_add:
        after["exec_add"] = list(after.get("exec_add") or []) + list(exec_add)
    return case(cid, cls, files, execs, args, prime=prime, after=after, mtime=MT, env_extra=env_extra,
                note=note, cache_home=cache_home)


def build(only=None):
    out = []
    add = out.append

    def keep(c):
        if only and c["class"] != only:
            return
        add(c)

    LISTF = lambda line: {LIST: line}
    F = lambda text=None, arg_exec="TerminalArgExec=-e\n", extra="", exec_="foot --a", cats="System;TerminalEmulator;": {
        APP + "/foot.desktop": entry(exec_, cats=cats, arg_exec=arg_exec, extra=extra)}
    PC = ["--print-cmd"]

    # ============================== WARM-HIT-DIFFERS ==============================
    # same-size same-minute content edits: the resolver's hash does not move, so a warm cache answers instead
    base = {**LISTF("foot.desktop\n"), **F()}
    keep(warm("v2-wd-01-exec-firstword", "WARM-HIT-DIFFERS", base, ["bin/foot", "bin/feot"], PC,
              prime=PC, after={"files": {APP + "/foot.desktop": sub(entry(), "Exec=foot --a", "Exec=feot --a")}},
              note="Exec[0] renamed, both stubs present; cached cmd=foot still resolves -> hit"))
    keep(warm("v2-wd-02-exec-secondword", "WARM-HIT-DIFFERS", base, ["bin/foot"], PC,
              prime=PC, after={"files": {APP + "/foot.desktop": sub(entry(), "foot --a", "foot --b")}},
              note="Exec argument changed, same size and mtime minute"))
    keep(warm("v2-wd-03-exec-quoted", "WARM-HIT-DIFFERS", {**LISTF("foot.desktop\n"), **F(exec_='foot "x y"')},
              ["bin/foot"], PC, prime=PC,
              after={"files": {APP + "/foot.desktop": sub(entry('foot "x y"'), '"x y"', '"z y"')}},
              note="quoted Exec word changed same size"))
    keep(warm("v2-wd-04-exec-three-words", "WARM-HIT-DIFFERS", {**LISTF("foot.desktop\n"), **F(exec_="foot --a --c")},
              ["bin/foot"], PC, prime=PC,
              after={"files": {APP + "/foot.desktop": sub(entry("foot --a --c"), "--a --c", "--a --d")}},
              note="last cached word changed"))
    keep(warm("v2-wd-05-argexec", "WARM-HIT-DIFFERS", base, ["bin/foot"], ["--print-cmd", "--", "htop"],
              prime=["--print-cmd", "--", "htop"],
              after={"files": {APP + "/foot.desktop": sub(entry(), "TerminalArgExec=-e", "TerminalArgExec=-q")}},
              note="TerminalArgExec changed same size; cached EXECARG=-e"))
    keep(warm("v2-wd-06-argdir", "WARM-HIT-DIFFERS", {**LISTF("foot.desktop\n"), **F(extra="TerminalArgDir=--chdir=\n")},
              ["bin/foot"], ["--print-cmd", "--dir=/srv"], prime=["--print-cmd", "--dir=/srv"],
              after={"files": {APP + "/foot.desktop": sub(entry(extra="TerminalArgDir=--chdir=\n"),
                                                          "--chdir=", "--chdor=")}},
              note="TerminalArgDir changed same size; --dir value comes from the current argv"))
    keep(warm("v2-wd-07-argtitle", "WARM-HIT-DIFFERS", {**LISTF("foot.desktop\n"), **F(extra="TerminalArgTitle=--title\n")},
              ["bin/foot"], ["--print-cmd", "--title=T x"], prime=["--print-cmd", "--title=T x"],
              after={"files": {APP + "/foot.desktop": sub(entry(extra="TerminalArgTitle=--title\n"),
                                                          "--title", "--tille")}},
              note="TerminalArgTitle changed same size"))
    keep(warm("v2-wd-08-argappid", "WARM-HIT-DIFFERS", {**LISTF("foot.desktop\n"), **F(extra="TerminalArgAppId=--class=\n")},
              ["bin/foot"], ["--print-cmd", "--app-id=app"], prime=["--print-cmd", "--app-id=app"],
              after={"files": {APP + "/foot.desktop": sub(entry(extra="TerminalArgAppId=--class=\n"),
                                                          "--class=", "--clazz=")}},
              note="TerminalArgAppId changed same size"))
    keep(warm("v2-wd-09-arghold", "WARM-HIT-DIFFERS", {**LISTF("foot.desktop\n"), **F(extra="TerminalArgHold=--hold\n")},
              ["bin/foot"], ["--print-cmd", "--hold"], prime=["--print-cmd", "--hold"],
              after={"files": {APP + "/foot.desktop": sub(entry(extra="TerminalArgHold=--hold\n"),
                                                          "--hold", "--holl")}},
              note="TerminalArgHold changed same size"))
    keep(warm("v2-wd-10-argexec-args-hold", "WARM-HIT-DIFFERS",
              {**LISTF("foot.desktop\n"), **F(extra="TerminalArgDir=--chdir=\nTerminalArgHold=--hold\n")},
              ["bin/foot"], ["--print-cmd", "--dir=/srv", "--hold", "--", "htop"],
              prime=["--print-cmd", "--dir=/srv", "--hold", "--", "htop"],
              after={"files": {APP + "/foot.desktop": sub(entry(extra="TerminalArgDir=--chdir=\nTerminalArgHold=--hold\n"),
                                                          "--hold", "--held")}},
              note="hold arg changed while dir arg cached"))
    # list preference edits of equal size
    two = {LIST: "aaaa.desktop\n",
           APP + "/aaaa.desktop": entry("aaaa --a"), APP + "/bbbb.desktop": entry("bbbb --a")}
    keep(warm("v2-wd-11-list-swap", "WARM-HIT-DIFFERS", two, ["bin/aaaa", "bin/bbbb"], ["--print-cmd", "--print-id"],
              prime=["--print-cmd"], after={"files": {LIST: "bbbb.desktop\n"}},
              note="list line changed same size, both ids valid; warm keeps aaaa"))
    keep(warm("v2-wd-12-list-order", "WARM-HIT-DIFFERS",
              {**two, LIST: "aaaa.desktop\nbbbb.desktop\n"}, ["bin/aaaa", "bin/bbbb"], ["--print-cmd", "--print-id"],
              prime=["--print-cmd"], after={"files": {LIST: "bbbb.desktop\naaaa.desktop\n"}},
              note="list order swapped, same total size"))
    keep(warm("v2-wd-13-list-comment", "WARM-HIT-DIFFERS", {**two, LIST: "# aaaa\nbbbb.desktop\n"},
              ["bin/aaaa", "bin/bbbb"], ["--print-cmd", "--print-id"], prime=["--print-cmd"],
              after={"files": {LIST: "# aaaa\naaaa.desktop\n"}},
              note="list selection line changed same size behind a comment"))
    keep(warm("v2-wd-14-list-second-line", "WARM-HIT-DIFFERS",
              {**two, LIST: "missing.desktop\naaaa.desktop\n"}, ["bin/aaaa", "bin/bbbb"],
              ["--print-cmd", "--print-id"], prime=["--print-cmd"],
              after={"files": {LIST: "missing.desktop\nbbbb.desktop\n"}},
              note="second list line changed same size"))
    # entry-level invalidations that a warm cache does not re-check
    keep(warm("v2-wd-15-tryexec-missing", "WARM-HIT-DIFFERS",
              {**LISTF("foot.desktop\n"), **F(extra="TryExec=foot\n")}, ["bin/foot"], PC, prime=PC,
              after={"files": {APP + "/foot.desktop": sub(entry(extra="TryExec=foot\n"), "TryExec=foot", "TryExec=feot")}},
              note="TryExec target removed while cached cmd (exec[0]) still resolves"))
    keep(warm("v2-wd-16-tryexec-stub-removed", "WARM-HIT-DIFFERS",
              {**LISTF("foot.desktop\n"), **F(extra="TryExec=tcheck\n")}, ["bin/foot", "bin/tcheck"], PC, prime=PC,
              after={"exec_remove": ["bin/tcheck"]},
              note="TryExec stub unlinked, not part of the hashed listing; exec[0] still resolves"))
    keep(warm("v2-wd-17-cats-degraded", "WARM-HIT-DIFFERS", base, ["bin/foot"], PC, prime=PC,
              after={"files": {APP + "/foot.desktop": sub(entry(), "Categories=System;TerminalEmulator;",
                                                          "Categories=System;TerminalEmulatoz;")}},
              note="entry no longer a TerminalEmulator for a cold run; warm keeps it"))
    keep(warm("v2-wd-18-header-degraded", "WARM-HIT-DIFFERS", base, ["bin/foot"], PC, prime=PC,
              after={"files": {APP + "/foot.desktop": sub(entry(), "[Desktop Entry]", "[Desktop Entrx]")}},
              note="group header broken same size; cold loses Exec"))
    keep(warm("v2-wd-19-exec-blanked", "WARM-HIT-DIFFERS", base, ["bin/foot"], PC, prime=PC,
              after={"files": {APP + "/foot.desktop": sub(entry(), "Exec=foot --a", "Exec=        ")}},
              note="Exec value blanked same size; cold has no command"))
    keep(warm("v2-wd-20-dirarg-key-degraded", "WARM-HIT-DIFFERS",
              {**LISTF("foot.desktop\n"), **F(extra="TerminalArgDir=--chdir=\n")},
              ["bin/foot"], ["--print-cmd", "--dir=/srv"], prime=["--print-cmd", "--dir=/srv"],
              after={"files": {APP + "/foot.desktop": sub(entry(extra="TerminalArgDir=--chdir=\n"),
                                                          "TerminalArgDir=", "TerminalArgDix=")}},
              note="key name degraded same size: cold ignores the line, warm keeps the cached dir arg"))
    keep(warm("v2-wd-36-hold-key-degraded", "WARM-HIT-DIFFERS",
              {**LISTF("foot.desktop\n"), **F(extra="TerminalArgHold=--hold\n")},
              ["bin/foot"], ["--print-cmd", "--hold"], prime=["--print-cmd", "--hold"],
              after={"files": {APP + "/foot.desktop": sub(entry(extra="TerminalArgHold=--hold\n"),
                                                          "TerminalArgHold=", "TerminalArgHolx=")}},
              note="hold key degraded same size"))
    # action cache
    act = entry(extra="Actions=new;old;\n") + "[Desktop Action new]\nExec=foot --n\n[Desktop Action old]\nExec=foot --o\n"
    keep(warm("v2-wd-21-action-exec", "WARM-HIT-DIFFERS", {LIST: "foot.desktop:new\n", APP + "/foot.desktop": act},
              ["bin/foot"], PC, prime=PC,
              after={"files": {APP + "/foot.desktop": sub(act, "Exec=foot --n", "Exec=foot --z")}},
              note="cached action new; its group Exec changed same size"))
    keep(warm("v2-wd-22-action-list", "WARM-HIT-DIFFERS", {LIST: "foot.desktop:new\n", APP + "/foot.desktop": act},
              ["bin/foot"], ["--print-id"], prime=["--print-cmd"],
              after={"files": {LIST: "foot.desktop:old\n"}},
              note="list action suffix changed same size; --print-id prints the cached id:action"))
    # compat env change after priming
    keep(warm("v2-wd-23-compat-strict", "WARM-HIT-DIFFERS",
              {**LISTF("foot.desktop\n"), APP + "/foot.desktop": entry(arg_exec="")},
              ["bin/foot"], ["--print-cmd", "--", "htop"], prime=["--print-cmd", "--", "htop"],
              after={"env": {"XTE_EXECARG_COMPAT": "0"}},
              note="entry has no TerminalArgExec: strict cold discards it, warm keeps cached -e"))
    keep(warm("v2-wd-24-compat-false-literal", "WARM-HIT-DIFFERS",
              {**LISTF("foot.desktop\n"), APP + "/foot.desktop": entry(extra="ExecArg=-x\n")},
              ["bin/foot"], ["--print-cmd", "--", "htop"], prime=["--print-cmd", "--", "htop"],
              after={"env": {"XTE_EXECARG_COMPAT": "false"}},
              note="literal 'false' (unlike '0') ignores legacy ExecArg, so strict cold discards the entry"))
    # /disable_cache directive added in a same-size edit; warm never reads the list
    keep(warm("v2-wd-25-disable-directive", "WARM-HIT-DIFFERS", {**LISTF("/enable_cache \nfoot.desktop\n"), **F()},
              ["bin/foot", "bin/feot"], PC, prime=PC,
              after={"files": {LIST: "/disable_cache\nfoot.desktop\n",
                               APP + "/foot.desktop": sub(entry(), "Exec=foot --a", "Exec=feot --a")}},
              note="list gains /disable_cache in a same-size edit; warm never reads the list, cold reads it "
                   "and picks up the new Exec"))
    # exec[0] name cached but a different valid entry appears in the list (same size)
    keep(warm("v2-wd-26-cached-path-print", "WARM-HIT-DIFFERS", two, ["bin/aaaa", "bin/bbbb"],
              ["--print-cmd", "--print-path"], prime=["--print-cmd"], after={"files": {LIST: "bbbb.desktop\n"}},
              note="--print-path prints the cached path"))
    # empty execarg cached value with --hold only
    keep(warm("v2-wd-27-hold-only", "WARM-HIT-DIFFERS", {**LISTF("foot.desktop\n"), **F(extra="TerminalArgHold=--hold\n")},
              ["bin/foot"], ["--print-cmd", "--hold"], prime=["--print-cmd", "--hold"],
              after={"files": {APP + "/foot.desktop": sub(entry(extra="TerminalArgHold=--hold\n"),
                                                          "TerminalArgHold=--hold", "TerminalArgHold=------")}},
              note="hold arg replaced by dashes, same size"))
    # cache hit with a *renamed* exec[0] whose stub exists, and a list that would pick another entry
    keep(warm("v2-wd-28-entry-and-list", "WARM-HIT-DIFFERS",
              {**LISTF("foot.desktop\nkkit.desktop\n"),
               APP + "/foot.desktop": entry(), APP + "/kkit.desktop": entry("kkit --k")},
              ["bin/foot", "bin/kkit"], PC, prime=PC,
              after={"files": {LIST: "kkit.desktop\nfoot.desktop\n",
                               APP + "/kkit.desktop": sub(entry("kkit --k"), "kkit --k", "kkit --m")}},
              note="both list order and the second entry changed; warm keeps foot"))
    # XDG_CURRENT_DESKTOP is in the hash: changing it must NOT be a hit (proved in WARM-INVALID),
    # while XTE_* knobs are not hashed
    keep(warm("v2-wd-29-argexec-compat-flag", "WARM-HIT-DIFFERS",
              {**LISTF("foot.desktop\n"), **F(extra="X-TerminalArgExec=-x\n")},
              ["bin/foot"], ["--print-cmd", "--", "htop"], prime=["--print-cmd", "--", "htop"],
              after={"files": {APP + "/foot.desktop": sub(entry(extra="X-TerminalArgExec=-x\n"),
                                                          "-x\n", "-y\n")}},
              note="X-TerminalArgExec cached name, same-size edit"))
    keep(warm("v2-wd-30-print-id-and-path", "WARM-HIT-DIFFERS", two, ["bin/aaaa", "bin/bbbb"],
              ["--print-id", "--print-path"], prime=["--print-cmd"], after={"files": {LIST: "bbbb.desktop\n"}},
              note="id+path from the cache, no command printed"))
    keep(warm("v2-wd-31-exec-rename-and-second", "WARM-HIT-DIFFERS",
              {**LISTF("foot.desktop\n"), **F(exec_="foot --a --b")}, ["bin/foot", "bin/feot"], PC, prime=PC,
              after={"files": {APP + "/foot.desktop": sub(entry("foot --a --b"), "foot --a --b", "feot --a --b")}},
              note="first cached word renamed, cached cmd foot still on PATH"))
    keep(warm("v2-wd-32-dir-value-only", "WARM-HIT-DIFFERS", {**LISTF("foot.desktop\n"), **F(extra="TerminalArgDir=--chdir=\n")},
              ["bin/foot"], ["--print-cmd", "--dir=/opt"], prime=["--print-cmd", "--dir=/srv"],
              after={"files": {APP + "/foot.desktop": sub(entry(extra="TerminalArgDir=--chdir=\n"),
                                                          "--chdir=\n", "--chdoq=\n")}},
              note="dir value differs from prime and the arg name changed; cached name + current value"))
    keep(warm("v2-wd-33-appid-hold", "WARM-HIT-DIFFERS",
              {**LISTF("foot.desktop\n"), **F(extra="TerminalArgAppId=--class=\nTerminalArgHold=--hold\n")},
              ["bin/foot"], ["--print-cmd", "--app-id=A", "--hold", "--", "top"],
              prime=["--print-cmd", "--app-id=A", "--hold", "--", "top"],
              after={"files": {APP + "/foot.desktop": sub(entry(extra="TerminalArgAppId=--class=\nTerminalArgHold=--hold\n"),
                                                          "--class=", "--clasz=")}},
              note="appid arg name changed, hold cached"))
    keep(warm("v2-wd-34-exec-rename-same-cmd", "WARM-HIT-DIFFERS", base, ["bin/foot", "bin/foob"], PC, prime=PC,
              after={"files": {APP + "/foot.desktop": sub(entry(), "foot --a", "foob --a")}},
              note="exec[0] renamed to another present stub"))
    keep(warm("v2-wd-35-cache-subst-exec-word", "WARM-HIT-DIFFERS", base, ["bin/foot"], PC, prime=PC,
              after={"cache_sub": [["foot\x1f--a", "foot\x1f--c"]]},
              note="edit the cached command tokens themselves, hash untouched; warm answer differs from cold"))

    # ============================== WARM-HIT-SAME ==============================
    keep(warm("v2-ws-01-name", "WARM-HIT-SAME", base, ["bin/foot"], PC, prime=PC,
              after={"files": {APP + "/foot.desktop": sub(entry(), "Name=Terminal", "Name=Terminax")}},
              note="Name is not printed; cache used, output equals cold"))
    keep(warm("v2-ws-02-cats-same", "WARM-HIT-SAME", base, ["bin/foot"], PC, prime=PC,
              after={"files": {APP + "/foot.desktop": sub(entry(), "Categories=System;TerminalEmulator;",
                                                          "Categories=System;TerminalEmulator ")}},
              note="Categories still TerminalEmulator-ish; cold still selects"))
    keep(warm("v2-ws-03-tryexec-existing", "WARM-HIT-SAME", {**LISTF("foot.desktop\n"), **F(extra="TryExec=foot\n")},
              ["bin/foot", "bin/feot"], PC, prime=PC,
              after={"files": {APP + "/foot.desktop": sub(entry(extra="TryExec=foot\n"), "TryExec=foot", "TryExec=feot")},
                     "exec_add": ["bin/feot"]},
              note="TryExec points at another existing stub"))
    keep(warm("v2-ws-04-content-mut", "WARM-HIT-SAME", base, ["bin/foot"], ["--print-content"], prime=["--print-cmd"],
              after={"files": {APP + "/foot.desktop": sub(entry(), "Name=Terminal", "Name=Terminax")}},
              note="--print-content reads the cached path, so the new bytes are printed by both"))
    keep(warm("v2-ws-05-comment", "WARM-HIT-SAME", {**LISTF("# note\nfoot.desktop\n"), **F()}, ["bin/foot"], PC,
              prime=PC, after={"files": {LIST: "# nood\nfoot.desktop\n"}},
              note="list comment changed; selection equal"))
    keep(warm("v2-ws-06-dir-arg-unchanged", "WARM-HIT-SAME", {**LISTF("foot.desktop\n"), **F(extra="TerminalArgDir=--chdir=\n")},
              ["bin/foot"], ["--print-cmd", "--dir=/srv"], prime=["--print-cmd", "--dir=/opt"],
              note="cached arg name, value from the current argv; cold agrees"))
    keep(warm("v2-ws-07-title-value", "WARM-HIT-SAME", {**LISTF("foot.desktop\n"), **F(extra="TerminalArgTitle=--title\n")},
              ["bin/foot"], ["--print-cmd", "--title=New"], prime=["--print-cmd", "--title=Old"],
              note="title value is not cached"))
    keep(warm("v2-ws-08-compat-with-termarg", "WARM-HIT-SAME", base, ["bin/foot"], ["--print-cmd", "--", "htop"],
              prime=["--print-cmd", "--", "htop"], after={"env": {"XTE_EXECARG_COMPAT": "0"}},
              note="strict cold still accepts: entry has TerminalArgExec"))
    keep(warm("v2-ws-09-trailing-args", "WARM-HIT-SAME", base, ["bin/foot"], ["--print-cmd", "--", "top"],
              prime=["--print-cmd", "--", "htop"], note="trailing command words come from the current argv"))
    keep(warm("v2-ws-10-cache-cmd-printf", "WARM-HIT-SAME", base, ["bin/foot"], PC, prime=PC,
              after={"cache_lines": {"2": "printf"}},
              note="line 2 changed to a builtin that resolves: hit, command output unchanged (explain cmd= differs)"))
    keep(warm("v2-ws-11-cats-key-dup", "WARM-HIT-SAME", base, ["bin/foot"], PC, prime=PC,
              after={"files": {APP + "/foot.desktop": sub(entry(), "Type=Application\nName=Terminal",
                                                          "Type=Application\nName=Terminax")}},
              note="Name-like key edit that does not affect the command"))
    keep(warm("v2-ws-12-print-cmd-delim", "WARM-HIT-SAME", base, ["bin/foot"], ["--print-cmd=,"],
              prime=["--print-cmd=,"], note="print delimiter is not part of the cache"))
    keep(warm("v2-ws-13-hold-added-later", "WARM-HIT-SAME",
              {**LISTF("foot.desktop\n"), **F(extra="TerminalArgHold=--hold\n")},
              ["bin/foot"], ["--print-cmd", "--hold"], prime=["--print-cmd"],
              note="--hold at score time only: cached hold arg name used by both"))
    keep(warm("v2-ws-14-id-only-name", "WARM-HIT-SAME", base, ["bin/foot"], ["--print-id"], prime=["--print-cmd"],
              after={"files": {APP + "/foot.desktop": sub(entry(), "Name=Terminal", "Name=Terminax")}},
              note="--print-id only: id unchanged"))

    # default cache directory ($HOME/.cache) and XTE_CACHE_ENABLED truth forms
    keep(case("v2-wd-38-default-cache-absent", "CACHE-DEFAULT", dict(base), ["bin/foot"], PC,
              cache_home="home",
              note="XDG_CACHE_HOME unset, $HOME/.cache empty: no cache data (clause i makes $HOME read-only, so a "
                   "prime to the default path cannot be observed here - see the report)"))
    keep(warm("v2-ws-15-cache-enabled-true", "WARM-HIT-SAME", base, ["bin/foot"], PC, prime=PC,
              after={"env": {"XTE_CACHE_ENABLED": "true"}}, note="truthy env form still reads the cache"))
    keep(warm("v2-ws-16-cache-enabled-one", "WARM-HIT-SAME", base, ["bin/foot"], PC, prime=PC,
              after={"env": {"XTE_CACHE_ENABLED": "1"}}, note="truthy env form 1"))
    keep(warm("v2-ws-17-cached-cmd-gate", "WARM-HIT-SAME", base, ["bin/foot"], PC, prime=PC,
              after={"cache_lines": {"2": "ls"}},
              note="cached cmd is only a gate: 'ls' resolves, the command printed still comes from line 11"))
    keep(warm("v2-ws-18-env-nonexistent-dir", "WARM-HIT-SAME", base, ["bin/foot"], PC, prime=PC,
              after={"env": {"XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share"}},
              note="an env change that only adds a NONEXISTENT data dir does not move the hash: still a hit"))
    # ============================== WARM-INVALID ==============================
    def inv(cid, note, after, *, files=None, execs=("bin/foot",), args=PC, prime=PC, exec_add=None):
        f = dict(files or base)
        a = dict(after or {})
        if exec_add:
            a["exec_add"] = list(a.get("exec_add") or []) + list(exec_add)
        keep(warm(cid, "WARM-INVALID", f, list(execs), list(args), prime=prime, after=a, note=note))

    inv("v2-wi-01-entry-mtime", "entry mtime moved by a day (an old date shows only the day in ls -l)",
        {"files": {}, "mtime": MT + 86400})
    inv("v2-wi-02-entry-size", "entry size changed by one byte",
        {"files": {APP + "/foot.desktop": entry() + "#"}})
    inv("v2-wi-03-entry-rename", "entry renamed (same dir, same bytes) -> listing name changed",
        {"files": {APP + "/foot.desktop": None, APP + "/fooot.desktop": entry()}})
    inv("v2-wi-04-entry-deleted", "entry deleted: deletion changes the directory listing (proves invalid)",
        {"files": {APP + "/foot.desktop": None}})
    inv("v2-wi-05-entry-added", "second entry added: directory listing changes",
        {"files": {APP + "/extra.desktop": entry("extra --x")}}, exec_add=["bin/extra"])
    inv("v2-wi-06-list-mtime", "list file mtime moved by a day", {"files": {}, "mtime": MT + 86400})
    inv("v2-wi-07-list-size", "list file size changed", {"files": {LIST: "foot.desktop\n\n"}})
    inv("v2-wi-08-list-created", "a list path that did not exist is created (it is a hash operand)",
        {"files": {GLOBAL_LIST: "foot.desktop\n"}})
    inv("v2-wi-09-list-deleted", "existing list file deleted", {"files": {LIST: None}})
    inv("v2-wi-10-subdir-added", "subdirectory added inside an applications dir",
        {"files": {APP + "/sub.desktop/": ""}})
    inv("v2-wi-11-subdir-mtime", "existing subdirectory mtime moved by a day",
        {"mtime": MT + 86400}, files={**base, APP + "/sub.desktop/": ""})
    inv("v2-wi-12-desktop-env", "XDG_CURRENT_DESKTOP changed after priming",
        {"env": {"XDG_CURRENT_DESKTOP": "GNOME"}})
    inv("v2-wi-13-desktop-env-case", "XDG_CURRENT_DESKTOP case changed",
        {"env": {"XDG_CURRENT_DESKTOP": "hyprland"}})
    inv("v2-wi-14-data-dirs", "XDG_DATA_DIRS gains an EXISTING applications dir -> listing changes",
        {"env": {"XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share"}},
        files={**base, "usr/local/share/applications/kitty.desktop": entry("kitty --a")})
    inv("v2-wi-15-data-home", "XDG_DATA_HOME changed",
        {"env": {"XDG_DATA_HOME": "$ROOT/home/.local/share2"}})
    inv("v2-wi-16-config-home", "XDG_CONFIG_HOME changed",
        {"env": {"XDG_CONFIG_HOME": "$ROOT/home/.config2"}})
    inv("v2-wi-17-exec-stub-gone", "exec[0] stub unlinked -> command -v fails -> out-of-date",
        {"exec_remove": ["bin/foot"]})
    inv("v2-wi-18-cache-disabled-env", "XTE_CACHE_ENABLED=0 after priming",
        {"env": {"XTE_CACHE_ENABLED": "0"}})
    inv("v2-wi-19-cache-disabled-no", "XTE_CACHE_ENABLED=no after priming",
        {"env": {"XTE_CACHE_ENABLED": "no"}})
    inv("v2-wi-20-cache-disabled-garbage", "XTE_CACHE_ENABLED=banana (check_bool error -> no)",
        {"env": {"XTE_CACHE_ENABLED": "banana"}})
    inv("v2-wi-21-mode-change", "entry mode changed (ls -l column)",
        {"modes": {APP + "/foot.desktop": 0o751}})
    inv("v2-wi-22-apps-dir-renamed", "applications dir renamed",
        {"files": {APP + "/": None, "home/.local/share/applications2/": "",
                   "home/.local/share/applications2/foot.desktop": entry()}},
        files={**base})
    inv("v2-wi-23-entry-big", "entry grew: size and mtime both move",
        {"files": {APP + "/foot.desktop": entry() + "[Desktop Action q]\nExec=foot --q\n"}})
    inv("v2-wi-24-list-is-dir", "the list operand became a directory",
        {"files": {LIST: None, LIST + "/": ""}},
        files={**base})
    inv("v2-wi-25-dir-entry-became-dir", "entry path became a directory (also a listing change)",
        {"files": {APP + "/foot.desktop": None, APP + "/foot.desktop/": ""}})
    inv("v2-wi-26-cache-line1-wrong", "line 1 replaced with a well-formed wrong hash",
        {"cache_lines": {"1": "00000000000000000000000000000000"}})
    inv("v2-wi-27-cache-line1-nonhex", "line 1 non-hex of the right length",
        {"cache_lines": {"1": "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"}})
    inv("v2-wi-28-cache-line1-empty", "line 1 emptied",
        {"cache_lines": {"1": ""}})
    inv("v2-wi-29-cache-line2-empty", "line 2 emptied -> command -v '' fails",
        {"cache_lines": {"2": ""}})
    inv("v2-wi-30-cache-line2-gone", "line 2 set to a name that does not exist",
        {"cache_lines": {"2": "nosuchcmd"}})
    inv("v2-wi-31-cache-crlf", "cache rewritten with CRLF line endings",
        {"cache_sub": [["\n", "\r\n"]]})
    inv("v2-wi-32-cache-hash-case", "line 1 upper-cased hex: string compare, not numeric",
        {"cache_lines": {"1": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"}})
    inv("v2-wi-34-exec-args-change", "cold answer differs, cache invalid because ExecArg line grew",
        {"files": {APP + "/foot.desktop": subn(entry(), "TerminalArgExec=-e", "TerminalArgExec=-e -x")}})
    inv("v2-wi-35-symlink-like", "a second list path (XDG_CONFIG_DIRS) appears",
        {"files": {"cd/xdg-terminals.list": "foot.desktop\n"}})

    # ============================== MALFORMED ==============================
    # parse-shape cases: the cache is literal and its hash cannot match, which is enough because read_cache
    # decides "invalid cache data" BEFORE it calls gen_hash; the shape alone is what is being tested.
    H = "0" * 32
    BODY = "\n".join([H, "foot", "$ROOT/" + APP + "/./foot.desktop", "foot.desktop", "", "-e", "", "", "", ""])
    END = "\x1eEND_OF_EXEC_USEP"
    mal = lambda cid, note, text, args=None, files=None, execs=("bin/foot",): keep(case(
        cid, "MALFORMED", dict(files or base), list(execs), args or PC, cache=text, note=note))
    mal("v2-mf-01-no-terminator", "line 11 without the terminator -> invalid cache data",
        BODY + "\nfoot\x1f--a\n")
    mal("v2-mf-02-terminator-line-10", "terminator on line 10 is not parsed (only line 11+ counts) -> invalid",
        "\n".join([H, "foot", "$ROOT/x", "foot.desktop", "", "-e", "", "", "", END]) + "\n")
    mal("v2-mf-03-terminator-line-11", "terminator on line 11 is the minimal accepted cache; hash is wrong -> stale",
        BODY + "\n" + END + "\n")
    mal("v2-mf-04-terminator-line-12", "command begins on line 11 and terminates on line 12",
        BODY + "\nfoot\n" + END + "\n")
    mal("v2-mf-05-empty-file", "zero-byte cache -> invalid cache data", "")
    mal("v2-mf-06-empty-hash", "empty hash line -> out-of-date",
        "\n".join(["", "foot", "$ROOT/x", "foot.desktop", "", "-e", "", "", "", "", END]) + "\n")
    mal("v2-mf-07-hash-short", "31 hex chars -> out-of-date", BODY.replace(H, H[:31]) + "\n" + END + "\n")
    mal("v2-mf-08-hash-long", "33 hex chars -> out-of-date", BODY.replace(H, H + "0") + "\n" + END + "\n")
    mal("v2-mf-09-fields-short", "only five fields then a bare terminator line 6 -> invalid",
        "\n".join([H, "foot", "$ROOT/x", "foot.desktop", "", END]) + "\n")
    mal("v2-mf-10-50-lines", "49 junk lines and no terminator; line 50 hits the limit -> invalid",
        BODY + "\n" + "\n".join(["j"] * 39) + "\n")
    mal("v2-mf-11-51-lines", "line 50 reached before any terminator -> invalid regardless of line 51",
        BODY + "\n" + "\n".join(["j"] * 40) + "\n" + END + "\n")
    mal("v2-mf-12-no-final-newline", "terminator line without a trailing newline never enters the read loop -> invalid",
        BODY + "\n" + END)
    mal("v2-mf-13-blank-lines", "11 blank lines -> hash empty -> out-of-date",
        "\n" * 11 + "\n", args=["--print-id"])
    mal("v2-mf-14-tabs", "fields separated by tabs instead of empty lines",
        "\n".join([H, "foot", "$ROOT/x", "foot.desktop", "", "-e\t", "", "", "", "", END]) + "\n")
    mal("v2-mf-15-very-long-line", "4 KiB command line is parsed; hash wrong -> stale",
        BODY + "\n" + "x" * 4096 + END + "\n")
    keep(case("v2-mf-17-no-cache-path", "MALFORMED",
              {**base, ".rw/cache/xdg-terminal-exec/": ""}, ["bin/foot"], PC,
              note="cache path holds a directory: [ -f ] fails -> no cache data"))
    mal("v2-mf-18-exec-empty-11", "line 11 is the bare terminator with a wrong hash -> stale, cold answer",
        BODY + "\n" + END + "\n", args=["--print-cmd", "--", "htop"])
    # accepted malformed caches, built by editing the PRIMED cache (hash stays right)
    keep(warm("v2-mf-19-junk-before-term", "MALFORMED", base, ["bin/foot"], PC, prime=PC,
              after={"cache_lines": {"11": "JUNK" + END}},
              note="accepted: junk before the terminator becomes part of the command"))
    keep(warm("v2-mf-20-junk-after-term", "MALFORMED", base, ["bin/foot"], PC, prime=PC,
              after={"cache_lines": {"11": END + "xx"}},
              note="rejected: bytes after the terminator mean no terminator is ever seen"))
    keep(warm("v2-mf-22-lying-path", "MALFORMED", base, ["bin/foot"], ["--print-path"], prime=["--print-cmd"],
              after={"cache_lines": {"3": "$ROOT/nope.desktop"}},
              note="accepted: --print-path prints the cached (nonexistent) path"))
    keep(warm("v2-mf-23-empty-id", "MALFORMED", base, ["bin/foot"], ["--print-id"], prime=["--print-cmd"],
              after={"cache_lines": {"4": ""}},
              note="accepted: --print-id prints nothing"))
    keep(warm("v2-mf-24-cached-action-id", "MALFORMED", base, ["bin/foot"], ["--print-id"], prime=["--print-cmd"],
              after={"cache_lines": {"5": "new"}},
              note="accepted: cached action appended to the printed id"))
    keep(warm("v2-mf-25-cached-execarg-crlf", "MALFORMED", base, ["bin/foot"], ["--print-cmd", "--", "htop"],
              prime=["--print-cmd", "--", "htop"], after={"cache_sub": [["\n", "\r\n"]]},
              note="CRLF cache: hash line carries \\r -> out-of-date"))
    keep(warm("v2-mf-26-cache-append-after-term", "MALFORMED", base, ["bin/foot"], PC, prime=PC,
              after={"cache_append": [END, "tail"]},
              note="lines after the terminator are never read"))
    keep(warm("v2-mf-27-two-terminators", "MALFORMED", base, ["bin/foot"], PC, prime=PC,
              after={"cache_append": ["foot\x1f--b" + END]},
              note="first terminator wins; appended second command ignored"))
    keep(warm("v2-mf-28-crlf-accepted", "MALFORMED", {**LISTF("foot.desktop\n"), **F()}, ["bin/foot"],
              ["--print-cmd", "--", "htop"], prime=["--print-cmd", "--", "htop"],
              after={"cache_lines": {"6": "-e\r"}},
              note="trailing CR on the execarg line becomes part of the arg"))
    keep(warm("v2-mf-29-line2-option", "MALFORMED", base, ["bin/foot"], PC, prime=PC,
              after={"cache_lines": {"2": "-p"}},
              note="cached cmd '-p': command -v parses it as its own option and exits 0 -> hit"))
    keep(warm("v2-mf-30-accepted-empty-cmd", "MALFORMED", base, ["bin/foot"], ["--print-cmd", "--", "htop"],
              prime=["--print-cmd", "--", "htop"], after={"cache_lines": {"11": END}},
              note="accepted: line 11 is the bare terminator, so the cached command is empty; only argv words print"))

    # ============================== HOME-UNSET ==============================
    # The pin runs under `set -euf` and expands ${HOME} only inside ${X:-default} forms, but bash expands the
    # default word only when the XDG var is unset. So with HOME unset: XDG_CONFIG_HOME, XDG_DATA_HOME and
    # XDG_CACHE_HOME must each be set, or the script dies with "<name>: unbound variable" (empty stdout, rc 1)
    # before it ever looks at the cache. That is the exact shape of the round-47 D1 closure.
    def home_case(cid, note, *, unset_xdg=(), files=None, execs=("bin/foot",), args=PC,
                  prime=None, after=None, env_extra=None):
        c = case(cid, "HOME-UNSET", dict(files or base), list(execs), list(args),
                 env_extra=env_extra, note=note, unset=["HOME"] + list(unset_xdg))
        if prime:
            c["meta"] = {"probe": "prime", "note": note}
            c["prime"] = {"args": list(prime)}
            c["mtime"] = MT
            a = dict(after or {})
            a.setdefault("mtime", MT)
            c["after"] = a
        keep(c)

    home_case("v2-hu-01-home-unset-xdg-set",
              "HOME unset, the three XDG defaults set: resolves normally")
    home_case("v2-hu-02-home-unset-config-unset",
              "HOME unset and XDG_CONFIG_HOME unset: dies at the config default (unbound variable), rc 1",
              unset_xdg=["XDG_CONFIG_HOME"])
    home_case("v2-hu-03-home-unset-data-unset",
              "HOME unset and XDG_DATA_HOME unset: dies at the data default, rc 1",
              unset_xdg=["XDG_DATA_HOME"])
    home_case("v2-hu-04-home-unset-cache-unset",
              "HOME unset and XDG_CACHE_HOME unset: dies at the cache default, rc 1 (round-47 D1)",
              unset_xdg=["XDG_CACHE_HOME"])
    home_case("v2-hu-05-home-unset-all-xdg",
              "HOME unset and every XDG dir unset: first unbound expansion (config) kills the run",
              unset_xdg=["XDG_CONFIG_HOME", "XDG_CONFIG_DIRS", "XDG_DATA_HOME", "XDG_DATA_DIRS",
                         "XDG_CACHE_HOME"])
    home_case("v2-hu-06-home-unset-data-dirs",
              "HOME unset, entry only reachable through XDG_DATA_DIRS (XDG_DATA_HOME set, empty)",
              env_extra={"XDG_DATA_HOME": "$ROOT/home/.local/share/empty"},
              files={LIST: "foot.desktop\n", USR_APP + "/foot.desktop": entry()})
    home_case("v2-hu-07-home-unset-warm",
              "HOME unset with a primed cache: warm hit still answers",
              prime=PC)
    home_case("v2-hu-08-home-unset-warm-differs",
              "HOME unset, primed cache, same-size Exec edit: warm != cold",
              prime=PC, after={"files": {APP + "/foot.desktop": sub(entry(), "Exec=foot --a", "Exec=feot --a")}},
              execs=("bin/foot", "bin/feot"))
    home_case("v2-hu-09-home-unset-print-id",
              "HOME unset, --print-id only", args=["--print-id"])
    home_case("v2-hu-10-home-unset-data-dirs-unset",
              "HOME unset, XDG_DATA_DIRS unset: default data dirs are empty in the sandbox, XDG_DATA_HOME wins",
              unset_xdg=["XDG_DATA_DIRS"])

    # ============================== READDIR ==============================
    # two valid candidates in ONE applications dir: the fallback order (and so the winner) is the directory's
    # readdir order, last entry first, because find emits readdir order and each id is prepended. meta.files_order
    # pins the creation order the observed order was measured with; meta.readdir_order records the observation.
    def rd(cid, names, note, *, files_extra=None, args=("--print-id",), datadir=APP):
        files = {}
        order = []
        for n in names:
            p = "%s/%s.desktop" % (datadir, n)
            files[p] = entry("%s --a" % n)
            order.append(p)
        if files_extra:
            for k, v in files_extra.items():
                files[k] = v
                order.append(k)
        c = case(cid, "READDIR", files, ["bin/" + n for n in names], list(args),
                 env_extra={"XDG_CONFIG_DIRS": "$ROOT/nonexist"},
                 note=note, files_order=order)
        keep(c)

    rd("v2-rd-01-foot-kitty", ("foot", "kitty"), "one dir, no list: find order decides")
    rd("v2-rd-02-alacritty-foot", ("alacritty", "foot"), "second pair")
    rd("v2-rd-03-aaaa-zzzz", ("aaaa", "zzzz"), "alphabetical vs readdir: same here, recorded")
    rd("v2-rd-04-ghostty-konsole", ("ghostty", "konsole"), "third pair")
    rd("v2-rd-05-three", ("foot", "kitty", "aaaa"), "three candidates, last in readdir order wins")
    rd("v2-rd-06-reverse-create", ("konsole", "ghostty"), "creation order reversed vs v2-rd-04")
    rd("v2-rd-07-with-subdir", ("foot", "zzzz"), "a subdirectory in the same dir is also walked by find",
       files_extra={APP + "/sub.desktop/": ""})
    rd("v2-rd-08-usr-share", ("foot", "kitty"), "two candidates in the usr/share dir (first find operand)",
       datadir=USR_APP, files_extra=None)
    keep(case("v2-rd-09-two-dirs-both", "READDIR",
              {USR_APP + "/foot.desktop": entry("foot --usr"), APP + "/foot.desktop": entry("foot --home")},
              ["bin/foot"], ["--print-path", "--print-cmd"],
              env_extra={"XDG_CONFIG_DIRS": "$ROOT/nonexist"},
              note="duplicate id across dirs: the higher-preference operand overwrites the alias",
              files_order=[USR_APP + "/foot.desktop", APP + "/foot.desktop"]))
    keep(case("v2-rd-10-subdir-ids", "READDIR",
              {APP + "/a.desktop/b.desktop": entry("foot --nested")}, ["bin/foot"],
              ["--print-id", "--print-path", "--print-cmd"],
              env_extra={"XDG_CONFIG_DIRS": "$ROOT/nonexist"},
              note="nested .desktop is registered as a-b id"))

    # ============================== H1 ==============================
    # find -L <d1>/. <d2>/. ... -type f ( -path d1p ) -o ( -path d2p ) ... : implicit -a binds tighter than -o, so
    # only the FIRST (lowest-preference) applications dir is filtered by -type f. A non-regular path named
    # *.desktop in any other dir overwrites the alias of the valid file.
    H1ENV = {"XDG_DATA_DIRS": "$ROOT/usr/share"}
    def h1(cid, note, files, execs=("bin/foot",), args=("--print-id", "--print-path", "--print-cmd")):
        keep(case(cid, "H1", files, list(execs), list(args), env_extra=H1ENV, note=note))

    h1("v2-h1-01-dir-shadow", "directory foot.desktop in home shadows the valid file in usr/share",
       {USR_APP + "/foot.desktop": entry(), APP + "/foot.desktop/": ""})
    h1("v2-h1-02-dir-shadow-print-id", "same, --print-id only: rc 1, empty stdout",
       {USR_APP + "/foot.desktop": entry(), APP + "/foot.desktop/": ""}, args=["--print-id"])
    h1("v2-h1-03-dir-shadow-empty", "empty shadow directory: find still matches the directory path",
       {USR_APP + "/foot.desktop": entry(), APP + "/foot.desktop/": ""})
    h1("v2-h1-04-dir-shadow-with-file", "shadow directory has a file inside: the alias points at the directory",
       {USR_APP + "/foot.desktop": entry(), APP + "/foot.desktop/x": "not an entry\n"})
    h1("v2-h1-05-dir-shadow-nested-entry", "nested entry gets its own id and wins the fallback order",
       {USR_APP + "/foot.desktop": entry(), APP + "/foot.desktop/nested.desktop": entry("foot --n")})
    h1("v2-h1-06-first-dir-exempt", "a directory in the FIRST dir is filtered by -type f: the valid home file wins",
       {APP + "/foot.desktop": entry(), USR_APP + "/foot.desktop/": ""})
    keep(case("v2-h1-07-dir-shadow-second", "H1",
              {USR_APP + "/foot.desktop": entry(), "usr/local/share/applications/foot.desktop/": ""},
              ["bin/foot"], ["--print-id", "--print-path", "--print-cmd"],
              env_extra={"XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share"},
              note="shadow in the middle dir (usr/local/share); only the first operand gets -type f"))
    h1("v2-h1-08-dir-shadow-list-second", "list names the shadowed id then a valid one",
       {USR_APP + "/foot.desktop": entry(), APP + "/foot.desktop/": "", APP + "/kitty.desktop": entry("kitty --a"),
        LIST: "foot.desktop\nkitty.desktop\n"}, execs=("bin/foot", "bin/kitty"))
    h1("v2-h1-09-dir-shadow-nested-only", "the shadow directory's nested entry is selected (id has a dash)",
       {APP + "/foot.desktop/a.desktop": entry("foot --n")}, execs=("bin/foot",))
    h1("v2-h1-10-dir-shadow-other-id", "shadow dir for an unrelated id does not disturb the valid entry",
       {USR_APP + "/foot.desktop": entry(), APP + "/zzz.desktop/": ""})
    keep(case("v2-h1-11-dir-shadow-warm-invalid", "H1",
              {USR_APP + "/foot.desktop": entry(), APP + "/foot.desktop/": ""}, ["bin/foot"],
              PC, env_extra=H1ENV,
              note="shadow dir present at prime: prime itself fails, so no cache exists -> cold answer"))
    keep(case("v2-h1-12-first-dir-file-and-shadow", "H1",
              {USR_APP + "/foot.desktop": entry(), USR_APP + "/kitty.desktop": entry("kitty --a"),
               APP + "/foot.desktop/": "", LIST: "kitty.desktop\nfoot.desktop\n"},
              ["bin/foot", "bin/kitty"], ["--print-id", "--print-path"], env_extra=H1ENV,
              note="list order means kitty is tried first; the shadowed foot is never read"))

    # ============================== H2 ==============================
    # `command -v "$name"` parses an option-like operand as its own option: a valid cluster leaves no operand and
    # exits 0, so Exec/TryExec values starting with '-' can be accepted.
    def h2(cid, note, exec_=None, tryexec=None, args=("--print-id", "--print-cmd"), execs=()):
        extra = ("TryExec=%s\n" % tryexec) if tryexec else ""
        e = entry(exec_ or "foot --a", extra=extra)
        keep(case(cid, "H2", {**LISTF("foot.desktop\n"), APP + "/foot.desktop": e}, list(execs), list(args),
                  note=note))

    h2("v2-h2-01-exec-p", "Exec[0]=-p: command -v -p exits 0", exec_="-p")
    h2("v2-h2-02-exec-pv", "Exec[0]=-pv", exec_="-pv")
    h2("v2-h2-03-exec-dashdash", "Exec[0]=--", exec_="--")
    h2("v2-h2-04-exec-v-space", "Exec=-v x: first word -v", exec_="-v x")
    h2("v2-h2-05-exec-pV", "Exec[0]=-pV", exec_="-pV")
    h2("v2-h2-06-tryexec-pv", "TryExec=-pv with a normal Exec", tryexec="-pv", execs=("bin/foot",))
    h2("v2-h2-07-tryexec-v", "TryExec=-v", tryexec="-v", execs=("bin/foot",))
    h2("v2-h2-08-exec-q-rejected", "control: --print-cmd with an option-like cluster that is not valid",
       exec_="-q")
    h2("v2-h2-09-exec-dash-rejected", "control: Exec[0]=- is neither an option cluster nor a command",
       exec_="-")
    h2("v2-h2-10-tryexec-badopt", "control: TryExec=--foo exits 2", tryexec="--foo", execs=("bin/foot",))
    h2("v2-h2-11-exec-p-with-list-cmd", "Exec=-p with trailing argv words",
       exec_="-p", args=["--print-cmd", "--", "htop"])
    # warm H2: cached cmd is the option-like word; command -v keeps exiting 0
    keep(warm("v2-h2-12-cached-option-cmd", "H2",
              {**LISTF("foot.desktop\n"), APP + "/foot.desktop": entry("-p")}, [], PC, prime=PC,
              after={"files": {APP + "/foot.desktop": sub(entry("-p"), "Exec=-p", "Exec=-q")}},
              note="cached cmd '-p' resolves; cold rejects '-q' -> warm hit differs"))
    keep(warm("v2-h2-13-cached-option-dashdash", "H2",
              {**LISTF("foot.desktop\n"), APP + "/foot.desktop": entry("-- x")}, [], PC, prime=PC,
              after={"files": {APP + "/foot.desktop": sub(entry("-- x"), "Exec=-- x", "Exec=-q x")}},
              note="cached cmd '--' resolves; cold rejects '-q'"))
    return out


# ------------------------------------------------------------------------------------------------ resolve
def fs_type(path):
    try:
        p = subprocess.run(["stat", "-f", "-c", "%T", path], capture_output=True)
        return p.stdout.decode().strip()
    except OSError:
        return "?"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--out")
    ap.add_argument("--receipt")
    ap.add_argument("--only", default=None)
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--verify", default=None,
                    help="re-resolve an existing fixtures file and compare every expect/cold; writes nothing")
    args = ap.parse_args()

    if not args.work.startswith("/fast/"):
        raise SystemExit("--work must live under /fast (scratch directive)")
    os.makedirs(args.work, exist_ok=True)
    box = Box(args.work)
    if args.verify:
        cases = json.load(open(args.verify))
        bad = 0
        for n, c in enumerate(cases, 1):
            base = os.path.join(args.work, "vf", c["id"])
            shutil.rmtree(base, ignore_errors=True)
            res = []
            for t in range(args.trials):
                rc, out, err, order = run_trial(box, c, os.path.join(base, "t%d/r" % t), cached=True)
                res.append((rc, out, order))
            got = {(r[0], r[1]) for r in res}
            orders_ok = all(r[2] == res[0][2] for r in res)
            e = c.get("expect")
            ok = got == {(e["rc"], e["stdout"])} and orders_ok
            if c.get("prime") or c.get("cache") is not None:
                crc, cout, _ = run_cold(box, c, os.path.join(base, "cold/r"))
                if (crc, cout) != (c.get("cold") or {}).get("rc", None) and True:
                    if c.get("cold") is not None and (crc, cout) != (c["cold"]["rc"], c["cold"]["stdout"]):
                        ok = False
                        print("COLD-DRIFT", c["id"], (crc, cout[:80]), c["cold"])
            if not ok:
                bad += 1
                print("DRIFT", c["id"], got, e)
            shutil.rmtree(base, ignore_errors=True)
            if n % 40 == 0:
                print("verified %d/%d" % (n, len(cases)), file=sys.stderr)
        print("VERIFY: %d/%d agree, trials=%d" % (len(cases) - bad, len(cases), args.trials))
        raise SystemExit(0 if bad == 0 else 1)
    cases = build(args.only)
    if len(cases) < 120 and not args.only:
        raise SystemExit("only %d cases built" % len(cases))
    ids = set()
    for c in cases:
        if c["id"] in ids:
            raise SystemExit("duplicate id %s" % c["id"])
        ids.add(c["id"])

    started = time.time()
    dropped, kept = [], []
    per_class = {}
    differ = {}
    states = {}
    for n, c in enumerate(cases, 1):
        base = os.path.join(args.work, "fx", c["id"])
        shutil.rmtree(base, ignore_errors=True)
        try:
            results = []
            orders = []
            stderr0 = ""
            for t in range(args.trials):
                root = os.path.join(base, "t%d/r" % t)
                rc, out, err, order = run_trial(box, c, root, cached=True)
                results.append((rc, out))
                orders.append(order)
                if t == 0:
                    stderr0 = err
            if len(set(results)) != 1:
                raise Bad("trials disagree: %r" % (results,))
            if any(o != orders[0] for o in orders):
                raise Bad("readdir order unstable across trials: %r" % (orders,))
            rc, out = results[0]
            c["expect"] = {"rc": rc, "stdout": out}
            # cold answer on the same tree, no cache (only meaningful for primed / pre-seeded cases)
            if c.get("prime") or c.get("cache") is not None:
                croot = os.path.join(base, "cold/r")
                crc, cout, _ = run_cold(box, c, croot)
                c["cold"] = {"rc": crc, "stdout": cout}
                c["meta"]["warm_differs_from_cold"] = (crc, cout) != (rc, out)
            else:
                c["cold"] = None
                c["meta"]["warm_differs_from_cold"] = False
            c["meta"]["cache_state"] = cache_state_from(stderr0)
            c["meta"]["fs"] = fs_type(os.path.join(base, "t0/r"))
            c["meta"]["readdir_order"] = orders[0] if c["class"] == "READDIR" or c["class"] == "H1" else {
                k: v for k, v in orders[0].items() if k.endswith("applications")}
            per_class[c["class"]] = per_class.get(c["class"], 0) + 1
            if c["meta"]["warm_differs_from_cold"]:
                differ[c["class"]] = differ.get(c["class"], 0) + 1
            states[c["meta"]["cache_state"]] = states.get(c["meta"]["cache_state"], 0) + 1
            kept.append(c)
        except Bad as e:
            dropped.append({"id": c["id"], "class": c["class"], "why": str(e)})
        shutil.rmtree(base, ignore_errors=True)
        if n % 20 == 0:
            print("resolved %d/%d (kept %d, dropped %d) %.1fs" % (n, len(cases), len(kept), len(dropped),
                                                                  time.time() - started), file=sys.stderr)
    if dropped:
        print("DROPPED:", json.dumps(dropped, indent=1)[:4000], file=sys.stderr)
    if len(kept) < 120 and not args.only:
        raise SystemExit("only %d cases survived" % len(kept))

    if not args.out or not args.receipt:
        raise SystemExit("--out and --receipt are required unless --verify")
    with open(args.out, "w") as fh:
        json.dump(kept, fh, indent=1, sort_keys=True)
        fh.write("\n")
    sha = hashlib.sha256(open(args.out, "rb").read()).hexdigest()
    receipt = {
        "set": os.path.basename(args.out),
        "sha256": sha,
        "cases": len(kept),
        "dropped": dropped,
        "classes": per_class,
        "warm_differs_from_cold": differ,
        "cache_states": states,
        "trials": args.trials,
        "pin_sha256": PIN_SHA256,
        "pin": PIN,
        "seed_mtime": MT,
        "work": args.work,
        "fs": fs_type(args.work),
        "seconds": round(time.time() - started, 1),
        "python": sys.version.split()[0],
        "sandbox": "bwrap argv from quality/counters/c1-r47-terminal.py Box.argv; prime wrapped (prime-wrap.sh)",
    }
    with open(args.receipt, "w") as fh:
        json.dump(receipt, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(receipt, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
