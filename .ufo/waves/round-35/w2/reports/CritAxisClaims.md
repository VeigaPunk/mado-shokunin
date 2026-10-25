# CritAxisClaims — claim/axis binding, round 35 wave 2

Seat: `L1Mado35.CritAxisClaims` (critic, UFO-FSD). Read-only attack: every lane byte was
read; the only writes are under
`.ufo/waves/round-35/scratch/CritAxisClaims/` and this report. No install or upgrade was
needed (no tool installed). `scratch/<Seat>/` was then **moved** to
`scratch-evidence/<Seat>/` at ~03:43 and committed (`4efaf63`, `b632f0b`); the writable
copy was removed by a later sweep and restored **byte-identically from that checkpoint**
(not rebuilt from memory — see §Limits). Every verdict below is inlined, so no finding
depends on a scratch path surviving.

## Measured revisions (state as observed, 2026-10-25)

| Ref | Value | Note |
|---|---|---|
| round-34 lane tip | `dff394109f3cc3d851309ad7c67dd3b35b46adf2` | the tip the registration names |
| round-34 data commit | `fa7ba11346116672352b5d41494141c5c4d738d0` | the mislabelled "tip" of the r34 blob artifact |
| round-35 freeze | `19e4ab3171c1540c40d6b12097745af98053b07d` | predicates, clause ledger, controls, receipts, blob ledger |
| round-35 data | `02088b4dff0da153df30ff174611d1257c92d0cd` | the three entries + S203–S210 landed **while this seat ran** |
| working tree at first measurement | `M LOG.md`, `M corpus/README.md`, `M corpus/knowledge/idle-lock-{never-asked-r12,chain-armed-r14,offered-in-the-bar-r15}.md`, `M corpus/lessons/round-35.md` | wave-2 errata + the `## Mistakes` summary paragraph |
| working tree at re-measure | the above plus `M corpus/QUALITY.md` (one-line append to criterion 55's citation: "…(lesson: lessons/round-35.md#mistakes M35-2)") | re-projected gate unchanged: `calibration published=41/41 derived=43/43 STALE`, `navigation published=47/47 derived=50/50 STALE`, `operability MATCH`, `exit=1` at `76471baa…` (scratch projection) |

The lane moved under this seat (`git status` lost the S203–S210 and QUALITY.md
modifications between two reads because the data commit landed). Every verdict below names
the revision it was measured at.

## Axes named

The round declares two claims on two axes: **C1 = coverage** (corpus admission of the
idle-lock control surface), **C2 = calibration** (the lane's self-description of its own
evidence ledger). The lane's published axis table at the round-34 tip carries three scored
sub-axes: `navigation` (coverage), `calibration resolved-active`, `operability selftest`.
First measured: counters and gate are green at the r34 tip and at the r35 data commit for
C1/C2 — the attacks below are about what those greens bind to, not about whether they run.

---

## (a) C1 coverage / C2 calibration are distinct axes — **PASS, with a named caveat**

**Distinct by label and by surface.** C1's counter reads `corpus/knowledge/…`,
`corpus/SOURCES.md` and `.ufo/waves/round-35/fetch/*` only. C2's counter reads
`.ufo/waves/round-35/c1/clauses.json`, the `c1` control receipts, the r35 blob ledger and
`git rev-parse <r34 tip>:<path>` only. Neither reads the other's claim data:

```
T1  C2 on a tree with the 3 entries + S203–S210 + index rows absent:
    PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET   exit=0
    (the same tree, C1: closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED       exit=1)
T2  C1 on a tree with .ufo/waves/round-35/{c2,ledger} deleted:
    PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET                exit=0
```
Receipts: `.ufo/waves/round-35/scratch-evidence/CritAxisClaims/sep-out.txt` (script
`sep.sh`), committed at `b632f0b`; the writable `scratch/CritAxisClaims/` copy is transient
(it has been swept twice) and is not a citation target.

**Caveat (not a blocking violation).** C2's subject *is* C1's instrument: 9 of its 10 live
clauses are clauses of the round-35 admission counter, and `uncovered` is a property of
that counter's control suite. Only `retired`, `toctou_declared` and `ledger_tip_ok` are
calibration proper; the dominant metric is instrument falsifiability — the same property
the r34 capabilities row attributes to the *coverage* counter. The labels are distinct;
the subject matter overlaps. Report it, do not relabel a frozen claim.

---

## (b) At least one claim works the lowest-scoring non-retired axis — **PASS on the quote, violations named**

**The published table at the round-34 tip** (`git show dff3941:SCORECARD.md:2110`, verbatim):

> Axis table re-derived at the round-34 data tree (criterion 22): **navigation 47/47 = 1.0;
> calibration resolved-active 41/41 = 1.0; operability selftest 12/12 = 1.0.** Not an
> axis-score claim.

All three are tied at 1.0, so any claim on one of them sits on a (joint) lowest non-retired
axis. The lane's own gate agrees at that tip:

```
python3 -I quality/check-axis-scores.py --rev dff3941 --repo .
MADO_AXIS_ROW: axis=navigation published=47/47 derived=47/47 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=41/41 derived=41/41 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=dff394109f3cc3d851309ad7c67dd3b35b46adf2
gate_dff3941_exit=0
```

`12/12` is the index instrument's own assertion count; the r34 correction appended at the
tip (`SCORECARD.md:2134-2135`) says the *axis-gate* selftest is 18/18. Both are 1.0; the
published cell names the index instrument, and the gate derives the same one. No conflict,
but the cell label "selftest" is ambiguous and the r35 registration inherits that
ambiguity without a pointer.

**Violation B1 — the enumeration "three tied sub-axes" is not the complete non-retired
set; `sourced-art` was silently dropped from the publication.** The round-32 publication
had four cells (`git show dff3941:SCORECARD.md:2063-2065`):

> Axis table re-derived at tip (criterion 22): navigation 46/46 = 1.0; calibration
> resolved-active 41/41 = 1.0; **sourced-art 1.0**; operability selftest 12/12 = 1.0.

The round-34 republication has three. `SCORECARD.md` §Retired still says "none retired;
record with justification when an axis is retired", and the gate's `AXES` tuple is
`("navigation", "calibration", "operability")` (`quality/check-axis-scores.py:32`), so the
gate cannot see the dropped cell. Last published `sourced-art` value was 1.0, so the
lowest-axis *conclusion* survives — but the registration's premise ("three sub-axes tied
at 1.0") is true only because the table lost a row without a retirement record.
Smallest safe correction: add a `sourced-art` line to `SCORECARD.md` §Retired with the
reason (not re-derivable by the gate) or restore it to the publication with its
instrument; do not amend the frozen registration.

**Violation B2 — neither claim moves the published sub-axis it is bound to; the only
round-35 movement of the published calibration instrument is negative at the data commit.**

- C1/coverage: the published coverage cell is `navigation`. C1's data preserves it —
  working tree measured `notes=50 indexed=50 dups=0` (50/50, still 1.0) — but at the data
  commit the published `47/47` is stale against the derived `50/50`.
- C2/calibration: C2's counter never reads `corpus/QUALITY.md` or
  `.ufo/waves/round-30/c2/count.py`, the instrument behind the published
  `calibration resolved-active` cell. Its target is a different calibration sub-surface.
  The round's only touch of the published calibration instrument is the QUALITY append
  (criteria 55/56 at `corpus/QUALITY.md:361-362`, committed in the data commit), and at
  that commit it **lowers the derived calibration axis**:

```
python3 -I quality/check-axis-scores.py --rev 02088b4 --repo .
MADO_AXIS_ROW: axis=navigation published=47/47 derived=50/50 verdict=STALE
MADO_AXIS_ROW: axis=calibration published=41/41 derived=41/43 verdict=STALE
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=2 rev=02088b4dff0da153df30ff174611d1257c92d0cd
gate_at_current_head_exit=1
```

Cause, from the instrument's own output at that tree: criteria 55/56 cite
`lessons/round-35.md#mistakes M35-2`, and the committed lesson at `02088b4` names M35-2
only in a `### M35-2` subsection heading, not in the `#mistakes` section body:
`UNRESOLVED criterion 55`, `UNRESOLVED criterion 56` → `active=43 resolved_active=41
fraction=0.9535`. The uncommitted working-tree lesson edit adds a section-level M35 list
("Four mistakes, named here at section level so a citation check that reads `#mistakes`
sees them") and repairs the derivation. Rubric quirk worth recording: the round-31
instrument resolves a `file#anchor id` citation only against the section *body prose* —
an id that appears solely as a `### M35-2` subsection heading does not resolve. That is why
the same lesson served `41/43` at the data commit and `43/43` one prose paragraph later.
Projection with those edits committed:

```
gate with the working-tree lesson committed (scratch clone of 02088b4 + working-tree files):
MADO_AXIS_ROW: axis=navigation published=47/47 derived=50/50 verdict=STALE
MADO_AXIS_ROW: axis=calibration published=41/41 derived=43/43 verdict=STALE
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=2 rev=335e0f8878777dc426cf08ebc41756b4757f302b
gate_projected_close_exit=1
```

So the registration's "no axis is lowered" is **false at the landed data commit**
(calibration 1.0 → 0.9535) and becomes merely "publication stale" once the lesson edit
lands. The round cannot close with the gate red: the axis-table republication (r34's own
practice — "The publication is updated so the existing gate does not go red when the new
note is indexed") is not named anywhere in the round-35 registration.
Smallest safe correction: (i) commit the lesson's section-level M35 list before close —
without it, round 35 ships a derived calibration fraction below the published 1.0; (ii)
append the r35 publication line `navigation 50/50 = 1.0; calibration resolved-active 43/43
= 1.0; operability selftest 12/12 = 1.0` (re-derived, not asserted) so the gate returns to
exit 0 at the close tip.

**Violation B3 — the coverage *before* state in the registration is falsified.** The
registration says the corpus "holds no measurement of the *offer*: the bar module, the menu
entry or the indicator's tooltip were never opened by this lane." At the round-34 tip:

```
git grep -n -i "idle lock" dff3941 -- corpus/knowledge
config-health-report-r3.md:298   `idle.sh` currently renders the disabled glyph + tooltip "Idle lock disabled".
idle-lock-plane.md:286           `idle.sh:3-6` prints the "idle lock disabled" glyph + `"class": "active"`
waybar-walker-plane.md:109       tooltip "Idle lock disabled", class `active`.
waybar-walker-semantics.md:139   | `custom/idle-indicator` (`:206-211`) | … tooltip "Idle lock disabled" … L → `omarchy-toggle-idle` … RUN `{"text": "󱫖", "tooltip": "Idle lock disabled", "class": "active"}`
```

`waybar-walker-semantics.md:139` is a **RUN-measured** module row (payload incl. tooltip,
click dispatch, signal), and `idle-lock-plane.md:284-289` measures the module's config
lines and the indicator's two-state script. The bar module and the tooltip were opened,
measured and published two rounds earlier. What is genuinely new in round 35: the menu
entry (S208), the dated config copies (S209), the toggle-state directory (S210), the
setup-path negative (S203/S204) and the host chain liveness (S205) — none of which the
corpus measured at `dff3941`. C1's count is unaffected by this, but the "new surface"
premise is overstated and the r15 entry duplicates a measurement that already exists in
`waybar-walker-semantics.md` §3.2 (two notes now speak about the same module row).
Smallest safe correction: record the corrected before-state in the round report/lesson
(the registration is frozen): "the corpus measured the bar module's file and RUN semantics
(`waybar-walker-semantics.md:139`, `idle-lock-plane.md:284-289`); it held no measurement of
the menu entry, the dated copies or the toggle-state record."

---

## (c) Stagnation nudge does not apply — **premise false against the canonical table; conclusion survives via the per-round table**

**Check the canonical capabilities table at the round-34 tip** (`git show
dff3941:SCORECARD.md:200-206`):

> ## Capabilities
>
> | Capability | What it can now do | Evidence pointer | First-working round |
> |---|---|---|---|
> | — none yet — | | | |
>
> Rows enter only through a round that demonstrates the capability running (`AXES.md`
> §Capabilities); none enter through this rollout.

The canonical table has never carried a row: `git log -S "| — none yet — |" -- SCORECARD.md`
returns only `c1b548a` ("protocol conformance … additive scaffolds only"), the 2026-10-16
rollout. The round-34 capability row lives only in the per-round subsection
`SCORECARD.md:2142` ("crib-rejecting coverage counter … First-working round: 34"). So
"a capability entered the capabilities table in round 34" is **true of the round-34
subsection and false of the canonical `## Capabilities` table**. AXES §Capabilities names
the SCORECARD capabilities table in the singular; the canonical one governs on a strict
reading.

The same dual authority exists for the nudge's other conjunct. Canonical `## Saturation` at
the r34 tip (`dff3941:SCORECARD.md:208-210`) still reads "The lane's saturation line and
stagnation window N are to be declared by the lane on its next round … not asserted by
this conformance change", while the round-12 block in the same file declares
`Saturation line: 9.0 … Stagnation window: N = 3` (`SCORECARD.md:272`) and
"Stagnation window resets: a capability entered this round" (`SCORECARD.md:313`). Scale is
also unresolved: the published cells are fractions (1.0) and the saturation line is 9.0
(0–10), so "every axis sits at or above the saturation line" cannot be evaluated from the
published table at all.

**Conclusion.** The nudge can only *waive* the lowest-axis obligation, and both claims sit
on axes tied at 1.0, so no admission criterion breaks under either reading. But the
registration's stated reason is not derivable from the canonical table, and the saturation
conjunct is never evaluated. Smallest safe correction: populate the canonical
`## Capabilities` table with the round-34 row (or retire the placeholder with a reason),
republish `## Saturation` with the operative line/number, and say in the round report which
table the nudge is evaluated against.

---

## (d) Claims are causally separable — **PASS at the claim-data level; one-way instrument coupling named**

Both divergence directions hold, which is the operative test:

```
T1  C2=TARGET_MET while C1=TARGET_MISSED (C1's entries/rows absent)          exit 0 / exit 1
T4  C1=TARGET_MET while C2=TARGET_MISSED (one control receipt deleted)       exit 0 / exit 1
T6  C1=TARGET_MET with c1/clauses.json and controls/ deleted                 exit 0
```

**Violation D1 — C2 cannot be verified without C1's instrument artifacts.**
```
T3  rm .ufo/waves/round-35/c1/clauses.json   → PRED-C2-r35-v1 error=clause-ledger-missing  exit=2
T4  rm .ufo/waves/round-35/controls/         → uncovered=9 … verdict=TARGET_MISSED          exit=1
```
C2's frozen spec points `clause_ledger` at `.ufo/waves/round-35/c1/clauses.json` and its
`uncovered` metric consumes the `c1` control receipts. If "C1 having landed" includes its
clause ledger and controls (they were committed in the same freeze commit as C1's
predicate, `19e4ab3`), C2 is not verifiable without C1's landing — the literal AXES
"each verifiable without the others having landed" fails in one direction. The
registration's own model treats C1's *claim data* as the corpus admission, and against that
model (d) passes cleanly. Smallest safe correction: move the clause ledger and control
receipts to a neutral path (`.ufo/waves/round-35/ledger/…`) so C2's subject does not live
under `c1/`, or state in the round report that the clause ledger is C2's subject data.

---

## Additional violations found while attacking the binding (same evidence surface)

**V1 — C2's `retired` metric is unanchored; the registration's "r34 `quote-equals-frozen`
clause" does not exist as an artifact.** r34's counter has no clause ids at all: the word
bound is inline, `found == quote and 1 <= len(words) <= 25`
(`.ufo/waves/round-34/c1/count.py:152-153`, blob `49089c18…`). The r35 ledger invents the
labels `r34-word-bound-1-25` / `quote-equals-frozen` and the counter only asks that a
retired id be absent from the live list (`c2/count.py:94-97`). A fabricated id passes:

```
T5  retired = [{"id": "phantom-clause-never-in-r34", "why": "fabricated"}]
    PRED-C2-r35-v1 uncovered=0 retired=1 … verdict=TARGET_MET    exit=0
```
Impact: calibration axis (C2's own claim). Smallest safe correction: give the retired entry
a `r34_ref` naming the exact bytes it retires
(`.ufo/waves/round-34/c1/count.py:152-153` at `dff3941`, blob `49089c18…`) and have C2
require that the cited construct is present at the r34 tip and absent from the live clause
list; a phantom id then cannot count.

**V2 — C2's `uncovered` accepts one receipt for every clause, and is not bound to the
counter's bytes.**
```
T7  all 9 load-bearing clauses pointed at the single controls/c1-entry-symlink receipt
    PRED-C2-r35-v1 uncovered=0 … verdict=TARGET_MET              exit=0
T8  .ufo/waves/round-35/c1/count.py replaced by a 2-line stub that prints TARGET_MET
    PRED-C2-r35-v1 uncovered=0 retired=1 … verdict=TARGET_MET    exit=0
```
The counter tests `verdict=TARGET_MISSED` presence in a named receipt, not "for which that
clause is the load-bearing check" — the stronger wording the round's own new QUALITY
criterion 56 requires (`corpus/QUALITY.md:362`: "a control whose committed receipt records
a `TARGET_MISSED` verdict **for which that clause is the load-bearing check**"). C2 can
therefore report `uncovered=0` on a counter whose implementation is anything.
Impact: calibration axis; the C2 claim's "every live clause accounted" is a statement about
`clauses.json`, not about `c1/count.py`. Smallest safe correction (round 36 per the lane's
own M35-2 fix list): one distinct committed control per clause, the control mutating only
the construct that clause implements, and C2 re-deriving the clause list from the counter's
bytes at the frozen blob id.

**V3 — C1's coverage counter is shape-only; the digest clause the registration names is
computed and discarded.** `c1/count.py` computes `digest = hashlib.sha256(blob).hexdigest()`
and never uses it; the `ok` block tests `receipt["sha256"] in cs[5]` (the *frozen* digest
string present in the row's anchor cell), so mutating the receipt bytes leaves the verdict
unchanged. Re-proved after the scratch move with a self-contained minimal root (no junk tree
and no git needed; script and receipt committed at
`.ufo/waves/round-35/scratch-evidence/CritAxisClaims/{digest.sh,digest-out.txt}`):

```
== D0 minimal root, real receipts =========================================
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET   exit=0
== D1 one receipt mutated (one byte appended) ==============================
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET   exit=0
== D4 S203 receipt fabricated: different bytes, gate-quote still present ====
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET   exit=0
   sha256 of the fabricated receipt = 5b262a2ed88a28061b9c9235ab6cd0d2549203b28a91d33f6fd5cfb0dbee75d5
   frozen digest for S203            = 1b7fa87ffe933990ee59acf3629ffbe3a90106bc9ebcce082237f7f495dd1646
== D3 control bite: S203 row's anchor digest zeroed =========================
PRED-C1-r35-v1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED exit=1
```

D4 is the decisive case: a receipt whose bytes hash to something else still closes the cite,
because `digest` is computed and discarded. D3 shows what `controls/c1-digest` actually
kills — the *row's* digest token, not the receipt's bytes. The lane's own durable junk-tree
receipt is `.ufo/waves/round-35/w1/reports/CritVacuous.md:1-13` (same command,
`TARGET_MET`); the `scratch/CritVacuous` tree itself was among the 3.2 GB mutant trees
dropped by the evidence checkpoint, so it is no longer re-runnable.
This is the lane's own M35-2, stated in the round's committed lesson; the registration's
predicate sentence ("whose anchor cell carries the sha256 of the named receipt") reads
stronger than the implementation. The clause ledger lists `digest-match` as a live,
controlled clause — but the control `controls/c1-digest` mutates the *row*, not the
receipt, so it kills the presence check, not the receipt-authenticity check the predicate
names. Impact: coverage claim's evidence strength (the binding target, not its axis label);
calibration claim (C2 certifies a clause whose failing case is not the control that exists).
Smallest safe correction for this round: report C1's verdict with the M35-2 limit in the
round report (as the lesson already does), and do not let the registration's predicate
wording stand as if receipts were bound; round 36 binds the digest to the bytes read.

---

## Verdict summary

| Check | Verdict | Blocking? |
|---|---|---|
| (a) distinct axes | pass (subject overlap reported) | no |
| (b) lowest non-retired axis | pass on the quoted table; violations B1 (sourced-art drop), B2 (published sub-axes unmoved; calibration derived 41/43 at the data commit, gate exit 1), B3 (coverage before-state overstated) | B2 **blocking at close**: gate red until the lesson edit is committed and the axis table republished |
| (c) nudge does not apply | premise false against the canonical capabilities table; conclusion survives via the per-round row | no (nudge only waives), but fix the dual authority |
| (d) causal separability | pass on claim data (T1/T4/T6); D1 one-way coupling to C1's instrument artifacts | no |

No axis is lowered *after* the working-tree lesson edit lands and the publication is
updated; as the tree stands at `02088b4` the lane's own calibration instrument reads
`41/43 = 0.9535 < 1.0` and the gate exits 1, which contradicts the registration's "no axis
is lowered."

## Limits of this review

- I did not re-open the host receipts' bytes against the live host (`S203`–`S210`); the
  receipt-content question is other seats' assignment. I tested only what the counters and
  the published instruments bind to.
- The T7/T8 mutants were made in scratch clones with `git clone --shared` (objects borrowed
  read-only); no lane file, index, jj state, or sibling repo was written.
- The lane moved during the run (data commit `02088b4` landed mid-review); the
  working-tree state at the final read is recorded above.
- **Scratch provenance.** `scratch/<Seat>/` was *moved* to `scratch-evidence/<Seat>/` at
  ~03:43 and the checkpoint committed (`4efaf63`, 240 files / 59 seat dirs; a later commit
  `ca870e9` records the lane without scratch trees). This seat's `sep.sh`, `sep-out.txt`,
  `reuse.sh`, `reuse-out.txt` were checkpointed byte-identically at
  `scratch-evidence/CritAxisClaims/` (first committed in `b632f0b`), and the writable
  `scratch/CritAxisClaims/` copy was restored **from that commit** (md5 equal:
  `sep-out.txt bd38a7a4…`, `reuse-out.txt 9493f268…`) — not rebuilt from memory. New
  post-checkpoint probes (`digest.sh`/`digest-out.txt`) live only in the writable scratch;
  their verdicts are inlined in V3 above, so the report body is the durable locus.
  `scratch-evidence/CritVacuous` does not exist: that tree was among the 3.2 GB mutant
  trees dropped by `4efaf63`, which is why V3 now carries a receipt-free minimal-root probe
  instead of a junk tree.
