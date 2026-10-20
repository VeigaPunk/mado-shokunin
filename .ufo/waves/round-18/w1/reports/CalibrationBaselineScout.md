# CalibrationBaselineScout — independent C1 recount (round 18, w1)

Seat: MadoR18.CalibrationBaselineScout. Assignment: independently recount C1 at
`d9a5a18` (23 criteria, literal lesson-citation fraction, declared 15/23 = 6.5217),
list each criterion cited/not, and check every cited `lessons/` path and
`#mistakes M<n>` anchor at that revision.

Method: committed bytes only (`git show d9a5a18:<path>`), read-only git; no host
binary, package tool, service or config tree was opened or executed. No web
source was opened, so there are no fetch receipts. No tool was installed or
upgraded.

## 1. Verdict — C1 reproduces exactly at d9a5a18

| item | observed | command |
|---|---|---|
| numbered criterion lines | **23** | `git show d9a5a18:corpus/QUALITY.md \| grep -cE '^[0-9]+\. '` |
| literal lesson-cited lines | **15** | `git show d9a5a18:corpus/QUALITY.md \| grep -cE '^[0-9]+\. .*lessons/'` |
| score (10 × 15/23) | **6.5217** | `10*15/23 = 6.521739…`, round 4 |
| `measure.py d9a5a18` c1 | `{"criteria": 23, "lesson_cited": 15, "score": 6.5217}` | `python3 -I .ufo/waves/round-17/measure.py d9a5a18` |

- Criterion numbers are exactly 1..23, each once; no extra `^[0-9]+\. ` line.
- `corpus/QUALITY.md` at `d9a5a18` is byte-identical at the pre-registration
  `d3a0000` and at current `HEAD` (= `d3a0000`): 9818 bytes, sha256
  `fedef5c17021823d4fad88c283ce8a870c34b5fe620f172f9c9dd0c04952d53d`.
  The declared baseline therefore also holds at the revision the round was
  declared from.
- Lowest-axis premise holds at baseline per the same instrument: c1 6.5217 <
  c2 6.6667 (4/6; P3 and P5 open, P1/P2/P4/P6 covered); c3 is presence+sha only
  (no score), tool sha `962919ce…`. `[OBS]`
- `d9a5a18` is on `refs/heads/master` (`git merge-base --is-ancestor` rc 0) and is
  the round-17 verifier spot-check commit (2026-10-20 12:18:08 -0300).

## 2. Criterion table at d9a5a18

`first` = literal counter (citation on the criterion's own numbered line);
`cont` = `lessons/` appears only on a wrapped continuation line, so the literal
counter does not count it.

| # | literal | citation(s) as written |
|---|---|---|
| 1 | no | — |
| 2 | no | — |
| 3 | no | — |
| 4 | no | — |
| 5 | no | — |
| 6 | yes | `lessons/round-12.md#mistakes` M1; `lessons/round-10.md:82-97` |
| 7 | yes | `lessons/round-12.md#mistakes` M2; `lessons/round-10.md:98-107` |
| 8 | yes | `lessons/round-12.md#mistakes` M3; `lessons/round-10.md:108-118` |
| 9 | yes | `lessons/round-12.md#mistakes` M6; `lessons/round-10.md:98-107` |
| 10 | yes | `lessons/round-12.md#mistakes` M7; `LOG.md:138-141,253-256` |
| 11 | yes | `lessons/round-12.md#mistakes` M8 |
| 12 | yes | `lessons/round-12.md#mistakes` M9; `lessons/round-1.md:19-22` |
| 13 | yes | `lessons/round-12.md#mistakes` M11; `lessons/round-10.md:74-78` |
| 14 | yes | `lessons/round-12.md#mistakes` M13 |
| 15 | yes | `lessons/round-12.md#inference-traps` M01-M07 |
| 16 | yes | `lessons/round-12.md#inference-traps` M03/M05/M06/M07 |
| 17 | yes | `lessons/round-13.md#mistakes` M1; outside finding `lessons/round-12-verifier-spotcheck.md` |
| 18 | cont | `lessons/round-14.md#mistakes` M4 |
| 19 | cont | `lessons/round-14.md#mistakes` M1 |
| 20 | cont | `lessons/round-15.md#mistakes` M2 |
| 21 | yes | `lessons/round-16.md#mistakes` M1/M2; outside `lessons/round-15-verifier-spotcheck.md` R15-V1/V2 |
| 22 | yes | `lessons/round-16.md#mistakes` M3 |
| 23 | yes | `lessons/round-17.md#mistakes` M1; outside `lessons/round-16-verifier-spotcheck.md` R16-V1 |

15 `yes` + 3 `cont` = 18 of 23 criteria cite a lesson somewhere in their block.

## 3. Citation resolution (all at d9a5a18)

**Paths.** 11 distinct cited lesson/spot-check paths, all present at `d9a5a18`:
`round-1.md`, `round-10.md`, `round-12.md`, `round-13.md`, `round-14.md`,
`round-15.md`, `round-16.md`, `round-17.md`, `round-12-verifier-spotcheck.md`,
`round-15-verifier-spotcheck.md`, `round-16-verifier-spotcheck.md`; plus `LOG.md`
(criterion 10). `[OBS]` via `git cat-file -e` / `git show` for each.

**`#mistakes M<n>`.** A `## Mistakes` heading exists in round-12, -13, -14, -15,
-16 and -17; its slug is exactly `mistakes`. Every referenced M row exists as a
table row in that section:

| file `#mistakes` | referenced | section rows available |
|---|---|---|
| round-12.md | M1 M2 M3 M6 M7 M8 M9 M11 M13 | M1–M14 |
| round-13.md | M1 | M1–M5 |
| round-14.md | M1 M4 | M1–M4 |
| round-15.md | M2 | M1–M3 |
| round-16.md | M1 M2 M3 | M1–M6 |
| round-17.md | M1 | M1–M5 |

No missing M row. `[OBS]`

**Line ranges.** Criterion 10's `LOG.md:138-141` is the stale-count paragraph
(313 quoted vs 315 measured) and `:253-256` the S3 off-by-one paragraph — both
ground "counts copied or summarized incorrectly". `round-10.md:82-97` =
"A citation that cannot be re-derived is a clock, not a value";
`:98-107` = "The commit is the binding revision"; `:108-118` = "A gap is not
false — it is a bill every reader pays"; `:74-78` = "scratch is not a handover
surface". `round-1.md:19-22` = outside-lane spot-check not supplied. All ranges
are inside their files (round-10 227 lines, round-1 126, LOG 1285). `[OBS]`

**Outside labels.** `round-15-verifier-spotcheck.md` carries `R15-V1` (line 254)
and `R15-V2` (line 268); `round-16-verifier-spotcheck.md` carries `R16-V1`
(line 164); `round-12-verifier-spotcheck.md` records the S030 disagree/adjudicate
rows. All resolve. `[OBS]`

**Disclosed non-grounding.** Criterion 8's secondary citation
`round-10.md:108-118` grounds record debt (round-12 M4), not planned paths; the
provenance note below criterion 16 says so explicitly and names
`round-12.md#mistakes M3` as the criterion-8 grounding. This is disclosed, not an
undisclosed defect.

## 4. Rule sensitivity of the literal counter

| counting rule | count | score (10×) |
|---|---|---|
| declared literal: `^[0-9]+\. .*lessons/` per criterion line | 15/23 | **6.5217** |
| citation anywhere in the criterion block | 18/23 | 7.8261 |
| literal + anchor slug must resolve exactly (see §5 F1) | 13/23 | 5.6522 |

The declared number is reproducible under its recorded rule. The spread between
the three rules is 2.17 points — exactly the "report literal versus semantic
counters separately" boundary of criterion 22.

## 5. Findings

**F1 (precision, undisclosed) — two literal citations carry a non-exact anchor.**
Criteria 15 and 16 cite `lessons/round-12.md#inference-traps`. The heading is
`## Inference traps (external, not incidents)` at line 28, whose slug is
`inference-traps-external-not-incidents`; there is no heading whose slug is
`inference-traps`. The M rows do resolve (M01–M07 exist under that heading), so
the evidence is reachable, but the fragment itself is a prefix, not an anchor.
2 of the 15 literal citations are affected. `[OBS]`

**F2 (instrument pin, adjacent to R17-V5) — the round-17 lesson pin names the
ab0bc9b instrument, not the landed one.** `measure.py` full-file sha256:
`a280b3ab…` at `f52f43f` (9634 B), `4023124fa40931f630197920e2534f468dc2b1cacfe010826b52032db846466b`
at `ab0bc9b` (11404 B, the value `lessons/round-17.md` pins),
`de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc` at `f71ccbe`
and at `d9a5a18` (11963 B). The delta is one c2-only hunk (Registry-section
scoping + duplicate-id exit at f71ccbe); the c1 branch is byte-identical across
`ab0bc9b`/`f71ccbe`/`d9a5a18` (c1 section sha256 `b07c82ab…`). So: the declared
c1 number is stable under either instrument bytes, and "instrument unchanged"
(pre-registration) is true against the round-17 tip `f71ccbe`; but any round-18
receipt that pins `measure.py` should name `de4c422b…`, not `4023124f…`. `[OBS]`

**F3 (routed R17-V1/V2 corroboration, read-only).**
- `tools/mado-tripwire.py`: sha256 `4ced68d3…` at `988b858` (32279 B),
  `7a98720ed3c0ea1676714381a9289a65dd2a416f98b764e2b52517f81ef31fe7` at `f71ccbe`
  (37437 B), `962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072`
  at `0ab1ccc` and at `d9a5a18` (37948 B). This matches the spot-check: the
  round-17 report's `7a98720e…` is the f71ccbe tool; the landed tool is
  `962919ce…`.
- The six affected receipts (`tripwire-r13..r16.txt`, `tripwire-anchor-r15.txt`,
  `tripwire-pacmanlog-join.txt`) were last changed at `f71ccbe`, carry neither
  `tool_sha256` nor `measured_commit` anywhere in their bytes, and `0ab1ccc`
  does not touch any of them (`git diff --name-only f71ccbe 0ab1ccc`). The
  spot-check's "the re-cut is unreceipted" holds. `[OBS]`
- Wording boundary for the round-18 Mistakes row: git **does** record the
  `962919ce…` tool bytes at `0ab1ccc`. The defect is that the *receipts* were
  not re-cut in any committed tree, not that the tool sha is absent from git.
  Writing "git never recorded `962919ce…`" would be falsified by
  `git show 0ab1ccc:tools/mado-tripwire.py | sha256sum` in one command.
- `lessons/round-17.md:175-176` at `d9a5a18` reads "...tool sha256
  `962919ce…`; all real-transcript receipts re-cut with identical counts." The
  first clause is true of `0ab1ccc`; the second clause is unreceipted as above.

## 6. Unknowns and limits

- `[UNK]` Whether L1 adopts an anchor-exact citation rule; if it does, the
  baseline becomes 13/23 = 5.6522 and the 18/26 target still needs 13 exact
  citations among 26. I did not choose a rule — both counts are reported.
- `[UNK]` Semantic adequacy of each citation beyond the ground it names (e.g.
  whether M1's pin-suffix incident fully covers criterion 6's wording) was
  checked at title/paragraph level, not scored as a judgment.
- No host state, package tool, service, compositor, transcript or credential
  file was read or touched; this seat contributes no host observation.
- Confidence: high for every count, path, anchor and sha above (deterministic
  committed-byte reads). The only judgment call is F1's "anchor must be exact",
  which is stated as a boundary, not as a verdict on the declared number.

## Files written

- `.ufo/waves/round-18/w1/reports/CalibrationBaselineScout.md` (this report).
- No fetch receipts (no web source opened). No tool install/update.
