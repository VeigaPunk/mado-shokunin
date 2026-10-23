#!/usr/bin/env python3
"""mado round 27 C1 counter v4 (redesign before data; v1-v3 kept with their receipts; v3 = v2 with random variable
names; v4 = v3 plus value-embedded variables, definitions in a sourced file, use before definition and a file
sourced twice, after w1 CritC1Counter met v3 41/41 with GlobalOnce and FileScope readers): the Hyprland workspace-rule table (`hyprctl workspacerules -j`) from config bytes.

PRED-C1-r27-v4 (same sentence in registration.md, this code and the receipt label):
  At REV, the committed bytes of tools/mado-wsrules.py, run in the tool sandbox (no network, no /run,
  cleared environment, the case tree read-only at /snap/home from a randomly named directory), print for
  the unperturbed snapshot of the four Hyprland config roots and for each of 40 generated cases (25 that
  add workspace rules to the snapshot, 15 independent trees that contain none of the snapshot's files;
  cases carry unsourced decoy files, nested and glob sources and source lines placed among rule lines)
  a JSON array equal, entry by entry and in order, to the array Hyprland v0.56.2 itself prints with
  `hyprctl workspacerules -j` for the same tree (a nested, headless, session-isolated instance run by the
  counter on a copy with exec lines removed); target: cases_pass=41/41.

Comparison: both sides are parsed JSON; a case passes only when the two lists are equal (same length,
same order, each entry the same object: same keys, same values), compared type-strictly as canonical JSON
(`json.dumps(..., sort_keys=True)`), so `1` is not `true` and `5` is not `5.0` (w1 CritC1Counter).

Guards (exit 2, nothing measured): harness binary pins differ (oracle.check_build); harness/oracle.py bytes
differ from ORACLE_SHA; a nested instance fails to answer (ORACLE_FAIL); two oracle runs of the
unperturbed snapshot disagree (ORACLE_UNSTABLE); the nested instance's `hyprctl version -j` commit is not
HYPR_COMMIT (ORACLE_VERSION).

Cases: APPEND (25) copy the snapshot and add 2-6 workspace-rule lines spread over the root, a file the
snapshot already sources, a new sourced file, and variables; SYNTH (15) are fresh trees (root + 0-2
sourced files). Every case carries at least one TRAP feature that a line-by-line reader without hyprlang
semantics misses (a repeated workspace selector that Hyprland merges, a 1-3 value gap shorthand, a
variable, a sourced file, an on-created-empty command, or a yes/no/on/off/1/0 boolean). Generated values
stay small (no overflowing numbers, no source cycles: M26-6). The receipt names each case's family and
features; the tool cannot see them (random directory names, shuffled run order).

Usage: python3 -I count.py REV [--tool-file PATH] [--seed HEX] [--jobs N]
Exit: 0 TARGET_MET, 1 TARGET_MISSED, 2 setup error / guard. Every path prints `exit=<n>`.
"""
import argparse, concurrent.futures, hashlib, importlib.util, json, os, random, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
ORACLE_PATH = os.path.join(HERE, "..", "harness", "oracle.py")
HYPR_COMMIT = "efb50993780079460b0cbed1363e2166a2de1d9f"
ORACLE_SHA = "0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601"
TOOL_PATH = "tools/mado-wsrules.py"
SCRATCH = "/fast/scratch/hyaku/mado-r27"
WORDS = ["web", "chat", "mail", "code", "music", "notes", "term", "games", "docs", "media"]
CMDS = ["kitty", "firefox", "alacritty -e btop", "foot", "thunar", "uwsm app -- obsidian"]
BOOLS_T = ["true", "yes", "on", "1"]
BOOLS_F = ["false", "no", "off", "0"]


def die(msg, code=2):
    print("SETUP_ERROR " + msg)
    print("exit=%d" % code)
    sys.exit(code)


def load_oracle():
    b = open(ORACLE_PATH, "rb").read()
    if hashlib.sha256(b).hexdigest() != ORACLE_SHA:
        die("harness/oracle.py sha256 differs from the pin")
    spec = importlib.util.spec_from_file_location("mado_r27_oracle", ORACLE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


O = load_oracle()


def rand_name(rng, n=6):
    return "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n))


def selector(rng):
    k = rng.random()
    if k < 0.40:
        return str(rng.randint(1, 10))
    if k < 0.60:
        return "name:" + rng.choice(WORDS)
    if k < 0.72:
        return "special:" + rng.choice(WORDS)
    if k < 0.82:
        a = rng.randint(1, 5)
        return "r[%d-%d]" % (a, a + rng.randint(0, 4))
    if k < 0.90:
        return "w[%s]" % rng.choice(["tv1", "t1", "f1", "g1", "1-3", "v2"])
    return "m[HEADLESS-1]" if rng.random() < 0.5 else "f[%d]" % rng.randint(-1, 1)


def gaps(rng, trap):
    n = rng.choice([1, 2, 3]) if trap else rng.choice([1, 2, 3, 4])
    return " ".join(str(rng.randint(0, 30)) for _ in range(n))


def boolv(rng, trap):
    pool = (BOOLS_T[1:] + BOOLS_F[1:]) if trap else ["true", "false"]
    return rng.choice(pool)


def rule_items(rng, feats, sel):
    """2-4 rule items for one `workspace =` line; appends trap feature names to feats."""
    items = []
    keys = rng.sample(["monitor", "default", "persistent", "gapsin", "gapsout", "bordersize", "border",
                       "rounding", "decorate", "shadow", "defaultName", "on-created-empty", "layoutopt"],
                      rng.randint(1, 4))
    for k in keys:
        if k == "monitor":
            items.append("monitor:" + rng.choice(["HEADLESS-1", "DP-1", "desc:Some Panel"]))
        elif k in ("gapsin", "gapsout"):
            trap = rng.random() < 0.6
            if trap:
                feats.add("GAPSHORT")
            items.append("%s:%s" % (k, gaps(rng, trap)))
        elif k == "bordersize":
            items.append("bordersize:%d" % rng.randint(0, 5))
        elif k == "defaultName":
            items.append("defaultName:" + rng.choice(WORDS) + str(rng.randint(0, 9)))
        elif k == "on-created-empty":
            feats.add("ONEMPTY")
            items.append("on-created-empty:" + rng.choice(CMDS))
        elif k == "layoutopt":
            items.append("layoutopt:orientation:" + rng.choice(["top", "left", "center"]))
        else:
            trap = rng.random() < 0.5
            if trap:
                feats.add("BOOLWORD")
            items.append("%s:%s" % (k, boolv(rng, trap)))
    return items


def rule_lines(rng, feats, nlines, var_ok=True):
    """Return (lines, vars) with nlines `workspace =` lines; may repeat a selector (MERGE) or use a variable."""
    lines, defs, used = [], [], []
    for i in range(nlines):
        if used and rng.random() < 0.35:
            sel = rng.choice(used)
            feats.add("MERGE")
        else:
            sel = selector(rng)
            used.append(sel)
        items = rule_items(rng, feats, sel)
        if var_ok and rng.random() < 0.25:
            v = "$" + rand_name(rng, rng.randint(5, 9))  # v3: no fixed prefix (w1 CritC1Counter)
            k = rng.random()
            if k < 0.35:
                defs.append("%s = %s" % (v, sel))
                sel_txt, item_txt = v, items
            elif k < 0.65 or ":" not in items[0]:
                defs.append("%s = %s" % (v, items[0]))
                sel_txt, item_txt = sel, [v] + items[1:]
            else:
                # VAREMBED (v4): the variable holds only the value of an item, used inside the item
                key, val = items[0].split(":", 1)
                defs.append("%s = %s" % (v, val))
                sel_txt, item_txt = sel, ["%s:%s" % (key, v)] + items[1:]
                feats.add("VAREMBED")
            feats.add("VARIABLE")
        else:
            sel_txt, item_txt = sel, items
        sep = rng.choice([", ", ",", " , "])
        line = "workspace = " + sel_txt + sep + sep.join(item_txt)
        if rng.random() < 0.2:
            line += "  # " + rand_name(rng)
            feats.add("COMMENT")
        lines.append(line)
    return defs + lines


def write(path, lines, mode="a"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode, encoding="utf-8") as fh:
        fh.write("\n" + "\n".join(lines) + "\n")


def sourced_existing(home):
    root = os.path.join(home, ".config/hypr/hyprland.conf")
    out = []
    for line in open(root, errors="replace"):
        s = line.split("#", 1)[0].strip()
        if s.startswith("source") and "=" in s:
            p = s.split("=", 1)[1].strip()
            p = os.path.join(home, p[2:]) if p.startswith("~/") else p
            if os.path.isfile(p) and os.path.realpath(p).startswith(os.path.realpath(home) + os.sep):
                out.append(p)
    return out


TRAPS = {"MERGE", "GAPSHORT", "VARIABLE", "SOURCED", "NEWSRC", "ONEMPTY", "BOOLWORD", "DECOY", "ORDER", "NESTED", "GLOB",
         "VARREDEF", "VAREMBED", "USEBEFOREDEF", "TWICE", "SRCDEF"}


def fname(rng):
    return rand_name(rng, rng.randint(3, 10)) + rng.choice([".conf", ".conf", ".hl", ".cfg"])


def build_case(rng, home, fam):
    """v2 (w1 CritC1Counter, before data): v1 sourced every file it wrote, at the end of the root, so a reader that
    scanned every file in the tree in filename order met v1 without following `source =`. v2 adds unsourced DECOY
    files that carry workspace rules (mentioned only in a commented-out source line, or sourced only from another
    unsourced decoy), places each new `source =` line at a random position among the root's rule lines (ORDER),
    sources files from sourced files (NESTED) and through glob patterns (GLOB), and draws file names of random
    length and extension in random subdirectories."""
    feats = set()
    hypr = os.path.join(home, ".config/hypr")
    root = os.path.join(hypr, "hyprland.conf")
    if fam == "SYNTH":
        os.makedirs(hypr, exist_ok=True)
        open(root, "w").close()
    nlines = rng.randint(2, 6)
    lines = rule_lines(rng, feats, nlines)
    defs = [ln for ln in lines if not ln.startswith("workspace")]
    rules = [ln for ln in lines if ln.startswith("workspace")]
    existing = sourced_existing(home) if fam == "APPEND" else []
    root_items, new_a, new_b, ex_lines = [], [], [], []
    for ln in rules:
        k = rng.random()
        if existing and k < 0.2 and "$" not in ln:  # existing files are sourced before the defs
            ex_lines.append(ln)
        elif k < 0.4:
            new_a.append(ln)
        elif k < 0.55:
            new_b.append(ln)
        else:
            root_items.append(ln)
    sub = rng.choice(["", "", rand_name(rng, rng.randint(2, 6)) + "/"])
    pa = os.path.join(hypr, sub, fname(rng))
    pb = os.path.join(hypr, sub, fname(rng))
    src_lines = []  # (line, target) to be placed into the root at random positions
    if new_a or new_b:
        mode = rng.random()
        if new_a and new_b and mode < 0.3:
            # GLOB: both files in one fresh directory, one glob source line (glob order = sorted names)
            gdir = os.path.join(hypr, rand_name(rng, rng.randint(3, 7)) + ".d")
            pa = os.path.join(gdir, fname(rng))
            pb = os.path.join(gdir, fname(rng))
            while os.path.basename(pb) == os.path.basename(pa):
                pb = os.path.join(gdir, fname(rng))
            write(pa, new_a, "w")
            write(pb, new_b, "w")
            src_lines.append("source = ~/" + os.path.relpath(gdir, home) + "/*")
            feats.update({"GLOB", "NEWSRC"})
        elif new_a and new_b and mode < 0.6:
            # NESTED: b is sourced from a random position inside a
            lines_a = list(new_a)
            lines_a.insert(rng.randint(0, len(lines_a)), "source = ~/" + os.path.relpath(pb, home))
            write(pa, lines_a, "w")
            write(pb, new_b, "w")
            src_lines.append("source = ~/" + os.path.relpath(pa, home))
            feats.update({"NESTED", "NEWSRC"})
        else:
            for p, ls in ((pa, new_a), (pb, new_b)):
                if ls:
                    write(p, ls, "w")
                    src_lines.append("source = ~/" + os.path.relpath(p, home))
            feats.add("NEWSRC")
    body = list(root_items)
    for sl in src_lines:
        i = rng.randint(0, len(body))
        if i < len(body):
            feats.add("ORDER")
        body.insert(i, sl)
    if rng.random() < 0.75:
        # DECOY: an unsourced file with rules; mentioned only by a commented source line or by another decoy
        pd = os.path.join(hypr, rng.choice(["", sub]), fname(rng))
        pd2 = os.path.join(hypr, fname(rng))
        dlines = rule_lines(rng, set(), rng.randint(1, 3), var_ok=False)
        if rng.random() < 0.5:
            dlines.append("source = ~/" + os.path.relpath(pd2, home))
            write(pd2, rule_lines(rng, set(), 1, var_ok=False), "w")
        write(pd, dlines, "w")
        if rng.random() < 0.6:
            body.insert(rng.randint(0, len(body)), "# source = ~/" + os.path.relpath(pd, home))
        feats.add("DECOY")
    if rng.random() < 0.35:
        # VARREDEF (w1 CritC1Counter): a variable is used, redefined, and used again; a global-prepass reader
        # that binds each name once gives both rules the last value
        v = "$" + rand_name(rng, rng.randint(5, 9))  # v3: no fixed prefix (w1 CritC1Counter)
        s1, s2 = selector(rng), selector(rng)
        while s2 == s1:
            s2 = selector(rng)
        blk = ["%s = %s" % (v, s1), "workspace = %s, bordersize:%d" % (v, rng.randint(0, 5)),
               "%s = %s" % (v, s2), "workspace = %s, rounding:%s" % (v, rng.choice(["true", "false"]))]
        i = rng.randint(0, len(body))
        body[i:i] = blk
        feats.add("VARREDEF")
    if ex_lines:
        write(rng.choice(existing), ex_lines)
        feats.add("SOURCED")
    if rng.random() < 0.3:
        # USEBEFOREDEF (v4, w1 CritC1Counter): an item variable used once before its only definition, then after it
        u = "$" + rand_name(rng, rng.randint(5, 9))
        s1, s2 = selector(rng), selector(rng)
        blk = ["workspace = %s, %s, bordersize:%d" % (s1, u, rng.randint(0, 5)),
               "%s = %s" % (u, rng.choice(["rounding:false", "decorate:false", "shadow:true", "persistent:true"])),
               "workspace = %s, %s" % (s2, u)]
        i = rng.randint(0, len(body))
        body[i:i] = blk
        feats.add("USEBEFOREDEF")
    if rng.random() < 0.3:
        # TWICE (v4): one file sourced twice with a conflicting rule for the same selector in between
        st = selector(rng)
        pt = os.path.join(hypr, fname(rng))
        write(pt, ["workspace = %s, bordersize:%d, gapsin:%d" % (st, rng.randint(0, 2), rng.randint(0, 9))], "w")
        blk = ["source = ~/" + os.path.relpath(pt, home),
               "workspace = %s, bordersize:%d" % (st, rng.randint(3, 5)),
               "source = ~/" + os.path.relpath(pt, home)]
        i = rng.randint(0, len(body))
        body[i:i] = blk
        feats.add("TWICE")
    if defs and rng.random() < 0.4:
        # SRCDEF (v4): the definitions live in a sourced file that runs before their uses
        pdefs = os.path.join(hypr, rng.choice(["", rand_name(rng, 4) + "/"]), fname(rng))
        write(pdefs, defs, "w")
        defs = ["source = ~/" + os.path.relpath(pdefs, home)]
        feats.add("SRCDEF")
    write(root, defs + body)
    if not feats & TRAPS:
        first = rules[0]
        sel = first.split("=", 1)[1].split(",", 1)[0].strip()
        write(root, ["workspace = %s, bordersize:%d" % (sel, rng.randint(0, 5))])
        feats.add("MERGE")
    return "%s:%s" % (fam, "+".join(sorted(feats)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--tool-file")
    ap.add_argument("--seed")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    try:
        O.check_build()
    except O.SetupError as ex:
        die(str(ex))
    rev = subprocess.run(["git", "-C", LANE, "rev-parse", "--verify", a.rev + "^{commit}"], capture_output=True, text=True)
    if rev.returncode != 0:
        die("bad REV %s" % a.rev)
    rev = rev.stdout.strip()
    me = open(os.path.abspath(__file__), "rb").read()
    print("counter c1-r27-v4 sha256:%s rev=%s oracle.py sha256:%s" % (O.sha(me), rev, ORACLE_SHA))
    core0 = O.coredumps()
    os.makedirs(SCRATCH, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="m27c1-", dir=SCRATCH)
    try:
        tool = os.path.join(tmp, "t" + os.urandom(4).hex() + ".py")
        if a.tool_file:
            tb = open(a.tool_file, "rb").read()
            print("tool=override:%s sha256:%s" % (a.tool_file, O.sha(tb)))
        else:
            p = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, TOOL_PATH)], capture_output=True)
            tb = p.stdout if p.returncode == 0 else None
            print(("tool=%s@%s sha256:%s" % (TOOL_PATH, rev[:12], O.sha(tb))) if tb is not None
                  else "tool=MISSING_TOOL at %s" % rev)
        if tb is not None:
            with open(tool, "wb") as fh:
                fh.write(tb)
        seed = a.seed or os.urandom(8).hex()
        print("seed=%s" % seed)
        rng = random.Random(int(seed, 16))
        snap0 = tempfile.mkdtemp(dir=tmp)
        nfiles, digest = O.snapshot(os.path.expanduser("~"), snap0)
        print("snapshot files=%d digest sha256:%s" % (nfiles, digest))
        built = [("BASE", snap0, "unperturbed")]
        for i, fam in enumerate(["APPEND"] * 25 + ["SYNTH"] * 15):
            home = tempfile.mkdtemp(dir=tmp)
            if fam == "APPEND":
                shutil.copytree(snap0, home, dirs_exist_ok=True)
            built.append(("C%02d" % i, home, build_case(rng, home, fam)))
        jobs = max(1, min(a.jobs, O.SLOTS))
        with concurrent.futures.ThreadPoolExecutor(jobs) as ex:
            futs = {lab: ex.submit(O.oracle, home, tempfile.mkdtemp(dir=tmp),
                                   ["workspacerules", "version"] if lab == "BASE" else ["workspacerules"])
                    for lab, home, _ in built}
            futs["BASE#2"] = ex.submit(O.oracle, snap0, tempfile.mkdtemp(dir=tmp), ["workspacerules"])
            truth = {lab: f.result() for lab, f in futs.items()}
        for lab, (res, err) in sorted(truth.items()):
            if res is None:
                die("ORACLE_FAIL %s: %s" % (lab, err))
        b1, b2 = truth["BASE"][0]["workspacerules"], truth["BASE#2"][0]["workspacerules"]
        if b1 != b2:
            die("ORACLE_UNSTABLE two oracle runs of the unperturbed snapshot disagree")
        print("ORACLE_CHECK base_twice equal rules=%d" % len(b1))
        ver = truth["BASE"][0]["version"]
        commit = ver.get("commit") if isinstance(ver, dict) else None
        if commit != HYPR_COMMIT:
            die("ORACLE_VERSION nested Hyprland commit %r is not %s" % (commit, HYPR_COMMIT))
        print("ORACLE_VERSION commit=%s tag=%s" % (commit, ver.get("tag")))
        order = list(built)
        random.Random(os.urandom(8)).shuffle(order)
        verdict = {}
        for lab, home, desc in order:
            exp = truth[lab][0]["workspacerules"]
            if tb is None:
                verdict[lab] = (False, "tool absent")
                continue
            got, err = O.run_tool(tool, home)
            if got is None:
                verdict[lab] = (False, err or "no output")
                continue
            if not isinstance(got, list):
                verdict[lab] = (False, "output is not a JSON array")
                continue
            ok = json.dumps(got, sort_keys=True) == json.dumps(exp, sort_keys=True)
            if ok:
                info = "rules=%d" % len(exp)
            else:
                diff = next((i for i in range(min(len(got), len(exp))) if got[i] != exp[i]), min(len(got), len(exp)))
                info = "rules got=%d want=%d first_diff=%d" % (len(got), len(exp), diff)
            verdict[lab] = (ok, info)
        npass = 0
        for lab, home, desc in built:
            ok, info = verdict[lab]
            npass += ok
            print("CASE %-5s %s %s oracle_rules=%d (%s)" % (lab, "PASS" if ok else "FAIL", info,
                                                          len(truth[lab][0]["workspacerules"]), desc))
        core1 = O.coredumps()
        print("HOST_SAFETY hyprland_coredumps_before=%d after=%d delta=%d" % (core0, core1, core1 - core0))
        met = npass == len(built)
        print("PRED-C1-r27-v4 cases_pass=%d/%d verdict=%s" % (npass, len(built), "TARGET_MET" if met else "TARGET_MISSED"))
        return 0 if met else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    rc = main()
    print("exit=%d" % rc)
    sys.exit(rc)
