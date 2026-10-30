# Attempt-2 draft registry rows (S396, S397) — authored by the L1 2026-10-30, pre-integration

Both sources were opened by the L1 this attempt (curl 2026-10-30, bytes pinned under
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/fetch/`). Both rows land
`queued` with `used-by —`: no knowledge entry cites them yet, and the frozen C3 counter's
`extra` leg counts any used-by path outside the entry set, so a lesson path in `used-by`
would flip `TARGET_MET` to `TARGET_MISSED` at the new tip. Citation lives in the attempt-2
lesson Gate text; the rows flip `queued`→`mined` (logged old→new) only when an entry cites
them in a later round.

## Proposed row S396

| S396 | Linux man-pages 6.19 inotify_add_watch(2) man page - https://man7.org/linux/man-pages/man2/inotify_add_watch.2.html | docs | B | the kernel's one-watch-per-inode rule behind the watcher's duplicate-path and symlink watch rows | inotify_add_watch.2.html:88,93 @ Linux man-pages 6.19 (2026-02-14); pin .ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html 11345 B sha256:98fe7feb381fa2687e8a3962e6d78a49cb1ad07c543f93449dcb42d6712c3d6d | a successful inotify_add_watch returns a unique watch descriptor for the filesystem object (inode), and an object already watched - even via a different link - returns its existing descriptor | queued | 2026-10-30 | 90d | — |

- Gate quote (line 88 of the pin): `A successful call to inotify_add_watch() returns a unique watch` (continuation line 93: `already being watched (perhaps via a different link to the same` / `object), then the descriptor for the existing watch is returned.`).
- Access date 2026-10-30; fetched bytes sha256 `98fe7feb381fa2687e8a3962e6d78a49cb1ad07c543f93449dcb42d6712c3d6d` (11,345 B, 258 lines).
- Why the lane lacked it: the round-56 entry's duplicate-path prose (M56-10 corrections: "the kernel keeps one watch") was grounded only in the entry's reading of ConfigWatcher/absolutePath pins and the kernel lab; the man-page statement of the one-watch-per-inode rule was not held by any row.

## Proposed row S397

| S397 | Linux man-pages 6.19 proc_pid_fdinfo(5) man page - inotify fields - https://man7.org/linux/man-pages/man5/proc_pid_fdinfo.5.html | docs | B | the /proc fdinfo fields the 40/40 watch-table comparison reads | proc_pid_fdinfo.5.html:160,164,171 @ Linux man-pages 6.19 (2026-02-14); pin .ufo/waves/round-56/fetch/man7-proc_pid_fdinfo.5.html 14694 B sha256:f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1 | each inotify fdinfo line is one monitored file with wd, ino, sdev and mask fields, so the running compositor's watch table is readable without touching it | queued | 2026-10-30 | 90d | — |

- Gate quote (line 160 of the pin): `Each of the lines beginning with "inotify" displays information` (field definitions at lines 164 `wd     A watch descriptor number (in decimal).` and 171 `mask   The mask of events being monitored for the target file (in`).
- Access date 2026-10-30; fetched bytes sha256 `f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1` (14,694 B, 366 lines).
- Why the lane lacked it: the attempt-1 `/proc` comparison (`w2/R56W2RevProcFdinfo/comparison.md`) read fdinfo fields with no sourced row for what the fields mean; the method's ground was prose, not a registry row.

## Reviewer questions (R56W3RevLessonGate)

1. Are the quotes located and ≤25 words, and do the taught claims stay within the pinned lines?
2. Is `queued` + `used-by —` right under CORPUS rule status definitions and the C3 `extra` leg?
3. Do the tier/kind/scope cells overreach? (S390 precedent: man page = tier B docs.)
4. Census shape: 11 cells, no `|` in any cell, id continues the registry (S395 is the last row).
