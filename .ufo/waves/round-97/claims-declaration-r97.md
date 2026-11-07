# mado round 97 — claims declaration (DRAFT until the L1 freeze commit)

Lane `mado`, round 97, hyaku run 15, attempt 1. Base revision `e6152b589c2c6a28426c28263c4bcc3c46398be4` (branch
`master`, the lane's tip at round start; `jj-lane.sh state` prints `ahead=0 behind=0`). Axes owned: coverage +
operability (desktop and compositor craft). Two claims, distinct axes, causally separable.

This file is the declaration **as the wave reads it**. The `## Freeze` block at the end pins every input by sha256
and lists the findings folded in before the freeze; the predicate sentences below do not change after the freeze.

**Axis selection.** Every owned axis sits at 10 in `SCORECARD.md` (rounds 87–96), so the lowest-axis duty is a tie;
the stagnation nudge is **not claimed** (capabilities entered at rounds 88–96). C1 moves coverage on a surface the
coverage map does not hold (the content-type the desktop's GIO reports for a *path*, not for guessed inputs);
C2 moves operability on the two round-96 counters that carry the Gate standard's named self-test gap.

---

## C1 — coverage (new surface): what GIO 2.90.1 reports as `standard::content-type` for a path

**Surface.** Rounds 94–96 modelled `g_content_type_guess` (name-only, data, text database). They do **not** model
the caller the desktop actually uses for a local file: `GLocalFileInfo`'s `get_content_type`
(`glocalfileinfo.c:1300-1389`, held as S522), whose stat branches answer `inode/directory`, `inode/chardevice`,
`inode/blockdevice`, `inode/fifo`, `inode/socket`, `inode/symlink` and `application/x-zerosize` **before** any
guess, and whose sniff is gated on the name-only guess's `uncertain` flag with a sniff length taken from the
database and clamped to 16384. Its public faces are the `standard::content-type` and `standard::fast-content-type`
attributes (`gio info -a …`, the installed `gio` CLI is the oracle). At base **no lane tool answers a path's
content type**; `tools/mado-mimeglob.py`, `mado-mimesniff.py` and `mado-mimetext.py` answer *inputs*, not paths.

**Candidate.** `tools/mado-filetype.py` (frozen candidate bytes at the freeze) — read-only; given `PATH...`, a
follow mode (`--follow` default, `--nofollow`), an attribute mode (`--fast` for `standard::fast-content-type`), and
the XDG roots (`--data-home`, `--data-dirs`, `--home` and their `-unset` forms, as in `tools/mado-mimesniff.py`),
prints one `MADO_FILETYPE: <type> attr=<full|fast> mode=<follow|nofollow> path=<escaped>` line per path plus
`MADO_FILETYPE_DIRS: db=<cache|text|none> …`. It loads `tools/mado-mimeglob.py` (r94), `tools/mado-mimesniff.py`
(r95) and `tools/mado-mimetext.py` (r96) from its own directory, pinned by sha256; `--selftest` exercises the stat
and gating branches over fixtures and does not require the siblings' imports beyond the pinned load.

**Rules modelled** (each with an S-row or a frozen oracle-labelled fixture):
1. branch order of `get_content_type`: symlink with a broken target **or** `NOFOLLOW_SYMLINKS` → `inode/symlink`
   (`glocalfileinfo.c:1309-1312`); directory `:1313`; character device `:1316`; block device `:1317`; FIFO
   `:1318`; regular with size 0 → `application/x-zerosize` `:1319-1325`; socket `:1327`; every one of these is
   returned through `g_content_type_from_mime_type`, which is the identity on Unix (`gcontenttype.c:291-296`).
2. the guess gate: `g_content_type_guess(basename, NULL, 0, &uncertain)` (`:1337`), then the sniff only when
   `!fast && uncertain && path != NULL` (`:1340`); `fast` never sniffs and returns the name-only answer.
3. the uncertain flag as `g_content_type_guess_impl` sets it (`gcontenttype-fdo.c:567-690`, held as S518/S521):
   one name type → that type, uncertain FALSE (never sniffed); no name type → `application/octet-stream` with
   uncertain **TRUE** (`:641-648`); several → first after the weight sort with uncertain TRUE (`:675-683`); a
   trailing `/` → `inode/directory` uncertain. **Certainty is a property of the database, not of the suffix**: on
   this host's `/usr/share/mime/globs2` `*.png` has two types (`image/png` 50, `image/apng` 40), so a `.png` name
   is uncertain and *is* sniffed (the answer still ends `image/png` unless the priority-80 or subclass rules move
   it); the one-type example holds only in a database with a single glob for that suffix (R97MReviewC1 F9).
4. the sniff length: `_g_unix_content_type_get_sniff_len()` = `xdg_mime_get_max_buffer_extents()`
   (`gcontenttype-fdo.c:55-67`, `xdgmime.c:724-732`), which is **the database's own extent**, not a constant:
   cache mode takes the maximum over the loaded caches of the magic section's `max_extent` field
   (`xdgmimecache.c:726-748`: header word at offset 24, then `+4`), and text mode the parser's maximum
   `offset + value_length + range_length` over the kept sections (`xdgmimemagic.c:695-721`, `:646-649`); it is
   clamped to 16384 when 0 or larger than the buffer (`glocalfileinfo.c:1352-1355`). The file is opened
   `O_RDONLY|O_NOATIME|O_CLOEXEC` with an EPERM retry without `O_NOATIME` (`:1357-1364`); the read's `res` is the
   length re-guessed (`:1368-1374`); an open or read failure keeps the name-only answer (`:1366-1378`).
5. the re-guess with `(basename, data, res)`: one name type still wins over the sniff; several → a sniffed
   priority ≥ 80 wins, else the first name type that is a subclass of the sniffed type, else the first name type
   uncertain; a sniffed `application/x-desktop` with a name becomes `text/plain` (`gcontenttype-fdo.c:622-688`,
   r95's model).
6. the magic and fallback steps are the held models: cache mode `tools/mado-mimesniff.py` (S519, S520), text mode
   `tools/mado-mimetext.py` (S524, S525); the reachable-database mode is `xdgmime.c`'s (S516/S523), and the
   `.desktop`/name/glob step is `tools/mado-mimeglob.py` (S515/S516/S518).
7. the stat itself is GLib's two-stage form (`glocalfileinfo.c:1932-1996`, connector's note): `lstat` first,
   then a guarded follow when the entry is a symlink and the query follows, so a dangling symlink and a **symlink
   loop** classify as `inode/symlink` (oracle-measured: `gio info` answers `inode/symlink` rc 0 for `l -> l`) and
   a symlink to a directory/FIFO/device follows to that branch. A failed `lstat` is refused only when its errno
   is **not** `EACCES` (`glocalfileinfo.c:1940-1951`: an EACCES is tolerated and the file continues with no stat,
   the attribute then coming from the name-only guess and a failed open); a missing path or an `ENOTDIR` (a
   trailing slash on a file) prints `MADO_FILETYPE: ERROR stat` and exits 2, matching `gio info`, and no case
   scores the refused path. Probes: a file under a mode-000 directory answers `application/octet-stream` exit 0;
   `a -> b -> a` answers `inode/symlink` exit 0.

**Predicate PRED-C1-r97-v1** (the same sentence here, in the counter's docstring and in the receipt label):
> `TARGET_MET` iff, at `--rev`, `tools/mado-filetype.py` is the frozen candidate (`tool_sha256 ==
> --expect-tool-sha256`, printed `tool_pin=ok`) and, run under an empty `PATH` through the audit launcher with the
> structural allowlist (no process, network or non-libc dynamic import; `socket` only as the AF_UNIX fixture
> constructor inside `--selftest`; the three sibling lane modules loaded by pinned path and allowed attributes only), it answers (i) every frozen case exactly (`correct ==
> cases`) over the declared classes `dir chr blk fifo sock zero empty sym brok nofollow follow certain uncertain
> fast readerr` (15 classes, ≥8 cases each) and `classes == 15/15`; (ii) every frozen mutant is killed and every
> class kills at least one mutant (`killed == mutants`, `class_kills == 15/15`); (iii) every fresh seeded case
> exactly (`fresh == fresh_total`, ≥120, fixtures generated at measurement time by a frozen generator, labels from
> the same oracle); (iv) every file of the frozen host list exactly (`host == host_total`, ≥1500 paths over the
> host's own database and its special files); (v) the oracle is the installed `gio` (`--expect-gio-sha256`, and
> every frozen label was produced by this binary at the freeze); (vi) the controls stay behind: the do-nothing
> instrument (r94's name-only answer for every case) scores fewer than the total, a naive extension-table model
> fewer, a memoriser keyed by (kind, basename, content sha256, symlink target) over the frozen labels answers
> strictly fewer than the fresh total (measured 80/426 on one seed - the fresh fixtures reuse fixed device names,
> so it is not zero; R97MReviewC1 F2), and a library-asking forgery is rejected (`audit_denials > 0`); and
> (vii) the candidate's `--selftest` is green (`checks=N failed=0`, N ≥ 20). rc 0 TARGET_MET, 1 TARGET_MISSED,
> 2 SETUP_ERROR.

**Counting command** (replayed verbatim by the L1 before the receipt lands; every argument named; the sha values
and the measured revision are filled from the freeze block):

```sh
python3 -I quality/counters/c1-r97-filetype.py --repo . \
  --rev <C1-measured-rev> --base-rev e6152b589c2c6a28426c28263c4bcc3c46398be4 \
  --cases .ufo/waves/round-97/controls/filetype-cases-r97-frozen.json --expect-cases-sha256 fc710b94df67391c392d95aeabd6dfa4c016081019d732f5c373fb990844be20 \
  --mutants .ufo/waves/round-97/controls/filetype-mutants-r97-frozen.json --expect-mutants-sha256 c6f156c380b42b9d1bb78e9eb3142f11cdca70cd0c504cdd8bae2edd3f8db120 \
  --genseed .ufo/waves/round-97/controls/filetype-fresh-r97.py --expect-genseed-sha256 c3143775d346921085a4f312eb596bc9b062abb11c3257aed47d9bba50bf7bf2 \
  --host-list .ufo/waves/round-97/controls/filetype-host-r97-frozen.txt --expect-host-list-sha256 943fd957f4fae5ce77ab2aff12ad473072a88055802afa03b634b290728c2a86 \
  --host-labels .ufo/waves/round-97/controls/host-labels-r97-frozen.json --expect-host-labels-sha256 f4ef8738b93a783c5358400f64de95da0ffc5558328772da19a5ac4a9a28ebea \
  --host-db .ufo/waves/round-97/controls/host-db-r97.json --expect-host-db-sha256 0c6c0c0c7f62353777053bb77b33bca4cb01a23d0e5ab81eaa5c8d9d00518562 \
  --expect-tool-sha256 da6af7a0789265187f6b2c2462bf5104a7c0b780baed3235300f89978a44d2d8 --expect-mimeglob-sha256 65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453 --expect-mimesniff-sha256 4ef019c69ea8ae4147f83d1558683f012fb4aac0815d36770304717aaca6af24 \
  --expect-mimetext-sha256 d5f174fc33d0b1f1847897a8e63724c7112137c1bf58a89508d1c1c13b857cbd --expect-gio-sha256 d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462 \
  --forgery .ufo/waves/round-97/controls/forgery-ctypes-r97.py --expect-forgery-sha256 7b1f1492445ec891fada7755ef103716d7cf89fc44ae655734c19e496ddf7cf9 \
  --scratch-root <SCRATCH>
```

**Before → after.** At base `git cat-file -e <base>:tools/mado-filetype.py` is absent and no lane tool answers a
path's content type (0 scored paths): **0/0 → cases/0**. The measured after is the frozen case total with every
leg exact.

**Cheap no-work controls (committed before the freeze, scored with the frozen counter):**
- do-nothing: the r94 name-only model (`tools/mado-mimeglob.py` at base) answers every case's basename; the
  counter prints `control_nameonly=<n>/<cases>` on cases where a path-level branch or the sniff changes the
  answer — it must score strictly fewer than the total.
- naive: an extension table over the fixture names, with the six fixed `inode/*` names.
- memoriser: the frozen case labels addressed by (kind, basename, content sha256, symlink target) → measured
  80/426 = 18.8% on one fresh seed (strictly fewer than the total; the fresh labels are oracle-produced at
  measurement time, so the memoriser cannot score the paths the fixed family does not repeat).
- forgery: a wrapper that asks the installed `gio`/libgio → rejected by the structural conjunct/audit.

**Named limits (declared with the claim).** Paths only (`g_content_type_guess` over raw inputs stays r94–r96);
`standard::content-type`/`standard::fast-content-type` only (other attributes out); a path whose `lstat` fails with
an errno other than `EACCES` (missing, `ENOTDIR`) is refused (`ERROR stat`, exit 2) and not scored; the fresh leg
re-samples contents and names over a fixed fixture family per class against measurement-time oracle labels (it
cannot reach a branch the frozen family does not build); a trailing slash is stripped from the argument (the `gio`
CLI does the same; measured); the frozen host list is restricted to stable system trees (`/usr`, `/etc`, `/dev`,
`/proc`, `/sys`) and excludes volatile user-config subtrees (measured: chromium's Safe Browsing store rotated two
minutes after one list was generated); 14 cases set `XDG_DATA_DIRS=/usr/share` and so pin the host database
through the frozen `host-db` manifest (the counter verifies that manifest's sha256 and treats a mismatch as
SETUP_ERROR), and the counter creates each case's empty env dirs where the case declares none; `O_NOATIME`'s EPERM retry is modelled, the atime effect is not
measured; the sniff-length source is the host database (a distro patch is scored as upstream); blob/chardev
fixtures use the host's own fixed device paths, declared in the case file.

---

## C2 — operability: the two round-96 counters gain a self-invocation mode, and the Gate standard's registry closes

**Surface.** `PROTOCOL.md` §Gate standard, Self-test asks a gate/probe to expose a self-invocation mode over
isolated fixtures that asserts an exit code and a stable finding id. Round 96's spot-check routed that gap as D4
for `quality/counters/c1-r96-magictext.py` and `quality/counters/c2-r96-selftest-kills.py`, and D3 for their
registry rows in `SKILL.md` plus the round-96 tool and kill-set. At base both counters refuse `--selftest`
(usage error), and `SKILL.md`'s registry holds **one** of the three instrument rows (`tools/mado-mimetext.py`,
line 887; the two counters have none - measured by R97MReviewC2 and R97MCritic at `e6152b58`, correcting this
declaration's first draft which said 0; the receipt-presence kill-set is a pinned input and is named inside its
gate's row).

**Change (declared).** (1) Each counter gains `--selftest`: it runs its own checks over isolated fixture inputs
(committed under `.ufo/waves/round-97/selftest-fixtures/`), asserts each check's exit code and finding id, prints
`MADO_COUNTER_SELFTEST: checks=N failed=0` (stdout, N ≥ 6 per counter) and exits 0/1/2 like the tool gates; its
production path is byte-unchanged when `--selftest` is not given (the counter prints the relocated/unchanged
identity and the diff's added/removed line counts). (2) `SKILL.md`'s registry gains **instrument** rows for
`tools/mado-mimetext.py` and the two counters `quality/counters/c1-r96-magictext.py` and
`quality/counters/c2-r96-selftest-kills.py` (name, gate|probe, entry command, verdict map, self-test
command/spelling, pinned-value path, write scope, owner), the receipt-presence kill-set is named as a pinned
input inside the existing `mado-selftest-strength` row's population (a JSON input has no entry command, so it
is not a registry row: R97MCritic C2-2), and `quality/tool-ledger.md` keeps the two counters covered.

**Predicate PRED-C2-r97-v1** (revised before the freeze on R97MReviewC2's findings 3.1-3.4; the original
sentence is preserved in `.ufo/waves/round-97/w1/R97MReviewC2.md` §3):
> `TARGET_MET` iff, at `--rev` and with `--base-rev` (the pre-landing revision), both counters are the frozen
> candidates (`sha256 == --expect-c1-sha256` / `--expect-c2-sha256`, printed `counter_pin=ok,ok`) and: (i) each
> `--selftest` prints its result line with `failed=0` and exits 0 (`selftest_green=2/2`), with `checks ≥ 6` each;
> (ii) every frozen single-check neutralisation of a counter's own check (≥6 per counter, `--panel`) makes its
> `--selftest` fail with the exact declared finding id (`negative_ids == panel`, survivors printed); (iii) every
> frozen broken-input mode carries its counter (`"counter"` in the panel entry; missing-input / wrong-rev /
> mutated-tool, ≥3 per counter) and makes that counter print its declared `SETUP_ERROR`/`TARGET_MISSED` id and exit
> 1 or 2 (`broken_modes == broken`, per-counter counts printed); (iv) the controls stay behind: the base
> revision's counter bytes (no `--selftest`) refuse with rc 2 and 0/2 green, and a stub that prints the result line
> **and every panel id** is credited with **none** of the neutralisations and the counter prints
> `stub_uncredited=<panel>/<panel>`; the registry rows for the three instruments are re-derived from `SKILL.md` at
> **both** `--base-rev` and `--rev` (measured base: one row, `tools/mado-mimetext.py` at `SKILL.md:887`; the two
> missing rows are the two counters) and move `1 → 3` (`registry=1->3`); and (v) both counters are ledger rows in the population at `--rev`
> (the counter reads `quality/tool-ledger.md` at `--rev`, finds a row for each of the two paths and prints
> `ledger_members=2/2`; this is an invariant, unchanged from base), while `quality/check-tool-ledger.py --repo .
> --rev <rev>` prints `uncovered=0`. rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR.

**Counting command:**

```sh
python3 -I quality/counters/c2-r97-counter-selftest.py --repo . --rev <C2-measured-rev> \
  --base-rev e6152b589c2c6a28426c28263c4bcc3c46398be4 --expect-base-registry-sha256 6a8754df2d6d0123b77db384ac85bef17baa378e0be2782a01ba79e069ff028d \
  --panel .ufo/waves/round-97/controls/counter-selftest-panel-r97.json --expect-panel-sha256 87ba2f4149ff5fbcd7dfe7179bc87b1bd50cd083867f736b62f02796cfa9b4ba \
  --expect-c1-sha256 4f6783848ded9c63f934c68a24da856369895987651d0f66fdd6920f07aaa64d --expect-c2-sha256 54143b8a28f2be4b2f1361c443d32156a68fd088c7cdb9c9030ca7415002217b \
  --expect-registry-sha256 <SKILL-AT-MEASURED-REV> --expect-ledger-sha256 <LEDGER-AT-MEASURED-REV> \
  --scratch-root <SCRATCH>
```

**Before → after.** At base: `--selftest` refused by both counters (rc 2, 0 green, 0/2), 0 registry rows, 0/≥6
neutralisations flagged. After: 2/2 green with ≥6 checks each, all panel neutralisations flagged with the
declared ids, all broken modes named, registry 0 → 4 rows, ledger uncovered 0.

**Controls (committed before the freeze):** the base counter bytes (no `--selftest`) as the do-nothing control; a
stub `--selftest` that prints `failed=0` without running checks (always-OK control) must be flagged by the
counter's structural clause (it checks the counter's real work, not the printed line); an empty panel flags none.

**Named limits.** The self-invocation mode proves the counter's own checks bite on the frozen fixtures, not that
the counter is complete; the panel's neutralisations are the wave's design set; the two counters' *production*
verdicts are re-derived by their own cross-leg (each counter reruns the round-96 receipt at `--rev`), not by this
new counter.

---

## Separability

C1 and C2 touch disjoint files (`tools/mado-filetype.py` + its two counters/controls vs the two round-96 counters
+ `SKILL.md` registry + ledger). The C1 counter is measurable at a revision where C2 has not landed, and the C2
counter at a revision where C1 has not landed; the L1 records one receipt per direction in
`.ufo/waves/round-97/receipts/`.

## Frontier step (round 97)

1. `corpus/SOURCES.md` curated this round: two new rows opened with HTTP 200 receipts in
   `.ufo/waves/round-97/receipts/sources-open-r97.txt` — `gcontenttype-fdo.c`'s sniff-length function
   (`_g_unix_content_type_get_sniff_len`) and the installed `gio(1)` manual's `info`/`-n`/`-a` contract that
   grounds the oracle; plus `used-by` appends on the held rows the C1 entry cites.
2. One mistake mined into `corpus/lessons/round-97.md` `## Mistakes` with class, evidence pointer, captured-by and
   a fix shown able to fail (candidates: the r96 post-report erratum D12, and this round's own findings).
3. C1 is the sourced claim: its model sentences cite S518/S521/S522/S526/S527 and the held magic rows.

## Freeze

Frozen by the L1 at 2026-11-07 14:5x -03 (before any scoring run), from the wave's final artifacts. Every pin is a
sha256 over committed bytes; the copies `controls/filetype-cases-v2.json` -> `controls/filetype-cases-r97-frozen.json`
and `controls/filetype-mutants-v2.json` -> `controls/filetype-mutants-r97-frozen.json`,
`controls/counter-selftest-panel-v2.json` -> `controls/counter-selftest-panel-r97.json` were made byte-exact by
`controls/freeze-r97.sh` and both sides' digests are in `.ufo/waves/round-97/receipts/freeze-copies-r97.txt`.

| input | frozen path | sha256 |
|---|---|---|
| C1 cases | `.ufo/waves/round-97/controls/filetype-cases-r97-frozen.json` (157 cases, 15 classes) | `fc710b94…844be20` |
| C1 mutants | `.ufo/waves/round-97/controls/filetype-mutants-r97-frozen.json` (101 counted, anchored to the tool pin) | `c6f156c3…f8db120` |
| fresh generator | `.ufo/waves/round-97/controls/filetype-fresh-r97.py` | `c3143775…50bf7bf2` |
| host list | `.ufo/waves/round-97/controls/filetype-host-r97-frozen.txt` (6,194 stable paths) | `943fd957…728c2a86` |
| host labels | `.ufo/waves/round-97/controls/host-labels-r97-frozen.json` (6,194 oracle labels, 0 ERROR) | `f4ef8738…a9a28ebea` |
| host DB manifest | `.ufo/waves/round-97/controls/host-db-r97.json` | `0c6c0c0c…5d18562` |
| C1 tool | `.ufo/waves/round-97/build/mado-filetype.v2.py` (landed as `tools/mado-filetype.py`) | `da6af7a0…8a44d2d8` |
| C1 counter | `.ufo/waves/round-97/build/c1-r97-filetype.v2.py` (landed as `quality/counters/c1-r97-filetype.py`) | `745a341e…195ba9e0` |
| forgery | `.ufo/waves/round-97/controls/forgery-ctypes-r97.py` | `7b1f1492…96ddf7cf9` |
| C2 selftest counter 1 | `.ufo/waves/round-97/build/c1-r96-magictext-selftest.v2.py` (landed as `quality/counters/c1-r96-magictext.py`) | `4f678384…aaa64d` |
| C2 selftest counter 2 | `.ufo/waves/round-97/build/c2-r96-selftest-kills-selftest.v2.py` (landed as `quality/counters/c2-r96-selftest-kills.py`) | `54143b8a…002217b` |
| C2 counter | `.ufo/waves/round-97/build/c2-r97-counter-selftest.v2.py` (landed as `quality/counters/c2-r97-counter-selftest.py`) | `abb17a01…06b879` |
| C2 panel | `.ufo/waves/round-97/controls/counter-selftest-panel-r97.json` (7 checks/counter, 6 broken, echo stub) | `95f86861…c188faa8` |
| base `SKILL.md` | `git show e6152b58:SKILL.md` | `6a8754df…ff028d` |

Two pins in the C2 command are **measured outputs of the C2 landing commit**, not inputs it could have had before
it: `<SKILL-AT-MEASURED-REV>` and `<LEDGER-AT-MEASURED-REV>` are read from that commit and written into the replay
command before its first run; they are recorded in `.ufo/waves/round-97/receipts/c2-measured-r97.txt`. No other pin
moves after this block.

Findings folded in before this freeze (each measured by a seat of this round, all in `.ufo/waves/round-97/w1/` and
`w1b/`): the sniff length is the database's own extent (R97MCritic C1-3, R97MReviewC1 F?), the constant is only the
16 KiB buffer clamp; `lstat` `EACCES` is tolerated and answered from the name, only other errnos refuse, and a
symlink loop answers `inode/symlink` (R97MCritic C1-1/C1-2, R97MReviewC1 F1/F4); the `gio` CLI trims trailing
slashes and GIO's GFile normalises `//`, `./`, `a/../b` (R97MCritic C1-2/F3, tool models both); certainty is a
property of the database (`*.png` has two globs on this host; R97MReviewC1 F9); the memoriser control is not zero
by measurement over the fixed device names (80/426, R97MReviewC1 F2) and is restated; the host leg ships frozen
oracle labels because PROTOCOL.md §Gate standard "Two evidences" requires a committed snapshot for a mutable
artifact (R97MCritic C1-6); the raw 12,042-path host census was filtered to 6,194 stable system paths to remove
credential-shaped names (lane r56 rule; R97MCritic C1-5) and volatile subtrees; the C2 registry move is 1 -> 3 over
instrument rows (R97MCritic C2-2), the always-OK control is the echo stub the counter must *catch* (stub_uncredited),
and the C2 command gained `--base-rev` + `--expect-base-registry-sha256` (R97MReviewC2 §3.1).
