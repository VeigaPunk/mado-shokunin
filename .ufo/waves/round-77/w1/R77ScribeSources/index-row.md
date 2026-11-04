# index-row.md — seat R77ScribeSources (round 77)

Two artifacts for `corpus/README.md`: one coverage-map row and one Frontier bullet, drafted
for the L1. Both are already present in the committed README at the landing tip
(`3e35d0a9`); this draft matches them verbatim and records the verification.

## 1. Coverage-map row (the `| Note | Holds | Sources |` table)

| `knowledge/bar-footprint-r77.md` (MADO-R77-1, round 77; covers C1) | The bar-footprint chain as one join: waybar's declared position/layer/height/width/margin/exclusive -> Hyprland's arrange (desired size, anchors, margins, exclusive zone) -> the live layer box in `hyprctl layers -j` -> the monitor's `reserved` band -> usable area. Host join 2026-11-04: DP-1 3440x1440@99.997, waybar level 2 at 0,0,3440,26, reserved `[0,26,0,0]`, usable area y=26..1440. Tool `tools/mado-barfoot.py` (read-only, exit map 0 CLEAN / 1 DIFFER / 2 SETUP / 3 NOT_FORMED) predicts the box from the declaration and separates MATCH from drift; five named join mutations killed 5/5; the live-echo control scores 8/15; margined exclusive bars and scaled/transformed monitors are named UNMODELLED. | `source:` S457, S458, S459, S460, S461, S462 in [SOURCES](SOURCES.md) (S463 rejected); evidence `.ufo/waves/round-77/fetch/`, receipts `.ufo/waves/round-77/receipts/`; recheck on-release. |

Verification: `quality/check-index.py` reported `indexed=96/96 missing=0 dangling=0
duplicates=0` at `3e35d0a9` (committed interim measurement); the SCORECARD round-77 block
carries 95/95 at base → 96/96 at tip.

## 2. Frontier bullet (the `## Frontier` list, newest first)

- Round 77 moves the bar's footprint onto measured ground ([bar footprint](knowledge/bar-footprint-r77.md); rows S457-S462 new, S463 opened and rejected): the declared waybar placement (position, layer, height, width, margin, exclusive) is joined to the live layer box in `hyprctl layers -j` and to the monitor's `reserved` band on this host (DP-1 3440x1440@99.997; waybar level 2 at 0,0,3440,26; reserved [0,26,0,0]; usable area y=26). A read-only tool (`tools/mado-barfoot.py`) predicts the box from the declaration, separates agreement from drift on a frozen 15-case set (15/15; five named mutations killed; live-echo control 8/15), and names what it cannot model (margined exclusive bars; scaled/transformed and dynamic-cross monitors refused). The SKILL.md read-only probe table becomes an executable runbook: 12 frozen expectations, each bound to its committed row, 12 executed / 12 matched / 0 unexecuted (read-the-table control: executed=0). Still open: the gtk-layer-shell auto-zone composition with non-zero margins, which surface set a level-0 zone, and any runtime change after capture.

The landed bullet at `corpus/README.md:133` matches this text in substance (same claims and
numbers); the seat draft only expands the runbook sentence — the L1 keeps the landed
shorter form or adopts this one; either is consistent with the measured receipts.
