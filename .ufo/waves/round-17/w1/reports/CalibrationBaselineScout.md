# CalibrationBaselineScout — independent C1 recount at 27cd06f and 0175f13

Date: 2026-10-20. Role: leaf scout, read-only. Scope: the literal
QUALITY lesson-citation fraction (C1) and resolution of every `lessons/...`
path and `#mistakes M<n>` cited from `corpus/QUALITY.md`. No subagents, no
writes outside this report, no pacman/sudo/systemctl/hyprctl/live probes, no
`.jj` commands, no tools installed.

## 1. Declared counting rule

Pre-registration `0175f13:SCORECARD.md:836-841`:

> Command: `git show REV:corpus/QUALITY.md | grep -cE '^[0-9]+\. .*lessons/'`
> over `grep -cE '^[0-9]+\. '`. Before 14/22 = 6.3636 → target ≥ 15/23.

[OBS] This is a line-anchored (literal) counter: a citation only counts when
the string `lessons/` appears on the criterion's numbered start line.

## 2. Recount

```text
$ for R in 27cd06f 0175f13; do git show $R:corpus/QUALITY.md | grep -cE '^[0-9]+\. '; done
27cd06f: 22
0175f13: 22
$ for R in 27cd06f 0175f13; do git show $R:corpus/QUALITY.md | grep -cE '^[0-9]+\. .*lessons/'; done
27cd06f: 14
0175f13: 14
$ git show <REV>:corpus/QUALITY.md | sha256sum
27cd06f: 88bb068106f2c10e261c84c1f4e1eb5d6d35a4696da3220f14d9c3dafa10c00a
0175f13: 88bb068106f2c10e261c84c1f4e1eb5d6d35a4696da3220f14d9c3dafa10c00a
$ git diff --name-only 27cd06f 0175f13 -- corpus/
(empty)
```

[OBS] Literal fraction is **14/22 at both revisions** = 0.636364 → 6.3636 on
the lane's ×10 scale. QUALITY.md is byte-identical across the two revisions
(same sha256; only `SCORECARD.md` and
`.ufo/waves/round-17/evidence/census-start.txt` changed between them), so the
pre-registered "before" value is reproducible and did not drift during
pre-registration. The declared target ≥ 15/23 therefore needs one new
criterion whose **numbered line** carries a `lessons/` reference.

Numbering integrity: the 22 matched lines carry unique numbers 1..22 in order
(no duplicate or nested numbering; no stray `N. ` list items elsewhere).

## 3. Per-criterion citation status (identical at both revs)

`on-line` = literal counter; `block` = `lessons/` anywhere in the criterion's
own paragraph (criterion 18/19/20 wrap the citation onto an indented
continuation line, so they count as block-cited only).

| # | start line | on-line | block | cited target(s) |
|---|---|---|---|---|
| 1 | 3 | no | no | — |
| 2 | 4 | no | no | — |
| 3 | 6 | no | no | — |
| 4 | 7 | no | no | — |
| 5 | 8 | no | no | — |
| 6 | 12 | yes | yes | round-12#mistakes M1; round-10.md:82-97 |
| 7 | 13 | yes | yes | round-12#mistakes M2; round-10.md:98-107 |
| 8 | 14 | yes | yes | round-12#mistakes M3; round-10.md:108-118 |
| 9 | 15 | yes | yes | round-12#mistakes M6; round-10.md:98-107 |
| 10 | 16 | yes | yes | round-12#mistakes M7; LOG.md:138-141,253-256 |
| 11 | 17 | yes | yes | round-12#mistakes M8 |
| 12 | 18 | yes | yes | round-12#mistakes M9; round-1.md:19-22 |
| 13 | 19 | yes | yes | round-12#mistakes M11; round-10.md:74-78 |
| 14 | 20 | yes | yes | round-12#mistakes M13 |
| 15 | 21 | yes | yes | round-12#inference-traps M01-M07 |
| 16 | 22 | yes | yes | round-12#inference-traps M03/M05/M06/M07 |
| 17 | 34 | yes | yes | round-13#mistakes M1; outside finding round-12-verifier-spotcheck.md |
| 18 | 43 | no | yes (l.49) | round-14#mistakes M4 |
| 19 | 50 | no | yes (l.55) | round-14#mistakes M1; outside R13-V1 |
| 20 | 72 | no | yes (l.77) | round-15#mistakes M2; orchestrator ruling |
| 21 | 82 | yes | yes | round-16#mistakes M1/M2; outside round-15-verifier-spotcheck.md R15-V1/V2 |
| 22 | 107 | yes | yes | round-16#mistakes M3; PlanningWalk note |

Tally: on-line cited = 6,7,8,9,10,11,12,13,14,15,16,17,21,22 = **14**;
on-line uncited = 1,2,3,4,5,18,19,20 = **8**. Block-cited = **17** (14 + 18,
19, 20), block-uncited = **5** (the base admission bar 1-5). Block-scoped
fraction would read 17/22 = 0.772727 → 7.7273. [OBS] The declared rule is the
literal one, so 14/22 is the correct C1 numerator; the 3-criterion gap is a
drafting property of criteria 18-20, not a miscount.

## 4. Citation resolution at each revision

All 9 distinct lesson paths cited by QUALITY.md exist at both revs
(`git cat-file -e 0175f13:corpus/<path>` OK; corpus tree identical at
27cd06f):

| Path | resolves |
|---|---|
| lessons/round-1.md | OK, 126 lines; cited range 19-22 present |
| lessons/round-10.md | OK, 226 lines; ranges 74-78, 82-97, 98-107, 108-118 present |
| lessons/round-12.md | OK, 126 lines; `## Mistakes` present; `## Inference traps (external, not incidents)` at l.28 |
| lessons/round-12-verifier-spotcheck.md | OK, 17 lines |
| lessons/round-13.md | OK, 95 lines; `## Mistakes` M1-M5 |
| lessons/round-14.md | OK, 214 lines; `## Mistakes` M1-M4 |
| lessons/round-15.md | OK, 200 lines; `## Mistakes` M1-M3 |
| lessons/round-15-verifier-spotcheck.md | OK, 291 lines; R15-V1 at l.254, R15-V2 at l.268 |
| lessons/round-16.md | OK, 159 lines; `## Mistakes` M1-M6 |

Every cited `#mistakes M<n>` id exists as a table row at that rev:

- round-12: M1 (l.13), M2 (l.14), M3 (l.15), M6 (l.18), M7 (l.19), M8 (l.20),
  M9 (l.21), M11 (l.23), M13 (l.25) — all present; `## Mistakes` heading
  present, so the `#mistakes` fragment resolves.
- round-12 `#inference-traps`: heading at l.28 and rows M01-M07 at l.34-40;
  criterion 15's full M01-M07 span and criterion 16's M03/M05/M06/M07 subset
  all exist.
- round-13: M1 present (`scope / duplicate evidence`, S030 outside
  disagreement). round-14: M4 (`vacuous existence predicate`) and M1
  (`scope / retained-data wording`). round-15: M2 (`host partial upgrade`,
  cites `/var/log/pacman.log:2429-2437`). round-16: M1 (`Host-safety harm
  from helpful-tool installation`), M2 (`Unauthorized live probe …`), M3
  (`Lowest-axis selection omitted active calibration`).

No dangling lesson path or M-id found at either revision.

## 5. Findings

1. [OBS] C1 baseline is **14/22 literal**, reproduced independently at both
   27cd06f and 0175f13; arithmetic 6.3636 checks. The pre-registration's
   "before" number is sound.
2. [OBS] The declared rule undercounts three genuinely cited criteria (18, 19,
   20) because their citations wrap to continuation lines. Literal vs
   block-scoped = 14/22 vs 17/22; the SCORECARD's QUALITY22 separately demands
   "literal versus semantic citation counters separately", so keeping literal
   as the scored counter is consistent, but the semantic number should be
   stated when C1 is closed.
3. [INF] Consequence for C1 drafting: the round-17 criterion and its M1
   lesson line must place the `lessons/round-17.md#mistakes M1` reference on
   the criterion's numbered start line; a wrapped citation writes 15/23 as
   14/23 and misses the declared target. Confidence: high (direct consequence
   of the grep rule).
4. [OBS] All cited lesson paths and M-ids resolve at both revs; no citation
   defect exists in QUALITY.md independent of C1's own change.
5. [OBS] Minor topical note (baseline-carrying, low severity): criterion 12's
   secondary `lessons/round-1.md:19-22` resolves and discusses "outside-lane
   spot-check: not supplied … no criterion is added … without an
   outside-disagreement lesson behind it" — adjacent to, but not literally,
   the `[x]`-requires-named-non-author-verifier rule. The primary
   `round-12#mistakes M9` row carries that rule. Not a dangling citation;
   reported only so a future reader does not treat round-1:19-22 as the
   criterion's sole grounding.
6. [OBS] No tool was installed or updated. Commands used: `git show`,
   `git diff`, `git cat-file`, `grep`, `awk`, `nl`, `sed`, `sha256sum`,
   `python3 -c` arithmetic. No package/service/compositor operation.

## 6. Unresolved / out of scope

- Whether L1's round-17 QUALITY criterion actually carries the citation on
  its numbered line: future artifact, [UNK] here.
- R16-V1's receipt mislabeling (`evidence/frozen-tampered.json` at 9dcf248) is
  routed to reviewer lanes; this report only confirms the calibration counts
  and QUALITY.md citation graph.

Confidence: high. Evidence is committed git bytes at named revisions only.
