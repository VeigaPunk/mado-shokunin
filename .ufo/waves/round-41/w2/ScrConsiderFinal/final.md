# ScrConsiderFinal — final text to land (considerthese, wave w2)

Seat `ScrConsiderFinal`, mado round 41, wave w2. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Data commit `07f2641696b5ac73de1404ea737a9f27e9819aa1`. Source: `.ufo/waves/round-41/w1/ScrConsiderthese/proposal.md`
(seats `ScrConsiderthese`, wave w1). This file is the exact text to land (sections A-C below); the L1
integrates. No tracked lane file is edited by this seat.

## Verification of the proposal's evidence (all read-only, at/against `07f2641`)

Every number the proposal repeats was re-derived by this seat with the command and output below. All
reproduce; no number could not be reproduced.

```
$ git rev-parse --verify 57a772b
57a772b1dc96389269732f45df5b586d2efd2f73
$ git rev-parse --verify f6e3247
f6e3247f73152a39afb86066af48f3cedf95fb0a
$ git rev-parse --verify ab2bfaa
ab2bfaab661c846d1de9d58c01651cd156a13949
$ git rev-parse --verify 07f2641
07f2641696b5ac73de1404ea737a9f27e9819aa1

$ git log --oneline 57a772b..f6e3247 | wc -l
68

$ git show 57a772b:corpus/SOURCES.md | grep -c '^| S[0-9]'
185
$ git show f6e3247:corpus/SOURCES.md | grep -c '^| S[0-9]'
207
$ git diff 57a772b..f6e3247 -- corpus/SOURCES.md | grep -c '^+| S[0-9]'
22

$ git ls-tree -r --name-only 57a772b corpus/knowledge | wc -l
43
$ git ls-tree -r --name-only f6e3247 corpus/knowledge | wc -l
52
$ git diff -M --name-status 57a772b..f6e3247 -- corpus/knowledge | grep -c '^A'
9
$ git diff -M --name-status 57a772b..f6e3247 -- corpus/knowledge | grep -c '^D'
0
$ git diff -M --name-status 57a772b..f6e3247 -- corpus/knowledge
A	corpus/knowledge/dispatcher-semantics-r25.md
A	corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md
A	corpus/knowledge/event-delivery-limits-r26.md
A	corpus/knowledge/event-queue-observability-r37.md
A	corpus/knowledge/idle-lock-chain-armed-r14.md
A	corpus/knowledge/idle-lock-never-asked-r12.md
A	corpus/knowledge/idle-lock-offered-in-the-bar-r15.md
A	corpus/knowledge/ipc-contract-r25.md
A	corpus/knowledge/waybar-module-text-route-r25.md
(9 `A` lines; 0 `D`; no `R`/`M` lines — the file count is the entry count)

$ git log --diff-filter=A --format= --name-only 57a772b..f6e3247 -- tools/ | grep -c .
1
$ git log --diff-filter=A --format= --name-only 57a772b..f6e3247 -- tools/
tools/mado-eventq.py

$ git log --diff-filter=A --format='%h' --name-only 57a772b..f6e3247 -- corpus/knowledge | awk 'NF==1{print}'
3f42425
corpus/knowledge/event-delivery-limits-r26.md
corpus/knowledge/event-queue-observability-r37.md
02088b4
corpus/knowledge/idle-lock-chain-armed-r14.md
corpus/knowledge/idle-lock-never-asked-r12.md
corpus/knowledge/idle-lock-offered-in-the-bar-r15.md
fa7ba11
corpus/knowledge/waybar-module-text-route-r25.md
f591087
corpus/knowledge/dispatcher-semantics-r25.md
corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md
corpus/knowledge/ipc-contract-r25.md

$ git show -s --format='%h %s' f591087
f591087 round-32: C1 IPC two-socket theme (3 entries, 5 rows) + C2 axis-score gate + wave-1 evidence
$ git show -s --format='%h %s' fa7ba11
fa7ba11 round-34: admit the waybar event-socket entry after the frozen counter
$ git show -s --format='%h %s' 02088b4
02088b4 round-35: the idle-lock control surface lands — three entries, eight rows S203-S210, errata, and the wave-1 evidence
$ git show -s --format='%h %s' 3f42425
3f42425 round-37: data — two event-socket delivery entries (one package entry re-grounded, two refused as null-channel), rows S212-S217, tools/mado-eventq.py with its live receipt, QUALITY 62-63, and the GIT_* scrub in four lane gates
(round 32: 3, round 34: 1, round 35: 3, round 37: 2)

$ git show ab2bfaa:corpus/QUALITY.md | grep -c '^[0-9]\{1,3\}\. '
68
$ git show 07f2641:corpus/QUALITY.md | grep -c '^[0-9]\{1,3\}\. '
68
$ git show 07f2641:corpus/QUALITY.md | grep -oE '^[0-9]{1,3}\. ' | tail -1
68. 
(QUALITY.md is at 68 criteria at both base and data commit; the new criterion is 69)

$ git show ab2bfaa:corpus/QUALITY.md | grep -n considerthese
367:60. Every round report states the lane's last-30-commit domain-versus-meta ratio with its command, and a lane that goes two or more rounds without a domain-facing change says so plainly in that section. Domain-facing means `tools/`, `corpus/knowledge/`, `PROVINCE.md` or `SKILL.md`; records and instruments are meta. Ground: `considerthese/2026-10-24.md` proposal 1 (2026-10-24), measured this round at 3 domain / 27 meta. (lesson: lessons/round-36.md#mistakes M36-5)
$ git show ab2bfaa:corpus/QUALITY.md | grep -ni 'relay\|first-hand\|first hand' || true
(empty)
$ git show ab2bfaa:SKILL.md | grep -ci considerthese
0
$ git show ab2bfaa:PROVINCE.md | grep -ci considerthese
0
$ git show 07f2641:quality/check-evidence-pointers.py | grep -n considerthese
49:PATHY = re.compile(r"^(?:\.ufo|corpus|quality|tools|scripts|considerthese)/[^\s]*$")

$ git show 07f2641:corpus/lessons/round-33.md | sed -n '28p'
- considerthese/2026-10-24.md proposal 5 (verify one cited fact first-hand) was
$ git show 07f2641:corpus/lessons/round-33.md | grep -n 'class: number-drift'
45:- class: number-drift. evidence: the round-32 report and LOG called the committed
$ git show 07f2641:corpus/lessons/round-33.md | sed -n '45,48p'
- class: number-drift. evidence: the round-32 report and LOG called the committed
  scratch 187 MB. The closure measured 11.6 MB / 554 blobs at `f5910876`, and
  `48f9fe09` deleted 130 files. captured-by: none. fix: this lesson; the filed
  round-32 report is not edited.
$ git show 07f2641:corpus/lessons/round-40.md | sed -n '146p'
`considerthese/2026-10-25.md` proposal 2 ("Count dead attempts and dirty closures from the watchdog digests", restating
$ git show 07f2641:corpus/lessons/round-40.md | sed -n '166p'
is added for it (no mistake of this round backs one); the proposals 1 and 3-6 of the same file stay open.
$ git show 07f2641:corpus/lessons/round-39.md | sed -n '82p'
(watch M37-5 by name) is served by C1's re-registration.
$ git show 07f2641:corpus/lessons/round-38.md | sed -n '4p'
**C1** (v3 re-grounding counter discriminating the round-37 v2 cribs), **C2**

$ git show 07f2641:considerthese/2026-10-25.md | sed -n '3p;5p;7p;38p;50p'
... this one covers the 68 commits after `57a772b` (yesterday's reflection) up to tip `f6e3247`: rounds 32–37 ...
**Bottom line:** ... In this window `corpus/knowledge/` gained eight entries, `corpus/SOURCES.md` went from 185 to 207 rows (S186–S217), and one new runnable tool landed (`tools/mado-eventq.py`). ...
## What landed after the last reflection
| Domain drift (flagged 2026-10-24) | Resolved for this window: 8 knowledge entries, 22 source rows, 1 tool |
5. **Verify one fact first-hand per day, read-only.** ... everything else is relayed from spot-checks. I could pick one cited source line each day and re-open it.
```

The reflection quotes were re-verified against `considerthese/2026-10-25.md` at `07f2641` (quotes
1-4, 12 of `.ufo/waves/round-41/w1/ScrConsiderthese/verify-quotes.py`, all PASS, `MADO_QUOTES:
passed=12/12`).

One verification note: my convenience check `git rev-parse --short 57a772b f6e3247 ab2bfaa
07f2641` (four names in one call) errored `fatal: Needed a single revision`; the four individual
`git rev-parse --verify` calls above succeed, so the error was a multi-arg parsing quirk of that
convenience call, not a missing revision. It is not an evidence command from the proposal and affects
no reproduced number.

## Text to land

### A. `corpus/QUALITY.md` — append as criterion 69 (after 68)

```
69. A round that mines a proposal from `considerthese/<date>.md` re-derives, from the lane's own bytes, every
number its mining note repeats, and the note carries the command and its output beside each re-derived number;
a number taken on trust is written `relayed:` with the spot-check path that carries it, because the reflection
is a pointer, not evidence. Check: run the note's commands at the reflection's own base and tip pins; a count
the command does not print is corrected in the note or marked `relayed:`. Shown able to fail:
`considerthese/2026-10-25.md:5` reports that `corpus/knowledge/` "gained eight entries" over rounds 32-37, while
`git ls-tree -r --name-only 57a772b corpus/knowledge | wc -l` prints `43` and the same command at `f6e3247`
prints `52` — nine files added (round 32: 3, round 34: 1, round 35: 3, round 37: 2), zero deleted. Ground:
`considerthese/2026-10-25.md` proposal 5 (2026-10-25); the relayed-number class is
`lessons/round-33.md#mistakes` (number-drift). (lesson: lessons/round-41.md#mistakes M41-n)
```

`M41-n` is the L1's numbering; substitute the round-41 mistake id it assigns (the next free id after
M41-8 is M41-9 if the optional section C is numbered).

### B. `corpus/lessons/round-41.md` — `## considerthese` section (replaces the skeleton line "No proposal is
claimed by this skeleton.")

```
`considerthese/2026-10-25.md` proposal 5 ("Verify one fact first-hand per day, read-only", restating
`2026-10-24.md` proposal 5, mined in round 33 as prose) is mined as QUALITY 69. The reflection's mined
sentence re-derives: 68 commits `57a772b..f6e3247`; SOURCES `185` -> `207` rows (22 added); knowledge files
`43` -> `52`; one tool added (`tools/mado-eventq.py`). One number fails — "eight entries" is nine
(`git diff -M --name-status 57a772b..f6e3247 -- corpus/knowledge | grep -c '^A'` prints `9`, `'^D'` prints
`0`) — so this note repeats the re-derived nine and marks the reflection's eight `relayed:` and corrected. The
reflection is a pointer, not evidence. Receipt:
`.ufo/waves/round-41/w1/ScrConsiderthese/receipts.txt`.
```

### C. `corpus/lessons/round-41.md` — `## Mistakes` entry (optional; the L1 numbers it)

```
**M41-n - the reflection's relayed entry count is wrong; first-hand re-derivation shows nine, not
eight.** Class: number-drift (relayed). Evidence: `considerthese/2026-10-25.md:5` states eight knowledge entries
for rounds 32-37; `git ls-tree -r --name-only 57a772b corpus/knowledge | wc -l` prints `43` and `52` at
`f6e3247`, and `git diff -M --name-status 57a772b..f6e3247 -- corpus/knowledge | grep -c '^A'` prints `9`
(zero deleted). Captured-by: this round's first-hand re-derivation
(`.ufo/waves/round-41/w1/ScrConsiderthese/receipts.txt`); the reflection is not a lane file and is not
edited. Fix: QUALITY 69; the round-41 `## considerthese` note carries the re-derivation and marks the
reflection's count `relayed:`.
```

## Numbers not reproducible

None. Every number in sections A-C above was reproduced by the commands in the verification block
(including "68", "185", "207", "22", "43", "52", "9", "0", "1 tool: `tools/mado-eventq.py`", and the
per-round 3/1/3/2 split). The only failed command this seat ran was its own convenience
`git rev-parse --short` four-arg call described above — not an evidence command, and its failure is
explained by the individual successful verifies.

## Scope and safety

- Read-only git only (`log`/`show`/`ls-tree`/`diff`/`rev-parse` at named revisions); no index/worktree
  mutation, no `status`-style worktree observables. No host service, journal, compositor or package
  access.
- No tool installed or updated: the lane's `git` and `grep` sufficed (no tooling event to record).
- Nothing is edited in the lane by this seat; sections A-C are the landing text for the L1. The receipt
  path cited in B/C (`.ufo/waves/round-41/w1/ScrConsiderthese/receipts.txt`) is tracked in the tree at
  `07f2641`.
