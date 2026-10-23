# AtkReadmeFrontier — round-24 README attack report

**Attacked item:** the round-24 changes to `corpus/README.md` between base `8e5d9369` and tip `39c596307333b8ca0a1e42b3f3b9a748bb8b208b` (index row accuracy; round-24 frontier bullet; round-23 withdrawal pointer for routed defect 2; sha256 label convention).

**Method:** `git diff 8e5d9369 39c59630 -- corpus/README.md`; direct re-reads of the note, SOURCES rows, lesson 23, SCORECARD, round-23 registration and spotcheck §7; direct sha256 computation via `git show REV:path | sha256sum` at base / round-23 tip `fa819d56` / current tip; C1 after receipt read.

## Findings

### Low — no factual error, wording precision only
1. **"The input ladder … as listed above" (frontier bullet, tip README ~:204-205).** The bullet lists "output management, the input ladder and Waybar module text" as still open, pointing at the round-12 bullet list. Round 15's bullet explicitly superseded "the older 'input ladder open' wording for that bounded documentary subset" (U6 documented layer route moved); only input-debugging *delivery* remains open. The pointer is tied to the historical round-12 list and the round-15 qualifier remains in the same section, so the statement is not false — but the strictly current phrasing would be "input-debugging delivery" (and "output management" / "Waybar module text" remain open per rounds 14/16). Suggested tightening only.

## Verified holds (no defects found)

### Index row accuracy (`corpus/README.md:47`, tip)
- Source range claim **S153–S160, S162–S168 (S161 queued)** is exact: SOURCES rows S153–S160 and S162–S168 are all `mined`, opened `2026-10-23`, `recheck: on-release`, used-by `corpus/knowledge/rule-attribution-r24.md`; S161 is `queued` with used-by `—` (SOURCES.md:165-180).
- Fetched-bytes claim verified: `.ufo/waves/round-24/fetch/S153.bin`–`S168.bin` all exist (16 files).
- Pins `efb50993` / `c66e8de2` match the note header and every S153–S168 row URL (`efb50993780079460b0cbed1363e2166a2de1d9f`, `c66e8de21f5ecdc4bc5e278e7d94800ea10957af`).
- Content summary matches the note: no attribution channel ("hyprctl, Lua, socket2, logs, window object, plugin bus swept" = note's Negative sweeps list); tag route via `hyprctl clients` (A10/A22); named-rule handle toggle operator-only (A12–A14/A23 + "operator only, never a mado probe"); host behaviour `[UNK]` (note Limits). "recheck on-release" matches the note's frontmatter.

### Round-24 frontier bullet (`corpus/README.md:198-205`, tip)
- "Round 24 moves the round-12 frontier item 'Still open: rule *attribution*'" — exact wording present in the base round-12 bullet (base `corpus/README.md:101`, unchanged at tip) and echoed by the note's `covers:` line.
- "Onto documentary sourced ground" is counter-backed: C1 after receipt `evidence/c1-after-cf86f9e0.txt` reports `PASS_ROW=23/26`, `readme_indexed=True`, `verdict=TARGET_MET` (v2, counted).
- Answer text ("no upstream channel maps an applied property back to the rule that set it; the usable route is a unique `tag` effect read from `hyprctl clients`") matches the note's Answer and table.
- Still-open items match the note: "observed attribution on this host (no rule was toggled and no tag value read)" = note Host join + Limits; "plugin-side match recording" = note Limits (`[INFERENCE]`, none installed).

### Round-23 withdrawal pointer (routed defect 2 of spotcheck §7)
- **sha256 labels present and correct:** both digests are given as `sha256:`-labelled prefixes and both match direct recomputation:
  - `tools/mado-tripwire.py` at base `8e5d9369`, round-23 tip `fa819d56` and tip `39c59630` are byte-identical: sha256 `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84` → `cd9da20c2f562efb…` ✓
  - candidate evidence file `.ufo/waves/round-23/evidence/candidate-classifier-e1dc8029.py` (exists) sha256 `e1dc8029ced9fcc62d458b8143209605f34b60c9e4cfe6d8f66515c2efce4a47` → `e1dc8029ced9fcc6…` ✓
- "withdrawn before landing closed" / "byte-identical to base" matches lesson 23 "Final C1 disposition: withdrawn to base bytes (honest stop)" (`corpus/lessons/round-23.md:212-229`).
- "C1 ended 6/12 against its 12/12 target" matches lesson 23 ("C1's registered target is therefore not met at the landed tip (6/12)"), SCORECARD round-23 final C1 disposition ("**C1 after-value at the landed tip: 6/12 — target 12/12 not met (honest stop).**", SCORECARD.md:1550-1557), and round-23 registration (target after 12/12, before 6/12).
- Routing matches spotcheck §7 defect 2 verbatim ("README round-23 bullet … does not say the repair was withdrawn to base bytes. Append the withdrawal pointer."). The original bullet is retained and the pointer appended, as registration dictates.

### Diff hygiene
- The diff touches only the three intended areas: one new coverage-map row, the appended withdrawal bullet, the new `### Round-24 rule attribution route` section. No other README content changed.

## Verdict

`VERDICT: holds`

No false statement, misattribution, stale count or unlabelled sha256 found in the reviewed README changes. One low-severity wording nuance (input-ladder phrasing) noted above; it does not falsify the bullet.

## Residual risk / verification gaps
- I did not re-run the C1/C2 counters (counted C1 refetches the network; C2 counter is single-run per hard bounds). I relied on the committed C1 receipt `c1-after-cf86f9e0.txt` and the running AtkC1Coverage counted-mode seat; the receipt self-reports `TARGET_MET` with `readme_indexed=True`.
- Claim-row semantic validity inside the note (quote supports claim) is out of my scope; per registration, wave-2 reviewers re-read each claim row against its bytes.
- No tools installed/updated this run.
