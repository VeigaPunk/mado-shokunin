# ReMeasureHarm — round-17 wave-2 harm watch re-run

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`, lane HEAD
`988b858bd6049bc709807534fd725c05264f7e60` (pushed).
Role: leaf reviewer (FALSIFY). No subagents. No writes outside this report.
Installs/updates this lane: **none**. No sudo/pacman/systemctl/hyprctl/live probe
was issued; `/var/log/pacman.log` and config trees were not touched by this lane.

## Verdict first

Both assigned harm-watch measurements **reproduce exactly, with no regression**.
I additionally established that the reproduction is not incidental: the round-16
instrument bytes, the SCORECARD counting command, and the entire `coverage`
subtree are **byte-identical** between baseline `27cd06f` and `988b858`. The only
movement is the declared append (2 notes, 15 source rows, 1 QUALITY criterion) and
the resulting denominator growth. No attack I ran found a counterexample.

- `coverage.count` = **7** (`U1..U7`) at `988b858` — unchanged, and *provably*
  unchanged: the full `coverage` JSON subtree is byte-identical to baseline.
- Navigation counter: **32/32 complete, exit 0** at `988b858`;
  **30/30 complete, exit 0** at `27cd06f`. Both executed from the SCORECARD
  fence bytes, not a transcription.

## 1. Harm watch — round-16 `measure.py` at lane HEAD

Command (as fenced in `SCORECARD.md` § Round 17 harm watch):

```
python3 .ufo/waves/round-16/measure.py 988b858bd6049bc709807534fd725c05264f7e60
```

Observed (`coverage` block, exact):

```
"items": ["U1","U2","U3","U4","U5","U6","U7"], "count": 7, "score": 10.0
```

`coverage.count 7` holds exactly as required, with U1–U7 the same seven items and
`score` still 10.0 (finite ceiling 7/7).

Whole-document fields at that revision (for the record, same run):

| field | value |
|---|---|
| `revision_sha` | `988b858bd6049bc709807534fd725c05264f7e60` |
| `navigation` | `notes 32, indexed 32, missing [], extra [], duplicates []` |
| `calibration` | `15/23` grounded, `fraction 0.6522`, `score 6.5217` |
| `source_registry` | `rows 70`; tiers `A63 B1 C6`; statuses `mined 55, queued 8, rejected 7` |
| `round15_required` / `round16_required` | S051/S052, S053/S054 all `present, mined, A` |
| `safety_artifacts` | 3 present, `executed:false` (declared design: presence/bytes only) |
| `measure_inputs.gate_executed` | `false` (declared design: structural observation, never executed) |

The `executed:false` / `gate_executed:false` flags are the instrument's own
declared semantics ("observed for presence and bytes only — never executed"), not
a regression: identical at `27cd06f`.

## 2. Fleet-round-1 navigation counter, fenced command, both revisions

I extracted the fence from `SCORECARD.md` at `988b858` between
`### Counting command` and the next `##` heading and ran the extracted bytes
(`/tmp/fenced-counter.sh`, 20 lines, sha256
`8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88`), with `REV`
set per run. Exact output:

```
=== VERBATIM FENCE, REV=988b858bd6049bc709807534fd725c05264f7e60 ===
revision=988b858bd6049bc709807534fd725c05264f7e60 indexed=32/32 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0
=== VERBATIM FENCE, REV=27cd06f ===
revision=27cd06f indexed=30/30 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0
```

This matches the ticket's expectation exactly: `32/32` at lane HEAD with the two
round-17 notes indexed, `30/30` at the round-17 baseline, both complete (exit 0).

Three-point trend (round-16 instrument's `navigation` block, independent of the
fence but same result):

| revision | notes | indexed | missing/extra/duplicates | exit |
|---|---|---|---|---|
| `0175f13` (round-17 pre-registration) | 30 | 30 | 0/0/0 | 0 |
| `27cd06f` (round-17 baseline) | 30 | 30 | 0/0/0 | 0 |
| `988b858` (lane HEAD) | 32 | 32 | 0/0/0 | 0 |

Denominator grew by exactly the two declared notes; nothing else moved.

## 3. Attacks run, and why each failed

Each item below is a concrete probe with its anchor, not an assertion of trust.

**A1 — Is the "harm watch" reproduction just equal by luck?**
`coverage` subtree serialized `sort_keys, indent=1`: **byte-identical**, 3401 bytes
at both `27cd06f` and `988b858` (`coverage subtree byte-identical: True | len 3401 3401`).
That pins every join, `covers` mapping, facet dict, `reserved` row, `uN_candidates`
list and `inverse` flag to the same values — not merely the same length.
`measure_inputs` and `safety_artifacts` (including all three sha256 values) are also
identical. Attack failed.

**A2 — Was the instrument edited to make the number?**
`git show REV:.ufo/waves/round-16/measure.py | sha256sum` =
`ea3db43fdc75634b02c3fd4f1bc7aa1e54700b2e2d1ae2261e4b78ec1782c73c` at **both**
`27cd06f` and `988b858`, and the working-tree file hashes identically. The
round-16 instrument was not touched. (The `f52f43f`/`ab0bc9b` sha256 values in
SCORECARD refer to the *round-17* `measure.py`, a different file.) Attack failed.

**A3 — Was the counting command itself redefined?**
The SCORECARD region from `### Counting command` through the closing fence hashes
`8a2b55bf811dae103aeaf6d97616c5bd19c50326b3760d5723854bfdcc74c150` at **both**
revisions. The round-17 append to `SCORECARD.md` is 76 lines, **0 deletions**, and
begins after line 817 (`+## Round 17 — declared claims`), i.e. it adds a section,
never edits the fence. Attack failed.

**A4 — Are the 32 rows real index rows, or decoys in a code block / second table?**
Walking `corpus/README.md` at `988b858` with fence tracking: **32 matching rows**,
every one `fence=False`, every one under the single heading `## Coverage map`,
lines 12–43. No duplicate, no row in a fenced block, no second table. Attack failed.

**A5 — Is the denominator complete? Could notes hide outside the counted glob?**
`git ls-tree 988b858:corpus/knowledge` returns **32 blobs, all top-level**
(no tree entries). `git ls-tree -r` count = 32, `grep '/'` = none. Same at
`27cd06f`. The full round diff (`27cd06f..988b858`, 99 files) adds no note-like
`.md` outside `corpus/knowledge/`; the only new notes are
`terminal-route-r17.md` and `idle-lock-route-r17.md`. Attack failed.

**A6 — Could the two new notes have silently claimed a U slot (inflating or
masking coverage)?**
Both new notes declare `surface: P4` / `surface: P6` in their headers and contain
**zero** `^covers: U[1-7]$` lines (`grep -c` = 0 for each, whole file). Under
`measure.py:225` (`^covers: (U[1-7])$` in the first 15 lines) they are structurally
invisible to the U-coverage scan — which is why A1's byte-identity is the expected
result and not a surprise. Attack failed.

**A7 — Retroactive source relabeling to manufacture rubric credit?**
`git diff 27cd06f 988b858 -- corpus/SOURCES.md` = **15 insertions, 0 deletions**;
no `-` line contains any `S0xx`. `round15_required` and `round16_required` blocks
are byte-identical. The 15 new rows: 12 `mined` tier-A (S056–S060, S063–S069)
whose `used-by` names exactly one of the two new notes, and 3 `rejected`
(S061, S062 — Alacritty wiki/community docs; S070 — FlareXes community) with
`used-by = —`, so they cannot credit any note. Aggregate delta is fully explained:
`A 51→63` (+12), `C 3→6` (+3), `mined 43→55` (+12), `rejected 4→7` (+3),
`queued 8→8`. Attack failed.

**A8 — Was any pre-existing index row removed or rewritten?**
`git diff 27cd06f 988b858 -- corpus/README.md`: 9 insertions, 0 deletions; no `-`
line mentioning `knowledge/`. `missing=[]` independently proves every pre-existing
note kept its row. Attack failed.

**A9 — Did anything else in the harm-watched corpus get rewritten?**
`git diff --numstat` for every touched corpus/tool file — all pure insertions:
`SCORECARD.md 76/0`, `SKILL.md 26/0`, `corpus/QUALITY.md 15/0`,
`corpus/README.md 9/0`, `corpus/SOURCES.md 15/0`,
`corpus/knowledge/idle-lock-route-r17.md 134/0`,
`corpus/knowledge/terminal-route-r17.md 131/0`,
`corpus/lessons/round-16.md 18/0`, `corpus/lessons/round-17.md 89/0`,
`tools/mado-tripwire.py 818/0`. The round-16 erratum is append-only and names the
superseded lines (`lines 131-132 at 27cd06f`) rather than editing them. No history
rewrite inside the corpus. Attack failed.

**A10 — Does the round-16 instrument disagree with the fenced counter?**
No: `measure.py` `navigation:{notes:32, indexed:32, missing:[], extra:[],
duplicates:[]}` equals the fenced counter's `indexed=32/32 … exit 0`. Both derive
the same row regex (`^\| \`knowledge/([^`]+\.md)\``, `measure.py:315`). Agreement
is a genuine second instrument, not a shared aggregate.

## 4. Regression statement

No regression found in the scope of this ticket.

- `coverage.count 7 (U1–U7)` at `988b858`: **pass**, and byte-identical subtree to
  baseline rather than equal-by-coincidence.
- Navigation complete at `988b858` (**32/32**) and at `27cd06f` (**30/30**), exit 0
  both: **pass**.
- No field of the round-16 measurement degraded between baseline and HEAD. The only
  changed values are the declared effects of the append: `navigation 30→32`,
  `calibration 14/22→15/23` (0.6364→0.6522, criterion 23 is the new grounded line,
  QUALITY.md 15/0 insertions), and SOURCES aggregates as decomposed in A7.
- Bonus cross-check, not part of the ticket: the run at `988b858` independently
  reproduces C1's stated target `15/23` (`lesson_grounded 15`,
  `criteria_total 23`) from an unmodified instrument — consistent with the
  pre-registered claim. Rubric V (`round-17/measure.py`) was **not** run here;
  that is ReMeasureC2's lane and is deliberately not duplicated.

## 5. Residual risk and verification gaps

1. **Instrument asymmetry (latent, currently moot).** The fenced navigation counter
   enumerates notes with `git ls-tree --name-only` (top level only), while
   `measure.py` coverage uses `ls-tree -r`. A future note placed in a
   `corpus/knowledge/<subdir>/` would be invisible to the counter's denominator but
   visible to the coverage scan — the two harm-watch instruments could then diverge
   silently in opposite directions. Not a defect at either measured revision (0
   nested paths at both), but it is the one structural hole I could not close by
   argument. Recommend a future round either make the counter `-r` or assert
   "no subdirectories under `corpus/knowledge`" as an explicit precondition.
2. **The counter counts rows, not truth.** `indexed=32/32` proves each note has
   exactly one row; SCORECARD's own fence states "This counts navigation, not the
   truth or freshness of a note's claims." The two new rows' `source:` citations
   (S056–S060, S063–S069) resolve to `mined` tier-A rows with matching `used-by`,
   but their documentary content was not re-verified here.
3. **Cosmetic Python warning, no score effect.** `measure.py:41` emits
   `SyntaxWarning: "\." is an invalid escape sequence` — the `\.` sits inside the
   module **docstring**, not in executable regex source. The calibration rule runs
   from code, so today's `15/23` is unaffected. It would only become hard
   breakage under a future Python that promotes invalid escapes to `SyntaxError`;
   pre-existing, identical at both revisions, and worth a one-character `\\`
   cleanup in a round that may touch the instrument.
4. **Other SCORECARD harm-watch rows are out of this ticket's scope**
   (hermetic selftest 372/372, classifier 52/52, census exit 0). I did not rerun
   them, by design, to avoid duplicating SelftestRerun/CensusRerun lanes; their
   verdict must come from those lanes, not from this report.
5. **`gate_executed:false` / `safety_executed:false`** are the instrument's declared
   design and identical across revisions; they are not evidence of a skipped gate,
   but they also mean this run says nothing about the gate's pass/fail.

## 6. Reproduction commands

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 .ufo/waves/round-16/measure.py 988b858bd6049bc709807534fd725c05264f7e60
git show 988b858:SCORECARD.md | sed -n '/^### Counting command/,/^## Fleet round 1 — interactive cutover/p' \
  | awk '/^```bash$/{f=1;next} /^```$/{f=0} f' > /tmp/fenced-counter.sh
REV=988b858bd6049bc709807534fd725c05264f7e60 bash /tmp/fenced-counter.sh   # 32/32, exit 0
REV=27cd06f bash /tmp/fenced-counter.sh                                     # 30/30, exit 0
```

Report: `.ufo/waves/round-17/w2/reports/ReMeasureHarm.md` (this file).
