# RevC1Ls — attack on exact `ls -LRl` hashing (frozen C1 tool)

Seat `RevC1Ls` · round 48 / wave **w2 = FALSIFY**, policy v1 · lane `mado-shokunin` ·
base `579f694b45c797a9c39761fdb4f9e0a1b71b3585` · frozen instruments read, never edited:
`quality/counters/c1-r48-terminal-cache.py` (sha256 `2a7d03d96d6ea5489fecc110de8d29b83d6c3d2d6abd4e5d4138096d01ccddd4`),
`quality/counters/c1-r48-fixtures.json` (= `SHA256_WARM`), `quality/counters/c1-r47-fixtures.json` (= `SHA256_COLD`),
`.ufo/waves/round-47/fetch/xdg-terminal-exec` (= `PIN_SHA256`).
Target: does the frozen tool's `gen_hash` reproduce the real resolver's cache hash byte for byte, focused on
multiple operands, numeric-owner padding, dangling symlinks, sibling symlink dirs, empty dirs, recent/future mtimes.

**Headline.** In the target class I found **no hash mismatch**: on 500 independently seeded trees, 61 purpose-built
cases and 7 primed warm trees the frozen tool `l1-draft/mado-terminal.py`
(sha256 `1dfde36cfa68beffb6b2bc2ae9cf04875bd48702669812ce3ecd10b986753a92`, identical to `tools/mado-terminal.py`)
is byte-identical to the pin. What I did find is a **pre-data hole in the predicate's discriminating power**:
`PRED-C1-r48` returns **TARGET_MET** for an emulator that never dereferences symlinks (`-L`), because no clause and
no fixture can create a symlink. Two full counter runs are the evidence (§4). That is not a miss under the frozen
letter (no clause fails) — it is a hole the registration itself allows w2 to surface before data, and it is the
finding I would act on before the data commit.

## 1. Method — the pin is the judge, the hash is read from the pin itself

Per tree: build a synthetic XDG hierarchy, leave a **complete but stale** cache file at `$XDG_CACHE_HOME/xdg-terminal-exec`
(10 fields + `\x1eEND_OF_EXEC_USEP`), run the **real pin** with `XTE_DEBUG=1 --print-id`, and read
`D: got fresh hash '<md5>'` — the pin's own `gen_hash` result (x:179-215), computed in the foreground because
`read_cache` hashes before it compares. Then ask the frozen tool for the hash of the *same tree and env* and compare.
`--print-id` never saves a cache (only `--print-cmd`/`--test` do), so the pin writes nothing.

Three independent quantities per tree, so a difference is attributed, never guessed:

| value | how |
|---|---|
| `pin_hash` | the judge: the pin's `got fresh hash` line |
| `h_ls_pinops` | md5 over real `LC_ALL=C LANG=C /usr/bin/ls -LRl` with the **pin's own** operand list (parsed from its `paths:` debug block) — must equal `pin_hash`, else the harness is at fault |
| `tool_hash` | `Resolver(env).select_paths().gen_hash()`, process cwd = tree root |

`PASS` requires `h_ls_pinops == pin_hash == tool_hash`. The `h_ls_pinops` step is not decoration: it caught two of my
own harness bugs before they became false findings (a `TZ` that the in-process tool saw differently, and a
bash-`echo` option model that ignored `dsk[1:]`), and it is what makes the operand-list parse trustworthy — if my
parse of the pin's operands were wrong, the reconstruction could not equal the pin's hash.

Harness properties that matter for reading the numbers: the tool is imported in-process, so `TZ` is applied with
`time.tzset()` per tree (the tool reads `TZ` through the C library, as a CLI tool should) and no `LS_*` variable is
in the process environment. Every hook/cwd/env of the compared run is the pin's env verbatim.

## 2. The 500-tree campaign (seeded, independent)

`python3 run/driver.py --from 1 --to 500` — seed `N` drives its own `random.Random(N)` tree, so the campaign is
reproducible tree for tree (`--seed N --keep` prints the reproduction command).

Observed last line: `SUMMARY {"PASS": 500} seeds=1..500`. **500/500.**

Scale actually exercised (measured per tree, aggregated in `summary.json` in this seat directory):

| dimension | measured |
|---|---|
| operands hashed | 5 895 positions (3 746 existing: list files, application dirs, dir-shaped list paths) |
| trees with **both** file and dir operands (file block + per-block widths + blank-line rule) | 492 / 500 |
| trees with **numeric-owner** entries (4242 / 60000 / 70000, uid-only, gid-only, next to resolved names) | 489 |
| trees with a **dangling symlink entry** / **dangling symlink operand** | 267 / 151 |
| trees with **sibling symlink dirs** (two names → one target, or link + real dir) | 192 |
| **empty dirs** / hidden-only dirs | 461 / 168 |
| **recent** / **old(year form)** / **future(year form)** mtimes | 490 / 498 / 445 |
| FIFO entries · setuid/setgid/sticky modes | 225 · 126 |
| duplicate operands · relative operands · `//` in a path | 43 · 40 · 37 |
| names with space / tab / non-ASCII | 55 / 56 / 47 |
| missing operands (stderr only, dropped from stdout) | 490 trees, 1 963 operands |
| `TZ` values | `UTC`, `America/Sao_Paulo`, `Europe/Berlin`, `Asia/Kolkata`, `UTC+5:30` |
| `XDG_CURRENT_DESKTOP` values | 12, incl. `-n`, `-e`, unset, `A:B:C`, and a value ending in a newline |

Not produced by the seed generator (and therefore covered by §3 instead, stated so the table is not read as
complete): ancestor **loops** and a **symlink-as-directory-operand** (0 seeds — my builder gated `..` links on a
depth it never reaches). Both are in the matrix.

## 3. Targeted matrix — one purpose-built tree per named class (61 cases)

`python3 run/matrix.py` → `MATRIX cases=61 pass=58 other=3`. The three non-pass are the tool's **declared**
out-of-contract classes (§5.3), where the pin hashes and the tool refuses by design.

Passing (each leaves a tree the case name describes; every one compared against the pin):
`dangling_entry_alone`, `dangling_entry_mixed`, `dangling_operand_only`, `dangling_operand_with_file`,
`dangling_two_entries`, `numeric_all`, `numeric_mixed`, `numeric_wide` (7-digit id beside 5-char names),
`numeric_gid_only`, `numeric_uid_only`, `numeric_dir_entry`, `numeric_operand_file`, `root_owned_name`,
`symlink_dir_twins`, `symlink_dir_and_real`, `symlink_dir_operand` (the operand itself is a symlink + trailing `/`),
`symlink_dir_operand_slash` (a list path that is a symlink to a directory → a dir operand with no trailing slash),
`symlink_ancestor_loop`, `symlink_to_self`, `symlink_chain`, `empty_operand`, `empty_nested`, `hidden_only`,
`empty_hidden_mix`, `time_future_file`, `time_future_dir`, `time_epoch`, `time_negative` (pre-1970),
`time_edge_min`/`time_edge_plus` (±2 days either side of the six-month rule), `time_now_exact`,
`time_mixed`, `many_dirs_files` (12 dir operands + 12 file operands), `file_only_operands`, `dup_dir_operand`,
`dup_appdir_operand` (the same application dir twice), `file_block_widths` (9 000-byte list file + dir operands),
`double_slash`, `dot_component`, `dotdot_component`, `relative_paths`, `trailing_slash_xdg`, `dash_desktop`,
`empty_desktop`, `multidesktop`, `long_name`, `high_byte_name` (invalid UTF-8 in a name), `high_byte_dir`
(invalid UTF-8 in an XDG path), `space_tab_names`, `unreadable_operand`, `unreadable_nested`,
`unreadable_file_operand`, `mode_bits` (suid/sgid/sticky), `socket_entry`, `device_entry`
(`mknod c 10 237` beside a 7-byte file → the shared size column), `hardlink_nlink`, `big_nlink_dir`, `mixed_sizes`.

Two GNU behaviours I confirmed from the binary rather than from prose, because they change the hash bytes:
`-L` on a **dangling operand** prints `ls: cannot access …` and *nothing* on stdout (the operand is dropped from
the hashed stream, and the tool agrees); an **unopenable directory** gets **no header and no `total`** (GNU opens
before it prints the header), which is exactly what the tool's `except OSError: return` does — I had expected the
opposite and the measurement corrected me.

## 4. The finding: `PRED-C1-r48` cannot see `-L` (two full counter runs)

The fixture schema (`files` text or `dir/`, `exec` stubs, `mtime`, `modes`, `cache`/`prime`, `after`) has no way to
create a symlink, and the counter has no such call: `grep -c 'os.symlink' quality/counters/c1-r48-terminal-cache.py`
→ **0** (the only symlink handling is bwrap's `--symlink usr/lib /lib` mount setup), `write_files` only does
`makedirs`/`open`, `add_execs` only writes 755 stubs, `apply_after.modes` only `chmod`s. `gen_case` and
`gen_warm_case` build `files`/`exec` dicts only. So **every** tree any clause prepares is symlink-free, and on a
symlink-free tree `-L` is indistinguishable from no `-L`.

I scored two mutants of the frozen tool through the frozen counter on my own scratch clone
(`run/seat-score.sh`, clone at base + draft counter/fixtures committed, `--nonce 48048`):

| mutant (one-line change in the frozen tool) | clause s | f | w | x | g | r | verdict |
|---|---|---|---|---|---|---|---|
| `m1-drop-dangling`: dangling row → `continue` | **rc=1, last=''** (selftest crashes) | 190/190 | 204/204 | 394/394 | 230/230 | ok | TARGET_MISSED (clause s only) |
| `m3-no-deref`: `_stat` uses `os.lstat` (= no `-L` anywhere) | ok `69/69` | 190/190 | 204/204 | 394/394 | 230/230 | ok | **TARGET_MET, exit 0** |

`out-m3-noderef.txt`, final line verbatim:
`PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET`

`m3` is not exotic: with it, `<data dir>/applications/` is a *link* rather than a directory operand whenever the
user symlinks that directory (a common dotfile/stow layout), and every symlinked subdirectory inside it prints as an
`l` row instead of its own block — a different hash on any such tree, i.e. the cache verdict flips. The frozen
predicate still says TARGET_MET. The 948 pin-judged cases (190+204+394+230) are all blind to it; only the tool's own
hermetic selftest is in the way for `m1`, and the selftest has no symlink case either (`69/69` with `m3`).

Control that makes the point non-rhetorical (my `mutants.py`, one tree each, pin as judge):

| mutant | tree | diverges from pin | real tool on same tree |
|---|---|---|---|
| `m1-drop-dangling` | dangling entry beside a numeric owner and a wide name | **yes** | matches |
| `m2-wrong-dangling-row` (`l---------`) | dangling entry alone | **yes** | matches |
| `m3-no-deref` | sibling symlink dirs | **yes** | matches |
| `m4-owner-right-justify-all` | numeric id 4242 beside `vgpnk` | **yes** | matches |
| control: `m1` | `many_dirs_files` (schema-expressible: files/dirs/modes only) | **no** | matches |
| control: `m3` | `many_dirs_files` | **no** | matches |

Recommendation (pre-data, the only window): add a `links` primitive to schema v2 (`{path: target}` for symlinks,
`{"path": null}` already deletes) and score it in clause w with: dangling entry, dangling *operand*, sibling twins
to one target, a symlink-to-directory operand (with and without a trailing slash), an ancestor loop, and a
link chain — one fixture per class is enough, plus one control that must miss (`m3`-shaped). Until then the
registration's own sentence — "`gen_hash` must be byte-equal to `LC_ALL=C LANG=C ls -LRl` output" — is not what the
instrument measures.

## 5. Further gaps, ranked

### 5.1 Owner-column justification is also unscored (same mechanism)
The schema has no `chown` and the counter's sandbox has no `/etc`, so `pwd`/`grp` lookups fail and **every** entry is
numeric with a uniform width; a wrong justification then produces identical bytes. `m4` (numeric ids left-justified)
diverges from the pin on `numeric_mixed` (§4 controls) but no fixture can build that tree. Measured on the host and
matched by the tool: GNU **right-justifies** a numeric uid/gid (`"  4242"` beside `vgpnk`, width 5) and left-justifies
resolved names; `numeric_wide` (7-digit id vs 5-char names) and `root_owned_name` (uid 0 → `root`) both pass.
Freeze-hygiene nit: the w1 `ExecLsEmu.md` table says "numeric ids and `?` go through the same name path"; the pin says
otherwise and the tool is right, so only that sentence needs fixing, not the tool.

### 5.2 Three declared-out-of-contract classes are reachable in reality and absent from `registration.md`'s residuals
Each was measured: the pin produces a hash, the tool exits 2.

| class | case | pin | tool |
|---|---|---|---|
| ACL / security xattr under a hashed path (mode byte `+`/`.`) | `acl_xattr` (`setfacl -m u:4242:r` on a hashed entry) | hashes fine | `MADO_TERM_OUT_OF_CONTRACT: ls ACL/security xattr present under a hashed path` |
| newline in a hashed name | `newline_name` | hashes fine (GNU prints `?`) | `… newline in an ls path/name changes the cache hash` |
| mtime within 1 s of the six-month boundary | `time_boundary_exact` (`now − 15778476`) | hashes fine | `… mtime within one second of GNU ls six-month date boundary` |

The tool docstring (line ~"Out of contract") does list them; `registration.md`'s C1 "Residuals" paragraph does not.
Suggest one residual line naming all three (a residual statement, not a predicate change), since the C1 claim as
written ("byte-equal … over the colon-split operands") is false for exactly these trees.

### 5.3 The `LS_COLORS` guard is over-broad
`run/envprobe.py` (same tree, one variable added at a time; `pin_moved` = the pin's hash changes):

| variable | pin hash moved | tool |
|---|---|---|
| `LS_COLORS=rs=0:di=01;34` | **no** | refuses: `OOC:LS_COLORS set …` |
| `QUOTING_STYLE=escape` | no (plain names; would move with a name needing quoting) | refuses |
| `TIME_STYLE=long-iso` | yes | refuses |
| `POSIXLY_CORRECT=1` | yes | refuses |
| `BLOCK_SIZE=512`, `LS_BLOCK_SIZE=512` | yes | refuses |
| `COLUMNS=40` | no | matches (correct) |
| `TZ=Europe/Berlin` | yes | matches (dates follow `TZ`, as the pin does) |

`LS_COLORS` cannot change `ls -lR` bytes (no `--color`, not a tty), so guarding it costs the capability outright in
any session that exports it: `mado-terminal.py print/explain` exits 2 instead of predicting. The counter is blind to
this because the sandbox runs `--clearenv` with the case env, and no fixture sets an `LS_*` variable. Narrow the
guard to the variables that can move the bytes (`TIME_STYLE`, `POSIXLY_CORRECT`, `BLOCK_SIZE`, `LS_BLOCK_SIZE`, and
`QUOTING_STYLE` only when some hashed name needs quoting).

### 5.4 Things I attacked and could **not** falsify (recorded so the pass is not over-read)
- `total` = floor(Σ `st_blocks`/2): unobservable on this filesystem — every `st_blocks` I sampled under
  `/usr/share/applications` and `tools/` is a multiple of 8 (0 odd values), so floor and round-to-nearest agree.
  No fixture can falsify the rounding rule here; the w1 note stands.
- The frozen warm-fixture determinism claim holds where it can be measured: the 145 fixtures that pin `mtime` use
  only `1577836800` / `1600000000` (2 235–2 491 days old at count time — always year form, never crossing the
  six-month boundary, never future); no `after.mtime` is near the boundary or future; no fixture sets an `LS_*`
  variable; no `cache`-literal fixture claims `state=hit` (25 literal caches: 14 invalid, 10 stale, 1 disabled);
  every `hit` fixture carries `prime`; all `WARM-DIFFERS`/`WARM-SAME` records are consistent with their `cold`.
  Digests verified: `SHA256_COLD` = `4836cc1d…dd86`, `SHA256_WARM` = `4d946bd7…11aa`, `PIN_SHA256` =
  `89f2be9a…27ac` = the committed pin **and** `/usr/bin/xdg-terminal-exec`.
- The hash *as used* (not just as a number): 7 trees primed by the pin itself, then checked four ways — pin says
  `cache is actual`, the tool's `read_cache` says `hit`, both print the same command; adding a file to a hashed
  directory makes **both** say `stale`; and a **same-length content edit with the mtime re-pinned** leaves both at
  `hit` (the hash covers the listing, not the content) — `run/matrix.py --warm`, 7/7.

## 6. Reproduce

```sh
S=/fast/scratch/hyaku/mado-r48/RevC1Ls          # seat scratch (created, then removed)
# the scripts below are the exact bytes that ran; put them in $S/run, plus the pin and tool:
#   cp <seat>/{driver,matrix,mutants,envprobe}.py <seat>/seat-score.sh $S/run/
#   mkdir -p $S/run/pin $S/run/tool
#   cp .ufo/waves/round-47/fetch/xdg-terminal-exec $S/run/pin/ && chmod +x $S/run/pin/xdg-terminal-exec
#   cp .ufo/waves/round-48/l1-draft/mado-terminal.py $S/run/tool/
cd $S/run && python3 driver.py --from 1 --to 500 --out results.jsonl     # 500 seeds, 25 s
cd $S/run && python3 matrix.py                                            # 61 cases, 9 s
cd $S/run && python3 matrix.py --warm                                     # 7 primed trees
cd $S/run && python3 mutants.py                                           # mutant/control demonstration
cd $S/run && python3 envprobe.py                                          # ls-env guard precision
# one frozen-counter run (writes only into its own scratch; clones the lane because the recipe does):
bash run/seat-score.sh $S/run/mut/m3-no-deref.py m3 48048
python3 driver.py --seed 137 --keep      # a single seeded tree + its reproduction command
```
Receipts in this seat directory: `driver.py`, `matrix.py`, `mutants.py`, `envprobe.py`, `seat-score.sh`,
`results.jsonl` (500 records incl. per-tree class coverage), `summary.json`, `matrix.json`, `warm.json`,
`mutants.json`, `envprobe.json`, `out-m1-dropdangling.txt`, `out-m3-noderef.txt`,
`m1-drop-dangling.py`, `m3-no-deref.py` (the two mutants as scored).

## 7. Budget, tooling, safety

No lane Git/jj mutation, no commit, no push, no edit to tracked lane files, registry, counters, entry or report —
only this file and `.ufo/waves/round-48/w2/RevC1Ls/`. No package install, no pacman transaction, no compositor or
service change, no input injection, no GUI. Host config and binaries read-only; `sudo -n` used only for
`chown -h` / `mknod` / `rm -rf` inside my own scratch trees (numeric-owner and device cases, and cleanup after
`chown`). Scratch: `/fast/scratch/hyaku/mado-r48/RevC1Ls/` (621 MB peak, under the 2 GB budget; removed at the end).
Largest file written: 4 207 542 B — the lane clone's largest tracked blob, an unavoidable byte copy in the
counter recipe; my own largest output is `results.jsonl` at 963 835 B, under 1 MiB. Every seat-authored writer ran
under `ulimit -f 2048`; `seat-score.sh` raises the limit to 65536 **only** around the lane clone (documented in the
script) because the 1 MiB/file bound cannot hold a 4.2 MB tracked blob, and the scratch budget is checked after the
run. Two full counter runs on a 269 MB clone each (the foreground one measured 5 m 53 s; the second ran in the background and its duration was not recorded); both clones deleted.

## 8. Residuals of this seat

- I compared the **hash**, not the resolver's stdout/exit on my trees (other seats own clause w/x behaviour); the
  warm subset (§5.4) does compare stdout, and it agreed.
- The tool ran in-process for hash extraction; `TZ` was matched with `time.tzset()` per tree. I did not reproduce the
  counter's bwrap mount set or its no-`/etc` numeric-id regime independently (the counter's own 204×2 pass covers
  it; my chown cases cover the harder *mixed* numeric/named regime on the host).
- No mismatch tree to reproduce: nothing in the target class diverged. The only divergences are the tool's three
  declared refusals (§5.2) and the four mutants (§4).
