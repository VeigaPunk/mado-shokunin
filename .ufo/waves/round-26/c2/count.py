#!/usr/bin/env python3
"""mado round 26 C2 counter (frozen before any control or data seat scores it).

PRED-C2-r26 (same sentence in registration.md, this code and the receipt label):
  At REV, the committed bytes of tools/mado-binds.py, run in the tool sandbox (no network, no
  /run, cleared environment, the case tree read-only at /snap/home from a randomly named
  directory), reproduce exactly over all 18 `hyprctl binds -j` fields the bind multiset that
  Hyprland v0.56.2 itself reports for the same tree (a nested, headless, session-isolated instance
  run by the counter on a copy with exec lines removed), for the unperturbed snapshot of the four
  Hyprland config roots, for 30 ARITH cases (added binds and variables whose values use hyprlang
  `{{...}}` expressions) and for 20 V3 cases (round 25's count-v3.py generator, two of each of its
  ten types, fed the oracle's table of the unperturbed snapshot), and the tool bytes contain none
  of that table's arg or description strings of 12 or more characters; target:
  cases_pass=51/51 and embed_hits=0.

Guards (exit 2, nothing measured): harness binary pins differ; harness/oracle.py or count-v3.py
bytes differ from their pins; a nested instance fails to answer (ORACLE_FAIL); two oracle runs of
the unperturbed snapshot disagree (ORACLE_UNSTABLE).

Usage: python3 -I count.py REV [--tool-file PATH] [--seed HEX] [--jobs N]
Exit: 0 TARGET_MET, 1 TARGET_MISSED, 2 setup error / guard.
"""
import argparse, concurrent.futures, hashlib, importlib.util, os, random, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
ORACLE_PATH = os.path.join(HERE, "..", "harness", "oracle.py")
ORACLE_SHA = "680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441"
V3_PATH = os.path.join(LANE, ".ufo/waves/round-25/c1/count-v3.py")
V3_SHA = "8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375"
TOOL_PATH = "tools/mado-binds.py"
NARITH = 30
V3_PER_TYPE = 2
EMBED_MIN = 12
MODS = ["SUPER", "SUPER SHIFT", "SUPER CTRL", "SUPER ALT", "SUPER CTRL ALT", "CTRL ALT", "SUPER SHIFT CTRL"]
KEYS = ["F13", "F14", "F15", "F16", "F17", "F18", "F19", "F20", "KP_2", "KP_3", "KP_4", "KP_6", "KP_7", "KP_8",
        "Y", "U", "I", "O", "B", "N", "M", "7", "8", "9"]


def die(msg, code=2):
    print("SETUP_ERROR " + msg)
    print("exit=%d" % code)
    sys.exit(code)


def load(path, want, name):
    b = open(path, "rb").read()
    if hashlib.sha256(b).hexdigest() != want:
        die("%s sha256 differs from the pin" % path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


O = load(ORACLE_PATH, ORACLE_SHA, "mado_r26_oracle")
V3 = load(V3_PATH, V3_SHA, "mado_r25_count_v3")


def operand(rng, vars_):
    r = rng.random()
    if vars_ and r < 0.3:
        return rng.choice(vars_)
    if r < 0.75:
        return str(rng.randint(0, 40))
    return "%.*f" % (rng.randint(1, 3), rng.uniform(0, 20))


def expr(rng, vars_):
    n = rng.randint(1, 3)
    s = operand(rng, vars_)
    for _ in range(n):
        s += rng.choice([" + ", "+", " - ", " * ", "*", " / "]) + operand(rng, vars_)
    if rng.random() < 0.25:
        s = "(" + s + ")" + rng.choice([" * 2", " + 1", "/4"])
    pad = rng.choice(["", " "])
    return "{{" + pad + s + pad + "}}"


def arith_case(rng, home, files):
    root = os.path.join(home, ".config/hypr/hyprland.conf")
    target = rng.choice(files)
    lines, vars_ = [], []
    for _ in range(rng.randint(0, 2)):
        v = "$ar" + "".join(rng.choice("abcdefghij") for _ in range(4))
        lines.append("%s = %s" % (v, rng.choice([str(rng.randint(1, 9)), "%.1f" % rng.uniform(1, 9), expr(rng, vars_)])))
        vars_.append(v)
    kinds = []
    for _ in range(rng.randint(2, 4)):
        mods, key = rng.choice(MODS), rng.choice(KEYS)
        k = rng.choice(["ws", "resize", "exec", "move", "escaped", "unclosed", "desc", "var"])
        kinds.append(k)
        e1, e2 = expr(rng, vars_), expr(rng, vars_)
        if k == "ws":
            lines.append("bind = %s, %s, workspace, %s" % (mods, key, e1))
        elif k == "resize":
            lines.append("bind = %s, %s, resizeactive, %s %s" % (mods, key, e1, e2))
        elif k == "exec":
            lines.append("bind = %s, %s, exec, notify-send r26 %s" % (mods, key, e1))
        elif k == "move":
            lines.append("binde = %s, %s, moveactive, %s -%s" % (mods, key, e1, e2))
        elif k == "escaped":
            lines.append("bind = %s, %s, exec, echo \\%s" % (mods, key, e1))
        elif k == "unclosed":
            lines.append("bind = %s, %s, exec, echo {{%d + %d" % (mods, key, rng.randint(1, 9), rng.randint(1, 9)))
        elif k == "desc":
            lines.append("bindd = %s, %s, Size %s, resizeactive, %s 0" % (mods, key, e1, e2))
        else:
            v = "$ar" + "".join(rng.choice("klmnop") for _ in range(4))
            lines.append("%s = %s" % (v, e1))
            lines.append("bind = %s, %s, workspace, %s" % (mods, key, v))
    with open(target, "a", encoding="utf-8") as fh:
        fh.write("\n" + "\n".join(lines) + "\n")
    return "ARITH[%s]@%s" % ("+".join(kinds), "root" if target == root else "sourced")


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
    print("counter c2-r26 sha256:%s rev=%s oracle.py sha256:%s count-v3.py sha256:%s" % (O.sha(me), rev, ORACLE_SHA, V3_SHA))
    core0 = O.coredumps()
    tmp = tempfile.mkdtemp(prefix="m26c2-", dir="/fast/scratch/hyaku/mado-r26")
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
        jobs = max(1, min(a.jobs, O.SLOTS))
        with concurrent.futures.ThreadPoolExecutor(2) as ex:
            f1 = ex.submit(O.oracle, snap0, tempfile.mkdtemp(dir=tmp), ["binds"])
            f2 = ex.submit(O.oracle, snap0, tempfile.mkdtemp(dir=tmp), ["binds"])
            (r1, e1), (r2, e2) = f1.result(), f2.result()
        if r1 is None or r2 is None:
            die("ORACLE_FAIL BASE: %s %s" % (e1, e2))
        base = r1["binds"]
        n1, n2 = V3.compare(base, r2["binds"])[:2]
        if n1 or n2:
            die("ORACLE_UNSTABLE two oracle runs of the unperturbed snapshot disagree (%d/%d)" % (n1, n2))
        print("ORACLE_CHECK base_twice equal binds=%d" % len(base))
        embed_hits = 0
        if tb is not None:
            text = tb.decode("utf-8", errors="replace")
            strs = {e[f] for e in base for f in ("arg", "description") if isinstance(e.get(f), str) and len(e[f]) >= EMBED_MIN}
            hits = sorted(s for s in strs if s in text)
            embed_hits = len(hits)
            for s in hits[:5]:
                print("EMBED_HIT %r" % s[:60])
        built = [("BASE", snap0, "unperturbed")]
        files = None
        for i in range(NARITH):
            home = tempfile.mkdtemp(dir=tmp)
            shutil.copytree(snap0, home, dirs_exist_ok=True)
            files = V3.sourced_files(home)
            built.append(("A%02d" % i, home, arith_case(rng, home, files)))
        gen = V3.Gen(rng, base)
        for t in V3.TYPES:
            for i in range(V3_PER_TYPE):
                home = tempfile.mkdtemp(dir=tmp)
                shutil.copytree(snap0, home, dirs_exist_ok=True)
                desc, _model = V3.perturb(t, rng, home, base, gen)
                built.append(("V%s-%d" % (t, i), home, desc))
        with concurrent.futures.ThreadPoolExecutor(jobs) as ex:
            futs = {lab: ex.submit(O.oracle, home, tempfile.mkdtemp(dir=tmp), ["binds"]) for lab, home, _ in built[1:]}
            truth = {lab: f.result() for lab, f in futs.items()}
        for lab, (res, err) in sorted(truth.items()):
            if res is None:
                die("ORACLE_FAIL %s: %s" % (lab, err))
        truth["BASE"] = (r1, "")
        order = list(built)
        random.Random(os.urandom(8)).shuffle(order)
        verdict = {}
        for lab, home, desc in order:
            exp = truth[lab][0]["binds"]
            if tb is None:
                verdict[lab] = (False, "tool absent", len(exp))
                continue
            got, err = O.run_tool(tool, home)
            if not (isinstance(got, list) and all(isinstance(e, dict) for e in got)):
                verdict[lab] = (False, err or "stdout is not a JSON array of objects", len(exp))
                continue
            nm, ne, missing, extra = V3.compare(got, exp)
            info = "missing=%d extra=%d" % (nm, ne)
            for k in list(missing)[:2]:
                info += " | missing " + V3.brief(k)
            for k in list(extra)[:2]:
                info += " | extra " + V3.brief(k)
            verdict[lab] = (nm == 0 and ne == 0, info, len(exp))
        npass = 0
        for lab, home, desc in built:
            ok, info, nexp = verdict[lab]
            npass += ok
            print("CASE %-14s %s oracle_binds=%d %s (%s)" % (lab, "PASS" if ok else "FAIL", nexp, info, desc[:120]))
        core1 = O.coredumps()
        print("HOST_SAFETY hyprland_coredumps_before=%d after=%d delta=%d" % (core0, core1, core1 - core0))
        met = npass == len(built) and embed_hits == 0
        print("PRED-C2-r26 cases_pass=%d/%d embed_hits=%d verdict=%s" % (
            npass, len(built), embed_hits, "TARGET_MET" if met else "TARGET_MISSED"))
        return 0 if met else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    rc = main()
    print("exit=%d" % rc)
    sys.exit(rc)
