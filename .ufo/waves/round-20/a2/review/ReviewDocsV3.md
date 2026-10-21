# ReviewDocsV3 — partly falsified: one recall count overstates execution certainty; two references need revision or path qualification

## Findings

### F1 — MEDIUM: `w2-dispositions.md:15` calls all 51 misses real executions

The row says “51 real-execution shapes silently missed.” The cited `AdvRecallShapes` report distinguishes 51 **raw** predecessor-only misses from the subset established as real execution: 49 certain regressions, one signal-contingent case (`ar49`), and `gap04`, an intentional old false-positive correction (`.ufo/waves/round-20/w2/reports/AdvRecallShapes.md:68-71`). So “51 real-execution” overstates the evidence by two cases.

- **Reproducing command** (from the lane root; all inputs are transcript data passed only to `--scan`):
  ```sh
  T=../../../../../tmp/mado-r20a2-ReviewDocsV3/recall
  python3 -I "$T/tw-1f7f995.py" --scan "$T/gap04-lambda-argv-lead.jsonl"
  python3 -I "$T/tw-9c54c56.py" --scan "$T/gap04-lambda-argv-lead.jsonl"
  python3 -I "$T/tw-28c6837.py" --scan "$T/gap04-lambda-argv-lead.jsonl"
  python3 -I "$T/../tools/mado-tripwire.py" --scan "$T/gap04-lambda-argv-lead.jsonl"
  python3 -I "$T/tw-1f7f995.py" --scan "$T/ar49-signal-handler-lambda.jsonl"
  python3 -I "$T/tw-9c54c56.py" --scan "$T/ar49-signal-handler-lambda.jsonl"
  python3 -I "$T/tw-28c6837.py" --scan "$T/ar49-signal-handler-lambda.jsonl"
  python3 -I "$T/../tools/mado-tripwire.py" --scan "$T/ar49-signal-handler-lambda.jsonl"
  ```
- **Inputs (pinned fixture bytes, SHA-256):** `.ufo/waves/round-20/w2/AdvRecallShapes/fixtures/gap04-lambda-argv-lead.jsonl` — `b8b218508567d048a2f2f0fb880d2f67687ed3349fcccf300aa0687d07032c03`; `.../ar49-signal-handler-lambda.jsonl` — `e9014d2d40e76f58e1e3ac2a6f6eb1a2757a8eaba599ecb15f93970ff16e1227` (both read from fixture revision `6a7d9ca0d2124a4077074b800c94a9bc1184441c`).
- **Observed vs expected:** `gap04` is a finding only at `1f7f995`; it is clean at `9c54c56`, `28c6837`, and `a8960de`. `ar49` is a finding at `1f7f995`/`9c54c56`, clean at `28c6837`, and a `lead` at `a8960de`. The report’s expected characterization is therefore 49 certain regressions + 1 contingent + 1 intentional old-FP correction, not 51 certain real executions.
- **Revisions compared:** `1f7f995` and `9c54c56` versus `28c6837`, with the final behavior checked at `a8960de` (tool SHA-256 `a57d4fe9277ff06c9b5916fc731e91f05bcd69cf05639cb2090ebcb00b5b6458`).
- **Fix:** change the headline to “51 raw predecessor-only misses: 49 certain execution regressions, one signal-contingent case, and one intentional old false-positive correction.”

### F2 — MEDIUM: `w2-dispositions.md:38` leaves the `measure.py` revision unstated

“`measure.py` rejected=[] at tip” is true for the current lane HEAD (`451c7e41f278e55e85347f91246dd32ad86c346e`), but not for the task’s required `a8960de` snapshot. The `measure.py` counter is revision-bound and reads committed bytes, so the unqualified “tip” makes this a stale/ambiguous result for the attempt-2 baseline.

- **Reproducing commands** (from the lane root):
  ```sh
  python3 -I ../../../../../tmp/mado-r20a2-ReviewDocsV3/.ufo/waves/round-17/measure.py a8960de
  python3 -I .ufo/waves/round-17/measure.py 451c7e41f278e55e85347f91246dd32ad86c346e
  ```
- **Input (revision-bound source bytes, not a transcript fixture):** `corpus/knowledge/tripwire-precision-r20.md@a8960de`, SHA-256 `199002895c14733a2da8b9da0c828f953ca66402dc4da564e21ab6b61a2058bf`; current `451c7e41` bytes, SHA-256 `38685fb989e4792cbea167f796b1c9c0edd47e05ef5100c90c8b1296aca567b7`.
- **Observed vs expected:** `measure.py a8960de` returns `rejected=[{"path":"corpus/knowledge/tripwire-precision-r20.md","declared":["MALFORMED"],"reason":"surface line must be exactly `surface: P<n>`"}]`; the committed `a8960de` note still has the old `surface: lane tooling` head. The second command at `451c7e41` returns `rejected=[]` after the note changed to `scope:`. Thus the empty list is accurate at the later revision, not at `a8960de`.
- **Revisions compared:** `a8960de` vs current docs HEAD `451c7e41`.
- **Fix:** pin the revision in this row. If it reports `a8960de`, record its rejection; if it means the later documentation tip, name `451c7e41` and retain that run’s receipt.

### F3 — LOW: `corpus/lessons/round-20.md:28` has a non-resolving lane-relative pointer

M14 cites `.ufo/watchdog.log:548`. That file is absent from the lane repository; the matching watchdog record is one directory above the lane, at `../.ufo/watchdog.log:548`. The event itself is present, but the citation does not resolve when read relative to the lane.

- **Reproducing command** (from the lane root):
  ```sh
  git -C ../../../../../tmp/mado-r20a2-ReviewDocsV3 cat-file -e a8960de:.ufo/watchdog.log
  ```
- **Input:** `../.ufo/watchdog.log`, SHA-256 `51ebf7221e4fdaf1d131db3384c25cff0fa69b6097a3f602991f34651083fbb5`; line 548 contains `lane-dead-no-report mado round=20`.
- **Observed vs expected:** the command reports the lane-local path absent; the parent-level file contains the cited event. Expected is a pointer that resolves from the lane root.
- **Revision compared:** lane `a8960de`; the watchdog log is the fleet-level file outside the lane.
- **Fix:** cite `../.ufo/watchdog.log:548` explicitly, or retain a lane-local evidence copy and point to it.

## Limits

- The required source census passed: `../scripts/sources-census.sh validate --root .. mado` returned `mado ok`, with W04 duplicate-URL warnings for S030, S042, S045, and S097. S113–S115 were fetched from their pinned CPython 3.14.8 URLs; byte hashes/sizes, quoted line spans, and word counts (10/12/10) matched the current `SOURCES.md` rows.
- Re-ran the precision/held-out, recall/split, attempt-2 guard, calibration, tally, and harm-watch commands at `a8960de`; the current attempt-2 guard returned `recall_lost=0`, `crash_flip=0`, `pure_rows=0`, `vcs_fn=0`, `vcs_fp=20`, and `a2_mismatch=0`. Harm watch passed. The `isolation-check.sh isolate.sh` run passed all six fail-closed modes plus its positive control. A v3/v3.1 scan of the exact W3 transcript confirmed M15’s additional `git:checkout/unparsed` row at v3.1.
- No other stale `3610e3e`-only final-state claim or actionable false sentence was found in the reviewed sections. LSP was unavailable (`read xd://lsp` returned “No such tool”); grep was used only to locate literal text, not as semantic proof. No package queries, host probes, builds, linters, or installations were run.

## Installs

none
