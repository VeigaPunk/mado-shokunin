# RevQuality — w2 review of QUALITY.md criteria 82-84 (round 44, data commit e4678921)

Seat: RevQuality (leaf, w2). Target: the three criteria landed at `e46789213830597348fe96a351ae004d10587385`
(`corpus/QUALITY.md:411` = 82, `:413` = 83, `:415` = 84; line numbers computed with `grep -n '^8[234]\.'`).
Method: ran each criterion's Check command and each "Shown able to fail" reproduction at the data commit
(scripts taken from the working tree at tip `290cddea92a18e2202456db89cb2bb60d9aaacff` — see F1 for why),
then checked every lesson citation. Receipts: `.ufo/waves/round-44/w2/RevQuality/receipts/*.txt`, each in
`$ cmd` / output / `exit=` form. No tracked file edited; no mutating git/jj; no pacman; no compositor call;
no tool installed (python3 3.14 stdlib + read-only git only).

## Result in one line

Every check command and every "Shown able to fail" claim reproduces exactly at e4678921, and all three
lesson citations exist with a real mistake behind them. One MEDIUM finding: the criteria's own instrument
citations are LATE at the admission revision — criterion 83, run on `corpus/QUALITY.md` itself at
e4678921, prints `verdict=FAIL` with one LATE row per criterion (82, 83, 84). Two LOW wording/resolution
nits and two INFO observations below.

## Criterion 82 (`corpus/QUALITY.md:411`) — verified

- Check command at the data commit: `python3 -I quality/ratio-domain-meta.py --repo . --rev e4678921… --from 34 --to 43`
  → `DOMAIN_META: domain=12 meta=5 window=34-43 default=1`, exit 0, 17 claim rows
  (`receipts/82-ratio-data.txt`). Identical at the freeze `03fa5c61` (the lesson's instantiated rev,
  `82-ratio-freeze-lesson-cmd.txt`) and at the tip (`82-ratio-tip.txt`).
- "which the round lesson carries verbatim": `corpus/lessons/round-44.md:255` is byte-equal to the tool's
  output line (`82-lesson-verbatim-check.txt`, `BYTE-EQUAL: True`; lesson unfenced, `grep -c '```'` → 0).
  The hand-labelled disagreement and its disposition are carried (`round-44.md:250-251` area: round-36 C2
  "is classed meta by the rule … the rule is retained").
- "rounds 34, 35 and 39 are mixed": visible in the same output (34 C1 domain/C2 meta; 35 same; 39 C1 meta,
  C2+C3 domain). The quoted tally "4 domain rounds to 2 calibration rounds" is at
  `considerthese/2026-10-25.md:46` (verified by grep).
- Shown able to fail, both reproduce at e4678921:
  - mutant `.ufo/waves/round-44/w1/ExecDomainMetaRatio/ratio-mutant-axis-token.py` →
    `DOMAIN_META: domain=13 meta=4 window=34-43 default=0` (`82-mutant-data.txt`) — "13 against 12" holds,
    and the two outputs differ in exactly one row (36 C2: domain vs meta).
  - draft 1 `ratio-draft1-no-clause2.py` → `40 | C1 | operability | meta`
    (`DOMAIN_META: domain=11 meta=6 window=34-43 default=2`, `82-draft1-data.txt`). The deliverable
    attribution is fair: the round-40 C1 claim row (SCORECARD.md:2480) carries only `--live`, and
    `tools/mado-options.py --live` is the tool behind it (SCORECARD.md:2487).
- Rule frozen in the docstring: `--rule` prints the 7-clause rule (`82-rule.txt`); the landed
  `quality/ratio-domain-meta.py` is byte-identical to the w1 `ratio.py` (diff empty), so the promotion
  changed nothing.
- Lesson citation exists: `corpus/lessons/round-44.md` `## considerthese` at `:248`;
  `considerthese/2026-10-25.md` proposal 1 at `:46`. Mistake behind it: the prose ratio was not a
  re-runnable count — grounded by the tool's own mixed-round output above.

## Criterion 83 (`corpus/QUALITY.md:413`) — red/green reproduce exactly

- Red: `python3 -I .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py --repo . --rev 1959770 --doc
  corpus/knowledge/hyprland-gkeep-geometry-r43.md --prefix .ufo/` →
  `CHECK83: verdict=FAIL citations=3 violations=2` with `LATE … ExecGoalVsValue/finding.md (added 2a3707c
  after 1959770)` and `LATE … ExecOracleGkeep/20-observation.txt (added 2a3707c after 1959770)`
  (`83-r43entry-1959770.txt`). `1959770` confirmed as the round-43 data commit and `2a3707c` as the
  round-43 w1-evidence commit (`git log --format='%h %s' -1` on both).
- Green: same doc at the tip → `CHECK83: verdict=PASS citations=6 violations=0` (`83-green-tip.txt`).
- Lesson citation exists: `lessons/round-44.md` M44-4 at `:135` (entry cited two seat receipts by bare
  path before they existed, plus the off-by-six locator — evidence commands in the lesson); "round-43
  closure D4" exists at `corpus/lessons/round-43-verifier-spotcheck.md:104`.

## Criterion 84 (`corpus/QUALITY.md:415`) — check command reproduces

- Full controls run at the criterion's own parameters:
  `python3 -I .ufo/waves/round-44/ctl/run-c2-controls-v2.py --repo . --freeze 03fa5c61… --base 6a1a905…
  --work /fast/scratch/hyaku/mado-r44/RevQuality/ctl-c2` → exit 0, 33 s:
  `CTL_C2v2 FORGED-PIN want=rejected got=rejected rc=1 ok | a:1 b:1 c:1 d:0 …` (the criterion's "rejected
  … d:0") and `CTL_C2v2 VERDICT: PASS (wrong=0 of 11; positive admitted=1)`; P admitted with
  `d:1 … j:1` (`84-ctl-c2-v2-rerun.txt`). Verdict lines match the committed receipt
  `.ufo/waves/round-44/receipts/ctl-c2-v2.txt` byte-for-byte on the verdict lines (fixture revs differ).
- Shown able to fail reproduces at three levels:
  - both cited v1 receipts exist at the tip and show the forgery ADMITTED under v1:
    `w1/CritC2Cheat/frozen-F2-FORGED-PIN.txt` (`clauses=a:1 … i:1 admitted=1 … verdict=TARGET_MET`,
    fixture rev `4a59d12`) and `w1/RevC2Counter/log-forged_s164.txt` (same verdict, rev `bf03580`);
  - the code fact: the v1 counter at the freeze sets `pin_ok = True` and digest-checks only
    `if i in new_ids` (`git show e2289516:quality/counters/c2-r44-gkeep-size-request.py` → `:496-497`);
  - "inherited by four C2 counters": the same branch verified at `c2-r43-gkeep-entry-v2.py:490-491`,
    `c2-r42-gkeep-entry.py:410-411`, `c2-r41-focus-entry-v2.py:367` (all at e4678921) — four counters
    including r44 v1.
- Lesson citation exists: `lessons/round-44.md` M44-8 at `:178`, with the mistake, the two receipts, the
  fix (T1 in PRED-C2-r44-v2) and the shown-able-to-fail control.

## Findings

**F1 MEDIUM — the landed criteria fail their own just-landed citation rule at their admission revision.**
Attacks: `corpus/QUALITY.md:411,413,415` as landed at `e4678921` — each criterion's Check/Shown-able-to-fail
text formats a wave path as code that is not in the tree at that revision. Reproduction (criterion 83's own
command, on QUALITY.md itself):
`python3 -I .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py --repo . --rev e4678921… --doc
corpus/QUALITY.md --prefix .ufo/` → `CHECK83: verdict=FAIL citations=60 violations=5` (`83-QUALITY-at-data.txt`),
with per-criterion isolation (`83-percriterion-*.txt`):
- 82: `LATE .ufo/waves/round-44/w1/ExecDomainMetaRatio/ratio-mutant-axis-token.py (added 410f193 after e467892)`;
- 83: `LATE .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py (added 410f193 after e467892)` — the criterion's own check script;
- 84: `LATE .ufo/waves/round-44/w1/CritC2Cheat/frozen-F2-FORGED-PIN.txt (added 410f193 after e467892)`.
All three first enter the tree at `410f193` (a `refs/jj/keep/` ref, child of the data commit); on the lane
branch they first appear at `290cddea`. At the tip the same per-criterion runs PASS — but the criterion's own
text says "reading the document at the tip does not repair it", and the M44-4/D4 precedent judged this exact
shape (claim admitted at a data commit, receipts landed in the next commit) a violation for the round-43
entry. Precedent nuance the L1 should weigh: `corpus/QUALITY.md` at the round-43 data commit `1959770` fails
the same way (`violations=7`: check78/79/80.py, ExecLocatorGate/receipt.txt, check78.sh all LATE there,
`83-QUALITY-at-1959770.txt`) and the round-43 closure scoped D4 to the entry only — so the landing practice
predates criterion 83, and criterion 83 now formalizes that practice as a violation. Also inside F1: two
evidence citations escape the criterion's own `--prefix .ufo/` filter entirely — 82's bare-name
`ratio-draft1-no-clause2.py` (absent at e4678921, `git cat-file -e` fails) and 84's relative
`w1/RevC2Counter/log-forged_s164.txt` (see F3) — and criterion 84's runner reads
`w1/CritClaimSizing/controls/entry-r12-repoint.md` and `entry-minimal.md` from the tree, both absent at
e4678921, so a checkout at exactly e4678921 cannot re-run the 84 command as written (my re-run used the tip
working tree and reproduced the committed verdict lines).

**F2 LOW — criterion 83's parenthetical explains both violations with the wrong directory.** Attacks:
`corpus/QUALITY.md:413`, "(the w1/ExecOracleGkeep files landed in `2a3707c`)". The run's two LATE rows are
`.ufo/waves/round-43/w1/ExecGoalVsValue/finding.md` (entry `:56`) and
`.ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt` (entry `:62`) — only one is ExecOracleGkeep; the
entry's `10-cases.txt` bare-name citation is OUTSIDE (unjudged) to the checker. Corrected sentence for the
L1: "(the cited w1 receipts `.ufo/waves/round-43/w1/ExecGoalVsValue/finding.md` and
`.ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt` landed in `2a3707c`)".

**F3 LOW — criterion 84's second shown-able-to-fail citation does not resolve as written.** Attacks:
`corpus/QUALITY.md:415`, backticked `w1/RevC2Counter/log-forged_s164.txt`. No tree path has that form; under
check83's resolution order (document-relative) it becomes `corpus/w1/…` → NOWHERE, and the criterion's own
`--prefix .ufo/` skips it unjudged. The file exists at `.ufo/waves/round-44/w1/RevC2Counter/log-forged_s164.txt`.
Corrected form: cite it with the `.ufo/waves/round-44/` prefix like its sibling citation in the same sentence.

**F4 INFO — the committed controls receipt's freeze label differs from the criterion's re-run freeze.**
`receipts/ctl-c2-v2.txt:1` records `freeze=e2289516…` (the receipt is committed in `03fa5c61`, so the v2
freeze did not exist when it was produced); criterion 84's command names `03fa5c61…`. My re-run at the
criterion's freeze reproduces every verdict line, so no correction is required; noted so a reader comparing
the two freeze labels is not surprised.

**F5 INFO — criterion 82 is the only one of the three grounded by a proposal section rather than a numbered
mistake.** Its lesson citation (`lessons/round-44.md ## considerthese`, `:248`) exists and the preamble's
lessons-citation requirement is met; the mistake behind it (a prose ratio that is not a re-runnable count) is
real and evidenced by the tool's mixed-round output. 83 and 84 anchor to M44-4 and M44-8. Observation only.

Context, not findings against 82-84: the whole-document run's other two violations are pre-existing checker
noise — `NOWHERE .ufo/waves/round-49/w1/ConnCrossClaim.md` (criterion 71's deliberately-dead example path)
and `NOWHERE .ufo/waves/round-N/receipts/closure-status.txt` (criterion 81's template placeholder).

## Support (what reproduces — summary)

| criterion | check command at e4678921 | shown able to fail | lesson |
|---|---|---|---|
| 82 | `DOMAIN_META: domain=12 meta=5 window=34-43 default=1` exit 0; byte-equal at lesson `:255` | mutant 13/4/0 (one-row diff at 36 C2); draft1 `40 C1 meta` | `## considerthese` `:248` + proposal 1 `considerthese/2026-10-25.md:46` |
| 83 | red `FAIL citations=3 violations=2` at `1959770`; green `PASS citations=6 violations=0` at tip | exact | M44-4 `:135` + D4 `round-43-verifier-spotcheck.md:104` |
| 84 | `FORGED-PIN … rejected … d:0`, `VERDICT: PASS (wrong=0 of 11; positive admitted=1)`, exit 0 | v1 admitted the same forgery (two receipts); branch in four counters at the cited lines | M44-8 `:178` |

## Residual risk and verification gaps

- "a rule frozen in the tool's docstring before its first run" (82) is not independently re-verifiable
  post-hoc; what is verified is that the landed tool is byte-identical to the w1 `ratio.py` whose report
  asserts the ordering, and `--rule` prints the docstring rule.
- I did not re-run the v1 forgery end-to-end myself; the v1-admission claim rests on the two committed w1
  receipts (both read, both show `admitted=1/1 verdict=TARGET_MET`) plus the v1 counter's verified
  new-ids-only branch. The v2 side is my own run.
- Criterion 83's checker scores backticked tokens only and its bare-name/relative resolution has the blind
  spots named in F1; a citation outside those forms is unchecked by it.

## Tooling record

No tool installed or updated (none needed). Scratch `/fast/scratch/hyaku/mado-r44/RevQuality/` used for the
controls fixtures and the per-criterion extraction files; the runner removes its own clones; the scratch dir
is deleted before this report is finalized. No pacman, no host-service or compositor call, no input
injection, no subagent, no background job.

Report: .ufo/waves/round-44/w2/RevQuality.md
