# Held-row reuse control (round 52, attack fixture)

No source was opened this round. The four propositions cite two pre-existing registry rows
(S364, S365) whose bytes were pinned in round 51 and whose `used-by` cell was amended to name
this file. Pin names, line anchors and quotes are deliberately non-existent: the point of the
control is what the committed counter does and does not read.

source: S364, S365
verified-at: 2026-10-27

| ID | Source row | Proposition | Pin | Anchor | Quote | Why it supports |
|---|---|---|---|---|---|---|
| P01 | S364 | The dispatcher table forwards every name to one legacy translator call. | No-Such-Pin-A.cpp:1 | no such anchor | this sentence appears in no pinned file | The rationale is prose and nothing checks the pin. |
| P02 | S364 | The press path calls the stored handler with the stored argument. | No-Such-Pin-B.cpp:2 | no such anchor | neither does this sentence appear anywhere | The rationale is prose and nothing checks the quote. |
| P03 | S365 | A missing dispatcher name is refused by the translator entry point. | No-Such-Pin-C.cpp:3 | no such anchor | a fabricated quote with five words | The rationale is prose and nothing checks the anchor. |
| P04 | S365 | The translator's implementation map holds seventy-one entries. | No-Such-Pin-D.cpp:4 | no such anchor | another fabricated quote of six words | The rationale is prose and nothing checks the row scope. |
