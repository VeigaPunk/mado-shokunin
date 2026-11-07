# R98MScoutExec - reconnaissance of the C1 launch-argv surface (round 98, w1)

Seat: scout (read-only; no candidate edits). Scope: the ground truth of the argv GIO 2.90.1
builds from a desktop entry's `Exec` key, for `gio launch DESKTOP [FILE-ARG...]`.

Everything below is **measured** against the installed `/usr/bin/gio` (glib2 2.90.1-1,
`/usr/bin/gio` sha256 `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`)
using a case root under the seat's scratch dir, whose `Exec` first token is a `probe.sh` that
records its own argv. No host application was launched; the only child processes are the case
roots' own probes, spawned by `gio` as a descendant of a case root the seat built.

## 0. Source provenance and digest verification

`[[W]]/receipts/sources-open-r98.txt` - verified byte-for-byte against
`[[W]]/fetch/` (recomputed sha256, byte counts):

| file | receipt sha256 | recomputed | bytes | verdict |
|---|---|---|---|---|
| `gdesktopappinfo.c` | `8e9ce1a8...5495b0d` | `8e9ce1a8...5495b0d` | 163369 | MATCH |
| `gshell.c` | `640a0d0f...0e60442` | `640a0d0f...0e60442` | 21464 | MATCH |
| `exec-variables.html` | `2c50a9e4...635277e` | `2c50a9e4...635277e` | 17153 | MATCH |

The receipt's located quotes are all present at the cited lines (verified in S1/S2 below).
Two further URLs were opened by this seat to close gaps the L1's three sources do not cover;
each was fetched with `curl -sSL -o <file> -w '%{http_code} %{url_effective}'` and counts only
at HTTP 200 (QUALITY 164):

| URL | HTTP | bytes | sha256 | why |
|---|---|---|---|---|
| `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gio-tool-launch.c` | 200 | 5704 | `16b4c8683b00407670f600eda0e65e9d929a59daac499cbe8f3d1fd532f6595a` | the `gio launch` CLI itself |
| `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gkeyfile.c` | 200 | 142052 | `e1d1270f6c9881daf8a9f49b41395cbdd8e99fa290212e8530e0bd3df23ff656` | the key-file value/escape layer (already registry row S502) |
| `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gio-launch-desktop.c` | 200 | - | `6d8df7399bf7600035101fc5f3a2f8fb83bfe58a368f516fa3876895c3759941` | the exec wrapper |
| `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gfile.c` | 200 | - | `1d72b7bd7dc63bbe40db081da9422ec8df33323a45feeae2ad04b2cac420999b` | `g_file_new_for_commandline_arg` |
| `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gutils.c` | 200 | - | `65086c293646bf83884f56f54bb5e2e872adb28ee77f1223d6d9f095a75e3771` | `g_find_program_for_path` (registry row S506) |

`gutils.c` sha256 `65086c29...` is byte-identical to registry row **S506**'s recorded digest, and
`gkeyfile.c` `e1d1270f...` to **S502**'s - the fetches agree with the registry.

`gio-tool-launch.c` establishes the CLI contract the case file assumes:
`g_canonicalize_filename (argv[1], NULL)` -> `g_key_file_load_from_file` (a *separate* parse,
used only for a better error message) -> `g_desktop_app_info_new_from_filename` ->
`g_file_new_for_commandline_arg` per FILE-ARG -> `g_app_info_launch`.

## 1. Rule table - `gdesktopappinfo.c`

Every rule below is stated as `rule -> file:line -> observed`.

| # | rule | line(s) | observed |
|---|---|---|---|
| R1 | desktop file loads only if the **start group** is `[Desktop Entry]` | 1905-1910 | `[Other]` first => `gio: Unable to load application information` (probe `fn03`, `b07`) |
| R2 | `Type` must be `Application` | 1912-1921 | `Type=Link`/`Applicationx`/absent => same refusal (`k04`, `ag01`-`ag03`) |
| R3 | `TryExec` must resolve to an executable | 1946-1961 | `TryExec=/nonexistent/xyz` => load refusal (`b06`) |
| R4 | `Exec` must parse **at load time** via `g_shell_parse_argv` | 1974-1984 | `Exec=probe 'unterminated` => load refusal, *not* a launch-stage refusal (`t06`) |
| R5 | `Exec`'s **argv[0] must resolve to an executable** | 1993-2003 | `/nonexistent/probe.sh` => load refusal (`b04`); a bare name not in `PATH` => load refusal (`b05`) |
| R6 | `Exec` absent => `no-exec` refusal | 2713-2718 | `gio: ... Desktop file didn't specify Exec field` (`b03`) |
| R7 | `Exec` present but empty => `exec-parse` refusal (EMPTY_STRING) | 2743 + gshell 590/607 | `Exec=` => `gio: ... Text was empty (or contained only whitespace)` (`b01`, `b02`) |
| R8 | the `%` walk: `%` + any byte => that byte is the **macro selector and is consumed** | 2722-2733 | `a%1b` => `ab`; `100% done` => `100done` (the space is eaten) (`ad02`, `ad01`) |
| R9 | a **trailing** `%` (last byte) is copied literally | 2724 (`p[1] != '\0'`) | `a%` => `a%` (`ad04`) |
| R10 | `%%` => one literal `%` | 2692-2694 | `a%%b` => `a%b` (`ad03`) |
| R11 | an unknown macro (`%z`, `%q`, `%1`, `% `) expands to **nothing** - no error, no text | 2617-2696 (no `default:` arm) | `%z` => nothing; the walk still consumed the selector byte (`m28`, `m29`, `ad02`) |
| R12 | `%u`/`%U` set `force_file_uri=TRUE` and `force_file_uri_macro='f'`/`'F'` | 2598-2615 | `%u` with a local file => the **path**, not `file://...` (`m10`); `%u` with `X-GIO-NoFuse=true` => the **URI** (`h08`) |
| R13 | `force_file_uri` applies only when `!info->no_fuse` (`X-GIO-NoFuse`) | 2600, 2021 | `X-GIO-NoFuse=true` => `%u` yields `file:///.../a.txt` (`h08`) |
| R14 | `expand_macro_uri`: if `!force_file_uri` **or** the URI contains `#` => expand the **URI's own** macro (`u`->URI, `f`->path) | 2563-2567 | `%u` + `file://.../a.txt#frag` => the path (`m12`, `r01`); `%u` + `http://...#frag` => the URI verbatim (`d03`, `fn05`) |
| R15 | `expand_macro_uri` else-branch: try `force_file_uri_macro` first, fall back to the URI macro only if that returned NULL | 2568-2575 | `%u` + local file => path; `%u` + http => URI (path is NULL for non-local) (`m10`, `m11`) |
| R16 | `%f`/`%F` expand to `g_file_get_path` - **NULL for a non-local URI**, so nothing is emitted | 2522-2527 | `%f` + `http://...` => the macro emits **nothing** (`q10`, `m12`) |
| R17 | `%d`/`%D` => `g_path_get_dirname` of the path (NULL => nothing) | 2528-2537 | `%d` + `http://...` => nothing (`q08`); `%d` + local => the directory (`e02`) |
| R18 | `%n`/`%N` => `g_path_get_basename` of the path (NULL => nothing) | 2538-2547 | `%n` + `http://...` => nothing (`q09`); `%n` + local => the basename (`e03`) |
| R19 | `%f`/`%u`/`%d`/`%n` consume **one** URI, and consume it **even when the expansion is NULL** | 2619-2636 | `%f` + http => the URI is consumed, the launch still happens (`q10`) |
| R20 | `%F`/`%U`/`%D`/`%N` consume **every remaining** URI; a NULL expansion emits **no text and no separator** | 2638-2657 | `%F` + [http, local] => only the local path, and the http URI is **dropped** (`q12`); `%F` + [local, http] => only the local path (`q13`); `%F` + [http, local, local] => two paths, http dropped (`h06`) |
| R21 | the separator between multi-URI expansions is a space **only when the previous expansion was non-NULL** | 2655-2656 | `%F` glued to a word: `x%F` with [http, local] => `x/abs/.../a.txt` - the `x` and the path are **concatenated with no space** (`i01`, `i02`, `i03`) |
| R22 | `%i` => `--icon ` + `g_shell_quote(icon_name)`, only when `icon_name` is set | 2661-2669 | `Icon=myicon` => `--icon 'myicon'` (`m22`); no `Icon` => nothing (`m23`, `n01`); `Icon=` (empty) => `--icon ''` (`c01`) |
| R23 | `%c` => `g_shell_quote(name)`, only when `name` is set | 2671-2677 | `Name=Probe App` => `'Probe App'` (`m24`); `Name` absent => nothing (`n02`, `k05`) |
| R24 | `%k` => `g_shell_quote(filename)` - the **canonicalized** desktop path, not the path as given | 2679-2686 + gio-tool-launch.c:83 | `gio launch app.desktop` (relative) => `%k` = the absolute path (`g01`, `ac01`); `./sub/../app.desktop` => normalized absolute path (`ac02`) |
| R25 | `%m` => nothing (deprecated) | 2688-2690 | `%m` => nothing, and the URI is **not** consumed => the no-substitution rule then fires (`m35`, `q07`) |
| R26 | **no-substitution rule**: if the URI list head pointer is **unchanged** after the walk and the list is non-empty => append one space + a `%f` expansion | 2735-2741 | `Exec=probe` (no macro) + 1 file => the file is appended (`m02`); with 3 files => 3 launches, one file each (`m03`, `q06`) |
| R27 | the fallback `%f` is applied to the **first remaining** URI, and the URI is consumed | 2740 (uses `expand_macro('f',...)`) | plain Exec + 3 files => launch 1 gets `a.txt`, launch 2 `b.txt`, launch 3 `c.txt` (`m03`, `q06`) |
| R28 | the fallback fires even when a **non-consuming** macro (`%c`, `%i`, `%k`, `%m`, `%z`) is present | 2736 compares the **head pointer**, not a count | `%c` + 1 file => argv = `[probe, 'Probe App', <file>]` (`q02`); `%i` + 1 file => `[probe, '--icon', 'ic', <file>]` (`q03`); `%k` + 1 file => `[probe, <desktop path>, <file>]` (`q04`) |
| R29 | the expanded string is parsed by `g_shell_parse_argv` | 2743 | the parse is of the **expanded** string, so quoting introduced by expansion participates (`p01`) |
| R30 | the **iteration rule**: the whole expansion repeats while URIs remain | 3007-3186 (`do { ... } while (dup_uris != NULL)`) | `Exec=probe %f` + 3 files => **3** launches, one file each (`q07`); `Exec=probe %F` + 3 files => **1** launch with 3 files (`q05`, `m09`); `Exec=probe %f %f` + 3 files => **2** launches (`[a,b]`, `[c]`) (`ai-ff-3`, `q05`) |
| R31 | each iteration's expansion sees the **remaining** URIs | 3018 (passes `&dup_uris`) | `%f %f` + 2 files => 1 launch with both (`ai-ff-2`); `%f %F` + 3 => 1 launch with all 3 (`ai-fF-3`) |
| R32 | with **no arguments** there is exactly **one** launch | 3186 (`dup_uris == NULL` => one pass) | `Exec=probe` + 0 args => 1 launch (`m01`, `ai-plain-0`) |
| R33 | `Terminal=true` prepends a terminal emulator to the argv | 3027-3031, 2749-2830 | the probe becomes argv[1] of `xdg-terminal-exec` (`ab01`); on this host `xdg-terminal-exec` then fails on no display => **no probe record** (`k02`, `term-real`) |
| R34 | `Path=` is the child's working directory; a non-existent `Path` => spawn refusal | 3036 (`info->path`), 3141 | `Path=/nonexistent/dir` => `gio: ... Failed to change to directory` (`m01-path-missing`) |
| R35 | `Hidden=true` does **not** prevent the launch | 2022 (read), 2209 (the only launch-path check is elsewhere) | `Hidden=true` => launches normally (`k01`) - confirms the L1's folded-in correction |
| R36 | `Icon`/`Name` are **locale** strings | 2007, 2013 (`get_locale_string`) | `LC_ALL=en_US.UTF-8` + `Name[en_US]=USName` => `%c` = `USName`; `LC_ALL=C` => `BaseName` (`af01`-`af03`, `loc01`-`loc03`) |
| R37 | a relative `Icon` loses a trailing `.png`/`.xpm`/`.svg` | 2049-2053 | `Icon=foo.png` => `%i` = `foo`; `Icon=foo.jpg` => `foo.jpg`; `Icon=/abs/ic.png` => unchanged (`c02`, `k01`, `k02`, `k03`, `c03`) |
| R38 | the key-file value layer rejects escapes outside `{s,n,t,r,\}` | gkeyfile.c 4743-4764 | `Exec=probe a\ b` => load refusal (`t05`, `m32`, `l04`); a **doubled** `\\` survives to the tokenizer (`o01`, `y05`) |
| R39 | the key-file layer turns `\n` into a real newline and `\s` into a space | gkeyfile.c 4716-4734 | `Exec=probe \nx` => argv `[probe, 'x']` (`l09`, `aa01`) - the newline **delimits** in the tokenizer |
| R40 | `argv[0]` of the spawned process is the **resolved** program, not the Exec token | 3064-3105 | `Exec=probe.sh` (bare name) => the probe's `argv[0]` is the absolute path (`j01`, `z-argv0`) |

### `gshell.c` - the tokenizer rules

| # | rule | line(s) | observed |
|---|---|---|---|
| S1 | whitespace splits words; `' '`/`'\t'` delimit a token, unquoted blanks are discarded | 503-510 | `probe  x` => `[probe, 'x']` (`l08`) |
| S2 | a newline **delimits** a token (and is kept inside a token otherwise) | 499-501 | `probe a\nb` => `[probe,'a','b']` (`aa01`) |
| S3 | single quotes are literal - **no** escapes inside | 522-526 + 154-171 | `'a\b'` => `a\b` (`y03`) |
| S4 | double quotes honour exactly `\"`, `\\`, ``\` ``, `\$`, `\n`; any other backslash is **kept** | 108-131 | `"a\"b" "c\\d" "e\$f" "g\`h"` => `a"b`, `c\d`, `e$f`, ``g`h`` (`y01`); `"a\zb"` => `a\zb` (`y02`) |
| S5 | outside quotes, `\` escapes the next byte; `\`+newline vanishes | 449-465 + 293-317 | `a\ b` => `a b` (one word) (`y05`, `o02`); `a\<newline>b` => `ab` (`fn01`) |
| S6 | a `#` **at the start of a token** starts a comment that discards to end of line; a `#` inside a word is literal | 534-552 | `probe keep # drop` => `[probe,'keep']` (`z01`, `t01`); `a#b` => `a#b` (`t02`); a `#` as the very first char of the Exec => the whole line is a comment => load refusal (`z02`, `s01`) |
| S7 | an unterminated quote is an error | 579-600 | `probe 'unterminated` => load refusal (`t06`) - see R4: the **load-time** parse fails first |
| S8 | an empty command line => `G_SHELL_ERROR_EMPTY_STRING` | 590, 607 | `Exec=` => refusal (`b01`) |
| S9 | an **empty quoted argument** is preserved as an empty argv element | 487-510 (quotes make the token non-empty) | `probe '' x` => `[probe,'','x']` (`t07`, `aa02`) |
| S10 | `g_shell_quote` always single-quotes; `'` => `'\''` | 200-233 | `'Bob''s App'` => `Bob's App` (`c07`); a file `a'b.txt` => `a'b.txt` (`m34`, `p03`) |

## 2. `exec-variables.html` - documented field codes and where GLib 2.90.1 departs

Documented codes (spec page, `exec-variables.html`): `%f` `%F` `%u` `%U` `%d` `%D` `%n` `%N` `%i`
`%c` `%k` `%v` `%m`.

| departure | spec says | GLib 2.90.1 does | source line |
|---|---|---|---|
| `%d %D %n %N` | Deprecated (spec lists them) | **implemented** - `%d`=dirname, `%n`=basename | 2528-2547 |
| `%v` | Deprecated | **absent** - no `case 'v'`, so `%v` expands to nothing and its byte is consumed | 2617-2696 (no `v` arm) |
| `%m` | Deprecated | present but expands to nothing | 2688-2690 |
| `%i` | "expanded as **two arguments**, first `--icon` then the Icon value"; "should not expand to any arguments if the Icon key is empty or missing" | `--icon` + value as two argv elements - **matches**; but an **empty** `Icon=` still yields `--icon` + an empty element, which the spec forbids | 2661-2669 |
| `%u %U` | "Local files may either be passed as `file:` URLs or as file path" | takes the **path** for a local file (FUSE intent) - a permitted choice, but not the only one | 2598-2615, 2557-2575 |
| unknown field code | "Command lines that contain a field code that is not listed ... are **invalid and must not be processed**" | **silently ignored** - no error, the byte is consumed, and the rest of the line still runs | 2617-2696, 2724-2733 |
| more than one `%f`/`%u`/`%F`/`%U` | "A command line may contain at most one" | **accepted**; the second code sees the next URI | 2619-2657 |
| field code inside a quoted argument | "the result ... is undefined" | the expansion happens **inside** the quotes and the quoted value is then re-parsed | 2722-2743 |
| quoting of the Exec line | spec mandates **double** quotes | `g_shell_parse_argv` accepts **single** quotes (literal) as well | gshell.c 522-526 |
| `#` in the Exec line | not mentioned | `#` at a token start begins a **comment** | gshell.c 534-552 |
| `Name`/`Icon` | plain keys | **locale** keys (`Name[ll]`, `Icon[ll]`) are consulted | 2007, 2013 |

## 3. Attack on the declaration's C1 rules 1-5

The L1 folded three corrections into rules 1-3 after its own measurements. **All three are
confirmed here** - and each is re-derived with an independent witness:

* **Hidden is read, not refused** (rule 1) - confirmed: `Hidden=true` launches (`k01`).
* **The `#`-bypass of `expand_macro_uri` is unobservable through `gio launch`** (rule 3) -
  confirmed *and sharpened*: the reason is not only that "a local file URI's fragment is
  dropped" (R14) but that **a non-local URI answers the URI on both branches** (R15), because
  `g_file_get_path` is NULL for it. So the branch is doubly unobservable. A **non-local** URI
  *with* a `#` does keep its fragment (`d03`, `fn05`) - the `#` is preserved in the URI, it just
  does not change the branch's answer.
* **GKeyFile refuses an Exec escape outside `{s,n,t,r,\}`** (rule 1) - confirmed (R38), and the
  **doubled** `\\` is the only way a backslash reaches the tokenizer (R38, `o01`, `y05`).
* **`gio launch` builds the app info from the filename** (rule 1) - confirmed via
  `gio-tool-launch.c:83` (`g_canonicalize_filename`) and R24 (`%k` is the canonicalized path).

### Sentences the source contradicts

| declaration sentence | contradicted by | the contradiction |
|---|---|---|
| rule 2: "`%X` is a field code ... every other byte is copied" | 2724-2732 | the byte **after** `%` is consumed as the selector, so `a%1b` => `ab` and `100% done` => `100done` - the space vanishes (R8, `ad01`, `ad02`) |
| rule 2 (implied): "a trailing `%` is a literal `%`" - true, but the rule omits that a `%` followed by **any** byte consumes that byte | 2724 | same as above; the trailing-`%` case is the *only* one where the byte after `%` survives |
| rule 3: "`%f`/`%u`/`%d`/`%n`: consume one argument ...; append `g_shell_quote(value)`" - stated as if the value always exists | 2522-2547 | for a **non-local** URI the value is **NULL**: nothing is emitted (`q08`-`q10`) |
| rule 3: "`%F`/`%U`/`%D`/`%N`: consume **every** remaining argument, each `g_shell_quote`d and space-joined" | 2638-2657 | a non-local URI under `%F`/`%D`/`%N` is **consumed and dropped** - it is neither quoted nor joined (`q12`, `q13`, `h06`). The list shrinks, not just the text |
| rule 3: "each `g_shell_quote`d and space-joined" (implies a separator between every pair) | 2655-2656 | the separator is emitted **only if the previous expansion was non-NULL**, so a preceding NULL expansion leaves the next one **glued** to the preceding text (`i01`: `x%F` => `x/abs/.../a.txt`) |
| rule 3: "`%u`/`%U`: the argument is first passed as a file path when the GFile has a local path ... else as the URI itself" | 2598-2615, 2600, 2021 | true **unless `X-GIO-NoFuse=true`**, which clears `force_file_uri` and makes `%u` yield the `file://` URI (`h08`) - the declaration does not mention `X-GIO-NoFuse` at all |
| rule 3: "`%i`: `--icon ` + `g_shell_quote(Icon)`" | 2049-2053 | the quoted value is **not** the `Icon` key: a relative `Icon` loses a trailing `.png`/`.xpm`/`.svg` (`c02`: `Icon=foo.png` => `foo`) |
| rule 3: "`%c`: `g_shell_quote(Name)`" | 2007 | `Name` is the **locale** string; `Name[en_US]` wins under `LC_ALL=en_US.UTF-8` (`af02`, `loc02`) |
| rule 3: "`%k`: `g_shell_quote(desktop path)`" | 2679-2686, gio-tool-launch.c:83 | it is the **canonicalized absolute** path, not the path as passed (`g01`, `ac02`) |
| rule 4: "if the walk consumed no argument and arguments were given, one space and a `%f` expansion are appended" - "the walk consumed no argument" | 2736 | the test is **pointer equality of the list head**, not a consumption count. A **non-consuming** macro (`%c`, `%i`, `%k`, `%m`, `%z`) leaves the head unchanged => the fallback fires *alongside* it (`q02`-`q04`) |
| rule 4: "(so only the **first remaining** argument is used)" | 2740 | correct per iteration, but the iteration makes it the first argument of **each** launch, not of one (`m03`: 3 launches, one file each) |
| rule 6: "a `%F`-only Exec spawns once; a `%f` Exec spawns once per argument" | 3007-3186 | the count depends on **how many** URIs each iteration consumes, not on the code's kind: `%f %f` + 3 args => **2** launches (`ai-ff-3`), `%f %F` + 3 => **1** (`ai-fF-3`) - the rule as written does not determine the count |
| the frozen-case contract: "A case whose `gio launch` exits nonzero or writes no `.out` is a REFUSAL case" | 3036, 3141 (spawn is async) | `gio launch` **returns before its child writes** (measured: gio exits at 0.003 s, the child's record appears at 1.0 s) - so "writes no `.out`" must be tested **after** quiescence, not at gio's exit (see S5) |

## 4. Class table - the declaration's 16 classes vs what is reachable

The declaration's classes are `plain, f, F, u-file, u-uri, u-anchor, U-mixed, d, n, i, c, k,
pct, bad, quote, path`. Every one of them is reachable and measured. The table gives the class ->
the probe -> the observed argv.

| class | probe (Exec + args) | observed argv |
|---|---|---|
| `plain` | `probe` + 0 args | `[probe]` (1 launch) - `m01` |
| `plain` | `probe` + 1 file | `[probe, <file>]` (1 launch) - `m02` |
| `plain` | `probe` + 2 files | 2 launches: `[probe,a]`, `[probe,b]` - `m03` |
| `f` | `probe %f` + 0 args | `[probe]` - `m04` |
| `f` | `probe %f` + 1 file | `[probe, <file>]` - `m05` |
| `f` | `probe %f` + 2 files | 2 launches, one file each - `m06` |
| `F` | `probe %F` + 0 args | `[probe]` - `m07` |
| `F` | `probe %F` + 1 file | `[probe, <file>]` - `m08` |
| `F` | `probe %F` + 3 files | **1** launch `[probe,a,b,c]` - `m09` |
| `u-file` | `probe %u` + local file | `[probe, <abs path>]` (the **path**, not `file://...`) - `m10` |
| `u-uri` | `probe %u` + `http://example.com/x` | `[probe, 'http://example.com/x']` - `m11` |
| `u-anchor` | `probe %u` + `file://.../a.txt#frag` | `[probe, <abs path>]` - the fragment is dropped - `m12`, `r01` |
| `U-mixed` | `probe %U` + file + http | **1** launch `[probe, <path>, 'http://example.com/x']` - `m13` |
| `d` | `probe %d` + `<root>/a.txt` | `[probe, <root>]` (the dirname) - `e02` |
| `n` | `probe %n` + `<root>/a.txt` | `[probe, 'a.txt']` (the basename) - `e03` |
| `i` | `probe %i`, no `Icon` | `[probe]` - `m23`, `n01` |
| `i` | `probe %i`, `Icon=myicon` | `[probe, '--icon', 'myicon']` - `m22` |
| `c` | `probe %c` | `[probe, 'Probe App']` - `m24` |
| `k` | `probe %k` | `[probe, <abs desktop path>]` - `m25` |
| `pct` | `probe 100%%` | `[probe, '100%']` - `m26` |
| `pct` | `probe 100%` | `[probe, '100%']` - `m27` |
| `bad` | `probe %z` + file | `[probe, <file>]` - the unknown macro emits nothing, the URI is unconsumed, so the **fallback** adds the file - `m28` |
| `bad` | `probe %q` + file | `[probe, <file>]` - `m29` |
| `quote` | `probe 'lit arg'` | `[probe, 'lit arg']` - `m30` |
| `quote` | `probe "dq arg"` | `[probe, 'dq arg']` - `m31` |
| `path` | `probe %f` + `a b.txt` | `[probe, '<root>/a b.txt']` (one argument, space preserved) - `m33` |
| `path` | `probe %f` + `a'b.txt` | `[probe, "<root>/a'b.txt"]` - `m34`, `p03` |

### Classes the declaration does not name, but which are reachable

Each is a real edge with a probe; the declaration's 16 classes do not cover them.

| # | missing class | probe | observed | why it matters |
|---|---|---|---|---|
| **X1** | **multi-launch** (a class whose point is *several* spawns) | `probe %f` + 3 files | 3 launches, one file each (`q07`); `probe %F` + 3 files => 1 launch with 3 (`q05`) | the L1's own contract change made the argv a **sequence**; a class that only means something with multiple spawns is `f`-with-2-args and `plain`-with-2-args |
| **X2** | **`%` + non-alpha byte** | `probe 100% done` | `[probe, '100done']` - the space is **eaten** (`ad01`, `w01`) | `pct` covers `%%` and a trailing `%`, not `%`+space/`%`+digit; a model that copies the byte after `%` fails here |
| **X3** | **`%` + unknown alpha** | `probe a%1b` | `[probe, 'ab']` (`ad02`) | same mechanism as X2 |
| **X4** | **`#` comment** | `probe keep # drop this` | `[probe, 'keep']` - the rest of the line is **discarded** (`t01`, `z01`) | the tokenizer's `#` rule is entirely absent from the declaration's rule 2 and from the 16 classes |
| **X5** | **`#` at the very start of the Exec** | `Exec=#{probe}` | **load refusal** (`z02`, `s01`) | a different refusal cause from `exec-parse` |
| **X6** | **`%F`/`%D`/`%N` with a non-local URI** | `probe %F` + http + file | the http URI is **consumed and dropped**: `[probe, <file>]` (`q12`, `q13`) | the declaration's rule 3 says every remaining argument is quoted and joined - it is not |
| **X7** | **`%f`/`%d`/`%n` with a non-local URI** | `probe %f` + http | `[probe]` - **nothing** is emitted, and the URI *is* consumed (`q08`-`q10`) | `d`/`n`/`f` classes are only defined on local files |
| **X8** | **`%u` + `file://` URI** | `probe %u` + `file://{root}/a.txt` | `[probe, <abs path>]` (`d01`, `m14`) | the URI form of a local file still yields the path |
| **X9** | **`X-GIO-NoFuse=true`** | `probe %u` + local file, with `X-GIO-NoFuse=true` | `[probe, 'file:///.../a.txt']` - the **URI**, not the path (`h08`) | the declaration never mentions this key; it flips `%u`/`%U` |
| **X10** | **non-empty `Icon` with an image extension** | `probe %i`, `Icon=foo.png` | `[probe, '--icon', 'foo']` - the extension is **stripped** (`c02`, `k01`, `k02`) | rule 3 quotes the `Icon` key verbatim; the source does not |
| **X11** | **empty `Icon`** | `probe %i`, `Icon=` | `[probe, '--icon', '']` (`c01`) | an empty `Icon` still emits the `--icon` pair - the spec forbids this |
| **X12** | **locale `Name`/`Icon`** | `probe %c` with `Name[en_US]=USName`, `LC_ALL=en_US.UTF-8` | `[probe, 'USName']` (`af02`) | the frozen oracle runs under `LC_ALL=C`, so the base key wins there - but the model must not hard-code "the `Name` key" |
| **X13** | **`Terminal=true`** | `probe` with `Terminal=true` | the argv becomes `[xdg-terminal-exec, probe, ...]` - the probe is **not** argv[0] (`ab01`); on this host the terminal then fails (no display) and **no probe record is written** (`k02`, `term-real`) | a case with `Terminal=true` would look like a refusal to a `.out`-based oracle |
| **X14** | **non-existent `Path=`** | `probe` with `Path=/nonexistent/dir` | spawn refusal `Failed to change to directory` (`m01-path-missing`) | a refusal cause not in the declaration's list |
| **X15** | **`Exec` whose argv[0] does not resolve** | `Exec=/nonexistent/probe.sh %f` | **load** refusal (`b04`, `b05`) | distinct from `exec-parse`; the case file's `Exec` is normally `{probe}`, so this only arises if a case varies the program |
| **X16** | **doubled backslash reaching the tokenizer** | file bytes `Exec=probe a\\b` | `[probe, 'ab']` - the tokenizer's outside-quote escape (`y05`, `o01`) | a single `\` is a **load refusal** (R38), so the tokenizer's backslash rule is only reachable via `\\` |
| **X17** | **`%` inside a quoted argument** | `probe '%f'` + file | `[probe, <file>]` - the quotes are **consumed** by the expansion and the value is re-parsed (`q01`, `a01`) | the spec calls this undefined; GLib does something specific |
| **X18** | **double-quoted `%`** | `probe "%f"` + file | `[probe, "'/.../a.txt'"]` - the **literal single quotes** survive, because the expansion's own quoting is *inside* the double quotes (`a02`) | the quoting of the expansion and the quoting of the Exec line interact |
| **X19** | **empty quoted argument** | `probe '' x` | `[probe, '', 'x']` (`t07`, `aa02`) | the tokenizer keeps an empty quoted argument |
| **X20** | **`#` mid-word** | `probe a#b` | `[probe, 'a#b']` (`t02`) | the complement of X4 |
| **X21** | **newline in the Exec value** | `probe a\nb` (key-file `\n`) | `[probe, 'a', 'b']` - the newline **delimits** (`l09`, `aa01`) | the tokenizer treats `\n` as a delimiter, distinct from a space |
| **X22** | **`Exec` starting with a field code** | `Exec=%f /usr/bin/true` | **load** refusal (`ah01`) | the load-time parse sees `%f` as argv[0] and fails to resolve it |
| **X23** | **`%` inside the *program path*** | a case root whose path contains `%` | the `%` is eaten **in the path too**, so the program path is corrupted (`dbg-%f` case) - a case-builder hazard, not a GIO rule | the walk covers the whole `Exec` line, path included |

**The declaration's class list is therefore incomplete on both ends**: it omits classes whose
answer is *not* a per-URI quote-and-join (X4, X6, X7, X9, X10, X11, X13, X17, X18, X19, X21) and it
omits the refusal shapes (X5, X14, X15, X22). If the counter freezes only the 16 named classes,
a model that implements the 16 named rules exactly can still be wrong on the reachable edges
above - that is the falsification surface this wave needs.

## 5. Two defects in the L1's oracle design - found by measurement

The declaration's case-file contract is: *"The probe child appends one record per spawn (`@@@ <argc>`
then `A<i>=<value>` lines) to `<probe>.out`; the oracle waits until the file stops changing (200 ms
of no change, 8 s cap) and parses the records in spawn order."* Two things in that sentence do not
hold against the installed `gio`.

### Defect B - the 200 ms quiescence rule truncates the label

`gio launch` spawns asynchronously (R34/R30: `g_spawn_async_with_fds`, gdesktopappinfo.c:3141)
and **returns before its child writes**. Measured: `gio launch` exited at **0.003 s** while the
child's record appeared at **1.0 s**. With a child that delays its write by 1.5 s, the
200 ms-quiescence reader stopped at **0.22 s having seen 1 record**, while the file eventually held
**2** - 4/4 trials truncated (`qB2-*`):

```
trial 0: quiescence stopped at 0.22s having seen 1 record(s); the file eventually holds 2 -> TRUNCATED LABEL
trial 1: ... 1 ... 2 -> TRUNCATED LABEL
trial 2: ... 1 ... 2 -> TRUNCATED LABEL
trial 3: ... 1 ... 2 -> TRUNCATED LABEL
```

A frozen label produced this way says "1 launch" where the truth is 2 - and the case would then
be graded against a wrong expectation. The same trap applies to the refusal test: *"a case whose
`gio launch` exits nonzero **or writes no `.out`**"* misfires if "writes no `.out`" is checked at
gio's exit instead of after quiescence (`timing2`).

### Defect C - "parses the records in spawn order" is false

The children run **concurrently**; the shared append file records *completion* order, not spawn
order. With the first-spawned child delayed 1 s, the file order is **inverted** - reproducibly
3/3 trials (`t1-order`, `ord-final`):

```
spawn order: a.txt then b.txt   (the do-while loop spawns in URI order)
file order  : b.txt, then a.txt
```

and under 8x CPU load with no artificial delay the order still flipped in 1/20 trials
(`%f x 3 args`). So a frozen `expect.argv` that is an **ordered** list is not reproducible from a
shared append stream, and the L1's own note that the records are parsed "in spawn order" cannot be
honoured by that reader.

**Fixes that measure clean** (both verified):
1. **One write per record.** A probe that builds the whole record in a variable and emits it with a
   single `printf` never interleaves (25/25 clean, `ae2`); the multi-`printf` form interleaved in
   1/20 trials (`ae1`) and produced a visibly torn record in `q06-plain-three`.
2. **Per-child files.** Each child writes its own file (e.g. `<probe>.out.<n>` or a file named
   from its own argv) - no shared buffer, no order dependence, and the **count** of files is
   exactly the launch count: `probe`+3 => 3 files, `probe %f`+3 => 3 files, `probe %F`+3 => **1** file,
   `probe %f %f`+3 => **2** files (`pf*`).

If the L1 keeps the shared-file form, the label must be an **unordered multiset** of argv vectors
and the reader must wait for the *expected count* (which the model predicts) rather than for
quiescence.

## 6. Unresolved / limits

* `Terminal=true` cannot be observed with the `.out` probe on this host (X13): `xdg-terminal-exec`
  is first in `known_terminals` (gdesktopappinfo.c:2766) and it fails with no `DISPLAY`/
  `WAYLAND_DISPLAY`. The argv shape was confirmed with a **fake** `xdg-terminal-exec` placed first
  on `PATH` inside the case root (`ab01`); the real terminal's own failure is not reproducible
  without a display server.
* `%F`/`%U` with a URI whose *fragment* survives: measured for a **non-local** URI
  (`d03`: `http://example.com/x#frag` => the URI with its fragment). For a local file the fragment
  is dropped before expansion (R14).
* `X-GIO-NoFuse` is read at 2021 but the key is **not** in the case-file schema
  (`desktop:{Name,Icon,Type,Exec,Path,Terminal,Hidden}`), so X9 is reachable in GIO but not
  expressible in a frozen case as the schema stands.
* `gio launch` uses `g_key_file_load_from_file` **and** `g_desktop_app_info_new_from_filename`
  (two parses of the same file); only the second's verdict reaches the model. The first exists for
  a better message (`gio-tool-launch.c:88-97`) and is what produces `Unable to load '...': Key file
  contains line ...` (`t08`).
* The `%` walk applies to the **whole** `Exec` line, so a `%` inside the substituted `{probe}`
  path corrupts the program path (X23). Case roots must not contain `%`.
* Not measured (out of scope, read-only): whether `gio launch` under a D-Bus session bus takes the
  `g_desktop_app_info_launch_uris_with_dbus` path (gdesktopappinfo.c:3412-3443) instead of the
  spawn path - that would change *whether a process starts*, not the argv.

## 7. Tooling

No tool was installed or upgraded: the whole investigation used the already-present `python3`
(3.14.8, stdlib only), `/usr/bin/gio` (glib2 2.90.1-1), `curl`, and `sha256sum`. No `pacman`
transaction was run (all `pacman` transactions are PAUSED host-wide). No host application was
launched: the only children were case roots' own `probe.sh` files, spawned by `gio` under the seat's
scratch dir.

**Scratch**: `S=$HYAKU_SCRATCH/mado-r98/R98MScoutExec` = `/fast/scratch/hyaku/mado-r98/R98MScoutExec`
(explicitly passed to every fixture driver; no inherited `TMPDIR` relied on). The scratch dir is
removed before this seat yields.

## 8. What the L1 should change before the freeze

1. **Rule 2**: state that the byte after `%` is consumed as the selector (R8) - otherwise `100% done`
   and `a%1b` are modelled wrongly.
2. **Rule 3**: split `%f`/`%d`/`%n` from `%u`/`%U` (NULL value => nothing emitted); state that a
   non-local URI under `%F`/`%D`/`%N` is consumed and **dropped**; state the separator is emitted
   only after a non-NULL expansion; add `X-GIO-NoFuse`; state that `%i` quotes the
   **extension-stripped, locale-resolved** `Icon`; state that `%c`/`%k` use the locale string and
   the canonicalized path.
3. **Rule 4**: say "the URI-list head pointer is unchanged", not "the walk consumed no argument".
4. **Rule 6**: state the launch count as "each iteration consumes as many URIs as its codes
   consume; the loop repeats while URIs remain" (so `%f %f` + 3 => 2 launches).
5. **The oracle**: replace the shared-append + 200 ms-quiescence reader with **per-child files**
   (or one atomic write per record plus an expected-count wait), and grade the argv as an
   **unordered multiset** unless spawn order is made observable. As written, the frozen labels are
   not reproducible (S5).
6. **The refusal test**: evaluate "writes no `.out`" **after** the wait, not at `gio`'s exit.
7. **The class list**: add the reachable classes of S4 (X1-X22), at minimum the multi-launch one
   (X1) and the ones whose answer is not a per-URI quote-and-join (X4, X6, X7, X9, X10, X11,
   X13, X17, X18, X19, X21), plus the refusal shapes (X5, X14, X15, X22).
