#!/usr/bin/env python3
"""mado round 25 C1 counter v2 (frozen before any data seat).

v2 adds the REWRITE case type after the v1 control call (receipts in
../controls/, all `not met` under v1; CtlLabelKeyed's critique showed that an
embedded live table plus a parser for only the counter's own generator grammar
could pass every v1 case without parsing a real config line).

PRED-C1 (same sentence in registration.md, this code and the receipt label):
  At REV, the committed bytes of tools/mado-binds.py, run in a bubblewrap
  sandbox (no network, no /run, cleared environment, HOME = a fresh case
  directory), reproduce the expected bind multiset exactly over all 18
  hyprctl JSON fields for the unperturbed snapshot of the four Hyprland config
  roots and for each of 36 counter-generated cases (4 each of ADD, UNBIND,
  VARIABLE, SOURCE, GLOB, UNSOURCED, COMMENT and REWRITE on that snapshot, and
  4 SYNTH whole synthetic config trees), and the tool bytes contain none of the
  live capture's arg or description strings of 12 or more characters; target:
  cases_pass=37/37 and embed_hits=0.

Expected multisets: the unperturbed case expects the live `hyprctl binds -j`
capture taken immediately before and after the snapshot copy (the two
captures must be equal, else the run is UNSTABLE and exits 2). Each perturbed
case expects that capture plus or minus the delta the counter itself wrote;
a SYNTH case expects exactly the binds of the tree the counter generated. Both
derive from Hyprland v0.56.2 semantics (efb50993: legacy
ConfigManager::handleBind/handleUnbind/parseKey, KeybindManager::
stringToModMask/removeKeybind, HyprCtl bindsRequest JSON fields).

Usage: python3 -I count.py REV [--tool-file PATH] [--seed HEX] [--live-json PATH]
  REV          lane revision whose tools/mado-binds.py is measured.
  --tool-file  score this file instead of REV's tool (controls only; the
               receipt names it and its sha256).
  --seed       replay a run's perturbations (default: fresh os.urandom).
  --live-json  use a saved capture instead of calling hyprctl (replay only;
               the receipt says so).
Exit: 0 TARGET_MET, 1 TARGET_MISSED, 2 setup error / UNSTABLE.
Reads host config bytes and runs `hyprctl binds -j` (read verb) only; writes
only a private temporary directory it removes.
"""
import argparse, collections, hashlib, json, os, random, re, shutil, string, subprocess, sys, tempfile

LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
TOOL_PATH = "tools/mado-binds.py"
FIELDS = ["locked", "mouse", "release", "repeat", "longPress", "non_consuming", "auto_consuming",
          "has_description", "modmask", "submap", "submap_universal", "key", "keycode", "catch_all",
          "description", "allow_input_capture", "dispatcher", "arg"]
ROOTS = [".config/hypr", ".config/omarchy/current/theme", ".local/share/omarchy/default/hypr",
         ".local/state/omarchy/toggles/hypr"]
TYPES = ["ADD", "UNBIND", "VARIABLE", "SOURCE", "GLOB", "UNSOURCED", "COMMENT", "SYNTH", "REWRITE"]
PER_TYPE = 4
MODBITS = [("SHIFT", 1), ("CTRL", 4), ("ALT", 8), ("SUPER", 64)]
KEYS = [c for c in string.ascii_uppercase] + [str(d) for d in range(10)] + ["F%d" % i for i in range(1, 25)] + \
       ["RETURN", "SPACE", "TAB", "ESCAPE", "BACKSPACE", "DELETE", "HOME", "END", "INSERT", "COMMA", "PERIOD",
        "SLASH", "MINUS", "EQUAL", "LEFT", "RIGHT", "UP", "DOWN", "PRINT", "KP_1", "KP_5", "KP_9"]
FLAGSETS = ["", "d", "l", "ld", "eld", "rd", "ed"]
BIND_RE = re.compile(r"^\s*bind[a-z]*\s*=")
SOURCE_RE = re.compile(r"^\s*source\s*=\s*(.+?)\s*$")


def die(msg, code=2):
    print("SETUP_ERROR " + msg)
    sys.exit(code)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def key_of(e):
    return tuple(json.dumps(e.get(f), sort_keys=True) for f in FIELDS)


def live_capture():
    try:
        out = subprocess.run(["timeout", "20", "hyprctl", "binds", "-j"], capture_output=True, check=True).stdout
    except Exception as ex:  # noqa: BLE001
        die("hyprctl binds -j failed: %r" % ex)
    return out


def copy_roots(home_src, home_dst):
    digest = hashlib.sha256()
    nfiles = 0
    for r in ROOTS:
        src = os.path.join(home_src, r)
        if not os.path.exists(src):
            continue
        real = os.path.realpath(src)
        for dp, dn, fn in os.walk(real):
            dn.sort()
            for f in sorted(fn):
                p = os.path.join(dp, f)
                if not os.path.isfile(p) or os.path.getsize(p) > 1 << 20:
                    continue
                rel = os.path.relpath(p, real)
                dst = os.path.join(home_dst, r, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                with open(p, "rb") as fh:
                    b = fh.read()
                with open(dst, "wb") as fh:
                    fh.write(b)
                digest.update((r + "/" + rel).encode() + b"\0" + sha(b).encode() + b"\n")
                nfiles += 1
    return nfiles, digest.hexdigest()


def sourced_files(home):
    """Minimal source-graph walk (glob + ~) used only to choose where perturbations go."""
    import glob
    seen = []

    def walk(pat):
        for f in sorted(glob.glob(pat.replace("~", home, 1) if pat.startswith("~") else pat)):
            if f in seen or not os.path.isfile(f):
                continue
            seen.append(f)
            with open(f, errors="replace") as fh:
                for line in fh:
                    m = SOURCE_RE.match(line.split("#", 1)[0])
                    if m:
                        walk(m.group(1))
    walk(os.path.join(home, ".config/hypr/hyprland.conf"))
    return seen


def mods_str(rng, mask):
    names = [n for n, b in MODBITS if mask & b]
    rng.shuffle(names)
    return " ".join(names)


def entry(flags, mask, key, desc, arg):
    return {"locked": "l" in flags, "mouse": False, "release": "r" in flags, "repeat": "e" in flags,
            "longPress": False, "non_consuming": False, "auto_consuming": False, "has_description": "d" in flags,
            "modmask": mask, "submap": "", "submap_universal": "false", "key": key, "keycode": 0, "catch_all": False,
            "description": desc if "d" in flags else "", "allow_input_capture": False, "dispatcher": "exec", "arg": arg}


class Gen:
    def __init__(self, rng, live):
        self.rng = rng
        self.used = {(e["modmask"], e["key"]) for e in live}

    def tok(self, n=8):
        return "".join(self.rng.choice(string.ascii_lowercase + string.digits) for _ in range(n))

    def bind(self):
        while True:
            mask = 0
            while mask == 0:
                for _, b in MODBITS:
                    if self.rng.random() < 0.5:
                        mask |= b
            key = self.rng.choice(KEYS)
            if (mask, key) not in self.used:
                self.used.add((mask, key))
                break
        flags = self.rng.choice(FLAGSETS)
        desc = self.tok(5).capitalize() + " " + self.tok(6)
        arg = self.rng.choice(["notify-send", "true", "printf", "logger"]) + " " + self.tok(10)
        parts = [mods_str(self.rng, mask), key] + ([desc] if "d" in flags else []) + ["exec", arg]
        return "bind%s = %s" % (flags, ", ".join(parts)), entry(flags, mask, key, desc, arg)


def insert_before_bind(rng, path, lines_to_insert):
    with open(path) as fh:
        lines = fh.read().split("\n")
    idx = [i for i, l in enumerate(lines) if BIND_RE.match(l)]
    i = rng.choice(idx)
    lines[i:i] = lines_to_insert
    with open(path, "w") as fh:
        fh.write("\n".join(lines))


def append(path, lines_to_add):
    with open(path) as fh:
        txt = fh.read()
    if txt and not txt.endswith("\n"):
        txt += "\n"
    with open(path, "w") as fh:
        fh.write(txt + "\n".join(lines_to_add) + "\n")


def perturb(kind, rng, home, live, gen):
    """Apply one perturbation in place; return (description, expected list)."""
    exp = [dict(e) for e in live]
    root = os.path.join(home, ".config/hypr/hyprland.conf")
    files = sourced_files(home)
    bindfiles = [f for f in files if any(BIND_RE.match(l) for l in open(f, errors="replace"))]
    if kind == "ADD":
        f = rng.choice(bindfiles)
        line, e = gen.bind()
        insert_before_bind(rng, f, [line])
        exp.append(e)
        return "ADD into %s" % os.path.relpath(f, home), exp
    if kind == "UNBIND":
        cand = [e for e in live if not e["catch_all"] and not e["mouse"] and (e["key"] or e["keycode"])
                and e["modmask"] & ~sum(b for _, b in MODBITS) == 0]
        t = rng.choice(cand)
        k = t["key"] if t["key"] else "code:%d" % t["keycode"]
        append(root, ["unbind = %s, %s" % (mods_str(rng, t["modmask"]), k)])
        exp = [e for e in exp if not (e["modmask"] == t["modmask"] and e["key"] == t["key"]
                                      and e["keycode"] == t["keycode"] and not e["catch_all"])]
        return "UNBIND mask=%d key=%r keycode=%d" % (t["modmask"], t["key"], t["keycode"]), exp
    if kind == "VARIABLE":
        name = "v" + "".join(rng.choice(string.ascii_lowercase) for _ in range(7))
        val = gen.tok(9)
        line, e = gen.bind()
        tail = gen.tok(4)
        head, _, _ = line.rpartition(", exec, ")
        line = head + ", exec, $%s %s" % (name, tail)
        e["arg"] = "%s %s" % (val, tail)
        with open(root) as fh:
            txt = fh.read()
        with open(root, "w") as fh:
            fh.write("$%s = %s\n" % (name, val) + txt)
        append(root, [line])
        exp.append(e)
        return "VARIABLE $%s" % name, exp
    if kind == "SOURCE":
        fname = gen.tok(8) + ".conf"
        l1, e1 = gen.bind()
        l2, e2 = gen.bind()
        with open(os.path.join(home, ".config/hypr", fname), "w") as fh:
            fh.write(l1 + "\n" + l2 + "\n")
        with open(root) as fh:
            lines = fh.read().split("\n")
        idx = [i for i, l in enumerate(lines) if SOURCE_RE.match(l.split("#", 1)[0])]
        i = rng.choice(idx)
        lines[i:i] = ["source = ~/.config/hypr/" + fname]
        with open(root, "w") as fh:
            fh.write("\n".join(lines))
        exp += [e1, e2]
        return "SOURCE new file at root line %d" % (i + 1), exp
    if kind == "GLOB":
        d = os.path.join(home, ".local/state/omarchy/toggles/hypr")
        os.makedirs(d, exist_ok=True)
        l1, e1 = gen.bind()
        with open(os.path.join(d, gen.tok(8) + ".conf"), "w") as fh:
            fh.write(l1 + "\n")
        exp.append(e1)
        return "GLOB new toggles file", exp
    if kind == "UNSOURCED":
        d = os.path.join(home, ".local/share/omarchy/default/hypr/bindings")
        os.makedirs(d, exist_ok=True)
        l1, _ = gen.bind()
        l2, _ = gen.bind()
        with open(os.path.join(d, gen.tok(8) + ".conf"), "w") as fh:
            fh.write(l1 + "\n" + l2 + "\n")
        return "UNSOURCED new bindings file", exp
    if kind == "COMMENT":
        f = rng.choice(bindfiles)
        l1, _ = gen.bind()
        l2, e2 = gen.bind()
        insert_before_bind(rng, f, ["# " + l1, l2 + " # " + gen.tok(6)])
        exp.append(e2)
        return "COMMENT into %s" % os.path.relpath(f, home), exp
    if kind == "SYNTH":
        return synth(rng, home, gen)
    if kind == "REWRITE":
        return rewrite(rng, home, live, gen, bindfiles, files)
    raise ValueError(kind)


def mod_mask(s):
    """KeybindManager::stringToModMask (v0.56.2): uppercase, then substring tests."""
    s = s.upper()
    m = 0
    for bit, names in ((1, ("SHIFT",)), (2, ("CAPS",)), (4, ("CTRL", "CONTROL")), (8, ("ALT", "MOD1")),
                       (16, ("MOD2",)), (32, ("MOD3",)), (64, ("SUPER", "WIN", "LOGO", "MOD4", "META")),
                       (128, ("MOD5",))):
        if any(n in s for n in names):
            m |= bit
    return m


def key_id(k):
    """parseKey (v0.56.2) -> (key, keycode)."""
    k = k.strip()
    if k.isdigit() and int(k) > 9:
        return "", int(k)
    if k.startswith("code:") and k[5:].isdigit():
        return "", int(k[5:])
    return k, 0


def rewrite(rng, home, live, gen, bindfiles, files):
    """Re-spell every sourced file without changing its meaning (lower-case mod names, whitespace
    around '=' and the first two commas of every bind line, inserted comment lines), then make three
    semantic edits whose vocabulary is copied from the live table: replace the arg of one real bind,
    add one bind, unbind one real bind."""
    exp = [dict(e) for e in live]
    plain = [e for e in live if not e["mouse"] and "#" not in e["arg"] and "$" not in e["arg"]
             and "#" not in e["description"] and "," not in e["description"] and "$" not in e["description"]]
    # locate real bind lines that map to exactly one live entry
    where = collections.defaultdict(list)
    for f in bindfiles:
        for i, l in enumerate(open(f).read().split("\n")):
            if not BIND_RE.match(l):
                continue
            kw, _, val = l.partition("=")
            flags = kw.strip()[4:]
            parts = val.split(",")
            if len(parts) < 3 or "$" in l:
                continue
            k, kc = key_id(parts[1])
            where[(mod_mask(parts[0]), k, kc)].append((f, i, flags))
    cands = []
    for (m, k, kc), locs in where.items():
        hits = [e for e in live if e["modmask"] == m and e["key"] == k and e["keycode"] == kc]
        if len(locs) == 1 and len(hits) == 1 and not set(locs[0][2]) & set("mks") and not hits[0]["mouse"]:
            cands.append(((m, k, kc), locs[0], hits[0]))
    (sm, sk, skc), (sf, si, sflags), starget = rng.choice(cands)
    newarg = rng.choice([e["arg"] for e in plain if e["arg"] and e["arg"] != starget["arg"]])
    lines = open(sf).read().split("\n")
    kw, _, val = lines[si].partition("=")
    nsep = 3 + ("d" in sflags)
    head = val.split(",", nsep)[:nsep]
    lines[si] = kw + "=" + ",".join(head) + ", " + newarg
    with open(sf, "w") as fh:
        fh.write("\n".join(lines))
    for e in exp:
        if e["modmask"] == sm and e["key"] == sk and e["keycode"] == skc:
            e["arg"] = newarg
    # unbind one other real bind
    ucands = [e for e in live if not e["catch_all"] and not e["mouse"] and (e["key"] or e["keycode"])
              and e["modmask"] & ~sum(b for _, b in MODBITS) == 0
              and (e["modmask"], e["key"], e["keycode"]) != (sm, sk, skc)]
    t = rng.choice(ucands)
    append(os.path.join(home, ".config/hypr/hyprland.conf"),
           ["unbind = %s, %s" % (mods_str(rng, t["modmask"]).lower(), t["key"] or "code:%d" % t["keycode"])])
    exp = [e for e in exp if not (e["modmask"] == t["modmask"] and e["key"] == t["key"]
                                  and e["keycode"] == t["keycode"] and not e["catch_all"])]
    # add one bind whose dispatcher, arg and description are copied from the live table
    src = rng.choice([e for e in plain if e["dispatcher"] != "mouse"])
    _, e_new = gen.bind()
    flags = rng.choice(FLAGSETS)
    desc = rng.choice([e["description"] for e in plain if e["description"]] or ["Probe"])
    mask, key = e_new["modmask"], e_new["key"]
    parts = [mods_str(rng, mask), key] + ([desc] if "d" in flags else []) + [src["dispatcher"], src["arg"]]
    e_add = entry(flags, mask, key, desc, src["arg"])
    e_add["dispatcher"] = src["dispatcher"]
    insert_before_bind(rng, rng.choice(bindfiles), ["bind%s = %s" % (flags, ", ".join(parts))])
    exp.append(e_add)
    # meaning-preserving re-spelling of every sourced file
    for f in files:
        out = []
        for l in open(f, errors="replace").read().split("\n"):
            if BIND_RE.match(l) or re.match(r"^\s*unbind\s*=", l):
                kw, _, val = l.partition("=")
                parts = val.split(",", 2)
                if len(parts) == 3:
                    mods = " ".join(w if w.startswith("$") else w.lower() for w in parts[0].split())
                    sep = [rng.choice([",", ", ", " , ", ",   "]) for _ in range(2)]
                    l = kw.rstrip() + rng.choice(["=", " = ", "  =   ", "= "]) + mods + sep[0] + \
                        parts[1].strip() + sep[1] + parts[2].lstrip()
            out.append(l)
            if rng.random() < 0.08:
                out.append("# " + gen.tok(5) + " " + gen.tok(7))
        with open(f, "w") as fh:
            fh.write("\n".join(out))
    return "REWRITE argswap mask=%d key=%r code=%d; unbind mask=%d key=%r code=%d; add %s" % (
        sm, sk, skc, t["modmask"], t["key"], t["keycode"], src["dispatcher"]), exp


def synth(rng, home, gen):
    """Replace the snapshot with a whole synthetic config tree whose bind table the counter knows."""
    shutil.rmtree(home)
    hyp = os.path.join(home, ".config/hypr")
    os.makedirs(os.path.join(hyp, "d"))
    exp = []
    variables = {}
    for _ in range(rng.randint(2, 3)):
        variables["s" + "".join(rng.choice(string.ascii_lowercase) for _ in range(7))] = gen.tok(9)

    def some_binds(n, allow_vars):
        out = []
        for _ in range(n):
            line, e = gen.bind()
            r = rng.random()
            if allow_vars and r < 0.35:
                name = rng.choice(sorted(variables))
                tail = gen.tok(4)
                head, _, _ = line.rpartition(", exec, ")
                line = head + ", exec, $%s %s" % (name, tail)
                e["arg"] = "%s %s" % (variables[name], tail)
            elif r < 0.55:
                line += " # " + gen.tok(5)
            out.append(line)
            exp.append(e)
        return out

    root = ["# %s %s" % (gen.tok(5), gen.tok(7))]
    root += ["$%s = %s" % (k, v) for k, v in variables.items()]
    root += ["", "general {", "    gaps_in = %d" % rng.randint(1, 9), "    border_size = 2", "}", ""]
    first = some_binds(rng.randint(3, 6), True)
    target = exp[-len(first)]
    root += first
    root += ["# " + gen.bind()[0]]
    root += ["source = ~/.config/hypr/a.conf", "source = ~/.config/hypr/d/*.conf"]
    root += some_binds(rng.randint(2, 4), True)
    root.append("unbind = %s, %s" % (mods_str(rng, target["modmask"]), target["key"]))
    exp.remove(target)
    with open(os.path.join(hyp, "hyprland.conf"), "w") as fh:
        fh.write("\n".join(root) + "\n")
    with open(os.path.join(hyp, "a.conf"), "w") as fh:
        fh.write("\n".join(some_binds(rng.randint(3, 5), True)) + "\n")
    for n in ("x", "y"):
        with open(os.path.join(hyp, "d", n + ".conf"), "w") as fh:
            fh.write("\n".join(some_binds(rng.randint(1, 2), True)) + "\n")
    n_before = len(exp)
    with open(os.path.join(hyp, "u.conf"), "w") as fh:
        fh.write("\n".join(some_binds(2, False)) + "\n")
    del exp[n_before:]
    return "SYNTH tree binds=%d unbound=1 vars=%d" % (len(exp), len(variables)), exp


def run_tool(tool, home):
    cmd = ["timeout", "60", "bwrap", "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib",
           "--symlink", "usr/lib64", "/lib64", "--symlink", "usr/bin", "/bin", "--proc", "/proc", "--dev", "/dev",
           "--tmpfs", "/tmp", "--ro-bind", home, "/snap/home", "--ro-bind", tool, "/snap/tool.py",
           "--unshare-all", "--die-with-parent", "--clearenv", "--setenv", "PATH", "/usr/bin",
           "--setenv", "HOME", "/snap/home", "python3", "-I", "/snap/tool.py", "--home", "/snap/home"]
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        return None, "exit=%d stderr=%s" % (p.returncode, p.stderr.decode(errors="replace")[-200:].replace("\n", " | "))
    try:
        data = json.loads(p.stdout)
        assert isinstance(data, list) and all(isinstance(e, dict) for e in data)
    except Exception:  # noqa: BLE001
        return None, "stdout is not a JSON array of objects"
    return data, ""


def compare(got, exp):
    g = collections.Counter(key_of(e) for e in got)
    x = collections.Counter(key_of(e) for e in exp)
    missing = x - g
    extra = g - x
    return sum(missing.values()), sum(extra.values()), missing, extra


def brief(k):
    d = dict(zip(FIELDS, k))
    return "mask=%s key=%s code=%s disp=%s arg=%s" % (d["modmask"], d["key"], d["keycode"], d["dispatcher"], d["arg"][:50])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--tool-file")
    ap.add_argument("--seed")
    ap.add_argument("--live-json")
    a = ap.parse_args()
    rev = subprocess.run(["git", "-C", LANE, "rev-parse", "--verify", a.rev + "^{commit}"], capture_output=True, text=True)
    if rev.returncode != 0:
        die("bad REV %s" % a.rev)
    rev = rev.stdout.strip()
    me = open(os.path.abspath(__file__), "rb").read()
    print("counter sha256:%s rev=%s" % (sha(me), rev))
    tmp = tempfile.mkdtemp(prefix="mado-r25-c1-")
    try:
        tool = os.path.join(tmp, "tool.py")
        if a.tool_file:
            tb = open(a.tool_file, "rb").read()
            print("tool=override:%s sha256:%s" % (a.tool_file, sha(tb)))
        else:
            p = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, TOOL_PATH)], capture_output=True)
            if p.returncode != 0:
                print("tool=MISSING_TOOL at %s" % rev)
                tb = None
            else:
                tb = p.stdout
                print("tool=%s@%s sha256:%s" % (TOOL_PATH, rev[:12], sha(tb)))
        if tb is not None:
            with open(tool, "wb") as fh:
                fh.write(tb)
        seed = a.seed or os.urandom(8).hex()
        print("seed=%s" % seed)
        snap0 = os.path.join(tmp, "snap0")
        if a.live_json:
            raw1 = open(a.live_json, "rb").read()
            nfiles, digest = copy_roots(os.path.expanduser("~"), snap0)
            print("live=replay:%s sha256:%s" % (a.live_json, sha(raw1)))
        else:
            raw1 = live_capture()
            nfiles, digest = copy_roots(os.path.expanduser("~"), snap0)
            raw2 = live_capture()
            if raw1 != raw2:
                die("UNSTABLE live capture changed during snapshot", 2)
            print("live=hyprctl binds -j sha256:%s" % sha(raw1))
        live = json.loads(raw1)
        print("snapshot files=%d digest sha256:%s live_binds=%d" % (nfiles, digest, len(live)))
        embed_hits = 0
        if tb is not None:
            text = tb.decode("utf-8", errors="replace")
            strs = {e[f] for e in live for f in ("arg", "description") if isinstance(e[f], str) and len(e[f]) >= 12}
            hits = sorted(s for s in strs if s in text)
            embed_hits = len(hits)
            for s in hits[:5]:
                print("EMBED_HIT %r" % s[:60])
        cases = [("BASE", None)] + [(t, i) for t in TYPES for i in range(PER_TYPE)]
        rng = random.Random(int(seed, 16))
        gen = Gen(rng, live)
        npass = 0
        for kind, i in cases:
            home = os.path.join(tmp, "case")
            if os.path.exists(home):
                shutil.rmtree(home)
            shutil.copytree(snap0, home, symlinks=False)
            if kind == "BASE":
                desc, exp = "unperturbed", [dict(e) for e in live]
            else:
                desc, exp = perturb(kind, rng, home, live, gen)
            label = "%s%s" % (kind, "" if i is None else "-%d" % i)
            if tb is None:
                print("CASE %-12s FAIL tool absent (%s)" % (label, desc))
                continue
            got, err = run_tool(tool, home)
            if got is None:
                print("CASE %-12s FAIL %s (%s)" % (label, err, desc))
                continue
            nm, ne, missing, extra = compare(got, exp)
            ok = nm == 0 and ne == 0
            npass += ok
            print("CASE %-12s %s missing=%d extra=%d (%s)" % (label, "PASS" if ok else "FAIL", nm, ne, desc))
            for k in list(missing)[:2]:
                print("    missing " + brief(k))
            for k in list(extra)[:2]:
                print("    extra   " + brief(k))
        met = npass == len(cases) and embed_hits == 0
        print("PRED-C1 cases_pass=%d/%d embed_hits=%d verdict=%s" % (npass, len(cases), embed_hits,
                                                                    "TARGET_MET" if met else "TARGET_MISSED"))
        return 0 if met else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
