# ExecQuarantineSlice — quarantine slice re-derived and hand-checked (round 40, w1)

Seat: `.ufo/waves/round-40/w1/ExecQuarantineSlice/`. Leaf seat; no dispatch, no background jobs,
no writes outside the seat dir and the one slice path the task names. No tool installs were needed
(nothing outside the stdlib + `curl` + `tar` + `grep`/`sha256sum` was used, so there is no
tool/version/channel line to record).

## 1. Slice derivation (section-10 command, run verbatim)

```
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" \
  > .ufo/waves/round-40/assimilation/quarantine-slice
```

- Output: **13 lines, every line carries an S-id** — `assimilation/quarantine-slice`, 637 B,
  sha256 `d9ea803d2433942dac094a14e9223be086ad460502163df7faf6e2509d9bb45d`.
- Ids: `S189 S195 S201 S205 S224 S228` (the register's `payload-absent` table) and
  `S199 S200 S209 S222 S223 S225 S235` (the register's "quotes never checked" table).
- The second table has **five** columns, not seven, so the command's `$4, $5` prints the id with
  its trailing backtick plus the class prose for those seven rows (` S199\`   the cited source could
  not be fetched…`). That is the command as specified, not a mangling on my side; the register's
  first table prints `id, class` as intended. Both shapes keep the S-id on the line, which is what
  the task requires.

## 2. What was checked, per row

Every row was hand-checked against its own cited source; nothing was taken from the register's
class column. Full table with anchors: `w1/ExecQuarantineSlice/verdicts.md` (15 212 B, sha256
`90f2068696bcff1bb179b2b0da9f69d400e33310b8db59e01f546d2dc69cfdc0`).

| id | verdict | anchor |
|---|---|---|
| S189 | PRESENT | `src/managers/EventManager.cpp:128` @ `efb5099…` (v0.56.2), 6479 B, sha256 `eea605df…` — matches the registry prefix |
| S195 | PRESENT | pkg member `usr/share/doc/arch-wiki-zh-cn/html/zh-cn/Hyprland.html` lines **1130** and **1235**; quotes are split by inline `<a>`/`<span>` markup, present under HTML tag-strip |
| S201 | PRESENT | full text `arxiv.org/html/2604.18860v1` char **31615** (`id="S1.p3"`) and **224311** (`id="S8.p1"`); **absent from the `abs` page** the register cites |
| S205 | PRESENT (JSON-normalized) | live interwikimap 8313 B: `{"prefix":"zh-hans",…,"url":"…archlinuxcn.org/wiki/$1"}` at byte **7996**, zh-hant at **8141** (CJK url `\u`-escaped); registered joined literal count 0 |
| S224 | **VOLATILE → unverifiable, NOT fabrication** | `status.json:3` `updated_at` read `2026-10-25T20:47:13Z` then `…20:52:19Z` 60 s later; the quoted `2026-10-23T22:52:44Z` is 0× in `status.json` and 0× in `inception-ledger.json` |
| S228 | PRESENT (quote-glyph) | `lanes/mado/round5/fetch/cn-export-hyprland.html:1519` renders U+201C/U+201D; register stores ASCII `"` |
| S199 | PRESENT in cached body, live URL 521 | `round2/fetch/csdn-149787804.md.txt` sha256 `1dab3c20…` (matches the row's own prefix); quotes at lines **160** / **167** |
| S200 | PRESENT in cached body, live URL 521 | `round2/fetch/csdn-164457293.md.txt` sha256 `6cd966f4…`; quotes at lines **1150** / **882** |
| S209 | UNVERIFIABLE (no quote exists) | no `S209` row and no `## Gate — S209` in `round3/SOURCES-PROPOSED.md`; the register's class is correct for this row |
| S222 | PRESENT (JSON-normalized) | same bytes as S205; `## Gate — S222` at `round3/SOURCES-PROPOSED.md:48` **does name its URL at `:49`** |
| S223 | PRESENT | `hypridle.service.in` @ v0.1.8, 339 B, sha256 `84859969…`; 3/3 gate quotes count 1 |
| S225 | PRESENT | `/usr/lib/systemd/user/hypridle.service`, 321 B, sha256 `81939c3f…`; 3/3 gate quotes count 1 |
| S235 | PRESENT | `omarchy-refresh-hypridle` @ v3.8.4, 188 B, sha256 `a5c4e33a…`; 2/2 gate quotes count 1 |

Live fetches, all 200 except the two CSDN URLs: EventManager.cpp 6479 B, idle.sh 159 B,
screen-recording.sh 169 B, notification-silencing.sh 174 B, upstream waybar config 5114 B,
`hypridle.service.in` 339 B, `omarchy-refresh-hypridle` 188 B, arxiv abs 42 386 B,
arxiv full text 243 019 B, interwikimap 8 313 B. CSDN: **521** (2 199 B / 2 165 B of anti-bot JS).

## 3. Rows the K1/K2 candidates cite (the hand-check the task asks for)

K1 (`host-bar-producers-r28.md`) cites **S224** and **S228**; K2 (`host-producer-outputs-r29.md`)
cites **S237-S241**. All seven located:

- **K1 S224** → `/home/vgpnk/.config/waybar/config.jsonc`, 6354 B, sha256 `a408a33d…`.
  `"exec": "$OMARCHY_PATH/default/waybar/indicators/idle.sh",` at **line 209**;
  `"return-type": "json",` count 4; `"exec": "~/.local/bin/gkeep waybar"` at **line 237**;
  `"exec": "~/.local/bin/ai-usage waybar"` at **line 247**. Module sets re-derived: host 10
  `custom/*` keys, upstream 8, host-only `custom/gkeep` + `custom/ai-usage`; upstream 5114 B —
  K1's byte-count and module-set claims hold.
- **K1 S228** → `…/omarchy/v3.8.4/default/waybar/indicators/idle.sh`, 159 B, sha256 `6d8d2c11…`;
  both candidate quotes verbatim at **lines 3 and 6**.
- **K2 S237/S238** → `screen-recording.sh` line 3 / `notification-silencing.sh` line 3, verbatim.
- **K2 S239/S240** → `~/.local/bin/gkeep` (symlink → `/home/vgpnk/Projects/gkeep/bin/gkeep`,
  sha256 `c1b147a0…`) line 9; `~/.local/bin/ai-usage` (symlink → `…/omarchy-usage-tray/bin/ai-usage`,
  sha256 `0ccd33ab…`) lines 2 and 64.
- **K2 S241** → same rotating `updated_at` as S224: **volatile, unverifiable, not fabrication**.

So both candidates' citations are adoptable; none of their quotes is fabricated.

## 4. The finding that matters for integration: ids are not unique keys

The register's ids are **not** the lane's ids, and a slice row must be adopted on
**(round, id, cited source)**, never on the id alone:

1. **Id collision on S224.** Register `round4 S224` = the `ai-usage` cache row, which is
   `round4/SOURCES-PROPOSED.md:29` **S241** in its own round file (quote at `:93`, gate at `:90`).
   K1's `S224` is the *round-3 host-waybar-config* row (`round3/SOURCES-PROPOSED.md:24`, gate `:61`).
   Two different rows, two different sources, same literal id — both verified, verdicts differ
   (config PRESENT vs cache VOLATILE).
2. **Id collision on S228.** Register `round5 S228` = the Chinese wiki export, which is
   `round5/SOURCES-PROPOSED.md:19` **S245** (gate `:28`). K1's `S228` is the round-3 `idle.sh` row
   (`round3/SOURCES-PROPOSED.md:28`, gate `:88`). Both verified PRESENT.
3. **Pre-packaging ids.** `ID-REMAP.md:9`: "the same id in two rounds names two different rows".
   `round3 S222`→`S228`, `round3 S223`→`S229` (`ID-REMAP.md:93-94`); register `round4 S224` /
   `round5 S228` are not in the map at all.
4. **Duplicate row.** Register `S205` and `S222` name the same source and the same gate quotes —
   one evidence set under two register ids.
5. **Round column off by one** on two rows: register `round4 S225` → lane `round3:25` S225;
   register `round5 S235` → lane `round4:23` S235.
6. **Four "no locator" classes are wrong.** S222, S223, S225 and S235 each sit under a gate block
   that names its URL on the line after the heading. Only S209 genuinely has no gate block.
7. **S209 is two rows.** Register `round3 S209` (Japanese wiki, no gate block, no quote) is not the
   lane registry's `S209` (`corpus/SOURCES.md:211`, round-35 own-work receipt) — that row's locator
   `.ufo/waves/round-35/fetch/S209.receipt.txt` exists (905 B) and its sha256 `a170c7a5…` matches the
   registry cell exactly.

## 5. D2 correction (round-39 non-author closure)

`corpus/lessons/round-39.md` labels the quarantined S224 "refused (fabrication class)", and
`round-39/w1/ExecQuarantineSlice/verdicts.md` repeats it as "absent — refused". Both are over-labels.
The row's payload is a **live telemetry line** (`/home/vgpnk/.cache/ai-usage/status.json`, `§
updated_at`), and I observed it rotate twice inside one minute of this seat's own runtime
(`20:47:13Z` → `20:52:19Z`). The correct class is **volatile/rotated → unverifiable, NOT
fabrication**; the register's `payload-absent` on this row is the same mislabel, and the durable
citation must be by shape (`§ updated_at`), not by value. This is exactly the D2 note the
registration asks for; I did not edit `corpus/lessons/round-39.md` (L1 is the only integrator).

## 6. Retained evidence

All under `.ufo/waves/round-40/w1/ExecQuarantineSlice/` (464 K total):

- `verdicts.md` — the 13-row table + the candidate-cited section + summary.
- `registry-rows.txt` — the slice ids' rows extracted from `corpus/SOURCES.md` (only S189, S201,
  S205, S209 exist there; the other nine are not lane-registry rows).
- `src/` — byte copies used as anchors: `EventManager.cpp` (6479 B, `eea605df…`),
  `Hyprland.zh-cn.html` (105 882 B, `bc15ddb2…`, extracted from the 8 575 462 B zh-cn wiki package),
  `arxiv-abs.html` (42 386 B, `ab6d25a3…`), `arxiv-html.html` (243 019 B, `06c10855…`),
  `wiki-interwikimap.json` (8 313 B, `bcff738b…`), `idle.sh` (`6d8d2c11…`),
  `screen-recording.sh` (`28491cd3…`), `notification-silencing.sh` (`312900d1…`),
  `hypridle.service.in` (`84859969…`), `omarchy-refresh-hypridle` (`a5c4e33a…`),
  `upstream-waybar-config.jsonc` (`ff387b21…`), `csdn-149787804.html` (`85bc4cc7…`, the 521 body),
  `csdn-164457293.html` (`0a038cd5…`, the 521 body).
- Host files were read, never written: `/home/vgpnk/.config/waybar/config.jsonc` (`a408a33d…`),
  `/usr/lib/systemd/user/hypridle.service` (`81939c3f…`), `~/.local/bin/{gkeep,ai-usage}` (symlinks),
  `~/.cache/ai-usage/status.json` (`ae44b170…` at the second read).

## 7. Risks and blockers

- **Risk (integration):** adopting a slice row by id alone would attach K1's waybar-config evidence
  to the `ai-usage` cache row (or vice versa). Any registry append must carry the round scope and
  the cited source in the same row, and `S205`/`S222` must not both be appended (duplicate evidence).
- **Risk (durability):** S224/S241 can never be quote-stable; if the lesson or an entry quotes the
  timestamp value again, the next census will flag it as ABSENT by construction.
- **Residual (declared, not a blocker):** the two CSDN rows are verified against the lane's own
  reader-proxy cache, not a live read — the live URL answers 521 to every plain client. The cache
  sha matches the row's recorded prefix, so the bytes are the ones the row was built from, but a
  future round cannot re-verify them from the source while CSDN keeps refusing.
- **No blocker.** Nothing in this slice needed a decision I could not derive; no row was guessed.
