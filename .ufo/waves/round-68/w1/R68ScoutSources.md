# R68ScoutSources — source binding and frozen recipe texts (read-only)

- lane/round: mado r68, w1, seat `R68ScoutSources`; read-only: no production edit, no git/jj mutation.
- lane HEAD observed during the seat: `40d2bef8964a098ae50f01094fa19e4725952010` ("round-68: successor
  control harness and the one-wave dispatch evidence", 2026-11-03 22:06:33 -0300).
- freeze declaration commit `e0727cda15621766c35dcf8b70c211b6531aab45` (22:04:51 -0300); control JSON and
  pre-freeze baseline `2ca2bec39c42770a3176989f013e8c1cbbdb7df3` (22:04:23 -0300).
- lane base (pre-r68): `510100c81e6cf63fec6be380c2f2f9c670f32cbc`.

## 1. Findings table

| item | exact locator | observed | verdict |
|---|---|---|---|
| round source fetch | `https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-cat-file.adoc` (opened 2026-11-03) | HTTP 200; 16,099 B; sha256 `6c32dbda8c2106be08bda471592db50b5afaf185de32f2e513e80d802b4a95b2`; three fetches (tag twice, peeled commit once) byte-identical (`cmp` rc 0) | bound |
| quote, object read | DESCRIPTION, `git-cat-file.adoc:21-22` | ""Output the contents or other properties such as size, type or delta information of one or more objects."" — 18 words | grounded, <=25 words |
| batch form | DESCRIPTION `:24-30`; OPTIONS `--batch` `:109-113`, `--batch-check` `:127-131`; BATCH OUTPUT `:298-312` | `:30` "In batch mode, arguments are read from standard input."; `:301-304` "cat-file will read objects from stdin" and each line is "considered as an object, as if it were fed to linkgit:git-rev-parse[1]" | grounded |
| pretty form | OPTIONS `-p`, `git-cat-file.adoc:54-55` | `:55` "Pretty-print the contents of `<object>` based on its type." | grounded |
| replacement exception | OPTIONS `--batch-all-objects`, `git-cat-file.adoc:192-199` | `:198-199` "Objects are presented as-is, without respecting the "replace" mechanism of linkgit:git-replace[1]." — scoped to this mode only | grounded, page-scoped |
| tag pin | `git ls-remote https://github.com/git/git 'v2.56.0' 'v2.56.0^{}'` | tag object `2478544319491bbd2a42cc57a83e3d2f4730a280`; peeled commit `a018953688f1b10bddf91bff8747068f5f4746a4` | matches S099/S100/S101/S436 |
| host git | `git --version` | `git version 2.56.0`, rc 0 | matches the tag |
| next SOURCES id | `corpus/SOURCES.md` at HEAD (round-start census, 373 data rows) | min S001, max S436, 63 unused ids below max (S190…), no `S437` row | next append is **S437** |
| duplicate URL | normalized scan of all 373 source cells | 0 rows naming `git-cat-file`; 0 rows naming `git-scm.com`; exact/fuzzy duplicate hits `[]` | no duplicate |
| sibling precedent | 6 rows under `raw.githubusercontent.com/git/git/v2.56.0/` | docs: S099 `git-commit.adoc`, S100 `git-add.adoc`, S101 `git-push.adoc`, S436 `git-replace.adoc`; code: S102 `git.c`, S118 `builtin/commit.c` | same repo+tag, different files: family precedent, not a URL duplicate; S436 is the immediately preceding row (`corpus/SOURCES.md:386`) |
| planned row (scribe) | `.ufo/waves/round-68/w1/R68ScribeKnowledge/draft/corpus/SOURCES-row.txt` (1068 B, sha256 `cbf4cf5ef05b0ca3381b2a6b5222049607c0ad055a97a463e56ff8b0e1eaac05`) | 11 cells; no literal or escaped pipe; id S437; `docs`/`A`; anchor `git-cat-file.adoc:6,21-22,27-28,40,44,50,55,198-199,295-296,303-304 @ tag v2.56.0` + sha256 + `16099 bytes`; opened `2026-11-03`; `mined`; `90d`; used-by two paths | PASS, 3 word-level nits (section 6) |
| used-by targets | `corpus/lessons/round-68.md`, `corpus/knowledge/gate-git-read-guards-r68.md` | both absent at check time; both are the wave's named integration targets (`w1-spec.json` items 4 and 5); knowledge draft already at `.ufo/waves/round-68/w1/R68ScribeKnowledge/draft/corpus/knowledge/gate-git-read-guards-r68.md` (247 lines) | will exist at integration; re-check at landing |

Supporting fetches at the same tag (all HTTP 200, rc 0): `git-show.adoc` 1,939 B sha256
`91dfc431d85e53a12ef7854cbeb52674f4e2e52a7fe9ffe3ee018c1b2ed5ea30` (`:16` "Shows one or more objects
(blobs, trees, tags and commits)."); `git-ls-tree.adoc` 5,515 B sha256
`fb78c902d5496cab2e2891b4be8d5f88096ff7baa30957ceb70798b2129877d6` (`:18-19` "Lists the contents of a given
tree object"); `git-rev-parse.adoc` 17,036 B sha256
`4d8e9aca13f6ea6808272eb44e417687a5cca7d23cf1ed311f25e9fdeb148902`; `git-config.adoc` 21,576 B sha256
`655541c20fe58e30c2e45803df422a5a1ed3658bf025ceaed6c1764089edcd27`.

Citation audit of the knowledge draft: the 12 line-cited doc quotes (L6, L21-22, L27-28, L40-41,
L44-45, L50-51, L55, L198-199, L295-296, L303-304, L379 `<object> SP missing LF`, L392
`<object> SP ambiguous LF`) are all present verbatim at the cited bytes; the row's sha256/byte count
match the fetched bytes. `c2-controls.json` sha256 `b7a1c939e5a715792d2969eb4ca86d8119cd5a72ef930d00d57338c62faf6a91`
matches the knowledge draft. The census vocabulary at `quality/counters/c2-r68-reader-guard.py:41-43`
matches the eight-verb list.

## 2. Frozen recipe texts against committed bytes

Exact-substring counts, computed on git blobs (`git show`), not on the worktree:

| id | find text | `c2-r67-landing-controls.py` @ `510100c8` | `c1-r68-landing-controls.py` @ `40d2bef8` | 2nd occurrence | mutant compiles |
|---|---|---|---|---|---|
| S1 | `mr_killed = bool(` | 1x, line 489 | 1x, line 491 | none in either file | yes (both) |
| S2 | `mz_killed = mz_rc != 0` | 1x, line 437 | 1x, line 439 | none in either file | yes (both) |
| S3 | `killed = int(mz_killed) + int(mr_killed)` | 1x, line 505 | 1x, line 507 | none in either file | yes (both) |

- Blob identity: c2-r67 @ `510100c8` = 30,697 B sha256
  `a4376fa739405a213ccd59847620be02bec5fd2a70584aa59dfbc916022d9b58` (equals the worktree file; `git diff`
  empty). c1-r68 @ `40d2bef8` = 36,005 B sha256
  `25470bc432ad3b612f08869052915f331d9a930149b3af6a9bf0e3eb87cf5527` (equals the worktree file). The c1
  harness was untracked at seat start and was committed concurrently at `40d2bef8`.
- Declaration table rows parse byte-identically to the counter's `RECIPES` tuple
  (`quality/counters/c1-r68-selfmutants.py:42-45`; counter sha256
  `bdea8dc6b4455f45c59896a44f0bd4ede21c26b82c67e0618a05ac069ef50a85`, tracked, clean at HEAD).
- Mechanism [observed]: `_scripted_checks` (`c1-r68-landing-controls.py:617`) -> `_measure_case` (`:593`)
  -> the real `measure()` with `run` monkeypatched; the none-killed case asserts
  `... selftest=0 mz=fail mr=fail killed=0/2 baseline=0/2 verdict=TARGET_MISSED ...` (`:636-637`);
  `selftest()` (`:772`) extends those checks and returns 1 when any fails (`:791`).
- Kill verdict **[INFERENCE, not executed by this seat]**: each forced credit moves `killed`/the
  `mz`-`mr` label away from the asserted none-killed line, so each mutant's `--selftest` exits nonzero.
  This seat ran neither the harness nor the counter; execution receipts belong to `R68RevC1` /
  `R68MutBattery`.
- Base consistency [observed]: `git cat-file -e 510100c8:quality/counters/c1-r68-landing-controls.py`
  rc 128 (path absent at base), so the scored harness cannot exist at the base rev — consistent with the
  declared baseline `selftest=absent`.

## 3. Rejected candidates for the lesson Gate

- **Primary reject:** `Documentation/git-config.adoc` @ v2.56.0 (21,576 B, sha256 `655541c2…`). It
  documents the config plane (`get`/`set`, `--replace-all`, deprecated forms); `GIT_NO_REPLACE_OBJECTS`
  count 0 and `cat-file` count 0. It cannot ground an object-read row.
  **Flip:** an admitted scope that turns on the repository/user-config plane (e.g. whether a config key
  can flip replacement behaviour) — then the config reference entry for that key is the source, not the
  read verb.
- **Secondary reject:** `Documentation/git-ls-tree.adoc` @ v2.56.0 (5,515 B, sha256 `fb78c902…`):
  grounds one verb only ("Lists the contents of a given tree object", `:16-19`) and neither the batch nor
  the pretty forms. **Flip:** a row scoped to `ls-tree` alone (e.g. the citecheck child's tree read).
- **Redundancy reject:** `git-replace.adoc` is already S436 (docs, same tag); a second row on the same URL
  would be a URL duplicate. **Flip:** S436's scope moving, which is not this round.

## 4. Commands and exit codes (all from the lane root or the seat scratch)

1. `curl -sS -f -o git-cat-file.adoc https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-cat-file.adoc`
   -> `http=200 bytes=16099`, rc 0.
2. re-fetch at tag and at peeled commit `a0189536…`, then `cmp` x2 -> rc 0 both (`tag-fetch-identical`,
   `peeled-identical`).
3. `sha256sum git-cat-file.adoc` -> `6c32dbda…a95b2`.
4. `git --version` -> `git version 2.56.0`, rc 0.
5. `git ls-remote https://github.com/git/git 'v2.56.0' 'v2.56.0^{}'` -> the two ids above, rc 0.
6. `git cat-file -s 510100c8:quality/counters/c2-r67-landing-controls.py` -> 30697; `git show … | sha256sum`
   -> `a4376fa7…`.
7. `git cat-file -e 510100c8:quality/counters/c1-r68-landing-controls.py` -> rc 128 (absent).
8. Python exact-substring count over the two blobs -> 1/1/1 in each, no secondary occurrence (rc 0);
   `compile()` of all six mutants -> ok.
9. Python SOURCES scan -> 373 rows, min S001, max S436, 63 gaps below max, 0 duplicate URLs, 0 `S437`.
10. Python row validator on the scribe draft -> 13 split parts / 11 cells; every frozen check True.
11. Python declaration-vs-counter compare -> 3/3 recipe pairs byte-equal.
12. Python citation audit -> 12/12 cited quotes found verbatim at the cited line spans.

No tool was installed or upgraded; no package manager transaction was attempted. No credential, token or
session material was read or written. Scratch `/fast/scratch/hyaku/mado-r68/R68ScoutSources/` was removed
before yield (`test ! -e` verified).

## 5. Remaining unknowns

- Mutant kills and the counter run are unexecuted here (inference above only).
- The lesson path `corpus/lessons/round-68.md` does not exist yet; its exact landing path is the wave
  target, not an observed file.
- The row's used-by cell can only be confirmed at L1 landing.

## 6. Row nits (word-level; no shape or id defect)

1. Anchor cites `:40`, `:44`, `:50` for sentences that wrap: exact spans are `:40-41`, `:44-45`,
   `:50-51`.
2. Teaches quote 2 is an ellipsis fragment ("as if it were fed to ... git-rev-parse"); the file has
   `linkgit:git-rev-parse[1]`.
3. Teaches quote 3 prints `the replace mechanism` where `:199` carries nested quoting
   (`the "replace" mechanism`). The scope phrase "the one documented mode that bypasses replacement" is
   page-scoped: the affirmative rule that ordinary reads honour replacement comes from S436, not from
   `:198-199`.
