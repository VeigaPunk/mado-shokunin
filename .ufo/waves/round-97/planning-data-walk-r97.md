# mado round 97 — L1 planning data walk (planner seat; before the freeze)

Measured 2026-11-07 on this host (glib2 2.90.1-1, `/usr/bin/gio` sha256
`$(sha256sum /usr/bin/gio)` see `.ufo/waves/round-97/receipts/`). Read-only; every
probe is `gio info -a standard::content-type` (or `standard::fast-content-type`, or `-n`).
This walk exists to prove the 15 case classes are reachable and that each branch the
declaration models is observable, before the wave's cases are frozen.

| branch the tool models | fixture | observed answer | note |
|---|---|---|---|
| directory | `p3/dir.png` | `inode/directory` | the branch wins over the `*.png` name |
| character device | `/dev/null`, `/dev/zero` | `inode/chardevice` | absolute host path, stat only |
| block device | `/dev/nvme1n1` | `inode/blockdevice` | absolute host path, stat only, never opened |
| FIFO | `p1/pipe1` (mkfifo) | `inode/fifo` | |
| socket | `p1/sock` (AF_UNIX bind) | `inode/socket` | |
| regular, size 0 | `p1/e.png`, `/proc/self/status`, `/proc/version` | `application/x-zerosize` | the zero-size branch precedes the name guess and the sniff |
| symlink, follow | `p1/l.txt -> a.txt` | `text/plain` | target's name and bytes |
| symlink, nofollow | `p1/l.txt` with `-n` | `inode/symlink` | |
| broken symlink | `p1/broken.txt -> nowhere` | `inode/symlink` (follow and nofollow) | |
| symlink loop | `p3/loop -> loop` | `inode/symlink` | stat fails ELOOP; is_symlink/broken |
| one name type, contradicting bytes | `p1/w.png` = `plain words` | `image/png` | one type is never sniffed (S522:1337-1340) |
| no name type, magic bytes | `p2/README`, `p2/blob.bin` | `text/x-readme`, `application/octet-stream`… then the sniff | `blob.bin` name guess is uncertain (ctypes: octet-stream uncertain=1) |
| several name types | `p2/page.html` | `text/html` (uncertain=1 then sniffed) | |
| `--fast` | `p3/page.html`, `p3/README`, `p3/zero.png` | `text/html`, `text/x-readme`, `application/x-zerosize` | fast never sniffs; zerosize branch still fires |
| read error | `p1/noread.dat` chmod 000 | `application/octet-stream` | open fails; the name-only answer stands (octet-stream, uncertain true) |
| desktop rewrite | `p1/d.desktop` garbage bytes | `application/x-desktop` | one name type, no sniff |
| trailing slash on a file | `p3/a.txt/` | no `standard::content-type` line (gio errors) | outside the scored surface (declared) |
| missing path | `p1/missing.txt` | gio rc 2, no attribute | outside the scored surface (declared) |

Name-only answers measured with ctypes `g_content_type_guess(name, NULL, 0, &uncertain)` (scratch probe, not a
committed tool): `README -> text/x-readme 0`, `blob.bin -> application/octet-stream 1`, `noext -> application/octet-stream 1`,
`x.y.z -> application/x-compress 0`, `page.html -> text/html 1`, `d.desktop -> application/x-desktop 0`.

Consequences folded into the freeze:

1. The `blk` class is reachable on this host through `/dev/nvme1n1` (never opened); the case file declares absolute
   host paths for `chr` and `blk` only.
2. `/proc/self/status` and `/proc/version` are `application/x-zerosize` (size 0), so they belong to the `zero`
   class, not to a read-error class.
3. A read-protected regular file answers `application/octet-stream` with the name-only rule; the `readerr` class
   must be scored on the type only (the uncertain flag is not printed by `gio info`).
4. A trailing-slash path to a file and a missing path produce no attribute; both are refused by the candidate
   (`ERROR stat`, exit 2) and excluded from the case labels.
5. The symlink loop and the dangling symlink answer `inode/symlink` under both modes, so the `brok` and `sym`
   classes need their own fixtures (loop vs dangling) rather than sharing one.
