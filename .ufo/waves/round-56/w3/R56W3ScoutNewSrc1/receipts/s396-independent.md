# s396-independent — independent read of inotify_add_watch(2), diffed against the L1's S396 row

Seat `R56W3ScoutNewSrc1` (scout, round-56 wave-3 attempt 2). Item: independently open
`https://man7.org/linux/man-pages/man2/inotify_add_watch.2.html`, sha256 the bytes, state the
man-pages release the page names, find the lines stating (a) the unique-watch-descriptor-per-inode
rule, (b) the existing-watch-returned-for-a-different-link rule, (c) the read-permission
requirement; **then** read the L1's draft and diff against its S396 row.

Ordering note: this receipt's section 1 was produced **before** I opened
`.ufo/waves/round-56/attempt2/s396-s397-draft.md`. The draft was read only afterwards; section 3 is
the diff. Raw command transcript: `receipts/raw-evidence.txt`; the two fetched pages are copied
beside it as `receipts/inotify_add_watch.2.html` and `receipts/fdinfo_fetch.html`.

---

## 1. Independent reading of the page (before the draft)

**URL** `https://man7.org/linux/man-pages/man2/inotify_add_watch.2.html`

**sha256 of the bytes I fetched** (2026-10-30, curl 8.23.0):

```
98fe7feb381fa2687e8a3962e6d78a49cb1ad07c543f93449dcb42d6712c3d6d  inotify_add_watch.2.html
```

11345 bytes, 258 lines. Fetched three times with two different user agents: all three digests are
identical, so the page's bytes are stable and the digest is a durable anchor. `cmp` against the
lane's pin `.ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html` → **IDENTICAL** (same 11345
bytes / 258 lines).

**man-pages release the page names:** **man-pages 6.19**, stated twice in the page itself:

- line 155 (COLOPHON): `This page was obtained from the tarball man-pages-6.19.tar.gz`
- line 165 (footline): `<span class="footline">Linux man-pages 6.19            2026-02-08           <i>inotify_add_watch</i>(2)</span>`

The page also carries its own HTML-rendering date `2026-09-09` ("HTML rendering created
2026-09-09"), and the upstream mirror lists the release tarball itself as
`man-pages-6.19.tar.xz  25-Aug-2026 17:43` (6.18 = 22-Apr-2026, 6.20 = 21-Oct-2026).

**The three required statements, by line number in the pin (258 lines):**

| item | lines | text |
|---|---|---|
| (a) unique watch descriptor per inode | **88–92** | `A successful call to <b>inotify_add_watch</b>() returns a unique watch / descriptor for this inotify instance, for the filesystem object / (inode) that corresponds to <i>path</i>.  If the filesystem object was / not previously being watched by this inotify instance, then the / watch descriptor is newly allocated.` |
| (b) existing watch returned for a different link | **93–94** | `already being watched (perhaps via a different link to the same / object), then the descriptor for the existing watch is returned.` |
| (c) read-permission requirement | **82** (and the `EACCES` row at **108**) | line 82: `caller must have read permission for this file.  The <i>fd</i> argument`; line 108: `<b>EACCES </b>Read access to the given file is not permitted.` |

Two precisions the lines carry that a reader should not lose:

- (a)/(b) are scoped **per inotify instance**: the descriptor is unique "for this inotify
  instance", and the object must have been watched **by this inotify instance**. The same inode
  watched by two different inotify instances yields two different descriptors.
- (b) is hedged in the man page's own words — "perhaps via a different link" — i.e. the
  different-link case is one way the already-watched condition can be met, not a separate rule.

---

## 2. What the L1's S396 row says (read after the above)

From `.ufo/waves/round-56/attempt2/s396-s397-draft.md` line 13 (the S396 registry row) and line 15
(the gate quote):

- anchor cell: `inotify_add_watch.2.html:88,93 @ Linux man-pages 6.19 (2026-02-14); pin
  .ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html 11345 B
  sha256:98fe7feb381fa2687e8a3962e6d78a49cb1ad07c543f93449dcb42d6712c3d6d`
- gate quote: line 88 → `A successful call to inotify_add_watch() returns a unique watch`;
  continuation line 93 → `already being watched (perhaps via a different link to the same` /
  `object), then the descriptor for the existing watch is returned.`
- teaches cell: `a successful inotify_add_watch returns a unique watch descriptor for the
  filesystem object (inode), and an object already watched - even via a different link - returns
  its existing descriptor`
- status `queued`, opened `2026-10-30`, recheck `90d`, used-by `—`.

---

## 3. Diff: my independent conclusions vs the S396 row

### AGREES

| point | verdict |
|---|---|
| sha256 `98fe7feb…95e2` | **AGREES** — my own fetch (3×, two UAs) produced exactly this digest; the lane pin is byte-identical. |
| byte size 11345 B | **AGREES** — my fetch is 11345 B / 258 lines. |
| man-pages release "6.19" | **AGREES** — the page names man-pages-6.19.tar.gz and "Linux man-pages 6.19". |
| pin path `.ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html` | **AGREES** — the file exists at the lane tip's working tree with the same bytes; but see D3 (it is not tracked at the tip). |
| locator lines 88 and 93 | **AGREES** — 88 is the unique-descriptor sentence; 93 is the different-link clause. |
| teaches: unique watch descriptor per filesystem object (inode) | **AGREES** — matches lines 88–90. |
| teaches: already-watched object returns its existing descriptor | **AGREES** — matches lines 92–94. |
| teaches: different link reaches the same descriptor | **AGREES** in substance — lines 93–94 say exactly this. |
| row is `queued` with `used-by —` and cited only from the lesson | **AGREES** — verified empirically (§4). |
| rationale: the lane lacked a man-page statement of the one-watch-per-inode rule | **AGREES** — the entry's own text at line 46 attributes that rule to "inotify(7) lines 90-92 and 296-302", and no registry row holds those lines (the only `inotify.7.html:` locator in the whole registry is `:186,262`). See D5. |

### DIFFERS — defects

**D1 — the anchor's page date is wrong (severity: weakens the claim).**
The S396 anchor cell says `@ Linux man-pages 6.19 (2026-02-14)`. **2026-02-14 is the footline date
of `inotify(7)` (S390), not of `inotify_add_watch(2)`.** This page's own footline (line 165) reads
`Linux man-pages 6.19   2026-02-08   inotify_add_watch(2)`. The draft copied S390's date onto the
new row. Input: `grep -n "footline"` on both pins —
`man7-inotify.7.html:811 → 2026-02-14`, `man7-inotify_add_watch.2.html:165 → 2026-02-08`.
The same wrong date is carried in the draft's S397 row, whose page footline reads
`2026-07-18` (`man7-proc_pid_fdinfo.5.html:276`).
*Why it matters:* the lane's date convention (S390's cell, and the man-pages footline the cell
mirrors) is the **page's own revision date**, and each page in the same 6.19 release carries a
different one. A date that names a different page's revision is a false locator for the row's own
pin. Not blocking the C1/C3 predicates (neither counter reads the date cell), but the anchor cell
is the row's provenance statement and it is wrong twice.

**D2 — the gate quote is de-tagged and therefore not a substring of the pin (severity: weakens the
claim; would block a freeze-verifier check).**
The draft's gate quote for line 88 is `A successful call to inotify_add_watch() returns a unique
watch`. The pin's actual line 88 is
`       A successful call to <b>inotify_add_watch</b>() returns a unique watch`.
Substring test against the pinned bytes: the **de-tagged** form occurs **0 times** in the whole
258-line pin; the **raw** form occurs exactly once. Under the lane's own freeze-verifier rule
(`.ufo/waves/round-56/freeze-verify-v2.py` line 17: `q in L[row["line"]-1]` and
`sum(q in x for x in L) == 1`), the de-tagged quote scores **BAD** and the raw form scores **ok**.
The lane's two existing man-page quotes keep the markup: K30 is
`Don't dereference <i>pathname</i> if it is a symbolic link.` (raw-tagged, and `q in L[261]`
is True), K29 is `File opened for writing was closed.` (tag-free line, substring True).
*Same defect in S397:* the draft quotes lines 164 and 171 as `wd     A watch descriptor number (in
decimal).` and `mask   The mask of events being monitored for the target file (in` — both
de-tagged; the raw lines are `<i>wd</i>     A watch descriptor number (in decimal).` and
`<i>mask</i>   The mask of events being monitored for the target file (in`, and **neither
de-tagged string is a substring of its line** (both False). The S397 line-160 quote
`Each of the lines beginning with "inotify" displays information` is tag-free and **is** a
substring (True).
*Why it matters:* a Gate quote that is not present in the pinned bytes cannot be re-verified
against the pin by the command that verifies quotes, so the row's evidence would not be
reproducible. This is the same class as M55-2 (frozen quote unsatisfiable as written) and M56-1
(anchor did not cover the quoted line).

**D3 — the pin is not tracked at the tip (severity: weakens the claim).**
`git cat-file -e 0f3a5436:.ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html` → **not present**
(untracked at the tip; `git status --porcelain` shows `?? .ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html`).
The S390 pin `man7-inotify.7.html` **is** tracked at the tip. Until the new pins are committed
alongside the rows, the anchor cell points at a path that does not exist at the revision the rows
would land on, and the C1 counter's pin lookup (`repo.blob(PIN_DIR + "/" + pin)`) cannot read it.

**D4 — the teaches cell drops the man page's own scope qualifier (severity: weakens the claim).**
The draft teaches: "a successful inotify_add_watch returns a unique watch descriptor **for the
filesystem object (inode)**". The man page says the descriptor is unique "**for this inotify
instance**, for the filesystem object (inode)" (lines 88–89), and the already-watched condition is
"already being watched **by this inotify instance**" (line 91). The dropped qualifier is the
difference between "the kernel keeps one watch per inode" and "the kernel keeps one watch per
inode **per inotify instance**". This matters for the row's stated purpose: the entry's line 46
already asserts the weaker, unqualified form ("the kernel keeps one watch per inode"), and S396 is
the row meant to ground it. Carrying the qualifier in the teaches cell would have let the entry's
sentence be corrected without a new claim.

**D5 — the "why the lane lacked it" rationale names the wrong gap (severity: cosmetic).**
The draft says the entry's duplicate-path prose "was grounded only in the entry's reading of
ConfigWatcher/absolutePath pins and the kernel lab; the man-page statement of the one-watch-per-inode
rule was not held by any row". The entry in fact attributes the rule to **inotify(7)** —
"the kernel keeps one watch per inode, the second add returns the same descriptor and modifies the
watch (inotify(7) lines 90-92 and 296-302…)" (entry line 46). So a man page **was** cited; what
was missing is a *row* holding those lines. And the two cited inotify(7) ranges do not in fact
state the rule: lines 90–92 say only that each watch "has a unique watch descriptor", and 296–302
are the `IN_MASK_CREATE` paragraph ("multiple paths may refer to the same inode, and multiple calls
to inotify_add_watch(2) without this flag may clobber existing watch masks") — the closest thing to
a "one watch per inode" statement, but phrased as a caveat about mask clobbering, not as the rule
the entry asserts. The draft's conclusion (a row is needed) holds; its account of the gap is
inaccurate.

---

## 4. Empirical checks on the draft's C3 reasoning (all run against a scratch clone)

Scratch clone at `/fast/scratch/hyaku/mado-r56/R56W3ScoutNewSrc1/clone`
(`git clone --shared` of the lane, checked out at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`;
`git rev-parse --show-toplevel` = the clone dir). All mutations were on the clone; the lane was
never written.

1. **Baseline at the tip** — `python3 -I quality/counters/c3-r56-used-by.py --repo <clone> --rev
   0f3a5436… --work <scratch>`:
   `MADO_USED_BY: rev=0f3a5436… entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0
   stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none` (exit 0).

2. **Draft rows landed verbatim (queued, used-by `—`)** — commit `b520ac0c…`:
   `entries=71 rows=334 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24
   verdict=TARGET_MET missed=none` (exit 0). **The draft's plan keeps C3 green.**
   Note `rows` rises 332 → 334. The frozen predicate sentence in `claims-frozen-v2.md` writes the
   count as a placeholder (`entries=<E> rows=<R>`), and `registration.md` §C3 likewise uses
   `<E>`/`<R>`, so no frozen number breaks; but `SCORECARD.md:2900` and `receipts/at-final.txt:12`
   state `rows=332` literally and would need updating when the rows land.

3. **Draft's stated worry — a lesson path in `used-by`** — the draft says a lesson path in `used-by`
   "would flip TARGET_MET to TARGET_MISSED at the new tip" because the `extra` leg counts any
   used-by path outside the entry set. **This is not what happens.** With `used-by =
   corpus/lessons/round-56.md` (commit `febfb6a5…`):
   `MADO_USED_BY: … entries=71 rows=334 missing=0 extra=0 … verdict=TARGET_MET missed=none` (exit 0).
   Reason: the counter's `USED_BY` regex is `corpus/knowledge/[A-Za-z0-9_.-]+\.md`, so a
   `corpus/lessons/…` path is never captured into `usedby` at all and cannot produce `extra`.
   The draft's conclusion (use `—`) is right; its stated mechanism is wrong.

4. **The direction that does flip C3** — with `used-by =
   corpus/knowledge/hyprland-config-autoreload-r56.md` while no entry cites the row (commit
   `d8319a27…`): `extra: S396 corpus/knowledge/…`, `extra: S397 corpus/knowledge/…` →
   `verdict=TARGET_MISSED missed=extra` (exit 1). And with the **entry** citing S396/S397 while
   `used-by` is `—` (commit `fc118bb4…`): `missing: S396 …`, `missing: S397 …` →
   `verdict=TARGET_MISSED missed=missing` (exit 1).
   ⇒ The rule that actually binds is the C3 contract's: **an entry that cites a row must have that
   row's `used-by` naming the entry.** The draft's "cited only from the lesson" plan is safe only
   as long as **no knowledge entry cites S396/S397**. The draft's own §"Why the lane lacked it"
   wants the entry's line-46 sentence re-grounded on S396 — i.e. it wants the entry to cite it. If
   the entry cites S396/S397, the rows must simultaneously be `mined` with `used-by =
   corpus/knowledge/hyprland-config-autoreload-r56.md`; I verified that combination:
   `entries=71 rows=334 missing=0 extra=0 … verdict=TARGET_MET missed=none` (exit 0, commit
   `2edc1209…`). **The draft's `queued`/`—` plan and the draft's stated intent are in tension**:
   the intent needs `mined` + the entry path. A row may be `queued` only while no entry cites it.

5. **Lesson-only citation is invisible to C3** — commit `21abfffc…`, lesson cites S396/S397,
   `used-by —`: `entries=71 rows=334 missing=0 extra=0 … verdict=TARGET_MET missed=none` (exit 0).
   Consistent with (3): the lesson is not in `corpus/knowledge/`, so `cite()` never sees it.

6. **C1 is unaffected** — with the draft rows landed (`b520ac0c…`):
   `MADO_AUTORELOAD_ENTRY: rev=b520ac0c… rows=30/30 hosts=3/3 sources=30/30 scope=30/30
   content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none` (exit 0). The C1 counter's
   `new_rows` leg iterates the frozen `new_row_ids` = S383–S390, so S396/S397 are outside it, and
   `rows=30/30` is unaffected (the counter's own `rows` count is the frozen 30 K rows).

7. **A K row citing S396 does not break C1** — commit `ea680b9f…`, entry K31 cites S396 with
   `man7-inotify_add_watch.2.html:88` and the raw-tagged quote: C1 stays
   `rows=30/30 … new_rows=8/8 verdict=TARGET_MET missed=none` (exit 0) — because C1 counts the
   **frozen** 30 K rows, not the entry's table. The same tree under C3 gives
   `missing: S396 corpus/knowledge/hyprland-config-autoreload-r56.md` →
   `verdict=TARGET_MISSED missed=missing` (exit 1). So adding an entry row that cites S396 is
   C1-safe and C3-hostile unless `used-by` is updated in the same commit.

8. **Index and ledger are unaffected** — at `b520ac0c…`: `MADO_INDEX: … indexed=71/71 missing=0
   dangling=0 duplicates=0 coverage=10.0000/10`; `MADO_INDEX_ROWS: … rows=71 errors=0 warns=3`
   (the 3 warns are pre-existing glob warnings, unchanged); `LEDGER: population=97 ledger_rows=97
   uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET`.

9. **`scope_covers` behaviour for the draft's locator** — running the C1 counter's own
   `scope_covers(anchor, "inotify_add_watch.2.html", line, 258)` against the draft's anchor cell:
   line 88 → True, line 93 → True, lines 89/90/91/92/94 → **False**. The draft teaches the
   "unique watch descriptor **for the filesystem object (inode)**" proposition, whose supporting
   text spans lines 88–90 ("descriptor for this inotify instance, for the filesystem object /
   (inode) that corresponds to path"), and the "existing descriptor is returned" proposition, whose
   supporting text is on line 94 ("…then the descriptor for the existing watch is returned."). Both
   of those lines fall **outside** the draft's locator `88,93`. Under the lane's E3/scope rule a
   locator that omits the lines carrying the taught proposition is the M56-1 defect class
   ("a registry anchor did not cover the quoted line"). A locator of `88-94` would cover the whole
   passage.

10. **S396 can never be a `source_cell` under the frozen v2 tables — a structural limit on the
    draft's plan.** `source_cell_ok(sid, pin)` (C1 counter, lines 460–474) requires
    `c1["pin_suffix"].get(pin)` and `rev_token(pin)` to be non-None, `cells[8] == OPENED`
    (`'2026-10-28'`), `cells[7] == "mined"`, tier in (A, B), and `ENTRY in cells[10]`.
    `frozen-tables-v2.json` has **no** `pin_suffix` or `rev_rule` entry for
    `man7-inotify_add_watch.2.html`, no `rows` entry for S396, and `new_row_ids` is
    S383–S390 — so `source_cell_ok('S396', …)` is False under the frozen tables for any cell
    combination. And C1 scores only the **frozen 30 K rows**, so an entry K-row citing S396 is
    invisible to C1 (test 9: `rows=30/30`) while it **is** visible to C3's `CITE` (test 9:
    `missing: S396`, `TARGET_MISSED`). Consequence: if the L1 adds a C1 K-row for S396 in a later
    round, that K row cannot be scored by the C1 counter until the tables are re-registered
    (which is a round-57 decision, not an attempt-2 edit) — and the draft's `queued`/`—`/
    `opened 2026-10-30` cells would need to change when it happens. **This is a routed finding,
    not a change to any frozen predicate.**

11. **Read-permission requirement (c) is unclaimed by any row.** `grep -n "EACCES\|read
    permission"` over `corpus/`, `tools/`, `.ufo/waves/round-56/ctl/` at the tip returns no
    inotify-related hit. `tools/mado-watchplan.py`'s docstring (its declared divergence (5)) says
    "duplicate paths print as separate watches while the kernel returns the same watch descriptor
    for the same inode" — a rule the tool asserts with **no registry row behind it** and that
    S396 would ground. The read-permission requirement itself (line 82 / EACCES at 108) is
    relevant to the tool's `ERROR inaccessible` handling (a path that exists but is unreadable
    fails `inotify_add_watch` with EACCES), and it is likewise ungrounded. Not a defect in the
    draft (S396 does not claim it), but the draft's S396 scope cell says "the kernel's
    one-watch-per-inode rule behind the watcher's duplicate-path and symlink watch rows" — the
    read-permission half of the same man page is a natural companion row and is currently
    unsourced.

---

## 5. Verdict on the S396 row

The **substance** of S396 is sound: my independent fetch reproduces the draft's sha256, byte
count, release name, locator lines and both taught propositions. The **defects are in the
provenance details**: a wrong page date (D1, twice — S396 and S397), a gate quote that is not
present in the pinned bytes because it was de-tagged (D2, four quotes across S396/S397), a pin that
is untracked at the tip (D3), a teaches cell that drops the man page's own per-instance
qualifier (D4), and an inaccurate account of the gap the row fills (D5).

The **C3 reasoning in the draft is wrong in its mechanism and right in its outcome**, and it
carries an internal tension: the row is planned as `queued`/`used-by —` while the row's stated
purpose is to re-ground the entry's line-46 sentence, and an entry that cites S396 makes C3 report
`missing` until `used-by` names that entry. That is a routing item for the L1, not a change to any
frozen predicate: the fix is inside the new rows' own cells (`status`, `used-by`) and the anchor
cell's date/locator.

Nothing here is a change to a frozen predicate, counter or target: every finding is in a cell of a
not-yet-landed registry row, or in prose the L1 is about to write.
