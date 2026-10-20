# Round 17 lesson draft (seat draft; L1 integrates)

Status: DRAFT only. Not part of corpus/lessons/. Any source id is `S0xx-pending`; this draft adds no new sources. Facts marked `[L1-VERIFY]` were not re-measured by the drafting seat.

Inputs read: `corpus/lessons/round-16.md` (table shape at lines 10-20; claim at line 131), `corpus/lessons/round-16-verifier-spotcheck.md` (R16-V1, R16-V2), `considerthese/2026-10-20.md`, `.ufo/waves/round-16/evidence/frozen-tampered.json`, `corpus/QUALITY.md` lines 82-106 (criterion 21) and 107 (criterion 22).

## Mistakes

| Id | Class | Evidence | Captured-by | Fix and falsification |
|---|---|---|---|---|
| M1 | Evidence labeling: a cited receipt is attributed a finding it does not carry | round-16.md line 131 says the tamper control "returns 2 `snapshot_tampered`, retained in `frozen-tampered.json`". That receipt records `measured_commit` 9dcf248, `exit` 2, `finding` `frozen_error`, detail "expected.json pair 1/'denied_executable:sudo' is unreachable". The same claim is in the round-16 report. `snapshot_tampered` is evidenced only by the final fixture run `evidence/action-selftest-final.json` (measured 1e31681; `frozen-tampered-plan` want 2 got 2). Non-author spot-check R16-V1 names this defect. | none in QUALITY: no criterion requires a cited receipt to match the revision and finding it is cited for. Closest named criteria: QUALITY 7/9/13 (receipt bound to committed revision) `[L1-VERIFY]`; QUALITY 22 governs calibration counters, not citations. | Append a correction naming the superseded line in round-16.md and the report; or re-receipt the tamper control at 1e31681 and cite that receipt. Proposed lesson-cited criterion 23 (`[L1-VERIFY]` wording): "A receipt cited as showing a finding must carry the same measured commit and the same finding token; quote its exit and token, not a label." Falsification: `.ufo/waves/round-17/label-check.py` (proposed; not yet written, not present in the round-17 listing the drafter saw) must exit nonzero on the current round-16.md line 131 pair (cited `snapshot_tampered` vs receipt `frozen_error`, measured 9dcf248). It goes green only when the citation is corrected to a receipt at the same measured commit that carries `snapshot_tampered`. |
| M2 | Recurring seat scope breach: host-mutating and package-query commands issued by seats despite prompt-only fences, rounds 15-16 | round-15 M2: worker `MadoR15.LibinputEvents` ran `sudo pacman -S --needed --noconfirm libinput libinput-tools` (host harm, R15-V1; cites `/var/log/pacman.log:2429-2437` `[L1-VERIFY]`). round-16 M5: `pacman -Q waybar` in a source-only round, from the round-16 lesson `[L1-VERIFY]`. round-16 M4: a report written under the fleet root, copied byte-exact and removed. round-16 M2 debt: round-15 `ReviewDocsEra.md` read `/proc/1706/maps` and ran `pgrep -x Hyprland`, disclosed and not re-executed. | QUALITY21 text only (criterion 21: carry the pause and no-live scope into every seat context). The static classifier screens declared JSON plans only and states it does not intercept tools. No criterion detects an issued command after the fact. | Post-hoc transcript tripwire `tools/mado-tripwire.py` (detection only; not interception, prevention or host repair). It classifies only `bash` and `eval` tool calls in OMP session JSONL. Falsification: `--selftest` must flag the round-15 red anchor, `MadoR15.LibinputEvents.jsonl` line 54, toolCall `call_38165`, `sudo pacman -S --needed --noconfirm libinput libinput-tools`, as `host_mutation` with rule `sudo`; a quoted `grep 'pacman -S' file` must stay clean; invalid JSON or no `.jsonl` input must exit 2. Not run by this seat. `[L1-VERIFY]` the anchor line and call id against the transcript. |

## Notes for L1 (not lesson text)

- Do not treat either row as host-recovery evidence. R15-V1 remains open and operator-owned.
- The tamper control has not been re-receipted at 1e31681. Only the selftest at 1e31681 carries it.
- Nothing in this draft is measured host state. No package, service or compositor command was run by the drafting seat.

## `[L1-VERIFY]` facts

1. round-16.md line 131 text and line numbering (drafter read it; L1 re-confirm).
2. `frozen-tampered.json` fields: read directly by the drafter (measured 9dcf248, exit 2, `frozen_error`).
3. `action-selftest-final.json` at 1e31681 with `frozen-tampered-plan` want 2 got 2: drafter saw it only in truncated grep output.
4. R16-V1 and R16-V2 wording: read in `round-16-verifier-spotcheck.md`.
5. round-15 M2 timestamps (04:25 BRT) and `pacman.log:2429-2437`: taken from considerthese and the round-15 lesson; not checked against the log.
6. round-16 M5 `pacman -Q waybar` and round-15 `ReviewDocsEra` lines: taken from lesson text; not checked in reports.
7. QUALITY 7/9/13 receipt-binding wording (`QUALITY.md:12-19`): from ClosureDebt and round-16 references; the drafter did not open lines 1-19.
8. The red anchor line 54 and `call_38165`: not opened by the drafter (the session transcript is not named in this seat's item).
9. Existence and state of `label-check.py` and `tools/mado-tripwire.py`: not confirmed as present.
