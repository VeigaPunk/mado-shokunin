# Quarantine slice verdicts — mado (round-39 w1 ExecQuarantineSlice)

Hand-checked 2026-10-25 against the absent-defect-register
(`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`, 13 mado rows).
Every row below carries its S-id. No row is appendable this round unless hand-checked AND present; payload-present
rows carry the located anchor.

| id | class | verdict | evidence / anchor |
|---|---|---|---|
| S189 | payload-absent | **present** — appendable | Fetched cited source `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp` (200 OK, 192 lines, sha1 see report). Quote `auto eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));` found verbatim at **line 128** in `CEventManager::formatEvent`. Register's `\"`/`\\n` escapes are markdown quoting of `"` / `\n`. |
| S195 | payload-absent | **present** — appendable | Extracted cited source member from `arch-wiki-docs-zh-cn-20260901-1-any.pkg.tar.zst` (mirror.sjtu.edu.cn copy cached at `lanes/mado/round2/fetch/`): `usr/share/doc/arch-wiki-zh-cn/html/zh-cn/Hyprland.html`. Both quotes found verbatim after HTML-strip normalization: `Hyprland 还公开了 2 UNIX 套接字，以便通过代码或命令行实用程序控制和获取有关 Hyprland 的信息。` and `Hyprland 需要一个外部的 Wayland 兼容的 idle 管理守护进程。最普遍安装的是 hypridle包 和 hyprlock包。` (paragraphs under IPC / hypridle–hyprlock sections). |
| S201 | payload-absent | **present** — appendable | Fetched cited source `https://arxiv.org/abs/2604.18860` (arXiv API abstract) and full text `https://arxiv.org/html/2604.18860v1` (243,019 B). `Desktop agents interact across disjoint applications, manage overlapping windows governed by X11/Wayland compositors, and respond to OS-level notifications.` at plain-text idx ~8414; `…dynamic UI manipulation — such as notification overlays and X11 window focus hijacking — can redirect agent actions with up to 100% success rates…` at idx ~52076–52169. Register `---` is markdown em-dash. |
| S205 | payload-absent | **present** — appendable | Fetched cited source `https://wiki.archlinux.org/api.php?action=query&meta=siteinfo&siprop=interwikimap&format=json`. `"prefix": "zh-hans"` + `"url": "https://wiki.archlinuxcn.org/wiki/$1"` at JSON **lines 414/418**; `"prefix": "zh-hant"` + `"url": "https://wiki.archlinux.org/title/$1_(正體中文)"` at JSON **lines 421/425**. |
| S224 | payload-absent | **absent — refused** | Cited source `/home/vgpnk/.cache/ai-usage/status.json` (live telemetry; 30,009 B, mtime 2026-10-25 16:05). Current bytes contain only `"updated_at": "2026-10-25T19:05:31Z"`; quoted `"updated_at": "2026-10-23T22:52:44Z",` appears nowhere in status.json or inception-ledger.json (grep exit 1, 0 hits). Volatile timestamp rotated; row not appendable. The old value survives only in the lane's own round-4 proposal files (circular; not the cited source). |
| S228 | payload-absent | **present** — appendable | Cited source `lanes/mado/round5/fetch/cn-export-hyprland.html` exists. Quote found at **line 1519**: `<li><a … title="Category:使用「模板:过时」标记的页面或章节（页面不存在）">使用“模板:过时”标记的页面或章节</a></li>` — text matches the registered quote modulo quote-glyph normalization (register straight `"`, page renders curly `“”`). |
| S199 | unreachable | **unreachable** (not fabrication) | Cited source `https://blog.csdn.net/2301_76324845/article/details/149787804` still unfetchable: re-fetch now returns HTTP **521** + anti-bot JS (2,156 B), no article text. No quote was ever recorded for this row, so nothing to locate. |
| S200 | unreachable | **unreachable** (not fabrication) | Cited source `https://blog.csdn.net/lxyoucan/article/details/164457293` still unfetchable: re-fetch returns HTTP **521** + anti-bot JS (2,232 B). No quote recorded. |
| S209 | unreachable (gate block, no locator) | **unreachable** | `## Gate — S209` named no locator; no quote to hand-check. |
| S222 | unreachable (gate block, no locator) | **unreachable** | `## Gate — S222` named no locator; no quote to hand-check. |
| S223 | unreachable (gate block, no locator) | **unreachable** | `## Gate — S223` named no locator; no quote to hand-check. |
| S225 | unreachable (gate block, no locator) | **unreachable** | `## Gate — S225` named no locator; no quote to hand-check. |
| S235 | unreachable (gate block, no locator) | **unreachable** | `## Gate — S235` named no locator; no quote to hand-check. |

## Summary
- Hand-checked present (appendable): **S189, S195, S201, S205, S228** (5).
- Hand-checked absent (refused): **S224** (1) — volatile telemetry rotated; no snapshot of cited bytes exists in the register's fetch set.
- Unreachable / prose-unverifiable (no fabrication verdict): **S199, S200, S209, S222, S223, S225, S235** (7).
- No row is flagged as fabrication; no register/campaign file was edited.
