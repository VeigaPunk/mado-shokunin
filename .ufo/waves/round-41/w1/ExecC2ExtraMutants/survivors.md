# C2 extra mutants — survivors of PRED-C2-r41-v1 (round-41 w1)

Seat: `ExecC2ExtraMutants`. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Frozen predicate: `quality/counters/c2-r41-focus-entry.py` (`PRED-C2-r41-v1`, clauses a–i).
Frozen controls: `.ufo/waves/round-41/ctl/run-c2-controls.py` (41 controls, receipt
`.ufo/waves/round-41/receipts/ctl-c2.txt` 41/41).

**45 new mutants** of the admitted fixture `G`, none in the frozen list, scored in fixture repos
built exactly as the frozen `score()` builds them (`D=$(mktemp -d)`, `git -C D init -q`, toplevel
verified equal to `D` before the first commit, throwaway identity passed with `-c`, counter run as
`python3 -I quality/counters/c2-r41-focus-entry.py --repo D --rev A --base B`).
Observed final line of the run (`results.txt`, `results.json`):

```
CTL_C2_EXTRA: mutants=45 survivors=29/45
```

Baselines: `G` (the frozen admitted fixture) `admitted=1/1` all clauses 1; `G2` (a variant base
with a second held row, used only by M22) `admitted=1/1`. **29 of 45 mutants survive** — the
counter admits each of them with `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1`.

## Survivors (29)

Severity: **HIGH** = a defective entry passes; **MED** = a normalization/threshold weakness lets a
defective-but-plausible entry pass; **LOW** = the strict reading of the clause is violated, the
literal reading is arguable; **BENIGN** = survives by design (recorded, not a defect).

| # | mutant | what the fixture does | clause that should kill it | sev |
|---|---|---|---|---|
| 1 | `M01-citation-past-line-20` | appends `source: S305` at entry line 23, no registry row, no gate | c (every cited id has exactly one row) | HIGH |
| 2 | `M02-cited-id-lowercase` | `source: s304` + row id `s304`: the entry cites a source with no visible row | b/c (case-insensitive citation) | HIGH |
| 3 | `M03-two-entry-lines-per-id` | two `**OBS** S301 …` lines carry the same Gate quote | g ("one entry line" per id) | LOW |
| 4 | `M04-one-line-serves-two-ids` | one line names `S301 S303` and carries both quotes (one nested in the other) | g (one line per id) | MED |
| 5 | `M05-quote-across-paragraphs` | receipt is `<p>hyprland focus grab manager</p> <p>interface commit request</p>`; quote only exists after tag stripping | d (quote occurs in the receipt) | MED |
| 6 | `M06-gate-line-outside-section` | a conflicting `GATE S301` with a zero sha placed under `## Receipts` | d (EXACTLY ONE GATE line per id) | LOW |
| 7 | `M08-receipt-symlink` | the `S301` receipt is a git symlink; its blob is a 532-byte target path containing the quote | d (the receipt is committed source bytes) | HIGH |
| 8 | `M09-new-row-recheck-junk` | new row `S301` recheck cell = `TBD` | c (a new row's recheck cell is never read) | HIGH |
| 9 | `M10-new-row-no-location` | new row `S304` cell 1 = `focus control surfaces` (no source at all) | e (cell 1 must end with a location) | HIGH |
| 10 | `M11-badloc-in-anchor-cell` | `https://amgsk.dev/posts/hyprland-rules/` in the new row's anchor cell, cell 1 clean | i (localized channel excluded) | MED |
| 11 | `M12-quote-whitespace-variant` | `S304`'s quote equals `S301`'s after whitespace collapse (double space) | d (quotes distinct after normalization) | MED |
| 12 | `M13-refuse-reason-20-filler` | `REFUSE … reason=aaaaaaaaaaaaaaaaaaaa` | i (a reason must be prose, not 20 filler chars) | MED |
| 13 | `M14-admit-self` | `ADMIT corpus/knowledge/hyprland-focus-grab-r41.md as <same path>` | i (the admitted path must be a staged package) | HIGH |
| 14 | `M15-admit-nonexistent-package` | `ADMIT merge/mado/…/does-not-exist-r99.md as <entry>` | i (the admitted package must exist) | HIGH |
| 15 | `M16-journal-no-boot-line` | journal with 3 sessions from PID changes only, zero `-- Boot` lines | h (a session needs a boot boundary) | MED |
| 16 | `M17-journal-duplicate-sessions` | one 24-advert block replayed 3× with PIDs 1900/1901/1902, all timestamps identical | h (replayed blocks are not sessions) | MED |
| 17 | `M18-quote-entity-encoded` | plain-text receipt holds `&#104;yprland focus grab …`; the quote exists only after `html.unescape` | d (literal occurrence in a text receipt) | MED |
| 18 | `M19-recheck-impossible-date` | `recheck: 2026-99-99` | b (a real date or interval) | MED |
| 19 | `M20-fenced-verified-at` | real front-matter `verified-at: 2026-10-23` / `recheck: whenever`; a fenced block earlier in the head says `2026-10-25` / `90d` | b (fences are removed before any line is matched) | HIGH |
| 20 | `M21-held-row-usedby-substituted` | held row `S050` loses `corpus/knowledge/old.md` from used-by, keeps only the entry | c (used-by must be a superset) | MED |
| 21 | `M22-two-new-ids-only` | 4 cited ids of which only 2 are new (S050, S051 held; S301, S302 new) | c (docstring: at least 3 new ids) | HIGH |
| 22 | `M23-admit-inside-fence` | the only `ADMIT` line sits inside a fence in `## Gate` | i (lesson lines are not unfenced) | MED |
| 23 | `M24-gate-lines-inside-fence` | every `GATE` line sits inside its own fence in `## Gate` | d (lesson lines are not unfenced) | MED |
| 24 | `M25-refuse-same-package` | `REFUSE` names the same package the `ADMIT` admits | i (refused ≠ admitted) | MED |
| 25 | `M26-location-url-fragment` | new row `S304` location `https://example.org/a.xml#frag`, the same document as `S301` | e (locations unique after URL normalization) | LOW |
| 26 | `M27-source-inside-fence` | `source: S304` sits inside a fence in the head | b (fences are removed before any line is matched) | HIGH |
| 27 | `M28-source-moved-past-line-20` | `source: S304` moved to line 22: the citation leaves the id set entirely | b/c (a citation must not escape the id set) | HIGH |
| 28 | `M29-source-id-cited-twice` | `source: S301` twice in the head | none — "distinct" is by design | BENIGN |
| 29 | `M30-quote-split-by-newline` | the receipt wraps the quote across a newline | none — normalization of wrapped text is by design | BENIGN |

## Mechanism, per survivor

Quoted counter lines are located by `file:line` and machine-checked by `check-quotes.py`
(`quote check: 25/25`, every quote <= 25 words).

### 1. `M01` / `M28` — clause b's id set is "the first 20 raw lines", nothing else
`head` is the raw first 20 lines and `ids` comes only from `SRC_RE.match` over that head:
> "head = text.splitlines()[:20]" — quality/counters/c2-r41-focus-entry.py:188
> "SRC_RE = re.compile(r\"^source:\\s*(S\\d{3,})\\b\")" — quality/counters/c2-r41-focus-entry.py:82

Every other clause (c, d, e, g) iterates `ids`. A `source:` line at line 23 (M01) or a citation
moved past line 20 (M28) is therefore a citation that no row, no gate line and no entry line has
to support. `evidence.txt` §A: `M28 … ids=['S050','S301','S302','S303'] … tail citations:
['source: S304 - docs']` — the entry cites S304 while the counter's id set does not contain it.

### 2. `M02` — a lowercase id is invisible to both the citation and the row grammar
> "ROW_RE = re.compile(r\"^ {0,3}\\|\\s*(S\\d{3,})\\s*\\|\")" — quality/counters/c2-r41-focus-entry.py:78

`source: s304` matches neither `SRC_RE` (line 82) nor `ROW_RE` (line 78). `evidence.txt` §A:
`M02 … L7 'source: s304 - docs'` with `ids=['S050','S301','S302','S303']` and the `| s304 |` row
present but unparsed. The entry cites a source for which no row exists — the exact defect clause c
is written to catch.

### 3. `M08` — the receipt can be a symlink: its "bytes" are a path string
> "blob = show(repo, rev, path) if path.startswith(FETCH) else None" — quality/counters/c2-r41-focus-entry.py:243
> "if (blob is not None and len(blob) >= MIN_RECEIPT" — quality/counters/c2-r41-focus-entry.py:244

`git show REV:path` returns the link target for mode `120000`; nothing checks the mode.
`evidence.txt` §D: `ls-tree: 120000 blob fd8e885c… .ufo/waves/round-41/fetch/S301.link.txt`,
`show bytes=532 sha256=562be874…`, `gate sha256 in lesson: 562be874…` — a 532-byte path string
satisfies `len >= MIN_RECEIPT`, the sha256 and the quote. No source byte is committed.

### 4. `M09` — a new row is validated only on status, used-by and opened
> "good &= cells[8] == OPENED" — quality/counters/c2-r41-focus-entry.py:221

`cells[7]` (status), `cells[10]` (used-by) and `cells[8]` (opened) are read for a new row; tier,
scope, anchor, teaches and recheck (cells 3–6, 9) are never inspected. `| TBD |` in the recheck
cell of a new row is admitted.

### 5. `M10` — clause e's "location" is just the last token of cell 1
> "loc = cells[1].split()[-1] if cells[1].split() else \"\"" — quality/counters/c2-r41-focus-entry.py:268

A cell 1 of `title - focus control surfaces` yields `loc='surfaces'` (`evidence.txt` §H), which is
unique, so a new row with no source at all passes e.

### 6. `M11` — the localized-channel ban reads cell 1 only
> "bad |= any(b_ in rows[0][1] for b_ in BAD_LOC)" — quality/counters/c2-r41-focus-entry.py:312

`rows[0][1]` is the source cell; the anchor cell (`rows[0][5]`) is never checked, so
`https://amgsk.dev/posts/hyprland-rules/` in the anchor cell is admitted (`evidence.txt` §H:
`anchor='https://amgsk.dev/posts/hyprland-rules/'`).

### 7. `M12` — quote distinctness compares raw strings, not normalized ones
> "and quote not in seen_quote" — quality/counters/c2-r41-focus-entry.py:248

`S304`'s quote differs from `S301`'s only by a double space: raw-distinct, `norm()`-equal
(`evidence.txt` §F: `raw distinct=True norm equal=True`). Two ids then share one quote.

### 8. `M05` / `M18` / `M30` — `norm()` makes a quote out of text that is not contiguous
> "return re.sub(r\"\\s+\", \" \", html.unescape(text)).strip()" — quality/counters/c2-r41-focus-entry.py:119

Tag stripping, entity decoding and whitespace collapse all run on every receipt. `evidence.txt` §E:
`norm(M05 html) contains quote: True (raw contains: False)`, `norm(M18 entity) contains quote: True
(raw contains: False)`, `norm(M30 newline) contains quote: True (raw contains: False)`. M05 and M18
are defects (two `<p>` blocks joined; `&#104;` decoded in a plain-text receipt); M30 is benign.

### 9. `M06` — "exactly one GATE line" is scoped to one section
> "for line in section(lesson, \"## Gate\"):" — quality/counters/c2-r41-focus-entry.py:228

A second, conflicting `GATE S301` under any other `## ` heading is invisible, so the gate section
can disagree with a stale line elsewhere in the same lesson file.

### 10. `M13` / `M14` / `M15` / `M25` — clause i's two regexes and nothing else
> "REFUSE_RE = re.compile(r\"^REFUSE (\\S+\\.md) reason=(.{20,})$\")" — quality/counters/c2-r41-focus-entry.py:90
> "ADMIT_RE = re.compile(r\"^ADMIT (\\S+\\.md) as (\\S+\\.md)\\s*$\")" — quality/counters/c2-r41-focus-entry.py:89

Nothing checks that the admitted path exists, that it is under the staged package, that it differs
from the entry, or that the refused path differs from the admitted one; and 20 filler characters
satisfy `reason=.{20,}`.

### 11. `M20` / `M27` — clause b uses the raw head although the preamble says fences are removed
> "corpus/knowledge/hyprland-focus-grab-r41.md. Fenced code blocks (``` ... ```) of" — quality/counters/c2-r41-focus-entry.py:6
> "the entry and of the README are removed before any line is matched. It is" — quality/counters/c2-r41-focus-entry.py:7

`lines = unfenced(text)` is used for f, g, h and the census line, but `head` (line 188) is raw.
`evidence.txt` §A for M20: the fenced `L4 'verified-at: 2026-10-25'` / `L5 'recheck: 90d'` shadow
the real `L13 'verified-at: 2026-10-23'` / `L14 'recheck: whenever'`, because `hv()` returns the
first match. This is a direct contradiction of the counter's own preamble for clauses b and c.

### 12. `M23` / `M24` — the lesson is never unfenced
> "admits = [m for m in map(ADMIT_RE.match, section(lesson, \"## Gate\")) if m]" — quality/counters/c2-r41-focus-entry.py:306
> "refuses = [m for m in map(REFUSE_RE.match, section(lesson, \"## Gate\")) if m]" — quality/counters/c2-r41-focus-entry.py:307

`unfenced()` is applied to the entry and the README only, so an `ADMIT` line or a `GATE` line inside
a fence in `## Gate` is still counted. (The preamble names only the entry and the README, so this is
a MED: the blind spot is that a fence hides nothing from clauses d and i.)

### 13. `M21` — cells 1-10 byte-equality deliberately excludes used-by, without a superset check
> "and old[0][:10] == cells[:10]" — quality/counters/c2-r41-focus-entry.py:218

The held row is allowed to gain the entry in cell 11 (index 10) — correct — but the same exclusion
lets it *lose* every pre-existing used-by item. `evidence.txt` §G: base used-by
`corpus/knowledge/old.md`, mutant used-by `corpus/knowledge/hyprland-focus-grab-r41.md`.

### 14. `M22` — code and docstring disagree on the new-id floor
> "registry (at least 3) carry opened 2026-10-25; ids present at BASE keep" — quality/counters/c2-r41-focus-entry.py:17
> "cl[\"c\"] = int(rows_ok and len(new_ids) >= 2)" — quality/counters/c2-r41-focus-entry.py:225

Docstring clause c says "at least 3"; the code requires 2. `evidence.txt` §B:
`cited=['S050','S051','S301','S302'] new=['S301','S302']` → `admitted=1/1`. This mutant needs a
base with a second held row (the fixture's `G2`), because 4 citations must still be distinct.

### 15. `M16` / `M17` — the journal parser accepts evidence a saved journal cannot contain twice
> "if BOOT_RE.fullmatch(line):" — quality/counters/c2-r41-focus-entry.py:160
> "if cur is None or changed or pid != cur[0]:" — quality/counters/c2-r41-focus-entry.py:167
> "h_ok = (got == jc and jc[0] >= 2 and jc[1] >= 40 and jc[2] >= 20" — quality/counters/c2-r41-focus-entry.py:283

`-- Boot` is optional (a PID change opens a session) and timestamps are never compared. `evidence.txt`
§C: `M16-no-boot counts(S,A,D,F)=(3, 72, 24, 1) bootlines=0`; `M17-replayed counts=(3, 72, 24, 1)
bootlines=0 first_ts=2026-10-25T13:10:00-03:00 last_ts=2026-10-25T13:10:00-03:00` — the replay is
visible in the identical first/last timestamps and is not rejected. The real host receipt
(`fetch/xdph-journal.txt`) does carry one `-- Boot` line, so a "≥ 1 BOOT" rule would not break the
data.

### 16. `M19` — `RECHECK_RE` accepts any `NNNN-NN-NN`
> "RECHECK_RE = re.compile(r\"^(\\d{4}-\\d{2}-\\d{2}|\\d+d|on-[a-z-]+)(\\s|$)\")" — quality/counters/c2-r41-focus-entry.py:81

`2026-99-99` matches; no calendar validation.

### 17. `M26` — location uniqueness is exact string equality
`loc` (line 268) is compared to `r[1].split()[-1]` verbatim, so `…/a.xml#frag` and `…/a.xml` are two
different locations for the same document.

### 18. `M03` / `M04` — clause g is `any(...)`, not "one line"
> "hit = any(re.search(r\"\\b%s\\b\" % i, l) and q in l" — quality/counters/c2-r41-focus-entry.py:298

An id may have any number of supporting lines (M03), and one line may carry two ids at once when one
quote is nested in the other (M04: `grab manager interface commit` ⊂ `hyprland focus grab manager
interface commit request`). Both still give every id "a line", so the defect is that clause g cannot
distinguish a per-id attribution from a shared one.

## Killed (16) — the counter's teeth on the same axes

| mutant | observed | killing clause |
|---|---|---|
| `M07-receipt-dot-segment` | `admitted=0/1` `d:0 g:0` | d — `git show` refuses `./` in a path |
| `K01-ten-cell-row` | `admitted=0/1` `c:0` | c — 11 cells |
| `K02-quote-case-differs` | `admitted=0/1` `d:0 g:0` | d — quote occurs in the receipt |
| `K03-gate-extra-field` | `admitted=0/1` `d:0 g:0` | d — `GATE` line shape |
| `K04-refuse-reason-19-chars` | `admitted=0/1` `i:0` | i — `reason >= 20` chars |
| `K05-verified-at-past-line-20` | `admitted=0/1` `b:0` | b — head is 20 lines |
| `K06-source-past-line-20` | `admitted=0/1` `b:0` (two source lines moved) | b — >= 4 distinct source lines in the head |
| `K07-journal-single-space-log` | `admitted=0/1` `h:0` | h — `[LOG]  | ` grammar |
| `K08-focus-grab-earlier-session` | `admitted=0/1` `h:0` | h — F is the latest session |
| `K09-row-four-space-indent` | `admitted=0/1` `c:0` | c — 0-3 leading spaces |
| `K10-two-readme-rows` | `admitted=0/1` `f:0` | f — exactly one index row |
| `K11-two-own-work-rows` | `admitted=0/1` `h:0` | h — exactly one new own-work row |
| `K12-journal-line-double-space` | `admitted=0/1` `h:0` | h — census line verbatim |
| `K13-admit-path-with-spaces` | `admitted=0/1` `i:0` | i — `ADMIT` line shape |
| `K14-receipt-dotdot-segment` | `admitted=0/1` `d:0 g:0` | d — `git show` refuses `..` in a path |
| `K15-readme-row-other-name` | `admitted=0/1` `f:0` | f — the row must name this entry |

Clause a's guard also holds: `SETUP-entry-present-at-base rc=2
PRED-C2-r41-v1 SETUP precondition_failed entry_present_at_base
corpus/knowledge/hyprland-focus-grab-r41.md`.

Note the two receipt-path traversal mutants (M07, K14) are killed by git's path handling, not by the
counter: `git show REV:fetch/./S301.html` and `REV:fetch/../fetch/S301.html` both fail with
`fatal: path … exists on disk, but not in …` (probed before the run).

## Root causes, ranked

1. **The head is raw** (line 188): clauses b and c read fenced text and ignore line 21+, contradicting
   the preamble (lines 6-7). Kills M20, M27, M28, M01, M02's cousin class. Cheapest fix: `head =
   unfenced(text)[:20]` and case-insensitive id extraction.
2. **Receipts are blobs, not files** (lines 243-244): no mode check → symlink receipts (M08).
3. **Clause c stops at four cells** (line 221/225): new-row recheck/tier/scope/anchor/teaches
   unread (M09), the new-id floor is 2 not 3 (M22), used-by is not a superset (M21).
4. **`norm()` is applied to every receipt** (line 119): entity decoding and tag stripping manufacture
   quotes across non-adjacent blocks (M05, M18).
5. **Clause i is two regexes** (lines 89-90): no package existence, no self-admit, no admit/refuse
   distinctness, 20 filler chars pass (M13-M15, M25).
6. **Clause h has no provenance floor** (lines 160/167/283): no boot line required, no timestamp
   monotonicity (M16, M17).
7. **The lesson is never unfenced** (lines 228/306/307) and **clause e/d compare raw strings**
   (lines 248/268): fenced gate/admit lines count (M23, M24), whitespace-variant quotes (M12) and
   fragment-variant locations (M26) pass.
8. **Clause g is `any()`** (line 298) and **clause i's BAD_LOC reads one cell** (line 312):
   shared attribution lines (M03, M04), localized channel in the anchor cell (M11).

## Reproduce

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/w1/ExecC2ExtraMutants
python3 extra-mutants.py     # 45 mutants; writes results.txt-equivalent stdout + results.json
python3 evidence.py          # mechanism facts (evidence.txt)
python3 check-quotes.py      # verifies every quote in this file at its file:line
```

`extra-mutants.py` imports the frozen runner with `importlib` (`main()` is `__main__`-guarded, never
run) and reuses `base_files()`, `admitted()`, `row()`, `gate_line()`, `set_receipt()`,
`with_journal()`, `journal()`, `QUOTES`, `FILLER`, `ADMIT`, `REFUSE`. The only delta from the frozen
`score()` is an optional `links` mapping that creates git symlinks after the regular files are
written and before `git add -A` (M08 cannot be expressed by the frozen writer). Every fixture repo
is removed in a `finally`; nothing in the lane is written.
