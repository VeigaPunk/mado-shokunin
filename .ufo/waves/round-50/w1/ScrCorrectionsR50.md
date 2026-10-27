# ScrCorrectionsR50 — routed D2, D3, D8 (mado round 50, w1)

Seat: `.ufo/waves/round-50/w1/ScrCorrectionsR50/` (leaf; no subagent, no background job, no tool installed).
Job: write the three append-only correction lines with their commands — D2 (final state of the 7 unsettled round-49 w1
seats), D3 (the unreceipted 57,865-pair figure), D8 (the lesson's gate-count drift). No counter, judge, control or gate
was run; every read was read-only git or worktree, and no tracked file in the lane or the fleet was touched.

## Deliverables

| path | what |
|---|---|
| `.ufo/waves/round-50/w1/ScrCorrectionsR50/corrections.md` | the three correction lines (each ready to append to the round-50 lesson) + their commands and measured outputs + limits |
| `.ufo/waves/round-50/w1/ScrCorrectionsR50/receipts/d2-seat-state.txt` | per-seat `git log`, canonical/in-dir report size, dir file counts |
| `.ufo/waves/round-50/w1/ScrCorrectionsR50/receipts/d2-postreport.txt` | round-49 report commit, post-report commits, `git status --porcelain`, worktree mtimes, committed-vs-worktree line 3, second snapshot |
| `.ufo/waves/round-50/w1/ScrCorrectionsR50/receipts/d3-figure.txt` | the receipt search for 57,865 (all commands + raw output), the committed 24,898 table, the arithmetic |
| `.ufo/waves/round-50/w1/ScrCorrectionsR50/receipts/d8-counts.txt` | 12 admits / 5 rejects in `gate.md`, 2 located admits / 5 rejected sources in the lesson, with commands |
| `.ufo/waves/round-50/w1/ScrCorrectionsR50/receipts/quote-sources.txt` | every quote's locator, computed by `grep -nF` |
| `.ufo/waves/round-50/w1/ScrCorrectionsR50/receipts/quote-check.txt` | output of `check-quotes.py` → `QUOTE_CHECK checked=10 failed=0` |
| `.ufo/waves/round-50/w1/ScrCorrectionsR50/check-quotes.py` | verifier: ≤25 words, quote present at its line, present in a receipt and in `corrections.md` |

## Verdicts

- **D2 — named, and the "no pending bytes" answer is no.** 5 of 7 landed (ExecSessionTriage and SentPrivacy at in-dir
  paths, ScoutHyprBinds / CritPremiseC2 / CritRoutedItems at their canonical paths, all `dd2e827e`); CritPremiseC1 is
  dead (interim stub only, seat dir empty, no commit ever touched it); ExecControlsC1 is partial — the committed state is
  the interim stub (`status: running 2026-10-27T01:56-03:00`, `dd2e827e:…/ExecControlsC1.md:3`) while its finished
  173-line report and three receipts sit uncommitted in the worktree (mtimes 02:55–02:57). One post-report commit exists,
  `8ae47b95` 02:45:06 (`check-quotes.py`), after the report commit `b0184c43` 02:36:01. The L1 must commit or drop
  ExecControlsC1's worktree report.
- **D3 — correction, not receipt.** `git grep -nP '(?<![0-9a-f])57865(?![0-9a-f])'` → no hit; no `.txt/.json/.jsonl/.py`
  carries "57,865"; only prose cites (`registration.md:22`, report `:16`, spotcheck). Committed figure:
  "24898 comparisons, 0 mismatched" (`w1/ExecRefKeysymB.md:51`), whose committed table
  (`w1/ExecRefKeysymB/receipts/diff.txt:25-34`) sums to 24898 over 125 named keymaps; the 57,865/400-keymap sentence is
  withdrawn.
- **D8 — both numbers corrected.** `w1/ScrRows/gate.md` §1 holds 12 admits (lines 8-19) and §2 holds 5 rejects
  (lines 23-27); the lesson's Gate section shows 2 located admits (lines 14, 16) and 5 rejected sources in 3 bullets
  (lines 20-22). "2 drafted admits and 4 rejects" (`corpus/lessons/round-49.md:26`) → 2 located examples of 12 admits,
  and 5 rejects.

## Limits

- The ExecControlsC1 row is a snapshot of a seat that was mid-write; re-checked at 03:00:02 unchanged. If the L1 commits
  it later, the state upgrades to landed at that hash — the three commands in the correction line reproduce the check.
- Not re-run, deliberately: reference B's comparisons, the gates, any counter or control, any build/lint/test.
- No scratch needed: a single `mkdir -p /fast/scratch/hyaku/mado-r50/ScrCorrectionsR50` was created and removed; no file
  was written there and no `/tmp` path is cited.
