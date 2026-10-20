# RevNavigation — round 18 W1 (navigation counter for the two new route notes)

Scope: what the two round-18 notes must add to `corpus/README.md` so the
SCORECARD fleet-round-1 navigation Counting command stays complete, and the
exact row format. Read-only review: no lane VCS write, no host command; the
rehearsal ran only in my own `/tmp/nav-r18*` git sandbox built from
`git archive d9a5a18`. No tool was installed or updated.

## 1. The instrument (as published, unchanged)

Source of truth: `SCORECARD.md` → `## Fleet round 1 — coverage navigation`
→ `### Counting command` (the fenced `bash` block). Its body (fence minus the
newline that follows ```` ```bash ````) hashes to
`8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88`,
the literal-wrapper SHA the SCORECARD records. No edit to that block is
needed this round; `harm-watch.sh` is assigned to run that same block with
`REV`.

What it does at one revision:

- notes: `git ls-tree --name-only REV:corpus/knowledge`, **non-recursive**,
  filtered `.md`. Only top-level files count.
- rows: `git show REV:corpus/README.md`, then
  `re.findall(r"^\| `knowledge/([^`]+\.md)`", index, re.M)` — the row must
  **begin** with `| ` + a backticked `knowledge/<name>.md`.
- verdict: exit 1 if any note lacks a row (`missing`), any row lacks a note
  (`dangling`), or any note name is matched ≠ 1 time (`duplicates`);
  otherwise exit 0. `coverage = 10 × covered / len(notes)`.
- It reads committed bytes only: worktree edits are invisible.

Baseline receipts (run read-only against the lane):

```text
revision=d9a5a18e17cd3a68b52148fcc01c4a30e340ba98 indexed=32/32 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0
revision=d3a00003e6ef0b1e3c7b4faf52d592eb293857ba indexed=32/32 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0
```

So the post-C2 expectation is **34/34**, not 32/32: 32 existing notes +
`walker-route-r18.md` + `theme-route-r18.md`, each with exactly one row.
Required final receipt line:

```text
revision=<final-sha> indexed=34/34 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0
```

(State at report time, 2026-10-20T15:47Z: both notes exist in the worktree as
untracked files still being written by their scribes — `walker-route-r18.md`
and `theme-route-r18.md`, each with its `surface: P3` / `surface: P5` line on
line 4 — but committed `refs/heads/master` = `d3a0000` still measures 32/32.
The 34 denominator exists only at a revision where both notes are committed.)

## 2. Exact rows to add

Both rows land as the last two rows of the `| Note | Holds | Sources |`
coverage-map table, immediately after the
`| \`knowledge/terminal-route-r17.md\` ... |` row (line 43 today), i.e. as
lines 44–45 before the blank line that precedes `## Quality bar`. Exact
byte form (the part before the first cell boundary is load-bearing; the cell
text is not):

```text
| `knowledge/walker-route-r18.md` (round 18; surface P3) | <Holds: what the note's Upstream contract + Host declaration establish> | `source:` <assigned ids S072–S099> in [SOURCES](SOURCES.md); <fetch receipts path + host-bytes-by-sha256 statement> |
| `knowledge/theme-route-r18.md` (round 18; surface P5) | <Holds: same> | `source:` <assigned ids S072–S099> in [SOURCES](SOURCES.md); <fetch receipts path + host-bytes-by-sha256 statement> |
```

`.ufo/waves/round-18/drafts/FrontierDraft.md` (sha256
`a3975065bd6b0bfbab3e0bf842717095f5cd47a480c6a984f46bfc5b2c8c499e`) already
contains two rows in this exact shape at its lines 22–23; its rows block
(sha256 `3e2e4fde97590c17f8437a642ae0d5cad2a94ca2e1154d0eb3123589d214dcfa`)
was rehearsed as-is. The literal rows, verbatim (only `S0xx-pending` must
become the assigned ids before commit):

```text
| `knowledge/walker-route-r18.md` (round 18; surface P3) | Documentary upstream contract for Walker and elephant, joined to declared host config by sha256 and line anchor. Declared configuration is not observed launcher behaviour; provider resolution at runtime, the elephant service, socket protocol and rendered UI stay `[UNK]`. | `source:` S0xx-pending in [SOURCES](SOURCES.md); tag-pinned fetch receipts under `.ufo/waves/round-18/fetch/NoteWalker/`. No walker or elephant process is started or queried. |
| `knowledge/theme-route-r18.md` (round 18; surface P5) | Documentary upstream contract for the omarchy theme-set and wallpaper path and for swaybg, joined to `current/theme`, the current background link and consumer imports by sha256 and line anchor. Declared chain is not runtime theme application; reload effects and rendered wallpaper stay `[UNK]`. | `source:` S0xx-pending in [SOURCES](SOURCES.md); tag-pinned fetch receipts under `.ufo/waves/round-18/fetch/NoteTheme/`. No theme, wallpaper or swaybg command is run. |
```

Byte-level constraints the regex imposes (each verified with the literal
pattern, §4):

1. The line starts exactly `| ` (pipe, one ASCII space) then a backtick,
   `knowledge/`, the filename, `.md`, a closing backtick. No indentation, no
   list bullet, no second space after the pipe, no missing backticks.
2. The filename inside the backticks is byte-identical (case included) to
   the committed note's basename at `corpus/knowledge/`; the note must be
   top-level there, never in a subdirectory.
3. Exactly **one** matching line per note across the whole README — not one
   per table. A second line of this shape anywhere (a "see also" table, a
   duplicated insert) is `duplicates=1` and exit 1. Markdown links
   `[label](knowledge/...)` and the `## Frontier` `-` bullet do not match.
4. Rows and notes must be present at the **same measured REV**. Rows-only
   is `dangling`; notes-only is `missing`; either exits 1. Landing them in
   one integration commit is the safe order.
5. The `(round 18; surface P3)` / `(round 18; surface P5)` annotation is
   convention copied from the round-17 rows, not parsed. Keep it consistent
   with each note's own `surface:` line so the index is honest.
6. The Sources cell is not parsed by this counter, but `S0xx-pending` must
   not land in a committed index: substitute the ids L1 assigns (reserved
   S072–S099) from `corpus/SOURCES.md`.

## 3. Findings

No defect in the drafted rows with respect to the navigation counter: the
rehearsal with those exact rows and two stub notes at the prescribed paths
gives `indexed=34/34 ... exit=0`.

- **High attention — single-revision landing.** The navigation block reads
  committed bytes only (`git ls-tree` / `git show`), not the worktree. If the
  notes and the two rows are split across commits, every intermediate REV is
  either `missing=2` or `dangling=2` (exit 1). Land both notes plus both rows
  together; run the final counter at that commit.
- **High attention — per-note row complement.** Rows and notes must pair
  one-for-one at the measured REV: two notes + one row is `missing=1`; one
  note + two rows is `dangling=1`. If integration lands one note first, land
  exactly its row; the 34/34 pair is the declared round target, not a rule
  for every intermediate commit.
- **Medium — placeholder source ids.** `FrontierDraft.md` rows say
  `S0xx-pending`. Navigation passes anyway (the cell is unparsed), but a
  committed index citing a non-existent source token contradicts SOURCES
  ownership and will be read as a source claim. Replace with the final ids
  before the row lands; the ids must be the ones whose SOURCES `used-by`
  names `corpus/knowledge/walker-route-r18.md` / `theme-route-r18.md` (the
  c2 join), or C2 will reject the note while navigation still passes.
  The note heads carry the same placeholders (`theme-route-r18.md:1` shows
  `S0xx-pending-A…D`, `walker-route-r18.md:1` shows bare `S0xx-pending`;
  c2's token regex matches `S\d{3}` only), so re-point the notes' `source:`
  lines too, not just the README cells.
- **Medium — subdirectory trap.** The navigation counter uses
  `ls-tree --name-only` (non-recursive); `measure.py` c2 uses `ls-tree -r`.
  A note written to `corpus/knowledge/r18/...` would be visible to C2 but
  invisible here, and its row would be `dangling` (exit 1). Keep both notes
  top-level.
- **Low — duplicate-shape risk outside the table.** The drafted
  `## Frontier` bullet is a `-` bullet with markdown links and adds no
  matching line (verified). Do not convert it, or a route-table entry, into
  a `| \`knowledge/...\`` row; that would duplicate the coverage-map row.
- **Low — route-table discoverability is not measured.** The README
  `Province routes` table's Walker/Themes rows still point only at older
  notes; updating them is optional, not required by this counter, and no
  committed script recomputes the historical fleet-round-1 link smoke
  (grep finds only the JSON receipt, no runner).

## 4. Rehearsal receipts (my sandbox only)

`/tmp/nav-r18` is a throwaway git repo seeded from
`git archive d9a5a18` (32 notes / 32 rows) with the published block fed via
`bash -s` and `REV` exported.

| Case | Revision | Observed |
|---|---|---|
| baseline | `27adb09e` (tree = d9a5a18) | `indexed=32/32 ... coverage=10.0000/10`, exit 0 |
| notes only, no rows | `1decb084` | `indexed=32/34 missing=2`, exit 1 |
| FrontierDraft rows + notes | `81e6d856` | **`indexed=34/34 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0**; rows at README lines 44–45 |
| same rows + the real note bytes read at 15:46Z | `59270bd4` | `indexed=34/34 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0 |
| duplicate walker row | `24d319cd` | `duplicates=1`, exit 1 |
| rows only, no notes | `7d313342` | `dangling=2`, exit 1 |
| note under `corpus/knowledge/r18/` | `fa0b64a9` | note invisible; `dangling=1`, exit 1 |

Regex micro-test against the literal pattern: canonical row matches
(`walker-route-r18.md`); these do **not**: `|  ` (two spaces),
one-space indent, `| knowledge/...` without backticks,
`- [route](knowledge/...)`, and
`| Walker | [route](knowledge/...) | ... |`.

## 5. Residual risk / verification gaps

- The real notes are not committed yet (both exist as untracked worktree
  files, still growing). The 34/34 receipt must be produced by harm-watch at
  the final integrated REV; I cannot certify a commit that does not exist.
- The counter is navigation-only: it never reads cell prose, source ids, the
  note's `surface:` line, headings, or content. A malformed note still
  counts 1/1. Conversely C2 (`measure.py` c2) never reads README, so the row
  is not a source or surface proof — the note's own head must carry
  `surface: P3` / `surface: P5`, the four exact H2 headings with ≥3
  non-blank body lines, `[UNK]` in `## Unexercised behavior`, and a
  `source:` S### whose mined tier-A used-by names the full note path plus an
  upstream https docs/spec/code row matching the P3/P5 keywords.
- Keep the Counting-command fence byte-identical. Its body hash is
  `8b59b503…`; if a later SCORECARD edit rewrites the block, the harm-watch
  extraction measures a different instrument from the recorded one.
