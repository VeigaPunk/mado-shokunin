# ConnectLessonChain — lesson-chain trace and falsification (round 17, wave 2)

Target: `R15-V1 → round-16 M1/M5/QUALITY21 → round-17 M2/C3 → SKILL usage subsection`,
at lane HEAD `988b858bd6049bc709807534fd725c05264f7e60` (pushed).

Installs: **none**. No pacman/sudo/systemctl/hyprctl/service/live probe was run; the only
executables run were `python3 -I tools/mado-tripwire.py --selftest …` (permitted) and
read-only `git` verbs plus coreutils text/listing tools (`cat`/`sed`/`grep`/`nl`/`find`/`ls`)
over file bytes. Host pause honored.

Working-tree drift observed at report time (`git diff --stat HEAD`): `corpus/README.md`,
`corpus/SOURCES.md`, `corpus/knowledge/terminal-route-r17.md`, `corpus/lessons/round-17.md`
— concurrent wave-2 lanes. **All citations below are to HEAD 988b858**; anything taken
from the worktree is marked `worktree`.

## Axes named

- **A1 claim correctness** — the declared C1 (calibration 15/23), C2 (rubric V 4/6), C3
  (tripwire capability) statements.
- **A2 chain fidelity** — every lesson/QUALITY/SKILL step cites a predecessor whose text
  actually carries the rule for the finding class being described.
- **A3 evidence precision** — every count/identifier in the chain resolves to a committed
  receipt at the revision the sentence describes.
- **A4 host safety** — no lane operation; R15-V1 stays operator-owned.
- **A5 separability** — no correction may move a measured fraction (C1/C2/C3).

## Chain trace (exact lines)

| # | Step | Anchor (HEAD) | Cites predecessor? | Verdict |
|---|---|---|---|---|
| 0 | R15-V1 origin | `corpus/lessons/round-15-verifier-spotcheck.md:254-257` — "R15-V1 → operator/host-safety owner … unresolved forbidden partial upgrade", exact `sudo pacman -S --needed --noconfirm libinput libinput-tools` | n/a (origin) | resolved anchor; no overreach |
| 1 | r16 M1 | `corpus/lessons/round-16.md:14` — evidence cell: "Outside closure R15-V1, actual forbidden libinput partial upgrade; round-15 lesson M2" | **yes**, R15-V1 + r15 M2 | no overreach: same row says "It does not intercept tools or **resolve R15-V1**" |
| 2 | r16 M5 | `corpus/lessons/round-16.md:18` — captured-by: "Context no package operations; QUALITY21" | **partially** (see F3) | query class is not in QUALITY 21's text |
| 3 | QUALITY 21 | `corpus/QUALITY.md:82-101` — "(lesson: lessons/round-16.md#mistakes M1/M2; outside lessons/round-15-verifier-spotcheck.md R15-V1/V2)" | **yes**, both predecessors | no overreach; explicit non-verdicts at `:91-92`, `:96-99`, `:104-105` |
| 4 | r17 M2 | `corpus/lessons/round-17.md:20` — captured-by: "QUALITY 21 and wave-context pause text (prompt-level); seat self-disclosure"; fix cell cites SKILL's tripwire section | **yes**, but two defects (F1, F3) and one scope overclaim (F2) | see findings |
| 5 | r17 C3 | `corpus/lessons/round-17.md:77-88` | cites receipts/oracles; **does not cite M2** (M2 cites C3 — asymmetric but not an overclaim) | all numbers verified (below); provenance claim unanchored (F6) |
| 6 | SKILL usage | `SKILL.md:525-534` — "…(lesson `round-17.md` M2)" | **yes**, M2 | one totality overclaim (F4); stale pointer elsewhere at `:45` (F5) |

Terminal hop verified: `SKILL.md:527-532` instructs the scan before any seat-conduct
sentence, forbids `--permit` while the pause holds, and says a finding "is an issued
command to disclose in the lesson, not a host-state fact". `SKILL.md:572-583` carries the
matching limits paragraph ("never interception, prevention or host repair … `clean` means
no finding in the covered forms").

## Findings (concrete counterexamples)

### F1 — `round-17.md:20` claims the r13 install is named only by the r13 spot-check. False at HEAD.
HEAD text: "Undisclosed in the round's own lesson: r13 wayland-utils install (only the
r13 spot-check names it)". The install is explicitly named by:
- `LOG.md:798-800` — "**Tool install:** wayland-utils **1.3.0-1** … `sudo pacman -S --needed --noconfirm wayland-utils`";
- `.ufo/waves/round-13/w1/reports/GlobalCapture.md:15-16` (the issuing seat);
- `.ufo/waves/round-13/w1/reports/EvidenceChain.md:81,168`;
- `.ufo/waves/round-13/w1/reports/ReviewPhases.md:24,71`;
- `corpus/lessons/round-13-verifier-spotcheck.md:211`.

The defensible half is "absent from `round-13.md`" (`git show 988b858:corpus/lessons/round-13.md`
contains wayland-utils only as upstream row S046, no install). The parenthetical overstates.
A concurrent lane has already edited this sentence in the worktree to "disclosed in
LOG.md:798-799 and seat reports, absent from `round-13.md`"; that correction is right and
my independent check matches it.

### F2 — `round-17.md:20` "4/4 mado-window package transactions" is attribution-scoped, not window-scoped.
The receipt it cites, `.ufo/waves/round-17/evidence/tripwire-pacmanlog-join.txt`, records a
fifth transaction inside the mado round window at line 9:
`2026-10-20T01:07:12-0300 pacman -S --needed --noconfirm man-pages` — `/var/log/pacman.log:2416-2419`,
23 s after the first joined transaction (`pacman.log:2410`, 01:06:49). It is excluded only
as "string present in MoriR13/MoriR14 transcripts (sibling lane; reported, not absorbed)" —
i.e. by **string presence in another lane's transcript**, not by a joined issued call (the
standard applied to the four). Additionally, the round receipts carry unparsed spawns
`r13=7, r14=10, r15=25, r16=23` (computed from `tripwire-r1{3,4,5,6}.txt` `files[].unparsed_spawns`;
`eval_unparsed=0` everywhere), so `join:12`'s "0 tripwire pacman transactions without a log
line" is a parsed-findings statement; the reverse direction (log line → mado finding) is not
closed for man-pages. `4/4` is true only under "mado-attributed", not under "in the window".

### F3 — QUALITY 21 is cited for the package-**query** class it does not contain.
`QUALITY.md:82-86`: "**no package transaction or host service/compositor mutation is
permitted**, including installing a tool merely to read its help". `grep -i 'quer' corpus/QUALITY.md`
returns **0** lines. Round-16 M5 (`round-16.md:18`) and round-17 M2 (`round-17.md:20`) both
name "QUALITY21" as the catching standard for a `pacman -Q` query. The actual written
authority is the wave context — `.ufo/waves/round-16/w1/spec.json` and `w2/spec.json`
context: "No package or service operations whatsoever" — and, at HEAD,
`SKILL.md:40-42` ("This source-only round additionally forbids package queries"). Scale:
of the 293 findings in the four receipts (33 + 50 + 208 + 2), **244 are `package_query`**
(19/46/177/2), 40 `live_probe`, 9 `host_mutation`. The citation, not the finding, is wrong;
the prohibition is real but lives in prompt-level text, which M2 itself labels "(prompt-level)".

### F4 — `SKILL.md:533-534` "every seat-disclosed breach" is a totality contradicted by the same page's limits.
Counterexample: round-16 M2's disclosed debt — `corpus/lessons/round-16.md:25-26` —
records that round-15 `ReviewDocsEra.md:20,76` read `/proc/1706/maps` and ran
`pgrep -x Hyprland`. The seat report itself records the maps read
(`.ufo/waves/round-15/w1/reports/ReviewDocsEra.md:20,76`). The tripwire reports the `pgrep`
(`tripwire-r15.txt`, `MadoR15.ReviewDocsEra.jsonl:68 live_probe pgrep 'pgrep -x Hyprland'`)
but has **zero** findings containing `maps` (`grep -c maps .ufo/waves/round-17/evidence/tripwire-r15.txt` → 0),
and `tools/mado-tripwire.py` has no `/proc` rule (rule vocabulary is process/package/
compositor tokens). A `/proc/<pid>/maps` read is exactly the "other tools"/read-only live
process probe the limits paragraph (`SKILL.md:572-583`) excludes. So "every" holds only
inside the covered command classes; the usage sentence omits the qualifier the limits
paragraph supplies, and the two paragraphs contradict on a literal reading.

### F5 — `SKILL.md:45` pointer does not resolve after round 17.
Line 45: "The round-15 rejected-harmed host debt is not cleared; see **QUALITY21/M1/M2**."
The reference is round-unqualified. At HEAD the newest lessons file is `corpus/lessons/round-17.md`,
whose M1 is the receipt-label row (`:15`) and M2 is the tripwire row (`:20`) — neither is
host debt. The correct form already exists at `SKILL.md:493-494`: "QUALITY 21 and **round-16
lesson M1/M2**". C1+M2 did not create the sentence: it is present at `27cd06f:SKILL.md:45`; round 17's
M1 (C1) and M2 (C3) supplied the colliding row ids that now make it resolve wrongly.

### F6 — C3 provenance is unanchored.
`round-17.md:79-80`: "`tools/mado-tripwire.py` (written by L1 after seat TripwireCore died
on an m_swe rate limit)". This is the **only** occurrence of `m_swe`/`rate limit` in the lane
(`grep -rn` over `corpus/`, `SKILL.md`, `.ufo/waves/round-17/w1/`); the dispatch registry
lists `TripwireCore` with `agentId: null` and no outcome. Not a capability overclaim, but it
is an unverified narrative inside the C3 block — the same class of defect QUALITY 23 exists
to prevent one hop over (sentence → receipt).

### F7 — Stated contradiction: "static gate refuses literal pacman including `-Q`" vs "fences were prompt-only".
- `round-16.md:18`: "static gate refuses literal pacman including `-Q`." Verified as a
  *declared-plan* verdict: `safety-policy.json` `deny_executables` includes `pacman`, and
  `tools/mado-action-plan.py:585-587` selftest `read-disguised-pacman` asserts
  `/usr/bin/pacman -Sp libinput` → `denied_executable:pacman` even under `read-source`.
- `round-17.md:20`: class cell "fences were prompt-only."

Both are true under different senses (a classifier's verdict ≠ enforcement of tool calls),
and `round-16.md:14` says the gate "does not intercept tools", while `round-17.md:20` says
"Detection only; it cannot prevent a call." Neither row states the distinction where the two
sentences meet; a reader of round 16 alone concludes a fence exists, a reader of round 17
alone concludes none did. One qualifier would reconcile them.

## Attacks that failed (stated plainly)

- **"prevents"/"closes R15-V1" overreach: not found.** Zero occurrences of `prevents`,
  `closes R15`, `close R15` or `clears R15` in `corpus/`, `SKILL.md`, `SCORECARD.md`;
  the only `resolve R15-V1` strings are negations (`round-16.md:14` "does not … resolve
  R15-V1"; `round-16-verifier-spotcheck.md:129` "This closure does not resolve R15-V1").
  The chain carries the opposite disclaimers:
  `round-16.md:14` ("does not intercept tools or resolve R15-V1"), `:93` ("R15-V1
  host-recovery L0 remains open"), `:152-153` ("carried/unresolved, not remeasured or
  repaired"), `round-17.md:74-75` ("R15-V1 stays operator-owned"), `round-17.md:20` ("cannot
  prevent a call"), `QUALITY.md:91-92` ("not tool interception … or remediation"), `:104-105`,
  `SKILL.md:572-573` ("never interception, prevention or host repair"), `SCORECARD.md:860`.
- **C3's numeric claims all hold at HEAD.** Re-ran the three suites at 988b858:
  `core` 9/9, `compound` 16/16, `hardening` 33/33, exit 0, identical
  `SELFTEST_SCRIPT_SHA256: 4ced68d3…`. Anchor: 8 findings over 7 distinct call lines
  (9, 17, 29, 43, 54, 54, 57, 60), counts `host_mutation:2, live_probe:1, package_query:5`,
  exit 1; `call_38165` is the line-54 toolCall id (`oracle-r15.json:455,467`,
  `schema-variants.json:147`). Oracle comparison: `oracle_only = 0` for rounds 13-16;
  `tripwire_only = 3+0+18+0 = 21` exactly as stated. `tripwire-r17-w1.txt`: 70 files,
  `clean`, 1 unparsed spawn, 1 `eval_unparsed`. Package counts 19/46/177/2 exact.
  Round-16 second query `CustomMan:24` exact; `ReviewDocsEra:50 sudo -n true` exact;
  r14 installs disclosed in `round-14.md:111-115` so correctly absent from M2's
  "undisclosed" list; r13 lesson install silence exact.
- **C1 literal counter holds.** `git show 988b858:corpus/QUALITY.md | grep -cE '^[0-9]+\. .*lessons/'`
  → **15**; total `^[0-9]+\. ` → **23**. QUALITY 23 text and the label-check registry row exist.
- **QUALITY 21 does not overclaim.** Its own text disclaims interception, host immutability,
  real dry-run and remediation (`QUALITY.md:91-94`), and keeps R15-V1 with the operator
  (`:104-105`).
- **R15-V1 is never closed by M2/C3.** M2's "fences were prompt-only" is a diagnosis of
  enforcement, not a claim that the libinput harm was repaired; the host-state row
  (`round-17.md:18`) marks the current state `[UNK]`.

## Affected axes

| Axis | Effect of the findings | Effect of the proposed move |
|---|---|---|
| A1 claim correctness C1 15/23 | unchanged (verified) | unchanged (prose only) |
| A1 C2 rubric V 4/6 | unchanged | unchanged (no `corpus/knowledge/` edit) |
| A1 C3 capability | unchanged (all numbers verified) | unchanged (no tool/suite edit) |
| A2 chain fidelity | harmed by F1/F3/F5/F7 | improved to literal accuracy |
| A3 evidence precision | harmed by F2/F4/F6 | improved; fifth transaction and /proc counterexample named |
| A4 host safety | unchanged; no lane operation | unchanged (text-only) |
| A5 separability | intact | intact (no measured fraction moves) |

## Proposed move (one, bounded)

**A single append-only "chain scope qualifiers" erratum** in `corpus/lessons/round-17.md`,
plus one pointer qualifier at `SKILL.md:45`. The first four findings share one root: an
attribution- or class-scoped observation is written as a window/class totality; F5 is the
same collision expressed as an unqualified row reference. One block, five short lines, no
rewrite of any landed row, no new QUALITY criterion:

1. Re-scope M2's r13 parenthetical: "absent from `round-13.md`; the install is disclosed at
   `LOG.md:798-800`, `GlobalCapture.md:15-16`, `EvidenceChain.md:81,168`, `ReviewPhases.md:24,71`
   and the r13 spot-check `:211` — 'only the spot-check' is withdrawn."
2. Re-scope the transaction census: "4/4 is **mado-attributed**, not window-total; the fifth
   in-window transaction, `man-pages` at `/var/log/pacman.log:2416` (01:07:12-0300), is
   excluded as sibling-lane by string presence only (`tripwire-pacmanlog-join.txt:9`); r13/r14/r15
   unparsed spawns 7/10/25 leave the log→finding direction open."
3. Re-assign the query authority: "the 244/293 `package_query` findings are forbidden by the
   wave-context text and `SKILL.md:40-42`; QUALITY 21's text covers transactions and
   service/compositor mutations only (`QUALITY.md:82-86`)."
4. Bound the SKILL sentence in place: "…every breach it reports **in its covered command
   classes**, including every previously disclosed one; the `/proc/1706/maps` read
   (`round-16.md:25-26`) is disclosed debt outside its rules."
5. `SKILL.md:45`: "see **QUALITY 21 and round-16 lesson M1/M2**" (matching `:493-494`).

Why this and not a new criterion: `SCORECARD.md:883-884` records that a tripwire criterion
was proposed and **not** added because it would inflate C1's fraction. Any new numbered
QUALITY line changes the denominator 23→24 and retroactively moves the measured calibration;
the erratum stays prose and keeps 15/23 and 4/6 untouched. This is a synthesis of the
separate wave-2 attacks on M2/C3/SKILL, not a fifth surface: the r13 correction already in
progress in the worktree becomes line 1 of the same block rather than a parallel edit.

## Risks

1. **In-flight collision.** The worktree already rewrites M2's r13 parenthetical (one line,
   +39 chars). The erratum must land after that edit and cite HEAD 988b858 plus the
   corrected sentence, or it will read as contradicting it.
2. **Append-only discipline.** M2 says "Earlier lessons are not rewritten here"; lines 1-3
   must be a new dated block, never an edit of row M2.
3. **Re-scoping does not weaken the rule.** Line 3 must keep the query prohibition (wave
   context is binding) and only move its authority; otherwise it reads as an excuse.
4. **`clean` stays bounded.** Line 4 must not turn the tripwire's `clean` into a host-clean
   verdict; it only removes the false universal.
5. **SKILL:45 is pre-round-17 text.** If in-place edits are disfavored, append the qualifier
   as a SKILL erratum line rather than editing the bullet; either way the string
   "round-16 lesson M1/M2" is the acceptance marker.
6. **F6 is left as disclosure, not repaired.** The `m_swe` provenance cannot be receipted
   from committed bytes; the erratum should either drop the parenthetical or tag it `[INF]`,
   not manufacture a receipt.

## Verification

- `git show REV:corpus/lessons/round-17.md | sed -n '/## Errata (round 17, wave 2)/,+12p'`
  → block present, five numbered lines.
- `git show REV:corpus/QUALITY.md | grep -cE '^[0-9]+\. .*lessons/'` → 15 and
  `grep -cE '^[0-9]+\. '` → 23 (unchanged; run at the post-edit rev).
- `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/core|compound|hardening`
  → 9/9, 16/16, 33/33, exit 0 (re-run today at HEAD: same output,
  script sha `4ced68d3…`).
- `grep -c maps .ufo/waves/round-17/evidence/tripwire-r15.txt` → 0 (counterexample still
  stands; the erratum acknowledges it rather than hiding it).
- `grep -n 'round-16 lesson M1/M2' SKILL.md` → hits at 45 and 494.
- `git diff --stat HEAD` before/after → only the erratum (plus the concurrent lanes), no
  receipt or tool byte changed.

## Evidence commands actually exercised

`git rev-parse HEAD`; `git log`; `git show 988b858:<path>`; `git diff --stat HEAD`;
`git diff 3e9848a 988b858 -- corpus/lessons/round-17.md SKILL.md`;
`python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/{core,compound,hardening}`;
`python3` one-shot parsers over `tripwire-r13..r16.txt`, `tripwire-anchor-r15.txt`,
`tripwire-vs-oracles.json`, `oracle-r15.json`, `tripwire-pacmanlog-join.txt`;
`sed`/`grep`/`nl` over `/var/log/pacman.log:2405-2435`, `corpus/lessons/round-1{5,6,7}.md`,
`corpus/QUALITY.md`, `SKILL.md`, `LOG.md`, `SCORECARD.md`, and the round-13/15 seat reports.
No file in the lane was written except this report. Install record: **none**.
