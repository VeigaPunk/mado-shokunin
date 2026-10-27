# Attack04 — W2 attack #04: C1 red control defect-isolation

Seat: `Attack04` (leaf, attack wave 2). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Round base: `85d57a818c3707397e21c840b6498b105ba798aa`. This is an attack on the frozen
C1 control's validity, not a vote and not a claim-landing judgment (L1 owns that seat).

## Attacked clauses

1. `registration.md` "Frozen predicates" C1: the new counter "must pass on the existing
   production ledger at the base revision and fail on `controls/c1-do-nothing.md`
   **specifically for self-pointer/context defects**."
2. `claims-frozen.md` C1: the control is "a no-work control of repeated generic
   self-pointers"; target includes "instrument-specific context checks. Demonstrate
   production pass and control fail at the frozen revision."
3. W1 evidence under test: `w1/C1ControlAttack.md`'s confound attack (schema/duplication
   confounds), `w1/C1Fixture.md`'s receipts (draft counter red receipt names both
   signals; old counter fails the control for the wrong reason), `w1/C1CounterDesign.md`'s
   attribution claims, and the orchestrator's W1 signal "C1 control does not isolate
   required defects if schema shape causes failure."

Subject under test: the W1 draft counter
`w1/C1CounterDesign/c1-r52-ledger.py` (sha256 `0fe862f1…`, 847 lines), evaluated with
`--repo <lane> --rev 85d57a8…`; and the committed prior counter
`quality/counters/c1-r51-ledger.py` at the base revision. At the frozen base the new
counter is absent from the tree (the claim's own premise; an untracked
`quality/counters/c1-r52-ledger.py` exists in the working tree from concurrent
integration work by other seats — out of scope here; claims judge the frozen revision).

## Verdict up front

- **Falsified (control-isolation reading):** the frozen control's red outcome is
  reachable by a counter with *zero* self-pointer/context detection — the committed r51
  counter fails it, and the lane's own committed gate fails it on schema shape alone.
  The control carries at least four independent defect classes; failure on it is not
  attributable specifically to self-pointer/context defects.
- **Verified (counter-side attribution):** the W1 draft counter names both required
  signals on the control and attributes each defect class exactly under isolation
  (single-defect controls fire exactly one signal; both-defect full-population control
  fires both with all structural fields at zero). The specificity the registration asks
  for is demonstrable only with a different (population-complete) control than the
  frozen one — exactly the shape `w1/C1ControlAttack.md` prescribed as the smallest
  safe correction and that I built and measured here as `ctrl-both-isolated`.

## Item 1 — frozen control bytes vs production schema (source evidence)

- `.ufo/waves/round-52/controls/c1-do-nothing.md` (read in full): header
  `| Tool | Reads | Writes | Owner and adjacent lanes |` — four columns; two
  byte-identical rows for `tools/mado-verify.sh`; Reads cell
  `quality/tool-ledger.md (commentary only)`; Writes cell `nothing`; final cell
  "generic accountability pointer to this ledger itself".
- `quality/tool-ledger.md` "Row grammar" (frozen base): three cells
  `| <repo-relative path> | <one-line description> | <pointer> |`; cell 3 must name a
  tracked repository file containing the instrument basename.
- Confirmed confound classes present in the control: (a) schema shape — 4 columns vs the
  3-column grammar; (b) duplication — the same row twice; (c) coverage — 2 rows vs the
  82-file population (independently re-derived: `git ls-tree -r --name-only 85d57a8…`
  filtered to `tools/` + `quality/*.py` + `quality/counters/*.py` = 82); (d) the two
  intended defects (self-pointer wording, generic context).
- Verdict reproduced: the control is not an isolating control. Confidence: high (bytes).

## Item 2 — draft r52 counter vs frozen control (reproduced red receipt)

Command (run from my scratch; lane read-only):

```
python3 -I .ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py \
  --repo <lane> --rev 85d57a818c3707397e21c840b6498b105ba798aa \
  --work /fast/scratch/hyaku/mado-r52/Attack04/work-red \
  --ledger <lane>/.ufo/waves/round-52/controls/c1-do-nothing.md
```

Observed (exit 1):

```
C1_R52: population=82 ledger_rows=2 uncovered=81 dup=1 dangling=0 bad_pointer=0 \
self_pointer=1 generic_desc=1 verdict=TARGET_MISSED rev=85d57a818c3707397e21c840b6498b105ba798aa
```

Reproduces the W1 receipt (`C1CounterDesign.md`, `C1Fixture.md`) byte-for-byte in the
summary fields. The red receipt carries **four** non-zero failure signals; only
`self_pointer` and `generic_desc` are the required defect classes. `uncovered=81` and
`dup=1` are structural and each alone forces `TARGET_MISSED` under this counter's
exit rule (any non-zero field misses). Outcome: red is real, but not specific — the
receipt cannot distinguish "counter detects self-pointer/context" from "counter counts
rows". Verdict reproduced. Confidence: high (direct run).

## Item 3 — FALSIFIER: the r51 counter (no self-pointer/context logic) fails the control

The frozen claim's own "Before" text states the old counter "accepts any referenced file
containing the instrument basename … generic descriptions and ledger-wide self-pointers
pass" — i.e. it implements none of the required new detection. Concrete test: committed
the frozen control byte-for-byte as `quality/tool-ledger.md` in a scratch
`git clone --shared --no-checkout` fixture (fixture commit
`452a09cc694eb44d9e2f92ed1110bed31af13c56`, parent = frozen base; every plumbing write
went to the fixture's own object store after asserting
`git rev-parse --show-toplevel` = the fixture dir) and ran the committed old counter:

```
python3 -I quality/counters/c1-r51-ledger.py --repo <fixture> --rev 452a09cc… \
  --work /fast/scratch/hyaku/mado-r52/Attack04/work-old-red
```

Observed (exit 1):

```
C1_R51: population=82 ledger_rows=2 uncovered=81 dangling=0 bad_pointer=1 empty_desc=0 \
selftest=ok dup=1 checker=failed verdict=TARGET_MISSED rev=452a09cc…
```

It names neither `self_pointer` nor `generic_desc` (it has no such fields). The lane's
own committed gate `quality/check-tool-ledger.py`, invoked by the old counter's checker
clause, parsed the 4-column control as `ledger_rows=0 dangling=2` — **the control fails
on schema shape alone under the committed toolchain**, without any row ever being
scored for content. Control run on the unmodified base fixture reproduces the frozen
receipt `receipts/c1-base.txt` final line byte-for-byte (`population=82 ledger_rows=82
uncovered=0 … verdict=TARGET_MET rev=85d57a8…`, exit 0).

Outcome: a counter that cannot detect either required defect fails the frozen control.
Therefore the control's red result is not attributable specifically to self-pointer/
context defects; the registration's "specifically" clause is not established by this
control alone. **Falsified as a property of the control.** Confidence: high (direct run
of the committed prior counter).

## Item 4 — verified: draft counter attributes each defect exactly under isolation

Scratch controls built from `git show 85d57a8…:quality/tool-ledger.md` (82 real table
rows; the fenced grammar example stays inside its fence and is never a row), run via
the counter's `--ledger` entry point at the frozen base:

| control | planted defect | observed summary | exit |
|---|---|---|---|
| `ctrl-selfptr-only.md` | all 82 pointers → `` `quality/tool-ledger.md` `` | `uncovered=0 dup=0 bad_pointer=0 self_pointer=82 generic_desc=0 TARGET_MISSED` | 1 |
| `ctrl-generic-only.md` | all 82 descriptions → `Generic accountability note.` | `uncovered=0 dup=0 bad_pointer=0 self_pointer=0 generic_desc=82 TARGET_MISSED` | 1 |
| `ctrl-both-isolated.md` | both, full 82-row population | `uncovered=0 dup=0 bad_pointer=0 self_pointer=82 generic_desc=82 TARGET_MISSED` | 1 |
| `ctrl-reshaped-unique.md` | frozen control re-shaped to 3-column grammar, two **unique** rows, both intended defects kept | `uncovered=80 dup=0 self_pointer=2 generic_desc=2 TARGET_MISSED` | 1 |

Verified: (a) the two required signals are separated, not conflated — each single-defect
control fires exactly one, with every structural field at zero; (b) the
population-complete both-defect control (`ctrl-both-isolated`) is the isolating control
the frozen control is not — red with *only* the two required signals non-zero; (c) even
after removing the frozen control's duplication and schema-shape confounds, the
coverage confound (`uncovered=80`) still forces `TARGET_MISSED` on its own. The draft
counter's green at base verified directly: `population=82 ledger_rows=82 …
self_pointer=0 generic_desc=0 verdict=TARGET_MET`, exit 0.

## Item 5 — gate cross-check cannot corroborate the red specificity

Measured in item 3: the committed gate reports no `self_pointer`/`generic_desc` fields
and, on the control, fails as `ledger_rows=0 dangling=2` (schema-shape parsing). Any
integration that kept the r51-style gate cross-check would record the control failure
as a parsing failure, not as detection of the required defects. Consistent with
`C1Fixture.md`'s flag to the L1. Verdict reproduced. Confidence: high.

## Limitations

- The r52 counter under test is the W1 draft (`0fe862f1…`), not a landed instrument;
  the frozen base tree has no r52 counter (claim's own premise). The untracked
  working-tree `quality/counters/c1-r52-ledger.py` from concurrent integration was not
  evaluated and not touched.
- The old counter has no `--ledger` entry point; item 3 used a scratch fixture commit
  (standard practice, mirrors `C1Fixture.md`). Lane HEAD stayed at
  `85d57a8…` and `git status --porcelain` is identical before and after all my runs;
  every write was under `/fast/scratch/hyaku/mado-r52/Attack04/`.
- "Specifically" has two readings. I falsify the control-isolation reading (a red on
  this control does not demonstrate the required detection) and verify the joint
  reading (draft counter + isolated controls do demonstrate it). Whether the frozen
  claim as worded is met by counter+receipts jointly is the L1's seat, not mine.
- Scope: red control defect-isolation only. The F3 counterfeit semantic-context bypass
  (`control-F3-forged` accepted on 72/82 rows) and the lexical-binding ceiling are
  assigned to other W2 seats; I note them as adjacent but did not re-attack them here.
- No packages installed; no host reads beyond the source checkout and my own scratch;
  no delegation; no git/jj mutation in any real repository (fixture plumbing commits
  live only in the scratch clone's object store).

## Commands (all reproduced above; lane paths relative to fleet root)

- `git -C mado-shokunin rev-parse HEAD` → `85d57a818c3707397e21c840b6498b105ba798aa`.
- Draft counter red: `python3 -I mado-shokunin/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py --repo mado-shokunin --rev 85d57a818c3707397e21c840b6498b105ba798aa --work <scratch>/work-red --ledger mado-shokunin/.ufo/waves/round-52/controls/c1-do-nothing.md` → `self_pointer=1 generic_desc=1 dup=1 uncovered=81 TARGET_MISSED`, exit 1.
- Old counter red: fixture commit `452a09cc694eb44d9e2f92ed1110bed31af13c56` (control as `quality/tool-ledger.md`, parent = base); `python3 -I mado-shokunin/quality/counters/c1-r51-ledger.py --repo <fixture> --rev 452a09cc… --work <scratch>/work-old-red` → `uncovered=81 dup=1 bad_pointer=1 checker=failed TARGET_MISSED`, exit 1; gate line `ledger_rows=0 dangling=2`.
- Old counter green: same counter, `--rev 85d57a8…` on unmodified fixture → final line byte-identical to `mado-shokunin/.ufo/waves/round-52/receipts/c1-base.txt`, exit 0.
- Isolated controls via draft counter `--ledger`: `ctrl-selfptr-only` → `self_pointer=82 generic_desc=0`; `ctrl-generic-only` → `self_pointer=0 generic_desc=82`; `ctrl-both-isolated` → `self_pointer=82 generic_desc=82` (all other fields 0); `ctrl-reshaped-unique` → `uncovered=80 self_pointer=2 generic_desc=2`; all exit 1.
- Draft counter green at base → `TARGET_MET`, exit 0.

Scratch `/fast/scratch/hyaku/mado-r52/Attack04/` removed after this report was written.

Report: `.ufo/waves/round-52/w2/Attack04.md`
