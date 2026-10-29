# Theme & wallpaper plane — declared-file census (round 7, lane M7-2)

Assignment: round-7 plan stage (b) — the theme/wallpaper plane. This note
carries the plane's declared-file census in the **verify-gate's file-plane
discipline**: rows are measurements with anchors, the live layer is separated
from the declared layer, an unverifiable surface reads UNKNOWN, and the pass
proves the substrate byte-identical. **No verdict token** is issued here —
`MADO_VERIFY: CLEAN|DIVERGED` is the gate's vocabulary
(`tools/mado-verify.sh:9-13`); landing gate rows is stage (b), gated on stage
(a) green per `plans/round-7.plan.md:110-113`.

Probe window 2026-10-14 18:19:59Z–18:23Z (host offset −03:00). Read verbs
only: `ls/stat/readlink/sha256sum/wc/du/find/head/sed/grep/file/od/cat` on
files, `pgrep/ps/systemctl --user is-active/makoctl/gsettings/printenv`,
`hyprctl -j layers`, `omarchy theme current`, `omarchy version`, and
read-only reads of `~/.local/share/omarchy/**` sources (the SKILL declares
reading them safe and encouraged, `SKILL.md:202`). Scratch
`/tmp/w7-mado-m7-2/` (logs: `bg-plane.log`, `bg-live.log`, `chain-decl.log`,
`layers.log`, `tree-before.sha.txt`). The gate was run twice (live + no-live)
as the closing boundary proof.

**Fenced — never executed by this lane** (each rewrites operator-owned theme
state; writer semantics below are read from their sources, not from a run):
`omarchy theme set`, `omarchy theme bg next|set|install`, `omarchy theme
install|remove|refresh`, `omarchy-theme-set-templates`, `omarchy-theme-set-*`
(all), `omarchy-restart-*`, `omarchy-hook`. No file under `~/.config/**`,
`~/.local/share/omarchy/**`, `~/.local/state/omarchy/**`, `/etc/**` was
written; no compositor state was mutated. Secrets shape-only: none read.

Tags: `[OBS]` measured · `[INF]` inference from measured parts · `[UNK]`
unknown. Times UTC unless marked.

## §0 Relation to the record

Already noted: `terminals-and-omarchy.md` §4 (theme colors plane, MADO-3);
`remaining-planes-census.md` §1–§2 (round-6 census M6-3, the closest sibling —
its file counts, the 24+4 split, and the payload/template provenance are
re-measured and reproduced here); `idle-lock-plane.md` §2 (theme hyprlock.conf
pin); gate v1 (`tools/mado-verify.sh`, 1,186 L, sha256
`c4c1afb75dd1c8aa…` — round-6 landed revision, unchanged this pass).

What this note adds, all measured this window:

1. The **wallpaper path** as a three-sided chain (declaration → symlink →
   live swaybg + layer surface), with the writer's semantics read from
   `omarchy-theme-bg-next` (§3).
2. **Per-part consumer chains for all 25 theme entries** — the 24 files + the
   `backgrounds/` set — each with its declaring anchor and the live evidence
   that exists or provably does not (§2, §4).
3. Three consumer chains the round-6 census did not carry: the `btop.theme`
   symlink pair, `gum.env.conf` sourced through the default envs.conf with a
   **live `printenv` agreement**, and the `icons.theme`/`chromium.theme`
   live-side pairs (§4).
4. The **theme-name normalization joint** measured from the two scripts that
   produce both sides (§5).
5. A **paste-ready row spec** for the stage-(b) gate widening, with its
   landing conditions (§6).
6. The exact probes for the parts whose live chain stays unresolved (§7).

Corrections this note lands (append-only, no earlier text edited):

- The plan's design-time gate line refs (`plans/round-7.plan.md:29-32`,
  `:1014-1021`) are **pre-round-6**; at the landed revision the theme rows sit
  at `tools/mado-verify.sh:1102-1108` (re-measured). Round-6's refs
  (`SKILL.md` round-6 append: `:1104`, `:1108`) are the current ones.
- `remaining-planes-census.md` §2 listed the theme-note gate rows as
  `:1014-1020` (correct for gate v1 at that lane's probe); superseded by the
  line above, same content.

## §1 `~/.config/omarchy/current/` wiring — three entries `[OBS]`

| Entry | Shape | Content / anchor |
|---|---|---|
| `theme.name` | regular file, mode 644, 12 B, mtime 2026-10-03 17:49:02.617 −03 | `matte-black\n` (od: `m a t t e - b l a c k \n`); sha256 `48749715228bfa375bd84bef15ea0ad85b2ef88445607e8e6277bed103955c3b` |
| `background` | **symlink**, mode 777, 71 B link, same mtime +.620 −03 | absolute target `/home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg` |
| `theme/` | **real directory** (not a link), mode 755 | 24 files + `backgrounds/` (4 files); `du -sb` 3,718,129 B |

The `current/` dir itself is mode 755. `theme.name` is the machine name and
is the *only* file the theme-set ritual writes at the root (`echo "$THEME_NAME"
> …/current/theme.name`, `bin/omarchy-theme-set:45`). The symlink is the
wallpaper's declared pointer, retargeted by `omarchy-theme-bg-next` (§3).

## §2 `current/theme/` file census — 24 files + 4 backgrounds `[OBS]`

All regular files mode 644, mtime 2026-10-03 17:49:02 −03 (theme-set time).
sha256 shown as first-16; the eight pins marked ★ are the wall-plane critical
ones, full sha in §2.1.

| File | B | sha256 (16) | Consumer role (§4 unless noted) |
|---|---|---|---|
| `alacritty.toml` ★ | 772 | `8c3d1457c09d32e8` | terminal import chain |
| `btop.theme` | 2,648 | `e9ee6fb643852b37` | btop symlink pair |
| `chromium.theme` | 9 | `e02da2b72d23d24c` | browser policy pair |
| `colors.toml` ★ | 461 | `dbdd13a629aac86d` | template-render input (palette) |
| `foot.ini` | 378 | `d9c2e20e079a9314` | declared in foot config (binary absent) |
| `ghostty.conf` | 454 | `418636f99922f1ea` | declared in ghostty config (binary absent) |
| `gum.env.conf` | 5,413 | `ecab9ec497c55515` | sourced by default envs.conf |
| `helix.toml` | 4,582 | `c7f85d447f480b00` | install-time reference only (helix absent) |
| `hyprland.conf` ★ | 143 | `79126bec8c28da30` | hypr core source chain |
| `hyprland-preview-share-picker.css` | 1,844 | `24474e34a4ed9022` | share-picker stylesheets |
| `hyprlock.conf` ★ | 176 | `3ef010e72b5f6911` | hyprlock source chain |
| `icons.theme` | 9 | `1c2342215182a8e2` | GNOME icon-theme pair (live) |
| `keyboard.rgb` | 8 | `8f32a6ecf0de6c50` | ASUS keyboard scripts (hardware absent) |
| `kitty.conf` | 444 | `e8795b49ff5b6135` | declared in kitty config (binary absent) |
| `mako.ini` ★ | 119 | `95bf0c86c955cc81` | mako config symlink target |
| `neovim.lua` | 150 | `ec7df5fb1d3b7fc6` | nvim plugin symlink target |
| `obsidian.css` | 2,523 | `d195eeaf760f9d87` | vault theme writer source |
| `preview.png` | 470,315 | — (image) | elephant themes provider |
| `preview-unlock.png` | 22,524 | — (image) | elephant unlocks provider |
| `swayosd.css` ★ | 166 | `f88118e98b44cfa3` | swayosd style import |
| `unlock.png` | 2,512 | — (image) | unlocks provider / plymouth setter |
| `vscode.json` | 65 | `18171ea89a57d463` | vscode-setter read (code absent) |
| `walker.css` ★ | 191 | `f44cb45063494d2f` | walker theme css import |
| `waybar.css` ★ | 68 | `a1807a176659d7d6` | waybar style import |

Cross-checks: every ★ pin reproduces the round-6 census §1.3 prefix; the
`hyprlock.conf` pin equals `idle-lock-plane.md` §2; the `mako.ini` pin equals
the R3-1 mako pin — the symlink chain resolves to these bytes.

`backgrounds/` (4 files, all mtime 17:49):

| File | B | sha256 | Type |
|---|---|---|---|
| `0-ship-at-sea.jpg` (active) | 1,681,677 | `55fa691adfd3fb8a9102b826a28d8de679938f04879799da499b8ace2fe039ac` | JPEG 3840×2160 |
| `1-dark-waters.jpg` | 1,033,920 | `98f0c2b65a2587d114949e8125c22f891c993e0305ca36537bd9b7a9869e8a93` | JPEG 3840×2160 |
| `2-dot-hands.jpg` | 482,067 | `e8d73aa65be29bf9d0bec62f64add450485ca52367701ff683e0f2bd66f0791a` | JPEG 3456×2234 |
| `omarchy.png` | 4,491 | `63d002b2320cef0184d79bb44fbf4062780d2c083428acf16191344084b75a8f` | PNG 3840×2160 |

### 2.1 Full pins for the wall-plane critical files `[OBS]`

```
8c3d1457c09d32e83367ac946ff6e85f6bda334c302587a043bef7dc7ac09139  alacritty.toml
dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786  colors.toml
79126bec8c28da306712148734a3ee58335a8bd48bf863e4e2e2db6d6d8344b6  hyprland.conf
3ef010e72b5f69113e1500bb083fb053f9f121212ad5ed4fe74ad8d12507ad0b  hyprlock.conf
95bf0c86c955cc813d1b60d18e738567c7f135885c5f02a6acfbbb38946e3bec  mako.ini
f88118e98b44cfa32ebc2d8f2394bd0448b2d1e0c01f01dd48677fe66ec7522b  swayosd.css
f44cb45063494d2f4a8f489c47d8901b3bc98b27fbd1ca1c5a8801b40606bbc0  walker.css
a1807a176659d7d6beaaf2a5c96cb7a03d131ee2740b8961d4c9aee393839c18  waybar.css
```

`colors.toml` opens with `accent = "#e68e0d"`, `cursor = "#eaeaea"`,
`foreground = "#bebebe"`, `background = "#121212"` — the values that reappear
in the pairs below.

## §3 The wallpaper path — declaration → link → live `[OBS]`

1. **Declaration.** `default/hypr/autostart.conf:5`:
   `exec-once = uwsm-app -- swaybg -i ~/.config/omarchy/current/background -m fill`
   (read at the resolved path `~/.local/share/omarchy/default/hypr/autostart.conf`).
   The symlink (not a filename) is what the declaration names — retargeting it
   changes the wallpaper without touching any config.
2. **Link.** `current/background` resolves to
   `current/theme/backgrounds/0-ship-at-sea.jpg` (§1); target exists,
   non-empty (1,681,677 B), sha `55fa691a…`. The link is absolute → resolves
   inside `current/theme/backgrounds/` by construction.
3. **Live.** `pgrep -ax swaybg` → PID **1203358**, argv exactly
   `/usr/bin/swaybg -i /home/vgpnk/.config/omarchy/current/background -m fill`,
   ppid **1203316** (the Hyprland session process). `hyprctl -j layers` →
   monitor `DP-1`, level `0`, namespace **`wallpaper`**, pid **1203358**,
   geometry `3440x1440`; level `2` carries `waybar` (pid 1203352, `3440x26`).
   The wallpaper layer pid **equals** the swaybg pid — the layer-side identity
   agrees with the process-side argv.
4. **Writer semantics** (read from `bin/omarchy-theme-bg-next`, never run):
   backgrounds are gathered from `~/.config/omarchy/backgrounds/<theme.name>/`
   (user; **absent on this host** — probed) plus `current/theme/backgrounds/`,
   `find -L … -maxdepth 1 -type f` + `sort -z`, cycling with wrap-around;
   the link is set with `ln -nsf <target> <link>` and swaybg is relaunched as
   `setsid uwsm-app -- swaybg -i <link> -m fill` after `pkill -x swaybg`.
   Zero backgrounds → black `swaybg --color '#000000'`. Read as `[OBS]` source
   semantics; the running instance is the theme-set/bg-next-launched one, not
   re-created by this lane.

Fence: `omarchy theme bg next|set|install` are the mutating verbs here; a
theme set also always runs bg-next (`bin/omarchy-theme-set:48-50`, skippable
only via `OMARCHY_THEME_SKIP_BACKGROUND=1`).

## §4 Consumer chains — every theme part, installed consumers first `[OBS]`

"Resolved" = the declaring anchor is measured and the named file/process
exists this pass. Live *render* for a running process stays `[UNK]` unless a
consumer read surface exists (rule: `SKILL.md:234-237`).

| Theme part | Declaring anchor (file bytes) | Live side (probe) | Status |
|---|---|---|---|
| `hyprland.conf` | `~/.config/hypr/hyprland.conf:13` `source = …/current/theme/hyprland.conf` | include graph loads; `hyprctl configerrors` empty (gate run) | resolved |
| `hyprlock.conf` | `~/.config/hypr/hyprlock.conf:1` `source = …/current/theme/hyprlock.conf` | hyprlock not running; no lock surface by design | resolved file-level; render `[UNK]` |
| `waybar.css` | `~/.config/waybar/style.css:1` `@import "../omarchy/current/theme/waybar.css";` (1,887 B) | waybar PID 1203352, layer ns `waybar` `3440x26` | resolved |
| `walker.css` | `~/.config/walker/config.toml:3-4` (`theme = "omarchy-default"`, `additional_theme_location = …/default/walker/themes/`) → `…/omarchy-default/style.css:1` `@import "…/.config/omarchy/current/theme/walker.css";` (1,243 B) | walker PID 1203471 `--gapplication-service`; elephant PID 1203474 | resolved file-level; render `[UNK]` |
| `swayosd.css` | `~/.config/swayosd/style.css:1` `@import "../omarchy/current/theme/swayosd.css";` (372 B) | swayosd-server PID 1203475; unit active | resolved file-level; render `[UNK]` |
| `alacritty.toml` | `~/.config/alacritty/alacritty.toml:1` `general.import = [ "…/current/theme/alacritty.toml" ]` (876 B) | 3 alacritty windows (pids 1204373/1205237/2603289) | resolved file-level; render `[UNK]` |
| `mako.ini` | `~/.config/mako/config` symlink → `…/current/theme/mako.ini` (50 B link, mode 777) | mako PID 1203350; `makoctl mode` → `default` | resolved |
| `btop.theme` | `~/.config/btop/themes/current.theme` symlink (52 B, mode 777) → `…/current/theme/btop.theme`; `~/.config/btop/btop.conf:5` `color_theme = "current"` | btop binary present, **not running** | resolved file-level; render `[UNK]` |
| `gum.env.conf` | `default/hypr/envs.conf:3` `source = …/current/theme/gum.env.conf` (guarded by `hyprlang noerror true/false`), the envs.conf being sourced at `hyprland.conf:9` | **live env agrees**: `printenv FOREGROUND` → `#bebebe`, `printenv GUM_CONFIRM_PROMPT_FOREGROUND` → `#e68e0d` (file declares `env = FOREGROUND,##bebebe`, `env = GUM_CONFIRM_PROMPT_FOREGROUND,##e68e0d`) | resolved live |
| `icons.theme` | read by `bin/omarchy-theme-set-gnome:15-17` (`gsettings set … icon-theme "$(<icons.theme)"`) | `gsettings get org.gnome.desktop.interface icon-theme` → `'Yaru-red'` == file content | resolved live |
| `chromium.theme` | read by `bin/omarchy-theme-set-browser` → writes `/etc/chromium/policies/managed/color.json` | file pair: `chromium.theme` = `18,18,18` → `#121212` → policy `{"BrowserThemeColor": "#121212", …}` (65 B, mtime 17:49); chromium PID 2552209 running | file pair resolved; adoption `[UNK]` |
| `neovim.lua` | `~/.config/nvim/lua/plugins/theme.lua` **symlink** (52 B) → `…/current/theme/neovim.lua`; retarget documented in `migrations/1784518937.sh` | nvim binary present, not running | resolved file-level; render `[UNK]` |
| `hyprland-preview-share-picker.css` | `~/.config/hyprland-preview-share-picker/config.yaml:4` `stylesheets: ["../omarchy/current/theme/hyprland-preview-share-picker.css"]` (2,412 B) | picker not running | resolved file-level |
| `preview.png`, `preview-unlock.png`, `unlock.png` | `default/elephant/omarchy_themes.lua:31-33` (theme preview), `omarchy_unlocks.lua:49` (unlocks menu) | elephant PID 1203474; walker PID 1203471 | resolved file-level; UI render `[UNK]` |
| `colors.toml` | input of `bin/omarchy-theme-set-templates` (`COLORS_FILE="$NEXT_THEME_DIR/colors.toml"`, `:9`); values reappear in `chromium.theme` (`#121212`) and `keyboard.rgb` (`#e68e0d`) | render happened at theme-set time (17:49 mtimes) | resolved (generation input) |

### 4.1 Declared-only rows — installed-consumer gate leaves them inert `[OBS]`

| Theme part | Declared in | Missing consumer |
|---|---|---|
| `foot.ini` | `~/.config/foot/foot.ini:2` `include=…/current/theme/foot.ini` | `foot` binary absent |
| `kitty.conf` | `~/.config/kitty/kitty.conf:1` `include …/current/theme/kitty.conf` | `kitty` absent |
| `ghostty.conf` | `~/.config/ghostty/config:2` `config-file = ?"…/current/theme/ghostty.conf"` | `ghostty` absent |
| `vscode.json` | `bin/omarchy-theme-set-vscode` reads it | `code` absent |
| `helix.toml` | `bin/omarchy-install-helix` references it | `helix` absent |
| `keyboard.rgb` | `bin/omarchy-theme-set-keyboard` → `-asus-rog`/`-f16` scripts read it | `asusctl` absent; no ASUS DMI vendor evidence read (`/sys/devices/virtual/dmi/id/sys_vendor` probe returned nothing) |
| `obsidian.css` | `bin/omarchy-theme-set-obsidian` syncs it into each vault's `.obsidian/themes/Omarchy/` | 1 vault, `.obsidian/` present, **`themes/Omarchy` absent** — the sync never landed in this vault (probe: vault path shape-only, no content read) |

Per the stage-(b) spec these rows stay **declared-only NOTEs** — never FAILs —
because the consumer is not installed (or, for obsidian, never materialized).

### 4.2 Inert artifacts — provably not consumed `[OBS]`

- `~/.config/omarchy/themed/alacritty.toml.tpl.sample` (2,729 B) — the renderer
  `bin/omarchy-theme-set-templates:38` globs `"$USER_TEMPLATES_DIR"/*.tpl` and
  `"$TEMPLATES_DIR"/*.tpl`; `*.tpl.sample` matches neither, and the file's own
  header says "Rename this file to: alacritty.toml.tpl (remove the .sample
  extension)". **The sample is inert** — this settles the plan's
  `themed/*.tpl.sample` open probe with a measured mechanism.
- `~/.config/omarchy/hooks/theme-set.d/show-theme-notification.sample` — the
  hook runner `bin/omarchy-hook:25` skips `[[ $hook == *.sample ]]`; the
  `theme-set.d` dir contains only this sample → the `theme-set` hook is a
  no-op here.
- Built-in templates: `default/themed/` holds **17 `*.tpl`** (re-counted:
  alacritty.toml, btop.theme, chromium.theme, foot.ini, ghostty.conf,
  gum.env.conf, helix.toml, hyprland.conf, hyprland-preview-share-picker.css,
  hyprlock.conf, keyboard.rgb, kitty.conf, mako.ini, obsidian.css,
  swayosd.css, walker.css, waybar.css) — these, not the theme's copies, are
  what render per-app files when a theme lacks one
  (`omarchy-theme-set-templates:38-45`; theme payload files are copied first
  and the renderer skips existing outputs, `:43`). `[INF]` — consistent with
  the payload/template split of M6-3 §1.5; not re-proven by a theme set.
- `~/.config/omarchy/themes/` — **0 entries** (no user themes), re-measured.

## §5 The theme-name normalization joint — measured from both scripts `[OBS]`

Both sides of the pair come from measured code, not convention:

- **Writer** (`bin/omarchy-theme-set:17`):
  `THEME_NAME=$(echo "$1" | sed -E 's/<[^>]+>//g' | tr '[:upper:]' '[:lower:]' | tr ' ' '-')`
  — the machine name written to `theme.name` is the argument lowercased with
  spaces → hyphens.
- **Reader** (`bin/omarchy-theme-current:9`):
  `cat theme.name | sed -E 's/(^|-)([a-z])/\1\u\2/g; s/-/ /g'` — the display
  name is derived by uppercasing the first letter after start/hyphen, then
  hyphens → spaces; missing file → `Unknown`.
- **Round-trip on this host's single theme**: `matte-black` → reader rule →
  `Matte Black` == `omarchy theme current` output (measured both). Reverse
  check: `printf 'Matte Black' | tr '[:upper:] ' '[:lower:]-'` → `matte-black`.

Rule boundary (never assumed general — per the plan's anti-claim): the reader
rule uppercases **letters only**, so a name containing digits does not
naively round-trip through a lower/space-swap — `[INF]` example from the
payload's own names: `retro-82` displays `Retro 82`. The gate row must apply
the *measured sed*, not a paraphrase. Only one theme is live on this host, so
generality across themes is `[UNK]` (§11.5). One more consumer artifact of the
same display form: `vscode.json` carries `"name": "Matte Black"` (65 B pin
§2) — the human form is written into theme payloads too.

## §6 Gate relation — measured state, and the stage-(b) row spec

Measured at the landed gate revision (1,186 L, sha `c4c1afb75dd1c8aa…`):

- Declared plane ids: `hypr|hypr-live|waybar|walker|terms|gate`
  (selftest regex alternation at `:352`, `:356`, `:371-375`); `row ` call
  sites 106 by line-count, plane-prefixed occurrences measured:
  hypr 23 · hypr-live 53 · waybar 17 · walker 5 · terms 10 · gate 3.
- `theme` prefix: **0 row sites**. The theme appears only as one
  record-level NOTE: `live.theme.current` (`:1102-1108`, "operator-owned; not
  a verdict input"). Its only live content today is `omarchy theme current`'s
  output string.
- Boundary machinery the new rows would ride: `boundary_hash()` (`:204`),
  the `gate boundary.readonly` row (`:821-832`), and NOTE-as-record semantics
  (`:29-30` header: NOTEs never flip the verdict).

**Paste-ready spec for stage (b)** (to land only after stage (a) regression
green, and only with a mutant covering each new clause — round-6 reading rule
2, `SKILL.md:596-599`). Plane id `theme`; row namespace `theme.*`:

| Row id | Layer | PASS | FAIL | Other |
|---|---|---|---|---|
| `theme.name.read` | file | `theme.name` exists, one line, matches `^[a-z0-9-]+$` | unreadable / malformed | UNKNOWN if HOME root lacks the tree |
| `theme.chain.hypr_include` | file | `hyprland.conf:13` equals the declared source line **and** the target exists | present but target missing / line moved | — |
| `theme.chain.hyprlock` | file | user `hyprlock.conf:1` sources the theme file, target exists | same | — |
| `theme.chain.waybar_css` | file | `waybar/style.css:1` imports the theme css, target exists | same | — |
| `theme.chain.alacritty` | file | `alacritty.toml:1` imports the theme toml, target exists | same | — |
| `theme.chain.mako_link` | file | `~/.config/mako/config` is a symlink resolving inside `current/theme/`, target exists | regular file / dangling / target outside | — |
| `theme.chain.walker_css` / `theme.chain.swayosd_css` | file | import line + target exist (installed-consumer-gated) | same | NOTE when the consumer is not installed |
| `theme.wallpaper.link` | file | symlink resolves inside `current/theme/backgrounds/` to a non-empty file | dangling / outside / empty | — |
| `theme.wallpaper.live` | live | swaybg argv names the background **symlink** with `-m fill`; level-0 `wallpaper` layer pid == swaybg pid | consumer/argv/layer disagreement | NOTE if no swaybg (open finding, mirroring `live.consumer.hypridle`); UNKNOWN if hyprctl unavailable |
| `theme.name.display_agree` | live | `omarchy theme current` == reader-rule(`theme.name`) | — | NOTE on a pair the rule does not join (record the pair, never force); UNKNOWN if `omarchy` absent |
| `theme.choice` | live | — | — | NOTE always (operator-owned; today's `live.theme.current` row, unchanged) |
| `theme.parts.declared_only` | file | — | — | NOTE listing the §4.1 parts whose consumer is absent |

Census impact when landed: plane ids 6 → 7; the four selftest regex sites
(`:352`, `:356`, `:371-375`) must widen to include `theme` or the new rows go
uncounted (round-6 hand-forward, `SKILL.md:662-667`); expected steady-state
counts change by the added PASS/NOTE sites. Fence rows: the spec observes the
theme plane and never sets it — no `theme set`, no `bg *`, no restarts.

## §7 Parts whose live chain stays unresolved — exact probes, no inferred consumer `[UNK]`

1. `walker.css` — probe: `pgrep -ax walker` → 1203471 (`--gapplication-service`);
   the import chain is file-measured (§4); whether the running walker renders
   the current css requires opening the launcher or restarting it → not
   executed (mutation). `[UNK]`.
2. `swayosd.css` — probe: `pgrep -ax swayosd-server` → 1203475; unit
   `swayosd-server.service` active. Render `[UNK]` (same reason).
3. `btop.theme` — probe: symlink pair (§4) + `pgrep -x btop` → empty (not
   running); rendering `[UNK]`.
4. `themed/*.tpl.sample` rendering — **settled inert** (§4.2): glob + file
   header measured; not rendered unless renamed to `*.tpl`.
5. Theme previews (`preview.png` etc.) — probe: referenced by the elephant
   providers (`omarchy_themes.lua:31-33`); the picker UI was not opened;
   render `[UNK]`.
6. `mako` layer-surface mapping — this pass `hyprctl -j layers` shows only
   `wallpaper` + `waybar` (no `notifications`), consistent with M6-3's E2
   ("not permanently mapped"); the mako process is unchanged (1203350).
   Layer rows are probe-window statements.

## §8 Boundary proof `[OBS]`

- Combined theme-tree hash over `find …/current/theme -type f` (sorted) +
  `readlink current/background` + `theme.name`:
  before = after = `f94687b0c231f9ce3aff30a57267ecc27eb9bcdf4fd06b77de5b63d9353434a6`.
- Gate run 2026-10-14 18:22:56Z (read-only): `MADO_VERIFY: CLEAN (35 pass,
  0 fail, 0 unknown, 4 notes)`, rc 0; `gate boundary.readonly PASS "config
  plane byte-identical before/after (combined sha bb2639d9a980…)"`. File-plane
  companion: `--no-live` → `CLEAN (17 pass, 2 notes)`, rc 0, same boundary
  sha. Gate file sha `c4c1afb75dd1c8aa…` identical before/after.
- No mutating verb ran (§ header fence); no substrate file written; scratch
  confined to `/tmp/w7-mado-m7-2/`.

## §9 Spot-checks (reproducible, read-only)

1. **Wallpaper three sides** — `readlink ~/.config/omarchy/current/background`
   → `…/theme/backgrounds/0-ship-at-sea.jpg`; `sha256sum` that path →
   `55fa691adfd3fb8a…`; `pgrep -ax swaybg` → `1203358 /usr/bin/swaybg -i
   /home/vgpnk/.config/omarchy/current/background -m fill`; `hyprctl -j layers`
   → DP-1 level 0 ns `wallpaper` pid 1203358.
2. **Name joint** — `cat ~/.config/omarchy/current/theme.name` → `matte-black`;
   `omarchy theme current` → `Matte Black`; `cat
   ~/.local/share/omarchy/bin/omarchy-theme-current` shows the sed rule; the
   round-trip is `printf 'Matte Black' | tr '[:upper:] ' '[:lower:]-'`.
3. **Live consumer pairs** — `printenv FOREGROUND GUM_CONFIRM_PROMPT_FOREGROUND`
   → `#bebebe` / `#e68e0d` (theme gum.env.conf); `gsettings get
   org.gnome.desktop.interface icon-theme` → `'Yaru-red'` (theme `icons.theme`);
   `cat /etc/chromium/policies/managed/color.json` → `"#121212"` (theme
   `chromium.theme` `18,18,18`).
4. **Inertness proofs** — `sed -n '41,48p'
   ~/.local/share/omarchy/bin/omarchy-theme-set-templates` (globs `*.tpl`);
   `sed -n '19,27p' ~/.local/share/omarchy/bin/omarchy-hook` (skips `*.sample`);
   `ls ~/.config/omarchy/themed/` (only the sample).
5. **Gate** — `bash tools/mado-verify.sh` → `MADO_VERIFY: CLEAN (35 pass, 0
   fail, 0 unknown, 4 notes)` with `boundary.readonly PASS`.

## §10 Errata (append-only — add blocks, never edit above)

- E1 (2026-10-14, M7-2 seed): new note; no corrections to earlier notes
  recorded yet. Cross-checks applied: round-6 census §1–§2 counts and pins
  reproduced (24+4 files, `du -sb` 3,718,129, the ★ prefixes); `SKILL.md`
  round-6 append's gate line refs (`:1104`, `:1108`) reproduced; the plan's
  `:1014-1021` refs corrected in §0. Obsidian vault probe read as
  shape-only (existence of `.obsidian/` and of the `themes/Omarchy` dir);
  no vault content read.

## §11 Unknowns and hand-forward

1. Live render of the running consumers (walker, swayosd, alacritty, waybar,
   btop-when-running) for today's theme bytes — needs an open/inspect or a
   restart; both are operator/mutation-only. `[UNK]` (unchanged from M6-3).
2. Chromium policy adoption: the policy file matches the theme hex, but
   whether the running chromium re-read it in-session is unverifiable without
   a restart. `[UNK]`.
3. Obsidian chain: the single vault has no `themes/Omarchy` dir — whether
   theme-set was run before the vault existed, or the sync failed, is `[UNK]`;
   the probe is exact and re-runnable (§4.1).
4. `omarchy-restart-swayosd` etc. run at theme-set time, but which of the
   restarts actually respawned a process (vs `pgrep` guard skips, e.g. btop
   absent) is `[UNK]` — needs a theme set, which is fenced.
5. Generality of the display-name rule beyond the one live theme (§5) —
   `[UNK]`; the gate row compares through the measured sed, so the row is
   still exact on this host.
6. Landing: this census's §6 spec is **not** gate rows; stage (a)
   (`MADO_REGRESSION: PASS`) gates it, and a mutant per new clause is required
   before shipping (round-6 reading rules). The `theme` plane id must be added
   to the four selftest regex sites in the same change.
7. `LOG.md` entry for this round is the scribe/finalizer lane's write
   (AGENTS.md:3) — this lane's write scope was this file only.
