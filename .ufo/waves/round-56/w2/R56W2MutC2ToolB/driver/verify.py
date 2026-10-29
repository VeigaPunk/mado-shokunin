#!/usr/bin/env python3
"""R56W2MutC2ToolB: verify each candidate killing fixture through the UNCHANGED C2 harness functions.

For each (mutant, fixture) in cands.CANDS:
  1. materialise the fixture dir (args.json, tree/ with symlinks, raw-byte names) under <work>/candfx/<mid>/
  2. expected.out / expected.rc := the PRISTINE tool run through the harness's own staged runner (bwrap)
  3. H.score(pristine) must be 1 (the fixture is a valid committed-style fixture: pristine passes it)
  4. H.score(mutant)  must be 0 (the fixture kills the mutant)
Output: one line per pair and a JSON receipt.
Usage: python3 -I verify.py --repo REPO --rev REV --work DIR --mutants survivor-tools.json --out DIR
"""
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
SAFE_PATH = "/usr/local/bin:/usr/bin:/bin"


def load_cands(path):
    spec = importlib.util.spec_from_file_location("cands", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CANDS


def materialise(root, spec):
    os.makedirs(root)
    with open(os.path.join(root, "args.json"), "w", encoding="utf-8") as fh:
        json.dump(spec["args"], fh, indent=1)
    tree = os.path.join(root, "tree")
    os.makedirs(tree)
    for d in spec.get("dirs", []):
        os.makedirs(os.path.join(tree, d), exist_ok=True)
    for name, content in spec.get("files", {}).items():
        p = os.path.join(tree, name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if isinstance(content, tuple) and content[0] == "link":
            os.symlink(content[1], p)
        else:
            with open(p, "wb") as fh:
                fh.write(content.encode("utf-8", "surrogateescape"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--mutants", required=True)
    ap.add_argument("--cands", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default=None)
    args = ap.parse_args()

    work = os.path.realpath(args.work)
    out_dir = os.path.realpath(args.out)
    os.makedirs(work, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    env = {"PATH": SAFE_PATH, "HOME": work, "TMPDIR": work, "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}

    # the unchanged harness module, from the lane at rev (read-only git)
    hsrc = subprocess.run(["git", "-C", args.repo, "show", "%s:quality/r56_ctl_c2.py" % args.rev],
                          stdout=subprocess.PIPE, check=True).stdout
    hdir = os.path.join(work, "harness-mod")
    shutil.rmtree(hdir, ignore_errors=True)
    os.makedirs(hdir)
    with open(os.path.join(hdir, "r56_ctl_c2.py"), "wb") as fh:
        fh.write(hsrc)
    sys.path.insert(0, hdir)
    import r56_ctl_c2 as H  # noqa: E402

    python = shutil.which("python3", path=SAFE_PATH)
    pristine = subprocess.run(["git", "-C", args.repo, "show", "%s:tools/mado-watchplan.py" % args.rev],
                              stdout=subprocess.PIPE, check=True).stdout
    ptool = os.path.join(hdir, "pristine-tool.py")
    with open(ptool, "wb") as fh:
        fh.write(pristine)
    with open(args.mutants, encoding="utf-8") as fh:
        mutants = json.load(fh)
    cands = load_cands(args.cands)
    only = set(args.only.split(",")) if args.only else None

    receipt = []
    for mid in sorted(cands):
        if only and mid not in only:
            continue
        mtool = mutants.get(mid)
        if mtool is None:
            receipt.append({"mutant": mid, "error": "no mutant tool"})
            continue
        for fid, spec in cands[mid]:
            fxroot = os.path.join(work, "candfx", mid)
            fxdir = os.path.join(fxroot, fid)
            shutil.rmtree(fxdir, ignore_errors=True)
            os.makedirs(fxroot, exist_ok=True)
            materialise(fxdir, spec)
            # expected bytes: the pristine tool through the harness's own staged runner
            stage = os.path.join(work, "st", mid, fid)
            shutil.rmtree(stage, ignore_errors=True)
            os.makedirs(stage)
            shutil.copytree(os.path.join(fxdir, "tree"), os.path.join(stage, "tree"), symlinks=True)
            cwd = os.path.join(work, "cw", mid, fid)
            shutil.rmtree(cwd, ignore_errors=True)
            os.makedirs(cwd)
            argv = H.fixture_args(fxdir, stage)
            exp_out, exp_rc = H.staged_run(python, ptool, argv, stage, cwd, env, sandbox=True)
            if exp_rc is None:
                receipt.append({"mutant": mid, "fixture": fid, "error": "pristine run failed"})
                continue
            with open(os.path.join(fxdir, "expected.out"), "wb") as fh:
                fh.write(exp_out)
            with open(os.path.join(fxdir, "expected.rc"), "w", encoding="utf-8") as fh:
                fh.write("%d\n" % exp_rc)
            # the harness's own scorer: pristine must pass, the mutant must fail
            sub_p = os.path.join(work, "sc", mid, fid, "p")
            sub_m = os.path.join(work, "sc", mid, fid, "m")
            for s in (sub_p, sub_m):
                shutil.rmtree(s, ignore_errors=True)
                os.makedirs(s)
            ppass = H.score(python, ptool, fxroot, fxroot, [fid], env, sub_p, True)
            mpass = H.score(python, mtool, fxroot, fxroot, [fid], env, sub_m, True)
            mout, mrc = H.staged_run(python, mtool, argv, stage, cwd, env, sandbox=True)
            verdict = "KILLED" if (ppass == 1 and mpass == 0) else "NOT-KILLED"
            rec = {"mutant": mid, "fixture": fid, "verdict": verdict, "pristine_harness_pass": ppass,
                   "mutant_harness_pass": mpass, "pristine_rc": exp_rc,
                   "pristine_out": exp_out.decode("utf-8", "replace"),
                   "mutant_rc": mrc, "mutant_out": (mout or b"").decode("utf-8", "replace")}
            receipt.append(rec)
            # keep the committed-style fixture for the report
            keep = os.path.join(out_dir, "fixtures", mid, fid)
            shutil.rmtree(keep, ignore_errors=True)
            os.makedirs(os.path.dirname(keep), exist_ok=True)
            shutil.copytree(fxdir, keep, symlinks=True)
            print("%s %s %s pristine=%d mutant=%d rc=%s/%s" % (mid, fid, verdict, ppass, mpass, exp_rc, mrc),
                  flush=True)

    with open(os.path.join(out_dir, "candidate-verify.json"), "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=1, ensure_ascii=False)
    kn = sum(1 for r in receipt if r.get("verdict") == "KILLED")
    print("CANDIDATES killed=%d of %d pairs" % (kn, len(receipt)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
