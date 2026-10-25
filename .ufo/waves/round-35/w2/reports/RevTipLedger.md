# RevTipLedger — attack on the ledger tip chain (round 35, wave 2)

Seat: `L1Mado35.RevTipLedger`. Scope: C2's `ledger_tip_ok` axis, the seven frozen blob ids in
`.ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md`, and the round-34 stale-label claim.
Read-only on lane corpus, counters, controls, `SOURCES.md` and jj state. All writes are under
`.ufo/waves/round-35/scratch/RevTipLedger/` and this file. Evidence transcript:
`.ufo/waves/round-35/scratch/RevTipLedger/evidence.txt`.

## 0. Verdict up front

| Axis | Verdict | Confidence |
|---|---|---|
| C2 counter reproduces `TARGET_MET` with `ledger_tip_ok=1` | **CONFIRMED** | HIGH |
| All 7 blob ids re-verify at `dff3941` by content, not just by name | **CONFIRMED 7/7** | HIGH |
| Ledger table rows == `c2/frozen.json` blob list | **CONFIRMED 7/7** | HIGH |
| `dff3941` is the round-34 lane tip | **FALSIFIED** — the tip is `6d754bd` | HIGH |
| `dff3941` is `master` | **FALSIFIED** — `master` = `origin/master` = `19e4ab3` | HIGH |
| Round-34 artifact's label was "stale by one commit" | **FALSIFIED** — stale by **two** commits | HIGH |
| `ledger_tip_ok` actually tests tip-ness | **FALSIFIED** — three forgeries pass, incl. the stale label itself | HIGH |
| §2 "no later commit on master touched it" | **CONFIRMED** on master's first-parent chain | HIGH |
| §2 "written once" / "no write-then-revert is possible" | **OVERSTATED** — repo-wide, each path has 3 touching commits | HIGH |

The blob-identity conclusion survives and is stronger than stated: the seven ids are identical at
`dff3941`, at `6d754bd`, at `master`, and in the working tree. What does not survive is the
**naming**: the re-issue that exists to repair a stale tip label carries its own stale tip label,
and the counter that certifies it cannot tell the defect from the fix.

## 1. Counter reproduction

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && \
  python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json
PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
EXIT=0
```

`ledger_tip_ok=1` as required. Exit code `0`, verdict `TARGET_MET`. C2's scored target is met.

## 2. Independent blob re-verification — 7/7 OK

The assignment asked for `git cat-file blob <id>` rather than trusting the id's spelling. I did
three independent things per blob: `cat-file -t` (must be `blob`), `cat-file -s` (object exists
locally), and `cat-file blob <id> | git hash-object --stdin` (the bytes re-hash to the id claimed).
Passing the third check means the id is the *content address* of the bytes, so no substitution is
possible under any name.

| Path | blob id | type | rehash | verdict |
|---|---|---|---|---|
| `.ufo/waves/round-33/c1/count.py` | `4ab3db435dd2e396402d1d83039e35082f1138fe` | blob | `4ab3db43…` | **OK** |
| `.ufo/waves/round-33/c1/frozen.json` | `60d1094baa2992294533bae37e0990ae23077609` | blob | `60d1094b…` | **OK** |
| `.ufo/waves/round-33/c2/count.py` | `df563528e725951b447ef31b324ec4b7d264e91b` | blob | `df563528…` | **OK** |
| `.ufo/waves/round-34/c1/count.py` | `49089c186fb75f1bd2cc4c45c0161282ea6e8a46` | blob | `49089c18…` | **OK** |
| `.ufo/waves/round-34/c1/frozen.json` | `0bfe0d866c4e9a2d17da297a11dae389150b488b` | blob | `0bfe0d86…` | **OK** |
| `.ufo/waves/round-34/c2/count.py` | `3a499a7eaa6cf5e861a5849992c37f1a7bede962` | blob | `3a499a7e…` | **OK** |
| `.ufo/waves/round-34/c2/frozen.json` | `ef3392b45f638513ff98dda95808f3f3938705e0` | blob | `ef3392b4…` | **OK** |

Sizes: 3969 / 1564 / 3630 / 6365 / 1235 / 5196 / 679 bytes. First lines are `#!/usr/bin/env python3`
for the four counters and `{` for the three JSON freeze files — the objects are the file types the
paths claim, so no path/type swap.

`git rev-parse dff3941:<path>` returns these same seven ids, so the ledger table is a faithful
transcription of the tree at the named commit. Cross-check of the ledger's markdown table against
`c2/frozen.json`'s `frozen_blobs` list, parsed programmatically:

```
ledger_table_rows= 7 ; frozen_json_entries= 7
table==json: True ; table_path_set==json_path_set: True
EXIT=0
```

No divergence row-by-row. This matters because the counter never parses that table (§5).

## 3. The stale-label claim — FALSIFIED in both directions

### 3.1 `fa7ba113` is not the tip — but neither is `dff3941`

```
$ git cat-file -t fa7ba113
commit                                                    EXIT=0
$ git log --oneline dff3941 -1
dff3941 round-34: the lesson, the log entry, and the round-34 claim rows
```

`fa7ba113` is a commit, as the ledger says. But the first-parent history of `master` puts a
round-34-labelled commit **after** `dff3941`:

```
$ git log --oneline master -6
19e4ab3 round-35: freeze C1 and C2 predicates, the clause ledger, the control receipts and the re-issued blob ledger
6d754bd round-34 verifier spot-check (integrator, hyaku): non-author admit/reject
dff3941 round-34: the lesson, the log entry, and the round-34 claim rows
57622b8 round-34: wave-1 evidence (64 seats, 0 dead), the named r33 scratch dispositions, and the axis-gate selftest transcript
fa7ba11 round-34: admit the waybar event-socket entry after the frozen counter
3420e82 round-34: freeze C1 and C2 predicates and pre-data control receipts

$ git log --oneline master --grep='^round-34'
6d754bd round-34 verifier spot-check (integrator, hyaku): non-author admit/reject
dff3941 round-34: the lesson, the log entry, and the round-34 claim rows
57622b8 round-34: wave-1 evidence ...
fa7ba11 round-34: admit the waybar event-socket entry after the frozen counter
3420e82 round-34: freeze C1 and C2 predicates and pre-data control receipts
```

`6d754bd` adds `corpus/lessons/round-34-verifier-spotcheck.md` (+341 lines), is the parent of the
round-35 freeze commit, and is the last `round-34`-labelled commit on `master`. **The round-34 lane
tip is `6d754bd`, not `dff3941`.** This falsifies the premise handed to this seat ("`dff3941` is
[the round-34 tip]") as well as the re-issue's §0 line 5 and its refs list at line 13, both of which
omit `6d754bd` entirely.

### 3.2 `dff3941` is not `master`

```
$ git rev-parse master ; git rev-parse origin/master
19e4ab3171c1540c40d6b12097745af98053b07d
19e4ab3171c1540c40d6b12097745af98053b07d
$ git log -1 --format='%h %p' 19e4ab3
19e4ab3 6d754bd
```

The ledger's "`dff3941` (`master`, pushed)" is half-wrong. `dff3941` *is* pushed (it is an ancestor
of `origin/master`, `merge-base --is-ancestor` → yes), but it stopped being `master` one commit
after `6d754bd` landed. `dff3941` was `master` only in the 17m37s window
`2026-10-24 22:46:49 → 23:04:26`.

### 3.3 "stale by one commit" is wrong — it is two

```
$ git rev-list --count fa7ba113..dff3941
2
$ git log --oneline --first-parent fa7ba113..dff3941
dff3941 round-34: the lesson, the log entry, and the round-34 claim rows
57622b8 round-34: wave-1 evidence (64 seats, 0 dead), ...
```

Two commits (`57622b8`, `dff3941`) separate the round-34 artifact's label from the commit the
re-issue substitutes for it. The re-issue's line 8, "The artifact's own **label** was stale by one
commit", undercounts by one.

### 3.4 The round-34 artifact was not wrong when it wrote it

The round-34 artifact was committed in `57622b8` at `22:46:39` (its file mtime is 22:34, i.e. it was
written before it was committed):

```
$ git log --format='%h %ci %s' master -- .ufo/waves/round-34/w1/reports/RevFrozenBlobs.md
57622b8 2026-10-24 22:46:39 -0300 round-34: wave-1 evidence (64 seats, 0 dead), ...
```

`fa7ba113` was `master` from `21:58:15` until `57622b8` landed at `22:46:39` — 0:48:24, which
contains both the write time (22:34) and the commit instant (22:46:39). So the round-34 artifact
correctly recorded the tip as it stood at measurement time; it aged by two commits afterwards.
Charging it with an error (rather than with obsolescence) is an inference the re-issue makes, and
the numbers do not support the "one commit" part of it.

### 3.5 The re-issue was stale when it was committed

The re-issue lands in `19e4ab3` at `23:24:06`, i.e. **0:19:40 after** `dff3941` ceased being
`master` (23:04:26). At its own commit instant, `dff3941` was two commits back and `master` was
`6d754bd`. The re-issue therefore reproduces the exact defect class it routes — a label naming a
commit that is not the tip — and does so with a 19-minute-known error, not a hindsight error.

| Commit | Time (2026-10-24 −0300) | Status |
|---|---|---|
| `3420e82` | 21:55:08 | round-34 freeze `F` |
| `fa7ba113` | 21:58:15 | round-34 artifact's label — was `master` for 0:48:24 |
| `57622b8` | 22:46:39 | round-34 wave-1 evidence |
| `dff3941` | 22:46:49 | re-issue's label — was `master` for 0:17:37 |
| `6d754bd` | 23:04:26 | **round-34 verifier spot-check — the real round-34 tip** |
| `19e4ab3` | 23:24:06 | round-35 freeze + re-issued ledger = `master` = `origin/master` |

## 4. The blob conclusion is stronger than the ledger claims

Because every commit in `dff3941..master` leaves the seven paths untouched, the ids hold at more
places than were checked:

```
$ git diff --name-only fa7ba113 dff3941  -- <7 paths>   → (empty)
$ git diff --name-only dff3941 master    -- <7 paths>   → (empty)   EXIT=0
$ git diff --name-only dff3941 6d754bd   -- <7 paths>   → (empty)   EXIT=0
$ git diff --stat dff3941 -- .ufo/waves/round-33/c1 ...  → (empty)   EXIT=0
$ git rev-parse master:<path>            → same 7 ids
$ git hash-object <worktree path>        → same 7 ids
```

So "byte-identical" is true at `fa7ba113`, `dff3941`, `6d754bd`, `master`, and the working tree.
The conclusion is unassailable; only the coordinate it is pinned to is wrong.

## 5. `ledger_tip_ok` does not test what its prose says — three forgeries

The predicate prose (`c2/frozen.json`, line 3) says: `ledger_tip_ok` is 1 when the ledger "names the
round-34 tip `dff3941…` and every frozen blob **it lists** re-verifies by git blob id at that
revision." The implementation is weaker in three independent ways:

```python
ledger_doc = repo / spec["blob_ledger"]          # 103
if ledger_doc.is_file():
    text = ledger_doc.read_text()
    if spec["r34_tip"] in text:                  # 106  bare substring, anywhere, in any polarity
        ...
        for blob in spec["frozen_blobs"]:        # 109  frozen.json's list — the ledger table is never parsed
            raw = subprocess.run(["git","-C",str(repo),"rev-parse", f"{spec['r34_tip']}:{blob['path']}"])
            if raw != blob["blob_id"]: ok = False
```

- **G1 — no tip test.** There is no `master` comparison, no ancestry check, no "is a round-34
  commit" check. Any commit carrying those blobs passes.
- **G2 — the ledger table is never read.** The loop iterates `spec["frozen_blobs"]`, not the
  document. `blob_ledger` is opened only for the line-106 substring.
- **G3 — substring ignores polarity.** A sentence *denying* the tip satisfies line 106.

I ran three scratched control specs (all writes under my scratch dir; the lane counters and the
real `frozen.json` untouched). Each scored a full pass:

| Control | Manipulation | Result |
|---|---|---|
| **A** | `r34_tip` = `19e4ab3` (`master`, a non-tip for round 34); doc reads "`19e4ab3…` **is NOT** the round-34 tip" | `ledger_tip_ok=1 verdict=TARGET_MET EXIT=0` |
| **B** | `r34_tip` correct; ledger table replaced with a single `deadbeef…` vanity row | `ledger_tip_ok=1 verdict=TARGET_MET EXIT=0` |
| **C** | `r34_tip` = `fa7ba113` — **the very stale label the re-issue was written to correct**; real ledger doc | `ledger_tip_ok=1 verdict=TARGET_MET EXIT=0` |

Control C is the decisive one. `fa7ba113` still carries all seven blobs (nothing between it and
`dff3941` touches them — §4), and the real ledger *mentions* `fa7ba113…` at line 4, so both the
substring test and the blob loop pass. **The counter cannot distinguish the defect from the fix it
was built to certify.** It would have printed `TARGET_MET` for the round-34 artifact's label too.

Consequence for C2: `ledger_tip_ok=1` is a true statement about *blob presence at a named commit*
and a silent statement about *tip-ness*. The gap is not academic here — the artifact it certifies
names a commit that is not the round-34 tip and not `master`, and the gauge still reads 1. Fixing
this needs, at minimum: resolve `spec["r34_tip"]` against `master` and the last `round-34`-labelled
commit, and parse the ledger's table rows instead of trusting a substring.

## 6. §2 per-path history — holds on master, overstated across refs

First-parent history on `master` matches the ledger's attribution exactly:

```
.ufo/waves/round-33/c1/count.py     9a46ccf
.ufo/waves/round-33/c1/frozen.json  9a46ccf
.ufo/waves/round-33/c2/count.py     9a46ccf
.ufo/waves/round-34/c1/count.py     3420e82
.ufo/waves/round-34/c1/frozen.json  3420e82
.ufo/waves/round-34/c2/count.py     3420e82
.ufo/waves/round-34/c2/frozen.json  3420e82
$ git merge-base --is-ancestor 9a46ccf master → yes ; 3420e82 → yes
```

One touching commit per path on `master`, at the freeze commit, and no later one — confirmed by the
empty `dff3941..master` diff in §4. So "no later commit on `master` touched it" is **CONFIRMED**.

But `git log --all` shows **three** commits per path, because two same-second sibling commits are
kept by jj's operation log:

```
$ git log --all --format='%h %ci %s' -- .ufo/waves/round-34/c1/count.py
735f7e5 2026-10-24 21:55:08 -0300
3420e82 2026-10-24 21:55:08 -0300  round-34: freeze C1 and C2 predicates and pre-data control receipts
c42a21f 2026-10-24 21:55:07 -0300
$ git for-each-ref --contains 735f7e5 --format='%(refname)'
refs/jj/keep/735f7e5846547d552fd3c6dd8761e786b9420f2c
```

Same shape for round 33 (`520a667`, `dbc1f8a` on `refs/jj/keep/`). None are on `master`
(`--is-ancestor` → NOT_ON_MASTER), so they do not disturb the frozen claim; but the ledger's two
inferences — "Each frozen path was **written once**" and "**so no write-then-revert is possible**" —
are true only of `master`'s first-parent chain. Repo-wide the paths were written three times, and a
write-then-revert confined to a kept jj commit is representable in this object store. The correct
statement is: *no write-then-revert is reachable from `master`, and the final bytes equal the frozen
blob id at every tip checked.* That is what the evidence supports; the ledger's wording is broader.

Secondary, same family: `frozen_blobs` covers only round-33/34 counters. The round-35 counter pair
(`round-35/c1/count.py`, `round-35/c2/count.py`) — the ones whose freeze this ledger is supposed to
witness — are not in the list, so the round-35 freeze is not covered by its own re-issue. The
predicate as literally written ("every frozen blob **it lists**") is satisfied, so this is a
scoping gap, not a falsification.

## 7. Divergences, ranked

1. **The re-issue names `dff3941` as the round-34 lane tip and as `master`. Both are false**
   (`6d754bd` is the round-34 tip; `19e4ab3` is `master`). Same defect class it was written to
   route, committed 0:19:40 after the fact was knowable. Lines 5–6, 13, 19, 38, 53–55.
2. **"stale by one commit" is wrong by one** — `rev-list --count fa7ba113..dff3941` = 2 (line 8).
3. **`ledger_tip_ok` cannot detect either defect** — controls A/B/C all score `TARGET_MET exit 0`,
   including control C where `r34_tip` is the original stale label.
4. **The ledger's table is never machine-checked.** It happens to be correct (7/7 == `frozen.json`,
   verified independently), but `ledger_tip_ok` would stay 1 with a `deadbeef` row (control B).
5. **§2 "written once" / "no write-then-revert is possible" overstates repo-wide** — two
   `refs/jj/keep/` sibling commits per path touch the same files at the same second.
6. **`6d754bd` is absent from the refs list** and from every count in the document, so the artifact
   under-reports round 34's closure by one commit.
7. **The counter's inputs are not all committed bytes.** Its docstring says "One command over
   committed bytes", but `clause_ledger` and `blob_ledger` are opened with `Path.read_text()` from
   the working tree; only the blob loop goes through `git`. Control B proves it: the forged ledger
   document is an *untracked* scratch file and was read anyway. With `corpus/SOURCES.md` and three
   `corpus/knowledge/` entries currently dirty in the worktree from other seats, the counter's two
   document inputs are not pinned to `19e4ab3`. They happened to be clean when I ran it
   (`git status --porcelain -- .ufo/waves/round-35/c1 .ufo/waves/round-35/ledger` → empty), and the
   run reproduced identically before and after my scratch work.

None of 1–7 changes any blob byte: the frozen counter set is intact and identical everywhere
checked. C2's *scored* target is met (`TARGET_MET`, `ledger_tip_ok=1`, exit 0, reproduced). C2's
*prose* goal — "the ledger names the round-34 tip ... and every frozen blob it lists re-verifies" —
fails on its first conjunct.

## 8. Notes

- No installs, no upgrades, no package transactions. `python3`, `git` only. Nothing written outside
  `.ufo/waves/round-35/scratch/RevTipLedger/` and this report.
- Scratch controls, reproducible: `scratch/RevTipLedger/frozen-forged-{A,B,C}.json` with
  `forged-{A,B}-*.md`; transcript in `scratch/RevTipLedger/evidence.txt`. Each was run as
  `python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen <spec>`.
- Inference, marked as such: that the re-issue's author intended "round-34 lane tip" in the
  present-tense sense. If "lane tip" meant "the tip at the instant this row was measured", then
  `dff3941` was defensible for 17m37s — but the document's own refs list and its "(`master`,
  pushed)" gloss, plus its omission of `6d754bd`, make the present-tense reading the only one the
  text supports.
- Left for the main agent: nothing in this seat's scope to run further; the counter, the bytes, the
  topology and the three controls are all exercised above with quoted exit codes.
