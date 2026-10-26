#!/usr/bin/env python3
"""ScrSkillProvince integration simulation (round 43, w1).

Applies the three drafted insertion sets to *scratch copies* of the lane's
SKILL.md / PROVINCE.md / corpus/README.md and checks the result structurally:
every table row keeps the cell count of the table it joins, each affected table
grows by exactly the drafted number of rows, and the simulated README passes
`quality/check-index-rows.py --root <scratch>`.

Nothing under the lane is written: the copies live in the scratch tree named by
$SIM_TREE (default /fast/scratch/hyaku/mado-r43/ScrSkillProvince/tree).

    python3 -I .ufo/waves/round-43/w1/ScrSkillProvince/simulate-integration.py
"""
import os
import re
import subprocess
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(SEAT)))))
TREE = os.environ.get(
    "SIM_TREE", "/fast/scratch/hyaku/mado-r43/ScrSkillProvince/tree")
FENCE = re.compile(r"^```markdown\n(.*?)^```$", re.M | re.S)
UNESCAPED = re.compile(r"(?<!\\)\|")


def blocks(name):
    text = open(os.path.join(SEAT, name), encoding="utf-8").read()
    return [m.group(1).rstrip("\n") for m in FENCE.finditer(text)]


def cells(line):
    parts = UNESCAPED.split(line)
    return parts[1:-1] if len(parts) >= 2 else parts


def insert_after(lines, lineno, block):
    """Insert block lines after 1-based lineno."""
    add = block.splitlines()
    return lines[:lineno] + add + lines[lineno:]


def table_span(lines, header_prefix):
    start = next(i for i, l in enumerate(lines) if l.startswith(header_prefix))
    j = start + 2  # skip header + separator
    while j < len(lines) and lines[j].startswith("|"):
        j += 1
    return start + 2, j  # 0-based first data row, end (exclusive)


def main():
    checks, failed = [], []

    def check(name, ok, detail=""):
        checks.append(name)
        if not ok:
            failed.append(f"{name} {detail}".rstrip())

    probe, decision, subsection = blocks("skill-rows.md")
    (province_row,) = blocks("province-row.md")
    index_row, frontier = blocks("readme-row.md")

    # --- SKILL.md: insert high line number first so earlier anchors stay valid
    skill = open(os.path.join(LANE, "SKILL.md"), encoding="utf-8").read().splitlines()
    n0 = len(skill)
    skill = insert_after(skill, 243, subsection)
    skill = insert_after(skill, 223, probe)
    skill = insert_after(skill, 157, decision)
    check("skill grows by the drafted lines",
          len(skill) == n0 + len(subsection.splitlines())
          + len(probe.splitlines()) + len(decision.splitlines()),
          f"{n0}->{len(skill)}")

    for header, want, expect_rows in (
        ("| Probe | Answers | Sample |", 3, 18),
        ("| The claim you must settle | Route to | Run (read-only) | Tag |", 4, 13),
        ("| Verdict | Licenses | Does not license |", 3, 6),
    ):
        a, b = table_span(skill, header)
        rows = skill[a:b]
        check(f"table {header[:28]!r} row count", len(rows) == expect_rows,
              f"{len(rows)} != {expect_rows}")
        bad = [(a + k + 1, len(cells(r))) for k, r in enumerate(rows)
               if len(cells(r)) != want]
        check(f"table {header[:28]!r} cells", not bad, str(bad[:3]))

    # the drafted rows landed in the right tables
    probe_span = table_span(skill, "| Probe | Answers | Sample |")
    check("probe row inside the probe table",
          any(l.startswith("| `hyprctl clients -j") for l in skill[probe_span[0]:probe_span[1]]))
    route_span = table_span(skill, "| The claim you must settle | Route to | Run (read-only) | Tag |")
    check("decision row inside the routing table",
          any(l.startswith("| Does the size a window rule asks for match")
              for l in skill[route_span[0]:route_span[1]]))
    check("subsection heading present",
          "### Rule size versus reported size" in skill)
    check("subsection sits before the mutating-commands heading",
          skill.index("### Rule size versus reported size")
          < skill.index("### Mutating commands — operator only, mado never runs"))

    # --- PROVINCE.md
    prov = open(os.path.join(LANE, "PROVINCE.md"), encoding="utf-8").read().splitlines()
    p0 = len(prov)
    prov = insert_after(prov, 31, province_row)
    check("province grows by one row", len(prov) == p0 + 1, f"{p0}->{len(prov)}")
    a, b = table_span(prov, "| Tool | Reads | Writes | Owner and adjacent lanes |")
    bad = [(a + k + 1, len(cells(r))) for k, r in enumerate(prov[a:b])
           if len(cells(r)) != 4]
    check("province tool table cells", not bad, str(bad[:3]))
    check("province row is last in the tool table",
          prov[b - 1].startswith("| `tools/mado-geometry.py`"))

    # --- corpus/README.md: index row + frontier bullet, then the real checker
    readme = open(os.path.join(LANE, "corpus", "README.md"),
                  encoding="utf-8").read().splitlines()
    r0 = len(readme)
    readme = insert_after(readme, 70, index_row)
    readme = readme + [""] + frontier.splitlines()
    check("readme grows by the drafted lines",
          len(readme) == r0 + 1 + 1 + len(frontier.splitlines()),
          f"{r0}->{len(readme)}")
    a, b = table_span(readme, "| Note | Holds | Sources |")
    bad = [(a + k + 1, len(cells(r))) for k, r in enumerate(readme[a:b])
           if len(cells(r)) != 3]
    check("readme coverage table cells", not bad, str(bad[:3]))
    check("index row is last in the coverage table",
          readme[b - 1].startswith("| `knowledge/hyprland-gkeep-geometry-r43.md`"))

    target = os.path.join(TREE, "corpus", "README.md")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as fh:
        fh.write("\n".join(readme) + "\n")
    p = subprocess.run(
        ["python3", "-I", os.path.join(LANE, "quality", "check-index-rows.py"),
         "--root", TREE], capture_output=True, text=True)
    print(p.stdout.strip())
    if p.stderr.strip():
        print(p.stderr.strip(), file=sys.stderr)
    check("check-index-rows on the simulated README exits 0", p.returncode == 0,
          f"rc={p.returncode}")
    check("check-index-rows reports errors=0", "errors=0" in p.stdout)

    print(f"SIM: {len(checks) - len(failed)}/{len(checks)} checks passed")
    for name in failed:
        print(f"FAILED: {name}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
