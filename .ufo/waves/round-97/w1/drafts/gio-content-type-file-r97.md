source: S522 (GLib 2.90.1 glocalfileinfo.c b006a93d8a9733ad9245aba396ca7e3ee42019e214f3addd6e873dbd7d334497, 93614 B - re-scoped this round: the stat-branch order, the stat-failure guard, the name-only guess and the sniff that `standard::content-type` runs), S526 (GLib 2.90.1 gcontenttype-fdo.c 8a5b4f475947a9de2e0ca34e60b0dc31f5c56a2d7e0a9fe8cf84002aca8a2d7c, 32741 B - new scope: the sniff-length function `_g_unix_content_type_get_sniff_len` at :54-67 and the Unix `g_content_type_from_mime_type_impl` it feeds at :551-565), S527 (`gio(1)` GLib 2.90.1 manual, `/usr/share/man/man1/gio.1.gz` sha256 810077be12cf2df5006db1e1b9b967f6c505930033c68aa9cfc964281906a565, 4961 B gz / 18793 B plain (measured here; the L1 receipt's `decompressed=` cell reads 13688 - routed in the seat report, the digest 84b3cdad... matches both), 781 lines - the `info` command, `-a`/`--attributes`, `-n`/`--nofollow-symlinks` and the exit-status sentence), S518 (gcontenttype-fdo.c, the name-only guess and its uncertain flag), S521 (gcontenttype-fdo.c, the guess given data and the arbitration), S524 (xdgmimemagic.c fcb1eafe748d3dc18f7f405d1078c8a32e313d23d2fab86b0f12e609ac2ce742, the text magic step the sniff length is read from), S525 (shared-mime-info spec 0.21 section 2.5 at e00fa00e69b1e95ad8642d05fc5023c26f859bdaf8bdda3e091a55feb016c61e), S519 (xdgmimecache.c ccda4366a1b3d6feb81c6213fde4885b547189e7cfe612f81799d8c1f298db69, the cache magic step and its max extent), S520 (xdgmimeint.c c2364aa825a761255fd6c3390a78c94f06eeaf9babeb07b5ea489ba4cef92f29, the binary/text fallback), S515/S516 (xdgmimeglob.c 38ed862316a6e948b2b45b93a27c463e1b1e162a2200cf4eeb1e2af8e2980734 / xdgmimecache.c, the name step), S505 (xdgmime.c afb1c1c1ba726a9fb8d8732f4031f5aa85a67ec3b7a2f989b617e4f4f5282410 with xdgmimealias.c a1e67ae3604c437b8516d6bc4c67f31afea6fc58393b9afe1c42a8b424111394, the alias table the branch answers pass through)
verified-at: 2026-11-07 - `glib2 2.90.1-1`, `shared-mime-info 2.5.1-2`; the oracle `/usr/bin/gio` sha256 d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462, `gio --version` 2.90.1; the fetched bytes re-hashed in this round's scratch against the L1 receipt (`gcontenttype-fdo.c` 8a5b4f47, `glocalfileinfo.c` b006a93d). The observed answers of section 7 are this round's read-only runs of that binary (36 host-database rows, 13 private-database rows); the candidate's own legs are the L1's C1 receipt, not this draft.
recheck: 90d - re-pull `glocalfileinfo.c` and `gcontenttype-fdo.c` at the next GLib tag that changes either (2.90.1 is the pin); also when `glib2` leaves 2.90.1-1 or `shared-mime-info` leaves 2.5.1-2 (the host's `mime/` bytes and the max extent are part of every host answer), and when the `gio` CLI's option spelling moves. A change to the branch order, the `!fast && result_uncertain && path != NULL` gate, the 16384 clamp or the `errsv != EACCES` guard flips this entry.
covers: what GIO 2.90.1 answers as `standard::content-type` and `standard::fast-content-type` for a **path** - the eight-branch stat order that answers `inode/symlink`, `inode/directory`, `inode/chardevice`, `inode/blockdevice`, `inode/fifo`, `application/x-zerosize` and `inode/socket` before any guess; the alias rewrite every branch answer passes through; the basename-only guess and the three states that make it uncertain; the sniff gate (`!fast`, uncertain, path present); the sniff length (the database's max extent, 0 or > 16384 clamped up/down to 16384); the `O_NOATIME` open with its EPERM retry and the read that keeps the name-only answer when it fails; the `EACCES`-tolerant stat failure and the `ELOOP`/broken-link answer; and the CLI faces `gio info -a standard::content-type` and `-a standard::fast-content-type`.

# The content type GIO 2.90.1 reports for a path, not for bytes

Rounds 94-96 modelled `g_content_type_guess (name, data, len)` - the name step, the magic step
and the text database. A file manager does not call that function. It asks
`GFileInfo` for `standard::content-type`, and `GLocalFileInfo` answers from a stat first and
from the guess second. This entry states that caller: the branch order, the gate that decides
whether the file is opened at all, the sniff length the database dictates, the two public
attributes, and what the `gio` CLI prints. Line numbers are `glocalfileinfo.c` (:1300-1382)
and `gcontenttype-fdo.c` (:54-66, :551-565, :567-690) as named in the front matter; the
manual's page lines are those of the decompressed `gio.1`. Every behavioural statement carries
a source row, a located line of one, or a probe row of section 7.

## 1. Question and scope

- **The surface.** `glocalfileinfo.c:2053` reads the attribute id
  `G_FILE_ATTRIBUTE_ID_STANDARD_CONTENT_TYPE`; `:2065` calls
  `get_content_type (basename, path, stat_ok ? &statbuf : NULL, is_symlink, symlink_broken,
  flags, FALSE)` and `:2080` the same call with `fast = TRUE` for
  `G_FILE_ATTRIBUTE_ID_STANDARD_FAST_CONTENT_TYPE`. Both attributes can be asked for at once
  and are computed by two separate calls; `--fast` in the lane tool selects the second.
- **What the CLI shows.** `gio info [OPTION...] LOCATION...` (`gio.1` page line 48, the command
  at 172); `-a, --attributes=<ATTRIBUTES>` selects attributes (page `:195`; `The attributes to get.` at
  `:198`); `-n, --nofollow-symlinks` means `follow symbolic links.` is off (page `:209`, `:212`).
  The page itself names no content-type attribute (`grep -c content-type` over the decompressed
  manual is 0; its only attribute example is `standard::icon` at `:200`, `:244`, `:661`), so the two
  attribute names below are `glocalfileinfo.c`'s attribute ids (`:2053`, `:2055`) and the measured
  output, not the manual's.
  Without `-a` the tool prints everything, which includes both content-type lines (probe H-default).
- **What is out of scope.** The guess over raw bytes is r94-r96's; the magic cache and text
  formats are r95/r96's; `standard::icon` and the other attributes are out; the `atime` effect
  of the `O_NOATIME` open is not measured; a path whose `lstat` fails with an errno other than
  `EACCES` is refused by GIO and scored only as a refusal (section 2.5).
- **Evidence class.** Section 2 carries located source lines; Section 7 carries the oracle's answers on
  fixtures this draft builds from the entry's own recipe; section 9 names the frozen set and its pins
  but carries no number this draft did not measure (round-96 D2).

## 2. The rules

### 2.1 The stat branches, in order

`get_content_type` (`:1300`) tests eight states before it guesses. `statbuf == NULL` skips
branches 2-7 entirely (see section 2.5); `is_symlink` and `symlink_broken` are decided before the call
(`:1964`, `:1994`).

| # | state | answer | source | anchor | quote |
|---|---|---|---|---|---|
| 1 | a symlink that is broken **or** queried with `NOFOLLOW_SYMLINKS` | `inode/symlink` | S522 | glocalfileinfo.c:1308-1310 | `if (is_symlink && (symlink_broken || (flags & G_FILE_QUERY_INFO_NOFOLLOW_SYMLINKS))) return g_content_type_from_mime_type ("inode/symlink");` |
| 2 | `S_ISDIR` | `inode/directory` | S522 | glocalfileinfo.c:1311 | `else if (statbuf != NULL && S_ISDIR(_g_stat_mode (statbuf))) return g_content_type_from_mime_type ("inode/directory");` |
| 3 | `S_ISCHR` (not Win32) | `inode/chardevice` | S522 | glocalfileinfo.c:1314 | `else if (statbuf != NULL && S_ISCHR(_g_stat_mode (statbuf)))` |
| 4 | `S_ISBLK` (not Win32) | `inode/blockdevice` | S522 | glocalfileinfo.c:1316 | `else if (statbuf != NULL && S_ISBLK(_g_stat_mode (statbuf)))` |
| 5 | `S_ISFIFO` (not Win32) | `inode/fifo` | S522 | glocalfileinfo.c:1318 | `else if (statbuf != NULL && S_ISFIFO(_g_stat_mode (statbuf)))` |
| 6 | `S_ISREG` **and** size 0 (not Win32) | `application/x-zerosize` | S522 | glocalfileinfo.c:1320-1326 | `else if (statbuf != NULL && S_ISREG(_g_stat_mode (statbuf)) && _g_stat_size (statbuf) == 0) ... return g_content_type_from_mime_type ("application/x-zerosize");` |
| 7 | `S_ISSOCK` (where defined) | `inode/socket` | S522 | glocalfileinfo.c:1328-1330 | `#ifdef S_ISSOCK else if (statbuf != NULL && S_ISSOCK(_g_stat_mode (statbuf))) return g_content_type_from_mime_type ("inode/socket");` |
| 8 | anything else (a non-empty regular file, or no statbuf at all) | the guess path of section 2.3-section 2.5 | S522 | glocalfileinfo.c:1332-1381 | `else { char *content_type; gboolean result_uncertain; content_type = g_content_type_guess (basename, NULL, 0, &result_uncertain);` |

The order is observable and it beats the name: a FIFO named `*.png` is `inode/fifo`, an empty
file named `*.png` is `application/x-zerosize`, a directory named `*.png` is
`inode/directory` (probes H-fifo_png, H-zero_png, H-sub2_png). Branch 6 is not "empty file":
it is "regular and size 0", and it sits **after** the device and FIFO tests, so `S_ISCHR` on
`/dev/null` wins over the zero size (`inode/chardevice`, probe H-chardev).

### 2.2 Every branch answer is unaliased first

Branches 1-7 all return through `g_content_type_from_mime_type`, which is a wrapper in
`gcontenttype.c:291-295` around `g_content_type_from_mime_type_impl`. On Unix that
implementation is `gcontenttype-fdo.c:551-565`, and it is **not** the identity:

| rule | source | anchor | quote |
|---|---|---|---|
| the Unix impl comments its own rule | S526 | gcontenttype-fdo.c:559 | `/* mime type and content type are same on unixes */` |
| it unaliases through the database's alias table | S526 | gcontenttype-fdo.c:560 | `umime = g_strdup (xdg_mime_unalias_mime_type (mime_type));` |
| the alias table is xdgmime's, read from the reachable directories | S505 | xdgmimealias.c (alias qsort/bsearch; the reader of `mime/aliases`) | - |

This is observable, not decorative: with a private database whose `mime/aliases` holds
`inode/symlink application/x-aliased` (alias first, canonical second), `gio info -n` on an
untouched symlink answers `application/x-aliased`; with the two fields reversed it answers
`inode/symlink` (probes D-alias_map, D-alias_rev). None of the three strings above is aliased
in the host database, which is why the ordinary answers read as written (probes H-link_nofollow,
H-broken).

### 2.3 The name-only guess and the three uncertain states

Branch 8 calls the guess with `(basename, NULL, 0)` (`:1337`) - no bytes, so the name step alone
answers. `g_content_type_guess_impl` (`gcontenttype-fdo.c:567`) sets `*result_uncertain = FALSE`
first (`:585`) and only these states set it TRUE:

| state | answer | uncertain | source | anchor |
|---|---|---|---|---|
| the name ends in `/` | `inode/directory` | TRUE | S518 | gcontenttype-fdo.c:597-603 |
| exactly one name type | that type | FALSE | S518 | gcontenttype-fdo.c:613-620 |
| no name type | `application/octet-stream` | TRUE | S518 | gcontenttype-fdo.c:641-648 |
| several name types | the first after the weight sort | TRUE | S518 | gcontenttype-fdo.c:675-683 |

The trailing-slash branch is unreachable through this caller in practice: a path ending in `/`
that is not a directory fails `stat` with `ENOTDIR` and GIO refuses it (probe H-enotdir), and
`basename` never ends in `/` otherwise. The two live states are "exactly one" (never sniffed)
and "zero or several" (sniffed unless `--fast`).

The name types themselves are the glob database's (S515 text / S516 cache, r94), so a case
environment with an empty `mime/` tree has zero name types for every basename and therefore
always reaches the sniff.

### 2.4 The sniff gate, the length, and the read

| rule | source | anchor | quote |
|---|---|---|---|
| the gate is `fast`, the uncertain flag and a non-NULL path | S522 | glocalfileinfo.c:1340 | `if (!fast && result_uncertain && path != NULL)` |
| the buffer is a 16384-byte stack array | S522 | glocalfileinfo.c:1346 | `guchar sniff_buffer[16384];` |
| the wanted length is the database's max extent | S522 | glocalfileinfo.c:1353 | `sniff_length = _g_unix_content_type_get_sniff_len ();` |
| the max extent is `xdg_mime_get_max_buffer_extents ()` under the gio-xdgmime lock | S526 | gcontenttype-fdo.c:61 | `size = xdg_mime_get_max_buffer_extents ();` |
| 0 or anything above 16384 becomes 16384 (never 0) | S522 | glocalfileinfo.c:1354-1355 | `if (sniff_length == 0 || sniff_length > sizeof (sniff_buffer)) sniff_length = sizeof (sniff_buffer);` |
| the file is opened read-only, no-atime, close-on-exec | S522 | glocalfileinfo.c:1358 | `fd = g_open (path, O_RDONLY | O_NOATIME | O_CLOEXEC, 0);` |
| an `EPERM` open is retried without `O_NOATIME` | S522 | glocalfileinfo.c:1360-1362 | `if (fd < 0 && errsv == EPERM) ... fd = g_open (path, O_RDONLY | O_CLOEXEC, 0);` |
| one read of at most `sniff_length` bytes | S522 | glocalfileinfo.c:1368 | `res = read (fd, sniff_buffer, sniff_length);` |
| a negative result keeps the name-only answer; otherwise the bytes are re-guessed with the same basename | S522 | glocalfileinfo.c:1370-1373 | `if (res >= 0) { ... content_type = g_content_type_guess (basename, sniff_buffer, res, NULL);` |

Four consequences follow, each measured in Section 7:

1. **`--fast` never opens the file.** The gate's first term is `!fast`; `:2080` passes `TRUE`.
   A file with no name type and a magic-matchable body answers `application/octet-stream` on
   the fast attribute and the magic type on the full one (probes D-near_fast vs D-near_off100).
2. **The sniff length is the database's, not the file's.** A database whose only rule needs
   extent 103 asks the read for 103 bytes (`:1368` reads `sniff_length`, which `:1353` set from
   that extent); a rule at offset 20000 makes the extent 20003 and the clamp asks the read for
   16384, so the rule can never fire for a GIO caller although the bytes are there (probes
   D-near_off100, D-far_off20000). The boundary is exact: extent 16383 reads 16383 and matches;
   extent 16385 clamps to 16384 and still matches because the compare allows
   `i + value_length == len`; extent 16388 clamps to 16384 and does not (probes D-b16380,
   D-b16382, D-b16385). Only the upper side is observable: every matchlet lies inside the extent
   by construction, so reading more than the extent can never add a match - a model may read a
   flat 16384 and answer identically; the difference is I/O, not the answer.
3. **The name still wins after the sniff.** The re-guess carries the same `basename`, so
   `n_name_mimetypes == 1` short-circuits again: a text file named `*.png` answers `image/png`
   with the sniff never reached (probe H-e_png), and a `.txt` file full of PNG bytes answers
   `text/plain` (probe H-mis_txt).
4. **The result is a type, not a type and a flag.** `:1373` passes `NULL` for
   `result_uncertain`, so nothing downstream can see whether the answer was certain; the CLI
   prints only the type (probes H-unread_bin vs H-plain_bin differ in answer, not in shape).

The max extent's own source depends on the mode: the text magic parser records
`value_length + offset + range_length` per matchlet and returns the maximum (S524
`xdgmimemagic.c:714`, `:648`; r96 section 2.8 measured 18730 on this host, above the clamp); the cache
reader answers the same question from `mime.cache` (S519). Either way the number is a property
of the database, so two hosts with different databases sniff different lengths.

### 2.5 When the stat fails: `EACCES` is tolerated, everything else is refused

`_g_local_file_info_get` `lstat`s the path (`:1932-1936`, the failure test at `:1937`). The failure handler has one exception:

| rule | source | anchor | quote |
|---|---|---|---|
| a failed `lstat` does not always bail out | S522 | glocalfileinfo.c:1937-1942 | `if (res == -1) { int errsv = errno; /* Don't bail out if we get Permission denied (SELinux?) */ if (errsv != EACCES)` |
| the tolerated case leaves `stat_ok` FALSE | S522 | glocalfileinfo.c:1956 | `stat_ok = res != -1;` |
| every attribute path then receives `NULL` instead of a stat buffer | S522 | glocalfileinfo.c:2065 | `get_content_type (basename, path, stat_ok ? &statbuf : NULL, is_symlink, symlink_broken, flags, FALSE)` |
| any other errno sets a `G_IO_ERROR` and returns `NULL` | S522 | glocalfileinfo.c:1944-1951 | `g_set_error (error, G_IO_ERROR, g_io_error_from_errno (errsv), _("Error when getting information for file ...")` |
| with a symlink and no `NOFOLLOW`, a failed follow `stat` marks the target broken | S522 | glocalfileinfo.c:1987-1994 | `/* Report broken links as symlinks */ if (res != -1) { statbuf = statbuf2; stat_ok = TRUE; } else symlink_broken = TRUE;` |

Measured consequences:

- **`EACCES` on the path itself** (a directory in the path is mode 000): `gio info` still prints
  an attribute block, answers from the name only, and exits 0 - `application/octet-stream` for
  a basename with no name type whose body is plain text (probe H-eacces). A true stat is
  impossible here (`stat` and `head` both fail with `EACCES`), so this is the name-only path,
  not a read of the file.
- **`ENOENT` or `ENOTDIR`**: no attribute line, the message
  `Error when getting information for file "...": No such file or directory`, exit 2 (probes
  H-missing, H-enotdir). The manual documents only `0` and nonzero (`gio.1:775`); the `2` is
  the CLI's mapping of the `G_IO_ERROR`, measured here, and the lane tool copies it.
- **A symlink loop**: `lstat` succeeds (the link exists) and the follow `stat` fails with
  `ELOOP`, so `symlink_broken` is TRUE and the answer is `inode/symlink`, exit 0 (probes
  H-loop, H-loop_n; `stat -L` on the same path fails). A loop is therefore **inside** this
  surface, and a broken link is indistinguishable from it at this attribute.
- **A symlink to a device, FIFO, socket or directory** is followed and answers that branch
  (probes H-fifolink, H-socklink, H-dirlink); `-n` answers `inode/symlink` first (branch 1).

### 2.6 The guess-combination recap (not restated here)

The re-guess at `:1373` is exactly r96's section 2.10 table, with the *same* basename: one name type
wins; a sniffed priority >= 80 wins otherwise (`gcontenttype-fdo.c:654`); else the first name
type that is a subclass of the sniffed type (`:663`); else the first name type, and the answer
is uncertain (r94-r96 own those rows). Three of its rows are visible from this surface and are
worth naming because they look surprising from the CLI:

| observation | what it looks like from `gio info` | why |
|---|---|---|
| a desktop-file body under a non-`.desktop` name | `text/plain`, never `application/x-desktop` | the rewrite at `gcontenttype-fdo.c:636-637` fires because `filename != NULL` (probe H-d_bin) |
| the same body under `*.desktop` | `application/x-desktop` | one name type short-circuits before the sniff (probe H-d_desktop) |
| a name with two types and a low-priority magic hit | the first name type after the weight sort | `:675-683` (r94's rows) |

## 3. Where the naive reading is wrong

| # | naive reading | measured | probe |
|---|---|---|---|
| a | `standard::content-type` reports the file's contents | the stat branch and the name dominate; contents are read only for an uncertain name | H-e_png, H-mis_txt, H-zero_png, H-fifo_png |
| b | an unreadable file is an error | `EACCES` is tolerated (name-only answer, exit 0); only other errnos refuse | H-eacces vs H-missing |
| c | a symlink loop is a stat error | the loop answers `inode/symlink`, exit 0 | H-loop |
| d | the fast attribute is the full one without a read | it also skips the sniff length, so the answer can differ in *type* | H-fast_d_bin, D-near_fast |
| e | `inode/*` answers are constants | they pass through the alias table | D-alias_map |
| f | the sniff reads the first 16 KiB | it reads `min(database max extent, 16384)`, with 0 -> 16384 | D-near_off100, D-b16380/82/85 |
| g | the CLI reveals the uncertainty | it prints a type only; two different states share one line shape | H-unread_bin vs H-plain_bin |
| h | the CLI's exit status is the library's | the manual promises 0/nonzero; the measured refusal is 2, a CLI mapping | gio.1:775, H-missing |

## 4. Operator consequences

1. **A file manager's type is not a detector.** A PNG named `.txt` is `text/plain`; text named
   `.png` is `image/png`; an empty file is `application/x-zerosize` whatever its name. Anything
   that needs the content must call the guess itself or read the bytes.
2. **An unreadable path is answered, not refused.** A mode-000 parent still yields a type (from
   the name), so a scan that treats "got a type" as "file is readable" is wrong.
3. **A loop and a broken link look alike.** Both answer `inode/symlink`; distinguishing them
   needs the target, not the attribute.
4. **The database decides how much is sniffed.** A distro whose `mime/magic` needs 18730 bytes
   still gets 16384 from GIO, so range-only rules beyond that offset never fire for desktop
   callers while they do for `g_content_type_guess` callers reading the whole file.
5. **`--fast` is not a cheap full type.** It can differ in the type itself, not only in cost;
   a caller that shows the fast type as the type is showing the name-only answer.
6. **The alias table reaches further than the guess.** A hand-edited `mime/aliases` rewrites
   `inode/symlink` and friends too, which no name- or magic-level model would predict.

## 5. The tool and how to run it

`tools/mado-filetype.py` (target path; the in-wave draft is
`.ufo/waves/round-97/build/mado-filetype.py`) is read-only: it stats paths, loads the reachable
`mime/` databases, and reads a file only when the gate of section 2.4 opens. It loads round 94's
`tools/mado-mimeglob.py`, round 95's `tools/mado-mimesniff.py` and round 96's
`tools/mado-mimetext.py` from its own directory, pinned by sha256.

```
mado-filetype.py PATH... [--follow|--nofollow] [--fast] [--data-home D | --data-home-unset]
                 [--data-dirs LIST | --data-dirs-unset] [--home H | --home-unset] [--json]
mado-filetype.py --selftest
```

``sh
python3 -I tools/mado-filetype.py notes.txt report.png
python3 -I tools/mado-filetype.py --fast --nofollow /tmp/x
python3 -I tools/mado-filetype.py --data-home /tmp/k/dh --data-dirs /tmp/k/d1:/tmp/k/d2 a.bin
python3 -I tools/mado-filetype.py --selftest          # checks=N failed=0, rc 0
``

Output (exit 0): one `MADO_FILETYPE: <type> attr=<full|fast> mode=<follow|nofollow>
path=<escaped>` line per path, plus one `MADO_FILETYPE_DIRS: db=<cache|text|none>` line.

**Verdict map.**

| state | tool exit | tool line |
|---|---|---|
| every path answered (any branch of section 2.1, the guess, a tolerated `EACCES`) | 0 | the type equals `gio info -a <attr> [-n]`'s line (section 7) |
| a path whose `lstat` fails with an errno other than `EACCES` (missing, `ENOTDIR`) | 2 | `MADO_FILETYPE: ERROR stat path=<escaped>` for that path; every other path is still printed |
| no PATH | 2 | `mado-filetype: setup error: ...` on stderr |

`--selftest` prints `MADO_FILETYPE_SELFTEST_FAIL: <label>` per failing check and
`MADO_FILETYPE_SELFTEST: checks=N failed=0` (stdout, N >= 20), exit 0/1.

## 6. Limits and unknowns

1. **Two attributes only.** `standard::content-type` and `standard::fast-content-type`; every
   other attribute (`standard::icon`, `unix::*`, `time::*`) is out of the model.
2. **The `O_NOATIME` retry is modelled, the `atime` effect is not.** The tool does not set
   `O_NOATIME`; a receipt cannot see which open a kernel chose.
3. **`EACCES` is a shape, not a permission model.** The tool reproduces the tolerated branch by
   stat'ing and, on `EACCES`, answering from the name and attempting no read; it does not
   reproduce SELinux specifics, uid/gid effects or a `CAP_DAC_READ_SEARCH` caller. A harness that
   runs as root cannot construct the shape at all (root bypasses the mode bits; probes here ran as
   uid 1000), so a `readerr` case that means "EACCES" must either declare a non-root harness or be
   labelled by what the oracle answers under the harness that measured it.
4. **The sniff length is the reachable database's.** A distro patch to `max_buffer_extents` is
   scored as upstream; a `mime.cache` in any reachable directory changes both the length and the
   magic step (r95's surface).
5. **`g_content_type_from_mime_type`'s alias step needs the alias table.** A case that declares
   `mime/aliases` without the text/alias files the guess needs is not a supported fixture; the
   frozen set must either carry a consistent tree or no alias edge at all.
6. **The CLI's exit `2` is a `gio` CLI mapping**, not a `GLocalFileInfo` fact; the tool copies
   the mapping as a surface convention and the entry says so (section 2.5).
7. **Symlink handling needs both stats.** The tool must `lstat`, then (when following) `stat`,
   and treat a failed follow `stat` as `symlink_broken` - not as a refusal (section 2.5, probes
   H-loop/H-broken). A tool that folds `ELOOP` into its ERROR line diverges on a reachable path.
8. **Not scored: a path that stats as a directory but whose basename ends in `/`.** The guess's
   trailing-slash branch (`:597-603`) is unreachable through this caller; no case construction
   observed here separates it.
9. **Labels come from the installed `gio`** (sha256 d2164260..., glib2 2.90.1-1) and the host's
   `shared-mime-info` 2.5.1-2; a distro patch is scored as upstream.
10. **The manual is a surface, not a specification of the attributes.** `gio(1)` carries no
    `content-type` text and no version or date in its `.TH` line, so S527 grounds the `info`
    command, `-a`, `-n` and the exit-status sentence only; the attribute names are
    `glocalfileinfo.c`'s ids, and the version binding is the owning package (glib2 2.90.1-1).
11. **The candidate's own legs are not this entry's.** Section 7 is the oracle's answers on fixtures
    built here; the frozen case, mutant, fresh and host legs are the L1's C1 receipt.

## 7. Measured results (this round's read-only probes)

`R97MScribeEntry` built every fixture under scratch and ran the oracle once per row; the
transcript is in this round's seat report, section 4 (same bytes, same order).
Every host row used `env -i LC_ALL=C HOME=<empty> /usr/bin/gio info -a <attr> [-n] <path>` with
`XDG_DATA_HOME` and `XDG_DATA_DIRS` unset, i.e. the host's own database (`/usr/share/mime`,
cache mode); every `DB` row pointed `XDG_DATA_DIRS` at a private tree and `XDG_DATA_HOME` at an
empty directory.

Host facts: `gio --version` 2.90.1; `glib2 2.90.1-1`; `shared-mime-info 2.5.1-2`;
`/usr/share/mime/mime.cache` present.

### 7.1 The host database (36 rows)

| probe | fixture | oracle answer | exit |
|---|---|---|---|
| H-a_txt | `a.txt`, `hello\n` | `text/plain` | 0 |
| H-w_png | `w.png`, PNG signature + digits | `image/png` | 0 |
| H-e_png | `e.png`, `hello\n` | `image/png` | 0 |
| H-mis_txt | `mis.txt`, PNG signature + digits | `text/plain` | 0 |
| H-d_desktop | `d.desktop`, `[Desktop Entry]` body | `application/x-desktop` | 0 |
| H-d_bin | `d.bin`, same body | `text/plain` | 0 |
| H-plain_bin | `plain.bin`, `hello\n` | `text/plain` | 0 |
| H-zero_bin | `zero.bin`, empty | `application/x-zerosize` | 0 |
| H-zero_png | `zero.png`, empty | `application/x-zerosize` | 0 |
| H-sub | directory `sub` | `inode/directory` | 0 |
| H-sub_slash | directory `sub/` | `inode/directory` | 0 |
| H-sub2_png | directory `sub2.png` | `inode/directory` | 0 |
| H-fifo | FIFO `fifo.bin` | `inode/fifo` | 0 |
| H-fifo_png | FIFO `fifo.png` | `inode/fifo` | 0 |
| H-sock | unix socket `sock.bin` | `inode/socket` | 0 |
| H-chardev | `/dev/null` | `inode/chardevice` | 0 |
| H-unread_bin | `unread.bin` mode 000, `garbage\n` | `application/octet-stream` | 0 |
| H-unread_png | `unread.png` mode 000, `hello\n` | `image/png` | 0 |
| H-link_follow | `link.txt -> a.txt` | `text/plain` | 0 |
| H-link_nofollow | same, `-n` | `inode/symlink` | 0 |
| H-broken | `broken.txt -> missing.txt` | `inode/symlink` | 0 |
| H-dirlink | `dirlink -> sub` | `inode/directory` | 0 |
| H-dirlink_n | same, `-n` | `inode/symlink` | 0 |
| H-fifolink | `fifolink -> fifo.bin` | `inode/fifo` | 0 |
| H-socklink | `socklink -> sock.bin` | `inode/socket` | 0 |
| H-loop | `loop1 -> loop2 -> loop1` | `inode/symlink` | 0 |
| H-loop_n | same, `-n` | `inode/symlink` | 0 |
| H-missing | `nope.bin` | no attribute line, `Error when getting information ...` | 2 |
| H-enotdir | `a.txt/x` | no attribute line, same message | 2 |
| H-eacces | `noax/f.bin` with `noax` mode 000 | `application/octet-stream` | 0 |
| H-two_locations | `a.txt` and `w.png` in one call | `text/plain` then `image/png`, order kept | 0 |
| H-default | `near.zzz` under `db1`, no `-a` at all | both lines: full `application/x-near`, fast `application/octet-stream` | 0 |
| F-e_png | `e.png` on `standard::fast-content-type` | `image/png` | 0 |
| F-d_bin | `d.bin` on the fast attribute | `application/octet-stream` | 0 |
| F-unread_bin | `unread.bin` on the fast attribute | `application/octet-stream` | 0 |
| F-chardev | `/dev/null` on the fast attribute | `inode/chardevice` | 0 |

### 7.2 Private text databases (13 rows)

Fixture recipe (bytes are exact; `<n>` is the decimal offset in ASCII):
`MIME-Magic\0\n[80:<type>]\n><n>=<00 02>AB\n`; the `globs2` line is `50:application/x-zz:*.zz\n`;
the aliases lines are given per row. The data files place `AB` at the offset the rule names.

| probe | database | file | oracle answer |
|---|---|---|---|
| D-near_off100 | rule at 100 -> `application/x-near` (extent 103) | `near.zzz`, `.` x100 + `AB` | `application/x-near` |
| D-near_fast | same, fast attribute | same | `application/octet-stream` |
| D-far_off20000 | rule at 20000 -> `application/x-far` (extent 20003) | `far.zzz`, `A` x20000 + `AB` | `text/plain` |
| D-off100_other | rule at 100 | `far.zzz` (no `AB` at 100) | `text/plain` |
| D-name_zz | rule at 100 + `globs2` `*.zz` | `near.zz`, `.` x100 + `AB` | `application/x-zz` |
| D-name_zz_fast | same, fast attribute | same | `application/x-zz` |
| D-b16380 | rule at 16380 (extent 16383) | `AB` at 16380 | `application/x-b16380` |
| D-b16382 | rule at 16382 (extent 16385 -> clamp 16384) | `AB` at 16382 | `application/x-b16382` |
| D-b16385 | rule at 16385 (extent 16388 -> clamp 16384) | `AB` at 16385 | `text/plain` |
| D-alias_map | `mime/aliases` = `inode/symlink application/x-aliased` | `link.txt`, `-n` | `application/x-aliased` |
| D-alias_rev | `mime/aliases` = `application/x-aliased inode/symlink` | same, `-n` | `inode/symlink` |
| D-none_db | no `mime/` file at all | `near.zzz` | `text/plain` |
| D-none_chardev | no `mime/` file at all | `/dev/null` | `inode/chardevice` |

The three boundary rows are read together: 16383 (no clamp) matches; 16385 (clamped, exact fit
at the buffer end) matches; 16388 (clamped, two bytes short) does not. The clamp is a read
length, so the compare's `i + value_length > len` rule turns "just past 16384" into "no match",
not into an error.

### 7.3 What these rows do and do not establish

They establish the branch order, the gate, the clamp, the alias step and the refusal shapes
against the installed binary. They do **not** establish any candidate's agreement: a tool is
scored by the L1's C1 counter, whose case labels are produced by the same oracle on frozen
fixtures (contract 2 of the round), and this draft carries no count from that run.

## 8. Located quotes for the registry rows

Every quote below is a whitespace-collapsed line of the fetched bytes (S522, S526, S527) and is
<= 25 words; the anchors are the line numbers of section 2's tables.

| rule | row | anchor | quote |
|---|---|---|---|
| the branch function | S522 | glocalfileinfo.c:1300 | `get_content_type (const char *basename,` |
| symlink broken or nofollow | S522 | glocalfileinfo.c:1308 | `if (is_symlink &&` |
| the nofollow flag test | S522 | glocalfileinfo.c:1309 | `(symlink_broken || (flags & G_FILE_QUERY_INFO_NOFOLLOW_SYMLINKS)))` |
| symlink answer | S522 | glocalfileinfo.c:1310 | `return g_content_type_from_mime_type ("inode/symlink");` |
| directory branch | S522 | glocalfileinfo.c:1311 | `else if (statbuf != NULL && S_ISDIR(_g_stat_mode (statbuf)))` |
| character device branch | S522 | glocalfileinfo.c:1314 | `else if (statbuf != NULL && S_ISCHR(_g_stat_mode (statbuf)))` |
| block device branch | S522 | glocalfileinfo.c:1316 | `else if (statbuf != NULL && S_ISBLK(_g_stat_mode (statbuf)))` |
| FIFO branch | S522 | glocalfileinfo.c:1318 | `else if (statbuf != NULL && S_ISFIFO(_g_stat_mode (statbuf)))` |
| zero-size regular branch | S522 | glocalfileinfo.c:1320 | `else if (statbuf != NULL && S_ISREG(_g_stat_mode (statbuf)) && _g_stat_size (statbuf) == 0)` |
| zerosize answer | S522 | glocalfileinfo.c:1325 | `return g_content_type_from_mime_type ("application/x-zerosize");` |
| socket branch | S522 | glocalfileinfo.c:1329 | `else if (statbuf != NULL && S_ISSOCK(_g_stat_mode (statbuf)))` |
| the name-only guess | S522 | glocalfileinfo.c:1337 | `content_type = g_content_type_guess (basename, NULL, 0, &result_uncertain);` |
| the sniff gate | S522 | glocalfileinfo.c:1340 | `if (!fast && result_uncertain && path != NULL)` |
| the buffer | S522 | glocalfileinfo.c:1346 | `guchar sniff_buffer[16384];` |
| the wanted length | S522 | glocalfileinfo.c:1353 | `sniff_length = _g_unix_content_type_get_sniff_len ();` |
| the clamp test | S522 | glocalfileinfo.c:1354 | `if (sniff_length == 0 || sniff_length > sizeof (sniff_buffer))` |
| the clamp value | S522 | glocalfileinfo.c:1355 | `sniff_length = sizeof (sniff_buffer);` |
| the no-atime open | S522 | glocalfileinfo.c:1358 | `fd = g_open (path, O_RDONLY | O_NOATIME | O_CLOEXEC, 0);` |
| the EPERM retry | S522 | glocalfileinfo.c:1362 | `fd = g_open (path, O_RDONLY | O_CLOEXEC, 0);` |
| the read | S522 | glocalfileinfo.c:1368 | `res = read (fd, sniff_buffer, sniff_length);` |
| the re-guess | S522 | glocalfileinfo.c:1373 | `content_type = g_content_type_guess (basename, sniff_buffer, res, NULL);` |
| the stat failure test | S522 | glocalfileinfo.c:1937 | `if (res == -1)` |
| the EACCES comment | S522 | glocalfileinfo.c:1941 | `/* Don't bail out if we get Permission denied (SELinux?) */` |
| the EACCES exception | S522 | glocalfileinfo.c:1942 | `if (errsv != EACCES)` |
| stat_ok follows the stat | S522 | glocalfileinfo.c:1956 | `stat_ok = res != -1;` |
| the symlink test | S522 | glocalfileinfo.c:1964 | `is_symlink = stat_ok && S_ISLNK (_g_stat_mode (&statbuf));` |
| broken links | S522 | glocalfileinfo.c:1987 | `/* Report broken links as symlinks */` |
| symlink_broken set | S522 | glocalfileinfo.c:1994 | `symlink_broken = TRUE;` |
| the full attribute call | S522 | glocalfileinfo.c:2065 | `char *content_type = get_content_type (basename, path, stat_ok ? &statbuf : NULL, is_symlink, symlink_broken, flags, FALSE);` |
| the fast attribute call | S522 | glocalfileinfo.c:2080 | `char *content_type = get_content_type (basename, path, stat_ok ? &statbuf : NULL, is_symlink, symlink_broken, flags, TRUE);` |
| the sniff-length function | S526 | gcontenttype-fdo.c:55 | `_g_unix_content_type_get_sniff_len (void)` |
| the max extent call | S526 | gcontenttype-fdo.c:61 | `size = xdg_mime_get_max_buffer_extents ();` |
| the Unix identity comment | S526 | gcontenttype-fdo.c:559 | `/* mime type and content type are same on unixes */` |
| the alias step | S526 | gcontenttype-fdo.c:560 | `umime = g_strdup (xdg_mime_unalias_mime_type (mime_type));` |
| the guess signature | S518 | gcontenttype-fdo.c:567 | `g_content_type_guess_impl (const gchar *filename,` |
| trailing slash | S518 | gcontenttype-fdo.c:597 | `if (i > 0 && filename[i - 1] == '/')` |
| one name type | S518 | gcontenttype-fdo.c:614 | `if (n_name_mimetypes == 1)` |
| no name type | S518 | gcontenttype-fdo.c:641 | `if (n_name_mimetypes == 0)` |
| several name types | S518 | gcontenttype-fdo.c:680 | `mimetype = g_strdup (name_mimetypes[0]);` |
| the priority-80 threshold | S521 | gcontenttype-fdo.c:654 | `if (sniffed_prio >= 80) /* High priority sniffing match, use that */` |
| the subclass tie-break | S521 | gcontenttype-fdo.c:663 | `if ( xdg_mime_mime_type_subclass (name_mimetypes[i], sniffed_mimetype))` |
| the desktop rewrite | S521 | gcontenttype-fdo.c:637 | `strcmp (sniffed_mimetype, "application/x-desktop") == 0)` |
| the `info` command form | S527 | gio.1:48 | `\fBgio\fP info [\fIOPTION\fP...] \fILOCATION\fP...` |
| `-a` selects attributes | S527 | gio.1:195 | `\fB\-a\fP, \fB\-\-attributes=<ATTRIBUTES>\fP` |
| what `-a` means | S527 | gio.1:198 | `The attributes to get.` |
| the default attribute set | S527 | gio.1:205 | `By default, all attributes are listed.` |
| `-n` spelling | S527 | gio.1:209 | `\fB\-n\fP, \fB\-\-nofollow\-symlinks\fP` |
| `-n` meaning | S527 | gio.1:212 | `follow symbolic links.` (the line reads `Don't ` + that, with a non-ASCII apostrophe) |
| the exit-status sentence | S527 | gio.1:775 | `On success, \fB0\fP is returned, a non\-zero failure code otherwise.` |

## 9. Frozen cases and pins (the set this entry is answered by)

The frozen case file is JSON `{"version":1,"oracle":"gio info -a standard::content-type (and
standard::fast-content-type)","gio_sha256":...,"glib2":"2.90.1-1","classes":[...],"cases":[...]}`
(contract 2 of the round). Each case holds a `{root}/h` HOME, `XDG_DATA_HOME` = `{root}/dh` or
null, a non-null `XDG_DATA_DIRS`, its `mime` tree (or none, for a `none` database), 1..12 paths
with one oracle label each, a `mode` (`follow`/`nofollow`, and the directory mode for entries
ending `/`) and an `attr` (`full`/`fast`). The 15 classes, in the declaration's order, are
`dir chr blk fifo sock zero empty sym brok nofollow follow certain uncertain fast readerr`, with
>= 8 cases each.

Rule -> case class map (from section 2): the eight stat branches -> `dir`, `chr`, `blk`, `fifo`, `sock`,
`zero`; the filename-vs-content pairs -> `empty` (empty and non-empty regular files) and
`certain`/`uncertain` (one name type vs zero or several); the symlink states -> `sym`;
broken/nofollow -> `brok`, `nofollow`; following -> `follow`; the fast attribute -> `fast`; the
tolerated `EACCES` and the refused other errnos -> `readerr` (the class that must carry both
shapes, per section 2.5).

| artifact | path | state |
|---|---|---|
| candidate | `tools/mado-filetype.py` | frozen at the C1 commit; the L1 pins its sha256 |
| siblings | `tools/mado-mimeglob.py`, `tools/mado-mimesniff.py`, `tools/mado-mimetext.py` | held; pinned by the C1 command |
| oracle | `/usr/bin/gio` | sha256 d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462 (measured here) |
| frozen cases | `.ufo/waves/round-97/controls/filetype-cases-r97-frozen.json` | the L1's freeze block pins it |
| frozen mutants | `.ufo/waves/round-97/controls/filetype-mutants-r97-frozen.json` | same |
| fresh generator | `.ufo/waves/round-97/controls/filetype-fresh-r97.py` | same |
| host list and db | `.ufo/waves/round-97/controls/filetype-host-r97.txt`, `host-db-r97.json` | same |
| forgery | `.ufo/waves/round-97/controls/forgery-ctypes-r97.py` | same |
| counter | `quality/counters/c1-r97-filetype.py` | the L1's counted run is the C1 receipt |

The measured cells (case count, per-class census, fresh total, host total, mutant kills, control
values, selftest check count) are the L1's C1 receipt
`.ufo/waves/round-97/receipts/c1-measured-r97.txt`; this draft states no number it did not
measure (round-96 D2).

## 10. Errata (append-only)

None yet. The two sentences of the round's shared contract that this entry contradicts by
measurement - "a symlink loop is a stat error" and "a path that cannot be stat'ed prints
`ERROR stat`" - are routed in the seat report; the L1 decides whether the frozen sentence or
the model moves (the model here is section 2.5's).

## 11. Verify

Pasteable, read-only, no application launched. `<root>` is any scratch root holding
`{h,dh/mime,d1/mime,d2/mime}`.

The oracle (the installed `gio`, sha256 d2164260...cfc462, glib2 2.90.1-1):

```sh
# one path, the full attribute
env -i LC_ALL=C HOME=/nonexistent /usr/bin/gio info -a standard::content-type /etc/passwd
# the fast attribute, without following a symlink
env -i LC_ALL=C HOME=/nonexistent /usr/bin/gio info -a standard::fast-content-type -n /etc/passwd
# a private text database: HOME and XDG_DATA_HOME empty, XDG_DATA_DIRS at the tree
env -i LC_ALL=C HOME=<root>/h XDG_DATA_HOME=<root>/dh XDG_DATA_DIRS=<root>/d1:<root>/d2 \
  /usr/bin/gio info -a standard::content-type <path>
# a refusal: no attribute line, exit 2
env -i LC_ALL=C HOME=/nonexistent /usr/bin/gio info -a standard::content-type /no/such/path; echo rc=$?
```

The tool:

```sh
python3 -I tools/mado-filetype.py /etc/passwd
python3 -I tools/mado-filetype.py --fast --nofollow /etc/passwd
python3 -I tools/mado-filetype.py --data-home <root>/dh --data-dirs <root>/d1:<root>/d2 --home <root>/h <path>
python3 -I tools/mado-filetype.py --selftest
```

Join: the tool's `<type>` for a path must equal the oracle's attribute line for the same `attr` and
`mode`, and the tool's `attr=` cell names which of the two invocations above it reproduces. A
`MADO_FILETYPE: ERROR stat` line must correspond to an oracle run that prints no attribute line and
exits 2.

Two rules that read wrong from the CLI, each reproducible in one command (both measured in section 7):

```sh
S=$(mktemp -d); mkdir -p "$S/h"; ln -s "$S/b" "$S/a"; ln -s "$S/a" "$S/b"
env -i LC_ALL=C HOME="$S/h" /usr/bin/gio info -a standard::content-type "$S/a"   # inode/symlink, rc 0
```

```sh
S=$(mktemp -d); mkdir -p "$S/h" "$S/d"; printf 'hi\n' > "$S/d/f.bin"; chmod 000 "$S/d"
env -i LC_ALL=C HOME="$S/h" /usr/bin/gio info -a standard::content-type "$S/d/f.bin"  # application/octet-stream, rc 0
```

The 16384 boundary of section 2.4 uses section 7.2's recipe: build a private `mime/magic` whose only
rule is `><n>=<00 02>AB` and a file with `AB` at offset `<n>`, then compare `n = 16380` (matches),
`n = 16382` (matches) and `n = 16385` (does not).
