# mado round 86 — claims declaration (frozen before data)

Lane: mado-shokunin, hyaku run 15, round 86, **fresh start** (r83, r84 and r85 were rejected; r85
was an honest stop with C1 admitted and C2 unverified). Read before declaring: `corpus/lessons/
round-85-verifier-spotcheck.md` (routed defects R1–R7), `corpus/lessons/round-84-verifier-spotcheck.md`,
`corpus/lessons/round-83-verifier-spotcheck.md`, `corpus/lessons/round-85.md`, and the 2026-11-04
`considerthese/` reflection.

- **Base revision** (lane `master` tip at round start, clean tree): `a722c60493f24f83429112e9123058835b2cdd82`
- **Freeze revision**: the commit that carries this declaration, the two counters, their control
  sets and the new runbook row. It is named in the report; nothing in this file is edited after a
  seat has scored.
- **Do-nothing controls** are built and committed **before** the candidate measurements
  (receipts under `.ufo/waves/round-86/receipts/control-*`), per the r84/r85 routed defects.

## Claims (2)

| # | Axis | One-sentence claim |
|---|---|---|
| C1 | calibration | The lane's refusal counter stops scoring a *substring* and starts scoring a *record*: a tool that prints every cause token among the honest answer is refused, while the held round-85 rule still gives it full marks. |
| C2 | operability | The runbook counter observes the clauses that judged each row (sample loop, negative loop, line-anchor branch) and carries the witness the two round-85 anchor survivors needed, so its own 37-mutant population dies 37/37 instead of 33/37. |

Distinct axes (calibration vs operability), distinct instruments (`quality/counters/c1-r86-refusal-records.py`
scores `tools/mado-barfoot.py`; `quality/counters/c2-r86-clause-observations.py` executes SKILL.md
runbook rows), distinct controls and distinct counters. Each verifies without the other landing:
C1 needs no SKILL.md row and C2 needs no barfoot change.

Operability is the lane's lowest non-retired axis (coverage/operability tie at 9.0/10 in
`SCORECARD.md`); C2 works it, so the lowest-axis obligation is met. The stagnation nudge does not
apply (a capability row entered round 81; window N = 3).

### C1 — calibration: refusal records, not cause substrings

**Why the prior state lacked it.** `quality/counters/c1-r85-identity-causes.py` bound a refusal with
`(" cause=%s " % cause) in stdout`. An all-cause flooding tool therefore scored 72/72 (r85 spot-check
§C1, `w1/R85ReviewerC1.md:37,43`; QUALITY 141 names the fix and supplies no detector). A gate that
cannot tell a record from a flood overreaches every claim it prints.

**Target (frozen predicate).**

```sh
python3 -I quality/counters/c1-r86-refusal-records.py --repo . --rev REV \
  --base-rev 2b6dd76b65de4dfe701db87db13b7e448b3538ee \
  --controls .ufo/waves/round-86/controls/c1-cases-r86.json \
  --carried .ufo/waves/round-85/controls/c1-cases-r85.json \
  --scratch-root /fast/scratch/hyaku/mado-r86/<seat>/c1
```

```
MADO_R86_REFUSALS: cases=75 correct=75 mutants=51 killed=51 carried=72/72 tool_selftest=152/152 \
  flooding=<k>/75 held_flooding=75/75 verdict=TARGET_MET rev=<freeze> tool_sha256=<sha>
```

rc 0 iff `correct == 75` **and** `killed == 51` **and** `carried == 72/72` **and** the tool selftest
is green **and** `flooding < 75` **and** `held_flooding == 75`.

**Kill rule (frozen).** The claim misses if any clause is false: a candidate rule that leaves the
flooding tool at 75/75, that scores the honest tool below 75/75, that loses a carried case, or that
lets a declared mutant survive. A survivor is a hole in the counter, not a footnote.

**What the counter binds.** The refusal record `^MADO_BARFOOT: ERROR \(stage=(setup|model)( cause=<tok>)? `
must occur **exactly once**; its stage must equal the expected stage; its cause must equal the
expected cause where the case binds one; and no token of the ten-token vocabulary may appear
anywhere in stdout outside that record's own cause field (the negative observation). Three witnesses
are appended to the carried 72: `alloc-negative-cause`, `alloc-bool-cause` (a JSON boolean is not a
band) and `alloc-float-band` (a JSON float is not an integer).

**Controls (pre-freeze, committed).**
1. *Flooding forgery* — the honest tool plus `MADO_BARFOOT: FLOOD: <all ten tokens>` printed before
   both refusal records, built deterministically by the counter from the tool source. Held r85 rule
   scores it 75/75; the r86 rule scores it 48/75 (only the 48 non-refusal cases pass).
2. *Held tool* — `tools/mado-barfoot.py` at `2b6dd76b` (r85 measured content) scores 75/75 under the
   r86 rule: the increment is the **rule**, not the tool, and the report says so.
3. *Carried set* — the 72 r85 cases are carried parsed-equal (checked in the counter, `carried=72/72`).

### C2 — operability: clause observation and the anchor witness

**Why the prior state lacked it.** `quality/counters/c2-r85-status-classes.py` matched 36/36 while
four of its own mutants survived (`negatives-skipped`, `samples-skipped`, `regex-anchor-dropped`,
`line-anchor-prefix`; `receipts/final-c2-r85.txt` — 33/37). Deleting a conjunct cannot lower an
already-perfect score, and both frozen anchor patterns already carried `^`/`$`, so the anchor
branch was never the discriminator (r85 spot-check routed defect R1).

**Target (frozen predicate).**

```sh
python3 -I quality/counters/c2-r86-clause-observations.py --repo . --rev REV \
  --controls .ufo/waves/round-86/controls/c2-cases-r86.json \
  --carried .ufo/waves/round-85/controls/c2-cases-r85.json \
  --scratch-root /fast/scratch/hyaku/mado-r86/<seat>/c2
```

```
MADO_R86_RUNBOOK: cases=37 executed=37 matched=37 shapes=27/27 anchors=37/37 rows=37/37 \
  clauses_observed=37/37 superseded=<declared> mutants=37 killed=37 verdict=TARGET_MET rev=<freeze> tree=bound
```

rc 0 iff `matched == 37`, `shapes == 27`, `bindings == 37`, `clauses_observed == 37` (every case's
observed sample/negative/anchor counts equal its declared populations) and `killed == 37`.

**Kill rule (frozen).** The claim misses if any of the four round-85 survivors lives, if any case's
declared clause is not observed, if the new witness is not matched, or if the working tree is not
the measured revision's bytes (`tree=bound` fails closed).

**What the counter binds.** The round-85 section is carried **byte-identical** (its own instrument
keeps its 36-row contract) and a new `### Executable runbook rows (round 86)` section adds one row:
`set -o pipefail; hyprctl getoption general:border_size -j | jq -r .int`, kind `regex`, value
`[0-9]+` (unanchored), `anchor: line`, samples `1`,`2`, negatives `0 extra`, `-1`, rc-127 `0`. A
substring search accepts `0 extra`; the whole-line rule refuses it. `case_correct` observes the
clause counters and refuses a case whose declared clause did not run.

**Controls (pre-freeze, committed).**
1. *Held rule on the new witness* — the round-85 rule (regex = substring search, no clause
   observation) scores `border-size-int` **0/1**; printed as `held_rule_new_case=0/1`.
2. *Held instrument at the new tree* — `c2-r85-status-classes.py` executes its own 36 rows at the
   freeze tree and still reports 33/37 kills: the four survivors are measured at the base, not
   asserted from the receipt.
3. *Carried set* — the 36 r85 cases are carried parsed-equal under the declared supersession fields.

## Sources this round (one per claim)

- **S491** RFC 7493 (I-JSON) §2.3 — "Objects in I-JSON messages MUST NOT have members with duplicate
  names." Grounds C1's duplicate-identity refusal class as a *specification* constraint (RFC 8259
  §4 only says SHOULD; S486 holds that weaker row). Fetched 2026-11-04,
  `.ufo/waves/round-86/fetch/S491.bin`, sha256 `a44ccf14…`, 12,849 B, quote at line 159.
- **S492** CPython v3.14.8 `Doc/library/re.rst` — "If the whole *string* matches the regular
  expression *pattern*, return a corresponding Match." Grounds C2's whole-line rule as `fullmatch`
  semantics rather than a search. Fetched 2026-11-04, `.ufo/waves/round-86/fetch/S492.bin`, sha256
  `d252cc18…`, 78,262 B, quote at line 957.

Both are opened and pinned this round; the Gate block in `corpus/lessons/round-86.md` carries the
access date, URL, byte offsets and ≤25-word quotes, plus at least one reject.

## Not claimed this round (named, not silently dropped)

- The join's extra-surface allocation arm (SCORECARD r82/r83 planned ground) — routed to r87.
- `considerthese/2026-11-04.md` proposal 2 (bind a published claim row to a red wave-done receipt) —
  still unimplemented; the 2026-11-04 reflection's figures are relayed, not re-measured here.
- Markdown status/outcome cells of the runbook table stay unbound (r85 R3): the counter binds the
  command and its live output, never the prose cell.
- `corpus/SOURCES.md` W04 duplicate-URL warnings stay as recorded warnings; no row is superseded
  this round.
