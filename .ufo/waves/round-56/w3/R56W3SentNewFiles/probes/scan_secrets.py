#!/usr/bin/env python3
"""Secret-shape scan for seat R56W3SentNewFiles.

Three fixed lane patterns (tools/mado-tripwire.py SECRET_PATTERNS at 0f3a5436) plus a
generic set (op://, AKIA, BEGIN PRIVATE KEY, long hex token in value position).

Output: per-pattern counts and per-file hit lists; a hit is reported as
file:line:col:pattern:<redacted-shape>.  The matched VALUE is never printed.
"""
import os
import re
import sys

FIXED = {
    "F1_url_userpass": re.compile(r"(?<=://)[^/\s:@]+:[^/\s@]+(?=@)"),
    "F2_aws_akia": re.compile(r"AKIA[0-9A-Z]{16}"),
    "F3_long_token_32": re.compile(r"[A-Za-z0-9_\-]{32,}"),
}
GENERIC = {
    "G1_op_uri": re.compile(r"op://[^\s\"'`>)\]]*"),
    "G2_akia_any": re.compile(r"\bAKIA[0-9A-Z]{8,}\b"),
    "G3_private_key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "G4_hex_value": re.compile(
        r"(?:=|:|=>|value|token|secret|key|password|passwd|pwd)"
        r"\s*[\"']?[0-9a-fA-F]{32,}[\"']?"),
    "G5_gh_pat": re.compile(r"\bgh[pousr]_[0-9A-Za-z]{20,}\b"),
    "G6_slack": re.compile(r"\bxox[abposr]-[0-9A-Za-z-]{10,}\b"),
    "G7_jwt": re.compile(r"\beyJ[0-9A-Za-z_-]{8,}\.[0-9A-Za-z_-]{8,}\.[0-9A-Za-z_-]{4,}\b"),
    "G8_pem_body": re.compile(r"-----BEGIN CERTIFICATE-----"),
}
ALL = dict(FIXED)
ALL.update(GENERIC)


def scan_file(path):
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError as exc:
        return [("<unreadable>", 0, 0, str(exc))]
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("utf-8", "replace")
    hits = []
    for lineno, line in enumerate(text.split("\n"), 1):
        for name, pat in ALL.items():
            for m in pat.finditer(line):
                hits.append((name, lineno, m.start(), m.group(0)))
    return hits


def main(argv):
    roots = argv[1:]
    files = []
    for root in roots:
        if os.path.isfile(root):
            files.append(root)
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames if d != ".git")
            for name in sorted(filenames):
                files.append(os.path.join(dirpath, name))
    files = sorted(set(files))
    totals = {}
    per_file = {}
    for path in files:
        hits = scan_file(path)
        if hits:
            per_file[path] = hits
            for name, _l, _c, _v in hits:
                totals[name] = totals.get(name, 0) + 1
    print("SCAN: files=%d files_with_hits=%d" % (len(files), len(per_file)))
    print("TOTALS: " + (" ".join("%s=%d" % (k, totals[k]) for k in sorted(totals)) or "(none)"))
    for path in sorted(per_file):
        rel = path
        print("FILE %s" % rel)
        for name, lineno, col, val in per_file[path]:
            shape = ("len=%d" % len(val)) if len(val) > 12 else val
            print("  HIT %s line=%d col=%d shape=%s" % (name, lineno, col, shape))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
