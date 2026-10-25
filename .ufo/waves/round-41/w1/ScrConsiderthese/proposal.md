# considerthese mining — `considerthese/2026-10-25.md` proposal 5

Seat `ScrConsiderthese`, mado round 41, wave w1. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Freeze `60c3914154333180450d5da27ba222d5763cc56a`, base `ab2bfaab661c846d1de9d58c01651cd156a13949`.
This file is a draft for the L1: a leaf may not edit `corpus/QUALITY.md` or the lesson.

## Chosen proposal

**Proposal 5 of `considerthese/2026-10-25.md` — "Verify one fact first-hand per day, read-only"**
(`considerthese/2026-10-25.md:50`). Its own words: "everything else is relayed from spot-checks" and
"I could pick one cited source line each day and re-open it."

It is still unimplemented at the freeze: `corpus/QUALITY.md` at base holds 68 numbered criteria and the only
one that mentions a `considerthese` file is 60 (`git show ab2bfaa…:corpus/QUALITY.md | grep -n considerthese`
-> `367:`), which grounds on `2026-10-24.md` proposal 1 (the domain-versus-meta ratio); `grep -ni 'relay\|first-hand\|first hand'`
over the same file is empty; `SKILL.md` at base has zero `considerthese` lines; `PROVINCE.md` zero. The
closest existing trace is one prose sentence about the *earlier* file —
`corpus/lessons/round-33.md:28`, "proposal 5 (verify one cited fact first-hand) was" — which recorded a mining,
not a rule. `quality/check-evidence-pointers.py` lists `considerthese/` only as a resolvable path prefix
(`:49`), it never checks a reflection's numbers.

## Why this one — the other five proposals at the freeze

| # | Proposal (2026-10-25) | Status at base `ab2bfaa` | Evidence |
|---|---|---|---|
| 1 | ratio as a running number | **already a criterion** — re-mining would duplicate: "Every round report states the lane's last-30-commit domain-versus-meta ratio with its command" | `corpus/QUALITY.md:367` (criterion 60, ground `2026-10-24.md` proposal 1, the same suggestion) |
| 2 | dead attempts / dirty closures from the watchdog | mined in round 40 as a table: "Count dead attempts and dirty closures from the watchdog digests" | `corpus/lessons/round-40.md:146` |
| 3 | watch M37-5 by name | served in round 39: "(watch M37-5 by name) is served by C1's re-registration" | `corpus/lessons/round-39.md:82`; round 38's C1 is the "v3 re-grounding counter discriminating the round-37 v2 cribs" (`corpus/lessons/round-38.md:4`) |
| 4 | put `mado-eventq.py` on a schedule; note what enabling logs would cost | open, but **not lane-actionable** | no trace in `corpus/lessons/round-3{7,8,9}.md`, `round-40.md`, `QUALITY.md`, `SKILL.md` (`grep -ni 'enabling logs\|log volume\|cost of enabling'` empty); its two halves are an operator ask (a timer) and a host config change (`debug:disable_logs = 0`), both outside this lane's write scope and this wave's host-safety rules |
| 5 | verify one fact first-hand per day, read-only | **open** — this draft | above |
| 6 | shorten the reflection's window to what is new | self-applied in the same file and operator-owned | the file already leads with "What landed after the last reflection" and pins its window to `57a772b..f6e3247`; `considerthese/` is operator-authored, never lane-edited |

Proposal 5 is the only open item that is both lane-actionable and checkable by a command. It also has teeth
already: re-deriving the mined sentence finds one number wrong (below).

## Evidence — re-derivation, not relay

Receipt: `.ufo/waves/round-41/w1/ScrConsiderthese/receipts.txt` (every command and its observed output,
`rc=0` each). `considerthese/2026-10-25.md:3` pins the window at 68 commits and `:5` states, in one sentence,
four numbers for rounds 32-37: "In this window `corpus/knowledge/` gained eight entries".

| reflection says | command | observed | verdict |
|---|---|---|---|
| "68 commits after `57a772b`" | `git log --oneline 57a772b..f6e3247 \| wc -l` | `68` | reproduces |
| SOURCES "185 to 207 rows" | `git show 57a772b:corpus/SOURCES.md \| grep -c '^\| S[0-9]'`; same at `f6e3247` | `185`; `207` | reproduces |
| 22 rows added (S186-S217) | `git diff 57a772b..f6e3247 -- corpus/SOURCES.md \| grep -c '^+\| S[0-9]'` | `22` (ids S186-S189, S196, S201-S217; the range spans 32 ids, the count is 22) | reproduces |
| "one new runnable tool" | `git log --diff-filter=A --format= --name-only 57a772b..f6e3247 -- tools/` | `tools/mado-eventq.py` (1) | reproduces |
| `corpus/knowledge/` "gained eight entries" | `git ls-tree -r --name-only 57a772b corpus/knowledge \| wc -l` -> `43`; same at `f6e3247` -> `52`; `git diff -M --name-status 57a772b..f6e3247 -- corpus/knowledge \| grep -c '^A'` -> `9`, `grep -c '^D'` -> `0` | **9 added, not 8** | **fails** |

The nine, by round: round 32 `f591087` 3 (`dispatcher-semantics-r25.md`,
`dispatcher-surface-and-request-grammar-r26.md`, `ipc-contract-r25.md`); round 34 `fa7ba11` 1
(`waybar-module-text-route-r25.md`); round 35 `02088b4` 3 (`idle-lock-never-asked-r12.md`,
`idle-lock-chain-armed-r14.md`, `idle-lock-offered-in-the-bar-r15.md`); round 37 `3f42425` 2
(`event-delivery-limits-r26.md`, `event-queue-observability-r37.md`). No renames (`-M` changes nothing) and no
deletions, so the file count is the entry count. The reflection repeats the wrong number in its carried-items
table ("8 knowledge entries").

The contrast is the point of the proposal: the one fact the reflection says it read first-hand (the SOURCES row
count) reproduces exactly; the number in the same sentence that it relayed from spot-checks does not. A mining
note that repeats the sentence would commit a number-drift of the class round 33 already recorded
(`corpus/lessons/round-33.md`, `class: number-drift`: the round-32 report narrated 187 MB for a scratch tree the
closure measured at 11.6 MB).

## Exact text to land

### A. `corpus/QUALITY.md` — append as criterion 69 (after 68)

> 69. A round that mines a proposal from `considerthese/<date>.md` re-derives, from the lane's own bytes, every
> number its mining note repeats, and the note carries the command and its output beside each re-derived number;
> a number taken on trust is written `relayed:` with the spot-check path that carries it, because the reflection
> is a pointer, not evidence. Check: run the note's commands at the reflection's own base and tip pins; a count
> the command does not print is corrected in the note or marked `relayed:`. Shown able to fail:
> `considerthese/2026-10-25.md:5` reports that `corpus/knowledge/` "gained eight entries" over rounds 32-37, while
> `git ls-tree -r --name-only 57a772b corpus/knowledge | wc -l` prints `43` and the same command at `f6e3247`
> prints `52` - nine files added (round 32: 3, round 34: 1, round 35: 3, round 37: 2), zero deleted. Ground:
> `considerthese/2026-10-25.md` proposal 5 (2026-10-25); the relayed-number class is
> `lessons/round-33.md#mistakes` (number-drift). (lesson: lessons/round-41.md#mistakes M41-n)

`M41-n` is the L1's numbering; substitute the round-41 mistake id it assigns.

### B. `corpus/lessons/round-41.md` — `## considerthese` section

> `considerthese/2026-10-25.md` proposal 5 ("Verify one fact first-hand per day, read-only", restating
> `2026-10-24.md` proposal 5, mined in round 33 as prose) is mined as QUALITY 69. The reflection's mined
> sentence re-derives: 68 commits `57a772b..f6e3247`; SOURCES `185` -> `207` rows (22 added); knowledge files
> `43` -> `52`; one tool added (`tools/mado-eventq.py`). One number fails - "eight entries" is nine
> (`git diff -M --name-status 57a772b..f6e3247 -- corpus/knowledge | grep -c '^A'` prints `9`, `'^D'` prints
> `0`) - so this note repeats the re-derived nine and marks the reflection's eight `relayed:` and corrected. The
> reflection is a pointer, not evidence. Receipt:
> `.ufo/waves/round-41/w1/ScrConsiderthese/receipts.txt`.

### C. `corpus/lessons/round-41.md` — `## Mistakes` entry (optional; the L1 numbers it)

> - class: number-drift (relayed). evidence: `considerthese/2026-10-25.md:5` states eight knowledge entries for
>   rounds 32-37; `git ls-tree -r --name-only 57a772b corpus/knowledge | wc -l` prints `43` and `52` at
>   `f6e3247`, and `git diff -M --name-status 57a772b..f6e3247 -- corpus/knowledge | grep -c '^A'` prints `9`
>   (zero deleted). captured-by: this round's first-hand re-derivation
>   (`.ufo/waves/round-41/w1/ScrConsiderthese/receipts.txt`); the reflection is not a lane file and is not
>   edited. fix: QUALITY 69; the round-41 `## considerthese` note carries the re-derivation and marks the
>   reflection's count `relayed:`.

## The command that reproduces the numbers

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
git log --oneline 57a772b..f6e3247 | wc -l                                    # 68
git show 57a772b:corpus/SOURCES.md | grep -c '^| S[0-9]'                      # 185
git show f6e3247:corpus/SOURCES.md | grep -c '^| S[0-9]'                      # 207
git diff 57a772b..f6e3247 -- corpus/SOURCES.md | grep -c '^+| S[0-9]'         # 22
git ls-tree -r --name-only 57a772b corpus/knowledge | wc -l                   # 43
git ls-tree -r --name-only f6e3247 corpus/knowledge | wc -l                   # 52
git diff -M --name-status 57a772b..f6e3247 -- corpus/knowledge | grep -c '^A' # 9
git log --diff-filter=A --format= --name-only 57a772b..f6e3247 -- tools/      # tools/mado-eventq.py
```

All read-only (`git log`/`show`/`ls-tree`/`diff` at named revisions); no worktree observable, so no witness
is needed under criterion 63.

## Limits and residuals

- I did not edit `corpus/QUALITY.md`, `SKILL.md` or any lesson: leaf write scope. Sections A-C are text for the
  L1; nothing here is landed.
- The criterion is a prose rule with a reader-run command, not a counter; no instrument enforces it, and a seat
  can still write `relayed:` beside a number it never checked. The `relayed:` label is what a spot-check can
  grep, not what a gate can prove.
- Only the mined sentence was re-derived. The reflection's other numbers are spot-check-derived and stay
  `relayed:` here by construction (e.g. the round-32 "TARGET MET on junk" is carried by
  `corpus/lessons/round-32-verifier-spotcheck.md:35`).
- Side observation, not this proposal: criterion 60 is the ratio criterion and no round-37..40 record states the
  ratio — `grep -rn 'last-30\|domain-versus-meta' corpus/lessons/round-3[7-9].md corpus/lessons/round-40.md
  LOG.md` returns only the round-36 lines (`LOG.md:2222`). A criterion without an application in four rounds is
  worth the round-41 verifier's attention; it is not re-mined here.
- No tool was installed or updated this seat; the lane's `git` and `grep` sufficed.
