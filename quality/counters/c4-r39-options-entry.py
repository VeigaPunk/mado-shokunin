#!/usr/bin/env python3
"""PRED-C4-r39-v1 - the config-option ownership ground is admitted (C3).

Scores one committed revision REV (revision-addressed git reads only, every
ambient GIT_* variable removed; nothing in the lane is written). The entry is
corpus/knowledge/config-option-table-r39.md; its cited rows are S218 (the
option-syntax documentation) and S219 (own-work: the options tool). It is
admitted iff every clause holds:

  a  the entry exists at REV (precondition: absent at BASE, else exit 2);
  b  its header carries `source:` naming S218 and S219, `verified-at:
     YYYY-MM-DD` and `recheck:` as an ISO date, an `NNd` count or `on-*`;
  c  S218 and S219 each have exactly one `## Registry` row (0-3 leading
     spaces), 11 cells, status `mined`, opened 2026-10-25, used-by naming the
     entry; S219's kind is `own-work`, S218's is not;
  d  corpus/lessons/round-39.md `## Gate` holds, per id, a line
     `GATE <id> receipt=<path> sha256=<64 hex> quote="<q>"` whose receipt is
     committed at REV under .ufo/waves/round-39/ with exactly that sha256, and
     whose quote is 3-25 words and occurs in the receipt's normalized text
     (tags, scripts and styles stripped, entities decoded, whitespace
     collapsed);
  e  the S219 receipt names the sha256 of tools/mado-options.py at REV (the
     own-work row binds the committed tool bytes);
  f  corpus/README.md holds exactly one column-zero index row for the entry;
  g  per id, one entry line names the id and carries its Gate quote.

Final line: `PRED-C4-r39-v1: admitted=N/1 verdict=TARGET_MET|TARGET_MISSED
rev=<full hash>`. TARGET_MET iff admitted=1/1 (exit 0), else exit 1.
Residual (declared): a fully fabricated, self-consistent set - invented
receipt bytes holding an invented quote - passes; committed bytes cannot
prove the receipt is what the URL served.
"""
import argparse
import hashlib
import html
import os
import re
import subprocess
import sys

PRED = "PRED-C4-r39-v1"
BASE_DEFAULT = "08be4eb7fd13358ed29b096e8924005d46ac409c"
ENTRY = "corpus/knowledge/config-option-table-r39.md"
LESSON = "corpus/lessons/round-39.md"
TOOL = "tools/mado-options.py"
IDS = ("S218", "S219")
OPENED = "2026-10-25"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
GATE_RE = re.compile(r'^GATE (S\d{3,}) receipt=(\S+) sha256=([0-9a-f]{64}) '
                     r'quote="(.+)"\s*$')
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)$")
INDEX_RE = re.compile(r"^\| `knowledge/config-option-table-r39\.md`")


class Setup(Exception):
    pass


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                       env=ENV)
    return p.stdout if p.returncode == 0 else None


def show(repo, rev, path):
    return git(repo, "show", "%s:%s" % (rev, path))


def resolve(repo, rev):
    out = git(repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}")
    if not out:
        raise Setup("unresolved revision %s" % rev)
    return out.decode().strip()


def norm(text):
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text,
                  flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def section(text, title):
    out, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.strip() == title
            continue
        if inside:
            out.append(line)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", default=BASE_DEFAULT)
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)
    rev = resolve(repo, args.rev)
    base = resolve(repo, args.base)
    if show(repo, base, ENTRY) is not None:
        raise Setup("precondition_failed entry_present_at_base")
    cl = dict.fromkeys("abcdefg", 0)
    raw = show(repo, rev, ENTRY)
    entry = raw.decode("utf-8", "replace") if raw is not None else ""
    cl["a"] = int(raw is not None)
    head = entry.splitlines()[:15]

    def hv(name):
        for line in head:
            if line.startswith(name + ":"):
                return line[len(name) + 1:].strip()
        return None
    src = hv("source") or ""
    va = hv("verified-at") or ""
    rc = hv("recheck") or ""
    cl["b"] = int(all(re.search(r"\b%s\b" % i, src) for i in IDS)
                  and re.fullmatch(r"\d{4}-\d{2}-\d{2}", va) is not None
                  and RECHECK_RE.match(rc) is not None)

    sources = (show(repo, rev, "corpus/SOURCES.md") or b"").decode(
        "utf-8", "replace")
    reg = section(sources, "## Registry")
    rows_ok = True
    for i in IDS:
        rows = [l for l in reg if (ROW_RE.match(l) or [None, None])[1] == i]
        if len(rows) != 1:
            rows_ok = False
            print("%s clause=c id=%s rows=%d" % (PRED, i, len(rows)))
            continue
        cells = [c.strip() for c in rows[0].strip().split("|")[1:-1]]
        if len(cells) != 11:
            rows_ok = False
            print("%s clause=c id=%s cells=%d" % (PRED, i, len(cells)))
            continue
        kind, status, opened, usedby = cells[2], cells[7], cells[8], cells[10]
        good = (status == "mined" and opened == OPENED and ENTRY in usedby
                and ((kind == "own-work") == (i == "S219")))
        rows_ok &= good
        print("%s clause=c id=%s kind=%s status=%s opened=%s used=%d ok=%d"
              % (PRED, i, kind, status, opened, ENTRY in usedby, good))
    cl["c"] = int(rows_ok)

    lesson = (show(repo, rev, LESSON) or b"").decode("utf-8", "replace")
    gates = {}
    for line in section(lesson, "## Gate"):
        m = GATE_RE.match(line.strip())
        if m and m.group(1) in IDS:
            gates.setdefault(m.group(1), []).append(m.groups()[1:])
    tool = show(repo, rev, TOOL)
    tool_hash = hashlib.sha256(tool).hexdigest() if tool is not None else None
    d_ok, e_ok, g_ok = True, False, True
    entry_lines = [re.sub(r"\s+", " ", l) for l in entry.splitlines()]
    for i in IDS:
        good = None
        for path, digest, quote in gates.get(i, []):
            if not path.startswith(".ufo/waves/round-39/"):
                continue
            blob = show(repo, rev, path)
            if blob is None or hashlib.sha256(blob).hexdigest() != digest:
                continue
            words = len(quote.split())
            if not 3 <= words <= 25:
                continue
            if norm(quote) not in norm(blob.decode("utf-8", "replace")):
                continue
            good = (blob, quote)
            break
        print("%s clause=d id=%s gates=%d bound=%d"
              % (PRED, i, len(gates.get(i, [])), good is not None))
        if good is None:
            d_ok = False
            g_ok = False
            continue
        q = re.sub(r"\s+", " ", good[1])
        hit = any(re.search(r"\b%s\b" % i, l) and q in l
                  for l in entry_lines)
        g_ok &= hit
        print("%s clause=g id=%s obs=%d" % (PRED, i, hit))
        if i == "S219" and tool_hash:
            e_ok = tool_hash in good[0].decode("utf-8", "replace")
    cl["d"], cl["e"], cl["g"] = int(d_ok), int(e_ok), int(g_ok)

    readme = (show(repo, rev, "corpus/README.md") or b"").decode(
        "utf-8", "replace")
    idx = sum(1 for l in readme.splitlines() if INDEX_RE.match(l))
    cl["f"] = int(idx == 1)
    admitted = int(all(cl.values()))
    print("%s clauses=%s" % (PRED, " ".join("%s:%d" % kv
                                             for kv in sorted(cl.items()))))
    print("%s: admitted=%d/1 verdict=%s rev=%s" % (
        PRED, admitted, "TARGET_MET" if admitted else "TARGET_MISSED", rev))
    return 0 if admitted else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Setup as exc:
        print("%s SETUP %s" % (PRED, exc))
        sys.exit(2)
