#!/usr/bin/env python3
"""Verify the Gate lines of a lesson draft against the committed receipts.

Reads one lesson file, parses its `## Gate` section with the counter's own
GATE_RE, and for every GATE line checks: the receipt is committed at REV under
.ufo/waves/round-41/fetch/, its sha256 equals the bytes, it is >= 512 bytes, the
quote is 3-25 words, present in the receipt's normalized text (norm(): tags,
scripts and styles stripped, entities decoded, whitespace collapsed), and
path/sha256/quote are distinct across ids. Read-only: git show only.

Usage: python3 quotes.py --repo <lane> --rev <rev> --lesson <file>
Exit 0 iff every line verifies.
"""
import argparse
import hashlib
import importlib.util
import os
import re
import subprocess
import sys

FETCH = ".ufo/waves/round-41/fetch/"


def load_counter(repo):
    path = os.path.join(repo, "quality/counters/c2-r41-focus-entry.py")
    spec = importlib.util.spec_from_file_location("c2counter", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--lesson", required=True)
    a = ap.parse_args()
    repo = os.path.abspath(a.repo)
    c2 = load_counter(repo)
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    text = open(a.lesson, encoding="utf-8").read()
    gates = []
    for line in c2.section(text, "## Gate"):
        m = c2.GATE_RE.match(line.rstrip("\n"))
        if m:
            gates.append(m.groups())
        if re.match(r"^\s+GATE S\d", line):
            print("FAIL indented gate line: %r" % line)
            return 1
    if not gates:
        print("FAIL no gate line")
        return 1
    seen_p, seen_s, seen_q, bad = set(), set(), set(), 0
    for sid, path, digest, quote in gates:
        p = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (a.rev, path)],
                           capture_output=True, env=env)
        blob = p.stdout if p.returncode == 0 else None
        ok = (blob is not None and path.startswith(FETCH)
              and len(blob) >= c2.MIN_RECEIPT
              and hashlib.sha256(blob).hexdigest() == digest
              and 3 <= len(quote.split()) <= 25
              and c2.norm(quote) in c2.norm(blob.decode("utf-8", "replace"))
              and path not in seen_p and digest not in seen_s and quote not in seen_q)
        seen_p.add(path)
        seen_s.add(digest)
        seen_q.add(quote)
        bad += 0 if ok else 1
        print("%s bytes=%s words=%d in_norm=%s ok=%d"
              % (sid, len(blob) if blob is not None else "-", len(quote.split()),
                 ok and c2.norm(quote) in c2.norm((blob or b"").decode("utf-8", "replace")),
                 ok))
    admits = [m for m in map(c2.ADMIT_RE.match, c2.section(text, "## Gate")) if m]
    refuses = [m for m in map(c2.REFUSE_RE.match, c2.section(text, "## Gate")) if m]
    print("admits=%d refuses=%d" % (len(admits), len(refuses)))
    print("QUOTES: gates=%d bad=%d" % (len(gates), bad))
    return 0 if bad == 0 and admits and refuses else 1


if __name__ == "__main__":
    sys.exit(main())
