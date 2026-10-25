# Quarantine slice verdicts — mado (round-40 w1 ExecQuarantineSlice)

Re-derived 2026-10-25 from the absent-defect register
(`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`, read-only)
with the section-10 command, verbatim:

```
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" \
  > .ufo/waves/round-40/assimilation/quarantine-slice
```

Output: **13 lines, every line carries an S-id** (`assimilation/quarantine-slice`):
S189 S195 S201 S205 S224 S228 (payload-absent section) and
S199 S200 S209 S222 S223 S225 S235 (never-checked section, whose table has five columns, so the
command prints column 4 — the id with its trailing backtick — and column 5 — the class prose).

## Resolution rule used here

The register's ids are **not** the lane's ids. Two independent facts, both checked:

1. The register's round column is off by one for several rows: its `round4 S225` and `round5 S235`
   resolve to the lane's `round3/SOURCES-PROPOSED.md:25` and `round4/SOURCES-PROPOSED.md:23`.
2. Its ids are pre-packaging ids: `lanes/mado/ID-REMAP.md:9` — "the same id in two rounds names two
   different rows". `round3 S222` remaps to packaged `S228`, `round3 S223` to `S229`
   (`ID-REMAP.md:93-94`), while the register's `round4 S224` / `round5 S228` are not in the map at all.

So each verdict is keyed on **(round, id, cited source)** and names the lane row the cited source
resolves to. An id-only adoption would move evidence between rows with every structural check green.

Evidence copies live in `w1/ExecQuarantineSlice/src/` (bytes fetched or extracted read-only; host
config trees were never written).

| # | register row | resolved lane row (source-resolved) | cited source | verdict | evidence |
|---|---|---|---|---|---|
| 1 | `round1 S189` | `corpus/SOURCES.md:201` S189 (also staged as `SOURCES-PROPOSED.md:58` S206) | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/src/managers/EventManager.cpp` | **PRESENT — adoptable** | Fetched 200, 6479 B, sha256 `eea605dfe5ce09e1…` (matches the registry prefix). Quote `auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));` at **`src/managers/EventManager.cpp:128`** inside `CEventManager::formatEvent` (function at `:126`, truncation `:128`, newline fold `:129`). The register's `\"`/`\\n` are markdown escaping of `"`/`\n`, not source bytes. |
| 2 | `round2 S195` | `lanes/mado/round2/SOURCES-PROPOSED.md:19` S212 | `https://mirror.sjtu.edu.cn/archlinux-cn/aarch64/arch-wiki-docs-zh-cn-20260901-1-any.pkg.tar.zst` | **PRESENT — adoptable (anchor = package member)** | Member `usr/share/doc/arch-wiki-zh-cn/html/zh-cn/Hyprland.html` extracted from the 8 575 462 B package (read-only copy in the shokuknow lane): 105 882 B, sha256 `bc15ddb2a30f24b9…`. Both quotes are present but **split by inline markup**, so a literal grep misses them: `Hyprland 还公开了 <a …>2 UNIX 套接字</a>，以便…` at **line 1130** (§ hyprctl 和 IPC) and `Hyprland 需要一个外部的 Wayland 兼容的 idle 管理守护进程。…` at **line 1235** (§ Idle). Present under HTML tag-strip (`html.unescape(re.sub('<[^>]+>','',…))`, text offsets 11265 / 13948). |
| 3 | `round2 S201` | `lanes/mado/round2/SOURCES-PROPOSED.md:69` S218 | `https://arxiv.org/abs/2604.18860` | **PRESENT — adoptable, anchor is the full text, not the abs page** | `abs` page fetched 200 (42 386 B, sha256 `ab6d25a3…`) — **neither quote is in the abstract**. Full text `https://arxiv.org/html/2604.18860v1` fetched 200 (243 019 B on the wire, sha256 `06c10855…`): `Desktop agents interact across disjoint applications, manage overlapping windows governed by X11/Wayland compositors` at **char 31615** (paragraph `id="S1.p3"`) and `…dynamic UI manipulation — such as notification overlays and X11 window focus hijacking — can redirect agent actions with up to 100% success rates…` at **char 224311** (conclusion paragraph `id="S8.p1"`). Fragment counts in the stripped full text: `Desktop agents interact` 1, `disjoint applications` 1, `X11/Wayland compositors` 1, `focus hijacking` 1, `up to 100% success rates` 1; all five are 0 on the abs page. Register `---` is the em dash. |
| 4 | `round3 S205` | `lanes/mado/round3/SOURCES-PROPOSED.md:22` S222 — **the same source and the same two gate quotes as the lane's S222 (register row 10)** | `https://wiki.archlinux.org/api.php?action=query&meta=siteinfo&siprop=interwikimap&format=json` | **PRESENT under JSON normalization; the registered contiguous literal is absent** | Live fetch 200, 8 313 B, sha256 `bcff738b…`, one line, 74 interwiki entries. `{"prefix":"zh-hans",…,"url":"https://wiki.archlinuxcn.org/wiki/$1"}` at **byte 7996**; `{"prefix":"zh-hant",…,"url":"https://wiki.archlinux.org/title/$1_(\u6b63\u9ad4\u4e2d\u6587)"}` at **byte 8141** (CJK url is `\u`-escaped in the raw bytes; `json.load` yields `正體中文`). The register's `"prefix": "zh-hans", "url": …` is a **reformatted pair** (spaces inserted, `local`/`language`/`bcp47` dropped) — count 0 in the raw response, so the quote must be re-quoted as the two field values, not the joined literal. |
| 5 | `round4 S224` | `lanes/mado/round4/SOURCES-PROPOSED.md:29` **S241** (`§ updated_at`, same quote at `:93`; gate at `:90`) | `/home/vgpnk/.cache/ai-usage/status.json` | **VOLATILE / ROTATED — unverifiable, NOT fabrication** | The line shape is present but the value rotates: `"updated_at": "2026-10-25T20:47:13Z",` at my first read (17:51 local) and `"updated_at": "2026-10-25T20:52:19Z",` at **line 3** of the second read 60 s later (29 877 B, sha256 `ae44b170…`). The quoted `2026-10-23T22:52:44Z` occurs **0** times in `status.json` and **0** times in `inception-ledger.json`. This is the register's own `payload-absent` mislabel for a live telemetry field — the D2 correction: a rotated volatile timestamp, not a fabrication. |
| 6 | `round5 S228` | `lanes/mado/round5/SOURCES-PROPOSED.md:19` **S245** (gate `:28`, quote `:32`) | `lanes/mado/round5/fetch/cn-export-hyprland.html` | **PRESENT — adoptable with the quote glyph corrected** | File exists, 105 882 B, sha256 `bc15ddb2a30f24b9…` — **byte-identical to the S195 package member above**. Quote at **line 1519**: `<li><a … title="Category:使用「模板:过时」标记的页面或章节（页面不存在）">使用“模板:过时”标记的页面或章节</a></li>`. The page renders U+201C/U+201D (`“”`, codepoints 0x201c/0x201d); the register stores ASCII `"`. Present under quote-glyph normalization only. |
| 7 | `round2 S199` | `lanes/mado/round2/SOURCES-PROPOSED.md:53` S216 (gate `:55`) | `https://blog.csdn.net/2301_76324845/article/details/149787804` | **PRESENT in the lane's reader-proxy body; live URL unreachable** | Live re-fetch: HTTP **521**, 2 199 B of anti-bot JS (`src/csdn-149787804.html`) — the cited URL still refuses a plain client. The cached reader-proxy body `lanes/mado/round2/fetch/csdn-149787804.md.txt` (71 921 B, sha256 `1dab3c20a1be5817…`, matching the row's own sha prefix) carries both row quotes: `windowrule = opacity 0.80 $& 0.80 $& 1,class:^([Cc]ode)$` at **line 160** and `对应opacity [active_alpha] $& [inactive_alpha] $& [fade_duration]` at **line 167**. The register's "no quote was checked" is a reachability artifact, not an absent payload. |
| 8 | `round2 S200` | `lanes/mado/round2/SOURCES-PROPOSED.md:61` S217 (gate `:63`) | `https://blog.csdn.net/lxyoucan/article/details/164457293` | **PRESENT in the lane's reader-proxy body; live URL unreachable** | Live re-fetch: HTTP **521**, 2 165 B of anti-bot JS (`src/csdn-164457293.html`). Cached body `lanes/mado/round2/fetch/csdn-164457293.md.txt` (30 325 B, sha256 `6cd966f4329da9df…`, matching the row's sha prefix): `hl.bind("SUPER + L", hl.dsp.exec_cmd("hyprlock"))` at **line 1150**, `Hyprland 官方专门提供了 Lua stubs，推荐让 LSP 加载它。` at **line 882**. |
| 9 | `round3 S209` | **none** — no `S209` row and no `## Gate — S209` in `lanes/mado/round3/SOURCES-PROPOSED.md` (the only S209 rows are the round-1 Japanese-wiki row at `SOURCES-PROPOSED.md:84`, gate `:86`, and `round16` S344-S346) | (register names none) | **UNVERIFIABLE — no quote exists** | The register's own class holds for this row: there is no gate block in the row's round and therefore no quote and no locator; nothing can be located or refused. Distinct from the lane registry's own S209 (`corpus/SOURCES.md:211`, round-35 own-work receipt), whose locator `.ufo/waves/round-35/fetch/S209.receipt.txt` exists (905 B) and whose sha256 `a170c7a50b9305b3448fc85ecddb0d7b1f1c3ff5e42c78cdc2d07718c3bdd27c` matches the registry cell exactly — different row, same id. |
| 10 | `round3 S222` | `lanes/mado/round3/SOURCES-PROPOSED.md:22` S222 (gate `:48`) | `https://wiki.archlinux.org/api.php?action=query&meta=siteinfo&siprop=interwikimap&format=json` | **PRESENT under JSON normalization — adoptable** | Same bytes as row 4 (fetch 200, 8 313 B, sha256 `bcff738b…`). Both field pairs located: zh-hans url at byte 7996's object, zh-hant url at byte 8141's object. **The register's class text is falsified**: `## Gate — S222` at `round3/SOURCES-PROPOSED.md:48-52` does name a locator (`- URL: https://wiki.archlinux.org/api.php?…`) and both quotes; it is not a block with "no locator". |
| 11 | `round3 S223` | `lanes/mado/round3/SOURCES-PROPOSED.md:23` S223 (gate `:54`) | `https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/systemd/hypridle.service.in` | **PRESENT — adoptable** | Fetched 200, 339 B, sha256 `848599690114926c…`. All three gate quotes at count 1: `PartOf=graphical-session.target`, `Restart=on-failure`, `ExecStart=@CMAKE_INSTALL_PREFIX@/bin/hypridle`. Register class text falsified — the gate block names its URL at `:55`. |
| 12 | `round4 S225` | `lanes/mado/round3/SOURCES-PROPOSED.md:25` S225 (gate `:68`) — **register round label off by one** | `/usr/lib/systemd/user/hypridle.service` | **PRESENT — adoptable** | Host unit exists, 321 B, sha256 `81939c3f6004a965…`. All three gate quotes at count 1: `ConditionEnvironment=WAYLAND_DISPLAY`, `ExecStart=/usr/bin/hypridle`, `WantedBy=graphical-session.target`. Register class text falsified — the gate block names the path at `:69`. |
| 13 | `round5 S235` | `lanes/mado/round4/SOURCES-PROPOSED.md:23` S235 (gate `:53`) — **register round label off by one** | `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-refresh-hypridle` | **PRESENT — adoptable** | Fetched 200, 188 B, sha256 `a5c4e33acfc52013…`. Both gate quotes at count 1: `omarchy-refresh-config hypr/hypridle.conf`, `omarchy-restart-hypridle`. Register class text falsified — the gate block names its URL at `:54`. |

## Rows the K1/K2 candidates cite

K1 (`merge/mado/knowledge/corpus/knowledge/host-bar-producers-r28.md`) cites **S224** and **S228**;
K2 (`…/host-producer-outputs-r29.md`) cites **S237-S241**. The candidates' ids are round-scoped
packaged ids and resolve to *different rows* than the register rows that happen to share the literal
id — this is the id collision the slice must not paper over:

| candidate id | candidate's cited source | verdict | evidence |
|---|---|---|---|
| K1 **S224** | `/home/vgpnk/.config/waybar/config.jsonc` | **PRESENT — adoptable** | Lane row `round3/SOURCES-PROPOSED.md:24` S224, gate `:61` (URL `/home/vgpnk/.config/waybar/config.jsonc`, upstream counterpart `…/omarchy/v3.8.4/config/waybar/config.jsonc`). Host file 6 354 B, sha256 `a408a33df48a39dc…`; gate quotes both present: `"exec": "$OMARCHY_PATH/default/waybar/indicators/idle.sh",` at **line 209** (count 1), `"return-type": "json",` (count 4). K1's table claims also check out: 10 distinct `custom/*` keys on the host vs 8 upstream (upstream file 5 114 B, sha256 `ff387b21…`), host-only `custom/gkeep` and `custom/ai-usage`, `"exec": "~/.local/bin/gkeep waybar"` at **line 237**, `"exec": "~/.local/bin/ai-usage waybar"` at **line 247**. |
| K1 **S228** | `…/omarchy/v3.8.4/default/waybar/indicators/idle.sh` | **PRESENT — adoptable** | Lane row `round3/SOURCES-PROPOSED.md:28` S228, gate `:88` (URL, plus both quotes). Fetched 200, 159 B, sha256 `6d8d2c11d3c3b15f…`: `if pgrep -x hypridle >/dev/null; then` at **line 3**, `echo '{"text": "󱫖", "tooltip": "Idle lock disabled", "class": "active"}'` at **line 6**. Both candidate quotes located verbatim. |
| K2 **S237** | `…/indicators/screen-recording.sh` | **PRESENT** | Fetched 200, 169 B, sha256 `28491cd3fdaaea78…`; `if pgrep -f "^gpu-screen-recorder" >/dev/null; then` at **line 3**. |
| K2 **S238** | `…/indicators/notification-silencing.sh` | **PRESENT** | Fetched 200, 174 B, sha256 `312900d1a9ca772e…`; `if makoctl mode \| grep -q 'do-not-disturb'; then` at **line 3**. |
| K2 **S239** | `/home/vgpnk/.local/bin/gkeep` | **PRESENT** | Symlink → `/home/vgpnk/Projects/gkeep/bin/gkeep` (sha256 `c1b147a07f0c34af…`); `from gkeep.cli import main` at **line 9**. |
| K2 **S240** | `/home/vgpnk/.local/bin/ai-usage` | **PRESENT** | Symlink → `/home/vgpnk/Projects/omarchy-usage-tray/bin/ai-usage` (sha256 `0ccd33ab7e83edd0…`); docstring at **line 2**, cache-path line `return Path(os.environ.get("AI_USAGE_CACHE", Path.home() / ".cache/ai-usage/status.json"))` at **line 64**. |
| K2 **S241** | `/home/vgpnk/.cache/ai-usage/status.json` | **VOLATILE — unverifiable, NOT fabrication** | Same bytes and same rotating `updated_at` as register row 5; K2's quote text is byte-identical to the register's `round4 S224` quote, which is the proof that the register row and K2's S241 are the same evidence under two ids. |

## Summary

- **Present / adoptable (11):** S189, S195, S201, S205 (=S222), S228, S199, S200, S222, S223, S225, S235.
- **Volatile, unverifiable, not fabrication (1):** S224 — and its K2 twin S241.
- **No quote exists, unverifiable (1):** S209.
- **Refused as fabrication (0).** No row in this slice is a fabricated payload; every "absent" class
  in the register resolves to a normalization gap (markdown escaping, HTML inline tags, JSON
  reformatting, quote glyphs), a reachability gap (CSDN 521), or a rotating telemetry value.
- **Register defects observed (data for the lesson, not repaired here):** (a) the round column is
  off by one on `round4 S225` / `round5 S235`; (b) ids are pre-packaging (`round3 S222`→`S228`,
  `round3 S223`→`S229` per `ID-REMAP.md:93-94`) while `round4 S224` / `round5 S228` are not in the
  map; (c) register `S205` duplicates lane `S222`'s source and gate quotes — the same evidence under two register ids;
  (d) four "gate block named no locator" rows (S222, S223, S225, S235) do name a locator in their
  own round file; (e) `round4 S224`'s payload is the live `ai-usage` cache, so it can never be
  quote-stable and must be cited by shape (`§ updated_at`), not by value.
- Nothing was written outside `.ufo/waves/round-40/w1/ExecQuarantineSlice*` and
  `.ufo/waves/round-40/assimilation/quarantine-slice`; the register and the shokuknow lane were read only.
