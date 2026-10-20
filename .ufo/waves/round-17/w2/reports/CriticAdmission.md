# CriticAdmission — round-17 admission case, attacked as a whole

Seat: `MadoR17.CriticAdmission` (critic, wave 2, FALSIFY). Lane HEAD
`988b858bd6049bc709807534fd725c05264f7e60` (worktree HEAD equals it; 5 untracked
wave-2 paths, none read as evidence). Read at 2026-10-20T11:56:10-03:00.

**Bottom line.** Every headline number reproduces. No axis is harmed by a lane
action that I can find. The attack on the numbers failed. The attack on the
**wording** succeeded in six places (W1–W6 below). Each one is a sentence that
says more than its receipt shows. None of them changes a score.

## Axes

| Axis / sub-axis | Before → after (re-measured here) | Harmed? | Verdict wording allowed |
|---|---|---|---|
| calibration / literal lesson-citation fraction | 14/22 = 6.3636 → 15/23 = 6.5217 | no | improved narrowly (+0.1581) |
| coverage / rubric V (P1–P6, declared this round) | 2/6 = 3.3333 → 4/6 = 6.6667 | no | improved on a rubric declared and baselined this round; documentary routes only |
| coverage / U-route (harm watch) | 7/7 → 7/7 | no | unchanged (finite ceiling) |
| coverage / navigation (harm watch) | 30/30 → 32/32, missing/extra/dup empty | no | unchanged-complete (+2 rows) |
| operability / capability | absent → tripwire selftests 9/9, 16/16, 33/33 | no new harm | capability acquired, detection after the fact only; R15-V1 harm carried |
| operability / legacy suites (harm watch) | 372/372, 52/52 (round 16) | not observed | **bytes unchanged, not re-executed this round** (W5) |
| freshness / file-plane (harm watch) | 29/29 (round 12) | not caused by the lane | **not re-measured**; host packages moved under the pins by a non-mado `-Syu` (W4) |
| depth, adjacency | unscored | — | unchanged, unscored |

## Claims, receipts, reproduction

| Claim | Receipt | Re-run here | Result |
|---|---|---|---|
| C1 14/22 → 15/23 | `evidence/measure-before.json`, `measure-c1.json`; `git show REV:corpus/QUALITY.md \| grep -cE` | literal greps at `27cd06f` / `988b858`; `python3 .ufo/waves/round-17/measure.py` both revs; round-16 `measure.py 988b858` | 14/22 and 15/23; lesson-grounded ids `…21,22,23`. Only criterion 23 added. QUALITY/SOURCES/README/round-16 lesson diffs are pure appends (`git diff --stat 27cd06f 988b858`: 0 deletions) |
| C1 red/green label check | `evidence/label-check.txt` | `python3 -I .ufo/waves/round-17/label-check.py` | `LABEL_SUMMARY: 4/7`, `EXPECT_SUMMARY: 7/7`, exit 1 (declared reds) |
| C2 2/6 → 4/6 | `measure-before.json`, `measure-c2.json`, `measure-instrument.json` | round-17 `measure.py 27cd06f` / `988b858` | P1 (U1,U2 legacy), P2 (U7 legacy), P4 `terminal-route-r17.md` (S056–S060), P6 `idle-lock-route-r17.md` (S063–S069); P3, P5 false |
| C2 sources | SOURCES S056–S070 | `sources-census.sh validate … mado` | exit 0; only historical W04 S030/S042/S045 (unchanged from `census-start.txt`) |
| C2 version anchors | notes cite pacman.log :639, :1792, :1798, :2935 | `sed -n` on `/var/log/pacman.log` | all four lines carry exactly the quoted text; no later alacritty/hypridle/hyprlock line |
| C3 selftests | `evidence/tripwire-selftest-{core,compound,hardening}.txt` | `--selftest` on each suite | `9/9`, `16/16`, `33/33`, exit 0 each |
| C3 anchor | `evidence/tripwire-anchor-r15.txt` | `--scan …/MadoR15/MadoR15.LibinputEvents.jsonl` | exit 1; stdout sha256 `dc3827df…f7cc` = receipt, byte-identical; tuple line 54 `call_38165` host_mutation `sudo` + `pacman:-S` present among 8 findings |
| C3 4/4 join | `evidence/tripwire-pacmanlog-join.txt` (L1-authored text, not tool output) | pacman.log :2410/2416/2422/2423/2429 and `tripwire-r13..r16.txt` findings | 4/4 by command string; **3/4 by same-second timestamp** (W2) |
| U 7/7, navigation | round-16 `measure.py 988b858` | same | `coverage.count 7`, navigation 32/32, gate sha `fba82a66…`, `gate_executed: false`, `safety_executed: false` |

## Counterexamples and precision defects

**W1 — "non-lane" is right but has no receipt; "round launch 10:51" has no committed anchor.**
SCORECARD.md:893-894 and lesson `round-17.md:18` (M5) say "13 non-lane runs …
07:45-09:39 … none after round launch / 0 lines from round launch 10:51". The count is right:
13 `[PACMAN] Running` lines at pacman.log:2440, 2448, 2454, 2461, 2462, 3064,
3085, 3091, 3092, 3125, 3126, 3132, 3152 (07:45:36 to 09:39:21 -0300). The
attribution has no receipt. I could not falsify it, and the metadata supports it:
- The indexed mado transcripts end before the window. `session-index.json`
  shows R16's last record at 09:13:27Z (06:13 -0300). Session `01a156ff…` .jsonl
  was last modified at 06:37:05 -0300. `MadoR17.jsonl` (L1) was born at
  10:51:52.15 -0300 (`stat %w`).
- `find ~/.omp/agent/sessions -maxdepth 2 -newermt '2026-10-20 07:30' ! -newermt '09:57'`
  finds no `-Projects-shokunin*` session file. It does find other OMP sessions
  that were active in the window: `-tmp/…10-42-30Z…` until 08:51,
  `-tmp/…10-59-55Z…` until 08:54, and `-Documents-nvhelpme/…11-58-22Z…` until
  09:55. I read names and mtimes only, not their contents.

So the most the lane can say is **"not issued from any mado or shokunin-project
session"**. Who issued them is `[UNK]`: the operator or another OMP session.
"10:51" is the L1 transcript's birth time. No committed receipt carries it. The
committed anchors are `census-start.txt` 10:56:14-03:00 and commit `0175f13`
10:56:28-03:00.

**W2 — the 4/4 join is 3/4 by timestamp; :2423 rests on command text and disclosure.**
pacman.log:2410, 2422 and 2429 each fall in the same second as their
tripwire finding (04:06:49Z, 05:41:25Z, 07:25:16Z). pacman.log:2423 is
`02:41:32-0300` = 05:41:32Z. Its joined record `MadoR14.OutputSpec.jsonl:65`
is timestamped 05:45:52.190Z, **260 s after the transaction it is said to
have issued**. The receipt concedes "record time, not call time". The oracle
gives that record `0_tool_…`/`3_tool_…` call ids, i.e. several calls in one
record. Without opening the transcript (not named by this item), the link rests
on two things: the command string, and `round-14.md:111-112` ("OutputSpec
installed wlr-protocols"). The ReviewSourceBar `-Sw` 7 s earlier is an
alternative issuer that is not excluded on timing. SKILL.md:532-533 tells
readers to "confirm package transactions … by timestamp". That method does
**not** confirm :2423. This is a precision defect, not a falsified count. No
tripwire pacman host_mutation lacks a log line (5 host_mutation rows in r13–r16:
four pacman calls, all logged, plus `sudo -n true`).

**W3 — round-17 "clean" covers wave-1 seats only, and drops the L1 transcript the earlier rounds included.**
`tripwire-r17-w1.txt` scans 70 files under `…/MadoR17/` and includes no L1 file.
Every r13–r16 receipt includes its L1 transcript (`MadoR13.jsonl` … `MadoR16.jsonl`;
r16's L1 alone has `unparsed_spawns 12`). `MadoR17.jsonl` (2,251,395 B, born
10:51:52 -0300) is outside the scan, and outside wave 2's readable paths. That
transcript wrote the tripwire, ran the pacman.log awk and made the commits.
Wave 2 is not yet scanned: 79 of 148 seat files were modified after the C3 commit
at 11:50:30. The w1 result is also `clean` with `unparsed_spawns 1` and `eval_unparsed 1`.

**W4 — freshness: the host moved under present-tense pins. A non-mado actor did it, and the round recorded it.**
The same 09:15 `-Syu` (pacman.log:2462) upgraded several packages:
- hyprland 0.56.2-2 → 0.56.2-4 (:2733)
- walker 2.17.0-1 → 2.17.2-1 (:2929)
- uwsm 0.26.7 → 0.27.1 (:2926)
- systemd 261.2 → 262 (:2531)
- mkinitcpio 41.1 → 42.2 (:2539)
- linux 7.2.3 → 7.2.11 (:2855). `/proc/sys/kernel/osrelease` is now `7.2.11-arch1-1`.

Separately, elephant went 2.21.0 → 2.22.1 (:3095, yay at 09:31).

Present-tense lane text now contradicted by log bytes: `SKILL.md:23` and
`SKILL.md:114` ("walker 2.17.0"), and `hyprctl-verification-layer.md:6`
("owned by package hyprland 0.56.2-2"). The P4 note records its own
xdg-terminal-exec drift (:2935). The lane did not cause any of this, so it is
not harm by the lane. But "freshness unchanged" would imply a check that did
not happen: the r12 29/29 receipt predates the upgrade and was not re-run.

**W5 — the operability harm-watch was checked by bytes only.**
No `MADO_VERIFY:`/`MADO_SELFTEST:` line exists anywhere under
`.ufo/waves/round-17` (`git grep` count 0). The round-16 `measure.py` reports
`gate_executed: false`. The executables are byte-unchanged (`fba82a66…`,
`226220ae…`, `tools/` diff = tripwire only). Neither 372/372 nor 52/52 was
re-run at `988b858`.

**W6 — R15-V1 is now also postdated by a full upgrade.**
R15-V1 is the libinput partial upgrade (pacman.log:2429-2436, libinput
1.31.3 → 1.32.0). A full non-mado `pacman -Syu` followed at 09:15:30 (:2462),
with mkinitcpio 42 and plymouth/btrfs-overlayfs hooks run at 09:18 (:2992,
:3006). The running kernel is the upgraded one. Whether that reconciled the
partial upgrade, and whether the boot chain is healthy, is `[UNK]` and
operator-owned. The lane must call it neither resolved nor worsened.

**Self-application of QUALITY 23.** I checked lesson `round-17.md:81-88`
(selftest, anchor, r17-w1 tokens) and SCORECARD:886-891 against their
receipts. The tokens match: `findings`, exit 1, `clean`, unparsed 1/1. The join
"4/4" is an author-written sum, not a tool verdict token. Label it that way (W2).

**Minor.** `lessons/round-17.md:20`: the M2 row comes after a blank line,
outside the Mistakes table (rows M1, M3, M4, M5). Under GFM it renders as a
paragraph, not a table row. `idle-lock-route-r17.md:115` says "six host files"
but the table and line 3 list seven. Neither affects a count.

## Wording the report must use (exact)

1. Host pause: "The pause is an instruction to lanes, not a host fact.
   `/var/log/pacman.log` (3,160 lines, sha256 `f34d34e7…1e76`, read 11:56 -0300)
   records 13 `pacman` runs on 2026-10-20 07:45:36-09:39:21 -0300 (:2440-:3152),
   including a full `-Syu` at 09:15:30 (:2462). None came from a mado or
   shokunin-project session: no such session file was written in that window
   (mtime/birth metadata). Actor `[UNK]`, operator-owned. **0** `[PACMAN]` lines
   after 09:39:21 through the read time. The L1 transcript was born
   10:51:52 -0300; the pre-registration commit is 10:56:28 -0300.
   `/var/lib/pacman/local` mtime is 09:39:21. pacman.log covers libalpm only. No
   change after 10:51 in `~/.local/bin`, `~/.local/share/uv/tools`,
   `~/.cargo/bin`, `/usr/local/{bin,lib}` (find -newermt)." Do **not** say
   "paused host-wide" or "no install occurred".
2. C3 join: "4/4 mado-window pacman transactions match an issued tripwire
   host_mutation by command string. 3/4 also match to the second. :2423's issuer
   rests on command text plus the round-14 disclosure, because the matched record
   postdates it by 260 s."
3. C3 round-17 scan: "Wave-1 seat transcripts (70 files): `clean` in the covered
   forms (unparsed_spawns 1, eval_unparsed 1). The L1 transcript and wave 2 are
   not yet scanned." Upgrade this only after the close scan includes `MadoR17.jsonl`.
4. Operability: "Capability acquired: post-hoc detection over the given files,
   never interception, prevention or repair. Host-safety harm from R15-V1 stays
   carried, unresolved and operator-owned. A later non-mado full `-Syu` makes
   its current state `[UNK]`. The legacy suites are byte-unchanged and **not
   re-executed** this round."
5. Freshness: "Not re-measured. pacman.log records a non-mado package drift at
   09:16 under present-tense pins (walker 2.17.0 → 2.17.2, hyprland -2 → -4,
   uwsm, systemd, kernel). Open freshness debt, not lane harm."
6. Coverage: "Rubric V 2/6 → 4/6 on a rubric declared and baselined this round.
   P4 is credited by an Alacritty-only documentary route. P4/P6 are documentary,
   not observed behaviour. U 7/7 unchanged. Navigation 32/32." Never write
   "P4/P6 verified" or "terminal/idle coverage".
7. Admission: say "self-verdicts pending non-author closure", never "admitted".
   SHONEN stays four author assertions. Round 15 is not readmitted.

## Smallest safe corrections

- Append (never edit) a note to `evidence/tripwire-pacmanlog-join.txt` or the
  report: 3/4 same-second, and the :2423 basis per wording 2.
- At close, scan `MadoR17.jsonl` plus all wave-2 seat files, and quote counts
  and unparsed fields. Give the round-launch anchor as the `stat %w` birth time
  or the commit time, not a bare "10:51".
- Report freshness and operability harm-watch as "not re-measured" or "bytes
  unchanged". Do not re-run the live gate under the pause.

## This seat's conduct

Commands run:
- `git log|diff|grep|show|rev-parse|status` (read verbs only)
- `mado-tripwire.py --selftest` ×3 and `--scan` of the committed anchor file, once
- `label-check.py`
- round-17 `measure.py` at two revisions; round-16 `measure.py` at HEAD
- `sources-census.sh validate`
- file reads: `sed`/`grep`/`sha256sum`/`stat` of `/var/log/pacman.log`, plus
  `cat /proc/sys/kernel/osrelease`
- `find`/`stat` metadata (names, mtimes, sizes) of `~/.omp/agent/sessions` and
  the install directories listed in wording 1

Disclosure: the single anchor `--scan` read `MadoR15.LibinputEvents.jsonl`
through the tripwire tool. It is a contract-listed command, but this item does
not name the transcripts. Its output matched the committed receipt byte for
byte. I opened no transcript directly and read no `agent.db*` or credential
file. I ran no pacman, sudo, systemctl, hyprctl or other probe. I wrote only
this report. Installs: **none**.
