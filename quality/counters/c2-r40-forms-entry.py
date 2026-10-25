#!/usr/bin/env python3
"""PRED-C2-r40-v1 - the getoption native-forms entry is admitted (C2, coverage).

Scores one committed revision REV (revision-addressed git reads, every ambient
GIT_* variable removed; nothing in the lane is written). The entry is
corpus/knowledge/hyprctl-getoption-native-forms-r40.md. It is admitted iff
every clause holds:

  a  the entry exists at REV and is absent at BASE (present at BASE is a
     setup error, exit 2);
  b  within its first 20 lines: >= 4 distinct `source: S###` lines,
     `verified-at: 2026-10-25` and `recheck:` as an ISO date, `NNd` or `on-*`;
  c  every cited id has exactly one `## Registry` row (0-3 leading spaces),
     11 cells, status `mined`, used-by naming the entry; ids absent from the
     BASE registry (at least 2 of them) carry opened 2026-10-25; ids present
     at BASE keep cells 1-10 byte-equal to their BASE row (a held row is
     re-opened, never rewritten);
  d  corpus/lessons/round-40.md `## Gate` holds, per cited id, a line
     `GATE <id> receipt=<path> sha256=<64 hex> quote="<q>"` whose receipt is
     committed at REV under .ufo/waves/round-40/fetch/ with exactly that
     sha256, and whose quote is 3-25 words and occurs in the receipt's
     normalized text (tags, scripts, styles stripped, entities decoded,
     whitespace collapsed);
  e  each new id's location (the last whitespace-separated token of cell 1)
     occurs in no other registry row;
  f  corpus/README.md holds exactly one column-zero index row for the entry;
  g  per cited id, one entry line names the id and carries its Gate quote;
  h  exactly one new cited row has kind own-work; its Gate receipt contains
     the sha256 of tools/mado-options.py at REV, one line
     `forms int=A float=B str=C custom=D` and one line
     `labels agreement=W agreement*=X mismatch=Y config-only=Z
     live-default=V` with A+B+C+D == W+X+Y+Z+V == N >= 1, and the entry text
     carries both lines verbatim.

Final line: `PRED-C2-r40-v1: admitted=N/1 verdict=TARGET_MET|TARGET_MISSED
rev=<full hash>`. TARGET_MET iff admitted=1/1 (exit 0), else exit 1.
Residual (declared): a fully fabricated, self-consistent set - invented
receipt bytes holding an invented quote and invented counts - passes;
committed bytes cannot prove the receipt is what the location served or what
the compositor answered.
"""
import argparse
import hashlib
import html
import os
import re
import subprocess
import sys

PRED = "PRED-C2-r40-v1"
BASE_DEFAULT = "9fc511ddce708327377161202f358ce37dc266ba"
ENTRIES = ("corpus/knowledge/hyprctl-getoption-native-forms-r40.md",)
TOOL = "tools/mado-options.py"
LESSON = "corpus/lessons/round-40.md"
FETCH = ".ufo/waves/round-40/fetch/"
OPENED = "2026-10-25"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
GATE_RE = re.compile(r'^GATE (S\d{3,}) receipt=(\S+) sha256=([0-9a-f]{64}) '
                     r'quote="(.+)"\s*$')
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)(\s|$)")
SRC_RE = re.compile(r"^source:\s*(S\d{3,})\b")


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


def registry(blob):
    """id -> list of cell lists (11 cells expected) from ## Registry."""
    rows = {}
    for line in section((blob or b"").decode("utf-8", "replace"),
                        "## Registry"):
        m = ROW_RE.match(line)
        if m:
            cells = [c.strip() for c in line.strip().split("|")[1:-1]]
            rows.setdefault(m.group(1), []).append(cells)
    return rows


def score(repo, rev, base, entry, reg_rev, reg_base, lesson, readme):
    name = os.path.basename(entry)
    cl = dict.fromkeys("abcdefgh", 0)
    raw = show(repo, rev, entry)
    text = raw.decode("utf-8", "replace") if raw is not None else ""
    cl["a"] = int(raw is not None)
    head = text.splitlines()[:20]
    ids = []
    for line in head:
        m = SRC_RE.match(line)
        if m and m.group(1) not in ids:
            ids.append(m.group(1))

    def hv(key):
        for line in head:
            if line.startswith(key + ":"):
                return line[len(key) + 1:].strip()
        return None
    va, rc = hv("verified-at"), hv("recheck")
    cl["b"] = int(len(ids) >= 4 and va == OPENED
                  and rc is not None and RECHECK_RE.match(rc) is not None)

    rows_ok = bool(ids)
    new_ids = []
    for i in ids:
        rows = reg_rev.get(i, [])
        if len(rows) != 1 or len(rows[0]) != 11:
            rows_ok = False
            print("%s %s clause=c id=%s rows=%d" % (PRED, name, i, len(rows)))
            continue
        cells = rows[0]
        good = cells[7] == "mined" and entry in cells[10]
        if i in reg_base:
            old = reg_base[i]
            good &= len(old) == 1 and len(old[0]) == 11 \
                and old[0][:10] == cells[:10]
        else:
            new_ids.append(i)
            good &= cells[8] == OPENED
        rows_ok &= good
        print("%s %s clause=c id=%s new=%d status=%s used=%d ok=%d" % (
            PRED, name, i, i not in reg_base, cells[7], entry in cells[10],
            good))
    cl["c"] = int(rows_ok and len(new_ids) >= 2)

    gates = {}
    for line in section(lesson, "## Gate"):
        m = GATE_RE.match(line.strip())
        if m:
            gates.setdefault(m.group(1), []).append(m.groups()[1:])
    entry_lines = [re.sub(r"\s+", " ", l) for l in text.splitlines()]
    d_ok, g_ok = bool(ids), bool(ids)
    receipts = {}
    for i in ids:
        good = None
        for path, digest, quote in gates.get(i, []):
            if not path.startswith(FETCH):
                continue
            blob = show(repo, rev, path)
            if blob is None or hashlib.sha256(blob).hexdigest() != digest:
                continue
            if not 3 <= len(quote.split()) <= 25:
                continue
            if norm(quote) not in norm(blob.decode("utf-8", "replace")):
                continue
            good = quote
            receipts[i] = blob.decode("utf-8", "replace")
            break
        print("%s %s clause=d id=%s gates=%d bound=%d" % (
            PRED, name, i, len(gates.get(i, [])), good is not None))
        if good is None:
            d_ok = g_ok = False
            continue
        q = re.sub(r"\s+", " ", good)
        hit = any(re.search(r"\b%s\b" % i, l) and q in l
                  for l in entry_lines)
        g_ok &= hit
        print("%s %s clause=g id=%s obs=%d" % (PRED, name, i, hit))
    cl["d"], cl["g"] = int(d_ok), int(g_ok)

    e_ok = True
    for i in new_ids:
        cells = reg_rev[i][0] if len(reg_rev.get(i, [[]])[0]) == 11 else None
        if cells is None:
            e_ok = False
            continue
        loc = cells[1].split()[-1] if cells[1].split() else ""
        same = [j for j, rr in reg_rev.items() for r in rr
                if len(r) == 11 and r[1].split() and r[1].split()[-1] == loc]
        e_ok &= bool(loc) and same == [i]
    cl["e"] = int(e_ok and bool(new_ids))

    h_ok = False
    own = [i for i in new_ids if reg_rev[i][0][2] == "own-work"]
    tool = show(repo, rev, TOOL)
    if len(own) == 1 and own[0] in receipts and tool is not None:
        rtext = receipts[own[0]]
        fm = re.search(r"^forms int=(\d+) float=(\d+) str=(\d+) custom=(\d+)$",
                       rtext, re.M)
        lm = re.search(r"^labels agreement=(\d+) agreement\*=(\d+) "
                       r"mismatch=(\d+) config-only=(\d+) "
                       r"live-default=(\d+)$", rtext, re.M)
        if fm and lm:
            nf = sum(int(x) for x in fm.groups())
            nl = sum(int(x) for x in lm.groups())
            h_ok = (hashlib.sha256(tool).hexdigest() in rtext
                    and nf == nl and nf >= 1
                    and fm.group(0) in text and lm.group(0) in text)
    cl["h"] = int(h_ok)

    pat = re.compile(r"^\| `knowledge/%s`" % re.escape(name))
    cl["f"] = int(sum(1 for l in readme.splitlines() if pat.match(l)) == 1)
    admitted = int(all(cl.values()))
    print("%s %s clauses=%s admitted=%d" % (
        PRED, name, " ".join("%s:%d" % kv for kv in sorted(cl.items())),
        admitted))
    return admitted


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", default=BASE_DEFAULT)
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)
    rev = resolve(repo, args.rev)
    base = resolve(repo, args.base)
    for e in ENTRIES:
        if show(repo, base, e) is not None:
            raise Setup("precondition_failed entry_present_at_base %s" % e)
    reg_rev = registry(show(repo, rev, "corpus/SOURCES.md"))
    reg_base = registry(show(repo, base, "corpus/SOURCES.md"))
    lesson = (show(repo, rev, LESSON) or b"").decode("utf-8", "replace")
    readme = (show(repo, rev, "corpus/README.md") or b"").decode(
        "utf-8", "replace")
    n = sum(score(repo, rev, base, e, reg_rev, reg_base, lesson, readme)
            for e in ENTRIES)
    met = n == 1
    print("%s: admitted=%d/1 verdict=%s rev=%s" % (
        PRED, n, "TARGET_MET" if met else "TARGET_MISSED", rev))
    return 0 if met else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Setup as exc:
        print("%s SETUP %s" % (PRED, exc))
        sys.exit(2)
