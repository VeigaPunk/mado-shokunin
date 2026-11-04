# R70CriticClaims — round-70 frozen-claims falsification

Audit snapshot: HEAD `f754347a` (2026-11-03 23:40:01 -0300) while the wave still ran; the evidence
below is read at immutable revisions — freeze `bc18399b` (23:27:05), instruments `5144a6b5`
(23:29:46), measured content `5adba5a9` (23:33:01). Every command pins `--rev`; no lane command ran
against a moving worktree. Scratch `/fast/scratch/hyaku/mado-r70/R70CriticClaims/` was removed
before this report was yielded.

## Blockers

### B1 — the C1 counter cannot produce the frozen sentence at the wave's scored revision (BLOCKER)

`quality/counters/c1-r70-real-children.py:251-254` at `5144a6b` calls
`subprocess.run(..., cwd=scratch)` with no `os.makedirs(scratch)`; `measure()` creates only `work`
(lines 266-269), never `work/cand-<mode>`.

```
D=$(mktemp -d /fast/scratch/hyaku/mado-r70/R70CriticClaims/b1.XXXX); cd /home/vgpnk/Projects/shokunin/mado-shokunin
git show 5144a6b5f43225d8021a469f4d24c19558026b9e:quality/counters/c1-r70-real-children.py > "$D/rc.py"
python3 -I "$D/rc.py" --repo . --rev 5144a6b5f43225d8021a469f4d24c19558026b9e \
  --base-rev b37a5aec4ea03f2223d8e09dd5d386d055c24179 --scratch-root "$D/s"
# rc=1; FileNotFoundError: .../r70-c1/cand-genuine (traceback line 303 -> line 254)
# last stdout line: MADO_R70_FIXTURE mode=garbage ...; NO MADO_R70_REAL_CHILDREN line
```

The same file at `9508e878` (23:32:33) adds `os.makedirs(scratch, exist_ok=True)`; the git-extracted
`5adba5a9` file runs clean:

```
git show 5adba5a9:quality/counters/c1-r70-real-children.py > "$D/rc2.py"
python3 -I "$D/rc2.py" --repo . --rev 5adba5a9 --base-rev b37a5aec --scratch-root "$D/s2"
# rc=0; MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=1 verdict=TARGET_MET rev=5adba5a9…
```

The lane discloses this as `corpus/lessons/round-70.md:52` (M70-1) and ties it to criterion 110(a)
("a counter is frozen only after its declared command is run verbatim"). The disposition is honest;
the identity problem remains: the measured instrument is not the one committed at `5144a6b`, and
`9508e878` landed 50 s after `.ready` and 28 s before the first measurement.

### B2 — the declared harm watch is false at the measured content (BLOCKER)

Declaration `:128` claims `quality/landing-counters.sh --round 69` stays GREEN.

```
bash quality/landing-counters.sh --repo . --rev 5adba5a92a8d58eb76533b39a9216d8e85d48fbc --round 69 \
  --scratch-root DIR --citecheck-paths .ufo/waves/round-69/measurement-final-r69.txt
# rc=1
# LEDGER: population=119 ledger_rows=116 uncovered=3 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED
# LANDING_LEG ledger rc=1
# MADO_LANDING_COUNTERS: RED (nav=0 usedby=0 ledger=1 citecheck=0 rev=5adba5a9…)
```

Same RED at `5144a6b` (`--round 70`): the three new instruments are uncovered. GREEN appears only at
`71caa8b7` (ledger rows, 23:34:48 — after the 23:33:01 measurement):

```
bash quality/landing-counters.sh --repo . --rev HEAD --round 70 --scratch-root DIR \
  --citecheck-paths .ufo/waves/round-70/measurement-r70.txt
# rc=0; MADO_LANDING_COUNTERS: GREEN (nav=0 usedby=0 ledger=0 citecheck=0 rev=3aea1e10…)
```

The literal clause with no `--citecheck-paths` is not runnable: `--round 69` defaults to
`.ufo/waves/round-69/receipts`, which does not exist → rc=2 "citecheck path missing". So the
harm-watch sentence as written is neither the command that was run nor true at the REV it scores.

### B3 — the C2 do-nothing control cannot be run with the r69 instrument (MINOR; number holds)

```
python3 -I quality/counters/c2-r69-guard-dominance.py --repo . --rev 5144a6b --base-rev b37a5aec \
  --controls .ufo/waves/round-70/controls/c2-controls-r70.json --scratch-root DIR
# rc=2: controls file sha256 29947b4c… does not match the frozen digest
```

`c2-r69-guard-dominance.py:69,493` pins `975ca3ba…`; the declaration's § C2 Before points at the r69
*classifier*, not at an r69 *invocation*. The 13/17 is real and reproduced two ways — via a
`runpy.run_path(...)["classify"]` shim over the 17 sources and via the r70 counter's
`base_classify` leg (`c2-r70-carriers.py:779-789`) — with exactly `alias-carried`,
`attribute-carried`, `splat-carried`, `constant-key` missing. The receipt should name the shim.

### B4 — C1's declared source is neither the adopted row nor the quoted text (MODERATE; disclosed)

Declaration `:59-64` names CPython `Doc/library/subprocess.rst` @ `v3.14.8`, "the `returncode`
paragraph", and enumerates "a usage error, a signal death reported as `-N`, an ordinary missing
program". The paragraph at `:135-142` says only:

> "Exit status of the child process. Typically, an exit status of 0 indicates that it ran
> successfully. A negative value ``-N`` indicates that the child was terminated by signal ``N``
> (POSIX only)."

"missing program" is at `:716-717` under Popen's versionchanged note, not the returncode paragraph;
"usage error" is in neither. No row or Gate quotes that paragraph: S108 (`corpus/SOURCES.md:120`) is
scoped to `args`; `corpus/lessons/round-70.md:91-96` rejects the URL as a duplicate and substitutes
the held S435 (Bash exit status), and both knowledge entries rest on S435. The lesson's own flip
condition ("re-opens S108 as a superseding row … with the new anchor") concedes the row is the right
vehicle. The rule is grounded by S435; the declaration's named ground and its three-cause
enumeration are not what any row or Gate quotes, and the frozen sentence stays wrong. Record an
erratum against `:59` rather than letting the duplicate refusal read as if it disproved the need.

### B5 — C2's single-source sentence is one document off (MINOR; disclosed in the lesson Gate)

Declaration `:101-104` attributes both halves — `**` unpacking and "a subscript target stores under
the key expression's value, not its spelling" — to `expressions.rst`. `expressions.rst:482-506`
grounds `**` verbatim; `:1090-1101,1139-1145` says the subscript is an expression and subscriptions
may be assignment targets calling `__setitem__`, but does not state the assignment evaluation order.
That sentence is `simple_stmts.rst:190-192` (adopted as S440). `corpus/lessons/round-70.md:83-84`
already admits "the required sentence is **not** in `expressions.rst`". S439/S440 are committed at
`f754347a`; at audit time `corpus/SOURCES.md` still carried an uncommitted `used-by` edit, so the
registry diff was mid-landing.

### B6 — a printed evidence line names the wrong rule (MINOR)

`c2-r70-carriers.py:854` prints `(the round-68 rule must miss the target)` while the classifier run
is `c2-r69-guard-dominance.py` and declaration `:70` says "the held round-69 classifier". The
contract line is unaffected; the evidence line is mislabeled. (`5adba5a9` only added `leg=` labels.)

### B7 — the declaration's seat count is stale (MINOR)

Declaration `:6` says "One v1 wave of 13 seats"; `.ufo/waves/round-70/w1-spec.json` has 14 items
(`R70ExecC1Real` … `R70ConnSiblings`) and the dispatch accepted 14. The declaration is frozen; this
needs an erratum, not an edit.

### B8 — chronology (identity finding, not a freeze violation)

```
bc18399b 23:27:05  freeze (declaration + 17-case set + baseline + proto)
5144a6b5 23:29:46  instruments (3 files)
.ready   23:31:43
9508e878 23:32:33  C1 setup repair (os.makedirs)
5adba5a9 23:33:01  measured content (C2 leg labels)
71caa8b7 23:34:48  measurement receipt + ledger rows
3aea1e10 23:35:34  harm-watch receipt
f754347a 23:40:01  records (entries, S439/S440, QUALITY, scorecard)
```

Freeze < instruments < `.ready` < first candidate measurement — true on all four questions. But the
measured C1 counter is `9508e878`'s bytes, not `5144a6b`'s, and the measured C2 counter is
`5adba5a9`'s bytes: the receipt's `MADO_R70_CONTROL leg=candidate …` lines do not exist in the
`5144a6b` counter. If "scored instruments at `5144a6b`" is binding, C1 is unlanded at that revision;
if the measured content is the score, both claims are reproducible (verified). The canonical judge
owns that call; the evidence for either reading is above.

### B9 — substitution is only partly blocked; C2's risk is undisclosed (MODERATE)

- C1: always-`pass` (1/3, genuine) and always-`fail` (1/3, crash+garbage) genuinely fail. But a
  harness that reads the fixture lane's `MODE=genuine|crash|garbage` line — the template writes
  `MODE=@MODE@` into `quality/landing-counters.sh` at each scenario revision — and prints the
  expected `mz=` scores 3/3 without measuring anything; a counter that prints the contract line
  scores too. The measurement reads `mz=` only (`parse_mz`, counter `:166-175`); nothing observes
  *how* the decision was made. The knowledge entry discloses this
  (`corpus/knowledge/landing-kill-credit-real-children-r70.md:96-99`, "A stand-in that printed the
  expected `mz=` per fixture revision would score 3/3"); the declaration's "Not claimed" does not.
- C2: the seventeen sources are external and frozen and the population is re-derived with
  `git ls-tree` (`c2-r70-carriers.py:761-765`), but a classifier keyed on the seventeen `src`
  strings (or one that returns `(True, True)` for the four carrier names) scores 17/17; there is no
  held-out case. The entry's limits name `dict(**GUARD)` etc., not the hardcode risk. Measurement
  cannot block it because the counter is the only observer.

## Checks that hold (commands and exit codes)

- C1 measured content (git-extracted `5adba5a9` file): rc=0,
  `MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=1 verdict=TARGET_MET`. Base leg credits
  `mz=pass` for all three scenarios, so only `genuine` matches → `base_correct=1/3`. The 3/3 target
  is not reachable with the r69 harness.
- C1 fixture identity: the frozen `proto/fixture-lane.tmpl` rendered per mode hashes exactly to the
  receipt's lane sha256s (`96cf148e…`, `e8562c3f…`, `85dcd09c…`); the counter's embedded
  `LANE_TEMPLATE` equals the template after the placeholder normalization
  (`__MODE__` ↔ `@MODE@`). Fixture commit revisions vary per run (timestamps); the lane sha is the
  stable identity.
- C2 at `5144a6b`: rc=0, exact frozen line,
  `population=20 readers=13 guarded=13 unguarded=0 controls=17/17 base_controls=13/17`. The
  seventeen-case file hashes `29947b4c…`; the r69 file `975ca3ba…`; the eleven carried cases are
  dict-identical to the r69 cases (checked programmatically, `True`).
- C2 base: 13/17 (shim + r70 base leg). The 17/17 target is not reachable with the r69 classifier.
- Predicate-literal binding: both frozen contract lines equal the builders' output with the frozen
  values (C1 `3/1/TARGET_MET`; C2 `20/13/13/0/17/13/TARGET_MET`), character-for-character
  (`C1 equal: True`, `C2 equal: True`); both counters re-emit through their own `CONTRACT_RE`
  before printing.
- C1 harness: `mz_killed = bool(mz_rc != 0 and summary_shows_failure(mz_out))`
  (`c1-r70-landing-controls.py:478`); `summary_shows_failure` full-matches
  `MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions passed` with `n > 0`, `p < n` (lines 300,
  316-330). Harness selftest 68/68 rc=0.
- C2 re-derivation: `POPULATION_RE = ^quality/check-[^/]+\.py$` (line 74), population from
  `git ls-tree -r --name-only <sha> -- quality` (761-765), per-file `git show`, held-check asserting
  the r69 digest and the eleven carried cases at `--rev` (722-746).
- Separability: no cross-reads (`grep` for `c1-` in C2 and `c2-`/`controls-r70` in C1 → none);
  disjoint scratch roots (`r70-c1`, `r70-c2-carriers`); each ran alone successfully. Shared
  read-only input noted: `quality/check-tool-ledger.py` is a C1 fixture child and a C2 population
  member.
- Frozen r69 no-harm at the measured content: `c1-r69-landing-controls.py --selftest` 59/59 rc=0;
  `c2-r69-guard-dominance.py --selftest --controls <r69>` 43/43 rc=0;
  `c1-r69-paired-recipes.py --selftest` 28/28 rc=0; `c1-r69-paired-recipes.py --repo . --rev
  5144a6b --base-rev b37a5aec` → `killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET` rc=0; the r69
  harness and classifier are byte-identical between `b37a5aec` and `5144a6b` (`git diff --stat`
  empty).
- Gate: `bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 460/460` rc=0 (at `5144a6b` and
  `f754347a`). Landing `--selftest` → 62/62 rc=0.
- Axis: `python3 -I quality/check-axis-scores.py --rev 5144a6b --repo .` and `--rev HEAD` →
  navigation 81/81, calibration 86/86, operability 12/12, `checked=3 mismatched=0` rc=0.
- C2 selftest 49/49 with `--controls` (47/47 without), matching the harm-watch receipt.

## Axis attribution

C1 calibration / C2 operability is the r69 mapping (r69 SCORECARD row: C1 calibration, C2
operability); the label is inherited, and the published fractions do not move (81/81, 86/86, 12/12
at both `5144a6b` and HEAD). Surfaces actually changed: C1 edits the kill-credit branch of a landing
control harness and adds a real-child counter; C2 edits the `quality/check-*.py` guard classifier.
No misattribution against the r69 precedent. The declaration's posture numbers are correct (axis
gate 3/3, gate 460/460), and round 69 records a capability row with first-working round 69
(gap 0). The one attribution gap: `SCORECARD.md` § Saturation (`:211-213`) does not assert N=3 — it
defers the line and window to the lane's next round; N=3 lives only in the per-round posture
sentences. The declaration's "(window N=3, gap 0)" is grounded in the round-69 posture line, not in
§ Saturation.

## Claim sizing

- Targets are finite denominators (3 and 17); no target is universal. The universal-sounding wording
  is rule scoping, not coverage: "all six of `population==20…`" (a conjunction of frozen values),
  "All four still require one of the three dominance flows" (the rule's shape over the four added
  carriers), "Every published finite sub-axis…" (verified by the axis gate), "Neither reads the
  other's artifacts" (verified by grep; shared third-party input noted above).
- Kill rules are in the declaration committed 23:27:05, before the 23:33:01 measurement; the
  baseline receipt is 23:26:29, also before.
- `base_correct=1` is structurally forced for the specified repair: genuine rc=1 → base credits pass
  and expectation is pass; crash rc=2 → base credits pass, expectation fail; garbage rc=1 → base
  credits pass, expectation fail. A legitimate repair (`rc!=0` AND parsed `p<n`) cannot make it 0/3
  without changing genuine's exit status, and cannot make it 2/3 without a fixture deviating from
  the frozen crash/garbage definitions. The residual risk is a degenerate fixture, not a legitimate
  repair; the counter pins the three lane sha256s in the receipt and in its own selftest.
- No after-the-fact narrowing observed: the post-freeze instrument changes are the setup repair
  (`9508e878`) and the `leg=`/label edit (`5adba5a9`); neither touches the predicate, the counters,
  or the expectations.

## Sourcing

- C1: S435 (held, Bash 5.3 §3.7.5) grounds "nonzero is a process outcome with more than one cause"
  (126/127 execution failures, 128+N signals) and is what the entry and the lesson Gate use. It does
  **not** ground the declaration's specific "usage error / missing program" enumeration, and the
  named CPython `returncode` paragraph is not the passage that says those things. No row or Gate
  quotes the declared paragraph; the duplicate refusal is disclosed (lesson M70-3) with a flip
  condition.
- C2: S439 (expressions.rst:509-512) grounds `**` dictionary unpacking; S440
  (simple_stmts.rst:190-192) grounds the subscription target's evaluation and therefore
  `constant-key`; S438 grounds that the exported environment is what acts on the git child. The
  declaration's single-source attribution of the subscript-value sentence to `expressions.rst` is
  wrong; the lesson Gate records the correction. Neither row existed at the freeze (`bc18399b`);
  both are committed at `f754347a`.

## Substitution

See B9. Short form: both targets are reachable by a substitute artifact that hardcodes the expected
per-case answer; the measurement (not the selftest) does not block it because the counter is the
only observer and no held-out input exists. C1's entry discloses; C2's entry does not.

## Scratch

`/fast/scratch/hyaku/mado-r70/R70CriticClaims/` — removed before yield (`trap`/`finally`).
