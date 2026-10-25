# ScoutQuarantineA — mado payload-absent registry check

Scope: six `mado` `payload-absent` rows (S189, S195, S201, S205, S224, S228) from
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (read-only).
For each: printed register URL + quoted span, grepped `corpus/SOURCES.md` for the URL and the id,
classified IN-REGISTRY-SAME-ID / IN-REGISTRY-DIFFERENT-ID / NOT-IN-REGISTRY.

Method: anchored `grep` on `corpus/SOURCES.md` for each URL's distinguishing tokens
(`EventManager.cpp`/`efb50993780079460b0cbed1363e2166a2de1d9f`, `arch-wiki-docs-zh-cn`/`mirror.sjtu.edu.cn`,
`2604.18860`/`arxiv`, `interwikimap`/`api.php?action=query`, `ai-usage/status.json`,
`cn-export-hyprland`/`round5/fetch`) and anchored `^\| S<id> \|` row checks. Registry has 192 `S`-rows,
last allocated id S202 — so S205/S224/S228 ids cannot exist; S195 id confirmed absent.

## Table (also at `.ufo/waves/round-34/scratch/ScoutQuarantineA/table.md`)

| id | register URL | register quoted span | classification |
|---|---|---|---|
| S189 | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp` | `auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));` | **IN-REGISTRY-SAME-ID** — S189 row cites this exact URL (registry line 201) |
| S195 | `https://mirror.sjtu.edu.cn/archlinux-cn/aarch64/arch-wiki-docs-zh-cn-20260901-1-any.pkg.tar.zst` | `Hyprland 还公开了 2 UNIX 套接字，以便通过代码或命令行实用程序控制和获取有关 Hyprland 的信息。` / `Hyprland 需要一个外部的 Wayland 兼容的 idle 管理守护进程。最普遍安装的是 hypridle包 和 hyprlock包。` | **NOT-IN-REGISTRY** — URL tokens and id both absent |
| S201 | `https://arxiv.org/abs/2604.18860` | `Desktop agents interact across disjoint applications, manage overlapping windows governed by X11/Wayland compositors` / `notification overlays and X11 window focus hijacking --- can redirect agent actions with up to 100% success rates` | **NOT-IN-REGISTRY** — URL absent; **id collision**: registry S201 cites `Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp` (registry line 203), a different source — not a DIFFERENT-ID match |
| S205 | `https://wiki.archlinux.org/api.php?action=query&meta=siteinfo&siprop=interwikimap&format=json` | `"prefix": "zh-hans", "url": "https://wiki.archlinuxcn.org/wiki/$1"` / `"prefix": "zh-hant", "url": "https://wiki.archlinux.org/title/$1_(正體中文)"` | **NOT-IN-REGISTRY** — URL tokens and id absent (registry ends at S202) |
| S224 | `/home/vgpnk/.cache/ai-usage/status.json` | `"updated_at": "2026-10-23T22:52:44Z",` | **NOT-IN-REGISTRY** — local path and id absent (registry ends at S202) |
| S228 | `lanes/mado/round5/fetch/cn-export-hyprland.html` | `使用"模板:过时"标记的页面或章节` | **NOT-IN-REGISTRY** — artifact path and id absent (registry ends at S202) |

## Findings

- 1 of 6 register rows corresponds to a live registry row: S189, exact-URL, same-id.
- 5 of 6 are NOT-IN-REGISTRY: the cited source is no longer in `corpus/SOURCES.md`.
- No row is IN-REGISTRY-DIFFERENT-ID.
- S201 note: the register's id is live in the registry but bound to an unrelated source — an id
  collision consistent with registry compaction, not an alternate id for the same URL.
- S189 note (non-classification): the S189 registry row itself covers `formatEvent` at
  `src/managers/EventManager.cpp:126` and the 1024-byte bound at `:128`, so the flagged quote
  plausibly paraphrases the registry's own anchored span — relevant to whichever quarantine
  action wave 1 chooses.

## Evidence

- Register lines 141–146 (the six mado rows) of `absent-defect-register.md`.
- `corpus/SOURCES.md`: S189 row at line 201; S201 row (Waybar) at line 203; 192 `S` rows total;
  zero matches for `mirror.sjtu.edu.cn`, `arch-wiki-docs-zh-cn`, `pkg.tar.zst`, `arxiv`,
  `2604.18860`, `api.php?action=query`, `interwikimap`, `ai-usage`, `status.json`,
  `cn-export-hyprland`, `round5/fetch`.
- Scratch table: `.ufo/waves/round-34/scratch/ScoutQuarantineA/table.md`.

Limits: classification is URL/id presence in `corpus/SOURCES.md` only; companion-URL fields and
knowledge-file citations were not searched. Whether the registry ever held these rows (vs. never)
is not determined here — MANIFEST/rounds history would answer that.
