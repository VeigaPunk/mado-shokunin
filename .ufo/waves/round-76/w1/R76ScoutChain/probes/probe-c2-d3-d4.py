#!/usr/bin/env python3
"""Probe the frozen c2-r76-shapes.py classifier on shapes the 59 controls do not cover.

Extracts the instrument from a read-only `git show`, so an in-flight working-tree edit cannot be
mistaken for the frozen claim's code. Writes only under --scratch.

    python3 probe-c2-d3-d4.py --repo ../.. --rev cb713254... --scratch DIR
"""
import argparse
import hashlib
import os
import runpy
import subprocess
import sys

REL = "quality/counters/c2-r76-shapes.py"


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args(argv)
    scratch = os.path.abspath(a.scratch)
    os.makedirs(scratch, exist_ok=True)
    sha = subprocess.run(["git", "-C", a.repo, "rev-parse", "--verify", a.rev + "^{commit}"],
                         check=True, stdout=subprocess.PIPE).stdout.decode().strip()
    data = subprocess.run(["git", "-C", a.repo, "show", "%s:%s" % (sha, REL)],
                          check=True, stdout=subprocess.PIPE).stdout
    path = os.path.join(scratch, "c2-frozen.py")
    with open(path, "wb") as fh:
        fh.write(data)
    print("REV %s FILE %s SHA256 %s" % (sha, REL, hashlib.sha256(data).hexdigest()))
    m = runpy.run_path(path)

    cases = {
        "d3-nested-same-name": '''def drop(m):
    del m["GIT_NO_REPLACE_OBJECTS"]

def run(repo):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    def helper():
        env = {"PATH": "/usr/bin"}
        drop(env)
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
''',
        "d3-callee-deletes-second-param": '''def drop(env, m):
    del m["GIT_NO_REPLACE_OBJECTS"]

def run(repo):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    drop(env, {"PATH": "/usr/bin"})
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
''',
        "d3-callee-deletes-env-second-arg": '''def drop(m, env):
    del env["GIT_NO_REPLACE_OBJECTS"]

def run(repo):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    drop({"PATH": "/usr/bin"}, env)
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
''',
        "d3-keyword-arg": '''def drop(m):
    del m["GIT_NO_REPLACE_OBJECTS"]

def run(repo):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    drop(m=env)
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
''',
        "d4-module-constant-slice": '''KEYNAME = "GIT_NO_REPLACE_OBJECTS"
def run(repo):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    del env[KEYNAME]
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
''',
        "d4-for-rebind": '''def run(repo):
    k = "GIT_NO_REPLACE_OBJECTS"
    for k in ["PATH"]:
        pass
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    del env[k]
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
''',
        "d4-with-rebind": '''def run(repo):
    k = "GIT_NO_REPLACE_OBJECTS"
    with open("x") as k:
        pass
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    del env[k]
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
''',
    }
    print("# classify -> (reader, guard); semantic reading in comments")
    for name, src in cases.items():
        print("%-34s %s" % (name, m["classify"](src)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
