# R71RevC1 — adversarial review of claim C1 (calibration): exit-status-disagreement kill credit

Instruments reviewed at `8e78a4ee82f6ccdc951faf531438178a9d12245e` (extracted bytes verified:
harness sha256 `f836499594fb4fa8898336b1a47241614bb2b9ddb6f93c369a9e00ece0f185f1`, counter
sha256 `18fb679a7f75322c783ca164ed6a9cf684983b19ef8969409a9bed8ea2742152`; base harness at
`c354f4d410b829d985b31560af9202d98655dad0` sha256 `71a7b6c45b904a734f194be9a8de6cc2eeb5f5ea1922760f908f5637f1d4db58`,
equal to the receipt's base role). No repo file was modified; all runs under
`/fast/scratch/hyaku/mado-r71/R71RevC1/` (removed before this report was finalized).

## Verdict

**C1 predicate sound as bounded.** The implementation is exactly the frozen sentence with
nothing else changed: the sole behavioral delta from the held round-70 harness is
`mz_killed = bool(mz_rc != 0 and summary_shows_failure(mz_out))` (`c1-r70-landing-controls.py:478`)
→ `mz_killed = bool(summary_shows_failure(mz_out))` (`c1-r71-landing-controls.py:486`);
`last_summary`, `summary_fraction`, `count_fails`, `summary_shows_failure`, `outcome_exit`,
`outcome_verdict` are byte-identical between the two revisions (function-body diff: all six
IDENTICAL). The expectation table, base leg, verdict predicate, and contract line all
reproduce verbatim. Every defect candidate found lives outside the frozen sentence's words or
inside the declaration's declared limits; each is listed below as a disclosure obligation, not
a soundness break.

## Evidence (all commands run in this review)

1. **Full counter run** (canonical command, verbatim):
   `python3 -I quality/counters/c1-r71-real-children.py --repo . --rev 8e78a4ee… --base-rev c354f4d4… --scratch-root <scratch>/counter-run` → rc=0,
   last line `MADO_R71_REAL_CHILDREN: cases=4 correct=4 base_correct=3 verdict=TARGET_MET rev=8e78a4ee…` — reproduces `measurement-r71.txt` § C1 exactly (fixture revs differ, lane sha256s identical).
2. **Four fixture modes run directly as real bash children**, M-Z clause deleted via the
   harness's own `mutate_clause`, streams captured separately and combined; all four
   `lane_sha256` values match the frozen receipt (`72afc84a…`, `98f71ebd…`, `11dc7efd…`,
   `89987f16…`):

   | mode | rc | summary stream | summary | combined reader | expect | match |
   |---|---|---|---|---|---|---|
   | liar-success | 0 | stdout | 1/2 | credit → mz=pass | pass | yes |
   | stderr-genuine | 1 | stderr | 1/2 | credit → mz=pass | pass | yes |
   | liar-kill | 1 | stdout | 2/2 | refuse → mz=fail | fail | yes |
   | crash-stderr | 2 | none | none | refuse → mz=fail | fail | yes |

   Reader-coverage matrix: a stdout-only reader **misses `stderr-genuine`** (sees no summary →
   mz=fail); a stderr-only reader misses `liar-success`. The combined stdout-then-stderr read
   is the only reader scoring 4/4 — "both streams are read" is load-bearing and confirmed.
3. **Base leg**: the same counter run shows `base_mz=fail` for `liar-success` only;
   `stderr-genuine`, `liar-kill`, `crash-stderr` all `base_mz=pass`. The do-nothing control
   misses `liar-success` and only it, as the declaration's Before claims.
4. **Doctrine counterexamples through the real decision function** (`summary_shows_failure`,
   harness-r71.py:323-334) and **end-to-end through both harnesses** on a purpose-built
   stale-lane fixture (scratch git repo, clause carried exactly once, children extracted at
   `8e78a4ee…`): see F1/F2 below.

## Findings by severity

**F1 — MEDIUM (disclosure; successor-harness behavior change, outside the claim's target surface).**
The summary-only credit flips a status-lying instrument from r70-red to r71-green at the
verdict level, because the instrument-health leg still keys on exit status alone
(`outcome_exit`, c1-r71-landing-controls.py:352-354: `0 if selftest_rc == 0 and killed == 2`;
selftest leg rc-only at :455). Repro: stale-lane fixture (lane prints a failing summary
`1/2` without running any assertion, exits 0; full lane text in scratch `stale-fx/fx/quality/landing-counters.sh`,
from_sha256 `c9e4cdd4…`):
- r71 candidate: `selftest=0 mz=pass mr=pass killed=2/2 verdict=TARGET_MET`, **rc=0**;
  evidence line honestly records `rc=0 failed_assertions=0 assertions=1/2 killed=yes`.
- r70 base, same fixture: `killed=1/2 verdict=TARGET_MISSED`, **rc=1**.

An instrument whose assertions genuinely fail while its exit status lies 0 (the exact class
the declaration names at claims-declaration-r71.md:44-46) now scores `TARGET_MET`/exit 0 on
the full harness. The kill credit itself is correct under the frozen doctrine (the summary is
the assertion signal); the inconsistency is that the same doctrine is not applied to the
unmutated selftest leg. The declaration's target surface (line 42: the conjunct only) and the
Harm watch (line 164+) do not name this flip; the round report must disclose it.

**F2 — MEDIUM (disclosure; inherent to the frozen sentence).**
Summary-only credit severs the evidentiary link between the mutation and the failing summary:
a lane whose output does not depend on the deleted clause at all (canned/stale/echoed failing
summary) earns the kill. The F1 fixture is the demonstration — mutation deleted, output
identical, `killed=yes`. Within the frozen four-mode fixture the link holds (the scenario
`else`-branch is reachable only when the clause is deleted — verified: unmutated lanes in all
four modes print `2/2`, rc 0). As a standing rule for the real instrument it does not. The
frozen sentence's words admit this by construction; the "Not claimed" ¶ (line 152-163) covers
forgery ("byte-indistinguishable … does not authenticate it", line 156-157) but never names
the stale/canned/skipped-run class — the report must name it explicitly.

**F3 — LOW (inherited, not a regression; underdetermined by the frozen sentence).**
Multi-summary tie-break is unspecified by the declaration; the implementation takes the LAST
summary line in stdout-then-stderr concatenation order (last_summary, :306-311), so a stderr
line outranks a stdout line by position, not chronology. Both directions demonstrated on the
decision function: genuine `1/2` stdout followed by stale `2/2` stderr → credit refused
(genuine kill lost); stale `1/2` stderr after genuine `2/2` stdout → false credit. r70 behaves
identically (functions byte-identical), so C1 introduces no change here; the report should
disclose the last-wins rule.

**F4 — LOW (docstring overclaims relative to code).**
`c1-r71-landing-controls.py:327-328` states "A kill is credited on a failed assertion, never
on a broken child." The F1 child is broken (runs no assertion, `failed_assertions=0`) and is
credited. The declaration's frozen sentence (lines 78-82) makes no such claim — it refuses
only crashes and unparseable summaries — so fidelity holds, but the report must not quote the
docstring sentence as a property of the rule.

**F5 — INFO.**
The counter drops the harness process's own exit rc from its receipt: `run_harness` returns
`r.returncode` (c1-r71-real-children.py:261-268) but `measure` discards it (`_, got, _ = ...`,
:317-318), scoring only the `mz=` field per the declaration (line 75). Compliant; visibility
nit only — the child rc remains visible in the harness's own `MADO_R71_MUTANT M-Z` evidence
line (`rc=%s`, :489-495), which satisfies "the receipt keeps the exit status visible".

**F6 — INFO (covered by the counter's own declared limit).**
The four observed child exit codes are {0, 1, 2}; a hypothetical rule crediting on
summary-failure but rc-gated at, say, rc≠5 is indistinguishable from the scored rule on this
fixture. The counter's docstring already declares it "cannot tell a correct decision from a
decision that happens to agree on these four inputs". No action.

## Attack-line adjudication

**(1) Doctrine.** (a) Lane exits 0, never runs assertions, prints a stale failing summary:
the frozen sentence ADMITS it — the credit fires on the parsed `p<n` summary "whatever the
exit status"; demonstrated end-to-end (F1). The Not-claimed ¶ refuses only to *claim
soundness* against a non-authenticated summary; the word "forged" (line 156) does not
literally cover staleness/skipped-run, so this must be named as its own limit. (b) Wrapper
echoing a captured summary: ADMITTED by the same words (decision-level: captured `1/2`, rc 0
→ credit True; r70 → False). If the echoed summary is genuine of an inner failure the credit
is defensible; if stale/canned it is a false credit (F2). (c) Summary lies while rc agrees
(truly `2/2`, prints `1/2`, exits 1): BOTH r70 and r71 credit — the rc conjunct never
authenticated summaries, so C1 newly admits nothing here; this is the doctrinal defense that
survives attack (1).

**(2) Fixture semantics.** Table in Evidence §2: the expectation table is exactly what a
combined-output reader sees, on real bash children whose lane bytes equal the frozen receipt.
Stream coverage is load-bearing (stdout-only misses `stderr-genuine`). Unmutated lanes are
`2/2`/rc 0 in all four modes, so the counter's mz-only scoring is isolated from the selftest
leg as the declaration intends.

**(3) Base leg.** Confirmed: the held r70 harness misses `liar-success` and only it
(Evidence §3); its conjunct is at `c1-r70-landing-controls.py:478`; its stream concatenation
(:475) and all shared decision functions are identical to r71's.

**(4) Frozen-sentence fidelity.** Exact. Conjunct removal only (:478 → :486). "Both streams
are read (stdout then stderr)": :483 = r70 :475 byte-identical. "A crash or an unparseable
summary is never a kill": verified — no-summary rc 2, garbled `??/2`, `0/0`, and `2/1` all
refuse; `61/62` credits (p<n). Parse strictness (fullmatch on the stripped line; inner
double-space or leading indent refuses) is inside the sentence's own "parsed" definition.
Verdict predicate: `verdict_met` (:191-192) = `correct == 4 and base_correct == 3`, matching
line 75-77; contract line (:195-199) reproduces the After sentence (lines 53-60) verbatim;
`CONTRACT_RE` (:85-88) additionally admits `correct=absent` per the documented absent-candidate
case. Exit map 0/1/2 matches the After clause "and exits 0" and the docstring.

## Residual limits the round report must disclose

1. A stale, canned, or echoed failing summary earns kill credit (skipped-run/wrapper classes);
   the Not-claimed "forged" wording does not literally name them.
2. Kill credit no longer evidences that the mutation caused the failing summary (F2); within
   the frozen fixture the link holds, as a standing harness rule it does not.
3. Verdict-level red→green flip vs r70 for an instrument with broken status propagation and a
   failing summary (F1): the selftest leg and `outcome_exit` remain rc-only — the class C1
   fixes for mutants persists one leg over in the same harness.
4. Multi-summary outputs resolve last-wins in stdout+stderr order; stderr dominates stdout by
   position, not chronology (F3, r70-identical).
5. rc-gated credit variants agreeing on the observed rc set {0,1,2} are indistinguishable on
   this fixture (F6).
6. Standing declared limits carry over unchanged: four modes are not fault coverage; the
   fixture lane is not the real landing instrument.

No production path was written; no mutating git/jj command touched the lane, the fleet repo,
or any sibling (fixture repos built under scratch with asserted `rev-parse --show-toplevel`
identity and explicit `-c user.name/-c user.email`). Scratch
`/fast/scratch/hyaku/mado-r71/R71RevC1/` removed. No tools installed; no pacman transaction.
