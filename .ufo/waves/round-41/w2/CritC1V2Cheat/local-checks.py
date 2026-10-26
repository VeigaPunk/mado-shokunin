#!/usr/bin/env python3
"""Local (unsandboxed) simulation of the counter's b2/b3 clauses for the w2
cheats, so the expensive scored runs are not spent on avoidable surprises.

Runs the counter's own mutate_source/function_sites and its b3 transforms; the
selftest is executed with HOME=/nonexistent and PATH=/usr/bin, as the sandbox
sets them.  Not a substitute for the scored run: the sandbox, RLIMIT_NPROC and
the fixtures are only exercised by the counter itself.
"""
import ast
import importlib.util
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r41-globals-v2.py")
spec = importlib.util.spec_from_file_location("c1v2", COUNTER)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

ENV = {"HOME": "/nonexistent", "PATH": "/usr/bin", "LC_ALL": "C"}


def run_selftest(text, tag):
    d = tempfile.mkdtemp(prefix="local-" + tag + "-")
    path = os.path.join(d, "mado-globals.py")
    with open(path, "w") as fh:
        fh.write(text)
    try:
        p = subprocess.run([sys.executable, "-I", path, "--selftest"],
                           capture_output=True, text=True, env=ENV, cwd=d,
                           timeout=300)
    except subprocess.TimeoutExpired:
        return None, 0, 0, False
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)
    m = M.re.search(r"MADO_GLOBALS_SELFTEST: (\d+)/(\d+) passed", p.stdout)
    k, n = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    return p.returncode, k, n, bool(m)


def main(names):
    for name in names:
        path = os.path.join(HERE, name)
        src = open(path).read()
        sites = M.function_sites(src)
        summ = [s for s, f in sites if f]
        rc, k, n, has = run_selftest(src, "base")
        print("%s b rc=%s %d/%d" % (name, rc, k, n))
        for tag, text in {
            "comment": src + "\n# b3-neutral c0ffee00deadbeef\n",
            "unparse": ast.unparse(ast.parse(src)) + "\nB3_NEUTRAL_c0ffee00 = 1\n",
        }.items():
            rc2, k2, n2, has2 = run_selftest(text, "b3-" + tag)
            print("%s b3=%s rc=%s %d/%d ok=%d" % (
                name, tag, rc2, k2, n2,
                int(rc2 == 0 and has2 and k2 == n2 and n2 >= 50)))
        dead = 0
        for site, _flag in sites:
            mut = M.mutate_source(src, site)
            if mut is None:
                print("%s site=%s:%d mutate=None" % (name, site[0], site[1]))
                continue
            rc3, k3, n3, has3 = run_selftest(mut, "mut")
            is_dead = rc3 != 0 or not has3 or k3 != n3
            dead += is_dead
            print("%s b2 site=%s:%d dead=%d%s" % (
                name, site[0], site[1], is_dead,
                " FORCED-CANDIDATE" if site in summ else ""))
        print("%s b2 all-sites killed=%d/%d summ_sites=%d" % (
            name, dead, len(sites), len(summ)))


if __name__ == "__main__":
    main(sys.argv[1:])
