# MadoA4CritAdmission — round-48 claim admission review

Axes: C1 operability / capability acquisition; C2 coverage / sourced; plus no-harm across axes.

## Rulings

**C1: not admitted by this review; no predicate break established. C2: not admitted by this review; no predicate break established.** Admission requires verified claims and no harmed axis. The specific no-harm evidence requested is incomplete: `receipts/a4/c1-r47-at-tip.txt:1` is only a header, and the available `receipts/v2/check96-l1.txt:14-16` is a `check-landed-contract.py` check, not the requested round-47 counters or `check-axis-scores` output. `receipts/a4/c2-r47-at-tip.txt:2-16` does report C2 round-47 `TARGET_MET` at the named tip, but does not close the missing C1/axis-score evidence.

### Do-nothing controls

- **C1:** `registration-v2.md:68-73` specifies a 64-candidate control set; `receipts/v2/ctl-c1v2.txt:6-69` reports every candidate `TARGET_MISSED`, and the landed tool meets (`:3`). However, the absent-tool candidate is a setup error, not a runnable skip-work tool (`receipts/v2/ctl-c1v2.txt:5`; `receipts/v2/ctl/ABSENT.txt:1-3`). A non-absent never-warm mutant does miss (`receipts/v2/ctl/w2MutC1Tool-m3-never-warm.txt:1-4`), but the receipts do not establish that it is the cheapest skip-work control required by the assignment. Thus the control evidence is supportive, not dispositive.
- **C2:** The cited evidence does not show a do-nothing tool/entry control scored against C2. The C2 98-variant harness is a mutation/control matrix, not an identified cheapest skip-work entry control (`registration-v2.md:84-88`; `receipts/v2/c2v2-revc2counter-matrix.txt:1-100`). This admission criterion remains unverified.

### Separability

- **C1:** C1 v2 reports at `cf3deeec` selftest `70/70` (`receipts/a4/c1v2-at-salvage.txt:1-4`); the base tool is separately reported as missing the target (`registration-v2.md:58-59`). Supports C1 independent of entry work.
- **C2:** The C2 mirror at candidate reports all clauses admitted and four new rows present (`receipts/a4/pre-c2v2.txt:1-2,14-22`). This supports entry work independent of the tool change, though this is a candidate mirror revision rather than the named data commit.

### v2 re-registration: repair or re-aim?

The disclosed chronology says v2 was authored after reading w2 results (`registration-v2.md:11-15`), hence it is not blind. The stated changes repair concrete v1 predicate defects raised by w2 (`registration-v2.md:17-35`); the control set then re-scores those candidates and requires them to miss (`:68-73`; `receipts/v2/ctl-c1v2.txt:6-69`). The registration reports that v2 preceded data and that predicates/counters/fixtures are frozen (`registration-v2.md:4-8,98-101`). Taken together, this is consistent with a pre-data repair under the stated §9 process, not evidence of a simple re-aim. The after-results authorship still warrants weighing the complete control set; it does not eliminate the separate missing C1 control/no-harm evidence.

### C2 coverage frontier

C2 is plausibly new coverage rather than re-scoring held ground: the claim says XKB compile behavior was not reproduced at base and names the surface shift (`claims.md:22-27`); the candidate mirror records new S351 and `present_at_rev=4/4` (`receipts/v2/c2v2-data-mirror.txt:14,18-21`). The v2 data receipt likewise reports S351, four rows present, and a successful live replay (`receipts/c2-after-data.txt:14,18-22`). This supports a frontier→core interpretation, while independent truth of all entry claims is outside what these counter summaries establish.

## Smallest safe correction

Provide the round-47 C1 counter output and `check-axis-scores` result at the specified tip. For full do-nothing admission evidence, identify and score the cheapest runnable skip-work C1 candidate and a C2 entry that skips the claimed coverage, rather than treating missing-tool setup failure or a mutation matrix as those controls.

No tools installed. Scratch was cleaned; no output file was retained there (largest scratch output: none).
