#!/usr/bin/env python3
"""R68RevC1 adversarial probe for claim C1 (mado round 68).

Sections:
  1. hand-apply the three frozen recipes S1/S2/S3 to a copy of the candidate harness,
     run each mutant's --selftest, report rc + failing assertion lines;
  2. try to BREAK the selftest with mutations the three frozen recipes do NOT cover
     (credit forgeries, decision forgeries, expectation edits, guard removal);
  3. dump the evidence lines the scripted measure() run prints, proving the scripted
     cases exercise extraction, both mutant copies, the R fixture and run_r_child;
  4. confirm the counter's CONTRACT_RE fullmatches the final line it printed at the tip.
Everything writes under /fast/scratch/hyaku/mado-r68/R68RevC1 only.
"""
import argparse
import contextlib
import hashlib
import importlib.util
import io
import os
import shutil
import subprocess
import sys

HARNESS = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r68-landing-controls.py"
COUNTER = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r68-selfmutants.py"
S = "/fast/scratch/hyaku/mado-r68/R68RevC1"
MUTDIR = os.path.join(S, "mut")

src = open(HARNESS, "rb").read().decode("utf-8")

# --- build the exact find text for the forged_credit-term drop from live bytes ---------------
a = src.index("mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker)")
TERM = "forged_credit(mr_rc, mr_marker))"
b = src.index(TERM, a) + len(TERM)
G_FIND = src[a:b]
G_REPL = "mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker))"

MUTANTS = [
    ("S1-frozen-mr_killed_True", [("mr_killed = bool(", "mr_killed = True or bool(")]),
    ("S2-frozen-mz_killed_True", [("mz_killed = mz_rc != 0", "mz_killed = True")]),
    ("S3-frozen-killed_2", [("killed = int(mz_killed) + int(mr_killed)", "killed = 2")]),
    ("A-forged_credit-always-True",
     [('return rc == 0 and marker == ("TARGET_MET", 0)', "return True")]),
    ("B-control_ok-always-True",
     [('return rc == 1 and marker == ("TARGET_MISSED", 1)', "return True")]),
    ("C-outcome_exit-always-0",
     [("return 0 if selftest_rc == 0 and killed == 2 else 1", "return 0")]),
    ("G-mr_killed-drops-forged_credit-term", [(G_FIND, G_REPL)]),
    ("H-outcome_verdict-constant-met",
     [('return "TARGET_MET" if selftest_rc == 0 and killed == 2 else "TARGET_MISSED"',
       'return "TARGET_MET"')]),
    ("I-subprocess-spawn-guard-disabled",
     [("subprocess.run = _no_spawn", "pass  # spawn guard disabled by R68RevC1")]),
    ("D1-paired-S2-plus-none-killed-expect-edit",
     [("mz_killed = mz_rc != 0", "mz_killed = True"),
      ("selftest=0 mz=fail mr=fail killed=0/2 ", "selftest=0 mz=pass mr=fail killed=1/2 ")]),
    ("D2-total-expectation-rewrite-S3",
     [("killed = int(mz_killed) + int(mr_killed)", "killed = 2"),
      ('line2 == ("MADO_R68_LANDING_CONTROLS: selftest=0 mz=fail mr=fail killed=0/2 "',
       'line2 == ("MADO_R68_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 "'),
      ('"baseline=0/2 verdict=TARGET_MISSED rev=" + sha))',
       '"baseline=0/2 verdict=TARGET_MET rev=" + sha))'),
      ('want("scripted none-killed exits 1", rc2 == 1)',
       'want("scripted none-killed exits 1", rc2 == 0)')]),
    ("K-mz_killed-ran-not-died-credit",
     [("mz_killed = mz_rc != 0", "mz_killed = mz_rc is not None")]),
]

print("########## section 1+2: hand recipes and selftest-breaking mutants")
shutil.rmtree(MUTDIR, ignore_errors=True)
os.makedirs(MUTDIR)
for name, pairs in MUTANTS:
    t = src
    counts = []
    aborted = False
    for f, r in pairs:
        n = t.count(f)
        counts.append((f, n))
        if n != 1:
            print("MUTANT %s ABORTED find-count=%d find=%r" % (name, n, f))
            aborted = True
            break
        t = t.replace(f, r, 1)
    if aborted:
        continue
    try:
        compile(t, "<mutant>", "exec")
        compiles = "yes"
    except SyntaxError as exc:
        compiles = "NO (%s)" % exc
    p = os.path.join(MUTDIR, name + ".py")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(t)
    os.chmod(p, 0o755)
    st = os.path.join(MUTDIR, "st-" + name)
    r = subprocess.run([sys.executable, "-I", p, "--selftest", "--scratch-root", st],
                       capture_output=True, text=True, timeout=300)
    out = r.stdout + r.stderr
    fails = [ln.strip() for ln in out.splitlines() if "FAIL" in ln]
    summ = [ln.strip() for ln in out.splitlines() if "SELFTEST:" in ln]
    verdict = "KILLED" if r.returncode != 0 else "SURVIVED"
    print("== MUTANT %s" % name)
    for f, n in counts:
        print("   edit find=%r occurrences=%d" % (f if len(f) <= 70 else f[:67] + "...", n))
    print("   compiles=%s sha256=%s" % (compiles, hashlib.sha256(t.encode()).hexdigest()))
    print("   selftest rc=%d -> %s" % (r.returncode, verdict))
    for ln in summ:
        print("   %s" % ln)
    for ln in fails[:8]:
        print("   FAILLINE %s" % ln)

print()
print("########## section 3: evidence lines from the scripted (no-spawn) measure() body")
spec = importlib.util.spec_from_file_location("h68", HARNESS)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
work = os.path.join(S, "probe")
shutil.rmtree(work, ignore_errors=True)
os.makedirs(work)
for case in ({"name": "both-killed", "mz_rc": 1, "child_rc": 0, "child_marker": h.MET_MARKER},
             {"name": "none-killed", "mz_rc": 0, "child_rc": 1, "child_marker": h.MISSED_MARKER}):
    scratch = os.path.join(work, "scripted-" + case["name"])
    os.makedirs(scratch, exist_ok=True)
    args = argparse.Namespace(repo=work, rev="HEAD", scratch_root=scratch)
    saved = h.run
    h.run = h._scripted_run(case, "a" * 40)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            rc = h.measure(args)
    finally:
        h.run = saved
    print("===== scripted case %s: measure() rc=%d, captured evidence lines:" % (case["name"], rc))
    for ln in buf.getvalue().splitlines():
        if ln.startswith(("MADO_R68_EXTRACT", "MADO_R68_SELFTEST", "MADO_R68_MUTANT",
                          "MADO_R68_R_CONTROL", "MADO_R68_CHILD_ENV", "MADO_R68_R_CHILD",
                          "MADO_R68_GUARDS", "MADO_R68_LANDING_CONTROLS")):
            print("   %s" % ln[:220])

print()
print("########## section 4: counter contract regex vs the final line printed at the tip")
cspec = importlib.util.spec_from_file_location("cnt68", COUNTER)
c = importlib.util.module_from_spec(cspec)
cspec.loader.exec_module(c)
tip_line = ("MADO_R68_SELFMUTANTS: selftest=0 killed=3/3 applied=3/3 base=0/3 "
            "verdict=TARGET_MET rev=40d2bef8964a098ae50f01094fa19e4725952010")
base_line = ("MADO_R68_SELFMUTANTS: selftest=absent killed=0/3 applied=0/3 base=0/3 "
             "verdict=TARGET_MISSED rev=510100c81e6cf63fec6be380c2f2f9c670f32cbc")
print("tip-line fullmatches counter CONTRACT_RE:      %s" % bool(c.CONTRACT_RE.fullmatch(tip_line)))
print("baseline-line fullmatches counter CONTRACT_RE: %s" % bool(c.CONTRACT_RE.fullmatch(base_line)))
print("counter met-condition: rc==0 and killed==len(RECIPES) == 3 (source: measure())")

print()
print("########## scratch-path sanity")
probe = S
while probe != os.path.dirname(probe):
    print("component %s islink=%s" % (probe, os.path.islink(probe)))
    probe = os.path.dirname(probe)
