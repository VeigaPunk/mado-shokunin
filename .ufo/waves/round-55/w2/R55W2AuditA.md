# R55W2AuditA: report (sentence-to-pin audit of K01, K02, K03, K08, E01, E02, E08)

Deliverable: `.ufo/waves/round-55/w2/R55W2AuditA/audit.md` (one table row per audited row). Receipts: `.ufo/waves/round-55/w2/R55W2AuditA/receipts/`.

## What was attacked
The seven rows of `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` named in the assignment. For each: proposition cell, pin line, neighbouring lines, and an upstream re-open.

## Commands and decisive output
- Pin quote check (`python3 -I receipts/check_rows.py`): all seven quotes are exact substrings of the cited pin line (`exact_substring=True` for K01, K02, K03, K08, E01, E02, E08).
- Upstream re-open: `curl` of `raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/{managers/input/InputManager.cpp, devices/IKeyboard.cpp, config/legacy/ConfigManager.cpp}`. `cmp` against the committed pins: IDENTICAL for all three. sha256 equals `frozen-tables.json` `c1.pin_sha256` (feedf32e…, 8a800efe…, 9db68cf4…).
- Neighbour lines: read with `sed -n` on the upstream copies (receipts/neighbour-and-upstream.txt).
- Scratch copies only, under `/fast/scratch/hyaku/mado-r55/R55W2AuditA/`, removed before yield. No lane file was edited, no git or jj command was run, no hyprctl command was run, no mutation test was performed.

## Verdicts per target
| Target | Verdict | Evidence pointer |
|---|---|---|
| K01 | SUPPORTED | audit.md row K01; InputManager.cpp:1213-1220 |
| K02 | SUPPORTED | audit.md row K02; InputManager.cpp:1221 |
| K03 | SUPPORTED | audit.md row K03; InputManager.cpp:1223 |
| K08 | SUPPORTED (boundary named only in the audit; optional cell wording given) | audit.md row K08; IKeyboard.cpp:61-64, 77-80, 120 |
| E01 | SUPPORTED; reach to the three keys HELD as the cell says | audit.md row E01; ConfigManager.cpp:1119, 1131-1134 |
| E02 | SUPPORTED | audit.md row E02; IKeyboard.cpp:60, 120, 122, 148 |
| E08 | SUPPORTED | audit.md row E08; InputManager.cpp:1135-1195, 1208 |

No row is OVERREACH or UNSUPPORTED. No row is BROKEN. None of the rows makes a runtime claim.

## Provenance finding (the one thing I would fix)
The doc says the Extra rows are "checked by the generator and by verify.py". The integrated generator (`.ufo/waves/round-55/integrate/build-entry.py`) does not check extra rows. The only extra-row check I found is `.ufo/waves/round-55/w1/R55ScribeEntryA/verify.py:92-105`, which is a w1 seat artifact outside the integrated tree. E01, E02 and E08 are not in `frozen-tables.json`. The quotes are still exact substrings. Fix: either integrate the extra-row check or change the sentence to name the seat script and say it is not integrated (audit.md P1).

## Out-of-scope neighbour (for the K10/K11 auditor)
`Hyprland-IKeyboard.cpp:147` calls `g_pSeatManager->updateActiveKeyboardData()` at the end of setKeymap. The chain in the doc does not mention it (audit.md P2).

## Could not verify
- Runtime behaviour of any row: out of scope by the doc's own Limits, and not claimed.
- Whether a `verify.py` the doc cites exists in the integrated tree: I searched and found only the w1 copy.
- The `hyprctl` host rows were not part of my assignment and were not re-read.

## Tooling
No tool was installed or upgraded. No pacman transaction was run. Network reads: three raw.githubusercontent.com files at the pinned commit.
