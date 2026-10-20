# RevengeR17Recut — what round-17's "receipts re-cut" actually did (data only)

Scope: reconstruct the post-P11 re-cut of `.ufo/waves/round-17/evidence/tripwire-*.txt`
from the round-17 lane transcript, and compare it with what commit `0ab1ccc`
recorded. Read-only: transcript read, lane git read-only (`log`, `show`, `diff`,
`ls-tree`, `rev-parse`); no lane file written except this report; no git/jj write,
no package/service/compositor command, no omp process.

## Sources

- Transcript `MadoR17.jsonl` under
  `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/`:
  549 records, 2,811,777 bytes, file mtime `2026-10-20 12:24:56.843 -0300`
  (15:24:56Z), last record `15:24:56.844Z`, session id
  `01a15995-3121-7010-9c4d-7425e31d15e3` (parent `…70c3-…`). Record indices
  below are 1-based line numbers in that file as read.
- Lane git, read-only: commits `988b858`, `f71ccbe`, `6046ab7`, `9bbb881`,
  `0ab1ccc`, `d9a5a18`; `refs/heads/master`.
- Tool shas by revision (`git show REV:tools/mado-tripwire.py | sha256sum`):
  `988b858 4ced68d3…d4c44`, `f71ccbe 7a98720e…f31fe7`,
  `6046ab7 7a98720e…f31fe7`, `9bbb881 7a98720e…f31fe7`,
  `0ab1ccc 962919ce…aaa072`, `d9a5a18 962919ce…aaa072`.

## Timeline (UTC; local = -03, commit timestamps below are git's)

| # | UTC | record | event |
|---|---|---|---|
| 1 | 15:06:41.372 | 464 eval | pre-fix receipt run ("Rerun all receipts with fixed tripwire"); writes selftests, r13–r16, anchor, r17, vs-oracles; tool sha `7a98720e` |
| 2 | 15:06:50.675 | 467 eval | rewrites `tripwire-vs-oracles.json` and `tripwire-r17.txt` |
| 3 | 12:09:20 -03 (15:09:20Z) | commit `f71ccbe` | commits those receipts |
| 4 | 15:09:56.334 | 508 bash | rewrites only `tripwire-r17.txt` (new scan) |
| 5 | 12:10:20 -03 (15:10:20Z) | commit `6046ab7` | commits it (carried unchanged in `9bbb881`) |
| 6 | **15:17:13.800** | **536 eval** | **P11 fix**: `strip_comment()` replaces post-shlex `#` break; 4 regression cases; reruns only the 4 main suites and rewrites their receipts |
| 7 | 15:17:13.802 | (fs mtime) | `tools/mado-tripwire.py` mtime (new bytes on disk) |
| 8 | 15:17:15.674 | 538 result | `core 9/9 compound 16/16 hardening 33/33 w2-regressions 30/30` |
| 9 | 15:17:14.00–15.67 | (fs mtimes) | `tripwire-selftest-{core,compound,hardening,w2-regressions}.txt` rewritten |
| 10 | **15:17:25.987** | **539 eval** | **receipts re-cut**: rewrites w2 adversarial/false-positive, anchor, r13–r16, r17, vs-oracles; prints counts and final tool sha |
| 11 | 15:17:26.5–27.8 | (fs mtimes) | w2, anchor, r13–r16, vs-oracles rewritten |
| 12 | 15:17:29.252 | (fs mtime) | `tripwire-r17.txt` rewritten |
| 13 | 15:17:29.253 | 541 result | printed counts (below); `962919ce…` printed as tool sha |
| 14 | **15:17:36.009** | **542 bash** | SKILL/SCORECARD string replacements, lesson lines appended, `git add -A tools/mado-tripwire.py SKILL.md SCORECARD.md corpus/lessons/round-17.md .ufo/waves/round-17 && git commit … && git push -q && git rev-parse HEAD && git status --porcelain \| head -3` |
| 15 | 15:17:38.585 | 544 result | `0ab1ccccaac5421f6e8ff2fe0cd2bcbd4e5bff4c`, no porcelain lines |
| 16 | 15:17:44.887 → 15:17:46.445 | 545/547 | report HEAD line updated; fleet report commit `16546d0` pushed |

Commit `0ab1ccc` author=committer=`2026-10-20T12:17:36-03:00` (`at=ct=1792509456`),
parent `9bbb881`. The re-cut result (15:17:29) precedes the commit call
(15:17:36) by 6.7 s; the fix precedes the commit by 22.2 s. No tool call
exists between record 541 (re-cut result) and record 542 (commit command).

## What the fix did (record 536)

Three replacements in `tools/mado-tripwire.py`:

- inserted `strip_comment(line)` before `tokenize()`: `#` starts a comment only
  when `i == 0 or line[i-1] in " \t\n;&|()<>"`, scanning with single/double
  quote state and backslash skipping; `tokenize` now calls `line = strip_comment(line)`;
- deleted `if tok.startswith("#"): break  # comment to end of line (a word starting with '#')`;
- changed the `lex.commenters = ""` comment text.

Then it registered four `w2-regressions` cases via `rx(...)`:
`quoted-hash-not-comment` (`echo '# x'; pacman -Syu`, want exit 1, `pacman:-Syu`),
`escaped-hash-not-comment` (`echo \# x; pacman -Syu`, want 1),
`comment-after-separator-is-data` (`ls; # sudo pacman -Syu`, want 0),
`redirect-target-before-command` (`>/tmp/log sudo pacman -Syu`, want 1, `sudo` + `pacman:-Syu`).
It reran the four suites and wrote their receipts. It did **not** touch the
real-transcript receipts (r13–r17, anchor, w2 oracles).

## What the re-cut did (record 539)

Exact operations, in order, all overwriting in place with `Path.write_text`:

1. `--selftest .ufo/waves/round-17/w2/adversarial` → `tripwire-w2-adversarial.txt`;
2. `--selftest .ufo/waves/round-17/w2/false-positive` → `tripwire-w2-false-positive.txt`;
3. `--scan <sess>/MadoR15/MadoR15.LibinputEvents.jsonl` → `tripwire-anchor-r15.txt`;
4. for `rr in (13,14,15,16)`: `--scan <sess>/MadoR<rr>.jsonl <sess>/MadoR<rr>` →
   `tripwire-r<rr>.txt`, and `res[rr] = json.loads(stdout line 2)`;
5. build `T[rr]` from the **new** `res[rr]['findings']` and compare against
   `O[rr]` (oracle sets built earlier from `evidence/oracle-r15.json`,
   `oracle-r16.json`, `oracle-r13-r14.json` by record 336 — not from the
   receipts), then rewrite `tripwire-vs-oracles.json` with a fresh
   `tool_sha256` of the tool file;
6. `--scan <sess>/MadoR17.jsonl <sess>/MadoR17` → `tripwire-r17.txt`;
7. print counts per round, the r17 label/counts/file counts, and
   `hashlib.sha256(tool bytes)`.

Printed in result 541:

```
anchor 1 {'host_mutation': 2, 'live_probe': 1, 'package_query': 5}
13 {'host_mutation': 2, 'live_probe': 12, 'package_query': 19}
14 {'host_mutation': 4, 'live_probe': 0, 'package_query': 46}
15 {'host_mutation': 3, 'live_probe': 29, 'package_query': 177}
16 {'host_mutation': 0, 'live_probe': 0, 'package_query': 2}
r17 MADO_TRIPWIRE: findings {'host_mutation': 0, 'live_probe': 1, 'package_query': 0} 149 139
962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
```

There is no `assert`, no `cmp`, no `diff`, no saved pre-fix copy, and no read of
the pre-fix receipt files anywhere in this call (or between it and the commit).

## What git recorded at `0ab1ccc`

`git show --numstat 0ab1ccc` (vs parent `9bbb881`), evidence paths only:

| file | +/− |
|---|---|
| `tripwire-r17.txt` | 1/1 |
| `tripwire-selftest-core.txt` | 1/1 |
| `tripwire-selftest-compound.txt` | 1/1 |
| `tripwire-selftest-hardening.txt` | 1/1 |
| `tripwire-selftest-w2-regressions.txt` | 6/2 |
| `tripwire-vs-oracles.json` | 1/1 |
| `tripwire-w2-adversarial.txt` | 1/1 |
| `tripwire-w2-false-positive.txt` | 1/1 |

**Not in the commit:** `tripwire-r13.txt`, `tripwire-r14.txt`, `tripwire-r15.txt`,
`tripwire-r16.txt`, `tripwire-anchor-r15.txt`, `tripwire-r17-w1.txt`.

Blob lineage (verified with `git ls-tree`):

- `tripwire-r13.txt`: `988b858 1902d02…` → `f71ccbe 89cfec0…` → `9bbb881 89cfec0…` → `0ab1ccc 89cfec0…`.
  Same pattern for r14/r15/r16 and the anchor: last blob change `f71ccbe`,
  byte-identical after the re-cut.
- `tripwire-r17.txt`: `f71ccbe db4c01a…` → `6046ab7 f50d437…` → `9bbb881 f50d437…` → `0ab1ccc 538c948…`.
  The 0ab1ccc change is confined to the single JSON data line. Its label
  (`MADO_TRIPWIRE: findings`), `counts` (`{hm 0, lp 1, pq 0}`), `exit` (1),
  149 file entries and the one finding tuple are identical to `9bbb881`;
  14 of the 149 `files[]` entries changed (input digest and/or line/bash/eval
  counters), because those seat transcripts were still being written:
  `MadoR17.jsonl` (509→540 lines, `sha256 8a427192…`→`012297231…`) plus
  `AttackErratum`, `AttackLessonM1M3`, `AttackReadmeRows`, `CriticTrends`,
  `RevengeMultiCallRecord`, `RevengeUnparsed`, `ReviewEvidenceIndex`,
  `ReviewPacman`, `ReviewScorecardCorrections`, `ReviewSkillRows`,
  `ReviewTokenizer`, `ReviewVerbs`, `SimplifyTripwire`.

Diff content of the files that did change:

- `tripwire-selftest-{core,compound,hardening}.txt`: only the
  `SELFTEST_SCRIPT_SHA256` line, `7a98720e…` → `962919ce…` (suite totals unchanged).
- `tripwire-selftest-w2-regressions.txt`: four added `CASE … ok` lines, the sha
  line, and `SELFTEST_SUMMARY: 26/26` → `30/30`.
- `tripwire-w2-{adversarial,false-positive}.txt`: only the sha line
  (adversarial remains `4/26 passed`, false-positive `3/3`).
- `tripwire-vs-oracles.json`: only `"tool_sha256"`, `7a98720e…` → `962919ce…`;
  `rounds` agreement data byte-identical.
- `tripwire-r17.txt`: data line as above; counts line identical.

## Receipt provenance surface (what the artifacts themselves carry)

`tripwire-r*.txt` / `-anchor-r15.txt` line 2 is schema `mado-tripwire-verdict-v1`
with keys `counts, exit, files, findings, permitted, schema, unpermitted`.
`files[]` entries carry per-input `path`, `sha256`, `lines`, `bash_calls`,
`eval_calls`, `unparsed_spawns`, `eval_unparsed`. There is **no** tool identity,
tool sha, or commit field in the scan output; the tool prints
`SELFTEST_SCRIPT_SHA256` only in `--selftest` mode (line 887 at `0ab1ccc`).

Only these evidence files contain a tool sha or commit marker:

| file | field | value at master |
|---|---|---|
| `tripwire-selftest-{core,compound,hardening,w2-regressions,w2-adversarial,w2-false-positive}.txt` | `SELFTEST_SCRIPT_SHA256` | `962919ce…` |
| `tripwire-vs-oracles.json` | `tool_sha256` | `962919ce…` |
| `frozen-tampered-recut.json`, `label-check{,-final}.txt`, `harm-{action,legacy}-selftest.txt` | `measured_commit` | other receipt families, not tripwire scans |

No `tripwire-r*.txt` or `-anchor-r15.txt` contains `tool_sha256` or
`measured_commit` (grep over `round-17/evidence`).

## Were outputs compared?

Within the transcript, no before/after comparison of receipt content:

- The re-cut call overwrites the receipt files and prints only the new run's
  counts. It does not read, diff, hash or re-open the pre-fix files.
- The only set comparison in the call is tripwire-vs-oracle (`O[rr]` from the
  `oracle-*.json` files), i.e. an external baseline, not the pre-fix receipts.
  Its output changed only in `tool_sha256`, so that comparison's membership was
  unchanged.
- The commit call stages with `git add -A` and runs `git commit`; it prints no
  `git diff`/`--stat`, and the result shows only the commit hash and an empty
  porcelain list. Nothing between records 541 and 542 inspects the re-cut.
- The "identical counts" statement first appears in the lesson text appended by
  the same commit call (record 542) and is repeated in the final assistant text
  (record 548: "re-ran all transcript receipts; the counts are unchanged").
  Its numeric basis is the printed tuple in record 541, whose values
  (2/12/19, 4/0/46, 3/29/177, 0/0/2) were already in the lesson's M2 row before
  the fix.

Post-hoc: the five rewritten files carry mtimes `15:17:26.6–27.8Z` (after the
fix, before the commit) and their blobs are identical to the pre-fix `f71ccbe`
blobs, so the "identical counts" statement is consistent with the committed
objects; `tripwire-r17.txt` also has identical counts and finding tuple but
different bytes (input transcripts grew).

## Mechanism of the unreceipted claim

1. **The scan receipt has no tool-provenance field.** Its bytes are a function
   of (input bytes, permit set, tool behaviour). A re-run under a new tool that
   returns the same output produces the same bytes; nothing in the receipt
   records which tool produced it.
2. **The re-cut was therefore a no-op in git for r13–r16 and the anchor.** The
   P11 fix changes bytes only for quoted/escaped `#` inputs; on these five
   inputs no finding changed (finding tuples identical between `f71ccbe` and
   `0ab1ccc`; blobs identical), so the regenerated files matched the
   `f71ccbe` blobs, `git add -A` had nothing to stage for them, and `0ab1ccc`
   lists no change to those five files. The r13–r16/anchor blobs were
   introduced at `f71ccbe` (tool `7a98720e…`) and are carried unchanged by
   `6046ab7`, `9bbb881` and `0ab1ccc`.
3. **The claim was written in the same commit that could not show it.** Record
   542 appends lesson lines 171–176 ("all real-transcript receipts re-cut with
   identical counts") and commits with the message "…, receipts re-cut"; the
   commit diff contains no r13–r16/anchor entry. The report (record 545) and
   chat (record 548) repeat the re-cut claim.
4. **Where the new tool sha is receipted:** the four suite receipts and the
   two `w2` receipts changed only their `SELFTEST_SCRIPT_SHA256` line (plus
   the four new cases in `w2-regressions`), and `tripwire-vs-oracles.json`
   changed only its `tool_sha256` line — those are the artifacts that bind
   `962919ce…` to a committed file. The real-transcript receipts do not.
5. **The report's C3 row kept the pre-fix sha.** `.ufo/reports/round-17/mado.md:76`
   reads "present, sha256 `7a98720e…`; 9/9, 16/16, 33/33, 30/30 exit 0", under
   a column headed "After @ `f71ccbe` (= content of `6046ab7`)". At `f71ccbe`
   the tool is `7a98720e…` and the w2-regressions receipt says `26/26`; `30/30`
   first exists at `0ab1ccc` (`962919ce…`). SCORECARD line 906 was updated in
   record 542 to "`962919ce…` after the late P11 fix … 30/30"; the report row
   was not updated in records 545/547 (only its HEAD line was).

## Divergences (claim vs committed record)

| # | claim | record |
|---|---|---|
| D1 | `corpus/lessons/round-17.md:176` — "all real-transcript receipts re-cut" | r13–r16 + anchor blobs unchanged since `f71ccbe`; `0ab1ccc` contains none of those five files |
| D2 | commit subject — "receipts re-cut" | only r17, the six selftest/w2 receipts and vs-oracles changed; the re-cut of the other five files is invisible |
| D3 | `corpus/lessons/round-17.md:175` — `w2-regressions` 30/30 under `962919ce…` | receipt has `SELFTEST_SUMMARY: 30/30` and `SELFTEST_SCRIPT_SHA256: 962919ce…` (consistent) |
| D4 | `.ufo/reports/round-17/mado.md:76` — `7a98720e…` + `30/30` | pair impossible at any revision: `7a98720e` = 26/26; 30/30 first appears at `0ab1ccc` = `962919ce…` |
| D5 | `.ufo/reports/round-17/mado.md:72` column "After @ `f71ccbe`" | `30/30` and `962919ce…` are `0ab1ccc` state; the report row was not updated when SCORECARD was |

## Landed text that carries the claim

- `corpus/lessons/round-17.md:171-176` (appended by the `0ab1ccc` commit call):
  "… `tripwire/w2-regressions` 30/30; tool sha256 `962919ce…`; all
  real-transcript receipts re-cut with identical counts."
- `corpus/lessons/round-17.md` M2 row: receipt pointers `tripwire-r13..r16.txt`
  and counts "19/46/177/2".
- `.ufo/reports/round-17/mado.md:3` (HEAD line): "… tool sha `962919ce…`,
  receipts re-cut with identical counts".
- `.ufo/reports/round-17/mado.md:76` (C3 row): pre-fix `7a98720e…` + `30/30`.
- `SCORECARD.md:906`: `962919ce…` + suites 9/9, 16/16, 33/33, 30/30.
- Outside spot-check, `corpus/lessons/round-17-verifier-spotcheck.md:183-195`
  (R17-V1/V2) states the same three facts reconstructed here: receipts last
  changed at `f71ccbe` under `7a98720e…`; git records no change at `0ab1ccc`;
  report line 76 cites `7a98720e…` while the tip is `962919ce…`.

## Confidence and limits

- High confidence (direct reads): every timestamp, record index, command text,
  file mtime, blob id, numstat row, printed count, and landed line quoted above.
- The transcript is a mutable session file (mtime 15:24:56Z; last record
  15:24:56.844Z). Record indices are as of this read; timestamps are the
  harness record times.
- "No comparison occurred" is bounded to tool calls visible in this transcript
  between record 536 and the commit at record 542; shell builtins inside a
  call are quoted exactly, and the commit call's command line contains no
  diff/stat/readback.
- Why the author treated the printed tuple as sufficient is intent;
  `[INFERENCE]` only: the thinking at record 539 says "Now I'm rerunning the
  real receipts to check the anchor cases and r13-17", with no stated
  comparison target. Nothing further is asserted.
- The `0ab1ccc` message and the lesson sentence use "receipts re-cut" for a
  regeneration whose committed evidence surface is the selftest/vs-oracles sha
  lines, not a change to the real-transcript receipts.
