# ScoutQuarantineA — mado payload-absent rows vs lane registry

Register: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (read-only).
Registry: `corpus/SOURCES.md` (192 `S`-rows; last allocated id S202). Checked 2026-10-24.

| id | register URL | register quoted span | URL in registry? | ID in registry? | classification |
|---|---|---|---|---|---|
| S189 | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp` | `auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));` | yes — S189 row cites this exact URL | yes — S189 | IN-REGISTRY-SAME-ID |
| S195 | `https://mirror.sjtu.edu.cn/archlinux-cn/aarch64/arch-wiki-docs-zh-cn-20260901-1-any.pkg.tar.zst` | `Hyprland 还公开了 2 UNIX 套接字，以便通过代码或命令行实用程序控制和获取有关 Hyprland 的信息。` / `Hyprland 需要一个外部的 Wayland 兼容的 idle 管理守护进程。最普遍安装的是 hypridle包 和 hyprlock包。` | no — `mirror.sjtu.edu.cn`, `arch-wiki-docs-zh-cn`, `pkg.tar.zst` all absent | no — no `S195` row | NOT-IN-REGISTRY |
| S201 | `https://arxiv.org/abs/2604.18860` | `Desktop agents interact across disjoint applications, manage overlapping windows governed by X11/Wayland compositors` / `notification overlays and X11 window focus hijacking --- can redirect agent actions with up to 100% success rates` | no — `arxiv`, `2604.18860` absent | collision — `S201` exists but cites `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp` | NOT-IN-REGISTRY (id reused by different source; no DIFFERENT-ID row holds the URL) |
| S205 | `https://wiki.archlinux.org/api.php?action=query&meta=siteinfo&siprop=interwikimap&format=json` | `"prefix": "zh-hans", "url": "https://wiki.archlinuxcn.org/wiki/$1"` / `"prefix": "zh-hant", "url": "https://wiki.archlinux.org/title/$1_(正體中文)"` | no — `api.php?action=query`, `interwikimap` absent | no — no `S205` row | NOT-IN-REGISTRY |
| S224 | `/home/vgpnk/.cache/ai-usage/status.json` | `"updated_at": "2026-10-23T22:52:44Z",` | no — `ai-usage`, `status.json` absent | no — no `S224` row | NOT-IN-REGISTRY |
| S228 | `lanes/mado/round5/fetch/cn-export-hyprland.html` | `使用"模板:过时"标记的页面或章节` | no — `cn-export-hyprland`, `round5/fetch` absent | no — no `S228` row | NOT-IN-REGISTRY |

Notes:

- S189: the flagged quote is a formatting/sanitisation fact; the S189 registry row does cover `formatEvent` at `src/managers/EventManager.cpp:126` and the `1024`-byte bound at `:128`, so the quoted span is presumably a paraphrase/misquote of `:126`–`:128` rather than a missing source. Quarantine decision is downstream; this table only establishes presence.
- S201 is the only row where the register id itself is live in the registry but bound to an unrelated source — an id collision, not a registry row for the cited arXiv URL.
- No register row's URL appears anywhere in `corpus/SOURCES.md` except S189's.
