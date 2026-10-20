# SrcOmarchyThemeHooks — omarchy v3.8.4 theme-hook mechanism (documentary)

Scout report. Answers one question: **when do theme-change hooks run in upstream omarchy
v3.8.4, and what exactly does the dispatcher do?** Nothing here was executed: no `omarchy-*`
binary, no hook, no compositor, no pacman, no sudo. Everything below is tag-pinned source
bytes or a file read of the `/tmp` clone.

## Fetch provenance (R17-V3 receipts)

- Repo `basecamp/omarchy`, tag `v3.8.4` → `refs/tags/v3.8.4` =
  `8fcc9d6048af4cb0e3af8512c78049857a3b53dd` via
  `git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4 'refs/tags/v3.8.4^{}'`
  — **lightweight tag**, no `^{}` peeled line returned; the commit is the tag object target.
- 19 receipts, one JSON line each, schema `mado-fetch-receipt-v1`:
  `.ufo/waves/round-18/fetch/SrcOmarchyThemeHooks/receipts.jsonl`
  Raw bodies: same directory, slug `path` with `/`→`_`.
- Every fetch used `curl -sSL --max-time 60 -o BODY -w '%{http_code} %{url_effective}'`,
  all HTTP 200, all `final_url` = `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/<path>`
  (no redirect, no auth). Tool: `curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0 OpenSSL/3.6.5`.
- The GitHub tree API response (`api.github.com/repos/basecamp/omarchy/git/trees/8fcc9d6…?recursive=1`,
  sha256 `c5facb09086f11c1477c0a5553235ed36883816d93d1e4c94a4ddb62adc43c9d`) is the file named
  `tree.json` and **has no receipt line** (it was fetched before the receipt loop started).
  Treat it as an index aid only; no finding below rests on it.
- Cross-check: a `--filter=blob:none --depth 1 --branch v3.8.4` clone in `/tmp/omarchy-r18-src`
  has `git rev-parse HEAD` = the same `8fcc9d60…`. The clone was used only to enumerate
  callers; every file I cite was independently curl-fetched and receipted.

| body slug (sorted) | path at v3.8.4 | bytes | sha256 |
|---|---|---|---|
| `bin_omarchy-battery-monitor` | bin/omarchy-battery-monitor | 834 | `352181b21a3279c65656c8d64608cb10d14faedc9c10b89253de97086c3b729a` |
| `bin_omarchy-first-run` | bin/omarchy-first-run | 1089 | `20508471d8237a60e630baf58f87c0b5a4391e34196ce11e5034745f6a062630` |
| `bin_omarchy-font-set` | bin/omarchy-font-set | 1770 | `03337f4bc74ef625b0ef6cfc8e4ed1f756d71bfb9246c9b825908ca3633b1a1d` |
| `bin_omarchy-hook` | bin/omarchy-hook | 611 | `c64ea844feb1849375e7cd43dde98933293b0e0f0f522e1ba2c6572d86386c7b` |
| `bin_omarchy-hook-install` | bin/omarchy-hook-install | 667 | `f17144bbf34e1ba9905f4cd1889a9eb63f374cd184a526b537f08a2fc0cf0f87` |
| `bin_omarchy-theme-bg-next` | bin/omarchy-theme-bg-next | 1650 | `ee4828127755566d48b46a3775d431601a4d56a9114277ddc78b49c273196c6a` |
| `bin_omarchy-theme-bg-set` | bin/omarchy-theme-bg-set | 671 | `638f265f3a8e62e4d477499627a8f270049df838f038db4f95837acf29acdc05` |
| `bin_omarchy-theme-install` | bin/omarchy-theme-install | 1261 | `894d6c86742b770538665f425b559e477e391b0156e454b165b69de46c257047` |
| `bin_omarchy-theme-refresh` | bin/omarchy-theme-refresh | 254 | `597dd7f2f082e41e54d67ad9be4096b05f8acf72d9c311097e5da1ba2e85216b` |
| `bin_omarchy-theme-set` | bin/omarchy-theme-set | 2147 | `79069c8018a7d6d20f52e357b0b473bd99fad0c5f2914523171687103eeb9516` |
| `bin_omarchy-theme-set-templates` | bin/omarchy-theme-set-templates | 1728 | `01264122666b3d49d4e976837db70d9f9962aa6afd1b2531010c8d7c7d0ea9c0` |
| `bin_omarchy-theme-update` | bin/omarchy-theme-update | 251 | `5d1946e257b8a602df8ff5dd4a98b4df8302a15fc8974c669f21485106ddb8ba` |
| `bin_omarchy-update-perform` | bin/omarchy-update-perform | 575 | `7e1f8ab09b8819b69fcbda35f03dda222ed35ed6b9a8b85b10906df873131a66` |
| `config_omarchy_hooks_theme-set.d_show-theme-notification.sample` | config/omarchy/hooks/theme-set.d/show-theme-notification.sample | 270 | `b9d6754d95057bdb2f37595fd2f40055872118cb2f442bdc7b0b900317bac332` |
| `config_omarchy_themed_alacritty.toml.tpl.sample` | config/omarchy/themed/alacritty.toml.tpl.sample | 2729 | `a05d015227a406470b571d9d8f372eb8042df94b32cf746e71fd2f513c9880ac` |
| `default_hypr_autostart.conf` | default/hypr/autostart.conf | 742 | `acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441` |
| `install_config_all.sh` | install/config/all.sh | 3921 | `b54cf877b0e1e37c3d754304c13e25efb18b6e82d867515bd26f0604eee06dea` |
| `install_config_config.sh` | install/config/config.sh | 182 | `944d7c78911347290dcbb3a7dfabf461e151ce9837b8e8f6e9727bfe4854e30f` |
| `install_config_theme.sh` | install/config/theme.sh | 1114 | `30b5cb8603ae248c089e7a1ae39d10bb0e912c4f56660d986e30112e1ab4ccf5` |

Digests above are copied verbatim from `receipts.jsonl` and each body was byte-compared (`cmp`)
against the same path in the clone at `8fcc9d60…`. Nothing was installed or upgraded this run.

## Observed facts

### F1 — The dispatcher (bin/omarchy-hook, 28 lines)

- Line 3 declares the contract: “Run a named hook from ~/.config/omarchy/hooks/<name> and
  ~/.config/omarchy/hooks/<name>.d/.”
- Line 14-15: `HOOK_PATH="$HOME/.config/omarchy/hooks/$1"` and `HOOK_DIR="$HOOK_PATH.d"`.
  A **bare file** `hooks/<name>` (no `.d`) is also supported; both run.
- Lines 18-19 run the bare file first, then lines 22-27 iterate `"$HOOK_DIR"/*` in shell glob
  (byte-lexicographic) order. There is no dependency ordering, no `run-parts` naming rule and
  no concurrency: each hook is a foreground `bash "$hook" "$@"`.
- Line 19 / 26: failures are **swallowed** — `|| echo "Hook failed: …"` and dispatch continues.
  `set -e` (line 6) never fires on a hook failure.
- Line 25: `[[ $hook == *.sample ]] && continue` — the shipped samples are inert by filename.
- Line 24: `[[ -f $hook ]] || continue` — directories and broken symlinks in the `.d` dir are
  skipped; anything that is a regular file is executed, execute-bit or not.
- Hooks receive exactly the dispatcher's remaining argv; the dispatcher itself adds nothing.

### F2 — When the theme hook runs (bin/omarchy-theme-set)

The whole apply is a single synchronous script with **no `set -e`** (`grep -c 'set -e'` = 0),
so a failing component restart does not abort it. Order inside `omarchy-theme-set`:

1. :17 name normalization — `sed -E 's/<[^>]+>//g' | tr '[:upper:]' '[:lower:]' | tr ' ' '-'`,
   so `Tokyo Night` → `tokyo-night`.
2. :25-30 build `current/next-theme` (`rm -rf`, `mkdir -p`, official theme copy, then user overlay).
3. :38 `omarchy-theme-set-templates` (renders `*.tpl` from `default/themed` + user `themed`).
4. :41-42 swap `next-theme` → `current/theme` (`rm -rf` then `mv`).
5. :45 write `current/theme.name`.
6. :48-50 `omarchy-theme-bg-next` unless `OMARCHY_THEME_SKIP_BACKGROUND=1`.
7. :53-62 `omarchy-restart-{waybar,swayosd,terminal,hyprctl,btop,opencode,mako,helix}`.
8. :65-70 `omarchy-theme-set-{foot,gnome,browser,vscode,obsidian,keyboard}`.
9. :73 `omarchy-hook theme-set "$THEME_NAME" >/dev/null` — **last step, after every consumer
   has already been restarted against the new theme.**

Quote (bin/omarchy-theme-set:73, 5 words):
`omarchy-hook theme-set "$THEME_NAME" >/dev/null`

Consequences that matter to a route note:
- The hook is an **observer of the post-apply state**, not a participant: it cannot pre-empt the
  swap, the template render, the background change or the restarts.
- Only **stdout** is discarded. stderr is not redirected, so a hook's own `>&2` still reaches the
  caller's terminal, but the dispatcher's own `Hook failed: …` line is stdout and is therefore
  invisible in this path.
- There is no theme hook on *failure* paths: a non-existent theme exits at :21 before any hook.
- Because the dispatcher is synchronous, a slow hook delays the command's return even though all
  visual work has already happened.

### F3 — Other entry points that reach the same hook

- `bin/omarchy-theme-refresh:8` — `OMARCHY_THEME_SKIP_BACKGROUND=1 omarchy-theme-set "$(cat $THEME_NAME_PATH)"`
  ⇒ **refresh re-fires `theme-set`** with the same normalized name, skipping only the background.
- `bin/omarchy-theme-install:39` — `omarchy-theme-set $THEME_NAME` after the clone ⇒ install
  fires it too.
- `install/config/theme.sh:13` — `omarchy-theme-set "Tokyo Night"` during install ⇒ the hook
  fires at first install. [INFERENCE] At that moment no active user hook exists yet: the only
  in-tree theme hook is shipped as `.sample` (F4) and `install/config/all.sh` runs `config.sh`
  (the copy) at line 1, before `theme.sh` at line 2.
- `bin/omarchy-theme-update` — only `git -C "$dir" pull` in a loop; **no hook**, no re-apply.
- `bin/omarchy-theme-bg-set` and `bin/omarchy-theme-bg-next` — background only, **no hook**;
  the background changes *before* the hook in the normal theme-set path.
- `bin/omarchy-theme-remove` — removes the directory only; **no hook**, no re-apply.

### F4 — Delivery of the sample, and why a shipped hook is inert

- `install/config/config.sh:3` — `cp -R ~/.local/share/omarchy/config/* ~/.config/` copies the
  sample to `~/.config/omarchy/hooks/theme-set.d/show-theme-notification.sample` **still suffixed
  `.sample`**, which F1 line 25 skips.
- The sample's own header says “To put it into use, remove .sample from this file name.” and
  “This hook is called with the snake-cased name of the theme that has just been set.”
- `bin/omarchy-hook-install` (:18 `HOOK_DIR="$HOME/.config/omarchy/hooks/$HOOK_TYPE.d"`) copies
  a file into the `.d` dir, `chmod 755`, prints the path; it does **not** run it and does not
  strip `.sample` (a source named `x.sample` would land inert).
- Hook classes present at the tag: `battery-low.d`, `font-set.d`, `post-boot.d`, `post-update.d`,
  `theme-set.d` — `theme-set.d` is the only theme-related class. The assignment's example path
  `config/omarchy/hooks/theme-set.sample` **does not exist**; the real artifact is
  `config/omarchy/hooks/theme-set.d/show-theme-notification.sample`.

### F5 — Sibling hook classes, for contrast (same dispatcher)

| class | fires from | quote / anchor |
|---|---|---|
| `post-boot` | Hyprland autostart | `exec-once = sleep 2 && omarchy-hook post-boot` (default/hypr/autostart.conf:16) |
| `post-update` | update pipeline | `omarchy-hook post-update` (bin/omarchy-update-perform:18) |
| `font-set` | font change | `omarchy-hook font-set "$font_name"` (bin/omarchy-font-set:48) |
| `battery-low` | battery monitor | `omarchy-hook battery-low "$1"` (bin/omarchy-battery-monitor:13) |

`bin/omarchy-first-run:23` uses `omarchy-hook-install post-update …install-voxtype.hook` — the
only in-tree use of the installer helper.

### F6 — Tag vs embedded version

`version` at tag `v3.8.4` contains `3.8.3\n` (`od -c` = `3 . 8 . 3 \n`). The tag name is not the
version string; a route note must not derive an installed package version from the tag or vice
versa.

## Confidence

- F1, F2, F4, F5: **high** — small complete files, byte-identical to the curl receipts and to
  the clone at the same commit.
- F3: **high** for the files read (refresh, install, update, bg-set/bg-next, theme-remove);
  the “no hook” entries are negative findings over the full `bin/ config/ install/ default/`
  tree of the clone (`grep -rn 'omarchy-hook' bin config install default` returns exactly five
  call sites — the four in F5 plus `bin/omarchy-theme-set:73` in F2 — together with the
  dispatcher `bin/omarchy-hook`, the installer helper `bin/omarchy-hook-install`, and
  `bin/omarchy-first-run:23` calling the helper). They are not a statement about host-installed
  code.
- The ordering in F2 step 7/8 is from the file as read; `omarchy-restart-*` internals were not
  fetched, so what each restart does is out of scope here.

## Remaining unknowns

- `[UNK]` Host behaviour: whether this host's `~/.config/omarchy/hooks/theme-set.d/` contains any
  active (non-`.sample`) hook, and whether the installed `omarchy-hook` matches these bytes
  (`~/.local/share/omarchy` version was not read by this seat).
- `[UNK]` Runtime effect: what a real theme switch does to a running Waybar/swaybg, whether hooks
  exist at runtime, timing/ordering as observed — all outside a documentary route.
- `[UNK]` `omarchy-restart-*` semantics (fetched by no one in this seat's scope).
- `[UNK]` Whether any out-of-tree hook calls `omarchy-theme-set` recursively; the code has no
  recursion guard (inference from F1/F2, not observed).

## Handoff for L1 / NoteTheme (candidate `theme-route-r18.md` material, P5)

1. Cite this as a **source row** (L1 assigns the id; draft wrote `S0xx-pending`): upstream
   `basecamp/omarchy` @ tag v3.8.4 = commit `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`, files
   `bin/omarchy-hook` (sha256 `c64ea844feb1849375e7cd43dde98933293b0e0f0f522e1ba2c6572d86386c7b`),
   `bin/omarchy-theme-set`
   (sha256 `79069c8018a7d6d20f52e357b0b473bd99fad0c5f2914523171687103eeb9516`),
   `bin/omarchy-theme-refresh`, `install/config/config.sh`,
   `config/omarchy/hooks/theme-set.d/show-theme-notification.sample`; receipt lines in
   `.ufo/waves/round-18/fetch/SrcOmarchyThemeHooks/receipts.jsonl` (must be committed for the
   row to be creditable).
2. Suggested `## Upstream contract` content: dispatcher semantics (F1), theme-set step order and
   the hook being the **last** step with stdout dropped (F2), the refresh/install re-entry (F3),
   the `.sample` inertness and install-time copy (F4).
3. Suggested `## Host declaration` content: only D1-style statements — the declared config path
   `~/.config/omarchy/hooks/theme-set.d/` and the declared sample name; host file existence
   stays `[UNK]` for this seat.
4. Suggested `## Safe observation`: reading `~/.config/omarchy/hooks/theme-set.d/` names and
   `.sample` suffixes as bytes; `sha256sum` of any active hook; no hook execution, no
   `omarchy-*`, no compositor command.
5. Suggested `## Unexercised behavior` (`[UNK]`): actual hook firing on this host, hook ordering
   vs. Waybar/swaybg reload, background change effect, any user hook side effects.
6. Correction to carry into the note: the sample path is `theme-set.d/show-theme-notification.sample`,
   not `theme-set.sample`; and the hook fires **after** the background swap (F2 step 6 vs 9),
   which contradicts any wording that has hooks preparing the theme.

## Files written by this seat

- `.ufo/waves/round-18/fetch/SrcOmarchyThemeHooks/` — 19 raw bodies, `receipts.jsonl`,
  `tree.json` (unreceipted index aid).
- `.ufo/waves/round-18/w1/reports/SrcOmarchyThemeHooks.md` — this report.
- Nothing in `corpus/`, `tools/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `PROVINCE.md`,
  `.gitignore`, or `lessons/` was touched. No lane gate was run.
