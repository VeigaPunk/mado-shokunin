# R97MMutC1b - the C1 candidate v2 mutant population (round 97, w1b)

Seat `R97MMutC1b` (mutation tester), lane `mado`, round 97, hyaku run 15, wave w1b, base revision
`e6152b589c2c6a28426c28263c4bcc3c46398be4` (branch `master`). Leaf seat: no subagents, no commits, no
mutating git/jj command, no host-service or sysctl change, no package transaction (nothing installed; the
host pacman pause is intact).

## Inputs and the anchor

| input | sha256 / value |
|---|---|
| anchored candidate bytes | `.ufo/waves/round-97/build/mado-filetype.v2.py` = `da6af7a0789265187f6b2c2462bf5104a7c0b780baed3235300f89978a44d2d8` (606 lines) |
| frozen cases | `.ufo/waves/round-97/controls/filetype-cases-v2.json` = `fc710b94df67391c392d95aeabd6dfa4c016081019d732f5c373fb990844be20` (157 cases, 15 classes) |
| freeze counter pairing | `.ufo/waves/round-97/build/c1-r97-filetype.v2.py` = `745a341e8a2aaefc7283d1ad4090ebde01d631d118f788ddd1dcc7b5195ba9e0` |
| oracle | `/usr/bin/gio` = `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`, glib 2.90.1 |
| my controls file | `.ufo/waves/round-97/controls/filetype-mutants-v2.json` = `549bb84a981168482defafccf54ba9a91d4a58a4783552e8d3efbc79632b3ae1` |

The candidate was still moving while the wave ran: `6454d3db` (first v2), `e0086e3f` (EACCES/trim), then the
final `da6af7a0` (GFile normalisation, in-place ERROR line, no-socket selftest). Every anchor in this file is
validated against `da6af7a0`; the extent anchors are byte-unchanged across all three pins. The earlier pins
were only used for mechanism study and are not reported as measurements.

## Method (counter-equal, audited)

120 probes were applied one at a time to an isolated scratch copy of the frozen candidate:

1. Each probe is a single `src.replace(find, replace, 1)` on the anchored bytes; `find` occurs exactly once
   in the whole file, lies outside `def selftest`, and is unique across all counted mutants (the freeze
   counters own `validate_mutants` returns zero errors on this file).
2. The copy sits beside copies of `mado-mimeglob.py`, `mado-mimesniff.py` and `mado-mimetext.py`; the probe
   runs through the C1 counters own `LAUNCHER_SRC` audit hook (allowlist = candidate tree + fixture root +
   Python roots, empty PATH, `TMPDIR` = case root), i.e. the same launcher that rejects a library-asking forgery.
3. Flags are generated exactly like the counters `tool_flags` (`--follow|--nofollow`, `--fast`, `--home`,
   `--data-home[-unset]`, `--data-dirs[-unset]`), paths passed after `--`.
4. Scoring is the counters: `MADO_FILETYPE` type, attr and mode must match the frozen label, attr and mode,
   the `MADO_FILETYPE_DIRS: db=` value must match the fixture-derived db mode, and a missing/extra line is
   wrong. A kill is at least one `wrong` case; a crash (unparsable/non-0/2 exit) is NOT a kill.

Pristine baseline under the same launcher and fixtures: **157/157 ok, 0 wrong, 0 crash**. Every reported
kill is therefore a behavioural difference, not a baseline failure. One first form of the cache-halve probe
had an unbalanced parenthesis (it crashed 150 cases); it was corrected, re-probed, and the corrected form
survives - it is listed under `not_observable`, not counted. No other crash occurred in the final run.

## Result totals

| bucket | count | audited outcome |
|---|---|---|
| counted mutants (`expect: kill`) | **101** | 101 killed, 0 crashed |
| not observable | **11** | 11 survived (0 wrong) |
| equivalents | **8** | 8 survived (0 wrong) |
| total probes | 120 | 101 killed, 19 survived, 0 crashed |

## class_kills census (the counters semantics: a killed mutant counts for every case class in which it
produced a wrong answer)

| case class | killed mutants | wrong cases |
|---|---|---|
| dir | 29 | 189 |
| chr | 12 | 80 |
| blk | 10 | 84 |
| fifo | 12 | 72 |
| sock | 18 | 132 |
| zero | 25 | 180 |
| empty | 34 | 196 |
| sym | 53 | 319 |
| brok | 15 | 107 |
| nofollow | 57 | 193 |
| follow | 56 | 191 |
| certain | 32 | 199 |
| uncertain | 51 | 347 |
| fast | 30 | 185 |
| readerr | 39 | 221 |

`class_kills = 15/15`; every one of the 15 mutant-class labels is also
present among the 101 counted mutants (dir, chr, blk, fifo, sock, zero, empty, sym, brok, nofollow, follow,
certain, uncertain, fast, readerr).

## Required rule coverage

### The database extent (declaration rule 4, contract 2)

| rule point | mutant | killing frozen case | observed |
|---|---|---|---|
| constant 16384 instead of cache extent | `uncertain-20-cache-extent-constant` | uncertain-13-cache-extent-small | want text/plain, got application/octet-stream |
| constant 16384 / extent erased (cache) | `uncertain-21-cache-extent-zero`, `uncertain-22-cache-extent-empty` | uncertain-13, uncertain-14 | want text/plain, got application/octet-stream |
| cache word 24 read as word 28 | `uncertain-23-cache-header-word28` | uncertain-13 | want text/plain, got application/octet-stream |
| cache section +8 instead of +4 | `uncertain-24-cache-extent-plus8` | uncertain-13, uncertain-14 | want text/plain, got application/octet-stream |
| cache section +0 instead of +4 | `uncertain-25-cache-extent-plus0` | uncertain-13, uncertain-14 | want text/plain, got application/octet-stream |
| OUT_OF_BOUNDS guard removed | `uncertain-26-cache-guard-off` | uncertain-14-cache-guard-badcache | want text/plain, got application/octet-stream |
| guard alignment clause dropped | `uncertain-27-cache-guard-alignment-drop` | uncertain-14 | want text/plain, got application/octet-stream |
| constant 16384 instead of text extent | `uncertain-32-text-extent-constant`, `uncertain-33-text-extent-zero`, `uncertain-40-text-init-cap`, `uncertain-46-clamp-always-cap` | uncertain-10-text-extent-small | want text/plain, got application/octet-stream |
| text extent fixed at 9 | `uncertain-34-text-extent-fixed9` | uncertain-10 | want text/plain, got application/octet-stream |
| text extent drops range_length | `uncertain-35-text-drop-range`, `uncertain-36-text-drop-range-substr` | uncertain-11-text-extent-range | want app/x-rangehit, got text/plain |
| text extent uses value only | `uncertain-38-text-value-only` | uncertain-11 | want app/x-rangehit, got text/plain |
| text max selection inverted | `uncertain-39-text-max-invert` | uncertain-10 | want text/plain, got application/octet-stream |
| text extent halved | `uncertain-43-text-halve` | uncertain-06-multi-foo-png (+1) | wrong parsed answer |
| text extent +1 (boundary) | `uncertain-44-text-return-plus1` | uncertain-10 | want text/plain, got application/octet-stream |
| clamp inverted (0 -> 0, >cap -> n) | `uncertain-45-clamp-invert` | empty-07-empty-none-db, uncertain-12-text-extent-clamp, +5 | want text/plain/octet-stream, got application/x-zerosize / app/x-farhit |
| clamp zero leg removed | `uncertain-47-clamp-zero-off` | empty-07, certain-10, uncertain-09 | wrong parsed answer |
| buffer constant 65536 | `uncertain-48-cap-65536` | uncertain-12 | want text/plain, got app/x-farhit |
| read n+1 bytes | `uncertain-50-read-extent-plus1` | uncertain-10 (+2) | want text/plain, got application/octet-stream |

### The two-stage stat and its follow/nofollow branches (declaration rule 7)

| rule point | mutant | killing frozen case | observed |
|---|---|---|---|
| lstat removed (single stat) | `sym-07-lstat-to-stat` | sym-02-link-to-file-nofollow, sym-04-link-to-dir-nofollow, +17 | want inode/symlink, got text/plain / inode/directory |
| follow dereference removed | `sym-04-stat-to-lstat` | sym-03-link-to-dir-follow, brok-01-dangling-follow, +15 | want inode/directory / inode/symlink, got application/octet-stream |
| broken flag dropped (raise) | `brok-02-broken-raises` | brok-01-dangling-follow, brok-03-self-loop-follow, +12 | want inode/symlink, got ERROR stat (rc 2) |
| broken classified as directory | `brok-01-broken-directory` | brok cases | want inode/symlink, got inode/directory |
| broken classified as octet-stream | `brok-03-broken-octet` | brok cases | want inode/symlink, got application/octet-stream |
| loop classification (self-loop, two-node) | `brok-02-broken-raises`, `sym-07-lstat-to-stat` | brok-03-self-loop-follow, brok-05-two-node-loop-follow | ERROR stat / octet-stream instead of inode/symlink |
| nofollow inverted (answer constant follow) | `nofollow-01-answer-const-follow` | sym-02, sym-04, sym-10 | want inode/symlink, got target type |
| nofollow inverted (decision) | `nofollow-02-answer-invert`, `nofollow-03-argparse-action`, `sym-01-nofollow-invert`, `sym-02-nofollow-false`, `sym-03-nofollow-true` | sym-02, sym-04, follow/nofollow cases | wrong mode/type |
| follow forced off | `follow-01-answer-false`, `follow-02-symlink-and-follow`, `follow-03-symlink-invert`, `sym-08-answer-follow-true` | follow/nofollow/sym cases | wrong target resolution |
| EACCES lstat tolerance removed | `readerr-40-eacces-tolerance-off` | readerr-11-dir-unreadable, readerr-12-dir-unreadable-named | want inode/directory / octet-stream / text/plain, got ERROR stat |
| gio trailing-slash trim removed | `dir-40-trailing-trim-off`, `dir-42-norm-all-off` | dir-11-trailing-slash-file, dir-12-trailing-slash-chardev, sym-11, sym-12 | want text/plain / inode/chardevice / inode/symlink, got ERROR stat |

## not_observable (11) - real behaviour changes the frozen cases cannot see

All 11 were applied to a scratch copy and run over all 157 frozen cases under the launcher: 0 wrong, 0
crash each. Each row names the missing fixture shape; these are coverage findings, not contract changes.

| mutant | what it changes | why no frozen case sees it |
|---|---|---|
| `dir-41-normpath-off` | drops posixpath.normpath, keeps rstrip | Drops posixpath.normpath but keeps rstrip. No frozen path contains '//', '/./' or '/../' (cases scan), so normalisation is the identity on every scored path. Fr |
| `follow-04-follow-default-false` | argparse --follow default | Changes the argparse default for --follow. The counter's tool_flags always passes an explicit --follow or --nofollow for every case (manifest flags), so the def |
| `nofollow-04-follow-default` | argparse --follow default | Same argparse-default mutation as follow-04 (the counter always passes one of the two flags explicitly), so no case can observe it. Frozen-suite probe: 0/157 wr |
| `uncertain-28-cache-guard-bounds-drop` | guard bounds clause dropped | Drops the bounds part of the OUT_OF_BOUNDS guard but keeps the alignment clause. The only malformed cache in the frozen set (uncertain-14-cache-guard-badcache,  |
| `uncertain-29-cache-last-wins` | max over caches -> last assignment | Assigns instead of taking max, so the last admissible cache wins. Every frozen fixture has at most one cache that passes the guard (uncertain-13/08: one cache;  |
| `uncertain-30-cache-halve` | cache extent halved | Halves the cache max_extent. uncertain-13/14: 8 -> 4; the control byte sits at index 8 and is not seen by a 4-byte read either, so both answer text/plain. uncer |
| `uncertain-31-cache-first-only` | caches[:1] | Iterates caches[:1]. In uncertain-14 the first cache (d1) is the good extent-8 cache and d2 is skipped by the guard anyway; all other cache fixtures hold one ca |
| `uncertain-37-text-drop-offset` | text extent drops matchlet offset | Drops '+ matchlet offset' from the text extent. Every frozen text magic database uses offset 0 except the clamp leg uncertain-12 (offset 16385), and there both  |
| `uncertain-41-text-first-matchlet` | matchlets[:1] per section | Takes only the first matchlet of each section. Every frozen text magic section (custom fixture DBs and the extent additions) contains exactly one matchlet; the  |
| `uncertain-42-text-first-match` | matches[:1] (first section only) | Takes only the first magic section. Every frozen text magic file has exactly one section; a text database with two sections whose second carries the maximum ext |
| `uncertain-49-cap-8192` | sniff buffer 8192 | Lowers the sniff buffer to 8192. Small extents (8/9) are unaffected; the clamp leg uncertain-12 has a 16390 window that is unreachable under both 8192 and 16384 |

## equivalents (8) - semantically identical mutations, audited 0/157 wrong

| mutant | argument |
|---|---|
| `eq-01-clamp-ge-boundary` | at n == 16384 both branches yield 16384; for n > 16384 both yield 16384; identical values. |
| `eq-02-max-le` | when max_extent == extent assigning extent leaves the value unchanged; max is identical. |
| `eq-03-cache-order` | max over the caches is commutative; the guard is per cache; the result is the same maximum. |
| `eq-04-no-cloexec` | the tool never forks or execs, so O_CLOEXEC has no observable effect on the answer or the descriptor use. |
| `eq-05-read-n-nonzero` | n is _clamp(extent) and clamp maps 0 to 16384, so the branch n==0 is unreachable; identical read length. |
| `eq-06-extent-add-order` | integer addition is commutative; the computed extent is identical. |
| `eq-07-guard-int-shift` | for integer offsets, offset > size is exactly offset >= size + 1. |
| `eq-08-norm-conditional` | a or b with truthy a is a; the same value is selected when a is empty. |

## Kill appendix (101 counted mutants)

`wrong n` is the number of frozen cases the probe answered differently from their gio label; `first case`
and the recorded difference is the first observed divergence (wrong type, attr or mode, wrong db line, or a
missing/extra line). Every row is a scratch-copy run over the 157 frozen cases through the audit launcher.

| mutant | class | wrong n | first killing case | recorded difference |
|---|---|---|---|---|
| `dir-01-wrong-symlink` | dir | 17 | dir-01-plain-subdir | want inode/directory/full/follow got ('type', 'inode/symlink', 'full', 'follow') |
| `dir-02-drop-branch` | dir | 17 | dir-01-plain-subdir | want inode/directory/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `dir-03-as-reg` | dir | 100 | dir-01-plain-subdir | want inode/directory/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `dir-04-always` | dir | 133 | dir-01-plain-subdir | want text/plain/full/follow got ('type', 'inode/directory', 'full', 'follow') |
| `dir-05-name-before-branch` | dir | 14 | dir-02-dir-named-x-png | want inode/directory/full/follow got ('type', 'image/png', 'full', 'follow') |
| `dir-06-branch-only-fast` | dir | 53 | dir-01-plain-subdir | want inode/directory/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `dir-40-trailing-trim-off` | dir | 4 | dir-11-trailing-slash-file | want text/plain/full/follow got ('error', None, None, None) |
| `dir-42-norm-all-off` | dir | 4 | dir-11-trailing-slash-file | want text/plain/full/follow got ('error', None, None, None) |
| `chr-01-wrong-block` | chr | 12 | dir-12-trailing-slash-chardev | want inode/chardevice/full/follow got ('type', 'inode/blockdevice', 'full', 'follow') |
| `chr-02-drop-branch` | chr | 7 | dir-12-trailing-slash-chardev | want inode/chardevice/full/follow got ('type', 'application/x-zerosize', 'full', 'follow') |
| `chr-03-as-reg` | chr | 99 | dir-01-plain-subdir | want text/plain/full/follow got ('type', 'inode/chardevice', 'full', 'follow') |
| `chr-04-always` | chr | 123 | dir-01-plain-subdir | want text/plain/full/follow got ('type', 'inode/chardevice', 'full', 'follow') |
| `blk-01-wrong-chr` | blk | 12 | blk-01-dev-nvme1n1 | want inode/blockdevice/full/follow got ('type', 'inode/chardevice', 'full', 'follow') |
| `blk-04-swap-bodies` | blk | 22 | dir-12-trailing-slash-chardev | want inode/chardevice/full/follow got ('type', 'inode/blockdevice', 'full', 'follow') |
| `fifo-01-wrong-sock` | fifo | 12 | fifo-01-plain | want inode/fifo/full/follow got ('type', 'inode/socket', 'full', 'follow') |
| `fifo-02-reg-or-fifo` | fifo | 92 | dir-01-plain-subdir | want text/plain/full/follow got ('type', 'inode/fifo', 'full', 'follow') |
| `fifo-03-zero-size-fifo` | fifo | 25 | sock-01-plain | want inode/socket/full/follow got ('type', 'inode/fifo', 'full', 'follow') |
| `fifo-04-sock-or-fifo` | fifo | 11 | sock-01-plain | want inode/socket/full/follow got ('type', 'inode/fifo', 'full', 'follow') |
| `sock-01-wrong-fifo` | sock | 11 | sock-01-plain | want inode/socket/full/follow got ('type', 'inode/fifo', 'full', 'follow') |
| `sock-02-drop-branch` | sock | 11 | sock-01-plain | want inode/socket/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `sock-03-as-reg` | sock | 87 | dir-01-plain-subdir | want text/plain/full/follow got ('type', 'inode/socket', 'full', 'follow') |
| `zero-01-wrong-empty` | zero | 14 | zero-01-empty-png-name | want application/x-zerosize/full/follow got ('type', 'application/x-empty', 'full', 'follow') |
| `zero-02-drop-size-guard` | zero | 78 | dir-01-plain-subdir | want text/plain/full/follow got ('type', 'application/x-zerosize', 'full', 'follow') |
| `zero-03-size-ne` | zero | 88 | dir-01-plain-subdir | want text/plain/full/follow got ('type', 'application/x-zerosize', 'full', 'follow') |
| `zero-04-size-one` | zero | 10 | zero-01-empty-png-name | want application/x-zerosize/full/follow got ('type', 'image/png', 'full', 'follow') |
| `zero-05-drop-reg-guard` | zero | 11 | sock-01-plain | want inode/socket/full/follow got ('type', 'application/x-zerosize', 'full', 'follow') |
| `zero-06-size-negative` | zero | 10 | zero-01-empty-png-name | want application/x-zerosize/full/follow got ('type', 'image/png', 'full', 'follow') |
| `zero-07-reg-or-size` | zero | 87 | dir-01-plain-subdir | want text/plain/full/follow got ('type', 'application/x-zerosize', 'full', 'follow') |
| `zero-08-branch-fifo-type` | zero | 14 | zero-01-empty-png-name | want application/x-zerosize/full/follow got ('type', 'inode/fifo', 'full', 'follow') |
| `zero-09-truncate-results` | zero | 35 | dir-01-plain-subdir | lines=1 want=2 |
| `empty-01-branch-disabled` | empty | 10 | zero-01-empty-png-name | want application/x-zerosize/full/follow got ('type', 'image/png', 'full', 'follow') |
| `sym-01-nofollow-invert` | sym | 21 | zero-10-proc-self-status | want application/x-zerosize/full/follow got ('type', 'inode/symlink', 'full', 'follow') |
| `sym-02-nofollow-false` | sym | 4 | sym-02-link-to-file-nofollow | want inode/symlink/full/nofollow got ('type', 'text/plain', 'full', 'nofollow') |
| `sym-03-nofollow-true` | sym | 17 | zero-10-proc-self-status | want application/x-zerosize/full/follow got ('type', 'inode/symlink', 'full', 'follow') |
| `sym-04-stat-to-lstat` | sym | 17 | sym-03-link-to-dir-follow | want inode/directory/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `sym-05-mode-relstat` | sym | 3 | sym-03-link-to-dir-follow | want inode/directory/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `sym-06-basename-realpath` | sym | 3 | sym-06-link-to-file-fast | want application/octet-stream/fast/follow got ('type', 'text/plain', 'fast', 'follow') |
| `sym-07-lstat-to-stat` | sym | 20 | sym-02-link-to-file-nofollow | want inode/symlink/full/nofollow got ('type', 'text/plain', 'full', 'nofollow') |
| `sym-08-answer-follow-true` | sym | 4 | sym-02-link-to-file-nofollow | want inode/symlink/full/nofollow got ('type', 'text/plain', 'full', 'nofollow') |
| `brok-01-broken-directory` | brok | 14 | brok-01-dangling-follow | want inode/symlink/full/follow got ('type', 'inode/directory', 'full', 'follow') |
| `brok-02-broken-raises` | brok | 14 | brok-01-dangling-follow | want inode/symlink/full/follow got ('error', None, None, None) |
| `brok-03-broken-octet` | brok | 14 | brok-01-dangling-follow | want inode/symlink/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `nofollow-01-answer-const-follow` | nofollow | 4 | sym-02-link-to-file-nofollow | want inode/symlink/full/nofollow got ('type', 'text/plain', 'full', 'nofollow') |
| `nofollow-02-answer-invert` | nofollow | 21 | zero-10-proc-self-status | want application/x-zerosize/full/follow got ('type', 'inode/symlink', 'full', 'follow') |
| `nofollow-03-argparse-action` | nofollow | 23 | dir-03-nested-dirs | want inode/directory/full/nofollow got ('type', 'inode/directory', 'full', 'follow') |
| `follow-01-answer-false` | follow | 17 | zero-10-proc-self-status | want application/x-zerosize/full/follow got ('type', 'inode/symlink', 'full', 'follow') |
| `follow-02-symlink-and-follow` | follow | 6 | sym-02-link-to-file-nofollow | want inode/symlink/full/nofollow got ('type', 'text/plain', 'full', 'nofollow') |
| `follow-03-symlink-invert` | follow | 40 | dir-03-nested-dirs | want inode/directory/full/nofollow got ('type', 'inode/symlink', 'full', 'nofollow') |
| `certain-01-guess-no-name` | certain | 2 | uncertain-05-multi-foo-text | want app/x-foo2/full/follow got ('type', 'text/plain', 'full', 'follow') |
| `certain-02-gate-suffix` | certain | 37 | dir-01-plain-subdir | want text/plain/full/follow got ('type', 'text/plainx', 'full', 'follow') |
| `certain-03-fast-uncertain-field` | certain | 14 | empty-05-text-fast | want application/octet-stream/fast/follow got ('type', '1', 'fast', 'follow') |
| `certain-05-name-only-sniffer` | certain | 50 | empty-01-text-no-name-type | want text/plain/full/follow got ('type', 'application/x-zerosize', 'full', 'follow') |
| `certain-08-type-suffix` | certain | 156 | dir-01-plain-subdir | want inode/directory/full/follow got ('type', 'inode/directoryX', 'full', 'follow') |
| `certain-09-type-upper` | certain | 156 | dir-01-plain-subdir | want inode/directory/full/follow got ('type', 'INODE/DIRECTORY', 'full', 'follow') |
| `uncertain-01-gate-invert` | uncertain | 27 | empty-01-text-no-name-type | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-02-gate-true` | uncertain | 27 | empty-01-text-no-name-type | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-03-read-zero` | uncertain | 33 | empty-01-text-no-name-type | want text/plain/full/follow got ('type', 'application/x-zerosize', 'full', 'follow') |
| `uncertain-04-empty-data` | uncertain | 33 | empty-01-text-no-name-type | want text/plain/full/follow got ('type', 'application/x-zerosize', 'full', 'follow') |
| `uncertain-05-types-first` | uncertain | 1 | uncertain-06-multi-foo-png | want app/x-pngdata/full/follow got ('type', 'app/x-foo2', 'full', 'follow') |
| `uncertain-06-guess-uncertain-field` | uncertain | 33 | empty-01-text-no-name-type | want text/plain/full/follow got ('type', '0', 'full', 'follow') |
| `uncertain-07-guess-empty` | uncertain | 33 | empty-01-text-no-name-type | want text/plain/full/follow got ('type', 'application/x-zerosize', 'full', 'follow') |
| `uncertain-12-read-no-directory` | uncertain | 27 | empty-01-text-no-name-type | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-13-fixed-or-octet` | uncertain | 63 | dir-01-plain-subdir | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-14-basename-split-first` | uncertain | 23 | dir-05-dir-with-slash | want app/x-foo/full/nofollow got ('type', 'text/plain', 'full', 'nofollow') |
| `uncertain-15-name-only-octet` | uncertain | 63 | dir-01-plain-subdir | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-16-fast-const-true` | uncertain | 7 | empty-05-text-fast | want application/octet-stream/fast/follow got ('type', 'text/plain', 'fast', 'follow') |
| `uncertain-20-cache-extent-constant` | uncertain | 2 | uncertain-13-cache-extent-small | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-21-cache-extent-zero` | uncertain | 2 | uncertain-13-cache-extent-small | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-22-cache-extent-empty` | uncertain | 2 | uncertain-13-cache-extent-small | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-23-cache-header-word28` | uncertain | 2 | uncertain-13-cache-extent-small | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-24-cache-extent-plus8` | uncertain | 2 | uncertain-13-cache-extent-small | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-25-cache-extent-plus0` | uncertain | 2 | uncertain-13-cache-extent-small | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-26-cache-guard-off` | uncertain | 1 | uncertain-14-cache-guard-badcache | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-27-cache-guard-alignment-drop` | uncertain | 1 | uncertain-14-cache-guard-badcache | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-32-text-extent-constant` | uncertain | 1 | uncertain-10-text-extent-small | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-33-text-extent-zero` | uncertain | 1 | uncertain-10-text-extent-small | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-34-text-extent-fixed9` | uncertain | 1 | uncertain-10-text-extent-small | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-35-text-drop-range` | uncertain | 1 | uncertain-11-text-extent-range | want app/x-rangehit/full/follow got ('type', 'text/plain', 'full', 'follow') |
| `uncertain-36-text-drop-range-substr` | uncertain | 1 | uncertain-11-text-extent-range | want app/x-rangehit/full/follow got ('type', 'text/plain', 'full', 'follow') |
| `uncertain-38-text-value-only` | uncertain | 1 | uncertain-11-text-extent-range | want app/x-rangehit/full/follow got ('type', 'text/plain', 'full', 'follow') |
| `uncertain-39-text-max-invert` | uncertain | 1 | uncertain-10-text-extent-small | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-40-text-init-cap` | uncertain | 1 | uncertain-10-text-extent-small | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-43-text-halve` | uncertain | 2 | uncertain-06-multi-foo-png | want app/x-pngdata/full/follow got ('type', 'app/x-foo2', 'full', 'follow') |
| `uncertain-44-text-return-plus1` | uncertain | 1 | uncertain-10-text-extent-small | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-45-clamp-invert` | uncertain | 7 | empty-07-empty-none-db | want application/octet-stream/full/follow got ('type', 'application/x-zerosize', 'full', 'follow') |
| `uncertain-46-clamp-always-cap` | uncertain | 3 | uncertain-10-text-extent-small | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `uncertain-47-clamp-zero-off` | uncertain | 3 | empty-07-empty-none-db | want application/octet-stream/full/follow got ('type', 'application/x-zerosize', 'full', 'follow') |
| `uncertain-48-cap-65536` | uncertain | 1 | uncertain-12-text-extent-clamp | want text/plain/full/follow got ('type', 'app/x-farhit', 'full', 'follow') |
| `uncertain-50-read-extent-plus1` | uncertain | 3 | uncertain-10-text-extent-small | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `fast-01-gate-false` | fast | 7 | empty-05-text-fast | want application/octet-stream/fast/follow got ('type', 'text/plain', 'fast', 'follow') |
| `fast-02-gate-invert` | fast | 34 | empty-01-text-no-name-type | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `fast-03-answer-const-full` | fast | 7 | empty-05-text-fast | want application/octet-stream/fast/follow got ('type', 'text/plain', 'fast', 'follow') |
| `fast-04-argparse-store-false` | fast | 156 | dir-01-plain-subdir | want inode/directory/full/follow got ('type', 'inode/directory', 'fast', 'follow') |
| `fast-05-attr-invert` | fast | 156 | dir-01-plain-subdir | want inode/directory/full/follow got ('type', 'inode/directory', 'fast', 'follow') |
| `fast-06-types-first-fallback` | fast | 9 | empty-05-text-fast | want application/octet-stream/fast/follow got ('type', 'text/plain', 'fast', 'follow') |
| `readerr-01-none-octet` | readerr | 1 | readerr-04-000-multi-foo | want app/x-foo2/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `readerr-02-none-suffix` | readerr | 7 | readerr-01-000-uncertain-png | want application/octet-stream/full/follow got ('type', 'application/octet-streamx', 'full', 'follow') |
| `readerr-03-open-nofollow` | readerr | 10 | sym-01-link-to-file-follow | want text/plain/full/follow got ('type', 'application/octet-stream', 'full', 'follow') |
| `readerr-04-open-empty-bytes` | readerr | 7 | readerr-01-000-uncertain-png | want application/octet-stream/full/follow got ('type', 'application/x-zerosize', 'full', 'follow') |
| `readerr-05-open-empty-or` | readerr | 7 | readerr-01-000-uncertain-png | want application/octet-stream/full/follow got ('type', 'application/x-zerosize', 'full', 'follow') |
| `readerr-40-eacces-tolerance-off` | readerr | 2 | readerr-11-dir-unreadable | want application/octet-stream/full/follow got ('error', None, None, None) |

## Restoration and hygiene

- The anchored lane bytes were never modified: `.ufo/waves/round-97/build/mado-filetype.v2.py` hashed
  `da6af7a0...` before the population was built and again after the final audited run; identical.
- Every probe was written only inside a per-probe directory under `/fast/scratch/hyaku/mado-r97/R97MMutC1b`
  (a scratch copy with the three sibling tools copied beside it); the lane `tools/`, `quality/`, `corpus/`,
  `SKILL.md` and the git/jj state were read-only. Scratch is deleted before yield (`chmod -R u+rwX` first
  because two fixtures carry mode-000 dirs); the wave artifacts are the controls JSON and this report.
- No tool was installed or upgraded; no package transaction, no sudo, no host-service change.
- Inputs re-checked at report time: cases `fc710b94...`, counter v2 `745a341e...`, tool `da6af7a0...`;
  the freeze must pin this exact three-way pairing (the 150-case ce56e42c file is superseded: it cannot
  exercise the trim/normalise/EACCES shapes, which is why dir-40/42 and readerr-40 moved from
  `not_observable` to counted mutants when the 157-case file landed).

## Report
Report: .ufo/waves/round-97/w1b/R97MMutC1b.md
