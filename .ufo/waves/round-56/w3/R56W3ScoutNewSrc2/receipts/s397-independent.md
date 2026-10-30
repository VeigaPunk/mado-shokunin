# S397 — independent re-verification of the proc_pid_fdinfo(5) source

Seat: R56W3ScoutNewSrc2 (leaf; read-only; no lane writes other than this seat directory).
Subject: the S397 row of `.ufo/waves/round-56/attempt2/s396-s397-draft.md` — the proposed registry row for
https://man7.org/linux/man-pages/man5/proc_pid_fdinfo.5.html.
Method: fetch the URL myself into scratch (no reuse of the lane's pin as the source of truth), hash it, read the
inotify field definitions, then diff against the draft row. All commands run from
`/fast/scratch/hyaku/mado-r56/R56W3ScoutNewSrc2/` with `TMPDIR` never relied upon.

## Verdict

**AGREES** on the row's identity, pin bytes and release, with **one date defect** and **one scope defect**.

| item | draft says | independently observed | verdict |
|---|---|---|---|
| URL | `https://man7.org/linux/man-pages/man5/proc_pid_fdinfo.5.html` | same URL fetched OK (HTTP 200) | AGREES |
| pin sha256 | `f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1` | **identical** on my own fetch | AGREES |
| pin size / lines | `14694 B`, `366 lines` | `14694` bytes, `366` lines | AGREES |
| man-pages release | `Linux man-pages 6.19` | footline `Linux man-pages 6.19`, colophon `man-pages-6.19.tar.gz` | AGREES |
| anchor date in cell 6 | `@ Linux man-pages 6.19 (2026-02-14)` | this page's footline reads **2026-07-18** | **DIFFERS** |
| locator `160` | "one line per monitored file" | confirmed at 160-162 | AGREES |
| locator `164` | `wd` field definition | confirmed at 164 | AGREES |
| locator `171` | `mask` field definition | confirmed at 171-172 | AGREES |
| proposition "one monitored file with wd, ino, sdev and mask" | fields named | all four defined at 164/166/168/171 — but the **row's locator list cites only 160,164,171, so `ino` (166) and `sdev` (168) are cited in the proposition and taught by the page, yet are NOT in the row's own locator set** | **DIFFERS (scope)** |

## 1. Independent fetch, sha256, release

```
$ mkdir -p /fast/scratch/hyaku/mado-r56/R56W3ScoutNewSrc2 && cd /fast/scratch/hyaku/mado-r56/R56W3ScoutNewSrc2
$ curl -sS -L --fail -o proc_pid_fdinfo.5.html https://man7.org/linux/man-pages/man5/proc_pid_fdinfo.5.html
exit=0
$ sha256sum proc_pid_fdinfo.5.html
f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1  proc_pid_fdinfo.5.html
$ wc -l -c proc_pid_fdinfo.5.html
 366 14694 proc_pid_fdinfo.5.html
```

The draft's cell-6 pin claim `14694 B sha256:f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1` is
**byte-for-byte correct**, and it also equals the sha256 of the lane's already-fetched copy
`.ufo/waves/round-56/fetch/man7-proc_pid_fdinfo.5.html` (same digest, same 14694 B) — the lane's pin and the live
URL agree, so nothing has drifted upstream.

Release string, from the fetched bytes:

```
$ grep -o 'Linux man-pages 6\.19 *[0-9-]*' proc_pid_fdinfo.5.html
Linux man-pages 6.19            2026-07-18
$ grep -n 'tarball' proc_pid_fdinfo.5.html
266:       This page was obtained from the tarball man-pages-6.19.tar.gz
$ grep -n 'fetched from' -A1 proc_pid_fdinfo.5.html
269:       2026-09-09.
```

So the page is man-pages **6.19**, rendered from the 6.19 tarball, fetched 2026-09-09. Independently corroborated
upstream: `git ls-remote .../man-pages.git refs/tags/man-pages-6.19` → `5a7bf78fd314b8390f30bee87aa2e933b7a8f880`,
tag commit `adb436b2e4471218021d86f188fb58dec3946eb8` "Changes: Ready for 6.19" dated 2026-08-25; the kernel.org
mirror lists `man-pages-6.19.tar.gz 25-Aug-2026 17:43`.

## 2. The inotify fdinfo field lines (raw, with line numbers)

```
150 |        For inotify file descriptors (see <a href="../man7/inotify.7.html">inotify(7)</a>), we see (since Linux
151 |        3.8) the following fields:
...
157 |            inotify wd:2 ino:7ef82a sdev:800001 mask:800afff ignored_mask:0 fhandle-bytes:8 fhandle-type:1 f_handle:2af87e00220ffd73
158 |            inotify wd:1 ino:192627 sdev:800001 mask:800afff ignored_mask:0 fhandle-bytes:8 fhandle-type:1 f_handle:27261900802dfd73
160 |        Each of the lines beginning with "inotify" displays information
161 |        about one file or directory that is being monitored.  The fields
162 |        in this line are as follows:
164 |        <i>wd</i>     A watch descriptor number (in decimal).
166 |        <i>ino</i>    The inode number of the target file (in hexadecimal).
168 |        <i>sdev</i>   The ID of the device where the target file resides (in
169 |               hexadecimal).
171 |        <i>mask</i>   The mask of events being monitored for the target file (in
172 |               hexadecimal).
```

### 2a. The "one line PER MONITORED FILE" ground — CONFIRMED

Line 160-162 is exactly the ground the seat asks about: *"Each of the lines beginning with "inotify" displays
information about one file or directory that is being monitored."* So one inotify fdinfo line = one monitored
file/directory, and the block of such lines is the kernel's watch table for that inotify instance. **The S397
proposition's premise is directly supported by the pinned page at the cited line 160.**

The host evidence agrees with the reading, from the attempt-1 capture already committed at
`.ufo/waves/round-56/w2/R56W2RevProcFdinfo/fdinfo-capture.txt`: 40 `inotify ` lines in each of the two inotify fds
(12 and 86), 40 distinct `wd` values, matching the 40 primary watches. I did not re-read `/proc` — that is not this
seat's remit and the capture is the committed evidence.

### 2b. The fhandle fields' exportfs condition — CONFIRMED at lines 174-176

```
174 |        If the kernel was built with exportfs support, the path to the
175 |        target file is exposed as a file handle, via three hexadecimal
176 |        fields: <i>fhandle-bytes</i>, <i>fhandle-type</i>, and <i>f_handle</i>.
```

This is a genuine *conditional* on the kernel build, and it is the only route by which the fdinfo exposes a
**path** rather than an identity. The S397 row's cell 5 scope says "the /proc fdinfo fields the 40/40 watch-table
comparison reads" and its cell 7 proposition ends "so the running compositor's watch table is readable without
touching it". The **watch table** (wd/ino/sdev/mask per monitored file) is readable from fdinfo unconditionally;
but the **path→file mapping** is readable only via the fhandle trio, and only *if* the kernel has exportfs support.
The host capture shows the fhandle fields are populated on this host (`fhandle-bytes:14 fhandle-type:4d`), so on
this host the condition holds — but the row does not say so, and the row's locator list does not include 174-176.
**Severity: weakens the claim** (the row overstates what the cited lines establish: lines 160-176 document the
fields and the exportfs condition, but the row cites neither 174-176 nor the condition).

## 3. DEFECT 1 — the anchor date is wrong for this page (severity: weakens the claim; not blocking)

The draft's cell 6 reads:

```
proc_pid_fdinfo.5.html:160,164,171 @ Linux man-pages 6.19 (2026-02-14); pin .ufo/waves/round-56/fetch/man7-proc_pid_fdinfo.5.html 14694 B sha256:f9e1...
```

The date `(2026-02-14)` is **this page's wrong date** — it is inotify.7.html's date, not proc_pid_fdinfo.5.html's.
Evidence:

* this page's own footline: `Linux man-pages 6.19   2026-07-18   proc_pid_fdinfo(5)`
* upstream man-pages 6.19 log for `man/man5/proc_pid_fdinfo.5`: the newest two commits are both **2026-07-18**
  ("Document that 'ino' and 'mnt_id' are decimal numbers" and "Document the 'ino' field", Maja Kądziołka) — the
  page's rendered content was last changed on 2026-07-18, and that is what the footline prints.
* the date **2026-02-14** belongs to `man/man7/inotify.7` (S390's page): its footline reads
  `Linux man-pages 6.19   2026-02-14   inotify(7)` and its upstream log for 6.19 also tops out at 2026-02-14.

So the S396/S397 draft rows were written by copying S390's date cell and pasting the new page's locators into it.
The same copy error is in the sibling draft row S396, whose page `man7-inotify_add_watch.2.html` carries
footline date **2026-02-08** (upstream log for `man/man2/inotify_add_watch.2` in 6.19 also tops out 2026-02-08), not
2026-02-14.

```
$ for f in man7-inotify.7.html man7-inotify_add_watch.2.html man7-proc_pid_fdinfo.5.html; do ... grep footline ...; done
man7-inotify.7.html            -> Linux man-pages 6.19            2026-02-14
man7-inotify_add_watch.2.html  -> Linux man-pages 6.19            2026-02-08
man7-proc_pid_fdinfo.5.html    -> Linux man-pages 6.19            2026-07-18
```

**Not blocking, and not a frozen-predicate change.** The date lives in cell 6 (`anchor`) of a row that is not yet
in the registry; no frozen leg reads it. The C1 `scope:<id>` leg reads only the locator list after `<basename>:`
(`quality/counters/c1-r56-autoreload-entry.py`, `scope_covers()`); the C3 counter does not read cell 6 at all
(`parse_registry()` reads only the id and cell 11). So a wrong date here cannot flip a counter. It is a
**citation-accuracy defect in a proposed row**: it asserts the pinned bytes come from a 2026-02-14 state of a page
whose 2026-07-18 state is what is pinned. Fix = write the footline date (`2026-07-18` for S397, `2026-02-08` for
S396), or drop the date and cite the tarball+tag.

## 4. DEFECT 2 — the locator list omits two of the four fields the row teaches (severity: weakens the claim)

The row's proposition names four fields — "wd, ino, sdev and mask" — but its locator list is `160,164,171`:

| field | definition line | in the row's locator list? |
|---|---|---|
| wd | 164 | yes |
| ino | 166 | **no** |
| sdev | 168 | **no** |
| mask | 171-172 | yes (171) |

Two of the four fields the proposition names are not covered by the row's own anchor. This matters for the
C1 `scope:<id>` leg, which requires the *registry row's* locator list to contain a range covering the entry row's
line: `scope_covers(cells[5], basename_of(pin), line, len(pl))`. If a later round grounds an entry row on this page
at line 166 (`ino`) or 168 (`sdev`) via S397, that leg fails — a locator-only defect, the same shape as the round-56
M56-8 "E-row anchors were outside the registry anchors" defect already logged in `corpus/lessons/round-56.md`.
The fix is to widen the row's locator list to `160,164,166,168,171` (and 174-176 if the fhandle/exportfs condition
is taught), not to change any predicate.

## 5. The quotes in the draft, byte-checked (the C1 `quote:<id>` leg's own test)

The draft's gate quote is `Each of the lines beginning with "inotify" displays information` (line 160). Against the
**raw** pinned bytes:

```
S397-160 in RAW line 160 -> True
S397-164 in RAW line 164 -> False    (raw is '       <i>wd</i>     A watch descriptor number (in decimal).')
S397-171 in RAW line 171 -> False    (raw is '       <i>mask</i>   The mask of events being monitored ...')
```

The draft's own text quotes 164 and 171 in **tag-stripped** form (`wd     A watch descriptor...`), while the
lane's committed precedent for a man-page row quotes the **raw** bytes including markup — the landed entry row
K30 quotes `Don't dereference <i>pathname</i> if it is a symbolic link.` and that string *is* a byte-substring of
the raw pin line 262:

```
K29 quote in RAW line 186 -> True
K30 quote in RAW line 262 -> True
```

The C1 counter's quote test is exactly byte-literal against the raw blob: `qok = pl is not None and quote.encode("utf-8") in pl`
(`quality/counters/c1-r56-autoreload-entry.py`). So a Gate quote written in stripped form for 164/171 would
**not** pass that leg if it were later frozen into an entry row. **Severity: weakens the claim** — the draft's
supporting quotes for the two field-definition lines are in the wrong surface form; the pin is HTML and the counter
matches raw bytes. (The line-160 gate quote is fine as written.)

## 6. A cross-source note, confirmed independently: `wd` is printed in HEX by the kernel

The man page says `wd` is "A watch descriptor number (in decimal)" (line 164). The kernel's own source says
otherwise — `fs/notify/fdinfo.c`:

```
87 | seq_printf(m, "inotify wd:%x ino:%llx sdev:%x mask:%x ignored_mask:0 ",
```

`%x` is hexadecimal. The man page is wrong here (an upstream man-pages defect, still present in 6.20 and in
upstream master: `A watch descriptor number (in decimal).`). The lane's own committed capture agrees with the
kernel: the 40 `wd` values in `w2/R56W2RevProcFdinfo/fdinfo-capture.txt` parse as HEX to exactly `{1..0x28}`
and **cannot** be parsed as decimal at all (`int('1f', 10)` raises ValueError). The attempt-1 comparison script
`w2/R56W2RevProcFdinfo/compare.py` already handles this correctly — it parses `wd` with `int(wd,16)`.

This is consistent with the peer report from `R56W3ConnCrossSrc`. It is **not** a defect in the S397 row as drafted
(the row's proposition says only "wd, ino, sdev and mask fields", asserting no radix), but it constrains what a
lesson may safely claim *from* this row: any statement about the `wd` value's radix must not be sourced to line
164. Severity: cosmetic for the row; a real trap for the lesson text.

Also confirmed for the peer report's second point: the inotify example lines 157-158 show `ignored_mask:0`, but the
prose that defines `ignored_mask` (lines 207-209) sits in the **fanotify** section (which explicitly says "Most of
these fields are as for inotify, except: mflags, mask, ignored_mask" at 200-209). The inotify section proper
(150-176) defines only `wd`, `ino`, `sdev`, `mask` and the fhandle trio — there is **no** inotify-scope prose for
`ignored_mask`. So the fanotify definition must not be transferred to inotify. The S397 row names only the four
fields that do have inotify-scope definitions, so it is clean on this point.

## 7. Counter interaction of the proposed rows (measured, not asserted)

I appended the two drafted rows verbatim to a scratch copy of the tip registry and re-ran both frozen counters.
Nothing in the frozen predicate moves:

```
$ python3 -I quality/counters/c3-r56-used-by.py --repo . --rev HEAD --work <w>
MADO_USED_BY: rev=HEAD entries=71 rows=334 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none
exit=0
$ python3 -I quality/counters/c1-r56-autoreload-entry.py --repo . --rev HEAD --work <w>
MADO_AUTORELOAD_ENTRY: rev=HEAD rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none
exit=0
```

Two things to note for the L1, both measured:

* **`rows` goes 332 → 334.** The frozen C3 sentence is `MADO_USED_BY: rev=<rev> entries=<E> rows=<R> missing=0 ...`
  with `<E>`/`<R>` as *placeholders*, so the frozen sentence is not violated by a different row count; but the
  committed receipt `receipts/at-final.txt` and `receipts/attempt2-l1.txt` both record `rows=332`, and the frozen
  *baseline* in `frozen-tables-v2.json` is `rows=319` at the base revision. The frozen `c3.base_pairs_sha256`
  covers the base-revision pair set, not the row count, so `lost`/`stale` are unaffected (measured: `lost=0`).
  The row count in the *target* receipt will read 334 whenever the rows land. Worth stating in the lesson so the
  receipt and the claim sentence are not read as contradicting each other.
* **`used-by —` + `queued` is what keeps the C3 `extra` leg at 0.** The `extra` leg counts used-by paths outside
  the entry set. I verified the mechanism both ways:
  * S397 `used-by` = a real knowledge entry path that does not cite S397 → `extra=1 ... verdict=TARGET_MISSED missed=extra`.
  * S397 `used-by` = `corpus/lessons/round-56.md` → **still `extra=0`, `TARGET_MET`** — because the counter's
    `USED_BY` regex is `corpus/knowledge/[A-Za-z0-9_.-]+\.md`, which never matches a `corpus/lessons/` path.
  So the draft's stated reason for `used-by —` ("a lesson path in used-by would flip TARGET_MET to TARGET_MISSED")
  is **not the mechanism**: a lesson path in `used-by` is invisible to the C3 counter, not fatal. The real reason
  `used-by —` is right is the `queued` status plus the C1 `source_cell:<id>` leg, which requires
  `cells[7] == "mined"` and `ENTRY in cells[10]` for a row to be a valid source cell. A `queued` row with
  `used-by —` is inert to both counters, which is what the draft wants. **Severity: cosmetic** (the draft's
  conclusion is right; its stated reason is wrong and would mislead the lesson).

  And the draft's own `queued`-row convention checks out against the registry: all 10 existing `queued` rows at the
  tip carry `used-by` = `—`, so `S396`/`S397` with `queued` + `—` matches the established shape. (20 existing rows
  do name a lesson path in `used-by`; that is a different, mined-row convention and not applicable to a `queued` row.)

* **Landing hazard, measured.** A `queued` row flips to `mined` only when an entry cites it — and if the flip and
  the entry's citation happen together while `used-by` is still `—`, the C3 `missing` leg fires. Reproduced:
  S397 flipped to `mined` with `used-by —` while the entry's `source:` line cites S397 →
  `missing=1 extra=0 ... verdict=TARGET_MISSED missed=missing`, exit 1. The fix is the ordering the draft already
  implies: when the row flips to `mined`, `used-by` must name the entry in the same change. This is a sequencing
  rule for the future round, not a defect in the drafted row.

## 8. Pin tracking — the two new pins are untracked at the tip

```
$ git cat-file -e 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/fetch/man7-proc_pid_fdinfo.5.html
-> UNTRACKED-at-tip
$ GIT_OPTIONAL_LOCKS=0 git status --porcelain -- .ufo/waves/round-56/fetch/
?? .ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html
?? .ufo/waves/round-56/fetch/man7-proc_pid_fdinfo.5.html
```

Both new pins exist only as untracked working-tree files. The S390 precedent (`man7-inotify.7.html`) *is* tracked at
the tip, so the drafted rows' anchor cells point at a path that does not exist in the committed tree. This is the
round-56 **M56-9** class already disclosed in `corpus/lessons/round-56.md` ("a pin and a row entered after the
freeze with no frozen hash… the counter's `pin_hash` leg does not cover it. Disclosed."): `frozen-tables-v2.json`
`c1.pin_sha256` names only the eight original pins, so the C1 `pin_hash` leg will not check these two. The
mitigation the lesson names is `receipts/pins-extra.sha256`, which at the tip holds exactly one line (the
PropRefresher.hpp pin) and does **not** yet cover either new man page. **Severity: weakens the claim** — the rows'
sha256 evidence is only reproducible from the working tree, not from the revision; the L1 must commit the two pins
and add them to `receipts/pins-extra.sha256` in the same change that lands the rows.

## 9. Summary of defects, with severities

| # | defect | evidence | severity |
|---|---|---|---|
| D1 | S397 anchor cell dates the page `2026-02-14`; the page's footline and upstream 6.19 history both say **2026-07-18** (2026-02-14 is inotify.7.html's date). Same copy error in S396 (should be 2026-02-08). | footline grep; upstream `git log` for `man/man5/proc_pid_fdinfo.5` | weakens the claim (cell-6 citation accuracy; no frozen leg reads it → not blocking) |
| D2 | S397's locator list `160,164,171` does not cover `ino` (166) or `sdev` (168), two of the four fields its own proposition names — a latent C1 `scope:<id>` failure if an entry row is later grounded on those lines. | locator table §4; `scope_covers()` | weakens the claim (fix in the row's cell 6; no predicate change) |
| D3 | The row teaches "the watch table is readable without touching it" but cites neither lines 174-176 nor the exportfs condition under which a *path* (as opposed to an identity) is exposed. | lines 174-176 | weakens the claim |
| D4 | The draft's supporting quotes for lines 164 and 171 are tag-stripped; the C1 quote leg matches raw bytes, and the lane's own K30 precedent keeps the markup. | §5 byte test; K29/K30 raw test | weakens the claim (draft-quote surface form) |
| D5 | The draft's stated reason for `used-by —` (a lesson path would trip the C3 `extra` leg) is wrong: the counter's `USED_BY` regex only matches `corpus/knowledge/*.md`, so a lesson path is invisible to it. The conclusion is right; the reason is not. | §7 two-way measurement | cosmetic (draft rationale; row itself correct) |
| D6 | The two new pins are untracked at the tip and absent from `receipts/pins-extra.sha256`; the C1 `pin_hash` leg does not cover them (M56-9 class). | §8 | weakens the claim (landing requirement) |

No defect found here would change a frozen predicate, a counter output, or a kill rule; all six are in the
proposed rows' own cells / draft rationale / landing sequence, and are therefore correctable in the row text.

## 10. What I could NOT verify

* I did not re-read `/proc/<pid>/fdinfo` for the live compositor — that is not this seat's remit (the host section
  of my brief names R56W3ExecReverifyC2, R56W3ExecLiveGetoption, R56W3RevProcFdinfo, R56W3RevWatchTable for that
  read). The 40-watch/40-wd figures come from the committed attempt-1 capture, which I checked only for internal
  consistency (40 `inotify` lines per fd, 40 distinct wd, wd parseable only as hex).
* I did not verify the *drafted* S397 row against a live registry, because S396/S397 are not in the registry at the
  tip (confirmed: 332 rows, last id S395, `grep -c proc_pid_fdinfo corpus/SOURCES.md` = 0). The counter
  interactions in §7 are measured on scratch copies with the rows appended.
* I did not run `check-r56-controls.py --claim c1/c3` (the harnesses). §7 exercises the two counters themselves,
  which is what the row additions can move; the harness control legs are untouched by adding rows (control 1
  replaces the registry with its base bytes, control 2 fills every used-by, control 7 replaces the allowlist — none
  is sensitive to two extra `queued` rows), but I did not measure that, so I state it as inference and not as
  verification.
* Whether the 2026-07-18 upstream revision of the page should be the cited version at all, or whether the
  2026-02-14 is meant to denote the man-pages 6.19 release (2026-08-25) — the draft's own convention is
  ambiguous here, and the page's footline date is the only self-consistent reading. I flag it rather than pick.

## 11. Cross-source attribution and the proposed Paths route

The `wd`-radix contradiction (§6) was reached independently here from the kernel source
(`fs/notify/fdinfo.c`, `wd:%x`) and from the lane's own committed capture — not taken on report. The peer seat
`R56W3ConnCrossSrc` reached the same conclusion from the cached capture and has already recorded it in its own
connector report; the formatter/source-side boundary it flagged as unverified is closed by §6 above (the kernel
format string is the formatter). **Attribution for the wd-radix and formatter findings stays with this report**;
`R56W3ConnCrossSrc` retains attribution for its connector-route observation. Neither seat made integration or row
edits.

`R56W3ConnCrossSrc`'s proposed Paths route is `S390 → S396 → S383 → S397`. **Every defect in §9 applies across that
whole chain, not only to S397**, and the chain makes D1 sharper rather than weaker:

* D1 (the wrong date) is a *propagation* along that chain. The draft's two new rows both carry `2026-02-14`, which
  is S390's page date — the route's own first hop. Correcting only S397 leaves S396 with the same wrong date; the
  fix belongs to the row-construction step, not to the last row.
* D2 (the locator list omitting `ino` 166 and `sdev` 168) applies to any row on that route whose proposition names
  fields its own locator list does not cover.
* D3 (the exportfs condition at 174-176) and D4 (raw-byte quote surface form) apply to whichever row on the route
  ends up teaching the fdinfo fields, since S397 is the route's only man-page row on this page.
* D6 (the two pins untracked at the tip, absent from `receipts/pins-extra.sha256`) is a landing prerequisite for
  both S396 and S397 and must be satisfied in the same change that commits the rows — the route's hops do not
  discharge it.

No counter output moves under any of this; the route's ordering is a provenance question, not a predicate question.
