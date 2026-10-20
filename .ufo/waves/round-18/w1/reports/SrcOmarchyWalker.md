# SrcOmarchyWalker — omarchy v3.8.4: walker defaults, launcher, elephant defaults

Date: 2026-10-20. Role: leaf scout, read-only. Surface: **P3 Walker**
(join lines to P5 themes are flagged). Scope: the walker configuration and
theme material omarchy ships, the launcher/restart chain, and elephant's
config defaults — all pinned to omarchy tag `v3.8.4`, fetched raw with
R17-V3 receipts, and joined to the host by file bytes only.

Method: `git ls-remote` for tag→commit (allowed network read), GitHub API
tree for path discovery, `curl`-only raw fetches with one receipt per body,
`sha256sum`/`cmp` against the local checkout, `read`/`nl` for anchors, and
`sed` on `/var/log/pacman.log`. No pacman/sudo/systemctl/journalctl/hyprctl/
walker/elephant/omarchy-* invocation, no compositor, service, screenshot or
input probe, no `git` or `jj` command inside the lane, no writes outside this
report and `.ufo/waves/round-18/fetch/SrcOmarchyWalker/`. No tools installed
(`curl 8.23.0`, `python3` stdlib only). LSP: no server serves `.toml`/`.sh`;
text anchoring is the honest instrument here and is labelled as such.

## 0. Result

[OBS] Tag `v3.8.4` is the lightweight tag
`8fcc9d6048af4cb0e3af8512c78049857a3b53dd`; the local checkout is that same
commit (`refs/heads/master` and `refs/tags/v3.8.4` both read `8fcc9d60…` in
`.git/packed-refs`). [OBS] The `version` file at the tag contains `3.8.3\n` —
the tag ships a stale version string; a note must pin the tag/commit, not the
version file. [OBS] All 18 fetched walker/elephant/theme files plus `version`
are **byte-identical** between the tag and the local checkout (19/19 sha256
equal), so the host's omarchy tree is byte-equal to `v3.8.4` on every path
this seat opened.

[OBS] Host walker is `2.17.2-1` (`/var/log/pacman.log:2929`, upgraded from
`2.17.0-1`); host elephant is `2.22.1-1` (`:3095`, upgraded from `2.21.0-1`);
the installed pacman hook fired at `:3123`. Host `~/.config/walker/config.toml`,
`~/.config/autostart/walker.desktop`, the systemd drop-in and all three
`~/.config/elephant/*.toml` are byte-identical to the upstream tag files.

[INFER] The shipped config is a *declaration* — theme name, provider list,
prefixes, emergency action, launch geometry, restart policy. Nothing here is
evidence that walker 2.17.2 parses every key, that elephant 2.22.1 registers
every provider, or that a launch renders anything. Those stay `[UNK]`.

## 1. Pinned target

```text
$ git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4 'refs/tags/v3.8.4^{}'
8fcc9d6048af4cb0e3af8512c78049857a3b53dd	refs/tags/v3.8.4
$ git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.3 'refs/tags/v3.8.3^{}'
6aa2aec1c035d50cfb6871d490cdf9a1169f5ac3	refs/tags/v3.8.3
```

[OBS] No `^{}` line for either tag → both are lightweight tags whose ref is the
commit. Recorded verbatim at
`.ufo/waves/round-18/fetch/SrcOmarchyWalker/git-ls-remote-tags.txt`
(sha256 `6f4b250f486cda9e3dace0340a06f167ff901632ac51688e4323a07f1d06e31c`).

[OBS] Local checkout, read as bytes, no git command:

```text
~/.local/share/omarchy/.git/HEAD            -> "ref: refs/heads/master"
~/.local/share/omarchy/.git/packed-refs:2   -> 8fcc9d60… refs/heads/master
~/.local/share/omarchy/.git/packed-refs:507 -> 6aa2aec1… refs/tags/v3.8.3
~/.local/share/omarchy/.git/packed-refs:508 -> 8fcc9d60… refs/tags/v3.8.4
~/.local/share/omarchy/version              -> "3.8.3\n" (6 bytes,
  sha256 0a5c29521592a324aa0381ac743c15dc552747cd89c5f5c9715e547df40258c6)
```

[OBS] Upstream `version` at the tag is the same 6-byte `3.8.3\n`, sha256
`0a5c2952…`. So `version` is an **upstream tag/version mismatch** (tag
`v3.8.4` carries `3.8.3`), not local drift. A route note that writes
"omarchy 3.8.4" from `version` would be wrong; write
"tag v3.8.4 @ 8fcc9d60, version file 3.8.3".

[OBS] Fetch redirect: every `github.com/basecamp/omarchy/raw/...` URL lands on
`raw.githubusercontent.com/omacom/omarchy/...`; the API tree lands on
`api.github.com/repositories/994093166/git/trees/v3.8.4?recursive=1`. The
repository now resolves under owner `omacom`. Receipts keep both `url`
(basecamp, as requested) and `final_url` (omacom). [INFER] A future verifier
should cite the `omacom` raw URL as canonical and expect the basecamp URL to
keep 301-ing; both fetched `200` today.

## 2. Fetch ledger

19 bodies, 19 receipts, schema `mado-fetch-receipt-v1`, all `http_status 200`,
all body digests re-verified against their files (`19 valid, 0 invalid`):

| body | bytes | sha256 (first 16) |
|---|---|---|
| `tree-v3.8.4.json` (1237 blobs, `truncated:false`) | 401538 | `c5facb09086f11c1` |
| `version` | 6 | `0a5c29521592a324` |
| `config-walker-config.toml` | 1336 | `fecf71fa4253803e` |
| `default-walker-restart.conf` | 38 | `de0f70294000bc29` |
| `default-walker-walker.desktop` | 138 | `5cb9874eedbcb32c` |
| `default-walker-layout.xml` | 6488 | `dbb6bbbe74be894a` |
| `default-walker-style.css` | 1243 | `481267af0e89a475` |
| `bin-omarchy-launch-walker` | 412 | `fd9e93f830bc2286` |
| `bin-omarchy-restart-walker` | 709 | `9ac82d0c1370ec19` |
| `config-elephant-calc.toml` | 14 | `2c0ef81b8edc9edf` |
| `config-elephant-desktopapplications.toml` | 62 | `999b191512b29b68` |
| `config-elephant-symbols.toml` | 81 | `9c0d5edf1fce95f3` |
| `install-config-walker-elephant.sh` | 1200 | `862f198f90a71dfb` |
| `install-first-run-elephant.sh` | 64 | `deef98b0303502b0` |
| `default-elephant-omarchy_themes.lua` | 2922 | `d997d5a4c27ffc10` |
| `default-elephant-omarchy_background_selector.lua` | 2076 | `292c7deb0ddc0d00` |
| `default-elephant-omarchy_unlocks.lua` | 2746 | `b577869246d8050f` |
| `default-hypr-apps-walker.conf` | 80 | `8ebc83e3e1c3c829` |
| `default-themed-walker.css.tpl` | 241 | `d7faea3d54688f6a` |

Full digests, URLs, `final_url`, timestamps:
`.ufo/waves/round-18/fetch/SrcOmarchyWalker/receipts.jsonl`; bodies are the
files above in the same directory. Tree path census (blob paths only, so this
is path-name evidence, not content evidence): 11 paths match `walk`, 8 match
`elephant`, 18 match `themed`. **0 paths** contain `wallpaper` or `swaybg` —
a negative for NoteTheme to use precisely (a path-name absence is not proof
that no file body mentions swaybg).

## 3. Upstream contract — walker config and theme material

`config/walker/config.toml` (the user config omarchy installs):

> `theme = "omarchy-default"` — `config-walker-config.toml:3`
> `additional_theme_location = "~/.local/share/omarchy/default/walker/themes/"` — `:4`

[OBS] The shipped theme name is `omarchy-default` and the theme search root is
the checkout's `default/walker/themes/`. [UNK] whether walker 2.17.2 expands
the literal `~` in that value.

> `default = [` / `"desktopapplications",` / `"websearch",` — `:18-21`

[OBS] Two default providers. Prefix table `:23-45` maps `/`→`providerlist`
(`:23-25`), `.`→`files` (`:27-29`), `:`→`symbols` (`:31-33`), `=`→`calc`
(`:35-37`), `@`→`websearch` (`:39-41`), `$`→`clipboard` (`:43-45`); the
quoted rows are `prefix = "/"` / `provider = "providerlist"` at `:24-25`.
[OBS] `max_results = 256` at `:17`. [OBS] Emergency action:

> `text = "Restart Walker"` / `command = "omarchy-restart-walker"` — `:48-49`

[OBS] Theme CSS is not self-contained: the shipped stylesheet imports the
live theme file, one line, no fallback:

> `@import "../../../../../../../.config/omarchy/current/theme/walker.css";` — `default-walker-style.css:1`

[OBS] Normalizing that relative path from
`~/.local/share/omarchy/default/walker/themes/omarchy-default/` (7 `..`
segments) yields exactly `/home/vgpnk/.config/omarchy/current/theme/walker.css`
(`os.path.normpath`; no filesystem probe). [OBS] The theme template defines
the six colors the stylesheet consumes:

> `@define-color selected-text {{ accent }};` / `@define-color base {{ background }};` — `default-themed-walker.css.tpl:1,3`
> `@define-color border {{ foreground }};` — `:4`

[OBS] The default theme layouts: GTK4 window `id="Window"` (`default-walker-layout.xml:4`),
list `GtkGridView id="List"` with `max_columns` `1` (`:96,100`), and two
placeholder labels, `ElephantHint` with `Waiting for elephant...` (`:61,67`)
and `Placeholder` with `No Results` (`:71,75`). [INFER] The `ElephantHint`
label is the UI affordance for the elephant dependency; it does not show the
dependency is satisfied.

## 4. Upstream contract — launcher, service, restart chain

`bin/omarchy-launch-walker` (412 bytes):

> `if ! pgrep -x elephant > /dev/null; then` / `setsid uwsm-app -- elephant &` — `bin-omarchy-launch-walker:5-6`
> `if ! pgrep -f "walker --gapplication-service" > /dev/null; then` — `:10`
> `exec walker --width 644 --maxheight 300 --minheight 300 "$@"` — `:14`

[OBS] The launcher (a) starts a bare `elephant` process if none matches
`pgrep -x elephant`, (b) starts `walker --gapplication-service` (with
`GSK_RENDERER=cairo`) if the service pattern does not match, (c) then `exec`s
a walker client at fixed geometry `644×300`, passing `"$@"` through.
[INFER] The `--gapplication-service` + plain `walker` split is a
client/service pair over GApplication; the launcher itself never asserts the
service is ready before the `exec`. [UNK] socket/registration timing, and
whether the service-start branch ever waits.

`default/walker/walker.desktop` (autostart source):

> `Exec=walker --gapplication-service` — `default-walker-walker.desktop:4`

`default/walker/restart.conf` (systemd drop-in):

> `Restart=always` / `RestartSec=2` — `default-walker-restart.conf:2-3`

`default/hypr/apps/walker.conf` (window rule applied to the layer):

> `layerrule = no_anim on, match:namespace walker` — `default-hypr-apps-walker.conf:2`

[OBS] `install/config/walker-elephant.sh` copies the desktop entry to
`~/.config/autostart/` (`:4-5`) and the drop-in to
`~/.config/systemd/user/app-walker@autostart.service.d/restart.conf`
(`:8-9`), writes a pacman hook, and symlinks the three elephant menus into
`~/.config/elephant/menus` (`:28-31`). The hook:

> `Target = walker` / `Target = walker-debug` / `Target = elephant*` — `install-config-walker-elephant.sh:17-19`
> `Exec = $OMARCHY_PATH/bin/omarchy-restart-walker` — `:24`

[INFER] `app-walker@autostart.service` is the xdg-autostart-generated unit for
the `walker.desktop` entry; that mapping is standard systemd behavior, not
observed here. [OBS] `bin/omarchy-restart-walker` restarts
`elephant.service` and `app-walker@autostart.service` only when each
`is-enabled` (`bin-omarchy-restart-walker:6-14`), and re-execs its own
function under the invoking owner's uid via `systemd-run` when run as root
(`:17-23`). [UNK] unit state on this host; not queried.

## 5. Upstream contract — elephant defaults

`config/elephant/desktopapplications.toml`:

> `show_actions = false` / `only_search_title = true` / `history = false` — `:1-3`

`config/elephant/calc.toml`: `async = false` — `:1`.

`config/elephant/symbols.toml`:

> `command = 'wl-copy && hyprctl dispatch sendshortcut "SHIFT,Insert,activewindow"'` — `:1`

[OBS] The symbols provider is declared to pipe its selection into `wl-copy`
and then dispatch a Hyprland `sendshortcut`. That is a declared command
string; it is *not* evidence that the shortcut path works, and this round
must not exercise it.

`default/elephant/omarchy_themes.lua` (theme menu): reads
`local user_theme_dir = os.getenv("HOME") .. "/.config/omarchy/themes"` (`:43`),
falls back to `$OMARCHY_PATH/themes` (`:44-45`), de-duplicates by theme name,
and dispatches

> `activate = "omarchy-theme-set " .. theme_name,` — `:80`

`default/elephant/omarchy_background_selector.lua` (wallpaper menu): searches
`home .. "/.config/omarchy/current/theme/backgrounds",` (`:38`) and
`table.insert(dirs, home .. "/.config/omarchy/backgrounds/" .. theme_name)` (`:41`,
only when `current/theme.name` reads), then dispatches

> `activate = "omarchy-theme-bg-set " .. ShellEscape(background),` — `:61`

`default/elephant/omarchy_unlocks.lua` (plymouth/unlock menu): `A "Default"
entry restores the omarchy-shipped Plymouth via omarchy-plymouth-reset` (`:4-5`),
theme entries run `omarchy-plymouth-set-by-theme <theme>` (`:6`) in a floating
terminal (`:7`).

[INFER] Elephant Lua menus are *data providers* with an `activate` command
string; the menu entries are computed at provider-call time by shelling out
(`find`/`ls`). [UNK] provider registration and the `activate` contract at
elephant 2.22.1 — no elephant source or README is in this seat's fetch set
(other seats own it).

`install/first-run/elephant.sh`: `elephant service enable` then
`systemctl --user start elephant.service` (`:1-2`). [OBS] There are therefore
two declared start paths — systemd `elephant.service` at first run and the
bare `elephant` process from the launcher. [UNK] whether the bare command
reaches the same service instance.

## 6. Host declaration (file bytes and pacman.log only)

| fact | evidence |
|---|---|
| walker `2.17.2-1` (from `2.17.0-1`) | `/var/log/pacman.log:2929` |
| elephant `2.22.1-1` (from `2.21.0-1`) | `/var/log/pacman.log:3095` |
| walker-restart hook executed after that transaction | `/var/log/pacman.log:3123` |
| `~/.config/walker/config.toml` = upstream | 1336 B, sha256 `fecf71fa…` (equal to body) |
| `~/.config/autostart/walker.desktop` = upstream | 138 B, `5cb9874e…` |
| systemd drop-in `restart.conf` = upstream | 38 B, `de0f7029…` |
| `~/.config/elephant/{calc,desktopapplications,symbols}.toml` = upstream | `2c0ef81b…`, `999b1915…`, `9c0d5edf…` |
| `/etc/pacman.d/hooks/walker-restart.hook` | sha256 `658171771949d8bc633faf79432cf78f42734423594f57eca695fb70d02888b9`; `Exec = /home/vgpnk/.local/share/omarchy/bin/omarchy-restart-walker` (the `$OMARCHY_PATH` expansion) |
| elephant menus wired | `~/.config/elephant/menus/` holds three symlinks into `~/.local/share/omarchy/default/elephant/` |
| current theme | `~/.config/omarchy/current/theme.name` = `matte-black` (12 B); `current/theme` is a directory (not a symlink) |
| walker theme css | `current/theme/walker.css` regular file, 191 B, 6 lines, sha256 `f44cb45063494d2f4a8f489c47d8901b3bc98b27fbd1ca1c5a8801b40606bbc0`; colors `#e68e0d` accent, `#bebebe` text, `#121212` base |
| current wallpaper | `current/background` is a symlink → `current/theme/backgrounds/0-ship-at-sea.jpg` |

[INFER] The host's walker config is a *regular file*, not a symlink into the
checkout; it happens to be byte-identical, so either it was copied at install
time or edited to the same bytes. The install mechanism for
`config/walker/config.toml` was not in this seat's fetch set → `[UNK]`.

[OBS] The installed hook is **byte-identical** to the installer's heredoc with
`$OMARCHY_PATH` mechanically substituted by
`/home/vgpnk/.local/share/omarchy`: both render
sha256 `658171771949d8bc633faf79432cf78f42734423594f57eca695fb70d02888b9`.
[INFER] That the installer produced the host file is inference; the byte
equality is observed. Because the checkout is at the same commit, a restart
after a walker/elephant upgrade would execute the tag-equal script. Whether
the hook is currently armed is a pacman database fact, not a file fact — the
last observed run at `:3123` shows it was armed then.

## 7. Safe observation boundary (what this establishes, and only this)

Safe and used: `curl` to tag-pinned URLs, `sha256sum`, `cmp`-equality by
digest, `nl`/`grep` on fetched bodies, `sed`/`grep` on `/var/log/pacman.log`,
`ls`/`stat`/`readlink` on config trees, `python3` for normpath and JSON.
Every claim in §3-§5 is about bytes at tag `v3.8.4`; every claim in §6 is
about bytes on this host or a pacman.log line. The two are joined only by
digest equality.

Not used: `pgrep`, `systemctl`, `journalctl`, `hyprctl`, `walker`,
`elephant`, `uwsm-app`, `omarchy-*`, `pacman`, any compositor or input probe.

## 8. Unexercised behaviour — `[UNK]`

- Whether walker `2.17.2` accepts the shipped keys (`force_keyboard_focus`,
  `selection_wrap`, `hide_action_hints`, `additional_theme_location`,
  `[columns] symbols`, `max_results`) — the schema of the binary is not in
  this fetch set. `[UNK]`
- Whether walker expands `~` in `additional_theme_location`. `[UNK]`
- GApplication service/client registration, timing, and whether the
  one-shot `exec walker --width …` window is a client of the service. `[UNK]`
- Whether `pgrep -x elephant` matches the process started by
  `elephant.service` (comm name, not queried). `[UNK]`
- Elephant 2.22.1 provider protocol, menu registration, `activate` string
  execution, and whether the Lua `find`/`ls` calls run per keystroke. `[UNK]`
- The theme render step that turns `default/themed/walker.css.tpl` into
  `~/.config/omarchy/current/theme/walker.css`, and whether `matte-black`
  produced the observed 6 lines. Only the tpl and the output file are
  evidenced. `[UNK]`
- Runtime theme application: no `omarchy-theme-set`, no wallpaper reload, no
  `swaybg`/`hyprpaper` process observation. `[UNK]`
- Rendered Walker UI, `ElephantHint` label visibility, GTK layout at runtime. `[UNK]`
- Pacman hook arming in the current pacman database; only the historical run
  at pacman.log `:3123` is observed. `[UNK]`

## 9. Proposed SOURCES rows (S0xx-pending; L1 assigns S072-S099)

11-column shape, `status`/`used-by` are the target state L1 must confirm at
integration. Each row's source or scope cell names walker/elephant, so any of
the three satisfies the P3 upstream-row clause. Canonical URL is the
`omacom` final URL with the basecamp URL recorded in the receipt.

```text
| S0xx-pending | omarchy v3.8.4 walker defaults — https://raw.githubusercontent.com/omacom/omarchy/v3.8.4/config/walker/config.toml | code | A | walker 2.17.2 config shipped by omarchy: theme and additional theme location, default providers, prefix providers, emergency restart, desktop entry, restart policy, css theme import | config/walker/config.toml:3-4,17-21,23-45,47-49; default/walker/walker.desktop:4; default/walker/restart.conf:2-3; default/walker/themes/omarchy-default/style.css:1; default/themed/walker.css.tpl:1-6; sha256s in .ufo/waves/round-18/fetch/SrcOmarchyWalker/receipts.jsonl; tag v3.8.4 = 8fcc9d60… | walker runs as a gapplication service themed from the live theme css; the shipped config declares defaults, not observed launch or provider behaviour | mined | 2026-10-20 | on-change | corpus/knowledge/walker-route-r18.md |
| S0xx-pending | omarchy v3.8.4 walker/elephant launch and restart chain — https://raw.githubusercontent.com/omacom/omarchy/v3.8.4/bin/omarchy-launch-walker | code | A | walker/elephant launch order and geometry; pacman hook targets and restart path; elephant menu symlinks | bin/omarchy-launch-walker:5-14; bin/omarchy-restart-walker:6-23; install/config/walker-elephant.sh:4-31; sha256 fd9e93f8…, 9ac82d0c…, 862f198f… | launcher starts elephant and the walker service, then execs a fixed-geometry client; the hook restarts walker/elephant after upgrades | mined | 2026-10-20 | on-change | corpus/knowledge/walker-route-r18.md |
| S0xx-pending | omarchy v3.8.4 elephant defaults — https://raw.githubusercontent.com/omacom/omarchy/v3.8.4/config/elephant/desktopapplications.toml | code | A | elephant 2.22.1 provider defaults shipped by omarchy: desktopapplications, calc, symbols; theme/background/unlock menus and their activate commands | config/elephant/desktopapplications.toml:1-3; calc.toml:1; symbols.toml:1; default/elephant/omarchy_themes.lua:43-45,80; omarchy_background_selector.lua:38,41,61; omarchy_unlocks.lua:4-7; sha256s in .ufo/waves/round-18/fetch/SrcOmarchyWalker/receipts.jsonl | provider behaviour is configured by files; the theme and background menus dispatch omarchy-theme-set and omarchy-theme-bg-set; command strings are declarations, not exercised effects | mined | 2026-10-20 | on-change | corpus/knowledge/walker-route-r18.md |
```

Ready-to-use head line for the P3 note (≤15 lines, `source:` + `surface: P3`
must be exact):

```text
source: S0xx-pending https://raw.githubusercontent.com/omacom/omarchy/v3.8.4/config/walker/config.toml (walker config); S0xx-pending https://raw.githubusercontent.com/omacom/omarchy/v3.8.4/bin/omarchy-launch-walker (launcher); S0xx-pending https://raw.githubusercontent.com/omacom/omarchy/v3.8.4/config/elephant/desktopapplications.toml (elephant defaults)
```

## 10. Notes for the integrator

1. **Pin the commit, not `version`.** Tag `v3.8.4` = `8fcc9d60…`; its
   `version` file says `3.8.3`. Writing "omarchy 3.8.4" from `version` is
   falsified by the tag's own bytes; write the tag/commit pair.
2. **R17-V3 satisfied.** Every row above maps to bodies under
   `.ufo/waves/round-18/fetch/SrcOmarchyWalker/` with schema-valid receipts
   (19/19 re-verified). NoteWalker may reuse these receipts or must open its
   own; it must not cite a row without one.
3. **P3↔P5 join is byte-proven and narrow.** Walker's stylesheet imports the
   theme-plane file; the host currently resolves it to `matte-black`
   (`f44cb450…`). The *render step* that produces that file is not in this
   seat's evidence — NoteTheme owns it. This is the only cross-surface claim
   this report supports.
4. **Double start paths.** `elephant.service` (first-run) and bare `elephant`
   (launcher) are both declared; a route note must not claim one is
   authoritative at runtime.
5. **Host binaries stay `[UNK]`.** pacman.log gives package versions only;
   nothing here shows walker/elephant internals at those versions.

## 11. Reproduction

```sh
D=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/fetch/SrcOmarchyWalker
python3 - "$D" <<'PY'
import json,hashlib,os,sys
d=sys.argv[1]; ok=0
for line in open(os.path.join(d,"receipts.jsonl")):
    r=json.loads(line); b=os.path.join(d,r["body"])
    assert r["schema"]=="mado-fetch-receipt-v1" and r["http_status"]==200
    assert hashlib.sha256(open(b,"rb").read()).hexdigest()==r["sha256"]
    assert os.path.getsize(b)==r["bytes"]; ok+=1
print("receipts valid:",ok)
PY
# tag -> commit (read-only network)
git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4
# host byte-equality for the walker config
sha256sum ~/.config/walker/config.toml "$D/config-walker-config.toml"
# host versions
sed -n '2929p;3095p' /var/log/pacman.log
# css import resolves into the theme plane
python3 -c 'import os;b=os.path.expanduser("~/.local/share/omarchy/default/walker/themes/omarchy-default/style.css");print(os.path.normpath(os.path.join(os.path.dirname(b),"../../../../../../../.config/omarchy/current/theme/walker.css")))'
```

## 12. Confidence

- Tag/commit identity, digest equality of all 19 bodies, host file equality,
  pacman.log line numbers: **high** (byte-level, re-checkable).
- Declared launch order, hook targets, menu dispatch strings: **high** as
  *declarations* (verbatim bytes), no runtime claim.
- Client/service split, xdg-autostart unit mapping, elephant start-path
  equivalence: **medium** (`[INFER]`, standard behaviour, not observed).
- Any runtime behaviour of walker 2.17.2 / elephant 2.22.1: **none** — `[UNK]`.
