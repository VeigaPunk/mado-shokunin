# ScrMistakes — w1 / round 40 — `## Mistakes` draft + criterion 65 candidate

Status: DONE. No claim verdict is asserted here; the deliverable is a draft for the L1 to land.
Nothing outside this seat's directory was written; no mutating git/jj command and no compositor
verb was run by this seat.

Report file: `.ufo/waves/round-40/w1/ScrMistakes.md` (this file).

## Files written

| path | sha256 | what |
|---|---|---|
| `.ufo/waves/round-40/w1/ScrMistakes/mistakes.md` | `0fdedff51c3ae04b7bb2ac5f8e25e9e82a098ef68c0eafb04f404d3408a6bfa9` | 221 lines: 4 mistake rows (M40-1…M40-4) + candidate QUALITY criterion 65 + evidence appendix + limits |
| `.ufo/waves/round-40/w1/ScrMistakes.md` | (this report) | seat status |

## Deliverable shape

- **M40-1** — the C1 generator drew each value type from a broad table; `M03-bool-exact` and
  `M05-gap-three-values-wrong` survive without the per-tree quirk guarantee. Fix: the frozen
  `plan = [(k, True, "agree") for k in kinds]` (`quality/counters/c1-r40-live.py:342`) + one mutant
  per spelling class. Shown able to fail: both mutants `fixtures=0/13` frozen vs `13/13` on a copy
  with the guarantee removed.
- **M40-2** — the first reference model mis-expanded a 3-value CSS gap; only some trees carry the
  class (4/8 reconstructed), so a wrong model fails a subset. Fix: source-grounded CSS 1/2/3/4
  expansion (`:188-196`) + a 3-value gap in every tree; `M05` `0/13`.
- **M40-3** — a naive compare read the compositor's conversion as 14 host divergences. Reproduced
  exactly: base tool over normalised native replies → `mismatch=14 agreement=50 agreement*=6` vs the
  native model's `62/8/0`. Fix: native-form conversion + angle inheritance; `M15` `0/13` and the
  no-inheritance variant flips exactly 2 keys (`62/8/0 → 62/6/2`).
- **M40-4** — round-39's `M39-2` fix (distractors in the trees) did not generalise to a per-type
  guarantee, and the receipt cannot show its own per-tree coverage. Fix: a per-tree spelling census
  in the freeze receipt; shown able to fail (`8/8` frozen vs `0/8`, `0/8`, `2/8` on the
  guarantee-free copy).
- **Criterion 65 candidate** — "every generated tree carries one quirk spelling of every value type;
  the controls list one mutant per spelling class, each `0/N` frozen and `N/N` once the guarantee is
  removed; the freeze receipt carries the per-tree spelling census." Criterion 64 is the current
  last row in `corpus/QUALITY.md`, so 65 is free.

## What was run (exact, this seat)

All in `/tmp` scratch (`mktemp -d`), lane read-only at `rev e2b51d3b3f79768282914d57c1fa32cc85dcb06a`,
scratch removed after the runs; no `GIT_*` env passed to the counter; no git write anywhere.

1. `git rev-parse master` → `e2b51d3b3f79768282914d57c1fa32cc85dcb06a`.
2. Two guarantee-free copies of the frozen counter (`V1`: plan `quirk=False` only; `V2`: plan + bool
   table + gap arity) scored against the reference tool's M03/M05 mutants via the counter's
   `--tool` switch (the switch `ctl/run-c1-controls.py:63-69` uses):
   `M03 frozen 0/13`, `M03 V1 13/13`, `M03 V2 13/13`, `M05 frozen 0/13`, `M05 V1 6/13`,
   `M05 V2 13/13`. Every line prints `exit=1`; on the V1/V2 lines that exit is clause b (reference
   selftest 71 < 79), not the fixture line.
3. Per-tree spelling census rebuilt from the counter's own seed rule (`:522-523`):
   `frozen garbage-bool=8/8 3-value-gap=8/8 ultraheavy=8/8`; `V2 0/8 0/8 2/8`; `V1 0/8 4/8 1/8`.
4. Naive run: normalised the 70 committed native replies
   (`.ufo/waves/round-40/c1/native-capture.jsonl`) to `{value, custom_type, set}` and ran
   `git show 9fc511d:tools/mado-options.py --home /home/vgpnk --getoption <normalised>` → exit 0,
   `mismatch=14 agreement=50 agreement*=6`; exact-text compare over the same bytes → 39 mismatches
   (`int 24, float 2, custom 13`).
5. The eight quirk gaps at this rev: `9 19 18`, `39 36 4`, `1 26 3`, `28 36 30`, `2 26 7`,
   `6 36 19`, `20 17 5`, `16 14 5` — none has `n[0] == n[1]`, so `M05`'s kill is not a
   value-collision accident at `e2b51d3b`.

## Findings and conflicts (verbatim for the canonical judge)

- **`14 of 70` reproduces exactly** under the base tool's comparison rule (`9fc511d` tool = `master`
  tool, `git diff --stat` empty). It is not host drift: the native model reads `mismatch=0`
  (`w1/ExecLiveCensus.md`). My witness is scratch, not committed.
- **The first draft's before-state is uncommitted** (as the task states): `receipts/ctl-c1.txt`
  holds 18 `control=` lines in final state only. My V1/V2 are reconstructions of "guarantee absent",
  not the draft's bytes; `M03` survives outright under both, `M05` survives under V2 and is caught
  only partially under V1 (`6/13`). The `2 of 8` first-model figure is reported as stated by the
  L1, not measured here.
- **Seeds are revision-dependent**: the census, the collision statement and the fixture counts are
  true at `e2b51d3b` and must be re-run (and committed) at the data rev.
- A blunter exact-text rule gives 39 mismatches, not 14 — the 14 is specific to the base tool's
  documented rule (`tools/mado-options.py:53-60`), which is why it reproduces.

## Out of scope / not done

No edit to `corpus/QUALITY.md`, `corpus/lessons/round-40.md`, `registration.md`, the counters, the
controls or any tracked file; no commit; the full `ctl/run-c1-controls.py` harness was not re-run
(the committed `receipts/ctl-c1.txt` is quoted); no compositor verb (`hyprctl getoption`/`version`/
`descriptions`) was run by this seat; no package transaction. Scratch `/tmp/mado-scr-mistakes.*`
removed.
