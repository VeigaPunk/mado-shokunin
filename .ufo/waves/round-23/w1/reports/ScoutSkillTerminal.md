# ScoutSkillTerminal — C2 recon: every foot / kitty / ghostty statement in the four named files

Read-only scout. No file in the lane repo was edited except this report. No jj, no git write, no
package transaction, no terminal/launcher run, no compositor probe. Host reads were `sed`, `grep`,
`cat`, `wc`, `stat`, `sha256sum`, `ls`, `command -v`, `pacman -Q` (all read-only and allowed by the
contract; `pacman -Q` is explicitly permitted).

## Answer in one paragraph

A new `corpus/knowledge/terminal-trees-r23.md` would **supersede four scope/negative statements**
(`terminal-route-r17.md:5`, `:17`, `terminals-and-omarchy.md:98`, `:165`, plus the README frontier
clause at `corpus/README.md:123-124`), **correct or narrow five claims** (§2.2 below, each from
already-corpus-sourced material plus today's read-only probe), and **leave every measured host
byte intact** — all of MADO-3's §1/§2/§3/§5/§6 anchors reproduce exactly today. A short decision
table fits as a new `###` subsection at the end of `SKILL.md` §Config-plane map, **insertion line 120**
(between the plane-map row at `:119` and `## Claim → evidence-class routing` at `:121`), and it
**cannot touch the frontmatter (lines 1-4)** because every candidate insertion is ≥ line 90 and no
tool in this repo parses mado's SKILL.md. The frontier sentence the note updates is
`corpus/README.md:122-125`, and the clause that becomes false is exactly
**"(foot, kitty and ghostty trees remain unsourced)"** at `:123-124`.

## Method — exact commands and the outputs that carry a claim

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
wc -l -c SKILL.md corpus/README.md corpus/knowledge/terminals-and-omarchy.md corpus/knowledge/terminal-route-r17.md
  → SKILL.md 1985 L / 169402 B; README 177 L / 40122 B; MADO-3 204 L / 15492 B; route-r17 152 L / 11450 B
sha256sum SKILL.md corpus/README.md corpus/knowledge/terminals-and-omarchy.md corpus/knowledge/terminal-route-r17.md
  → f8f856c5f583394fc830b4cfb6c1e340505b2962a20957dbabbd7af0a2fbca42  SKILL.md
  → 419683dbf3b41e1d63b7edee7e800208c2a4c0374f70249fb9a0c37210588fd2  corpus/README.md
  → ac8c94ad6fd623e887cfdfad0c772ab04f4fc84b0fc9f79eec6298e6876197b0  corpus/knowledge/terminals-and-omarchy.md
  → 8ae41c4c889d93531e8cff2593923165ef3e227ff17f536aae68ec8fb8d632af  corpus/knowledge/terminal-route-r17.md
git rev-parse HEAD → a28e4815aabfa85f55274884000fb2608355f8cf   (matches the round-23 registration base)
grep -niE 'foot|kitty|ghostty' <each of the four files>          (line inventory: §1)
grep -nE '^#{1,4} ' SKILL.md                                     (section map: §3)
grep -nE 'SKILL\.md:[0-9]' SKILL.md                              (self line-pins: §3.3)
grep -cinE 'foot|kitty|ghostty' corpus/SOURCES.md → 0            (no registry row names any of the three)
grep -oE '^\| S[0-9]{3}' corpus/SOURCES.md | tail -3 → S120 S121 S122   (highest id in the registry)
grep -c '2026-10-22' corpus/SOURCES.md → 0                       (no row opened today yet)
```

Read-only host probes (2026-10-22), all non-mutating:

```
command -v alacritty foot footclient kitty ghostty → /usr/bin/alacritty only
pacman -Q foot kitty ghostty alacritty
  → error: package 'foot' was not found ; 'kitty' was not found ; 'ghostty' was not found
  → alacritty 0.17.0-1
ls -l /usr/bin/foot /usr/bin/kitty /usr/bin/ghostty → all three: No such file or directory
ls -la ~/.config/{alacritty,foot,kitty,ghostty}   → the four trees + .bak.20261003-190229 siblings, mtimes Oct 3 19:02
wc -c/-l + sha256sum on foot.ini / kitty.conf / ghostty/config → values in §5
ls ~/.local/share/applications | grep -iE 'foot|kitty|ghostty|alacritty'
  → Alacritty.desktop 452 B ; foot-server.desktop 28 B ; footclient.desktop 28 B   (no kitty, no ghostty entry)
ls /usr/share/applications/*{foot,kitty,ghostty}* → all absent (only a 374 B root-owned Alacritty.desktop)
cat ~/.local/share/applications/foot{client,-server}.desktop → both exactly: "[Desktop Entry]" + "Hidden=true"
cat -n ~/.config/xdg-terminals.list → :3 "Alacritty.desktop"; 127 B
ls /etc/xdg/xdg-terminals.list → absent ; ls /usr/share/xdg-terminal-exec/xdg-terminals.list → 1053 B, Sep 18
ls ~/.config/*-xdg-terminals.list /etc/xdg/*-xdg-terminals.list → absent (no desktop-prefixed lists)
sha256sum ~/.config/{foot/foot.ini,kitty/kitty.conf,ghostty/config} + the three .bak files → §5
```

---

## 1. Statement inventory — every foot / kitty / ghostty statement, by file and line

Class column: **HB** = host-byte measurement (falsifiable by re-reading the file), **SEM** =
semantics/effect asserted without an upstream source, **SCOPE** = a scope/negative claim about what
is or is not sourced, **HIST** = dated historical append, **IDX** = navigation/index text.

### 1.1 `SKILL.md` (1985 L, `f8f856c5…`) — 4 lines name the three trees

| Line | Section | Statement (verbatim excerpt) | Class |
|---|---|---|---|
| 90 | §Config-plane map → **Who-owns-it table** (`###` at `:69`), row "Terminal font / padding / keybinds" | `per-terminal file (alacritty/foot/kitty/ghostty); colors via theme include; only Alacritty installed` … verify `command -v <term>`; file read … anchors `MADO-3 §1-3, §5` | HB + IDX |
| 118 | §Config-plane map → **Plane map** (`###` at `:105`), row "terminals" | `~/.config/{alacritty,foot,kitty,ghostty}/ — only Alacritty installed (MADO-3 §1/§5)`; consumer `per-terminal binary; omarchy restart terminal (omarchy skill:172)`; live route `file bytes + command -v`; operator-only `restart; omarchy install terminal` | HB + IDX |
| 952 | §Round-6 append → `###` Watch arm 2 (`:943`) | `live windows (alacritty 0.17.0-1; foot/kitty/ghostty absent)` | HIST |
| 1413 | §Round-9 append → gate registry row `theme.parts.declared_only` | NOTE `the §4.1 parts whose consumer is absent (live: 6 — foot.ini, kitty.conf, ghostty.conf, helix.toml, vscode.json, keyboard.rgb)` | HIST (landed gate note) |

Adjacent, terminal-generic lines that a note must not contradict:

| Line | Statement |
|---|---|
| 8 | body subtitle: "the Hyprland/waybar/walker/**terminal** config plane" (frontmatter `description` at `:3` says only "desktop & compositor craft") |
| 218 | mutating list: `omarchy restart waybar|walker|terminal` — operator only |
| 270 | checklist step 2: baseline "waybar/walker/mako/**terminal**/theme" files |
| 379 | §Omarchy boundary: skill ritual "**terminal** restart (`:172`)" |
| 667-669 | §Evidence trail: `terminals-and-omarchy.md (MADO-3, 179 L by wc -l; editor 180): terminals §1-2, invariants §3, theme plane §4, install state §5, backup delta §6, skill anatomy §7` |
| 736 | gate scope sentence: "One command verifies the declared planes (hypr core, waybar, walker, **terminals**)" |

### 1.2 `corpus/knowledge/terminal-route-r17.md` (152 L, `8ae41c4c…`)

| Line | Section | Statement | Class |
|---|---|---|---|
| 5 | frontmatter `scope:` | `one Alacritty-only route (selection chain + config import); foot, kitty and ghostty trees are not sourced here` | SCOPE |
| 14-17 | body intro | "Companion measured inventory: `corpus/knowledge/terminals-and-omarchy.md` (2026-10-14, all four terminal trees …). This note adds the sourced upstream contract; **it covers Alacritty only, not foot, kitty or ghostty.**" | SCOPE |
| 44-46 (bullet opens at `:40`) | §Upstream contract, "Working directory option" bullet | "the applicability check … reads `Categories` for `TerminalEmulator` (xdg-terminal-exec:816-822), `TryExec` (:933-937) and **`Hidden` (:938-942)**, is enforced at :1088-1090" — the already-sourced reason a `Hidden=true` entry can never be selected | SEM (sourced, S057) |
| 55 | §Upstream contract, compliance bullet | quote: `"Some examples of compliant terminals: xterm, alacritty, kitty, foot, qterminal"` (README.md:264, from S056) — the only place in the corpus where kitty/foot appear as named upstream-compliant terminals | SEM (sourced, S056) |

### 1.3 `corpus/knowledge/terminals-and-omarchy.md` (MADO-3, 204 L, `ac8c94ad…`)

| Lines | Section | Statement | Class |
|---|---|---|---|
| 17 / 18 / 19 | §1 What exists table | foot `516 B / 25 L`, kitty `954 / 34`, ghostty `1325 / 41`; all mtime `2026-10-03 19:02`; backups `513 / 953 / 1322 B` | HB |
| 21-23 | §1 note | naming split "ghostty's file is `config` (no extension) … matching the paths the omarchy skill lists at `SKILL.md:166-169`" | HB (+ omarchy-skill anchor, verified correct) |
| 41-50 | §2 `### foot.ini (25 lines)` | `include=…theme/foot.ini` `:2`; `term=xterm-256color` `:3`; `initial-window-mode=windowed` `:6`; font `:4`; `pad=14x14` `:5`; `workers=0` `:7`; `[scrollback] lines=10000` `:9-10`; cursor block/blink=no `:12-14`; clipboard binds `:16-19`; `[text-bindings]` `\x1b[13;2u=Shift+Return`, `\x1b[13;4u=Mod1+Shift+Return` `:21-25` | HB anchors + SEM wording ("Imports the theme", "Text bindings map …") |
| 52-60 | §2 `### kitty.conf (34 lines)` | `include …theme/kitty.conf` `:1`; font/bold_italic/font_size `:4-6`; `window_padding_width 14`, `hide_window_decorations yes`, `confirm_os_window_close 0` `:9-11`; `ctrl+insert copy_to_clipboard`, `shift+insert paste_from_clipboard` `:14-15`; `shift+enter → send_text all \e[13;2u` `:17`; `alt+shift+enter` `:19`; `allow_remote_control yes` `:22`; cursor/shell-integration/bell `:25-28`; tab bar `:31-34` | HB anchors + SEM ("Allow remote access") |
| 62-71 | §2 `### ghostty/config (41 lines)` | optional theme include `config-file = ?"…theme/ghostty.conf"` `:2`; font `:5-7`; window keys `:10-15`; cursor `:18-19`; `shell-integration-features = no-cursor,ssh-env` `:21-23`; keybinds incl. `resize_split` ×4 `:26-35`; `mouse-scroll-multiplier = 0.95` `:38`; `async-backend = epoll` `:40-41` | HB anchors + SEM |
| 75-80 | §3 Cross-terminal invariants | same font family (`:75`), same size 12.5 (`:76`), padding 14 (`:77`), insert pair (`:78`), Shift/Alt+Shift Return CSI-u (`:79`), block cursor blink-off for foot/kitty/ghostty (`:80`) | HB (all anchors re-checked, §2.3) |
| 81 | §3 last bullet | "**Every file delegates colors to the omarchy theme include; none carries a hex color itself**" | HB for the include lines; the ghostty include is *optional-marked* (`?`) |
| 86 | §4 theme plane | theme dir holds `foot.ini`, `kitty.conf`, `ghostty.conf` per-app color files | HB |
| 87 | §4 palette | palette anchors incl. `theme/foot.ini:2-3`, `theme/kitty.conf:1-2,9-10`, `theme/ghostty.conf:1-5,7-10` | HB |
| 93 | §5 install state | `command -v foot/kitty/ghostty → no output (not found), 2026-10-14` | HB (dated) |
| 96 | §5 | "foot launcher entries are **hidden stubs**: `footclient.desktop` and `foot-server.desktop` are 28-byte files containing `[Desktop Entry]` + `Hidden=true`" | HB |
| 97 | §5 | `~/.config/xdg-terminals.list` (127 B) lists `Alacritty.desktop` as first choice; `/etc/xdg/xdg-terminals.list` does not exist | HB |
| 98 | §5 observation + inference | "**config trees exist for all four terminals, but only Alacritty is installed and referenced. kitty/foot/ghostty configs are inert on this host until their packages are installed (`omarchy install terminal`).**" | HB premise + INF conclusion |
| 106-108 | §6 backup delta | font size 9 → 12.5 in `foot.ini:4`, `kitty.conf:6`, `ghostty/config:7` | HB |
| 165 | §8 Inferences | "**kitty/foot/ghostty configs are inert here** because their packages are absent" | INF |
| 168-169 | §8 Unknowns (1) | "whether `foot`/`kitty`/`ghostty` binaries exist outside PATH (only PATH was probed)" | UNK |
| 170-171 | §8 Unknowns (2) | "whether `omarchy restart terminal` actually restarts kitty/foot/ghostty when installed" | UNK |
| 198-201 | §Errata (round 2) | palette/§5 re-measure record; "both foot stubs 28 B" | HIST |

### 1.4 `corpus/README.md` (177 L, `419683db…`)

| Line | Section | Statement | Class |
|---|---|---|---|
| 14 | Coverage map, MADO-3 row | "only Alacritty installed of alacritty/foot/kitty/ghostty (`command -v` sweep §1); per-terminal key settings (§2) and cross-terminal invariants (§3) …" | IDX |
| 43 | Coverage map, `terminal-route-r17.md` row | "Documentary route … to the Alacritty v0.17.0 config-import contract. **Which terminal actually launches and reload effects stay `[UNK]`.**" | IDX |
| 65 | §Province routes, row "Alacritty / foot / kitty / ghostty" | Start here: terminal plane §§1–6 + runtime census §3. Limit: "Only Alacritty was installed in the recorded sweep; the other configs are declarations, not tested consumers." | IDX |
| **122-125** | §Frontier, round-17 bullet | `- Round 17 moves P6 screen/idle (hypridle/hyprlock) and one Alacritty-only` / `  P4 terminal route onto **documentary** sourced ground (foot, kitty and` / `  ghostty trees remain unsourced): [idle/lock route](knowledge/idle-lock-route-r17.md)` / `  and [terminal route](knowledge/terminal-route-r17.md). Still open: idle/lock` | SCOPE (frontier) |

---

## 2. What a sourced note on the three trees supersedes, corrects, or leaves intact

### 2.1 Superseded outright (the note makes them false)

1. `terminal-route-r17.md:5` — "foot, kitty and ghostty trees are **not sourced here**".
2. `terminal-route-r17.md:17` — "it covers Alacritty only, **not foot, kitty or ghostty**".
3. `terminals-and-omarchy.md:98` (second sentence) — "kitty/foot/ghostty configs are inert on this host
   until their packages are installed" (see 2.2a: the "until installed" rule is incomplete, not merely unsourced).
4. `terminals-and-omarchy.md:165` — "kitty/foot/ghostty configs are inert here because their packages are absent".
5. The frontier clause at `corpus/README.md:123-124` — "(foot, kitty and ghostty trees remain unsourced)".

Because both notes are append-only under the lane's own rule (`SKILL.md:39` "Errata append-only"),
items 1-4 are recorded as an errata/pointer block in the new note, **not** by editing those lines.
Only the README frontier bullet is superseded in the README's established way (2.5 / §4).

### 2.2 Corrected or narrowed (derivable now from corpus-sourced material + read-only host bytes)

**a. `MADO-3:98` "inert … until their packages are installed" is an incomplete liveness rule.**
Installing foot would still not make `xdg-terminal-exec` choose it: the host's only foot desktop
entries are `Hidden=true` (`~/.local/share/applications/footclient.desktop` and `foot-server.desktop`,
28 B each, re-read 2026-10-22), and the resolver's applicability check reads `Hidden` — an
already-sourced fact in this corpus at `terminal-route-r17.md:44-46` (xdg-terminal-exec:938-942, S057).
The live selection list names only `Alacritty.desktop` (`~/.config/xdg-terminals.list:3`). Confidence: high.

**b. `MADO-3:168` unknown (1) — closed.** Not merely "outside PATH": `pacman -Q foot kitty ghostty`
returns "package … was not found" for all three, and `/usr/bin/{foot,kitty,ghostty}` do not exist.
A 2026-10-22 note may state they are not installed at all (package-level absence, not a PATH artifact).
Confidence: high (read-only `pacman -Q`, explicitly permitted by the contract).

**c. Quote-shape defects that a verbatim re-quote fixes.** `MADO-3:57` writes
`ctrl+insert copy_to_clipboard`, `shift+insert paste_from_clipboard`, but the file's lines are
`map ctrl+insert copy_to_clipboard` / `map shift+insert paste_from_clipboard` (`kitty.conf:14-15`)
— the `map` keyword is dropped. Same shape at `MADO-3:69`, where ghostty's `keybind = ` prefix is
dropped for `:26-27`. Values and line anchors are correct; only the quoted text is shortened.
Every other quoted value in §2 matches the bytes exactly (`cat -n` cross-check, §2.3).

**d. `MADO-3:81` + `:64` — the ghostty include is optional-marked.** The include is
`config-file = ?"~/.config/omarchy/current/theme/ghostty.conf"` (`ghostty/config:2`); the `?` prefix
is a documented optional-file marker in ghostty's config grammar. The new note should state the
documented meaning (a missing theme file is tolerated, unlike the foot/kitty includes), which
sharpens the §3 "delegates colors" invariant. I did **not** open ghostty's docs, so this is a
candidate correction to source, not a finding (`[INF]`).

**e. `MADO-3:58` — `allow_remote_control yes` is stated at the strength of the file's own comment
("Allow remote access").** The documented effect (remote control via `kitten @`; a listening socket
only when `listen_on` is set) is what a source must bound. `[INF]` candidate; kitty's upstream is
being opened by a peer (`SrcKitty.md`: tag `v0.49.2`, commit `b2cb8712…`, 9 raw files, access date
2026-10-22) — coordinate rather than duplicate.

**f. All §2 semantics claims are the note's actual payload.** The unsourced effect wording in
`MADO-3` §2 that a source must carry: foot `include`, `initial-window-mode`, `[text-bindings]`
direction (`MADO-3:43-50`); kitty `include`, `map`/`send_text all`, `confirm_os_window_close`,
`allow_remote_control` (`:54-58`); ghostty `config-file`/`?`, `window-theme`, `resize_split`,
`shell-integration-features`, `mouse-scroll-multiplier`, `async-backend` (`:64-71`). Matching each
claim to its upstream key reference is the cheap way to make the note's rows falsifiable.

### 2.3 Left intact — re-measured 2026-10-22, identical

- `MADO-3:15-19` — foot `516 B/25 L`, kitty `954/34`, ghostty `1325/41`; backups `513/953/1322 B`;
  mtime `2026-10-03 19:02` on all six files. **Exact match.**
- `MADO-3` §2 line anchors for all three trees — verified line-by-line with `cat -n`; all correct.
- `MADO-3` §3 invariants `:75-80` — all anchors resolve (including the alacritty side `10-12`, `13`,
  `16-17`, `22-27`).
- `MADO-3:93` — `command -v` sweep still yields only `/usr/bin/alacritty`.
- `MADO-3:96` — both foot stubs are still exactly 28 B with `[Desktop Entry]` + `Hidden=true`.
- `MADO-3:97` — `~/.config/xdg-terminals.list` still 127 B, `:3` = `Alacritty.desktop`;
  `/etc/xdg/xdg-terminals.list` still absent (the system list that *does* exist is
  `/usr/share/xdg-terminal-exec/xdg-terminals.list`, 1053 B — the S060 path, a different file from
  the absent `/etc/xdg/` one; the note should keep both paths distinct).
- `MADO-3:106-108` — backup-vs-live delta is still the single font-size change (byte counts differ
  by exactly 3 B per file, as recorded).
- `MADO-3:21-23` — omarchy skill lists the four paths at its own `SKILL.md:166-169`; I read those
  lines: `alacritty.toml`, `foot.ini`, `kitty.conf`, `ghostty/config`. Anchor still correct.
- `SKILL.md:90`, `:118` — "only Alacritty installed" is **still true today**; the note re-sources
  the fact rather than correcting it. `SKILL.md:952` and `:1413` are dated records / a landed gate
  NOTE and must not be edited; `:1413`'s "live: 6" count stays exactly 6 (Alacritty is the only
  installed terminal, so all three tree parts remain declared-only).

### 2.4 One cross-note consistency point the note should state

The corpus carries **two different "system list" paths**: `/etc/xdg/xdg-terminals.list` (absent,
`MADO-3:97`) and `/usr/share/xdg-terminal-exec/xdg-terminals.list` (present, 1053 B, S060,
`terminal-route-r17.md:23`). Both statements are true; only their juxtaposition reads as a
contradiction. The note's route table should name both with their roles.

### 2.5 Corpus mechanical constraints the note must satisfy (C2 counter)

`.ufo/waves/round-23/c2/count.py` (read in full) requires, per terminal:

- a Markdown table row in `corpus/knowledge/terminal-trees-r23.md` whose **first cell** fullmatches
  the terminal name case-insensitively (optionally backticked) — `re.fullmatch(rf"`?{term}`?", row[0].lower())`;
- an `S\d{3}` token **on that same line** resolving to a `corpus/SOURCES.md` row with exactly
  **11 cells**, `status == "mined"` (cell 8) and `opened == "2026-10-22"` (cell 9);
- the registry **source cell** (cell 2, lowercased) must contain the terminal name.

Hence: S056's `README.md:264` compliance quote (opened 2026-10-20) can be *cited* but **cannot carry
the count**; each of the three needs a newly mined row opened today whose source string names it.
No SOURCES row currently mentions any of the three (grep count 0); highest existing id is **S122**;
zero rows are opened `2026-10-22` yet. The note file does not exist at base (verified `ls`).

---

## 3. Where a short SKILL.md decision table "which terminal tree is live on this host" fits

### 3.1 Recommended placement

**Section:** `SKILL.md` §Config-plane map — who owns this key (heading `##` at `:47`), as a new
`###` subsection **after the Plane map table**, i.e. **insert at line 120** — the blank line between
the last plane-map row (`:119`, "theme & wallpaper") and `## Claim → evidence-class routing` (`:121`).

Why this exact spot:

- The subsection's charter is already the right one — `:107-108`: "A scoped verification starts by
  picking a scope; this table says where each plane lives, what reads it, how it takes effect, and
  **which live route can verify it**." Liveness of a terminal tree is a scope gate.
- It sits immediately below the two lines that today carry the answer without a deciding procedure
  (`:90` Who-owns-it row, `:118` Plane map row), so those rows can gain a pointer instead of
  restating the rule; the two keep their content.
- It is above §Claim → evidence-class routing, so a top-down reader meets the scope gate before
  choosing a claim class.
- Heading depth matches its siblings (`###` at `:69` and `:105`).
- House table shape exists and is already indexed by this document: `MADO-2 §7`
  `| Situation | Action | Why (anchor) |` at `corpus/knowledge/waybar-walker-plane.md:320-331`,
  cited in `SKILL.md:667` ("decision table §7").

Suggested content shape (4 rows, one per tree; the `Action` is the deciding read, the `Why` is the anchor):

| Situation | Action | Why (anchor) |
|---|---|---|
| Which tree is live? | `command -v <term>` + `pacman -Q <term>`; read `~/.config/xdg-terminals.list`; read the `.desktop` entries' `Hidden=` | alacritty 0.17.0-1 installed; foot/kitty/ghostty not found (2026-10-22) |
| foot tree | declared-only — never a live consumer | no binary/package; both `foot*.desktop` are `Hidden=true` (28 B) — resolver reads `Hidden` (xdg-terminal-exec:938-942) |
| kitty tree | declared-only | no binary/package; no `kitty*.desktop` anywhere on the host |
| ghostty tree | declared-only | no binary/package; no `ghostty*.desktop` anywhere on the host |

### 3.2 Acceptable alternatives (both body-only, cheaper)

- **A2 — one row in §Claim-first routing** (`###` at `:134`), appended after the last row at `:148`
  (blank `:149`): "Which terminal tree is live on this host | consumer-side probe + file bytes |
  `command -v`/`pacman -Q`; `~/.config/xdg-terminals.list`; `Hidden=` in `~/.local/share/applications/*.desktop` | `[OBS]`".
  One line, no heading, no shift of the two tables above.
- **A3 — one row in §Error patterns & traps** (`##` at `:345`), after the last row `:369`:
  symptom "A full config tree must be the live terminal" → cause "tree presence ≠ consumer" →
  check as A2. This is the "trap" formulation and matches the section's existing rows.

**Avoid** `:93-103` (the four-trap paragraph): its lead-in says "**Four** traps" at `:93`, so a fifth
item forces an edit to a measured, dated paragraph for no gain. Avoid also the round appends
(`:952` round 6, `:1413` round 9) — those are dated records / a landed gate registry note.

### 3.3 Does it touch the frontmatter? No.

- `SKILL.md` frontmatter is **lines 1-4** only: `---`, `name: mado-shokunin`,
  `description: Domain specialist — desktop & compositor craft. Rank: shonen (probation).`, `---`.
  Every candidate insertion (§3.1, A2, A3) is at ≥ line 90, so the frontmatter block is untouched
  and the skill's name/description (its trigger surface) does not change.
- No tool in the repo reads mado `SKILL.md`: the only references are documentation comments in
  `tools/mado-verify.sh` (`:21`, `:66`, `:68`, `:2002`), an argv string in a policy self-test
  (`tools/mado-action-plan.py:553`, `action("repo-write", ["edit","SKILL.md"])`), and the rubric
  string `tools/mado-assessment.py:21`. No sha256 or line-count pin of mado `SKILL.md` exists in
  `PROVINCE.md`, `SHONEN.md`, `tools/`, or `.ufo/waves/round-23/repair/expected.json`.
- The corpus pins of mado `SKILL.md` length are already stale and unaffected by further growth:
  "tested SKILL `016ecd68…` 374 L" (`corpus/README.md:19`; the same version string heads
  `executor-test-sufficiency.md:35`) and "current `SKILL.md` reads 315 L"
  (`config-health-report-r3.md:591`) vs today's **1985 L**.
- Self line-pins inside `SKILL.md` (found by `grep -nE 'SKILL\.md:[0-9]'`): `:1773`, `:1860-1865`,
  `:1900-1908`, all written as "**former** `SKILL.md:NNN`" except `:1864`
  ("Earlier `ai-usage.conf` line in the shadowing example — `SKILL.md:338`"). That single unqualified
  pin is **already stale** — line 338 is scratch-copy text in §Reproduction package, and the
  shadowing example is at `:102-103`/`:144`. So an insertion at 120 cannot make a correct pointer
  wrong; if the lander wants the pin fixed, that is a new append-only errata line, not an edit.
- Adding a decision table *matches* the only SKILL.md-content rubric in the lane
  (`tools/mado-assessment.py:21` subject 1, mirrored at `SHONEN.md:5` "SKILL.md contains real
  decision tables, error patterns, checklists, cited sources"), so the change is rubric-neutral-to-positive.
- Note for the lander: `tools/mado-action-plan.py:553` classifies `edit SKILL.md` as a `repo-write`
  action, i.e. mado's own instrument treats this edit as a write — the L1 owns it, not an executor seat.

---

## 4. The exact `corpus/README.md` frontier sentence the note would update

Verbatim (`sed -n '122,125p'`), one bullet, four physical lines — the sentence ends at `:125`:

```
122  - Round 17 moves P6 screen/idle (hypridle/hyprlock) and one Alacritty-only
123    P4 terminal route onto **documentary** sourced ground (foot, kitty and
124    ghostty trees remain unsourced): [idle/lock route](knowledge/idle-lock-route-r17.md)
125    and [terminal route](knowledge/terminal-route-r17.md). Still open: idle/lock
```

The clause that becomes false, and the one the note must name, is exactly
**`corpus/README.md:123-124` — "(foot, kitty and ghostty trees remain unsourced)"**.

Landing pattern (do not edit the round-17 bullet): round 18 superseded a round-17 open item by
*appending* its own bullet — `corpus/README.md:130-132`: "Round 18 moves P3 Walker and P5
themes/wallpapers onto **documentary** sourced ground, **superseding the round-17 "P3 Walker and P5
theme/wallpaper sourced routes" open item**". A round-23 bullet should read the same way, e.g.
"Round 23 moves the foot, kitty and ghostty config trees onto documentary sourced ground
(terminal-trees-r23.md), superseding the round-17 'foot, kitty and ghostty trees remain unsourced'
clause; which terminal actually launches stays open."

Two companion README edits a new note normally carries (navigation only, both in the Coverage-map
table): a new row for `knowledge/terminal-trees-r23.md` (rows live at `:12-47`; nearest siblings
`:43` route-r17, `:14` MADO-3), and the `:65` province-route row's "Start here" cell gains the note —
its Limit text ("only Alacritty was installed in the recorded sweep; the other configs are
declarations, not tested consumers") stays true and should not change. The `:43` row's
"which terminal actually launches … `[UNK]`" also stays.

---

## 5. Ready evidence for the note author (measured 2026-10-22, read-only)

| File | Bytes | Lines | SHA-256 |
|---|---|---|---|
| `~/.config/foot/foot.ini` | 516 | 25 | `3e88354476f2682e7a1a0bc840d04e221e5c6a7312b3ee9dcf76ec16d0842e60` |
| `~/.config/kitty/kitty.conf` | 954 | 34 | `f875291ecfe64ebc4ddc588282bcdb20fb883769e9938148411efa378d7f1e70` |
| `~/.config/ghostty/config` | 1325 | 41 | `cb828c044b07d4fd924fe1d6b55c956035feb16f8d5c67899c8a598994596667` |
| `~/.config/foot/foot.ini.bak.20261003-190229` | 513 | — | `8afc9646c61e58e67f244e50a9ce5d4a45546920511a06b47f7443a3998da602` |
| `~/.config/kitty/kitty.conf.bak.20261003-190229` | 953 | — | `95eed20aaedb09627e00e3ff504919b585a54799aa41cb45bba5e17b91c8dd44` |
| `~/.config/ghostty/config.bak.20261003-190229` | 1322 | — | `e47630125605cb19c6b2c9bc33d767a0f3f1b5bf04cd4f36a2bb910897e24f78` |

`MADO-3` carries **no sha256** for the three trees (only byte/line counts); the six digests above
are the missing pins and can be cited directly by the note.

Other confirmed inputs: `~/.config/xdg-terminals.list` 127 B (`:3` `Alacritty.desktop`, lines 1-2 are
Omarchy template comments); `/etc/xdg/xdg-terminals.list` absent; `/usr/share/xdg-terminal-exec/xdg-terminals.list`
1053 B; `/usr/share/applications/Alacritty.desktop` 374 B root-owned, no foot/kitty/ghostty entries;
`~/.local/share/applications/` = Alacritty 452 B + two 28 B `Hidden=true` foot stubs; package state
`alacritty 0.17.0-1`, foot/kitty/ghostty not found; `corpus/knowledge/terminal-trees-r23.md` absent.

## 6. Confidence and remaining unknowns

Observed `[OBS]`: every line number, every quoted statement, every digest and probe output above —
read directly from the four named files and the host filesystem today; the four files' sha256 are
recorded in §Method so a later pass can prove they did not move.

Inference `[INF]`: the placement judgment in §3 (structural argument from the section's own charter
and the document's heading/table conventions), and the two candidate corrections 2.2d/2.2e, which
need upstream docs I did not open.

Remaining unknowns:
1. foot/ghostty upstream documentation — **not opened by me** (out of this ticket's scope; kitty's
   upstream is a peer's lane, `SrcKitty.md`, tag `v0.49.2`, opened 2026-10-22). Whether §2.2d/§2.2e
   hold is the note author's to source.
2. Whether the L1 wants the SKILL.md decision table at all — the C2 counter reads only the note file
   and `SOURCES.md`, so a SKILL.md edit adds zero counter value and is purely a usability call.
3. Whether the operator intends any of the three trees to become live (that would flip §2.2a from a
   correction to a live-route change); nothing on the host suggests it today.

## Verdict

**PASS (advice + evidence).** Line-anchored inventory of all 39 foot/kitty/ghostty statements across
the four named files (4 in `SKILL.md`, 4 in `terminal-route-r17.md`, 27 in `terminals-and-omarchy.md`,
4 in `corpus/README.md`), with the exact supersede/correct/intact split; the decision table's home is
`SKILL.md:120` (new `###` subsection under §Config-plane map, house shape from MADO-2 §7, two
body-only fallbacks at `:148` and `:369`); the frontmatter (lines 1-4) is provably untouched and no
tool or pin reads mado `SKILL.md`; and the frontier sentence to update is `corpus/README.md:122-125`,
whose false clause is `:123-124` "(foot, kitty and ghostty trees remain unsourced)". No file was
edited; all measurements are read-only and reproducible from the commands in §Method.
