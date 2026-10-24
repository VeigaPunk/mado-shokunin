author: hyaku closure (non-author integrator, @m_opus)

# Round 17 — non-author verifier spot-check (mado)

Date: 2026-10-20. Closure of mado round 17, hyaku phase 2. Baseline
`27cd06f5067c3d3540ab9aa7cc734eb8eee162cc` → lane tip
`0ab1ccccaac5421f6e8ff2fe0cd2bcbd4e5bff4c` (`refs/heads/master`). The closure
did not author any of this round's work. Driver digest (`.ufo/watchdog.log`):
`2026-10-20T10:51:22-03:00 launch mado round=17 pgid=2433501 driver=hyaku-inline attempt=1`;
`2026-10-20T12:18:08-03:00 complete mado round=17; hyaku-inline attempt=1`.
Every command below was re-run at closure time. The closure did not execute
the lane's gates or probes (`tools/mado-tripwire.py`, `measure.py`,
`label-check.py`, `mado-verify.sh`). It ran plain git/grep/sha256/curl only,
with no package query and no host-surface action.

## 1. Conformance (PROTOCOL §Round-robin closure step 1)

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an %H %cI' -- .ufo/reports/round-17/mado.md` (fleet) | `mado-shokunin <mado@shokunin.local>` fb81be5 12:11:27, 3f02dd0 12:13:54, 16546d0 12:17:44 | ok |
| report lands last | lane commit times vs report commits | 6046ab7 12:10:20 < fb81be5; 9bbb881 12:13:47 < 3f02dd0; 0ab1ccc 12:17:36 < 16546d0 | ok |
| SHONEN heading | `## SHONEN`, report lines 133-138 | four `[~]` lines, one per box | ok |
| cited hashes exist + ancestry | `git cat-file -t H` and `git merge-base --is-ancestor H refs/heads/master` for 0ab1ccc 27cd06f 0175f13 f52f43f ab0bc9b a9998d1 fc6f960 245fd11 3722ba4 3e9848a 988b858 f71ccbe 6046ab7 9bbb881 | 14/14 `commit`, 14/14 ancestor | ok |
| pushed, clean | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git status --porcelain` | `state branch=master local=0ab1ccc… remote=0ab1ccc… ahead=0 behind=0 head=attached tracked=0 untracked=0`; porcelain empty; `ls-remote origin refs/heads/master` = 0ab1ccc… | ok |
| lane commit identity | `git log --format='%h %an <%ae>' 27cd06f..refs/heads/master` | 13 commits, all `mado-shokunin <mado@shokunin.local>` | ok |
| prompt carries template | rendered `templates/round-prompt.md` (c030d1f) with FLEET_ROOT/LANE/ROUND/AXES vs `.ufo/prompts/mado-round-17.md:1-140` | only placeholder substitutions differ (`<mado-repo>`→`mado-shokunin`, AXES = `coverage + operability (desktop and compositor craft)`) | ok |
| hyaku addendum §6 | prompt tail vs `scripts/hyaku/lane-addendum.md` at dispatch-time commit 4bb0943 (10:13; prompt committed 10:51:17), rendered | identical after placeholder substitution. The current addendum (67a3123, b8afbd0, after launch) differs, which is expected | ok |
| five child-lane items | grep in prompt: report path ×3, `SHONEN` ×1, commit-before-report ×2, hash rule ×3, write scope ×1, L0 ×9 | all present; no L2 route map quoted, so no MISSION bucket to compare | ok |

Conformance defects: none status-relevant (see §6 for minor ones).

## 2. Claims — re-checks

**C1 calibration (re-measured).**
`for r in 27cd06f 0ab1ccc; do git show $r:corpus/QUALITY.md | grep -cE '^[0-9]+\. .*lessons/'; … grep -cE '^[0-9]+\. '; done`
→ `27cd06f 14/22`, `0ab1ccc 15/23`. That is 6.3636 → 6.5217, which matches the report.
`git diff 27cd06f 0ab1ccc -- corpus/QUALITY.md | grep -c '^-[^-]'` → `0` (append-only).
The only new criterion is 23, and it cites `lessons/round-17.md#mistakes M1`, which exists at line 15.
It also cites the outside `round-16-verifier-spotcheck.md` R16-V1, and that file exists at 0ab1ccc.
Label check committed evidence `evidence/label-check-final.txt`:
`EXPECT_SUMMARY: 7/7`, `exit=0`, `measured_commit=f71ccbe…`, and the line
`LABEL R16-V1-red MISMATCH (receipt outcome ['frozen_error'] lacks 'snapshot_tampered')`.
Evidence-verified, not executed. Verdict: **improved**.

**C2 coverage, rubric V (re-measured by hand + every newly counting row re-opened).**
- Surface lines: `git grep -n -E '^(surface|covers): ' REV -- corpus/knowledge`.
  At 27cd06f only `covers: U1..U7` lines exist; the pinned legacy map credits
  P1 (U1, U2) and P2 (U7), giving 2/6.
  At 0ab1ccc the same lines plus `idle-lock-route-r17.md:4 surface: P6` and
  `terminal-route-r17.md:4 surface: P4` exist, giving 4/6 (P3 and P5 open).
  This matches `measure-before.json` (count 2) and `measure-final.json`
  (count 4, rev f71ccbe).
- `git diff --name-only f71ccbe 0ab1ccc` touches no `corpus/knowledge`,
  `corpus/SOURCES.md` or `PROVINCE.md` byte, so the f71ccbe measurement holds
  at the tip.
- Row join: `awk -F'|'` over the `## Registry` rows at 0ab1ccc shows:
  - S056-S060, S063-S069 and S071 are tier A, `mined`, opened 2026-10-20.
  - Their `used-by` names the citing note.
  - S061, S062 and S070 are tier C, `rejected`, `used-by —`.
  - Row count 55 → 71 (`awk … | wc -l`); 0 deleted lines.
- The author says the counter cannot tell a fetched row from an invented one,
  so the closure re-opened every tier-A row the counter credits (curl/sha256
  at closure time):

| row | re-opened | recorded sha256 | fetched | quote at cited line | words |
|---|---|---|---|---|---|
| S056 | raw xdg-terminal-exec v0.14.3 README.md | c7a1a8bb… | match (14762 B) | :166 verbatim | 11 |
| S057 | raw xdg-terminal-exec v0.14.3 script | 89f2be9a… | match (44020 B) | :106 `--dir=workdir      set workdir of terminal.` | 4 |
| S058 | raw alacritty v0.17.0 alacritty.5.scd | e444fa45… | match (28787 B) | :35-37 verbatim (wrapped) | 16 |
| S059 | host bindings.conf / xdg-terminals.list / alacritty.toml | e574a1ed… / d035da57… / 695301c8… | match / match / match (toml 28 lines) | bindings.conf:2 verbatim | 10 |
| S060 | host /usr/share/xdg-terminal-exec/xdg-terminals.list | a2b5bf69… | match (1053 B); upstream v0.14.3 list fetched: same digest | :3 verbatim | 3 |
| S063 | wiki.hypr.land hypridle page | b45c03dc… | match (254750 B) | quote present in page text | 9 |
| S064 | wiki.hypr.land hyprlock page | f69cff6b… | match (291777 B) | quote present in page text | 24 |
| S065 | raw hypridle v0.1.8 README.md | f5b852ee… | match | :6 verbatim | 10 |
| S066 | raw hypridle v0.1.8 Hypridle.cpp | 2dd4d73d6f5c… (corrected value) | match | :473 `if (MEMBER == "Lock") {` | 5 |
| S067 | raw hypridle v0.1.8 Hypridle.hpp | f9e4e558… | match | :23 verbatim | 3 |
| S068 | raw hypridle v0.1.8 main.cpp | 379bf321… | match | :61 verbatim | 5 |
| S069 | raw hyprlock v0.9.6 README.md | 83096def… | match | :5 verbatim | 4 |
| S071 | host ~/.local/share/applications/Alacritty.desktop | 713703ba… | match (452 B) | :7 `Categories=System;TerminalEmulator;` | 1 |

The tags exist (`git ls-remote`). For xdg-terminal-exec, `v0.14.3` = 065925df…,
which equals the S056 ref. For alacritty, `v0.17.0` = dc946285… and
`^{}` = 94e7c887…, which equal S058. Also present are hypridle `v0.1.8`
(e5c01af0…) and hyprlock `v0.9.6` (b222d9b1…). Result: 13/13 credited rows
reproduce byte-exactly, so no row is invented.

Note claims spot-read against the cited lines (agree on all 9):
- [HC:473/476-478]: Lock → `spawn(*LOCKCMD)` when the command is non-empty.
- [HC:128-129]: mode 3 waits only `if (m_sWaylandState.lockNotifier)`.
- [HC:70-71]: `ignoreInhibit` and `conditionCmd` are copied from the rule.
- [HH:26]: `conditionRetry`.
- [HM:55-63]: a missing config is a CRIT path.
- Wiki text: "A config file is required", "command to run when receiving a
  dbus lock event" and "3 makes your system wait until the session" are all present.
- xdg-terminal-exec:1252: `--dir=*)`.

Both notes say they are documentary routes and that no behaviour was observed. Verdict: **improved**.

**C3 operability — capability acquisition (evidence-verified; tool not executed).**
- `git show 27cd06f:tools/mado-tripwire.py` → rc 128, so the tool is absent before the round.
- Tool sha256 by revision: 988b858 `4ced68d3…`, f71ccbe `7a98720e…`, 0ab1ccc `962919ce…`.
- Selftest receipts (last commit 0ab1ccc), each with `SELFTEST_SCRIPT_SHA256: 962919ce…`:
  - core `9/9 passed` exit=0
  - compound `16/16` exit=0
  - hardening `33/33` exit=0
  - w2-regressions `30/30` exit=0
  - adversarial `4/26 passed` exit=1 (22 known misses)
- Committed case files (`git ls-tree -r`): core 10 = 9 cases + `expected.json`
  (nodata is a dir case); compound 14; hardening 34; w2-regressions 31. These
  are consistent with the tallies plus expected files.
- Independent anchor: `evidence/tripwire-anchor-r15.txt` reports exit 1,
  line 54, `call_38165`, rules `sudo` and `pacman:-S`. The closure read the
  transcript itself:
  - Input `…/MadoR15/MadoR15.LibinputEvents.jsonl`: 173 lines, sha256
    `78388d42…`, which equals `evidence/session-index.json`.
  - Line 54 is a `toolCall` `call_38165` `bash`
    `sudo pacman -S --needed --noconfirm libinput libinput-tools` at
    2026-10-20T07:25:16.905Z.
  - `/var/log/pacman.log:2429` (file read) has
    `[2026-10-20T04:25:16-0300] [PACMAN] Running 'pacman -S --needed --noconfirm libinput libinput-tools'`.
  - `:2410`, `:2422` and `:2423` are the wayland-utils / wlr-protocols
    transactions named by the join receipt; `:2416` is man-pages (reported as mori's).
- Registry: `SKILL.md:562` has row `mado-tripwire | probe | …` with the entry
  command, verdict map 0/1/2, selftest spelling `--selftest DIR` per suite,
  write scope and owner. It is registered as a probe; no frozen input snapshot
  exists yet (the round-18 plan names one).

The round demonstrates the capability running, so the capability row enters
legitimately. Verdict: **improved**.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| calibration | improved | C1 re-measured 14/22 → 15/23; criterion 23 lesson-grounded with a failing control |
| coverage | improved | rubric V hand-recount 2/6 → 4/6; 13/13 credited rows reproduce; U 7/7 unchanged (`evidence/harm-u-nav.txt` `U 7 nav 32 / 32`) |
| operability | improved | tripwire capability acquired (evidence-verified). Harm watch: `harm-legacy-selftest.txt` `MADO_SELFTEST: 372/372`, `measured_commit=f71ccbe…`; `tools/mado-verify.sh` unchanged across the round (`git diff --quiet` ok, sha256 `fba82a66…`); `harm-action-selftest.txt` 52/52 |
| freshness | unchanged | not re-measured; no lane change. The 09:15 non-lane `-Syu` moved walker 2.17.0→2.17.2 and hyprland 0.56.2-2→0.56.2-4 (`pacman.log:2929`, `:2733`). `SKILL.md:22-26` holds these as declared claim pins with a re-verify rule, not present-tense host facts, and SCORECARD round-18 plan item 3 names the re-anchor |
| depth | unchanged | unscored; no claim |
| adjacency | unchanged | `PROVINCE.md` unchanged (`git diff --stat` empty); mori's man-pages install reported, not absorbed |

No owned axis harmed. For QUALITY.md, SOURCES.md, SKILL.md, LOG.md, PROVINCE.md,
`lessons/round-16.md` and `corpus/README.md`, `git diff 27cd06f 0ab1ccc -- <f> | grep -c '^-[^-]'`
is 0 in every file. `corpus/knowledge` diff: 2 new files only (+290).

## 4. Discernment spot-check (`lessons/round-17.md` § Gate)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S066 hypridle Hypridle.cpp @ v0.1.8 | admit (tier A, mined) | https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp | agree | tag-pinned upstream code; sha256 matches the corrected digest; :473 quote verbatim; supports the P6 lock claim exactly |
| S064 hyprlock wiki | admit (tier A, mined) | https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/ | agree | digest reproduces; 24-word quote (≤25) present; "Latest git" scope stated in the row |
| S058 alacritty.5.scd @ v0.17.0 | admit (tier A, mined) | raw v0.17.0 man source | agree | tag object and commit match; :35-37 import-order quote verbatim |
| S062 linuxjunkies configure-alacritty | reject (tier C) | https://linuxjunkies.org/guides/configure-alacritty | agree | sha256 08608a0b… reproduces; it says "Starting with 0.12, Alacritty switched to TOML", but alacritty v0.13.0 `CHANGELOG.md:36` "Configuration file now uses TOML instead of YAML" (v0.12.0 CHANGELOG has no TOML switch), so the source is false |
| S061 Arch Wiki Alacritty | reject (tier C) | `index.php?title=Alacritty&action=raw` | agree | sha256 c39c563d… reproduces; :22 `/etc/alacritty/alacritty.toml` and :24 before-0.13 line present; an unpinned restatement of upstream, so it is right not to use it as sole support |
| S070 flarexes walkthrough | reject (tier C) | the flarexes URL | agree | per-fetch bytes differ (closure sha fce8f836…, as the row predicts); page text contains "You can learn more about" (wiki restatement); no hypr version pin |

Newly written row quote check: S064 :7 quote is 24 words and S056 :166 is 11 words, both ≤25.
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
printed three historical W04 lines (S030, S042, S045 duplicate urls),
`mado ok …/corpus/SOURCES.md`, exit 0. This is identical to
`evidence/census-end.txt`.

The spot-check agrees with the gate on the admit and reject samples (6/6 sampled, 13/13 admits re-opened).

## 5. Trend verdicts

- **expansion: improved.** Two admitted `knowledge/` entries landed on ground
  the coverage map did not hold (P4 Alacritty-only route, P6). Each `source:`
  cites mined rows that the closure re-opened. One capability was admitted
  (post-hoc transcript tripwire). These are documentary routes, not behaviour.
- **quality: improved.**
  - The R16-V1 erratum is appended to `lessons/round-16.md` (0 deleted lines),
    with recut tamper control `evidence/frozen-tampered-recut.json`.
  - Same-round row corrections are logged old→new.
  - Every credited row re-checks clean.
  - Freshness debt from the non-lane `-Syu` is named, not hidden (see §3).
- **discernment: improved.** The non-author spot-check agrees with the gate on
  admits and rejects (§4). The round-16 outside disagreement (R16-V1) became
  lesson M1 and the grounded QUALITY criterion 23, with a failing control.

## 6. Routed defects (lane fixes next round)

- **R17-V1 (operability/calibration).** The real-transcript scan receipts
  carry no tool sha or `measured_commit`:
  - Affected files: `evidence/tripwire-r13.txt`..`tripwire-r16.txt`,
    `tripwire-anchor-r15.txt` and `tripwire-pacmanlog-join.txt`
    (last changed f71ccbe, under tool `7a98720e…`).
  - `lessons/round-17.md:175-176` says "all real-transcript receipts re-cut
    with identical counts" under `962919ce…`. Git records no change to those
    files at 0ab1ccc, so the re-cut is unreceipted.
  - Fix: record the tool sha and measured revision in every scan receipt
    (PROTOCOL §Gate standard, "names the revision it was measured against").
- **R17-V2 (calibration, minor).** The report's before→after table
  (`.ufo/reports/round-17/mado.md:76`) cites tool sha `7a98720e…`, which is
  the f71ccbe tool. The landed tip tool is `962919ce…` (report line 3,
  SCORECARD capability row). Cite both, with labels, in the next report's carry-over.
- **R17-V3 (coverage instrument).** Rubric V still cannot tell a fetched row
  from an invented one (lane wave-2 E1). This closure re-opened all 13
  credited rows by hand. Commit raw fetch receipts (sha256 + bytes + fetch
  time) for new credited rows, as round-18 plan item 2 states.
- **R17-V4 (operability).** The tripwire is a probe with no frozen input
  snapshot. Its inputs live under `~/.omp/agent/sessions` (mutable, outside
  the repo; pinned only by `session-index.json` digests). The round-18 frozen
  replay with digest-pinned `expected.json` is needed before it can be
  registered as a gate.
- **R17-V5 (calibration).** The M3 instrument tightenings were shown to bite
  only in a seat `/tmp` lab (lane self-disclosed at `lessons/round-17.md:156-158`).
  Commit mutant receipts for `measure.py`.

Host evidence (operator-owned, not lane debt):
- `grep -n "\[PACMAN\] Running" /var/log/pacman.log` from line 2430 lists 13
  runs on 2026-10-20, 07:45:36-09:39:21 (lines 2440-3152). They include
  `pacman -Syu --needed --noconfirm …` at `:2462` (09:15:30; mkinitcpio
  41.1→42.2 at `:2539`, linux 7.2.11 at `:2855`).
- No actor is recorded.
- There are 0 lines from 10:00 onward: the log ends at line 3160, 09:39.
  This agrees with `evidence/pacmanlog-round-window.txt`
  `pacman_runs_since_10:51=0`.
- R15-V1 stays operator-owned.

Seats: `…/MadoR17/` holds 148 seat `.jsonl` transcripts (= 70 + 78).
`MadoR17.TripwireCore.jsonl` carries `resource_exhausted: Reached free model
rate limit`, so it is the one dead seat. `w1/reports` has 70 files and
`w2/reports` has 79.

SHONEN: all four boxes stay `[~]` author assertions. The closure does not
judge them fully checkable by a non-author this round: there is no round-17
end-to-end desktop task (host pause). Promotion is operator-owned.
