# Mitigation probe: each fixture's input (args + tree) is staged alone and the tool runs in bwrap that can see nothing else.
import json, os, shutil, subprocess, sys
exp, tool, stage = sys.argv[1], sys.argv[2], sys.argv[3]
res = [0, 0]
for fx in sorted(os.listdir(os.path.join(exp, "fixtures/c2"))):
    src = os.path.join(exp, "fixtures/c2", fx)
    if not os.path.isfile(os.path.join(src, "args.json")): continue
    d = os.path.join(stage, fx); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    os.makedirs(os.path.join(d, "tree"), exist_ok=True)
    if os.path.isdir(os.path.join(src, "tree")): shutil.copytree(os.path.join(src, "tree"), os.path.join(d, "tree"), symlinks=True, dirs_exist_ok=True)
    args = [a.replace("{FX}", "/work") for a in json.load(open(os.path.join(src, "args.json")))]
    cmd = ["bwrap", "--unshare-all", "--die-with-parent", "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib",
           "--symlink", "usr/lib64", "/lib64", "--symlink", "usr/bin", "/bin", "--proc", "/proc", "--dev", "/dev",
           "--ro-bind", d, "/work", "--chdir", "/work", "--setenv", "LC_ALL", "C", "--clearenv", "--setenv", "PATH", "/usr/bin:/bin",
           "--setenv", "LC_ALL", "C", "--ro-bind", tool, "/tool.py", "python3", "-I", "/tool.py", *args]
    p = subprocess.run(cmd, capture_output=True)
    want = open(os.path.join(src, "expected.out"), "rb").read(); rc = int(open(os.path.join(src, "expected.rc")).read())
    res[1] += 1; res[0] += (p.stdout == want and p.returncode == rc)
print("sandboxed", tool.split("/")[-1], f"{res[0]}/{res[1]}")
