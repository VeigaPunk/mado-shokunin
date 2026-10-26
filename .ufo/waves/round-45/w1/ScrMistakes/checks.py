#!/usr/bin/env python3
"""Proposal checkers for QUALITY criteria 86-89 (seat ScrMistakes, round 45 w1).

Read-only. Every check is addressed by revision (`git -C <repo> show <rev>:<path>`); a
`--repo` may be any git repository. They exist so each proposed criterion ships a
command that goes red on the defect this round mined and green on a corrected fixture.

  87  session material stays shape-only in tracked bytes
        R1 a client-dump object (has address+class+mapped) carries an identity key:
           title, initialTitle, pid, stableId, xdgDescription, xdgTag
        R3 any object carries a non-empty instance_sig (the full signature)
        R4 a monitor-shaped object (has `name`) carries a non-empty
           serial/description/make/model (hardware identity)
  86  a receipt named *tip* carries the measured revision's full hex, or states the
      equivalence and the diff outside the round's own directory is empty
  88  every `| C<n>` claim row of a SCORECARD round section carries an after value in
      its Before -> after cell, not only a `see receipt` pointer
  89  every counter the round's registration names seeds its draw: `--nonce` default
      None (a fresh random draw per run) is a violation; `--seed` with an integer
      default passes

Output: one line per violation, `<check> VIOLATION <path> <detail>`, then a summary
`CHECK<n>: violations=<v> verdict=FAIL|CLEAN`, exit 1 on violations, 0 clean, 2 setup.
"""
import argparse
import json
import re
import subprocess
import sys

FORBID = {"title", "initialTitle", "pid", "stableId", "xdgDescription", "xdgTag"}
MONITOR_ID = {"serial", "description", "make", "model"}
HEX = re.compile(r"\b[0-9a-f]{40}\b")


def git(repo, *args, binary=False):
    p = subprocess.run(["git", "-C", repo] + list(args), capture_output=True)
    return p.stdout if binary else p.stdout.decode("utf-8", "replace")


def tracked(repo, rev):
    out = git(repo, "ls-tree", "-r", "--name-only", rev)
    if not out.strip():
        print("SETUP: no tracked files at %s" % rev, file=sys.stderr)
        sys.exit(2)
    return out.split()


def walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


def is_client_dump(o):
    return isinstance(o, dict) and {"address", "class", "mapped"} <= set(o)


def check87(repo, rev):
    v = 0
    for f in tracked(repo, rev):
        if not f.endswith(".json"):
            continue
        try:
            d = json.loads(git(repo, "show", "%s:%s" % (rev, f), binary=True))
        except Exception:
            continue
        for o in walk(d):
            if is_client_dump(o):
                bad = set(o) & FORBID
                if bad:
                    print("87 VIOLATION %s R1 identity_keys=%s" % (f, ",".join(sorted(bad))))
                    v += 1
                ident = {k for k in MONITOR_ID if isinstance(o.get(k), str) and o[k]}
                if ident and "name" in o:
                    print("87 VIOLATION %s R4 monitor_identity_keys=%s" % (f, ",".join(sorted(ident))))
                    v += 1
            if isinstance(o.get("instance_sig"), str) and o["instance_sig"]:
                print("87 VIOLATION %s R3 instance_sig len=%d" % (f, len(o["instance_sig"])))
                v += 1
    return v


def check86(repo, rev, rounddir):
    v = 0
    names = [f for f in tracked(repo, rev)
             if f.startswith(rounddir.rstrip("/") + "/receipts/") and "tip" in f.rsplit("/", 1)[-1]]
    if not names:
        print("SETUP: no *tip* receipt under %s/receipts at %s" % (rounddir, rev), file=sys.stderr)
        return None
    tip = git(repo, "rev-parse", rev).strip()
    for f in names:
        b = git(repo, "show", "%s:%s" % (rev, f))
        if tip in b:
            continue
        stated = [h for h in HEX.findall(b) if h != tip]
        equiv = re.search(r"equivalen", b, re.I) is not None
        if equiv and stated:
            outside = [x for x in git(repo, "diff", "--name-only", stated[0], tip).split()
                       if not x.startswith(rounddir.rstrip("/") + "/")]
            if not outside:
                continue
        print("86 VIOLATION %s names=%s tip=%s" % (f, ",".join(h[:8] for h in stated) or "none", tip[:8]))
        v += 1
    return v


def check88(repo, rev, scorecard="SCORECARD.md"):
    v = 0
    text = git(repo, "show", "%s:%s" % (rev, scorecard))
    if not text.strip():
        print("SETUP: %s absent at %s" % (scorecard, rev), file=sys.stderr)
        return None
    for i, line in enumerate(text.splitlines(), 1):
        if not re.match(r"^\| C[0-9]", line):
            continue
        cells = line.split("|")
        if len(cells) < 4:
            continue
        cell = cells[2]
        if "-->" not in cell and "->" not in cell:
            continue
        after = re.split(r"-->|->", cell)[-1]
        has_value = re.search(r"\d", after) and re.search(r"TARGET_MET|TARGET_MISSED|=", after)
        if not has_value:
            print("88 VIOLATION %s:%d after=%r" % (scorecard, i, after.strip()[:90]))
            v += 1
    return v


def check89(repo, rev, registration):
    v = 0
    reg = git(repo, "show", "%s:%s" % (rev, registration))
    if not reg.strip():
        print("SETUP: %s absent at %s" % (registration, rev), file=sys.stderr)
        return None
    names = sorted(set(re.findall(r"quality/counters/[\w.-]+\.py", reg)))
    if not names:
        print("SETUP: no counter path in %s at %s" % (registration, rev), file=sys.stderr)
        return None
    for f in names:
        b = git(repo, "show", "%s:%s" % (rev, f))
        m = re.search(r'add_argument\(\s*"--nonce"(.*?)\)', b, re.S)
        if m and "default=None" in m.group(1).replace(" ", ""):
            print("89 VIOLATION %s --nonce default=None (fresh random draw per run)" % f)
            v += 1
            continue
        s = re.search(r'add_argument\(\s*"--seed"(.*?)\)', b, re.S)
        if s and "default=None" in s.group(1).replace(" ", ""):
            print("89 VIOLATION %s --seed default=None" % f)
            v += 1
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("check", choices=["86", "87", "88", "89"])
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--round", default=".ufo/waves/round-45")
    ap.add_argument("--scorecard", default="SCORECARD.md")
    ap.add_argument("--registration", default=".ufo/waves/round-45/registration.md")
    a = ap.parse_args()
    if a.check == "87":
        v = check87(a.repo, a.rev)
    elif a.check == "86":
        v = check86(a.repo, a.rev, a.round)
    elif a.check == "88":
        v = check88(a.repo, a.rev, a.scorecard)
    else:
        v = check89(a.repo, a.rev, a.registration)
    if v is None:
        print("CHECK%s: setup error" % a.check)
        return 2
    print("CHECK%s: violations=%d verdict=%s" % (a.check, v, "FAIL" if v else "CLEAN"))
    return 1 if v else 0


if __name__ == "__main__":
    sys.exit(main())
