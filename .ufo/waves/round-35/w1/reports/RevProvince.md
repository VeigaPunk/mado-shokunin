# RevProvince — PROVINCE.md scope check on the three adopted entries

Date: 2026-10-24. Reviewer: wave-1 RevProvince seat. Lane bounds: leaf member, no
subagent dispatch used.

Read: `PROVINCE.md` (all clauses incl. round-19, round-23, round-23 wave-2,
round-25 and round-27 append-only corrections); the three entries
(`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/idle-lock-never-asked-r12.md`,
`idle-lock-chain-armed-r14.md`, `idle-lock-offered-in-the-bar-r15.md`); the eight
adopted source rows `.ufo/waves/round-35/controls/golden/corpus/SOURCES.md`
S203–S210; sibling `PROVINCE.md` files of tsukuroi, mori, kumitate, souji,
chousa, kaidoku, kagi, kama, kengaku, tabi, kake, kotoba, revenger, lore,
kasegi, kotodama, audio, tameshi (grepped for `omarchy`, `local/share`,
`local/state`, `first-run`, `idle`, `hypridle`, `journalctl`, `toggles`,
`waybar`, `walker`).

**Governing frame:** the lane owns surfaces read-only — "All config trees are
READ-ONLY for this lane: probe, measure, recommend — the operator applies
changes" (`PROVINCE.md:12-13`). IN/OUT below therefore means in/out of the
lane's **probe-and-record domain**, not a write surface; mado has no host write
surface either way.

## The two named surfaces

### The desktop's own toggle menu — mado's evidence surface, not a sibling's

`~/.local/share/omarchy/bin/omarchy-menu` (S208/package-S337) and
`~/.local/share/omarchy/bin/omarchy-first-run` (S203/S315) live in the omarchy
checkout. Round-19 refinement (`PROVINCE.md:18`) resolves this tree already:
"`~/.local/share/omarchy/**` (checkout) is read-only source evidence for this
chain." The clause grants the whole checkout as read-only evidence — `bin/` and
`default/` are not carved out. The same clause's OUT list covers "every
omarchy program update, theme write or consumer reload": **reading the menu's
bytes is IN; running or altering it is OUT.** Domain clause also applies — the
menu is the desktop's own control surface for screen/idle toggles
("display behavior", `PROVINCE.md:3-4`). No sibling claims it: tsukuroi's
ADJ-03 affirmatively routes "menu or idle behavior … configuration-level
diagnosis" to mado (`tsukuroi-shokunin/PROVINCE.md:48`), and the only other
`omarchy` hit in any sibling province is kotoba noting mado's skill-file
frontmatter facet (`kotoba-shokunin/PROVINCE.md:61`) — the `~/.agents/skills/`
documentation surface, a different object.

### The bar's indicator script — mado's evidence surface, not a sibling's

`~/.local/share/omarchy/default/waybar/indicators/idle.sh` (S207/S336) is the
`exec` target of `custom/idle-indicator` in the owned `~/.config/waybar/` plane
(S206, verified at `config.jsonc:207-212`). Two clauses cover it: Owns
`~/.config/waybar/` (`PROVINCE.md:6`) makes the module itself owned; the
script it points at is chain evidence under the round-19 precedent (`mako.ini`,
`swayosd.css`, `btop.theme`, `neovim.lua` are "chain evidence only, their
consumer configs not owned", `:18`) and under the same round-19
checkout-evidence grant as the menu. Same caveat: reading IN, executing or
updating OUT.

Neither surface belongs to a sibling. Both are mado's — as evidence, never as
an absorbable or writable surface.

## Per-entry verdicts

| Entry | Surfaces read | Verdict | Clause relied on |
|---|---|---|---|
| `idle-lock-never-asked-r12.md` | `~/.local/share/omarchy/bin/omarchy-first-run` (S203); journal count of `omarchy-toggle` invocations and `~/.local/state/omarchy/toggles/hypr/` flag listing (S204) | **IN PROVINCE** | Round-19 checkout-evidence clause (`:18`) for the script; domain clause (`:3-4`, "screen/idle behavior … display behavior") for the probes — all read-only, answering a display-behavior question |
| `idle-lock-chain-armed-r14.md` | `pgrep hypridle`/`pgrep hyprlock`, `systemctl --user is-active hypridle`, journal start lines, `hypridle.conf` timeouts (S205) | **IN PROVINCE** | Owns `~/.config/hypr/` (`:5`) for the declared timeouts; domain clause for daemon liveness. Boundary already drawn by the round-23 wave-2 correction (`:32`): unit-*health* ground stays tsukuroi's — the entry reads `is-active` to explain an idle-chain measurement artefact, not to pronounce unit health |
| `idle-lock-offered-in-the-bar-r15.md` | `~/.config/waybar/config.jsonc` + four `.bak*` copies (S206, S209); `idle.sh` (S207); `omarchy-menu` (S208); `~/.local/state/omarchy/toggles/hypr/` (S210) | **IN PROVINCE** | Owns `~/.config/waybar/` (`:6`) outright for the live config and its dated copies; round-19 checkout-evidence clause (`:18`) for the two omarchy-checkout scripts; domain clause for the toggle-state directory |

## Notes for the record

- `~/.local/state/omarchy/toggles/hypr/` (S204/S210) is the one surface no
  clause names explicitly. It is the desktop's own toggle-state record inside
  the declared domain, read-only. Verdict: in-province **as evidence**,
  same status as the checkout — probe and cite, never absorb. If a future
  round wants it enumerated, that is a PROVINCE.md append, not an expansion of
  ownership.
- Journal reads appear in all three entries' evidence. Boundary confirmed:
  tsukuroi owns journal/boot *triage* (`tsukuroi-shokunin/PROVINCE.md:11`) and
  mori owns OOM/coredump journal classification; neither claims the
  `omarchy-toggle` invocation history or session start lines, and mado's own
  wave-2 correction already runs journal probes beside tsukuroi's ground.
- Nothing in the three entries touches the Refuses list (`PROVINCE.md:14-16`):
  no secrets, no model endpoints, no model quality.

**Bottom line:** all three adopted entries are IN PROVINCE. The menu and the
indicator script are mado's surfaces — read-only evidence surfaces under the
round-19 checkout clause and the domain clause — not a sibling's.
