# considerthese 2026-10-25 proposal 2 — dead attempts and dirty closures, landed as a measured criterion

Seat `ScrConsiderthese`, mado round 43, wave `w1`, 2026-10-26. Writes only inside this seat directory.
Target: land proposal 2 of `considerthese/2026-10-25.md` (never edited) as a counted, re-runnable criterion.

The proposal, verbatim (`considerthese/2026-10-25.md:47`; the quoted sentence is 16 words):

> Count dead attempts and dirty closures from the watchdog digests. Two of six rounds lost attempt 1 and four of six closed with leftover files.

## 1. What was run

Two tables, one tool, both from read-only sources:

| # | command | receipt |
|---|---|---|
| T1 | `bash .ufo/waves/round-43/w1/ScrConsiderthese/check78.sh --log /home/vgpnk/Projects/shokunin/.ufo/watchdog.log --lessons corpus/lessons --from 36 --to 42 --repo . --tip-map .ufo/waves/round-43/w1/ScrConsiderthese/tips.txt` | `receipt-78-table-36-42.txt` |
| T2 | `bash .ufo/waves/round-43/w1/ScrConsiderthese/check78.sh --log /home/vgpnk/Projects/shokunin/.ufo/watchdog.log --lessons corpus/lessons --from 32 --to 37` | `receipt-78-table-32-37.txt` |
| W  | `git ls-tree -r --name-only <tip> -- .ufo/waves/round-N \| grep -cE '^\.ufo/waves/round-N/w[0-9]/.+\.md$'` per round tip (`tips.txt`) | `receipt-78-wave-column.txt` |
| C  | driver channel: where closure dirt is measured and where it is discarded | `receipt-78-channel.txt` |
| L  | the round-41 leftover instance | `receipt-78-leftovers.txt` |
| S  | the tool's selftest, shown able to fail | `receipt-78-selftest.txt` |
| Q  | every quote in this file, grepped | `receipt-78-quotes.txt` |

### 1.1 T1 — rounds 36-42 (the window this task names), run

```
$ bash .ufo/waves/round-43/w1/ScrConsiderthese/check78.sh --log /home/vgpnk/Projects/shokunin/.ufo/watchdog.log --lessons corpus/lessons --from 36 --to 42 --repo . --tip-map .ufo/waves/round-43/w1/ScrConsiderthese/tips.txt
check78 source: log=/home/vgpnk/Projects/shokunin/.ufo/watchdog.log sha256=2a917544532fe6245b6e397551042886ff2482240f2bacb8812c4fdac457dd3a
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

Read as the task asks — `round | attempts launched | closed clean` — with the honesty labels left on:

| round | attempts launched | dead attempts | closed clean (untracked files at closure) |
|---|---|---|---|
| 36 | 1 | 0 | dirty — `?? .ufo/waves/round-36/w1/reports/DistillerFindings.md` |
| 37 | 2 | 1 | clean — `No uncommitted round work; pushed. OK.` |
| 38 | 1 | 0 | dirty — `3 modified seat reports` |
| 39 | 1 | 0 | clean — `status --porcelain` empty at closure |
| 40 | 1 | 0 | dirty — one untracked `w1.ready.dispatched` |
| 41 | 1 | 0 | dirty — `**2 untracked** scratch files` |
| 42 | 1 | 0 | clean — `untracked=0`, status empty — **and zero seats spawned** (see §1.4) |

`relayed=7`: none of the seven closes on a committed witness of its own worktree state. The cleanliness cell re-derives
from spot-check prose, not from a revision. §3 says what that costs and the criterion fixes it forward.

### 1.2 T2 — the reflection's own claim, re-derived (criterion 76)

Proposal 2 states "two of six … four of six" for rounds 32-37. Re-derived from the digest and the six spot-checks, not
from the reflection:

```
$ bash .ufo/waves/round-43/w1/ScrConsiderthese/check78.sh --log /home/vgpnk/Projects/shokunin/.ufo/watchdog.log --lessons corpus/lessons --from 32 --to 37
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

dead=2 of 6 (rounds 35 and 37, both `lane-dead-no-report` in the digest), dirty=4 of 6 (32, 33, 35, 36). The
proposal's two numbers reproduce exactly — and they reproduce against the digest, which the reflection did not read: it
says of itself that its numbers are "the lane's receipts as re-checked in the non-author spot-checks"
(`considerthese/2026-10-25.md:5`), i.e. relayed. The numbers are right here; that is a re-derivation, not a relay.

Round-40 mined the same proposal and published the same shape of table (`corpus/lessons/round-40.md:150-165`). Running
T2 at 2026-10-26 reproduces its eight rows (it took 32-39; this run's 32-37 rows agree with its 32-37 rows on every
cell), so the reproduction is two-source: its table and this tool.

### 1.3 The motivating instance the proposal's window stops short of — round 41

`corpus/lessons/round-41-verifier-spotcheck.md:17` records the closure as dirty with `**2 untracked** scratch files`
(`s-grow`, `s-size`), and `corpus/lessons/round-42-verifier-spotcheck.md:24` records them `absent; tree clean` at the next
round's start. Checked at the round-42 tip: both paths `absent-at-r42-tip`, and the directory's 93 committed fixtures do
not include either name (`receipt-78-leftovers.txt`). Because both files were untracked, no commit ever carried them:
their existence is prose-only, their absence is tree-checkable. That asymmetry is exactly what a `closure-status.txt`
witness would end.

### 1.4 The instance the digest cannot see — round 42

The digest's last round-42 line is `complete mado round=42; hyaku-inline attempt=1` (`watchdog.log:1462`); the round's own
closure says the opposite about the work: `wave 1 never spawned` (`round-42-verifier-spotcheck.md:28`) and `0 seats
spawned` (`:88`). Measured on the tree at the round-42 tip `a62f2e0`:

```
round=42 tip=a62f2e0c3 wave_md=0 all_files=29 closure_status=ABSENT
```

against 37-190 markdown files under `w1/`/`w2/` at every other tip in 36-41 (`receipt-78-wave-column.txt`). So round 42
scores **1 launch, 0 dead, clean closure, and no wave** — a perfect row in the proposal's two-column table. That is the
proposal's blind spot, and the reason the criterion below carries three columns, not two.

## 2. Where the proposal is a pointer, not evidence

1. **The table is from the digest and the spot-checks; the reflection carries neither.** The reflection states its own
   numbers are relayed from spot-checks, and gives no command. Everything in §1.1/§1.2 was produced here by
   `check78.sh`, whose receipt prints the digest's sha256 (`2a917544…`) because the digest is mutable and grows after
   closure (round 43's own launch line is already in it, `watchdog.log:1496`).
2. **The digest is a partial channel, not a log of outcomes.** It carries `launch`, `complete` and
   `lane-dead-no-report` and nothing about worktrees: `grep -c 'WARN lane repo has uncommitted'
   /home/vgpnk/Projects/shokunin/.ufo/watchdog.log` prints `0`, while `grep -c uncommitted` prints `22` — every one of
   them a retry reason (`20 × "uncommitted files untrusted"`, `1 × "uncommitted, no report"`,
   `1 × "uncommitted work inherited by next attempt"`), never a path count. Round-40's own reading — "the dirty half is
   **not** in the digest - a null channel" (`corpus/lessons/round-40.md:150`) — is confirmed here, and the count-of-22
   is the trap it warns about: a bare `uncommitted` grep reads 22 hits and still measures nothing.
3. **The driver measures closure dirt and throws it away.** `scripts/hyaku/inline.sh:172` prints
   `WARN lane repo has uncommitted changes: N paths` to the operator's stdout and writes nothing; `:176` writes the
   digest's `complete` line regardless. Round-40 cited this at `inline.sh:126` — correct then; the disk-guard commit
   `5f4fa8d8` moved it to `:172` (`git show 5f4fa8d8^:scripts/hyaku/inline.sh` → `126:`). Locator drift, and the reason
   the criterion cites a line it re-checks rather than a remembered one. The repair — routing `N paths` into the digest
   — is operator-owned (fleet `scripts/`, not the lane) and is recorded here as an observation, not a claim.
4. **Round-40 already mined this proposal and declined a criterion:** "No QUALITY criterion" is added for it because no
   mistake of that round backed one (`corpus/lessons/round-40.md:165`). This landing supplies that ground: M43-6, the
   round-42 mistake (below). The criterion is not a duplicate; it is the landing round 40 deferred.
5. **Round-40's attempt-field figure does not reproduce.** It writes "round 28 carries `attempt=1` seven times"
   (`corpus/lessons/round-40.md:149`); measured now, round 28 has 9 launches, 7 dead lines, and the field on those lines
   reads `1,1,1,2,2,3,3` (`receipt-78-attempt-field.txt`). The reason to ignore the field holds; the count is corrected.
6. **`events.log` is gone.** Round-40 cited `events.log:1381`; `/home/vgpnk/Projects/shokunin/.ufo/*.log` today holds
   only `watchdog.log`, so that citation no longer resolves (`receipt-78-channel.txt`). A pointer that cannot be opened
   is not evidence.

## 3. Criterion draft — QUALITY.md 81 (hedged: the next free slot at landing)

Numbering: peer `ScrQualityCriteria` claims 77-80 for the four round-42 mistake classes, so this seat takes **81**; the L1
sets the final order, hence the hedge. Ground to be *landed*: `corpus/lessons/round-43.md#mistakes M43-6` (drafted by
`ScrLessonSkeleton` as "a driver `complete` line and a clean `git status` were read as the round having succeeded, for a
round that spawned no seat"). Until the L1 lands that line the citation dangles, which is criterion 54's rule and is
stated here rather than hidden.

> **81.** A round's closure row counts three things separately, each from a named channel: **attempts** from the driver
> digest's `launch`/`complete`/`lane-dead-no-report mado round=N` lines and never from its `attempt=` field (it repeats: round 28's
> seven dead lines carry `1,1,1,2,2,3,3`); **cleanliness** from a `receipts/closure-status.txt` committed at
> the revision the round closes on, holding the raw `GIT_OPTIONAL_LOCKS=0 git status --porcelain` output, empty or not
> (extends criterion 63 — a worktree observable re-derives only from its committed witness); and **work** from the round's
> own wave bytes at that revision, the count of `.md` files under `.ufo/waves/round-N/w[0-9]/`. A `complete` line and an
> empty `status` are driver and worktree facts, not round facts: a round whose wave count is 0 says so in its report in
> the driver's retry words whatever the digest says, and a round with no committed witness writes its cleanliness cell
> `relayed:` with the spot-check's `path:line` instead of `clean`/`dirty`. Check:
> `bash .ufo/waves/round-43/w1/ScrConsiderthese/check78.sh --log <fleet>/.ufo/watchdog.log --lessons corpus/lessons
> --from <a> --to <b> --repo . --tip-map <tips>` prints one row per round with `closure` ∈ {CLEAN, DIRTY,
> RELAYED:clean, RELAYED:dirty, ABSENT} and `source` ∈ {receipt, spotcheck}, and exits 1 while any row is `ABSENT` or a
> launch has neither a `complete` nor a `dead` line (`UNEXPLAINED`). Shown able to fail: `--selftest` prints `SELFTEST:
> PASS (12 assertions)` and rejects a launch with no outcome line, a round with no spot-check (`ABSENT`,
> `TABLE_INCOMPLETE`, exit 1), the prefix collision (`round=12` not counted into round 1), a later dirty line behind an
> earlier clean one, and a non-empty witness (`DIRTY` even where the prose says clean); at 2026-10-26 the real ranges
> print `TALLY rounds=7 launches=8 dead=1 complete=7 clean=3 dirty=4 relayed=7` and `TALLY rounds=6 launches=8 dead=2
> complete=6 clean=2 dirty=4 relayed=6`, with every row `source=spotcheck` because
> `git cat-file -e <tip>:.ufo/waves/round-N/receipts/closure-status.txt` fails at all seven tips, while round 42 reads
> `wave_md=0` beside a `complete` digest line. Ground: `considerthese/2026-10-25.md` proposal 2 (2026-10-25); extends
> criterion 63. (lesson: lessons/round-43.md#mistakes M43-6)

The re-runnable check a closure can run on itself, before it writes its report:

```sh
cd <lane> && bash .ufo/waves/round-43/w1/ScrConsiderthese/check78.sh \
  --log /home/vgpnk/Projects/shokunin/.ufo/watchdog.log --lessons corpus/lessons \
  --from <N> --to <N> --repo . --tip-map <tips-file>
# and for the round just closed, the witness itself:
GIT_OPTIONAL_LOCKS=0 git status --porcelain > .ufo/waves/round-<N>/receipts/closure-status.txt
```

### 3.1 The sentence for the round report

> Closure accounting, rounds 36-42: the driver logged 8 launches for 7 rounds and one `lane-dead-no-report` (round 37);
> 4 of 7 closures carry uncommitted round work in the spot-check's own row (36, 38, 40, 41) and 3 read clean (37, 39,
> 42) — but none of the seven closes on a committed witness, so every cleanliness cell is `relayed:` and re-derives
> from prose, and round 42's `complete` line stands beside `wave_md=0`: digest completion and a clean tree are not round
> success. Command: `check78.sh --log /home/vgpnk/Projects/shokunin/.ufo/watchdog.log --lessons corpus/lessons --from
> 36 --to 42 --repo . --tip-map .ufo/waves/round-43/w1/ScrConsiderthese/tips.txt` (`relayed=7`), plus
> `receipt-78-wave-column.txt` for the `wave_md` column.

## 4. Limits of this landing

- **Historical cleanliness stays relayed.** No round 32-42 committed a closure witness, so the criterion cannot make the
  historical column evidence; it can only stop labelling prose as measurement. The witness requirement binds future
  closes.
- **`wave_md` counts markdown, not seats.** A wave that spawns seats but lands only JSON would read a low number; the
  number is a floor on "the wave wrote something at its own path", which is what round 42 fails at 0.
- **The digest is mutable.** Every table prints its sha256; a later reader comparing bytes must compare to that hash,
  not to "the log".
- **`attempt=` is not used.** Round 28 is the counterexample that keeps the rule: 9 launches, 7 `lane-dead-no-report`
  lines carrying `1,1,1,2,2,3,3` (`receipt-78-attempt-field.txt`). Round-40 wrote this as "`attempt=1` seven times"
  (`round-40.md:149`); seven is the dead-line count, so that number is corrected here under criterion 76 — the rule
  survives, the figure does not.
- **Round-40's `events.log:1381` cannot be re-checked** (no such file today); the observation stands only as far as its
  spot-check carries it.

## 5. Receipts (this directory)

`check78.sh` (tool, `--selftest` 12 assertions), `tips.txt` (round → tip, each tip from that round's spot-check header),
`quotes.txt` + `verify-quotes.sh`, `receipt-78-table-36-42.txt`, `receipt-78-table-32-37.txt`,
`receipt-78-wave-column.txt`, `receipt-78-channel.txt`, `receipt-78-leftovers.txt`, `receipt-78-selftest.txt`,
`receipt-78-quotes.txt`, `receipt-78-watchdog-raw.txt`.
