# R55RevCoverage — round 55 wave w1, C1 coverage-truth

Deliverable: `.ufo/waves/round-55/w1/R55RevCoverage/coverage-truth.md` (full classification and duplication test).
Receipt: `.ufo/waves/round-55/w1/R55RevCoverage/receipts/base-grep.txt`.

## What I did

1. Ran the lane-specified `git -C …/mado-shokunin grep -n -i -E 'repeat_rate|repeat_delay|numlock_by_default|repeat_info|m_repeatRate' 3b55b6e91e40f455dd56b2985e4ffc087ada92d5 -- corpus/knowledge tools SKILL.md PROVINCE.md`. Output: 16 lines (exit 0).
2. Broad sweep at base for `numlock|num lock|repeat.?(rate|delay)|key ?repeat|keyboard repeat` over corpus, tools, SKILL.md, PROVINCE.md.
3. Zero-hit checks at base for `repeat_info`, `m_repeatRate`, `updateRepeatInfo`, `SeatManager`, `protocols/core/Seat`, `IKeyboard.hpp`, `applyConfigToKeyboard`, `getDeviceInt`, `wl_keyboard`, default repeat figures 25/600 in corpus/knowledge.
4. Confirmed the entry file is absent at base (`git cat-file -e` → exit 128). Max SOURCES id at base is S377.
5. Read the context of each hit (`git show <base>:<path>` line ranges) and the header legends (`hyprctl-verification-layer.md` §legend lines 46-48).
6. Cross-checked the registration S380 anchor (IKeyboard.hpp :121-123): round-55 fetch file sha256 `82e0bc9e…f05` equals the SHA256SUMS line, the S363 row sha, and the round-46 receipt; lines 121-123 are `m_repeatRate`, `m_repeatDelay`, `m_numlockOn`.

Host: no host command run. Tooling: none installed. Scratch `/fast/scratch/hyaku/mado-r55/R55RevCoverage/` used for one temp file and removed before yield. No tracked files modified, no git mutation, no subagent.

## Findings

**F1 — The source-level surface is uncovered at base (claim holds).** No corpus/knowledge note, SOURCES row, README row, tool or SKILL/PROVINCE line names the per-keyboard repeat/numlock chain (`repeat_info`, `m_repeatRate`, `SeatManager`, `Seat.cpp`, `IKeyboard.hpp` members, `applyConfigToKeyboard` repeat/numlock, `getDeviceInt`, defaults). The C1 source-chain rows are new corpus ground.

**F2 — The three option names are not absent; they are covered only at the global-readback layer.** The 16 lane-grep hits split into: 6 host-readback rows (config-health-report-r3.md:546-548, 829-831, `agreement`); 3 readback rows (hyprctl-verification-layer.md:132-134, `agreement`); 1 sourced disambiguation (r46:34: the dump's `numLock` is lock state, not the option); 1 UNK note (r46:70); 5 self-test passing mentions in tools/mado-options.py (1345, 1407, 1495, 1584, 1607). No hit is a source-level or per-keyboard claim.

**F3 — Expansion credit is partial, and the H01–H06 host rows add none.** The host values 40 / 250 / 1 are already `agreement` in config-health-report-r3 §2.4 and hyprctl-verification-layer §3.2. The H rows restate that ground under a new pin; they should be labelled restatement, not expansion. Credit applies to the K-row source chain and to closing the r46:70 UNK for these three names.

**F4 — Protocol-side repeat_info is not in corpus but is in wave evidence.** `repeat_info` appears in `.ufo/waves/round-15/w1/reports/WaylandKeyboard.md:125-126` and `ReviewKeyboard.md:16` (wayland.xml:2732-2751), never in corpus/knowledge. The entry's protocol rows are corpus-first, but the entry should cite round 15 as prior reading, not present it as first-seen. (Outside the lane's grep scope; reported as a whole-tree observation.)

**F5 — Integration risk: stale UNK and a misreadable "agreement".** After the entry lands, r46 line 70 and corpus/README.md:122 still say UNK for the three names. The host "agreement" rows mean global value equals declaration, not keyboard-level effective value. Neither is a false claim at base; both can mislead a reader once C1 lands. The L1 should add cross-links; I did not edit anything.

**F6 — Registration anchor S380 consistent with pinned bytes.** Round-55 fetch `Hyprland-IKeyboard.hpp` sha `82e0bc9e1f31f6342f193b0981000245b932719cf406988d98aba64f0f716f05` matches the SHA256SUMS line, S363's recorded sha, and the round-46 receipt; members are at :121-123 as registration §C1 states.

**F7 — Frozen-claim text check.** The claims-frozen.md "unmoved command" (`grep -lE 'repeat_info|m_repeatRate' corpus/knowledge/*.md` → 0 files) is correct at base. Whole-tree it is non-zero (wave reports and fetch files); the frozen command is scoped and remains true as written.

## Anomalies / ambiguities

- None that change the C1 verdict. The lane text "the surface is uncovered" is accurate only at the source-chain level; the option names are present at the readback and UNK levels. The coverage-truth file states this split.
- No input in the lane's inputs was found to contradict another. No hold-out path was seen or used.

## Not verified

- Counter, harness and controls for C1 were not run (not in this seat's assignment).
- `efb50993` provenance of the round-46 receipt was inferred from the matching sha with the S363 row, not re-fetched.
- SOURCES S052 row read only to its first ~260 characters; its repeat_info coverage is inferred from the absence of `repeat_info` in corpus.
- Broad-sweep patterns were limited to the terms named; a paraphrased mention (for example "keyboard delay" without "repeat") would not appear. Not searched.

## Verdict for the seat

C1 surface-uncovered claim: **confirmed** at the source-chain level; **partially refuted** for the three option names (global readback and UNK already present). Expansion credit: K-row source chain and r46:70 UNK closure; no credit for H01–H06 host restatement.

## Deliverables

- `.ufo/waves/round-55/w1/R55RevCoverage/coverage-truth.md`
- `.ufo/waves/round-55/w1/R55RevCoverage/receipts/base-grep.txt`
- `.ufo/waves/round-55/w1/R55RevCoverage.md` (this file)
