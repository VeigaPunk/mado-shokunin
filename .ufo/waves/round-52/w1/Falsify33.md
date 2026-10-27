# Falsify33 — C1 self-pointer/context bypass

## Finding

Attacked item: C1 frozen control / the **non-self pointer and instrument-specific context** clauses. The frozen `controls/c1-do-nothing.md` is not a discriminating isolated test of those clauses against the pinned base counter: it has only two identical rows for `tools/mado-verify.sh`, while the base population is 82 files. The base counter's acceptance contract checks only that a pointer names a tracked file containing the instrument basename and that the description is non-empty. It has no context-specific predicate (see `quality/counters/c1-r51-ledger.py:28-31,196-208,229-236`). Thus, when evaluated by the old counter, this control would miss for the duplicate/coverage population defects, not specifically because its pointer is self-referential or its descriptions generic. **This identifies a control-attribution gap, not a reproduced false accept of the absent round-52 counter.**

## Reproducible setup and result

Source: lane base `85d57a818c3707397e21c840b6498b105ba798aa`; frozen control ` .ufo/waves/round-52/controls/c1-do-nothing.md` (two repeated rows). No new C1 counter exists in the pinned tree; only `quality/counters/c1-r51-ledger.py` is present, consistent with registration's “new counter absent” statement. I did not run a package query, producer, host/live probe, or mutate the source checkout.

Command (read-only parser probe):

```sh
python3 -I -c 'import importlib.util,pathlib; p=pathlib.Path("/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r51-ledger.py"); s=importlib.util.spec_from_file_location("c1",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); t=pathlib.Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/controls/c1-do-nothing.md").read_text(); rows=m.parse_rows(t); print("rows",len(rows)); [print("path=%r desc=%r pointers=%r"%(r["path"],r["desc"],m.pointer_tokens(r["pointer"]))) for r in rows]'
```

Actual output:

```text
rows 2
path='tools/mado-verify.sh' desc='quality/tool-ledger.md (commentary only)' pointers=[]
path='tools/mado-verify.sh' desc='quality/tool-ledger.md (commentary only)' pointers=[]
```

Control source is `.ufo/waves/round-52/controls/c1-do-nothing.md:1-4`. Counter source: `quality/counters/c1-r51-ledger.py:155-174` parses both duplicates; `:196-208` accepts any resolvable pointer-file containing the basename; `:229-236` only rejects empty/punctuation descriptions; `:415-418` separately rejects duplicates, uncovered rows and other structural failures. Base receipt `.ufo/waves/round-52/receipts/c1-base.txt:1-4` records 82/82 and `TARGET_MET` for the production ledger.

## Verdict and limits

Reproduced: **yes**, the old parser produces the two identical rows and no pointer tokens. The exact self-pointer/context detector outcome is **not tested**: the frozen new detector is absent at base, and this control is too sparse/duplicate-heavy to attribute a fail to those two clauses under the old counter. I therefore make no claim that the planned round-52 counter survives or fails this attack. This is a control validity/diagnostic-power finding; the fresh counter still needs a clean control receipt that shows the self-pointer/context checks themselves cause rejection while other frozen structural checks remain valid.

Scratch directory created: `/fast/scratch/hyaku/mado-r52/Falsify33/`; no fixture files or clones were created, and no install was needed. No temporary evidence remains to clean.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify33.md`

Report: `.ufo/waves/round-52/w1/Falsify33.md`
