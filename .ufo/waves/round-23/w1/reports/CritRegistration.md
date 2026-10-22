# CritRegistration — attack on the round-23 registration

Seat: `MadoR23.CritRegistration` (critic, leaf). Target: `.ufo/waves/round-23/registration.md` at lane
`master` = `a28e4815aabfa85f55274884000fb2608355f8cf` (registration commit `6b383c4`, append-only
clarification `a28e481`; `git diff e33ea304 a28e481 -- tools/` is empty, so no production edit yet).
Checked against `.ufo/prompts/mado-round-23.md` §6.9, `MANIFEST.json` `rounds[400]` and `rounds[426]`
(read with python `json`; not edited), AXES.md, PROTOCOL.md and the goal file's D11 ruling.

Write scope used: this file only. Gaming probes ran in a throwaway clone under `/tmp/critreg-*`
(local commits there only, deleted afterwards). Tool installs/updates: none.

## Verdict summary

| # | Finding | Severity | Kind |
|---|---|---|---|
| F1 | H2 disclosure misattributes 2 of 9 cases and doesn't separate the 6 r21-introduced regressions from the 3 round-20 misses | High | fixable (disclosure) |
| F2 | D11 says "the round's first claim repairs its routed harms"; C1 explicitly leaves the routed H2 unrepaired without citing D11 | High | judge's call: tradeoff to be disclosed, not fixable by wording alone |
| F3 | The precision guard "166/175 with the same passing set" treats any precision improvement as a harm | High | fixable (guard wording) |
| F4 | C3's counter is satisfied by a scope-free bare mention (live in base: `mado-verify.sh`) | High | fixable (counter) |
| F5 | C3's counted object is AXES' *coverage* signal; the count ignores the self-assessment mark, which risks C2+C3 being read as two coverage claims | Medium | fixable (declaration) |
| F6 | C3's "read-only scope" append can silently absorb contested transcript/pacman ground (adjacency harm, box-4 bleed) | Medium | fixable (append content) |
| F7 | C2's counter reaches 3/3 from one generic source plus a "Footnotes" doc, with no route or path | High | fixable (counter) |
| F8 | C1 can be gamed by suppressing unparsed counters; the corpus guard doesn't cover unparsed-counter changes | Medium | fixable (guard wording) |
| F9 | Routed defects missing from the H-table: r426 (1) census W04 omission, (4) M6/M11/M13 conformance debt; M13 recurs as H3 vs C1 | Medium | fixable (table rows) |
| F10 | Counters and guards as written read working-tree bytes, and several guards have no command | Low–Medium | fixable (commands) |
| F11 | C1↔C3 coupling through `tools/` population; C3's counter is blind to nested tools; git errors exit 1 (same code as "mismatch") | Low | fixable |

Verified sound (no finding): C1 before value 6/12 (re-run below); the four r22 supplemental fixtures
are byte-identical copies (`cmp`); `expected.json` sha256 = `53e34d26…c6b9` as registered; the repair set and
receipts landed before any `tools/` change; the 1356-file corpus comparator reads a frozen snapshot
(`round-21/corpus/snapshot/manifest.json`, 1356 files all under `.ufo/`), so C2 and C3 edits can't
perturb it; C3's lowest-axis citation 7.1875 re-derives (`round-17/measure.py e33ea304` → c1 23/32 = 7.1875);
host trees `~/.config/{foot,kitty,ghostty}` exist (`ls -d`); C2 before 0/3 and C3 before 4 reproduce.

---

## F1 — The H2 disclosure is not accurate (High, fixable)

**Counterexample.** The registration says: "Of its nine disagreements, five are strict VCS index-write
readings (`git commit --dry-run` forms, a `jj $c` variable verb) and three are reset-cleared helper leads
that round 21 changed deliberately; one is a class-method instance case."

**Evidence.**
- At base the 9 failing cases (`round-22/evidence/resume/precision-final.json`, tool `cd9da20c`) are 5 H-family
  vcs_write false positives, 3 L-family missing leads and 1 W-family case.
- Three of the nine were already failing at round 20 (172/175), per `round-20/evidence/precision-final.txt`
  @ `28c68378`: `W-CaseWrapperForms-class-method-instance`, `L-AdoptW2-AdvHelperFn-b14` and
  `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help`. Round 21's own review says the same thing
  (`round-21/residual/FinalEvidenceReview.md:150`: "Three are the round-20 misses … Six are new").
- So the routed harm H2 (the drop from 172 to 166) is six cases:
  - Four `git commit` dry-run forms. Round 21 deliberately made these strict, citing S118
    (`corpus/lessons/round-21.md:32`, `FinalEvidenceReview.md:151`).
  - Two reset-cleared leads, adjudicated `false_positive_removed` in
    `round-21/evidence/final/corpus-adjudication-a6cef89.json`.
- `b14` is not a reset-cleared helper. Its fixture
  (`round-20/precision/CaseAdoptW2--AdoptW2-AdvHelperFn-b14.jsonl`) is an uncalled `def run_all(run_case)`.
  So "three reset-cleared helper leads that round 21 changed deliberately" is wrong for one case, and
  `jj $c` is not a round-21 change.
- The class-method-instance case is a **false observed** `pacman -Q`. That is the same defect type C1
  repairs, and the registration doesn't mention it.

**Axes:** calibration (false provenance), operability (harm accounting).

**Smallest fix.** Before any after-measurement, add an append-only clarification:

> H2 = 6 r21-introduced disagreements: 4 git dry-run commit forms (strict index-write reading, S118;
> FinalEvidenceReview.md:151) and 2 reset-cleared lead removals (corpus-adjudication-a6cef89.json,
> false_positive_removed). The remaining 3 failures are round-20 misses outside H2:
> class-method-instance (a false observed), b14 (an uncalled-helper lead) and the `jj $c` variable verb.

Drop "Which of those historic wants is right is not settled here" for the six. Round 21 recorded sourced
or adjudicated reasons for them; say whether round 23 accepts or contests those reasons.

## F2 — The D11 recovery ruling vs. the H2 non-repair (High, the judge must weigh it)

**Counterexample.** Goal file `.scratch/goal-20261022-hyaku-12h.md:215-218` (D11, which the registration
invokes) says: "The round's first claim repairs its routed harms. If that round is rejected, restore
`blocked/<lane>`."

`rounds[400].verification.rechecks` routes the precision drop as an "independent second precision harm".
The registration's C1 turns H2 into a no-worse guard and never cites the D11 clause.

**Axes:** operability (harm left standing), calibration (an unstated conflict with the governing ruling).

**Assessment.** This is not a wording defect. If the judge holds D11 literally, C1 can't satisfy it while
H2 stays unrepaired. The registration should say so, not leave the conflict for the closure to discover.

**Smallest fix.** Append one sentence: "Under D11 the first claim does not repair routed harm H2; the
round asks the judge to rule the six r21-introduced cases want-errors (F1 evidence) or to count H2 as
unrepaired." Also file the matching L0 line. Don't add a new target, because that inflates the claim count.

## F3 — The precision guard penalises improvement (High, fixable)

**Counterexample.** Guard: "precision 166/175 with the same passing set". "A guard failure is a harm."
C1 targets false observed rows from caller frames and bindings. If the patch also fixes
`W-CaseWrapperForms-class-method-instance` (a false observed `pacman -Q`, see F1), precision becomes
167/175 with a different passing set. As written, that is a guard failure, and therefore a harm.

**Evidence.** The committed comparator already has the right predicate:
`round-22/evidence/resume/precision-comparison.json` keys `previous_passing_losses` (list) and
`fixed_population_equal`.

**Smallest fix.** Re-word the guard as "175 fixed cases; `previous_passing_losses == []` against base
`cd9da20c`; passed ≥ 166". Any newly passing case is recorded, not counted as harm.

## F4 — C3's counter is satisfied by a scope-free mention (High, fixable)

**Counterexample (live in base).** PROVINCE.md names `mado-verify.sh` only inside a round-19 parenthetical
gate reference ("gate `theme_plane()`/`omarchy_plane()` in `tools/mado-verify.sh`"), with no tool-scope
statement. The counter already credits that as named, which is why the before value is 4 and not 5.

**Exercised.** In the scratch clone at `a28e4815`, I appended one PROVINCE line:
`Not reviewed for scope: mado-action-plan.py, mado-assessment.py, mado-evidence-audit.py, mado-tripwire.py.`
Committed, then ran `python3 -I .ufo/waves/round-23/c3/count.py HEAD`:
- base: `4 ['tools/mado-action-plan.py', 'tools/mado-assessment.py', 'tools/mado-evidence-audit.py', 'tools/mado-tripwire.py']`
- after the scope-free (even negative) line: `0 []`

The registration promises "an append-only PROVINCE refinement that states each tool's actual read-only
scope". That universal clause is wider than the counter, which tests `Path(p).name in province`
(substring anywhere).

**Axes:** calibration (a counter that can be gamed).

**Smallest fix.** Tighten the counter before after-measurement. Count a tool as named only when
PROVINCE.md holds a table row whose first cell is exactly `` `tools/<name>` `` and which has non-empty
`reads`, `writes` and `owner/adjacent` cells. Either list `mado-verify.sh` explicitly as covered by
such a row, or re-state before = 5. Tightening is not narrowing, and the clarification precedent
already exists in `a28e481`.

## F5 — C3 measures a coverage signal, and the count ignores the self-assessment (Medium, fixable)

**Counterexample.**
- AXES.md:12 defines coverage's expert signal as "PROVINCE.md lists every surface", with surfaces
  including "repo paths, tools".
- C3's cure is exactly that: make PROVINCE list every tool. C2 is also coverage.
- `c3/count.py` matches box 4 with `^- \[[ x~]\] `, so the count doesn't depend on whether the lane
  asserts the box at all.

**Exercised.** In the clone I flipped box 4 to `- [ ] No cross-domain bleed …`. The counter still reports
`4` and quotes the unasserted box as the "self_assessment". The number depends only on PROVINCE and
`tools/`, not on the self-assessment.

**Axes:** calibration and coverage. AXES.md says two claims on one axis count as one. If the judge
re-classes C3 as coverage, the lowest-axis obligation (calibration 7.1875) goes unmet.

**Smallest fix.** Append a clarification:
- C3 counts a mismatch only while box 4 is marked `[~]` or `[x]`.
- The admissible cures are (a) PROVINCE rows per F4, or (b) downgrading box 4.
- The PROVINCE append adds no new owned domain surface, so C3's coverage verdict is `unchanged`.
- Name the SCORECARD row C3 updates (a new `calibration / box-4 tool mismatches` sub-row), and state
  that QUALITY c1 7.1875 is not moved by C3.

## F6 — The C3 append risks silent absorption of contested ground (Medium, fixable)

**Counterexample.**
- `tools/mado-tripwire.py:2` is "post-hoc tripwire over OMP session transcripts", classifying
  host_mutation, package_query, vcs_write and tool_install.
- mori owns "passive terminal-at-scan transcript observation" (`mori-shokunin/PROVINCE.md:103`).
- tsukuroi owns pacman state (`tsukuroi-shokunin/PROVINCE.md:8`).
- mado's domain is "desktop & compositor craft".

Writing the tripwire into mado's PROVINCE as owned scope would make PROVINCE "accurate" by declaring the
bleed that box 4 denies. PROTOCOL says contested scope is "reported, never silently absorbed", and
LEARNING says the province "grows by evidence, not by declaration".

The "read-only" wording is also inaccurate as stated:
- `mado-action-plan.py:702-763` writes a TemporaryDirectory in selftest.
- `mado-assessment.py:195`, `mado-evidence-audit.py:244` and `mado-tripwire.py:3320` spawn subprocesses.

**Axes:** adjacency (harm risk) and calibration (false provenance).

**Smallest fix.** The append classifies each tool as a lane-internal evidence instrument, not a domain
surface. It states: no substrate or config writes; selftest writes only a private temp dir. For the
tripwire it names mori (transcript observation) and tsukuroi (pacman state) as Adjacent, and the
lane report flags it as contested scope.

## F7 — C2's counter reaches 3/3 without three sourced routes (High, fixable)

**Exercised.** In the scratch clone at `a28e4815` I appended two SOURCES rows:
- `S901 | Arch Wiki List of terminal emulators (foot, kitty, ghostty) | … | mined | 2026-10-22`
- `S902 | Markdown guide: Footnotes | … | mined | 2026-10-22`

The note `corpus/knowledge/terminal-trees-r23.md` contained only `| foot | S902 |`, `| kitty | S901 |`
and `| ghostty | S901 |`. Running `python3 -I .ufo/waves/round-23/c2/count.py HEAD` gives
`"count": "3/3"`, exit 0. Base is `0/3`.

Three counter defects:
1. Substring match: `term in src["source"]`, so "Footnotes" counts for foot.
2. One generic source can satisfy all three terminals.
3. No config path or route content is required, and `used-by` linkage isn't checked. The r17 rubric's
   c2 does check `used-by`.

The census (`scripts/sources-census.sh`) checks enums and that `used-by` paths exist, not relevance
[INFERENCE from its header E/W code list].

The claim says "sourced routes for the foot, kitty and ghostty config trees", which is wider than the counter.

**Context the note must carry.** `pacman -Q foot kitty ghostty` → "not found"; only `alacritty 0.17.0-1`
is installed. The trees are declarations with no installed consumer, so the note must not claim live
behaviour.

**Axes:** coverage (a counter that can be gamed) and calibration.

**Smallest fix.** Append a clarification tightening `count.py` before after-measurement:
- word-boundary match `\b<term>\b` on the source cell;
- a distinct S### per terminal;
- the S### row's `used-by` names `corpus/knowledge/terminal-trees-r23.md`;
- the route row carries a cell containing `~/.config/<term>/`;
- the source cell or anchor is on the terminal's upstream (codeberg.org/dnkl/foot,
  sw.kovidgoyal.net/kitty or github.com/kovidgoyal/kitty, ghostty.org or github.com/ghostty-org/ghostty).

## F8 — C1 can pass by suppressing unparsed counters (Medium, fixable)

**Counterexample.** The C1 before run (below) shows two of the six failing cases,
`ForwarderPassesCallerArgument` and `ForwarderInvokesFactoryClosure`, fail only because `unparsed == 1`;
their rows already equal the want. `ForwardExistingClosure…` and `ForwarderInvokesCallback` also carry
`unparsed 1`.

A patch that stops counting `unparsed_spawns` at forwarder sites, without resolving them, flips both of
those cases to pass. The guards wouldn't catch it:
- None of the r21 oracle, r22 primary or r22 residual-truth expected files pins a nonzero unparsed
  value (regex scan: 0 nonzero).
- The selftests pin only eval-level unparsed cases (`eval-nonliteral-unparsed-clean`,
  `eval-memoryerror-is-unparsed`, `unparsed-pacman-operator`).
- The corpus has 132 files with `unparsed_spawns: 1` at base, but the registration's corpus guard
  names only "added or removed finding group[s]" and "error flips", not counter changes. Round 22's
  own scorecard did track "eight reduced unparsed counters".

**Axes:** operability (an honesty signal lost).

**Smallest fix.** Widen the corpus guard: every changed `unparsed_spawns` or `eval_unparsed` value
against base is listed and adjudicated. A reduction is admissible only when the spawn now resolves to
a row or is proven non-spawn. Zero unadjudicated counter reductions.

## F9 — Routed items missing from the H-table (Medium, fixable)

`rounds[426].notes` "Defects routed" and how the registration handles each:
1. "report's pasted End census omits the S121 W04 line … correct next report": **absent**. Add a row
   whose re-measure is: the round-end report pastes `sources-census.sh validate` output byte-equal to
   its receipt, including every W04 line.
2. Normalized expectations committed after implementation: answered in the preamble only. Add a row
   with a one-command check, e.g. `git merge-base --is-ancestor 6b383c4 <first commit touching tools/>`.
3. The three detector defects: covered (H3 and H4).
4. Conformance debt M6 (shared-checkout harness writers), M11 (W2 scope overruns) and M13 (overlapping
   comparators): **absent**. M13 recurs in this registration. H3's
   `round-22/residual-truth/measure.py` and C1's repair set score the same four byte-identical fixtures
   (`cmp`: all four `same`), so there are two comparators over one population. Name the repair set as
   the counter of record for H3, or state that H3 is a view of four of C1's cases. Add M6 and M11 rows
   pointing at the wave contract's clone-only and absolute-path bounds.

`rounds[400]`: F1–F5 (H1) and the precision drop (H2) are covered, H2 with the F1/F2 defects above.
`rounds[426].outside_spotcheck[3]` (the v3 recall loss) is covered as H5.

## F10 — Not "one command over committed bytes" as written (Low–Medium, fixable)

- C1, H1 and H3 commands pass `--tool tools/mado-tripwire.py`, which is working-tree bytes. In this
  jj-colocated lane git HEAD is detached and `@` may hold uncommitted edits.
- `measure.py` pins `expected.json` and the fixtures, but only *reports* the helper sha
  (`round-21/oracle/measure.py`, currently `4eb893d2…`, last touched `b96d1b8`). It doesn't assert it.
- Guards with no command in the registration: "eleven legacy selftest suites 247/247" (receipts exist
  as `round-22/evidence/resume/selftest-*.json` ×11) and "resource populations clean" (receipts
  `resource-api.json` and `resource-cli.json` via `replay.py --mode resource-*`, plus
  `round-22/resource-closure-measure.py`).
- The "every … adjudicated" corpus clause rests on author prose, not a command.
- "No tool is removed" has no command.

**Smallest fix.**
- Counter of record: `git show REV:tools/mado-tripwire.py > $T && python3 -I .ufo/waves/round-23/repair/measure.py --tool $T`, run in a clean clone at REV.
- Pin `HELPER` sha `4eb893d2…` in `measure.py`, or record it as a guard.
- List each guard's exact command and its base receipt path.
- "No tool removed": `git diff --diff-filter=D --name-only e33ea304 REV -- tools/` must print nothing.

## F11 — Smaller C3 counter defects and C1↔C3 coupling (Low, fixable)

- `git ls-tree --name-only REV tools/` is non-recursive. Exercised: adding `tools/lib/frame.py` leaves
  the count at 4, with the new file absent from `tracked_tools`. Conversely, if C1 adds a top-level
  `tools/*.py` helper, C3's count rises: the claims are coupled through the `tools/` population. Fix:
  use `ls-tree -r`, and state that C1 modifies only `tools/mado-tripwire.py`.
- On a git failure, `count.py` raises `SystemExit(<json string>)`. Exercised with REV `deadbeef`: it
  printed `{"error": "git show deadbeef:SHONEN.md failed"}` and exited 1, the same code as "mismatches
  present", while the docstring reserves 2 for cannot-evaluate. Fix: print the JSON, then `sys.exit(2)`.

C1↔C2 and C2↔C3 are causally separable: they touch disjoint files, and the corpus comparator population
is frozen.

## Commands run (exact) and outputs

- `python3 -c "import json; r=json.load(open('MANIFEST.json'))['rounds']; …r[400], r[426]…"` →
  `rounds[400]` round 21 rejected-harmed (operability harmed; precision 172→166 "independent second
  precision harm"); `rounds[426]` round 22 rejected-honest-stop with routed defects (1)–(4) as quoted in F9.
- `git -C <lane> show e33ea304:tools/mado-tripwire.py > /tmp/critreg-base-tripwire.py` → sha256
  `cd9da20c…ea84`, then `python3 -I .ufo/waves/round-23/repair/measure.py --tool /tmp/critreg-base-tripwire.py`
  → `6 12`, exit 1. Passing: ReturnedGlobalHelper, CallerArgumentBeforeClosureOverlay,
  NestedDefReadsDefiningFrame, LateGlobalRebinding, CallbackStoredInDict, CallbackStoredOnAttribute.
  This matches `evidence/repair-before-e33ea304.json`. (One harness child per case, 384 MiB / 15 s, via
  the round-21 helper.)
- `for f in round-22/residual-truth/*.jsonl; do cmp "$f" round-23/repair/fixtures/$(basename $f); done`
  → all 4 same.
- `sha256sum round-23/repair/expected.json` → `53e34d26…c6b9`.
- `python3 -I .ufo/waves/round-17/measure.py e33ea304` → `c1 criteria 32, lesson_cited 23, score 7.1875`.
- `python3 -I .ufo/waves/round-23/c3/count.py <rev>` in the clone: base `4`; scope-free line `0`;
  box `[ ]` still `4`; nested tool still `4`; bad rev exit 1.
- `python3 -I .ufo/waves/round-23/c2/count.py <rev>` in the clone: base `0/3` exit 1; gamed `3/3` exit 0.
- `pacman -Q foot kitty ghostty alacritty` → three "not found", `alacritty 0.17.0-1`;
  `ls -d ~/.config/{foot,kitty,ghostty}` → all three exist.
- Precision split read from the committed receipts (`round-22/evidence/resume/precision-final.json`,
  `round-20/evidence/precision-final.txt`, `round-21/evidence/final/precision-legacy-a6cef89.json`). I did
  not re-execute `tw-precision.py`; the 166/175 base value rests on those receipts and on the r426 closure.

## Verdict

**Registration admissible only after an append-only, pre-measurement clarification.**
- Correct the H2 disclosure (F1) and acknowledge the D11 conflict (F2).
- Make the precision guard tolerate improvement (F3) and cover unparsed-counter changes (F8).
- Tighten the C2 and C3 counters (F4, F7) and declare C3's axis separation (F5) and adjacency handling (F6).
- Add the missing routed-defect rows (F9) and pin the commands to committed bytes (F10, F11).

F2 is the one item the canonical judge must rule on. The rest are fixable without narrowing any target.
