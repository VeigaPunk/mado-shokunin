# R97MExecToolC1 — mado-filetype candidate report

## Files changed
- `.ufo/waves/round-97/build/mado-filetype.py` (new; the C1 candidate draft)
- `.ufo/waves/round-97/w1/R97MExecToolC1.md` (this report; Report trailer: `.ufo/waves/round-97/w1/R97MExecToolC1.md`)

No other files written. Scratch deleted before yield (`/fast/scratch/hyaku/mado-r97/R97MExecToolC1`; tooling already installed: `python3`, `gio`).

## Behavior
Implements Shared contract 1 / declaration rules 1-7:
- Stat branches first, in C order: `os.lstat` (symlink -> broken-target or `--nofollow` -> `inode/symlink`, ELOOP loop -> `inode/symlink` per gio oracle; live target follows to its own type), dir -> `inode/directory`, chr -> `inode/chardevice`, blk -> `inode/blockdevice`, fifo -> `inode/fifo`, regular size 0 -> `application/x-zerosize`, socket -> `inode/socket`.
- Name-only guess on `basename` via the sibling `mado-mimeglob` (`Resolver.guess`), then the gated sniff (`--fast` never sniffs; sniff only when `uncertain`), sniff length `_clamp(max_buffer_extents)` with `max_buffer_extents = 16384` (mutex oracle-measured clamp of the absent/0 extents), `os.open(O_RDONLY|O_CLOEXEC)` read at most the clamp; an open/read failure keeps the name-only answer.
- Database mode from `mg.Resolver(dirs).mode`; sniffers `ms.Sniffer` (cache) / `mt.Sniffer` (text, resolver injected), loaded by exactly one pinned `spec_from_file_location` each (`_load_sibling`), limited to default construction and `.guess` — no other sibling attributes touched. Lone-copy safe: `--selftest` never reaches any sibling load.
- Output: `MADO_FILETYPE: <type> attr=<full|fast> mode=<follow|nofollow> path=<escaped>` per path + `MADO_FILETYPE_DIRS: db=<cache|text|none>`; unstat'able path prints `MADO_FILETYPE: ERROR stat path=<escaped>` and exits 2 (other paths kept); `--json` prints `{db, attr, mode, results:[{path, type}]}`.
- ASCII only, stdlib only.

## Exact retained evidence
- `sha256sum` of the frozen draft: `e492c46d6afa947f7e2beaa1991604a12bc4165eb3370e61dd5fa9c97b41033b` (re-verified after the final `python3` run; `grep -c spec_from_file_location` = 1, all three siblings via the single helper).
- Selftest transcript (`python3 mado-filetype.py --selftest`, run from a `tools/`-layout scratch copy so sibling paths resolve, and also as a lone copy):
  `MADO_FILETYPE_SELFTEST: checks=25 failed=0` (exit 0). Checks cover branch order, follow/nofollow, broken/loop symlink, fast vs full, one-type-never-sniffs, no-type-sniffs, several-types, clamp (0/>16384/small), read-error, stat-error exit 2, output escaping.
- Oracle comparison (read-only `gio info`, `env -i` sets; glib2 2.90.1 host): branch agreement on `/dev/null` (`inode/chardevice`), directory, fifo, zerosize, broken-symlink (`inode/symlink`), symlink loop (rc 0, `inode/symlink`), missing (rc 2); sniff-length probe at offset 16380/16383 shows the effective sniff length is 16384 (mutex-measured).
- Smoke run (scratch copy next to the three siblings, `--data-dirs /usr/share`):
  `MADO_FILETYPE: text/plain attr=full mode=follow path=/etc/hosts`, `inode/chardevice` for `/dev/null`, `inode/directory` for `/tmp`, `MADO_FILETYPE_DIRS: db=cache`, rc 0; `/nonexistent123` prints `MADO_FILETYPE: ERROR stat path=/nonexistent123` with rc 2 and `text/plain` for the valid sibling path preserved.

## Risks and blockers
- The tool resolves the three siblings from its own directory, read at `tools/` in final layout; the frozen counter must copy `tools/` alongside the candidate (does).
- Symlink-loop wording differs from the declaration sentence ("missing, or a symlink loop" -> `ERROR stat`): the gio oracle prints `inode/symlink` rc 0 for a loop; frozen cases must carry the oracle label, not the declaration sentence (L1).
- `max_buffer_extents` is fixed at 16384 (the measured clamp for an absent/0 extents report); a database that reports a smaller positive extents is unmeasured this wave.
- `O_READERROR` fixtures (unreadable files) stay root-readable in this harness; the read-failure-keeps-name-only path is covered by the selftest's fake-sniffer leg, not by a live unreadable file.

## Checks for the main agent
- Re-run `python3 tools/mado-filetype.py --selftest` at the landed revision (expect `checks=25 failed=0`).
- Re-run the smoke command above against `/usr/share` (cache mode) and an empty data dir (mode `none`, `application/octet-stream` for binary data).

## Report
Report: .ufo/waves/round-97/w1/R97MExecToolC1.md
