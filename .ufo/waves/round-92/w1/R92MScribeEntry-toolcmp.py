#!/usr/bin/env python3
"""DRAFT: run the candidate over every L1 case fixture and compare with the labelled expect. Not a measurement."""
import base64, json, os, shutil, subprocess, sys, tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
CASES = LANE + "/.ufo/waves/round-92/controls/xdgmime-cases-r92-l1.json"
TOOL = LANE + "/.ufo/waves/round-92/build/mado-xdgmime.c1.py"
SCRATCH = "/fast/scratch/hyaku/mado-r92/R92MScribeEntry/toolcmp"
os.makedirs(SCRATCH, exist_ok=True)
cases = json.load(open(CASES))["cases"]


def sub(v, root):
    return v.replace("{ROOT}", root)


def materialise(case, root):
    items = sorted(case.get("files", {}).items(), key=lambda kv: (0 if kv[1].get("dir") else 1, kv[0]))
    for rel, spec in items:
        p = os.path.join(root, rel)
        if spec.get("dir"):
            os.makedirs(p, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(p) or root, exist_ok=True)
        if "symlink" in spec:
            os.symlink(sub(spec["symlink"], root), p)
            continue
        data = base64.b64decode(spec["b64"]) if "b64" in spec else spec["text"].encode("utf-8", "surrogateescape")
        open(p, "wb").write(data)
    for rel, spec in items:
        if "mode" in spec and "symlink" not in spec:
            os.chmod(os.path.join(root, rel), int(spec["mode"], 8))


bad = []
n = 0
for c in cases:
    root = tempfile.mkdtemp(prefix="c-", dir=SCRATCH)
    materialise(c, root)
    args = [sys.executable, "-I", TOOL, "--json", "--cwd", root]
    for k, v in c["env"].items():
        args += ["--env", f"{k}={sub(v, root)}"]
    args += ["--"] + list(c["types"])
    p = subprocess.run(args, capture_output=True)
    if p.returncode != 0:
        bad.append((c["id"], "tool_rc", p.returncode, p.stderr.decode()[:200]))
        shutil.rmtree(root, ignore_errors=True)
        continue
    got = json.loads(p.stdout)["results"]
    for r in got:
        exp = c["expect"][r["type"]]
        n += 1
        if (r["default"], r["rc"]) != (exp["default"], exp["rc"]):
            bad.append((c["id"], r["type"], r["default"], r["rc"], exp["default"], exp["rc"]))
    shutil.rmtree(root, ignore_errors=True)
print(f"DRAFT_TOOL_CHECK rows={n} mismatches={len(bad)}")
for b in bad:
    print(b)
