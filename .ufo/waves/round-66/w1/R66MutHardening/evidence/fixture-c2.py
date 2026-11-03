#!/usr/bin/env python3
"""fixture-c2.py — r66 C2 control matrix for a landing instrument (mutation seat).

Builds a green nav fixture repo, a lab tree whose three sibling instruments are
marker-faithful stubs, and runs the instrument under test across the frozen
conditions (a)-(d), plus green / citecheck-red / round-binding probes.

    python3 fixture-c2.py --instrument PATH --work DIR [--label NAME] [--round-n 65]

Expected (PRED-C2-r66):
  green      -> GREEN, exit 0
  a red      -> RED,   exit 1  (child rc=1, contract marker present)
  b crash    -> ERROR, exit 2  (child rc=2)
  c no-marker-> ERROR, exit 2  (child rc=0, no marker)
  d missing  -> ERROR, exit 2  (used-by sibling absent)
  e cite-red -> RED,   exit 1  (only citecheck red)
  f round    -> default receipts tree follows --round (path log)
Writes only under --work; fixture git toplevel asserted before the first commit.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

ROUNDS = (65, 64)
STUB_USEDBY = r'''#!/usr/bin/env python3
import os, sys
leg = "usedby"
behavior = os.environ.get("R66_STUB_%s" % leg.upper(), "green")
log = os.environ.get("R66_PATH_LOG")
if log:
    with open(log, "a", encoding="utf-8") as fh:
        fh.write("%s\t%s\n" % (leg, "\t".join(sys.argv[1:])))
rev = os.environ.get("R66_STUB_REV", "unknown")
if behavior == "green":
    print("MADO_USED_BY: rev=%s entries=1 rows=1 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=0 verdict=TARGET_MET missed=none" % rev)
    sys.exit(0)
if behavior == "red":
    print("MADO_USED_BY: rev=%s entries=1 rows=1 missing=1 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=0 verdict=TARGET_MISSED missed=missing" % rev)
    sys.exit(1)
if behavior == "crash":
    sys.stderr.write("stub usedby: simulated crash\n")
    sys.exit(2)
if behavior == "dupmarker":
    line = "MADO_USED_BY: rev=%s entries=1 rows=1 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=0 verdict=TARGET_MET missed=none" % rev
    print(line)
    print(line)
    sys.exit(0)
print("stub usedby: no contract marker")
sys.exit(0)
'''
STUB_LEDGER = r'''#!/usr/bin/env python3
import os, sys
leg = "ledger"
behavior = os.environ.get("R66_STUB_%s" % leg.upper(), "green")
log = os.environ.get("R66_PATH_LOG")
if log:
    with open(log, "a", encoding="utf-8") as fh:
        fh.write("%s\t%s\n" % (leg, "\t".join(sys.argv[1:])))
rev = os.environ.get("R66_STUB_REV", "unknown")
if behavior == "green":
    print("LEDGER: population=1 ledger_rows=1 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET rev=%s" % rev)
    sys.exit(0)
if behavior == "red":
    print("LEDGER: population=1 ledger_rows=0 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED rev=%s" % rev)
    sys.exit(1)
if behavior == "crash":
    sys.stderr.write("stub ledger: simulated crash\n")
    sys.exit(2)
print("stub ledger: no contract marker")
sys.exit(0)
'''
STUB_CITECHECK = r'''#!/usr/bin/env python3
import os, sys
leg = "citecheck"
behavior = os.environ.get("R66_STUB_%s" % leg.upper(), "green")
log = os.environ.get("R66_PATH_LOG")
if log:
    with open(log, "a", encoding="utf-8") as fh:
        fh.write("%s\t%s\n" % (leg, "\t".join(sys.argv[1:])))
rev = os.environ.get("R66_STUB_REV", "unknown")
if behavior == "green":
    print("MADO_CITECHECK: rev=%s files=1 citations=1 resolved=1 missing=0 skipped_large=0 verdict=TARGET_MET (VERSION fixture)" % rev)
    sys.exit(0)
if behavior == "red":
    print("MADO_CITECHECK: rev=%s files=1 citations=1 resolved=0 missing=1 skipped_large=0 verdict=TARGET_MISSED (VERSION fixture)" % rev)
    sys.exit(1)
if behavior == "crash":
    sys.stderr.write("stub citecheck: simulated crash\n")
    sys.exit(2)
print("stub citecheck: no contract marker")
sys.exit(0)
'''
STUBS = {
    "quality/counters/c3-r56-used-by.py": STUB_USEDBY,
    "quality/check-tool-ledger.py": STUB_LEDGER,
    "tools/mado-receipt-citecheck.py": STUB_CITECHECK,
}


def run(argv, cwd=None, env=None, timeout=120):
    return subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=env, text=True, timeout=timeout)


def git(repo, *args):
    return run(["git", "-C", repo, *args])


def build_repo(repo, cites):
    if os.path.exists(repo):
        shutil.rmtree(repo)
    os.makedirs(repo)
    g = git(repo, "init", "-q")
    assert g.returncode == 0, g.stderr
    top = git(repo, "rev-parse", "--show-toplevel").stdout.strip()
    assert top == os.path.realpath(repo), (top, repo)
    files = {
        "corpus/knowledge/a.md": "# a\n",
        "corpus/knowledge/b.md": "# b\n",
        "corpus/README.md": "# corpus\n\n| note |\n| --- |\n| `knowledge/a.md` |\n| `knowledge/b.md` |\n",
        "corpus/SOURCES.md": "# SOURCES\n| id | url |\n| --- | --- |\n",
    }
    for rnd in ROUNDS:
        files[".ufo/waves/round-%d/receipts/receipt.txt" % rnd] = "MADO_FIXTURE: cite corpus/README.md\n"
    for rel, text in files.items():
        path = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    git(repo, "add", "-A")
    c = git(repo, "-c", "user.name=mado-r66-mut", "-c",
            "user.email=mut@example.invalid", "-c", "commit.gpgsign=false",
            "commit", "-q", "-m", "green nav fixture")
    assert c.returncode == 0, c.stderr
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def build_lab(base, instrument, drop_usedby=False):
    if os.path.exists(base):
        shutil.rmtree(base)
    os.makedirs(os.path.join(base, "quality", "counters"))
    os.makedirs(os.path.join(base, "tools"))
    dst = os.path.join(base, "quality", "landing-counters.sh")
    shutil.copyfile(instrument, dst)
    os.chmod(dst, 0o755)
    for rel, text in STUBS.items():
        if drop_usedby and rel.endswith("c3-r56-used-by.py"):
            continue
        path = os.path.join(base, rel)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.chmod(path, 0o755)
    return dst


def parse_verdict(out):
    for line in out.splitlines():
        if line.startswith("MADO_LANDING_COUNTERS:"):
            return line
    return ""


def classify(out, rc):
    line = parse_verdict(out)
    verdict = ""
    if "GREEN" in line:
        verdict = "GREEN"
    elif "RED" in line:
        verdict = "RED"
    elif "ERROR" in line:
        verdict = "ERROR"
    elif rc == 2:
        verdict = "ERROR(no-summary)"
    return verdict, rc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instrument", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--label", default="instrument")
    ap.add_argument("--round-n", type=int, default=65)
    ap.add_argument("--no-round", action="store_true")
    args = ap.parse_args()
    work = os.path.realpath(args.work)
    os.makedirs(work, exist_ok=True)
    instrument = os.path.realpath(args.instrument)
    repo = os.path.join(work, "repo")
    rev = build_repo(repo, instrument)
    scenarios = [
        ("green", {"USEDBY": "green", "LEDGER": "green", "CITECHECK": "green"}, "GREEN", 0, False),
        ("a-red", {"USEDBY": "red", "LEDGER": "green", "CITECHECK": "green"}, "RED", 1, False),
        ("b-crash", {"USEDBY": "crash", "LEDGER": "green", "CITECHECK": "green"}, "ERROR", 2, False),
        ("c-nomarker", {"USEDBY": "nomarker", "LEDGER": "green", "CITECHECK": "green"}, "ERROR", 2, False),
        ("h-dup-marker", {"USEDBY": "dupmarker", "LEDGER": "green", "CITECHECK": "green"}, "ERROR", 2, False),
        ("d-missing", {"USEDBY": "green", "LEDGER": "green", "CITECHECK": "green"}, "ERROR", 2, True),
        ("e-cite-red", {"USEDBY": "green", "LEDGER": "green", "CITECHECK": "red"}, "RED", 1, False),
    ]
    results = {}
    correct = 0
    for name, behavior, want_verdict, want_rc, drop in scenarios:
        lab = os.path.join(work, "lab-" + name)
        script = build_lab(lab, instrument, drop_usedby=drop)
        runroot = os.path.join(work, "run-" + name)
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        for leg, behavior_value in behavior.items():
            env["R66_STUB_" + leg] = behavior_value
        env["R66_STUB_REV"] = rev
        round_args = [] if args.no_round else ["--round", str(args.round_n)]
        proc = run(["bash", script, "--repo", repo, "--rev", rev,
                    *round_args, "--scratch-root", runroot], cwd=work, env=env)
        verdict, rc = classify(proc.stdout, proc.returncode)
        ok = ((verdict == want_verdict or (want_verdict == "ERROR" and verdict == "ERROR(no-summary)"))
              and rc == want_rc)
        if name == "green" and proc.returncode == 2 and not proc.stdout:
            ok = False
        correct += int(ok)
        results[name] = {
            "want_verdict": want_verdict, "want_rc": want_rc,
            "verdict": verdict, "rc": proc.returncode, "correct": ok,
            "stdout": proc.stdout, "stderr": proc.stderr,
        }
        print("%s\t%s\twant=%s/%d\tgot=%s/%d\t%s"
              % (args.label, name, want_verdict, want_rc, verdict or "-",
                 proc.returncode, "CORRECT" if ok else "WRONG"))
        if not ok:
            tail = [ln for ln in proc.stderr.splitlines() if ln.strip()][-2:]
            for line in tail:
                print("    stderr: %s" % line)

    # f: --round binding through the citecheck leg's received --paths argument.
    binding = {}
    for rnd in ROUNDS:
        lab = os.path.join(work, "lab-round-%d" % rnd)
        script = build_lab(lab, instrument)
        runroot = os.path.join(work, "run-round-%d" % rnd)
        log = os.path.join(work, "paths-round-%d.log" % rnd)
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update({"R66_STUB_USEDBY": "green", "R66_STUB_LEDGER": "green",
                    "R66_STUB_CITECHECK": "green", "R66_STUB_REV": rev,
                    "R66_PATH_LOG": log})
        round_args = [] if args.no_round else ["--round", str(rnd)]
        proc = run(["bash", script, "--repo", repo, "--rev", rev,
                    *round_args, "--scratch-root", runroot], cwd=work, env=env)
        seen = ""
        if os.path.isfile(log):
            with open(log, encoding="utf-8") as fh:
                for line in fh:
                    if line.startswith("citecheck\t"):
                        seen = line.rstrip("\n")
        want = "/round-%d/receipts" % rnd
        ok = want in seen
        binding[rnd] = {"want": want, "seen": seen, "correct": ok,
                        "rc": proc.returncode, "stdout": proc.stdout.strip(),
                        "stderr": proc.stderr.strip()}
        print("%s\tround-%d\twant_path=%s\t%s\t%s"
              % (args.label, rnd, want, "CORRECT" if ok else "WRONG", seen or "(no log)"))
    correct += sum(1 for v in binding.values() if v["correct"])

    aux = {}

    # Inherited GIT_* steering must not redirect the legs (green stubs, poisoned env).
    lab = os.path.join(work, "lab-gitsteering")
    script = build_lab(lab, instrument)
    env = dict(os.environ)
    env.update({"R66_STUB_USEDBY": "green", "R66_STUB_LEDGER": "green",
                "R66_STUB_CITECHECK": "green", "R66_STUB_REV": rev,
                "GIT_DIR": "/nonexistent/r66-gitdir", "GIT_WORK_TREE": "/nonexistent/r66-wt",
                "GIT_INDEX_FILE": "/nonexistent/r66-index", "GIT_CONFIG_COUNT": "1"})
    proc = run(["bash", script, "--repo", repo, "--rev", rev,
                "--round", str(args.round_n),
                "--scratch-root", os.path.join(work, "run-gitsteering")], cwd=work, env=env)
    verdict, rc = classify(proc.stdout, proc.returncode)
    gs_ok = verdict == "GREEN" and rc == 0
    aux["gitsteering"] = {"want_verdict": "GREEN", "want_rc": 0,
                          "verdict": verdict, "rc": proc.returncode, "correct": gs_ok,
                          "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()}
    correct += int(gs_ok)
    print("%s\tgitsteering\twant=GREEN/0\tgot=%s/%d\t%s"
          % (args.label, verdict or "-", proc.returncode, "CORRECT" if gs_ok else "WRONG"))

    # Auxiliary probe: --round has no hardcoded default.
    lab = os.path.join(work, "lab-no-round")
    script = build_lab(lab, instrument)
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"R66_STUB_USEDBY": "green", "R66_STUB_LEDGER": "green",
                "R66_STUB_CITECHECK": "green", "R66_STUB_REV": rev})
    proc = run(["bash", script, "--repo", repo, "--rev", rev,
                "--scratch-root", os.path.join(work, "run-no-round")], cwd=work, env=env)
    aux["no-round"] = {"want_rc": 2, "rc": proc.returncode,
                       "correct": proc.returncode == 2,
                       "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()}
    print("%s\taux-no-round\twant_rc=2\tgot_rc=%d\t%s"
          % (args.label, proc.returncode, "CORRECT" if proc.returncode == 2 else "WRONG"))

    total = len(scenarios) + len(binding) + 1
    summary = {"label": args.label, "instrument": instrument, "repo": repo, "rev": rev,
               "correct": correct, "total": total, "scenarios": results,
               "round_binding": binding, "aux": aux}
    out = os.path.join(work, "c2-matrix-%s.json" % args.label)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    print("%s\tTOTAL\t%d/%d\t%s" % (args.label, correct, total, out))
    return 0 if correct == total else 1


if __name__ == "__main__":
    sys.exit(main())
