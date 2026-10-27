# Round 51 lesson — dispatcher execution and instrument ledger (2026-10-27, hyaku run 10)

Base `6ca8c559a4a3d6d361101592116eea2bc7452437`; claim freeze `d274028163033244bd78938ad152dc250cc50480`; C1 freeze/capability commit `56026fcb9800370ae04bc65952a6567181c398d0`. Wave 1: 43 seats, all settled; results `.ufo/waves/round-51/w1-results.json`. C1 is the lane-level instrument ledger; C2 is the sourced Hyprland dispatcher-execution entry.

## Gate

### Admitted: C2 dispatcher-execution entry

`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` — new dispatcher-execution ground, distinct from the round-50 key-match surface. New rows S364-S369, all status `mined`, opened 2026-10-27, used by this entry. Each quote was opened and checked at its cited pin line; quote spans are copied from the pin and are ≤25 whitespace words:

- S364, tier A, code. URL: https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp; pin `.ufo/waves/round-51/fetch/Hyprland-KeybindManager.cpp:785`; quote: `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);` (9 words).
- S365, tier A, code. URL: https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp; pin `.ufo/waves/round-51/fetch/Hyprland-legacy-DispatcherTranslator.cpp:32`; quote: `return {.success = false, .error = "Bad dispatcher"};` (8 words).
- S366, tier A, code. URL: https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp; pin `.ufo/waves/round-51/fetch/Hyprland-HyprCtl.cpp:1149`; quote: `const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(DISPATCHSTR);` (5 words).
- S367, tier A, code. URL: https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.cpp; pin `.ufo/waves/round-51/fetch/Hyprland-ConfigActions.cpp:1681`; quote: `return std::unexpected(std::format("Cannot set submap {}, submap doesn't exist (wasn't registered!)", submap));` (11 words).
- S368, tier A, code. URL: https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp; pin `.ufo/waves/round-51/fetch/Hyprland-legacy-ConfigManager.cpp:1594`; quote: `const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(HANDLER);` (5 words).
- S369, tier A, code. URL: https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/SharedDefs.hpp; pin `.ufo/waves/round-51/fetch/Hyprland-SharedDefs.hpp:53`; quote: `bool        passEvent = false;` (4 words).

W1 seat `ScrRowsDispatch/rows.md` includes the independently grep-verified quote transcript and exact row anchors. Staged `merge/mado` candidates were screened by `ScoutAssim`: dispatcher-semantics topics are adjacent candidates, but no matching staged file was available to re-ground into this entry; assimilation is **none** this round. Reject the staged localized-documentation candidate `chinese-hyprland-window-rules-r16.md`: the channel is out of province per `PROVINCE.md`’s round-36 localization refinement; flip only if the lane’s province changes. Staged-ID collision scan found 53 collisions (`S203-S255`), so no staged row was appended. Absent-defect register slice: 13 rows reviewed; all remain `unverifiable` because this seat’s cited payloads could not be independently re-opened; adoption stays closed (see `w1/ScoutQuarantine/quarantine-verdicts.md`).

`considerthese/2026-10-26.md` proposal 2 (opened this round) is partially addressed: C1 creates a lane-level instrument inventory/accountability ledger, but does not record last-live-run or verdict freshness; that part remains open (see `w1/ScoutConsiderthese/considerthese-row.md`). No other proposal is claimed.

### C1 evidence

C1 at `56026fcb9800370ae04bc65952a6567181c398d0`: `python3 -I quality/counters/c1-r51-ledger.py --repo . --rev 56026fcb9800370ae04bc65952a6567181c398d0 --work /fast/scratch/hyaku/mado-r51/L1/c1-freeze` → `population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET`, exit 0. Base `6ca8c559a4a3d6d361101592116eea2bc7452437` → `ledger=absent population=79 verdict=TARGET_MISSED`, exit 1. Checker selftest 50/50. W1 attacks preserve material predicate limits: a comment-only basename pointer and repeated generic descriptions satisfy the literal frozen predicate; do not interpret these counts as independent semantic accountability.


### C2 evidence

At base `6ca8c559a4a3d6d361101592116eea2bc7452437`, the entry is absent and `quality/counters/c2-r51-dispatch-entry.py` returns `admitted=0/1 verdict=TARGET_MISSED`, exit 1 (`w1/ExecCounterC2/receipt-base.txt`). At data commit `a0e34387b30538372a1bb219eb3ccdc74013d458`, `TMPDIR=/fast/scratch/hyaku/mado-r51/L1/c2-data python3 -I quality/counters/c2-r51-dispatch-entry.py --repo . --rev a0e34387b30538372a1bb219eb3ccdc74013d458 --work /fast/scratch/hyaku/mado-r51/L1/c2-data` returns `clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET`, exit 0; receipt `.ufo/waves/round-51/receipts/c2-at-data.txt`. The counter reports 6 verified rows, maximum 8-gram overlap 0.1% across 66 base knowledge files plus 3 candidate files, and 7/3 held citations. These are lexical/predicate results, not semantic truth certification; the w2 review attacks that boundary.
## Mistakes

**M51-1** · class `evidence chronology` · evidence: round-50 verifier spot-check §2 D1 (`corpus/lessons/round-50-verifier-spotcheck.md`): the report and LOG asserted a two-wave WAVE-DONE receipt at tip `74782d39`, but the committed receipt at `8dbbf61a` only recorded `waves=1 settled=1`; the w2 results landed later at `c12b588e`. · captured-by: none before round 51; the existing checker proved the committed state but the integration process did not require a final-tip receipt. · fix: round-51 integration procedure runs `quality/check-wave-done.py --repo . --rev <final-tip> --round 51` after both results exist and commits that exact output at the integration tip before the report; w1 `RevWaveDone` confirms the round-50 historical red (`8dbbf61a` reports one wave) and final-history green (`74782d39` reports two). The current round’s final receipt is added after w2 at its integration tip, so the procedure is demonstrated able to fail and recover.

W1 first-wave weakness is also retained: RevLedgerPred found C1's literal pointer rule accepts basename-in-comment and non-specific descriptions; CritHeldFacts found C2 held-token bindings can be generic. No predicate was silently amended after seats scored; these residuals remain in `registration.md` for w2 and outside review.

## Assimilation and provenance

Assimilation: none (staged dispatcher candidates were not separately re-grounded/adopted; the new lane-authored entry is C2, not a copied package entry). New S364-S369 rows are the sourced evidence for C2. No tool installs/upgrades this round.
