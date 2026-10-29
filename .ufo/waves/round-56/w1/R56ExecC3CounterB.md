# R56ExecC3CounterB — C3 counter `c3-r56-used-by.py`

Deliverable: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ExecC3CounterB/c3-r56-used-by.py`
(python3 stdlib only, single file; written from registration §C3 + claims-frozen PRED-C3-r56 only; no other seat's counter read; no tool installed).

## What it does
- `python3 -I c3-r56-used-by.py --repo R --rev V --work D` (each exactly once; anything else = exit 2 `usage`). `--work` is created when missing and is HOME/TMPDIR of every git child (scrubbed env, `--no-replace-objects`, `GIT_CONFIG_GLOBAL=/dev/null`); the counter writes nothing else.
- Reads only git objects: `rev-parse --verify REV^{commit}` (then the full sha is used for every later read), `ls-tree -z` walked component by component (a symlink/submodule/blob where a directory is expected = absent), `cat-file blob`. Regular blobs only (100644/100755).
- Legs printed in order `missing,extra,dangling,tables_sha` (all failing ones listed). `tables_sha`: blob `.ufo/waves/round-56/frozen-tables.json` at REV hashes to the embedded `d50d2b7b…f9af`.
- Exit 0 only on TARGET_MET; 1 on a miss; 2 setup (reason on stderr, stdout empty): bad/unresolvable rev, `corpus/SOURCES.md` not a regular blob, a registry row with != 11 cells, usage errors.
- `--selftest --repo R --rev V --work D` (R:V only supplies the real frozen-tables blob, which it verifies against the constant): builds scratch git repos under `--work` (witness corpus generated in the script: 4 entries, 6 rows) and runs the counter as a child process; prints `<n>/<n> assertions passed`.

## Evidence (read-only runs)
```
$ python3 -I c3-r56-used-by.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 13f0acbe3a15da2d9c08357a576d91dcadc85273 --work $W
MADO_USED_BY: rev=13f0acbe3a15da2d9c08357a576d91dcadc85273 entries=70 rows=319 missing=65 extra=0 dangling=0 verdict=TARGET_MISSED missed=missing,tables_sha   (rc=1)
$ ... --rev 3423ae285676c2a10273000f4519163472b443db   (freeze commit; tables blob present)
MADO_USED_BY: rev=3423ae28... entries=70 rows=319 missing=65 extra=0 dangling=0 verdict=TARGET_MISSED missed=missing   (rc=1)
$ ... --selftest --repo <lane> --rev 3423ae28... --work $W
42/42 assertions passed   (rc=0)
$ ... --rev nonesuch      -> stderr "MADO_USED_BY setup error: rev 'nonesuch' does not resolve ...", stdout empty, rc=2
```
The required counts `entries=70 rows=319 missing=65 extra=0 dangling=0` reproduce at base. At base the verdict line carries `missed=missing,tables_sha` because the tables blob does not exist at base (it is committed in the freeze commit) — see ambiguity 1. The selftest also covers: each of the 6 harness controls' mutation shapes, list-all, fences (``` / ~~~ / 3-space / 4-space / mismatched closer), symlink entry, symlinked `corpus/knowledge`, symlinked SOURCES.md (exit 2), 3- and 12-cell rows (exit 2), usage errors, working-tree edits/untracked files ignored, token grammar, `source:` outside first 15 lines / indented, nested and non-.md files, 100755 entries, one stdout line, `--work` created and left empty, base-revision baseline (runs only when the base commit is readable in `--repo`; it was).
Not run: `quality/check-r56-controls.py --claim c3` (not part of this seat), a run against a post-fix tree (none exists).

## Ambiguities (most literal reading taken; the other reading listed)
1. `tables_sha` in the line. Registration prints `missed=<missing,extra,dangling|none>`; the seat brief says leg `tables_sha` with list-all. Taken: a failing/absent tables blob is a leg `tables_sha` appended to `missed` (verdict TARGET_MISSED, exit 1). Other reading: absent blob = setup error (exit 2), or the check fails silently outside `missed`. Consequence: at base the line differs from a bare `missed=missing` only by `,tables_sha`; on the final revision both agree (`none`).
2. Fence grammar. Registration: "``` / ~~~ fences with 0-3 leading spaces". Taken: opener = 0-3 spaces + run of >=3 of one char (any trailing text, even backticks); closer = same char, run >= opener, only whitespace after; unclosed fence runs to EOF. Other reading: plain toggle on any fence-looking line (differs only for mixed ``` / ~~~ nesting, shorter-run closers, or closers with text). All 70 base entries use plain ``` only, so both agree on the base corpus.
3. `SRC(entry)` tokens: taken as the CITE regex `(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])`. Other reading: any `S[0-9]{3,}` (registry id form). Under the taken reading `S1234` on a `source:` line is invisible to `dangling`. Likewise `source:` must start at column 0 and within lines 1-15 (split on `\n`), fences are not excluded for SRC.
4. Row cells: line stripped, ONE leading `|` and ONE trailing `|` (if present) removed, split on `|`; a row without a trailing pipe is still accepted if it has 11 cells; `\|` is not special (adds a cell -> setup error). Rows inside fenced blocks of SOURCES.md still count (regex only).
5. Duplicate row ids: USEDBY is the union over duplicate rows; `rows=` counts lines. Not specified; a duplicate row can therefore satisfy a leg. Set semantics for pairs: repeated cites / repeated used-by paths count once.
6. `USEDBY` regex is unanchored: `corpus/knowledge/x.md` embedded in prose, a URL or after `not ` counts as naming x.md; `x.md.bak` yields `x.md`. `_S004` and `S004_` count as cites (only alphanumerics block the lookbehind).
7. `ENTRIES` = direct-child names ending `.md` with mode 100644/100755 (names with spaces etc. can never be in USEDBY, so they could never be fixed). `corpus/knowledge` absent/symlinked = zero entries (not a setup error).
8. `rev=` prints the argument as given (a symbolic rev prints the symbol), reads use the resolved sha.

## What a forger could add to flip a leg without a real citation
- `missing`/`extra` (cite side): any unfenced `S###` anywhere in the entry — HTML comment, inline code, URL fragment, `_S004`, a line in front matter — plus the entry path anywhere in the row's cell 11 (even `not corpus/knowledge/x.md`, or a path in a URL). The counter checks lexical co-occurrence, not that the entry cites the row for its claim.
- Hide a pair: wrap the real citation in a fence (and drop the used-by) -> no `missing`, no `extra`; make the entry a symlink or non-`.md`; indent a registry row by 4 spaces (it stops being a row, citations of its id are then non-row tokens) or put a 12th cell... (that one is exit 2); add a duplicate row of the same id whose used-by names the entry.
- `dangling`: put the bad id as `S1234`, on line 16+, indent `source:`, write `Source:`, or leave it off `source:`; or make the id a real registry row.
- Row-grammar side effects: `used-by` is the only cell read, so editing any other cell changes nothing for this counter.
- `tables_sha` is a pure blob-hash check; flipping it needs the true tables bytes (the counter does not otherwise read the tables).
