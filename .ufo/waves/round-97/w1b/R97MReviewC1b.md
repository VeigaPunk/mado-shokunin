# R97MReviewC1b -- attack on the final C1 bytes (round 97, w1b)

Seat: `R97MReviewC1b` (reviewer, leaf member; no subagents). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Base revision
`e6152b589c2c6a28426c28263c4bcc3c46398be4`. Read-only review: no lane file, counter, case file,
mutant file or receipt of another seat was modified or committed (this report and its own receipt are
the only lane writes); scratch was `$HYAKU_SCRATCH/mado-r97/R97MReviewC1b` (removed before yield).

## 0. Inputs attacked (final bytes, measured at review time)

| input | sha256 | size / shape |
|---|---|---|
| `build/mado-filetype.v2.py` (final candidate) | `da6af7a0789265187f6b2c2462bf5104a7c0b780baed3235300f89978a44d2d8` | 606 lines, 29646 B, 0 non-ASCII |
| `controls/filetype-cases-v2.json` (final cases) | `fc710b94df67391c392d95aeabd6dfa4c016081019d732f5c373fb990844be20` | 157 cases, 201 paths, 15 classes, 1 `ERROR` label |
| `controls/filetype-fresh-r97.py` (fresh generator) | `c3143775d346921085a4f312eb596bc9b062abb11c3257aed47d9bba50bf7bf2` | 120-case run used |
| `controls/filetype-host-r97.txt` (host list) | `4f28035b4cfea0b3f6d8d9f5eb3efb630b2a09db4fc06fa141555e76a9a829a4` | 11834 paths (no trailing `/`, no `.`/`..` segments) |
| `/usr/bin/gio` (oracle) | `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462` | `gio --version` 2.90.1; glib2 2.90.1-1 |
| counter v2 (`build/c1-r97-filetype.v2.py`, not frozen) | `745a341e8a2aaefc7283d1ad4090ebde01d631d118f788ddd1dcc7b5195ba9e0` (last checked; three v2 pins passed) | used only for `static_check`/`validate_cases` |

The seat brief named `build/mado-filetype.v2.py` and `controls/filetype-cases-v2.json`; both were
moving during the wave. Intermediate pins I also attacked and rejected as superseded:
`6454d3db...` (extent fix only) and `e0086e3f...` (extent + EACCES + slash-trim only). All numbers below
are the final pins above unless a row says otherwise. The case file gained seven scored cases between
`ce56e42c...` (150) and `fc710b94...` (157): trailing slash on file/chardev/symlink, two `dir-unreadable`
EACCES cases and one `missing`/`ERROR` case.

Environment: python 3.14.8, non-root uid 1000 (EACCES probes bite), host db cache mode, host extent
18730 clamped to 16384.

## 1-2. Oracle re-derivation and candidate diff (tasks 1 and 2)

Method: rebuild every case root from the case JSON (base64 `files`, typed `paths` incl.
`dir-unreadable`/`missing`, `chmod 000` last), then per path
`env -i LC_ALL=C HOME=<root>/h [XDG_DATA_HOME=<root>/dh] XDG_DATA_DIRS=<root>/db[:..] /usr/bin/gio
info -a standard::content-type|standard::fast-content-type [-n] <raw path>`; the candidate is run
per path with the same four roots, mode and attribute, from the same root cwd.

* 30-case deterministic sample (first two cases of each of the 15 classes): 36 paths,
  `label_rederived=36/36`, `candidate=36/36`, `nameonly=13/36`.
* All 157 cases: 201 paths, `label_rederived=201/201`, `candidate=201/201`, `nameonly=67/201`.
  No candidate mismatch and no label mismatch on any path; the single `ERROR` label
  (`readerr-13-missing`) is reproduced as `MADO_FILETYPE: ERROR stat` with rc 2.

Class shape of the final file (cases / paths): dir 12/18, chr 9/9, blk 10/10, fifo 9/10, sock 9/10,
zero 11/12, empty 9/9, sym 12/22, brok 10/11, nofollow 9/17, follow 9/17, certain 11/12,
uncertain 14/14, fast 10/10, readerr 13/14. Every class is reachable and >= 9 cases (>= 8 required).

Per-class result of the 30-case sample (paths; all 100%): dir 4, chr 2, blk 2, fifo 2, sock 2,
zero 2, empty 2, sym 4, brok 2, nofollow 3, follow 3, certain 2, uncertain 2, fast 2, readerr 2.

**Verdict (surface):** at the final pins the candidate is the oracle on every frozen path, including
the newly added trailing-slash, `dir-unreadable` and `missing` cases.

## 3. No-work control (task 3)

The r94 name-only model (`tools/mado-mimeglob.py`, the same sibling the candidate loads, called on
each path's basename with the case's db env) scores **13/36** on the sample and **67/201** on the
full file, against **36/36** and **201/201** for the candidate. It is strictly lower on both sets.
It misses at least one path in all 15 classes (dir 12, chr 9, blk 10, fifo 10, sock 10, zero 12,
empty 5, sym 10, brok 11, nofollow 13, follow 13, certain 1, uncertain 9, fast 1, readerr 2 of 201),
so the gap is structural (stat branches, the sniff and the re-guess), not one fixture.

## 4. Extent-rule attack (task 4)

Fixtures are review-built (scratch, read-only); the "16384-byte read" comparator is the base draft
`build/mado-filetype.py` (`e68150b5...`, `SNIFF_CAP` constant 16384), i.e. exactly what a constant-cap
model would answer.

| probe | gio | final v2 | base draft (constant 16384) |
|---|---|---|---|
| cache whose magic section declares `max_extent=8`; file `SQLite format 3\0...` (rule needs 16 B at 0) | `text/plain` (8 B are printable, no match) | `text/plain` | `application/vnd.sqlite3` |
| text db, matchlet `0>0=\x00\x03ZZZ` -> extent 4; file `ABCD`+16000 NUL | `text/plain` (4-byte read) | `text/plain` | `application/octet-stream` |
| cache extent field 0 -> clamp 16384; sqlite header file | `application/vnd.sqlite3` | `application/vnd.sqlite3` | `application/vnd.sqlite3` |
| two caches: patched extent 8 + host extent 18730 -> max -> clamp 16384; sqlite header | `application/vnd.sqlite3` | `application/vnd.sqlite3` (both dir orders) | `application/vnd.sqlite3` |
| guard: `d1` extent 8, `d2` header word24 = 5 (misaligned, `OUT_OF_BOUNDS` skip) (frozen `uncertain-14`) | `text/plain` | `text/plain` | `application/octet-stream` |
| `d2` alone (bad guard cache only) | `application/octet-stream` | `application/octet-stream` | same |
| text db nested indents `0>0=AB`, `1>6=CD` -> extent 9; file `ABxxxxCDyy` | `app/x-nest` | `app/x-nest` | `app/x-nest` |

Frozen extent cases (`uncertain-10...14`) scored individually: the base draft fails
`uncertain-10-text-extent-small` (octet-stream vs text/plain), `uncertain-13-cache-extent-small`
(octet-stream vs text/plain) and `uncertain-14-cache-guard-badcache` (octet-stream vs text/plain);
the final candidate passes all five. A guard-removal model would read `d2`'s `u32@(5+4)=9998336`,
clamp to 16384 and answer octet-stream on `uncertain-14`, so that case discriminates the guard.
The 8/4-byte vs 16384-byte flip is therefore demonstrated live for both database modes, and the
constant-cap model is observably killed by the frozen case file.

## 5. Two-stage-stat attack (task 5)

22 probes, gio vs final v2, same env/flags, **0 diffs**:

| probe | gio rc | final v2 rc |
|---|---|---|
| self loop `l -> l`, follow / mutual `a<->b`, follow / `b`, nofollow | `inode/symlink` 0 | same |
| dangling `-> nope`, follow / nofollow | `inode/symlink` 0 | same |
| symlink to fifo, to dir (follow), to dir (nofollow), to `/dev/null`, to file (follow/nofollow) | `inode/fifo`, `inode/directory`, `inode/symlink`, `inode/chardevice`, `text/plain`, `inode/symlink` 0 | same |
| child of a `chmod 000` dir, untyped name / `*.txt` name | `application/octet-stream` 0 / `text/plain` 0 | same |
| hardlink first/second name | `text/plain` 0 | same |
| trailing slash on a regular file (`t.txt/`) | `text/plain` 0 (local path printed without the slash) | `text/plain` 0 |
| `t.txt/x` (ENOTDIR inside the path) | rc 2, no attribute | `ERROR stat` rc 2 |
| missing path | rc 2, no attribute | `ERROR stat` rc 2 |
| directory named `*.png`, socket, fifo | `inode/directory`, `inode/socket`, `inode/fifo` 0 | same |

Normalisation edges the final `_norm` handles like the CLI (all matched): `.`, `..`, `./t.txt`,
`sub/../t.txt`, `t.txt/.`, `t.txt/..`, `sub/./a.txt`, `//`, `///`, empty argument (all dir/type
answers equal). The intermediate pin `e0086e3f` only trimmed a trailing slash and diverged on
`t.txt/.` (`ERROR` vs gio `text/plain`); the final `posixpath.normpath(...).rstrip("/") or "/"`
closes that.

Two defects existed in the *earlier* pins and are fixed in the final bytes (recorded because the
seat asks for them):

* `6454d3db...` refused an `lstat` `EACCES` (`ERROR stat` rc 2) where gio answers the name-only type
  (rc 0); final returns `None` from the stat branch and answers `application/octet-stream` /
  `text/plain` exactly like gio.
* `6454d3db...` passed the raw path to `lstat`, so a trailing slash on a file was `ENOTDIR` (`ERROR`)
  where gio answers the file; final trims/normalises first.

**Measured contradiction in the claim text.** The seat brief says "a trailing-slash-to-file (gio
error)" and declaration rule 7 says an `ENOTDIR` "(a trailing slash on a file)" is refused
"matching `gio info`". The oracle does *not* error: `gio info -a standard::content-type t.txt/`
prints `local path: .../t.txt` and `standard::content-type: text/plain`, rc 0 (also `/dev/null/` ->
`inode/chardevice`, `link/ -n` -> `inode/symlink`). The shipped tool now matches that behaviour.
The declaration sentence must be corrected at the freeze (finding F1).

## 6. Predicate clauses (i)-(vii): can I falsify each?

Falsification method: run the same surface the counter scores, at the final pins, and look for one
counterexample. The counter itself was not run end-to-end (its pins are not frozen), so each clause
below names the independent evidence.

(i) **Every frozen case exact, `classes == 15/15`.** Falsifier: any candidate/oracle mismatch or a
class count below 8. Measured 201/201 paths exact over 157 cases, 15/15 classes, minimum 9 cases.
Cannot falsify. Structural conjunct (empty `PATH`, launcher, allowlist): the current counter v2's
`static_check(candidate)` returns `[]` and `validate_cases(final cases)` returns 0 errors; the
candidate imports only `argparse errno importlib.util json os posixpath stat sys` plus
selftest-local `struct tempfile contextlib io`, and has exactly one `spec_from_file_location`
helper. (A counter that lacks `posixpath`/`contextlib` in its allowlist would flag it -- see F4.)

(ii) **Every frozen mutant killed, `class_kills == 15/15`.** The frozen mutant file is not present
at review time (only the w1 `filetype-mutants-r97.json`, anchored to the base draft). I built and
ran 13 mutants of my own on the final candidate over all 157 cases, one single-occurrence
`find`/`replace` each: constant cache extent, text-extent range drop, clamp removal, guard removal,
dir/chr branch swaps, nofollow inversion, zerosize drop, socket drop, fast-sniffing, read-failure
sniff-on-empty, no normalisation, EACCES refusal. Result: see section 7 -- every one is killed by a frozen
case (the last two by the new `dir-11/12`, `sym-11/12`, `readerr-11/12` cases). So the examined
surfaces are killable; the clause cannot be falsified without the frozen set, and the frozen set
must keep at least one mutant per class for `class_kills == 15/15` (the w1 draft does).

(iii) **Every fresh case exact, >= 120.** Ran the frozen generator
(`filetype-fresh-r97.py`, `c3143775...`, `--seed a11ce97 --count 120`): 120 cases, 432 paths,
`label_rederived=432/432`, `candidate=432/432`, 15 classes, db modes text 49 / cache 35 / none 36.
Cannot falsify. Caveat: every fresh database is a copy of the host db (extent 18730 -> clamp
16384), so this leg cannot discriminate rule 4; the extent evidence is the frozen `uncertain-10...14`
cases (F3).

(iv) **Every host path exact, >= 1500.** Two random samples of the frozen 11834-path list
(seed 97: 150 paths; seed 971: 300 paths) over `/usr/share` cache mode with the tool and gio on the
same db: 450/450 exact, 0 diffs. The full 11834-path leg is the counter's; I cannot falsify the
sample. The host list contains no trailing-slash, `.`/`..`, double-slash or non-ASCII paths
(measured), so it cannot exercise the normalisation/EACCES fixes; only the frozen cases can.

(v) **Oracle is the installed gio; frozen labels produced by it.** `/usr/bin/gio` sha256 is
`d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462` and `--version` is 2.90.1; my
independent re-derivation of all 201 frozen labels with that binary matched 201/201. Cannot falsify.

(vi) **Controls stay behind.** Name-only: 67/201 < 201 (and 13/36 < 36) -- behind. Memoriser, keyed
as the current predicate says by `(kind, basename, content sha256, symlink target)` and built from
the frozen labels: on my 120-case fresh seed it hits 80 of 432 paths and is correct on all 80
(`80/432 = 18.5 %`, strictly fewer than the fresh total; not zero, because the fresh family reuses
fixed device names/text fixtures -- this reproduces the declaration's `80/426` hit count on its own
seed). Naive extension table and the library-asking forgery are the counter's own control and audit;
not runnable from this seat without the frozen pins. I cannot falsify the name-only/memoriser parts;
the forgery part is untested here.

(vii) **Candidate `--selftest` green, `checks >= 20`.** Final bytes: `checks=40 failed=0` rc 0 in the
sibling layout, `checks=38 failed=0` rc 0 as a lone copy (the two sibling-dependent checks are
skipped by design). Cannot falsify.

## 7. Own-mutant probes (evidence for clause ii)

Built with one exact-occurrence replacement each on the final candidate (mutant copies placed beside
the three sibling tools so the pinned loads resolve), run over the 201 frozen paths:

13/13 killed; the first differing frozen path is listed (mutant copy beside the three siblings).

| mutant (single replacement) | first failing path | label vs mutant |
|---|---|---|
| cache extent -> constant 16384 | uncertain-13-cache-extent-small | text/plain vs application/octet-stream |
| text extent drops `range` | uncertain-11-text-extent-range | app/x-rangehit vs text/plain |
| clamp removed (`return n`) | empty-07-empty-none-db | application/octet-stream vs application/x-zerosize |
| OUT_OF_BOUNDS guard removed | uncertain-14-cache-guard-badcache | text/plain vs application/octet-stream |
| dir branch -> symlink | dir-01-plain-subdir | inode/directory vs inode/symlink |
| chr branch -> block | dir-12-trailing-slash-chardev (`/dev/null/`) | inode/chardevice vs inode/blockdevice |
| nofollow inverted | zero-10-proc-self-status | application/x-zerosize vs inode/symlink |
| size-0 branch dropped | zero-01-empty-png-name | application/x-zerosize vs image/png |
| socket branch dropped | sock-01-plain | inode/socket vs application/octet-stream |
| fast sniffs | empty-05-text-fast | application/octet-stream vs text/plain |
| read failure sniffs empty data | readerr-01-000-uncertain-png | application/octet-stream vs application/x-zerosize |
| `_norm` -> identity | dir-11-trailing-slash-file (`a.txt/`) | text/plain vs ERROR |
| EACCES guard removed | readerr-11-dir-unreadable (`sub/note.txt`) | application/octet-stream vs ERROR |

The last two are exactly the behaviours added in the final case file (trailing slash, EACCES); the
earlier 150-case file carried neither shape (no non-directory path ending `/`, no `dir-unreadable`
type - inspected), so those two mutants could not have been killed by it.

## Findings (severity order)

**F1 (medium, claim text -- must be fixed at the freeze).** Declaration rule 7's parenthetical "a
missing path or an `ENOTDIR` (a trailing slash on a file) prints ... `ERROR stat` ... matching
`gio info`, and no case scores the refused path" is false in two ways: gio does not refuse a
trailing slash (it answers the file: `text/plain`, rc 0, after trimming/normalising), and
`readerr-13-missing` does score a refused path (`ERROR`). Rule 7 also contradicts the declaration's
own named limits, which correctly say "a trailing slash is stripped from the argument (the `gio`
CLI does the same; measured)". ENOTDIR *inside* a path (`t.txt/x`) is the only ENOTDIR that refuses,
and both gio and the tool refuse it (rc 2). Suggested sentence: "a trailing run of `/` and `.`/`..`
segments are normalised away before the query (the CLI/GFile behaviour); a path that still cannot be
stat'ed (missing, ENOTDIR inside the path) prints `ERROR stat` and exits 2, matching gio".

**F2 (medium, contract text -- must be fixed at the freeze).** The final case file extends Shared
contract 3 with two path types (`dir-unreadable`, `missing`) and one `["ERROR"]` label. The current
counter v2 supports them (`validate_cases` = 0 errors; docstring names the types), but the Shared
contract 3 text (and any freeze note that restates the case schema) still enumerates only the old
eight types, and rule 7's "no case scores the refused path" is no longer true
(`readerr-13-missing` does score it). The contract text and the freeze note must carry the
extension so the declared schema matches the frozen file.

**F3 (low, coverage).** Rule 4's extent is not reachable from the fresh leg: the generator copies
the host database, whose extent is 18730 -> clamp 16384 in every mode; only `uncertain-10...14`
discriminate the rule. Likewise the host list has no EACCES/trailing-slash/normalisation paths.
The frozen cases are therefore load-bearing for the last three fixes; a freeze that drops
`readerr-11/12`, `readerr-13`, `dir-11/12` or `sym-11/12` would make those behaviours unscored.

**F4 (low, counter dependency).** The final candidate imports `posixpath` (production) and
`contextlib` (selftest-only). The w1 counter's `_OK_IMPORTS` did not list them and `static_check`
returned `['import:posixpath:69', 'import:contextlib:569']` on the candidate; the counter v2 now
lists both and returns `[]`. The frozen counter must keep that allowlist, or clause (i)'s structural
conjunct fails a correct candidate. (Counter v2 last checked `745a341e...`; it may still move -- the two earlier v2 pins I checked also returned `[]`.)

**F5 (informational -- closed).** The two defects found in the earlier pins (`6454d3db...` refused an
`lstat` EACCES; `e0086e3f...` trimmed slashes only and diverged on `t.txt/.`) are fixed in the final
bytes; section 5 shows the final candidate agreeing with the oracle on every probe, including the new
frozen cases.

## Residual risk and verification gaps

* Full host leg not run (450 of 11834 paths sampled, 0 diffs); the counter's own leg remains the
  proof, and the sampled paths can change on disk between review and measurement.
* The frozen mutant file and the counter's end-to-end run are absent at review time; my 13 mutants
  and `static_check`/`validate_cases` are independent evidence, not the counted predicate.
* The audit launcher / empty-`PATH` execution was not exercised by me; only `static_check` was.
* The fresh leg cannot see the extent rule (F3); it also cannot see EACCES or trailing-slash paths
  (the generator drops paths whose oracle run refuses, and it does not write `dir-unreadable`).
* `_norm` is lexical (`posixpath.normpath`); it matched gio on every probed shape, but a symlink
  traversal combined with `..` was not separately measured (GFile also normalises lexically, and the
  frozen/host/fresh paths carry none).
* The `dir-unreadable` labels assume a non-root measurement uid; running the counter as root would
  turn the 000-dir cases into readable ones (all other hosts facts unchanged).
* The `ERROR` label and the new path types depend on the counter v2 extensions; a counter pinned
  to the w1 bytes would SETUP_ERROR on the final case file.

## Checks for the main agent / L1

```
python3 -I build/mado-filetype.v2.py --selftest              # checks=40 failed=0, rc 0
sha256sum build/mado-filetype.v2.py controls/filetype-cases-v2.json   # da6af7a0... / fc710b94...
```

The case/oracle/candidate figures were produced by a scratch-only harness (deleted); the L1's
frozen counting command is the authoritative replay. The receipt keeps the exact commands and
output shapes.

Report: `.ufo/waves/round-97/w1b/R97MReviewC1b.md`
