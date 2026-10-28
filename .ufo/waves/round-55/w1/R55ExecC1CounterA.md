# R55ExecC1CounterA — c1-r55-kbd-entry.py (round 55, wave w1)

## What I did
Wrote the strict C1 counter for registration §C1 and its `--selftest`. Deliverables:
- `.ufo/waves/round-55/w1/R55ExecC1CounterA/c1-r55-kbd-entry.py` (sha256 `d98a9f87413441b5f013756528504d44e50c17e7b07f904ebe772919653182d6`; ships to `quality/counters/c1-r55-kbd-entry.py`)
- `.ufo/waves/round-55/w1/R55ExecC1CounterA/selftest-output.txt` (selftest, two counter-mutants, real-lane runs, dry integration run)

Design: `python3 -I`, stdlib only. Every byte is read through git objects (`rev-parse`, `ls-tree -z`, `cat-file blob`) with a scrubbed env (HOME/TMPDIR=`--work`, no global git config, literal pathspecs). The working tree is never opened. Only regular blobs (100644/100755) count; a symlink blob, or a path under a symlinked directory, is absent. `--work` is required (created if missing, must be writable); the counter writes nothing; selftest writes only under `<work>/selftest-<pid>` and removes it. The sha256 of `frozen-tables.json` (`bf46c889…9490`) is embedded and checked against the blob read. Stdout is exactly the frozen line; exit 0 on TARGET_MET, 1 on a miss, 2 on a setup error (reason on stderr, stdout empty).

Legs emitted in order: `entry_absent, provenance, index, row:, anchor:, quote:, pin_hash, source_cell:, new_rows, host:, tables_sha`.

## Commands and decisive output
- `python3 -I c1-r55-kbd-entry.py --selftest --repo <lane> --rev HEAD --work <scratch>` → `MADO_KBD_ENTRY_SELFTEST: 50/50 passed`, rc 0. Each case builds its own scratch git repo (`mktemp -d -p <work>`, `git -C "$D"` everywhere, toplevel asserted before the first commit, `-c user.name=ctl -c user.email=ctl@ctl`) from a synthetic good tree generated from `frozen-tables.json` plus the 10 real pins, and runs the counter as a child process (`python3 -I`), comparing the exact `missed=` string and the exit code.
  - the 7 frozen controls: CTL1 `entry_absent`; CTL2 `quote:K04`; CTL3 `anchor:K01`; CTL4 `source_cell:K10`; CTL5 `row:K17`; CTL6 `quote:H02,host:H02`; CTL7 `pin_hash,tables_sha`.
  - the asked-for strictness cases: whole-file CRLF (`provenance` + all 24 `row:`), a single CRLF row (`row:K05`), trailing spaces / a trailing tab after a row (`row:K09`, `row:H01`), a duplicated row id identical and differing (`row:K03`, `row:H05`), double-backtick quote cell (`quote:K05`), no-backtick cell (`quote:H06`), a symlink pin file (`quote:K10,pin_hash`), a symlinked pin directory (all quote:*, `pin_hash`, all host:*), a symlinked entry (`entry_absent`) and SOURCES.md (all `source_cell:*`, `new_rows`).
  - others: row only inside a code fence / HTML comment, short propositions, extra pipe in a proposition, wrong host cell, wrong anchor pin file, quote with changed spacing (K18), provenance (no recheck, no S-id, wrong date), README row missing/duplicated, S379 used-by lacking the entry, S380 not `mined`, tables absent / trailing newline / bad shape with wrong sha, S215 accepted for K15, repo path given as a symlink, uncommitted working-tree vandalism ignored, rev as full sha, determinism, bad rev / bad repo / missing `--work` (rc 2, empty stdout), a commit with none of the files.
- Counter mutants: accepting symlink blobs → selftest `49/50` (symlink-entry-file fails); disabling the anchor compare → `48/50` (CTL3 and anchor-wrong-pin-file fail).
- Real lane: at `HEAD` `rows=0/18 hosts=0/6 sources=0/18 new_rows=0/3 verdict=TARGET_MISSED missed=entry_absent,index,new_rows` rc 1; at base `3b55b6e` `missed=entry_absent,index,tables_sha` rc 1 (the base has no frozen-tables.json).
- Dry run on a scratch repo of lane HEAD's tables/pins/README/SOURCES plus the scribes' drafts (R55ScribeEntryA `entry.md`, R55ScribeIndex README row, R55ScribeSources S378–S380 rows): `MADO_KBD_ENTRY: rev=HEAD rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none` rc 0. This is a draft-integration dry run, not the integrated tree.

## Defects / ambiguities (with the input that shows them)
1. **Contract conflict, K16.** Registration says "no `|` inside a cell" but the frozen K16 quote is `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())`, which holds `||`. I split the row on the 3-byte separator ` | ` (which `||` does not match) and forbid `|` only in cells 1–4; the quote cell may hold pipes and must equal the frozen bytes. A renderer that splits on every pipe would break that row; the contract (byte-equal) wins. The first selftest run hit this (tables shape check rejected K16) before I fixed it.
2. **`source_cell` "contains the frozen commit" cannot hold for S052** (gitlab wayland 1.26.0 URL). I require the commit only for `Hyprland-*` pins; the wayland pin must match its suffix `1.26.0/protocol/wayland.xml`.
3. **Registration gives no per-row S-id.** `source_cell:<id>` accepts any single registry row (status `mined`, URL suffix match) so S215/S318 are both fine for K13–K15.
4. **`new_rows` count** is the number of `new_row_pins` pins covered by ≥1 qualifying row (not a raw row count), so two rows with the same suffix cannot stand in for a missing third.
5. **CTL-7 prints `pin_hash,tables_sha`**, because the control edits the tree's `frozen-tables.json`, which also breaks the embedded sha. The required leg `pin_hash` is present; the harness must not demand `missed==pin_hash` alone.
6. **CTL-6 prints `quote:H02,host:H02`** (a forged cell differs from the frozen quote and from the pin line).
7. Strict choices the contract does not spell out: a CRLF or trailing-space row is `row:<id>`; the trio must sit in the first 30 lines, with `verified-at: 2026-10-28` as an exact line; rows in fences/HTML comments are not rows; unknown extra ids (K19, H07) are ignored; `entry_absent` suppresses the entry-dependent legs; unusable tables report only `tables_sha` for the table-dependent legs; `rev=` echoes the argument as given; setup errors print nothing on stdout.
8. A symlinked pin directory is reported as every K/H quote plus `pin_hash` (the content is unreadable at that path), not as a single leg.

## Not verified
- `quality/check-r55-controls.py` / `r55_ctl_c1.py` were not run against this counter (the harness module is another seat's; its mutation procedure may differ from my reconstruction of the controls).
- Whether the lane's real entry (when integrated) uses `S` ids from the registry that satisfy `source_cell`: only the scribe draft was dry-run.
- Python 3.14.8 / git 2.56.0 only.

Tooling: none installed. Sealed hold-out: not looked for, not encountered. Scratch `/fast/scratch/hyaku/mado-r55/R55ExecC1CounterA` removed.
