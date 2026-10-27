# Falsify03 — C1 no-work control validity

## Finding

**Attacked item/predicate:** C1's frozen control clause: the new counter must fail `controls/c1-do-nothing.md` specifically for self-pointer/context defects, while passing production at base `85d57a818c3707397e21c840b6498b105ba798aa`.

**Concrete validity failure reproduced: the named control is absent from the frozen revision.** The lane is at the requested base. `git ls-tree -r --name-only <base> -- controls receipts quality/counters/c1-r51-ledger.py quality/tool-ledger.md .ufo/waves/round-52` returned only:

```
quality/counters/c1-r51-ledger.py
quality/tool-ledger.md
```

Thus neither `controls/c1-do-nothing.md` nor the referenced `receipts/c1-base.txt` is present in the base tree, and no round-52 path was present in that tree. A new counter tested against that relative path at the frozen revision cannot observe the described fixture unless it is supplied outside the revision; if supplied externally, this base-tree probe does not establish that it is the registered committed control. The frozen control's intended repeated-generic-self-pointer shape therefore cannot be independently reproduced from the specified base bytes.

## Reproducible setup / command / actual result

Setup: read-only lane checkout `/home/vgpnk/Projects/shokunin/mado-shokunin`; `git rev-parse HEAD` returned `85d57a818c3707397e21c840b6498b105ba798aa`. Disk guard `df -h /fast/scratch` returned 600G available. No scratch fixture was needed; no source checkout writes or counter/producer execution occurred.

Command:

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-tree -r --name-only 85d57a818c3707397e21c840b6498b105ba798aa -- controls receipts quality/counters/c1-r51-ledger.py quality/tool-ledger.md .ufo/waves/round-52 | sort
```

Actual result: the two paths above. `controls/` does not exist at the lane root in the checked-out tree (`glob` returned `Path not found: mado-shokunin/controls`). The registered path is therefore not a base-committed control at the claimed revision.

**Reproduced: yes** — the discrepancy between the frozen registration's assertion and the base tree was reproduced with read-only tree inspection. This does not test whether a later-created control has the claimed row defects or whether a future counter detects them; it falsifies only the control's stated availability at the frozen revision.

## Evidence and limits

- `claims-frozen.md`, C1: “Demonstrate production pass and control fail at the frozen revision”; target control described as repeated generic self-pointers.
- `registration.md`, “Frozen controls”: “C1 do-nothing control `controls/c1-do-nothing.md` is the committed ledger shape...” and the base receipt named `receipts/c1-base.txt`.
- Base tree command result above.
- `SKILL.md:39-45` confirms the source-only restriction; no package queries, live reads, screenshots, or producer execution were performed.
- No external source candidate was used; no URL or web access applies.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify03.md` — this bounded control-validity finding.

Report: `.ufo/waves/round-52/w1/Falsify03.md`
