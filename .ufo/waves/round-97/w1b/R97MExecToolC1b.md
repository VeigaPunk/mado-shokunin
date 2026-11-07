# R97MExecToolC1b — mado-filetype v2 (extent fix + EACCES + trim/normalisation + F5/F6 quality) report

## Files changed
- `.ufo/waves/round-97/build/mado-filetype.v2.py` (FINAL; sha256
  `da6af7a0789265187f6b2c2462bf5104a7c0b780baed3235300f89978a44d2d8`, 606 lines, 29646 bytes, ASCII)
- `.ufo/waves/round-97/w1b/R97MExecToolC1b.md` (this report)

No other file written. Base draft `build/mado-filetype.py` (sha256 `e68150b5…`) untouched. Scratch deleted before
yield. No tools installed; no pacman transaction; no network beyond the pre-fetched round-95/97 sources.
Intermediate pins, all superseded: `6454d3dbdb01…` (extent only) → `e0086e3f74c7…` (+EACCES/trim) → FINAL
`da6af7a07892…` (+F5/F6/F3, socket import removed).

## The production changes vs the base draft
1. **Database extent (contract 2)** — sniff length is the database's own, not the 16384 constant:
   `_cache_max_extents` (xdgmimecache.c:726-748: BE header word 24 = magic section offset,
   `OUT_OF_BOUNDS(offset,1,8,size)` guard, max over loaded caches of the u32 at offset+4) and `_text_max_extents`
   (xdgmimemagic.c:701-721: max `value_length+offset+range_length` over kept sections' flat matchlet chains),
   dispatched in `FileType.__init__` on `mode == "cache"` mirroring the C's `if (_caches)`; none mode arrives as
   the text sniffer with empty kept sections → 0 → clamp 16384. `_clamp` caps at `SNIFF_CAP` (the
   `guchar sniff_buffer[16384]` of glocalfileinfo.c:1349). `answer()`'s read site is byte-identical to v1.
2. **EACCES tolerance** — `_stat_branch`: `lstat` failure with `errno == EACCES` returns None (glocalfileinfo.c
   :1937-1951; get_content_type guards every stat branch with `statbuf != NULL`, :1309-1331, so all branches
   skip and the name-only guess + a failed open answer); any other errno raises → `ERROR stat`, exit 2.
   Follow failures stay `inode/symlink` (the C's `symlink_broken`).
3. **CLI path normalisation** — `_norm(path) = posixpath.normpath(path).rstrip("/") or "/"` applied first in
   `answer()`: the gio CLI trims trailing '/' (L1-measured) and GFile folds duplicate slashes, './' and
   'x/../y' (re-measured: `orac//a.txt`, `orac/./a.txt`, `orac/adir/../a.txt` all text/plain on both sides);
   `/` stays and `//` folds to it. Printed `path=` keeps the raw argument.
4. **Output order (F6)** — `main` appends ERROR entries into `results` in place and prints ONE line per path in
   argv order; a refused path keeps its contract form `MADO_FILETYPE: ERROR stat path=<escaped>` (no
   attr/mode fields); `--json` includes every path, refused ones as `{"path", "type": "ERROR"}`; exit 2 kept
   when any path errored.

Everything else of the production path (stat branch order, `_read_sniff`, `_guess`, the guess/gate body, CLI
flags, exit codes) is byte-identical to v1.

## Selftest — `MADO_FILETYPE_SELFTEST: checks=40 failed=0` rc 0 (sibling layout / landed bytes); 38 on a truly lone copy
Lone copies skip the sibling-dependent checks (`_load_mimeglob()` raising SystemExit marks them skipped) so
`--selftest` stays runnable without the siblings; the landed `tools/` layout — what the counter pins — runs all
40. The five weak checks are now real predicates:
- **f08** was a TUPLE `(a, b)` (always truthy) → now `t[0] == "image/png" and t[1] == 0` (exact type AND zero
  sniffer calls).
- **f13** accepted either outcome → now exact: the subclass walk returns the FIRST name type that subclasses the
  sniffed one, `== "app/child"` (deterministic in the fake: table order + first-hit walk).
- **f17** was `(... ) if False else True` in v1 — already reworked in the EACCES pass; it is the real lstat-level
  ENOTDIR unit (`_raises(txt + "/")` against `_stat_branch`, the library behavior the CLI trim hides).
- **f21** was the constant `chr(0) == "\x00"` → now the exact esc predicate
  `_esc(b"a\x01b") == "a\\x01b" and _esc(b"ok") == "ok"` (esc loads the sibling, so it is sibling-gated like
  f40/f41; `esc` is `chr(c) if 33 <= c < 127 and c != 92 else \xNN` — a wrong esc fails it).
- **f24** accepted either outcome → now exact `== "text/plain"` (a certain name never sniffs).
New legs:
- **f33** EACCES via a mode-000 parent dir: answer `application/octet-stream` (name-only + failed open) AND
  `_stat_branch(...) is None`; modes restored before cleanup.
- **f34-f36** trim: `f.txt/` → text/plain; `dir/` → inode/directory; `link/` follows → image/png, nofollow →
  inode/symlink. **f37** root cases. **f38** GFile normalisation: `_norm("a//b") == "a/b"`, `./a`, `a/../b`, plus
  end-to-end `root/a/./f.txt` and `root//a/f.txt` → text/plain.
- **f40/f41** (sibling-gated, per the L1's run(argv) request): `main()` called in-process under a captured
  stdout — f40 over `[dir, missing, fifo, zerosize]` asserts rc 2, the four exact output lines in argv order with
  the ERROR line in place, then the `MADO_FILETYPE_DIRS:` line; f41 over `[missing]` asserts rc 2, exactly the
  `MADO_FILETYPE: ERROR stat path=<escaped>` line then the dirs line.
- The socket fixture no longer imports anything: `os.mknod(sock, stat.S_IFSOCK | 0o600)` (works as this user,
  f03 green). The candidate now contains **zero** `socket`, `subprocess` or `ctypes` tokens; imports are
  argparse, errno, importlib.util, json, os, posixpath, stat, sys + selftest-local struct/tempfile/contextlib/io.

## Host database measurements (shared-mime-info 2.5.1-2)
Reachable mode cache (2 caches); per-cache extent words 0 and 18730; **cache extent 18730 → clamp 16384**; the
independently parsed text extent is also **18730** (689 kept sections, 1743 matchlets). Real-db end-to-end
differential (custom cache, extent word 4 vs 16384, probe `xxxxHI`): the answer flips `text/plain` ↔ `app/hi`;
none-db (`--data-home <empty> --data-dirs ""`) answers `db=none` rc 0.

## Oracle agreement (`env -i LC_ALL=C HOME=… XDG_DATA_DIRS=/usr/share /usr/bin/gio info -a standard::content-type`)
| case | gio | v2 tool |
|---|---|---|
| 000-dir file, typed name | text/plain rc 0 | text/plain rc 0 |
| 000-dir file, untyped name | application/octet-stream (L1) | application/octet-stream rc 0 |
| `a.txt/`, `adir/`, `lnk/` (follow), `lnk/ -n`, `/dev/null/` | text/plain / inode/directory / text/plain / inode/symlink / inode/chardevice | identical, rc 0 |
| `orac//a.txt`, `orac/./a.txt`, `orac/adir/../a.txt` | text/plain | text/plain |
| missing path | rc 2, no attribute | `ERROR stat` rc 2 |
| `/dev/nvme1n1`, symlink loop, dangling | blockdevice / inode/symlink rc 0 / inode/symlink | identical |

## Structural facts for the counter/audit authors
- Exactly **one** `spec_from_file_location` (`_load_sibling`); imports: argparse, errno, importlib.util, json,
  os, posixpath, stat, sys (+ selftest-local struct, tempfile, contextlib, io). **No socket, subprocess or
  ctypes token anywhere in the file** (the AF_UNIX fixture is `os.mknod(..., S_IFSOCK)`).
- **Allowlist (direct sibling-module attributes) — unchanged**: mg.{Resolver, g_path_get_basename,
  xdgmime_dirs, esc, _libc (only .setlocale), _LC_ALL}, ms.{Sniffer}, mt.{Sniffer}. Object-attribute reads
  (outside a direct-attr allowlist): `sniffer.caches`, `sniffer.matches` (read-only, FileType.__init__).
  Own-module additions: `SNIFF_CAP` (name kept), `_cache_max_extents`, `_text_max_extents`, `_norm`.
- Mutant-seat separability (5 statements, all non-selftest, byte-stable since the intermediate pin): cache word
  read, OUT_OF_BOUNDS guard, text accumulation, cache-vs-text dispatch, clamp + call site. The F5/F6/F3 pass
  touched none of them.
- Selftest transcript: landed `checks=40 failed=0`; lone `checks=38 failed=0` (the sibling-gated f21/f40/f41 are
  constant-skip on a lone copy — noted so the counter's N bound is measured in the landed layout, where N=40).

## Risks and blockers
- `_norm` models the gio CLI + GFile argument handling; a leg that bypasses the CLI (raw library call semantics)
  would disagree on unnormalised spellings — frozen case labels must be CLI-measured (they are).
- EACCES legs are meaningful only non-root (root ignores the 000 mode); the counter harness must not run the
  tool as root for that leg.
- C `int` overflow of `value_length + offset + range_length` is UB upstream, computed exactly here (declared
  limits).

## Checks for the main agent
- `python3 tools/mado-filetype.v2.py --selftest` → `MADO_FILETYPE_SELFTEST: checks=40 failed=0`, rc 0.
- `python3 tools/mado-filetype.v2.py /etc/hosts /nonexistent-xyz /tmp --data-dirs /usr/share
  --data-home-unset --home-unset` → three lines in argv order (`text/plain`, `ERROR stat` in place,
  `inode/directory`), rc 2; with `--json` the ERROR entry appears as `{"path": "/nonexistent-xyz",
  "type": "ERROR"}`.
- sha256 of the landed candidate == `da6af7a0789265187f6b2c2462bf5104a7c0b780baed3235300f89978a44d2d8`.

## Report
Report: .ufo/waves/round-97/w1b/R97MExecToolC1b.md
