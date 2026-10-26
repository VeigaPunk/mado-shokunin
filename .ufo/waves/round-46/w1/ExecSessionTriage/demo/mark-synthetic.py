#!/usr/bin/env python3
"""Write synthetic-material markers and the waiver registry into a scratch clone.

Reads the triage table (path, rule, count, class, basis) and, for every
(SEAT-marked) SYNTHETIC finding, writes the sidecar ``<path>.synthetic`` and one
line of ``quality/session-material-waivers.txt``, then commits both in the
clone. The registry lives outside ``.ufo/`` on purpose: a wave cannot issue its
own waiver.

Usage:
  mark-synthetic.py <clone> --tsv <triage.tsv> [--prefix <p>]... [--message M]
"""

import argparse
import hashlib
import os
import subprocess
import sys

MARKER = ("SYNTHETIC-MATERIAL v1 kind=%s rules=%s sha256=%s\n")


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", repo, *args], check=True, capture_output=True
    ).stdout


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("clone")
    ap.add_argument("--tsv", required=True)
    ap.add_argument("--prefix", action="append", default=[])
    ap.add_argument("--also", action="append", default=[],
                    help="extra <path>:<rule> to mark even though the triage "
                         "table does not list it")
    ap.add_argument("--registry", default="quality/session-material-waivers.txt")
    ap.add_argument("--gate-source", default="quality/check-session-material.py")
    ap.add_argument("--message", default="demo: synthetic-material markers")
    args = ap.parse_args(argv)

    clone = os.path.realpath(args.clone)
    top = git(clone, "rev-parse", "--show-toplevel").decode().strip()
    if os.path.realpath(top) != clone:
        sys.exit("toplevel %r != %r" % (top, clone))

    wanted = {}
    with open(args.tsv, encoding="utf-8") as handle:
        header = handle.readline().rstrip("\n").split("\t")
        if header != ["path", "rule", "count", "class", "basis"]:
            sys.exit("unexpected tsv header: %r" % (header,))
        for line in handle:
            path, rule, _count, cls, _basis = line.rstrip("\n").split("\t")
            if cls != "SYNTHETIC":
                continue
            if args.prefix and not any(path.startswith(p) for p in args.prefix):
                continue
            wanted.setdefault(path, []).append(rule)

    for spec in args.also:
        path, _sep, rule = spec.partition(":")
        if not path or not rule:
            sys.exit("bad --also value: %r" % (spec,))
        wanted.setdefault(path, []).append(rule)

    gate_path = os.path.join(clone, args.gate_source)
    gate_sha = None
    if os.path.exists(gate_path):
        with open(gate_path, "rb") as handle:
            gate_sha = hashlib.sha256(handle.read()).hexdigest()

    rows = []
    counts = {"gate-copy": 0, "fixture": 0}
    rules_total = 0
    for path in sorted(wanted):
        full = os.path.join(clone, path)
        with open(full, "rb") as handle:
            data = handle.read()
        digest = hashlib.sha256(data).hexdigest()
        rules = sorted(set(wanted[path]))
        kind = "gate-copy" if digest == gate_sha else "fixture"
        counts[kind] += 1
        rules_total += len(rules)
        with open(full + ".synthetic", "w", encoding="utf-8") as handle:
            handle.write(MARKER % (kind, ",".join(rules), digest))
        rows.append("%s %s %s kind=%s\n" % (path, digest, ",".join(rules), kind))

    registry = os.path.join(clone, args.registry)
    os.makedirs(os.path.dirname(registry), exist_ok=True)
    with open(registry, "w", encoding="utf-8") as handle:
        handle.write("# path sha256 rules kind — see quality/check-session-material.py\n")
        handle.writelines(rows)

    git(clone, "add", "-A")
    git(clone, "-c", "user.name=seat", "-c", "user.email=seat@scratch.invalid",
        "commit", "-q", "-m", args.message)
    print("MARKED files=%d findings=%d gate-copy=%d fixture=%d rev=%s"
          % (len(wanted), rules_total, counts["gate-copy"], counts["fixture"],
             git(clone, "rev-parse", "HEAD").decode().strip()))


if __name__ == "__main__":
    main()
