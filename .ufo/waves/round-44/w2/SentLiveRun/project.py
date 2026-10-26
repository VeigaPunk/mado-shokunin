#!/usr/bin/env python3
"""project.py RAW — shape-only projection of a live `hyprctl clients -j` dump.

Keeps the ten fields the round-44 tool contract reads (round-43 precedent
`fetch/host-clients-r43.json` plus the three state fields C1 is about) and nothing else:
no title, pid, stableId, workspace, xwayland or tag. The raw bytes are NOT retained; only
their sha256 and byte count are recorded. Then it proves the projection is loss-free for
the tool by running the tool on the raw dump and on the projection and comparing stdout,
stderr and exit.

usage: python3 project.py RAW.json --tool TOOL --rules RULES [--out DIR]
"""
import argparse, hashlib, json, os, subprocess, sys

KEEP = ("address", "mapped", "class", "floating", "size", "at", "monitor",
        "fullscreen", "fullscreenClient", "fullscreenHandler")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("--tool", required=True)
    ap.add_argument("--rules", required=True)
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    a = ap.parse_args()
    raw = open(a.raw, "rb").read()
    doc = json.loads(raw)
    proj = [{k: c[k] for k in KEEP if k in c} for c in doc]
    out = os.path.join(a.out, "live-clients-projected.json")
    body = json.dumps(proj, indent=1) + "\n"
    open(out, "w").write(body)
    raw_sha = hashlib.sha256(raw).hexdigest()
    proj_sha = hashlib.sha256(body.encode()).hexdigest()
    fields = sorted({k for c in doc for k in c})
    extra = [k for k in fields if k not in KEEP]
    open(os.path.join(a.out, "raw-dumps.sha256"), "w").write(
        "clients raw_sha256=%s raw_bytes=%d raw_keys=%s kept=%s items=%d -> live-clients-projected.json "
        "sha256=%s\n(raw bytes not retained; %d dropped keys: %s)\n"
        % (raw_sha, len(raw), fields, ",".join(KEEP), len(proj), proj_sha, len(extra), ",".join(extra)))
    runs = []
    for label, path in (("raw", a.raw), ("projected", out)):
        p = subprocess.run([sys.executable, "-I", a.tool, "--clients", path, "--rules", a.rules],
                           capture_output=True, timeout=60)
        runs.append((label, p.returncode, p.stdout, p.stderr))
    same = runs[0][1:] == runs[1][1:]
    rep = ["projection invariance: raw vs projected through %s" % a.tool,
           "  raw       rc=%d stdout_sha=%s stderr_bytes=%d"
           % (runs[0][1], hashlib.sha256(runs[0][2]).hexdigest(), len(runs[0][3])),
           "  projected rc=%d stdout_sha=%s stderr_bytes=%d"
           % (runs[1][1], hashlib.sha256(runs[1][2]).hexdigest(), len(runs[1][3])),
           "  VERDICT: %s" % ("BYTE-IDENTICAL (loss is outside what the tool reads)" if same else "MISMATCH"),
           "", "tool stdout on the projection:", runs[1][2].decode().rstrip()]
    open(os.path.join(a.out, "projection-invariance.txt"), "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))
    return 0 if same else 1


if __name__ == "__main__":
    sys.exit(main())
