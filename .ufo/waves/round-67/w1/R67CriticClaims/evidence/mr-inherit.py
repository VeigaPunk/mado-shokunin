#!/usr/bin/env python3
"""Falsification: docs the base citecheck child read real objects when invoked
with the instrument's inherited env (parent exports GIT_NO_REPLACE_OBJECTS=1),
and forged only when that inherited key is scrubbed?  All writes under $S."""
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/mado-r67/R67CriticClaims/mr-inherit"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "0b28ffb4baac9586566d246c3f0986b2bb650a33"
CHILD_REL = "tools/mado-receipt-citecheck.py"


def run(argv, env=None, cwd=None):
    return subprocess.run(argv, capture_output=True, text=True, env=env, cwd=cwd)


def main():
    shutil.rmtree(S, ignore_errors=True)
    os.makedirs(S)
    child = os.path.join(S, "citecheck.py")
    src = subprocess.run(["git", "-C", LANE, "show", BASE + ":" + CHILD_REL],
                         capture_output=True, check=True).stdout
    open(child, "wb").write(src)
    D = os.path.join(S, "fx")
    os.makedirs(os.path.join(D, ".ufo/waves/round-66/receipts"))
    os.makedirs(os.path.join(D, "corpus"))
    open(os.path.join(D, "corpus/README.md"), "w").write("# corpus\n")
    receipt = os.path.join(D, ".ufo/waves/round-66/receipts/a.txt")
    open(receipt, "w").write("cited file corpus/cited.md\n")
    for args in (["init", "-q"], ["add", "-A"],
                 ["-c", "user.name=p", "-c", "user.email=p@example.invalid",
                  "-c", "commit.gpgsign=false", "commit", "-qm", "base"]):
        subprocess.run(["git", "-C", D, *args], check=True, capture_output=True)
    top = subprocess.run(["git", "-C", D, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    assert top == D, top
    rev = subprocess.run(["git", "-C", D, "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    real_tree = subprocess.run(["git", "-C", D, "rev-parse", rev + "^{tree}"],
                               capture_output=True, text=True).stdout.strip()
    blob = subprocess.run(["git", "-C", D, "hash-object", "-w", "--stdin"],
                          input="cited file\n", capture_output=True, text=True).stdout.strip()
    subprocess.run(["git", "-C", D, "update-index", "--add", "--cacheinfo",
                    "100644,%s,corpus/cited.md" % blob], check=True, capture_output=True)
    forged_tree = subprocess.run(["git", "-C", D, "write-tree"],
                                 capture_output=True, text=True).stdout.strip()
    subprocess.run(["git", "-C", D, "read-tree", rev], check=True, capture_output=True)
    subprocess.run(["git", "-C", D, "replace", real_tree, forged_tree], check=True,
                   capture_output=True)
    base_env = {"PATH": "/usr/bin:/bin", "HOME": S, "LC_ALL": "C",
                "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
                "GIT_OPTIONAL_LOCKS": "0"}
    for label, extra in (("instrument-inherited GIT_NO_REPLACE_OBJECTS=1",
                          {"GIT_NO_REPLACE_OBJECTS": "1"}),
                         ("harness child_env (GIT_* scrubbed, key absent)", {})):
        env = dict(base_env, **extra)
        r = run([sys.executable, child, "--repo", D, "--rev", rev, "--paths", receipt],
                env=env, cwd=S)
        marker = [ln for ln in (r.stdout + r.stderr).splitlines()
                  if ln.startswith("MADO_CITECHECK:")]
        print(f"CASE {label}\n  rc={r.returncode} marker={marker[-1] if marker else 'none'}")
    shutil.rmtree(S, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
