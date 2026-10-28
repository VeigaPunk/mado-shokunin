# R55W2CritEntryProse — report

Seat: R55W2CritEntryProse (wave w2, falsify). Leaf member, no subagent dispatch.
Target: non-row prose of `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` at 57584ed67716340b3d466fa04333ac0bab3fb79e. Sections: `What this entry settles`, `What stays UNKNOWN`, `Chain`, `Limits`, `How to verify`.
Deliverable: `.ufo/waves/round-55/w2/R55W2CritEntryProse/prose-attack.md` (sentence-by-sentence table, receipts copied alongside: `freeze-verify-run.txt`, `freeze-verify-v2-run.txt`, `c1-counter-run.txt`, `how-to-verify-run.txt`, `extra-receipts.txt`).

## What ran
- Every How-to-verify command, read-only, from the lane root: `sha256sum fetch/*` (exit 0), `freeze-verify.py` (exit 0, ends OK), the three `sed` commands (print the cited lines), `sed` on host-input.conf (lines 14,15,18), `cat host-getoption.json`, the three `hyprctl getoption … -j` (outputs equal H04-H06).
- Additional read-only: `freeze-verify-v2.py` (exit 0, OK), `quality/counters/c1-r55-kbd-entry.py --rev 57584ed… --work <scratch>` (exit 0, `verdict=TARGET_MET missed=none`), unlisted `sed` prints of IKeyboard 122-132, legacy 1119-1134, Seat 441-445 and 603-608, SeatManager 170-182, InputManager 1135/1195, Seat 336-352, `hyprctl version`, `hyprctl devices -j` (keyboard `main` field only).
- Upstream re-open (network reads, raw URLs): Hyprland commit efb50993… for all seven Hyprland pins, tag `refs/tags/v0.56.2` for two, gitlab wayland `1.26.0` for the XML. All sha256-equal to the pins.
- E01-E13 quotes checked as substrings of the named pin lines in Python (13/13). K/H table quote cells compared with `frozen-tables.json` and `frozen-tables-v2.json` (23/24 equal to both; K16 equal to v2 only).

## What did not run / not done
- Nothing mutated: no lane file edited, no git/jj command, no commit, no hyprctl keyword/dispatch/reload. Mutation tests: none in this seat.
- No tools installed or upgraded (none needed; `curl`, `python3`, `sed`, `hyprctl` were present). No pacman activity.
- Scratch `/fast/scratch/hyaku/mado-r55/R55W2CritEntryProse/` (upstream copies, counter work dir) is removed before yield.

## Verdicts (per target; details and line evidence in prose-attack.md §1-§5)
- `settles` S2, S4, S6, S7, S10, S11 — SURVIVES. S6 "no else" is entailed by the source but not printed by any How-to-verify command (H4).
- `settles` S1 ("getDeviceInt with that fallback"), S3, S8 (line 605 gate), C2 ("called from setupKeyboard"), C4 — ROW-GAP: entailed by pinned source at legacy:1132, InputManager:1135, Seat:605; cited rows do not carry those lines.
- `settles` S5 — SURVIVES but incomplete: line 1271 is a nine-term test; the prose names only the repeat/delay pair.
- `settles` S9 ("sends only when the owner is present … not both equal to the last sent values", cites K11, E10, K12) — ROW-GAP. Source (Seat.cpp:442, 444) entails it; no cited row carries the owner term, the equality term, or the `m_lastRate` assignment.
- UNKNOWN U1 (`set: true` meaning, "no pinned source row defines it") — UNKNOWN WRONG-PLACED. `corpus/knowledge/hyprctl-getoption-native-forms-r40.md:20,26` holds the meaning as a measurement (S279: set true = declared in some file of the tree); the entry's own Joining section points to that file. Host consistency: all three keys are declared in host-input.conf and read `"set": true`.
- UNKNOWN U2 (enforcement of min/max), U5 (client bind v4+), U6 (numlock on host keymap), U7 (observed-claims) — SURVIVES as UNKNOWN.
- UNKNOWN U3 — the reach question stays open and the consequence is correctly labelled INFERENCE, but it says "clamped", see C1.
- UNKNOWN U4 (`m_keyboard`) — SURVIVES as UNKNOWN; the host dump has one keyboard with `"main": true` (`hl-virtual-keyboard-fcitx5`); the field is defined in no pin or corpus row; the entry does not mention it.
- Chain C1 ("it **clamps** rate and delay (K04, K05)", and U3's "stored clamped value") — BROKEN wording. `std::max(0, x)` floors only (InputManager.cpp:1282-1283); the entry's own Limits says "sets no upper bound".
- Chain C3 — chain sentence survives; row E03's proposition "declared numlock default is -1" overclaims (member initializer; config default is false, K15).
- Chain C5 — omission: step 5 presents K10…K12 as the seat push and omits the bind-time send in the `CWLKeyboardResource` constructor (Seat.cpp:349-350), the path a client binding at v4+ would trigger.
- Chain C6 (1.26.0 rate-zero and negative rules, E04/E05/K17) — SURVIVES.
- Limits L1 ("pinned tag commit efb5099…") — SURVIVES, now verified outside the rows: `hyprctl version` reports `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993… clean`; upstream tag and commit fetch equal the pins.
- Limits L2-L8 — SURVIVES (QUALITY 104 "only" checks in K09 and K10 are entailed; registry anchor gaps in L9 verified against corpus/SOURCES.md rows 64, 265, 267 and the wl_keyboard interface 2573-2752).
- Limits L10 ("The counter checks only the S-id URL suffix and status") — BROKEN (understated): the counter also requires 11 pipe cells, uniqueness, `mined` status and the frozen commit in Hyprland-pin URLs. The conclusion that line-range anchors go unchecked still holds.
- How-to-verify H1 (`sha256sum fetch/*`) — runs; prints 11 lines; 10 match `c1.pin_sha256`; the match is manual and `SHA256SUMS.txt` is unlisted — SURVIVES with caveat.
- How-to-verify H2 (`freeze-verify.py`) — runs and ends OK, but it verifies the SUPERSEDED v1 table (`frozen-tables.json`, sha bf46c889…). The Source-rows text "Cells are generated from frozen-tables.json" is false for K16 (cell = v2 quote). The counter (the only check binding markdown cells to tables; TARGET_MET) and `freeze-verify-v2.py` (OK) are not in the verification path — BROKEN (stale table named).
- How-to-verify H3, H5, H6, H7, H8 — SURVIVES (each runs and prints the lines the text describes; H8 matches H04-H06 exactly).
- How-to-verify H4 (`sed -n '120,122p' IKeyboard.cpp`) — runs, but does not print 123-131, so the "no else" claim cannot be reproduced from the entry's commands — verification gap.
- Extra-rows provenance ("checked by the generator and by verify.py") — the substrings are true (13/13 by me); the generator (`integrate/build-entry.py`) does not check E quotes; the referent `w1/R55ScribeEntryA/verify.py` is a wave-1 draft not run by How-to-verify.

## Evidence pointers
- Prose attack table: `.ufo/waves/round-55/w2/R55W2CritEntryProse/prose-attack.md` §1 (settles), §2 (UNKNOWN), §3 (Chain), §4 (Limits), §5 (How to verify), §7 (receipts).
- Entry at scored rev: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 57584ed67716340b3d466fa04333ac0bab3fb79e:corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md`.
- Pins: `.ufo/waves/round-55/fetch/` (sha256 `SHA256SUMS.txt` and `c1.pin_sha256`, 10/10 equal).
- Counter run: `c1-counter-run.txt` (`MADO_KBD_ENTRY: rev=57584ed6… rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none`).

## Not verified
- Meaning of `"main"` in `hyprctl devices -j` (no source re-read of HyprCtl.cpp).
- Whether any live client binds wl_keyboard at v4+; whether the host keymap carries NumLock.
- The lane's "No keypress … observed" claim (U7) was not checked against run logs.
- Whether the hyprlang parser accepts negative integers for these keys (U3).

## Recommended corrections (for the L1; the seat did not edit the entry)
1. Chain step 3 and U3: replace "clamps"/"clamped" with "floors at zero (std::max(0, x)); no upper bound".
2. Limits L10: replace "only the S-id URL suffix and status" with the counter's actual checks, or drop "only".
3. How to verify: add `python3 -I .ufo/waves/round-55/freeze-verify-v2.py` and the counter run line; fix "generated from frozen-tables.json" to `frozen-tables-v2.json` (K16 is the only cell that differs).
4. How to verify: print 122-131 of IKeyboard.cpp (`sed -n '120,131p'`) if the "no else" claim stays.
5. S9: add rows (or a quoted line) for Seat.cpp:442 (full guard) and :444 (`m_lastRate`); S1: add a row for legacy 1132 (`getDeviceInt` forwards the fallback); C2: add a row for InputManager.cpp:1135 (the `setupKeyboard` header); C5: name Seat.cpp:349-350 as the bind-time send in Chain step 5; S6/S8: quote the Seat.cpp:605 `return;` and IKeyboard.cpp:131 if the "no else" and "gate" claims stay.
6. UNKNOWN U1: say the meaning is held as a measurement in `hyprctl-getoption-native-forms-r40.md` (S279), not defined by a pinned source row.
7. E03 proposition: change "declared numlock default is -1" to "the member initializer is -1; the config default is false (K15)".
8. Mention `hyprctl devices -j` `"main": true` on `hl-virtual-keyboard-fcitx5` as an unpinned observation under U4.
