#!/usr/bin/env python3
"""R79ExecC2Runbook — prove the C2 counter refuses a tree whose bytes differ.

Operates ONLY on a scratch copy of the lane (cp -a, .git included). Every git call
names -C the copy. The real lane is never written.
"""
import os
import shutil
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


def sh(argv, cwd=None):
    return subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                          text=True, errors="replace")


def counter(repo):
    return sh(["python3", "-I", COUNTER, "--repo", ".", "--rev", REV,
               "--controls", CONTROLS, "--carried", CARRIED,
               "--scratch-root", SCRATCH_ROOT, "--no-mutants"], cwd=repo)


def label(tag, proc):
    line = proc.stdout.strip().splitlines()
    print("%s rc=%d %s" % (tag, proc.returncode,
                           line[-1] if line else "<no output>"))
    return proc.returncode, proc.stdout


def main():
    if os.path.exists(COPY):
        shutil.rmtree(COPY)
    print("copying lane → scratch copy (cp -a)…")
    proc = sh(["cp", "-a", LANE, COPY])
    if proc.returncode != 0:
        print("cp failed:", proc.stdout)
        return 1

    top = sh(["git", "-C", COPY, "rev-parse", "--show-toplevel"]).stdout.strip()
    print("toplevel:", top)
    if top != COPY:
        print("GUARD: toplevel is not the scratch copy — aborting")
        return 1
    head = sh(["git", "-C", COPY, "rev-parse", "HEAD"]).stdout.strip()
    print("copy HEAD:", head)

    results = {}
    rc, out = label("baseline-clean", counter(COPY))
    results["baseline_clean"] = {"rc": rc, "tail": out.strip().splitlines()[-1]}

    def tamper(rel, mutate):
        path = os.path.join(COPY, rel)
        with open(path, "rb") as fh:
            original = fh.read()
        with open(path, "wb") as fh:
            fh.write(mutate(original))
        rc, out = label("tamper:" + rel, counter(COPY))
        results["tamper_" + rel] = {"rc": rc,
                                    "line": out.strip().splitlines()[-1]}
        with open(path, "wb") as fh:  # restore exact bytes
            fh.write(original)
        return rc

    tamper("SKILL.md", lambda b: b.replace(b"### Advertised Wayland globals",
                                           b"### Advertised Wayland globalZ", 1))
    tamper("tools/mado-barfoot.py", lambda b: b.replace(b"MADO_BARFOOT",
                                                        b"MADO_BARFOOTX", 1))
    tamper(".ufo/waves/round-79/fixtures/refuse-mode/config.json",
           lambda b: b + b"\n")

    rc, out = label("restored-clean", counter(COPY))
    results["restored_clean"] = {"rc": rc, "tail": out.strip().splitlines()[-1]}

    import json
    with open(os.path.join(SCRATCH, "tamper-results.json"), "w") as fh:
        json.dump(results, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
