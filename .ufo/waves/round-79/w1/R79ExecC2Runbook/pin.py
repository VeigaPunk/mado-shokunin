#!/usr/bin/env python3
"""R79ExecC2Runbook — clean tree-binding proof on a rev-pinned scratch copy.

Diagnoses the lane drift seen at cp time, pins the copy's counter-bound files to the
measured revision blobs (file writes only, inside the scratch copy), then proves:
clean → rc 0 tree=bound; SKILL.md byte change → rc 2; tool byte change → rc 2;
fixture byte change → rc 2; restore → rc 0.
"""
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SCRATCH = "/fast/scratch/hyaku/mado-r79/R79ExecC2Runbook"
COPY = os.path.join(SCRATCH, "lane-copy")
REV = "5eb8f20fe291603c74973fa94cc55723ac8089a4"
COUNTER = "quality/counters/c2-r79-runbook.py"
CONTROLS = ".ufo/waves/round-79/controls/c2-runbook-cases-r79.json"
CARRIED = ".ufo/waves/round-78/controls/c2-runbook-cases-r78.json"
SCRATCH_ROOT = os.path.join(SCRATCH, "tw")

BOUND = ["SKILL.md", "tools/mado-barfoot.py"] + sorted(
    ".ufo/waves/round-79/fixtures/%s/%s" % (d, f)
    for d in ("refuse-mode", "refuse-scale", "refuse-layer-background", "refuse-output-space")
    for f in ("config.json", "layers.json", "monitors.json"))


def sh(argv, cwd=None):
    return subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                          text=True, errors="replace")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def counter(repo):
    return sh(["python3", "-I", COUNTER, "--repo", ".", "--rev", REV,
               "--controls", CONTROLS, "--carried", CARRIED,
               "--scratch-root", SCRATCH_ROOT, "--no-mutants"], cwd=repo)


def tail(proc):
    lines = proc.stdout.strip().splitlines()
    return lines[-1] if lines else "<no output>"


def main():
    results = {}

    # --- 1. diagnose: what drifted between the audit and the cp?
    diag = {}
    for tag, path in (("lane", os.path.join(LANE, "SKILL.md")),
                      ("copy", os.path.join(COPY, "SKILL.md"))):
        with open(path, "rb") as fh:
            diag[tag + "_skillmd_sha"] = sha(fh.read())
    blob_copy = subprocess.run(["git", "-C", COPY, "show", REV + ":SKILL.md"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    diag["blob_at_rev_sha"] = sha(blob_copy.stdout) if blob_copy.returncode == 0 else "ERR"
    diag["lane_head_now"] = sh(["git", "-C", LANE, "rev-parse", "HEAD"]).stdout.strip()
    diag["lane_log3"] = sh(["git", "-C", LANE, "log", "-3",
                            "--format=%H %s"]).stdout.strip()
    diag["copy_head"] = sh(["git", "-C", COPY, "rev-parse", "HEAD"]).stdout.strip()
    print("DIAG:", json.dumps(diag, indent=1))
    results["diagnosis"] = diag

    # --- 2. pin the copy's bound files to the measured revision blobs
    for path in BOUND:
        blob = subprocess.run(["git", "-C", COPY, "show", REV + ":" + path],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if blob.returncode != 0:
            print("pin failed for", path, blob.stderr.decode())
            return 1
        with open(os.path.join(COPY, path), "wb") as fh:
            fh.write(blob.stdout)
    print("pinned %d bound files to %s" % (len(BOUND), REV[:12]))

    # --- 3. clean baseline must now pass
    proc = counter(COPY)
    print("baseline-pinned rc=%d %s" % (proc.returncode, tail(proc)))
    results["baseline_pinned"] = {"rc": proc.returncode, "tail": tail(proc)}

    # --- 4. tamper each of the three representative bound files
    def tamper(rel, mutate):
        path = os.path.join(COPY, rel)
        with open(path, "rb") as fh:
            original = fh.read()
        with open(path, "wb") as fh:
            fh.write(mutate(original))
        proc = counter(COPY)
        print("tamper:%s rc=%d %s" % (rel, proc.returncode, tail(proc)))
        results["tamper_" + rel.replace("/", "_")] = {"rc": proc.returncode,
                                                      "tail": tail(proc)}
        with open(path, "wb") as fh:
            fh.write(original)

    tamper("SKILL.md",
           lambda b: b.replace(b"### Advertised Wayland globals",
                               b"### Advertised Wayland globalZ", 1))
    tamper("tools/mado-barfoot.py",
           lambda b: b.replace(b"MADO_BARFOOT", b"MADO_BARFOOTX", 1))
    tamper(".ufo/waves/round-79/fixtures/refuse-mode/config.json",
           lambda b: b + b"\n")

    # --- 5. restore to rev bytes: the copy must bind again
    for path in ("SKILL.md", "tools/mado-barfoot.py",
                 ".ufo/waves/round-79/fixtures/refuse-mode/config.json"):
        blob = subprocess.run(["git", "-C", COPY, "show", REV + ":" + path],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with open(os.path.join(COPY, path), "wb") as fh:
            fh.write(blob.stdout)
    proc = counter(COPY)
    print("restored rc=%d %s" % (proc.returncode, tail(proc)))
    results["restored"] = {"rc": proc.returncode, "tail": tail(proc)}

    with open(os.path.join(SCRATCH, "pin-results.json"), "w") as fh:
        json.dump(results, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
