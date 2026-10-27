# Falsify19 — C1 no-work control validity

## Finding

- **Axes:** operability (C1); this attacks the frozen C1 control's ability to isolate its claimed defects.
- **Attacked item/predicate:** C1 registration: the new counter must fail `controls/c1-do-nothing.md` “specifically for self-pointer/context defects” (round-52 `registration.md:7,15`; frozen claim `claims-frozen.md:7`).
- **Concrete control confound:** the frozen control has two identical inventory rows, both for `tools/mado-verify.sh` (`.ufo/waves/round-52/controls/c1-do-nothing.md:3-4`). Thus it violates the separately claimed unique/complete population condition before the self-pointer or generic-context properties are considered. A red verdict on this fixture does not by itself establish detection of the self-pointer/context defects; it can be caused by duplicate/missing population accounting. This is a control-validity defect, not a claim that the control unexpectedly passes.
- **Source evidence:** the round-51 counter's `population()` deduplicates candidates with `sorted(set(pop))` (`quality/counters/c1-r51-ledger.py:133-148`), while `describe()` counts repeated ledger paths as `dup` and skips the duplicate row (`:211-248`); its verdict rejects any `dup` (`:415-430`). This illustrates why duplicate control rows are an independent failure condition in the legacy implementation. It is not evidence of how a not-yet-present round-52 counter handles the control.

## Reproduction and result

At the pinned lane HEAD `85d57a818c3707397e21c840b6498b105ba798aa`, inspect the committed control (`controls/c1-do-nothing.md:1-4`) and the frozen contract (`.ufo/waves/round-52/registration.md:7,15`). The control contains the exact same tool path twice; population uniqueness is therefore violated by inspection. The base receipt is only a production-ledger run (`.ufo/waves/round-52/receipts/c1-base.txt:1-4`, 82/82, TARGET_MET), not a run of this control. No round-52 counter exists at the pinned base, so there is no valid frozen-counter command/result to report for this control.

**Repro setup/command:** source-only inspection; `git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD` returned `85d57a818c3707397e21c840b6498b105ba798aa`; read `controls/c1-do-nothing.md` lines 1-4. No counter/producer was executed, no fixture created, and no host/source mutation made, respecting this round's source-only restriction.

**Reproduced:** yes — duplicate population row is directly present in frozen control bytes. The stronger claim that this necessarily causes a round-52 control run to fail for that reason is **not tested** (counter absent at base). Accordingly this finding shows the registered control is confounded, not that the future counter fails its production/control acceptance test.

## Limitations

No new round-52 counter or scored-revision receipt was available at base. I did not run any counter, package query, live read, producer, or host operation. No scratch/fixture was needed; no install. The control itself is frozen and was not changed. This is distinct from a semantic/context-threshold bypass: it identifies the named control's independent uniqueness defect.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify19.md`

Report: `.ufo/waves/round-52/w1/Falsify19.md`
