# RecheckSweep — 8 of 65 trigger rows fired: S003 (PROTOCOL.md drift+line shift) and the 7 omarchy-v3.8.4 rows (v4 line, default branch `quattro`); all 16 in-lane upstream projects except omarchy/xdp sit exactly on their pinned tag

Freshness inputs for L1's frontier step. No lane file was edited; this report is the only write.

## Method and decision rule

Rows taken from `corpus/SOURCES.md` rows with `recheck` ∈ {`on-release` (44), `on-change` (21)} = 65 of 95 rows; other triggers (`180d` 13, `90d` 11, `on-gate-change` 2, `on-session-change` 1, `on-capture-change` 1, `on-compositor-release` 1, `on-operator-recovery-decision` 1) are out of scope.

Trigger reads used, all read-only:

- upstream tag sets: `git ls-remote --tags --heads <url>` over 17 repos; tag→commit dates only where a tag newer than the pin existed, via `git init --bare` + `git fetch --filter=blob:none --depth=1 origin refs/tags/<t>` + `git log -1 --format=%cI FETCH_HEAD` in a **/tmp** scratch repo (removed after each);
- branch drift: same shallow fetch of the default-branch ref, resolved with `git ls-remote --symref <url> HEAD`;
- host package moves: `/var/log/pacman.log` read as file bytes (`grep -n 'upgraded <pkg>'`), never pacman;
- host/local file bytes: `sha256sum` compared against the digest written in the row, plus `stat -c %y`;
- one crates.io API read (S084), no receipt dir opened — see Limits.

`fired?` is one of:

- `yes` — the row's recheck condition is satisfied now: on-release ⇒ a release tag newer than the row's pin exists and is dated on/after the row's `opened` date; on-change ⇒ the cited bytes or the upstream ref the row leans on moved on/after `opened`.
- `yes*` — the cited tag bytes are immutable, but the upstream project moved past the pin on/after `opened` (major line / renamed default branch); re-anchor is L1's call.
- `no` — cited bytes unchanged and no newer release.
- `[UNK]` — not decidable without a fetch this seat did not open.

Reference instants: this run's UTC clock `2026-10-20T17:06:52Z`; `opened` is date-only in the ledger, so same-day events are reported with their exact timestamps.

## Summary

- **8 yes**: S003 (own/fleet spec drift), S085-S089 (omarchy on-change, project-level `yes*`), S093/S094 (omarchy on-release, `v4.5.0-rc1` same-day).
- **57 no**: every other pinned upstream tag is still the newest tag of its repo. Specifically `Hyprland v0.56.2`, `wayland-protocols 1.49`, `xdph v1.4.1`, `wayland-utils 1.3.0`, `libinput 1.32.0`, `wayland 1.26.0`, `Waybar 0.15.0`, `xdg-terminal-exec v0.14.3`, `alacritty v0.17.0`, `hypridle v0.1.8`, `hyprlock v0.9.6`, `walker v2.17.2`, `elephant v2.22.1`, `swaybg v1.2.2` are each the maximum tag in their repo's `ls-remote` output today.
- Two "pin already behind at open" cases that are **not** trigger fires but are freshness inputs: **S038** (pins xdp 1.21.0 while 1.22.0 @2026-06-08 and 1.22.1 @2026-06-17 already existed) and **S039** (pins 1.22.0 while 1.22.1 @2026-06-17 already existed).
- Host moves since the 2026-10-20 opened day are all *at* the pinned versions, not past them: walker 2.17.2 (pacman.log:2929), elephant 2.22.1 (:3095), hyprland 0.56.2-4 (:2733, pkgrel only), xdg-terminal-exec 0.14.3-2 (:2935, pkgrel only), libinput 1.32.0 (:2432), wayland-utils 1.3.0-1 installed (:2413).

## Table

| id | trigger | fired? | basis (evidence) |
|---|---|---|---|
| S003 | on-change | **yes** | `sha256 PROTOCOL.md` at worktree/master = `886e459b…` vs cited `b1d4f4c0…` @31baf5c; changed by `7c5b34f 2026-10-19T19:08-03` (fleet `git log -1 --format=%cI -- PROTOCOL.md`). Cited ranges are text-identical but shifted **+15 lines**: `## Evidence standard` 328→343, `## Gate standard` 360→375 (`git show <rev>:PROTOCOL.md | grep -n '^## '`; `diff` of 328-358 vs 343-373 and 360-408 vs 375-423 = identical) — the numeric anchor in the row is stale even though the prose is not. |
| S004 | on-change | no | worktree `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` sha256 `6c674a2281afb75b…` = cited; `git cat-file -t 5b471e4` = commit, `git show 5b471e4:<path>` sha256 `6c674a22…` = same. |
| S005 | on-release | no | README last commit still `3dac056` 2026-01-16T10:34:26+02 (`git log -3 -- README.md` in a 400-deep bare clone); wayland-protocols main HEAD `35d9638` @2026-10-12 (pre-opened); 50 tags, max `1.49`. |
| S013 | on-change | no | gkeep `git rev-parse HEAD` = `133b8671…` = cited; `git hash-object install.sh` = `de4f910a4e9b…` = `HEAD:install.sh`; `git status --porcelain` empty. |
| S015 | on-change | no | `stat`: `corpus/knowledge/omarchy-drift-watch.md` mtime 2026-10-14 14:45:41 -0300, before opened 2026-10-19. |
| S018 | on-release | no | Hyprland `ls-remote --tags`: 119 tags, max `v0.56.2` = pin (no v0.57*); main HEAD `2860d07` @2026-10-20T15:02Z is commit drift only; host `pacman.log:2733` 0.56.2-2→0.56.2-4 is pkgrel-only. |
| S020 | on-change | no | `stat`: `~/.local/share/omarchy/default/hypr/windows.conf` + `apps/terminals.conf` mtime 2026-10-03 17:42, before opened. |
| S021 | on-release | no | Hyprland tag set max `v0.56.2` (released 2026-08-05, pre-opened); no post-opened release. |
| S022 | on-release | no | Same: no Hyprland release after v0.56.2; v0.54.0 wiki page is a version archive. |
| S023 | on-release | no | Same: no Hyprland release after v0.56.2; v0.54.0 archive. |
| S024 | on-release | no | Same: no Hyprland release after v0.56.2 (Lua announcement is 2026-04-26, historical). |
| S025 | on-release | no | Same: no release after v0.56.2 (0.55 announcement historical). |
| S026 | on-release | no | Same: `v0.55.0` remains max-but-one; no newer release since opened. |
| S027 | on-release | no | Same: no release after v0.56.2 (0.56 announcement historical). |
| S028 | on-release | no | Same: `v0.56.2` is still the repo's max tag. |
| S029 | on-release | no | No Hyprland release since opened; live-wiki page-byte edits are not release-gated and were not fetched by this seat. |
| S030 | on-release | no | Same as S029 (row is `rejected`; status unchanged by this sweep). |
| S035 | on-release | no | xdp tags max `1.22.1` @2026-06-17 (pre-opened); xdp main HEAD `8eba842` @2026-10-15 (pre-opened). |
| S036 | on-release | no | Same xdp evidence as S035. |
| S037 | on-release | no | XDPH 31 tags, max `v1.4.1` = pin; master HEAD `0121b2e` @2026-10-12 (pre-opened); host `pacman.log:1945` 1.4.0→1.4.1 on 2026-10-11. |
| S038 | on-release | no | xdp `1.21.0` pin; newer `1.22.0` @2026-06-08 and `1.22.1` @2026-06-17 both predate opened — **pin already behind at open**, no release since opened. |
| S039 | on-release | no | `1.22.1` tag @2026-06-17 (commit `1d20fadc`) predates opened — **pin already behind at open**, nothing since. |
| S040 | on-release | no | cited `35d9638cf0c3f0bb…` = current `refs/heads/main` of wayland-protocols (`ls-remote --heads`); commit immutable. |
| S043 | on-release | no | `/usr/share/wayland/wayland.xml` sha256 `cc860987…` = cited raw sha; `pacman.log:1473` wayland 1.25.0→1.26.0 on 2026-10-11, no later upgrade; wayland tags max `1.26.0`. |
| S046 | on-release | no | wayland-utils 6 tags, max `1.3.0` = pin; `pacman.log:2413` `installed wayland-utils (1.3.0-1)` 2026-10-20T01:06:49, same version. |
| S047 | on-release | no | `a741f0ac…` is an ancestor of master `bf4fc79` (2026-03-09, pre-opened); `git diff <pin> master -- unstable/wlr-output-management-unstable-v1.xml` empty, file last changed 2025-07-02; repo has 0 tags. |
| S048 | on-release | no | wayland-protocols 50 tags, max `1.49` = pin. |
| S051 | on-release | no | libinput 193 tags, max `1.32.0` = pin; `pacman.log:2432` 1.31.3→1.32.0 @2026-10-20T04:25:17 (host reaches the pin, not past it). |
| S052 | on-release | no | wayland 113 tags, max `1.26.0` = pin; host XML digest matches S052's raw sha (above). |
| S053 | on-release | no | Waybar 67 tags, max `0.15.0` = pin; host waybar 0.15.0-3 since `pacman.log:1944` 2026-10-11; master HEAD 2026-10-19T23:29+02 is commit drift, no tag. |
| S054 | on-release | no | Same Waybar tag evidence as S053. |
| S056 | on-release | no | xdg-terminal-exec 21 tags, max `v0.14.3` = pin; master `065925df…` equals the row's v0.14.3 ref; `pacman.log:2935` 0.14.3-1→0.14.3-2 is pkgrel only. |
| S057 | on-release | no | Same tag/master evidence as S056. |
| S058 | on-release | no | alacritty 163 tags, max `v0.17.0` = pin (`v0.17.0-rc1`/`-rc2` sort below it). |
| S059 | on-change | no | 3/3 digests match: bindings.conf `e574a1ed…`, xdg-terminals.list `d035da57…`, alacritty.toml `695301c8…`. |
| S060 | on-change | no | `/usr/share/xdg-terminal-exec/xdg-terminals.list` sha256 `a2b5bf69…` = cited (1053 B, mtime 2026-09-18); package moved 0.14.3-1→-2 (`pacman.log:2935`) without changing these bytes. |
| S065 | on-change | no | hypridle 9 tags, max `v0.1.8` = pin; main HEAD `aa958ed` @2026-08-11 (pre-opened). |
| S066 | on-change | no | Same hypridle evidence as S065. |
| S067 | on-change | no | Same hypridle evidence as S065. |
| S068 | on-change | no | Same hypridle evidence as S065. |
| S069 | on-change | no | hyprlock 20 tags, max `v0.9.6` = pin; main HEAD `0332e40` @2026-08-11 (pre-opened). |
| S071 | on-change | no | `~/.local/share/applications/Alacritty.desktop` sha256 `713703ba…` = cited. |
| S072 | on-change | no | walker 392 tags, max `v2.17.2` = pin (tag bytes immutable); master HEAD `a515085` @2026-10-08 (pre-opened). |
| S073 | on-release | no | walker max tag `v2.17.2` = pin; `pacman.log:2929` 2.17.0→2.17.2 @2026-10-20T09:16:46. |
| S074 | on-release | no | Same walker tag evidence as S073. |
| S075 | on-release | no | Same walker tag evidence as S073. |
| S076 | on-release | no | Same walker tag evidence as S073. |
| S077 | on-release | no | Same walker tag evidence as S073. |
| S078 | on-release | no | Same walker tag evidence as S073. |
| S079 | on-release | no | Same walker tag evidence as S073. |
| S080 | on-release | no | elephant 128 tags, max `v2.22.1` = pin; master HEAD `a35b3b5` @2026-09-29 (pre-opened); `pacman.log:3095` 2.21.0→2.22.1 @2026-10-20T09:31:03. |
| S081 | on-release | no | Same elephant evidence as S080. |
| S082 | on-release | no | Same elephant evidence as S080. |
| S083 | on-release | no | Same elephant evidence as S080. |
| S084 | on-release | no | crates.io API: `xdg` max_version `3.0.0`, published 2025-05-04T10:42:18Z; no release since opened. (Unpinned `latest` alias defect R18-V4 is a provenance issue, not a freshness fire.) |
| S085 | on-change | **yes\*** | omarchy: pin `v3.8.4` = `8fcc9d6` @2026-07-20; **9 newer tags** `v4.0.0…v4.5.0-rc1`; `v4.5.0-rc1` @2026-10-20T02:45-04; default branch is now `quattro` (`git ls-remote --symref HEAD`), HEAD `3ac4365` @2026-10-20T23:14+08 = 15:14Z, after opened. Cited v3.8.4 bytes immutable. Note host `~/.local/share/omarchy/version` = `3.8.3`. |
| S086 | on-change | **yes\*** | Same omarchy drift as S085 (quattro HEAD 2026-10-20T15:14Z, v4.5.0-rc1 same day); cited v3.8.4 script bytes immutable. |
| S087 | on-change | **yes\*** | Same omarchy drift as S085. |
| S088 | on-change | **yes\*** | Same omarchy drift as S085. |
| S089 | on-change | **yes\*** | Same omarchy drift as S085 (`default/walker/walker.desktop`); v4 moved the walker wiring into the new tree. |
| S090 | on-change | no | cited `pacman.log` lines 1943 (walker 2.17.0, 2026-10-11), 2929 (2.17.2, 2026-10-20T09:16:46), 3095 (elephant 2.22.1, 09:31:03) unchanged; no walker/elephant upgrade after 09:31:03; file grew only with unrelated transactions (last 13:23:09). |
| S091 | on-change | no | 3/3 digests match: `~/.config/walker/config.toml` `fecf71fa…`, `/etc/xdg/walker/config.toml` `3c5c6867…`, `/usr/bin/walker` `25240650…` (7,039,912 B). |
| S092 | on-release | no | swaybg 6 tags, max `v1.2.2` = pin; master `a59ea3d` = the row's peeled tag commit (2026-02-26). |
| S093 | on-release | **yes** | omarchy 72 tags; 9 newer than `v3.8.4`: v4.0.0 @2026-08-14 … v4.0.6 @2026-10-19T15:05-04 (=19:05Z) and `v4.5.0-rc1` @2026-10-20T06:45Z; default branch `quattro` HEAD 2026-10-20T15:14Z. Pin is a full major line behind. |
| S094 | on-release | **yes** | Same omarchy release drift as S093. Separate, pre-existing defect: the row's anchor is GitHub tree-listing HTML digests, which vary per fetch (round-18 M7 / R18-V1) and cannot be re-verified as written. |

## Notes for the frontier step

1. **S003 is the only in-lane/fleet spec that moved.** The cited prose is intact; only the line numbers shifted by 15 (`328-358`→`343-373`, `360-408`→`375-423`). A re-anchor can keep the digest rule and fix the offsets; no re-mine is needed.
2. **omarchy is the only upstream project that genuinely moved past a pin**: it renamed its default branch to `quattro` and shipped v4.0.0–v4.5.0-rc1 after the v3.8.4 pin (2026-07-20). All seven rows pinned there (S085-S089 on-change, S093-S094 on-release) are candidates for re-anchor or supersession; the host itself reports 3.8.3, so the pin was already a minor ahead of the host.
3. **xdp 1.22.1 was already superseded at row-open**: S038/S039 pinned older tags while 1.22.1 (2026-06-17) existed. Not a trigger fire by the stated rule (no release since opened), but a stale-at-open pin if L1 wants strict currency.
4. **No other upstream tag moved.** `Hyprland`, `wayland-protocols`, `xdph`, `wayland-utils`, `libinput`, `wayland`, `Waybar`, `xdg-terminal-exec`, `alacritty`, `hypridle`, `hyprlock`, `walker`, `elephant`, `swaybg` each have their row's pin as the maximum tag today.
5. **Host package moves since opened all land on the pinned versions** (walker 2.17.2, elephant 2.22.1, libinput 1.32.0, wayland 1.26.0, wayland-utils 1.3.0, hyprland 0.56.2, xdg-terminal-exec 0.14.3) — none passes a pin. R18-V3's claim "host moved to 2.17.2 at pacman.log:2929" is confirmed by file bytes (`awk 'NR==2929'`: `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`).
6. `S084`'s `latest` alias still resolves to `xdg 3.0.0` (2025-05-04); the R18-V4 pinning objection is untouched by freshness.

## Commands used (all read-only)

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 - <<'EOF'  # extract id|trigger|opened|source from corpus/SOURCES.md
git ls-remote --tags --heads <17 repo urls>
git ls-remote --symref <url> HEAD
git init -q --bare /tmp/<x> && git -C /tmp/<x> fetch -q --filter=blob:none --depth=1 <url> refs/tags/<t> && git -C /tmp/<x> log -1 --format=%cI %H FETCH_HEAD
git clone -q --bare --filter=blob:none --depth=400 https://gitlab.freedesktop.org/wayland/wayland-protocols /tmp/wp   # README last-commit probe
git clone -q --bare --filter=blob:none https://gitlab.freedesktop.org/wlroots/wlr-protocols /tmp/wlr              # ancestry/diff probe
sha256sum ~/.config/hypr/bindings.conf ~/.config/xdg-terminals.list ~/.config/alacritty/alacritty.toml /usr/share/xdg-terminal-exec/xdg-terminals.list ~/.local/share/applications/Alacritty.desktop ~/.config/walker/config.toml /etc/xdg/walker/config.toml /usr/bin/walker ~/.local/share/omarchy/default/hypr/windows.conf ~/.local/share/omarchy/default/hypr/apps/terminals.conf /usr/share/wayland/wayland.xml
grep -n 'upgraded <pkg>' /var/log/pacman.log
cd /home/vgpnk/Projects/shokunin && git show refs/heads/master:PROTOCOL.md | sha256sum && git show 31baf5c:PROTOCOL.md | sha256sum && git log -1 --format='%h %cI %s' refs/heads/master -- PROTOCOL.md
```

## Limits

- `opened` is date-only in the ledger; same-day events (omarchy `v4.5.0-rc1` 06:45Z, `quattro` HEAD 15:14Z; walker/elephant/waybar/etc. package moves between 09:16 and 09:31 -0300) cannot be ordered against the exact edit time of a row. Verdicts use the date, with timestamps shown.
- Live docs pages (S029/S030 wiki, S021-S028 news posts, S035/S036 portal spec HTML) were not re-fetched; their triggers were answered from project release tags and branch heads. A page edit that is not a release would not be seen, and page bytes are not digest anchors anyway (round-18 M7). `[UNK]` for page-byte drift.
- `S094`'s HTML tree-listing digests are unverifiable as written; not re-fetched.
- `S084` was decided from one crates.io API read made inside the eval cell (`urllib`, no receipt written, no body saved). It is a freshness check only; no digest was taken from it and no lane artifact cites it.
- Host install/version facts beyond the cited file bytes were not probed (no pacman/`-Q` queries per the host pause); only `/var/log/pacman.log` upgrade lines and the cited files were read.
- Tag lists were compared to the pins using tags only; tags re-pointed without changing name cannot be detected by `ls-remote`, though the two pins spot-checked by commit (omarchy `v3.8.4` = `8fcc9d6`, swaybg `v1.2.2` = `a59ea3d`, xdg-terminal-exec `v0.14.3` = `065925df`) still match their rows.
- No verification of the lane gate, fresh-pins counter, or QUALITY criteria was performed (out of scope; L1 owns integration).

## Installs

none.
