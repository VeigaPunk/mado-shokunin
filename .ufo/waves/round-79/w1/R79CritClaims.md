# R79CritClaims — adversarial falsification of the two frozen claims (round 79, ONE v1 wave)

Seat: R79CritClaims (critic, leaf). Scope: the two frozen claims of
`.ufo/waves/round-79/claims-declaration-r79.md` (freeze `5eb8f20fe291603c74973fa94cc55723ac8089a4`).
All experiments ran against the FROZEN bytes at that revision, extracted with read-only `git show`
(counter sha `48ebfab6…`, tool sha `c9aa1391…`, controls sha `5f7ebb3c…` — verified against the
declaration pins at review start). Scratch fixture repo: `/fast/scratch/hyaku/mado-r79/R79CritClaims/crepo`
(every git call named `-C`; deleted at close). Evidence copies in `w1/R79CritClaims/evidence/`.

Re-derivation commands (as declared), both run from the lane root:

- C1: `python3 -I quality/counters/c1-r79-reserve.py --repo . --rev 5eb8f20f… --base-rev e4b153df… --controls .ufo/waves/round-79/controls/c1-cases-r79.json --carried .ufo/waves/round-78/controls/c1-cases-r78.json --scratch-root DIR`
- C2: `python3 -I quality/counters/c2-r79-runbook.py --repo . --rev 5eb8f20f… --controls .ufo/waves/round-79/controls/c2-runbook-cases-r79.json --carried .ufo/waves/round-78/controls/c2-runbook-cases-r78.json --scratch-root DIR`

## 1. C1 — cheapest route to `correct=23, killed=12, base=18` without the claimed composition

Setup: scratch fixture repo; base commit = `tools/mado-barfoot.py` bytes from `e4b153df…`
(sha `1bceb514…`, rev `95685aa3…`); cheat commits scored by the FROZEN counter
(`evidence/c1-r79-reserve.py.5eb8f20`) against the frozen 23-case set and the round-78 carried set.

### Route A — answer-key table (caught)

`evidence/cheat-a-answerkey.py` (~60 lines): reads the four input files only to fingerprint them
(sha256 of config|layers|monitors|rules|monitor), and prints the frozen receipt's own per-case
fields from a 23-row table. No model code at all; `--selftest` prints a fabricated `1/1`.

Command + observed output (`evidence/cheat-a2.txt`):

```
python3 -I <frozen c1 counter> --repo crepo --rev 0efc2e2d… --base-rev 95685aa3… --controls …r79.json --carried …r78.json --scratch-root …
MADO_R79_BARFOOT: cases=23 correct=23 mutants=12 killed=0 base_correct=18/23 carried=18/18 tool_selftest=1/1 verdict=TARGET_MISSED
```

The case score is fully forgeable (`correct=23`); the catch is the kill rule `killed < 12`:
every one of the 12 mutation anchors is absent from the table tool, and an anchor that occurs
other than exactly once is reported `anchor-absent`, never a setup error — frozen counter lines
189 (`if count != 1: raise Setup`) and 334–338 (`reason=anchor-absent`). The counter **catches**
this route. (An earlier generator version that scored 22/23 due to a KeyError is kept as
`evidence/cheat-a.txt`; it does not change the verdict.)

### Route B — fingerprint-aliased rules input (NOT caught)

`evidence/cheat-b-fingerprint-alias.py` = the honest frozen tool with a ~5-line patch at the one
rules call site (tools/mado-barfoot.py @5eb8f20, line 847):

```python
_raw = read_text(args.rules)
_raw = _ALIAS.get(hashlib.sha256(_raw.encode("utf-8")).hexdigest(), _raw)
static = parse_static_reserve(_raw, monitor)
```

`_ALIAS` maps the five new cases' committed rules bytes to DIFFERENT text: static-last-wins'
`10,0,0,0 / 26,0,0,0 / M2 5,0,0,0` becomes `1,0,0,0 / 26,0,0,0 / M2 9,0,0,0`; static-composed's
single `addreserved 26` becomes a two-rule last-wins pair `13` then `26`; static-source-refused's
`source = ~/.config/hypr/other.conf` becomes `source = ~/alias-from-the-seat-table.conf`.
`parse_static_reserve` (lines 334–363) never receives the committed bytes for any of the five new
cases — the parsed slot values are the seat's table, laundered through the real parser so the five
static-mutant anchors stay live and mutation-sensitive.

Firing proof (`evidence/probe.txt`), control case `static-source-refused`:

```
committed rules bytes: 'source = ~/.config/hypr/other.conf\n'
honest tool : MADO_BARFOOT: ERROR (stage=model the rules file carries a `source =` line (line 1); …)   rc=3   (tools/mado-barfoot.py:355-357)
aliased tool: MADO_ALIAS_FIRED: fired   MADO_BARFOOT_STATIC: monitor=M1 top=26 … source=rules   rc=1   (probe variant maps to a valid addreserved 26)
```

The committed bytes are demonstrably not consulted. The scoring run (`evidence/cheat-b.txt`):

```
MADO_R79_BARFOOT: cases=23 correct=23 mutants=12 killed=12 base_correct=18/23 carried=18/18
                  tool_selftest=43/43 verdict=TARGET_MET rev=482fa999… tool_sha256=b5b79124…
```

**Every clause of the frozen C1 predicate passes** with a tool whose binding to the config tree
is a lookup table.

### Q1 verdict

The target is **under-specified with respect to the claimed composition's binding clause**. The
declaration claims "the static reserved area a `monitor = NAME, addreserved, …` rule declares is
**read from the same config tree (`--rules`)**" — no machine-checked clause enforces it. What the
kill rule does enforce is the anchor arithmetic's liveness (mutations `static-dropped`,
`static-order-swapped`, `static-first-wins`, `static-box-unoffset`, `static-selector-ignored` at
frozen-counter lines 48–90 must each flip ≥1 case) — and Route B keeps those lines live while
sourcing their inputs elsewhere. `expected_ok` (lines 153–164) checks only the subset of fields
present in each expectation and never inspects the tool's own `STATIC` row
(tools/mado-barfoot.py:515), so output-pinning would not close this either: any expectation a
table can encode is forgeable, since the corpus is finite and committed.

**Smallest safe correction.** Have the counter re-derive the five new cases' static slot at run
time with its own ~40-line reference parser over the committed rules text and assert the tool's
printed `STATIC` row against it. That does not make a determined table impossible (a finite
committed corpus is always forgeable); it moves the forgery cost from "read the answer key" to
"reimplement the model inside the table" — at which point the seat has implemented the model.
The declaration should also name the bound honestly: the 23/12/18 contract certifies the
mechanics, not the provenance.

## 2. C2 — special-casing, execution, and `control_new=0/5`

### (a) A rule that only special-cases the five new cases: closed by construction

A successor matcher that returns True unconditionally for the five new kinds (`refusal`,
`lines_shape`) would be caught, because the four mutants anchored on those kinds derive their
entire killing power from the five new cases' frozen negative samples
(`.ufo/waves/round-79/controls/c2-runbook-cases-r79.json`, verified): every refusal case carries
negatives `(rc=2, "ERROR (stage=model …")`, `(rc=3, "ERROR (stage=setup …")`, `(rc=0, CLEAN)` —
so `refusal-rc-blind` (drops the rc check) accepts the first, `refusal-stage-blind` (drops the
stage check) accepts the second. Measurement margins confirm exactly this: both mutants scored
18/22 — precisely the four refusal cases flipping — and `lines-any-line`/`lines-min-lines-dropped`
scored 21/22 via the `lines_shape` negatives (1-line reply, arrow-less line, empty reply, rc=1
dump). A vacuous matcher spares those negatives → `killed=5 < 9` → TARGET_MISSED (kill logic,
`dead = mrc != 0 and (mm is None or mmatched < CASES)`, line 557).

Execution cannot be skipped: `executed += 1` runs once per case regardless of outcome (line 525)
and `matched` requires the live `(rc, stdout)` through `case_correct` (lines 526–527, 318–327);
the row bindings are exact command-cell equality with double-binding and no-row setup errors
(lines 509–517).

### (b) `control_new=0/5`: tautological, worthless as a predicate clause

`held_rule` (lines 309–313) returns False whenever `"frozen" not in case`, and none of the five
new cases has a `frozen` field (verified in the control); the four refusals exit rc≠0 behind the
held rule's rc==0 gate regardless. The counter's own output label admits the construction:
`held=fixed-value(no-frozen-value-for-the-five-new-rows)` (measurement receipt). The kill rule's
`control_new != 0 → claim fails` clause can therefore never fire for any subject on this frozen
set — it is dead weight in the predicate. The declaration is honest about this ("by
construction"), so it is bookkeeping, not a hidden flaw; but it proves nothing.

**Stronger control.** A negation/differential shadow set: permute the five new cases' values
(stage model↔setup, rc 3↔2, min_lines 100→10000, arrow regex→non-arrow) into a committed shadow
control file and require the same counter to score 0/22 (rc≠0) on it. That converts the
constructed zero into an observed zero — it fails if the matcher is ever vacuous for the new
kinds — and is still one command over committed bytes. (The existing control (a), the held r78
instrument against the 22-case set, rc 2, is non-tautological and should stay.)

### (c) Verdict per claim (Q2 summary)

- Special-case route: **closed** — the r79 mutant battery is anchored exactly where a vacuous
  new-kind matcher would sit, and the negatives are the ammo (evidence above).
- `control_new=0/5`: **tautological for this frozen set**; keep as documentation, or replace with
  the negation control; do not count it as instrument evidence.

## 3. Fleet §9 sizing verdicts (per claim, with reasons)

§9 asks: one concrete after-state, re-derivable with one command over committed bytes; no
universal clause without an enumeration; not the same axis twice.

### C1 — PASS, with two weak clauses

- After-state: `correct=23, killed=12, base_correct=18/23, carried=18/18, tool_selftest green,
  verdict=TARGET_MET, rev=5eb8f20f, tool_sha256=c9aa1391…` — one command, a pure function of
  `git show` at two revs plus two committed control files; no working-tree or host dependency.
- **Re-derivation observed**: `diff` of `receipts/measurement-c1-r79.txt` against my in-scratch
  rerun (`evidence/rerun-c1.txt`) — byte-identical, diff exit 0 — run after HEAD had already left
  5eb8f20f (the counter never touches the working tree).
- Universal clauses: none unenumerated — 23/12/18/18 are counts produced by enumerated loops.
- Weak clause 1: "a green tool selftest" is self-reported — the counter only checks `n==n` and
  rc 0 (frozen-counter lines 321–324); Route A fabricated `1/1` and this clause did not notice.
- Weak clause 2: the control set's provenance sentence ("expectations derived from the sources,
  not from a tool run") is a declaration-of-method; nothing machine-checks it — and Route B shows
  the same gap at the tool level.

### C2 — MIXED

- Clause enumeration is proper: 22 executed/matched, 17 shapes, 22/22 anchors with double-binding
  and no-row checks (lines 509–517), tree binding of SKILL.md/tool/fixtures (lines 493–501),
  carried-field equality (lines 486–490).
- Not a pure function of committed bytes: 17 carried rows execute live host verbs (hyprctl,
  omarchy) and the five new rows hit the live host or live tool; `matched=22` depends on host
  posture exactly like the printed `control_all`, which the counter itself demotes to "an
  observation, never a predicate" — yet `matched` stays a predicate. Fine on a stable lane;
  document it.
- Re-derivation is **time-boxed by the moving tree**: `tree=bound` compares the working tree,
  and the lane moved during this review (§4). Observed: the declared command exited rc 2
  `MADO_R79_RUNBOOK: ERROR (stage=setup SKILL.md in the working tree is not the measured
  revision's bytes)` (line 495) — `evidence/rerun-c2.txt`. At review start all 14 bound files
  were byte-identical to 5eb8f20f; they no longer are.
- Same axis twice? **No.** C1 moves the tool-model surface (coverage of the static-reserve edge
  class; instrument: tool vs frozen artifacts; do-nothing control = base tool). C2 moves the
  runbook surface (operability; instrument: live host + committed SKILL.md rows; do-nothing
  controls = held r78 instrument / held fixed-value rule). The four refusal rows overlap C1's
  refusal ground but score a different side (row binding + exit status, not model semantics).
- Smallest correction for C2 sizing: execute rows from a temp extraction of the rev's bytes
  (`git show` into scratch) instead of binding the working tree — keeps one-command
  re-derivation stable under lane movement — and either pin a host-posture note into the receipt
  or demote `matched` alongside `control_all` with the host-dependent rows covered by committed
  churn/negative samples only.

## 4. Lane movement observed during this review (data, not judgment)

- Review start: HEAD `03e76ee9`; controls sha `5f7ebb3c…` (declaration pin ✓); all 14 tree=bound
  files byte-identical to 5eb8f20f; C1 re-derivation byte-identical to the receipt.
- During the session, commits `3b8af34c` and `d6be05ef` ("round-79 repair R1", wave finding
  R79ScribeEntry F1) landed: SKILL.md (4 lines), `tools/mado-barfoot.py`
  (`c9aa1391…` → `673ac44d…`), `quality/counters/c1-r79-reserve.py` (9 lines),
  `.ufo/waves/round-79/controls/c1-cases-r79.json` (`5f7ebb3c…` → `108bde32…`), plus
  SCORECARD/LOG. HEAD is now `d6be05ef`.
- Consequences observed: the C2 declared command now fails rc 2 (§3); the C1 declared command now
  runs different counter and control bytes than the receipt's (its CONTROL line would print
  `108bde32…`, not `5f7ebb3c…`). The frozen bytes survive only at rev 5eb8f20f (`git show`).
  The declaration's unfreeze binds seats; the L1's integration is a separate authority. Recorded
  so the closure knows the receipts' re-derivation window on a live lane measured in minutes-to-
  hours, and that all §3 verdicts attach to the frozen revision, not the moving tree.

## 5. Evidence index (copies in `w1/R79CritClaims/evidence/`)

| file | content |
|---|---|
| `rerun-c1.txt` | C1 re-derivation at 5eb8f20f — byte-identical to the measurement receipt |
| `rerun-c2.txt` | C2 re-derivation after lane movement — rc 2, tree=bound failure (line 495) |
| `cheat-a2.txt` | Route A score: `correct=23 killed=0 … TARGET_MISSED` |
| `cheat-a.txt` | Route A v1 (generator KeyError, `correct=22`): kept for honesty |
| `cheat-b.txt` | Route B score: `correct=23 killed=12 … TARGET_MET` — the counterexample |
| `cheat-a-answerkey.py`, `cheat-b-fingerprint-alias.py`, `cheat-b-probe.py`, `gen-cheats.py` | the two cheats and their generator |
| `probe.txt` | alias firing proof (`MADO_ALIAS_FIRED`) on the static-source-refused case |
| `c1-r79-reserve.py.5eb8f20` | the frozen counter bytes used for all scoring (sha `48ebfab6…`) |

No repo, lane, counter, control-set, fixture, or host-config bytes were written by this seat;
scratch deleted at close.
