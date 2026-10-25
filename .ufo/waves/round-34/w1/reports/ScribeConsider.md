# ScribeConsider — report

**Seat:** leaf member, no dispatch. **Date:** 2026-10-24.
**Deliverable:** `.ufo/waves/round-34/scratch/ScribeConsider/note.md` (written, 4824 B).

## Proposal mined

`considerthese/2026-10-24.md`, §"Self-improvement suggestions (proposals only; not acted on)",
item 4 (line 49): read `PROVINCE.md` and propose the next Hyprland config table (window
rules, monitors, layer rules) with grounding sources. File untouched, per instruction.

## Grounding — what was opened (the thing the proposal points at, not the text)

- `PROVINCE.md` — owned surfaces + tool inventory.
- `corpus/SOURCES.md` — window-rule source rows S017/S030, S154–S160, S162, S168; layer-rule
  S163/S166; zero dedicated monitor rows.
- Host, first-hand (Hyprland 0.56.2 `efb5099`):
  - `hyprctl windowrules -j` / `layerrules` / `rules` → **`unknown request`** — no rule-table
    oracle on v0.56.2.
  - `hyprctl monitors -j` → live JSON table, 36 fields; `hyprctl workspacerules -j` works
    (confirms the r27 premise). `hyprctl help` is not a verb.
  - Declared-line census of `~/.config/hypr` + `~/.local/share/omarchy/default/hypr`:
    windowrule ×78, monitor ×1 (`monitors.conf:10`), layerrule ×2, workspace ×0.

## Verdict per candidate

- **Window rules:** biggest surface, but no `hyprctl` oracle — the r25–r27 predict-table
  method cannot transfer; oracle would be `clients -j`/`getprop` attribution (route already
  documented in `window-rule-effects-getprop.md`, `rule-attribution-r24.md`). Different claim
  shape — must be re-scoped, not assumed.
- **Layer rules:** 2 lines, no oracle — not worth a round.
- **Monitors:** only candidate with a live JSON oracle and declared bytes, but tiny (1 line)
  and mostly runtime-only fields; the honest cheap next table.

## Disposition

**Lesson**, not a QUALITY.md criterion and not a SOURCES row — the evidence is host probes
plus existing S-rows; the finding is planning knowledge (oracle availability per table), not
a rubric or a new external source.

## Bonus defect found while grounding

`PROVINCE.md` "Round-23 refinement" claims its table covers every tracked `tools/` file, but
`tools/mado-wsrules.py` (r27) has no row. Named here, not edited (operator-side surface).
