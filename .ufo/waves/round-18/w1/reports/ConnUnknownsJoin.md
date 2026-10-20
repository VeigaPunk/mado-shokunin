# ConnUnknownsJoin — joining the P3/P5 documentary routes to the open ledgers

Seat: MadoR18.ConnUnknownsJoin (connector, leaf, no dispatch). Round 18 / w1.
Target root `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Scope: for each open ledger row the two landed routes touch — `arc-synthesis.md`
§6, `gate-standing-use.md` §6, `walker-deep-r9.md` §8, `corpus/README.md`
Frontier — say **which unknowns a documentary route narrows and which it leaves
open**, and give the **exact cross-link lines** L1 can land. This seat writes no
ledger, note or draft; only this report.

Evidence classes below: **[OBS]** read from bytes this seat (file reads,
`sha256sum`, line-numbered `sed`/`grep`); **[OBS-fetch]** a committed round-18
fetch body written by a sibling seat, read here; **[INF]** reasoning from those
bytes; **[UNK]** not established. **Both route notes landed during this pass**:
`corpus/knowledge/theme-route-r18.md` (sha256
`704f6967900f1b760fc0d496c53c891be66691ae6356ef60738a5192a91d44a6`) and
`corpus/knowledge/walker-route-r18.md` (sha256
`53f035e2f827a19d0cedc69e9ef693cd07367fcd486907541e033ca34a63e28c`); both
are checked against the joins in §2.5. Every join below is still
**conditional on the route passing the unchanged c2 instrument** (ids, used-by,
receipts — §5). No web fetch was needed (the
bodies are already committed under `.ufo/waves/round-18/fetch/`); no tool was
installed or updated; no gate was run.

Hashes of the bytes this report's line numbers bind to [OBS]:

| file | sha256 | lines |
|---|---|---|
| `corpus/knowledge/arc-synthesis.md` | `a5b48331414618108cdc9596cf6c7cc0dc78994ebcf61141c3e6d80428419d50` | 387 (+1 unterminated) |
| `corpus/knowledge/gate-standing-use.md` | `7072db4832339fa16d82ee7f53ac7f0a842468eb1cb2dfc13f65208258547328` | 505 (+1 unterminated) |
| `corpus/knowledge/walker-deep-r9.md` | `a5acfe0162c9e5cd05cc3c2ab11dc9ad394d710e8673723feb1e39c3b39a48c7` | 398 (+1 unterminated) |
| `corpus/README.md` | `12cbb09351eeb442aea59efb9e4677a6fa63283d2c502eae4aa7a742f2f32211` | 126 |
| `.ufo/waves/round-18/drafts/FrontierDraft.md` | `a3975065bd6b0bfbab3e0bf842717095f5cd47a480c6a984f46bfc5b2c8c499e` | — |
| `tools/mado-verify.sh` (current worktree) | `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207` | — |
| `corpus/knowledge/theme-route-r18.md` (landed mid-pass) | `704f6967900f1b760fc0d496c53c891be66691ae6356ef60738a5192a91d44a6` | — |
| `corpus/knowledge/walker-route-r18.md` (landed mid-pass) | `53f035e2f827a19d0cedc69e9ef693cd07367fcd486907541e033ca34a63e28c` | 321 |

A moved hash invalidates the line numbers, not the classification.

## 0. The one-line answer

**One ledger row genuinely moves: `arc-synthesis.md` §6 `walker socket
protocol` (line 297) is narrowed from "shape only" to a documented transport,
message-family contract, and socket path — and still not closed (wire schema
and message field semantics stay `[UNK]`). Every other named ledger row stays
open.** The theme route closes no gate residual; both routes create no gate
read. The README must gain the round-18 bullet **and** amend the round-17
bullet's "still open" clause, or the index contradicts itself. The sharpest
cross-surface conflict is not in a ledger but in the gate: the Walker version
pin `2.17.0` (`tools/mado-verify.sh:3212`) versus
`/var/log/pacman.log:2929` `2.17.0-1 -> 2.17.2-1`; it must be reported, not
smoothed, and no gate edit is a round-18 claim.

## 1. What the documentary class can carry (grounded anchors)

The route notes are `[INF-docs]`/file-bytes documents; a tag never proves the
host binary. The material the scribes already fetched supports exactly these
narrowings.

### P3 — Walker / Elephant / omarchy launcher

| fact class | anchor | class |
|---|---|---|
| Config is one XDG-resolved file, merged default → user → `WALKER_*` env | `src/config.rs:7` (`OnceLock<Walker>`), `:8` (embedded default), `:218-223` (`xdg::BaseDirectories::with_prefix("walker").find_config_file("config.toml")`), `:235-242` (`Environment::with_prefix("WALKER").separator("_")`) | [OBS-fetch] |
| One-shot load; no reachable watch path in `src/` | `src/config.rs:7` (`OnceLock<Walker>`), `:586-589` (`load()` sets it once), `src/main.rs:108`; whole-tree search of the tag tarball `WX` finds no `notify::`, no `use notify`, no `inotify` call in `src/` — the declared `notify = "8.2.0"` dependency (`Cargo.toml:21`) is unused there; unmatched code stays `[UNK]`; the README's "Reload" tokens are result-list actions (r9 §3.3) | [OBS-fetch] |
| User-config failure modes | syntax-level build error returns through `?` (`src/config.rs:221-223`) and `load().unwrap()` at `src/main.rs:108` would panic (INF from code, not exercised); build-OK/deserialize-fail is non-fatal: `set_error("Config: {error}")` + `println!`, defaults stay (`src/config.rs:225-231`) | [OBS-fetch] |
| Theme dirs and precedence | `src/theme/mod.rs:53-63`: `find_config_files("themes")` (XDG dirs, user last per xdg 3.0.0 `find_config_files`), then `additional_theme_location` appended **last** with textual `~`→`$HOME`; `:132-134` inserts a builtin `default` theme if absent; `:140-231` `setup_theme_from_path` starts from `Theme::default()` so a partial theme inherits default parts | [OBS-fetch] |
| Theme name resolution | `src/main.rs:110-120`: CLI `--theme` → `config.theme` → `"default"`; unknown theme prints `theme not found. using default theme.` | [OBS-fetch] |
| Walker socket role and path | README:179-185: a socket call is a faster **launch** (`nc -U /run/user/1000/walker/walker.sock`), no command-line options; `src/main.rs:872-886` binds `$XDG_RUNTIME_DIR/walker/walker.sock` and listens for activation | [OBS-fetch] |
| Walker↔Elephant IPC | Elephant README:3, :9, :198-215: Unix domain sockets + Protocol Buffers; message families **Query / Activation / Menu / Subscribe**; `pkg/pb/` holds the definitions. **Path resolved by source**: walker connects to `$XDG_RUNTIME_DIR/elephant/elephant.sock` (fallback `env::temp_dir()`) [WD:156-161,169]; elephant listens on the same path [EC:38-44]; the README's "typically at `/tmp/elephant.sock`" [ER:211] is stale for this tag. The source path equals the path the round-9 host observation recorded — documentary agreement, no live probe this round | [OBS-fetch] |
| omarchy launcher | `bin/omarchy-launch-walker:5-14`: ensure `elephant`, ensure `walker --gapplication-service` under `GSK_RENDERER=cairo`, then `exec walker --width 644 --maxheight 300 --minheight 300 "$@"` | [OBS-fetch] |
| Host version relation | `/var/log/pacman.log:2929` `[2026-10-20T09:16:46-0300] upgraded walker (2.17.0-1 -> 2.17.2-1)`; `:3095` elephant `2.21.0-1 -> 2.22.1-1`; `:3123` `walker-restart.hook` ran. Round-9's on-disk binary was `2.17.0-1`, sha `64826a85…`, measured 2026-10-14 — the package moved **after** that observation | [OBS] |

What P3 therefore **narrows**: the config read model (path resolution, merge
order, env prefix, one-shot load, failure modes), the theme directory
precedence and per-part fallback, the walker.sock *role*, the elephant
transport + message families, and **the elephant socket path** — source and
the 2026-10-14 host observation agree on `$XDG_RUNTIME_DIR/elephant/elephant.sock`;
the README's `/tmp/elephant.sock` is stale for the tag. What it **cannot**
carry: the running binary's identity (log line ≠ binary), the protobuf field
schema and message semantics, any provider result, rendered UI, and any live
reload discriminator.

### P5 — omarchy theme-set / background / swaybg

| fact class | anchor | class |
|---|---|---|
| Theme apply is a copy and swap, not a symlink | `bin/omarchy-theme-set:12-15` paths, `:24-30` clean `next-theme` then copy official then user overlay, `:32-35` `colors.toml` fallback from alacritty, `:38` `omarchy-theme-set-templates`, `:41-42` `rm -rf current/theme && mv next-theme current/theme`, `:45` write `theme.name` | [OBS-fetch] |
| Background choice on theme set | `:47-50` calls `omarchy-theme-bg-next` unless `OMARCHY_THEME_SKIP_BACKGROUND=1` | [OBS-fetch] |
| Consumer refresh list (declared, not observed) | `:52-62` waybar (if running), swayosd, terminal, hyprctl, btop, opencode, mako, helix; `:64-70` foot/gnome/browser/vscode/obsidian/keyboard; `:73` `omarchy-hook theme-set "$THEME_NAME"` | [OBS-fetch] |
| Background symlink and relaunch | `bin/omarchy-theme-bg-next:6-9` paths; `:11` `find -L` over user then theme backgrounds; `:14-17` empty set → `pkill -x swaybg` + `swaybg --color '#000000'`; `:19-34` read `current/background` and find its index; `:36-43` next with wraparound; `:46` `ln -nsf "$NEW_BACKGROUND" current/background`; `:49-50` `pkill -x swaybg`, `setsid uwsm-app -- swaybg -i current/background -m fill` | [OBS-fetch] |
| Session-start launch | `default/hypr/autostart.conf:5` `exec-once = uwsm-app -- swaybg -i ~/.config/omarchy/current/background -m fill`; sourced at `~/.config/hypr/hyprland.conf:4`; no `hyprpaper` anywhere; no systemd unit | [OBS] |
| swaybg contract | `swaybg.1.scd`: `-c/--color`, `-i/--image`, `-m/--mode` (`stretch` default, `fill`, `fit`, `center`, `tile`, `solid_color`), `-o/--output` | [OBS-fetch] |
| Host theme state | `theme.name` = `matte-black\n` (`4874971…`); `current/theme` is a **real copied directory** (28 files, 0 symlinks, 16 template-rendered + 12 copied); `current/background` is an absolute symlink to `current/theme/backgrounds/0-ship-at-sea.jpg` (`55fa691a…`); `~/.config/omarchy/themes/` empty | [OBS] |
| Host swaybg version | `/var/log/pacman.log:1158` installed `swaybg (1.2.2-1)`, no later row; binary `e36544a1…` | [OBS] |

What P5 therefore **narrows**: the declared apply mechanism end-to-end (copy,
template render, `theme.name`, background symlink, `pkill`+`swaybg -i … -m
fill`, the restart list, the hook), and the exact multi-output options the
`swaybg` command line uses. What it **cannot** carry: whether a theme set
actually restarted any consumer, which background ultimately renders, reload
effects, rendered pixels/screenshots, and the theme *choice* (operator-owned).

## 2. Ledger-by-ledger join

### 2.1 `arc-synthesis.md` §6 — gap ledger (table at lines 294-307, sha `a5b48331…`)

| line | row | verdict | why |
|---|---|---|---|
| 296 | rendered UI / screenshots | **OPEN, unchanged** | neither route observes pixels; both must say so in `## Unexercised behavior` |
| 297 | walker socket protocol | **NARROWED, not closed** | transport + message families + walker.sock role + elephant socket path are documented (P3 §1); the source path agrees with the 2026-10-14 host observation and the README's `/tmp/elephant.sock` is stale for the tag; wire schema/field semantics remain `[UNK]`; no live probe |
| 298 | idle/lock transitions | **OPEN, unchanged** | P5 touches the autostart file but not idle/lock |
| 299 | dispatcher behaviour | **OPEN, unchanged** | no dispatcher evidence |
| 300 | window-rule effects / exec-once results | **OPEN, unchanged** | P5 documents the `exec-once` *declaration* and the theme-set restart list, not their results; no new read verb |
| 301 | waybar module text | **OPEN, unchanged** | P5 renders `waybar.css`; module text has no read surface |
| 302 | env vars (compositor, NVIDIA trio) | **OPEN, unchanged** | P3's `WALKER_*` merge is walker's own env override, not the compositor's env surface |
| 303 | hypridle/hyprsunset stop-cause | **OPEN, unchanged** | not in either surface |
| 304 | tree-wide omarchy cleanliness | **OPEN, unchanged** | checkout read as file bytes only |
| 305 | battery / power-supply | **OPEN, unchanged** | no device |
| 306 | exit-flatten mutant family | **OPEN, unchanged** | harness-side |
| 307 | theme live rows / walker live rows | **OPEN, unchanged** | a knowledge note creates no gate row; the round-9 exemptions stand |

§7's "Unknown (12 named)" count is **not** changed by a narrowing: the row is
still an unknown, only less coarse. Do not re-count it closed.

### 2.2 `gate-standing-use.md` §6 — residual ledger (table at 255-264, sha `7072db48…`)

The table is explicitly bound to `93e43f8f…` (round 10). The current worktree
gate is `fba82a66…`; the table is historical either way. Route join:

| line | residual | verdict | why |
|---|---|---|---|
| 257 | theme live rows `theme.wallpaper.live`, `theme.name.display_agree` | **OPEN, unchanged** | the P5 route does not read a running swaybg or compare display agreement; the `grep` check still reads 0 |
| 258 | walker live-surface rows (2 sockets, D-Bus owner, layer invariant) | **OPEN, unchanged** | the P3 route never connects or queries; the gate still emits only version + services rows (`:3208-3227`) |
| 259-263 | J/K/L stubs, assertion floor, usage arms, boundary prefix, rc-6 arm | **OPEN, unchanged** | unrelated to P3/P5 |
| 264 | theme clauses' covering mutant | **OPEN, unchanged** | a knowledge note is not a mutant; round-6 rule 2 still owed |

New fact this ledger must carry (not a route claim): the gate's Walker pin at
`:3212` compares `walker --version` to `2.17.0`, while
`/var/log/pacman.log:2929` records the package upgrade to `2.17.2-1` on
2026-10-20T09:16:46 −0300. A live run would compare the installed binary's
version string (log line says `2.17.2-1`) and would print
`FAIL "pin changed: '<value>'; re-verify claim anchors"` unless it still prints
`2.17.0` [INF]. Under the host pause the row was **not** run. This is a moved
pin: report first, re-anchor only in a later gate-edit round.

### 2.3 `walker-deep-r9.md` §8 — errata owed (lines 378-396, sha `a5acfe01…`)

§8 is candidate text for the `walker-deep.md` owning lane and remains
unapplied. The P3 route is the new provenance for most of it:

| §8 item | verdict | P3 carries |
|---|---|---|
| `§11.6` reload half (383-385) | **narrowed** | `OnceLock` + one `config::load()` in `main.rs:108`; whole-tree textual search finds no reachable watch/reload path in `src/` (declared `notify` dependency unused there) — source-level corroboration of the round-9 A–E negatives; live discriminator still `[UNK]` |
| `§11.6` parse-error half (385) | **narrowed, two modes** | syntax-level build error → `?` then `load().unwrap()` panic (INF); build-OK/deserialize-fail → `set_error` + `println!`, defaults stay (`config.rs:221-231`); host-visible behaviour unobserved |
| `§10` "what config does it read" (390-393) | **narrowed** | `config.rs:218-223` one XDG `config.toml`; `theme/mod.rs:53-63` theme bases + extra location; r9's 784,064 embedded-offset pin is date-bounded — the 2.17.2 binary embeds the same 13,743-byte default at 806,960 (route MOVED table) |
| `§9` decision rule (394-396) | **narrowed, not changed** | three companion negatives now have a fourth, source-level: one-shot `OnceLock` load; the rule "edit then restart" is unchanged |
| r9 §7 items | **partly narrowed** | item 3 XDG honoring → source (`find_config_file`); item 1 live reload discriminator → still `[UNK]`; item 2 help short-circuit → still `[UNK]` |
| `walker-deep.md` §11 items 1, 5, 6, 7 | **narrowed** | theme-part order/fallback; `WALKER_` env surface; parse-error path; `~` textual replace (see §3.6 block) |

**Version relation, stated as a relation (not a contradiction):** r9 §1 pinned
the binary at `2.17.0-1` on 2026-10-14; pacman.log `:2929` moved the package
to `2.17.2-1` on 2026-10-20. The tag class moved; the running binary stays
`[UNK]`. r9's pin remains historical and is not "wrong" — it is date-bounded.

### 2.4 `corpus/README.md` Frontier (lines 76-126, sha `12cbb093…`)

| line | text today | verdict |
|---|---|---|
| 80-82 | "Rendered UI, Waybar module text, **Walker socket protocol**, dispatcher behavior and per-window rule effects: [arc gap ledger] §6" | **must not stand unqualified** after the round-18 bullet: the socket row is now narrowed to transport/message families/path. Either amend this bullet's phrase to "Walker socket **wire schema**" or make the new bullet state the narrowing explicitly (the block in §3.1 does) |
| 119-126 | round-17 bullet: "Still open: …; **P3 Walker and P5 theme/wallpaper sourced routes**." | **contradiction**: the round-18 bullet says those routes now exist. Amend this clause in place to point forward (exact edit in §3.2); the README is a maintained index, not append-only |
| after 126 | — | **insert the round-18 bullet** (§3.1). FrontierDraft says "after line 125"; that is wrong — the round-17 bullet ends at line 126. Inserting after 125 would split the `(a pacman.log pkgver …)` parenthetical |
| after 43 | — | **insert the two index rows** (§3.3); line 44 is blank, so after 43 is correct |

### 2.5 Landed theme note — checked against the landed bytes (sha `704f6967…`)

The P5 note landed during this pass; the joins above were re-checked against
it, not only against its scout inputs:

- **Structure passes what can be checked statically**: line 1 is a `source:`
  line; line 4 is exactly `surface: P5`; all four required level-2 headings
  exist; each has well over three non-blank lines; `[UNK]` is inside
  `## Unexercised behavior`. The only open c2 dependency is id assignment:
  `S0xx-pending-A..D` does not match `S\d{3}`, so L1 must replace each with a
  distinct committed id and set the exact entry path in each row's `used-by`.
- **Its `## Unexercised behavior` independently lists the same P5 opens this
  report classifies**: running swaybg/argv/layer, whether the retargeted link
  is re-read, whether a theme set's restarts took effect, the rendered bytes
  and pixels, and the packaging/tag relation. It claims no gate row and no
  observed behaviour — the §2.2/§2.4 joins are consistent with the landed text.
- **Host declaration confirms the shape** used in §1: `current/theme` is a
  directory (24 top-level files, 8 payload + 16 rendered), `current/background`
  is the only symlink, `theme.name` is `matte-black`, and the round-7 census
  pins agree. No contradiction with `theme-wallpaper-plane.md`.
- **Receipt coverage is complete for the cited swaybg files**: bodies and
  receipts exist for `swaybg.1.scd`, `README.md`, `main.c`,
  `background-image.c`, and the four omarchy scripts plus autostart and the
  theme tree pages under `.ufo/waves/round-18/fetch/NoteTheme/` [OBS].
- Remaining L1 action before measurement: id assignment + exact `used-by`
  paths; ensure at least one assigned row is an upstream `https` row of kind
  `docs`/`spec`/`code` naming theme/wallpaper/swaybg; then run the c2 counter.
  The Walker note's half is checked in §2.6.

### 2.6 Landed Walker note — checked against the landed bytes (sha `53f035e2…`)

The P3 note also landed during this pass; the P3 joins were re-checked against
it:

- **Structure passes what can be checked statically**: line 1 is a `source:`
  line, line 4 is exactly `surface: P3`, all four required level-2 headings
  exist with long bodies, and `[UNK]` is inside `## Unexercised behavior`.
- **Its MOVED-pin table is the canonical old→new report** (it does not edit the
  2026-10-14 notes): `/usr/bin/walker` 6,661,264 → 7,039,912 B, sha
  `64826a85…` → `25240650…`, mtime 2026-07-26 → 2026-10-08;
  `/etc/xdg/walker/config.toml` 13,220 → 13,743 B, sha `5b4e47b7…` →
  `3c5c6867…`; embedded-default offset 784,064 → 806,960; version 2.17.0 →
  2.17.2. My §3.6 append now points at that table; the pins stay date-bounded
  history.
- **The socket-path divergence expected in my first draft is resolved in the
  note**: `src/data.rs` (walker client) and `internal/comm/comm.go` (elephant
  listener) agree on `$XDG_RUNTIME_DIR/elephant/elephant.sock` with an
  `env::temp_dir()` fallback, and the README's `/tmp/elephant.sock` is
  explicitly marked stale for the tag. That path also matches the round-9 host
  observation. The arc §6 narrowing is therefore one notch stronger than my
  first draft: path = documentary + dated-observed; wire schema = `[UNK]`.
- **One correction carried into §3.6**: the note separates a syntax-level
  build error (returns via `?`, then `load().unwrap()` would panic — INF) from
  a build-OK/deserialize failure (`set_error`, defaults stay). My first-draft
  "parse error → set_error" text was too broad.
- **Receipt coverage is complete for every cited file** (`src/data.rs`,
  `internal/comm/comm.go`, `Cargo.toml`, the codeload tarball, the xdg docs
  page, the omarchy scripts/config, the log read) [OBS].
- Remaining L1 action: the single `source:` line carries **19
  `S0xx-pending` tokens — 18 https rows plus the host `/var/log/pacman.log`
  row**; each needs a distinct id, each row needs the exact entry path in
  `used-by`, and at least one must be an upstream `docs`/`spec`/`code` row
  naming `walker` or `elephant`. Then run c2. The note's opens match §4's P3
  list.

## 3. Exact cross-link lines (copy-paste)

### 3.1 README — round-18 Frontier bullet (insert after line 126, EOF)

Recommended text (supersedes FrontierDraft's bullet; the deltas are named in
§3.5):

```
- Round 18 moves P3 Walker and P5 themes/wallpapers onto **documentary** sourced
  ground: [Walker route](knowledge/walker-route-r18.md) and
  [theme route](knowledge/theme-route-r18.md), upstream contracts joined to host
  file bytes. The Walker route narrows the arc's socket-protocol row to the
  documented transport and path (walker activation socket; elephant Unix
  socket + Protocol Buffers, message families only) — wire schema and message
  semantics stay `[UNK]`. Still open: runtime theme application and wallpaper
  reload, which background renders, Walker provider results, the elephant
  service, and rendered UI for both surfaces. Unlanded theme/Walker gate rows
  stay unlanded ([gate residual ledger](knowledge/gate-standing-use.md) §6).
  Host binaries stay `[UNK]`; no theme, wallpaper, walker or elephant command runs.
```

### 3.2 README — round-17 bullet amendment (lines 124-125)

Replace exactly:

```
  actually launches and Alacritty reload effects; P3 Walker and P5
  theme/wallpaper sourced routes. Compiled host binaries stay `[UNK]` (a
```

with:

```
  actually launches and Alacritty reload effects; P3 Walker and P5
  theme/wallpaper sourced routes (landed round 18, next bullet). Compiled
  host binaries stay `[UNK]` (a
```

This keeps the round-17 record true and stops the two bullets contradicting.

### 3.3 README — index rows (insert after line 43)

```
| `knowledge/walker-route-r18.md` (round 18; surface P3) | Documentary upstream contract for Walker v2.17.2 (XDG config/theme resolution, one-shot load, config failure modes, activation socket) and Elephant v2.22.1 (Unix socket + Protocol Buffers IPC, message families, socket path, provider config), joined to the host's declared config and the omarchy v3.8.4 launcher by sha256 and line anchor. Declared configuration is not observed launcher behaviour; wire schema, live resolution, provider results, the running binary and rendered UI stay `[UNK]`. | `source:` S0xx-pending in [SOURCES](SOURCES.md); tag-pinned fetch receipts under `.ufo/waves/round-18/fetch/NoteWalker/`. No walker or elephant process is started or queried. |
| `knowledge/theme-route-r18.md` (round 18; surface P5) | Documentary upstream contract for the omarchy v3.8.4 theme-set/background chain (next-theme copy → `current/theme`, `theme.name`, `current/background` symlink, `swaybg -i … -m fill`) and the swaybg v1.2.2 man page, joined to `current/theme` contents and the consumer imports by sha256 and line anchor. Declared chain is not runtime theme application; which background renders, restart effects, reload effects and pixels stay `[UNK]`. | `source:` S0xx-pending in [SOURCES](SOURCES.md); tag-pinned fetch receipts under `.ufo/waves/round-18/fetch/NoteTheme/`. No theme, wallpaper or swaybg command is run. |
```

### 3.4 `arc-synthesis.md` — append-only addendum (after line 388, EOF)

The §6 table must not be edited. Append:

```
## Append-only addendum — round 18 (2026-10-20, P3/P5 documentary routes)

The §6 table above is the round-10 record and is not edited; §7's "Unknown
(12 named)" count is unchanged (a narrowing is not a closure). Round 18's
documentary routes move exactly one row:

- `walker socket protocol` (line 297) — **narrowed, not closed**.
  `corpus/knowledge/walker-route-r18.md` documents the transport from walker
  v2.17.2 and elephant v2.22.1 bytes: walker's socket is an activation
  trigger (`$XDG_RUNTIME_DIR/walker/walker.sock`, launch call only), and
  walker↔elephant IPC is Unix sockets + Protocol Buffers with message
  families query/activation/menu/subscribe. The wire schema and message field
  semantics remain `[UNK]`; nothing was connected. The elephant socket path is
  resolved by source (`$XDG_RUNTIME_DIR/elephant/elephant.sock`, with
  `env::temp_dir()` fallback) and agrees with the round-9 host observation;
  the README's "typically `/tmp/elephant.sock`" is stale for the v2.22.1 tag.
- `theme live rows / walker live rows` (line 307) — **unchanged**.
  `corpus/knowledge/theme-route-r18.md` documents the declared theme and
  wallpaper chain; no gate read was added, so the round-9 exemptions stand.
- Every other §6 row is untouched by both routes (rendered UI, idle/lock,
  dispatcher, rule/exec-once effects, module text, env vars, stop-cause,
  omarchy cleanliness, battery, exit-flatten).
```

### 3.5 `gate-standing-use.md` — append-only cross-link (after line 506, EOF)

Append:

```
## Cross-link — round 18 P3/P5 documentary routes (2026-10-20)

Append-only; §6's table is the `93e43f8f…` (round-10) record and is not
edited. The round-18 documentary routes settle no row here:

- `theme live rows …` and `walker live-surface rows …` (lines 257-258) —
  **still exempted**. `corpus/knowledge/theme-route-r18.md` and
  `corpus/knowledge/walker-route-r18.md` document declared chains only; no
  gate row was added, so the checks in the §6 table still read 0. The theme
  route cannot supply `theme.wallpaper.live` (no running-swaybg read) and the
  Walker route cannot supply the socket/owner/layer rows (it never connects
  or queries).
- The theme clauses' covering mutant (line 264) is untouched: a knowledge
  note is not a mutant.
- Revision/pin note: the working gate at this write is `fba82a66…`
  (round-14 committed bytes), not `93e43f8f…`; §6's "Check at" column is
  historical. The Walker version pin at `:3212` (`2.17.0`) disagrees with
  `/var/log/pacman.log:2929` (`2.17.0-1 -> 2.17.2-1`,
  2026-10-20T09:16:46 -0300): reported here, not re-anchored. No gate edit
  is a round-18 claim; the live row would FAIL if run and must be re-run and
  re-anchored under the moved-pin rule.
```

### 3.6 `walker-deep-r9.md` — appended cross-link (after line 399, EOF)

Its own closing line invites appends. Append:

```
## Appended cross-link — round 18 (2026-10-20)

`corpus/knowledge/walker-route-r18.md` is the new provenance for §8's
candidate answers; like §8 it does not apply errata to `walker-deep.md`.
Documentary class: upstream source at walker v2.17.2 (`a515085f…`) and
elephant v2.22.1, joined to host file bytes.

- §7 item 3 (XDG honoring) — **narrowed**: `src/config.rs:218-223` resolves
  one `config.toml` through `xdg::BaseDirectories::with_prefix("walker")`;
  the xdg 3.0.0 `find_config_file` reads `$XDG_CONFIG_HOME` first, then
  `XDG_CONFIG_DIRS`. Host resolution remains `[UNK]` (nothing ran).
- §7 item 1 (edit-without-restart) — **mechanism narrowed, discriminator
  still `[UNK]`**: `src/config.rs:7,586-589` holds the config in a
  `OnceLock` and `src/main.rs:108` calls `config::load()` once at startup; a
  whole-tree textual search of the tag finds no `notify::`, no `use notify`
  and no `inotify` call in `src/` (the declared `notify` dependency is unused
  there), and no `reload_config`/`set_config` function. Source-level
  corroboration of the round-9 A–E negatives, not a host observation; code
  the textual search did not match stays `[UNK]`.
- `walker-deep.md` §11 item 5 (`WALKER_` env surface) — **narrowed**:
  `src/config.rs:235-242` merges `Environment::with_prefix("WALKER")
  .separator("_")` after the file; the literal `WALKER_` token is an
  env-override surface by source, not only by adjacency.
- `walker-deep.md` §11 item 6 (parse-error half) — **narrowed, two failure
  modes**: a syntax-level build error returns through `?` (`src/config.rs:221-223`)
  and the `load().unwrap()` at `src/main.rs:108` would panic (INF from code,
  not exercised); a build-OK/deserialize-fail is non-fatal — `set_error("Config:
  {error}")` + `println!`, defaults stay (`src/config.rs:225-231`). The host
  binary's visible behaviour is still unobserved.
- `walker-deep.md` §11 item 7 (`~` in `additional_theme_location`) —
  **narrowed**: `src/theme/mod.rs:60-63` does a textual `.replace("~", &home)`.
- `walker-deep.md` §11 item 1 (theme-part resolution order) — **partly
  narrowed**: `src/theme/mod.rs:53-137` searches XDG theme bases then appends
  `additional_theme_location` last (a later duplicate theme name wins in the
  HashMap), and `setup_theme_from_path` starts from `Theme::default()` so a
  partial theme inherits default parts; the host's resolution of
  `omarchy-default` remains `[UNK]`.
- Version and artifact relation: §1 pinned the on-disk binary at `2.17.0-1`
  (`64826a85…`, 6,661,264 B, 2026-10-14); `/var/log/pacman.log:2929` records
  `2.17.0-1 -> 2.17.2-1` on 2026-10-20T09:16:46 -0300, and the route's MOVED
  table (S015 protocol, old→new) records the new pins: binary `25240650…`,
  7,039,912 B, mtime 2026-10-08; `/etc/xdg/walker/config.toml` `3c5c6867…`,
  13,743 B; embedded-default offset 784,064 → 806,960. The running binary
  stays `[UNK]` (a log line is not a binary fact; no `/proc/<pid>/exe` read),
  and §1's pins are date-bounded history, not contradicted.
```

### 3.7 Back-links the notes should carry (so a reader enters from either side)

Insert these exact lines, one per note, in its intro (after the "Documentary
route only" paragraph):

- `walker-route-r18.md`: `Open ledgers this note narrows: walker-deep-r9.md
  §7 items 1–3 and §8; arc-synthesis.md §6 row "walker socket protocol"
  (transport/message families/path only). The gate residuals in
  gate-standing-use.md §6 stay open.`
- `theme-route-r18.md`: `Open ledger this note narrows: theme-wallpaper-plane.md
  §11 items 1–2/4 (declared mechanism only). The gate residuals in
  gate-standing-use.md §6 (theme live rows, covering mutant) stay open.`

## 4. What stays open after both routes (explicit)

**P3:** running binary identity and version (pacman.log only); on-disk binary
versus tag fidelity (Arch packaging `[UNK]`); live config resolution and
`WALKER_*` field names; array-merge semantics for user `[providers] default`
and `[[providers.prefixes]]`; live reload discriminator; `walker.sock`
request/response and whether the host service honours the documented launch
call; elephant wire schema/field semantics; provider results and scoring;
emergency trigger; `[providers.sets]` behavior; rendered UI; theme rendering
(host `omarchy-default` resolution unobserved); the `notify` dependency
residual (whole-tree textual search only); version skew of the elephant
providers (13 plugins per log/read; running set unobserved). The elephant
socket path is **not** on this list: source and the dated host observation
agree.

**P5:** whether a theme set actually restarted any consumer (the list is
declared, the restarts are `pgrep`-guarded); whether the background symlink is
re-resolved by a running swaybg; which background renders; reload effects;
rendered pixels; Chromium policy adoption; Obsidian chain; display-name
generality beyond `matte-black`; gate theme live rows; the theme choice
(operator-owned).

**Both:** no screenshot, no process query, no socket connect, no source
execution. Compiled host binaries stay `[UNK]`; a pacman.log pkgver is a log
line, not a running-binary fact.

## 5. C2/R17-V3 conditionality (the join is void if the notes fail the instrument)

The c2 counter reads committed bytes only; a note that misses any of these
covers nothing and the ledger addenda must not land:

1. `source:` at column 0 within the first **15** lines, carrying `S###` tokens
   that resolve to `SOURCES.md` rows with `status == mined`, `tier == A`, and
   **`used-by` containing the exact entry path**. The counter splits the
   used-by cell on `,` and requires exact equality after strip
   (`measure.py:124-125`); a parenthetical or a different path form fails.
   Rows must sit inside the `## Registry` section, start with `|`, and have the
   11-column shape (13 split cells); a duplicate id exits 2
   (`measure.py:101-117`). L1 assigns S072-S099; the used-by proposal is
   ConnSourcesUsedBy's lane. **`S0xx-pending` does not match the scanner's
   `S\d{3}` token regex**, and a written range `S072–S075` yields only its two
   endpoints — list each cited id individually before measurement.
2. Exactly one `surface:` line, exact form `surface: P3` / `surface: P5` (two
   surfaces or any trailing text → rejected).
3. At least one cited row of kind `docs`/`spec`/`code` with `https://` in its
   source cell and `walker|elephant` (P3) or `theme|wallpaper|hyprpaper|swaybg`
   (P5) in its source or scope cell.
4. Exact level-2 headings `## Upstream contract`, `## Host declaration`,
   `## Safe observation`, `## Unexercised behavior`, each with ≥3 non-blank
   lines, and `[UNK]` inside the last section's body.
5. Every credited row has a committed raw fetch receipt (`mado-fetch-receipt-v1`:
   body, sha256, bytes, UTC time, tool) under
   `.ufo/waves/round-18/fetch/<Seat>/` — the NoteWalker and NoteTheme
   receipts already exist [OBS].
6. **Both landed notes pass the static structure checks** [OBS]: each has a
   `source:` line at line 1, exactly one `surface:` line (`P3` / `P5` on line
   4), all four exact headings, sections well over the three-line floor, and
   `[UNK]` in `## Unexercised behavior`. Their cited bodies all have receipts:
   NoteWalker covers `src/data.rs`, `internal/comm/comm.go`, the codeload
   tarball and the xdg docs page in addition to the files above; NoteTheme
   covers `main.c`, `background-image.c` and the four omarchy scripts. The
   remaining c2 work is id assignment + exact `used-by`, then the counter.

If any item fails, the honest outcome is 5/6 (P3 or P5 still open) and the
README bullet must name the missing surface instead of linking a note that
does not count.

## 6. Risks / contradictions, stated not smoothed

1. **Gate pin vs package upgrade (S1-adjacent).** `mado-verify.sh:3212`
   expects `walker --version` = `2.17.0`; pacman.log `:2929` records
   `2.17.2-1`. A live gate run would FAIL on `live.walker.version`. Not run
   (host pause). The P3 route must not claim the host runs 2.17.2; the lane
   must report the moved pin and defer re-anchor to a gate-edit round.
2. **Elephant path: README staleness, not a live conflict.** The elephant
   README says "typically /tmp/elephant.sock" [ER:211]; the v2.22.1 source
   shows `$XDG_RUNTIME_DIR/elephant/elephant.sock` (fallback
   `env::temp_dir()`) on both sides [WD:156-161,169; EC:38-44], which agrees
   with the 2026-10-14 host observation. Cite the source, mark the README line
   stale for the tag, and still claim no live read this round.
3. **`current/theme` is a copy, not a symlink.** `omarchy-theme-set:41-42`
   and the host census agree; any wording calling it a symlink contradicts
   both. Only `current/background` is a symlink.
4. **"Themes inherit the default theme"** (walker README:219) means per-part
   fallback in `setup_theme_from_path`, not config inheritance. Do not let
   that sentence become a broader claim.
5. **README self-contradiction.** The round-17 bullet (line 124-125) declares
   P3/P5 routes still open; the round-18 bullet must not leave it standing
   (§3.2). FrontierDraft's "insert after line 125" is off by one (§2.4).
6. **Narrowing ≠ closure.** Do not move `walker socket protocol` out of
   `arc-synthesis.md` §7's 12 unknowns, and do not close any
   `gate-standing-use.md` §6 row. The gate has no new read path.
7. **`WALKER_*` env is walker's config overlay**, not the compositor env row
   (`arc-synthesis.md:302`). Do not let the P3 source finding leak into that
   row.
8. **SOURCES used-by join is a hard dependency.** A `source:` line with the
   right ids but a `used-by` cell that does not name the note is rejected by
   c2; the ledger addenda would then cite a non-crediting note.

## 7. Verification performed (and not performed)

- Read: the four ledgers and their tails, the two round-17 route notes
  (format precedent), **both landed round-18 route notes at the hashes in the
  header**, the c2 implementation in
  `.ufo/waves/round-17/measure.py:145-290`, `SCORECARD.md:931-975`,
  the current gate's Walker/theme rows (`:3195-3232`, `:3470-3500`), the
  committed round-18 fetch bodies for walker/elephant/omarchy-theme-set/
  bg-next/autostart/swaybg, and sibling reports
  (`SrcWalkerConfigPaths`, `SrcWalkerReadme`, `HostThemeFiles`,
  `HostBackgroundChain`).
- Not performed (by contract): no gate run, no `python3 measure.py` against a
  revision, no `walker`/`elephant`/`swaybg`/`omarchy-*`/`systemctl`/`pacman`
  invocation, no socket connect, no fetch (bodies pre-committed), no write
  outside this report.
- Tool installs/updates this seat: **none**.

## 8. Hand-off to L1 (ordered, minimal)

1. Land the two notes only after they pass c2; if one fails, land the other
   and keep the failed surface open (5/6 is the honest result).
2. Assign S072-S099 and set `used-by` to the exact note paths
   (ConnSourcesUsedBy's proposal is the input).
3. Apply README §3.3 rows (after 43), §3.1 bullet (after 126), §3.2 amendment
   (lines 124-125).
4. Apply the three ledger appends: `arc-synthesis.md` §3.4 (after 388),
   `gate-standing-use.md` §3.5 (after 506), `walker-deep-r9.md` §3.6
   (after 399).
5. Carry the Walker pin conflict in the round-18 report as a reported moved
   pin (no gate edit claimed); do not re-run the live gate under the pause.
6. Re-check every line number against the landed note hashes if any ledger
   moved after this write.
