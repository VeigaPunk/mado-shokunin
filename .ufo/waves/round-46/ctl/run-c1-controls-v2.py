#!/usr/bin/env python3
"""C1 controls for PRED-C1-r46-v2 (registration-v2.md): the v2 reference must be TARGET_MET; every control must be
TARGET_MISSED.

Each control is a tool installed at tools/mado-devices.py on a scratch clone of the freeze commit and scored with the
frozen counter at one nonce. Controls: the base (no tool), a stub that prints an OK summary, tools/mado-monitors.py
copied, the v1 reference, the v1 variants V01-V20 re-cut on the v2 reference, V21-V28 (each undoes one v2 correction),
the w1 cheat tools (w1/CritC1Cheat cheatA-D, w1/CritClaimSizing control-delegator.py) and DELEGATE-ANY (searches the
host's /fast, /home and /tmp for any mado-devices.py and execs it), TRIP-ABSOLUTE-PATH (/usr/bin/hyprctl by
absolute path in every run) and TRIP-SELFTEST-ONLY (bare hyprctl during --selftest only; w1/SentTool F2).
Run: python3 -I run-c1-controls.py <lane> <freeze-rev> <scratch-dir> [nonce]
"""
import os
import shutil
import subprocess
import sys

LANE, REV, SCR = sys.argv[1], sys.argv[2], sys.argv[3]
NONCE = sys.argv[4] if len(sys.argv) > 4 else "4646"
REF = os.path.join(LANE, ".ufo/waves/round-46/v2/mado-devices.py")
REF1 = os.path.join(LANE, ".ufo/waves/round-46/l1-draft/mado-devices.py")
W1 = os.path.join(LANE, ".ufo/waves/round-46/w1")
COUNTER = os.path.join(LANE, "quality/counters/c1-r46-devices-v2.py")
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
    "V13-no-float32": ('    v = round_f32(q)', '    v = float(q)'),
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
    "V20-no-stof-prefix": ('        m = FLOAT_RE.match(value)', '        m = FLOAT_RE.fullmatch(value)'),
    "V21-double-rounding": ('    v = round_f32(q)', '    v = f32(float(q))'),
    "V22-hex-refused": ('    m = HEX_RE.match(value)\n    if m:', '    m = HEX_RE.match(value)\n    if m and False:'),
    "V23-inf-refused": ('        return "ok", -math.inf if m.group(1) == "-" else math.inf', '        return "unsupported", None'),
    "V24-range-unsupported": ('    if math.isinf(v) or (q != 0 and abs(v) < FLT_MIN):\n        return "unset", None',
                              '    if math.isinf(v) or (q != 0 and abs(v) < FLT_MIN):\n        return "unsupported", None'),
    "V25-phantom-final-line": ('    if text.endswith("\\n"):\n        raw_lines.pop()\n', ''),
    "V26-directive-word-boundary": ('words[0].startswith("hyprlang")', 'words[0] == "hyprlang"'),
    "V27-source-in-block-ignored": ('        if lhs == "source" and stack:\n            st.unsupported += 1\n            continue\n', ''),
    "V28-narrow-strip": ('        line = raw.strip(WS)\n        if line.startswith("#"):', '        line = raw.strip(" \\t\\r")\n        if line.startswith("#"):'),
}
DELEGATE_ANY = """import os, sys
for root in ("/fast", "/home", "/tmp"):
    for d, _, fs in os.walk(root):
        if "mado-devices.py" in fs and d.endswith(("v2", "l1-draft", "tools")):
            os.execv(sys.executable, [sys.executable, "-I", os.path.join(d, "mado-devices.py")] + sys.argv[1:])
sys.exit(3)
"""


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
                ("MONITORS-COPY", open(os.path.join(LANE, "tools/mado-monitors.py")).read()),
                ("V1-REF", open(REF1).read()), ("DELEGATE-ANY", DELEGATE_ANY),
                ("DELEGATOR-W1", open(os.path.join(W1, "CritClaimSizing/control-delegator.py")).read())]
    trip_abs = ref.replace("\ndef main():\n", "\ndef main():\n    import subprocess\n    subprocess.run(['/usr/bin/hyprctl', 'version'], capture_output=True)\n", 1)
    trip_st = ref.replace("\ndef selftest():\n", "\ndef selftest():\n    import subprocess\n    subprocess.run(['hyprctl', 'version'], capture_output=True)\n", 1)
    assert trip_abs != ref and trip_st != ref
    controls += [("TRIP-ABSOLUTE-PATH", trip_abs), ("TRIP-SELFTEST-ONLY", trip_st)]
    for c in ("cheatA", "cheatB", "cheatC", "cheatD"):
        controls.append(("CHEAT-" + c[-1], open(os.path.join(W1, "CritC1Cheat/receipts/%s.py" % c)).read()))
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
        print("CTL_C1v2 %s rc=%d %s" % (name, rc, last.split(" rev=")[0]))
        shutil.rmtree(d, ignore_errors=True)
    ok = ref_met and met_controls == 0
    print("CTL_C1v2 VERDICT: %s (controls scoring TARGET_MET: %d of %d; reference met: %d)" % (
        "PASS" if ok else "FAIL", met_controls, len(controls) - 1, int(ref_met)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
