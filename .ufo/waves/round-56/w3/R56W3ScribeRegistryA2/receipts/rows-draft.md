# Round 56 attempt 2 — draft registry rows S396 and S397 (seat R56W3ScribeRegistryA2)

Authored 2026-10-30 by seat R56W3ScribeRegistryA2 (scribe). Draft only: nothing in the lane is
edited by this seat. The rows below are proposals for the L1 to land inside the `## Registry`
section of `corpus/SOURCES.md` immediately after the `S395` row.

Base revision of the copied registry: lane tip `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`
(332 registry rows, 71 knowledge entries).

## Pin provenance — the pins existed; I did not re-fetch them into the lane

The two pins were already present in the lane working tree when this seat started:

```
$ ls -la /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/fetch/
-rw-r--r-- 1 vgpnk vgpnk 11345 Oct 30 02:02 man7-inotify_add_watch.2.html
-rw-r--r-- 1 vgpnk vgpnk 14694 Oct 30 02:02 man7-proc_pid_fdinfo.5.html
```

They are **untracked** at the tip (`git status --porcelain` shows `??` for both), so they are not
yet part of any commit; the L1 must add them with the rows.

```
$ sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html \
            /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/fetch/man7-proc_pid_fdinfo.5.html
98fe7feb381fa2687e8a3962e6d78a49cb1ad07c543f93449dcb42d6712c3d6d  man7-inotify_add_watch.2.html
f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1  man7-proc_pid_fdinfo.5.html
```

I independently re-fetched both URLs into scratch and the bytes are identical to the lane's copies
(so the pin sha256s are upstream-verifiable, not just locally asserted):

```
$ curl -sS -o up-inotify_add_watch.2.html https://man7.org/linux/man-pages/man2/inotify_add_watch.2.html
$ curl -sS -o up-proc_pid_fdinfo.5.html  https://man7.org/linux/man-pages/man5/proc_pid_fdinfo.5.html
$ cmp up-inotify_add_watch.2.html .../fetch/man7-inotify_add_watch.2.html   # identical
$ cmp up-proc_pid_fdinfo.5.html  .../fetch/man7-proc_pid_fdinfo.5.html    # identical
98fe7feb381fa2687e8a3962e6d78a49cb1ad07c543f93449dcb42d6712c3d6d  up-inotify_add_watch.2.html
f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1  up-proc_pid_fdinfo.5.html
```

Sizes: 11345 B and 14694 B (`stat -c %s`).

Both pages come from man-pages 6.19 (COLOPHON in each pin: "obtained from the tarball
man-pages-6.19.tar.gz"; upstream mirror lists `man-pages-6.19.tar.xz` dated 25-Aug-2026; the
tarball's own `Changes` says "Released: 2026-08-25").

## The two rows (verbatim, as they would land)

```
| S396 | Linux man-pages 6.19 inotify_add_watch(2) man page - https://man7.org/linux/man-pages/man2/inotify_add_watch.2.html | docs | B | the kernel one-watch-per-inode rule behind the watcher's duplicate-path and symlink watch rows | inotify_add_watch.2.html:88-94 @ Linux man-pages 6.19 (2026-02-08); pin .ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html 11345 B sha256:98fe7feb381fa2687e8a3962e6d78a49cb1ad07c543f93449dcb42d6712c3d6d | a successful inotify_add_watch returns a unique watch descriptor per filesystem object within one inotify instance, and an object already watched, even through a different link, returns its existing descriptor | queued | 2026-10-30 | 90d | — |
| S397 | Linux man-pages 6.19 proc_pid_fdinfo(5) man page - https://man7.org/linux/man-pages/man5/proc_pid_fdinfo.5.html | docs | B | the /proc fdinfo fields the watch-table comparison reads | proc_pid_fdinfo.5.html:104-105,157-158,160-161,164,166,168-169,171-172 @ Linux man-pages 6.19 (2026-07-18); pin .ufo/waves/round-56/fetch/man7-proc_pid_fdinfo.5.html 14694 B sha256:f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1 | each inotify line of an fdinfo file names one watched file or directory by watch descriptor, inode, device and event mask, and the inotify inode there is hexadecimal while the fdinfo header's own ino field is decimal, so a running compositor's watch table can be read without touching it | queued | 2026-10-30 | 90d | — |
```

Both rows: 11 cells, `NF=13` under `awk -F'|'`, no `|` inside any cell, id continues the sequence
after `S395`, `used-by` is the em dash.

### Anchor cell, line by line

**S396** — `inotify_add_watch.2.html:88-94`. Lines 88-94 of the pin are the DESCRIPTION paragraph
that carries both halves of the claim:

```
 88:       A successful call to <b>inotify_add_watch</b>() returns a unique watch
 89:       descriptor for this inotify instance, for the filesystem object
 90:       (inode) that corresponds to <i>path</i>.  If the filesystem object was
 91:       not previously being watched by this inotify instance, then the
 92:       watch descriptor is newly allocated.  If the filesystem object was
 93:       already being watched (perhaps via a different link to the same
 94:       object), then the descriptor for the existing watch is returned.
```

The pin is 258 lines, so the locator is in range. Note the man-page text says the uniqueness is
**"for this inotify instance"** — the scope cell and the teaches cell both keep that qualifier
(a second inotify instance gets its own descriptor for the same inode).

**S397** — `proc_pid_fdinfo.5.html:104-105,157-158,160-161,164,166,168-169,171-172`. The pin is
366 lines; every locator is in range. The lines are:

```
104:       <i>ino</i>    This field, present since Linux 5.14, is the decimal inode
105:               number of the file.
157:               inotify wd:2 ino:7ef82a sdev:800001 mask:800afff ignored_mask:0 ...
158:               inotify wd:1 ino:192627 sdev:800001 mask:800afff ignored_mask:0 ...
160:       Each of the lines beginning with "inotify" displays information
161:       about one file or directory that is being monitored.  The fields
162:       in this line are as follows:
164:       <i>wd</i>     A watch descriptor number (in decimal).
166:       <i>ino</i>    The inode number of the target file (in hexadecimal).
168:       <i>sdev</i>   The ID of the device where the target file resides (in
169:               hexadecimal).
171:       <i>mask</i>   The mask of events being monitored for the target file (in
172:               hexadecimal).
```

Line 160-161 is the "one file or directory per line" ground (the page's own words), 164/166/168/171
are the four field definitions the wave-2 comparison reads, 104-105 is the header `ino` field
(decimal) that the teaches cell contrasts against, 157-158 is the worked example the page prints.

### Anchor dates: the pages' own footers, not a copied date

Each man page prints its own release date in its footline; the two differ:

```
man7-inotify_add_watch.2.html:165: <span class="footline">Linux man-pages 6.19  2026-02-08   inotify_add_watch(2)</span>
man7-proc_pid_fdinfo.5.html:276:  <span class="footline">Linux man-pages 6.19  2026-07-18    proc_pid_fdinfo(5)</span>
```

and the source tarball agrees (`.TH inotify_add_watch 2 2026-02-08`,
`.TH proc_pid_fdinfo 5 2026-07-18`). The rows therefore carry `(2026-02-08)` and `(2026-07-18)`,
each page's own date. The string `2026-02-14` appears **zero** times in either new pin
(`grep -c "2026-02-14"` returns 0 for both) — it is the date on the *old* `man7-inotify.7.html`
pin that the `S390` row quotes, and copying it into these two rows would misdate both.

## Census validation of the draft registry

Registry = copy of `corpus/SOURCES.md` at `0f3a5436` with the two rows inserted after `S395`,
inside the `## Registry` section (which runs to `## Paths` at line 349 of the draft).

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
      --file <scratch>/full/corpus/SOURCES.md.draft --today 2026-10-30
rc=0
$ diff <(sed 's/SOURCES.md.draft/SOURCES.md/' final-validate.txt) baseline-full-validate.txt
(no differences — identical finding set to the unedited baseline)
```

The finding set is the 37 pre-existing `W04`/`W01` warnings plus `file ok`; the baseline (unedited
copy of the same file at the same revision) produces exactly the same lines, so the two rows add
**no** new census finding and no `E` code. Specifically: no `E01` (11 cells), no `E02` (id shape),
no `E03` (duplicate id), no `E04` (duplicate URL+scope), no `E05`/`E06`/`E07` (kind/tier/status
enums), no `E08` (opened date), no `E09` (recheck), no `E11` (used-by path on disk — not checked for
`queued` rows), no `E12` (row outside the Registry section).

Census counts move exactly as expected: `rows` 332 → 334, `tier.B` 5 → 7, `status.queued` 10 → 12.

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file <scratch>/full/corpus/SOURCES.md.draft
file	rows	334
file	tier.A	320
file	tier.B	7
file	tier.C	7
file	status.mined	311
file	status.queued	12
file	status.rejected	11
FLEET	rows	334
```

## Frozen counters re-run against the draft (scratch clone, scratch commit)

Registry-only scratch commit on top of the tip; the lane itself is untouched.

```
$ git -C <scratch clone> rev-parse --show-toplevel
/fast/scratch/hyaku/mado-r56/R56W3ScribeRegistryA2/tmp.gW816VRnQW     (the clone, not the lane)
$ python3 -I quality/counters/c3-r56-used-by.py --repo <clone> --rev 0cb102f010e63c77d291686c48be445404bb9a24 --work <scratch>
MADO_USED_BY: rev=0cb102f010e63c77d291686c48be445404bb9a24 entries=71 rows=334 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none
rc=0
$ python3 -I quality/counters/c1-r56-autoreload-entry.py --repo <clone> --rev 0cb102f010e63c77d291686c48be445404bb9a24 --work <scratch>
MADO_AUTORELOAD_ENTRY: rev=0cb102f010e63c77d291686c48be445404bb9a24 rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none
rc=0
$ python3 -I quality/check-r56-controls.py --claim c3 --repo <clone> --rev 0cb102f010e63c77d291686c48be445404bb9a24 --work <scratch>
MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK
rc=0
$ python3 -I quality/check-index.py --repo <clone> --rev 0cb102f010e63c77d291686c48be445404bb9a24
MADO_INDEX: rev=0cb102f010e63c77d291686c48be445404bb9a24 indexed=71/71 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
rc=0
$ python3 -I quality/check-tool-ledger.py --repo <clone> --rev 0cb102f010e63c77d291686c48be445404bb9a24
LEDGER: population=97 ledger_rows=97 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET rev=0cb102f010e63c77d291686c48be445404bb9a24
rc=0
```

`check-index-rows.py` also passes (`rows=71 errors=0 warns=3`; the three warns are pre-existing
`cited-glob-nomatch` warnings in unrelated rows, identical to the baseline).

## Constraint the L1 must respect: `used-by` must track the citation, both ways

The C3-v2 `missing` and `extra` legs are symmetric, and both fire on a half-landed row. Measured
on scratch clones, each mutation one step from the draft:

| scratch mutation | C3 verdict |
|---|---|
| draft as drafted (no entry citation, `used-by —`) | `missing=0 extra=0 … verdict=TARGET_MET` rc=0 |
| entry `source:` line cites S396 and S397, `used-by` stays `—` | `missing=2 … verdict=TARGET_MISSED missed=missing` rc=1 |
| entry `source:` line cites S396 and S397 **and** `used-by` names the entry | `missing=0 extra=0 … verdict=TARGET_MET` rc=0 |
| `used-by` names the entry but no entry cites the rows | `extra=2 … verdict=TARGET_MISSED missed=extra` rc=1 |
| the **lesson** (`corpus/lessons/round-56.md`) cites S396 and S397 | `missing=0 extra=0 … verdict=TARGET_MET` rc=0 |

So the landing state "queued + `used-by —`" is only safe while the *knowledge entry* does not cite
the rows. A lesson-text citation is safe: `ENTRIES` is `corpus/knowledge/*.md` only, so a lesson
mention is not a `CITE` and does not create a pair. This matches the L1's stated plan in
`.ufo/waves/round-56/attempt2/s396-s397-draft.md` ("Citation lives in the attempt-2 lesson Gate
text"), and the D7 row above confirms it empirically.

The rows must also stay `queued` for the frozen C1 claim. The C1 counter's `source_cell` leg
requires a cited row to be `mined`, tier A or B, opened `2026-10-28`, with a URL ending in
`c1.pin_suffix[pin]` and containing the rev token, and the used-by cell naming the entry. A
`queued` row with `used-by —` cannot satisfy any of that, so if a future round cites S396 from a K
row, that row also needs `mined`, opened `2026-10-28` and an entry-matching used-by. Measured:

```
$ (K03 cites S396 instead of S383; S396 present as a queued row)
MADO_AUTORELOAD_ENTRY: … sources=29/30 scope=29/30 … verdict=TARGET_MISSED missed=prov,source_cell:K03,scope:K03
rc=1
```

This is expected for a `queued` row and is not a defect in the draft; it is the shape a later
round must satisfy before citing either row from an entry.
