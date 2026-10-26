#!/usr/bin/env python3
"""C1 controls for PRED-C1-r46: the reference must be TARGET_MET; every control must be TARGET_MISSED.

Each control is a tool installed at tools/mado-devices.py on a scratch clone of the freeze commit and scored with the
frozen counter at one nonce. Controls: the base (no tool), a stub that prints an OK summary, tools/mado-monitors.py
copied, and reference variants that each undo one modelled semantic (string edits of the reference, each asserted to
apply exactly once).
Run: python3 -I run-c1-controls.py <lane> <freeze-rev> <scratch-dir> [nonce]
"""
import os
import shutil
import subprocess
import sys

LANE, REV, SCR = sys.argv[1], sys.argv[2], sys.argv[3]
NONCE = sys.argv[4] if len(sys.argv) > 4 else "4646"
REF = os.path.join(LANE, ".ufo/waves/round-46/l1-draft/mado-devices.py")
COUNTER = os.path.join(LANE, "quality/counters/c1-r46-devices.py")
ref = open(REF).read()

STUB = '''import sys
if sys.argv[1:] == ["--selftest"]:
    print("MADO_DEVICES_SELFTEST: 30/30 passed"); sys.exit(0)
print("MADO_DEVICES: keyboards=1 agree=1 differ=0 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=OK")
'''

VARIANTS = {
    # (old, new) applied exactly once to the reference
    "V01-no-fallback-verdict": ('        elif rep == FALLBACK:\n', '        elif False:\n'),
    "V02-global-scroll-factor": ('exp = min(max(blk["scroll_factor"], 0.0), 100.0) if "scroll_factor" in blk else -1.0',
                                 'exp = min(max(blk["scroll_factor"], 0.0), 100.0) if "scroll_factor" in blk else 1.0'),
    "V03-case-insensitive-names": ('        name = kb["name"]\n', '        name = kb["name"].lower()\n'),
    "V04-no-bracket": ('        if lb != -1 and rb != -1 and lb < rb:', '        if False:'),
    "V05-no-continuation": ('        while line.endswith("\\\\"):', '        while False:'),
    "V06-no-hash-escape": ('        if pos < len(line) - 1 and line[pos + 1] == "#":', '        if False:'),
    "V07-virtual-compared": ('        if name.startswith(VIRTUAL_PREFIX):', '        if False:'),
    "V08-stale-ignored": ('        stale += 0 if ok else 1\n', '        stale += 0\n'),
    "V09-no-clamp": ('min(max(blk["scroll_factor"], 0.0), 100.0)', 'blk["scroll_factor"]'),
    "V10-device-first": ('        if k in blk:\n            v = blk[k]\n        elif k in st.globals:\n            v = st.globals[k]',
                         '        if k in st.globals:\n            v = st.globals[k]\n        elif k in blk:\n            v = blk[k]'),
    "V11-empty-marker-literal": ('        out.append("" if v == EMPTY else v)', '        out.append(v)'),
    "V12-default-layout-empty": ('            v = "us" if n == "layout" else ""', '            v = ""'),
    "V13-no-float32": ('    v = f32(float(m.group(0)))', '    v = float(m.group(0))'),
    "V14-unsupported-ignored": ('    if st.unsupported:\n', '    if False:\n'),
    "V15-current-device-kept": ('                    if not stack:\n                        cur = None\n',
                                '                    pass\n'),
    "V16-flat-device-key-applies": ('            else:\n                st.unsupported += 1\n                cur = False\n            continue',
                                    '            else:\n                cur = None\n            continue'),
    "V17-variables-modelled": ('        if any(t in lhs or t in rhs for t in ("$", "{{", "\\\\")):',
                               '        if any(t in lhs or t in rhs for t in ("{{",)):'),
    "V18-no-tablet-pad-owner": ('            b = e.get("belongsTo")\n', '            b = None\n'),
    "V19-stale-before-differ": ('    elif c["differ"] + c["fallback"] + c["mice_differ"]:\n        v, rc = "DIFFER", 1\n    elif not c["keyboards"]:\n        v, rc = "NO_KEYBOARDS", 3\n    elif stale:\n        v, rc = "STALE_BLOCK", 4\n',
                                '    elif stale:\n        v, rc = "STALE_BLOCK", 4\n    elif c["differ"] + c["fallback"] + c["mice_differ"]:\n        v, rc = "DIFFER", 1\n    elif not c["keyboards"]:\n        v, rc = "NO_KEYBOARDS", 3\n'),
    "V20-no-stof-prefix": ('    m = FLOAT_RE.match(value)', '    m = FLOAT_RE.fullmatch(value)'),
}


def make(name, body):
    d = os.path.join(SCR, "ctl-" + name)
    shutil.rmtree(d, ignore_errors=True)
    subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", LANE, d], check=True)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    assert top == d, (top, d)
    subprocess.run(["git", "-C", d, "checkout", "-q", "--detach", REV], check=True)
    if body is not None:
        with open(os.path.join(d, "tools/mado-devices.py"), "w") as f:
            f.write(body)
        subprocess.run(["git", "-C", d, "add", "tools/mado-devices.py"], check=True)
        subprocess.run(["git", "-C", d, "-c", "user.name=ctl", "-c", "user.email=ctl@scratch.invalid", "commit", "-qm",
                        name], check=True)
    return d


def score(d):
    w = os.path.join(SCR, "w")
    os.makedirs(w, exist_ok=True)
    p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", d, "--rev", "HEAD", "--work", w, "--nonce", NONCE],
                       capture_output=True, text=True)
    return p.returncode, p.stdout.strip().split("\n")[-1]


def main():
    controls = [("REF", ref), ("BASE", None), ("STUB", STUB),
                ("MONITORS-COPY", open(os.path.join(LANE, "tools/mado-monitors.py")).read())]
    for name, (old, new) in VARIANTS.items():
        assert ref.count(old) == 1, (name, ref.count(old))
        controls.append((name, ref.replace(old, new)))
    met_controls, ref_met = 0, False
    for name, body in controls:
        d = make(name, body)
        rc, last = score(d)
        met = "verdict=TARGET_MET" in last
        if name == "REF":
            ref_met = met
        else:
            met_controls += met
        print("CTL_C1 %s rc=%d %s" % (name, rc, last.split(" rev=")[0]))
        shutil.rmtree(d, ignore_errors=True)
    ok = ref_met and met_controls == 0
    print("CTL_C1 VERDICT: %s (controls scoring TARGET_MET: %d of %d; reference met: %d)" % (
        "PASS" if ok else "FAIL", met_controls, len(controls) - 1, int(ref_met)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
