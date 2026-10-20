# ConnConsiderThese — the two reflections against round 18's claims

Seat `MadoR18.ConnConsiderThese` (connector, leaf, no dispatch). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Snapshot `2026-10-20T15:46Z`,
lane HEAD `d3a0000` (pre-registration), worktree dirty with wave-1 output
(`tools/mado-tripwire.py`, `tools/mado-verify.sh`, `.gitignore` modified;
frozen snapshot and drafts untracked). Every path below is a lane path.
This report is my only write. No git/jj write, no lane gate run, no package,
service, compositor, input or screenshot operation; no tool installed or
updated.

Snapshot caveat: the wave is in flight. `tools/mado-tripwire.py` was
`962919ce…` at `d9a5a18` and `762cf56f…` in the worktree at snapshot; none of
those bytes is committed yet. Values below are labelled *snapshot* where they
are not stable across the wave.

Axes in play: **C1 calibration** (literal lesson-citation fraction), **C2
coverage** (rubric V, P1-P6), **C3 operability** (capability acquisition).
Harm watch, not claims: freshness file plane, U-route 7/7, hermetic selftest,
classifier, tripwire suites, navigation, census.

## 1. Source class — both files are reflections, not operator teaching

| Test | 2026-10-19 | 2026-10-20 |
|---|---|---|
| Self-label | `considerthese/2026-10-19.md:3` "Daily mado-shokunin reflection."; `:32` "Self-improvement suggestions (proposals only; not acted on)" | `considerthese/2026-10-20.md:3` same; `:48` same header |
| Commit | `8e0c9b2`, author `João Pedro Veiga <jpveigao10@gmail.com>`, 2026-10-19 10:01:23 -0300 | `f898e52`, same author, 2026-10-20 10:02:18 -0300 |
| Byline inside | none | none |
| Operator-teaching slot | `LEARNING.md:50-51`: a teaching "lands verbatim as `corpus/lessons/operator-<YYYY-MM-DD>-<slug>.md`"; `ls corpus/lessons/operator-*` → none | same |
| Citation weight in lane docs | `grep -c considerthese` → 0 in `LOG.md`, `SCORECARD.md`, `PROVINCE.md`, `README.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md` | same |

The commit identity is the operator's, but authorship authority is not: the
content self-labels as a reflection, no operator-teaching file exists, and the
lane cites the files nowhere. Consequences that bind this join:

1. **No citation obligation runs either way.** These are leads to be re-verified,
   never grounds for a claim. A QUALITY row citing `considerthese/…` would be a
   false grounding (the criteria require `lessons/`).
2. **Their facts are dated snapshots.** `2026-10-20.md:5` says "Round 16 isn't
   admitted yet, and there's no round-16 non-author spot-check in the repo so
   far". `27cd06f` (10:18:29, sixteen minutes after the reflection) admitted
   round 16 with its spot-check. `2026-10-19.md:5` says "no round ran" — true for
   its 10-16..10-19 window, false since 2026-10-19 18:43.
3. **The lane already adopted one line of this.** The round-17 fleet report
   (`.ufo/reports/round-17/mado.md:46`) calls `considerthese/2026-10-20.md` "a
   reflection, not an operator teaching". It did **not** adopt the prior join's
   four-sentence mapping (`round-17/w1/reports/ConsiderTheseJoin.md` §5); the
   label landed, the per-suggestion disposition did not.

## 2. `2026-10-19.md` — dispositions against round 18

Verdicts: *acted* (the round/rounds commit the same move by content, uncredited),
*shape-changed* (same idea, different denominator/evidence class), *partial*,
*open*, *operator-gated*.

| # | Ask (abridged, `:34-40`) | Verdict | Evidence |
|---|---|---|---|
| 1 | Turn the empty `## Capabilities` table into a ready demonstration list (gate live, `--no-live`, `--selftest`, `--regression`, snapshot-diff, drift-watch) | **partial: acted in a round-local annex; the table the ask names is still empty** | `SCORECARD.md:304-311` (round 12) re-demonstrated and entered 4 rows: sources registry, verdict gate live+file plane, hermetic self-test, mutation regression. `:915-919` (round 17) adds the tripwire. `:200-206` — the contract-level `## Capabilities` — still reads `— none yet —`. Two of the six named families (snapshot-diff, drift-watch) have no row at all and appear only in the move log and one erratum (`:21`, `:23`, `:24`, `:258`). `drafts/ScoreResultsDraft.md` adds a round-18 row placeholder. |
| 2 | Declare a saturation line and stagnation window N now | **acted** | `SCORECARD.md:270-274`: "Saturation line: **9.0** on every scored sub-axis. Stagnation window: **N = 3**". `:911` restates "Saturation 9.0 / N=3 unchanged" at round 17; `:948-949` round 18 relies on it ("No stagnation waiver (capability entered round 17)"). The contract-level `## Saturation` at `:208-210` still says "to be declared … on its next round" — same annex/contract split as #1. |
| 3 | Write a one-page unblock brief for João (fleet round 1 routing + receipt binding) | **open (operator-facing)** | `.ufo/blocked/fleet-round-1-routing.json` and `…-receipt-binding.json` were committed at `7cd7f33` (2026-10-15 02:12:36 -0300), before the reflection. They carry `unblockAction` prose and `missingBindings` arrays but are machine blockers, not the decision sheet. `grep -rln "unblock brief\|decision sheet"` matches only `considerthese/2026-10-19.md`. |
| 4 | Refresh the live plane with a read-only gate run | **open / operator-gated (host pause)** | `SCORECARD.md:936-938` carries the host pause; `:945-947`: "freshness … not re-measured — live re-anchor is planned work, not claimed". Round 19's planned freshness item (`drafts/ScoreResultsDraft.md`, Planned) is a file-byte re-anchor of walker/hyprland pins, not the live gate run this asks for. |
| 5 | Restore outside-lane calibration with one sibling admit/reject sample | **acted, exceeded** | Six non-author closures exist: `corpus/lessons/round-{12,13,14,15,16,17}-verifier-spotcheck.md`, commits `e3e6a8e`, `873ff08`, `ea0446f`, `32c4fda`, `27cd06f`, `d9a5a18`, all carrying the protocol-shokunin closure subject line. Effect on `SHONEN.md` is *not* asserted: the round-17 closure keeps four `[~]` author assertions and calls promotion operator-owned. |
| 6 | Target the named coverage gaps next (walker live rows, theme mutant, arc ledger) | **acted in part; remainder named** | `corpus/knowledge/arc-synthesis.md` §6 (12 unknown surfaces) and §7 (9 closed / 8 operator-owned / 12 unknown) are present as described. Round 17 C2 took P6+P4; round 18 C2 takes P3+P5 (`SCORECARD.md:961-968`). Still open: walker live rows and theme live rows (exempted by name, arc §6 last row); the theme covering mutant is record debt #8 (operator-owned); the 12 unknowns are unchanged. The reflection's "walker live rows" is **not** what C2 delivers — C2 is documentary, host binaries `[UNK]`. |
| 7 | Improve the daily pass (cloud `--selftest`, PR listener, stale-PR section) | **open / operator-side** | No lane artifact and no consumer wiring; the ask is `2026-10-19.md:40`, and the next day's file still has no stale-PR section (`2026-10-20.md:5` names PR #1 only in its bottom line). PR #1 status is `[UNK]` here (GitHub not read). |

## 3. `2026-10-20.md` — dispositions against round 18

This table updates the round-17 join's verdicts where round 17 or the round-18
pre-registration changed the answer. No document credits the reflection.

| # | Ask (abridged, `:50-56`) | Verdict | Evidence |
|---|---|---|---|
| 1 | Lead each reflection with a prose host-safety scan (sudo, pacman, systemctl, hyprctl dispatch/keyword, pkill, restart wording) | **not adopted; reflection-side** | The ask is about the reflection's own document order, and the file that proposed it cannot have applied it. The lane's adjacent mechanism is the opposite evidence class: the tripwire reads issued tool calls, not prose (`SCORECARD.md:969-977`; round-17 join §3, still correct). Round 16's fence is `corpus/QUALITY.md:82-88` (criterion 21) plus the SKILL safety section plus `tools/mado-action-plan.py`; round 18's `SentinelHostPause` is harm-watch, not this scan. |
| 2 | Keep a running table of R15 remediation, round-16 admission, PR #1, SHONEN | **partial** | `SCORECARD.md:933` carries the admitted round-17 closure as the round-18 baseline; `:938` carries "R15-V1 stays operator-owned". There is no standing table (`grep '^## ' SCORECARD.md` has no debt section), and PR #1 / SHONEN are absent from the round-18 block — SHONEN is a report section, not a debt row. |
| 3 | Keep a metrics trend line (sources, selftest, U-coverage, calibration, navigation, gate digest) | **open** | `evidence/measure-before.json` is one snapshot (`schema mado-measure-r17-v1`, `rev d9a5a18`); `measure-final.json` does not exist at snapshot; no cross-round trend file exists anywhere in the lane. The round-17 before→after table is the one R17-V2 says was mislabelled — now a criterion-24 row, not a trend. |
| 4 | Read the verifier's verdict, not just the author's; flag rounds without a spot-check | **acted** | Baseline is the admitted closure (`:933`); R17-V1..V5 are routed into C1 (`:951-968`) and into the `ReportSkeleton` disposition table; `corpus/lessons/round-{12..17}-verifier-spotcheck.md` all exist (no round lacks one now); `w1/reports/CriticC1.md` is the in-round adversary applying the same posture. No new "flag a missing closure" mechanism was added; the standing rule did the work. |
| 5 | Draft a post-ceiling coverage rubric for João to judge | **acted, shape-changed** | C2 uses rubric V unchanged, P3 Walker + P5 themes (`:961-968`), not the suggested "observed-behaviour confirmations … operator-cleared" (impossible under the host pause). Operator judgement stays at admission. Same shape-change as round 17's P6/P4. |
| 6 | Reproduce hermetic receipts independently, with João's OK | **open / operator-gated** | No João OK is recorded, and no independent reproduction exists. `gen_w1.py:69` makes `harm-watch.sh` lane self-verification with RECEIPT headers; that is not the reflection's sandbox run. The receipt header is the lane-side precondition that makes reproduction possible (see §6), but the independent act remains operator-gated. |
| 7 | Machine-readable per-round digest (claims, verdicts, incidents, receipts) | **open / operator-gated** | No digest artifact and no consumer. `w1/spec.json`, `w1/dispatch.json`, `w1/record.json` are wave plumbing; `SCORECARD`/drafts are prose. The reflection itself says "a repo change, so it's João's call" (`2026-10-20.md:56`). |

**Which stay operator proposals.** 10-19: #3 (brief), #4 (live run), #7
(reflection tooling) are open; #1/#2/#6 are acted or partial; #5 is acted.
10-20: #2 and #3 are open/partial, #1 is open on the reflection, #6 and #7 are
operator-gated, #4 and #5 are acted. Nothing in either file is the *ground* of a
round-18 claim: C1's ground is `round-17-verifier-spotcheck.md` §6, C2's is the
arc ledger plus the PROVINCE surfaces, C3's is the R17-V4 interface.

## 4. What the round's claims actually take

- **C1 calibration.** Takes the *posture* of 10-20 #4 (the closure's verdict is
  the input), not its text. The routed defects are cited from the spot-check,
  not from the reflection. This is correct; citing the reflection in QUALITY
  would be the reverse of criterion 23's defect.
- **C2 coverage.** Takes the targets of 10-19 #6 and the shape of 10-20 #5:
  P3/P5, documentary only. It does **not** deliver the walker live rows, theme
  live rows, or the theme mutant that 10-19 #6 also names. Any report sentence
  that says "walker covered" without "documentary; host binary `[UNK]`" imports
  the reflection's over-read.
- **C3 operability.** Adjacent to 10-20 #1, not identical: #1 scans prose for
  command tokens; C3 replays committed tool-call bytes and compares a finding
  multiset. The frozen replay is detection after the fact, not prevention and not
  R15-V1 remediation. Calling C3 "#1 acted" would be a receipt cited for a token
  it does not carry.

## 5. Contradictions, stated

1. **Contract-level `Capabilities` / `Saturation` vs round-local annexes.**
   `SCORECARD.md:200-206` says "— none yet —" and `:208-210` says saturation is
   "to be declared … on its next round", while `:270-274`, `:304-311` and
   `:915-919` contain the declaration and five capability rows. 10-19 #1 and #2
   are therefore true in the annexes and false in the section the reflection
   pointed at. No count moves either way; L1 owns the section.
2. **C3's acceptance receipt fails the round's own criterion 24.** The frozen
   verdict payload (`tools/mado-tripwire.py:858-877`) carries `tool_sha256` but
   **no `measured_commit`**. The criterion-24 draft
   (`drafts/QualityDraft.md:3-4`) requires both on a scan/selftest/measure receipt
   a sentence relies on; `receipt-check.py` classifies a receipt without either
   as `MISSING_PROVENANCE`. Nothing produces a frozen receipt:
   `harm-watch.sh` has no `--frozen` (grep, 0 hits), `gen_w1.py` names no frozen
   evidence path, and `drafts/ScoreResultsDraft.md` leaves every frozen row
   `[PENDING]`. As it stands, the report sentence "frozen run exit 0
   `frozen_match`" would rest on a file its own new criterion would reject —
   R17-V1's class recurring in the round that fixes it.
3. **One criterion, two checkers, two paths.** QualityDraft cites
   `.ufo/waves/round-18/checks/receipt-check.py` (and `checks/mutant-check.py`,
   `checks/pipe-rc-*`); the executor landed `.ufo/waves/round-18/receipt-check.py`
   (+ `receipt-claims.json`, `measure-mutants.py`, `pipe-rc-census.py`);
   `drafts/SkillRegistryDraft.md:25` cites the executor path. `checks/` does not
   exist at snapshot. The two receipt checkers do not mean the same thing:
   QualityDraft's `RECEIPT...` form scans text for the two fields and exits 1 on
   any miss; the executor's claims form exits 0 when every claim meets its
   `expect`, including claims that expect `MISSING_PROVENANCE`, and binds the
   digest to `git show`. `w1/reports/CriticC1.md` §2 (criterion 24,
   counterexample 1) already flags the interface/file mismatch. Sibling
   `SiblingOverlap18` is chartered for the overlap; the consequence here is C1's:
   the QUALITY text must name the landed checker and describe its semantics.
4. **C1's target is contested, so reflection suggestions must not pad it.**
   `w1/reports/CriticC1.md` finds C1 "partly count inflation" as drafted: the
   literal counter rises for any appended numbered line containing `lessons/`
   (its §1 table: three one-line restatements reach 18/26). None of the 14
   reflection suggestions is a lesson, so converting any of them into a QUALITY
   row would add a false citation to raise the fraction. If the criteria are
   folded to avoid restatement, C1 may land below 18/26; that is the honest
   outcome, not a reason to import the reflections.
5. **Dated facts must not be imported.** See §1.2: 10-20's round-16 admission and
   missing-spot-check lines were falsified sixteen minutes after the file
   landed. 10-19's "no round ran" was true only for its window.

## 6. Proposed move (one, bounded)

**Give C3's acceptance run the receipt its own criterion demands, at the last
tool commit.**

Why this and not something larger: it is the one measurement in the round that
no item produces and no seat receipts, it is the round's own headline capability
evidence, and it makes criterion 24 self-applying on production bytes instead of
only an authored fixture plus legacy reds. It also completes the lane-side
precondition of 10-20 #6 (a third party can derive the tool bytes and re-run the
argv) without claiming #6 done.

Steps (L1, at integration):

1. Let `T` be the commit that finalizes `tools/mado-tripwire.py` — after
   `TwFrozenMode` and any accepted `TwMiss*` patch. Do not write the receipt
   before `T`.
2. Run from a worktree whose tool bytes equal `T`:
   `python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen-tripwire`
   Capture stdout byte-exact to `.ufo/waves/round-18/evidence/frozen-match.txt`
   (first line `MADO_TRIPWIRE_FROZEN: frozen_match`) and capture the exit
   separately; do not append anything to the raw file.
3. Write `.ufo/waves/round-18/evidence/frozen-match.receipt.txt` whose leading
   lines are standalone so both checker dialects accept them:
   ```
   RECEIPT tool=tools/mado-tripwire.py
   tool_sha256=<sha256 of tools/mado-tripwire.py at T>
   measured_commit=<T, 40-hex>
   utc=<date -u, Z>
   argv=python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen-tripwire
   exit=0
   stdout=evidence/frozen-match.txt
   stdout_sha256=<sha256 of the raw file>
   expected_sha256=<from the verdict JSON>
   ```
   followed by the raw stdout. (A JSON receipt with `tool_sha256` /
   `measured_commit` keys is the alternative the executor checker also accepts;
   the header form is the one the QualityDraft variant's regex accepts too.)
4. Commit the receipt at `R` (a child of `T`; `R` may be the integration
   commit). Add to `receipt-claims.json`:
   `{"id":"r18-frozen-match","receipt":".ufo/waves/round-18/evidence/frozen-match.receipt.txt","rev":"<R>","tool":"tools/mado-tripwire.py","expect":"ok"}`.
   `measured_commit` stays `T`, because that is the revision whose tool bytes
   produced the output; `rev` is only where the receipt text is read.
5. Optional in the same wrapper family: the tampered-copy control
   (`snapshot_tampered`, exit 2) can carry the same header. It is not required
   for this move.

Axes and harm:

| Axis | Effect | Harm |
|---|---|---|
| C1 calibration | Criterion 24 gets a production green from the round's own bytes (today its green is `r18-fixture-ok`, an authored fixture, plus red legacy receipts). No count change: the literal fraction stays whatever L1 lands. | none |
| C3 operability | The gate's primary evidence becomes commit-bound; a non-author can recompute `git show T:tools/mado-tripwire.py`, compare the digest, and re-run the argv over the committed snapshot. The registry row's move to `gate` then rests on a receipt, not prose. | none |
| C2 coverage | none | none |

Cost: two evidence files plus one claim entry. No tool behaviour, no QUALITY line,
no denominator, no host operation, no new dependency.

Risks:

- **Sequencing.** If the tool is edited after `T` without a re-cut, the claim
  fails `SHA_MISMATCH`. That is the designed alarm, but it means the run must be
  the last measurement of the tool.
- **Classifier changes force a re-pin first.** If an accepted `TwMiss*` rule
  changes what the classifier finds on the snapshot, `expected.json` (including
  `known_misses`, where a firing known-miss forces a re-pin by design) must be
  re-derived at `T` before the receipt is written. Otherwise the frozen run
  legitimately reports `frozen_verdict_mismatch`, and that is a finding to
  record, not a receipt to hide.
- **The checker is narrower than the receipt.** It binds digest↔commit only;
  `argv`, `exit` and `stdout_sha256` are informational unless another check reads
  them. Do not claim the checker proves the command ran.
- **Dialect choice.** If L1 adopts the QualityDraft `checks/` checker instead of
  the executor's, the header form still satisfies its regex but the claims file
  is ignored; state which checker the QUALITY text names.
- **Scope reading.** If criterion 24 is read as governing corpus claim admission
  only (`corpus/QUALITY.md:24`), the receipt is still a C3 improvement at one
  file's cost; it harms no axis either way.

Verification (to run once, at integration; not run here):

```text
python3 -I .ufo/waves/round-18/receipt-check.py
  -> RECEIPT r18-frozen-match ok; summary evaluated count +1; exit 0 once the
     six PENDING-L1 re-cuts are filled
git show <T>:tools/mado-tripwire.py | sha256sum          == tool_sha256
sha256sum .ufo/waves/round-18/evidence/frozen-match.txt  == stdout_sha256
head -1 .ufo/waves/round-18/evidence/frozen-match.txt    == MADO_TRIPWIRE_FROZEN: frozen_match
```

Red controls on a copy of the receipt: set `measured_commit` to `f71ccbe…`
(tool `7a98720e…`) while keeping the landed digest → `SHA_MISMATCH`; delete
`tool_sha256` → `MISSING_PROVENANCE`. The same two shapes the round already
authored as fixtures, now on the round's own receipt.

What the move does **not** do: it does not prevent host actions (the tripwire
docstring is explicit), does not remediate R15-V1, and does not prove snapshot
provenance — the tool says provenance is the snapshot author's claim;
`frozen-provenance-check.py` is the separate check.

## 7. Evidence anchors

Read-only commands used (all at the snapshot above):

```text
git log --oneline -12 --decorate                     -> HEAD d3a0000
git log --format='%h %ad %an %s' --date=iso -- considerthese/
  -> 8e0c9b2 / f898e52, both João Pedro Veiga
grep -c considerthese {LOG,SCORECARD,PROVINCE,README,SKILL,corpus/QUALITY,corpus/SOURCES}
  -> 0 each; corpus/lessons/: only round-16-verifier-spotcheck.md contains the token
grep -n "^## " SCORECARD.md                          -> no debt table; annexes at 304, 915
grep -n "frozen" .ufo/waves/round-18/harm-watch.sh   -> 0 hits
grep -n "evidence/frozen" .ufo/waves/round-18/gen_w1.py -> 0 hits
python3 -c 'json.load(receipt-claims.json)'          -> 15 claims, none r18-frozen-*
sha256sum tools/mado-tripwire.py                     -> 762cf56f… (snapshot, uncommitted)
git show d9a5a18:tools/mado-tripwire.py | sha256sum  -> 962919ce…d5aaa072
```

Pre-registration text: `SCORECARD.md:931-984` (C1 at `:951-960`, C2 at
`:961-968`, C3 at `:969-977`, separability at `:979-981`, cold-start facts at
`:933-949`). Source-class slot: `LEARNING.md:50-51`. Prior join:
`round-17/w1/reports/ConsiderTheseJoin.md`; its label landed at
`.ufo/reports/round-17/mado.md:46`, its mapping did not.

## 8. Limits and `[UNK]`

- PR #1 merge state `[UNK]` — GitHub was not read; the reflection's "still open"
  line is a dated claim, not re-derived here.
- `SHONEN.md` promotion `[UNK]` — promotion is operator-owned; the spot-checks
  exist but the round-17 closure does not assert independence.
- Wave-1 values (tool shas, `receipt-claims.json` contents, draft paths) are
  snapshot values; L1 verifies once after integration.
- No lane gate, live gate, host command or package query was run. No tool was
  installed or updated.
