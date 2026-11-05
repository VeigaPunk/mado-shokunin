source: S491 — RFC 7493 (I-JSON) §2.3 Object Constraints, https://www.rfc-editor.org/rfc/rfc7493.txt (pin `.ufo/waves/round-86/fetch/S491.bin`, sha256 `a44ccf1451a7bf4f4bbb78b39e10ed0e9a27ff2ee5b639c6458042b5a7197062`, 12,849 B, quote at lines 159–160) · S492 — CPython v3.14.8 `Doc/library/re.rst`, https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/re.rst (pin `.ufo/waves/round-86/fetch/S492.bin`, sha256 `d252cc185dfc1014e1b4a8087b2515b71c76527f0f2f6dfddba9a880537e6a48`, 78,262 B, quote at lines 957–958)
verified-at: 2026-11-05; instrument freeze `237ecf4e69a4986108f719f3beeafe111adaa033`; counters `quality/counters/c1-r86-refusal-records.py` (freeze sha256 `d651c6aa…`, git blob `893d903d`) and `quality/counters/c2-r86-clause-observations.py` (freeze sha256 `1283df22…`)
recheck: see "Recheck" at the end — both counters must be run from bytes that equal the freeze, not from the working tree.

# How a refusal and a runbook row are authenticated

A lane judgement is only as good as the artefact it reads. Round 86 changes what the two scoring
counters accept as evidence. A refusal is accepted as a *record* the tool printed, not as a
substring that happens to occur in its output. A runbook row is accepted only when the clauses that
judge it actually ran, and when its whole output line matches. Both rules were measured against the
rule they replace.

## 1. The refusal record (C1)

`tools/mado-barfoot.py` (sha256 `62626fce852bc5bef263a26ddee78b12c6fc9b2883e41ef55c015becf3a76fb5`,
unchanged at `2b6dd76b`, `237ecf4e` and `b33afc08`) refuses in one shape:

```
MADO_BARFOOT: ERROR (stage=<setup|model>( cause=<token>)? …
```

The round-86 rule (`expected_ok`, `quality/counters/c1-r86-refusal-records.py`) accepts a refusal
case only when all four hold:

| clause | rule | what it refuses |
|---|---|---|
| record shape | `REFUSAL_RE` = `^MADO_BARFOOT: ERROR \(stage=(setup\|model)(?: cause=([a-z][a-z0-9-]*))? ` under `re.M` | text that is not a record at the start of a line |
| occurrence | exactly one record | a second record, or a record plus a look-alike |
| stage and cause | the record's stage equals the case's stage; where the case binds a cause, the record's cause equals it | the right refusal for the wrong reason |
| negative observation | `{token in CAUSE_VOCAB if token in stdout} − {record's cause}` is empty | a flood of other cause tokens printed beside the record |

The vocabulary is the tool's ten refusal causes: `alloc-duplicate-key`, `alloc-not-object`,
`alloc-empty-namespace`, `alloc-non-integer`, `alloc-negative`, `alloc-unknown-namespace`,
`namespace-duplicate-bar`, `namespace-duplicate-surface`, `namespace-duplicate-cross-level`,
`live-duplicate-surface`.

The r86 case set (`.ufo/waves/round-86/controls/c1-cases-r86.json`, 75 cases) has 27 refusal cases
and 48 non-refusal cases. Of the 27, 13 bind a cause and 14 bind only a stage. The 13 bound causes
cover all ten tokens, including `alloc-negative` (bound by `alloc-negative-cause`, a witness added
in r86). The carried round-85 set (72 cases, `.ufo/waves/round-85/controls/c1-cases-r85.json`) binds
nine of the ten: `alloc-negative` was stage-only there (`alloc-negative-refused`).

### Why a substring test is overreach

The held round-85 rule was `(" cause=%s " % cause) in stdout` plus a stage substring. Its control
here is a flooding forgery: the honest tool with `MADO_BARFOOT: FLOOD: <all ten tokens>` printed
before both records (`flooding_sha256=3c5ec8b280e1c9d2e947afbc8a0991fe1174343c2026f26612dd10f71c4f3948`,
built by the counter from the tool source).

| rule | flooding tool | honest tool |
|---|---|---|
| held round-85 (substring) | 75/75 | 75/75 |
| round-86 (record) | 48/75 | 75/75 |

The flood scores 48 under the new rule because the 48 non-refusal cases still pass: a flood cannot
satisfy a refusal case. The honest tool scores 75/75 under the new rule, so the increment is the
rule, not the tool. A substring cannot tell a record from a flood, which is why the held rule
overreached: the same ten tokens satisfy it wherever they sit.

Reproduced at the freeze bytes (the counter file taken with `git show 237ecf4e:quality/counters/c1-r86-refusal-records.py`,
run with `--repo` at the lane and `--rev 237ecf4e`; every per-case and per-mutant line equals
`.ufo/waves/round-86/receipts/c1-r86.txt`):

```
MADO_R86_REFUSALS: cases=75 correct=75 mutants=51 killed=51 base_correct=75/75 carried=72/72
  tool_selftest=152/152 flooding=48/75 held_flooding=75/75 verdict=TARGET_MET
  rev=237ecf4e69a4986108f719f3beeafe111adaa033 tool_sha256=62626fce852bc5bef263a26ddee78b12c6fc9b2883e41ef55c015becf3a76fb5
```

The counter's own selftest reproduces at the freeze: `MADO_R86_REFUSALS_SELFTEST: 127/127`, rc 0.

### What the record rule does not do

- It reads the tool's own `stage` and `cause` words. It authenticates the record's shape and count,
  not the reason: a tool that names a correct cause for a wrong reason still passes.
- The negative observation excludes the record's own cause token from the foreign set **wherever**
  it appears (see finding 1 in §5). It checks other tokens, not repetitions of the record's own token.

## 2. The runbook row (C2)

`quality/counters/c2-r86-clause-observations.py` executes each SKILL.md runbook row. A case is
correct only when the live output meets the row's outcome, every committed churn sample still
matches, every committed negative still fails to match, and **each declared clause was observed**:

| clause | observation | declared population |
|---|---|---|
| sample loop | `OBS["samples"] += 1` per sample | `len(case.samples)` |
| negative loop | `OBS["negatives"] += 1` per negative | `len(case.negatives)` |
| line-anchor branch | `LIVE["anchors"]`, snapshotted after the live call | `1` when `anchor: line` |

A count that differs from its population is a missing judgement: the case is refused, not passed.
The line-anchor population is one, the live call's, because a negative refused by the producer-status
gate never reaches the matcher (`receipts/instrument-repair-r86.md`, repair 2).

Whole-line matching is `fullmatch` semantics. S492 (lines 957–958 of the pin):

> If the whole *string* matches the regular expression *pattern*, return a corresponding Match.

(the pinned text marks up `:class:`~re.Match``; the quote here strips the markup). S492 line 955
defines `re.fullmatch(pattern, string)`; `re.search` is not the whole-string predicate. The round-86
`anchor: line` row binds the unanchored pattern `[0-9]+` to
`set -o pipefail; hyprctl getoption general:border_size -j | jq -r .int`; the committed negative
`0 extra` is accepted by `search` and refused by the whole-line rule.

### Measured at the freeze

Reproduced from the frozen tree (§Recheck, C2):

```
MADO_R86_RUNBOOK: cases=37 executed=37 matched=37 shapes=27/27 anchors=37/37 rows=37/37
  clauses_observed=37/37 superseded=16 mutants=37 killed=37 verdict=TARGET_MET
  rev=237ecf4e69a4986108f719f3beeafe111adaa033 tree=bound
```

The 16 superseded rows are the round-85 rows that carry declared supersession fields. The 37
probe lines and 37 mutant lines equal `receipts/c2-repaired-r86.txt`.

Against the held round-85 instrument, run on the same freeze tree
(`quality/counters/c2-r85-status-classes.py`):

```
MADO_R85_RUNBOOK: cases=36 executed=36 matched=36 shapes=26/26 anchors=36/36 rows=36/36 ... mutants=37 killed=33 verdict=TARGET_MISSED rev=237ecf4e69a4986108f719f3beeafe111adaa033 tree=bound
```

Its four survivors are `regex-anchor-dropped`, `line-anchor-prefix`, `negatives-skipped` and
`samples-skipped`, each at `matched=36/36`. The held rule scores the new witness `border-size-int`
0/1 (`held_rule_new_case=0/1`). A substring search accepts `0 extra`.

Deleting a conjunct cannot lower an already-perfect score, so the held instrument's 36/36 matched
was never evidence of the clauses. The r86 counter is measured by the mutants it kills: 37 of 37.

## 3. Sources and invocations

| source | used for | what it grounds |
|---|---|---|
| S491 RFC 7493 §2.3 | C1 duplicate-identity refusal class | "Objects in I-JSON messages MUST NOT have members with duplicate names." A duplicate-name object is a specification violation, so the lane refuses it rather than choosing one duplicate. RFC 8259 §4 gives only SHOULD. |
| S492 CPython `re` | C2 whole-line rule | `fullmatch` matches the whole string; `search` matches a prefix or infix. An `anchor: line` row must be refused when a line merely starts with the value. |

Invocations (run from the **frozen** tree; see Recheck):

```sh
python3 -I quality/counters/c1-r86-refusal-records.py --repo . --rev 237ecf4e69a4986108f719f3beeafe111adaa033 \
  --base-rev 2b6dd76b65de4dfe701db87db13b7e448b3538ee \
  --controls .ufo/waves/round-86/controls/c1-cases-r86.json \
  --carried .ufo/waves/round-85/controls/c1-cases-r85.json --scratch-root DIR
python3 -I quality/counters/c2-r86-clause-observations.py --repo . --rev 237ecf4e69a4986108f719f3beeafe111adaa033 \
  --controls .ufo/waves/round-86/controls/c2-cases-r86.json \
  --carried .ufo/waves/round-85/controls/c2-cases-r85.json --scratch-root DIR
```

## 4. Recheck and known limits

**Recheck.** Both counters must run from the freeze's bytes. C2 refuses to run otherwise: it
compares `SKILL.md` and `tools/mado-barfoot.py` in the working tree to the `--rev` bytes and exits 2
on mismatch (`tree=bound` fails closed). Running `--rev 237ecf4e` at HEAD `b33afc08` reproduces
this: it printed `ERROR (stage=setup SKILL.md in the working tree is not the measured revision's
bytes)` with rc 2, because `b33afc08` added two registry rows to `SKILL.md` after the freeze. The
frozen verdict was reproduced by extracting the freeze tree with `git archive 237ecf4e` into scratch
and running the counter there (TARGET_MET, rc 0). C1 does not bind the working tree; it extracts
the tool at `--rev`, but it runs its own counter from whatever path it is invoked as. C1 takes
about 335 seconds; a foreground call exceeds a 300-second tool deadline.

**Known limits.**

- The ten-token vocabulary is exhaustive for the tool at the freeze. A new cause token added to
  the tool without a control case would pass the negative observation vacuously.
- The Markdown status and outcome cells of the runbook tables are prose. The counter binds the
  command cell and its live output only (round-85 routed defect R3, still open).
- A numeric status cannot distinguish a normal `exit 141` from SIGPIPE (QUALITY 142).
- The counters bind their inputs by sha256 and do not bind the receipt to the run that printed it.

## 5. Scribe findings (for the L1; not corpus text)

The findings below were produced by running the frozen counters or by reading the committed bytes.
None was fixed.

1. **Negative observation is weaker than the declared rule.** The declaration says no vocabulary
   token may appear "anywhere in stdout outside that record's own cause field". The code is
   `foreign = {t for t in CAUSE_VOCAB if t in stdout} - {cause}` (`c1-r86-refusal-records.py`,
   `expected_ok`), so the record's own token is removed wherever it occurs. Probe, run against the
   freeze copy with `expect = {error: True, rc: 3, stage: setup, cause: alloc-negative}`
   (`python3 -I probe_foreign.py <counter>`, printed `expected_ok held_ok`):
   - honest record only: `True True`
   - record plus `debug: alloc-negative seen again` line: `True True` (declared rule: must be False)
   - record plus `also alloc-duplicate-key` line: `False True`
   The held rule scores all three as passing. The held rule is the control, so only the first
   case is the expected outcome for it; the r86 rule passes the second case when it should refuse.
2. **A frozen instrument has an uncommitted working-tree edit.**
   `git diff -- quality/counters/c1-r86-refusal-records.py` shows one line changed in the module
   docstring (`mutants=53 killed=53` → `mutants=51 killed=51`). The working-tree file has sha256
   prefix `4ff50ac2`; the freeze file has `d651c6aa`. The working-tree file's mtime is
   2026-11-05 00:15:58, after the freeze. The changed text is not executable, but the freeze bytes
   are no longer on disk. The round-86 counters are declared frozen. Other tracked files also show
   uncommitted edits at the time of reading: `.ufo/waves/round-86/receipts/instrument-repair-r86.md`,
   `SCORECARD.md`, `corpus/SOURCES.md`, `corpus/lessons/round-86.md`.
3. **Receipt `rev=` stamps are not the declared freeze.** `receipts/c1-r86.txt` and
   `receipts/c2-repaired-r86.txt` print `rev=f72bba01928efe80cfa1a7907fe3aaa9eba1cfd7` (the
   attempt-1 commit), not `237ecf4e`; the declaration's target line says `rev=<freeze>`. The C1
   counter blob is identical at both (`893d903d`). The per-case and per-mutant lines of my freeze
   reproduction equal the receipts' lines; only the `rev=` stamp differs.
4. **Control receipts are partial.** `receipts/control-c1-r86.txt` and `receipts/control-c2-r86.txt`
   carry `verdict=MUTANTS_SKIPPED` (`--no-mutants`; C2 prints `mutants=0`). The held C2 control with
   33/37 kills (`receipts/control-held-rule-r86.txt`) is stamped `rev=b33afc08`, not the freeze.
5. **Declared base revision differs from the flag.** The declaration's "Base revision" line is
   `a722c604…`; the C1 counter's `--base-rev` (and the tool it scores against) is `2b6dd76b…`. Both
   carry the same tool sha256 `62626fce…`, so the score is not affected, but the two names are not
   reconciled in the declaration.
6. **The landed knowledge entry overgeneralises one sentence.** `corpus/knowledge/refusal-records-clause-observations-r86.md`
   §4 says the counters "bind `SKILL.md`, `tools/mado-barfoot.py` and every listed fixture to the
   measured revision by sha256 (`tree=bound`)". Only C2 does this; C1 has no working-tree binding.
   Its recheck line uses `--rev REV` with no statement that the working tree must equal the freeze,
   which the HEAD run above shows it must.
7. **The 33/37 citation names the wrong revision.** The landed entry attributes the held C2 instrument's
   33/37 to "the round-85 freeze". The only receipt I opened for that figure is stamped `rev=b33afc08`
   (`control-held-rule-r86.txt`). I reproduced 33/37 at `237ecf4e`; the round-85 freeze receipt was not
   opened, so the citation should name `237ecf4e` for the reproduction.
