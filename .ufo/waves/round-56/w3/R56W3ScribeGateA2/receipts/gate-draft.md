# Gate draft — attempt 2, rows S396 and S397 (seat R56W3ScribeGateA2, 2026-10-30)

Draft for the L1 to integrate into `corpus/lessons/round-56.md` (attempt-2 `## Gate`). Nothing here is landed; the
registry rows are the L1's. Both pages were opened by this seat on 2026-10-30 (independent `curl` to scratch); the
fetched bytes are byte-identical to the L1's pins and to the lane's working-tree copies in `.ufo/waves/round-56/fetch/`:

- `man7-inotify_add_watch.2.html` — 11,345 B — sha256 `98fe7feb381fa2687e8a3962e6d78a49cb1ad07c543f93449dcb42d6712c3d6d` — page footline **Linux man-pages 6.19, 2026-02-08** (tarball man-pages-6.19.tar.gz, HTML rendering created 2026-09-09)
- `man7-proc_pid_fdinfo.5.html` — 14,694 B — sha256 `f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1` — page footline **Linux man-pages 6.19, 2026-07-18** (same tarball and rendering date)

## Gate

### New source rows opened this round (2026-10-30), tier B docs, read from the fetched bytes above (sha256 in the anchor cells)

| row | URL | accessed | located quote |
|---|---|---|---|
| S396 | `https://man7.org/linux/man-pages/man2/inotify_add_watch.2.html` | 2026-10-30 | `already being watched (perhaps via a different link to the same` (:93) |
| S397 | `https://man7.org/linux/man-pages/man5/proc_pid_fdinfo.5.html` | 2026-10-30 | `Each of the lines beginning with "inotify" displays information` (:160) |

- **S396** — located quote `already being watched (perhaps via a different link to the same` (:93, 11 words, byte-exact).
  The sentence completes at :94: `object), then the descriptor for the existing watch is returned.` (:94, 10 words, byte-exact).
  The per-instance scoping the taught claim must carry is on the same page: :89 `descriptor for this inotify instance, for the filesystem object` and :91 `not previously being watched by this inotify instance, then the`.
  Recommended anchor cell: `inotify_add_watch.2.html:88-94 @ Linux man-pages 6.19 (2026-02-08)` — it covers the unique-descriptor sentence (:88-90), both per-instance qualifiers (:89, :91) and the reuse sentence (:92-94), and stays inside the pin's 259 split-lines (E3 bound).
  Why the lane lacked it: the registry's only inotify man page is S390 (inotify(7)), whose pinned line :90 says a call `creates a new watch item, or modifies an existing watch` and whose IN_MASK_CREATE note (:293-302) says several paths may name one inode and unguarded calls may clobber masks, so the kernel rule the entry's duplicate-path sentence asserts — that the second add returns the same descriptor — was held by no row until this page, which states it at :92-94.
- **S397** — located quote `Each of the lines beginning with "inotify" displays information` (:160, 9 words, byte-exact).
  The sentence completes at :161: `about one file or directory that is being monitored.  The fields` (:161, 11 words, byte-exact); the field definitions are :164 (`wd`), :166 (`ino`), :168-169 (`sdev`), :171-172 (`mask`); the sample block :153-158 shows one such line per watched file, and the read-access statement is :72-77 (`readable only by the owner of the process`, :74).
  Recommended anchor cell: `proc_pid_fdinfo.5.html:160-172 @ Linux man-pages 6.19 (2026-07-18)` (add `72-77` only if the `teaches` cell keeps a readability clause).
  Why the lane lacked it: the registry has no `/proc` or fdinfo row at all (grep of `corpus/SOURCES.md`: zero hits for `fdinfo` and `/proc`), so the attempt-1 comparison that read the compositor's 40 watches out of `/proc/<pid>/fdinfo` (`w2/R56W2RevProcFdinfo/comparison.md`) decoded `wd`, `ino`, `sdev` and `mask` with no row defining those fields; the entry itself labels that reading "not a row".

### Byte-exactness and quote discipline

- Every quoted string above is a contiguous byte substring of the single stated pin line (verified with `python3 -I`; none of the quoted lines carries HTML markup, so no tag stripping is involved).
- A quote spanning :93-94 joined at the wrap is **not** byte-contiguous (the file has a newline plus indentation between `same` and `object),`); a single-line quote is also what the C1 quote leg would demand if a future entry row cites these pins (`quality/counters/c1-r56-autoreload-entry.py` tests `quote.encode("utf-8") in pin_line`, one line).
- The L1 draft's designated S396 quote at :88, `A successful call to inotify_add_watch() returns a unique watch`, is **not** byte-exact: the pin's bytes at :88 are `A successful call to <b>inotify_add_watch</b>() returns a unique watch`. The lane's own frozen rows keep markup in quotes (entry K30: `Don't dereference <i>pathname</i> if it is a symbolic link.`), so a markup-bearing quote of :88 is acceptable — this draft simply grounds the row's scope on :93 instead.
- The L1 draft's S397 quote at :160 is byte-exact as written (no markup on that line); this draft keeps it.

### Landing notes for the L1 (each verified this seat; none is landed by this seat)

1. **Anchor date defect (both rows).** The draft's anchor cells say `@ Linux man-pages 6.19 (2026-02-14)` — that is inotify(7)'s footline date (S390). The pages' own footlines read **2026-02-08** (inotify_add_watch(2)) and **2026-07-18** (proc_pid_fdinfo(5)). Severity: weakens the row (the anchor misstates the pinned revision).
2. **Anchor ranges.** Draft S396 anchor `88,93` leaves :94 — the `descriptor for the existing watch is returned` conclusion — outside; draft S397 anchor `160,164,171` leaves :161 (one monitored file per line), :166 (`ino`) and :168-169 (`sdev`) outside. Use `88-94` and `160-172`. Severity: weakens the row (the taught claim must sit inside the anchor).
3. **Per-instance qualifier.** The draft's S396 `teaches` cell states the reuse rule without the qualifier the page carries at :89 and :91; the taught sentence must read "within the same inotify instance". Severity: weakens the claim (the unqualified form overstates the rule).
4. **`queued` + `used-by —` rationale is false (measured).** The draft keeps both rows `queued` with `used-by —` because "a lesson path in `used-by` would flip `TARGET_MET` to `TARGET_MISSED` at the new tip". Measured on the frozen counter at a scratch commit that appends both rows with `mined` and `used-by = corpus/lessons/round-56.md`:
   `MADO_USED_BY: rev=cd0c017219a9482b3dc2fbdcf92c3d16a22d1b9f entries=71 rows=334 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none` (exit 0).
   The frozen parser collects cell-11 paths with `USED_BY = re.compile(rb"corpus/knowledge/[A-Za-z0-9_.-]+\.md")` (`quality/counters/c3-r56-used-by.py:51` at the tip), so a lesson path is never parsed into `USEDBY` and cannot trip `extra`; and since no entry cites S396/S397, `missing` has no pairs. Per CORPUS `## used-by` ("knowledge entries **or lessons** citing the row") and `## status` (`mined` = cited by at least one such path), a lesson-cited row is `mined` with the lesson path. Sibling seat `R56W3RevLessonGate` reached the same conclusion independently.
5. **Census safety (measured).** With the rows appended and mined + lesson path, `scripts/sources-census.sh validate` exits 0 and its findings are byte-identical to the same run without the rows (38 lines before, 38 after, `diff` empty); no E-code and no W-code mentions S396/S397 (the URLs are new, so no W04; used-by is non-empty, so no W03). If the attempt-2 lesson lands as a **new** file rather than an append to `corpus/lessons/round-56.md`, the `used-by` cell must name that file and it must exist on disk at census time (E11).
6. **New ids are free and the pins are untracked.** 332 registry rows at tip, last id S395, so S396/S397 continue the registry (no E03/E04). The two pin files the draft anchors cite exist only in the working tree — `git ls-files --error-unmatch` fails for both — so they must be added to the tree when the rows land, or the anchor cells point at paths absent from the repository (M56-9 class; the C1 `pin_hash` leg covers only the frozen pin set, so no counter would catch it).
7. **Routed prose observation (entry, frozen at tip — not edited here).** `corpus/knowledge/hyprland-config-autoreload-r56.md:46` attributes "the kernel keeps one watch per inode, the second add returns the same descriptor and modifies the watch" to `inotify(7) lines 90-92 and 296-302`; those lines say `creates a new watch item, or modifies an existing watch`, `Each watch has a unique "watch descriptor"` and (IN_MASK_CREATE) `multiple paths may refer to the same inode ... may clobber existing watch masks` — the returned-descriptor statement itself is not in them. S396 (:92-94) is the verbatim ground for that clause.
8. **S397 `teaches` wording.** `so the running compositor's watch table is readable without touching it` — the page grounds readability by the owner (:74) and the per-line format (:160-161); "without touching it" is the lane's own read-only-method statement, and the 40/40 result is the wave-2 comparison's, not the man page's. Scope the cell accordingly.

### Receipt

Commands and outputs for every claim in this draft are in `receipts/gate-draft-evidence.txt`; the fetched pin bytes are
`receipts/man7-inotify_add_watch.2.html` and `receipts/man7-proc_pid_fdinfo.5.html` (byte-identical to the lane's
working-tree copies and to the draft's stated sizes and sha256 values).
