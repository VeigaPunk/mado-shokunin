# Round 45 lesson — the monitor rule plane (2026-10-26, hyaku run 9, attempt 1)

Lane mado-shokunin. Claims: C1 operability (capability acquisition) `tools/mado-monitors.py`; C2 coverage (sourced)
`corpus/knowledge/hyprland-monitor-rule-r45.md`. Registration `.ufo/waves/round-45/registration.md` (freeze `22a8dedd`), superseded before
any data by `registration-v2.md` (freeze `7c0b0035`) after wave w1 (41 seats) broke both v1 predicates.

## Gate

Candidates considered: the nine v1 pins and five v2 pins under `.ufo/waves/round-45/fetch/` (all fetched and opened by the L1 2026-10-26;
sha256 in `.ufo/waves/round-45/receipts/fetch-sha256.txt`); held S158 (HyprCtl.cpp) and S162 (legacy ConfigManager.cpp) for reuse; the
hyprland-wiki Monitors page at main; Hyprland main (fb6e5380) Parser/Rule sources (w1/ScoutRecheck); `merge/mado/` package themes (w1/ExecIdGuard).

Admitted (new rows S302-S315, tier A, status mined, opened 2026-10-26, used-by the entry). Quotes are whitespace-normalized; S303, S305,
S306, S307, S308, S311, S313 span or de-space source lines, as the locator's start line shows. Each URL is the row's location cell.

GATE S302 receipt=.ufo/waves/round-45/fetch/Hyprland-Parser.cpp sha256=616468fd0576d8b201ef00cd69289234f0ffb1c3137ae2a0ac954fabe37dd589 quote="m_rule.m_refreshRate = stof(value.substr(value.find_first_of('@') + 1));"
GATE S303 receipt=.ufo/waves/round-45/fetch/Hyprland-legacy-ConfigManager.cpp sha256=9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b quote="if (ARGS[1] == "disable" || ARGS[1] == "disabled" || ARGS[1] == "addreserved" || ARGS[1] == "transform") {"
GATE S304 receipt=.ufo/waves/round-45/fetch/Hyprland-MonitorRuleManager.cpp sha256=17d46685c2623657f52e71b22a033c0a798cf3903f7bbeb64ceebce87527f016 quote="std::erase_if(m_rules, [&x](const auto& e) { return e.m_name == x.m_name; });"
GATE S305 receipt=.ufo/waves/round-45/fetch/Hyprland-MonitorRule.hpp sha256=b01d31a16d5fb413ead28f46825381f36a70c29b86eceb58cd633dcbf031a2f5 quote="float m_refreshRate = 60;"
GATE S306 receipt=.ufo/waves/round-45/fetch/Hyprland-Monitor.cpp sha256=9cf88e154eb5dae676c79d37b5b055ca6134838857cecdbb89a3b747a6821927 quote="float searchScale = std::round(m_scale * 120.0);"
GATE S307 receipt=.ufo/waves/round-45/fetch/Hyprland-HyprCtl.cpp sha256=798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa quote=""physicalHeight": {}, "refreshRate": {:.5f},"
GATE S308 receipt=.ufo/waves/round-45/fetch/Hyprland-MonitorPositionController.cpp sha256=3b705388fa53aef77c5e8c6f6307c94dab08b5dae9460bab427d648359b5ae49 quote="m->moveTo(*POS); arranged.push_back(m); it = toArrange.erase(it);"
GATE S309 receipt=.ufo/waves/round-45/fetch/hyprutils-String.cpp sha256=a92c131a45f41918388eece78f225dbeab7791bb3cd2d3761d840aefa1527bac quote="if (i == 0 && str.at(i) == '-') {"
GATE S310 receipt=.ufo/waves/round-45/fetch/wiki-Monitors.md sha256=f2ac7025b7d7dd13b467ad52a5ca7b4da39e198f3ae4c6a675f92a38cd0304b9 quote="monitor = name, resolution, position, scale"
GATE S311 receipt=.ufo/waves/round-45/fetch/Hyprland-MonitorState.cpp sha256=b5033be770b95f13b9ca65d9f60daae2446910e946576156c50dae8da89cab1c quote="mon->m_self = mon; m_realMonitors.emplace_back(mon);"
GATE S312 receipt=.ufo/waves/round-45/fetch/Hyprland-macros.hpp sha256=b62d51406768f08d3a820c882de77ac47b55c15693b68322180ff2002164d738 quote="#define DELTALESSTHAN(a, b, delta) (abs((a) - (b)) < (delta))"
GATE S313 receipt=.ufo/waves/round-45/fetch/hyprutils-Vector2D.hpp sha256=967bd9d7e12efb8f68694760f6d28b8b3c4810055b966b8c61e2ecebb6de2ddb quote="constexpr Vector2D operator/(const double& a) const { return Vector2D(this->x / a, this->y / a);"
GATE S314 receipt=.ufo/waves/round-45/fetch/hyprutils-VarList2.hpp sha256=0e484df50ec18ef432c319a4d3249dfc3ddf25bb990a836ebcdd597a441f2179 quote="explicit CVarList2(std::string&& in, const size_t lastArgNo = 0, const char delim = ',',"
GATE S315 receipt=.ufo/waves/round-45/fetch/aquamarine-DRM.cpp sha256=ff9b19d823a0f2f8b365ba7efd4b09bf9515fcfcdb10f3b1ae505abd6d1977b3 quote="output->description = std::format("{} {} {} ({})", make, model, serial, szName);"

Rejected:
- REJECT reuse of held S158/S162 for the monitor scope: their scope cells cover clients/getprop/layers and windowrule handlers; new rows
  S307/S303 carry the same URLs under the monitor scope (census W04, not an error). Flip: a registry rule that lets one row hold several scopes.
- REJECT hyprland-wiki Monitors.md at main as a source for this entry: it is Lua-only after Hyprland a9902ea and documents no line form
  (w1/ScoutRecheck drift.md section 2). Flip: the host moves to a Hyprland release past 0.56.x.
- REJECT w1/CritToolSemantics finding 1 (float32 integrality): hyprutils Vector2D holds doubles (`fetch/hyprutils-Vector2D.hpp:21-22,39-41`);
  w1/ExecScaleOracle: 0 divergences in 445,875 cases. Flip: a pin showing float storage of the logical size.
- Assimilation: none. w1/ExecIdGuard found no `merge/mado/` theme on the monitor plane; no staged row appended.

Registry changes: none to held rows (no status/recheck/used-by change).

## Mistakes

**M45-1** · class `scope` (session material) · evidence: `.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json` and
`.ufo/waves/round-43/w2/SentLiveRun/dump-now.json` carried live window titles (round-44 closure D1) · captured-by: SKILL.md rule 4, no gate ·
fix: both projected to the 7-key shape (w1/ExecProjectTitles) and `quality/check-session-material.py` (w1/ExecPrivacyGate, QUALITY 85),
shown able to fail: at base `SESSION_MATERIAL: ... findings=50` with both files listed, on the projected tree 48 (w1/ExecPrivacyGate/base-run.txt,
projected-run.txt). The other 48 findings are open (triage next round).
**M45-2** · class `scope` · evidence: this round's seat `w1/ExecLiveHost/verify-quotes.py` wrote the host monitor serial as a deny-list literal,
and held `corpus/knowledge/hyprctl-verification-layer.md:153` has carried it since round 2 ·
captured-by: none (the gate's R3 rule reads JSON `serial` keys, not prose) · fix: the seat file was redacted before commit; the held entry is
reported, not rewritten (corrections are new entries; history rewrite is the operator's).
**M45-3** · class `vacuous` · evidence: PRED-C1-r45 v1 met by 11 cheats and 5 do-nothing controls (w1/CritC1Cheat, w1/ExecDoNothingC1) ·
captured-by: QUALITY 65-66 (lattice, hidden judge) only partly · fix: v2 clauses i (sandbox) and g (nonce-generated cases against a pinned
reference), shown able to fail: the same 16 tools all MISS under v2 (`receipts/ctl-c1-v2.txt`).
**M45-4** · class `vacuous` · evidence: PRED-C2-r45 v1 admitted 9 forgeries (w1/CritC2Forgery) · captured-by: none for fences, receipt
citations and README ids · fix: v2 T1-T5, shown able to fail by controls PROSE-CENSUS-SPACED, ROW-SUPERSEDES, FENCE-TABLE, RECEIPT-CONTRADICT,
README-IDS (`receipts/ctl-c2-v2.txt`).
**M45-5** · class `stale-premise` · evidence: the v1 reference contract mis-modelled six Hyprland forms (registration-v2.md C1 Why) ·
captured-by: QUALITY 68 (a reference model names the parser it copies) partly · fix: v2 contract + fixtures; K16-K25 controls fail on each.
**M45-6** · class `number-drift` · evidence: round-44 closure D4 (nonce-dependent before share) · captured-by: none · fix: v2 C1 counter's
before state is deterministic (tool absent) and its fixture part runs at seed 45 with the nonce part separate.

## Round-44 closure items

D1 fixed (M45-1). D2: SCORECARD Round 44 after values appended in the Round 45 section (C1 `fixtures=26/26 tool=present verdict=TARGET_MET`,
C2 `admitted=1/1 verdict=TARGET_MET`, `.ufo/waves/round-44/receipts/c1-after-data.txt`, `c2-after-data.txt`). D3: this round's tip receipts name
the commit they measured. D4: M45-6. D5: round-44 counters not reused; C2 v2 keeps the 30-line width bound. D6 (S290-S297 supersession):
deferred again — w1/ExecSupersede drafted rows but T2 of this round's own counter forbids supersession words only in cited rows; landing needs
its own registration. D7: w1/ConnCalibration counted 6 mismatches at base (`w1/ConnCalibration/mismatches.md`), recorded, not corrected here.

## Search log

Question: how does Hyprland 0.56.2 turn a `monitor =` line into the running output, and what does `hyprctl monitors all -j` show? Searched:
the Hyprland tree at efb50993 via the GitHub tree API (files matching Monitor/ConfigManager/HyprCtl: 43 identified), hyprutils v0.14.2,
aquamarine v0.15.1, hyprland-wiki ecc06f3. Screened 43; included 14 (the pins); excluded 29 (zoom, frame scheduling, query, layout controller:
no rule-to-state step). Stop: every step of the chain the tool compares has a pinned line.

## considerthese

`considerthese/2026-10-26.md` proposal 1 (privacy check on new receipts) → `quality/check-session-material.py` + QUALITY 85.
