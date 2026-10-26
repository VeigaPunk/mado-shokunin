# ExecRerunC2 — C2 data-tip attack (PRED-C2-r41-v2, admitted=1/1)

Seat: `ExecRerunC2` (w2, leaf). Fu ll report: `.ufo/waves/round-41/w2/ExecRerunC2/report.md`.

## Baseline (committed bytes, lane repo)

- `python3 -I quality/counters/c2-r41-focus-entry-v2.py --repo . --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1` →
  `PRED-C2-r41-v2: admitted=1/1 verdict=TARGET_MET rev=07f264…` rc 0.
- `python3 -I quality/counters/c2-r41-focus-entry.py --repo . --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1` →
  `PRED-C2-r41-v1: admitted=1/1 verdict=TARGET_MET rev=07f264…` rc 0.

The data-tip claim reproduces exactly as registered.

## Mutation battery (30 single-purpose edits on committed data, scratch clone, frozen v2 counter)

24/30 rejected by the clause that names the edited property (drop/indent/outside gate,
census number/fence/dup, invalid recheck, used-by drop, README row delete, ghost id,
verified-at below 20, receipt byte flip, location dot loss, opened/kind/dup row changes,
REFUSE/ADMIT violations, held-row edit, row-body swap, non-receipt quote, BOOT removal,
extra source below window). Six admitted:

| edit | admitted | finding |
|---|---|---|
| S283 quote "whitelist of surfaces" -> "whitelist of surface" (entry:19 + lesson:25) | **1/1** | F1 — clause d quote check is substring-based (`c2-r41-focus-entry-v2.py:378`); a quote can end inside a word ("surface" ⊂ "surfaces") and still pass, so the entry can claim a quote the receipt does not literally contain. Open predicate defect. |
| swapped S283/S284 header source captions (entry:3-4) | **1/1** | F2 — captions are unbound from ids; two ids can trade their source descriptions unseen. Open predicate defect. |
| GATE S287 quote re-pointed to "fixed in b09f157" (lesson:29 only) | **1/1** | F3 — gate quote binds receipt<->entry-line, not quote<->claim; declared residual demonstrated with a one-line edit. |
| entry recheck `90d` -> `1999-01-01` (entry:12) | **1/1** | F4 — any calendar-valid date passes; no sanity bound. Minor. |
| ghost GATE inside a fence in the Gate section | **1/1** | O1 — fences invisible by design; non-cited id GATEs in-section unchecked. |

## Verdict

Data tip confirmed: `admitted=1/1 TARGET_MET` at `07f2641…`. The landed data passes every
clause; no finding corresponds to a data defect. F1-F4 are open predicate defects (no
third registration per round rules); F1 (mid-word quote truncation) is the strongest.
Scratch cleaned; no lane file touched; no tools installed.
