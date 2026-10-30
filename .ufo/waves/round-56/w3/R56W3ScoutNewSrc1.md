# R56W3ScoutNewSrc1 — independent read of inotify_add_watch(2), diffed against the L1's S396 row

**Item attacked:** the L1's proposed registry row **S396** (`inotify_add_watch(2)` man page) in
`.ufo/waves/round-56/attempt2/s396-s397-draft.md` line 13 (row) and line 15 (gate quote), and the
draft's C3 reasoning about it.
**Seat type:** scout (leaf member — no subagent dispatch).
**Verdict:** the row's **substance AGREES** with my independent reading; its **provenance details
carry 5 defects**, and the draft's **C3 mechanism is wrong** while its outcome is right — with an
internal tension between the row's `queued`/`—` plan and the row's stated purpose.

## What I did

1. **Independently fetched** `https://man7.org/linux/man-pages/man2/inotify_add_watch.2.html`
   with curl to scratch — three times, two user agents — and sha256'd the bytes.
2. **Read the page myself** and located the lines stating (a) the unique-watch-descriptor-per-inode
   rule, (b) the existing-watch-returned-for-a-different-link rule, (c) the read-permission
   requirement. I also located the release the page names.
3. **Only then** read `.ufo/waves/round-56/attempt2/s396-s397-draft.md` and diffed my conclusions
   against its S396 row (quote lines, sha256, teaches wording).
4. **Ran the frozen counters against a scratch clone** to test the draft's C3 claims empirically
   rather than by reading the counter.

Full detail and every command output: `.ufo/waves/round-56/w3/R56W3ScoutNewSrc1/receipts/s396-independent.md`.
Raw transcript: `.../receipts/raw-evidence.txt`. The two fetched pages are copied beside them as
`.../receipts/inotify_add_watch.2.html` and `.../receipts/fdinfo_fetch.html`.

## Independent findings (my own reading, before the draft)

**sha256 of the bytes I fetched:**
```
98fe7feb381fa2687e8a3962e6d78a49cb1ad07c543f93449dcb42d6712c3d6d  inotify_add_watch.2.html
```
11345 B, 258 lines. 3/3 fetches identical (two UAs). `cmp` vs the lane pin → **IDENTICAL**.

**man-pages release the page names:** **man-pages 6.19** — line 155
(`This page was obtained from the tarball man-pages-6.19.tar.gz`) and line 165 (footline
`Linux man-pages 6.19   2026-02-08   inotify_add_watch(2)`). The upstream mirror lists the release
tarball as `man-pages-6.19.tar.xz  25-Aug-2026 17:43` (6.18 = 22-Apr-2026, 6.20 = 21-Oct-2026).

**The three statements, by line in the pin:**

| item | lines | text |
|---|---|---|
| (a) unique watch descriptor per inode | **88–92** | `A successful call to <b>inotify_add_watch</b>() returns a unique watch / descriptor for this inotify instance, for the filesystem object / (inode) that corresponds to <i>path</i>.  If the filesystem object was / not previously being watched by this inotify instance, then the / watch descriptor is newly allocated.` |
| (b) existing watch returned for a different link | **93–94** | `already being watched (perhaps via a different link to the same / object), then the descriptor for the existing watch is returned.` |
| (c) read-permission requirement | **82** (`EACCES` at **108**) | `caller must have read permission for this file.` / `<b>EACCES </b>Read access to the given file is not permitted.` |

Two precisions the lines carry that the draft drops: (a)/(b) are scoped **per inotify instance**
("for this inotify instance", "already being watched by this inotify instance"), and (b) is hedged
in the man page's own words — "**perhaps** via a different link".

## Diff against the S396 row: AGREES

| point | verdict |
|---|---|
| sha256 `98fe7feb…95e2` | **AGREES** (3× independent fetch, byte-identical to the lane pin) |
| byte size 11345 B | **AGREES** |
| man-pages release "6.19" | **AGREES** |
| locator lines 88 and 93 | **AGREES** |
| teaches: unique watch descriptor for the filesystem object (inode) | **AGREES** (lines 88–90) |
| teaches: already-watched object returns its existing descriptor | **AGREES** (lines 92–94) |
| teaches: a different link reaches the same descriptor | **AGREES** (lines 93–94) |
| `queued` + `used-by —`, cited only from the lesson | **AGREES as a plan** — empirically C3-green (§"Empirical" below) |
| rationale: the lane lacked a row holding the one-watch-per-inode man-page statement | **AGREES** — the only `inotify.7.html:` locator in the whole registry is `:186,262`; no row holds the lines the entry cites |

## Defects

**D1 — wrong page date in the anchor cell (weakens the claim).** S396's anchor says
`@ Linux man-pages 6.19 (2026-02-14)`. **2026-02-14 is `inotify(7)`'s (S390's) footline date.**
This page's own footline (line 165) reads `2026-02-08`. Input:
`man7-inotify.7.html:811 → 2026-02-14` vs `man7-inotify_add_watch.2.html:165 → 2026-02-08`.
The lane convention is the page's own revision date, and each page in the same 6.19 release
carries a different one. **The same wrong date is in the draft's S397 row**, whose page footline
reads `2026-07-18` (`man7-proc_pid_fdinfo.5.html:276`). Twice wrong, two rows.

**D2 — gate quotes are de-tagged and are not substrings of the pinned bytes (weakens the claim;
would block a freeze-verifier check).** The draft's line-88 quote is
`A successful call to inotify_add_watch() returns a unique watch`; the pin's line 88 is
`       A successful call to <b>inotify_add_watch</b>() returns a unique watch`. The de-tagged form
occurs **0 times** in the 258-line pin; the raw form occurs once. Under the lane's own
`freeze-verify-v2.py` rule (`q in L[line-1]` and `sum(q in x for x in L)==1`) the de-tagged quote
scores **BAD**, the raw form **ok**. The lane's existing man-page quote keeps the markup
(K30: `Don't dereference <i>pathname</i> if it is a symbolic link.`). Same defect in S397 at lines
164 and 171 (`wd`/`<i>wd</i>`, `mask`/`<i>mask</i>`): both de-tagged forms score **False** as
substrings of their lines. S397's line-160 quote is tag-free and **is** a substring (True). Four
quotes affected across the two rows. Class: M55-2 / M56-1 family.

**D3 — the pin is untracked at the tip (weakens the claim).**
`git cat-file -e 0f3a5436:.ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html` → **not
present**; `git status --porcelain` shows it as `??`. The S390 pin `man7-inotify.7.html` **is**
tracked. Until the pins are committed with the rows, the anchor names a path that does not exist at
the landing revision and the C1 counter's pin lookup cannot read it.

**D4 — the teaches cell drops the man page's per-instance qualifier (weakens the claim).** The
draft teaches "…returns a unique watch descriptor **for the filesystem object (inode)**"; the page
says "for **this inotify instance**, for the filesystem object (inode)" (88–89) and "already being
watched **by this inotify instance**" (91). The dropped qualifier is exactly the difference
between "one watch per inode" and "one watch per inode **per inotify instance**" — and the entry's
line 46 already asserts the weaker unqualified form, which is the sentence S396 is meant to ground.

**D5 — the "why the lane lacked it" rationale names the wrong gap (cosmetic).** The draft says the
entry's duplicate-path prose "was grounded only in the entry's reading of ConfigWatcher/absolutePath
pins and the kernel lab". In fact the entry attributes it to **inotify(7)** (entry line 46:
"…(inotify(7) lines 90-92 and 296-302…)"), and those two ranges do not state the rule either —
90–92 say only that each watch "has a unique watch descriptor", and 296–302 are the
`IN_MASK_CREATE` paragraph ("multiple paths may refer to the same inode, and multiple calls to
inotify_add_watch(2) without this flag may clobber existing watch masks"). A man page **was**
cited; what was missing is a *row* holding those lines. The conclusion holds; the account is wrong.

**D6 — the locator omits the lines that carry the taught propositions (weakens the claim; M56-1
class).** Running the C1 counter's own `scope_covers(anchor, "inotify_add_watch.2.html", line, 258)`
against the draft's anchor cell: line 88 → True, 93 → True, but **89 / 90 / 91 / 92 / 94 →
False**. The taught proposition "unique watch descriptor for the filesystem object (inode)" is
supported by lines 88–90; "the descriptor for the existing watch is returned" is on line 94. Both
fall outside `88,93`. A locator of `88-94` would cover the whole passage.

**D7 — the draft's C3 mechanism is wrong, and the row's plan contradicts the draft's own intent
(weakens the claim; routing item, no frozen predicate touched).** The draft says a lesson path in
`used-by` "would flip TARGET_MET to TARGET_MISSED … because the `extra` leg counts any used-by path
outside the entry set". Empirically it does **not**: with `used-by = corpus/lessons/round-56.md`,
C3 prints `entries=71 rows=334 missing=0 extra=0 … verdict=TARGET_MISSED` — no, it prints
`verdict=TARGET_MET missed=none` (exit 0). The `USED_BY` regex is
`corpus/knowledge/[A-Za-z0-9_.-]+\.md`, so a `corpus/lessons/…` path is never captured into
`usedby` and cannot produce `extra`. The direction that **does** flip C3 is the opposite:
(a) a **knowledge** path in `used-by` for a row no entry cites → `extra: S396 …`, `extra: S397 …`
→ `TARGET_MISSED missed=extra` (exit 1); (b) an **entry** citing S396/S397 while `used-by` is `—`
→ `missing: S396 …`, `missing: S397 …` → `TARGET_MISSED missed=missing` (exit 1). So the rule
that binds is the C3 contract's own: *an entry that cites a row must have that row's `used-by`
naming the entry*. The draft's outcome (`—`) is right while no entry cites the row; but the
draft's stated intent is to re-ground the **entry's** line-46 sentence on S396 — i.e. to make the
entry cite it. With `mined` + `used-by = corpus/knowledge/hyprland-config-autoreload-r56.md` I
measured `verdict=TARGET_MET missed=none` (exit 0). **The `queued`/`—` plan and the stated intent
cannot both hold.**

## Empirical checks (scratch clone; the lane was never written)

Clone: `/fast/scratch/hyaku/mado-r56/R56W3ScoutNewSrc1/clone` (`git clone --shared` of the lane,
checked out at `0f3a5436…`; `git rev-parse --show-toplevel` = the clone dir; every commit used
`-c user.name=ctl -c user.email=ctl@ctl`). All mutations were on the clone.

| # | tree | command | output |
|---|---|---|---|
| 1 | baseline `0f3a5436` | `c3-r56-used-by.py --rev 0f3a5436…` | `entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none` (exit 0) |
| 2 | `b520ac0c` draft rows verbatim | same | `entries=71 rows=334 missing=0 extra=0 … verdict=TARGET_MET missed=none` (exit 0) — **the draft's plan keeps C3 green** |
| 3 | `febfb6a5` `used-by` = lesson path | same | `… rows=334 missing=0 extra=0 … verdict=TARGET_MET missed=none` (exit 0) — **the draft's stated worry does not occur** |
| 4 | `d8319a27` `used-by` = knowledge path, no entry cite | same `--detail` | `extra: S396 corpus/knowledge/…` / `extra: S397 …` → `verdict=TARGET_MISSED missed=extra` (exit 1) |
| 5 | `fc118bb4` entry cites S396/S397, `used-by` = `—` | same `--detail` | `missing: S396 corpus/knowledge/…` / `missing: S397 …` → `verdict=TARGET_MISSED missed=missing` (exit 1) |
| 6 | `21abfffc` lesson cites S396/S397, `used-by` = `—` | same | `… rows=334 missing=0 extra=0 … verdict=TARGET_MET missed=none` (exit 0) — a lesson is not in `corpus/knowledge/`, so `cite()` never sees it |
| 7 | `2edc1209` entry cites + `mined` + `used-by` = entry path | same | `… rows=334 missing=0 extra=0 … verdict=TARGET_MET missed=none` (exit 0) — the working combination |
| 8 | `b520ac0c` draft rows landed | `c1-r56-autoreload-entry.py --rev b520ac0c…` | `MADO_AUTORELOAD_ENTRY: rev=b520ac0c… rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none` (exit 0) — **C1 unaffected** |
| 9 | `ea680b9f` entry K31 cites S396 | C1 then C3 | C1 `rows=30/30 … new_rows=8/8 verdict=TARGET_MET` (exit 0); C3 `missing: S396 …` → `TARGET_MISSED missed=missing` (exit 1) |
| 10 | `b520ac0c` | `check-index.py` / `check-index-rows.py` / `check-tool-ledger.py` | `MADO_INDEX: indexed=71/71 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`; `MADO_INDEX_ROWS: rows=71 errors=0 warns=3` (3 pre-existing glob warns, unchanged); `LEDGER: population=97 ledger_rows=97 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET` |

Two consequential-but-not-fatal consequences of the rows landing, for the L1's bookkeeping:
`rows` goes **332 → 334** — no frozen number breaks (`claims-frozen-v2.md` and `registration.md` §C3
both write the count as `entries=<E> rows=<R>`), but `SCORECARD.md:2900` and
`receipts/at-final.txt:12` state `rows=332` literally and would need updating.

## Additional observations (not defects in the draft)

- **S396 can never be a `source_cell` under the frozen v2 tables — a structural limit on the
  draft's plan (routing item; no frozen predicate touched).** `source_cell_ok(sid, pin)`
  (`quality/counters/c1-r56-autoreload-entry.py:460-474`) requires
  `c1["pin_suffix"].get(pin)` and `rev_token(pin)` non-None, `cells[8] == OPENED`
  (`'2026-10-28'`), `cells[7] == "mined"`, tier in (A, B), and `ENTRY in cells[10]`.
  `frozen-tables-v2.json` has **no** `pin_suffix`/`rev_rule` entry for
  `man7-inotify_add_watch.2.html`, no `rows` entry for S396, and `new_row_ids` = S383–S390 — so
  `source_cell_ok('S396', …)` is False under the frozen tables for **any** cell combination.
  Meanwhile C1 scores only the **frozen 30 K rows**, so an entry K-row citing S396 is invisible to
  C1 (test 9: `rows=30/30`) but visible to C3's `CITE` (test 9: `missing: S396`,
  `TARGET_MISSED`). Consequence: a C1 K-row for S396 in a later round cannot be scored until the
  tables are re-registered — a round-57 decision, not an attempt-2 edit — and the draft's
  `queued` / `—` / `opened 2026-10-30` cells would need to change when it happens.
- The **read-permission requirement (c)** is at pin line 82 (`EACCES` at 108) and is claimed by
  **no row**: `grep -n "EACCES\|read permission"` over `corpus/`, `tools/` and
  `.ufo/waves/round-56/ctl/` at the tip returns no inotify-related hit. It bears on
  `tools/mado-watchplan.py`'s divergence (5) and on the tool's `ERROR inaccessible` handling (a
  path that exists but is unreadable fails `inotify_add_watch` with EACCES). A natural companion
  row; currently unsourced.
- `tools/mado-watchplan.py`'s docstring asserts "the kernel returns the same watch descriptor for
  the same inode" — the exact rule S396 would ground, asserted today with no registry row behind
  it.
- The C1 counter counts the **frozen** 30 K rows, so an entry row citing S396 is C1-invisible and
  C3-binding (test 9). The two counters disagree about a row that does not exist in the frozen
  tables — worth knowing before the entry's table grows.

## Files written

- `.ufo/waves/round-56/w3/R56W3ScoutNewSrc1/receipts/s396-independent.md` — the deliverable:
  independent read, the diff, and every empirical check with commands and outputs.
- `.ufo/waves/round-56/w3/R56W3ScoutNewSrc1/receipts/raw-evidence.txt` — raw command transcript.
- `.ufo/waves/round-56/w3/R56W3ScoutNewSrc1/receipts/inotify_add_watch.2.html` — my fetched bytes
  (sha256 `98fe7feb…95e2`).
- `.ufo/waves/round-56/w3/R56W3ScoutNewSrc1/receipts/fdinfo_fetch.html` — my independently fetched
  `proc_pid_fdinfo.5.html` (sha256 `f9e12387…d8a1`, byte-identical to the lane pin).

## Could not verify / limits

- I did **not** verify the draft's S397 row beyond the shared defects (D1 date, D2 quotes) and its
  sha256; S397's *content* claims (wd/ino/sdev/mask field semantics, the "one monitored file"
  reading) I checked only for the three quoted lines, not line by line. S397's own anchor locator
  `160,164,171` omits lines 166 (`ino`) and 168 (`sdev`) though its teaches cell names "wd, ino,
  sdev and mask fields" — the same shape as D6; I did not run `scope_covers` for S397.
- I did **not** check whether the man-pages release named by the pages has changed since the
  2026-09-09 rendering (the upstream mirror now also lists 6.20, dated 21-Oct-2026, i.e. newer
  than the pinned pages). The pins are byte-stable across three fetches today, so the sha256 holds;
  but "man-pages 6.19 is current" is not a claim I can make.
- I did **not** run the C2 counter, the harness controls or `check-r56-controls.py` — none of them
  read these registry rows' cells, and the item did not name them.
- I did not verify the L1's intent for the `queued` vs `mined` status against any CORPUS rule
  beyond the observed convention (10 `queued` rows exist, e.g. S036/S038/S039 with `used-by —`;
  S376 is `mined` with `used-by corpus/lessons/round-54.md`). Whether a row whose only citation is
  in a lesson should be `queued`/`—` or `mined`/lesson-path is an L1 call; I verified both shapes
  are C3-green, and I verified the entry-citing shape requires `used-by` = the entry path.

## Tooling

No tool was installed or upgraded by this seat; the operator directive's channel order was not
needed. Tools used, all pre-existing: `curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0
OpenSSL/3.6.5 zlib/1.3.2 brotli/1.2.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.5 libssh2/1.11.1
nghttp2/1.70.0 nghttp3/1.18.0 libngtcp2/1.25.0`, `Python 3.14.8` (`python3 -I`), `git` (read-only on
the lane; a `git clone --shared` fixture under scratch). No pacman transaction; the host-wide pacman
pause was respected.
