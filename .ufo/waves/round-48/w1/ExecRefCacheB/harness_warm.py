#!/usr/bin/env python3
"""Warm-cache fixtures: the patched tool against the REAL pinned resolver, in the counter-shaped sandbox.

  /usr/bin/python3 /mod/harness_warm.py <workdir>

Per fixture the case is materialized TWICE (o/r for the oracle, t/r for the tool, identical bytes written in
the same order), the tree is pinned to one mtime, and BOTH trees are primed by the real pin (a cold
`--print-cmd`, then the wrapper lets the background save_cache land). The fixture's `after` mutations are
applied to both trees, then
  oracle: /oracle/xdg-terminal-exec <args>
  tool:   /usr/bin/python3 -I /oracle/tool.py print <args>
must agree on exit status and on stdout with the root rewritten to $ROOT. The tool's tree is walked before
and after its run and must be unchanged (the tool writes nothing).

The expected value is never typed here: it is the oracle's own output at run time.
"""
import hashlib
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import warmcache  # noqa: E402

PIN = "/oracle/xdg-terminal-exec"
TOOL = "/oracle/tool.py"
WRAP = "/xbin/wrapped-pin"
USEP = warmcache.USEP

FOOT = "[Desktop Entry]\nType=Application\nName=Foot\nExec=foot\nCategories=System;TerminalEmulator;\n"


def base_files(entry=FOOT, lst="foot.desktop\n"):
    return {"usr/share/applications/foot.desktop": entry, "home/.config/xdg-terminals.list": lst}


def case_env(root, extra=None):
    e = {
        "HOME": os.path.join(root, "home"),
        "XDG_CONFIG_HOME": os.path.join(root, "home/.config"),
        "XDG_CONFIG_DIRS": os.path.join(root, "etc/xdg"),
        "XDG_DATA_HOME": os.path.join(root, "home/.local/share"),
        "XDG_DATA_DIRS": os.path.join(root, "usr/share"),
        "XDG_CACHE_HOME": os.path.join(root, ".rw/cache"),
        "XDG_CURRENT_DESKTOP": "Hyprland",
        "PATH": os.path.join(root, "bin") + ":/oracle/bin",
        "LANG": "C.UTF-8",
    }
    for k, v in (extra or {}).items():
        if v is None:
            e.pop(k, None)
        else:
            e[k] = v.replace("$ROOT", root)
    return e


def materialize(root, case):
    for d in ("home/.config", "home/.local/share/applications", "usr/share/applications", "etc/xdg",
              "bin", ".rw/cache"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    for rel, text in case.get("files", {}).items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(text.replace("$ROOT", root).encode("utf-8", "surrogateescape"))
    for rel in case.get("exec", []):
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)


def pin_mtimes(root, ts):
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        for nm in filenames + dirnames + ["."]:
            p = os.path.join(dirpath, nm)
            try:
                os.utime(p, (ts, ts), follow_symlinks=False)
            except OSError:
                pass


def apply_after(root, after):
    for rel, text in (after.get("files") or {}).items():
        p = os.path.join(root, rel)
        if text is None:
            if os.path.lexists(p):
                os.unlink(p)
            continue
        data = text.replace("$ROOT", root).encode("utf-8", "surrogateescape")
        old_size = os.stat(p).st_size if os.path.exists(p) else None
        old_times = (os.stat(p).st_atime, os.stat(p).st_mtime) if os.path.exists(p) else None
        with open(p, "wb") as fh:
            fh.write(data)
        if after.get("same_meta", True) and old_size is not None:
            if len(data) != old_size:
                raise SystemExit("after.files[%s]: same_meta needs equal size (%d != %d)"
                                 % (rel, len(data), old_size))
            os.utime(p, old_times)
    for rel in after.get("exec_remove", []):
        p = os.path.join(root, rel)
        if os.path.lexists(p):
            os.unlink(p)
    for rel in after.get("exec_add", []):
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)
    for rel, off in (after.get("touch") or {}).items():
        p = os.path.join(root, rel)
        ts = after.get("base_ts")
        os.utime(p, (ts + off, ts + off))
    if after.get("mtime") is not None:
        pin_mtimes(root, after["mtime"])


def prime(root, args):
    env = case_env(root)
    subprocess.run([WRAP] + args, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                   timeout=60)
    cache = os.path.join(root, ".rw/cache/xdg-terminal-exec")
    for _ in range(50):
        if os.path.exists(cache):
            break
        time.sleep(0.02)


def snapshot(root):
    h = hashlib.sha256()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for nm in sorted(filenames + dirnames):
            p = os.path.join(dirpath, nm)
            st = os.lstat(p)
            h.update(("%s %o %d %d\n" % (p[len(root):], st.st_mode, st.st_size, st.st_mtime_ns)).encode())
            if os.path.isfile(p) and not os.path.islink(p):
                try:
                    with open(p, "rb") as fh:
                        h.update(fh.read())
                except OSError:
                    h.update(b"<unreadable>")
    return h.hexdigest()


def run_oracle(root, args, envkw=None):
    p = subprocess.run([PIN] + args, env=case_env(root, envkw), stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=60)
    if p.returncode != 0:
        sys.stderr.write("  oracle-stderr: %r\n" % p.stderr.decode("utf-8", "surrogateescape")[-400:])
    return p.returncode, p.stdout.decode("utf-8", "surrogateescape")


def run_tool(root, args, envkw=None):
    before = snapshot(root)
    p = subprocess.run(["/usr/bin/python3", "-I", TOOL, "print"] + args, env=case_env(root, envkw),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    after = snapshot(root)
    return p.returncode, p.stdout.decode("utf-8", "surrogateescape"), (before == after), \
        p.stderr.decode("utf-8", "surrogateescape")


def run_case(work, case, ts):
    cid = case["id"]
    root_o = os.path.join(work, cid, "o", "r")
    root_t = os.path.join(work, cid, "t", "r")
    for r in (root_o, root_t):
        shutil.rmtree(os.path.dirname(r), ignore_errors=True)
        os.makedirs(r)
        materialize(r, case)
        pin_mtimes(r, ts)
        if case.get("prime"):
            prime(r, case["prime"])
        if case.get("cache"):
            text = case["cache"](case_env(r))
            with open(os.path.join(r, ".rw/cache/xdg-terminal-exec"), "wb") as fh:
                fh.write(text)
        if case.get("cache_after"):
            cp = os.path.join(r, ".rw/cache/xdg-terminal-exec")
            with open(cp, "rb") as fh:
                data = fh.read()
            with open(cp, "wb") as fh:
                fh.write(case["cache_after"](data))
        after = dict(case.get("after") or {})
        after.setdefault("base_ts", ts)
        apply_after(r, after)
    o_rc, o_out = run_oracle(root_o, case["args"], case.get("env_after"))
    t_rc, t_out, quiet, t_err = run_tool(root_t, case["args"], case.get("env_after"))
    o_norm = (o_rc, o_out.replace(root_o, "$ROOT"))
    t_norm = (t_rc, t_out.replace(root_t, "$ROOT"))
    ok = o_norm == t_norm and quiet
    return ok, o_norm, t_norm, quiet, t_err


def resolver_paths(env):
    """XTE__CONFIGS and XTE__APPLICATIONS_DIRS exactly as make_paths builds them (x:143-174)."""
    desk = [c if not "A" <= c <= "Z" else chr(ord(c) + 32) for c in env.get("XDG_CURRENT_DESKTOP", "")]
    desk = [d for d in "".join(desk).rstrip("\n").split(":")]
    cfg_dirs = [d.rstrip("/") if d.endswith("/") else d
                for d in (env.get("XDG_CONFIG_HOME") or env["HOME"] + "/.config").split(":") +
                (env.get("XDG_CONFIG_DIRS") or "/etc/xdg").split(":")]
    data_dirs = [d.rstrip("/") if d.endswith("/") else d
                 for d in (env.get("XDG_DATA_DIRS") or "/usr/local/share:/usr/share").split(":")]
    configs = []
    for d in cfg_dirs:
        for dk in desk:
            configs.append(d + "/" + dk + "-xdg-terminals.list")
        configs.append(d + "/xdg-terminals.list")
    for d in data_dirs:
        for dk in desk:
            configs.append(d + "/xdg-terminal-exec/" + dk + "-xdg-terminals.list")
        configs.append(d + "/xdg-terminal-exec/xdg-terminals.list")
    apps = ""
    for d in [env.get("XDG_DATA_HOME") or env["HOME"] + "/.local/share"] + data_dirs:
        d = d[:-1] if d.endswith("/") else d
        apps = d + "/applications/" + (":" + apps if apps else "")
    return ":".join(configs), apps


def literal_cache(env, **fields):
    """A cache whose hash is this tree's own (warmcache.gen_hash), with fields as save_cache writes them."""
    confs, apps = resolver_paths(env)
    rec = {"hash": warmcache.gen_hash(env.get("XDG_CURRENT_DESKTOP", ""), confs, apps),
           "cmd": "foot", "entry_path": os.path.join(env["XDG_DATA_DIRS"], "applications/foot.desktop"),
           "entry_id": "foot.desktop", "entry_action": "", "execarg": "-e", "appidarg": "",
           "titlearg": "", "dirarg": "", "holdarg": "", "exec_usep": "kitty" + USEP + "--warm"}
    rec.update(fields)
    lines = [rec[k] for k in ("hash", "cmd", "entry_path", "entry_id", "entry_action", "execarg",
                              "appidarg", "titlearg", "dirarg", "holdarg")]
    return ("".join(x + "\n" for x in lines) + rec["exec_usep"] + warmcache.RSEP +
            "END_OF_EXEC_USEP\n").encode("utf-8", "surrogateescape")


def fixtures():
    f = []
    entry_kitty = FOOT.replace("Exec=foot", "Exec=kitty --new")
    f.append(dict(id="cold-control", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"]))
    f.append(dict(id="warm-absent", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"]))
    f.append(dict(id="warm-hit-plain", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-id", "--print-path", "--print-cmd"], prime=["--print-cmd"]))
    # the warm answer differs from the cold one: the entry is rewritten with the same size and mtime
    f.append(dict(id="warm-hit-entry-edit-same-meta", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"], prime=["--print-cmd"],
                  after={"files": {"usr/share/applications/foot.desktop":
                                   entry_kitty.ljust(len(FOOT), "-")[:len(FOOT)]},
                         "same_meta": True}))
    # ... and the same edit with a *different second* inside the same minute: still invisible
    f.append(dict(id="warm-hit-entry-edit-other-second", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"], prime=["--print-cmd"],
                  after={"files": {"usr/share/applications/foot.desktop":
                                   entry_kitty.ljust(len(FOOT), "-")[:len(FOOT)]},
                         "same_meta": False,
                         "touch": {"usr/share/applications/foot.desktop": 30}}))
    # the list is rewritten to name another terminal, same size and mtime
    list_kitty = "kitt.desktop\n"
    assert len(list_kitty) == len("foot.desktop\n")
    f.append(dict(id="warm-hit-list-edit-same-meta",
                  files=dict(base_files(),
                             **{"usr/share/applications/kitt.desktop":
                                FOOT.replace("Exec=foot", "Exec=kitt").replace("Name=Foot", "Name=Kitt")}),
                  exec=["bin/foot", "bin/kitty", "bin/kitt"],
                  args=["--print-cmd"], prime=["--print-cmd"],
                  after={"files": {"home/.config/xdg-terminals.list": list_kitty}, "same_meta": True}))
    # a TryExec stub removed while exec[0] still resolves: a cold run rejects the entry, the cache does not
    f.append(dict(id="warm-hit-tryexec-stub-gone",
                  files={"usr/share/applications/foot.desktop": FOOT.replace(
                      "Categories=", "TryExec=footx\nCategories="),
                      "home/.config/xdg-terminals.list": "foot.desktop\n"},
                  exec=["bin/foot", "bin/kitty", "bin/footx"], args=["--print-id", "--print-cmd"],
                  prime=["--print-cmd"], after={"exec_remove": ["bin/footx"]}))
    # cached argument names applied over --title/--dir/--app-id/--hold
    f.append(dict(id="warm-hit-args-over-cached-names",
                  files={"usr/share/applications/foot.desktop": FOOT.replace(
                      "Categories=", "X-TerminalArgTitle=--title\nX-TerminalArgDir=--working-directory=\n"
                      "X-TerminalArgAppId=--app-id=\nX-TerminalArgHold=--hold\nCategories="),
                      "home/.config/xdg-terminals.list": "foot.desktop\n"},
                  exec=["bin/foot", "bin/kitty"], prime=["--print-cmd"],
                  args=["--print-cmd", "--title=T", "--dir=/d", "--app-id=A", "--hold"]))
    # hash invalidations
    f.append(dict(id="warm-stale-desktop", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"], prime=["--print-cmd"], env_after={"XDG_CURRENT_DESKTOP": "GNOME"}))
    f.append(dict(id="warm-stale-size", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"], prime=["--print-cmd"],
                  after={"files": {"usr/share/applications/foot.desktop":
                                   FOOT + "NoDisplay=true\n"}, "same_meta": False}))
    f.append(dict(id="warm-stale-name", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"], prime=["--print-cmd"],
                  after={"files": {"usr/share/applications/foop.desktop":
                                   FOOT}}))
    f.append(dict(id="warm-stale-exec-gone", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"], prime=["--print-cmd"], after={"exec_remove": ["bin/foot"]}))
    f.append(dict(id="warm-invalid-no-terminator", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"], prime=["--print-cmd"],
                  cache_after=lambda data: data.rsplit(warmcache.RSEP.encode(), 1)[0]))
    f.append(dict(id="warm-invalid-line50", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"], prime=["--print-cmd"],
                  cache_after=lambda data: data.replace(
                      warmcache.TERMINATOR + b"\n",
                      b"\n" * 39 + warmcache.TERMINATOR + b"\n")))
    f.append(dict(id="warm-env-disabled", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"], prime=["--print-cmd"], env_after={"XTE_CACHE_ENABLED": "false"}))
    f.append(dict(id="warm-env-disabled-empty", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"], prime=["--print-cmd"], env_after={"XTE_CACHE_ENABLED": ""}))
    # literal caches: a hit whose values no cold run would produce, a missing entry path, a line-50 cache
    f.append(dict(id="warm-literal-hit-values", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-id", "--print-path", "--print-cmd"],
                  cache=lambda env: literal_cache(env, entry_id="cached.desktop", entry_action="act")))
    f.append(dict(id="warm-literal-content", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-content"], cache=lambda env: literal_cache(env)))
    f.append(dict(id="warm-literal-content-missing-path", files=base_files(), exec=["bin/foot"],
                  args=["--print-id", "--print-content"],
                  cache=lambda env: literal_cache(env, entry_path="/nonexistent/entry.desktop")))
    f.append(dict(id="warm-literal-content-dir-path", files=base_files(), exec=["bin/foot"],
                  args=["--print-content"],
                  cache=lambda env: literal_cache(env, entry_path=os.path.join(env["HOME"]))))
    f.append(dict(id="warm-literal-line50", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"],
                  cache=lambda env: literal_cache(env, exec_usep="\n" * 39 + "kitty" + USEP + "--warm")))
    f.append(dict(id="warm-literal-line49", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"],
                  cache=lambda env: literal_cache(env, exec_usep="\n" * 38 + "kitty" + USEP + "--warm")))
    f.append(dict(id="warm-literal-cmd-function", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"], cache=lambda env: literal_cache(env, cmd="read_cache")))
    f.append(dict(id="warm-literal-cmd-empty", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"], cache=lambda env: literal_cache(env, cmd="")))
    f.append(dict(id="warm-literal-exec-usep-empty", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"], cache=lambda env: literal_cache(env, exec_usep="")))
    f.append(dict(id="warm-literal-newline-exec", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"],
                  cache=lambda env: literal_cache(env, exec_usep="kitty" + USEP + "a\nb")))
    f.append(dict(id="warm-literal-disable-directive",
                  files=base_files(FOOT, "/disable_cache\nfoot.desktop\n"),
                  exec=["bin/foot", "bin/kitty"], args=["--print-cmd"],
                  cache=lambda env: literal_cache(env)))
    f.append(dict(id="warm-literal-symlink-cache", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-id"], cache=lambda env: literal_cache(env, entry_id="cached.desktop")))
    # HOME unset
    f.append(dict(id="home-unset-default", files=base_files(), exec=["bin/foot"],
                  args=["--print-id"], env_after={"HOME": None, "XDG_CONFIG_HOME": None}))
    f.append(dict(id="home-unset-all-set", files=base_files(), exec=["bin/foot"],
                  args=["--print-id"], env_after={"HOME": None}))
    # a hit with the list unreadable (proves the warm path never reads it): chmod happens in the cache lambda
    f.append(dict(id="warm-hit-list-unreadable", files=base_files(), exec=["bin/foot", "bin/kitty"],
                  args=["--print-cmd"], cache=lambda env: _unreadable_list(env)))
    return f


def _unreadable_list(env):
    p = os.path.join(env["XDG_CONFIG_HOME"], "xdg-terminals.list")
    os.chmod(p, 0o000)              # first: the hash must describe the tree as the warm run sees it
    return literal_cache(env)


def main(argv):
    work = argv[1]
    ts = int(time.time() // 60) * 60 - 1800
    bad = 0
    fxs = fixtures()
    for case in fxs:
        try:
            ok, o, t, quiet, err = run_case(work, case, ts)
        except SystemExit:
            raise
        except Exception as ex:                        # noqa: BLE001
            print("FAIL %-34s EXC %r" % (case["id"], ex))
            bad += 1
            continue
        if ok:
            print("ok   %-34s oracle=(%d, %r)" % (case["id"], o[0], o[1][:90]))
        else:
            bad += 1
            print("FAIL %-34s oracle=%r tool=%r quiet=%s\n     tool-stderr=%r" %
                  (case["id"], o, t, quiet, err[-300:]))
    print("WARM: fixtures=%d/%d" % (len(fxs) - bad, len(fxs)))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
