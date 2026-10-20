# DeltaWalkerConfig — 2.17.0→2.17.2 adds four defaults (blur_corner_radius, [niri], desktopapplications edit/ctrl-e, clipboard remove/SimpleDelete); host L1 is now 305 L / 13,743 B / 3c5c6867 and the five notes' L1 pins are stale, their user-config and theme pins are not

Scope: walker default config delta between tags v2.17.0 and v2.17.2, and the claim
impact in `corpus/knowledge/{walker-deep,walker-deep-r9,walker-live-surface,waybar-walker-plane,waybar-walker-semantics}.md`.
All paths below are relative to `/home/vgpnk/Projects/shokunin/mado-shokunin` unless absolute.

## 1. Fetch and identity (OBS)

Tag→commit (`git ls-remote https://github.com/abenz1267/walker`):

| Tag | Ref line | Commit |
|---|---|---|
| `v2.17.0` | annotated: `refs/tags/v2.17.0` `2a4bde009b0d…`; peeled `^{}` | **`42b3ed88abf50bc52638fb2835b7f17e3ea3ac4c`** |
| `v2.17.1` | lightweight (no `^{}` line) | `56c9e2b69e7d2b00f0f9481ae8c89f53810c1de5` |
| `v2.17.2` | lightweight (no `^{}` line) | **`a515085fd39fae80acc086c8fbfd9b7771a9a11d`** |

Bodies + receipts: `.ufo/waves/round-19/fetch/DeltaWalkerConfig/`
(`resources-config-v2.17.0.toml`, `…-v2.17.1.toml`, `…-v2.17.2.toml`,
`…-commit-a515085.toml`, `receipts.jsonl`, 4 lines, all HTTP 200, curl 8.23.0).

| Body | Bytes | Lines | sha256 |
|---|---|---|---|
| `resources/config.toml` v2.17.0 | 13,220 | 298 | `5b4e47b7d2314bf8b2fda1e85d9e55126ef4a1f62a984f8e03f78ee6c74d63e6` |
| `resources/config.toml` v2.17.1 | 13,731 | 305 | `be6099be55c4575f39ad6e0fadc5af61f4a8ecb1d39ce4ca4a0e32b7117f3e2a` |
| `resources/config.toml` v2.17.2 | 13,743 | 305 | `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b` |
| `resources/config.toml` @ `a515085` (commit-pinned) | 13,743 | 305 | `3c5c6867…` (identical to tag body) |

Cross-checks that anchor the raw URLs to host artifacts (OBS):

- The **2.17.0** raw body is byte-identical to the config shipped in the cached
  package `/var/cache/pacman/pkg/walker-2.17.0-1-x86_64.pkg.tar.zst`
  (`tar --zstd -x`, `etc/xdg/walker/config.toml` → sha `5b4e47b7…`, 298 L).
  Its binary (`usr/bin/walker`) is sha `64826a8531eac525adfa3eff65548e93a6f7714feb1d3e13b4fa35bbcc3cfda0`, 6,661,264 B —
  exactly the binary pin in the five notes, and it embeds that config verbatim at offset 784,064.
- The **2.17.2** raw body is byte-identical to host `/etc/xdg/walker/config.toml`
  (`cmp` clean; sha `3c5c6867…`, 13,743 B, 305 L, mtime 2026-10-08 11:14:32 -03) and to
  the cached 2.17.2 package file.
- Host `/usr/bin/walker` is sha `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096`,
  7,039,912 B, mtime 2026-10-08 11:14:32 -03, `cmp`-identical to the 2.17.2 package binary.
  Package db `/var/lib/pacman/local/walker-2.17.2-1/desc`: version `2.17.2-1`,
  `%SIZE% 7123420`, builddate 1791468872 (2026-10-08 14:14:32Z), installdate 1792498606
  (2026-10-20 12:16:46Z).
- Upgrade event: `/var/log/pacman.log:2929`
  `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`.
- New binary embeds the 2.17.2 file verbatim (`embedded==file: True`) at
  `blob.find(b'force_keyboard_focus = false')` = **806,960**; the `2.17.0` literal is
  **absent** (`find → -1`) and `2.17.2` sits at 856,302.

## 2. Exact default-config delta (OBS, `diff` of the two bodies)

`diff -u` = 1 file changed, **8 insertions, 1 deletion**. All four semantic changes
land in **2.17.1**; **2.17.2 changes only the `blur_corner_radius` comment text**
(nothing else differs between the v2.17.1 and v2.17.2 bodies).

| # | Change | v2.17.2 line | v2.17.0 | Value |
|---|---|---|---|---|
| A | new top-level key `blur_corner_radius` | `:22` | absent | `20` |
| B | new `[niri]` table | `:24-27` | absent | `launch_on_empty_workspace = false`, `launch_on_startup = false`, `cmd_on_esc = ""` |
| C | new `desktopapplications` action row | `:174` | absent | `{ action = "edit", bind = "ctrl e" }` |
| D | `clipboard` `remove` action `after` | `:250` | `:243` `after = "AsyncClearReload"` | `after = "SimpleDelete"` |

A's comment moved between releases: 2.17.1 `"corner radius of the blur region (only used when ext_background_effect_blur is true)"`
→ 2.17.2 `"blur region radius on GTK older than 4.24; GTK 4.24+ uses the theme's .box-wrapper border-radius"`.

Structural corroboration in the rebuilt binary: `struct Walker with 29 elements` →
**`struct Walker with 31 elements`** (+1 scalar `blur_corner_radius`, +1 table `[niri]`);
`SimpleDelete` occurs twice (offset 817,396); the config's distinct `after` values are now
`Nothing, Close, KeepOpen, AsyncReload, AsyncClearReload, ClearReload, SimpleDelete`;
`Reload`-bearing action rows in the file drop 47 → 46 (one `AsyncClearReload` became `SimpleDelete`).

Old→new line map (needed for every anchor claim): v2.17.0 line *n* → v2.17.2 line *n* for n≤21,
*n+6* for 22≤n≤167, *n+7* for n≥168 (old `:243` → new `:250`).

## 3. Claims that depend on a changed default (direct)

| Claim (path:line) | Depends on | Was (2.17.0) | Now (2.17.2) |
|---|---|---|---|
| `corpus/knowledge/walker-deep.md:109` "binary contains `struct Walker with 29 elements` … 21 scalar keys + 6 tables … = 29" | A+B | 29 = 21 scalars + 6 tables + 2 | **31** (OBS); decomposition **22 scalars + 7 tables + 2** [INF, matches A+B exactly] |
| `corpus/knowledge/walker-deep.md:607` spot-check expects `struct Walker with 29 elements` | A+B | 29 | **31** |
| `corpus/knowledge/walker-deep.md:137-149` "every key *not* listed above is inherited … `ext_background_effect_blur=false`, and the `[shell]` block" | A+B | complete for 2.17.0 | **incomplete**: also inherited are `blur_corner_radius=20` and `[niri]` (`launch_on_empty_workspace=false`, `launch_on_startup=false`, `cmd_on_esc=""`) |
| `corpus/knowledge/walker-deep.md:163-164` "the `after` values in use: `Nothing`, `Close`, `KeepOpen`, `AsyncReload`, `AsyncClearReload`, `ClearReload`" | D | exhaustive set of 6 | **7 values**; `SimpleDelete` missing |
| `corpus/knowledge/walker-deep.md:252-254` packaged actions "apply verbatim (e.g. `desktopapplications`: Return=start, shift+Return=open+next, ctrl+Return=new_instance …; `clipboard`: Return=copy, ctrl+d=remove …)" | C+D | cited rows correct | cited rows still exist, but the enumerated examples are **incomplete** (`desktopapplications` also has ctrl e=edit) and `clipboard` ctrl-d remove no longer asks for a reload (`SimpleDelete`, not `AsyncClearReload`) |
| `corpus/knowledge/walker-deep-r9.md:176` "`Reload` \| 52 \| offset 732,314 … every hit is `after = "AsyncReload"` / `AsyncClearReload` / `ClearReload` (`/etc/xdg/walker/config.toml:117-296` carries the same rows)" | D (+A/B byte shift) | 52; rows at `:117-296` | **51**; first offset **753,642**; rows at **`:123-303`**; one row (`clipboard` remove) is now `SimpleDelete` |
| `corpus/knowledge/walker-deep-r9.md:320` spot-check "`Reload`=52 (action rows)" | D | 52 | **51** |

## 4. Whole-file identity claims invalidated by the delta (hash / size / lines / embedded offset)

The embedded-default equality itself still holds for the new pair; only the recorded
numbers moved.

| Claim (path:line) | Recorded (2.17.0) | Measured now |
|---|---|---|
| `walker-deep.md:68` embedded blob offset + equality | offset 784,064, `embedded==file: True` | offset **806,960**, equality **True**; trailing run unchanged in shape (`…visit_url" },\n]\nconfig.tomlWALKER_config not initialized…` at 820,703) |
| `walker-deep.md:69` L1 packaged | 298 L / 13,220 B / `5b4e47b7d2314bf8` / mtime 2026-07-26 21:42 | **305 L / 13,743 B / `3c5c6867d0216d0c` / mtime 2026-10-08 11:14:32 -03** |
| `walker-deep.md:587` pin table `/etc/xdg/walker/config.toml` | `5b4e47b7d2314bf8`, 13,220 B | **`3c5c6867d0216d0c`, 13,743 B** |
| `walker-deep.md:604` spot-check expected output | `784064 True` | **`806960 True`** |
| `walker-deep-r9.md:64` config layers, packaged | 13,220 B / mtime 2026-07-26 21:42:11 / `5b4e47b7…` | **13,743 B / 2026-10-08 11:14:32 / `3c5c6867…`** |
| `walker-deep-r9.md:69` embedded byte-run | offset 784,064 | **806,960** |
| `walker-deep-r9.md:291` embedded offset pin | 784,064 | **806,960** |
| `walker-deep-r9.md:334` spot-check | `784064 True` | **`806960 True`** |
| `walker-deep-r9.md:345` boundary table packaged sha | `5b4e47b7…` | **`3c5c6867…`** |
| `walker-live-surface.md:113` L0 embedded | offset 784,064, `match True` | **806,960, True** |
| `walker-live-surface.md:114` L1 packaged | `5b4e47b7d2314bf8…`, 13,220 B, mtime 2026-07-26 21:42:11 -03 | **`3c5c6867d0216d0c…`, 13,743 B, 2026-10-08 11:14:32 -03** |
| `walker-live-surface.md:258` spot-check | `784064 True` | **`806960 True`** |
| `walker-live-surface.md:277` boundary table packaged sha | `5b4e47b7d2314bf8…` | **`3c5c6867d0216d0c…`** |
| `waybar-walker-semantics.md:234` packaged default size | "298 lines" | **305 lines** |
| `waybar-walker-semantics.md:467-470` freshness pointer | flags 298/`:47`/`:112` as "not re-checked against 2.17.2" | measured: **305 L; `:53`; `:118`** — pointer's stale list is now superseded |

## 5. Line-anchor drift only (values identical, no claim falsified)

Use the map in §2. Anchors cited by the notes:

| Claim (path:line) | Old anchor | New anchor |
|---|---|---|
| `walker-deep.md:97` packaged `[providers.actions]` comment | `:112` | `:118` |
| `walker-deep.md:129` `[placeholders] default` input | `:35` | `:41` |
| `walker-deep.md:130` `quick_activate` | `:47` | `:53` |
| `walker-deep.md:131` `"symbols" = 3` | `:31-32` | `:37-38` |
| `walker-deep.md:132` `max_results = 50` | `:61` | `:67` |
| `walker-deep.md:133` `[providers] default` block | `:53-58` | `:59-64` |
| `walker-deep.md:134`, `:156`, `:266`, `:514` packaged prefixes | `:69-107` | `:75-113` |
| `walker-deep.md:245-247` `[providers]` rows (`empty`; `ignore_preview`/`sets`/`max_results_provider`/`argument_delimiter`; `clipboard.time_format`) | `:59`; `:60-67`; `:109-110` | `:65`; `:66-73`; `:115-116` |
| `walker-deep.md:250`, `:255` `[providers.actions]` table / comment | `:112-298`, `:112` | `:118-305`, `:118` |
| `walker-deep-r9.md:176` Reload rows range | `:117-296` | `:123-303` |
| `waybar-walker-plane.md:440` packaged `[providers] default` | `:53-58` | `:59-64` |
| `waybar-walker-plane.md:443` packaged `[columns]` | `:31-32` | `:37-38` |
| `waybar-walker-semantics.md:247` | `:35` | `:41` |
| `waybar-walker-semantics.md:248` | `:47`; block `:38-50` | `:53`; block `:44-56` |
| `waybar-walker-semantics.md:249`, `:261` | `:31-32` | `:37-38` |
| `waybar-walker-semantics.md:250` | `:61` | `:67` |
| `waybar-walker-semantics.md:251`, `:262`, `:386` | `:53-58` | `:59-64` |
| `waybar-walker-semantics.md:252` | `:69-107` | `:75-113` |
| `waybar-walker-semantics.md:253` | `:112-298`; `:112` | `:118-305`; `:118` |
| `waybar-walker-semantics.md:254` `[shell]` block | `:23-29` | `:29-35` |

## 6. Claims unaffected (verified, not assumed)

- **All other default values.** The body diff is exactly 8 insertions + 1 deletion (§2);
  every key outside those hunks is byte-identical. That covers `max_results=50`,
  `[providers] default/empty`, the ten packaged prefix routes, `[shell]` values,
  `ext_background_effect_blur=false`, `[placeholders]`, the twelve `[keybinds]` arrays,
  `clipboard.time_format="relative"`, `additional_theme_location` (still absent), and the
  `[providers.actions]` comment text.
- **User layer (L2).** `~/.config/walker/config.toml` re-measured: 49 L / 1,336 B /
  `fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787`, mtime 2026-10-03 17:44:32.097633418 -03 —
  identical to `walker-deep.md:70`, `walker-deep-r9.md:64`, `walker-live-surface.md:115`,
  `waybar-walker-plane.md:21`, `waybar-walker-semantics.md:445`. All user-file anchors
  (`:1-49`) and every user override value in `walker-deep.md:124-135` /
  `waybar-walker-semantics.md:246-255` are unaffected.
- **Theme pins.** `~/.local/share/omarchy/default/walker/themes/omarchy-default/layout.xml`
  `dbb6bbbe74be894a…` 6,488 B, `…/style.css` `481267af0e89a475…` 1,243 B,
  `~/.config/omarchy/current/theme/walker.css` `f44cb45063494d2f…` 191 B — unchanged
  (`walker-deep.md:365-366`, `waybar-walker-plane.md:28`).
- **Packaged theme file set.** Package db `walker-2.17.2-1/files`: same 29 paths
  (10 dirs + `config.toml` + `/usr/bin/walker` + `LICENSE` + 16 files under
  `etc/xdg/walker/themes/default/`), same names — `walker-deep.md:295-300`,
  `walker-live-surface.md:43` hold. Extracted both packages and sha256-compared all 16
  `/etc/xdg/walker/themes/default/*` files: **16/16 identical**, so the §4.4 structural
  descriptions of those files are unaffected too.
- **Reload-semantics negatives** (`walker-deep-r9.md:166-190`, `:261-266`). Re-ran the
  token census on the new binary vs the extracted 2.17.0 binary: `inotify` 0/0,
  `(?i)watch` 0/0, `restart` 0/0, `load_config`/`reload_config`/`set_config`/`file_watch`
  0/0, `config.toml` 1/1, `WALKER_` 1/1, `unknown_fields` 1/1, `(?i)notif` 3/3 (MIME only).
  "No hot-reload, restart is the apply path" is not disturbed by the delta.
- **Merge semantics** (`walker-deep.md:88-107`, arrays replace; keybinds merge per key)
  and the `[providers.actions]` inheritance fact: untouched by the delta (C/D are rows
  *inside* that inherited table).

## 7. Adjacent artifact-identity claims (same package move; not default-value dependencies)

These do not depend on a changed default, but are now false and will be read as false
alongside §4 unless re-pinned. Measured on `/usr/bin/walker` 2.17.2 vs the 2.17.0 package binary:

| Claim (path:line) | Old | New |
|---|---|---|
| `walker-deep-r9.md:57`, `walker-live-surface.md:37` binary size/sha/mtime | 6,661,264 B / `64826a85…` / 2026-07-26 21:42:11 | **7,039,912 B / `25240650…` / 2026-10-08 11:14:32 -03** |
| `walker-deep-r9.md:58`, `walker-live-surface.md:38`, `waybar-walker-plane.md:38/197/405`, `waybar-walker-semantics.md:23`, `walker-deep.md:27` version `2.17.0`/pkg `2.17.0-1` | `2.17.0` | **[INF] 2.17.2** — binary literal `2.17.0` absent, `2.17.2` at 856,302; `walker --version` **not run** (host pause forbids invoking walker) |
| `walker-deep-r9.md:60` package fields | 2.17.0-1, 6.43 MiB, Build Date Jul 26 | **2.17.2-1, %SIZE% 7,123,420 B (~6.79 MiB), build 2026-10-08 14:14:32Z** |
| `walker-deep-r9.md:109` version literal offset | 847,791 | **856,302** |
| `walker-deep-r9.md:175` `reload` label offset | 791,458 | **814,881** (same `refresh_index` row) |
| `walker-deep-r9.md:176` first `Reload` offset | 732,314 | **753,642** |
| `walker-deep-r9.md:179` `FileSource` offsets | 732,448 / 822,835 | **753,808 / 836,239** |
| `walker-deep-r9.md:180` `failed to set loaded config` offset | 784,031 | **806,884** (`Failed to set loaded config`) |
| `walker-deep-r9.md:181` `config not initialized` | 797,345 | **820,721** |
| `walker-deep-r9.md:182`, `walker-live-surface.md:130-132` `config.toml` / `WALKER_` | 797,284 / 797,295 | **820,703 / 820,714** (adjacency run unchanged) |
| `walker-deep-r9.md:183`, `:387-388` config-file error templates | 742,953 / 761,944 | **773,735 / 793,806** |
| `walker-deep-r9.md:184` `unknown_fields` | 828,369 | **870,078** |
| `walker-deep-r9.md:388-392` prose offset chain | 784,031 / 797,345 / 797,284 / 797,295 | values above |
| `walker-live-surface.md:52` help sha `ca4820a827273f6a…`; `walker-deep.md:314` flag list | 2.17.0 help blob | **[UNK]** — requires executing `walker --help`, barred by host pause |

**Pre-existing defect found, independent of the version move:** `walker-deep-r9.md:180`
records the token as lowercase `failed to set loaded config`. The **2.17.0** binary
contains **zero** lowercase occurrences and one **`Failed to set loaded config`** at
784,031 (the same offset/count the row reports); r9's own prose at `:388` spells it
capitalized. So the row's case is a transcription error that predates 2.17.2, and the
new binary keeps the capitalized form at 806,884.

## 8. Actionable summary for the owner of these notes

- Re-pin L1 everywhere to `305 L / 13,743 B / sha 3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b`
  (walker-deep 69/587, r9 64/345, live-surface 114/277, semantics 234).
- Re-run the embedded-blob spot-check to `806960 True` (walker-deep 604, r9 334, live-surface 258).
- Extend the `[providers]`/key enumerations with A/B and the `after`-value set with D
  (walker-deep 137-149, 163-164, 252-254, 607; r9 176/320).
- Apply the anchor map in §5 (mechanical, no semantic rewrites).
- Treat §7 rows as separate re-pin work; `walker --version`/`--help` need a window
  outside the host pause.

## Limits

- `walker` was never executed (host pause): version bytes, help shas, live PID/unit
  state, and "walk" behaviour are unverified; the 2.17.2 version claim is [INF] from
  binary literals only.
- 2.17.0/2.17.2 binaries were read as file bytes only, from `/usr/bin` and the pacman
  cache; the 2.17.1 binary and package were not fetched, so "all four changes landed in
  2.17.1" is supported by the config bodies at the three tags, not by a 2.17.1 binary.
- Packaged theme **contents** were compared by path list only (package db), not by hash
  against the old package; no note pins those hashes.
- `walker-route-r18.md` was not audited except as a cross-reference; it already records
  the 13,743 B / 806,960 drift at `:240-244`.
- No check of elephant or of any file outside the five named notes plus the artifacts above.

## Installs

none
