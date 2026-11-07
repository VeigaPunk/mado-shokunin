# R98MExecTool - round 98 w1 - C1 candidate `mado-execargv.py`

Seat: build + falsify-support for C1 (launch argv). Report path (lane-relative):
`.ufo/waves/round-98/w1/R98MExecTool.md`. Owned file, final bytes (after the L1's 20-class rule fold and the reviewer
fold):
`.ufo/waves/round-98/build/mado-execargv.py`, sha256
`acfcc4f7d75162d8035ac26e7ecf48ace8b78dcc8255775e8bab347cfa70ab61`.
Selftest: `MADO_EXECARGV_SELFTEST: checks=38 failed=0` (exit 0).
Live oracle head-to-head: **52/52 cases PASS** (launch count + multiset of
vectors, the amended reader rule) against `/usr/bin/gio`
(sha256 `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`,
glib2 2.90.1-1), covering the 16 original class shapes, the 4 added classes
(`nonlocal`, `nofuse`, `multilaunch`, `comment`), the reviewer folds
(absolute-icon, byte walk, indented comment) and 9 further attack edges.

## 1. Deliverable and structure

CLI exactly per Shared contract 1 plus the L1's rule-6 update: text output
`MADO_EXECARGV: launches=N` / `LAUNCH k: argc=M` / `ARGV[k][i]=v`; refusals
`MADO_EXECARGV: ERROR <cause> detail=<...>` exit 2 with causes exactly
{no-exec, desktop-file, exec-parse}; `--json` `{"launches":N,"argv":[[...],...]}`
/ `{"error":...,"detail":...}`; `--selftest` prints
`MADO_EXECARGV_SELFTEST: checks=N failed=M` plus
`MADO_EXECARGV_SELFTEST_FAIL: <id>` lines. Refusal detail tokens are stable:
unreadable, key-before-group, grammar, no-desktop-entry-group, type,
bad-escape-type, bad-escape-path, bad-escape-exec, missing-exec, static,
trailing-backslash, comment-at-eof, unterminated-quote, empty, unmatched-quote.

Candidate imports: sys, json, re, tempfile, shutil (stdlib only). No
subprocess, socket, ctypes; the only file read is the DESKTOP argument's bytes
(desktop decoded UTF-8 with surrogateescape) plus selftest fixtures the tool
itself wrote under `tempfile.mkdtemp()`. `def selftest(` (line 527) sits after
the whole production path (QUALITY 167); each spec concept has exactly one
implementation in the non-selftest prefix (mutation anchor map sent to
R98MMutC1). Counter (R98MExecCounter) scores via `--json`; text grammar is the
human face only. All scratch drivers (`calib.sh`, `calib2.sh`, `compare.py`,
`probe.sh`) are instruments that spawn `gio` - none of that code is in the
candidate.

## 2. Rule-to-line map (declaration rule -> fetched glib bytes -> candidate line)

| rule | glib 2.90.1 ground (fetched `fetch/gdesktopappinfo.c`, `fetch/gshell.c`) | candidate |
|---|---|---|
| 1 start-group gate | gdesktopappinfo.c:1907-1911 (`get_start_group` must be "Desktop Entry") | `parse_desktop` :97-140 (first group; keys only while `current == group`) |
| 1 Type check | :1913-1918 (NULL or != "Application" -> refuse) | `run` :480-497 (`desktop-file`/`type`) |
| 1 Path read | :1920-1931 with `is_invalid_key_error` | `run` `bad-escape-path` (value unused by argv; working-dir is spawn-plane) |
| 1 Exec read | :1953-1960 with `is_invalid_key_error`; empty-string branch :1976 | `run` `bad-escape-exec`; empty Exec -> expansion "" -> `exec-parse`/`empty` |
| 1 Exec static parse | :1977-1980 (`g_shell_parse_argv(exec)` at load; failure refuses the load) | `run` static leg -> `exec-parse`/`static` |
| 1 program lookup | :1983-2004 (`g_find_program_for_path(argv[0])`) - NOT modelled (named limit; scored cases pin an existing executable probe) | absent by design |
| 1 Name/Icon reads | :2010-2012 (`get_locale_string`, error=NULL) | `lenient_value` :452 (bad escape -> key absent) |
| 1 icon suffix strip | :2049-2055 (trailing .png/.xpm/.svg, case-sensitive, at last dot) | `strip_icon_ext` :460 |
| 1 Terminal/Hidden | :2019-2025 booleans; **Hidden does not refuse** (see 3.1) | `bool_value` :472 (read, unused) |
| 1 no-exec | launch error "Desktop file didn't specify Exec field" :2711-2714 | `run` `no-exec`/`missing-exec` |
| 2 % walk | :2721-2725 (`p[0]=='%' && p[1]!='\0'`: the selector byte is CONSUMED, unknown selectors expand to nothing, so `100% done` -> `100done`); trailing `%` falls through :2726-2728 | `build_launches` walk loop (`macro(code); i += 2`) |
| 2 tokenizer | gshell.c:433-585 `tokenize_command_line` (backslash state keeps `\x` pairs; `#` comment after line-start/space/newline; `\n` delimits; consecutive-backslash `quoted` flag) | `tokenize_command_line` :315-382 |
| 2 unquote | gshell.c:261-317 `g_shell_unquote` + unquote_string_inplace :100-193 (dquote escapes `"`,`\`,`` ` ``,`$`,newline; outside-quote backslash escapes any char but newline) | `unquote_token` :384-436 |
| 2 parse_argv | gshell.c:657-690 (tokenize, then unquote each token) | `shell_parse_argv` :438-450 |
| 3 one-arg codes | :2506-2555 `expand_macro_single` (u/U quote URI; f/F/d/D/n/N need a local path - non-local URIs append NOTHING and are consumed/dropped by the list codes) | `expand_single` :220-231 |
| 3 force_file_uri | :2556-2578 `expand_macro_uri` + :2599-2601 (`X-GIO-NoFuse=true` skips the force step, so %u/%U pass the URI form) + **measured**: gio-tool-launch.c:106 + `g_file_get_uri` drop `#fragment` and `?query` for local file URIs, so the `#` bypass is unobservable locally | `arg_model` :184-213 + `expand_macro_uri` :234-248 (`force_file_uri` gate) |
| 3 %i | :2660-2668 (`--icon ` + quoted icon_name; strip per :2044-2055 applies to the themed branch only - absolute icon paths are GFileIcons and KEEP their extension, measured `Icon=/tmp/ic.png` -> `--icon /tmp/ic.png`) | `macro` 'i' branch; `strip_icon_ext` :507-517 |
| 3 %c / %k / %m / %% | :2670-2677 / :2679-2686 / :2688-2689 / :2691-2692; unknown codes: switch has no default -> dropped, no error. %c is the LOCALE-SELECTED Name (info->name via `get_locale_string` :2010, locale=NULL -> current locale), %k the CWD-resolved absolute desktop path (gio tool builds a GFile from the argument) | `macro` branches; `locale_selected` + `locale_language_list` :466-500; `desktop_k_path` :502-509 |
| 4 default %f | :2735-2742 (`uri_list == *uris && uri_list != NULL`: HEAD-POINTER equality, so a non-consuming macro (%c, %i, %%, unknown) still triggers the fallback) | `build_launches` tail |
| 5 g_shell_quote | gshell.c:200-232 (always `'...'`, `'` -> `'\''`) | `shell_quote` :143-144 |
| 6 iteration | :3002-3021 `do { old_uris = dup_uris; expand_application_parameters(...); } while (dup_uris != NULL)` (`%f %f` + 3 args -> 2 launches; `%f %F` + 3 -> 1) | `build_launches` `while True` :251-318 |

GKeyFile grammar facts the desktop half relies on (whole-file scan, first
group's values, lazy per-read unescaping, value strip set = g_ascii_isspace
{TAB LF FF CR SP}, CRLF tolerated, key-before-group refuses): measured in 3.3
and consistent with SOURCES rows S502/S514 (gkeyfile.c, same glib pin).

## 3. Measured rule corrections - attack findings with probe receipts

Every probe: case root under the seat scratch, `env -i LC_ALL=C HOME=<root>/h
PATH=/usr/bin:/bin /usr/bin/gio launch <root>/app.desktop <args>`, contract
probe child appending `@@@ argc` / `P0=` / `A<i>=` records; argv values quoted
below without the `<root>` prefix.

1. **Hidden launches.** `Hidden=true` + valid Exec -> rc=0, probe records
   `[probe, f1]`. The declaration's rule-1 "the `Hidden` refusal" is
   contradicted by the oracle; the only launch-path hidden gate is the
   desktop-id lookup (:2208-2212), while `g_desktop_app_info_new_from_filename`
   (:2101-2112) calls load_from_keyfile with no hidden branch. Candidate:
   Hidden read-only. (Same measurement independently taken by R98MMutC1;
   confirmed folded by the L1.)
2. **Duplicate keys keep the LAST.** Two Exec lines (`... %c` then `... %k`)
   -> child argv `[probe, "Demo App", f1]` = the *second* Exec expanded plus
   rule-4 default. The declaration's "a duplicate key keeps the first" is
   contradicted; candidate keeps last (fixture `dup-key` PASS). Routed to the
   L1 for the freeze wording.
3. **Escape-refusal scope is per-read-key.** `X-Unknown=a\z` (unknown key),
   `# a\z` (comment), and a bad escape inside a second group all LAUNCH (rc=0);
   only keys read with `is_invalid_key_error` (Type :1917, Path :1929, TryExec
   :1966, Exec :1983) refuse - GKeyFile unescapes at read time, not at parse
   time. Candidate validates escapes exactly on Type/Path/Exec and reads
   Name/Icon leniently. Probe rows: escX/escC/escG rc=0 launch vs trailbs
   (`Exec` value ending in `\`) rc=1 "Unable to load application information".
4. **Local file URI arguments lose `#fragment` AND `?query` before expansion.**
   `%u` with `file://<root>/a.txt#frag` -> argv `[probe, <root>/a.txt]`;
   `file://<root>/a%20b.txt?x#f` -> `[probe, <root>/a b.txt]` (query dropped,
   space decoded). The `expand_macro_uri` `#` bypass (:2562-2565) is therefore
   unobservable for local arguments; it stays live for non-local schemes where
   the fallback yields the raw URI anyway (`U-mixed` http#y PASS). First
   measured by R98MMutC1, re-measured by me; folded by the L1.
5. **Icon extension strip.** `Icon=ic.png` -> `--icon ic`; `my icon.xpm` ->
   `my icon`; case-sensitive suffix set {.png, .xpm, .svg} only (:2049-2055).
   First measured by R98MMutC1/R98MExecOracle; folded by the L1.
6. **`#` in the expanded line.** `Exec=<probe> arg # tail %f` -> argv
   `[probe, "arg"]` with the file consumed (the walk expands `%f`, then the
   tokenizer's comment state eats the tail). A `#` that is the LAST character
   of the expanded line is a parse error (glib EMPTY_STRING); a comment running
   to EOF resets cleanly - my first port errored there and the oracle probe
   caught it (fixed in tokenize_command_line :362-367).
7. **Oracle instrumentation hazards** (routed to R98MExecOracle and
   R98MExecCounter): `gio launch` exits 0 *before* the detached probe child
   writes (settle-poll required), and a per-line `printf >> "$0.out"` probe
   INTERLEAVES between the concurrent spawns of one launch sequence - my first
   `f-2` run recorded a merged `@@@/P0/A` soup that parses as one empty launch
   plus one 4-argv launch. The LANDED recorder (R98MExecOracle's
   `controls/execargv-probe-r98.py`, sha `c5c69445...577c9`) removes the
   shared-append surface entirely: each child takes a sequence number under
   flock and writes its whole record to `$0.out.<seq>`; the builder waits for
   the record set to go quiet (200 ms quiet window, 8 s cap) and parses one
   sealed record per file in sequence order. My single-printf suggestion was
   insufficient - dash's printf can emit multiple write()s, so O_APPEND does
   not make a shared-file record atomic. This mechanism is the plausible
   source of the multi-launch ordering defect R98MMutC1 routed on the frozen
   file. Reader window per the L1's amended declaration: **2 s quiet, 20 s cap**
   (the 200 ms/8 s cell in the first oracle reply was corrected by the L1).
8. **Folded-rule confirmations (20-class plane).** Selector consumption:
   `Exec=<probe> 100% done` -> argv `[probe, 100done]`, `x%1y` -> `xy` (rows
   pct-word, selector PASS). Non-local drops: `%f` with an http URI consumes
   and appends nothing (`[probe]`), `%F` with two http URIs -> one launch
   `[probe]` (rows nonlocal-f/F/u PASS). NoFuse: `X-GIO-NoFuse=true` flips
   `%u` on a local file to the rebuilt file URI (`file://<root>/f1.txt`) and
   leaves `%f` on the path (rows nofuse-u/U/f PASS). Empty `Icon=` ->
   `--icon ''` (row i-empty PASS). Locale: scored runs are LC_ALL=C where the
   language list is `['C']` and plain `Name` wins; the `Name[en_US]` selection
   under en_US.UTF-8 is covered by selftest st-locale-name (env swap), not by
   an LC_ALL=C oracle row. **Order caveat measured**: per-spawn record files
   seal in child-start order, not spawn order (iter-ff recorded `[f3]` before
   `[f1,f2]` in one run) - exactly why the amended reader compares the launch
   count and the MULTISET of vectors; my driver compares multisets, and the
   candidate's emitted order remains the deterministic spawn order.
9. **Reviewer folds (R98MReviewC1, re-measured here).** (a) The icon strip is
   bound to the themed branch: an ABSOLUTE Icon path keeps its extension
   (`Icon=/tmp/ic.png` -> `--icon /tmp/ic.png`; row i-abs PASS, selftest
   st-i-icon-abs). (b) The `%` walk is byte-wise on the raw Exec value: a
   multi-byte UTF-8 char after `%` loses its lead byte (consumed as an unknown
   selector) and its trailing bytes survive (`Exec=<probe> 100%e-acute` ->
   argv `100<U+00A9-as-raw-byte>`; row bytewalk PASS, selftest st-byte-walk;
   the candidate walks bytes and prints via surrogateescape). (c) The load-time
   `g_shell_parse_argv` rejection of the raw Exec value refuses with
   `exec-parse` - already the candidate's static leg (st-quote-unterminated).
   (d) My own docstring claimed "X-GIO-NoFuse is not read" after the code had
   started reading it - an M97-1-class self-contradiction in my own artifact,
   fixed in the same pass; the report's section 6 carried the same stale
   sentence until now.
10. **Indented comments and leading whitespace.** The frozen
   `comment-03-indented` case (`  # indented comment` line) launches on the
   oracle and refuses under my pre-fix grammar check. GKeyFile skips leading
   whitespace on every line before classification (gkeyfile.c:1687-1696, the
   S514 whitespace positions), so the candidate now lstrips KEYFILE_WS before
   the comment/group/key classification. Emulation of the frozen case's exact
   `desktop_raw` answers `launches=1, argv=[[probe, <root>/a.txt]]` = its
   recorded expect; rows indent-comment PASS; selftest st-indent-comment.

## 4. Live oracle head-to-head (52 cases; assignment asked for 20)

Driver: scratch `compare.py` (instrument; builds each case root, runs the gio
oracle with the env -i recipe, settle-polls the probe records, runs the
candidate, compares launch count + multiset of vectors; refusal rows compare
rc!=0 against an ERROR line). Final run on the folded + reviewer rules:
**pass=52/52, fails=[]**.

Rows: plain-0/1/2 (rule 4/6: 1/1/2 launches), f-0/1/2 (one launch per
argument), F-3 (drain, quoting incl. space file), F-0, u-file (force -> path),
u-uri (http -> raw URI), u-anchor (`#frag` -> path), u-qfrag (`?x#f` -> bare
path), U-mixed (path then URI, one launch), U-2, d-1 (dirname), n-1
(basename), i-icon (`ic.png`->`ic`), i-none (default %f still applies),
i-space (`my icon`), i-empty (`--icon ''`), c-1 (`Demo App`), k-1 (desktop
path as given), pct-1 (`100%` + file), pct-t (trailing `%` literal), pct-word
(selector consumed -> `100done`), selector (`x%1y` -> `xy`), bad-1 (`%z`
dropped), bad-2 (`%q` + 2 files -> 2 launches via rule 4), quote-1 (`'a b'`,
`"c\"d"` -> `c"d`, `x\\y` file bytes -> `xy`), quote-ref (unterminated quote ->
exec-parse refusal), path-F (space + apostrophe files round-trip through
`g_shell_quote`), iter-ff (`%f %f` 3 files -> [f1,f2] then [f3], multiset),
iter-fF (`%f %F` 3 files -> 1 launch), nonlocal-f/F/u (consumed, dropped),
nofuse-u/U/f (URI flip under X-GIO-NoFuse=true), esc-ref (`a\z` in Exec ->
desktop-file), noexec (-> no-exec), notype (-> desktop-file), nogroup (first
group `[Other]` -> desktop-file), hidden (launches), dup-key (last Exec wins),
x-unknown (unknown-key escape launches), hash-cut (comment eats the tail),
desk-comment (desktop `#` comment lines skipped), indent-comment (leading-
whitespace comment line), cons-fallback (`%c` +
file -> `[probe, "Demo App", file]`), i-abs (absolute icon keeps extension),
bytewalk (multi-byte char after `%` leaves its trailing byte).

History: first pass on the 16-class plane 35/37 (`f-2` recorder race - fixed
probe, re-measured PASS; `u-qfrag` query drop - fixed in arg_model); 37/37
green at sha 31aca8d8...; the L1's 20-class fold passed first try except the
iter-ff record-order observation (resolved by the amended multiset reader
rule, 3.8); 49/49 at 630faeee...; the reviewer fold + indent-comment fix took
it to 52/52 at the final sha (3.9-3.10). Final bytes re-pinned to
MutC1/Counter.

## 5. Selftest

38 checks, stable ids (never line numbers), fixtures built by the tool under
`tempfile.mkdtemp()`: st-plain-one, st-plain-argless, st-default-f-two-launches,
st-f-one-per-launch, st-f-drain, st-f-f-pairs, st-u-file-path, st-u-remote-uri,
st-u-anchor-file-path, st-u-query-drop, st-U-mixed-order, st-d-dirname,
st-n-basename, st-i-icon, st-i-icon-ext, st-i-icon-space-kept, st-i-empty-icon,
st-i-icon-abs, st-byte-walk, st-nofuse-u-uri, st-locale-name,
st-plain-locale-c, st-i-noicon, st-c-name, st-k-desktop-path, st-pct-double,
st-pct-trailing, st-unknown-code-dropped, st-quote-tokens,
st-quote-unterminated, st-hash-comment-cut, st-dup-key-last-wins,
st-noexec-refusal, st-desktopfile-type, st-desktopfile-escape,
st-desktopfile-group, st-desktopfile-earlykey, st-indent-comment.
Result `checks=38 failed=0`.

## 6. Named limits (off the frozen case plane, stated for the freeze block)

- Load-time TryExec check (:1966-1974) and Exec argv[0] program lookup
  (:1976-2004) plus spawn-time PATH resolution (:3053-3070) are not modelled;
  every scored case pins `{probe}` as an existing absolute executable. A case
  whose expanded argv[0] is not executable (e.g. `Exec=%f ...`) fails in gio at
  spawn - a refusal cause outside the three-cause taxonomy; the case author
  must not freeze such a shape.
- `Terminal=true` would prepend the emulator argv (:2779+); unmodelled; case
  desktops keep Terminal null/false.
- `X-GIO-NoFuse` (:2021, :2599-2601) IS read: true gates the force_file_uri
  step for %u/%U, which then pass the URI form (rows nofuse-u/U/f).
- `g_file_new_for_uri` percent-decode leniency: my `pct_decode` keeps invalid
  `%` sequences literal where `g_filename_from_uri` would NULL; only reachable
  with malformed `%` in a file URI argument.
- Group-header padding (`[Desktop Entry ]`) treated as a different group
  (refusal); machine-written case desktops never pad.
- DBus-activation/portal launch paths are frontier by declaration, unmodelled.

## 7. Routed interface notes

- R98MMutC1: final sha pin, arg_model anchor line ~209, uniqueness map over the
  single-implementation helpers, atomic-probe warning, refusal detail tokens.
- R98MExecCounter: --json scoring ack; rc discipline (only 0 and 2 ever;
  no-POSitional usage error = stderr + rc 2 with empty stdout); new sha;
  settle-poll + single-write recorder requirements.
- R98MExecOracle: recorder atomicity + async settle-poll (3.7), query drop for
  fresh u-anchor variants, dup-last and Hidden-launch confirmations.
- L1 pre-freeze wording fixes this report asks for: rule 1 "Hidden refusal"
  strike; rule 1 "duplicate key keeps the first" -> "the last"; rule 1's
  refusal-line example `desktop=...` vs contract 1 `detail=<...>` - I emit
  `detail=`; the frozen `bad-06-not-keyfile` oracle inconsistency (valid
  desktop block, desktop-file expect) R98MMutC1 routed - my launch there
  matches gio.

## 8. Tooling and hygiene

No tool installed or upgraded (host python3 + `/usr/bin/gio` sufficed); no
pacman transaction (host-wide pause respected); no sudo; no network beyond the
L1's already-fetched `fetch/` bytes (no new URL opened); no writes outside the
owned files, this report, and the seat scratch
`/fast/scratch/hyaku/mado-r98/R98MExecTool` (deleted before yield; decisive
receipts embedded above). ASCII-only committed artifacts.
