#!/usr/bin/env python3
"""R56W2MutC1CounterA -- randomized differential for the mutants claimed EQUIVALENT.

Each trial applies ONE random byte-level perturbation to the entry, the registry or the README of a
fresh scratch repo (built from the 28fc86ac archive), then runs the pristine counter and every
equivalence candidate on that repo and compares stdout and exit status. A divergence would refute the
equivalence argument; zero divergences is EMPIRICAL support only, reported as such.

Usage: python3 -I equiv_fuzz.py --base SCRATCH_BASE --rev REV --scratch DIR --trials N --seed S
"""
import argparse
import importlib.util
import json
import os
import random
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


mutate = load("mutate", os.path.join(HERE, "mutate.py"))
killers = load("killers", os.path.join(HERE, "killers.py"))

CANDIDATES = ["M02", "M11", "M46", "M60", "M61"]
TARGETS = [killers.ENTRY, killers.REG, killers.README]


def perturb(rng, D):
    rel = rng.choice(TARGETS)
    data = killers.rd(D, rel).decode("utf-8")
    lines = data.split("\n")
    idxs = [i for i, l in enumerate(lines) if l.strip()]
    i = rng.choice(idxs)
    line = lines[i]
    op = rng.choice(["del", "ins_pipe", "ins_space", "ins_char", "sub_digit", "dup_line", "tab_pipe",
                     "double_space"])
    if op == "del" and line:
        k = rng.randrange(len(line))
        line = line[:k] + line[k + 1:]
    elif op == "ins_pipe":
        k = rng.randrange(len(line) + 1)
        line = line[:k] + "|" + line[k:]
    elif op == "ins_space":
        k = rng.randrange(len(line) + 1)
        line = line[:k] + " " + line[k:]
    elif op == "ins_char":
        k = rng.randrange(len(line) + 1)
        line = line[:k] + rng.choice("Sx9K`-_. ") + line[k:]
    elif op == "sub_digit":
        ds = [k for k, c in enumerate(line) if c.isdigit()]
        if ds:
            k = rng.choice(ds)
            line = line[:k] + str((int(line[k]) + rng.randrange(1, 9)) % 10) + line[k + 1:]
    elif op == "dup_line":
        lines.insert(i, line)
        killers.put_lines(D, rel, lines)
        return "%s dup_line@%d" % (rel, i)
    elif op == "tab_pipe":
        line = line.replace(" | ", "\t| ", 1)
    elif op == "double_space":
        line = line.replace(" | ", "  | ", 1)
    lines[i] = line
    killers.put_lines(D, rel, lines)
    return "%s %s@%d" % (rel, op, i)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--trials", type=int, default=60)
    ap.add_argument("--seed", type=int, default=56)
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    scratch = os.path.abspath(a.scratch)
    os.makedirs(scratch, exist_ok=True)
    src = mutate.read_pristine(a.base, a.rev)
    pristine_lines = src.split("\n")
    ppath = os.path.join(scratch, "eq-pristine.py")
    with open(ppath, "w", encoding="utf-8") as fh:
        fh.write(src)
    mpaths = {}
    for mid in CANDIDATES:
        _, label, ln, old, new = [m for m in mutate.MUTANTS if m[0] == mid][0]
        ml, err = mutate.apply_mutant(pristine_lines, ln, old, new)
        assert err is None, err
        p = os.path.join(scratch, "eq-%s.py" % mid)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("\n".join(ml))
        mpaths[mid] = p
    rng = random.Random(a.seed)
    stats = {mid: {"runs": 0, "diverge": 0, "examples": []} for mid in CANDIDATES}
    baseline_diverge = 0
    for t in range(a.trials):
        D = None
        import tempfile
        D = tempfile.mkdtemp(prefix="eq-%03d-" % t, dir=scratch)
        import subprocess
        subprocess.run(["git", "-C", a.base, "archive", a.rev, "--", killers.ENTRY, killers.REG,
                        killers.README, killers.TABLES, killers.FETCH],
                       check=True, stdout=open(os.path.join(scratch, "_eq.tar"), "wb"))
        subprocess.run(["tar", "-x", "-C", D, "-f", os.path.join(scratch, "_eq.tar")], check=True)
        subprocess.run(["git", "-C", D, "init", "-q"], check=True)
        top = subprocess.run(["git", "-C", D, "rev-parse", "--show-toplevel"], capture_output=True,
                             text=True, check=True).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(D), (top, D)
        desc = perturb(rng, D)
        subprocess.run(["git", "-C", D, "add", "-A"], check=True)
        subprocess.run(["git", "-C", D, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "-c",
                        "commit.gpgsign=false", "commit", "-q", "-m", "eq %d" % t], check=True)
        sha = subprocess.run(["git", "-C", D, "rev-parse", "HEAD"], capture_output=True, text=True,
                             check=True).stdout.strip()
        work = os.path.join(scratch, "eqw")
        pr = killers.run_counter(ppath, D, sha, work)
        for mid in CANDIDATES:
            mr = killers.run_counter(mpaths[mid], D, sha, work)
            stats[mid]["runs"] += 1
            if (mr["out"], mr["rc"]) != (pr["out"], pr["rc"]):
                stats[mid]["diverge"] += 1
                if len(stats[mid]["examples"]) < 3:
                    stats[mid]["examples"].append({"trial": t, "edit": desc,
                                                   "pristine": pr["out"].strip()[:200],
                                                   "mutant": (mr["out"] or mr["err"])[:200]})
        shutil.rmtree(D, ignore_errors=True)
    try:
        os.remove(os.path.join(scratch, "_eq.tar"))
    except OSError:
        pass
    out = a.out or os.path.join(scratch, "equiv_fuzz.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"trials": a.trials, "seed": a.seed, "stats": stats}, fh, indent=1, ensure_ascii=False)
    for mid in CANDIDATES:
        print("%s trials=%d divergences=%d" % (mid, stats[mid]["runs"], stats[mid]["diverge"]))
    print("results: %s" % out)


if __name__ == "__main__":
    main()
