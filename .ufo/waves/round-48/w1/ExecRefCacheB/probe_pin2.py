#!/usr/bin/env python3
"""Pin probes with a cache whose hash is REAL: the cache is written by this harness from
warmcache.gen_hash() over the resolver's own XTE__CONFIGS/XTE__APPLICATIONS_DIRS (XTE_DEBUG=1), so every
scenario below asks what the resolver does with a cache it would consider genuine.

  /usr/bin/python3 /mod/probe_pin2.py <workdir>

Prints, per scenario: rc, stdout, whether the cache file survived, and the cold answer for contrast.
"""
import os
import re
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import warmcache  # noqa: E402

PIN = "/oracle/xdg-terminal-exec"
TERM = warmcache.TERMINATOR
USEP = warmcache.USEP.encode()


def rmtree(path):
    for dirpath, dirnames, _f in os.walk(path):
        for nm in dirnames:
            try:
                os.chmod(os.path.join(dirpath, nm), 0o755)
            except OSError:
                pass
    shutil.rmtree(path, ignore_errors=True)


def base(root, entry_text=None, list_text=b"foot.desktop\n"):
    for d in ("home/.config", "home/.local/share/applications", "bin", ".rw/cache", "data/applications"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    for name in ("foot", "kitty"):
        p = os.path.join(root, "bin", name)
        with open(p, "w") as fh:
            fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)
    text = entry_text if entry_text is not None else (
        "[Desktop Entry]\nType=Application\nName=Foot\nExec=foot\n"
        "Categories=System;TerminalEmulator;\n")
    with open(os.path.join(root, "home/.local/share/applications/foot.desktop"), "w") as fh:
        fh.write(text)
    with open(os.path.join(root, "home/.config/xdg-terminals.list"), "wb") as fh:
        fh.write(list_text)


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


def run(e, args):
    p = subprocess.run([PIN] + args, env=e, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    tail = [ln for ln in p.stderr.decode("utf-8", "surrogateescape").splitlines() if ln.strip()][-2:]
    return p.returncode, p.stdout.decode("utf-8", "surrogateescape"), " | ".join(tail)


def paths_of(root):
    """The resolver's own XTE__CONFIGS / XTE__APPLICATIONS_DIRS, from a cold XTE_DEBUG=1 run."""
    e = env(root, XTE_DEBUG="1")
    p = subprocess.run([PIN, "--print-id"], env=e, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       timeout=60)
    err = p.stderr.decode("utf-8", "surrogateescape")
    conf = re.search(r"^D:   XTE__CONFIGS=(.*)$", err, re.M)
    apps = re.search(r"^D:   XTE__APPLICATIONS_DIRS=(.*)$", err, re.M)
    if not conf or not apps:
        raise SystemExit("no debug paths: %r" % err[-400:])
    return conf.group(1), apps.group(1)


def write_cache(root, lines):
    p = os.path.join(root, ".rw/cache/xdg-terminal-exec")
    with open(p, "wb") as fh:
        fh.write(b"".join(ln + b"\n" for ln in lines))
    return p


def cache_lines(root, cmd=b"foot", path_suffix=b"", entry=b"foot.desktop", action=b"",
                exec_usep=b"kitty" + USEP + b"--warm", args=(b"", b"", b"", b"", b""), hash_hex=None,
                n_command_lines=None):
    """A cache the resolver should accept: its own hash, then the ten fields, then the command."""
    conf, apps = paths_of(root)
    h = hash_hex or warmcache.gen_hash(os.environ.get("XDC", "Hyprland"), conf, apps).encode()
    epath = os.path.join(root, "home/.local/share/applications/foot.desktop").encode() + path_suffix
    fields = [h, cmd, epath, entry, action] + list(args)
    if n_command_lines is None:
        return fields + [exec_usep + TERM]
    out = fields + [b"" for _ in range(n_command_lines)]   # empty filler: collapses, keeps the exec
    out[-1] = out[-1] + exec_usep + TERM
    return out


def scenario(work, name, fn):
    root = os.path.join(work, "p_" + name)
    rmtree(root)
    os.makedirs(root)
    try:
        print("%-26s %s" % (name, fn(root)))
    except Exception as ex:                     # noqa: BLE001 - a probe reports, it does not judge
        print("%-26s EXC %r" % (name, ex))


def main(argv):
    work = argv[1]

    def s_hit_uses_cache(root):
        base(root)
        cold = run(env(root), ["--print-cmd"])
        write_cache(root, cache_lines(root))
        rc, out, err = run(env(root), ["--print-cmd"])
        return "cold=%r warm rc=%d out=%r err=%r" % (cold[1], rc, out, err)

    def s_hit_id_path_action(root):
        base(root)
        write_cache(root, cache_lines(root, entry=b"cached.desktop", action=b"act"))
        rc, out, err = run(env(root), ["--print-id", "--print-path"])
        return "rc=%d out=%r" % (rc, out)

    def s_hit_cmd_empty(root):
        base(root)
        write_cache(root, cache_lines(root, cmd=b""))
        rc, out, err = run(env(root), ["--print-cmd"])
        return "rc=%d out=%r err=%r" % (rc, out, err)

    def s_hit_cmd_function(root):
        base(root)
        write_cache(root, cache_lines(root, cmd=b"read_cache"))
        rc, out, err = run(env(root), ["--print-cmd"])
        return "rc=%d out=%r" % (rc, out)

    def s_hit_terminator_line49(root):
        base(root)
        # 10 fields + 38 filler + terminator on line 49
        write_cache(root, cache_lines(root, n_command_lines=39))
        rc, out, err = run(env(root), ["--print-cmd"])
        return "rc=%d out=%r (warm would be kitty --warm)" % (rc, out)

    def s_hit_terminator_line50(root):
        base(root)
        write_cache(root, cache_lines(root, n_command_lines=40))
        rc, out, err = run(env(root), ["--print-cmd"])
        return "rc=%d out=%r err=%r" % (rc, out, err)

    def s_hit_exec_usep_empty(root):
        base(root)
        write_cache(root, cache_lines(root, exec_usep=b""))
        rc, out, err = run(env(root), ["--print-cmd"])
        return "rc=%d out=%r" % (rc, out)

    def s_hit_entry_path_missing_content(root):
        base(root)
        cache = write_cache(root, cache_lines(root))
        # rewrite line 3 to a path that never existed: the hash does not cover the cache's own fields
        lines = open(cache, "rb").read().split(b"\n")
        lines[2] = b"/nonexistent/entry.desktop"
        write_cache(root, [ln for ln in lines if ln != b"" or True][:-1])
        rc, out, err = run(env(root), ["--print-id", "--print-content"])
        return "rc=%d out=%r err=%r" % (rc, out, err)

    def s_hit_entry_path_missing_path_mode(root):
        base(root)
        cache = write_cache(root, cache_lines(root))
        lines = open(cache, "rb").read().split(b"\n")
        lines[2] = b"/nonexistent/entry.desktop"
        write_cache(root, [ln for ln in lines][:-1])
        rc, out, err = run(env(root), ["--print-path", "--print-cmd"])
        return "rc=%d out=%r" % (rc, out)

    def s_hit_while_list_unreadable(root):
        base(root)
        os.chmod(os.path.join(root, "home/.config/xdg-terminals.list"), 0o000)   # before the hash: 0o000 shows in `ls -l`
        write_cache(root, cache_lines(root))
        rc, out, err = run(env(root), ["--print-cmd"])
        return "rc=%d out=%r err=%r" % (rc, out, err)

    def s_hit_with_disable_cache_directive(root):
        base(root, list_text=b"/disable_cache\nfoot.desktop\n")
        write_cache(root, cache_lines(root))
        cache = os.path.join(root, ".rw/cache/xdg-terminal-exec")
        rc, out, err = run(env(root), ["--print-cmd"])
        return "rc=%d out=%r cache_after=%s" % (rc, out, os.path.exists(cache))

    def s_hit_with_disable_cache_directive_id(root):
        base(root, list_text=b"/disable_cache\nfoot.desktop\n")
        write_cache(root, cache_lines(root, entry=b"cached.desktop"))
        rc, out, err = run(env(root), ["--print-id"])
        return "rc=%d out=%r" % (rc, out)

    def s_hit_newline_in_exec_usep(root):
        base(root)
        write_cache(root, cache_lines(root, exec_usep=b"kitty" + USEP + b"a\nb" + USEP + b"--x"))
        rc, out, err = run(env(root), ["--print-cmd"])
        return "rc=%d out=%r" % (rc, out)

    def s_hit_stale_by_mtime(root):
        base(root)
        write_cache(root, cache_lines(root))
        p = os.path.join(root, "home/.local/share/applications/foot.desktop")
        st = os.stat(p)
        os.utime(p, (st.st_atime, st.st_mtime - 600))       # a minute change is enough
        rc, out, err = run(env(root), ["--print-cmd"])
        return "rc=%d out=%r (cold answer expected)" % (rc, out)

    def s_hit_same_size_same_minute(root):
        base(root)
        write_cache(root, cache_lines(root))
        p = os.path.join(root, "home/.local/share/applications/foot.desktop")
        st = os.stat(p)
        with open(p, "wb") as fh:
            fh.write(
                ("[Desktop Entry]\nType=Application\nName=Foot\nExec=foot --x\n"
                 "Categories=System;TerminalEmulator;\n").encode()[:st.st_size]
                .ljust(st.st_size, b"\n"))
        os.utime(p, (st.st_atime, st.st_mtime))
        rc, out, err = run(env(root), ["--print-cmd"])
        return "rc=%d out=%r (warm = kitty --warm)" % (rc, out)

    def s_hash_desktop_change(root):
        base(root)
        write_cache(root, cache_lines(root))
        rc, out, err = run(env(root, XDG_CURRENT_DESKTOP="GNOME"), ["--print-cmd"])
        return "rc=%d out=%r" % (rc, out)

    for nm, fn in sorted(locals().items()):
        if nm.startswith("s_") and callable(fn):
            scenario(work, nm[2:], fn)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
