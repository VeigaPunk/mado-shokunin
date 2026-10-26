#!/usr/bin/env python3
"""Controls for PRED-C1-r45-v2 (registration-v2.md). One scratch clone per control under --work (git -C <dir> only,
scratch identity, never the lane); each commits its tools/mado-monitors.py and is scored by the frozen v2 counter
quality/counters/c1-r45-monitors-v2.py with one fixed nonce for all controls. PASS iff the v2 reference scores
TARGET_MET and every other control scores TARGET_MISSED: the base (tool absent), tools/mado-geometry.py copied, a
stub, the v1 reference, the v1 variants K03-K15 re-cut on the v2 reference, the v2 variants K16-K25 (one v2
correction undone each), the 11 cheat tools of w1/CritC1Cheat and the 7 do-nothing controls of w1/ExecDoNothingC1.

    python3 -I .ufo/waves/round-45/ctl/run-c1-controls-v2.py --lane <lane repo> --work <scratch dir> [--nonce N]
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile

BASE = "0c89478af821a6424c9ac922eafe02e39630cf4f"
W = ".ufo/waves/round-45"
REF2 = W + "/v2/mado-monitors.py"
REF1 = W + "/l1-draft/mado-monitors.py"
COUNTER = "quality/counters/c1-r45-monitors-v2.py"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}

STUB = '''import sys
if sys.argv[1:] == ["--selftest"]:
    print("MADO_MONITORS_SELFTEST: 48/48 passed")
    sys.exit(0)
print("MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK")
'''

VARIANTS = [
    ("K03-RATE-NO-DEFAULT", "a rule without @RATE accepts any refresh",
     [('abs(rr - rule["rate"]) < 1.0', '(rule["rate"] == 60.0 or abs(rr - rule["rate"]) < 1.0)')]),
    ("K04-TOLERANCE-LE", "|live - RATE| <= 1 agrees", [('abs(rr - rule["rate"]) < 1.0', 'abs(rr - rule["rate"]) <= 1.0')]),
    ("K05-NO-SCALE-CORRECTION", "the expected scale is the written scale",
     [("def expected_scale(s, w, h):\n", "def expected_scale(s, w, h):\n    return s\n")]),
    ("K06-FIRST-MATCH", "the first matching rule wins",
     [("for n in range(len(rules), 0, -1):", "for n in range(1, len(rules) + 1):")]),
    ("K07-NO-ERASE", "adding a rule keeps earlier same-selector rules",
     [('rules[:] = [r for r in rules if r["sel"] != rule["sel"]]', "pass")]),
    ("K08-LIVE-HYPRCTL", "reads the live compositor instead of the dump",
     [('mdata = read_stdin() if monitors == "-" else read_regular(monitors)',
       'import subprocess; mdata = subprocess.run(["hyprctl", "monitors", "all", "-j"], capture_output=True).stdout or b"[]"')]),
    ("K09-V2-IGNORED", "monitorv2 blocks are not counted", [('counts["v2"] += 1', "pass")]),
    ("K10-BADKEY-KEEPS-RULE", "an unknown key keeps the rule",
     [('                counts["badrules"] += 1\n                return', '                counts["badrules"] += 1\n                break')]),
    ("K11-NO-DESC", "desc: selectors never match", [('if sel.startswith("desc:"):', "if False:")]),
    ("K12-NO-TRANSFORM-MODIFIER", "the transform modifier line is ignored",
     [('cpy["transform"] = t\n                add(rules, cpy)', "pass")]),
    ("K13-ADDRESERVED-NO-DEFAULT", "addreserved without a rule adds nothing",
     [("        add(rules, new_rule(sel))\n        return\n    r = new_rule(sel)", "        return\n    r = new_rule(sel)")]),
    ("K14-MIRROR-IGNORED", "mirror is never compared",
     [('    if rule["mirror"]:\n', "    if False:\n"), ('elif mo != "none":', "elif False:")]),
    ("K15-UNSUPPORTED-SILENT", "unmodelled lines do not make the verdict NOT_COMPARED",
     [('counts["unsupported"] += 1', "pass")]),
    ("K16-DESC-SHORT-ONLY", "desc: tests the short description only",
     [("if desc.startswith(text) or longd.startswith(text):", "if desc.startswith(text):")]),
    ("K17-TRANSFORM-ONE-DIGIT", "transform values must be one digit (v1)",
     [('if INT_RE.fullmatch(value) and 0 <= int(value) <= 7:', 'if len(value) == 1 and value in "01234567":')]),
    ("K18-ADDRESERVED-STRICT", "addreserved fields must be plain integers (v1)",
     [("STOI_RE.match(fld(i))", "INT_RE.fullmatch(fld(i))")]),
    ("K19-ZERO-MODE-EXPLICIT", "0x0 is compared as an explicit mode",
     [("    if w == 0 and h == 0:\n        return\n", "")]),
    ("K20-UNPREDICTED-AGREES", "an unpredicted scale is reported AGREE (v1)",
     [('return [], ("NOT_COMPARED" if unpredicted else "AGREE")', 'return [], "AGREE"')]),
    ("K21-FIELDS-SPACE-TAB-ONLY", "fields are stripped of spaces and tabs only (v1)",
     [("fields = [f.strip(WS) for f in body.split(\",\")]", "fields = [f.strip(\" \\t\") for f in body.split(\",\")]")]),
    ("K22-NONFINITE-NUMBERS", "NaN and Infinity count as numbers",
     [(" and math.isfinite(v)\n", "\n")]),
    ("K23-DEEP-JSON-CRASH", "a parser recursion error is not bad_json",
     [("except (UnicodeDecodeError, ValueError, RecursionError):", "except (UnicodeDecodeError, ValueError):")]),
    ("K24-KEY-TRANSFORM-INVALID-DROPS", "an invalid transform key value makes the line unsupported (v1)",
     [('                if t is not None:\n                    r["transform"] = t',
       '                if t is None:\n                    raise Unsupported()\n                r["transform"] = t')]),
    ("K25-NO-SIZE-CAP", "the 1 MiB input cap is not enforced", [("MAX_BYTES = 1048576", "MAX_BYTES = 1 << 40")]),
]


def git(d, *args):
    return subprocess.run(["git", "-C", d, *args], capture_output=True, env=ENV, check=True).stdout


def build(lane, work, name, text):
    d = tempfile.mkdtemp(dir=work, prefix=name[:40] + "-")
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


def score(lane, work, repo, nonce):
    w = tempfile.mkdtemp(dir=work, prefix="w-")
    p = subprocess.run([sys.executable, "-I", os.path.join(lane, COUNTER), "--repo", repo, "--rev", "HEAD",
                        "--work", w, "--nonce", str(nonce)], capture_output=True, text=True)
    return p.returncode, p.stdout.strip().split("\n")[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--nonce", type=int, default=4545)
    a = ap.parse_args()
    lane = os.path.realpath(a.lane)
    work = tempfile.mkdtemp(dir=a.work, prefix="ctl-c1v2-")
    try:
        ref2 = open(os.path.join(lane, REF2)).read()
        controls = [("REF2", "the v2 reference (positive control)", ref2),
                    ("K00-BASE-ABSENT", "the base tree, tool absent", None),
                    ("K01-GEOMETRY-COPY", "tools/mado-geometry.py copied as the tool",
                     git(lane, "show", BASE + ":tools/mado-geometry.py").decode()),
                    ("K02-STUB", "prints OK and a 48/48 selftest", STUB),
                    ("K26-V1-REFERENCE", "the v1 reference (l1-draft)", open(os.path.join(lane, REF1)).read())]
        for name, what, subs in VARIANTS:
            t = ref2
            for old, new in subs:
                if old not in t:
                    raise SystemExit("variant %s: anchor not found: %r" % (name, old[:60]))
                t = t.replace(old, new)
            controls.append((name, what, t))
        for path in sorted(glob.glob(os.path.join(lane, W, "w1/CritC1Cheat/tools/cheat-*.py"))):
            controls.append(("W1-" + os.path.basename(path)[:-3], "w1/CritC1Cheat " + os.path.basename(path),
                             open(path).read()))
        for path in sorted(glob.glob(os.path.join(lane, W, "w1/ExecDoNothingC1/control-*.py"))):
            controls.append(("W1-" + os.path.basename(path)[:-3], "w1/ExecDoNothingC1 " + os.path.basename(path),
                             open(path).read()))
        met_ref, wrong = 0, 0
        print("CTL_C1v2: nonce=%d controls=%d (REF2 positive; %d negative)" % (a.nonce, len(controls), len(controls) - 1))
        for name, what, text in controls:
            repo = build(lane, work, name, text)
            rc, last = score(lane, work, repo, a.nonce)
            met = "verdict=TARGET_MET" in last
            if name == "REF2":
                met_ref = int(met)
            elif met:
                wrong += 1
            fx = " ".join(last.split()[1:3]) if last.startswith("PRED-C1-r45-v2:") else last
            print("CTL_C1v2 %s (%s): rc=%d %s %s" % (name, what, rc, fx, "TARGET_MET" if met else "TARGET_MISSED"))
            shutil.rmtree(repo, ignore_errors=True)
        ok = met_ref == 1 and wrong == 0
        print("CTL_C1v2 VERDICT: %s (controls scoring TARGET_MET: %d of %d; reference met: %d)" % (
            "PASS" if ok else "FAIL", wrong, len(controls) - 1, met_ref))
        return 0 if ok else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
