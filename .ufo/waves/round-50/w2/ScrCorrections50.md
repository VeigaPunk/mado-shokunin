# ScrCorrections50 — D8 erratum re-derivation + round-49 w1 mid-write seats (mado round 50, w2 FALSIFY)

Seat: `.ufo/waves/round-50/w2/ScrCorrections50/` (leaf; no subagent, no background job, no tool installed, no counter/
gate/judge/control run). Attack revision `b4a79843cc2545bbe800db9322e58f6e00436629` (lane HEAD; data `906178b6`, freeze
`470bfd77`). Target: the w1/ScrCorrectionsR50 mid-write snapshot caveat (D2's ExecControlsC1 row, plus the second tracked
dirty file `ExecCounterC1.md`) and the D8 erratum that landed in `corpus/lessons/round-49.md`.

Method: committed bytes were read with `git -C <lane> show REV:<path>` (read-only git on the lane; no clone was needed
because no counter was run); the one path-shaped erratum command was additionally run literally against the lane
worktree, whose two inputs are clean at HEAD. Every command ran with HOME/XDG_*/TMPDIR under
`/fast/scratch/hyaku/mado-r50/ScrCorrections50`; nothing outside this seat dir was written; scratch removed at exit.

## Verdicts

| item | verdict |
|---|---|
| (a) D8 erratum block + counting command in `corpus/lessons/round-49.md` | **LANDED, counts re-derive (`2`, `5`); one attribution caveat** (F1) |
| (b) `corpus/lessons/round-50.md` Gate bullet counts | **LANDED** — admits `12`, rejects `5`; agree with the section's own prose |
| (c) `ExecControlsC1` (round-49 w1) clean at `b4a79843` vs w1 snapshot | **LANDED, no divergence** — committed report is the 173-line `complete` worktree version, receipts committed, sha256 stable |
| (c) `ExecCounterC1` (round-49 w1) clean at `b4a79843` vs w1 snapshot | **CLEAN at rev; committed report diverges from the w1 snapshot by one 5-line note added at landing** (F2); all four hash-pinned deliverables unchanged |

## (a) D8 erratum — landed, command re-derives

At `b4a79843`, `corpus/lessons/round-49.md:65-69` (in `## Round-48 closure items`, heading at `:49`; the corrected
sentence it names is at `:26-27`):

```
- Erratum (2026-10-27, round 50, D8): the "Spot-check shape" sentence above says "2 drafted admits and 4 rejects"; the corrected
  sentence is "the non-author closure sampled 2 drafted-admit examples and 5 rejected decisions represented above (counts computed
  from this section; the full source gate has 12 admits and 5 rejects; round-48 N3)". Counting command:
  `L=…/mado-shokunin; grep -cE '^- \*\*S[0-9]+ \(drafted admit\)' $L/corpus/lessons/round-49.md; grep -cE '^- \*\*REJECT' $L/.ufo/waves/round-49/w1/ScrRows/gate.md`
  → `2` and `5` (seat CritGateLesson, w1, `.ufo/waves/round-50/w1/CritGateLesson.md`).
```

- **Append-only, and byte-equal at data and attack revs.** `git show 906178b6 --numstat -- corpus/lessons/round-49.md` →
  `5 0`; `git diff --stat 906178b6 b4a79843 -- corpus/lessons/round-49.md corpus/lessons/round-50.md` → empty.
- **Proposed sentence appears verbatim.** Normalized compare of the landed erratum sentence against
  `.ufo/waves/round-50/w1/CritGateLesson.md:9` (`Spot-check shape: the non-author closure sampled …`): `identical_core_sentence:
  True`.
- **Counting command re-derives.** Run literally (`$L` = the lane; both inputs clean at HEAD, and again against the rev
  bytes): pattern 1 → `2`; pattern 2 → `5`. Matches the erratum's `→ 2 and 5`.
- **The sentence's internal claim re-derives.** "the full source gate has 12 admits and 5 rejects":
  `git show b4a79843:.ufo/waves/round-49/w1/ScrRows/gate.md | grep -cE '^- \*\*S3[0-9][0-9] admit\*\*'` → `12`; the same
  file `grep -cE '^- \*\*REJECT'` → `5`.
- **The sentence it corrects exists as quoted.** `:26-27` reads `Spot-check shape: the non-author closure samples from the 2
  drafted admits and 4 rejects above (counts computed from this section, round-48 N3).`

**F1 (attribution caveat, not a number failure).** The corrected sentence says *"5 rejected decisions … (counts computed
from this section…)"*, but the taught measurement for that 5 is `gate.md`, not the lesson section: in the lesson's Gate
section `grep -cE '^- \*\*REJECT'` → `0` and `grep -c '^- '` over `### Rejected after opening` → `3` bullets (which name
5 sources: `grep -oE 'https://[^`]+|ArchWiki|IKeyboard\.cpp|ConfigValues\.cpp' | wc -l` → `5`). So the `5` re-derives as
source count (and as gate.md line count) but not as a bullet count of "this section"; a reader who counts bullets gets 3.
The erratum's own command is what makes the 5 reproducible, and it is reproducible.

## (b) round-50 lesson Gate counts — landed

`git show b4a79843:corpus/lessons/round-50.md`:

```
$ grep -cE '^- \*\*S[0-9]{3} admit\*\*'   → 12      # lines 21-32, S352..S363
$ grep -cE '^- \*\*REJECT'                → 5       # lines 37-41
```

The located lines are S352-S363 in row order (tier A; 9 code, 2 docs, 1 own-work) and the five rejects are wiki 0.56.0,
wiki latest, ArchWiki, `IKeyboard.cpp` duplicate, `ConfigValues.cpp` duplicate. The same section's prose says
`quotes re-verified …` (`:18`) and `Rejected after opening (5; …` (`:34`), so prose and bullets agree at `12`/`5`. The
worktree copy carries an unrelated +8-line sibling append (M50-5, `git diff --stat b4a79843 -- corpus/lessons/round-50.md`
→ `8 ++++++++`); both patterns still count `12`/`5` there, and the rev bytes are what I scored.

## (c) round-49 w1 `ExecControlsC1` / `ExecCounterC1` at `b4a79843`

**w1 record of dirtiness** (read-only): `w1/ExecWaveDone/receipts/deliverables.txt:27` and `w1/ScrQualityR50.md:77-80`
(03:03) and `w1/ScrRowsR50.md:118-121` all list ` M .ufo/waves/round-49/w1/ExecCounterC1.md` plus the three
`ExecControlsC1` entries; `w1/ScrCorrectionsR50/receipts/d2-postreport.txt:23-47` records the ExecControlsC1 mid-write
snapshot: committed stub at `dd2e827e`, worktree `worktree_line3: status: complete 2026-10-27T02:57-03:00…`,
`worktree_lines=173`, `?? …/receipts/`.

**Now clean:** `git status --porcelain -- …/ExecControlsC1* …/ExecCounterC1*` → no lines; `git diff --stat b4a79843 --
<same paths>` → empty. Both landed in `1b37a59e` (author 03:26:12, committer 04:44:32), i.e. after the w1 snapshot
(03:00:02).

**ExecControlsC1 — landed, matches the snapshot.** Committed `:3` is character-identical to the recorded `worktree_line3`;
committed and worktree are both 173 lines with sha256 `c1fae2ad…3d8e`; the landing diff is `173 +++` (170+/3-) against the
stub, and the three formerly untracked receipts (`clause-lines.txt` 193, `controls.txt` 113, `quotes.txt` 5 lines) are
committed. Its report still makes the substantive claim the receipt supports (`0 of 20 score TARGET_MET`, report `:4`,
`:55`; `receipts/controls.txt` tail carries the c07 isolation pair).

**ExecCounterC1 — clean, deliverable bytes unchanged, report prose gained a note (F2).** The w1 records captured only the
` M` state, not content, so byte-identity with the w1 worktree copy is not provable. What is provable: the landing commit
`1b37a59e` touches only this one file with `5 insertions / 1 deletion`, appending a "Control-margin note from
ScExecControlsC1 (20 controls, 0 `TARGET_MET` at counter sha `1a7fcc21…`)…" inside item 2 of the freeze-edit list
(`ExecCounterC1.md:235-239`); that string exists nowhere else in the lane (`grep -rn 'Control-margin note' .ufo` → only the
file). All four hash-pinned deliverables in the report's own table re-hash byte-equal to the blobs at `b4a79843`:
`c1-r49-keysym.py` `1a7fcc21…b4fe` (732 lines), `c1-r49-fixtures.json` `81836bfb…e393`, `counter-selftest.py`
`5e4c2472…4c80`, `scratch-refB-tool.py` `81cd3b19…2fff`; the report is 272 lines with `:3` still
`Status: **complete** …`. So: the seat's *deliverables* are landed and stable; the *report* is not the exact
w1 snapshot — it is that snapshot plus an integration note attributed to `ScExecControlsC1`.

## Findings for the L1

1. **F1** — D8 erratum: numbers land (`2`, `5`, `12`), but the "(counts computed from this section)" attribution fits the
   admit half only; the reject 5 is a source count / a gate.md line count, not the section's bullet count (3). No fix
   demanded by the D8 predicate; recorded so a later closure does not cite "3 bullets" as the erratum's own count.
2. **F2** — `ExecCounterC1.md` landed as w1-snapshot + 5-line control-margin note at `1b37a59e`. The note is accurate
   against the counter's sha and the 0-of-20 controls, but it is text no w1 record saw before landing; if the L1 wants the
   snapshot preserved exactly, the note needs its own landed line rather than an in-place edit of a closed round's report.
3. **F3** — the w1 dirtiness records are state-only (no content hashes), so "no divergence" for a report file can only be
   proven where a snapshot descriptor exists (ExecControlsC1: line 3 + 173 lines + receipts). For `ExecCounterC1.md` the
   proof stops at the hash-pinned deliverables.
4. **F4** (context, not mine) — the lane worktree carries a sibling w2 append to `corpus/lessons/round-50.md` (`+8` lines,
   M50-5) at attack time; committed bytes at `b4a79843` are the ones scored here and are unchanged from `906178b6`.

## Limits / not run

- No counter (`PRED-C1-r50`, `PRED-C2-r50`), no gate, no judge, no control, no build/lint/test: this item is a
  re-derivation of textual counts and of tracked-file state. No clone was made — the counts read committed bytes via
  `git show`, and the erratum's own command needs the worktree paths it names.
- Host/compositor untouched (no `hyprctl`, no xkbcli, no pacman, no home write); no tool installed.
- `/tmp` used for nothing; the only scratch is `/fast/scratch/hyaku/mado-r50/ScrCorrections50` (removed at exit); no
  scratch path is cited as evidence.
- Round-50 lesson bytes were read at the rev only; the worktree divergence (F4) is another seat's.

## Deliverables (all `test -f`-checked at close)

| path | what |
|---|---|
| `.ufo/waves/round-50/w2/ScrCorrections50.md` | this report |
| `.ufo/waves/round-50/w2/ScrCorrections50/receipts/a-d8-erratum.txt` | erratum block at rev, sentence/command presence, both counts (worktree + rev), gate 12/5, section bullet/source counts |
| `.ufo/waves/round-50/w2/ScrCorrections50/receipts/b-lesson-r50-gate-counts.txt` | round-50 Gate `12`/`5` with located lines, prose lines, worktree delta |
| `.ufo/waves/round-50/w2/ScrCorrections50/receipts/c-r49-seats-clean.txt` | w1 dirtiness records, `status`/`diff` clean at rev, ExecControlsC1 snapshot-vs-committed, ExecCounterC1 landing diff + re-hashed deliverables |
| `.ufo/waves/round-50/w2/ScrCorrections50/receipts/d-d8-sentence-identity.txt` | append-only numstat, data/attack rev equality, normalized proposal-vs-landed sentence identity, literal command run |
