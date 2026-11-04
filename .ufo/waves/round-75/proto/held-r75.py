#!/usr/bin/env python3
"""Pre-freeze prototype for mado round 75 (NOT a scored counter).

Builds the round-75 candidate case list in memory, scores it with the held round-74 classifier,
and re-derives the guard census at a revision for the held rule and for a successor prototype
(any-name guard constructions + `del env[KEY]` cancellation). Output is the freeze evidence.
"""
import argparse, json, os, re, runpy, subprocess, sys

LANE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
HELD = os.path.join(LANE, "quality", "counters", "c2-r74-shapes.py")
POPULATION_RE = re.compile(r"^quality/check-[^/]+\.py$")

def git(*args):
    return subprocess.check_output(["git", "-C", LANE, *args], text=True)

def held_module():
    return runpy.run_path(HELD)

NEW = [
 ("copy-dict-kw-bound", 'def run(repo):\n    env = os.environ\n    child = dict(env, GIT_NO_REPLACE_OBJECTS="1")\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=child)\n', True, True),
 ("copy-splat-bound", 'def run(repo):\n    env = os.environ\n    child = {**env, "GIT_NO_REPLACE_OBJECTS": "1"}\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=child)\n', True, True),
 ("copy-dict-builtin-bound", 'def run(repo):\n    child = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=child)\n', True, True),
 ("copy-dict-literal-base", 'def run(repo):\n    base = {"PATH": "/usr/bin"}\n    child = dict(base, GIT_NO_REPLACE_OBJECTS="1")\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=child)\n', True, True),
 ("copy-dict-no-key", 'def run(repo):\n    env = os.environ\n    child = dict(env)\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=child)\n', True, False),
 ("copy-dict-value-position", 'def run(repo):\n    child = dict(os.environ, LABEL="GIT_NO_REPLACE_OBJECTS")\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=child)\n', True, False),
 ("copy-rebound", 'def run(repo):\n    env = os.environ\n    child = dict(env, GIT_NO_REPLACE_OBJECTS="1")\n    child = dict(env)\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=child)\n', True, False),
 ("del-env-store-cancel", 'def run(repo):\n    env = {"PATH": "/usr/bin"}\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    del env["GIT_NO_REPLACE_OBJECTS"]\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, False),
 ("del-env-literal-cancel", 'def run(repo):\n    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}\n    del env["GIT_NO_REPLACE_OBJECTS"]\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, False),
 ("del-other-key", 'def run(repo):\n    env = {"PATH": "/usr/bin"}\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    del env["PATH"]\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, True),
 ("del-before-store", 'def run(repo):\n    env = {"PATH": "/usr/bin"}\n    del env["GIT_NO_REPLACE_OBJECTS"]\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, True),
]

def successor(mod):
    ast = mod["ast"]
    base_gcl = mod["guard_construction_lines"]
    base_rebinds = mod["unguarded_rebindings"]
    mapping_has_key = mod["mapping_has_key"]
    env_named = mod["env_named"]
    KEY = mod["KEY"]

    def gcl(nodes, dead_lines, maps=frozenset()):
        out = base_gcl(nodes, dead_lines, maps)
        for node in nodes:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                    and node.lineno not in dead_lines:
                target = node.targets[0]
                if isinstance(target, ast.Name) and mapping_has_key(node.value, maps):
                    out.setdefault(target.id, set()).add(node.lineno)
            elif isinstance(node, ast.AnnAssign) and node.lineno not in dead_lines:
                target = node.target
                if isinstance(target, ast.Name) and node.value is not None \
                        and mapping_has_key(node.value, maps):
                    out.setdefault(target.id, set()).add(node.lineno)
        return out

    def rebinds(nodes, maps=frozenset()):
        out = base_rebinds(nodes, maps)
        for node in nodes:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and not mapping_has_key(node.value, maps):
                        out.setdefault(target.id, set()).add(node.lineno)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) \
                    and node.value is not None and not mapping_has_key(node.value, maps):
                out.setdefault(node.target.id, set()).add(node.lineno)
            elif isinstance(node, ast.Delete):
                for target in node.targets:
                    if isinstance(target, ast.Subscript) and isinstance(target.ctx, ast.Del) \
                            and isinstance(target.value, ast.Name) \
                            and isinstance(target.slice, ast.Constant) \
                            and target.slice.value == KEY:
                        out.setdefault(target.value.id, set()).add(node.lineno)
        return out

    g = mod["has_guard"].__globals__
    g["guard_construction_lines"] = gcl
    g["unguarded_rebindings"] = rebinds
    return mod["classify"]

def population_at(sha):
    return sorted(p for p in git("ls-tree", "-r", "--name-only", sha, "--", "quality").splitlines()
                  if POPULATION_RE.match(p))

def score(fn, cases, tag):
    out = []
    for name, src, er, eg in cases:
        r, g = fn(src)
        out.append((name, r, g, (r == er and g == eg)))
    return out

def census(fn, sha):
    rows = []
    for path in population_at(sha):
        src = git("show", "%s:%s" % (sha, path))
        r, g = fn(src)
        rows.append((path, r, g))
    readers = sum(1 for _p, r, _g in rows if r)
    guarded = sum(1 for _p, r, g in rows if r and g)
    return rows, len(rows), readers, guarded

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default="master")
    ap.add_argument("--cases-out")
    args = ap.parse_args()
    sha = git("rev-parse", args.rev + "^{commit}").strip()
    held = held_module()
    succ_mod = held_module()
    succ = successor(succ_mod)
    print("PY held=%s rev=%s" % (HELD, sha))
    frozen = os.path.join(LANE, ".ufo/waves/round-75/controls/c2-cases-r75.json")
    scored = json.load(open(frozen))["cases"] if os.path.exists(frozen) else \
        [{"name": n, "src": s, "expect_reader": r, "expect_guard": g} for n, s, r, g in NEW]
    held_correct = 0
    for case in scored:
        hr, hg = held["classify"](case["src"])
        sr, sg = succ(case["src"])
        ok = (hr == case["expect_reader"] and hg == case["expect_guard"])
        held_correct += int(ok)
        if not ok or case["name"] in [n for n, *_ in NEW]:
            print("PY case=%-26s expect=(%s,%s) held=(%s,%s) succ=(%s,%s) held_correct=%s"
                  % (case["name"], case["expect_reader"], case["expect_guard"], hr, hg, sr, sg,
                     ok))
    print("PY held_correct=%d/%d (the do-nothing control's score; the target must be %d/%d)"
          % (held_correct, len(scored), len(scored), len(scored)))
    held36 = json.load(open(os.path.join(LANE, ".ufo/waves/round-74/controls/c2-cases-r74.json")))["cases"]
    drift = []
    for case in held36:
        if held["classify"](case["src"]) != succ(case["src"]):
            drift.append((case["name"], held["classify"](case["src"]), succ(case["src"])))
    print("PY held36_drift=%d %s" % (len(drift), drift))
    _, pop_h, reads_h, guard_h = census(held["classify"], sha)
    _, pop_s, reads_s, guard_s = census(succ, sha)
    print("PY population held=%d readers=%d guarded=%d | succ=%d/%d/%d"
          % (pop_h, reads_h, guard_h, pop_s, reads_s, guard_s))
    if args.cases_out:
        doc = {"schema": "mado-r75-new-cases-draft-v1",
               "note": "draft before freeze; ordered for appending after the 36 carried r74 cases",
               "cases": [{"name": n, "src": s, "expect_reader": r, "expect_guard": g}
                         for n, s, r, g in NEW]}
        with open(args.cases_out, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=1)
            fh.write("\n")
        print("PY wrote %s" % args.cases_out)

if __name__ == "__main__":
    main()
