#!/usr/bin/env python3
"""Round-44 C1 controls: score the reference, the base tool, the absent tool and single-defect
variants of the reference with the frozen PRED-C1-r44 counter. Only REF may reach TARGET_MET.
Usage: run-c1-controls.py --repo LANE --rev BASE --work SCRATCHDIR"""
import argparse, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "c1", "ctl-ref-tool.py.txt")
VARIANTS = {
    # name: [(old, new), ...] applied to the reference text; each must match exactly once
    "K01-no-maximized": [('        elif fsmode == 1:\n            verdict = "MAXIMIZED"\n', "")],
    "K02-fields-always": [('    if t["maximized"] + t["fullscreen"] > 0:\n', "    if True:\n")],
    "K03-bool-is-mode": [('isinstance(f, int) and not isinstance(f, bool) and f in (1, 2)', 'isinstance(f, int) and f in (1, 2)')],
    "K04-tiled-first": [('        elif fsmode == 2:\n            verdict = "FULLSCREEN"\n        elif fsmode == 1:\n            verdict = "MAXIMIZED"\n        elif not floating:\n            verdict = "TILED"\n',
                         '        elif not floating:\n            verdict = "TILED"\n        elif fsmode == 2:\n            verdict = "FULLSCREEN"\n        elif fsmode == 1:\n            verdict = "MAXIMIZED"\n')],
    "K05-fullscreen-before-badsize": [('        if size is None:\n            verdict = "BADSIZE"\n        elif fsmode == 2:\n            verdict = "FULLSCREEN"\n',
                                      '        if fsmode == 2:\n            verdict = "FULLSCREEN"\n        elif size is None:\n            verdict = "BADSIZE"\n')],
    "K06-float-is-mode": [('isinstance(f, int) and not isinstance(f, bool) and f in (1, 2)', '(isinstance(f, (int, float)) and not isinstance(f, bool)) and f in (1, 2)'),
                          ("        return f\n    return 0", "        return int(f)\n    return 0")],
    "K07-any-nonzero": [('isinstance(f, int) and not isinstance(f, bool) and f in (1, 2)', 'isinstance(f, int) and not isinstance(f, bool) and f != 0'),
                        ("        return f\n    return 0", "        return 2 if f >= 2 else 1\n    return 0")],
    "K08-client-mode": [('    f = c.get("fullscreen")\n', '    f = c.get("fullscreenClient")\n')],
    "K09-states-differ": [('    elif t["differ"] > 0:\n', '    elif t["differ"] + t["fullscreen"] + t["maximized"] > 0:\n')],
    "K10-swapped-words": [('            verdict = "FULLSCREEN"\n', '            verdict = "MAXIMIZED_"\n'),
                          ('            verdict = "MAXIMIZED"\n', '            verdict = "FULLSCREEN"\n'),
                          ('            verdict = "MAXIMIZED_"\n', '            verdict = "MAXIMIZED"\n')],
    "K11-old-summary": [('                 "matched=%d unmapped=%d agree=%d differ=%d tiled=%d badsize=%d%s verdict=%s" % (', '                 "matched=%d unmapped=%d agree=%d differ=%d tiled=%d badsize=%d%.0s verdict=%s" % (')],
    "K12-field-order": [('states = " maximized=%d fullscreen=%d" % (t["maximized"], t["fullscreen"])', 'states = " fullscreen=%d maximized=%d" % (t["fullscreen"], t["maximized"])')],
    "K13-no-new-selftest": "CUT",
}
CUT_FROM = "    def fs(size, mode, floating=True):\n"
CUT_TO = "    bad = [c for c in cases if not c[1]]\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    counter = os.path.join(a.repo, "quality", "counters", "c1-r44-geometry-states.py")
    ref = open(REF).read()
    os.makedirs(a.work, exist_ok=True)
    runs = [("REF", ["--tool", REF], "met"), ("BASE-tool", [], "missed"),
            ("ABSENT-62dd798", ["--rev-override", "62dd798bb08401a8697383552edcc36f109344fa"], "missed")]
    for name, subs in VARIANTS.items():
        text = ref
        if subs == "CUT":
            i, j = text.index(CUT_FROM), text.index(CUT_TO)
            text, subs = text[:i] + text[j:], []
        for o, n in subs:
            if text.count(o) != 1:
                print("CTL_C1 %s SETUP replacement-count=%d" % (name, text.count(o)))
                sys.exit(2)
            text = text.replace(o, n)
        p = os.path.join(a.work, name + ".py")
        open(p, "w").write(text)
        runs.append((name, ["--tool", p], "missed"))
    print("CTL_C1: rev=%s controls=%d (anchors REF; do-nothing BASE-tool, ABSENT; %d single-defect variants)"
          % (a.rev, len(runs) - 1, len(VARIANTS)))
    wrong, met_ctl, met_ref = 0, 0, 0
    for name, extra, want in runs:
        rev = a.rev
        if extra[:1] == ["--rev-override"]:
            rev, extra = extra[1], []
        cmd = [sys.executable, "-I", counter, "--repo", a.repo, "--rev", rev, "--work", a.work] + extra
        p = subprocess.run(cmd, capture_output=True, text=True)
        lines = p.stdout.strip().splitlines()
        last = lines[-1] if lines else ""
        clauses = next((l for l in lines if " clauses=" in l), "")
        got = "met" if (p.returncode == 0 and "verdict=TARGET_MET" in last) else "missed"
        ok = got == want
        wrong += not ok
        if name == "REF":
            met_ref = int(got == "met")
        else:
            met_ctl += got == "met"
        print("CTL_C1 %s want=%s got=%s rc=%d %s | %s | %s" % (name, want, got, p.returncode,
              "ok" if ok else "WRONG", clauses.split(" clauses=")[-1], last.split(": ", 1)[-1]))
    print("CTL_C1 VERDICT: %s (controls scoring TARGET_MET: %d of %d; reference met: %d)" % (
        "PASS" if wrong == 0 else "FAIL", met_ctl, len(runs) - 1, met_ref))
    return 0 if wrong == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
