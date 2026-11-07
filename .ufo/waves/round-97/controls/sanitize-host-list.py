#!/usr/bin/env python3
"""Filter credential-shaped paths out of the round-97 C1 host list (L1 safety step).

Usage: sanitize-host-list.py IN OUT [--report FILE]

The host census must never hand a sniffing tool a credential-shaped path (lane r56
credential-material rule). A line is dropped when its first field (the path) has any
component matching CRED_RE, or sits under any DENY_PREFIX. Prints the counts; writes
OUT with the surviving lines byte-identical, comments kept.
"""
import argparse, re, sys

CRED_RE = re.compile(
    r"(^|[./_-])(\.ssh|\.gnupg|agent\.db|credentials?|keyring|tokens?|secrets?|\.netrc|hosts\.yml|auth|shadow|passwd|id_rsa|id_ed25519)([./_-]|$)",
    re.I)
EXT_RE = re.compile(r"\.(pem|key|p12|pfx|kdbx)$", re.I)
DENY_PREFIX = (
    "/home/vgpnk/.config/gh/", "/home/vgpnk/.config/anthropic/", "/home/vgpnk/.config/elevenlabs/",
    "/home/vgpnk/.config/omp/", "/home/vgpnk/.config/sops/", "/home/vgpnk/.local/share/keyrings/",
    "/home/vgpnk/.aws/", "/home/vgpnk/.docker/", "/home/vgpnk/.mozilla/", "/home/vgpnk/.thunderbird/",
    "/home/vgpnk/.password-store/", "/home/vgpnk/.cache/omp/",
)

def path_of(line):
    s = line.rstrip("\n")
    if not s or s.lstrip().startswith("#"):
        return None
    return s.split("\t")[0]

def denied(path):
    if not path.startswith("/"):
        return True
    if any(path == p.rstrip("/") or path.startswith(p) for p in DENY_PREFIX):
        return True
    base = path.rsplit("/", 1)[-1]
    if EXT_RE.search(base):
        return True
    return bool(CRED_RE.search(path))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp")
    ap.add_argument("out")
    ap.add_argument("--report")
    a = ap.parse_args()
    kept, dropped, comments = [], [], 0
    for line in open(a.inp, encoding="utf-8", errors="replace"):
        p = path_of(line)
        if p is None:
            comments += 1
            kept.append(line)
        elif denied(p):
            dropped.append(p)
        else:
            kept.append(line)
    open(a.out, "w", encoding="utf-8").write("".join(kept))
    msg = ["SANITIZE: kept_paths=%d dropped_paths=%d comments=%d" % (len(kept) - comments, len(dropped), comments)]
    msg += ["DROP %s" % p for p in dropped]
    text = "\n".join(msg) + "\n"
    sys.stdout.write(text)
    if a.report:
        open(a.report, "w", encoding="utf-8").write(text)
    return 0

if __name__ == "__main__":
    sys.exit(main())
