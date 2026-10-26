#!/usr/bin/env python3
"""mutrun44.py - re-run the round-43 MutCheckLocators mutant set against a base file.

The 37 (name, category, pattern, replacement) mutants are imported verbatim from
the round-43 seat harness (read-only) so this run cannot drift from the frozen set.

Two detectors per mutant, both compared against the SAME base's own output:
  D1 selftest: python3 -I <mutant> --selftest
  D2 control:  python3 -I <mutant> --fetch <round-42 fetch> LOG-r42.md
A mutant is killed when either (rc, output) pair differs from the base's pair.

Usage: mutrun44.py <tag> <base.py> [<out-dir>]
Writes <out-dir>/BASE-<tag>.{selftest,control}.txt, <out-dir>/<tag>-<mutant>.* and
<out-dir>/matrix-<tag>.tsv; prints one row per mutant plus the survivor list.
"""

import hashlib
import importlib.util
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MUT43 = (
    "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w2/MutCheckLocators/mutrun.py"
)
FETCH42 = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-42/fetch"
LOG42 = os.path.join(HERE, "LOG-r42.md")
SCRATCH = "/fast/scratch/hyaku/mado-r44/ExecLocatorTeeth"

spec = importlib.util.spec_from_file_location("mut43", MUT43)
_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_mod)
MUTANTS = _mod.MUTANTS


def apply_once(base_text, name, pattern, repl):
    new, n = re.subn(pattern, lambda _m: repl, base_text, count=1)
    if n != 1:
        return None, "pattern applied %d times (want 1)" % n
    if new == base_text:
        return None, "replacement produced identical bytes"
    return new, None


def run(cmd):
    env = dict(os.environ)
    env["TMPDIR"] = SCRATCH
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=180, cwd=HERE, env=env)
    return p.returncode, p.stdout + p.stderr


def main():
    tag, base_path = sys.argv[1], sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    os.makedirs(SCRATCH, exist_ok=True)
    with open(base_path, "r", encoding="utf-8") as fh:
        base_text = fh.read()

    base_self = run([sys.executable, "-I", base_path, "--selftest"])
    base_ctl = run([sys.executable, "-I", base_path, "--fetch", FETCH42, LOG42])
    with open(os.path.join(out, "BASE-%s.selftest.txt" % tag), "w") as fh:
        fh.write("rc=%d\n%s" % base_self)
    with open(os.path.join(out, "BASE-%s.control.txt" % tag), "w") as fh:
        fh.write("rc=%d\n%s" % base_ctl)
    print(
        "BASE %s sha256=%s selftest rc=%d control rc=%d"
        % (tag, hashlib.sha256(base_text.encode()).hexdigest(), base_self[0], base_ctl[0])
    )

    rows = []
    for name, cat, pattern, repl in MUTANTS:
        src, err = apply_once(base_text, name, pattern, repl)
        if src is None:
            rows.append((name, cat, "-", "-", "NOT-APPLICABLE (%s)" % err, "-"))
            print("%-28s %-20s NOT-APPLICABLE %s" % (name, cat, err))
            continue
        mpath = os.path.join(SCRATCH, "m_%s_%s.py" % (tag, name))
        with open(mpath, "w", encoding="utf-8") as fh:
            fh.write(src)
        try:
            s = run([sys.executable, "-I", mpath, "--selftest"])
            c = run([sys.executable, "-I", mpath, "--fetch", FETCH42, LOG42])
        finally:
            os.remove(mpath)
        killed_by = None
        if s != base_self:
            killed_by = "selftest"
        if c != base_ctl:
            killed_by = (killed_by + "+control") if killed_by else "control"
        verdict = killed_by or "SURVIVED"
        with open(os.path.join(out, "%s-%s.selftest.txt" % (tag, name)), "w") as fh:
            fh.write("rc=%d\n%s" % s)
        with open(os.path.join(out, "%s-%s.control.txt" % (tag, name)), "w") as fh:
            fh.write("rc=%d\n%s" % c)
        rows.append((name, cat, s[0], c[0], verdict, hashlib.sha256(src.encode()).hexdigest()[:12]))
        print("%-28s %-20s selftest=%3d control=%3d %s" % (name, cat, s[0], c[0], verdict))

    with open(os.path.join(out, "matrix-%s.tsv" % tag), "w") as fh:
        fh.write("mutant\tcategory\tselftest_rc\tcontrol_rc\tverdict\tmutant_sha12\n")
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")
    surv = [r[0] for r in rows if r[4] == "SURVIVED"]
    print("\n%s: %d mutants, %d killed, %d survived: %s"
          % (tag, len(rows), len(rows) - len(surv), len(surv), ", ".join(surv) or "none"))


if __name__ == "__main__":
    main()
