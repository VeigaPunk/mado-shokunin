#!/usr/bin/env python3
# R55ScribeP19a draft generator (leaf seat). Reads the frozen c3 table and the
# base blobs through git objects only; writes block.md and after.md into this dir.
# Q rows are emitted from frozen-tables.json c3.q (no retyped quotes).
import hashlib
import json
import os
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "3b55b6e91e40f455dd56b2985e4ffc087ada92d5"
FREEZE = "54dacbd843d64ba744cd3f1bdc2ec622e5010039"
ENTRY = "corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"
TABLES = ".ufo/waves/round-55/frozen-tables.json"
OUT = os.path.dirname(os.path.abspath(__file__))


def git_show(rev, path):
    return subprocess.run(
        ["git", "-C", REPO, "show", f"{rev}:{path}"],
        check=True, capture_output=True,
    ).stdout


def main():
    tables = json.loads(git_show(FREEZE, TABLES))
    c3 = tables["c3"]
    assert c3["entry"] == ENTRY, c3["entry"]
    assert c3["new_id"] == "P23" and c3["supersedes"] == "P19"
    pin_bytes = git_show(BASE, c3["pin"])
    pin_sha = hashlib.sha256(pin_bytes).hexdigest()
    assert pin_sha == c3["pin_sha256"], "pin sha mismatch"
    base = git_show(BASE, ENTRY)
    assert base.endswith(b"\n")
    pin_lines = pin_bytes.split(b"\n")

    q_rows = []
    for q in c3["q"]:
        quote = q["quote"]
        assert "|" not in quote and "`" not in quote and "\n" not in quote
        line = pin_lines[q["line"] - 1].strip(b" \t\r\n\v\f")
        assert line == quote.encode("utf-8"), (q["id"], line)
        q_rows.append(f"| {q['id']} | {q['pin']}:{q['line']} | `{quote}` |")

    q02 = next(q["quote"] for q in c3["q"] if q["id"] == "Q02")

    prop = (
        "`Actions::pass` calls `sendKeyboardMods(modMask, 0, 0, 0)`, then branches on `S.m_passPressed`. "
        "If `m_passPressed == 1`: `isMouse` false (keyboard) sends one PRESSED keyboard key (`key - 8`); "
        "`isMouse` true (pointer) sends one PRESSED pointer button. "
        "If `m_passPressed == 0`: keyboard sends one RELEASED keyboard key; pointer sends one RELEASED pointer button. "
        "Otherwise (any other value, the `else` arm): keyboard sends a PRESSED keyboard key then a RELEASED keyboard key; "
        "pointer sends a PRESSED pointer button then a RELEASED pointer button. "
        "It ends with `sendKeyboardMods(0, 0, 0, 0)`. "
        "This corrects P19: its `only when m_passPressed == 1` is false, the `else` arm also sends a PRESSED keyboard key."
    )
    support = (
        "direct: lines 1554-1576 are one contiguous excerpt with the three arms and the keyboard/pointer split; "
        "where `m_passPressed` is set and which values reach `else` are not in the excerpt (see Not claimed)."
    )
    assert "|" not in prop and "\n" not in prop

    lines = []
    lines.append("")
    lines.append("## Correction (round 55): P23 supersedes P19")
    lines.append("")
    lines.append(f"source: S371 — pin `{c3['pin']}` (sha256 {pin_sha}), base blob {BASE[:7]}.")
    lines.append("verified-at: 2026-10-28")
    lines.append("recheck: on-release")
    lines.append("")
    lines.append("Append-only. P19 above is kept unedited as history; this block supersedes P19 only. Basis: round-54 closure routed defect 1 (M54-5; QUALITY 104).")
    lines.append("")
    lines.append("| ID | Supersedes | Proposition | Source row | Pin:anchor | Quote | Support |")
    lines.append("|---|---|---|---|---|---|---|")
    lines.append(
        f"| P23 | P19 | {prop} | S371 | Hyprland-ConfigActions.cpp:1554-1576 | `{q02}` | {support} |"
    )
    lines.append("")
    lines.append("### Pinned lines (Q01–Q13, byte-equal to the round-52 pin after strip)")
    lines.append("")
    lines.append("| ID | Pin:line | Quote |")
    lines.append("|---|---|---|")
    lines.extend(q_rows)
    lines.append("")
    lines.append("### Not claimed")
    lines.append("")
    lines.append("- Where `m_passPressed` is assigned: the pin excerpt only reads it; no setter is in the pinned lines and none is claimed.")
    lines.append("- Which values reach the `else` arm at runtime: the pin shows the arm exists, not that any caller passes a value other than 0 or 1.")
    lines.append("- Runtime delivery: no client, compositor or host event is claimed; this correction is source-level only.")
    lines.append("- P23 is not reviewed by a non-author; the review gate in the entry's Limits section still applies.")
    lines.append("")
    block = "\n".join(lines)
    block_b = block.encode("utf-8")
    after_b = base + block_b

    with open(os.path.join(OUT, "block.md"), "wb") as f:
        f.write(block_b)
    with open(os.path.join(OUT, "after.md"), "wb") as f:
        f.write(after_b)
    print(f"gen: base_bytes={len(base)} block_bytes={len(block_b)} after_bytes={len(after_b)} q_rows={len(q_rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
