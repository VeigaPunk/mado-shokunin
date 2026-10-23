# ConnOracleGaps — cross-axis pattern scan (read-only)

Lane: mado-shokunin. Base tip 1ed41fa8. No lane files edited except this report.

## Evidence scanned

- mado lessons: `corpus/lessons/round-*.md`, `*-verifier-spotcheck.md` (rounds 1–24).
- mado SCORECARD: `SCORECARD.md` (1627 L, capability rows and claim sections).
- sibling lanes: `*-shokunin/corpus/lessons/` (grep for oracle/running-program patterns).

## mado claims whose instrument compared a lane artifact against its own model/transcription

| # | Pointer | Claim / instrument | Closure that caught it | External oracle existed? |
|---|---|---|---|---|
| 1 | `corpus/lessons/round-12.md:19` (M7) | Counts in lane artifacts transcribed from prior summaries instead of re-derived commands | M7 itself (round-12) | Yes — the named `wc`/`grep` commands |
| 2 | `corpus/lessons/round-17.md:16` (M1) and `round-18.md:21` (M6) | Rubric V credits a SOURCES row whose bytes were never fetched (row text vs. fetch bytes) | round-17 verifier spotcheck R17-V3; round-18 M6 | Yes — fetched source bytes / `fetch-verify.py` |
| 3 | `corpus/lessons/round-19.md:20` (M7), `round-19-verifier-spotcheck.md:61-65` | `fresh-pins` credits any permitted row token, not the S096 row the claim names | wave-2 critics (CriticC2W2) + round-19 verifier | Yes — pinned source rows |
| 4 | `corpus/lessons/round-20.md:22` (M9) | Tripwire recall credits any finding of any class on six incident lines (draft-written lines) | wave-2 AdvRecallShapes + round-20 verifier | Yes — round-18 known-miss notes |
| 5 | `corpus/lessons/round-24.md:16` (M24-2) and `round-24-verifier-spotcheck.md:60-67` | C1 rule-attribution counter: a generic/single-page rule note meets `PASS_ROW≥6` because expected rows are the counter's own criteria, not attribution content | hyaku closure §2.1 (CloseC1PostDataCtl) | Yes — pinned Hyprland/wiki bytes |
| 6 | `corpus/lessons/round-24.md:88` (M24-5) and `round-24-verifier-spotcheck.md:98-115` | C2 capability table: `0/12` reached by transcribing the counter's observed column into the stated column | hyaku closure §2.2 (CloseC2Audit) | Partial — demonstration commands (some run lane scripts) |
| 7 | `registration.md` (attempt 3, C1 v4 section) + `c1/count-v3.py` | C1 v1–v3 expected bind tables taken from the counter's own line model (`line_entry`/`unbind_apply`); a faithful transcription of that model scores `TARGET_MET` without Hyprland | v4 design (Hyprland oracle) — the v4 counter removes this | Yes — Hyprland v0.56.2 nested instance (`hyprctl binds -j`) |

## Sibling lanes that used a running program as an oracle in a counter

| Lane | Pointer | One line |
|---|---|---|
| kaidoku-shokunin | `corpus/lessons/round-31.md:39` | "a row for node:sqlite / libsqlite3 builds (host readers used as oracle and probe, not learning sources)" |
| tsukuroi-shokunin | `corpus/lessons/round-30.md:72` | "CriticCounterV2 installed cmarkgfm 2025.10.22 from PyPI with uv pip into a private venv under its scratch directory (renderer oracle)" |
| mori-shokunin | `corpus/lessons/2026-10-15-forgeable-oracle-visible-fixtures.md:1` | "a fixture oracle can be forged when the system under test can see which case is running" |

## Proposed move

Treat "expected value derived from the lane's own model/transcription" as a named counter-design defect class for this round's mined mistake. For any future counter, require the expected column to come from an independent oracle (a running program or pinned source bytes) and add a pre-data control that transcribes the model to show it fails.

## Risks

- Some entries (#1, #4) are adjacent to but not exactly self-model expectations; they are included because their instrument accepted lane-authored values without an independent check.
- Sibling scan was grep-based over lesson files only; lanes may use running programs in counters without the word "oracle".

## Verification

Read-only scan; no commands executed beyond grep/read. Pointers verified by direct file reads.

Verdict line: `CONNECTOR self-model instruments: 7 in mado, 3 sibling oracle patterns`