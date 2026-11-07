# R97MScribeEntry - scribe report (round 97, wave w1)

Seat: `R97MScribeEntry` (leaf; no subagent dispatch). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, base `e6152b589c2c6a28426c28263c4bcc3c46398be4`.
Scope: write only `.ufo/waves/round-97/w1/drafts/` and this report. I wrote no product code, no
`corpus/`, no `SKILL.md`, no `quality/`, no git index or jj state, and no sibling lane; I installed or
upgraded no tool (no package, `uv`, `npx` or binary install was needed).

## 1. What was done

1. Read the contract first: `.ufo/waves/round-97/claims-declaration-r97.md`,
   `corpus/QUALITY.md` 162-167, the `SKILL.md` registry tables (headers at lines 786 and 928; the
   `mado-selftest-strength` row at 879), `corpus/lessons/round-96.md`, `corpus/lessons/round-96-verifier-spotcheck.md` (the mined
   defects D1-D13), the round-96 entry `corpus/knowledge/mime-textdb-magic-r96.md` for shape, and
   `quality/tool-ledger.md` + `quality/check-tool-ledger.py` for the ledger population rule.
2. Re-derived the C1 model from the L1's fetched bytes in `.ufo/waves/round-97/fetch/`
   (`gcontenttype-fdo.c` 8a5b4f47...a2d7c, `glocalfileinfo.c` b006a93d...4497, `gio.1.gz`
   810077be...a565) and ran the installed oracle `/usr/bin/gio` (sha256 d2164260...cfc462,
   glib2 2.90.1-1) on 36 host-database rows and 13 private-database rows, all read-only, all
   fixtures built under scratch. One extra fetch, `gio/gcontenttype.c` (HTTP 200, 10399 B, sha256
   fb9c68782af7c266f22551ef11e328f9d2491c262efd3de7336dbbfc36554664), was made only to check the
   public wrapper's delegation; its bytes were not committed and it is not proposed as a row.
3. Wrote the six drafts listed in section 2, with every rule located to a source line or to a probe
   row, ASCII-only, and quotes <= 25 words.
4. Reported the conflicts verbatim (section 3) instead of widening or smoothing any predicate.
5. Coordination: `R97MScoutSources` confirmed S526 and S527 as the next free ids and re-measured
   every digest twice (byte-identical to mine), and supplied two corrections I applied to the drafts:
   (a) the `gio.1.gz` decompressed size is 18793 (the receipt's 13688 is wrong), and (b) a `file://`
   locator has no HTTP status (`curl -w '%{http_code}'` prints 000), so S527 must be shaped like the
   installed-man rows S509/S510 rather than as an HTTP 200. The scout also bounded S527's scope (the
   page contains no `content-type` text and no version in its `.TH` line) and S526's (name only the
   uncovered lines, never the guess implementation S518 anchors). All four are now in the drafts.

## 2. Artifacts (all under `.ufo/waves/round-97/w1/`)

| path | what it is | sha256 |
|---|---|---|
| `drafts/gio-content-type-file-r97.md` | the knowledge entry `corpus/knowledge/gio-content-type-file-r97.md` in r96's shape: front matter with source ids (S522, S526, S527, S518, S521, S524, S525, S519, S520, S515/S516, S505), sections 1-11, a stat-branch table with one row per branch and its line, the sniff gate and length table, the fast attribute, the guess-combination recap, 36+13 oracle-labelled probe rows, 49 located quotes, and a `## 11. Verify` section with pasteable oracle and tool commands | `48ee2bd9906ec4ea7d3b91f81f658331e8cd3ed64fc4c61cd98df52edb04fc14` |
| `drafts/round-97.md` | the lesson `corpus/lessons/round-97.md`: `## Mistakes` with M97-1 (the mined D12 erratum) and M97-2 (this round's refusal-sentinel finding), the `## Gate` rows/candidates/findings, `## Census`, `## Cross-domain evidence` | `4a2187a7b4fae72b928841d8a7cd0002dbc034155c562145a2c1fd8603925c80` |
| `drafts/sources-rows-r97.md` | the S526 and S527 rows in the 13-column shape, the ten `used-by` appends (old -> new), the census and fetch notes | `db5acac48ef6704b082a9214d3d5a662ea30c0efe0b64d99baeac5c4e8128570` |
| `drafts/skill-registry-rows-r97.md` | six registry rows (three missing round-96 rows, the kill-set row, the two round-97 rows), the `mado-selftest-strength` list amendment, and the measured base state of the registry | `144aa62c2b63b56d0a92182258f8b943c7fd043882f7005f8d4e418a6d89dd90` |
| `drafts/ledger-rows-r97.md` | three `quality/tool-ledger.md` rows (`tools/mado-filetype.py`, the two round-97 counters) plus the population note that keeps the kill-set JSON out | `0a05ef601fca37bf0a9c5b7dcf9453593db7d632e46cc7f7c682c6ed60c2894d` |
| `R97MScribeEntry.md` | this report, with the probe script and its transcript inline (section 4) | this file |

## 3. Findings routed to the L1 (verbatim conflicts, with the measurement)

1. **The registry count at base is 1, not 0.** C2 (iv) says the registry "moves `0 -> 4` rows for the
   four named artifacts". At base `e6152b58`, `git show HEAD:SKILL.md | grep -c "mado-mimetext"` = 1
   (the row at `SKILL.md:887`, added by `5dd921b3`), and the other three names count 0 each. So a
   literal `0 -> 4` assertion is false at the base and the C2 counter must count the rows it
   re-derives (the move is `1 -> 4`, or `0 -> 3` over the three absent ones).
2. **C1 rule 7 and shared contract 1 name the wrong refusal condition for a failed stat.** Measured:
   a `lstat` failing with `EACCES` is tolerated (`glocalfileinfo.c:1941-1942`, `if (errsv != EACCES)`)
   and answered from the name - probe `H-eacces` prints `application/octet-stream`, exit 0, while
   `stat` and `head` on the same path fail with `EACCES`. A symlink loop is not a stat failure at
   this surface: the `lstat` succeeds, the follow `stat` fails with `ELOOP`, and `symlink_broken`
   (`:1994`) makes branch 1 answer `inode/symlink` - probe `H-loop`, exit 0 (`stat -L` fails). Only
   `ENOENT`/`ENOTDIR` refuse (probes `H-missing`, `H-enotdir`: no attribute line, exit 2). The
   contract's "a path that cannot be stat'ed at all (missing, or a symlink loop) ... `ERROR stat` ...
   exits 2" therefore mislabels two reachable shapes, which is `QUALITY.md` 166's class applied to an
   input state.
3. **C1 rule 1's "identity on Unix" is not the identity.** The Unix implementation is
   `gcontenttype-fdo.c:551-565`, and `:560` is `umime = g_strdup (xdg_mime_unalias_mime_type
   (mime_type));`. Measured: with a private `mime/aliases` holding `inode/symlink
   application/x-aliased`, `gio info -n` on an untouched symlink answers `application/x-aliased`
   (probe `D-alias_map`); with the fields reversed it answers `inode/symlink` (`D-alias_rev`).
   `R97MScoutSources` independently measured the same effect on two other branches (a directory and a
   zero-size file answered their aliased types). The frozen case tree must either carry a consistent
   alias table or no alias edge.
4. **The sniff clamp is observable and needs three boundary cases, not one.** Extent 16383 (rule at
   `16380`) matches (`D-b16380`); extent 16385 clamps to 16384 and still matches because the compare
   allows `i + value_length == len` (`D-b16382`); extent 16388 clamps and misses (`D-b16385`). A rule
   at offset 20000 is unreachable for a GIO caller (`D-far_off20000` -> `text/plain`).
5. **The `gio.1.gz` decompressed size in the L1's fetch receipt is wrong.** The receipt cell reads
   `decompressed=13688`; `gzip -dc gio.1.gz | wc -c` prints 18793 (781 lines, digest
   `84b3cdad868feecd69f113b789d7009113e16531b67d750cd0e424ba2bcb8bc5`, which the receipt has right).
   No source claim depends on the byte count, but the cell should be corrected (`census`/receipt
   fidelity, round-96 D11's lesson).
6. **The declaration's branch line ranges drift by 1-2 lines.** Re-derived from the fetched bytes:
   symlink `1308-1310` (declared `1309-1312`), directory `1311` (declared `1313`), chardev
   `1314-1315` (declared `1316`), block `1316-1317` (declared `1317`), FIFO `1318-1319` (declared
   `1318`), zerosize `1320-1326` (declared `1319-1325`), socket `1328-1330` (declared `1327`), clamp
   `1353-1355` (declared `1352-1355`), open `1358-1362` (declared `1357-1364`), read/re-guess
   `1368-1373` (declared `1368-1374`); the function ends at `1382`, not `1389`. The entry uses the
   re-derived ranges.
7. **`gio info`'s exit `2` is a CLI mapping, not a documented code.** `gio.1:775` promises only `On
   success, \fB0\fP is returned, a non\-zero failure code otherwise.` The `2` is measured
   (`H-missing`, `H-enotdir`). The tool's contract copies the measurement, which is fine, but no
   source row grounds it as a documented value.
8. **The `--fast` difference is a difference in type, not only in cost.** `F-d_bin` answers
   `application/octet-stream` where the full attribute answers `text/plain`; `D-near_fast` answers
   `application/octet-stream` where `D-near_off100` answers `application/x-near`.
   `standard::fast-content-type` is therefore not a cheaper spelling of the full attribute.
9. **The C2 registry gap is real and its data is 7 kills / 6 checks.** `quality/selftest-kills/
   check-receipt-presence.json` holds 7 kills and `selftest_checks: 6`; the strength gate's own
   `--selftest` prints `SELFTEST_STRENGTH_SELFTEST: checks=11 failed=0`; and at base both round-96
   counters refuse `--selftest` (exit 2, usage), which is the C2 "before" state measured here.

10. **The candidate's fixed `max_buffer_extents = 16384` is answer-equivalent, not a defect.**
   `.ufo/waves/round-97/build/mado-filetype.py` (report `.ufo/waves/round-97/w1/R97MExecToolC1.md`)
   clamps a constant 16384 instead of asking the database. Every matchlet lies inside the database's
   extent by construction, so reading more can never add a match; only the upper side of the clamp is
   observable (probes `D-b16380/82/85`). The model sentence in the entry says so, so the row and the
   tool agree - no case should be written to separate them.
11. **A root-run harness cannot carry the `EACCES` shape.** Probes here ran as uid 1000 and the
   tolerated branch was live (`H-eacces`). The tool seat reports that its unreadable-file fixtures
   stay readable in its harness; under root the mode bits do not block `lstat` or `open`, so a
   `readerr` case that means "EACCES at the stat" needs a declared non-root harness (or a label from
   whatever the measuring harness's oracle answers). The entry's limit 3 now states this.

12. **A `file://` row carries no HTTP status.** The L1 receipt records the `gio.1.gz` row as
   "-> 200"; `curl -sS -o /dev/null -w '%{http_code}' file:///usr/share/man/man1/gio.1.gz` prints
   `000` because no HTTP transaction happens. Shape S527 like the installed-man rows S509/S510
   (`file://` path, container and decompressed digests, owner `pacman -Qo` = glib2 2.90.1-1) and do
   not claim a transport event. Related scope limits, both measured: the page contains zero
   occurrences of `content-type` (its only attribute example is `standard::icon` at lines 200, 244
   and 661), and its `.TH` line is `.TH "gio" "" "" ""` with no version or date.

13. **S522's held anchor cell drifts by one line.** Its cell reads `1345 (16 KiB buffer),
   `1351-1353 (sniff length)`, `1368-1374 (read and guess with data)`; measured on the same bytes:
   the buffer is at `1346`, the sniff-length call at `1353` with the clamp at `1354-1355`, and the
   read/re-guess pair at `1368-1373` (`1374` is a closing brace). `1337` and `1340` are exact. The
   proposals (held row, needs an old -> new log) are in `drafts/sources-rows-r97.md` section 3;
   `R97MScoutSources`' D4 reaches the same two numbers independently.

**Landing order the L1 must keep.** Census E11 (`scripts/sources-census.sh:566`) requires a `mined`
row's `used-by` path to exist on disk, and `corpus/knowledge/gio-content-type-file-r97.md` does not
exist at base: the entry must land before or with the registry commit that marks S526/S527 `mined`,
or the census fails on the round's own rows.

**Where those corrections must land.** Both wrong cells (F5's `13688`, F12's `-> 200`) live in the
L1's own `.ufo/waves/round-97/receipts/sources-open-r97.txt`, which is outside this seat's and the
scout's write scope; `R97MScoutSources`' receipt quotes both cells verbatim beside the re-measured
values and this draft carries the corrected figures, so the L1 can land an append-only correction
there and the two artifacts will agree.

**Deltas against `R97MScoutSources`' report (so the two do not read as contradicting).** F2 and
their D6 agree on the symlink loop; F2 is the fuller statement (it also carries the `EACCES`
tolerance and the `ENOENT`/`ENOTDIR` refusal, which their D6 mentions only in passing). F6 and their
D4 agree on every branch line and both flag `1337`/`1340` as exact; F13 above is the anchor-cell
correction that follows from both. The sniff-length function span is `54-66` (closing brace at 66) in
both drafts; their file cites `551-566` for the Unix implementation where this seat cites `551-565`
(closing brace at 565) - the cited lines are the same lines, only the end-of-block convention
differs.

## 4. Probes (the evidence for section 3 and for the entry's section 7)

Producer: `probe-all.sh`, sha256 `17e87b3b6dbda5afe7211359f88554647b7466d7b533ccfba87d40ac2ebf1c90`; transcript `probe-all.out.txt`, sha256 `cd86bca89f90c50701855ab688659b46b6e0d256025eb9f0f50640919573b9fb`, exit 0.
Read-only: `lstat`/`stat`, `mime/` reads under scratch roots, `/usr/bin/gio`; one `mkfifo`, one
`AF_UNIX` bind and `chmod` inside scratch; no network, no host config, no service.

```text
# host
gio_sha256 d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462
gio_version 2.90.1
glib2 glib2 2.90.1-1
shared_mime_info shared-mime-info 2.5.1-2
mime_cache_present yes

# host database (HOME=<empty>, XDG_DATA_HOME and XDG_DATA_DIRS unset -> /usr/share/mime)
HOST a_txt          -    rc=0 text/plain
HOST w_png          -    rc=0 image/png
HOST e_png          -    rc=0 image/png
HOST mis_txt        -    rc=0 text/plain
HOST d_desktop      -    rc=0 application/x-desktop
HOST d_bin          -    rc=0 text/plain
HOST plain_bin      -    rc=0 text/plain
HOST zero_bin       -    rc=0 application/x-zerosize
HOST zero_png       -    rc=0 application/x-zerosize
HOST sub            -    rc=0 inode/directory
HOST sub_slash      -    rc=0 inode/directory
HOST sub2_png       -    rc=0 inode/directory
HOST fifo           -    rc=0 inode/fifo
HOST fifo_png       -    rc=0 inode/fifo
HOST sock           -    rc=0 inode/socket
HOST chardev        -    rc=0 inode/chardevice
HOST unread_bin     -    rc=0 application/octet-stream
HOST unread_png     -    rc=0 image/png
HOST link_follow    -    rc=0 text/plain
HOST link_nofollow  -n   rc=0 inode/symlink
HOST broken         -    rc=0 inode/symlink
HOST dirlink        -    rc=0 inode/directory
HOST dirlink_n      -n   rc=0 inode/symlink
HOST fifolink       -    rc=0 inode/fifo
HOST socklink       -    rc=0 inode/socket
HOST loop           -    rc=0 inode/symlink
HOST loop_n         -n   rc=0 inode/symlink
HOST missing        -    rc=2 
HOST enotdir        -    rc=2 
HOST eacces         -    rc=0 application/octet-stream
HOST two_locations  -    rc=0 text/plain/image/png/
HOST default_attrs  -    rc=0 full=application/x-near fast=application/octet-stream
FAST fast_e_png     -    rc=0 image/png
FAST fast_d_bin     -    rc=0 application/octet-stream
FAST fast_unread    -    rc=0 application/octet-stream
FAST fast_chardev   -    rc=0 inode/chardevice

# private text databases (XDG_DATA_DIRS=<db>, XDG_DATA_HOME=<empty>)
DB   near_off100    db1    rc=0 application/x-near
DB   near_fast      db1    rc=0 application/octet-stream
DB   far_off20000   db2    rc=0 text/plain
DB   off100_other   db1    rc=0 text/plain
DB   name_zz        db3    rc=0 application/x-zz
DB   name_zz_fast   db3    rc=0 application/x-zz
DB   b16380         db4    rc=0 application/x-b16380
DB   b16382         db6    rc=0 application/x-b16382
DB   b16385         db5    rc=0 text/plain
DB   alias_map      db7    rc=0 application/x-aliased
DB   alias_rev      db8    rc=0 inode/symlink
DB   none_db        dbnone rc=0 text/plain
DB   none_chardev   dbnone rc=0 inode/chardevice

# private database digests (first 16 hex of sha256)
db1     magic=5adb90a524c3deb0 aliases= globs2=
db2     magic=87012fd13ba004f4 aliases= globs2=
db3     magic=5adb90a524c3deb0 aliases= globs2=3f500eb90637f00f
db4     magic=7cff2f88b5df7b4d aliases= globs2=
db5     magic=4717707c27f7f0a1 aliases= globs2=
db6     magic=423a09f9e250b20b aliases= globs2=
db7     magic= aliases=786066dc68fdcced globs2=
db8     magic= aliases=210f023e209f3542 globs2=
```

The script, for re-running (it builds its own tree under `$S`):

```sh
#!/bin/bash
# R97MScribeEntry read-only probe of /usr/bin/gio "standard::content-type" for a path.
# Builds every fixture under $S/probe (scratch), writes nothing else, launches no
# application, opens no network. One invocation reproduces the whole transcript.
set -u
S=${S:?}
P=$S/probe
G=/usr/bin/gio
rm -rf "$P"
mkdir -p "$P/h" "$P/h2" "$P/dh2/mime" "$P/fix" \
         "$P/db1/mime" "$P/db2/mime" "$P/db3/mime" "$P/db4/mime" "$P/db5/mime" \
         "$P/db6/mime" "$P/db7/mime" "$P/db8/mime" "$P/dbnone"
FIX=$P/fix

python3 - "$P" <<'PY'
import os, sys
p = sys.argv[1]; fix = os.path.join(p, "fix")
def w(rel, data):
    full = os.path.join(fix, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "wb").write(data)
png = b"\x89PNG\r\n\x1a\n0000000000"
desktop = b"[Desktop Entry]\nType=Application\nName=probe\n"
w("a.txt", b"hello\n"); w("w.png", png); w("e.png", b"hello\n"); w("mis.txt", png)
w("d.desktop", desktop); w("d.bin", desktop); w("plain.bin", b"hello\n")
w("zero.bin", b""); w("zero.png", b"")
w("unread.bin", b"garbage\n"); w("unread.png", b"hello\n")
os.chmod(os.path.join(fix, "unread.bin"), 0o000); os.chmod(os.path.join(fix, "unread.png"), 0o000)
os.makedirs(os.path.join(fix, "sub")); os.makedirs(os.path.join(fix, "sub2.png"))
os.mkfifo(os.path.join(fix, "fifo.bin")); os.mkfifo(os.path.join(fix, "fifo.png"))
w("noax/f.bin", b"hello\n"); os.chmod(os.path.join(fix, "noax"), 0o000)

HDR = b"MIME-Magic\x00\n"
def magic(off):
    return HDR + b"[80:application/x-b" + str(off).encode() + b"]\n>" + str(off).encode() + \
           b"=" + b"\x00\x02" + b"AB" + b"\n"
def put(db, name, data):
    open(os.path.join(p, db, "mime", name), "wb").write(data)
put("db1", "magic", HDR + b"[80:application/x-near]\n>100=\x00\x02AB\n")
put("db2", "magic", HDR + b"[80:application/x-far]\n>20000=\x00\x02AB\n")
put("db3", "magic", HDR + b"[80:application/x-near]\n>100=\x00\x02AB\n")
put("db3", "globs2", b"50:application/x-zz:*.zz\n")
put("db4", "magic", magic(16380)); put("db5", "magic", magic(16385)); put("db6", "magic", magic(16382))
put("db7", "aliases", b"inode/symlink application/x-aliased\n")
put("db8", "aliases", b"application/x-aliased inode/symlink\n")
near = bytearray(b"." * 100); near += b"AB"
far  = bytearray(b"A" * 20000); far += b"AB"
for off, nm in ((16380, "b16380.zzz"), (16385, "b16385.zzz"), (16382, "b16382.zzz")):
    b = bytearray(b"A" * 16390); b[off:off + 2] = b"AB"; w(nm, bytes(b))
w("near.zzz", bytes(near)); w("far.zzz", bytes(far)); w("near.zz", bytes(near))
PY

ln -sfn a.txt "$FIX/link.txt"; ln -sfn missing.txt "$FIX/broken.txt"
ln -sfn sub "$FIX/dirlink"; ln -sfn fifo.bin "$FIX/fifolink"; ln -sfn sock.bin "$FIX/socklink"
ln -s loop2 "$FIX/loop1"; ln -s loop1 "$FIX/loop2"
python3 -c "import socket; s=socket.socket(socket.AF_UNIX); s.bind('$FIX/sock.bin')"

echo "# host"
echo "gio_sha256 $(sha256sum "$G" | cut -d' ' -f1)"
echo "gio_version $(env -i LC_ALL=C "$G" --version 2>&1 | head -1)"
echo "glib2 $(pacman -Q glib2 2>/dev/null)"
echo "shared_mime_info $(pacman -Q shared-mime-info 2>/dev/null)"
echo "mime_cache_present $(test -f /usr/share/mime/mime.cache && echo yes || echo no)"
echo

run_host() {   # label path [flags...]
  local label=$1 path=$2; shift 2
  local out rc
  out=$(env -i LC_ALL=C HOME="$P/h" "$G" info "$@" -a standard::content-type "$path" 2>&1); rc=$?
  printf 'HOST %-14s %-4s rc=%s %s\n' "$label" "${*:--}" "$rc" \
    "$(printf '%s\n' "$out" | sed -n 's/^ *standard::content-type: //p' | head -1)"
}
run_fast() {
  local label=$1 path=$2
  local out rc
  out=$(env -i LC_ALL=C HOME="$P/h" "$G" info -a standard::fast-content-type "$path" 2>&1); rc=$?
  printf 'FAST %-14s %-4s rc=%s %s\n' "$label" - "$rc" \
    "$(printf '%s\n' "$out" | sed -n 's/^ *standard::fast-content-type: //p' | head -1)"
}
run_db() {     # label db path attr [flags]
  local label=$1 db=$2 path=$3 attr=$4; shift 4
  local out rc
  out=$(env -i LC_ALL=C HOME="$P/h2" XDG_DATA_HOME="$P/dh2" XDG_DATA_DIRS="$P/$db" \
        "$G" info "$@" -a "$attr" "$path" 2>&1); rc=$?
  printf 'DB   %-14s %-6s rc=%s %s\n' "$label" "$db" "$rc" \
    "$(printf '%s\n' "$out" | sed -n "s/^ *$attr: //p" | head -1)"
}

echo "# host database (HOME=<empty>, XDG_DATA_HOME and XDG_DATA_DIRS unset -> /usr/share/mime)"
run_host a_txt        "$FIX/a.txt"
run_host w_png        "$FIX/w.png"
run_host e_png        "$FIX/e.png"
run_host mis_txt      "$FIX/mis.txt"
run_host d_desktop    "$FIX/d.desktop"
run_host d_bin        "$FIX/d.bin"
run_host plain_bin    "$FIX/plain.bin"
run_host zero_bin     "$FIX/zero.bin"
run_host zero_png     "$FIX/zero.png"
run_host sub          "$FIX/sub"
run_host sub_slash    "$FIX/sub/"
run_host sub2_png     "$FIX/sub2.png"
run_host fifo         "$FIX/fifo.bin"
run_host fifo_png     "$FIX/fifo.png"
run_host sock         "$FIX/sock.bin"
run_host chardev      /dev/null
run_host unread_bin   "$FIX/unread.bin"
run_host unread_png   "$FIX/unread.png"
run_host link_follow  "$FIX/link.txt"
run_host link_nofollow "$FIX/link.txt" -n
run_host broken       "$FIX/broken.txt"
run_host dirlink      "$FIX/dirlink"
run_host dirlink_n    "$FIX/dirlink" -n
run_host fifolink     "$FIX/fifolink"
run_host socklink     "$FIX/socklink"
run_host loop         "$FIX/loop1"
run_host loop_n       "$FIX/loop1" -n
run_host missing      "$FIX/nope.bin"
run_host enotdir      "$FIX/a.txt/x"
run_host eacces       "$FIX/noax/f.bin"
two=$(env -i LC_ALL=C HOME="$P/h" "$G" info -a standard::content-type "$FIX/a.txt" "$FIX/w.png" 2>&1 |
      sed -n 's/^ *standard::content-type: //p' | tr '\n' '/')
printf 'HOST %-14s %-4s rc=%s %s\n' two_locations - 0 "$two"
dflt=$(env -i LC_ALL=C HOME="$P/h2" XDG_DATA_HOME="$P/dh2" XDG_DATA_DIRS="$P/db1" "$G" info "$FIX/near.zzz" 2>&1)
printf 'HOST %-14s %-4s rc=%s full=%s fast=%s\n' default_attrs - 0 \
  "$(printf '%s\n' "$dflt" | sed -n 's/^ *standard::content-type: //p')" \
  "$(printf '%s\n' "$dflt" | sed -n 's/^ *standard::fast-content-type: //p')"
run_fast fast_e_png   "$FIX/e.png"
run_fast fast_d_bin   "$FIX/d.bin"
run_fast fast_unread  "$FIX/unread.bin"
run_fast fast_chardev /dev/null
echo

echo "# private text databases (XDG_DATA_DIRS=<db>, XDG_DATA_HOME=<empty>)"
run_db near_off100   db1 "$FIX/near.zzz" standard::content-type
run_db near_fast     db1 "$FIX/near.zzz" standard::fast-content-type
run_db far_off20000  db2 "$FIX/far.zzz"  standard::content-type
run_db off100_other  db1 "$FIX/far.zzz"  standard::content-type
run_db name_zz       db3 "$FIX/near.zz"  standard::content-type
run_db name_zz_fast  db3 "$FIX/near.zz"  standard::fast-content-type
run_db b16380        db4 "$FIX/b16380.zzz" standard::content-type
run_db b16382        db6 "$FIX/b16382.zzz" standard::content-type
run_db b16385        db5 "$FIX/b16385.zzz" standard::content-type
run_db alias_map     db7 "$FIX/link.txt" standard::content-type -n
run_db alias_rev     db8 "$FIX/link.txt" standard::content-type -n
run_db none_db       dbnone "$FIX/near.zzz" standard::content-type
run_db none_chardev  dbnone /dev/null standard::content-type
echo
echo "# private database digests (first 16 hex of sha256)"
for d in db1 db2 db3 db4 db5 db6 db7 db8; do
  printf '%-7s magic=%s aliases=%s globs2=%s\n' "$d" \
    "$(sha256sum "$P/$d/mime/magic" 2>/dev/null | cut -c1-16)" \
    "$(sha256sum "$P/$d/mime/aliases" 2>/dev/null | cut -c1-16)" \
    "$(sha256sum "$P/$d/mime/globs2" 2>/dev/null | cut -c1-16)"
done
chmod 755 "$FIX/noax"
```

## 5. Gates applied, and what this seat did not do

- Located claims only: every rule in the entry cites a fetched line or a probe row; nothing is marked
  `[UNVERIFIED]` and no cell of the frozen measurement tables is filled with a number this seat did
  not measure (round-96 D2). The L1's C1 receipt supplies those cells.
- Quotes: each is a whitespace-collapsed line of the fetched bytes and `<= 25` words; the S527 quotes
  are the raw roff lines, and the one line that carries a non-ASCII apostrophe is quoted as an
  ASCII substring with a note (ASCII-only artifacts).
- Provenance: digests are this seat's `sha256sum` reads of the wave's fetched bytes and of
  `/usr/bin/gio`; the producer status was checked (`curl -w '%{http_code}'` -> 200 for the one
  extra fetch; `sha256sum` exit 0 for every digest).
- Not done, by scope: no build, test or lint of any instrument and no counter run. Sibling drafts
  appeared under `.ufo/waves/round-97/build/` while this seat worked (`mado-filetype.py`,
  `c2-r97-counter-selftest.py`); I read the tool's report for corroboration (findings 10-11) and ran
  none of them. No census validator run; no commit, push, `jj` or git mutating command; no package
  install; no live compositor or application probe; no `agent://all`.

## 6. Cleanup

Scratch `$HYAKU_SCRATCH/mado-r97/R97MScribeEntry` held only the probe tree, the one fetched file and
the transcript embedded above; it was deleted before yield. No temporary file was left in `/tmp` and
nothing was copied outside the two declared paths.
