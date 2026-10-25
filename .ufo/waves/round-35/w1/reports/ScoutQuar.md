# ScoutQuar — mado slice of the absent-defect register

Source: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (375 lines, read-only; not edited).
Derivation: `awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' <register>`.

## Data rows: 13

The register holds mado rows in **two distinct tables**:

- **Table 1 — "Rows"** (line 27, schema `lane | round | id | class | cited source | quote(s) | note`): 6 mado rows. Matches the register's own "By lane" tally of `mado | 6` (line 248). All carry class `payload-absent`.
- **Table 2 — "Rows whose quotes were NEVER CHECKED"** (line 265, schema `lane | round | id | why it was not checked | cited source`): 7 mado rows. This table has **no quote column**; the register itself states (lines 258-261) these rows are neither fabricated nor confirmed — the checker never attempted a match. The trailing backtick on the id field (`S199\``) is verbatim register formatting, not an extraction artifact.

## Table 1 rows (quote present; locator present)

| id | round | cited source (locator) | quoted document |
|---|---|---|---|
| S189 | round1 | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp` | `` `auto             eventString = std::format(\"{}>>{}\\n\", event.event, data.substr(0, 1024));` `` |
| S195 | round2 | `https://mirror.sjtu.edu.cn/archlinux-cn/aarch64/arch-wiki-docs-zh-cn-20260901-1-any.pkg.tar.zst` | `` `Hyprland 还公开了 2 UNIX 套接字，以便通过代码或命令行实用程序控制和获取有关 Hyprland 的信息。` `` + `` `Hyprland 需要一个外部的 Wayland 兼容的 idle 管理守护进程。最普遍安装的是 hypridle包 和 hyprlock包。` `` (two quotes joined by `<br>`) |
| S201 | round2 | `https://arxiv.org/abs/2604.18860` | `` `Desktop agents interact across disjoint applications, manage overlapping windows governed by X11/Wayland compositors` `` + `` `notification overlays and X11 window focus hijacking --- can redirect agent actions with up to 100% success rates` `` (two quotes) |
| S205 | round3 | `https://wiki.archlinux.org/api.php?action=query&meta=siteinfo&siprop=interwikimap&format=json` | `` `\"prefix\": \"zh-hans\", \"url\": \"https://wiki.archlinuxcn.org/wiki/$1\"` `` + `` `\"prefix\": \"zh-hant\", \"url\": \"https://wiki.archlinux.org/title/$1_(正體中文)\"` `` (two quotes) |
| S224 | round4 | `/home/vgpnk/.cache/ai-usage/status.json` (local file path) | `` `\"updated_at\": \"2026-10-23T22:52:44Z\",` `` |
| S228 | round5 | `lanes/mado/round5/fetch/cn-export-hyprland.html` (local repo-relative path) | `` `使用\"模板:过时\"标记的页面或章节` `` |

Locator? **All 6 name a locator** — four external URLs and two local filesystem paths.

## Table 2 rows (no quote column; locator per cited-source field)

| id | round | why it was not checked | cited-source field | names a locator? |
|---|---|---|---|---|
| S199 | round2 | the cited source could not be fetched, so no quote was checked | `https://blog.csdn.net/2301_76324845/article/details/149787804` | **Yes** — external URL |
| S200 | round2 | the cited source could not be fetched, so no quote was checked | `https://blog.csdn.net/lxyoucan/article/details/164457293` | **Yes** — external URL |
| S209 | round3 | the gate block named no locator, so no quote was checked | `## Gate — S209` | **No** — self-referential markdown heading, not a resolvable source locator |
| S222 | round4 | the gate block named no locator, so no quote was checked | `## Gate — S222` | **No** — same |
| S223 | round4 | the gate block named no locator, so no quote was checked | `## Gate — S223` | **No** — same |
| S225 | round4 | the gate block named no locator, so no quote was checked | `## Gate — S225` | **No** — same |
| S235 | round5 | the gate block named no locator, so no quote was checked | `## Gate — S235` | **No** — same |

The table cell is non-empty in all 7 rows, but for the five "gate block" rows the register's own reason column states the gate block **named no locator**; the heading text is a pointer to the round artifact, not a fetchable source.

## Summary counts

- 13 mado data rows total.
- 6 rows with a recorded quote (Table 1, all `payload-absent` — quote checked, absent from cited source and companions).
- 7 rows with no recorded quote (Table 2 — never checked).
- Locator named: 8 of 13 (all 6 Table-1 rows + S199, S200). Locator absent: 5 (S209, S222, S223, S225, S235).
- Round distribution: round1 ×1 (S189), round2 ×4 (S195, S199, S200, S201), round3 ×2 (S205, S209), round4 ×4 (S222, S223, S224, S225), round5 ×2 (S228, S235). Rounds 1-5 only; no mado rows from rounds 6-10.
