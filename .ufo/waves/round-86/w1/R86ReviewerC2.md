# R86ReviewerC2 — C2 attack report (round 86, wave 1)

Seat: R86ReviewerC2 · Freeze rev: `237ecf4e69a4986108f719f3beeafe111adaa033` · Lane HEAD at review time: `b33afc089fad2fcc5f6684f3b3a9d2260cf2e915` (SKILL.md +2 registry lines past the freeze; both C2 counters tree-bind the working tree to `--rev`, so every run below was made against a scratch fixture tree made byte-identical to the freeze rev by `git archive | tar -x`, verified with `cmp` — no mutating git command anywhere, no lane file written except this report).

## Verdict on the claim (attacker's summary)

The frozen predicate is green at the freeze rev and reproducible from my commands (rc 0, `tree=bound`), and the four r85 survivors are measurably alive before and dead after. The claim's kill rule holds. What breaks under attack is the **strength of the observation sentence**: the clause observation binds loop *iterations*, not *judgements*, and two count-preserving forgeries pass every case-level conjunct. Both forgeries still fail closed at the verdict level — one via the mutant population, one via the mutation-anchor setup guard — so no false TARGET_MET is reachable by them. Findings below; no fix proposed (instruments frozen).

## Findings by severity

### F1 — Medium: the clause observation counts iterations, never evaluations; the case-level rule cannot refuse a count-preserving stub (counter 2(i))

Counter-side forgery tested (scratch copy of the frozen instrument, both `okay(sample…)` evaluation lines replaced by `if False:`, increments untouched):

```
MADO_R86_PROBE: name=border-size-int row=36 kind=regex match=yes clauses=anchors:1,samples:2,negatives:3 declared=anchors:1,samples:2,negatives:3 rc=0 stdout-bytes=2
MADO_R86_RUNBOOK: cases=37 executed=37 matched=37 shapes=27/27 anchors=37/37 rows=37/37 clauses_observed=37/37 … mutants=37 killed=5 verdict=TARGET_MISSED rev=237ecf4e… tree=bound   [rc 1]
```

* Does the r86 rule refuse the case? **No.** matched=37/37 and clauses_observed=37/37 with zero sample/negative ever evaluated; the border-size-int probe line is byte-identical to the honest run's.
* Which conjunct catches it? **None of the case-level conjuncts.** The only refusal is `killed == 37`: with evaluations stubbed, 32 of the 37 declared mutants survive (only `pipeline-guard-stripped`, `any-nonzero`, `signal-as-exit`, `negatives-skipped`, `samples-skipped` still die — the first three via the live call, the last two via clauses_observed). So the observation adds no evaluation semantics of its own; the defense against this forgery class is indirect and population-dependent (it works only because the declared mutants happen to need sample/negative evaluations to die).

### F2 — Medium: negative-loop replaced by a second live evaluation scores 37/37 green under `--no-mutants`; only the mutation-anchor guard stops it (counter 2(ii))

Forgery tested (negative loop deleted; `OBS["negatives"] = len(negatives)` assigned; live output re-evaluated instead):

```
# with --no-mutants:
MADO_R86_RUNBOOK: cases=37 executed=37 matched=37 shapes=27/27 anchors=37/37 rows=37/37 clauses_observed=37/37 … mutants=0 killed=0 verdict=MUTANTS_SKIPPED rev=237ecf4e… tree=bound   [rc 0]
# with the declared mutant loop enabled:
MADO_R86_RUNBOOK: ERROR (stage=setup mutant negatives-skipped anchor occurs 0 times, not once)   [rc 2, never a verdict]
```

* Case refused? **No** — rc 0, every conjunct green, the negative's content never judged (an honest-looking counter prints MUTANTS_SKIPPED rc 0).
* Which conjunct catches it? Only the **mutation-anchor existence guard** (`hits != 1 → Setup`, rc 2 fail-closed), and only because this edit deletes the `negatives-skipped` anchor text verbatim. A body-only stub that keeps loop headers is exactly F1's variant and passes the guard; the guard is tamper-evidence on the counter's own source, not part of the clause observation.

### F3 — Low (diagnostics): the summary field `anchors=` does not report anchor observations

The summary line prints `anchors=len(bindings)/CASES` (format string: `… anchors=%d/%d rows=%d/%d clauses_observed=%d/%d …` fed `len(bindings), CASES, len(rows), CASES, observed_all, CASES`). `len(bindings) != CASES` raises Setup before the summary, so `anchors=37/37` is tautological on any run that reaches it; the real anchor-clause observation is folded into `clauses_observed`. Misleading label inherited from the r85 line format — cosmetic, predicate unaffected.

### F4 — Low (receipt provenance): no committed receipt shows the frozen predicate green at the freeze rev

* `.ufo/waves/round-86/receipts/control-c2-r86.txt` — the committed control run — is at `rev=b33afc08…` (post-freeze SKILL.md) with `mutants=0 killed=0 verdict=MUTANTS_SKIPPED`.
* `.ufo/waves/round-86/receipts/c2-repaired-r86.txt` — the full TARGET_MET run — is at `rev=f72bba01928efe80cfa1a7907fe3aaa9eba1cfd7` (attempt-1 bytes), not the freeze rev.
* My run supplies the missing point: **rc 0, TARGET_MET, `tree=bound` at `237ecf4e…`** (line quoted below). Deterministic instrument, so this is provenance, not validity.

### F5 — Info (declaration ambiguity, resolved fail-closed): "observed counts equal their declared populations" holds only under the live-snapshot reading

For an `anchor: line` case with S samples and N negatives (the witness: S=2, N=3), the counter requires the triple `(LIVE["anchors"], OBS["samples"], OBS["negatives"]) == (1, S, N)`, where `LIVE["anchors"]` is snapshotted after the live call, before the loops. Under a literal reading of the final `OBS` dict the honest case would fail: border-size-int's final anchor count is 5 (1 live + 2 samples + 2 of 3 negatives — the rc-127 negative is refused at the producer-status gate and never reaches the anchor branch), against a declared population of 1. The counter's own selftest asserts `dict(OBS) == {"anchors": 3, …}` for a 1-sample/1-negative case, and `receipts/instrument-repair-r86.md` repair 2 documents exactly this contradiction in the attempt-1 bytes. So: the declaration's sentence and the instrument agree only under the "one judgement of the row's own output" reading; on the OBS-final reading the honest instrument would print clauses_observed=34/37 TARGET_MISSED — fail-closed, never a false pass.

* Can a case be scored without its anchor clause running? **Not under the frozen bytes at case level.** The increment sits inside `matches()`'s `anchor == "line"` branch and `case_correct` hard-refuses any anchor:line case with `LIVE["anchors"] != 1`; a live call that exits at the status gate leaves LIVE=0 → refused. The reachable failure is counter-side (F1/F2): a clause that runs without judging is indistinguishable from a clause that judged.

## (1) Before-side measured: the four r85 survivors are alive at the freeze rev

`c2-r85-status-classes.py` executed at `237ecf4e…` (round-85 controls, round-84 carried set; rc 1):

```
MADO_R85_MUTANT: name=regex-anchor-dropped matched=36/36 killed=no
MADO_R85_MUTANT: name=line-anchor-prefix matched=36/36 killed=no
MADO_R85_MUTANT: name=negatives-skipped matched=36/36 killed=no
MADO_R85_MUTANT: name=samples-skipped matched=36/36 killed=no
MADO_R85_RUNBOOK: cases=36 executed=36 matched=36 shapes=26/26 anchors=36/36 rows=36/36 … mutants=37 killed=33 verdict=TARGET_MISSED rev=237ecf4e… tree=bound
```

Measured at the freeze tree, not asserted from `receipts/final-c2-r85.txt` (which was taken at `2b6dd76b…`). After-side, same rev: `regex-anchor-dropped matched=36/37 killed=yes`, `line-anchor-prefix matched=36/37 killed=yes`, `negatives-skipped matched=0/37 killed=yes`, `samples-skipped matched=5/37 killed=yes`. Kill mechanisms: the two anchor survivors die via the negative `0 extra` (matched=36; clauses_observed stays 37/37 — see F5/F1), the two count-skippers die via clauses_observed (0 and 5 matched = the cases declaring 0 samples are exactly the 5 that survive `samples-skipped`).

## (2)/(3) attempted forgeries — see F1, F2, F5

## (4) Frozen counter re-run once at the freeze rev — quoted line

```
MADO_R86_RUNBOOK: cases=37 executed=37 matched=37 shapes=27/27 anchors=37/37 rows=37/37 clauses_observed=37/37 superseded=active-workspace,binds-count,clients-count,gaps-out,kb-layout,keybindings-actions,keybindings-chords,layers-namespaces,monitors-reserved,monitors-size,omarchy-version,tray-items,tray-methods,version,waybar-process,workspaces-count mutants=37 killed=37 verdict=TARGET_MET rev=237ecf4e69a4986108f719f3beeafe111adaa033 tree=bound
```
rc 0.

## Exact commands (reproducible; scratch removed after review)

```sh
S=/fast/scratch/hyaku/mado-r86/R86ReviewerC2; REV=237ecf4e69a4986108f719f3beeafe111adaa033
git clone --no-hardlinks -q /home/vgpnk/Projects/shokunin/mado-shokunin "$S/freeze-tree"
git -C "$S/freeze-tree" archive "$REV" | tar -x -C "$S/freeze-tree"
git -C "$S/freeze-tree" show "$REV:SKILL.md" | cmp - "$S/freeze-tree/SKILL.md"   # byte-identical, else exit
cd "$S/freeze-tree"
# before-side (rc 1, killed=33):
python3 -I quality/counters/c2-r85-status-classes.py --repo . --rev "$REV" \
  --controls .ufo/waves/round-85/controls/c2-cases-r85.json \
  --carried .ufo/waves/round-84/controls/c2-runbook-cases-r84.json --scratch-root "$S/r85"
# frozen counter (rc 0, TARGET_MET):
python3 -I quality/counters/c2-r86-clause-observations.py --repo . --rev "$REV" \
  --controls .ufo/waves/round-86/controls/c2-cases-r86.json \
  --carried .ufo/waves/round-85/controls/c2-cases-r85.json --scratch-root "$S/c2"
```
Note: the r85 instrument demands a 33-case carried set — round-84's file qualifies; round-83's `c2-runbook-cases-r83.json` now holds 31 cases and the instrument refuses it (`ERROR (stage=setup carried set carries 31 cases, frozen target expects 33)`, rc 2 fail-closed — correct behavior, but the declaration's command block does not pin the r85 carried path; this cost me one mis-invocation before the run above).

Variant forgeries: scratch copies of the frozen instrument with (A) both `okay(sample…)` evaluation lines → `if False:`; (B) negative loop → `OBS["negatives"] = len(negatives)` + second live evaluation; (C) `found.group(0) == line` equality dropped (= declared `line-anchor-prefix`, run standalone: border-size-int probe `match=no`, matched=36/37, shapes=26/27, clauses_observed=37/37, verdict=TARGET_MISSED rc 1 — refused by `matched == 37` via the negative, not by the observation).

## Residual risk and verification gaps

* The clause observation cannot distinguish "clause judged" from "clause counted" (F1/F2). Any future mutant population whose members are killed by clauses_observed alone would make a count-preserving stub fully green; today the population's dependence on sample/negative evaluations is the load-bearing defense.
* Live rows are host-dependent (hyprland/waybar/systemd state); matched=37 holds at measurement time on this host and is not pinned beyond it.
* I did not audit C1 or the control-set construction (out of seat scope); the `anchors=` label (F3) is shared with the r85 line format.
* 5 fixture runs + 3 variant runs executed; every quoted line is from my own runs at `237ecf4e…` with `tree=bound`.
