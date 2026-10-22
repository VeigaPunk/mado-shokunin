# ReviewNoteClaims: C2 claim review, round 23 wave 2 (falsify)

Seat: MadoR23.ReviewNoteClaims (leaf reviewer; no subagents; no lane edits).
Lane tip reviewed: 2f1134f38930fc8b067d2d7f5bba126338faabdd. The C2 note and its SOURCES rows landed at c8cb3930; the tip commit touches only PROVINCE.md, so the note and SOURCES are unchanged since c8cb3930.

Bytes reviewed (identical to the tip blobs and to the working copy):
- corpus/knowledge/terminal-trees-r23.md: sha256 1038dbc4e2182ce368ffb8c9eb6a83274207a411b8e4cd4f0961c446b10a2c2e, 95 lines.
- corpus/SOURCES.md: sha256 ed4c561f0c35ecf8c9da6468ddeccd5df98d99d538f7df0aa3d248769f69f1dc, 392 lines.

## Verdict

NOT CLEAN. Tag pins, upstream source bytes, dates and this host's file bytes all check out. Five of the fifteen claim rows fail as worded: F4, K4, C2, C4 and C5. Six pass only with a fix (an anchor, a precondition, or wording). Four pass clean. The C2 counter reports 3/3, but it checks citation shape only; none of the failures below would make it fail.

Coverage: 15/15 claim rows; all upstream rows cited by the note (29 source digests); 4/4 tag pins; 7/7 dates; 6/6 host files; the Upstream contract, Host declaration, Safe observation, Unexercised and Supersedes sections; one counter re-run.

## What I did (read-only)

1. Lane pin. Read-only git only: `rev-parse`, `log`, `show --stat` on 2f1134f3. `git show 2f1134f3:<path> | sha256sum` for both files (match the working copy). `git diff --stat c8cb3930 2f1134f3 -- <both paths>` returned nothing.
2. Upstream bytes. Fetched all 29 SOURCES-row sources with a plain HTTPS GET (raw.githubusercontent.com; codeberg raw/tag/1.28.0). All returned 200. sha256 matched the digest in each row (29/29). S132 is queued and supports nothing, so it was not fetched. Copies: /fast/scratch/hyaku/mado-r23/ReviewNoteClaims/upstream/.
3. Foot wiki. `git clone --bare https://codeberg.org/dnkl/foot.wiki.git`, then `git show 2475351a...:Home.md`: sha256 78bd64dc... matches S149. Commit date 2025-12-28 12:19:14 +0100.
4. Tag pins, `git ls-remote --tags`. Foot 1.28.0 gives tag object 3d97bba5, peeled ab33c9a1. Kitty v0.49.2 gives e3005973, peeled b2cb8712. Ghostty v1.3.1 gives 22efb0be, peeled 332b2aef; v1.2.3 gives ae9b7892, peeled 6d2dd585. All match the note. The newest tag by version sort equals the pin for all three upstreams at check time.
5. Shallow clones at the pins: /fast/scratch/hyaku/mado-r23/ReviewNoteClaims/clones/{ghostty-v1.3.1,foot-1.28.0}. Full-tree greps for the C5 sweep and the foot signal/reload surface.
6. GitHub API, unauthenticated GET. PR #8885: merged_at 2025-10-12T20:48:06Z, merge commit cbeb6890. Website commits 3755ed6e (2026-04-01) and 155c4cd7 (2026-03-13, message "update refs"). Ghostty tag taggers: v1.2.3 2025-10-23T17:34:09Z, v1.3.1 2026-03-13T16:03:38Z.
7. Host probes, read-only. `command -v foot kitty ghostty` (none). `pacman -Q foot kitty ghostty` (not found, exit 1). `pgrep -l -x` per name (none). `sha256sum`, `stat -c`, `ls -la` on the six files. `cat ~/.config/xdg-terminals.list`. `cmp` of each backup against ~/.local/share/omarchy/config/{foot/foot.ini,kitty/kitty.conf,ghostty/config} (identical). `diff` of live against omarchy (one changed line each). `git -C ~/.local/share/omarchy describe --tags`, `log -1`, `tag --points-at HEAD`, `status --porcelain`. `hyprctl -j clients | jq` (query only). Grep of `Hidden=` in ~/.local/share/applications/{foot-server,footclient}.desktop.
8. Counter re-run: `python3 -I .ufo/waves/round-23/c2/count.py 2f1134f38930fc8b067d2d7f5bba126338faabdd` gave 3/3, exit 0. This matches evidence/c2-after-2f1134f3.json.
9. lsp not used. No lane code is under review; upstream checks were text reads and greps over pinned trees.

Installs and updates: none. The only pacman call was `pacman -Q` (no transaction). I wrote nothing in the lane except this report.

## Findings

### High

**H1. C4 (note line 51): "Two documented upstream routes".** Only the keybinding is documented. The docs (index.mdx:121-131) name the keybinding and the `reload_config` action. reference.mdx has no SIGUSR or SIGHUP text (grep). SIGUSR2 appears only in code: application.zig:1486-1495 (GTK) and AppDelegate.swift:543-551 (macOS). At this pin the SIGUSR2 route is code-only and should not be called documented.

**H2. C4 (line 51): "SIGUSR2 ... performs a hard reload ... or a soft reload".** Neither user route can soft-reload at this pin. The GTK SIGUSR2 handler calls `Action.reloadConfig(self, .app, .{})` (application.zig:1492-1495). `ReloadConfig` defaults to `soft = false` (apprt/action.zig:858-862), so the signal always does a hard reload. The keybind path (App.zig:447) also passes `.{}`, so it is hard too. The only `soft = true` call sites are internal: App.zig:412-431 (colour-scheme change) and Surface.zig:1677-1687 (conditional-state change). Suggested wording: "both user routes perform a hard reload; soft reload is internal, triggered by colour-scheme and conditional-state changes."

**H3. C5 (line 52): "a treewide sweep of the v1.3.1 tree found SIGUSR2 only (GTK app, macOS app delegate)".** Wrong on two counts.
- Scope. SrcGhostty.md:42 extracts only `ghostty-1.3.1/src/*` and `ghostty-1.3.1/macos/*`. The grep at SrcGhostty.md:53 ran over that extract, so it was not treewide.
- Result. dist/linux/systemd.service.in:8-9 contains `Type=notify-reload` and `ReloadSignal=SIGUSR2`, so systemd-driven reloads also send SIGUSR2.

The negative claims survive my full-tree sweep. Zero hits for FileMonitor, inotify_init, inotify_add_watch, GFileMonitor, makeFileSystemObjectSource, EVFILT_VNODE, FSEvents, watchFile, fs.watch, FileWatch, file_watch and IN_MODIFY. A case-insensitive "watch" in src/ shows only comments and unrelated code. SIGHUP appears only where the child is signalled (see M11). The conclusion "reload needs keybind, action or SIGUSR2, or a restart" still holds; the sweep's scope and result text do not.

**H4. F4 (line 31), and the `teaches` columns of S146 and S141: "the only handled signals (SIGUSR1, SIGUSR2)".** foot 1.28.0 also handles SIGINT and SIGTERM (main.c:663-665, `fdm_sigint`) and SIGCHLD (reaper.c:41). footclient registers SIGINT, SIGTERM, SIGUSR1 and SIGUSR2 (client.c:559-562). The docs (foot.1.scd:702-705) list only SIGUSR1/2 as "special meaning", not "only". The conclusion that no signal reloads the config still holds, because none of the extra handlers reloads it. The sentence is false as written. Suggested: "SIGUSR1/2 switch theme; SIGINT/SIGTERM terminate; SIGCHLD is reaped; SIGHUP and SIGPIPE are ignored."

**H5. C2 (line 49): "the per-option reference carries the same text (S135)".** False. reference.mdx contains none of: "custom, but very simplistic key = value syntax", "Comments start with a `#`", "Empty values reset the configuration", "Every configuration key is a valid CLI flag". Only index.mdx:57-90 (S134) carries those format claims. Drop the S135 citation for the format row.

### Medium

**M1. C2 (line 49): "2025-10-12 change 'Add .ghostty extension to config (#8885)'".** The date is right: PR #8885 merged 2025-10-12T20:48:06Z (merge commit cbeb6890). No SOURCES row carries it; S134, S135 and S151 do not. Add a row for the PR or merge commit, or drop the date.

**M2. K4 (line 41): "the default keybind kitty_mod+f5 ... bound to reload_config_file".** The key invokes the `load_config_file` action. definition.py:4694 reads `'reload_config_file kitty_mod+f5 load_config_file'`. conf/types.py:760-764 (`add_map`) takes the first token as the shortcut name. `ShortcutMapping` (types.py:457-458) sets key = `kitty_mod+f5` and action = `load_config_file`. `reload_config_file` is the documentation name (the :sc: role), not the action.

**M3. K5 (line 42): "a running instance can be told to reload a specified kitty.conf".** The precondition is missing. `kitten @` needs remote control, and `allow_remote_control` defaults to `no` (definition.py:2912-2915). The row cites only rc/load_config.py. The note does say remote control was not enabled, but the row should state the precondition.

**M4. K1 (line 38): "documented and implemented order at one tag".** The launcher's implementation differs from the help text. launcher/utils.h:190-199 accepts a candidate directory only if kitty/kitty.conf exists inside it and the directory is writable. `check_and_ret` (:215-219) applies that gate to XDG_CONFIG_HOME, ~/.config and every XDG_CONFIG_DIRS entry. :235-240 falls back to creating $XDG_CONFIG_HOME/kitty. An XDG_CONFIG_DIRS candidate, which is normally not writable, cannot be the chosen directory. The macOS ~/Library/Preferences entry is also omitted (harmless on this Linux host). Suggested: "documented (CONFIG_HELP) and implemented with a writability gate."

**M5. C2 (line 49) and S136 `teaches`: "(or config before 1.2.3)" and "prefers whichever exists".** "(or config before 1.2.3)" is the site's wording. Upstream v1.3.1 still loads the legacy `config`: Config.zig:3994-4011 loads legacy then config.ghostty, and warns when both exist. S136's "prefers whichever exists" describes `preferredXdgPath` and `preferredDefaultFilePath` (file_load.zig:27-50, 96-121), which the XDG loader does not use. C1 is right that both files are consulted; say both are loaded, with config.ghostty winning.

**M6. F2 (line 29): "a trailing # comment after a value is accepted by the parser".** True at config.c:3221-3241, but only when the `#` is preceded by whitespace (the `isblank` test at :3234). `key=value#x` keeps the `#`. No cited S row covers `parse_config_file`; S145 covers open_config, include and config_load. Add the anchor and the whitespace qualifier.

**M7. F4 (line 31) and S147 `teaches`: "spawn-terminal execs a new foot --config <path>".** `term_spawn_new` passes `--config` only when `term->conf->conf_path` is set (terminal.c:3821-3825). Otherwise the child starts without it. Add the condition.

**M8. F5 (line 32): "every client terminal inherits that parsed config".** server.c:364-392 clones the server config when a client has `-o` overrides or a different hold setting. Otherwise clients share `server->conf`. True only without per-client overrides; say so.

**M9. K4 (line 41): "whose handler calls the load_config_file boss action".** The signal handler only sets a flag (child-monitor.c:1708, 1851-1854). The event loop consumes it (:558-566) and makes the boss call (:640). Reword.

**M10. Citation hygiene.** F4's bound column says the wiki's [colors] spelling is stale for 1.28.0. That is true (CHANGELOG.md:110-118, S152), but F4's sources column does not cite S152. Header-listed sources that no claim row cites: S131 (kitty changelog; the 2026-10-01 date), S142 (footclient), S143 (foot README) and S152. The counter does not check this.

**M11. C5 (line 52): "SIGHUP only where a child process is signalled (src/termio/Exec.zig, src/pty.zig)".** pty.zig:215-234 (`childPreExec`) resets the child's dispositions to SIG_DFL, HUP included. It signals nothing. Exec.zig:1095-1162 and :1227 do signal the child. Reword the pty.zig part.

### Host statements not observed, or inconsistent

**HO1. L67-70 (selection chain "still resolves away from all three").** Presented as an observed present-tense fact. What was observed: xdg-terminals.list names only Alacritty.desktop, and one Alacritty client. The xdg-terminal-exec resolution was never run. Label it [INFERENCE] or cite the round-17 documentary route.

**HO2. L68-70 ("the live clients are Alacritty (HostGhostty ... 2 Alacritty clients)").** My probe at 2026-10-22 found one client, class Alacritty (`hyprctl -j clients | jq`). HostGhostty.md:80-82 recorded two. Timestamp the count or drop it.

**HO3. L65 ("omarchy 3.8.3 checkout").** git says v3.8.4. `git describe --tags` gives v3.8.4. HEAD 8fcc9d60 (2026-07-20T14:05:35-07:00) carries that tag, and the tree is clean. Only the `version` file says 3.8.3. The byte-identity holds against the v3.8.4 checkout; fix the label.

**HO4. L12-13 ("no consumer today").** An inference from absence of binaries and processes. It is not labelled.

### Verified as stated (no change needed)

- Host (L63-65): sizes, sha256 prefixes, mtimes (2026-10-03 19:02:29), no binaries, no packages, no processes, Alacritty-only xdg list. Backups are byte-identical to the omarchy defaults. Live files differ from them by one line each: foot `size=9` vs `12.5`; kitty `font_size 9.0` vs `12.5`; ghostty `font-size = 9` vs `12.5`.
- Unexercised (L86-87): both foot user desktop entries (foot-server.desktop, footclient.desktop) carry `Hidden=true`. Re-derived here.
- Supersedes (L92-95): both quotes match verbatim (terminal-route-r17.md:5; corpus/README.md:123-124). terminals-and-omarchy.md §8 unknown (1) matches.
- Upstream contract (L18-22): tag objects and peeled commits; kitty 0.49.2 changelog heading [2026-10-01] (changelog.rst:202); foot 1.28.0 tagger 2026-09-02 (matches S140's "released" date); each pin is the newest tag at check time.

## Claim-by-claim (15 rows)

| Row | Line | Verdict | Evidence checked, and what fails |
|---|---|---|---|
| F1 foot search order | 28 | PASS | doc 14-20; config.c 421-476 (XDG_CONFIG_HOME, then XDG_CONFIG_DIRS default /etc/xdg); 3712-3723 (`--config` bypasses search). |
| F2 foot format | 29 | PASS with gap (M6) | doc 9-33 and template match. Trailing `#` needs anchor and whitespace qualifier. |
| F3 foot include | 30 | PASS | doc 110-121; config.c 909-947 (`~/` expansion, absolute-path check, recursive parse with its own section state). |
| F4 foot reload | 31 | FAIL in part (H4, M7, M10) | Parsed once (main.c:539-540) ✓. SIGHUP ignored (:681-688) ✓. Theme signals (:56-70) ✓. Wiki FAQ Home.md:1011-1015 ✓. No config-reload action and no inotify anywhere in the 1.28.0 tree ✓ (sweep, not recorded in the row). "Only handled signals" ✗. |
| F5 foot check-config | 32 | PASS with nuance (M8) | `ret` starts at -26 (main.c:198-199), which is exit 230. check_config returns before window setup (:548-551) ✓. |
| K1 kitty search | 38 | PASS with nuance (M4) | CONFIG_HELP (simple_cli_definitions.py:366-376) ✓. Launcher writability gate. macOS entry omitted. |
| K2 kitty format | 39 | PASS with gap | conf.rst 26-37 ✓. conf/utils.py 287-289 (`#` lines), 401-404 (backslash continuation), 359-362 (unknown key ignored). Those lines are not in the cited anchors. |
| K3 kitty includes | 40 | PASS | conf.rst 39-63 ✓. conf/utils.py 344-355: relative to the including file (base path from :377); missing file logged and ignored. Optional: geninclude can be disabled (:317-320). |
| K4 kitty reload | 41 | FAIL in part (M2, M9) | auto_reload 0.1 s and "only if kitty.conf existed at start" (definition.py:3090-3102) ✓. kitty_mod ctrl+shift (:3650-3651) ✓. SIGUSR1 documented (conf.rst:22) ✓. Action name ✗. |
| K5 kitty load-config | 42 | PASS with gap (M3) | rc/load_config.py 31-40 ✓. Remote-control precondition missing. |
| C1 ghostty paths | 48 | PASS with nuance (M5) | index.mdx 41-55 ✓. Config.zig:3992-3993 quote verified ✓. xdg.zig 23-29, 56-101 ✓. macOS path after XDG ✓. |
| C2 ghostty format | 49 | FAIL (H5, M1, M5) | Format facts ✓ (index.mdx 57-90). S135 citation ✗. Date true but unanchored. Legacy `config` still loaded at 1.3.1. |
| C3 ghostty include | 50 | PASS | index.mdx 99-108 ✓. reference.mdx 2490-2503 ✓. Config.zig 2435-2436 quote ✓. loadRecursiveFiles (:4171) cycle diagnostic (:4214-4222) ✓. |
| C4 ghostty reload | 51 | FAIL (H1, H2) | Keybind ✓ (index.mdx 123-126; Config.zig 6401-6406). "Some options cannot be reloaded at runtime" ✓ (index.mdx 128-131). SIGUSR2 "documented" ✗ (code-only). Hard-or-soft ✗ (always hard). |
| C5 ghostty negative | 52 | FAIL in part (H3, M11) | Negative API claims confirmed on the full tree ✓. Sweep scope ✗. systemd unit omitted ✗. pty.zig wording ✗. |

Counts: PASS clean 4 (F1, F3, K3, C3). PASS with nuance or gap 6 (F2, F5, K1, K2, K5, C1). FAIL in part 5 (F4, K4, C2, C4, C5).

## Source bytes, anchors and dates

- 29/29 digests match. Every kitty S124-S133 anchor I checked is accurate. Foot S140-S148 and S152 anchors checked. Ghostty S134-S139, S150 and S151 checked.
- Small line-range drifts only, none used by a claim: S136 preferredDefaultFilePath cited 88-112 (body 96-121); S139 reloadConfig cited 2406-2450 (body 2407-2444); S151 cited 3375-3380 (body 3376-3380).
- Orphan rows (header-listed, cited by no claim row): S131, S142, S143, S152 (M10). S132 is queued and correctly unused.
- Dates, 7/7 checked: PR #8885 merge; website commits 3755ed6e and 155c4cd7; ghostty v1.2.3 and v1.3.1 taggers; foot 1.28.0 tagger; kitty changelog heading; wiki commit date.

## Counter scope

count.py (v2) checks: table-row shape; host-tree cell; each S-id resolves to a registry row with status `mined` and opened 2026-10-22; source cell names the terminal and its upstream host; used-by names the note. It does not check whether an anchor supports the row's claim. All 15 claim rows pass the counter; every fail above passes it too. Do not cite 3/3 as evidence of claim support.

## Residual risk and verification gaps

- No terminal binary is installed on this host. Runtime behaviour is documentary only; nothing was observed.
- macOS sources (AppDelegate.swift, macOS app-support loader) were read as bytes only.
- Sweeps used shallow clones at the tags. The literal ghostty sweep covered the whole tree. The case-insensitive "watch" sweep covered src/ only. The foot sweep used grep patterns (signal registration, sigaction, fdm_signal_add, config_load, inotify, FileMonitor, reload, watch, case-insensitive); I did not enumerate every keybinding name.
- Host state is point-in-time: the client count and the omarchy HEAD may change. I could not check the L1's 11:55Z timestamp.
- The rendered ghostty.org pages (S134/S135 "rendered" digests) were not re-fetched; the pinned raw files match, and the claims cite those.
- The PR merge date comes from the GitHub API. I did not read the merge commit's diff.

## Suggested fixes (advice only; the L1 decides)

1. C4: documented route is the keybinding (S134); code-only route is SIGUSR2 (S139, S150), always a hard reload; soft reload is internal (App.zig:412-431; Surface.zig:1677-1687).
2. C5: rerun the sweep over the whole tree, including dist/, and record the exact patterns and scope. Add dist/linux/systemd.service.in:8-9. Reword the pty.zig clause.
3. F4, S141 and S146: replace "only handled signals" with the list in H4.
4. C2: drop the S135 citation for format facts. Add an S row for PR #8885 (merge cbeb6890) or drop the date. State that legacy `config` is still loaded at v1.3.1.
5. K4: "bound to the load_config_file action (shortcut name reload_config_file)".
6. K5: add the allow_remote_control precondition (default `no`).
7. K1: "documented (CONFIG_HELP), implemented with a writability gate".
8. Host: relabel the omarchy checkout as v3.8.4 (per git); timestamp the client count; mark the chain resolution [INFERENCE].
9. Cite S152 in F4. Cite S131 for the kitty date. Drop unused S142 and S143 from the header, or cite them.

Verdict: NOT CLEAN. Five of fifteen claim rows fail as worded (F4, K4, C2, C4, C5). Pins (4/4), upstream source bytes (29/29), dates (7/7) and host bytes (6/6) pass.
