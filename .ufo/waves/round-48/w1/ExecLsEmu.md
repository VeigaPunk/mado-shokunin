# ExecLsEmu — byte-exact `LC_ALL=C LANG=C ls -LRl` emulation (the hard core of C1)

Seat: `ExecLsEmu` · round 48 / wave w1 (BUILD) · lane `mado-shokunin` · base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`
Claim fed: **C1** (operability) — the warm-cache path of `tools/mado-terminal.py` needs the exact byte stream that
`xdg-terminal-exec` v0.14.3 feeds to md5 in `gen_hash` (`/usr/bin/xdg-terminal-exec:179-215`). This seat supplies that
stream without starting a process.

## 1. Deliverables

| path | what | sha256 |
|---|---|---|
| `.ufo/waves/round-48/w1/ExecLsEmu/lsemu.py` (589 lines) | the emulator | `8aaab3dc1fc32e118bb7e7030d9fda4dc40be1389ba3245b575d595347a937d4` |
| `.ufo/waves/round-48/w1/ExecLsEmu/fuzz.py` (624 lines) | differential fuzzer, host + bwrap | `18eb8a4203f1e39cc30ce27241471e13c4e31cbbd579cb10829b03432b75e953` |
| `.ufo/waves/round-48/w1/ExecLsEmu/receipts/fuzz.txt` | 15 000-tree campaign | — |
| `.ufo/waves/round-48/w1/ExecLsEmu/receipts/real-tree.txt` | real system directories, incl. 361 788 lines | — |
| `.ufo/waves/round-48/w1/ExecLsEmu/receipts/contract-edges.txt` | evidence for every out-of-contract class | — |
| `.ufo/waves/round-48/w1/ExecLsEmu/receipts/static.txt` | imports, no process/socket/write, compile, hashes | — |

API (exactly what the C1 tool needs):

```python
ls_lRL(operands, now=None, cwd=None) -> bytes              # stdout only: the gen_hash input
ls_lRL_full(operands, now=None, cwd=None) -> (stdout, stderr, rc)
```

`operands` may be `str` or `bytes`; `cwd` is the base for relative operands (default: process cwd); `now` models ls's
clock (see §3, dates). Imports are `errno`, `os`, `stat`, `time` only (`pwd`/`grp` lazily for the two name lookups);
there is no `subprocess`, no `socket`, and no write path — verified by grep in `receipts/static.txt`.

## 2. Method: source first, fuzz second

The implementation was **derived from the source of the binary that runs on this host**, not reverse-engineered from
output:

* `/usr/bin/ls` — `ls (GNU coreutils) 9.12`, sha256 `29abfee0d588cfbee70103be11aa0a2f81b0d8c1292341e2345fc9f3ffa1558b`
  (`coreutils 9.12-2`; note the PATH `ls` on this host is a shell wrapper reporting `0.8.0` — the fuzzer pins `/usr/bin/ls`);
* source: `https://ftp.gnu.org/gnu/coreutils/coreutils-9.12.tar.xz`, 6 704 996 bytes,
  sha256 `a480198559733e9b3da999e90543ac6f888a2caa544d8d664c5a1f17e528e210`; extracted `src/ls.c` sha256
  `936768065464ccc85b3084594ea2bca5b0cbc3786bcf5e7ca26ffbe93a0d1e4d`, plus `lib/filemode.c`, `lib/file-has-acl.c`,
  `lib/human.c`, `lib/quotearg.c`, `lib/cycle-check.c`.

The tarball lives only in scratch (deleted); it is a source reference, not an install.

Every rule below was read in that source and then *checked* by differential fuzzing — the fuzzer never defined the
model, it only falsified it.

## 3. Rule map (behaviour → source location → how it was checked)

| behaviour | source | check |
|---|---|---|
| operands: files first then dirs, both sorted by `strcoll` (= byte order in C), dirs queued LIFO so they print in sorted order | `ls.c:1757-1795`, `extract_dirs_from_files` 3707 | fuzz `operand-order`, `file-then-dir-widths`; 507 `missing-operand` cases |
| a blank line precedes every directory header except the very first thing printed, and one blank line separates the file block from the first header | `ls.c:1787-1795`, `print_dir` 2996-3005 (`first`) | all multi-block cases |
| header path = `attach(dirname,name)` (drops a dirname of exactly `"."`), recursion path = `file_name_concat` (keeps `./`) | `ls.c:5271` | `dot-operand`, `dot-slash-operand`, `./` headers with `..`-links |
| `total` = **floor**(Σ `st_blocks` / 2) — `human_readable(n, opts=0, 512, 1024)` takes the integer path and never rounds up | `ls.c:3092-3105`, `lib/human.c:154-330` | totals on every case; `contract-edges.txt §9` |
| hidden entries (leading `.`) excluded from block **and** from `total` | `ls.c` `file_ignored`, `gobble_file` | `hidden` cases, hidden-only dir |
| column widths per block: `nlink` right-justified; owner/group **names left-justified with `width-len+1` spaces**, numeric ids and `?` go through the same name path; size right-justified; devices print `%*ju, %*ju` with `file_size_width` = max(len(size), major+2+minor) | `ls.c:3570-3648` (accumulation), `print_long_format` 4336-4400, `format_user_or_group` 4187-4225 | `two-digit-nlink`, `devices:/dtmp` (major 10, minor 237 next to a 7-byte file), numeric-uid sandbox |
| the **file-operand block's widths include the directory operands** (accumulators are filled before `extract_dirs_from_files` removes them) | `gobble_file` + `extract_dirs_from_files` | `file-then-dir-widths` |
| mode string from `strmode`, 11 bytes with a trailing space; the 11th byte is `' '` for an ACL-free file, `'+'` for an ACL, `'.'` for an LSM context only, `'?'` if undeterminable, and the whole column is **truncated to 10 bytes when no entry in the block has an ACL** | `lib/filemode.c:85` (`strmode`), `ls.c:4286-4300` | `special-mode` (1 643 cases), `acl` (56), mixed blocks |
| `+` means "the xattr exists": `system.posix_acl_access`, or `system.posix_acl_default` for a directory; `security.selinux` present without an ACL means `'.'` | `lib/file-has-acl.c` (Linux `USE_LINUX_XATTR` path) | `acl` tag; trivial-ACL probe (`setfacl` base-only → kernel drops the xattr → no `+`, model agrees) |
| a dangling symlink under `-L` is kept as `l` + 9 `?` (10 `?` when the block has an ACL, because the ACL byte is still `'?'`), produces a **minor** diagnostic (rc 1), and is never counted for widths or `total` (early return before the width code) | `ls.c:3432-3472` | `dangling` (185 cases), `dangling-operand`, `l??????????` blocks |
| dates: `%b %e  %Y` when old, `%b %e %H:%M` when recent; recent ⟺ `now-15778476 < mtime < now` (both strict, `31556952/2`); unknown date = `'?'` right-justified in `long_time_expected_width()` (12 in C locale, computed from epoch 0) | `ls.c:4420-4440`, `long_time_expected_width` 4151 | `recent`/`old-time`/`future`/`epoch`/`absolute-time` (≈4 900 cases) |
| recursion + loop detection: every printed directory joins an active set; a child whose `(dev,ino)` is already active prints `ls: <path>: not listing already-listed directory` to stderr, sets rc 2 and gets **no** header; the set entry is dropped after the subtree (so a legitimate sibling target is listed twice) | `print_dir` 2964-2992, `visit_dir` 1449-1475, markers in `extract_dirs_from_files` 3712-3720 + main 1792-1820 | 209 `loop` cases, `link-sibling`, `duplicate-operand`, `symlink-dir-operand` |
| errors are emitted in **readdir order**; the block itself is sorted | `print_dir` loop 3033-3045 | stderr comparisons in every case |
| names: the non-tty default is literal quoting with `qmark_funny_chars=false`, so the only transformation is `'\n' → '?'` | `ls.c:2337-2345`, `quote_name_buf` 4480-4540 | control bytes, tab, 0x7f, invalid UTF-8, 255-byte names |
| stderr quoting: `quoteaf` (always) for `cannot access/…`, `quotef` (colon-marked shell_escape) for the loop message; apostrophe switches to C quotes when every byte is C *and* shell compatible | `lib/quotearg.c:290-780` | 4 quoting defects found and fixed by the fuzzer |
| exit status: 2 for operand/dir/loop failures, 1 for a failed stat inside a directory, 0 otherwise | `set_exit_status` 2902, `file_failure` 2915 | rc compared on all 15 000 cases |

## 4. Verification (measured)

**Random trees** — `receipts/fuzz.txt`, seeds 1/2/3, 2 500 trees each in each environment (seed+100 000 for bwrap):

| environment | trees | mismatches (stdout, stderr, rc) |
|---|---|---|
| host (owner names) | 7 500 | **0** |
| bwrap user namespace, no `/etc` (numeric ids) | 7 500 | **0** |

plus 17 hand-built cases per host run and 19 per sandbox run (option-parsing excluded; devices; unreadable dir;
two-digit nlink; forty entries; every operand shape). Reproducible: seed 5 run twice produced identical receipts.

**Real content** — `receipts/real-tree.txt`: `/usr/share/applications` (123 lines), `/usr/lib/xkbcommon` (14),
and `/usr/share` (**361 788 lines, 22.7 MB**) are byte-identical including stderr and exit status (rc 1 on `/usr/share`,
a dangling entry). Cost: 3.2 ms vs ls 1.5 ms on `/usr/share/applications`; 4.95 s vs 2.37 s on `/usr/share` — about
2× C ls, which is irrelevant for the resolver's config/app directories.

**Sandbox mode really has no `/etc`** — printed into the receipt (`/etc/passwd present=False`), and owner/group
columns are numeric (`1000`), which is exactly what `xdg-terminal-exec`'s `gen_hash` sandbox sees.

Reproduce:

```sh
cd .ufo/waves/round-48/w1/ExecLsEmu
TMPDIR=/fast/scratch/hyaku/mado-r48/ExecLsEmu python3 fuzz.py \
  --cases 2500 --seed 1 --mode both --out receipts/fuzz.txt
```

## 5. Edge classes — exactly emulated, or declared out of contract

### Emulated exactly (byte-identical stdout, stderr and exit status)

| class | evidence |
|---|---|
| operand order: non-existent dropped with stderr, files sorted first, then each directory block with `name:` header, `total N`, blank lines between blocks | 507 `missing-operand`, all multi-operand cases |
| `total` in 1 KiB units (floor of Σ`st_blocks`/2), directories contribute 0 on xfs, hidden entries never counted, dangling entries contribute 0 | every block; `contract-edges.txt §9` |
| per-block alignment of `nlink`, owner, group, size; names left-justified vs numeric ids right-justified; `?` fields; 1–2 digit nlink; 7-digit sizes | `two-digit-nlink`, `forty-entries`, numeric-uid sandbox, `big-size` (1 430 cases) |
| devices: `major, minor` with per-column widths and the shared size-column width (major 10 / minor 237 beside a 7-byte regular file) | `devices:/dtmp` |
| mode strings incl. `s/S/t/T`, fifo `p`, socket `s`, dir `d`, symlink `l`, ACL `+`, and the 10-vs-11-byte column depending on `any_has_acl` | `special-mode`, `acl`, mixed blocks |
| `-L` following: symlink→file (target mode/size, no arrow), symlink→dir (a separate block), dangling (`l?????????` + minor rc), chains, `ELOOP`, ancestor loops with the exact message and rc 2, legitimate sibling targets listed twice | 209 `loop`, 185 `dangling`, 1 386 `symlink`, `link-chain`, `symlink-dir-operand` |
| dates: both formats, recent/old/future mtimes, epoch 0 and pre-1970, the 6-month rule from source (fuzz keeps ±2 h away from the boundary) | ≈4 900 time-tagged cases |
| names: spaces, tabs, `\n`→`?`, control bytes, `0x7f`, invalid UTF-8 bytes emitted raw, 255-byte names, `C`-locale ordering (`Caps` < `alpha`) | name pool in every run; `contract-edges.txt §11` |
| empty dirs, hidden-only dirs, unreadable dir (`cannot open directory`, rc 2, no header), `-R` into unreadable children | `empty-dir`, `hidden-only`, `unreadable-dir`, `unreadable-then-readable` |
| stderr text and ordering (including gnulib shell/C quoting and readdir order) | compared on all 15 000 cases |

### Declared out of contract (with the measured evidence)

| class | why declared, and evidence |
|---|---|
| operands beginning with `-` | `ls` parses them as **options** (`-dash` = `-d -a -s -h`), not as paths — `contract-edges.txt §10`. The resolver only ever passes path operands; the fuzzer excludes such names as operands but keeps them as entries (where they are handled exactly). |
| `POSIXLY_CORRECT`, `BLOCK_SIZE`, `LS_BLOCK_SIZE` | change `total` (512-byte units / scaled) — `§2-4`. The model implements the default (1 KiB, floor). |
| `TIME_STYLE` | changes the date column — `§5`. Model: the two default formats. |
| `QUOTING_STYLE` | changes **stdout name bytes**, i.e. the hash input — `§6`. Model: the non-tty default (literal + `\n`→`?`). |
| `COLUMNS` | verified to have **no** effect on `-l` — `§7`. |
| `TZ` | the model follows the process `TZ` exactly like `ls`; caller must not mix (a mismatch is a caller error, visible as a diff in the time column). |
| mtime years outside 1000…9999, `--dired`, `LS_MULTI_COL`/`LS_LONG_FORMAT` modes | not reachable from `ls -LRl`; not modelled. |
| odd `st_blocks` sums (`total` rounding) | the floor rule comes from `lib/human.c` (inexact style 0). On this filesystem every `st_blocks` is 0 or a multiple of 8 (`§9`), so the rounding is **not observable** here; if a future filesystem reports 512-byte granularity, re-run `fuzz.py` there. |
| ACL "triviality" | the model, like coreutils' Linux path, tests xattr **presence**; a normal `setfacl` to base-only makes the kernel drop the xattr, and both sides then print no `+` (probed). A hand-crafted present-but-base-only ACL would show `+` on both sides, so this is not a divergence. |

## 6. Notes for the C1 tool and the L1 freeze

* The md5 input is **stdout only**; stderr is dropped by `gen_hash`'s `2>/dev/null`. `ls_lRL` returns exactly that.
* `ls_lRL` starts no process, opens no socket and writes nothing — it only `stat`s, lists directories and reads
  xattrs, so it is compatible with the tool's "never launch anything" contract and with the read-only seat rules.
* Cost ~2× C `ls`; for the resolver's directories (tens to hundreds of entries) this is single-digit milliseconds.
* The model honours the *default* environment. Because `xdg-terminal-exec` inherits the caller's environment for its
  `env LC_ALL=C LANG=C ls -LRl` call (`§2-7` show `POSIXLY_CORRECT`, `*BLOCK_SIZE`, `TIME_STYLE`, `QUOTING_STYLE` all
  change the byte stream), the cache's validity is environment-sensitive: worth stating in the C1 contract that the
  tool models the default environment, and worth a lesson line later.
* `now` is the model's clock; for a file whose mtime equals `now` exactly, GNU prints the year form (recent requires
  `mtime < current_time`). Pass the wall clock observed at the same time as the real `ls` run would see it.

## 7. Risks and blockers

No blockers.

* **Clock boundary**: an mtime in the same second as `ls`'s clock is inherently racy to reproduce; the formula is taken
  from source and the fuzzer keeps every generated mtime ≥ 120 s away from both boundaries. Real configuration trees
  have stable mtimestamps, so this is a theoretical edge.
* **Version drift**: the rules are pinned to coreutils 9.12. A host upgrade of `ls` invalidates them; `fuzz.py` is the
  regression test (it prints the `ls` version and hash at the top of every receipt).
* **Filesystem dependence**: `total`, `st_blocks` and directory sizes come from the filesystem; both sides read the
  same one, so this is modelled from syscall data rather than from a formula.
* **Session material**: none collected. Receipts contain scratch paths, synthetic names, and three system directories
  (`/usr/share/...`); no home listings, window titles, monitor or input-device data.

## 8. Tooling / scratch

No package was installed, no pacman transaction, no host or compositor mutation. One download (coreutils 9.12 tarball,
sha256 above) into scratch to read the source. All fixtures and work dirs lived under
`/fast/scratch/hyaku/mado-r48/ExecLsEmu/` and were deleted at the end; receipts were copied into the seat directory
first.
