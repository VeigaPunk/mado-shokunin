#!/usr/bin/env python3
"""Build round-34 pre-data controls and print the counter commands.

Not the claim counter. Exit 0 if every required control has the expected
verdict. Exit 1 if a kill control meets or the golden does not.
"""
from __future__ import annotations

import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
W = LANE / ".ufo/waves/round-34"
FETCH = W / "fetch"
C1 = W / "c1/count.py"
C1F = W / "c1/frozen.json"
C2 = W / "c2/count.py"
C2F = W / "c2/frozen.json"
ENTRY = "corpus/knowledge/waybar-module-text-route-r25.md"
Q1 = "$XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr"
Q2 = 'm_ipc.registerForIPC("activewindow", this);'
ENTRY_TEXT = (
    "gate-quote: S201 " + Q1 + "\n"
    "gate-quote: S202 " + Q2 + "\n"
)
ROW = (
    "| {sid} | waybar | code | A | event socket | anchor | teaches | mined | "
    "2026-10-24 | 90d | corpus/knowledge/waybar-module-text-route-r25.md |\n"
)
SOURCES = (
    "# control\n\n## Registry\n\n"
    "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|\n"
    + ROW.format(sid="S201")
    + ROW.format(sid="S202")
)


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, text=True, capture_output=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def write_tree(root: Path, fetches: str) -> None:
    if root.exists():
        shutil.rmtree(root)
    (root / "corpus/knowledge").mkdir(parents=True)
    (root / ".ufo/waves/round-34/fetch").mkdir(parents=True)
    (root / ENTRY).write_text(ENTRY_TEXT)
    (root / "corpus/SOURCES.md").write_text(SOURCES)
    dest = root / ".ufo/waves/round-34/fetch"
    if fetches == "copy":
        shutil.copyfile(FETCH / "S201.bin", dest / "S201.bin")
        shutil.copyfile(FETCH / "S202.bin", dest / "S202.bin")
    elif fetches == "symlink":
        os.symlink(FETCH / "S201.bin", dest / "S201.bin")
        os.symlink(FETCH / "S202.bin", dest / "S202.bin")
    elif fetches == "hardlink":
        os.link(FETCH / "S201.bin", dest / "S201.bin")
        os.link(FETCH / "S202.bin", dest / "S202.bin")
    else:
        raise SystemExit(f"unknown fetches {fetches}")


def main() -> None:
    receipts = W / "controls"
    receipts.mkdir(parents=True, exist_ok=True)
    golden = W / "controls/golden"
    crib = W / "controls/symlink-crib"
    entry_crib = W / "controls/symlink-entry"
    rows_only = W / "controls/rows-only"
    entries_only = W / "controls/entries-only"
    write_tree(golden, "copy")
    write_tree(crib, "symlink")
    write_tree(rows_only, "copy")
    (rows_only / ENTRY).unlink()
    write_tree(entries_only, "copy")
    (entries_only / "corpus/SOURCES.md").write_text("# no rows\n")
    write_tree(entry_crib, "copy")
    real_entry = entry_crib / ENTRY
    held = entry_crib / "held-entry.md"
    held.write_text(real_entry.read_text())
    real_entry.unlink()
    os.symlink(held, real_entry)

    hard = W / "controls/hardlink-work"
    write_tree(hard, "hardlink")
    nlink = (hard / ".ufo/waves/round-34/fetch/S201.bin").stat().st_nlink

    cases = [
        ("c1-donothing", [sys.executable, "-I", str(C1), "--root", str(LANE), "--frozen", str(C1F)], 1),
        ("c1-symlink-crib", [sys.executable, "-I", str(C1), "--root", str(crib), "--frozen", str(C1F)], 1),
        ("c1-symlink-entry", [sys.executable, "-I", str(C1), "--root", str(entry_crib), "--frozen", str(C1F)], 1),
        ("c1-rows-only", [sys.executable, "-I", str(C1), "--root", str(rows_only), "--frozen", str(C1F)], 1),
        ("c1-entries-only", [sys.executable, "-I", str(C1), "--root", str(entries_only), "--frozen", str(C1F)], 1),
        ("c1-hardlink", [sys.executable, "-I", str(C1), "--root", str(hard), "--frozen", str(C1F)], 1),
        ("c1-golden", [sys.executable, "-I", str(C1), "--root", str(golden), "--frozen", str(C1F)], 0),
        ("c2-donothing", [sys.executable, "-I", str(C2), "--repo", str(LANE), "--scorecard", str(LANE / "SCORECARD.md"), "--frozen", str(C2F)], 1),
    ]
    junk = receipts / "c2-junk-card.md"
    junk.write_text("r34-s189-line: line=128\n")
    cases.append(("c2-junk", [sys.executable, "-I", str(C2), "--repo", str(LANE), "--scorecard", str(junk), "--frozen", str(C2F)], 1))
    reach = receipts / "c2-reachable-card.md"
    reach.write_text( (LANE / "SCORECARD.md").read_text() + "\nr34-s189-line: line=169\n")
    cases.append(("c2-reachable", [sys.executable, "-I", str(C2), "--repo", str(LANE), "--scorecard", str(reach), "--frozen", str(C2F)], 0))

    # r33 counter on its own crib, if present — must still MET. Do not edit it.
    r33_crib = LANE / ".ufo/waves/round-33/scratch/CriticC1Junk"
    r33_count = LANE / ".ufo/waves/round-33/c1/count.py"
    r33_frozen = LANE / ".ufo/waves/round-33/c1/frozen.json"
    failed = 0
    if r33_crib.is_dir():
        code, out = run([sys.executable, "-I", str(r33_count), "--root", str(r33_crib), "--frozen", str(r33_frozen)])
        (receipts / "r33-counter-on-its-crib.txt").write_text(f"exit={code}\n{out}\nnlink_note=not this counter\n")
        print(f"r33-counter-on-its-crib exit={code} {out}")
        if code != 0 or "TARGET_MET" not in out:
            failed += 1
    for name, cmd, expect in cases:
        code, out = run(cmd)
        text = f"exit={code}\n{out}\n"
        if name == "c1-hardlink":
            text += f"nlink={nlink}\n"
        (receipts / f"{name}.txt").write_text(text)
        ok = code == expect and ("TARGET_MET" if expect == 0 else "TARGET_MISSED") in out
        print(f"{name} exit={code} expect={expect} ok={ok} {out}")
        if not ok:
            failed += 1
    # indented collision guard: the prompt's grep extractor, staged set vs indented S197
    guard = W / "assimilation"
    guard.mkdir(parents=True, exist_ok=True)
    fix = guard / "indented-fixture.md"
    fix.write_text("  | S197 | collision fixture |\n")
    staged = Path("/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md")
    extract = "grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' | grep -oE 'S[0-9]+' | sort"
    zero_extract = "grep -oE '^\\|[[:space:]]*S[0-9]{3,}' | grep -oE 'S[0-9]+' | sort"
    subprocess.check_call(f"{extract} > {guard}/fixture-ids", shell=True, stdin=open(fix))
    subprocess.check_call(f"{zero_extract} > {guard}/fixture-zero-ids", shell=True, stdin=open(fix))
    subprocess.check_call(f"{extract} > {guard}/staged-ids", shell=True, stdin=open(staged))
    subprocess.check_call(f"comm -12 {guard}/fixture-ids {guard}/staged-ids > {guard}/fixture-collisions", shell=True)
    coll = (guard / "fixture-collisions").read_text().strip()
    zero = (guard / "fixture-zero-ids").read_text().strip()
    (receipts / "indented-guard.txt").write_text(
        f"spaced={(guard / 'fixture-ids').read_text().strip()} column_zero={zero!r} collisions={coll!r}\n"
    )
    print("indented-guard", coll, "zero", zero)
    if coll != "S197" or zero:
        failed += 1
    shutil.rmtree(hard)
    print(f"failed={failed}")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
