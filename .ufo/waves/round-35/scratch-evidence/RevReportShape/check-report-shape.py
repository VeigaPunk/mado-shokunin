#!/usr/bin/env python3
"""Round-report shape checker for mado round 35 (seat RevReportShape).

Two layers, both quoted from an authority, neither invented:

A. Driver/mechanical predicate = scripts/shokunin-watchdog.sh:report_of (lines 140-163)
   + report_sources_conformance (lines 302-318). Defaults: MIN_REPORT_BYTES=400.
B. Prompt contract = .ufo/prompts/mado-round-35.md section 4 "Report contract"
   (required sections in order + evidence pointer each + marker rule) and
   scripts/hyaku/lane-addendum.md:196 (canonical Stale-lane line, tool installs).

Usage: check-report-shape.py <report.md> [--shonen <SHONEN.md>]
Exit 0 = every checked property holds; 1 = >=1 defect; 2 = usage error.
"""
import re
import sys

MIN_REPORT_BYTES = 400  # scripts/shokunin-watchdog.sh:54 default

# §4 order, exact spellings observed in the lane's own precedent
# (.ufo/reports/round-34/mado.md:9,143,156,192,229,252).
SECTIONS = [
    ("Work performed", r"^#{2,6}[ \t]+Work performed[ \t]*$"),
    ("Landed changes", r"^#{2,6}[ \t]+Landed changes[ \t]*$"),
    ("Before -> after measurements",
     r"^#{2,6}[ \t]+Before[ \t]*(?:→|->)[ \t]*after measurements[ \t]*$"),
    ("Sources & frontier", r"^#{2,6}[ \t]+Sources[ \t]*&[ \t]*frontier[ \t]*$"),
    ("Trend verdicts", r"^#{2,6}[ \t]+Trend verdicts[ \t]*$"),
    ("SHONEN", r"^#{2,6}[ \t]+SHONEN[ \t]*$"),
]

# watchdog report_of lines 145-163, transcribed verbatim (LC_ALL=C semantics).
WATCHDOG_SHONEN = re.compile(
    r"^#+[ \t]*[Ss][Hh](?:[Oo]|Ō|ō)[Nn][Ee][Nn](?:[^A-Za-z0-9_]|$)"
    r"|^[ \t]*-[ \t]+\*\*[Ss][Hh](?:[Oo]|Ō|ō)[Nn][Ee][Nn]\*\*(?:[ \t]|$)",
    re.MULTILINE,
)
WATCHDOG_SOURCES = re.compile(
    r"^#{1,6}[ \t]+sources[ \t]*&[ \t]*frontier(?:[ \t]|$)", re.IGNORECASE | re.MULTILINE
)

PLACEHOLDER = re.compile(
    r"\b(?:TODO|TBD|FIXME|XXX|placeholder|lorem ipsum|<insert|<fill)\b", re.IGNORECASE
)

# An evidence pointer = a path:line, a path with a code/doc extension, a commit-ish
# hex run, or a backticked command.
POINTER = re.compile(
    r"`[^`\n]{3,}`"
    r"|\b[\w./-]+\.(?:md|py|json|txt|sh|mjs|ts|tsv|yml|yaml|cfg|conf)\b"
    r"|\b[0-9a-f]{7,40}\b"
    r"|[\w./-]+:\d+(?:-\d+)?\b"
    r"|\bS\d{3,}\b"  # a corpus/SOURCES.md row id: resolvable inside the lane corpus
)

# lane-addendum.md:196 canonical sentence; decoration (*, -, >) does not change it.
CANONICAL_STALE = "respawn-per-round driver; no other mission of this lane is open"
STALE_ANY = re.compile(r"^[ \t>*-]*\**[ \t]*Stale-lane[ \t]*\**[ \t]*:.*$", re.MULTILINE | re.IGNORECASE)

TREND_AXES = ("expansion", "quality", "discernment")
VERDICTS = ("improved", "harmed", "unchanged", "unprovable-but-better")
SHONEN_BOX = re.compile(r"^[ \t]*-[ \t]*\[([x~ ])\]", re.IGNORECASE | re.MULTILINE)


def split_sections(text):
    """Return [(name, header_line_index, body)] for the six contract sections."""
    lines = text.splitlines()
    starts = {}
    for name, pat in SECTIONS:
        rx = re.compile(pat)
        for i, line in enumerate(lines):
            if rx.match(line):
                starts[name] = i
                break
    found = []
    for name, _ in SECTIONS:
        if name in starts:
            idx = starts[name]
            end = len(lines)
            for other, j in starts.items():
                if j > idx:
                    end = min(end, j)
            found.append((name, idx, "\n".join(lines[idx + 1:end])))
    return found, starts


def check(path, shonen_path):
    defects = []
    notes = []
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError as exc:
        defects.append(("A.exists", f"report absent or unreadable: {exc}"))
        return defects, notes

    text = raw.decode("utf-8", "replace")
    size = len(raw)
    if size < MIN_REPORT_BYTES:
        defects.append(("B.size", f"{size} bytes < MIN_REPORT_BYTES {MIN_REPORT_BYTES}"))
    else:
        notes.append(f"B.size {size} >= {MIN_REPORT_BYTES}")

    if not WATCHDOG_SHONEN.search(text):
        defects.append(("C.watchdog-shonen", "watchdog report_of SHONEN predicate does not match"))
    if not WATCHDOG_SOURCES.search(text):
        defects.append(("D.watchdog-sources", "watchdog sources-conformance heading absent"))

    found, starts = split_sections(text)
    present = [n for n, _, _ in found]
    for name, _ in SECTIONS:
        if name not in present:
            defects.append(("E.section", f"missing required section: {name}"))
    order = [starts[n] for n in present]
    if order != sorted(order):
        defects.append(("E.order", f"required sections out of order: {present}"))

    for name, _, body in found:
        if not POINTER.search(body):
            defects.append(("F.pointer", f"section has no evidence pointer: {name}"))

    for m in PLACEHOLDER.finditer(text):
        line = text[: m.start()].count("\n") + 1
        defects.append(("G.placeholder", f"placeholder text at line {line}: {m.group(0)!r}"))

    stale = STALE_ANY.findall(text)
    if not stale:
        defects.append(("H.stale-lane", "no Stale-lane line"))
    elif not any(CANONICAL_STALE in s for s in stale):
        defects.append(("H.stale-lane",
                        f"Stale-lane line present but not canonical: {stale[0].strip()!r}"))
    tools_seen = re.search(r"\**[ \t]*Tool installs[ \t]*\**[ \t]*:", text, re.IGNORECASE)
    if not tools_seen:
        defects.append(("H.tool-installs", "no 'Tool installs:' line (lane-addendum.md:196)"))

    trend = dict((n, b) for n, _, b in found).get("Trend verdicts", "")
    for axis in TREND_AXES:
        if axis.lower() not in trend.lower():
            defects.append(("I.trend", f"Trend verdicts lacks axis: {axis}"))
    if trend and not any(v in trend.lower() for v in VERDICTS):
        defects.append(("I.trend", "Trend verdicts carries no verdict keyword"))

    if shonen_path:
        try:
            with open(shonen_path, encoding="utf-8") as fh:
                want = len(SHONEN_BOX.findall(fh.read()))
        except OSError as exc:
            defects.append(("J.shonen", f"cannot count SHONEN.md boxes: {exc}"))
        else:
            got = len(SHONEN_BOX.findall(dict((n, b) for n, _, b in found).get("SHONEN", "")))
            if got != want:
                defects.append(("J.shonen",
                                f"SHONEN lines {got} != SHONEN.md boxes {want}"))
            else:
                notes.append(f"J.shonen {got}/{want} boxes covered")
    return defects, notes


def main(argv):
    if len(argv) < 2:
        print("usage: check-report-shape.py <report.md> [--shonen <SHONEN.md>]", file=sys.stderr)
        return 2
    path = argv[1]
    shonen = None
    if "--shonen" in argv:
        shonen = argv[argv.index("--shonen") + 1]
    defects, notes = check(path, shonen)
    print(f"TARGET {path}")
    for note in notes:
        print(f"  ok    {note}")
    for code, msg in defects:
        print(f"  DEFECT {code}: {msg}")
    verdict = "SHAPE_OK" if not defects else "SHAPE_DEFECTS"
    print(f"{verdict} defects={len(defects)}")
    return 0 if not defects else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
