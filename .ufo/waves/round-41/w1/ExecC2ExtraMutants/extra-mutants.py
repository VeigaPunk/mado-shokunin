#!/usr/bin/env python3
"""Round-41 C2 EXTRA mutants: blind spots of PRED-C2-r41-v1 beyond the frozen
41 controls.

Imports the frozen control runner (importlib, its main is guarded) and reuses
its admitted fixture `G`, its row/gate/receipt builders and its `score()`
recipe verbatim: D=mktemp -d, `git -C D init -q`, toplevel verified equal to D
before the first commit, throwaway identity passed with -c, counter run as
`python3 -I quality/counters/c2-r41-focus-entry.py --repo D --rev A --base B`.

Only delta from the frozen `score()`: a `links` mapping that creates git
symlinks after the regular files are written and before `git add -A` (the
symlink-receipt mutant cannot be expressed by the frozen writer). Everything
else is byte-identical in construction.

Usage: python3 extra-mutants.py [--only NAME ...]
Final line: `CTL_C2_EXTRA: mutants=N survivors=K/N`.
"""
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
CTL = os.path.join(LANE, ".ufo/waves/round-41/ctl", "run-c2-controls.py")
COUNTER = os.path.join(LANE, "quality", "counters", "c2-r41-focus-entry.py")

_spec = importlib.util.spec_from_file_location("ctlc2r41", CTL)
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)  # module level only; main() is __main__-guarded

ENV = C.ENV
ENTRY = C.ENTRY
SRC = C.SRC
LES = C.LES
FETCH = C.FETCH
Q = C.QUOTES
FILLER = C.FILLER
FG = C.FG
row = C.row
gate_line = C.gate_line
set_receipt = C.set_receipt
with_journal = C.with_journal
journal = C.journal
jline = C.jline
receipt_text = C.receipt_text
sha = C.sha

BASE = C.base_files()
G = C.admitted()


def commit_all(d, files, msg, links=None):
    for rel, text in files.items():
        path = os.path.join(d, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="") as fh:
            fh.write(text)
    for rel, target in (links or {}).items():
        path = os.path.join(d, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.lexists(path):
            os.remove(path)
        os.symlink(target, path)
    ident = ["-c", "user.name=ctl", "-c", "user.email=ctl@ctl.invalid"]
    subprocess.run(["git", "-C", d, "add", "-A"], check=True, env=ENV)
    subprocess.run(["git", "-C", d, *ident, "commit", "-q", "-m", msg,
                    "--no-gpg-sign"], check=True, env=ENV)
    return subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True,
                          env=ENV).stdout.strip()


def score(files_base, files_after, links_after=None):
    """The frozen score() recipe, plus symlink support."""
    d = tempfile.mkdtemp(prefix="mado-c2r41x-")
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True, env=ENV)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             check=True, capture_output=True, text=True,
                             env=ENV).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise SystemExit("fixture toplevel mismatch: %s != %s" % (top, d))
        b = commit_all(d, files_base, "base")
        a = commit_all(d, files_after, "after", links_after)
        p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", d,
                            "--rev", a, "--base", b],
                           capture_output=True, text=True, env=ENV)
        lines = p.stdout.strip().splitlines()
        cls = [l for l in lines if " clauses=" in l]
        clauses = cls[0].split(" clauses=")[1].split(" admitted")[0] if cls else "-"
        last = lines[-1] if lines else "NO-OUTPUT"
        return p.returncode, last, clauses, p.stdout
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ---------------------------------------------------------------- base variants
ROW51 = ("| S051 | held hyprland protocols readme - https://example.org/proto | "
         "docs | A | scope | anchor | teaches | mined | 2026-10-24 | on-change | "
         "corpus/knowledge/old.md |")


def base_two_held():
    """base + a second held row, so a 4-citation entry can carry only 2 new ids."""
    f = C.base_files()
    f[SRC] = f[SRC].replace(C.HELD_ROW, C.HELD_ROW + "\n" + ROW51)
    return f


def g_two_new():
    """admitted set with 4 cited ids of which only TWO are new (docstring wants >=3)."""
    g = base_two_held()
    q51 = "hyprland protocols readme lists the focus grab xml"
    g[SRC] = g[SRC].replace(ROW51, ROW51 + "\n" + "\n".join([
        row("S301", "https://example.org/a.xml"),
        row("S302", ".ufo/waves/round-41/fetch/S302.journal.txt",
            kind="own-work")]))
    g[SRC] = g[SRC].replace("| on-change | corpus/knowledge/old.md |",
                            "| on-change | corpus/knowledge/old.md, %s |" % ENTRY)
    g[FETCH + "S050.txt"] = receipt_text("S050")
    g[FETCH + "S051.txt"] = "%s source bytes for S051. %s\n" % (q51, FILLER)
    g[FETCH + "S301.html"] = receipt_text("S301")
    g[FETCH + "S302.journal.txt"] = receipt_text("S302")
    gates = [gate_line(i, FETCH + fn, g[FETCH + fn], q)
             for i, fn, q in (("S050", "S050.txt", Q["S050"]),
                              ("S051", "S051.txt", q51),
                              ("S301", "S301.html", Q["S301"]),
                              ("S302", "S302.journal.txt", Q["S302"]))]
    g[LES] = ("# round 41\n\n## Gate\n\n" + "\n".join(gates) + "\n" + C.ADMIT
              + "\n" + C.REFUSE + "\n")
    g[ENTRY] = "\n".join([
        "# The focus-grab protocol", "",
        "source: S050 - held parser", "source: S051 - protocols readme",
        "source: S301 - protocol xml", "source: S302 - own-work journal",
        "verified-at: 2026-10-25", "recheck: 90d", "",
        "**OBS** S050 %s." % Q["S050"],
        "**OBS** S051 %s." % q51,
        "**OBS** S301 %s." % Q["S301"],
        "**OBS** S302 %s." % Q["S302"], "", C.JLINE, ""]) + "\n"
    g["corpus/README.md"] += "| `knowledge/hyprland-focus-grab-r41.md` | new |\n"
    return g


# ---------------------------------------------------------------- mutants
MUTANTS = []


def mut(name, expect, fn, base_key="G", why=""):
    MUTANTS.append({"name": name, "expect": expect, "fn": fn,
                    "base": base_key, "why": why})


def gate_of(g, i):
    return [l for l in g[LES].splitlines() if l.startswith("GATE %s " % i)][0]


# ---- survivors expected -------------------------------------------------
def m01(g):  # a 5th citation past line 20, no registry row, no gate line
    g[ENTRY] += ("\nprose a\nprose b\nprose c\nprose d\n"
                 "source: S305 - extra citation with no registry row\n")


def m02(g):  # a cited id in lowercase: invisible to SRC_RE and ROW_RE
    g[ENTRY] = g[ENTRY].replace("source: S304 - docs", "source: s304 - docs")
    g[SRC] = g[SRC].replace("| S304 |", "| s304 |")


def m03(g):  # two entry lines carry the same id's quote
    q = Q["S301"]
    g[ENTRY] = g[ENTRY].replace("**OBS** S301 %s." % q,
                                "**OBS** S301 %s.\n**OBS** S301 %s." % (q, q))


def m04(g):  # ONE line serves two ids (nested quotes, distinct raw strings)
    q3 = "grab manager interface commit"
    t3 = "%s source bytes for S303. %s\n" % (q3, FILLER)
    set_receipt(g, "S303", "S303.txt", t3, q3)
    e = g[ENTRY].replace("**OBS** S301 %s.\n" % Q["S301"], "")
    e = e.replace("**OBS** S303 %s." % Q["S303"],
                  "**OBS** S301 S303 %s." % Q["S301"])
    assert "**OBS** S301 S303" in e
    g[ENTRY] = e


def m05(g):  # quote assembled across two <p> blocks; not contiguous in the bytes
    a, b = "hyprland focus grab manager", "interface commit request"
    assert Q["S301"] == a + " " + b
    t = "<html><body><p>%s</p> <p>%s</p> %s</body></html>" % (a, b, FILLER)
    assert Q["S301"] not in t
    set_receipt(g, "S301", "S301.html", t, Q["S301"])


def m06(g):  # a conflicting second GATE line outside the ## Gate section
    bogus = ('GATE S301 receipt=%sS301.html sha256=%s '
             'quote="a stale gate line outside the gate section"'
             % (FETCH, "0" * 64))
    g[LES] = g[LES].replace(C.REFUSE, C.REFUSE + "\n\n## Receipts\n\n" + bogus)


def m07(g):  # receipt path with a dot segment (git refuses to resolve it)
    g[LES] = g[LES].replace("receipt=%sS301.html" % FETCH,
                            "receipt=%s./S301.html" % FETCH)


def m08(g):  # receipt is a git symlink: 530-byte target string, not source bytes
    target = "pad/" * 120 + Q["S301"]
    assert len(target) >= 512  # the counter's MIN_RECEIPT
    path = FETCH + "S301.link.txt"
    g[LES] = g[LES].replace(gate_of(g, "S301"),
                            gate_line("S301", path, target, Q["S301"]))
    return {path: target}


def m09(g):  # new row whose recheck cell is prose
    r = row("S301", "https://example.org/a.xml")
    g[SRC] = g[SRC].replace(r, r.replace("| 90d |", "| TBD |"))


def m10(g):  # new row with no locatable source at all
    g[SRC] = g[SRC].replace(row("S304", "https://example.org/d.md"),
                            row("S304", "focus control surfaces"))


def m11(g):  # excluded localized channel in the anchor cell, cell 1 clean
    r = row("S304", "https://example.org/d.md")
    g[SRC] = g[SRC].replace(
        r, r.replace("| anchor |", "| https://amgsk.dev/posts/hyprland-rules/ |"))


def m12(g):  # quote distinct only in whitespace from another id's quote
    q4 = "hyprland  focus grab manager interface commit request"
    t4 = "%s source bytes for S304. %s\n" % (q4, FILLER)
    set_receipt(g, "S304", "S304.txt", t4, q4)
    g[ENTRY] = g[ENTRY].replace(Q["S304"], q4)


def m13(g):  # REFUSE reason of exactly 20 filler characters
    g[LES] = g[LES].replace(
        "reason=generic wayland security analysis, not a measurement",
        "reason=" + "a" * 20)


def m14(g):  # self-admit: the entry admitted as itself
    g[LES] = g[LES].replace(C.ADMIT, "ADMIT %s as %s" % (ENTRY, ENTRY))


def m15(g):  # admit names a package path that does not exist
    g[LES] = g[LES].replace(
        C.ADMIT,
        "ADMIT merge/mado/knowledge/corpus/knowledge/does-not-exist-r99.md as "
        + ENTRY)


def m16(g):  # no BOOT line at all: sessions only from PID change
    with_journal(g, journal(sessions=3, boots=False))


def m17(g):  # the same session block replayed three times with different PIDs
    one = journal(sessions=1, boots=False)
    with_journal(g, one + one.replace("[1900]", "[1901]")
                 + one.replace("[1900]", "[1902]"))


def m18(g):  # quote matches only after html.unescape of a plain-text receipt
    t = "&#104;yprland focus grab manager interface commit request " + FILLER
    assert Q["S301"] not in t
    set_receipt(g, "S301", "S301.html", t, Q["S301"])


def m19(g):  # recheck: an impossible ISO date
    g[ENTRY] = g[ENTRY].replace("recheck: 90d", "recheck: 2026-99-99")


def m20(g):  # verified-at/recheck satisfied by a fenced block in the head
    e = g[ENTRY].replace("verified-at: 2026-10-25",
                         "verified-at: 2026-10-23").replace(
        "recheck: 90d", "recheck: whenever")
    e = e.replace("# The focus-grab protocol\n",
                  "# The focus-grab protocol\n\n```\nverified-at: 2026-10-25\n"
                  "recheck: 90d\n```\n", 1)
    g[ENTRY] = e


def m21(g):  # a held row LOSES its pre-existing used-by item (substitution)
    g[SRC] = g[SRC].replace("corpus/knowledge/old.md, " + ENTRY, ENTRY)


def m22(g):  # 4 cited ids but only 2 new (docstring c says at least 3)
    g.clear()
    g.update(g_two_new())


def m23(g):  # ADMIT inside a fence in ## Gate still counts
    g[LES] = g[LES].replace(C.ADMIT + "\n", "```\n" + C.ADMIT + "\n```\n")


def m24(g):  # every GATE line inside its own fence still counts
    out = []
    for line in g[LES].splitlines():
        out += ["```", line, "```"] if line.startswith("GATE ") else [line]
    g[LES] = "\n".join(out) + "\n"


def m25(g):  # REFUSE the same package the ADMIT admits
    g[LES] = g[LES].replace("REFUSE " + C.PKG2, "REFUSE " + C.PKG)


def m26(g):  # new row whose location is the same document as another row
    g[SRC] = g[SRC].replace(row("S304", "https://example.org/d.md"),
                            row("S304", "https://example.org/a.xml#frag"))


def m27(g):  # a source: line inside a fence in the head counts as a citation
    g[ENTRY] = g[ENTRY].replace("source: S304 - docs\n",
                                "```\nsource: S304 - docs\n```\n")


def m28(g):  # one source: line moved past line 20 silently leaves the id set
    e = g[ENTRY].replace("source: S304 - docs\n", "")
    g[ENTRY] = e + "\nfa\nfb\nfc\nfd\nsource: S304 - docs\n"


def m29(g):  # the same id cited twice in the head (dedupe by design)
    g[ENTRY] = g[ENTRY].replace("source: S301 - protocol xml\n",
                                "source: S301 - protocol xml\n"
                                "source: S301 - protocol xml\n")


def m30(g):  # the quote is split by a line break inside the receipt
    t = ("hyprland focus grab\nmanager interface commit request " + FILLER)
    assert Q["S301"] not in t
    set_receipt(g, "S301", "S301.html", t, Q["S301"])


# ---- expected to be killed (teeth) --------------------------------------
def k01(g):  # 10-cell row
    r = row("S301", "https://example.org/a.xml")
    r10 = ("| S301 | title - https://example.org/a.xml | docs | A | scope | "
           "anchor | teaches | mined | 2026-10-25 | %s |" % ENTRY)
    g[SRC] = g[SRC].replace(r, r10)


def k02(g):  # quote case differs from the receipt
    g[LES] = g[LES].replace('quote="%s"' % Q["S301"],
                            'quote="%s"' % Q["S301"].title())


def k03(g):  # GATE line with an extra field after the quote
    g[LES] = g[LES].replace(gate_of(g, "S301"), gate_of(g, "S301") + " extra=1")


def k04(g):  # REFUSE reason of exactly 19 characters
    g[LES] = g[LES].replace(
        "reason=generic wayland security analysis, not a measurement",
        "reason=" + "a" * 19)


def k05(g):  # verified-at/recheck in the second 20 lines
    e = g[ENTRY].replace("verified-at: 2026-10-25\n", "").replace(
        "recheck: 90d\n", "")
    g[ENTRY] = e + "\nfa\nfb\nfc\nfd\nverified-at: 2026-10-25\nrecheck: 90d\n"


def k06(g):  # TWO source: lines moved past line 20 (only 3 ids left)
    e = g[ENTRY].replace("source: S303 - client source\n", "").replace(
        "source: S304 - docs\n", "")
    g[ENTRY] = (e + "\nfa\nfb\nfc\nfd\nsource: S303 - client source\n"
                "source: S304 - docs\n")


def k07(g):  # [LOG] | with a single space: nothing parses
    t = C.JTEXT.replace("[LOG]  |", "[LOG] |")
    set_receipt(g, "S302", "S302.journal.txt", t + "\n# " + Q["S302"] + "\n")


def k08(g):  # the focus-grab advert only in an earlier session
    lines = journal(sessions=3, focus=False).split("\n")
    lines.insert(1, C.advert("2026-10-25T13:10:00-03:00", "1900", FG))
    with_journal(g, "\n".join(lines))


def k09(g):  # row indented 4 spaces (outside the 0-3 rule)
    r = row("S301", "https://example.org/a.xml")
    g[SRC] = g[SRC].replace(r, "    " + r)


def k10(g):  # two README index rows for the entry
    g["corpus/README.md"] += "| `knowledge/hyprland-focus-grab-r41.md` | dup |\n"


def k11(g):  # two new rows of kind own-work
    g[SRC] = g[SRC].replace(row("S301", "https://example.org/a.xml"),
                            row("S301", "https://example.org/a.xml",
                                kind="own-work"))


def k12(g):  # census line with two spaces after `journal`
    g[ENTRY] = g[ENTRY].replace(C.JLINE, C.JLINE.replace("journal ", "journal  "))


def k13(g):  # the only ADMIT names a package path containing spaces
    g[LES] = g[LES].replace(
        C.ADMIT,
        "ADMIT merge/mado/knowledge/corpus/knowledge/focus control surfaces "
        "r28.md as " + ENTRY)


def k14(g):  # receipt path with a `..` segment
    g[LES] = g[LES].replace("receipt=%sS301.html" % FETCH,
                            "receipt=%s../fetch/S301.html" % FETCH)


def k15(g):  # the README index row names a different entry
    g["corpus/README.md"] = g["corpus/README.md"].replace(
        "| `knowledge/hyprland-focus-grab-r41.md` | new |",
        "| `knowledge/other.md` | new |")


for _n, _f, _w in [
    ("M01-citation-past-line-20", m01,
     "c: every cited id needs exactly one row (a source: line at line 23 is a citation)"),
    ("M02-cited-id-lowercase", m02,
     "b/c: a lowercase id is a citation the counter never sees, so no row is required"),
    ("M03-two-entry-lines-per-id", m03,
     "g: 'one entry line' per id (counter uses any())"),
    ("M04-one-line-serves-two-ids", m04,
     "g: one line per id (nested quotes let one line satisfy two ids)"),
    ("M05-quote-across-paragraphs", m05,
     "d: the quote must occur contiguously in the receipt (norm() joins <p> blocks)"),
    ("M06-gate-line-outside-section", m06,
     "d: EXACTLY ONE GATE line per id (a second one outside ## Gate is invisible)"),
    ("M07-receipt-dot-segment", m07,
     "d: the receipt path must resolve under FETCH (git refuses ./ segments)"),
    ("M08-receipt-symlink", m08,
     "d: the receipt must be committed bytes, not a symlink whose blob is a path string"),
    ("M09-new-row-recheck-junk", m09,
     "c: a new row's recheck cell is never validated"),
    ("M10-new-row-no-location", m10,
     "e: cell 1 must end with a locatable source, not a bare word"),
    ("M11-badloc-in-anchor-cell", m11,
     "i: the localized-channel ban must cover the whole row, not only cell 1"),
    ("M12-quote-whitespace-variant", m12,
     "d: quotes must be distinct after normalization, not only as raw strings"),
    ("M13-refuse-reason-20-filler", m13,
     "i: a reason must be prose about the refused entry, not 20 filler chars"),
    ("M14-admit-self", m14,
     "i: the admitted package path must be a staged package, not the entry itself"),
    ("M15-admit-nonexistent-package", m15,
     "i: the admitted package path must exist in the staged package"),
    ("M16-journal-no-boot-line", m16,
     "h: sessions must be separated by a boot boundary, not only a PID change"),
    ("M17-journal-duplicate-sessions", m17,
     "h: replayed blocks with identical timestamps must not count as extra sessions"),
    ("M18-quote-entity-encoded", m18,
     "d: the quote must occur literally in a plain-text receipt (norm() unescapes entities)"),
    ("M19-recheck-impossible-date", m19,
     "b: recheck must be a real date/interval, not any NN-NN-NN shape"),
    ("M20-fenced-verified-at", m20,
     "b: the preamble removes fences before any line is matched; head uses raw lines"),
    ("M21-held-row-usedby-substituted", m21,
     "c: a held row must keep its used-by items and gain the entry (superset)"),
    ("M22-two-new-ids-only", m22,
     "c: docstring says at least 3 new ids; the code accepts >= 2"),
    ("M23-admit-inside-fence", m23,
     "i: the lesson is never unfenced, so a fenced ADMIT counts"),
    ("M24-gate-lines-inside-fence", m24,
     "d: the lesson is never unfenced, so fenced GATE lines count"),
    ("M25-refuse-same-package", m25,
     "i: the refused package must differ from the admitted one"),
    ("M26-location-url-fragment", m26,
     "e: locations must be unique after URL normalization (a fragment is the same document)"),
    ("M27-source-inside-fence", m27,
     "b: the preamble removes fences before any line is matched; a fenced source: counts"),
    ("M28-source-moved-past-line-20", m28,
     "b/c: a citation moved past line 20 leaves the id set and every row/gate check"),
    ("M29-source-id-cited-twice", m29,
     "none: 'distinct' is by design, so this is benign (recorded, not a defect)"),
    ("M30-quote-split-by-newline", m30,
     "none: normalization collapses a wrapped line, so this is benign (recorded)"),
]:
    mut(_n, "admit", _f, why=_w)

for _m in MUTANTS:
    if _m["name"] == "M22-two-new-ids-only":
        _m["base"] = "G2"

for _n, _f, _w in [
    ("K01-ten-cell-row", k01, "c: 11 cells"),
    ("K02-quote-case-differs", k02, "d: quote occurs in the receipt"),
    ("K03-gate-extra-field", k03, "d: GATE line shape"),
    ("K04-refuse-reason-19-chars", k04, "i: reason >= 20 characters"),
    ("K05-verified-at-past-line-20", k05, "b: verified-at within the first 20 lines"),
    ("K06-source-past-line-20", k06, "b: >= 4 distinct source lines in the head"),
    ("K07-journal-single-space-log", k07, "h: ADVERT grammar"),
    ("K08-focus-grab-earlier-session", k08, "h: F is counted in the latest session"),
    ("K09-row-four-space-indent", k09, "c: rows may be indented 0-3 spaces"),
    ("K10-two-readme-rows", k10, "f: exactly one index row"),
    ("K11-two-own-work-rows", k11, "h: exactly one new own-work row"),
    ("K12-journal-line-double-space", k12, "h: census line verbatim"),
    ("K13-admit-path-with-spaces", k13, "i: ADMIT line shape"),
    ("K14-receipt-dotdot-segment", k14, "d: the receipt path must resolve under FETCH"),
    ("K15-readme-row-other-name", k15, "f: exactly one index row for THIS entry"),
]:
    mut(_n, "reject", _f, why=_w)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--json", default=os.path.join(HERE, "results.json"))
    args = ap.parse_args()
    sel = [m for m in MUTANTS if not args.only or m["name"] in args.only]
    base2 = base_two_held()
    G2 = g_two_new()
    rows = []
    # sanity: the unmutated fixtures must be admitted before anything is read
    for tag, (bf, gf) in (("G", (BASE, G)), ("G2", (base2, G2))):
        rc, last, cls, _ = score(bf, gf)
        print("fixture=%s baseline rc=%d %s clauses=%s" % (
            tag, rc, last.split(" verdict")[0], cls))
        rows.append({"name": "baseline-" + tag, "expect": "admit", "rc": rc,
                     "last": last, "clauses": cls, "verdict": "BASELINE"})
    for m in sel:
        bf = BASE if m["base"] == "G" else base2
        g = dict(G) if m["base"] == "G" else dict(G2)
        links = m["fn"](g)
        rc, last, cls, out = score(bf, g, links)
        admitted = "admitted=1/1" in last
        if m["expect"] == "admit":
            ok = rc == 0 and admitted
            verdict = "SURVIVOR" if ok else "killed"
        else:
            ok = rc == 1 and "admitted=0/1" in last
            verdict = "killed" if ok else ("SURVIVOR" if admitted else "odd")
        print("%s expect=%s verdict=%s rc=%d %s clauses=%s" % (
            m["name"], m["expect"], verdict, rc, last.split(" verdict")[0],
            cls))
        rows.append({"name": m["name"], "expect": m["expect"], "why": m["why"],
                     "rc": rc, "last": last, "clauses": cls,
                     "verdict": verdict,
                     "failed": [c for c in cls.split() if c.endswith(":0")]})
    # clause a's guard: entry present at BASE must be a setup error
    b_dup = dict(BASE)
    b_dup[ENTRY] = "already present at base\n"
    rc, last, cls, out = score(b_dup, G)
    setup = rc == 2 and "SETUP" in out
    print("SETUP-entry-present-at-base rc=%d %s ok=%d" % (
        rc, last.split(" rev=")[0], setup))
    rows.append({"name": "SETUP-entry-present-at-base", "expect": "setup",
                 "rc": rc, "last": last, "clauses": cls,
                 "verdict": "setup-guard-ok" if setup else "SETUP-GUARD-BROKEN"})
    with open(args.json, "w") as fh:
        json.dump(rows, fh, indent=1)
    surv = [r for r in rows if r["verdict"] == "SURVIVOR"]
    n = len([r for r in rows if r["expect"] in ("admit", "reject")
             and not r["name"].startswith("baseline-")])
    print("CTL_C2_EXTRA: mutants=%d survivors=%d/%d" % (n, len(surv), n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
