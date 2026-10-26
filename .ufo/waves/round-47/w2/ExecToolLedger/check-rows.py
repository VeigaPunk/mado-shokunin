#!/usr/bin/env python3
"""check-rows.py — re-derive every round-47 w1 tool-ledger row from the repo.

For each row of `.ufo/waves/round-47/w1/ScrToolLedger/ledger.md` (the §2 tables) and each row of
its §8 machine block, print:

  tool | receipt exists at base/HEAD (git cat-file) | round stated vs round in the receipt path |
  tool sha256 the receipt records vs sha256 of tools/<tool> at HEAD | declared status vs derived |
  selftest: rc + last line at HEAD (the tool is run read-only with --selftest)

Read-only: `git cat-file`, `git ls-tree`, file reads and one `--selftest` per tool that has one.
Writes nothing.  Usage: python3 -I check-rows.py --repo <lane> [--no-selftest]
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE = "c24adef2632672325a4eef3e3492f6716ccb6d14"
LEDGER_REL = ".ufo/waves/round-47/w1/ScrToolLedger/ledger.md"
NO_SELFTEST = {"mado-eventq.py", "mado-tripwire.py", "mado-binds.py", "mado-anims.py",
               "mado-wsrules.py"}          # `--selftest` is an unrecognised argument
NEEDS_ARG = {"mado-assessment.py": ".ufo/waves/round-21/assessment-fixtures",
             "mado-evidence-audit.py": ".ufo/waves/round-22/audit/fixtures"}


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), capture_output=True)


def rows_from_tables(text):
    """tool -> (receipt, stated_round) from the §2 markdown tables.

    A row that says "same file" (the §2c gates) inherits the receipt of the row above it.
    The receipt of a `none` row is not a receipt: the §8 block decides that, not this table.
    """
    out = {}
    last = "-"
    for line in text.splitlines():
        if not line.startswith("| `mado-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        tool = cells[0].strip("`")
        blob = " | ".join(cells)
        m = re.search(r"(\.ufo/[\w./-]+\.txt)", blob)
        r = re.search(r"·\s*r(\d+)\s*·", blob)
        if m:
            last = m.group(1)
            out.setdefault(tool, (last, "r" + r.group(1) if r else "-"))
        elif "same file" in blob:
            out.setdefault(tool, (last, "r" + r.group(1) if r else "-"))
    return out


def rows_from_block(text):
    """tool -> (declared, receipt, sha) from the ledger-rows block."""
    out = {}
    if "<!-- ledger-rows" not in text:
        return out
    body = text.split("<!-- ledger-rows", 1)[1].split("-->", 1)[0]
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        tool, declared, receipt, sha = line.split("\t")
        out[tool] = (declared, receipt, sha)
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--no-selftest", action="store_true")
    a = ap.parse_args(argv)
    repo = os.path.abspath(a.repo)
    text = open(os.path.join(repo, LEDGER_REL), encoding="utf-8").read()
    tables = rows_from_tables(text)
    block = rows_from_block(text)
    tools = sorted(p for p in git(repo, "ls-tree", "-r", "--name-only", a.rev, "--", "tools/")
                   .stdout.decode().splitlines()
                   if os.path.basename(p).startswith("mado-"))
    print("# ledger: %s sha256=%s" % (LEDGER_REL, hashlib.sha256(text.encode()).hexdigest()))
    print("# rev=%s base=%s" % (git(repo, "rev-parse", a.rev).stdout.decode().strip(), BASE))
    print("ROW\ttool\treceipt\tbase\tHEAD\tstated\tpath-round\tsha-in-receipt\tbytes\tdeclared\tderived\tselftest\ttable-evidence")
    bad = 0
    for path in tools:
        tool = os.path.basename(path)
        t_receipt, t_round = tables.get(tool, ("-", "-"))
        declared, b_receipt, b_sha = block.get(tool, ("-", "-", "-"))
        receipt = b_receipt if b_receipt != "-" else (t_receipt if declared != "none" else "-")
        in_base = git(repo, "cat-file", "-e", "%s:%s" % (BASE, receipt)).returncode == 0
        in_head = git(repo, "cat-file", "-e", "%s:%s" % (a.rev, receipt)).returncode == 0
        rnd = re.search(r"/round-(\d+)/", receipt)
        path_round = "r" + rnd.group(1) if rnd else "-"
        cur = hashlib.sha256(git(repo, "show", "%s:%s" % (a.rev, path)).stdout).hexdigest()
        rec_text = ""
        if in_head:
            rec_text = open(os.path.join(repo, receipt), encoding="utf-8",
                            errors="replace").read()
        sha_in = "yes" if b_sha != "-" and b_sha in rec_text else ("n/a" if b_sha == "-" else "NO")
        derived = "-" if declared == "none" else ("ok" if cur == b_sha else "stale")
        st = "-"
        if not a.no_selftest:
            if tool in NO_SELFTEST:
                st = "no-flag"
            else:
                cmd = ([os.path.join(repo, "tools", "mado-verify.sh"), "--selftest"]
                       if tool.endswith(".sh")
                       else [sys.executable, "-I", os.path.join(repo, path), "--selftest"])
                if tool in NEEDS_ARG:
                    cmd.append(os.path.join(repo, NEEDS_ARG[tool]))
                env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
                p = subprocess.run(cmd, capture_output=True, text=True, timeout=300,
                                   env=env, cwd=tempfile.gettempdir())
                last = (p.stdout or p.stderr).strip().splitlines()[-1][:60] if (p.stdout or p.stderr) else ""
                st = "rc=%d %s" % (p.returncode, last)
        print("ROW\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"
              % (tool, receipt, "yes" if in_base else "NO", "yes" if in_head else "NO",
                 t_round, path_round, sha_in, "ok" if (b_sha != "-" and cur == b_sha) else
                 ("-" if b_sha == "-" else "stale"), declared, derived, st,
                 t_receipt if t_receipt != receipt else ""))
        if declared == "none":
            continue                      # a none row is re-derived by absence, not here
        if not in_head or sha_in == "NO" or declared != derived \
                or (t_round not in ("-", path_round)):
            bad += 1
    print("ROWS=%d row-level-mismatch=%d" % (len(tools), bad))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
