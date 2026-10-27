# ExecRefCacheB — C1 reference B: an independent warm-cache implementation (round 48, w1 BUILD)

Seat: `.ufo/waves/round-48/w1/ExecRefCacheB/` · lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`
(round base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`; the lane tip I read was `5ff167423ee410251da0ef0c82f8e6fa25875665`).
Nothing frozen by this seat; nothing outside the seat dir and this report was written; no git/jj mutation in the lane; no
tool installed; scratch `/fast/scratch/hyaku/mado-r48/ExecRefCacheB/` deleted at the end.

## 0. What is delivered

| file | bytes | sha256 | what it is |
|---|---|---|---|
| `ExecRefCacheB/warmcache.py` | 17549 | `b36b8e8ed02b75526e5766269ed9974e0a5ef7b70ebfabe122cca6942aaae943` | the standalone module: `ls_lRL()`, `gen_hash()`, `read_cache()` |
| `ExecRefCacheB/mado-terminal.py` | 76996 | `1fd09ac284986b5964b07ae41da5837cbb6413ec1e51496db08c029f4d3bf255` | the patched tool: base + the warm-cache block inlined verbatim + 25 new selftest cases |
| `ExecRefCacheB/patch_tool.py` | — | — | the mechanical patcher that produced it (asserts every anchor occurs once) |
| `ExecRefCacheB/harness_{ls,shapes,hash,warm}.py`, `probe_pin{,2}.py`, `run_{sandbox,shapes,hash,warm,probe}.sh` | — | — | the verifiers behind the five receipts, re-runnable as written |
| `ExecRefCacheB/receipts/{hash-agree,ls-diff,pin-probes,warm-fixtures,r47-counter,inline-identical}.txt`, `tool-diff.txt` | — | — | evidence |

Base read unmodified: `tools/mado-terminal.py` sha256 `b84d5c4f723049c0fd14189ffc7b6db1f71eb70fb97e0c476d20ddeca6de2222` (49839 bytes).
The patched tool is that file with **14 hunks, +587 −32 lines, 1046 lines unchanged** (`receipts/tool-diff.txt`), and its
warm-cache block is `warmcache.py` from `# xdg-terminal-exec constants` to EOF, byte for byte
(`receipts/inline-identical.txt`: both sides 11544 bytes, sha256 `257f59ba…`, `identical=True`).

Contract of the new tool (the L1 freezes the final wording):

- `print` keeps its round-47 meaning for the cold path and now reproduces the resolver's stdout and exit status on the
  **warm** path too: the cache file that exists in the environment is honoured exactly as `read_cache` honours it
  (x:217-298) — a hit adopts the cached entry path/id/action, exec argument, ap-id/title/dir/hold arguments and the whole
  command, and **no list or entry file is read**; a miss is the round-47 model.
- `explain` reports `cache=<absent|hit|stale|invalid|disabled>` in its `MADO_TERM:` line (`disabled` = the environment
  gate `XTE_CACHE_ENABLED` fails; see §3.1 for why a `/disable_cache` directive is *not* `disabled`).
- HOME unset is now in contract (round-47 D1 / `ExecC1Diff` H3): a default that needs HOME makes `print` exit 1 with
  empty stdout, and all five XDG variables set lets the resolver run normally.
- Still Python 3 stdlib only, no process, no socket, writes nothing — the tool never saves the cache the resolver would.
  "Writes nothing" is checked per warm fixture (a stat+content snapshot of the tree before and after the run); "no
  process, no socket" is the r47 clause-r property, and the warm path adds only `stat`/`open`/`read` on the cache file.
- `--selftest`: 43 → **68** cases (`MADO_TERMINAL_SELFTEST: 68/68 passed`), still ≥ 30 for clause s.

## 1. The five verifications, and what each one proves

| # | receipt | command | result |
|---|---|---|---|
| 1 | `hash-agree.txt` | `run_hash.sh <seed> 20` × 4 seeds | **80 trees, 0 disagreements**: `gen_hash()` = line 1 of the cache the real pin saved = the pin's own `got fresh hash` line |
| 2 | `ls-diff.txt` | `run_sandbox.sh <seed> 10` × 6 seeds + `harness_shapes.py` | **240 random cases + 31 targeted shapes, 0 byte differences** against the host's GNU ls |
| 3 | `warm-fixtures.txt` | `run_warm.sh` | **31/31 warm fixtures**: the patched tool's rc+stdout = the pin's, and every run left its tree byte-identical (the `quiet` check; a fixture that wrote would have printed `quiet=False`) |
| 4 | `r47-counter.txt` | lane counter at `--nonce 48` on a throwaway clone | `fixtures=190/190 explained=190/190 generated=150/150 selftest=ok readonly=ok verdict=TARGET_MET` |
| 5 | `pin-probes.txt` | `run_probe.sh` | 36 raw resolver probes (20 + 16), the behaviour table of §3 |

All five run inside the counter-shaped sandbox (bwrap `--unshare-all --clearenv`: no `/etc`, `/usr/bin`, `/usr/share`,
`/home`, `/var`; `/usr/lib` + the host bash + copies of the resolver's seven externals; `<root>/.rw` rw for the cache —
the warm harness also binds its fixture tree rw, because it has to prime and mutate it).

How to re-run (scratch is recreated):

```sh
cd <lane>/.ufo/waves/round-48/w1/ExecRefCacheB
python3 patch_tool.py                       # regenerate mado-terminal.py from warmcache.py + the base
TMPDIR=/fast/scratch/hyaku/mado-r48/ExecRefCacheB/tmp python3 -I mado-terminal.py --selftest
for s in 31 32 33 34; do ./run_hash.sh $s 20; done           # 80 primed trees
for s in 1 2 3 4 5 6; do ./run_sandbox.sh $s 10; done        # 240 random ls cases
./run_shapes.sh                                              # 31 targeted ls shapes
./run_probe.sh                                               # 36 resolver cache-edge probes
./run_warm.sh                                                # 31 warm fixtures against the pin
```

Each runner creates its own sandbox assets (the pin copied and sha-checked, copies of the resolver's externals, the
wrapper that keeps the sandbox alive for the background `save_cache`); they share only
`/fast/scratch/hyaku/mado-r48/ExecRefCacheB` and are self-sufficient from an empty one. All receipts in this seat were
regenerated in exactly that order from a clean scratch with the final artifacts. The `r47-counter.txt` recipe (§1.4) is
independent of the scratch: it clones the lane afresh.

Hash/receipt identity detail: the hash in the cache is md5 over `"4\n" + XDG_CURRENT_DESKTOP + "\n"` plus the bytes of
`LANG=C ls -LRl <configs:appdirs>` (x:194-201; whole function x:179-215). `gen_hash()` therefore takes the resolver's *own* `XTE__CONFIGS` and
`XTE__APPLICATIONS_DIRS` (read from `XTE_DEBUG=1` stderr, never re-derived by the harness), so a wrong path list cannot
hide behind a wrong hash.

## 2. `ls` behaviours that surprised me (and that the emulation now encodes)

Each item was found by a failing differential case; the emulation is fixed and all 271 cases pass.

1. **`total` is `sum(st_blocks)` rescaled 512→1024 with CEILING, not a sum of sizes and not a block count.** A 1-byte file
   on XFS has `st_blocks=8` and prints `total 4`. Two such files print `total 8`. A sparse 12345-byte file contributes 0
   while its size column still shows 12345 (one 1-byte file alone in a fresh directory prints `total 4`; two print
   `total 8`; `harness_shapes` `plain-dir`/`plain-files-only`).
2. **A symlink listed under `-L` contributes its target's blocks to the total *again*.** `a.txt` (8 blocks) plus
   `lnk -> a.txt` prints `total 12`, i.e. three 4 KiB units for two names.
3. **The file block's column widths are computed over *all* operands, including directory operands that print no line.**
   `ls -l f1 /usr/share` prints `f1` with the size column 4 wide (from `/usr/share`'s 4222) although `/usr/share` only
   gets a header. A directory block's widths come from its own entries only, floor 1.
4. **The block separator belongs to a directory *attempt*, and the two operand classes differ.** A command-line
   directory that cannot be opened emits the blank line *before* `opendir`, so `ls -lR file noread` ends with a bare
   blank line and no header; a *subdirectory* that cannot be opened emits stderr only — no separator at all
   (`harness_shapes` `unreadable-*`, `tc/br` probe). A missing operand is not a block at all, so `ls -lR nope f1`
   prints `f1` with no header even though two operands were given.
5. **An entry whose `stat()` fails under `-L` gets `l?????????` — and the type letter comes from the *dirent*, not from
   `-L`.** In an unsearchable directory (mode 0644: listable, not traversable) regular files print `-?????????` while a
   dangling symlink prints `l?????????`; the `?` is then padded into the batch's computed widths — right-aligned in
   nlink/size/date, left-aligned in owner/group (so the date slot is 11 spaces + `?`). My first model assumed `l` always
   and the random harness caught it (`ls-diff.txt`, tree 5/8 of seed 1).
6. **A directory operand gets a header under `-R` even when it is the only operand, and `ls -Rl` with NO operands lists
   `.` and prints `.:`** — while `ls -lR ""` (an explicit empty word) prints nothing. Since the resolver expands its
   operand string unquoted, empty fields never reach ls; `gen_hash` relies on that (`ls-diff.txt`, `operands: ['']` case
   that I first got wrong).
7. **LF in a name is printed as `?` even in `literal` quoting** — every other control byte (tab, ESC, 0x01, 0x7f, 0x80,
   0xff) passes through raw. The substitution also applies to operand names and to header paths
   (`nl?name/ctl\x01-x`, `nd?name:`), so it happens at *print* time, never in the path used for `stat`.
8. **Dedupe is only the fts ancestor stack.** `sub` and `dirlnk -> sub` are both listed (contents twice), while
   `self -> .` is skipped with `not listing already-listed directory` on stderr and **no** header; and recursion order is
   the *sorted* order, not readdir order (mkdir order `br,aa,cc` produced blocks `aa`, `br` error, `cc`).
9. **The date field's two boundaries are exact and asymmetric.** Recent iff `mtime <= now` **and**
   `mtime > now − 15778476` (31556952/2): `now−15778476` prints the year, `now−15778475` prints `HH:MM`, and any future
   mtime — even one second ahead — prints the year. 12 columns both ways (`%b %e %H:%M` / `%b %e  %Y`).
10. **`ls` on this host's PATH is a shell builtin** (`ls 0.8.0`) in this session's shell, not GNU coreutils; the
    resolver copies `/usr/bin/ls` 9.12 (the counter picks it with `shutil.which(n, path="/usr/bin")`). My first probe
    used the builtin and reported `ls: d/dirlnk: not listing already-listed directory`, where GNU ls lists that
    directory's contents — every number in this report comes from `/usr/bin/ls`.

Not modelled (declared out of contract in the tool): `BLOCKSIZE`/`LS_BLOCK_SIZE`/`POSIXLY_CORRECT` (they rescale
`total`), `TIME_STYLE`, `COLUMNS`, ACL/SELinux mode suffixes, device nodes, a name whose `lstat` also fails
(`??????????`), and a cache line longer than 1 MiB.

## 3. Resolver behaviours that surprised me (the C1 substance)

Locations are lines of the pinned script (sha256 `89f2be9a…`); every claim is in `receipts/pin-probes.txt`.

1. **`/disable_cache` cannot stop a cache hit.** The directive is parsed on the cold path only, and `save_cache` runs only
   when the cache was *not* used (`save_cache "$1" &`, x:1457), so a cache that still hashes to the tree is used **and
   survives** a `/disable_cache` directive: `out='kitty\n--warm\n' cache_after=True` (`pin-probes.txt:39-40`). The
   resolver's own comment says editing config "should invalidate the cache" — it invalidates by changing the list file's
   metadata, not by the directive. Only `XTE_CACHE_ENABLED=false|0|''` (x:1172, `check_bool`) skips the read; `''` also
   prints `Assuming '' means no`.
2. **An unreadable cache file is a cold path, not an exit.** `read_cache` sits inside `check_bool … && read_cache`
   (x:1179), an `&&` list where `set -e` is suspended, so the failed `done < file` redirection only makes `read_cache`
   return 1: stderr `line 217: … Permission denied`, stdout and rc from the cold path (`pin-probes.txt:16`).
3. **The cached command is checked with `command -v`, which also accepts the script's own function names.** A cache whose
   line 2 is `read_cache` or `gen_hash` is trusted and used (`pin-probes.txt:27`). This makes the cache a
   names-resolve-to-a-function edge that no list/entry fixture reaches.
4. **The hash is metadata, so the whole identity of a file is its size and its *minute* of mtime.** An `Exec=` rewrite
   that keeps the byte count and the minute leaves the cache valid and the warm command wins over the entry's new one
   (`pin-probes.txt:33`); a second-granularity change inside the same minute is equally invisible. `-600 s` or one byte
   more is stale (`pin-probes.txt:34`).
5. **A cached entry path that vanished: `--print-content` exits 1 *after* printing the preceding items** — stdout
   `foot.desktop\n`, rc 1, `line 1362: … No such file or directory` (`pin-probes.txt:28`). But if the cached path is a
   **directory**, the redirection opens, every `read` fails, `shcat` returns 0 and `--print-content` prints nothing with
   **rc 0** (`warm-fixtures.txt:31`). Two different endings, one line of shell.
6. **HOME unset is fatal only where a default needs it.** `${XDG_CONFIG_HOME:-"${HOME}/.config"}` (x:148),
   `${XDG_DATA_HOME:-…}` (x:166) and `${XDG_CACHE_HOME:-…}` (x:172) each die with `HOME: unbound variable`, rc 1, empty
   stdout — but with all five XDG variables set the resolver runs normally (`pin-probes.txt:20-23`). The r47 model
   refused unconditionally, so this is also the `ExecC1Diff` H3 fix.
7. **Cache syntax edges:** a terminator on line 49 is a hit, on line 50 the line-limit branch wins and it is invalid
   (`pin-probes.txt:35-36`); a terminator line without its final LF is never read, so invalid; a cache *directory* is not
   a cache (`[ -f ]`); an empty command line is stale (`command -v ""` fails); a cached `exec_usep` may contain newlines
   and is reassembled with them (`pin-probes.txt:32`), while an empty one prints just a newline (`:30`).
8. **Order of the printed command on a hit:** the Exec words come first, then the prepends app-id, title, dir, hold, then
   the exec argument and the command — so a cached `kitty …--warm` plus `--title=T --hold` prints
   `kitty --warm --title T --hold` (`warm-fixtures.txt:19`). My first selftest expectation had this backwards and the pin
   corrected me.
9. **A warm hit never reads the list**, so a broken/unreadable list is invisible on a hit — the flip side of (1) and the
   sharpest operability consequence: the hotkey can start a command whose configuration is no longer readable
   (`pin-probes.txt:38`, `warm-fixtures.txt:42`).

## 4. What the L1 should know before freezing (my output feeds the freeze)

1. **Schema v2: the hash embeds the absolute paths, so a cache primed at root A is stale at root B.** The resolver hashes
   the *listing text*, which contains the operand paths. Consequence for the counter's two-tree design: a warm fixture
   must prime **each** tree with the real pin (priming is fixture materialization, not judging), or use a `cache` literal
   whose hash the fixture builder computes per root. A literal cache with a *matching* hash is not root-portable; a
   literal cache with a wrong hash is portable and only exercises `stale`/`invalid`. Draft `prime` is therefore
   per-tree, and `after` must be applied to both trees.
2. **Pin every fixture's mtime.** Two runs of the same fixture at different wall-clock times change the `HH:MM` column
   (and, at the six-month edge, the format), so `expect` recorded from the oracle can drift. With `mtime` pinned to a
   fixed epoch the hash text is stable forever; also avoid mtimes within ±120 s of `now` or `now−15778476`, where the
   oracle and the tool can legitimately disagree (my selftest pins to 2019-01-01 and the warm harness to a minute-aligned
   epoch 30 minutes back).
3. **The fixtures that make C1 worth having** (all proven here, `warm-fixtures.txt`): an entry rewrite that keeps size and
   minute (`:15`), the same edit with another second in the same minute (`:16`), a list rewrite that names another terminal with the same size and minute (`:17`), a removed `TryExec`
   stub while `exec[0]` still resolves (`:18`), an unreadable list on a hit (`:42`), cached argument names applied over
   `--title/--dir/--app-id/--hold` (`:19`), and the invalidations: `XDG_CURRENT_DESKTOP` change (`:20`), extra byte
   (`:21`), rename (`:22`), `exec[0]` gone → cold → rc 1 (`:23`), no terminator (`:24`), line 50 (`:25`),
   `XTE_CACHE_ENABLED=false` and `=''` (`:26-27`).
4. **`explain cache=` vocabulary.** I propose `absent|hit|stale|invalid|disabled` with `disabled` = the environment gate
   only; a `/disable_cache` directive with a valid cache is a **hit** (§3.1), so a counter that freezes "disabled" as the
   directive's verdict would encode a resolver bug as a contract. `stale` covers both a hash mismatch and a cached
   command that does not resolve (the resolver prints `cache is out-of-date` for both, x:274-288).
5. **Read-only clause for warm fixtures.** Trace the tool run, not the priming run: the pin forks `save_cache` in the
   background, so an "after python's execve" rule applied to the whole fixture would count the primer's own children. My
   harness instead compares a stat+content snapshot of the tree before and after the tool run (all 31 fixtures clean) —
   that also catches `SendC1Sandbox` F4 (a tool write reaching a later run).
6. **Two holes in the r47 `explain`/`--observed` check that a warm cache makes sharper** (routed `CritC1Explain`): mutate
   the *third* captured line (the command) to require `DIFFER`, and compare `cmd=` in `MADO_TERM:` — on a hit `cmd=` is a
   cached value, the only case where the field can disagree with the entry file.
7. **Integration.** The tool is a single file and must stay one: `python3 -I` drops the script directory from
   `sys.path`, so an `import warmcache` would fail in the counter. Copy `mado-terminal.py` over `tools/mado-terminal.py`
   (it passes the frozen r47 predicate unchanged, §1.4) and, if the module is committed as `tools/warmcache.py` for
   readability, keep it byte-identical to the inlined block — `receipts/inline-identical.txt` is the check, and
   `patch_tool.py` regenerates the tool from the module.

## 5. Residuals, risks, and what is *not* proven

- **Hash fidelity beyond the tested shapes** rests on receipts 1–2: 80 primed trees and 271 `ls` comparisons, all on this
  host's coreutils 9.12 in the counter's sandbox. A different `ls` (busybox, BSD, a coreutils upgrade) is a different
  judge; the counter's oracle uses the host binary, so a host upgrade changes both sides together but the *emulation*
  would need re-verification — the differential harness is the tool for that.
- **`total` depends on the filesystem's `st_blocks`.** Both sides stat the same tree, so fixtures are safe; the selftest
  avoids golden hashes entirely (it builds its cache with the tool's own `gen_hash`), so the selftest proves the cache
  *logic*, not hash fidelity. Fidelity is proven by receipts 1–4 only.
- `--test` with a warm cache is modelled (same argv path) but not fixtured; neither is `--print-cmd=SEQ` /
  `--print-delimiter` on a hit. All four cached argument keys are exercised (`warm-hit-args-over-cached-names`:
  `--app-id`/`--title`/`--dir`/`--hold`).
- Non-UTF-8 bytes in cached fields: `read_cache` decodes them with `surrogateescape` (byte-exact through `os.fsencode`) and
  the tool writes stdout as `latin-1` with `surrogateescape`, so both the tool's latin-1 file convention and raw path
  bytes round-trip; the one gap is a cached *path* holding invalid UTF-8, which `os.stat` would still resolve but the
  output side would print as the original bytes — untested.
- Two new out-of-contract paths, declared: a cache line longer than 1 MiB (`WarmOutOfContract` → the tool's
  `MADO_TERM_OUT_OF_CONTRACT`, exit 2) and mtimes within ±120 s of a date boundary (unstable between two runs, see §4.2).
- The selftest's warm cases use `_pin(root, 1546300800)` and the tool's own hash, so they are portable across hosts and
  filesystems but do not by themselves prove byte-agreement with a real `ls`.
