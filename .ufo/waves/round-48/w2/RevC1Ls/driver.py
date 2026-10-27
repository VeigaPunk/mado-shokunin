#!/usr/bin/env python3
"""RevC1Ls - differential: frozen C1 tool's gen_hash vs the real pin's gen_hash (w2 FALSIFY, round 48).

For each seeded tree: build a synthetic XDG config/data hierarchy, force the REAL pin
(xdg-terminal-exec v0.14.3, the frozen sha256) to compute gen_hash in the foreground by leaving a
complete-but-stale cache file, read the hash it reports on its XTE_DEBUG stderr, then ask the frozen
tool (l1-draft/mado-terminal.py) for the hash of the same tree and the same env, and compare.

Attribution on mismatch (all computed, never guessed):
  pin_hash       - the judge, from `D: got fresh hash '<md5>'`
  h_ls_pinops    - md5 over real `LC_ALL=C LANG=C ls -LRl` with the pin's own operand list
  h_ls_toolops   - same real ls but with the tool's operand list  -> isolates operand-list drift
  tool_hash      - the tool's gen_hash
Reproduction: --seed N --keep leaves the tree at <S>/run/trees/N and prints the commands.
"""
import hashlib
import importlib.util
import json
import os
import random
import shutil
import stat
import subprocess
import sys
import time

S = "/fast/scratch/hyaku/mado-r48/RevC1Ls"
RUN = os.path.join(S, "run")
PIN = os.path.join(RUN, "pin", "xdg-terminal-exec")
TOOLP = os.path.join(RUN, "tool", "mado-terminal.py")
TREES = os.path.join(RUN, "trees")
LS = "/usr/bin/ls"
END = "\x1eEND_OF_EXEC_USEP"
sys.dont_write_bytecode = True

spec = importlib.util.spec_from_file_location("mtool", TOOLP)
mtool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mtool)

DESKTOPS = ["Hyprland", "GNOME", "KDE", "sway", "", "Hyprland:GNOME", "sway:Hyprland:GNOME", "hyprland",
            "wlroots:Hyprland", "-n", "-e", "Hyprland\n"]
TERMS = ["foot", "kitty", "alacritty", "wezterm", "ghostty", "xterm", "st", "konsole", "tilix", "urxvt"]
SPICY = ["with space.desktop", "\u00fcmlaut.desktop", "tab\tname.desktop", "quote'name.desktop",
         "dollar$name.desktop", ".hidden.desktop", "UPPER.desktop", "two.dots.desktop",
         "long" + "x" * 36 + ".desktop", "semi;colon.desktop"]
SIX_MONTHS = 31556952 // 2


def pick_mtime(rnd, now):
    """A time far (>= 2 days) from the six-month boundary, in one of four shapes."""
    while True:
        k = rnd.randrange(5)
        if k == 0:
            t = now - rnd.randrange(120, 86400 * 120)          # recent
        elif k == 1:
            t = now - rnd.randrange(86400 * 300, 86400 * 2400)  # old (year form)
        elif k == 2:
            t = now + rnd.randrange(120, 86400 * 40)           # future (year form)
        elif k == 3:
            t = 0                                               # epoch
        else:
            t = now - rnd.randrange(86400 * 150, 86400 * 220)   # just past six months
        if abs((now - t) - SIX_MONTHS) > 86400 * 2:
            return t


def desktop_names(desk):
    low = "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in desk).rstrip("\n")
    if low == "":
        return []
    parts = low.split(":")
    if parts and parts[-1] == "":
        parts.pop()
    return parts


def touch(path, text, rnd, now, mode=None):
    with open(path, "w", encoding="latin-1", errors="surrogateescape") as fh:
        fh.write(text)
    if mode is not None:
        os.chmod(path, mode)
    return path


def appdir_name(rnd):
    r = rnd.random()
    if r < 0.55:
        return rnd.choice(TERMS) + ".desktop"
    if r < 0.75:
        return rnd.choice(SPICY)
    return "x%02d.desktop" % rnd.randrange(100)


def fill_dir(d, rnd, now, root, depth, own, accents):
    """One application directory. Entries exercise every class named in the seat spec."""
    os.makedirs(d, exist_ok=True)
    n = rnd.randrange(0, 6)
    made = []
    names = set()
    for _ in range(n):
        nm = appdir_name(rnd)
        if nm in names:
            continue
        names.add(nm)
        made.append(nm)
    if rnd.random() < 0.35 and ".hidden" not in names:
        made.append(".hidden")
        names.add(".hidden")
    children = []
    for nm in made:
        p = os.path.join(d, nm)
        if nm == ".hidden":
            touch(p, "h\n", rnd, now)
            continue
        k = rnd.random()
        if k < 0.42 or depth >= 3:
            touch(p, "[Desktop Entry]\nName=%s\nExec=%s\nCategories=System;TerminalEmulator;\n"
                  % (nm, nm), rnd, now,
                  mode=rnd.choice((0o644, 0o644, 0o600, 0o755, 0o4755)))
        elif k < 0.60:
            # an empty subdirectory (dir block with "total 0")
            os.makedirs(p, exist_ok=True)
            children.append(p)
        elif k < 0.72:
            # a subdirectory with content, recursed
            os.makedirs(p, exist_ok=True)
            touch(os.path.join(p, "deep.desktop"), "[Desktop Entry]\n", rnd, now)
            children.append(p)
        elif k < 0.80:
            # a hidden-only subdirectory
            os.makedirs(p, exist_ok=True)
            touch(os.path.join(p, ".only"), "x\n", rnd, now)
            children.append(p)
        elif k < 0.88:
            # symlink to a directory in the same block (sibling), sometimes the very same target twice
            tgt = rnd.choice(children) if children else None
            if tgt is None:
                os.makedirs(p + ".t", exist_ok=True)
                tgt = p + ".t"
                children.append(tgt)
            os.symlink(os.path.basename(tgt) if rnd.random() < 0.5 else os.path.relpath(tgt, d), p)
        elif k < 0.94:
            # dangling symlink (entry)
            os.symlink("/nonexistent/mado-%d" % rnd.randrange(1000), p)
        else:
            # symlink to an ancestor -> a loop, or to a file
            if rnd.random() < 0.5 and depth >= 1:
                os.symlink("..", p)
            else:
                os.symlink("/nonexistent/up-%d" % rnd.randrange(100), p)
    if rnd.random() < 0.20:
        try:
            os.mkfifo(os.path.join(d, "pipe.fifo"), 0o644)
        except OSError:
            pass
    if own:
        # numeric-owner padding: an id with no passwd entry next to resolved names
        cand = [os.path.join(d, x) for x in made if os.path.lexists(os.path.join(d, x))]
        rnd.shuffle(cand)
        for p in cand[:rnd.randrange(0, 3)]:
            accents.append(p)
    return children


def build(root, rnd, now):
    """Returns (env, ownpaths)."""
    os.makedirs(root + "/home", exist_ok=True)
    os.makedirs(root + "/cache", exist_ok=True)
    desk = rnd.choice(DESKTOPS)
    desknames = desktop_names(desk)
    cfg = [root + "/cfg"]
    if rnd.random() < 0.55:
        cfg.append(root + "/xdgA")
    if rnd.random() < 0.30:
        cfg += [root + "/xdgB", root + "/xdgC"]
    if rnd.random() < 0.12:
        cfg.append(root + "/cfg")                      # duplicate operand
    sysd = [root + "/usr/share"]
    if rnd.random() < 0.50:
        sysd.append(root + "/usr/local/share")
    if rnd.random() < 0.18:
        sysd.append(root + "/opt/share")
    home_data = root + "/data"
    own = rnd.random() < 0.85
    accents = []
    # config-side list files (may be missing, a dir, or a dangling symlink)
    for d in cfg:
        os.makedirs(d, exist_ok=True)
        for dk in desknames + [None]:
            name = (dk + "-xdg-terminals.list") if dk else "xdg-terminals.list"
            p = os.path.join(d, name)
            if os.path.lexists(p):
                continue
            r = rnd.random()
            if r < 0.55:
                touch(p, "".join("%s.desktop\n" % rnd.choice(TERMS) for _ in range(rnd.randrange(1, 3))),
                      rnd, now, mode=rnd.choice((0o644, 0o600, 0o755)))
            elif r < 0.63:
                os.makedirs(p, exist_ok=True)          # a config operand that is a directory
                touch(os.path.join(p, "inside.desktop"), "[Desktop Entry]\n", rnd, now)
            elif r < 0.70:
                os.symlink("/nonexistent/list-%d" % rnd.randrange(50), p)
    # data-side: xdg-terminal-exec/*.list (configs) and applications/ (hash dirs)
    datadirs = sysd + [home_data]
    for d in datadirs:
        sub = d + "/xdg-terminal-exec"
        os.makedirs(sub, exist_ok=True)
        for dk in desknames + [None]:
            name = (dk + "-xdg-terminals.list") if dk else "xdg-terminals.list"
            p = os.path.join(sub, name)
            if rnd.random() < 0.5:
                touch(p, "%s.desktop\n" % rnd.choice(TERMS), rnd, now)
        fill_dir(d + "/applications", rnd, now, root, 0, own, accents)
    if own:
        accents.append(root + "/cfg/xdg-terminals.list")
        accents.append(root + "/usr/share/xdg-terminal-exec/xdg-terminals.list")
    tz = rnd.choice(("UTC", "UTC", "UTC", "America/Sao_Paulo", "Europe/Berlin", "Asia/Kolkata", "UTC+5:30"))
    env = {"HOME": root + "/home", "PATH": "/usr/bin:/bin", "TZ": tz,
           "XDG_CONFIG_HOME": cfg[0], "XDG_CONFIG_DIRS": ":".join(cfg[1:]) or root + "/xdgEmpty",
           "XDG_DATA_HOME": home_data, "XDG_DATA_DIRS": ":".join(sysd),
           "XDG_CACHE_HOME": root + "/cache"}
    if desk != "":
        env["XDG_CURRENT_DESKTOP"] = desk
    # relative and doubled-slash path shapes
    r = rnd.random()
    if r < 0.08:
        env["XDG_DATA_DIRS"] = "usr/share"                       # relative operand
        env["XDG_DATA_HOME"] = "data"
    elif r < 0.16:
        env["XDG_DATA_DIRS"] = root + "//usr/share"              # doubled slash
    elif r < 0.22:
        env["XDG_CONFIG_DIRS"] = ":" + ":".join(cfg[1:])         # empty element
    return env, accents


def coverage(root, env, pin_ops):
    """What the tree actually exercises (measured on the built tree, not assumed)."""
    c = {"operands": len(pin_ops), "file_ops": 0, "dir_ops": 0, "missing_ops": 0, "dangling_ops": 0,
         "symlink_dir_ops": 0, "dup_ops": 0, "entries": 0, "dangling_entries": 0, "empty_dirs": 0,
         "hidden_only_dirs": 0, "sibling_symlink_dir": 0, "loop_symlink": 0, "fifo": 0,
         "numeric_owner": 0, "uid_only": 0, "gid_only": 0, "recent": 0, "old": 0, "future": 0,
         "setuid_or_sticky": 0, "space_name": 0, "utf8_name": 0, "tab_name": 0, "hidden_entry": 0,
         "relative_op": 0, "double_slash": 0, "empty_elem": 0, "desk_dash": 0, "desk_empty": 0}
    now = time.time()
    seen = set()
    for op in pin_ops:
        if op == "":
            c["empty_elem"] += 1
            continue
        if op in seen:
            c["dup_ops"] += 1
        seen.add(op)
        if not op.startswith("/"):
            c["relative_op"] += 1
        if "//" in op:
            c["double_slash"] += 1
        p = op if op.startswith("/") else os.path.join(root, op)
        if os.path.islink(p) and not os.path.exists(p):
            c["dangling_ops"] += 1
            continue
        if not os.path.exists(p):
            c["missing_ops"] += 1
            continue
        if os.path.isdir(p):
            c["dir_ops"] += 1
            if os.path.islink(p):
                c["symlink_dir_ops"] += 1
        else:
            c["file_ops"] += 1
            st = os.lstat(p)
            if st.st_uid not in (0, 1000) or st.st_gid not in (0, 1000):
                c["numeric_owner"] += 1
                if st.st_uid == 1000:
                    c["gid_only"] += 1
                elif st.st_gid == 1000:
                    c["uid_only"] += 1
            if now - st.st_mtime < 86400 * 100:
                c["recent"] += 1
            if now + 120 < st.st_mtime:
                c["future"] += 1
            if now - st.st_mtime > 86400 * 200:
                c["old"] += 1
    def walk(d, depth=0, ancestors=()):
        try:
            names = sorted(os.listdir(d))
        except OSError:
            return
        kids = 0
        shown = 0
        for n in names:
            if n.startswith("."):
                c["hidden_entry"] += 1
                continue
            shown += 1
            p = os.path.join(d, n)
            c["entries"] += 1
            try:
                st = os.lstat(p)
            except OSError:
                continue
            if " " in n:
                c["space_name"] += 1
            if "\t" in n:
                c["tab_name"] += 1
            if any(ord(ch) > 127 for ch in n):
                c["utf8_name"] += 1
            if st.st_uid not in (0, 1000) or st.st_gid not in (0, 1000):
                c["numeric_owner"] += 1
                if st.st_uid == 1000:
                    c["gid_only"] += 1
                elif st.st_gid == 1000:
                    c["uid_only"] += 1
            if st.st_mode & (stat.S_ISUID | stat.S_ISGID | stat.S_ISVTX):
                c["setuid_or_sticky"] += 1
            if now - st.st_mtime < 86400 * 100:
                c["recent"] += 1
            if now + 120 < st.st_mtime:
                c["future"] += 1
            if now - st.st_mtime > 86400 * 200:
                c["old"] += 1
            if stat.S_ISFIFO(st.st_mode):
                c["fifo"] += 1
            if stat.S_ISLNK(st.st_mode):
                if not os.path.exists(p):
                    c["dangling_entries"] += 1
                    continue
                if os.path.isdir(p):
                    real = os.path.realpath(p)
                    if real in ancestors or real == os.path.realpath(d):
                        c["loop_symlink"] += 1
                    sib = [x for x in names if x != n and os.path.islink(os.path.join(d, x))
                           and os.path.realpath(os.path.join(d, x)) == real]
                    if sib or any(os.path.isdir(os.path.join(d, x)) and not os.path.islink(os.path.join(d, x))
                                  and os.path.realpath(os.path.join(d, x)) == real for x in names if x != n):
                        c["sibling_symlink_dir"] += 1
            if stat.S_ISDIR(st.st_mode):
                kids += 1
                try:
                    sub = [x for x in os.listdir(p)]
                except OSError:
                    sub = []
                if not sub:
                    c["empty_dirs"] += 1
                elif all(x.startswith(".") for x in sub):
                    c["hidden_only_dirs"] += 1
                if depth < 4:
                    walk(p, depth + 1, ancestors + (os.path.realpath(p),))
        if shown == 0:
            c["empty_dirs"] += 1
    for op in pin_ops:
        if op == "":
            continue
        p = op if op.startswith("/") else os.path.join(root, op)
        if op.endswith("/") and os.path.isdir(p) and not os.path.islink(p):
            walk(p, 0, (os.path.realpath(p),))
    dsk = env.get("XDG_CURRENT_DESKTOP")
    if dsk is None or dsk == "":
        c["desk_empty"] = 1
    elif dsk.startswith("-"):
        c["desk_dash"] = 1
    return c


def pin_run(root, env, args=("--print-id",), timeout=30):
    e = dict(env)
    e["XTE_DEBUG"] = "1"
    p = subprocess.run([PIN] + list(args), cwd=root, env=e, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def stale_cache(root):
    os.makedirs(root + "/cache", exist_ok=True)
    p = root + "/cache/xdg-terminal-exec"
    with open(p, "w") as fh:
        fh.write("\n".join(["0" * 32, "foot", "/x/foot.desktop", "foot.desktop", "", "", "", "", "", "",
                            "foot" + END]) + "\n")
    return p


def parse_paths(stderr):
    """The pin's own XTE__CONFIGS / XTE__APPLICATIONS_DIRS (its 'paths:' debug block)."""
    conf = apps = None
    for line in stderr.decode("utf-8", "surrogateescape").split("\n"):
        s = line[3:].lstrip(" ") if line.startswith("D: ") else None
        if s is None:
            continue
        if s.startswith("XTE__CONFIGS="):
            conf = s[len("XTE__CONFIGS="):]
        elif s.startswith("XTE__APPLICATIONS_DIRS="):
            apps = s[len("XTE__APPLICATIONS_DIRS="):]
    return conf, apps


def split_colon(s):
    """bash field splitting of an unquoted expansion with IFS=':' (empty string -> no field)."""
    if s == "":
        return []
    parts = s.split(":")
    if len(parts) > 1 and parts[-1] == "":
        parts.pop()
    return parts


def ls_run(operands, root, env):
    e = {"LC_ALL": "C", "LANG": "C", "PATH": "/usr/bin:/bin", "TZ": env.get("TZ", "UTC"),
         "HOME": env.get("HOME", root)}
    p = subprocess.run([LS, "-LRl"] + list(operands), cwd=root, env=e, stdout=subprocess.PIPE,
                       stderr=subprocess.DEVNULL, timeout=60)
    return p.returncode, p.stdout


def echo_bytes(desk):
    if len(desk) > 1 and desk[0] == "-" and all(c in "neE" for c in desk[1:]):
        return b"" if "n" in desk else b"\n"
    return desk.encode("utf-8", "surrogateescape") + b"\n"


def h_of(desk, listing):
    return hashlib.md5(b"4\n" + echo_bytes(desk) + listing).hexdigest()


def tool_hash(root, env):
    """The frozen tool's gen_hash for this tree/env (process cwd = root, as the sandbox runs it)."""
    old = os.getcwd()
    os.chdir(root)
    try:
        r = mtool.Resolver(dict(env), cwd=root)
        r.select_paths()
        return r.gen_hash(), ":".join(r.configs) + ":" + ":".join(r.app_dirs), None
    except mtool.OutOfContract as ex:
        return None, None, "OOC:%s" % ex
    except mtool.Exit as ex:
        return None, None, "EXIT:%d" % ex.rc
    finally:
        os.chdir(old)


def one(seed, keep=False, quiet=True):
    rnd = random.Random(seed)
    now = int(time.time())
    root = os.path.join(TREES, str(seed), "r")
    if os.path.isdir(os.path.join(TREES, str(seed))):
        subprocess.run(["sudo", "-n", "rm", "-rf", "--", os.path.join(TREES, str(seed))],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.makedirs(root, exist_ok=True)
    env, accents = build(root, rnd, now)
    os.environ["TZ"] = env["TZ"]                 # the tool reads TZ through the C library: same zone as the pin
    time.tzset()
    # mtimes first (deepest-first so setting a parent does not fight a child), then ownership
    allpaths = []
    for base, ds, fs in os.walk(root):
        for nm in fs + ds:
            allpaths.append(os.path.join(base, nm))
    allpaths.append(root)
    rnd.shuffle(allpaths)
    for p in allpaths:
        try:
            os.utime(p, ns=(now * 10 ** 9, pick_mtime(rnd, now) * 10 ** 9), follow_symlinks=False)
        except OSError:
            pass
    for p in allpaths:
        if os.path.isdir(p):
            continue                      # never own a directory: a non-writable dir would block cleanup
        if not os.path.lexists(p):
            continue
        if rnd.random() < 0.25:
            accents.append(p)
    if accents:
        accents = [p for p in accents if os.path.lexists(p)]
        mode = rnd.randrange(3)
        lst = accents[:12]
        for i in range(0, len(lst), 6):
            chunk = lst[i:i + 6]
            spec = ["4242", ":60000", "70000:70000"][mode]
            subprocess.run(["sudo", "-n", "chown", "-h", spec, "--"] + chunk,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    stale_cache(root)
    rc, out, err = pin_run(root, env)
    rec = {"seed": seed, "desk": env.get("XDG_CURRENT_DESKTOP"), "tz": env["TZ"], "pin_rc": rc,
           "pin_stdout": out.decode("latin-1")[:400]}
    pin_hash = None
    for line in err.decode("latin-1").split("\n"):
        if "got fresh hash '" in line:
            pin_hash = line.split("got fresh hash '")[1].split("'")[0]
    rec["pin_hash"] = pin_hash
    conf, apps = parse_paths(err)
    rec["pin_paths"] = {"configs": conf, "apps": apps}
    if pin_hash is None:
        rec["verdict"] = "PIN-NO-HASH"
        rec["pin_stderr"] = err.decode("latin-1")[-1500:]
        return rec
    pin_ops = (split_colon(conf) if conf is not None else []) + (split_colon(apps) if apps is not None else [])
    lsrc, lout = ls_run(pin_ops, root, env)
    rec["real_ls_rc"] = lsrc
    rec["coverage"] = coverage(root, env, pin_ops)
    rec["h_ls_pinops"] = h_of(env.get("XDG_CURRENT_DESKTOP", ""), lout)
    th, tool_ops_s, terr = tool_hash(root, env)
    rec["tool_hash"] = th
    rec["tool_err"] = terr
    if tool_ops_s is not None:
        tool_ops = split_colon(tool_ops_s) if tool_ops_s != "" else []
        rec["tool_ops_match"] = tool_ops == pin_ops
        if pin_ops != tool_ops:
            rec["h_ls_toolops"] = h_of(env.get("XDG_CURRENT_DESKTOP", ""), ls_run(tool_ops, root, env)[1])
        else:
            rec["h_ls_toolops"] = rec["h_ls_pinops"]
    if rec["h_ls_pinops"] != pin_hash:
        rec["verdict"] = "ECHO-MODEL-DIFF"        # my hash reconstruction, not the tool, disagrees
    elif th == pin_hash:
        rec["verdict"] = "PASS"
    else:
        rec["verdict"] = "MISMATCH"
        # attribute: listing emulation vs operand list
        if rec.get("h_ls_toolops") != pin_hash:
            rec["attribute"] = "operand-list"
        else:
            rec["attribute"] = "listing"
        rec["listing_diff"] = diff_lines(lout, pin_ops, root, env, rec)
    if rec["verdict"] != "PASS":
        rec["tree"] = os.path.join(TREES, str(seed), "r")
        rec["env"] = env
    if not keep and rec["verdict"] == "PASS":
        subprocess.run(["sudo", "-n", "rm", "-rf", "--", os.path.join(TREES, str(seed))],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return rec


def diff_lines(real, operands, root, env, rec):
    """First differing line between the real ls and the tool's ls_lRL, with a little context."""
    try:
        old = os.getcwd()
        os.chdir(root)
        try:
            tool = mtool.ls_lRL(operands)
        finally:
            os.chdir(old)
    except mtool.OutOfContract as ex:
        return {"tool_raised": str(ex)}
    a = real.decode("latin-1").split("\n")
    b = tool.decode("latin-1").split("\n")
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            lo = max(0, i - 3)
            return {"line": i + 1, "real": a[lo:i + 4], "tool": b[lo:i + 4],
                    "real_len": len(a), "tool_len": len(b)}
    if len(a) != len(b):
        return {"tail": {"real": a[-4:], "tool": b[-4:]}, "real_len": len(a), "tool_len": len(b)}
    return {}


def main(argv):
    if "--seed" in argv:
        seed = int(argv[argv.index("--seed") + 1])
        rec = one(seed, keep=True)
        rec["repro"] = ("cd %s && XTE_DEBUG=1 %s --print-id   # stale cache already in place" % (TREES + "/" + str(seed) + "/r", PIN))
        print(json.dumps(rec, indent=1)[:12000])
        return 0
    n0 = int(argv[argv.index("--from") + 1]) if "--from" in argv else 1
    n1 = int(argv[argv.index("--to") + 1]) if "--to" in argv else 500
    out = argv[argv.index("--out") + 1] if "--out" in argv else os.path.join(RUN, "results.jsonl")
    t0 = time.time()
    with open(out, "w", encoding="latin-1") as fh:
        counts = {}
        for seed in range(n0, n1 + 1):
            try:
                rec = one(seed)
            except Exception as ex:                     # a harness failure must be visible, not swallowed
                rec = {"seed": seed, "verdict": "HARNESS-ERROR", "error": repr(ex)[:600]}
            counts[rec["verdict"]] = counts.get(rec["verdict"], 0) + 1
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
            if rec["verdict"] != "PASS":
                print("%4d %-16s %s" % (seed, rec["verdict"],
                                        json.dumps({k: rec.get(k) for k in ("attribute", "tool_err", "pin_hash",
                                                                            "tool_hash", "h_ls_pinops")})[:300]))
    print("SUMMARY %s seeds=%d..%d secs=%.1f" % (json.dumps(counts), n0, n1, time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
