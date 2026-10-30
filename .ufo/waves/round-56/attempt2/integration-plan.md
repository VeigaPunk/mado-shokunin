# Attempt-2 integration checklist (L1; executed after w3 settles, before the report)

## Registry rows (insert AFTER line 345 of corpus/SOURCES.md, inside ## Registry; S395 is the last row)

Row text (final form, `mined` — the attempt-2 lesson Gate cites both rows; the C3 counter
tolerates a lesson path in cell 11 — probe `receipts/attempt2-l1.txt` + the
c3-probe receipt: extra=0 TARGET_MET at scratch revs 6c7cc56d/b271ee45):

| S396 | Linux man-pages 6.19 inotify_add_watch(2) man page - https://man7.org/linux/man-pages/man2/inotify_add_watch.2.html | docs | B | the kernel one-watch-per-inode rule behind the watcher duplicate-path and symlink watch rows | inotify_add_watch.2.html:88,93 @ Linux man-pages 6.19 (2026-02-14); pin .ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html 11345 B sha256:98fe7feb381fa2687e8a3962e6d78a49cb1ad07c543f93449dcb42d6712c3d6d | a successful inotify_add_watch returns a unique watch descriptor for the filesystem object (inode), and an object already watched returns its existing descriptor | mined | 2026-10-30 | 90d | corpus/lessons/round-56.md |
| S397 | Linux man-pages 6.19 proc_pid_fdinfo(5) man page - inotify fields - https://man7.org/linux/man-pages/man5/proc_pid_fdinfo.5.html | docs | B | the /proc fdinfo fields the watch-table comparison reads | proc_pid_fdinfo.5.html:160,164,171 @ Linux man-pages 6.19 (2026-02-14); pin .ufo/waves/round-56/fetch/man7-proc_pid_fdinfo.5.html 14694 B sha256:f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1 | each inotify fdinfo line is one monitored file with wd, ino, sdev and mask fields, so the running compositor watch table is readable without touching it | mined | 2026-10-30 | 90d | corpus/lessons/round-56.md |

(Adjust ONLY on a RevLessonGate/ScribeRegistryA2 ADMIT-WITH-EDITS verdict; census E12 fix =
rows must sit inside ## Registry. Gates quote pin lines 88 (S396) and 160/164/171 (S397).)

## Steps

1. Collect w3 seat reports; build the dead-seat table from w3-results.json.
2. Apply blocking findings as content edits (entry/rows/docs); re-run the three frozen
   gates + census + selftest after ANY edit (content revision moves).
3. Insert the registry rows; run census validate --file on a scratch copy, then the real
   census (expect `mado ok`, 334 rows, exit 0).
4. Append the round-55 correction block (from ExecInherited deliverable) to
   corpus/lessons/round-55.md (append-only).
5. Append the attempt-2 section to corpus/lessons/round-56.md (Gate with S396/S397 quotes +
   spot-check-pending note; Registry changes old→new; Mistakes M56-11+ from findings).
6. Append the LOG attempt-2 entry (LOG-draft.md, filled).
7. Land new instruments from seats: quality/check-anchor-cover.py (ExecCrit107Build, with
   ledger row in quality/tool-ledger.md), kill fixtures + runners (MutKill*), any other
   committed instrument — every new quality/*.py or quality/counters/*.py needs a
   tool-ledger row (population predicate) and keeps LEDGER TARGET_MET.
8. Update SCORECARD round-56 section: attempt-2 paragraph (wave w3 settled, receipts at the
   new final revision), capabilities row unchanged (evidence pointer gains the second
   /proc sample), 'Planned (round 57)' stays.
9. Update corpus/README.md frontier bullet ONLY if the wave changes a claim of fact.
10. Commit via jj-lane.sh (round-56 message), verify ls-remote; then write the report at
    .ufo/reports/round-56/mado.md (required sections; SHONEN grep -c '^## SHONEN' = 1) and
    fleet-commit.sh --as mado; remove /fast/scratch/hyaku/mado-r56.
