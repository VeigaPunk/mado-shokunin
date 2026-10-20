# PacmanLogMoves — 22 province packages upgraded (incl. 12 elephant plugins), hyprwayland-scanner removed, and the C2 counter sees only one of them

Verdict: the 2026-10-20 09:16/09:31 transactions moved **walker, elephant (+12 plugins), uwsm,
hyprland (pkgrel 2→4, rebuilt 2026-09-30), hyprtoolkit 0.5→0.6, aquamarine, omarchy-nvim,
xdg-terminal-exec** and removed **hyprwayland-scanner**; the round-19 C2 denominator
(`2.17.0` tokens) covers walker only, so 5 stale-pin classes below are structurally invisible to it.
The gate row `live.walker.version` still hard-pins `2.17.0` and would FAIL today, and the
"selftest stub" the C2 claim assumes does **not** exist in the tool. No edits made.

## 1. Method and window

- Log read as file bytes (`grep`/`sed` on `/var/log/pacman.log`); no pacman/expac/checkupdates query.
- Window: lines matching `^\[2026-10-(1[4-9]|20)T`; 694 ALPM move lines fall in it.
- Province filter (first pass) plus a broad `hypr|waybar|walker|elephant|sway|mako|omarchy|uwsm|kitty|ghostty|alacritty|foot|terminal|portal` sweep to catch names the first alternation missed (it did miss two: `hyprtoolkit`, `hyprwayland-scanner`, `xdg-terminal-exec`).
- Installed state read from `/var/lib/pacman/local/*/desc` (file bytes) — directory name + `%VERSION%`, never a query.

## 2. Moves in the window (log line `before -> after`)

| Package | Log line | Move | Installed now (desc) | Class |
|---|---|---|---|---|
| aquamarine | 2578 | 0.15.0-2 → 0.15.1-1 | `aquamarine-0.15.1-1` | patch |
| hyprtoolkit | 2729 | 0.5.4-5 → **0.6.0-1** | `hyprtoolkit-0.6.0-1` | minor bump |
| hyprland-guiutils | 2730 | 0.2.2-3 → 0.2.2-4 | `hyprland-guiutils-0.2.2-4` | pkgrel only |
| hyprland | 2733 | 0.56.2-**2** → 0.56.2-**4** | `hyprland-0.56.2-4`, `%BUILDDATE% 1790757390` = 2026-09-30 08:36:30Z | pkgrel/rebuild |
| hyprland-preview-share-picker | 2736 | 0.2.1-1 → 0.2.1-3 | `0.2.1-3` | pkgrel only |
| omarchy-nvim | 2895 | 2026.8.13-1 → 2026.9.21-5 | `omarchy-nvim-2026.9.21-5` | minor bump |
| uwsm | 2926 | 0.26.7-1 → **0.27.1-1** | `uwsm-0.27.1-1` | minor bump |
| walker | 2929 | 2.17.0-1 → 2.17.2-1 | `walker-2.17.2-1` | patch (`S096` subject) |
| xdg-terminal-exec | 2935 | 0.14.3-1 → 0.14.3-2 | `xdg-terminal-exec-0.14.3-2` | pkgrel only |
| elephant + 12 plugins | 3095-3119 | 2.21.0-1 → 2.22.1-1 (core + clipboard, runner, calc, providerlist, symbols, files, websearch, desktopapplications, bluetooth, unicode, todo, menus) | 13 × `elephant*-2.22.1-1` | minor bump |
| elephant-debug ×13 | 3096-3120 installed, **3135-3147 removed** | transient debug split packages | absent | churn |
| hyprwayland-scanner | **3156** | **removed** (0.4.6-1) | absent from local db | dependency removal |

Restart hooks for the walker plane: `:3062` (09:18:25) and `:3123` (09:31:04) `running 'walker-restart.hook'`.

**No move in the window** (last log line in parentheses): waybar 0.15.0-3 (:1944), alacritty 0.17.0-1 (:639), hypridle 0.1.8-2 (:1792), hyprlock 0.9.6-3 (:1798), hyprsunset 0.4.0-3 (:855), mako 1.11.0-1 (:1024), swaybg 1.2.2-1 (:1158), swayosd 0.3.2-1 (:1931), xdg-desktop-portal-hyprland 1.4.1-2 (:1945), hyprutils 0.14.2-1 (:1718), hyprlang 0.6.8-5 (:818), omarchy-walker 1.0.0-2 (:1110).

## 3. Stale pins found (stated → host)

### 3.1 Walker (the C2 denominator; all 13 files, 2 current at HEAD `17661e0`)

Reproduced the counter's own reading without running it: for each of the 13 files carrying `2.17.0` at `9c54c56`, the only lines matching `2\.17\.2.*S\d{3}|S\d{3}.*2\.17\.2` at HEAD are `corpus/README.md:44` and `corpus/knowledge/walker-route-r18.md:1` → **2/13**, score 1.5385, matching the claim's "2/13 now".

Stated `2.17.0` with **no same-line S### pointer** (each must gain one):

| path:line | stated | host |
|---|---|---|
| `SKILL.md:23` | "walker 2.17.0 (MADO-1 §9…)" | 2.17.2-1 |
| `SKILL.md:114` | "walker 2.17.0 via `app-walker@autostart.service`" | 2.17.2-1 |
| `SKILL.md:1075` | "`walker --version` = `2.17.0`; binary sha `64826a85…`" | 2.17.2; sha `25240650…` |
| `SKILL.md:1475` | "`walker 2.17.0-1` with `pacman -Qkk` 29 files" | 2.17.2-1 |
| `corpus/knowledge/arc-synthesis.md:229`, `:393` | version `2.17.0`, sha `64826a85…` | 2.17.2, `25240650…` (`:393` already names the new sha but no S###) |
| `corpus/knowledge/closeout-r11.md:43` | "2.17.0" | 2.17.2-1 |
| `corpus/knowledge/config-health-report-r3.md:900` | capture comment "# v0.15.0 / **2.17.0** / 0.3.2 / v0.9.6" | 2.17.2 |
| `corpus/knowledge/remaining-planes-census.md:246` | `walker 2.17.0-1` | 2.17.2-1 |
| `corpus/knowledge/walker-deep.md:27` | `--version` → `2.17.0`; pkg `2.17.0-1` | 2.17.2-1 |
| `corpus/knowledge/walker-deep-r9.md:30,58,60,78,103,110,111,305,316,317` | version/binary/help pins | 2.17.2 build |
| `corpus/knowledge/walker-live-surface.md:19,37,38` | 2.17.0, sha `64826a85…`, `32 2e 31 37 2e 30 0a` | 2.17.2 |
| `corpus/knowledge/waybar-walker-plane.md:37-38`, `:196-197`, `:405` | `2.17.0` | 2.17.2 |
| `corpus/knowledge/waybar-walker-semantics.md:23` | pkg `2.17.0-1` | 2.17.2-1 |
| `tools/mado-verify.sh:56`, `:60` | header: "version pin 2.17.0"; "pins — … walker 2.17.0" | 2.17.2 |

Note: `SKILL.md:1822-1826` (the round-18 erratum) already narrates the move and cites
`/var/log/pacman.log:2929`, but no `S###` sits on those lines, so the counter still scores SKILL.md 0.

### 3.2 Elephant (`2.21.0` → `2.22.1`; **not counted by fresh-pins.py at all**)

| path:line | stated | host | pointer |
|---|---|---|---|
| `corpus/knowledge/walker-deep.md:28` | `elephant version` → `2.21.0`; pkg `2.21.0-1` | 2.22.1-1 | only at `:624` (different line) |
| `corpus/knowledge/walker-live-surface.md:299` | "round-5 §1 pins it at 2.21.0" | 2.22.1-1 | **none** |
| `corpus/knowledge/waybar-walker-semantics.md:24` | pkg `2.21.0-1` | 2.22.1-1 | `:469` (S090 + 2.22.1) |

`corpus/knowledge/waybar-walker-plane.md:481` already declares elephant unpinned in that note.

### 3.3 uwsm (`0.26.7` → `0.27.1`; **no pointer anywhere**)

`corpus/knowledge/remaining-planes-census.md:246` "`uwsm 0.26.7-1`". Repo-wide grep for `0.27.1` = 0 hits.

### 3.4 Hyprland pkgrel and build date (`0.56.2-2` → `0.56.2-4`; version and commit unchanged)

| path:line | stated | host |
|---|---|---|
| `corpus/knowledge/hyprctl-verification-layer.md:6`, `:27`, `:160` | package `hyprland 0.56.2-2` | 0.56.2-4 |
| `corpus/knowledge/hyprland-config-plane.md:175` | package `hyprland 0.56.2-2` | 0.56.2-4 |
| `corpus/knowledge/remaining-planes-census.md:244` | `hyprland 0.56.2-2` | 0.56.2-4 |
| `corpus/knowledge/hyprctl-verification-layer.md:28` | "(build date 2026-08-05)" | `%BUILDDATE%` 1790757390 = **2026-09-30 08:36:30Z**; `/usr/bin/Hyprland` mtime 2026-09-30 05:36:30 -0300 |

These lines contain no `2.17.0`, so they are outside the C2 denominator. The commit anchor
`efb5099…` (`:28`, `:160`, `hyprland-config-plane.md:172-173`) is **still correct** (same upstream
version, pkgrel-only rebuild). The ABI token string at `hyprland-config-plane.md:174`
(`…_aq_0.15_hu_0.14_hg_0.5_hc_0.1_hlg_0.6`) remains consistent with the installed major.minors
(aquamarine 0.15.1, hyprutils 0.14.2, hyprgraphics 0.5.1, hyprcursor 0.1.13, hyprlang 0.6.8).
[INFERENCE — high] Unchanged, since hyprtoolkit 0.6.0 is *not* a direct `hyprland` dependency
(`hyprland` desc `%DEPENDS%` lists hyprgraphics/hyprlang/hyprcursor/hyprland-guiutils; hyprtoolkit
appears only under `hyprland-guiutils` as `libhyprtoolkit.so=6-64`). No executable confirmation
(`hyprctl` is not runnable under the host pause).

### 3.5 Moved packages with **no** corpus statement (nothing to re-pin)

`hyprtoolkit` 0.6.0, `omarchy-nvim` 2026.9.21, `hyprwayland-scanner` (removed), `xdg-terminal-exec`
0.14.3-2, `aquamarine` 0.15.1, `hyprland-guiutils` 0.2.2-4, `hyprland-preview-share-picker` 0.2.1-3:
repo-wide grep outside `.ufo/` returns 0 version statements for these. `terminal-route-r17.md:21`
pins the upstream **tag** `v0.14.3`, which is unaffected by the pkgrel bump.

## 4. Gate consequence (input for C2's second clause)

- `tools/mado-verify.sh:3276-3280`: `kv=$(walker --version)`; `if [ "$kv" = "2.17.0" ] … PASS "2.17.0 (pin matches)"` else `FAIL "pin changed: '$kv'; re-verify claim anchors"`. With the host at 2.17.2-1 the live row `walker.version` would report **FAIL** on the next live gate run. The live gate is not run (host pause); this is a code + host-version reading.
- **No selftest stub for this row exists.** `grep -n 'walker --version'` matches only `:3276`. The `STUB_*` census is `STUB_CONTROL STUB_EOF STUB_EXIT STUB_GIT_… STUB_OM_CMDS STUB_OM_THEME STUB_OM_VERSION STUB_RESTORE STUB_ROWS` — no walker stub. The hermetic `--selftest` sandbox (`:1036-1042`) links only coreutils/python3 into `PATH`, so no selftest arm executes `walker`. Selftest coverage of the walker plane is file-level only (`walker.config`, `:610`, `:638`, `:677`, `:1061`).
- `live.waybar.version` (`:3217`) pins `Waybar v0.15.0` and stays correct (waybar unmoved).

## 5. S096-suitable host bytes (recorded here as evidence, row ownership left to L1)

- `/usr/bin/walker`: 7,039,912 B, mtime 2026-10-08 11:14:32 -0300, `sha256 25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096` — equal to the sha already recorded at `walker-route-r18.md:183` and `corpus/SOURCES.md:103` (S091).
- Compiled-in version literal: `grep -abo '2\.17\.[02]' /usr/bin/walker` → `856302:2.17.2` (only hit). The round-9 2.17.0 literal was at 847,791, so the literal **moved +8,511 B**; consistent with the embedded-default offset move to 806,960 recorded at `walker-route-r18.md:244`.
- Package row: `/var/lib/pacman/local/walker-2.17.2-1/desc` `%VERSION% 2.17.2-1`.
- Elephant plugin shape survives 2.22.1: `/usr/lib/elephant/` holds the same 12 `*.so` names as the 2.21.0 census (bluetooth, calc, clipboard, desktopapplications, files, menus, providerlist, runner, symbols, todo, unicode, websearch) — count and names only; contents not hashed.

## 6. Recommended next-round shape (advisory, not applied)

1. Widen the freshness denominator from the `2.17.0` token to a (package, host-version) table: walker, elephant, uwsm, hyprland-*pkgrel*, hyprtoolkit, omarchy-nvim. The walker-only token test cannot see 5 of the 6 moved packages.
2. Add a second pointer form for pkgrel/build-date refreshes (`0.56.2-4`, build date 2026-09-30), since the commit anchor alone does not age.
3. When moving `live.walker.version`, treat `tools/mado-verify.sh:3277-3278` as the whole pin surface (plus comments `:56`, `:60`); no selftest coupling exists, so C2's "and its selftest stub move with it" needs either a new stub or a recorded correction of the claim.

## Limits

- No executable probe of any kind: `walker --version`, `hyprctl`, `omarchy version`, `systemctl`, `pacman -Q*` were **not** run (host pause). Host "now" values come from `/var/lib/pacman/local/*/desc` and binary/`stat`/`sha256sum` file bytes.
- `hyprctl version`'s printed build-date token is [INFERENCE] from `%BUILDDATE%`; the ABI-token equality is [INFERENCE] from installed major.minors plus the dependency graph.
- Whether the restarted walker process (`:3062`, `:3123`) now runs the 2.17.2 binary, and whether `app-walker@autostart`/`elephant` are `active`, are **[UNK]** — no process/service query under the pause.
- The 13-file denominator and the 2/13 reading were reproduced with `git ls-tree`/`git show` at `9c54c56` and HEAD `17661e0`; I did not run `fresh-pins.py` itself.
- `corpus/lessons/*`, `corpus/SOURCES.md`, `SCORECARD.md` content changes and the three tripwire drafts are out of this ticket; only `SCORECARD.md:1099-1105` was read for the C2 wording.
- One earlier raw read of the log was truncated mid-transaction (83 elided lines); the province and broad sweeps used after it were complete and are the basis for the tables.

## Installs

none
