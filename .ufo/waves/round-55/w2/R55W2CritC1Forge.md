# R55W2CritC1Forge — report (wave w2, falsify; target PRED-C1-r55)

Full evidence: `.ufo/waves/round-55/w2/R55W2CritC1Forge/forge.md`; receipts in `.ufo/waves/round-55/w2/R55W2CritC1Forge/receipts/` (driver `forge.py`, per-variant `counter.out`/`harness.out`, `diffs/*.diff`, `summary.json`, `lane-baseline-57584ed.txt`).

## What ran

- Scored rev `57584ed67716340b3d466fa04333ac0bab3fb79e`. The lane's HEAD is now `721ba9c…`; `git diff --name-only 57584ed HEAD -- quality corpus tools .ufo/waves/round-55/fetch` is empty, so the scored content is what HEAD carries for those paths.
- Baseline on the lane (read-only, git objects only): counter `TARGET_MET rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3`, rc 0; harness `good=ok controls=7/7 verdict=OK`, rc 0.
- Six forged trees in scratch (`git archive` export → scratch repo → one edit to the entry → one commit per variant), each scored with the real counter (`python3 -I`) and the real harness (`python3 -I quality/check-r55-controls.py --claim c1`). The counter and harness blobs are byte-identical to the scored rev in every variant. Only the entry file differs.
- Mutations were applied to scratch COPIES. Nothing in the lane was modified, restored or committed.
- Tools installed or upgraded: none. No pacman, no network, no hyprctl.

## Results

| variant | counter | harness | human reviewer |
|---|---|---|---|
| J1 junk: frozen quotes, anchors, real S-ids, placeholder 40+ char propositions, provenance trio, no prose | TARGET_MET | 7/7 OK | reject |
| B1 K04 proposition says "capped at 200"; pin line 1282 is `std::max(0, REPEATRATE);` | TARGET_MET | 7/7 OK | reject |
| B2 all 18 K and 6 H propositions contradict their quotes | TARGET_MET | 7/7 OK | reject |
| C1 K13–K15 cite S215 (log-switch row) and K16 cites S162 (windowrule row) instead of S318/S317, same file family | TARGET_MET | 7/7 OK | reject |
| P1 provenance `source: S999` (no such registry id), rows honest | TARGET_MET | 7/7 OK | reject |
| control: entry absent | TARGET_MISSED `entry_absent` | good=bad 0/7 | n/a |

Decisive line, J1: `MADO_KBD_ENTRY: rev=8ff1bec293c467d01a987bd9c19c4dad23202408 rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none`, with `MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK`.

Every variant keeps the frozen grammar, so none is a syntactic rejection. Each pass is a valid row with a false or empty claim, or a citation the counter does not check.

## Verdicts per target

- **PRED-C1-r55 as a sourced-entry predicate: BROKEN.** J1 is a do-nothing-equivalent (it adds no claim beyond the frozen quotes) and meets the target. Under the round's §9 test ("predicate wrong" if a do-nothing-equivalent meets the target), this is the predicate-wrong outcome. The counter's stated job, quote identity at an exact pin line with row, source and host binding, is what SURVIVES.
- **Counter source-binding leg: BROKEN for same-family swaps.** `source_ok` checks status, URL suffix and commit only. It does not read the registry's scope or anchor cells, so S215 (log-switch defaults at ConfigValues.cpp:629/632) passes for a K13 that cites line 279. Cross-family swaps are still caught (harness CTL-4, `source_cell:K10`).
- **Provenance leg: BROKEN.** It accepts any `S###` token on a `source:` line, so `S999` passes.
- **Proposition content: not checked by any leg.** The only check is length ≥40 (K) and ≥20 (H). B1 and B2 pass unchanged, which is the declared limit (QUALITY 104/105) made concrete.
- **Harness (7 controls): SURVIVES for its own scope, BROKEN as content evidence.** It is 7/7 on J1, B1, B2, C1 and P1 because all its controls are mutations of the honest tree. The harness cannot see propositions.
- **Registered do-nothing control (entry absent): SURVIVES.** It scores TARGET_MISSED with `entry_absent`, and the harness scores it good=bad 0/7. The control does not meet the target, but it is not the right do-nothing: J1 is.
- **v2 errata (registration-v2.md E1–E9): no content check added, so the picture does not change; the target becomes reachable.** E1–E9 change quotes, the `source_cell` URL rule, host lookup, counts, control legs and the hold-out commitment. None adds a proposition check. The v2 text itself records that a junk entry reaches TARGET_MET, and this run confirms it. The v1 claim that no entry could pass (`||` in K16, K17's URL) is UNVERIFIED by run: the counter embeds the v2 sha, and running v1 would need an edited instrument. The text of registration-v2 is the only evidence for it.

## What a human reviewer would reject, and why the counter does not

All five forged variants pass the counter and the harness. A reviewer rejects J1 (no content), B1 and B2 (propositions contradict the pin lines they cite), C1 (registry rows cite a different subject: S215 is a log-switch row, S162 a windowrule row) and P1 (`S999` is not a registry id). None of these is caught by any leg. The honest entry's propositions are not tested by this counter either. That is the sentence-to-pin audit, which this seat did not run.

## Declared limits for the L1

1. The registration's declared limit ("entailment is the w2 audit, reported not counted") is the only thing standing between J1 and a TARGET_MET claim. Count the counter's TARGET_MET as quote identity only, not as a sourced entry.
2. Adding a registry-scope check (the cited line range must fall inside the registry row's scope or anchor) would catch C1; it needs a new frozen predicate, not an edit of this one.
3. Provenance needs a registry-membership check on `source:` ids to catch P1.

## Not verified

- v1 counter behaviour (see above).
- Whether the honest entry's propositions are entailed by their quotes (sentence-to-pin audit, not this seat).
- Anything on the running host. Only the lane's git objects and the counter's own output were read.

## Cleanup

Scratch `/fast/scratch/hyaku/mado-r55/R55W2CritC1Forge/` is removed before yield (receipts were copied first). The lane has only my two deliverable files and the receipts directory added as untracked paths.
