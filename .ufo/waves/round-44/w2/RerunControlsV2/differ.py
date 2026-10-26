#!/usr/bin/env python3
"""RerunControlsV2 differ (round-44 w2): compare two control-runner receipts field by field.

Allowed to differ (declared in registration-v2.md / the counter docstrings): nonce, rev (both are RNG seeds of
the C1 fixture lattice, and the C2 clone commits cannot hash the same at a different freeze), and therefore the
C1 `fixtures=k/26` share. Everything else - control roster, want/got/rc/ok, the clause vector, the top verdict
word, and (C2) admitted=x/1 - must be identical.

Usage: differ.py COMMITTED RERUN
Exit 0 = no disallowed difference."""
import re
import sys

ALLOWED = {"nonce", "rev", "fixtures"}


def parse(path):
    head, rows, trailer = None, [], None
    for line in open(path, encoding="utf-8").read().splitlines():
        if not line.strip():
            continue
        m = re.match(r"(CTL_C[12]v2):? +(.*)$", line)
        if m is None:
            raise SystemExit("unparsable line in %s: %r" % (path, line))
        body = m.group(2)
        if body.startswith("VERDICT:"):
            trailer = body if trailer is None else trailer + " || " + body
            continue
        if body.startswith("rev=") or body.startswith("freeze="):
            head = body
            continue
        name = body.split(" ")[0]
        fields = {}
        for k, v in re.findall(r"(want|got|rc|admitted)=(\S+)", body):
            fields[k] = v.rstrip("|")
        fields["ok"] = "WRONG" if " WRONG " in body else ("ok" if " ok |" in body else "?")
        clauses = re.search(r"\| ([a-z0-9]+:\d(?: [a-z0-9]+:\d)*) \|", body)
        fields["clauses"] = clauses.group(1) if clauses else "-"
        verd = re.search(r"verdict=(TARGET_MET|TARGET_MISSED)", body)
        fields["verdict"] = verd.group(1) if verd else "-"
        tail = re.search(r"(?:fixtures=(\d+)/(\d+)|admitted=(\d+)/(\d+))", body)
        if tail:
            fields["fixtures"] = "%s/%s" % (tail.group(1), tail.group(2)) if tail.group(1) is not None \
                else "%s/%s" % (tail.group(3), tail.group(4))
        rows.append((name, fields))
    return head, rows, trailer


def main():
    a, b = parse(sys.argv[1]), parse(sys.argv[2])
    diffs = 0
    keys = ["want", "got", "rc", "ok", "clauses", "verdict"]
    print("HEAD committed: %s" % a[0])
    print("HEAD rerun    : %s" % b[0])
    strip = lambda s: re.sub(r"(rev|freeze)=\S+", r"\1=<SEED>", s or "")
    if strip(a[0]) != strip(b[0]):
        print("HEAD DIFF beyond the rev/freeze seed")
        diffs += 1
    if len(a[1]) != len(b[1]):
        print("ROSTER COUNT %d vs %d" % (len(a[1]), len(b[1])))
        diffs += 1
    for (na, fa), (nb, fb) in zip(a[1], b[1]):
        if na != nb:
            print("ROSTER %-40s vs %s" % (na, nb))
            diffs += 1
            continue
        bad = []
        for k in keys:
            va, vb = fa.get(k, "-"), fb.get(k, "-")
            if va != vb:
                bad.append("%s: %s -> %s" % (k, va, vb))
        fa_, fb_ = fa.get("fixtures"), fb.get("fixtures")
        note = "" if fa_ == fb_ else "  [allowed fixtures %s -> %s]" % (fa_, fb_)
        print("%-42s %s%s" % (na, "IDENTICAL" if not bad else "DIFF " + "; ".join(bad), note))
        diffs += bool(bad)
    print("TRAILER committed: %s" % a[2])
    print("TRAILER rerun    : %s" % b[2])
    if a[2] != b[2]:
        print("TRAILER DIFF (expected: freeze/rev label)")
    print("RESULT: %s" % ("MATCH (no disallowed difference)" if diffs == 0 else "%d DISALLOWED DIFFS" % diffs))
    return 0 if diffs == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
