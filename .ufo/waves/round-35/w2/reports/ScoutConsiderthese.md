# ScoutConsiderthese — full `considerthese/` inventory, one-proposal falsification

Seat: `L1Mado35.ScoutConsiderthese` (leaf scout). Round 35, wave 2.
Lane repo: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Read-only: no `considerthese/` byte, lane corpus file, counter, control, `SOURCES.md`, jj/Git
state, sibling lane, fleet repo or `/home/vgpnk/Projects/shokuknow` path was written. Nothing was
implemented from any proposal. No tool was installed or upgraded; no `pacman` transaction was
attempted (host pause).

LSP note: no language server answers `considerthese/*.md`, `corpus/**` or `.ufo/**`, so this seat
used file reads plus literal text search, which is the correct primitive for prose inventory.
Every claim below is either a quoted byte range or a command with its exit code (appendix A).

Scratch note: `.ufo/waves/round-35/scratch/ScoutConsiderthese/evidence.log` was rebuilt from this
seat's transcript on 2026-10-25 after an external sweep removed the whole round-35 scratch tree
(~03:45). This report cites **no** round-35 scratch path, so nothing here dangles; the round-34
scratch files cited in §5 were outside the sweep and are still present.

---

## 0. Verdict

- **6 files**, `2026-10-19.md` … `2026-10-24.md`, one per day, newest last. All six carry the same
  final section heading, verbatim: `## Self-improvement suggestions (proposals only; not acted on)`.
- **41 proposals** total: 7 + 7 + 7 + 7 + 7 + 6 (appendix A1).
- Status at the round-35 tip: **9 adopted** (a later artifact performs the practice), **11 partial**,
  **20 not implemented**, **1 unverifiable from the repo**. The 41-item breakdown is §2; the
  still-unimplemented set is §3.
- **The one proposal checked against round 35's landed work:** `2026-10-20.md` #5, *"Draft a
  post-ceiling coverage rubric for João to judge … or rows from the arc gap ledger (Walker live
  rows, theme mutants, idle)"*. Verdict: **partially reflected in substance, not reflected in the
  form asked** — round 35 lands the idle *third* of the row groups, but it measures the idle-lock
  **offer**, not the ledger's named **idle/lock transitions**, and it does not deliver an
  operator-facing rubric. Ground it would need: §4.
- Round 35's own idle work does contain one genuine improvement the proposal did not ask for and
  the arc ledger has not absorbed: the ledger's reason for the idle row ("hypridle absent") is
  stale — S205 records `hypridle` live at pid 1667 on 2026-10-24 (`idle-lock-chain-armed-r14.md:20-24`).

---

## 1. File inventory

| file | date in name | git commit (author time, -0300) | worktree mtime | bytes | window it covers | proposals |
|---|---|---|---|---|---|---|
| `considerthese/2026-10-19.md` | 2026-10-19 | `8e0c9b2` 2026-10-19 10:01 | 2026-10-19 22:04 | 7032 | 2026-10-16 09:59 → 2026-10-19 09:59 BRT; housekeeping only, no round | 7 |
| `considerthese/2026-10-20.md` | 2026-10-20 | `f898e52` 2026-10-20 10:02 | 2026-10-20 10:18 | 9205 | 2026-10-17 09:59 → 2026-10-20 09:59 BRT; rounds 12–16 incl. the round-15 host incident | 7 |
| `considerthese/2026-10-21.md` | 2026-10-21 | `234f0bc` 2026-10-21 09:56 | 2026-10-21 11:18 | 9656 | 2026-10-18 09:55 → 2026-10-21 09:55 BRT; round-16 closure + rounds 17–21 | 7 |
| `considerthese/2026-10-22.md` | 2026-10-22 | `5bb2c87` 2026-10-22 10:01 | 2026-10-23 00:11 | 9060 | 2026-10-19 09:52 → 2026-10-22 09:52 BRT; rounds 22–23 | 7 |
| `considerthese/2026-10-23.md` | 2026-10-23 | `0a9ea77` 2026-10-23 09:56 | 2026-10-23 15:13 | 9303 | 2026-10-20 09:52 → 2026-10-23 09:52 BRT; rounds 24–26 + round 27 in flight | 7 |
| `considerthese/2026-10-24.md` | 2026-10-24 | `a327cd4` 10:02, followed by `57a772b` 10:03 ("time-window correction") | 2026-10-24 20:05 | 8227 | 2026-10-21 09:52 → 2026-10-24 09:52 BRT; rest of 27 + 28–31 | 6 |

Observed, not explained: every worktree mtime is later than its commit time (up to 13 h for
`2026-10-22.md`). Filename date, commit date and mtime therefore disagree; the *content* windows
quoted above are the files' own. This seat did not diff the working tree against the commits
(read-only bound on Git index; no need for the question asked).

Content shape is identical in all six: "What landed …" table → "Top 3 lessons / gains" →
"Open debt carried forward" (from 2026-10-20 on; absent in 2026-10-19) → the proposal section.
The proposal section is the only place that claims a proposal status, and its heading asserts
`proposals only; not acted on` for the whole list; no individual item carries its own
implemented/landed-at marker.

---

## 2. Every proposal, with status

Legend — **ADOPTED** = a later lane artifact performs the practice; **PARTIAL** = one component
landed, or the idea appears only as prose in the same file; **NOT** = no artifact anywhere and no
later file performs it; **UNVERIFIED** = the act, if it happened, would leave no trace in the repo.

### 2.1 `2026-10-19.md` (7)

| id | proposal (condensed) | status | evidence / nearest artifact |
|---|---|---|---|
| P19-1 | Turn the empty `## Capabilities` table into a ready demonstration list (exact command + expected receipt per row) | **PARTIAL** | Contract table is still a placeholder: `SCORECARD.md:204` = `\| — none yet — \| \| \| \|`, acknowledged by the lane itself at `SCORECARD.md:1642` ("a tenth such table, `:202`, holds only the `— none yet —` placeholder `:204`"). Per-round demonstration tables do exist (`SCORECARD.md:306`, `:435`, `:785`, `:922`). Rows enter only through a demonstrating round (`AXES.md` §Capabilities), so this cannot be closed by a doc edit alone |
| P19-2 | Declare a saturation line and stagnation window N now | **ADOPTED** | `SCORECARD.md:270-274`: "Saturation line: **9.0** on every scored sub-axis. Stagnation window: **N = 3** rounds without a capability row"; restated in every later registration (e.g. `.ufo/waves/round-35/registration.md:5-12`). Residue: the contract-level `## Saturation` at `SCORECARD.md:208-210` still says "to be declared … not asserted by this conformance change" — same annex/contract split as P19-1 |
| P19-3 | One-page unblock brief for João (fleet round 1 routing + receipt binding) | **NOT** | The machine blockers exist (`.ufo/blocked/fleet-round-1-routing.json`, `…-receipt-binding.json`, both mtime 2026-10-15) but no decision sheet: the only prose hits outside `considerthese/` are scout reports (`round-18/w1/reports/ConnConsiderThese.md`, `round-35/w1/reports/ConnOperator.md`), not a brief. `2026-10-21` #2 and `2026-10-22` #2 re-ask it |
| P19-4 | Refresh the live plane with a read-only `bash tools/mado-verify.sh` run, committed as evidence | **NOT** | Newest `.ufo/evidence/` directories are `round-12` (2026-10-19) and `fleet-round-1` (2026-10-15); the "live" hits under `.ufo/waves/**/evidence/` are file-plane and regression receipts, not a live run. The reflections themselves still say the newest live evidence is 2026-10-14 (`2026-10-19.md` §"No gain"); host pause + operator gate stand |
| P19-5 | Restore outside-lane calibration with a sibling admit/reject spot-check sample | **ADOPTED (exceeded)** | Non-author `*-verifier-spotcheck.md` exist for rounds 12–20 and 23–34 (`corpus/lessons/`, appendix A8). Effect on `SHONEN.md` is still *not* asserted: 4 × `[~]`, 0 × `[x]` (appendix A4), and the operator-owned promotion rule is unchanged |
| P19-6 | Target the named coverage gaps next (arc gap ledger: walker live rows, theme mutants, idle; 12 surfaces) | **PARTIAL** | Idle now partly covered by round 35 (§4). Walker live rows: still "not landed: hermetic barrier is structural" (`corpus/knowledge/arc-synthesis.md:311-312`). Theme mutants: no entry carries a theme-mutant claim (`grep -rliE 'theme.mutant' corpus/knowledge` → 0). The ledger (§6, `arc-synthesis.md:290`) is unchanged |
| P19-7 | Improve the daily pass (run `--selftest` via a cloud agent; PR-opened/merged listener; standing stale-PR section) | **NOT** | Every reflection through 2026-10-24 states it did not re-run anything ("I did not re-run any counter", `2026-10-24.md:5`); PR #1 is still a line in the debt table, not a standing section (`2026-10-24.md:42`); no listener artifact exists |

### 2.2 `2026-10-20.md` (7)

| id | proposal | status | evidence |
|---|---|---|---|
| P20-1 | Lead every reflection with a host-safety tripwire scan (`sudo`, `pacman`, `systemctl`, `hyprctl dispatch`/`keyword`, `pkill`), hits first | **PARTIAL** | Host safety now appears every day inside the bottom line or debt table (`2026-10-23.md`: coredump note; `2026-10-24.md:5`: "Host safety held: Hyprland coredumps stayed at 1338 on every oracle receipt"), but no file opens with a scan block and `2026-10-21`/`2026-10-22` still lead with other news |
| P20-2 | Keep a running open-debt table (R15 remediation, round-16 admission, PR #1, SHONEN `[~]`) | **ADOPTED** | `## Open debt carried forward` in all of `2026-10-21` … `2026-10-24` |
| P20-3 | Keep a metrics trend line (sources, selftest, U-coverage, calibration, navigation, gate digest) | **NOT** | No table in any file; `2026-10-21` #4 re-asks it. `grep -rlE 'trend line\|run reliability\|per-round digest\|carried list' corpus/` → 0 files |
| P20-4 | Read the verifier's verdict, not just the author's; flag rounds with no `*-verifier-spotcheck.md` | **ADOPTED** | `2026-10-21` flags round 21's missing closure and puts it in the debt table; `2026-10-22`/`2026-10-23`/`2026-10-24` cite the hyaku closures by file. (The "flag every missing one daily" half is not sustained — see P22-5) |
| P20-5 | Draft a post-ceiling coverage rubric for João to judge, e.g. observed-behaviour confirmations or rows from the arc gap ledger (Walker live rows, theme mutants, idle) | **NOT in the form asked; PARTIAL in substance** | §4 (the one deep check) |
| P20-6 | Reproduce one hermetic receipt per day, sandboxed, no host operations | **NOT** | Re-asked at `2026-10-21` #7 and `2026-10-22` #7; `2026-10-23`/`2026-10-24` still say no counter was re-run |
| P20-7 | Build a tiny machine-readable per-round digest (claims, verdicts, incidents, receipts) | **NOT** | No digest artifact: only per-seat `digest` receipts under `.ufo/waves/**/` (e.g. `round-22/…/digests-before.txt`), not a per-round digest. Corpus grep for "per-round digest" → 0 |

### 2.3 `2026-10-21.md` (7)

| id | proposal | status | evidence |
|---|---|---|---|
| P21-1 | Flag loops, not just incidents (consecutive rounds on one artifact, alternating verdicts) | **ADOPTED** | `2026-10-22.md:5`: "the tripwire repair loop is still not converging … Round 23 … first closure in five rounds"; `2026-10-23.md:5` narrates the pivot off the loop |
| P21-2 | Give João a hold/unblock brief (one-page read-only option sheet) | **NOT** | Options are argued inside `2026-10-22` #2, never delivered as an artifact (appendix A7) |
| P21-3 | Propose a post-ceiling rubric concretely (observed behaviour on the Omarchy host, or depth/adjacency) | **NOT** | Same gap as P20-5; no rubric document exists in `corpus/` (only a lesson mention, `corpus/lessons/round-17.md`) |
| P21-4 | Keep a metrics trend line across files | **NOT** | Duplicate of P20-3; no table appears |
| P21-5 | Prefer the verifier's verdict and flag missing ones until they land | **PARTIAL** | Citation practice adopted (P20-4), but rounds 21 and 22 have no `-verifier-spotcheck.md` (A8) and neither `2026-10-23` nor `2026-10-24` mentions them |
| P21-6 | Scale reading to volume (lesson files + verifier spot-checks, not just LOG) | **PARTIAL** | `2026-10-23` cites `corpus/lessons/round-25.md`; `2026-10-24` cites `round-{27..31}-verifier-spotcheck.md`. No evidence the full tree is read; both files still describe sampling |
| P21-7 | Reproduce one hermetic receipt per day | **NOT** | Duplicate of P20-6 |

### 2.4 `2026-10-22.md` (7)

| id | proposal | status | evidence |
|---|---|---|---|
| P22-1 | Track the repair loop as a single metric ("rounds on the same artifact / admitted") | **PARTIAL** | `2026-10-23` #2 re-proposes it and `2026-10-24` narrates the streak in prose ("four rounds of self-audit after one capability round"), but no standing line or file records the metric |
| P22-2 | Draft the post-block option sheet for João | **NOT** | Same artifact gap as P19-3 / P21-2 |
| P22-3 | Separate "harmed" from "honest stop" and grade by the verifier's axis table | **ADOPTED** | `2026-10-23.md`: round 23 = `rejected-honest-stop` with "no axis harmed"; `2026-10-24.md` uses the same two-way grading for rounds 28 and 31 |
| P22-4 | Surface host-relevant facts the lane finds, separately from capability news | **ADOPTED** | `2026-10-23.md`: "Worth João knowing the count jumped this morning"; `2026-10-24.md` host-safety sentence. Stays inside the bottom line, not a separate block (see P20-1) |
| P22-5 | List every round lacking a non-author closure each day | **NOT** | Rounds 21 and 22 have no spot-check file (A8); no reflection lists them. Verifier citation is the norm (P20-4), the missing-closure ledger is absent |
| P22-6 | Read lesson files, not only LOG | **ADOPTED** | `2026-10-23` quotes `corpus/lessons/round-25.md`; `2026-10-24` reads `round-27…31` lessons and spot-checks and quotes M28-1 |
| P22-7 | Reproduce one hermetic receipt per day | **NOT** | Duplicate of P20-6 |

### 2.5 `2026-10-23.md` (7)

| id | proposal | status | evidence |
|---|---|---|---|
| P23-1 | Flag host-impact events to João the same day, at the top of the message | **PARTIAL** | `2026-10-24.md` reports host safety in one sentence inside the bottom line; no top block, and it reports a *negative* (coredumps unchanged), not an event |
| P23-2 | Track admission streaks and pivots ("rounds since last admission / artifact being worked") as a running line | **PARTIAL** | `2026-10-24`'s bottom line is a streak/pivot statement ("one real desktop capability landed … then the lane spent rounds 28–31 hardening its own counters") and its debt table carries "No `tools/` or `corpus/knowledge/` change since round 27" — running prose, not a standing metric line. `round-32/w1/reports/ScoutConsiderThese.md` calls this **IMPLEMENTED**; `round-34/scratch/ScoutConsiderB/list.md` calls the same item **not covered**. Two lane artifacts disagree; this seat takes the narrower reading and records both |
| P23-3 | Cross-check one landed tool against a public pin, read-only, one cited line per day (e.g. S177) | **NOT** | No reflection reports opening a cited line. `2026-10-24` #5 re-proposes the same act. Lane-side only: `corpus/lessons/round-33.md:28-30` records a seat opening S190's bytes, which is the lane, not the reflection loop |
| P23-4 | Watch "trade" rulings and their follow-through (M26-10 et al.) | **ADOPTED** | `2026-10-24` #3: "Yesterday I flagged M26-10; today I could confirm it landed at `b6650d5`" |
| P23-5 | Read in-progress rounds at the registration level, compare outcome against intent | **UNVERIFIED** | `2026-10-24` reports registration-level facts (round 28's C1 guard pinned the wrong `count-v4.py` hash) but cites no `registration.md`, and the same facts are in the spot-check; cannot tell which was read |
| P23-6 | Handle commit-list caps explicitly (page fully or note the cap) | **PARTIAL** | `2026-10-24.md:3` gives an exact count ("the 42 commits after `0a9ea77` …") with no statement about paging or a cap; a cap would make the count a lower bound, which is not flagged |
| P23-7 | Offer operator-actionable summaries (e.g. a read-only "what your config resolves to" note) | **NOT** | No operator-facing summary exists; `round-35/w1/reports/ConnOperator.md` confirms there is no `operator-*.md` corpus. Round 35's entries carry the operator *question* (`idle-lock-never-asked-r12.md:31` UNK) but are coverage entries, not a summary written for the operator |

### 2.6 `2026-10-24.md` (6)

| id | proposal | status | evidence |
|---|---|---|---|
| P24-1 | Report a domain-versus-meta ratio per window; flag ≥2 rounds without a desktop-facing change | **NOT** | `grep -rlE 'trend line\|run reliability\|per-round digest\|carried list' corpus/` → 0; nothing records a ratio. Round 35 *is* a domain round (three `corpus/knowledge/` entries), which is the condition the ratio was meant to make visible, and no artifact counts it |
| P24-2 | Report run reliability (dead attempts, OOM, 429s) as its own line | **NOT** | Zero corpus artifacts (A9); incidents live only in lessons (`round-20.md` M14, `round-19.md` M9) and in `2026-10-24`'s table narrative for round 28 |
| P24-3 | Keep a short carried list of routed items, checked off by commit | **PARTIAL** | The file performs one check-off in place (M26-10 → `b6650d5`) but keeps no persistent list; `2026-10-24`'s own debt table names n2 / Holds semantics / undispatched waves without commit links |
| P24-4 | Read `PROVINCE.md` and propose the next Hyprland table (window rules, monitors, layer rules) with grounding sources | **NOT** | No proposal exists in `corpus/` (`grep -rlE 'next (desktop )?(table\|surface\|plane)' corpus/` → 0 files); round 35 chose the idle-lock surface, which is none of the three named, and neither its registration nor the entries propose a successor |
| P24-5 | Verify one cited fact first-hand per day, read-only | **PARTIAL** | Lane-side instance: `corpus/lessons/round-33.md:28-30` records opening S190's fetched bytes. Round 35 wave 2 is doing the same at scale: `w2/reports/RevQuoteS203.md`, `RevQuoteS205.md`, `RevQuoteS206.md`, `RevQuoteS208.md`, `RevQuoteS209.md` exist at read time (03:31–03:32). No *reflection* file reports a first-hand check, and the file that proposes it is the newest. **Conflict with an existing lane artifact:** `round-34/scratch/ConnConsiderLatest/table.md` marks this "implemented", while `round-34/scratch/ScoutConsiderA/list.md` marks all six "NOT implemented" — see §5 |
| P24-6 | Note the window's time-of-day pattern (round timing vs host load/coredumps) | **NOT** | The pattern is stated once inside `2026-10-24`'s own proposal sentence; no later file exists and none records timing as a section |

---

## 3. What is still unimplemented (the 20)

These are the items with status **NOT** at the round-35 tip, i.e. the proposals the operator's own
section heading calls "not acted on" and for which this sweep found no performing artifact:

- **2026-10-19**: #3 unblock brief · #4 live-plane refresh · #7 daily-pass infrastructure
  (cloud `--selftest`, PR listener, stale-PR section).
- **2026-10-20**: #3 metrics trend line · #5 post-ceiling rubric for João (deep check, §4) ·
  #6 daily hermetic receipt · #7 per-round machine-readable digest.
- **2026-10-21**: #2 hold/unblock brief · #3 post-ceiling rubric · #4 metrics trend line ·
  #7 daily hermetic receipt.
- **2026-10-22**: #2 post-block option sheet · #5 missing-non-author-closure list ·
  #7 daily hermetic receipt.
- **2026-10-23**: #3 daily public-pin cross-check · #7 operator-actionable summary.
- **2026-10-24**: #1 domain-vs-meta ratio · #2 run-reliability line ·
  #4 next-desktop-table proposal · #6 time-of-day pattern.

Structurally, three asks recur and none has an artifact: a **brief/decision sheet for João**
(P19-3, P21-2, P22-2), a **metrics/reliability line** (P20-3, P21-4, P22-1, P24-1, P24-2), and a
**fresh hermetic/live receipt** (P19-4, P20-6, P21-7, P22-7, P23-3, P24-5). The first two are
pure text and need no host access; the third is operator-gated (host pause) except the hermetic
`--selftest` form, which is sandboxed by construction.

---

## 4. The one proposal checked against round 35's landed work — `2026-10-20.md` #5

Verbatim (`considerthese/2026-10-20.md:54`):

> **Draft a post-ceiling coverage rubric for João to judge.** For example, "observed-behaviour
> confirmations of U1–U7 on the Omarchy host, read-only, operator-cleared", or rows from the arc
> gap ledger (Walker live rows, theme mutants, idle). Clearly labelled as a draft for the next
> round to adopt or reject.

It asks for two things: **(a)** a rubric draft submitted to the operator for judgement, and
**(b)** rows from the arc gap ledger, three groups named (Walker live, theme mutants, idle).

### Prior lane artifact on this same proposal (must not be re-derived as new)

`round-17/w2/reports/ConnectConsiderThese.md:134-198` tests this exact proposal clause by clause
and returns **"acted, shape-changed"**: rubric V matches the structure, the fixed baseline and the
surface taxonomy, but not the evidence class and not the judge.

- Its decisive finding, quoted: "V cannot admit suggestion 5's primary example … An observed
  confirmation on the host has no upstream https row … A hypothetical observation entry is rejected
  by construction", and "V is not a *successor* to suggestion 5's rubric; it is a different rubric
  over the same surfaces."
- And on authority: "Suggestion 5 says 'for João to judge … a draft for the next round to adopt or
  reject.' V was adopted inside L1's own pre-registration (`0175f13`) with no operator row … it
  should not be reported as 'João's post-ceiling rubric landed.'"

Round 35 changes neither half. Its eight rows S203–S210 carry origin **`own-work`** and point at
host paths or `.ufo/waves/round-35/fetch/*.receipt.txt` (`corpus/SOURCES.md`, S203–S210 cells read
in this seat), so they cannot enter rubric V's `mined` upstream-`https` condition; and no operator
row exists anywhere. `[INFERENCE]` on the "cannot enter V" step: it follows from the row cells plus
the round-17 account of `measure.py`; this seat did not run `measure.py`.

### (a) Rubric draft — not reflected

- No operator-facing rubric exists. `grep -rlE "post-ceiling" corpus/` → 1 file,
  `corpus/lessons/round-17.md` (a lesson), count = 1 (appendix A6).
- The only rubric on the coverage axis is **rubric V** (P1–P6), a *lane scoring* rubric in
  `SCORECARD.md:842-852` ("C2 coverage — new declared rubric V (post-ceiling; U stays 7/7)"), with
  P6 = idle/lock. It was declared in round 17, i.e. the round immediately *after* the window this
  proposal was written from, which is exactly why round 17's connector had to adjudicate it. It is
  a scoring device for the lane's axis, not a coverage rubric handed to the operator to accept or
  reject, and the round-17 connector already recorded that divergence.
- Round 35 does not draft one either. Its C1 predicate `PRED-C1-r35-v1`
  (`.ufo/waves/round-35/registration.md` §C1) is a frozen pass/fail counter over three entries and
  eight rows — a different object, and not addressed to the operator.

### (b) Arc gap ledger rows — one third, and not the named unknown

Round 35's C1 lands three entries and eight rows about the idle-lock **offer**: the bar module
(S206), the indicator script (S207), the menu entry (S208), the copy history (S209), the toggle
directory (S210), the setup path (S203) and its negative (S204). Landing state at read time: the
three entries first landed in commit `02088b4` ("round-35: the idle-lock control surface lands —
three entries, eight rows S203-S210, errata, and the wave-1 evidence"), and all three carried
**uncommitted wave-2 errata** (`git status --porcelain` → ` M` on each; the `offered-in-the-bar`
entry now has an "Errata (round 35, wave 2)" block from `RevQuoteS209`). That is the "idle" group
of the sentence — so the proposal *is reflected in substance* for one of its three groups.

But the ledger's idle row is a different claim:

- `corpus/knowledge/arc-synthesis.md:298` — `| idle/lock transitions | no read surface; hypridle
  absent; idle-lock plane note keeps them UNKNOWN by constraint (r4) |`
- Round 35 explicitly does **not** measure transitions:
  `idle-lock-chain-armed-r14.md:36` — "**UNK** No lock, screensaver or suspend transition was
  triggered or observed. The chain is armed; whether it fires … stay unknown."
- The other two groups are untouched: Walker live rows remain "not landed: hermetic barrier is
  structural" (`arc-synthesis.md:311-312`); no theme-mutant entry exists (A10 → 0 files).

So the round advances the *idle surface* but does not close the ledger's named idle unknown, and
the ledger itself is not updated. The round's registration does not cite the ledger at all:
`grep -nE "arc-synthesis|gap ledger" .ufo/waves/round-35/registration.md` → no match, **exit 1**
(appendix A2). The linkage is therefore reconstructive, not recorded — a later reader cannot tell
from the round whether it was targeting the ledger or had chosen the surface independently.

One real advance the ledger has not absorbed: the ledger's reason clause "hypridle absent" is
stale. S205 measures the daemon live (pid 1667, journal start 2026-10-23 22:14:11) and explains
why the unit probe disagrees (`systemctl --user is-active` → `inactive` because the daemon runs in
a transient scope) — `idle-lock-chain-armed-r14.md:20-33`. That is a ledger *reason* correction
waiting for a carrier, and it is exactly the kind of finding the proposal's "rows from the arc gap
ledger" form was meant to collect.

### What ground the proposal would need

0. **What the round's own groundability scan already settled** (`round-35/w1/reports/CritConsider.md`,
   independent of this seat): the "observed-behaviour rubric" branch has **no frozen denominator**,
   window rules have **no table oracle** on 0.56.2 (`hyprctl windowrules` → `unknown request`,
   re-read first-hand by that seat), and layer rules are the same missing-oracle class
   (`hyprctl layers -j` reports live surfaces, not the `layerrule =` table). The one named surface
   that would pass the M25-1 oracle test is **monitors** (`hyprctl monitors -j`, read verb already in
   the PROVINCE row, resolver shape identical to the three admitted ones). So the proposal's
   "or rows from the arc gap ledger" branch is *harder* than it reads, and the idle branch round 35
   took is the only one that can be moved without an oracle.
1. **The rubric draft itself (pure text, no host access) is producible but not a claim.** A one-page
   declared rubric with surface, denominator, read-only/operator-cleared constraint and the accept
   or reject line the operator signs. `SCORECARD.md:842-852` (rubric V) and the `registration.md`
   predicates give the shape; what it cannot do is score an axis by existing, which is why a
   reflection proposal alone cannot land it. Landing it needs a round-authored declaration plus a
   SCORECARD/LOG pointer, and, per CritConsider, a denominator over a surface that has an oracle.
2. **Idle group.** Needs a transitive observation of the chain firing (or a declaration that it
   stays `[UNK]` by constraint). Round 35 shows the blocking condition: no lock/screensaver/suspend
   may be triggered by this lane, so the only admissible evidence is a journal/event record of a
   firing the operator caused — operator-gated.
3. **Walker live rows.** Needs the hermetic barrier relaxed for four rows: `--root` roots `$HOME`
   while `$XDG_RUNTIME_DIR` and the session bus sit outside it (`arc-synthesis.md:311-312`). That
   is a harness change, not a note.
4. **Theme mutants.** No lane artifact addresses the gap; it needs a declared population and a
   producing claim first (the arc's "theme-mutant gap C4" is still named as open).
5. **Ledger hygiene.** Whoever lands the next idle claim should also correct
   `arc-synthesis.md:298`'s "hypridle absent" reason, or record why it is left as a dated sample.

---

## 5. Cross-check against existing lane artifacts (disagreements named, not resolved silently)

- `round-18/w1/reports/ConnConsiderThese.md` scored `2026-10-19`'s proposals: #1 partial, #2
  acted, #3 open, #4 open, #5 acted/exceeded. This sweep reaches the same five verdicts
  independently, which is a useful consistency check on the 2026-10-19 column.
- **`round-34/scratch/ConnConsiderLatest/table.md` and `round-34/scratch/ScoutConsiderA/list.md`
  contradict each other on `2026-10-24` #5.** `ConnConsiderLatest` marks it "implemented", using a
  declared definition ("a proposal counts as implemented when the lane mined it into the corpus");
  `ScoutConsiderA` marks all six "NOT implemented". Both are defensible under their own definition;
  neither states that the definition is the disputed part. This seat's position: the proposal's
  own sentence is about the *reflection's* daily practice ("Verify one cited fact first-hand per
  day, read-only"), so a lane seat opening S190 does not satisfy it; the round-35 wave-2 quote
  seats are the same lane-side act at scale. Marked **PARTIAL**, with both readings cited, and the
  definitional gap flagged so the next reader does not inherit a silent "implemented".
- **Prior sweeps exist, but no six-file inventory.** What the lane already holds: `round-17/w1/reports/ConsiderTheseJoin.md` + `round-17/w2/reports/ConnectConsiderThese.md` (all seven of `2026-10-20`, with a verdict table); `round-18/w1/reports/ConnConsiderThese.md` (all seven of `2026-10-19`); `round-32/w1/reports/ScoutConsiderThese.md` (all seven of `2026-10-23`, with a recommendation and an executed first-hand S177 re-open); `round-33/w1/reports/ScoutConsider.md` (item 5 of `2026-10-24` only); `round-34/scratch/ScoutConsiderA/`, `ScoutConsiderB/`, `ConnConsiderLatest/` (all six of `2026-10-24`, twice, plus `2026-10-23` again in B); `round-35/w1/reports/ScoutConsider.md` (all six of `2026-10-24`). **`2026-10-21` and `2026-10-22` have no item-level inventory in any lane artifact I found** — those two columns are new here, as is the single cross-file table.
- **The prior sweeps contradict each other on two items, and the contradiction is unresolved.** `2026-10-23` #2 (admission-streak line): `round-32` says IMPLEMENTED, `round-34 ScoutConsiderB` says not covered. `2026-10-24` #5 (first-hand cited fact): `round-34 ConnConsiderLatest` says implemented, `round-34 ScoutConsiderA` says NOT implemented, and `round-33 ScoutConsider` argues the S190 open does not satisfy it because "S190 is cited nowhere in the file". This seat's PARTIAL verdicts sit inside those ranges by construction, with the definition stated; the lane should not treat any of the three as settled.
- **On `2026-10-24` #5 specifically, the round-33 seat is right and its argument is checkable**: `2026-10-24` cites S178–S182 and S183–S185, not S190 (`grep -n "S190" considerthese/2026-10-24.md` → no match), so opening S190's bytes cannot ground a claim of that reflection. Round 35's wave-2 quote seats are the correct target shape but verify registry rows S203–S210, not a reflection claim — a third distinct act.
- **`round-35/w1/reports/CritConsider.md` premise is not supported by this inventory.** It states the
  five earlier files' proposals are "already dispositioned … or superseded"; this sweep finds **20
  still unimplemented across all six files**, including ten in `2026-10-19`–`2026-10-22` (briefs,
  metrics/reliability lines, hermetic receipts, live-plane refresh). Its substantive findings on
  groundability (no table oracle for window/layer rules; monitors is the live one) are independent
  of that premise and stand.
- `round-35/w1/reports/ConnOperator.md` scores operator *teachings* against QUALITY/SKILL. This
  report scores the *proposals* against artifacts; the two touch at P20-1/P23-1 (host-safety
  surfacing) and at the "domain-vs-meta ratio" item, which ConnOperator also lists as an
  operator-side watch item with no lane rule requiring it. No contradiction.

---

## 6. Residual gaps in this seat's own evidence

- Statuses for the reflection loop's **private practice** (whether the operator's agent actually
  re-verified a pin, paged a capped commit list, or read a registration) are unobservable from the
  lane. Those are marked UNVERIFIED or PARTIAL, never "passing".
- The `.ufo/evidence/` recency test for P19-4 relies on directory mtimes plus the reflections' own
  statements; this seat did not open every receipt under `.ufo/waves/**/evidence/`. A live receipt
  newer than 2026-10-14 hidden under a round directory would overturn P19-4's status.
- No LSP server answers these files, so semantic reference tracing was not available; the
  inventory is literal-text based (recorded here rather than presented as semantic proof).
- "Adopted" is judged from later *artifacts*. If the reflection loop adopted a practice without
  recording it, this report will understate it — deliberately.

---

## Appendix A — commands and exit codes

Run in `/home/vgpnk/Projects/shokunin/mado-shokunin`. All read-only. Exit 0 unless stated.

| # | command | result |
|---|---|---|
| A0 | `stat -c '%n %y %s' considerthese/*.md` | six files, mtimes/sizes as in §1 |
| A1 | `for f in considerthese/*.md; do printf '%s %s\n' "$f" "$(grep -cE '^[0-9]+\. \*\*' "$f")"; done` | 7,7,7,7,7,6 = 41 |
| A2 | `grep -nE "arc-synthesis\|gap ledger" .ufo/waves/round-35/registration.md` | no match, **exit=1** |
| A3 | `grep -n "Saturation line: \*\*9.0\*\*" SCORECARD.md` | `272:` hit, exit=0 |
| A4 | `grep -c '^\- \[~\]' SHONEN.md; grep -c '^\- \[x\]' SHONEN.md` | 4 ; 0 |
| A5 | `grep -n -- "— none yet —" SCORECARD.md` | `204:` and `1642:` (the second acknowledges the placeholder) |
| A6 | `grep -rlE "post-ceiling" corpus/ \| wc -l` | 1 (`corpus/lessons/round-17.md`) |
| A7 | `grep -rlE "unblock brief\|decision sheet\|option sheet" --include=*.md . \| grep -v considerthese \| grep -v scratch \| grep -v fixtures \| grep -v clone` | two lane seat reports only (`round-18/w1/reports/ConnConsiderThese.md`, `round-35/w1/reports/ConnOperator.md`); no brief |
| A8 | `ls corpus/lessons/*-verifier-spotcheck.md \| sed 's/.*round-\([0-9]*\)-verifier.*/\1/' \| sort -n` | 12–20, 23–34; **21 and 22 absent** |
| A9 | `grep -rlE "trend line\|run reliability\|per-round digest\|carried list" corpus/ \| wc -l` | 0 |
| A10 | `grep -rliE "theme.mutant" corpus/knowledge` | no output, exit 1 |
| A11 | `grep -rlE "next (desktop )?(table\|surface\|plane)" corpus/` | no output, exit 1 |
| A12 | `grep -n "proposal 5" corpus/lessons/round-33.md` | `28:` hit — the lane-side S190 first-hand check |
| A13 | `ls -lt .ufo/evidence/ \| head -4` | newest dirs `round-12`, `fleet-round-1`; no live receipt after 2026-10-14 |
| A14 | `grep -n "UNK" corpus/knowledge/idle-lock-*.md` | chain entry `:36` transitions unobserved; both other entries carry the operator-preference UNK |
| A15 | `grep -nE "arc-synthesis\|gap ledger"` (repeat on `c1/frozen.json`) | no match |
| A16 | `ls -l .ufo/blocked/` | two JSON blockers, both 2026-10-15; no brief |
| A17 | `git log --format='%h %ad %s' --date=iso -- considerthese` | `57a772b`, `a327cd4`, `0a9ea77`, `5bb2c87`, `234f0bc`, `f898e52`, `8e0c9b2` |
| A18 | `ls -la .ufo/waves/round-35/w2/reports/` | `RevQuoteS203/S205/S206/S208/S209.md`, `MutC2Real.md`, `RevCollision.md` present at 03:31–03:32 |

No installs, no upgrades, no package transactions: nothing to record under the tooling directive.
