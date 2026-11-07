# R97MReviewC1 - adversarial review of C1 (the content type GIO reports for a path)

Seat R97MReviewC1, round 97, wave w1. Reviewer only: I edited no candidate, no case file, no
counter, no sibling lane module. Everything below is pinned to the shas named in section 1 and
was produced from scratch roots under /fast/scratch/hyaku/mado-r97/R97MReviewC1 (deleted before
yield). The two paths I wrote are this report and
.ufo/waves/round-97/receipts/review-c1-r97.txt.

The assignment: re-derive the oracle on a sample of the frozen cases, run the candidate on the
same paths, score the cheapest no-work control myself, probe the attack surface named in the
declaration, and state clause by clause whether PRED-C1-r97-v1 (i)-(vii) can be falsified.

**Headline.** At the latest pins the candidate is exact on every scored leg I can measure
(196/196 frozen case paths, 1288/1288 fresh paths over three seeds, 11837/11837 host paths), its
selftest is green, and every frozen label I re-derived came from the pinned gio. Two ship-blockers
remain outside the scored legs: the structural conjunct is red under the only implemented allowlist
(F11) and the shipped host list carries the password-manager tree, so the host leg reads credential
bytes and must not run as shipped (F12). The defects are
in the *claims* and in paths outside the scored sets: the declaration sentences on symlink loops
(F1) and on "cannot be stat'ed" (F4) are false of the oracle, the "memoriser 0 on the fresh leg"
control is false or vacuous (F2), GFile's path normalization is not modelled (F3), and the selftest
pads its check count (F5). The counting command cannot run at all yet: the C1 counter, the
mutant set, the forgery and the -frozen copies do not exist (section 4, clause (ii)).

## 1. Pinned inputs (what I attacked)

| artifact | sha256 | measured |
|---|---|---|
| `.ufo/waves/round-97/build/mado-filetype.py` (C1 candidate) | `e68150b553ee7b93550fabb0a57221b51a4fc71ec43da7c9dff71d318c7e070c` | 13:50, 18594 B |
| `tools/mado-mimeglob.py` (sibling, read by the candidate) | `65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453` | base tools/ |
| `tools/mado-mimesniff.py` | `4ef019c69ea8ae4147f83d1558683f012fb4aac0815d36770304717aaca6af24` | base tools/ |
| `tools/mado-mimetext.py` | `d5f174fc33d0b1f1847897a8e63724c7112137c1bf58a89508d1c1c13b857cbd` | base tools/ |
| `.ufo/waves/round-97/controls/filetype-cases-r97.json` (draft; not yet -frozen) | `c88c06aacf447880bf44052fdf69219a8bcbee59024a81938cbeeffd13e088f8` | 13:54, 140 cases, 196 paths |
| `.ufo/waves/round-97/controls/filetype-fresh-r97.py` (generator) | `59db603e54b7e6da57db455308336181edf50937060b91948b8d97eccddf0829` (seeds 0x97/0x5eed) and `d286ac6b78562f9c5db14bf0aa7d5901eb8e67f0a72b3bb879004b3119b4b0a0` (seed 0xaa) | the generator was rewritten during the review |
| `.ufo/waves/round-97/controls/filetype-host-r97.txt` (host list) | `8499d0c8...` (13:53, 12042 paths), `e8cdfc96...` (14:01, 11837), `4f28035b4cfea0b3f6d8d9f5eb3efb630b2a09db4fc06fa141555e76a9a829a4` (later, 11834, 0 lstat errors) | the seat rewrote it three times during the review |
| `/usr/bin/gio` (the oracle) | `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462` | `gio --version` 2.90.1 |
| host packages | glib2 2.90.1-1, shared-mime-info 2.5.1-2, xdg-utils 1.2.1-2, file 5.48-1 | `pacman -Q` |

Two in-wave drafts matter as evidence of the leg biting: the tool at `15ddaf03...` (13:46, `name_only`
returned a list in text/none mode -> TypeError; `_stat_branch` re-raised ELOOP) and the case file at
`4f296ae5...` (13:52, labels carried a `:content-type: ` prefix). Neither is the candidate or the
case file any more; do not cite their behavior as the current state.

## 2. Method (all read-only; scratch only)

Harness scripts in the seat scratch (not committed, stdlib only; they invoke `/usr/bin/gio` as the
oracle):

- `case_harness.py` - builds each frozen case root from the JSON (files base64, env `{root}`
  substitution, symlink/fifo/sock/unreadable creation), re-derives the label with
  `env -i LC_ALL=C HOME=<root>/h [XDG_DATA_HOME=..] [XDG_DATA_DIRS=..] gio info -a
  standard::content-type|standard::fast-content-type [-n] <abs path>`, then (mode `tool`) runs the
  pinned candidate with the matching `--home/--data-home/--data-dirs` flags, and (mode `control`)
  runs `tools/mado-mimeglob.py` on each path's basename for the name-only instrument.
- `compare.py` - pins the candidate by sha into its own directory next to the three siblings (the
  candidate resolves them from its own directory), builds one attack-surface root (trailing
  slashes, symlink loop, dangling link, live/dir links, mode-000 file, mode-000 parent, socket,
  fifo, char/block device, /proc, size-0 typed name, several-type names, desktop magic with a
  control byte, space and newline names) and runs oracle and tool on 51 (path, attr, mode) rows.
- `fresh_check.py` - runs the frozen fresh generator for a seed, then re-derives every label with
  gio and runs the candidate on every generated root.
- `host_compare.py` - runs the candidate once over the whole host list and gio per path (24
  workers), mapping the tool's answer by its `path=` field (not by position; see F6).
- `memo_check.py` - the memoriser control: keys frozen labels by (kind, basename, content sha256 /
  link target), then tests the fresh paths against that map.
- `attack_probe*.py` - oracle-only recordings of the attack-surface rows.

No writes outside the scratch root; no network; no compositor or config touched; no pacman. No
tool installed or upgraded (nothing was needed: python3 and gio are already present).

## 3. Findings (severity order)

### F1 (High, declaration truth): the symlink-loop sentence is false, and the frozen cases score loops

The declaration's rule 7 and named limits say "a path that cannot be stat'ed at all (missing, or a
symlink loop) is outside the surface ... the same refusal gio info makes ... and no case scores
it". Both halves are false. GLocalFileInfo lstats first (glocalfileinfo.c:1932-1964), sees a
symlink, and a failing follow-stat sets `symlink_broken`, so get_content_type returns
`inode/symlink` through the broken-target branch (:1309-1312), rc 0. The oracle answers the loop,
it does not refuse it. And the frozen case draft scores four loop cases with `inode/symlink`
labels: `brok-03-loop-follow`, `brok-04-loop-nofollow`, `nofollow-04-loop-nofollow`,
`follow-04-loop-follow` (two paths each).

Repro:

```
env -i LC_ALL=C HOME=$S/cmp/h XDG_DATA_HOME=$S/cmp/dh \
  XDG_DATA_DIRS=/usr/local/share:/usr/share /usr/bin/gio info -a standard::content-type $S/cmp/l
  -> standard::content-type: inode/symlink   (rc=0)
env -i LC_ALL=C python3 -I <pin>/mado-filetype.py --data-home $S/cmp/dh \
  --data-dirs /usr/local/share:/usr/share --home $S/cmp/h $S/cmp/l
  -> MADO_FILETYPE: inode/symlink ...        (rc=0)
```

The candidate at `15ddaf03...` had been changed to re-raise ELOOP (`except OSError as e: if
e.errno == errno.ELOOP: raise`) so that it printed `MADO_FILETYPE: ERROR stat` and exited 2 for a
loop, i.e. it was fitted to the declaration sentence instead of the oracle; that made it fail the
four frozen loop paths (my run on `4f296ae5` + `15ddaf0`: 94/196 paths, 62/140 cases wrong, four of
them the loop paths). At `e68150b5` the code returns `inode/symlink` and passes them. The current
docstring still carries the false sentence (lines 34-35: "a path that cannot be stat'ed (missing,
or a symlink loop) is outside the surface ... ERROR stat"), so the tool's own documentation
contradicts its code. The same false premise ("a loop answers only under NOFOLLOW (follow mode
cannot stat it: ELOOP -> the oracle refuses ...)") is a comment in the fresh generator
(filetype-fresh-r97.py, the `brok` class), although the generator still adds the loop path under
both modes and measures it: seed 0xaa produced follow-mode loop cases `brok-33-text`, `brok-42-text`,
`brok-66-text`, `brok-91-cache`, all labelled (and answered by the tool) `inode/symlink`. So the
false sentence propagated to three places (declaration rule 7, candidate docstring, generator
comment) and must be corrected in all three at the freeze.

Impact: the predicate sentence itself only says "every frozen case exactly", so it is not broken;
the *declaration text* is, and it must not drive the implementation (it already did once). Fold:
delete "or a symlink loop" from rule 7 and from the named limits, state that a loop answers
`inode/symlink`, and fix the candidate docstring at the freeze (the L1 owns the edit).

### F2 (High, predicate control): "the memoriser 0 on the fresh leg" is false

A memoriser keyed by the input identity (kind, basename, content sha256, symlink target) and
addressed to the frozen case labels answers 80 of the 426 fresh paths of seed `0x5eed` (18.8%),
all of them exactly right: chardev 32, blkdev 24, dir 16, fifo 8. The fresh generator reuses the
frozen fixture vocabulary for fixed-identity paths (`/dev/null`, `/dev/zero`, `/dev/full`,
`/dev/tty`, `pipe`, `sub`, `h`, ...), so the control cannot be 0 as declared unless it is keyed on
something the fresh leg changes (the case id/root, which makes the control vacuous), or the
generator is changed to emit inputs that never appear in the frozen set.

Repro:

```
python3 -I controls/filetype-fresh-r97.py --seed 0000000000005eed \
  --dir $S/fresh2 --out $S/fresh2.jsonl --count 120        # 120 cases, 426 paths
python3 memo_check.py cases-pin-c88c06aa.json fresh2.jsonl fresh2
  -> {"fresh_paths": 426, "memo_hits": 80, "memo_keys": 82}
  -> hits by kind: {"chardev": 32, "blkdev": 24, "dir": 16, "fifo": 8}
```

Impact: under an input-identity keying the memoriser conjunct is falsified (80/426, all correct
labels); under an env-inclusive keying (the fresh env is `{root}/db`+`{root}/dh`, the frozen envs
are `{root}/d1`+null) it is 0 by construction and tests nothing (the same conclusion R97MCritic
reaches for its own memoriser). Either way the declared "memoriser 0 on the fresh leg" does not
demonstrate that the tool is not a memoriser; the tool itself is not one (its fresh-leg answers are
0/426 wrong by measurement). Fold: key the memoriser on the path input only and assert the fresh
inputs are disjoint from the frozen ones, or state the control as vacuous.

### F3 (Medium-high, tool vs oracle, outside every scored set): GFile path normalization is not modelled

GIO's GFile normalizes the path before lstat (the `local path:` line in `gio info` output shows
it): trailing slashes and a trailing `/.` are stripped, so a regular file with a trailing slash is
answered normally. The candidate lstats the raw string. Measured divergences:

| path | oracle | tool |
|---|---|---|
| `$R/blob/` (regular file, text/plain content) | `image/png` (rc 0) | `ERROR stat` (rc 2) |
| `$R/blob/.` | `image/png` (rc 0) | `ERROR stat` (rc 2) |
| `$R/fake.png///` | `image/png` (rc 0) | `ERROR stat` (rc 2) |
| `$R/dlink/ --nofollow` (link to a dir) | `inode/symlink` (rc 0) | `inode/directory` (rc 0) |

The declaration's rule 3 also says "a trailing `/` -> inode/directory uncertain"; that
g_content_type_guess_impl branch (gcontenttype-fdo.c:597-603) is unreachable through
GLocalFileInfo because the GFile path never carries the slash, so the sentence describes a path the
surface cannot take. The candidate implements neither the branch nor the normalization.

Impact: no frozen case or host path has this shape today (the only trailing-slash paths in the case
file are real directories, `dir-01`, `dir-05`, `dir-10`, which both sides answer
`inode/directory`), so clause (i)/(iv) stay green; but the CLI takes arbitrary PATHs and the
declared surface is "the content type GIO reports for a path". The fresh generator does emit a
trailing-slash symlink (`fldir/`, `follow` class, label `inode/directory`; eight follow cases per
seed), and both sides answer `inode/directory` there because follow mode resolves the link anyway.
The `nofollow` class currently emits `nldir` without a slash; if it ever emitted `nldir/`, the
label would be `inode/symlink` (GIO strips the slash, then lstats) and the tool's `inode/directory`
would fail clause (iii). That is the concrete falsifier for this finding inside the scored surface.
Fold: either model the normalization (strip trailing slashes except `/`, then lstat) or add it to
the named limits; either way, fix rule 3's sentence.

### F4 (Medium, tool vs oracle, outside every scored set): EACCES from lstat is tolerated by GIO, refused by the tool

glocalfileinfo.c:1932-1954 does not error on EACCES from lstat; it proceeds with `stat_ok = FALSE`
and answers the name-only guess (the sniff's open then fails and the name-only answer is kept).
The candidate maps every OSError from `os.lstat` to `MADO_FILETYPE: ERROR stat` + exit 2. Measured
(a file inside a mode-000 directory):

```
env -i LC_ALL=C HOME=$R/h XDG_DATA_HOME=$R/dh XDG_DATA_DIRS=/usr/local/share:/usr/share \
  /usr/bin/gio info -a standard::content-type $R/sub/denied/child
  -> standard::content-type: application/octet-stream   (rc=0)
(the same for $R/sub/denied2/child.txt -> text/plain, rc=0)
<pin>/mado-filetype.py ... $R/sub/denied/child
  -> MADO_FILETYPE: ERROR stat ...                      (rc=2)
```

Impact: none of the frozen `readerr` cases hits it (they are mode-000 *files*: lstat succeeds, the
sniff open fails, both sides keep the name-only answer), and the current host list has 0 EACCES
paths. R97MCritic's C1-11 shows why the case set is empty here: the case builder crashed on its own
unsearchable-parent case (`readerr-05-locked-dir-iner`) and the case was rewritten to a readable
file, which removed the only input that would have caught this divergence. But rule 7's "a path that cannot be stat'ed ... the same refusal gio info makes" is false
for EACCES, and a future case or host path with an unsearchable parent mis-scores. Fold: treat
EACCES like the oracle (answer, name-only) or declare the refusal in the named limits.

### F5 (Medium, selftest quality): three always-true checks and two weakened ones

`--selftest` prints `MADO_FILETYPE_SELFTEST: checks=25 failed=0` (rc 0, also under `env -i` with an
empty PATH), and the tool seat's report cites "checks cover ... stat-error exit 2". The check list
does not support that:

- f08's value is a tuple: `(lambda t: (t[0] == "image/png", t[1] == 0))(ans(...))` - a non-empty
  tuple is truthy, so the check can never fail.
- f17 is `... if False else True` - a constant.
- f21 is `chr(0) == "\x00"` - a constant.
- f13 accepts either "app/child" or "app/zz" (the subclass walk or its fallback), f24 accepts
  "text/plain" or "app/hi"; neither discriminates the behaviour it names.
- No check invokes `main`, so no check asserts "exit 2" or the ERROR line format.

Impact: clause (vii) is technically satisfied (`failed=0`, N=25>=20) but the real check count is
about 20, and a green selftest is weaker evidence than the count suggests. The three tautologies
are one-line fixes; recommend fixing them before the freeze rather than arguing the threshold.

### F6 (Medium, output contract): line order is not argv order when errors are mixed; --json drops errors

ERROR lines are printed inside the loop; success lines are printed after the loop. With a mix the
output starts with the errors and then continues with the successes in argv order, so the output
sequence is not the input sequence:

```
<pin>/mado-filetype.py ... $R/nope $R/"a b.txt" $R/zero.desktop
  MADO_FILETYPE: ERROR stat path=.../nope
  MADO_FILETYPE: text/plain ... path=.../a\x20b.txt
  MADO_FILETYPE: application/x-zerosize ... path=.../zero.desktop
  MADO_FILETYPE_DIRS: db=cache            (rc=2)
```

`--json` prints only the answered paths (errors vanish from the JSON) and still exits 2. The
contract says "one line per path", and the only safe key is the `path=` field. My first host run
mapped by position and reported 3302 phantom mismatches; keying by `path=` gave 0 (section 4, clause (iv)). The
counter must key by path (or the tool must emit in argv order and include errors in --json).
Recommend the latter: it is a small change and removes a silent-mis-score trap.

### F7 (Low-medium, host leg): volatile host paths make clause (iv) non-reproducible

On the 13:53 host list (`8499d0c8...`, 12042 paths) the full run gave 5 mismatches, all of the form
oracle ERROR / tool "application/octet-stream" or "application/x-coff", all under
`/home/vgpnk/.config/chromium/Safe Browsing/`. Re-checking seconds later: the five files no longer
exist (`stat` and `gio` both ENOENT); chromium rotates those store files. The tool had seen them
before the oracle did. This is a race on the list, not a modelling error. The seat's sanitized
lists (14:01 `e8cdfc96...`, 11837 paths: 0 mismatches; later `4f28035b...`, 11834 paths, 0 lstat
errors) look cleaner, but the 14:01 list still carried 46 `Safe Browsing` paths.

Impact: clause (iv) says `host == host_total` exactly; with mutating files that is luck between the
two processes. Fold: pin a list whose paths are stable for the measurement window (or drop
`~/.config/chromium` stores), or have the counter re-lstat and relabel at measurement time with a
retry before counting a mismatch.

### F8 (Low, case schema vs the shared contract): 14 host-db cases and 4 implicit none cases

Shared contract 2 says a case's `XDG_DATA_DIRS` is `{root}/d1:{root}/d2` (null forbidden) and that
"at least one mime/ tree must be declared per case in files OR the env points only at empty dirs".
The case draft has 14 cases with `XDG_DATA_DIRS="/usr/share"` and `XDG_DATA_HOME="{root}/h"` and
no mime/ tree (`dir-07`, `dir-10`, `chr-09`, `blk-07`, `fifo-06`, `sock-06`, `zero-09`, `empty-09`,
`sym-08`, `brok-07`, `certain-09`, `uncertain-09`, `fast-09`, ...). Their labels depend on the
host's shared-mime-info (pinned in host-db-r97.json, so the dependence is known), but they are not
the env shape the contract describes. Separately, 4 none-mode cases declare no files at all and
rely on the builder to create the empty env dirs. Both sides answer these cases identically today
(196/196), so this is a contract/artifact mismatch to fold, not a scoring risk: amend the contract
sentence to allow the host-db cases (and to say the builder creates env dirs), or drop them.

### F9 (Low, model claim): the `.png` "never sniffed" example is false on the host database

Rule 3 says "a file named *.png with plain text is image/png and is never sniffed". On the host DB
`*.png` has two name types (`image/png` weight 50 and `image/apng` weight 40,
/usr/share/mime/globs2:1374,1587), so the name-only guess is uncertain and the file is sniffed; the
answer still ends as `image/png` (first name type, sniffed type is not a subclass and has priority
< 80). The example is true only in the frozen cases' custom DBs. The host-DB certainty case
`certain-09-certain-host-db` (fixture `a.png` with text bytes) is therefore not a certainty case on
this host, so a mutation "a certain name never sniffs" is not killed by it (R97MCritic C1-4). No
score effect at the current case set; the sentence should say "in a database where the extension
has exactly one type".

### F10 (Low, operability/structural): `_esc` reloads mado-mimeglob once per output line

`_esc(b)` calls `_load_mimeglob()`, which runs a fresh `spec_from_file_location` + `exec_module` for
every path (success and error alike). The host leg (11837 paths) spends most of its ~30 s in
repeated module execution, and the escaping module instance is distinct from the answering one.
The sibling-load *call site* is still exactly one, so the structural conjunct's letter holds; a
runtime load-count audit would see N+1 loads, and a tight counter timeout would be wasted. Cache
the module at module level (one import) - it is pure.

### F11 (High, structural conjunct): the only implemented allowlist denies the candidate

The predicate's structural conjunct ("run under an empty PATH through the audit launcher with the
structural allowlist (no process, socket, network or non-libc dynamic import; the three sibling lane
modules loaded by pinned path and allowed attributes only)") has one implemented precedent: the
round-96 counter's `static_check` (`quality/counters/c1-r96-magictext.py:424-506`), which AST-walks
every `ast.Import` including function-local ones against `_OK_IMPORTS = {__future__, argparse,
importlib.util, json, os, struct, sys, tempfile}`. Run against the candidate at e68150b5 it returns
four findings:

```
python3 - <<'EOF'   # loads quality/counters/c1-r96-magictext.py, calls static_check(candidate bytes)
["import:errno:52", "import:stat:56", "import:socket:343",
 "spec_location-not-sibling-mimeglob:64"]
```

`socket` is imported inside `selftest()` (line 343) to bind a UNIX socket fixture; `errno`/`stat`
are module-level stdlib imports absent from the r96 set; and the single `spec_from_file_location`
call passes the variable `fname`, not the literal `mado-mimeglob.py`, which the precedent insists
on. If the C1 counter reuses that conjunct, the candidate is denied before any case is scored. Of
the four, `socket` is the one the predicate's own sentence names ("no ... socket ... import"), so
the candidate should replace the fixture with `os.mknod(path, stat.S_IFSOCK | 0o600)` (no import;
verified by R97MCritic) or move the selftest socket creation behind a different mechanism; `errno`
and `stat` are harmless stdlib and the C1 allowlist should include them; the literal-spec demand is
over-strict for a three-sibling loader and the C1 counter should accept a variable whose value is a
sibling file name.

### F12 (High, guard): the shipped host list carries the password-manager tree

The current host list (`4f28035b...`, 11834 paths) contains 76 paths under
`/home/vgpnk/.config/1Password/`; 53 of them are regular non-zero files and 19 are also
name-uncertain under the host cache (no single name type: `1password.sqlite`, `*.sqlite-wal`,
`Local State`, `Trust Tokens`, ...). Both the oracle and the candidate `open()` and `read()` the
first up-to-16384 bytes of a name-uncertain regular file on the sniff path, so the host leg reads
credential material. The list header's credential filter (236 dropped) misses the password manager
(the prefix list has no `1Password`, `Local State` or `Trust Tokens`), and re-running
`sanitize-host-list.py` on the shipped list is a no-op (R97MCritic C1-5). Census (names only, no
content read):

```
76 paths /1Password/ in the list; 53 regular non-zero; 19 name-uncertain regular non-zero
(e.g. 1password.sqlite, 1password.sqlite-shm, 1password.sqlite-wal, 1password_resources.sqlite*, Local State)
```

Transparency for this seat: my two host-leg runs (the 12042-path and 11837-path lists) executed
`/usr/bin/gio` on every listed path, so those runs also read the sniff bytes of the 1Password files
that were in those lists. The labels are MIME type strings only; no file content was printed,
stored or copied. I cancelled my third (final-list) host run for this reason and will not run the
host leg again until the list denies the prefix. This is the list's defect, not the tool's, but the
counter must not run until it is fixed; the C1 counter should additionally assert that no path
under the denied prefixes is present before it labels (fail closed, SETUP_ERROR).

## 4. PRED-C1-r97-v1, clause by clause

(i) **every frozen case exactly, 15/15 classes.** Falsifiable: yes, and falsified at an earlier
in-wave draft (tool 15ddaf0 + case 4f296ae5: 94/196 paths, 62/140 cases wrong - the name-only API
mismatch in text/none mode and the ELOOP re-raise). At the current pins it is green: 140/140 cases,
196/196 paths exact, all 15 classes 9-10 cases each.

```
python3 case_harness.py oracle cases-pin-c88c06aa.json --scratch $S/c2-oracle --all
  -> {"mode":"oracle","cases":140,"paths":196,"bad_paths":0}
python3 case_harness.py tool cases-pin-c88c06aa.json --scratch $S/c2-tool \
  --tool $S/pin-e68150b553ee/mado-filetype.py --all
  -> {"mode":"tool","cases":140,"paths":196,"bad_paths":0}
```

Caveat: the -frozen copy does not exist; this is the 13:54 draft (sha c88c06aa).

(ii) **every frozen mutant killed, class_kills 15/15.** Falsifiable: no - there is no mutant file
and no C1 counter at review time (`.ufo/waves/round-97/controls/` has no
`filetype-mutants-r97*.json`; `quality/counters/c1-r97-filetype.py` is absent). The leg has no
artifact to run, so it is neither passed nor failed; it cannot be certified at the freeze unless
the mutants and the counter land first.

(iii) **every fresh seeded case exact, >=120.** Falsifiable: yes; green on two seeds at generator
59db603e. The generator's own labels were re-derived by gio (label provenance) and the tool was run
on every generated root (tool agreement): 0 bad paths both times.

```
python3 -I controls/filetype-fresh-r97.py --seed 0000000000005eed --dir $S/fresh2 \
  --out $S/fresh2.jsonl --count 120            # 120 cases, 426 paths
python3 fresh_check.py pin-e68150b553ee fresh2.jsonl fresh2
  -> {"fresh_cases":120,"paths":426,"bad":0}
# seed 0x0000000000000097: generator 59db603e, 120 cases, 425 paths -> bad 0
# seed 0x00000000000000aa: generator d286ac6b, 120 cases, 437 paths -> bad 0
#   (that seed carries follow-mode loop cases brok-33/42/66/91 and follow-mode trailing-slash
#    symlinks fldir/ in eight follow cases - the tool matches the measured label on all of them)
```

(iv) **every host-list file exact, >=1500.** Falsifiable: yes, but the leg must not run as shipped
(F12: 76 password-manager paths, 19 of them name-uncertain regular files that the sniff reads; and
F7: volatile paths). On the 11837-path sanitized list the run was exact (0 mismatches, rc 0) before
the credential defect was found; that run itself read the listed 1Password files, so it is evidence
of arithmetic, not a green light. The tool exits 2 when a path is missing; the counter must map by
`path=` and treat rc 2 as "answered, with ERROR rows" (F6). My run on the final list was cancelled
(F12), so the shipped list's exactness is unmeasured by this seat.

```
python3 host_compare.py pin-e68150b553ee 0
  # 13:53 list (8499d0c8..., 12042 paths): 5 mismatches, all 5 chromium stores gone a second later
  # 14:01 list (e8cdfc96..., 11837 paths): {"host_total":11837,"mismatches":0},
  #   tool_rc 0, tool_lines 11837, tool_map 11837
```

Census of the later list (4f28035b..., 11834 paths): chardev 94, symlink 850, blkdev 11, file
6403, dir 4473, sock 3, lstat errors 0.

(v) **the oracle is the installed gio.** Falsifiable: yes; green. `sha256sum /usr/bin/gio` =
`d2164260...`, equal to the case file's `gio_sha256` and the L1's receipt; `gio --version` 2.90.1;
glib2 2.90.1-1. All 196 frozen labels and all 851 fresh labels were reproduced by this binary
(re-derivation above); the case file's `glib2` field is 2.90.1-1.

(vi) **controls stay behind.** Partly measurable, one conjunct falsified:
- name-only instrument (r94 model on every basename): 59/196 paths and 34/140 cases exact, strictly
  fewer than both totals. Claim holds.
  `python3 case_harness.py control cases-pin-c88c06aa.json --scratch $S/c3-ctl --mimeglob tools/mado-mimeglob.py --all`
  (per-case tally computed from the JSONL: 34 exact).
- naive extension-table model: not implemented by me; a static extension table plus the fixed
  inode names cannot answer the custom text/none databases (the case file has app/x-* types and
  none-mode cases), so it is structurally < total. [INFERENCE - not measured; the counter's own
  naive model does not exist yet.]
- memoriser 0 on the fresh leg: **FALSIFIED**, 80/426 hits (F2). The tool itself is not a
  memoriser, but this control as declared does not prove it.
- library-asking forgery rejected: not measurable (no `forgery-ctypes-r97.py`, no counter audit).
  The structural conjunct itself is **falsified at this snapshot** under the only implemented
  allowlist: the r96 `static_check` returns `import:errno:52`, `import:stat:56`,
  `import:socket:343`, `spec_location-not-sibling-mimeglob:64` (F11). The answer path does not
  import socket (it is inside `selftest()`), but the AST walk sees every import.

(vii) **selftest green, N>=20.** Falsifiable: yes; falsified at 15ddaf0 (`failed=3`, rc 1) and green
at e68150b5, including under `env -i` with an empty PATH. But three of the 25 checks are
tautologies and two are weakened (F5), so a stricter "20 genuine checks" reading is at the
boundary; and if the counter runs `--selftest` through the structural allowlist, the
`import:socket:343` finding (F11) may deny the leg before the checks run.

```
python3 .ufo/waves/round-97/build/mado-filetype.py --selftest
  -> MADO_FILETYPE_SELFTEST: checks=25 failed=0    (rc=0)
env -i /usr/bin/python3 -I <pin>/mado-filetype.py --selftest
  -> MADO_FILETYPE_SELFTEST: checks=25 failed=0    (rc=0)
```

## 5. Attack-surface probes that matched (no finding)

These were measured oracle-versus-tool at pin e68150b5 and agree: `--fast` on an uncertain name
(application/octet-stream, never sniffed); a live symlink with follow (target type) and with
nofollow (inode/symlink); a dangling link both modes (inode/symlink); a symlink to a denied target
(inode/symlink); a FIFO without hanging (inode/fifo, oracle and tool under a 10 s timeout); a
socket (inode/socket); /dev/null (inode/chardevice); the host block device /dev/nvme1n1p2
(inode/blockdevice); /proc/self/status (application/x-zerosize - size 0 is answered before the
sniff, no /proc read); a size-0 file named `zero.desktop` and one named `empty.png`
(application/x-zerosize); a read-protected file with PNG bytes (open fails -> name-only
application/octet-stream); a name-only-certain `.png` with plain text (image/png, no sniff); the
several-type names `.doc`/`.png`/`.html` with contradicting bytes (first name type wins);
space and newline names escape as `\x20`/`\x0a` and stay on one line; `blob/..`-class paths were
not probeable (the tool errors, as in F3); `.` and `/` (inode/directory); a host file with no name
type and root-owned (/etc/passwd -> text/plain, which also shows the O_NOATIME EPERM retry's
effect: the sniff still happened).

Two model notes (no observable defect):

- The sniff length is hardcoded 16384, not read from the database. Measured equivalence: a crafted
  cache/text DB with magic at offset 5000 -> oracle and tool both `application/x-far` (cache and
  text mode); magic at offset 16500 -> both `application/octet-stream` (the clamp). Any read length
  >= min(max_extent, 16384) matches identically, and 16384 always is, so the hardcode is
  observationally exact; the docstring sentence "the source is the database" is the only drift.
- `--json` drops error paths (F6); text mode and none mode now answer correctly (both were the
  15ddaf0 crash); `MADO_FILETYPE_DIRS` prints `db=none` for empty dirs, matching the contract's
  vocabulary.

## 5bis. Cross-check with R97MCritic, and one correction

R97MCritic (same wave) independently reaches the EACCES finding (C1-1, including a `/proc/1/fd/0`
instance), the trailing-slash finding (C1-2), the `*.png` two-type finding (C1-4), the host-leg
credential finding (C1-5), the missing frozen host labels (C1-6), the selftest tautologies and
socket import (C1-7), the generator's false drop/refusal sentences and label shape (C1-8), the
missing ERROR coverage (C1-9) and the 14 host-db cases (C1-10). My independent measurements agree
with those; F2/F4/F9/F11/F12 above carry the reproductions from this seat.

One correction to their C1-3: the claim "the host's extent is 128" does not reproduce. Their probe
(`sx127` with a NUL at index 127 vs `sx128` with the NUL at 128) measures the *binary/text fallback
window* (xdgmimeint.c:176-190, the first 128 bytes), not `xdg_mime_get_max_buffer_extents`. The
host cache stores `max_extent = 18730` (u32 at cache offset 24 -> magic section at 112992, +4; the
section header words are 689, 18730, ...), and the host text database's parser maximum is 4104
(`>4096=<len 8>EFI PART`); get_content_type clamps both to 16384. Functional proof that the read is
larger than 128: a file with `Microsoft Excel 5.0 Worksheet` at offset 2080 (extent 2109) answers
`application/vnd.ms-excel` from the oracle (cache mode) and from the tool:

```
python3 -c "d=bytearray(2400); d[2080:2109]=b'Microsoft Excel 5.0 Worksheet'; open('excelmagic','wb').write(bytes(d))"
env -i LC_ALL=C HOME=$P /usr/bin/gio info -a standard::content-type $P/excelmagic
  -> application/vnd.ms-excel (rc=0)
<pin>/mado-filetype.py --home-unset --data-home-unset --data-dirs-unset $P/excelmagic
  -> MADO_FILETYPE: application/vnd.ms-excel ... (rc=0)
```

So the hardcoded 16384 is observationally equivalent to `clamp(max_buffer_extents)` for every
*consistent* database (any read length >= min(max_extent, 16384) matches identically, and a
max_extent above 16384 clamps for both). Their proposed falsifier does still stand in principle: a
hand-written cache that declares a max_extent smaller than one of its own matchlets is accepted by
GLib's reader (it does not validate consistency), and against such a case the tool would match
where gio does not. That is the only way the hardcode is observable; it is a case-schema
possibility, not a host-DB fact. My crafted-DB probes (magic at 5000 -> both `application/x-far`;
magic at 16500 -> both `application/octet-stream`) confirm the equivalence on consistent databases.

## 6. Residual risk and verification gaps

- I could not run the literal counting command: `quality/counters/c1-r97-filetype.py`, the
  `*-frozen.json` copies, `filetype-host-r97-frozen.txt`, the mutants and the forgery are absent at
  review time (the C1 counter seat had not produced them). Every green above is my independent
  re-derivation, not the counter's verdict; the pin/structural/audit conjuncts are unverified
  beyond the static import read.
- The artifacts moved during the review: the tool through three shas (reported e492c46d, measured
  15ddaf0, current e68150b5), the case file through two (4f296ae5, c88c06aa), the host list through
  three. The L1 must pin all of them in the Freeze block and re-run section 4's four commands at
  the measured revision; my findings F1-F4 are about claims and out-of-set paths, so a green
  predicate will not repair them.
- F3 and F4 are the two known tool-versus-oracle divergences left. They are outside every scored
  set today, which is exactly why they survived; if the L1 keeps the surface claim ("what GIO
  reports for a path"), they should be either fixed or listed in the named limits.
- The selftest tautologies mean a green selftest understates nothing about the tool but overstates
  what it proves; fixing the three checks is cheap and should happen before the freeze.
- The fresh-leg memoriser collision (F2) is false under an input-identity keying and vacuous under
  an env-inclusive one; the other controls are either true or absent.
- The host list must be regenerated with the password-manager tree denied before the counter runs
  (F12). My first two host runs read the sniff bytes of the listed 1Password files; that is a
  guard breach caused by the list, not by an attempt to inspect credentials, and it must not be
  repeated. The host leg's arithmetic (0 mismatches on 11837 paths) is unaffected as an arithmetic
  result, but it is not a ship-ready green.
- The structural conjunct is currently red under the only implemented allowlist (F11); this is the
  single most likely way the C1 predicate fails at the freeze even though every scored leg is
  exact.

## 7. Repro index (commands, all from the seat scratch; S = /fast/scratch/hyaku/mado-r97/R97MReviewC1)

- oracle re-derivation: `python3 case_harness.py oracle cases-pin-c88c06aa.json --scratch $S/c2-oracle --all`
- candidate on the frozen draft: `python3 case_harness.py tool cases-pin-c88c06aa.json --scratch $S/c2-tool --tool $S/pin-e68150b553ee/mado-filetype.py --all`
- name-only control: `python3 case_harness.py control cases-pin-c88c06aa.json --scratch $S/c3-ctl --mimeglob /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-mimeglob.py --all`
- attack table: `python3 compare.py` (51 rows, 5 mismatches: F3/F4)
- fresh legs: `python3 -I .../filetype-fresh-r97.py --seed <hex> --dir $S/freshN --out $S/freshN.jsonl --count 120` then `python3 fresh_check.py pin-e68150b553ee freshN.jsonl freshN`
- host leg: `python3 host_compare.py pin-e68150b553ee 0`
- memoriser: `python3 memo_check.py cases-pin-c88c06aa.json fresh2.jsonl fresh2`
- oracle identity: `sha256sum /usr/bin/gio; /usr/bin/gio --version; pacman -Q glib2 shared-mime-info xdg-utils file`

## 8. Ship note

Nothing in this review changes a contract, an axis, a route or a judgment. The verdict below is a
recommendation: at pins e68150b5 (tool) x c88c06aa (case draft) x 59db603e (generator) x e8cdfc96
(host list), the C1 case and fresh and host legs are exact and the labelled provenance is the
installed gio; the declaration must still (a) drop the symlink-loop sentence, (b) fix the memoriser
control or the fresh pool, (c) decide on the EACCES and path-normalization limits, (d) land the
counter, mutants, forgery and frozen copies before the counting command can run, (e) align the
structural allowlist with the candidate (the `socket` import is the one the predicate names) and
(f) regenerate the host list with the password-manager tree denied before the host leg runs again.
The arithmetic greens above were measured at generator 59db603e/d286ac6b and host list
e8cdfc96; the fresh leg is also green at d286ac6b/seed 0xaa (437 paths).

Report: .ufo/waves/round-97/w1/R97MReviewC1.md
