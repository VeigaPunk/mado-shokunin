#!/usr/bin/env python3
"""Falsifier matrix for r56_ctl_c1.py (run: python3 -I test_matrix.py WITNESS_REPO WITNESS_SHA WORK).

1. scope test: each control's scratch commit differs from the good commit by exactly the registered files;
2. counter-variant matrix: ref_counter.py with ONE leg disabled / one protocol defect must lose the matching control
   (and good must stay ok unless the defect is protocol-level); results printed as a table.
"""
import os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
H = HERE.parent
repo, rev, work = sys.argv[1], sys.argv[2], Path(sys.argv[3])
work.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(H))
import r56_ctl_c1 as h

# ---- 1. mutation scope ----
tmp = Path(tempfile.mkdtemp(prefix="scope-", dir=str(work)))
W = tmp
ctx_json = h.json.loads(h.git(W, "-C", repo, "show", "%s:%s" % (rev, h.TABLES_PATH)))["c1"]
ctx = {"entry": ctx_json["entry"], "pin_dir": ctx_json["pin_dir"], "k_ids": [r["id"] for r in ctx_json["k"]], "h_ids": [r["id"] for r in ctx_json["h"]]}
good = W / "good"
h.export_good(W, repo, rev, [ctx["entry"], h.TABLES_PATH, ctx["pin_dir"], *h.EXTRA_PATHS], good)
base = W / "repos"; base.mkdir()
d0, s0 = h.materialize(W, base, "good", good, None)
print("== scope: files changed per control vs the good commit")
for cid, name, mut, req, chk, coll in h.CONTROLS:
    d, s = h.materialize(W, base, cid.lower(), good, lambda dd, m=mut: m(dd, ctx))
    out = h.git(W, "-C", str(d), "diff", "--stat", "--stat-width=150", "--no-color", "--compare-to" if False else s0 if False else "HEAD~0", "--") if False else b""
    # compare trees by blob listing (separate repos): diff two directories
    r = subprocess.run(["diff", "-rq", "--exclude=.git", str(d0), str(d)], capture_output=True, text=True)
    changed = [l.replace(str(d0) + "/", "").replace(str(d) + "/", "") for l in r.stdout.strip().split("\n") if l]
    print("%s %-20s %s" % (cid, name, "; ".join(changed)))

# ---- 2. variant matrix ----
src = (HERE / "ref_counter.py").read_text()
VARIANTS = [
    ("no-entry_absent", 'missed.insert(0, "entry_absent")', "pass", "C1-CTL-01"),
    ("no-prov", 'missed.append("prov")', "pass", "C1-CTL-06"),
    ("no-num", 'missed.append("num:" + rid)', "pass", "C1-CTL-03"),
    ("no-source_cell", 'missed.append("source_cell:" + rid)', "pass", "C1-CTL-04"),
    ("no-scope", 'missed.append("scope:" + rid)', "pass", "C1-CTL-05"),
    ("no-quote-leg", 'missed.append("quote:" + rid)', "pass", "C1-CTL-08"),
    ("no-row-leg", 'missed.append("row:" + rid)', "pass", "C1-CTL-07"),
    ("no-pin_hash", 'missed.append("pin_hash")', "pass", "C1-CTL-09"),
    ("no-new_rows", 'missed.append("new_rows")', "pass", "C1-CTL-10"),
]
def write(name, text):
    p = work / ("var-%s.py" % name); p.write_text(text); return p
def run_h(counter):
    p = subprocess.run([sys.executable, "-I", str(H / "r56_ctl_c1.py"), "--repo", repo, "--rev", rev, "--work", str(work / "hw"), "--counter", str(counter)],
                       capture_output=True, text=True)
    err = p.stderr
    failed = re.findall(r"^(C1-CTL-\d\d) \S+: FAIL", err, re.M)
    return p.returncode, p.stdout.strip(), failed, err
print("== variant matrix")
rows = []
for name, old, new, want in VARIANTS:
    assert src.count(old) >= 1, (name, old)
    rc, out, failed, err = run_h(write(name, src.replace(old, new)))
    print("%-16s rc=%d %s failed=%s expect=%s %s" % (name, rc, out, ",".join(failed), want, "OK" if want in failed and rc == 1 else "UNEXPECTED"))
# tok-disable: disabling tok+num together must lose junk control (CTL-02)
t = src.replace('missed.append("tok:" + rid)', "pass").replace("if tok_ok and num_ok:", "if True:")
rc, out, failed, err = run_h(write("no-tok", t))
print("%-16s rc=%d %s failed=%s expect=C1-CTL-02 %s" % ("no-tok(+content)", rc, out, ",".join(failed), "OK" if "C1-CTL-02" in failed else "UNEXPECTED"))
# protocol defects
PROT = {
    "exit0-on-miss": ("wrap", "import subprocess,sys,os\np=subprocess.run([sys.executable,'-I',%r]+sys.argv[1:],capture_output=True)\nsys.stdout.buffer.write(p.stdout)\nsys.exit(0)\n"),
    "met-with-legs": ("wrap", "import subprocess,sys\np=subprocess.run([sys.executable,'-I',%r]+sys.argv[1:],capture_output=True)\nsys.stdout.write(p.stdout.decode().replace('TARGET_MISSED','TARGET_MET'))\nsys.exit(p.returncode)\n"),
    "two-lines": ("wrap", "import subprocess,sys\np=subprocess.run([sys.executable,'-I',%r]+sys.argv[1:],capture_output=True)\nsys.stdout.write('hello\\n'+p.stdout.decode())\nsys.exit(p.returncode)\n"),
    "crash-rc2": ("wrap", "import sys\nsys.stderr.write('boom\\n')\nsys.exit(2)\n"),
    "wrong-rev": ("wrap", "import subprocess,sys\np=subprocess.run([sys.executable,'-I',%r]+sys.argv[1:],capture_output=True)\nsys.stdout.write(p.stdout.decode().replace('rev=','rev=x'))\nsys.exit(p.returncode)\n"),
    "bad-leg-grammar": ("wrap", "import subprocess,sys\np=subprocess.run([sys.executable,'-I',%r]+sys.argv[1:],capture_output=True)\nsys.stdout.write(p.stdout.decode().replace('missed=none','missed=ok').replace('missed=','missed=Z,'))\nsys.exit(p.returncode)\n"),
}
refp = HERE / "ref_counter.py"
for name, (kind, body) in PROT.items():
    text = body % str(refp) if "%r" in body else body
    rc, out, failed, err = run_h(write(name, text))
    print("%-16s rc=%d %s failed=%s" % (name, rc, out, ",".join(failed) or "-"))
shutil.rmtree(tmp, ignore_errors=True)
