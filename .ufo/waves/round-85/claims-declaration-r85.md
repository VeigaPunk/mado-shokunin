# round 85 — declaration, frozen before any score

Lane mado, hyaku run 15. Base `5f174ca48d4f9cf94abf1a8c58b7d6f88733aced` (lane branch tip after
the round-84 closure and its non-author spot-check). Two claims, distinct axes, causally
separable. The round-84 routed defects R1–R4 are answered inside C1/C2 and the lesson; no
round-84 frozen population is widened.

Axis selection: the lane's lowest non-retired measured axes are **coverage** and **operability**
(ties, SCORECARD round 84). C1 works coverage on the layer join's declaration-identity surface;
C2 works operability on the executable runbook's producer-status surface. Saturation line 9.0 and
stagnation window N=3 are unchanged; no axis is retired.

## C1 — coverage: declaration-identity refusals carry their own cause

**Surface named, not the number.** `tools/mado-barfoot.py` refuses a declaration whose identity
is ambiguous. Round 84 bound only the refusal *stage* (`setup` / `model`), so a tool that refused
the right stage for the wrong reason scored; the round-84 reviewer's three anchor-preserving
cheats (equal-valued duplicate collapse, non-adjacent duplicate collapse, level-qualified extra
identities) and its casefold over-refusal survived that population.

**Predicate (one sentence).** Over the 72-case frozen set, `tools/mado-barfoot.py` at the
measured revision refuses each identity witness with its declared `cause=` token and its declared
stage, accepts the case-distinct-names pair as two surfaces, and every declared mutant of the
scoring counter dies.

**Frozen cause vocabulary** (ten tokens; a refusal that is not one of these carries no token and
is not scored):

| cause | stage | class of declaration defect |
|---|---|---|
| `alloc-duplicate-key` | setup | the `--allocation` object repeats a namespace key — adjacent, interleaved or equal-valued |
| `alloc-not-object` | setup | the allocation declaration is not an object |
| `alloc-empty-namespace` | setup | the allocation declaration carries an empty key |
| `alloc-non-integer` | setup | an allocation band is not an integer |
| `alloc-negative` | setup | an allocation band is negative |
| `alloc-unknown-namespace` | setup | an allocation key names no declared surface (exact string; case variants do not resolve) |
| `namespace-duplicate-bar` | setup | an extra surface repeats the bar's namespace |
| `namespace-duplicate-surface` | setup | two extra surfaces repeat a namespace at one level |
| `namespace-duplicate-cross-level` | setup | two extra surfaces repeat a namespace at different levels |
| `live-duplicate-surface` | model | the layer capture carries two entries with the declared namespace at its declared level |

**Population.** `.ufo/waves/round-85/controls/c1-cases-r85.json`: 72 cases = the 61 frozen
round-84 cases carried parsed-equal + 11 identity witnesses
(`alloc-dup-key-equal`, `alloc-dup-key-interleaved`, `alloc-not-object`, `alloc-non-integer`,
`alloc-empty-namespace`, `alloc-unknown-case-variant`, `ns-dup-bar`, `ns-dup-surface`,
`ns-dup-cross-level`, `ns-case-distinct-accepted`, `live-dup-surface`). Every witness declares
`expect.cause`; the accept case declares no error and binds the composed verdict.

**Target.** `cases=72 correct=72 mutants=51 killed=51 base_correct=62/72 carried=61/61
tool_selftest=p/p`.

**Kill rule.** A mutant is killed when it scores fewer than 72/72 cases. The 51 declared mutants
are the 41 round-84 mutations (re-anchored only where the round-85 cause argument moved the rule
line) plus ten identity mutants: `dup-key-equal-collapsed`, `dup-key-interleaved-collapsed`,
`alloc-dup-cause-collapsed`, `cause-dropped`, `ns-dup-cause-collapsed`, `ns-dup-level-blind`,
`ns-dup-surface-accepted`, `ns-case-folded`, `alloc-case-folded`, `live-dup-first`. Mutant text
is declared in `quality/counters/c1-r85-identity-causes.py`; an anchor that does not occur exactly
once is a setup refusal, never a pass.

**No-work control.** The held round-84 tool scored with the same frozen counter is the control:
it refuses the right stages but prints no cause, so it must score 62/72 (measured at the base
revision; see `receipts/control-c1-r85-base.txt`). A counter that dropped the cause clause would
meet the target, so `cause-dropped` is a declared mutant and must die.

**Counting command.**

```sh
python3 -I quality/counters/c1-r85-identity-causes.py --repo . --rev REV \
  --base-rev 5f174ca48d4f9cf94abf1a8c58b7d6f88733aced \
  --controls .ufo/waves/round-85/controls/c1-cases-r85.json \
  --carried .ufo/waves/round-84/controls/c1-cases-r84.json --scratch-root DIR
```

## C2 — operability: the runbook binds the producer's status class

**Surface named.** The `SKILL.md` executable runbook rows. Round 84 guarded fifteen pipelines
with `set -o pipefail` but scored their producer status behind one blanket rule (`rc != 0` is a
failure); the round-84 mutation tester's `any-nonzero` and prefix-text survivors passed 33/33.

**Predicate (one sentence).** Over the 36-row frozen set, each row is executed against the
committed row it documents, its output meets the row's declared outcome under its declared
status class, every committed churn sample still matches, every committed negative sample is
refused, and every declared mutant of the scoring counter dies.

**Frozen status classes** (three; a row declares exactly one):

| class | bound status |
|---|---|
| `ok` | exit 0 |
| `exact` | one named nonzero exit code |
| `signal` | death by one named signal, reported by a POSIX shell as 128+N |

**Population.** `.ufo/waves/round-85/controls/c2-cases-r85.json`: 36 rows = the 33 frozen
round-84 rows carried (each gains `status: ok` and two class-dimension negatives: a text
extension of the same output, and the same text under another status) + three contained
producer rows over guarded pipes: `status-ok-contained` (0), `status-exit7-contained` (7),
`status-sigpipe-contained` (128+13). The two version rows additionally bind a full-line pattern
and declare `anchor: line`, so a prefix extension is not accepted.

**Target.** `cases=36 executed=36 matched=36 shapes=26/26 anchors=36/36 rows=36/36
mutants=37 killed=37`.

**Kill rule.** A mutant is killed when it exits nonzero or matches fewer than 36/36 rows. The 37
declared mutants are the 28 round-84 mutants whose anchors still occur exactly once after the
status refactor plus nine: `any-nonzero`, `status-class-ignored`, `exact-any-nonzero`,
`signal-any-nonzero`, `signal-as-exit`, `regex-anchor-dropped`, `line-anchor-prefix`,
`negatives-skipped`, `samples-skipped`. The nine round-84 mutants whose rule lines the refactor
moved are not carried; their rules are still exercised by the carried cases, and this is stated
in the round lesson rather than silently dropped.

**No-work control.** The unguarded fixtures are the control: without `set -o pipefail` all three
producers report exit 0 while two of them fail or die, so no `exact`/`signal` row can be met
(`receipts/control-c2-r85-unguarded.txt`). A counter that accepted any nonzero status would meet
the target, so `any-nonzero` is a declared mutant and must die.

**Counting command.**

```sh
python3 -I quality/counters/c2-r85-status-classes.py --repo . --rev REV \
  --controls .ufo/waves/round-85/controls/c2-cases-r85.json \
  --carried .ufo/waves/round-84/controls/c2-runbook-cases-r84.json --scratch-root DIR
```

## Carried-field supersessions (declared, printed by each counter)

- C1: the 61 carried cases are compared parsed-equal; the counter refuses a successor set that
  does not carry them unchanged.
- C2: `status` and `negatives` are added to every carried row; `value` and `anchor` change for
  `version` and `omarchy-version` only; the round-84 fifteen `argv`/`skill_anchor` supersessions
  remain in force. No other carried field may change.

## Sources (round-85 frontier step)

C2 rests on two rows opened this round and pinned under `.ufo/waves/round-85/fetch/`:
**S488** POSIX.1-2024 XCU §2.9.3 *Pipelines* (the pipeline's exit status is the last command's)
and **S489** GNU Bash Reference Manual §3.7.6 *Exit Status* (a command killed by signal N reports
128+N). C1 rests on held **S486** (RFC 8259 §4: duplicate names are undefined for
interoperability) and the lane's own declaration grammar. Registry deltas, access dates, quotes
and the reject verdict are recorded in `corpus/lessons/round-85.md` § Gate.

## Harm watch (every claim)

Standing gate `--selftest` stays N/N; the note index stays N/N with zero missing/dangling/
duplicate; the instrument ledger stays N/N with zero uncovered; the axis table stays
`mismatched=0`; the source census stays exit 0 with its known warnings; navigation and the
carried cases keep their before values. No config tree, compositor state, sibling repo or
operator file is written; no pacman transaction is run.

## Exploratory claim

None.
