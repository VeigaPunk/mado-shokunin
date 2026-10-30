# R56W3ScoutNewSrc2 — independent re-verification of the S397 proc_pid_fdinfo(5) source

Seat: R56W3ScoutNewSrc2 (leaf; no subagent dispatch; read-only outside my own seat directory).
Item attacked: the **S397** row of `.ufo/waves/round-56/attempt2/s396-s397-draft.md` — the proposed registry row for
`https://man7.org/linux/man-pages/man5/proc_pid_fdinfo.5.html`.
Deliverable: `.ufo/waves/round-56/w3/R56W3ScoutNewSrc2/receipts/s397-independent.md`.
Scratch (removed before yield): `/fast/scratch/hyaku/mado-r56/R56W3ScoutNewSrc2/`.

## Verdict

**AGREES** with the draft row on the URL, the pin bytes and the man-pages release; **DIFFERS** on the anchor cell's
date and on the locator list's coverage of the fields the row itself teaches. The row's central premise — that the
page documents **one fdinfo line per monitored file** — is **CONFIRMED** at the cited line 160.

## What I did

1. Fetched the URL myself with curl into scratch (never reusing the lane's pin as the source of truth), hashed it,
   and compared against the draft's cell-6 sha256/size/line-count claims.
2. Read the man-pages release string from the fetched bytes' footline and colophon, and corroborated it upstream
   (`git ls-remote` on the man-pages tag, `git log` on the page path in the 6.19 tree, kernel.org mirror listing).
3. Extracted the inotify fdinfo field definitions with line numbers: `wd` 164, `ino` 166, `sdev` 168, `mask` 171-172,
   the fhandle/exportfs condition 174-176, and the per-monitored-file statement 160-162.
4. Diffed the draft's S397 row against those observations cell by cell.
5. Byte-tested the draft's quotes the way the C1 `quote:<id>` leg does, and against the lane's own landed K29/K30
   man-page quotes.
6. Measured the counter interaction of the two proposed rows on scratch clones of the tip: both counters with the
   rows appended; `used-by` set to a lesson path vs a real entry path; the mined-row flip ordering hazard.

## Decisive output (trimmed)

```
$ curl -sS -L --fail -o proc_pid_fdinfo.5.html https://man7.org/linux/man-pages/man5/proc_pid_fdinfo.5.html ; sha256sum ; wc -lc
exit=0
f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1  proc_pid_fdinfo.5.html
 366 14694 proc_pid_fdinfo.5.html
        -> matches the draft's "14694 B sha256:f9e12387..." exactly, and the lane's own copy of the same bytes

$ grep -o 'Linux man-pages 6\.19 *[0-9-]*' proc_pid_fdinfo.5.html
Linux man-pages 6.19            2026-07-18          <- the draft's cell 6 says (2026-02-14)
$ grep -n 'tarball' proc_pid_fdinfo.5.html
266:       This page was obtained from the tarball man-pages-6.19.tar.gz   -> release 6.19 CONFIRMED

$ python3 -I ... # lines of the fetched bytes
160 |        Each of the lines beginning with "inotify" displays information
161 |        about one file or directory that is being monitored.  The fields
162 |        in this line are as follows:
164 |        <i>wd</i>     A watch descriptor number (in decimal).
166 |        <i>ino</i>    The inode number of the target file (in hexadecimal).
168 |        <i>sdev</i>   The ID of the device where the target file resides (in
171 |        <i>mask</i>   The mask of events being monitored for the target file (in
174 |        If the kernel was built with exportfs support, the path to the
175 |        target file is exposed as a file handle, via three hexadecimal
176 |        fields: <i>fhandle-bytes</i>, <i>fhandle-type</i>, and <i>f_handle</i>.

$ # upstream man-pages 6.19 history for this page
2026-07-18 man/man5/proc_pid_fdinfo.5: Document that 'ino' and 'mnt_id' are decimal numbers
2026-07-18 man/man5/proc_pid_fdinfo.5: Document the 'ino' field
   -> the pinned bytes are the 2026-07-18 state of the page; 2026-02-14 is inotify.7.html's date (S390's page)

$ # counters at the tip with the two drafted rows appended verbatim
MADO_USED_BY: rev=HEAD entries=71 rows=334 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none   exit=0
MADO_AUTORELOAD_ENTRY: rev=HEAD rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none          exit=0

$ # S397 used-by = corpus/lessons/round-56.md   (the draft's stated failure mode)
MADO_USED_BY: ... extra=0 ... verdict=TARGET_MET missed=none      exit=0   -> the draft's reason is NOT the mechanism
$ # S397 used-by = a real corpus/knowledge path not citing S397
MADO_USED_BY: ... extra=1 ... verdict=TARGET_MISSED missed=extra  exit=1
$ # S397 flipped to mined, used-by still em dash, entry cites S397
MADO_USED_BY: ... missing=1 ... verdict=TARGET_MISSED missed=missing exit=1   -> landing-ordering hazard
```

## Defects

| # | defect | input that shows it | severity |
|---|---|---|---|
| D1 | S397's anchor cell dates the page `2026-02-14`; the page's footline and the upstream 6.19 log both say **2026-07-18** (2026-02-14 is inotify.7.html's date, S390's). The sibling draft row S396 has the same copy error (its page's footline is 2026-02-08). | footline grep; upstream `git log` for `man/man5/proc_pid_fdinfo.5`; `man7-inotify.7.html` footline 2026-02-14 | **weakens the claim** — citation accuracy in a proposed row's cell 6; no frozen leg reads cell 6, so not blocking |
| D2 | S397's locator list `160,164,171` does not cover `ino` (166) or `sdev` (168) — two of the four fields its own proposition names. Latent C1 `scope:<id>` failure (`scope_covers()` requires the registry row's own locator list to cover the entry row's line). | locator table in the receipt §4; `quality/counters/c1-r56-autoreload-entry.py` `scope_covers()` | **weakens the claim** |
| D3 | The row teaches "the running compositor's watch table is readable without touching it" but cites neither lines 174-176 nor the **exportfs condition** under which a *path* (vs. an identity) is exposed. | lines 174-176 of the fetched bytes | **weakens the claim** |
| D4 | The draft's supporting quotes for 164/171 are tag-stripped; the C1 quote leg matches **raw** bytes, and the lane's own K30 precedent keeps the markup (`Don't dereference <i>pathname</i> …`). | raw-vs-stripped byte test in the receipt §5; K29/K30 raw test both True | **weakens the claim** (draft-quote surface form) |
| D5 | The draft's stated reason for `used-by —` ("a lesson path in used-by would flip TARGET_MET to TARGET_MISSED") is wrong: the counter's `USED_BY` regex only matches `corpus/knowledge/*.md`, so a lesson path is invisible to it. The conclusion (`queued` + `—`) is right and matches all 10 existing `queued` rows; only the reason is wrong. | two-way measurement in the receipt §7 | **cosmetic** (draft rationale) |
| D6 | The two new pins are **untracked** at the tip (`?? .ufo/waves/round-56/fetch/man7-proc_pid_fdinfo.5.html`) and absent from `receipts/pins-extra.sha256` (1 line, PropRefresher.hpp only). The C1 `pin_hash` leg does not cover them — the round-56 **M56-9** class. | `git cat-file -e <tip>:<path>` → absent; `git status --porcelain`; pins-extra.sha256 | **weakens the claim** (landing requirement) |

Cross-source note, independently confirmed (not taken on report): the man page says `wd` is "in decimal" (line 164),
but the kernel prints it in **hex** — `fs/notify/fdinfo.c:87`: `seq_printf(m, "inotify wd:%x ino:%llx sdev:%x mask:%x …")`.
The lane's own committed capture agrees with the kernel (the 40 `wd` values parse as hex to exactly `{1..0x28}` and
`int('1f',10)` raises). Also confirmed: `ignored_mask`'s prose (lines 207-209) is in the **fanotify** section, and the
inotify section (150-176) defines no `ignored_mask` — so the fanotify definition must not be transferred. The S397 row
names only the four fields that do have inotify-scope definitions, so it is clean on that point. The `wd` radix point
is a trap for the *lesson text*, not a defect in the row.

**No defect found would change a frozen predicate, a counter output, or a kill rule.** All six live in the proposed
rows' own cells, the draft's rationale, or the landing sequence — all correctable in row text.

**Route propagation.** The peer seat `R56W3ConnCrossSrc` proposes a Paths route `S390 → S396 → S383 → S397`; all six
defects apply across that chain, not just to S397. D1 is a *propagation along the route* — `2026-02-14` is S390's own
page date, so correcting only S397 leaves S396 with the same wrong date; the fix belongs to the row-construction
step. D2 applies to whichever route row names fields its locator list omits; D3/D4 apply to whichever route row ends
up teaching the fdinfo fields (S397 is the route's only row on this page); D6 is a landing prerequisite for both
S396 and S397 and is not discharged by the route's hops. No counter output moves under any of it — the route is a
provenance question, not a predicate question.

## Deliverable paths

* `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScoutNewSrc2/receipts/s397-independent.md`
* `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScoutNewSrc2.md` (this report)

## What I could not verify

* No live `/proc/<pid>/fdinfo` read — not this seat's remit; the 40-watch/40-wd figures are from the committed
  attempt-1 capture, checked only for internal consistency.
* `check-r56-controls.py --claim c1/c3` (the harnesses) was **not** run; §7 exercises the counters themselves. The
  harness legs are unaffected by two extra `queued` rows by inspection — **stated as inference, not measurement**.
* S396/S397 are not in the registry at the tip (332 rows, last id S395), so all counter numbers above come from
  scratch copies with the rows appended.
* Whether the intended date convention was the page's footline date or something else (e.g. the 6.19 release date
  2026-08-25) — the footline date is the only self-consistent reading of the existing S390 row; I flag the ambiguity
  rather than pick.

## Tooling

No tools installed, upgraded or removed — the task needed only `curl`, `git` (read-only: `ls-remote`, `clone
--shared` into scratch, `cat-file`, `log`, `status --porcelain` with `GIT_OPTIONAL_LOCKS=0`) and `python3 -I`.
Per the pacman guard, no pacman transaction was attempted.
