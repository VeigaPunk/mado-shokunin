# LogDraft — round-19 LOG entry skeleton drafted; before values from receipts, after values left as placeholders

Wrote only `.ufo/waves/round-19/drafts/LogDraft.md` (round-18 entry style: heading, Trigger, Cn paragraphs, Waves, Harm watch, closing "Admission not asserted."). No git or jj write; no host-package, service, compositor or live-gate command; host files read as bytes only.

## Verified inputs (commands run, observed output)

- `git cat-file -t 9c54c56` → commit; `git cat-file -t 17661e0` → commit; `17661e0` subject `round-19: pre-registration (claims C1-C3, sub-axis rubrics, baselines, counters)`.
- `sha256sum .ufo/waves/round-19/fresh-pins.py` → `a094be01…` (matches receipt `tool_sha256`); `.ufo/waves/round-19/tw-recall.py` → `22090298…` (matches receipt); `.ufo/waves/round-17/measure.py` → `de4c422b…` (matches receipt).
- `sed -n 2929p /var/log/pacman.log` → `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`. Confirms R18-V3's host pointer.
- `.ufo/waves/round-19/evidence/measure-before.json.txt`: c1 18/26 score 6.9231; c2 count 6 score 10.0, u_routes 7; c3 tool sha `c1ae45a7…`.
- `.ufo/waves/round-19/evidence/fresh-pins-before.txt`: denominator 13, current 2, score 1.5385 (current: `corpus/README.md` line 44, `corpus/knowledge/walker-route-r18.md` line 1).
- `.ufo/waves/round-19/evidence/tw-recall-before.txt`: incident_lines 6, detected 3, score 5.0.
- `.ufo/waves/round-19/evidence/census-before.txt`: exit 0; S030, S042, S045 historical W04 duplicates.
- `LOG.md` tail: round-18 entry at line 1287, format `## 2026-10-20 — round 18: …` with Trigger / Cn / Waves / Harm watch paragraphs; ends "Admission not asserted."
- `SCORECARD.md` tail (declared claims): C1 target ≥21/29; C2 target 13/13; C3 target 6/6. Reserved rows S096–S098 with S099–S105 L1-assigned.
- Draft sha256: `.ufo/waves/round-19/drafts/LogDraft.md` → `06b660a5…` (5,397 bytes at write time).
- Drafts sha256: `TwInstallerChannels.patch` `1acb8549…`, `TwMissBashCVar.patch` `6911e949…`, `TwMissHelperFn.patch` `6cf9ca69…`.
- `JjAuditMado.md` findings F6, F9, F16 (no landedness check; lane 8 commits ahead), F17 (lane colocated, jj run in it) located at the report's F-headings.

## Findings for L1

1. **Stale annotation in the before receipts.** `fresh-pins-before.txt` and `tw-recall-before.txt` both say "(tool not yet committed; pre-registration baseline)". `git show --stat 17661e0` lists `.ufo/waves/round-19/fresh-pins.py` and `tw-recall.py` as committed in the pre-registration commit, and the current file hashes match the receipts. The annotation is wrong, not the measurement. The draft does not repeat it. L1 should correct the receipts (append-only) or leave them with this note.
2. **Score scale.** The before receipts store `score` as 10 × ratio (fresh-pins 1.5385 = 2/13 × 10; tw-recall 5.0 = 3/6 × 10; c1 6.9231 = 18/26 × 10). The draft states this convention once in its header. The SCORECARD prose uses the same numbers.
3. **Criteria arithmetic.** The declared C1 target ≥21/29 implies exactly three appended criteria (27–29). If L1 adds more, the target line must change in the same entry, not silently.
4. **R18-V3 count.** "Eleven owned files" in the closure equals 13 `2.17.0` files minus the 2 already current (`corpus/README.md`, `walker-route-r18.md`). Consistent with the before receipt; no conflict.
5. **Harm-watch gap.** The before receipts measure rubric V (6/6), U (7/7) and census (exit 0) at `9c54c56`. They do not measure the gate selftest, classifier 52/52, tripwire suites, frozen 31/31, failsafe or navigation at `9c54c56`. The round-18 closure reported these at `b7148a1` (gate 389/389). The draft marks these `⟨UNK⟩` for L1 to measure or cite with their commit. I did not run them (host-pause and live-gate prohibition for this seat).
6. **Gate pin value unverified.** SCORECARD line 1103 names the gate's `live.walker.version` pin as moving with its selftest stub. I did not read the gate to confirm the pin's current value at `9c54c56`; the draft does not state one.

## Draft

`.ufo/waves/round-19/drafts/LogDraft.md` (5,397 bytes; sha256 `06b660a5…`). Placeholders: `⟨after⟩` for C1/C2/C3 after values, drafts' apply/reject outcomes, frozen-baseline digests, wave counts and dead seats, harm-watch after values, install record, and verdicts. The before values are from the receipts above; no number is invented.

## Limits

- Did not run `measure.py`, `fresh-pins.py`, `tw-recall.py`, `sources-census.sh`, the gate, or any selftest. Before values are taken from the committed receipts; I checked only the tool hashes and the pacman line.
- Did not read `corpus/lessons/round-19.md` (not yet written) or the wave reports for w1/w2 (no wave counts available to me).
- Did not check the round-18 frozen baseline `expected.json` or the tripwire fixtures.
- Did not confirm the current gate `live.walker.version` pin value.
- Did not verify the R18-V1 fetch digests (they are from the closure, re-shown there; not re-fetched; no web source opened by this seat).
- `[UNK]`: R15-V1 host state (operator-owned).

## Installs

none
