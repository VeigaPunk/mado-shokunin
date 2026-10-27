#!/usr/bin/env python3
"""Clause-level discrimination for PRED-C2-r51 on the scratch control fixture.

Each mutant is one commit cut from the control fixture rev; the counter must MISS and the named
clause must be the one that fails. Nothing here touches the lane.
"""
import argparse
import os
import subprocess
import sys

ENTRY = "corpus/knowledge/hyprland-dispatcher-dispatch-r51.md"
SOURCES = "corpus/SOURCES.md"
README = "corpus/README.md"
FETCH = ".ufo/waves/round-51/fetch"


def git(repo, *args, **kw):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, **kw)
    if p.returncode != 0 and kw.get("check", True):
        sys.exit("git %s failed: %s" % (" ".join(args), p.stderr))
    return p


def read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        return fh.read()


def write(root, rel, text):
    with open(os.path.join(root, rel), "w", encoding="utf-8") as fh:
        fh.write(text)


def sub(root, rel, old, new):
    text = read(root, rel)
    if old not in text:
        sys.exit("mutant anchor absent in %s: %r" % (rel, old))
    write(root, rel, text.replace(old, new, 1))


def sub_row(root, rel, rowid, old, new):
    """Replace inside the single table row whose first cell is ROWID."""
    lines = read(root, rel).splitlines(keepends=True)
    hits = [i for i, l in enumerate(lines) if l.startswith("| %s |" % rowid)]
    if len(hits) != 1:
        sys.exit("mutant row %s: %d matches in %s" % (rowid, len(hits), rel))
    if old not in lines[hits[0]]:
        sys.exit("mutant anchor absent in %s row %s: %r" % (rel, rowid, old))
    lines[hits[0]] = lines[hits[0]].replace(old, new, 1)
    write(root, rel, "".join(lines))


def m_nopins(root):
    for name in sorted(os.listdir(os.path.join(root, FETCH))):
        os.remove(os.path.join(root, FETCH, name))
    return "fetch pins removed"


def m_badtoken(root):
    sub(root, ENTRY, "keys=dispatcher,params", "keys=dispatcher,zzznotontheline")
    return "held token absent from the cited base line"


def m_status(root):
    sub_row(root, SOURCES, "S364", "| mined | 2026-10-27 |", "| queued | 2026-10-27 |")
    return "S364 status queued"


def m_noindex(root):
    text = read(root, README)
    keep = [l for l in text.splitlines(keepends=True)
            if "hyprland-dispatcher-dispatch-r51.md" not in l]
    write(root, README, "".join(keep))
    return "README index row removed"


def m_noquote(root):
    sub(root, ENTRY,
        '`const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);`',
        "the event path looks the handler up")
    return "S364 source quote removed"


def m_pinrow(root):
    sub(root, ENTRY, "| Hyprland-KeybindManager.cpp | src/managers/KeybindManager.cpp | S364 |",
        "| Hyprland-KeybindManager.cpp | src/managers/KeybindManager.cpp | S352 |")
    return "manifest binds the S364 pin to a different row"


MUTANTS = (("m1-nopins", m_nopins, "b"), ("m2-badtoken", m_badtoken, "d"),
           ("m3-status", m_status, "b"), ("m4-noindex", m_noindex, "a"),
           ("m5-noquote", m_noquote, "b"), ("m6-pinrow", m_pinrow, "b"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", required=True)
    args = ap.parse_args()
    root = os.path.realpath(args.fixture)
    top = git(root, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == root, top
    fails = 0
    for name, mutate, clause in MUTANTS:
        git(root, "checkout", "-q", "-B", "mut", args.rev)
        note = mutate(root)
        git(root, "-c", "user.name=ExecCounterC2", "-c", "user.email=fixture@shokunin.local",
            "add", "-A")
        git(root, "-c", "user.name=ExecCounterC2", "-c", "user.email=fixture@shokunin.local",
            "commit", "-q", "-m", "mutant %s: %s" % (name, note))
        rev = git(root, "rev-parse", "HEAD").stdout.strip()
        work = os.path.join(args.work, name)
        os.makedirs(work, exist_ok=True)
        env = dict(os.environ, TMPDIR=args.work)
        p = subprocess.run([sys.executable, "-I", args.counter, "--repo", root, "--rev", rev,
                            "--work", work], capture_output=True, text=True, env=env)
        last = p.stdout.strip().splitlines()[-1]
        met = [l for l in p.stdout.splitlines() if l.startswith("C2_R51: %s " % clause)]
        ok = (p.returncode == 1 and "verdict=TARGET_MISSED" in last and met
              and " ok=0 " in met[0])
        fails += 0 if ok else 1
        print("== %s (%s) exit=%d %s" % (name, note, p.returncode,
                                         "PASS" if ok else "FAIL"))
        for line in p.stdout.strip().splitlines():
            print("   " + line)
    git(root, "checkout", "-q", "-B", "fixture", args.rev)
    print("mutants=%d fails=%d" % (len(MUTANTS), fails))
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
