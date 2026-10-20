# S096 row draft — host walker version binding by file bytes (round 19)

Prepared by seat `MadoR19.HostWalkerBytes`, 2026-10-20. Host pause respected: walker,
pacman, yay, expat/pactree/checkupdates and every process probe were **not** run. Every fact
below was read as file bytes (`sha256sum`, `stat`, `file`, `readelf`, `gzip -dc`, `cat`,
`sed`, and `python3 open()`), and `/usr/bin/walker` was never executed.

## Row (11-column shape, `corpus/SOURCES.md`)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S096 | host walker version binding — `/usr/bin/walker` (compiled-in rodata literal) + `/var/lib/pacman/local/walker-2.17.2-1/desc` + `/var/log/pacman.log` | code | A | this host's installed walker version and package identity, read as file bytes only (no walker or pacman execution) | `/usr/bin/walker` 7,039,912 B sha256 `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096`, mtime `2026-10-08T11:14:32-0300`, BuildID `19200fe47eb6c90fc4956f0d52d0c7c84bb89e99`; literal `2.17.2\n` at file offset **856,302** inside `.rodata` (off `0x0b6900`, size `0x074654`), context `…loadstruct Action with 6 elementsversion2.17.2\ntoggle exact search…`; package `desc` sha256 `5c0d9d89d3e8d6c433b89ebaf2bb8f11056e15cfaed69a430333e0b8d50b0928` with `%VERSION%` `2.17.2-1`, `%BUILDDATE%` `1791468872` = `2026-10-08T14:14:32Z`, `%INSTALLDATE%` `1792498606` = `2026-10-20T12:16:46Z`; `/var/log/pacman.log` 244,858 B sha256 `27bbd0b558cfbc6ee27f5644863d6a62e1b468d462f4ea0de577ced86b256ffc`, line 2929 `upgraded walker (2.17.0-1 -> 2.17.2-1)` at `2026-10-20T09:16:46-0300`; package `mtree` (gzip, sha256 `d5dfb3f1f4d964aed2ab984c256df29109c8f67c42277b4e4168e279f1519aa4`) line 30 records `./usr/bin/walker … size=7039912 sha256digest=25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096` | the installed walker is version `2.17.2` by three independent file-byte facts — compiled-in rodata literal, package database `desc`, and the transaction log — whose dates agree (binary mtime = `%BUILDDATE%`; `%INSTALLDATE%` = log line 2929 timestamp), and the packaged digest equals the on-disk binary digest; no `2.17.0` literal survives (0 hits); **no running-process fact is claimed** — `walker --version` was not executed (host pause) | mined | 2026-10-20 | on-change | corpus/knowledge/walker-route-r18.md; corpus/knowledge/walker-deep-r9.md |

## Located quote (≤25 words)

- `/usr/bin/walker` @ byte 856,302: `version2.17.2` — the literal is the 7 bytes
  `2.17.2\n` (digits at 856,302, LF at 856,308).
- `/var/log/pacman.log:2929`: `upgraded walker (2.17.0-1 -> 2.17.2-1)`.

## Byte receipts (commands as run)

```text
$ sha256sum /usr/bin/walker
25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096  /usr/bin/walker
$ stat -c '%s bytes mtime=%y' /usr/bin/walker
7039912 bytes mtime=2026-10-08 11:14:32.000000000 -0300
$ file /usr/bin/walker
ELF 64-bit LSB pie executable, x86-64 … stripped
$ readelf -n /usr/bin/walker  (build-id)
Build ID: 19200fe47eb6c90fc4956f0d52d0c7c84bb89e99
$ python3  # open('/usr/bin/walker','rb').read()
size 7039912 sha256 25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096
b'2.17.2' count 1 first 856302
b'2.17.0' count 0
b'2.17.1' count 0
bytes[856302:856309] == b'2.17.2\n'
context[856262:856362] == b'loadstruct Action with 6 elementsversion2.17.2\ntoggle exact search%RESUME_LAST_QUERY%resume last que'
$ cat /var/lib/pacman/local/walker-2.17.2-1/desc
%VERSION% 2.17.2-1 ; %BUILDDATE% 1791468872 ; %INSTALLDATE% 1792498606
$ sed -n '2929p' /var/log/pacman.log
[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)
$ gzip -dc /var/lib/pacman/local/walker-2.17.2-1/mtree | grep bin/walker
./usr/bin/walker time=1791468872.0 size=7039912 sha256digest=25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096
```

`mtree` is gzip on disk; the on-disk (compressed) file digest is
`d5dfb3f1f4d964aed2ab984c256df29109c8f67c42277b4e4168e279f1519aa4`; the decompressed
stream digest is `eb38f891173da1f8efb2d1f55b499d8e9b2b3de11ca0afad4b280c61734e30e3`
(record the on-disk digest as the anchor, since that is the file byte identity).

## Moved pin against the round-9 note (old → new, not edited here)

- `corpus/knowledge/walker-deep-r9.md:109` reports `version2.17.0\n` at offset **847,791**
  in the then-installed binary (6,661,264 B, sha `64826a85…`, per
  `corpus/knowledge/walker-route-r18.md` § MOVED pins). The current 7,039,912 B binary
  carries `2.17.2\n` at offset **856,302**; a file offset is not comparable across builds,
  so only the literal shape (`version` + 7 bytes + LF) is the invariant: at the old offset
  847,791 the current binary holds XML template bytes
  (`<property name="vexpand">true</p…`), not a version literal.
- The `2.17.2` literal is the only `2.17.x` semver-like token in the rodata neighbourhood
  (a full-binary regex scan finds 251 semver-like tokens; within 840,000–880,000 only
  `2.17.2` at 856,302 and `0.22.10` at 856,676, the latter an unrelated UI/const string).

## Provenance of the literal, stated at its true strength

- **OBS:** the bytes `2.17.2\n` exist at file offset 856,302; the package version string is
  `2.17.2-1`; the log line and both package timestamps agree; the package's recorded digest
  and size equal the on-disk binary.
- **[INF]** that this literal is exactly what `walker --version` prints: the round-9 note
  established that method for the 2.17.0 binary by byte equality of the printed 7 bytes with
  the rodata run, and the shape here is identical (`version` token + 7 bytes + LF). It is not
  re-verified by execution — the host pause forbids running walker, so the row claims file
  bytes only.
- **[INF]** the left boundary of the literal is ambiguous: Rust rodata has no per-string NUL
  separators (the enclosing NUL-free run is 13,034 bytes, `[856175,869209)`), so the adjacent
  `version` token could be read as part of the same run; the right boundary is the LF at
  856,308.
- **[UNK]** Arch packaging patch level and build flags beyond the recorded `%BUILDDATE%`
  / `%PACKAGER%` fields; whether the process now running in the session was restarted at
  `HP:3062`/`HP:3123` (process state is not probed by constraint).

## Limits

No walker, pacman, systemctl, journalctl, pidof or hyprctl invocation; no reading of
`/proc`, no socket connection, no screenshot. The literal's identity with the printed
`--version` output is inherited from round 9 and marked `[INF]`; only file bytes were
measured here.
