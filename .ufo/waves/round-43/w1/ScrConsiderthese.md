# ScrConsiderthese — considerthese 2026-10-25 proposal 2, landed as a measured criterion

Seat of mado round 43, wave `w1`, 2026-10-26. Leaf seat: no subagent dispatch, no background job, no host mutation.
Deliverable: `.ufo/waves/round-43/w1/ScrConsiderthese/proposal.md` (criterion draft + commands + run output + the
pointer/evidence statement). This report is the scoped findings index.

## Behavior

Proposal 2 of `considerthese/2026-10-25.md:47` ("Count dead attempts and dirty closures from the watchdog digests. Two of
six rounds lost attempt 1 and four of six closed with leftover files.", 16 words) is landed as a counted table over two
read-only sources plus a third column the proposal does not name, and as a QUALITY.md criterion draft with a re-runnable
check.

Tool: `.ufo/waves/round-43/w1/ScrConsiderthese/check78.sh` (new, 11.4 KB). It counts, per round, `launches` /
`dead` / `complete` from the fleet digest's `launch|complete|lane-dead-no-report mado round=N` lines, classifies closure
cleanliness from a committed `receipts/closure-status.txt` witness when one exists at the round's tip and otherwise from
the round's spot-check line, marking the cell `RELAYED:`; it prints the digest's sha256 in its header.

## Gates (all run here, output committed in the seat dir)

| gate | command | result |
|---|---|---|
| tool selftest, shown able to fail | `check78.sh --selftest` | `SELFTEST: PASS (12 assertions)`, exit 0 (`receipt-78-selftest.txt`) |
| table 36-42 | `check78.sh --log …/.ufo/watchdog.log --lessons corpus/lessons --from 36 --to 42 --repo . --tip-map …/tips.txt` | `TALLY rounds=7 launches=8 dead=1 complete=7 clean=3 dirty=4 relayed=7 unknown=0` / `TABLE_COMPLETE`, exit 0 |
| table 32-37 (the reflection's own window) | `check78.sh … --from 32 --to 37` | `TALLY rounds=6 launches=8 dead=2 complete=6 clean=2 dirty=4 relayed=6 unknown=0` / `TABLE_COMPLETE`, exit 0 |
| wave column | `git ls-tree -r --name-only <tip> -- .ufo/waves/round-N \| grep -cE '…/w[0-9]/.+\.md$'` per tip | 36-41 → 114/190/37/73/96/136; **42 → 0** |
| quote verification | `verify-quotes.sh` | `QUOTES checked=13 failed=0` / `QUOTES_OK` |

The proposal's own numbers reproduce: rounds 32-37, 2 of 6 dead (35, 37) and 4 of 6 dirty (32, 33, 35, 36). Round-40's
table for 32-39 reproduces on the overlapping rows.

## Findings

1. **The digest cannot see the failure the proposal is about.** Round 42's only digest line is
   `complete mado round=42; hyaku-inline attempt=1` (`/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1462`), while its
   wave never spawned (`corpus/lessons/round-42-verifier-spotcheck.md:28`, `:88` "0 seats spawned") and the tree at
   `a62f2e0` holds 29 files under `.ufo/waves/round-42` with **0** markdown files under `w[0-9]/` (36-41: 37-190). In
   the proposal's two-column table round 42 is a perfect round: 1 launch, clean closure. Attacks
   `considerthese/2026-10-25.md:47`; supports the third column of the criterion.
2. **The dirty column is a null channel, not a zero.** `scripts/hyaku/inline.sh:172` computes the path count and prints
   `WARN lane repo has uncommitted changes: N paths` to stdout; `:176` writes the digest's `complete` line regardless.
   `grep -c 'WARN lane repo has uncommitted' .ufo/watchdog.log` → `0`, while `grep -c uncommitted` → `22`, all of them
   retry reasons (`20 × "uncommitted files untrusted"`, `1 × "uncommitted, no report"`, `1 × "uncommitted work inherited
   by next attempt"`). Confirms `corpus/lessons/round-40.md:149` ("the dirty half is **not** in the digest - a null
   channel"). Routing that count into the digest is an operator-owned edit in the fleet `scripts/`, not made here.
3. **Locator drift, round-40 → now.** Round-40 cited the same discard at `inline.sh:126`; that was correct before the
   disk-guard commit `5f4fa8d8` (`git show 5f4fa8d8^:scripts/hyaku/inline.sh` → `126:`), and it is `:172` today. Attacks
   `corpus/lessons/round-40.md:150` as a citation a later reader cannot open at the named line.
4. **Round-40's attempt-field figure does not reproduce.** It writes that round 28 carries `attempt=1` seven times
   (`round-40.md:149`). Measured now: 9 launches, 7 `lane-dead-no-report` lines, `attempt=` on those lines `1,1,1,2,2,3,3`
   (over all 17 round-28 lines: 1×8, 2×5, 3×4). Seven is the dead-line count. The rule (never count `attempt=`) holds;
   the number is corrected under criterion 76 (`receipt-78-attempt-field.txt`).
5. **`events.log:1381` no longer resolves.** `ls /home/vgpnk/Projects/shokunin/.ufo/*.log` → `watchdog.log` only, so
   round-40's second citation for the same null channel is a dead pointer today.
6. **Round-41's leftovers are prose-only by construction.** `round-41-verifier-spotcheck.md:17` names
   `**2 untracked** scratch files`; at the round-42 tip both paths are `absent-at-r42-tip` and neither name is among the
   93 committed fixtures of that directory; `round-42-verifier-spotcheck.md:24` records them `absent; tree clean`.
   Existence is not re-derivable — nothing committed ever carried them. Supports the witness requirement.
7. **Round-40 declined this criterion and round 43 supplies the ground.** `round-40.md:165` "No QUALITY criterion" was
   added because no mistake of that round backed one; `M43-6` (drafted by `ScrLessonSkeleton`, confirmed to this seat by
   message) is now that mistake, so the criterion is the deferred landing, not a duplicate.
8. **Numbering.** QUALITY.md tops at 76 (`grep -cE '^[0-9]+\. ' corpus/QUALITY.md` → 76, 399 lines). Peer
   `ScrQualityCriteria` claims 77-80 for the round-42 mistake classes (told to this seat directly); this seat's draft is
   **81**, hedged "the next free slot at landing", and its report to the L1 asks for the final order.

## Criterion draft (text: `proposal.md` §3; not written to QUALITY.md — the L1 integrates)

> 81. A round's closure row counts attempts, cleanliness and work separately, each from a named channel … a `complete`
> line and an empty `status` are driver and worktree facts, not round facts … a round with no committed witness writes
> its cleanliness cell `relayed:` … Check: `bash .ufo/waves/round-43/w1/ScrConsiderthese/check78.sh --log … --from <a>
> --to <b> --repo . --tip-map <tips>` … Ground: `considerthese/2026-10-25.md` proposal 2; extends criterion 63.
> (lesson: `lessons/round-43.md#mistakes M43-6`)

The citation to `corpus/lessons/round-43.md#mistakes M43-6` **dangles until the L1 lands that lesson line**; the draft
says so in the proposal rather than hiding it (criterion 54's rule). Sentence for the round report: `proposal.md` §3.1.

## Where the proposal is a pointer, not evidence

The table above is from the watchdog digest and the lane's spot-check prose, never from the reflection: the reflection
states its own numbers are relayed from spot-checks and carries no command. All seven cleanliness cells for rounds 36-42
are `RELAYED:` (`relayed=7`) because no round in that range committed a witness of its closure worktree state, so each is
today re-derivable only from prose; and the digest's `complete` line is a driver fact contradicted by round 42's wave
count.

## Touched surfaces

Created (all new, inside the seat's own directory): `.ufo/waves/round-43/w1/ScrConsiderthese/` = `check78.sh`,
`verify-quotes.sh`, `quotes.txt`, `tips.txt`, `proposal.md`, `receipt-78-{table-36-42,table-32-37,wave-column,channel,
leftovers,selftest,quotes,attempt-field,watchdog-raw}.txt`; and this report `.ufo/waves/round-43/w1/ScrConsiderthese.md`.
No tracked file was edited; no counter, control, registration, reference or fetch receipt was touched; the lane's
git/jj index was not written (`GIT_OPTIONAL_LOCKS=0` for the one `status` read; `M LOG.md` in the worktree is another
seat's edit, not this one's). Read-only external reads: fleet `.ufo/watchdog.log`, `scripts/hyaku/inline.sh` (working
tree and `5f4fa8d8^`), `git log/show/ls-tree/cat-file` in the lane and the fleet. No compositor verb, no pacman, no
network. Tools installed: none. Scratch `/fast/scratch/hyaku/mado-r43/ScrConsiderthese/` deleted at exit.

## Out of scope (deliberately not done)

- No edit to `corpus/QUALITY.md` (only the L1 integrates) and none to `corpus/lessons/round-43*.md`.
- No repair of the driver's discarded dirt line (fleet `scripts/`, operator-owned); recorded as an observation only.
- No count for rounds 1-31 or 43 (43 has no closure yet) and no claim about the reflection's other proposals.

## Artifact hashes (sha256, 2026-10-26)

`check78.sh 2906c095…`, `verify-quotes.sh 79aea1a4…`, `proposal.md e243744f…`, `receipt-78-table-36-42.txt d4923def…`,
`receipt-78-table-32-37.txt a877e918…`, `receipt-78-wave-column.txt fddcbc62…`, `receipt-78-channel.txt c0b306a8…`,
`receipt-78-leftovers.txt 98a2d698…`, `receipt-78-selftest.txt d05d00f9…`, `receipt-78-quotes.txt 70717607…`,
`receipt-78-attempt-field.txt e43254c0…`, `receipt-78-watchdog-raw.txt fafa213c…`, `tips.txt f96ff58f…`,
`quotes.txt 11697300…`.
