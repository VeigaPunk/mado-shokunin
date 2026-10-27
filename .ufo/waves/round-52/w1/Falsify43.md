# Falsify43 — C1 no-work control validity (round 52, mado)

Base inspected: `85d57a818c3707397e21c840b6498b105ba798aa` (lane tree clean; only
`.ufo/waves/round-52/` untracked). Seat-local fixtures only; no tracked lane file touched;
scratch `/fast/scratch/hyaku/mado-r52/Falsify43/` used and removed on exit.

## Attacked clauses

1. **registration.md:7 (C1 predicate, failure-attribution half)** — the new counter "must
   pass on the existing production ledger at the base revision and fail on
   `controls/c1-do-nothing.md` **specifically for self-pointer/context defects**."
2. **registration.md:15 (control description)** — "C1 do-nothing control
   `controls/c1-do-nothing.md` is **the committed ledger shape** with only repeated generic
   self-pointers."
3. **claims-frozen.md:7 (C1, discriminative-power reading)** — the counter "distinguishes
   the production ledger from a no-work control of repeated generic self-pointers".

## Control bytes vs. the committed ledger shape

`.ufo/waves/round-52/controls/c1-do-nothing.md` (4 lines) rows are **4-column and
unbackticked**:

```
| tools/mado-verify.sh | quality/tool-ledger.md (commentary only) | nothing | generic accountability pointer to this ledger itself |
| tools/mado-verify.sh | quality/tool-ledger.md (commentary only) | nothing | generic accountability pointer to this ledger itself |
```

The committed grammar (quality/tool-ledger.md:9-12, enforced by
`quality/check-tool-ledger.py`) is 3-column with backticked cells:
`` | `<repo-relative path>` | <description> | `<pointer path>` or `<pointer path>:<line>` ``.
The control's only path-like token (`quality/tool-ledger.md`) sits in the **description**
cell; the pointer cell is prose with no resolvable token. Registration:15's "committed
ledger shape" is therefore false of the frozen bytes.

## Setup (reproducible)

```
S=/fast/scratch/hyaku/mado-r52/Falsify43
git clone <lane> $S/fixture-X && git -C $S/fixture-X checkout -q --detach 85d57a818c37…
# assert: git -C $S/fixture-X rev-parse --show-toplevel == $S/fixture-X   (passed)
cp <ledger-variant> $S/fixture-X/quality/tool-ledger.md
git -C $S/fixture-X -c user.name=Falsify43 -c user.email=Falsify43@seat commit -qam …
python3 <counter> --repo $S/fixture-X --rev <fixture-rev> --work $S/work-…      # scratch, never /tmp
```

Fixtures (sha256s and revs in `sha256-evidence.txt`):
- `CTL_REV=6362e5ba0daec46f8c3338424f2e129630e61ed0` — frozen control bytes as ledger.
- `BYP_REV=caee345803588b0fc43404413fa4d2065ce233c3` — **bypass**: a mechanically generated
  ledger (`gen_bypass.py`, kept in this seat): 82 unique rows, description = the
  instrument's own leading docstring/comment line (same extraction rule for every file, no
  human reading), pointer cell copied verbatim from the production ledger row (non-self,
  resolvable, basename-bearing at base). Zero work performed.
- `V2_REV=6a46649188c235cdd6cba8b6bfbd13b81f36270d` — control-v2: the shape
  registration:15 *describes* (82 unique committed-grammar rows, all pointers
  `` `quality/tool-ledger.md` ``, one repeated generic description).

Counters run: committed `quality/counters/c1-r51-ledger.py` (+ `quality/check-tool-ledger.py`
via the counter); sibling drafts `w1/C1Simplify/c1-r52-ledger.py` (self_pointer:117-118,
single-backtick POINTER_TOKEN:38, 4-cell rows dropped as dangling before pointer clauses)
and `w1/Falsify41/candidate-c1-r52.py` (pointer=`join(cells[2:])`:105, `tokens`:110,
`selfp`:158). Drafts are uncommitted sibling work; I ran byte-copies (hashes recorded).

## Actual results

| ledger variant | r51 + checker | C1Simplify draft | Falsify41 candidate |
|---|---|---|---|
| production at base | TARGET_MET 82/82 (receipt `receipts/c1-base.txt`) | TARGET_MET 82/82 | TARGET_MET 82/82 |
| frozen control | TARGET_MISSED dup=1 bad_pointer=1 uncovered=81 — **no self clause exists** | TARGET_MISSED dangling=2 (cells=4) uncovered=82 **self_pointer=0 generic_desc=0** | TARGET_MISSED bad_pointer=1 no_context=1 dup=1 uncovered=81 **self_pointer=0** |
| bypass (zero work) | **TARGET_MET** (selftest 50/50, checker ledger ok) | **TARGET_MET, all counts 0** | **TARGET_MET, all counts 0** |
| control-v2 | (r51 has no self/desc clauses — the known r51 weakness) | TARGET_MISSED **self_pointer=82 generic_desc=82** | TARGET_MISSED **self_pointer=82 no_context=82** |

Raw receipts: `receipt-draft-lane-base.txt`, `receipt-draft-control-fixture.txt`,
`receipt-f41-control-fixture.txt`, `receipt-r51-control-fixture.txt`,
`receipt-draft-bypass-fixture.txt`, `receipt-f41-bypass-fixture.txt`,
`receipt-r51-bypass-fixture.txt`, `receipt-draft-controlv2-fixture.txt`,
`receipt-f41-controlv2-fixture.txt`.

## Findings

**F1 — HIGH, attribution failure (reproduced: YES, 3/3 implementations).** The frozen
control cannot fail "specifically for self-pointer/context defects" under any
grammar-faithful counter: r51 has no self-pointer clause; the C1Simplify draft drops the
4-cell rows as `dangling` before the pointer/context clauses ever run (self_pointer=0,
generic_desc=0); the Falsify41 candidate finds no pointer token in the prose pointer cell
(self_pointer=0; its red comes from bad_pointer/dup/uncovered). The eventual red receipt on
this control therefore cannot evidence the self-pointer half of the C1 predicate.

**F2 — HIGH, control bytes contradict registration (reproduced: YES).** registration:15
calls the control "the committed ledger shape"; the frozen bytes are 4-column, unbackticked,
and carry no resolvable pointer token, so no implementation that parses the committed
3-cell grammar can exercise self-pointer or context clauses on it. A counter that *did*
fire self-pointer on these bytes would have to parse the description cell as a pointer —
i.e., be reverse-fitted to one control file, defeating control independence. Either horn is
a defect.

**F3 — HIGH, no-work class not closed (bypass reproduced: YES).** The zero-work bypass
ledger passes TARGET_MET on the committed r51 counter + checker and on **both** new-counter
candidates with every clause count at 0. The control therefore excludes only its own exact
byte pattern, not the no-work class: a ~100-line generator satisfies "unique population,
non-self resolvable evidence targets, instrument-specific context" without any work. This
stays inside the claim's own boundary (bounded accountability, not prose entailment — it
does not allege the descriptions are false); the defect is control *validity*: green on
this counter does not distinguish "work done" from "generator run", and the frozen control
is not a representative member of the class it is frozen to exemplify.

**F4 — constructive, fix demonstrated (reproduced: YES).** control-v2 (registration's
described shape) fires self_pointer=82 + generic/no_context=82 on both candidates. The
predicate *can* be red-tested for self-pointer/context; the frozen control file simply is
not that control. Since "controls cannot be changed after workers score them"
(registration:15), the control bytes must be regenerated in the committed grammar before
scoring, or the red receipt will be structurally mislabeled.

## Limitations / residual risk

- The round-52 counter is uncommitted at investigation time; clause-level runs used the two
  furthest-along sibling drafts (hashes in `sha256-evidence.txt`). The byte-level argument
  in F2 is implementation-independent for any counter parsing the committed grammar.
- The bypass's context clause was exercised against the drafts' two operationalizations
  (bigram-in-source; ≥2 shared tokens + verb gate). A materially different committed
  context check could reject docstring-derived descriptions — F1/F2 are unaffected.
- Production-pass side re-verified only at base; no live reads, package queries, producer
  execution, or host mutation occurred (source-only round honored).

## Dissent / failed controls

None of my controls failed silently: every expected red/green reproduced as predicted. I
note as dissent that both sibling selftests label the frozen control shape "red" without
asserting which clause fires (Falsify41 selftest accepts `any(counts.values())`), which is
how F1 would slip through a red/green receipt unnoticed.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify43.md` — this report
- `.ufo/waves/round-52/w1/Falsify43/gen_bypass.py` — mechanical zero-work ledger generator/verifier
- `.ufo/waves/round-52/w1/Falsify43/bypass-ledger.md` — generated bypass ledger (82/82 clause-clean)
- `.ufo/waves/round-52/w1/Falsify43/control-v2-fixture-ledger.md` — control in registration-described shape
- `.ufo/waves/round-52/w1/Falsify43/control-copy-c1-do-nothing.md` — frozen control byte copy
- `.ufo/waves/round-52/w1/Falsify43/receipt-copy-c1-base.txt` — frozen base receipt copy
- `.ufo/waves/round-52/w1/Falsify43/draft-copy-c1-r52-ledger.py` — C1Simplify draft byte copy
- `.ufo/waves/round-52/w1/Falsify43/sha256-evidence.txt` — evidence hashes + fixture revs
- `.ufo/waves/round-52/w1/Falsify43/receipt-*.txt` — nine counter-run receipts (matrix above)

Report: findings F1–F4; all fixture revs, commands, and hashes above; scratch
`/fast/scratch/hyaku/mado-r52/Falsify43/` removed on exit; no installs; lane tree left with
no tracked modifications.
