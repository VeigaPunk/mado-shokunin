# round-98 SOURCES rows - the C1 launch-argv surface

Draft for the L1. Four new rows (S528-S531) and one held-row `used-by` append (S504). Nothing here
is landed; the L1 lands it through the lane helper.

Id placeholders are S528-S531 (the registry's highest id at base `35f3ce80` is S527). Every digest
below was re-measured in this seat's scratch against the L1's receipt
`.ufo/waves/round-98/receipts/sources-open-r98.txt` and matches it byte for byte:

```
8e9ce1a8327a2daf6bc16e8dcfb653c482afde7bebc2ca2621747626b5495b0d  gdesktopappinfo.c  163369 B  5356 L
640a0d0fbc9c50d0c70eb8f9ff2c4994392515c6174f76ade9292d7500e60442  gshell.c            21464 B   730 L
2c50a9e427b295928d2b05a19049ab74db18e5d11567c0bd14a8f0f70635277e  exec-variables.html 17153 B   121 rendered L
810077be12cf2df5006db1e1b9b967f6c505930033c68aa9cfc964281906a565  gio.1.gz             4961 B
84b3cdad868feecd69f113b789d7009113e16531b67d750cd0e424ba2bcb8bc5  gio.1 (decompressed) 18793 B  781 L
```

## 1. The four rows, in registry form

Each line is one table row: 11 columns, no `|` inside a cell, ASCII only.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S528 | GLib 2.90.1 launch-argv expansion - https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gdesktopappinfo.c (sha256 8e9ce1a8327a2daf6bc16e8dcfb653c482afde7bebc2ca2621747626b5495b0d, 163369 B, HTTP 200 at the recorded URL; the same file S504 holds, new scope, census W04 expected); host package glib2 2.90.1-1, /usr/bin/gio sha256 d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462 | code | A | how GIO builds and spawns the launch argv from a desktop entry's Exec key: the load gate, the % walk, the twelve field codes, force_file_uri, the no-substitution %f append, and the do-while that spawns once per URI | gdesktopappinfo.c:2506-2554 (expand_macro_single), 2556-2577 (expand_macro_uri; :2565 the '#' test), 2579-2698 (expand_macro; :2600 no_fuse, :2604-2610 force_file_uri, :2689 %m, :2692 %%), 2700-2746 (expand_application_parameters; :2724 the walk, :2735-2741 the no-substitution append, :2743 g_shell_parse_argv), 3007-3186 (the do-while; :3186 the loop tail), 1893-2097 (the load gate; :1906 group, :1917 Type, :1978 raw parse, :1993 argv[0] lookup, :2021 X-GIO-NoFuse, :2022 Hidden); sha256 8e9ce1a8...b0d, 163369 B, 5356 L | the argv sequence GIO spawns from Exec and its arguments: which code consumes how many, what each appends, and how many processes result | mined | 2026-11-07 | 180d | corpus/knowledge/gio-exec-argv-r98.md |
| S529 | GLib 2.90.1 shell quoting and tokenizer - https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gshell.c (sha256 640a0d0fbc9c50d0c70eb8f9ff2c4994392515c6174f76ade9292d7500e60442, 21464 B, HTTP 200 at the recorded URL; the same file S506 holds, new scope, census W04 expected); host package glib2 2.90.1-1 | code | A | g_shell_quote's always-single-quote form and the g_shell_parse_argv grammar the expanded Exec is parsed by: the tokenizer's quote, backslash, whitespace and '#' rules, the unquoter's two quote states, and the four error shapes | gshell.c:200-235 (g_shell_quote; :202 the single-quote comment, :212 the opening quote, :221-223 the quote replacement, :230 the close), 56-62 (the two quote states), 65-176 (unquote_string_inplace), 434-612 (tokenize_command_line; :453 backslash-newline, :469 the comment scan, :534-545 the '#' rule, :583-597 the errors), 658-730 (g_shell_parse_argv; :672 the tokenizer call, :696 the per-token unquote, :710 the argc assert); sha256 640a0d0f...442, 21464 B, 730 L | how the expanded Exec string becomes argv: which bytes split, which quote states preserve, which escapes survive, and which four inputs are errors | mined | 2026-11-07 | 180d | corpus/knowledge/gio-exec-argv-r98.md |
| S530 | Desktop Entry Specification, "The Exec key" - https://specifications.freedesktop.org/desktop-entry/latest/exec-variables.html (sha256 2c50a9e427b295928d2b05a19049ab74db18e5d11567c0bd14a8f0f70635277e, 17153 B, HTTP 200; the S523/S525 pattern: the locator .../desktop-entry-spec/latest/exec-variables.html answers 301 to it) | spec | A | the documented Exec contract: quoting and reserved characters, the field-code list with %f/%F/%u/%U/%d/%D/%n/%N/%i/%c/%k/%v/%m, the at-most-one rule, the no-field-code-inside-quotes rule, and the once-only expansion rule | exec-variables.html rendered lines 12-26 (quoting and reserved characters), 27-34 (the backslash escape applied before quoting), 38-40 (the % + alpha form and %%), 41-42 (deprecated codes), 43-44 (expanded once), 45-48 (unlisted codes invalid), 50-54 (one argument per value), 63 (%f), 72-76 (%F), 77-79 (%u), 80-84 (%U), 85-92 (%d %D %n %N deprecated), 93-99 (%i two arguments), 100-107 (%c, %k), 112 (at most one), 116-118 (not inside quotes; %F/%U/%i alone); rendering: tags stripped, entities unescaped, blank lines dropped, 121 lines | the documented Exec rules this implementation departs from: deprecated codes, the one-code limit, quoting order, and the undefined quoted-field-code case | mined | 2026-11-07 | 180d | corpus/knowledge/gio-exec-argv-r98.md |
| S531 | `gio(1)` manual, GLib 2.90.1, `launch` command - file:///usr/share/man/man1/gio.1.gz (installed page: no HTTP status exists for a `file://` locator, `curl -w '%{http_code}'` reports 000; container sha256 810077be12cf2df5006db1e1b9b967f6c505930033c68aa9cfc964281906a565, 4961 B; decompressed sha256 84b3cdad868feecd69f113b789d7009113e16531b67d750cd0e424ba2bcb8bc5, 18793 B, 781 lines; owner `pacman -Qo` = glib2 2.90.1-1; the same page S527 holds, new scope) | docs | A | the installed gio CLI's launch command: its DESKTOP-FILE plus FILE-ARG form, that it takes any desktop file rather than only registered handlers, and the exit-status sentence | gio.1 lines 49 (the synopsis), 218 (the command form), 221 (Launch a desktop file from any location given.), 223-225 (extends open), 773-775 (EXIT STATUS); .TH "gio" "" "" "" at line 31 | the CLI face of launch: the argument form, that any desktop file is accepted, and that the manual promises only 0 versus non-zero | mined | 2026-11-07 | 180d | corpus/knowledge/gio-exec-argv-r98.md |

## 2. The held row that gains the entry

The entry's frontmatter cites five ids: S528, S529, S530, S531 (new, `used-by` correct from birth)
and **S504** (held). S504's scope already covers `gdesktopappinfo.c:1894-2097 (load_from_keyfile)`,
which is where the load gate of the entry's section 2 lives, so the entry cites it and S504 must
name the entry back (the C2 gate's R4 rule).

| row | cell | old | new |
|---|---|---|---|
| S504 | `used-by` | `corpus/knowledge/mime-default-resolution-r91.md,corpus/lessons/round-91.md` | `corpus/knowledge/mime-default-resolution-r91.md,corpus/lessons/round-91.md,corpus/knowledge/gio-exec-argv-r98.md` |

No other cell of S504 moves: its `scope`, `anchor`, `teaches`, `status`, `opened` and `recheck` stay
as they are. In particular the entry does **not** re-scope S504 - the launch expansion is S528's.

S527 is not touched. Its scope is the `info` command; the `launch` command is S531's. If the L1
prefers to fold S531 into S527 instead, that would be an in-place `scope` change, which the
registry's own header forbids (`Only status, recheck and used-by change in place`), so this draft
keeps them separate - the same shape S525 and S526 used in round 97.

## 3. Located quotes for the lesson's Gate block

Every quote is a whitespace-collapsed line of the fetched bytes, <= 25 words, ASCII.

| id | locator | access | located quote | line |
|---|---|---|---|---|
| S528 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gdesktopappinfo.c (8e9ce1a8...b0d, 163369 B), HTTP 200; new scope on the file S504 holds | 2026-11-07 | `if (p[0] == '%' && p[1] != '\0')` | gdesktopappinfo.c 2724 |
| S528 | same | 2026-11-07 | `/* If there is no macro default to %f. This is also what KDE does */` | 2738 |
| S528 | same | 2026-11-07 | `res = g_shell_parse_argv (expanded_exec->str, argc, argv, error);` | 2743 |
| S528 | same | 2026-11-07 | `while (dup_uris != NULL);` | 3186 |
| S528 | same | 2026-11-07 | `/* Pass URI if it contains an anchor */` | 2564 |
| S529 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gshell.c (640a0d0f...442, 21464 B), HTTP 200; new scope on the file S506 holds | 2026-11-07 | `/* We always use single quotes, because the algorithm is cheesier.` | gshell.c 202 |
| S529 | same | 2026-11-07 | `/* Replace literal ' with a close ', a \', and an open ' */` | 221 |
| S529 | same | 2026-11-07 | `/* Discard up to and including next newline */` | 469 |
| S530 | https://specifications.freedesktop.org/desktop-entry/latest/exec-variables.html (2c50a9e4...77e, 17153 B), HTTP 200 after the documented 301 | 2026-11-07 | `A single file name (including the path), even if multiple files are selected.` | rendered 63 |
| S530 | same | 2026-11-07 | `A command line may contain at most one %f, %u, %F or %U field code.` | rendered 112 |
| S530 | same | 2026-11-07 | `field code expansion inside a quoted argument is undefined. The %F, %U` | rendered 117 |
| S531 | `gio(1)` GLib 2.90.1, file:///usr/share/man/man1/gio.1.gz (installed page, no HTTP status for a `file://` locator; container 810077be...a565, 4961 B; plain 84b3cdad...8bc5, 18793 B, 781 lines; owner `pacman -Qo` = glib2 2.90.1-1); new scope on the page S527 holds | 2026-11-07 | `\fBlaunch\fP \fIDESKTOP\-FILE\fP [\fIFILE\-ARG\fP...]` | gio.1 218 |
| S531 | same | 2026-11-07 | `Launch a desktop file from any location given.` | gio.1 221 |

## 4. Notes the L1 needs before landing

1. **The item's parenthetical names the wrong held rows.** The seat item said the gdesktopappinfo.c
   row is "a new scope on the file S518/S521/S505/S526 hold". Those four rows hold
   `gcontenttype-fdo.c` (and S505 also `xdgmime/*.c`); `gdesktopappinfo.c` is held by **S504**
   (`corpus/SOURCES.md:456`). This draft anchors the row on S504 and keeps the W04 duplicate-URL
   warning, which is real either way because S528 repeats S504's first URL.
2. **The item's "a new scope on S527" is drafted as a new row (S531).** A `scope` change in place
   is forbidden by the registry header; S525/S526 established the new-row shape for a new scope on
   a held locator. If the L1 wants S527 itself re-scoped, that contradicts the header and should be
   logged as an exception in the lesson.
3. **W04 duplicates expected:** S528 vs S504 (same URL), S529 vs S506 (same URL), S531 vs S527
   (same `file://` locator). S530 is a new locator (the spec page moved; S517's locator answers 301
   to it), so no duplicate there - the same relationship S523 has to S517.
4. **No row is marked `queued`.** All four were opened and read this round; the entry cites located
   lines of each.
5. **`recheck` 180d on all four.** S528/S529 flip on a GLib tag change; S530 on a spec revision;
   S531 on a `glib2` package change (the page carries no version and no date - `.TH "gio" "" "" ""`
   at line 31 - so the owning package is the only version binding, exactly as S527 records).
