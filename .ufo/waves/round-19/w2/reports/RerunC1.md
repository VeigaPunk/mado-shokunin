# MadoR19.RerunC1 — partial

Attack target: C1, the calibration literal QUALITY lesson-citation fraction
`18/26 → 20/28`, with target `≥21/29` declared and missed, plus its two new
runnable-check claims (QUALITY 27 `anchor-durability.py`, 28 `supersede-sweep.py`).
Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, tip
`01b80946d92b26370d3012a7da655d00dd135154` (HEAD; tracked worktree had no
modifications at my run time — a sibling seat added 38 lines to `SCORECARD.md` at
15:07:07 -0300, one minute after my last snapshot; every number below is read from
committed bytes via `git show REV:path`, not from that file), baseline
`9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`.
Run at 2026-10-20T18:06Z, Python 3.14.8. Host pause respected: file bytes and
`git show` only; no gate, no package tool, no jj, no service/compositor call.

**Verdict in one line:** the `c1` counts are exact and the instrument is
byte-identical at both revisions; both criteria cite `lessons/round-19.md`
`## Mistakes` ids that exist; both checks reproduce their red/green tokens and
exit codes at the named revisions and at the integrated tip. `partial` is for two
evidence-scope defects that the green claims do not disclose: (F1)
`supersede-sweep` credits `POINTED corpus/README.md` from a pre-existing upstream
contract line whose `S090` arrives only through a `S072–S091` span, so `pointed=13`
is not 13 substantive pointers; (F2) criterion 27's "superseding row names the
replaced id" clause is not exercised by its checker (manually true today).

## 1. Instrument identity — `de4c422b…` at both revisions (holds)

```
$ git show 9c54c56:.ufo/waves/round-17/measure.py | sha256sum
de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc  -
$ git show 01b80946:.ufo/waves/round-17/measure.py | sha256sum
de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc  -
$ sha256sum .ufo/waves/round-17/measure.py
de4c422b… (same bytes; git blob fc06e54f…, mode 100755 at both revs)
```
So the two runs below used identical instrument bytes; the difference is the
revision argument only. `git status --porcelain` shows no tracked modification, so
the worktree copy is the committed copy.

## 2. c1 counts (hold exactly)

```
$ python3 .ufo/waves/round-17/measure.py 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
"c1": {"criteria": 26, "lesson_cited": 18, "score": 6.9231}
$ python3 .ufo/waves/round-17/measure.py 01b80946d92b26370d3012a7da655d00dd135154
"c1": {"criteria": 28, "lesson_cited": 20, "score": 7.1429}
```
10*20/28 = 7.14286 → 7.1429; 10*18/26 = 6.92308 → 6.9231. Arithmetic checks.
(`c3.sha256` differs between the runs — `c1ae45a7…` → `367be947…` — because
`tools/mado-tripwire.py` moved; that is C3's axis, not a c1 inconsistency.)

Hand count, committed bytes:

```
$ git show 01b80946:corpus/QUALITY.md | grep -cE '^[0-9]+\. '          -> 28
$ git show 01b80946:corpus/QUALITY.md | grep -E '^[0-9]+\. ' | grep -c lessons/  -> 20
$ ... | grep -v lessons/    -> criteria 1,2,3,4,5,18,19,20
$ git show 9c54c56:corpus/QUALITY.md | grep -cE '^[0-9]+\. '           -> 26
$ ... | grep -c lessons/                                              -> 18
$ ... | grep -v lessons/    -> criteria 1,2,3,4,5,18,19,20
```
The uncited set is identical at both revisions; the delta is exactly the two new
criteria 27 and 28, each cited on its own line (`corpus/QUALITY.md:174`, `:183`).
Numbered lines at tip are exactly 1..28 with no indented/bold variant missed
(`grep -oE '^[0-9]+\.'` → 1 2 … 28).

## 3. Criteria 27/28 citations resolve (hold)

`corpus/lessons/round-19.md` has `## Mistakes` at `:12` and rows
`| M1 |`–`| M9 |` at `:16`–`:24`. Criterion 27 cites `#mistakes M1/M2`
(`QUALITY.md:174`, M1 row `:16` = S094 reference-drift/R18-V1, M2 `:17` = S084
unpinned-alias/R18-V4); criterion 28 cites `#mistakes M3` (`QUALITY.md:183`,
M3 row `:18` = the ConnStalePinsSweep landing failure/R18-V3). A scripted
resolution of all 20 literal citations (file exists at tip, `## Mistakes` section
exists, each named `M\d+` row present, each `path:line` range within the file)
returned `BAD: none`.

Baseline line anchors in the lesson also check out: `9c54c56:corpus/SOURCES.md:96`
is the S084 row and `:106` is the S094 row (M1/M2 pointers); M3's
`SKILL.md:1822` at `9c54c56` is the round-18 `ConnStalePinsSweep` erratum line.

## 4. QUALITY 27 `anchor-durability.py` red/green (reproduces)

```
$ python3 -I .ufo/waves/round-19/anchor-durability.py 9c54c56
ROW S084 UNPINNED_ALIAS — source path segment latest and anchor names no 40-hex commit, tag or dated version; also sha256 0291cfe6… is a page digest, not shown to rotate (receipts: 6 records, 1 digests)
ROW S094 PER_FETCH_DIGEST — 5 distinct 200 digests for https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black (3b18a612… ≠ 50c1ac25…; matched by credited digest 50c1ac25…)
SUMMARY rev=9c54c56… mined=80 durable=78 per_fetch_digest=1 unpinned_alias=1 flagged=2 receipt_files=49 bad_receipt_lines=0
FLAGGED S084 S094
rc=1
$ python3 -I … 01b80946
SUMMARY rev=01b80946… mined=81 durable=81 per_fetch_digest=0 unpinned_alias=0 flagged=0 receipt_files=57 bad_receipt_lines=0
rc=0
```
`df84807` also prints `flagged=0`, rc=0. The QUALITY parenthetical "5 receipts /
5 digests" is exact for the exact tree URL: independent recount over committed
`round-1[0-9]/fetch/*/receipts.jsonl` at `9c54c56` gives 5 records with
`http_status==200`, 5 distinct `sha256` (across
`MadoR18.ReviewSourcesRows`, `NoteTheme`, `ReopenS094`×2, `ReviewThemeUpstream`
receipt files). Instrument bytes are unchanged `df84807 → 01b80946` (git blob
`f15279e1…`; sha256 `9e66dce8…` = worktree copy).

Replaced-id clause, read manually (the checker does not test it — F2):
`corpus/SOURCES.md:109` S097 title "… (supersedes S094)"; `:110` S098 evidence cell
begins "supersedes S084 — walker calls `xdg::BaseDire…"; S084 (`:96`) and S094
(`:106`) are `rejected` at tip. So the sentence's claim holds today.

## 5. QUALITY 28 `supersede-sweep.py` red/green (reproduces)

```
$ python3 -I .ufo/waves/round-19/supersede-sweep.py 9c54c56
supersede-sweep: walker-2.17.2 rev=9c54c56… files=13 pointed=2 stale=11   (stderr)
POINTED corpus/README.md ; POINTED corpus/knowledge/walker-route-r18.md ; 11× STALE
rc=1
$ … df84807   -> files=13 pointed=13 stale=0, rc=0
$ … 01b80946  -> files=13 pointed=13 stale=0, rc=0
```
Instrument bytes unchanged `df84807 → 01b80946` (blob `486e7917…`; sha256
`fd7c31df…`). Denominator 13 reproduces; the scope is the ledger's five globs
(`.ufo/waves/round-19/supersessions.json`, rows S090/S096).

## 6. Finding F1 — `pointed=13` includes one line-rule artifact (README)

Enumerating every line that the sweep's own `pointed()` accepts, at both revs:

```
9c54c56:  SKILL.md [] ; README.md [44] ; route-r18.md [1] ; other 10 files []
01b80946: SKILL.md [573,1853,1855,1856,1858-1865] ; README.md [44] ;
          route-r18.md [1,328] ; each knowledge note [one new line, e.g. 392/299/1009/338/403/622/305/479/467] ;
          tools/mado-verify.sh [56,101,1258,1920,3285]
```
`corpus/README.md:44` is the round-18 knowledge-map row — "Documentary upstream
contract for Walker v2.17.2 …" with the row's source span `S072–S091`; the
`S090` credit comes only from that span and the `2.17.2` is the *upstream* contract
version, not the host pin. The line is unchanged from baseline. README's actual
round-19 pointer is split across physical lines: `:137` "walker's **binary bytes**
are a mined host row (S096: digest, package `desc`" / `:138` "`2.17.2-1`,
compiled-in literal `2.17.2` at offset 856,302), and the 13 owned" — no single
line carries both, so the checker never sees it.

Consequences, stated at their true strength:
- The green is a real checker output (rc=0), and README still complies on a human
  reading of `:134–141` (it names S096, `2.17.2-1`, and the superseded `2.17.0`
  mentions); the file's state is not false. This is a check-proxy gap, the class
  the QUALITY 28 Limit line already concedes, but a *pre-existing-line* instance
  it does not name.
- The same artifact inflates the baseline: `walker-route-r18.md:1` qualifies only
  because its `source:` list enumerates S072…S091 (including S090) next to
  `v2.17.2` upstream URLs. Neither of the two baseline `POINTED` files carried a
  pointer to the host supersession, so under criterion 28's wording the pre-state
  was 0/13, not 2/13. Lesson M3's "11 of 13 owned files still stated walker
  `2.17.0` with no in-file pointer" therefore counts two files as pointed that were
  not; the defect was larger than recorded, and the `2 → 13` move includes two
  no-op credits at the baseline end. This is C2's denominator, but criterion 28's
  red sentence is the evidence under attack and it inherits the number.
- The checker also accepts a span that happens to cover S090/S096 on any line, so
  a future unrelated `S072–S091` citation clears a file again.

## 7. Finding F2 — criterion 27's replaced-id clause is not checked

`anchor-durability.py` screens anchor durability only (UNPINNED_ALIAS /
PER_FETCH_DIGEST over `mined` rows). Nothing in it resolves "the superseding row
names the replaced id". QUALITY 27's Limit line (`corpus/QUALITY.md:181-182`)
mentions only anchor-text reading and single-fetch pages, so the green reads as
covering the whole numbered sentence when it covers two of its three clauses.
Today the third clause is true by inspection (§4); it is a coverage overclaim,
not a false statement, and it would silently stay green if S098 lost the phrase.

## 8. Adjacent observations (not used to grade C1)

- N1, criterion 24 self-application: `.ufo/waves/round-19/evidence/` at tip holds
  8 files (`census-before.txt`, `fresh-pins-before{,-recut}.txt`,
  `gate-swap-d9a5a18.sh`, `gate-swap-receipt.txt`, `measure-before.json.txt`,
  `tw-recall-before{,-recut}.txt`); none is produced by the two new checkers
  (`git grep -l 'anchor-durability\|supersede-sweep' -- '.ufo/waves/round-19/evidence/*.txt'`
  → no hits). Criteria 27/28's red/green are narrated reruns in QUALITY/lesson.
  The same round's R18-V2 note disciplines criterion 26's evidence with criterion
  24; the new criteria's evidence has no `tool_sha256=`/`measured_commit=` receipt.
  Both runs are reproducible by rerun (this report), so the numbers are not in
  doubt — the receipt shape is.
- N2, QUALITY 22 (literal vs semantic): semantic count (citation anywhere in the
  criterion block, including continuation lines) is 23/28 at tip vs 21/26 at
  baseline; criteria 18, 19, 20 cite only on continuation lines. The round-19
  lesson (`corpus/lessons/round-19.md:63`) says only "C1 therefore misses its
  pre-registered ≥21/29 target"; the achieved `20/28 = 7.1429` appears in the
  committed `w1/reports/CriticC1.md:118` but not in QUALITY/LOG/SCORECARD. Under
  the semantic rule 23/28 exceeds 21/29, so the miss is literal-rule-only; the
  declared axis is literal (`SCORECARD.md:1072`, `:1098`), so the miss statement
  is honest, but the round-19 record I read does not carry the second counter
  QUALITY 22 asks to report separately.
- R18-V2 note spot-check: `gate-swap-receipt.txt:1` carries
  `tool_sha256=6e6782c3…` equal to `git show df84807:.ufo/waves/round-19/evidence/gate-swap-d9a5a18.sh | sha256sum`
  (and identical at tip), `measured_commit=df84807…`; the failed list is R10 plus
  five OM9 bullets (6 failed, 383 passed), matching the note's "five OM9
  assertions plus R10". `receipt-check.py .ufo/waves/round-19/receipt-claims.json`
  prints `EXPECT_SUMMARY: 3/5` — the two `MISSING_PROVENANCE` claims the note cites,
  plus two `ERROR` claims that lesson M5 documents.

## Limits

- Did not run the gate or its fixture, any package/service/compositor command, or
  jj; no network fetch. C3/C2 counters were not re-run except as they bear on
  criterion 28's scope.
- The checkers were executed as the worktree copies; I verified those bytes are
  identical to the committed blobs at `df84807` and `01b80946` (sha256 above), so
  the results are revision-bound.
- README's compliance under criterion 28 is my reading of a wrapped paragraph,
  not a checked property; F1 states exactly what the checker does and does not
  establish.
- `[INFERENCE]` that a span-citation clearing a file is unintentional; I can show
  the credit path, not the author's intent. `[UNK]` whether a wave-1 reviewer
  already read README:44 as a pointer (CriticC1 documents only the bare-line
  mutant).
- The lane's other wave-2 seats are writing untracked reports under
  `.ufo/waves/round-19/w2/`; nothing there was read or relied on. A sibling
  modified the tracked `SCORECARD.md` (`git status`: ` M SCORECARD.md`, +38/-0,
  mtime 15:07:07 -0300) after my measurement snapshot; it is not my change and no
  evidence here depends on the worktree copy of it — committed `01b80946:SCORECARD.md`
  is what I quoted (`:1072`, `:1083`, `:1098`).

## Installs

none
