#!/usr/bin/env python3
"""ExecRows w2 probe: run the FROZEN C2 counter's clause_c over the drafted round-47 rows.

Reads the rows from the w1 seat draft (or --rows), the pins from the lane's
.ufo/waves/round-47/fetch/, and reports per-row clause-c results twice:
  as-drafted : exactly the receipts the rows carry
  repathed   : `.ufo/waves/round-47/w1/ScrRows/fetch/` rewritten to `.ufo/waves/round-47/fetch/`
A scratch git repo is built under --work (required; TMPDIR is never relied on) and removed.

  python3 clause-c-probe.py --work /fast/scratch/hyaku/mado-r47/ExecRows
"""
import argparse
import importlib.util
import os
import re
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality/counters/c2-r47-terminal-entry.py")
ROWS = os.path.join(LANE, ".ufo/waves/round-47/w1/ScrRows/rows.md")
PINS = os.path.join(LANE, ".ufo/waves/round-47/fetch")
ROW_RE = re.compile(r"^ {0,3}\|\s*S\d{3,}\s*\|")
DRAFT_PREFIX = ".ufo/waves/round-47/w1/ScrRows/fetch/"


def load_counter():
    spec = importlib.util.spec_from_file_location("c2", COUNTER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse_rows(path, repath):
    rows = {}
    for line in open(path, encoding="utf-8"):
        if not ROW_RE.match(line):
            continue
        cells = [c.strip() for c in line.strip().split("|")[1:-1]]
        if repath:
            cells = [c.replace(DRAFT_PREFIX, ".ufo/waves/round-47/fetch/") for c in cells]
        rows.setdefault(cells[0], []).append(cells)
    return {k: [list(v[0])] for k, v in rows.items()}


def build_pin_repo(work):
    repo = os.path.join(work, "pinrepo")
    shutil.rmtree(repo, ignore_errors=True)
    os.makedirs(repo)
    dst = os.path.join(repo, ".ufo/waves/round-47")
    os.makedirs(dst)
    shutil.copytree(PINS, os.path.join(dst, "fetch"))
    subprocess.run(["git", "-C", repo, "init", "-q"], check=True)
    top = subprocess.run(["git", "-C", repo, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        sys.exit("toplevel %r != %r" % (top, repo))
    subprocess.run(["git", "-C", repo, "add", "-A"], check=True)
    subprocess.run(["git", "-C", repo, "-c", "user.name=probe",
                    "-c", "user.email=probe@scratch.invalid", "commit", "-q",
                    "-m", "pins"], check=True)
    rev = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                         capture_output=True, text=True, check=True).stdout.strip()
    return repo, rev


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--rows", default=ROWS)
    args = ap.parse_args()
    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    m = load_counter()
    repo, rev = build_pin_repo(work)
    pins = m.fetch_pins(repo, rev)
    by_base = m.pin_index(pins)
    print("# pinrepo=%s rev=%s pins=%s" % (repo, rev, sorted(pins)))
    for label, repath in (("as-drafted", False), ("repathed", True)):
        reg = parse_rows(args.rows, repath)
        ok, _ = m.clause_c(repo, rev, sorted(reg), reg, pins, by_base, label)
        print("# %s ok=%s" % (label, ok))
    shutil.rmtree(repo, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
