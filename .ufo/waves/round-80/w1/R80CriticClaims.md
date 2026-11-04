# R80CriticClaims — falsifying C1 and C2 as DECLARED (round mado 80, wave 1)

Method: the frozen instruments were never touched. Every experiment ran either the frozen
counter unmodified or a labelled lab copy derived from it by the scripts in this directory
(`make-c1-critic.py`, `make-c2-critic.py`, `doctor-c1.py` → `c1-critic.py`, `c2-critic.py`),
with all knobs printed on the tool (`--tool`, `--base-tool`, `--skip-carried-comparison`,
`--before`, `--no-tree-check`). Doctored control sets are in `evidence/doctored-*.json`; the
sha-verified r79 tool copy and the two one-line variants are in `evidence/`. All writes stayed
inside `w1/R80CriticClaims/` and `/fast/scratch/hyaku/mado-r80/R80CriticClaims/` (scratch
removed at the end; the lab files above are kept here so every number below is re-runnable).

## C1 — coverage: predicate, kill rule, do-nothing control (restated)

- **Predicate:** the successor counter prints `correct=33`, `killed=22`, `base_correct=23/33`,
  `carried=23/23`, a green tool selftest, `verdict=TARGET_MET` at `6c302a53`, exit 0.
- **Kill rule:** any of `correct < 33`; `killed < 22`; `base_correct != 23`; `carried != 23/23`;
  red selftest → claim fails, honest stop.
- **Do-nothing control:** the base revision's r79 tool (`9e274157…`) scored by the same counter
  on the same 33 cases; it has no `--surfaces`, so the ten new cases error: 23/33 (frozen
  receipt `receipts/control-c1-r80-at-base.txt`; reproduced bit-identically by the lab copy,
  `base_sha256=9e274157…`).

### Q1a — is 23/33 really the cheapest skip? (one-line edit of the r79 tool)

**Verdict: the control is the cheapest skip — a one-line edit buys exactly zero.** Two variants
of the cheapest conceivable evasion, both scored by the counter on the frozen set:

| variant | one-line diff | sha256 | base_correct |
|---|---|---|---|
| pristine r79 tool | none (sanity) | `9e274157…` | 23/33 |
| `tool-1line-arg.py` | `ap.add_argument("--surfaces")` (accept and ignore) | `f90d8a3f…` | **23/33** |
| `tool-1line-known.py` | `ap.parse_known_args(argv)[0]` (ignore unknown flags) | `e08d2799…` | **23/33** |

Command (lab copy; identical numbers via the frozen base line):
`python3 -I evidence/c1-critic.py --repo . --rev 6c302a53… --base-rev e10f7e9f… --controls .ufo/waves/round-80/controls/c1-cases-r80.json --carried .ufo/waves/round-79/controls/c1-cases-r79.json --scratch-root … --base-tool evidence/tool-1line-arg.py --no-mutants`

Why zero: the r79+1-line model still prints the single-surface RESULT shape, and **every one of
the ten new cases pins multi-surface fields the r79 printer cannot emit** — `boxes` (all ten;
`boxes=MATCH,MATCH` or `MATCH,SKIP`), `attributed`/`gt`/`attr`/`ls` (nine; `ls-area-invalid`
pins `attributed=2026`+`ls=INVALID`), `attr_ns` (six). Five new cases even coincide on `band=26`
(anchor-unmatched, overlay-unexclusive-full, negative-margin-skip, empty-box-skip,
full-box-vs-usable) and still fail on `boxes` alone; the other five fail on `band` (66/66/62/56/0)
and `verdict` besides. The case set discriminates on the *shape of the join*, not just the
number — no hole here; this part of the claim survives its cheapest attack.

### Q1b — is `carried=23/23` load-bearing or tautological?

**Verdict: load-bearing, but only as a tamper guard over the 23-case prefix, and only if the
`--carried` path is procedurally trusted; tautological as a measurement clause; and mechanically
vacuous for the ten NEW cases.**

- For honest runs it is tautological: the frozen set is constructed to satisfy it, so removing
  the comparison changes no honest score (constant-true on the frozen inputs).
- What breaks if it is removed — demonstrated at both ends:

```sh
# tamper: weaken one carried expectation (bottom-bar expect.band 30 -> 31), prefix only
# (a) comparison intact (frozen counter): GUARD BITES
python3 -I quality/counters/c1-r80-multisurface.py --repo . --rev 6c302a53… \
  --base-rev e10f7e9f… --controls evidence/doctored-controls-prefix.json \
  --carried .ufo/waves/round-79/controls/c1-cases-r79.json --scratch-root …
# -> ERROR (stage=setup the successor set does not carry the frozen round-79 cases unchanged)  rc 2

# (b) comparison removed (lab knob --skip-carried-comparison): SILENT WRONGFUL REJECT
# same files, honest r80 candidate -> correct=32, verdict=TARGET_MISSED, NO refusal:
# a tampered set undetectably flips an honest tool's verdict (rc 1, no trace but the sha).

# (c) weakening tamper: DELETE bottom-bar.expect.reserved (a weaker constraint the honest
#     tool still satisfies), comparison removed, WITH mutants:
python3 -I evidence/c1-critic.py … --controls evidence/doctored-controls-weaken.json \
  --carried .ufo/waves/round-79/controls/c1-cases-r79.json --skip-carried-comparison
# -> cases=33 correct=33 mutants=22 killed=22 base_correct=23/33 carried=23/23
#    tool_selftest=111/111 verdict=TARGET_MET   (rc 0 by the exit map)
# a silently weakened frozen set fully certifies. THE hole if the comparison is removed.
```

- The guard's boundary — the ten new cases have NO mechanical pin. With the comparison INTACT,
  the genuine r79 carried file, and a controls copy whose ten new-case expects were re-derived
  from the do-nothing one-line tool (`evidence/doctored-controls-new.json`,
  `doctor-c1.py`), the counter prints `correct=33 carried=23/23 base_correct=23/33
  tool_selftest=50/50 … tool_sha256=f90d8a3f…` — the do-nothing tool is one clause away from
  full certification, and the clause that blocks it is the mutant count failing for a STRUCTURAL
  reason, not because the tamper was caught: `killed=12`, all ten composition mutants
  `reason=anchor-absent`, because the mutants are cut from the **candidate's own source**, so
  any candidate substitution voids them mechanically. Against the honest r80 candidate a
  new-case weakening is partially self-limiting (weakened expects let composition mutants
  survive, dropping `killed` below 22) — but nothing in the predicate or kill rule references
  the control-set bytes at all: `control_sha` is printed and never compared, and `--controls`
  / `--carried` are unpinned paths (demonstrated: the doctored files are accepted silently;
  detection is only a human diff of the printed sha against `17c27157…` in the declaration).

**Smallest safe correction:** add two mechanical clauses to the predicate/kill rule (or enforce
them in the counter): `controls sha256 == 17c27157…` and `carried sha256 == <frozen r79 sha>`.
One line each; closes the weakening hole, the path-substitution hole, and puts the ten new
cases under the same pin the declaration already claims procedurally.

## C2 — operability: the declared before-state (rc 2)

### Q1c — verdict or setup refusal?

**Plainly a setup refusal — by the instrument's own definition, never a verdict.** The frozen
receipt (`receipts/control-c2-r80-at-base.txt`) and my reproduction both print
`ERROR (stage=setup SKILL.md in the working tree is not the measured revision's bytes)`, rc 2;
the counter's own exit map says "2 setup error (never a verdict)". No case is executed; nothing
is scored. Worse, the refusal is STRUCTURAL, not merely the tree gate — with the tree check
waived the counter refuses again:

```sh
python3 -I evidence/c2-critic.py --repo . --rev e10f7e9f… --controls …c2-runbook-cases-r80.json \
  --carried …c2-runbook-cases-r79.json --scratch-root … --no-tree-check
# -> ERROR (stage=setup the runbook section carries 22 command rows, frozen target expects 24) rc 2
```

`CASES=24`, the round-80 literal section title, and the per-case 1:1 anchor binding are all
pinned to the after-state, so the frozen instrument cannot score the base revision at all, at
any tree. **The claim's before→after is therefore NOT measurable as a verdict pair as
declared**: before = refusal (no score), after = TARGET_MET; both do-nothing controls are also
refusals (the held r79 instrument: "carries 24 cases, frozen target expects 22", rc 2) or an
observation about the held r78 rule (`control_new=0/2`), never a scored before. The claim is
one-sided: after-only + mutant kills. Note also the tree-binding clause inside the kill rule is
an integrity gate, not a measurement — at the current lane tip (`2c1a37de`; tree SKILL.md
`e7412d8c…` ≠ rev `0702f8d0…`, tool `5b9e2930…` ≠ `c3eb5fbe…`) the frozen C2 command refuses
even for the AFTER run; in a fresh clone detached at the frozen rev it reproduces
`verdict=TARGET_MET … tree=bound` (demonstrated). The receipt is the durable record; the live
command is time-bound to the tree.

**Cheapest honest fix (proposed, not implemented in any frozen instrument; demonstrated on the
labelled lab copy `c2-critic.py --before`):** score the rev's own bytes instead of refusing —
(1) key the section by `### Executable runbook rows \(round \d+\)`; (2) treat a zero-hit anchor
as an unbound case (printed `row=-1`) instead of a setup refusal; (3) waive the tree binding
for the before-run. ~6 lines on a copy. Demonstrated result at the base rev:

```
MADO_R80_PROBE: name=keybindings-chords row=-1 kind=chord_shape match=yes rc=0 …
MADO_R80_PROBE: name=hypridle-is-active row=-1 kind=is_active match=yes rc=3 out='inactive'
MADO_R80_RUNBOOK: cases=24 executed=24 matched=24 shapes=19/19 anchors=22/24 rows=22/24
                  control_new=0/2 verdict=TARGET_MISSED rev=e10f7e9f… tree=relaxed   (rc 1)
```

The honest before-failure is a row-EXISTENCE failure — both new commands already run and match
on the host; only their runbook rows are missing — which is exactly the operability claim's
shape (rows that can be run and bound), and it gives the round a real before→after:
`rows=22/24 → 24/24`.

## Q2 — causal separability and shared dependencies

- **C1 without C2: separable.** The c1 counter never reads SKILL.md and never executes a
  runbook row; its inputs are tool bytes at `--rev` plus the control files. Every C1 run here
  exercised C1 alone.
- **C2 without C1: subject-separable, measurement-coupled.** Four of C2's 24 cases execute the
  C1 instrument (the refusal probes) and C2's setup hashes `tools/mado-barfoot.py` tree-bytes
  against the rev. **The asymmetric failure is live right now:** at the drifted lane tip the
  frozen C2 refuses (rc 2, tree gate) while the frozen C1 at the same rev still scores

```
MADO_R80_BARFOOT: cases=33 correct=33 mutants=22 killed=22 base_correct=23/33 carried=23/23
                  tool_selftest=111/111 verdict=TARGET_MET rev=6c302a53… tool_sha256=c3eb5fbe…
```

  because C1 is rev-pinned (`git show rev:path`) and tree-blind by construction. So any byte
  change to C1's instrument — even a comment — or any tree movement fails C2 without touching
  C1; a C2-side SKILL.md row edit fails C2 only; only a behavioral refusal-contract change
  (rc or `stage=` token) hits both (each pins rc 3 + `ERROR (stage=model `).
- **Shared dependency that can make one fail with the other:** the tree-binding gate over the
  same two files, plus the shared rev pin and the case-count constants (both counters refuse
  rc 2 on successor-set drift — the mechanism the C2 held-instrument control demonstrates).
- **Verdict:** the two claims are causally separable in subject matter (each verifiable without
  the other landing), but not independent as measurements: C2's verdict is gated on C1's
  instrument bytes sitting exactly in the tree. Naming the coupling is enough; no correction
  needed beyond awareness at integration time.

## Q3 — axis naming against AXES.md

- AXES.md: **coverage** = "fraction of the domain's real surfaces the skill governs (repo
  paths, tools, edge classes)"; **operability** = "runnable artifacts: checklists that are
  executable, commands that exist, scripts that run; a checklist item can be run and produces
  the stated outcome."
- **C1 is genuinely coverage-shaped**: the moved artifact is the diagnostic tool's model
  gaining the second-surface composition — arrangement order, exclusive-edge attribution,
  invalid-area void, skip guards — and the ten new cases are exactly new edge classes. The
  counter is measurement scaffolding, not the moved artifact, so this is not "instrument work"
  in the axis sense. **Caveat worth recording:** the lane's existing coverage rubrics (U-route
  7/7, rubric V 6/6) are untouched; C1's ground is a new diagnostic model-space with its
  denominator being the frozen 33-case set, declared without a SCORECARD rubric row. Defensible
  under "edge classes", but the L1 must not book it as a move of an existing coverage score —
  that would be false provenance.
- **C2 is genuinely operability**: the runbook gains two rows that can be run and whose stated
  outcome is bound (chord grammar, state/exit-status agreement), with committed negatives so
  the rule can fail. The matcher classes are the measure; the rows are the moved artifact.
- Distinct axes per AXES.md ("two claims on one axis in one round count as one claim") — the
  distinctness holds.

## Other observations (not holes in the claims)

- The frozen c1 counter accepts `--no-mutants` and silently ignores it (the mutant loop always
  runs) — dead flag, harmless, worth deleting or honoring next generation.
- The lane receipts dir gained an untracked file during the wave,
  `.ufo/waves/round-80/receipts/control-c1-r80-parser-stub.txt` (not mine; unregistered) —
  L1 hygiene item.
- Piping counter output through `grep` in my early commands masked process exit codes; where
  this file quotes a verdict it quotes the printed contract line, whose rc the exit map
  defines (TARGET_MET ⇔ rc 0).

## Verdict summary

| Question | Verdict |
|---|---|
| Q1a C1 control = cheapest skip? | HOLDS — two one-line evasions score exactly 23/33; new cases pin multi-surface fields |
| Q1b carried load-bearing? | PREFIX-ONLY tamper guard; tautological as measurement; new cases mechanically unpinned; removal → silent `TARGET_MET` on a weakened set (demonstrated); fix = sha clauses |
| Q1c C2 before-state | SETUP REFUSAL, never a verdict; structurally unscorable at base; before→after not measurable as declared; honest fix demonstrated: scored base = `rows=22/24 verdict=TARGET_MISSED rc 1` |
| Q2 separability | Subject-separable; C2's measurement coupled to C1's instrument bytes via the tree gate (live asymmetric failure at the drifted tip) |
| Q3 axis naming | coverage/operability naming holds; caveat: C1 books no rubric row — do not book it as an existing-coverage score move |

STATUS: ok — nothing missing; all demonstrations re-runnable from `evidence/` with the commands above.
