#!/usr/bin/env python3
"""S207 row mutation harness for sources-census.sh validate.

Reads the pristine copy of corpus/SOURCES.md, emits one isolated mutant
registry per probe (each in its own --file root with the lane's used-by
resolution farm symlinked in), runs the census validator on each, and writes a
TSV/Markdown ledger. Writes only under the scratch directory.
"""
import hashlib
import json
import os
import subprocess
import sys

SCRATCH = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SCRIPT = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
TODAY = "2026-10-25"
PRISTINE = os.path.join(SCRATCH, "pristine.SOURCES.md")
MUTROOT = os.path.join(SCRATCH, "mutants")
OUTROOT = os.path.join(SCRATCH, "out")

# E11 resolves used-by paths against dirname(file)/.. — mirror every lane-root
# entry into each mutant root so the baseline stays resolvable and only the
# mutated row can change the verdict.
FARM_ROOT = [".ufo", "tools", "quality", "SKILL.md", "considerthese",
             "plans", "reports", "README.md", "AGENTS.md", "LOG.md",
             "MINT.md", "PROVINCE.md", "SCORECARD.md"]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_pristine() -> list[str]:
    with open(PRISTINE, "r", encoding="utf-8") as fh:
        # keep newlines so byte-exact reconstruction is possible
        return fh.read().splitlines(keepends=True)


def split_row(line: str) -> list[str]:
    """| a | b |\n -> ['', ' a ', ' b ', ''] (newline stripped)."""
    had_nl = line.endswith("\n")
    body = line.rstrip("\n")
    return body.split("|"), had_nl


def join_row(cells: list[str], had_nl: bool) -> str:
    return "|".join(cells) + ("\n" if had_nl else "")


def find_s207(lines: list[str]) -> int:
    hits = [i for i, ln in enumerate(lines) if ln.startswith("| S207 |")]
    if len(hits) != 1:
        sys.exit(f"expected exactly one S207 row, found {hits}")
    return hits[0]


def build_mutant(lines: list[str], spec: dict) -> tuple[list[str], str]:
    """Apply one spec. Returns (new_lines, one-line diff description)."""
    idx = find_s207(lines)
    cells, had_nl = split_row(lines[idx])
    op = spec["op"]
    if op == "set_cell":
        col = spec["col"]           # 0-based index into split('|') fields
        old = cells[col]
        cells[col] = spec["value"]
        new = join_row(cells, had_nl)
        return lines[:idx] + [new] + lines[idx + 1:], f"cell[{col}] {old.strip()!r} -> {spec['value'].strip()!r}"
    if op == "drop_cell":
        col = spec["col"]
        old = cells[col]
        del cells[col]
        new = join_row(cells, had_nl)
        return lines[:idx] + [new] + lines[idx + 1:], f"deleted cell[{col}] {old.strip()!r}"
    if op == "duplicate_row":
        # insert an exact copy of S207 right after the last registry row (S210)
        last = max(i for i, ln in enumerate(lines) if ln.startswith("| S2"))
        copy = lines[idx]
        return lines[:last + 1] + [copy] + lines[last + 1:], "duplicated S207 row after S210"
    raise SystemExit(f"unknown op {op}")


def make_root(name: str, lines: list[str]) -> str:
    root = os.path.join(MUTROOT, name)
    corpus = os.path.join(root, "corpus")
    os.makedirs(corpus, exist_ok=True)
    for entry in FARM_ROOT:
        src = os.path.join(LANE, entry)
        if not os.path.exists(src):
            continue
        dst = os.path.join(root, entry)
        if not os.path.lexists(dst):
            os.symlink(src, dst)
    for entry in os.listdir(os.path.join(LANE, "corpus")):
        if entry == "SOURCES.md":
            continue
        dst = os.path.join(corpus, entry)
        if not os.path.lexists(dst):
            os.symlink(os.path.join(LANE, "corpus", entry), dst)
    with open(os.path.join(corpus, "SOURCES.md"), "w", encoding="utf-8") as fh:
        fh.writelines(lines)
    return os.path.join(corpus, "SOURCES.md")


def run(mode: str, path: str) -> tuple[int, str]:
    proc = subprocess.run(
        ["bash", SCRIPT, mode, "--file", path, "--today", TODAY],
        capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


SPECS = [
    # --- the five assigned probes -------------------------------------------
    dict(name="M01-status-queued", op="set_cell", col=8, value=" queued ",
         expect="no E-code (queued is a legal status)", axis="status enum"),
    dict(name="M02-recheck-prose", op="set_cell", col=10,
         value=" after the next hypridle release ",
         expect="E09", axis="recheck grammar"),
    dict(name="M03-usedby-stray", op="set_cell", col=11, value=" stray-token ",
         expect="E11", axis="used-by existence"),
    dict(name="M04-drop-cell", op="drop_cell", col=6, expect="E01",
         axis="column count"),
    dict(name="M05-duplicate-row", op="duplicate_row", expect="E03",
         axis="identity"),
    # --- discriminating controls around the same fields ---------------------
    dict(name="M06-recheck-hyphen-token", op="set_cell", col=10,
         value=" after-hypridle-release ", expect="E09", axis="recheck grammar"),
    dict(name="M07-recheck-digit-first", op="set_cell", col=10,
         value=" 30 days ", expect="E09", axis="recheck grammar"),
    dict(name="M08-usedby-empty", op="set_cell", col=11, value=" ",
         expect="E11", axis="used-by existence"),
    dict(name="M09-status-watch", op="set_cell", col=8, value=" watch ",
         expect="E07", axis="status enum"),
    dict(name="M10-queued-plus-stray", op="set_cell", col=8, value=" queued ",
         also=[(11, " stray-token ")], expect="E11", axis="status x used-by"),
    dict(name="M11-usedby-two-paths", op="set_cell", col=11,
         value=" corpus/knowledge/idle-lock-offered-in-the-bar-r15.md,corpus/knowledge/missing-mutant.md ",
         expect="E11", axis="used-by list"),
    dict(name="M12-id-short", op="set_cell", col=1, value=" S20 ", expect="E02",
         axis="identity"),
    dict(name="M13-recheck-emdash", op="set_cell", col=10, value=" \u2014 ",
         expect="E09", axis="recheck grammar"),
    dict(name="M14-recheck-empty", op="set_cell", col=10, value=" ",
         expect="E09", axis="recheck grammar"),
    dict(name="M15-status-capital", op="set_cell", col=8, value=" Queued ",
         expect="E07", axis="status enum"),
    dict(name="M16-status-rejected", op="set_cell", col=8, value=" rejected ",
         expect="no E-code", axis="status enum"),
    dict(name="M17-recheck-bad-date", op="set_cell", col=10, value=" 2026-13-45 ",
         expect="E09", axis="recheck grammar"),
    dict(name="M18-rejected-plus-stray", op="set_cell", col=8, value=" rejected ",
         also=[(11, " stray-token ")], expect="E11", axis="status x used-by"),
]


def main() -> int:
    os.makedirs(MUTROOT, exist_ok=True)
    os.makedirs(OUTROOT, exist_ok=True)
    pristine = read_pristine()
    pristine_bytes = b"".join(x.encode() for x in pristine)
    pristine_hash = sha256(pristine_bytes)
    rows = []

    # baseline against a farm root of its own (mutants/ base, no mutation)
    base_path = make_root("M00-baseline", pristine)
    rc, out = run("validate", base_path)
    rows.append(dict(name="M00-baseline", op="none", expect="ok/rc0", got_rc=rc,
                     findings=[l for l in out.splitlines() if "\tE" in l or "\tW" in l],
                     s207=[l for l in out.splitlines() if "\tS207\t" in l or "\tS207 " in l],
                     sha256=sha256(open(base_path, "rb").read()),
                     description="pristine copy, no mutation"))
    with open(os.path.join(OUTROOT, "M00-baseline.txt"), "w") as fh:
        fh.write(out)

    for spec in SPECS:
        name = spec["name"]
        lines, desc = build_mutant(pristine, spec)
        for col, value in spec.get("also", []):
            idx = find_s207(lines)
            cells, had_nl = split_row(lines[idx])
            desc += f"; cell[{col}] -> {value.strip()!r}"
            cells[col] = value
            lines[idx] = join_row(cells, had_nl)
        path = make_root(name, lines)
        rc, out = run("validate", path)
        with open(os.path.join(OUTROOT, name + ".txt"), "w") as fh:
            fh.write(out)
        codes = sorted({l.split("\t")[1] for l in out.splitlines()
                        if len(l.split("\t")) > 2 and l.split("\t")[1] in
                        ("E%02d" % i for i in range(1, 13))})
        warnings = sorted({l.split("\t")[1] for l in out.splitlines()
                           if len(l.split("\t")) > 2 and l.split("\t")[1].startswith("W")})
        s207 = [l for l in out.splitlines() if "\tS207" in l]
        rc_overdue = None
        overdue_out = ""
        if name in ("M02-recheck-prose", "M06-recheck-hyphen-token",
                    "M07-recheck-digit-first", "M17-recheck-bad-date"):
            rc_overdue, overdue_out = run("overdue", path)
            with open(os.path.join(OUTROOT, name + ".overdue.txt"), "w") as fh:
                fh.write(overdue_out)
        rows.append(dict(name=name, op=spec["op"], description=desc,
                         expect=spec["expect"], got_rc=rc, codes=codes,
                         warnings=warnings, s207=s207,
                         sha256=sha256(open(path, "rb").read()),
                         overdue_rc=rc_overdue,
                         overdue_s207=[l for l in overdue_out.splitlines() if "S207" in l]))

    # restore evidence: the working copy must still equal pristine byte for byte
    restored = hashlib.sha256(open(os.path.join(SCRATCH, "corpus", "SOURCES.md"), "rb").read()).hexdigest()
    rc_final, out_final = run("validate", os.path.join(SCRATCH, "corpus", "SOURCES.md"))
    payload = dict(pristine_sha256=pristine_hash, restored_sha256=restored,
                   restored_rc=rc_final,
                   restored_ok=any(l.endswith("\tok\t" + os.path.join(SCRATCH, "corpus", "SOURCES.md")) for l in out_final.splitlines()),
                   rows=rows)
    with open(os.path.join(OUTROOT, "results.json"), "w") as fh:
        json.dump(payload, fh, indent=2)
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
