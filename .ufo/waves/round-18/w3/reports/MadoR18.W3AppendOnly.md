# MadoR18.W3AppendOnly — append-only audit, `d9a5a18` → `a210241` (round 18)

Seat: MadoR18.W3AppendOnly. Scope: append-only discipline of `LOG.md`,
`corpus/QUALITY.md`, `corpus/lessons/round-17.md`, `corpus/SOURCES.md` rows
S001-S071 and `SKILL.md` between the round-17 baseline `d9a5a18` and the final
landed commit `a210241`; plus the same-round in-place edits to
`corpus/knowledge/walker-route-r18.md` and `theme-route-r18.md` between
`4c103b5` and `a210241`.

Verdict: **PASS on append-only discipline for all five scoped files and both
route notes.** The only deletions in the scoped files are the two `SKILL.md`
lines of the documented tripwire probe-limit sentence (exempted by the
assignment). One **Low** documentation defect found in a row this round itself
inserted (`mado-tripwire-frozen` understates its self-test as 17 cases; the
landed suite is 31), plus three nits, all listed under Findings. Nothing else
in scope was altered in place.

## Identity and ancestry

```
$ git rev-parse --abbrev-ref HEAD
HEAD
$ git rev-parse master
a210241b5429fb3c3f9ad23f42863d6e6d9e5845
$ git rev-parse a210241 d9a5a18 4c103b5 abfbf35 be886a3
a210241b5429fb3c3f9ad23f42863d6e6d9e5845
d9a5a18e17cd3a68b52148fcc01c4a30e340ba98
4c103b55b1ea5c3c555884afe3eb69b5189701b7
abfbf35b1ed4d4a1eb294d525ef286be30f3886f
be886a3cd05cf27d47a976c69df2f5f556759c08
$ git merge-base --is-ancestor d9a5a18 a210241 && echo "d9a5a18 ancestor OK"
d9a5a18 ancestor OK
```

`master` resolves to `a210241`; the worktree HEAD is detached at the same
commit (jj-colocated state, observed only, not a finding).

## Method, and a caveat about the prescribed counter

The prescribed command is

```
git diff d9a5a18 a210241 -- <f> | grep -c '^-[^-]'
```

It undercounts in two ways that matter here: it misses a deleted *blank* line
(`-` alone) and a deleted line whose content begins with `-`, i.e. every
markdown bullet. The theme-route edit below is exactly such a line: the
prescribed counter returns `0` while `git diff --numstat` and
`git diff | grep '^-' | grep -vc '^--- '` both return `1` deletion.

Because of that I checked every file three ways: the prescribed counter, a
robust deletion counter (`git diff ... | grep '^-' | grep -vc '^--- '`, which
still undercounts only deleted blank lines, so `--numstat` is the final
arbiter), and a byte-level proof over `git show REV:<path>` blobs
(prefix test for pure appends; line-subsequence test for mid-file
insertions).

Counts:

| file | prescribed `^-[^-]` | robust `^-` minus header | `--numstat` (add/del) | byte-level result |
|---|---|---|---|---|
| `LOG.md` | 0 | 0 | 25 / 0 | old blob is a **prefix** of new (86,314 → 87,907 B) |
| `corpus/QUALITY.md` | 0 | 0 | 39 / 0 | old blob is a **prefix** of new (9,841 → 13,497 B) |
| `corpus/lessons/round-17.md` | 0 | 0 | 25 / 0 | old blob is a **prefix** of new (17,184 → 18,669 B) |
| `corpus/SOURCES.md` | 0 | 0 | 24 / 0 | old lines are an ordered **subsequence**; 24 rows inserted after S071 |
| `SKILL.md` | 2 | 2 | 20 / 2 | every old line except the two below is preserved in order |

Per-commit steps (robust counter), to exclude a transient edit that is
reverted inside the window:

```
d9a5a18..4c103b5   LOG 0/0   QUALITY 0/32   round-17 0/25   SOURCES 0/24   SKILL 2/9
4c103b5..abfbf35   LOG 0/0   QUALITY 0/0    round-17 0/0    SOURCES 0/0    SKILL 0/0
abfbf35..be886a3   LOG 0/0   QUALITY 0/7    round-17 0/0    SOURCES 0/0    SKILL 0/11
be886a3..a210241   LOG 0/25  QUALITY 0/0    round-17 0/0    SOURCES 0/0    SKILL 0/0
```

(remove/add; `removed` counted with `grep '^-' | grep -vc '^--- '`.) No step
removes a line from any scoped file except the two `SKILL.md` lines at
`4c103b5`.

## Removed lines, each explained

### `SKILL.md` — 2 lines (the exempted tripwire limit sentence)

`git diff -U0 d9a5a18 a210241 -- SKILL.md` shows exactly three hunks:

```
@@ -538,2 +538,3 @@ ...
-misroots) are not findings. It is labelled a probe: it reads mutable
-transcripts with no frozen replay.
@@ -564,0 +566,6 @@ ...
@@ -1811,0 +1819,11 @@ ...
```

The two deleted lines are old lines 538-539 (1-based), immediately above
`## Gate registry`, and they are exactly the sentence the assignment exempts:

- old 538: ``misroots) are not findings. It is labelled a probe: it reads mutable``
- old 539: ``transcripts with no frozen replay.``

They are replaced by three lines (new 538-540) that narrow the probe label to
the `--scan` entry and document the new gate entry `--frozen` (registry row
`mado-tripwire-frozen`). The replacement is truthful against the registry:
`mado-tripwire` still reads `probe` with the `--scan` command, and the new
`mado-tripwire-frozen` row reads `gate`. It is also documented in the
round-18 record: `LOG.md` C3 ("registry row `mado-tripwire-frozen` (gate)")
and `corpus/lessons/round-18.md` § Wave-2 corrections (the `--frozen`
hardening bullet). Deletion was forced by the registry addition — leaving the
sentence would have asserted "no frozen replay" beside a frozen-replay row.

### Other scoped files

`LOG.md`, `corpus/QUALITY.md`, `corpus/lessons/round-17.md` and
`corpus/SOURCES.md`: **zero deleted lines** by all three counters. The
byte-level prefix tests show the first three are pure EOF appends.

### Route notes (separate check, `4c103b5..a210241`)

```
$ git diff --numstat 4c103b5 be886a3 -- corpus/knowledge/theme-route-r18.md corpus/knowledge/walker-route-r18.md
19  1  corpus/knowledge/theme-route-r18.md
3   1  corpus/knowledge/walker-route-r18.md
$ git diff --numstat be886a3 a210241 -- <both notes>
(empty)
```

Both in-place edits landed at `be886a3` (wave-2 integration), not at
`a210241`. One deleted line each:

- `theme-route-r18.md` line 60, old: `[OA:5] ... The declaration names the
  link; retargeting the link changes the wallpaper without editing config.`
  New: the declaration-names-the-link sentence plus the scoped mechanism
  claim and `whether an already-running swaybg follows a retarget is [UNK]`,
  marked inline `(wave-2 correction, CriticC2W2 D1)`. The cited anchors
  `[OB:49-50]`/`[OS:24-25]` are defined in the note's citation table (lines
  22-23) and their target lines (`pkill -x swaybg` + relaunch with `-m fill`)
  support the replacement. **Logged**: the note's own
  `## Wave-2 corrections (round 18, append-only)` first bullet quotes the old
  text and names CriticC2W2 D1 (line 149).
- `walker-route-r18.md` line 212, old: `no elephant.toml is present, so
  EG:85-89 applies to the global config.` New: same sentence qualified
  `[INF]` with three conditions (`--config`, `XDG_CONFIG_DIRS`,
  `ProviderConfig` not read) and `CriticC2W2 D2`. **Logged**: there is no
  Wave-2 block in this note (`grep -n 'Wave-2\|wave-2\|Wave 2'` returns
  nothing), but the lesson logs it at `round-18.md:89`: "`walker-route-r18.md:212`
  elephant global-config inference marked `[INF]` with its conditions
  (CriticC2W2 D2)". That satisfies the assignment's "note's Wave-2 block or
  the lesson" alternative.

## `corpus/SOURCES.md` rows S001-S071

Rows compared as exact bytes (trailing newline included):

```
old rows 71 mismatched []
new row count 95
```

Byte-level placement:

```
common_prefix_lines 83 common_suffix_lines 203 old_lines 286 new_lines 310
line_subsequence_preserved True
```

Line 83 is S071 and new line 84 is S072, so the 24 added rows S072-S095 were
inserted immediately after S071, in ID order (`new ids ordered: True`), and
the 203 trailing lines (leads/notes sections) are unchanged. A multiset diff
of new-minus-old lines yields exactly the 24 row lines and nothing else; every
row carries the table's 11-field/12-pipe shape; S095 carries recheck `90d`.
No status/recheck/used-by change to any pre-existing row.

## `SKILL.md` structure

Additions total 20 = 3 (replacement sentence) + 6 (registry rows) + 11
(appended errata); the prescribed addition counter reports 18 because two
added lines are blank. Structural proof:

```
old 536-541:
536 'package transaction plus undisclosed elevated/query calls (lesson\n'
537 '`round-17.md` M2); breaches outside its classes (jj, /proc reads, file\n'
538 'misroots) are not findings. It is labelled a probe: it reads mutable\n'
539 'transcripts with no frozen replay.\n'
540 '\n'
541 '## Gate registry\n'
every other old line preserved in order: True
registry rows added: ['mado-tripwire-frozen', 'mado-frozen-provenance',
 'mado-receipt-check', 'mado-fetch-verify', 'mado-pipe-rc-census',
 'mado-measure-mutants']
```

The six rows are schema-conformant registry insertions per `PROTOCOL.md`
§Gate standard, Registry (SKILL is this lane's registry home; 8 fields/9
pipes each): `mado-tripwire-frozen` = gate; the other five = probe. Every
path they name is committed at `a210241`
(`git cat-file -e a210241:.ufo/waves/round-18/{frozen-provenance-check.py,
receipt-check.py,fetch-verify.py,pipe-rc-census.py,measure-mutants.py}`,
`.ufo/waves/round-18/frozen`, `.ufo/waves/round-18/tripwire/frozen` all OK;
also OK: `tools/mado-tripwire.py`,
`.ufo/waves/round-18/frozen/provenance.json`,
`.ufo/waves/round-17/evidence/session-index.json`,
`.ufo/waves/round-18/receipt-claims.json`,
`.ufo/waves/round-18/evidence/measure-mutants.json`, the four scan-suite
directories under `.ufo/waves/round-17/tripwire/`, and 49
`.ufo/waves/round-18/fetch/*/receipts.jsonl` files),
and each tool has a committed w1 report (`FrozenProvenanceCheck.md`,
`ReceiptCheck.md`, `FetchVerify.md`, `PipeRcCensus.md`, `MeasureMutants.md` in
`.ufo/waves/round-18/w1/reports/`). The table's pre-existing `mado-tripwire`
row was not edited.

The 11-line `## Errata (round 18, append-only)` block is a pure EOF append.
Its claims reproduce: `SKILL.md:23`/`:114` carry the dated `walker 2.17.0`
pins it names; `/etc/xdg/walker/config.toml` is 305 L / 13,743 B /
`3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b`;
`/var/log/pacman.log:2929` is the walker `2.17.0-1 -> 2.17.2-1` upgrade and
`:3095` the elephant `2.21.0-1 -> 2.22.1-1` upgrade.

## Other scoped content verified

- `corpus/QUALITY.md` append (pure prefix): criteria 24-26 continue after 23
  with no renumbering, each citing `lessons/round-18.md#mistakes` and a
  runnable check; the trailing wave-2 correction paragraph (that criterion
  24's red fixture prints `STALE`, not `SHA_MISMATCH`) is part of the same
  append.
- `corpus/lessons/round-17.md` append (pure prefix, 25 lines): an
  `## Erratum (round 18, append-only; outside R17-V1/V2)` section. Quoted
  lines 175-176 exist at `d9a5a18` (the quote starts mid-line 175 after
  `real comment) — ` but the quoted text is verbatim), and the line-132
  `26/26` reference exists.
- `LOG.md` append (pure prefix, 25 lines): the 2026-10-20 round-18 entry,
  appended only at `a210241`; each scoped file's change has a narrative
  entry.

## Findings

### Low — registry row `mado-tripwire-frozen` understates its self-test (17 vs 31)

`SKILL.md:566` (inserted at `4c103b5`, unchanged since) says the self-test is

```
python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-18/tripwire/frozen
(17 mode-frozen cases; exit and first-line outcome)
```

At `a210241` the committed suite is 31 cases:

```
$ ls -d .ufo/waves/round-18/tripwire/frozen/*/ | wc -l
31
$ grep -n "SELFTEST_SUMMARY" .ufo/waves/round-18/evidence/final/tripwire-frozen-selftest.txt
34:SELFTEST_SUMMARY: 31/31 passed failed=[]
```

The round's own record says 31/31 (SCORECARD results/harm watch) and the
lesson logs "Frozen suite 17 → 31 cases". The registry row is the gate's
canonical contract and now understates coverage by 14 cases. This is **not**
an append-only violation (the row was not edited after insertion; the count
was correct for the wave-1 suite), but the sanctioned fix is an appended
erratum under `## Errata (round 18, append-only)`, not an in-place edit. No
behavioural risk; a reader of the registry is told 17 when 31 run.

### Low — lesson's S092-S095 recheck "old→new" records uncommitted working-copy values

`round-18.md` lines 77-80 log `S092/S093/S094` recheck
`on-change; …` → `on-release` and `S095` → `90d`, then state "(same-round, to
satisfy census E09 before first landing at `4c103b5`)". At `4c103b5` the rows
already carry the new values:

```
$ git show 4c103b5:corpus/SOURCES.md | grep -oE '^\| S09[2-5] .*\| (mined|rejected) \| 2026-10-20 \| [^|]+ \|'
… recheck=on-release / on-release / on-release / 90d
$ git diff 4c103b5 a210241 -- corpus/SOURCES.md | grep '^-' | grep -vc '^--- '
0
```

So no committed tree contains the old strings and there is no append-only
violation; the parenthetical discloses the timing. The defect is only that an
"old→new" entry cannot be re-derived from history, which is precisely what
the lane's old→new convention is for. Future logs should label these
"working copy (never committed)" or omit `old→new`.

### Nit — `walker-route-r18.md` in-place edit is logged only in the lesson, without old→new

It is logged (lesson bullet, CriticC2W2 D2) and the assignment allows the
lesson as the log location. But the note carries no Wave-2 block, and the
lesson bullet does not quote the removed text (theme's note does). A reader
of the note cannot tell that line 212 was rewritten rather than authored that
way.

### Nit — round-17 erratum quote begins mid-line

`round-17.md:180` says "Lines 175-176 read: …" but the quoted span starts
after `real comment) — ` on line 175. The text is verbatim, so this is
cosmetic; an ellipsis would make the partial-line quote explicit.

### Method note (not a lane defect)

The prescribed `grep -c '^-[^-]'` reports `0` for `theme-route-r18.md` where
the diff has one real deletion (markdown bullet), and reports 18 of the 20
added `SKILL.md` lines (blank added lines). Use `--numstat` as the arbiter;
any audit that relies on the prescribed counter alone will miss bullet
deletions in the notes.

## Residual risk and verification gaps

- I did not re-run any tool, receipt or replay, and did not re-fetch any URL.
  The 17-vs-31 finding rests on the committed suite listing and the committed
  `SELFTEST_SUMMARY` receipt, not on executing the suite.
- Endpoint blob analysis plus the four per-commit cumulative checks can see
  every committed change; an edit made and reverted *within one commit* is
  not observable in git history and would not be an append-only violation of
  committed history in any case.
- I checked only the files named in the assignment. Other round-18 paths
  (tools, `.ufo/waves/round-18/**`, SCORECARD, lessons/round-18.md) were read
  as evidence but their own append-only status is not asserted here.
- No host-mutating command was issued: no package query, service, compositor,
  input or screenshot operation. No tool was installed or upgraded. Only
  read-only git (`show`/`diff`/`log`/`rev-parse`/`merge-base`/`cat-file`/
  `ls-tree`), file reads (`/etc/xdg/walker/config.toml`,
  `/var/log/pacman.log`) and a `mkdir` for this report's directory were run.
