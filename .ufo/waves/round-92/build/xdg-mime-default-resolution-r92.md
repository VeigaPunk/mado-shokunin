source: S508 (provisional id; upstream xdg-utils v1.2.1 `scripts/xdg-mime.in` sha256 11e7d91e…b95c7e and `scripts/xdg-utils-common.in` 1f6969b5…9cc532, https://gitlab.freedesktop.org/xdg/xdg-utils/-/raw/v1.2.1/scripts/<file>), S509 (provisional id; upstream `scripts/xdg-open.in` a6b0c7af…80790b plus the installed host package xdg-utils 1.2.1-2, `/usr/bin/xdg-mime` sha256 a587107f…615f3f). Provisional ids and digests: the L1 binds them in SOURCES.md at the round-92 freeze. No S490: this entry makes no claim about exit status as evidence of a termination cause.
covers: what `xdg-mime query default TYPE` prints — the session dispatch that picks `defapp_generic`, the mimeapps-list search, `desktop_file_to_binary`, the `defaults.list`/`mimeinfo.cache` grep fallback, the `MimeType` scan with `InitialPreference`, and where each answer differs from the GLib answer of `corpus/knowledge/mime-default-resolution-r91.md`
verified-at: 2026-11-06 — the candidate `.ufo/waves/round-92/build/mado-xdgmime.c1.py` (sha256 4121d583…a8bd) replayed against the 128 frozen L1 cases (131 type rows) agrees with the installed `/usr/bin/xdg-mime` label on every row: `DRAFT_TOOL_CHECK rows=131 mismatches=0` (DRAFT run, `.ufo/waves/round-92/w1/R92MScribeEntry-draft-check.txt`; the measured receipt is the round-92 C1 counter, not this run)
recheck: 90d — re-pull the three files at the next xdg-utils tag that changes xdg-mime.in, xdg-utils-common.in or xdg-open.in; also when `xdg-utils` leaves 1.2.1-2, `bash` leaves 5.3.20-1, `grep` leaves 3.12-2, `gawk` leaves 5.4.1-1 or `coreutils` leaves 9.12-2.

# xdg-utils 1.2.1 `xdg-mime query default`: the resolver `xdg-open` uses on an unrecognised desktop

This entry states how xdg-utils 1.2.1 answers "which `.desktop` file opens this MIME type" through
`xdg-mime query default TYPE` — the question `xdg-open` asks on a session whose desktop it does not
recognise (Hyprland, sway, i3, …). Line numbers are those of tag v1.2.1: `xdg-mime.in`, `xdg-open.in`
and `xdg-utils-common.in` (`common:` below). Behaviour that depends only on the shell is cited by the
labelled L1 case that measures it, in `.ufo/waves/round-92/controls/xdgmime-cases-r92-l1.json`
(`case m09`), where the label is the installed `/usr/bin/xdg-mime`'s own stdout and exit status.

The cited line numbers are the tag's `.in` files. The installed `/usr/bin/xdg-mime` (1794 lines, sha256
a587107f…) is the build product: `xdg-utils-common.in` is inlined and `@NAME@` is substituted, so its line
numbers differ. Every function this entry cites is byte-identical between the two —
`defapp_generic`, `check_mimeapps_list`, `defapp_fallback`, `defapp_kde`, `defapp_lxqt`,
`search_desktop_file`, `desktop_file_to_binary`, `detectDE`, `first_word`, `has_display`, `xdg_realpath`,
`exit_success` — as checked function-block by function-block on 2026-11-06 (only `exit_failure_syntax`'s
`@NAME@` strings differ). So the labels come from bytes whose code is the code cited here.

Scope: *resolution* only — which id is printed. Out of scope: whether the named application starts,
`xdg-open`'s launch (`search_desktop_file` at xdg-open.in:312-390), D-Bus/portal activation, and MIME
sniffing (`query filetype`, xdg-mime.in:577-591), which this entry does not model.

## 1. Who asks, and which desktops reach the question

`xdg-open` runs `detectDE` (xdg-open.in:593), and an empty result becomes `generic` (xdg-open.in:595-597).
Only `generic` reaches `open_generic` (xdg-open.in:664-665). `open_generic` asks xdg-mime twice:

- a file path: `xdg-mime query filetype FILE` to get the type (xdg-open.in:486), then
  `open_generic_xdg_mime` (xdg-open.in:489), which runs `default="$(xdg-mime query default "$filetype")"`
  (xdg-open.in:392-395) and stops when that is empty (:396);
- a URL: `open_generic_xdg_x_scheme_handler` (xdg-open.in:507-508) builds `x-scheme-handler/<scheme>`
  from the scheme's leading `[[:alpha:]][[:alnum:]+.-]*` run (:414-417) and calls the same function (:419).

Both calls need a display: `has_display` is true only when `DISPLAY` or `WAYLAND_DISPLAY` is non-empty
(xdg-open.in:485, :507; common:400-407). `xdg-mime` is invoked by bare name, so it is whatever `PATH`
provides (:395).

Which sessions are `generic` (common:278-378): `XDG_CURRENT_DESKTOP` maps through a fixed case —
`Cinnamon|X-Cinnamon`→cinnamon, `ENLIGHTENMENT`→enlightenment, `GNOME*`→gnome, `KDE`→kde,
`DEEPIN|Deepin|deepin`→deepin, `LXDE`→lxde, `LXQt`→lxqt, `MATE`→mate, `XFCE`→xfce, `X-Generic`→generic
(common:283-317). **Anything else** — `Hyprland`, `sway`, `i3`, `niri` — leaves `DE` empty (:318), and then
the classic fallbacks run in order: `KDE_FULL_SESSION`, `GNOME_DESKTOP_SESSION_ID`, `MATE_DESKTOP_SESSION_ID`,
a `dbus-send` name-owner probe for `org.gnome.SessionManager`, two `xprop` probes for xfce, `$DESKTOP`
starting `Enlightenment`, `LXQT_SESSION_CONFIG` (common:321-332); then `$DESKTOP_SESSION` in a small case
(:334-350); then `uname` for cygwin/darwin/wsl (:352-367); then gnome→gnome3 when
`gnome-default-applications-properties` is absent (:369-373); and finally `$XDG_RUNTIME_DIR/flatpak-info`
overrides everything to `flatpak` (:375-377). With none of those, `DE` stays empty and xdg-open sets
`generic` (:595-597). The other `open_*` functions also fall back into `open_generic` when their own tool
is missing or fails: open_deepin :177, open_gnome3 :194, open_gnome :213, open_mate :232, open_xfce :251,
open_enlightenment :266, open_lxde :543 — so a GNOME or XFCE session whose tool is absent asks the same
question. `case s02` fixes the xdg-mime side of that boundary: with `XDG_CURRENT_DESKTOP=KDE` and
`KDE_SESSION_VERSION` unset, `[ "$KDE_SESSION_VERSION" -lt "6" ]` (xdg-mime.in:715) is a failing test rather
than a true one, so `defapp_kde` is skipped and the `*` branch answers from `mimeapps.list`.

`xdg-mime` then dispatches `query default` after `detectDE` (xdg-mime.in:712-713):

| `DE` | resolver | source |
|---|---|---|
| `kde` with `KDE_SESSION_VERSION` numerically < 6 | `defapp_kde` (trader query); when no `ktraderclient*` is on `PATH` it calls `defapp_generic` | xdg-mime.in:715-717, :507-536 |
| `lxqt` | `defapp_lxqt` — `qtxdg-mat defapp`, exit 3 when absent | xdg-mime.in:720-722, :538-551 |
| everything else, including an empty `DE` (Hyprland), `generic`, and `flatpak` | `defapp_generic` | xdg-mime.in:724-726 |

If `defapp_generic` ever returned without exiting, xdg-mime would exit 3 (:728); in the code as shipped it
always exits (`exit_success` at :504 or :402), so that line is dead.

## 2. `defapp_generic`: the search order

Environment defaults are applied with `[ -n ]` tests, so a variable that is set but empty also falls back
(xdg-mime.in:462-470): `XDG_CONFIG_HOME`→`$HOME/.config`, `XDG_CONFIG_DIRS`→`/etc/xdg`,
`XDG_DATA_HOME`→`$HOME/.local/share`, `XDG_DATA_DIRS`→`/usr/local/share/:/usr/share/`. `case m21`,
`case m22` (unset and empty config home), `case d31` (unset data home).

| # | where | what is read | source |
|---|---|---|---|
| 1 | each `$XDG_CONFIG_HOME` and `$XDG_CONFIG_DIRS` element, in order | `<desktop>-mimeapps.list` for every desktop, then `mimeapps.list` (§3) | :474-479 |
| 2 | each `$XDG_DATA_HOME` and `$XDG_DATA_DIRS` element + `/applications` | the same files (§3) | :481-485 |
| 3 | each data element + `/applications` | `<prefix>defaults.list`, then `<prefix>mimeinfo.cache`, first matching line (§5) | :487-501 |
| 4 | each data element + `/applications`, recursive | any `.desktop` whose text contains `TYPE;`, highest `InitialPreference` (§6) | :503, :372-404 |

The first answer wins and the function exits 0 (:450-451, :497-498, :402, :504). Everything is done with
unquoted expansions, so the directory lists are also **pathname-expanded**: `XDG_CONFIG_DIRS="…/etc?"`
reads `…/etc1` (`case g04`).

Order consequences, each a labelled case: config directories outrank data directories (`case m20`);
`XDG_CONFIG_DIRS` order is honoured (`case m18`); data directories are read in order (`case m19`,
`case f15`); the desktop-specific file in a data directory outranks `mimeapps.list` there (`case m23`).

## 3. Per directory: `<desktop>-mimeapps.list`, then `mimeapps.list`

`check_mimeapps_list` (xdg-mime.in:406-457) walks `for desktop in $XDG_CURRENT_DESKTOP ''` with `IFS=:`
(:413-414): each `:`-separated token is tried in order, then one empty token for the plain file. A token is
lower-cased and given a trailing `-` by `tr '[:upper:]' '[:lower:]'` (:418), so
`XDG_CURRENT_DESKTOP=Hyprland` looks for `hyprland-mimeapps.list` (`case m05`, `case m06`); `B:A` tries
`b-mimeapps.list` before `a-mimeapps.list` (`case m07`); a two-token value is never used whole — with
`GNOME-Classic:GNOME`, a file literally named `gnome-classic:gnome-mimeapps.list` is not read and the
second token's `gnome-mimeapps.list` answers (`case s10`). Each directory therefore
contributes up to `N+1` files, all of that directory's files before the next directory. The file must be a
regular file (`[ -f ]`, :423): a directory of that name is skipped (`case m28`), a symlink to a file is
followed (`case m29`).

The value is extracted by awk (:425-441):

- a line beginning `[Default Applications]` opens the group — the test is `index($0,…) == 1`, so
  `[Default Applications] # x` still opens it (`case m10`), and content after `]` is ignored;
- any other line beginning `[` closes the group (:434); a later `[Default Applications]` re-opens it, so
  a match after an intervening group still counts (`case m15`);
- the key must **start the line** — `index($0, "TYPE=") == 1` (:436) — so an indented key
  (`case m12`), a space before `=` (`case m13`, `case m36`) and `TYPE-x=` (`case m24`) do not match;
- only the **first** matching line in the file is printed (:436-439, `found=1`); a second `TYPE=` line in
  the same file is never consulted (`case m09`: the first line names an uninstalled app, the file's second
  line is ignored, the next directory answers);
- the line's tail is taken verbatim (`substr($0, length(prefix)+1)`, :437), so a CRLF line keeps its `\r`
  and the id never resolves (`case m16`); a file with no final newline still matches (`case m35`);
- `[Added Associations]` and `[Removed Associations]` are never read, since only the default group is
  tracked (`case m14`).

The tail is then a `;`-list: `IFS=\;` and `for app in $result` (:445-446), unquoted, so a space after `;`
stays inside the id (`case m26`), empty pieces are skipped (`case m25`), and the value is pathname-expanded
(`case g02`: `text/plain=*.desktop` in the config resolves to the file `*.desktop` matched in the working
directory). Each app goes through `desktop_file_to_binary` (§4); the first one that resolves is echoed
**exactly as written in the list** and xdg-mime exits 0 (:448-451) — the printed id can contain a `/`
(`case d22`: the list says `sub/x.desktop`, the answer is `sub/x.desktop`, found via `x.desktop` in
`applications/`). When no app of the first matching line resolves, the search continues with the next
file, then the next directory.

## 4. `desktop_file_to_binary`: "is this id installed?"

common:55-90, called with one list entry:

1. Roots are `"${XDG_DATA_HOME:-$HOME/.local/share}:${XDG_DATA_DIRS:-/usr/local/share:/usr/share}"`
   (:57), split on `:` and pathname-expanded (:59-60).
2. `desktop="$(basename "$1")"` (:58). coreutils `basename` reads a leading `-` as an option, so an id
   `-x.desktop` produces nothing and the id cannot resolve even when the file exists (`case d23`).
3. A root is skipped unless it has `applications/` or `applnk/` (:62 — a root with only `applnk/` is used,
   `case d21`, `case d06`).
4. **Vendor layout first**, only when the name contains `-` (:64): `vendor=${desktop%-*}` strips through the
   **last** `-` and `app=${desktop#*-}` strips through the **first**, so `a-b-c.desktop` looks for
   `applications/a-b/b-c.desktop` (:65-71, `case d02`) and `v-x.desktop` for `applications/v/x.desktop`
   (`case d39`, also `applnk/v/x.desktop`). A vendor file found here outranks the flat file of the same
   name in the same root, and its failure ends the whole lookup rather than falling through (`case d32`).
5. Otherwise the flat glob order, inside that root: `applications/`, `applications/*/`, `applnk/`,
   `applnk/*/` (:74-80) — subdirectories are searched (`case d04`), in glob (byte-sorted) order, a hidden
   subdirectory is not (`case d33`), and the first readable name breaks (`case d05`: the first subdirectory's
   copy wins even though its `Exec` is missing).
6. The **first root** that yields a readable file ends the search: the function computes the answer and
   `return`s unconditionally (:82-87), so a readable but unusable copy in an earlier root blocks a good copy
   in a later one (`case d20`, `case d38`). A readable *directory* named `x.desktop` also stops there
   (`case d30`).
7. The answer is "installed" iff the first `Exec` word resolves:
   `grep -E "^Exec(\[[^]=]*])?=" FILE | cut -d= -f 2- | first_word`, then `command -v`, then
   `xdg_realpath` (:84-86). `first_word` is `read first rest; echo "$first"` (common:16-21): the first
   whitespace-delimited word of the first matching `Exec` line with backslash escapes removed and a
   `\`-newline continuation dropped (`case d13`: `Exec=my\ prog` yields the single word `my prog`,
   `case d28`), quote marks are not stripped (`case d12`: `Exec="x"` yields `"x"`), and the word is printed
   through `echo`, so the word `-n` prints nothing (`case d18`). The first matching line may be a localised
   key (`Exec[de]=`, `case d14`) or sit inside `[Desktop Action …]` before `[Desktop Entry]`
   (`case d15`): group structure is not consulted.
8. `command -v` (common:85) sees shell functions of xdg-mime and bash keywords/builtins as names
   (`case d25` `detectDE`, `case d26` `time`, `case d09` `true`); a name containing `/` is tested directly
   and must be executable and not a directory (`case d17` `./run.sh` mode 755, `case d36` mode 644,
   `case d29` a directory); a bare name is searched in `$PATH` in order, skipping non-executable files
   (`case d19`), a dangling symlink (`case d34`) and directories, with an empty `PATH` element meaning the
   working directory (`case d35`).
9. `xdg_realpath` is used only as a truth test: it returns failure unless `[ -e "$1" ]` (common:446-447).
   A builtin or function name therefore resolves iff a *file of that name exists in the working directory*
   (`case d24`: `Exec=true` with an empty file `true` next to the fixtures). `XDG_UTILS_REALPATH_BACKEND`
   selects the backend (common:430-461); an unrecognised value exits 3 (:459-461).
10. Nothing else is checked: no `Type=`, `Hidden=`, `TryExec=`, `MimeType=` or `Path=` key is read, and no
    process is run. The output of the function is only used as `[ -n "$exists" ]` (xdg-mime.in:448-449).

## 5. The `defaults.list` / `mimeinfo.cache` grep fallback

xdg-mime.in:487-501, data directories only, for each directory in order and for
`prefix` = `$XDG_MENU_PREFIX` then `""`:

```
grep "$MIME=" "$x/applications/${prefix}defaults.list" "$x/applications/${prefix}mimeinfo.cache" 2>/dev/null |
head -n 1 | cut -d '=' -f 2 | cut -d ';' -f 1
```

- `defaults.list` is matched before `mimeinfo.cache` (`case f01`, `case f02`, `case f03`), and
  `$XDG_MENU_PREFIX` before the empty prefix (`case f04`, `case f20`).
- The pattern is the raw type text in a **BRE**, so `.` is a wildcard (`case f05`: `text/x.y` matches
  `text/xzy=`), `*` and `+` are literal-ish (`case f17`, `case f19`), and an invalid pattern makes grep
  fail silently (`case f14`).
- The match is **unanchored**: `text/plain=` matches inside `xtext/plain=` (`case f06`), inside a
  `[Removed Associations]` line (`case f07`), and inside `TYPE-x=` (`case f21`). No group is tracked.
- `head -n 1` takes the first matching line in operand order, so a later line of the same file is never
  used, and an empty value there sends the search to the next directory (`case f08`).
- `cut -d '=' -f 2` keeps only the second field of the *whole* output line: a value containing `=` is
  truncated at the second `=` (`case f12` → `a`), and because grep prefixes hits with `file:` whenever it
  has two operands, a file path containing `=` leaks into the answer (`case f13` →
  `are/applications/defaults.list:text/plain`).
- `cut -d ';' -f 1` takes the first `;` field; a value with no `;` is used whole (`case f11`).
- There is **no installation check**: a cache entry naming a missing application is printed
  (`case f16`, after the mimeapps pass failed for the same type).
- The result is printed by `echo "$trader_result"` (:497), so bash's `echo` option parsing applies: the
  capture `-n` is non-empty at the `[ -n ]` gate (:496) but prints nothing before `exit_success`
  (`case f09`: no output, rc 0), and `-e` prints one newline, i.e. an empty string
  (`case f10`: stdout `\n`, label `""`).

## 6. `defapp_fallback`: the `MimeType=` scan

xdg-mime.in:372-404, reached only when §3 and §5 found nothing, data directories only, `<d>/applications`:

- `search_desktop_file` (:359-370) runs `grep -l "$MIME;" "$dir/"*.desktop` (:365) — again a BRE, again
  unanchored, over any line of the file: a `MimeType=text/plain;` line matches (`case b01`), as does any
  other occurrence including a `[Removed Associations]` line. Hidden names are not in the `*.desktop` glob;
  with no match the literal pattern is passed to grep and fails silently (`case b16`).
- It then recurses into every `"$dir/"*/` subdirectory (:367-368) — subdirectory results come after the
  top-level ones, and the recursion is depth-first in glob order (`case b04`).
- The caller expands the result unquoted (`for x in $(…)`, :388), so a file name containing a space is split
  into words and the fragment is used as a path (`case b10`: `my app.desktop` yields the id `my`).
- The score is `pref="0$(awk -F"=" '/InitialPreference=/ {print($2)}' "$x")"` (:389): every matching line's
  second `=`-field concatenated, so an absent key scores `0` (`case b01`), `X-InitialPreference=9` also
  matches and scores 9 (`case b06`), two lines concatenate into a non-number (`case b07`), a non-numeric
  value makes `test -gt` fail and the file is skipped (`case b05`), and `0-1` is −1, which loses to the
  initial −1 threshold comparison (`case b12`).
- `[ "$pref" -gt "$preference" ]` is strict (:392), so with equal scores the earlier file wins; glob order is
  byte-sorted, hence the id comes from the alphabetically first name (`case b03`).
- The answer is `basename` of the winning path (:401) and exit 0 (:402). No installation check.

## 7. Exit status and stdout

- Success with or without an answer is exit 0: `defapp_generic` and `defapp_fallback` end in `exit_success`
  (xdg-mime.in:504, :402; common:96-104). Nothing found prints nothing and still exits 0 — the label
  `{"default": null, "rc": 0}` (`case m02`, `case b16`).
- A malformed type exits 1 before any resolver runs (xdg-mime.in:593-612; common:112-126): no `/`
  (`case s05`), a leading `-` (`case s06`), an empty argument (`case s07`).
- An LXQt session without `qtxdg-mat` exits 3 (xdg-mime.in:538-551; common:140-147, `case s01`).
- `check_common_commands "$@"` scans **every** argument before parsing (common:262, :232-260), so any
  argument equal to `--version` prints `xdg-mime 1.2.1` and exits 0 (:250-253, `case s08`), and `--help` /
  `--manual` print their text; `--` is consumed only when `XDG_UTILS_ENABLE_DOUBLE_HYPEN` is unset (:255-257).
- Only stdout is the answer. `DEBUG` writes to stderr and only when `XDG_UTILS_DEBUG_LEVEL` is at least the
  call's level (common:7-13, :264-272), so the label is unaffected by debug output.
- The answer is printed with `echo`, so a returned id of `-n`/`-e`/`-E` changes the bytes (§5); command
  substitution strips trailing newlines, not a `\r` inside the value (`case f18`: the answer is
  `cr.desktop\r`).

## 8. Decision table: where `xdg-mime` and GLib 2.90.1 differ

Every row is a frozen L1 case of `.ufo/waves/round-92/controls/xdgmime-cases-r92-l1.json`; the xdg-mime
column is that case's stored label (the installed `/usr/bin/xdg-mime`'s stdout). The GLib column is the
round-91 resolver's answer for the same fixture (`corpus/knowledge/mime-default-resolution-r91.md`, the
section named in the last column), re-read in a DRAFT run of `tools/mado-mime.py` on the same files
(`.ufo/waves/round-92/w1/R92MScribeEntry-draft-check.txt`); `—` is "no default", i.e. GLib prints nothing.

| # | state | xdg-mime | GLib 2.90.1 | xdg-mime source | GLib (r91 reference) | case |
|---|---|---|---|---|---|---|
| 1 | `[Added Associations]` is the only group | — | `a.desktop` | :432-439 (default group only) | §3 (additions are read) | m14 |
| 2 | two `TYPE=` lines in one file, first uninstalled | next directory's id | the file's second line | :436-439 | §4 step 2 (last value of the key) | m09 |
| 3 | header with trailing text `[Default Applications] # x` | `a.desktop` | — | :432 | GKeyFile group name must match (S502) | m10 |
| 4 | key indented by one space | — | `a.desktop` | :436 | GKeyFile key must start the line (S502) | m12 |
| 5 | space before `=` | — | `a.desktop` | :436 | same | m13 |
| 6 | CRLF value line | — | `a.desktop` | :437 (`\r` kept) | §9 row 33 (k11) | m16 |
| 7 | `text/plain= a.desktop` (space after `=`) | — | `a.desktop` | :445-446 (only `;` splits) | §5 (leading value whitespace chugged) | m26 |
| 8 | `XDG_CONFIG_HOME` holding two `:`-separated dirs | `b.desktop` (second dir) | — | :475-476 | §2 (one directory per variable) | m32 |
| 9 | id `a-b-c.desktop`, file `applications/a-b/b-c.desktop` | `a-b-c.desktop` | — | common:64-71 | §8 quirk 11 (dir id is `a-b/b-c.desktop`) | d02 |
| 10 | file in `applications/sub/` | `x.desktop` | — | common:74-80 | §8 quirk 11 (dir id is `sub-x.desktop`) | d04 |
| 11 | file in `applnk/` | `x.desktop` | — | common:62, :74 | §2 (applnk is not searched) | d21 |
| 12 | `Exec=true` and no file named `true` in cwd | — | `x.desktop` | common:85-86, :446-447 | §6 step 5 (`argv[0]` must resolve) | d09 |
| 13 | `Exec=my\ prog` | `x.desktop` | — | common:16-21, :84 | §8 quirk 10 (escapes decoded twice) | d13 |
| 14 | first root has a readable file whose `Exec` is missing | — | `x.desktop` (the system copy) | common:82-87 | §4 step 3 (an unloadable file is skipped) | d20 |
| 15 | `defaults.list` `[Default Applications]`, id not installed | `dl.desktop` | — | :493-498 | §4 step 3 (the id must load) | f01 |
| 16 | `mimeinfo.cache` only, no desktop file | `mc.desktop` | — | :493-498 | §4 step 3 (cache entry must load) | f02 |
| 17 | type `text/x.y`, cache line `text/xzy=` | `dot.desktop` | — | :493 (BRE) | §3 (the key is parsed, not matched) | f05 |
| 18 | cache line `xtext/plain=` | `un.desktop` | — | :493 (unanchored) | §3 (group/key parse) | f06 |
| 19 | match inside `[Removed Associations]` | `rm.desktop` | — | :493-494 | §3 (group-aware) | f07 |
| 20 | value `-n` | nothing, rc 0 | — | :496-498 (`echo -n`) | n/a | f09 |
| 21 | value `-e` | `""` (one newline) | — | :497 (`echo -e`) | n/a | f10 |
| 22 | value `a=b.desktop` | `a` | — | :494 (`cut -f 2`) | §4 step 3 (`a` cannot load) | f12 |
| 23 | data-dir path containing `=` | `are/applications/defaults.list:text/plain` | — | :493-494 (`grep file:line`) | n/a | f13 |
| 24 | cache names a missing application | `ghost.desktop` | — | :493-498 (no check) | §4 step 3 | f16 |
| 25 | CRLF in `mimeinfo.cache` | `cr.desktop\r` | — | :494 (`cut` keeps `\r`) | §9 row 33 (k11) | f18 |
| 26 | only a `MimeType=` line in a `.desktop` | `a.desktop` | — | :359-370, :388 | §4 (associations come only from the lists) | b01 |
| 27 | two `MimeType` candidates, one with `InitialPreference=5` | `b.desktop` | — | :389-396 | §4 (no preference weighting) | b02 |
| 28 | equal scores | `a.desktop` (byte-sorted first) | — | :365, :386-396 | §4 | b03 |
| 29 | `InitialPreference=abc` | `b.desktop` (the other file) | — | :389-392 | n/a | b05 |
| 30 | `.desktop` name containing a space | `my` | — | :388 (word splitting) | §4 | b10 |
| 31 | `XDG_CURRENT_DESKTOP=LXQt`, no `qtxdg-mat` | nothing, rc **3** | `a.desktop` | :720-722, :538-551 | §2 (no session dispatch) | s01 |

Rows 1-8 are the mimeapps-file grammar: xdg-mime searches lines of text while GLib parses a key file, so an
added-associations entry, an indented key, a CR or a stray space disappears in one reader and counts in the
other. Rows 9-14 are the installation test: xdg-mime's is the first `Exec` word of a file found by its own
layout rules, GLib's is a full desktop-file load. Rows 15-25 are the `defaults.list`/`mimeinfo.cache`
fallback, which both readers open but with different rules (GLib parses keys and requires the id to load;
xdg-mime greps, cuts and prints). Rows 26-30 are the `MimeType=` scan, for which GLib has no counterpart:
every one of those cases is `—` for GLib because nothing put the association in a list.

## 9. Scope refusals and assumptions of the lane tool

`tools/mado-xdgmime.py` (landed from `.ufo/waves/round-92/build/mado-xdgmime.c1.py` after the freeze)
replays §1-§7 over files only. It **refuses with rc 2 and prints `unsupported`** rather than guessing for:
an LXQt session with `qtxdg-mat` on `PATH`; a KDE session with `KDE_SESSION_VERSION` 4/5 and
`ktraderclient`/`ktraderclient5` on `PATH`; `XDG_UTILS_REALPATH_BACKEND` set to a non-empty value (an
unrecognised value is an exit 3 path, §4.9); `XDG_UTILS_DEBUG_LEVEL` set to a non-empty value; a file it must
read holding a NUL byte (bash drops NULs in
command substitution, which the replay does not model); `PATH` unset (bash's compiled-in default path); and
`--help`/`--manual` as the type (the usage text is not modelled). It **assumes**, without checking:
`org.gnome.SessionManager` has no D-Bus owner and no X root property says xfce — true on a Hyprland session
and with no session bus, and the reason `detectDE` is reduced to its environment cases; and that `PATH`
reaches GNU coreutils, grep and gawk under their own names (§4.8, §5). It models `PATH` only for
`command -v` inside `desktop_file_to_binary`; it runs no program, writes nothing and opens only the files
named in §2-§6.

Known limits, stated rather than hidden: `query filetype` is out of scope, so the tool answers the second
half of xdg-open's file path only; stderr text is not reproduced; a `--version`/`--help` argument anywhere
in a real invocation short-circuits the whole script (common:262) while the tool treats its arguments as
types in order.

## 10. How to run it

```sh
python3 -I tools/mado-xdgmime.py text/plain
python3 -I tools/mado-xdgmime.py --json image/png application/pdf x-scheme-handler/https
python3 -I tools/mado-xdgmime.py --env XDG_CURRENT_DESKTOP=sway --env HOME=/home/u text/html
python3 -I tools/mado-xdgmime.py --from-environ text/plain      # this session's variables
python3 -I tools/mado-xdgmime.py --cwd /some/dir --env PATH=/usr/bin:/bin text/plain
```

`--env NAME=VALUE` sets one variable of the resolved environment (repeatable; the default environment is
empty), `--from-environ` starts from the caller's environment, `--cwd` fixes the working directory used for
the pathname expansions of §2-§6 (default: the process cwd), and `--` ends option parsing.

Text output on stdout: one line per type, `TYPE<TAB>APP`, or `TYPE<TAB>-` when `xdg-mime` would print
nothing; `--json` prints `{"results":[{"type","default","rc"}]}` with `default` null for no output and `rc`
the exit status xdg-mime would use (0 with or without an answer, 1 for a malformed type, 3 for LXQt). The
process exits 0 on a completed run and 2 on a refusal (§9).
