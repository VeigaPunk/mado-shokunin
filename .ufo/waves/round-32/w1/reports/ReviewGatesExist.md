# ReviewGatesExist — sources-census.sh validate contract, verified

Scope: read-only review of `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (806 lines,
read end to end) plus an empirical probe against the live script. All line cites are
`sources-census.sh:<line>` unless prefixed. Goal: make the round-32 append rows pass the gate on
first submission.

## 1. What `validate --file` reads, and the used-by root

- `--file PATH` selects exactly one registry file; the file must exist or exit 2
  (`--file not found`, line 498). `resolve_targets` resolves it with `realpath` and records
  `dir_abs=$(realpath -- "$(dirname -- "$file_abs")/..")` — **the parent of the file's directory**
  (lines 499-502). For the standard layout `<lane>/corpus/SOURCES.md`, that is `<lane>/`.
- Only that one file is parsed: `row_pass` feeds a single `$f` to gawk (line 717; gawk reads `"$f"`,
  line ~712), and `usedby_findings` reads the same file (`done < "$f"`, line 570), invoked only in
  validate mode (lines 720-722). No other registry/sibling file is ever read.
- Used-by targets are **existence-probed, not read**: `[ ! -e "$dir/$path" ]` → E11 (lines 566-567),
  resolved against `$dir`, i.e. relative to the lane repo root (roster mode: `files[$lane]="$ROOT/${repo:+$repo/}corpus/SOURCES.md"`,
  `dirs[$lane]="$ROOT${repo:+/$repo}"`, lines 467-468; unlisted child dirs lines 483-485).
  So `corpus/knowledge/foo.md` means `<lane-root>/corpus/knowledge/foo.md`.
- With `--file`, the lane label in output is literally `file` (line 502). `--root` only feeds the
  conf-based roster; it does not redirect used-by resolution.

## 2. Accepted `recheck` forms (E09)

Three forms, lines 663-667:

1. ISO date matching `/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/` that is a **real calendar date** — validated by
   `epoch()`: year 0 rejected, `mktime(...,1)` UTC round-trip `strftime("%Y-%m-%d",t,1)!=s` rejects
   impossible dates like `2026-02-30` (lines 583-590; empirically confirmed). Future recheck dates are
   legal in validate mode (only `overdue` judges them, lines 675-685).
2. `/^[0-9]+d$/` — one or more digits + literal `d` (`90d`, `7d`, `0d`). `90 days` is rejected
   (empirically confirmed).
3. Symbolic cadence, `symbolic()` line 582: `/^[A-Za-z][A-Za-z0-9 _-]*$/` — must **start with a
   letter**; then letters/digits/spaces/underscore/hyphen (`on-release`, `annual`).

Anything else — including `—` and empty — is E09 (empirically: row with recheck `—` → `E09 … recheck=—`).
**recheck is mandatory on every registry row.**

## 3. Accepted `opened` rule (E08)

Lines 660-662: `epoch(opened)` must be valid (same real-ISO-date check as above) and
`opened_epoch <= today_s`; strict `>` means same-day is fine. `today` is `--today` or `date -u +%F`
(lines 90-91) — **UTC**, independent of local TZ (selftest `UTC-date-in-Sao-Paulo`, lines 160-161).
Future or impossible dates → E08 (empirically: `2026-10-25` vs `--today 2026-10-24` → E08;
`2026-02-30` → E08).

## 4. `used-by` rule and separators

- Column 12 of 11 (`$12` in gawk line 628; `cells[11]` in `usedby_findings` line 560).
- **Comma-separated** for multiple paths: `IFS=',' read -r -a paths` (line 562), each element
  whitespace-trimmed (line 564; `trim_cell` lines 531-535 strips spaces/tabs at edges).
- `—` (em dash) and empty entries are skipped (line 565). Placeholder must be the **em dash `—`**;
  a plain `-` would be treated as a path and E11'd.
- Every non-dash path must exist at `$dir/$path` else E11 (lines 566-567).
- **Path checks apply only to `status = mined` rows** — line 559: `[ "$status" = mined ] || continue`.

## 5. The 0-3 leading-space rule

Two implementations, same regex:

- gawk `row_pass`: table rows must match `/^ {0,3}\|/` (line 615), then `sub(/^ {0,3}/,"",line)`
  (line 616). Headings: `/^ {0,3}##[ \t]/` (line 609), `/^ {0,3}#[ \t]/` (line 614).
- `usedby_findings`: `heading_re='^ {0,3}##[[:space:]]'`, `top_heading_re='^ {0,3}#[[:space:]]'`,
  `table_re='^ {0,3}\|'` (lines 540-541), then strip up to 3 leading spaces (line 553).

Documented in the header: "Maintained parser accepts 0–3 leading ASCII spaces before Markdown
rows/headings; 4 or more spaces are indented code and ignored" (lines 39-41). Selftest exercises
widths 0-3 (loop at line 287). Empirically: a 3-space-indented row is fully counted/validated; a
4-space-indented row is ignored entirely (its `watch` status and year-2099 `opened` produced no
findings). **A tab-indented row does not match `^ {0,3}` and is silently ignored** — regex is
spaces-only.

## 6. Exact codes and meanings

Usage header lines 24-33; implementation lines 634-674 plus 566-567 and 618-622. Rows are parsed
`-F'|'`, so 11 columns ⇔ NF=13 (E01 prints `fields=NF-2`, line 636). Header and `|---|` rows are
skipped (`separator_row`, lines 591-598, call at 625; header detected by `trim($2)=="id"`).

| Code | Meaning | Site |
|---|---|---|
| E01 | Malformed row, NF≠13 (not 11 columns); row skips further checks except E02, then `next` | 635-638 |
| E02 | id not `/^S[0-9]{3,}$/` (S + ≥3 digits) | 637, 640 |
| E03 | Duplicate id within the same file | 640-642 |
| E04 | Duplicate URL **within the same scope**; exempt if this row is `rejected`, all prior same-scope rows are `rejected`, or `teaches` contains `supersedes S###` | 646-649 |
| E05 | kind not in `spec\|docs\|paper\|code\|tool\|dataset\|talk\|book\|community\|own-work` | 655-656 |
| E06 | tier not exactly `A`, `B`, or `C` | 657 |
| E07 | status not `queued\|mined\|rejected` (`watch` is not a status, header line 4) | 658-659 |
| E08 | `opened` not a real ISO date or in the future | 660-662 |
| E09 | `recheck` not ISO-date / `NNd` / symbolic (see §2) | 663-667 |
| E10 | `community` kind at tier A | 668 |
| E11 | used-by path missing on disk (**mined rows only**) | 559, 566-567 |
| E12 | Row-shaped source (`\| S### \|`) outside the `## Registry` section; section match is exact after trim (`trim(substr(line,3))=="Registry"`, line 611) | 618-622 |
| W01 | Tier C + mined + used-by ≠ `—` | 669-670 |
| W02 | rejected + `teaches` shorter than 8 chars | 671-672 |
| W03 | mined + used-by = `—` | 673-674 |
| W04 | Same normalized URL across **different** scopes | 643-645 |

URL normalization for E04/W04 (`url_of`, lines 600-605): first `https?://` URL in the source cell;
`#fragment` and trailing `/` stripped; scheme stripped; host lowercased. Exit semantics: any E → 1;
W-only → 0 with a `<lane>	ok	<path>` line (selftest lines 158-159, 364-365); missing registry file
→ `missing` line and exit 2 in validate (selftest lines 145-146).

## 7. Decisive: dangling used-by — error or warning?

**Depends on status.** E11 fires only for `mined` rows (line 559). Empirically verified against the
live script (`bash sources-census.sh validate --today 2026-10-24 <fixture>`):

```
lane	E09	S904 recheck=—
lane	E08	S905 opened=2026-10-25
lane	E08	S906 opened=2026-02-30
lane	E09	S907 recheck=90 days
lane	E11	S903 missing used-by corpus/knowledge/gone.md
exit=1
```

- S901: `queued` row with used-by `corpus/knowledge/not-yet.md` (file absent) → **no finding**; the
  row was counted (census `rows 7`) and, alone, would validate clean.
- S902: `mined`, two comma-separated paths both present → clean (comma split + trim confirmed).
- S903: `mined`, path absent → E11, exit 1.

**Consequence for the append:** rows may point at knowledge files that have not landed yet **only
while `status=queued`**. Any appended row staged as `mined` must have all its used-by paths already
on disk, or the gate fails with E11.

## Append-block check

`.ufo/waves/round-32/assimilation/append-block.md` **does not exist**. A whole-lane search for
`*append*` matches only unrelated round-24 fixtures
(`.ufo/waves/round-24/carry/fixtures/ReClosureNeighbour/W2*-…append….jsonl`). The round-32
`assimilation/` directory holds gate proofs and id lists only: `quarantine-slice`,
`guard-proof-{collisions,reg-ids,staged-ids}-{col0,tolerant}.txt`, `guard-proof-{staged,registry}-fixture.md`,
`collisions.txt`, `staged-ids.txt`, `reg-ids.txt`. **Zero cells to refuse — nothing is staged at the
named path.**

Composer checklist so the eventual append passes first time:

1. Exactly 11 columns per row; leading and trailing `|` present (NF=13).
2. Rows inside `## Registry` (exact heading, ≤3 leading spaces, never a tab), before the next `##`/`#`.
3. ids `S###` unique within SOURCES.md.
4. No URL reused within the same scope unless rejected/supersedes-noted; cross-scope reuse is only W04.
5. `opened` ≤ today UTC, real calendar date.
6. `recheck` mandatory: `NNd` or symbolic (`^[A-Za-z][A-Za-z0-9 _-]*$`); never `—`, never empty.
7. `used-by`: `—` for queued is safe and silent; mined rows need every path on disk (E11) and non-`—`
   (W03); tier C mined rows must keep `—` (W01). Multiple paths comma-separated, lane-root-relative.

## Verification record

- Full read of `scripts/sources-census.sh` (806 lines) — all cites above from that file.
- Live probe: throwaway fixture in `/tmp/census-verify.*` (removed), 9 rows exercising dangling
  queued/mined used-by, comma lists, `—` recheck, `90 days`, future/impossible `opened`, 3-space vs
  4-space indentation, plus the `--file` variant run from `/` (identical findings, lane label `file`).
  Output quoted in §7. No repo files mutated; script run read-only.
