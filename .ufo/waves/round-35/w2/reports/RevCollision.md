# RevCollision — id-collision guard, round 35 wave 2

Seat: `L1Mado35.RevCollision` (leaf executor). Read-only over lane and `/home/vgpnk/Projects/shokuknow`.
Scratch: `.ufo/waves/round-35/scratch/RevCollision/`. Tooling installed: none.

## Verdicts

| # | Claim tested | Result | Evidence |
|---|---|---|---|
| V1 | Specified pipeline on the real registry pair yields the collision count | **8 collisions: S203–S210** (verified) | V1 below, rc=0 |
| V2 | "Inject `  \| S203 \|` and the same pipeline reports a collision" | **FALSE — reports 0** | V2/V2b below, rc=0 |
| V3 | Pipeline is live (control: same injection, zero indent) | **1 collision** | V3 below, rc=0 |
| V4 | A column-anchored, indent-stripping repair | **8 real, 8/8 injections, 0 false positives** | V4 below, rc=0 |

Two independent results. (1) On the actual data the guard is correct and reports a
**true-positive count of 8**. (2) The guard **cannot detect an indented row**, so the
fault-injection step the round item asks for does not produce the collision it expects.
The count on real data is unaffected only because neither file currently contains an
indented row.

## Axes (godspeed)

- **A1 count correctness** — collisions on the real pair.
- **A2 sensitivity** — does an injected colliding row fire the guard.
- **A3 specificity** — does the guard avoid non-id-column mentions.
- **A4 reach** — which leading-whitespace shapes the line anchor admits.

## V1 — specified pipeline, unmodified inputs

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <lane>/corpus/SOURCES.md | LC_ALL=C sort > lane-ids.txt   # rc=0
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md | LC_ALL=C sort > append-ids.txt   # rc=0
$ LC_ALL=C comm -12 lane-ids.txt append-ids.txt > collisions-specified.txt   # rc=0
$ wc -l collisions-specified.txt
8
```

lane ids: **200** (unique, `sort | uniq -d` empty — no internal duplicates)
append ids: **147** (contiguous S203…S349, no gaps)
collision count: **8**

### Lane list tail (last 10)

```
| S201
| S202
| S203
| S204
| S205
| S206
| S207
| S208
| S209
| S210
```

### Append list tail (last 10)

```
| S340
| S341
| S342
| S343
| S344
| S345
| S346
| S347
| S348
| S349
```

### Collisions

```
| S203
| S204
| S205
| S206
| S207
| S208
| S209
| S210
```

### The 8 are real namespace reuse, not parser noise

Same id, unrelated source in each registry:

```
lane   | S203 | host omarchy first-run installer - the desktop's post-login questionnaire ...
append | S203 | Hyprland IPC page — current upstream source — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/...
```

Provenance of the overlap (`/home/vgpnk/Projects/shokuknow/merge/mado/MERGE-REPORT.md:9`):

> lane registry currently holds **192** rows; first staged id is **S203**

The merge staged 147 rows **S203–S349** against a 192-row snapshot of the lane, i.e.
"continuing the lane's S-space" from a lane that then ended at S202. Wave 1 of this
round subsequently minted **S203–S210** into the lane registry for the three idle-lock
entries (`corpus/knowledge/idle-lock-{never-asked-r12,chain-armed-r14,offered-in-the-bar-r15}.md`).
Both writers were internally consistent; the id space was allocated twice. The guard's
8 is therefore a true positive and a live merge concern: appending S203–S349 onto the
current registry duplicates S203–S210. With the lane still at 200 rows, a clean merge
either renumbers the appended block or renumbers the round-35 block.

## V2 — fault injection with the specified parser FAILS to fire

Scratch registry = lane registry with the 8 pre-existing closed rows removed
(`registry-baseline.md`, 192 rows, **0 collisions** — V4 confirms), so an injected row is
the only possible source of a hit. This cleaning is required: on the uncleaned registry
`sort -u` dedups, so injecting a second `S203` cannot change the count of 8 — the test
would be vacuous.

```
$ printf '  | S203 | INJECTED two-space indent probe | own-work | A | p | p | p | mined | 2026-10-25 | on-change | none |\n' >> registry-inject2sp.md
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' registry-inject2sp.md | LC_ALL=C sort -u > inj2.ids   # rc=0
$ LC_ALL=C comm -12 inj2.ids append-ids.txt | wc -l
0
```

**0, not 1.** The item's expected collision does not occur.

### V2b — why: `-o` keeps the indent in the token

```
$ grep -E 'INJECTED 2-space' registry-inject2sp.md | grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' | od -An -c
           |       S   2   0   3  \n
```

The extracted token is the 8-byte string `"  | S203"`. The append side yields `"| S203"`.
`comm` compares byte strings, so the two never intersect:

```
$ LC_ALL=C comm -3 inj2.ids append-ids.txt | grep S203 | cat -A
  | S203$          <- unique to the injected list
^I| S203$          <- unique to the append list
```

The `^ {0,3}` prefix makes the line *reachable* but simultaneously *embeds the indent into
the comparison key*. Net effect: rows indented 1–3 spaces are matched and then discarded.
The parser cannot be worse than `^\|` — it is exactly as blind, because the prefix is
carried into the key instead of being dropped.

### V3 — control: the pipeline itself is live

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' registry-inject0sp.md | LC_ALL=C sort -u > inj0.ids   # rc=0
$ LC_ALL=C comm -12 inj0.ids append-ids.txt
| S203
```

count = **1**. Same file, same commands, indent removed → detected. The miss in V2 is
caused solely by the indent, not by a broken pipeline, a bad path, or a dead append list.

### Indent sweep, specified parser

| injected leading whitespace | token produced | collisions |
|---|---|---|
| 0 spaces | `\| S203` | **1** |
| 1 space | ` \| S203` | 0 |
| 2 spaces (item's case) | `  \| S203` | **0** |
| 3 spaces | `   \| S203` | 0 |
| 4 spaces | *(line not matched)* | 0 |
| 1 tab | *(line not matched)* | 0 |

Two distinct failure modes: indents 1–3 are matched but keyed wrong; indent ≥4 and tabs
never satisfy `^ {0,3}\|` at all. Measured reach: `registry-inject4sp.md` and
`registry-inject-tab.md` each hold **193** id-column rows of which the specified parser
reaches **192** — exactly the un-injected count, i.e. the injected row is invisible to the
line anchor. Both modes are silent — exit code stays 0.

## V4 — repair that improves every axis and harms none

Anchor the **id column** (require the closing pipe of the first cell) and emit the **bare id**,
which also lifts the indent bound:

```
$ grep -oE '^[[:space:]]*\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' <file> | grep -oE 'S[0-9]{3,}' | LC_ALL=C sort -u
```

| input | specified parser | repaired parser |
|---|---|---|
| real lane + real append | 8 | **8** (no regression) |
| injection, 0 space | 1 | **1** |
| injection, 2 spaces | 0 | **1** |
| injection, 3 spaces | 0 | **1** |
| injection, 4 spaces | 0 | **1** |
| injection, 1 tab | 0 | **1** |
| cleaned baseline | 0 | **0** |
| append inline mentions S013/S014 | excluded | **excluded** |

The repair is strictly dominant: same answer on real data, every injection caught, no
false positives.

### Why the naive repair (strip indent only) is wrong

`grep -E '^ {0,3}\|...' | grep -oE 'S[0-9]{3,}'` reports **10** collisions, adding
`S013` and `S014`. Those are not id rows in the append file — they are inline references
inside the cells of rows S249 and S251:

```
53:| S249 | host gkeep waybar producer ...
55:| S251 | host gkeep window rules ...
$ grep -nE '^ {0,3}\|[[:space:]]*S(013|014)[[:space:]]*\|' SOURCES.append.md
(none)
```

Lane rows `S013`/`S014` at `corpus/SOURCES.md:25-26` are genuine, but the append-side hits
are mentions. Normalizing to bare ids without re-anchoring the column trades a
false-negative for two false-positives. The column-anchored form in V4 avoids both.

## Retained artifacts (scratch, sha256)

| file | sha256 |
|---|---|
| `lane-ids.txt` | `a94fea1406e983a8360cee4e7c8e9fc3de6afc104eb4a34ff49190a5ed12df94` |
| `append-ids.txt` | `6b007a2f34f974b52b7459c495eb09f93f89b73284f205245b2af1cf6af217d6` |
| `collisions-specified.txt` | `5aedf9d39cd0949583da8d58e0386994b03cddee7bb7a56c38760f157c5cdb95` |
| `registry-baseline.md` | `fbbf365c6f1a1aaa2a7d4ffb62ffdec6063807e973da34c45f394d35511dd657` |
| `registry-inject2sp.md` | `7e17b60f456aa88e94e6fb63ef87b8528f3a6a61a14430904650509fb9f543ab` |

Also present: `registry-inject{0,1,2,3,4}sp.md`, `registry-inject-tab.md`,
`lane-ids-norm.txt`, `append-ids-norm.txt`, `lane-rep.txt`, `append-rep.txt`, `summary.txt`.

## Risks / open items

1. **The guard's indent property is false as specified.** Any future use of
   `^ {0,3}\|[[:space:]]*S[0-9]{3,}` as a merge gate inherits a silent-miss class. Use the
   V4 form.
2. **The 8 collisions are unresolved in-repo.** This seat is read-only and did not
   renumber anything. Whether the appended block or the round-35 block moves is a merge
   decision above this ticket; the guard output is a true positive either way.
3. **The count is data-dependent, not property-dependent.** V1 = 8 holds only while
   neither file contains indented id rows. It is not evidence that the guard works.
4. No blocker. Every verdict above is a command run in this session with rc=0; nothing
   is inferred from source reading. Unverified: whether round 35 intends the appended
   S203–S349 block to be renumbered before merge — no artifact in the lane states it.
