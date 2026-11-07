# SOURCES rows for round 97 (draft - the L1 lands them; the scout owns the fetch receipt)

Registry: `corpus/SOURCES.md`, 11-column shape (13 pipe-separated cells counting the two empty edge
cells, E01: `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck |
used-by |`). The two rows below are the round's new rows; the
declaration's C1 frontier names them. Digests are re-measured from the L1's fetched bytes
(`.ufo/waves/round-97/fetch/`, receipt `.ufo/waves/round-97/receipts/sources-open-r97.txt`); every
quote is <= 25 words and located. ASCII only.

## 1. New rows

```
| S526 | GLib 2.90.1 GIO content-type sniff length and the Unix mime-type mapping - https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gcontenttype-fdo.c (sha256 8a5b4f475947a9de2e0ca34e60b0dc31f5c56a2d7e0a9fe8cf84002aca8a2d7c, 32741 B, HTTP 200 at the recorded URL; the same file S518/S521/S505 hold, new scope); host package glib2 2.90.1-1 | code | A | how GIO turns a mime type into the content type it reports on Unix and how much of a file it asks the database to sniff: `_g_unix_content_type_get_sniff_len` and the `xdg_mime_get_max_buffer_extents` call it wraps under the gio-xdgmime lock, and `g_content_type_from_mime_type_impl`'s unalias step | gcontenttype-fdo.c:54-66 (`gsize _g_unix_content_type_get_sniff_len (void)`; :61 `size = xdg_mime_get_max_buffer_extents ();`), :551-565 (the Unix impl; :559 the comment, :560 `umime = g_strdup (xdg_mime_unalias_mime_type (mime_type));`) | the sniff length is the reachable database's max buffer extent (0 or > 16384 becomes 16384 at the caller), and every stat-branch answer - `inode/symlink`, `inode/directory`, `inode/chardevice`, `inode/blockdevice`, `inode/fifo`, `inode/socket`, `application/x-zerosize` - passes through the alias table before it is reported, so a hand-written `mime/aliases` rewrites them | mined | 2026-11-07 | 180d | corpus/knowledge/gio-content-type-file-r97.md |
```

```
| S527 | `gio(1)` manual, GLib 2.90.1 - file:///usr/share/man/man1/gio.1.gz (installed page: no HTTP status exists for a `file://` locator, `curl -w '%{http_code}'` reports 000; container sha256 810077be12cf2df5006db1e1b9b967f6c505930033c68aa9cfc964281906a565, 4961 B; decompressed sha256 84b3cdad868feecd69f113b789d7009113e16531b67d750cd0e424ba2bcb8bc5, 18793 B, 781 lines); owner `pacman -Qo` = glib2 2.90.1-1 | docs | A | the installed `gio` CLI's `info` command surface: the command and its LOCATION form, `-a`/`--attributes` and what omitting it does, `-n`/`--nofollow-symlinks`, and the exit-status sentence (the page names no content-type attribute - `grep -c content-type` = 0 - and its `.TH` line carries no version and no date, so the version binding is the owning package) | gio.1 lines 48 (the synopsis form), 172-177 (the command), 195-205 (`-a`; the default attribute set), 209-212 (`-n`), 773-775 (EXIT STATUS); `.TH "gio" "" "" ""` at line 31 | which options select and name attributes, that `-a` takes comma-separated GIO attribute names and that omitting it lists every attribute, that `-n` suppresses the follow, and that the manual promises only 0 vs non-zero - the per-error exit codes are the CLI's own mapping, and the content-type attribute names themselves are not in this page | mined | 2026-11-07 | 180d | corpus/knowledge/gio-content-type-file-r97.md |
```

## 2. Used-by appends on held rows (old -> new, exact cell text)

| id | old `used-by` | new `used-by` |
|---|---|---|
| S505 | `corpus/knowledge/mime-default-resolution-r91.md,corpus/lessons/round-91.md,corpus/knowledge/mime-glob-guess-r94.md,corpus/knowledge/mime-magic-sniff-r95.md,corpus/lessons/round-95.md,corpus/knowledge/mime-textdb-magic-r96.md` | the same plus `,corpus/knowledge/gio-content-type-file-r97.md` |
| S515 | `corpus/knowledge/mime-glob-guess-r94.md,corpus/lessons/round-94.md` | the same plus `,corpus/knowledge/gio-content-type-file-r97.md` |
| S516 | `corpus/knowledge/mime-glob-guess-r94.md,corpus/lessons/round-94.md` | the same plus `,corpus/knowledge/gio-content-type-file-r97.md` |
| S518 | `corpus/knowledge/mime-glob-guess-r94.md,corpus/lessons/round-94.md` | the same plus `,corpus/knowledge/gio-content-type-file-r97.md` |
| S519 | `corpus/knowledge/mime-magic-sniff-r95.md,corpus/lessons/round-95.md,corpus/knowledge/mime-textdb-magic-r96.md` | the same plus `,corpus/knowledge/gio-content-type-file-r97.md` |
| S520 | `corpus/knowledge/mime-magic-sniff-r95.md,corpus/lessons/round-95.md,corpus/knowledge/mime-textdb-magic-r96.md` | the same plus `,corpus/knowledge/gio-content-type-file-r97.md` |
| S521 | `corpus/knowledge/mime-magic-sniff-r95.md,corpus/lessons/round-95.md,corpus/knowledge/mime-textdb-magic-r96.md` | the same plus `,corpus/knowledge/gio-content-type-file-r97.md` |
| S522 | `corpus/knowledge/mime-magic-sniff-r95.md,corpus/lessons/round-95.md,corpus/knowledge/mime-textdb-magic-r96.md` | the same plus `,corpus/knowledge/gio-content-type-file-r97.md` |
| S524 | `corpus/knowledge/mime-textdb-magic-r96.md, corpus/lessons/round-96.md` | the same plus `, corpus/knowledge/gio-content-type-file-r97.md` |
| S525 | `corpus/knowledge/mime-textdb-magic-r96.md, corpus/lessons/round-96.md` | the same plus `, corpus/knowledge/gio-content-type-file-r97.md` |

Each append keeps the row's own separator style (S524/S525 carry a space after the comma; the others
do not), and no appends or trailing text sits outside the closing pipe (round-96 D1). No anchor,
digest, scope or status cell of a held row moves.

## 3. Census and fetch notes

- Expected row count after the two rows: 460 -> 462 (tier A +2). This is arithmetic, not a validator
  run; the L1's `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` output is the
  census, and no receipt cell here cites a count this seat did not derive.
- **Landing order (census E11).** A `mined` row's `used-by` path must exist on disk
  (`scripts/sources-census.sh:566`), and `corpus/knowledge/gio-content-type-file-r97.md` does not
  exist at base, so the entry must land before or with the registry commit that marks S526/S527
  `mined` - otherwise the census fails on the rows this round adds (R97MScoutSources' D9 says the
  same).
- S526 repeats the URL of S518/S521/S505, so the census's W04 duplicate-URL warning is expected;
  the differing cell is `scope`.
- S527 carries both digests for the installed page (container `810077be...`, decompressed
  `84b3cdad...`) so a later `glib2` bump shows which half moved.
- The L1 receipt's `decompressed=13688` cell for `gio.1.gz` does not match the bytes: `gzip -dc
  gio.1.gz | wc -c` prints 18793 (781 lines, digest 84b3cdad...). The row text above carries 18793;
  the receipt cell should be corrected so the two artifacts agree.
- Fetch policy: S526 is HTTP 200 at the recorded URL (QUALITY 164; no 301 stub, no unregistered URL
  cited). S527 is an installed page, not a URL: a `file://` locator has no HTTP status (`curl -w
  '%{http_code}'` prints 000), so the row is shaped like S509/S510 - `file://` path, container and
  decompressed digests, and the owning package. No HTTP-200 claim is made for it.
- S527 scope limits: the page contains zero occurrences of `content-type`, and its `.TH` line is
  `.TH "gio" "" "" ""` (no version, no date), so the row claims the `info` command, `-a`, `-n` and
  the exit-status sentence only, bound to glib2 2.90.1-1 through `pacman -Qo`.
- S526 scope limit: `gcontenttype-fdo.c` is already the URL of S505/S518/S521, so the scope names
  only the uncovered lines (the sniff-length function at 54-66 and the Unix `from_mime_type`
  implementation at 551-565) and never the guess implementation, which S518 anchors at 567-690.
- **S522's own anchor cell drifts by one line (proposed correction; the L1's call).** The cell
  reads `glocalfileinfo.c:1337 (name-only guess), 1340 (sniff condition), 1345 (16 KiB buffer),
  1351-1353 (sniff length), 1368-1374 (read and guess with data)`. Measured on the same bytes:
  `1337` and `1340` are exact, the buffer is at `1346`, the sniff-length call is `1353` with the
  clamp at `1354-1355`, and the read/re-guess pair is `1368-1373` (`1374` is a closing brace).
  Proposed new cell: `glocalfileinfo.c:1337 (name-only guess), 1340 (sniff condition), 1346
  (16 KiB buffer), 1353-1355 (sniff length and the clamp), 1368-1373 (read and re-guess with
  data)`. Changing a held row's anchor needs the round's old -> new log; this draft only proposes it
  (R97MScoutSources' D4 reaches the same two numbers independently).
- `gio/gcontenttype.c` (HTTP 200, 10399 B, sha256
  fb9c68782af7c266f22551ef11e328f9d2491c262efd3de7336dbbfc36554664) was fetched by this seat only
  to check that the public wrapper at `:291-295` calls the Unix impl; it is **not** proposed as a row
  (S526's scope carries the locator) and its bytes were not committed.
