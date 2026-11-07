#!/usr/bin/env python3
"""magictext-probe-r96 — materialize round-96 C1 text-magic cases, label them with the
compiled GLib oracle, and verify labels.

  magictext-probe-r96.py --cases FILE --oracle BIN --scratch DIR [--out FILE]
                         [--check] [--filter ID-SUBSTR] [--stats]

Behaviour:
  * materializes each case root under SCRATCH (case env dirs dh/d1/d2 plus the always
    empty HOME dir h); "{root}" in env values and the leading component of file paths
    is the case root;
  * a case whose files hold a reachable */mime/mime.cache is a cache-mode refusal case:
    its labels are the contract sentinels ["UNSUPPORTED", null] (one per input) and the
    oracle is never run for it;
  * every other case is labelled by ONE oracle run over all its inputs:
    env -i LC_ALL=C HOME=<root>/h [XDG_DATA_HOME=<root>/dh] XDG_DATA_DIRS=<root>/d1:<root>/d2
    oracle <0|=NAME> <datafile> ...  ->  one "<type>\t<0|1>" line per input;
  * a case whose oracle run exits non-zero, times out, or prints a wrong-shaped/short
    output is FAILED (a candidate for dropping); with --check FAILED is an error;
  * --out writes the case file back with labels filled in (deterministic order);
    without --out nothing is written;
  * --check compares the file's existing labels against a fresh oracle run and exits 1
    on any mismatch, any refusal-label drift, or any FAILED case.

Deterministic: fixed iteration order, fixed scratch layout, no RNG.  Stdlib only.
ASCII only.  Read-only outside --scratch.
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys

ORACLE_TIMEOUT = 10.0
CACHE_RE = re.compile(r"(^|/)mime/mime\.cache$")


def cache_loadable(data):
    """Mirror xdgmimecache.c _xdg_mime_cache_new_from_file / tools/mado-mimeglob.py
    load_cache: a cache loads iff it is >= 40 bytes and its BE u16 version at offset
    0 is major 1 with minor 1 or 2.  A non-loadable cache file falls back to text
    mode in GLib and must NOT be labelled a refusal."""
    if len(data) < 40:
        return False
    major = int.from_bytes(data[0:2], "big")
    minor = int.from_bytes(data[2:4], "big")
    return major == 1 and minor in (1, 2)


def unb64(s):
    return base64.b64decode(s.encode("ascii"))


def b64(b):
    return base64.b64encode(b).decode("ascii")


def case_env(case, root):
    env = {"LC_ALL": "C", "HOME": os.path.join(root, "h")}
    ce = case["env"]
    if ce.get("XDG_DATA_HOME") is not None:
        env["XDG_DATA_HOME"] = ce["XDG_DATA_HOME"].replace("{root}", root)
    env["XDG_DATA_DIRS"] = ce["XDG_DATA_DIRS"].replace("{root}", root)
    return env


def materialize(case, root):
    os.makedirs(os.path.join(root, "h"), exist_ok=True)
    inbox = os.path.join(root, ".inputs")
    os.makedirs(inbox, exist_ok=True)
    for rel, data_b64 in sorted(case["files"].items()):
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(unb64(data_b64))
    pairs = []
    for i, inp in enumerate(case["inputs"]):
        fp = os.path.join(inbox, "d%03d" % i)
        with open(fp, "wb") as fh:
            fh.write(unb64(inp["data_b64"]))
        name = None if inp["name_b64"] is None else unb64(inp["name_b64"])
        pairs.append((name, fp))
    return pairs


def run_oracle(oracle, env, pairs, timeout):
    """One oracle invocation for all pairs; returns [(type, uncertain)] or raises ProbeError."""
    args = [oracle]
    for name, fp in pairs:
        args.append("0" if name is None else b"=" + name)
        args.append(fp)
    try:
        r = subprocess.run(args, env=env, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise ProbeError("oracle timeout")
    if r.returncode != 0:
        raise ProbeError("oracle rc=%d stderr=%r" % (r.returncode, r.stderr[:200]))
    lines = r.stdout.split(b"\n")
    if lines and lines[-1] == b"":
        lines.pop()
    if len(lines) != len(pairs):
        raise ProbeError("oracle printed %d lines for %d inputs" % (len(lines), len(pairs)))
    out = []
    for ln in lines:
        if b"\t" not in ln:
            raise ProbeError("oracle line %r has no tab" % ln[:80])
        t, u = ln.rsplit(b"\t", 1)
        if u not in (b"0", b"1"):
            raise ProbeError("oracle line %r bad flag" % ln[:80])
        out.append((t.decode("utf-8", "surrogateescape"), int(u)))
    return out


class ProbeError(Exception):
    pass


def label_case(case, oracle, root, timeout=ORACLE_TIMEOUT):
    """Returns (labels, error).  Labels are contract sentinels for cache-refusal cases."""
    if any(CACHE_RE.search(rel) and cache_loadable(unb64(data))
           for rel, data in case["files"].items()):
        return [["UNSUPPORTED", None]] * len(case["inputs"]), None
    pairs = materialize(case, root)
    env = case_env(case, root)
    try:
        answers = run_oracle(oracle, env, pairs, timeout)
    except ProbeError as e:
        return None, str(e)
    return [[t, u] for t, u in answers], None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--cases", required=True)
    ap.add_argument("--oracle", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", help="write the labelled case file here")
    ap.add_argument("--check", action="store_true",
                    help="verify existing labels against a fresh oracle run")
    ap.add_argument("--filter", help="only process cases whose id contains this substring")
    ap.add_argument("--stats", action="store_true", help="print the per-class census")
    a = ap.parse_args()

    with open(a.cases, "rb") as fh:
        doc = json.loads(fh.read().decode("ascii"))
    os.makedirs(a.scratch, exist_ok=True)

    labeled = failed = refused = checked = mismatched = 0
    census = {}
    failures = []
    for idx, case in enumerate(doc["cases"]):
        if a.filter and a.filter not in case["id"]:
            continue
        cls = case["class"]
        census[cls] = census.get(cls, 0) + 1
        root = os.path.join(a.scratch, "case-%04d-%s" % (idx, case["id"]))
        labels, err = label_case(case, a.oracle, root)
        if err is not None:
            failed += 1
            failures.append((case["id"], err))
            if a.check:
                print("PROBE_FAIL %s: %s" % (case["id"], err))
            continue
        if case["inputs"] and labels == [["UNSUPPORTED", None]] * len(case["inputs"]):
            refused += 1
        else:
            labeled += 1
        if a.check:
            checked += 1
            old = case.get("labels")
            if old != labels:
                mismatched += 1
                print("PROBE_MISMATCH %s:\n  file:    %r\n  current: %r" % (case["id"], old, labels))
        else:
            case["labels"] = labels
        if a.filter:
            print("%s %s %r" % (case["id"], cls, labels))

    if a.stats or not a.check:
        total_in = sum(len(c["inputs"]) for c in doc["cases"]
                       if not a.filter or a.filter in c["id"])
        print("PROBE cases=%d labelled=%d refused=%d failed=%d inputs=%d"
              % (len(doc["cases"]) if not a.filter else checked + failed,
                 labeled, refused, failed, total_in))
        print("PROBE_CENSUS " + " ".join("%s=%d" % (k, v) for k, v in sorted(census.items())))
        for cid, err in failures:
            print("PROBE_DROP %s: %s" % (cid, err))

    if a.out:
        with open(a.out, "wb") as fh:
            fh.write(json.dumps(doc, indent=1, sort_keys=False).encode("ascii"))
            fh.write(b"\n")
        print("PROBE_WROTE %s" % a.out)
    if a.check:
        if mismatched or failed:
            print("PROBE_CHECK mismatches=%d failed=%d" % (mismatched, failed))
            return 1
        print("PROBE_CHECK ok cases=%d" % checked)
    return 0


if __name__ == "__main__":
    sys.exit(main())
