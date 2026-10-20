# MadoR18.W3NumbersAudit — round-18 number/hash audit at `a210241`

Seat: `MadoR18.W3NumbersAudit` (residual non-author check, wave 3).
Target: `a210241b5429fb3c3f9ad23f42863d6e6d9e5845` (branch `master`), read
only. Baseline `d9a5a18`, integration `4c103b5`, receipts `abfbf35`,
wave-2 integration `be886a3`. All lane reads are `git show a210241:…` or a
clean clone at `a210241` (`/tmp/mado-r18-a210241`); the lane worktree was
**not** used as evidence (see § Worktree condition).

**Verdict.** Every tool sha, measure value, selftest count, suite count,
row/tier/mined count, fetch digest and GATE-line hash/byte/word count in
`SCORECARD.md` § Round 18 results, the `LOG.md` round-18 entry and
`corpus/lessons/round-18.md` (M1–M8, Gate, Wave-2 corrections) reproduces at
`a210241`. No wrong arithmetic, no fabricated digest, no stale tool identity
was found. One medium claim-scope defect (`SCORECARD.md:991-992`), one
low-medium registry number outside the three target docs
(`SKILL.md:566`), and three low wording/scope mismatches are listed below;
the rest are residual risks, not receipt contradictions.

## Findings (by severity)

### F1 — MEDIUM — `SCORECARD.md:991-992` states a universal receipt-header rule that the cited receipts do not meet

Committed text (`git show a210241:SCORECARD.md | nl -ba | sed -n '991,992p'`):

```
991  (`evidence/final/measure-final.json.txt`; identical c1/c2). Every receipt's first
992  line names `tool_sha256` and `measured_commit` (QUALITY 24).
```

The three receipts named in the immediately preceding clause **do** comply
(`measure-before.json.txt`, `measure-after.json.txt`,
`evidence/final/measure-final.json.txt`: each first line is
`RECEIPT tool=.ufo/waves/round-17/measure.py tool_sha256=de4c422b… measured_commit=…`).
Read as the universal the sentence states (and as the round's M1 /
QUALITY 24 target), it is false for receipts cited in the same table:

| cited artifact | first line | `tool_sha256`/`measured_commit` |
|---|---|---|
| `.ufo/waves/round-18/evidence/measure-mutants.json` (criterion 25, `SCORECARD.md:996`) | `{` | **0 occurrences** (`grep -c 'tool_sha256\|measured_commit'` → `0`) |
| `.ufo/waves/round-18/evidence/final/recut-summary.json` (C3, `:998`) | `{` | present as JSON keys, not first line |
| `.ufo/waves/round-18/evidence/final/tripwire-pacmanlog-join.txt` (M1, lesson `:16`) | `# Round-18 C1 re-derivation…` | no `RECEIPT` header; the lesson itself calls it a hand-authored join |
| `.ufo/waves/round-18/evidence/gate-rc-redbefore.txt` (criterion 26, `:996`) | `# gate-rc-redbefore …` | 0 occurrences of either token |
| `.ufo/waves/round-18/evidence/regression-recut.txt` (M3/PIN, `:996`) | `# regression-recut …` | 0 occurrences of either token |

Quantified: of the 27 files under `evidence/final/`, 23 begin with `RECEIPT`
and 4 do not (`harm-watch-pins.txt`, `harm-watch-summary.txt`,
`recut-summary.json`, `tripwire-pacmanlog-join.txt`).

The material consequence is criterion 25, not the narrative lab files.
`measure-mutants.json` (committed at `a210241`, `generated_at`
`2026-10-20T15:50:02+00:00`, `baseline_rev` `d9a5a18`) names its producer only
as `harness.sha256 = 075815bd5bbcf80fbf00a80ac9400ff9ec82082562a6691c1f5cc290da601d73`
plus `harness.path`/`argv`. That sha **is** `.ufo/waves/round-18/measure-mutants.py`
at `4c103b5`/`abfbf35`/`be886a3`, but the script is **absent at the receipt's
`baseline_rev`**:

```
$ for rev in d9a5a18 4c103b5; do git cat-file -e "$rev:.ufo/waves/round-18/measure-mutants.py" \
    && echo "$rev present" || echo "$rev absent"; done
d9a5a18 absent
4c103b5 present
```

So the QUALITY-24 formula `tool_sha256 = sha256(git show <measured_commit>:<tool>)`
cannot be formed from the receipt as written; the `harness.sha256` is not a
`tool_sha256` bound to a `measured_commit`. QUALITY 25's own requirement
(instruments by sha256, each mutant by diff digest) is met — the JSON's
`instruments.loose`/`instruments.tight` and `mutants[].diff_sha256` are
present and the rerun reproduces 6/6 — but the receipt is not producer-bound
under QUALITY 24.

**Status at `a210241`:** unfixed. The worktree contains an **uncommitted**
W3CriticC1Final correction to this sentence (worktree `SCORECARD.md:1037-1046`)
that calls it "too broad" and lists the same files as "provenance only"; that
text is not in `a210241` (committed `SCORECARD.md` is 1030 lines, 0
`W3Critic` occurrences). If that correction lands, the criterion-25 receipt
still lacks the header and the 33/33 claim in the correction is not the
committed claims file (see § Worktree condition).

### F2 — LOW-MEDIUM — `SKILL.md:566` says "17 mode-frozen cases"; the committed suite has 31

`git show a210241:SKILL.md | nl -ba | sed -n '566p'` contains:

```
| mado-tripwire-frozen | gate | … --selftest .ufo/waves/round-18/tripwire/frozen (17 mode-frozen cases; exit and first-line outcome) …
```

Committed evidence:

```
$ python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-18/tripwire/frozen
SELFTEST_SUMMARY: 31/31 passed failed=[]
$ git ls-tree -r --name-only abfbf35 .ufo/waves/round-18/tripwire/frozen | \
    awk -F/ '$7=="expected.json" && NF==7' | wc -l
17
```

The suite was 17 case directories at `abfbf35` and is 31 cases at `a210241`
(30 `expected.json` dirs + the `symlinked-frozen-dir` case). `SCORECARD.md:998`
and lesson `:98` both say 31, so the registry row is the stale number. The
worktree has an **uncommitted** erratum (worktree `SKILL.md:1831-1843`,
W3CriticC3Final) correcting 17 → 31; it is not in `a210241` (committed
`SKILL.md` has 0 `W3CriticC3Final` occurrences). The row is outside the three
target documents, but `LOG.md:1301` claims the registry row as a delivered
artifact, so the committed registry number is part of the round's state.

### F3 — LOW — `SCORECARD.md:997` "95 digest-only" mixes two scopes; the retention split is 103

`SCORECARD.md:997` says "329 licensed bodies committed, 95 digest-only; fresh
clone `fetch-verify` exit 1 …". At `a210241`:

```
RETENTION.json summary: {"bodies":432,"commit":329,"digest_only":103,...}
fetch-verify SUMMARY: receipts=424 ok=329 bad=0 digest_only=95 non200=0
                      conflicts=4 rows=24 unreceipted=0
```

`95` is fetch-verify's count over 424 receipt lines; the retention manifest
has 103 digest-only entries. The 8-entry difference is exactly the
digest-only entries with no receipt line:

```
MadoR18.SrcWalkerThemes/walker-ls-remote-v2.17.2.txt
MadoR18.SrcWalkerThemes/walker-tree-api.json
ReopenS086/commit, ReopenS086/omarchy-v3.8.4-bin-omarchy-launch-walker, ReopenS086/redirect
ReopenS089/git-ls-remote-v3.8.4.txt
SrcOmarchyThemeHooks/tree.json
SrcOmarchyWalker/git-ls-remote-tags.txt
```

`corpus/lessons/round-18.md:103-104` labels 95 as the fetch-verify number and
`:106` labels 103 as the retention number, so the lesson is consistent; the
SCORECARD's unlabelled pair can be read as the retention split and is then
off by 8. No fetched body is missing: fetch-verify re-hashes 329/329 and
gitleaks over the committed fetch set is clean (see § Passed checks).

### F4 — LOW — lesson `M8` (`corpus/lessons/round-18.md:23`) says "`session_exit` 16:15:47Z in each transcript"; one of the twelve is 16:15:48.174Z

Committed transcripts
(`/home/vgpnk/.omp/agent/sessions/…/MadoR18/MadoR18.<seat>.jsonl`) give:

| seat | `session_exit.recordedAt` |
|---|---|
| FetchBodyPolicy | 2026-10-20T16:15:47.339Z |
| GateRerun | 16:15:47.343Z |
| ReviewWalkerUnknowns | 16:15:47.358Z |
| ReviewQuality2426 | 16:15:47.365Z |
| ReviewLesson18 | 16:15:47.370Z |
| ReviewSkillRegistry | 16:15:47.376Z |
| ReviewGateDiff | 16:15:47.382Z |
| ReviewTripwireDiff | 16:15:47.387Z |
| ReviewFrozenExpected | 16:15:47.391Z |
| RevengeOldWalkerNotes | 16:15:47.413Z |
| TwFrozenHarden | 16:15:47.924Z |
| **FetchVerifyFix** | **16:15:48.174Z** |

The L1 session's own `session_exit` is `16:15:48.181Z`. The counts 14 = 2 + 12
are correct (73 w2 members, 59 report files, 14 missing reports), and the two
named 429 seats are correct (CriticAdmission `status="failed (exit 1)"`,
`[anthropic/claude-opus-5-5] 429 {"type":"error","type":"rate_limit_error",…}`;
CriticHonestyW2 `errorStatus=429`), but "each transcript" is true to the
second for 11/12, not 12/12. Low severity: one-second boundary.

### F5 — LOW — lesson `:62` GATE S082 says "3/3 wave-1 receipts"; one of the three is a wave-2 seat

The seat's own report (`w2/reports/ReopenS082.md:21-24`) lists the three as
`NoteWalker`, `SrcElephantProviders`, **`ReviewWalkerUpstream`**. The wave
records at `a210241` put `ReviewWalkerUpstream` in wave 2, not wave 1:

```
$ python3 -c "import json;print('ReviewWalkerUpstream' in json.load(open('.ufo/waves/round-18/w2/record.json'))['members'])"
True
$ python3 -c "import json;print('ReviewWalkerUpstream' in json.load(open('.ufo/waves/round-18/w1/record.json'))['members'])"
False
```

The count of three agreeing receipts is right (all `9283 B` / `c1c2ecaa…`);
only the wave label is wrong. The lesson copies the seat's verbatim GATE line,
so this is a report-level label, not a count fabrication. Same class, no
count error: `S080` says "all 5 receipts" and the tag URL has exactly 5
receipt lines (the 6th same-sha line is the commit-pinned URL, not the same
URL); `S092` says "three seats" and the three named seats agree (a later
wave-2 seat adds a fourth fetch, which does not falsify "across three").

### F6 — LOW (wording) — two C1-row claims are narrower/more precise in the underlying reports than in `SCORECARD.md:996`

1. "MutGateOM 8/8 killed": the report headline is "8 KILLED, 0 SURVIVED,
   0 INCONCLUSIVE" (`w2/reports/MutGateOM.md:18`), but mutant `m07-z-arm-first`
   is recorded "KILLED by pin only; behavioral slice SURVIVED"
   (`MutGateOM.md:69`). The detector verdict is 8/8; the behavioral slice did
   not survive detection but was not covered. No number is wrong; the
   unqualified "8/8 killed" hides the one pin-only kill.
2. "`STALE`/`SHA_MISMATCH` controls": the committed claims file has 2
   `SHA_MISMATCH`, 1 `STALE`, **1 `NOT_ANCESTOR`, 1 `PRODUCER_MISMATCH`** and
   10 `ok`. The sentence names three of the five control statuses; not false,
   incomplete. The lesson's Wave-2 block (`:92-94`) names all three added
   checks correctly.

### F7 — LOW (wording) — "real-transcript re-cut identical" means content identity, not byte identity

`SCORECARD.md:998` "real-transcript re-cut identical" and lesson `:100`
"all identical" match `recut-summary.json`'s `all_receipts_identical: true`,
but that field is computed from exit, verdict line, counts, file list,
findings multiset, permitted list and `receipt_header_ok` — not raw bytes
(`recut-receipts.sh:419-433`). The summary itself records different receipt
sha256 for every pair, because the new `RECEIPT` header was added:
r13 `3abb24a1…` → `39de9f62…`; r14 `bd55e901…` → `1306d2c4…`;
r15 `23d7f49d…` → `ce2bd57b…`; r16 `5664584b…` → `3bbf7095…`;
anchor `d1db10cf…` → `2dadd4cc…`. Findings/counts/verdicts are identical
(33/50/209/2/8 findings; exits 1/1/1/1/1), and the header is the M1 fix, so
byte difference is intended. "Identical" needs the word "content" or
"counts/findings".

### F8 — INFORMATIONAL — S090's GATE digest `f34d34e7…` no longer matches the live log; it reconstructs exactly

`corpus/lessons/round-18.md:70` GATE S090 gives `/var/log/pacman.log` sha256
`f34d34e72702c94e29213c2eaed3bb8f3947f1a224acefa5ebf3a5c635741e76`,
7 anchors, access 2026-10-20 (read at ~15:59Z = 12:59 -03). The live file is
now `244,858 B / 27bbd0b5…`, because the 13:23 -03 `pacman -U zcode`
transaction (lines 3161-3169, documented at `SCORECARD.md:1009-1012`)
appended 754 bytes after the read. Deleting exactly lines 3161-3169 from a
copy reproduces the GATE receipt:

```
$ cp /var/log/pacman.log /tmp/pacman-now.log && sed -i '3161,3169d' /tmp/pacman-now.log
$ wc -c /tmp/pacman-now.log; sha256sum /tmp/pacman-now.log
244104 /tmp/pacman-now.log
f34d34e72702c94e29213c2eaed3bb8f3947f1a224acefa5ebf3a5c635741e76  /tmp/pacman-now.log
```

So the receipt was true at access time; no mismatch. A re-checker must apply
the documented transaction, not hash the live file. The five anchors
(1943, 2929, 3062, 3095, 3123) are verbatim as claimed.

### F9 — RESIDUAL WORDING — S094's row still says "the only theme on this host"; the note defines it as "only *applied*"

`corpus/SOURCES.md:106` (a210241) retains the scope clause
"…(the only theme on this host)". Lesson `:74` GATE S094 flags "the scope's
false 'only theme'"; lesson `:88` records the qualification in the note's
Wave-2 block, and the note now defines it at
`corpus/knowledge/theme-route-r18.md:162`: `"the only theme on this host"
(S094 scope) means the only *applied* theme`. The credited note is therefore
qualified; the row cell alone is not. The planned round-19 superseding row
(`SCORECARD.md:1027-1028`) covers the HTML digests, not this wording. No hash
or count is affected.

### F10 — NOTE — worktree condition (not part of `a210241`)

At review time `git status --porcelain` in the lane showed:

```
 M .ufo/waves/round-18/receipt-claims.json
 M SCORECARD.md
 M SKILL.md
?? .ufo/waves/round-18/w3/
```

These are other W3 seats' in-flight edits. They are **not** in `a210241`
(committed `SCORECARD.md` 1030 lines, `SKILL.md` 1829 lines,
`receipt-claims.json` 21 claims). The worktree `receipt-claims.json` currently
has 33 claims, and the uncommitted SCORECARD correction says "33/33"; at
`a210241` the committed claims file has 21 and the committed checker returns
`EXPECT_SUMMARY: 21/21`, exit 0. If the 33/33 correction is landed, the
33-claim file must be committed with it and the run reproduced from the
committed file; otherwise the correction's number is not evidence at any
committed revision. I did not treat any worktree byte as evidence.

## Passed checks (what was run, exact outputs)

All commands below ran in `/tmp/mado-r18-a210241` (clean clone, detached at
`a210241`) unless prefixed `git show` from the lane. Tool shas were recomputed
with `git show REV:path > /tmp/f; echo rc=$?; sha256sum /tmp/f`; every git
read exited 0.

### Tool identity

| tool | rev | sha256 | claimed |
|---|---|---|---|
| `tools/mado-tripwire.py` | `d9a5a18` | `962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072` | `962919ce…` (round-17 landed) |
| " | `4c103b5` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `c87a31ef…` |
| " | `abfbf35` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `c87a31ef…` |
| " | `be886a3` / `a210241` | `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd` | `c1ae45a7…` (final) |
| `.ufo/waves/round-17/measure.py` | `d9a5a18`/`4c103b5`/`abfbf35`/`be886a3` | `de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc` | `de4c422b…` unchanged |
| " | `f52f43f` | `a280b3ab7c4dc21a25a954056f6a0c55187fd84dc06cfcddcb28e7f897d3508e` | loose instrument `a280b3ab…` |
| `tools/mado-verify.sh` | `d9a5a18` | `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207` | `fba82a66…` |
| " | `be886a3`/`a210241` | `c9fb0cef3e081dc878d69f8e20c148429bdfbdce949f8afaed705db957ea42b5` | `c9fb0cef…` |
| `PIN_MADO` | `d9a5a18` | `cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96` | `cd1d73d7…` |
| " | `be886a3` | `20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744` | `20714096…` |

`git diff --name-only be886a3 a210241 -- tools/ .ufo/waves/round-18/*.py .ufo/waves/round-18/fetch/`
is empty: `a210241` adds 31 evidence/doc files only, so the final tool shas
are the `be886a3` shas.

### Measure / calibration

```
$ python3 .ufo/waves/round-17/measure.py <REV>   # parsed JSON, header dropped
d9a5a18  c1 {criteria:23, lesson_cited:15, score:6.5217}  c2 {count:4, score:6.6667, u_routes:7}
4c103b5  c1 {criteria:26, lesson_cited:18, score:6.9231}  c2 {count:6, score:10.0, u_routes:7}
be886a3  c1 {criteria:26, lesson_cited:18, score:6.9231}  c2 {count:6, score:10.0, u_routes:7}
```

`18/26×10 = 6.9231`, `15/23×10 = 6.5217`, delta `0.4014`; `4/6×10 = 6.6667`.
Independent semantic-block parse of `corpus/QUALITY.md` (numbered block
contains `lessons/` on any line): `d9a5a18` 23 criteria / 18 semantic / 15
literal; `be886a3` 26 / 21 / 18 → `18/23 → 21/26`. `QUALITY.md:131/138/144`
contains criteria 24/25/26 at `a210241`.

### receipt-check (criterion 24)

```
$ python3 .ufo/waves/round-18/receipt-check.py     # committed 21-claim file
RECEIPT r17-tripwire-r13 MISSING_PROVENANCE  (×6: r13,r14,r15,r16,anchor,pacmanlog-join)
RECEIPT r18-fixture-bad-sha SHA_MISMATCH
RECEIPT r18-fixture-stale-rev SHA_MISMATCH
RECEIPT r18-fixture-stale-tool STALE
RECEIPT r18-fixture-nonancestor NOT_ANCESTOR
RECEIPT r18-fixture-producer-mismatch PRODUCER_MISMATCH
… 10 r18 receipts ok …
EXPECT_SUMMARY: 21/21
exit 0
```

Historical red reproduced in the clone at `abfbf35`:
`python3 .ufo/waves/round-18/receipt-check.py` → `EXPECT_SUMMARY: 9/15`,
`rc=2`, 6 `PENDING` — matching the C1 row's "24 was not green at `abfbf35`
(… PENDING claims)".

### fetch / retention / rows (C2)

Clean clone at `a210241`:

```
$ python3 .ufo/waves/round-18/fetch-verify.py --sources corpus/SOURCES.md \
    --rows S072,…,S095
ROW S072 receipted … ROW S089 receipted … ROW S094 receipted   (21/21 web rows)
ROW S090 host/no-url ; ROW S091 host/no-url ; ROW S095 host/no-url
CONFLICT https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black            (×2 hosts)
CONFLICT https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black/backgrounds (×2 hosts)
SUMMARY receipts=424 ok=329 bad=0 digest_only=95 non200=0 conflicts=4 rows=24 unreceipted=0
exit 1
```

The 4 conflicts contain the M7 digests `50c1ac25…` and `9e1160a0…`.
`RETENTION.json`: 432 bodies, 329 commit (3,512,679 B), 103 digest-only
(10,856,600 B); by class `raw-pinned` 296 + `api-pinned` 19 + `license` 14 =
329 commit; 52 html + 11 http-error + 10 archive + 10 unreceipted + 5 archwiki
+ 5 third-party + 4 unlicensed-text + 4 aur + 2 unpinned = 103 digest-only.
`fetch/.gitignore` has 104 lines (1 comment + 103 paths). All 49
`fetch/*/receipts.jsonl` files parse; 424 receipt lines.
`gitleaks detect --no-git --source=.ufo/waves/round-18/fetch` over the clean
clone: "no leaks found" (the lane worktree scan finds 90 because the untracked
digest-only HTML bodies are present there; those are not committed).

Row/tier/status counts (`git show REV:corpus/SOURCES.md`, field parse):

```
d9a5a18: 71 rows  tier A 64 / B 1 / C 6   mined 56 / queued 8 / rejected 7
be886a3: 95 rows  tier A 88 / B 1 / C 6   mined 80 / queued 8 / rejected 7
```

All 24 new rows S072–S095 have `opened=2026-10-20`; recheck values are
S072 `on-change`, S073–S084 `on-release`, S085–S091 `on-change`,
S092–S094 `on-release`, S095 `90d` — exactly lesson `:77-81`.

### GATE lines (24/24)

All 24 lesson lines `- GATE | S0NN | …` are byte-identical (after stripping
the leading `- `) to the single `GATE | S0NN | …` line in the corresponding
`w2/reports/ReopenS0NN.md`: 24/24 exact, 0 `disagree`. For every web row the
GATE sha256 is present both in that row's `SOURCES.md` anchor cell and in a
200 receipt; the quote word counts match a whitespace split 24/24
(`S075` 6, `S082` 1, `S084` 8 verified with the pipe-aware parse). Byte
counts checked: S072 7,926; S073 13,743 B / 305 lines; S075 26,673;
S076 26,338 (4 receipts incl. commit-pinned); S077 9,364; S078 952;
S079 165,438; S080 6,969 (5 tag-URL receipts); S081 2,552; S082 9,283;
S083 3,609 (3 wave-1 receipts); S084 105,537; S085 1,336; S086 412;
S087 709; S088 893; S089 138 + 38 (11 receipt lines across 4 seats);
S091 13,743 (embedded once in `/usr/bin/walker` at offset 806,960);
S092 1,124/1,026/21,390/3,993 (4 anchors, 4 seats); S093 742; S094 461;
S095 host hashes `48749715…`, `55fa691a…`, `481267af…`, `b8d173…`.

Reproduced M1: `f71ccbe` tool (`7a98720e…`) on the 30-case
`round-17/tripwire/w2-regressions` suite → `28/30` (fails
`quoted-hash-not-comment`, `escaped-hash-not-comment`); `0ab1ccc` tool
(`962919ce…`) → `30/30`. `MadoR17.jsonl` line 539 timestamp is exactly
`2026-10-20T15:17:25.987Z`; the six round-17 receipts at `d9a5a18` contain
0 hits for `tool_sha256|measured_commit|962919ce|7a98720e`.

### C3 / frozen / gate

```
$ python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-18/tripwire/frozen
SELFTEST_SUMMARY: 31/31 passed failed=[]
$ python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen
MADO_TRIPWIRE_FROZEN: frozen_match   exit 0
$ bash tools/mado-verify.sh --selftest
MADO_SELFTEST: 389/389 assertions passed   exit 0
```

`frozen/expected.json`: 8 findings, 3 known misses. `tripwire-frozen-before.txt`:
`--frozen` usage `could_not_evaluate` exit 2 with the `d9a5a18` tool
`962919ce…`. `tripwire-frozen-tampered.txt`: one-byte append →
`snapshot_tampered`, exit 2. `tripwire-frozen-selftest-redbefore.txt`:
`abfbf35` tool `c87a31ef…` → `17/31 passed`, 14 failed. `frozen-provenance.txt`:
`MADO_FROZEN_PROVENANCE: match`, exit 0, 228 indexed sources. Case-directory
count: 17 at `abfbf35`, 31 at `a210241`. OM9/OM10 contain exactly 17
`st_*` assertion calls (OM9 8 + OM10 9); `git diff d9a5a18 be886a3 -- tools/mado-verify.sh | grep -c '^-.*st_'`
= 0, so "none dropped". `regression-recut.txt`: 10/10 KILLED, kill-rate
100%, `PIN_MADO cd1d73d7… → 20714096…`; `w2-gate-regression.txt` is
`MADO_REGRESSION: PASS` with target sha `20714096…`; `w2-gate-selftest.txt`
is `389/389`, header bound to `c9fb0cef…` at `abfbf35`.

### Harm watch (at `be886a3`)

`harm-watch-summary.txt`: 11 commands, all exit 0, `HARM_WATCH: PASS`.
`harm-gate-selftest.txt` 389/389; `harm-action-plan-selftest.txt` 52/52;
`harm-tripwire-round-17-core` 9/9, `…compound` 16/16, `…hardening` 33/33,
`…w2-regressions` 30/30, `…round-18-frozen` 31/31,
`…round-18-r18-failsafe` 1/1; `harm-measure-u.txt` coverage count 7/7,
score 10.0; `harm-nav-fleet-round-1.txt` `indexed=34/34`;
`harm-census-validate.txt` exit 0 with W04 on S030, S042, S045 (three).
Baseline 372/372 is in `round-17/evidence/harm-legacy-selftest.txt`
(`measured_commit=f71ccbe`), matching "372 → 389 (+17)".

### Seats / host

`w1/record.json` 88 members, 88 report `.md`, 0 missing; `w2` 73 members,
59 reports, missing set exactly the 14 named in M8. `/var/log/pacman.log`
lines 3161 and 3169 are the `pacman -U zcode` / `pacman -D` lines at
13:23:08-09 -03; the round-18 seat scan
`evidence/final/tripwire-r18-seats.txt` is `MADO_TRIPWIRE: clean`, exit 0
(161 seat transcripts, counts all zero).

## Residual risk / verification gaps

- **Worktree is dirty** (F10). Do not treat the worktree SCORECARD/SKILL/
  claims as committed evidence; the committed numbers differ (21 vs 33
  claims; 17 vs 31 case erratum absent/present).
- **Live remote tag state** (`a515085f…` for walker v2.17.2, `8f1e21d6…` for
  elephant v2.22.1, `8fcc9d60…` for omarchy v3.8.4, `a59ea3db…` for swaybg
  v1.2.2) was not re-fetched over the network; I verified the committed
  bodies, receipts and the seats' `ls-remote` outputs. The host pause and
  read-only scope made this a documentary check, not a live one.
- **`mado-verify.sh --regression`** was not rerun by me (it needs the tameshi
  harness and temp trees). I verified the committed `w2-gate-regression.txt`
  receipt fields (tool sha `c9fb0cef…`, target sha `20714096…`, PASS) and the
  committed `regression-recut.txt` 10/10, not a fresh regression run.
- **Frozen provenance** was checked from the committed receipt
  (`MADO_FROZEN_PROVENANCE: match`, 228 sources), not by re-reading all 228
  host transcripts; I read the five input digests and the receipt's pairs
  (5/5/5/6/5 = 26).
- **"Non-author" identity** of the 24 re-open seats is report-declared; I
  verified the 24 GATE lines, their hashes, bytes and word counts, not the
  seats' independence beyond their IDs.
- **Gitleaks version** prints `version is set by build process`; the run is
  the host binary over the committed fetch set only, not over the untracked
  digest-only worktree bodies (which do trip 90 findings on the lane
  worktree; they are not committed).
- **S090's live log** changed after the receipt; the reconstruction in F8
  shows the receipt is exact for the pre-13:23 file. A re-checker must apply
  the documented transaction.
- M1's `tripwire-pacmanlog-join.txt` is hand-authored (lesson says so); it is
  not a tool receipt and was not treated as one.

## Reproduction commands (one-liners)

```bash
# tool shas, with git status checked
cd /home/vgpnk/Projects/shokunin/mado-shokunin
for rev in d9a5a18 4c103b5 abfbf35 be886a3 a210241; do
  git show "$rev:tools/mado-tripwire.py" > /tmp/tw.$rev; echo "$rev rc=$?"; sha256sum /tmp/tw.$rev; done

# clean clone, all final checks
git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mado-r18-a210241
cd /tmp/mado-r18-a210241 && git checkout -q a210241b5429fb3c3f9ad23f42863d6e6d9e5845
python3 .ufo/waves/round-18/receipt-check.py                 # 21/21, exit 0
python3 .ufo/waves/round-18/fetch-verify.py --sources corpus/SOURCES.md \
  --rows S072,S073,S074,S075,S076,S077,S078,S079,S080,S081,S082,S083,S084,S085,\
S086,S087,S088,S089,S090,S091,S092,S093,S094,S095            # 424/329/95/4, exit 1
gitleaks detect --no-git --source=.ufo/waves/round-18/fetch --redact # no leaks
python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-18/tripwire/frozen  # 31/31
python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen             # frozen_match, 0
bash tools/mado-verify.sh --selftest                          # 389/389
```

No lane write was made except this report. No package, service, compositor,
input, screenshot or `jj` command was run; host config was read as bytes only.
No tool was installed or upgraded.
