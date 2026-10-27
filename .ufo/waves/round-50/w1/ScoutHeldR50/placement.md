# Placement findings: Hyprland bind-key-match

## Held-ground restatements in the round-49 candidate

Candidate citations below are the candidate's own locator lines; held-source locations are literal line ranges in the named note. Each pair is a held claim/statement reused as context rather than new S-row evidence.

| Candidate line | Held source / line | Restated held sentence or claim |
|---|---|---|
| 15 | `corpus/knowledge/keybind-rule-semantics.md:106` | Key-field forms (keysym, XF86, keycode, wheel, switch, mouse) were documentary `[INF-docs]` semantics only. Candidate restates this as key forms standing at `[INF-docs]` level. |
| 16 | `corpus/knowledge/keybind-rule-semantics.md:104-105` | The key-name interpretation and `resolve_binds_by_sym` determine the keymap/layout relation; candidate cites held S318/S319 for the compositor's default/fallback. |
| 16 | `corpus/knowledge/hyprland-input-devices-r46.md:71` | Per-device layouts do not change the keymap binds resolve against unless `resolve_binds_by_sym = 1`; the input-device join does not check binds. Candidate's line 19 explicitly paraphrases this as bind resolution outside the join. |
| 19 | `corpus/knowledge/keybind-rule-semantics.md:106` | The documented key-field forms remain `[INF-docs]`; repeated in the ground paragraph. |
| 19 | `corpus/knowledge/hyprland-input-devices-r46.md:71` | Bind resolution is outside the round-46 join; repeated in the ground paragraph. |
| 19 | `corpus/knowledge/xkb-keymap-compile-r48.md:17` | Held S318/S319 are the compositor's default and failed-compile fallback; candidate's “neighbours cited here and never re-claimed” carries this held context. |

Note: candidate lines 15-16 also point to held source rows, but are not full-sentence quotations from the three target knowledge notes; the table pairs claims and paraphrases rather than pretending these are verbatim matches. The candidate's references to S318/S319 reuse the already-held registry rows; the new matcher material is supported by S352-S363.

## README placement

Coverage-map row, following the existing round-48 row, with the same three-column format:

`| \`knowledge/hyprland-bind-key-match-r50.md\` (MADO-R50-1, round 50; Hyprland bind-key matching) | How Hyprland 0.56.2 turns the bind KEY field into a match against a pressed key: parser forms, keysym resolution and case handling, the selected XKB state/layout, modifier-mask comparison, keycode and non-keyboard paths, branch order and shadowing; grounded in pinned Hyprland/libxkbcommon/wiki rows and this host's shape-only bind capture. Held S318/S319 are cited, not re-registered. | rows S352-S363 plus held S318/S319 |`

Frontier row: insert at line 112 after the round-48 bullet (or immediately following it), before the round-46 bullet:

`- Round 50 moves Hyprland bind-key matching onto sourced ground ([bind-key match](knowledge/hyprland-bind-key-match-r50.md), rows S352-S363; held S318/S319 cited, not re-claimed): how the 0.56.2 parser stores the KEY field, how key names resolve to keysyms, which XKB state supplies the pressed keysym, and how modifier masks and keycode/non-keyboard branches determine a match. The live receipt is shape-only; it does not exercise a key press or dispatcher.`

## SKILL.md placement

Use the existing `## XKB keymap compile (round 48)` section at lines 2226-2237 as the single placement: append a pointer immediately after its knowledge-entry sentence at line 2237, rather than creating a second bind section. Proposed text:

`For what a Hyprland bind's KEY field matches at runtime (including keysym resolution, selected XKB state, and modifier-mask comparison), see [bind-key matching](corpus/knowledge/hyprland-bind-key-match-r50.md) (rows S352-S363; held defaults/fallback S318/S319).`

Evidence basis: candidate locator lines 15-19; README coverage row 76 and Frontier lines 109-115; SKILL.md lines 2226-2237; held-source lines `hyprland-input-devices-r46.md:71`, `xkb-keymap-compile-r48.md:17`, and `keybind-rule-semantics.md:103-109`; registry rows S318/S319 at `corpus/SOURCES.md:267-268`.