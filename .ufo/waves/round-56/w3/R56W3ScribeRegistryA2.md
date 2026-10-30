# R56W3ScribeRegistryA2 — round 56 w3, attempt 2 (2026-10-30)

Seat: scribe. Item: draft the two full 11-cell registry rows S396 (inotify_add_watch(2)) and S397
(proc_pid_fdinfo(5)) from the pins under `.ufo/waves/round-56/fetch/`, verify the draft registry
passes `scripts/sources-census.sh validate --file` in scratch. Lane bounds: leaf member, no
subagent dispatch. No tracked lane file was edited; no git/jj mutation touched the lane or the
fleet repo. Scratch: `/fast/scratch/hyaku/mado-r56/R56W3ScribeRegistryA2/` (removed before
yielding; receipts copied into the deliverable dir first).

Deliverable: `.ufo/waves/round-56/w3/R56W3ScribeRegistryA2/receipts/rows-draft.md` (the two rows,
pin provenance, census output, and the measured integration constraints).

## What I attacked and what I did

The item was a draft-and-verify seat, so the falsification work went into three places: (1) are
the pins themselves sound, (2) does the drafted row text survive the census and every frozen
counter, and (3) does the landed state survive the integration the L1 is planning.

1. **Pin existence and provenance.** The two pins existed under
   `.ufo/waves/round-56/fetch/` (mtime 2026-10-30 02:02, untracked working-tree files), so I used
   them — I did not need to fetch into the lane. I did fetch both URLs into scratch independently
   and `cmp` confirmed the bytes are identical, so the sha256s I pin are upstream bytes, not just
   local assertions. Recorded tool usage: none installed; used the preinstalled
   `bash`/`python3 -I`/`git`/`curl`/`gawk` stack only.

2. **Anchor date** (finding D-1, conflicts with the seat template — see Findings). The seat
   template literally says `@ Linux man-pages 6.19 (2026-02-14)`; the L1's own draft
   (`.ufo/waves/round-56/attempt2/s396-s397-draft.md`) uses the same date on both rows.
   `2026-02-14` occurs **0** times in either new pin (`grep -c "2026-02-14"` → 0 for both). It is
   the date on the *old* `man7-inotify.7.html` pin quoted by S390. Each new page carries its own
   footline date, and the row anchors carry those instead.

3. **Locator coverage** (finding D-2). The L1 draft's locators (`88,93` and `160,164,171`) miss
   lines the teaches cells assert. My anchors use the covering ranges/line lists recorded below,
   and I verified with the C1 counter's own `scope_covers()` that every asserted line is inside a
   locator of the anchor's basename, and every locator is bounded above by the pin's line count
   (258 and 366 lines).

4. **Full draft verification.** I built the draft registry as a copy of `corpus/SOURCES.md` at
   `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` plus the two rows inserted after `S395`, *inside*
   the `## Registry` section, and re-ran the census plus every frozen counter on a scratch
   commit of a scratch clone. All green (commands and outputs under Receipts).

5. **Integration landmine** (finding D-3). The rows as drafted (`queued`, `used-by —`) are only
   C3-safe while the *knowledge entry* does not cite them. I measured every half-landed state with
   a C3 counter run on a scratch clone. Headline: if the L1 adds `S396`/`S397` to the entry's
   `source:` line while leaving `used-by —`, C3 flips to `missing=2, TARGET_MISSED` (rc 1).

## The two rows (verbatim, as delivered in receipts/rows-draft.md)

```
| S396 | Linux man-pages 6.19 inotify_add_watch(2) man page - https://man7.org/linux/man-pages/man2/inotify_add_watch.2.html | docs | B | the kernel one-watch-per-inode rule behind the watcher's duplicate-path and symlink watch rows | inotify_add_watch.2.html:88-94 @ Linux man-pages 6.19 (2026-02-08); pin .ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html 11345 B sha256:98fe7feb381fa2687e8a3962e6d78a49cb1ad07c543f93449dcb42d6712c3d6d | a successful inotify_add_watch returns a unique watch descriptor per filesystem object within one inotify instance, and an object already watched, even through a different link, returns its existing descriptor | queued | 2026-10-30 | 90d | — |
| S397 | Linux man-pages 6.19 proc_pid_fdinfo(5) man page - https://man7.org/linux/man-pages/man5/proc_pid_fdinfo.5.html | docs | B | the /proc fdinfo fields the watch-table comparison reads | proc_pid_fdinfo.5.html:104-105,157-158,160-161,164,166,168-169,171-172 @ Linux man-pages 6.19 (2026-07-18); pin .ufo/waves/round-56/fetch/man7-proc_pid_fdinfo.5.html 14694 B sha256:f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1 | each inotify line of an fdinfo file names one watched file or directory by watch descriptor, inode, device and event mask, and the inotify inode there is hexadecimal while the fdinfo header's own ino field is decimal, so a running compositor's watch table can be read without touching it | queued | 2026-10-30 | 90d | — |
```

Cells per the seat spec: id; source (title - URL, hyphen separator, S390 precedent); kind docs;
tier B; scope (the spec's one-line wording); anchor `NAME:locators @ Linux man-pages 6.19 (DATE);
pin <path> <bytes> B sha256:<hex>`; teaches (one grounded benefit, no pipes); status queued;
opened 2026-10-30; recheck 90d; used-by — (em dash U+2014, the registry's queued-row convention,
bytes `e2 80 94`). Both rows parse as exactly 11 cells (`awk -F'|'` NF=13) and contain no `|`
inside any cell.

## Pins (state which I did)

The pins existed (untracked working-tree files, mtime 2026-10-30 02:02); I did **not** re-fetch
them into the lane. I fetched both URLs into scratch and `cmp` proved byte-identity with the lane
copies:

```
$ curl -sS -o up-inotify_add_watch.2.html https://man7.org/linux/man-pages/man2/inotify_add_watch.2.html
$ curl -sS -o up-proc_pid_fdinfo.5.html  https://man7.org/linux/man-pages/man5/proc_pid_fdinfo.5.html
$ cmp up-inotify_add_watch.2.html <lane>/.ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html   # identical
$ cmp up-proc_pid_fdinfo.5.html  <lane>/.ufo/waves/round-56/fetch/man7-proc_pid_fdinfo.5.html    # identical
98fe7feb381fa2687e8a3962e6d78a49cb1ad07c543f93449dcb42d6712c3d6d   (11345 B)
f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1   (14694 B)
```

Both pins are **untracked** at the tip (`git status --porcelain` shows `??` for both), so the
anchors' `pin … sha256:…` is not yet verifiable from any commit — the L1 must add the two files
when landing the rows.

Anchor lines (both verified `in range`, via `sed -n` on the pin bytes):
- S396 `88-94` (pin 258 lines): the paragraph carrying the whole one-watch-per-inode rule.
- S397 `104-105,157-158,160-161,164,166,168-169,171-172` (pin 366 lines): the header `ino` field
  (decimal), the two example `inotify wd:…` lines, the "one file or directory per line" sentence,
  and the four field definitions `wd`/`ino`/`sdev`/`mask` the wave-2 comparison parses.

## Census verification (the seat's required check)

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file /fast/scratch/hyaku/mado-r56/R56W3ScribeRegistryA2/full/corpus/SOURCES.md.draft \
    --today 2026-10-30
rc=0   (exit 0)
$ diff <(sed 's/SOURCES.md.draft/SOURCES.md/' final-validate.txt) baseline-full-validate.txt
(no differences)
```

The draft is the tip registry plus exactly two rows; the census finding set is byte-identical to
the unedited baseline's (37 pre-existing `W04`/`W01` warnings + `file ok`), so the rows introduce
**no** new census finding and no `E` code. Counts move exactly two steps: `rows` 332 → 334,
`tier.B` 5 → 7, `status.queued` 10 → 12.

Placement check: the rows sit at lines 346-347, before `## Paths` (line 349), i.e. inside the
`## Registry` section — the `E12` trap the L1's own LOG-draft records was probed and is avoided.

## Frozen counters re-run on the draft (scratch clone, scratch commit `0cb102f010e63c77d291686c48be445404bb9a24`)

```
$ git -C <clone> rev-parse --show-toplevel          # = the clone path (asserted)
$ python3 -I quality/counters/c3-r56-used-by.py --repo <clone> --rev 0cb102f0… --work <scratch>
MADO_USED_BY: rev=0cb102f010e63c77d291686c48be445404bb9a24 entries=71 rows=334 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none     rc=0
$ python3 -I quality/counters/c1-r56-autoreload-entry.py --repo <clone> --rev 0cb102f0… --work <scratch>
MADO_AUTORELOAD_ENTRY: rev=0cb102f010e63c77d291686c48be445404bb9a24 rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none     rc=0
$ python3 -I quality/check-r56-controls.py --claim c3 --repo <clone> --rev 0cb102f0… --work <scratch>
MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK     rc=0
$ python3 -I quality/check-index.py --repo <clone> --rev 0cb102f0…
MADO_INDEX: rev=0cb102f0… indexed=71/71 missing=0 dangling=0 duplicates=0 coverage=10.0000/10     rc=0
$ python3 -I quality/check-index-rows.py --repo <clone> --rev 0cb102f0…
MADO_INDEX_ROWS: rev=0cb102f0… rows=71 errors=0 warns=3     rc=0   (3 warns = pre-existing cited-glob-nomatch)
$ python3 -I quality/check-tool-ledger.py --repo <clone> --rev 0cb102f0…
LEDGER: population=97 ledger_rows=97 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET     rc=0
$ python3 -I quality/check-evidence-pointers.py …     rc=0
```

So landing these two rows moves `MADO_USED_BY` from `rows=332` to `rows=334` and leaves every
frozen leg, control and downstream check green. Note `receipts/at-final.txt` still records
`rows=332`; that number is a receipt, not a predicate leg (the frozen sentence writes
`entries=<E> rows=<R>` symbolically), but the attempt-2 receipts must be re-taken at the new tip.

## The constraint table (measured, one mutation each, all on scratch clones)

| # | scratch state on top of the draft | C3 counter result |
|---|---|---|
| D0 | draft as drafted (no entry citation, `used-by —`) | `missing=0 extra=0 … TARGET_MET` rc=0 |
| D2 | entry `source:` line cites S396+S397, `used-by` stays `—` | `missing=2 … TARGET_MISSED missed=missing` rc=1 |
| D3 | entry `source:` line cites S396+S397 **and** `used-by` names the entry | `missing=0 extra=0 … TARGET_MET` rc=0 |
| D6 | `used-by` names the entry, no entry cites the rows | `extra=2 … TARGET_MISSED missed=extra` rc=1 |
| D7 | only the **lesson** (`corpus/lessons/round-56.md`) cites S396+S397 | `missing=0 extra=0 … TARGET_MET` rc=0 |
| D8 | `used-by` names a **lesson** path | `missing=0 extra=0 … TARGET_MET` rc=0 (and census unchanged) |

Why D7/D8 are green: `USED_BY` matches only `corpus/knowledge/[A-Za-z0-9_.-]+\.md`, so a lesson
path never enters `USEDBY`, and `ENTRIES` is `corpus/knowledge/*.md` only, so a lesson mention is
never a `CITE`. This empirically refutes the L1 draft's stated rationale — its own preamble claims
"a lesson path in `used-by` would flip TARGET_MET to TARGET_MISSED at the new tip", but D8 shows a
lesson path in `used-by` keeps every leg at zero. The real hazards are the two knowledge-entry
directions (D2 and D6).

D2 is the landmine: `CITE(entry)` reads every non-fence line of the entry *including the
`source:` line*, so the natural-looking move of listing the two new sources on the entry's
`source:` line while leaving `used-by —` flips C3 to `TARGET_MISSED`. The L1's own plan (citation
lives only in the attempt-2 lesson Gate text) is safe, confirmed by D7.

## Findings

**D-1. Anchor date in the seat template and the L1 draft is not in either pin — severity: weakens
the claim.** The seat template literally specifies `@ Linux man-pages 6.19 (2026-02-14)` and the
L1's draft (`.ufo/waves/round-56/attempt2/s396-s397-draft.md`) uses `(2026-02-14)` on both rows.
`grep -c "2026-02-14"` returns **0** for both new pins. `2026-02-14` is the date printed in the
footline of the *old* `man7-inotify.7.html` pin that S390 quotes
(`man7-inotify.7.html:811: … Linux man-pages 6.19  2026-02-14  inotify(7)`). The new pins print
their own dates: `man7-inotify_add_watch.2.html:165` → `2026-02-08`;
`man7-proc_pid_fdinfo.5.html:276` → `2026-07-18`; the source tarball agrees (`.TH
inotify_add_watch 2 2026-02-08`, `.TH proc_pid_fdinfo 5 2026-07-18`). The S390 precedent is
"the date printed in that page's own footline", so I used `(2026-02-08)` / `(2026-07-18)` per page.
Conflict reported verbatim: if the judge prefers the template's literal `(2026-02-14)` for shape
parity with S390, the change is the parenthetical date alone — but that date does not occur in
either pinned file, and the anchors' whole job is to be checkable against the pin bytes. (Not
candidate-blocking: no frozen leg reads the anchor date of a queued, uncited row.)

**D-2. The L1 draft's locator lists under-cover its own teaches cells — severity: weakens.**
L1 S396 anchors `88,93`: line 94 ("then the descriptor for the existing watch is returned") and
line 90 (the "(inode)" wording) are outside the list, yet the teaches cell asserts both halves of
the rule. L1 S397 anchors `160,164,171`: lines 104-105 (the header `ino` field the L1 does not
mention), 166 (`ino`, hexadecimal) and 168-169 (`sdev`) are outside the list, yet the L1's teaches
cell names "wd, ino, sdev and mask fields". My ranges cover every asserted line; verified with the
counter's own `scope_covers()` (all asserted lines `True`, all locators ≤ the pin line counts).

**D-3. The landed-state landmine (both directions) — severity: blocks C3 if half-landed.** D2 and
D6 above. Operationally: the two rows may be cited only by a lesson, or (if cited by the knowledge
entry) their `used-by` must name the entry in the same landing. Neither half state is green.
Verified the L1's planned state (lesson-only citation) is green (D7).

**D-4. `rows=332` receipts go stale — severity: cosmetic to weakens.** Landing the rows moves
`MADO_USED_BY rows=332` → `rows=334` (`receipts/at-final.txt:12`, `receipts/attempt2-l1.txt`, and
any prose quoting 332). The frozen sentence writes `rows=<R>` symbolically, so the predicate is
not violated, but the receipt must be re-taken at the new tip.

**D-5. The two pins are untracked — severity: weakens until committed.** The anchors reference
`.ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html` and
`…/man7-proc_pid_fdinfo.5.html`, which exist only as untracked working-tree files at
`0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (`git status --porcelain` → `??` for both; `git
ls-tree` shows 13 tracked fetch files). No commit contains them, so today the pinned sha256s are
verifiable only against the working tree. The L1 must commit both files with the rows.

**D-6. C1 compatibility limit for round 57 — severity: informational/routed.** A future K row
citing S396/S397 fails under the current frozen tables, demonstrated by a scratch mutation (K03
cites S396, S396 present as a queued row):
`MADO_AUTORELOAD_ENTRY: … sources=29/30 scope=29/30 … TARGET_MISSED missed=prov,source_cell:K03,scope:K03`.
The counter requires the cited row to be `mined`, tier A/B, `opened 2026-10-28`, with a URL
ending in `c1.pin_suffix[pin]` and containing the rev token — and `c1.pin_suffix`/`c1.rev_rule`
have no entry for either new man page (the frozen tables list only `man7-inotify.7.html`). Fixing
that needs a new frozen-tables version; it is a round-57 routing, not something this seat may
change.

## Could not verify / limits

- The census and the counters run from scratch copies; the lane's tracked files were never edited
  and no git mutation touched the lane or the fleet repo (scratch clones only; toplevel asserted
  equal to the clone directory before every commit; commits used `-c user.name=ctl
  -c user.email=ctl@ctl`).
- I did not run the C1 controls harness (`check-r56-controls.py --claim c1`) against the draft —
  the C1 counter itself passes on the draft commit, and nothing in the draft touches the C1 entry,
  pins, or K rows; the C3 controls harness (the one whose registry the draft modifies) was run and
  is 9/9.
- Whether the L1 lands the rows, the pins, or the lesson citation is outside this seat; D-3/D-5
  record exactly what must hold when it does.
- Tooling installs: none (preinstalled stack only), so there is nothing to record under the
  tooling-authorization rule.

## Receipts

- `.ufo/waves/round-56/w3/R56W3ScribeRegistryA2/receipts/rows-draft.md` — the two rows, pin
  provenance with exact commands, census output, and the constraint table.
- `…/receipts/census-validate-draft.txt` / `census-validate-baseline.txt` — the validate runs the
  diff compares (byte-identical finding sets).
- `…/receipts/counter-mutations.txt` — every C1/C3 counter run quoted in the constraint table,
  with the scratch commit id of each mutation.
- `…/receipts/SOURCES.draft.md` — the exact draft registry (tip copy + S396 + S397).
- Scratch (`/fast/scratch/hyaku/mado-r56/R56W3ScribeRegistryA2/`) is removed before yield;
  everything quoted above is reproduced in the receipt files.

Report: .ufo/waves/round-56/w3/R56W3ScribeRegistryA2.md
