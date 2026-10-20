# RevSeparability — round-17 causal separability attack

Seat: `MadoR17.RevSeparability` (reviewer, leaf). Date 2026-10-20.
Baseline `27cd06f` / pre-registration `0175f13`; inspected HEAD `3e9848a`
(C1 and C2 committed, C3 not yet). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Read-only work: `git show`,
`git archive`, `measure.py` on committed revisions, and a scratch clone under
`/tmp` for the commit-replay removals. No lane commits, no lane edits, no
pacman/sudo/systemctl/hyprctl/live probe, no jj, no tool installs.

## Verdict

C1 and C2 are causally separable **as landed**, with commit-granularity
removal tests executed; C3 is structurally separable pending its commit (the
tool is absent). The one C1↔C3 metric path was closed before measurement.

- **C1 is separable.** `measure.py 245fd11` = `14/22`; with the C1 commit
  `3722ba4` = **`15/23`**; reverting `3722ba4` from `3e9848a` returns
  **`14/22`** while C2 stays `4/6`. C1's increment exists only with C1's
  commit, and the C1 commit touches no C2 path.
- **C2 is separable.** `measure.py ab0bc9b` (instrument only) = `2/6`;
  with the C2 commit `a9998d1` = **`4/6`** (`P1,P2,P4,P6`, `rejected []`,
  `u_routes 7`); reverting `a9998d1` from `3e9848a` returns **`2/6`** while C1
  stays `15/23`. The C2 commit touches no QUALITY path.
- **C3 is separable structurally.** It is not committed yet
  (`tools/mado-tripwire.py` absent at HEAD); `measure.py` reports C3 as
  presence+sha only (`measure.py:286-291`) and never executes it. Its selftest
  inputs are DIR-relative fixtures and its scan inputs are the named OJSONL
  files; no C1/C2 path is an input. The removal test is exact once the C3
  commit lands: `measure.py` flips `c3.tool_present` only for that commit.
- **The one genuine C1↔C3 coupling path was closed before measurement.** A
  lesson-cited QUALITY criterion for M2/tripwire (draft "criterion 24") would
  have moved C1's numerator and denominator: a C3-only tree reaches the
  pre-registered C1 target `15/23` on its own and `F − C1` still reads
  `15/23`. The landed C1 commit contains **criterion 23 only** (23 criteria,
  15 cited), and SCORECARD §"Round-17 pre-measurement corrections" records
  the exclusion. The arithmetic below is the guard if a later commit adds such
  a criterion.

## Executed removal matrix (a scratch clone of the lane; read-only on lane)

| tree | rev | C1 cited/criteria | C2 | C3 present |
|---|---|---|---|---|
| B pre-registration | `0175f13` | 14/22 | 2/6 `P1,P2` | no |
| instrument only | `ab0bc9b` | 14/22 | 2/6 `P1,P2` | no |
| C2 commit | `a9998d1` | 14/22 | **4/6** `P1,P2,P4,P6` | no |
| + label mutant fixture | `245fd11` | 14/22 | 4/6 | no |
| + C1 commit | `3722ba4` | **15/23** | 4/6 | no |
| F pre-measurement corr. | `3e9848a` | 15/23 | 4/6 | no |
| C1-only replay (`0175f13` + C1 paths + measure) | temp `c1only` | **15/23** | 2/6 | no |
| F − C2 (`git revert a9998d1` on `3e9848a`) | temp `f` | 15/23 | **2/6** | no |
| F − C1 (`git revert 3722ba4` on `3e9848a`) | temp `f1` | **14/22** | 4/6 | no |
| F − C3 | = F | 15/23 | 4/6 | no (C3 absent) |

The C1-only replay checked out `3722ba4`'s QUALITY/lessons/label files onto
`0175f13` plus the neutral `measure.py` from `ab0bc9b`. The reverts were made
with `git revert --no-commit` in `/tmp/mado-sep` (a `--no-hardlinks` clone).
No lane ref or worktree was modified.

File-level disjointness backs the metric result: `a9998d1` changes
`corpus/README.md`, `corpus/SOURCES.md` and the two notes only; `3722ba4`
changes `corpus/QUALITY.md`, `corpus/lessons/round-16.md`,
`corpus/lessons/round-17.md`, `label-check.py`, `label-claims.json` and the
label receipt only; `3e9848a` changes SCORECARD only; `fc6f960` is evidence
only; `245fd11` is one fixture only.

## Why each metric separates (input graph)

`measure.py` (committed `f52f43f`, tightened `ab0bc9b`) reads:

- `c1`: `corpus/QUALITY.md` only (`measure.py:87-100`).
- `c2`: `corpus/SOURCES.md` + `corpus/knowledge/*.md` only
  (`measure.py:103-282`); it does not read QUALITY, `tools/`, or evidence JSON.
  The tightening adds T2 exact `surface: P<n>` line, T3 legacy credit pinned
  to the three 27cd06f entries, T4 a cited mined-A upstream https row of kind
  docs/spec/code naming the surface, T5 three non-blank lines per required
  section — strictness only; C2 was re-measured under both instrument versions.
- `c3`: `tools/mado-tripwire.py` presence+blob sha only
  (`measure.py:286-291`); it never executes the tool.

`label-check.py` reads `label-claims.json` plus `git show` of the pinned docs
and receipts (and, for mutant claims, inline `doc_text` + the named fixture);
no C2/C3 path is an input. Verified in the `F − C2` clone: output is identical
to `F` — `LABEL_SUMMARY: 4/7`, `EXPECT_SUMMARY: 7/7`, exit 1 (exit 1 is
expected because three control claims declare MISMATCH). The tripwire contract
reads only the JSONL paths given; its fixtures are DIR-relative and
self-contained (verified: `expected.json` args are `incident-replica.jsonl`,
`..., multi`, `nodata`; no absolute or lane paths).

## C1↔C3 arithmetic (the guard that was closed)

The draft `QualityDraft.md` contained criterion 23 (R16-V1/M1) and a
*candidate* criterion 24 `(lesson: lessons/round-17.md#mistakes M2 ...)`.
Both first lines match the pre-registered `^[0-9]+\. .*lessons/` pattern.
Measured on a provisional tree, exact grep rule:

| tree | criteria | cited | C1-attributed | score |
|---|---:|---:|---:|---:|
| B | 22 | 14 | 0 | 6.3636 |
| C1-only (+23) | 23 | 15 | 1 | 6.5217 |
| C3-only (+24) | 23 | 15 | **0** | **6.5217** |
| F (+23+24) | 24 | 16 | 1 | 6.6667 |
| F − C3 (23 only) | 23 | 15 | 1 | 6.5217 |
| F − C1 (24 only) | 23 | 15 | **0** | 6.5217 |
| F with uncited 24 (+23+uncited24) | 24 | 15 | 1 | **6.2500** |

The C3-only row meets the pre-registered C1 target without any R16-V1
criterion; the uncited row pushes C1 below its own baseline. This is why
criterion 24 must not be admitted as C1 content. The landed state avoids it:
`git show 3722ba4:corpus/QUALITY.md` has 23 criteria / 15 cited, with only
criterion 23 and no M2/tripwire criterion; SCORECARD records the exclusion.
If a future round admits such a criterion, report C1 from `F − C3` and assert
the R16-V1-attributed criterion count, not the literal count alone.

## Findings (severity order)

### S1 — C1↔C3 QUALITY-criterion coupling: avoided, still the guard (high if reopened)

Landed: not present (criterion 23 only). Reopened form: any lesson-cited
criterion appended for C2/C3 moves C1's literal numerator and denominator, and
an uncited one can sink C1 below baseline. Keep the SCORECARD exclusion text
with the C1 measurement; do not admit criterion 24 under a C1 heading.

### S2 — commit granularity: resolved for C1/C2 (was high, process)

`a9998d1` (C2) and `3722ba4` (C1) are single-claim commits on neutral
instrument/evidence commits, so the reverts above are exact. C3 still needs its
own commit. `corpus/lessons/round-17.md` is already in the C1 commit (M1, M3,
M4, M5) and will gain M2 when C3 lands; line-level removal is then required for
the lesson row, but it is not a metric input, so it cannot move any of the
three counts. The same applies to SKILL/SCORECARD.

### S3 — rubric V as measured is stricter than its declaration (medium)

The pre-registration's "C2 needs no tool or criterion" is false as worded: the
declared command is `measure.py`, and the committed instrument adds T2–T5
facets not in the rubric text. This is disclosed in SCORECARD's correction and
is strictness, not widening; C2 is 2/6 at both instrument revisions and 4/6
with the notes, `rejected []`. A closure should compare the *implemented*
rubric, not the shorter declaration.

### S4 — C1's tuple is ambiguous under any added criterion (medium)

`16/24` scores higher than `15/23` but is a different pair. The landed C1 has
the exact pre-registered pair `15/23`; keep it. If another criterion is ever
added, report the pair and the claim-scoped pair separately.

### S5 — label check now exercises outcome tokens and revision binding (low; resolved)

The committed checker (after CriticC1) extracts only outcome tokens: a
`MADO_<NAME>: <token>` line, a `"finding"` value, or the got-side of a selftest
row (`label-check.py:75-90, 92-135`). It adds optional `measured_commit`,
`expect`, and `EXPECT_SUMMARY`. The seed set has 7 claims: the R16-V1 red and
the `want-side-only` / `superseded-commit` mutants are MISMATCH; the four ok
claims are `frozen-match-green`, `spotcheck-selftest-final-green`,
`honest-red-green`, `recut-green`; `EXPECT_SUMMARY: 7/7`, exit 1
(`evidence/label-check.txt`, reproduced identically in the `F − C2` clone).
The R16-V1-red claim itself does not carry `measured_commit` (it fires on token
absence); the revision clause is exercised by `superseded-commit-mutant` and
`honest-red-green`. Do not describe the checker as proving the red claim's
revision binding; it proves the token and, via the mutants, the rule.

### S6 — C2 id assignment: resolved (low)

The C2 commit assigns mined-A `S056–S060` (terminal), `S063–S069` (idle) and
rejected `S061`, `S062`, `S070`; `measure.py a9998d1` returns 4/6 with
`rejected []`. If a later edit renumbers these, re-check `rejected[]` before
reading a 3/6 as non-separability.

### S7 — C3 not yet committed (low)

`tools/mado-tripwire.py` is absent at `3e9848a`; the selftest and real-scan
legs were not executed by this seat (transcript read is outside this item). The
fixtures are present and C3-owned; `oracle-r15.json` independently confirms the
red anchor (file `MadoR15.LibinputEvents.jsonl`, line 54, `call_38165`,
`host_mutation`). Once the tool lands, the removal test is:
`measure.py F` `c3.tool_present=true` + sha; `measure.py` on the tree with the
C3 commit reverted `false`; selftest core+compound run before and after
deleting every C1/C2 path — the fixture args are DIR-relative, so the result
must be identical; the real scan compares the same transcript digests (bound
by `session-index.json`) and the same tool bytes.

## Exact tests for the closure (post-C3)

```sh
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
B=0175f13; F=<final>; C1C=3722ba4; C2C=a9998d1; C3C=<c3>
rm -rf /tmp/mado-sep && git clone -q --no-hardlinks "$LANE" /tmp/mado-sep
cd /tmp/mado-sep
# C1-only
git checkout -q -B c1only "$B"
git checkout "$C1C" -- corpus/QUALITY.md corpus/lessons/round-16.md corpus/lessons/round-17.md \
  .ufo/waves/round-17/label-check.py .ufo/waves/round-17/label-claims.json .ufo/waves/round-17/evidence/label-check.txt
git checkout ab0bc9b -- .ufo/waves/round-17/measure.py
git add -A && git -c user.email=x@x -c user.name=x commit -qm c1only
python3 -I .ufo/waves/round-17/measure.py HEAD         # c1 15/23, c2 2/6, c3 false
# F - C2
git checkout -q -B f "$F"
git revert --no-commit "$C2C" && git -c user.email=x@x -c user.name=x commit -qm fminusC2
python3 -I .ufo/waves/round-17/measure.py HEAD         # c1 15/23, c2 2/6
# F - C1
git checkout -q -B f1 "$F"
git revert --no-commit "$C1C" && git -c user.email=x@x -c user.name=x commit -qm fminusC1
python3 -I .ufo/waves/round-17/measure.py HEAD         # c1 14/22, c2 4/6
# label check must be identical on F and F-C2
python3 -I .ufo/waves/round-17/label-check.py          # 4/7 ok, EXPECT_SUMMARY 7/7, exit 1
```

For C3: `git revert --no-commit "$C3C"` on `F` and compare
`measure.py` (`c3.tool_present` true→false), the two selftests, and the scan
verdict JSON. Expected final matrix: C1 `15/23`, C2 `4/6`, C3 present; each
leave-one-out drops only its own metric.

## Residual risk

- C3's capability remains unobserved here (tool absent). Its separability is
  structural and will be exact only after the C3 commit lands; L1 must run the
  selftest and scan once.
- `corpus/lessons/round-17.md` is shared between C1 (M1/M3/M4/M5) and the
  future C3 M2 row; removal at line level is needed for a C3-only tree, but it
  does not feed any metric.
- The C1 label check's red claim lacks `measured_commit`; the mutant pair
  covers the revision rule (S5).
- Rubric V's implemented facets exceed its short declaration; disclose in
  SCORECARD (done in the pre-measurement corrections) (S3).
- If a later commit adds a lesson-cited QUALITY criterion for C2/C3, the S1
  arithmetic applies; report C1 from `F − C3`.

No tools installed or upgraded; no host package/service/compositor command run.
