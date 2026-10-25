# RevCensus — wave 2 falsification of the fleet census gate (mado)

Seat: `L1Mado35.RevCensus` (leaf reviewer). Round 35, wave 2.
Lane repo: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Read-only attack: no lane corpus file,
counter, control, `corpus/SOURCES.md`, jj/Git index state, fleet file, or
`/home/vgpnk/Projects/shokuknow` byte was modified. Scratch evidence:
`.ufo/waves/round-35/scratch/RevCensus/` (`validate.stdout.txt`, `selftest.stdout.txt`,
`base/corpus/SOURCES.md` = HEAD copy, `base_ids.txt`, `work_ids.txt`, `warn_ids.txt`,
`base_w04.txt`, `work_w04.txt`).

No tool was installed or upgraded this seat; pacman was not touched.

## Verdict

**CONFIRM — the census claim survives attack.** `sources-census.sh validate --root
/home/vgpnk/Projects/shokunin mado` exits 0 and emits zero E-codes; the registry carries exactly
200 data rows (192 before + 8), all unique, all inside `## Registry`, all 13-field; the only
findings are 7 `W04` warnings and every one of them names an OLD id
(S030, S042, S045, S097, S119, S120, S121; numeric max 121). No warning names S203–S210. The
warning set is byte-identical against the pre-wave `HEAD` registry, so the appended eight rows
introduced no warning and reordered nothing. The validator that produced this silence is not
vacuous: its own selftest kills 96/96 checks including the `W04` mutant.

Axes named: **A1** row-count integrity · **A2** 192+8 decomposition (baseline fidelity) ·
**A3** warning identity (no new-row warning) · **A4** validator non-vacuity + determinism ·
**A5** absence of padding/hidden rows.

## Mandated command, verbatim

Command (exactly as assigned; `--today` omitted so the script takes `date -u +%F` = 2026-10-25):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado; echo rc=$?
```

stdout (tab-separated; tabs preserved, copy at `scratch/RevCensus/validate.stdout.txt`):

```
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
rc=0
```

`rc=0` — warnings never change status (`sources-census.sh:16-18`), and the `mado ok` line is
emitted only when the lane produced no `E`-code (`:738-745`: `lane_errors=1` iff a line matches
`\tE[0-9]+\t`, and `emit "$lane\tok"` runs only when `lane_errors != 1`). The lane resolved to the expected registry through the conf row
`mado|mado-shokunin|coverage + operability (desktop and compositor craft)` (`shokunin.conf:56`),
and `mado` is the only lane token match.

## A1 — row count is exactly 200 (PASS)

```
$ grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md
200        # rc=0
```

Cross-checks, all agreeing on 200:

| probe | command | result |
|---|---|---|
| parser's own counter | `sources-census.sh census --root . mado` | `mado rows 200`; `FLEET rows 200` |
| distinct ids | `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' … \| grep -oE 'S[0-9]+' \| sort \| uniq -d` | empty (no duplicate id) |
| table-ish tokens anywhere | `grep -oE '\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' … \| wc -l` | 200 |
| rows with 4+ leading spaces (parser-invisible code) | `grep -cE '^ {4,}\|[[:space:]]*S[0-9]{3,}'` | 0 |
| rows lacking a leading pipe | `grep -cE '^[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | 0 |
| byte-identical duplicate row lines | `… \| sort \| uniq -d \| wc -l` | 0 |

So the grep count is neither inflated (no duplicate/duplicate-line rows) nor deflated (no
4-space-indented or pipe-less row that the parser would silently drop). Parser and grep agree
because every one of the 200 rows sits under `## Registry`: the section-scoped awk tally gives
`200 ## Registry` and nothing under any other heading, and `validate` emitted no `E12`
(row outside Registry) — consistent with a single `## Registry` heading at
`corpus/SOURCES.md:9` and the table closing at line 212 immediately before `## Paths` at line
214.

Field shape: every row is `NF=13` under the parser's `-F'|'` (11 cells + two edge empties).
`validate` emitted no `E01`, which is emitted exactly when `NF!=13` (`sources-census.sh:635-639`);
spot-checked directly on the eight new rows — all `13`, and `sed -n '205,216p' … | grep -c $'\t'`
= `0`, i.e. no stray tab shifting cells.

## A2 — the 192 baseline is real, and the delta is exactly the eight new ids (PASS)

Baseline is not assumed; it is read from the lane's committed bytes (read-only `git show`, no
index refresh — `--no-optional-locks`):

```
$ git --no-optional-locks show HEAD:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'
192
$ git --no-optional-locks log --oneline -1 -- corpus/SOURCES.md
fa7ba11 round-34: admit the waybar event-socket entry after the frozen counter
```

Set difference of ids, HEAD vs working tree:

```
added   : S203 S204 S205 S206 S207 S208 S209 S210
removed : (none)
HEAD max id: S202;  working max id: S210
```

The same delta measured by the census parser itself on the extracted HEAD copy
(`scratch/RevCensus/base/corpus/SOURCES.md`, byte-identical to `HEAD:corpus/SOURCES.md`, written
by the same `git show`):

```
$ sources-census.sh census --file base/corpus/SOURCES.md
file	rows	192
file	tier.A	185
…
$ sources-census.sh census --root . mado
mado	rows	200
mado	tier.A	193
```

192 + 8 = 200 and tier.A 185 + 8 = 193: all eight new rows are tier A, and nothing pre-existing
changed count. Recognised id gaps (S190–S195, S197–S200) are pre-existing arithmetic, not loss
this wave: 202 max old id − 10 gaps = 192, and the `removed` set is empty, so no old row was
deleted or renumbered to make room.

## A3 — every warning names an OLD id; none names S203–S210 (PASS)

Warned ids extracted from the live run (`scratch/RevCensus/warn_ids.txt`):

```
S030 S042 S045 S097 S119 S120 S121      numeric max = 121
```

- `grep -cE 'S20[3-9]|S210' validate.stdout` → `0` matches (grep exits 1 on zero count; that is
  the expected "absent" signal, not a failure).
- Only one code class appears — `W04 ×7`, zero `E`-codes and zero `W01/W02/W03`:
  `validate … | awk -F'\t' '$2~/^[EW][0-9]+$/{print $2}' | sort | uniq -c` → `7 W04`.
  Zero `W03` independently proves every mined row (181) carries a non-`—` used-by, the eight new
  rows included; zero `E11` proves every mined used-by path resolves on disk
  (`corpus/knowledge/idle-lock-{never-asked-r12,chain-armed-r14,offered-in-the-bar-r15}.md` all
  exist, `ls` rc=0).
- **The warnings are not this wave's.** Running `validate --file` on the HEAD copy and on the
  working file and diffing the `W04` lines:

  ```
  base W04 lines = 7 ; working W04 lines = 7 ; diff → IDENTICAL_W04
  ```

  Since `W04` fires position-dependently ("URL seen in a scope not seen before",
  `sources-census.sh:644-645`), an append that reused a URL in a new scope **would** have added a
  line here. It added none: the eight rows introduced zero W04, and no old warning moved or
  vanished. The seven are genuine pre-existing cross-scope URL repeats (e.g. S030 and S045 both
  repeat `wiki.hypr.land/Configuring/Basics/Window-Rules` in a further scope) — a standing
  condition of the registry, unchanged by round 35 and not a failure (exit 0 by design).

## A4 — the validator that produced this silence is not vacuous (PASS)

A clean validate only means something if the codes are armed. `scripts/sources-census.sh selftest`:

```
$ ./scripts/sources-census.sh selftest > scratch/RevCensus/selftest.stdout.txt; echo rc=$?
rc=0        # last line: "selftest ok"; 96 killed checks, "SURVIVED" count = 0
```

Includes the mutants that matter to this gate: `E01-malformed-row`, `E02-malformed-id`,
`E03-duplicate-id`, `E11-dangling-usedby`, `E12-row-outside-registry-mutant`,
`W03-mined-unused`, `W04-scope-sensitive-mutant`, `W04-does-not-fail-validation`,
`E04-rejected-pair-exemption-mutant`, the full 0/1/2/3-space indentation matrix, the
`FLEET-rows` totals, `gawk-failure-is-error-not-ok`, and `H1-no-table-cell-execution`
(the registry is parsed, never sourced/shell-evaluated). All killed → a zero-finding run on the
lane is a positive result, not an unarmed one.

Determinism: the mandated command run twice, byte-identical stdout, `rc1=0 rc2=0`, `diff` empty
(`DETERMINISTIC`).

## A5 — the eight new rows are rows, not padding (PASS)

| id | line | status | tier | used-by | receipt exists + sha256 |
|---|---|---|---|---|---|
| S203 | 205 | mined | A | `corpus/knowledge/idle-lock-never-asked-r12.md` | yes, `1b7fa87f…1646` = row's cited hash |
| S204 | 206 | mined | A | `…never-asked-r12.md` | yes, `4cd5ba65…4ad` |
| S205 | 207 | mined | A | `corpus/knowledge/idle-lock-chain-armed-r14.md` | yes, `f3387bfc…1a` |
| S206 | 208 | mined | A | `…offered-in-the-bar-r15.md` | yes, `1d30e4a9…8d5` |
| S207 | 209 | mined | A | `…offered-in-the-bar-r15.md` | yes, `81c33e79…c59` |
| S208 | 210 | mined | A | `…offered-in-the-bar-r15.md` | yes, `6e72f0db…654` |
| S209 | 211 | mined | A | `…offered-in-the-bar-r15.md` | yes, `a170c7a5…27c` |
| S210 | 212 | mined | A | `…offered-in-the-bar-r15.md` | yes, `ef282e38…726` |

`sha256sum .ufo/waves/round-35/fetch/S2{03..10}.receipt.txt` reproduces the receipt hash cited
inside each row (all eight match); eight source cells are eight distinct strings
(`awk … substr($3,1,60) | sort -u | wc -l` → `8`). The rows↔entries mapping is bidirectionally
consistent: rows S203,S204 → r12; S205 → r14; S206–S210 → r15, and grepping each entry for
`S20x` returns exactly those ids and no others (2 + 1 + 5 = 8) — the same 3 entries / 8 rows that
C1 freezes.

## Residual risk (not a finding against the claim)

1. **URL dedup is vacuous for the eight new rows.** `url_of()` only extracts `http(s)://`
   (`sources-census.sh:600-606`); `grep -cE '…S2(0[3-9]|10)…https?://'` → `0`. So `E04`/`W04` and
   `shared` mode never evaluate S203–S210: their uniqueness rests on distinct id, distinct source
   cell, and distinct receipt hash — all three verified above — not on the registry's URL guard.
   Correct for `own-work`/host-evidence rows, but no URL-level duplicate protection exists for
   this class of row.
2. **Id space is not dense** (S190–S195, S197–S200 absent). Pre-existing at HEAD, harmless for
   counters that count rows rather than ids, but any future gate asserting `max_id == row_count`
   would false-fail.
3. **The seven W04 warnings remain** a real (pre-existing) cross-scope URL duplication condition.
   In scope for a future simplification pass, out of scope for round 35 and not a regression.
4. This seat's scope is the census gate. `C1` and `C2` were only run as corroboration —
   `PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET` (rc=0) and
   `PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET`
   (rc=0) — their internals are covered by the assigned C1/C2 seats, not here.

## Verification ledger (command → exit code)

| # | command (abridged) | rc | observed |
|---|---|---|---|
| 1 | `sources-census.sh validate --root …/shokunin mado; echo rc=$?` | 0 | 7×W04 + `mado ok` |
| 2 | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` | 0 | `200` |
| 3 | `… \| uniq -d` (ids) / `… \| uniq -d \| wc -l` (lines) | 0 | empty / `0` |
| 4 | `sources-census.sh census --root . mado` | 0 | `rows 200`, `tier.A 193` |
| 5 | `git show HEAD:corpus/SOURCES.md \| grep -cE …` | 0 | `192` |
| 6 | `comm -13/-23 base_ids work_ids` | 0 | added S203–S210, removed none |
| 7 | `sources-census.sh census --file base/corpus/SOURCES.md` | 0 | `rows 192`, `tier.A 185` |
| 8 | `diff base_w04.txt work_w04.txt` | 0 | `IDENTICAL_W04` |
| 9 | `grep -cE 'S20[3-9]\|S210' validate.stdout` | 1 | `0` matches (grep's zero-count exit — expected) |
| 10 | `awk '$2~/^[EW][0-9]+$/' \| sort \| uniq -c` | 0 | `7 W04`, zero E |
| 11 | `sources-census.sh selftest` | 0 | `selftest ok`, 96 killed, 0 survived |
| 12 | validate ×2 + `diff` | 0/0 | `DETERMINISTIC` |
| 13 | `sha256sum .ufo/waves/round-35/fetch/S2{03..10}.receipt.txt` | 0 | all 8 match row-cited hashes |
| 14 | `ls corpus/knowledge/idle-lock-{…}.md` | 0 | all three exist |
| 15 | `C1`/`C2` frozen counters | 0/0 | both `TARGET_MET` |
