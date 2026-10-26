# xdg-terminal-exec 0.14.3 — hidden selection behaviours (differential fuzz)

Seat: ExecRefCompare, round 47 w1 (lane mado-shokunin). Nothing here is frozen; this feeds the
L1's predicate freeze.

Target (pinned): `/usr/bin/xdg-terminal-exec`, 1499 lines,
sha256 `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` (re-hashed this seat).
Locators are written `:N` (or `:A-:B` for a range) and mean line N of that file; they were computed
with `grep -n` / substring search, never typed, and `receipts/locators.txt` re-dumps every cited line with the file's sha256.

## 0. What was run, and how

Every observation is a real run of the pinned script with a `--print-*` option (never bare: a bare
invocation launches a terminal), `stdin=/dev/null`, `XDG_CACHE_HOME` = a fresh empty directory per
run (cold cache), `PATH=$ROOT/bin:<toolbin>`, and a complete environment (`env` never inherited).

- `fuzz.py run`: **730 runs** — 600 random XDG trees from a line-level grammar, plus 23 families
  with 107 one-token variants (each variant differs from its family base in exactly one line
  fragment). 71 distinct outcomes, 44 intra-family flips (`receipts/flips.tsv`).
- `probe.py`: **79 minimal cases**, one per behaviour (`receipts/probes.tsv`,
  `receipts/probe-cases/*.json`).
- **809 case-runs** total in the final campaign; a further 10 replays produced
  `receipts/expansion.txt` (full stderr of the script's own `XTE_DEBUG` output).

Cases are in the frozen fixture schema. One fuzzer-only key is used where a text map cannot express
the setup: `"setup":{"symlinks":{path:target},"modes":{path:<mode int>}}`. A judge that ignores `setup`
sees the same case without the symlink/chmod. `expect` in every case was produced by running the
real script, never typed.

Host filesystem note: fallback ordering below was measured on /fast/scratch (readdir returns
creation order there); §F-09 says why that matters to the judge.

## 1. Selection: list files, IDs, entries

### F-01 A failing higher-priority entry shadows the system entry — and yields NO terminal
Attacks: :782 (alias set, "last found wins"), :790 (fallback list prepend), :1060 (walk list),
:1081/:1085 (alias consumed once), :1086 (read failure `|| continue`).

```json
{"args": ["--print-id", "--print-path", "--print-cmd"], "class": "shadow/hidden-over-system", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 1, "stdout": ""}, "files": {"home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty\nHidden=true\n", "usr/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=foot\n"}, "id": "P01-hidden-shadow"}
```

Observed: `rc=1`, stdout empty. Control with the user entry removed (`P01c-system-only`): the same
system entry resolves, `rc=0`, `foot`.

Mechanism: `find` walks `/usr/share/applications` before `~/.local/share/applications` (:168 builds
`XTE__APPLICATIONS_DIRS` by prepending, so the highest-priority dir is last), the alias at :782 is
overwritten by the later find, and the same ID is registered twice in the fallback list (:790). The
first walk hits the user file, `read_entry_path` fails on `Hidden=true`, and :1085 has already
`unalias`'d the name — so the second occurrence falls through :1081 and the system copy is never
read. `P01b-invalid-shadow` (user entry whose `Exec=ghost` is not on PATH) gives the same `rc=1`.
This is not "the user override wins"; it is "the user override either wins or blocks".

Tool consequence: C1 must model a per-ID single-slots map keyed by the last-found path, and must
delete the slot after the first attempt, not fall back to the earlier path.

### F-02 A listed ID that fails validation consumes its own fallback slot
Attacks: :442 (ID appended to the explicit list), :1060, :1085, :1090.

```json
{"args": ["--print-id", "--print-path", "--print-cmd"], "class": "list/action-unlisted", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 1, "stdout": ""}, "files": {"home/.config/xdg-terminals.list": "Alacritty.desktop:New\n", "home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty\nTerminalArgExec=-e\n"}, "id": "P19-action-consumes-fallback"}
```

Observed: `rc=1`, stdout empty, stderr `No valid terminal entry was found in:` + dirs. Control
`P19b-control-unlisted-not-listed` (no list file, same entry): `rc=0`, `Alacritty.desktop`.
The list line `Alacritty.desktop:New` asks for an action the entry does not declare in `Actions`;
the entry is discarded, and because the same ID was unaliased the plain fallback candidate is gone.

Tool consequence: the unalias-at-first-attempt rule applies to the explicit list too; an invalid
list line can make the terminal platform-unresolvable.

### F-03 Duplicate keys are conjunctive, not last-wins
Attacks: :816-:826 (Categories), :947-:964 (Exec), :938-:946 (Hidden), :1086.

Every `Categories` line is tested; one that lacks the exact category discards the entry — even if
an earlier line had it. Every `Exec` line must be valid; one that fails `command -v` (:964) discards
the entry — even if an earlier line was fine. Two *valid* `Exec` lines: the last one wins.

```json
{"args": ["--print-id", "--print-path", "--print-cmd"], "class": "entry/duplicate-key", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty"], "expect": {"rc": 1, "stdout": ""}, "files": {"home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nName=Alacritty\nType=Application\nCategories=Xterm;\nCategories=TerminalEmulator;\nExec=alacritty\nTerminalArgExec=-e\n"}, "id": "F04-cat-second-good"}
```

Observed `rc=1` (`Categories=Xterm;` then `Categories=TerminalEmulator;`). Mirror cases:
`F04-exec-second-missing` (`Exec=alacritty` then `Exec=nothere`) `rc=1`;
`P20-exec-twice-valid` (`Exec=alacritty` then `Exec=foot`) `rc=0`, cmd `foot`;
`P20b-cat-twice-valid` `rc=0`.

### F-04 Key matching is a prefix match, not `key=`
Attacks: :816 (`'Categories'*=*`), :831, :846, :865, :933, :938, :947 — all `'Key'*=*` arms.

`CategoriesFoo=TerminalEmulator;` classifies as a terminal; `ExecFoo=alacritty` sets the command;
`HiddenFoo=true` hides the entry; `TryExecX=ghost` rejects it.

```json
{"args": ["--print-id", "--print-path", "--print-cmd"], "class": "entry/key-prefix", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "Alacritty.desktop\n$ROOT/home/.local/share/applications/Alacritty.desktop\nalacritty\n"}, "files": {"home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategoriesFoo=TerminalEmulator;\nExec=alacritty\n"}, "id": "P02-key-prefix-cat"}
```

Observed `rc=0` (chosen via the bogus key). `P02b-key-prefix-exec` `rc=0`; `P02c-key-prefix-hidden`
`rc=1`; `P02d-key-prefix-tryexec` `rc=1`.

Note the asymmetry: the *key* is loose, the *category word* is exact — `Categories=TerminalEmulatorX;`
and `Categories=terminalemulator;` both reject (`P10i-cat-prefix-word` rc=1, `P10j-cat-lower` rc=1),
while `Categories=TerminalEmulator` without the trailing `;` is accepted (`F02-no-trailing-semi`,
rc=0) because the value is split on `;`.

```json
{"args": ["--print-id", "--print-path", "--print-cmd"], "class": "entry/categories", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 1, "stdout": ""}, "files": {"home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulatorX;\nExec=alacritty\n"}, "id": "P10i-cat-prefix-word"}
```

### F-05 Section handling: prefix header, keys before the header, later Exec overrides
Attacks: :989 (`'[Desktop Entry]'*)`), :991 (any line starting alnum/`-` is a Key=Value), :993/:995
(value split at the first `=`, then leading spaces only), :1014 (stop at the next group header),
:958-:964.

- `[Desktop Entry] comment` counts as the header (:989 prefix match); `[Desktop Entry` (unclosed)
  and `[KDE Entry]` do not, so `read_exec` never turns on and the entry is discarded
  (`F05-unclosed` rc=1).
- `Categories=` before the header still counts (`P03-preheader-cat` rc=0); an `Exec=` before the
  header is silently ignored (`P03b-preheader-exec` rc=0, command comes from the later line).
- A second `[Desktop Entry]` does not stop parsing; a later `Exec=ghost` then overrides and kills
  the entry (`P03c-header-twice` rc=1).

```json
{"args": ["--print-id", "--print-path", "--print-cmd"], "class": "entry/pre-header", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "Alacritty.desktop\n$ROOT/home/.local/share/applications/Alacritty.desktop\nalacritty\n"}, "files": {"home/.local/share/applications/Alacritty.desktop": "Categories=TerminalEmulator;\n[Desktop Entry]\nExec=alacritty\n"}, "id": "P03-preheader-cat"}
```

### F-06 `Hidden` is exactly `true`
Attacks: :938-:946 (`case "$xte__value" in true) ...`), :995 (leading spaces stripped).

`Hidden=True`, `Hidden=TRUE`, `Hidden=1` do **not** hide (`F06-True` rc=0, selected), `Hidden=true`
does (`F06-true` rc=1), and `Hidden= true` also hides because the leading space is stripped at :995
(`F06-spaced` rc=1). Contrast `check_bool` (:52), which accepts `True|TRUE|yes|1` for *its* uses.

```json
{"args": ["--print-id", "--print-path", "--print-cmd"], "class": "entry/hidden-case", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty"], "expect": {"rc": 0, "stdout": "Alacritty.desktop\n$ROOT/home/.local/share/applications/Alacritty.desktop\nalacritty\n"}, "files": {"home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nName=Alacritty\nType=Application\nCategories=TerminalEmulator;\nExec=alacritty\nHidden=True\nTerminalArgExec=-e\n"}, "id": "F06-True"}
```

### F-07 Show-in rules apply to fallback only, and match case-sensitively
Attacks: :1058 (`xte__de_checks=false`), :1071 (flip to true at the fallback marker), :846/:865, :1144
(lowercased name only for file discovery).

`NotShowIn=Hyprland;` rejects a fallback entry but is ignored when the same ID is written in a list
file (`F16-explicit` rc=0). `OnlyShowIn=hyprland;` never matches `XDG_CURRENT_DESKTOP=Hyprland`
(`P10f-showin-case` rc=1) — only the *file name* is lowercased, never the comparison.

```json
{"args": ["--print-id", "--print-path", "--print-cmd"], "class": "entry/showin", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "Foot.desktop\n$ROOT/usr/share/applications/Foot.desktop\nfoot\n"}, "files": {"home/.config/xdg-terminals.list": "Foot.desktop\n", "usr/share/applications/Foot.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=foot\nNotShowIn=Hyprland;\n"}, "id": "F16-explicit"}
```

### F-08 The find filter: invisible files, and a dotfile asymmetry
Attacks: :762/:766 (find arguments), :773 (`-path` + `! -path` filters), :795 (`find -L`), :797
(`awk` builds the ID with `gsub("/","-")`).

Invisible to the resolver: `Ok.Desktop` (wrong case), `Ok Two.desktop` (space), `Ok` (no extension),
`.hidden.desktop` at the top of an applications dir (`F21-space-in-name`, `F21-leading-dot`, both
rc=1). But a dotfile **inside a subdirectory** is registered: `sub/.hidden.desktop` becomes the ID
`sub-.hidden.desktop` (`P16b-dotfile-in-subdir`, rc=0) because only the first path character is
constrained. Nested dirs map `sub/nested/` → `sub-nested-` (`P16-nested-id`).

```json
{"args": ["--print-id", "--print-path", "--print-cmd"], "class": "find/dotfile", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "sub-.hidden.desktop\n$ROOT/home/.local/share/applications/sub/.hidden.desktop\nalacritty\n"}, "files": {"home/.local/share/applications/sub/.hidden.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty\nTerminalArgExec=-e\n"}, "id": "P16b-dotfile-in-subdir"}
```

### F-09 Fallback order is reverse `readdir` order, not lexical
Attacks: :790 (each found ID is prepended), :795 (`find` without a sort), :1060.

Three identical entries created in three different orders in one directory select three different
terminals — always the **last created**:

| creation order | selected |
|---|---|
| Mmm, Aaa, Zzz | `Zzz.desktop` (`P13-order-maz`) |
| Aaa, Zzz, Mmm | `Mmm.desktop` (`P13b-order-azm`) |
| Zzz, Mmm, Aaa | `Aaa.desktop` (`P13c-order-zma`) |

```json
{"args": ["--print-id", "--print-path", "--print-cmd"], "class": "order/readdir", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "Zzz.desktop\n$ROOT/usr/share/applications/Zzz.desktop\nalacritty\n"}, "files": {"usr/share/applications/Aaa.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=foot\n", "usr/share/applications/Mmm.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty\n", "usr/share/applications/Zzz.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty\n"}, "id": "P13-order-maz"}
```

Tool consequence: C1's model must reproduce the observed order for the fixtures it is judged on,
which means the judge's fixtures must not depend on it — see §7.

### F-10 An unreadable **list** file aborts the whole resolution; an unreadable **entry** is skipped
Attacks: :23 (`set -euf`), :365 (`[ -f ]`), :367-:473 (`while read ... done < "$xte__config_path"`,
unguarded), :1198 (unguarded call), versus :1017 + :1086 (`read_entry_path ... || continue`).

```json
{"args": ["--print-id", "--print-path", "--print-cmd"], "class": "list/unreadable", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 1, "stdout": ""}, "files": {"home/.config/xdg-terminals.list": "Foot.desktop\n", "home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty\nTerminalArgExec=-e\n", "usr/share/applications/Foot.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=foot\nTerminalArgExec=-e\n"}, "id": "P18-unreadable-list", "setup": {"modes": {"home/.config/xdg-terminals.list": 0}}}
```

Observed: `rc=1`, stdout empty, stderr is only
`/usr/bin/xdg-terminal-exec: line 361: …/home/.config/xdg-terminals.list: Permission denied` (the failing redirection is :473) — the
`No valid terminal entry was found in:` line is **absent**, i.e. the script died rather than
exhausting candidates. A valid entry existed (`Alacritty.desktop`) and an unreadable list file in a
*lower*-priority dir (`P18b-unreadable-list-lowprio`) kills it just the same.

```json
{"args": ["--print-id", "--print-path", "--print-cmd"], "class": "list/unreadable", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 1, "stdout": ""}, "files": {"etc/xdg/xdg-terminals.list": "Alacritty.desktop\n", "home/.config/xdg-terminals.list": "Foot.desktop\n", "home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty\nTerminalArgExec=-e\n", "usr/share/applications/Foot.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=foot\nTerminalArgExec=-e\n"}, "id": "P18b-unreadable-list-lowprio", "setup": {"modes": {"etc/xdg/xdg-terminals.list": 0}}}
```

By contrast an unreadable desktop entry is a warning plus skip: `P12-unreadable-first` (user copy
chmod 000, a system entry present) → `rc=0`, `Foot.desktop`, stderr
`…/applications/./Alacritty.desktop: Permission denied`.

## 2. `Exec` parsing

### F-11 Tokenizer and field stripping fail open
Attacks: :958 (`de_tokenize_exec`), :960 (`de_strip_fields`, return value discarded), :962 (`EXEC0`),
:964 (`command -v`), :623/:683 (tokenizer's `return 1` paths), :708/:729 (strip's `return 1` paths).

- Unclosed quote: accepted, the fragment becomes an argument — `Exec=alacritty "open` yields
  `alacritty open` (`P05d-unclosed-quote`, rc=0).
- Unknown `%` field: not stripped, not rejected — `Exec=alacritty %Z --tail` yields
  `alacritty %Z --tail` (`P05e-percent-bad`, rc=0). Same for the second `%f`/`%u`
  (`P05f-percent-file` → `alacritty %f %u`, rc=0).
- A *single* `%F` is removed (`F14-field-f` == base), `%%` becomes `%` (`100%%` → `100%`).
- Only when the failure leaves `EXEC_USEP` empty does the entry die: `Exec=$HOME/bin/alacritty` has
  an unquoted `$` (:623), the tokenizer returns before appending anything, and `command -v ""` fails
  (`P05b-dollar-exec`, rc=1). An empty `Exec=` is discarded the same way (`P05g-empty-exec`).

```json
{"args": ["--print-id", "--print-path", "--print-cmd"], "class": "exec/quote", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "Alacritty.desktop\n$ROOT/home/.local/share/applications/Alacritty.desktop\nalacritty\nopen\n"}, "files": {"home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty \"open\n"}, "id": "P05d-unclosed-quote"}
```

```json
{"args": ["--print-id", "--print-path", "--print-cmd"], "class": "exec/percent", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "Alacritty.desktop\n$ROOT/home/.local/share/applications/Alacritty.desktop\nalacritty\n%Z\n--tail\n"}, "files": {"home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty %Z --tail\n"}, "id": "P05e-percent-bad"}
```

### F-12 `Exec[0]` is resolved with `command -v` against the process cwd
Attacks: :964, :1450.

`Exec=./bin/alacritty` is accepted and printed verbatim (`P05-relative-exec`, rc=0,
cmd `./bin/alacritty`) — the existence test is relative to the caller's cwd, not to the entry.
Absolute paths cannot be expressed at all while containing `$` (see F-11).

```json
{"args": ["--print-id", "--print-path", "--print-cmd"], "class": "exec/relative", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "Alacritty.desktop\n$ROOT/home/.local/share/applications/Alacritty.desktop\n./bin/alacritty\n"}, "files": {"home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=./bin/alacritty\n"}, "id": "P05-relative-exec"}
```

### F-13 Whitespace: spaces trimmed, tabs tolerated, CR accepted in an entry, rejected in a list
Attacks: :985 (entry `read -r` with the original IFS), :993/:995 (only leading *spaces* trimmed), :367
(list `read -r`), :425 + :1025 (list-line and ID validation), :571-:686 (tokenizer).

- `Exec=   alacritty` → `alacritty` (:995, `P04b-space-exec` rc=0).
- `Exec=<TAB>alacritty` → also `alacritty` (`P04-tab-exec` rc=0): the leading separator produces an
  empty first field that the `${x:+…}` join drops, so the tab does not create an empty argv[0].
- A CRLF desktop entry is accepted (`P04c-crlf-entry` rc=0): the trailing `\r` is `[:space:]` to the
  tokenizer, and the end-of-string space arm discards it (:653-:666).
- A CRLF **list** line is rejected — `Foot.desktop\r` fails ID validation and prints
  `Discarded possibly misspelled entry 'Foot.desktop\r'` on stderr (`P04e-crlf-list`, rc=0 with the
  fallback entry selected). A UTF-8 BOM at the start of a list line is silently ignored
  (`P04d-bom-list`), as are leading tabs (`P04g-tab-lines-list`, `Foot` still selected).

```json
{"args": ["--print-id", "--print-path", "--print-cmd"], "class": "list/whitespace", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "Alacritty.desktop\n$ROOT/home/.local/share/applications/Alacritty.desktop\nalacritty\n"}, "files": {"home/.config/xdg-terminals.list": "Foot.desktop\r\n", "home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty\nTerminalArgExec=-e\n", "usr/share/applications/Foot.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=foot\nTerminalArgExec=-e\n"}, "id": "P04e-crlf-list"}
```

### F-14 Actions: header suffix tolerated, last action group wins, order matters
Attacks: :1005 (`"[Desktop Action ${action}]"*`), :1014, :839 (`action_listed`), :831.

`[Desktop Action New] extra` is accepted. Two `[Desktop Action New]` groups: the second group's
`Exec` wins (`P10d-action-twice` → `alacritty --second`). An action group placed *before* the
`Actions=` line is discarded (`F13-action-group-before-actions` rc=1) because `action_listed` is
still false at :1005.

```json
{"args": ["--print-id", "--print-path", "--print-cmd"], "class": "list/action", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "Alacritty.desktop:New\n$ROOT/home/.local/share/applications/Alacritty.desktop:New\nalacritty\n--second\n"}, "files": {"home/.config/xdg-terminals.list": "Alacritty.desktop:New\n", "home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty\nActions=New;\n[Desktop Action New]\nExec=alacritty --first\n[Desktop Action New]\nExec=alacritty --second\n"}, "id": "P10d-action-twice"}
```

## 3. Print modes

### F-15 Output order is fixed; only a `\n` delimiter gets a trailing newline; cache differs per mode
Attacks: :1221/:1223 (delimiter defaults), :1331 (id), :1337/:1342 (path), (:1368-:1385 early bail),
:1457 (`save_cache "$1" &`), :1480/:1486 (cmd delimiters).

- Order is always id, path, content, cmd regardless of argument order (`P07c-reversed-order`).
- Repeated flags collapse to one print each (`P07d-duplicate-flags` → `Alacritty.desktop` + `alacritty`).
- `--print-delimiter=|` prints `id|path` with **no** trailing newline; `--print-delimiter=` (empty)
  prints `idpath` with no separator and no newline (`P07f-delim-empty`).
- `--print-cmd=` (empty) prints the command with no newline (`P07e-cmd-empty-delim`); `--print-cmd=,`
  joins argv with no newline.
- `--print-id`/`--print-path`/`--print-content` exit at :1374-:1383 **before** the cache save, so they
  never write `XDG_CACHE_HOME`; `--print-cmd` does write it (:1457)
  (`receipts/cache.tsv`: `P06-cache-print-id` → empty, `P06b-cache-print-cmd` →
  `xdg-terminal-exec`).

```json
{"args": ["--print-id", "--print-path", "--print-delimiter="], "class": "args/delimiter", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "Alacritty.desktop$ROOT/home/.local/share/applications/Alacritty.desktop"}, "files": {"home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty\nTerminalArgExec=-e\n"}, "id": "P07f-delim-empty"}
```

### F-16 `--print-path` rewrites any `/./` in the path and can emit a non-existent path
Attacks: :1342 (`${PATH%%/./*}/${PATH##*/./}`).

Because `find` is handed `<dir>.` (:762), every entry path normally contains one `/./` and the
rewrite is harmless. Any data dir that itself contains a `./` segment (or an empty element, §F-21)
breaks it: `XDG_DATA_DIRS=$ROOT/usr/./share` prints `$ROOT/usr/Foot.desktop` — a path that does not
exist (`P15b-dot-segment-path`, `F10-dot-segment`). The rule keeps everything before the *first*
`/./` and the last component after the *last* `/./`.

```json
{"args": ["--print-path"], "class": "find/path-rewrite", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/./share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "$ROOT/usr/Foot.desktop\n"}, "files": {"usr/share/applications/Foot.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=foot\nTerminalArgExec=-e\n"}, "id": "P15b-dot-segment-path"}
```

### F-17 Nothing found
Attacks: :1208 (`find_entry || exit 1`), :1109 (`error "No valid terminal entry was found in:"`).

`rc=1`, stdout completely empty, stderr lists the applications dirs. All 16 `rc=1` probe cases and
569 of 730 fuzz runs behaved this way, so "empty stdout + rc1" is the normal `NO_TERMINAL` shape.

## 4. Argument handling

### F-18 Space-separated options are silently swallowed and become the command
Attacks: :1252 (`--dir=*` only), :1313 (`[!-]*` breaks), :1317 (`-*` shifts and discards), :1231
(`-e | "$XTE__EXECARG"` breaks).

`--print-cmd --dir /x -- cmd` produces `alacritty -e /x -- cmd`: `--dir` is dropped by :1317, `/x` is
a non-option so option parsing stops, and the value is prepended with `-e` (:1389). Unknown options are
discarded without a message (`P07b-unknown-option` prints id+path normally).

```json
{"args": ["--print-cmd", "--dir", "/x", "--", "cmd"], "class": "args/space-form", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "alacritty\n-e\n/x\n--\ncmd\n"}, "files": {"home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty\nTerminalArgExec=-e\n"}, "id": "P07-dir-space-form"}
```

### F-19 Prepend order, and empty-valued terminal args
Attacks: :1388-:1389 (execarg), :1393 (hold), :1400 (dir), :1415 (title), then app-id, :1450 (exec).

Final argv = `Exec…`, `TerminalArgAppId`, `TerminalArgTitle`, `TerminalArgDir`, `TerminalArgHold`,
`TerminalArgExec`, user args — in that order (`P07g-verbose-order`: `alacritty --class=A --title=T
--working-directory=D --hold -e cmd`). `TerminalArgExec=` (empty but defined) removes `-e` (:1388)
(`P07h-empty-execarg` → `alacritty cmd`). `--hold` with no `TerminalArgHold` is dropped silently
(`P10h-hold-no-arg` → `alacritty -e cmd`); an empty `--title=`/`--dir=` value is dropped too (`P22-empty-option-values` → `alacritty -e cmd`).

```json
{"args": ["--print-cmd", "--app-id=A", "--title=T", "--dir=D", "--hold", "--", "cmd"], "class": "args/prepend-order", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "alacritty\n--class=A\n--title=T\n--working-directory=D\n--hold\n-e\ncmd\n"}, "files": {"home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty\nTerminalArgExec=-e\nX-TerminalArgAppId=--class=\nX-TerminalArgTitle=--title=\nX-TerminalArgDir=--working-directory=\nX-TerminalArgHold=--hold\n"}, "id": "P07g-verbose-order"}
```

### F-20 `execarg` compat is on by default; the first directive wins
Attacks: :1147 (`XTE__EXECARG_COMPAT=${XTE_EXECARG_COMPAT-true}`), 390/396 (first-directive-wins
guard), :1092-:1099, :1128 (`-e`).

An entry with no `TerminalArgExec` is accepted with `-e` (`P07j-execarg-default` shows the custom
`--x` from `/execarg_default:…`). `/execarg_strict` discards such entries (`P07i-no-execarg-strict`
rc=1, `F19-strict` rc=1), and a later `/execarg_compat` in the same or a following file does not
undo it (:390/:396).

```json
{"args": ["--print-cmd", "--", "cmd"], "class": "args/compat-default", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "alacritty\n--x\ncmd\n"}, "files": {"home/.config/xdg-terminals.list": "/execarg_default:Alacritty.desktop:--x\nAlacritty.desktop\n", "home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty\n"}, "id": "P07j-execarg-default"}
```

## 5. Environment expansion

### F-21 An empty element in `XDG_CONFIG_DIRS`/`XDG_DATA_DIRS` becomes a root-absolute path
Attacks: :148, :151-:153 (config build), :157-:162 (data config build), :168 (applications build).

```json
{"args": ["--print-id"], "class": "env/expansion", "env": {"XDG_CONFIG_DIRS": ":$ROOT/etc/xdg/", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/share/:$ROOT/opt//x", "XDG_DATA_HOME": "$ROOT/home/.local/share", "XTE_DEBUG": "1"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "Alacritty.desktop\n"}, "files": {"home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty\nTerminalArgExec=-e\n"}, "id": "P11-expanded-paths"}
```

`XDG_CONFIG_DIRS=":$ROOT/etc/xdg/"` puts `/hyprland-xdg-terminals.list` and `/xdg-terminals.list`
into `XTE__CONFIGS` (observed in the script's own debug line, `receipts/expansion.txt`). A *middle*
empty element does the same for the data hierarchy: `XDG_DATA_DIRS="$ROOT/usr/share::$ROOT/opt/x"`
yields `/xdg-terminal-exec/hyprland-xdg-terminals.list`, `/xdg-terminal-exec/xdg-terminals.list`
and `/applications/` in the dir list (`P17-double-colon`). A *trailing* empty element is dropped
(`XDG_DATA_DIRS="$ROOT/usr/share:"` adds nothing, `P15-empty-data-element`).

```json
{"args": ["--print-id"], "class": "env/expansion", "env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/share::$ROOT/opt/x", "XDG_DATA_HOME": "$ROOT/home/.local/share", "XTE_DEBUG": "1"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "Alacritty.desktop\n"}, "files": {"home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty\nTerminalArgExec=-e\n"}, "id": "P17-double-colon"}
```

### F-22 An empty (but set) variable is replaced by the default
Attacks: :148, :157, :166 (`:-` expansion).

`XDG_CONFIG_DIRS=""` is not "no config dirs": `/etc/xdg` is used instead, so a list file in the
case's own `etc/xdg` is **not** read (`P08d-config-dirs-empty-string` selects the fallback
`Alacritty.desktop`) while `XDG_CONFIG_DIRS=$ROOT/etc/xdg` reads it (`P08c-config-dirs-empty` selects
`Foot.desktop`). The same applies to `XDG_DATA_DIRS=""`, `XDG_DATA_HOME=""` and
`XDG_CONFIG_HOME=""` (`P21-config-home-empty-string` reads `$HOME/.config/xdg-terminals.list` and
selects `Foot.desktop`, proving the default substitution).

```json
{"args": ["--print-id"], "class": "env/empty-string", "env": {"XDG_CONFIG_DIRS": "", "XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_DATA_DIRS": "$ROOT/usr/local/share:$ROOT/usr/share", "XDG_DATA_HOME": "$ROOT/home/.local/share"}, "exec": ["bin/alacritty", "bin/foot"], "expect": {"rc": 0, "stdout": "Alacritty.desktop\n"}, "files": {"etc/xdg/xdg-terminals.list": "Foot.desktop\n", "home/.local/share/applications/Alacritty.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=alacritty\nTerminalArgExec=-e\n", "usr/share/applications/Foot.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=foot\nTerminalArgExec=-e\n"}, "id": "P08d-config-dirs-empty-string"}
```

## 6. All 44 flips found by one-token mutation (`receipts/flips.tsv`; `~` = the case root)

| family | one-token delta | base selection | variant selection |
|---|---|---|---|
| F04 | `cat-second-bad` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | <rc1> |
| F04 | `cat-second-good` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | <rc1> |
| F04 | `exec-second-missing` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | <rc1> |
| F04 | `exec-second-ok` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | <rc1> |
| F04 | `hidden-second` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | <rc1> |
| F05 | `unclosed` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | <rc1> |
| F05 | `kde-group` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | <rc1> |
| F06 | `true` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | <rc1> |
| F06 | `spaced` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | <rc1> |
| F07 | `dangling` | Linked.desktop (…/applications/Linked.desktop) → alacritty | <rc1> |
| F08 | `mode000` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | <rc1> |
| F10 | `leading-colon` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | Foot.desktop (…/applications/Foot.desktop) → foot |
| F10 | `trailing-colon` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | Foot.desktop (…/applications/Foot.desktop) → foot |
| F10 | `double-colon` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | Foot.desktop (…/applications/Foot.desktop) → foot |
| F10 | `trailing-slash` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | Foot.desktop (…/applications/Foot.desktop) → foot |
| F10 | `dot-segment` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | Foot.desktop (~/usr/Foot.desktop) → foot |
| F12 | `system-only` | Same.desktop (…/applications/Same.desktop) → alacritty | Same.desktop (…/applications/Same.desktop) → foot |
| F13 | `listed-action` | `Alacritty.desktop $ROOT/home/.local/share/applications/Alacritty.desktop` | `Alacritty.desktop:New $ROOT/home/.local/share/applications/Alacritty.desktop:New alacritty --new` |
| F13 | `unlisted-action` | `Alacritty.desktop $ROOT/home/.local/share/applications/Alacritty.desktop` | <rc1> |
| F13 | `action-group-before-actions` | `Alacritty.desktop $ROOT/home/.local/share/applications/Alacritty.desktop` | <rc1> |
| F13 | `action-header-suffix` | `Alacritty.desktop $ROOT/home/.local/share/applications/Alacritty.desktop` | `alacritty --new` |
| F14 | `unclosed-quote` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | `Alacritty.desktop $ROOT/home/.local/share/applications/Alacritty.desktop alacritty unclosed` |
| F14 | `field-bad` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | `<entry content: 5 lines>` |
| F14 | `field-double-fu` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | `<entry content: 5 lines>` |
| F14 | `field-escaped` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | `Alacritty.desktop $ROOT/home/.local/share/applications/Alacritty.desktop alacritty 100%` |
| F14 | `empty-exec` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | <rc1> |
| F15 | `exclude-then-list` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | Foot.desktop (…/applications/Foot.desktop) → foot |
| F16 | `explicit` | <rc1> | Foot.desktop (…/applications/Foot.desktop) → foot |
| F17 | `list-reversed` | ZZZ.desktop (…/applications/ZZZ.desktop) → alacritty | AAA.desktop (…/applications/AAA.desktop) → foot |
| F18 | `cmd-only` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | `alacritty` |
| F18 | `delim-pipe` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | `Alacritty.desktop\|$ROOT/home/.local/share/applications/Alacritty.desktop` |
| F18 | `cmd-delim-comma` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | `alacritty` |
| F18 | `id-only` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | `Alacritty.desktop` |
| F18 | `content` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | `<entry content: 6 lines>` |
| F19 | `strict` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | <rc1> |
| F20 | `tryexec-missing` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | <rc1> |
| F20 | `exec-not-path` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | <rc1> |
| F20 | `exec-absolute` | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty | <rc1> |
| F21 | `uppercase-ext` | Ok.desktop (…/applications/Ok.desktop) → alacritty | <rc1> |
| F21 | `space-in-name` | Ok.desktop (…/applications/Ok.desktop) → alacritty | <rc1> |
| F21 | `leading-dot` | Ok.desktop (…/applications/Ok.desktop) → alacritty | <rc1> |
| F21 | `no-ext` | Ok.desktop (…/applications/Ok.desktop) → alacritty | <rc1> |
| F22 | `joined-reversed` | Foot.desktop (…/applications/Foot.desktop) → foot | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty |
| F23 | `both-lists` | Foot.desktop (…/applications/Foot.desktop) → foot | Alacritty.desktop (…/applications/Alacritty.desktop) → alacritty |

## 7. Harness hazards for the C1 judge and for the tool's own selftest

1. **Never let a fixture depend on readdir order** (F-09). Two valid entries in the same
   applications directory make `expect` a function of file creation order and filesystem type. Either
   put at most one valid candidate per applications dir, or make the fixture write files in a fixed,
   documented order and state the assumption.
2. **`stderr` is not in the C1 contract, but the shell's diagnostics leak absolute paths** (F-10,
   F-13). Compare stdout + exit status only; do not assert on stderr.
3. **`--print-id`/`--print-path`/`--print-content` never touch the cache** (F-15). Only `--print-cmd`
   writes it, and it does so in a backgrounded subshell. A tool that models "cold cache" is right for
   all modes; a *fixture harness* that reuses one `XDG_CACHE_HOME` across runs would see a different
   code path for `--print-cmd` only.
4. **`/./` and empty path elements** (F-16, F-21) are the two ways to get a surprising `--print-path`;
   both are cheap adversarial fixtures for the tool.
5. **A single failing line must not be treated as ignorable** (F-03, F-11): the script fails *open* on
   `Exec` tokenizing but fails *closed* on a second bad `Categories`/`Exec` line.

## 8. Limits of this seat's evidence

- No bare invocation was ever run (it would launch a terminal); the launch half (`exec "$@"`, :1499) is
  inferred from source only.
- The cache *hit* path was exercised only for existence (`receipts/cache.tsv`), not for correctness of
  a warm cache; the C1 contract models a cold cache anyway.
- No non-UTF-8 bytes, no very large trees (>2 entries/dir), no NFS/overlay readdir-order variation,
  no `XDG_CURRENT_DESKTOP` values containing `/` or spaces.
- `XTE_DEBUG=1` was used only to *observe* path expansion; it changes stderr, never stdout.
- Random trees are one seed (`--seed 20261026`); 600 of them produced 71 outcome classes.

## 9. Reproduce

```
S=/fast/scratch/hyaku/mado-r47/ExecRefCompare; mkdir -p "$S"
python3 <seat>/fuzz.py  run  --work "$S" --out "$S/out" --random 600
python3 <seat>/probe.py       --work "$S" --out "$S/probes"
python3 <seat>/fuzz.py  case "$S/probes/P01-hidden-shadow.json" --work "$S"
python3 <seat>/verify_findings.py --receipts <seat>/receipts
```
