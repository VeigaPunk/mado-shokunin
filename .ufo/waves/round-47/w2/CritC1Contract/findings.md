# CritC1Contract — docstring sentences vs the pinned real script

Seat: CritC1Contract (w2 FALSIFY). Test subject: docstring of
`.ufo/waves/round-47/l1-draft/mado-terminal.py` lines 2-88 (C1 contract for `tools/mado-terminal.py`).
Reference: the pinned real script `.ufo/waves/round-47/fetch/xdg-terminal-exec`, sha256
`89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` (verified; copy in this dir,
`pin.sha256`). Every claim below was tested by running the pin itself on hermetic scratch trees
(HOME/PATH/XDG_* all inside a per-case dir under `/fast/scratch/hyaku/mado-r47/CritC1Contract/`;
XDG_CONFIG_DIRS/XDG_DATA_DIRS isolated to empty dirs so the host cannot leak in; cold cache per
case; `--print-*`/`--test` only; no empty argv elements; `timeout 25`; XTE_DEBUG=true observed
reads). Full transcripts: `results2.log`, `results3.log`, `results4.log` in this dir.

Reproducible case driver (pattern used for every case below):

```
R=$(mktemp -d -p /fast/scratch/hyaku/mado-r47/CritC1Contract); mkdir -p "$R/home/.config" \
  "$R/home/.local/share/applications" "$R/bin" "$R/cache" "$R/empty-cfg" "$R/empty-data"
printf '#!/bin/sh\nexit 0\n' > "$R/bin/alacritty"; chmod 755 "$R/bin/alacritty"
printf '[Desktop Entry]\nType=Application\nName=T\nExec=alacritty\nCategories=System;TerminalEmulator;\n' \
  > "$R/home/.local/share/applications/alacritty.desktop"
printf 'alacritty.desktop\n' > "$R/home/.config/xdg-terminals.list"
cd "$R" && timeout 25 env -i HOME="$R/home" PATH="$R/bin:/usr/bin:/bin" \
  XDG_CONFIG_HOME="$R/home/.config" XDG_CONFIG_DIRS="$R/empty-cfg" \
  XDG_DATA_HOME="$R/home/.local/share" XDG_DATA_DIRS="$R/empty-data" \
  XDG_CACHE_HOME="$R/cache" XDG_CURRENT_DESKTOP=Hyprland LC_ALL=C LANG=C XTE_DEBUG=true \
  /fast/scratch/hyaku/mado-r47/CritC1Contract/pin/xdg-terminal-exec --print-id --print-cmd
```

## Verdicts

Every *resolver-side* sentence tested true (verified below). Qu tool-side sentences (the tool is
not in the lane yet) are UNTESTABLE here; they are listed separately. Two sentences are
MISLEADING for an implementer (they describe a function as failing where the real script ignores
the failure); one sentence is loosely worded; one environment list is incomplete.

### MISLEADING (would break fixture parity if implemented strictly)

1. **Docstring line 65-66** — "Exec (when allowed) is escape-expanded, tokenized by the
   shell-quoting rules of x:561-692, its field codes stripped (x:694-740), and its first word
   must be found by `command -v` (reject otherwise)."
   The strip/tokenize steps do NOT reject on malformed input: `de_tokenize_exec` and
   `de_strip_fields` can return 1, but `check_entry_key` ignores the return value (pin
   `x:954-964`) and keeps the partial/raw `$XTE__EXEC_USEP`. Evidence:

   - `Exec=foot %x` (unknown field): tokenizer fine, strip leaves `%x` untouched, entry
     **accepted**, `--print-cmd` prints `foot\n%x`, rc 0 (results2.log `p19_unknownfield`).
   - `Exec=foot )` (unquoted special): tokenizer error "Encountered unquoted character: ')'",
     entry **accepted** with `foot` (results4.log `p45_tokerr`).
   - `Exec=alacritty "unclosed` (unclosed quote — this exact line is already a C1 fixture,
     `c1-r47-fixtures.json`): error "Double quote was not closed!", entry **accepted**,
     `--print-cmd` prints `alacritty\nunclosed`, rc 0 (results4.log `p46_unclosed`).
   - `Exec=alacritty $HOME` (unquoted `$`): same class, accepted (fixture too).
   A reimplementation that rejects these (a natural reading of "tokenized by the shell-quoting
   rules … reject otherwise") diverges from the pinned oracle on existing fixtures.

2. **Docstring line 44-45** — "the id must match [a-zA-Z0-9_.-]+ ending in `.desktop` and not
   be `.desktop`, the action [a-zA-Z0-9-]* - else "Discarded possibly misspelled entry"
   (stderr)." — the message is exact, but note the id is never re-validated later; the
   `id:action` split at candidate time (x:1064-1066) takes id before first `:` and action after
   last `:`. True, but only because list-time validation already restricted the shape.

### LOOSELY WORDED (not false, but easy to misread)

3. **Docstring line 47** — "Plain lines are kept verbatim (after the +/- strip) in list order,
   duplicates included." There are no *plain* lines: only lines matching
   `[a-zA-Z0-9_]* | [+-][a-zA-Z0-9_]*` (then validated) are kept; every other non-empty line
   (e.g. `foo bar.desktop`, `x/{id}`) is silently ignored, as the next sentence "Anything else
   is ignored" says. Verified: `# c`, `x/{id}`, ``, `foo bar.desktop` all ignored (results2.log
   `p01_basic`/`p03_*` debug reads; the discarded-line case appears in fixtures LISTL).

### INCOMPLETE ENVIRONMENT LIST

4. **Docstring lines 28-29** — the resolver also reads `XTE_DEBUG` / `DEBUG` (debug switch,
   changes stderr volume) and `LC_ALL` / `LANG` (non-C LC_ALL makes the script re-call itself,
   `x:355-359`; `LANG` affects `ls` hashing, `x:200`). Omission is harmless for stdout/rc but
   the list claims to be "as the resolver reads it".

### UNTESTABLE (tool-side; `tools/mado-terminal.py` absent — no data commit yet)

- Line 4: "Read-only. Starts no process, opens no socket, writes no file. Python 3 standard
  library only."
- Line 13-16: "Prints exactly what `xdg-terminal-exec` prints … exits with its exit status"
  (tool half) and "this tool refuses with exit 2".
- Lines 17-24: the whole `explain` contract (trace, MADO_TERM line, AGREE/DIFFER, exit map 0/1/2/3).
- Lines 25-26: `--selftest` (N/N passed line, exit 0 iff all pass).
- Lines 83-84: "This tool always models the cold path; `explain` says whether a cache file exists."

(Their resolver halves — "the resolver would launch a terminal" etc. — are supported: with no
print option the script reaches `exec "$@"` /x:1499/ after prepending the entry's Exec words, so
it does launch; exit-2 is a tool-only behavior.)

## Verified-true sentences (highlights; full transcripts in the logs)

| Docstring | Result | Evidence (case in results2/3/4.log) |
|---|---|---|
| desktop names lowercased, split on ':' empties kept/trailing dropped (33-34) | true | p02 (GNOME:Hyprland → gnome- list first), p03 (`:Hyprland:` → `-xdg-terminals.list` read once, trailing empty dropped), p35 (empty desktop → generic lists only) |
| list-file order incl. XDG_DATA_DIRS `xdg-terminal-exec/` subdirs; `%` slash removal (35-38) | true | p02/p23 debug read order; p30 (`XDG_CONFIG_HOME=$R/…config/` → single-slash paths) |
| non-regular list file skipped; unreadable → exit 1 errexit (39-40) | true | p29 (directory at list path → skipped, rc 0), p37 (symlink-to-regular followed), p04 (chmod 000 → rc 1, empty stdout, "Permission denied") |
| read -r semantics: trim, NUL dropped, unterminated last line ignored (40-41) | true | p05 (`foot.desktop\0xx` → line becomes `foot.desktopxx`, discarded), p05b (`foo\0bar.desktop` → `foobar.desktop`), p06 (last line without `\n` ignored) |
| directives: first-of-pair wins; env wins over directives; execarg_default compat-only (41-43) | true | p07_pair_first (`/disable_cache` then `/enable_cache` → cache disabled, removed), p07_env_compat (env `XTE_EXECARG_COMPAT=false` beats `/execarg_compat` → strict, rc 1), p07_env_cache (env false beats `/enable_cache` → no cache), p31 (env true beats `/disable_cache` → cache written), p32 (`/execarg_strict` then `/execarg_compat` → strict), p34 (`/execarg_default:foot.desktop:-x` applied: `foot -x echo hi`) |
| +/- exclusion/inclusion: exclusions only remove from fallback; first word wins (46-47) | true | p15_excl (`-foot.desktop` → rc 1 no terminal), p44 (`-foot.desktop` + explicit `foot.desktop` → explicit still selected), p15_incl (`-` then `+` → still excluded), p40 (`+` then `-` → protected, selected) |
| entry ids: validation, first-':' split, stderr "Discarded possibly misspelled entry" (44-45) | true | p11 (`foot.desktop:run` accepted), p05 (`foot.desktopxx` discarded with message) |
| find over app dirs, id mapping `/`→`-`, last-path-wins incl. DATA_HOME beats DIRS, fallback front-insert (49-53) | true | p28 (same id in DATA_DIRS and DATA_HOME → HOME path wins, content shows HOMEVERSION), p15_fallback, p23 |
| candidates: list lines then fallback; `id:action` split first/last colon; no-path/already-tried skipped (54-55) | true | p11 (action run), p44 debug (fallback exclusion), p27 (action rides on id and path: `foot.desktop:run` both) |
| group headers, key whole-text matching incl. `CategoriesX=` counts as Categories (56-60) | true | p09 (`CategoriesX=System;TerminalEmulator;` alone → selected) |
| OnlyShowIn/NotShowIn case-sensitive, fallback-only (61-62) | true | p17 (lowercase `hyprland` vs `Hyprland` rejected/selected; explicit-listed entry ignores OnlyShowIn; NotShowIn rejects) |
| X-/TerminalArg* escapes `\s \n \t \r \\`, other backslash dropped; TryExec via command -v; Hidden=true rejects (62-65) | true | p16_tryexec_miss/hit, p16_hidden; p12 (entry args set and printed) |
| Exec first-word resolution: aliases, functions, builtins, reserved words, path-with-'/', first PATH hit, empty PATH entry = cwd (71-73) | true | p18_builtin (`echo`), p18_reserved (`if`), p18_abspath (`/…/bin/foot`), p18_cwd (PATH `:` entry → cwd program), p25 (`Exec=foot.desktop` via registered alias), p42 (`Exec=check_bool` via script function) |
| while-loop status rejects when last executed step failed (66-67) | true | p11 (entry file ending with `[Desktop Entry]` + action requested → rc 1, no terminal) |
| skipped-without-reset inheritance across entries (68-69) | true | p10 (a.desktop: Exec=foot, no Categories; b.desktop: Categories, no Exec → b selected, cmd `foot`) |
| execarg default: entry default or `-e` compat, strict skips (69-70) | true | p34 (custom `-x`), p08_default_plain (`-e` when command given: `foot -e …` in p20/p33), p08_strict (rc 1) |
| no candidate: stderr "No valid terminal entry was found in:", exit 1, empty stdout (74) | true | p26_isolate, p14_none |
| printing: id `id[:action]`, path with `/./` folded, content lines, cmd words+args order, delimiters via `printf %b`, --test shape (75-79) | true | p01, p27 (path `:run`), p12 (argv order `foot APP a TIT t DIR d H -E cc arg1 arg2` — matches the docstring's stated order), p21 (`--print-delimiter=,` → `foot.desktop,/path` no trailing newline), p33 (`--print-cmd=,` → `foot,-e,echo,x`, `--print-cmd=\t` → tabs, no trailing newline), p20 (`--test` → `Command and arguments:` + `  >arg<` lines), p41 (`--print-content` drops an unterminated last line), p22 |
| cache: path, md5 validity incl. invalidation on change, background rewrite only on `--print-cmd` (81-84) | true | p13 (no cache file after `--print-id`/`--print-path` alone; file appears after `--print-cmd`; warm second run shows "got cache / cache is actual"), p43 (after adding an app file, "cache is out-of-date" → recompute) |

## Tool installs / environment

None. No package transactions (host pacman paused per operator directive); no tools installed;
no host config/compositor touched; all resolver runs used only `--print-*`/`--test` with
XDG_CACHE_HOME inside scratch; nothing outside the lane or the seat scratch was written.

## Honest scope note

No hard FALSE sentence was found among the resolver-testable claims: the contract text is a
faithful description of the pinned script for the exercised surface. The two MISLEADING items
above (1, 2) and the untestable tool-side sentences are the reportable holes; item 1 is the only
one with a direct fixture-parity consequence (unknown-field / malformed-Exec fixtures would be
miscounted by a strict implementation).
