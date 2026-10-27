# C1 frozen-control attack — C1ControlAttack

Axes considered: **operability** (primary), **coverage** (none demonstrated). This is an attack on frozen C1 control validity, not a vote or predicate amendment.

## Counterexample

`controls/c1-do-nothing.md` is not an isolating control for the frozen failure modes. Its table has four columns (`Tool | Reads | Writes | Owner and adjacent lanes`), whereas the production ledger states a three-column row grammar (`path | description | pointer`). It also repeats the exact same `tools/mado-verify.sh` row twice. A checker that reports only a population/row uniqueness or malformed-shape defect can reject this control without demonstrating it detects either self-pointers or missing instrument-specific functional context. The frozen registration requires failure *specifically* for self-pointer/context defects, so this control does not establish that criterion unless the run reports those defect classes independently despite the confounds.

The exact control rows each use `quality/tool-ledger.md` in the Reads column and `nothing` in Writes; the final cell says “generic accountability pointer to this ledger itself.” Under the old checker parser, cell 1 is treated as path, cell 2 as description, and cells 3 onward as pointer: consequently `nothing` is not a resolvable pointer token. The old counter’s independent parser similarly would not recognize the final cell as a pointer because its pointer tokens require backticks or path-like tokens. Thus a failure on this control under either old path would be attributable to schema/pointer parsing and duplication, not a targeted demonstration of self-pointer/context detection.

## Evidence

- Frozen claim C1: `claims-frozen.md`, section C1 — requires production pass and control fail “specifically for self-pointer/context defects.”
- Frozen registration: `registration.md`, “Frozen predicates” C1 — requires uniqueness, resolvable/non-self evidence pointer, instrument-specific functional context, and control failure specifically on self-pointer/context defects.
- Control bytes: `.ufo/waves/round-52/controls/c1-do-nothing.md` — four headings; two byte-identical rows, each with generic self-pointer wording.
- Production schema: `quality/tool-ledger.md`, “Row grammar” — three cells; describes pointer as a tracked repository file naming the instrument.
- Old parser evidence: `quality/check-tool-ledger.py`, `parse_rows()` (three cells required; malformed rows counted as dangling), `evaluate()` (duplicate path counted as dangling; description checked only for blank/placeholder; pointer checked for path existence and basename mention). `quality/counters/c1-r51-ledger.py`, `parse_rows()` and `pointer_resolves()` (remaining cells joined as pointer; pointer resolution checks whether the row basename occurs in pointed-to bytes). Those rules do not establish functional-context semantics or exclude self-pointer targets.
- Base and source status: lane HEAD observed as `85d57a818c3707397e21c840b6498b105ba798aa`; `receipts/c1-base.txt` records the prior counter’s 82/82 TARGET_MET result. The new C1 counter is absent from the base tree listing.

## False-positive bypasses against the frozen predicate

1. **Duplicate/schema confound (control itself).** A counter may reject for duplicate rows or malformed rows and still never implement the required self-pointer/context clauses. Item attacked: C1 control validity / the control’s red-result specificity.
2. **Circular or shared evidence.** “Resolvable” plus “non-self” does not itself mean an evidence target independently supports the row. Two instruments can point to each other, or every row can point to one shared document that merely names all basenames. Item attacked: C1 non-self resolvable evidence target. This is a predicate gap unless counter behavior additionally requires meaningful target evidence; whether that is in frozen scope is ambiguous, so it should be rejected only if the implementation claims such evidence semantics.
3. **Description keyword forgery.** “Instrument-specific functional context” is not operationally defined in the frozen text. A counter that checks for the basename plus a small vocabulary (e.g. “parses”, “checks”, “runs”) can accept fabricated descriptions unrelated to the instrument’s source. Item attacked: C1 context check. This is the strongest remaining bypass: the safe bounded correction is to make the control isolate the specified defects and require the counter’s red receipt to identify them separately; do not silently expand the predicate into automated semantic entailment.

## Smallest safe correction

For the control fixture only, preserve the committed ledger shape and make its population rows unique and schema-valid, with each description non-placeholder and each pointer a resolvable path. Then deliberately retain only the two intended defects (self-pointer and generic context). Require the counter’s red receipt to show both defect categories, not merely a nonzero exit. This tightens the experimental control without editing frozen claims or predicates. For the broader context ambiguity, report it as a bounded-check limitation; do not claim prose entailment.

## Commands and results

- `git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD` → `85d57a818c3707397e21c840b6498b105ba798aa`.
- `read` of frozen claim, registration, control, production ledger, old counter, and old checker confirmed the evidence cited above.
- `df -h /fast` → 804G total, 204G used, 600G available (26%); scratch directory `/fast/scratch/hyaku/mado-r52/C1ControlAttack/` created.
- No fixture driver/counter was executed and no Git fixture was committed: the assignment explicitly forbids producer execution and Git mutations. Therefore the forgery bypasses above are source-level counterexamples, not claimed runtime results. No external source candidate used; no URL/access date/quote applies. No packages installed.

## Deliverables

- `.ufo/waves/round-52/w1/C1ControlAttack.md` — this scoped attack report.

Report: `.ufo/waves/round-52/w1/C1ControlAttack.md`
