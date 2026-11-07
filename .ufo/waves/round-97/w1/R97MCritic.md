# R97MCritic  --  falsification report (round 97, w1)

Scope: attack PRED-C1-r97-v1 and PRED-C2-r97-v1 and their inputs before the freeze; no candidate, case
file, counter, control or lane file was edited. Every command below was run read-only; all fixtures live
under `$S=/fast/scratch/hyaku/mado-r97/R97MCritic` (deleted before yield).

## Snapshot attacked (the artifacts moved during this review)

| artifact | sha256 | bytes / time |
|---|---|---|
| `.ufo/waves/round-97/claims-declaration-r97.md` | (live draft, not pinned) | 17091, 2026-11-07 13:59:07 -0300 |
| `.ufo/waves/round-97/build/mado-filetype.py` (C1 candidate) | `e68150b553ee7b93550fabb0a57221b51a4fc71ec43da7c9dff71d318c7e070c` | 18594, 13:50:06 |
| `.../controls/filetype-cases-r97.json` (C1 cases) | `c88c06aacf447880bf44052fdf69219a8bcbee59024a81938cbeeffd13e088f8` | 140 cases, 13:54:41 |
| `.../controls/filetype-probe-r97.py` (case builder) | `a6c544eb21b8ee29a347f08569b194897a1d93d0e27e732f5f0c428a48d6d0e0` | 45210, 13:53:37 |
| `.../controls/filetype-fresh-r97.py` (fresh generator) | `59db603e54b7e6da57db455308336181edf50937060b91948b8d97eccddf0829` | 17025, 13:58:01 |
| `.../controls/filetype-host-r97.txt` (host list) | `4f28035b4cfea0b3f6d8d9f5eb3efb630b2a09db4fc06fa141555e76a9a829a4` | 11834 paths, 14:03 |
| `.../controls/host-db-r97.json` | `0c6c0c0c7f62353777053bb77b33bca4cb01a23d0e5ab81eaa5c8d9d00518562` | 13:44 |
| `quality/counters/c1-r97-filetype.py`, `c2-r97-counter-selftest.py` | absent | - |
| mutants / forgery / counter panel / `selftest-fixtures/` | absent (fixtures dir empty) | - |

Host ground: glib2 2.90.1-1, shared-mime-info 2.5.1-2, `/usr/bin/gio` sha256
`d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`. The C1 case file was rebuilt with
`--check` and matched (`CHECK_OK ... 140 cases, sha256 c88c06aa...`), so it is reproducible from the builder
at this snapshot.

## Predicate arithmetic (what is reachable at this snapshot)

- `classes == 15/15`: reachable. 140 cases, `dir` 10 and each of the other 14 classes 9; every class is >= 8.
- `correct == cases`: the candidate answers **140/140 frozen labels exactly** under my independent
  materialisation (I rebuilt every case from the JSON `files`/`paths` and compared the tool's per-path line
  to the file's label).
- `fresh == fresh_total`: at `--seed 0x97c0ffee --count 24` the generator produced 24 cases / 82 paths /
  0 dropped and the candidate answered **82/82**.
- name-only control: **59/196 labels correct** (per class: `certain` 10/11, `fast` 9/10, `readerr` 8/11,
  `sym` 12/23, `uncertain` 4/11, `dir` 4/21, `chr`/`blk`/`fifo`/`sock`/`zero`/`brok` 0). Strictly below the
  total, so the "control stays behind" conjunct is satisfiable (the control is weak: it is name-only, as
  declared).
- host leg census (11834 paths, sha 4f28035b): dir 4472, reg 6159, reg0 242, lnk 850, chr 94, blk 11,
  sock 3, unstatable 3 (ENOENT), EACCES 0. The stat branches are exercised; the two failure branches in C1-1/C1-2 are not.
- `C1 --selftest` at the candidate snapshot: `checks=25 failed=0`, rc 0.
- C2 base controls: `python3 -I quality/counters/c1-r96-magictext.py --selftest` and
  `... c2-r96-selftest-kills.py --selftest` both exit rc 2 (argparse usage)  --  the "base refuses" control
  holds. `python3 -I quality/check-tool-ledger.py --repo . --rev e6152b58` prints
  `LEDGER: population=188 ledger_rows=188 uncovered=0 ... verdict=TARGET_MET`, and
  `git show e6152b58:quality/tool-ledger.md | grep -c 'c1-r96-magictext'` = 1, same for
  `c2-r96-selftest-kills` = 1  --  the ledger invariant is true at base.

## C1 findings

### C1-1 (model vs the revised rule 7): lstat `EACCES` is answered by gio, refused by the candidate

The declaration (rule 7, lines 62-70) now says: a failed lstat is refused only when its errno is **not**
`EACCES`; an EACCES "is tolerated and the file continues with no stat, the attribute then coming from the
name-only guess and a failed open". The candidate does not implement this:

```sh
P=$S/t
mkdir -p $P/locked && printf 'hello\n' > $P/locked/pic.png && chmod 000 $P/locked
env -i LC_ALL=C HOME=$P/root/h /usr/bin/gio info -a standard::content-type $P/locked/pic.png
#   standard::content-type: image/png        rc=0
env -i LC_ALL=C HOME=$P/root/h python3 -I $S/tool/mado-filetype.py $P/locked/pic.png
#   MADO_FILETYPE: ERROR stat path=.../locked/pic.png   rc=2
env -i LC_ALL=C HOME=$P/root/h /usr/bin/gio info -a standard::content-type /proc/1/fd/0
#   standard::content-type: application/octet-stream    rc=0
env -i LC_ALL=C HOME=$P/root/h python3 -I $S/tool/mado-filetype.py /proc/1/fd/0
#   MADO_FILETYPE: ERROR stat path=/proc/1/fd/0        rc=2
```

Cause: `_stat_branch` lets `os.lstat` raise. In `glocalfileinfo.c:1940-1951` only non-EACCES errors
bail; EACCES continues with `stat_ok = FALSE`, `is_symlink = FALSE`, i.e. the basename is guessed and the
sniff open then fails. Impact: the frozen case set has **no** unsearchable-parent case (the earlier
`readerr-05-locked-dir-iner` was rewritten to a readable file, see C1-11) and the host list has 0 EACCES
paths, so the predicate's legs cannot catch this; the declaration's own sentence is currently false of the
tool it freezes.

Smallest safe correction: in `_stat_branch`, catch `OSError` from `os.lstat`; if `e.errno == errno.EACCES`
return `None` with the "no stat" semantics (the caller's name guess + failed open already produce the
answer), else re-raise. Add one frozen case: a `000` parent directory with `pic.png` (label `image/png`)
and an untyped child (label `application/octet-stream`).

### C1-2 (declaration false): a trailing slash on a file is answered, not refused

Rule 7 now says "a missing path or an `ENOTDIR` (a trailing slash on a file) prints
`MADO_FILETYPE: ERROR stat` and exits 2, matching `gio info`". The oracle does not refuse; the CLI
normalises the path before stat:

```sh
env -i LC_ALL=C HOME=$P/root/h /usr/bin/gio info -a standard::content-type $P/f.txt/
#   local path: .../f.txt ; standard::content-type: text/plain   rc=0
env -i LC_ALL=C HOME=$P/root/h /usr/bin/gio info -a standard::content-type $P/f.txt//
#   local path: .../f.txt ; standard::content-type: text/plain   rc=0
env -i LC_ALL=C HOME=$P/root/h /usr/bin/gio info -a standard::content-type /dev/null/
#   local path: /dev/null ; standard::content-type: inode/chardevice  rc=0
env -i LC_ALL=C HOME=$P/root/h python3 -I $S/tool/mado-filetype.py $P/f.txt/
#   MADO_FILETYPE: ERROR stat path=.../f.txt/    rc=2
```

`//` is preserved by gio and answers `inode/directory`; `dir//` answers `inode/directory`. The case file
has no trailing-slash path, so no leg sees this. Fix: normalise like `GLocalFile` (`p.rstrip('/')`, keeping
`"/"` and `"//"`), then stat; amend the rule-7 sentence; add a frozen case with `f.txt/` and `dir/`.

### C1-3 (rule 4 vs candidate): the sniff extent is hardcoded, the host's extent is 128

Rule 4 (lines 47-54) now derives the extent from the database (cache: header word at offset 24, then +4;
text: the parser's maximum). The candidate sets `self.max_buffer_extents = 16384` (line 164) for every
mode and reads 16384 bytes. The host's extent is measured at **128**:

```sh
python3 -c "open('sx127','wb').write(b'A'*127+b'\x00'+b'B'*10); open('sx128','wb').write(b'A'*128+b'\x00'+b'B'*10)"
env -i LC_ALL=C HOME=$P/root/h /usr/bin/gio info -a standard::content-type $P/sx127   # application/octet-stream
env -i LC_ALL=C HOME=$P/root/h /usr/bin/gio info -a standard::content-type $P/sx128   # text/plain
```

The answers still agree today only because the pinned sibling's magic step tests text over `data[:128]`
(`tools/mado-mimesniff.py:218`) and no host matchlet reaches beyond 128. The *magic matcher* uses the whole
16384-byte buffer, so a fixture cache declaring a smaller `max_extent` with a matchlet beyond it would match
in the tool and not in gio (the case schema allows such a cache). Fix: read the extent from the parsed
cache/text tables and use it for the read; add one frozen case with a small declared extent and a matchlet
beyond it.

### C1-4 (rule 3 false in cache mode): `*.png` is not a one-type name

Rule 3 (lines 43-46) says "one name type -> that type, uncertain FALSE (so a file named `*.png` with plain
text is `image/png` and is never sniffed)". Against the host cache the name step returns two types:

```sh
python3 - <<'EOF'   # tools/mado-mimeglob.py Resolver over the host dirs
# x.png -> image/png uncertain=1 types=['image/png','image/apng']
EOF
```

so a `.png` file **is** sniffed (the answer stays `image/png` only because nothing name-subclassed is found).
The frozen `certain` cases use the text fixture DB (`DB_MAIN` has one `*.png` glob), so they are certain in
their own DB; but the host-DB cases (`certain-09-certain-host-db`, fixture `a.png` with text bytes) are not
certainty cases, and a mutation "a certain name never sniffs" is not killed by them. Fix: correct the
sentence; use a one-type host name (`*.txt`, `*.desktop`) for host-DB `certain` cases.

### C1-5 (host leg reads credential material)

The host list contains **77 paths under `/home/vgpnk/.config/1Password/`**, and **19 of them are regular,
non-zero and name-uncertain** under the host cache, so both gio and the tool `open()`+`read()` their first
bytes on the sniff path:

```
/home/vgpnk/.config/1Password/1password.sqlite          (1900544 B, types=[])
/home/vgpnk/.config/1Password/1password.sqlite-wal      (4416672 B, types=[])
/home/vgpnk/.config/1Password/1password_resources.sqlite
/home/vgpnk/.config/1Password/Local State
/home/vgpnk/.config/1Password/Trust Tokens
...
```

The current list header documents its own credential filter: "dropped every path whose basename or any
dirname segment (case-insensitive) matches .ssh|.gnupg|agent.db|credential|keyring|token|secret|.netrc|
hosts.yml|auth|*.pem|*.key|id_rsa|shadow|passwd, or any path under ~/.config/{gh,anthropic,elevenlabs,omp}|
~/.local/share/keyrings|~/.aws|~/.docker. 236 dropped, 12042 kept". The filter misses the password manager:
`python3 sanitize-host-list.py filetype-host-r97.txt OUT` on the shipped list prints
`SANITIZE: kept_paths=11834 dropped_paths=0 comments=22` and OUT still holds all 77 (CRED_RE does not match
"1Password", "Local State", "Trust Tokens"). Re-running the safety script on its own output is a no-op, so
the filter cannot repair the shipped list; the same header still says "~/.config filenames only (never
contents)", which the host leg's sniff contradicts (it opens every name-uncertain regular file and reads
its first bytes). This also contradicts the seat's no-credential rule. No vault byte was read in this
review; the evidence is lstat + basename certainty only. Fix: add `/home/vgpnk/.config/1Password/` (and the
other credential stores: browser `Local State`/`Cookies`/`Login Data`, keyrings, `wallet*`) to
`DENY_PREFIX`, regenerate the list from the census (not from the shipped file) and its receipt, and have
the C1 counter assert the prefix is absent before it labels; do not run the host leg until then.

### C1-6 (host leg has no frozen labels; the leg is not reproducible)

The C1 counting command passes `--host-list` and `--host-db` but no host-label file or pin; predicate (iv)
"every file of the frozen host list exactly" is therefore measured against labels produced live at
measurement. The list spans 6159 regular files and 242 zero-size files under `/home`, `/etc`, `/proc`,
`/sys` and `/usr`; contents and existence on the host are mutable (3 paths were already ENOENT when I
re-censused the shipped list minutes after it was written). `PROTOCOL.md` 390-395 requires a gate
whose verdict depends on a mutable artifact to ship a committed snapshot with a committed expected verdict.
Fix: freeze `host-labels-r97.json` (path, label, sha256) with `--expect-host-labels-sha256` and score
against it (the oracle re-run can then be a separate drift check).

### C1-7 (selftest: structural denial and two tautologies)

`mado-filetype.py` at `e68150b5` imports `socket` inside `selftest()` (line 343) to bind a UNIX socket
fixture. The predicate's structural allowlist is "no process, socket, network or non-libc dynamic import",
and the r96 static checker AST-walks every `ast.Import` (`quality/counters/c1-r96-magictext.py:424,436`),
so `import:socket:343` fails the selftest leg under the launcher. Two checks are tautologies that can never
fail:

- line 397: `("f17 missing path raises, ...", (lambda: ...)() if False else True)`
- line 402: `("f21 esc renders a control byte", chr(0) == "\x00")`

`checks=25` still meets N>=20, but the count overstates coverage. Fix: build the socket with
`os.mknod(path, stat.S_IFSOCK | 0o600)` (verified to work as this user; no import), and replace f17 with
`_raises(missing)` and f21 with `_esc(b"\x00") == "\\x00"`.

### C1-8 (fresh generator: false drop rule, label shape, vacuous memoriser)

(a) The generator docstring says paths whose oracle run exits nonzero without an attribute "(missing target,
symlink loop, ENOTDIR, EACCES on stat)" are dropped. That is false for three of the four: gio answers a
symlink loop (`inode/symlink`, rc 0), never returns ENOTDIR for a trailing slash (it strips it), and answers
EACCES paths (name-only). Only a missing target produces no attribute. The frozen `brok`/`follow` cases
score loops, so the generator must keep them (it does).

(b) The generator's JSON lines carry `labels` as plain strings (`["inode/symlink", ...]`), while Shared
contract 2 requires `[["<type>"] or ["ERROR"]]`. A counter that validates the schema will reject or
misread. Fix: emit the contract's shape, or state the difference in the counter contract.

(c) The memoriser keys on a fingerprint that includes the env; the fresh env is `{root}/db` +
`{root}/dh`, the frozen envs are `{root}/d1` + null, so no fresh case can equal a frozen one and the
memoriser is **0 by construction**. The conjunct "the memoriser 0 on the fresh leg" is therefore true and
tests nothing. Fix: state the control as vacuous (disjoint env), or key the memoriser on mode+files+inputs
only and assert the fresh inputs are disjoint from the frozen ones.

### C1-9 (the ERROR/refusal branch has no frozen coverage)

The fresh generator's docstring says the ERROR/refusal leg "is covered by the frozen case file and the host
list instead". The frozen case file has **0 `ERROR` labels** (label census over all 140 cases: 16 MIME
types, no ERROR), and the shipped host list has 3 ENOENT paths with no frozen labels (the 37 volatile
/proc paths were removed). So `MADO_FILETYPE: ERROR stat` + exit 2 is implemented by the tool and named by the declaration
but unmeasured. Fix: add one or two frozen cases with a missing path labelled `["ERROR"]`, or declare the
branch untested in the named limits.

### C1-10 (14 frozen cases break the case-env contract and are non-hermetic)

Case-file env census: 126 cases `{"HOME":"{root}/h","XDG_DATA_DIRS":"{root}/d1","XDG_DATA_HOME":null}`;
14 cases `{"HOME":"{root}/h","XDG_DATA_DIRS":"/usr/share","XDG_DATA_HOME":"{root}/h"}` (the ids ending
`-host-db`). Shared contract 2 defines `XDG_DATA_DIRS` as `{root}/d1:{root}/d2` or null (null forbidden) and
`XDG_DATA_HOME` as `{root}/dh` or null; `/usr/share` and `{root}/h` are outside it. The 14 labels also
depend on the host's `/usr/share/mime` (cache mode), whose sha is not recorded in the case file: a later
glib/shared-mime-info upgrade makes frozen labels stale (the `host-db-r97.json` pin does not reach the case
file). Fix: copy the host DB into `{root}/dX/mime` (the fresh generator already does this with `{root}/db`)
and regenerate the 14 cases, or amend the contract and record the host DB sha in the case file.

### C1-11 (builder latent defect, and the case it removed)

At builder sha `4fbda5d7` the `finally` restore chmods a path of type `unreadable` to `0o644`; for a
directory that clears the x bit and the builder crashed on its own case `readerr-05-locked-dir-iner`:

```
PermissionError: [Errno 13] Permission denied: '.../cases/readerr-05-locked-dir-iner/locked/secretdata'
  at filetype-probe-r97.py:1215 (files_schema open)
```

The case was then rewritten to a readable `locked/secretdata` file (current sha `a6c544eb`), which removed
the only unsearchable-parent case and with it the only input that would catch C1-1. Fix: restore `0o755`
for directories; re-add the locked-parent case.

## C2 findings

### C2-1 (internal contradiction): "0 registry rows / registry 0 -> 4" survives in the prose

The revised surface and predicate are correct: the base has **one** row (`tools/mado-mimetext.py`,
`SKILL.md:887`, measured with `git show e6152b58:SKILL.md | grep -c mado-mimetext` = 1; the two counters and
the kill-set are 0), and the predicate now says `1 -> 4`. But the "Before -> after" block (lines 175-177)
still says "0 registry rows ... registry 0 -> 4 rows". A reader replaying that block would look for a
movement the tree cannot show. Fix: change the block to "1 row ... registry 1 -> 4".

### C2-2 (duplicate authority / category): the fourth row is a kill-set input, not a gate

`quality/selftest-kills/check-receipt-presence.json` is the `--kills` input of the existing
`mado-selftest-strength` gate row (`SKILL.md:879` names the (TOOL, KILLSET) population) and is consumed by
`quality/counters/c2-r96-selftest-kills.py`. The registry row schema is
`| name | gate/probe | entry command | verdict map | self-test | ... |`; a JSON input has no entry command
or verdict map, and no other kill-set JSON (`check-seat-reports.json`, `mado-mimeglob.json`,
`mado-portals.json`, ...) has a row. Adding one creates a row kind the registry does not have. Fix: extend
the `mado-selftest-strength` row's population with the new kill-set and add rows only for the two counters
(registry 1 -> 3); or declare the new row kind explicitly in the registry header.

### C2-3 (the always-OK control is still not expressed as a test of the counter)

Predicate (iv) now reads: "a stub that prints the result line without running a check flags **none** of the
neutralisations (`always_ok_flagged=0`)". A stub trivially flags nothing; that is a property of the stub,
not evidence that the C2 counter catches it. A correct counter must print that it *caught* the stub on the
panel. Fix: require `always_ok_caught=<panel>/<panel>` (or `always_ok_unflagged=0` with the sentence saying
"the counter rejects the stub on every neutralisation").

### C2-4 (fixed in the revision; verified): base controls

`--base-rev` is now in the command (line 168). `python3 -I quality/counters/{c1-r96-magictext,
c2-r96-selftest-kills}.py --selftest` both exit rc 2 with argparse usage (the do-nothing control holds), and
`quality/check-tool-ledger.py --repo . --rev e6152b58` prints `uncovered=0` with both counter rows present.
No finding beyond C2-1/C2-2/C2-3.

### C2-5 (id stability): neither counter prints a per-check id today

The r96 counters print `case <id> WRONG`, `probe ...`, and the verdict line; there is no per-check finding
id. The new `--selftest` must therefore introduce literal ids (the shared contract's
`MADO_COUNTER_SELFTEST_FAIL: <id>`), and the C2 counter must verify, per panel entry, that the `find` text
occurs **exactly once** in the counter source (a shared helper neutralisation would otherwise fail several
ids and `negative_ids == panel` fails). `PROTOCOL.md` 385-389 requires the expected ids to be committed and
independent of the recomputation; the panel JSON satisfies this only if each id is a literal in the check
body, not a list index.

### C2-6 (unbuilt): the C2 legs are unmeasurable at the snapshot

`quality/counters/c2-r97-counter-selftest.py`, the panel, and the `selftest-fixtures/` content are absent,
so (ii)-(iv) cannot be measured. The declaration must not be frozen with `<PANEL>`/`<C1COUNTER>`/
`<C2COUNTER>` pins unfilled.

## Mid-wave near-misses (fixed at the snapshot; for the round-97 lesson and the freeze discipline)

These were live defects earlier in the same wave and are recorded because the freeze pins must be verified,
not assumed:

- candidate `15ddaf03` (13:46): `--selftest` failed 3/25 (`f06`, `f13`, `f24`).
- candidate `e492c46d` (13:48): text-mode **and** none-mode crashed
  (`TypeError: list indices must be integers or slices, not str` at `answer()`), i.e. every case whose DB is
  a `mime/` text tree produced no line; fixed at `e68150b5` (name-only now uses the resolver for all modes).
- builder `4fbda5d7` (13:49): `gio_label` returned `':content-type: image/png'` and
  `':fast-content-type: image/png'` (it did `line.split(':', 1)[1]`); every frozen label would have carried
  the prefix and no tool could match. Fixed at `a6c544eb` (prefix stripped). A label-shape check (no `:`,
  a MIME token) belongs in the counter's setup so a regressed builder is SETUP_ERROR, not a wrong verdict.
- builder `4fbda5d7` also crashed on its own locked-dir case (C1-11), and the case was removed (C1-1).
- host list `8499d0c8` (13:44, 12278 paths) had 37 unstatable /proc paths and 79 1Password paths; rewritten
  at `e8cdfc96` (14:01, 11837 paths) and again at `4f28035b` (14:03, 11834 paths), with 77 1Password paths
  still in it (C1-5); the re-run of its own sanitizer drops 0.

## Limits of this review

- The C1 and C2 counters, the C1 mutants/forgery, the counter panel, and the selftest fixtures were absent;
  every "the counter will..." sentence in the predicate is therefore unverified, not merely unrun.
- The host-leg findings are from the list bytes, lstat, the sanitizer run, and name-only certainty of the
  basenames; no vault or credential file was opened by this seat.
- My scoring used the case file's own labels and an independent materialisation of its `files`/`paths`; the
  fresh score used the generator at the pinned sha with a fixed seed. Both are sample-dependent only through
  the fresh seed; the frozen score is exhaustive over the 140 cases.
- The candidate changed four times during the review (`15ddaf03`, `e492c46d`, `e68150b5`, plus the 13:45
  state); every C1 command above is stated against `e68150b5` and must be re-run by the L1 at the frozen
  `--expect-tool-sha256`.
