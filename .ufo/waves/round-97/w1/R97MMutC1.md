# R97MMutC1 - C1 mutant population and kill evidence (round 97, w1)

Seat: mutation tester for C1. Inputs read (read-only):

- candidate draft `.ufo/waves/round-97/build/mado-filetype.py`, sha256 `e68150b553ee7b93550fabb0a57221b51a4fc71ec43da7c9dff71d318c7e070c`;
- C1 case set `.ufo/waves/round-97/controls/filetype-cases-r97.json`, sha256 `c5630cd0ccafa850435f9810d9366d2bff316efb6d97cd87c9d97667064ebbd2`
  (140 cases, 15 classes, 9-10 cases each; ids/classes/modes/attrs/labels frozen by the case owner).

Deliverable: `.ufo/waves/round-97/controls/filetype-mutants-r97.json`, strict counter schema
`{"version":1,"tool":"tools/mado-filetype.py","mutants":[{"id","class","find","replace"}]}`, sha256
`39292ea9184d0aed4d32775ebbc79e8d586ba5b84b739fc9c2dc9db045442ae7`; the counter draft's own `validate_mutants(<file>, <candidate bytes>)` returns an empty error
list on it. **79 counted mutants, 79 killed, 15/15 classes.**

All 79 `find`s sit before the first literal `def selftest(` (checked: zero anchors inside the selftest
block), so a gate that cuts at that line sees every anchor; the counter's validator accepts exactly
`id`/`class`/`find`/`replace`, so the seat's `expect:"kill"` is carried by the measured 79/79 kill
evidence below rather than by a JSON key.

## Method

1. One literal `find` -> `replace` per mutant over the candidate's whole bytes. The emitter asserts:
   `find` occurs exactly once, is unique across mutants, differs from `replace`, and the id starts
   with its class - the counter's SETUP_ERROR anchors.
2. The sweep runs in the counter's own shape: a launcher installs an audit hook that refuses any
   `open` outside {the tool tree, the case root, the Python stdlib roots, /dev/null} and exits 97;
   the case env is mapped to the tool flags (`--home`, `--data-home[-unset]`, `--data-dirs[-unset]`,
   `--follow|--nofollow`, `--fast`) and the tool runs with `cwd` = case root. Sockets stay bound while
   the case runs; unreadable fixtures are chmod 000.
3. Scoring per case mirrors the counter: parsed lines in path order (type, `attr=`, `mode=`, `path=`
   esc-reversibly), `MADO_FILETYPE_DIRS: db=` equal to the mode derived from the case files, line
   count/missing lines, and exit inside {0,2} (outside = crash). No mutant in the file alters the
   path field, and no case carries an ERROR label, so the rc-only and path-only clauses are not
   exercised by the counted set (see the dropped list).
4. **Kill** = >=1 frozen case scored wrong; a mutant that only crashes is `crashed_not_killed`, never
   a kill. The sweep records **every** wrong case per mutant (not only the first), which is what the
   counter's `class_kills` census reads.
5. Baseline: the pristine candidate under the same launcher answers `140/140` cases exactly (0 case(s)
   not ok). The 14 rewritten host-db cases now carry case-local mime trees, so no host path is read.
6. Restoration: the build file was never opened for writing; all mutation happened on scratch copies,
   and `sha256sum` of the build file before and after is `e68150b553ee7b93550fabb0a57221b51a4fc71ec43da7c9dff71d318c7e070c`.

## Class census

`mutants` is the counted population by mutant class; `kills` is how many members killed. The
`class_kills` column is the counter's census: the number of counted mutants with at least one wrong
case in that class (a mutant counts once per class, however many of its cases are wrong).

| class | mutants | kills | class_kills |
|---|---|---|---|
| dir | 6 | 6 | 35 |
| chr | 4 | 4 | 15 |
| blk | 4 | 4 | 14 |
| fifo | 4 | 4 | 17 |
| sock | 3 | 3 | 23 |
| zero | 9 | 9 | 23 |
| empty | 1 | 1 | 35 |
| sym | 8 | 8 | 51 |
| brok | 3 | 3 | 20 |
| nofollow | 4 | 4 | 45 |
| follow | 4 | 4 | 59 |
| certain | 6 | 6 | 32 |
| uncertain | 12 | 12 | 32 |
| fast | 6 | 6 | 31 |
| readerr | 5 | 5 | 36 |
| **total** | **79** | **79** | **468** |

Every one of the 15 class names has >=1 counted mutant and >=1 kill; the counter's `class_kills`
(a class counts once per mutant with >=1 wrong case in it) reaches **15/15**.

## Kill evidence

`probe` is the same mutant over a 54-case scratch supplement built for corners the frozen set does
not carry (clamp boundary at 16384, name-certain symlink, nested basename, unreadable file with name
types, a space in a path). `wrong` is the measured first wrong case with its field and expected value.

| id | class | anchor | first wrong (frozen) | probe |
|---|---|---|---|---|
| blk-01-wrong-chr | blk | `return "inode/blockdevice"` | blk-01-dev-sda:wrong:type | killed |
| blk-02-drop-branch | blk | `if stat.S_ISBLK(mode): (+1 lines)` | blk-05-dev-sda-fast:wrong:type | killed |
| blk-03-as-chr | blk | `if stat.S_ISBLK(mode):` | blk-05-dev-sda-fast:wrong:type | killed |
| blk-04-swap-bodies | blk | `if stat.S_ISCHR(mode): (+3 lines)` | chr-01-dev-null:wrong:type | killed |
| brok-01-broken-directory | brok | `st = os.stat(path) (+2 lines)` | brok-01-dangling-follow:wrong:type | killed |
| brok-02-broken-raises | brok | `except OSError as e: (+2 lines)` | brok-01-dangling-follow:wrong:type | killed |
| brok-03-broken-octet | brok | `except OSError as e: (+1 lines)` | brok-01-dangling-follow:wrong:type | killed |
| certain-01-guess-no-name | certain | `return _guess(self.sniffer, base, data, len(data))` | certain-09-certain-host-db:wrong:type | killed |
| certain-02-gate-suffix | certain | `if not res["uncertain"]: (+1 lines)` | dir-02-dir-with-name-type:wrong:type | killed |
| certain-03-fast-uncertain-field | certain | `return self.name_only(base)["type"]` | empty-07-text-fast:wrong:type | killed |
| certain-05-name-only-sniffer | certain | `def name_only(self, basename): (+1 lines)` | dir-01-plain-subdir:wrong:type | killed |
| certain-08-type-suffix | certain | `print(f"MADO_FILETYPE: {x['type']} attr={'fast' if a.fast else 'full'} "` | dir-01-plain-subdir:wrong:type | killed |
| certain-09-type-upper | certain | `results.append({"path": _esc(pb), "type": t})` | dir-01-plain-subdir:wrong:type | killed |
| chr-01-wrong-block | chr | `return "inode/chardevice"` | chr-01-dev-null:wrong:type | killed |
| chr-02-drop-branch | chr | `if stat.S_ISCHR(mode): (+1 lines)` | chr-01-dev-null:wrong:type | killed |
| chr-03-as-reg | chr | `if stat.S_ISCHR(mode):` | dir-01-plain-subdir:wrong:type | killed |
| chr-04-always | chr | `if stat.S_ISCHR(mode): (+2 lines)` | dir-01-plain-subdir:wrong:type | killed |
| dir-01-wrong-symlink | dir | `if stat.S_ISDIR(mode): (+1 lines)` | dir-01-plain-subdir:wrong:type | killed |
| dir-02-drop-branch | dir | `if stat.S_ISDIR(mode): (+1 lines)` | dir-01-plain-subdir:wrong:type | killed |
| dir-03-as-reg | dir | `if stat.S_ISDIR(mode):` | dir-01-plain-subdir:wrong:type | killed |
| dir-04-always | dir | `return "inode/directory" (+1 lines)` | dir-01-plain-subdir:wrong:type | killed |
| dir-05-name-before-branch | dir | `if fixed is not None: (+1 lines)` | dir-02-dir-with-name-type:wrong:type | killed |
| dir-06-branch-only-fast | dir | `if fixed is not None: (+2 lines)` | dir-01-plain-subdir:wrong:type | killed |
| empty-01-branch-disabled | empty | `return "inode/fifo" (+2 lines)` | zero-01-empty-png:wrong:type | killed |
| fast-01-gate-false | fast | `if fast:` | empty-07-text-fast:wrong:type | killed |
| fast-02-gate-invert | fast | `base = self.name_base(os.fsencode(path)) (+1 lines)` | dir-01-plain-subdir:wrong:type | killed |
| fast-03-answer-const-full | fast | `t = ft.answer(p, a.follow, a.fast) (+1 lines)` | empty-07-text-fast:wrong:type | killed |
| fast-04-argparse-store-false | fast | `ap.add_argument("--fast", action="store_true", help="standard::fast-c...` | dir-01-plain-subdir:wrong:echo | killed |
| fast-05-attr-invert | fast | `attr={'fast' if a.fast else 'full'}` | dir-01-plain-subdir:wrong:echo | killed |
| fast-06-types-first-fallback | fast | `if fast: (+2 lines)` | empty-07-text-fast:wrong:type | killed |
| fifo-01-wrong-sock | fifo | `return "inode/fifo"` | fifo-01-plain:wrong:type | killed |
| fifo-02-reg-or-fifo | fifo | `if stat.S_ISFIFO(mode):` | dir-01-plain-subdir:wrong:type | killed |
| fifo-03-zero-size-fifo | fifo | `if stat.S_ISFIFO(mode): (+1 lines)` | sock-01-plain:wrong:type | killed |
| fifo-04-sock-or-fifo | fifo | `if stat.S_ISFIFO(mode): (+2 lines)` | sock-01-plain:wrong:type | killed |
| follow-01-answer-false | follow | `fixed = _stat_branch(path, follow) (+2 lines)` | sym-01-link-to-file-follow:wrong:type | killed |
| follow-02-symlink-and-follow | follow | `if stat.S_ISLNK(mode):` | sym-02-link-to-file-nofollow:wrong:type | killed |
| follow-03-symlink-invert | follow | `mode = st.st_mode (+1 lines)` | dir-03-nested-dirs:wrong:type | killed |
| follow-04-follow-default-false | follow | `ap.add_argument("--follow", dest="follow", action="store_true", defau...` | dir-01-plain-subdir:wrong:echo | killed |
| nofollow-01-answer-const-follow | nofollow | `t = ft.answer(p, a.follow, a.fast)` | sym-02-link-to-file-nofollow:wrong:type | killed |
| nofollow-02-answer-invert | nofollow | `t = ft.answer(p, a.follow, a.fast) (+2 lines)` | sym-01-link-to-file-follow:wrong:type | killed |
| nofollow-03-argparse-action | nofollow | `ap.add_argument("--nofollow", dest="follow", action="store_false")` | dir-03-nested-dirs:wrong:echo | killed |
| nofollow-04-follow-default | nofollow | `ap.add_argument("--follow", dest="follow", action="store_true", defau... (+1 lines)` | dir-01-plain-subdir:wrong:echo | killed |
| readerr-01-none-octet | readerr | `if data is None: (+1 lines)` | readerr-04-000-multi-foo:wrong:type | killed |
| readerr-02-none-suffix | readerr | `data = _read_sniff(path, _clamp(self.max_buffer_extents)) (+2 lines)` | readerr-01-000-uncertain-png:wrong:type | killed |
| readerr-03-open-nofollow | readerr | `fd = os.open(path, os.O_RDONLY \| os.O_CLOEXEC)` | sym-01-link-to-file-follow:wrong:type | killed |
| readerr-04-open-empty-bytes | readerr | `except OSError: (+2 lines)` | readerr-01-000-uncertain-png:wrong:type | killed |
| readerr-05-open-empty-or | readerr | `data = _read_sniff(path, _clamp(self.max_buffer_extents)) (+1 lines)` | readerr-01-000-uncertain-png:wrong:type | killed |
| sock-01-wrong-fifo | sock | `return "inode/socket"` | sock-01-plain:wrong:type | killed |
| sock-02-drop-branch | sock | `if stat.S_ISSOCK(mode): (+1 lines)` | sock-01-plain:wrong:type | killed |
| sock-03-as-reg | sock | `if stat.S_ISSOCK(mode):` | dir-01-plain-subdir:wrong:type | killed |
| sym-01-nofollow-invert | sym | `if not follow: (+3 lines)` | sym-01-link-to-file-follow:wrong:type | killed |
| sym-02-nofollow-false | sym | `if stat.S_ISLNK(mode): (+1 lines)` | sym-02-link-to-file-nofollow:wrong:type | killed |
| sym-03-nofollow-true | sym | `if not follow: (+1 lines)` | sym-01-link-to-file-follow:wrong:type | killed |
| sym-04-stat-to-lstat | sym | `st = os.stat(path)` | sym-03-link-to-dir-follow:wrong:type | killed |
| sym-05-mode-relstat | sym | `mode = st.st_mode (+1 lines)` | sym-03-link-to-dir-follow:wrong:type | killed |
| sym-06-basename-realpath | sym | `base = self.name_base(os.fsencode(path)) (+2 lines)` | sym-05-link-fast:wrong:type | killed |
| sym-07-lstat-to-stat | sym | `st = os.lstat(path) (+1 lines)` | sym-02-link-to-file-nofollow:wrong:type | killed |
| sym-08-answer-follow-true | sym | `fixed = _stat_branch(path, follow) (+1 lines)` | sym-02-link-to-file-nofollow:wrong:type | killed |
| uncertain-01-gate-invert | uncertain | `res = self.name_only(base) (+1 lines)` | dir-01-plain-subdir:wrong:type | killed |
| uncertain-02-gate-true | uncertain | `if not res["uncertain"]: (+2 lines)` | dir-01-plain-subdir:wrong:type | killed |
| uncertain-03-read-zero | uncertain | `data = _read_sniff(path, _clamp(self.max_buffer_extents))` | dir-01-plain-subdir:wrong:type | killed |
| uncertain-04-empty-data | uncertain | `return res["type"] (+1 lines)` | dir-01-plain-subdir:wrong:type | killed |
| uncertain-05-types-first | uncertain | `data = _read_sniff(path, _clamp(self.max_buffer_extents)) (+3 lines)` | uncertain-06-multi-foo-png-hi:wrong:type | killed |
| uncertain-06-guess-uncertain-field | uncertain | `return sniffer.guess(name_bytes, data)["type"]` | dir-01-plain-subdir:wrong:type | killed |
| uncertain-07-guess-empty | uncertain | `if data is None: (+2 lines)` | dir-01-plain-subdir:wrong:type | killed |
| uncertain-12-read-no-directory | uncertain | `try: (+1 lines)` | dir-01-plain-subdir:wrong:type | killed |
| uncertain-13-fixed-or-octet | uncertain | `fixed = _stat_branch(path, follow)` | dir-01-plain-subdir:wrong:type | killed |
| uncertain-14-basename-split-first | uncertain | `self.name_base = mg.g_path_get_basename` | dir-02-dir-with-name-type:wrong:type | killed |
| uncertain-15-name-only-octet | uncertain | `return self.resolver.guess(basename)` | dir-01-plain-subdir:wrong:type | killed |
| uncertain-16-fast-const-true | uncertain | `if fast: (+1 lines)` | empty-07-text-fast:wrong:type | killed |
| zero-01-wrong-empty | zero | `return "application/x-zerosize"` | zero-01-empty-png:wrong:type | killed |
| zero-02-drop-size-guard | zero | `if stat.S_ISREG(mode) and st.st_size == 0:` | dir-01-plain-subdir:wrong:type | killed |
| zero-03-size-ne | zero | `if stat.S_ISREG(mode) and st.st_size == 0: (+1 lines)` | dir-01-plain-subdir:wrong:type | killed |
| zero-04-size-one | zero | `st.st_size == 0: (+1 lines)` | zero-01-empty-png:wrong:type | killed |
| zero-05-drop-reg-guard | zero | `if stat.S_ISREG(mode) and st.st_size == 0: (+2 lines)` | sock-01-plain:wrong:type | killed |
| zero-06-size-negative | zero | `if stat.S_ISREG(mode) and st.st_size == 0: (+3 lines)` | zero-01-empty-png:wrong:type | killed |
| zero-07-reg-or-size | zero | `return "inode/fifo" (+1 lines)` | dir-01-plain-subdir:wrong:type | killed |
| zero-08-branch-fifo-type | zero | `if stat.S_ISREG(mode) and st.st_size == 0: (+4 lines)` | zero-01-empty-png:wrong:type | killed |
| zero-09-truncate-results | zero | `for x in results:` | dir-01-plain-subdir:wrong:lines | killed |

## Not observable / equivalent (dropped before the freeze)

The counter schema has no representation for these (`version`, `tool`, `mutants` only; a frozen
non-killer fails the wave), so they are **not** in the file; each is recorded here with its argument
and the measured leg. Totals: **13 dropped** - 5 equivalent, 8 not observable/crash-only.

| id | class | change | measured | why it cannot kill |
|---|---|---|---|---|
| dir-08-dirs-host-default | dir | `dirs = mg.xdgmime_dirs(dh, home, dd) -> mg.xdgmime_dirs(None, home, None)` | crashed_not_killed, measured 140/140 (probe: killed) | ignoring the case's data roots sends every case to the host database; /usr/share is outside the allow for a case whose env no longer declares it, so the resolver's open is denied and exit 97 occurs before any path is answered (sweep: 140 new-crash cases, 0 wrong). |
| dir-09-dd-ignored | dir | `dd = ... env.get("XDG_DATA_DIRS") -> dd = None` | crashed_not_killed, measured 140/140 (probe: killed) | same mechanism as dir-08: the tool resolves the host roots and the audit denies the host cache open (sweep: 140 new-crash cases, 0 wrong). |
| empty-02-size-lt-one | empty | `st.st_size == 0: ... "application/x-zerosize" -> st.st_size < 1: ...` | equivalent (probe: survived) | st_size is a non-negative count, so `st_size < 1` holds exactly when `st_size == 0`; survives all 54 probe cases and all 140 frozen cases with no byte of output differing. |
| dir-07-env-empty | dir | `env = os.environ -> env = {}` | equivalent under the scored CLI (probe: survived) | every scored run passes --home/--data-home[-unset]/--data-dirs[-unset] explicitly (the counter's tool_flags and my harness both do), so the os.environ fallback is never consulted; measured survivor. |
| certain-04-basename-upper | certain | `base = self.name_base(os.fsencode(path)) -> same .upper()` | equivalent (probe: survived) | GLib glob matching is case-insensitive (round 94's model lowercases the name before matching), so upper-casing the basename preserves the name-type set in every database; measured survivor. |
| certain-07-json-raw-path | certain | `json.dumps(results) -> json.dumps([{path,type} for r in results])` | equivalent (probe: survived) | the rebuilt list has the same dicts in the same order, so stdout is byte-identical; measured survivor. |
| uncertain-08-clamp-lower | uncertain | `return 16384 if n == 0 or n > 16384 else n -> return 16383 if ... else n` | equivalent under this candidate (probe: survived) | the candidate fixes max_buffer_extents at 16384, so the only value _clamp ever sees is 16384 and the mutated else-branch returns it unchanged. A cap-lowering mutant needs `else min(n, 16383)` plus a case whose magic match ends at 16384. |
| uncertain-09-read-minus-one | uncertain | `return os.read(fd, n) -> return os.read(fd, n - 1)` | not observable on the frozen cases (probe: killed) | no frozen case has a magic match beyond offset 0 (the two case-local magic trees are `0>0=`, and the copied host magic's highest offset is 4096 with no fixture byte pattern there), so 16383 and 16384 read the same answer; my scratch boundary fixture kills it, the frozen set does not carry one. |
| uncertain-10-read-plus-one | uncertain | `return os.read(fd, n) -> return os.read(fd, n + 1)` | not observable on the frozen cases (probe: killed) | the extra byte only matters when a match ends at 16385; no frozen fixture has a match above offset 0. |
| uncertain-11-extents-small | uncertain | `self.max_buffer_extents = 16384 -> 8192` | not observable on the frozen cases (probe: killed) | the longest match any frozen fixture can trigger ends at byte 15, so 8192 and 16384 answer identically. |
| uncertain-20-error-answer-type | uncertain | `ERROR stat line -> a type line` | not observable on the frozen cases (probe: killed) | the 140-case file has no ERROR-labelled case (the declaration puts stat failure outside the surface), so the branch is never entered and the output is identical to pristine. |
| uncertain-21-error-no-rc | uncertain | `rc = 2 -> rc = 0` | not observable on the frozen cases (probe: killed) | no ERROR case reaches the branch; the counter scores rc only as 2-when-an-ERROR-label / 0 otherwise, so with no ERROR case the mutated assignment is dead code. |
| certain-06-raw-path | certain | `results.append({"path": _esc(pb), ...}) -> {"path": p, ...}` | not observable on the frozen cases (probe: killed) | the counter compares path= esc-reversibly, but every one of the 140 cases' paths is printable ASCII without a backslash, where esc() is the identity, so raw and escaped spellings are the same string. A case whose scored path carries a space, a backslash or a byte outside 0x21..0x7e would make this mutant kill; the frozen set has none (recommendation below). |

## Findings handed to the wave

1. **The declaration's clamp sentence has no observable mutant on this candidate.** `_clamp` is the
   identity because `max_buffer_extents` is the constant 16384; read-length mutants survive every
   frozen case because no fixture triggers a magic match above offset 0. A case whose magic value
   ends at 16384 (offset 16382, 2 bytes) would make them observable - measured in scratch: a cache
   magic at 16380 matches, one at 16383 does not. Recommendation to the case owner; not a change I
   made.
2. **The ERROR surface has no case.** All 140 labels are types; the declaration's `ERROR stat`/exit-2
   path is unscored, so an ERROR-branch mutant has no frozen case to break (and `rc = 2 -> 0` never
   executes). The declared error branch therefore carries no counted mutant.
3. **Output escaping has no case.** The counter compares `path=` esc-reversibly, but every frozen
   path is printable ASCII without a backslash (esc() = identity), so the esc->raw mutant is
   unobservable; a case whose scored path carries a space, backslash or byte outside 0x21..0x7e
   would make it kill. Recommendation, not a change I made.
4. **Audit-shape exclusions and one near miss.** Two data-root defects (dir-08/dir-09) resolve the
   host database and are crash-only under the audit launcher (measured 140/140 new-crash, 0 wrong),
   so they stay out. The two block-branch defects look equally crash-only on the sniffing cases, but
   the frozen `--fast` block cases (blk-05, blk-06) answer name-only without opening the device, so
   they do produce parsed wrong answers and are counted; their other block cases crash, which the
   counter ignores once a wrong case exists. All 79 counted mutants therefore kill by a parsed wrong
   answer inside the allowlist, not by crash.
5. **Draft revisions observed while anchoring.** `15ddaf03...` crashed on every text/none database
   (`name_only` used `names.lookup`, a list) and could not print `db=none`; the refrozen
   `e68150b5...` fixed the resolver use and mode reporting. All anchors and every measurement here
   are against `e68150b5...`, and the pristine run is green 140/140.

## Files

- `controls/filetype-mutants-r97.json` - the counted population (this seat's write scope).
- `w1/R97MMutC1.md` - this report.
- Scratch (deleted before yield): `$HYAKU_SCRATCH/mado-r97/R97MMutC1` held the emitter, the
  audit-shape sweep, the 54-case probe supplement and the measured JSON this report reads.

