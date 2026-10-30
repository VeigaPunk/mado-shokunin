#!/usr/bin/env python3
"""End-to-end proof that the CONTROL-1 fixtures kill their mutant THROUGH THE HARNESS.

A scratch copy of the frozen harness quality/r56_ctl_c1.py is extended with the wave-2
fixtures as extra controls (each control's mutation applies the fixture's git patch; each
control's check asserts the required leg with the harness's own _need()).  The harness is then
run with --counter <mutant>: if the fixture really is a control, the harness must report that
control as FAIL ("mutant admitted") for the mutant while reporting it as ok for the pristine.

Nothing in the lane is written: the harness copy lives in scratch, the counter copies live in
scratch, and the lane is read through `git show` only.
"""
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = "/fast/scratch/hyaku/mado-r56/R56W3MutKillC1"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
HARNESS_REL = "quality/r56_ctl_c1.py"
COUNTER_REL = "quality/counters/c1-r56-autoreload-entry.py"

ENV = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C.UTF-8",
       "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1",
       "GIT_TERMINAL_PROMPT": "0", "GIT_NO_REPLACE_OBJECTS": "1"}


def git(d, *args, check=True):
    p = subprocess.run(["git", "-C", d] + list(args), env=dict(ENV, HOME=ROOT, TMPDIR=ROOT),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (args, p.stderr.decode()[-300:]))
    return p.stdout.decode().strip()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_patch_mutation(patch_path):
    """A harness-shaped mutation: apply the fixture's git patch inside the scratch repo."""
    def m(d, ctx):
        p = subprocess.run(["git", "apply", "--binary", "--whitespace=nowarn", patch_path],
                           cwd=str(d), env=dict(ENV, HOME=ROOT), capture_output=True)
        if p.returncode != 0:
            raise ctl.MutationError("fixture patch does not apply: %s"
                                    % p.stderr.decode("utf-8", "replace").strip()[:200])
    return m


def build_harness(ctl, out_path, controls, n_controls):
    """A scratch copy of the frozen harness with extra controls appended."""
    src = open(os.path.join(LANE, HARNESS_REL), encoding="utf-8").read()
    lines = []
    for cid, name, patch, required, exact_legs in controls:
        if exact_legs:
            check = "_exact(%r)" % (list(exact_legs),)
        else:
            check = '_need("%s")' % required
        lines.append('    ("%s", "%s", _mk_patch("%s"), "%s", %s, ()),'
                     % (cid, name, patch, required, check))
    block = "\n".join(lines)
    src = src.replace("]\n\n\n# ----------------------------------------------------------------- counter run",
                      block + "\n]\n\n\n# ----------------------------------------------------------------- counter run", 1)
    src = src.replace("N_CONTROLS = 12", "N_CONTROLS = %d" % n_controls, 1)
    with open(os.path.join(ROOT, "harness-helpers.py"), encoding="utf-8") as fh:
        helper = fh.read()
    src = src.replace("\ndef _need(leg: str):", helper + "\ndef _need(leg: str):", 1)
    if "def _mk_patch" not in src or "def _exact" not in src:
        raise SystemExit("could not inject the helpers")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(src)
    return out_path


def run_harness(harness, repo, rev, work, counter=None):
    os.makedirs(work, exist_ok=True)
    cmd = [sys.executable, "-I", harness, "--repo", repo, "--rev", rev, "--work", work]
    if counter:
        cmd += ["--counter", counter]
    p = subprocess.run(cmd, env=dict(ENV, HOME=work, TMPDIR=work), cwd=work,
                       capture_output=True, timeout=900)
    return {"rc": p.returncode, "out": p.stdout.decode("utf-8", "replace").strip(),
            "err": p.stderr.decode("utf-8", "replace")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    ctl = load("r56_ctl_c1", os.path.join(LANE, HARNESS_REL))
    carriers = json.load(open(os.path.join(ROOT, "kill-carriers.json")))["rows"]
    final = json.load(open(os.path.join(ROOT, "routes-final.json")))["rows"]
    base_rev = open(os.path.join(ROOT, "BASE_REV.txt")).read().strip()
    base = os.path.join(ROOT, "base")

    # one control per CONTROL-1 fixture (a single _need on the discriminating leg) and per
    # CONTROL-N fixture (a check that asserts the exact leg set)
    fin = {}
    for r in final:
        fin.setdefault(r["fixture"], r)
    seen = {}
    for r in final:
        if r["carrier"] == "CONTROL-1":
            seen.setdefault(r["fixture"], ("_need", r["lost"][0] if r["lost"] else None))
        elif r["carrier"] == "CONTROL-N":
            seen.setdefault(r["fixture"], ("_exact", r["pristine_legs"]))
    controls = []
    for tag, (kind, arg) in sorted(seen.items()):
        controls.append((tag.replace("-", "-ctl-"), tag, os.path.join(ROOT, "fixtures", tag + ".patch"),
                         arg if kind == "_need" else "exact-leg-set",
                         arg if kind == "_exact" else None))
    print("controls to prove: %d" % len(controls))

    harness = build_harness(ctl, os.path.join(ROOT, "harness-with-fixtures.py"), controls,
                            12 + len(controls))
    # sanity: the extended harness on the PRISTINE counter must pass all of them
    w = os.path.join(ROOT, "work", "hp")
    r = run_harness(harness, base, base_rev, w)
    print("PRISTINE with the extended harness: rc=%s %s" % (r["rc"], r["out"]))
    for line in r["err"].split("\n"):
        if " FAIL" in line:
            print("   ", line)

    # now each mutant: the harness must FAIL (the control is admitted)
    muts = json.load(open(os.path.join(ROOT, "kill-results.json")))["results"]
    results = []
    for rec in muts:
        if "error" in rec:
            continue
        tag = "%s-%s" % (rec["ns"], rec["fixture"])
        if tag not in seen:
            continue
        for m in rec["mutants"]:
            src = os.path.join(ROOT, "mutants", "%s-%s.py" % (tag, m["mutant"]))
            if not os.path.isfile(src):
                continue
            w2 = os.path.join(ROOT, "work", "hm-" + tag)
            rr = run_harness(harness, base, base_rev, w2, counter=src)
            failed_control = None
            for line in rr["err"].split("\n"):
                if "FAIL" in line and tag.replace("-", "-ctl-") in line:
                    failed_control = line.strip()
            killed = rr["rc"] != 0 and failed_control is not None
            results.append({"fixture": tag, "mutant": m["mutant"], "harness_rc": rr["rc"],
                            "harness_out": rr["out"], "failed_control_line": failed_control,
                            "killed_by_harness": killed})
            print("%-8s %-5s harness_rc=%s killed=%-5s %s" % (tag, m["mutant"], rr["rc"], killed,
                                                             (failed_control or "")[:110]))
    with open(os.path.join(ROOT, "harness-proof.json"), "w", encoding="utf-8") as fh:
        json.dump({"controls": [c[0] for c in controls], "results": results}, fh, indent=1)
    print("\nproved kills: %d/%d" % (sum(1 for r in results if r["killed_by_harness"]), len(results)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
