## Findings

### Evidence and attacked predicate

- **Axes:** coverage and operability. This attack targets C1's frozen uniqueness/population condition: “validates population row uniqueness” and the frozen claim's “unique population” requirement (round-52 `registration.md:7`, `claims-frozen.md:7`).
- Base counter receipt reports `population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0`, verdict `TARGET_MET`, revision `85d57a818c3707397e21c840b6498b105ba798aa` (`.ufo/waves/round-52/receipts/c1-base.txt:1-4`). It does not measure instrument-specific context or row uniqueness.
- Frozen control has duplicate `tools/mado-verify.sh` rows and points both to `quality/tool-ledger.md` itself (`.ufo/waves/round-52/controls/c1-do-nothing.md:3-4`).
- Current source checker (`quality/check-tool-ledger.py`) explicitly creates a sorted population (`population(blobs)`, lines 163-170); evaluation implementation lines 268-328 is the relevant future audit surface. The legacy counter's population helper returns `sorted(set(pop))` (`quality/counters/c1-r51-ledger.py:133-148`), meaning duplication is removed before its count is measured.

### Attack / result

Concrete bypass candidate: a counter that derives population using a set and compares only total `ledger_rows` to population can report 82/82 despite duplicated ledger instrument paths if it fails to separately enforce row-path uniqueness. This is grounded by the legacy counter's set-based population construction and the frozen control's exact duplicate rows. The old counter's recorded production pass is confirmed; the control itself was **not** executed because source-only assignment prohibits running producer/counter code.

**Reproduced: no.** The proposed bypass is a named failure mode, not a demonstrated result against the new round-52 counter (absent from this source view). The round-51 82/82 receipt is evidence of legacy acceptance metrics only, not proof that this exact control passes the old counter.

### Operational limits and verification

No package queries, live reads, producer execution, source checkout writes, or git/jj mutations performed. Disk guard: `df -h /fast/scratch` reported 600G available; no scratch artifacts created. No installs.

To verify once a new counter is available, use the pinned C1 target counter against the frozen revision and control ledger in a seat-local fixture, confirming production passes and duplicate rows fail specifically for uniqueness. Do not infer that result from the round-51 receipt.

## Deliverables
- `.ufo/waves/round-52/w1/Falsify18.md`

Report: `.ufo/waves/round-52/w1/Falsify18.md`
