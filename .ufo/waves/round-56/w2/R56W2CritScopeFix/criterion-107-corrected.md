## Criterion 107 (corrected draft, R56W2CritScopeFix; M56-1; text only, not executed as a checker)

**107.** **A registry row cited by a knowledge entry's evidence row has a unique anchor that names the row's upstream file, covers the quoted line, and stays within that file's length (extends 77 and 97).**

Scope. Every evidence row of a knowledge entry, any row class: a table row, outside fenced code and HTML comments, whose third cell is a registry id `S` followed by three or more digits. A row of that shape whose fourth cell is not exactly `<file>:<N>` (one decimal number; no range, no list, no second file) is a violation `reason=malformed-pin`. It is never skipped.

For each such row, let R be the registry row whose first cell is that id in `corpus/SOURCES.md` at the checked revision:

1. Uniqueness. R must be the only row with that id. Zero rows reads `reason=no-registry-row`; two or more read `reason=dup-id`, whatever their content.
2. NAME. The last path component of the last `http(s)://` token in R's source cell (cell 2), with trailing `).,;` removed. If NAME contains `#` or `?`, the row reads `reason=no-name` and must be read by hand.
3. Bounded occurrence. An occurrence of `NAME:` in R's anchor cell (cell 6) counts only when the character before it is absent or is not in `[A-Za-z0-9_]`. A hyphen or a slash before it is allowed; `OldConfigWatcher.cpp:` does not contain an occurrence of `ConfigWatcher.cpp:`.
4. Locator list. Right after `NAME:` comes a comma-separated list of locators. Each locator is `N` or `N-M`, decimal, with N at least 1. One optional space may follow a comma. The list continues only while the next item starts with a digit. A locator with M less than N denotes no line and covers nothing.
5. Cover. Some locator of some counted occurrence has N <= L <= M, where L is the quoted line. A single `N` means N = L.
6. Length. If the anchor cell names its pin as `pin <path>`, the blob at that path at the checked revision is read, and every locator of the counted occurrence must have max(N, M) <= the blob's line count (the number of `\n`-separated pieces). A locator past the end of the file reads `reason=past-eof` for every row of that pin. An anchor with no named pin reads `eof=unchecked` in the output.

Output: one line per evidence row, `ANCHOR_COVER: row=<id> sid=<S###> line=<N> name=<NAME> locators=<list|none> eof=checked|unchecked verdict=OK|MISS [reason=...]`, then `CHECK107: rows=<n> covered=<k> miss=<m> verdict=OK|FAIL`. The requirement is `miss=0` with `rows>0`. Exit 0 on OK, 1 on FAIL, 2 on setup error with empty stdout. The check reads git objects at `<rev>` only and writes only under `--work`.

Shown able to fail, on the committed round-55 entry `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` at `63f48dc1`: rows=32 covered=25 miss=7 (K14, K17, E04, E05, E08, E11, E14; `receipts/anchor-cover-r55-63f48dc1.out`). Each registry mutant named in `R56W2CritScopeFix/receipts/` (widen past EOF, narrow below a K row, drop the name, reversed range, identifier-prefixed name, malformed pin cell, duplicate id) fails under this text on the row or rows it names; the EOF, boundary, reversed-range, malformed-pin and duplicate-id clauses are the ones the round-56 draft lacked.

Fix path (registry rows are append-only, CORPUS rule 2): a supersession row with a new id and a widened anchor, then a re-cite in the entry. Each change is logged in the round lesson.

Declared limits.
- The check reads the anchor text, not the upstream file's statement at the line. An anchor that names the right file, with a range whose lines carry another statement, passes; the sentence-to-pin audit of criterion 104 carries that.
- Identity is by basename. `legacy/ConfigManager.cpp` and `ConfigManager.cpp` are the same name to this check; an anchor that names the basename of a different directory's file passes. The directory is not checked.
- A source URL whose last component is not the file the anchor names (a rename) reads MISS and must be read before it is treated as a violation.
- Without a named `pin <path>` the length bound is unchecked for that row (`eof=unchecked`), and the row is listed in the round report, not passed silently.
- An entry with no evidence rows reads `rows=0 verdict=FAIL`, so an empty entry is not vacuously green.
