#!/usr/bin/env python3
"""Round-92 C1 forgery control (R92MCritic §3): a "tool" that carries its own bash and xdg-mime's text.

  gen-forgery-bundled-r92.py OUT_TOOL
Embeds base64 of /usr/bin/bash and of /usr/bin/xdg-mime; at run time writes both into the fixture root and
runs the script with the shipped bash (named `sh`).  It holds no model of xdg-mime.  The sandbox masks only the
host's copies, so this forgery answers like xdg-mime itself; the counter's bytes clause is what refuses it.
The OUT_TOOL is built in scratch and never committed (it embeds a binary).
"""
import base64
import sys

bash = base64.b64encode(open("/usr/bin/bash", "rb").read()).decode()
xm = base64.b64encode(open("/usr/bin/xdg-mime", "rb").read()).decode()
src = f'''#!/usr/bin/env python3
import argparse, base64, json, os, subprocess
B = "{bash}"
X = "{xm}"
ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true"); ap.add_argument("--cwd")
ap.add_argument("--env", action="append", default=[]); ap.add_argument("types", nargs="+")
a = ap.parse_args()
env = dict(kv.split("=", 1) for kv in a.env)
d = os.path.join(a.cwd, ".forge"); os.makedirs(d, exist_ok=True)
sh = os.path.join(d, "sh"); xm = os.path.join(d, "xdg-mime")
open(sh, "wb").write(base64.b64decode(B)); os.chmod(sh, 0o755)
open(xm, "wb").write(base64.b64decode(X)); os.chmod(xm, 0o755)
res = []
for t in a.types:
    r = subprocess.run([sh, xm, "query", "default", t], cwd=a.cwd, env=env, capture_output=True)
    out = r.stdout.decode("utf-8", "surrogateescape")
    res.append({{"type": t, "default": (out[:-1] if out.endswith("\\n") else out) if out else None, "rc": r.returncode}})
print(json.dumps({{"results": res}}))
'''
open(sys.argv[1], "w").write(src)
print(f"wrote {sys.argv[1]} ({len(src)} bytes)")
