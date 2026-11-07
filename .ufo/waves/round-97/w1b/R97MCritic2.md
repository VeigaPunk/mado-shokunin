# R97MCritic2 — falsification report on the corrected round-97 claims (w1b)

Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`. Base revision
`e6152b589c2c6a28426c28263c4bcc3c46398be4`. Host: glib2 2.90.1-1, `/usr/bin/gio`
sha256 `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`, python 3.14.8,
uid 1000 (so EACCES/chmod probes bite). Scratch `$HYAKU_SCRATCH/mado-r97/R97MCritic2`
(deleted before yield). Every probe is read-only; no git/jj mutation anywhere (the one
fixture repo is a `mktemp -d` of my own, toplevel asserted).

Artifacts as measured (these files are being rewritten by siblings while this seat runs;
each finding names the sha it was measured on):

```
6454d3dbdb01c9fad2cda9c08b31671f8d1701a627a0bffc61acc49cb14d77ee  build/mado-filetype.v2.py
e68150b553ee7b93550fabb0a57221b51a4fc71ec43da7c9dff71d318c7e070c  build/mado-filetype.py (v1)
4f0b19e3f174b982355bf83b8cab471cbe25d2d2f0058a8c2c17880f912a5199  controls/filetype-cases-v2.json
672bbf5cdfebc531a979f08d13ae462e8fe3c4f968a4e144a2b4737bd0e2334c  controls/filetype-mutants-r97.json
d286ac6b78562f9c5db14bf0aa7d5901eb8e67f0a72b3bb879004b3119b4b0a0  controls/filetype-fresh-r97.py
4c4fb3c50c629b7b68b77dc1f3fad0b549e1f453c8f4d82a3eb3f271d87f4cf4  build/c1-r96-magictext-selftest.py
2bd9e5628993ceccf2739d0782a9cef7ff9ed5c6247336f5f3d07188eb4eb895  build/c2-r96-selftest-kills-selftest.py (== base bytes)
5bb9a8b625481972bf4e0c6ed0ac331ce9a8e4be061acbd8304ba02eb18aa5b8  build/c2-r97-counter-selftest.py (v1)
291d70876078a15c7b51fe61fd86cb1c2656f885fab0b96bb4e5b3abb1289a11  build/c2-r97-counter-selftest.v2.py
```

---
## C1 — findings

### C1-1 (defect, blocks the claim) — an `lstat` EACCES is refused, not tolerated

Rule 7 pins `glocalfileinfo.c:1940-1951`: "A failed `lstat` is refused only when its errno is
**not** `EACCES` … an EACCES is tolerated and the file continues with no stat, the attribute then
coming from the name-only guess and a failed open", and the same rule block ends with the probe
"a file under a mode-000 directory answers `application/octet-stream` exit 0". Both candidates
refuse it:

```
$ R=$PWD/fx; stat -c '%a %n' $R/p3/000d          -> 0  (a search-denied directory)
$ env -i LC_ALL=C HOME=$R/h /usr/bin/gio info -a standard::content-type $R/p3/000d/f.dat
  standard::content-type: application/octet-stream        rc=0
$ env -i LC_ALL=C HOME=$R/h PATH=/usr/bin:/bin python3 -I v2/mado-filetype.py $R/p3/000d/f.dat
  MADO_FILETYPE: ERROR stat path=.../p3/000d/f.dat        rc=2
```

Same result on v1 (`e68150b`). Root cause: `_stat_branch` calls `os.lstat(path)` with no
`try/except`, so an `EACCES` propagates to `main`'s `except OSError` and the path is refused.
Nothing in the frozen material scores it: `controls/filetype-cases-v2.json` has no path whose
parent denies search (`path types` = dir/file/chardev/blkdev/fifo/sock/symlink/unreadable only;
`unreadable` = a mode-000 *file*, which is the open-failure leg, not the stat leg), the fresh
generator's `readerr` class is likewise mode-000 files, and the host list contains no such path
(the tool's 11834-path run prints exactly one `ERROR stat`, for a path that no longer exists).

- Impacted axes: C1 correctness (the branch-order model the claim sells) and C1 coverage (the
  predicate legs are blind to the branch). A reviewer who replays the declaration's own probe
  line gets `ERROR stat` rc 2 where the declaration promises `application/octet-stream` rc 0.
- Smallest safe correction: in `_stat_branch`, wrap the `lstat` and, when `errno == EACCES`,
  return `None` so the caller proceeds with the name-only guess and a failed open
  (`application/octet-stream` for the example); keep refusing every other errno. Add one frozen
  case (a file under a mode-000 directory, label `application/octet-stream`) so the leg bites.

### C1-2 (defect, blocks the claim) — a trailing slash is not trimmed before the stat

GLib's `GLocalFile` trims trailing separators when it constructs the file's path, so the lstat
never sees them. `gio info` prints the trimmed path:

```
$ env -i LC_ALL=C HOME=$R/h /usr/bin/gio info -a standard::content-type $R/p3/a.txt/
  local path: .../p3/a.txt
  standard::content-type: text/plain                       rc=0
$ env -i LC_ALL=C HOME=$R/h /usr/bin/gio info -a standard::content-type /dev/null/
  standard::content-type: inode/chardevice                  rc=0
$ env -i LC_ALL=C HOME=$R/h /usr/bin/gio info -n -a standard::content-type $R/p3/linkdir/
  standard::content-type: inode/symlink                    rc=0     (linkdir -> realdir)
$ env -i LC_ALL=C HOME=$R/h /usr/bin/gio info -a standard::content-type $R/p3/linktxt/
  standard::content-type: text/plain                       rc=0     (linktxt -> a.txt)
```

The candidate passes the raw path to `os.lstat`, so the kernel resolves the slash first:

```
v2, follow:    a.txt/      -> MADO_FILETYPE: ERROR stat            rc=2   (gio text/plain)
v2, follow:    linktxt/    -> MADO_FILETYPE: ERROR stat            rc=2   (gio text/plain)
v2, nofollow:  linkdir/    -> MADO_FILETYPE: inode/directory       rc=0   (gio inode/symlink)
v2, follow:    /dev/null/  -> MADO_FILETYPE: ERROR stat            rc=2   (gio inode/chardevice)
```

The `linkdir/ --nofollow` case is the worst shape: a *silent wrong answer* (rc 0, wrong type),
not a refusal. This also falsifies two evidence documents: (a) the declaration's named limit
"a trailing-slash path to a file … refused … matching `gio info`", and (b) the planning walk's
row "trailing slash on a file | `p3/a.txt/` | no `standard::content-type` line (gio errors)" —
on this host `gio` answers `text/plain` rc 0. Unscored by every leg: 0 of the 150 frozen v2
cases and 0 of the 11834 host paths end in `/`; a 2-link symlink cycle under follow mode is
measured as `inode/symlink` rc 0, so the fresh generator's `brok` comment ("follow mode cannot
stat it: ELOOP -> the oracle refuses") is also wrong, though harmless there.

- Impacted axes: C1 correctness; the claim's own named limit is false.
- Smallest safe correction: strip trailing `/` (leaving `""` and `"/"` intact) from each PATH
  before lstat/follow/open and before `g_path_get_basename`; then `a.txt/` -> `text/plain`,
  `linkdir/ -n` -> `inode/symlink`. Add two frozen cases (file+slash; symlink-to-dir+slash
  under `--nofollow`). If instead the L1 prefers to keep slashes out of scope, the named limit
  and the planning-walk row must be corrected, and a guard must refuse a trailing slash with a
  declared `UNSUPPORTED`, never silently with the wrong branch.

### C1-3 (fixed in v2 — recorded as the checked delta) — sniff length is the database extent

v1's `self.max_buffer_extents = 16384` was the sniff length; v2 derives it
(`_cache_max_extents` over `cache.u32(24)+4`, `_text_max_extents` over the kept matchlets) and
clamps with `_clamp`. Both directions measured on a synthetic database:

```
cache mode, mime.cache patched so the magic section's max_extent field is 4
  file "abcd"+200 NUL:  gio text/plain    v1 application/octet-stream   v2 text/plain
text  mode, magic "[50:application/x-abc] >0=<len 3>XYZ" (extent 0+3+1 = 4)
  file "abcd"+200 NUL:  gio text/plain    v1 application/octet-stream   v2 text/plain
  file "XYZ"+NULs:      gio application/x-abc on both candidates (the magic matches inside 4)
```

Caveat for the freeze: the **host** database's extent is 18730, which clamps to 16384, so
neither the host leg nor the fresh generator (which copies the host DB) can ever observe this
rule; only a synthetic-extent case can. Add one frozen case with a built `mime.cache` whose
magic extent is small and a second with a text-mode `magic` of extent 4, or the rule is verified
only by the candidate's own `--selftest`.

### C1-4 — coverage arithmetic of the frozen case file (predicate clause (i))

`controls/filetype-cases-v2.json` (sha `4f0b19e`): 150 cases, `classes` = the 15 declared names,
per class `dir 10, chr 9, blk 10, fifo 9, sock 9, zero 11, empty 9, sym 10, brok 10, nofollow 9,
follow 9, certain 11, uncertain 14, fast 10, readerr 10` — every class >= 8. Label census spans
every branch the model has: `text/plain 48, inode/symlink 20, application/octet-stream 19,
inode/directory 17, application/x-zerosize 15, inode/fifo 14, inode/blockdevice 12, inode/socket 12,
inode/chardevice 11, image/png 7, app/x-pngdata 5, text/html 3, app/x-foo 3, app/x-foo2 3,
application/x-desktop 1, text/x-readme 1, app/x-rangehit 1`; `ERROR` labels 0. So clause (i) is
reachable — but the two path classes of C1-1/C1-2 are absent (`path types` has no
"file-under-denied-dir", and 0 trailing-slash non-dir paths).

Mutants (`672bbf5`): 81 rows, all 15 classes (`dir 8, chr 4, blk 4, fifo 4, sock 3, zero 9,
empty 1, sym 8, brok 3, nofollow 4, follow 4, certain 6, uncertain 12, fast 6, readerr 5`), and
every `find` occurs exactly once in v2 (`not anchored: []`). `empty` has a single mutant and
`sock`/`brok` three each — thin, but each class kills at least one. No mutant touches the
EACCES or trailing-slash behaviour, which is unavoidable: they are wrong in the base candidate,
so they are not "mutations" of a correct model.

### C1-5 — the host leg does exercise the stat branches (predicate clause (iv))

`lstat` classification of the 11834 host paths: `reg 6403` (243 of size 0), `dir 4472`,
`lnk 850`, `chr 94`, `blk 11`, `sock 3`, one path already gone. Sample of 600 random paths,
tool (v1) vs `/usr/bin/gio`: **0 mismatches**; the gio label census over that sample is
`inode/directory 234, text/plain 70, application/xml 61, ... inode/chardevice 5,
inode/symlink 7, application/x-zerosize 10, application/x-desktop 8`; a 220-path v2 sample:
0 mismatches. The full run over the list (v1) answers 11834/11834 and prints exactly one
`ERROR stat` (the vanished path; gio also exits 2 on it); v2 was compared on a 220-path
sample plus the 15 special paths, 0 mismatches. Note the list is *volatile*:
`/home/vgpnk/.config/OpenBot/blob_storage/7fbceadf-...` was present at generation and absent
~40 minutes later; a stale line is harmless only because both sides refuse it.

### C1-6 — the name-only control really scores below (computed)

Using `tools/mado-mimeglob.py`'s `Resolver` over each case's own XDG dirs, answering every path
by its basename only: **64 / 192 = 0.333** on `filetype-cases-v2.json` (and 59 / 196 = 0.301 on
the v1 case file). Per class: `blk 0/10, chr 0/9, fifo 0/10, sock 0/10, zero 0/12, brok 0/11,
certain 11/12, fast 9/10, readerr 9/11, dir 6/18, sym 12/22, uncertain 5/14, follow 4/17,
nofollow 4/17, empty 4/9`. Strictly below the total, as the claim requires.

### C1-7 — the fresh generator: oracle-measured labels, but a fixed fixture family

`controls/filetype-fresh-r97.py` computes every label by running `/usr/bin/gio` on the built
root (`gio_label`), so there is no concealed fixed label table; a path whose oracle run yields
no attribute is dropped with a counted note, and `empty_cases != 0` is a SETUP_ERROR. What is
*not* fresh: the file contents and the relative paths per class are constants (`PNG/PDF/ZIP/ELF/
OGG/TXT/DESKTOP/SH`), and the DB is always a copy of the host's eight text files or its cache,
so the extent is always the host's 18730->16384. Consequence: a path-keyed memoriser is not
tested (only an input-hash-keyed one is), and the fresh leg cannot reach C1-1, C1-2 or the
extent rule. Not a defect in itself; it bounds what "fresh" proves.

---
## C2 — findings

### C2-1 (defect, blocks clause (i)) — the counter's `--selftest` cannot find the fixtures where they are

Contract 4 puts fixtures under `.ufo/waves/round-97/selftest-fixtures/`; the counter resolves
`__file__/../selftest-fixtures` (`_mado_counter_selftest_fixtures_dir(None, None)`) and the
dispatch at `main()` passes `_mado_counter_selftest(None, _fdir)`. In the build directory that
happens to be right; in the landed layout (`quality/counters/…`) and in the C2 runner's layout
it is not. Measured in a layout mirroring the v2 runner (counter at `quality/counters/`, the
committed fixtures copied to `.ufo/waves/round-97/selftest-fixtures/`):

```
$ python3 -I lay/quality/counters/c1-r96-magictext.py --selftest
MADO_COUNTER_SELFTEST: checks=7 failed=0
rc=2                              <- could-not-evaluate; the C2 runner requires rc 0
$ ... --selftest --fixture-dir lay/.ufo/waves/round-97/selftest-fixtures
MADO_COUNTER_SELFTEST_FAIL: C1-missing-cases
MADO_COUNTER_SELFTEST_FAIL: C1-mutant-mismatch
MADO_COUNTER_SELFTEST: checks=7 failed=2
rc=1
```

So under the runner's invocation (`[python3, -I, <counter>, --selftest]`, no `--fixture-dir`,
no `--repo`) the green leg is unreachable, and with the fixtures supplied the selftest is red.
The second counter (`build/c2-r96-selftest-kills-selftest.py`, sha `2bd9e56` = base bytes) has
no `--selftest` at all, so `selftest_green=2/2` is 0/2 at this revision.

- Fix: resolve the fixture root with an upward walk for `.ufo/waves/round-97/selftest-fixtures`
  (then `$PWD`), and teach the C2 runner to pass it; and land the third counter's selftest.

### C2-2 (defect) — two of the seven selftest checks are red on their own fixtures

- `C1-missing-cases` invokes the counter with only five of the ~20 mandatory arguments, so
  argparse refuses (rc 2) and prints no `SETUP_ERROR`; the check looks for `SETUP_ERROR` in the
  output and fails. (Reproduced directly: the same invocation prints `error: the following
  arguments are required: --mutants, --expect-mutants-sha256, ...`.)
- `C1-mutant-mismatch` asserts `dummy_tool.count(mut["find"]) != 1` while
  `selftest-fixtures/dummy-tool.py` contains the mutant's `find` (`checks=50`) exactly once ->
  the check returns False by construction.
- Fix: pass the full argument set in the first check (dummy pins are fine: the missing `--cases`
  fires first), and align the second check's polarity with its fixture (`== 1` if the intent is
  "detectable", or remove the anchor from the dummy).

### C2-3 (fixed in v2 — recorded as the checked delta) — the C2 counter v1 cannot be replayed and cannot go green

On `build/c2-r97-counter-selftest.py` (`5bb9a8b`):

```
$ python3 -I build/c2-r97-counter-selftest.py --repo . --rev <rev> --base-rev <base> \
    --expect-base-registry-sha256 <sha> ... --scratch-root <dir>
c2-r97-counter-selftest.py: error: unrecognized arguments: --base-rev ... --expect-base-registry-sha256 ...
rc=2
```

i.e. the declaration's own counting command is rejected. And its always-OK expression
(`stub_flagged = rc == 1 or failed != 0 or id in out`) can never be true for the three-line stub
(rc 0, `failed=0`, no id), while `always_ok_flagged == 0` is required: on a synthetic repo whose
counters satisfy contract 4 the counter printed
`TARGET_MISSED ... negative_ids=12/12 broken_modes=3/3 registry_rows=4/4 always_ok_flagged=12` —
the only failing conjunct is the unsatisfiable one. v2 (`291d708`) fixes both; on the same
synthetic repo it prints
`TARGET_MET ... selftest_green=2/2 checks=6,6 negative_ids=12/12 broken_modes=6/6 broken_c1=3/3
broken_c2=3/3 always_ok_flagged=0 registry=1->4 ledger_members=2/2 ledger_uncovered_ok=True`.
That synthetic run is the satisfiability witness for PRED-C2 v2's plumbing — the remaining
blockers are on the counters' side (C2-1, C2-2).

### C2-4 — the registry move 1 -> 4 is re-derivable (checked)

At `e6152b58`, over `SKILL.md` table rows: `tools/mado-mimetext.py` 1 hit (line 887),
`quality/counters/c1-r96-magictext.py` 0, `quality/counters/c2-r96-selftest-kills.py` 0,
`quality/selftest-kills/check-receipt-presence.json` 0 -> base 1. v2 prints the per-artifact
`base=/rev=` pairs and `registry artifacts covered base=1 rev=4`, so the corrected `1 -> 4`
movement is now measured at both revisions.

### C2-5 (residual) — the always-OK control is a tautology

v2 keeps the three-line stub (`print('MADO_COUNTER_SELFTEST: checks=6 failed=0')`, exit 0) and
counts a neutralisation as "credited" when the stub's rc is 1, its result line is non-green, or
the panel id appears in its output. As written the stub can never produce any of those, so
`always_ok_flagged=0` is guaranteed and the clause tests nothing. A stub that echoed the panel
ids would be *counted as flagging* (and fail the clause), which is backwards. Fix: make the
control "the judging code must not credit a file that prints the declared ids without running
the checks", i.e. have the stub print the result line **and every panel id**, and require
`always_ok_flagged == 0` with that stronger stub (the `find`-anchor rule then refuses the stub
because its ids come from a print, not from a check that can be neutralised).

### C2-6 (instrument vs sentence) — "no socket" is not what the structural allowlist enforces

The predicate's clause reads "the structural allowlist (no process, socket, network or non-libc
dynamic import)". `build/c1-r97-filetype.py` (current bytes) has
`_OK_IMPORTS = {..., 'errno', 'socket', ...}` and an audit hook that admits `socket.__new__` for
`AF_UNIX` only; `static_check(build/mado-filetype.v2.py)` returns `[]`, and the candidate's
`--selftest` does `import socket as _sock` to create the `inode/socket` fixture. The instrument
is defensible; the frozen sentence is wrong. Fix: restate clause (vi) as "no process, network or
non-libc dynamic import; `socket` only as the AF_UNIX fixture constructor in `--selftest`", or
move the socket fixture behind `os.mknod(S_IFSOCK)` (needs privilege) and drop the import.

### C2-7 (freeze bookkeeping) — declared input paths vs present filenames

The C1 command in the declaration names `controls/filetype-cases-r97-frozen.json`,
`controls/filetype-mutants-r97-frozen.json` and `controls/forgery-ctypes-r97.py`; the C2 command
names `controls/counter-selftest-panel-r97.json`. At this revision the first two exist only as
`filetype-cases-v2.json` (`4f0b19e`) and `filetype-mutants-r97.json` (`672bbf5`), and the
forgery file and the panel do not exist. Replaying either command verbatim today exits 2
(SETUP_ERROR). This is expected to be closed by the freeze copies, but the names must match
exactly or the pins land against the wrong bytes.

---
## What held (negative results, so the L1 does not re-run them)

- Branch order on the host: `/dev/null`,`/dev/zero` -> `inode/chardevice`; `/dev/nvme1n1` ->
  `inode/blockdevice`; a bound AF_UNIX socket -> `inode/socket`; `mkfifo` -> `inode/fifo`;
  directories named `dir.png` -> `inode/directory`; size-0 regular files (incl. `/proc/self/status`,
  `/proc/version`, `/proc/self/maps`, `/proc/kallsyms`, `/proc/1/status`) -> `application/x-zerosize`.
- Symlinks: `tonull -> /dev/null` follow -> `inode/chardevice`, `-n` -> `inode/symlink`;
  dangling and `loop -> loop` and a two-link cycle -> `inode/symlink` rc 0 in both modes;
  live link to a file follows to the target's name/bytes; `linkdir/` in follow mode -> directory.
- Name step: `.desktop` with desktop bytes -> `application/x-desktop` (one name type, never
  sniffed); the same bytes under `d.txt` -> `text/plain`; desktop bytes under an untyped name
  (`deskblob.bin`) -> `text/plain` (the x-desktop rewrite); `w.png` holding `plain words` ->
  `image/png`; a name containing a newline -> `text/plain` (escaped `\x0a` in the output, same
  answer); a non-UTF-8 name (`caf\xe9.png`) -> `image/png` on both.
- Read/open legs: mode-000 file -> name-only answer (`application/octet-stream`, `text/plain`
  when the name is typed) on both; `/proc/kcore` (huge size, open refused) -> octet-stream on
  both; `/sys/class/dmi/id/sys_vendor` and `/sys/devices/system/cpu/online` (stat size 4096,
  short read) -> `text/plain` on both. I could not produce a size-change-between-stat-and-read
  divergence: both sides re-guess with the bytes actually read, and the only asymmetry
  (open failure) is the modelled name-only fallback. Deterministic size changes (`truncate`)
  remain unmeasured — no safe way to schedule them against the oracle.
- Databases: empty element in `XDG_DATA_DIRS` (`d1::`, `d1:`) agrees (`db=none`, same answers);
  a single-name-type file under a >16384 extent agrees (no sniff); `--fast` never sniffs;
  the clamp keeps 16384 for extent 20000.

## Verdict

**C1 is not ready to freeze.** The candidate's own declaration (rule 7 plus its probe line) is
falsified by measured oracle disagreements on two path classes (C1-1 EACCES, C1-2 trailing
slash), and no frozen leg — cases, mutants, fresh generator, host list — can see either. The v2
extent fix is real and checked (C1-3), but it is invisible to every frozen leg as well.
**C2's instrument v2 is sound** (satisfiability witness in C2-3; registry movement measured), but
the counters it measures are red or absent (C2-1, C2-2), and three predicate sentences overstate
what is enforced (C2-5, C2-6) or name files that do not exist yet (C2-7).

Checks the L1 must re-run at the freeze, because these artifacts are moving targets:
`python3 -I build/<candidate> --selftest` from a landed-layout copy; the C2 counter v2 against a
tree carrying the four registry rows and the two counter selftests; and the two oracle probes of
C1-1/C1-2 (`chmod 000` parent directory; `a.txt/`, `linkdir/ -n`, `/dev/null/`).

Report: .ufo/waves/round-97/w1b/R97MCritic2.md
