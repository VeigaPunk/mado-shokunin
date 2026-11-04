#!/usr/bin/env python3
"""Append the round-79 SOURCES rows and re-point the rows the new entry cites.

Append-only: two new rows (S465, S466) and `used-by` cells updated old->new for S303, S457,
S458, S459. Nothing else changes; the lesson's Gate records each change.
"""

import re

PATH = "corpus/SOURCES.md"
ENTRY = "corpus/knowledge/bar-footprint-reserve-r79.md"

NEW_ROWS = [
    "| S465 | Hyprland v0.56.2 — src/output/Monitor.cpp — "
    "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/output/Monitor.cpp"
    " | code | A | mado compositor plane: the static reserved area a monitor rule applies and the usable box"
    " the layer plane is arranged in (round-79 C1) | applyMonitorRuleSoft :653-655 setStatic,"
    " logicalBoxMinusReserved :1772-1774 @ efb5099 (fetched 2026-11-04, sha256 9cf88e15…, 112738 B)"
    " | m_reservedArea.setStatic(m_activeMonitorRule.m_reservedArea); | mined | 2026-11-04 | on-release"
    " | corpus/knowledge/bar-footprint-reserve-r79.md |",
    "| S466 | Hyprland v0.56.2 — src/desktop/reserved/ReservedArea.cpp — "
    "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/reserved/ReservedArea.cpp"
    " | code | A | mado compositor plane: the static band and every dynamic contribution are summed into one"
    " reserved area (round-79 C1) | calculate :43-51, setStatic :69-74, addType :101-112 @ efb5099"
    " (fetched 2026-11-04, sha256 0a52e145…, 3339 B) | m_bottomRight += e.bottomRight; | mined | 2026-11-04"
    " | on-release | corpus/knowledge/bar-footprint-reserve-r79.md |",
]

UPDATES = {
    "S303": "corpus/knowledge/bar-footprint-reserve-r79.md",
    "S457": "corpus/knowledge/bar-footprint-reserve-r79.md",
    "S458": "corpus/knowledge/bar-footprint-reserve-r79.md",
    "S459": "corpus/knowledge/bar-footprint-reserve-r79.md",
}


def main():
    text = open(PATH).read()
    lines = text.splitlines()
    last_row = max(i for i, line in enumerate(lines) if re.match(r"^\| S[0-9]{3,} \|", line))
    for ident, entry in UPDATES.items():
        pattern = re.compile(r"^(\| %s \|.*)$" % ident)
        hits = [i for i, line in enumerate(lines) if pattern.match(line)]
        if len(hits) != 1:
            raise SystemExit("row %s occurs %d times" % (ident, len(hits)))
        index = hits[0]
        cells = lines[index].split(" | ")
        if len(cells) != 11:
            raise SystemExit("row %s has %d cells, expected 11" % (ident, len(cells)))
        used = cells[-1].rstrip(" |").strip()
        if entry in used:
            print("SKIP %s already cites the entry" % ident)
            continue
        cells[-1] = (used + "," + entry) if used and used != "—" else entry
        lines[index] = " | ".join(cells[:-1]) + " | " + cells[-1] + " |"
        print("UPDATE %s used-by %r -> %r" % (ident, used, cells[-1]))
    insert = ["", *NEW_ROWS]
    if any(line.startswith("| S465 |") for line in lines):
        raise SystemExit("S465 already present")
    lines[last_row + 1:last_row + 1] = insert
    open(PATH, "w").write("\n".join(lines) + "\n")
    print("APPENDED S465, S466")


if __name__ == "__main__":
    main()
