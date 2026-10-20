# ScoutMeasureC1 — c1 counts a criterion only at column 0 as `N. ` with `lessons/` on that same line; 22/30 = 7.3333 reproduces only if every round-20 criterion line takes that shape and no other col-0 numbered line is added

Scout seat, read-only on the lane; every probe ran in `/tmp/mado-r20-ScoutMeasureC1`
(`git clone -q` of the lane, observed clone HEAD `e629f731172b8238caffe50f152217ce56535fb4`;
probe commits are local to that clone). No lane file was written; `git status --porcelain`
in the lane still shows only the untracked round-20 wave dirs, `git diff HEAD -- corpus/QUALITY.md tools/`
is empty.

## The counting rule, as the instrument implements it

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/measure.py`:

- `:92` denominator — `criteria_n = len(re.findall(r'^[0-9]+\. ', quality, re.M))`
- `:93` numerator — `lesson_cited_n = len(re.findall(r'^[0-9]+\. .*lessons/', quality, re.M))`
- `:94-99` `c1 = {criteria, lesson_cited, score: round(10*lesson_cited/criteria, 4)}` (`None` at 0 criteria)
- `:78-84` `try_source` reads `git -C <repo> show <resolved-commit>:corpus/QUALITY.md` — **committed bytes only**
- `:50` `REPO = Path(__file__).resolve().parents[3]`, so the counter measures the checkout that
  contains the script, not the cwd; a lane script copy cannot resolve a `/tmp`-clone revision
  (observed: `fatal: Needed a single revision` / `measure.py: cannot resolve revision '51a5da5'`, rc=2).
- Instrument identity observed: `sha256sum .ufo/waves/round-17/measure.py` =
  `de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc` (lane and clone copies identical).

A line counts as a criterion iff, at **byte 0 of the line**, it matches `[0-9]+\. ` — digits,
a literal period, one literal space, then text. It counts as lesson-cited iff the **same line**
contains the substring `lessons/` somewhere after that prefix. Nothing joins wrapped lines,
nothing reads the next line, nothing checks that `lessons/` is a citation (a prose mention or a
bare path segment satisfies it), indentation kills both counts, and any col-0 numbered line
anywhere in the file — list, note, fenced block — enters the denominator.

Regex probe (no commit, direct `re.match` on the module's two patterns):

| candidate line | denominator | numerator |
|---|---|---|
| `29. text (lesson: lessons/x.md)` | True | True |
| `- 29. text (lesson: lessons/x.md)` | False | False |
| `  29. text (lesson: lessons/x.md)` (2 spaces) | False | False |
| `**29.** text (lesson: lessons/x.md)` | False | False |
| `### 29. text (lesson: lessons/x.md)` | False | False |

## Base census at `e629f73` (why it is 20/28, not 23/28)

Observed c1 at the clone's base commit: `{"criteria": 28, "lesson_cited": 20, "score": 7.1429}`.
Numbered lines are exactly 1..28, each once (28 unique, no duplicates), so the denominator currently
equals the criterion count. The eight uncited numbered lines:

| line | criterion | why uncounted |
|---|---|---|
| 3, 4, 6, 7, 8 | 1–5 (admission bar) | no `lessons/` at all |
| 43 | 18 | citation sits at `:49` (4-space continuation) |
| 50 | 19 | citation at `:55` |
| 72 | 20 | citation at `:77` |

Criteria 18, 19 and 20 are the real-file proof that a wrapped citation is invisible: their
`(lesson: lessons/…)` text exists in the file, at lines 49, 55 and 77, and buys nothing.
Criteria 21–28 and 6–17 carry a same-line citation and are the 20 that count. The five
admission-bar lines 1–5 are permanently uncited, so the literal ceiling at N=30 is
`10*25/30 = 8.3333`, not 10.

## Empirical probe matrix (clone commits, `python3 -I .ufo/waves/round-17/measure.py HEAD`)

I appended a `## Round 20 — probe (dummy)` section at EOF (after the round-19 limit paragraphs) —
placement is irrelevant, only line shape matters — and moved one variable per commit:

| probe | clone commit | observed c1 |
|---|---|---|
| base, unmodified | `e629f73` | 28 / 20 / **7.1429** |
| two criteria, each `N. … (lesson: lessons/…)` on one line | `51a5da5` | 30 / 22 / **7.3333** ✅ |
| criterion 29's citation wrapped onto a 4-space continuation line | `bd9d36b` | 30 / 21 / **7.0** |
| criterion 30 indented 2 spaces | `28aea96` | 29 / 21 / **7.2414** |
| `30.A stated count …` (no space after the period) | `d48a9ae` | 29 / 21 / **7.2414** |
| stray col-0 sub-point `1. …` added to a note (criterion 30 still indented) | `7d44362` | 30 / 21 / **7.0** |
| stray `1. …` sub-point + both criteria correct | `46223de` | 31 / 22 / **7.0968** |
| criterion 29 reduced to prose `The helper walks lessons/ files …` | `78437a1` | 30 / 22 / **7.3333** |

Arithmetic confirmation: `10*22/30 = 7.33333…`, `round(…, 4) = 7.3333`. The SCORECARD
target text at `SCORECARD.md:1263-1265` ("Before 20/28 = 7.1429 → target 22/30 = 7.3333") is
exactly reachable by appending two same-line-cited criteria and changing nothing else.

Working-tree edits are invisible: with an uncommitted `31. …` line appended, `measure.py HEAD`
still printed `31/22/7.0968` from the last commit — the count moves only when the QUALITY edit
is committed. Short revisions resolve fine (`measure.py 51a5da5` → `commit 51a5da5…`,
`c1 30/22/7.3333`).

## Exact shape a round-20 criterion must take

```
## Round 20 — <axis> (outside <verifier> R19-Vn)

29. <one-sentence rule> (lesson: lessons/round-19.md#… ; outside lessons/round-19-verifier-spotcheck.md#…).
    <optional continuation lines: may hold the red-before sentence, the runnable
    command, and limits — but NEVER the first `lessons/` citation>
30. <one-sentence rule> (lesson: lessons/round-19.md#… ; outside lessons/round-19-verifier-spotcheck.md#…).
```

Hard requirements, each observed:

1. Number at byte 0. No leading spaces (7.2414), no `- `, `**`, or `### ` prefix.
2. `29` then a literal `.` then exactly one space, then text. `30.A…` does not count.
3. The `lessons/` substring must be on the numbered line itself. Continuation-line citations
   are dead (7.0); this is already the fate of criteria 18, 19, 20.
4. `lesson_cited` rises by 1 per new criterion and `criteria` by 1 per new criterion, so two
   correct criteria move 20/28 → 22/30. One correct + one wrapped gives 21/30 = 7.0, i.e. the
   claim silently misses.
5. Do not add any other col-0 `N. ` line in the round-20 QUALITY edits — a sub-bullet, an
   enumerated note or a pasted list costs 22/31 = 7.0968. Bullets (`-`, `*`) and indented
   sub-points are safe.
6. A mere mention of `lessons/` in the criterion prose counts (7.3333 at `78437a1`), so the
   counter cannot police citation honesty: the criterion must actually name the lesson for the
   claim to survive reading, even though the regex would accept `walks lessons/ files`.

## Notes for the C2 owner and for L1 verification

- The claim's REV must be the commit that lands the QUALITY text; measuring before that commit
  reports the old 20/28 no matter what the working tree says.
- The counter must run from a checkout containing that commit. In the lane this is the lane
  copy (`REPO` = lane); a `/tmp` clone's copy measures only clone revisions. For an independent
  re-derivation L1 may run the lane copy against the landed lane commit (read-only `git show`,
  no jj/git write) — that is the same instrument, same sha `de4c422b…`.
- [INFERENCE] If the round's real criteria 29/30 later get extra continuation paragraphs that
  shift line numbers, nothing breaks: `criteria`/`lesson_cited` are counts, not line lookups.
  Only the prefix shape of each numbered line matters.
- [INFERENCE] Any future criterion appended as `29.` + citation will also be counted by any other
  consumer of `^[0-9]+\. ` in QUALITY.md; I checked no other counter reads QUALITY.md in this
  round's claim (C2 alone does).

## Limits

- Probed `c1` only; I did not exercise `c2` (provinces) or `c3` (tool sha), nor the round-20
  precision counter `.ufo/waves/round-20/tw-precision.py`.
- Did not test with a QUALITY.md absent at REV (code path gives `criteria=0`, `score=None`) or
  with CRLF line endings (the `^…lessons/` patterns are line-ending agnostic; `\r` would sit
  after the citation and not affect either match — untested).
- Did not check whether the planned round-20 criteria 29/30 text is already drafted anywhere;
  my dummy text is placeholders only, the real criteria must carry their own red-before commands
  (criterion 29 isolation-harness fail-closed; criterion 30 count re-derivation).
- The probe clone `/tmp/mado-r20-ScoutMeasureC1` is left in place with the eight probe commits
  (`e629f73`, `51a5da5`, `bd9d36b`, `28aea96`, `d48a9ae`, `7d44362`, `46223de`, `78437a1`); its
  git identity was passed per-command (`-c user.name=probe`), no global config touched.

## Installs

none
