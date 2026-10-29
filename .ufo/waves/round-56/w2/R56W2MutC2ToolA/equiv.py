#!/usr/bin/env python3
"""Equivalence prover for the round-56 w2 mutation run (seat R56W2MutC2ToolA).

For a mutant that no proposed fixture killed, decide EQUIVALENT vs DISTINGUISHED by in-process differential
testing: import the pristine tool and the mutant as modules, call `run(argv)` on a broad generated corpus of
config trees and argument sets, and compare the returned lines and exit codes. Equal on every case means no
observed behaviour change on the corpus. A single difference refutes equivalence (and is printed).

The mutant's output is the tool's output, so this compares exactly the observable contract (stdout lines and rc).

Usage: python3 -I equiv.py --repo DIR --work DIR --out DIR --mutants M73,M77,...
"""
import importlib.util
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mutate import MUTANTS, TOOL_REL  # noqa: E402

CONFIGS = [
    b"", b"\n\n\n", b"# just a comment\n", b"#\n", b"# misc {\n", b"# misc:disable_autoreload = 1\n",
    b"; a semicolon line\n", b"; note {\n", b"} stray close\n", b"}}}\n", b"misc {\n}\n",
    b"misc {\n  disable_autoreload = 1\n}\n", b"misc:disable_autoreload = 1\n", b"misc:disable_autoreload = 0\n",
    b"misc:disable_autoreload =  1\n", b"misc:disable_autoreload =1\n", b"misc:disable_autoreload =1 # c\n",
    b"misc:disable_autoreload = 1 # c\n", b"misc:disable_autoreload = 1 ## x\n", b"misc:disable_autoreload = 1 ##x\n",
    b"misc:disable_autoreload = on$x\n", b"misc:disable_autoreload = off\\\n", b"misc:disable_autoreload = on{\n",
    b"misc:disable_autoreload = 1!\n", b"misc:disable_autoreload = 1abc\n", b"misc:disable_autoreload = maybe\n",
    b"misc:disable_autoreload = true\n", b"misc:disable_autoreload = online\n", b"misc:disable_autoreload = yes\n",
    b"misc:disable_autoreload = no\n", b"misc:disable_autoreload = none\n", b"misc:disable_autoreload = 007\n",
    b"misc:disable_autoreload = 000\n", b"misc:disable_autoreload = 12\n", b"misc:disable_autoreload = -1\n",
    b"misc:disable_autoreload = 1.5\n", b"misc:disable_autoreload = True\n", b"misc:disable_autoreload = $V\n",
    b"$V = 1\nmisc:disable_autoreload = 1\n", b"$\n", b"$ = 1\n", b"misc:disable_autoreload$ = 1\n",
    b"misc:disable_autoreload = 1 $ x\n", b"misc:disable_autoreload = 1 { x }\n",
    b"misc {\n  disable_autoreload = on$x\n}\n", b"misc {\n  disable_autoreload = 1 ## x\n}\n",
    b"misc {\n  source = x.conf\n}\n", b"misc {\n  disable_autoreload = 1\n}\nmisc:disable_autoreload = 0\n",
    b"source = a.conf\n", b"source = a.conf\nsource = a.conf\n", b"source = nothing/*.conf\n", b"source = x\n",
    b"source = .\n", b"source = /dev/null\n", b"source = ~/a.conf\n", b"source = a\\b\n",
    b"source = mix/*.conf\n", b"source = *[\n", b"source = [x\n", b"source = ../out/*.conf\n", b"source = sub\n",
    b"source = conf.d/*.conf\n", b"source = out/a.conf\n", b"source = ./out/a.conf\n", b"source = ../tree/out/a.conf\n",
    b"source = .hidden.conf\n", b"source = ..x\n",
    b"general {\n  x = 1\n}\n", b"general {\n", b"x = 1\n", b"a = b = c\n",
    b"misc:disable_autoreload = 1\nmisc:disable_autoreload = 0\n",
    b"misc:disable_autoreload = 0\nmisc:disable_autoreload = 1\n",
    b"\xff\xfe not utf8\nmisc:disable_autoreload = 1\n",
    b"misc {\n  x = 1\n", b"misc {\n}\n}\nmisc:disable_autoreload = 1\n",
    b"  misc:disable_autoreload = 1  \n", b"\tmisc:disable_autoreload\t=\t1\t\n",
    b"misc:disable_autoreload = 1\r\n", b"misc:disable_autoreload = 1\x0b\n",
]
GETOPTION = [
    None, b"", b'{"option": "misc:disable_autoreload", "int": 0}\n',
    b'{"option": "misc:disable_autoreload", "int": 1}\n', b'{"option": "misc:disable_autoreload", "int": false}\n',
    b'{"option": "misc:disable_autoreload", "int": 0.0}\n', b'{"option": "misc:disable_autoreload", "int": -1}\n',
    b'{"option": "misc:disable_autoreload", "value": 1}\n', b'{"option": "misc:x", "int": 0}\n',
    b'{"option": "misc:disable_autoreload", "int": 1}\n{"option": "misc:disable_autoreload", "int": 0}\n',
    b"[1]\n", b"null\n", b"{bad\n", b'{"int": NaN}\n',
    b'{"option": "misc:disable_autoreload", "int": 2}\n', b'{"option": "misc:disable_autoreload", "int": 00}\n',
]


def build_tree(root):
    def put(rel, data):
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(data)
    put("hyprland.conf", b"misc:disable_autoreload = 0\n")
    put("a.conf", b"x = 1\n")
    put("conf.d/a.conf", b"x = 1\n")
    put("conf.d/b.conf", b"x = 2\n")
    put("conf.d/.hidden.conf", b"x = 3\n")
    put("mix/a.conf", b"x = 1\n")
    os.symlink("missing-target.conf", os.path.join(root, "mix", "b.conf"))
    put("out/a.conf", b"x = 1\n")
    put("home/a.conf", b"x = 1\n")
    os.makedirs(os.path.join(root, "sub"), exist_ok=True)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    repo = work = out = None
    want = []
    i = 0
    while i < len(argv):
        if argv[i] == "--repo":
            repo = argv[i + 1]; i += 2
        elif argv[i] == "--work":
            work = argv[i + 1]; i += 2
        elif argv[i] == "--out":
            out = argv[i + 1]; i += 2
        elif argv[i] == "--mutants":
            want = argv[i + 1].split(","); i += 2
        else:
            print("usage"); return 2
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    os.makedirs(out, exist_ok=True)
    pristine_path = os.path.join(repo, TOOL_REL)
    pristine_src = open(pristine_path, "rb").read().decode("utf-8")
    pristine = load("pristine", pristine_path)

    stage = os.path.join(work, "stage")
    build_tree(os.path.join(stage, "tree"))
    cases = []
    for ci, body in enumerate(CONFIGS):
        cfg = os.path.join(stage, "tree", "cfg%03d.conf" % ci)
        with open(cfg, "wb") as fh:
            fh.write(body)
        for gi, go in enumerate(GETOPTION):
            gp = None
            if go is not None:
                gp = os.path.join(work, "go%03d.json" % gi)
                with open(gp, "wb") as fh:
                    fh.write(go)
            for extra in ([], ["--home", os.path.join(stage, "tree", "home")], ["--home", os.path.join(stage, "tree") + "/"]):
                args = ["--config", cfg, "--display-root", os.path.join(stage, "tree")] + extra
                if gp is not None:
                    args += ["--getoption", gp]
                cases.append(args)
    for extra in (["--config", "rel.conf"], ["--config", os.path.join(stage, "tree")],
                  ["--display-root", os.path.join(stage, "tree")],
                  ["--config", "/dev/null", "--display-root", os.path.join(stage, "tree")],
                  ["--config", os.path.join(stage, "tree", "hyprland.conf"), "--getoption", "/dev/null"],
                  ["--config", os.path.join(stage, "tree", "hyprland.conf"), "--getoption", os.path.join(stage, "tree")],
                  ["--config", os.path.join(stage, "tree", "hyprland.conf"), "--config", "/x"],
                  ["--config", os.path.join(stage, "tree", "hyprland.conf"), "--home", "relative"],
                  ["--config", os.path.join(stage, "tree", "hyprland.conf"), "--display-root", os.path.join(stage, "tree", "")],
                  ["--config", os.path.join(stage, "tree", "hyprland.conf"), "--display-root", os.path.join(stage, "tree", "out")],
                  ["--config", os.path.join(stage, "tree", "hyprland.conf"), "--display-root", os.path.join(stage, "tree", "out") + "/"]):
        cases.append(extra)

    print("corpus cases: %d" % len(cases))
    pristine_out = [pristine.run(list(a)) for a in cases]
    results = {}
    for mid in want:
        m = [x for x in MUTANTS if x[0] == mid][0]
        if pristine_src.count(m[2]) != 1:
            print("%s: snippet ambiguous" % mid); continue
        mpath = os.path.join(out, "equiv-%s.py" % mid)
        with open(mpath, "wb") as fh:
            fh.write(pristine_src.replace(m[2], m[3]).encode("utf-8"))
        mutant = load("mutant_" + mid, mpath)
        diffs = []
        for n, args in enumerate(cases):
            mo = mutant.run(list(args))
            if mo != pristine_out[n]:
                diffs.append({"args": [a.replace(stage, "<S>") for a in args],
                              "pristine": [pristine_out[n][0], pristine_out[n][1]] if isinstance(pristine_out[n][0], list) else pristine_out[n],
                              "mutant": mo})
        verdict = "EQUIVALENT" if not diffs else "DISTINGUISHED"
        results[mid] = {"mutant": mid, "cases": len(cases), "diffs": len(diffs), "verdict": verdict,
                        "examples": diffs[:3]}
        print("%-6s %-14s differences in %d/%d cases" % (mid, verdict, len(diffs), len(cases)))
    with open(os.path.join(out, "equiv-results.json"), "w") as fh:
        json.dump(results, fh, indent=1, default=str)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
