# R75ScribeEntries — knowledge-entry drafts

## Behavior and axes

Drafted the two admitted knowledge entries, without modifying the corpus or product code.
Claim axes: C1 calibration; C2 operability. Report-quality axes: evidence accuracy,
completeness, clarity, actionability, conciseness. No measurements were rerun.

- `entry-c1.md` targets `corpus/knowledge/harness-witness-credit-r75.md`: successor harness
  composition, arithmetic plus byte-exact last witness, green-outcome gate, all eleven frozen
  modes, supplied 11/11 versus 6/11 receipt, and authentication/fixture limits.
- `entry-c2.md` targets `corpus/knowledge/guard-carrier-copy-del-r75.md`: name-neutral keyed
  construction and literal-key delete cancellation, all eleven appended cases grouped by
  shape, supplied population 20/13/13/0 and controls 47/47 versus 41/47, and syntactic limits.
- Both use house front matter (`source:`, `verified-at:`, `recheck:`), cite the freeze revision
  `def73656c94f0e88bd671cfb4a65124338261722`, and reserve external S-row citations for the L1.

## Evidence and gates

Read the declaration first, both supplied measurement receipts, both new counters, the held
and successor landing harnesses, appended frozen C2 cases, and the two named round-74 house
entries. The counters were read as source, not imported or executed. The C1 counter's case
score is its M-Z decision, not an overall harness-exit score; the draft makes this distinction.
Both drafts quote the supplied final contract lines without presenting them as new execution.

The user describes the receipts as committed. At the scribe's provenance read, however, both
were untracked and absent from the measured freeze tree. The L1 subsequently instructed:
"The two measurement receipts are now being committed" and "receipt committed with this
round's landing". Drafts distinguish the measured freeze from that later receipt landing and
explicitly attribute landing status to the L1, not this seat's observation. No later git check
was performed merely to decorate this report.

Exact observed provenance commands (cwd `/home/vgpnk/Projects/shokunin/mado-shokunin`):

```
git log -1 --format='%H %s' -- .ufo/waves/round-75/measurement-c1-r75.txt .ufo/waves/round-75/measurement-c2-r75.txt && git rev-parse HEAD
```

Exit 0. The log portion printed no entry; `rev-parse` printed
`def73656c94f0e88bd671cfb4a65124338261722`.

```
git ls-tree def73656c94f0e88bd671cfb4a65124338261722 .ufo/waves/round-75/measurement-c1-r75.txt .ufo/waves/round-75/measurement-c2-r75.txt .ufo/waves/round-75/claims-declaration-r75.md quality/counters/c1-r75-harness-witness.py quality/counters/c1-r75-landing-controls.py quality/counters/c2-r75-shapes.py && git status --short -- .ufo/waves/round-75/measurement-c1-r75.txt .ufo/waves/round-75/measurement-c2-r75.txt
```

Exit 0. `ls-tree` listed the declaration and three instruments, not the receipts. Status was:

```
?? .ufo/waves/round-75/measurement-c1-r75.txt
?? .ufo/waves/round-75/measurement-c2-r75.txt
```

No test, build, lint, measurement, publication or commit command was executed by this seat.
The supplied receipt files contain TARGET_MET contract lines; their command exit codes were
not independently observed here. The user reports rc 0 for each; the draft documents the
counter's exit map rather than claiming this seat saw those exits.

## Findings and verbatim conflicts

1. Receipt C2 line 118 says `MADO_R75_BASE controls=41/47 (the held round-73 rule must miss the target)`.
   Its base path is `quality/counters/c2-r74-shapes.py`; declaration and case base lines agree
   with round 74. L1 calls this a stale evidence label to repair/re-measure. Draft quotes only
   the final contract line and does not rewrite the receipt.
2. Declaration says `Shape: ONE v1 wave of 12 seats (band 8–16)`; assignment says
   `ONE v1 wave (13 seats)`. Neither draft makes a seat-count claim; disposition belongs to L1.
3. C2 source docstring says `must keep twenty readers, thirteen guarded, zero unguarded`;
   constants, declaration, and receipt distinguish population 20 from readers 13. Draft uses
   the declared and printed 20/13/13/0, not the docstring's wording.
4. C1's `uppercase-echo` parser accepts uppercase hex but comparison is byte-exact; the draft
   does not incorrectly describe uppercase tokens as syntactically malformed.
5. `del-before-store` is frozen syntactic evidence, not an executed Python mapping-deletion
   success claim. The draft states that boundary explicitly.

## Touched surfaces and commands

Created only these deliverables under the seat directory:

- `.ufo/waves/round-75/w1/R75ScribeEntries/entry-c1.md`
- `.ufo/waves/round-75/w1/R75ScribeEntries/entry-c2.md`
- `.ufo/waves/round-75/w1/R75ScribeEntries/report.md`

Directory setup, cwd `/home/vgpnk/Projects/shokunin`, exit 0:

```
mkdir -p /fast/scratch/hyaku/mado-r75/R75ScribeEntries /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-75/w1/R75ScribeEntries
```

Scratch cleanup, same cwd, exit 0:

```
rmdir /fast/scratch/hyaku/mado-r75/R75ScribeEntries
```

No scratch receipts were generated or cited. Scratch was empty and is removed. No tools were
installed or upgraded. One attempted draft edit used nonexistent line numbers and was rejected;
source was re-read and the provenance-only edit then succeeded. No product edit occurred.

## Out of scope and handoff

L1 owns source-row citation insertion, corpus admission, index/ledger/doc integration, receipt
landing, stale-label repair and re-measurement, and canonical judgment. No no-harm gate is
claimed exercised by this seat. The report resides inside the seat directory per the L1's
explicit trailer correction rather than the assignment's outside-directory report suggestion.

## Self-evaluation

| axis | score | evidence / improvement |
|---|---|---|
| accuracy | 4/5 | Rule/parser and receipt provenance are distinguished; receipt landing remains L1-reported, not observed. |
| completeness | 4/5 | Both full draft bodies and all frozen case names are present; external S-row citations intentionally await L1. |
| clarity | 4/5 | Separate rule/cases/limits/provenance sections; lengthy provenance can be shortened after admission. |
| actionability | 4/5 | Target paths and recheck commands are explicit; L1 must integrate citations and receipts before publication. |
| conciseness | 4/5 | Tables avoid repeating case explanations; audit report retains necessary command/provenance detail. |

Overall 4.0/5. Highest-impact improvements: L1 lands the receipts, inserts S-row citations,
and resolves the stale base-label evidence defect. Would the user agree: drafts satisfy the
scribe scope, while execution and landing evidence are not inflated.
