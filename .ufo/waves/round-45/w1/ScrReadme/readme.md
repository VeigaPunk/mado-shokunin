# ScrReadme — draft `corpus/README.md` index row + Frontier subsection (round 45, w1)

Seat: `ScrReadme` (scribe, leaf). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Freeze read first:
`.ufo/waves/round-45/registration.md` (commit `22a8dedd02f507689c567777e0f20b5e645c8ce0`, base
`0c89478af821a6424c9ac922eafe02e39630cf4f`). Entry under index: `corpus/knowledge/hyprland-monitor-rule-r45.md`
(L1 draft `.ufo/waves/round-45/l1-draft/entry.md`, 90 lines).

Nothing in this file is applied: the L1 integrator pastes the two blocks below. No tracked lane file was edited.

## Axes

1. **Row-shape conformance** — one column-0 line, three cells, `| ` + backticked entry path prefix. That prefix is
   the only thing the frozen predicate reads for the README (`c2-r45-monitor-entry.py:614-615`, clause f:
   `pat = re.compile(r"^\| \`knowledge/%s\`" % re.escape(name))`, exactly one unfenced match).
2. **Claim truth** — every phrase in the row traces to the entry draft or to a pin line I recomputed with `grep -n`
   (receipt `ScrReadme/locators.txt`, check `ScrReadme/check-locators.py` → `locators-check.txt`).
3. **Frontier honesty** — the bullet names exactly what moved (U5 runtime state agreement, read plane only) against
   the two Frontier items it touches (`corpus/README.md:131`, `:137-139`), and names the four remaining open items
   without upgrading any of them to measured.
4. **Integration friction** — paste-ready, numbered insertion points, no serials / monitor descriptions / window
   titles / process tables (session material shape-only).

## 1. Index row — paste after `corpus/README.md:72` (the round-44 row)

The block holds exactly one line. `build-pos.py:98` inserts the placeholder
`| \`knowledge/hyprland-monitor-rule-r45.md\` (MADO-R45-1, round 45) | draft | S302-S310 |` after that same line;
this row replaces the placeholder's cells 2 and 3, and keeps the prefix clause f needs.

```markdown
| `knowledge/hyprland-monitor-rule-r45.md` (MADO-R45-1, round 45; no assimilation — the monitor plane carries no `merge/mado/` theme) | The chain from a `monitor =` line to `hyprctl monitors all -j` at Hyprland 0.56.2 (`efb50993`): the handler splits the line on commas and parses mode, position and scale positionally (`Hyprland-legacy-ConfigManager.cpp:1345-1347`), then reads eight KEY/VALUE keys — mirror, bitdepth, cm, sdrsaturation, sdrbrightness, transform, vrr, icc — and drops the whole line on any other key (`Hyprland-legacy-ConfigManager.cpp:1352-1378`); a rule written without `@RATE` keeps the 60 Hz default, so `WxH` asks for the mode closest to 60 Hz (`Hyprland-MonitorRule.hpp:46`); the rule list is erased-then-appended per selector and searched in reverse with an empty-selector fallback (`Hyprland-MonitorRuleManager.cpp:38,96-106`), a selector matching an exact output name or `desc:` text against the short or the long description (`Hyprland-Monitor.cpp:1201-1211`); a requested mode counts as met within 1 px and 1 Hz (`Hyprland-Monitor.cpp:836-837`); a written scale that leaves a fractional logical size is searched from its nearest 1/120 step, one step up then one down for up to 89 steps (`Hyprland-Monitor.cpp:1001`); explicit positions are placed as written before any `auto` placement (`Hyprland-MonitorPositionController.cpp:27`); the dump prints the running rate to five decimals beside the pixel size, applied scale, `disabled` and `mirrorOf` (`Hyprland-HyprCtl.cpp:242,276-288`) and lists every output only for its `all` argument (`Hyprland-HyprCtl.cpp:320`); and the wiki documents an `sdr_eotf` key the 0.56.2 line handler reads only in `monitorv2` blocks (`wiki-Monitors.md:253`, `Hyprland-legacy-ConfigManager.cpp:819-831`). The read-only join `tools/mado-monitors.py` scores that agreement per output — AGREE / DIFFER / DISABLED / UNRULED, top verdict NO_RULES 4, NOT_COMPARED 5, DIFFER 1, NO_MATCHING_MONITOR 3, OK 0 — and reads AGREE/OK here: one rule and one output, 3440x1440@100 declared against 99.997 Hz reported, 0x0 and scale 1 on both sides. | S302-S310 |
```

Why this shape (checked against the neighbours): the two most recent rows use the same three-cell form and a bare
source-id range in cell 3 (`corpus/README.md:70` `S283-S289, S037`; `:72` `S164, S298, S299, S300, S301`). The range
`S302-S310` is the registry block the entry's nine `source:` lines cite (`entry.md:3-11`) and the block `build-pos.py`
mines as `mined / 2026-10-26 / 90d / corpus/knowledge/hyprland-monitor-rule-r45.md`. Held S158/S162 are not in the
cell: the entry cites S303/S307, whose locations are S162's and S158's URLs under a second scope (registration, C2
sources paragraph; census W04). Cell 2 carries no `|`, no newline and no serial/description.

## 2. Frontier subsection — append at end of `corpus/README.md` (after current line 320)

Precedent is the tail-subsection form of `:295` (round 43) and `:304` (round 44), not a bullet in the older list
(the round-44 section is the file's last block and the file ends with its "Still open:" sentence).

```markdown

### Round-45 monitor-rule route

- Advances the round-14 route's open item "runtime state agreement" for the display plane, and narrows the round-12
  bullet's "output-management behavior" to what can be read rather than applied; no other Frontier bullet is moved.
  What a `monitor =` line declares against what the output runs: the positional parse and the eight-key loop with
  whole-line rejection (`Hyprland-legacy-ConfigManager.cpp:1345-1347,1352-1378`), the 60 Hz default a bare `WxH` line
  inherits (`Hyprland-MonitorRule.hpp:46`), erase-then-append and the reverse search with an empty-selector fallback
  (`Hyprland-MonitorRuleManager.cpp:38,96-106`), the 1 px / 1 Hz closeness bound (`Hyprland-Monitor.cpp:836-837`),
  the 1/120 scale search (`Hyprland-Monitor.cpp:1001`), explicit positions placed before `auto`
  (`Hyprland-MonitorPositionController.cpp:27`), the five-decimal `refreshRate` and the `all` argument
  (`Hyprland-HyprCtl.cpp:242,320`), and the wiki's `sdr_eotf` key that only a `monitorv2` block reads
  (`wiki-Monitors.md:253`, `Hyprland-legacy-ConfigManager.cpp:819-831`)
  ([monitor rule](knowledge/hyprland-monitor-rule-r45.md), rows S302-S310 plus held S158/S162 under a second scope).
  The read-only join `tools/mado-monitors.py` prints one verdict per output (AGREE / DIFFER / DISABLED / UNRULED; top
  verdict NO_RULES 4, NOT_COMPARED 5, DIFFER 1, NO_MATCHING_MONITOR 3, OK 0) and reads AGREE/OK on this host: one
  rule, one output, 3440x1440@100 declared against 99.997 Hz reported, 0x0 and scale 1 on both sides. Still open:
  colour/HDR rendering and physical accuracy (the round-14 item, unchanged), output-management *apply* — a client's
  committed state overrides the chosen rule before it is applied (`Hyprland-MonitorRuleManager.cpp:45-84`) —
  `monitorv2` field parsing beyond `sdr_eotf`, and a `desc:` selector that matches only the long description, which
  the dump's short-only `description` cannot check. Nothing was applied: the 60 Hz default's mode choice and a
  fractional scale's correction were read, not exercised, and a runtime `hyprctl keyword` monitor override is outside
  both sides of the join.
```

The four open items are the seat spec's list, each with its ground: colour/HDR is `corpus/README.md:137-139`
(round-14 bullet, unchanged); output-management *apply* is the override the rule manager applies on top of the config
rule (`Hyprland-MonitorRuleManager.cpp:45-84`, entry §2); `monitorv2` parsing is the entry's `Limits` bullet 2; the
long description is `Limits` bullet 3 (the JSON carries `m_shortDescription` only,
`Hyprland-HyprCtl.cpp:277`, `Hyprland-Monitor.cpp:255-256`). "Nothing was applied" is the entry's §6 UNK paragraph:
both unexercised cases need a config change, which is the operator's; the runtime-`keyword` clause follows the same
paragraph (a `keyword monitor` override changes the applied state without touching any config file, so neither side of
the join sees it).

The held bullets at `corpus/README.md:128-132` and `:136-139` are **not** rewritten (append-only convention; the
round-21 correction at `:193-195` is the model for appended corrections). This subsection states the relation to them
instead. The form mirrors the round-43/44 tail subsections, as mapped by
`.ufo/waves/round-45/w1/ScoutFrontier/map.md` §2.

## 3. Phrase → ground

| row / frontier phrase | ground (recomputed this seat) |
|---|---|
| positional parse of mode/position/scale | `Hyprland-legacy-ConfigManager.cpp:1345-1347` |
| eight keys, other key drops the line | `Hyprland-legacy-ConfigManager.cpp:1352-1378` (keys at `:1352,1355,1358,1361,1364,1367,1370,1373`; `"invalid syntax"` return at `:1378`) |
| 60 Hz default | `Hyprland-MonitorRule.hpp:46` — `float m_refreshRate = 60;` |
| erase-then-append, reverse search, empty-selector fallback | `Hyprland-MonitorRuleManager.cpp:38`, `:96` (`std::views::reverse`), `:103` |
| exact name vs `desc:` short/long | `Hyprland-Monitor.cpp:1201-1211` (`matchesStaticSelector`, `selector.starts_with("desc:")` at `:1202`) |
| 1 px / 1 Hz closeness | `Hyprland-Monitor.cpp:836-837` (`DELTALESSTHAN(..., 1)`) |
| 1/120 scale search, 89 steps | `Hyprland-Monitor.cpp:1001` — `std::round(m_scale * 120.0)`; census `scale_step=1/120 scale_search=89` (`entry.md:72`) |
| explicit positions before `auto` | `Hyprland-MonitorPositionController.cpp:27` — `m->moveTo(*POS);` |
| five decimals, fields, `all` | `Hyprland-HyprCtl.cpp:242` (`"refreshRate": {:.5f}`), `:276-288`, `:320` (`vars[1] == "all"`) |
| `sdr_eotf` documented, read only by `monitorv2` | `wiki-Monitors.md:253`; `Hyprland-legacy-ConfigManager.cpp:819-831`, `:576` |
| verdict tokens and exits | `quality/counters/c1-r45-monitors.py` docstring + `registration.md` C1; `l1-draft/mado-monitors.py` `--help` mapping |
| host AGREE/OK, 99.997 Hz vs @100 | `.ufo/waves/round-45/receipts/live-monitors-host-l1.txt` (`MADO_MONITOR_OUTPUT ... verdict=AGREE`, `MADO_MONITORS ... verdict=OK`, exit 0) |
| apply override | `Hyprland-MonitorRuleManager.cpp:45-84` (`applyWlrOutputConfig`, `outputManagement->getOutputStateFor`) |
| short-only description | `Hyprland-HyprCtl.cpp:277` (`m_shortDescription`), `Hyprland-Monitor.cpp:255-256` |

Every locator above was produced by `grep -n` on
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/fetch/` (receipt `ScrReadme/locators.txt`) and
re-asserted by `ScrReadme/check-locators.py` (output `ScrReadme/locators-check.txt`).

## 4. Deliberately not claimed

- The row does not say the tool *verifies* Hyprland: it scores the join of config text and one dump; a DIFFER can be
  a client's committed state or a stale dump (entry §2, Limits 1).
- The Frontier bullet does not close "output-management behavior" (`corpus/README.md:131`) or "colour/HDR" /
  "physical accuracy" (`:137-139`); it moves the read half of the monitor rule and leaves apply, colour and the
  `monitorv2`/long-description fields open by name.
- No serial, monitor description, window title, process table or home-directory listing appears in either block; the
  host values used are the declared mode and the reported rate, position, scale, transform, disabled and mirror,
  which are the receipt's projected fields.
- The row's 99.997 Hz is the receipt's number, not a fresh probe by this seat: no host command was run here.

## 5. Checks run by this seat

- `ScrReadme/locators.txt` — `grep -n` output for every locator cited above, on the pins under
  `.ufo/waves/round-45/fetch/`.
- `ScrReadme/check-locators.py` → `ScrReadme/locators-check.txt` — re-reads each cited `file:line` and requires its
  expected token (34 PASS), then asserts the drafted row is one line with three cells, no inner pipe, the clause-f
  prefix, source cell `S302-S310`, and no serial field (`SUMMARY failures=0`).
- `ScrReadme/gate-clone.txt` — the drafted row applied in place of `build-pos.py`'s placeholder on a scratch clone of
  the freeze (`git clone --shared` → `checkout --detach 22a8dedd…` → `build-pos.py` → row replaced at
  `corpus/README.md:73`, commit `7e6e2ed41956b54dcbc00aa07828715a4d2bf725`), then:
  - `quality/check-index.py --repo D --rev HEAD` → `MADO_INDEX: ... indexed=62/62 missing=0 dangling=0
    duplicates=0 coverage=10.0000/10`, exit 0;
  - `quality/check-index-rows.py --repo D --rev HEAD` → `MADO_INDEX_ROWS: rows=62 errors=0 warns=3`, exit 0; the three
    warns are pre-existing `cited-glob-nomatch` lines on other rows (`window-rule-effects-getprop.md`,
    `config-drift-r12.md`, `rule-attribution-r24.md`), not `holds-no-overlap` on this row — the Holds cell shares no
    ≥5-word sequence with the note's own bytes;
  - `quality/counters/c2-r45-monitor-entry.py --repo D --rev HEAD --base 0c89478a…` →
    `PRED-C2-r45: admitted=1/1 verdict=TARGET_MET rev=7e6e2ed4…`, exit 0, `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1
    i:1 j:1` — the drafted row satisfies clause f.

Not run: the C1 counter, the tool, any host or compositor probe; no tracked lane file was edited. The Frontier text is
read by neither counter — its check is the locator receipt above.
