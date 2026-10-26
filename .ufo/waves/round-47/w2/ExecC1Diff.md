# ExecC1Diff — C1 differential fuzz (w2 falsify, round 47)

Verdict: **three contract errors found** in the frozen C1 contract (two root causes worth a v2 freeze before the data
commit, one minor). 3487 differential cases, 65 disagreements (60 holes + 5 declared out-of-contract paths), 39
distinct hole signatures, all reduced to 3 causes. Nothing outside the contract was counted.

- Contract attacked: the docstring of `.ufo/waves/round-47/l1-draft/mado-terminal.py` at the freeze
  `d7527d608ad2b2e3cc398fdde34db7947b254a1a` (`sha256 762d042c96e7e5f2c3187133b0ffe670c1d076b698b958199602cfa019aa6c08`,
  identical in the freeze commit and the working tree).
- Judge: `.ufo/waves/round-47/fetch/xdg-terminal-exec` (`sha256 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`),
  run in the same bwrap allowlist sandbox the C1 counter builds (same 7 externals, no /usr/bin, /usr/share, /etc, /home,
  /fast; `PATH=<root>/bin:/oracle/bin`, `HOME=<root>/home`, `XDG_CACHE_HOME=<root>/.rw/cache`, `LANG=C.UTF-8`).
- Nothing in the lane was written outside `.ufo/waves/round-47/w2/ExecC1Diff/` and this file. Scratch
  `/fast/scratch/hyaku/mado-r47/ExecC1Diff/` was deleted at the end. No tool install, no pacman, no compositor write,
  no terminal launch (the pin ran only with `--print-*`, always with `XDG_CACHE_HOME` inside scratch).

## Method

`w2/ExecC1Diff/fuzz.py` generates cases, materializes each one **twice** (oracle tree / tool tree, so the pin's cache
file is never visible to the tool), runs the pin as `/oracle/xdg-terminal-exec ARGS` and the reference as
`python3 -I /oracle/tool.py print ARGS`, and compares **exit status and stdout bytes** with the case root replaced by
`$ROOT` (stderr is not compared — the contract only speaks about stdout and exit status). A case that differs is
delta-minimized (drop args/files/lines/env keys/execs/modes/links/dirs while the disagreement survives) with a guard
that a minimized case still carries a print option or `--test` (otherwise it would fall into the *declared*
"would launch a terminal" path and be a false positive).

```
python3 -I .ufo/waves/round-47/w2/ExecC1Diff/fuzz.py --work <scratch> --jobs 8 --timeout 25 --max-fail 40 \
        --receipt .ufo/waves/round-47/w2/ExecC1Diff/fuzz-receipt.txt
```

Areas (grammar the frozen `ctl/l1-fuzz.py` does not reach), with the generated case count:

| area | cases | differ | what it covers |
|---|---|---|---|
| `symlink` | 516 | 3 | file/dir symlinks, dangling links, loops, chains, symlinked applications dir, `/dev/null`, cross-dir targets |
| `unreadable` | 28 | 0 | mode-000 lists/entries/dirs/PATH dirs/TryExec targets, unreadable dirs, symlink-to-unreadable |
| `nul` | 42 | 0 | NUL at every position of a list line and of an `Exec` value, NUL in keys/content |
| `cr` | 38 | 0 | CR at every position of a list line and of an `Exec` value, CRLF entries/lists, `\r` delimiters |
| `longline` | 14 | 0 | 4 KiB / 64 KiB comment, list, `Name=`, quoted-`Exec` and key lines; 2000 fields; 64 KiB delimiter |
| `groups` | 36 | 0 | repeated `[Desktop Entry]` at every body position (with/without an action), `[Desktop Action ]`, `[]`, `[`, EOF headers |
| `escape` | 885 | 0 | every printable `\X` in `Exec` unquoted/quoted/`\\X`, every `TerminalArg*`/`TryExec` value escape, every `%` field code |
| `xdg` | 98 | 1 | empty components, `:`, `::`, trailing `/` and `//`, `.`, relative components, duplicate dirs, desktop-name list edges |
| `xte_env` | 127 | 0 | `XTE_EXECARG_COMPAT`/`XTE_CACHE_ENABLED` × 19 values, against the four directives |
| `print` | 344 | 5 (declared) | `--print-content`, `--test`, unknown/malformed options, option order, `-e`/`--`, every delimiter escape |
| `cmdv` | 59 | 23 | `command -v` name space: option-like names, paths, builtins, keywords, script functions, aliases |
| `mixed` | 1300 | 33 | random combination of the above |
| **total** | **3487** | **65** | 60 holes, 5 declared, 0 timeout, 0 invalid |

Receipt: `w2/ExecC1Diff/fuzz-receipt.txt` (+ `.json` with every disagreement and its minimal case),
per-case cause table `w2/ExecC1Diff/classification.txt` (`holes=60 by_cause={'H2 command-v-option': 54, 'H1 find-type-f': 5, 'H3 home-unset': 1}`).

## H1 — `find -L ... -type f` applies to the first applications dir only (5 cases, one cause)

**Mechanism.** `find_entry_paths` builds one expression
`find -L dir1/. dir2/. dir3/. -type f ( -path dir1-pattern ) -o ( -path dir2-pattern ) -o ( -path dir3-pattern )`
(x:760-774). Implicit `-a` binds tighter than `-o`, so the expression is
`(-type f AND group1) OR group2 OR group3`: for every applications dir except the **first** (lowest preference,
`usr/share/applications`) **no file-type test is applied at all**. Any path type whose name matches is printed,
converted to an id by `awk` and registered as an alias (x:782), so a directory / symlink-to-directory / dangling
symlink / device / FIFO named `foo.desktop` in a higher-preference dir **overwrites the alias of a valid regular file
of the same id in a lower-preference dir**. Reading it then fails (or blocks), the entry is skipped, and the id is
gone. The reference models the docstring's claim ("`find -L <dir>/. -type f` over the application dirs") and filters
by `S_ISREG` for every dir, so it keeps the regular file.

**Minimal case** (`fuzz` id `sym003`, tree shown by `repro.py`): `usr/share/applications/foot.desktop` = a valid
terminal entry, `home/.local/share/applications/foot.desktop` = an **empty directory**, `bin/foot` = stub.

```
pin  rc=1  stdout=''        stderr: ".../xdg-terminal-exec: line 985: read: 0: read error: Is a directory"
                                   "No valid terminal entry was found in:" ...
tool rc=0  stdout='<root>/usr/share/applications/foot.desktop\n'
```

**Script lines:** `766` (`set -- "$@" -type f`), `769-774` (the `-o` groups), `782` (alias overwritten by the later
path), `790` (fallback id), `985` (the `read` that fails on a directory) and `1017` (`done < "$xte__entry_path"`).

**Three faces of the same cause, all measured** (`w2/ExecC1Diff/hand-receipts.txt`):

| case | shadowing path | pin | tool |
|---|---|---|---|
| `H1` | directory `foot.desktop` in `home/.local/share/applications` | rc=1, no stdout | rc=0, prints the usr path |
| `H1b` | symlink `foot.desktop` → `/dev/null` | rc=1, no stdout | rc=0, prints the usr path |
| `H1c` | **FIFO** `foot.desktop` | **rc=124 (blocks forever; killed by the probe's `timeout`)** | rc=0, prints the usr path |

`H1c` is the sharp edge: a FIFO named `*.desktop` in a higher-preference applications dir makes the real resolver
hang on `read`, while the reference returns a selection (measured with `timeout 8`, `timeout 10` and `timeout 20`;
124 every time).
A dangling symlink (left by a removed package) has the same shadowing effect — measured as `fuzz` id `mix970`
(pin rc=1, tool prints the `--test` line).

**Reproduce:**

```
sh .ufo/waves/round-47/w2/ExecC1Diff/hand-probes.sh          # builds H1, H1b, H1c, H2x4, H3 and writes hand-receipts.txt
python3 -I .ufo/waves/round-47/w2/ExecC1Diff/repro.py --cases \
    .ufo/waves/round-47/w2/ExecC1Diff/fuzz-receipt.txt.json --id sym003 --work <scratch>
```

**Why the counter cannot see it:** `quality/counters/c1-r47-fixtures.json` (190 entries) has only `files` and `exec`
per case — no directory, symlink or mode — and `gen_case` in the counter draws `KEYS` without an option-like
`Exec`/`TryExec`; so clause f/g never build a non-regular `*.desktop` path. The hole is in the **contract text**, not
in the counter's score: a tool that matched the pin on these inputs would still pass the frozen counter.

## H2 — `command -v` parses an option-like name as its own option (54 cases, one cause)

**Mechanism.** The resolver validates `TryExec` (x:936) and `Exec[0]` (x:964) with `command -v "$name" >/dev/null`.
Bash's `command` builtin parses its *operand* as an option when it begins with `-`: a name that is a valid option
cluster leaves `command` with no operand and it exits **0**. The reference's `command_v()` returns False for any name
starting with `-` (`if name == "" or name.startswith("-"): return False`), so it rejects entries the pin accepts.

Measured table (the exact check the script makes; `hand-receipts.txt`):

```
-p -> 0   -v -> 0   -V -> 0   -- -> 0   -pv -> 0   -pV -> 0   -vp -> 0
-x -> 2   -q -> 2   --foo -> 2   - -> 1   -e -> 2   -c -> 2   -a -> 2
```

Only the 0 group diverges (`rc 2` and `rc 1` are both non-zero, so both implementations reject). Reached from
`Exec=` (a first word, so `--print-cmd` prints it verbatim) and from `TryExec=`, and with a leading space in the value
(which `read` strips) or CRLF line endings.

**Minimal cases:** `cmdv001` (`Exec=-p`), `cmdv002` (`--print-cmd`), `cmdv008` (`Exec=--`), `cmdv029` (`TryExec=-p`),
`cmdv032` (`TryExec=--`), `mix009` (`TryExec=-p` after a broken `Exec` line).

```
entry: [Desktop Entry]\nExec=-p\nCategories=System;TerminalEmulator;\n
pin  rc=0  stdout='p.desktop\n'      (and 'p.desktop' with --print-cmd printing '-p')
tool rc=1  stdout=''                 stderr: "No valid terminal entry was found in:" ...
```

**Script lines:** `936` (`command -v "$XTE__EXPANDED_STR"` for TryExec), `964` (`command -v "$XTE__EXEC0"` for Exec).

**Reproduce:** `python3 -I .ufo/waves/round-47/w2/ExecC1Diff/repro.py --cases .ufo/waves/round-47/w2/ExecC1Diff/fuzz-receipt.txt.json --id cmdv001 --work <scratch>`
or `sh .ufo/waves/round-47/w2/ExecC1Diff/hand-probes.sh` (the `H2` block, four entries).

**Why the counter cannot see it:** no fixture and no `gen_case` key uses an option-like `Exec`/`TryExec` (the 13
fixture lines that contain `=-p`/`=--` are all `X-TerminalArg*`/`TerminalArg*` *values*, never `Exec[0]`/`TryExec`).

## H3 — `HOME` unset: exit 2 where the resolver exits 1 (1 case, minor)

**Mechanism.** With `HOME` unset and `XDG_CONFIG_HOME`/`XDG_DATA_HOME` unset, the resolver dies on
`${XDG_CONFIG_HOME:-"${HOME}/.config"}` under `set -u` → **exit 1, empty stdout**. The reference raises
`OutOfContract("HOME unset")` → **exit 2** plus `MADO_TERM_OUT_OF_CONTRACT: HOME unset` on stderr. The docstring's
out-of-contract list does not contain "HOME unset", and it promises "prints exactly what `xdg-terminal-exec` prints …
and exits with its exit status", so the exit status is outside its own declaration (stdout agrees: empty).

**Script line:** `148` (the `HOME` default). **Case:** `xdg098`. **Reproduce:** the `H3` block of `hand-probes.sh`.

## What agreed (the rest of the frozen contract)

3422 of 3487 cases agree, including every case in the areas the frozen `ctl/l1-fuzz.py` did not reach:

- **symlinks** — file links, chains, loops (both skip via ancestor/loop detection), symlinked applications dirs,
  symlinked subdirs holding entries, symlinks to unreadable files, cross-dir targets, link names with invalid
  characters: 513/516 agree; the 3 exceptions are H1.
- **unreadable files** — mode-000 list (resolver exits 1, tool exits 1, empty stdout), mode-000 entry (skipped, keys
  carried over the same way), unreadable dirs, unreadable `TryExec` target, unreadable PATH entry: 28/28.
- **NUL bytes** — at every position of a list line and of an `Exec` value, in keys, in `--print-content`:
  42/42 (both drop NUL before parsing/printing).
- **CR** — CRLF lists and entries, CR inside keys/values/`Exec`, `\r` as a delimiter: 38/38 (CR is not IFS
  whitespace, so it survives `read`; it is `[[:space:]]` for the tokenizer).
- **very long lines** — 4 KiB and 64 KiB comments/list lines/`Name=`/quoted `Exec`, 2000 `%U` fields, 64 KiB
  delimiter: 14/14 (see the observation below for 256 KiB).
- **repeated `[Desktop Entry]` groups** — a second header at every body position, with and without an action,
  `[Desktop Entry]x`, `[Desktop Action ]`, `[]`, `[`, `[Desktop Action act` (unterminated), headers at EOF and the
  resulting `while` loop status: 36/36.
- **every `Exec` escape** — 885 cases: each printable `\X` unquoted, quoted, doubled, and inside `TerminalArg*`
  values; trailing/dangling backslashes; every `%` field code alone and inside words; `%%` and `%f %u` combinations.
  All agree (the `de_expand_str` drop-unknown-backslash rule, the tokenizer's quoting state machine and
  `de_strip_fields`' keep-on-failure rule are modelled exactly).
- **XDG components** — empty values (defaults), `:`, `::`, `:::`, leading/trailing/doubled `/`, `.`, `..`, relative
  components, duplicate dirs, `XDG_CURRENT_DESKTOP` with empty/trailing/doubled `:` and newlines: 97/98; the
  exception is H3.
- **`XTE_EXECARG_COMPAT` / `XTE_CACHE_ENABLED`** — 19 values (including empty, garbage, `TRUE `, ` true`) crossed with
  the four directives and with entries that do/do not define `TerminalArgExec`/`X-ExecArg`: 127/127 (the env sets the
  "configured" flag, so a directive is ignored; `check_bool`'s "Assuming … means no" goes to stderr only).
- **`--print-content`, `--test`, unknown options** — every print-mode combination and order, `--test` winning over
  `--print-cmd`, `--print-content`'s early exit (which also swallows `--test`), unknown/malformed options discarded
  (`--print-idd`, `--print-id=x`, `--dir`, `-x`, `-`), `-e`/`--` breaks, `--print-cmd=`/`--print-delimiter=` with
  `=` inside the value, newline-truncated values: 339/344; the 5 exceptions are the declared paths below.

`printf %b` of delimiters was also checked directly against bash (`w2/ExecC1Diff/printf-diff.py`):
**6743 cases, 6734 agree**, and the 9 differences are *all* non-ASCII `\u`/`\U` escapes — the contract's own declared
exclusion (the reference raises `OutOfContract`, exit 2). Receipt: `w2/ExecC1Diff/printf-diff-receipt.txt`.

## Declared out-of-contract paths — confirmed, not counted as holes

| case | behaviour | declared where |
|---|---|---|
| `prn340-342` (`--print-idd`, `--test=x`, `--hold` only) | pin runs/execs, tool exits 2 | docstring: "without one the resolver would launch a terminal; this tool refuses with exit 2" |
| `prn343-344` (`-h`, `--help`) | pin prints help, exit 0; tool exits 2 | docstring: "-h/--help" |
| `printf-diff` 9 × `\u`/`\U` ≥ 0x80 | pin emits UTF-8, tool exits 2 | docstring: "\\u/\\U escapes beyond ASCII in a delimiter" |

## Observation, not a hole

A 256 KiB quoted `Exec` word (`Exec=foot "aaa…"`) takes the **real resolver ~60 s** (measured 59.9 s, `timeout 120`;
the 20 s fuzz timeout had flagged it) while the reference answers instantly — stdout and exit status are **identical**
(rc=1, empty). So this is a performance property of the resolver's shell loops, not a contract divergence; the
longline family was reduced to 64 KiB after measuring it, and the 256 KiB probe is recorded here rather than in the
receipt.

## Limits of this seat's evidence

- Only `print` is fuzzed. `explain`, `--observed` and `--selftest` are the counter's clauses x and s and were not
  re-judged here.
- The warm-cache path (a pre-existing `$XDG_CACHE_HOME/xdg-terminal-exec`), `-h/--help`, an empty argv element, XDG
  dirs holding glob characters or quotes, and non-ASCII `\u`/`\U` delimiters are declared out of contract and were
  not counted (each tree is fresh, so every run is the cold path).
- My harness omits the counter's `strace` read-only clause (r); the tool's no-process/no-socket claim is the
  counter's, not mine.
- Locale: every run used `LANG=C.UTF-8` (the counter's variant A). `tr '[:upper:]' '[:lower:]'` lowering only ASCII
  in `C.UTF-8` was confirmed, but the `en_US.UTF-8` variant B was not probed for non-ASCII desktop names (the
  counter's generators only draw ASCII desktop strings, so it is unreachable there).
- The fuzzer is my own; it reuses the counter's sandbox recipe (same externals, same allowlist, same env) but is not
  the counter, so its numbers are not counter numbers.

## Files

| path | what |
|---|---|
| `w2/ExecC1Diff/fuzz.py` | the differential harness + generator + minimizer (`--work` honoured, nothing hardcoded) |
| `w2/ExecC1Diff/fuzz-receipt.txt` / `.json` | the 3487-case run: per-area counts, every disagreement, minimal cases |
| `w2/ExecC1Diff/classification.txt` | per-case cause assignment (H1/H2/H3) |
| `w2/ExecC1Diff/repro.py` | rebuild one case from the receipt JSON, print tree/env/argv, run both, print DIFFER |
| `w2/ExecC1Diff/hand-probes.sh` / `hand-receipts.txt` | the four holes reproduced outside the fuzz driver, with the `command -v` table |
| `w2/ExecC1Diff/printf-diff.py` / `printf-diff-receipt.txt` | `printf %b` model vs bash, 6743 cases |

Nothing in the lane was modified outside this directory and this report; no commit, no index write, no package
transaction, no host or compositor mutation.
