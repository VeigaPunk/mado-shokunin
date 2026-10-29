# R56W2MutC1CounterB — mutation test of `quality/counters/c1-r56-autoreload-entry.py`

Pinned revision: `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` (counter sha256 `2b2ef41b3329edde`). Oracle, unchanged: the counter's own `--selftest`, and `python3 -I quality/check-r56-controls.py --claim c1 --repo <lane> --rev <rev> --work <w> --counter <mutant>`. A mutant is **KILLED** when either oracle fails on it; **SURVIVED** when both pass; **EQUIVALENT** when it survives and no input (argued or fuzzed) changes the counter's output.

Mutants are one-line edits of COPIES in scratch (`/fast/scratch/hyaku/mado-r56/R56W2MutC1CounterB/mutants/`); the lane is read-only (git objects only). Selftest on the unmutated counter: `242/242 assertions passed`, rc 0. Harness on the unmutated counter: `MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK`, rc 0 (receipts/baseline-*.txt).

## Summary

| measure | count |
|---|---|
| mutants generated | 71 |
| KILLED by the existing oracle (selftest and/or harness) | 35 (49.3% of 71; 55.6% of the 63 non-equivalent) |
| SURVIVED the existing oracle | 36 |
| of which EQUIVALENT (argued; fuzz or output check where possible) | 8 |
| of which NON-EQUIVALENT (each has a verified kill fixture) | 28 |
| proposed kill fixtures run against the mutant (F-ids, receipts/fixtures-results.json) | 28 / 28 killed |
| non-equivalent mutants killed with the existing oracle plus the proposed fixtures | 63 / 63 (100%) |

Kill rate of the existing oracle: 35/71 = 49.3% of all mutants, 35/63 = 55.6% of the non-equivalent ones. The round-55 survivor counts quoted in the wave brief (11/24, 8/38, 4/17) were not re-measured here.

Selftest vs harness: the 35 KILLED mutants are killed by the selftest (21 of them also by the harness, 14 by the selftest alone). The harness alone kills none of them.

Scope note: the mutations are helpers (`split_lines`, `fence_*`, `live_lines`, `first_cell`, `strict_row`, `lenient_row`, `registry_cells`, `registry_id`, `scope_covers`, `to_int`, the four regexes, `Repo.*`), plus the thresholds `ECHO_MIN`, `K_MIN`, `H_MIN`, `NEW_ROWS_DENOM`, `REGULAR_MODES`. Disclosure: `ECHO_MIN`, `K_MIN` and `NEW_ROWS_DENOM` are read inside `evaluate()` (M57-M61 touch those legs); the others are helper-level.

## Survivors

### Equivalent (8)

- **M14** (`live_lines`): ``                i += 3`` → ``                i += 2``. live_lines comment-close skip `i += 2`: after `-->` the baseline resumes at i+3, the mutant at i+2, where the character is `>`. Outside a comment the scanner reacts only to `<!--` (starts with `<`) and `|`, so both resume in the same state. Fuzz: 200000 random multi-line inputs, 0 disagreements (receipts/fuzz-equiv.txt).
- **M26** (`strict_row`): ``    if not (line.startswith("| ") and line.endswith(" |")) or len(line) < 4:`` → ``    if not (line.startswith("| ") and line.endswith(" |")) or len(line) < 2:``. strict_row `len(line) < 2`: differs from the baseline only on the 3-character line `| |` (strict_row returns [''] instead of None). The three call sites (evaluate's cell loop, prop_count, row_data) receive only candidate lines, whose first cell is a K/H id (length >= 7), so `| |` never reaches them. Output-level check: inserting `| |` and `|  |` lines into the entry and the registry gives byte-identical counter output (E26 in mutants.md).
- **M44** (`scope_covers`): ``        pos = anchor.find(key, pos + 1)`` → ``        pos = anchor.find(key, pos + len(key))``. scope_covers occurrence step `pos + len(key)`: key = basename + ':' and ':' occurs only as its last character, so no occurrence can begin inside another; the occurrence positions are identical. Fuzz: 200000 random anchors, 0 disagreements.
- **M57** (`constants`): ``ECHO_MIN = 30`` → ``ECHO_MIN = 29``. ECHO_MIN 29: the echo leg tests len(quote) >= ECHO_MIN with quote from the frozen table; no frozen quote has length 29 (receipts/frozen-quote-lengths.json lists 28, 30, 32, 34, ...; 29 is absent). Equivalent under the tables_sha-pinned table; a tampered table fails tables_sha in both versions.
- **M63** (`Repo.regular_oid`): ``        if any(c in ("", ".", "..") for c in comps):`` → ``        if any(c in ("", ".") for c in comps):``. regular_oid drops '..' from the rejected components: every path the counter reads is a constant or PIN_DIR + a pin name from the frozen table, and none of those contains a '.' or '..' component (checked: no such pin name). Unreachable.
- **M64** (`Repo.regular_oid`): ``                if mode != "040000" or typ != "tree":`` → ``                if typ != "tree":``. tree test drops `mode != "040000"`: in git's ls-tree a `tree` entry always has mode 040000 (gitlink entries are typ `commit`). Git object-format invariant.
- **M66** (`Repo.blob`): ``        if oid not in self.blobs:`` → ``        if True:``. blob cache forced off (`if True:`): the cache memoises `cat-file blob` by oid; outputs are identical, only cost differs.
- **M70** (`Repo.listing`): ``                mode, typ, oid = meta.decode().split(" ")`` → ``                mode, typ, oid = meta.decode().split(" ", 2)``. ls-tree meta split `split(" ", 2)`: the meta is exactly `<mode> <type> <oid>` (two spaces), so maxsplit 2 is a no-op.

### Non-equivalent, killed by a verified proposed fixture (28)

Each fixture is ONE edit of the pinned tree (`fixtures.py`); both the baseline and the mutant counter run on it with `--rev HEAD`. KILLED = the mutant's (rc, stdout) differs from the baseline's. The baseline's own output is shown: it is the registered behaviour.

| mutant | mutated line (old → new) | proposed fixture (F) | baseline (rc, output) | mutant (rc, output) | note |
|---|---|---|---|---|---|
| M02 (split_lines) | ``return data.decode("utf-8", "replace").split("\n")`` → ``return data.decode("utf-8", "ignore").split("\n")`` | F02: invalid UTF-8 byte between locator 33 and -34 in the S383 anchor | rc 1, rows=30/30 hosts=3/3 sources=30/30 scope=21/30 content=33/33 new_rows=8/8 verdict=TARGET_MISSED missed=scope:K04,scope:K05,scope:K06,scope:K07,scope:K08,scope:K09,scope:K10,scope:K11,scope:K12 | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | decode error policy `ignore`; invalid UTF-8 cannot occur in the real entry or registry (both decode as UTF-8, checked) |
| M03 (split_lines) | ``return data.decode("utf-8", "replace").split("\n")`` → ``return data.decode("utf-8", "replace").splitlines()`` | F03: CRLF line endings in the entry | rc 1, rows=0/30 hosts=0/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K01,row:K02,row:K03,row:K04,row:K05,row:K06,row:K07,row:K08,row:K09,row:K10,row:K11,row:K12,row:K13,row:K14,row:K15,row:K16,... | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | `splitlines()` accepts CR-terminated lines; the registered grammar says no trailing byte |
| M04 (fence_open) | ```     if n > 3 or n >= len(line) or line[n] not in "`~": ``` → ```     if n > 4 or n >= len(line) or line[n] not in "`~": ``` | F04: 4-space ``` line around K05 (not a fence in CommonMark) | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | rc 1, rows=4/30 hosts=0/3 sources=4/30 scope=4/30 content=4/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K05,row:K06,row:K07,row:K08,row:K09,row:K10,row:K11,row:K12,row:K13,row:K14,row:K15,row:K16,row:K17,row:K18,row:K19,row:K20,row... | 4-space ``` accepted as a fence opener (CommonMark: indented code, not a fence) |
| M06 (fence_open) | ```     if ch == "`" and "`" in line[m:]: ``` → ```     if ch == "~" and "`" in line[m:]: ``` | F06: ``` `x` opener around K05 (backtick in info string) | rc 1, rows=5/30 hosts=0/3 sources=5/30 scope=5/30 content=5/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K06,row:K07,row:K08,row:K09,row:K10,row:K11,row:K12,row:K13,row:K14,row:K15,row:K16,row:K17,row:K18,row:K19,row:K20,row:K21,row... | rc 1, rows=29/30 hosts=3/3 sources=29/30 scope=29/30 content=32/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K05,source_cell:K05,scope:K05,tok:K05,num:K05,echo:K05 | backtick fence with a backtick in the info string not rejected for ``` (tilde/backtick swapped) |
| M08 (fence_close) | ``    if n > 3:`` → ``    if n > 4:`` | F08: ``` opener around K05, 4-space closer after it | rc 1, rows=4/30 hosts=0/3 sources=4/30 scope=4/30 content=4/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K05,row:K06,row:K07,row:K08,row:K09,row:K10,row:K11,row:K12,row:K13,row:K14,row:K15,row:K16,row:K17,row:K18,row:K19,row:K20,row... | rc 1, rows=29/30 hosts=3/3 sources=29/30 scope=29/30 content=32/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K05,source_cell:K05,scope:K05,tok:K05,num:K05,echo:K05 | closer indented 4 spaces accepted |
| M10 (fence_close) | ``    return m - n >= length and line[m:].strip(" \t") == ""`` → ``    return m - n >= length and line[m:].strip() == ""`` | F10: ``` opener around K05, closer with trailing VT | rc 1, rows=4/30 hosts=0/3 sources=4/30 scope=4/30 content=4/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K05,row:K06,row:K07,row:K08,row:K09,row:K10,row:K11,row:K12,row:K13,row:K14,row:K15,row:K16,row:K17,row:K18,row:K19,row:K20,row... | rc 1, rows=29/30 hosts=3/3 sources=29/30 scope=29/30 content=32/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K05,source_cell:K05,scope:K05,tok:K05,num:K05,echo:K05 | closer tail: `strip()` accepts a trailing vertical tab/form feed |
| M11 (live_lines) | ``            if line.startswith("<!--", i):`` → ``            if line.startswith("<!", i):`` | F11: <!DOCTYPE html> line before K05 (no close) | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | rc 1, rows=4/30 hosts=0/3 sources=4/30 scope=4/30 content=4/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K05,row:K06,row:K07,row:K08,row:K09,row:K10,row:K11,row:K12,row:K13,row:K14,row:K15,row:K16,row:K17,row:K18,row:K19,row:K20,row... | `<!` (not `<!--`) opens an HTML comment; `<!DOCTYPE` hides every later row |
| M13 (live_lines) | ``                    i += 4`` → ``                    i += 1`` | F13: <!--> opener before K05, --> after it | rc 1, rows=29/30 hosts=3/3 sources=29/30 scope=29/30 content=32/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K05,source_cell:K05,scope:K05,tok:K05,num:K05,echo:K05 | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | `<!-->` opener: baseline opens a comment; the mutant closes it at once [INFERENCE, not verified against a renderer: CommonMark HTML-block type 2 ends at a line containing `-->`, which would include the opener line] |
| M19 (first_cell) | ``    while i < len(line) and line[i] in " \t":`` → ``    while i < len(line) and line[i] == " ":`` | F19: leading tab on the K05 row | rc 1, rows=29/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K05 | rc 1, rows=29/30 hosts=3/3 sources=29/30 scope=29/30 content=32/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K05,source_cell:K05,scope:K05,tok:K05,num:K05,echo:K05 | leading tab on a row: baseline finds the candidate (best-effort cells survive); mutant drops the candidate |
| M25 (strict_row) | ``    if not (line.startswith("\| ") and line.endswith(" \|")) or len(line) < 4:`` → ``    if not (line.startswith("\| ") and line.endswith("\|")) or len(line) < 4:`` | F25: K05 row ends '`|' (no space before final pipe) | rc 1, rows=29/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K05 | rc 1, rows=29/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K05,quote:K05 | row ends ``\|` (no space before the final pipe): strict parse of the mutant takes a 5-cell split that loses a backtick |
| M29 (lenient_row) | ``    s = line.strip()`` → ``    s = line`` | F29: trailing space after the K05 row | rc 1, rows=29/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K05 | rc 1, rows=29/30 hosts=3/3 sources=29/30 scope=29/30 content=32/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K05,source_cell:K05,scope:K05,tok:K05,num:K05,echo:K05 | trailing space on a row: lenient parse without strip yields 7 cells |
| M33 (registry_cells) | ``    return lenient_row(line)`` → ``    return strict_row(line) or lenient_row(line)`` | F33: double space before the S383 status separator | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | rc 1, rows=30/30 hosts=3/3 sources=20/30 scope=30/30 content=33/33 new_rows=7/8 verdict=TARGET_MISSED missed=source_cell:K03,source_cell:K04,source_cell:K05,source_cell:K06,source_cell:K07,source_cell:K08,source_cell:K09,source_cell:K10... | registry double space before the status separator: strict split keeps the trailing space in the status cell |
| M37 (registry_id) | ``    while j < len(line) and line[j].isspace():`` → ``    while j < len(line) and line[j] == " ":`` | F37: tab after the S383 opening pipe | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | rc 1, rows=30/30 hosts=3/3 sources=20/30 scope=20/30 content=33/33 new_rows=7/8 verdict=TARGET_MISSED missed=prov,source_cell:K03,source_cell:K04,source_cell:K05,source_cell:K06,source_cell:K07,source_cell:K08,source_cell:K09,source_cel... | registry id with a tab after the pipe: baseline `isspace()`, mutant `' '` only |
| M42 (scope_covers) | ``                if m > k + 1:`` → ``                if m > k:`` | F42: S383 anchor '33-,' dangling hyphen | rc 1, rows=30/30 hosts=3/3 sources=30/30 scope=21/30 content=33/33 new_rows=8/8 verdict=TARGET_MISSED missed=scope:K04,scope:K05,scope:K06,scope:K07,scope:K08,scope:K09,scope:K10,scope:K11,scope:K12 | rc 1, no stdout: ValueError: invalid literal for int() with base 10: '' | `basename:33-,`: baseline stops the locator list; mutant raises ValueError (no output) |
| M45 (scope_covers) | ``    return covered and not over`` → ``    return covered`` | F45: S383 anchor with a covering range AND 9999 | rc 1, rows=30/30 hosts=3/3 sources=30/30 scope=20/30 content=33/33 new_rows=8/8 verdict=TARGET_MISSED missed=scope:K03,scope:K04,scope:K05,scope:K06,scope:K07,scope:K08,scope:K09,scope:K10,scope:K11,scope:K12 | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | E3 past-EOF verdict dropped: a covering range AND a past-EOF locator in one anchor (harness control 12 has only the lone past-EOF range, which the counter never counts as covering) |
| M46 (scope_covers) | ``            if lo is None or hi is None or (nlines is not None and (hi > nlines or lo > nlines)):`` → ``            if lo is None or hi is None or (nlines is not None and hi > nlines):`` | F46: S383 anchor with reversed range 5000-5 beside 33-34 | rc 1, rows=30/30 hosts=3/3 sources=30/30 scope=20/30 content=33/33 new_rows=8/8 verdict=TARGET_MISSED missed=scope:K03,scope:K04,scope:K05,scope:K06,scope:K07,scope:K08,scope:K09,scope:K10,scope:K11,scope:K12 | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | E3 lower bound dropped: reversed range 5000-5 (lo past EOF) beside a covering locator |
| M48 (scope_covers) | ``            while j < len(anchor) and anchor[j] in "0123456789":`` → ``            while j < len(anchor) and anchor[j].isdigit():`` | F48: S383 anchor '105²' (superscript digit) | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | rc 1, no stdout: ValueError: invalid literal for int() with base 10: '105²' | `isdigit()` accepts superscript two; int() raises (no output) |
| M49 (scope_covers) | ``                while m < len(anchor) and anchor[m] in "0123456789":`` → ``                while m < len(anchor) and anchor[m].isdigit():`` | F49: S383 anchor '34²' range end | rc 1, rows=30/30 hosts=3/3 sources=30/30 scope=22/30 content=33/33 new_rows=8/8 verdict=TARGET_MISSED missed=scope:K05,scope:K06,scope:K07,scope:K08,scope:K09,scope:K10,scope:K11,scope:K12 | rc 1, no stdout: ValueError: invalid literal for int() with base 10: '34²' | `isdigit()` on the range end; int() raises (no output) |
| M50 (scope_covers) | ``            lo = int(anchor[i:j]) if j - i < 19 else None`` → ``            lo = int(anchor[i:j]) if j - i < 18 else None`` | F50: pin absent; 18-digit locator beside 33 in S383 anchor | rc 1, rows=20/30 hosts=3/3 sources=30/30 scope=21/30 content=33/33 new_rows=8/8 verdict=TARGET_MISSED missed=quote:K03,quote:K04,quote:K05,quote:K06,quote:K07,quote:K08,quote:K09,quote:K10,quote:K11,quote:K12,pin_hash,scope:K04,scope:K0... | rc 1, rows=20/30 hosts=3/3 sources=30/30 scope=20/30 content=33/33 new_rows=8/8 verdict=TARGET_MISSED missed=quote:K03,quote:K04,quote:K05,quote:K06,quote:K07,quote:K08,quote:K09,quote:K10,quote:K11,quote:K12,pin_hash,scope:K03,scope:K0... | 18-digit locator: mutant treats it as past EOF; baseline differs only when the pin blob is absent (nlines None) |
| M51 (to_int) | ``    return int(run) if len(run) < 19 else None`` → ``    return int(run) if len(run) < 18 else None`` | F51: K04 proposition gains a zero-padded 18-digit '3' | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | rc 1, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=32/33 new_rows=8/8 verdict=TARGET_MISSED missed=num:K04 | 18-digit zero-padded run `000000000000000003`: baseline counts it as 3 (accepted), the 19-digit form is rejected (inconsistent boundary) |
| M54 (RUN_RE) | ``RUN_RE = re.compile(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])")`` → ``RUN_RE = re.compile(r"(?<![A-Za-z0-9])[0-9]+(?![0-9])")`` | F54: K04 proposition gains 'config7' | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | rc 1, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=32/33 new_rows=8/8 verdict=TARGET_MISSED missed=num:K04 | digit run followed by a letter (`12x`): baseline ignores it (lookahead), mutant counts it |
| M55 (SID_RE) | ``SID_RE = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")`` → ``SID_RE = re.compile(r"S[0-9]{3}")`` | F55: source line gains S3999 (not a registry row) | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | rc 1, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MISSED missed=prov | `S3999` (4 digits): baseline's `S[0-9]{3}(?![0-9])` does not see it, so the dangling check is silent; mutant reads `S399` |
| M56 (URL_RE) | ``URL_RE = re.compile(r"https?://\S+")`` → ``URL_RE = re.compile(r"https?://.*")`` | F56: S383 source cell has text after its URL | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | rc 1, rows=30/30 hosts=3/3 sources=20/30 scope=30/30 content=33/33 new_rows=7/8 verdict=TARGET_MISSED missed=source_cell:K03,source_cell:K04,source_cell:K05,source_cell:K06,source_cell:K07,source_cell:K08,source_cell:K09,source_cell:K10... | URL token `https?://.*` swallows text after the URL inside the registry cell |
| M58 (constants) | ``ECHO_MIN = 30`` → ``ECHO_MIN = 31`` | F58: K07 proposition = its 30-char quote + echo text | rc 1, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=32/33 new_rows=8/8 verdict=TARGET_MISSED missed=echo:K07 | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | ECHO_MIN 31: a 30-character quote (K07) is not echo-checked; harness control 11 needs only ANY echo leg |
| M59 (constants) | ``K_MIN, H_MIN = 40, 20`` → ``K_MIN, H_MIN = 39, 19`` | F59: K05 proposition of exactly 39 characters | rc 1, rows=29/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K05 | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | K_MIN 39: a 39-character proposition accepted (baseline requires >= 40) |
| M60 (constants) | ``K_MIN, H_MIN = 40, 20`` → ``K_MIN, H_MIN = 41, 21`` | F60: K05 proposition of exactly 40 characters | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | rc 1, rows=29/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MISSED missed=row:K05 | K_MIN 41: a 40-character proposition rejected (baseline accepts >= 40) |
| M62 (constants) | ``REGULAR_MODES = ("100644", "100755")`` → ``REGULAR_MODES = ("100644",)`` | F62: entry file mode 100755 | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | rc 1, rows=0/30 hosts=0/3 sources=0/30 scope=0/30 content=0/33 new_rows=8/8 verdict=TARGET_MISSED missed=entry_absent | executable blob mode 100755 rejected by the mutant; baseline accepts regular blobs of either mode |
| M69 (Repo.resolve) | ``        p = self.git("rev-parse", "--verify", "-q", rev + "^{commit}", check=False)`` → ``        p = self.git("rev-parse", "--verify", "-q", rev + "^{tree}", check=False)`` | F69: --rev <tree oid> (not a commit) | rc 2, (no stdout) | rc 0, rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none | `--rev <tree oid>`: baseline setup error (rev must be a commit); mutant peels to the tree and reports TARGET_MET |

Not-killed fixtures: 0. Every proposed fixture kills its mutant (receipts/fixtures-results.json, verdict KILLED).

## Full table (71)

| id | helper | oracle verdict | killed by | classification |
|---|---|---|---|---|
| M01 | split_lines | KILLED | selftest+harness | KILLED (existing oracle) |
| M02 | split_lines | SURVIVED | - | SURVIVED -> KILLED by F02 |
| M03 | split_lines | SURVIVED | - | SURVIVED -> KILLED by F03 |
| M04 | fence_open | SURVIVED | - | SURVIVED -> KILLED by F04 |
| M05 | fence_open | KILLED | selftest | KILLED (existing oracle) |
| M06 | fence_open | SURVIVED | - | SURVIVED -> KILLED by F06 |
| M07 | fence_open | KILLED | selftest | KILLED (existing oracle) |
| M08 | fence_close | SURVIVED | - | SURVIVED -> KILLED by F08 |
| M09 | fence_close | KILLED | selftest | KILLED (existing oracle) |
| M10 | fence_close | SURVIVED | - | SURVIVED -> KILLED by F10 |
| M11 | live_lines | SURVIVED | - | SURVIVED -> KILLED by F11 |
| M12 | live_lines | KILLED | selftest | KILLED (existing oracle) |
| M13 | live_lines | SURVIVED | - | SURVIVED -> KILLED by F13 |
| M14 | live_lines | SURVIVED | - | EQUIVALENT |
| M15 | live_lines | KILLED | selftest | KILLED (existing oracle) |
| M16 | live_lines | KILLED | selftest | KILLED (existing oracle) |
| M17 | live_lines | KILLED | selftest | KILLED (existing oracle) |
| M18 | live_lines | KILLED | selftest | KILLED (existing oracle) |
| M19 | first_cell | SURVIVED | - | SURVIVED -> KILLED by F19 |
| M20 | first_cell | KILLED | selftest+harness | KILLED (existing oracle) |
| M21 | first_cell | KILLED | selftest+harness | KILLED (existing oracle) |
| M22 | first_cell | KILLED | selftest+harness | KILLED (existing oracle) |
| M23 | first_cell | KILLED | selftest | KILLED (existing oracle) |
| M24 | strict_row | KILLED | selftest | KILLED (existing oracle) |
| M25 | strict_row | SURVIVED | - | SURVIVED -> KILLED by F25 |
| M26 | strict_row | SURVIVED | - | EQUIVALENT |
| M27 | strict_row | KILLED | selftest+harness | KILLED (existing oracle) |
| M28 | strict_row | KILLED | selftest+harness | KILLED (existing oracle) |
| M29 | lenient_row | SURVIVED | - | SURVIVED -> KILLED by F29 |
| M30 | lenient_row | KILLED | selftest+harness | KILLED (existing oracle) |
| M31 | lenient_row | KILLED | selftest+harness | KILLED (existing oracle) |
| M32 | lenient_row | KILLED | selftest+harness | KILLED (existing oracle) |
| M33 | registry_cells | SURVIVED | - | SURVIVED -> KILLED by F33 |
| M34 | registry_id | KILLED | selftest | KILLED (existing oracle) |
| M35 | registry_id | KILLED | selftest+harness | KILLED (existing oracle) |
| M36 | registry_id | KILLED | selftest+harness | KILLED (existing oracle) |
| M37 | registry_id | SURVIVED | - | SURVIVED -> KILLED by F37 |
| M38 | registry_id | KILLED | selftest+harness | KILLED (existing oracle) |
| M39 | scope_covers | KILLED | selftest+harness | KILLED (existing oracle) |
| M40 | scope_covers | KILLED | selftest+harness | KILLED (existing oracle) |
| M41 | scope_covers | KILLED | selftest+harness | KILLED (existing oracle) |
| M42 | scope_covers | SURVIVED | - | SURVIVED -> KILLED by F42 |
| M43 | scope_covers | KILLED | selftest+harness | KILLED (existing oracle) |
| M44 | scope_covers | SURVIVED | - | EQUIVALENT |
| M45 | scope_covers | SURVIVED | - | SURVIVED -> KILLED by F45 |
| M46 | scope_covers | SURVIVED | - | SURVIVED -> KILLED by F46 |
| M47 | scope_covers | KILLED | selftest+harness | KILLED (existing oracle) |
| M48 | scope_covers | SURVIVED | - | SURVIVED -> KILLED by F48 |
| M49 | scope_covers | SURVIVED | - | SURVIVED -> KILLED by F49 |
| M50 | scope_covers | SURVIVED | - | SURVIVED -> KILLED by F50 |
| M51 | to_int | SURVIVED | - | SURVIVED -> KILLED by F51 |
| M52 | TOKEN_RE | KILLED | selftest | KILLED (existing oracle) |
| M53 | TOKEN_RE | KILLED | selftest | KILLED (existing oracle) |
| M54 | RUN_RE | SURVIVED | - | SURVIVED -> KILLED by F54 |
| M55 | SID_RE | SURVIVED | - | SURVIVED -> KILLED by F55 |
| M56 | URL_RE | SURVIVED | - | SURVIVED -> KILLED by F56 |
| M57 | constants | SURVIVED | - | EQUIVALENT |
| M58 | constants | SURVIVED | - | SURVIVED -> KILLED by F58 |
| M59 | constants | SURVIVED | - | SURVIVED -> KILLED by F59 |
| M60 | constants | SURVIVED | - | SURVIVED -> KILLED by F60 |
| M61 | constants | KILLED | selftest+harness | KILLED (existing oracle) |
| M62 | constants | SURVIVED | - | SURVIVED -> KILLED by F62 |
| M63 | Repo.regular_oid | SURVIVED | - | EQUIVALENT |
| M64 | Repo.regular_oid | SURVIVED | - | EQUIVALENT |
| M65 | Repo.regular_oid | KILLED | selftest | KILLED (existing oracle) |
| M66 | Repo.blob | SURVIVED | - | EQUIVALENT |
| M67 | Repo.listing | KILLED | selftest+harness | KILLED (existing oracle) |
| M68 | Repo.listing | KILLED | selftest+harness | KILLED (existing oracle) |
| M69 | Repo.resolve | SURVIVED | - | SURVIVED -> KILLED by F69 |
| M70 | Repo.listing | SURVIVED | - | EQUIVALENT |
| M71 | Repo.listing | KILLED | selftest+harness | KILLED (existing oracle) |

## Mutated lines (exact)

Each is a single-line substring replacement applied with `str.replace` to the pinned counter; `mutate.py` asserts the old text occurs exactly once and the line count is unchanged.

- **M01** split_lines — line-separator swap: `return data.decode("utf-8", "replace").split("\n")` → `return data.decode("utf-8", "replace").split("\r\n")`
- **M02** split_lines — decode error policy: `return data.decode("utf-8", "replace").split("\n")` → `return data.decode("utf-8", "ignore").split("\n")`
- **M03** split_lines — splitlines() instead of split: `return data.decode("utf-8", "replace").split("\n")` → `return data.decode("utf-8", "replace").splitlines()`
- **M04** fence_open — indent bound widened 3->4: ``     if n > 3 or n >= len(line) or line[n] not in "`~": `` → ``     if n > 4 or n >= len(line) or line[n] not in "`~": ``
- **M05** fence_open — fence minimum length 3->4: `    if m - n < 3:` → `    if m - n < 4:`
- **M06** fence_open — backtick/tilde operator swap: ``     if ch == "`" and "`" in line[m:]: `` → ``     if ch == "~" and "`" in line[m:]: ``
- **M07** fence_open — info-string bound off-by-one: ``     if ch == "`" and "`" in line[m:]: `` → ``     if ch == "`" and "`" in line[m - 1:]: ``
- **M08** fence_close — closer indent bound widened: `    if n > 3:` → `    if n > 4:`
- **M09** fence_close — closer length off-by-one: `    return m - n >= length and line[m:].strip(" \t") == ""` → `    return m - n >= length - 1 and line[m:].strip(" \t") == ""`
- **M10** fence_close — closer tail whitespace widened: `    return m - n >= length and line[m:].strip(" \t") == ""` → `    return m - n >= length and line[m:].strip() == ""`
- **M11** live_lines — comment opener changed: `            if line.startswith("<!--", i):` → `            if line.startswith("<!", i):`
- **M12** live_lines — comment closer changed: `                if line.startswith("-->", i):` → `                if line.startswith("--> ", i):`
- **M13** live_lines — comment open skip off-by-one: `                    i += 4` → `                    i += 1`
- **M14** live_lines — comment close skip off-by-one: `                i += 3` → `                i += 2`
- **M15** live_lines — inverted liveness test: `        if first_pipe_live:` → `        if first_pipe_live is not None:`
- **M16** live_lines — fence state dropped: `            if in_fence is not None:` → `            if False:`
- **M17** live_lines — closer length argument swapped: `                if fence_close(line, *in_fence):` → `                if fence_close(line, in_fence[0], 1):`
- **M18** live_lines — comment state ignored: `        if not in_comment:` → `        if True:`
- **M19** first_cell — leading tab no longer skipped: `    while i < len(line) and line[i] in " \t":` → `    while i < len(line) and line[i] == " ":`
- **M20** first_cell — cell separator search start off-by-one: `    j = line.find("|", i + 1)` → `    j = line.find("|", i)`
- **M21** first_cell — cell text not stripped: `    return line[i + 1:j].strip()` → `    return line[i + 1:j]`
- **M22** first_cell — cell text case-folded: `    return line[i + 1:j].strip()` → `    return line[i + 1:j].strip().lower()`
- **M23** first_cell — pipe test dropped: `    if i >= len(line) or line[i] != "|":` → `    if i >= len(line):`
- **M24** strict_row — left pad relaxed: `    if not (line.startswith("| ") and line.endswith(" |")) or len(line) < 4:` → `    if not (line.startswith("|") and line.endswith(" |")) or len(line) < 4:`
- **M25** strict_row — right pad relaxed: `    if not (line.startswith("| ") and line.endswith(" |")) or len(line) < 4:` → `    if not (line.startswith("| ") and line.endswith("|")) or len(line) < 4:`
- **M26** strict_row — minimum length off-by-one: `    if not (line.startswith("| ") and line.endswith(" |")) or len(line) < 4:` → `    if not (line.startswith("| ") and line.endswith(" |")) or len(line) < 2:`
- **M27** strict_row — cell separator widened: `    return line[2:-2].split(" | ")` → `    return line[2:-2].split("|")`
- **M28** strict_row — cell separator trailing space dropped: `    return line[2:-2].split(" | ")` → `    return line[2:-2].split(" |")`
- **M29** lenient_row — line not stripped: `    s = line.strip()` → `    s = line`
- **M30** lenient_row — leading pipe test changed: `    if s.startswith("|"):` → `    if s.startswith("||"):`
- **M31** lenient_row — trailing pipe test changed: `    if s.endswith("|"):` → `    if s.endswith("||"):`
- **M32** lenient_row — cell text not stripped: `    return [c.strip() for c in s.split("|")]` → `    return s.split("|")`
- **M33** registry_cells — strict cells preferred: `    return lenient_row(line)` → `    return strict_row(line) or lenient_row(line)`
- **M34** registry_id — indent bound widened: `    if n > 3 or n >= len(line) or line[n] != "|":` → `    if n > 4 or n >= len(line) or line[n] != "|":`
- **M35** registry_id — S-id digit count 3->4: `    if k - j - 1 < 3:` → `    if k - j - 1 < 4:`
- **M36** registry_id — id token off-by-one: `    return line[j:k]` → `    return line[j + 1:k]`
- **M37** registry_id — leading whitespace rule narrowed: `    while j < len(line) and line[j].isspace():` → `    while j < len(line) and line[j] == " ":`
- **M38** registry_id — S prefix case folded: `    if j >= len(line) or line[j] != "S":` → `    if j >= len(line) or line[j] != "s":`
- **M39** scope_covers — basename key loses colon: `    key = basename + ":"` → `    key = basename`
- **M40** scope_covers — E3 past-EOF bound dropped: `            if lo is None or hi is None or (nlines is not None and (hi > nlines or lo > nlines)):` → `            if lo is None or hi is None:`
- **M41** scope_covers — range end exclusive: `            elif lo <= line <= hi:` → `            elif lo <= line < hi:`
- **M42** scope_covers — hi parse guard off-by-one: `                if m > k + 1:` → `                if m > k:`
- **M43** scope_covers — comma-separated locator list dropped: `            if k < len(anchor) and anchor[k] == ",":` → `            if False:`
- **M44** scope_covers — occurrence scan step widened: `        pos = anchor.find(key, pos + 1)` → `        pos = anchor.find(key, pos + len(key))`
- **M45** scope_covers — past-EOF verdict dropped: `    return covered and not over` → `    return covered`
- **M46** scope_covers — E3 lo clause dropped: `            if lo is None or hi is None or (nlines is not None and (hi > nlines or lo > nlines)):` → `            if lo is None or hi is None or (nlines is not None and hi > nlines):`
- **M47** scope_covers — locator start off-by-one: `        i = pos + len(key)` → `        i = pos`
- **M48** scope_covers — digit class widened: `            while j < len(anchor) and anchor[j] in "0123456789":` → `            while j < len(anchor) and anchor[j].isdigit():`
- **M49** scope_covers — digit class widened (hi): `                while m < len(anchor) and anchor[m] in "0123456789":` → `                while m < len(anchor) and anchor[m].isdigit():`
- **M50** scope_covers — locator digit bound off-by-one: `            lo = int(anchor[i:j]) if j - i < 19 else None` → `            lo = int(anchor[i:j]) if j - i < 18 else None`
- **M51** to_int — digit-run bound off-by-one: `    return int(run) if len(run) < 19 else None` → `    return int(run) if len(run) < 18 else None`
- **M52** TOKEN_RE — token min length widened: `TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")` → `TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{2,}")`
- **M53** TOKEN_RE — token min length dropped: `TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")` → `TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")`
- **M54** RUN_RE — digit-run boundary widened: `RUN_RE = re.compile(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])")` → `RUN_RE = re.compile(r"(?<![A-Za-z0-9])[0-9]+(?![0-9])")`
- **M55** SID_RE — S-id boundary dropped: `SID_RE = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")` → `SID_RE = re.compile(r"S[0-9]{3}")`
- **M56** URL_RE — URL token widened: `URL_RE = re.compile(r"https?://\S+")` → `URL_RE = re.compile(r"https?://.*")`
- **M57** constants — echo threshold lowered: `ECHO_MIN = 30` → `ECHO_MIN = 29`
- **M58** constants — echo threshold raised: `ECHO_MIN = 30` → `ECHO_MIN = 31`
- **M59** constants — proposition length bound lowered: `K_MIN, H_MIN = 40, 20` → `K_MIN, H_MIN = 39, 19`
- **M60** constants — proposition length bound raised: `K_MIN, H_MIN = 40, 20` → `K_MIN, H_MIN = 41, 21`
- **M61** constants — new_rows denominator changed: `NEW_ROWS_DENOM = 8` → `NEW_ROWS_DENOM = 7`
- **M62** constants — executable blob mode dropped: `REGULAR_MODES = ("100644", "100755")` → `REGULAR_MODES = ("100644",)`
- **M63** Repo.regular_oid — path dot-dot guard dropped: `        if any(c in ("", ".", "..") for c in comps):` → `        if any(c in ("", ".") for c in comps):`
- **M64** Repo.regular_oid — tree mode test dropped: `                if mode != "040000" or typ != "tree":` → `                if typ != "tree":`
- **M65** Repo.regular_oid — blob mode test dropped: `                if typ != "blob" or mode not in REGULAR_MODES:` → `                if typ != "blob":`
- **M66** Repo.blob — blob cache disabled: `        if oid not in self.blobs:` → `        if True:`
- **M67** Repo.listing — ls-tree record split changed: `                meta, _, name = rec.partition(b"\t")` → `                meta, _, name = rec.partition(b" ")`
- **M68** Repo.listing — ls-tree NUL termination dropped: `            out = self.git("ls-tree", "-z", tree_oid).stdout` → `            out = self.git("ls-tree", tree_oid).stdout`
- **M69** Repo.resolve — rev peel changed: `        p = self.git("rev-parse", "--verify", "-q", rev + "^{commit}", check=False)` → `        p = self.git("rev-parse", "--verify", "-q", rev + "^{tree}", check=False)`
- **M70** Repo.listing — meta split argument changed: `                mode, typ, oid = meta.decode().split(" ")` → `                mode, typ, oid = meta.decode().split(" ", 2)`
- **M71** Repo.listing — empty ls-tree record guard dropped: `            if not rec:` → `            if False:`

## Fixture details (verified)

All 28 fixtures and the CLI check are in receipts/fixtures-results.json (full stdout and stderr). Summary:

| F | mutant | fixture | base rc | mut rc | verdict |
|---|---|---|---|---|---|
| F02 | M02 | invalid UTF-8 byte between locator 33 and -34 in the S383 anchor | 1 | 0 | KILLED |
| F03 | M03 | CRLF line endings in the entry | 1 | 0 | KILLED |
| F04 | M04 | 4-space ``` line around K05 (not a fence in CommonMark) | 0 | 1 | KILLED |
| F06 | M06 | ``` `x` opener around K05 (backtick in info string) | 1 | 1 | KILLED |
| F08 | M08 | ``` opener around K05, 4-space closer after it | 1 | 1 | KILLED |
| F10 | M10 | ``` opener around K05, closer with trailing VT | 1 | 1 | KILLED |
| F11 | M11 | <!DOCTYPE html> line before K05 (no close) | 0 | 1 | KILLED |
| F13 | M13 | <!--> opener before K05, --> after it | 1 | 0 | KILLED |
| F19 | M19 | leading tab on the K05 row | 1 | 1 | KILLED |
| F25 | M25 | K05 row ends '`|' (no space before final pipe) | 1 | 1 | KILLED |
| F29 | M29 | trailing space after the K05 row | 1 | 1 | KILLED |
| F33 | M33 | double space before the S383 status separator | 0 | 1 | KILLED |
| F37 | M37 | tab after the S383 opening pipe | 0 | 1 | KILLED |
| F42 | M42 | S383 anchor '33-,' dangling hyphen | 1 | 1 | KILLED |
| F45 | M45 | S383 anchor with a covering range AND 9999 | 1 | 0 | KILLED |
| F46 | M46 | S383 anchor with reversed range 5000-5 beside 33-34 | 1 | 0 | KILLED |
| F48 | M48 | S383 anchor '105²' (superscript digit) | 0 | 1 | KILLED |
| F49 | M49 | S383 anchor '34²' range end | 1 | 1 | KILLED |
| F50 | M50 | pin absent; 18-digit locator beside 33 in S383 anchor | 1 | 1 | KILLED |
| F51 | M51 | K04 proposition gains a zero-padded 18-digit '3' | 0 | 1 | KILLED |
| F54 | M54 | K04 proposition gains 'config7' | 0 | 1 | KILLED |
| F55 | M55 | source line gains S3999 (not a registry row) | 0 | 1 | KILLED |
| F56 | M56 | S383 source cell has text after its URL | 0 | 1 | KILLED |
| F58 | M58 | K07 proposition = its 30-char quote + echo text | 1 | 0 | KILLED |
| F59 | M59 | K05 proposition of exactly 39 characters | 1 | 0 | KILLED |
| F60 | M60 | K05 proposition of exactly 40 characters | 0 | 1 | KILLED |
| F62 | M62 | entry file mode 100755 | 0 | 1 | KILLED |
| F69 | M69 | --rev <tree oid> (not a commit) | 2 | 0 | KILLED |

E26 (M26 output-level check, not a fixture of the set): inserting `| |` and `|  |` lines into the entry and a `| |` line into the registry gives identical counter output for the baseline and M26 (`True`).

## Proposed additions (smallest fixture or control per survivor)

Each addition below is exactly the F-transform in `fixtures.py`, verified against the mutant above. Adding them as harness controls (`r56_ctl_c1.py`) or selftest cases would kill the mutants in the oracle itself:

- F02 (kills M02): invalid UTF-8 byte between locator 33 and -34 in the S383 anchor. Baseline shows: scope:K* (line 34 uncovered).
- F03 (kills M03): CRLF line endings in the entry. Baseline shows: row:K* (CR is a trailing byte).
- F04 (kills M04): 4-space ``` line around K05 (not a fence in CommonMark). Baseline shows: none (TARGET_MET).
- F06 (kills M06): ``` `x` opener around K05 (backtick in info string). Baseline shows: none (TARGET_MET).
- F08 (kills M08): ``` opener around K05, 4-space closer after it. Baseline shows: row:K05..K30,H01..H03.
- F10 (kills M10): ``` opener around K05, closer with trailing VT. Baseline shows: row:K06.. (closer does not match).
- F11 (kills M11): <!DOCTYPE html> line before K05 (no close). Baseline shows: none (TARGET_MET).
- F13 (kills M13): <!--> opener before K05, --> after it. Baseline shows: row:K05 (K05 hidden in comment).
- F19 (kills M19): leading tab on the K05 row. Baseline shows: row:K05 only (best-effort cells survive).
- F25 (kills M25): K05 row ends '`|' (no space before final pipe). Baseline shows: row:K05 only.
- F29 (kills M29): trailing space after the K05 row. Baseline shows: row:K05 only.
- F33 (kills M33): double space before the S383 status separator. Baseline shows: none (TARGET_MET).
- F37 (kills M37): tab after the S383 opening pipe. Baseline shows: none (TARGET_MET).
- F42 (kills M42): S383 anchor '33-,' dangling hyphen. Baseline shows: scope:K04.. (list ends at 33).
- F45 (kills M45): S383 anchor with a covering range AND 9999. Baseline shows: scope:K* (past-EOF verdict).
- F46 (kills M46): S383 anchor with reversed range 5000-5 beside 33-34. Baseline shows: scope:K* (past-EOF lo).
- F48 (kills M48): S383 anchor '105²' (superscript digit). Baseline shows: none (TARGET_MET).
- F49 (kills M49): S383 anchor '34²' range end. Baseline shows: none (TARGET_MET).
- F50 (kills M50): pin absent; 18-digit locator beside 33 in S383 anchor. Baseline shows: none on scope:K03 (33 covered).
- F51 (kills M51): K04 proposition gains a zero-padded 18-digit '3'. Baseline shows: none (num:K04 passes).
- F54 (kills M54): K04 proposition gains 'config7'. Baseline shows: none (glued digits ignored).
- F55 (kills M55): source line gains S3999 (not a registry row). Baseline shows: none (prov OK).
- F56 (kills M56): S383 source cell has text after its URL. Baseline shows: none (URL ends at whitespace).
- F58 (kills M58): K07 proposition = its 30-char quote + echo text. Baseline shows: echo:K07.
- F59 (kills M59): K05 proposition of exactly 39 characters. Baseline shows: row:K05.
- F60 (kills M60): K05 proposition of exactly 40 characters. Baseline shows: none (accepted).
- F62 (kills M62): entry file mode 100755. Baseline shows: none (TARGET_MET).
- F69 (kills M69): --rev <tree oid> (not a commit). Baseline shows: setup error rc 2.
- F69 is a CLI case, not a tree edit: selftest should assert `--rev <tree oid>` exits 2 with no stdout (the baseline does).

## Deliverables

- `mutants.md` (this file)
- `mutate.py` — generates the 71 mutants from `git show 28fc86ac…:quality/counters/c1-r56-autoreload-entry.py`, runs both oracles, writes results.json. `python3 -I mutate.py <scratch>`
- `diffhelpers2.py` — helper-level differential (baseline vs mutant) on fixed batteries; writes diffs2.json
- `fuzz_equiv.py` — random differential for M14, M44, M26, M57
- `fixtures.py` — the 28 proposed fixtures plus the M69 CLI check; each is one edit of a minimal export of the pinned tree (the export is `git -C <lane> archive 28fc86ac… -- corpus/knowledge/hyprland-config-autoreload-r56.md corpus/SOURCES.md corpus/README.md .ufo/waves/round-56/frozen-tables-v2.json .ufo/waves/round-56/fetch | tar -x -C <scratch>/base`)
- `receipts/baseline-selftest.txt`, `receipts/baseline-harness.txt` — the unmutated counter under both oracles
- `receipts/mutants-results.json` — per mutant: selftest rc/out, harness rc/out, verdict, mutant sha256
- `receipts/helper-diffs.json`, `receipts/fuzz-equiv.txt`, `receipts/frozen-quote-lengths.json`
- `receipts/fixtures-results.json` — per fixture: baseline and mutant rc, stdout, stderr
- `receipts/mutant-sha256.txt` — sha256 of every mutant file and of the baseline
