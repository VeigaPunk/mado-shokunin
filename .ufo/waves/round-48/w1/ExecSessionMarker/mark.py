#!/usr/bin/env python3
"""mark.py — write one synthetic marker pair into a scratch clone.

Demo helper, never installed. Writes the sidecar ``<path>.synthetic`` with the
blob sha of ``HEAD:<path>`` and appends the matching row to
``quality/session-material-waivers.txt``. It does not decide anything: the
gate decides, and it will refuse the marker unless the content really is
synthetic.

Usage::

    mark.py --repo <clone> --path <.ufo/waves/...> --kind fixture|gate-copy \
            --rules R3_MONITOR_IDENT[,R1_CLIENT_DUMP]
"""

import argparse
import hashlib
import os
import subprocess
import sys

REGISTRY_REL = "quality/session-material-waivers.txt"
MARKER_FMT = "SYNTHETIC-MATERIAL v1 kind=%s rules=%s sha256=%s\n"


def git_bytes(repo, *args):
    proc = subprocess.run(["git", "-C", repo, *args], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args),
                                                proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout


def git_text(repo, *args):
    proc = subprocess.run(["git", "-C", repo, *args], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args),
                                                proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout.decode("utf-8", "replace").strip()


def main(argv=None):
    parser = argparse.ArgumentParser(prog="mark.py")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--kind", choices=("fixture", "gate-copy"), default="fixture")
    parser.add_argument("--rules", required=True)
    args = parser.parse_args(argv)

    repo = os.path.abspath(args.repo)
    blob = hashlib.sha256(git_bytes(repo, "show", "HEAD:%s" % args.path)).hexdigest()
    sidecar = os.path.join(repo, args.path + ".synthetic")
    os.makedirs(os.path.dirname(sidecar), exist_ok=True)
    with open(sidecar, "w", encoding="utf-8") as handle:
        handle.write(MARKER_FMT % (args.kind, args.rules, blob))
    registry = os.path.join(repo, REGISTRY_REL)
    os.makedirs(os.path.dirname(registry), exist_ok=True)
    existing = ""
    if os.path.exists(registry):
        with open(registry, encoding="utf-8") as handle:
            existing = handle.read()
    if not existing:
        existing = "# path sha256 rules kind — see quality/check-session-material.py\n"
    with open(registry, "w", encoding="utf-8") as handle:
        handle.write(existing)
        handle.write("%s %s %s kind=%s\n" % (args.path, blob, args.rules, args.kind))
    print("marker: path=%s kind=%s rules=%s" % (args.path, args.kind, args.rules))
    return 0


if __name__ == "__main__":
    sys.exit(main())
