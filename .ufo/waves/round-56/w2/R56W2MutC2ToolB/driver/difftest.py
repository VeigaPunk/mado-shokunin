#!/usr/bin/env python3
"""R56W2MutC2ToolB: differential probe for the surviving mutants.

For each survivor, build many random config trees + argument sets, run the PRISTINE tool and the
MUTANT, and report any input where the outputs differ. A difference proves the mutant is
behaviour-distinguishable (a coverage gap in the 26 fixtures + selftest); no difference over a
broad input space suggests the mutant is observationally EQUIVALENT on the reachable behaviour.

Usage: python3 -I difftest.py --repo REPO --rev REV --work DIR --mutants FILE --out FILE [--iters N]
"""
import argparse
import json
import os
import random
import shutil
import subprocess
import sys

SAFE_PATH = "/usr/local/bin:/usr/bin:/bin"

WORDS = ["misc", "general", "source", "disable_autoreload", "a.conf", "b.conf", "sub/c.conf",
         "./rel.conf", "../up.conf", "~/h.conf", "x", "*.conf", "conf.d/*.conf", "~/g/*.conf",
         "# comment", "}", "{", "misc {", "general {", "z = 3", "misc:disable_autoreload = 1",
         "misc:disable_autoreload = on", "misc:disable_autoreload = off", "misc:disable_autoreload = 0",
         "misc:disable_autoreload = 2", "misc:disable_autoreload = maybe", "$V = 1",
         "misc:disable_autoreload = $V", "misc:disable_autoreload = 1 ## x", "source = sub",
         "source = /dev/null", "source = .", "source = ~", "source = ~x", "source = a\\b",
         "source = [x", "source = a[", "source = *[", "misc:disable_autoreload = 1 # c",
         "general { disable_autoreload = 1 }", "}", "  ", "\t", "misc:disable_autoreload = 007",
         "misc:disable_autoreload = none", "misc:disable_autoreload = True", "misc:disable_autoreload = 1.5"]


def build_tree(rng, root):
    """random tree under root"""
    os.makedirs(root, exist_ok=True)
    names = ["a.conf", "b.conf", "sub", "conf.d", "home"]
    for n in names:
        if rng.random() < 0.7:
            p = os.path.join(root, n)
            if n in ("sub", "conf.d", "home"):
                os.makedirs(p, exist_ok=True)
            else:
                with open(p, "wb") as fh:
                    fh.write(b"z = 3\n")
    if os.path.isdir(os.path.join(root, "conf.d")):
        for n in ("c.conf", "C.conf", ".hid.conf"):
            if rng.random() < 0.6:
                with open(os.path.join(root, "conf.d", n), "wb") as fh:
                    fh.write(b"")
    if os.path.isdir(os.path.join(root, "sub")):
        with open(os.path.join(root, "sub", "deep.conf"), "wb") as fh:
            fh.write(b"source = ../b.conf\n")
    # a symlink and a dangling symlink
    if rng.random() < 0.5:
        tgt = "b.conf" if os.path.exists(os.path.join(root, "b.conf")) else "nope"
        try:
            os.symlink(tgt, os.path.join(root, "link.conf"))
        except OSError:
            pass
    if rng.random() < 0.3:
        try:
            os.symlink("missing-target.conf", os.path.join(root, "dangling.conf"))
        except OSError:
            pass
    if rng.random() < 0.3:
        os.makedirs(os.path.join(root, "dir.conf"), exist_ok=True)


def gen_config(rng):
    lines = []
    for _ in range(rng.randint(1, 6)):
        lines.append(rng.choice(WORDS))
    return "\n".join(lines) + "\n"


def run_tool(tool, args, cwd, env):
    try:
        p = subprocess.run([sys.executable, "-I", tool] + args, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        return p.stdout, p.returncode
    except (subprocess.TimeoutExpired, OSError):
        return b"", -99


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--mutants", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--iters", type=int, default=300)
    ap.add_argument("--seed", type=int, default=12345)
    args = ap.parse_args()

    work = os.path.realpath(args.work)
    os.makedirs(work, exist_ok=True)
    env = {"PATH": SAFE_PATH, "HOME": work, "TMPDIR": work, "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
    pristine = subprocess.run(["git", "-C", args.repo, "show", "%s:tools/mado-watchplan.py" % args.rev],
                              stdout=subprocess.PIPE).stdout
    ptool = os.path.join(work, "pristine.py")
    with open(ptool, "wb") as fh:
        fh.write(pristine)
    with open(args.mutants, encoding="utf-8") as fh:
        mutants = json.load(fh)

    out = {}
    for mid, tool in sorted(mutants.items()):
        rng = random.Random(args.seed)
        diffs = []
        for i in range(args.iters):
            root = os.path.join(work, "probe", mid)
            shutil.rmtree(root, ignore_errors=True)
            os.makedirs(root)
            tree = os.path.join(root, "tree")
            build_tree(rng, tree)
            with open(os.path.join(tree, "hyprland.conf"), "w", encoding="utf-8") as fh:
                fh.write(gen_config(rng))
            argv = ["--config", os.path.join(tree, "hyprland.conf")]
            if rng.random() < 0.8:
                argv += ["--display-root", root]
            if rng.random() < 0.4:
                argv += ["--home", os.path.join(tree, "home")]
            if rng.random() < 0.4:
                go = os.path.join(tree, "go.json")
                with open(go, "w", encoding="utf-8") as fh:
                    fh.write(rng.choice([
                        '{"option": "misc:disable_autoreload", "int": 0}\n',
                        '{"option": "misc:disable_autoreload", "int": 1}\n',
                        '{"option": "misc:disable_autoreload", "int": true}\n',
                        '{"option": "misc:x", "int": 0}\n',
                        '', '[1,2]\n', '{"option": "misc:disable_autoreload", "int": 0}\n\n'
                        '{"option": "misc:disable_autoreload", "int": 1}\n']))
                argv += ["--getoption", go]
            po, prc = run_tool(ptool, argv, root, env)
            mo, mrc = run_tool(tool, argv, root, env)
            if po != mo or prc != mrc:
                diffs.append({"iter": i, "argv": [a.replace(root, "$R") for a in argv],
                              "config": open(os.path.join(tree, "hyprland.conf")).read(),
                              "pristine_rc": prc, "mutant_rc": mrc,
                              "pristine_out": po.decode("utf-8", "replace").replace(root, "$R"),
                              "mutant_out": mo.decode("utf-8", "replace").replace(root, "$R")})
                break
        out[mid] = {"distinguishable": bool(diffs), "example": diffs[0] if diffs else None}
        print("%s distinguishable=%s" % (mid, bool(diffs)), flush=True)
        if diffs:
            e = diffs[0]
            print("   argv=%r config=%r" % (e["argv"], e["config"]), flush=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
