# ExecQuarantineSlice — mado quarantine hand-check (round 32, w1)

Register: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
(read-only; its header and `## By lane` totals are stale — slice derived by the prescribed
awk filter; output: `.ufo/waves/round-32/assimilation/quarantine-slice`, 13 data rows).

Slice = 6 rows from the register's `payload-absent` section + 7 rows from its
"Rows whose quotes were NEVER CHECKED" section (2 `could not be fetched`, 5 `named no
locator`). Checked 2026-10-24.

## Verdict table

| id | register class | verdict | source fetched / checked | located quote or failure text |
|---|---|---|---|---|
| S189 | payload-absent | **PRESENT** (adoptable) | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp` | Verbatim in `formatEvent`: `auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));`. Checker likely escaped-quote fold miss. |
| S195 | payload-absent | **PRESENT** (adoptable) | package fetched earlier, verified against lane copy `lanes/mado/round2/fetch/arch-wiki-docs-zh-cn-20260901-1-any.pkg.tar.zst` (remote HEAD 200); extracted `usr/share/doc/arch-wiki-zh-cn/html/zh-cn/Hyprland.html` | Both quotes verbatim: `Hyprland 还公开了 2 UNIX 套接字，以便通过代码或命令行实用程序控制和获取有关 Hyprland 的信息。` and `Hyprland 需要一个外部的 Wayland 兼容的 idle 管理守护进程。最普遍安装的是 hypridle包 和 hyprlock包。` (markup links inside 包 names still emit the same text stream). |
| S201 | payload-absent | **PRESENT** (adoptable, re-anchor) | `https://arxiv.org/abs/2604.18860` (abstract page) + lane's full-source artifact `lanes/mado/round8/fetch/arXiv-2604.18860.txt` | Abstract page does NOT contain the quotes. Located in the paper's full LaTeX source: line 97 `Desktop agents interact across disjoint applications, manage overlapping windows governed by X11/Wayland compositors` (§intro) and line 430 `focus hijacking --- can redirect agent actions with up to 100\% success rates` (§evaluation). Adopt only with anchor changed to the full source, not the abstract page. |
| S205 | payload-absent | **PRESENT** (adoptable) | `https://wiki.archlinux.org/api.php?action=query&meta=siteinfo&siprop=interwikimap&format=json` (live, 200) | Both verbatim as the last two `interwikimap` entries: `"prefix": "zh-hans", … "url": "https://wiki.archlinuxcn.org/wiki/$1"` and `"prefix": "zh-hant", … "url": "https://wiki.archlinux.org/title/$1_(正體中文)"`. Also present in lane's `round3/fetch/interwiki.json`. |
| S224 | payload-absent | **ABSENT** (refuse as quoted — stale snapshot, not fabrication) | `/home/vgpnk/.cache/ai-usage/status.json` (local host file) | Cited `"updated_at": "2026-10-23T22:52:44Z",` is not in the file; current line 4 reads `"updated_at": "2026-10-24T23:01:21Z"`. The cache is rewritten by the ai-usage producer; `"version": 2,` still verifies at line 2. The cited timestamp is a rotating value — correct the quote to the current value or re-quote a stable field. |
| S228 | payload-absent | **PRESENT under quote-normalization** (adoptable with corrected quote) | `lanes/mado/round5/fetch/cn-export-hyprland.html` (lane artifact, 105882 B) | Line 1519 anchor text reads `使用“模板:过时”标记的页面或章节` — curly quotes “ ”, not the cited straight `"`. Verbatim-cited string is absent; normalized form present. Adopt with the corrected curly-quote string. |
| S199 | could not be fetched | **UNVERIFIABLE** | `https://blog.csdn.net/2301_76324845/article/details/149787804` — direct fetch now answers HTTP 521 (Cloudflare/origin) | Lane's reader-proxy artifact `round2/fetch/csdn-149787804.md.txt` (71921 B) does contain the gate quotes verbatim: `windowrule = opacity 0.80 $& 0.80 $& 1,class:^([Cc]ode)$` (line 160), `对应opacity [active_alpha] $& [inactive_alpha] $& [fade_duration]` (line 167). Remote still unreachable; payload corroborated by artifact, not re-verified live. |
| S200 | could not be fetched | **UNVERIFIABLE** | `https://blog.csdn.net/lxyoucan/article/details/164457293` — direct fetch now answers HTTP 521 | Lane's artifact `round2/fetch/csdn-164457293.md.txt` (30325 B) contains both gate quotes: `hl.bind("SUPER + L", hl.dsp.exec_cmd("hyprlock"))` (line 1150), `Hyprland 官方专门提供了 Lua stubs，推荐让 LSP 加载它。` (line 882). Same corroboration caveat as S199. |
| S209 | named no locator | **UNVERIFIABLE** (register cell is prose) — claim re-verified on successor state | Register cell `## Gate — S209` is prose, but the gate block DOES name a locator: `/run/user/1000/hypr/<HIS>/hyprland.log` | Cited HIS dir `…_1792772698_564628331` no longer exists (compositor restarted; current HIS `…_1792804449_426444678`). Current log: 2480916 B, 16069 lines, 0 occurrences of `overflowed event queue` / `failed writing event` / `Socket2 fd` — claim consistent on live state. |
| S222 | named no locator | **UNVERIFIABLE** (prose cell) — gate locator verified PRESENT | gate locator `/home/vgpnk/.local/bin/gkeep` | Whole file (11 lines) contains both quotes verbatim: `from gkeep.cli import main`, `raise SystemExit(main())`. |
| S223 | named no locator | **UNVERIFIABLE** (prose cell) — gate locator verified PRESENT | gate locator `/home/vgpnk/.local/bin/ai-usage` | Line 2 `"""Cache AI CLI usage windows and render a Waybar chip. waybar reads cache only."""`; line 65 `return Path(os.environ.get("AI_USAGE_CACHE", Path.home() / ".cache/ai-usage/status.json"))`. Both verbatim. |
| S225 | named no locator | **UNVERIFIABLE** (prose cell) — claim re-verified on successor state | gate locator `journalctl --user -u wayland-wm@hyprland.desktop.service` | Unit output now 718 lines (was 1091 — journal rotated/restarted), still 0 marker occurrences. Claim holds on live state; the 1091-line figure is stale. |
| S235 | named no locator | **UNVERIFIABLE** (prose cell) — claim re-verified on successor state | gate locator `/run/user/1000/hypr/<HIS>/` | Cited HIS dir gone; current instance dir is `700 directory`, `.socket.sock` and `.socket2.sock` both `755 socket`. Mode claim holds on live state. |

## Count by class (13 rows)

| verdict | rows |
|---|---|
| PRESENT — payload located, adoptable | 5 (S189, S195, S205; S201 on re-anchor to full source; S228 after quote-normalization) |
| ABSENT — refuse as quoted | 1 (S224 — rotating timestamp value; stale, not fabricated) |
| UNVERIFIABLE — prose-class register cell | 7 (S199, S200, S209, S222, S223, S225, S235) |

Notes: `unreachable` is not fabrication — S199/S200 remotes answer 521 but lane artifacts
corroborate the quotes. S209/S222/S223/S225/S235 are marked UNVERIFIABLE per the prose-cell
rule even though their gate blocks do name locators; hand-check evidence for them is in the
table above. Five of the six `payload-absent` rows are checker misses (JSON-escape,
markup-embedded text, curly-vs-straight quotes, abstract-vs-full-text anchor), not
fabrications; only S224's quoted timestamp is genuinely absent from a rotated file.

## Register defects (named, not edited)

1. `## By lane` summary undercounts mado: it lists `| mado | 6 |` but the register carries
   13 mado data rows (6 in §1 + 7 in §2); the summary counts only §1.
2. §2 mado id cells carry a stray trailing backtick (`S199\``, `S200\``, `S209\``, `S222\``,
   `S223\``, `S225\``, `S235\``) — cosmetic defect shared with every §2 row in the register.
3. §2's claim "the gate block named no locator" is inaccurate for all five mado gate rows:
   S209, S222, S223, S225, S235 each name a concrete locator (host path or journalctl unit)
   in their `## Gate — S###` block of `SOURCES-PROPOSED.md`. The checker evidently did not
   treat non-HTTP locators as locators.
4. No mado row is missing an S-id (all 13 rows carry one); zero no-S-id defects in this slice.
