#!/usr/bin/env python3
"""Pre-freeze prototype: run the HELD round-70 classifier over the six new r71 C2
control cases and record (expect_reader, expect_guard) vs held (reader, guard)."""
import importlib.util
import json
import sys

REPO = "/home/vgpnk/Projects/shokunin/mado-shokunin"
spec = importlib.util.spec_from_file_location(
    "c2r70", REPO + "/quality/counters/c2-r70-carriers.py")
mod = importlib.util.module_from_spec(spec)
sys.modules["c2r70"] = mod
spec.loader.exec_module(mod)

CASES = [
    ("dict-call-splat", True, True, '''GUARD = {"GIT_NO_REPLACE_OBJECTS": "1"}

def run(repo):
    env = dict(os.environ, **GUARD)
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
'''),
    ("dict-call-splat-object-alias", True, True, '''GUARD = {"GIT_NO_REPLACE_OBJECTS": "1"}

def run(repo):
    m = GUARD
    env = {**os.environ, **m}
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
'''),
    ("store-through-alias-two-hop", True, True, '''def run(repo):
    e = {"PATH": "/usr/bin"}
    staging = e
    staging["GIT_NO_REPLACE_OBJECTS"] = "1"
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=e)
'''),
    ("attribute-second-object", True, True, '''def run(repo):
    runner.env = {}
    runner.env["GIT_NO_REPLACE_OBJECTS"] = "1"
    cfg.runner = runner
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=cfg.runner.env)
'''),
    ("unguarded-dict-splat-negative", True, False, '''OTHER = {"LABEL": "x"}

def run(repo):
    env = dict(os.environ, **OTHER)
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
'''),
    ("env-call-no-key-negative", True, False, '''def run(repo):
    env = dict(os.environ)
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
'''),
]

for name, er, eg, src in CASES:
    reader, guard = mod.classify(src)
    held_ok = (reader == er and guard == eg)
    print("PROTO_R71_C2 case=%s expect=(%s,%s) held=(%s,%s) held_correct=%s"
          % (name, er, eg, reader, guard, "yes" if held_ok else "NO"))
