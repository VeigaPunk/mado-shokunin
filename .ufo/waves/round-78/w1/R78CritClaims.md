# R78CritClaims — round-78 claims-design critique

Critic seat. Read-only: no repo edit, no commit, no mutating git/jj. Citations name the command
and the observed output; instrument bytes are named by sha256. The repository changed under this
review (HEAD walked `00ed4ac0 → 3eb518a5 → aea5409e → f7c9bf9b → 307c125a → edb4159b`); §0 and §5
separate what I measured at which tip.

## 0. Ground at review time

| instrument | brief pin | tree at HEAD `edb4159b` |
|---|---|---|
| `tools/mado-barfoot.py` | `aac5d41b…` | `aac5d41b…` unchanged |
| `quality/counters/c1-r78-margins.py` | `1c39a53c…` | `1c39a53c…` unchanged |
| `quality/counters/c2-r78-runbook.py` | `b9c774b8…` | **`7e7fdc94…` — repaired mid-wave** (`90fc8d84`, `d27c5ff4`, `aea5409e`) |
| `c1-cases-r78.json` | `99f1d82f…` | unchanged |
| `c2-runbook-cases-r78.json` | `f1c75a7d…` | unchanged |

The declaration at HEAD is clean and is the frozen text plus a 14-line append-only
"Provenance notes / Known limits" section (`f7c9bf9b`; `git diff 44a36b64 -- …/claims-declaration-r78.md`
shows a pure append). Both receipts are committed: C1 at `rev=d27c5ff4`, C2 at `rev=aea5409e`
(`measurement-c{1,2}-r78.txt`, last lines). Evidence copies this report cites are in
`w1/R78CritClaims/`.

## 1. Q1 — axis classification

`AXES.md:12` defines coverage as "Fraction of the domain's real surfaces the skill governs (repo
paths, tools, edge classes)"; `AXES.md:13` defines operability as "Runnable artifacts: checklists
that are executable, commands that exist, scripts that run".

**C1 is a coverage move.** Surface: the bar-footprint domain `tools/mado-barfoot.py` can judge.
The base receipt's ten misses are exactly the ungoverned edge classes —
`reserved=NOT_MODELLED`/`verdict=UNMODELLED` on six margined/vertical/sized bars, plus
`second-consumer`, `reserved-differ`, and the refusal class
(`control-baseline-c1-r78-frozen.txt:3-8,13,15-16,18`). The move adds those surfaces; that is
coverage, not depth (depth would tighten an already-governed surface).
*Command that shows the surface unmoved:*
`python3 -I quality/counters/c1-r78-margins.py --repo . --rev f597eccb --base-rev f597eccb --controls .ufo/waves/round-78/controls/c1-cases-r78.json --scratch-root DIR`
→ `cases=18 correct=8 … verdict=TARGET_MISSED` rc 1
(`control-baseline-c1-r78-frozen.txt:21`). After: `correct=18 … TARGET_MET`
(`measurement-c1-r78.txt`, last line).

**C2 is an operability move.** Surface: the SKILL.md read-only probe rows (`SKILL.md:227-229`, the
two added rows and the dump row) as executable shape-bound probes.
*Command that shows the surface unmoved:* the frozen C2 command with `--rev f597eccb` → rc 2,
`anchor 'hyprctl activeworkspace' … not in SKILL.md` (`control-baseline-c2-r78.txt:1`).

**Lowest-axis obligation / nudge.** `SCORECARD.md:4437-4444` (round-77 §Planned, items 1–2) names
exactly these two grounds ("the margined auto exclusive-zone composition … on its own frozen set";
"the volatile probe rows as shape-checked cases … and the two captured dumps"). The round-77 axis
line (`SCORECARD.md:4446-4452`) has navigation 96/96, calibration 86/86, operability 12/12,
ledger 140/140 and a capability row at r77 within N=3, so the declaration's waiver reading
(`claims-declaration-r78.md:83-88`) is accurate. No lowest-axis defect.

## 2. Q2 — control sufficiency

### 2.1 C1: the hardcode attacks are refused; three spec gaps remain

**Attack A — anchorless hardcode.** Fixture git repo (my scratch; commit 1 = r77 tool extracted
from `f597eccb:tools/mado-barfoot.py`, commit 2 = constant-output stub). Ran the frozen C1 command
with `--repo <fixture> --rev HEAD --base-rev HEAD~1`. Observed: 18 `MADO_R78_CASE` rows then
`MADO_R78_BARFOOT: ERROR (stage=setup mutant opposite-margin-dropped anchor occurs 0 times, not
once)` **rc=2** (`w1/R78CritClaims/r78-c1-attack-anchorless.txt`). A tool without the six anchor
strings never reaches a verdict (`c1-r78-margins.py:144-149,:292-293`). The hardcode cannot score.

**Attack B — dead-anchor hardcode.** Same fixture; the stub embeds all six anchor strings once each
inside an unused string literal and prints constant output. Observed: `correct=1 mutants=7
killed=7 … verdict=TARGET_MISSED` **rc=1**
(`w1/R78CritClaims/r78-c1-attack-deadanchor.txt`). Reading rule: `killed=7/7` here is **vacuous** —
the kill rule is `dead = mcorrect < CASES` (`c1-r78-margins.py:282`), so any candidate already
below 18 collects seven "kills" without a mutation changing anything. The target conjunction
`correct == CASES and … killed == MUTANTS` (`:292-293`) is what makes the clause meaningful; the
printed clause alone is not evidence. Not a target hole; a closure rule.

**Gap C1-a (case under-enumeration).** `exclusive-false`'s `expect` is
`{band:0, box, rc:0, reserved, verdict}` — **no `expected` key** (control set, jq output in
`w1/R78CritClaims/r78-case-structure.txt`). `expected_ok` compares only declared keys
(`c1-r78-margins.py:115-124`: `all(got[key] == exp[key] for key in exp)`), so the receipt's
`expected=26` for that case is unverified. `claims-declaration-r78.md:31-32` says `correct` counts
cases whose "band, expected value … all equal the case's declaration" — overstated by one field on
this case. Case set is frozen → round-79 ground. Smallest correction: add `"expected": 26`.

**Gap C1-b (refusal under-specified).** `dynamic-cross` and `negative-margin-refused` pin only
`{error:true, rc:3}`; `expected_ok` accepts **any** `"ERROR ("` text (`c1-r78-margins.py:117-118`).
A tool refusing at setup stage (not model stage) still scores; refusal cause unverified. The claim
is "refused, never composed", so this is under-specification, not contradiction. Next freeze: pin
`stage=model`.

**Gap C1-c (rc weaker than the printed contract).** The rc-0 gate uses `base_correct < CASES`
(`:292`) and `m.group(1) == m.group(2)` (`:266`) — any n/n selftest and any base below 18 pass —
while the frozen predicate prints exact `base_correct=8/18 tool_selftest=22/22`
(`claims-declaration-r78.md:29-31`). A closure that trusts only rc 0 admits a line that deviates
from the frozen predicate. Closure must string-compare the `MADO_R78_BARFOOT:` line.

### 2.2 C2: the frozen control was insufficient; the repaired control is sufficient; the repair is the open judgment

Zero-work control: rc 2 at base — separates "did nothing". Accept-everything control: every one of
the 17 cases carries ≥1 negative and every shape case ≥1 churn sample (jq table,
`w1/R78CritClaims/r78-case-structure.txt`), so a universal-accept `matches()` fails all 17; the
"churn clause never runs" attack fails. ✓

**Counterexample (the finding).** Fixture: a git repo whose only file is `SKILL.md` = the 17
`skill_anchor` strings, one per line, 314 bytes, no table. Command: the frozen C2 command with
`--repo <fixture> --rev HEAD`, executed against the **brief-pinned** counter `b9c774b8…`
(`git show 44a36b64:quality/counters/c2-r78-runbook.py`). Observed:

```
MADO_R78_RUNBOOK: cases=17 executed=17 matched=17 shapes=12/12 anchors=17/17 control=5/17 mutants=5 killed=5 verdict=TARGET_MET
rc=0
```

(`w1/R78CritClaims/r78-c2-attack-bare-anchor-frozen.txt`). Against the pinned instrument the
SKILL.md side of "binds its volatile rows by shape" is file-wide substring presence
(`if case["skill_anchor"] not in skill`, frozen:365; `anchors += 1 if … in skill`, frozen:378).
The shape knowledge the verdict measures lives entirely in the **pre-frozen** case set; the only
anchors absent at base were two (`control-baseline-c2-r78.txt:1`), so C2's SKILL.md work could
have been satisfied by two appended lines with no claim of a shape-bound row. This is the
"do-nothing for the claimed rewrite" path; it exists in the frozen design.

The wave found the same hole independently (commit `d27c5ff4`, "anchor check bound to the table
row") and repaired it. Same fixture against the repaired counter (`7e7fdc94…`): **rc=2**,
`ERROR (stage=setup anchor 'hyprctl version' … not in a SKILL.md table row …)` for all 17 anchors
(`w1/R78CritClaims/r78-c2-attack-bare-anchor-repaired.txt`). `row_bound` is at
`quality/counters/c2-r78-runbook.py:249`, used at `:399`.

**Residual C2 row-identity weakness (both versions).** The binding is existential over rows and
per-substring: 17 cases use **13 distinct anchors** (`hyprctl monitors` ×3, `hyprctl getoption
<key>` ×2, `hyprctl layers -j` ×2). Both dump anchors already existed at base (`SKILL.md:210,213`)
and appear again at `:229`; deleting row 229 would not be detected. `anchors=17/17` is a tautology
after the gate (substring is implied by row_bound). Next freeze: per-case distinct anchors (e.g.
the row's full command cell) — or declare the binding presence-only.

**Kill rule.** `dead = mrc != 0 and (mm is None or mmatched < CASES)`
(`c2-r78-runbook.py:436-437`) — same conjunction dependence as C1; meaningful only under
`matched == CASES`, which the target pins (`:444-446`). OK.

**Gap C2-d (rc weaker than the printed contract).** `control_total < CASES` (`:445`) vs printed
`control=5/17`; a host where more rows are stable prints a different value with rc 0. Same class
as C1-c.

### 2.3 C1 baseline provenance — found, and already remedied at `307c125a`

`claims-declaration-r78.md:36-39` says the do-nothing control was measured "with the same counter
and case set" and cites `control-baseline-c1-r78.txt`. Counter: true
(`b8508bd9:quality/counters/c1-r78-margins.py` = `1c39a53c…` = frozen). Case set: **false** for
that receipt — it prints `MADO_R78_CONTROL: sha256=d19c20e2…`, the `b8508bd9` blob, not the frozen
`99f1d82f…` (`git show b8508bd9:…/c1-cases-r78.json | sha256sum` → `d19c20e2…`). The separation
is nonetheless re-derived under the frozen set inside the primary receipt (`MADO_R78_BASE:
correct=8/18`, control sha `99f1d82f…`), and the wave's `307c125a` committed
`control-baseline-c1-r78-frozen.txt` (21 lines, control sha `99f1d82f…`, `correct=8 … TARGET_MISSED`
rc 1). Substance resolved; the declaration sentence still cites the pre-freeze receipt — an
append-only pointer to the frozen-set receipt is the smallest correction.

## 3. Q3 — causal separability

Inputs are disjoint by code: C1 reads `tools/mado-barfoot.py@rev`, the base blob at
`f597eccb`, and its control set; C2 reads `SKILL.md@rev` and its control set and executes live
probes. Neither counter reads the other's bytes. Landing one without the other: a rev with only C2
landed ⇒ C1 honestly reads `correct=8 base_correct=8` rc 1 (no false pass); a rev with only C1
landed ⇒ C2's anchors absent ⇒ rc 2. ✓ The wave's commit sequence touches both receipts, the
SCORECARD row and the ledger — integration order, not causal coupling; each verdict re-derives
from its own artifacts. No coupling found.

## 4. Q4 — one value over committed bytes; universal clauses

- **C1: ✓ deterministic over committed bytes**, one command (fixtures only). With the C1-c caveat:
  rc 0 is necessary, not sufficient; compare the printed line to the frozen predicate.
- **C2: ✗ by construction** — `executed` are live probes (`c2-r78-runbook.py:407`); on a host
  without the session the same bytes yield `matched < 17` rc 1. The declaration concedes "point
  sample of this host at measurement time" and the append repeats it. Acceptable as an operability
  tradeoff **only if** the round report states the host scope.
- **Instrument-pin identity (the sharper failure):** the brief's `b9c774b8…` equals no committed
  counter at HEAD (`7e7fdc94…`). A closure following the brief fails its sha check; a closure
  following the tree measures a different instrument than the brief froze. §5.

Universal clauses the predicates do not enumerate:

1. C1 "band, expected value … all equal" — `exclusive-false` (missing `expected`); the two refusal
   cases have no band/box/expected at all.
2. C1 printed `base_correct=8/18` and `tool_selftest=22/22` — enforced as `< CASES` and
   `numerator == denominator` (`:266,:292`).
3. C2 `killed=5/5` — vacuous below `matched=17` (C1 Attack B printed `killed=7/7` at
   `correct=1/18`).
4. C2 `anchors=17/17` — tautological after the gate; per-case row identity unverified; 13 distinct
   anchors for 17 cases; shape *language* in SKILL.md unverified by any clause (the shape lives in
   case kind/value — honest if the report says so).
5. C2 `control=5/17` — enforced `< 17`.
6. C2 churn/negative clauses **are** fully enumerated: samples ≥1 on all 12 shape cases, negatives
   ≥1 on all 17. No gap.

## 5. Mid-wave freeze event — the fork the canonical judge must rule

Sequence: `44a36b64` (frozen) → `90fc8d84` (`observed()` stops quoting JSON dumps — a label
change) → `d27c5ff4` (`row_bound` — anchor predicate) → `3eb518a5`/`aea5409e` (matcher predicates:
bare-digit ints, padded list parts refused; selftest 40/40) → `f7c9bf9b` (dispositions, declaration
append) → `307c125a` (frozen-set baseline) → `edb4159b` (serial redaction).

`claims-declaration-r78.md:5-7`: "the predicates, counters, control sets and targets below do not
change after the first measurement. Instrument repairs during the wave may not touch a predicate,
case, label, kill rule or target". The repairs touch predicates and a label.

For the defense: the frozen claim text itself says the probes are "bound to their committed
`SKILL.md` table rows" (`claims-declaration-r78.md:50`); `b9c774b8` under-enforced that claim (my
§2.2 counterexample is the proof); the repair makes enforcement equal the frozen wording; every
count is unchanged (17/17, 5/17, 5/5); the append documents the event; the C1 instrument and both
control sets never moved.

Judgment fork:

- **(a) Accept as enforcement alignment** — then the round report must update the instrument pin to
  `7e7fdc94…` and the receipt rev to `aea5409e…`; the brief's "never rewritten by a seat" line
  must not stand against a rewritten counter.
- **(b) Reject as predicate change** — revert the counter to `b9c774b8…`, keep the substring hole,
  declare it round-79 ground (the connector finding still lands next round).

Either branch is defensible. Leaving both live — brief pins one sha, tree ships another — is the
one outcome that cannot stand: an identity change.

## 6. Smallest safe corrections, ordered

1. Resolve §5 explicitly and update the brief's instrument pin (or revert). Record the repaired
   sha and the receipt revision in the round report either way.
2. Round report: (i) C2's verdict is host-scoped; (ii) the row-binding residual (13 anchors for 17
   cases, dump-row identity); (iii) closures compare the printed `MADO_R78_*` line, not only rc.
3. Append a pointer from `claims-declaration-r78.md:36-39` to
   `control-baseline-c1-r78-frozen.txt`.
4. Next freeze: `exclusive-false` gains `"expected": 26`; refusal cases pin `stage=model`;
   per-case distinct anchors; pin `base_correct == 8` and `control == 5` in rc (or drop them from
   the printed contract).
5. C1 target needs no change; it separates under the frozen conjunction.

## 7. What this seat did and did not do

No repo edit, no commit, no mutating git/jj. Two attack fixtures lived under my scratch (each
`git -C` asserted to its fixture dir); the only live commands were the frozen case argv (read
verbs) executed by the counters themselves. No session material printed: JSON-kind probe outputs
were kept out of my transcripts and receipts (counts only); the wave's own `edb4159b` records the
same privacy concern. Scratch deleted after copying receipts into `w1/R78CritClaims/`.

Impacted axes: coverage measurement strength (C1-a/C1-b), operability measurement coverage
(C2 row identity), calibration (rc-vs-line closure rule; freeze event), freshness/identity (the
brief's pin vs the tree).
