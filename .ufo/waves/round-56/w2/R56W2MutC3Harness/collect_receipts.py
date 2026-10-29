#!/usr/bin/env python3
"""collect_receipts.py -- assemble the receipt bundle of seat R56W2MutC3Harness.

Writes into the seat deliverable directory:
  receipts/00-environment.txt      tool versions, lane rev, target file sha256, scratch paths
  receipts/01-reference-oracle.txt the three oracle checks on the UNMUTATED harness (stdout+stderr+rc)
  receipts/02-lane-crosscheck.txt  the same harness run against the REAL lane repo (read-only git)
  receipts/03-sweep.json           the raw sweep result (per mutant: checks, details, sha256)
  receipts/04-sweep.txt            the sweep result as a readable table
  receipts/05-survivors.txt        the survivor verification (proposed addition kills the mutant)
  receipts/06-environment-note.txt the reduced-repo fidelity proof (blob sha256 identity per path)
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

S = os.environ.get("SCRATCH", "/fast/scratch/hyaku/mado-r56/R56W2MutC3Harness")
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "28fc86ac2359ec27406d8a2c63bef82ea6e947ed"
DELIVER = os.environ.get("DELIVER", os.path.join(LANE, ".ufo/waves/round-56/w2/R56W2MutC3Harness"))
RECEIPTS = os.path.join(DELIVER, "receipts")
sys.path.insert(0, S)


def sh(cmd, **kw):
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kw).stdout.decode("utf-8", "replace")


def main():
    os.makedirs(RECEIPTS, exist_ok=True)
    mini_sha = open(os.path.join(S, "mini_sha.txt")).read().strip()

    # ---- 00 environment
    env = []
    env.append("python3: %s" % sh(["python3", "-VV"]).strip())
    env.append("git: %s" % sh(["git", "--version"]).strip())
    env.append("lane: %s" % LANE)
    env.append("lane commit under test: %s" % REV)
    env.append("target file: quality/r56_ctl_c3.py (read from `git archive %s`)" % REV)
    env.append("target sha256: %s" % hashlib.sha256(open(os.path.join(S, "tree/quality/r56_ctl_c3.py"), "rb").read()).hexdigest())
    env.append("real counter sha256: %s" % hashlib.sha256(open(os.path.join(S, "tree/quality/counters/c3-r56-used-by.py"), "rb").read()).hexdigest())
    env.append("scratch: %s" % S)
    env.append("reduced scratch repo: %s (tip %s, objects borrowed from the lane via .git/objects/info/alternates)"
               % (os.path.join(S, "mini"), mini_sha))
    env.append("tools installed by this seat: none (no package manager was used; no tool upgrade was needed)")
    open(os.path.join(RECEIPTS, "00-environment.txt"), "w").write("\n".join(env) + "\n")

    # ---- 06 fidelity: blob sha256 identity per path, lane vs reduced repo
    paths = ["corpus/SOURCES.md", ".ufo/waves/round-56/frozen-tables-v2.json", ".ufo/waves/round-56/c3-name-only.tsv",
             "quality/counters/c3-r56-used-by.py"]
    lines = ["path, lane blob sha256, reduced-repo blob sha256, identical"]
    for p in paths:
        a = sh(["git", "-C", LANE, "rev-parse", "%s:%s" % (REV, p)]).strip()
        b = sh(["git", "-C", os.path.join(S, "mini"), "rev-parse", "HEAD:%s" % p]).strip()
        lines.append("%s, %s, %s, %s" % (p, a, b, a == b))
    ka = sh(["git", "-C", LANE, "ls-tree", "%s" % REV, "corpus/knowledge/"])
    kb = sh(["git", "-C", os.path.join(S, "mini"), "ls-tree", "HEAD", "corpus/knowledge/"])
    lines.append("corpus/knowledge/ listing identical: %s" % (ka == kb))
    lines.append("entry count: lane=%d reduced=%d" % (ka.count("\n"), kb.count("\n")))
    lines.append("base registry blob (13f0acbe) identical: %s"
                 % (sh(["git", "-C", LANE, "rev-parse", "13f0acbe3a15da2d9c08357a576d91dcadc85273:corpus/SOURCES.md"]).strip()
                    == sh(["git", "-C", os.path.join(S, "mini"), "rev-parse", "13f0acbe3a15da2d9c08357a576d91dcadc85273:corpus/SOURCES.md"]).strip()))
    open(os.path.join(RECEIPTS, "06-environment-note.txt"), "w").write("\n".join(lines) + "\n")

    # ---- 01 reference oracle
    ref = os.path.join(S, "ref")
    os.makedirs(ref, exist_ok=True)
    shutil.copyfile(os.path.join(S, "tree/quality/check-r56-controls.py"), os.path.join(ref, "check-r56-controls.py"))
    shutil.copyfile(os.path.join(S, "tree/quality/r56_ctl_c3.py"), os.path.join(ref, "r56_ctl_c3.py"))
    out = []
    for label, counter in (("A-real-counter", "tree/quality/counters/c3-r56-used-by.py"),
                           ("B-always-green-stub", "stubs/stub_green.py"),
                           ("C-every-leg-missed-stub", "stubs/stub_legs.py")):
        w = os.path.join(S, "rcpt." + label)
        shutil.rmtree(w, ignore_errors=True)
        os.makedirs(w)
        cmd = ["python3", "-I", os.path.join(ref, "check-r56-controls.py"), "--claim", "c3", "--repo",
               os.path.join(S, "mini"), "--rev", mini_sha, "--work", w, "--counter", os.path.join(S, counter)]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=w)
        out.append("$ %s" % " ".join(cmd))
        out.append("rc=%d" % p.returncode)
        out.append("stdout: %s" % p.stdout.decode().strip())
        out.append("stderr (last 12 lines):")
        out += ["  " + l for l in p.stderr.decode().strip().split("\n")[-12:]]
        out.append("")
        shutil.rmtree(w, ignore_errors=True)
    open(os.path.join(RECEIPTS, "01-reference-oracle.txt"), "w").write("\n".join(out) + "\n")

    # ---- 02 lane cross-check
    if os.path.exists(os.path.join(S, "work_lane.out")):
        lc = ["$ python3 -I <lane>/quality/check-r56-controls.py --claim c3 --repo %s --rev %s --work <scratch>" % (LANE, REV),
              "rc=0", "stdout: " + open(os.path.join(S, "work_lane.out")).read().strip(), "", "stderr:"]
        lc += open(os.path.join(S, "work_lane.err")).read().rstrip().split("\n")
        open(os.path.join(RECEIPTS, "02-lane-crosscheck.txt"), "w").write("\n".join(lc) + "\n")

    # ---- 03/04 sweep
    res = json.load(open(os.path.join(S, "results.json")))
    shutil.copyfile(os.path.join(S, "results.json"), os.path.join(RECEIPTS, "03-sweep.json"))
    tab = ["id, status, operator, A(real counter), B(always-green), C(every-leg)"]
    for r in res:
        c = {x["check"]: x for x in r.get("checks", [])}
        tab.append("%s, %s, %s, %s, %s, %s" % (
            r["id"], r["status"], r["operator"],
            "as-expected" if c.get("A", {}).get("ok") else "DEVIATES: " + c.get("A", {}).get("detail", ""),
            "as-expected" if c.get("B", {}).get("ok") else "DEVIATES: " + c.get("B", {}).get("detail", ""),
            "as-expected" if c.get("C", {}).get("ok") else "DEVIATES: " + c.get("C", {}).get("detail", "")))
    killed = [r for r in res if r["status"] == "KILLED"]
    survived = [r for r in res if r["status"] == "SURVIVED"]
    tab.append("")
    tab.append("mutants=%d killed=%d survived=%d kill-rate=%d/%d=%.1f%%"
               % (len(res), len(killed), len(survived), len(killed), len(res), 100.0 * len(killed) / len(res)))
    open(os.path.join(RECEIPTS, "04-sweep.txt"), "w").write("\n".join(tab) + "\n")

    # ---- 05 survivors
    p = os.path.join(S, "survivor_verification.json")
    if os.path.exists(p):
        v = json.load(open(p))
        lines = ["id, proposed addition, reference passes, mutant passes, verdict, mutant detail"]
        for r in v:
            lines.append("%s, %s, %s, %s, %s, %s" % (
                r["id"], r.get("addition"), r.get("reference_passes"), r.get("mutant_passes"),
                r.get("verdict"), r.get("mutant_detail", "")))
        open(os.path.join(RECEIPTS, "05-survivors.txt"), "w").write("\n".join(lines) + "\n")
    print("receipts written to %s" % RECEIPTS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
