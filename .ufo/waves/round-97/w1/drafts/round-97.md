# mado round 97 - lessons

Round 97, hyaku run 15, attempt 1 (`MadoR97`). Two frozen claims from
`.ufo/waves/round-97/claims-declaration-r97.md`: C1 coverage (new surface:
`tools/mado-filetype.py`, the content type GIO 2.90.1 reports for a **path**) and C2 operability (a
`--selftest` mode for the two round-96 counters, the `SKILL.md` registry rows for the four round-96
artifacts, and the ledger row). This file is the scribe's DRAFT for the L1 to land after the freeze.
It contains no measured cell it did not measure: the C1/C2 receipt cells are named where they belong
and left to the L1 (round-96 D2).

## Mistakes

**M97-1 - an admitted model sentence was contradicted by the round's own frozen fixture, and nothing
in the round caught it.**
Class: self-contradiction inside one round's artifacts - a rule stated from memory while the same
round froze a fixture that reads the field the other way. It is M96-1's family (a value asserted
beside its own re-derivation) with a rule rather than a digest as the payload.
Evidence: at `0caf2465^`, `corpus/knowledge/mime-textdb-magic-r96.md` line 654 says the cache version
sits `at bytes 4..7`, while `quality/counters/c1-r96-magictext.py:227-228` reads
`int.from_bytes(data[0:2], "big") == 1 and int.from_bytes(data[2:4], "big") in (1, 2)` and the
round's refusal fixtures carry `0001 0001` / `0001 0002` at offset 0. The entry and the counter
disagreed, both were admitted, and no check compared them.
Captured-by: none of the round's own instruments - the counter knew the right offset and the entry
was never re-derived from it; the spot-check's D12 (`corpus/lessons/round-96-verifier-spotcheck.md`
item 12) raised it after the report.
Fix: the erratum landed append-only (`0caf2465`: the superseded sentence stays in the entry, section
10 names both readings and the re-derivation), and the criterion is added - a model sentence whose
subject is a field of the round's own frozen fixture is re-derived from that fixture before admission,
and a superseded sentence is named by an erratum rather than rewritten. The next free `QUALITY.md`
number at base is 168 (167 is the last: `grep -c '^\*\*16[0-9]\.' corpus/QUALITY.md` = 8); the L1
owns the registration.
Shown able to fail: at `0caf2465^` the pair
`git show 0caf2465^:corpus/knowledge/mime-textdb-magic-r96.md | grep -c '^## 10. Erratum'` -> `0` and
`grep -c 'int.from_bytes(data\[0:2\], "big")' quality/counters/c1-r96-magictext.py` -> `1` shows a
disagreement with nothing naming it; at base the same pair reads `1` and `1`. The criterion's check is
therefore "for every sentence that names a fixture field, the entry either matches the fixture reader
or carries an erratum naming both readings", which fails on the pre-fix bytes and passes after.

**M97-2 - the shared contract stated the refusal condition for a failed stat without the library's
errno guard, and two reachable path shapes were misclassified.**
Class: refusal sentinel on a coarser proxy (`QUALITY.md` 166's class, applied to an input state
instead of a database mode). The contract said "a path that cannot be stat'ed at all (missing, or a
symlink loop) ... prints `MADO_FILETYPE: ERROR stat` ... exits 2". The library tests something
narrower, and a symlink loop is not even a stat failure at this surface.
Evidence (all this round, read-only, `/usr/bin/gio` sha256 `d2164260...cfc462`, glib2 2.90.1-1):
- `glocalfileinfo.c:1937-1951`: a failed `lstat` bails out only `if (errsv != EACCES)`; `EACCES` is
  tolerated with the comment `/* Don't bail out if we get Permission denied (SELinux?) */`, and
  `stat_ok = res != -1` (`:1956`) then hands `NULL` to `get_content_type` (`:2065`, `:2080`).
  Measured: a file under a mode-000 parent answers `application/octet-stream` with exit 0, while
  `stat` and `head` on the same path fail with `EACCES` (probe H-eacces).
- `glocalfileinfo.c:1987-1994`: a symlink whose follow `stat` fails sets `symlink_broken = TRUE`, and
  branch 1 answers `inode/symlink`. Measured: `a -> b -> a` answers `inode/symlink`, exit 0, while
  `stat -L` on the same path fails (probe H-loop).
- Only `ENOENT` and `ENOTDIR` refuse: no attribute line, `Error when getting information for file
  "...": No such file or directory`, exit 2 (probes H-missing, H-enotdir). The manual documents only
  `On success, 0 is returned, a non-zero failure code otherwise.` (`gio.1:775`), so the `2` is a CLI
  mapping the contract copied from one measurement and then over-generalised.
Captured-by: none of the declaration's own checks. The contract sentence and the model sentence were
written from the same reading, so they agreed with each other; this wave's independent oracle probes
found the two shapes.
Fix (routed to the L1 before the freeze): the frozen sentence names the library's condition - a
`lstat` that fails with an errno other than `EACCES` is refused; `EACCES` is answered from the name;
a symlink loop is answered `inode/symlink`. The `readerr` class carries the `EACCES` shape and one
refusal, and the loop case sits in `sym`/`brok`, not in `readerr`.
Shown able to fail: with `S=$(mktemp -d); mkdir -p "$S/h"; ln -s "$S/b" "$S/a"; ln -s "$S/a" "$S/b"`,
`env -i LC_ALL=C HOME="$S/h" /usr/bin/gio info -a standard::content-type "$S/a"` prints
`inode/symlink` and exits 0 (measured here); with `mkdir -p "$S/d"; printf 'hi\n' > "$S/d/f.bin";
chmod 000 "$S/d"` the same command on `"$S/d/f.bin"` prints `application/octet-stream` and exits 0
(measured here). Both contradict the contract's predicted `ERROR stat` / exit 2, so a case labelled
from the contract would score an honest tool wrong - the failure `QUALITY.md` 166 names.

## Gate

### Registry rows (opened 2026-11-07; the L1's fetch receipt is
`.ufo/waves/round-97/receipts/sources-open-r97.txt`)

| id | locator | access | located quote | line |
|---|---|---|---|---|
| S526 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gcontenttype-fdo.c (8a5b4f47...a2d7c, 32741 B), HTTP 200; new scope on the file S518/S521/S505 hold | 2026-11-07 | `size = xdg_mime_get_max_buffer_extents ();` | gcontenttype-fdo.c 61 |
| S527 | `gio(1)` GLib 2.90.1, file:///usr/share/man/man1/gio.1.gz (installed page, no HTTP status for a `file://` locator; container 810077be...a565, 4961 B; plain 84b3cdad...8bc5, 18793 B, 781 lines; owner `pacman -Qo` = glib2 2.90.1-1) | 2026-11-07 | `\fB\-a\fP, \fB\-\-attributes=<ATTRIBUTES>\fP` | gio.1 195 |

S526 duplicates S518/S521/S505's URL, so the census's W04 warning is expected and the scope cell is
what differs. Every quote in the entry's section 8 is a whitespace-collapsed line of the fetched
bytes and is <= 25 words; the full map is
`.ufo/waves/round-97/w1/drafts/gio-content-type-file-r97.md` section 8 (49 rows).

### Rows touched

S522, S518, S521, S515, S516, S519, S520, S524, S525, S505: `used-by` only, each appended with
`corpus/knowledge/gio-content-type-file-r97.md` (old -> new in
`.ufo/waves/round-97/w1/drafts/sources-rows-r97.md` section 2). No anchor, digest or scope cell of a
held row moves.

### Candidates considered (round 97) - every gate decision of this draft

| candidate | decision | reason | flip |
|---|---|---|---|
| `corpus/knowledge/gio-content-type-file-r97.md` | **admit** | every rule cites a located line of S522/S526/S527/S518/S521 or an oracle-labelled probe row of its section 7; the only unmeasured cells are the L1's C1 receipt, named, not filled | a GLib tag that changes the branch order or the gate |
| S526, S527 | **admit** | S526 is HTTP 200 at the recorded URL; S527 is an installed man page (a `file://` locator has no HTTP status - `curl -w '%{http_code}'` prints 000), so it is shaped like S509/S510 and bound to glib2 2.90.1-1; digests re-measured here; quotes located and <= 25 words | a newer GLib pin |
| `gio/gcontenttype.c` (fetched this round, HTTP 200, 10399 B, sha256 fb9c68782af7c266f22551ef11e328f9d2491c262efd3de7336dbbfc36554664) | **reject as a separate row** (fold the locator into S526) | the file holds the public wrapper only (`:291-295` calls `_impl`); the behaviour is S526's scope, and a third row for the same pair widens the declaration's two-row frontier | a later round that needs the wrapper's own scope (e.g. the Win32 content-type split) |
| `gio.1`'s EXIT STATUS as a rule | **reject as a model fact** (admit the observation) | the manual promises `0`/non-zero only (`:775`); the measured refusal exit `2` is the CLI's `G_IO_ERROR` mapping, not a documented per-error code, so the entry states it as a surface convention | a `gio` release that documents per-error codes |
| the contract's "a symlink loop is a stat error" | **reject as a model fact** | measured `inode/symlink`, exit 0 (M97-2); the loop is `ELOOP` on the follow `stat` (`:1987-1994`), not on the `lstat` | a GLib change that treats `ELOOP` as broken at the `lstat` |
| the contract's "any path that cannot be stat'ed prints `ERROR stat`" | **reject as a model fact** | `EACCES` is tolerated (`:1941-1942`) and answered from the name (probe H-eacces) | a GLib change to the `EACCES` exception |
| `g_content_type_from_mime_type` as "the identity on Unix" | **reject as a model fact** (admit the alias step) | the Unix impl unaliases (`gcontenttype-fdo.c:560`); a private `mime/aliases` rewrites `inode/symlink` (probe D-alias_map) | an aliases-free code path |
| the L1 receipt's `-> 200` status cell for the `file://` row | `curl -sS -w '%{http_code}'` on `file:///usr/share/man/man1/gio.1.gz` prints `000`: a `file://` locator has no HTTP status, so an "HTTP 200" cell claims a transport event that cannot happen | shape S527 like the other installed man pages (S509/S510): `file://` path, container and decompressed digests, owner bound by `pacman -Qo` |
| the manual as documentation of the content-type attributes | `grep -c content-type` over the decompressed page = 0; the page's only attribute example is `standard::icon` (lines 200, 244, 661), and its `.TH` line is `.TH "gio" "" "" ""` (no version, no date) | state S527's scope as the `info` command, `-a`, `-n` and the exit-status sentence; the attribute names come from `glocalfileinfo.c`'s attribute ids and the measured output, and the version binding is the owning package |
| the receipt's `decompressed=13688` cell for `gio.1.gz` | **reject** (corrected in place in this round's text) | the decompressed bytes measure 18793 (`gzip -dc gio.1.gz | wc -c`), 781 lines, digest `84b3cdad...8bc5` (which the receipt has right); the entry carries 18793 | a re-fetch that reproduces 13688 |
| the declaration's line ranges `:1309-1312`, `:1313`, `:1316`, `:1317`, `:1319-1325`, `:1327`, `:1352-1355`, `:1357-1364`, `:1368-1374` | **reject** (corrected in place) | re-derived from the fetched bytes: symlink `1308-1310`, directory `1311`, chardev `1314-1315`, block `1316-1317`, FIFO `1318-1319`, zerosize `1320-1326`, socket `1328-1330`, clamp `1353-1355`, open `1358-1362`, read/re-guess `1368-1373`; the entry uses the re-derived ranges | a different `glocalfileinfo.c` at the pin |

### Wave findings routed to the L1 before the freeze

These are this draft's findings against the declaration's C1 model and the round's shared contracts;
each carries the measurement that produced it (this seat's probes, or a located line).

| finding | what the bytes say | fix the L1 should land before freezing |
|---|---|---|
| C1 rule 7 / contract 1: "a path that cannot be stat'ed at all (missing, or a symlink loop) ... `MADO_FILETYPE: ERROR stat` ... exits 2" | `EACCES` is tolerated and answered from the name (`glocalfileinfo.c:1941-1942`, probe H-eacces); a symlink loop answers `inode/symlink` (`:1987-1994`, probe H-loop); only other errnos refuse (probes H-missing, H-enotdir) | state the errno guard; move the loop case to `sym`/`brok`; keep one refusal shape in `readerr` |
| C1 rule 1: "`g_content_type_from_mime_type`, which is the identity on Unix" | the Unix impl is `gcontenttype-fdo.c:551-565` and it unaliases at `:560` (probe D-alias_map answers `application/x-aliased` for a `-n` symlink) | say "identity after alias resolution", and either freeze an alias edge or require an aliases-free case tree |
| C1 rule 4: "clamped to 16384 when 0 or larger" | true, and observable at the boundary: extent 16383 matches, 16385 clamps and matches by exact fit, 16388 clamps and misses (probes D-b16380/82/85) | freeze the three-boundary triple in the `certain`/`uncertain` or a `fast`-adjacent class; the clamp needs no other case |
| C1 rule 4: "the file is opened `O_RDONLY|O_NOATIME|O_CLOEXEC` with an EPERM retry" | the tool cannot observe which open the kernel granted; the retry is modelled | keep the declared limit, and do not score atime |
| C1 predicate class list (15) | the list matches the entry's classes, but `readerr` must carry both shapes (tolerated `EACCES`, refused `ENOENT`) or the class tests only one side | name both shapes in the freeze block so a case author cannot label `EACCES` as `ERROR` |
| C2 (iv): "the registry count moves `0 -> 4` rows for the four named artifacts" | at base `e6152b58`, `SKILL.md` already holds **1** row: `| mado-mimetext | probe | ...` (line 887, added by `5dd921b3`); the two counters and the kill-set have 0 | restate the move as `1 -> 4` (or `0 -> 3` over the three missing), and have the C2 counter count the rows it re-derives rather than assert `0` |
| C2: the kill-set row | `quality/selftest-kills/check-receipt-presence.json` holds 7 kills and `selftest_checks` 6; the strength gate's own `--selftest` prints `SELFTEST_STRENGTH_SELFTEST: checks=11 failed=0` | use 7/6/11 in the row text and add the pair to `mado-selftest-strength`'s (TOOL, KILLSET) list |
| receipt `sources-open-r97.txt`: `gio.1.gz` `decompressed=13688` | the decompressed size is 18793 (`gzip -dc | wc -c`), 781 lines, digest as recorded | correct the cell; the digest cell is right and no source claim depends on the byte count |

## Census

- Start: 460 rows at base `e6152b58` (the round-96 landing's count; the L1's
  `.ufo/waves/round-96/receipts/census-end-r96.txt` records 460).
- After S526 and S527: 462 by arithmetic (+2, tier A). Not validated by this seat - the L1's
  `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` run is the census, and this
  draft does not cite a validator output it did not see (round-96 D11).
- Row count is a navigation fact, not a behavioural verdict.

## Cross-domain evidence

GLib's GIO local-file layer (`glocalfileinfo.c`) and its xdgmime port of the freedesktop
shared-mime-info database (`gcontenttype-fdo.c`, `xdgmime/*.c`); the `gio(1)` CLI as the installed
surface (`/usr/bin/gio`, glib2 2.90.1-1); shared-mime-info 2.5.1-2 for the host's `mime/` bytes and
its max extent. `file(1)`/libmagic is revenger's ground and is **not** this surface: GIO's
`standard::content-type` answers from the shared-mime-info database and the stat, never from
`magic(5)`. Desktop-facing consequence: a file manager's "type" column is the attribute of this entry,
so a name/type mismatch there is expected behaviour, not a bug in the database.
