# R97MScoutSources - independent re-open of the round-97 C1 sources

Seat `R97MScoutSources`, round 97 (hyaku run 15, attempt 1), 2026-11-07.
Scope: re-open every source the L1 opened this round, re-locate the lines the
C1 model rests on, and draft the two registry rows. Nothing was installed for
this seat (host packages read, not changed): curl 8.23.0, gzip, python3
stdlib, `/usr/bin/gio` 2.90.1 (sha256
`d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`).
Scratch `/fast/scratch/hyaku/mado-r97/R97MScoutSources`, deleted at yield.

Full receipt (fetch records, every located line, all measurements, the two row
drafts): `.ufo/waves/round-97/receipts/sources-verify-r97.txt`.

## Verdict in one paragraph

All three URLs the L1 opened re-fetch cleanly: two HTTPS rows at HTTP 200 with
no redirect and byte-identical bodies across two fetches, digests equal to the
receipt's and to round 95's (no rotation); the man page's container digest and
its plain-text digest both confirmed, and the file is byte-identical to the
host's `/usr/share/man/man1/gio.1.gz`. Two receipt cells do not survive
re-measurement (the `file://` row's status and its decompressed byte count),
and five model sentences in the declaration disagree with the bytes or with
the oracle - most consequentially the claim that the six stat branches answer
the literal `inode/*` strings, and the claim that a symlink loop is a stat
failure. Details and evidence in D1-D10 below.

## D-numbered findings

| id | subject | severity | one line |
|---|---|---|---|
| D1 | receipt row 3 records a status curl cannot produce | receipt defect | `file://` has no HTTP status; curl reports `000`, the receipt says `-> 200` |
| D2 | receipt row 3 decompressed byte count is wrong | receipt defect | receipt says 13688, the bytes are 18793 (781 lines) |
| D3 | HTTPS rows 1-2 | none | confirmed, two 200 fetches each, digests stable across rounds |
| D4 | declaration + S522 line cites are off by 1-3 lines | model cite drift | socket is at 1329-1330, not 1327; the sniff-len function is 54-66, not 55-67 |
| D5 | "g_content_type_from_mime_type ... is the identity on Unix" | **model defect** | the stat branches answer the ALIASED type; measured `inode/directory` -> `application/x-customalias` |
| D6 | "a symlink loop" is put in the ERROR class | **model defect** | gio answers `inode/symlink` with exit status 0 for a 2-cycle, twice measured |
| D7 | clamp "when 0 or larger" | model wording | the C clamps only `== 0` or `> 16384`; a smaller extent is used as it stands |
| D8 | S527 scope | scope limit | the manual names NO content-type attribute and carries no version |
| D9 | landing order | process | a mined row citing `corpus/knowledge/gio-content-type-file-r97.md` raises census E11 until that file exists |
| D10 | S526 scope vs S518/S521 | registry hygiene | the URL is shared; the scope cell must name only the uncovered lines, and W04 is expected |

### D1 - the `file://` row's status cell cannot be reproduced

Receipt bytes:
`2026-11-07T16:40:02Z file:///usr/share/man/man1/gio.1.gz -> 200 file:///usr/share/man/man1/gio.1.gz bytes=4961 (gz) decompressed=13688 (781 lines) sha256_gz=810077be... sha256_plain=84b3cdad...`

Re-measured twice with the mandated recorder (`curl -sS -o <file> -w '%{http_code} %{url_effective}'`):
`000 file:///usr/share/man/man1/gio.1.gz` on both fetches. A `file://` locator
carries no HTTP status; curl reports `000` (also with `-L`, and with `--head`).
QUALITY 164's gate is "an HTTP 200 at the recorded URL", so this row cannot be
presented as an HTTP 200 open. The row belongs in the shape of the other
installed man pages (S509 `bash(1)`, S510 `grep(1)`): a host-file locator with
a container digest and a decompressed digest, bound to the owning package
(`pacman -Qo /usr/share/man/man1/gio.1.gz` -> `glib2 2.90.1-1`).

### D2 - the decompressed byte count is wrong

The receipt says `decompressed=13688 (781 lines)`. The committed fetch copy
decompresses to **18793** bytes and 781 lines, and the plain digest
`84b3cdad868feecd69f113b789d7009113e16531b67d750cd0e424ba2bcb8bc5` matches
the receipt's. The digest and the line count are right; only the byte count is
wrong. No rendering of the page reproduces 13688 (`MANWIDTH` 60/80/100/120/132
give 15280/14514/14277/14210/14136 bytes; dropping roff control lines gives
13736 bytes / 13594 characters; `gzip -l` says 18793).

### D4 - line cites are off by 1-3 lines (and the same drift sits in S522)

Measured in the fetched `glocalfileinfo.c` (sha256 `b006a93d...`, identical
to the round-95 copy):

| the model cites | the bytes hold |
|---|---|
| symlink `:1309-1312` | condition 1308-1309, return 1310 |
| directory `:1313` | condition 1311, return 1312 (1313 is the `#ifndef`) |
| character device `:1316` | condition 1314, return 1315 (1316 is the block-device condition) |
| block device `:1317` | condition 1316, return 1317 - correct |
| FIFO `:1318` | condition 1318, return 1319 |
| zero size `:1319-1325` | condition 1320, return 1325 (1319 is the FIFO return) |
| socket `:1327` | condition 1329, return 1330 (1327 is the `#endif`) |
| sniff length `gcontenttype-fdo.c:55-67` | 54 `gsize`, 55 name, 61 the call, 66 closing brace, 67 blank |

Two of the declaration's cites are exact and worth keeping: the name-only guess
at `glocalfileinfo.c:1337` and the sniff gate at `:1340`. The held row S522
carries the same drift ("1345 (16 KiB buffer), 1351-1353 (sniff length)": the
buffer is declared at 1346, and the sniff length is 1353 with the clamp at
1354-1355).

### D5 - the stat branches answer the ALIASED type, not the literal string

Declaration bytes: "every one of these is returned through
`g_content_type_from_mime_type`, which is the identity on Unix
(`gcontenttype.c:291-296`)".

The bytes: `g_content_type_from_mime_type` (gcontenttype.c:290-296) forwards to
`g_content_type_from_mime_type_impl` (gcontenttype-fdo.c:551), which returns
`xdg_mime_unalias_mime_type (mime_type)` (gcontenttype-fdo.c:560); that
resolves through the database's alias table (xdgmime.c:735-746;
`cache_alias_lookup` in cache mode, the `aliases` file in text mode).
xdgmimealias.c:126-138 stores the LEFT column of an aliases line as the alias
key and the RIGHT column as the type it maps to; :83-98 looks up by alias.

Measured on this host, text mode, custom `XDG_DATA_HOME` with a
`mime/aliases` file:

- `inode/directory application/x-customalias` -> a directory answers
  `standard::content-type: application/x-customalias`
- `application/x-zerosize application/x-weird` -> a 0-byte file answers
  `application/x-weird`
- `application/x-probeB inode/directory` -> a directory answers
  `inode/directory` (unchanged)
- `text/plain application/x-textalias` -> a `.txt` file still answers
  `text/plain` (the guess path is not unaliased)
- control, same tree without the aliases file -> `inode/directory`

On the host's own database the identity reading happens to hold, because
`/usr/share/mime/aliases` never lists the seven stat-branch names as alias
keys. A frozen C1 case whose `mime/` tree carries an `aliases` file would
disagree with a candidate that hard-codes the `inode/*` strings.

### D6 - a symlink loop is not a stat failure

Declaration bytes (rule 7): "a path that cannot be stat'ed at all (missing, or
a symlink loop) is outside the surface: the tool prints `MADO_FILETYPE: ERROR
stat` for that path and exits 2 (the same refusal `gio info` makes)".

Measured twice, with two independent 2-cycles (`z1->z2->z1` and `l1<->l2`):
`gio info -a standard::content-type ./z1` prints
`standard::content-type: inode/symlink` and exits **0**. The source reason:
lstat on the link itself succeeds (glocalfileinfo.c:1932), so `is_symlink` is
TRUE (:1964) and the follow-stat fails with ELOOP, which sets
`symlink_broken` (:1993-1994); the first branch then answers `inode/symlink`
(:1308-1310). Only a genuinely missing path makes gio exit 2 with no attribute
(measured). With the case-file label rule ("ERROR only when gio exits nonzero
and prints no attribute"), a symlink loop belongs to the `inode/symlink` class,
not to the ERROR class - a candidate answering `ERROR stat` for a loop is
scored wrong on such a case.

### D7 - the clamp is `== 0` or `> 16384`

Declaration bytes (rule 4): "clamped to 16384 when 0 or larger". The bytes
(glocalfileinfo.c:1354-1355, `sizeof (sniff_buffer)` is 16384 from :1346):
`if (sniff_length == 0 || sniff_length > sizeof (sniff_buffer))` ->
`sniff_length = sizeof (sniff_buffer);`. A length between 1 and 16384 is used
as it stands and is NOT raised. The seat contract's phrasing ("0 or > 16384 ->
16384") is the correct one. On this host the clamp does fire: the cache's
magic-list MAX_EXTENT, read the way xdgmimecache.c:741-745 reads it, is
**18730**, so the effective sniff length is 16384.

### D8 - the manual grounds the CLI contract, not the attribute names

Measured on the decompressed 781-line page: `content-type` appears 0 times,
`fast-content` 0 times, `standard::` only as `standard::icon` (lines 200, 244,
661), and the `.TH` line is `.TH "gio" "" "" ""` - no version, no date. The
S527 row may therefore claim the `info` command and its `-a/--attributes` and
`-n/--nofollow-symlinks` options and the exit-status sentence; it may not
claim that the manual documents `standard::content-type` or
`standard::fast-content-type`, and the version binding must be the owning
package.

### D9 - the used-by target does not exist yet

`corpus/knowledge/gio-content-type-file-r97.md` is absent at the base
revision, and the census treats a mined row's used-by paths as on-disk
requirements (scripts/sources-census.sh:558-568, `E11 <id> missing used-by
<path>`). S526, S527 and any used-by append naming that path must land
together with the knowledge file.

### D10 - S526 shares a URL with two held rows

`gcontenttype-fdo.c` is the URL of S505 (which lists it among several), S518
and S521, so the census will print the expected W04 duplicate-url warning
(the same pattern as S525 against S523 in round 96). The scope cell must name
only what no held row anchors. Held anchors for that file: S518 -> 567-690
with :597-603, :613-620, :641-648, :675-683; S521 -> 532-548 with :542-544,
622-639, 641-684 with :654; S505 -> 69-111, 116-138. The uncovered lines are
exactly **54-66** (the sniff-length accessor) and **551-566** (the unalias hop
of the stat-branch answer), which is what the drafted scope names.

## Registry-row drafts (11 columns, as the registry uses them)

Next free ids, by the seat's own command
(`grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE
'S[0-9]+' | sort | tail -3` -> `S523 S524 S525`; `grep -c "S526\|S527"
corpus/SOURCES.md` -> 0): **S526** and **S527**. No cell below contains a
literal or escaped `|`. The house convention writes an em dash (U+2014) after
the source title; this report is ASCII-only, so the drafts use a plain hyphen -
the L1 may substitute the em dash for byte-parity with the neighbouring rows.

```
| S526 | GLib 2.90.1 content-type sniff length source - https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gcontenttype-fdo.c (sha256 8a5b4f475947a9de2e0ca34e60b0dc31f5c56a2d7e0a9fe8cf84002aca8a2d7c, 32741 B, HTTP 200 twice at the recorded URL); host package glib2 2.90.1-1 | code | A | where the path-level sniff length comes from, and what the six stat branches answer once the database alias table is applied | gcontenttype-fdo.c:54-66 (_g_unix_content_type_get_sniff_len; :61 size = xdg_mime_get_max_buffer_extents ()), 551-566 (g_content_type_from_mime_type_impl; :560 xdg_mime_unalias_mime_type) | the sniff length is the database's max buffer extent, and a stat branch answers the canonical type of its inode name, not the literal name | mined | 2026-11-07 | 180d | corpus/knowledge/gio-content-type-file-r97.md |

| S527 | gio(1) manual, GLib 2.90.1, installed on this host - file:///usr/share/man/man1/gio.1.gz (container sha256 810077be12cf2df5006db1e1b9b967f6c505930033c68aa9cfc964281906a565, 4961 B; decompressed sha256 84b3cdad868feecd69f113b789d7009113e16531b67d750cd0e424ba2bcb8bc5, 18793 B, 781 lines); host package glib2 2.90.1-1 | docs | A | the installed gio CLI contract the C1 oracle relies on: which locations it reports, how attributes are selected, the nofollow flag and the exit status | gio.1:48 (info synopsis), 172-177 (info command), 195-205 (-a and --attributes), 209-212 (-n and --nofollow-symlinks), 773-775 (EXIT STATUS) | the manual names no content-type attribute: it shows attribute selection by GIO name, and zero on success against a non-zero failure code | mined | 2026-11-07 | 180d | corpus/knowledge/gio-content-type-file-r97.md |
```

S527's locator is a local host file, so the census's URL extraction (which
matches `https?://`) leaves it without a URL: no W04 for it, exactly like the
held man-page rows S493/S495/S497/S498/S503/S509/S510.

## What the oracle does on this host (measurements the C1 model must match)

All by `/usr/bin/gio info -a standard::content-type <path>`, attribute lines
printed as `  standard::content-type: <type>`; the fast column is the same
command with `standard::fast-content-type`.

| path | full | fast |
|---|---|---|
| regular, 0 bytes | application/x-zerosize | application/x-zerosize |
| regular, 0 bytes, `.txt` name | application/x-zerosize | application/x-zerosize |
| regular, text, `.txt` | text/plain | text/plain |
| regular, text, `.png` | image/png | image/png |
| regular, text, no extension | text/plain | application/octet-stream |
| regular, binary, no extension | application/octet-stream | application/octet-stream |
| directory (also named `dir.png`) | inode/directory | inode/directory |
| fifo | inode/fifo | inode/fifo |
| unix socket | inode/socket | inode/socket |
| `/dev/null`, `/dev/zero` | inode/chardevice | inode/chardevice |
| `/dev/sda`, `/dev/sr0` | inode/blockdevice | inode/blockdevice |
| symlink `link.png` -> regular text file | image/png | image/png |
| symlink `link` -> regular text file | text/plain | application/octet-stream |
| symlink -> directory | inode/directory | inode/directory |
| symlink -> fifo | inode/fifo | inode/fifo |
| symlink -> 0-byte file | application/x-zerosize | application/x-zerosize |
| broken symlink | inode/symlink | inode/symlink |
| symlink 2-cycle | inode/symlink (exit 0) | inode/symlink |
| `gio info -n` on a valid symlink | inode/symlink | - |
| missing path | no attribute, exit 2 | - |
| path under a regular file (ENOTDIR) | no attribute, exit 2 | - |
| path under an unreadable directory | attribute present, exit 0 | - |
| file mode 000, `.txt` name | text/plain | text/plain |
| file mode 000, no extension | application/octet-stream | application/octet-stream |
| `/proc/self/status`, `/proc/version` | application/x-zerosize | - |

Three of these matter for the C1 case classes and are worth the C1 seat's
attention:

1. A **symlink's own name** drives the name-only guess (`link.png` ->
   `image/png` although the target is a text file), because the guess runs on
   `g_path_get_basename(local->filename)` (glocalfile.c:1250, 1256) - never on
   the resolved target's name.
2. A **0-byte regular file** answers `application/x-zerosize` whatever its
   name says: the zero-size branch (:1320-1325) precedes the guess, so the
   `certain`/`uncertain` classes do not apply to it.
3. The **`zero` and `empty` class names** cannot both denote a 0-byte regular
   file: every 0-byte regular file answers `application/x-zerosize` from the
   stat branch (:1320-1325) and never reaches the guess. Two readings remain
   open, and the class names are the L1's and the case seat's to fix:
   [INFERENCE] `zero` = the 0-byte regular file (application/x-zerosize) and
   `empty` = a file whose name yields no type at all, whose answer is
   application/octet-stream when the sniff finds nothing binary (measured) or
   when the read fails (mode 000, measured); or `zero` = the `/dev/zero`
   character device, which on this host answers inode/chardevice exactly like
   `/dev/null`. This seat reports the measurements; it does not fix the
   mapping.

## The lines the C1 model rests on (quick index)

`gcontenttype-fdo.c` (fetched, sha256 `8a5b4f47...`): 54-66 sniff-length
accessor (61 the call) | 613-620 one-name-type early return (before the data
block at 622) | 641-648 no-name-type branch (643-645 the uncertain flag, 647
the answer) | 654 the `sniffed_prio >= 80` threshold | 661-671 the subclass
tie-break | 636-638 the desktop rewrite | 551-566 the stat-branch unalias hop.

`glocalfileinfo.c` (held S522's file; the round-97 fetch is byte-identical,
sha256 `b006a93d...`): 1308-1330 the seven stat branches in order | 1337 the
name-only guess | 1340 the sniff gate | 1346 the 16 KiB buffer | 1353-1355 the
length and its clamp | 1357-1362 the open and the EPERM retry | 1364-1375 the
read and the re-guess.

`gio.1` (fetched, sha256 `810077be...`): 48 the `info` synopsis | 172-177 the
`info` command | 195-205 `-a/--attributes` | 209-212 `-n/--nofollow-symlinks` |
773-775 the exit status | no content-type wording anywhere (D8).

## Limits of this seat

- The alias rewrite (D5) was measured in text mode only; the host runs in cache
  mode, where the same lookup is `cache_alias_lookup`
  (xdgmimecache.c:314-361, 1051-1062). The cache-mode rewrite is [INFERENCE]
  from the shared code path, not measured.
- The declaration's predicate sentences were treated as frozen. D4-D7 report
  disagreements against the model's own sentences and against the measured
  oracle; none of them widens a predicate.
- No registry row was edited - `corpus/SOURCES.md` is the L1's to land; the two
  drafts above are proposals for the L1 and the scribe.
