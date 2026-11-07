# R97MExecCasesC1 -- frozen C1 case file report (round 97, w1)

Seat: R97MExecCasesC1 (leaf executor). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base revision `e6152b589c2c6a28426c28263c4bcc3c46398be4`. No tools installed or
upgraded (host pacman pause honoured; only `/usr/bin/gio` and stdlib Python used).

## Files written (owned scope only)

- `.ufo/waves/round-97/controls/filetype-cases-r97.json` (draft, 140 cases;
  sha256 `c5630cd0ccafa850435f9810d9366d2bff316efb6d97cd87c9d97667064ebbd2`;
  supersedes sha256 `c88c06...088f8` -- see the host-db amendment below)
- `.ufo/waves/round-97/controls/filetype-probe-r97.py` (the oracle builder; re-runnable)
- `.ufo/waves/round-97/w1/R97MExecCasesC1.md` (this report)

No other tracked paths written. Nothing committed. No network beyond the host's
own `/usr/bin/gio` invocations. No non-ASCII bytes in committed artifacts (the
JSON is emitted with sorted keys and `(',',':')` separators; `--check` rebuilds
byte-identical).

## Oracle

`/usr/bin/gio` sha256 `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`
(matched the L1's freeze receipt `.ufo/waves/round-97/receipts/sources-open-r97.txt`).
glib2 `2.90.1-1`. Every case built under scratch
`/fast/scratch/hyaku/mado-r97/R97MExecCasesC1/cases/<id>/`, labelled by
`env -i LC_ALL=C HOME=<root>/h [XDG_DATA_HOME=..] [XDG_DATA_DIRS=..] gio info -a
standard::content-type|standard::fast-content-type [-n] <path>`, parsing the
single `standard::*-content-type:` line. Zero `ERROR` labels (no path was
missing/looping in the stat sense; dangling and loop links answer
`inode/symlink` in both modes, as measured).

## Case counts per class (total 140, >= 9 per class, >= 8 required by predicate)

| class | cases | class | cases |
|---|---|---|---|
| dir | 10 | nofollow | 9 |
| chr | 9 | follow | 9 |
| blk | 9 | certain | 10 |
| fifo | 9 | uncertain | 10 |
| sock | 9 | fast | 10 |
| zero | 9 | readerr | 10 |
| empty | 9 |  |  |
| sym | 9 |  |  |
| brok | 9 |  |  |

140 = sum; all 15 classes present in declaration order.

## Label census (types seen, over all 198 path labels)

`inode/directory` 27, `text/plain` 38, `inode/symlink` 25,
`application/x-zerosize` 14, `inode/chardevice` 12, `inode/fifo` 12,
`inode/socket` 12, `inode/blockdevice` 11, `application/octet-stream` 17,
`image/png` 9, `app/x-pngdata` 5, `app/x-pngdata2` 2, `app/x-foo` 4,
`app/x-foo2` 4, `application/x-desktop` 1, `text/html` 3. Zero `ERROR` labels.

## Fixture coverage per class (per seat spec)

- `dir`: plain subdir, dir named `looks.png` (+ file inside), nested dirs,
  nofollow, fast attr, trailing-slash path, host-db dir, empty-db dir, dir
  with a typed file. 10 cases.
- `chr`: `/dev/null`, `/dev/zero`, `/dev/full`, `/dev/tty`, `/dev/pts/ptmx`,
  nofollow, fast, nofollow+fast, host-db. 9 cases.
- `blk`: `/dev/sda`, `/dev/sda1`, `/dev/nvme0n1`, nofollow, fast,
  nofollow+fast, host-db, `/dev/nvme1n1p1`, `/dev/dm-0`. **`/dev/loop0` does
  not exist on this host** (`ls /dev/loop0` fails; loop devices absent from
  `/dev`), so the class uses real block devices instead and is not short --
  it carries 9 full cases. No class was left short.
- `fifo`: plain, nofollow, fast, two pipes, `pipe.png`, host-db, in subdir,
  dot-name, nofollow+fast. 9 cases (`mkfifo`).
- `sock`: plain, nofollow, fast, two sockets, `sock.txt`, host-db, in subdir,
  dot-name, nofollow+fast. 9 cases (AF_UNIX bind held while gio runs).
- `zero`: empty `.png` named, empty unknown name, empty `.desktop` name, empty
  `.txt`, empty `.foo`, nofollow, fast, two empty files, host-db. All
  `application/x-zerosize`. 9 cases.
- `empty`: non-empty plain text with unknown name / `.txt` name / `.foo` name,
  binary, PNG bytes unknown name, nofollow, fast, empty-db, host-db. 9 cases.
- `sym`: symlink to file (both modes), to dir (both modes), fast, two links,
  link named `link.png` to a binary target, host-db, in subdir. 9 cases.
- `brok`: dangling (both modes), loop `l1<->l2` (both modes), fast, dangling
  in subdir, host-db, dangling named `dang.png`, empty-db. 9 cases. No
  `ERROR` labels: follow mode on a dangling/loop link answers `inode/symlink`
  (broken-target branch), matching `glocalfileinfo.c:1309-1312`.
- `nofollow`: mode=nofollow over sym, brok, dirlink, loop, mixed
  file+fifo+sock, empty file, dir, chardev+blkdev, sym+brok+file. 9 cases.
- `follow`: same nine shapes with mode=follow. 9 cases.
- `certain`: text bytes in `a.png`, PNG bytes in `a.txt`, HTML bytes in
  `a.txt`, PNG bytes in `a.foo`, nofollow variant, fast variant, text bytes
  in `a.desktop`, two files, host-db, empty-db. All show the single name type
  winning over contradicting bytes (no sniff). 10 cases.
- `uncertain`: PNG bytes in no-extension `README`, plain text in `blob.bin`,
  HTML in multi-type `page.html`, binary unknown, multi-type `*.foo` with
  text bytes, PNG bytes against a priority-90 sniff (`app/x-pngdata` wins
  over name types), PNG bytes against a priority-90 sniff of another type
  (`app/x-pngdata2` wins), sniffed `application/x-desktop` on a nameless
  file -> `text/plain`, host-db. 10 cases.
- `fast`: attr=fast over uncertain fixtures (PNG README -> name-only
  `application/octet-stream`; text blob.bin; HTML page; binary; multi `*.foo`;
  desktop bytes; certain `a.png`; empty `z.png`; host-db mystery; multi `*.foo`
  against priority-90 sniff -> name-only winner). 10 cases. No sniff happens;
  the labels diverge from the full-attribute labels exactly on the uncertain
  shapes.
- `readerr`: chmod-000 regular file with uncertain name (PNG bytes and text
  bytes; open fails, name-only `application/octet-stream` kept), chmod-000
  certain name (`.txt`, name-only `text/plain`), chmod-000 multi-type
  `*.foo`, unlocked-subdir control (readable PNG bytes answered
  `app/x-pngdata`), nofollow, fast, two unreadable paths, host-db readable
  control. The process runs as `vgpnk` (uid 1000) so chmod-000 genuinely
  blocks reads (verified with `cat`/`open` giving EACCES); the
  `locked/secretdata` path in `readerr-05` covers the under-a-locked-dir
  shape without a second mechanism. 10 cases.

Every case declares a `mime/` tree in `files` (`globs2` and/or `magic`) or
points the env only at empty dirs / the host's `/usr/share` (the `none`/
host-db cases). `mime/magic` files use the correct `MIME-Magic\0\n` header
(measured: a lowercase `MIME-magic` header contributes no match -- one of the
probe's early mistakes, caught by the oracle, not the model). `XDG_DATA_DIRS`
is never null; `HOME` is always `{root}/h` (created, empty).

## Verified model facts (oracle, before freezing)

1. Chardev/block/fifo/socket/dir/zerosize branches fire **before** any name
   or content guess (`/dev/null` -> `inode/chardevice`, `/dev/sda` ->
   `inode/blockdevice`, empty `z.png` -> `application/x-zerosize`).
2. Symlink in nofollow mode -> `inode/symlink`; symlink to a file in follow
   mode answers the *target's* type (`text/plain` for `real.txt`); symlink to
   a dir in follow mode -> `inode/directory`. Dangling and loop links answer
   `inode/symlink` in **both** modes (the broken branch precedes the nofollow
   check).
3. One name type -> that type, certain, bytes ignored
   (`a.png` with plain text -> `image/png`; `image/png` (host db) with plain
   text -> `image/png`). No name type + uncertain + full attr -> the sniff
   decides (`README` with PNG bytes -> `app/x-pngdata` / `image/png` (host)).
4. Several name types + sniffed priority 90 (>= 80) -> the sniffed type wins;
   text bytes (fallback priority 0) -> the first name type wins
   (`multi.foo` with text bytes -> `app/x-foo`).
5. Sniffed `application/x-desktop` on a file with no name type -> `text/plain`.
6. `fast` never sniffs: PNG README answers `application/octet-stream`
   (name-only, uncertain) under fast, `app/x-pngdata` under full.
7. Unreadable uncertain file -> the name-only answer is kept (open failure);
   the readable control answers the sniffed type.
8. A trailing slash on a file path still answers the name type (`t.txt/` ->
   `text/plain`); on a dir path it answers `inode/directory`. (Both are just
   another path in the same case; the schema allows relative paths.)

## Known limits / flags for the L1 and the tool seat

- The case JSON is a **draft**; the predicate's frozen name is
  `filetype-cases-r97-frozen.json`. Content, ids and the 15-class order must
  not change after the freeze. Current sha256 (draft):
  `c5630cd0ccafa850435f9810d9366d2bff316efb6d97cd87c9d97667064ebbd2`.
- Determinism check: `--check` rebuilds and compares byte-for-byte
  (OK, 140 cases). Two consecutive runs produce identical sha256.
- The `FILES` in each case are complete for the case root (reads back what
  the probe wrote), so the counter can rebuild every case root from the JSON
  alone: directories (`*/`), file bytes, fifo/sock/symlink/unreadable entries
  in `paths`, modes in `mode`, attribute in `attr`. Host-absolute paths
  (`/dev/null`, `/dev/sda`, ...) are declared in `paths` and not created.
- Flaw worth a falsifier: `certain-10-empty-db-certain` (empty-db `a.png`
  with text bytes) answers `text/plain` -- the sniff fires (name-only is
  uncertain on an empty db) and the text fallback answers. It therefore
  separates "certain because of the db" from "certain because of the branch"
  less cleanly than the other `certain` cases; it is included as the
  empty-db contrast, not as a name-wins case. `uncertain-03` (`page.html`
  HTML bytes ~ multi name type + sniffed `text/html`) is the mirror.
- Scratch was `/fast/scratch/hyaku/mado-r97/R97MExecCasesC1` (kept during
  the run for rebuild; removed before yield per seat hygiene).

## Host-db amendment (after the mutant seat's heads-up)

The first draft pointed 14 cases (`*-host-db-*`) at `XDG_DATA_DIRS=/usr/share`
with no case-local mime tree. That shape is wrong on two counts: the counter
derives the database mode from `case["files"]` only (so those cases derived
`none` while the candidate prints `db=cache`), and the scored run's audit
allowlist only tracks case roots (a `/usr/share/mime` read could be denied).

Resolution (case bytes only; no counter change needed, no labels moved):

- The 6 label-bearing cases (`dir-10`, `empty-09`, `certain-09`,
  `uncertain-09`, `fast-09`, `readerr-10`) now carry a case-local copy of the
  host's `/usr/share/mime` tree: `globs2`, `globs`, `magic`, `aliases`,
  `subclasses` and `mime.cache` under `d1/mime/` (read at import by the
  probe's `host_db()` and frozen into `files` as base64). The counter derives
  `db=cache` from the case-local cache, and the labels are identical to the
  host-db labels (each re-verified under the mirror before the rebuilt file
  was accepted: all 6 cases `OK`).
- The 8 pure stat-branch cases (`dir-07`, `chr-09`, `blk-07`, `fifo-06`,
  `sock-06`, `zero-09`, `sym-08`, `brok-07`) now use an empty `d1`
  (`db=none`); their labels never depended on the database, so nothing
  changed for them either.

No case id, class, label, mode, attr or path changed. New draft sha256:
`c5630cd0ccafa850435f9810d9366d2bff316efb6d97cd87c9d97667064ebbd2`
(previous: `c88c06aacf447880bf44052fdf69219a8bcbee59024a81938cbeeffd13e088f8`).

## Files changed

- `.ufo/waves/round-97/controls/filetype-cases-r97.json` (new draft)
- `.ufo/waves/round-97/controls/filetype-probe-r97.py` (new builder)
- `.ufo/waves/round-97/w1/R97MExecCasesC1.md` (this report)

Report: `.ufo/waves/round-97/w1/R97MExecCasesC1.md`
