# HostWalkerBytes — host walker is 2.17.2 by three agreeing file-byte facts; compiled literal `2.17.2\n` at offset 856,302

Seat `MadoR19.HostWalkerBytes` (wave 1, fan-out). Question: what version does this host's
walker install carry, determinable from file bytes alone under the host pause? Answer:
**2.17.2**, bound independently by the binary's compiled-in rodata literal, the pacman
package `desc`, and `/var/log/pacman.log:2929`; the packaged digest equals the on-disk
digest. No `2.17.0` literal survives in the binary. `walker --version` was **not** run.

Draft delivered: `.ufo/waves/round-19/drafts/HostWalkerBytes-row.md` (reserved row **S096**,
11 columns, kind `code`, tier `A`, status `mined`, opened `2026-10-20`, recheck `on-change`).

## Evidence (commands run; walker/pacman never executed)

1. Binary identity — `/usr/bin/walker` is a regular file (not a symlink; `readlink -f`
   returns itself):

   ```text
   $ sha256sum /usr/bin/walker
   25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096  /usr/bin/walker
   $ stat -c '%s bytes mtime=%y' /usr/bin/walker
   7039912 bytes mtime=2026-10-08 11:14:32.000000000 -0300
   $ file /usr/bin/walker
   ELF 64-bit LSB pie executable, x86-64 … stripped
   $ readelf -n /usr/bin/walker
   Build ID: 19200fe47eb6c90fc4956f0d52d0c7c84bb89e99
   ```

2. Compiled-in version literal — `python3` with `open('/usr/bin/walker','rb').read()`:

   ```text
   size 7039912 sha256 25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096
   data.find(b'2.17.2') -> 856302  (exactly 1 occurrence)
   data.find(b'2.17.0') -> -1      (0 occurrences)
   data.find(b'2.17.1') -> -1      (0 occurrences)
   bytes[856302:856309] = b'2.17.2\n'
   data[856262:856362] = b'loadstruct Action with 6 elementsversion2.17.2\ntoggle exact search…'
   ```

   `readelf -SW` places offset 856,302 inside `.rodata` (`off 0x0b6900`, `size 0x074654`,
   i.e. file bytes 747,776–1,224,531; section-relative 108,526). Compare
   `corpus/knowledge/walker-deep-r9.md:109` — the 2.17.0 binary had `version2.17.0\n` at
   offset 847,791 (6,661,264 B, sha `64826a85…`). Offsets are not comparable across builds;
   the literal shape is the invariant and it matches. The old offset is not reusable on
   this build: `data[847791-20:847791+24]` is `b'            <property name="vexpand">true</p'`
   (XML template bytes), so a check that hard-codes 847,791 would read template text, not a
   version.

3. Package database — `cat /var/lib/pacman/local/walker-2.17.2-1/desc` (dir name itself
   carries `2.17.2-1`; file sha256 `5c0d9d89d3e8d6c433b89ebaf2bb8f11056e15cfaed69a430333e0b8d50b0928`):

   ```text
   %NAME%    walker
   %VERSION% 2.17.2-1
   %BUILDDATE%   1791468872   = 2026-10-08T14:14:32Z = 2026-10-08T11:14:32-03:00
   %INSTALLDATE% 1792498606   = 2026-10-20T12:16:46Z = 2026-10-20T09:16:46-03:00
   %PACKAGER% Omarchy <pkgs@omarchy.org>
   %VALIDATION% sha256, pgp
   ```

   `%BUILDDATE%` equals the binary's mtime to the second; `%INSTALLDATE%` equals the
   transaction log timestamp below to the second.

4. Transaction log — `/var/log/pacman.log`, 244,858 B, 3,169 lines, sha256
   `27bbd0b558cfbc6ee27f5644863d6a62e1b468d462f4ea0de577ced86b256ffc`:

   ```text
   line 2929: [2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)
   line 1943: [2026-10-11T16:14:39-0300] [ALPM] upgraded walker (2.16.2-1 -> 2.17.0-1)
   lines 3062, 3123: running 'walker-restart.hook'  (09:18:25, 09:31:04)
   ```

   Line 2929's own sha256 is `2b9fad9a21da73eff330d54278d828a923805ed22ed055e0c8bfe523c8ccce3a`.
   S090 already cites this line; S096 adds the binary literal, the package `desc`, and the
   whole-log digest.

5. Package file manifest — `mtree` is gzip on disk (sha256
   `d5dfb3f1f4d964aed2ab984c256df29109c8f67c42277b4e4168e279f1519aa4`; decompressed
   `eb38f891173da1f8efb2d1f55b499d8e9b2b3de11ca0afad4b280c61734e30e3`):

   ```text
   $ gzip -dc /var/lib/pacman/local/walker-2.17.2-1/mtree | grep bin/walker
   ./usr/bin/walker time=1791468872.0 size=7039912 sha256digest=25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096
   ```

   The packaged `size`/`sha256digest` equal the on-disk binary exactly: the installed file
   is the packaged file.

## Reading of the evidence

- **OBS:** three independent file-byte facts agree on `2.17.2` — rodata literal, package
  `desc`, package name-dir plus appended version `/var/lib/pacman/local/walker-2.17.2-1`.
  Their timestamps cross-agree (build date = mtime; install date = log line).
- **OBS:** `2.17.0` occurs zero times in the current binary, so no stale literal can be
  mistaken for the live pin by a byte-level check.
- **[INF]** that `walker --version` prints exactly these 7 bytes: round 9 established the
  method by byte equality on the 2.17.0 build (`corpus/knowledge/walker-deep-r9.md` §2.3),
  and the shape is identical here; the host pause forbids re-verifying by execution, and the
  row states file-byte evidence only, as C2 requires.
- **[INF]** the literal's left boundary is ambiguous: Rust rodata has no NUL separators
  between strings (the enclosing NUL-free run spans `[856175,869209)`, 13,034 bytes), so the
  adjacent `version` token is not provably separate. The right boundary (LF at 856,308) is
  unambiguous.
- **[UNK]** running-process state: log lines 3062/3123 record restart hooks, but no process
  probe was made (constraint), so what binary the current session's walker process executes
  is not claimed.
- Full-binary scan: 251 semver-like tokens; in 840,000–880,000 only `2.17.2` (856,302) and
  `0.22.10` (856,676, an unrelated string), so no lookalike near the literal.

## Bearing on C2 (freshness, sourced)

The 13-file re-pin can cite in-file: `walker 2.17.2`, `S096` (host rodata literal at binary
offset 856,302 + binary sha256 `2524065…`), and/or `S090` (`/var/log/pacman.log:2929`). The
gate's `live.walker.version` pin move (owned by `GateFreshJj`) is consistent with this row:
the literal is `2.17.2`, and the package version is `2.17.2-1`. Nothing here contradicts
`corpus/knowledge/walker-route-r18.md` § MOVED pins (7,039,912 B, sha `25240650…`, mtime
2026-10-08); this row pins the version literal that note left unfixed.

## Limits

- Did not run walker, pacman, yay, paru, expac, pactree, checkupdates, systemctl, journalctl,
  pidof, or any input/compositor probe; no `/proc` read; no socket connection.
- Did not open/copy `~/.omp/agent/agent.db*`, credentials, or auth files; no omp CLI launch.
- Did not compare against the upstream v2.17.2 tag or source (S072–S078 territory); the
  binary's provenance beyond packaged digest is not claimed.
- Did not read Arch packaging sources or PKGBUILD; patch level `pkgrel 1` is observed, its
  content `[UNK]`.
- Did not verify the old 2.17.0 binary (not present on disk); the 847,791 offset is
  inherited from `corpus/knowledge/walker-deep-r9.md:109`, not re-measured.
- No network source was opened, so no fetch receipt or `receipts.jsonl` line was written.

## Installs

none.
