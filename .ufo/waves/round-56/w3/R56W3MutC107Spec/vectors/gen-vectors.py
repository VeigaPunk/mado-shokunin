#!/usr/bin/env python3
"""Criterion-107 acceptance vectors, built from the SPEC ALONE.

Spec source (read-only, never edited):
  corpus/QUALITY.md @ 0f3a54361a9824484d0801679ceb1fd8ac7c32e1, lines 592-607.

This generator materialises one scratch git repo per vector (registry +
knowledge entry + pinned blob), writes the hand-authored expected stdout/rc and
the strict/forbidden token sets, and emits the vector table and the receipts.

It does NOT implement criterion 107 as the lane gate.  reference-check-107.py
exists only to (a) prove the hand-authored expectations are attainable under the
documented readings and (b) power the mutation battery in mutate-check-107.py.
The lane gate is the sibling seat's quality/check-anchor-cover.py.

Usage:
  python3 -I gen-vectors.py --fixture-out <dir> --dest <dir>

--fixture-out receives one git repo per vector (scratch only).
--dest receives vectors/expected/*, vectors/fixtures/*, vectors/vectors.tsv and
receipts/vectors.txt.
"""

import argparse
import os
import re
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SPEC_REV = "0f3a54361a9824484d0801679ceb1fd8ac7c32e1"
PIN_PATH = ".ufo/waves/round-56/fetch/ConfigWatcher.cpp"
PIN_LINES = 200
FIXED_DATE = "2026-10-30T00:00:00+00:00"

SRC_URL = "https://example.org/src/ConfigWatcher.cpp"

REG_HEADER = (
    "| id | source | kind | tier | scope | anchor | teaches | status | opened "
    "| recheck | used-by |"
)
REG_SEP = "|---|---|---|---|---|---|---|---|---|---|---|"

ENT_HEADER = "| id | proposition | src | pin:line | quote |"
ENT_SEP = "|---|---|---|---|---|---|"

ALL_REASONS = {
    "malformed-pin",
    "no-registry-row",
    "dup-id",
    "no-name",
    "past-eof",
}


def reg_row(rid, source, anchor):
    return (
        f"| {rid} | {source} | code | A | fixture scope text | {anchor} | "
        f"fixture teaches text | mined | 2026-10-30 | 180d | — |"
    )


def ent_row(rid, sid, pin, prop="fixture proposition text",
            quote="fixture quote text"):
    return f"| {rid} | {prop} | {sid} | {pin} | {quote} |"


def sources_md(rows):
    return (
        "# SOURCES — criterion-107 vector fixture\n"
        "\n"
        "## Registry\n"
        "\n"
        f"{REG_HEADER}\n{REG_SEP}\n" + "\n".join(rows) + "\n"
    )


def entry_md(body_lines, intro="Cites the fixture registry rows below."):
    parts = [
        "# Vector entry — criterion 107 fixture",
        "",
        intro,
        "",
        ENT_HEADER,
        ENT_SEP,
    ]
    parts.extend(body_lines)
    return "\n".join(parts) + "\n"


def pin_blob():
    """PIN_LINES lines, NO trailing newline: split(b"\\n") pieces == lines == 200.

    The spec defines the blob's line count as "the number of \\n-separated
    pieces", so a trailing newline would make pieces = lines + 1 and put the
    EOF boundary at an off-by-one the fixture does not intend to test.
    """
    return "\n".join(f"line {i}" for i in range(1, PIN_LINES + 1))


def anchor(good="33-40", name="ConfigWatcher.cpp", pin=True, extra=""):
    a = f"{name}:{good}"
    if extra:
        a += " " + extra
    if pin:
        a += f"; pin {PIN_PATH}"
    return a


V = []


def add(**kw):
    V.append(kw)


# --- V01 good row ------------------------------------------------------------
add(
    id="V01",
    clause="good row (OK)",
    spec=(
        "Scope: every evidence row whose third cell is a registry id S + 3 or more "
        "digits; (5) Cover: some locator of some counted occurrence has N <= L <= M."
    ),
    amb=[],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S901", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="33-40", extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [ent_row("K01", "S901", "ConfigWatcher.cpp:35")]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S901 line=35 name=ConfigWatcher.cpp "
        "locators=33-40 eof=checked verdict=OK",
        "CHECK107: rows=1 covered=1 miss=0 verdict=OK",
    ],
    rc=0,
)

# --- V02 malformed pin -------------------------------------------------------
add(
    id="V02",
    clause="malformed pin (fourth cell not <file>:<N>)",
    spec=(
        "Scope: a row of that shape whose fourth cell is not exactly <file>:<N> "
        "(one decimal number; no range, no list, no second file) is a violation "
        "reason=malformed-pin. It is never skipped."
    ),
    amb=["line", "name", "locators", "eof"],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S902", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="33-40", pin=False, extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [
                ent_row("K01", "S902", "ConfigWatcher.cpp:35-36"),
                ent_row("K02", "S902", "ConfigWatcher.cpp:35,36"),
                ent_row("K03", "S902", "ConfigWatcher.cpp:35 Other.cpp:12"),
            ]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S902 line=none name=none locators=none "
        "eof=unchecked verdict=MISS [reason=malformed-pin]",
        "ANCHOR_COVER: row=K02 sid=S902 line=none name=none locators=none "
        "eof=unchecked verdict=MISS [reason=malformed-pin]",
        "ANCHOR_COVER: row=K03 sid=S902 line=none name=none locators=none "
        "eof=unchecked verdict=MISS [reason=malformed-pin]",
        "CHECK107: rows=3 covered=0 miss=3 verdict=FAIL",
    ],
    rc=1,
)

# --- V03 no registry row -----------------------------------------------------
add(
    id="V03",
    clause="no-registry-row",
    spec=(
        "(1) Uniqueness. R must be the only row with that id. Zero rows reads "
        "reason=no-registry-row."
    ),
    amb=["name", "locators", "eof"],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S901", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="33-40", pin=False, extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [ent_row("K01", "S903", "ConfigWatcher.cpp:35")]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S903 line=35 name=none locators=none "
        "eof=unchecked verdict=MISS [reason=no-registry-row]",
        "CHECK107: rows=1 covered=0 miss=1 verdict=FAIL",
    ],
    rc=1,
)

# --- V04 dup id --------------------------------------------------------------
add(
    id="V04",
    clause="dup-id",
    spec=(
        "(1) Uniqueness. ... two or more read reason=dup-id, whatever their content."
    ),
    amb=["name", "locators", "eof"],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [
                reg_row("S904", f"Upstream fixture one - {SRC_URL}",
                        anchor(good="33-40", pin=False, extra="@ fixture000")),
                reg_row("S904", f"Upstream fixture two - {SRC_URL}",
                        anchor(good="90-99", pin=False, extra="@ fixture000")),
            ]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [ent_row("K01", "S904", "ConfigWatcher.cpp:35")]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S904 line=35 name=none locators=none "
        "eof=unchecked verdict=MISS [reason=dup-id]",
        "CHECK107: rows=1 covered=0 miss=1 verdict=FAIL",
    ],
    rc=1,
)

# --- V05 no name -------------------------------------------------------------
add(
    id="V05",
    clause="no-name (source token with #/?)",
    spec=(
        "(2) NAME. The last path component of the last http(s):// token in R's "
        "source cell (cell 2), with trailing `).,;` removed. If NAME contains # "
        "or ?, the row reads reason=no-name and must be read by hand."
    ),
    amb=["name", "locators", "eof"],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [
                reg_row("S905", f"Upstream fixture query - {SRC_URL}?rev=1",
                        anchor(good="33-40", pin=False, extra="@ fixture000")),
                reg_row("S906", f"Upstream fixture fragment - {SRC_URL}#L10",
                        anchor(good="33-40", pin=False, extra="@ fixture000")),
            ]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [
                ent_row("K01", "S905", "ConfigWatcher.cpp:35"),
                ent_row("K02", "S906", "ConfigWatcher.cpp:35"),
            ]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S905 line=35 "
        "name=ConfigWatcher.cpp?rev=1 locators=none eof=unchecked verdict=MISS "
        "[reason=no-name]",
        "ANCHOR_COVER: row=K02 sid=S906 line=35 "
        "name=ConfigWatcher.cpp#L10 locators=none eof=unchecked verdict=MISS "
        "[reason=no-name]",
        "CHECK107: rows=2 covered=0 miss=2 verdict=FAIL",
    ],
    rc=1,
)

# --- V06 identifier prefix ---------------------------------------------------
add(
    id="V06",
    clause="identifier-prefix name (Old<X>.cpp must NOT count as <X>.cpp:)",
    spec=(
        "(3) Bounded occurrence. An occurrence of NAME: in R's anchor cell (cell 6) "
        "counts only when the character before it is absent or is not in "
        "[A-Za-z0-9_]. ... OldConfigWatcher.cpp: does not contain an occurrence of "
        "ConfigWatcher.cpp:."
    ),
    amb=[],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S907", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="33-40", name="OldConfigWatcher.cpp", pin=False,
                            extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [ent_row("K01", "S907", "ConfigWatcher.cpp:35")]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S907 line=35 name=ConfigWatcher.cpp "
        "locators=none eof=unchecked verdict=MISS",
        "CHECK107: rows=1 covered=0 miss=1 verdict=FAIL",
    ],
    rc=1,
)

# --- V07 hyphen / slash prefix ----------------------------------------------
add(
    id="V07",
    clause="hyphen-prefix name (-<X>.cpp: MUST count) + slash prefix",
    spec="(3) Bounded occurrence. ... A hyphen or a slash before it is allowed.",
    amb=[],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [
                reg_row("S908", f"Upstream fixture - config watcher - {SRC_URL}",
                        anchor(good="33-40", name="-ConfigWatcher.cpp", pin=False,
                               extra="@ fixture000")),
                reg_row("S909", f"Upstream fixture - config watcher - {SRC_URL}",
                        anchor(good="33-40", name="src/ConfigWatcher.cpp", pin=False,
                               extra="@ fixture000")),
            ]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [
                ent_row("K01", "S908", "ConfigWatcher.cpp:35"),
                ent_row("K02", "S909", "ConfigWatcher.cpp:35"),
            ]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S908 line=35 name=ConfigWatcher.cpp "
        "locators=33-40 eof=unchecked verdict=OK",
        "ANCHOR_COVER: row=K02 sid=S909 line=35 name=ConfigWatcher.cpp "
        "locators=33-40 eof=unchecked verdict=OK",
        "CHECK107: rows=2 covered=2 miss=0 verdict=OK",
    ],
    rc=0,
)

# --- V08 reversed range ------------------------------------------------------
add(
    id="V08",
    clause="reversed range (M<N covers nothing)",
    spec=(
        "(4) Locator list. ... A locator with M less than N denotes no line and "
        "covers nothing."
    ),
    amb=["locators"],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S910", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="50-40", pin=False, extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [ent_row("K01", "S910", "ConfigWatcher.cpp:50")]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S910 line=50 name=ConfigWatcher.cpp "
        "locators=50-40 eof=unchecked verdict=MISS",
        "CHECK107: rows=1 covered=0 miss=1 verdict=FAIL",
    ],
    rc=1,
)

# --- V09 narrow below the quoted line ----------------------------------------
add(
    id="V09",
    clause="narrow range below the quoted line (cover fails)",
    spec=(
        "(5) Cover. Some locator of some counted occurrence has N <= L <= M, "
        "where L is the quoted line."
    ),
    amb=[],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S911", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="20-30", pin=False, extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [ent_row("K01", "S911", "ConfigWatcher.cpp:35")]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S911 line=35 name=ConfigWatcher.cpp "
        "locators=20-30 eof=unchecked verdict=MISS",
        "CHECK107: rows=1 covered=0 miss=1 verdict=FAIL",
    ],
    rc=1,
)

# --- V10 past eof ------------------------------------------------------------
add(
    id="V10",
    clause="past-eof (locator past the pin blob's lines)",
    spec=(
        "(6) Length. ... every locator of the counted occurrence must have "
        "max(N, M) <= the blob's line count (the number of \\n-separated pieces). "
        "A locator past the end of the file reads reason=past-eof for every row "
        "of that pin."
    ),
    amb=[],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S912", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="500", extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [ent_row("K01", "S912", "ConfigWatcher.cpp:500")]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S912 line=500 name=ConfigWatcher.cpp "
        "locators=500 eof=checked verdict=MISS [reason=past-eof]",
        "CHECK107: rows=1 covered=0 miss=1 verdict=FAIL",
    ],
    rc=1,
)

# --- V11 past eof hits every row of the pin ---------------------------------
add(
    id="V11",
    clause="past-eof for every row of that pin",
    spec=(
        "(6) Length. ... A locator past the end of the file reads reason=past-eof "
        "for every row of that pin."
    ),
    amb=[],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S913", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="10,20,500", extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [
                ent_row("K01", "S913", "ConfigWatcher.cpp:10"),
                ent_row("K02", "S913", "ConfigWatcher.cpp:20"),
            ]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S913 line=10 name=ConfigWatcher.cpp "
        "locators=10,20,500 eof=checked verdict=MISS [reason=past-eof]",
        "ANCHOR_COVER: row=K02 sid=S913 line=20 name=ConfigWatcher.cpp "
        "locators=10,20,500 eof=checked verdict=MISS [reason=past-eof]",
        "CHECK107: rows=2 covered=0 miss=2 verdict=FAIL",
    ],
    rc=1,
)

# --- V12 eof unchecked -------------------------------------------------------
add(
    id="V12",
    clause="eof=unchecked (anchor without `pin <path>`)",
    spec=(
        "(6) Length. If the anchor cell names its pin as `pin <path>`, the blob at "
        "that path at the checked revision is read ... An anchor with no named "
        "pin reads eof=unchecked in the output."
    ),
    amb=["verdict"],
    amb_summary=["covered", "miss", "verdict"],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S914", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="33-40", pin=False, extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [ent_row("K01", "S914", "ConfigWatcher.cpp:35")]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S914 line=35 name=ConfigWatcher.cpp "
        "locators=33-40 eof=unchecked verdict=OK",
        "CHECK107: rows=1 covered=1 miss=0 verdict=OK",
    ],
    rc=0,
)

# --- V13 comma locator spacing ----------------------------------------------
add(
    id="V13",
    clause="comma-locator spacing (zero and one space)",
    spec=(
        "(4) Locator list. Right after NAME: comes a comma-separated list of "
        "locators. ... One optional space may follow a comma. The list continues "
        "only while the next item starts with a digit."
    ),
    amb=["locators"],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [
                reg_row("S915", f"Upstream fixture - config watcher - {SRC_URL}",
                        anchor(good="33,46", pin=False, extra="@ fixture000")),
                reg_row("S916", f"Upstream fixture - config watcher - {SRC_URL}",
                        anchor(good="33, 46", pin=False, extra="@ fixture000")),
            ]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [
                ent_row("K01", "S915", "ConfigWatcher.cpp:46"),
                ent_row("K02", "S916", "ConfigWatcher.cpp:46"),
            ]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S915 line=46 name=ConfigWatcher.cpp "
        "locators=33,46 eof=unchecked verdict=OK",
        "ANCHOR_COVER: row=K02 sid=S916 line=46 name=ConfigWatcher.cpp "
        "locators=33,46 eof=unchecked verdict=OK",
        "CHECK107: rows=2 covered=2 miss=0 verdict=OK",
    ],
    rc=0,
)

# --- V14 boundary N = L ------------------------------------------------------
add(
    id="V14",
    clause="boundary N=L covers",
    spec="(5) Cover. ... A single N means N = L.",
    amb=[],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S917", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="35", pin=False, extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [ent_row("K01", "S917", "ConfigWatcher.cpp:35")]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S917 line=35 name=ConfigWatcher.cpp "
        "locators=35 eof=unchecked verdict=OK",
        "CHECK107: rows=1 covered=1 miss=0 verdict=OK",
    ],
    rc=0,
)

# --- V15 boundary M = L ------------------------------------------------------
add(
    id="V15",
    clause="boundary M=L covers",
    spec="(5) Cover. Some locator of some counted occurrence has N <= L <= M.",
    amb=[],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S918", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="30-35", pin=False, extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [ent_row("K01", "S918", "ConfigWatcher.cpp:35")]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S918 line=35 name=ConfigWatcher.cpp "
        "locators=30-35 eof=unchecked verdict=OK",
        "CHECK107: rows=1 covered=1 miss=0 verdict=OK",
    ],
    rc=0,
)

# --- V16 scope: fenced code and HTML comments -------------------------------
add(
    id="V16",
    clause="scope: fenced code and HTML comments are out of scope",
    spec=(
        "Scope. Every evidence row of a knowledge entry, any row class: a table "
        "row, outside fenced code and HTML comments, whose third cell is a "
        "registry id S followed by three or more digits."
    ),
    amb=[],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S919", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="33-40", pin=False, extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": (
            "# Vector entry — criterion 107 fixture\n"
            "\n"
            "Cites the fixture registry rows below.\n"
            "\n"
            f"{ENT_HEADER}\n{ENT_SEP}\n"
            + ent_row("K01", "S919", "ConfigWatcher.cpp:35")
            + "\n"
            "\n"
            "```\n"
            + ent_row("K02", "S919", "ConfigWatcher.cpp:35")
            + "\n"
            "```\n"
            "\n"
            "<!--\n"
            + ent_row("K03", "S919", "ConfigWatcher.cpp:35")
            + "\n"
            "-->\n"
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S919 line=35 name=ConfigWatcher.cpp "
        "locators=33-40 eof=unchecked verdict=OK",
        "CHECK107: rows=1 covered=1 miss=0 verdict=OK",
    ],
    rc=0,
)

# --- V17 scope: empty entry --------------------------------------------------
add(
    id="V17",
    clause="scope: no in-scope evidence row",
    spec=(
        "Declared limits: An entry with no evidence rows reads rows=0 verdict=FAIL, "
        "so an empty entry is not vacuously green."
    ),
    amb=[],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S920", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="33-40", pin=False, extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": (
            "# Vector entry — criterion 107 fixture\n"
            "\n"
            "Cites the fixture registry rows below.\n"
            "\n"
            "The registry row S920 is mentioned here in prose, not in a table row.\n"
            "\n"
            "```\n"
            + ent_row("K01", "S920", "ConfigWatcher.cpp:35")
            + "\n"
            "```\n"
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "CHECK107: rows=0 covered=0 miss=0 verdict=FAIL",
    ],
    rc=1,
)

# --- V18 scope: third cell is not a registry id -----------------------------
add(
    id="V18",
    clause="scope: third cell that is not S+3 digits is out of scope",
    spec=(
        "Scope. ... whose third cell is a registry id S followed by three or more "
        "digits."
    ),
    amb=[],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S921", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="33-40", pin=False, extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [
                ent_row("K01", "S921", "ConfigWatcher.cpp:35"),
                ent_row("K02", "S12", "ConfigWatcher.cpp:35"),
                ent_row("K03", "ConfigWatcher.cpp", "ConfigWatcher.cpp:35"),
                ent_row("K04", "see S921", "ConfigWatcher.cpp:35"),
            ]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S921 line=35 name=ConfigWatcher.cpp "
        "locators=33-40 eof=unchecked verdict=OK",
        "CHECK107: rows=1 covered=1 miss=0 verdict=OK",
    ],
    rc=0,
)

# --- V19 four-digit registry id ---------------------------------------------
add(
    id="V19",
    clause="scope: S + four digits is in scope",
    spec=(
        "Scope. ... whose third cell is a registry id S followed by three or more "
        "digits."
    ),
    amb=[],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S0921", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="33-40", pin=False, extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [ent_row("K01", "S0921", "ConfigWatcher.cpp:35")]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S0921 line=35 name=ConfigWatcher.cpp "
        "locators=33-40 eof=unchecked verdict=OK",
        "CHECK107: rows=1 covered=1 miss=0 verdict=OK",
    ],
    rc=0,
)

# --- V20 trailing punctuation in the source token ---------------------------
add(
    id="V20",
    clause="NAME strips trailing `).,;` from the last path component",
    spec=(
        "(2) NAME. The last path component of the last http(s):// token in R's "
        "source cell (cell 2), with trailing `).,;` removed."
    ),
    amb=[],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S922", f"Upstream fixture - config watcher - ({SRC_URL}).",
                     anchor(good="33-40", pin=False, extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [ent_row("K01", "S922", "ConfigWatcher.cpp:35")]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S922 line=35 name=ConfigWatcher.cpp "
        "locators=33-40 eof=unchecked verdict=OK",
        "CHECK107: rows=1 covered=1 miss=0 verdict=OK",
    ],
    rc=0,
)

# --- V21 EOF boundary: locator exactly at the blob's line count -------------
add(
    id="V21",
    clause="EOF boundary: locator == the pin blob's line count is inside",
    spec=(
        "(6) Length. ... every locator of the counted occurrence must have "
        "max(N, M) <= the blob's line count (the number of \\n-separated pieces)."
    ),
    amb=[],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S923", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="200", extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [ent_row("K01", "S923", "ConfigWatcher.cpp:200")]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S923 line=200 name=ConfigWatcher.cpp "
        "locators=200 eof=checked verdict=OK",
        "CHECK107: rows=1 covered=1 miss=0 verdict=OK",
    ],
    rc=0,
)

# --- V22 EOF boundary: one past the blob's line count ------------------------
add(
    id="V22",
    clause="EOF boundary: locator == line count + 1 is past-eof",
    spec=(
        "(6) Length. ... A locator past the end of the file reads reason=past-eof "
        "for every row of that pin."
    ),
    amb=[],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S924", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="200,201", extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [ent_row("K01", "S924", "ConfigWatcher.cpp:200")]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S924 line=200 name=ConfigWatcher.cpp "
        "locators=200,201 eof=checked verdict=MISS [reason=past-eof]",
        "CHECK107: rows=1 covered=0 miss=1 verdict=FAIL",
    ],
    rc=1,
)

# --- V23 the anchor names a different file entirely -------------------------
add(
    id="V23",
    clause="anchor names a different file (no occurrence of NAME: at all)",
    spec=(
        "(3) Bounded occurrence. An occurrence of NAME: in R's anchor cell (cell 6) "
        "counts only when the character before it is absent or is not in "
        "[A-Za-z0-9_]."
    ),
    amb=[],
    amb_summary=[],
    files={
        "corpus/SOURCES.md": sources_md(
            [reg_row("S925", f"Upstream fixture - config watcher - {SRC_URL}",
                     anchor(good="33-40", name="OtherWatcher.cpp", pin=False,
                            extra="@ fixture000"))]
        ),
        "corpus/knowledge/entry-c107.md": entry_md(
            [ent_row("K01", "S925", "ConfigWatcher.cpp:35")]
        ),
        PIN_PATH: pin_blob(),
    },
    expected=[
        "ANCHOR_COVER: row=K01 sid=S925 line=35 name=ConfigWatcher.cpp "
        "locators=none eof=unchecked verdict=MISS",
        "CHECK107: rows=1 covered=0 miss=1 verdict=FAIL",
    ],
    rc=1,
)


# --- emission ----------------------------------------------------------------

def git(*args, cwd=None, env=None):
    return subprocess.run(
        ["git", "-C", cwd, *args], check=True, capture_output=True, text=True,
        env=env,
    ).stdout


def materialise(vec, fixture_out):
    d = os.path.join(fixture_out, vec["id"])
    os.makedirs(d, exist_ok=True)
    subprocess.run(["git", "init", "-q", d], check=True)
    top = git("rev-parse", "--show-toplevel", cwd=d).strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise SystemExit(f"fixture toplevel mismatch: {top} != {d}")
    for rel, content in vec["files"].items():
        full = os.path.join(d, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(content)
    git("add", "-A", cwd=d)
    env = dict(os.environ)
    env["GIT_AUTHOR_DATE"] = FIXED_DATE
    env["GIT_COMMITTER_DATE"] = FIXED_DATE
    git("-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q",
        "-m", f"fixture {vec['id']}", cwd=d, env=env)
    return git("rev-parse", "HEAD", cwd=d).strip(), d


def spec_reason(vec):
    for line in vec["expected"]:
        m = re.search(r"reason=([a-z-]+)", line)
        if m:
            return m.group(1)
    return None


def strict_tokens(vec):
    """Tokens that must be present in the checker's stdout for this vector."""
    toks = []
    fields = {"row", "sid", "line", "name", "locators", "eof", "verdict"}
    for line in vec["expected"]:
        if not line.startswith("ANCHOR_COVER:"):
            continue
        for kv in line.split():
            k, _, v = kv.partition("=")
            if k not in fields:
                continue
            if k in vec["amb"]:
                continue
            toks.append(f"{k}={v}")
    r = spec_reason(vec)
    if r:
        toks.append(f"reason={r}")
    summary = vec["expected"][-1]
    for kv in summary.split():
        k, _, v = kv.partition("=")
        if k in ("rows", "covered", "miss", "verdict"):
            if k in vec["amb_summary"]:
                continue
            toks.append(f"{k}={v}")
    return toks


def forbidden_tokens(vec):
    """Tokens that must NOT appear (wrong reason / flipped verdict)."""
    out = []
    r = spec_reason(vec)
    if r:
        for other in sorted(ALL_REASONS - {r}):
            out.append(f"reason={other}")
    summary = vec["expected"][-1]
    fields = dict(kv.partition("=")[::2] for kv in summary.split())
    if "verdict" not in vec["amb_summary"]:
        if fields.get("verdict") == "OK":
            out.append("verdict=FAIL")
        elif fields.get("verdict") == "FAIL":
            out.append("verdict=OK")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture-out", required=True)
    ap.add_argument("--dest", required=True)
    args = ap.parse_args()

    fx = os.path.abspath(args.fixture_out)
    dest = os.path.abspath(args.dest)
    os.makedirs(fx, exist_ok=True)
    for sub in ("vectors/expected", "vectors/fixtures", "receipts"):
        os.makedirs(os.path.join(dest, sub), exist_ok=True)

    tsv = [
        "id\tclause\tverdict\treason\trc\trows\tcovered\tmiss\tsha\t"
        "deciding_spec_sentence"
    ]
    rec = []
    for vec in V:
        sha, d = materialise(vec, fx)
        exp = os.path.join(dest, "vectors/expected", vec["id"])
        with open(exp + ".stdout", "w", encoding="utf-8") as fh:
            fh.write("\n".join(vec["expected"]) + "\n")
        with open(exp + ".rc", "w", encoding="utf-8") as fh:
            fh.write(f"{vec['rc']}\n")
        with open(exp + ".strict", "w", encoding="utf-8") as fh:
            fh.write("\n".join(strict_tokens(vec)) + "\n")
        with open(exp + ".forbid", "w", encoding="utf-8") as fh:
            ft = forbidden_tokens(vec)
            fh.write("\n".join(ft) + ("\n" if ft else ""))
        with open(os.path.join(dest, "vectors/fixtures", vec["id"] + ".txt"),
                  "w", encoding="utf-8") as fh:
            fh.write(f"# vector {vec['id']} — clause: {vec['clause']}\n")
            fh.write(f"# fixture commit (regenerate with gen-vectors.py): {sha}\n")
            fh.write(f"# deciding spec sentence: {vec['spec']}\n")
            fh.write(f"# ambiguous output fields: "
                     f"{','.join(vec['amb'] + vec['amb_summary']) or 'none'}\n\n")
            for rel in sorted(vec["files"]):
                fh.write(f"===== {rel} =====\n")
                body = vec["files"][rel]
                if rel == PIN_PATH:
                    fh.write(f"<{len(body.split(chr(10)))} line blob, "
                             f"no trailing newline>\n")
                else:
                    fh.write(body)
                fh.write("\n")
        summary = vec["expected"][-1]
        fields = dict(kv.partition("=")[::2] for kv in summary.split())
        tsv.append(
            "\t".join([
                vec["id"], vec["clause"], fields.get("verdict", ""),
                spec_reason(vec) or "-",
                str(vec["rc"]), fields.get("rows", ""), fields.get("covered", ""),
                fields.get("miss", ""), sha,
                vec["spec"].replace("\t", " "),
            ])
        )
        rec.append(
            f"{vec['id']}  clause={vec['clause']}\n"
            f"      expected-verdict: {fields.get('verdict')} "
            f"(rows={fields.get('rows')} covered={fields.get('covered')} "
            f"miss={fields.get('miss')}) rc={vec['rc']}"
            f"{' reason=' + spec_reason(vec) if spec_reason(vec) else ''}\n"
            f"      deciding spec sentence: {vec['spec']}\n"
            f"      fixture commit: {sha}\n"
            f"      expected stdout: vectors/expected/{vec['id']}.stdout\n"
            f"      strict tokens: vectors/expected/{vec['id']}.strict\n"
            f"      forbidden tokens: vectors/expected/{vec['id']}.forbid\n"
            f"      ambiguous output fields: "
            f"{','.join(vec['amb'] + vec['amb_summary']) or 'none'}\n"
        )
    with open(os.path.join(dest, "vectors/vectors.tsv"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(tsv) + "\n")
    with open(os.path.join(dest, "receipts/vectors.txt"), "w", encoding="utf-8") as fh:
        fh.write(
            f"criterion-107 acceptance vectors, built from corpus/QUALITY.md @ "
            f"{SPEC_REV} lines 592-607 (spec alone; no checker implementation "
            f"read)\n"
        )
        fh.write(f"vectors: {len(V)}\n\n")
        fh.write("\n".join(rec))
    print(f"vectors={len(V)} fixture_out={fx} dest={dest}")


if __name__ == "__main__":
    main()
