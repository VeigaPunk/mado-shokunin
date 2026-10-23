#!/usr/bin/env python3
"""mado round 27 C1 counter: the Hyprland workspace-rule table (`hyprctl workspacerules -j`) from config bytes.

PRED-C1-r27 (same sentence in registration.md, this code and the receipt label):
  At REV, the committed bytes of tools/mado-wsrules.py, run in the tool sandbox (no network, no /run,
  cleared environment, the case tree read-only at /snap/home from a randomly named directory), print for
  the unperturbed snapshot of the four Hyprland config roots and for each of 40 generated cases (25 that
  add workspace rules to the snapshot, 15 independent trees that contain none of the snapshot's files)
  a JSON array equal, entry by entry and in order, to the array Hyprland v0.56.2 itself prints with
  `hyprctl workspacerules -j` for the same tree (a nested, headless, session-isolated instance run by the
  counter on a copy with exec lines removed); target: cases_pass=41/41.

Comparison: both sides are parsed JSON; a case passes only when the two lists are equal (same length,
same order, each entry the same object: same keys, same values).

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
            v = "$ws" + rand_name(rng, 3)
            if rng.random() < 0.5:
                defs.append("%s = %s" % (v, sel))
                sel_txt, item_txt = v, items
            else:
                defs.append("%s = %s" % (v, items[0]))
                sel_txt, item_txt = sel, [v] + items[1:]
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


TRAPS = {"MERGE", "GAPSHORT", "VARIABLE", "SOURCED", "NEWSRC", "ONEMPTY", "BOOLWORD"}


def build_case(rng, home, fam):
    feats = set()
    root = os.path.join(home, ".config/hypr/hyprland.conf")
    if fam == "SYNTH":
        os.makedirs(os.path.dirname(root), exist_ok=True)
        open(root, "w").close()
    nlines = rng.randint(2, 6)
    lines = rule_lines(rng, feats, nlines)
    # split lines: root / existing sourced / new sourced file
    where = []
    existing = sourced_existing(home) if fam == "APPEND" else []
    for ln in lines:
        k = rng.random()
        if existing and k < 0.25 and "$ws" not in ln:  # existing files are sourced before the defs
            where.append(("EX", ln))
        elif k < 0.45:
            where.append(("NEW", ln))
        else:
            where.append(("ROOT", ln))
    # variable definitions must precede their use: keep defs in the root, at the top
    defs = [ln for w, ln in where if not ln.startswith("workspace")]
    rest = [(w, ln) for w, ln in where if ln.startswith("workspace")]
    root_lines = defs + [ln for w, ln in rest if w == "ROOT"]
    new_lines = [ln for w, ln in rest if w == "NEW"]
    ex_lines = [ln for w, ln in rest if w == "EX"]
    if new_lines:
        sub = ".config/hypr/%s.conf" % rand_name(rng)
        write(os.path.join(home, sub), new_lines, "w")
        root_lines.append("source = ~/" + sub)
        feats.add("NEWSRC")
    if ex_lines:
        write(rng.choice(existing), ex_lines)
        feats.add("SOURCED")
    write(root, root_lines)
    if not feats & TRAPS:
        # force a merge: repeat the first rule's selector with one more item
        first = next(ln for ln in lines if ln.startswith("workspace"))
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
    print("counter c1-r27 sha256:%s rev=%s oracle.py sha256:%s" % (O.sha(me), rev, ORACLE_SHA))
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
            ok = got == exp
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
        print("PRED-C1-r27 cases_pass=%d/%d verdict=%s" % (npass, len(built), "TARGET_MET" if met else "TARGET_MISSED"))
        return 0 if met else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    rc = main()
    print("exit=%d" % rc)
    sys.exit(rc)
