# considerthese proposal-2 closure table — w2 falsification run

Seat `ScribeClosureTable`, mado round 43, wave `w2`, 2026-10-26. Attacks **QUALITY criterion 81** (its numbers) and
the sentence of `w1/ScrConsiderthese/proposal.md` §3.1, by running the two commands they name against the current
digest. Everything below is a command and its output; nothing is copied from the w1 receipts except where a diff
against them is shown.

Tool under test: `.ufo/waves/round-43/w1/ScrConsiderthese/check78.sh`, worktree-clean against the lane tip
`2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa` (`git diff --stat <tip> -- <path>` prints nothing); the other input,
`tips.txt`, resolves all seven tips (`git cat-file -t` → `commit` ×7).

Criterion 81 was read at the data commit the task names:

```
$ git show 1959770657f1f8665097c1aed4be6c1cbb07139f:corpus/QUALITY.md   # line 409, criterion 81
```

Its text is byte-identical at the lane tip (`awk '/^81\. /{print;exit}'` piped to `sha256sum` → `9f771160…` at both
revisions), so a defect found in it is a defect of the landed data, not of one revision.

---

## 1. Runs

### 1.1 Selftest (criterion 81's "Shown able to fail")

```
$ bash .ufo/waves/round-43/w1/ScrConsiderthese/check78.sh --selftest
check78 source: log=/tmp/check78.mf4OPP/wd.log sha256=fa45966a12bf590b96654757f5ed0ff3324cb3ccdd71334c43cde95323a71f76
round	launches	dead	complete	closure	source	cite
1	1	0	1	CLEAN	receipt	/tmp/check78.mf4OPP/receipts/round-1/closure-status.txt:0-nonblank
2	2	1	1	RELAYED:dirty	spotcheck	/tmp/check78.mf4OPP/round-2-verifier-spotcheck.md:1
3	1	0	1	ABSENT	spotcheck	/tmp/check78.mf4OPP/round-3-verifier-spotcheck.md
4	1	0	1	DIRTY	receipt	/tmp/check78.mf4OPP/receipts/round-4/closure-status.txt:1-nonblank
5	1	0	1	RELAYED:dirty	spotcheck	/tmp/check78.mf4OPP/round-5-verifier-spotcheck.md:2
TALLY rounds=5 launches=6 dead=1 complete=5 clean=1 dirty=3 relayed=2 unknown=1
VERDICT: TABLE_INCOMPLETE
TALLY rounds=5 launches=6 dead=1 complete=5 clean=2 dirty=3 relayed=3 unknown=0
VERDICT: TABLE_COMPLETE
SELFTEST: PASS (12 assertions)
exit=0
```

(`receipt-selftest.txt`.)

### 1.2 The command criterion 81 names, rounds 36-42, with `tips.txt`

```
$ bash .ufo/waves/round-43/w1/ScrConsiderthese/check78.sh --log /home/vgpnk/Projects/shokunin/.ufo/watchdog.log \
    --lessons corpus/lessons --from 36 --to 42 --repo . \
    --tip-map .ufo/waves/round-43/w1/ScrConsiderthese/tips.txt
check78 source: log=/home/vgpnk/Projects/shokunin/.ufo/watchdog.log sha256=4ae5c0621c286374cfc39f208ae2a03bbe0752e735008ab2c0c73fba6553a87b
round	launches	dead	complete	closure	source	cite
36	1	0	1	RELAYED:dirty	spotcheck	corpus/lessons/round-36-verifier-spotcheck.md:21
37	2	1	1	RELAYED:clean	spotcheck	corpus/lessons/round-37-verifier-spotcheck.md:20
38	1	0	1	RELAYED:dirty	spotcheck	corpus/lessons/round-38-verifier-spotcheck.md:17
39	1	0	1	RELAYED:clean	spotcheck	corpus/lessons/round-39-verifier-spotcheck.md:16
40	1	0	1	RELAYED:dirty	spotcheck	corpus/lessons/round-40-verifier-spotcheck.md:15
41	1	0	1	RELAYED:dirty	spotcheck	corpus/lessons/round-41-verifier-spotcheck.md:17
42	1	0	1	RELAYED:clean	spotcheck	corpus/lessons/round-42-verifier-spotcheck.md:21
TALLY rounds=7 launches=8 dead=1 complete=7 clean=3 dirty=4 relayed=7 unknown=0
VERDICT: TABLE_COMPLETE
exit=0
```

(`receipt-t1-36-42.txt`.) The digest grew while the seat ran, so the same command was re-run at the report-time bytes:

```
$ ...same command...
check78 source: log=/home/vgpnk/Projects/shokunin/.ufo/watchdog.log sha256=69ec6152e9bf19bc6b238858767793f0f5bd5cb3806bd18c08752a28a38524e3
...seven rows byte-identical...
TALLY rounds=7 launches=8 dead=1 complete=7 clean=3 dirty=4 relayed=7 unknown=0
VERDICT: TABLE_COMPLETE
exit=0
```

(`receipt-t1b-36-42.txt`.) Compare with the w1 receipt at the w1 log bytes `2a917544…`:

```
$ diff .ufo/waves/round-43/w1/ScrConsiderthese/receipt-78-table-36-42.txt \
       .ufo/waves/round-43/w2/ScribeClosureTable/receipt-t1-36-42.txt
2c2
< check78 source: log=... sha256=2a917544532fe6245b6e397551042886ff2482240f2bacb8812c4fdac457dd3a
---
> check78 source: log=... sha256=4ae5c0621c286374cfc39f208ae2a03bbe0752e735008ab2c0c73fba6553a87b
```

One line differs, and it is the digest hash the tool prints on purpose. Three log states
(`2a917544`, `4ae5c062`, `69ec6152`) give one table.

### 1.3 Criterion 81's second range (32-37) — needed to check its second tally

```
$ bash .ufo/waves/round-43/w1/ScrConsiderthese/check78.sh --log /home/vgpnk/Projects/shokunin/.ufo/watchdog.log \
    --lessons corpus/lessons --from 32 --to 37
round	launches	dead	complete	closure	source	cite
32	1	0	1	RELAYED:dirty	spotcheck	corpus/lessons/round-32-verifier-spotcheck.md:18
33	1	0	1	RELAYED:dirty	spotcheck	corpus/lessons/round-33-verifier-spotcheck.md:19
34	1	0	1	RELAYED:clean	spotcheck	corpus/lessons/round-34-verifier-spotcheck.md:41
35	2	1	1	RELAYED:dirty	spotcheck	corpus/lessons/round-35-verifier-spotcheck.md:46
36	1	0	1	RELAYED:dirty	spotcheck	corpus/lessons/round-36-verifier-spotcheck.md:21
37	2	1	1	RELAYED:clean	spotcheck	corpus/lessons/round-37-verifier-spotcheck.md:20
TALLY rounds=6 launches=8 dead=2 complete=6 clean=2 dirty=4 relayed=6 unknown=0
VERDICT: TABLE_COMPLETE
exit=0
```

(`receipt-t2-32-37.txt`.)

---

## 2. Every number in criterion 81, against the output

| # | criterion 81 says | command | observed | verdict |
|---|---|---|---|---|
| 1 | `SELFTEST: PASS (12 assertions)` printed by `--selftest` | `check78.sh --selftest` | `SELFTEST: PASS (12 assertions)`, `exit=0` | MATCH |
| 2 | `TALLY rounds=7 launches=8 dead=1 complete=7 clean=3 dirty=4 relayed=7` | T1 (§1.2) | identical (two log hashes) | MATCH |
| 3 | `TALLY rounds=6 launches=8 dead=2 complete=6 clean=2 dirty=4 relayed=6` | T2 (§1.3) | identical | MATCH |
| 4 | round 28's seven dead lines carry `1,1,1,2,2,3,3` | `grep -c "lane-dead-no-report mado round=28;"` → `7`; `... \| grep -oE 'attempt=[0-9]+' \| sort \| uniq -c` → `3 attempt=1 / 2 attempt=2 / 2 attempt=3` | dead=7; multiset 1,1,1,2,2,3,3 | MATCH |
| 5 | `git cat-file -e <tip>:...closure-status.txt` fails at all seven tips | loop over `tips.txt`, 7 tips | `ABSENT` ×7 | MATCH |
| 6 | round 42 reads `wave_md=0` beside a `complete` digest line | `git ls-tree ... a62f2e0 ... \| grep -cE '^\.ufo/waves/round-42/w[0-9]/.+\.md$'` → `0`; `grep -nE 'complete mado round=42;'` → `1462` | `wave_md=0`, `all_files=29`; `watchdog.log:1462: … complete mado round=42; hyaku-inline attempt=1` | MATCH |
| 7 | `closure` ∈ {CLEAN, DIRTY, RELAYED:clean, RELAYED:dirty, ABSENT} | T1/T2 + selftest | all five values observed across the three runs | MATCH |
| 8 | `source` ∈ {receipt, spotcheck} | T1/T2 + selftest | `spotcheck` ×7 in T1, `spotcheck` ×6 in T2, `receipt` in selftest rounds 1 and 4 | MATCH |
| 9 | exits 1 while a row is `ABSENT` | `--selftest` (round 3 absent) | first pass `TABLE_INCOMPLETE`, asserted `rc -eq 1` | MATCH |
| 10 | exits 1 while a launch has neither `complete` nor `dead` (`UNEXPLAINED`) | `--from 43 --to 43` on the real digest | `  UNEXPLAINED round=43 launches=1 != complete+dead=0`, `TABLE_INCOMPLETE`, `exit=1` | **mechanism MATCH, but not shown by `--selftest`** — see F2 |
| 11 | "Check:" names a command that prints the three counted things (attempts, cleanliness, **work**) | T1 header `round\tlaunches\tdead\tcomplete\tclosure\tsource\tcite`; `grep -nE 'wave\|ls-tree' check78.sh` finds no wave count | no `wave`/`wave_md` column is printed; no `ls-tree` call in the tool | **MISMATCH** — see F1 |
| 12 | extends criterion 63 | `git show <data>:corpus/QUALITY.md \| grep -nE '^63\.'` | `373:63. A receipt observable read from the working tree …` | MATCH |
| 13 | ground `lessons/round-43.md#mistakes M43-6` | `git show <data>:corpus/lessons/round-43.md \| grep -n 'M43-6'` | `161:**M43-6 — a driver \`complete\` line and a clean \`git status\` …` | MATCH |

The `1.1`-style row constants behind #2: 36-42 launches 1+2+1+1+1+1+1 = 8, dead 1 (round 37), complete 7 — no round in
36-42 has `launches != complete+dead`, so no `UNEXPLAINED` line and `TABLE_COMPLETE` is correct.

The seven `cite` cells also carry the words that decide them (re-read, not trusted): `:21` "**partial** — … `?? …DistillerFindings.md`",
`:20` "untracked=0`; `git status --porcelain` empty", `:17` "DEFECT — … 3 modified seat reports", `:16` "`tracked=0 untracked=0`",
`:15` "one untracked … defect, status-neutral", `:17` "**2 untracked** scratch files", `:21` "untracked=0`; … empty".

Wave column, recomputed for all seven tips with the receipt's own command
(`git ls-tree -r --name-only <tip> -- .ufo/waves/round-N | grep -cE '^\.ufo/waves/round-N/w[0-9]/.+\.md$'`):

```
round=36 tip=a5aaa09ad wave_md=114 all_files=381
round=37 tip=654224826 wave_md=190 all_files=550
round=38 tip=f9057de60 wave_md=37  all_files=87
round=39 tip=b6078c3ed wave_md=73  all_files=337
round=40 tip=fb4962107 wave_md=96  all_files=425
round=41 tip=b20155b10 wave_md=136 all_files=1252
round=42 tip=a62f2e0c3 wave_md=0   all_files=29
```

Row-for-row identical to `.ufo/waves/round-43/w1/ScrConsiderthese/receipt-78-wave-column.txt`
(`receipt-wave-column.txt`). The proposal's "37-190 markdown files … at every other tip in 36-41" holds (min 37,
max 190). Round 42's zero is prose-backed too: `corpus/lessons/round-42-verifier-spotcheck.md:28` "wave 1 never" and
`:88` "0 seats spawned".

## 3. Every number in proposal.md §3.1, against the output

| §3.1 says | observed | verdict |
|---|---|---|
| "8 launches for 7 rounds" | TALLY `rounds=7 launches=8` | MATCH |
| "one `lane-dead-no-report` (round 37)" | TALLY `dead=1`; row 37 `dead=1` | MATCH |
| "4 of 7 closures carry uncommitted round work … (36, 38, 40, 41)" | `dirty=4`; rows 36, 38, 40, 41 `RELAYED:dirty` | MATCH |
| "3 read clean (37, 39, 42)" | `clean=3`; rows 37, 39, 42 `RELAYED:clean` | MATCH |
| "none of the seven closes on a committed witness, so every cleanliness cell is `relayed:`" | `relayed=7`, `source=spotcheck` ×7, closure-status ABSENT ×7 | MATCH |
| "round 42's `complete` line stands beside `wave_md=0`" | `watchdog.log:1462`, `wave_md=0` | MATCH |
| "(`relayed=7`)" | TALLY `relayed=7` | MATCH |
| "plus `receipt-78-wave-column.txt` for the `wave_md` column" | file exists; recomputed rows identical | MATCH |

**§3.1 is fully supported by the run as written.** No number in it needs a correction.

---

## 4. Findings (defects in the landed criterion, not in its numbers)

**F1 — the named Check cannot check the third of the three things the criterion mandates.** Criterion 81 requires
`work` to be "the count of `.md` files under `.ufo/waves/round-N/w[0-9]/`", but its `Check:` names one command,
`check78.sh`, whose header is `round  launches  dead  complete  closure  source  cite` — no wave column — and which
contains no `ls-tree` call (`grep -nE 'wave|ls-tree' check78.sh` matches only the docstring and fixture rows). A reader
running the criterion's own command therefore sees two of the three counts. The number `wave_md=0` the criterion quotes
for round 42 comes from the *separate* W command of `proposal.md` §1 (`git ls-tree …`), which §3.1 names and criterion 81
does not. Under criterion 10 ("Publish each pinned value with a re-derivation command") the `work` cell has no command in
the criterion.

**F2 — `--selftest` does not show the `UNEXPLAINED` rejection it is credited with.** Criterion 81's "Shown able to fail"
list credits `--selftest` with rejecting "a launch with no outcome line". The selftest fixture has five in-range rounds
and every one satisfies `launches == complete + dead`
(`sed -n '/^selftest() {/,/^}/p' check78.sh | grep -E 'mado round=[0-9]+' | grep -oE '(launch|complete|lane-dead-no-report) mado round=[0-9]+' | sort | uniq -c`:
r1 1/1/0, r2 2/1/1, r3 1/1/0, r4 1/1/0, r5 1/1/0; the round-12 launch is out of the 1..5 range and exists only for the
prefix-collision assertion), so the `UNEXPLAINED` branch is never entered. The branch is real and fires on the live digest
(#10 above, round 43, `exit=1`), and the selftest does assert `exit 1` — but on the `ABSENT` row, not on a launch without
an outcome. The other five credited rejections do hold in the fixture (no spot-check → `ABSENT`/`TABLE_INCOMPLETE`/exit 1;
prefix collision; later dirty line behind an earlier clean one; non-empty witness → `DIRTY`).

**F3 — the tool's own comment repeats the figure the criterion corrected.** `check78.sh:17-18` says "round 28 carries
attempt=1 seven times, corpus/lessons/round-40.md:150". Measured: `grep 'mado round=28' watchdog.log | grep -c 'attempt=1'`
→ `8`; the seven *dead* lines carry `attempt=1` three times; and the sentence it cites sits at
`corpus/lessons/round-40.md:148-149` (`:150` is "the known round-31"). The criterion's text carries the corrected multiset,
so the criterion is right and the frozen tool's comment is wrong in both the number and the locator.

**Observation (not a defect).** The `12` in the selftest label counts distinct assertions: 13 `ok=0` guards exist, two of
them (`tally4`, `tally`) repeat the same TALLY grep. The printed string is what criterion 81 quotes, verbatim.

---

## 5. Corrected sentences (drafted, for the L1; nothing else in criterion 81 changes)

Replacement for the `Check:`/`Shown able to fail:` tail of criterion 81 (numbers untouched — every one reproduced):

> Check: `bash .ufo/waves/round-43/w1/ScrConsiderthese/check78.sh --log <fleet>/.ufo/watchdog.log --lessons corpus/lessons
> --from <a> --to <b> --repo . --tip-map <tips>` prints one row per round with `closure` ∈ {CLEAN, DIRTY,
> RELAYED:clean, RELAYED:dirty, ABSENT} and `source` ∈ {receipt, spotcheck}, and exits 1 while any row is `ABSENT` or a
> launch has neither a `complete` nor a `dead` line (`UNEXPLAINED`); it does **not** print the `work` count, which is
> re-derived separately as `git ls-tree -r --name-only <tip> -- .ufo/waves/round-N | grep -cE
> '^\.ufo/waves/round-N/w[0-9]/.+\.md$'` per round tip. Shown able to fail: `--selftest` prints `SELFTEST: PASS
> (12 assertions)` and rejects a round with no spot-check (`ABSENT`, `TABLE_INCOMPLETE`, exit 1), the prefix collision
> (`round=12` not counted into round 1), a later dirty line behind an earlier clean one, and a non-empty witness
> (`DIRTY` even where the prose says clean); the `UNEXPLAINED` branch is shown separately on a live digest, where
> `--from 43 --to 43` prints `UNEXPLAINED round=43 launches=1 != complete+dead=0` and exits 1; at 2026-10-26 the real
> ranges print `TALLY rounds=7 launches=8 dead=1 complete=7 clean=3 dirty=4 relayed=7` and `TALLY rounds=6 launches=8
> dead=2 complete=6 clean=2 dirty=4 relayed=6`, with every row `source=spotcheck` because `git cat-file -e
> <tip>:.ufo/waves/round-N/receipts/closure-status.txt` fails at all seven tips, while round 42 reads `wave_md=0` beside
> a `complete` digest line.

And the tool's comment (`check78.sh:17-18`) should read: "round 28's seven dead lines carry `attempt=`
`1,1,1,2,2,3,3`; over all 17 round-28 lines the field reads 1×8, 2×5, 3×4 (`corpus/lessons/round-40.md:148-149`)". That
edit is the L1's, not this seat's — the tool is frozen.

---

## 6. Limits

- Numbers are checked against the digest's bytes as of the hash printed in each receipt; the digest grew twice during
  this seat (`2a917544` → `4ae5c062` → `69ec6152`) and the two tallies did not move, which is the criterion's own
  "the digest is mutable" limit exercised, not contradicted.
- `work` is a markdown count, not a seat count (criterion 81 says so); no attempt was made to map seats to files.
- The classification of each spot-check row is checked only by re-reading the cited line's own words; the tool's token
  rules were not adversarially re-tested beyond the selftest's five fixture cases.
- F1 and F2 are read from the tool's source and selftest fixture; no attempt was made to edit the frozen tool to prove
  what a patched version would do.
