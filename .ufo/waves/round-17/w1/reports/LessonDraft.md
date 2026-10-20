# LessonDraft report — round 17 (scoped)

## Behavior
Drafted `## Mistakes` rows M1 and M2 for the round-17 lesson in the round-16 table shape. Draft only, at `.ufo/waves/round-17/drafts/LessonDraft.md`. Nothing else written.

## Touched surfaces
- Written: `.ufo/waves/round-17/drafts/LessonDraft.md` (draft), this report.
- Read only: `corpus/lessons/round-16.md`, `corpus/lessons/round-16-verifier-spotcheck.md`, `considerthese/2026-10-20.md`, `.ufo/waves/round-16/evidence/frozen-tampered.json`, `corpus/QUALITY.md` lines 1-34, 43-106, `.ufo/waves/round-16/evidence/` and `.ufo/waves/round-17/` directory listings, grep hits for `snapshot_tampered|frozen-tampered|frozen_error` across the lane, `.ufo/waves/round-13/` frozen and reports.

## Gates and checks
- No tests, builds, linters or gate runs. No `pacman`, `sudo`, `systemctl`, `hyprctl`, live probe, or session transcript read. No tools installed or updated.
- Verification beyond reads: none.

## Findings
- **M1 (evidence labeling).** round-16.md line 131 attributes `snapshot_tampered` to `evidence/frozen-tampered.json`. That receipt records exit 2 `frozen_error`, measured at 9dcf248. It is not evidence of `snapshot_tampered`. The only support is the final selftest at 1e31681. No QUALITY criterion covers citation-to-revision and finding matching. Proposed criterion 23 and a `label-check.py` falsification (red on the current line 131 pair) are in the draft.
- **M2 (scope breach, prompt-only fences).** Round-15 `sudo pacman -S` (R15-V1), round-16 `pacman -Q waybar`, round-16 fleet misroot, round-15 `/proc` and `pgrep` reads. Captured by QUALITY21 text only. Proposed fix: `tools/mado-tripwire.py` as post-hoc detection, with the round-15 anchor (`MadoR15.LibinputEvents.jsonl` line 54, `call_38165`) as selftest red.
- Facts needing L1 verification are listed in the draft under `[L1-VERIFY]`.

## Out of scope / not done
- `label-check.py` and `tools/mado-tripwire.py` were not written (not in this seat's file list).
- No new source rows; no `SOURCES.md`, `QUALITY.md`, `SCORECARD.md`, `LOG.md` or lesson edits.
- No transcript was opened; the red anchor is unverified by this seat.

## Artifact paths
- Draft: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/drafts/LessonDraft.md`
- Report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/w1/reports/LessonDraft.md`

## Checks for L1 to run once after integration
- Verify `round-16.md` line 131 and `frozen-tampered.json` fields.
- Confirm `action-selftest-final.json` (1e31681) carries `frozen-tampered-plan` want 2 got 2.
- Decide whether to re-receipt the tamper control or append a correction.
- Once written: run `label-check.py` on line 131 (expect red) and `mado-tripwire.py --selftest` on the round-15 anchor (expect `host_mutation` / `sudo`).
