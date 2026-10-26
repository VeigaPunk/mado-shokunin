#!/usr/bin/env python3
"""ScrSkillProvince table-row structure check (round 43, w1).

A markdown table splits on an unescaped `|`, so a drafted row with the wrong cell
count silently becomes a different table.  This script extracts every fenced block
from the three drafts and checks the cell count of each drafted table row against
the table it is meant to join, plus that the shell pipe in the command cells is
escaped as `\\|`.  Reads only this seat directory; writes nothing.

    python3 -I .ufo/waves/round-43/w1/ScrSkillProvince/verify-rows.py
"""
import os
import re
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
FENCE = re.compile(r"^```markdown\n(.*?)^```$", re.M | re.S)
UNESCAPED = re.compile(r"(?<!\\)\|")


def cells(row):
    """Cells of a table row, unescaped-pipe split, edge pipes dropped."""
    parts = UNESCAPED.split(row)
    return parts[1:-1] if len(parts) >= 2 else parts


def main():
    checks, failed = [], []

    def check(name, ok, detail=""):
        checks.append(name)
        if not ok:
            failed.append(f"{name} {detail}".rstrip())

    def blocks(name):
        text = open(os.path.join(SEAT, name), encoding="utf-8").read()
        return [m.group(1) for m in FENCE.finditer(text)]

    # 1. probe row: Read-only probes table = 3 cells, command cell escaped
    blk = blocks("skill-rows.md")
    probe = [l for b in blk for l in b.splitlines()
             if l.startswith("| `hyprctl clients -j")]
    check("probe-row-found", len(probe) == 1, f"found={len(probe)}")
    if probe:
        row = probe[0]
        check("probe-row-3-cells", len(cells(row)) == 3, f"cells={len(cells(row))}")
        check("probe-row-pipe-escaped", r"clients -j \| python3" in row)
        check("probe-row-no-bare-pipe-in-code",
              len(UNESCAPED.split(row)) == 5, f"segments={len(UNESCAPED.split(row))}")

    # 2. decision row: Claim-first routing table = 4 cells
    dec = [l for b in blk for l in b.splitlines()
           if l.startswith("| Does the size a window rule asks for match")]
    check("decision-row-found", len(dec) == 1, f"found={len(dec)}")
    if dec:
        row = dec[0]
        check("decision-row-4-cells", len(cells(row)) == 4, f"cells={len(cells(row))}")
        check("decision-row-pipe-escaped", r"clients -j \| python3" in row)

    # 3. verdict table inside the subsection: 6 rows x 3 cells
    verdict = [l for b in blk for l in b.splitlines()
               if l.startswith("| AGREE |") or l.startswith("| DIFFER |")
               or l.startswith("| TILED |") or l.startswith("| BADSIZE |")
               or l.startswith("| NO_MATCHING_CLIENT") or l.startswith("| NO_SIZE_RULES")]
    check("verdict-rows-found", len(verdict) == 6, f"found={len(verdict)}")
    for row in verdict:
        check(f"verdict-row-3-cells {row.split('|')[1].strip()}",
              len(cells(row)) == 3, f"cells={len(cells(row))}")

    # 4. PROVINCE tool row: 4 cells
    prow = [l for b in blocks("province-row.md") for l in b.splitlines()
            if l.startswith("| `tools/mado-geometry.py`")]
    check("province-row-found", len(prow) == 1, f"found={len(prow)}")
    if prow:
        check("province-row-4-cells", len(cells(prow[0])) == 4,
              f"cells={len(cells(prow[0]))}")

    # 5. README index row: 3 cells, all non-empty
    irow = [l for b in blocks("readme-row.md") for l in b.splitlines()
            if l.startswith("| `knowledge/hyprland-gkeep-geometry-r43.md`")]
    check("index-row-found", len(irow) == 1, f"found={len(irow)}")
    if irow:
        c = cells(irow[0])
        check("index-row-3-cells", len(c) == 3, f"cells={len(c)}")
        check("index-row-cells-non-empty", all(x.strip() for x in c))
        check("index-row-note-cell-names-note",
              "knowledge/hyprland-gkeep-geometry-r43.md" in c[0])
        check("index-row-sources-cell-non-empty", bool(c[2].strip()))

    # 6. the insertion anchors named in each draft are the real neighbours
    # SEAT = <lane>/.ufo/waves/round-43/w1/ScrSkillProvince
    lane = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(SEAT)))))
    skill = os.path.join(lane, "SKILL.md")
    readme = os.path.join(lane, "corpus", "README.md")
    province = os.path.join(lane, "PROVINCE.md")
    for path, lineno, prefix in (
        (skill, 223, "| `python3 tools/mado-globals.py --journal-file"),
        (skill, 157, "| Which Wayland globals the compositor advertises"),
        (skill, 243, ""),
        (skill, 244, "### Mutating commands"),
        (province, 31, "| `tools/mado-globals.py`"),
        (readme, 70, "| `knowledge/hyprland-focus-grab-r41.md`"),
        (readme, 71, ""),
        (readme, 72, "## Quality bar"),
        (readme, 291, ""),
    ):
        lines = open(path, encoding="utf-8").read().splitlines()
        ok = lineno <= len(lines) and lines[lineno - 1].startswith(prefix)
        check(f"anchor {os.path.basename(path)}:{lineno}", ok,
              f"got={lines[lineno - 1][:50]!r}" if lineno <= len(lines) else "EOF")

    print(f"ROWS: {len(checks) - len(failed)}/{len(checks)} checks passed")
    for name in failed:
        print(f"FAILED: {name}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
