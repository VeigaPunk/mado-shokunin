#!/usr/bin/env python3
# check-sources-readback.py -- round-98 C2 gate: SOURCES.md citation read-back.
#
# Reads <repo>/corpus/SOURCES.md (rows with 0-3 leading spaces, 11 columns, in
# the "## Registry" section) and every <repo>/corpus/knowledge/*.md entry's
# source frontmatter block, then reports five finding rules:
#
#   R1 recheck-path                a row whose recheck cell contains "/" or
#                                  ends ".md"
#   R3 usedby-missing              a used-by member that does not exist on
#                                  disk (compared after posixpath.normpath;
#                                  "-" and the em-dash are empty cells)
#   R4 entry-cites-unacknowledged  an entry-cited row with status "mined"
#                                  whose used-by cell does not name that
#                                  entry; one finding per (row, entry) pair
#   R5 entry-cites-missing-row     an entry-cited id with no registry row
#   R6 duplicate-id                a row id that appears more than once
#
# R2 (usedby-outside-corpus) is deliberately NOT a finding: the committed
# registry legitimately names lane artifacts outside corpus/ in used-by cells
# (tools/*, SKILL.md, quality/*, .ufo/waves/*; 21 such cells at base, all
# legitimate per the declaration), the census validates those cells by
# existence (E11), and the L1 dropped R2 from the frozen predicate in round
# 98.  The gate still surfaces them as non-finding NOTE lines in plain mode.
#
# Frontmatter scope (pinned by the declaration): the source block starts at
# the entry's first column-0 "source:" line, continues over indented
# "  - Sxxx" list items and wrapped continuation lines, ends at a blank line,
# a "---" fence, a "#" heading or a column-0 "key:" line, and no later
# "source:" line ever opens another block.  An id counts only as a standalone
# token: not preceded by "/" (except inside an S-only slash chain such as
# S511/S512, whose members all count), not followed by "."/ "-" / "_", so
# .ufo/waves/round-37/fetch/S213.receipt.txt is not a citation.
#
# One finding per line:  SOURCES_READBACK: FINDING <rule> <id> <detail>
# Note line (plain mode): SOURCES_READBACK: NOTE outside-corpus <id> path=<p>
# Result line:           SOURCES_READBACK: rows=N entries=M findings=K
# Exit: 0 clean / 1 findings / 2 setup (missing registry, unreadable entry,
#       missing entry dir).  An entry without a "source:" block contributes no
#       citations and is not a setup error.
#
# CLI:
#   check-sources-readback.py --repo DIR [--json]
#   check-sources-readback.py --selftest
#
# Read-only, stdlib only, no subprocess, no network, no dynamic imports.

import argparse
import io
import json
import os
import posixpath
import re
import sys
import tempfile

PROG = "check-sources-readback.py"
RESULT = "SOURCES_READBACK:"
FINDING = "SOURCES_READBACK: FINDING"
EMPTY_CELLS = ("", "-", "\u2014")  # empty, ASCII hyphen, em-dash "none"
CHAIN_RE = re.compile(r"(?<![A-Za-z0-9])(S\d{3,}(?:/S\d{3,})+)(?![A-Za-z0-9])")
SOLO_RE = re.compile(r"(?<![A-Za-z0-9/])(S\d{3,})(?![A-Za-z0-9._\-])")
KEY_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*:")
SELFTEST_OK_LINE = "SOURCES_READBACK_SELFTEST: checks=%d failed=%d"
SELFTEST_FAIL_LINE = "SOURCES_READBACK_SELFTEST_FAIL: %s"


class SetupError(Exception):
    pass


def split_row(line):
    s = line.strip()
    if not s.startswith("|"):
        return None
    cells = [c.strip() for c in s.strip("|").split("|")]
    if len(cells) != 11:
        return None
    return cells


def is_separator(cells):
    return all(c and set(c) <= set("-:") for c in cells)


def parse_registry(text):
    rows = []
    in_reg = False
    for raw in text.splitlines():
        body = raw.lstrip(" ")
        indent = len(raw) - len(body)
        if body.startswith("##") and not body.startswith("###"):
            in_reg = body.strip() == "## Registry"
            continue
        if not in_reg or indent > 3:
            continue
        cells = split_row(body)
        if cells is None or cells[0] == "id" or is_separator(cells):
            continue
        rows.append(cells)
    return rows


def usedby_members(cell):
    """Empty markers are the empty string, "-" and the em-dash; normpath'd."""
    c = cell.strip()
    if c in EMPTY_CELLS:
        return []
    return [posixpath.normpath(m.strip()) for m in c.split(",") if m.strip()]


def token_ids(text):
    """S-ids in one line of the source block (chains split, tokens standalone)."""
    out = []
    spans = []
    for m in CHAIN_RE.finditer(text):
        out.extend(m.group(1).split("/"))
        spans.append(m.span())
    for m in SOLO_RE.finditer(text):
        if any(a <= m.start() < b for a, b in spans):
            continue
        out.append(m.group(1))
    return out


def source_block_ids(text):
    """S-ids of the entry's first source block; later source: lines ignored."""
    ids = []
    started = False
    in_block = False
    for raw in text.splitlines():
        if not started:
            if raw.startswith("source:"):
                started = True
                in_block = True
                ids.extend(token_ids(raw[len("source:"):]))
            continue
        if not in_block:
            continue  # the block has ended; no later source: line reopens it
        stripped = raw.strip()
        if (stripped == "" or raw.startswith("---") or raw.startswith("#")
                or KEY_RE.match(raw)):
            in_block = False
            continue
        ids.extend(token_ids(raw))
    seen = []
    for sid in ids:
        if sid not in seen:
            seen.append(sid)
    return seen


def load_entries(repo):
    kdir = os.path.join(repo, "corpus", "knowledge")
    if not os.path.isdir(kdir):
        raise SetupError("missing-entry-dir corpus/knowledge")
    out = []
    for name in sorted(os.listdir(kdir)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(kdir, name)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, "rb") as fh:
                text = fh.read().decode("utf-8")
        except (OSError, UnicodeDecodeError):
            raise SetupError("unreadable-entry corpus/knowledge/" + name)
        out.append(("corpus/knowledge/" + name, text))
    return out


def evaluate(repo):
    """Returns (rows, entries, findings, notes); raises SetupError."""
    reg = os.path.join(repo, "corpus", "SOURCES.md")
    if not os.path.isfile(reg):
        raise SetupError("missing-registry corpus/SOURCES.md")
    try:
        with open(reg, "rb") as fh:
            text = fh.read().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        raise SetupError("unreadable-registry corpus/SOURCES.md")
    rows = parse_registry(text)
    entries = load_entries(repo)

    counts = {}
    for cells in rows:
        rid = cells[0]
        if rid:
            counts[rid] = counts.get(rid, 0) + 1

    findings = []
    notes = []
    dup_done = set()
    for cells in rows:
        rid = cells[0]
        if not rid:
            continue
        if counts[rid] > 1 and rid not in dup_done:
            findings.append({"rule": "R6", "id": rid,
                             "detail": "count=%d" % counts[rid]})
            dup_done.add(rid)
        recheck = cells[9]
        if recheck not in EMPTY_CELLS and (
                "/" in recheck or recheck.endswith(".md")):
            findings.append({"rule": "R1", "id": rid,
                             "detail": "recheck=%s" % recheck})
        for m in usedby_members(cells[10]):
            if m == "corpus" or m.startswith("corpus/"):
                if not os.path.lexists(os.path.join(repo, m)):
                    findings.append({"rule": "R3", "id": rid,
                                     "detail": "path=%s" % m})
            else:
                # R2 per the L1 round-98 ruling: a note, never a finding.
                notes.append("NOTE outside-corpus %s path=%s" % (rid, m))

    acked = {}
    status = {}
    for cells in rows:
        acked.setdefault(cells[0], set()).update(usedby_members(cells[10]))
        status[cells[0]] = cells[7]
    seen_pairs = set()
    for epath, etext in entries:
        ekey = posixpath.normpath(epath)
        for sid in source_block_ids(etext):
            if sid not in acked:
                findings.append({"rule": "R5", "id": sid,
                                 "detail": "entry=%s" % epath})
            elif status.get(sid) == "mined" and ekey not in acked[sid]:
                pair = (sid, ekey)
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    findings.append({"rule": "R4", "id": sid,
                                     "detail": "entry=%s" % epath})
    return rows, entries, findings, notes


# --------------------------------------------------------------- selftest ---
FIX_HEADER = (
    "# SOURCES - fixture registry\n"
    "## Registry\n"
    "| id | source | kind | tier | scope | anchor | teaches | status"
    " | opened | recheck | used-by |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|\n"
)


def make_repo(root, row_lines, entries):
    corpus = os.path.join(root, "corpus")
    kdir = os.path.join(corpus, "knowledge")
    os.makedirs(kdir)
    with open(os.path.join(corpus, "SOURCES.md"), "w", encoding="utf-8") as fh:
        fh.write(FIX_HEADER)
        for line in row_lines:
            fh.write(line + "\n")
    for rel, text in sorted(entries.items()):
        with open(os.path.join(root, rel), "w", encoding="utf-8") as fh:
            fh.write(text)


def row(idn, usedby, recheck="90d", status="mined"):
    if usedby == "-":
        usedby = "\u2014"  # the registry's "none" marker
    return ("| %s | https://example.test/%s | docs | A | fixture scope %s"
            " | anchor %s | teaches %s | %s | 2026-11-01 | %s | %s |"
            % (idn, idn.lower(), idn.lower(), idn.lower(), idn.lower(),
               status, recheck, usedby))


def entry(ids_line):
    return "source: %s\n\n# fixture entry\n" % ids_line


def cli(argv, out, err):
    """In-process CLI; returns the exit code."""
    ap = argparse.ArgumentParser(prog=PROG)
    ap.add_argument("--repo")
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return gate_selftest(out, err)
    if not args.repo:
        err.write("usage: %s --repo DIR [--json] | --selftest\n" % PROG)
        return 2
    try:
        rows, entries, findings, notes = evaluate(args.repo)
    except SetupError as exc:
        err.write("%s SETUP %s\n" % (RESULT, exc))
        if args.as_json:
            out.write(json.dumps({"error": "setup", "detail": str(exc)}) + "\n")
        return 2
    if args.as_json:
        out.write(json.dumps({"rows": len(rows), "entries": len(entries),
                              "findings": findings}, sort_keys=True) + "\n")
    else:
        for f in findings:
            out.write("%s %s %s %s\n"
                      % (FINDING, f["rule"], f["id"], f["detail"]))
        for n in notes:
            out.write("%s %s\n" % (RESULT, n))
        out.write("%s rows=%d entries=%d findings=%d\n"
                  % (RESULT, len(rows), len(entries), len(findings)))
    return 1 if findings else 0


def gate_selftest(out, err):
    checks = []

    def check(cid):
        def deco(fn):
            checks.append((cid, fn))
            return fn
        return deco

    tmpobj = tempfile.TemporaryDirectory(prefix="readback-selftest-")
    tmp = tmpobj.__enter__()
    try:
        def build(name, row_lines, entries):
            d = os.path.join(tmp, name)
            os.makedirs(d)
            make_repo(d, row_lines, entries)
            return d

        def run(fx, extra=()):
            o, e = io.StringIO(), io.StringIO()
            rc = cli(["--repo", fx] + list(extra), o, e)
            return rc, o.getvalue(), e.getvalue()

        def rules(o):
            return [ln.split()[2] for ln in o.splitlines()
                    if ln.startswith(FINDING)]

        @check("st01-clean-registry-zero-findings")
        def _():
            fx = build("clean",
                       [row("S001", "corpus/knowledge/alpha.md"),
                        row("S002", "corpus/knowledge/alpha.md"),
                        row("S003", "corpus/knowledge/beta.md")],
                       {"corpus/knowledge/alpha.md": entry("S001/S002"),
                        "corpus/knowledge/beta.md": entry("S003")})
            rc, o, e = run(fx)
            assert rc == 0, (rc, o, e)
            assert "rows=3 entries=2 findings=0" in o, o

        @check("st02-recheck-path-slash")
        def _():
            fx = build("r1a", [row("S001", "-", recheck="docs/a.md")], {})
            rc, o, e = run(fx)
            assert rc == 1, (rc, o, e)
            assert "FINDING R1 S001 recheck=docs/a.md" in o, o

        @check("st03-recheck-md-no-slash")
        def _():
            fx = build("r1b", [row("S001", "-", recheck="notes.md")], {})
            rc, o, e = run(fx)
            assert rc == 1, (rc, o, e)
            assert "FINDING R1 S001 recheck=notes.md" in o, o

        @check("st04-outside-corpus-note-not-finding")
        def _():
            fx = build("r2", [row("S001", "plans/notes.md")], {})
            rc, o, e = run(fx)
            assert rc == 0, (rc, o, e)  # R2 is a note, never a finding
            assert ("NOTE outside-corpus S001 path=plans/notes.md" in o), o
            assert "FINDING" not in o, o

        @check("st05-usedby-missing-on-disk")
        def _():
            fx = build("r3", [row("S001", "corpus/knowledge/ghost.md")], {})
            rc, o, e = run(fx)
            assert rc == 1, (rc, o, e)
            assert "FINDING R3 S001 path=corpus/knowledge/ghost.md" in o, o

        @check("st06-entry-cites-unacknowledged")
        def _():
            fx = build("r4", [row("S001", "-")],
                       {"corpus/knowledge/alpha.md": entry("S001")})
            rc, o, e = run(fx)
            assert rc == 1, (rc, o, e)
            assert ("FINDING R4 S001 entry=corpus/knowledge/alpha.md" in o), o

        @check("st07-entry-cites-missing-row")
        def _():
            fx = build("r5", [row("S001", "corpus/knowledge/alpha.md")],
                       {"corpus/knowledge/alpha.md": entry("S001 S999")})
            rc, o, e = run(fx)
            assert rc == 1, (rc, o, e)
            assert "FINDING R5 S999 entry=corpus/knowledge/alpha.md" in o, o
            assert "R4" not in o, o

        @check("st08-duplicate-id")
        def _():
            fx = build("r6", [row("S001", "-"), row("S001", "-"),
                              row("S002", "-")], {})
            rc, o, e = run(fx)
            assert rc == 1, (rc, o, e)
            assert "FINDING R6 S001 count=2" in o, o
            assert o.count("R6") == 1, o

        @check("st09-mixed-findings-ordered-exit1")
        def _():
            fx = build("mix", [row("S001", "plans/x.md", recheck="a/b.md"),
                               row("S001", "-")],
                       {"corpus/knowledge/alpha.md": entry("S001")})
            rc, o, e = run(fx)
            assert rc == 1, (rc, o, e)
            assert rules(o) == ["R6", "R1", "R4"], (o,)
            assert "NOTE outside-corpus S001 path=plans/x.md" in o, o

        @check("st10-indent-0-3-parsed-4-ignored")
        def _():
            d = os.path.join(tmp, "ind")
            os.makedirs(os.path.join(d, "corpus", "knowledge"))
            body = (FIX_HEADER
                    + "| S001 | u | docs | A | s | a | t | mined | 2026-11-01"
                      " | 90d | corpus/knowledge/alpha.md |\n"
                    + " | S002 | u | docs | A | s | a | t | mined | 2026-11-01"
                      " | 90d | corpus/knowledge/alpha.md |\n"
                    + "      | S003 | u | docs | A | s | a | t | mined"
                      " | 2026-11-01 | 90d | plans/deep.md |\n"
                    + "### a subsection heading inside the section\n"
                    + "| S004 | u | docs | A | s | a | t | mined | 2026-11-01"
                      " | 90d | corpus/knowledge/alpha.md |\n")
            with open(os.path.join(d, "corpus", "SOURCES.md"), "w",
                      encoding="utf-8") as fh:
                fh.write(body)
            with open(os.path.join(d, "corpus", "knowledge", "alpha.md"),
                      "w", encoding="utf-8") as fh:
                fh.write(entry("S001"))
            rc, o, e = run(d)
            assert "rows=3" in o, o  # 4-space row is indented code, ignored
            assert rc == 0, (rc, o, e)  # a ### heading does not close Registry

        @check("st11-empty-and-spaced-usedby-cells")
        def _():
            spaced = row("S003", "corpus/knowledge/alpha.md ,"
                                 " corpus/knowledge/beta.md")
            fx = build("cells",
                       [row("S001", "\u2014"),          # em-dash: empty
                        row("S002", "-"),               # ASCII hyphen: empty
                        row("S004", ""),                # blank cell: empty
                        spaced],
                       {"corpus/knowledge/alpha.md": entry("S003"),
                        "corpus/knowledge/beta.md": entry("S003")})
            rc, o, e = run(fx)
            assert rc == 0, (rc, o, e)  # empty markers: no R2/R3/R4 noise
            assert "findings=0" in o, o
            assert "path=-" not in o and "NOTE" not in o, o

        @check("st12-missing-registry-exit2")
        def _():
            d = os.path.join(tmp, "noreg")
            os.makedirs(d)
            rc, o, e = run(d)
            assert rc == 2, (rc, o, e)
            assert "SETUP missing-registry" in e, e

        @check("st13-unreadable-entry-exit2")
        def _():
            d = os.path.join(tmp, "bad")
            make_repo(d, [row("S001", "corpus/knowledge/alpha.md")], {})
            with open(os.path.join(d, "corpus", "knowledge", "alpha.md"),
                      "wb") as fh:
                fh.write(b"source: S001\n\xff\xfe not utf-8\n")
            rc, o, e = run(d)
            assert rc == 2, (rc, o, e)
            assert "SETUP unreadable-entry" in e, e

        @check("st14-json-shape")
        def _():
            fx = build("js", [row("S001", "-")],
                       {"corpus/knowledge/alpha.md": entry("S001")})
            rc, o, e = run(fx, ["--json"])
            assert rc == 1, (rc, o, e)
            obj = json.loads(o)
            assert set(obj) == {"rows", "entries", "findings"}, obj
            assert obj["rows"] == 1 and obj["entries"] == 1, obj
            f0 = obj["findings"][0]
            assert set(f0) == {"rule", "id", "detail"}, f0
            assert f0["rule"] == "R4" and f0["id"] == "S001", f0

        @check("st15-slash-pair-ids-both-acked")
        def _():
            fx = build("pair", [row("S001", "corpus/knowledge/alpha.md"),
                                row("S002", "corpus/knowledge/alpha.md")],
                       {"corpus/knowledge/alpha.md": entry("S001/S002")})
            rc, o, e = run(fx)
            assert rc == 0 and "entries=1 findings=0" in o, (rc, o, e)
            # and the unacked half of a pair fires
            fx2 = build("pair2", [row("S001", "corpus/knowledge/alpha.md"),
                                  row("S002", "-")],
                        {"corpus/knowledge/alpha.md": entry("S001/S002")})
            rc, o, e = run(fx2)
            assert rc == 1, (rc, o, e)
            assert "FINDING R4 S002" in o, o

        @check("st16-yaml-list-frontmatter")
        def _():
            fx = build("yaml", [row("S001", "corpus/knowledge/alpha.md"),
                                row("S002", "-")],
                       {"corpus/knowledge/alpha.md":
                        "---\nauthor: fixture\nsource:\n  - S001\n  - S002\n"
                        "---\n\n# fixture entry (yaml list)\n"})
            rc, o, e = run(fx)
            assert rc == 1, (rc, o, e)
            # the fence ends the block; both list items counted; S002 unacked
            assert "FINDING R4 S002 entry=corpus/knowledge/alpha.md" in o, o
            assert "S001" not in "".join(rules(o)), o

        @check("st17-wrapped-source-line")
        def _():
            fx = build("wrap", [row("S001", "corpus/knowledge/alpha.md"),
                                row("S002", "-")],
                       {"corpus/knowledge/alpha.md":
                        "source: S001,\n  held S002 (fixture wrap)\n"
                        "verified-at: 2026-11-01\n\n# fixture entry\n"})
            rc, o, e = run(fx)
            assert rc == 1, (rc, o, e)
            # the wrapped continuation id counts; the key line ends the block
            assert "FINDING R4 S002 entry=corpus/knowledge/alpha.md" in o, o
            assert "S001" not in "".join(rules(o)), o

        @check("st18-path-token-not-a-citation")
        def _():
            fx = build("ptok",
                       [row("S213", "-"), row("S214", "-"),
                        row("S215", "corpus/knowledge/alpha.md")],
                       {"corpus/knowledge/alpha.md":
                        "source: see .ufo/waves/round-37/fetch/S213.receipt.txt"
                        " and S214-x for bytes; acked S215\n\n# fixture\n"})
            rc, o, e = run(fx)
            assert rc == 0, (rc, o, e)  # S213/S214 mentions are not citations
            assert "findings=0" in o, o

        @check("st19-status-aware-r4")
        def _():
            fx = build("status",
                       [row("S001", "-"),
                        row("S002", "-", status="rejected"),
                        row("S003", "-", status="queued")],
                       {"corpus/knowledge/alpha.md": entry("S001 S002 S003")})
            rc, o, e = run(fx)
            assert rc == 1, (rc, o, e)
            # only the mined row's unacknowledged citation fires
            assert rules(o) == ["R4"] and "R4 S001" in o, o
            assert "R4 S002" not in o and "R4 S003" not in o, o

        @check("st20-normpath-ack")
        def _():
            fx = build("norm", [row("S001", "corpus/knowledge/./alpha.md")],
                       {"corpus/knowledge/alpha.md": entry("S001")})
            rc, o, e = run(fx)
            assert rc == 0, (rc, o, e)  # normpath(cell) names the entry
            assert "findings=0" in o, o

        @check("st21-no-source-line-after-block")
        def _():
            fx = build("later", [row("S001", "corpus/knowledge/alpha.md")],
                       {"corpus/knowledge/alpha.md":
                        "source: S001\n\n# fixture\n\nbody provenance note:\n\n"
                        "source: S999\n"})
            rc, o, e = run(fx)
            assert rc == 0, (rc, o, e)  # the later source: line is not a block
            assert "findings=0" in o, o

        failed = []
        for cid, fn in checks:
            try:
                fn()
            except AssertionError as exc:
                failed.append(cid)
                err.write(SELFTEST_FAIL_LINE % cid
                          + (" %s" % (exc,) if str(exc) else "") + "\n")
            except Exception as exc:  # noqa: BLE001 - report and continue
                failed.append(cid)
                err.write(SELFTEST_FAIL_LINE % cid + " %r\n" % (exc,))
    finally:
        tmpobj.__exit__(None, None, None)
    out.write(SELFTEST_OK_LINE % (len(checks), len(failed)) + "\n")
    return 1 if failed else 0


def main(argv=None):
    out = sys.stdout
    err = sys.stderr
    return cli(sys.argv[1:] if argv is None else argv, out, err)


if __name__ == "__main__":
    sys.exit(main())
