# bypass ledger (mechanical, zero-work)

| instrument | description | accountability pointer |
|---|---|---|
| `quality/check-axis-scores.py` | mado — calibration gate: the lane's published axis table must not be stale. | `SCORECARD.md:2081` |
| `quality/check-control-receipts.py` | Round-27 successor of the QUALITY criterion 36 checker (round-26 spot-check §7 repairs 2 and 5). | `corpus/lessons/round-25-verifier-spotcheck.md:135` |
| `quality/check-counter-discrimination.py` | mado — counter-discrimination gate: can the lane's own counters tell work from shape? | `PROVINCE.md:61` |
| `quality/check-deliverables.py` | check101-deliverables.py — seat prototype for candidate QUALITY criterion 101 (M49-3). | `corpus/QUALITY.md:566` |
| `quality/check-evidence-pointers.py` | mado — evidence-pointer durability gate: does every pointer in the lane's own records resolve? | `PROVINCE.md:64` |
| `quality/check-index-rows.py` | mado index-row fidelity gate (round 31, claim C1). | `SCORECARD.md:2032` |
| `quality/check-index.py` | mado index-completeness gate (round 30, claim C3 / capability row; | `SCORECARD.md:202` |
| `quality/check-landed-contract.py` | QUALITY 96 - a landed contract is not narrower than, nor silently different from, the frozen reference. | `corpus/lessons/round-48.md:245` |
| `quality/check-locators.py` | check-locators.py - recompute prose source locators against pinned receipts. | `SCORECARD.md:2548` |
| `quality/check-population.py` | Round-28 quality check for QUALITY criterion 37 (round-25 routed defect 3, M25-4): | `SCORECARD.md:1735` |
| `quality/check-r38-discrimination.py` | mado — round-38 discrimination gate: do the v3 counters tell work from crib? | `SCORECARD.md:200` |
| `quality/check-round-outcome-first.py` | check-round-outcome-first.py — check for QUALITY criterion 99 (round-48; drafted by seat ScrConsider as "check96", renumbered at landing). | `corpus/lessons/round-48.md:187` |
| `quality/check-session-material.py` | check-session-material.py — privacy gate for committed receipts. | `PROVINCE.md:100` |
| `quality/check-state-cite.py` | check100-state-cite.py — seat prototype for candidate QUALITY criterion 100 (M49-1). | `corpus/QUALITY.md:560` |
| `quality/check-tool-ledger.py` | check-tool-ledger.py -- PRED-C1-r51 gate: the tracked lane-level tool ledger is complete. | `.ufo/waves/round-51/registration.md` |
| `quality/check-wave-done.py` | check-wave-done.py -- did every wave of a round reach WAVE-DONE? | `SCORECARD.md:2763` |
| `quality/counter-selftest.py` | mado round 27 quality: counter self-test, suite A (offline). | `SCORECARD.md:1767` |
| `quality/counters/c1-idle-lock.py` | PRED-C1-r36-v1 counter — the round-35 idle-lock admission counter, repaired. | `PROVINCE.md:56` |
| `quality/counters/c1-r37-event-ground.py` | PRED-C1-r37-v2 — event-socket delivery ground admitted into the corpus. | `SCORECARD.md:2369` |
| `quality/counters/c1-r38-event-ground.py` | PRED-C1-r38-v3 — event-socket delivery ground admitted into the corpus (v3). | `SCORECARD.md:200` |
| `quality/counters/c1-r40-live-v2.py` | PRED-C1-r40-v2 - the option table merges a LIVE compositor in its native forms. | `SCORECARD.md:2480` |
| `quality/counters/c1-r40-live.py` | PRED-C1-r40-v1 - the option table merges a LIVE compositor in its native forms. | `.ufo/waves/round-40/registration.md:38` |
| `quality/counters/c1-r41-globals-v2.py` | PRED-C1-r41-v2 - a read-only census of the compositor's advertised Wayland globals (C1, operability). | `SCORECARD.md:2502` |
| `quality/counters/c1-r41-globals.py` | PRED-C1-r41-v1 - a read-only census of the compositor's advertised Wayland globals (C1, operability). | `corpus/QUALITY.md:393` |
| `quality/counters/c1-r42-geometry.py` | PRED-C1-r42 - a read-only join of window-rule sizes and the compositor's reported client sizes (C1, operability). | `SCORECARD.md:2535` |
| `quality/counters/c1-r44-geometry-states-v2.py` | PRED-C1-r44-v2 - mado-geometry names maximized and fullscreen clients instead of comparing them (C1, operability). | `SCORECARD.md:2570` |
| `quality/counters/c1-r44-geometry-states.py` | PRED-C1-r44 - mado-geometry reports maximized and fullscreen clients as such (C1, operability). | `.ufo/waves/round-44/registration.md:27` |
| `quality/counters/c1-r45-monitors-v2.py` | PRED-C1-r45-v2 - tools/mado-monitors.py joins monitor rules with live output state (C1, operability, capability acquisition). | `SCORECARD.md:2600` |
| `quality/counters/c1-r45-monitors.py` | PRED-C1-r45 - tools/mado-monitors.py joins monitor rules with live output state (C1, operability, capability acquisition). | `.ufo/waves/round-45/registration.md:21` |
| `quality/counters/c1-r46-devices-v2.py` | PRED-C1-r46-v2 - tools/mado-devices.py joins input/device config with live keyboard and mouse state (C1, operability, capability acquisition). | `PROVINCE.md:109` |
| `quality/counters/c1-r46-devices-v3.py` | PRED-C1-r46-v3 - tools/mado-devices.py joins input/device config with live keyboard and mouse state (C1, operability, capability acquisition). | `PROVINCE.md:109` |
| `quality/counters/c1-r46-devices.py` | PRED-C1-r46 - tools/mado-devices.py joins input/device config with live keyboard and mouse state (C1, operability, capability acquisition). | `PROVINCE.md:108` |
| `quality/counters/c1-r47-terminal.py` | PRED-C1-r47 - tools/mado-terminal.py answers which terminal xdg-terminal-exec picks (C1, operability, capability). | `SCORECARD.md:2660` |
| `quality/counters/c1-r48-terminal-cache-v2.py` | PRED-C1-r48-v2 - tools/mado-terminal.py predicts which terminal xdg-terminal-exec picks, INCLUDING the warm cache. | `SCORECARD.md:2707` |
| `quality/counters/c1-r48-terminal-cache.py` | PRED-C1-r48 - tools/mado-terminal.py predicts which terminal xdg-terminal-exec picks, INCLUDING the warm cache. | `corpus/lessons/round-48.md:153` |
| `quality/counters/c1-r49-keysym.py` | PRED-C1-r49 - tools/mado-keysym.py predicts what `xkbcli how-to-type --disable-compose --keysym` prints. | `SCORECARD.md:2736` |
| `quality/counters/c1-r50-bind-entry.py` | PRED-C1-r50 - the Hyprland bind-key-match entry is admitted (C1, coverage, sourced). | `SCORECARD.md:2754` |
| `quality/counters/c1-r51-ledger.py` | c1-r51-ledger.py — PRED-C1-r51: the tracked lane-level tool ledger is complete and accountable. | `.ufo/waves/round-51/registration.md` |
| `quality/counters/c2-ledger.py` | PRED-C2-r36-v1 counter — the lane's evidence ledger, repaired against its own fail-opens. | `PROVINCE.md:59` |
| `quality/counters/c2-r37-eventq.py` | PRED-C2-r37-v2 — the event-socket subscriber census runs and discriminates. | `SCORECARD.md:2370` |
| `quality/counters/c2-r38-eventq.py` | PRED-C2-r38-v3 — the event-socket subscriber census runs and discriminates (v3). | `SCORECARD.md:2435` |
| `quality/counters/c2-r38-request-ground.py` | PRED-C2-r38-v1 — request-socket contract ground admitted into the corpus. | `SCORECARD.md:201` |
| `quality/counters/c2-r40-forms-entry-v2.py` | PRED-C2-r40-v2 - the getoption native-forms entry is admitted (C2, coverage). | `SCORECARD.md:2481` |
| `quality/counters/c2-r40-forms-entry.py` | PRED-C2-r40-v1 - the getoption native-forms entry is admitted (C2, coverage). | `.ufo/waves/round-40/registration.md:77` |
| `quality/counters/c2-r41-focus-entry-v2.py` | PRED-C2-r41-v2 - the Hyprland focus-grab entry is admitted (C2, coverage, sourced). | `SCORECARD.md:2503` |
| `quality/counters/c2-r41-focus-entry.py` | PRED-C2-r41-v1 - the Hyprland focus-grab entry is admitted (C2, coverage, sourced). | `corpus/lessons/round-41.md:128` |
| `quality/counters/c2-r42-gkeep-entry.py` | PRED-C2-r42 - the Hyprland gkeep-geometry entry is admitted (C2, coverage, sourced). | `corpus/lessons/round-44.md:180` |
| `quality/counters/c2-r43-gkeep-entry-v2.py` | PRED-C2-r43-v2 - the Hyprland gkeep-geometry entry is admitted (C2, coverage, sourced). | `SCORECARD.md:2536` |
| `quality/counters/c2-r43-gkeep-entry.py` | PRED-C2-r43 - the Hyprland gkeep-geometry entry is admitted (C2, coverage, sourced). | `corpus/lessons/round-43.md:150` |
| `quality/counters/c2-r44-gkeep-size-request-v2.py` | PRED-C2-r44-v2 - the gkeep size-request entry is admitted (C2, coverage, sourced; assimilation). | `SCORECARD.md:2571` |
| `quality/counters/c2-r44-gkeep-size-request.py` | PRED-C2-r44 - the gkeep size-request entry is admitted (C2, coverage, sourced; assimilation). | `corpus/lessons/round-44.md:179` |
| `quality/counters/c2-r45-monitor-entry-v2.py` | PRED-C2-r45-v2 - the monitor-rule entry is admitted (C2, coverage, sourced). | `SCORECARD.md:2601` |
| `quality/counters/c2-r45-monitor-entry.py` | PRED-C2-r45 - the monitor-rule entry is admitted (C2, coverage, sourced). | `.ufo/waves/round-45/registration.md:46` |
| `quality/counters/c2-r46-input-device-entry-v2.py` | PRED-C2-r46-v2 - the input-device entry is admitted (C2, coverage, sourced). | `SCORECARD.md:2632` |
| `quality/counters/c2-r46-input-device-entry.py` | PRED-C2-r46 - the input-device entry is admitted (C2, coverage, sourced). | `PROVINCE.md:111` |
| `quality/counters/c2-r47-terminal-entry.py` | PRED-C2-r47 - the terminal-selection entry is admitted (C2, coverage, sourced). | `SCORECARD.md:2661` |
| `quality/counters/c2-r48-xkb-entry-v2.py` | PRED-C2-r48-v2 - the XKB-compile entry is admitted (C2, coverage, sourced). | `SCORECARD.md:2708` |
| `quality/counters/c2-r48-xkb-entry.py` | PRED-C2-r48 - the XKB-compile entry is admitted (C2, coverage, sourced). | `corpus/lessons/round-48.md:153` |
| `quality/counters/c2-r49-bind-entry.py` | PRED-C2-r49 - the Hyprland bind-key-match entry is admitted (C2, coverage, sourced). | `SCORECARD.md:2737` |
| `quality/counters/c2-r50-session-gate.py` | c2-r50-session-gate.py — PRED-C2-r50: the session-material gate detects its covered shapes. | `SCORECARD.md:2755` |
| `quality/counters/c2-r51-dispatch-entry.py` | PRED-C2-r51 - the dispatcher-dispatch entry is admitted (C2, coverage, sourced). | `.ufo/waves/round-51/registration.md` |
| `quality/counters/c3-r39-options.py` | PRED-C3-r39-v2 - the option-ownership tool resolves trees it has never seen. | `SCORECARD.md:2436` |
| `quality/counters/c4-r39-options-entry.py` | PRED-C4-r39-v1 - the config-option ownership ground is admitted (C3). | `SCORECARD.md:2437` |
| `quality/population-suite.py` | Offline gate over the round-26 population checker (quality/check-population.py). | `SCORECARD.md:1767` |
| `quality/ratio-domain-meta.py` | Re-runnable domain-versus-meta count over SCORECARD claim rows. | `SCORECARD.md:2583` |
| `tools/mado-action-plan.py` | mado-action-plan.py — fail-closed static action-plan safety gate (mado r16 / C2). | `PROVINCE.md:20` |
| `tools/mado-anims.py` | Static resolver for the animation table of a Hyprland v0.56.2 config tree. | `PROVINCE.md:30` |
| `tools/mado-assessment.py` | Read-only artifact assertion gate, not independent authentication of its author. | `PROVINCE.md:20` |
| `tools/mado-binds.py` | Static resolver for the bind table of a Hyprland v0.56.2 config tree. | `PROVINCE.md:29` |
| `tools/mado-devices.py` | mado-devices - does each keyboard run the XKB names its config declares, and does each mouse report the scroll factor its device block sets? | `PROVINCE.md:105` |
| `tools/mado-eventq.py` | mado-eventq — read-only census of Hyprland event-socket (socket2) subscribers. | `SCORECARD.md:2370` |
| `tools/mado-evidence-audit.py` | Audit artifact arithmetic and explicit evidence labels, never execution truth. | `PROVINCE.md:20` |
| `tools/mado-geometry.py` | mado-geometry - does the size a window rule asks for match the size the compositor reports? | `PROVINCE.md:32` |
| `tools/mado-globals.py` | mado-globals — read-only census of the Wayland globals the compositor advertised. | `PROVINCE.md:31` |
| `tools/mado-hostguard.py` | mado-hostguard.py - run a command against a scratch HOME and fail if a declared operator-owned path changed. | `SCORECARD.md:2762` |
| `tools/mado-keysym.py` | mado-keysym.py - which key and modifiers type a keysym under a compiled keymap. | `SCORECARD.md:2730` |
| `tools/mado-monitors.py` | mado-monitors - does each connected output run the mode, position, scale and transform its monitor rule declares? | `PROVINCE.md:100` |
| `tools/mado-options.py` | mado-options.py - static resolver of the config-tree option table. | `SCORECARD.md:2436` |
| `tools/mado-terminal.py` | mado-terminal.py - which terminal does `xdg-terminal-exec` (SUPER+RETURN on this host) pick, and why. | `SCORECARD.md:2660` |
| `tools/mado-tripwire.py` | mado-tripwire — post-hoc tripwire over OMP session transcripts (JSONL). | `PROVINCE.md:20` |
| `tools/mado-verify.sh` | ============================================================================= mado-verify.sh — mado-shokunin config-plane verdict gate (v1, round 5 / M5-2) | `PROVINCE.md:18` |
| `tools/mado-wsrules.py` | mado-wsrules.py - workspace rule table from config bytes (Hyprland v0.56.2). | `SCORECARD.md:1766` |
