# ConnSourcesOverlap — open new mado rows on one tag-pinned file URL each; no sibling id is the same census key

Axes: census URL identity (first `https://` in the source cell only), claim scope (a sibling row must teach this claim), version pin (tag or `?h=` query, not `latest` or `/3/`). C2 calibration is the axis this moves. C1 tripwire operability is untouched.

Verdict for L1: every candidate file URL is absent from all 21 `*-shokunin/corpus/SOURCES.md` registries. Open them as new mado ids (`S098` is the last registry row, `corpus/SOURCES.md:110`; `S099`–`S110` are unused). Do not cite a sibling id. Do not write `supersedes` with a sibling's number: mado `S043` is the Wayland registry spec, and souji `S043` is a different file.

## How a duplicate is decided

`scripts/sources-census.sh` `url_of` (the W04 / E04 / `shared` key), lines 600–605: first `https?://` run in the source cell, fragment stripped, one trailing slash stripped, scheme stripped, host lowercased, path and query kept. A second URL in the same cell is invisible. A redirect is not followed. `v2.56.0` and the peeled commit are different keys.

Tool: `scripts/sources-census.sh` sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30` (same digest as `.ufo/waves/round-20/evidence/census-start.txt`).

```
bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin <21 *-shokunin dirs>
```

Exit 0. 32 `W04`, 0 `E04`. None of the W04 keys are a candidate URL. Mado's own four are pre-existing and unrelated (`corpus/SOURCES.md` sha256 `ccaff539b159a7c0a431f873193e7d0969bda3d0996b1debad1cc4939315b67c`):

```
mado  W04  S030  wiki.hypr.land/Configuring/Basics/Window-Rules
mado  W04  S042  wayland.freedesktop.org/extras.html
mado  W04  S045  wiki.hypr.land/Configuring/Basics/Window-Rules
mado  W04  S097  raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml
```

```
bash scripts/sources-census.sh shared --root /home/vgpnk/Projects/shokunin <same 21 dirs>
```

Exit 0, 8 shared keys. The only jj/git/Python key among them is `docs.jj-vcs.dev/latest/git-compatibility` (mori, souji, tameshi). Also shared, and not this round's manuals: `git-scm.com/docs/git`, `git-scm.com/docs/git-merge-base`, `git-scm.com/docs/git-symbolic-ref`, `git-scm.com/docs/git-rev-parse`. No `git-commit`, `git-add`, `git-push`, cpython, util-linux, or bash key is shared.

Same `url_of` via gawk over the 21 registries: 713 rows that carry a URL, 661 distinct keys. Every candidate below was looked up in that map.

## Tag pins (read-only `git ls-remote`)

```
git ls-remote https://github.com/git/git refs/tags/v2.56.0 'refs/tags/v2.56.0^{}'
2478544319491bbd2a42cc57a83e3d2f4730a280  refs/tags/v2.56.0
a018953688f1b10bddf91bff8747068f5f4746a4  refs/tags/v2.56.0^{}

git ls-remote https://github.com/jj-vcs/jj refs/tags/v0.45.1 'refs/tags/v0.45.1^{}'
7c41cdeb16b6b321c64e789a966b6adf723816a5  refs/tags/v0.45.1

git ls-remote https://github.com/python/cpython refs/tags/v3.14.8 'refs/tags/v3.14.8^{}'
992560c2cc62d47b308cec662feb485456847931  refs/tags/v3.14.8
8e6e75d9102e39bed2a2b279203a396741180f12  refs/tags/v3.14.8^{}

git ls-remote https://github.com/util-linux/util-linux refs/tags/v2.42.4 'refs/tags/v2.42.4^{}'
a1d2b6980b84f38b389a6d6dda4a9623f47d13be  refs/tags/v2.42.4
d76cbf8f13e65ff657344f7f6a90042cf755ba59  refs/tags/v2.42.4^{}
```

`v0.45.1` returned no peel line. `v2.56.0`, `v3.14.8`, and `v2.42.4` are annotated: the tag object and the commit are different census keys if someone puts the OID in the path.

## Cite vs open

`CORPUS.md` (shape rules): a knowledge `source:` cites an `S###` in that lane's own `SOURCES.md`. A sibling id cannot be mado's citation. "Cite" below means "do not open a second row; point at an existing mado id". There is no such mado id. "Open" means a first mado row. None of these are re-opens, and none should say `supersedes`.

| Claim | Census key to admit | In any registry? | Do this |
|---|---|---|---|
| `git commit` dry-run / `-n` | `raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-commit.adoc` | no | Open once |
| `git add -n` | `.../v2.56.0/Documentation/git-add.adoc` | no | Open |
| `git push -n` | `.../v2.56.0/Documentation/git-push.adoc` | no | Open |
| `git <sub> -h/--help` before the subcommand | `.../v2.56.0/git.c` (tag form) | no, and `github.com/git/git/tree/v2.56.0` is also absent | Open one row on the tag file URL, not the tree URL |
| jj help vs snapshot, `jj git push --dry-run` | tag raw `cli/src/cli_util.rs`, `cli/src/commands/git/push.rs`, tag `docs/cli-reference` | those paths absent. `docs.jj-vcs.dev/latest/cli-reference` is mori `S045` | Open the tag file. Do not cite mori `S045` |
| `frozenset` / `set` / `tuple` | `raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/functions.rst` | no. `Doc/library/functions.rst` at that tag is HTTP 404 | Open the builtins path. Do not cite souji `S050` |
| `deque` / `Counter` / `namedtuple` | `.../v3.14.8/Doc/library/collections.rst` | no | Open |
| `shlex.join` | `.../v3.14.8/Doc/library/shlex.rst` | no | Open |
| `subprocess` `args` vs `args=` | `.../v3.14.8/Doc/library/subprocess.rst` | no | Open. Do not cite kama `S044` or tameshi `S049` |
| unshare / mount without a root mapping | `raw.githubusercontent.com/util-linux/util-linux/v2.42.4/sys-utils/unshare.1.adoc` and `.../mount.8.adoc` | no (tag form and peeled-commit form) | Open. Do not cite tsukuroi `S059` |
| `set -e` and `&&` / `\|\|` | `cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?h=bash-5.3` | no (pre-redirect host also absent; tarball URL absent) | Open one row on the post-redirect URL. Do not cite souji `S043` |

### Sibling rows that are not the same key

Same section or same project, different `url_of`, different claim. Citing them would attach the wrong scope; copying their URL into mado would be a cross-lane `shared` hit and still would not teach E2/E4.

- souji `S043` `corpus/SOURCES.md:59` (file sha256 `25c91f68e22aa36f19311b7693db47ae4aca2f3af7c4dcbe086da7869db21f82`). Key `www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html`. Scope is `` `-n` parse-only ``, teaches "`bash -n` reads commands without executing them". Anchor: live gnu.org page unreachable 2026-10-20. Not the `set -e` exception list. mado's own `S043` (`corpus/SOURCES.md:55`) is "Wayland core registry specification" with key `wayland.freedesktop.org/docs/html/apa.html` (fragment `#protocol-spec-wl_registry` stripped). A mado teaches-line `supersedes S043` would name the Wayland row.
- souji `S050` line 66. Key `docs.python.org/3/library/functions.html` (`#compile` stripped). Scope is `compile()` without execution. Anchor says the page opened was Python 3.15.0 documentation. Not `frozenset` at tag `v3.14.8`.
- kama `S044` line 56 (sha256 `d821f66b89714522168c2c46efbb311f1e9f37f3aba61d4076a068f708276d6a`). Key `docs.python.org/3.14/library/subprocess.html`. Scope is `Popen.returncode` on a page titled Python 3.14.8. Not the `args` / `args=` parameter.
- tameshi `S049` line 58 (sha256 `ac82b2df0ffd44f4e3e74e90cdae2a2eac6bc72ed557dd428c45397f97c828d5`). Key `docs.python.org/3/library/subprocess.html`. Scope is `run()` `env`. Anchor: Python 3.15.0 docs served 2026-10-20.
- mori `S045` line 51 (sha256 `59c6d4a14a258037125eaced3b828a132cbc45ce758aad791dc0455e91cc381f`). Key `docs.jj-vcs.dev/latest/cli-reference`. Scope is `metaedit --update-author`. Not `jj git push --dry-run`, and `latest` is not tag `v0.45.1`.
- tsukuroi `S059` line 65 (sha256 `764d59c56bbd242d97677120d18ff58ff9eaa7bf9b88f0493739999b7a40a900`). Own-work capture, no URL. The source cell mentions "util-linux 2.42.4" as the `findmnt`/`mount` binary identity in an overlay emulation. Not `unshare.1.adoc` or `mount.8.adoc`.
- souji `S004` line 20 cites `Documentation/git-repack.adoc` at tag `v2.56.0` in the anchor; the census key is `git-scm.com/docs/git-repack`. souji `S009` line 25 names `builtin/commit.c` at tag `v2.55.0` but the key is `github.com/git/git/blob/v2.55.0/builtin/gc.c`. souji `S010` line 26 is `github.com/git/git/tree/master/Documentation/RelNotes`. None of those is `git-commit.adoc`, `git.c`, or `parse-options.c` at `v2.56.0`.

### Why "no W04" is not "nobody opened this document"

Three lanes already opened jj `v0.45.1` `docs/git-compatibility.md` under three keys, and `shared` connects only one of them:

- kaidoku `S036` line 42 (sha256 `e798df5cf32e814a6cb3565978bda31e52d1862f8a1221dc8c931e2635bf3e41`): first URL `raw.githubusercontent.com/jj-vcs/jj/v0.45.1/docs/git-compatibility.md`. The rendered `docs.jj-vcs.dev/v0.45.1/...` URL is second, so it is not the key.
- souji `S051` line 67: first URL `docs.jj-vcs.dev/latest/git-compatibility`. The same raw tag URL is second, so `shared` does not pair souji with kaidoku.
- tabi `S049` line 63 (sha256 `81f849da8c78c5e496b5d3973a6a4f47fb1823dfc163f2e5e80c8d845767fa55`): first URL `docs.jj-vcs.dev/v0.45.1/git-compatibility`.
- `shared` prints `docs.jj-vcs.dev/latest/git-compatibility` for mori `S044`, souji `S051`, tameshi `S061` only.

kake `S008` line 16 (sha256 `b30b5d9f3810b47f07aa914b936a0bbfcac310749d5fb6296e9f86eb2c62c4b5`) already uses the post-redirect savannah host `cgit.git.savannah.gnu.org`, for tar, not bash. A bash row that stores `git.savannah.gnu.org` will not match a row that stores `cgit.git.savannah.gnu.org`.

## Drafts already on disk (intra-wave, not yet registry rows)

Fetched keys are pairwise distinct, so they will not W04 each other. Two drafts will not be seen by W04 even when the bytes are the same document.

- `SrcGitCommitDoc` draft (`w1/reports/SrcGitCommitDoc.md:63`) keys `.../v2.56.0/Documentation/git-commit.adoc`. `SrcGitAddPushDoc` fetched that same file (both bodies sha256 `ec670cfacaf3df8745e9cfe2fa68b74247cb111e4208e1a0095036732cb5e717`, 21772 bytes) and did not draft a row for it (`w1/reports/SrcGitAddPushDoc.md:114-115` are add and push only). Keep a single commit row.
- Add and push drafts are one URL each, the tag raw file. Open both.
- `SrcGitHelpSource` draft (`w1/reports/SrcGitHelpSource.md:99`) keys `github.com/git/git/tree/v2.56.0` while the bodies were fetched at the peel `a018953688f1b10bddf91bff8747068f5f4746a4`. `parse-options.h` was also fetched as `.../v2.56.0/parse-options.h` by `SrcGitAddPushDoc`. Both files sha256 `87e2be30e54631812165cf2e489116fe476e5edce7b92221dd1f4cdfa0e2d6d1`, 19624 bytes. Census will not treat the tree URL, the tag URL, and the peel URL as one row.
- `SrcPyBuiltins` drafts (`w1/reports/SrcPyBuiltins.md:63-64`) key `Doc/builtins/functions.rst` and `Doc/library/collections.rst` at `v3.14.8`. The assigned `Doc/library/functions.rst` URL is a 404 in that seat's receipt. Open the two drafted keys.
- `SrcPyShlex` drafts (`w1/reports/SrcPyShlex.md:142-143`) each put two URLs in the source cell. `url_of` keeps `shlex.rst` and `subprocess.rst`. `Lib/shlex.py` and `Lib/subprocess.py` will not be duplicate-checked.
- `SrcBashErrexit` draft (`w1/reports/SrcBashErrexit.md:78`) source cell is `GNU Bash 5.3 Reference Manual — §The Set Builtin, -e (doc/bashref.texi)` with no `https://` URL, so the census key is empty. Receipt `fetch/SrcBashErrexit/receipts.jsonl` (sha256 `744994af901cd3e36c6518e831641f07a0dca7041090996fc0667a09ead62977`): requested `https://git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?h=bash-5.3`, `final_url` `https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?h=bash-5.3`, HTTP 200, body sha256 `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5` (recomputed on the stored `bashref.texi`). The receipt says the `bash-5.3.tar.gz` member matches that digest; the tarball is a second URL (`ftp.gnu.org/gnu/bash/bash-5.3.tar.gz`) and was not stored (over 1 MiB). Seat ls-remote in that report: tag `bash-5.3` = `b8c60bc9ca365f8261fa97900b6fa939f6ebc303`, no peel line. I did not re-run that savannah ls-remote.

`fetch/SrcJjHelp/` and `fetch/SrcUnshare/` had bodies and no `receipts.jsonl` at this scan, and neither seat had a `w1/reports/Src*.md`. Their exact fetched URLs are [UNK]. Path fragments `cli_util.rs`, `commands/git/push.rs`, `unshare.1`, `mount.8`, and `util-linux/util-linux` do not occur in any registry row.

## Proposed move

Admit each round-20 source row with exactly one `https://` URL in the source cell, and make that URL the tag-pinned file that was fetched.

- git add, push, commit: the three `raw.githubusercontent.com/git/git/v2.56.0/Documentation/*.adoc` URLs already drafted, one row each. Do not add a second commit row.
- git help: replace `github.com/git/git/tree/v2.56.0` with `https://raw.githubusercontent.com/git/git/v2.56.0/git.c`. Name `parse-options.c`, `builtin/help.c`, and `Documentation/gitcli.adoc` as paths in the anchor, not as more `https://` URLs. Do not key the row on the peel `a0189536…`.
- Python: keep the four tag raw doc URLs (`Doc/builtins/functions.rst`, `collections.rst`, `shlex.rst`, `subprocess.rst`). Move `Lib/shlex.py` and `Lib/subprocess.py` out of the source cell into the anchor. Give a `.py` its own row only if that file is a separate claim.
- bash: put only `https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?h=bash-5.3` in the source cell (the receipt `final_url`, query kept). Do not also put the pre-redirect host or the tarball URL in that cell.
- jj and unshare, when their drafts arrive: same rule, tag name `v0.45.1` / `v2.42.4` in the raw path, not `latest` and not the peeled OID. Do not cite mori `S045` or tsukuroi `S059`.

No `supersedes S0xx` on these rows. Sibling numbers are a different lane's registry; mado `S043` is already taken by Wayland.

C2: the id L1 records is the file whose bytes were hashed, and W04/E04 can see a second row that reuses it. C1: no tripwire change. Coverage: all five families still open; nothing is dropped because a sibling has a nearby page.

## Risks

- One URL per cell means `Lib/subprocess.py` will not trip W04 until it has its own row. That is the point of the rule; a parenthetical second URL looks registered and is not.
- Keying the help row on `git.c` does not dedupe `parse-options.c`. The tree URL would false-collide with any later "v2.56.0 tree" row and still would not catch a raw-file duplicate.
- `git.c` byte equality between `.../v2.56.0/git.c` and `.../a0189536…/git.c` was not re-downloaded here. [INFERENCE] from the peel. Observed byte equality is only `parse-options.h` (both URLs, same sha256).
- jj and unshare drafts were not present. A draft that copies mori `S045`'s `latest` URL would `shared`-match a metaedit row and still miss the dry-run claim.
- Putting `supersedes S043` on the bash row to "replace" souji's `-n` page would supersede mado's Wayland `S043` in the only registry that string can refer to. The census `supersedes` check is a same-file regex; it does not resolve another lane.

## Verification

Done this round, read-only:

- `validate` exit 0, 0 `E04`, 32 `W04`, no candidate key.
- `shared` exit 0, 8 keys, no candidate file key.
- gawk `url_of` lookup: the admit-these keys are absent; the five alias keys above are present once each.
- `git ls-remote` for the four GitHub tags.
- sha256 of the two `git-commit.adoc` bodies and the two `parse-options.h` bodies.

After L1 appends rows, re-run `validate` on mado: each new key appears once, or a second row in another scope is the expected `W04` and a second non-rejected row in the same scope without `supersedes` is `E04`. Then `shared` across the 21 lanes: the new raw tag URLs should not appear (they were absent), and the new bash key should not appear.

## Limits

- Absence claims are first-URL census keys, plus a full-file fragment scan for `Documentation/git-commit`, `git-add`, `git-push`, `parse-options.c`, `cli_util.rs`, `commands/git/push.rs`, `Doc/library/shlex`, `unshare.1`, `mount.8`, `bashref.texi`, `bash-5.3`. Anchor prose can name a path without becoming a key. souji `S004` / `S009` / `S010` are that case.
- `SrcJjHelp` and `SrcUnshare` had no receipts and no reports. Their URLs are [UNK].
- Savannah `bash-5.3` → `b8c60bc9…` is the seat's ls-remote, not re-run here. The stored texi digest was recomputed.
- Did not re-fetch candidate URLs and did not read sibling `corpus/knowledge/` for a `set -e` quote outside the registry scope/teaches cells.
- Scout reports were still being written; draft line numbers are from this read (`SrcPyShlex.md` rows at 142–143, bash draft at 78, help draft at 99).
- Did not run tripwire suites, `measure.py`, or the live gate.

## Installs

none
