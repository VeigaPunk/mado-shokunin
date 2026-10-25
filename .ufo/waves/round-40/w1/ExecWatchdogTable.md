# ExecWatchdogTable — report

Read-only digest of dead attempts and dirty closures for mado, rounds 32–39. No lane/fleet source
file, config tree, index or compositor state was touched; no package transaction, no git/jj mutation,
no background job, no subagent. Nothing was installed (no tool needed: `grep`, `python3` stdlib only).

## Files written (only these)

- `mado-shokunin/.ufo/waves/round-40/w1/ExecWatchdogTable/table.md` — the deliverable table (180 lines).
- `mado-shokunin/.ufo/waves/round-40/w1/ExecWatchdogTable.md` — this report.

## Result (all numbers reproduced by the commands in table.md §E; verified by re-running them)

| round | launches | `lane-dead-no-report` | complete line | completion time | elapsed first launch→complete | spot-check names leftover working-tree files |
|---|---|---|---|---|---|---|
| 32 | 1 | 0 | 1 | `2026-10-24T20:33:30-03:00` | 36m52s | yes — `round-32-verifier-spotcheck.md:18` (5 paths, round-30 leftovers) |
| 33 | 1 | 0 | 1 | `2026-10-24T21:30:29-03:00` | 32m18s | yes — `:19` (`untracked=19`) |
| 34 | 1 | 0 | 1 | `2026-10-24T22:55:29-03:00` | 1h14m33s | no — `:43` (`untracked=0`, porcelain empty) |
| 35 | 2 | 1 | 1 | `2026-10-25T03:53:57-03:00` | 4h39m19s | yes — `:46-48` (`tracked=8 untracked=2`) |
| 36 | 1 | 0 | 1 | `2026-10-25T05:41:00-03:00` | 1h31m55s | yes — `:21` (untracked `DistillerFindings.md`) |
| 37 | 2 | 1 | 1 | `2026-10-25T09:35:45-03:00` | 3h30m06s | no — `:20-21` (porcelain empty) |
| 38 | 1 | 0 | 1 | `2026-10-25T12:49:09-03:00` | 2h09m56s | yes — `:17` (3 modified seat reports) |
| 39 | 1 | 0 | 1 | `2026-10-25T17:15:05-03:00` | 1h18m49s | no — `:17` (porcelain empty) |
| **32–39** | **10** | **2** | **8** | — | — | 5 yes / 3 no |

Counting commands (cwd `/home/vgpnk/Projects/shokunin`, NN = round):

```sh
grep -c " launch mado round=NN pgid=" .ufo/watchdog.log
grep -c " lane-dead-no-report mado round=NN;" .ufo/watchdog.log
grep -c " complete mado round=NN;" .ufo/watchdog.log
grep -c -E ' launch mado round=3[2-9] pgid=' .ufo/watchdog.log          # 10
grep -c -E ' lane-dead-no-report mado round=3[2-9];' .ufo/watchdog.log  # 2
grep -c -E ' complete mado round=3[2-9];' .ufo/watchdog.log             # 8
```

Dead lines (verbatim, the only two in the slice):

- r35 `:1245` — `2026-10-25T03:23:08-03:00 lane-dead-no-report mado round=35; retry same round (hyaku-inline attempt=1: run-6: attempt-1 orphan — no report, session died 2026-10-24 ~23:30 -03)`
- r37 `:1303` — `2026-10-25T06:46:34-03:00 lane-dead-no-report mado round=37; retry same round (hyaku-inline attempt=1: run-6: L1 returned after 40m with no commits and no report (abandoned mid-round; uncommitted work inherited by next attempt))`

## Evidence retained in table.md

- §Pins: watchdog sha256 `5827413…4631` / 1418 lines at first read, re-checked `7844337…8e2b` /
  1419 lines (one appended line, `launch kama round=42`, not mado; mado counts identical).
- §A/§A2: per-round counts with the `grep -c` in each cell; per-attempt spans for the two
  multi-attempt rounds (r35 attempt 1 = 4h08m30s to the dead line, attempt 2 = 30m19s; r37 attempt 1 =
  40m55s, gap 2h03m42s, attempt 2 = 45m29s).
- §B/§B2: leftover verdict + mention count (uniform regex) + `grep -F -c` = 1 for the quoted decisive
  fragment, and the full spot-check lines verbatim.
- §D: all 20 mado 32–39 log lines verbatim with line numbers; §E every command; §F the elapsed-time
  script.

## Checks I ran on my own artifact (the measurement is the deliverable)

- Table A cells vs re-run `grep -c` for rounds 32–39: `table=[1,0,1] … greps=[1,0,1]`, all 8 OK.
- Completion timestamps and elapsed strings vs the log/script: 8/8 present and equal.
- Quote transcription: 20 cited source lines (r32:18,84; r33:19,23; r34:41-43,207; r35:46-48,217-220;
  r36:21; r37:20-21; r38:17; r39:17) — a 40-char mid-line slice of each is present verbatim in
  table.md: `quote slices missing: none`.

## Risks / limits (stated, not resolved)

- The leftover column's uniform regex is a **phrase-mention** count, not a verdict: it also matches
  negating lines (r37 `No uncommitted round work`, r39 `PASS`). The yes/no is read off the quoted line
  and pinned by the fixed-string grep; table.md §G says so explicitly.
- r32's leftovers are round-30 files (`:18`, `:84`), r34's `:207` names r33's 19 paths as a
  cross-reference while r34 itself is clean. Both are stated as quotes; no classification beyond the
  quoted text was added.
- The watchdog log is live: counts hold for any append after line 1419, but a new `lane-dead-no-report
  mado round=3[2-9]` line would change a row (none can appear for a round whose `complete` line is
  already logged, except by a later correction the log has never carried).
- No claim, gate, counter or axis is referenced; nothing here is scored, and no interpretation of the
  dead attempts was offered beyond the verbatim lines.
