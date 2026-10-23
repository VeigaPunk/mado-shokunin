#!/usr/bin/env python3
"""mado round 25 C1 counter v3 (frozen before any v3-scoring seat and before any data seat).

v2 added the REWRITE case type after the v1 control call (receipts in
../controls/, all `not met` under v1; CtlLabelKeyed's critique showed that an
embedded live table plus a parser for only the counter's own generator grammar
could pass every v1 case without parsing a real config line).
v3 (attempt 2, before any seat scored v2) adds the HARD case type: an encoded
cache of the snapshot's normalized lines plus a parser for the easy grammar
could still pass every v2 case, because every v2 edit of real lines is
parsable with the easy grammar and SYNTH used only the easy grammar. HARD
trees put the hard grammar (modifier aliases, keycodes, mouse binds, flag
combinations, dispatcher case, comma-bearing args, variables in every field,
rejected lines, case-sensitive unbind) into fresh random lines, so no cache
of the operator's lines helps. v3 also checks its own line model against the
live table before scoring (MODEL_CHECK; drift exits 2).

PRED-C1 (same sentence in registration.md, this code and the receipt label):
  At REV, the committed bytes of tools/mado-binds.py, run in a bubblewrap
  sandbox (no network, no /run, cleared environment, HOME = a fresh case
  directory), reproduce the expected bind multiset exactly over all 18
  hyprctl JSON fields for the unperturbed snapshot of the four Hyprland config
  roots and for each of 40 counter-generated cases (4 each of ADD, UNBIND,
  VARIABLE, SOURCE, GLOB, UNSOURCED, COMMENT and REWRITE on that snapshot,
  4 SYNTH whole synthetic config trees, and 4 HARD whole synthetic trees whose
  lines exercise modifier aliases, keycodes, mouse binds, flag combinations,
  dispatcher case, comma-bearing args, variables and rejected lines), and the
  tool bytes contain none of the live capture's arg or description strings of
  12 or more characters; target: cases_pass=41/41 and embed_hits=0.

Expected multisets: the unperturbed case expects the live `hyprctl binds -j`
capture taken immediately before and after the snapshot copy (the two
captures must be equal, else the run is UNSTABLE and exits 2). Each perturbed
case expects that capture plus or minus the delta the counter itself wrote;
a SYNTH or HARD case expects exactly the binds of the tree the counter
generated. All derive from Hyprland v0.56.2 semantics (efb50993: legacy
ConfigManager::handleBind :1492-1655 / handleUnbind :1657-1674 / parseKey
:1481-1490, KeybindManager::stringToModMask :221-242 / removeKeybind
:197-202, HyprCtl bindsRequest :1026-1080 JSON fields; hyprutils a21e87b8
CVarList). The HARD line model (line_entry) must reproduce, for every
modelable real bind line of the snapshot, an entry present in the live
capture (MODEL_CHECK), else the run exits 2 and measures nothing.

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
TYPES = ["ADD", "UNBIND", "VARIABLE", "SOURCE", "GLOB", "UNSOURCED", "COMMENT", "SYNTH", "REWRITE", "HARD"]
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
    if kind == "HARD":
        return hard(rng, home, live, gen)
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


# ---- v3: the hard bind grammar (legacy ConfigManager::handleBind, v0.56.2 efb50993 :1492-1655) ----
WS = " \t\n\r\f\v"
VALID_FLAGS = set("lremnatisodpcgukx")
MOD_ALIASES = {1: ["SHIFT", "shift", "Shift"], 4: ["CTRL", "CONTROL", "ctrl", "Control"], 8: ["ALT", "MOD1", "alt"],
               64: ["SUPER", "WIN", "LOGO", "MOD4", "META", "super", "win"]}


def varlist(s, last=0):
    """hyprutils CVarList(in, lastArgNo, ',', removeEmpty=false) (a21e87b8): split, trim each field; field
    number lastArgNo takes the rest of the string."""
    if s == "":
        return [""]
    out, pos = [], 0
    for idx, p in enumerate(s.split(","), 1):
        if idx == last:
            out.append(s[pos:].strip(WS))
            break
        pos += len(p) + 1
        out.append(p.strip(WS))
    return out


def parse_key(k):
    """parseKey :1481-1490 -> (key, keycode, catch_all)."""
    if k.isascii() and k.isdigit() and int(k) > 9:
        return "", int(k), False
    if k.startswith("code:") and k[5:].isascii() and k[5:].isdigit():
        return "", int(k[5:]), False
    if k == "catchall":
        return "", 0, True
    return k, 0, False


def line_entry(kw, val, dispatchers):
    """One expanded, comment-free bind line -> hyprctl entry, None when Hyprland rejects it (outside a submap),
    "UNMODELED" for the s/k flags (multi-key, per-device), which neither the snapshot nor HARD uses."""
    flags = kw.strip(WS)[4:]
    if any(c not in VALID_FLAGS for c in flags):
        return None
    f = set(flags)
    if f & set("sk"):
        return "UNMODELED"
    rel, rep, lp, mouse = bool(f & set("rcg")), "e" in f, "o" in f, "m" in f
    if (lp or rel) and rep:
        return None
    if mouse and (rep or rel or "l" in f):
        return None
    if "c" in f and "g" in f:
        return None
    dd = 1 if "d" in f else 0
    args = varlist(val, 4 + dd)
    if len(args) < 3 or (not mouse and len(args) > 4 + dd) or (mouse and len(args) > 3 + dd):
        return None
    at = lambda i: args[i] if i < len(args) else ""  # noqa: E731  CVarList::operator[] returns "" past the end
    mod, modstr, key = mod_mask(args[0]), args[0], args[1]
    desc = at(2) if dd else ""
    handler = at(2 + dd)
    command = handler if mouse else at(3 + dd)
    if mouse:
        handler = "mouse"
    handler = handler.lower()
    if handler not in dispatchers or (mod == 0 and modstr != "") or key == "":
        return None
    k, kc, ca = parse_key(key)
    if ca:
        return None  # catchall is only allowed inside a submap
    return {"locked": "l" in f, "mouse": mouse, "release": rel, "repeat": rep, "longPress": lp,
            "non_consuming": "n" in f, "auto_consuming": "a" in f, "has_description": bool(dd), "modmask": mod,
            "submap": "", "submap_universal": "true" if "u" in f else "false", "key": k, "keycode": kc,
            "catch_all": False, "description": desc, "allow_input_capture": "x" in f, "dispatcher": handler,
            "arg": command}


def unbind_apply(exp, val):
    """handleUnbind :1657-1674 + removeKeybind :197-202 (exact key string, keycode, catch_all)."""
    args = varlist(val)
    if len(args) == 1 and args[0] == "all":
        exp.clear()
        return
    mod = mod_mask(args[0])
    k, kc, ca = parse_key(args[1] if len(args) > 1 else "")
    exp[:] = [e for e in exp if not (e["modmask"] == mod and e["key"] == k and e["keycode"] == kc
                                     and e["catch_all"] == ca)]


def model_check(snap, live):
    """Run line_entry over every real bind line of the snapshot whose only '$' is '$(' and with no '##';
    every modeled entry must be in the live capture (multiset containment) and none may be rejected."""
    dispatchers = {e["dispatcher"] for e in live} | {"mouse"}
    pool = collections.Counter(key_of(e) for e in live)
    modeled = bad = 0
    for f in sourced_files(snap):
        for l in open(f, errors="replace").read().split("\n"):
            if not BIND_RE.match(l) or "##" in l:
                continue
            l = l.split("#", 1)[0]
            if re.search(r"\$(?!\()", l):
                continue
            kw, _, val = l.partition("=")
            e = line_entry(kw, val.strip(WS), dispatchers)
            modeled += 1
            if not isinstance(e, dict) or pool[key_of(e)] == 0:
                bad += 1
                if bad <= 3:
                    print("MODEL_DRIFT %r -> %r" % (l[:90], e if not isinstance(e, dict) else brief(key_of(e))))
                continue
            pool[key_of(e)] -= 1
    return modeled, bad


def spell_mods(rng, mask):
    names = [rng.choice(MOD_ALIASES[b]) for b in (1, 4, 8, 64) if mask & b]
    rng.shuffle(names)
    return rng.choice([" ", "_", "  "]).join(names)


def hard(rng, home, live, gen):
    """Replace the snapshot with a whole synthetic tree written in the hard grammar; expected = line_entry
    over the tree in Hyprland's processing order (root lines, each `source` inline, globs sorted)."""
    shutil.rmtree(home)
    hyp = os.path.join(home, ".config/hypr")
    os.makedirs(os.path.join(hyp, "d"))
    disps = sorted({e["dispatcher"] for e in live} - {"mouse"})
    dispatchers = set(disps) | {"mouse"}
    variables = {}

    def newvar(value):
        name = "h" + "".join(rng.choice(string.ascii_lowercase) for _ in range(7))
        variables[name] = value
        return name

    v_mods = newvar(spell_mods(rng, rng.choice([64, 65, 68, 72, 73])))
    v_disp = newvar(rng.choice(["exec", "Exec", "EXEC"]))
    v_arg = newvar(rng.choice(["notify-send", "printf", "logger"]) + " " + gen.tok(5) + "," + gen.tok(3))
    v_desc = newvar(gen.tok(4).capitalize() + " " + gen.tok(5))

    def expand(s):
        for n in sorted(variables, key=len, reverse=True):
            s = s.replace("$" + n, variables[n])
        return s

    def pad(s):
        return rng.choice(["", " ", "  "]) + s + rng.choice(["", " ", "   "])

    def mods_text(mask):
        if mask == 0:
            return ""
        if rng.random() < 0.15:
            return "$" + v_mods
        return spell_mods(rng, mask)

    def key_text():
        r = rng.random()
        if r < 0.45:
            return rng.choice(KEYS)
        if r < 0.65:
            return "code:%d" % rng.randint(10, 250)
        if r < 0.8:
            return "%d" % rng.randint(10, 250)
        if r < 0.9:
            return "%d" % rng.randint(0, 9)
        return rng.choice(["mouse_down", "mouse_up", "mouse:274"])

    def arg_for(d):
        if d == "exec":
            parts = [rng.choice(["notify-send", "uwsm-app --", "printf", "logger -t"]), gen.tok(6)]
            r = rng.random()
            if r < 0.25:
                parts.append('"$(%s %s)"' % (gen.tok(5), gen.tok(3)))
            elif r < 0.5:
                parts.append("%s, %s" % (gen.tok(4), gen.tok(4)))
            elif r < 0.65:
                parts.append("$" + v_arg)
            elif r < 0.8:
                parts.append('"%s %s"' % (gen.tok(3), gen.tok(5)))
            return " ".join(parts)
        if d == "sendshortcut":
            return "%s, %s, activewindow" % (spell_mods(rng, rng.choice([1, 4, 5])), rng.choice(KEYS))
        if d in ("workspace", "movetoworkspace", "movetoworkspacesilent"):
            return rng.choice(["%d" % rng.randint(1, 20), "e+1", "e-1", "special:%s" % gen.tok(4)])
        if d in ("resizeactive",):
            return "%d %d" % (rng.randint(-60, 60), rng.randint(-60, 60))
        if d in ("movefocus", "swapwindow", "movecurrentworkspacetomonitor", "focusmonitor", "moveintogroup"):
            return rng.choice(["l", "r", "u", "d"])
        return rng.choice(["", gen.tok(4)])

    def valid_line():
        if rng.random() < 0.12:  # mouse bind: dispatcher "mouse", arg = the named action (case kept)
            dd = rng.random() < 0.6
            mask = rng.choice([64, 65, 72, 4])
            parts = [mods_text(mask), "mouse:%d" % rng.choice([272, 273, 274])]
            if dd:
                parts.append(gen.tok(5).capitalize() + " " + gen.tok(4))
            parts.append(rng.choice(["movewindow", "resizewindow", "MoveWindow"]))
            return "bindm%s = %s" % ("d" if dd else "", ",".join(pad(p) for p in parts))
        base = rng.choice(["", "", "l", "e", "r", "le", "lr", "n", "a", "x", "o", "lo", "c", "g", "t", "i", "p", "ln"])
        flags = list(base + ("d" if rng.random() < 0.6 else ""))
        rng.shuffle(flags)
        flags = "".join(flags)
        mask = 0 if rng.random() < 0.1 else rng.choice([1, 4, 8, 64, 65, 68, 72, 73, 76, 69, 13])
        d = rng.choice(disps)
        parts = [mods_text(mask), key_text()]
        if "d" in flags:
            parts.append("$" + v_desc if rng.random() < 0.15 else
                         "%s %s (%s)" % (gen.tok(5).capitalize(), gen.tok(4), gen.tok(3)))
        if d == "exec" and rng.random() < 0.15:
            parts.append("$" + v_disp)
        else:
            parts.append(rng.choice([d, d, d.upper(), d.capitalize()]))
        a = arg_for(d)
        if a or rng.random() < 0.5:
            parts.append(a)
        return "bind%s = %s" % (flags, ",".join(pad(p) for p in parts))

    def invalid_line():
        mods, key = spell_mods(rng, 64), rng.choice(KEYS)
        bad_mod = ""
        while not bad_mod or mod_mask(bad_mod) != 0:
            bad_mod = "".join(rng.choice("bdfghjknpqvxyz") for _ in range(5)).upper()
        kind = rng.choice(["flag", "er", "ml", "mod", "disp", "few", "nokey", "mousemany", "catchall", "cg"])
        return {"flag": "bind%s = %s, %s, exec, %s" % (rng.choice("yzbfhjqvw"), mods, key, gen.tok(6)),
                "er": "bind%s = %s, %s, exec, %s" % (rng.choice(["er", "re", "eo", "ec"]), mods, key, gen.tok(6)),
                "ml": "bind%s = %s, mouse:272, movewindow" % (rng.choice(["ml", "me", "mr"]), mods),
                "mod": "bind = %s, %s, exec, %s" % (bad_mod, key, gen.tok(6)),
                "disp": "bind = %s, %s, %s, %s" % (mods, key, "zq" + gen.tok(7), gen.tok(4)),
                "few": "bind = %s, %s" % (mods, key),
                "nokey": "bind = %s, , exec, %s" % (mods, gen.tok(6)),
                "mousemany": "bindm = %s, mouse:273, resizewindow, %s" % (mods, gen.tok(4)),
                "catchall": "bind = %s, catchall, exec, %s" % (mods, gen.tok(6)),
                "cg": "bindcg = %s, %s, exec, %s" % (mods, key, gen.tok(6))}[kind]

    exp = []

    def apply(raw):
        txt = expand(raw.split("#", 1)[0])
        kw, _, val = txt.partition("=")
        if kw.strip(WS) == "unbind":
            unbind_apply(exp, val.strip(WS))
            return
        e = line_entry(kw, val.strip(WS), dispatchers)
        assert e != "UNMODELED", raw
        if e is not None:
            exp.append(e)

    def batch(n):
        out = []
        for _ in range(n):
            line = invalid_line() if rng.random() < 0.2 else valid_line()
            if rng.random() < 0.2:
                line += " # " + gen.tok(5)
            out.append(line)
        return out

    def unbind_for(line, mismatch):
        txt = expand(line.split("#", 1)[0])
        kw, _, val = txt.partition("=")
        e = line_entry(kw, val.strip(WS), dispatchers)
        if not isinstance(e, dict) or e["mouse"]:
            return None
        mods = spell_mods(rng, e["modmask"])
        if e["keycode"]:
            k = rng.choice(["code:%d" % e["keycode"], "%d" % e["keycode"]]) if e["keycode"] > 9 else "code:%d" % e["keycode"]
        elif mismatch and e["key"].lower() != e["key"]:
            k = e["key"].lower()
        else:
            k = e["key"]
        return "unbind = %s, %s" % (mods, k)

    head = ["# %s %s" % (gen.tok(5), gen.tok(7))] + ["$%s = %s" % (n, v) for n, v in variables.items()]
    head += ["", "input {", "    kb_layout = us", "}", ""]
    first = batch(rng.randint(8, 12))
    a_lines = batch(rng.randint(5, 8))
    x_lines, y_lines = batch(rng.randint(2, 4)), batch(rng.randint(2, 4))
    rest = batch(rng.randint(4, 7))
    unb = [u for u in (unbind_for(rng.choice(first), False), unbind_for(rng.choice(first), True),
                       unbind_for(rng.choice(a_lines), False)) if u]
    mid = rng.randint(1, len(a_lines) - 1)
    a_lines = a_lines[:mid] + unb[-1:] + a_lines[mid:]
    root = head + first + ["source = ~/.config/hypr/a.conf", "source = ~/.config/hypr/d/*.conf"] + rest + unb[:-1]
    for l in head + first:
        if BIND_RE.match(l) or l.startswith("unbind"):
            apply(l)
    for l in a_lines + x_lines + y_lines + rest + unb[:-1]:
        apply(l)
    for path, lines in ((os.path.join(hyp, "hyprland.conf"), root), (os.path.join(hyp, "a.conf"), a_lines),
                        (os.path.join(hyp, "d", "x.conf"), x_lines), (os.path.join(hyp, "d", "y.conf"), y_lines),
                        (os.path.join(hyp, "u.conf"), batch(3))):
        with open(path, "w") as fh:
            fh.write("\n".join(lines) + "\n")
    return "HARD tree lines=%d binds=%d unbinds=%d vars=%d" % (
        len(first) + len(a_lines) + len(x_lines) + len(y_lines) + len(rest) + len(unb[:-1]), len(exp), len(unb),
        len(variables)), exp


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
        modeled, drift = model_check(snap0, live)
        print("MODEL_CHECK modeled=%d drift=%d" % (modeled, drift))
        if drift or modeled < 100:
            die("MODEL_DRIFT the HARD line model does not reproduce the live table", 2)
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
