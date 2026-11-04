# mado — round 69 report

Lane: `mado-shokunin`. Round 69, hyaku run 15, attempt 1. Session: in-session L1 `MadoR69`.
Base `04093b83f73a841117d3b31dbb2a6063f4f2a454`; freeze `789a87f1a667b43dd759222a2f048bf8f75b43ce`;
instruments at `5fc29ae72e66b9347d576c796ee656aea2fdd04c`; instruments-repaired content
`296ed0d75e361387908cf2dd418d3677f49f94c8`.

## Work performed

Round 69 declares **two claims**, each on a distinct axis, each with a frozen finite denominator
and a committed do-nothing control that misses the target:

- **C1 — calibration:** the hardened control harness kills *paired* (decision + oracle) forgeries.
- **C2 — operability:** the guard census requires the guard key in key position and requires the
  guarded environment to reach a `git` launch (dominance), not merely to occur in the file.

Work items (evidence pointer after each):

- Read the round contract, mission/axes, lane PROVINCE/SCORECARD/corpus and the r68 lesson and
  spot-check before declaring (`corpus/lessons/round-68-verifier-spotcheck.md`,
  `corpus/lessons/round-68.md`).
- Froze both claims, the eleven-case control set, the three recipe texts and the two do-nothing
  baselines before any candidate data — `789a87f1`
  (`.ufo/waves/round-69/claims-declaration-r69.md`, `controls/c2-controls-r69.json`,
  `control-baseline-r69.txt`, `proto/`).
- Built and landed the two new counters and the harness successor — `5fc29ae7`
  (`quality/counters/c1-r69-landing-controls.py`, `c1-r69-paired-recipes.py`,
  `c2-r69-guard-dominance.py`).
- Measured both claims at the content revision — `5fc29ae7`, receipts
  `.ufo/waves/round-69/measurement-c1-r69.txt`, `measurement-c2-r69.txt`.
- Dispatched one v1 wave of 12 seats (spec `98bff016`, validated dispatch
  `.ufo/waves/round-69/w1-dispatch.json`, `spawn=12`; seats under `.ufo/waves/round-69/w1/`).
- Closed the C2 reviewer's six bounded defects against the frozen sentence — `6d21f535`,
  receipt `.ufo/waves/round-69/c2-classifier-repair-r69.txt` (pre-fix 7 violations → post-fix
  8/8 cases; frozen controls and the 20/13/13 population unchanged; selftest 40/40 with the six
  cases pinned).
- Closed the C1 reviewer's S1–S5 — `296ed0d7`
  (`quality/counters/c1-r69-paired-recipes.py`: base harness required and its absence a setup
  error, `py_compile` gate before any kill, `OSError`/`SubprocessError` → rc 2 with a reason;
  harness adopted from the seat draft `9461a059…`, `r69-c1` scratch dirs, round-69 limits
  paragraph; selftest 27/27).
- Landed the sourced knowledge entry, the registry row, the lesson, QUALITY 111, the index row and
  Frontier bullet, PROVINCE and SKILL gate rows, the tool-ledger rows, the SCORECARD section and
  the LOG entry — `5864b00d`, `3cd68aa3`, `fc0387b9`.
- Harm watch: gate `MADO_SELFTEST: 460/460`; axis table 3/3 MATCH; landing counters; instrument
  selftests (r69 harness 59/59, C1 counter 27/27, C2 counter 40/40; r68 counters 27/27, 52/52,
  26/26); cross-set check that the r69 rule scores 11/11 on the round-68 control set too
  (`.ufo/waves/round-69/cross-set-r69.txt`).
- Frontier step: census exit 0 at start (374 rows) and end (375 rows); one new `A/docs/mined` row
  S438; one mistake mined with class/evidence/captured-by/fix; C2's claim rests on S438.
- Curation: `considerthese/2026-10-28.md` proposal 4 (a live-tool table) was read and is **not**
  adopted this round (reported, not acted on). Assimilation: none — no `merge/mado/` theme was
  taken; declared as such.
- Tooling: nothing installed or upgraded; no pacman transaction (host pause respected).

## Landed changes

| Change | LOG entry | Commit |
|---|---|---|
| Frozen claims, control set, recipes, do-nothing baselines | round-69 bullet 1–2 | `789a87f1a667b43dd759222a2f048bf8f75b43ce` |
| Wave spec and validated dispatch (12 seats) | round-69 bullet 3 | `98bff016d0ef151aceedf03d75239b81c9f6eeed` |
| `quality/counters/c1-r69-landing-controls.py`, `c1-r69-paired-recipes.py`, `c2-r69-guard-dominance.py` | bullet 4 | `5fc29ae72e66b9347d576c796ee656aea2fdd04c` |
| Claim measurements, harm watch, census start, ready file | bullet 4–5 | `6a5cefd252c41c7ff71217da65126fc831f8bc34` |
| C2 classifier repair (six review findings) + receipt | bullet 5 | `6d21f535492f74dfef538eecb303486a1588c1be` |
| C1 instrument repairs (S1–S5) | bullet 5 | `296ed0d75e361387908cf2dd418d3677f49f94c8` |
| Entry, S438, lesson, QUALITY 111, index/frontier, PROVINCE, SKILL, ledger, SCORECARD, LOG, measurement | bullet 6–7 | `5864b00da73631cad2b9f719c4ea9c9a8eaca509` |
| Criterion-107 locator cells to single line pins | bullet 7 | `3cd68aa33fa9986a02614922370b714413d0dcdc` |
| Registry `used-by` cells for S436/S437 and the lesson's old→new log | bullet 7 | `fc0387b970e602e4588bbf07f95675f88678094b` |

## Before → after measurements

**C1 — calibration.** Counting command (frozen at the declaration):

```sh
python3 quality/counters/c1-r69-paired-recipes.py --repo . --rev <rev> \
  --base-rev 04093b83f73a841117d3b31dbb2a6063f4f2a454 --scratch-root <scratch>
```

- Before, at the base revision (`04093b83`): `selftest=absent killed=0/3 applied=0/3 base=0/3
  verdict=TARGET_MISSED` rc 1 — the harness does not exist there, and the do-nothing control (the
  r68 harness under the same three recipes) survives all three (`killed=0/3 applied=3/3`, green
  52/52). Bounded `10 × killed / 3` = 0.0000.
- After, at `296ed0d7`: `selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET` rc 0.
  Bounded 10.0000. Receipt `.ufo/waves/round-69/measurement-r69.txt`.

**C2 — operability.** Counting command (frozen at the declaration):

```sh
python3 quality/counters/c2-r69-guard-dominance.py --repo . --rev <rev> \
  --base-rev 04093b83f73a841117d3b31dbb2a6063f4f2a454 \
  --controls .ufo/waves/round-69/controls/c2-controls-r69.json --scratch-root <scratch>
```

- Before: the counter does not exist at the base revision, and the *held rule* — the round-68
  classifier on the same frozen eleven cases — scores `controls=7/11` (it accepts
  `value-position-only`, `dead-branch-only`, `uncalled-helper`, `overwritten-env`).
  Receipt `.ufo/waves/round-69/control-baseline-r69.txt`.
- After, at `296ed0d7`: `population=20 readers=13 guarded=13 unguarded=0 controls=11/11
  base_controls=7/11 verdict=TARGET_MET` rc 0. Bounded `10 × guarded / readers` = 10.0000; the
  population count is 13/13 at both ends, so the move is discrimination, and the report says so.
  Receipt `.ufo/waves/round-69/measurement-r69.txt`.

No claim was narrowed after data; both predicates are the same sentence in the declaration, the
counter's code and the printed label. Two instrument defects (C2: six bounded violations of the
frozen sentence; C1: an absent base leg that could print `TARGET_MET`, a missing compile gate, a
timeout path with no contract line) were repaired *before* landing, each with a red-before
receipt, and no frozen predicate changed.

## Sources & frontier

- Census command (both ends):
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
  — start `mado ok` exit 0, 374 data rows (`census-start-r69.txt`); end `mado ok` exit 0, 375 data
  rows (same command at the final tip).
- Rows added: **S438** (tier `A`, kind `docs`, status `mined`) — git v2.56.0 `Documentation/git.adoc`,
  fetched three times byte-identically, sha256 `050c5330…`, 47005 B, `git.adoc:14,178-182,927-929`.
- Rows touched old→new: S436 `used-by` and S437 `used-by` each gain
  `corpus/knowledge/gate-guard-dominance-r69.md`; no `status` or `recheck` cell changed (logged in
  `corpus/lessons/round-69.md` § Gate).
- Frontier rows advanced: one `corpus/README.md` Frontier bullet plus one index row for the new
  entry; navigation 80/80 → 81/81 (axis publication re-derived in `SCORECARD.md`).
- Sourced claim: **C2** rests on S438 (its entry cites it with locators; criterion 107
  `rows=8 covered=8 miss=0 verdict=OK`).
- Lesson `## Gate`: one admit (S438, URL + access date + a ≤25-word located quote) and one reject
  (`git-replace.adoc` as a new row — duplicate scope with held S436; flip condition recorded).
- Assimilation: none this round (no `merge/mado/` theme taken); `considerthese/2026-10-28.md`
  proposal 4 read and not adopted.


### Gate results at the final records tip (`fc0387b9`)

Receipt `.ufo/waves/round-69/final-gates-r69.txt` (one line per gate, all at that revision):

| gate | result |
|---|---|
| axis table | `MADO_AXIS: checked=3 mismatched=0` (navigation 81/81, calibration 86/86, operability 12/12) |
| index | `indexed=81/81 missing=0 dangling=0 duplicates=0` |
| index rows | `rows=81 errors=0 warns=3` (the three warnings are the pre-existing cited-glob and row-shape warnings) |
| tool ledger | `population=116 ledger_rows=116 uncovered=0 dangling=0` |
| used-by | `entries=81 rows=375 missing=0 extra=0 dangling=0 conflict=0 stale=0` |
| criterion 107 | `CHECK107: rows=8 covered=8 miss=0 verdict=OK` |
| hermetic gate | `MADO_SELFTEST: 460/460 assertions passed` |
| landing instrument | `MADO_LANDING_COUNTERS: GREEN (nav=0 usedby=0 ledger=0 citecheck=0)` |
| evidence pointers | `PRED-PTR-r36-v1 … dangling_r36=0 … verdict=TARGET_MET` |
| landed contract | `CHECK96: frozen=9 landed=9 added=0 removed=0 unregistered=0 verdict=OK` |
| census | `mado ok`, exit 0, 375 rows |

Two gates are red for reasons that predate the round and are reported, not smoothed:

- `check-freeze-order.py --round 69 --wave w1` reads `verdict=FAIL reason=no_freeze` because the
  gate's FREEZE set expects `.ufo/waves/round-N/claims-frozen.md` + `registration.md`, while this
  lane has used `claims-declaration-rN.md` since the r56 era; **round 68 reads the same
  `no_freeze`**. The freeze-before-launch order is instead evidenced by commit and file times:
  freeze `789a87f1` 22:42:47-03:00, ready file 22:44:47, dispatch marker 22:47:43.
- `check-deliverables.py` on the round-68 seat reports reads `verdict=FAIL
  (reports=6 declared=4 exists=1 absent=3 undeclared=5)`; the cadence seat reproduced the same
  class at the base (`reports=12 declared=4 exists=1 absent=3 undeclared=11`, rc 1) and traced it
  to seat-relative `## Deliverables` bullets and missing `Report:` trailers in that wave — not to
  this round's files.

## Lane state

- `Stale-lane`: no other mission of this lane is open; the lane is respawn-per-round under the
  hyaku driver, and this report closes round 69 only.
- Tool installs: none (no `uv`, `npm`, `cargo`, binary or pacman transaction this round); the
  pacman pause was respected.
- Inherited state: the lane was clean at the base (`tracked=0 untracked=0`, `ahead=0`), so nothing
  was inherited from an earlier attempt of this round and nothing had to be resolved.

## Trend verdicts

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | unchanged | No new province ground; the round is instrument craft. The new entry documents a lane-tooling guard grammar (adjacent to, not inside, the desktop/compositor axis), and S438 is one technical source opened, not a new surface. |
| quality | improved | Two new measured instruments with frozen do-nothing controls (0/3 and 7/11), six C2 violations and five C1 defects repaired before landing with red-before receipts, QUALITY 111 added, and the cross-set check shows the new rule loses nothing the old set caught (11/11 on the round-68 set). |
| discernment | improved | The round mines its own predecessor's equivalent-mutant misclassification (M69-1) and the round-68 classifier's value-position over-inclusion (M69-2), excludes the equivalent recipe from the frozen denominator with a probe, and names the limits of both claims instead of widening them. Three of the round's own instrument defects (M69-3 and the two review sets) were caught by attack seats and closed, not smoothed. |

## SHONEN

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — historical assertion `corpus/knowledge/executor-test-sufficiency.md`; round 69 adds two gate rows (`mado-r69-paired-recipes`, `mado-r69-guard-dominance`) but no outside-lane promotion authority.
- [~] At least one end-to-end domain task executed and logged in LOG.md — historical assertion round 3; round 69 is instrument craft, and its end-to-end task is the frozen counting commands run green at `296ed0d7` (`.ufo/waves/round-69/measurement-r69.txt`).
- [~] Instructions executable by an agent without oral context — the two new gate rows carry entry command, verdict map, selftest and pinned path; the declaration and lesson are self-contained; dispatched subagents still do not satisfy the outside-lane rule.
- [~] No cross-domain bleed (PROVINCE.md still accurate) — PROVINCE.md carries the round-69 paragraph and names the instruments as lane record tools; no outside-lane adjudication in this round.
