#!/usr/bin/env python3
"""RerunCensus seat checker: registry diff + per-row cell checks for round-43 data commit.

Reads the two extracted registries in this seat dir (SOURCES-base.md = a35cfdf,
SOURCES-data.md = 1959770) and prints one line per check, all prefixed CHK.
No writes outside this seat dir.
"""
import re
import sys

BASE = "SOURCES-base.md"
DATA = "SOURCES-data.md"
ENTRY = "corpus/knowledge/hyprland-gkeep-geometry-r43.md"
NEW_IDS = [f"S{n}" for n in range(290, 298)]
HELD = ["S155", "S158"]

ROW_RE = re.compile(r"^ {0,3}\|[ ]*S[0-9]{3,}[ ]*\|")


def rows(path):
    """id -> (lineno, raw line, cells) for table rows under ## Registry."""
    out = {}
    order = []
    in_reg = False
    with open(path, encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            line = line.rstrip("\n")
            s = line.lstrip(" ")
            if s.startswith("## "):
                in_reg = s[3:].strip() == "Registry"
                continue
            if s.startswith("# "):
                in_reg = False
                continue
            if not in_reg or not ROW_RE.match(line):
                continue
            cells = line.split("|")
            rid = cells[1].strip()
            out[rid] = (i, line, cells)
            order.append(rid)
    return out, order


def main():
    base, border = rows(BASE)
    data, dorder = rows(DATA)
    fails = []

    def chk(ok, name, detail):
        print(("CHK PASS " if ok else "CHK FAIL ") + name + " :: " + detail)
        if not ok:
            fails.append(name)

    chk(len(border) == 226, "base-row-count", f"base rows={len(border)} (claimed 226)")
    chk(len(dorder) == 234, "data-row-count", f"data rows={len(dorder)} (claimed 234)")
    chk(len(dorder) - len(border) == 8, "row-delta", f"delta={len(dorder)-len(border)} (claimed +8)")

    added = [r for r in dorder if r not in base]
    removed = [r for r in border if r not in data]
    chk(added == NEW_IDS, "added-ids", f"added={added} expected={NEW_IDS}")
    chk(removed == [], "removed-ids", f"removed={removed}")
    chk(dorder[: len(border)] == border, "row-order-prefix",
        "base row order is a strict prefix of the data row order (append-only)")

    for rid in NEW_IDS:
        ln, raw, c = data[rid]
        nf = len(c)
        chk(nf == 13, f"{rid}-NF13", f"split('|') len={nf} => {nf-2} cells (want 11)")
        if nf != 13:
            continue
        chk(c[8].strip() == "mined", f"{rid}-status", f"status={c[8].strip()!r}")
        chk(c[9].strip() == "2026-10-26", f"{rid}-opened", f"opened={c[9].strip()!r}")
        chk(c[11].strip() == ENTRY, f"{rid}-usedby", f"used-by={c[11].strip()!r}")
        chk(c[4].strip() == "A", f"{rid}-tier", f"tier={c[4].strip()!r}")
        chk(c[3].strip() in ("code", "own-work"), f"{rid}-kind", f"kind={c[3].strip()!r}")
        chk(c[10].strip() != "", f"{rid}-recheck", f"recheck={c[10].strip()!r}")

    for rid in HELD:
        b = base[rid][2]
        d = data[rid][2]
        chk(len(b) == len(d) == 13, f"{rid}-NF13", f"base NF={len(b)} data NF={len(d)}")
        same = all(b[i] == d[i] for i in range(1, 11))
        chk(same, f"{rid}-cells1-10-byte-equal", "columns id..recheck identical byte for byte")
        btail = b[11].strip()
        dtail = d[11].strip()
        chk(dtail.startswith(btail + ", "), f"{rid}-usedby-prefix",
            "data used-by starts with the base used-by (stripped) plus ', '")
        suffix = dtail[len(btail) + 2:]
        chk(suffix == ENTRY, f"{rid}-usedby-one-item",
            f"appended item={suffix!r} expected={ENTRY!r}")
        bitems = [x.strip() for x in btail.split(",") if x.strip()]
        ditems = [x.strip() for x in dtail.split(",") if x.strip()]
        chk(ditems == bitems + [ENTRY], f"{rid}-usedby-order",
            f"items {len(bitems)}->{len(ditems)}, prior items unchanged in order")

    changed = []
    for rid in border:
        if rid in data and base[rid][1] != data[rid][1]:
            changed.append(rid)
    chk(changed == HELD, "changed-rows", f"rows whose full line differs={changed} expected={HELD}")

    # every other row byte-identical
    others = [r for r in border if r not in HELD and r in data]
    bad = [r for r in others if base[r][1] != data[r][1]]
    chk(bad == [], "others-unchanged", f"unchanged={len(others)} mismatched={bad}")

    print("CHK SUMMARY fails=%d" % len(fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
