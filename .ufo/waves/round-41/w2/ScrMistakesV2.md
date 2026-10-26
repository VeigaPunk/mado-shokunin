# ScrMistakesV2 (w2, round 41) — seat report

Status: DONE (draft of the `## Mistakes` additions for what wave 1 found).

Deliverable: `.ufo/waves/round-41/w2/ScrMistakesV2/mistakes.md` — M41-9..17 rows, in the
existing M41 row shape (class | evidence pointer | captured-by | fix | shown able to fail),
with every evidence pointer verified by `.ufo/waves/round-41/w2/ScrMistakesV2/verify-pointers.py`
(output: `verify-pointers.out`; all checks PASS).

Sources read: the ten named w1 reports (`w1/CritC1Cheat.md`, `w1/RevC1Counter.md`,
`w1/ExecC1ExtraMutants.md`, `w1/ExecC2ExtraMutants.md`, `w1/CritC2Cheat.md`, `w1/RevC2Counter.md`,
`w1/ExecDiffFuzz.md`, `w1/ExecJournalFormat.md`, `w1/RevRefTool.md`, `w1/MutC1CounterGates.md`),
`git show 07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/lessons/round-41.md` (M41-1..8),
`registration-v2.md`, `w1-results.json`, `make-w2-spec.py`, `receipts/ctl-c1-v2.txt`,
`receipts/ctl-c2-v2.txt`, `ctl/run-c1-v2-controls.py` (K01-K10 names), `ctl/run-c2-v2-controls.py`
(F1-F6 names). No lane file was written outside this seat dir and this report; no git/jj mutation;
no pacman; no host-service/compositor/journal contact (all reads are file reads or read-only git show).

Rows drafted:
- M41-9: v1 predicates falsified by w1 (8/12 cheats MET; C2 9/9; extra mutants 13/42, 29/45) — re-registration order.
- M41-10: unreadable-stub design (CH1 oracle / CH2 on-disk journal copy).
- M41-11: b2 teeth vacuous (CH6/CH9/CH10 — path, fingerprint, rename).
- M41-12: silent NO_SESSIONS on five of six `-o` formats.
- M41-13: FIFO hang + unbounded live buffering (RevRefTool M1/M2).
- M41-14: C2 forgeries (F1-F7, H1-H4, 29/45 survivors).
- M41-15: C1 control suite nonce lottery (MutC1CounterGates).
- M41-16: kernel restart dropped w1-results.json seat outputs (reports on disk).
- M41-17: M41-5 shape-line wording resolved by registration-v2.

Tooling: none installed (host python3 3.14 stdlib only). Limits: the draft is the L1's to
integrate; fixtures-only fixes have no control name and are marked "none" in the shown-able-to-fail
column, matching the M41-2/M41-3 convention.

Report trailer: `.ufo/waves/round-41/w2/ScrMistakesV2.md`
