# DeltaWalkerCli — 2.17.0→2.17.2 changes no CLI flag, no socket code and no default service behaviour; 2.17.0-era CLI/socket/service *claims* survive on source and released bytes, while artifact pins (sha, BuildID, offsets) move and help-output shas are GLib-bound

Seat `MadoR19.DeltaWalkerCli` (wave 1). Question: what changed between walker
v2.17.0 and v2.17.2 in CLI/help, socket and service behaviour, and which 2.17.0-era
claims in `corpus/knowledge/walker-live-surface.md` and `walker-deep-r9.md` are
affected. Method: tag→commit via `ls-remote`, commit-pinned raw fetches with
receipts, a `/tmp` blobless clone for `git log`/`git diff`, and — as a bonus the
upgrade left behind — **byte comparison of both released package binaries**
(`/var/cache/pacman/pkg/walker-2.17.{0,2}-1-x86_64.pkg.tar.zst`). No walker, pacman,
systemctl or busctl execution; host bytes only.

Headline: **the walker-side CLI text is byte-identical between the two released
builds** (838-byte option-description run, sha256 `e429efc3…`, at 2.17.0 offset
819,030 and 2.17.2 offset 832,855). Whether the rendered `--help` *bytes* moved is
not a walker question: GOption's framing lines live in the host GLib/GIO, not in
either walker binary, and the same 2026-10-20 transaction also upgraded
`glib2 2.88.3-1 → 2.90.1-1` (`/var/log/pacman.log:2554`) and
`gtk4 1:4.22.4-1 → 1:4.24.1-1` (`:2641`). `src/data.rs` (elephant socket protocol)
is byte-identical. `src/main.rs` adds one config-gated service feature (niri
workspace launch) and refactors two GTK-rs API calls with unchanged semantics.

---

## §1 Tags, commits, receipts

Tag resolution (`git ls-remote https://github.com/abenz1267/walker …`):

| Tag | Ref | Type | Commit |
|---|---|---|---|
| v2.17.0 | `2a4bde0…` (annotated) | tag object | `42b3ed88abf50bc52638fb2835b7f17e3ea3ac4c` — 2026-07-16 18:06:34 +0200, "bump version" |
| v2.17.1 | — | lightweight | `56c9e2b69e7d2b00f0f9481ae8c89f53810c1de5` — "feat(desktopapps): support new edit action" |
| v2.17.2 | `a515085…` (lightweight) | commit | `a515085fd39fae80acc086c8fbfd9b7771a9a11d` — 2026-10-08 08:45:24 +0200, "fix: GTK 4.24 blur handling causing crash" |

Commits in `42b3ed8..a515085` (newest first):
`a515085` GTK 4.24 blur crash fix (=v2.17.2) · `ebe4ade` updated GTK4 dependencies ·
`d885437` nix flake (#742) · `56c9e2b` desktopapps edit action (=v2.17.1) ·
`dcb4d68` rounded blur region `blur_corner_radius` (#737) · `253f44f` `SimpleDelete`
after action · `c299cd8` niri ipc integration + config.

Fetch receipts: `.ufo/waves/round-19/fetch/DeltaWalkerCli/receipts.jsonl`
(7 lines, 4,537 B, sha256 `82e82c58e7a7962db8e415f33bd0276b4d957a236b34733b88b8a67a256d6715`).
Correction made in place before hand-off: the first write carried a hand-typed `tool`
string that did not match `curl --version`; every line's `tool` field was rewritten to
the real first line (`curl 8.23.0 … zstd/1.5.7 … libssh2/1.11.1 … ngtcp2/1.25.0
nghttp3/1.18.0 mit-krb5/1.22.2`) after re-checking each body's byte count and sha256
against its line. No other field changed.
All fetches HTTP 200, commit-pinned `raw.githubusercontent.com/abenz1267/walker/<commit>/…`
plus `static.crates.io` (see §10). Bodies in the same directory:

| body | bytes | sha256 (prefix) |
|---|---|---|
| `v2.17.0-src_main.rs` | 24,450 | `c258547840491e9c…` |
| `v2.17.2-src_main.rs` | 26,673 | `f09466fecf903cb0…` |
| `v2.17.0-src_data.rs` | 26,338 | `996db119ba61cb15…` |
| `v2.17.2-src_data.rs` | 26,338 | `996db119ba61cb15…` — **identical** |
| `v2.17.0-Cargo.toml` | 908 | `c8d51eb497ad8614…` |
| `v2.17.2-Cargo.toml` | 952 | `d1676045d1101a2d…` |

## §2 Release delta (12 files, +977/−250)

```text
$ git -C /tmp/dw19/walker diff --stat 42b3ed8 a515085     # output condensed onto 4 lines
 Cargo.lock | 539 ++++----  Cargo.toml | 10 +-  README.md | 16 ++  flake.lock | 12 +-
 resources/config.toml | 9 +  src/config.rs | 44 ++  src/keybinds.rs | 1 +
 src/main.rs | 93 +-  src/niri.rs | 399 ++++++++ (new)  src/state/mod.rs | 9 +
 src/ui/window.rs | 64 +-  src/wayland_blur.rs | 31 +-
 12 files changed, 977 insertions(+), 250 deletions(-)
```

`src/data.rs`, all `src/protos/*` and every provider module are **not** in the
diffstat — the elephant query/activate wire protocol is untouched.

`Cargo.toml`: `version 2.17.0→2.17.2`; `gtk4 ^0.9.7→^0.11.5`; `gtk4-layer-shell
0.5.0→0.8.1`; `gdk4-wayland ^0.9→^0.11.5`; **new** `glib-unix = "0.22"`;
**new** `niri-ipc = "=26.4.0"`; `xdg = "3.0.0"` unchanged
(`.ufo/…/fetch/DeltaWalkerCli/v2.17.2-Cargo.toml:7-10,30,32`).
Resolved in `Cargo.lock`: `glib 0.20.12/0.21.5 → 0.21.5/0.22.10`, `gtk4 0.9.7 → 0.11.5`,
`xdg 3.0.0 → 3.0.0` (same).

`resources/config.toml` gains `blur_corner_radius = 20`, a `[niri]` table
(`launch_on_empty_workspace`, `launch_on_startup`, `cmd_on_esc`), a
desktopapps `{ action = "edit", bind = "ctrl e" }` row, and switches the clipboard
`remove` row to `after = "SimpleDelete"`.

## §3 CLI surface: unchanged in source and in the released bytes

1. **Flag set identical.** `fn add_flags` bodies are byte-identical across the two
   tags (`diff <(sed -n '/^fn add_flags/,/^}/p' v0/main.rs) <(… v2/main.rs)` → no
   output). Both register **23** application options
   (`grep -c 'app.add_main_option'` over the function → 23 / 23), in the same order:
   `version, nosearch, nohints, inputonly, password, selectsingle, index, provider,
   set, placeholder, height, minheight, maxheight, current, width, minwidth,
   maxwidth, theme, dmenu, close, hideqa, keepopen, exit`.
2. **Released-binary proof.** The concatenated run from the first description
   `show version` through the last `exit after this dmenu call. only when using
   service. dmenu only` is **838 bytes with the same sha256 in both package builds**:

   ```text
   2.17.0: [819030,819868) sha256 e429efc3bc96c328d284d3d0583e48c5beb3ac7001f0e8f599afa8de26d25c75
   2.17.2: [832855,833693) sha256 e429efc3bc96c328d284d3d0583e48c5beb3ac7001f0e8f599afa8de26d25c75
   DESC RUN BYTE-IDENTICAL: True
   ```
3. **`--version`**: the print path is unchanged
   (`v2.17.2-src_main.rs:86-92`, `v2.17.0-src_main.rs:80-86`:
   `connect_handle_local_options` → `println!("{}", env!("CARGO_PKG_VERSION"))`); only
   the GTK-rs return type moved from `0`/`-1` to
   `ControlFlow::Break(ExitCode::SUCCESS)`/`Continue(())` — same semantics. The
   literal changes: `version2.17.2\n` at offset 856,302; `2.17.0` occurs **0** times in
   the 2.17.2 binary and `2.17.2` occurs 0 times in the 2.17.0 binary.
4. **No new/removed CLI gate.** The pre-GTK argv checks in `fn startup`
   (`v2.17.2-src_main.rs:778-804` vs `v2.17.0-src_main.rs:771-797`: dmenu,
   `--version` early return, `-q/--close` → `process::exit(0)` when not a service,
   service fallback message) are identical text; the only added line in that function
   is `listen_niri_workspaces(app.clone())` (`v2.17.2-src_main.rs:812`).
5. **No `--config`, no reload verb** — still true: `add_flags` identical and the
   description run contains no `config`/`reload`/`watch` token (§8 row `:157-161`).
6. **dmenu exit code** on cancel: `cmd.set_exit_status(130)` →
   `cmd.set_exit_code(130.into())` (`v2.17.2-src_main.rs:608,614`) — same 130.

## §4 Socket behaviour: path and semantics unchanged; the UNK is closable from source

Path construction `v2.17.2-src_main.rs:872-886` is character-identical to
`v2.17.0-src_main.rs:807-821`: `XDG_RUNTIME_DIR` (fallback `env::temp_dir()`) →
`walker` dir → `walker.sock`, `remove_file` then `UnixListener::bind`.

Accept handler `v2.17.2-src_main.rs:891-918` (`v2.17.0-src_main.rs:826-853`): `listener.accept()` → `drop(stream)` (`:895`) →
reset width/height/min/max/`is_dmenu`/`keepopen`/`param_close`/`hide_qa`/provider →
`activate()`. **The connection payload is never read**: the connection itself is the
message. `README.md:179-185` at both tags documents the call
(`nc -U /run/user/1000/walker/walker.sock`) and states "it does not handle any
commandline options". This resolves `walker-live-surface.md:227` (unknown #3,
"`walker.sock` protocol / query API") as **no query API, activation-only**, valid at
both tags because the code is unchanged. Only the intra-crate helper moved
(`glib::unix_fd_add_local` → `glib_unix::unix_fd_add_local`).

Live socket state today (stat only): both sockets `755 0`, mtime
`2026-10-20 09:57:13.737056297 -0300` (walker) / `.715056299` (elephant) — later
than both post-upgrade restart-hook lines (`pacman.log:3062` 09:18:25, `:3123`
09:31:04); the cause of the 09:57 bind is `[UNK]`. Shape claim holds; the round-7/9
mtime and PID pins are dated.

## §5 Service behaviour: one new config-gated feature, nothing default-on

- `--gapplication-service` is still GIO's flag (its help string lives in
  `libgio-2.0.so.0`, §9.1); walker's `ApplicationFlags::IS_SERVICE` checks are the
  same four as 2.17.0 — `init_ui` (`v2.17.2-src_main.rs:104`), `keepopen` (`:505`),
  the non-service `--close` exit (`:782`), the fallback message (`:802`) — plus one
  new check in the niri path (`:823`).
- **New** `fn listen_niri_workspaces` (`v2.17.2-src_main.rs:815-870`): returns
  immediately unless `[niri].launch_on_empty_workspace|launch_on_startup` is true;
  otherwise requires service mode, else prints
  `niri workspace launch requires walker to run as a service` and returns. It spawns
  a thread over `UnixStream::pair()` and watches it with
  `glib_unix::unix_fd_add_local`; a readable event calls
  `set_is_auto_launched(true); activate(&app)`.
- **New** `cmd_on_esc` (`src/ui/window.rs` at `a515085`, `fn
  run_auto_launch_escape_command` line 746): runs `sh -c <cmd>` only when
  `key == Escape && is_auto_launched()` and the config string is non-empty; also
  wired to the window-close action. `handle_command_line` clears the flag
  (`v2.17.2-src_main.rs:407`), so an ordinary invocation never runs it.
- Packaged defaults for `[niri]` are all `false`/empty
  (`/etc/xdg/walker/config.toml:24-27`), so **stock service behaviour is unchanged**.
- `ext_background_effect_blur` is now gated on `gtk4::minor_version() < 24`
  (`src/ui/window.rs:361` at `a515085`) — the GTK 4.24 crash fix; `src/wayland_blur.rs`
  adds the `blur_corner_radius` region radius. This host moved to `gtk4 1:4.24.1-1`
  in the same transaction (`pacman.log:2641`), so on this host the walker-side blur
  request path is now skipped whenever that option is enabled; it is `false` in the
  packaged default (`/etc/xdg/walker/config.toml:21`) and absent from the user file
  (`grep -n ext_background_effect_blur ~/.config/walker/config.toml` → no match, rc 1)
  — `[INFERENCE]` from source, not exercised.
- `SimpleDelete` is a new `AfterAction` variant (`src/keybinds.rs`) and a new
  clipboard default row; the old `AsyncClearReload` row is replaced.

## §6 Artifact pins moved (what a re-pin must carry)

| Fact | 2.17.0 (cache pkg verified) | 2.17.2 (installed + cache pkg, `cmp` equal) |
|---|---|---|
| package | `walker 2.17.0-1` | `walker 2.17.2-1` (pacman.log:2929) |
| binary sha256 | `64826a8531eac525adfa3eff65548e93a6f7714feb1d3e13b4fa35bbcc3cfda0` | `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096` |
| size | 6,661,264 | 7,039,912 |
| BuildID | `a22452d1e4243bad1bf9fd487aa569f673ad9c5a` | `19200fe47eb6c90fc4956f0d52d0c7c84bb89e99` |
| `.comment` | GCC 16.1.1 20260430 / rustc 1.97.1 / LLD 22.1.8 | GCC 16.2.1 20260810 / rustc 1.99.0 / LLD 23.1.1 |
| entry point | `0x190420` | `0x1a3110` (12 phdrs / 35 shdrs / shstrtab 34 unchanged) |
| version literal | 847,791 (`version2.17.0\n`) | 856,302 (`version2.17.2\n`) |
| embedded default config | 784,064, = packaged 13,220 B `5b4e47b7…` | 806,960, = packaged 13,743 B `3c5c6867…` |
| packaged `/etc/xdg/walker/config.toml` | 13,220 B `5b4e47b7…` | 13,743 B `3c5c6867…` (== on-disk, `cmp` clean) |
| `WALKER_` literal | 797,295 (after `config.toml` @797,284) | 820,714 (after `config.toml` @820,703) |
| socket token | `XDG_RUNTIME_DIRwalkerwalker.sock` @818,871 | same token @832,681 |
| option-description run | 819,030, 838 B `e429efc3…` | 832,855, 838 B `e429efc3…` |
| package entries | 29 (10 dirs + 19 files), no man/doc | 29 (10 dirs + 19 files), no man/doc |

Package-cache finding worth carrying: **the 2.17.0 artifact is still on disk** —
`/var/cache/pacman/pkg/walker-2.17.0-1-x86_64.pkg.tar.zst` extracts to a binary whose
sha256 is exactly `64826a85…` and a config whose sha256 is exactly `5b4e47b7…`. The
round-7/9 pins were therefore re-provable after the upgrade; the sibling note
`HostWalkerBytes.md` states the old binary is "not present on disk" — it is present
in the package cache.

The "rodata cluster" the round-7 note anchors at "≈818,871" is the head of one
contiguous run, not the description blob: at 818,871 starts
`XDG_RUNTIME_DIRwalkerwalker.sock`, followed by
`org.gnome.desktop.interfacecolor-schemesettings-schemaaccent-color`,
`make sure 'walker --gapplication-service' is running!\nversion`, and then
`show version…` at 819,030 (159 B after the socket token). In 2.17.2 the same run
has `dev.benz.walker` inserted right after `walker.sock` (@832,713), so the distance
grows to 174 B (+15 = `len("dev.benz.walker")`). In 2.17.0 the app id is not a
rodata string at all: it is built from `movabs` immediates `dev.benz` / `z.walker`
at file offset 2,163,434, inside `.text` (file range 1,635,360–6,455,232 per
`readelf -SW`); in 2.17.2 it is a `.rodata` literal (`.rodata` file range
747,776–1,224,531). A byte census for `dev.benz.walker` therefore reads 0 on the
2.17.0 build and 1 on the 2.17.2 build — a codegen change, not an app-id change
(`application_id("dev.benz.walker")` at `v2.17.0-src_main.rs:76` and
`v2.17.2-src_main.rs:82`).

## §7 Claim map — `corpus/knowledge/walker-live-surface.md`

Verdicts: **UNAFFECTED** = still true of 2.17.2; **MOVED** = value/pin changes,
statement as written is stale; **SHARPENED** = substance survives, wording needs the
note below; **UNMEASURED** = cannot re-check under the host pause.

| Note line | 2.17.0-era claim (abridged) | Verdict | Basis |
|---|---|---|---|
| 19-24 | host walker 2.17.0; help family + `--version` state-free; help recoverable from binary | MOVED (version) + SHARPENED | 2.17.2 per pacman.log:2929 / binary literal 856,302; state-free property is source-level unchanged, not re-executed |
| 37 | binary sha `64826a85…`, pkg `2.17.0-1` | MOVED | §6 row |
| 38 | `--version` = `2.17.0\n` (7 B) | MOVED | literal `2.17.2\n` @856,302; print path `v2.17.2-src_main.rs:86-92` = `v2.17.0-src_main.rs:80-86` (return type only) |
| 39-42 | PID/unit/elephant PID pins | UNMEASURED | restart hooks ran (pacman.log:3062, 3123); no process/systemd probe |
| 43 | 29 package entries, no man page/doc | UNAFFECTED | manifest `walker-2.17.2-1/files`: 10 dirs + 19 files incl. `usr/bin/walker`, no `man`/`doc` |
| 44-47 | running argv equals the documented `--gapplication-service` | UNAFFECTED | flag meaning and `startup()` unchanged |
| 51-55 | `--help` 1,726 B, sha `ca4820a8…`, 33 L, 26 option lines | UNMEASURED (bytes) / UNAFFECTED (counts, walker side) | 23 option registrations both; walker strings identical; framing comes from GLib, which moved 2.88.3→2.90.1 (`pacman.log:2554`) — the sha is stale by construction, its new value `[UNK]` (§9.1) |
| 56-88 | verbatim option text block | UNAFFECTED | 838-byte run identical (§3.2) |
| 91-94 | `--help-all` 1,867 B `b513c43f…`; `--help-gapplication` 144 B `0945536c…` | UNMEASURED (GLib-owned bytes) | `Show all help options` / `Enter GApplication service mode…` occur 0× in both walker binaries, 1× in host `libglib`/`libgio` 2.90.1 (§9.1) |
| 95-97 | no `--config` option exists | UNAFFECTED | `add_flags` byte-identical; no config flag in 23-name list |
| 98-103 | help "compiled into the binary as one concatenated blob" (≈818,871) | SHARPENED | true for the 23 descriptions (compiled, stable); false for framing/help-option lines, which are runtime GLib; 818,871 is the socket token, blob starts 819,030 (§6) |
| 104-105 | `-q`, `-e`, `-d` are mutating/fenced | UNAFFECTED | argv checks identical (`v2.17.2-src_main.rs:778-804` = `v2.17.0-src_main.rs:771-797`); `close`/`exit`/`dmenu` registrations identical |
| 113 | L0 embedded default @784,064 equals packaged | MOVED (offset) / UNAFFECTED (mechanism) | @806,960 equals the 13,743 B packaged file verbatim |
| 114 | L1 packaged 13,220 B `5b4e47b7…` | MOVED | 13,743 B `3c5c6867…` |
| 115 | L2 user `fecf71fa…`, 1,336 B | UNAFFECTED | re-read today: same sha and size |
| 130-137 | one `WALKER_` literal adjacent to `config.toml`, no `WALKER_<NAME>`; quoted run `config.tomlWALKER_called …` | UNAFFECTED (substance) / MOVED (quoted run) | 2.17.2: `config.toml`@820,703, `WALKER_`@820,714, count 1 each; the only `WALKER_[A-Za-z0-9_]*` match is now `WALKER_config` because `config not initialized` follows at 820,721 (2.17.0: `WALKER_called`, `config not initialized`@797,345) — still a rodata boundary artifact, not a variable name |
| 138-143 | XDG env token census | UNAFFECTED (in kind) | `XDG_DATA_HOME`/`XDG_CONFIG_HOME` 1× each, `XDG_RUNTIME_DIR` 3× in 2.17.2 |
| 147-152 | GSettings tokens (`org.gnome.desktop.interface`, `color-scheme`, `accent-color`) | UNAFFECTED | present in 2.17.2: 1 / 2 / 2 |
| 164-167 | socket mode·size·mtime | UNAFFECTED (shape) / MOVED (mtime) | `755 0`, mtime 2026-10-20 09:57:13 |
| 169-174 | socket path = runtime dir + `walker` + `walker.sock` | UNAFFECTED | `v2.17.2-src_main.rs:872-886` = `v2.17.0-src_main.rs:807-821`; token @832,681 |
| 178-193 | D-Bus name `dev.benz.walker`, interface set, `Actions.List` empty | UNAFFECTED (identity) / UNMEASURED (introspection) | `application_id("dev.benz.walker")` at `v2.17.2-src_main.rs:82` = `v2.17.0-src_main.rs:76`; no D-Bus code in the diff; busctl not run (host pause) |
| 195-200 | no walker namespace in layer list | UNMEASURED | `hyprctl` barred |
| 202-205 | service-mode fallback message token | UNAFFECTED | 2.17.2 @832,794, count 1 |
| 212-234 | §10/§11 ledger incl. unknown 3 (`walker.sock` protocol UNK) and 5 (`WALKER_`) | SHARPENED (3) / UNAFFECTED (5) | unknown 3 is now answerable from source (§4) |
| 246-262 | §6 spot-check recipes | MOVED (pins) | every offset/sha recipe needs the §6 table values |
| 270-279 | §7 boundary proof | historical | — |
| 292-300 | §8 unknowns, incl. #5 "help blob stability across rebuilds" | SHARPENED | cross-build question is now answered for the description run: identical across two builds with different rustc/GTK (1.97.1→1.99.0, gtk4 0.9.7→0.11.5) |
| 305-307 | round-19 freshness pointer (already appended) | UNAFFECTED | carries `2.17.2` + `S090`/`S096` on the same lines |

## §8 Claim map — `corpus/knowledge/walker-deep-r9.md`

| Note line | Claim (abridged) | Verdict | Basis |
|---|---|---|---|
| 30 | 2.17.0 build-identity claim | MOVED | §6 |
| 58 | `--version` = `2.17.0\n` | MOVED | §6 |
| 59 | three help-family sha256 pins | UNMEASURED (stale by construction) | rendered bytes = walker strings (identical, §3.2) + GLib/GIO framing; GLib moved 2.88.3→2.90.1 in the same transaction (`pacman.log:2554`); new values `[UNK]` without a run (§9.1) |
| 60 | package row `2.17.0-1`, `pacman -Qkk` 29/0 altered | MOVED | 2.17.2-1; manifest still 29 entries; `gzip -dc …/walker-2.17.2-1/mtree` → `./usr/bin/walker … size=7039912 sha256digest=25240650…` = on-disk binary (`-Qkk` itself not run) |
| 69, 291 | embedded-config offset 784,064 reproduces | MOVED | 806,960 |
| 78-85 | bare-semver shape; 26 help lines = 3 + 23; no subcommands; only service flag | UNAFFECTED (walker side) | 23 registrations both, same order; `--gapplication-service` is GIO's (string in `libgio`), unchanged by walker; the 3 help-option lines and `[OPTION…]` framing are GLib's (§9.1) |
| 93-99 | ELF shape table incl. BuildID `a22452d1…`, `.comment` toolchain | MOVED | 2.17.0 values re-verified on the cache-package binary (`readelf -n`/`-p .comment`); 2.17.2: BuildID `19200fe4…`, GCC 16.2.1 20260810 / rustc 1.99.0 / LLD 23.1.1 (single GCC line, not two); entry `0x1a3110`; 12 phdrs / 35 shdrs unchanged |
| 102-105 | identity chain printed→literal→sha→BuildID→pkg | UNAFFECTED (method) / MOVED (values) | — |
| 109-116 | version literal provenance @847,791 | MOVED | 856,302; same `…version2.17.2\n…` shape |
| 157-161 | help has no `config` / `reload` / `restart` / `watch` hits | UNAFFECTED | `add_flags` identical; run token-free |
| 166-184 | token census (inotify/watch/notify/restart/reload/Reload/refresh…) | UNAFFECTED in kind, MOVED in counts | 2.17.2: `inotify` 0, `(?i)watch` 0, `watcher` 0, `(?i)notif` 3 (MIME, as before), `restart` 0, `reload` 1, `Reload` 51, `refresh` 12 (2.17.0: 0/0/0/3/0/1/52/7); offsets all move |
| 186-191 | no hot-reload machinery ⇒ no config watch | UNAFFECTED | true, and the new niri event stream is workspace focus, not config: `v2.17.2-src_main.rs:815-870`, `src/niri.rs` |
| 193-200 | one-shot load/set design | UNAFFECTED | `src/config.rs` diff only adds merge arms for `[niri]`/`blur_corner_radius` |
| 3.5 (`:204-220`) | no D-Bus/systemd reload path | UNAFFECTED (source) / UNMEASURED (live) | no new methods in diff; unit file is generator-owned and unchanged; systemctl not run |
| 3.6 (`:221-233`) | operator apply path = service restart | UNAFFECTED | `~/.local/share/omarchy/bin/omarchy-restart-walker` present, sha256 `9ac82d0c1370ec19f59c8347716036765d3335d348feaec4c9581e2ca3bf8174` (note pins no hash) |
| 3.7 (`:234-258`) | broken-config `--help` probe | MOVED (version-bound) | not re-runnable under host pause |
| 3.8 (`:259-282`) | read-once verdict (INF high) | UNAFFECTED | `src/config.rs` still one-shot; no watcher tokens |
| 305-317 | §5 spot-check recipes | MOVED (pins) | §6 table |
| 403-405 | round-19 freshness pointer (already appended) | UNAFFECTED | `2.17.2` + `S090`/`S096` on the same lines |

## §9 Three substantive corrections the notes should absorb

1. **Help bytes are not a walker-binary property.** Raw `bytes.count` over both walker
   binaries: `Usage:`, `[OPTION`, `Help Options:`, `Show help options`,
   `Show all help options`, `Show GApplication options`,
   `Enter GApplication service mode (use from D-Bus service files)` → **0×** in 2.17.0
   and 2.17.2. The same census over the host libraries (file bytes):
   `/usr/lib/libglib-2.0.so.0.9000.1` carries `Usage:` 2, `[OPTION` 2,
   `Help Options:` 2, `Show help options` 2, `Show all help options` 1;
   `/usr/lib/libgio-2.0.so.0.9000.1` carries `Show GApplication options` 1 and
   `Enter GApplication service mode (use from D-Bus service files)` 1. So
   `--help`/`--help-all`/`--help-gapplication` sha256 pins are a property of
   *(walker strings, host GLib/GIO, locale)*. The walker half did not move; the GLib
   half did (`glib2 2.88.3-1 → 2.90.1-1`, `pacman.log:2554`, same transaction as
   walker `:2929`). Whether 2.90.1 renders different bytes is `[UNK]` without a run.
   The invariants worth pinning are the 838-byte description run and the 23-count.
2. **The socket question is closed.** `walker.sock` is an activation doorbell: the
   accepted stream is dropped unread and the request state is reset
   (`v2.17.2-src_main.rs:891-918`, identical except the `glib_unix::` path at 2.17.0
   `:826-853`). Keep the residual
   UNK only for *who connects and with what payload* (e.g. omarchy helpers), not for
   "is there a query protocol".
3. **Cross-build help stability is now measured once.** The 838-byte description run
   is byte-identical across 2.17.0 and 2.17.2 despite a rustc 1.97.1→1.99.0 and
   gtk4 0.9.7→0.11.5 rebuild, so `walker-live-surface.md:300` (unknown §8.5) and
   `walker-deep-r9.md` §2.4.1 (`:119-128`) can be narrowed from "untested" to "stable across these
   two builds; still not proven for arbitrary rebuilds".

## §10 Support for the reserved SOURCES ids

- **S096 (host walker bytes)** — add the 2.17.2 values in §6 and, importantly, the
  fact that the *2.17.0* artifact is still available at
  `/var/cache/pacman/pkg/walker-2.17.0-1-x86_64.pkg.tar.zst` (binary sha `64826a85…`,
  config sha `5b4e47b7…`), so old pins are verifiable rather than merely inherited.
- **S097 (superseding row for S094)** — the receipts file is the anchor shape to
  cite: commit-pinned `raw.githubusercontent.com/.../<40-hex-commit>/...` URLs with
  per-body sha256 (`receipts.jsonl` sha256 `82e82c58…`), no HTML/API page, no
  `latest` alias. The two `src_data.rs` bodies are byte-identical
  (`996db119…`), which is exactly the kind of claim a per-fetch HTML digest cannot
  support.
- **S098 (xdg crate tarball replacing S084's `latest` support)** — version is pinned
  twice: requirement `xdg = "3.0.0"` at `v2.17.0-Cargo.toml:29` and
  `v2.17.2-Cargo.toml:30`, resolved `name = "xdg" version = "3.0.0"` in **both**
  `Cargo.lock`s. Tarball fetched for the row:
  `https://static.crates.io/crates/xdg/xdg-3.0.0.crate` → HTTP 200, 15,821 B,
  sha256 `2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5`
  (body `xdg-3.0.0.crate` in this seat's fetch dir, receipt line 7). **Independent
  check:** that sha256 equals the registry `checksum` recorded for `xdg 3.0.0` in
  walker's `Cargo.lock` at both tags (`42b3ed8:Cargo.lock:2595`,
  `a515085:Cargo.lock:2708`), so the row's digest is anchored by the tag-pinned
  lockfile as well as by this fetch.

## Limits

- Walked only the surfaces the question names: `src/main.rs`, `src/data.rs`,
  `Cargo.toml` (+ repo-wide `--stat`/`--name-only`/`Cargo.lock` greps at both tags).
  `src/niri.rs` (399 new lines) was not read in full — only its call sites and the
  generated strings were checked; its IPC details are `[UNK]` beyond "workspace-focus
  event stream, gated by `[niri]` config + service mode".
- No walker execution, no `--help`/`--version` run: rendered help/version bytes for
  2.17.2 are `[INFERENCE]` from source + rodata, not observed. Host GLib/GTK moves
  were read from `/var/log/pacman.log` lines 1439, 2554, 2641 only; GLib 2.88.3 vs
  2.90.1 GOption formatting was not compared (no GLib source fetched).
- No pacman/systemctl/journalctl/busctl/hyprctl/pgrep; no `/proc` read; no socket
  connect. Process/unit/D-Bus rows are UNMEASURED, not refuted.
- Upstream issues, PR bodies and release notes were not fetched — the delta is
  characterised from tag-pinned source + released binaries only.
- Scratch `/tmp/dw19` (blobless clone at `a515085`, extracted package binaries) was
  removed after the run; recreate with
  `git clone --filter=blob:none https://github.com/abenz1267/walker` and
  `tar --zstd -xf /var/cache/pacman/pkg/walker-2.17.{0,2}-1-x86_64.pkg.tar.zst usr/bin/walker etc/xdg/walker/config.toml`.
  No git or jj command ran inside the lane; only lane write = this report plus the
  seat's own `fetch/DeltaWalkerCli/` bodies and `receipts.jsonl`.
- Package→tag attribution is `[INFERENCE]`: tag commit 2026-10-08 06:45Z precedes the
  package build date 2026-10-08 14:14Z and the literal matches, but the PKGBUILD was
  not read (no packaging source fetched).
- Peer report `HostWalkerBytes.md` predates this seat; its "old binary not on disk"
  limit is superseded by the package-cache finding in §6, not by disagreement on any
  measured value.

## Installs

none.
