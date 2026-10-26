#!/usr/bin/env python3
"""ScrSkillProvince index-row evidence driver (round 43, w1).

Builds a throwaway tree from the lane's `corpus/` (plus symlinks to `.ufo`,
`tools`, `quality` so the checker's path checks resolve), applies the drafted
README row there, runs `quality/check-index-rows.py` on it, runs five negative
controls, then runs `simulate-integration.py` on the same tree.  Writes one
receipt: `receipts/check-index-rows.txt`.

Nothing under the lane is written.  The scratch tree is disposable; the receipt
is the evidence.

    python3 -I .ufo/waves/round-43/w1/ScrSkillProvince/run-index-evidence.py
"""
import os
import re
import shutil
import subprocess
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(SEAT)))))
TREE = "/fast/scratch/hyaku/mado-r43/ScrSkillProvince/tree_ctl"
CHECKER = os.path.join(LANE, "quality", "check-index-rows.py")
RECEIPT = os.path.join(SEAT, "receipts", "check-index-rows.txt")
UNESCAPED = re.compile(r"(?<!\\)\|")

REGISTRY_STUBS = [
    "| S290 | Hyprland RegexMatchEngine.cpp - the rule match engine at the host's tag - https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/desktop/rule/matchEngine/RegexMatchEngine.cpp | code | A | scratch stub row for the checker run | :7-8 negative prefix, :16 FullMatch | scratch stub | mined | 2026-10-26 | on-release | corpus/knowledge/hyprland-gkeep-geometry-r43.md |",
    "| S291 | Hyprland WindowRuleApplicator.cpp - the static rule effects - https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/desktop/rule/windowRule/WindowRuleApplicator.cpp | code | A | scratch stub row for the checker run | :426 static_.size | scratch stub | mined | 2026-10-26 | on-release | corpus/knowledge/hyprland-gkeep-geometry-r43.md |",
    "| S292 | Hyprland DefaultFloatingAlgorithm.cpp - the floating placement path - https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/layout/algorithm/floating/default/DefaultFloatingAlgorithm.cpp | code | A | scratch stub row for the checker run | :49,55-56 | scratch stub | mined | 2026-10-26 | on-release | corpus/knowledge/hyprland-gkeep-geometry-r43.md |",
    "| S293 | Hyprland Target.cpp - the target box - https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/layout/target/Target.cpp | code | A | scratch stub row for the checker run | whole file | scratch stub | mined | 2026-10-26 | on-release | corpus/knowledge/hyprland-gkeep-geometry-r43.md |",
    "| S294 | Hyprland WindowTarget.cpp - the window target - https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/layout/target/WindowTarget.cpp | code | A | scratch stub row for the checker run | whole file | scratch stub | mined | 2026-10-26 | on-release | corpus/knowledge/hyprland-gkeep-geometry-r43.md |",
    "| S295 | Hyprland GeometricMovableAnimated.cpp - goal versus current - https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/desktop/view/types/GeometricMovableAnimated.cpp | code | A | scratch stub row for the checker run | :19-20 | scratch stub | mined | 2026-10-26 | on-release | corpus/knowledge/hyprland-gkeep-geometry-r43.md |",
    "| S296 | Hyprland HyprCtl.cpp - the clients reply - https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/debug/HyprCtl.cpp | code | A | scratch stub row for the checker run | :395, :427-428, :448, :2007 | scratch stub | mined | 2026-10-26 | on-release | corpus/knowledge/hyprland-gkeep-geometry-r43.md |",
    "| S297 | mado saved host gkeep.conf - byte copy of the host rule file - .ufo/waves/round-43/fetch/host-gkeep.conf | own-work | A | scratch stub row for the checker run | whole file | scratch stub | mined | 2026-10-26 | on-change | corpus/knowledge/hyprland-gkeep-geometry-r43.md |",
    "| S298 | mado saved host clients dump - hyprctl clients -j reduced - .ufo/waves/round-43/fetch/host-clients-r43.json | own-work | A | scratch stub row for the checker run | whole file | scratch stub | mined | 2026-10-26 | 90d | corpus/knowledge/hyprland-gkeep-geometry-r43.md |",
    "| S299 | gkeep ui excerpt - set_default_size - .ufo/waves/round-43/fetch/gkeep-ui-excerpt.py | own-work | A | scratch stub row for the checker run | whole file | scratch stub | mined | 2026-10-26 | on-change | corpus/knowledge/hyprland-gkeep-geometry-r43.md |",
]

STUB_NOTE = (
    "# hyprland gkeep geometry r43 (scratch stub, not the entry)\n\n"
    "What determines the size of the host's gkeep window, end to end: the rule text,\n"
    "the match engine, the floating algorithm, the animated goal box, the client's own\n"
    "request, and today's census.\n"
)


def sh(cmd, env=None):
    p = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def build_tree():
    if os.path.isdir(TREE):
        shutil.rmtree(TREE)
    os.makedirs(TREE)
    shutil.copytree(os.path.join(LANE, "corpus"), os.path.join(TREE, "corpus"))
    for d in (".ufo", "tools", "quality"):
        os.symlink(os.path.join(LANE, d), os.path.join(TREE, d))


def drafted_row():
    text = open(os.path.join(SEAT, "readme-row.md"), encoding="utf-8").read()
    rows = [l for l in text.splitlines()
            if l.startswith("| `knowledge/hyprland-gkeep-geometry-r43.md`")]
    assert len(rows) == 1, f"drafted rows: {len(rows)}"
    return rows[0]


def apply_row(row):
    path = os.path.join(TREE, "corpus", "README.md")
    lines = open(path, encoding="utf-8").read().splitlines()
    assert lines[69].startswith("| `knowledge/hyprland-focus-grab-r41.md`")
    assert lines[70] == ""
    out = lines[:70] + [row] + lines[70:]
    open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")

    spath = os.path.join(TREE, "corpus", "SOURCES.md")
    s = open(spath, encoding="utf-8").read().splitlines()
    idx = max(i for i, l in enumerate(s) if re.match(r"^\|\s*S\d{3}\s*\|", l))
    s = s[:idx + 1] + REGISTRY_STUBS + s[idx + 1:]
    open(spath, "w", encoding="utf-8").write("\n".join(s) + "\n")

    open(os.path.join(TREE, "corpus", "knowledge",
                      "hyprland-gkeep-geometry-r43.md"),
         "w", encoding="utf-8").write(STUB_NOTE)


def mutants(row):
    good = open(os.path.join(TREE, "corpus", "README.md"),
                encoding="utf-8").read()
    yield "M0 drafted row (no mutation)", good
    yield "M1 Sources cell emptied", good.replace(
        row, re.sub(r"\| `source:`.*\|\s*$", "| |", row))
    yield "M2 two cells only (the round-41 failure shape)", good.replace(
        row, "| `knowledge/hyprland-gkeep-geometry-r43.md` (MADO-R43-1) | "
             "What determines the size of the host's gkeep window, end to end |")
    yield "M3 an S-id the registry lacks", good.replace(
        row, row.replace("S299 in [SOURCES]", "S399 in [SOURCES]"))
    yield "M4 a Sources path that does not exist", good.replace(
        row, row.replace(".ufo/waves/round-43/fetch/",
                         ".ufo/waves/round-43/fetch-nope/"))
    yield "M5 the same row outside the coverage map", good + "\n" + row + "\n"


def main():
    build_tree()
    row = drafted_row()
    apply_row(row)

    lines = [
        "# seat ScrSkillProvince — check-index-rows.py evidence for the drafted README row",
        "# tool: quality/check-index-rows.py sha256 "
        + sh(["sha256sum", CHECKER])[1].split()[0],
        "# lane corpus/README.md sha256 "
        + sh(["sha256sum", os.path.join(LANE, "corpus", "README.md")])[1].split()[0]
        + " (unmodified; the row is applied only to the scratch tree)",
        "# scratch tree: copy of corpus/ + symlinks to .ufo, tools, quality;",
        "#   plus 10 SCRATCH-ONLY registry stub rows S290-S299 and a SCRATCH-ONLY stub note",
        "#   (written by this driver) — the entry seat owns the real registry append and note.",
        "",
    ]

    readme = os.path.join(TREE, "corpus", "README.md")
    good = open(readme, encoding="utf-8").read()
    for name, text in mutants(row):
        open(readme, "w", encoding="utf-8").write(text)
        rc, out, err = sh(["python3", "-I", CHECKER, "--root", TREE])
        lines.append(f"## {name}")
        lines.append(f"$ python3 -I quality/check-index-rows.py --root <scratch>")
        lines.append(out)
        if err:
            lines.append(f"stderr: {err}")
        lines.append(f"exit={rc}")
        lines.append("")
    open(readme, "w", encoding="utf-8").write(good)

    lines.append("## simulated integration (row + Frontier bullet in the scratch README)")
    rc, out, err = sh(["python3", "-I", os.path.join(SEAT, "simulate-integration.py")],
                      env={**os.environ, "SIM_TREE": TREE})
    lines.append("$ SIM_TREE=<scratch> python3 -I "
                 ".ufo/waves/round-43/w1/ScrSkillProvince/simulate-integration.py")
    lines.append(out)
    if err:
        lines.append(f"stderr: {err}")
    lines.append(f"exit={rc}")
    lines.append("")

    os.makedirs(os.path.dirname(RECEIPT), exist_ok=True)
    with open(RECEIPT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
