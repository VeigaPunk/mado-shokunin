#!/usr/bin/env python3
"""Round-92 C1 forgery control: a tool holding the frozen labels, keyed by the fixture's bytes; None otherwise.

  gen-forgery-table-r92.py CASES OUT_TOOL
The key is sha256 over the sorted (relpath, content-sha256 | 'dir' | 'link:'+target with the root as {ROOT})
records plus the asked types and the environment with the root as {ROOT}.  A frozen case is answered from the
table; anything else (every fresh case) gets None/0.
"""
import base64, hashlib, json, sys

def key_of(records, types, env):
    return hashlib.sha256(json.dumps([sorted(records), types, sorted(env.items())]).encode()).hexdigest()

cases = json.load(open(sys.argv[1]))["cases"]
table = {}
for c in cases:
    recs = []
    for rel, spec in c["files"].items():
        if spec.get("dir"):
            recs.append([rel, "dir"])
        elif "symlink" in spec:
            recs.append([rel, "link:" + spec["symlink"]])
        else:
            data = base64.b64decode(spec["b64"]) if "b64" in spec else spec["text"].encode("utf-8", "surrogateescape")
            recs.append([rel, hashlib.sha256(data).hexdigest()])
    table[key_of(recs, c["types"], c["env"])] = c["expect"]
src = '''#!/usr/bin/env python3
import argparse, hashlib, json, os
TABLE = json.loads(%r)
ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true"); ap.add_argument("--cwd")
ap.add_argument("--env", action="append", default=[]); ap.add_argument("types", nargs="+")
a = ap.parse_args()
root = a.cwd
recs, parents = [], set()
for d, ds, fs in os.walk(root):
    for n in ds + fs:
        p = os.path.join(d, n); rel = os.path.relpath(p, root)
        parents.add(os.path.dirname(rel))
        if os.path.islink(p):
            recs.append([rel, "link:" + os.readlink(p).replace(root, "{ROOT}")])
        elif os.path.isdir(p):
            recs.append([rel, "dir"])
        else:
            recs.append([rel, hashlib.sha256(open(p, "rb").read()).hexdigest()])
recs = [r for r in recs if not (r[1] == "dir" and r[0] in parents)]
env = {k: v.replace(root, "{ROOT}") for k, v in (kv.split("=", 1) for kv in a.env)}
key = hashlib.sha256(json.dumps([sorted(recs), a.types, sorted(env.items())]).encode()).hexdigest()
lab = TABLE.get(key, {})
print(json.dumps({"results": [{"type": t, "default": lab.get(t, {}).get("default"), "rc": lab.get(t, {}).get("rc", 0)} for t in a.types]}))
''' % json.dumps(table)
open(sys.argv[2], "w").write(src)
print(f"table of {len(table)} cases")
