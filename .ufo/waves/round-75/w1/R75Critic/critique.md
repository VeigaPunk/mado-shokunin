# R75Critic — framing review

Review scope: frozen base `b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6`, generation `def73656c94f0e88bd671cfb4a65124338261722`. No admission or canonical judgment is made here.

Axes: coverage, depth, operability, freshness, calibration, adjacency. Directly affected: calibration (C1's measurement authority), operability (C2 and unchanged-call compatibility). The other four have no demonstrated change in this review.

## Questions (a)–(e)

### (a) New denominator or re-scoring? — NEW HARNESS SURFACE, HELD RULE SEMANTICS

C1 introduces an end-to-end harness-decision denominator, not a new witness doctrine. Base `SCORECARD.md`, “Planned (round 75)” item 1, explicitly requests wiring the witness into a successor harness while freezing r72. Base `corpus/lessons/round-74.md:33-37` explicitly disclaims such wiring. Declaration `claims-declaration-r75.md:38-42,47-54,66-70` targets precisely that missing connection. The counter actually invokes extracted harness programs against committed fixture repositories (`c1-r75-harness-witness.py:220-249,282-305`). Thus this is more than calling the r74 pure rule on eleven replacement strings.

However, declaration lines 33-34 (“Both claims take new finite denominators rather than re-scoring a held rule on new inputs”) needs the qualification **new measured harness integration; witness predicate carried from r74**. It must not be read as a newly discovered authenticity rule. The r74 lesson's duplicate-input caveat at lines 122-126 also applies again: r75 `right` and `liar-success` take identical report and witness branches and both exit 0 (`c1-r75-harness-witness.py:89-125`). Eleven fixture modes are not eleven distinct rule-visible behaviors. Smallest correction: disclose this duplicate, preserving frozen cases and denominator.

### (b) Harness decision or rule alone? — HARNESS M-Z DECISION ONLY; OUTCOME NOT SCORED

The real extraction/selftest/M-Z mutation pipeline runs. `parse_decision` returns regex group 1 (`c1-r75-harness-witness.py:212-217`), and group 1 is only `mz=(pass|fail)` (`:67-73`). Scoring compares only that field to `expect_kill` (`:297-315`). Neither harness exit status, overall `verdict`, `witness` state, nor `mr` correctness is scored.

Executable counterexample in `rederived-controls.txt`: the contract

```
MADO_R75_LANDING_CONTROLS: selftest=2/2 mz=pass mr=fail killed=1/2 baseline=0/2 witness=absent verdict=TARGET_MISSED rev=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

is scored as `pass`. A harness that produces the expected M-Z field while incorrectly greening its outcome on absent witnesses would retain the same eleven-case score. This does not show that the current outcome implementation is wrong: its witness conjunction is visible in `c1-r75-landing-controls.py:192-219`. It shows the frozen C1 counter cannot establish the outcome half of declaration lines 50-52. Smallest safe correction this round: explicitly separate **measured M-Z claim** from **outcome implementation inspected, not certified by this denominator**. Any new outcome-scoring criterion needs a successor predicate, not relabeling the frozen result.

### (c) Forty-seven cases: new carrier class or padding? — REAL DELTAS, CARRIED REGRESSION MAJORITY

The first 36 case objects equal the frozen r74 cases exactly, independently re-derived in `rederived-controls.txt`. The eleven additions (`controls/c2-cases-r75.json:221-286`) cover four non-env-named key-carrying copies, three copy negatives, two delete cancellations, and two delete negatives. The held classifier fails all four new copy positives and both cancellation negatives. These are real name-neutral-carrier/cancellation deltas identified in base SCORECARD plan item 2 and r74's carried-limit list, not 47 independently new capabilities. Characterize the result as **36 carried + 11 additions, six held misses repaired**, not 47 new carrier classes. The four copy examples overlap semantically but separate concrete syntax/source spellings; retaining them is useful regression coverage, not evidence of four independent capabilities.

### (d) Can do-nothing reach either target? — NO, UNDER THE DECLARED HELD CONTROLS

Independent derivation from frozen bytes is in `rederived-controls.txt`:

- C1: held r72 credit accepts `right`, `liar-success`, `uppercase-echo`, `stale-witness`, `absent-witness`, `wrong-witness`, `last-wins-wrong`. Only the first two are labeled positive. It correctly rejects `crash`, `zero-denominator`, `mismatch-detail`, `green-mutant`. Therefore 2 true positives + 4 true negatives = **6/11**, with five false positives. This local derivation ran the frozen fixture reports after exactly the M-Z clause deletion and applied the frozen held credit; it did not repeat full fixture-repository harness measurement. The already committed full-pipeline baseline `control-baseline-r75.txt:25-38` agrees exactly.
- C2: independently loaded the held r74 classifier bytes from base and classified all 47 frozen source strings: **41/47**. Misses: `copy-dict-kw-bound`, `copy-splat-bound`, `copy-dict-builtin-bound`, `copy-dict-literal-base`, `del-env-store-cancel`, `del-env-literal-cancel`. The 36 carried cases and five added negatives/controls pass.

These fall short of 11/11 and 47/47. This is not proof against a substitute/canned artifact; question (b) provides a counter to that stronger interpretation. No claims of universal anti-gaming follow from the do-nothing result.

### (e) Universal clauses beyond enumeration? — YES; TWO IMPORTANT LIMITS

1. Declaration C1 lines 50-52 contains two behavioral clauses, but only M-Z is scored. “The contract outcome is green only under the same echo” is not established by the eleven-case score; see (b).
2. Declaration C2 lines 83-88 says “any simple name” and specifies dominance/delete behavior generally. The added positive copies all use the literal name `child`; cancellation additions use `env`. Forty-seven cases cannot enumerate every Python name or all scope/binding combinations. The implementation is syntactically name-neutral, and inspection supports that intent; the denominator supports only the named frozen set. Keep the stated syntactic limits (`:101-105`) and label the general sentence as implementation scope rather than exhaustive measured correctness.

Additional framing defects and smallest corrections:

- **Random uppercase separator is not unconditional.** Frozen `uppercase-echo` always expects rejection, but `secrets.token_hex(8)` can generate sixteen decimal digits. Uppercasing then leaves the challenge byte-identical. Deterministic exercise with `1234567890123456` returns credit=True while the frozen label is False (`rederived-controls.txt`). Probability per challenge is `(10/16)^16 = 0.0005421010862427522`, about 1 in 1845. The frozen observed receipt remains valid, but a future correct implementation can miss this case through no defect. Smallest safe current correction: disclose the probabilistic false miss; do not silently redraw until passing. A future denominator should use a guaranteed case-changing challenge for this grammar separator, or derive expectation from actual byte equality.
- **“Only right and liar-success credit”** (`c1-r75-harness-witness.py:24-26`) is therefore not unconditional across generated challenges. Qualify as the observed frozen measurement and disclose the digits-only collision above.
- **“A captured block from an earlier run cannot carry the challenge generated now”** (`c1-r75-landing-controls.py:23-25`, also inherited r74 lesson `:66-67`) is probabilistic, not impossible: an independently fixed 64-bit witness can coincide with probability 2^-64. Correct to “rejects stale fixed echoes except random collision”; this is not an assertion-authenticity mechanism, as the declared limits already acknowledge.
- **“Eleven modes are rule separators”** (declaration `:67`) overstates independence: `right`/`liar-success` have identical observable behavior. Say eleven named modes including one duplicate behavior. Do not rewrite frozen labels.

## Lowest axis and stagnation

Qualified **re-derivable** for the currently active published finite sub-axes: base SCORECARD's r74 tail records navigation 91/91, calibration resolved-active 86/86, operability selftest 12/12 and ledger 130/130, all 10 under their finite rubrics. Its r57 freshness rebaseline table records surface-state audit currency 8/8 = 10.0000. Depth and adjacency are explicitly unscored in the earlier axis table, not proven saturated.

The old freshness/file-plane value **9.6552** remains explicitly “dormant, host-absent,” with disposal operator-owned (base SCORECARD “Freshness sub-axis re-baseline”, and r58 axis posture). If dormant scores are excluded, there is no distinctly lowest active scored axis. Including that historical non-retired value makes freshness lower. The declaration's “no axis is distinctly lowest” must retain the **active published finite rubrics, dormant-score disposition still open** qualifier; this review does not resolve the outstanding authority question. It does not establish province saturation.

Stagnation: base SCORECARD declares saturation line 9.0 and N=3, and contains a capability row first-working r74. At r75 start the intervening capability-free gap is 0, below 3. Thus the stagnation nudge does not apply. That does not itself waive another obligation; the no-distinct-lowest argument is the tie among active finite scores, not stagnation.

## No-harm amendment and assigned selftest

Executed requested read-only diff from base to freeze for `quality/landing-counters.sh`. The only functional changes are a new `landing_witness` helper and calls after the selftest summary and normal contract summary. With `MADO_LANDING_NONCE` absent, `${MADO_LANDING_NONCE:-}` is empty and helper returns 0 before output. The normal path retains explicit `exit "$exitcode"`; the selftest retains its explicit P=N test after the helper. Error/help paths precede the new calls. Therefore no absent-nonce caller output or exit-status change follows from this amendment. This is a scoped static compatibility finding, not an exhaustive execution of every historical caller.

Executed the **frozen new-generation bytes** extracted to owned scratch, with nonce removed from environment:

```
bash <owned-scratch>/landing-counters.sh --selftest --scratch-root <owned-scratch>/instrument-selftest
MADO_LANDING_COUNTERS_SELFTEST: 62/62 assertions passed
returncode=0
```

Full receipt: `landing-selftest.txt`. No witness line was emitted. The instrument's internal fixture git writes stayed under owned scratch; its toplevel assertion precedes each commit. No lane git mutation or production edit was performed.

## Correction classification

Fixable documentation/measurement-boundary defects: outcome-score overclaim, duplicate-mode disclosure, universal wording, active-vs-dormant axis qualification, and randomness caveat. The uppercase fixture is a real frozen-oracle defect, not evidence the candidate witness rule should become case-insensitive. Do not “repair” it by weakening byte-exact comparison or retrying until green. Altering a frozen expectation/target or claiming the outcome clause has now been measured would require canonical disposition or a successor denominator; this critic neither admits nor judges that tradeoff.

Tools installed/updated: none. Receipts were copied into this owned report directory before scratch deletion.

Self-evaluation: accuracy 4/5 (full C1 pipeline uses committed evidence; local re-derivation isolates credit); completeness 4/5 (all assigned questions and selftest covered; dormant-axis authority remains explicitly unresolved); clarity 4/5 (evidence localized, but detailed); actionability 4/5 (smallest corrections distinguish disclosure from frozen-predicate change); conciseness 4/5 (full requested framing review). Overall 4.0/5. No canonical pass/fail or promotion decision is implied.
