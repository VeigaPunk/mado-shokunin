# CritPremise — round 47 w1 (seat report, final)

Premise attack on C1 (tools/mado-terminal.py) and C2 (corpus/knowledge/xdg-terminal-selection-r47.md) before the L1 freeze.

**Status: COMPLETE.** Findings: `.ufo/waves/round-47/w1/CritPremise/findings.md`.

## Bottom line

- **C1 (capability) premise HOLDS**: at base `60edb66…` no lane tool resolves xdg-terminal-exec selection (14 tools, none a terminal resolver; mado-binds.py knows the launch command string only; mado-verify.sh checks config files only). Two wording fixes: scope "which terminal SUPER+RETURN launches" to the resolver's selection (uwsm-app / `--dir` seam is outside the model); and clarify the observe source phrase in C2 (F6/F7).
- **C2 (coverage) premise is mis-scoped**: (F1) print-mode runs never observe launch, so the round-17 [UNK] ("…at launch", terminal-route-r17.md:144-145) cannot be closed as worded — only its *selection* half can be re-observed; (F2) that selection fact is already recorded at base (r17:123-127 cache [OBS, bytes]; HostTerminalFiles.md:33), so a do-nothing control (reading the existing cache) reaches the same conclusion — the live run adds only a dated cold re-derivation; (F3) most of the claimed surface (list order, validation, cache, execargs) is already in r17:24-59; genuinely new rules are narrow: print-mode output semantics, `--hold/--app-id/--title` action composition, ShowIn/NotShowIn, exit-code map, upstream test-suite artifacts; (F4) the [UNK] is open at base but already narrowed by cache bytes and round-23 process observations — crediting C2 with "closing" it mis-assigns credit.

## Evidence anchors (verified)
- terminal-route-r17.md:123-127, 128-130, 144-145 (base rev via `jj file show -r 60edb66…`)
- round-17/w2/reports/AttackP4Claims.md:61-65; round-17/drafts/FrontierDraft.md:8
- round-17/w1/reports/HostTerminalFiles.md:32-33; round-23/w1/reports/HostFoot.md:127,151; SKILL.md:218
- round-47/claims.md:10-17; base tools/ listing (`jj file list -r 60edb66…`); mado-binds.py:2-10,56-69; mado-verify.sh:3261-3316; SKILL.md:121-127

## Compliance
- Read-only repo inspection only (jj log/file show, greps, file reads); no host mutation, no terminal run, no process/socket usage, no installs. Scratch dir `/fast/scratch/hyaku/mado-r47/CritPremise` created empty and deleted on finish. Quotes ≤25 words, locators computed by grep -n and verified (appendix in findings.md).
