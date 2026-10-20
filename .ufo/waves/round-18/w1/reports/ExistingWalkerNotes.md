# ExistingWalkerNotes — P3 corpus claim inventory for `walker-route-r18.md`

Assignment: read the existing walker notes and list (a) every claim the new
P3 route note must not contradict, (b) stale present-tense claims from the
walker 2.17.0 era, (c) open unknowns a documentary route can narrow. Leaf
scout; no edits outside this report.

Read at lane HEAD `d3a00003e6ef0b1e3c7b4faf52d592eb293857ba` (2026-10-20):

- `corpus/knowledge/walker-deep-r9.md` (399 L) — full.
- `corpus/knowledge/walker-live-surface.md` (301 L) — full.
- `corpus/knowledge/waybar-walker-plane.md` (475 L) — §3 walker, §6 drift,
  §7 decision table, §8 unknowns, §10 errata (R2-E2, R4-E3, R4-E4).
- `corpus/knowledge/arc-synthesis.md` (388 L) — §6 gap ledger, §7 classes.
- `corpus/knowledge/walker-deep.md` (617 L, round 5) — full skim, because
  r7/r9 route their errata/ledgers there and never landed them (§ Errata is
  still `_None yet_`).
- Upstream bodies already fetched by round-18 sibling seats under
  `.ufo/waves/round-18/fetch/` (walker v2.17.2 README/config/config.rs/
  theme/mod.rs/data.rs/main.rs; elephant v2.22.1 README/config.go; omarchy
  v3.8.4 walker scripts). I opened **no web source**, so this report creates
  no fetch receipt; every upstream quote below points at the sibling body and
  receipt that already exist.
- Host bytes read with `stat`/`sha256sum`/`wc`/`cmp`/`grep` only. No walker,
  elephant, pacman, systemctl, hyprctl, omarchy-*, compositor, socket or
  screenshot operation. No installs or upgrades.

Tags: **[OBS]** file read this pass, **[OBS-r9]** observation recorded in an
existing note (dated), **[SRC]** upstream source/doc at tag v2.17.2 (or
elephant v2.22.1) read from a sibling fetch body, **[INF]** inference with
basis, **[UNK]** not measurable.

Revision identities used throughout: walker v2.17.2 tag
`a515085fd39fae80acc086c8fbfd9b7771a9a11d` (receipt
`.ufo/waves/round-18/fetch/MadoR18.SrcWalkerThemes/walker-ls-remote-v2.17.2.txt`);
omarchy tag v3.8.4 = `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`
(`~/.local/share/omarchy/.git/packed-refs:2,508`, [OBS]).

---

## 1. What moved since the 2.17.0-era notes

| Object | 2.17.0-era pin (note) | Now | Evidence |
|---|---|---|---|
| walker package | `2.17.0-1` (r9 §1, r7 §1, walker-deep §1) | **`2.17.2-1`** (`2.17.0-1 -> 2.17.2-1`, 2026-10-20T09:16:46-0300) | `/var/log/pacman.log:2929` [OBS] |
| elephant package | `2.21.0-1` (walker-deep §1) | **`2.22.1-1`** (`2.21.0-1 -> 2.22.1-1`, 2026-10-20T09:31:03-0300) | `/var/log/pacman.log:3095` [OBS] |
| `/usr/bin/walker` | 6,661,264 B, sha256 `64826a85…` (r9 §1) | 7,039,912 B, mtime 2026-10-08 11:14:32 -0300; contents **[UNK]** this round | sibling `HostWalkerFiles.md` §1 stat [OBS]; binary not read here |
| packaged L1 `/etc/xdg/walker/config.toml` | 13,220 B / 298 L / sha `5b4e47b7…` (walker-deep §2.1, r9 §1) | **13,743 B / 305 L / sha `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b`** | [OBS]; equals walker v2.17.2 `resources/config.toml` byte-for-byte (`NoteWalker/walker-v2.17.2-resources-config.toml`) |
| walker v2.17.0 `resources/config.toml` | — | 13,220 B / 298 L / sha `5b4e47b7…` | [OBS] `SrcWalkerChangelog/walker-v2.17.0-resources-config.toml`; **proves the old L1 pin was the v2.17.0 tag file** |
| user L2 `~/.config/walker/config.toml` | 1,336 B / 49 L / sha `fecf71fa…` (all three notes) | **unchanged**, same sha | [OBS]; equals omarchy v3.8.4 `config/walker/config.toml` |
| omarchy theme files | layout 6,488 `dbb6bbbe…`; style 1,243 `481267af…`; `current/theme/walker.css` 191 B `f44cb450…` | **unchanged** | [OBS] |
| autostart desktop | 138 B `5cb9874e…` (r7 §1) | **unchanged**, `cmp`-equal to stock | [OBS] |
| elephant user TOMLs | 14/62/81 B, sha `2c0ef81b…`/`999b1915…`/`9c0d5edf…` (walker-deep §4.1) | **unchanged** | [OBS] |
| omarchy launch/restart/refresh scripts | 3.8.3-era claim lines (walker-deep §7.2, waybar-walker-plane §3.1) | host bytes **`cmp`-equal** to v3.8.4 tag bodies; claimed line numbers still exact | [OBS] `NoteWalker/omarchy-v3.8.4-bin-omarchy-{launch,restart,refresh}-walker` vs `~/.local/share/omarchy/bin/` |

Consequence: the walker **config file** claims survive; the walker **version,
binary, packaged default, elephant runtime and help/version surface** do not.
This is the split the new note must preserve.

---

## 2. Claims the new P3 note must not contradict

### 2.1 Host declarations that are still literally true (restate only with these bytes)

These are file-declaration claims, not behaviour. Contradicting them would
re-introduce measurements that no longer hold or would invent drift.

1. **User config shape and overrides** — `~/.config/walker/config.toml` 49 L /
   1,336 B / sha `fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787`;
   `force_keyboard_focus=true` :1, `selection_wrap=true` :2,
   `theme="omarchy-default"` :3,
   `additional_theme_location="~/.local/share/omarchy/default/walker/themes/"` :4,
   `hide_action_hints=true` :5, `max_results=256` :17, default providers
   `desktopapplications, websearch` :18-21, six `[[providers.prefixes]]`
   :23-45 (`/` providerlist, `.` files, `:` symbols, `=` calc, `@` websearch,
   `$` clipboard), one emergency `Restart Walker` → `omarchy-restart-walker`
   :47-49 (waybar-walker-plane §3, walker-deep §2.4, r7 §3). The file’s
   secret-shape scan (`token|secret|password|api_key|bearer`) still has no
   hits (r7 §3). [OBS]
2. **The user file is a byte-identical install copy of omarchy’s stock config**
   (`~/.local/share/omarchy/config/walker/config.toml`, same sha) — it is not
   a user-authored customization and not a full schema (walker-deep §1,
   HostWalkerFiles §2/§4). [OBS]
3. **Theme wiring**: exactly one theme dir under
   `~/.local/share/omarchy/default/walker/themes/` (`omarchy-default/`), whose
   `style.css:1` imports `../../../../../../../.config/omarchy/current/theme/walker.css`;
   that file is 6 `@define-color` lines, 191 B `f44cb450…`, values from
   `colors.toml` via `omarchy-theme-set-templates` (walker-deep §6.2,
   waybar-walker-plane §3). The theme CSS still hides item subtext
   (`.item-subtext` :97, `font-size: 0px` :98), italicizes the selected row
   (`.current` :109-110), and puts `.keybind-hints` at :113; the waybar
   note’s round-1 subtext anchor `:94-99` is off by three — re-anchor from
   current bytes. [OBS]
4. **Layout geometry and packaged theme set**: omarchy `layout.xml`
   `GtkWindow#Window` → `BoxWrapper` `width-request 644`; packaged default
   layout `600`/`height-request 570`; the packaged default theme still ships
   16 files (generic `item.xml`, 11 provider `item_*.xml`, `keybind.xml`,
   `layout.xml`, `preview.xml`, `style.css`) (walker-deep §6.2/§4.4;
   HostWalkerFiles §4 line 19-20). [OBS]
5. **Service and launch path**: `app-walker@autostart.service` generated from
   `~/.config/autostart/walker.desktop` (argv `walker --gapplication-service`);
   `Restart=always`/`RestartSec=2` drop-in; `omarchy-launch-walker:5-14`
   starts elephant, ensures the service, then `exec walker --width 644
   --maxheight 300 --minheight 300 "$@"`; `omarchy-restart-walker:5-15`
   restarts elephant (when enabled) then the walker service, else prints
   `Unable to restart Walker -- RESTART MANUALLY`; `omarchy-refresh-walker`
   refreshes configs and **omits `elephant/symbols.toml`** (walker-deep §7.2,
   r7 §1, waybar-walker-plane §3.1). `~/.config/hypr/autostart.conf` does not
   launch walker (only the commented template plus the Grok Bot exec-once).
   Host scripts are `cmp`-equal to the
   v3.8.4 tag bodies; line numbers hold. [OBS]
6. **Launcher bindings**: stock `utilities.conf:2` `SUPER, SPACE` →
   `omarchy-launch-walker`; `utilities.conf:3` `SUPER CTRL, E` → `-m symbols`;
   `clipboard.conf:5` `SUPER CTRL, V` → `-m clipboard`; the user
   `~/.config/hypr/bindings.conf` keeps them commented (:34-35, :40); the bar
   left click is `omarchy-menu` at `config.jsonc:58`; `omarchy-launch-screensaver:18`
   runs `walker -q`; `omarchy-menu` closes a live dmenu with `walker --close`
   (:21-22) and opens menus with `-m menus:…` (:269, :298, :302) and
   `walker -p "Launch…"` (:857). Note R2-E2 already superseded the older
   “no active launcher bind” wording: SUPER+SPACE **is** the stock bind.
   [OBS host bytes]
7. **Elephant host declarations**: three user TOMLs, three menu Lua
   symlinks, `/usr/lib/elephant/` still exactly 12 provider modules with the
   2.21.0 names (walker-deep §4.1; HostWalkerFiles §9). The on-disk module
   set is current; the *running provider list* is not (see §3). [OBS]
8. **Boundary invariants**: the walker socket was never connected and the
   launcher never opened (r7 §4/§7, r9 §6); a missing walker layer surface is
   a NOTE, never a pass/fail signal (r7 §4); rendered pixels and socket
   protocol are outside the read surface (arc §6). A route note that claims
   a connection, a launch, a screenshot or an observed render contradicts
   the lane’s own recorded method.
9. **PROVINCE scope**: `~/.config/walker/` is read-only for this lane;
   documentary only; every claim file-byte- or screenshot-verified
   (`PROVINCE.md:5-12`). [OBS]

### 2.2 2.17.0-era observations that stay true as historical measurements

The note must not “correct” these into 2.17.2 values; it must either cite
them with their date or leave them alone. All are [OBS-r9] measured
2026-10-14 in compositor session `efb50993780079460b0cbed1363e2166a2de1d9f`:

1. `walker --version` → bytes `32 2e 31 37 2e 30 0a` (`2.17.0\n`), 7 B;
   `--help` 1,726 B / 33 L / sha `ca4820a8…`; 26 option lines = 3 help + 23
   application; no subcommands; no `--config`, no `--reload`
   (r9 §2.1/§3.2, r7 §2). The only state-free verbs are `--version` and the
   three `--help*` forms; `-d/--dmenu`, `-q/--close`, `-e/--exit` start or act
   on a session and stay fenced (r9 §3.1).
2. Binary identity chain: 6,661,264 B, sha `64826a85…`, BuildID
   `a22452d1e4243bad1bf9fd487aa569f673ad9c5a`, rustc 1.97.1 `.comment`,
   embedded version literal at offset 847,791, embedded default config at
   offset 784,064 equal to the then-packaged file (r9 §2.2/§2.3, r7 §3).
3. Package `walker 2.17.0-1`, 29 files, `pacman -Qkk` 0 altered, Build Date
   == binary mtime (r9 §1/§2.2).
4. Reload settlement and its classes: no reload verb in help; no
   `inotify`/`watch`/`restart`/reload-config tokens (`reload` 1 = result-list
   action label, `Reload` 52 = `AsyncReload` rows); `CanReload=no`, no
   `ExecReload`; D-Bus interfaces `org.freedesktop.Application`,
   `org.gtk.Application`, `org.gtk.Actions` with **no reload method** and
   `Actions.List` = `as 0`; the only state-changing D-Bus verbs are
   UI-driving (`Activate`/`ActivateAction`/`Open`/`CommandLine`) and fenced;
   `Failed to set loaded config` / `config not initialized` are
   one-shot lifecycle strings; broken-config `--help` probe byte-identical
   (r9 §3.2-§3.7). Verdict classes must be preserved: **settled OBS**,
   **INF-high read-once**, **UNK live edit-without-restart** (r9 §3.8).
5. Runtime shape: PID 1203471 `/usr/bin/walker --gapplication-service`, unit
   `app-walker@autostart.service`, elephant PID 1203474, sockets
   `$XDG_RUNTIME_DIR/walker/walker.sock` and `.../elephant/elephant.sock`
   mode `srwxr-xr-x` size 0, D-Bus owner `dev.benz.walker` = the walker PID,
   elephant holds **no** session-bus name, no walker layer namespace
   (r7 §1/§4, r9 §1).
6. Env census: exactly one bare `WALKER_` literal (offset 797,295) and **zero
   `WALKER_<NAME>` tokens**; XDG path token run; units declare no
   `Environment=`/`EnvironmentFile=`; `gsettings get` color-scheme
   `'prefer-dark'`, accent `'blue'` (r7 §3, walker-deep §1).
7. Provider/runtime inventory: `elephant listproviders` 13 names, 12 plugin
   files, `bluetooth` absent though its `.so` exists, `runprefix autodetect =
   "uwsm-app --"`; 644-line generated docs (walker-deep §4.1, §13).
8. Theme chain and decision rules: `theme = "omarchy-default"` +
   `additional_theme_location`, `style.css` import into the generated
   `walker.css`, `omarchy-theme-set:38` → template renderer → `current/theme`
   swap; restart is the apply path (walker-deep §6/§7/§9).
9. Config-semantics observations that remain true as observations:
   `[columns] symbols = 1` is the grid column count, **not** default
   providers (R4-E3); local `config.toml:14` comment is wrong; the array
   replace claim and the prefix map are handled in §4 below because source
   evidence refines them.
10. Round-5 ledger contents (walker-deep §10/§11) and the r7 §5 ledger were
    **never appended** to `walker-deep.md` — its `## Errata` is still
    `_None yet_`. The new note must not claim those errata were applied, and
    any use of walker-deep §10/§11 should name the r5/r7/r9 note it comes
    from.

### 2.3 Contract claims that stay true and must be restated with their class

1. **Config is read once per process** — r9 INF-high on five classes; now
   also source-level at v2.17.2: `static LOADED_CONFIG: OnceLock<Walker>`
   (`config.rs:7`), `load()` sets it once and errors `Failed to set loaded
   config` on a second set (`config.rs:586-593`), `config::load().unwrap()`
   once in `main.rs:108`. Host live behaviour remains **[UNK]**.
2. **Restart is the apply path** — `omarchy-restart-walker` restarts the
   services; no in-process reload. True in 2.17.0 observation and in the
   v3.8.4 script bytes; the note may state the script contract and keep host
   execution unexercised.
3. **“Reload” in walker means result-list refresh** — the token trap is
   still the correct reading; v2.17.2 config only adds an `edit` action and
   changes `clipboard.remove` to `SimpleDelete`, neither is config reload.
4. **Socket path shape** — `$XDG_RUNTIME_DIR/walker/walker.sock`, app-named
   subdir + fixed name; walker README:179-185 uses the same shape
   (`/run/user/1000/walker/walker.sock`) as an example.
5. **Theme fallbacks** — `theme not found. using default theme.` on an
   unknown `-t`; per-part inheritance from the built-in default; built-in
   default CSS when the theme has none.
6. **Omarchy restart/refresh contract** — restart path, refresh path,
   `symbols.toml` omission: true at v3.8.4 bytes.
7. **Documentary-only status** — host binaries stay **[UNK]**; no walker or
   elephant execution, no socket connect, no service/compositor operation.
   This is C2’s own admission rule, not a corpus claim, but a note violating
   it fails credit regardless of content.

---

## 3. Stale present-tense claims (walker 2.17.0 / elephant 2.21.0 era)

“Stale” here means: true when measured, false or unproven as a
present-tense statement about the host today. The new note must not copy any
of these into the present tense.

| # | Stale claim (location) | Era value | Current status |
|---|---|---|---|
| S1 | “walker 2.17.0 is installed” (walker-deep §1; r7 §1/§2; r9 §1-§2) | 2.17.0-1 | **2.17.2-1** (`pacman.log:2929`) |
| S2 | “elephant 2.21.0” (walker-deep §1) | 2.21.0-1 | **2.22.1-1** (`pacman.log:3095`) |
| S3 | Binary sha `64826a85…`, 6,661,264 B, BuildID, `.comment`, ELF shape (PIE, stripped, entry `0x190420`), version-literal offset 847,791 (r9 §1-§2, r7 §1) | 2.17.0 build | binary replaced (7,039,912 B); contents **[UNK]**; never cite the old sha as current |
| S4 | `--version` bytes `2.17.0\n`; help shas `ca4820a8…`/`b513c43f…`/`0945536c…`; 26 option lines; no `--config`; help is one compiled-in blob (r7 §2, r9 §2) | 2.17.0 help/binary | 2.17.2 help and compiled blob **[UNK]** (not executed); README/source still show no reload, but that is not the help text |
| S5 | Packaged L1 13,220 B / 298 L / `5b4e47b7…` and all its line anchors (`:31-32`, `:53-58`, `:69-107`, `:112`, `:117-296`) (walker-deep §2.1-§2.4) | v2.17.0 tag bytes | **13,743 B / 305 L / `3c5c6867…` = v2.17.2 tag**; `[niri]` inserted at :24, prefixes moved to :75-113, actions :118-304, so every old packaged line anchor is off by roughly +6/+7 |
| S6 | Embedded default at offset 784,064 equals packaged file (r7 §3, walker-deep §14.1) | 2.17.0 binary | 2.17.2 binary **[UNK]**; tag source still `include_str!`s `resources/config.toml`, but that is not the host build |
| S7 | Package 29 files, `pacman -Qkk` 0 altered, Build Date == binary mtime (r9 §2.2) | 2.17.0-1 | 2.17.2-1 unmeasured (pacman barred) |
| S8 | `struct Walker with 29 elements`; 29-key universe (walker-deep §2.3, §14.2) | 2.17.0 binary | v2.17.2 source **adds `niri` and `blur_corner_radius`** (`compare` patch to `src/config.rs`, +44/−0); count changed; exact binary token **[UNK]** |
| S9 | PIDs 1203471/1203474, unit MainPID, socket mtimes 13:11:09, D-Bus `:1.23`, layer rows, compositor instance/time (r7 §1/§4, r9 §1/§4) | 2026-10-14 session | historical only; new session/PIDs unmeasured this round |
| S10 | 13-provider runtime list, `bluetooth` disabled, 644-line generated docs, `runprefix autodetect` (walker-deep §4.1/§13) | elephant 2.21.0 | 2.22.1 runtime **[UNK]**; on-disk plugin names unchanged (HostWalkerFiles §9) |
| S11 | Packaged action rows: no `edit` action; `clipboard.remove` with `after="AsyncClearReload"` (walker-deep §4.2, r9 §3.3) | v2.17.0 config | v2.17.2 adds `edit = ctrl e` and `clipboard.remove … SimpleDelete` (`resources/config.toml` diff) — do not quote old rows as current |
| S12 | Packaged theme file bytes (§6.2 mentions the default theme’s part set) | v2.17.0 package | v2.17.2 package theme files rewritten (mtime 2026-10-08); geometry 600/570 still true, sizes/hashes not |
| S13 | `omarchy version` → 3.8.3 vs checkout `v3.8.4` (R4-E4, walker-deep §1) | CLI + checkout | CLI pin cannot be re-run (`omarchy-*` barred); file bytes show master `8fcc9d60…` = tag v3.8.4; the two-pin caveat is unmeasured, not disproved |
| S14 | Bar left click at `config.jsonc:57` (waybar-walker-plane §3.1, inherited from round 1) | line 57 | current bytes: `on-click` at **:58**; line anchors drift with any edit — re-anchor from current bytes |
| S15 | “No `watch` token / no watch machinery” (r9 §3.3) | 2.17.0 token census | v2.17.2 **adds a Niri event-stream watch** (`src/niri.rs` added; `main.rs:809-870`), unrelated to config; do not generalise “no watch” to the new binary |
| S16 | “No active launcher bind; SUPER+SPACE does not open the menu” (waybar-walker-plane §8 U1/§9, later errata R2-E2) | round-1 wording | superseded: stock SUPER+SPACE **does** launch walker; use the R2-E2 form, never the pre-errata sentence |
| S17 | Broken-config `--help` probe (r9 §3.7) | 2.17.0 binary | not re-run; 2.17.2 behaviour **[UNK]** |
| S18 | `CanReload=no`, `ExecReload` unset, no unit `Environment` (r9 §3.5, r7 §3) | 2.17.0 unit | current unit state **[UNK]** (systemctl barred) |
| S19 | Theme-set pipeline line anchors (`omarchy-theme-set:38`, templates :6-46) (walker-deep §6.2) | omarchy 3.8.3 checkout | P5 seat is re-anchoring theme scripts; do not re-date walker-deep’s 3.8.3 line numbers without a fresh read |
| S20 | `pacman -Qi walker` Build Date / Install Date, `pacman -Ql` 29 entries, “no man page” (r7 §1) | 2.17.0-1 | pacman barred; package file list may have changed; [UNK] |

Additional caution: the notes’ **present-tense verbs** are the problem, not
the numbers. `walker “is” 2.17.0`, `config “falls through to L1”`, `“the
packaged prefixes do not exist”`, `“walker does not parse SCSS”` all read as
current claims. The route note should use “measured 2026-10-14 under
2.17.0-1” or “declared at v2.17.2 tag”.

---

## 4. Old claims the documentary evidence overturns or refines (do not repeat as-is)

These are not just stale; upstream v2.17.2 source contradicts the earlier
inference. The note may state the source-backed version and label the older
sentence as the r5 inference it supersedes (append-only: do not edit the old
note). Compare receipt: `SrcWalkerChangelog/walker-compare-v2.17.0-v2.17.2.json`
shows `src/config.rs` +44/−0 with **no change to `Providers::merge`**, so
these semantics hold for 2.17.0 as well as 2.17.2.

### 4.1 Prefix routes: merge by provider, not wholesale replacement

Old claim (walker-deep §2.2/§2.4, carried into §4.3 and the §9 decision
table): “arrays are replaced wholesale”, therefore the packaged-only routes
`;`, `>`, `!`, `%` do not exist at runtime and `runner`/`todo` are reachable
only through `/` or `-m`.

Source: `Providers::merge` (`config.rs:343-363`) assigns `default`, `empty`,
`ignore_preview`, `sets`, `max_results` directly (replace), but for
`prefixes` it iterates the user list and, for each entry, finds an existing
entry **with the same `provider`** and rewrites its `prefix`; only providers
not already present are pushed (`:353-363`). [SRC]

Applying that to the host’s six user entries over the ten packaged entries
(packaged order `;` providerlist, `>` runner, `/` files, `.` symbols,
`!` todo, `%` bookmarks, `=` calc, `@` websearch, `:` clipboard, `$`
windows; `resources/config.toml:75-113`) gives the **derived effective
list**: `/` providerlist, `>` runner, `.` files, `:` symbols, `!` todo,
`%` bookmarks, `=` calc, `@` websearch, `$` clipboard, `$` windows. [INF
from SRC]

Consequences the note must not get wrong:

- `;` disappears (providerlist moved to `/`), but **`>`, `!`, `%` remain**.
- `$` is duplicated (clipboard and windows). `data.rs:520-533` uses the
  **first** matching prefix over the merged vector and gates on
  `providers.contains_key(&prefix.provider)`, so clipboard (earlier in the
  packaged order) wins when both providers load. Host provider presence is
  **[UNK]** this round, so the live `$` outcome stays **[UNK]**.
- The §9 rule “remember the array replaces the packaged ten” is wrong;
  changing an existing provider moves its prefix, adding a new provider
  appends.
- The r5 §12 rejection “the packaged prefixes stay active” is over-broad and
  its stated reason (“two routes for `.` and `=`) does not hold: merge is by
  provider, so `>`/`!`/`%` do stay active, `;` does not, and `.`/`=` end up
  single-valued. The note should state the mechanism and the derived map,
  not the rejection.

### 4.2 The “four layers” are embedded defaults + one config file + env

Old claim (walker-deep §2.1/§2.2, r7 §3): L0 embedded → L1 packaged → L2
user → L3 env, with absent L2 keys “falling through to L1”.

Source: `DEFAULT_CONFIG` is `include_str!("../resources/config.toml")`
(`config.rs:8`); the program then calls `xdg::BaseDirectories::with_prefix(
"walker").find_config_file("config.toml")` (`config.rs:219`) — a **single**
first-existing file — and merges it; then merges `Environment::with_prefix(
"WALKER").separator("_")` (`config.rs:235`). [SRC] Because the user file
exists, `/etc/xdg/walker/config.toml` is not read at runtime; it is the
fallback only when no user file exists. Values coincide because both the
packaged file and the embedded default are the same upstream document
(v2.17.0 `5b4e47b7…`; v2.17.2 `3c5c6867…`). [OBS + SRC]

The note may keep the “L0/L1 same document” fact but must not present L1 as
an independent runtime layer under the user file. It also must not say the
user file is a full schema (it omits roughly two dozen keys; HostWalkerFiles
§4).

### 4.3 Theme parts inherit per file; SCSS is supported

Old claim: theme part resolution order **UNK**; a theme may be all-or-default
(walker-deep §6.3, r7 §11.1); and “walker parses SCSS themes” was **rejected**
(walker-deep §12).

Source: `Theme::default()` builds layout/keybind/preview from
`include_str!("../../resources/themes/default/*.xml")` plus provider item
layouts from `PROVIDERS` (`theme/mod.rs:30-49`). `setup_theme_from_path`
starts from `Theme::default()` and overwrites only parts that exist in the
theme dir (`theme/mod.rs:140-147`, cases at :160-215); missing parts keep
the built-in defaults. `setup_css` reads `style.scss` if present and compiles
it with `grass::from_string`, loading the result and returning; otherwise it
loads `style.css`, otherwise the built-in default CSS
(`theme/mod.rs:234-261`, `style.scss` at :165, `style.css` at :170,
`grass` at :241-244, built-in CSS at :260). [SRC]

README:219 confirms the user-facing statement: “Themes inherit the default
theme by default, so if you just want to change the CSS, you can just create
`themes/yours/style.css`.” [SRC] So:

- per-part inheritance, not all-or-default;
- `style.scss` **is** parsed (by `grass`) and takes precedence over
  `style.css` when present; a SCSS parse error returns before CSS fallback;
- the host `omarchy-default` theme ships only `layout.xml` and `style.css`,
  so the built-in XML parts and provider item layouts fill the rest;
- live rendering under that theme remains **[UNK]**.

The r5 §12 rejection must not be repeated. (This is exactly the kind of
token-only rejection the lane’s later method lessons warn about.)

### 4.4 `~` is replaced textually, not expanded by a shell

Old status: `~` expansion in `additional_theme_location` **UNK**
(walker-deep §2.4, §11.7; r7 §11.7).

Source: `config_paths.push(PathBuf::from(a.replace("~", &home).to_string()))`
(`theme/mod.rs:60-63`), gated on `HOME`. [SRC] Every `~` in the string is
replaced; this is not `shellexpand`, not `$HOME` interpolation generally.
Host binary behaviour still **[UNK]**, but the contract question is settled
at source level.

### 4.5 `WALKER_` env surface: prefix and separator known

Old status: exactly one bare `WALKER_` literal at 797,295, zero
`WALKER_<NAME>` tokens; whether it is a runtime prefix **UNK** (r7 §8.1,
r9 §7.6).

Source: `config::Environment::with_prefix("WALKER").separator("_")`
(`config.rs:235`), merged after the file. [SRC] So env overrides are
`WALKER_`-prefixed with `_` separator; the exact spelling for nested keys
(e.g. `WALKER_PROVIDERS__DEFAULT`) is **not** verified in the fetched code.
The old binary census remains true as a census of the 2.17.0 build; it must
not be restated as “there is no env surface”.

### 4.6 Unknown keys are ignored; a type error drops the whole user overlay

Old status: parse-error/unknown-key behaviour **UNK** (`unknown_fields` token
only; walker-deep §3, r7 §11.6).

Source: `PartialWalker` is `#[serde(default)]` with every field
`Option<…>` and **no `deny_unknown_fields`** in `config.rs`; a
`try_deserialize` failure sets an error string, prints it, and skips
`config.merge(res)` (`config.rs:211-242`). [SRC + serde default INF] So:
unknown keys are ignored; a type error keeps the built-in defaults (and the
env merge still runs) and surfaces `Config: <error>` via `set_error`.
Observed host UI/behaviour remains **[UNK]**.

### 4.7 `installed_providers` is a config field, not a proven runtime value

Old claim: `installed_providers` appears only in the binary run, “runtime-
populated candidate” (walker-deep §2.3, §11.4).

Source: it is a field on `Walker` and `PartialWalker`
(`config.rs:36,96`) and is merged like any other option (`:303-304`);
nothing in the fetched modules reads it. [SRC] So the “runtime-populated”
guess is unsupported; the field is user-configurable and its consumer is
**[UNK]** until `src/providers/mod.rs` is read.

### 4.8 `[providers.sets]` semantics are now readable

Old status: `-s` path and `[providers.sets]` with a real set **UNK**
(walker-deep §11.10, r7 §11.10).

Source: `data.rs:553-571` — when no `-m` provider is set, an empty query
uses `providers.empty`, a non-empty query uses `providers.default`; if a
current set is set, it indexes `providers.sets[set]` and uses that set’s
`empty`/`default`; a missing set hits `.expect("can't find specified set")`.
`main.rs:435-437` sets the current set from `-s`. [SRC] This settles the
shape (set = named pair of provider lists) and the missing-set failure mode;
the actual host sets (`{}` in both layers) and live dispatch remain
**[UNK]**.

### 4.9 `global_argument_delimiter` has no elephant-side key in the fetched elephant surface

Old status: elephant-side counterpart **UNK** (walker-deep §4.3).

Source: walker reads `cfg.global_argument_delimiter` (`data.rs:535`,
`:754`); the elephant v2.22.1 `common/config.go` struct has no delimiter
field (`provider_hosts`, `auto_detect_launch_prefix`, `terminal_cmd`, … at
:29-32), and the elephant README has no delimiter hit. [SRC] The key is
walker-side; “no elephant-side counterpart in the fetched files” is the
strongest documentary statement; the generated provider docs were not
re-read for 2.22.1.

### 4.10 `walker.sock` is protobuf-framed; elephant README’s path is not the host path

Old status: socket protocol **UNK** (walker-deep §11.3, r7 §11.3, arc §6).

Source: `main.rs:811,872` listens on the activation socket; `data.rs`
writes a frame `vec![1, 0]` + big-endian length + protobuf
(`data.rs:785-792` for activate; `:668-671` and `:693` for other requests;
query uses `vec![0, 0]` at `:584-592`). The tree ships
`src/protos/{query,activate,subscribe,providerstate}.proto` and
`ext-background-effect-v1.xml` (`walker-v2.17.2-git-tree.json`). [SRC] The
protocol is a typed protobuf frame, not a text line; wire semantics remain
**[UNK]** until the protos are read.

Separately, elephant README:200-211 says IPC is Unix sockets + Protocol
Buffers and gives `/tmp/elephant.sock` as the “typical” path; the 2.21.0
host observation was `$XDG_RUNTIME_DIR/elephant/elephant.sock` (r7 §4).
The note must not adopt `/tmp/elephant.sock` as a host fact; runtime path
for 2.22.1 is **[UNK]**.

---

## 5. Open unknowns a documentary route can narrow

| # | Unknown (anchor) | Documentary anchor already fetched | Narrowed to | Residual **[UNK]** | Next fetch, if wanted |
|---|---|---|---|---|---|
| U1 | Theme/layout resolution order for partial themes (walker-deep §6.3/§11.1; r7 §11.1; r9 §7.1) | `theme/mod.rs:30-49,140-215`; README:219 | per-file inheritance from built-in default; scss > css; item templates per provider with `item.xml` → key `default` | live render under `omarchy-default`; item-template precedence when both theme and provider layouts exist | none needed for contract; render stays barred |
| U2 | Emergency trigger condition (walker-deep §7.4/§11.2) | `src/providers/emergency.rs` exists in tree; not fetched | nothing yet | trigger condition | fetch `src/providers/emergency.rs` at v2.17.2 |
| U3 | `walker.sock` protocol (walker-deep §11.3; r7 §11.3; arc §6) | `main.rs:811,872`; `data.rs:584-592,668-671,785-792`; proto file list; README:179-185 | protobuf frame `[type,0] + BE len + msg`; socket open is a “faster `walker` call” with no CLI options | exact message schemas and reply semantics | fetch the four `.proto` files at v2.17.2 |
| U4 | `installed_providers` semantics (walker-deep §2.3/§11.4) | `config.rs:36,96,303-304` | a user-settable option merged like any other; not read by fetched modules | consumer (`providers/mod.rs`) and effect | fetch `src/providers/mod.rs` |
| U5 | `WALKER_` env surface (r7 §8.1; r9 §7.6) | `config.rs:235` | prefix `WALKER`, separator `_`, merged last | exact nested-key spelling; host runtime | fetch a config-crate version doc or test; host stays barred |
| U6 | Unknown-key / parse-error behaviour (walker-deep §3; r7 §11.6) | `config.rs:53-110,211-242` | serde ignores unknown keys; type error skips the user overlay and sets an error string | observed UI/error text; whether env still merges (source says yes) | none needed for contract |
| U7 | `~` expansion (walker-deep §2.4/§11.7) | `theme/mod.rs:60-63` | textual replace of every `~` with `$HOME` | host binary behaviour | none |
| U8 | Elephant-side delimiter (walker-deep §4.3) | elephant `common/config.go:29-32`; README | no delimiter key in fetched elephant config/docs; walker owns it | generated provider docs for 2.22.1; runtime | fetch elephant `generatedoc` output only if a seat can capture it without running the daemon (currently a command → barred) |
| U9 | `[providers.sets]` (walker-deep §11.10) | `data.rs:553-571`; `main.rs:435-437` | set = named `empty`/`default` provider lists; `-s` selects; missing set panics via `expect` | live sets (none configured) and UI error path | `src/providers/mod.rs` if the panic path matters |
| U10 | Rendered UI / pixels (r7 §5; arc §6) | — | nothing | everything | not narrowable documentarily |
| U11 | Live edit-without-restart discriminator (r9 §3.8; arc §7 #12) | `config.rs:7,586-593`; `main.rs:108` | source has one-shot `OnceLock` and no reload entry point | live host behaviour | none; stays [UNK] by constraint |
| U12 | Provider availability/behaviour on host (walker-deep §11; r7 §4) | elephant README; upstream tree | upstream provider set and requirements | which providers 2.22.1 loads; runtime results | barred (daemon query) |
| U13 | Help/version/rebuild stability (r7 §8.5; r9 §2.4) | v2.17.0/v2.17.2 release bodies; compare files | what changed 2.17.0→2.17.2 (niri, blur, edit action, SimpleDelete, GTK deps); exact commit `a515085` | rebuild stability; host help bytes | none |
| U14 | Elephant 2.22.1 provider surface vs 2.21.0 observation | elephant README and tree; on-disk 12 plugin names unchanged | on-disk module names unchanged; runtime list unmeasured | live list | barred |
| U15 | Niri integration (new in 2.17.2) | `compare` adds `src/niri.rs`; `main.rs:105-140`; config `[niri]` :24-27 | upstream ships an event-stream watch; host compositor is Hyprland and `launch_on_*` defaults are false | whether the host binary includes it and whether it ever activates | host stays barred; contract settleable from source |

Notes on using this table in the route note: each “narrowed” cell is a
**documentary** statement at v2.17.2 (or elephant v2.22.1). None of them is
a host observation, and the note must keep the host binary **[UNK]** even
where source is unambiguous (C2: “host binaries stay [UNK]”).

---

## 6. Credit mechanics and evidence already on disk (for the note author / L1)

1. **SOURCES gap.** `corpus/SOURCES.md` has 71 rows, S001-S071, and **zero**
   rows whose source or scope names walker or elephant (`grep -i
   'walker\|elephant'` → 0 hits, [OBS]). S072-S099 are reserved for this
   round. C2’s `mined_a()` requires a row that is `status=mined`,
   `tier=A`, and whose `used-by` cell contains the exact path
   `corpus/knowledge/walker-route-r18.md`; the upstream gate additionally
   requires at least one cited row of kind `docs|spec|code` whose **source
   cell** contains `https://` and whose source+scope contains a
   `SURFACE_KEYWORDS['P3']` token (`walker`, `elephant`) — measure.py
   :135-290 at `d9a5a18`. No existing row can satisfy this by itself.
2. **Draft ids do not count.** The head `source:` line is parsed with
   `re.findall(r'S\d{3}', …)`; `S0xx-pending` yields no token. The final
   note must carry real `S0xx` ids assigned by L1 (S072-S099) or it fails
   as “no head source S### token resolves”.
3. **Head/section shape.** First 15 lines need `source: S### …` and exactly
   one `surface: P3` value (a second, *different* `surface:` line rejects the
   note; a duplicate identical line happens to dedupe in the parser’s set, but
   should not be risked). Required
   sections: `## Upstream contract`, `## Host declaration`, `## Safe
   observation`, `## Unexercised behavior`; each ≥3 non-blank lines;
   `[UNK]` inside the last. [OBS measure.py `REQUIRED_HEADINGS`,
   `FACET_MIN_LINES`, `HEAD_LINES`]
4. **Receipts already fetched (wave tree, must be committed by L1 under
   R17-V3).** Bodies + `receipts.jsonl` exist for at least:
   - walker v2.17.2 `README.md` — 7,926 B, sha
     `9755f955d5c4e460ac8538e1b648ba2a3c86da37ceaa4d0655dca4d1ea3d2456`
     (`fetch/SrcWalkerReadme/`, `fetch/NoteWalker/`);
   - walker v2.17.2 `resources/config.toml` — 13,743 B, sha
     `3c5c6867…` (`fetch/SrcWalkerDefaultConfig/`, `fetch/NoteWalker/`);
   - walker v2.17.2 `src/config.rs` — 19,675 B, sha
     `93b6bd6f360312dc0dcd70cd939a14e673431ee89b95608084253069aaad1469`;
   - walker v2.17.2 `src/theme/mod.rs` — 9,364 B, sha
     `93287a1c389a4b1856e2736e16246cef90691074023f57521fbb1422a61e0349`;
   - walker v2.17.2 `src/data.rs` — 26,338 B, sha
     `996db119ba61cb1505aa26782a19c7b8db49889874bd87ecbf277c9145cada09`;
   - walker v2.17.2 `src/main.rs`, `Cargo.toml`, git tree, release
     v2.17.0/v2.17.1/v2.17.2 JSON, compare v2.17.0…v2.17.2
     (`fetch/SrcWalkerChangelog/`);
   - elephant v2.22.1 `README.md` — 6,969 B, sha
     `aa19a7e2d1c07bf1852b65fd38ca24a6b04bba0dacfd9f6cb02ada0ee0b61389`,
     plus `pkg/common/config.go`, menu/provider READMEs
     (`fetch/NoteWalker/`, `fetch/SrcElephantProviders/`);
   - omarchy v3.8.4 `bin/omarchy-launch-walker`,
     `bin/omarchy-restart-walker`, `bin/omarchy-refresh-walker`,
     `config/walker/config.toml`, `default/walker/walker.desktop`,
     `default/walker/restart.conf` (`fetch/NoteWalker/`,
     `fetch/SrcOmarchyWalker/`).
   Tag→commit records: walker `a515085…` (ls-remote receipt);
   omarchy `v3.8.4 = 8fcc9d60…` (`.git/packed-refs`, plus
   `fetch/MadoR18.HostOmarchyCheckoutTag/gh-ref-tags-v3.8.4.json`).
5. **What must stay out of the note.** Any claim to have run walker,
   elephant, `omarchy-*`, `systemctl`, `hyprctl`, `pacman`, or to have
   connected either socket; any host binary behaviour; any screenshot/render.
   Safe observation for the note: re-fetch the tag URLs and compare
   sha256; `sha256sum`/`wc -l` the host config files; read pacman.log lines;
   `cmp` the host omarchy scripts against tag bodies. These are re-runnable
   and cannot touch session state.
6. **Terminology.** Use “P3 Walker” and name elephant as the provider engine,
   not a second surface. The measure keyword list for P3 is exactly
   `walker`, `elephant`; for P5 it is `theme`, `wallpaper`, `hyprpaper`,
   `swaybg`. A source row about omarchy’s walker scripts qualifies for P3;
   a row about the theme pipeline qualifies for P5. Do not mix both
   surfaces in one note (one `surface:` line only).

---

## 7. Gaps / confidence of this report

- I did not fetch any web source; all [SRC] anchors come from sibling fetch
  bodies already in the wave tree. Their receipts are the authority, and I
  did not re-verify their sha256 against the live URLs (that is the note’s
  `## Safe observation` recipe).
- I did not read the walker 2.17.2 **binary** (C2 keeps it [UNK]); the
  “struct Walker” count change is from the tag source compare, not from
  `/usr/bin/walker`.
- I did not read `src/providers/{mod,emergency}.rs`, the four `.proto`
  files, or `src/niri.rs`; those are named above as the next documentary
  fetches (U2, U3, U4, U15).
- I did not re-measure any runtime surface; every PID/socket/D-Bus/layer
  value quoted from r7/r9 is historical and marked so.
- I did not run `measure.py`; credit mechanics above are read from its
  source at `d9a5a18`, not from a measurement. L1 owns the gate.
- Sibling reports `HostWalkerFiles.md`, `SrcWalkerReadme.md`,
  `SrcWalkerConfigPaths.md`, `SrcWalkerDefaultConfig.md` and
  `SrcWalkerThemes`/`SrcWalkerChangelog` receipts were read as corroboration;
  where they disagree with this report, the raw host bytes and upstream
  bodies cited above are the evidence, not the reports.
- Confidence: high on the byte-level staleness (S1-S7, S10-S12, S14) and on
  the source-backed refinements (4.1-4.9) because the raw bodies
  were read directly; medium on U8/U14 (elephant surface not exercised);
  the r5 “prefixes wholesale” and SCSS rejections should be treated as
  superseded, not merely “unverified”.
