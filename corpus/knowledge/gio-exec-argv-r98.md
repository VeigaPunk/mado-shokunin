source: S528 (GLib 2.90.1 gdesktopappinfo.c 8e9ce1a8327a2daf6bc16e8dcfb653c482afde7bebc2ca2621747626b5495b0d, 163369 B, 5356 L - new scope on the file S504 holds: the launch-argv expansion at :2506-2746 and the spawn loop at :3003-3186), S529 (GLib 2.90.1 gshell.c 640a0d0fbc9c50d0c70eb8f9ff2c4994392515c6174f76ade9292d7500e60442, 21464 B, 730 L - new scope on the file S506 holds: g_shell_quote at :200-235 and tokenize_command_line at :434-612), S530 (Desktop Entry Specification, "The Exec key", https://specifications.freedesktop.org/desktop-entry/latest/exec-variables.html 2c50a9e427b295928d2b05a19049ab74db18e5d11567c0bd14a8f0f70635277e, 17153 B, HTTP 200 after the documented 301 from the desktop-entry-spec locator), S531 (`gio(1)` GLib 2.90.1 manual, `/usr/share/man/man1/gio.1.gz` container 810077be12cf2df5006db1e1b9b967f6c505930033c68aa9cfc964281906a565, 4961 B, decompressed 84b3cdad868feecd69f113b789d7009113e16531b67d750cd0e424ba2bcb8bc5, 18793 B, 781 L - new scope on the page S527 holds: the `launch` command at page line 218), S504 (held; the desktop-file load gate at gdesktopappinfo.c:1893-2097, already that row's scope)
verified-at: 2026-11-07 - `glib2 2.90.1-1`; the oracle `/usr/bin/gio` sha256 d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462, `gio --version` 2.90.1; the three fetched files re-hashed in this seat's scratch against the L1 receipt (`receipts/sources-open-r98.txt`) and matching byte for byte. The 75 rows of section 12 are this seat's read-only runs of that binary over desktop files and probe children built under `/fast/scratch/hyaku/mado-r98/R98MScribe`; no host application was started and no host file was read by any probe.
recheck: 180d - re-pull `gdesktopappinfo.c` and `gshell.c` at the next GLib tag that changes either (2.90.1 is the pin), and re-open the Exec section of the spec at its current locator; also when `glib2` leaves 2.90.1-1 or the `gio` CLI's `launch` spelling moves. A change to the `%` walk, the `force_file_uri` switch, the `while (dup_uris != NULL)` loop, `g_shell_quote`'s single-quote rule or the tokenizer's `#` rule flips this entry.
covers: the **sequence of argv vectors** GIO 2.90.1 builds and spawns from one desktop file's `Exec` key and a list of file/URI arguments - the load gate that decides whether a desktop file is launchable at all; the byte walk that replaces `%X`; the twelve named field codes and `%%` with what each appends and how many arguments it consumes; `force_file_uri` and `X-GIO-NoFuse`; the no-substitution `%f` append; the iteration rule that spawns once per URI for the single-consuming codes and once in total for `%F`/`%U`; `g_shell_quote`'s always-single-quote form; the `g_shell_parse_argv` tokenizer and unquoter; the five refusal shapes and the exit status the CLI gives them; the spec-vs-implementation deltas; and the named limits.

# The launch argv GIO 2.90.1 builds from a desktop entry's Exec key

Rounds 91-97 answered *which* MIME type and *which* application. This entry answers the next
question in the same chain: given a desktop file and a list of arguments, **what does GIO hand to
`execve`, and how many times**? The answer is not one argv: `expand_application_parameters`
(`gdesktopappinfo.c:2700-2746`) is called inside a `do { } while (dup_uris != NULL)` loop
(`:3007-3186`), so a single-consuming field code produces **one spawn per argument**. The surface
this entry models is therefore the *sequence* of argv vectors, not a single vector.

Line numbers are `gdesktopappinfo.c` (`:2506-2746`, `:3003-3186`) and `gshell.c` (`:56-235`,
`:434-730`) as named in the front matter. Spec line numbers are those of the rendering described in
section 1.3. Every behavioural statement carries a located line of one of the three fetched files,
a located line of the manual, or a probe row of section 12.

## 1. Question and scope

### 1.1 The surface

- **What is read.** `gio launch DESKTOP-FILE [FILE-ARG...]` (`gio.1` page line 218:
  `\fBlaunch\fP \fIDESKTOP\-FILE\fP [\fIFILE\-ARG\fP...]`) loads the desktop file, builds an argv
  from `Exec`, and spawns. The manual's own sentence is `Launch a desktop file from any location
  given.` (`gio.1:221`) and `The \fBlaunch\fP command extends the behavior of the \fBopen\fP
  command by` (`gio.1:223`).
- **What is modelled.** The `[Desktop Entry]` read that gates launchability (section 2), the byte
  walk over `Exec` (section 3), the field-code table (section 4), `force_file_uri` (section 5),
  the no-substitution append (section 6), `g_shell_quote` (section 7), the tokenizer and unquoter
  (section 8), the refusal shapes (section 9), and the spawn loop that turns one expansion into a
  sequence of vectors (section 3.3).
- **What is out of scope.** Whether the process then starts, and whether a portal answers instead,
  stays frontier: `notify_desktop_launch` (`:3173-3178`) and the D-Bus activation path
  (`:3431-3437`) are read only far enough to say when they are taken (section 13).

### 1.2 Evidence class

Sections 2-10 carry located source lines. Section 12 carries the oracle's answers on fixtures this
draft builds from the entry's own recipe. Section 13 names the limits. No cell of this draft is a
number the C1 counter will print - those are the L1's receipt.

### 1.3 The spec rendering

`exec-variables.html` is quoted by line number of a rendering produced as: strip `<script>` and
`<style>` blocks, strip all remaining tags, unescape HTML entities, drop blank lines, number from 1.
That rendering is 121 lines. The method is stated so a reader can reproduce the numbers from the
fetched bytes; the page's own anchors are not used.

## 2. The desktop-file read

`g_desktop_app_info_load_file` (`:2098-2113`) calls `g_key_file_load_from_file` (`:2108`) and then
`g_desktop_app_info_load_from_keyfile` (`:2109`). A `FALSE` return makes
`g_desktop_app_info_new_from_filename_unlocked` clear the object (`:1060-1061`), so the caller sees
"no application". `gio launch` reports that as a **load** refusal (section 9.1).

### 2.1 The gate, in order

| # | test | line | quote | effect on failure |
|---|---|---|---|---|
| 1 | the key file parses | `:2108` | `if (g_key_file_load_from_file (key_file, self->filename, G_KEY_FILE_NONE, NULL))` | load refusal |
| 2 | the start group is `[Desktop Entry]` | `:1906` | `if (start_group == NULL \|\| strcmp (start_group, G_KEY_FILE_DESKTOP_GROUP) != 0)` | load refusal |
| 3 | `Type` is `Application` | `:1917` | `if (type == NULL \|\| strcmp (type, G_KEY_FILE_DESKTOP_TYPE_APPLICATION) != 0)` | load refusal |
| 4 | `Path` is readable | `:1928` | `if (is_invalid_key_error (local_error))` | load refusal |
| 5 | `TryExec` is readable | `:1939` | `if (is_invalid_key_error (local_error))` | load refusal |
| 6 | `TryExec`, if set, resolves | `:1951-1952` | `t = GLIB_PRIVATE_CALL (g_find_program_for_path) (try_exec, NULL, path);` | load refusal |
| 7 | `Exec` is readable | `:1965` | `if (is_invalid_key_error (local_error))` | load refusal |
| 8 | the **raw** `Exec` parses | `:1978` | `if (!g_shell_parse_argv (exec, &argc, &argv, NULL))` | load refusal |
| 9 | `argv[0]` of the raw `Exec` resolves | `:1993` | `t = GLIB_PRIVATE_CALL (g_find_program_for_path) (argv[0], NULL, path);` | load refusal |

`is_invalid_key_error` (`:1886-1891`) is the reason a **missing** key is not a load failure:
`!g_error_matches (error, G_KEY_FILE_ERROR, G_KEY_FILE_ERROR_KEY_NOT_FOUND)` (`:1890`). A missing
`Exec` therefore loads, and refuses later at expansion (section 9.2, probe `noexec`).

### 2.2 The keys the expansion reads

| key | line | quote | used by |
|---|---|---|---|
| `Name` | `:2007` | `info->name = g_key_file_get_locale_string (key_file, G_KEY_FILE_DESKTOP_GROUP, G_KEY_FILE_DESKTOP_KEY_NAME, NULL, NULL);` | `%c` |
| `Icon` | `:2013` | `info->icon_name =  g_key_file_get_locale_string (key_file, G_KEY_FILE_DESKTOP_GROUP, G_KEY_FILE_DESKTOP_KEY_ICON, NULL, NULL);` | `%i` |
| `Path` | `:2018` | `info->path = g_steal_pointer (&path);` | the child's cwd (section 13.2) |
| `Terminal` | `:2019` | `info->terminal = g_key_file_get_boolean (key_file, G_KEY_FILE_DESKTOP_GROUP, G_KEY_FILE_DESKTOP_KEY_TERMINAL, NULL) != FALSE;` | the terminal prepend (section 13.3) |
| `X-GIO-NoFuse` | `:2021` | `info->no_fuse = g_key_file_get_boolean (key_file, G_KEY_FILE_DESKTOP_GROUP, "X-GIO-NoFuse", NULL) != FALSE;` | `force_file_uri` (section 5) |
| `Hidden` | `:2022` | `info->hidden = g_key_file_get_boolean (key_file, G_KEY_FILE_DESKTOP_GROUP, G_KEY_FILE_DESKTOP_KEY_HIDDEN, NULL) != FALSE;` | **nothing on this path** (section 10.3) |
| `DBusActivatable` | `:2026` | `bus_activatable = g_key_file_get_boolean (key_file, G_KEY_FILE_DESKTOP_GROUP, G_KEY_FILE_DESKTOP_KEY_DBUS_ACTIVATABLE, NULL);` | `app_id` (section 13.4) |

`Name` and `Icon` are read with `g_key_file_get_locale_string`, so a localized `Name[xx]` wins when
the locale matches; the probe rows of section 12 ran under `LC_ALL=C` and read the plain key.

### 2.3 The key-file value unescape happens before any of this

`Exec` reaches the expansion as a **GKeyFile-decoded string**, not as the file's bytes. Measured
(section 12, rows `q_back2`, `q_back3`, `esc_z`, `esc_colon`, `esc_dq`, `esc_n`, `esc_t`):

| file bytes in `Exec` | accepted | decoded value | resulting argv |
|---|---|---|---|
| `a\\ b` | yes | `a\ b` | `a b` (one argument) |
| `a\sb` | yes | `a b` | `a`, `b` (two arguments) |
| `a\nb` | yes | `a` LF `b` | `a`, `b` |
| `a\tb` | yes | `a` TAB `b` | `a`, `b` |
| `a\zb` | **no** | - | load refusal |
| `a\:b` | **no** | - | load refusal |
| `"a\"b"` | **no** | - | load refusal |

So the two layers are: GKeyFile unescape (`\s \n \t \r \\` only, everything else refused), then
`g_shell_parse_argv`. A desktop file that wants one argument containing a space writes `a\\ b`.
This is the mechanism behind spec line 27-34 (`the backslash character can be escaped as ("\\") as
well and that this escape rule is applied before the quoting rule`), and it is why the spec's
"four successive backslash characters" sentence exists. The unescape belongs to the key-file reader
(S514's scope, whose bytes this seat did not re-read); this entry states it only from the probe rows
above.

## 3. The `%` walk

### 3.1 The loop

```
while (*p)
  {
    if (p[0] == '%' && p[1] != '\0')
      {
        expand_macro (p[1], expanded_exec, info, uris);
        p++;
      }
    else
      g_string_append_c (expanded_exec, *p);
    p++;
  }
```
(`:2722-2733`)

Two consequences, both measured:

- `if (p[0] == '%' && p[1] != '\0')` (`:2724`) - a `%` that is the **last byte** fails the second
  test and is copied literally by the `else` branch (`:2729-2730`). Probe `pct_trail`:
  `Exec={probe} 100%` gives one argument `100%`.
- The walk consumes **two bytes** per field code (`p++` inside, `p++` at the bottom) and **one**
  byte otherwise. Expansion is textual: the result is a single string, and only then is it parsed.

### 3.2 Every byte not consumed by a field code is copied

`g_string_append_c (expanded_exec, *p);` (`:2730`). That includes `%` when it is the last byte,
and it includes the whole of a quoted region - the walk has no notion of quoting. This is why a
field code inside a quoted argument still expands (section 10.5).

### 3.3 The expansion runs once per iteration of a spawn loop

`expand_application_parameters` is called at `:3018` inside:

```
  dup_uris = uris;
  do
    {
      ...
      old_uris = dup_uris;
      if (!expand_application_parameters (info, exec_line, &dup_uris, &argc, &argv, error))
        goto out;
      ...
    }
  while (dup_uris != NULL);
```
(`:3007-3186`, the loop tail at `:3186`)

`expand_macro` advances the caller's list pointer (`*uri_list = uris;` at `:2697`), so each
iteration starts from the first **unconsumed** argument and rebuilds the whole string from the
`Exec` text. The iteration rule that follows:

| Exec shape | arguments consumed per iteration | spawns |
|---|---|---|
| no field code, or only non-consuming codes (`%i` `%c` `%k` `%%`, or an unknown `%X`) | 1 (by the section 6 append) | one per argument |
| one single-consuming code (`%f` `%u` `%d` `%n`) | 1 | one per argument |
| `k` single-consuming codes | `k` | ceil(n/k) |
| a list code (`%F` `%U` `%D` `%N`) | all remaining | 1 |

Measured instances: `plain2` (2 spawns), `f3` (3), `ff3` (2 spawns: 2 arguments then 1), `F3`
(1 spawn, 3 arguments), `iargs` (2 spawns), `fmix` (2 spawns, the second with an empty tail).

`g_assert (argc > 0);` at `:3064` is the invariant every iteration must satisfy: an expansion that
parses to zero tokens is a programming error, not a refusal. The measured way to reach an argv with
no arguments is therefore a **non-empty** first token plus a field code that contributes nothing
(`f0`, `F0`, `bad_z`, `d_http`).

## 4. The field-code table

`expand_macro` (`:2579-2698`) is one `switch` on the code byte with thirteen arms - `u f d n U F D
N i c k m %` - and no `default:`. An unlisted code therefore contributes nothing and is not an
error, the opposite of spec line 45-48 (`Command lines that contain a field code that is not listed
in this` / `specification are invalid and must not be processed`). `grep -c "case 'v'"
gdesktopappinfo.c` is 0, so the spec's `%v` (`:108-109`) has no arm at all and behaves like an
unlisted code.

| code | line | what it appends | consumes | measured example (row) |
|---|---|---|---|---|
| `%f` | `:2622-2627` | `g_shell_quote` of the URI's **local path**; nothing when the URI has no local path | 1 | `f1`: `['<root>/files/one.txt']` |
| `%F` | `:2639-2657` | the same, for every remaining URI, space-joined | all | `F3`: one spawn, 3 arguments |
| `%u` | `:2619-2627` | the **path** when the URI is local and has no `#`, else `g_shell_quote (uri)` | 1 | `ufile`: `['<root>/files/one.txt']`; `uhttp`: `['http://example.com/a?b=c']` |
| `%U` | `:2638-2657` | the same, for every remaining URI | all | `Umix`: `['<root>/files/one.txt', 'http://example.com/x']` |
| `%d` | `:2528-2537` | `g_path_get_dirname` of the local path, quoted; nothing when there is no local path | 1 | `d1`: `['<root>/files']` |
| `%D` | `:2528-2537` | the same, for every remaining URI, space-joined; **no de-duplication** | all | `D2`: `['<root>/files', '<root>/files']` |
| `%n` | `:2538-2547` | `g_path_get_basename` of the local path, quoted | 1 | `n1`: `['one.txt']` |
| `%N` | `:2538-2547` | the same, for every remaining URI | all | not measured separately; `%N` shares `expand_macro_single`'s arm with `%n` (`:2538-2539`) and `expand_macro`'s loop with `%D` (`:2641`) |
| `%i` | `:2661-2669` | `"--icon "` then `g_shell_quote (Icon)`; nothing when `Icon` is unset | 0 | `i_icon`: `['--icon', 'my-icon']`; `i_noicon`: `[]` |
| `%c` | `:2671-2678` | `g_shell_quote (Name)`; nothing when `Name` is unset | 0 | `c_name`: `['Case c_name']`; `noname`: `[]` |
| `%k` | `:2680-2687` | `g_shell_quote (info->filename)` | 0 | `k_path`: `['<root>/app.desktop']` |
| `%m` | `:2689-2690` | nothing (`case 'm': /* deprecated */`) | 0 | not measured separately: the arm is empty and `%m` shares the no-substitution path with `%i` |
| `%%` | `:2692-2694` | one `%` (`g_string_append_c (exec, '%');`) | 0 | `pct`: `['%', 'done']` |
| `%v` | no arm | nothing | 0 | not measured separately: `grep -c "case 'v'"` over the file is 0 |
| any other `%X` | no arm | nothing | 0 | `bad_z`: `[]`; `bad_q`: `['ab']` |

Two details the table cannot show:

- `%f`/`%F` append **nothing** when `g_file_get_path` returns NULL (`:2524-2526`), i.e. for a
  non-local URI. Probe `fhttp` (`%f` with `http://example.com/x`) gives an argv of zero arguments;
  probe `fmix` shows the same inside a sequence: the second spawn has an empty tail.
- No code tests whether the path exists. `expand_macro_single` (`:2506-2554`) calls only
  `g_file_new_for_uri` and `g_file_get_path`; the rows `f_in_arg_quotes` and `F_in_arg_quotes` pass
  paths that were never created and the expansion still emits them.
- `%d`/`%D`/`%n`/`%N` have the same NULL guard (`:2530-2532`, `:2540-2542`), so they too contribute
  nothing for a non-local URI (`d_http`, `n_http`).

## 5. `force_file_uri` and the `#` rule

`expand_macro` sets a second macro letter for `%u`/`%U` before dispatching:

```
  force_file_uri_macro = macro;
  force_file_uri = FALSE;
  if (!info->no_fuse)
    {
      switch (macro)
        {
        case 'u':
          force_file_uri_macro = 'f';
          force_file_uri = TRUE;
```
(`:2598-2606`, `%U` at `:2608-2610`)

`expand_macro_uri` (`:2556-2577`) then decides:

```
  if (!force_file_uri ||
      /* Pass URI if it contains an anchor */
      strchr (uri, '#') != NULL)
    {
      expanded = expand_macro_single (macro, uri);
    }
  else
    {
      expanded = expand_macro_single (force_file_uri_macro, uri);
      if (expanded == NULL)
        expanded = expand_macro_single (macro, uri);
    }
```
(`:2563-2574`)

Read as a rule:

1. `force_file_uri` is TRUE only for `%u`/`%U` and only when `X-GIO-NoFuse` is unset
   (`if (!info->no_fuse)` at `:2600`). Every other code takes the first branch and expands itself.
2. With `force_file_uri` set, the `#` test runs **on the URI string**. A `#` sends the URI down the
   first branch, where `expand_macro_single ('u', uri)` appends the URI itself.
3. Otherwise the path form is tried first (`force_file_uri_macro` = `f`/`F`), and the URI form is
   the fallback when the path is NULL (`:2571-2573`).

**The `#` branch is not observable through `gio launch`.** The CLI converts each command-line
argument to a `GFile` before building the URI list, and a `file:` URI's fragment does not survive
that conversion: probe `uanchor` passes `file://<root>/files/one.txt#frag` to `%u` and the child
receives `<root>/files/one.txt` - the *path*, which is the branch `strchr` did **not** take. A
non-local URI keeps its fragment (`uhttp_frag` passes `http://example.com/x#frag` and the child
receives `http://example.com/x#frag`), but for a non-local URI both branches agree anyway, because
`g_file_get_path` is NULL and the fallback at `:2573` returns the URI. So the `#` test is a real
rule of the library and a **named limit** of this model (section 13.1).

`X-GIO-NoFuse` is observable and is the only way to make `%u` emit a URL for a local file: probe
`ufile_nofuse` sets `X-GIO-NoFuse=true` and `%u` yields `file://<root>/files/one.txt` where `ufile`
yields the path.

The comment above the switch explains the intent: `On %u and %U, pass POSIX file path pointing to
the URI via` / `the FUSE mount in ~/.gvfs.` (`:2593-2594`). On a host with no gvfs mount the path
form is the URI's own path, which is what every probe row shows.

## 6. The no-substitution `%f` rule

```
  /* No file substitutions */
  if (uri_list == *uris && uri_list != NULL)
    {
      /* If there is no macro default to %f. This is also what KDE does */
      g_string_append_c (expanded_exec, ' ');
      expand_macro ('f', expanded_exec, info, uris);
    }
```
(`:2735-2741`)

`uri_list` is the list pointer captured **before** the walk (`:2708`) and `*uris` is the pointer
after it. The condition is therefore "the walk consumed nothing **and** there is at least one
argument". Both halves matter:

- A trailing space is appended before the expansion (`:2739`), so the appended value is always a
  separate token even when `Exec` ends inside a word.
- Only the **first** argument is used, because the appended macro is `f`, not `F`. The remaining
  arguments are left to the spawn loop, which re-runs the whole expansion for each of them.

Measured: `plain1` (one argument, one spawn, the path appended after `one two`), `plain2` (two
arguments, two spawns), `iargs` (the `%i` expansion plus the appended `%f`, two spawns), `c_arg2`,
`k_arg2`, `pct_arg2`.

The rule fires for every non-consuming code, which is why `%i`, `%c`, `%k`, `%%` and an unknown
`%X` all behave like `%f` when arguments are present.

## 7. `g_shell_quote`

```
  /* We always use single quotes, because the algorithm is cheesier.
```
(`gshell.c:202`)

```
  dest = g_string_new ("'");
```
(`:212`)

```
      /* Replace literal ' with a close ', a \', and an open ' */
      if (*p == '\'')
        g_string_append (dest, "'\\''");
```
(`:221-223`)

```
  /* close the quote */
  g_string_append_c (dest, '\'');
```
(`:230`)

So the output is always `'` + the value with each `'` replaced by `'\''` + `'`. The function's own
comment says the style is not part of the contract - `The quoting style used is undefined (single
or double quotes may be` / `used).` - but 2.90.1's implementation is single-quote only, and every
measured value goes through it: `q_apos_name` (`Name=it's mine` gives one argument `it's mine`),
`q_apos_icon` (`Icon=it's` gives `--icon`, `it's`), `ufile2` (`two words.txt` stays one argument).

`g_shell_quote` is applied to **every** substituted value: the URI (`:2520`), the path (`:2526`),
the dirname (`:2534`), the basename (`:2544`), the icon (`:2665`), the name (`:2674`) and the
filename (`:2683`). Nothing else in the expansion quotes anything - the `Exec` text's own quoting is
the file author's (`:2729-2730` copies it byte for byte).

## 8. The `g_shell_parse_argv` grammar

`res = g_shell_parse_argv (expanded_exec->str, argc, argv, error);` (`gdesktopappinfo.c:2743`).
The parser is `tokenize_command_line` (`gshell.c:434-612`) followed by one `g_shell_unquote` per
token (`:696`).

### 8.1 The tokenizer

| input | rule | line | quote |
|---|---|---|---|
| space, TAB | split; a run of blanks is discarded | `:503-516` | `/* discard all unquoted blanks (don't add them to a token) */` |
| LF | split | `:499-501` | `case '\n':` |
| `'` | enter single-quote state; the quote byte is kept in the token | `:524-527` | `current_quote = *p;` |
| `"` | enter double-quote state; the quote byte is kept | `:524-527` | same arm |
| `\` outside quotes | escape the next byte; both bytes are kept for the unquoter | `:530-532` | `current_quote = *p;` |
| `\` + LF | both dropped | `:451-454` | `/* we append nothing; backslash-newline become nothing */` |
| `#` at the very first byte, or after space/LF/NUL | comment to end of line | `:534-545` | `/* '#' was the first char */` |
| `#` anywhere else | an ordinary byte | `:547-550` | `g_string_append_c (current_token, *p);` |
| any other byte | appended to the current token | `:554-559` | `/* Combines rules 4) and 6) - if we have a token, append to it,` |

### 8.2 The unquoter

`unquote_string_inplace` (`:65-176`) is called on each token that begins with a quote.

- Single quotes: `Single quotes preserve the literal string exactly. escape` / `sequences are not
  allowed; not even \'` (`:56-57`). The scan stops at the first `'` (`:148-155`).
- Double quotes: `Double quotes allow $ ` " \ and newline to be escaped with backslash.` (`:60`).
  Only `"`, `\`, `` ` ``, `$` and LF lose the backslash (`:113-121`); any other `\x` keeps the
  backslash (`:123-128`).
- A token that does not begin with a quote is copied unchanged.

### 8.3 The errors

| condition | error | line | quote |
|---|---|---|---|
| text ends inside `'` or `"` | `G_SHELL_ERROR_BAD_QUOTING` | `:595` | `_("Text ended before matching quote was found for %c."` |
| text ends just after `\` | `G_SHELL_ERROR_BAD_QUOTING` | `:579` | `if (current_quote == '\\')` |
| the whole input is empty or blank | `G_SHELL_ERROR_EMPTY_STRING` | `:590` | `_("Text was empty (or contained only whitespace)"));` |
| a token does not start with a quote when one is required | `G_SHELL_ERROR_BAD_QUOTING` | `:174` | `_("Unmatched quotation mark in command line or other shell-quoted text"));` |

`g_shell_parse_argv` also refuses a zero-token result (`:602-608`) and asserts a non-empty vector on
success (`g_assert (argc > 0);` at `:710`).

### 8.4 What the grammar does not do

`g_shell_parse_argv` performs no expansion at all: `we simply remove quotes, and don't do any field
splitting or` / `empty word removal` (`:685-686`). Globs, `$VAR`, `~` and operators are literal
bytes. This is the same parser the load gate uses on the raw `Exec` (`gdesktopappinfo.c:1978`), so
a desktop file whose `Exec` does not tokenize never loads.

## 9. The refusals

`gio launch` exits **1** for every refusal measured here (`gio.1:775`: `On success, \fB0\fP is
returned, a non\-zero failure code otherwise.`). The manual promises no per-error code, so the
`1` is the CLI's mapping, not a documented contract.

### 9.1 Load refusals - `Unable to load application information`

One message covers gate steps 2-9 of section 2.1. Measured: `notype`, `typelink`, `nogroup`,
`badquote`, `noprog`, `esc_z`, `esc_colon`, `esc_dq`, `i_nospace`, `f_in_quotes`. The key-file
parse failure (gate step 1) has its own message: `garbage` prints `Key file contains line "not a key file at all" which is not a key-value pair, group, or comment`.

### 9.2 Launch refusals - `Unable to launch application`

| shape | line | message (ASCII rendering) | probe |
|---|---|---|---|
| no `Exec` key | `:2713-2717` | `Desktop file didn't specify Exec field` (source apostrophe is U+2019) | `noexec` |
| `Exec=` empty, no arguments | `:2743` | `Text was empty (or contained only whitespace)` | `emptyexec` |
| `Exec=` blank, no arguments | `:2743` | the same | `q_space_only_exec` |
| `Exec=` empty, one argument | `:3066-3094` | `Program '<the argument>' not found in $PATH` | `emptyexec_arg` (argument `<root>/notaprogram`) |

The fourth row is the interesting one: with an empty `Exec` and an argument, the section 6 append
makes the **argument** `argv[0]`, and the program lookup at `:3077-3079` fails on it. The expansion
itself succeeded; the refusal is the spawn path's.

### 9.3 What is *not* a refusal

`Hidden=true` launches. `info->hidden` is read at `:2022` and consulted only where an application is
**added to a list** (`if (info->hidden)` at `:413`, inside the `g_app_info_get_all` family), never
on the launch path. Probe `hidden`: a desktop file with `Hidden=true` spawns the probe with
`['one']`, exit 0. The spec's `Hidden` key is a menu-visibility statement; `gio launch` names the
file explicitly and does not consult it.

## 10. Spec vs implementation deltas

| # | spec says | implementation does | evidence |
|---|---|---|---|
| 10.1 | `%d`, `%D`, `%n`, `%N` are `Deprecated.` (`:85-92`) and `Deprecated field codes should be removed from the command line and` / `ignored.` (`:41-42`) | all four are implemented: dirname and basename, single and list | `d1`, `d2dirs`, `D2`, `n1` |
| 10.2 | `%i` is `expanded as two arguments, first` / `--icon and then the value of the` / `Icon key.` (`:94-96`) | appends the literal text `--icon ` and then the quoted icon; the split into two arguments is the tokenizer's, and the space is part of the appended text | `i_icon`, `i_iconspace`; `noicon_pct_i` shows the surrounding bytes joining when `Icon` is unset |
| 10.3 | `%f` is `A single file name (including the path), even if multiple files are selected.` (`:63`) | one file per spawn: the loop at `:3186` repeats the whole expansion, so "multiple files" means multiple processes, not one process with one file | `f2` (2 spawns), `f3` (3 spawns) |
| 10.4 | `A command line may contain at most one %f, %u, %F or %U field code.` (`:112`) | not enforced: two codes are expanded in order | `ff` (`%f %f`, 2 arguments, 1 spawn), `fF` (`%f %F`, 3 arguments, 1 spawn), `ff3` (`%f %f` with 3 arguments, 2 spawns) |
| 10.5 | `Field codes must not be used inside a quoted argument, the result of` / `field code expansion inside a quoted argument is undefined.` (`:116-117`) | defined: the expansion is textual and precedes parsing, so the `g_shell_quote`d value lands **inside** the token and its single quotes survive literally | `f_in_arg_quotes`: `Exec={probe} "a %f b"` gives one argument `a '<root>/files/one.txt' b`; `u_in_arg_quotes` the same for `%u`; `F_in_arg_quotes` gives `a 'p1' 'p2' b` in one argument |
| 10.6 | `Command lines that contain a field code that is not listed in this` / `specification are invalid and must not be processed` (`:45-46`) | an unlisted code contributes nothing and is not an error | `bad_z` (`%z`), `bad_q` (`a%qb` gives `ab`) |
| 10.7 | `Implementations must take care not to expand field codes into multiple` / `arguments` (`:50-51`) | true for every code: each value is `g_shell_quote`d, so a value with spaces stays one argument | `ufile2`, `F3` (`two words.txt` and `q'uote.txt` each one argument) |
| 10.8 | `Implementations must undo quoting before` / `expanding field codes` (`:19-20`) | the implementation expands **first**, then parses: the walk at `:2722-2733` sees raw bytes including quotes | `q_single`, `q_double` (the quoting is undone by the parser, after expansion); 10.5 is the visible consequence |
| 10.9 | `The name or path of the executable program may not contain the equal` / `sign ("=").` (`:10-11`) | not checked anywhere on this path | no probe: a `=` in `argv[0]` would simply be looked up and not found (`:3077`) |
| 10.10 | local files `may either be passed as` / `file: URLs or as file path` for `%u` (`:78-79`) | the path is chosen whenever the URI has a local path, unless `X-GIO-NoFuse` is set | `ufile` (path), `ufile_nofuse` (`file:` URL) |
| 10.11 | `%v` is `Deprecated.` (`:108-109`) and deprecated codes `should be removed from the command line and` / `ignored.` (`:41-42`) | `%v` has no arm and no explicit skip: it is an unlisted code, so it contributes nothing by falling through the `switch` | `grep -c "case 'v'" gdesktopappinfo.c` = 0; no probe row (the observable result equals `bad_z`'s) |

## 11. The `%` walk, worked

`Exec={probe} %i %f` with `Icon=my-icon` and two files:

1. Iteration 1. The walk copies `{probe} `, meets `%i` (`:2661`), appends `--icon ` and
   `'my-icon'`, copies ` `, meets `%f`, appends `'<file1>'` and advances the list. The no-substitution
   test at `:2736` is false (a URI was consumed). `g_shell_parse_argv` yields
   `[<probe>, --icon, my-icon, <file1>]`. One spawn.
2. Iteration 2. The same text is expanded again from `Exec`, `%i` appends the same two tokens, `%f`
   takes `<file2>`. One spawn.
3. `dup_uris` is now NULL, the loop ends (`:3186`). Two spawns, two vectors.

Measured as `iargs`: two spawns, each `[--icon, my-icon, <one file>]`.

## 12. Measured probes

### 12.1 Method

Every row is one run of

```
env -i LC_ALL=C HOME=<root>/h PATH=/usr/bin:/bin \
  gio launch <root>/app.desktop <arg>...
```

where `<root>` is a case directory this seat built under
`/fast/scratch/hyaku/mado-r98/R98MScribe/cases/<id>`, `app.desktop` is the fixture, and the first
token of `Exec` is `<root>/probe.sh`, mode 0755:

```
#!/bin/sh
out="$0.out"
{ printf 'ARGC=%s\n' "$#"
  i=0
  for a in "$@"; do printf 'A%s=%s\n' "$i" "$a"; i=$((i+1)); done
  printf 'END\n'; } >> "$out"
```

The probe **appends**, so a second spawn is visible as a second `ARGC=` block. `LAUNCHn` below is
the n-th block in that file. In the argv columns `<root>` stands for the case root's absolute path,
which is what the probe recorded; `R` is used for the case root in the Exec column. Every row ran
against `/usr/bin/gio` sha256 `d2164260...c462`, `gio --version` 2.90.1, `glib2 2.90.1-1`.

`rc` is `gio launch`'s exit status. `NO-OUT` means the probe never ran.

### 12.2 No field code (the section 6 append)

| row | Exec | arguments | launches | argv vectors | rc |
|---|---|---|---|---|---|
| `plain0` | `{probe} one two` | - | 1 | `[one, two]` | 0 |
| `plain1` | `{probe} one two` | 1 file | 1 | `[one, two, <root>/files/one.txt]` | 0 |
| `plain2` | `{probe} one two` | 2 files | 2 | `[one, two, <root>/files/one.txt]`; `[one, two, <root>/files/two words.txt]` | 0 |

### 12.3 `%f` and `%F`

| row | Exec | arguments | launches | argv vectors | rc |
|---|---|---|---|---|---|
| `f0` | `{probe} %f` | - | 1 | `[]` | 0 |
| `f1` | `{probe} %f` | 1 file | 1 | `[<root>/files/one.txt]` | 0 |
| `f2` | `{probe} %f` | 2 files | 2 | `[<root>/files/one.txt]`; `[<root>/files/two words.txt]` | 0 |
| `f3` | `{probe} %f` | 3 files | 3 | `[<root>/files/one.txt]`; `[<root>/files/two words.txt]`; `[<root>/files/q'uote.txt]` | 0 |
| `ff` | `{probe} %f %f` | 2 files | 1 | `[<root>/files/one.txt, <root>/files/two words.txt]` | 0 |
| `ff3` | `{probe} %f %f` | 3 files | 2 | `[<root>/files/one.txt, <root>/files/two words.txt]`; `[<root>/files/q'uote.txt]` | 0 |
| `fmix` | `{probe} %f` | file, `http://example.com/x` | 2 | `[<root>/files/one.txt]`; `[]` | 0 |
| `fhttp` | `{probe} %f` | `http://example.com/x` | 1 | `[]` | 0 |
| `F0` | `{probe} %F` | - | 1 | `[]` | 0 |
| `F1` | `{probe} %F` | 1 file | 1 | `[<root>/files/one.txt]` | 0 |
| `F3` | `{probe} %F` | 3 files | 1 | `[<root>/files/one.txt, <root>/files/two words.txt, <root>/files/q'uote.txt]` | 0 |
| `fF` | `{probe} %f %F` | 3 files | 1 | `[one.txt, two words.txt, q'uote.txt]` (all three, in Exec order) | 0 |
| `Fi` | `{probe} %F %i` | 2 files, `Icon=my-icon` | 1 | `[<root>/files/one.txt, <root>/files/two words.txt, --icon, my-icon]` | 0 |

### 12.4 `%u` and `%U`

| row | Exec | arguments | launches | argv vectors | rc |
|---|---|---|---|---|---|
| `ufile` | `{probe} %u` | 1 file | 1 | `[<root>/files/one.txt]` | 0 |
| `ufile2` | `{probe} %u` | 2 files | 2 | `[<root>/files/one.txt]`; `[<root>/files/two words.txt]` | 0 |
| `uhttp` | `{probe} %u` | `http://example.com/a?b=c` | 1 | `[http://example.com/a?b=c]` | 0 |
| `uanchor` | `{probe} %u` | `file://<root>/files/one.txt#frag` | 1 | `[<root>/files/one.txt]` (the fragment is gone) | 0 |
| `uhttp_frag` | `{probe} %u` | `http://example.com/x#frag` | 1 | `[http://example.com/x#frag]` | 0 |
| `ufile_nofuse` | `{probe} %u`, `X-GIO-NoFuse=true` | 1 file | 1 | `[file://<root>/files/one.txt]` | 0 |
| `Umix` | `{probe} %U` | file, `http://example.com/x` | 1 | `[<root>/files/one.txt, http://example.com/x]` | 0 |
| `U0` | `{probe} %U` | - | 1 | `[]` | 0 |

### 12.5 `%d`, `%D`, `%n`

| row | Exec | arguments | launches | argv vectors | rc |
|---|---|---|---|---|---|
| `d1` | `{probe} %d` | 1 file | 1 | `[<root>/files]` | 0 |
| `d2dirs` | `{probe} %d` | 2 files in 2 directories | 2 | `[<root>/files]`; `[<root>/h]` | 0 |
| `D2` | `{probe} %D` | 2 files in one directory | 1 | `[<root>/files, <root>/files]` | 0 |
| `n1` | `{probe} %n` | 1 file | 1 | `[one.txt]` | 0 |
| `d_http` | `{probe} %d` | `http://example.com/x` | 1 | `[]` | 0 |
| `n_http` | `{probe} %n` | `http://example.com/x` | 1 | `[]` | 0 |

### 12.6 `%i`, `%c`, `%k`

| row | Exec | arguments | launches | argv vectors | rc |
|---|---|---|---|---|---|
| `i_icon` | `{probe} %i`, `Icon=my-icon` | - | 1 | `[--icon, my-icon]` | 0 |
| `i_noicon` | `{probe} %i` | - | 1 | `[]` | 0 |
| `i_iconspace` | `{probe} %i`, `Icon=my icon` | - | 1 | `[--icon, my icon]` | 0 |
| `iargs` | `{probe} %i`, `Icon=my-icon` | 2 files | 2 | `[--icon, my-icon, <root>/files/one.txt]`; `[--icon, my-icon, <root>/files/two words.txt]` | 0 |
| `noicon_pct_i` | `{probe} x%iy` | - | 1 | `[xy]` | 0 |
| `c_name` | `{probe} %c` | - | 1 | `[Case c_name]` | 0 |
| `c_arg2` | `{probe} %c` | 1 file | 1 | `[Case c_arg2, <root>/files/one.txt]` | 0 |
| `q_apos_name` | `{probe} %c`, `Name=it's mine` | - | 1 | `[it's mine]` | 0 |
| `noname` | `{probe} %c` (no `Name`) | - | 1 | `[]` | 0 |
| `k_path` | `{probe} %k` | - | 1 | `[<root>/app.desktop]` | 0 |
| `k_arg2` | `{probe} %k` | 1 file | 1 | `[<root>/app.desktop, <root>/files/one.txt]` | 0 |
| `krel` | `{probe} %k`, launched as `./app.desktop` | - | 1 | `[/absolute/<root>/app.desktop]` | 0 |
| `q_apos_icon` | `{probe} %i`, `Icon=it's` | - | 1 | `[--icon, it's]` | 0 |

`krel` is the one row whose value is not `info->filename` verbatim: the property setter stores the
string it is given (`self->filename = g_value_dup_string (value);` at `:1757`), so the absolute path
is the **CLI's** canonicalization of its argument, not a rule of `gdesktopappinfo.c`.

### 12.7 `%%`, a trailing `%`, and unlisted codes

| row | Exec | arguments | launches | argv vectors | rc |
|---|---|---|---|---|---|
| `pct` | `{probe} %% done` | - | 1 | `[%, done]` | 0 |
| `pct_trail` | `{probe} 100%` | - | 1 | `[100%]` | 0 |
| `pct_arg2` | `{probe} %%` | 1 file | 1 | `[%, <root>/files/one.txt]` | 0 |
| `bad_z` | `{probe} %z` | - | 1 | `[]` | 0 |
| `bad_q` | `{probe} a%qb` | - | 1 | `[ab]` | 0 |

### 12.8 Quoting

| row | Exec (file bytes) | arguments | launches | argv vectors | rc |
|---|---|---|---|---|---|
| `q_single` | `'{probe}' one` | - | 1 | `[one]` | 0 |
| `q_double` | `"{probe}" one` | - | 1 | `[one]` | 0 |
| `q_back2` | `{probe} a\\ b` | - | 1 | `[a b]` | 0 |
| `q_back3` | `{probe} a\sb` | - | 1 | `[a, b]` | 0 |
| `q_tab` | `{probe}` TAB `one` | - | 1 | `[one]` | 0 |
| `esc_n` | `{probe} a\nb` | - | 1 | `[a, b]` | 0 |
| `esc_t` | `{probe} a\tb` | - | 1 | `[a, b]` | 0 |
| `f_in_arg_quotes` | `{probe} "a %f b"` | 1 file | 1 | `[a '<root>/files/one.txt' b]` | 0 |
| `u_in_arg_quotes` | `{probe} "a %u b"` | 1 file | 1 | `[a '<root>/files/one.txt' b]` | 0 |
| `F_in_arg_quotes` | `{probe} "a %F b"` | 2 files | 1 | `[a '<root>/files/one.txt' '<root>/files/two.txt' b]` | 0 |

### 12.9 `Path` and `Hidden`

| row | Exec | arguments | launches | observed | rc |
|---|---|---|---|---|---|
| `pathcwd` | `{probe} %f`, `Path=<root>/wd` | 1 file | 1 | probe `PWD=<root>/wd`, `ARGC=1` | 0 |
| `hidden` | `{probe} one`, `Hidden=true` | - | 1 | `[one]` | 0 |

### 12.10 Refusals

| row | desktop file | launches | stderr (ASCII rendering) | rc |
|---|---|---|---|---|
| `garbage` | not a key file | NO-OUT | `gio: Unable to load '<path>': Key file contains line "not a key file at all" which is not a key-value pair, group, or comment` | 1 |
| `nogroup` | `[Other Group]` only | NO-OUT | `gio: Unable to load application information for '<path>'` | 1 |
| `notype` | no `Type` | NO-OUT | the same | 1 |
| `typelink` | `Type=Link` | NO-OUT | the same | 1 |
| `badquote` | `Exec={probe} 'unterminated` | NO-OUT | the same | 1 |
| `noprog` | `Exec=/nonexistent/prog %f` | NO-OUT | the same | 1 |
| `esc_z` | `Exec={probe} a\zb` | NO-OUT | the same | 1 |
| `esc_colon` | `Exec={probe} a\:b` | NO-OUT | the same | 1 |
| `esc_dq` | `Exec={probe} "a\"b"` | NO-OUT | the same | 1 |
| `i_nospace` | `Exec={probe}%i`, `Icon=ico` | NO-OUT | the same | 1 |
| `f_in_quotes` | `Exec="{probe} %f"` | NO-OUT | the same | 1 |
| `noexec` | no `Exec` key | NO-OUT | `gio: Unable to launch application '<path>': Desktop file didn't specify Exec field` | 1 |
| `emptyexec` | `Exec=` | NO-OUT | `gio: Unable to launch application '<path>': Text was empty (or contained only whitespace)` | 1 |
| `q_space_only_exec` | `Exec=   ` | NO-OUT | the same | 1 |
| `emptyexec_arg` | `Exec=`, argument `<root>/notaprogram` | NO-OUT | `gio: Unable to launch application '<path>': Program '<root>/notaprogram' not found in $PATH` | 1 |

`i_nospace` and `f_in_quotes` are load refusals for the reason in section 2.1 step 9: the raw `Exec`
parses to an `argv[0]` that is not an executable file, so the file never becomes an application.
They are the reason a field code cannot be placed inside `argv[0]`'s token.

## 13. Named limits

### 13.1 The `#` branch of `expand_macro_uri`

`strchr (uri, '#') != NULL` (`:2565`) is implemented and is **not observable through `gio launch`**.
The CLI converts each argument to a `GFile` before the URI list exists, and a `file:` URI's fragment
does not survive that conversion (`uanchor` receives the path). A non-local URI keeps its fragment
(`uhttp_frag`) but both branches return the same string for it, because `g_file_get_path` is NULL
and the fallback at `:2573` yields the URI. A model of this surface therefore includes the
`g_file_new_from_commandline_arg` step and may treat the `#` test as unreachable; a caller that
builds the URI list itself (a file manager passing `g_file_get_uri` output) can reach it.

### 13.2 `Path=` is the child's working directory, not part of argv

`info->path` is handed to `g_spawn_async_with_fds` as its working directory
(`if (!g_spawn_async_with_fds (info->path,` at `:3134`) and to
`g_find_program_for_path` as the search directory (`:3077-3079`). Probe `pathcwd` confirms the cwd.
The argv this entry models is unaffected by `Path` except through the program lookup; the model
does not cover the cwd and does not model the lookup's directory argument.

### 13.3 `Terminal=true` prepends a terminal

`if (info->terminal && !prepend_terminal_to_vector (&argc, &argv,` (`:3027`) rewrites `argv` before
the spawn, choosing from a fixed table (`:2766-2777`: `xdg-terminal-exec`, `kgx -e`,
`gnome-terminal --`, `mate-terminal -x`, `xfce4-terminal -x`, `tilix -e`, `konsole -e`, `nxterm -e`,
`color-xterm -e`, `rxvt -e`, `dtterm -e`, `xterm -e`) and failing the launch when none is found
(`:3031-3032`). **Not measured**: the probe would have to start a host terminal, which this seat's
rules forbid. The model does not cover it.

### 13.4 D-Bus activation and the portal path

`g_desktop_app_info_launch_uris_internal` takes the D-Bus branch only when a session bus exists
**and** `info->app_id` is set:

```
  if (session_bus && info->app_id)
    g_desktop_app_info_launch_uris_with_dbus (info, session_bus, uris, launch_context,
                                              NULL, NULL, NULL);
  else
    success = g_desktop_app_info_launch_uris_with_spawn (info, session_bus, info->exec, uris, launch_context,
```
(`:3431-3439`)

`app_id` requires `DBusActivatable=true` **and** a filename whose basename minus `.desktop` is a
valid D-Bus name (`if (bus_activatable && info->filename)` at `:2071`, the `g_dbus_is_name` test at
`:2083`). The D-Bus branch sends no argv at all - it calls `org.freedesktop.Application` on an object
path derived from the app id (`:3341`, `:3354`) - so it is outside this model by construction. Every
probe row ran under `env -i` with no session bus, which is why all of them took the spawn branch.

The portal path is the `#ifdef G_OS_UNIX` block at `:2979-3001`: when the desktop file carries
`X-SnapInstanceName`, the URIs are first offered to `g_document_portal_add_documents` (`:2994`) and
the returned list replaces them. Not measured (it needs a portal and a snap-named desktop file); the
model does not cover it.

### 13.5 `X-GIO-NoFuse`

Modelled as far as section 5 goes (it flips `force_file_uri`), and measured once (`ufile_nofuse`).
The key is GLib-private and appears in no specification; a desktop file that sets it changes what
`%u`/`%U` emit for local files, and nothing else on this path reads it.

### 13.6 Not modelled at all

- Whether the spawned process starts, and what `notify_desktop_launch` (`:3173-3178`) does with it.
- The `gio-launch-desktop` wrapper: `wrapped_argv[0] = g_strdup (gio_launch_desktop_path);`
  (`:3125`) means the process GIO spawns is the wrapper, which then execs the real program. The
  probe sees the real program's argv because the wrapper execs; the model stops at the vector handed
  to `g_spawn_async_with_fds`.
- Startup notification and the environment GIO adds (`GIO_LAUNCHED_DESKTOP_FILE` at `:3037-3040`,
  `DESKTOP_STARTUP_ID`/`XDG_ACTIVATION_TOKEN` at `:3054-3055`).
- `TryExec`'s effect beyond the load gate (section 2.1 step 6).
- Locale selection for `%c`: the rows ran under `LC_ALL=C`.
