# R56ExecC1CounterB — PRED-C1-r56 counter, independent implementation

Deliverable: `.ufo/waves/round-56/w1/R56ExecC1CounterB/c1-r56-autoreload-entry.py`
(sha256 `fa83bf437b3e18e806608e38e099c963ed8bc96d9183668ef4b8e825f27e58fd`; 1 file, stdlib only, ~800 lines).
Receipts beside it: `selftest.txt`, `run-2aa347b1.txt`.

## What I did
Wrote the counter from registration.md §C1 and claims-frozen.md PRED-C1-r56 only. I did not open any other seat's counter.
- Git access: `Repo` class runs `git rev-parse|ls-tree -z|cat-file` through subprocess at the commit's tree. It never reads the working tree. The git child env is built from scratch (HOME/TMPDIR = `--work`, `GIT_NO_REPLACE_OBJECTS=1`, no inherited `GIT_*`).
- Regular-blob rule: it walks `ls-tree` component by component. Only mode 100644/100755 blobs count. A symlink blob, or a path crossing a non-tree directory entry, is absent.
- Parsing strategy (no line regex decides a row):
  - a character-level block scanner (`live_lines`) for fences and HTML comments;
  - a first-cell tokenizer plus a strict ` | ` cell splitter for rows;
  - a hand-written scanner for the registry id and for the `N`/`N-M` locator list in the anchor cell;
  - small regexes only for the identifier, digit-run, S-id and URL token definitions that registration.md itself states as regexes.
- Output: exactly one frozen line. Exit codes: 0 only on TARGET_MET, 1 on a miss, 2 on a setup error (reason on stderr, stdout empty).
- Setup errors: unknown, repeated or valueless option, missing `--repo`/`--rev`/`--work`, empty or `-`-leading rev, a non-repo, an unresolvable rev.
- `--work` is created when missing. The counter writes nothing else.
- `TABLES_SHA256` is embedded (`d50d2b7b…f9af`). Leg `tables_sha` compares it with the blob at `--rev`.
- Every failing leg is listed (list-all), in a fixed order: `entry_absent, tables_sha, prov, index, row:*, quote:*, pin_hash, host:*, source_cell:*, scope:*, tok:*, num:*, new_rows, content`.
- `--selftest [--repo R] [--rev REV] [--work W]`:
  - Source: `R`/`REV` default to `.`/`HEAD`. They supply the frozen tables and the 12 pin blobs, read via git.
  - Fixture: a scratch git repo built from those tables, a SOURCES.md and README, and a witness entry the counter generates itself. I did not use anybody else's witness.
  - Checks: the good tree, the 10 registered controls, 20+ extra legs and grammar cases, setup errors, and scanner unit checks.
  - Run in this seat: `227/227 assertions passed`, rc 0 (`selftest.txt`).
  - Run by hand at base `13f0acbe`: `missed=tables_sha,entry_absent,index`, rc 1.
  - Run on a scratch repo at lane tip `2aa347b1` (no entry yet): `rows=0/30 hosts=0/3 sources=0/30 scope=0/30 content=0/33 new_rows=0/8 verdict=TARGET_MISSED missed=entry_absent,index,new_rows`, rc 1.
  - Setup error: `--rev nope` printed `setup error: rev does not resolve to a commit: nope` on stderr, rc 2.
  - Good witness tree (in-process): `MADO_AUTORELOAD_ENTRY: rev=<commit> rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none`, rc 0.

Not run: the real lane entry (it does not exist yet), `quality/check-r56-controls.py` (not mine), and any comparison against another counter.

## Findings and ambiguities (the first two are the ones to act on)
1. **Control 8 vs the literal `quote:<id>` leg (disagreement inside registration.md).**
   - `quote:<id>` is defined as "the frozen quote is a substring of line `<line>` of the pin blob". It does not depend on the entry. Under that text, control 8 (one character changed in the K05 quote cell) fails only `row:K05`, because the row grammar demands the frozen quote. Control 8 requires `quote:K05`.
   - What I did: `quote:<id>` holds only if the frozen quote is on the pin line AND, when the row exists, the quote the row carries (backtick-wrapped) is on that pin line too.
   - Effect: verdicts and the counts a/b are unchanged. Only the `missed` list differs. With the literal reading, control 8 would print `missed=row:K05` and the harness would score it not admitted, so controls would be 9/10. An implementation that follows the literal text will disagree with this one on exactly that list. The L1 should pick one.
2. **Control 2 is only partly caught by `tok:`.** The placeholder text `…not a claim about any source line` contains the identifier `source`. The K23 quote is `"source= skipping directory {}", value);`, so K23 passes `tok`. Result: `content=1/33` (K23), and `tok:` is listed for every other row. Still `e<33` and `TARGET_MISSED`. It is an example of the declared lexical-grounding limit.
3. **`content` as a leg name.** The legs table has no `content` leg, but control 2 says "`tok:` and `content` shortfall". I emit `content` in `missed` exactly when `e<33`, in addition to the `tok:`/`num:` legs. Control 3 therefore also lists `content`. Alternative reading: no aggregate leg, `tok:` only. I could not tell which one the harness checks.
4. **Entry absent.** "All entry-dependent legs are not evaluated" is read as: `prov`, `row`, `host`, `source_cell`, `scope`, `tok`, `num` and `content` are not listed. Counts rows/hosts/sources/scope/content print 0. Still evaluated: `tables_sha`, `index`, `quote:*`, `pin_hash`, `new_rows`. Alternative: `quote:*` also skipped.
5. **Unusable tables** (blob absent or not parseable JSON) has no registered behaviour. I list `tables_sha` plus the independent legs (`entry_absent`, `prov`, `index`) and print zero counts. When the tables parse but the sha is wrong, every table-driven leg is still evaluated against that blob.
6. **Row detection.** A candidate row is a live line (outside fences and comments) whose first cell, after optional leading blanks and a `|`, equals a known id. The strict grammar then rejects leading blanks, trailing bytes, cell counts other than 5, a pipe inside a cell, and cells with edge whitespace. A `K01..K30`/`H01..H03` line with an anchor-less shape is therefore `row:<id>` rather than invisible. An id appearing on two live lines fails `row` for that id.
7. **Duplicate proposition.** Both rows fail `row`, not only the later one. The duplicate test covers every candidate row line, K and H.
8. **Fences and comments.**
   - A fence is 0-3 spaces plus at least three backticks or tildes. A backtick-fence opener whose info string contains a backtick is not a fence.
   - A closer is the same character, at least as long, with only blanks after it. An unclosed fence runs to EOF. Fence markers inside an HTML comment are inert.
   - A row line counts as inside a comment when its first `|` is inside one. A comment starting later in the line leaves a trailing byte, so the row fails the grammar.
9. **`prov`.**
   - "one `verified-at: 2026-10-28`" is read as exactly one line (right-trimmed) equal to that text in lines 1-30.
   - "in that order" is read as: exists a `source:` line before the verified line, and a `recheck:` line after it. A `source:` line after it does not help.
   - `S###` tokens use the C3 regex `(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])`. The source set must contain every S-id in a K row's src cell, taken from the best-effort cell parse even if the row is malformed.
10. **`index`.** Exactly one line of README starting `` | `knowledge/hyprland-config-autoreload-r56.md` ``. Fences are not excluded.
11. **`source_cell`.**
    - The S-id must have exactly one registry line (the id regex applied to all of SOURCES.md) and that line must have 11 cells. Alternative: "one among the 11-cell rows".
    - URL = last `https?://\S+` match in the source cell (cell 2). Alternative: whitespace tokens starting with the scheme. `used-by names the entry path` = plain substring of cell 11.
    - `rev_rule` keys are matched with fnmatch (`Hyprland-*`) or as a literal pin name.
    - New rows S383-S390 use the same test with the pin from `c1.rows`. The "equals frozen sid" clause applies only to K rows.
12. **`scope`.**
    - Any `<basename>:` occurrence counts, matched as a substring. So `Hyprland-ConfigWatcher.cpp:` matches basename `ConfigWatcher.cpp`.
    - The locator list starts right after the colon (no blanks). After a comma, spaces are skipped. The list ends at the first non-locator, so `271-279 input kb options, X.cpp:296` ends at `input`.
    - A reversed range `10-5` is empty. The cited (not the frozen) S-id's row is used. A missing or duplicate row fails `scope`.
13. **`tok`/`num`.**
    - Both use the frozen quote, not the row's carried quote. They are evaluated on the best-effort row cells even when `row:` fails.
    - "A digit run of the quote" = any maximal `[0-9]+` in the quote (looser than the boundary regex used on the proposition), compared as strings. Line numbers and `0..3` compare as integers. Runs of 19 or more digits compare as strings only.
14. **`pin_hash`.** The union of `pin_sha256` (8) and `host_pin_sha256` (4) is checked: 12 pins, including `host-watched-lstat.txt`. Alternative: only the 8 in `pin_sha256`.
15. **Denominators.** `/30 /3 /30 /30 /33 /8` are printed as fixed text. `new_rows` also requires `len(new_row_ids)==8`.
16. **Rev echo.** `rev=` in the output is the string passed to `--rev` (not the resolved hash).

## Not verified
- No run against the real entry, because it is not yet committed. All TARGET_MET evidence is on my own generated witness tree.
- No check that propositions are entailed by quotes (declared limit).
- `python3 -I` was used for every run recorded here. Python 3.14.8, git 2.56.0.
- Tooling installed: none.
- Scratch `/fast/scratch/hyaku/mado-r56/R56ExecC1CounterB/` was removed. No lane tracked file, index or ref was touched. I did not look for the sealed hold-out and found none.
