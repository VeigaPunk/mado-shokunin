#!/usr/bin/env python3
"""R91MResidC1 sandbox probe: runs as a scored tool would (same argv shape, env, cwd)."""
import glob, json, os, shutil, subprocess, sys

out = {}
out["argv_head"] = sys.argv[1:5]
out["cwd"] = os.getcwd()
out["env"] = {k: os.environ.get(k) for k in ("HOME", "PATH", "LC_ALL", "XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_DATA_DIRS")}
try:
    out["cwd_listdir"] = sorted(os.listdir("."))[:12]
except OSError as e:
    out["cwd_listdir"] = f"ERR {e}"
work = os.path.dirname(os.getcwd())
try:
    out["work_listdir"] = sorted(os.listdir(work))[:12]
except OSError as e:
    out["work_listdir"] = f"ERR {e}"
scratch = os.path.dirname(work)
try:
    out["scratch_root_listdir"] = sorted(os.listdir(scratch))[:12]
except OSError as e:
    out["scratch_root_listdir"] = f"ERR {e}"
lane = "/home/vgpnk/Projects/shokunin/mado-shokunin"
try:
    out["lane_listdir"] = sorted(os.listdir(lane))[:12]
except OSError as e:
    out["lane_listdir"] = f"ERR {e}"
try:
    b = open(lane + "/.ufo/waves/round-91/controls/mime-cases-r91.json", "rb").read(16)
    out["lane_labels_read"] = f"OK head={b.hex()}"
except OSError as e:
    out["lane_labels_read"] = f"ERR {e}"
for pth in ("/usr/bin/gio", "/usr/lib/libgio-2.0.so.0"):
    try:
        b = open(pth, "rb").read()
        out["read:" + pth] = f"len={len(b)} head={b[:8].hex()}"
    except OSError as e:
        out["read:" + pth] = f"ERR {e}"
out["libgio_glob"] = {d: glob.glob(d + "/libgio-2.0.so*") for d in ("/usr/lib", "/usr/lib32", "/usr/lib64")}
try:
    r = subprocess.run(["/usr/bin/gio", "mime", "text/plain"], capture_output=True, text=True)
    out["subprocess_gio_mime"] = {"rc": r.returncode, "stdout": r.stdout.strip()[:80], "stderr": r.stderr.strip()[:120]}
except OSError as e:
    out["subprocess_gio_mime"] = f"EXEC-ERROR {type(e).__name__}: {e}"
out["which_gio"] = shutil.which("gio")
print(json.dumps(out, indent=1))
