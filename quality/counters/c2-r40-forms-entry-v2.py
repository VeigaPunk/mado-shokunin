#!/usr/bin/env python3
"""PRED-C2-r40-v2 - the getoption native-forms entry is admitted (C2, coverage).

v2 re-registers PRED-C2-r40-v1 (quality/counters/c2-r40-forms-entry.py, frozen
5e7e885) after the round-40 wave falsified it BEFORE any data commit: a 5-file,
1.4 kB fabrication with one receipt shared by four ids and an N=1 census scored
1/1; used-by was a substring test; the count lines were free text in the entry;
the README row and the GATE lines were fence- and indent-blind; a stale GATE
line preceded the valid one; the opened-date and receipt-path clauses were not
exercised by the controls. v1 stays in the tree as the superseded predicate.

Scores one committed revision REV (revision-addressed git reads, every ambient
GIT_* variable removed; nothing in the lane is written). The entry is
corpus/knowledge/hyprctl-getoption-native-forms-r40.md. Fenced code blocks
(``` ... ```) of the entry and of the README are removed before any line is
matched. It is admitted iff every clause holds:

  a  the entry exists at REV and is absent at BASE (present at BASE is a
     setup error, exit 2);
  b  within its first 20 lines: >= 4 distinct `source: S###` lines,
     `verified-at: 2026-10-25` and `recheck:` as an ISO date, `NNd` or `on-*`;
  c  every cited id has exactly one `## Registry` row (0-3 leading spaces),
     11 cells, status `mined`, and its used-by cell, split on `,` and `;` and
     trimmed, lists the entry's path as one item; ids absent from the BASE
     registry (at least 2) carry opened 2026-10-25; ids present at BASE keep
     cells 1-10 byte-equal to their BASE row;
  d  corpus/lessons/round-40.md `## Gate` holds, per cited id, EXACTLY ONE line
     (starting in column 0) `GATE <id> receipt=<path> sha256=<64 hex>
     quote="<q>"`; the receipt is committed at REV under
     .ufo/waves/round-40/fetch/ with exactly that sha256, is >= 512 bytes, and
     is distinct per id (no two ids share a path or a sha256 or a quote); the
     quote is 3-25 words and occurs in the receipt's normalized text (tags,
     scripts, styles stripped, entities decoded, whitespace collapsed);
  e  each new id's location (the last whitespace-separated token of cell 1)
     occurs in no other registry row;
  f  corpus/README.md holds exactly one column-zero index row for the entry
     outside fenced blocks;
  g  per cited id, one entry line (outside fences) names the id and carries its
     Gate quote, and that line is not one of the three census lines of h;
  h  exactly one new cited row has kind own-work; its Gate receipt holds, each
     on a line of its own, `tool sha256 <hex>` equal to the sha256 of
     tools/mado-options.py at REV, `forms int=A float=B str=C custom=D`,
     `labels agreement=W agreement*=X mismatch=Y config-only=Z live-default=V`
     and `allforms int=A float=B str=C custom=D vec2=E`; the forms line equals
     the counts of the committed capture .ufo/waves/round-40/c1/
     native-capture.jsonl at REV, the allforms line equals the counts of
     native-capture-all.jsonl at REV, A+B+C+D == W+X+Y+Z+V == the capture's
     line count; and the entry carries the three lines verbatim, each as a
     line of its own (outside fences).

Final line: `PRED-C2-r40-v2: admitted=N/1 verdict=TARGET_MET|TARGET_MISSED
rev=<full hash>`. TARGET_MET iff admitted=1/1 (exit 0), else exit 1.
Residual (declared): a fabricated self-consistent set - invented receipt bytes
(>= 512 bytes, distinct per id) holding invented quotes, and census lines
copied from the committed captures - passes; committed bytes cannot prove a
receipt is what its location served or what the compositor answered.
"""
import argparse
import collections
import hashlib
import html
import json
import os
import re
import subprocess
import sys

PRED = "PRED-C2-r40-v2"
BASE_DEFAULT = "9fc511ddce708327377161202f358ce37dc266ba"
ENTRIES = ("corpus/knowledge/hyprctl-getoption-native-forms-r40.md",)
TOOL = "tools/mado-options.py"
CAPTURE = ".ufo/waves/round-40/c1/native-capture.jsonl"
CAPTURE_ALL = ".ufo/waves/round-40/c1/native-capture-all.jsonl"
LESSON = "corpus/lessons/round-40.md"
FETCH = ".ufo/waves/round-40/fetch/"
OPENED = "2026-10-25"
MIN_RECEIPT = 512
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
GATE_RE = re.compile(r'^GATE (S\d{3,}) receipt=(\S+) sha256=([0-9a-f]{64}) '
                     r'quote="(.+)"\s*$')
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)(\s|$)")
SRC_RE = re.compile(r"^source:\s*(S\d{3,})\b")
FORMS_RE = re.compile(r"^forms int=(\d+) float=(\d+) str=(\d+) custom=(\d+)$")
LABELS_RE = re.compile(r"^labels agreement=(\d+) agreement\*=(\d+) "
                       r"mismatch=(\d+) config-only=(\d+) "
                       r"live-default=(\d+)$")
ALL_RE = re.compile(r"^allforms int=(\d+) float=(\d+) str=(\d+) custom=(\d+) "
                    r"vec2=(\d+)$")
SHA_RE = re.compile(r"^tool sha256 ([0-9a-f]{64})$")


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


def unfenced(text):
    out, fenced = [], False
    for line in text.splitlines():
        if re.match(r"^\s{0,3}(```|~~~)", line):
            fenced = not fenced
            continue
        if not fenced:
            out.append(line)
    return out


def registry(blob):
    rows = {}
    for line in section((blob or b"").decode("utf-8", "replace"),
                        "## Registry"):
        m = ROW_RE.match(line)
        if m:
            cells = [c.strip() for c in line.strip().split("|")[1:-1]]
            rows.setdefault(m.group(1), []).append(cells)
    return rows


def capture_counts(blob, forms):
    c = collections.Counter()
    n = 0
    for l in (blob or b"").decode("utf-8", "replace").splitlines():
        if not l.strip():
            continue
        try:
            o = json.loads(l)
        except ValueError:
            return None, 0
        n += 1
        for f in forms:
            if f in o:
                c[f] += 1
    return c, n


def score(repo, rev, base, entry, reg_rev, reg_base, lesson, readme):
    name = os.path.basename(entry)
    cl = dict.fromkeys("abcdefgh", 0)
    raw = show(repo, rev, entry)
    text = raw.decode("utf-8", "replace") if raw is not None else ""
    lines = unfenced(text)
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
        items = [x.strip() for x in re.split(r"[,;]", cells[10])]
        good = cells[7] == "mined" and entry in items
        if i in reg_base:
            old = reg_base[i]
            good &= len(old) == 1 and len(old[0]) == 11 \
                and old[0][:10] == cells[:10]
        else:
            new_ids.append(i)
            good &= cells[8] == OPENED
        rows_ok &= good
        print("%s %s clause=c id=%s new=%d status=%s used=%d ok=%d" % (
            PRED, name, i, i not in reg_base, cells[7], entry in items, good))
    cl["c"] = int(rows_ok and len(new_ids) >= 2)

    gates = collections.defaultdict(list)
    for line in section(lesson, "## Gate"):
        m = GATE_RE.match(line.rstrip("\n"))
        if m:
            gates[m.group(1)].append(m.groups()[1:])
    for line in section(lesson, "## Gate"):
        if re.match(r"^\s+GATE S\d", line):
            gates["<indented>"].append(None)
    d_ok, g_ok = bool(ids), bool(ids)
    receipts, seen_paths, seen_sha, seen_quote = {}, set(), set(), set()
    census = {"forms": FORMS_RE, "labels": LABELS_RE, "allforms": ALL_RE}
    census_lines = set()
    for i in ids:
        good = None
        gl = gates.get(i, [])
        if len(gl) == 1:
            path, digest, quote = gl[0]
            blob = show(repo, rev, path) if path.startswith(FETCH) else None
            if (blob is not None and len(blob) >= MIN_RECEIPT
                    and hashlib.sha256(blob).hexdigest() == digest
                    and 3 <= len(quote.split()) <= 25
                    and path not in seen_paths and digest not in seen_sha
                    and quote not in seen_quote
                    and norm(quote) in norm(blob.decode("utf-8", "replace"))):
                good = quote
                receipts[i] = blob.decode("utf-8", "replace")
                seen_paths.add(path)
                seen_sha.add(digest)
                seen_quote.add(quote)
        print("%s %s clause=d id=%s gates=%d bound=%d" % (
            PRED, name, i, len(gl), good is not None))
        if good is None:
            d_ok = g_ok = False
    cl["d"] = int(d_ok and not gates.get("<indented>"))

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

    own = [i for i in new_ids if reg_rev[i][0][2] == "own-work"]
    cap, n_cap = capture_counts(show(repo, rev, CAPTURE),
                                ("int", "float", "str", "custom"))
    capall, n_all = capture_counts(show(repo, rev, CAPTURE_ALL),
                                   ("int", "float", "str", "custom", "vec2"))
    h_ok = False
    tool = show(repo, rev, TOOL)
    if (len(own) == 1 and own[0] in receipts and tool is not None
            and cap is not None and capall is not None and n_cap > 0):
        rlines = receipts[own[0]].splitlines()
        shas = [m.group(1) for m in map(SHA_RE.match, rlines) if m]
        fm = [m for m in map(FORMS_RE.match, rlines) if m]
        lm = [m for m in map(LABELS_RE.match, rlines) if m]
        am = [m for m in map(ALL_RE.match, rlines) if m]
        if len(fm) == 1 and len(lm) == 1 and len(am) == 1 \
                and shas == [hashlib.sha256(tool).hexdigest()]:
            want_f = [cap[f] for f in ("int", "float", "str", "custom")]
            want_a = [capall[f] for f in
                      ("int", "float", "str", "custom", "vec2")]
            got_f = [int(x) for x in fm[0].groups()]
            got_l = [int(x) for x in lm[0].groups()]
            got_a = [int(x) for x in am[0].groups()]
            ent = set(lines)
            census_lines = {fm[0].group(0), lm[0].group(0), am[0].group(0)}
            h_ok = (got_f == want_f and got_a == want_a
                    and sum(got_f) == sum(got_l) == n_cap
                    and sum(got_a) == n_all
                    and census_lines <= ent)
    cl["h"] = int(h_ok)

    entry_lines = [re.sub(r"\s+", " ", l) for l in lines
                   if l not in census_lines
                   and not l.startswith(("forms ", "labels ", "allforms "))]
    for i in ids:
        quote = None
        for path, digest, q in gates.get(i, []):
            quote = q
        if i not in receipts or quote is None:
            g_ok = False
            continue
        q = re.sub(r"\s+", " ", quote)
        hit = any(re.search(r"\b%s\b" % i, l) and q in l
                  for l in entry_lines)
        g_ok &= hit
        print("%s %s clause=g id=%s obs=%d" % (PRED, name, i, hit))
    cl["g"] = int(g_ok)

    pat = re.compile(r"^\| `knowledge/%s`" % re.escape(name))
    cl["f"] = int(sum(1 for l in unfenced(readme) if pat.match(l)) == 1)
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
