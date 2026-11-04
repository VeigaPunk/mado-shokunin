# R79ScribeEntry — C1 knowledge entry draft and source audit

Seat: scribe. Round: 79, wave 1. Lane: mado-shokunin. Base revision
`e4b153dfa4a67ca56f7ec65cb6639082451626a7`; freeze `5eb8f20fe291603c74973fa94cc55723ac8089a4`.
Write scope: this file plus `.ufo/waves/round-79/w1/R79ScribeEntry/`. No repo file was edited, no
git/jj write command was run, no host write or compositor write was issued.

## Axes named (Godspeed)

1. **Coverage** — how much of the static-`addreserved` composition the entry can state from pinned
   bytes, with each claim traceable to one S-id and line.
2. **Auditability** — every number in the entry either names a receipt line or a case name; no value
   was produced by re-running the counter here.
3. **Frontier honesty** — the places where the frozen case set assumes more than the source states
   are named in the entry and below, not smoothed over.

## Artifact

Draft entry: `.ufo/waves/round-79/w1/R79ScribeEntry/bar-footprint-reserve-r79.md`
(110 lines, provenance trio present, `Report:` trailer not embedded). It is staged only; the L1 owns
integration into `corpus/knowledge/`.

## Commands run and observed output

All read-only, from `/home/vgpnk/Projects/shokunin/mado-shokunin`.

1. `sha256sum -c .ufo/waves/round-79/fetch/sha256-r79.txt`
   → `S457.bin: OK` … `S466.bin: OK` for nine source rows, then
   `.ufo/waves/round-79/fetch/sha256-r79.txt: FAILED` (see F2).
2. `sha256sum tools/mado-barfoot.py .ufo/waves/round-79/controls/c1-cases-r79.json`
   → `c9aa139152643020acf27b5aef8026ae5b8a5f70372e86abb4a032c82bed86de` (matches the declaration's
   `r79-v1` pin) and `5f7ebb3c47c68dedcd113f29f63f995fccdb201e16eb949a4a450be892252eb7` (matches the
   frozen control set `5f7ebb3c…`).
3. `grep -n "setStatic\|logicalBoxMinusReserved\|m_reservedArea" .ufo/waves/round-79/fetch/S465.bin`
   → `654: m_reservedArea.setStatic(m_activeMonitorRule.m_reservedArea);`,
   `1772: CBox CMonitor::logicalBoxMinusReserved() const {`, `1773: return m_reservedArea.apply(logicalBox());`.
4. `grep -n "m_size\|xfmd" .ufo/waves/round-79/fetch/S465.bin`
   → `699: Vector2D xfmd = …`, `700: m_size = (xfmd / m_scale).round();` (duplicated at `:1058-1059`).
5. `sed -n '1,120p'` on `S466.bin` → `calculate` `:43-51` (`m_bottomRight += e.bottomRight;` / `m_topLeft +=
   e.topLeft;`), parent/child ctor `:19-37`, `setStatic` `:69-74`, `addType` `:101-108` plus the
   `CReservedArea` overload `:110-112`.
6. `grep -n "ORIGINAL_USABLE_AREA\|addType(Desktop::RESERVED_DYNAMIC_TYPE_LS\|resetType" S457.bin`
   → `2680: PMONITOR->m_reservedArea.resetType(Desktop::RESERVED_DYNAMIC_TYPE_LS);`,
   `2682: const CBox ORIGINAL_USABLE_AREA = PMONITOR->logicalBoxMinusReserved();`,
   `2696: …addType(Desktop::RESERVED_DYNAMIC_TYPE_LS, Desktop::CReservedArea{ORIGINAL_USABLE_AREA, usableArea});`.
7. `grep -n "applyExclusive" S457.bin` → `2529: static void applyExclusive(CBox& usableArea, …)`,
   `2664: applyExclusive(*usableArea, …)`; body shows `if (exclusive <= 0) return;` at `:2531-2533`,
   the `exclusive + edges[i].margin > 0` guard at `:2575`, `+=` at `:2577`, `-=` at `:2580`.
8. `grep -n "m_reservedArea" S458.bin` → `281-282` print `left(), top(), right(), bottom()`;
   `grep -n "namespace\|pid"` → layers template `676-677`.
9. `sed -n '1293,1400p' .ufo/waves/round-45/fetch/Hyprland-legacy-ConfigManager.cpp` →
   `1299` modifier test, `1323` `area = {stoi(ARGS[2]), stoi(ARGS[5]), stoi(ARGS[3]), stoi(ARGS[4])}`,
   `1331: rule->m_reservedArea = area.value();`, `1341: Config::monitorRuleMgr()->add(std::move(parser.rule()));`,
   `1384:` the same add on the positional path.
   `grep -n "void CMonitorRuleManager::add" Hyprland-MonitorRuleManager.cpp` → `37`, body `38:
   std::erase_if(m_rules, …m_name == x.m_name…)`.
10. `grep -rl "addreserved" /home/vgpnk/.config/hypr/ ; echo $?` → no output, `1` (no static reserve on
    this host; `monitors.conf` exists, 1012 B).

## Findings (data)

**F1 — the rule-slot assumption is real, and one frozen case leans on it.** `handleMonitor` writes an
`addreserved` area into the selector's *existing* rule (`Hyprland-legacy-ConfigManager.cpp:1331`) and
returns; when no rule exists it falls through to `add(parser.rule())` at `:1341`, where `parser` was
built from the selector only (`:1297`) and never received the area, so the rule is added with a zero
reserve. The tool models the area as effective whenever `addreserved` appears (`tools/mado-barfoot.py:369-374`),
and `static-composed` carries only `monitor = M1, addreserved, 26, 0, 0, 0` in its `rules` cell
(`.ufo/waves/round-79/controls/c1-cases-r79.json`, `static-composed.rules`). Read strictly, a config
whose only M1 line is that `addreserved` would leave a zero static reserve, so the case's
`expected=60` (receipt `MADO_R79_CASE: name=static-composed … band=60 expected=60`) presupposes a
pre-existing M1 rule slot — true of any config that also positions the monitor. This is a modelling
assumption, not a measurement error: the instrument and case set are frozen and the score stands. The
entry states it in §2 and in "What is not claimed". `[INFERENCE]` for the runtime consequence: no live
reload was performed (host posture is read-only), so the drop was read from source, not observed.

**F2 — the fetch manifest cannot verify itself.** `sha256sum -c` (step 1) fails only on
`.ufo/waves/round-79/fetch/sha256-r79.txt`, which is line 10 of its own listing with digest
`a9806336…`. A file cannot contain its own post-write digest, so this row is unverifiable by
construction and the nine source rows are the meaningful pins. Reported so no later seat reads the
warning as a source drift.

**F3 — S466 and S459 are one file pinned twice.** Both `.ufo/waves/round-79/fetch/S459.bin` and
`S466.bin` hash to `0a52e145ed2bdfddfa2b2e658ef2d326a01e86b2266d8af0f015915452a6e0db` (all 3339 B), i.e.
the same `src/desktop/reserved/ReservedArea.cpp` at `efb5099`. The declaration calls S466 a new row;
the entry says "byte-identical to S459" so a reader does not infer two distinct files.

**F4 — an off-by-one in the committed SOURCES row for S465.** `corpus/SOURCES.md:417` states
`applyMonitorRuleSoft :653-655`. Observed: the function opens at `:652`, `:653` is
`m_activeMonitorRule = std::move(pMonitorRule);`, and `:654` is the `setStatic` call; `:655` is
`m_transform = …`. The span `:652-655` (used in the entry) covers the function; `:653-655` starts one
line late. SOURCES.md is a committed lane file, so this is reported, not edited.

**F5 — the tree already holds a draft of the target entry.** `corpus/knowledge/bar-footprint-reserve-r79.md`
exists (read-only to this seat) with a compatible shape: 23/23, twelve mutants, `base_correct=18/23`,
and the same S466 `addType :101-112` span (accurate as a span over the two overloads `:101-108` and
`:110-112`). Differences from my staged draft: (a) it does not state the rule-slot assumption of F1;
(b) its decision table omits the `exclusive: false` *without* static row (`exclusive-false` case,
receipt `band=0 expected=26 reserved=NOT_APPLIED`); (c) its `addreserved` span `:1319-1341` is broader than the two anchors
(in-place set `:1331`, fall-through add `:1341`); (d) it does not note that S466 and S459 are
byte-identical. Integration choice belongs to the L1.

## What this report does not claim

- The counter was **not** re-run. `correct=23 killed=12 base_correct=18/23 carried=18/18
  tool_selftest=43/43 verdict=TARGET_MET` is quoted from
  `.ufo/waves/round-79/receipts/measurement-c1-r79.txt`, and `18/23 killed=4` from
  `control-c1-r79-at-base.txt`; my only measurement is the hash check of step 1-2.
- No host state was probed beyond reading `~/.config/hypr/**`; `hyprctl` was not called at all.
- C2 (runbook operability) was not audited by this seat; the C2 points above are not made.
- No claim about Hyprland after v0.56.2; anchors are at `efb5099` only.

## Tooling

No tool was installed, upgraded or run beyond `sha256sum`, `sed`, `grep`, `wc`, `awk`. No pacman
transaction was attempted.

Report: .ufo/waves/round-79/w1/R79ScribeEntry.md
