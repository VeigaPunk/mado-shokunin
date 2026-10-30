#!/usr/bin/env python3
"""counter_killers.py -- the kill fixtures for the survivors of the C3 counter mutation sweep.

Each fixture is a MUTATION OF A TREE (a registry row edit, an entry edit, a used-by cell edit, an allowlist
edit or a frozen-tables edit) committed to a scratch clone of the tip tree.  On that tree the PRISTINE counter
must satisfy a stated predicate; the MUTANT counter must violate it.  The predicate is one of:

  * a frozen leg must appear in `missed=`   ("the counter must print the leg in missed=")
  * a frozen population number must be right (`entries=`, `rows=`, `missing=`)
  * the counter must FAIL CLOSED (exit 2, no stdout) when the frozen base objects do not match the frozen hash

The fixture file for each entry is written under fixtures/counter/<id>.json (the recipe) so the fixture is
reproducible from the deliverable alone; the driver materializes it in the scratch clone.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures", "counter")

TABLES = ".ufo/waves/round-56/frozen-tables-v2.json"
ALLOW = ".ufo/waves/round-56/c3-name-only.tsv"
SOURCES = "corpus/SOURCES.md"


# --------------------------------------------------------------------------------------- helpers on a checkout
def read(p):
    with open(p, "rb") as fh:
        return fh.read()


def write(p, data):
    with open(p, "wb") as fh:
        fh.write(data)


def registry_rows(text):
    """[(line_index, row_id, used_by_cell_text)] over every registry row."""
    out = []
    for i, ln in enumerate(text.split("\n")):
        m = re.match(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|", ln)
        if m:
            cells = ln.split("|")
            out.append((i, m.group(1), cells[11]))
    return out


def cell_paths(cell):
    """the used-by paths of a cell (the separator is ', ' after the round-56 E13 errata)."""
    return [p.strip() for p in cell.split(",") if p.strip()]


def set_cell(text, row_id, new_cell):
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        if re.match(r"^ {0,3}\|\s*%s\s*\|" % re.escape(row_id), ln):
            parts = ln.split("|")
            parts[11] = new_cell
            lines[i] = "|".join(parts)
            return "\n".join(lines)
    raise KeyError(row_id)


def drop_path(cell, path):
    """the cell with `path` removed (comma-separated, per the E13 errata)."""
    keep = [p for p in cell_paths(cell) if p != path]
    return " " + ", ".join(keep) + " " if keep else " - "


def drop_row(text, row_id):
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        if re.match(r"^ {0,3}\|\s*%s\s*\|" % re.escape(row_id), ln):
            del lines[i]
            return "\n".join(lines)
    raise KeyError(row_id)


def add_row(text, row_id):
    row = "| %s | src %s | docs | A | scope | anchor | teaches | mined | 2026-10-30 | 2027-01-01 | - |" % (row_id, row_id)
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        if re.match(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|", ln):
            lines.insert(i, row)
            return "\n".join(lines)
    raise KeyError("no registry row to insert before")


# --------------------------------------------------------------------------------------- the fixtures
# each fixture: id -> (description, mutate(checkout_dir, ctx) -> None, predicate(line, rc) -> (ok, why))
def fx_CM01(checkout, ctx):
    """registry/used-by edit: the allowlisted pair (S005, output-colour-boundaries-r14.md) is back-referenced.

    The frozen `conflict` leg must fire: the pair is on the frozen allowlist AND its entry is now in the
    used-by cell of S005 (the cell is APPENDED to, so no other pair changes)."""
    text = read(os.path.join(checkout, SOURCES)).decode("utf-8", "surrogateescape")
    rows = dict((r[1], r[2]) for r in registry_rows(text))
    cell = rows["S005"]
    paths = cell_paths(cell)
    if "corpus/knowledge/output-colour-boundaries-r14.md" not in paths:
        paths.append("corpus/knowledge/output-colour-boundaries-r14.md")
    new = set_cell(text, "S005", " " + ", ".join(paths) + " ")
    write(os.path.join(checkout, SOURCES), new.encode("utf-8", "surrogateescape"))


def fx_CM03(checkout, ctx):
    """allowlist edit: one allowlist row is removed -> the frozen `exempt` count (24) no longer holds."""
    p = os.path.join(checkout, ALLOW)
    lines = read(p).decode("utf-8", "surrogateescape").split("\n")
    lines = [l for l in lines if l]
    write(p, ("\n".join(lines[:-1]) + "\n").encode("utf-8", "surrogateescape"))


def fx_CM04(checkout, ctx):
    """frozen-tables edit: a harmless extra key -> the tables blob no longer matches the embedded sha256."""
    p = os.path.join(checkout, TABLES)
    d = json.loads(read(p).decode("utf-8"))
    d["_kill_fixture_CM04"] = "the frozen tables blob must hash to the embedded sha256"
    write(p, (json.dumps(d, indent=1) + "\n").encode("utf-8", "surrogateescape"))


def _insert_source_line(checkout, entry_rel, at_index, token):
    """entry edit: put `source: <token>` at line index `at_index` (0-based) of an entry."""
    p = os.path.join(checkout, entry_rel)
    lines = read(p).decode("utf-8", "surrogateescape").split("\n")
    if at_index > len(lines):
        lines += [""] * (at_index - len(lines))
    lines.insert(at_index, "source: %s" % token)
    write(p, "\n".join(lines).encode("utf-8", "surrogateescape"))


def fx_CM06(checkout, ctx):
    """entry edit: a `source:` line at index 15 (line 16) -- one line past the frozen 15-line SRC window."""
    _insert_source_line(checkout, "corpus/knowledge/arc-synthesis.md", 15, "S999")


def fx_CM07(checkout, ctx):
    """entry edit: a `source:` line at index 25 (line 26) -- past the frozen window and past a 16-line window."""
    _insert_source_line(checkout, "corpus/knowledge/arc-synthesis.md", 25, "S999")


def fx_CM08(checkout, ctx):
    """entry edit: a two-digit S id on a `source:` line inside the window.

    The frozen token rule reads exactly three digits, so S38 is not a citation and no dangling fires; a widened
    token rule reads it as a citation and reports a dangling that does not exist."""
    p = os.path.join(checkout, "corpus/knowledge/arc-synthesis.md")
    lines = read(p).decode("utf-8", "surrogateescape").split("\n")
    lines.insert(2, "source: S38")
    write(p, "\n".join(lines).encode("utf-8", "surrogateescape"))


def fx_CM11(checkout, ctx):
    """entry edit: one more corpus/knowledge/*.md entry -> the reported entry population must grow by one."""
    write(os.path.join(checkout, "corpus/knowledge/kill-fixture-extra-r56.md"),
          b"# kill fixture\n\nAn extra entry file for the CM11 population check.\n")


def fx_CM12(checkout, ctx):
    """registry edit: one more registry row -> the reported row population must grow by one."""
    p = os.path.join(checkout, SOURCES)
    text = read(p).decode("utf-8", "surrogateescape")
    write(p, add_row(text, "S999").encode("utf-8", "surrogateescape"))


def fx_CM19(checkout, ctx):
    """frozen-tables edit: `base_rev` points at a commit whose base pairs do not hash to the frozen value.

    The counter must FAIL CLOSED (setup error, exit 2, nothing on stdout)."""
    p = os.path.join(checkout, TABLES)
    d = json.loads(read(p).decode("utf-8"))
    d["c3"]["base_rev"] = ctx["base_rev"]
    write(p, (json.dumps(d, indent=1) + "\n").encode("utf-8", "surrogateescape"))


def fx_CM25(checkout, ctx):
    """used-by edit: two back-referenced pairs lose their used-by entry -> `missing` must be 2, not 1."""
    p = os.path.join(checkout, SOURCES)
    text = read(p).decode("utf-8", "surrogateescape")
    for sid, entry in ctx["two_pairs"]:
        rows = dict((r[1], r[2]) for r in registry_rows(text))
        text = set_cell(text, sid, drop_path(rows[sid], entry))
    write(p, text.encode("utf-8", "surrogateescape"))


def fx_CM28(checkout, ctx):
    """registry edit: the registry row S005 is deleted while the frozen allowlist still lists it.

    The pair (S005, output-colour-boundaries-r14.md) is no longer a cited pair, so the frozen `stale` leg must
    fire; a counter that filters the allowlist to known row ids cannot see it."""
    p = os.path.join(checkout, SOURCES)
    text = read(p).decode("utf-8", "surrogateescape")
    write(p, drop_row(text, "S005").encode("utf-8", "surrogateescape"))


# --------------------------------------------------------------------------------------- predicates
def _parse(line):
    m = re.search(r" missing=(\d+) extra=(\d+) dangling=(\d+) conflict=(\d+) stale=(\d+) lost=(\d+) "
                  r"exempt=(\d+) verdict=(\S+) missed=(\S+)$", line)
    if not m:
        return None
    g = m.groups()
    return {"missing": int(g[0]), "extra": int(g[1]), "dangling": int(g[2]), "conflict": int(g[3]),
            "stale": int(g[4]), "lost": int(g[5]), "exempt": int(g[6]), "verdict": g[7], "missed": g[8]}


def pred_leg(leg):
    def f(line, rc):
        d = _parse(line)
        if d is None:
            return False, "no parsable MADO_USED_BY line (rc=%s)" % rc
        legs = [] if d["missed"] == "none" else d["missed"].split(",")
        if leg not in legs:
            return False, "missed=%s does not carry the leg %s" % (d["missed"], leg)
        return True, "missed=%s carries %s" % (d["missed"], leg)
    return f


def pred_count(field, value):
    def f(line, rc):
        d = _parse(line)
        if d is None:
            return False, "no parsable MADO_USED_BY line (rc=%s)" % rc
        if d[field] != value:
            return False, "%s=%s, expected %s" % (field, d[field], value)
        return True, "%s=%s" % (field, value)
    return f


def pred_fail_closed(line, rc):
    if rc == 2 and not line.strip():
        return True, "exit 2 with no stdout (fail closed)"
    return False, "rc=%s stdout=%r (the counter must fail closed)" % (rc, line.strip()[:120])


def pred_CM28(line, rc):
    """the frozen allowlist row of a registry row that no longer exists must stay in the exemption map.

    The pristine counter keeps all 24 allowlist rows (exempt=24) and reports the row as stale; a counter that
    filters the allowlist to known row ids drops the row, so the exemption count is wrong (exempt=1) and the
    staleness is invisible."""
    d = _parse(line)
    if d is None:
        return False, "no parsable MADO_USED_BY line (rc=%s)" % rc
    legs = [] if d["missed"] == "none" else d["missed"].split(",")
    if d["exempt"] != 24:
        return False, "exempt=%s, expected 24 (the frozen allowlist has 24 rows)" % d["exempt"]
    if "stale" not in legs:
        return False, "missed=%s does not carry the leg stale" % d["missed"]
    return True, "missed=%s exempt=24" % d["missed"]


FIXTURES = {
    "CM01": {"kind": "registry/used-by edit", "desc": "the allowlisted pair (S005, output-colour-boundaries-r14.md) is back-referenced",
             "mutate": fx_CM01, "predicate": pred_leg("conflict")},
    "CM03": {"kind": "allowlist edit", "desc": "one allowlist row is removed (23 rows instead of 24)",
             "mutate": fx_CM03, "predicate": pred_leg("exempt")},
    "CM04": {"kind": "frozen-tables edit", "desc": "the frozen tables blob no longer matches its embedded sha256",
             "mutate": fx_CM04, "predicate": pred_leg("tables_sha")},
    "CM06": {"kind": "entry edit", "desc": "a `source:` line at line 16 (one past the frozen 15-line SRC window)",
             "mutate": fx_CM06, "predicate": pred_count("dangling", 0)},
    "CM07": {"kind": "entry edit", "desc": "a `source:` line at line 26 (past the frozen 15-line SRC window)",
             "mutate": fx_CM07, "predicate": pred_count("dangling", 0)},
    "CM08": {"kind": "entry edit", "desc": "a two-digit S id on a `source:` line inside the window",
             "mutate": fx_CM08, "predicate": pred_count("dangling", 0)},
    "CM11": {"kind": "entry edit", "desc": "one more corpus/knowledge/*.md entry (population must grow)",
             "mutate": fx_CM11, "predicate": None},
    "CM12": {"kind": "registry edit", "desc": "one more registry row (population must grow)",
             "mutate": fx_CM12, "predicate": None},
    "CM19": {"kind": "frozen-tables edit", "desc": "base_rev points at a commit whose base pairs do not match the frozen hash",
             "mutate": fx_CM19, "predicate": pred_fail_closed},
    "CM25": {"kind": "used-by edit", "desc": "two back-referenced pairs lose their used-by entry (missing must be 2)",
             "mutate": fx_CM25, "predicate": pred_count("missing", 2)},
    "CM28": {"kind": "registry edit", "desc": "registry row S005 is deleted while the frozen allowlist still lists it",
             "mutate": fx_CM28, "predicate": pred_CM28},
}

# CM27 (the resolved-revision name check accepts 39 hex characters instead of 40) has no reachable fixture:
# the sha comes from `git rev-parse --verify <rev>^{commit}`, which always prints 40 (or 64) hex characters.
# The attempt is recorded in the report; the difference is only reachable with a forged git, which is not an
# input of the claim.  See suite/probe_cm27.py for the attempt.
NO_FIXTURE_NOTE = {
    "CM27": "the mutant widens the accepted resolved-revision name from 40 to 39 hex characters; the name comes "
            "from `git rev-parse --verify <rev>^{commit}`, which prints 40 (or 64) hex characters, so no "
            "registry/entry/used-by mutation reaches the difference (attempt recorded in receipts/kill-c3.txt)",
}
