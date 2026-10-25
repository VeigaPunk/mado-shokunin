# ExecQuarantineSlice — round 39 w1 report (mado quarantine slice)

## Scope
Hand-check the mado slice of the absent-defect-register; write verdicts; do not edit the register or any
campaign file. No tools were installed (used existing `python3`, `curl`, `tar --zstd`, `awk`, `grep`).

## Register location note
Task gave `/home/vgpnk/Projects/shokunin/.ufo/waves/corpus-expansion-1/absent-defect-register.md`; that path
does not exist (awk exit 2, 0 rows). The register actually lives under **`shokuknow`**:
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`. Slice regeneration
with the corrected path succeeded (`exit=0 rows=13`).

## Slice extraction (13 rows)
```
A=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-39/w1/ExecQuarantineSlice
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" > $A/quarantine-slice
```
Rows: S189 S195 S201 S205 S224 S228 (class `payload-absent`); S199 S200 (class `unreachable`,
source-unfetchable); S209 S222 S223 S225 S235 (gate block named no locator).

## Hand-check results (per-row)
- **S189 — PRESENT.** `curl -sL` of the cited commit `…/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp`
  → 192 lines. `grep -n 'eventString = std::format'` → **line 128**:
  `auto eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));` inside `formatEvent`. Match.
- **S195 — PRESENT.** `tar --zstd -tf` on the cited package (8,575,462 B, 1,362 members) → member
  `usr/share/doc/arch-wiki-zh-cn/html/zh-cn/Hyprland.html` exists; extracted it alone (extract exit 0). After
  strip-tags + collapse-whitespace, both registered sentences found **verbatim** (`found=True` for both).
- **S201 — PRESENT.** `curl -sL https://arxiv.org/html/2604.18860v1` (243,019 B). Plain-text normalization:
  quote 1 at idx ~8414, quote 2 at idx ~52076–52169, including `governed by X11/Wayland compositors` and
  `can redirect agent actions with up to 100% success rates` (register `---` = em dash).
- **S205 — PRESENT.** Fetched siteinfo JSON; `grep -n 'zh-hans|zh-hant|archlinuxcn'` → zh-hans
  `"prefix"`/`"url"` at JSON lines 414/418; zh-hant at 421/425 with `https://wiki.archlinux.org/title/$1_(正體中文)`.
- **S224 — ABSENT (refused).** `grep -c '2026-10-23T22:52:44Z' /home/vgpnk/.cache/ai-usage/status.json` → 0
  (exit 1); only `"updated_at": "2026-10-25T19:05:31Z"` present. Compiled JSON walk confirms a single
  `updated_at`. Same grep in `inception-ledger.json` → 0. Live telemetry file rotated; quote bytes no longer exist
  anywhere in the cited source. Refused.
- **S228 — PRESENT.** `grep -n '模板:过时' lanes/mado/round5/fetch/cn-export-hyprland.html` → **line 1519**
  (category link, text `使用“模板:过时”标记的页面或章节`; matches register quote modulo curly/straight quotes).
- **S199 / S200 — UNREACHABLE.** Re-fetch of both CSDN URLs now returns HTTP **521** with anti-bot JS shell
  (2,156 B / 2,232 B; no article content). No quote was recorded for either row → nothing to locate. Marked
  unreachable, not fabrication.
- **S209 / S222 / S223 / S225 / S235 — UNREACHABLE.** Register rows consist only of `## Gate — Sxxx` with no
  locator and no quote; nothing to hand-check.

## Verdict tally
- Present, hand-checked (appendable): **S189, S195, S201, S205, S228** — 5.
- Absent, refused: **S224** — 1.
- Unreachable (unverifiable class, no fabrication): **S199, S200, S209, S222, S223, S225, S235** — 7.

## Files written (lane repo only)
- `.ufo/waves/round-39/w1/ExecQuarantineSlice/quarantine-slice` (13 rows)
- `.ufo/waves/round-39/w1/ExecQuarantineSlice/verdicts.md`
- `.ufo/waves/round-39/w1/ExecQuarantineSlice.md` (this report)

## Risks / notes
- S224 is time-sensitive: a status.json snapshot taken at round-4 time would have contained the quote; current
  bytes do not. If a canonically snapshotted copy exists elsewhere in the corpus it was not found under the cited
  path (only the lane's own round-4 proposal files contain the old timestamp — circular, not cited-source evidence).
- Quote-glyph normalization differences (straight vs curly quotes, `---` vs em dash) were treated as equivalent
  only when the surrounding text matched verbatim.
- No register or campaign file was modified; no git/jj mutations performed.
