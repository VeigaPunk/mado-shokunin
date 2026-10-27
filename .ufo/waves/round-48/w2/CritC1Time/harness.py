#!/usr/bin/env python3
"""CritC1Time: real pin vs frozen tool over explicit file/dir mtimes (cache hash date boundaries).

Read-only against the lane; writes only under S (this scratch) and OUT (the seat evidence dir).
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
TOOLP = LANE + "/.ufo/waves/round-48/l1-draft/mado-terminal.py"
PIN = "/usr/bin/xdg-terminal-exec"
S = "/fast/scratch/hyaku/mado-r48/CritC1Time"
OUT = LANE + "/.ufo/waves/round-48/w2/CritC1Time"
LS = "/usr/bin/ls"
SIX = 31556952 // 2

spec = importlib.util.spec_from_file_location("madoterm", TOOLP)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

LIST_TEXT = "foot.desktop\n"
DESKTOP = b"[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=foot --a\n"
DESKTOP_SAME_SIZE = b"[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=fool --a\n"   # same byte count, different command word
STUB = b"#!/bin/sh\nexit 1\n"


def build_tree(root):
    for d in ("cd", "usr/share/applications", "bin", "home/.config", "home/.local/share", ".rw/cache"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    with open(os.path.join(root, "cd/xdg-terminals.list"), "w") as fh:
        fh.write(LIST_TEXT)
    p = os.path.join(root, "usr/share/applications/foot.desktop")
    with open(p, "wb") as fh:
        fh.write(DESKTOP)
    p = os.path.join(root, "bin/foot")
    with open(p, "wb") as fh:
        fh.write(STUB)
    os.chmod(p, 0o755)


def env_for(root, tz, cache):
    return {"HOME": root + "/home", "PATH": root + "/bin:/usr/bin:/bin",
            "XDG_CONFIG_DIRS": root + "/cd", "XDG_CONFIG_HOME": root + "/home/.config",
            "XDG_DATA_DIRS": root + "/usr/share", "XDG_DATA_HOME": root + "/home/.local/share",
            "XDG_CACHE_HOME": cache, "XDG_CURRENT_DESKTOP": "Hyprland", "TZ": tz,
            "LC_ALL": "C", "LANG": "C"}


def set_times(root, t, dir_t=None):
    """Explicit mtimes: every file and the applications dir (dir_t defaults to t)."""
    files, dirs = [], []
    for d, ds, fs in os.walk(root):
        rel = os.path.relpath(d, root).split(os.sep)[0]
        if rel == ".rw":
            ds[:] = []
            continue
        for f in fs:
            files.append(os.path.join(d, f))
        for x in ds:
            if os.path.relpath(os.path.join(d, x), root).split(os.sep)[0] != ".rw":
                dirs.append(os.path.join(d, x))
    for p in files:
        os.utime(p, (t, t))
    for p in dirs:
        os.utime(p, (dir_t if dir_t is not None else t,) * 2)


def wait_cache(cache):
    """Wait for the resolver's background save to terminate, bounded."""
    p = os.path.join(cache, "xdg-terminal-exec")
    for _ in range(400):
        try:
            txt = open(p, "rb").read().decode("utf-8", "surrogateescape")
        except OSError:
            time.sleep(0.01)
            continue
        if "END_OF_EXEC_USEP" in txt:
            return txt
        time.sleep(0.01)
    return None


def pin_run(root, tz, cache, args=("--print-cmd",)):
    shutil.rmtree(cache, ignore_errors=True)
    os.makedirs(cache, exist_ok=True)
    env = env_for(root, tz, cache)
    env["XTE_DEBUG"] = "1"
    r = subprocess.run([PIN, *args], env=env, capture_output=True, timeout=60)
    txt = wait_cache(cache)
    return r, txt


def ls_real(ops, tz):
    env = {"LC_ALL": "C", "LANG": "C", "TZ": tz, "PATH": "/usr/bin:/bin"}
    r = subprocess.run([LS, "-LRl", *ops], env=env, capture_output=True, timeout=60)
    return r.stdout


def datecol(line):
    """The date column of an `ls -l` row (text after the size/rdev field)."""
    parts = line.split()
    if len(parts) < 9:
        return "?"
    return " ".join(parts[5:8])


def tool_listing(ops, now_ns):
    try:
        return mod.ls_lRL(ops, now_ns=now_ns), None
    except mod.OutOfContract as ex:
        return None, "OutOfContract: %s" % ex


def shell_hash(desktop, listing):
    return hashlib.md5(b"4\n" + desktop.encode() + b"\n" + listing).hexdigest()


def regime(root, tz, label, snap, dir_t=None, ops=None):
    """Apply mtimes `snap(t)` then measure real ls, the tool listing and the pin's cache hash."""
    cache = root + "/.rw/cache"
    t, extra = snap()
    set_times(root, t, dir_t)
    ns_real = time.time_ns()
    real = ls_real(ops, tz)
    ns_tool = time.time_ns()
    tl, exc = tool_listing(ops, ns_tool)
    pr, ptext = pin_run(root, tz, cache)
    pin_hash = (ptext or "").split("\n")[0] if ptext else None
    row = {"regime": label, "tz": tz, "mtime": t, "now_ns_real": ns_real, "now_ns_tool": ns_tool,
           "pin_hash": pin_hash, "pin_rc": pr.returncode,
           "pin_stdout": pr.stdout.decode("utf-8", "surrogateescape").strip(),
           "real_hash_replay": shell_hash("Hyprland", real),
           "tool_hash": None if tl is None else shell_hash("Hyprland", tl),
           "tool_exc": exc, "extra": extra}
    row["hash_equal"] = (row["pin_hash"] is not None and row["pin_hash"] == row["tool_hash"])
    row["replay_matches_pin"] = row["pin_hash"] == row["real_hash_replay"]
    row["listing_equal"] = (tl is not None and tl == real)
    # date columns: the list file (command-line file operand) and the desktop file inside the app dir
    def cols(b):
        d = {}
        if b is None:
            return d
        for ln in b.decode("utf-8", "surrogateescape").split("\n"):
            if ln.endswith("cd/xdg-terminals.list"):
                d["listfile"] = datecol(ln)
            elif ln.endswith("applications/foot.desktop"):
                d["desktop"] = datecol(ln)
        return d
    row["real_dates"] = cols(real)
    row["tool_dates"] = cols(tl)
    # end-to-end: does the tool read the pin's own freshly written cache as a hit?
    env = env_for(root, tz, cache)
    r = subprocess.run([sys.executable, "-I", TOOLP, "explain"], env=env, capture_output=True, timeout=60)
    line = [l for l in r.stdout.decode("utf-8", "surrogateescape").split("\n") if l.startswith("MADO_TERM: ")]
    row["tool_explain"] = line[-1] if line else ("rc=%d err=%s" % (r.returncode, r.stderr.decode()[:200]))
    if row["pin_hash"] is None:
        row["diff_head"] = None
        return row
    if tl is None:
        row["diff_head"] = "tool refused; real ls date=%r" % (row["real_dates"],)
        return row
    if tl != real:
        a = real.decode("utf-8", "surrogateescape").split("\n")
        b = tl.decode("utf-8", "surrogateescape").split("\n")
        import difflib
        row["diff_head"] = "\n".join(list(difflib.unified_diff(a, b, "real-ls", "tool", lineterm=""))[:14])
    else:
        row["diff_head"] = None
    return row


def main():
    tz = sys.argv[1]
    out = []
    ops = None
    root = os.path.join(S, "tree-" + tz.replace("/", "_"))
    shutil.rmtree(root, ignore_errors=True)
    build_tree(root)
    # discover the operand list the pin hashes (its own XTE_DEBUG 'paths:' line)
    cache = root + "/.rw/cache"
    r, _txt = pin_run(root, tz, cache)
    dbg = r.stderr.decode("utf-8", "surrogateescape")
    conf = apps = None
    for ln in dbg.split("\n"):
        if "XTE__CONFIGS=" in ln:
            conf = ln.split("XTE__CONFIGS=")[1].split("  XTE__APPLICATIONS_DIRS=")[0]
        if "XTE__APPLICATIONS_DIRS=" in ln:
            apps = ln.split("XTE__APPLICATIONS_DIRS=")[1].strip()
    ops = conf.split(":") + apps.split(":")
    receipt = {"tz": tz, "operands": ops, "pin_paths_debug": [l for l in dbg.split("\n") if "paths:" in l or "XTE__CONFIGS=" in l]}
    regs = [
        ("now", lambda: (time.time_ns() // 1000000000, "")),
        ("now-1s", lambda: (time.time_ns() // 1000000000 - 1, "")),
        ("now-30s", lambda: (time.time_ns() // 1000000000 - 30, "")),
        ("sixmo+1s(recent side)", lambda: (time.time_ns() // 1000000000 - SIX + 1, "")),
        ("sixmo exact", lambda: (time.time_ns() // 1000000000 - SIX, "")),
        ("sixmo-1s(old side)", lambda: (time.time_ns() // 1000000000 - SIX - 1, "")),
        ("future+1s", lambda: (time.time_ns() // 1000000000 + 1, "")),
        ("future+1h", lambda: (time.time_ns() // 1000000000 + 3600, "")),
        ("2020-01-01", lambda: (1577836800, "")),
        ("2020+dir-1d", lambda: (1600000000, "1600086400")),
    ]
    rows = []
    for label, snap in regs:
        dt = None
        if label == "2020+dir-1d":
            rows.append(regime(root, tz, label, snap, dir_t=1600086400, ops=ops))
        else:
            rows.append(regime(root, tz, label, snap, ops=ops))
    # same-minute same-size edit (real clock): tree at now-k with the same minute as now
    tzrow = same_minute(root, tz, ops, same_minute=True)
    rows.append(tzrow)
    rows.append(same_minute(root, tz, ops, same_minute=False))
    # dir mtimes: same file mtimes, dir mtimes one day apart - does the hash move?
    set_times(root, 1600000000, 1600000000)
    r1, t1 = pin_run(root, tz, cache)
    set_times(root, 1600000000, 1600086400)
    ns_a = time.time_ns()
    real_a = ls_real(ops, tz)
    ns_b = time.time_ns()
    tl_b, exc_b = tool_listing(ops, ns_b)
    r2, t2 = pin_run(root, tz, cache)
    receipt["dir_mtime_pair"] = {
        "files": 1600000000,
        "pin_hash_dirs_1600000000": (t1 or "").split("\n")[0],
        "pin_hash_dirs_1600086400": (t2 or "").split("\n")[0],
        "real_listing_equal_across_dir_mtimes": real_a == ls_real(ops, tz),
        "real_hash_replay_1600086400": shell_hash("Hyprland", real_a),
        "tool_hash_1600086400": None if tl_b is None else shell_hash("Hyprland", tl_b),
        "tool_exc": exc_b,
        "dir_mtime_visible": (t1 or "").split("\n")[0] != (t2 or "").split("\n")[0],
    }
    receipt["rows"] = rows
    with open(os.path.join(S, "matrix-%s.json" % tz.replace("/", "_")), "w") as fh:
        json.dump(receipt, fh, indent=1)
    for row in rows:
        print(json.dumps(row, sort_keys=True))


def same_minute(root, tz, ops, same_minute):
    """Prime at a recent mtime, then a same-size edit; does the hash move exactly when the date string does?"""
    cache = root + "/.rw/cache"
    now = time.time_ns() // 1000000000
    if same_minute:
        # newest whole second in this minute, at least 3 s old
        t = now - 3 if now % 60 >= 3 else now - (now % 60) - 3
    else:
        t = now - 60 - (now % 60)          # previous minute
    set_times(root, t)
    r, ptext = pin_run(root, tz, cache, args=("--print-cmd",))
    before = (ptext or "").split("\n")[0]
    # same-size edit: Exec=foot -> Exec=fool (identical byte count)
    with open(os.path.join(root, "usr/share/applications/foot.desktop"), "wb") as fh:
        fh.write(DESKTOP_SAME_SIZE)
    os.utime(os.path.join(root, "usr/share/applications/foot.desktop"), (now, now))
    env = env_for(root, tz, cache)
    env["XTE_DEBUG"] = "1"
    r2 = subprocess.run([PIN, "--print-cmd"], env=env, capture_output=True, timeout=60)
    err = r2.stderr.decode("utf-8", "surrogateescape")
    state = ("cache is actual" if "cache is actual" in err else
             "cache is out-of-date" if "cache is out-of-date" in err else "other")
    fresh = [l for l in err.split("\n") if "got fresh hash" in l]
    te = subprocess.run([sys.executable, "-I", TOOLP, "explain"], env=env_for(root, tz, cache),
                        capture_output=True, timeout=60)
    line = [l for l in te.stdout.decode("utf-8", "surrogateescape").split("\n") if l.startswith("MADO_TERM: ")]
    d_before = time.strftime("%b %e %H:%M", time.localtime(t))
    d_after = time.strftime("%b %e %H:%M", time.localtime(now))
    return {"regime": "same-minute-edit" if same_minute else "cross-minute-edit", "tz": tz,
            "mtime": t, "now_ns_real": time.time_ns(), "now_ns_tool": time.time_ns(),
            "pin_hash": before, "pin_rc": r.returncode,
            "pin_stdout": r.stdout.decode().strip(), "real_hash_replay": None,
            "tool_hash": None, "tool_exc": None, "hash_equal": None, "replay_matches_pin": None,
            "listing_equal": None,
            "real_dates": {"before": d_before, "after": d_after},
            "tool_dates": {}, "extra": {"pin_state_after_edit": state, "pin_stdout_after_edit": r2.stdout.decode().strip(),
                                        "same_minute_string": d_before == d_after,
                                        "fresh_hash_after_edit": fresh[:1]},
            "tool_explain": line[-1] if line else te.stderr.decode()[:200], "diff_head": None}


if __name__ == "__main__":
    main()
