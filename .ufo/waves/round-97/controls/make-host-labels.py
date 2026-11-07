#!/usr/bin/env python3
"""Build the frozen host-label file for the round-97 C1 counter (L1 freeze step).

Usage: make-host-labels.py --list PATH --out PATH [--limit N]

Reads the host list (one absolute path per line; '#' comments; trailing TAB reason is
ignored), keeps only STABLE system trees (/usr /etc /dev /proc /sys) and drops
credential-shaped paths (lane r56), then labels every surviving path with
`env -i LC_ALL=C /usr/bin/gio info -a standard::content-type PATH`. A path with no
attribute and a nonzero exit is labelled "ERROR". Output: one JSON object per line,
sorted by path, `{"path": "...", "label": "..."}`, plus a final
`{"summary": {...}}` line with counts and the sha256 of the label lines.
"""
import argparse, hashlib, json, os, subprocess, sys

KEEP = ("/usr/", "/etc/", "/dev/", "/proc/", "/sys/")
CRED = (".ssh", ".gnupg", "agent.db", "credential", "keyring", "token", "secret",
        ".netrc", "hosts.yml", "shadow", "passwd", "id_rsa")
CRED_EXT = (".pem", ".key", ".p12", ".pfx", ".kdbx")

def kept(path):
    if not path.startswith("/"):
        return False
    if not any(path.startswith(p) for p in KEEP):
        return False
    base = path.rsplit("/", 1)[-1]
    if base.endswith(CRED_EXT):
        return False
    low = path.lower()
    if any(t in low for t in CRED):
        return False
    if path.startswith("/proc/") and path.count("/") > 2 and path.split("/")[2].isdigit():
        return False
    return True

def label(path):
    env = {"LC_ALL": "C", "PATH": "/usr/bin:/bin"}
    try:
        r = subprocess.run(["/usr/bin/gio", "info", "-a", "standard::content-type", path],
                           env=env, capture_output=True, text=True, timeout=20)
    except Exception:
        return "ERROR"
    for line in r.stdout.splitlines():
        if "content-type: " in line:
            return line.split(": ", 1)[1].strip()
    return "ERROR"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    paths = []
    for line in open(a.list, encoding="utf-8", errors="replace"):
        s = line.rstrip("\n")
        if not s or s.lstrip().startswith("#"):
            continue
        p = s.split("\t")[0]
        if kept(p):
            paths.append(p)
    paths = sorted(set(paths))
    if a.limit:
        paths = paths[:a.limit]
    rows = []
    for p in paths:
        rows.append({"path": p, "label": label(p)})
    body = "".join(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n" for r in rows)
    sha = hashlib.sha256(body.encode()).hexdigest()
    errs = sum(1 for r in rows if r["label"] == "ERROR")
    summary = {"paths": len(rows), "errors": errs, "labels_sha256": sha}
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(body)
        f.write(json.dumps({"summary": summary}, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps(summary, indent=1))
    return 0

if __name__ == "__main__":
    sys.exit(main())
