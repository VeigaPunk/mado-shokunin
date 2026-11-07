import json, base64, os, shutil, subprocess, hashlib, struct, concurrent.futures as cf
S = "/fast/scratch/hyaku/mado-r95/R95MMutC1"
W = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-95/w1"
C1B = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-95/build/mado-mimesniff.c1b.py"
TOOLB = os.path.join(S, "tools-c1b", "mado-mimesniff.py")
MUT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-95/controls/mimesniff-mutants-r95.json"
src = open(C1B, encoding="utf-8").read()
m = json.load(open(MUT))

FIX = {
 "max_nest_zero": ("MAX_NEST = 512", "MAX_NEST = 0"),
 "lltext_lt7": ("b < 8 or", "b < 7 or"),
 "wrap_raise_removed": (
   '        if i + value_length > M32:\n'
   '            raise Unsupported("matchlet i + value_length wraps to <= len (memcmp past the data)")\n', ""),
 "len_check_ge": (
   '        if ((i + value_length) & M32) > len(data):\n            return False',
   '        if ((i + value_length) & M32) >= len(data):\n            return False'),
 "nest_raise_removed": (
   '        if len(stack) > MAX_NEST:\n'
   '            raise Unsupported("matchlet children nested past 512 (declared limit; the C recursion overflows deeper)")\n',
   ""),
}
def adjust(x):
    y = dict(x)
    if x["id"] in FIX:
        y["find"], y["replace"] = FIX[x["id"]]
    return y

# nest_ge becomes countable on c1b (MAX_NEST=512): a 513-deep chain answers on the
# correct tool and raises on the mutant; the oracle answers at 513 (measured app/deep 0).
counted, equiv = [], []
for x in m["mutants"] + m["equivalent_not_counted"]:
    y = adjust(x)
    if y["id"] == "nest_ge":
        y["argument"] = ("Countable on c1b: with MAX_NEST = 512 a chain of 513 matchlets reaches stack "
                         "depth 512 (not > 512) and answers, while the mutant raises; the oracle answers at "
                         "513 (measured app/deep 0), so case nest-04-513 kills it.")
        counted.append(y)
    elif y["id"] == "text_mode_removed":
        equiv.append(y)
    else:
        counted.append(y)
for x in counted + equiv:
    assert src.count(x["find"]) == 1, (x["id"], src.count(x["find"]))
out = {"mutants": counted, "equivalent_not_counted": equiv}
p = os.path.join(W, "R95MMutC1-mutants-c1b.json")
json.dump(out, open(p, "w"), indent=1)
print("wrote", p, "counted", len(counted), "equiv", len(equiv),
      "sha", hashlib.sha256(open(p, "rb").read()).hexdigest())

# --- cases: the 51 emitted cases + nest-04-513
cases = json.load(open(os.path.join(W, "R95MMutC1-cases.json")))
M32 = 0xFFFFFFFF
def u32(v): return struct.pack(">I", v & M32)
def deep_cache(n, mime=b"app/deep"):
    blob = bytearray(40)
    def align():
        while len(blob) % 4: blob.append(0)
    mo = len(blob); blob.extend(mime + b"\0"); align()
    lo = len(blob); blob.extend(u32(1) + u32(0) + u32(0))
    eo = len(blob); blob.extend(b"\0" * 16)
    mt = len(blob); blob.extend(b"\0" * (32 * n))
    for i in range(n):
        at = mt + 32 * i
        kids = 1 if i < n - 1 else 0
        co = mt + 32 * (i + 1) if i < n - 1 else 0
        blob[at:at+32] = u32(0)+u32(1)+u32(1)+u32(0)+u32(0)+u32(0)+u32(kids)+u32(co)
    blob[lo+8:lo+12] = u32(eo)
    blob[eo:eo+16] = u32(90) + u32(mo) + u32(1) + u32(mt)
    for k in (28, 32, 36): blob[k:k+4] = u32(0)
    blob[0:4] = struct.pack(">HH", 1, 2)
    blob[4:8] = u32(len(blob)); blob[8:12] = u32(0); blob[12:16] = u32(0)
    blob[16:20] = u32(0); blob[20:24] = u32(0); blob[24:28] = u32(lo)
    return bytes(blob)
blob = deep_cache(513)
cases["cases"].append({
    "id": "nest-04-513", "class": "nest",
    "env": {"HOME": "{root}/h", "XDG_DATA_HOME": "{root}/dh", "XDG_DATA_DIRS": "{root}/s1:{root}/s2"},
    "files": {"dh/mime/mime.cache": base64.b64encode(blob).decode()},
    "inputs": [{"name_b64": None, "data_b64": base64.b64encode(b"a" * 16).decode()}],
    "labels": [["app/deep", 0]],
})
cp = os.path.join(W, "R95MMutC1-cases-c1b.json")
json.dump(cases, open(cp, "w"), indent=1)
print("wrote", cp, "cases", len(cases["cases"]), "sha", hashlib.sha256(open(cp, "rb").read()).hexdigest())

# --- verify: oracle label of nest-04-513, c1b baseline, all counted mutants killed
root0 = os.path.join(S, "emitted_c1b"); shutil.rmtree(root0, ignore_errors=True)
def materialise(c):
    root = os.path.join(root0, c["id"]); os.makedirs(root)
    for rel, b64 in c["files"].items():
        q = os.path.join(root, rel); os.makedirs(os.path.dirname(q), exist_ok=True)
        open(q, "wb").write(base64.b64decode(b64))
    inp = c["inputs"][0]
    dp = os.path.join(root, "in", "0.bin"); os.makedirs(os.path.dirname(dp), exist_ok=True)
    open(dp, "wb").write(base64.b64decode(inp["data_b64"]))
    env = {"PATH": os.path.join(S, "emptybin"), "LC_ALL": "C"}
    for k, v in c["env"].items():
        if v is not None: env[k] = v.replace("{root}", root)
    return {"case": c, "dp": dp, "env": env, "inp": inp, "root": root}
prepared = [materialise(c) for c in cases["cases"]]

def run(tool, mm):
    args = ["/usr/bin/python3", "-I", tool, "--json"]
    if mm["inp"]["name_b64"] is not None:
        args += ["--name", base64.b64decode(mm["inp"]["name_b64"]).decode("utf-8", "surrogateescape")]
    args.append(mm["dp"])
    try:
        r = subprocess.run(args, env=mm["env"], capture_output=True, timeout=10)
    except subprocess.TimeoutExpired:
        return {"rc": "timeout"}
    o = {"rc": r.returncode}
    if r.returncode == 0:
        try:
            res = json.loads(r.stdout)["results"][0]
            o["type"], o["uncertain"] = res["type"], res["uncertain"]
        except Exception:
            o["parse_error"] = True
    return o

def ok(label, o):
    if label[0] == "UNSUPPORTED":
        return o.get("rc") == 3
    return o.get("rc") == 0 and o.get("type") == label[0] and o.get("uncertain") == label[1]

# oracle label of the new case
mm = prepared[-1]
e = dict(mm["env"]); e.pop("PATH", None)
r = subprocess.run([os.path.join(S, "oracle"), b"0", mm["dp"]], env=e, capture_output=True, timeout=10)
print("nest-04-513 oracle:", r.returncode, r.stdout)

bad = [mm["case"]["id"] for mm in prepared if not ok(mm["case"]["labels"][0], run(TOOLB, mm))]
print(f"c1b baseline on the {len(prepared)} cases: {len(prepared)-len(bad)}/{len(prepared)}; bad={bad}")

survivors = []
for x in counted:
    d = os.path.join(S, "mutb", x["id"]); os.makedirs(d, exist_ok=True)
    tp = os.path.join(d, "mado-mimesniff.py")
    open(tp, "w").write(src.replace(x["find"], x["replace"], 1))
    shutil.copyfile(os.path.join(S, "tools", "mado-mimeglob.py"), os.path.join(d, "mado-mimeglob.py"))
    killed = False
    with cf.ThreadPoolExecutor(8) as ex:
        for mm, o in zip(prepared, ex.map(lambda mm: run(tp, mm), prepared)):
            if not ok(mm["case"]["labels"][0], o):
                killed = True; break
    if not killed:
        survivors.append(x["id"])
print(f"c1b counted mutants killed: {len(counted)-len(survivors)}/{len(counted)}; survivors: {survivors}")
