import json, base64, os, shutil, subprocess, sys
S = "/fast/scratch/hyaku/mado-r95/R95MMutC1"
tool = sys.argv[2] if len(sys.argv) > 2 else os.path.join(S, "tools", "mado-mimesniff.py")
j = json.load(open(sys.argv[1]))
root0 = os.path.join(S, "check"); 
if os.path.isdir(root0): shutil.rmtree(root0)
bad = 0
for c in j["cases"]:
    root = os.path.join(root0, c["id"]); os.makedirs(root)
    for rel, b64 in c["files"].items():
        p = os.path.join(root, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "wb").write(base64.b64decode(b64))
    inp = c["inputs"][0]
    dp = os.path.join(root, "in", "0.bin"); os.makedirs(os.path.dirname(dp), exist_ok=True)
    open(dp, "wb").write(base64.b64decode(inp["data_b64"]))
    env = {"PATH": os.path.join(S, "emptybin"), "LC_ALL": "C"}
    for k, v in c["env"].items():
        if v is not None: env[k] = v.replace("{root}", root)
    args = ["/usr/bin/python3", "-I", tool, "--json"]
    if inp["name_b64"] is not None:
        args += ["--name", base64.b64decode(inp["name_b64"]).decode("utf-8", "surrogateescape")]
    args.append(dp)
    try:
        r = subprocess.run(args, env=env, capture_output=True, timeout=10)
    except subprocess.TimeoutExpired:
        print("TIMEOUT", c["id"]); bad += 1; continue
    lab = c["labels"][0]
    if lab[0] == "UNSUPPORTED":
        ok = r.returncode == 3
    else:
        ok = r.returncode == 0
        if ok:
            res = json.loads(r.stdout)["results"][0]
            ok = (res["type"], res["uncertain"]) == (lab[0], lab[1])
            got = (res["type"], res["uncertain"])
    if not ok:
        bad += 1
        print(f"FAIL {c['id']}: label={lab} rc={r.returncode} got={locals().get('got')}")
    got = None
print(f"{os.path.basename(sys.argv[1])}: {len(j['cases']) - bad}/{len(j['cases'])} ok")
