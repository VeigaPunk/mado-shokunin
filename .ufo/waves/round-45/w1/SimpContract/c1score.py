#!/usr/bin/env python3
"""Score the reference, the proposed deletions, and unpinned-semantics mutants with the frozen C1 counter."""
import os
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FREEZE = "22a8dedd02f507689c567777e0f20b5e645c8ce0"
REF = LANE + "/.ufo/waves/round-45/l1-draft/mado-monitors.py"
CTR = LANE + "/quality/counters/c1-r45-monitors.py"
SCR = "/fast/scratch/hyaku/mado-r45/SimpContract"
SRC = open(REF, encoding="utf-8").read()

DELETIONS = [
    ("D1-isfinite", "    return math.isfinite(x) and x == math.floor(x + 0.5)",
     "    return x == math.floor(x + 0.5)"),
    ("D2-zpos", "    if z > 0 and whole(w / z) and whole(h / z):",
     "    if whole(w / z) and whole(h / z):"),
    ("D3-cand0", "            if cand != 0 and whole(w / cand) and whole(h / cand):",
     "            if whole(w / cand) and whole(h / cand):"),
    ("D4-isinstance", "        if not (isinstance(mo, str) and len(ids) >= 1 and mo == str(ids[0])):",
     "        if not (len(ids) >= 1 and mo == str(ids[0])):"),
]
SINGLE = [
    ("M3-range90", "    for i in range(1, 90):", "    for i in range(1, 91):"),
    ("M4-order", "        for cand in ((k + i) / 120.0, (k - i) / 120.0):",
     "        for cand in ((k - i) / 120.0, (k + i) / 120.0):"),
    ("M15-emptyskip", '        sel = rules[n - 1]["sel"]\n        if sel == "":\n            continue\n',
     '        sel = rules[n - 1]["sel"]\n'),
    ("M20-f32rate", '    rule["rate"] = f32(float(m.group(4))) if m.group(4) is not None else 60.0',
     '    rule["rate"] = float(m.group(4)) if m.group(4) is not None else 60.0'),
    ("M44-wpos", '            e = expected_scale(rule["scale"], w, h) if w > 0 and h > 0 else None',
     '            e = expected_scale(rule["scale"], w, h)'),
]


def apply(src, pairs):
    for _, old, new in pairs:
        n = src.count(old)
        if n != 1:
            raise SystemExit("bad pattern %r count=%d" % (old[:50], n))
        src = src.replace(old, new)
    return src


D = tempfile.mkdtemp(prefix="c1clone-", dir=SCR)
subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", LANE, D], check=True)
top = subprocess.run(["git", "-C", D, "rev-parse", "--show-toplevel"], capture_output=True).stdout
assert top.decode().strip() == D, top
subprocess.run(["git", "-C", D, "checkout", "-q", "--detach", FREEZE], check=True)

work = os.path.join(SCR, "w1work")
os.makedirs(work, exist_ok=True)


def score(tag, src):
    os.makedirs(os.path.join(D, "tools"), exist_ok=True)
    with open(os.path.join(D, "tools", "mado-monitors.py"), "w") as f:
        f.write(src)
    subprocess.run(["git", "-C", D, "add", "-A"], check=True)
    subprocess.run(["git", "-C", D, "-c", "user.name=seat", "-c", "user.email=seat@scratch.invalid",
                    "commit", "-q", "-m", tag], check=True)
    p = subprocess.run([sys.executable, "-I", CTR, "--repo", D, "--rev", "HEAD", "--work", work],
                       capture_output=True, text=True)
    lines = [l for l in p.stdout.splitlines() if l.startswith("PRED-C1-r45:") or "clause=s " in l]
    print("%-16s rc=%d %s" % (tag, p.returncode, " | ".join(lines)), flush=True)


score("ref", SRC)
score("deletions4", apply(SRC, DELETIONS))
for tag, old, new in SINGLE:
    score(tag, apply(SRC, [(tag, old, new)]))
shutil.rmtree(D, ignore_errors=True)
print("clone removed:", not os.path.exists(D))
