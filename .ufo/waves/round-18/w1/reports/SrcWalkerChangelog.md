# SrcWalkerChangelog — walker 2.17.x release notes: config delta 2.17.0 → 2.17.2

Seat: `MadoR18.SrcWalkerChangelog` (leaf scout). Round 18 / hyaku phase 2.
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Baseline `d9a5a18`,
pre-registration `d3a0000`. Access date for every network read: **2026-10-20**
(UTC fetch times in §1). Question answered: the three requested GitHub release
payloads and exactly which config-affecting changes separate walker v2.17.0
from v2.17.2, as freshness input for the r9/r17 walker notes.

Safety: host pause honoured. No walker/pacman/systemctl/journalctl/hyprctl or
compositor invocation, no service or socket touch, no `--version`. Host facts
are file reads only (`/var/log/pacman.log`, `stat`/`sha256sum`/`grep` of
config and binary bytes). Network: unauthenticated `curl` to
`api.github.com` / `raw.githubusercontent.com` / `git ls-remote` only.
No files written outside this report, its fetch directory, and `/tmp`.

## 0. Bottom line

- **All three release payloads fetched cleanly** (HTTP 200) and the tag chain
  was pinned: v2.17.0 = annotated tag `2a4bde0…` → commit `42b3ed8…`;
  v2.17.1 = lightweight `56c9e2b…`; v2.17.2 = lightweight `a515085…` (§1).
- **The whole v2.17.0→v2.17.2 delta is 7 commits across 12 files** (compare
  API, `ahead_by 7`, base/merge-base `42b3ed8`). The v2.17.1 + v2.17.2
  release notes list 4 + 3 = 7 commits, same SHAs (§2, §4).
- **Every config-surface addition landed in v2.17.1** (published
  2026-09-24): top-level `blur_corner_radius = 20`; a new `[niri]` table with
  `launch_on_empty_workspace` / `launch_on_startup` / `cmd_on_esc`; a new
  default `desktopapplications` keybind `{ action = "edit", bind = "ctrl e" }`;
  and the clipboard `remove` default `after` switched from `AsyncClearReload`
  to the new `SimpleDelete` `AfterAction` (§3).
- **v2.17.2 adds no config key.** Its only `resources/config.toml` edit is a
  comment rewrite on line 22 (the v2.17.1→v2.17.2 file diff is exactly that one
  line). Its real payload is a GTK 4.24 blur-crash fix plus GTK crate bumps (§3, §4).
- **Host chain (OBS, file reads):** `walker 2.17.0-1 -> 2.17.2-1` at
  `pacman.log:2929` (2026-10-20T09:16:46-0300), `gtk4 4.22.4-1 -> 4.24.1-1`
  at `:2641`. `/usr/bin/walker` is now 7,039,912 B, mtime 2026-10-08
  11:14:32 -03, sha256 `25240650…`. `/etc/xdg/walker/config.toml` is
  13,743 B / `3c5c6867…`, **byte-identical to the v2.17.2 tag's
  `resources/config.toml`**; r9's old pin 13,220 B / `5b4e47b7…` is
  **byte-identical to the v2.17.0 tag file**. The user overlay is unchanged
  (1,336 B / `fecf71fa…`) and contains none of the new keys (§5).
- **On GTK ≥ 4.24 walker no longer attaches its own background-effect blur**
  (`gtk4::minor_version() < 24` gate). With host GTK 4.24.1, both
  `ext_background_effect_blur` and `blur_corner_radius` are inert; GTK owns
  the effect and derives its region from the theme's `.box-wrapper`
  border-radius. That is also what the 2.17.2 crash fix is about (§3.3).
- **Freshness result:** r9's identity pins and config-layer pins are stale but
  explainable (they are the 2.17.0 bytes), and several present-tense corpus
  pins (`SKILL.md:114`, `walker-live-surface.md:19,37-38`,
  `walker-deep.md:27`, etc.) describe a version the host no longer has (§6).
  The r9 *mechanism* conclusion ("no reload path — restart is the apply path")
  is not contradicted by the delta: no CLI flag, D-Bus method, or config
  watcher was added in the 7 commits; the new niri listener watches workspace
  focus only (§6.3).

## 1. Tag pins, published notes, receipts

Tag resolution by `git ls-remote https://github.com/abenz1267/walker 'refs/tags/v2.17*'`
(2026-10-20; no lane write):

| Tag | Ref shape | Tag object / commit | Peeled commit | Release published (API) |
|---|---|---|---|---|
| `v2.17.0` | annotated (two lines) | `2a4bde009b0deb34e6f9cdd1a4f8c2457e33c18f` | `42b3ed88abf50bc52638fb2835b7f17e3ea3ac4c` | `2026-07-16T16:10:05Z` |
| `v2.17.1` | lightweight (no `^{}` line) | `56c9e2b69e7d2b00f0f9481ae8c89f53810c1de5` | same | `2026-09-24T06:42:02Z` |
| `v2.17.2` | lightweight (no `^{}` line) | `a515085fd39fae80acc086c8fbfd9b7771a9a11d` | same | `2026-10-08T06:49:30Z` |

The compare API independently confirms base/merge-base `42b3ed8` and head
`a515085` (§4). The release-note text is the JSON `body` string on line 78 of
each saved release payload; quotes below anchor there.

Receipt protocol: `curl -sSL --max-time 60 -o BODY -w '%{http_code} %{url_effective}' URL`;
one JSON line per fetch in `receipts.jsonl` (schema `mado-fetch-receipt-v1`).
All fetches HTTP 200, tool `curl 8.23.0`.

| Body (saved under `.ufo/waves/round-18/fetch/SrcWalkerChangelog/`) | URL | Bytes | sha256 |
|---|---|---|---|
| `walker-release-v2.17.0.json` | `https://api.github.com/repos/abenz1267/walker/releases/tags/v2.17.0` | 4,946 | `37d9fcdb0f9a536f9573cec6e0e5c430082855c23866e015348f0a6e4b55cee0` |
| `walker-release-v2.17.1.json` | `…/releases/tags/v2.17.1` | 4,395 | `3ce44ee021a26deda61716a910acd69a4a92044ef41793cc487c1e078c9e9d8b` |
| `walker-release-v2.17.2.json` | `…/releases/tags/v2.17.2` | 4,305 | `30e642b0d6bcd2290f2a67eee2c2806ea63d48f56a46b8ca3dd83814fc895e56` |
| `walker-compare-v2.17.0-v2.17.2.json` | `…/compare/v2.17.0...v2.17.2` | 121,140 | `a63c7bdbf4909de68f4fd3224935762eb1ab7719016550e7669b863e5332a774` |
| `walker-v2.17.0-resources-config.toml` | `raw.githubusercontent.com/abenz1267/walker/v2.17.0/resources/config.toml` | 13,220 | `5b4e47b7d2314bf8b2fda1e85d9e55126ef4a1f62a984f8e03f78ee6c74d63e6` |
| `walker-v2.17.1-resources-config.toml` | `…/v2.17.1/resources/config.toml` | 13,731 | `be6099be55c4575f39ad6e0fadc5af61f4a8ecb1d39ce4ca4a0e32b7117f3e2a` |
| `walker-v2.17.2-resources-config.toml` | `…/v2.17.2/resources/config.toml` | 13,743 | `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b` |
| `walker-v2.17.2-README.md` | `…/v2.17.2/README.md` | 7,926 | `9755f955d5c4e460ac8538e1b648ba2a3c86da37ceaa4d0655dca4d1ea3d2456` |
| `walker-v2.17.2-src-niri.rs` | `…/v2.17.2/src/niri.rs` | 11,838 | `f18846831c9741cdac4498f94baaaef85aa79c35a63e9dc9a6a4a0a2c1cff167` |

Fetch times: releases `15:40:14–15:40:15Z`, compare `15:40:44Z`, config/README
`15:41:42Z`, v2.17.1 config `15:42:41Z`, niri source `15:45:36Z` (2026-10-20).
Raw tag URLs are pinned by the tag→commit table above; a tag is not immutable,
so both the ls-remote result and the body digests are recorded. These bodies
and `receipts.jsonl` are staged in the round-18 fetch tree for L1's lane
commit; this seat performed no git/jj write.

Release asset note (OBS, from the already-saved v2.17.2 release JSON): the
official `walker-v2.17.2-x86_64-unknown-linux-gnu.tar.gz` is 2,772,997 B with
API digest `sha256:57e68d1f9f14782f1ae0f1c704509749a545a92531b8788b76b16bc29fcc5c19`.
It was **not downloaded** — the receipt body cap is 1 MiB — so host binary ↔
release artifact equality is UNK (§7).

Candidate upstream rows for L1's `SOURCES.md` mining (upstream https code/docs
at the immutable tag, each with a raw-body receipt above): the three release
payloads, `resources/config.toml` and `README.md` at `v2.17.2`, and
`src/niri.rs` at `v2.17.2`. Their `used-by` can name the walker route note
(P3) and the r9 freshness update; the R17-V3 committed-receipt requirement is
satisfied by the bodies + `receipts.jsonl` in this directory once L1 commits
them. Assign the `S###` ids in `payload`.


## 2. The release notes as published

### 2.1 v2.17.0 (published 2026-07-16T16:10:05Z; "Commits since v2.16.2")

Verbatim bullets (`walker-release-v2.17.0.json:78`):

- `bump version (42b3ed8)`
- `fix(preview): strip file:// scheme in preview_file() (#732) (eba3041)`
- `fix(keybinds): show_actions config not being merged (3463b74)`
- `fix(providers): non-ASCII absolute icon paths render as images (#727) (0810315)`
- `feat(protonpass): add action handling (5e9dd90)`
- `fix(config): correct bitwarden TOTP action names (#724) (4866257)`
- `clipboard: handle new show_pinned_only action (3623b93)`
- `feat(aptpackages): implement aptpackages provider (#720) (e0ddb89)`
- `remove discord link (aa1e4b7)`

These are **below the baseline** for this seat (they separate v2.16.2 from
v2.17.0); r9 already measured the binary that contains them. The two clearly
config-surface entries are the `show_actions` merge fix and the clipboard
`show_pinned_only` action; the rest are provider-surface changes or provider
fixes (protonpass/aptpackages, bitwarden TOTP action names, preview and icon
fixes). They are listed for completeness, not counted in the 2.17.0→2.17.2
delta.

### 2.2 v2.17.1 (published 2026-09-24T06:42:02Z; "Commits since v2.17.0")

Verbatim bullets (`walker-release-v2.17.1.json:78`):

- "feat(desktopapps): support new edit action (56c9e2b)"
- "feat: configurable rounded blur region (blur_corner_radius) (#737) (dcb4d68)"
- "feat: add SimpleDelete after action (253f44f)"
- "feat: add niri ipc integration + config (c299cd8)"

### 2.3 v2.17.2 (published 2026-10-08T06:49:30Z; "Commits since v2.17.1")

Verbatim bullets (`walker-release-v2.17.2.json:78`):

- "fix: GTK 4.24 blur handling causing crash (a515085)"
- "general: updated GTK4 dependencies (ebe4ade)"
- "chore(nix): update flake (#742) (d885437)"

Cross-check (OBS): compare `total_commits` = 7; commit series is
`c299cd8`, `253f44f`, `dcb4d68`, `56c9e2b`, `d885437`, `ebe4ade`, `a515085`
— the v2.17.1 + v2.17.2 bodies' abbreviated hashes are exactly these seven,
and the two tag commits (`56c9e2b`, `a515085`) are the last bullet of their
respective releases.

## 3. Config-affecting delta 2.17.0 → 2.17.2

The default provider table is machine-checkable: diffing the two tagged
`resources/config.toml` bodies yields **8 inserted lines and 1 replaced line**
(`+8/-1`), all shown below with v2.17.2 line numbers. No key was removed or
renamed; the additions are serde-optional in `PartialWalker`, so a 2.17.0-era
user config keeps parsing (INF from `src/config.rs` hunk in §4).

| # | Surface (v2.17.2 anchor) | v2.17.0 | v2.17.2 | Landed | Effect |
|---|---|---|---|---|---|
| 1 | `blur_corner_radius` (top level, `config:22`) | absent | `blur_corner_radius = 20` (i32) | v2.17.1 (`dcb4d68`) | Rounded blur region instead of a full rectangle **only** when walker attaches blur itself. `src/config.rs` adds the field and merge; `src/wayland_blur.rs` builds per-row rounded rects with `radius.clamp(0, w/2).clamp(0, h/2)`; `r <= 0` falls back to one full rect. Comment: "blur region radius on GTK older than 4.24; GTK 4.24+ uses the theme's .box-wrapper border-radius" (`config:22`). |
| 2 | `[niri]` table (`config:24-27`) | absent | `[niri]` then `launch_on_empty_workspace = false`, `launch_on_startup = false`, `cmd_on_esc = ""` | v2.17.1 (`c299cd8`) | New `Niri` struct + `PartialNiri` merge in `src/config.rs`; new `src/niri.rs` (399 lines) watcher; `src/main.rs` attaches a glib-unix fd listener at startup. README: "When Walker runs as a service, it can watch Niri's event stream…" (`README:187-190`). Requires `--gapplication-service` (`ApplicationFlags::IS_SERVICE`; otherwise stderr note and no listener) and a Niri IPC socket. Defaults are false/empty, so the watcher does not start unless opted in. |
| 3 | `desktopapplications` default keybind (`config:174`) | row absent | `{ action = "edit", bind = "ctrl e" }` | v2.17.1 (`56c9e2b`) | New default binding for the provider's edit action (provider-side support is the named feature). Keybind-layer only; no other provider default changed. |
| 4 | clipboard `remove` `after` (`config:250`) | `after = "AsyncClearReload"` | `after = "SimpleDelete"` | v2.17.1 (`253f44f`) | New `AfterAction::SimpleDelete` variant (`src/keybinds.rs`). `src/ui/window.rs` removes the selected item from the visible `ListStore`, clamps selection, then `handle_changed_items()`/`set_keybind_hint()` — no provider re-query. Default clipboard delete is now a local row removal rather than a clear+reload. |

### 3.1 The v2.17.2 config edit is comment-only (OBS)

The v2.17.1 file (`be6099be…`, 13,731 B) and v2.17.2 file (`3c5c6867…`,
13,743 B) differ by exactly one line:

- v2.17.1: `blur_corner_radius = 20            # corner radius of the blur region (only used when ext_background_effect_blur is true)`
- v2.17.2: `blur_corner_radius = 20            # blur region radius on GTK older than 4.24; GTK 4.24+ uses the theme's .box-wrapper border-radius`

Key, value, ordering and every other line are identical (12 B net is the
comment text). So the config schema was complete at v2.17.1; v2.17.2 only
documents the GTK gate.

### 3.2 The GTK 4.24 gate changes what the existing blur keys do (OBS code)

`src/ui/window.rs` (2.17.2) now reads:

- `if get_config().ext_background_effect_blur && gtk4::minor_version() < 24 { attach_blur(…) }`

with the comment "GTK 4.24 owns the background effect object and derives its
region from CSS." Consequences:

- `ext_background_effect_blur` still parses on every version, but walker's own
  ext-background-effect attach is **skipped entirely on GTK ≥ 4.24**; the
  region then comes from the theme's `.box-wrapper` border-radius.
- `blur_corner_radius` is read only inside `attach_blur`'s `init_context`, so
  it is inert on GTK ≥ 4.24. Host GTK is 4.24.1 (§5), so both are inert here.
- The 2.17.2 fix is the crash avoidance for the 4.24 path, not a new config
  key. On the host, the user overlay does not enable
  `ext_background_effect_blur` (grep finds none), so this path is not selected
  by host config either.

### 3.3 `cmd_on_esc` execution semantics (OBS code, documentary)

When -- and only when -- walker was auto-launched by the niri watcher and is
closed with Escape, `run_auto_launch_escape_command` runs the configured
string through `sh -c` with stdin/stdout/stderr set to null. README:
"`cmd_on_esc` is optional and only runs when Escape closes Walker after an
automatic launch." (`README:199-200`). Empty string (the default) is a no-op.
This is a shell-exec surface in a config file; the route notes should record
it as such, not as a verified host behaviour (host is Hyprland and the key is
unset).

## 4. Non-config deltas in the same 7 commits (for scope honesty)

From the compare payload (12 files, +957/−230 including lockfiles):

- `Cargo.toml`: `gtk4 ^0.9.7 -> ^0.11.5` (features unchanged: `v4_6`,
  `v4_12`, `gio_v2_80`), `gtk4-layer-shell 0.5.0 -> 0.8.1`,
  `gdk4-wayland ^0.9 -> ^0.11.5`, added `glib-unix = "0.22"` and
  `niri-ipc = "=26.4.0"` (exact pin). `Cargo.lock` +306/−193.
- `src/main.rs` +79/−14: `glib::unix_fd_add_local` → `glib_unix::unix_fd_add_local`
  for the activation socket too, `connect_handle_local_options` migrated to
  `ControlFlow`, `set_is_auto_launched(false)` per command line, and the new
  `listen_niri_workspaces` + startup hook. No new CLI flag is added in this
  diff.
- `src/niri.rs` new +399: Niri event-stream watcher. Body checked (receipt in
  §1): `Socket::connect()` then `Request::EventStream`; handled events are
  `WorkspacesChanged`, `WindowsChanged`, `WindowOpenedOrChanged`,
  `WindowClosed`, `WorkspaceActivated`, `OverviewOpenedOrClosed`; deferred
  launch across an open overview and a 1 s reconnect loop. No config path,
  file read or reload entry point appears in the module.
- `src/state/mod.rs` +9: `is_auto_launched` state.
- `src/ui/window.rs` +54/−10: GTK 4.24 gate, `SimpleDelete` handler,
  Escape auto-launch command, quit-state reset.
- `src/wayland_blur.rs` +29/−2: radius field and rounded-region construction.
- `README.md` +16: only the new "Niri workspace launch" section (`README:187-201`).
- `flake.lock` 6/6, `Cargo.lock` as above: dependency churn.

No reload/watch of `config.toml` is added anywhere in these 12 files. The only
new watcher is the niri workspace stream, gated on niri config flags; its
module body was read and contains only the IPC event loop (see above).

## 5. Host chain, read-only (freshness ground truth)

All host values below are **file reads only**; no package, service, process or
compositor query was executed.

| Fact | Value | Evidence |
|---|---|---|
| walker first installed | `2.16.2-1` | `/var/log/pacman.log:1095` |
| upgraded to 2.17.0 | `2.16.2-1 -> 2.17.0-1` | `pacman.log:1943` |
| gtk4 upgraded | `1:4.22.4-1 -> 1:4.24.1-1` at 2026-10-20T09:16:33-0300 | `pacman.log:2641` |
| walker upgraded | `2.17.0-1 -> 2.17.2-1` at 2026-10-20T09:16:46-0300 | `pacman.log:2929` |
| current binary | `/usr/bin/walker` 7,039,912 B, mtime 2026-10-08 11:14:32 -03, sha256 `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096` | `stat` + `sha256sum` (file read) |
| packaged default config | `/etc/xdg/walker/config.toml` 13,743 B, mtime 2026-10-08 11:14:32 -03, sha256 `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b` | `stat` + `sha256sum` |
| = v2.17.2 tag file? | **yes**, same sha256 as `walker-v2.17.2-resources-config.toml` | §1 receipt |
| = r9's old pin? | r9's `/etc/xdg` pin `5b4e47b7…` / 13,220 B is **the v2.17.0 tag file** byte-for-byte | `walker-deep-r9.md:64` + §1 receipt |
| user overlay | `~/.config/walker/config.toml` 1,336 B, mtime 2026-10-03 17:44:32 -03, sha256 `fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787`; no `blur_corner_radius`, `[niri]`, `launch_on_*`, `ext_background_effect_blur` or `SimpleDelete` line | `stat`, `sha256sum`, `grep` (file reads) |
| autostart unit file | `~/.config/autostart/walker.desktop` 138 B, sha256 `5cb9874eedbcb32c7b121ea60f6433f881499247cac7e6473a9a93adeebc3aa7`, `Exec=walker --gapplication-service` (PATH-resolved); unchanged from r9's pin `5cb9874e…` | `stat`, `sha256sum`, `grep` (file reads) |
| build/install dates | binary mtime 2026-10-08 11:14:32 -03 (= 14:14:32Z) is after the v2.17.2 release publication 06:49:30Z the same day; install/upgrade per `:2929` | [INF] consistent with the 2.17.2 Arch package, not proof of exact tag identity |

The packaged-config equality is the strongest source↔host bridge available
under the pause: the Arch package's `/etc/xdg` file is byte-identical to the
v2.17.2 tag's `resources/config.toml`, and the old file was byte-identical to
the v2.17.0 tag's file. That does **not** prove the executable was built from
commit `a515085`; it proves the packaged config layer did move between the two
tagged configs. Binary bytes are pinned above for a later seat that may hash
the official tarball (not fetched here; >1 MiB).

## 6. Freshness impact on r9 / r17 notes

### 6.1 Directly stale pins (present tense no longer true)

| Note / anchor | Old observed pin | Current host fact |
|---|---|---|
| `walker-deep-r9.md:30,58,60,78,103` | walker 2.17.0, `2.17.0\n`, package 2.17.0-1, Build Date 2026-07-26, binary 6,661,264 B / `64826a85…` | package 2.17.2-1 (`:2929`), binary 7,039,912 B / `25240650…`, mtime 2026-10-08 11:14:32 -03; `--version` bytes not re-measured (pause) but the package version is logged |
| `walker-deep-r9.md:64,69-70` | packaged config 13,220 B / `5b4e47b7…`; embedded default blob at offset 784,064 equals it | packaged config 13,743 B / `3c5c6867…` = v2.17.2 tag file; embedded-blob offset and equality not re-measured (binary changed by +378,648 B; embedded config grew +523 B) |
| `walker-deep-r9.md:305,316-317` | binary offsets 847,791 for the `2.17.0\n` literal run | 2.17.0-only offsets; the 2.17.2 binary is a different size, so every quoted offset must be re-derived before reuse |
| `walker-live-surface.md:19,37,38` | 2.17.0, `2.17.0\n`, binary `64826a85…` | same supersession; help-family sha256 values were not re-run (walker execution forbidden) |
| `walker-deep.md:27`; `waybar-walker-semantics.md:23`; `waybar-walker-plane.md:38,197,405`; `remaining-planes-census.md:246`; `closeout-r11.md:43`; `arc-synthesis.md:229` | present-tense "2.17.0" / "2.17.0-1" | superseded on host; the measurements remain valid as-of their round, but must not be cited as current |
| `SKILL.md:114` (L1-owned) | "walker 2.17.0 via app-walker@autostart.service" | superseded; L1 owns the file, flagged not edited |

The r17 reports already named this debt (`round-17/w1/reports/CriticC2.md:154-158`,
`round-17/w2/reports/CriticAdmission.md:91,100`); this report supplies the
source-side delta and the exact replacement values.

### 6.2 What r9 keeps without change

- The **reload-mechanism conclusion** ("no reload verb, no D-Bus method, no
  systemd reload path; restart is the apply path") is not contradicted by the
  2.17.0→2.17.2 delta: none of the 7 commits adds a config watcher, CLI
  reload flag, or D-Bus method. The niri watcher is a workspace-focus stream,
  not a config watch, and it starts only when niri flags are enabled.
- r9's safety framing and its classification of config as a one-shot load
  remain usable as history. But r9's **token-census counts and offsets**
  (`§3.3`) are 2.17.0-binary-specific and should be re-derived on 2.17.2
  before being quoted as current; walker execution is forbidden under the
  pause and this seat did not re-derive the binary token census.

### 6.3 New material the route notes can cite (documentary only)

- `[niri]` config exists but is **not a P3 Hyprland route**: it requires a Niri
  IPC session. The host session is Hyprland (`walker-deep-r9.md:12`), so no
  Niri socket is expected; the flags default false and the user overlay sets
  none of them. The walker-side service precondition is met
  (`Exec=walker --gapplication-service`, unchanged autostart bytes), but the
  watcher has no Niri stream to read, so it is inert. Not a P3 route.
- The GTK ≥ 4.24 gate is a real theme-adjacent fact for P5/P3: walker's blur
  region now follows the theme's `.box-wrapper` border-radius, and
  `blur_corner_radius` is inert on this host. Host GTK 4.24.1 is the current
  value (pacman.log:2641).
- The `SimpleDelete` default is a behavior change for the clipboard keybind,
  not a file-format change; it removes the row from the visible model without
  re-querying the provider (possible divergence on provider failure is UNK).

## 7. Unknowns and non-claims

- **UNK:** whether the running walker process restarted onto 2.17.2 after the
  09:16 transaction. No `systemctl`/`pgrep` was run (host pause). `--version`
  bytes, `--help` hashes, D-Bus interface and live layers are not re-measured.
- **UNK:** host executable ↔ upstream release-artifact equality. The official
  2.17.2 tarball is 2,772,997 B (>1 MiB receipt cap), not fetched; only its
  API digest is recorded (§1). The config-file equality is the only exact
  source↔host bridge measured.
- **UNK:** whether the Arch `2.17.2-1` package carries downstream patches that
  alter behavior. No PKGBUILD was fetched (out of seat scope).
- **INF:** the niri keys are inert on this host (code requires service mode +
  niri IPC + enabled flags; host is Hyprland; user overlay sets none). This is
  inference from the fetched source and file bytes, not an observed no-op.
- **INF:** old 2.17.0 user configs remain parseable because the new fields are
  `Option` overrides merged additively in `PartialWalker`; no config migration
  step appears in the diff.
- Release notes are commit-title lists, not exhaustive prose; the 12-file
  compare diff was used as the stronger source. The release bodies and compare
  payload agree on all seven commits.
- Quotes above are ≤25 words each and anchored to the saved body lines; tag
  source never proves the host binary, and no host binary was executed.
- Tooling: nothing installed or upgraded this seat; `curl 8.23.0`, `git`,
  `python3` and coreutils were pre-existing.

## Appendix — re-run recipe (read-only, no host services)

```bash
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/fetch/SrcWalkerChangelog
# tag pins
git ls-remote https://github.com/abenz1267/walker 'refs/tags/v2.17*'
# note bytes (compare with receipts.jsonl)
sha256sum walker-release-v2.17.2.json        # 30e642b0…
sha256sum walker-v2.17.2-resources-config.toml  # 3c5c6867…
# config delta
diff -u walker-v2.17.0-resources-config.toml walker-v2.17.2-resources-config.toml
# host bridge
sha256sum /etc/xdg/walker/config.toml        # 3c5c6867…
sha256sum /usr/bin/walker                    # 25240650…
```
