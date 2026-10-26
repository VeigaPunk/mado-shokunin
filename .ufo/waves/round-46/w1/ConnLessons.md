# ConnLessons — round-46 w1 report

Task: group the rounds 43-45 `## Mistakes` (and the three non-author spot-checks) by class; for each
class say whether round 46's freeze repeats it, with file:line. Full evidence in
`.ufo/waves/round-46/w1/ConnLessons/report.md`. Tools installed: none.

## Verdicts

**REPEATED — session material (M45-1/M45-2 class).** The freeze commits host input-device identity:
`receipts/live-devices-host-l1.txt:6-19` prints 14 verbatim device names (yubico, razer-deathadder-v2,
hp hyperx-alloy-origins-core, video-bus, power-button, …) plus their layouts/options. The standing fence
`SKILL.md:571-572` says "No … device identity … retained. Device inventory rechecks keep only counts/shape"
— a `hyprctl devices -j` dump is a device inventory. Captured-by: none — `check-session-material.py`
rules R1-R4 (docstring :30-48) cover titles/process tables/monitor serials/home listings, no device-name
rule. Spread: the same identities are embedded in the frozen fixture name pool
(`quality/counters/c1-r46-devices.py:96-99`). The registration endorses the receipt (`registration.md:16-17`).
Mitigating read: the seat-spec forbidden list is narrower than the fence; device names may be classed with
allowed window-class names. Judgment call for the L1; w1's routed privacy triage should rule on it.

**REPEATED, resolved before data — pointer to a target not committed at the cited revision (M43-3/M44-4
class).** `registration.md:30` and `:52` cite `receipts/ctl-c1.txt`/`ctl-c2.txt`; neither exists at the
freeze `8c5434c` (`git ls-tree -r --name-only 8c5434c -- .ufo/waves/round-46/receipts/` → 7 receipts, no
ctl pair). Both land one commit later at `e0be61e4` (verified ancestor: merge-base exit 0), which exists
precisely to land "controls at freeze". Same shape as M44-4; no harm because resolution preceded data.

**PARTIALLY — declared residuals as prose (M44-6 class).** `registration.md:36` re-declares r45's
residuals unmitigated (sandbox detection "by means not varied in environment B"; clause g's self-referential
oracle); `:56` re-declares the C2 reading-residuals. Fixed half: an explicit kill rule now exists
(`registration.md:27`, `:51`).

## Not repeated (evidence in the full report)

- **Locators asserted not computed (M43-1/M43-7):** ~20 entry locator ranges re-opened in the pins; all
  contain their anchors; all inside receipt line counts.
- **Counts without a recomputing command (M43-2/M44-5):** "0 of 23" (`ctl-c1.txt:25`) recomputes by grep;
  "controls=15" (`ctl-c2.txt:1`) = P + 14 enumerated; 90 fixtures / 150 generated / 28 surfaces / 10+4
  devices all re-derived from bytes; reference selftest "48/48" (`registration.md:16`) reproduced in scratch.
- **Write-time run read as committed (M43-6/M44-7):** `axis-base.txt` committed at the freeze names the base
  rev; before-receipts deterministic.
- **Vacuous gate (M43-8/M44-8/M45-3/M45-4):** C2 clause d digest-checks held ids too and clause i covers
  every PINS name; FORGED-PIN dies `d:0`; C1 clauses i/r/g hold; V01-V20 all MISS, reference MET.
- **Universal from partial set (M43-9):** the entry's "never" claims survive whole-pin greps
  (`m_scrollFactor` has exactly 2 assignment sites, InputManager.cpp:1380/:1382 — the else is nullopt);
  the census line (`entry.md:53`) recomputes exactly (47 keys, clamp 100, 2 decimals, hl-virtual-keyboard,
  us/us) and `fetch-sha256.txt` equals the counter's PINS table.
- **Stale premise (M45-5):** 20 one-semantic variants each die; contract chain verified at pins.
- **Number drift (M45-6):** before-state `tool=absent` at `seeds=46,46`; deterministic.
- **Overstated premise (M44-9), support claim broader than code (M44-3):** not present; the tool's
  no-process/no-socket docstring matches its imports (json, math, os, re, stat, struct, sys).
- **M44-1/M44-2 (refusal reason subset / row cell premise):** N/A at the freeze — no assimilation decisions
  exist yet; drafted rows' teaches cells verified consistent.
- **M43-4 (frontier step skipped):** in flight — mined mistakes is routed this round.

## Checks run (all read-only in the lane; one scratch run)

`git ls-tree`/`merge-base` at the freeze and `e0be61e4`; `grep -n` locators vs pins (`sed -n` range
re-opens); `grep -c` census recomputation; `sha256sum` of reference, fixtures, receipts; `python3 -I
l1-draft/mado-devices.py --selftest` (48/48, exit 0) under `/fast/scratch/hyaku/mado-r46/ConnLessons`;
`wc -l` on the ten pins. No counter executed; no lane or host mutation.
