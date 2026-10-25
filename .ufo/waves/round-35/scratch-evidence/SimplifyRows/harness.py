#!/usr/bin/env python3
"""YAGNI deletion harness for the round-35 row set.

Builds a throwaway root that mirrors only what PRED-C1-r35-v1 reads
(corpus/ + .ufo/waves/round-35/fetch), applies one mutation, runs the
unmodified lane counter, and prints the verdict. Never writes outside
.ufo/waves/round-35/scratch/SimplifyRows/.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
BASE = LANE / ".ufo/waves/round-35/scratch/SimplifyRows"
COUNTER = LANE / ".ufo/waves/round-35/c1/count.py"
FROZEN = LANE / ".ufo/waves/round-35/c1/frozen.json"
SRC = "corpus/SOURCES.md"
ENTRIES = {
    "S203": "corpus/knowledge/idle-lock-never-asked-r12.md",
    "S204": "corpus/knowledge/idle-lock-never-asked-r12.md",
    "S205": "corpus/knowledge/idle-lock-chain-armed-r14.md",
    "S206": "corpus/knowledge/idle-lock-offered-in-the-bar-r15.md",
    "S207": "corpus/knowledge/idle-lock-offered-in-the-bar-r15.md",
    "S208": "corpus/knowledge/idle-lock-offered-in-the-bar-r15.md",
    "S209": "corpus/knowledge/idle-lock-offered-in-the-bar-r15.md",
    "S210": "corpus/knowledge/idle-lock-offered-in-the-bar-r15.md",
}


def mirror(name: str) -> Path:
    root = BASE / "exp" / name / "root"
    if root.exists():
        shutil.rmtree(root)
    (root / "corpus").mkdir(parents=True)
    shutil.copy2(LANE / SRC, root / SRC)
    for rel in {ENTRIES[k] for k in ENTRIES}:
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(LANE / rel, dest)
    shutil.copytree(LANE / ".ufo/waves/round-35/fetch", root / ".ufo/waves/round-35/fetch")
    (root / ".ufo/waves/round-35/c1").mkdir(parents=True)
    return root


def drop_row(root: Path, sid: str) -> None:
    path = root / SRC
    lines = path.read_text().splitlines(keepends=True)
    kept = [ln for ln in lines if not ln.lstrip().startswith(f"| {sid} |")]
    assert len(kept) == len(lines) - 1, f"{sid}: row not uniquely dropped"
    path.write_text("".join(kept))


def drop_gate_quote(root: Path, sid: str) -> None:
    path = root / ENTRIES[sid]
    text = path.read_text()
    needle = f"gate-quote: {sid} "
    kept = [ln for ln in text.splitlines(keepends=True) if not ln.startswith(needle)]
    assert len(kept) == len(text.splitlines(keepends=True)) - 1, f"{sid}: quote not dropped"
    path.write_text("".join(kept))


def drop_entry_source(root: Path, sid: str) -> None:
    path = root / ENTRIES[sid]
    text = path.read_text()
    needle = f"source: {sid} "
    kept = [ln for ln in text.splitlines(keepends=True) if not ln.startswith(needle)]
    assert len(kept) == len(text.splitlines(keepends=True)) - 1
    path.write_text("".join(kept))


def replace_cell(root: Path, sid: str, col: int, value: str) -> None:
    """Replace one pipe-delimited cell of a registry row (1-based, id=1)."""
    path = root / SRC
    out = []
    hit = 0
    for ln in path.read_text().splitlines(keepends=True):
        if ln.lstrip().startswith(f"| {sid} |"):
            parts = ln.rstrip("\n").split("|")
            parts[col] = f" {value} "
            out.append("|".join(parts) + "\n")
            hit += 1
        else:
            out.append(ln)
    assert hit == 1
    path.write_text("".join(out))


def add_superseding_row(root: Path, new_sid: str, old_sid: str) -> None:
    """Append a correction row per CORPUS.md rule 2 (teaches opens 'supersedes S0NN —')."""
    row = (
        f"| {new_sid} | host idle-toggle implementation - the script the bar click and the menu "
        f"entry run - /home/vgpnk/.local/share/omarchy/bin/omarchy-toggle-idle | own-work | A | "
        f"The mechanism behind {old_sid}: the idle toggle keeps no state file and writes nothing to "
        f"the toggle-state directory, it starts or stops hypridle | "
        f"body lines 3-12 at /home/vgpnk/.local/share/omarchy/bin/omarchy-toggle-idle, "
        f"218 B, file sha256 8f7e6f4c1b2a9d0e5c3a7b6d4f2e1c0a9b8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f; "
        f"receipt .ufo/waves/round-35/fetch/S210.receipt.txt sha256 "
        f"ef282e386cdfb686fd331f4ed2fa7f0a33faf3ef4714844639b3eee4790b8726 | "
        f"supersedes {old_sid} - the toggles directory cannot hold an idle entry because the idle "
        f"toggle never writes there | mined | 2026-10-25 | on-change | "
        f"corpus/knowledge/idle-lock-offered-in-the-bar-r15.md |\n"
    )
    path = root / SRC
    path.write_text(path.read_text() + row)


def run(root: Path, frozen: Path | None = None) -> tuple[str, int]:
    proc = subprocess.run(
        [sys.executable, "-I", str(COUNTER), "--root", str(root),
         "--frozen", str(frozen or FROZEN)],
        capture_output=True, text=True,
    )
    return (proc.stdout.strip() + proc.stderr.strip()).strip(), proc.returncode


def main() -> None:
    exp = sys.argv[1]
    root = mirror(exp)
    if exp == "e0-base":
        pass
    elif exp == "e1-drop-s204":
        drop_row(root, "S204")
    elif exp == "e2-drop-s210":
        drop_row(root, "S210")
    elif exp == "e3-drop-s203":
        drop_row(root, "S203")
    elif exp == "e4-drop-s204-and-quote":
        drop_row(root, "S204")
        drop_gate_quote(root, "S204")
    elif exp == "e5-drop-s204-s210-full":
        for sid in ("S204", "S210"):
            drop_row(root, sid)
            drop_gate_quote(root, sid)
            drop_entry_source(root, sid)
    elif exp == "e6-drop-sid-from-frozen":
        spec = json.loads(FROZEN.read_text())
        spec["entries"]["corpus/knowledge/idle-lock-never-asked-r12.md"].remove("S204")
        frozen = BASE / "exp" / exp / "frozen-no-s204.json"
        frozen.write_text(json.dumps(spec, indent=1) + "\n")
        drop_row(root, "S204")
    elif exp == "e7-substitute-source":
        # S204's "source" becomes a genuinely distinct document; receipt digest kept.
        replace_cell(root, "S204", 2,
                     "host idle-toggle implementation - the script the bar click and the menu entry run - "
                     "/home/vgpnk/.local/share/omarchy/bin/omarchy-toggle-idle")
    elif exp == "e8-anchor-lie":
        replace_cell(root, "S206", 6,
                     "lines 999-1000 at /home/vgpnk/.config/waybar/config.jsonc, 1 B, file sha256 deadbeef; "
                     "receipt .ufo/waves/round-35/fetch/S206.receipt.txt sha256 1d30e4a999b53d5288369edc7573d7ceee0aef99570a55d781c4625440a938d5")
    elif exp == "e9-teaches-lie":
        replace_cell(root, "S210", 7, "The idle lock has a recorded entry in this directory")
    elif exp == "e11-s210-source-rewrite":
        # Same sid, same receipt digest in the anchor, primary document re-pointed
        # at the script the click runs (which is what the entry's INF needs).
        replace_cell(root, "S210", 2,
                     "host idle-toggle implementation - the command the bar click and the menu entry run - "
                     "/home/vgpnk/.local/share/omarchy/bin/omarchy-toggle-idle")
    elif exp == "e12-s204-rescope":
        replace_cell(root, "S204", 5,
                     "No omarchy-toggle invocation in the user journal within its retained window "
                     "(2026-10-23T07:18 to the read date)")
    elif exp == "e13-supersede-append":
        add_superseding_row(root, "S211", "S210")
    elif exp == "e14-supersede-and-uncite":
        add_superseding_row(root, "S211", "S210")
        drop_entry_source(root, "S210")
        drop_gate_quote(root, "S210")
    elif exp == "e10-merge-into-s203":
        drop_row(root, "S204")
    else:
        raise SystemExit(f"unknown experiment {exp}")

    frozen = BASE / "exp" / exp / "frozen-no-s204.json"
    out, code = run(root, frozen if frozen.is_file() else None)
    print(f"{exp}: exit={code} {out}")


if __name__ == "__main__":
    main()
