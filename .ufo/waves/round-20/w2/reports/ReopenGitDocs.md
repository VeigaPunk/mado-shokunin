# ReopenGitDocs — partly falsified: S099's Gate quote is 16 words, not 14; every pin, digest, quote, and substantive claim otherwise holds

Seat: ReopenGitDocs (wave 2, FALSIFY). Question: re-open SOURCES rows S099/S100/S101
and their Gate lines in `corpus/lessons/round-20.md`, re-fetch each pinned URL, compare
sha256 with row + receipt, check the located quote verbatim at the stated lines and
<= 25 words, check the tag→commit pin, and say whether each row supports what
`corpus/knowledge/tripwire-precision-r20.md` and `SKILL.md` claim it supports.

Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`, tip `a4046a8`. All fetches below
were made 2026-10-20T20:37–20:40Z into
`.ufo/waves/round-20/w2/ReopenGitDocs/fetch/` (6 receipt lines, schema
`mado-fetch-receipt-v1`, curl 8.23.0). Empirical git work was done in
`/tmp/mado-r20w2-ReopenGitDocs/lab-git` with `HOME` and all git config redirected under
/tmp; the lane was cloned to `/tmp/mado-r20w2-ReopenGitDocs` and `origin` removed
(`a4046a82…`). No lane file was written except this report.

## 1. Re-fetch, byte and digest

Fresh `curl` of the three pinned URLs returned 200 and reproduced the recorded bytes and
digests exactly:

| row | file | bytes | sha256 (fresh = row = receipt) |
|---|---|---|---|
| S099 | `Documentation/git-commit.adoc` @ v2.56.0 | 21,772 | `ec670cfacaf3df8745e9cfe2fa68b74247cb111e4208e1a0095036732cb5e717` |
| S100 | `Documentation/git-add.adoc` @ v2.56.0 | 16,586 | `42089b80b378a7e9711dde024b7ec94a6863378164ea434a34c6af07632e65db` |
| S101 | `Documentation/git-push.adoc` @ v2.56.0 | 32,212 | `b68851f83be3624cba85e8e620e6271b566c4d5d818d44b4b59eb3335e6ec64c` |

The w1 receipts agree: `fetch/SrcGitCommitDoc/receipts.jsonl` line 1 (git-commit.adoc,
21,772 B, `ec670cfa…`, 200, 19:44:20Z) and `fetch/SrcGitAddPushDoc/receipts.jsonl`
lines 1–2 (git-add.adoc 16,586 B `42089b80…`; git-push.adoc 32,212 B `b68851f8…`, both
200, 19:43:39–40Z). I also re-hashed every stored body my line reads rely on; all match
their receipts: `builtin-commit-v2.56.0.c` `e566f209…`, `add.c` `c96956fd…`,
`push.c` `a6c0dc07…`, `parse-options.h` `87e2be30…`, `read-cache.c` `d4d9584c…`,
`transport.c` `760ca671…`, `githooks.adoc` `c3aff486…`.

## 2. Tag → commit pin

```
$ git ls-remote https://github.com/git/git refs/tags/v2.56.0 'refs/tags/v2.56.0^{}'
2478544319491bbd2a42cc57a83e3d2f4730a280	refs/tags/v2.56.0
a018953688f1b10bddf91bff8747068f5f4746a4	refs/tags/v2.56.0^{}
```

This is exactly the tag object / peeled commit stated in all three rows. I additionally
fetched each doc by the peeled commit
(`https://raw.githubusercontent.com/git/git/a0189536…/Documentation/…`) and `cmp`-ed:
`commit_same`, `add_same`, `push_same` — the tag URL and the peeled-commit URL serve
byte-identical content, so the pin is not just declared, it resolves.

Host side of the pin also matches: `git --version` → `git version 2.56.0`, `/usr/bin/git`
sha256 `2912a2a32f408c9b8122e476251b32f4b35f4c3f0c15961686ae87ca456d384c` (4,968,112 B),
`/var/lib/pacman/local/git-2.56.0-1/desc` `%VERSION%` `2.56.0-1` — the row's "tag
matching the host git" claim is true.

## 3. Quote and line checks

Line extraction is from my fresh bodies; whitespace-normalized for display.

**S099 `git-commit.adoc:378-381`** — stated: "Do not create a commit, but show a list of
paths that are to be committed" (14 words).

```
378  `--dry-run`::
379      Do not create a commit, but show a list of paths that are
380      to be committed, paths with local changes that will be left
381      uncommitted and paths that are untracked.
```

- Text is verbatim, in order, within the stated range, and <= 25 words.
- **Word count is 16, not 14** (`Do not create a commit, but show a list of paths that are
  to be committed`). This is the only false statement I found in the three Gate lines.
- The quoted text begins at :379; :378 is the option label. The row and Gate line both
  present :378-381 as the quote's range without the "(quote at :379-381)" qualifier the
  S100/S101 rows use. Minor anchor imprecision.
- The quote silently stops mid-sentence: the source continues
  "`, paths with local changes that will be left uncommitted and paths that are
  untracked.`" with no ellipsis. The dropped continuation also supports non-write
  (it names paths left uncommitted), so the truncation does not invert meaning.

**S099 `git-commit.adoc:218-221`** — `-n` / `--verify` / `--no-verify` labels at :218-220,
`Bypass the `pre-commit` and `commit-msg` hooks.` at :221. Verbatim; the Gate line's
`-n … --no-verify …` composition is an ellipsis of real tokens, not a fabricated quote.
This supports `commit -n` = `--no-verify`.

**S100 `git-add.adoc:67-70` (quote at :69-70)** — :67 `-n`::, :68 `--dry-run`::, :69-70
`Don't actually add the file(s), just show if they exist and/or will be ignored.`
Verbatim, 14 words as stated, <= 25. Exact.

**S101 `git-push.adoc:161-163` (quote at :163)** — :161 `-n`::, :162 `--dry-run`::, :163
`Do everything except actually send the updates.` Verbatim, 7 words as stated, <= 25.
Exact.

So: all three quotes are real, and the <= 25-word gate is met even for the miscounted one;
only the S099 word count (and the :378 start-of-quote convention) is wrong.

## 4. Do the rows support the knowledge note and SKILL?

The rows are much richer than their Gate lines: S099 cites `:144-146` (`--short` "Implies
`--dry-run`"), `:152-155` (`--porcelain`), `:157-160` (`--long`), `:162-166` (`-z`/`--null`
"If no format is given, implies the `--porcelain` output format"), the binding
`builtin/commit.c` `:1750` (`OPT_BOOL('n', "no-verify", …)`), `:1751`
(`OPT_BOOL(0, "dry-run", …)`), `:1725` (`-s` = signoff), `:1422-1423`
(`if (status_format != STATUS_FORMAT_NONE) dry_run = 1;`), `:1836-1837` (early
`dry_run_commit` return), plus a host observation. I verified every one of those lines in
the receipt-matched source; each is at the stated line and says what the row says.
S100's bindings (`builtin/add.c:262` = `OPT__DRY_RUN`, `parse-options.h:568` =
`OPT_BOOL('n', "dry-run", …)`, `read-cache.c:735` = `hash_flags = pretend ? 0 :
INDEX_WRITE_OBJECT`, `:812-817` = `if (pretend) discard_cache_entry` else add) and the
`:157-163`/`:176-180` boundaries (`-N` intent-to-add; `--ignore-missing` only with
`--dry-run`) are at the stated lines and match. S101's `push.c:716`
(`OPT_BIT('n', "dry-run", … TRANSPORT_PUSH_DRY_RUN)`), `transport.c:1497` (get remote
refs = contact), `:1525-1526` (`run_pre_push_hook` with no dry-run guard), `:1599-1607`
(tracking-ref update skipped when `TRANSPORT_PUSH_DRY_RUN`) are all at the stated lines.

Claim-by-claim answer:

| note/SKILL claim | row support | my reproduction |
|---|---|---|
| `git commit --dry-run` (also `--short`, `--porcelain`, `--long`, `-z`) is not a write (note §2 table; SKILL §round 20) | S099 row: yes — the four implications are cited at :144-166 and commit.c :1422-1423. **The note's inline pointer `S099 :378-381` covers only `--dry-run`; the "(also …)" support is the same row's other lines, not :378-381.** | all five forms: `head_moved=no`; `commit --short --no-dry-run` also does not commit; `--short --no-short`, `-z --no-null` do commit and are flagged by the tool |
| no ref or index *entry* change, while "a tree object and the index cache may be rewritten" (note §2) | S099 row + commit.c `dry_run_commit` → `prepare_index(..., 1)` then `rollback_index_files` | HEAD unchanged; `git ls-files -s` entry byte-identical; one new `tree` object written by `--dry-run` — exactly the stated hedge |
| `git commit -n` is `--no-verify` and **writes** (note §2; SKILL "still writes") | S099 :218-221; :1750 | `git commit -qm msg -n` → `moved=yes` |
| `git add -n` stages nothing (S100; note says "measured: index bytes unchanged") | S100 :67-70, add.c:262, parse-options.h:568, read-cache.c:735/:812-817 | index sha256 and `ls-files -s` unchanged; `add 'f'` printed only |
| `git push -n` changes no ref, **skips remote-tracking writes, still runs pre-push** (S101; SKILL "pre-push hook still runs") | S101 :161-163 + transport.c :1497/:1525-1526/:1599-1607 | remote master unchanged, `origin/master` unchanged, `prepush_hook_ran=yes`; `--no-verify` → `prepush_hook_ran=no`; control real push moved remote and ran hook |
| `--branch` / `--ahead-behind` / `-s` write; `--show-stash` is not a commit option (row's measured list) | S099 row measured clause | `--branch -m` and `--ahead-behind -m` both moved HEAD; `git commit --show-stash` → rc 129 `unknown option` |

No row over-claims. The one support gap is in the note, not the rows: the note's citation
for its `--short/--porcelain/--long/-z` parenthetical points at :378-381, while the
supporting lines are :144-166 (cited by the S099 row, but not by the note's table cell).

## 5. Counterexample hunt (would have shown the opposite)

I fed eleven forms to the tool at `28c6837` from the /tmp clone
(`tools/mado-tripwire.py` sha256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`,
confirmed via `git show 28c6837:…` and `git show a4046a8:…`; at `1f7f995` it is
`367be947…`). Result: `MADO_TRIPWIRE: findings`, 11 bash calls, 7 `vcs_write`
(`evidence: observed`) — lines 3, 6, 7, 8, 9, 10, 11:

```
line  3 git:commit :: git commit -n -m x
line  6 git:commit :: git commit --branch -m x
line  7 git:commit :: git commit -m --short          (the token is the message; git writes)
line  8 git:commit :: git commit -m x --short --no-short   (git writes)
line  9 git:commit :: git commit -m x -z --no-null         (git writes)
line 10 git:commit :: git commit --short --no-dry
line 11 git:commit :: git commit -m x --porcelain --no-porcelain  (git writes)
```

Lines 1, 2, 4, 5 (`commit --short`, `commit -z`, `add -n`, `push -n`) produced no row.
Every classification matches git's measured behavior except line 10: with
`--short --no-dry`, git does **not** commit (status format forces `dry_run = 1` after
parse) but the tool reports a finding. That is the documented conservative choice in the
tool's own docstring ("an abbreviated negation (`--no-dry`) keeps the finding") — a
recall-safe false positive, not a row or SKILL contradiction.

Non-forms also behave sanely: `git commit -z --long` dies rc 128 with no commit and the
tool gives no row (outcome correct though for the conflict reason, not dry-run);
`git add -n` and `push -n` emit no row, matching the rows.

## 6. The one defect, precisely

Both `corpus/SOURCES.md:111` and `corpus/lessons/round-20.md:36` quote the `--dry-run`
text verbatim, but `corpus/lessons/round-20.md:36` annotates it **"(14 words)"**; the
quoted string is **16 words**. The range `:378-381` also begins on the `--dry-run`:: label
(:378) rather than on the quote (:379), whereas S100/S101 explicitly say "quote at
:69-70"/":163". Suggested append-only correction: change "(14 words)" to "(16 words)" and
either say "quote at :379-381" or retain the option-block convention explicitly. This does
not overturn admission: the quote is verbatim, well under 25 words, tag- and sha-pinned,
and every substantive claim behind it reproduces.

## 7. Limits

- I did not run `tw-precision.py` / `tw-recall.py` or the 11 suites; other wave-2 seats
  own C1/C2. I ran only the tool scan of my eleven synthetic forms.
- Network reachability: raw.githubusercontent.com and github.com only; no GitHub UI/tree
  pages were used as anchors.
- The empirical claims are reproduced on the host's git 2.56.0; behavior of other git
  versions is not asserted.
- I read the host's `/usr/bin/git` and pacman `desc` as file bytes; no pacman command was
  run (host pause).

## Installs

none.
