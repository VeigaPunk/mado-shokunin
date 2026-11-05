source: S491 — RFC 7493 (I-JSON) §2.3 Object Constraints, https://www.rfc-editor.org/rfc/rfc7493.txt (opened this round; pin `.ufo/waves/round-86/fetch/S491.bin`, sha256 `a44ccf1451a7bf4f4bbb78b39e10ed0e9a27ff2ee5b639c6458042b5a7197062`, 12,849 B, quote at line 159) · S492 — CPython v3.14.8 `Doc/library/re.rst`, https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/re.rst (opened this round; pin `.ufo/waves/round-86/fetch/S492.bin`, sha256 `d252cc185dfc1014e1b4a8087b2515b71c76527f0f2f6dfddba9a880537e6a48`, 78,262 B, quote at line 957)
verified-at: 2026-11-04; instrument freeze `237ecf4e69a4986108f719f3beeafe111adaa033`; counters `quality/counters/c1-r86-refusal-records.py` and `quality/counters/c2-r86-clause-observations.py`
recheck: `python3 -I quality/counters/c1-r86-refusal-records.py --repo . --rev REV --base-rev 2b6dd76b65de4dfe701db87db13b7e448b3538ee --controls .ufo/waves/round-86/controls/c1-cases-r86.json --carried .ufo/waves/round-85/controls/c1-cases-r85.json --scratch-root DIR` and `python3 -I quality/counters/c2-r86-clause-observations.py --repo . --rev REV --controls .ufo/waves/round-86/controls/c2-cases-r86.json --carried .ufo/waves/round-85/controls/c2-cases-r85.json --scratch-root DIR`

# A refusal is a record; a matched row is a clause that ran

Two of the lane's judgements were scored by the shape of a string rather than by the artefact that
made the judgement. Round 86 replaces both with observations the instrument can see: a refusal must
be one *record* with its own stage and cause and no stray cause token anywhere else in the output,
and a runbook row must have had its sample loop, negative loop and anchor branch *run*. Both
replacements are measured against the rule they replace, not asserted.

## 1. The refusal record

The lane's bar-footprint tool refuses in one shape (`tools/mado-barfoot.py`, sha256
`62626fce852bc5bef263a26ddee78b12c6fc9b2883e41ef55c015becf3a76fb5` at both the r85 measurement
revision `2b6dd76b` and the r86 freeze `237ecf4e` — the tool did not change):

```
MADO_BARFOOT: ERROR (stage=<setup|model>( cause=<token>)? …
```

The round-86 rule is `expected_ok()` over the 75-case set
(`.ufo/waves/round-86/controls/c1-cases-r86.json`) and binds four things:

| clause | rule (counter line) | what it refuses |
|---|---|---|
| record shape | `REFUSAL_RE` = `^MADO_BARFOOT: ERROR \(stage=(setup\|model)(?: cause=([a-z][a-z0-9-]*))? `, matched with `re.M` | a refusal whose text is not a record at the start of a line |
| occurrence | `len(parse_refusal_records(stdout)) != 1` → refuse (`:336-338`) | a tool that prints two records, or a record plus a look-alike |
| stage and cause | `records[0]` stage must equal the expected stage; where the case binds a cause, the record's cause must equal it (`:342-345`) | a setup refusal answering a model case, or a refusal for another reason |
| negative observation | `{token for token in CAUSE_VOCAB if token in stdout} - {cause or ""}` must be empty (`:347-349`) | an all-cause flood printed among the honest answer |

`CAUSE_VOCAB` (`:41-52`) is the tool's ten refusal causes: `alloc-duplicate-key`, `alloc-not-object`,
`alloc-empty-namespace`, `alloc-non-integer`, `alloc-negative`, `alloc-unknown-namespace`,
`namespace-duplicate-bar`, `namespace-duplicate-surface`, `namespace-duplicate-cross-level`,
`live-duplicate-surface`. The flood forgery is built by the counter from the tool source, so its
bytes are reproducible (`flooding_sha256=3c5ec8b280e1c9d2e947afbc8a0991fe1174343c2026f26612dd10f71c4f3948`).
All ten tokens are bound by at least one case (27 of the 75 cases are refusal cases and their
expected causes cover the vocabulary; round 85 bound nine and left `alloc-negative` stage-only) —
which is what makes the negative observation's vocabulary exhaustive for the tool at the freeze,
and no more than that.

Measured at the freeze (`receipts/c1-r86.txt`):

```
MADO_R86_REFUSALS: cases=75 correct=75 mutants=51 killed=51 base_correct=75/75 carried=72/72
  tool_selftest=152/152 flooding=48/75 held_flooding=75/75 verdict=TARGET_MET
```

`flooding=48/75` is the point of the round: the **same** honest tool, with the ten cause tokens
printed before its records, scores 48/75 under the record rule and **75/75 under the held round-85
rule** (`held_flooding=75/75`), which tested `(" cause=%s " % cause) in stdout`. Forty-eight is the
non-refusal half of the case set: a flood cannot satisfy a refusal case, and it now cannot hide
beside one either. `base_correct=75/75` is the third control — the r85 tool scores full marks under
the *new* rule, so the increment is the rule, not the tool.

## 2. Why a substring is not a record

`(" cause=%s " % cause) in stdout` asks whether some substring exists, not whether the tool said
that. Three consequences, all measured in round 85 (`w1/R85ReviewerC1.md`, QUALITY 141):

- an all-cause flooding tool passes every case, because every expected token is present;
- `cause=alloc-negative` satisfies a case binding `cause=alloc`, because the shorter token is a
  substring of the longer one;
- a record on stderr, or a second contradicting record, is invisible.

The record rule closes those by construction: the regex is anchored at the record start, the
occurrence count is exact, the stage and cause are read out of the record's own fields, and any
token outside that field is a foreign observation. It does **not** authenticate the refusal's
*reason* — `stage` and `cause` are the tool's own words, and a tool that lies about its stage still
passes. That limit is QUALITY 142's neighbourhood and is stated here rather than implied.

### What I-JSON adds, and what it does not

S491 §2.3 (line 159 of the pin) is normative where RFC 8259 §4 is not:

> Objects in I-JSON messages MUST NOT have members with duplicate names.

The sentence makes a duplicate member name a **specification violation** in an I-JSON object, not a
tolerated ambiguity, so the lane's duplicate-name refusal class has a ground for *refusing* rather
than for *picking one of the duplicates*. It says nothing about which duplicate a lenient parser
would keep, and nothing about non-JSON text a tool refuses to parse — those stay the lane's own
declared decisions.

## 3. A row is a clause that ran

`quality/counters/c2-r86-clause-observations.py` executes every row of the SKILL.md runbook sections
`### Executable runbook rows (round 85)` and `(round 86)` — 37 cases, one row each, bound by command
text and by exactly one case. A case is correct only when the live output meets the row's outcome,
every committed churn sample still matches, every committed negative still fails to match, **and
the declared clauses actually ran**:

| clause | observation | declared population | a case that would otherwise pass |
|---|---|---|---|
| sample loop | `OBS["samples"] += 1` per sample evaluated | `len(cases.samples)` | `version` (1 sample) |
| negative loop | `OBS["negatives"] += 1` per negative evaluated | `len(cases.negatives)` | `version` (5 negatives) |
| line-anchor branch | `OBS["anchors"] += 1`, snapshotted after the **live** call as `LIVE["anchors"]` | `1` when the case declares `anchor: line` | `border-size-int` |

The declared anchor population is **one**, not one per sample: a negative refused by the
producer-status gate never reaches the matcher, so "anchors == 1 + samples + negatives" is a
different claim and was measured to fail three anchored cases
(`receipts/c2-anchor-only-r86.txt`, `matched=34/37`). The live call is the judgement; churn and
negative samples are witnesses to it.

Measured at the freeze (`receipts/c2-repaired-r86.txt`):

```
MADO_R86_RUNBOOK: cases=37 executed=37 matched=37 shapes=27/27 anchors=37/37 rows=37/37
  clauses_observed=37/37 mutants=37 killed=37 verdict=TARGET_MET
```

against the held rule's `held_rule_new_case=0/1` on the same witness and the round-85 instrument's
33/37 kills at the round-85 freeze (four survivors: `negatives-skipped`, `samples-skipped`,
`regex-anchor-dropped`, `line-anchor-prefix`).

### The whole line, not a prefix

S492 (line 957 of the pin) is the semantics the `anchor: line` witnesses need:

> If the whole *string* matches the regular expression *pattern*, return a corresponding Match.

`re.fullmatch` is that predicate; `re.search` is not. The counter implements it as `search` plus
`match.group(0) == line` (`line_anchored`), which is the same predicate for these patterns — the
match's own span must be the whole line. The round-86 witness row
`set -o pipefail; hyprctl getoption general:border_size -j | jq -r .int` binds an **unanchored**
pattern `[0-9]+` to a whole line, so a plausible next-day output that carries the value with
trailing text (`0 extra`) is accepted by `search` and refused by the whole-line rule; `-1` and
`0 extra` are the committed negatives. The row is read-only and its value (`0` on this host) is
host state, reported with churn samples, never frozen.

## 4. What this entry does not certify

- **The negative observation exempts by token identity, not by position** (`w1/R86CriticClaims.md`
  (a)): the record's own cause token is allowed *anywhere* in stdout, so a tool that echoes its own
  cause on a second line and then prints the honest record scores 75/75, although the declared
  binding says no vocabulary token may appear outside the record's own cause field.
- **Four forgery classes score 75/75 under the record rule** (`w1/R86ReviewerC1.md`
  S1-a/S1-b/S2-a/S2-b): all ten tokens printed on **stderr** (the counter captures stderr and never
  inspects it); a duplicate record shifted by one leading space (`^`-anchored `re.M`, so "exactly
  once" holds only at column 0); all ten tokens printed on the **result** path, where no vocabulary
  check exists; and a homoglyph flood (`а` U+0430 for `a`) against a byte-substring vocabulary.
  Three of the four also score 75/75 under the held rule, so the increment does not cover them.
- The ten-token cause vocabulary is exhaustive for the tool **at the freeze** — `R86ReviewerC1`
  verified the raise sites by AST (`vocab − raised = ∅`) — but a new cause token added to the tool
  without editing the control set would pass the negative observation vacuously.
- The record rule reads the tool's own stage/cause words; it does not verify the refusal happened
  for the reason claimed, and a cause-free case accepts a spurious cause (the record's own token is
  self-exempted from the foreign check).
- The clause observation **counts iterations, not evaluations** (`w1/R86ReviewerC2.md` F1/F2): a
  count-preserving stub passes every case-level conjunct and is caught only by the declared mutant
  population, not by the observation itself.
- A numeric status still cannot distinguish a normal `exit 141` from SIGPIPE (QUALITY 142, S489).
- The Markdown status and outcome cells of the runbook tables are prose; the counter binds the
  command cell and its live output only (r85 routed defect R3, still open).
- The counters bind `SKILL.md`, `tools/mado-barfoot.py` and every listed fixture to the measured
  revision by sha256 (`tree=bound`) — which also means a later edit to any of those files makes the
  frozen counter refuse to run at the older revision; they do not bind their own receipt to the run
  that printed it.
