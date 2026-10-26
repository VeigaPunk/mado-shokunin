#!/usr/bin/env python3
"""Controls for PRED-C1-r45 (registration.md). Builds one scratch clone per control under --work (git -C <dir>
only, scratch identity, never the lane), commits the control's tools/mado-monitors.py, runs the frozen counter
quality/counters/c1-r45-monitors.py on it and prints one line per control. PASS iff the reference scores
TARGET_MET and every other control (base tool absent, a sibling tool copied, a stub, and cheap variants that drop
one semantic of the contract) scores TARGET_MISSED.

    python3 -I .ufo/waves/round-45/ctl/run-c1-controls.py --lane <lane repo> --work <scratch dir>
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

BASE = "0c89478af821a6424c9ac922eafe02e39630cf4f"
REF = ".ufo/waves/round-45/l1-draft/mado-monitors.py"
COUNTER = "quality/counters/c1-r45-monitors.py"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}

STUB = '''import sys
if sys.argv[1:] == ["--selftest"]:
    print("MADO_MONITORS_SELFTEST: 33/33 passed")
    sys.exit(0)
print("MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK")
'''

# (name, what it drops, [(old, new), ...]) applied to the reference text; each old must occur
VARIANTS = [
    ("K03-RATE-NO-DEFAULT", "a rule without @RATE accepts any refresh",
     [('abs(rr - rule["rate"]) < 1.0', '(rule["rate"] == 60.0 or abs(rr - rule["rate"]) < 1.0)')]),
    ("K04-TOLERANCE-LE", "|live - RATE| <= 1 agrees",
     [('abs(rr - rule["rate"]) < 1.0', 'abs(rr - rule["rate"]) <= 1.0')]),
    ("K05-NO-SCALE-CORRECTION", "the expected scale is the written scale",
     [("def expected_scale(s, w, h):\n", "def expected_scale(s, w, h):\n    return s\n")]),
    ("K06-FIRST-MATCH", "the first matching rule wins",
     [("for n in range(len(rules), 0, -1):", "for n in range(1, len(rules) + 1):")]),
    ("K07-NO-ERASE", "adding a rule keeps earlier same-selector rules",
     [('rules[:] = [r for r in rules if r["sel"] != rule["sel"]]', "pass")]),
    ("K08-LIVE-HYPRCTL", "reads the live compositor instead of the dump",
     [('mdata = read_stdin() if monitors == "-" else read_regular(monitors)',
       'import subprocess; mdata = subprocess.run(["hyprctl", "monitors", "all", "-j"], capture_output=True).stdout or b"[]"')]),
    ("K09-V2-IGNORED", "monitorv2 blocks are not counted",
     [('counts["v2"] += 1', "pass")]),
    ("K10-BADKEY-KEEPS-RULE", "an unknown key keeps the rule",
     [('                counts["badrules"] += 1\n                return', '                counts["badrules"] += 1\n                break')]),
    ("K11-NO-DESC", "desc: selectors never match",
     [('if sel.startswith("desc:"):', "if False:")]),
    ("K12-NO-TRANSFORM-MODIFIER", "the transform modifier line is ignored",
     [('cpy["transform"] = t\n                add(rules, cpy)', "pass")]),
    ("K13-ADDRESERVED-NO-DEFAULT", "addreserved without a rule adds nothing",
     [("        add(rules, new_rule(sel))\n        return\n    r = new_rule(sel)", "        return\n    r = new_rule(sel)")]),
    ("K14-MIRROR-IGNORED", "mirror is never compared",
     [('    if rule["mirror"]:\n', "    if False:\n"), ('elif mo != "none":', "elif False:")]),
    ("K15-UNSUPPORTED-SILENT", "unmodelled lines do not make the verdict NOT_COMPARED",
     [('counts["unsupported"] += 1', "pass")]),
]


def git(d, *args):
    return subprocess.run(["git", "-C", d, *args], capture_output=True, env=ENV, check=True).stdout


def build(lane, work, name, text):
    d = tempfile.mkdtemp(dir=work, prefix=name + "-")
    git(work, "clone", "-q", "--shared", "--no-checkout", lane, d)
    if git(d, "rev-parse", "--show-toplevel").decode().strip() != os.path.realpath(d):
        raise SystemExit("scratch clone toplevel mismatch for %s" % name)
    git(d, "checkout", "-q", BASE)
    if text is not None:
        os.makedirs(os.path.join(d, "tools"), exist_ok=True)
        with open(os.path.join(d, "tools", "mado-monitors.py"), "w") as f:
            f.write(text)
        git(d, "add", "tools/mado-monitors.py")
        git(d, "-c", "user.name=ctl", "-c", "user.email=ctl@scratch.invalid", "commit", "-q", "-m", name)
    return d


def score(lane, work, repo):
    w = tempfile.mkdtemp(dir=work, prefix="w-")
    p = subprocess.run([sys.executable, "-I", os.path.join(lane, COUNTER), "--repo", repo, "--rev", "HEAD",
                        "--work", w], capture_output=True, text=True)
    return p.returncode, p.stdout.strip().split("\n")[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    lane = os.path.realpath(a.lane)
    work = tempfile.mkdtemp(dir=a.work, prefix="ctl-c1-")
    try:
        ref = open(os.path.join(lane, REF)).read()
        geom = git(lane, "show", BASE + ":tools/mado-geometry.py").decode()
        controls = [("REF", "the reference (positive control)", ref),
                    ("K00-BASE-ABSENT", "the base tree, tool absent", None),
                    ("K01-GEOMETRY-COPY", "tools/mado-geometry.py copied as the tool", geom),
                    ("K02-STUB", "prints OK and a 33/33 selftest", STUB)]
        for name, what, subs in VARIANTS:
            t = ref
            for old, new in subs:
                if old not in t:
                    raise SystemExit("variant %s: anchor not found: %r" % (name, old[:60]))
                t = t.replace(old, new)
            controls.append((name, what, t))
        met_ref, wrong = 0, 0
        for name, what, text in controls:
            repo = build(lane, work, name, text)
            rc, last = score(lane, work, repo)
            met = "verdict=TARGET_MET" in last
            if name == "REF":
                met_ref = int(met)
            elif met:
                wrong += 1
            fx = last.split()[1] if last.startswith("PRED-C1-r45:") else last
            print("CTL_C1 %s (%s): rc=%d %s %s" % (name, what, rc, fx, "TARGET_MET" if met else "TARGET_MISSED"))
        ok = met_ref == 1 and wrong == 0
        print("CTL_C1 VERDICT: %s (controls scoring TARGET_MET: %d of %d; reference met: %d)" % (
            "PASS" if ok else "FAIL", wrong, len(controls) - 1, met_ref))
        return 0 if ok else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
