#!/usr/bin/env python3
# R56ConnHistory — C2 channel demonstration. reader.py (next to this file) never parses its config; it answers
# with the expected.out found beside or above any absolute path it receives. It is run in the harness shape of
# registration.md section C2: the committed fixtures exported at the freeze commit, {FX} replaced by the absolute
# fixture directory inside the export, cwd = export root, scrubbed environment. The hold-out is not exported,
# not read and not named by this script. Writes only under --work.
# Run: python3 -I -B sibling-run.py --work <scratch dir>
import argparse
import io
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tarfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "3423ae285676c2a10273000f4519163472b443db"
FIX = ".ufo/waves/round-56/fixtures/c2"

ap = argparse.ArgumentParser()
ap.add_argument("--work", required=True)
a = ap.parse_args()
work = pathlib.Path(a.work).resolve()
exp = work / "export"
if exp.exists():
    shutil.rmtree(exp)
exp.mkdir(parents=True)
data = subprocess.run(["git", "-C", LANE, "archive", REV, FIX], capture_output=True, check=True).stdout
tarfile.open(fileobj=io.BytesIO(data)).extractall(exp, filter="tar")
shutil.copy(pathlib.Path(__file__).resolve().parent / "reader.py", work / "reader.py")
root = exp / FIX
ok, bad = [], []
for d in sorted(p for p in root.iterdir() if p.is_dir()):
    args = [x.replace("{FX}", str(d)) for x in json.loads((d / "args.json").read_text())]
    r = subprocess.run([sys.executable, "-I", "-B", str(work / "reader.py"), *args], cwd=exp,
                       capture_output=True, env={"PATH": os.environ.get("PATH", ""), "LANG": "C"})
    eo = (d / "expected.out").read_bytes()
    erc = int((d / "expected.rc").read_text().strip())
    (ok if (r.stdout == eo and r.returncode == erc) else bad).append(d.name)
print(f"SIBLING_READER rev={REV[:12]} committed_pass={len(ok)}/{len(ok) + len(bad)} fail={bad}")
sys.exit(0 if not bad else 1)
