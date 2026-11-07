# R97MExecCasesC1b — C1 frozen case file v2 report (round 97, w1b)

Seat: R97MExecCasesC1b (leaf executor). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
No tools installed or upgraded (host pacman pause honoured; only `/usr/bin/gio`, stdlib Python,
and the already-fetched round-95/97 control sources used). Nothing committed; no network beyond
`/usr/bin/gio` invocations on the host.

## Files written (owned scope only)

- `.ufo/waves/round-97/controls/filetype-cases-v2.json` (**157 cases**; **sha256
  `fc710b94df67391c392d95aeabd6dfa4c016081019d732f5c373fb990844be20`**; 2,318,009 bytes,
  ASCII-only, sorted keys, `(',',':')` separators, trailing newline)
- `.ufo/waves/round-97/controls/filetype-probe-v2.py` (the oracle builder; re-runnable;
  **sha256 `d7ddd79891ab638b7fa6d445958545e186e4a7fbe28581a52119c2c003012327`**)
- `.ufo/waves/round-97/w1b/R97MExecCasesC1b.md` (this report)

The w1 draft `controls/filetype-cases-r97.json` (sha256 `c5630cd0…`, 140 cases) and its probe
`filetype-probe-r97.py` are **untouched** — v2 is the repaired/complete successor the C1 counter
should freeze against. Scratch `/fast/scratch/hyaku/mado-r97/R97MExecCasesC1b` deleted before yield.

An intermediate 150-case v2 (sha256 `ce56e42c…`) was superseded after the L1 directed three
scored-shape additions once the C1 counter v2 landed its extensions (see below).

## What was wrong with the w1 draft (diagnosed, then fixed)

Running the counter's own `validate_cases` over the w1 draft returned **18 errors**, all in the
database/env contract (Shared contract 3):

1. Host-text-db cases pointed `XDG_DATA_DIRS` at the literal `/usr/share` — forbidden: every
   `:`-segment must start `{root}/`. Fixed by copying the host db tree into `{root}/db/mime/`
   (text and cache presets) or a fully synthetic db, and setting `XDG_DATA_DIRS={root}/db`.
2. `none`-db cases did not declare the env roots as empty dirs, tripping the counter's
   database rule. Fixed by declaring `dh/` and `db/` as empty dirs on every `none` case.

v2 uniformises the env: `HOME={root}/h`, `XDG_DATA_HOME={root}/dh`, `XDG_DATA_DIRS={root}/db` —
except the one multi-db guard case, which uses `XDG_DATA_DIRS={root}/d1:{root}/d2`.

## Oracle

`/usr/bin/gio` sha256 `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`
(matches the L1 freeze receipt). glib2 `2.90.1-1`. Every label produced by
`env -i LC_ALL=C HOME=<root>/h XDG_DATA_HOME=<root>/dh XDG_DATA_DIRS=<root>/db[:..] gio info -a
standard::content-type|standard::fast-content-type [-n] <path>`. The scored path keeps its raw
spelling (trailing slash included); the probe strips it only for filesystem materialisation.

## Case counts (total 157, ≥ 9 per class, ≥ 140 required)

| class | n | class | n | class | n |
|---|---|---|---|---|---|
| dir | 12 | brok | 10 | uncertain | 14 |
| chr | 9 | nofollow | 9 | fast | 10 |
| blk | 10 | follow | 9 | readerr | 13 |
| fifo | 9 | certain | 11 | | |
| sock | 9 | zero | 11 | | |
| empty | 9 | sym | 12 | | |

Label census (18 distinct types incl. ERROR): `text/plain` 51, `inode/symlink` 21,
`application/octet-stream` 20, `inode/directory` 19, `application/x-zerosize` 15,
`inode/fifo` 14, `inode/blockdevice` 12, `inode/chardevice` 12, `inode/socket` 12,
`image/png` 7, `app/x-pngdata` 5, `app/x-foo` 3, `app/x-foo2` 3, `text/html` 3,
`application/x-desktop` 1, `text/x-readme` 1, `app/x-rangehit` 1, `ERROR` 1.

## Verification (exercised)

- `python3 filetype-probe-v2.py --check --scratch <fresh> --out controls/filetype-cases-v2.json`
  → `CHECK_OK: 157 cases, sha256 fc710b94…` — **byte-identical re-run on a fresh scratch tree**.
- Counter **v2** `build/c1-r97-filetype.v2.py` (sha256 `745a341e8a2aaefc7283d1ad4090ebde01d631d118f788ddd1dcc7b5195ba9e0`)
  `validate_cases(data, gio_sha)` over the landed file → **0 errors**.
- `materialise_case` on all 7 new cases: scored-path count == label count; trailing-slash paths
  scored with the raw spelling (`a.txt/`, `link/`, `/dev/null/`); dir-unreadable dirs chmod 000
  last and locked for the caller; `missing` path not created.
- ASCII-only confirmed (`all(b < 128)` over the raw bytes); JSON `sort_keys=True`,
  `separators=(",",":")`, trailing `\n`.
- All 15 classes present in declaration order; every non-ERROR label oracle-produced.

## Extent / guard cases (folded in from R97MMutC1b feedback)

Five `uncertain` cases carry the database-extent and OUT_OF_BOUNDS-guard legs the mutation
tester anchored. All labels are oracle `text/plain` / `app/x-rangehit` as noted:

| id | leg | fixture | oracle |
|---|---|---|---|
| `uncertain-10-text-extent-small` | (a) small-extent text | synth db, matchlet len7 off0 range1 → extent 8; file 20B = 8 text + `\x01`@8 + 11 text | text/plain |
| `uncertain-11-text-extent-range` | (b) range text | synth db, matchlet `\xaa` off0 range_length8 → extent 9; file `ABCDEFG`+`\xaa`+`hijklmn` | app/x-rangehit |
| `uncertain-12-text-extent-clamp` | (d) clamp > 16384 | synth db, matchlet off16385 `\xde\xad\xbe\xef` range1 → extent 16390; file 16399B | text/plain |
| `uncertain-13-cache-extent-small` | (c) small-extent cache | host mime.cache max_extent word patched to 8; same 20B discriminator | text/plain |
| `uncertain-14-cache-guard-badcache` | (e) guard/bad-cache | two-db `d1:d2`: d1 = cache max_extent 8, d2 = cache with `u32@24`=5 (misaligned → OUT_OF_BOUNDS skip); same 20B discriminator | text/plain |

Guard-removal simulation (computed from the landed bytes, not a live mutant): the bad cache's
`u32@24`=5 is misaligned so the correct path skips it; a guard-removal reads `u32@(5+4)=u32@9`
of the host cache header = `9998336` (> 16384) → clamps to 16384 → reads all 20 bytes → sees
`\x01`@8 → `application/octet-stream`. The bad-cache u32 read is in-page (offset 9 of a
207 KB mapping), so no crash-exit-3 risk.

### Key finding that shaped the extent set (from R97MMutC1b, confirmed in code)

The cache sniffer's text fallback checks **only `data[:128]`** (`tools/mado-mimesniff.py:218-221`,
mirroring xdgmimecache.c `mime_type_for_data`). Consequence: a cache-mode `max_extent > 16384`
clamp is **not** discriminable by a control byte at index ≥ 128 — clamp and no-clamp both answer
`text/plain`. The host cache's largest top-level matchlet extent is 4105 (no matchlet beyond
16384), so no host-cache magic matchlet can discriminate a cache clamp either. I therefore did
**not** ship a cache-clamp-text-fallback case (it would be a non-discriminating decoy); the
clamp > 16384 leg is carried by `uncertain-12` (text-mode magic matchlet, immune to the 128-byte
cap), and the cache extent mechanism is covered by `uncertain-13` (small extent) +
`uncertain-14` (guard). I replied to `R97MMutC1b` with the final sha256 and these five ids.

## L1-directed additions (added once counter v2 landed its extensions)

The L1 (MadoR97) directed three scored shapes; the C1 counter v2
(`c1-r97-filetype.v2.py`) landed support for trailing-slash stripping, the `dir-unreadable`
path type, and the `missing` path type, after which these 7 cases were added (150 → 157):

| id | class | shape | labels (oracle) |
|---|---|---|---|
| `dir-11-trailing-slash-file` | dir | `a.txt/` (file, trailing slash) | text/plain |
| `dir-12-trailing-slash-chardev` | dir | `/dev/null/` (chardev, trailing slash) | inode/chardevice |
| `sym-11-trailing-slash-link-nofollow` | sym | `link/` → `a.txt`, nofollow | inode/symlink |
| `sym-12-trailing-slash-link-follow` | sym | `link/` → `a.txt`, follow | text/plain |
| `readerr-11-dir-unreadable` | readerr | text file under chmod-000 dir, NONE db, full | [inode/directory, application/octet-stream] |
| `readerr-12-dir-unreadable-named` | readerr | same locked parent, synth db (`*.txt`→text/plain), fast | [inode/directory, text/plain] |
| `readerr-13-missing` | readerr | `nope.txt` listed in paths, never materialised | [ERROR] |

Notes on these:

- **Trailing slash**: the case schema's `path` field keeps the slash (`a.txt/`, `link/`,
  `/dev/null/`); the counter v2 strips it for filesystem operations but scores the raw spelling
  against the tool and gio. Labels verified with gio: `a.txt/`→text/plain, `link/` nofollow→
  inode/symlink, `link/` follow→text/plain, `/dev/null/`→inode/chardevice.
- **dir-unreadable**: the directory is created with its children first, then chmod 000 last; the
  probe's `finally` restores it to **0o755** (not 0o644 — R97MCritic C1-11: 0o644 on a dir clears
  the x bit and wedges cleanup). With a NONE db the full attr gives `application/octet-stream`
  (EACCES-tolerant stat; content sniff fails and there is no name fallback). The "typed name
  variant text/plain" is achievable only as a separate synth-db fast-attr case (`readerr-12`),
  because a synth db's globs map `*.txt`→text/plain; under a NONE db the fast attr is also
  octet-stream (no name table), and with a synth db the FULL attr also falls back to text/plain.
- **missing**: a path listed in `paths` but never materialised; gio exits 2 with no attribute, so
  the label is `ERROR` and the tool's `MADO_FILETYPE: ERROR stat` + exit-2 branch is scored
  (R97MCritic C1-9).
- **brok loop symlinks** (brok-03/04/05/10) remain `inode/symlink` (L1 requirement (c), no change).

## Risks and blockers

- **128-byte text cap is load-bearing.** Any future extent fixture that relies on a control byte
  at index ≥ 128 to discriminate will silently not discriminate. The small-extent cases place the
  control byte at index 8 (extent 8, < 128) specifically to stay inside the scanned window.
- **Host-device dependence.** `chr`/`blk` cases score `/dev/ttyS0`, `/dev/ttyS1`, `/dev/nvme1n1`
  (and siblings). If the host device set changes, those labels change and `--check` would diverge;
  the probe does not freeze-check device existence (matching the counter's freeze-time check).
- **Cache db size.** The cache-mode cases embed the ~207 KB host `mime.cache` (base64), plus the
  two-cache guard case; this is why the file is ~2.3 MB. Text-mode and synthetic dbs are small.
- **Guard leg is reasoned, not mutant-run.** `uncertain-14`'s discrimination is verified by
  computing the cache-header bytes (documented above), not by executing a guard-removal mutant;
  that is the mutation tester's leg. The oracle label itself is `text/plain` (exercised).
- **Counter v2 is the validation target.** The landed file validates against
  `c1-r97-filetype.v2.py` (sha `745a341e…`), not the original `c1-r97-filetype.py` (sha
  `6536b0ae…`), which lacks the trailing-slash / dir-unreadable / missing extensions.

## Checks for the main agent

- `python3 .ufo/waves/round-97/controls/filetype-probe-v2.py --check` → `CHECK_OK … 157 cases,
  sha256 fc710b94df67391c392d95aeabd6dfa4c016081019d732f5c373fb990844be20`.
- Counter v2: import `build/c1-r97-filetype.v2.py`, `validate_cases(json.load(open(
  'controls/filetype-cases-v2.json')), '<gio_sha>')` → `[]`.
- Freeze target is `controls/filetype-cases-v2.json` (sha256 `fc710b94…`, 157 cases), paired with
  counter `c1-r97-filetype.v2.py` (sha256 `745a341e…`).
