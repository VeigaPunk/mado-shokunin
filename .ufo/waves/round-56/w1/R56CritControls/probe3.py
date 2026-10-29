import json, subprocess, shutil, os, sys, re
from pathlib import Path
W=Path("/fast/scratch/hyaku/mado-r56/R56CritControls/x/.ufo/waves/round-56"); T=json.load(open(W/"frozen-tables.json"))
print("top keys:", list(T.keys()), "c2 keys:", [k for k in T["c2"] if k!="fixture_files"], "c2.holdout:", T["c2"].get("holdout_commit_sha256"))
ROOT=Path("probe_export").resolve()
def export(strip_expected):
    if ROOT.exists(): shutil.rmtree(ROOT)
    shutil.copytree(W/"fixtures"/"c2", ROOT/"fixtures"/"c2", symlinks=True)
    shutil.copytree(W/"ctl", ROOT/"ctl")
    # synthetic hold-out-shaped copy (NOT the sealed set): H01 := copy of F01 layout, used only to show layout-equivalence
    shutil.copytree(W/"fixtures"/"c2"/"F01", ROOT/"fixtures"/"c2-holdout"/"H01", symlinks=True)
    if strip_expected:
        for p in ROOT.rglob("expected.*"): p.unlink()
        for p in ROOT.rglob("note.txt"): p.unlink()
def run(stub, fx):
    args=json.load(open(W/"fixtures"/"c2"/fx/"args.json"))
    args=[a.replace("{FX}", str(ROOT/"fixtures"/"c2"/fx)) for a in args]
    p=subprocess.run(["python3","-I",str(ROOT/"ctl"/stub),*args],cwd=ROOT,capture_output=True,env={"PATH":"/usr/bin:/bin"})
    exp=(W/"fixtures"/"c2"/fx/"expected.out").read_bytes() if (W/"fixtures"/"c2"/fx/"expected.out").exists() else None
    expc=int((W/"fixtures"/"c2"/fx/"expected.rc").read_text().strip())
    ok = p.stdout==exp and p.returncode==expc
    return ok
fxs=sorted(d.name for d in (W/"fixtures"/"c2").iterdir() if d.is_dir())
for stub in ["const-host.py","empty.py","lookup-committed.py"]:
    export(False)
    res=[run(stub,f) for f in fxs]
    print(stub, "committed pass", sum(res), "/", len(res), "passing:", [f for f,r in zip(fxs,res) if r])
