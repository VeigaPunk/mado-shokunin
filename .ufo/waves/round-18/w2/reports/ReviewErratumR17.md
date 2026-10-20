# ReviewErratumR17 — round-17 erratum falsified against git and the three w1 reports

Seat `MadoR18.ReviewErratumR17`, 2026-10-20. Target: the block appended to
`corpus/lessons/round-17.md` (lines 177-201) at integration commit
`4c103b55b1ea5c3c555884afe3eb69b5189701b7`; receipts commit
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f` (master tip). Read-only: lane git
only (`log/show/diff/ls-tree/merge-base/rev-parse`), file bytes, and the three
w1 reports `RevR17V1Facts`, `RevengeR17Recut`, `RevR17V2Facts`. No gate/tool
run, no package/service/compositor command, no transcript read (the round-17
transcript is not named to this item; run facts below rest on the w1 reports),
no file written except this report. Nothing installed or updated.

## Verdict

The erratum is **substantially accurate**: its central corrections (the
round-17 re-cut ran but left no producer-bound receipt; r13-r16/anchor are
byte-identical to their `f71ccbe` blobs; the round-17 report's C3 row pairs a
`f71ccbe` tool sha with a post-P11 count) are all supported by git and the w1
reports. Two statements are nonetheless checkable defects in an append-only
correction record, and four are precision/advisory issues.

Append-only requirement: **met**. Lines 172-176 are untouched; the block is a
pure append after the previous EOF.

```
$ git diff --numstat d9a5a18 4c103b5 -- corpus/lessons/round-17.md
25      0       corpus/lessons/round-17.md
$ git diff d9a5a18 4c103b55b1ea5c3c555884afe3eb69b5189701b7 -- corpus/lessons/round-17.md | grep -c '^-[^-]'
0                    # grep rc 1 (no match)
$ git show 4c103b5 -- corpus/lessons/round-17.md   # one hunk @@ -174,3 +174,28 @@
$ git log --oneline 4c103b5..abfbf35 -- corpus/lessons/round-17.md   # empty
$ git diff --stat 4c103b5 -- corpus/lessons/round-17.md              # empty
```

The block is lines 177 (blank separator) through 201, file length 201.

## Findings by severity

### F1 — Medium: the erratum's exhaustive changed-bytes claim is false

Erratum lines 187-189:

> r13-r16 and the anchor came out byte-identical to their `f71ccbe` blobs, so
> `0ab1ccc` records no change to them; only `tripwire-r17.txt` (growing seat
> transcripts) and the selftest receipts changed bytes.

`tripwire-vs-oracles.json` also changed bytes at `0ab1ccc`. Git:

```
$ git diff-tree --no-commit-id --name-status -r 0ab1ccc -- .ufo/waves/round-17/evidence
M  .../tripwire-r17.txt
M  .../tripwire-selftest-compound.txt
M  .../tripwire-selftest-core.txt
M  .../tripwire-selftest-hardening.txt
M  .../tripwire-selftest-w2-regressions.txt
M  .../tripwire-vs-oracles.json
M  .../tripwire-w2-adversarial.txt
M  .../tripwire-w2-false-positive.txt
```

and its only delta is one line:

```
$ git diff 9bbb881 0ab1ccc -- .ufo/waves/round-17/evidence/tripwire-vs-oracles.json
- "tool_sha256": "7a98720ed3c0ea1676714381a9289a65dd2a416f98b764e2b52517f81ef31fe7",
+ "tool_sha256": "962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072",
```

The erratum's own cited source contradicts it: `RevengeR17Recut` §"What git
recorded at `0ab1ccc`" lists `tripwire-vs-oracles.json` as `1/1` and states
"`tripwire-vs-oracles.json`: only `"tool_sha256"`, `7a98720e…` → `962919ce…`".
The six selftest/w2 receipts named in the erratum are correctly in the changed
set; the omitted file is the only committed 962919ce attribution for the scans.

Impact: the erratum, whose subject is exactly the committed provenance
surface, understates that surface by one file. Fix (append-only): "…and the
selftest receipts changed bytes, plus `tripwire-vs-oracles.json` (its
`tool_sha256` line only)".

Secondary (not false, noted for completeness): record 539 also regenerated
`tripwire-w2-adversarial.txt` and `tripwire-w2-false-positive.txt`
(`RevengeR17Recut` steps 1-2); the erratum's "regenerated r13-r16, the r15
anchor, r17 and the vs-oracles file" omits them from the enumeration, though
its next clause's "selftest receipts" covers them.

### F2 — Medium: the supersession pointer's "first line" universal is false for one file in its own glob

Erratum lines 194-197:

> It is superseded by the round-18 receipts `.ufo/waves/round-18/evidence/tripwire-*.txt`,
> whose first line names `tool_sha256` and `measured_commit`

The glob matches 9 committed files at `abfbf35`; 8 have a `RECEIPT` first
line carrying both fields, `tripwire-pacmanlog-join.txt` does not:

```
$ for f in $(git ls-tree -r --name-only abfbf35 -- .ufo/waves/round-18/evidence | grep 'tripwire-.*\.txt$'); do
    l=$(git show abfbf35:$f | sed -n '1p')
    printf '%s tool=%s commit=%s\n' "$(basename $f)" \
      "$(printf '%s' "$l" | grep -c 'tool_sha256=')" \
      "$(printf '%s' "$l" | grep -c 'measured_commit=')"
  done
...
tripwire-pacmanlog-join.txt    tool=0 commit=0
tripwire-r13.txt               tool=1 commit=1
...
```

`tripwire-pacmanlog-join.txt` line 1 is
`# Round-18 C1 re-derivation: tripwire host_mutation pacman findings vs /var/log/pacman.log`;
the two fields first appear on line 4 in a hand-authored `# receipt:` comment,
and the file is a join (it documents the `awk` command), the same class of
artifact the erratum correctly excludes for round 17. The rest of the
supersession claim is sound and stronger than the erratum states: every
tool-produced receipt header validates against the revision it names:

```
# for the 8 tool receipts: tool_sha256 == sha256(git show <measured_commit>:tools/mado-tripwire.py)
harm-tripwire-* / tripwire-anchor-r15 / frozen-{before,match,tampered} / r13-r16 -> OK (8/8)
# e.g. frozen-before: tool 962919ce…, measured_commit d9a5a18; tool at d9a5a18 = 962919ce…
#      r13/r14/r15/r16/anchor/frozen-match/frozen-tampered: c87a31ef… at measured_commit 4c103b5
```

Fix (append-only): say "every tool-produced round-18 `tripwire-*.txt` receipt
carries `RECEIPT … tool_sha256=… measured_commit=…` on line 1; the join is
hand-authored and records the pair in its header comment (line 4)."

Timing caveat (not a falsehood): at `4c103b5`, `.ufo/waves/round-18/evidence/`
contains **no** `tripwire-*` file; the glob is real only at `abfbf35`. The
erratum names no revision for the receipts, so a reader checking the erratum's
own commit sees a dangling path. Master (`abfbf35`) resolves it.

### F3 — Low: "No committed byte shows that the re-cut ran" is stronger than the w1 record

Erratum lines 190-192. `RevR17V1Facts` §5 says:

> The only committed `962919ce` attribution for the r13–r16 scans is
> `tripwire-vs-oracles.json`'s single `tool_sha256` field, which changed by
> exactly one line at `0ab1ccc` … A one-line text edit would be
> indistinguishable from the real regeneration that in fact occurred.

A committed byte produced by the re-cut cell therefore does name the new tool,
though it does not bind the `.txt` receipt bytes and a hand edit would look
identical. Read as "no committed byte *binds* the receipt bytes", the erratum
is correct; read literally, it is contradicted by the vs-oracles delta (F1).
Recommended wording: "no committed byte binds those receipts to the re-cut;
the only committed 962919ce attribution for the scans is `tripwire-vs-oracles.json`'s
one-line `tool_sha256` change, which does not bind the receipt bytes."

### F4 — Low: "30/30 … exists only at `0ab1ccc`" is globally false, locally true

Erratum lines 198-200. The 30/30 state *first appears* at `0ab1ccc` and is
carried unchanged afterwards:

```
$ git log --oneline -- .ufo/waves/round-17/evidence/tripwire-selftest-w2-regressions.txt
0ab1ccc ...
f71ccbe ...
$ git show 0ab1ccc:.../tripwire-selftest-w2-regressions.txt | grep -E 'SUMMARY|SHA256'
SELFTEST_SCRIPT_SHA256: 962919ce…d5aaa072
SELFTEST_SUMMARY: 30/30 passed failed=[]
# same receipt bytes at d9a5a18, 4c103b5, abfbf35
```

`RevR17V2Facts` F1 uses the correct phrasing ("30/30 first appears at
`0ab1ccc`"). Since the erratum compares `f71ccbe` vs `0ab1ccc`, "only" is
readable as "only after the P11 fix", but it is false as a global claim. Use
"first exists at".

### F5 — Informational: the quotation is a mid-line fragment presented as the lines

Erratum lines 180-181 say `Lines 175-176 read:` and quote a fragment that is a
true substring of the two lines but starts after an unmarked elision:

```
175:  real comment) — `tripwire/w2-regressions` 30/30; tool sha256 `962919ce…`;
176:  all real-transcript receipts re-cut with identical counts.
```

The quoted fragment omits line 175's prefix `real comment) — `. Not a
falsehood; flag only because this erratum's value is exact quotation.

### F6 — Low, advisory: the same sentence's false case list is left uncorrected

Erratum scope is lines 175-176, but the sentence it quotes begins at line 174:

```
174:  before tokenizing; four new regression cases (quoted, escaped, mid-word,
175:  real comment) — ...
```

`RevR17V2Facts` F4 shows the list is wrong in two of four slots. Git confirms
the four added cases at `0ab1ccc` are `quoted-hash-not-comment`,
`escaped-hash-not-comment`, `comment-after-separator-is-data`,
`redirect-target-before-command`; `midword-hash-not-comment.jsonl` and
`real-comment-is-data.jsonl` already exist at `f71ccbe`:

```
$ git diff --name-status f71ccbe 0ab1ccc -- .ufo/waves/round-17/tripwire/w2-regressions/
A comment-after-separator-is-data.jsonl
A escaped-hash-not-comment.jsonl
M expected.json
A quoted-hash-not-comment.jsonl
A redirect-target-before-command.jsonl
$ git ls-tree --name-only f71ccbe -- .../w2-regressions/ | grep -E 'midword|real-comment'
midword-hash-not-comment.jsonl
real-comment-is-data.jsonl
```

The erratum does not assert the list is right, so this is a scope gap rather
than a false fact; but a round-18 correction record that leaves a known-false
clause in the sentence it addresses invites the next round's erratum.

### F7 — Informational: heading "outside R17-V1/V2" reads against its own content

The heading (line 178) says `outside R17-V1/V2`, while bullet 2 is the R17-V1
defect and bullet 4 is explicitly `R17-V2: …`. If the intended meaning is
"additive to the spot-check's routed items / does not modify them" (as
`corpus/QUALITY.md:124` uses "outside R17-V1/V2/V5"), say so; as written it
can be read as "not about R17-V1/V2", which the bullets contradict.

## Claim-by-claim verification

| Erratum claim (lines) | Verdict | Evidence |
|---|---|---|
| Appended, append-only (177-201) | TRUE | `25 0` numstat; `grep -c '^-[^-]'` = 0 (rc 1); single hunk `@@ -174,3 +174,28 @@`; unchanged through `abfbf35` and worktree |
| Lines 175-176 read `30/30; 962919ce…; all … re-cut with identical counts` (180-181) | TRUE as substring | line 175 contains first fragment, line 176 the second; line 175 also carries the lead-in `real comment) — ` (F5) |
| Re-cut ran at record 539, 15:17:25.987Z (184) | TRUE | `RevR17V1Facts` §4 item 3: line 539 `15:17:25.987Z`; `RevengeR17Recut` timeline row 10; result 541 `15:17:29.253Z` |
| After P11 fix at record 536 (184-185) | TRUE | `RevR17V1Facts` §4 item 2: line 536 `15:17:13.800Z`, suites 9/9 16/16 33/33 30/30 at line 538 |
| Regenerated r13-r16, anchor, r17, vs-oracles with 962919ce (185-186) | TRUE | `RevengeR17Recut` §What the re-cut did steps 3-6; printed sha `962919ce…` in result 541; tool at `0ab1ccc` = `962919ce…` |
| Record 541 printed the counts (186) | TRUE | `RevR17V1Facts` §4 item 4 / `RevengeR17Recut` count block; counts r13 2/12/19, r14 4/0/46, r15 3/29/177, r16 0/0/2, anchor 2/1/5 |
| r13-r16 + anchor byte-identical to `f71ccbe` blobs (187) | TRUE | blobs at both revisions: r13 `89cfec0…`, r14 `a31e9d6…`, r15 `cd5cce1…`, r16 `0fc3829…`, anchor `dc0e740…`; `git diff --stat f71ccbe 0ab1ccc -- <five>` empty |
| `0ab1ccc` records no change to them (187-188) | TRUE | `git diff-tree … 0ab1ccc -- evidence` lists 8 paths, none of the five (nor the join) |
| Only r17 + selftest receipts changed bytes (188-189) | **FALSE** | vs-oracles also changed (F1); r17 change (growing seat transcripts) matches `RevengeR17Recut` (MadoR17.jsonl 509→540 lines, 14/149 entries) |
| No committed byte shows the re-cut ran / producer (190-192) | TRUE as scoped to the six; **overbroad** for "ran" | six receipts: top-level keys `counts, exit, files, findings, permitted, schema, unpermitted`; 0 grep hits for `tool_sha256|measured_commit|962919ce|7a98720e` in each at `0ab1ccc`; see F3 for the vs-oracles nuance |
| Join never re-cut; hand-authored, not tool output (192-193) | TRUE | blob `3dd1b04…` identical at `f71ccbe`/`0ab1ccc`; `git log --oneline -- join` = `f71ccbe`, `988b858`; `RevR17V1Facts` §3 (heredoc at transcript line 381, header documents `awk` command) |
| Superseded by round-18 `tripwire-*.txt`, first line has both fields (194-197) | PARTLY FALSE | 8/9 first lines have both and validate (8/8 header sha == `git show <measured_commit>:tools/mado-tripwire.py`); join lacks them on line 1 (F2). Receipts committed only from `abfbf35`, not `4c103b5` |
| Citation: lesson `round-18.md` M1, QUALITY 24 (196-197) | TRUE | `corpus/lessons/round-18.md:16` M1 = producer-identity defect; `corpus/QUALITY.md:131` criterion 24 requires `tool_sha256`/`measured_commit` and a committed re-cut receipt ("never a narrated rerun") |
| Report C3 row pairs `7a98720e…` with `30/30` (198-199) | TRUE | fleet report `.ufo/reports/round-17/mado.md:76` verbatim: "present, sha256 `7a98720e…`; 9/9, 16/16, 33/33, 30/30 exit 0; anchor exit 1…"; line 3 carries `962919ce…` + 30/30 |
| At `f71ccbe` suite was 26/26 (199-200) | TRUE | committed receipt: `SELFTEST_SCRIPT_SHA256: 7a98720e…`, `SELFTEST_SUMMARY: 26/26`, 26 `CASE` lines; replay in `RevR17V2Facts` F1 (7a98720e on 26-case suite = 26/26) |
| Line 132 `("26/26")` is the `f71ccbe` count (200) | TRUE | `round-17.md:132` text `tripwire/w2-regressions 26/26`; block heading `## Wave-2 corrections` (line 90, landed `f71ccbe`); f71ccbe receipt 26/26 |
| Line 175 `("30/30")` is the `0ab1ccc` count (200-201) | TRUE | `round-17.md:175` `30/30`; 0ab1ccc receipt 30/30 with 962919ce; 30 `CASE` lines |
| Tool shas: `7a98720e` = `f71ccbe`, `962919ce` = `0ab1ccc` | TRUE | `f71ccbe` `7a98720ed3c0ea16…f31fe7`; `0ab1ccc` `962919cec38ab81d…d5aaa072`; `d9a5a18` = `962919ce…`; `4c103b5`/`abfbf35`/worktree = `c87a31efa2f4eb6d…d59b4bb` |
| Erratum is at `4c103b5` | TRUE | `git show 4c103b5:corpus/lessons/round-17.md` lines 178-201; w1 report blobs committed there: `RevR17V1Facts` `6d36db8…`, `RevengeR17Recut` `a25e68a…`, `RevR17V2Facts` `00018a0…`; worktree identical |

## Residual risk and verification gaps

- **Transcript not re-read.** The run facts (record indices, timestamps, cell
  order, tool sha, printed counts) are taken from `RevR17V1Facts` §4 and
  `RevengeR17Recut`; both agree on every value checked. I did not open
  `MadoR17.jsonl` (not named to this item; the prompt restricts transcripts to a
  different session). The two reports' agreement plus committed blob identity
  is the corroboration.
- **No replay.** Counts and tool shas come from committed receipts and blobs;
  I did not execute the tripwire or any suite (lane bounds). The 26/26 vs 30/30
  distinction is additionally corroborated by `RevR17V2Facts`'s replay.
- **"No committed byte" is a proof claim.** F3 is a wording finding: whether
  vs-oracles' one-line change "shows" the re-cut ran depends on whether "shows"
  means "proves/binds" or "records a value". The report should say which.
- **Timing.** The round-18 receipts exist only at `abfbf35` (31 evidence files
  tracked there); at `4c103b5` the evidence tree has 7 files and no
  `tripwire-*`. Any check of the supersession pointer must use `abfbf35`/master.
- **Not verified:** that the round-18 receipts' counts equal round-17's (the
  erratum does not claim it), and the correctness of the receipts' findings
  against oracles. Out of scope here.
- **F6 is a scope judgment:** the erratum's quoted lines exclude line 174, so
  leaving the case-list error is not a false statement, only an incomplete
  correction. L1 decides whether the erratum should have covered it.

## Reproduction (all read-only)

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
git diff --numstat d9a5a18 4c103b5 -- corpus/lessons/round-17.md          # 25 0
git diff d9a5a18 4c103b5 -- corpus/lessons/round-17.md | grep -c '^-[^-]' # 0, rc 1
git diff-tree --no-commit-id --name-status -r 0ab1ccc -- .ufo/waves/round-17/evidence
git diff 9bbb881 0ab1ccc -- .ufo/waves/round-17/evidence/tripwire-vs-oracles.json
git show f71ccbe:.ufo/waves/round-17/evidence/tripwire-selftest-w2-regressions.txt | grep -E 'SUMMARY|SHA256'
git show 0ab1ccc:.ufo/waves/round-17/evidence/tripwire-selftest-w2-regressions.txt | grep -E 'SUMMARY|SHA256'
for r in f71ccbe 0ab1ccc 4c103b5 abfbf35 d9a5a18; do git show $r:tools/mado-tripwire.py | sha256sum; done
for f in $(git ls-tree -r --name-only abfbf35 -- .ufo/waves/round-18/evidence | grep 'tripwire-.*\.txt$'); do
  git show abfbf35:$f | sed -n '1p'; done
sed -n '128,136p;170,201p' corpus/lessons/round-17.md
sed -n '76p' /home/vgpnk/Projects/shokunin/.ufo/reports/round-17/mado.md
sed -n '16p' corpus/lessons/round-18.md; sed -n '124,152p' corpus/QUALITY.md
```
