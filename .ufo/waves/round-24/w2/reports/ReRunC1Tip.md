# ReRunC1Tip — re-run of frozen C1 counter at tip and base (wave 2, falsification seat)

Seat: MadoR24.ReRunC1Tip, 2026-10-23. Assignment: re-run the frozen C1 counter in counted
(re-fetch) mode at tip `39c5963` and base `8e5d9369`, compare with the wave-1 receipt, verify
counter bytes and history, verdict on TARGET_MET. Leaf seat; no writes to the lane except this
report. No tools installed (nothing needed).

## What was run (commands and outputs)

All runs from the lane with `python3 -I` (isolated), wrapped in `timeout 900`, counted mode
(no `--offline`), so every claim-row URL was re-fetched live from raw.githubusercontent.com.

### 1. Tip `39c596307333b8ca0a1e42b3f3b9a748bb8b208b` — counted (re-fetch)

```
A1 S153 PASS_ROW   A9  S157 PASS_ROW   A17 S163 PASS_ROW
A2 S154 PASS_ROW   A10 S158 PASS_ROW   A18 S164 PASS_ROW
A3 S155 PASS_ROW   A11 S158 PASS_ROW   A19 S165 PASS_ROW
A4 S155 PASS_ROW   A12 S159 PASS_ROW   A20 S165 PASS_ROW
A5 S155 FAIL_ROW quote-off-topic
A6 S155 PASS_ROW   A13 S160 PASS_ROW   A21 S165 PASS_ROW
A7 S156 FAIL_ROW quote-off-topic
A8 S156 FAIL_ROW quote-off-topic
                   A14 S160 PASS_ROW   A22 S165 PASS_ROW
                   A15 S162 PASS_ROW   A23 S166 PASS_ROW
                   A16 S162 PASS_ROW   A24 S167 PASS_ROW
                                       A25 S168 PASS_ROW
                                       A26 S168 PASS_ROW
counter_version=v2 revision=39c5963… mode=refetch note_present=True rows=26
PASS_ROW=23 distinct_sources=14 readme_indexed=True verdict=TARGET_MET
counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
exit=0
```

### 2. Base `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` — counted (re-fetch)

```
counter_version=v2 revision=8e5d9369… mode=refetch note_present=False rows=0
PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET
counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
exit=1
```

Matches the registered before-value in registration.md ("Before at base: PASS_ROW=0, note
absent, exit 1") and the do-nothing control receipt (PASS_ROW 0).

### 3. Comparison with `.ufo/waves/round-24/evidence/c1-after-cf86f9e0.txt`

Identical per-row labels and `why` codes (A5/A7/A8 `quote-off-topic`, all others PASS_ROW);
identical summary except the `revision` field (cf86f9e0 vs 39c5963): PASS_ROW=23,
distinct_sources=14, readme_indexed=True, verdict=TARGET_MET, same counter_sha256. Only one
commit exists between cf86f9e0 and tip (`39c5963` — QUALITY 33-35, carry population, wave-1
reports/receipts); it does not touch the counter and does not move the counted value.

### 4. Counter bytes and history

- `git show 39c5963:.ufo/waves/round-24/c1/count.py | sha256sum` =
  `b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66` — equals the required
  v2 prefix `b2f37c57…`, the receipt's `counter_sha256`, and the working-tree file
  (`sha256sum` on the file: same; `git status --porcelain` on the path: clean).
- `git log c9b76646..39c5963 -- .ufo/waves/round-24/c1/count.py` is empty: no commit after
  c9b76646 changed count.py. Full history: 8efd00af (v1 landing) → d9fec1d3 (lane-path
  override) → c9b76646 (v2 claim-anchor clause); `git merge-base --is-ancestor c9b76646
  39c5963` OK.

### 5. Source check of the frozen counter (full 177 lines read)

The code implements the registered v2 predicate: 11-cell SOURCES row with `status=mined`
(cell 8), `opened=2026-10-23` (cell 9), used-by naming the note (cell 11), pinned URL
(`PIN_RE`: 40-hex or vX.Y tag) under github.com / raw.githubusercontent.com /hyprwm/Hyprland
or hyprland-wiki, live re-fetch (User-Agent `mado-r24-c1-counter`, urlopen timeout 60) whose
sha256 must equal the recorded value, quote ≤25 words containing a rule-topic word occurring
verbatim (whitespace-collapsed) in the fetched bytes, claim ≥8 words anchored by the v2
clause (≥4 consecutive quote words, or a backticked ≥4-char identifier from the quote), and
a duplicate-quote guard. TARGET = PASS_ROW ≥ 6 from ≥ 3 distinct S### plus a
`corpus/README.md` coverage-map row `| \`knowledge/rule-attribution-r24.md\``. Mode is
`refetch` unless `--offline` (diagnostic only). Matches registration.md; v2 text identical.

## Verdict

VERDICT: holds — TARGET_MET at the landed tip 39c5963 is reproducible with the frozen v2
counter: PASS_ROW=23 (target ≥ 6) from 14 distinct sources (target ≥ 3), README-indexed,
exit 0, re-fetch mode; base stays PASS_ROW=0/exit 1; counter bytes are v2
b2f37c57… and unchanged since c9b76646.

## Residual risk / verification gaps

- Counter-level verdict only. Per registration's own v2 limit, the counter cannot judge
  whether a claim is *supported* by its source; row-level truth was assigned to the
  ReopenS### seats (in flight, separate). A5/A7/A8 already fail `quote-off-topic` and are
  correctly excluded.
- The counted value depends on live remote bytes matching recorded sha256; upstream edits or
  force-pushes at the pinned tags/commits could flip rows to `sha256-mismatch` on any future
  re-run. Today: all 14 fetched sources matched.
- `TOPIC_RE` includes the generic token `rules?`, so the topic test is weak by design;
  mitigated by the v2 anchor clause and the control results (off-topic and label-shortcut
  controls score 0 under v2).
- Fetches ran once per (URL, S###) per invocation via an in-process cache; no fetch
  counter-variation was tested beyond the two invocations performed.
