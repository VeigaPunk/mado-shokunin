#!/usr/bin/env python3
# R55ScribeP19b seat: generates block.md (C3 append-only correction) and after.md (base bytes + block).
# Q rows are generated from frozen-tables.json c3.q; the pin is checked against c3.pin_sha256 before use.
# Usage: python3 -I gen.py   (absolute paths only; writes only into this seat directory)
import hashlib
import json
import os
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-55/w1/R55ScribeP19b")
BASE_REV = "3b55b6e91e40f455dd56b2985e4ffc087ada92d5"
ENTRY = "corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"

tables = json.load(open(os.path.join(LANE, ".ufo/waves/round-55/frozen-tables.json"), encoding="utf-8"))
c3 = tables["c3"]

pin_path = os.path.join(LANE, c3["pin"])
pin_bytes = open(pin_path, "rb").read()
pin_sha = hashlib.sha256(pin_bytes).hexdigest()
if pin_sha != c3["pin_sha256"]:
    raise SystemExit("pin sha mismatch: %s != %s" % (pin_sha, c3["pin_sha256"]))
pin_lines = pin_bytes.decode("utf-8").split("\n")

base = subprocess.run(
    ["git", "-C", LANE, "show", BASE_REV + ":" + ENTRY],
    check=True, capture_output=True,
).stdout

q_rows = []
for q in c3["q"]:
    quote = q["quote"]
    if "|" in quote or "`" in quote:
        raise SystemExit("quote contains | or backtick: " + q["id"])
    if pin_lines[q["line"] - 1].strip() != quote:
        raise SystemExit("frozen quote is not stripped pin line: " + q["id"])
    q_rows.append("| %s | %s:%d | `%s` |" % (q["id"], q["pin"], q["line"], quote))

lines = []
lines.append("")
lines.append("## Correction (round 55): P23 supersedes P19")
lines.append("")
lines.append(
    "This block is appended after the unchanged round-53 entry above. It adds one corrected proposition, "
    "P23, which supersedes P19 only. The original P19 row stays above as history and must not be used as current "
    "evidence. P20 through P22 and the rest of this entry are not changed here. The correction is source-level: "
    "it states what the pinned `Actions::pass` text in `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp` "
    "tests and sends, and it makes no claim about a configured bind, a sent client event, or host behavior."
)
lines.append("")
lines.append(
    "The P19 wording was false because it made the keyboard PRESSED send exclusive to the `m_passPressed == 1` "
    "branch. The pinned text shows the keyboard PRESSED call again in the arm that Q08 opens: Q09 sends a keyboard "
    "key PRESSED there, and Q10 sends the matching keyboard RELEASED, so a value that is neither 1 (Q02) nor 0 (Q05) "
    "reaches a keyboard PRESSED send. The old quote covered only the `== 1` text (Q01 to Q03), so it could not show "
    "the other two arms. P23 therefore states all three arms and the keyboard-versus-pointer split inside each."
)
lines.append("")
lines.append(
    "Not claimed here: (a) where `m_passPressed` is set. The pin also writes it outside the quoted range: "
    "`sendKeyState` sets it to 1 or 0 around its `pass` calls (`Hyprland-ConfigActions.cpp:1603-1615`), and the header "
    "declares a default of -1 with the comment `-1 = dynamic (press+release)` (`Hyprland-ConfigActions.hpp:114`). "
    "This block does not say which setter reaches `pass` on any path. (b) which values reach the else arm. "
    "The else arm runs for any value other than 0 and 1; whether -1 or another value is stored when `pass` runs is "
    "not established here, and the `dynamic` comment is not evidence of it. (c) runtime delivery: that any send in "
    "any arm reaches a client, a focused window, or a keymap is not claimed. Pin sha256 is recorded in "
    "`verify.txt`; the non-author source-truth review named in the base entry is still required."
)
lines.append("")
lines.append("| ID | Supersedes | Proposition | Source row | Pin:anchor | Quote | Support |")
lines.append("|---|---|---|---|---|---|---|")
lines.append(
    "| P23 | P19 | `Actions::pass` sends modifier state (`sendKeyboardMods`) before its delivery branch and clears it after "
    "that branch. The branch tests `m_passPressed`. When `m_passPressed == 1`, a non-mouse key sends a keyboard key "
    "PRESSED and a mouse button sends a pointer button PRESSED. When `m_passPressed == 0`, a non-mouse key sends a "
    "keyboard key RELEASED and a mouse button sends a pointer button RELEASED. When `m_passPressed` is any other "
    "value (the `else` arm), a non-mouse key sends a keyboard key PRESSED and then a keyboard key RELEASED, and a "
    "mouse button sends a pointer button PRESSED and then a pointer button RELEASED. | S371 | "
    "Hyprland-ConfigActions.cpp:1554-1576 | Q01 to Q13 below | direct: Q01 to Q13 quote every call and branch test "
    "at the cited lines; runtime delivery not claimed. |"
)
lines.append("")
lines.append("Branch table for P23 (keyboard and pointer split inside each branch):")
lines.append("")
lines.append("| Branch | Non-mouse key (keyboard) | Mouse button (pointer) | Quotes |")
lines.append("|---|---|---|---|")
lines.append("| `m_passPressed == 1` | keyboard key PRESSED | pointer button PRESSED | Q02 to Q04 |")
lines.append("| `m_passPressed == 0` | keyboard key RELEASED | pointer button RELEASED | Q05 to Q07 |")
lines.append(
    "| any other value (`else` arm) | keyboard key PRESSED, then keyboard key RELEASED | pointer button PRESSED, "
    "then pointer button RELEASED | Q08 to Q12 |"
)
lines.append("")
lines.append("Quote rows for P23 (generated from `frozen-tables.json` `c3.q`; each quote is the stripped pin line):")
lines.append("")
lines.append("| ID | Pin:line | Quote |")
lines.append("|---|---|---|")
lines.extend(q_rows)
lines.append("")

block = "\n".join(lines).encode("utf-8")
after = base + block

open(os.path.join(SEAT, "block.md"), "wb").write(block)
open(os.path.join(SEAT, "after.md"), "wb").write(after)
print("base_bytes=%d block_bytes=%d after_bytes=%d" % (len(base), len(block), len(after)))
