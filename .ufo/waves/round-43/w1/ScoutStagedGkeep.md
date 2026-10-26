# ScoutStagedGkeep report (mado r43 w1)

Status: done. Deliverable: `.ufo/waves/round-43/w1/ScoutStagedGkeep/survey.md` (table + recommendation). No scratch dir used, no host call, nothing mutated.

## Recommendation
ONE successor entry `corpus/knowledge/hyprland-gkeep-geometry-r43.md`.
- ADMIT (spine) `gkeep-size-to-real-size-r11.md`: only staged file whose public sources (S302-S305 at v0.56.2) land entirely on pinned receipts
  S292-S295 (7/7 quotes FOUND). Optional lineage ADMITs: `glyph-and-geometry-r31.md` (§2 only) and `gkeep-element-rules-r30.md` (rule triad only).
- REFUSE the other 8 (r8, r9, r10, observation-route-r11, r12, r13, r14, r15) - reasons and flip conditions in survey.md §4.

## Findings that matter
1. The package carries NO private receipts (`lanes/` absent): S275, S292, S293, S299, S310, S320, S326, S339 cannot be re-opened by anyone.
2. The counter PINS contain no `Window.cpp`: staged quotes from Window.cpp (`fetchClass`, `readStaticRules(true)`, `setPseudoSize`, `REPORTSIZE`,
   `sendWindowSize`, `onAck`, `Map request dispatched`) are 8/8 ABSENT from every pinned receipt, so r9/r10/r12/r13 are not admissible this round.
3. Quote check: 24 staged quotes grepped against the 10 pins - 17 FOUND (with locators), 8 ABSENT (all Window.cpp), 1 absence claim
   (r12 "no set_size_request") not provable from the 45-line excerpt (true on the host ui.py: 0 hits, sha256 07a3c4a5...e66a).
4. r31 cites dangling ids: "round 5's row S219" (staged S219 = omarchy hypridle.conf) and S216 (a Chinese CSDN blog row = localized channel, PROVINCE
   Round-36). Staged ids S203-S349 collide with lane ids; successor uses S290-S299.
5. Pins qualify r11's "settled": size applied only inside `m_firstMap` (DefaultFloatingAlgorithm.cpp:49; else lastFloatingSize :85-87), value is an
   expression (WindowRuleApplicator.cpp:422, calculateExpression :56, parse-fail logs ERR :58), `sendWindowSize` is unpinned Window.cpp -> `[UNK]`.
6. Staged gaps the pins fill that no staged file covers: RE2 `FullMatch`/`negative:` (RegexMatchEngine.cpp:7-8,:16), `clients -j` size =
   `GEOMETRIC_GOAL` (HyprCtl.cpp:427-428,:448 -> GeometricMovableAnimated.cpp:19), today's census (4 clients, gkeep=0).
7. "Lane cannot observe" (r8, r13 §4, r14 §3) is stale: `hyprctl clients -j` is an allowed read; census has 4 clients, not 3.

Verified: `sha256sum -c ../receipts/fetch-sha256.txt` 10/10 OK. Not run: any counter or control (not my assignment).
