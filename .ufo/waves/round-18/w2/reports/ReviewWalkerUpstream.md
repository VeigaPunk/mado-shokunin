# ReviewWalkerUpstream — § Upstream contract spot-check (walker-route-r18)

Seat `MadoR18.ReviewWalkerUpstream` (wave 2 = FALSIFY, leaf). Reviewed
`corpus/knowledge/walker-route-r18.md` § Upstream contract, note lines 46-172,
at integration commit `4c103b55b1ea5c3c555884afe3eb69b5189701b7`. Note blob
sha256 `3ff430a4627d4204ff14c1e9e92eb726a38244ad8c27d8bda412243dfb8fbf20`
(321 lines), byte-equal in the worktree and identical at receipts commit
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f` (`git ls-tree` blob
`c2056f3fc11ddb3ebfcc58c7d83203dd7dd91c09` at both revisions).

Scope: 12 anchored claims sampled across S072-S089, each checked against
re-fetched tag-pinned bodies whose sha256 I compared with the committed
`mado-fetch-receipt-v1` lines. No runtime observation, no host process, no
socket, no package query; host bytes read only for the stock-config equality
in C12. Verdict summary: **11 agree; C8 agrees on substance but its literal
"only" enumeration is false** (detail below). No claim in the section is
contradicted by its own anchored bytes. 18/18 rows S072-S089 are covered by
the 12 claims; all 72 bracket citations in the section (`[WR:…]` …
`[OD:…]`) were resolved to body ranges and read.

## Method (exact commands and observed output)

1. **Revision identity.** `git show 4c103b5:corpus/knowledge/walker-route-r18.md | sha256sum`
   → `3ff430a4…fbf20`, equal to `sha256sum corpus/knowledge/walker-route-r18.md`;
   321 lines. `git ls-tree 4c103b5` and `abfbf35` both list the same note blob
   and the same SOURCES blob `2b8dd7c0…`.

2. **What is committed.** `git ls-tree -r --name-only 4c103b5 -- .ufo/waves/round-18/fetch`
   → 21 paths, all `receipts.jsonl` (one per seat). The fetched bodies are
   **untracked** at both revisions; only the receipts + digests are committed.
   `git show 4c103b5:…/NoteWalker/receipts.jsonl | sha256sum` →
   `a244ddc1…`, equal to the worktree file; 27 receipt lines.
   Local bodies vs committed receipts (python re-hash of every `body`):
   `receipts 27 mismatches 0`.

3. **Independent re-fetch.** 19 URLs fetched with
   `curl -sSL --max-time 60 -o <body> -w '%{http_code} %{url_effective}' URL`
   into `.ufo/waves/round-18/fetch/ReviewWalkerUpstream/`, one receipt per body
   appended to its `receipts.jsonl`. All 19 returned `200` and the same final
   URL; every body's sha256 and byte count equal the corresponding NoteWalker
   receipt (0 disagreements). Bodies: walker v2.17.2 `README.md` 7,926 B
   `9755f955…`; `resources/config.toml` 13,743 B `3c5c6867…`; `src/config.rs`
   19,675 B `93b6bd6f…`; `src/main.rs` 26,673 B `f09466fe…`; `src/data.rs`
   26,338 B `996db119…`; `src/theme/mod.rs` 9,364 B `93287a1c…`; `Cargo.toml`
   952 B `d1676045…`; elephant v2.22.1 `README.md` 6,969 B `aa19a7e2…`;
   `internal/comm/comm.go` 2,552 B `2b4a6f14…`; `cmd/elephant/elephant.go`
   9,283 B `c1c2ecaa…`; `pkg/common/config.go` 3,609 B `46ed4755…`; omarchy
   v3.8.4 `bin/omarchy-launch-walker` 412 B `fd9e93f8…`,
   `bin/omarchy-restart-walker` 709 B `9ac82d0c…`,
   `bin/omarchy-refresh-walker` 893 B `05cd9c67…`,
   `config/walker/config.toml` 1,336 B `fecf71fa…`,
   `default/walker/walker.desktop` 138 B `5cb9874e…`,
   `default/walker/restart.conf` 38 B `de0f7029…`; docs.rs
   `xdg/latest/struct.BaseDirectories.html` 105,537 B `0291cfe6…`; walker tag
   tarball 165,438 B `e50c6060…`. One extra fetch, `pkg/common/files.go`
   1,348 B `19492c24…`, to adjudicate C11.

4. **Line reads.** `nl -ba <body> | sed -n '<ranges>'` on each body; exact
   ranges and output summarized per claim. `tar -xzf walker-2.17.2-src.tar.gz
   -C /tmp/rwu-walker` for the whole-tree searches; scratch tree only.

5. **Docs version.** `grep -o '<title>[^<]*</title>' …` →
   `<title>BaseDirectories in xdg - Rust</title>`; page contains `xdg 3.0.0`;
   walker `Cargo.toml:30` declares `xdg = "3.0.0"`.

## Claims (12)

### C1 — S072 walker README: needs, start, client forms, config location: AGREE
Note lines 50-68. Anchors `[WR:3, 59, 167-171, 173-177, 179-182, 185, 213, 215]`.
- `WR:3` — “A fast, customizable application launcher built with GTK4 and Rust, designed for Linux desktop environments.” (contains the quoted phrase).
- `WR:59` — “- make sure [elephant](https://github.com/abenz1267/elephant) is running before starting Walker”.
- `WR:167` — “In order to improve startup performance, run a Walker service with:”; `169-171` fenced `walker --gapplication-service`.
- `WR:173-177` — “If the service is running, you can either open Walker with: `walker`”.
- `WR:179-182` — “or for an even faster launch make a socket call … `nc -U /run/user/1000/walker/walker.sock`”; `WR:185` — “it does not handle any commandline options”.
- `WR:213` — “Configuration should be done in `~/.config/walker`.”; `WR:215` — “Check out the [default config](…)”.
Verdict: every clause agrees. Caveat (F8): the `WR:215` link targets `refs/heads/master`, not the tag; the note does not claim its content, so no claim is affected.

### C2 — S073 packaged default config: AGREE
Note lines 109-117. Anchors `[WC:2, 4, 6, 9, 18, 37-38, 58-66, 67, 75-113]`.
- `WC:2` `close_when_open = true`; `WC:4` `as_window = false`; `WC:6` `selection_wrap = false`; `WC:9` `theme = "default"`; `WC:18` `resume_last_query = false`.
- `WC:37-38` `[columns]` / `"symbols" = 3`.
- `WC:58-64` `[providers] default = ["desktopapplications", "calc", # "runner", "websearch",]`; `WC:65` `empty`; `WC:66` `ignore_preview`.
- `WC:67` `max_results = 50`.
- `WC:75-113` exactly ten `[[providers.prefixes]]` entries: `;`→providerlist, `>`→runner, `/`→files, `.`→symbols, `!`→todo, `%`→bookmarks, `=`→calc, `@`→websearch, `:`→clipboard, `$`→windows.
Verdict: all ten mappings and every scalar agree; file is 13,743 B sha `3c5c6867…`, equal to the S073 row and to host `/etc/xdg/walker/config.toml` (`sha256sum` → `3c5c6867…`).

### C3 — S074 load order + S084 xdg search order: AGREE
Note lines 71-81. Anchors `[WS:7, 8, 212-216, 218-219, 221-223, 225-231, 234-239, 235, 238, 586-589, 592-594]`, `[WM:108]`, `[XD:302, 306, 356-358]`.
- `WS:7` `static LOADED_CONFIG: OnceLock<Walker>`; `WS:8` `const DEFAULT_CONFIG: &str = include_str!("../resources/config.toml");`.
- `WS:212-216` builder from `DEFAULT_CONFIG` then `try_deserialize` into `Walker`; `WS:218-219` `xdg::BaseDirectories::with_prefix("walker").find_config_file("config.toml")`.
- `WS:221-223` `.build()?` (error propagates); `WS:225-231` `try_deserialize` error → `set_error(...)` + `println!`, defaults kept.
- `WS:234-239` `config::Environment::with_prefix("WALKER").separator("_")`, applied only inside `if let Ok(partial) = …::<PartialWalker>()`; `WS:245` `fn merge(&mut self, partial: PartialWalker)`.
- `WS:586-589` `LOADED_CONFIG.set(Walker::new()?).map_err(|_| "Failed to set loaded config".into())`; `WS:592-594` `get_config()` `.expect("config not initialized")`. `WM:108` `config::load().unwrap();`.
- `XD:302` XDG_CONFIG_HOME default `$HOME/.config`; `XD:306` XDG_CONFIG_DIRS default `/etc/xdg`; `XD:356-358` “Searches `XDG_CONFIG_HOME` and then `XDG_CONFIG_DIRS`.” Page title/version: xdg 3.0.0; `WK:30` `xdg = "3.0.0"` — the unversioned `latest` URL currently serves the declared crate version, and its digest still matches the committed receipt.
Verdict: agree. Residual risk (F6): S084 is the only row in S072-S089 not tag-pinned; its digest can move when a newer xdg release becomes `latest`.

### C4 — S075 main.rs startup, service, close, elephant gate: AGREE (two precision notes)
Note lines 50-68. Anchors `[WM:104-105, 108, 124-126, 635-642, 670-674, 782, 784-786, 802-803, 872-882]` (all but 872-882 are cited in the section; 872-882 is the row's socket anchor).
- `WM:104-105` `if app.flags().contains(ApplicationFlags::IS_SERVICE) { set_is_service(true); }`; `WM:782` recomputes the same flag.
- `WM:108` `config::load().unwrap();`.
- `WM:124-126` `if !dmenu || is_service() { elephant = which("elephant").is_ok(); … }`.
- `WM:670-674` `else if !has_elephant() && !is_dmenu() { println!("Please install elephant."); process::exit(1); }`.
- `WM:784-786` `if !is_service && (args.contains("--close") || args.contains("-q")) { process::exit(0); }`.
- `WM:802-803` `if !app.flags().contains(ApplicationFlags::IS_SERVICE) && !dmenu { println!("make sure 'walker --gapplication-service' is running!"); }`.
- `WM:872-882` `XDG_RUNTIME_DIR` / `env::temp_dir()`, then `walker` + `walker.sock` (S075 row claim).
Verdict: agree. F3: the sentence “when visible and `close_when_open` is set the activation closes it [WM:635-642]” omits the guards visible at `WM:635-639` (`!is_stay_open_explicit_provider`, `&& !is_dmenu_keep_open()`, `|| is_param_close()`); the anchor shows the exceptions, the prose does not. F4: “without a running service” at `WM:802-803` is not in the anchored condition — the code tests only `!IS_SERVICE && !dmenu`; the qualifier is an inference from GApplication `HANDLES_COMMAND_LINE` behaviour (`WM:83,96`), not shown at 802-803. Neither note makes the claim false against the body.

### C5 — S076 data.rs elephant socket and reconnect: AGREE
Note lines 128-137. Anchors `[WD:156-161, 169, 653-660]`.
- `WD:156-161` `env::var("XDG_RUNTIME_DIR").map(PathBuf::from).unwrap_or_else(|_| env::temp_dir())`, then `push("elephant")`, `push("elephant.sock")`.
- `WD:163-164` `wait_for_file(...)`; `WD:169` `UnixStream::connect(&socket_path)`.
- `WD:653-660` `handle_disconnect()` → `set_is_connected(false)` then `thread::spawn(|| { while let Err(err) = init_socket() { println!("{err}"); } })`.
Verdict: agree.

### C6 — S077 theme search and `~` replacement: AGREE (precision note)
Note lines 119-124. Anchors `[WT:56, 60-63, 132-135]`.
- `WT:53` `pub fn setup_themes(...)`; `WT:56` `xdg::BaseDirectories::with_prefix("walker").find_config_files("themes")`.
- `WT:60-63` `if let Some(a) = &get_config().additional_theme_location && let Ok(home) = env::var("HOME") { config_paths.push(PathBuf::from(a.replace("~", &home).to_string())); }` — literal replace, not shell expansion.
- `WT:132-135` `if !themes.contains_key("default") { themes.insert("default".to_string(), Theme::default()); … }`.
Verdict: agree. F5: the adjective “compiled” is established by `WT:30-39` (`include_str!("../../resources/themes/default/layout.xml")`, `keybind.xml`, `preview.xml`) and `WT:260` (compiled default `style.css`), not by 132-135 alone; the anchor shows only the fallback call.

### C7 — S078 Cargo.toml version and notify: AGREE
Note lines 50-51 and 99-107. Anchors `[WK:2-3, 21]`.
- `WK:2-3` `name = "walker"` / `version = "2.17.2"`.
- `WK:21` `notify = "8.2.0"`.
Verdict: agree.

### C8 — S079 tag tarball watcher/reload search: AGREE on substance; literal “only” enumeration DISAGREE
Note lines 91-107. Anchors `[WX]` (whole-tree).
Extracted tarball to `/tmp/rwu-walker/walker-2.17.2`, then:
- `grep -rn 'notify' .` (excluding Cargo.lock): `./Cargo.toml:21`, `./LICENSE:419` (“fails to notify you”), `./src/niri.rs:160,168,185,205,212,213` (closure parameter names / call). No `notify::` and no `use notify` (both greps empty over the tree).
- `grep -rn 'inotify' .` → only `Cargo.lock:1163,1169,1174,1355`; `Cargo.lock` `name = "notify"` / `version = "8.2.0"` block lists `"inotify"` at `:1355`. No inotify in `src/`.
- `grep -rnE 'reload_config|set_config' .` → empty.
- `grep -rn 'connect_changed' src/` → exactly three: `src/main.rs:142` (`color-scheme`), `src/main.rs:149` (`accent-color`), `src/ui/window.rs:479` (search entry).
Verdict: the material claim (notify crate unused by code; read-once; exactly three connect_changed; no reload entry point) is confirmed. The sentence “finds `notify` only in the `Cargo.lock` entry … and as closure parameter names in `src/niri.rs:160-213`” is literally false: the token also occurs at `Cargo.toml:21` (the declaration) and `LICENSE:419` (licence prose). No behavioural consequence; word “only” should be dropped or scoped to code/`src`.

### C9 — S080 elephant README: AGREE
Note lines 126-152. Anchors `[ER:123, 129, 140-141, 177-178, 183-189, 192-194, 211]`.
- `ER:123` “It needs to run with the users environment.”; `ER:127-129` `elephant service enable/disable`; “The service file will be placed in `~/.config/systemd/user/elephant.service`.”
- `ER:140-141` `elephant --config /path/to/config`.
- `ER:175` `elephant generatedoc`; `ER:177-178` service management.
- `ER:183-189` `~/.config/elephant/` tree with `elephant.toml`, `.env`, `<provider>.toml`; `ER:192-194` `generatedoc`/`generatedoc <provider>`.
- `ER:211` “Connect to the Unix socket (typically at `/tmp/elephant.sock`)”.
Verdict: agree. The drift sentence is supported by `EC:38-44` (XDG path; `/tmp` only via `os.TempDir()` with an `elephant/` subdirectory, `EC:40-42`), so the README line is stale for this tag.

### C10 — S081 elephant comm.go socket: AGREE
Note lines 128-132. Anchors `[EC:38-44, 40-42, 47]`.
- `EC:38` `rd := os.Getenv("XDG_RUNTIME_DIR")`; `EC:40-42` `if rd == "" { slog.Error("socket", "runtimedir", "XDG_RUNTIME_DIR not set. falling back to /tmp"); Socket = filepath.Join(os.TempDir(), "elephant", "elephant.sock") }`.
- `EC:44` `Socket = filepath.Join(rd, "elephant", "elephant.sock")`; `EC:47` `os.MkdirAll(filepath.Dir(Socket), 0o755)`.
- `EC:58-63` `StartListen()` removes and listens on `Socket`.
Verdict: agree (byte-for-byte on the quoted log string).

### C11 — S082 elephant CLI + S083 global config loader: AGREE (one inference now proven outside the cited set)
Note lines 138-152. Anchors `[ED:46-47, 94-95, 177-187, 299-305, 325]`, `[EG:28-36, 41-48, 85-89, 93-96]`.
- `ED:46-47` and `94-95` `h := xdg.ConfigHome; filepath.Join(h, "systemd", "user", "elephant.service")` (enable / disable).
- `ED:177-187` `generate config` subcommand → `handleGenerateConfig(cmd.StringArg("provider"), true)`.
- `ED:299-305` `StringFlag{Name:"config", … Action: func(…) error { common.SetExplicitDir(val); return nil }}`; `ED:325` `common.LoadGlobalConfig()`.
- `EG:28-36` `ElephantConfig` fields `provider_hosts`, `auto_detect_launch_prefix`, `launch_prefix`, `terminal_cmd`, `overload_local_env`, `ignored_providers`, `git_on_demand`, `before_load`.
- `EG:41-48` `LoadGlobalConfig()` sets defaults and calls `LoadConfig("elephant", elephantConfig)`.
- `EG:85-89` `userConfig, err := ProviderConfig(provider); if err != nil { slog.Info(provider, "config", "using default config"); return }`; `EG:93-96` parse error `slog.Error(...); os.Exit(1)`.
Verdict: agree. F7: the note’s phrase “a missing user file” is not shown by `EG:85-89`; the extra body `pkg/common/files.go:65-77` shows `ProviderConfig` returns `ErrConfigNotExists` when no file exists in `ConfigDirs()` (it has no other error path), so the label is true — but it rests on a file the note declares unread in § Unexercised (`ProviderConfig` body absent; `EG:85` only call site). Next round: cite `files.go` or mark the clause `[INF]`.

### C12 — S085-S089 omarchy stock config, launcher, restart, refresh, unit files: AGREE
Note lines 154-171. Anchors `[OC]`, `[OL:5-7, 10-12, 14]`, `[OR:6-8, 10-14, 17-21]`, `[OF:5-10, 15-17, 20-23, 26]`, `[OD:4]`.
- Stock config `OC`: 1,336 B, 49 lines, sha `fecf71fa…`; equal to host `~/.config/walker/config.toml` (`sha256sum` → `fecf71fa…`, `wc` → 49 lines). Contents at the claimed lines: `force_keyboard_focus = true` :1, `selection_wrap = true` :2, `theme = "omarchy-default"` :3, `additional_theme_location = "~/.local/share/omarchy/default/walker/themes/"` :4, `hide_action_hints = true` :5, `[keybinds]`/`quick_activate = []` :10-11, `[columns]`/`symbols = 1` :13-14, `[providers]`/`max_results = 256` :17, `default = ["desktopapplications","websearch"]` :18-21, six `[[providers.prefixes]]` :23-45, `[[emergencies]]` text/command :47-49. Its prefix table does differ from `WC:75-113` (`/`→providerlist, `.`→files, `:`→symbols, `$`→clipboard), as stated.
- `OL:5-7` `if ! pgrep -x elephant …; then setsid uwsm-app -- elephant &`; `OL:10-12` `pgrep -f "walker --gapplication-service"` → `setsid uwsm-app -- env GSK_RENDERER=cairo walker --gapplication-service &`; `OL:14` `exec walker --width 644 --maxheight 300 --minheight 300 "$@"`.
- `OR:6-8` `systemctl --user is-enabled elephant.service` → `restart elephant.service`; `OR:10-14` `app-walker@autostart.service`, else “Unable to restart Walker -- RESTART MANUALLY”; `OR:17-21` `EUID == 0` → `systemd-run --uid="$SCRIPT_OWNER" --setenv=XDG_RUNTIME_DIR=…`.
- `OF:5-10` copies `walker.desktop` and `restart.conf` to `~/.config/autostart/` and `app-walker@autostart.service.d/`; `OF:15-17` `omarchy-refresh-config walker/config.toml`, `elephant/calc.toml`, `elephant/desktopapplications.toml`; `OF:20-23` links `default/elephant/*.lua` into `~/.config/elephant/menus`; `OF:26` `omarchy-restart-walker`.
- `OD:4` `Exec=walker --gapplication-service`; `restart.conf` 38 B sha `de0f7029…` (`[Service] Restart=always RestartSec=2`).
Verdict: agree.

## Findings (severity order)

- **Low — F1 (C8 literal).** “finds `notify` only in the `Cargo.lock` entry … and as closure parameter names in `src/niri.rs:160-213`” is false as an enumeration: `Cargo.toml:21` and `LICENSE:419` also contain the token. The substantive “notify crate unused in `src/`” claim is proved by the same searches. Fix wording, not data.
- **Low — F2 (row anchor summaries under-cover the note).** Five cited ranges across three rows fall outside the SOURCES row anchor cells while still being true in the bodies: S074 `WS:245` (row lists `211-243`; `WS:245` is `fn merge`), S075 `WM:635-642` and `WM:782` (row lists `104-108,124-126,670-674,784-786,802-803,872-882`), S080 `ER:177-178` and `192-194` (row lists `123-141,166,181-192,211`). No claim falsehood; the registry cells and the note drifted apart. Extend the cells or trim the citations.
- **Low — F3 (C4 over-generalisation).** “when visible and `close_when_open` is set the activation closes it” omits the `!is_stay_open_explicit_provider` / `!is_dmenu_keep_open` / `is_param_close` guards printed at `WM:635-639`; the anchor itself carries the exceptions.
- **Low — F4 (C4 inference).** “without a running service” is not the literal `WM:802-803` condition (`!IS_SERVICE && !dmenu`); it follows only from GApplication remote-instance behaviour (`WM:83,96`), which the note does not anchor.
- **Low — F5 (C6 anchor).** “compiled theme” is not shown by `WT:132-135`; the compiled assets are at `WT:30-39` (`include_str!` for layout/keybind/preview) and `WT:260` (default `style.css`). Add the anchor.
- **Info — F6 (S084 mutability).** The only non-tag-pinned row in S072-S089 is S084 (`docs.rs/xdg/latest`); on 2026-10-20 it serves xdg 3.0.0, matching `WK:30`, and the digest still equals the committed receipt. It is mutable on the next xdg release; the gate text in `lessons/round-18.md` already rejects unversioned docs as version-specific support, so this row should be pinned to `/xdg/3.0.0/` at the next touch.
- **Info — F7 (C11 chain).** “missing user file” is true, but only via `pkg/common/files.go:65-77`, which is outside the note’s fetched set and is declared `[UNK]` in § Unexercised. Cite it or label the clause `[INF]`; the row’s S083 anchor list does not include `files.go`.
- **Info — F8 (C1 link).** `WR:215` links `refs/heads/master`, not the tag; harmless today because the note does not quote the link’s content.
- **Process — F9 (self-disclosure).** I ran `git status --porcelain` twice in the lane (on `.ufo/waves/round-18/fetch`) before re-reading the “never `git status` in the lane” fence. Read-only; no byte changed, but it is a fence violation and is recorded here for the wave report.
- **Process — F10 (bodies untracked).** At `4c103b5` and `abfbf35` only `receipts.jsonl` is committed (21 blobs); the 27 NoteWalker bodies are untracked. Verification of quoted text is therefore network-dependent: receipt digest + re-fetch. My 19 re-fetches agree, but no committed byte carries the quoted lines. R17-V3 asked for “body bytes, sha256, byte count, fetch time”; the receipt carries bytes/sha/time but the body is not in git.
- **Process — F11 (self-disclosure, misroot).** My first `write`/`edit` calls used a workspace-root-relative path and landed the report at `/home/vgpnk/Projects/shokunin/.ufo/waves/round-18/w2/reports/ReviewWalkerUpstream.md` (fleet root). I detected it when `read` on the lane path returned “not found”, moved the file to the lane with `mv` (sha `60ed2284…` at move time), and removed the three empty directories I had created under the fleet root with `rmdir`. The report now exists only at the lane path; no other lane or fleet byte was touched. Same class as lesson M5; the relative-path fence remains prompt-level.

## Residual risk / verification gaps

- Documentary only: no walker/elephant process, socket, service or Hyprland state was observed; `/usr/bin/walker` build identity to tag v2.17.2 remains `[UNK]` (not re-checked here; out of this item).
- The tag raw URLs were fetched at `v2.17.2` / `v2.22.1` / `v3.8.4`; I did not re-run `git ls-remote` for the tags (sibling reports ReopenS075/S086 do, with lightweight-tag results). Digests match the committed receipts, so the raw bytes are the ones wave 1 recorded.
- Line numbers are body lines for these exact digests; any upstream retag/rewrite invalidates them.
- Sibling independent reports (`ReopenS073`, `S075`, `S077`, `S078`, `S079`-`S083`, `S086`) reach the same row verdicts; I did not rely on them for any verdict above.
- No tool install or upgrade was performed; no fetch outside the lane; scratch extraction only in `/tmp/rwu-walker`.

## Verdict

11 of 12 sampled claims agree exactly with the anchored bodies; C8 agrees on substance with one literal overstatement. No claim in § Upstream contract cites a line that does not support it. The section survives falsification; the actionable residue is wording/anchor hygiene (F1, F2, F3, F5, F6, F7) and two process gaps (F9 self-disclosure, F10 uncommitted bodies). No crash, no wrong digit, no invented row.
