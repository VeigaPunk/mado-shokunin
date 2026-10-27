#!/usr/bin/env python3
"""Build seat-local git fixtures for Falsify41 (C1 self-pointer/context bypass).

All writes stay under /fast/scratch/hyaku/mado-r52/Falsify41/fixtures.
Instrument bytes are copied from the lane repo at the pinned base revision
(read-only `git show`), so the fixture ledgers describe real instruments.
"""

import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "85d57a818c3707397e21c840b6498b105ba798aa"
ROOT = "/fast/scratch/hyaku/mado-r52/Falsify41/fixtures"
INSTRUMENTS = [
    "tools/mado-verify.sh",
    "tools/mado-binds.py",
    "tools/mado-globals.py",
    "quality/counters/c1-r51-ledger.py",
    "quality/check-population.py",
]
CONTROL = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/controls/c1-do-nothing.md"


def run(args, cwd=None):
    proc = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit("failed: %s\n%s\n%s" % (args, proc.stdout, proc.stderr))
    return proc.stdout


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def source(rel):
    return run(["git", "-C", LANE, "show", "%s:%s" % (BASE, rel)])


def commit(repo, msg):
    top = run(["git", "-C", repo, "rev-parse", "--show-toplevel"]).strip()
    assert os.path.realpath(top) == os.path.realpath(repo), (top, repo)
    run(["git", "-C", repo, "add", "-A"])
    run(["git", "-C", repo, "-c", "user.name=Falsify41",
         "-c", "user.email=falsify41@local.invalid",
         "-c", "commit.gpgsign=false", "commit", "-q", "-m", msg])


def new_repo(name):
    repo = os.path.join(ROOT, name)
    if os.path.exists(repo):
        shutil.rmtree(repo)
    os.makedirs(repo)
    run(["git", "init", "-q", "-b", "main", repo])
    run(["git", "-C", repo, "config", "user.name", "Falsify41"])
    run(["git", "-C", repo, "config", "user.email", "falsify41@local.invalid"])
    return repo


def row(rel, desc, pointer):
    return "| `%s` | %s | `%s` |" % (rel, desc, pointer)


def build_laundered():
    repo = new_repo("laundered")
    for rel in INSTRUMENTS:
        write(os.path.join(repo, rel), source(rel))
    census = "# Tracked instrument inventory (generated census)\n\n" + "".join(
        "- %s — tracked instrument; see the ledger.\n" % os.path.basename(rel)
        for rel in INSTRUMENTS)
    write(os.path.join(repo, "quality/tool-inventory.md"), census)
    ledger = ["# mado tracked-instrument ledger",
              "",
              "| instrument | description | accountability pointer |",
              "|---|---|---|"]
    for rel in INSTRUMENTS:
        desc = ("Read only helper for %s; reports config bytes from a file "
                "line by line." % os.path.basename(rel))
        ledger.append(row(rel, desc, "quality/tool-inventory.md"))
    write(os.path.join(repo, "quality/tool-ledger.md"), "\n".join(ledger) + "\n")
    commit(repo, "fixture: laundered no-work ledger (census pointer, templated descriptions)")
    return repo


def build_control():
    repo = new_repo("control")
    write(os.path.join(repo, "tools/mado-verify.sh"), source("tools/mado-verify.sh"))
    write(os.path.join(repo, "quality/tool-ledger.md"), open(CONTROL, encoding="utf-8").read())
    commit(repo, "fixture: frozen c1-do-nothing control installed as the ledger")
    return repo


def build_copy():
    repo = new_repo("laundered-copy")
    for rel in INSTRUMENTS:
        write(os.path.join(repo, rel), source(rel))
    ledger = ["# mado tracked-instrument ledger",
              "",
              "| instrument | description | accountability pointer |",
              "|---|---|---|"]
    for rel in INSTRUMENTS:
        desc = ("Read only helper for %s; reports config bytes from a file "
                "line by line." % os.path.basename(rel))
        ledger.append(row(rel, desc, "quality/tool-ledger-copy.md"))
    text = "\n".join(ledger) + "\n"
    write(os.path.join(repo, "quality/tool-ledger.md"), text)
    write(os.path.join(repo, "quality/tool-ledger-copy.md"), text)
    commit(repo, "fixture: no-work ledger whose pointer target is a byte-identical copy")
    return repo


if __name__ == "__main__":
    os.makedirs(ROOT, exist_ok=True)
    for fn in (build_laundered, build_control, build_copy):
        repo = fn()
        print("%s %s" % (repo, run(["git", "-C", repo, "rev-parse", "HEAD"]).strip()))
