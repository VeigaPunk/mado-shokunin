#!/usr/bin/env python3
"""PRED-C1-r37-v2 — event-socket delivery ground admitted into the corpus.

Counts, at one committed revision, the frozen target entries that land on
coverage ground the lane did not hold at the round base. An entry counts only
when every clause holds:

  a  the entry exists at REV and did not exist at BASE
  b  its first 15 lines carry `source:`, `verified-at:` and `recheck:`; the
     `source:` lines name at least one S-id
  c  every cited S-id is a `## Registry` row of corpus/SOURCES.md with 11
     cells, status `mined`, and `used-by` naming the entry
  d  every cited S-id has a `GATE <id> receipt=<path> sha256=<hex>
     quote="<text>"` line under `## Gate` of corpus/lessons/round-37.md; the
     receipt is committed at REV, its sha256 equals the declared digest, the
     quote has at most 25 words and occurs verbatim in the receipt bytes
  e  a `## Coverage map` table row of corpus/README.md names
     `knowledge/<basename>` in its first cell
  f  each of the entry's frozen surface tokens occurs in the entry and in at
     least one receipt its Gate lines bind
  g  the entry states its evidence: for every cited S-id, the body carries one
     of that id's located Gate quotes verbatim and at least one `**OBS**` line
     naming the id (v1 lacked g: a token-only stub wired to real receipts
     reached the target — the v1 golden control)

Precondition (exit 2 when false): no corpus/knowledge/ file at BASE contains
any frozen surface token — the ground is unheld at the base.

Target: admitted == 2 -> TARGET_MET, exit 0; otherwise TARGET_MISSED, exit 1.
Setup or usage errors exit 2. Git runs with every ambient GIT_* variable
removed, so the caller's environment cannot redirect the repository.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys

PRED = "PRED-C1-r37-hardened-scratch"
BASE_DEFAULT = "b4e47e980bfb0cbc8a4e788f59a41db858751fd8"
TARGETS = {
    "corpus/knowledge/event-delivery-limits-r26.md": ["MAX_QUEUED_EVENTS", "overflowed event queue"],
    "corpus/knowledge/event-queue-observability-r37.md": ["debug:disable_logs", "m_logsEnabled"],
}
LESSON = "corpus/lessons/round-37.md"
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
GATE_RE = re.compile(r'^GATE (S\d{3,}) receipt=(\S+) sha256=([0-9a-f]{64}) quote="(.+)"\s*$')
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
F = ".ufo/waves/round-37/fetch/"
PINNED = {
    "S189": (F + "S189.bin", "eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d"),
    "S201": (F + "S201.bin", "799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e"),
    "S212": (F + "S212.bin", "1e19d92638e7923f0e72f6e65c83f579e32b41d588d166d6efef543c3f97d7e9"),
    "S213": (F + "S213.receipt.txt", "1c1b0ce149ecd7b1d20b0a83f266197c89c9f5334d17dc035fe499d93272ce58"),
    "S214": (F + "S214.bin", "d04e3a2fe5c73ad8684377856ce8301e493929ed9f391e405fde4975eaf6b868"),
}
REQUIRED = {"corpus/knowledge/event-delivery-limits-r26.md": {"S189"},
            "corpus/knowledge/event-queue-observability-r37.md": {"S213", "S214"}}
LINEAGE = ["hands each connected client its own queue", "removed, not throttled",
           "partial writes are resumed rather than restarted",
           "events are dropped with a warning instead of being delivered",
           "drop it after 64 queued events", "with no error shown to the user",
           "reads at most 1024 bytes per event"]
CLAUSES = set(os.environ.get("C1H_CLAUSES", "pqul"))


def norm(s):
    return " ".join(s.replace("*", "").replace("`", "").lower().split())


class Setup(Exception):
    pass


def git(repo, *args, binary=False):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, env=ENV)
    if p.returncode != 0:
        return None
    return p.stdout if binary else p.stdout.decode("utf-8", "replace")


def show(repo, rev, path, binary=False):
    return git(repo, "show", f"{rev}:{path}", binary=binary)


def section(text, heading):
    out, inside = [], False
    for line in text.splitlines():
        if re.match(r"^ {0,3}## ", line):
            inside = line.strip() == heading
            continue
        if inside:
            out.append(line)
    return out


def registry_rows(text):
    rows = {}
    for line in section(text, "## Registry"):
        m = ROW_RE.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.setdefault(m.group(1), []).append(cells)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", default=BASE_DEFAULT)
    a = ap.parse_args()
    repo = os.path.abspath(a.repo)
    rev = git(repo, "rev-parse", "--verify", f"{a.rev}^{{commit}}")
    base = git(repo, "rev-parse", "--verify", f"{a.base}^{{commit}}")
    if not rev or not base:
        raise Setup("unresolvable revision")
    rev, base = rev.strip(), base.strip()

    base_files = git(repo, "ls-tree", "-r", "--name-only", base, "--", "corpus/knowledge") or ""
    held = []
    for path in base_files.split():
        body = show(repo, base, path) or ""
        for toks in TARGETS.values():
            held += [f"{path}:{t}" for t in toks if t in body]
    if held:
        raise Setup("ground_held_at_base " + ",".join(held))

    sources = show(repo, rev, "corpus/SOURCES.md") or ""
    rows = registry_rows(sources)
    lesson = show(repo, rev, LESSON) or ""
    gates = {}
    for line in section(lesson, "## Gate"):
        m = GATE_RE.match(line.strip())
        if m:
            gates.setdefault(m.group(1), []).append(m.groups()[1:])
    readme = show(repo, rev, "corpus/README.md") or ""
    map_cells = [l.strip().strip("|").split("|")[0] for l in section(readme, "## Coverage map")
                 if l.strip().startswith("|")]

    admitted = 0
    for path, tokens in TARGETS.items():
        body = show(repo, rev, path)
        c = dict.fromkeys("abcdefgh", 0)
        c["a"] = int(body is not None and show(repo, base, path) is None)
        body = body or ""
        head = body.splitlines()[:15]
        src_lines = [l for l in head if re.match(r"^[-* ]*source *:", l)]
        ids = sorted(set(re.findall(r"\bS\d{3,}\b", " ".join(src_lines))))
        c["b"] = int(bool(ids)
                     and any(re.match(r"^[-* ]*verified-at *:", l) for l in head)
                     and any(re.match(r"^[-* ]*recheck *:", l) for l in head))
        c["c"] = int(bool(ids) and all(
            any(len(r) == 11 and r[7] == "mined" and path in [u.strip() for u in r[10].split(",")]
                for r in rows.get(i, []))
            for i in ids))
        receipts = []
        d_ok = g_ok = bool(ids)
        lines = body.splitlines()
        for i in ids:
            good, stated = False, False
            for rpath, digest, quote in gates.get(i, []):
                if "p" in CLAUSES and PINNED.get(i) != (rpath, digest):
                    continue
                if "q" in CLAUSES and (quote.strip() in sum(TARGETS.values(), [])
                                       or (len(quote.split()) < 3 and len(quote) < 24)):
                    continue
                blob = show(repo, rev, rpath, binary=True)
                if (blob is not None and hashlib.sha256(blob).hexdigest() == digest
                        and len(quote.split()) <= 25 and quote.encode() in blob):
                    good = True
                    receipts.append(blob)
                    stated = stated or quote in body
            d_ok = d_ok and good
            g_ok = g_ok and stated and any("**OBS**" in l and re.search(rf"\b{i}\b", l) for l in lines)
        c["d"] = int(d_ok)
        c["g"] = int(g_ok)
        base_name = "knowledge/" + path.rsplit("/", 1)[1]
        c["e"] = int(any(base_name in cell for cell in map_cells))
        c["f"] = int(all(t in body and any(t.encode() in b for b in receipts) for t in tokens))
        h = 1
        if "p" in CLAUSES:
            h &= int(set(ids) <= set(PINNED) and REQUIRED[path] <= set(ids))
        if "u" in CLAUSES:
            h &= int(all(len(rows.get(i, [])) == 1 for i in ids))
        lineage = sum(s in norm(body) for s in LINEAGE)
        if "l" in CLAUSES and path.endswith("-r26.md"):
            h &= int(lineage >= 4)
        c["h"] = h
        ok = int(all(c.values()))
        admitted += ok
        print(f"{PRED} entry={path} " + " ".join(f"{k}={v}" for k, v in c.items())
              + f" ids={','.join(ids) or '-'} lineage={lineage}/{len(LINEAGE)} clauses={''.join(sorted(CLAUSES))} ok={ok}")

    verdict = "TARGET_MET" if admitted == len(TARGETS) else "TARGET_MISSED"
    print(f"{PRED} admitted={admitted}/{len(TARGETS)} verdict={verdict} rev={rev} base={base}")
    return 0 if verdict == "TARGET_MET" else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Setup as e:
        print(f"{PRED} SETUP {e}")
        sys.exit(2)
