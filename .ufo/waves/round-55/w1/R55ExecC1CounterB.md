# R55ExecC1CounterB — report

Deliverables (draft; L1 integrates):
- `.ufo/waves/round-55/w1/R55ExecC1CounterB/c1-r55-kbd-entry.py` (sha256 `b404c0cdcf9e33d8d9cee0a7c7fb85d7d6b827b6e9ab897957396a51057a1b1c`, stdlib only, executable)
- `.ufo/waves/round-55/w1/R55ExecC1CounterB/selftest-output.txt` (44 cases)

## What I did
Wrote the C1 counter from registration §C1 + claims-frozen §C1 + frozen-tables.json only. I did not open any other seat's counter
(I read only `quality/counters/c2-r51-dispatch-entry.py`'s first lines and grepped older counters for a `sources=` convention; none exists).
- Reads only git objects at `--rev` of `--repo`: `git ls-tree -z --full-tree` + `git cat-file blob`; only regular blobs (mode 100644/100755) are returned,
  so a committed symlink (file or directory) is never followed and counts as unreadable. Env: all `GIT_*` stripped, `TMPDIR=--work`, no global/system git config.
- `--repo` must be the repository root (or bare); `--rev` must resolve to a commit; else exit 2 with stdout `MADO_KBD_ENTRY: SETUP <reason>`.
- Embeds `TABLES_SHA256 = bf46c889…9490`; the tables actually used are the blob at `--rev` (so a tampered tree is evaluated and flagged `tables_sha`).
- Parser: no per-line regex. A cell scanner (`table_cells`) tokenises rows (starts at column 0 with `|`, ends with `|` after stripping trailing space/tab/CR;
  fenced code blocks skipped). Row ids / S-ids / URLs / dates use small hand-written scanners.
- Exit 0 only on TARGET_MET, 1 on a miss, 2 on setup error. Stdout is exactly one line.

Leg order in `missed=` (fixed): entry_absent, provenance, index, row:*, anchor:*, quote:*, pin_hash, source_cell:*, new_rows, host:*, tables_sha; ids K01..K18 then H01..H06.

## Commands and decisive output
```
python3 -I c1-r55-kbd-entry.py --selftest --repo <lane> --rev HEAD --work <scratch>
  -> MADO_R55_C1_SELFTEST: cases=44/44 verdict=OK   rc=0   (scratch dir empty and removed afterwards)
python3 -I c1-r55-kbd-entry.py --repo <lane> --rev HEAD --work <scratch>      (lane HEAD dbc2eef, entry not yet present)
  -> MADO_KBD_ENTRY: rev=HEAD rows=0/18 hosts=0/6 sources=0/18 new_rows=0/3 verdict=TARGET_MISSED missed=entry_absent,index,new_rows   rc=1
```
Selftest builds `git -C $D init` under `--work` (asserts `rev-parse --show-toplevel` == `$D`; commits with `-c user.name=ctl -c user.email=ctl@ctl`), generates
the good tree from `frozen-tables.json` (entry, README row, SOURCES rows S052 S162 S215 S316-S319 S378-S380) and the real pin bytes read from `--rev` of the lane.
Cases (each has the exact full output line in the file): good; the seven frozen controls CTL-1..7 (exact legs `entry_absent`, `quote:K04`, `anchor:K01`, `source_cell:K10`,
`row:K17`, `quote:H02,host:H02`, `pin_hash,tables_sha`); duplicated K05 / H01 rows; CRLF in entry+README+SOURCES (tolerated → TARGET_MET); trailing space/tab after every row
(tolerated); double-backtick quote (K02 → `quote:K02`) and no-backtick quote (K03); pin file replaced by a symlink (→ `quote:K08,quote:K09,pin_hash`); the whole `fetch/` dir
replaced by a symlink (→ all quote, pin_hash, all host legs); README row missing / duplicated / prose-only (`index`); three provenance mutants; four registry mutants
(`new_rows`, `source_cell:K18` with S380 not mined, S379 URL lacking the commit, K11 citing S317); tables blob + `\n` (`tables_sha`); short proposition; extra cell; wrong kind
cell on an H row; shifted H anchor; K07 row inside a code fence; backticked pipes in a proposition (tolerated); escaped `\|\|` in K16's quote (`quote:K16`); unbalanced
backtick in a proposition (`row:K05`); a committed-good tree whose working tree was edited afterwards (still TARGET_MET — worktree not read); CLI exit codes
(0 / 1 / 2 ×5 incl. bad rev, non-repo, missing args, unknown flag, tables blob absent) and one-line stdout exactness.

## Defects / ambiguities in the frozen contract (found with the input that shows them)
1. **K16 quote contains `||`**: frozen quote `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())` (legacy ConfigManager.cpp:1119) contradicts "no `|` inside a cell". A plain
   `split('|')` row parser sees 7 cells and drops K16 (my first selftest run did: `missed=row:K16` on the good tree). My scanner treats a `|` between two single backticks as part of the cell, so the
   raw row passes; the GFM-escaped form `\|\|` is byte-different from the frozen quote and misses `quote:K16`. Anyone writing the entry must use raw `||` inside the backticks (it renders badly in
   GFM but is what the frozen byte-equality demands). Any other counter/harness using naive splitting will reject the good entry.
2. **source_cell "contains the frozen commit" vs K17**: K17 cites the wayland pin, whose registry row (S052) URL is `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml`
   (no Hyprland commit; real S052 row confirmed). Read literally, K17 could never pass. I require the commit only for pins whose file name starts with `Hyprland-`.
3. `sources=<c>/<d>` undefined: I print `<K ids passing source_cell>/<18>`. `rows=` / `hosts=` = ids with no row/anchor/quote(/host) leg. `new_rows=<m>/<c1.new_rows_min>`.
4. `new_rows` literal reading: three qualifying rows with the *same* suffix would pass; I do not demand one row per `new_row_pins` suffix (that would exceed the frozen text).
5. "Opens with the provenance trio": I look at the lines before the first table row; `source:` needs an `S###` token on a `source:` line; `verified-at: 2026-10-28` as a prefix followed by end of line
   or a non-digit/non-`-` (trailing annotations accepted, as in existing entries); `recheck:` as a line prefix (non-empty value not demanded).
6. Strictness choices (tell the entry author): row lines must start at column 0; rows inside fenced code blocks do not count; an entry row with ≠5 cells, a K proposition <40 / H <20 chars,
   a K source cell not `S###`, or an H source cell not `host` is `row:<id>`; the anchor cell is exactly `<pin>:<line>` (no backticks); the quote cell is exactly one backtick-delimited span with
   the frozen text (double backticks, none, trailing text, or inner spaces → `quote:<id>`).
7. Dependent-leg policy: a missing/duplicated/malformed row emits only `row:<id>` (no anchor/quote/source/host for it); a pin unreadable as a regular blob emits `pin_hash` plus `quote:`/`host:` legs for
   the ids that need that pin's line; absent entry emits `entry_absent` only for entry-dependent legs (index, new_rows, pin_hash, tables_sha still evaluated).
8. CTL-7 as written changes the tree's `frozen-tables.json`, so a correct counter also prints `tables_sha`; the required leg `pin_hash` is present (`pin_hash,tables_sha`).
9. A duplicated `S###` registry row makes any K row citing it fail `source_cell` and is not counted in `new_rows` (ambiguous, so not trusted). The real SOURCES.md currently has 314 unique ids, all 11 cells.

## Not verified
- The counter ran against the real committed lane only at the pre-entry HEAD (`entry_absent`); the real entry/S378–S380/README row do not exist yet, so TARGET_MET on the real tree is untested.
  The synthetic good tree uses the real pin bytes and real frozen tables (so quote/anchor/pin_hash/host checks ran against real data); SOURCES/README/entry text is synthetic.
- `quality/check-r55-controls.py` does not exist yet; I did not run it or match its parsing of my line.
- No other seat's counter was compared. No hold-out path was seen or used. No tool installs; no host reads or mutations; no lane/fleet writes outside my deliverable dir; scratch removed.
