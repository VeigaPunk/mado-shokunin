#!/usr/bin/env python3
"""Raw probes of the pinned resolver's cache edges, run inside the counter-shaped sandbox.

  /usr/bin/python3 /mod/probe_pin.py <workdir>

Each scenario builds a fresh root under <workdir>, primes (or writes) a cache, mutates, and prints
  NAME rc=<rc> stdout=<repr> stderr=<last line>
Nothing is asserted: this only records what xdg-terminal-exec v0.14.3 actually does.
"""
import os
import shutil
import subprocess
import sys
import time

PIN = "/oracle/xdg-terminal-exec"
NOW = int(time.time())
RSEP = b"\x1e"
TERM = RSEP + b"END_OF_EXEC_USEP"


def rmtree(path):
    for dirpath, dirnames, _f in os.walk(path):
        for nm in dirnames:
            try:
                os.chmod(os.path.join(dirpath, nm), 0o755)
            except OSError:
                pass
    shutil.rmtree(path, ignore_errors=True)


def base(root, entry_text=None, execs=("foot", "kitty"), cache_dir=".rw/cache"):
    """The minimal case: a list naming foot.desktop, entries, stub executables, XDG dirs under root."""
    for d in ("home/.config", "home/.local/share/applications", "bin", cache_dir, "data/applications"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    for name in execs:
        p = os.path.join(root, "bin", name)
        with open(p, "w") as fh:
            fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)
    text = entry_text if entry_text is not None else (
        "[Desktop Entry]\nType=Application\nName=Foot\nExec=foot\n"
        "Categories=System;TerminalEmulator;\n")
    with open(os.path.join(root, "home/.local/share/applications/foot.desktop"), "w") as fh:
        fh.write(text)
    with open(os.path.join(root, "home/.config/xdg-terminals.list"), "w") as fh:
        fh.write("foot.desktop\n")


def env(root, **kw):
    e = {
        "HOME": os.path.join(root, "home"),
        "XDG_CONFIG_HOME": os.path.join(root, "home/.config"),
        "XDG_CONFIG_DIRS": os.path.join(root, "nonexist"),
        "XDG_DATA_HOME": os.path.join(root, "home/.local/share"),
        "XDG_DATA_DIRS": os.path.join(root, "nonexist"),
        "XDG_CACHE_HOME": os.path.join(root, ".rw/cache"),
        "XDG_CURRENT_DESKTOP": "Hyprland",
        "PATH": os.path.join(root, "bin") + ":/oracle/bin",
        "LANG": "C.UTF-8",
    }
    for k, v in kw.items():
        if v is None:
            e.pop(k, None)
        else:
            e[k] = v.replace("$ROOT", root)
    return e


def run(e, args, wrapper=True):
    argv = (["/xbin/wrapped-pin"] if wrapper else [PIN]) + args
    p = subprocess.run(argv, env=e, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    tail = [ln for ln in p.stderr.decode("utf-8", "surrogateescape").splitlines() if ln.strip()][-1:]
    return p.returncode, p.stdout.decode("utf-8", "surrogateescape"), (tail[0] if tail else "")


def prime(root, args=("--print-cmd",)):
    cache = os.path.join(root, ".rw/cache/xdg-terminal-exec")
    rc, out, err = run(env(root), list(args))
    for _ in range(100):
        if os.path.exists(cache):
            break
        time.sleep(0.02)
    return cache, rc, out


def write_cache(root, text):
    cache = os.path.join(root, ".rw/cache/xdg-terminal-exec")
    with open(cache, "wb") as fh:
        fh.write(text)
    return cache


def read(p):
    try:
        with open(p, "rb") as fh:
            return fh.read()
    except OSError:
        return b"<absent>"


def scenario(work, name, fn):
    root = os.path.join(work, "s_" + name)
    rmtree(root)
    os.makedirs(root)
    detail = fn(root)
    print("%-28s %s" % (name, detail))


def main(argv):
    work = argv[1]
    def s_home_unset(root):
        base(root)
        rc, out, err = run(env(root, HOME=None, XDG_CONFIG_HOME=None, XDG_DATA_HOME=None,
                                XDG_CACHE_HOME=None), ["--print-id"])
        return "rc=%d stdout=%r stderr=%r" % (rc, out, err)

    def s_home_unset_xdg_set(root):
        base(root)
        e = env(root)
        e.pop("HOME")
        rc, out, err = run(e, ["--print-id"])
        return "rc=%d stdout=%r stderr=%r" % (rc, out, err)

    def s_home_unset_cache_default(root):
        base(root)
        e = env(root, XDG_CACHE_HOME=None)
        e.pop("HOME")
        rc, out, err = run(e, ["--print-id"])
        return "rc=%d stdout=%r stderr=%r" % (rc, out, err)

    def s_home_unset_datahome_default(root):
        base(root)
        e = env(root, XDG_DATA_HOME=None)
        e.pop("HOME")
        rc, out, err = run(e, ["--print-id"])
        return "rc=%d stdout=%r stderr=%r" % (rc, out, err)

    def s_cache_unreadable(root):
        base(root)
        cache, rc0, out0 = prime(root)
        os.chmod(cache, 0o000)
        rc, out, err = run(env(root), ["--print-id", "--print-path"])
        os.chmod(cache, 0o600)
        return "prime_rc=%d cold=%r warm rc=%d stdout=%r stderr=%r" % (rc0, out0, rc, out, err)

    def s_cache_dir(root):
        base(root)
        os.makedirs(os.path.join(root, ".rw/cache/xdg-terminal-exec"))
        rc, out, err = run(env(root), ["--print-id"])
        return "rc=%d stdout=%r stderr=%r" % (rc, out, err)

    def s_cache_invalid_no_terminator(root):
        base(root)
        write_cache(root, b"x" * 32 + b"\nfoot\n\n\n\n\n\n\n\n\nfoot\n")
        rc, out, err = run(env(root), ["--print-id", "--print-cmd"])
        return "rc=%d stdout=%r stderr=%r" % (rc, out, err)

    def s_cache_invalid_line50(root):
        base(root)
        body = b"x" * 32 + b"\n" + b"\n".join([b"f"] * 9) + b"\n" + b"\n".join([b"w"] * 39) + b"\n" + \
            b"zzz" + TERM + b"\n"
        write_cache(root, body)          # terminator on line 50
        rc, out, err = run(env(root), ["--print-id", "--print-cmd"])
        return "lines=%d rc=%d stdout=%r stderr=%r" % (body.count(b"\n"), rc, out, err)

    def s_cache_invalid_line49_ok(root):
        base(root)
        # 10 field lines + 38 command lines + terminator on line 49
        body = b"x" * 32 + b"\n" + b"\n".join([b"k"] * 9) + b"\n" + b"\n".join([b"w"] * 38) + b"\n" + \
            b"zzz" + TERM + b"\n"
        write_cache(root, body)
        rc, out, err = run(env(root), ["--print-id", "--print-cmd"])
        return "lines=%d rc=%d stdout=%r stderr=%r" % (body.count(b"\n"), rc, out, err)

    def s_cache_no_final_newline(root):
        base(root)
        prime(root)
        cache = os.path.join(root, ".rw/cache/xdg-terminal-exec")
        data = read(cache)
        write_cache(root, data.rstrip(b"\n"))     # terminator line now lacks its LF
        rc, out, err = run(env(root), ["--print-id", "--print-cmd"])
        return "rc=%d stdout=%r stderr=%r" % (rc, out, err)

    def s_warm_differs_from_cold(root):
        """Warm hit whose cached exec args differ from what a cold run would now compute."""
        base(root)
        prime(root)
        # same size + same mtime minute: rewrite the entry with other args
        p = os.path.join(root, "home/.local/share/applications/foot.desktop")
        st = os.stat(p)
        body = ("[Desktop Entry]\nType=Application\nName=Foot\nExec=kitty --warm\n"
                "Categories=System;TerminalEmulator;\n").encode()
        with open(p, "wb") as fh:
            fh.write(body[:st.st_size].ljust(st.st_size, b"\n"))
        os.utime(p, (st.st_atime, st.st_mtime))
        cold = run(env(root), ["--print-cmd"])
        cache = os.path.join(root, ".rw/cache/xdg-terminal-exec")
        warm = run(env(root), ["--print-cmd"])
        return "cold rc=%d out=%r ; warm rc=%d out=%r" % (cold[0], cold[1], warm[0], warm[1])

    def s_disable_cache_directive_with_valid_cache(root):
        base(root)
        prime(root)
        with open(os.path.join(root, "home/.config/xdg-terminals.list"), "ab") as fh:
            fh.write(b"/disable_cache\n")
        rc, out, err = run(env(root), ["--print-cmd"])
        exists = os.path.exists(os.path.join(root, ".rw/cache/xdg-terminal-exec"))
        return "rc=%d out=%r cache_after=%s" % (rc, out, exists)

    def s_cache_removed_entry_path_print_content(root):
        base(root)
        prime(root, ["--print-id", "--print-path", "--print-cmd"])
        p = os.path.join(root, "home/.local/share/applications/foot.desktop")
        sz = os.stat(p).st_size
        os.unlink(p)
        rc, out, err = run(env(root), ["--print-id", "--print-content"])
        return "entry_size=%d rc=%d stdout=%r stderr=%r" % (sz, rc, out, err)

    def s_cache_removed_entry_path_print_path(root):
        base(root)
        prime(root, ["--print-id", "--print-path", "--print-cmd"])
        p = os.path.join(root, "home/.local/share/applications/foot.desktop")
        os.unlink(p)
        # keep the hash: a deleted file changes the listing, so prime again is impossible; instead rewrite
        rc, out, err = run(env(root), ["--print-id", "--print-path"])
        return "rc=%d stdout=%r" % (rc, out)

    def s_cache_cmd_gone(root):
        base(root)
        prime(root)
        os.unlink(os.path.join(root, "bin/foot"))
        rc, out, err = run(env(root), ["--print-id", "--print-cmd"])
        return "rc=%d stdout=%r stderr=%r" % (rc, out, err)

    def s_cache_cmd_still_resolves_other_exec(root):
        base(root)
        prime(root)
        # exec[0] resolves, but the entry's later words change
        p = os.path.join(root, "bin/foot")
        with open(p, "w") as fh:
            fh.write("#!/bin/sh\nexit 1\n")
        os.utime(p, (0, 0))
        rc, out, err = run(env(root), ["--print-cmd"])
        return "rc=%d stdout=%r" % (rc, out)

    def s_cache_args_from_options(root):
        base(root, entry_text="[Desktop Entry]\nType=Application\nName=Foot\nExec=foot\n"
                              "X-TerminalArgTitle=--title\nX-TerminalArgDir=--working-directory=\n"
                              "X-TerminalArgAppId=--app-id=\nX-TerminalArgHold=--hold\n"
                              "Categories=System;TerminalEmulator;\n")
        cache, rc0, out0 = prime(root)
        data = read(cache)
        rc, out, err = run(env(root), ["--print-cmd", "--title=T", "--dir=/d", "--app-id=A", "--hold"])
        return "prime=%r rc=%d stdout=%r" % (out0, rc, out)

    def s_cache_newline_in_exec(root):
        base(root, entry_text="[Desktop Entry]\nType=Application\nName=Foot\n"
                              "Exec=foot \"a\nb\"\nCategories=System;TerminalEmulator;\n")
        cache, rc0, out0 = prime(root)
        data = read(cache)
        rc, out, err = run(env(root), ["--print-cmd"])
        return "cache_lines=%d prime_out=%r rc=%d stdout=%r" % (data.count(b"\n"), out0, rc, out)

    def s_env_cache_disabled(root):
        base(root)
        prime(root)
        rc, out, err = run(env(root, XTE_CACHE_ENABLED="false"), ["--print-cmd"])
        exists = os.path.exists(os.path.join(root, ".rw/cache/xdg-terminal-exec"))
        return "rc=%d out=%r cache_after=%s" % (rc, out, exists)

    def s_env_cache_disabled_empty(root):
        base(root)
        prime(root)
        rc, out, err = run(env(root, XTE_CACHE_ENABLED=""), ["--print-cmd"])
        exists = os.path.exists(os.path.join(root, ".rw/cache/xdg-terminal-exec"))
        return "rc=%d out=%r cache_after=%s stderr=%r" % (rc, out, exists, err)

    for nm, fn in sorted(locals().items()):
        if nm.startswith("s_") and callable(fn):
            scenario(work, nm[2:], fn)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
