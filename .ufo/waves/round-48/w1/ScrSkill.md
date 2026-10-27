# ScrSkill — SKILL.md sections for round-48's two planes

STATUS: **complete** (2026-10-26). Seat dir `.ufo/waves/round-48/w1/ScrSkill/`. Scratch
`/fast/scratch/hyaku/mado-r48/ScrSkill/` created and **deleted** (`rm -rf --`, verified absent; the
remaining `/fast/scratch/hyaku/mado-r48` dirs belong to other seats).

## Behavior

`section.md` (130 lines, 32 table-row lines) holds the two paste-ready SKILL.md appends:

- `## XKB keymap compile (round 48)` — intro (what the compile does and what it does not reproduce),
  a 14-row host matrix (names → rc → stderr → keymap size/md5), the include-path list as the compiler
  itself prints it, a run recipe, and a 7-row symptom → first read → rule → next step table
  (keyboard prints `us`; layout name unknown; variant unknown/ignored; option silently ignored; model
  changes nothing; custom layout in `~/.config/xkb`; variant-count mismatch). C2's compile is grounded;
  the compositor's fallback to `us` is cited from round 46 (rows S318/S319) and never re-claimed.
- `## Terminal cache (round 48)` — the warm-cache path as the pinned resolver implements it, the three
  shapes where SUPER+RETURN starts a command the files no longer name, the read-only check
  (`tools/mado-terminal.py explain`, `cache=`), and the operator-owned clear. 8-row symptom table
  (`cache=hit` divergence, same-size/same-minute edit, removed `TryExec`, changed `X-TerminalArg*`,
  `stale`, `invalid`, `disabled`, tool-vs-hotkey argv).

Seven `<AFTER: …>` markers name exactly the values that only the landed w1 work supplies (listed below).

## Gates

| gate | command | result |
|---|---|---|
| every quote/fragment is at the file:line the section cites | `python3 .ufo/waves/round-48/w1/ScrSkill/verify.py` | `RESULT PASS checks=44 failed=0` (`receipts/section-verify.txt`, sha256 `8f2f3f60…`) — the pin sha256 plus 43 fragment locators across the pinned resolver, this seat's receipts, the two host config files and the lane files (`SKILL.md`, `corpus/`, `tools/`) |
| section shape | same script | 2 `##` sections, names as specified; 7 `<AFTER>` markers |
| resolver pin | `sha256sum` | `.ufo/waves/round-47/fetch/xdg-terminal-exec` = `/usr/bin/xdg-terminal-exec` = `89f2be9a…27ac` (`receipts/resolver-cache-locators.txt`) |

The verifier re-ran to the same PASS on every edit; no gate depends on a scratch path.

## Touched surfaces

Created (nothing else written, nothing edited):

- `.ufo/waves/round-48/w1/ScrSkill.md` (this report)
- `.ufo/waves/round-48/w1/ScrSkill/section.md` — sha256 `9c1ae33922af9a056bd74e4916f801e42585a1c6c05d98c52b7983967c5bcc63`
- `.ufo/waves/round-48/w1/ScrSkill/verify.py` — sha256 `4944d54c…` (stdlib only, absolute paths, read-only)
- `.ufo/waves/round-48/w1/ScrSkill/receipts/xkbcli-matrix.txt` — sha256 `f84c1221…`
- `.ufo/waves/round-48/w1/ScrSkill/receipts/resolver-cache-locators.txt` — sha256 `39eba269…`
- `.ufo/waves/round-48/w1/ScrSkill/receipts/section-verify.txt` — sha256 `8f2f3f60…`

Read only: `SKILL.md`, `corpus/README.md`, `corpus/knowledge/hyprland-input-devices-r46.md`,
`corpus/SOURCES.md` (S318/S319 rows), `tools/mado-terminal.py`, the round-47 pin,
`~/.config/hypr/input.conf`, `~/.config/hypr/bindings.conf`, `claims.md`. No lane file was modified —
the L1 is the integrator.

## Facts measured this seat (the section's numbers)

Read verbs only: `xkbcli --version`, `xkbcli compile-keymap`, `xkbcli list`; nothing else was executed
against the host.

- `xkbcli 1.13.2`; libxkbcommon 1.13.2-1, xkeyboard-config 2.48-1 (echoed in the receipt; also stated by L1).
- `--layout br --options compose:caps` → rc 0, 73079 B keymap; `--layout br` → rc 0, 73043 B.
- `--layout zz` and `--layout br,zz` → rc 1, `[XKB-338] Couldn't find file "symbols/zz" in include paths`.
- `--rules nope --layout br` → rc 1, `[XKB-338] Couldn't find file "rules/nope" in include paths`.
- `--layout br --variant nope` → rc 1, `[XKB-661] Couldn't process include statement for 'br(nope)'` +
  `Failed to compile xkb_symbols`.
- `--layout br --options nope` → rc 0, `[XKB-595] Unrecognized RMLVO option "nope" was ignored`, keymap
  identical to `--layout br` (md5 `f73b560f…`); `compose:caps,nope` → the host keymap byte for byte, so a
  valid option beside an invalid one still applies.
- `--layout br --model nope` → rc 0, **no stderr**, keymap identical to `--layout br` — a bogus model is
  silently accepted (new detail, not in L1's summary).
- Variant alignment is positional: `us,dk` + `intl` → rc 0 (77943 B), `us,dk` + `,winkeys` → rc 0
  (76323 B), `us,dk,br` + `intl,winkeys` → rc 0 (82427 B); `--layout br --variant intl,nope` → rc 1
  `Less layouts than variants: "br" vs. "intl,nope".`
- Include paths in the compiler's own error: 1 searched `/usr/share/xkeyboard-config-2`; 3 "could not be
  added": `$HOME/.config/xkb`, `$HOME/.xkb`, `/etc/xkb`.
- Compile needs no display: rc 0 with `DISPLAY`/`WAYLAND_DISPLAY`/`XDG_SESSION_TYPE` unset.
- `xkbcli list` catalogue: `models:` at line 1, `layouts:` at line 555, 5101 lines; 9 `br` rows (base
  `variant: ''` + 8 variants), 0 `zz` rows, **no options section** — so an option name has no catalogue.
- Resolver cache locators (computed, in the receipt): file `:173`, default `:172`, hash input `:194-201`,
  line limit 50 `:223`, terminator `:247-251` / written `:332`, trust test `:274`, read gate `:1179`,
  cold branch `:1183-1209` (so `find_entry` is never reached on a hit), print bail-out `:1368-1376`,
  arg composition `:1400-1409`, save `:1455-1457`, `XTE_CACHE_ENABLED` default `:1172`, `/disable_cache`
  `:380`, removal when disabled `:337`.

## Findings for the L1

1. **Placement**: append both sections after `## Terminal selection (round 47)` (SKILL.md:2155 to EOF),
   keeping the blank-line separation the file already uses.
2. **Superseded row**: the round-47 table row `a change has no effect` (`SKILL.md:2213`) describes the
   cold-only tool. The new section says so in its notes; the L1 may either leave the old row in place
   (history) or strike it — the new text does not assume either.
3. **Round-46 row cross-reference**: `SKILL.md:2128` (`FALLBACK`) is the row the XKB section sends the
   reader to first. Nothing in it changes.
4. **Two facts L1's summary does not carry** and that the freeze may want in the C2 rows: the unknown
   **model** is accepted with no message at all (not "warning"), and `xkbcli list` exposes
   models+layouts but **no options**, so "which options exist" has no catalogue answer on 2.48.
5. **One inference flagged**: the user-paths-before-system-root order is `[INF]` from the order of the
   compiler's two lists, not from a source line — `<AFTER>` names the w1 source seat as the place that
   line should come from.
6. **Seat deviation, disclosed**: the receipt echoes `pacman -Q libxkbcommon xkeyboard-config` (one
   read-only query, no transaction, no lock, no sync, no install; the versions were already given by L1
   and the section does not cite the query). No other package-manager or host-service call was made; no
   `xdg-terminal-exec` run at all (so no cache was written anywhere), no compositor verb, no terminal.

## Out of scope (by the seat spec, not done here)

- `corpus/knowledge/xkb-keymap-compile-r48.md`, the SOURCES rows S340.., and any C1 tool change — other
  w1 seats own those; this seat wrote text that points at them.
- No CHANGELOG/MANIFEST/state edit; no git/jj mutation; no judge or counter run.

## `<AFTER>` items the L1 must fill at integration

| where | needs |
|---|---|
| XKB intro | the landed knowledge entry path and its row numbers (S340..) |
| XKB include-path paragraph | the libxkbcommon line fixing path order/prefixes (w1 source seat) |
| XKB option row | whether 2.48 ships any options listing |
| XKB `~/.config/xkb` row | the libxkbcommon prefix rules for the user paths |
| Terminal `explain` paragraph | the landed `cache=` spelling, the tool's selftest count, the warm-case receipts |
| Terminal notes | the landed round-47 D1 lesson line (HOME unset) |
| Terminal ground line | the warm-cache SOURCES row numbers |
