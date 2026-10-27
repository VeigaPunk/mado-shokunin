# C1Simplify — simplest legitimate C1 check and an isolating failing control

Axes: **operability** (C1). No coverage claim and no axis moved. This report is a
simplifier review, not a vote; it attacks item **C1 (frozen)** — specifically its control
and its counter surface — and recommends a smaller check.

Scope note: at review start **no C1 r52 counter existed**. Measured evidence:
`ls .ufo/waves/round-52/w1/C1CounterDesign` → `No such file or directory`;
`git ls-tree -r --name-only 85d57a8 | grep -c c1-r52` → `0`. The only C1 artifacts in
`w1/` were `C1ControlAttack.md`, `C1Mutation.md`, `C1Fixture/harness/`. `C1CounterDesign`'s
draft landed during this review and is reviewed and executed in §9. So this report covers
(a) the ancestor counter the draft derives from, (b) the harness that scores it, (c) a
working minimum-size reference with red/green controls, and (d) the landed draft, all
measured at the frozen revision.

## 1. The frozen control exhibits the predicates only under a wider row reading (measured)

Frozen registration requires the new counter to fail `controls/c1-do-nothing.md`
**"specifically for self-pointer/context defects."** Under the ledger's own pointer-region
reading that is not reachable with the committed bytes; it is reachable only with a wider
all-cell reading, at a measured cost (§9). Both readings are measured here.

Control bytes (`cat -A .ufo/waves/round-52/controls/c1-do-nothing.md`): a 4-column
header, two byte-identical rows, no backticked pointer token anywhere:

```
| Tool | Reads | Writes | Owner and adjacent lanes |
| tools/mado-verify.sh | quality/tool-ledger.md (commentary only) | nothing | generic accountability pointer to this ledger itself |
| tools/mado-verify.sh | quality/tool-ledger.md (commentary only) | nothing | generic accountability pointer to this ledger itself |
```

The production schema is 3 cells (`quality/tool-ledger.md`, "Row grammar"); measured at
base: `cell-count histogram (data rows): {3: 82}`. Run of the minimum reference at
`85d57a8` against the frozen control:

```
LEDGER52: population=82 ledger_rows=2 uncovered=82 dup=0 dangling=2 bad_pointer=0 self_pointer=0 generic_desc=0 verdict=TARGET_MISSED rev=85d57a818c3707397e21c840b6498b105ba798aa
```

Under the ledger's pointer-region reading, a red receipt on this control demonstrates only
*shape/population* failure: `self_pointer` and `generic_desc` stay 0, so neither new
clause is exercised. The signals do appear once the counter scores the 4-cell row and
derives self-references from every cell — not from the phrase "this ledger itself", but
from the bare token `quality/tool-ledger.md` in the Reads cell (§9, measured against the
peer draft). Independently reached at source level by `C1ControlAttack.md` (schema/duplicate
confound, "smallest safe correction"); §9 supersedes its recommendation to change the
control.

**Operational consequence:** `C1Fixture/harness/` asserts red = `self` signal AND
`context` signal (README "What the harness measures"; `findings.append("no self-pointer
defect reported…")`, `findings.append("no instrument-specific-context defect reported…")`).
A counter that discards the 4-cell row as malformed can never satisfy that red case; a
counter that scores it and scans cells outside the pointer region can. `C1CounterDesign`'s
peer draft does the latter and its harness receipt is `verdict=PASS` with red
`self_pointer=1 generic_desc=1` (verified in `receipts.txt`, "PEER DRAFT"). So the
registration is satisfiable without a new control, at the price analysed in §9; the
population-complete controls in §4 remain the only set that names one defect class at a
time.

## 2. Simplest legitimate check (reference implementation, measured)

`.ufo/waves/round-52/w1/C1Simplify/c1-r52-ledger.py` — **194 lines including docstring**,
no clone, no subprocess, no sandbox, no writes, no `--work` requirement (it accepts the
flag and ignores it, only because the harness passes one). Runtime **150 ms** at base.
Its only inputs are `git ls-tree -r --name-only <rev>` and `git show <rev>:<path>`.

```
LEDGER52: population=<P> ledger_rows=<R> uncovered=<n> dup=<n> dangling=<n>
          bad_pointer=<n> self_pointer=<n> generic_desc=<n> verdict=<MET|MISSED> rev=<sha>
```

Rules, all evidence-anchored and none semantic:

- population = files at `--rev` under `tools/` + `quality/*.py` + `quality/counters/*.py`
  (`__pycache__`, `*.pyc`, `*.pyo` excluded) — measured 82 at base.
- rows = pipe rows outside fenced blocks, **exactly 3 cells**; the ledger's own grammar
  example is fenced and must be skipped (a naive parser counts 83 rows, measured).
- `dup` = repeated path; `uncovered` = population path without a row;
  `dangling` = non-population path or non-3-cell row.
- pointer = **the whole cell must be one backticked repo path** (optional `:N`/`:N-M`
  stripped). Production conforms 82/82 (measured: `pointer cells not single backticked
  token: 0`), so the strict grammar costs nothing and removes r51's whitespace-prose
  fallback. Then: `self_pointer` if the target is the row's own path **or** the canonical
  ledger path (independent of how the ledger was read — see §5); `bad_pointer` if the
  target does not exist at rev or its bytes lack the row's basename. Only 12 unique
  targets exist at base, so the byte reads are one cache away from free.
- `generic_desc` = description empty/placeholder, or shared verbatim with an earlier row,
  or sharing no adjacent word pair with the instrument's own committed bytes.
  A word-count floor was **tested and dropped** as redundant: identical verdicts on green,
  the frozen control and B/C/D/E with the floor on and off; the reference carries no such
  constant.

Every rule above is load-bearing for the frozen wording; the context clause is the only
one that is defeatable by construction (§6).

## 3. YAGNI deltas against the ancestor counter

`quality/counters/c1-r51-ledger.py` is 445 lines, 2154 ms at base (earlier run 1991 ms;
receipt in
`C1Simplify/receipts.txt`, "ANCESTOR"). The reference is 194 lines, 150 ms. What to drop,
with reasons:

| ancestor component | move | basis |
|---|---|---|
| `make_clone`, `resolve_work`, `REFUSED_ROOTS`, clone teardown | drop | `git show`/`ls-tree` read committed bytes without a work tree; nothing is written, so no scratch lifecycle exists |
| `run_python`, `sandbox_env`, `RUN_TIMEOUT` | drop | no child process runs |
| `checker_selftest`, `checker_ledger`, `RATIO_PASSED`, `SELFTEST_OK`, `SELFTEST_FAIL`, `SELFTEST_FALLBACK_RC`, `normalise_checker` | drop | re-running `quality/check-tool-ledger.py` and cross-comparing its six numbers is not in the frozen C1 predicate; it doubles the failure surface and adds a dependency on a tracked file the claim never names. Independence of measurement is preserved by the counter reading revision bytes itself |
| `pointer_tokens` whitespace fallback | drop | production pointers are 82/82 single backticked paths; the fallback is precisely the generic-prose acceptance C1 exists to remove |
| word-count floor (my own first draft) | drop | not load-bearing: identical outcomes on green + B/C/D/E + frozen control with the floor on and off; removed from the reference |

What must be **kept** although it looks optional: fenced-block skipping (otherwise +1 row
and a dangling finding), and the `:line` suffix strip (all production pointers carry one).

## 4. The failing control the predicate actually needs (measured)

Four isolating controls derived deterministically from the production ledger by
`C1Simplify/gen-controls.py` (same rows, same order, so population/row uniqueness cannot
be the cause of failure). Verdicts from the reference at `85d57a8`:

| control | changed | result | isolates |
|---|---|---|---|
| committed `c1-do-nothing.md` | 2 rows, 4 cells, prose pointer | `uncovered=82 dangling=2 self_pointer=0 generic_desc=0` MISSED | nothing new |
| B `control-B-row-selfpointer.md` | every pointer → own path; every description → one repeated generic sentence | `self_pointer=82 generic_desc=82` MISSED | both clauses |
| C `control-C-ledger-selfpointer.md` | every pointer → `quality/tool-ledger.md` | `self_pointer=82 generic_desc=0` MISSED | ledger-self only |
| D `control-D-generic-desc.md` | descriptions → repeated generic sentence; pointers untouched | `self_pointer=0 generic_desc=82` MISSED | context only |
| E `control-E-one-selfpointer.md` | one row (`tools/mado-anims.py`) → self-pointer | `self_pointer=1 generic_desc=0` MISSED | minimal single defect |

Recommendation: B, C, D, E are the **per-class isolation set** — the only controls that
name one defect class at a time. They are not required for the red case if the counter
adopts the all-cell reading (§9), and no frozen control needs replacing: the committed
control fires both signals under that reading (measured, §9). What B still buys is
diagnosis: without it, a red receipt on the committed control cannot show *which* clause
fired. Keep it as evidence, not as the scored control.

**Harness cost, measured, and the fixture that is not needed.** The harness clones the
455 MB lane tree twice (`du -sm <lane> --exclude=.git` → 455; `git ls-files | wc -l` → 24582)
and sha256-digests every tracked file before and after. Measured on this host while sibling
seats were running: `--cases green` alone did not finish in 110 s (`timeout 110` → exit
124), and the two-case run did not finish in 300 s. The counter it measures takes 161 ms.
Because a counter may read the control through `--ledger` (production stays `git show
rev:quality/tool-ledger.md`), the red case needs **no fixture commit and no clone at all**:
green is the lane repo at `--rev` (read-only), red is one process run with `--ledger
<control>`. The harness's fixture-commit design is therefore avoidable weight, and its
`git add -A`/commit path is the only code in the round that mutates a repository.

No executed harness verdict was obtained (timeouts above), so the red-expectation finding
is a code-reading result (`c1-fixture-harness.py`, `evaluate()` findings), not an executed one.

Also measured, three single-defect mutations of the production ledger (discrimination,
same generator): duplicated row → `ledger_rows=83 dup=1`; one description `—` →
`generic_desc=1`; one pointer `corpus/nonexistent.md` → `bad_pointer=1`.

## 5. Maintainability hazards found by building the minimum

1. **False green on the ledger-self pointer.** First reference draft compared the pointer
   with the *effective* ledger path only, which is `None` when `--ledger` names an
   external control: control C passed `verdict=TARGET_MET` with 82 self-pointers. Fix:
   always exclude the canonical `quality/tool-ledger.md`, plus the `--ledger` path when it
   is repo-relative. This is a live trap for any counter that reads controls from the
   working tree while resolving pointers at `--rev`; control C exists to catch it.
2. **Control bytes are not at `--rev`.** The ledger must come from `git show rev:…` for
   production and from the filesystem for a control; a counter that only accepts
   revision bytes cannot run the red case at all, and r51 could not.
3. **Fenced grammar row.** `quality/tool-ledger.md` contains a pipe-row example inside a
   fenced block; measured 83 vs 82 rows. Skipping fences is not optional.
4. **Harness interface coupling.** `C1Fixture` passes `--repo --rev --work` and rejects
   exit 2 as "counter rejected the frozen argument set". A no-write counter must therefore
   accept an unused `--work`; document it as compatibility, not as a scratch parameter.
5. Constant `LEDGER_REL` couples the counter to one ledger filename. That is the frozen
   artifact's own path, not a second authority; keep it a single constant and do not
   reintroduce a `--ledger-rel` knob.

## 6. Honest bound — a control that defeats the context clause (failed control)

`control-F3-forged.md`: population-complete, unique descriptions, real non-self pointers,
but every description is generic boilerplate followed by an index and a four-word phrase
copied from the instrument's own docstring ("Generic accountability note 0 mado action
plan py."). Result: **`generic_desc=0 verdict=TARGET_MET`** — the forged ledger passes.

The minimal form of the same forgery needs no 82-row construction: control H changes one
production row's description to `PRED-C1-r47 does things.` and both counters accept it, because
`pred c1` is a genuine two-word phrase in that instrument's own bytes (measured in
`receipts.txt`; the peer draft reports the same case). So a prediction id plus filler passes
the context clause on every counter in this round.

Therefore the lexical context clause measures *description-to-source lexical binding*,
not instrument-specific functional context. C1's own text already limits the claim to
"bounded accountability checks, not prose entailment", so this is not a predicate change;
it is a limit the C1 receipt must state in those words. If a scored control is expected to
reject F3-style forgeries, the lexical check cannot do it and the claim would be
overstated — see §7.

## 7. Dissent

- Against the strict pointer-region reading I first proposed (§1/§9): it makes the frozen
  control unreachable and would force a replacement control. The peer draft's wider
  reading satisfies the frozen registration with the committed control; I withdraw the
  demand to add or replace a control, and keep B/C/D/E only as per-class diagnostics.
- Against the wider reading's first cost (§9): naming the ledger in any cell disqualified a
  row (control G), including an honest description of an instrument whose job is to read the
  ledger. The peer seat narrowed the scan (fires only on rows with no accountable pointer):
  G is green, the frozen control still fires both signals, B/C/D/E unchanged. Residual:
  `self_pointer` now means two things, so the `note` line must stay in receipts.
- Against any C1 receipt that reports instrument-specific context as demonstrated: §6 and
  §9 show constructed no-work ledgers that pass or nearly pass. Report `generic_desc` as a
  lexical binding check; do not claim context detection beyond it.
- No position taken on C2; none taken on claim scope, which I did not touch.

## 8. Commands, environment, limitations

- Base and state: `git -C <lane> rev-parse HEAD` → `85d57a818c3707397e21c840b6498b105ba798aa`;
  `git ls-tree -r --name-only 85d57a8` → 24582 paths; population 82; ledger rows 82.
- Full command/output receipts with exit codes: `.ufo/waves/round-52/w1/C1Simplify/receipts.txt`
  (green, frozen red, B, C, D, E, F3, G, H, three mutations, ancestor r51 at 2154 ms, and the
  read-only runs of both peer-draft revisions — `c0291662` and final `382a0606` — including
  the G false positive and its fix)
- Reproduction: `python3 gen-controls.py` in the seat dir rebuilds all controls from
  `85d57a8` with `git show` only; the counter then runs as
  `python3 -I c1-r52-ledger.py --repo <lane> --rev 85d57a8 --ledger <control>`.
- Read-only throughout: no source-tree writes (`git status --porcelain` in the lane shows
  only `?? .ufo/waves/round-52/`, the round's own untracked wave dir), no host/probe/live
  reads, no package queries or installs, no git/jj mutations. Scratch:
  `/fast/scratch/hyaku/mado-r52/C1Simplify/` (disk guard `df -h /fast`: 600G available, 26% used).
- Limitations: the review began before any counter existed, so §2–§4 are a measured
  reference; §9 was added after `C1CounterDesign`'s draft landed and is a review of that
  draft as read and executed here. §6's forgery is a constructed control, not evidence
  about any shipped counter. My own harness invocations timed out (110 s green-only, 300 s
  two-case) under concurrent sibling load, so the harness verdict cited in §9 is the peer
  seat's receipt (`.ufo/waves/round-52/w1/C1CounterDesign/receipts/harness-summary.json`,
  `verdict: PASS`, `lane_unchanged`), not my execution. No external source candidate was
  used, so no URL/access date/quote applies.

## 9. The peer draft (`C1CounterDesign`) — review and integration

`C1CounterDesign/c1-r52-ledger.py` landed after this seat's reference. Executed here,
read-only, at `85d57a8`, twice: draft `c0291662…` (680 lines) and the final
`382a0606408d714089b1f8906972eba551ea560e332d5c30755fee894ff32d6e` (787 lines). Final
numbers:

| input | peer draft | my reference |
|---|---|---|
| production ledger | `TARGET_MET`, all fields 0, exit 0 | identical |
| committed frozen control | `uncovered=81 dup=1 self_pointer=1 generic_desc=1` MISSED | `uncovered=82 dangling=2 self_pointer=0 generic_desc=0` MISSED |
| B / C / D / E | 82/82, 82/0, 0/82, 1/0 — all MISSED | identical |
| F3 forged | `generic_desc=10` MISSED (7 on the first draft) | `generic_desc=0` TARGET_MET |
| G legitimate ledger reader | `TARGET_MET` (first draft: `self_pointer=1` MISSED) | `TARGET_MET` |

Two mechanical differences explain the frozen-control row. The draft (a) scores a row
wider than three cells instead of calling it `dangling`, and (b) derives the self signal
from path-shaped tokens in **every** cell, not only the pointer region. On the control
that is not prose-guessing: the Reads cell literally contains the bare token
`quality/tool-ledger.md`, and the fallback tokenizer treats bare path-shaped words as
paths. So the self signal is real under that reading — my §1 statement that firing the
signal requires reinterpretation was too strong for the draft's model, and this section
replaces it.

The cost of (b) was measured with control G: a production-shaped ledger whose only change
is a legitimate description that names the ledger it reads:

```
| quality/check-tool-ledger.py | Reads quality/tool-ledger.md and reports each instrument's accountability row. | .ufo/waves/round-51/registration.md |
```

First draft → `self_pointer=1` MISSED; reference → `TARGET_MET`. The peer seat then adopted
narrowing rather than documentation: the all-cell scan still runs, but fires only on a row
with **no accountable pointer**, and a ledger mention in prose on an accounted row is
printed as `note path=… names-the-ledger-in-prose` instead of scored. Re-measured on the
final draft: G → `TARGET_MET`; frozen control unchanged at `self_pointer=1
generic_desc=1`; B/C/D/E unchanged. The false positive I measured is closed.

The residual cost is semantic, not behavioural: `self_pointer` now means two things — a
pointer-region target that is the ledger/row, or an any-cell ledger mention on a row with
no accountable pointer. Keep the `note` line in the receipt so a reader can tell which
fired; without it the field is ambiguous. This resolution is better than my original
"document the fail-closed rule" because it removes a real false failure at the cost of one
conditional whose dependence on the pointer check is stated in the docstring.

Clauses the draft adds that I did not have, both green-safe (production: 0 of 82 pointer
cells target a population instrument; 12 distinct document targets):

- pointer must land on a document, not a sibling instrument — closes one-row-points-at-peer.
- the matched description phrase must not consist only of the instrument's path words —
  rejects 10 of F3's 82 forged rows (`generic_desc=10`, measured above; 7 before the extra
  filters) but not the remaining 72, so the lexical ceiling in §6 stands.

**Integration recommendation.** Integrate the peer draft, not my reference: it satisfies
the frozen red case without replacing a frozen control, and its extra clauses are
green-safe. Simplify it in three places, in this order of value:

1. **Selftest size — open disagreement, integrator's call.** The registration requires a
   selftest with explicit red/green receipts, so a selftest is not optional. The draft's
   `Suite`/`fixture_repo`/`selftest`/`resolve_work` block (~230 of the 787 lines) builds
   and commits throwaway git repositories and carries the `--work`/refused-root machinery;
   the scored path (`measure()`) writes nothing and needs no work directory, so a selftest
   could call the same `measure()` on two literal ledger texts plus a stub reader answering
   `listing`/`blob` from a dict. The peer seat declined this, on three grounds: the lane's
   own `quality/check-tool-ledger.py --selftest` already builds fixture repositories (lane
   convention), the repo path is the only thing that exercises the git plumbing, and its
   `SELFTEST_CHECKS` fixed-count guard caught an in-flight regression. I record the
   disagreement rather than resolve it: the change is confined to the selftest block and
   does not touch a clause, so it is a size-versus-git-path-coverage trade for the
   integrator, not a predicate question.
2. **One summary line (resolved).** The draft prints a single `C1_R52:` line and already
   uses the harness alias spellings (`self_pointer`, `generic_desc`), so no profile edit and
   no alias table is needed; keep it that way rather than adding a second format.
3. **Keep the narrowed all-cell rule and its `note` line** (the G case): the scan fires
   only when the pointer region yields no accountable target, which keeps G green while the
   frozen control stays red. Document the two meanings of `self_pointer` and keep
   `note path=… names-the-ledger-in-prose` in the receipt so a scored self-reference is
   distinguishable from an informational mention. My earlier preference for a documented
   fail-closed rule is withdrawn: it bought one branch at the price of a real false failure.
   Resolved in the peer receipt: `receipts/receipts.txt` line 74 carries the note line for
   G next to the scored self-pointer lines for B/C/E.

**Gate coexistence — the integrator's remaining decision.** Neither counter consults
`quality/check-tool-ledger.py`: my reference drops the call by design (§3), and the final
peer draft contains no reference to it (measured: `grep -n "check-tool-ledger\|LEDGER:"
C1CounterDesign/c1-r52-ledger.py` → no match). r51's cross-check is therefore gone in both
candidates, and the lane gate's `LEDGER:` line has no `self_pointer`/`generic_desc` field to
agree on. Decide explicitly which gate is authoritative for which fields this round; my
recommendation is that the new counter owns the r52 C1 receipt while the old checker remains
the lane-level ledger gate, and that the receipt says so instead of implying one gate
corroborates the other.

## Deliverables

- `.ufo/waves/round-52/w1/C1Simplify.md` — this report.
- `.ufo/waves/round-52/w1/C1Simplify/c1-r52-ledger.py` — minimum-size reference counter (194 lines).
- `.ufo/waves/round-52/w1/C1Simplify/receipts.txt` — measured green/red/mutation/ancestor receipts.
- `.ufo/waves/round-52/w1/C1Simplify/gen-controls.py` — deterministic control generator (read-only git).
- `.ufo/waves/round-52/w1/C1Simplify/control-B-row-selfpointer.md` — recommended scored red control.
- `.ufo/waves/round-52/w1/C1Simplify/control-C-ledger-selfpointer.md` — ledger-self isolation.
- `.ufo/waves/round-52/w1/C1Simplify/control-D-generic-desc.md` — context isolation.
- `.ufo/waves/round-52/w1/C1Simplify/control-E-one-selfpointer.md` — minimal single-defect isolation.
- `.ufo/waves/round-52/w1/C1Simplify/control-F3-forged.md` — forged control; passes the reference, 10/82 rows rejected by the final peer draft (ceiling).
- `.ufo/waves/round-52/w1/C1Simplify/control-H-minimal-forgery.md` — one row, description `PRED-C1-r47 does things.`; accepted by both counters (minimal context-clause forgery).
- `.ufo/waves/round-52/w1/C1Simplify/control-G-legit-ledger-reader.md` — legitimate row naming the ledger; false positive of the peer draft's first all-cell scan, green after its narrowing.
- `.ufo/waves/round-52/w1/C1Simplify/mut-dup.md`, `mut-emptydesc.md`, `mut-badpointer.md` — discrimination mutations.

Report: `.ufo/waves/round-52/w1/C1Simplify.md`
