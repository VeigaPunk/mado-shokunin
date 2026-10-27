# Falsify15 — C2 held-ground novelty

## Attacked frozen clause

C2's requirement for a **distinct new indexed entry on a distinct Hyprland dispatcher-execution mechanism**, with every material proposition mapped to a source row/pin/quote and rationale. The structural counter requirement (proposition count, row/pin/quote bindings, complete mapping) does not itself specify a cross-entry novelty test. Attack: a newly named entry that remaps/copied propositions already present in the round-51 dispatcher-execution entry can satisfy those structural conditions while adding no distinct mechanism. This is a coverage/novelty bypass, not a claim that a future counter does so.

## Grounding and reproducible setup

Read-only local sources; no package/live probes or producer execution.

- Frozen predicate: `.ufo/waves/round-52/claims-frozen.md` (C2); its structural checks are enumerated in `.ufo/waves/round-52/registration.md` (C2).
- Existing indexed entry: `corpus/README.md:78` indexes `hyprland-dispatcher-dispatch-r51.md` as Hyprland dispatcher execution.
- Existing entry, `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:3-8,70-84,88-243`: already covers stored dispatcher name/argument, press-time map dispatch, `submap`/`pass`, socket entry to the table, and what the evidence licenses. Its source rows S364-S369 and held sources are listed at lines 14-24. This supplies a concrete prior mechanism/claim set against which an alleged distinct entry can be compared.

Reproduce the attack surface by opening those files and comparing a proposed C2 draft's mechanism and propositions against the cited R51 sections. At inspection time the assigned `w1/C2EntryDraft/` directory was empty, and `w1/C2CounterDraft/` did not exist; thus no round-52 candidate draft/counter was available to run or mutate. The registration explicitly says the new counter is absent at base and the frozen C2 target entry is absent. No candidate existed to establish a pristine detector output, make a one-point mutation, rerun the same detector on mutated/restored bytes, or report hashes; I therefore did not manufacture a detector or run an unrelated runtime.

## Result

- **Concrete bypass mode:** duplicate/relabel R51's already indexed execution mechanism and its source-grounded propositions as the purported new entry. Row/pin/quote binding and proposition count can all be valid while novelty is false; the specified structural counter fields alone do not compare semantic mechanism/proposition overlap with prior entries.
- **Actual result / reproduced:** **No** — not reproduced against an implementation. The failure mode is identified from the frozen predicate and locally present R51 corpus; there is no round-52 counter/candidate at the inspected paths to demonstrate a false positive. This is an untested counter-coverage risk, not evidence that a particular implementation accepts it.
- **Limit:** no fresh external source candidate was opened; this attack is strictly about held-ground novelty against already admitted local corpus material. No git/jj mutation, tracked edit, package query, live read, source fetch, or runtime execution.
- **Tooling:** none installed.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify15.md`

Report: `.ufo/waves/round-52/w1/Falsify15.md`
