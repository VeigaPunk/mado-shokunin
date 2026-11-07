# R98MScribe - the C1 entry draft and its SOURCES rows

Seat: scribe, round 98 w1. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`, base
`35f3ce808788b11c063309b1b5ad0192754795ea` (branch `master`). No commit, push, or mutating git/jj
command was run anywhere. No product code, judge, quality file, corpus file or sibling lane was
written. Scratch `/fast/scratch/hyaku/mado-r98/R98MScribe` was deleted at the end of the run.

## 1. What was produced

| artifact | path | state |
|---|---|---|
| the knowledge entry draft | `.ufo/waves/round-98/w1/drafts/gio-exec-argv-r98.md` | 690 lines, ASCII only, 4-key frontmatter, 13 sections |
| the SOURCES row draft | `.ufo/waves/round-98/w1/drafts/sources-rows-r98.md` | 86 lines: four registry rows, one held-row `used-by` append, the Gate-block quote table, four landing notes |
| this report | `.ufo/waves/round-98/w1/R98MScribe.md` | - |

The entry targets `corpus/knowledge/gio-exec-argv-r98.md`; the L1 lands it. The rows target
`corpus/SOURCES.md` as S528-S531; the L1 lands them.

## 2. Behaviour the drafts describe (the surface the L1 re-declared)

The surface is the **sequence** of argv vectors, not one vector. `expand_application_parameters`
(`gdesktopappinfo.c:2700-2746`) is called inside `do { ... } while (dup_uris != NULL)`
(`:3007-3186`), and `expand_macro` advances the caller's list pointer (`*uri_list = uris;` at
`:2697`), so each iteration rebuilds the whole string from `Exec` and consumes what it can.

| Exec shape | consumed per iteration | spawns | measured |
|---|---|---|---|
| no field code, or only non-consuming codes (`%i` `%c` `%k` `%%`, unknown `%X`) | 1, by the section 6 append | one per argument | `plain2`, `iargs`, `c_arg2`, `k_arg2`, `pct_arg2` |
| one single-consuming code (`%f` `%u` `%d` `%n`) | 1 | one per argument | `f2`, `f3`, `ufile2`, `d2dirs` |
| k single-consuming codes | k | ceil(n/k) | `ff3` (2 then 1) |
| a list code (`%F` `%U` `%D` `%N`) | all remaining | 1 | `F3`, `Umix`, `D2` |

## 3. Gates and provenance

- The three fetched files were re-hashed against the L1's receipt
  `.ufo/waves/round-98/receipts/sources-open-r98.txt` and match byte for byte:
  `gdesktopappinfo.c` 163369 B / `8e9ce1a8...b0d`, `gshell.c` 21464 B / `640a0d0f...442`,
  `exec-variables.html` 17153 B / `2c50a9e4...77e`.
- The oracle is the installed `/usr/bin/gio`, sha256
  `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`, `gio --version` 2.90.1,
  `glib2 2.90.1-1`. The digest is the declaration's pin.
- `gio(1)` was rendered from `/usr/share/man/man1/gio.1.gz` (container `810077be...a565`, 4961 B;
  decompressed `84b3cdad...8bc5`, 18793 B, 781 lines) - the same cells S527 records.
- The spec's line numbers are those of a stated rendering (tags stripped, entities unescaped, blank
  lines dropped, 121 lines). The method is in the entry's section 1.3 so a reader can reproduce it.
- **Instrument vs candidate.** The probe runner and the `gio launch` invocations are instruments.
  Nothing in the drafts is candidate code; the entry describes the C1 candidate's model, it does not
  contain it.
- Every probe ran as
  `env -i LC_ALL=C HOME=<root>/h PATH=/usr/bin:/bin gio launch <root>/app.desktop <args...>`
  with the case root under the seat's scratch. The only process started was the fixture probe child
  (`probe.sh`, mode 0755, appending `ARGC=`/`A<i>=` blocks to `$0.out`). No host application was
  launched, no host config was written, no service was touched, no network was used.

## 4. Findings

### 4.1 Contract defects found by measurement (all three already folded in by the L1)

| # | the contract said | the bytes and the oracle say | evidence |
|---|---|---|---|
| F1 | the `#` bypass of `expand_macro_uri` is a scored rule (`u-anchor` class, "`%u` with a file URI carrying `#`") | **unobservable through `gio launch`**: the CLI converts each argument to a `GFile` first and a `file:` URI's fragment does not survive it. `uanchor` passes `file://<root>/files/one.txt#frag` and the child receives the **path**. A non-local URI keeps its fragment (`uhttp_frag`) but both branches agree for it, because `g_file_get_path` is NULL and `:2573` falls back to the URI | `gdesktopappinfo.c:2563-2574`; probes `uanchor`, `uhttp_frag` |
| F2 | the `Hidden` refusal is part of the model | **`Hidden=true` launches**: `info->hidden` (`:2022`) is consulted only where an application is added to a list (`:413`), never on the launch path. `hidden` spawns the probe with `['one']`, exit 0 | `gdesktopappinfo.c:413`, `:2022`; probe `hidden` |
| F3 | `exec-parse` is reachable from a malformed `Exec` | a malformed **raw** `Exec` refuses at **load** (gate step 8/9), not at expansion. `exec-parse` is reachable only through an empty or blank `Exec` (`Text was empty (or contained only whitespace)`), and with an argument that shape instead fails the program lookup (`Program '<arg>' not found in $PATH`) | `:1978`, `:1993`, `:2743`, `:3066-3094`; probes `badquote`, `noprog`, `emptyexec`, `q_space_only_exec`, `emptyexec_arg` |

### 4.2 Findings the L1 has not yet seen

| # | finding | evidence | what it changes |
|---|---|---|---|
| F4 | **`X-GIO-NoFuse` is a real, observable axis.** `force_file_uri` is TRUE only when `!info->no_fuse` (`:2600`). With `X-GIO-NoFuse=true`, `%u` emits `file://<root>/files/one.txt` where it otherwise emits the path | probe `ufile_nofuse` vs `ufile` | if the freeze wants the `u-file` class to be unambiguous, either the case tree must never set the key (then it is a named limit) or the class gains a case. The entry models it and names it in 13.5 |
| F5 | **`%f` with a non-local URI yields a spawn with an empty argv tail.** `g_file_get_path` returns NULL (`:2524-2526`), nothing is appended, but the URI is still consumed, so the loop advances and spawns again | probe `fmix`: `[<root>/files/one.txt]` then `[]` | a case schema that scores one argv per case cannot express this; the frozen `expect` must be the vector **sequence** |
| F6 | **`%d`/`%D` do not de-duplicate.** Two files in one directory give the same dirname twice | probe `D2`: `['<root>/files', '<root>/files']` | the `d` class should include the same-directory pair, not only two directories |
| F7 | **A field code inside a quoted argument is well defined, and the spec calls it undefined.** The expansion is textual and precedes parsing, so the `g_shell_quote`d value lands inside the token with its single quotes literal | probes `f_in_arg_quotes`, `u_in_arg_quotes`, `F_in_arg_quotes`: `Exec={probe} "a %f b"` gives one argument `a '<root>/files/one.txt' b` | a `quote`-class case worth freezing; it is the sharpest spec-vs-implementation delta on this surface |
| F8 | **GKeyFile refuses any `Exec` escape outside `\s \n \t \r \\`.** `a\zb`, `a\:b`, `"a\"b"` are load refusals; `a\\ b` decodes to `a\ b` (one argument), `a\sb` to `a b` (two arguments) | probes `esc_z`, `esc_colon`, `esc_dq`, `q_back2`, `q_back3`, `esc_n`, `esc_t` | confirms the L1's (b) and gives the `quote` class its two-layer escaping cases |
| F9 | **The load gate makes some shapes unloadable, so they cannot be frozen as expansion cases.** `Exec={probe}%i` and `Exec="{probe} %f"` refuse at load because the raw `Exec`'s `argv[0]` is not an executable file | probes `i_nospace`, `f_in_quotes` | a case author must keep `argv[0]` a resolvable program in every case |
| F10 | **`%k` prints `info->filename` verbatim** (`:2683`), and the property setter stores the string it is given (`:1757`). The absolute path a probe sees is the **CLI's** canonicalization of its argument, not a rule of `gdesktopappinfo.c` | probe `krel` (launched as `./app.desktop`, child receives the absolute path) | the `k` class should assert the path the CLI was given, and the entry must not claim the library canonicalizes |
| F11 | **The spec's `%v` has no arm at all** (`grep -c "case 'v'" gdesktopappinfo.c` = 0), so it behaves like an unlisted code rather than like `%m`'s explicit empty arm | `:2617-2695`; no probe (the observable result equals `bad_z`) | a delta row, not a case |

### 4.3 Discrepancies in my own seat item (for the L1 to rule on)

1. **The item names the wrong held rows.** It says the gdesktopappinfo.c row is "a new scope on the
   file S518/S521/S505/S526 hold". Those hold `gcontenttype-fdo.c` (S505 also `xdgmime/*.c`);
   `gdesktopappinfo.c` is held by **S504** (`corpus/SOURCES.md:456`). The draft anchors on S504 and
   keeps the W04 duplicate-URL warning, which is real either way.
2. **"a new scope on S527" is drafted as a new row S531.** The registry header says
   `Only status, recheck and used-by change in place`, so a `scope` change must be a new row; S525
   and S526 established that shape. If the L1 wants S527 itself re-scoped, it is an exception the
   lesson should log.
3. **The item's row count and the registry's max id agree**: S527 is the highest id at base, so
   S528-S531 are free.

## 5. The Gate block the lesson needs

Verbatim from `sources-rows-r98.md` section 2, ready to paste into `corpus/lessons/round-98.md`
under `## Gate`:

```
### Rows touched

S504: `used-by` only, appended with `corpus/knowledge/gio-exec-argv-r98.md`
(old -> new in `.ufo/waves/round-98/w1/drafts/sources-rows-r98.md` section 2). No anchor, digest
or scope cell of a held row moves.

### Registry rows (opened 2026-11-07; the L1's fetch receipt is
`.ufo/waves/round-98/receipts/sources-open-r98.txt`)

| id | locator | access | located quote | line |
|---|---|---|---|---|
| S528 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gdesktopappinfo.c (8e9ce1a8...b0d, 163369 B), HTTP 200; new scope on the file S504 holds | 2026-11-07 | `if (p[0] == '%' && p[1] != '\0')` | gdesktopappinfo.c 2724 |
| S529 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gshell.c (640a0d0f...442, 21464 B), HTTP 200; new scope on the file S506 holds | 2026-11-07 | `/* We always use single quotes, because the algorithm is cheesier.` | gshell.c 202 |
| S530 | https://specifications.freedesktop.org/desktop-entry/latest/exec-variables.html (2c50a9e4...77e, 17153 B), HTTP 200 after the documented 301 | 2026-11-07 | `A single file name (including the path), even if multiple files are selected.` | rendered 63 |
| S531 | `gio(1)` GLib 2.90.1, file:///usr/share/man/man1/gio.1.gz (installed page, no HTTP status for a `file://` locator; container 810077be...a565, 4961 B; plain 84b3cdad...8bc5, 18793 B, 781 lines; owner `pacman -Qo` = glib2 2.90.1-1); new scope on the page S527 holds | 2026-11-07 | `\fBlaunch\fP \fIDESKTOP\-FILE\fP [\fIFILE\-ARG\fP...]` | gio.1 218 |
```

S528 repeats S504's URL, S529 repeats S506's, S531 repeats S527's `file://` locator: three W04
duplicates are expected and the `scope` cell is what differs. S530 is a new locator (S517's answers
301 to it), so no duplicate there - the same relationship S523 has to S517.

## 6. Out of scope / not measured

- **`Terminal=true`.** `prepend_terminal_to_vector` (`:3027`, table at `:2766-2777`) rewrites argv
  before the spawn. Measuring it would start a host terminal, which this seat's rules forbid. Named
  limit 13.3.
- **`Path=` as cwd.** Measured once (`pathcwd`: the child's `PWD` is `<root>/wd`) and named as a
  limit (13.2), because the model's output is the argv, not the cwd.
- **D-Bus activation** (`:3431-3437`) and **the portal path** (`:2979-3001`): read far enough to say
  when each is taken, not measured. Every probe ran under `env -i` with no session bus, which is why
  all of them took the spawn branch.
- **`%N`** is not probed separately: it shares `expand_macro_single`'s arm with `%n` (`:2538-2539`)
  and `expand_macro`'s loop with `%D` (`:2641`). The entry says so rather than claiming a row.
- **`%m`** and **`%v`** are not probed: `%m`'s arm is empty and `%v` has no arm; both are stated from
  the source, and the entry marks them "not measured separately".
- **`X-SnapInstanceName` / `g_document_portal_add_documents`**: needs a portal and a snap-named
  desktop file. Named limit 13.4.
- **`gio-launch-desktop`**: `wrapped_argv[0]` is the wrapper (`:3125`), which execs the real
  program. The probe sees the real argv; the model stops at the vector handed to
  `g_spawn_async_with_fds`.
- **The C1 counter's numbers**: no cell of either draft is a number the counter will print. Those
  are the L1's receipt (round-96 D2 discipline).
- **`gkeyfile.c`**: not re-read this round. The GKeyFile escape rule is stated only from probe rows;
  the entry says so explicitly (section 2.3).

## 7. Tooling

No tool was installed, upgraded or removed. No pacman transaction was attempted. The only binaries
used were the host's `bash`, `awk`, `sed`, `grep`, `sha256sum`, `gzip`, `python3`, `wc`, `ls`, `cat`,
`mkdir`, `rm`, `chmod`, `printf`, `env` and `/usr/bin/gio` (the oracle). No `git` command was run at
all, mutating or otherwise. No `sudo`.

## 8. Checks the L1 should run

1. `grep -nP '[^\x00-\x7F]'` over both drafts - expected empty (verified here for both).
2. The registry row shape: each of the four rows has exactly 12 `|` (11 columns) - verified here.
3. `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` after landing - W04
   warnings expected for S528/S529/S531.
4. The C2 read-back gate over the landed registry: the entry's five frontmatter ids must each name
   the entry back. S504's `used-by` append is the only held-row edit.

## Appendix A - verbatim probe transcript (the 60 spawn rows)

One block per row of the entry's section 12.2-12.9, in the entry's order. `EXEC` is the desktop
file's `Exec` value after the `{probe}` substitution is undone; `L<n>` is the n-th `ARGC=` block the
probe appended, i.e. the n-th spawn. `<root>` is the case root's absolute path; `\t` in an `EXEC` line is a literal TAB byte.

```
### plain0
EXEC: {probe} one two
L1 ARGC=2
  A0=one
  A1=two
### plain1
EXEC: {probe} one two
L1 ARGC=3
  A0=one
  A1=two
  A2=<root>/plain1/files/one.txt
### plain2
EXEC: {probe} one two
L1 ARGC=3
  A0=one
  A1=two
  A2=<root>/plain2/files/one.txt
L2 ARGC=3
  A0=one
  A1=two
  A2=<root>/plain2/files/two words.txt
### f0
EXEC: {probe} %f
L1 ARGC=0
### f1
EXEC: {probe} %f
L1 ARGC=1
  A0=<root>/f1/files/one.txt
### f2
EXEC: {probe} %f
L1 ARGC=1
  A0=<root>/f2/files/one.txt
L2 ARGC=1
  A0=<root>/f2/files/two words.txt
### f3
EXEC: {probe} %f
L1 ARGC=1
  A0=<root>/f3/files/one.txt
L2 ARGC=1
  A0=<root>/f3/files/two words.txt
L3 ARGC=1
  A0=<root>/f3/files/q'uote.txt
### ff
EXEC: {probe} %f %f
L1 ARGC=2
  A0=<root>/ff/files/one.txt
  A1=<root>/ff/files/two words.txt
### ff3
EXEC: {probe} %f %f
L1 ARGC=2
  A0=<root>/ff3/files/one.txt
  A1=<root>/ff3/files/two words.txt
L2 ARGC=1
  A0=<root>/ff3/files/q'uote.txt
### fmix
EXEC: {probe} %f
L1 ARGC=1
  A0=<root>/fmix/files/one.txt
L2 ARGC=0
### fhttp
EXEC: {probe} %f
L1 ARGC=0
### F0
EXEC: {probe} %F
L1 ARGC=0
### F1
EXEC: {probe} %F
L1 ARGC=1
  A0=<root>/F1/files/one.txt
### F3
EXEC: {probe} %F
L1 ARGC=3
  A0=<root>/F3/files/one.txt
  A1=<root>/F3/files/two words.txt
  A2=<root>/F3/files/q'uote.txt
### fF
EXEC: {probe} %f %F
L1 ARGC=3
  A0=<root>/fF/files/one.txt
  A1=<root>/fF/files/two words.txt
  A2=<root>/fF/files/q'uote.txt
### Fi
EXEC: {probe} %F %i
L1 ARGC=4
  A0=<root>/Fi/files/one.txt
  A1=<root>/Fi/files/two words.txt
  A2=--icon
  A3=my-icon
### ufile
EXEC: {probe} %u
L1 ARGC=1
  A0=<root>/ufile/files/one.txt
### ufile2
EXEC: {probe} %u
L1 ARGC=1
  A0=<root>/ufile2/files/one.txt
L2 ARGC=1
  A0=<root>/ufile2/files/two words.txt
### uhttp
EXEC: {probe} %u
L1 ARGC=1
  A0=http://example.com/a?b=c
### uanchor
EXEC: {probe} %u
L1 ARGC=1
  A0=<root>/uanchor/files/one.txt
### uhttp_frag
EXEC: {probe} %u
L1 ARGC=1
  A0=http://example.com/x#frag
### ufile_nofuse
EXEC: {probe} %u
L1 ARGC=1
  A0=file://<root>/ufile_nofuse/files/one.txt
### Umix
EXEC: {probe} %U
L1 ARGC=2
  A0=<root>/Umix/files/one.txt
  A1=http://example.com/x
### U0
EXEC: {probe} %U
L1 ARGC=0
### d1
EXEC: {probe} %d
L1 ARGC=1
  A0=<root>/d1/files
### d2dirs
EXEC: {probe} %d
L1 ARGC=1
  A0=<root>/d2dirs/files
L2 ARGC=1
  A0=<root>/d2dirs/h
### D2
EXEC: {probe} %D
L1 ARGC=2
  A0=<root>/D2/files
  A1=<root>/D2/files
### n1
EXEC: {probe} %n
L1 ARGC=1
  A0=one.txt
### d_http
EXEC: {probe} %d
L1 ARGC=0
### n_http
EXEC: {probe} %n
L1 ARGC=0
### i_icon
EXEC: {probe} %i
L1 ARGC=2
  A0=--icon
  A1=my-icon
### i_noicon
EXEC: {probe} %i
L1 ARGC=0
### i_iconspace
EXEC: {probe} %i
L1 ARGC=2
  A0=--icon
  A1=my icon
### iargs
EXEC: {probe} %i
L1 ARGC=3
  A0=--icon
  A1=my-icon
  A2=<root>/iargs/files/one.txt
L2 ARGC=3
  A0=--icon
  A1=my-icon
  A2=<root>/iargs/files/two words.txt
### noicon_pct_i
EXEC: {probe} x%iy
L1 ARGC=1
  A0=xy
### c_name
EXEC: {probe} %c
L1 ARGC=1
  A0=Case c_name
### c_arg2
EXEC: {probe} %c
L1 ARGC=2
  A0=Case c_arg2
  A1=<root>/c_arg2/files/one.txt
### q_apos_name
EXEC: {probe} %c
L1 ARGC=1
  A0=it's mine
### noname
EXEC: {probe} %c
L1 ARGC=0
### k_path
EXEC: {probe} %k
L1 ARGC=1
  A0=<root>/k_path/app.desktop
### k_arg2
EXEC: {probe} %k
L1 ARGC=2
  A0=<root>/k_arg2/app.desktop
  A1=<root>/k_arg2/files/one.txt
### krel
EXEC: {probe} %k
L1 ARGC=1
  A0=<root>/krel/app.desktop
### q_apos_icon
EXEC: {probe} %i
L1 ARGC=2
  A0=--icon
  A1=it's
### pct
EXEC: {probe} %% done
L1 ARGC=2
  A0=%
  A1=done
### pct_trail
EXEC: {probe} 100%
L1 ARGC=1
  A0=100%
### pct_arg2
EXEC: {probe} %%
L1 ARGC=2
  A0=%
  A1=<root>/pct_arg2/files/one.txt
### bad_z
EXEC: {probe} %z
L1 ARGC=0
### bad_q
EXEC: {probe} a%qb
L1 ARGC=1
  A0=ab
### q_single
EXEC: '{probe}' one
L1 ARGC=1
  A0=one
### q_double
EXEC: "{probe}" one
L1 ARGC=1
  A0=one
### q_back2
EXEC: {probe} a\\ b
L1 ARGC=1
  A0=a b
### q_back3
EXEC: {probe} a\sb
L1 ARGC=2
  A0=a
  A1=b
### q_tab
EXEC: {probe}\tone   (\t is a literal TAB byte in the file)
L1 ARGC=1
  A0=one
### esc_n
EXEC: {probe} a\nb
L1 ARGC=2
  A0=a
  A1=b
### esc_t
EXEC: {probe} a\tb
L1 ARGC=2
  A0=a
  A1=b
### f_in_arg_quotes
EXEC: {probe} "a %f b"
L1 ARGC=1
  A0=a '<root>/f_in_arg_quotes/files/one.txt' b
### u_in_arg_quotes
EXEC: {probe} "a %u b"
L1 ARGC=1
  A0=a '<root>/u_in_arg_quotes/files/one.txt' b
### F_in_arg_quotes
EXEC: {probe} "a %F b"
L1 ARGC=1
  A0=a '<root>/F_in_arg_quotes/files/one.txt' '<root>/F_in_arg_quotes/files/two.txt' b
### pathcwd
EXEC: {probe} %f
  PWD=<root>/pathcwd/wd
L1 ARGC=1
### hidden
EXEC: {probe} one
L1 ARGC=1
  A0=one
```

## Appendix B - verbatim refusal transcript (the 15 refusal rows)

`rc` is `gio launch`'s exit status; `NO-OUT` means the probe never ran. The CLI renders the path
and the key-file line with U+2018/U+2019/U+201C/U+201D; they are ASCII-rendered here.

```
CASE garbage rc=1
  STDERR: gio: Unable to load '<root>/garbage/app.desktop': Key file contains line "not a key file at all" which is not a key-value pair, group, or comment|
  NO-OUT
CASE nogroup rc=1
  STDERR: gio: Unable to load application information for '<root>/nogroup/app.desktop'|
  NO-OUT
CASE notype rc=1
  STDERR: gio: Unable to load application information for '<root>/notype/app.desktop'|
  NO-OUT
CASE typelink rc=1
  STDERR: gio: Unable to load application information for '<root>/typelink/app.desktop'|
  NO-OUT
CASE badquote rc=1
  STDERR: gio: Unable to load application information for '<root>/badquote/app.desktop'|
  NO-OUT
CASE noprog rc=1
  STDERR: gio: Unable to load application information for '<root>/noprog/app.desktop'|
  NO-OUT
CASE esc_z rc=1
  STDERR: gio: Unable to load application information for '<root>/esc_z/app.desktop'|
  NO-OUT
CASE esc_colon rc=1
  STDERR: gio: Unable to load application information for '<root>/esc_colon/app.desktop'|
  NO-OUT
CASE esc_dq rc=1
  STDERR: gio: Unable to load application information for '<root>/esc_dq/app.desktop'|
  NO-OUT
CASE i_nospace rc=1
  STDERR: gio: Unable to load application information for '<root>/i_nospace/app.desktop'|
  NO-OUT
CASE f_in_quotes rc=1
  STDERR: gio: Unable to load application information for '<root>/f_in_quotes/app.desktop'|
  NO-OUT
CASE noexec rc=1
  STDERR: gio: Unable to launch application '<root>/noexec/app.desktop': Desktop file didn't specify Exec field|
  NO-OUT
CASE emptyexec rc=1
  STDERR: gio: Unable to launch application '<root>/emptyexec/app.desktop': Text was empty (or contained only whitespace)|
  NO-OUT
CASE q_space_only_exec rc=1
  STDERR: gio: Unable to launch application '<root>/q_space_only_exec/app.desktop': Text was empty (or contained only whitespace)|
  NO-OUT
CASE emptyexec_arg rc=1
  STDERR: gio: Unable to launch application '<root>/emptyexec_arg/app.desktop': Program '<root>/emptyexec_arg/notaprogram' not found in $PATH|
  NO-OUT
```
