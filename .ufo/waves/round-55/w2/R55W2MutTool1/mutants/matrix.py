import json, os, subprocess, sys, glob
# run every tool on each survivor fixture; compare to original output (stdout bytes + rc)
root = sys.argv[1]
orig = sys.argv[2]
tools = sorted(glob.glob(os.path.join(root, "work/mut/M*.py")))
surv = sorted(glob.glob(os.path.join(root, "work/survivors/S*")))
def run(tool, args, cwd):
    p = subprocess.run([sys.executable, "-I", tool] + args, cwd=cwd, capture_output=True, timeout=60)
    return p.stdout, p.returncode
base = {}
for s in surv:
    args = json.load(open(os.path.join(s, "args.json")))
    base[os.path.basename(s)] = run(orig, args, os.path.join(root, "work"))
for t in tools:
    row = []
    for s in surv:
        sid = os.path.basename(s)
        args = json.load(open(os.path.join(s, "args.json")))
        out = run(t, args, os.path.join(root, "work"))
        row.append("%s:%s" % (sid, "KILL" if out != base[sid] else "-"))
    print(os.path.basename(t), " ".join(row))
