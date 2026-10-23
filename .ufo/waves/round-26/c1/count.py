#!/usr/bin/env python3
"""mado round 26 C1 counter (frozen before any control or data seat scores it).

PRED-C1-r26 (same sentence in registration.md, this code and the receipt label):
  At REV, the committed bytes of tools/mado-anims.py, run in the tool sandbox (no network, no /run,
  cleared environment, the case tree read-only at /snap/home from a randomly named directory),
  print for the unperturbed snapshot of the four Hyprland config roots and for each of 40 generated
  cases the same animation-node set (name, overridden, bezier, enabled, speed, style) and the same
  bezier set (name, X0, Y0, X1, Y1) that Hyprland v0.56.2 itself reports with `hyprctl animations
  -j` for the same tree (a nested, headless, session-isolated instance run by the counter on a copy
  with exec lines removed); target: cases_pass=41/41.

Comparison: the tool prints a JSON array [nodes, beziers] in the shape of `hyprctl animations -j`;
both sides become sets of tuples of the named fields (order ignored, values compared exactly as
parsed JSON). A case passes only when both sets are equal.

Guards (exit 2, nothing measured): harness binary pins differ (oracle.check_build); a nested
instance fails to answer (ORACLE_FAIL); two oracle runs of the unperturbed snapshot disagree
(ORACLE_UNSTABLE); harness/oracle.py bytes differ from ORACLE_SHA.

Cases: each generated case applies 2-4 operations drawn from OPS (plus one from EFFECTIVE when none of
the drawn ones is in it) to a copy of the snapshot; the receipt names them, the tool cannot (random directory names, shuffled run order).

Usage: python3 -I count.py REV [--tool-file PATH] [--seed HEX] [--jobs N]
Exit: 0 TARGET_MET, 1 TARGET_MISSED, 2 setup error / guard.
"""
import argparse, concurrent.futures, hashlib, importlib.util, json, os, random, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
ORACLE_PATH = os.path.join(HERE, "..", "harness", "oracle.py")
ORACLE_SHA = "680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441"
TOOL_PATH = "tools/mado-anims.py"
NCASES = 40
NODE_FIELDS = ("name", "overridden", "bezier", "enabled", "speed", "style")
BEZ_FIELDS = ("name", "X0", "Y0", "X1", "Y1")
NODES = ["global", "windows", "windowsIn", "windowsOut", "windowsMove", "layers", "layersIn", "layersOut",
         "fade", "fadeIn", "fadeOut", "fadeSwitch", "fadeShadow", "fadeDim", "fadeLayers", "fadeLayersIn",
         "fadeLayersOut", "fadePopups", "fadePopupsIn", "fadePopupsOut", "fadeDpms", "fadeGlow", "border",
         "borderangle", "glowangle", "shadowangle", "workspaces", "workspacesIn", "workspacesOut",
         "specialWorkspace", "specialWorkspaceIn", "specialWorkspaceOut", "zoomFactor", "monitorAdded"]
STYLES = ["", "", "slide", "popin", "popin 80%", "popin 33%", "gnomed", "fade", "slidevert", "slidefade",
          "slidefade 20%", "slidefadevert", "slidefadevert 35%", "once", "loop", "slide top", "slide left",
          "bogus", "popin 150%"]
EFFECTIVE = {"ROOT", "SOURCED", "NEWSRC", "BEZIER", "REBEZ", "VARIABLE", "CATEGORY", "DISABLE", "ORDER", "SPACING"}
OPS = ["ROOT", "SOURCED", "NEWSRC", "UNSOURCED", "BEZIER", "REBEZ", "VARIABLE", "COMMENT", "CATEGORY",
       "DISABLE", "INVALID", "ORDER", "SPACING"]


def die(msg, code=2):
    print("SETUP_ERROR " + msg)
    print("exit=%d" % code)
    sys.exit(code)


def load_oracle():
    b = open(ORACLE_PATH, "rb").read()
    if hashlib.sha256(b).hexdigest() != ORACLE_SHA:
        die("harness/oracle.py sha256 differs from the pin")
    spec = importlib.util.spec_from_file_location("mado_r26_oracle", ORACLE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


O = load_oracle()
SOURCE_RE = re.compile(r"^\s*source\s*=\s*(.+?)\s*$")


def sourced_files(home):
    import glob
    seen = []

    def walk(pat):
        pat = pat.replace("~", home, 1) if pat.startswith("~") else pat
        for f in sorted(glob.glob(pat)):
            if f in seen or not os.path.isfile(f):
                continue
            seen.append(f)
            for line in open(f, errors="replace"):
                m = SOURCE_RE.match(line.split("#", 1)[0])
                if m:
                    walk(m.group(1))
    walk(os.path.join(home, ".config/hypr/hyprland.conf"))
    return seen


def num(rng, lo, hi, maxdec=4):
    d = rng.randint(0, maxdec)
    v = rng.uniform(lo, hi)
    return ("%d" % round(v)) if d == 0 else ("%.*f" % (d, v))


def bezier_names(home):
    names = ["default", "linear"]
    for f in sourced_files(home):
        for line in open(f, errors="replace"):
            m = re.match(r"^\s*bezier\s*=\s*([^,#]+),", line)
            if m:
                names.append(m.group(1).strip())
    return names


def anim_line(rng, home, node=None, bez=None, speed=None, style=None):
    node = node or rng.choice(NODES)
    bez = bez or rng.choice(bezier_names(home))
    speed = speed or num(rng, 0.1, 10)
    style = rng.choice(STYLES) if style is None else style
    parts = [node, rng.choice(["1", "1", "0"]), speed, bez] + ([style] if style else [])
    return "animation = " + ", ".join(parts)


def append(path, lines):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write("\n" + "\n".join(lines) + "\n")


def rand_name(rng, n=6):
    return "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n))


def apply_op(op, rng, home):
    root = os.path.join(home, ".config/hypr/hyprland.conf")
    files = sourced_files(home)
    if op == "ROOT":
        append(root, [anim_line(rng, home)])
    elif op == "SOURCED":
        append(rng.choice(files), [anim_line(rng, home)])
    elif op == "NEWSRC":
        name = rand_name(rng)
        sub = os.path.join(home, ".config/hypr", name + ".conf")
        append(sub, [anim_line(rng, home) for _ in range(rng.randint(1, 3))])
        append(rng.choice(files), ["source = ~/.config/hypr/%s.conf" % name])
    elif op == "UNSOURCED":
        sub = os.path.join(home, ".config/hypr", rand_name(rng) + ".conf")
        append(sub, [anim_line(rng, home) for _ in range(2)])
    elif op == "BEZIER":
        b = "bz" + rand_name(rng, 4)
        pts = [num(rng, 0, 1, 5), num(rng, -0.5, 1.5, 5), num(rng, 0, 1, 5), num(rng, -0.5, 1.5, 5)]
        append(rng.choice(files), ["bezier = %s, %s" % (b, ", ".join(pts)), anim_line(rng, home, bez=b)])
    elif op == "REBEZ":
        b = rng.choice(bezier_names(home))
        pts = [num(rng, 0, 1, 3), num(rng, 0, 1, 3), num(rng, 0, 1, 3), num(rng, 0, 1, 3)]
        append(rng.choice(files), ["bezier = %s, %s" % (b, ", ".join(pts))])
    elif op == "VARIABLE":
        vs, vb = "$sp" + rand_name(rng, 3), "$bz" + rand_name(rng, 3)
        b = rng.choice(bezier_names(home))
        append(root, ["%s = %s" % (vs, num(rng, 0.5, 9)), "%s = %s" % (vb, b),
                      "animation = %s, 1, %s, %s" % (rng.choice(NODES), vs, vb)])
    elif op == "COMMENT":
        append(rng.choice(files), ["# " + anim_line(rng, home),
                                   anim_line(rng, home, style="") + " # " + rand_name(rng),
                                   "#animation = %s, 0" % rng.choice(NODES)])
    elif op == "CATEGORY":
        b = "cb" + rand_name(rng, 4)
        append(rng.choice(files), ["animations {", "    bezier = %s, 0.2, 0.8, 0.3, 1" % b,
                                   "    " + anim_line(rng, home, bez=b), "}"])
    elif op == "DISABLE":
        append(rng.choice(files), ["animation = %s, 0" % rng.choice(NODES)])
    elif op == "INVALID":
        bad = rng.choice([
            "animation = %s, 1, 3, default" % ("no" + rand_name(rng)),
            "animation = %s, 1, 3, %s" % (rng.choice(NODES), "nb" + rand_name(rng)),
            "animation = %s, 2, 3, default" % rng.choice(NODES),
            "animation = %s, 1, -4, default" % rng.choice(NODES),
            "animation = %s, 1, fast, default" % rng.choice(NODES),
            "animation = %s, 1" % rng.choice(NODES),
            "bezier = %s, 0.1, 0.2" % ("bb" + rand_name(rng, 3)),
        ])
        append(rng.choice(files), [bad])
    elif op == "ORDER":
        node = rng.choice(NODES)
        f1, f2 = rng.choice(files), rng.choice(files)
        append(f1, [anim_line(rng, home, node=node)])
        append(f2, [anim_line(rng, home, node=node)])
    elif op == "SPACING":
        node, b = rng.choice(NODES), rng.choice(bezier_names(home))
        append(rng.choice(files), ["animation=%s,1,%s,%s" % (node, num(rng, 1, 8), b),
                                   "\tanimation   =   %s ,  1 , %s ,%s" % (rng.choice(NODES), num(rng, 1, 8), b)])
    else:
        raise ValueError(op)


def node_set(data):
    return {tuple(json.dumps(e.get(f), sort_keys=True) for f in NODE_FIELDS) for e in data[0]}


def bez_set(data):
    return {tuple(json.dumps(e.get(f), sort_keys=True) for f in BEZ_FIELDS) for e in data[1]}


def well_formed(data):
    return (isinstance(data, list) and len(data) == 2 and all(isinstance(x, list) for x in data)
            and all(isinstance(e, dict) for x in data for e in x))


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
    print("counter c1-r26 sha256:%s rev=%s oracle.py sha256:%s" % (O.sha(me), rev, ORACLE_SHA))
    core0 = O.coredumps()
    tmp = tempfile.mkdtemp(prefix="m26c1-", dir="/fast/scratch/hyaku/mado-r26")
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
        for i in range(NCASES):
            home = tempfile.mkdtemp(dir=tmp)
            shutil.copytree(snap0, home, dirs_exist_ok=True)
            ops = rng.sample(OPS, rng.randint(2, 4))
            if not set(ops) & EFFECTIVE:
                ops.append(rng.choice(sorted(EFFECTIVE)))
            for op in ops:
                apply_op(op, rng, home)
            built.append(("C%02d" % i, home, "+".join(ops)))
        jobs = max(1, min(a.jobs, O.SLOTS))
        with concurrent.futures.ThreadPoolExecutor(jobs) as ex:
            futs = {lab: ex.submit(O.oracle, home, tempfile.mkdtemp(dir=tmp), ["animations"]) for lab, home, _ in built}
            futs["BASE#2"] = ex.submit(O.oracle, snap0, tempfile.mkdtemp(dir=tmp), ["animations"])
            truth = {lab: f.result() for lab, f in futs.items()}
        for lab, (res, err) in sorted(truth.items()):
            if res is None:
                die("ORACLE_FAIL %s: %s" % (lab, err))
        b1, b2 = truth["BASE"][0]["animations"], truth["BASE#2"][0]["animations"]
        if node_set(b1) != node_set(b2) or bez_set(b1) != bez_set(b2):
            die("ORACLE_UNSTABLE two oracle runs of the unperturbed snapshot disagree")
        print("ORACLE_CHECK base_twice equal nodes=%d beziers=%d" % (len(b1[0]), len(b1[1])))
        order = list(built)
        random.Random(os.urandom(8)).shuffle(order)
        verdict = {}
        for lab, home, desc in order:
            exp = truth[lab][0]["animations"]
            if tb is None:
                verdict[lab] = (False, "tool absent")
                continue
            got, err = O.run_tool(tool, home)
            if got is None or not well_formed(got):
                verdict[lab] = (False, err or "output is not [nodes, beziers]")
                continue
            try:
                gn, gb = node_set(got), bez_set(got)
            except (AttributeError, TypeError):
                verdict[lab] = (False, "entries are not objects")
                continue
            en, eb = node_set(exp), bez_set(exp)
            ok = gn == en and gb == eb
            verdict[lab] = (ok, "nodes missing=%d extra=%d beziers missing=%d extra=%d" % (
                len(en - gn), len(gn - en), len(eb - gb), len(gb - eb)))
        npass = 0
        for lab, home, desc in built:
            ok, info = verdict[lab]
            npass += ok
            print("CASE %-5s %s %s (%s)" % (lab, "PASS" if ok else "FAIL", info, desc))
        core1 = O.coredumps()
        print("HOST_SAFETY hyprland_coredumps_before=%d after=%d delta=%d" % (core0, core1, core1 - core0))
        met = npass == len(built)
        print("PRED-C1-r26 cases_pass=%d/%d verdict=%s" % (npass, len(built), "TARGET_MET" if met else "TARGET_MISSED"))
        return 0 if met else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    rc = main()
    print("exit=%d" % rc)
    sys.exit(rc)
