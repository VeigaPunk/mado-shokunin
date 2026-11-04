#!/usr/bin/env python3
"""Discrimination matrix against the COMMITTED r69 C2 counter at 5fc29ae."""
import importlib.util, json, os, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
S = os.path.dirname(os.path.abspath(__file__))
REV = "296ed0d75e361387908cf2dd418d3677f49f94c8"
PATH = "quality/counters/c2-r69-guard-dominance.py"


def load_src():
    src = subprocess.check_output(["git", "-C", LANE, "cat-file", "-p", "%s:%s" % (REV, PATH)]).decode()
    return src


def load(src, tag):
    p = os.path.join(S, "tip_mut_%s.py" % tag)
    open(p, "w").write(src)
    spec = importlib.util.spec_from_file_location("tip_mut_" + tag, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def score(mod, cases):
    bad = []
    for c in cases:
        r, g = mod.classify(c["src"])
        if not ((r == c["expect_reader"]) and (g == c["expect_guard"])):
            bad.append(c["name"])
    return len(cases) - len(bad), bad


def main():
    src = load_src()
    m0 = load(src, "orig")
    cases = json.load(open(os.path.join(LANE, ".ufo/waves/round-69/controls/c2-controls-r69.json")))["cases"]
    ok, bad = score(m0, cases)
    print("COMMITTED counter %d/%d bad=%s" % (ok, len(cases), bad))
    shapes = {
        "nested-dict-value-key":
            ('def run(repo):\n    env = {"PATH": "/usr/bin", "NESTED": '
             '{"GIT_NO_REPLACE_OBJECTS": "1"}}\n'
             '    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n'),
        "non-dict-call-keyword":
            ('def make_env(**kw):\n    return {"PATH": "/usr/bin"}\n\n\n'
             'def run(repo):\n    env = make_env(GIT_NO_REPLACE_OBJECTS="1")\n'
             '    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n'),
        "guard-but-git-called-without-env":
            ('def run(repo):\n    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}\n'
             '    subprocess.run(["git", "-C", repo, "show", "HEAD:a"])\n'),
    }
    for k, v in shapes.items():
        print("SHAPE %-30s classify=%s" % (k, m0.classify(v)))

    MUTANTS = {
        "no-git-launch-requirement":
            ("        if call_is_git(node):\n            lines.add(node.lineno)\n            continue",
             "        if True:\n            lines.add(node.lineno)\n            continue"),
        "no-git-requirement-inline":
            ("            if kw.arg != \"env\" or not call_is_git(node):\n                continue",
             "            if kw.arg != \"env\":\n                continue"),
        "reader-always-true":
            ("def is_reader(src):\n    return bool(GIT_TOKEN_RE.search(src)) and bool(VERB_RE.search(src))",
             "def is_reader(src):\n    return True"),
        "no-dead-branch-subscript":
            ("                    if (isinstance(base, ast.Name) and env_named(base.id)\n"
             "                            and isinstance(key, ast.Constant) and key.value == KEY\n"
             "                            and node.lineno not in dead_lines):",
             "                    if (isinstance(base, ast.Name) and env_named(base.id)\n"
             "                            and isinstance(key, ast.Constant) and key.value == KEY):"),
    }
    for tag, (old, new) in MUTANTS.items():
        c = src.count(old)
        if c != 1:
            print("MUTANT %-30s occurrences=%d SKIP" % (tag, c))
            continue
        mm = load(src.replace(old, new), tag)
        ok, bad = score(mm, cases)
        print("MUTANT %-30s %2d/%d caught_by=%s" % (tag, ok, len(cases), bad))


if __name__ == "__main__":
    main()
