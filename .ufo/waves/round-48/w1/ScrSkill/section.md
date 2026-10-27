## XKB keymap compile (round 48)

`xkbcli compile-keymap --layout <L> --variant <V> --options <O> --rules <R> --model <M>` compiles the five RMLVO names
this host's config carries (`kb_layout = br`, `kb_options = compose:caps` at `~/.config/hypr/input.conf:10-11`) into a
keymap on stdout and returns the compile's own status. It needs no display — measured rc 0 with `DISPLAY`,
`WAYLAND_DISPLAY` and `XDG_SESSION_TYPE` unset — so it separates a keymap failure from a compositor, an error overlay
or a stale device dump, and it touches neither the compositor nor an input device. What it does not reproduce is the
compositor's own call: that a failed compile leaves Hyprland with layout `us` and four empty names is the held rule
from round 46 (step 4, `corpus/knowledge/hyprland-input-devices-r46.md`; rows S318/S319 in `corpus/SOURCES.md`), cited
here, never re-claimed. The compile itself was the open half of that entry (its Limits,
`hyprland-input-devices-r46.md:69`) and of `corpus/README.md:112`; ground now
`corpus/knowledge/xkb-keymap-compile-r48.md` (rows S340..) <AFTER: the landed entry and its row numbers>.

Host matrix (libxkbcommon 1.13.2-1, xkeyboard-config 2.48-1; receipt
`.ufo/waves/round-48/w1/ScrSkill/receipts/xkbcli-matrix.txt` — `compile-keymap` and `list` are read verbs, stdout
only):

| names | rc | stderr | keymap |
|---|---|---|---|
| `--layout br --options compose:caps` (the host's) | 0 | — | 73079 B |
| `--layout br` | 0 | — | 73043 B |
| `--layout zz` | 1 | `[XKB-338] Couldn't find file "symbols/zz" in include paths`, then the include-path list | empty |
| `--layout br,zz` | 1 | the same — one unknown name fails the whole list | empty |
| `--layout br --variant nope` | 1 | `[XKB-661] Couldn't process include statement for 'br(nope)'`, `Failed to compile xkb_symbols` | empty |
| `--rules nope --layout br` | 1 | `[XKB-338] Couldn't find file "rules/nope" in include paths` | empty |
| `--layout br --options nope` | 0 | `[XKB-595] Unrecognized RMLVO option "nope" was ignored` | 73043 B, md5 = `--layout br`'s |
| `--layout br --options compose:caps,nope` | 0 | the same warning for `"nope"` | 73079 B, md5 = the host run's |
| `--layout br --model nope` | 0 | *nothing* | 73043 B, md5 = `--layout br`'s |
| `--layout br,dk` | 0 | — | 78029 B |
| `--layout us,dk --variant intl` | 0 | — | 77943 B (the variant reaches `us` only) |
| `--layout us,dk --variant ,winkeys` | 0 | — | 76323 B (the empty slot leaves `us` plain) |
| `--layout us,dk,br --variant intl,winkeys` | 0 | — | 82427 B |
| `--layout br --variant intl,nope` | 1 | `Less layouts than variants: "br" vs. "intl,nope".`, then the include failure | empty |

Include paths, as the compiler names them in its own `XKB-338` error on this host: one searched,
`/usr/share/xkeyboard-config-2`; three "could not be added", `/home/vgpnk/.config/xkb`, `/home/vgpnk/.xkb`,
`/etc/xkb`. The error prints the one path it searched and the three it could not add, in that order: [INF] the user
paths come before the xkeyboard-config root, and a path that does not exist is skipped, not an error. <AFTER: the libxkbcommon line that fixes the
order and the prefixes, from the w1 source seat>

    # the host's names off-compositor; stdout is the keymap, stderr the messages above
    $ xkbcli compile-keymap --layout br --options compose:caps >/dev/null; echo rc=$?
    rc=0
    $ xkbcli compile-keymap --layout br --variant nope >/dev/null; echo rc=$?
    rc=1
    # the name catalogue the checks below read: models first, then layouts (one row per layout+variant)
    $ xkbcli list | grep -c "layout: 'br'"
    9

| symptom | first read | the rule behind it | next step |
|---|---|---|---|
| a keyboard prints `us` and four empty names although the config names something else | the round-46 join's `FALLBACK` verdict (`SKILL.md:2128`), then the same names through `compile-keymap` | either the names never reached the keyboard (the global default is `us`, S318) or they reached it and no keymap resulted, which resets them to `us` with the rest empty (S319) — a reset shape, not proof of a cause | `compile-keymap` on the *expected* names: rc 0 leaves the compile innocent — read `hyprctl getoption input:kb_layout -j` and the config chain instead; rc 1 reads the failing component in the matrix above |
| a layout name does nothing, or the keyboard falls back | stderr: `Couldn't find file "symbols/<name>" in include paths` plus the path list | a layout is a `symbols/<name>` file resolved through the include paths; a missing one is an error and takes the whole compile with it, including a bad second name in a list | take the name from the catalogue: `xkbcli list` prints `models:` then `layouts:`, one row per layout+variant — `br` has 9 rows (base row `variant: ''`, then `nodeadkeys`, `dvorak`, `nativo`, `nativo-us`, `thinkpad`, `thinkpad_nodeadkeys`, `nativo-epo`, `rus`), `zz` has none |
| a variant is ignored, or the keyboard falls back | stderr: `Couldn't process include statement for '<layout>(<variant>)'` | the variant is the parenthesised part of the include `layout(variant)`; a name the symbols file does not carry fails the compile (rc 1) — it is not dropped | take the variant from that layout's own rows (`intl` is not a `br` variant; `us` has it), and keep the list aligned — see the last row |
| an option is silently ignored | stderr: `[XKB-595] Unrecognized RMLVO option "<name>" was ignored` | unknown options are dropped with a warning and the compile still succeeds (rc 0, keymap written); a valid option in the same list still applies — `compose:caps,nope` produced the host keymap byte for byte | read the warning as the verdict: the round-46 join compares names only, so it can print AGREE while an option is dropped; fix the spelling — `xkbcli list` has no options section, so the warning is the only catalogue <AFTER: whether 2.48 ships an options listing> |
| a model name changes nothing, or "works" | the keymap stdout | an unknown model is accepted in silence: `--layout br --model nope` exited 0 with no stderr and a keymap identical to `--layout br` (md5 `f73b560f90bbfbe2169e1c946a967dbf`) | do not read rc 0 as "the model exists"; check the name against the `models:` rows of `xkbcli list`, or compare the stdout |
| a layout placed in `~/.config/xkb` has no effect | the include-path list from a deliberately failing compile (`--layout zz`) | the user paths are searched before the system root, but all three were absent on this host, so a file there is read only when the same path the compiler names exists — `$XDG_CONFIG_HOME/xkb` when `XDG_CONFIG_HOME` is set to `~/.config`, `$HOME/.xkb` otherwise | make one compile fail on purpose and read the paths it names; then check the file sits under a `symbols/` subdirectory of exactly that path <AFTER: the libxkbcommon prefix rules> |
| a layout list and a variant list of another length misbehave | both lists as written in `kb_layout` / `kb_variant` | variants align with layouts by position: a short list leaves the trailing layouts without a variant (rc 0, `us,dk` + `intl` = 77943 B), a longer list is an error (`Less layouts than variants`) and the compile exits 1; with the lists equal in length the compile still fails if any pair names a variant that layout lacks (`br(intl)`) | write one slot per layout and an empty slot where a layout has none (`us,dk` + `,winkeys`) |

Notes: the compile is silent about the model and loud about layouts, variants, rules and options — a clean rc 0 says
"these names produced a keymap", not "these names exist". Hyprland compiles from the names itself, so the stdout is
[INF] a comparison handle and not an installed file: two runs are comparable by `md5sum`, and a keymap that differs
only in options differs only where those options act. This check is about names, not behaviour: whether a composed key
produces the expected symbol is out of scope, as are `kb_file` (which bypasses the names entirely, round-46 step 4)
and per-device blocks (round-46 step 3). The receipt holds file paths only — no session material, no device names —
and nothing here starts a compositor or an input device. The matrix is pinned to libxkbcommon 1.13.2-1 and
xkeyboard-config 2.48-1: re-verify both before reusing a row.


## Terminal cache (round 48)

The resolver caches its whole answer in `$XDG_CACHE_HOME/xdg-terminal-exec` (default `$HOME/.cache/xdg-terminal-exec`,
`xdg-terminal-exec:172-173`) and reads that file **before** any list or entry: `read_cache` gates everything at
`:1179`, and the cold branch that builds the entry lists and calls `find_entry` sits inside its `else` (`:1183-1209`)
— on a hit no `.list` file and no desktop entry is opened at all. The file holds ten lines (hash, executable, entry
path, entry id, action, then the five argument names) and an exec line terminated by `0x1e` + `END_OF_EXEC_USEP`
(`:247-251`, written at `:332`). It is trusted only while line 1 still equals the md5 of `4`, `$XDG_CURRENT_DESKTOP`
and `LANG=C ls -LRl` of the colon-joined list and data paths (`:194-201`) **and** `command -v <line 2>` succeeds
(`:274`). Only a run that reaches `:1455` saves it: the early bail-out at `:1368-1376` sends a run that asks for `id`,
`path` or `content` without `cmd` home before that point, so a `--print-id` capture rewrites nothing while
`--print-cmd`, `--test` or a launch does — and the save is forked off in the background (`save_cache "$1" &`,
`:1457`).

So SUPER+RETURN (`~/.config/hypr/bindings.conf:2`, `uwsm-app -- xdg-terminal-exec
--dir="$(omarchy-cmd-terminal-cwd)"`) can start a command the current files no longer name, in three shapes the hash
cannot see: an entry edited in place inside the same size and the same minute (the `ls` listing keeps mode, nlink,
owner/group, size, date-to-the-minute and name), an entry whose `X-TerminalArg*` keys changed (the cached *option
names* are reused; only the `--dir` value is composed over them at print time, `:1400-1409`), and a removed `TryExec`
stub behind an `exec[0]` that still resolves (`read_cache` re-checks `command -v` on line 2 and nothing else). A run
that *used* the cache never rewrites it — the save sits behind `if [ "$XTE__CACHE_USED" = "false" ]` (`:1455`) — so
repeating the hotkey cannot repair a stale answer; only a run that had to compute one writes the file. The cache is
invalidated by anything that changes the listing — size, mode, name, directory, a new or removed file, or a different
`XDG_CURRENT_DESKTOP` — and by a malformed file: the parse abandons it on reaching its 50th line
(`xte__line_limit=50`, `:223` — at most 49 lines count) or when the `0x1e` terminator is missing. Disabling is
`XTE_CACHE_ENABLED=false` in the environment (`:1172`) or a `/disable_cache` line in a list file (`:380`); either
counts as the configured flag, and the first one seen wins.

Read it with `tools/mado-terminal.py explain`: the extended tool (round 48) reports the cache verdict in its
`MADO_TERM:` line as `cache=<absent|hit|stale|invalid|disabled>` and `print` reproduces the resolver's stdout and exit
status with a warm cache as with a cold one <AFTER: landed field spelling, the tool's selftest
count, and the warm-case receipts>. The round-47 tool models the cold path only and says whether a cache file exists
(`tools/mado-terminal.py:82-85`); it writes nothing, so it can report a stale cache but never repair one. Comparing
warm against cold stays read-only: point `XDG_CACHE_HOME` at a throwaway directory, keep to `--print-*`, and diff the
two answers.

    # the two answers, read-only: the environment's cache against a cold one
    $ python3 tools/mado-terminal.py explain            # MADO_TERM: ... cache=hit ...
    $ XDG_CACHE_HOME=$(mktemp -d) xdg-terminal-exec --print-id --print-cmd > cold.observed
    $ python3 tools/mado-terminal.py explain --observed cold.observed

| symptom | first read | the rule behind it | next step |
|---|---|---|---|
| SUPER+RETURN starts a command the list no longer names | `explain`'s `cache=` and the cached entry path and id | the cache answers before any list or entry is read (`:1179`) and is trusted while the hash matches and line 2 resolves (`:274`) | a cold run answers from the files: `XDG_CACHE_HOME=$(mktemp -d) xdg-terminal-exec --print-id --print-cmd`, then `explain --observed` on that capture |
| an edit to an entry or a list line has no effect | the edited file's size and mtime minute, then the cache's first line | the hash covers `LANG=C ls -LRl`: mode, nlink, owner and group as `ls` prints them, size, date to the minute and the name — never the content (`:194-201`) | a cold run shows the new answer; the cache catches up only when the listing changes. Clearing the file is operator-owned (below) |
| a removed `TryExec` stub does not drop the entry, or a changed `Exec` does not take effect | cache line 2 (the executable) and the cached exec line | on a hit only `command -v` line 2 is re-evaluated (`:274`); `TryExec`, `Exec`, `Categories`, `Hidden` and `Actions` are not re-read because no entry is opened | a cold run is the validation answer: it drops the candidate the cache keeps |
| a changed `X-TerminalArgDir` / `-Title` / `-Exec` key in the entry is ignored | the entry's `X-TerminalArg*` keys and the cache's lines 6-10 | the cache stores the resolved option *names*; the run adds the current `--dir`/`--title`/`--app-id` value over them (`:1400-1409`), so the value is fresh and the option is not | compare with a cold run before editing the entry again; the entry's key takes effect when the listing changes |
| `cache=stale` | `explain`'s `MADO_TERM:` line, then the file that changed | stale means the hash no longer matches — a listing change, a mtime minute, a different desktop — and is normal after any edit; the next run that reaches `:1455` rewrites it | nothing to fix: confirm with a cold run that the answer is the one you want, then let the resolver save it |
| `cache=invalid` | the cache's line count and the end of its exec line | the parse gives up at the 50th line (`:223`) and requires the `0x1e` + `END_OF_EXEC_USEP` terminator (`:247-251`); a truncated or hand-written file is ignored, not repaired | a cold run overwrites it from scratch; do not hand-edit the file |
| `cache=disabled` while you expected a hit | the environment, then each list file | `XTE_CACHE_ENABLED=false` (`:1172`) and a `/disable_cache` line (`:380`) both disable it, the first configured value wins, and a cold run that reaches the save *removes* the file (`:337`) | expect a cold answer on every run: read the lists, not the cache |
| the tool's answer and the hotkey's answer differ | the argv and the environment: the hotkey adds `uwsm-app --` and `--dir="$(omarchy-cmd-terminal-cwd)"` (`~/.config/hypr/bindings.conf:2`) | the tool models the resolver's argv and files, not the wrapper's environment | pass the same `--dir` value and the same `XDG_*` values to the tool; a difference that survives that is the round-47 `DIFFER` reading, not a new rule |

Notes: the cache file is `umask 077`, so it is a user-only file, and it is a record of one past answer, not a rule —
reading it is a capture, not a selection. Clearing or deleting `~/.cache/xdg-terminal-exec` is operator-owned and
outside this lane's write surface: the lane reads that path, never writes, never deletes, and points `XDG_CACHE_HOME`
at a throwaway directory for every capture (a cold `--print-cmd` run rewrites the cache wherever `XDG_CACHE_HOME`
points, and the save is forked — [INF] a second run can therefore read the file while it is being written). This section supersedes
the round-47 row "a change has no effect" (`SKILL.md:2213`), which described the cold-only tool. HOME unset is a
modelled branch of the extended tool, as the pin does it (round-47 closure D1: exit 1, empty stdout), so the cache
verdict is not read on that path <AFTER: the landed D1 lesson line>. Ground:
`corpus/knowledge/xdg-terminal-selection-r47.md` (rows S326..) plus the warm-cache rows <AFTER: S-numbers>; locators
in `.ufo/waves/round-48/w1/ScrSkill/receipts/resolver-cache-locators.txt`.