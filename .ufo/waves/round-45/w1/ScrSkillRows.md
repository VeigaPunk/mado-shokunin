# w1/ScrSkillRows — SKILL.md additions for `tools/mado-monitors.py` (round 45)

Deliverable: `.ufo/waves/round-45/w1/ScrSkillRows/skill-rows.md` — append-ready text, four blocks, each naming the exact
`SKILL.md` line it goes after. No `SKILL.md` edit: the L1 is the integrator.

## Behavior

Read (not edited): `SKILL.md:142-160` (Claim-first routing table), `:204-226` (Read-only probes table), `:246-313`
(§ "Rule size versus reported size" — the `mado-geometry` precedent: prose, per-verdict licence table, exit map, known
limit), `.ufo/waves/round-45/l1-draft/mado-monitors.py:1-140` + its `report`/`selftest`/`run` bodies, `l1-draft/entry.md`,
`.ufo/waves/round-45/registration.md`, `.ufo/waves/round-45/receipts/live-monitors-host-l1.txt`, and the nine pins in
`.ufo/waves/round-45/fetch/`.

Wrote, in the SKILL's existing shapes:

- **Block A** — one Claim-first routing row (four columns `| claim | route to | run | tag |`), goes after `SKILL.md:158`.
  Tag splits `[OBS]` for both printed sides from `[INF]` for the rule the tool *chose*, and `[UNK]` for rendering.
- **Block B** — one Read-only-probes row (three columns `| Probe | Answers | Sample |`), goes after `SKILL.md:225`, with
  the L1's live sample quoted verbatim.
- **Block C** — new § "Monitor rule versus running output", goes after `SKILL.md:313` (before `### Mutating commands`):
  contract paragraph, support ceiling, the tolerance derivation with pin locators, the decision table
  `question | verdict/field | what it proves | what it does not` (8 rows: AGREE, DIFFER, DISABLED, rule=/UNRULED,
  NOT_COMPARED, NO_MATCHING_MONITOR, NO_RULES, `desc:` unmatched), the exit-map line, four licence bullets
  (join-not-blame / runtime overrides / `desc:` long form / `monitorv2` → NOT_COMPARED), the host run block and known limits.
- **Block D** — a locator receipt table (not SKILL text) for the integrator's re-check.

## Gates run by this seat

| gate | command | result |
|---|---|---|
| locator truth (33 locators) | `python3 -I .ufo/waves/round-45/w1/ScrSkillRows/verify-locators.py` | `LOCATORS: checked=33 failed=0`, rc 0 — every cited `pin:line` was re-opened and the row's backticked token found inside that line or range |
| draft artefact truth | `python3 -I .ufo/waves/round-45/w1/ScrSkillRows/verify-draft.py` | `DRAFT: checked=1 failed=0`, rc 0 — the three quoted `MADO_MON*` lines are verbatim lines of the L1 receipt; `~/.config/hypr/monitors.conf:10` is the quoted rule; the draft's verdict chain and summary format are verbatim substrings of the reference docstring; every decision-table row has exactly four cells |

Receipts: `…/w1/ScrSkillRows/receipts/locators.txt`, `…/draft-check.txt`, `…/v2-differ-precedence.txt`.

Both scripts live in the seat dir and are re-runnable as written; they read the pins, the draft and the L1 receipt only.

## Findings

**F1 — NOT_COMPARED outranks DIFFER, and the first draft had it backwards.** I wrote, from the docstring's exit list,
that "a dump with a differing output still exits 1". A run of the L1 reference on a scratch fixture carried the opposite:
config `monitorv2 { output = DP-1 }` + `monitor = DP-1, 1920x1080@60, 0x0, 1` against a dump reporting 3440x1440@99.997 prints
`MADO_MON_OUTPUT: … differ=mode verdict=DIFFER` and then
`MADO_MONITORS: … differ=1 … verdict=NOT_COMPARED`, exit 5
(`receipts/v2-differ-precedence.txt`). The docstring's chain places NOT_COMPARED before DIFFER; the per-output lines keep
their own verdicts. Block C now states this and the licence bullet no longer claims the top verdict "never reads as DIFFER".
Attacks: the first draft's NOT_COMPARED row and its fourth licence bullet. Supports: the reference's own order
(`mado-monitors.py:85-88`, quoted verbatim in `verify-draft.py`'s assertion).

**F2 — two locators I had typed from `entry.md` were off by a line boundary.** `Hyprland-legacy-ConfigManager.cpp:1345`
holds only `parseMode`; `parsePosition`/`parseScale` are `:1346-1347`. `Hyprland-MonitorPositionController.cpp:27` holds
`m->moveTo(*POS)`; `arranged.push_back(m)`/`erase` are `:28-29`. Both corrected to ranges and re-passed. This is exactly what
`verify-locators.py` is for; the entry's own citations are ranges that already covered these lines, so the entry is not
wrong, only my narrowed singletons were.

**F3 — `--selftest` hermeticity is a code fact, not a docstring fact.** The docstring never says "hermetic"; the selftest
at `mado-monitors.py:455-510` builds its cases as inline strings and calls `report()` directly, plus three setup cases on
`/nonexistent` paths. Block C therefore says "runs built-in fixtures only, reading no file and no host surface" with that
range cited, instead of borrowing SKILL's `hermetic` word for `mado-geometry`.

**F4 — the `desc:` licence row is the one place the tool's own model is provably partial.** The dump prints
`m_shortDescription` as `description` (`Hyprland-HyprCtl.cpp:277`), while the selector test reads both forms
(`Hyprland-Monitor.cpp:1206`). An unmatched `desc:` therefore cannot be read as a dead rule; Block C says so and points at
`make`/`model`/`serial` in the same dump as the only way to check.

## Touched surfaces

- `.ufo/waves/round-45/w1/ScrSkillRows.md` (this report)
- `.ufo/waves/round-45/w1/ScrSkillRows/skill-rows.md` (deliverable)
- `.ufo/waves/round-45/w1/ScrSkillRows/verify-locators.py`, `verify-draft.py`
- `.ufo/waves/round-45/w1/ScrSkillRows/receipts/{locators.txt,draft-check.txt,v2-differ-precedence.txt}`
- Scratch `/fast/scratch/hyaku/mado-r45/ScrSkillRows/` (fixtures + `locators.txt`); deleted before hand-off.
- Not touched: `SKILL.md`, the reference, counters, controls, registration, pins, `corpus/`, any git index.

## Out of scope (deliberate)

- Installing `tools/mado-monitors.py`, or scoring `c1-r45-monitors.py` / `c2-r45-monitor-entry.py`. The seat spec is SKILL
  prose; the counters are the C1/C2 seats' and the L1's.
- Any host probe. The only live material quoted is the L1's own receipt, cited as received, not re-run.
- `corpus/knowledge/hyprland-monitor-rule-r45.md` rows S302-S310 — the entry's business.

## Limits

- The decision table's `[INF]` framing (rule selection is a source re-implementation) is a reading of
  `Hyprland-MonitorRuleManager.cpp:96-107` at `efb50993`; it is not corroborated by a compositor-side disclosure, because
  Hyprland does not print the rule it chose.
- Block C's known-limits paragraph says the multi-output, mirror, transform and fractional-scale branches are exercised only
  by `--selftest` fixtures here — one output on this host. That is `[OBS]` from the receipt (`outputs=1`).
- The draft asserts nothing about rendering or about a rule's effect after a config change; both stay `[UNK]` by design.
- Tooling: nothing installed, nothing upgraded. pytest not used; both verifiers are stdlib-only `python3 -I`.
