# QUALITY criteria 82–86 — draft (round 44, w1, seat ScrQualityCriteria)

Append after criterion 81 (`corpus/QUALITY.md:409` is the file's last line; `grep -c '^[0-9]\+\. ' corpus/QUALITY.md`
prints `81`). No renumbering; criteria 1–81 stay byte-identical. Suggested section heading, because criteria 69–81 still
sit under the round-30 heading (`corpus/QUALITY.md:338`):

```
## Criteria from the round-43 closure defects (round 44; spotcheck §6 D3–D7)
```

Every criterion below has a mistake behind it — the routed closure defects of
`corpus/lessons/round-43-verifier-spotcheck.md` §6 (`:97`–`:109`) — and every claim in it was re-derived this seat
from committed bytes. The transcript is `receipts.txt` in this directory (`bash run-checks.sh [WORKDIR]` re-derives it
from committed objects and regenerates every synthetic control). Nothing here writes the lane: the five checkers read
git objects only. Six of the nine items in §6 are refused at the end, with reasons.

## Grounds: five mistakes, each with the pointer that carries it

| # | mistake (round 43, routed) | evidence pointer | control that shows the check can fail |
|---|---|---|---|
| 82 | a tool's verdict vocabulary ignored a state field its input carries, so a fullscreen client read `DIFFER`; the same overstatement sits in prose at `SKILL.md:276` | `.ufo/waves/round-44/fetch-c1/Hyprland-HyprCtl.cpp:410` (`"fullscreen": {},`), `:451` (`.internal` printed); `git show 6a1a905:tools/mado-geometry.py \| grep -ci fullscreen` → `0`; `.ufo/waves/round-44/receipts/ctl-c1.txt:3` (`fixtures=13/26`) | base tool `L2-unmentioned-undeclared`; L3-only red on the reference with its field cases removed; L1 red at the wrong line |
| 83 | an entry cited an oracle transcript by path and the transcript did not exist at the data commit that admitted the entry | entry `:66` (D4, `corpus/lessons/round-43-verifier-spotcheck.md:104`); `git cat-file -e 1959770:.ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt` → absent; the adding commit is `2a3707c` | same document: `LATE` at `1959770`, `PASS citations=6` at `5846662` |
| 84 | the report quoted a tip axis reading that no receipt in the tip tree names; the tip tree's only axis receipt names the base | `.ufo/waves/round-43/receipts/axis-base.txt:4` (`rev=a35cfdf…`); D7 at `corpus/lessons/round-43-verifier-spotcheck.md:109` | red at `5846662` and at round 44's freeze; synthetic tip receipt passes, its `mismatched=1` twin fails |
| 85 | the registration's plan count (`37 seats`) was read as the count that ran (38) | `.ufo/waves/round-43/registration.md:5`; `.ufo/waves/round-43/w1-results.json` (`seats=38`, 38 rows); D5 at `corpus/lessons/round-43-verifier-spotcheck.md:106` | red on the round-43 pair (`plan=37 results_seats=38`, `plan=69 results_rows=70`); green on round 44's bound form and on a synthetic agreeing pair |
| 86 | a receipt cited `gkeep-shm.c:156-164` for a fact at `150-159`; criterion 77 cannot see it (the locator is not backticked and the file is outside `fetch/`) | `.ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt:24`; `gkeep-shm.c` occurrences of `app_id` at `34,58,116,118,150` | red on the committed receipt (`ids_outside=app_id@34`), green on the `150-159` copy |

Classes: 82 *state-space shortfall* (the vocabulary is smaller than the producer's state space — captured by deriving
the field list from the pinned serializer and requiring silence to be declared); 83 *early citation* (a claim admitted
before its evidence exists — captured by resolving the path at the citing revision, not at the tip); 84 *untipped
receipt* (a receipt exists but names another revision — captured by matching `rev=` to the closing revision); 85
*plan read as result* (captured by one number from two files); 86 *range slop* (the range contains part of the fact —
captured by resolving the source in the repo and testing each identifier against the range).

---

82. A tool that reports on a value an external program owns audits its verdict vocabulary against the state fields that
program's serializer carries: for each field that can move the compared value without the client asking, the tool either
consumes it (a verdict word, a summary counter, a selftest case that names it) or ships a line declaring it ignored with
a reason. The field list is derived from the pinned producer source, never from the tool's own reading, so a field the
tool never opens is a decision it writes down rather than a gap nobody recorded. Check:
`python3 -I .ufo/waves/round-44/w1/ScrQualityCriteria/check82.py --source .ufo/waves/round-44/fetch-c1/Hyprland-HyprCtl.cpp --tool <tool> --must fullscreen:Hyprland-HyprCtl.cpp:410 [--declare FILE] [--audit]`
— leg L1 requires the cited source line to print `"KEY":` inside the client-object block, L2 requires the tool to name
the key or carry `IGNORED-FIELD KEY <reason>`, L3 requires a `chk(` case whose call text names the key; a
`L1-source-miss`, `L2-unmentioned-undeclared` or `L3-no-selftest-case` row with `CHECK82: verdict=FAIL` is a violation.
Shown able to fail: the round-43 tool at `6a1a905` names the field zero times and is `13/26` under the round-44 counter
(`.ufo/waves/round-44/receipts/ctl-c1.txt:3`), scored `mention=0 declare=0 case=0`; the frozen reference scores
`mention=31 declare=0 case=10 ok`; L3 fails alone on the reference with its 13 selftest lines naming the field removed
(`mention=14 declare=0 case=0`), and L1 fails alone when the same reference is scored at `Hyprland-HyprCtl.cpp:400`. (lesson:
lessons/round-43-verifier-spotcheck.md §6 D3 — the same state-space shortfall in prose at `SKILL.md:276`, whose
`Licenses` column says `the tiler, not the floating rule path, set its box` while its own caveat column carries the
pseudo-size setter; the tool half is round 44's C1 claim, `.ufo/waves/round-44/registration.md` §C1)

83. A citation resolves at the revision the citing document is judged at: every repository path a document formats as
code exists in that revision's tree, and a path that first appears in a later commit is `LATE` — the claim was admitted
before its evidence was in the tree — whether it is a receipt, an oracle transcript or a log. Reading the document at
the tip does not repair it: an entry admitted at a data commit is read at that commit, and a document that resolves only
later carries the defect into every later reader. Check:
`python3 -I .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py --repo . --rev <REV> --doc <PATH-IN-REPO> [--prefix .ufo/]`
— backticked tokens are resolved as written under a repo-root prefix, relative to the document's directory, or by
basename; a `LATE`/`EARLIER`/`NOWHERE` row with `CHECK83: verdict=FAIL` is a violation, and a name no ref holds that is
neither repo-rooted nor path-shaped is reported `OUTSIDE` (package and upstream names are not the lane's citations).
Shown able to fail: `corpus/knowledge/hyprland-gkeep-geometry-r43.md` at the data commit `1959770` prints
`LATE …/20-observation.txt (added 2a3707c after 1959770)` and exits 1 (`citations=3 violations=2`), while the same
document at `5846662` passes `citations=6 violations=0`; the defect is D4 (`corpus/lessons/round-43-verifier-spotcheck.md:104`:
`they did not exist at data commit 1959770`). (lesson: lessons/round-43-verifier-spotcheck.md §6 D4)

84. A round's axis verdict at closure is read from a receipt committed at the closing revision whose own bytes name that
revision. A receipt naming the base or an earlier data commit is a base or data reading, is labelled as one, and cannot
stand in for the tip; the report's axis line and the receipt are one reading, so either the report quotes a
`MADO_AXIS … rev=<closing revision>` line from the closing tree or it says, in the same line, at which revision the last
receipt stands. Check:
`python3 -I .ufo/waves/round-44/w1/ScrQualityCriteria/check84.py --repo . --rev <CLOSING_REV> --receipts <round>/receipts`
— every `MADO_AXIS: checked=… mismatched=… rev=…` line is printed with `TIP`/`OTHER`; `verdict=FAIL` when no receipt
names the closing revision or the tip receipt reads `mismatched>0` or carries a `FAILED:` line. Shown able to fail: at
round 43's tip `5846662` the only axis receipt is `.ufo/waves/round-43/receipts/axis-base.txt:4`, whose `rev=` is the
base `a35cfdf…` → `CHECK84: verdict=FAIL no receipt names the closing revision 5846662`; round 44's freeze tree has the
same shape (`axis-base.txt`, `rev=6a1a905…`); a synthetic receipt naming `5846662` passes, and its `mismatched=1` twin
fails. A scan of every committed `MADO_AXIS` receipt in `round-35`…`round-44` (13 rows, each one `match=0`) finds no
receipt whose `rev=` is the commit that carries it — round 37's four are the base, the data commit and two others, and
`round-38`…`round-44` commit only an `axis-base.txt` — so adopting this criterion is prospective: the LOG says so rather
than the past being silently tightened (the same disclosure criterion 79 needed).
(lesson: lessons/round-43-verifier-spotcheck.md §6 D7 — `no committed axis receipt at the tip`)

85. A frozen registration's seat count is a plan; the executed count is the wave's results file, and the closure
reconciles the two in one line. A registration either states no literal seat number and binds the counts to each wave's
`*-results.json`, or every literal `w<k> … N seats` equals both that file's `seats` field and its `results` length, and
any planned total equals their sum. A plan number quoted as the count that ran is a violation even when the difference
is disclosed elsewhere, and a literal number with no results file at the revision is unverified, not green. Check:
`python3 -I .ufo/waves/round-44/w1/ScrQualityCriteria/check85.py --repo . --rev <REV> --registration <round>/registration.md --results w1=<round>/w1-results.json [--results w2=…]`
— `VIOLATION WAVE`/`VIOLATION TOTAL`/`VIOLATION UNBOUND` lines with `verdict=FAIL` are violations. Shown able to fail:
round 43's `.ufo/waves/round-43/registration.md:5` states `w1` … `37 seats` while `w1-results.json` holds `seats=38` and 38 rows →
`VIOLATION WAVE w1 plan=37 results_seats=38`, and its planned total 69 against 70 rows; round 44's registration passes
in bound form (`bound=1`, no literal count), and a synthetic pair with agreeing numbers passes in equal form.
(lesson: lessons/round-43-verifier-spotcheck.md §6 D5 — `says 37 w1 seats (38 ran`)

86. A locator's source is resolved from the repository, not only from the pinned fetch set, and the cited range carries
the identifiers the citing line names: for `<name>:<start>-<end>` where a committed file of that name exists, every
code-shaped identifier (snake_case) on the citing line that occurs in the source also occurs inside the range. A range
that contains some of the fact is not the fact's span, and a file the lane itself committed is not exempt from the gate
because it is not a fetch. Check:
`python3 -I .ufo/waves/round-44/w1/ScrQualityCriteria/check86.py --repo . --rev <REV> --file <PATH-IN-REPO> [--only <basename>]`
— `UNRESOLVED`, `AMBIGUOUS`, `RANGE` and `OUTSIDE` rows with `verdict=FAIL` are violations; an identifier absent from the
source is listed as `skipped`, not scored. Shown able to fail:
`.ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt:24` cites `(gkeep-shm.c:156-164)` for a sentence naming
`app_id`, and `app_id` occurs in the committed `gkeep-shm.c` only at lines 34, 58, 116, 118 and 150 →
`OUTSIDE gkeep-shm.c:156-164 ids_inside=0 ids_outside=app_id@34`; the corrected `150-159` copy prints
`ids_inside=app_id` and passes. Criterion 77 cannot see this: the locator carries no backticked fragment and
`gkeep-shm.c` is not a file under `fetch/`. (lesson: lessons/round-43-verifier-spotcheck.md §6 D4, second sentence —
`correct range 150-159`)

---

## Which of the routed defects I refuse, and why

- **D1 — refused (already numbered).** The r10 refusal reason (`corpus/lessons/round-43.md:75`: its row cites S291/S293) cites the box-path rows
  and not the reported-field rows, and maps S310 to two of its three registry rows. That is an application of criterion
  42 and criterion 77, both of which M43-1 and M43-7 already record as this lane's own repeats of the class; a new number would restate them. The repair is the appended erratum
  the spotcheck asks for at `:97`.
- **D2 — refused (no observable).** A row title that echoes a refuted premise (`corpus/SOURCES.md` S293,
  `corpus/lessons/round-43-verifier-spotcheck.md:100`) is repaired by the registry's own append-only supersession; a
  criterion needs a check that can fail, and no mechanical reading of a title distinguishes "echoes the premise" from
  "names the document". Minting one would create a criterion with a judgement and no control.
- **D3 — refused as a new number (assigned to 82).** `SKILL.md:276`'s `Licenses` column asserts
  `the tiler, not the floating rule path, set its box` while its own caveat column carries the pseudo-tile setter
  (`Window.cpp:2402-2408` at `.ufo/waves/round-43/w1/ExecGoalVsValue/pins/window.cpp:2402-2408`). The class is
  criterion 82's (a vocabulary smaller than the pinned source's state space) applied to prose, and M43-9 already
  records the inference half; the repair is a supersession of the cell, not a new gate.
- **D6 — refused (declared predicate weakness, already bound).** The cheats that reach MET and the surviving mutants
  are the lane's own declared residuals; criteria 36 and 56 bind controlled-versus-declared clauses, and the lane's
  repair is re-registration before the next use. Nothing in D6 is a class the bar does not already carry.
- **D8 — refused (no lane mistake).** A duplicated driver `complete` line is a driver fact; criterion 81 already
  counts attempts from the digest's `launch`/`complete` lines and says a completion line is not round fact.
- **D9 — refused (no mistake this round).** The still-open round-41 items are logged and carried; being unresolved is
  not a mistake of round 43.

## Notes for the L1 (integrator)

- **Numbering.** 82–86 because `corpus/QUALITY.md` ends at criterion 81 (409 lines, `grep -c` → 81). No other seat's
  draft is visible to this seat at write time; if another seat claims 82, shift this block and update the five `Check:`
  commands in one commit (they name this seat's directory, not a number).
- **Checkers are seat-local, as in rounds 41 and 43.** `check82.py`–`check86.py` live beside this file with
  `run-checks.sh` and `receipts.txt`; their sha256 are the first block of `receipts.txt`. If they should outlive the
  round they need a committed home under `quality/`; moving them means editing the five `Check:` lines.
- **Criterion 84 is not criterion 69 re-run.** 69 extracts a `rev=` token from a report's prose and looks for it in a
  receipt; 84 reads the receipts themselves and keys on the closing revision, so it runs in the lane alone. The
  round-43 report is committed in the fleet repo (`906cfe70`), and 69 invoked lane-only returns `MISSING-REPORT`
  (exit 2) rather than a verdict — the tail of `receipts.txt` records both invocations. A setup error is not a pass.
- **Adopting 82 does not condemn the frozen reference.** The reference tool itself leaves 15 scalar keys of the client
  block unmentioned and undeclared (`AUDIT` line in `receipts.txt`), so the criterion's scope is the claim's own subject
  (`--must`), which is what its `Check:` command takes; "every field" would fail the artifact the round froze.
- **Parser limits, declared.** 82's block extraction includes the nested `workspace` keys (`id`, `name`) and stops at
  `stableId`; 83 judges backticked tokens only (bare prose paths are out of scope on purpose); 85 reads a same-line
  `N seats` form and needs the pattern extended for table-shaped plans; 86 scores snake_case identifiers only, so a
  locator line naming no code-shaped identifier (`gkeep-shm.c:152-155`) is unchecked.
