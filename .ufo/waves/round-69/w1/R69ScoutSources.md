# R69ScoutSources — source opening and registry reconnaissance (read-only)

- lane/round: mado r69, w1, seat `R69ScoutSources`; axis C2 (operability), sourced ground for
  `corpus/knowledge/gate-guard-dominance-r69.md` + registry row **S438**.
- base rev: `04093b83f73a841117d3b31dbb2a6063f4f2a454`. Lane HEAD observed during the seat:
  `98bff016d0ef151aceedf03d75239b81c9f6eeed` (freeze commits `789a87f1`, `98bff016` sit above base;
  `corpus/SOURCES.md` is unchanged between base and worktree: `git diff 04093b83 -- corpus/SOURCES.md`
  → 0 lines, blob sha256 `19c5004c018d4991d1ddc8d2f4c630eeec9f086c354e90384c0112efe5cab4bb` both sides).
- frozen declaration: `.ufo/waves/round-69/claims-declaration-r69.md`, sha256
  `ecd481ae3e21ff5653d21a1b2151bf95d327b1689d3a861172f047d83d924b43` (read first, never edited).
- receipt: `.ufo/waves/round-69/w1/R69ScoutSources/sources-r69.json` (10,280 B, sha256
  `2306b5a5885c90af53ffdbca5806646c01b38bb0f6cd92a7bcafa0a496e332d3`).
- writes: only the two files above plus `/fast/scratch/hyaku/mado-r69/R69ScoutSources/` (removed before
  yield; see § 7). No production path, no git/jj mutation, no package manager, no desktop probe.

## 1. Source fetch — three times, byte-identical

| attempt | command shape | curl rc | HTTP code | bytes | sha256 |
|---|---|---|---|---|---|
| 1 | `curl -sS -o git-adoc-1.txt -w '%{http_code} %{size_download}' <URL>` | 0 | 200 | 47,005 | `050c5330f1a231be22bee3db27c7ef90d8ba22bb7bd6c72c8bab462f6f0a1f79` |
| 2 | same | 0 | 200 | 47,005 | same |
| 3 | same | 0 | 200 | 47,005 | same |

`cmp git-adoc-1.txt git-adoc-2.txt` rc 0; `cmp git-adoc-2.txt git-adoc-3.txt` rc 0. URL:
`https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc`.

HTTP layer (separate `curl -I`, rc 0): `HTTP/2 200`, `content-type: text/plain; charset=utf-8`,
`content-length: 47005`, `etag: "ec0023fea0cdcf4699330e260c89caf8a0d9baad3fc9a4b57fa9ecd293c4e6a6"`,
`remote_ip 2606:50c0:8003::154`.

Tag pin (`git ls-remote https://github.com/git/git 'v2.56.0' 'v2.56.0^{}'`, rc 0): tag object
`2478544319491bbd2a42cc57a83e3d2f4730a280`, peeled commit
`a018953688f1b10bddf91bff8747068f5f4746a4` — identical to the pin already carried by
S099/S100/S101/S436/S437.

## 2. The two passages (verbatim, 1-based lines)

**Q1 — `--no-replace-objects`, block at `git.adoc:178-181`; quote at :180-181.**

```
176|	directory.
177|
178|--no-replace-objects::
179|	Do not use replacement refs to replace Git objects.
180|	This is equivalent to exporting the `GIT_NO_REPLACE_OBJECTS`
181|	environment variable with any value.
182|	See linkgit:git-replace[1] for more information.
183|
184|--no-lazy-fetch::
```

Quote: "This is equivalent to exporting the `GIT_NO_REPLACE_OBJECTS` environment variable with any
value." — 12 words, 1 occurrence in the file.

**Q2 — `GIT_NO_REPLACE_OBJECTS` env entry, block at `git.adoc:927-929`; quote at :928-929.**

```
925|	redaction.
926|
927|`GIT_NO_REPLACE_OBJECTS`::
928|	Setting and exporting this environment variable tells Git to
929|	ignore replacement refs and do not replace Git objects.
930|
931|`GIT_LITERAL_PATHSPECS`::
932|	Setting this Boolean environment variable to true will cause Git to treat all
933|	pathspecs literally, rather than as glob patterns. For example,
```

Quote: "Setting and exporting this environment variable tells Git to ignore replacement refs and do
not replace Git objects." — 18 words, 1 occurrence in the file.

Both declared fragments are present: "is equivalent to exporting the `GIT_NO_REPLACE_OBJECTS`
environment variable" (:180) and "setting and exporting" (:928). **Case nit for the scribe:** the
declaration writes "setting and exporting" lower-case; the source capitalizes it ("Setting and
exporting"). Quote the source case in the row and the knowledge file.

## 3. Registry reconnaissance at base rev

| step | command | observed | rc |
|---|---|---|---|
| census | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | 38 output lines: 36 × `W04` duplicate-url warnings, 1 × `W01` (`S277 tierC mined`), summary line below | **0** |
| rows | `git show 04093b83:corpus/SOURCES.md \| grep -cE '^ {0,3}\| *S[0-9]'` | **374** (worktree identical: 374) | 0 |
| ids | `git show 04093b83:corpus/SOURCES.md \| grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' \| grep -oE 'S[0-9]+' \| sort` | S001…S437, 374 unique, 0 duplicates | 0 |

Summary line (tab-separated, exact):

```
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
```

Highest id: **S437**. Next free id: **S438** (`grep -c '^S438$'` on base ids = 0; also absent from the
staged package ids).

**Id collision.** The frozen declaration contains **no** collision command
(`grep -c collision claims-declaration-r69.md` → 0; `grep -n shokuknow` → only line 183). I therefore
ran the lane's own frozen extraction convention (round-32 `ExecCollisionGuard`, re-run in round-67
`R67ConnSiblings`):

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 04093b83f73a841117d3b31dbb2a6063f4f2a454:corpus/SOURCES.md \
  | grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' | grep -oE 'S[0-9]+' | sort > reg-ids.txt
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md \
  | grep -oE 'S[0-9]+' | sort > staged-ids.txt
comm -12 reg-ids.txt staged-ids.txt > collisions.txt; wc -l collisions.txt
```

Observed: `reg=374 staged=147 collisions=94`; staged range S203–S349, 147 unique, no in-set
duplicates; the 94 collisions span the whole staged range (S203…S349); 53 staged ids are free but
interleaved. **Adoption: none** (declaration line 183), so the adopted collision count is
**collisions=0**; the 94/147 is the counterfactual if the set were adopted. This reproduces the
round-67 finding exactly.

## 4. Duplicate-URL check

- `git.adoc` occurrences in `corpus/SOURCES.md` at base: **0**. `git-scm.com` rows: **0**. Exact URL
  `raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc`: **not present**.
- Same repo/tag/documentation family (different filenames, so family precedent, not duplicates):
  S099 `git-commit.adoc` (:111), S100 `git-add.adoc` (:112), S101 `git-push.adoc` (:113),
  S436 `git-replace.adoc` (:386), S437 `git-cat-file.adoc` (:387).
- **Content overlap, resolved as distinct.** S436 (git-replace.adoc) already states
  "--no-replace-objects and GIT_NO_REPLACE_OBJECTS make a command read the real objects", but its
  document's only env sentence is `git-replace.adoc:55-56` "The `GIT_NO_REPLACE_OBJECTS` environment
  variable **can be set** to achieve the same effect as the `--no-replace-objects` option" — no export
  requirement (0 occurrences of "export" in that file). `git.adoc:928-929` is the only passage saying
  "Setting and exporting"; that export clause is the dominance ground, so S438 is a different document
  carrying a clause no row holds.

**Verdict: no duplicate. S438 is admissible and correctly numbered.**

## 5. Rejected candidate(s), located

1. **`https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/ast.rst`** — HTTP 200,
   curl rc 0, **92,619 B**, sha256
   `9908f4f029c3258bdfb9ffa6af69d2bca5bd17ff2f175f92a71303d43699ab85`. Read: the Python "Abstract
   syntax trees" reference (`:mod:`ast``; anchors `abstract-grammar:30`, `ast-expressions:531`,
   `ast-statements:926`, `ast-cli:2608`). Counts: `GIT_NO_REPLACE_OBJECTS`/`replacement ref` = 0;
   `git` (case-insensitive) = 1, and that single hit is line 2685, a `leo-editor.github.io` link host
   (substring only); `replac` = 4 and all four are AST-node replacement (lines 155, 2466, 2468, 2469,
   visitor semantics). It documents language ASTs, not git environment semantics — **REJECT**
   (generic, lane-external; cannot ground the dominance predicate).
2. **`Documentation/git-replace.adoc` @ v2.56.0** (5,398 B, sha256
   `3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631`; `GIT_NO_REPLACE_OBJECTS` at
   :55-56, `export` count 0). **REJECT as the ground for this claim**: "can be set" does not state
   that the variable must be exported into the child environment; it is already S436 for a different
   clause.

## 6. Verdict

**ADMIT S438.** Conditions: URL new at base; id S438 unused at base and in the staged set (max S437);
both quotes verbatim at the cited 1-based lines, one occurrence each; bytes/sha256 stable across three
fetches with HTTP 200 / curl rc 0; tag pin matches the existing git rows.

Row record fields this seat certifies: anchor `git.adoc:178-181, :927-929 @ tag v2.56.0`; sha256
`050c5330f1a231be22bee3db27c7ef90d8ba22bb7bd6c72c8bab462f6f0a1f79`; 47,005 bytes; fetched
2026-11-03/04 (America/Sao_Paulo).

Residual unknowns: none for this seat. Not claimed: that the manual's export clause is enforced by git
at runtime (the declaration's § Not claimed already excludes runtime truth), and that the 36 `W04`
duplicate-url warnings are all benign (pre-existing, outside this seat's scope; census rc is 0).

## 7. Scratch

`/fast/scratch/hyaku/mado-r69/R69ScoutSources/` held the three fetches, `cpython-ast.rst`,
`git-replace.adoc`, the census capture and the id lists; it was removed before yield
(`rm -rf -- "$S"`), and `test -e` afterwards confirms absence.
