#!/usr/bin/env python3
"""RevC1Ls targeted matrix: one purpose-built tree per named attack class, pin vs frozen tool gen_hash.

Each case builds its own tree, runs the REAL pin (forced to compute gen_hash via a complete-but-stale
cache), and compares the pin's hash with the frozen tool's. --list prints the case names.
Reuse the driver's helpers so both harnesses share one implementation of pin-run/parse/ls/tool-hash.
"""
import json
import os
import socket
import stat
import sys
import time

S = "/fast/scratch/hyaku/mado-r48/RevC1Ls"
sys.path.insert(0, os.path.join(S, "run"))
import driver as D                                   # noqa: E402  (imports the frozen tool too)

MDIR = os.path.join(S, "run", "matrix")
SIX = D.SIX_MONTHS


def mk(root, rel, text=None, mode=None):
    p = os.path.join(root, rel)
    if rel.endswith("/"):
        os.makedirs(p, exist_ok=True)
        return p
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="latin-1", errors="surrogateescape") as fh:
        fh.write("" if text is None else text)
    if mode is not None:
        os.chmod(p, mode)
    return p


def setm(root, rel, mtime=None, times=("recent",)):
    """mtime: absolute; times: recent|old|future|epoch|neg|edge-min|edge-plus|sixminus|sixplus."""
    now = int(time.time())
    p = os.path.join(root, rel)
    if mtime is None:
        k = times[0]
        mtime = {"recent": now - 3600, "old": now - 86400 * 700, "future": now + 3600,
                 "epoch": 0, "neg": -86400 * 400,
                 "edge-min": now - SIX + 2 * 86400, "edge-plus": now - SIX - 2 * 86400,
                 "sixminus": now - SIX + 86400, "sixplus": now - SIX - 86400,
                 "bindexact": now - SIX, "nowexact": now}[k]
    os.utime(p, ns=(mtime * 10 ** 9, mtime * 10 ** 9), follow_symlinks=False)
    return mtime


def skel(root, desk="Hyprland", tz="UTC", cfgdirs=None, datadirs=None, lists=True):
    """Standard skeleton: HOME/cache/config/data + the list files the resolver always hashes."""
    os.makedirs(root + "/home", exist_ok=True)
    os.makedirs(root + "/cache", exist_ok=True)
    cfg = [root + "/cfg"] + [root + "/" + d for d in (cfgdirs or ["xdgA"])]
    sysd = [root + "/" + d for d in (datadirs or ["usr/share"])]
    for d in cfg:
        os.makedirs(d, exist_ok=True)
        for dk in D.desktop_names(desk) + [None]:
            nm = (dk + "-xdg-terminals.list") if dk else "xdg-terminals.list"
            if lists is not False:
                mk(root, os.path.relpath(os.path.join(d, nm), root), "foot.desktop\n")
    for d in sysd:
        os.makedirs(os.path.join(d, "xdg-terminal-exec"), exist_ok=True)
        os.makedirs(os.path.join(d, "applications"), exist_ok=True)
        for dk in D.desktop_names(desk) + [None]:
            nm = (dk + "-xdg-terminals.list") if dk else "xdg-terminals.list"
            mk(root, os.path.relpath(os.path.join(d, "xdg-terminal-exec", nm), root), "foot.desktop\n")
    env = {"HOME": root + "/home", "PATH": "/usr/bin:/bin", "TZ": tz,
           "XDG_CONFIG_HOME": cfg[0], "XDG_CONFIG_DIRS": ":".join(cfg[1:]),
           "XDG_DATA_HOME": root + "/data", "XDG_DATA_DIRS": ":".join(sysd),
           "XDG_CACHE_HOME": root + "/cache"}
    if desk != "":
        env["XDG_CURRENT_DESKTOP"] = desk
    mk(root, "data/applications/foot.desktop",
       "[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nName=foot\nExec=foot\n")
    return env, cfg, sysd


def entry(root, rel, text="[Desktop Entry]\n", times=("recent",)):
    p = mk(root, rel, text, mode=0o644)
    setm(root, rel, times=times)
    return p


def settle(root, kind="recent"):
    now = int(time.time())
    t = {"recent": now - 3600, "recent2": now - 7200, "old": now - 86400 * 700,
         "future": now + 3600, "epoch": 0, "neg": -86400 * 400}[kind]
    for base, ds, fs in os.walk(root):
        for n in ds + fs:
            try:
                os.utime(os.path.join(base, n), ns=(t * 10 ** 9, t * 10 ** 9), follow_symlinks=False)
            except OSError:
                pass
    try:
        os.utime(root, ns=(t * 10 ** 9, t * 10 ** 9))
    except OSError:
        pass


def own(paths, spec):
    paths = [p for p in paths if os.path.lexists(p)]
    for i in range(0, len(paths), 8):
        import subprocess
        subprocess.run(["sudo", "-n", "chown", "-h", spec, "--"] + paths[i:i + 8],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def compare(root, env):
    os.environ["TZ"] = env["TZ"]
    time.tzset()
    D.stale_cache(root)
    rc, out, err = D.pin_run(root, env)
    rec = {"pin_rc": rc, "desk": env.get("XDG_CURRENT_DESKTOP")}
    pin_hash = None
    for line in err.decode("latin-1").split("\n"):
        if "got fresh hash '" in line:
            pin_hash = line.split("got fresh hash '")[1].split("'")[0]
    rec["pin_hash"] = pin_hash
    if pin_hash is None:
        rec["verdict"] = "PIN-NO-HASH"
        rec["pin_stderr"] = err.decode("latin-1")[-800:]
        return rec
    conf, apps = D.parse_paths(err)
    ops = (D.split_colon(conf) if conf is not None else []) + (D.split_colon(apps) if apps is not None else [])
    rec["operands"] = len(ops)
    rec["existing_ops"] = sum(1 for o in ops if o and os.path.exists(o))
    lsrc, lout = D.ls_run(ops, root, env)
    rec["real_ls_rc"] = lsrc
    rec["real_ls_lines"] = lout.count(b"\n")
    rec["h_ls_pinops"] = D.h_of(env.get("XDG_CURRENT_DESKTOP", ""), lout)
    th, tops, terr = D.tool_hash(root, env)
    rec["tool_hash"] = th
    rec["tool_err"] = terr
    if rec["h_ls_pinops"] != pin_hash:
        rec["verdict"] = "HARNESS-ECHO-DIFF"
    elif terr is not None and terr.startswith("OOC:"):
        rec["verdict"] = "TOOL-OOC"
    elif th == pin_hash:
        rec["verdict"] = "PASS"
    else:
        rec["verdict"] = "MISMATCH"
        rec["attribute"] = "listing" if D.h_of(env.get("XDG_CURRENT_DESKTOP", ""),
                                               D.ls_run(ops if tops is None else D.split_colon(tops), root, env)[1]) == pin_hash else "operand-list"
        rec["listing_diff"] = D.diff_lines(lout, ops, root, env, rec)
    return rec


# ------------------------------------------------------------------ cases
def c_dangling_entry_alone(root):
    env, cfg, sysd = skel(root)
    os.symlink("/nonexistent/x", os.path.join(sysd[0], "applications", "gone.desktop"))
    settle(root)
    return env


def c_dangling_entry_mixed(root):
    env, cfg, sysd = skel(root)
    a = sysd[0] + "/applications"
    entry(root, "usr/share/applications/a.desktop")
    os.symlink("/nonexistent/y", a + "/broken.desktop")
    entry(root, "usr/share/applications/zzzzzzzzzzzzzzzzzzzz.desktop")
    own([a + "/a.desktop"], "4242")
    settle(root)
    return env


def c_dangling_operand_only(root):
    env, cfg, sysd = skel(root)
    p = cfg[0] + "/xdg-terminals.list"
    os.remove(p)
    os.symlink("/nonexistent/list", p)
    settle(root)
    return env


def c_dangling_operand_with_file(root):
    env, cfg, sysd = skel(root)
    p = cfg[0] + "/xdg-terminals.list"
    os.remove(p)
    os.symlink("/nonexistent/list", p)
    settle(root)
    return env


def c_dangling_two_entries(root):
    env, cfg, sysd = skel(root)
    a = sysd[0] + "/applications"
    os.symlink("/nonexistent/1", a + "/b1.desktop")
    os.symlink("/nonexistent/2", a + "/b2.desktop")
    settle(root)
    return env


def c_numeric_all(root):
    env, cfg, sysd = skel(root)
    a = sysd[0] + "/applications"
    for i in range(3):
        entry(root, "usr/share/applications/n%d.desktop" % i)
    own([a + "/n0.desktop", a + "/n1.desktop", a + "/n2.desktop"], "4242:4242")
    settle(root)
    return env


def c_numeric_mixed(root):
    env, cfg, sysd = skel(root)
    a = sysd[0] + "/applications"
    entry(root, "usr/share/applications/named.desktop")
    entry(root, "usr/share/applications/numeric.desktop")
    own([a + "/numeric.desktop"], "4242:4242")
    settle(root)
    return env


def c_numeric_wide(root):
    env, cfg, sysd = skel(root)
    a = sysd[0] + "/applications"
    entry(root, "usr/share/applications/short.desktop")
    entry(root, "usr/share/applications/wide.desktop")
    own([a + "/wide.desktop"], "1234567:7654321")
    settle(root)
    return env


def c_numeric_gid_only(root):
    env, cfg, sysd = skel(root)
    a = sysd[0] + "/applications"
    entry(root, "usr/share/applications/g.desktop")
    own([a + "/g.desktop"], ":60000")
    settle(root)
    return env


def c_numeric_uid_only(root):
    env, cfg, sysd = skel(root)
    a = sysd[0] + "/applications"
    entry(root, "usr/share/applications/u.desktop")
    own([a + "/u.desktop"], "60000")
    settle(root)
    return env


def c_numeric_dir_entry(root):
    env, cfg, sysd = skel(root)
    a = sysd[0] + "/applications"
    mk(root, "usr/share/applications/sub/")
    own([a + "/sub"], "4242:4242")
    settle(root)
    return env


def c_numeric_operand_file(root):
    env, cfg, sysd = skel(root)
    own([cfg[0] + "/xdg-terminals.list"], "4242:4242")
    settle(root)
    return env


def c_root_owned_name(root):
    env, cfg, sysd = skel(root)
    a = sysd[0] + "/applications"
    entry(root, "usr/share/applications/r.desktop")
    own([a + "/r.desktop"], "0:0")
    settle(root)
    return env


def c_symlink_dir_twins(root):
    env, cfg, sysd = skel(root)
    a = sysd[0] + "/applications"
    mk(root, "usr/share/applications/target/x.desktop")
    os.symlink("target", a + "/alink")
    os.symlink("target", a + "/blink")
    settle(root)
    return env


def c_symlink_dir_and_real(root):
    env, cfg, sysd = skel(root)
    a = sysd[0] + "/applications"
    mk(root, "usr/share/applications/real/x.desktop")
    os.symlink("real", a + "/alias")
    settle(root)
    return env


def c_symlink_dir_operand(root):
    """`<datadir>/applications` is itself a symlink: the operand is a symlink + trailing slash."""
    env, cfg, sysd = skel(root)
    a = sysd[0] + "/applications"
    os.rename(a, sysd[0] + "/applications.real")
    os.symlink("applications.real", a)
    with open(sysd[0] + "/applications.real/x.desktop", "w") as fh:
        fh.write("[Desktop Entry]\n")
    settle(root)
    return env


def c_symlink_dir_operand_slash(root):
    """A config list path that is a symlink to a directory: a dir operand with no trailing slash."""
    env, cfg, sysd = skel(root)
    p = cfg[0] + "/xdg-terminals.list"
    os.remove(p)
    os.makedirs(cfg[0] + "/listdir", exist_ok=True)
    with open(cfg[0] + "/listdir/inner.desktop", "w") as fh:
        fh.write("[Desktop Entry]\n")
    os.makedirs(cfg[0] + "/listdir/sub", exist_ok=True)
    os.symlink("listdir", p)
    settle(root)
    return env


def c_symlink_ancestor_loop(root):
    env, cfg, sysd = skel(root)
    a = sysd[0] + "/applications"
    mk(root, "usr/share/applications/sub/x.desktop")
    os.symlink("..", a + "/up")
    settle(root)
    return env


def c_symlink_to_self(root):
    env, cfg, sysd = skel(root)
    a = sysd[0] + "/applications"
    os.symlink("self", a + "/self")
    settle(root)
    return env


def c_symlink_chain(root):
    env, cfg, sysd = skel(root)
    a = sysd[0] + "/applications"
    mk(root, "usr/share/applications/c/x.desktop")
    os.symlink("c", a + "/b")
    os.symlink("b", a + "/a")
    settle(root)
    return env


def c_empty_operand(root):
    """The hashed application directory itself is empty."""
    env, cfg, sysd = skel(root)
    os.remove(root + "/data/applications/foot.desktop")
    settle(root)
    return env


def c_empty_nested(root):
    env, cfg, sysd = skel(root)
    mk(root, "usr/share/applications/emptydir/")
    settle(root)
    return env


def c_hidden_only(root):
    env, cfg, sysd = skel(root)
    mk(root, "usr/share/applications/.only")
    settle(root)
    return env


def c_empty_hidden_mix(root):
    env, cfg, sysd = skel(root)
    mk(root, "usr/share/applications/emptydir/")
    mk(root, "usr/share/applications/.hidden")
    mk(root, "usr/share/applications/sub/")
    settle(root)
    return env


def c_time_future_file(root):
    env, cfg, sysd = skel(root)
    entry(root, "usr/share/applications/f.desktop", times=("future",))
    settle(root)
    setm(root, "usr/share/applications/f.desktop", times=("future",))
    return env


def c_time_future_dir(root):
    env, cfg, sysd = skel(root)
    mk(root, "usr/share/applications/sub/")
    settle(root)
    setm(root, "usr/share/applications/sub", times=("future",))
    return env


def c_time_epoch(root):
    env, cfg, sysd = skel(root)
    entry(root, "usr/share/applications/e.desktop")
    settle(root)
    setm(root, "usr/share/applications/e.desktop", times=("epoch",))
    return env


def c_time_negative(root):
    env, cfg, sysd = skel(root)
    entry(root, "usr/share/applications/n.desktop")
    settle(root)
    setm(root, "usr/share/applications/n.desktop", times=("neg",))
    return env


def c_time_edge_min(root):
    env, cfg, sysd = skel(root)
    entry(root, "usr/share/applications/m.desktop")
    settle(root)
    setm(root, "usr/share/applications/m.desktop", times=("edge-min",))
    return env


def c_time_edge_plus(root):
    env, cfg, sysd = skel(root)
    entry(root, "usr/share/applications/p.desktop")
    settle(root)
    setm(root, "usr/share/applications/p.desktop", times=("edge-plus",))
    return env


def c_time_now_exact(root):
    env, cfg, sysd = skel(root)
    entry(root, "usr/share/applications/t.desktop")
    settle(root)
    setm(root, "usr/share/applications/t.desktop", mtime=int(time.time()))
    return env


def c_time_mixed(root):
    env, cfg, sysd = skel(root)
    for nm, kind in (("a.desktop", "recent"), ("b.desktop", "old"), ("c.desktop", "future"),
                     ("d.desktop", "epoch")):
        entry(root, "usr/share/applications/" + nm, times=(kind,))
    settle(root)
    for nm, kind in (("a.desktop", "recent"), ("b.desktop", "old"), ("c.desktop", "future"),
                     ("d.desktop", "epoch")):
        setm(root, "usr/share/applications/" + nm, times=(kind,))
    return env


def c_time_boundary_exact(root):
    env, cfg, sysd = skel(root)
    entry(root, "usr/share/applications/bd.desktop")
    settle(root)
    setm(root, "usr/share/applications/bd.desktop", times=("bindexact",))
    return env


def c_many_dirs_files(root):
    env, cfg, sysd = skel(root)
    dirs = []
    for i in range(12):
        d = root + "/usr/share/applications/d%02d" % i
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "e.desktop"), "w") as fh:
            fh.write("x" * (i * 37 + 1))
        dirs.append(d)
    settle(root)
    return env


def c_file_only_operands(root):
    env, cfg, sysd = skel(root, cfgdirs=[], datadirs=["usr/share"])
    # remove every applications dir so only file operands print
    os.rmdir(sysd[0] + "/applications")
    settle(root)
    return env


def c_dup_dir_operand(root):
    env, cfg, sysd = skel(root)
    env["XDG_CONFIG_DIRS"] = cfg[0] + ":" + cfg[1]
    settle(root)
    return env


def c_file_block_widths(root):
    env, cfg, sysd = skel(root)
    big = cfg[0] + "/xdg-terminals.list"
    with open(big, "w") as fh:
        fh.write("x" * 9000)
    mk(root, "usr/share/applications/wide/e.desktop", "y" * 1000)
    settle(root)
    return env


def c_double_slash(root):
    env, cfg, sysd = skel(root)
    env["XDG_DATA_DIRS"] = root + "//usr/share"
    env["XDG_CONFIG_DIRS"] = root + "//xdgA"
    settle(root)
    return env


def c_dot_component(root):
    env, cfg, sysd = skel(root)
    env["XDG_DATA_DIRS"] = root + "/./usr/share"
    settle(root)
    return env


def c_dotdot_component(root):
    env, cfg, sysd = skel(root)
    env["XDG_DATA_DIRS"] = root + "/usr/xdgA/../share"
    env["XDG_CONFIG_DIRS"] = root + "/usr/../xdgA"
    settle(root)
    return env


def c_relative_paths(root):
    env, cfg, sysd = skel(root)
    env["XDG_DATA_DIRS"] = "usr/share"
    env["XDG_CONFIG_DIRS"] = "xdgA"
    settle(root)
    return env


def c_trailing_slash_xdg(root):
    env, cfg, sysd = skel(root)
    env["XDG_CONFIG_HOME"] = cfg[0] + "/"
    env["XDG_DATA_HOME"] = root + "/data/"
    settle(root)
    return env


def c_dash_desktop(root):
    env, cfg, sysd = skel(root, desk="-n")
    settle(root)
    return env


def c_empty_desktop(root):
    env, cfg, sysd = skel(root, desk="")
    settle(root)
    return env


def c_multidesktop(root):
    env, cfg, sysd = skel(root, desk="Hyprland:GNOME:sway")
    settle(root)
    return env


def c_long_name(root):
    env, cfg, sysd = skel(root)
    entry(root, "usr/share/applications/" + "n" * 96 + ".desktop")
    settle(root)
    return env


def c_high_byte_name(root):
    env, cfg, sysd = skel(root)
    p = os.path.join(sysd[0].encode(), b"applications", b"caf\xe9.desktop")
    with open(p, "wb") as fh:
        fh.write(b"[Desktop Entry]\n")
    settle(root)
    return env


def c_space_tab_names(root):
    env, cfg, sysd = skel(root)
    entry(root, "usr/share/applications/with space.desktop")
    entry(root, "usr/share/applications/tab\tname.desktop")
    entry(root, "usr/share/applications/quote'name.desktop")
    settle(root)
    return env


def c_unreadable_operand(root):
    env, cfg, sysd = skel(root)
    p = sysd[0] + "/applications"
    settle(root)
    os.chmod(p, 0o000)
    return env


def c_unreadable_nested(root):
    env, cfg, sysd = skel(root)
    mk(root, "usr/share/applications/locked/")
    settle(root)
    os.chmod(sysd[0] + "/applications/locked", 0o000)
    return env


def c_mode_bits(root):
    env, cfg, sysd = skel(root)
    entry(root, "usr/share/applications/suid.desktop")
    os.chmod(sysd[0] + "/applications/suid.desktop", 0o4755)
    entry(root, "usr/share/applications/sgid.desktop")
    os.chmod(sysd[0] + "/applications/sgid.desktop", 0o2755)
    mk(root, "usr/share/applications/sticky/")
    os.chmod(sysd[0] + "/applications/sticky", 0o1777)
    settle(root)
    return env


def c_socket_entry(root):
    env, cfg, sysd = skel(root)
    sp = sysd[0] + "/applications/sock.socket"
    s = socket.socket(socket.AF_UNIX)
    s.bind(sp)
    s.close()
    settle(root)
    return env


def c_hardlink_nlink(root):
    env, cfg, sysd = skel(root)
    a = entry(root, "usr/share/applications/hl1.desktop")
    os.link(a, sysd[0] + "/applications/hl2.desktop")
    settle(root)
    return env


def c_big_nlink_dir(root):
    env, cfg, sysd = skel(root)
    for i in range(14):
        mk(root, "usr/share/applications/many/s%02d/" % i)
    settle(root)
    return env


def c_mixed_sizes(root):
    env, cfg, sysd = skel(root)
    entry(root, "usr/share/applications/sizes.desktop", "x" * 900000)
    entry(root, "usr/share/applications/tiny.desktop", "y")
    settle(root)
    return env



def c_dup_appdir_operand(root):
    """The same application directory twice in XDG_DATA_DIRS: two identical dir operands."""
    env, cfg, sysd = skel(root)
    env["XDG_DATA_DIRS"] = sysd[0] + ":" + sysd[0]
    settle(root)
    return env


def c_unreadable_file_operand(root):
    env, cfg, sysd = skel(root)
    settle(root)
    os.chmod(cfg[0] + "/xdg-terminals.list", 0o000)
    return env


def c_high_byte_dir(root):
    """An XDG data dir whose name holds a byte that is not valid UTF-8."""
    raw = os.path.join(root.encode(), b"usr/l\xe9share")
    os.makedirs(os.path.join(raw, b"applications"), exist_ok=True)
    with open(os.path.join(raw, b"applications", b"foot.desktop"), "wb") as fh:
        fh.write(b"[Desktop Entry]\nExec=foot\n")
    env, cfg, sysd = skel(root)
    env["XDG_DATA_DIRS"] = os.path.join(root, "usr/l\udce9share")
    settle(root)
    return env


def c_device_entry(root):
    """A character device beside a 7-byte file: the shared size column."""
    env, cfg, sysd = skel(root)
    a = sysd[0] + "/applications"
    entry(root, "usr/share/applications/tiny.desktop", "y")
    settle(root)
    import subprocess
    subprocess.run(["sudo", "-n", "mknod", a + "/cd", "c", "10", "237"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    settle(root)
    return env


def c_newline_name(root):
    """A newline in a hashed name: the tool's declared out-of-contract class."""
    env, cfg, sysd = skel(root)
    with open(sysd[0] + "/applications/new\nline.desktop", "w") as fh:
        fh.write("[Desktop Entry]\n")
    settle(root)
    return env


def c_acl_xattr(root):
    """An ACL under a hashed path: the mode column grows a `+`, which the tool declares out of contract."""
    env, cfg, sysd = skel(root)
    entry(root, "usr/share/applications/acl.desktop")
    settle(root)
    import subprocess
    subprocess.run(["setfacl", "-m", "u:4242:r", sysd[0] + "/applications/acl.desktop"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return env


CASES = [(n[2:], f) for n, f in sorted(globals().items()) if n.startswith("c_") and callable(f)]


def run(only=None):
    os.makedirs(MDIR, exist_ok=True)
    recs = []
    for name, fn in CASES:
        if only and name != only:
            continue
        base = os.path.join(MDIR, name)
        os.system("sudo -n rm -rf -- %s >/dev/null 2>&1" % base)
        root = os.path.join(base, "r")
        os.makedirs(root, exist_ok=True)
        try:
            env = fn(root)
            rec = compare(root, env)
        except Exception as ex:
            rec = {"verdict": "HARNESS-ERROR", "error": repr(ex)[:500]}
        rec["case"] = name
        rec["tree"] = root
        recs.append(rec)
        print("%-26s %-14s pin=%s tool=%s%s" % (name, rec["verdict"], (rec.get("pin_hash") or "-")[:12],
                                               (rec.get("tool_hash") or "-")[:12],
                                               (" => " + str(rec.get("tool_err"))) if rec.get("tool_err") else ""))
        if rec["verdict"] == "PASS":
            os.system("sudo -n rm -rf -- %s >/dev/null 2>&1" % base)
    out = os.path.join(S, "run", "matrix.json")
    with open(out, "w") as fh:
        json.dump(recs, fh, indent=1)
    print("MATRIX cases=%d pass=%d other=%d -> %s" % (
        len(recs), sum(1 for r in recs if r["verdict"] == "PASS"),
        sum(1 for r in recs if r["verdict"] != "PASS"), out))
    return recs



# --------------------------------------------------------------- warm checks: the hash AS USED (cache hit/stale)
def wtree(root, kind, desk="Hyprland"):
    env, cfg, sysd = skel(root, desk=desk)
    e = ("[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=foot\nName=foot\n")
    mk(root, "usr/share/applications/foot.desktop", e)
    mk(root, "bin/foot", "#!/bin/sh\nexit 1\n", mode=0o755)
    env["PATH"] = root + "/bin:/usr/bin:/bin"
    a = sysd[0] + "/applications"
    if kind == "dangling":
        os.symlink("/nonexistent/x", a + "/broken.desktop")
        entry(root, "usr/share/applications/other.desktop")
    elif kind == "twins":
        mk(root, "usr/share/applications/target/x.desktop")
        os.symlink("target", a + "/alink")
        os.symlink("target", a + "/blink")
    elif kind == "empty":
        mk(root, "usr/share/applications/emptydir/")
    elif kind == "numeric":
        own([a + "/foot.desktop"], "4242:4242")
    elif kind == "times":
        entry(root, "usr/share/applications/future.desktop", times=("future",))
        entry(root, "usr/share/applications/old.desktop", times=("old",))
    elif kind == "multi":
        env["XDG_DATA_DIRS"] = sysd[0] + ":" + root + "/usr/local/share"
        mk(root, "usr/local/share/applications/l2.desktop", e)
    settle(root)
    if kind == "times":
        setm(root, "usr/share/applications/future.desktop", times=("future",))
        setm(root, "usr/share/applications/old.desktop", times=("old",))
    return env


def wait_cache(root, timeout=8.0):
    p = root + "/cache/xdg-terminal-exec"
    end = D.END.encode()
    t0 = time.time()
    last = b""
    while time.time() - t0 < timeout:
        try:
            with open(p, "rb") as fh:
                b = fh.read()
        except OSError:
            b = b""
        last = b
        if b.rstrip(b"\n").endswith(end):
            return b
        time.sleep(0.02)
    return last


def pin_state(err):
    t = err.decode("utf-8", "surrogateescape")
    for k, v in (("cache is actual", "hit"), ("cache is out-of-date", "stale"),
                 ("invalid cache data", "invalid"), ("reached cache line limit", "invalid"),
                 ("failed to get fresh hash", "invalid"), ("no cache data", "absent")):
        if k in t:
            return v
    return "disabled" if "paths:" in t else "-"


def tool_state(root, env):
    old = os.getcwd()
    os.chdir(root)
    try:
        r = D.mtool.Resolver(dict(env), cwd=root)
        r.select_paths()
        return r.read_cache()
    finally:
        os.chdir(old)


def warm_checks():
    out = []
    for kind in ("plain", "dangling", "twins", "empty", "numeric", "times", "multi"):
        base = os.path.join(MDIR, "warm_" + kind)
        os.system("sudo -n rm -rf -- %s >/dev/null 2>&1" % base)
        root = os.path.join(base, "r")
        os.makedirs(root, exist_ok=True)
        env = wtree(root, kind)
        os.environ["TZ"] = env["TZ"]
        time.tzset()
        rc1, o1, e1 = D.pin_run(root, env, ("--print-cmd",))
        cache = wait_cache(root)
        rec = {"kind": kind, "prime_rc": rc1, "cache_bytes": len(cache)}
        rc2, o2, e2 = D.pin_run(root, env, ("--print-cmd",))
        rec["pin_state_hit"] = pin_state(e2)
        rec["pin_stdout_hit"] = o2.decode("latin-1")
        rec["tool_state_hit"] = tool_state(root, env)
        try:
            tout, trc, _terr = D.mtool.run_print(dict(env), ["--print-cmd"], cwd=root)
        except Exception as ex:
            tout, trc = "EXC:%r" % ex, -1
        rec["tool_stdout_hit"] = tout
        rec["hit_agree"] = (o2.decode("latin-1") == tout and rc2 == trc and rec["pin_state_hit"] == "hit"
                            and rec["tool_state_hit"] == "hit")
        pin_hash = None
        for line in e2.decode("utf-8", "surrogateescape").split("\n"):
            if "got fresh hash '" in line:
                pin_hash = line.split("got fresh hash '")[1].split("'")[0]
        th, _ops, terr = D.tool_hash(root, env)
        rec.update({"pin_hash": pin_hash, "tool_hash": th, "tool_err": terr,
                    "hash_agree": pin_hash is not None and pin_hash == th})
        # invalidate: a NEW file in a hashed directory must make both sides report stale.
        # The tool is read FIRST: the pin's own cold run rewrites the cache at the end.
        with open(root + "/usr/share/applications/invalidate.desktop", "w") as fh:
            fh.write("[Desktop Entry]\n")
        rec["tool_state_stale"] = tool_state(root, env)
        try:
            tout2, trc2, _ = D.mtool.run_print(dict(env), ["--print-cmd"], cwd=root)
        except Exception as ex:
            tout2, trc2 = "EXC:%r" % ex, -1
        rc3, o3, e3 = D.pin_run(root, env, ("--print-cmd",))
        rec["pin_state_stale"] = pin_state(e3)
        rec["pin_stdout_stale"] = o3.decode("latin-1")
        rec["tool_stdout_stale"] = tout2
        # a same-length content edit with the mtime re-pinned must NOT move the hash (still a hit)
        p2 = next((c for c in (root + "/usr/share/applications/foot.desktop",
                               root + "/data/applications/foot.desktop") if os.access(c, os.W_OK)), None)
        try:
            if p2 is None:
                raise OSError("no writable desktop entry in a hashed dir: phase skipped")
            before = os.stat(p2).st_mtime_ns
            raw = open(p2, "rb").read()
            if b"foot" in raw:
                raw = raw.replace(b"foot", b"fOOt", 1)
            else:
                raw = raw[:1] + (b"Z" if raw[1:2] != b"Z" else b"Y") + raw[2:]
            with open(p2, "wb") as fh:
                fh.write(raw)
            os.utime(p2, ns=(before, before))
            rec["pin_state_samesize"] = pin_state(D.pin_run(root, env, ("--print-cmd",))[2])
            rec["tool_state_samesize"] = tool_state(root, env)
        except OSError as ex:
            tag = "ERR:no writable" if "no writable" in str(ex) else "ERR:%s" % ex
            rec["pin_state_samesize"] = rec["tool_state_samesize"] = tag
        rec["stale_agree"] = (o3.decode("latin-1") == tout2 and rc3 == trc2
                             and rec["pin_state_stale"] == "stale" and rec["tool_state_stale"] == "stale")
        same = (rec.get("pin_state_samesize") == rec.get("tool_state_samesize")
                and rec.get("pin_state_samesize") in ("hit", "ERR:no writable"))
        rec["verdict"] = ("PASS" if rec["hit_agree"] and rec["stale_agree"] and rec["hash_agree"] and same
                          else "MISMATCH")
        out.append(rec)
        print("%-10s %-9s cache=%dB hit=(%s/%s) stale=(%s/%s) samesize=(%s/%s) hash=%s"
              % (kind, rec["verdict"], rec["cache_bytes"], rec["pin_state_hit"], rec["tool_state_hit"],
                 rec["pin_state_stale"], rec["tool_state_stale"], rec.get("pin_state_samesize"),
                 rec.get("tool_state_samesize"), rec["hash_agree"]))
        os.system("sudo -n rm -rf -- %s >/dev/null 2>&1" % base)
    with open(os.path.join(S, "run", "warm.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("WARM cases=%d pass=%d" % (len(out), sum(1 for r in out if r["verdict"] == "PASS")))
    return out

if __name__ == "__main__":
    only = None
    if "--case" in sys.argv:
        only = sys.argv[sys.argv.index("--case") + 1]
    if "--warm" in sys.argv:
        warm_checks()
    elif "--list" in sys.argv:
        print("\n".join(n for n, _ in CASES))
    else:
        run(only)
